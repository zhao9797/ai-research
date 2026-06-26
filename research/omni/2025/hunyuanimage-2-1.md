---
title: "HunyuanImage 2.1：高效的 2K 高分辨率文生图扩散模型"
org: 腾讯混元
country: China
date: 2025-09
type: model-card
category: t2i
tags: [t2i, mmdit, diffusion-transformer, high-resolution, 2k, distillation, meanflow, rlhf, text-rendering, byt5, vae, repa, open-source]
url: https://huggingface.co/tencent/HunyuanImage-2.1
arxiv:
pdf_url:
github_url: https://github.com/Tencent-Hunyuan/HunyuanImage-2.1
hf_url: https://huggingface.co/tencent/HunyuanImage-2.1
modelscope_url:
project_url: https://hunyuan.tencent.com/image/en?tabIndex=0
downloaded: [hunyuanimage-2-1--hf-readme.md, hunyuanimage-2-1--github-readme.md, hunyuanimage-2-1--github-readme-cn.md, hunyuanimage-2-1--ckpts-download.md, arxiv-2509.04545-promptenhancer.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
HunyuanImage 2.1 是腾讯混元 2025-09 开源的 **17B 参数单/双流 DiT 文生图模型**，原生直出 **2K（2048×2048）分辨率**；靠 **32× 高压缩 VAE** 把 2K 图压到与别家 1K 同等的 token 长度从而大幅省算力，配 **MLLM + ByT5 双文本编码器**强化语义对齐与中英文字渲染，并用 **RLHF + meanflow 步数蒸馏**收尾。开源模型语义对齐 SSAE 达 0.8888（Mean Image Accuracy），逼近闭源 GPT-Image（0.8952），并登顶 Artificial Analysis 文生图开源模型竞技场榜首。

## 背景与定位
2025 年文生图开源主线已从 SDXL/U-Net 转向 **MMDiT/DiT + flow matching**（[[flux-1]]、[[stable-diffusion-3]]、[[qwen-image]]），竞争焦点集中在三件事：**更高原生分辨率、更强中英文字渲染、更低推理成本**。HunyuanImage 2.1 正是冲着"2K + 文字 + 速度"三杀去的：

- 相比上一代 [[hunyuan-dit]]（1.5B 级 DiT、依赖外部超分到高清），2.1 直接把**原生 2K 直出**做进 backbone（README 明确"只支持 2K，1K 会出 artifact"），并用高压缩 VAE 把高分辨率的算力代价压回 1K 量级。
- 相比同期开源标杆 [[qwen-image]]（同样强调中文与文字渲染），HunyuanImage 2.1 在自家 SSAE 语义对齐上略高（0.8888 vs 0.8854），GSB 人评对 Qwen-Image 胜率 +2.89%；对闭源 Seedream 3.0 的 GSB 胜率 -1.36%（基本打平闭源商用）。
- 技术脉络上承接 [[latent-diffusion-ldm]] 的潜空间扩散 + [[dit-scalable-diffusion-transformers]] 的 transformer backbone + [[flow-matching]]/[[rectified-flow]] 训练范式，新增高压缩 VAE（REPA/DINOv2 对齐加速）与 meanflow 少步蒸馏两条工程主线。

> 注：HunyuanImage 2.1 在发布时**没有独立的 arXiv 技术报告**（README 标注 "Report: Coming Soon"），方法披露主要在 HF model card 的 "Overall Pipeline" 章节与 GitHub README；其 PromptEnhancer 重写模块单独发了论文（arXiv 2509.04545）。后续的 HunyuanImage 3.0 才有独立技术报告（arXiv 2509.23951，已是自回归架构，属另一工作）。

## 模型架构

整体是**两阶段流水线**：基础文生图模型 → Refiner 精修模型；外挂 PromptEnhancer 重写模块。

**Backbone（基础 T2I 模型）**
- **单流 + 双流混合的 Diffusion Transformer（DiT），17B 参数**。"双流"指图像 token 与文本 token 各走独立 transformer 分支（类似 MMDiT 的 dual-stream），后段并入"单流"做联合注意力——这是 FLUX/SD3 系 MMDiT 的标准设计变体。
- 致谢中明确借鉴了 **FLUX** 与 **Qwen** 的开源工作，diffusers 生态接入。

**高压缩 VAE（核心创新之一）**
- **32×32 空间压缩率**的 VAE（远高于常见 8× / 16×），把进入 DiT 的 token 数大幅削减——其结果是"生成 2K 图所用 token 长度（因而推理时间）≈ 别家生成 1K 图"，这是 2.1 推理效率的根本来源。
- 高压缩 VAE 难训，团队用 **REPA（Representation Alignment）训练加速**：把 VAE/DiT 的特征空间与 **DINOv2** 高维语义特征对齐，缓解高压缩下的训练崩塌；并用 **multi-bucket、multi-resolution 的 REPA loss** 把 DiT 特征对齐到高维语义空间，加速收敛。

**双文本编码器（中英文字渲染的关键）**
- **MLLM（多模态大语言模型）编码器**：理解场景描述、人物动作、细节要求，强化图文对齐。官方推理代码用的是自研 **HunyuanMLLM**（发布时未放出），开源社区替代方案为 **Qwen2.5-VL-7B-Instruct**。
- **多语言、字符感知的 ByT5 编码器**：专门负责文字生成与多语言表达。具体实现为 **Glyph-SDXL-v2**（基于 google/byt5-small），即 glyph-aware 的字节级编码，是中英文"长文本、密集文字"渲染强的直接来源。

**分辨率/宽高比策略**
- 仅支持 2K 档：1:1=2048×2048、16:9=2560×1536、4:3=2304×1792、3:4=1792×2304、9:16=1536×2560 等（还支持 3:2/2:3）。多 bucket 训练对应这些宽高比。

**Refiner（第二阶段）**
- 独立的 refiner 模型，进一步提升清晰度、压制 artifact。具体架构/训练细节官方未单独披露。

## 数据

官方对数据规模/配比披露较粗，但**结构化 caption 体系**讲得较细：

- **分层结构化 caption**：为每张图提供 **short / medium / long / extra-long 四个层级**的语义描述，提升模型对复杂语义的响应能力。
- **多专家模型协作标注**：引入 **OCR agent** 补强密集文字场景的描述，引入 **IP RAG**（检索增强）补强世界知识/IP 类描述——这两点是为弥补通用 VLM captioner 在"密集文字 + 世界知识"上的短板。
- **双向验证策略（bidirectional verification）**保证 caption 准确性。
- 训练数据总规模、图文对数量、来源构成、美学/安全过滤细节 **未披露**。

## 训练方法

**主训练目标**：扩散 / flow 范式（推理用 flow-style 采样，README 配置含 `shift` 参数，符合 rectified-flow 风格的时间步重排；官方未逐字写 "rectified flow"，但配置与 FLUX/SD3 系一致）。

**两阶段后训练（RLHF）**
- **SFT → RL 顺序进行**的两阶段后训练。
- RL 阶段提出 **Reward Distribution Alignment（奖励分布对齐）算法**：创新地把**高质量真实图像作为 selected 样本**纳入，稳定并提升强化学习效果（缓解 RLHF 中 reward hacking / 训练不稳）。目标是优化美学与结构一致性。

**蒸馏与加速（核心创新之二）**
- 提出基于 **meanflow** 的新蒸馏方法，解决标准 meanflow 训练**不稳定、低效**的痛点，实现少步采样下的高质量生成。
- 官方称这是 **meanflow 首次成功应用于工业级（大规模）模型**。
- 实际效果：蒸馏模型 **8 步**即可出图（非蒸馏 50 步）。

**PromptEnhancer 重写模块（单独论文 arXiv 2509.04545，方法已精读）**
- 定位为"首个系统化工业级重写模型"，**与生成器解耦**、对任意预训练 T2I 模型通用（无需改 T2I 权重）。
- 训练两阶段：
  - **Stage 1 SFT**：基座为 **Hunyuan-7B-Instruct**，在 **485,119 条 (user prompt, CoT, reprompt) 三元组**上做 SFT，学会 Chain-of-Thought 式结构化重写；数据来自 **3.26M 图池（1.53M 中文向 + 1.73M 英文向）**经 image-caption 模拟出的 **2.26M proxy user prompt**，经"用户 prompt 模拟 → **Gemini-2.5-Pro** 生成 CoT/多候选 → Gemini-2.5-Pro 自动过滤（1M→611,921 三元组）→ 人在环选优（→485,119）"四步管线构造（主题分布：Design 27% / Art 23% / Film&Story 22% / Illustration 18% / Creative 10%）。effective batch size 128，warmup 10%。
  - **Stage 2 GRPO**：用 **AlignEvaluator 奖励模型**做策略对齐，学习率降到 **1.0×10⁻⁶**（cosine→constant），rollout 每 prompt 采 **N=8** 候选，KL 系数 0.001，global batch 64；RL prompt 集约 **5 万条**（与 SFT 图源不相交，防泄漏）。注：epoch 数论文自相矛盾——正文写"GRPO for 10 epochs"，但 Table 2 明确列 GRPO Epochs=1（SFT 同样正文写 10、表里写 2），以权威超参表为准取 **1**。
- **AlignEvaluator** 奖励模型：基于 **24 个细粒度 key point（归为 6 大类）**的 T2I-KeyPoints 体系打分（覆盖否定、代词指代、属性绑定、构图关系、计数、世界知识等 T2I 常见失败模式），输出标量奖励——比 CLIP score / 通用人偏分更细粒度。
- 线上版用的是 **PromptEnhancer-32B**（更高质量重写），HF model card 侧把该模块描述为 SFT 结构化重写 + GRPO（AlignEvaluator 覆盖"6 大类 24 细粒度点"，与论文一致）。

## Infra（训练 / 推理工程）

- **主模型训练算力/GPU·时/并行策略/混合精度/吞吐：官方未披露**（HunyuanImage 2.1 本体无独立技术报告，model card 未给训练集群数字）。
- **唯一披露的训练 infra 是 PromptEnhancer 子模块**（arXiv 2509.04545）：训练与推理全程在 **8×NVIDIA H800** 上完成，bfloat16 混合精度；SFT 用 per-device batch 8 + 2 步梯度累积凑 effective batch 128。基座 HunyuanImage 2.1 权重全程冻结（plug-and-play）。
- **推理工程**（有具体数字）：
  - **FP8 量化模型**：开 CPU offloading + FP8 后，**仅需 24GB 显存**即可生成 2048×2048（2025-09-12 发布）。
  - **推理效率根因**：32× 高压缩 VAE 使 2K 图的 token 长度 ≈ 别家 1K，单步算力大降；叠加 meanflow 蒸馏把步数从 50 压到 8。
  - **采样配置**：非蒸馏 50 步 / guidance 3.5 / shift 5；蒸馏 8 步 / guidance 3.25 / shift 4。推荐开 prompt enhancement + refiner 全流程以获最佳质量。
  - 依赖 flash-attn 2.7.3，仅支持 Linux + NVIDIA CUDA。
  - 社区已提供 ComfyUI workflow。
- 部署形态：开源权重（HF/ModelScope）+ 官网在线体验（hunyuan.tencent.com modelSquare）。

## 评测 benchmark（把效果讲清楚）

**SSAE（Structured Semantic Alignment Evaluation，自建语义对齐指标）**
- 方法：12 类共 3500 个 key point，用 MLLM 对照生成图自动打分。Mean Image Accuracy = 图级平均；Global Accuracy = 全 key point 平均。

| 模型 | 开源 | Mean Image Acc | Global Acc |
|---|---|---|---|
| FLUX-dev | ✅ | 0.7122 | 0.6995 |
| Seedream-3.0 | ❌ | 0.8827 | 0.8792 |
| Qwen-Image | ✅ | 0.8854 | 0.8828 |
| GPT-Image | ❌ | 0.8952 | 0.8929 |
| **HunyuanImage 2.1** | ✅ | **0.8888** | **0.8832** |

结论：开源模型中语义对齐 **SOTA**，逼近闭源商用 GPT-Image（差距约 0.6pp）。分项里 HunyuanImage 2.1 在 "Scene Noun"（0.9615）、"Scene Attributes"（0.9254）等场景维度甚至领先全场。

**GSB 人评（1000 prompt，>100 名专业评测员，单次推理不挑图）**
- 对 **Seedream 3.0（闭源）**：相对胜率 **-1.36%**（基本打平闭源）。
- 对 **Qwen-Image（开源）**：相对胜率 **+2.89%**（领先同类开源）。

**竞技场榜单**
- 2025-09-16 登顶 **Artificial Analysis 文生图开源模型 Arena 榜首（Top1）**。

**PromptEnhancer 消融（来自 arXiv 2509.04545，base = HunyuanImage 2.1）**
- 在自建 24 维 benchmark 上，加重写后 **平均准确率 +5.1%**；15 个类别提升 >5.0%。
- 提升最大的维度：Similarity Relation **+17.3%**、Counterfactual **+17.2%**、Counting **+15.0%**、Pronoun Resolution **+13.9%**、Expression **+12.0%**、Cross-Entity Binding **+11.3%**。
- 个别维度无提升/微降：Contact Interaction / Size +0.0%、Artistic Style +0.9%、Text Layout -0.7%、Interaction w/o Contact -0.9%。

**未报告**：FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、HPSv2、ImageReward、PickScore 等标准学术 benchmark 官方均未单独给出（官方主打自建 SSAE + GSB 人评 + Arena 榜）。

## 创新点与影响

**核心贡献**
1. **32× 高压缩 VAE + REPA/DINOv2 对齐训练**：把原生 2K 直出的 token/算力代价压回 1K 量级，是"高分辨率开源直出"在工程上可行的关键。
2. **meanflow 工业级蒸馏**：首次把 meanflow 蒸馏稳定地用到大规模模型上，8 步出 2K 图。
3. **MLLM + ByT5(Glyph-SDXL-v2) 双编码器**：把中英文密集文字渲染做到开源第一梯队，配合 OCR agent + IP RAG 的结构化 caption。
4. **Reward Distribution Alignment RLHF + 解耦式 PromptEnhancer（CoT 重写 + AlignEvaluator 细粒度奖励）**：把"语义对齐"从隐式 CLIP/偏好分细化到 24 个可诊断 key point。

**影响**
- 把开源文生图的"原生 2K + 中英文字 + 低显存（24GB 可跑）"门槛一次性拉齐到闭源商用水平，成为电商/营销/游戏等场景的可商用基座（社区 ComfyUI 生态快速跟进）。
- PromptEnhancer 作为"模型无关、与生成器解耦"的重写框架，可外挂到任意 T2I 模型，被论文证明对 FLUX/Qwen-Image 等同样有效，具一般适用性。
- 是腾讯混元图像线从 HunyuanDiT → HunyuanImage 2.1（DiT 扩散）→ HunyuanImage 3.0（自回归统一）演进中的关键扩散范式里程碑。

**已知局限**
- 仅支持 2K 档生成，1K 会出 artifact（缺乏分辨率灵活性）。
- 自研 HunyuanMLLM 文本编码器与训练算力细节未开源/未披露，复现需用 Qwen2.5-VL-7B 替代。
- 缺独立技术报告与标准学术 benchmark（FID/GenEval/T2I-CompBench 等）数字，外部横评依赖自建 SSAE/GSB。
- 重写对极少数维度（文字排版、无接触交互）有轻微负作用。

## 原始链接
- hf (model card / 主页面): https://huggingface.co/tencent/HunyuanImage-2.1
- github: https://github.com/Tencent-Hunyuan/HunyuanImage-2.1
- ckpts 组件说明: https://github.com/Tencent-Hunyuan/HunyuanImage-2.1/blob/main/ckpts/checkpoints-download.md
- project page: https://hunyuan.tencent.com/image/en?tabIndex=0
- 官网在线体验: https://hunyuan.tencent.com/modelSquare/home/play?modelId=286
- PromptEnhancer 论文 (arXiv 2509.04545): https://arxiv.org/abs/2509.04545
- PromptEnhancer 项目页: https://hunyuan-promptenhancer.github.io
- PromptEnhancer-32B (HF): https://huggingface.co/PromptEnhancer/PromptEnhancer-32B

## 一手源存档（sources/）
- [hf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuanimage-2-1--hf-readme.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuanimage-2-1--github-readme.md)
- [github-readme-cn.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuanimage-2-1--github-readme-cn.md)
- [ckpts-download.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuanimage-2-1--ckpts-download.md)
- arxiv-2509.04545-promptenhancer.pdf  （PDF 不入 git，走 HF bucket）
