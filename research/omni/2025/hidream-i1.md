---
title: "HiDream-I1: A High-Efficient Image Generative Foundation Model with Sparse Diffusion Transformer"
org: "智象未来 (HiDream.ai)"
country: China
date: "2025-05"
type: tech-report
category: t2i
tags: [text-to-image, dit, mmdit, moe, sparse-moe, flow-matching, distillation, dmd, gan, open-source]
url: "https://arxiv.org/abs/2505.22705"
arxiv: "https://arxiv.org/abs/2505.22705"
pdf_url: "https://arxiv.org/pdf/2505.22705"
github_url: "https://github.com/HiDream-ai/HiDream-I1"
hf_url: "https://huggingface.co/HiDream-ai/HiDream-I1-Full"
modelscope_url: ""
project_url: "https://vivago.ai/studio"
downloaded: [arxiv-2505.22705.pdf, hidream-i1--readme.md, hidream-i1--hf-modelcard.md, hidream-i1--hf-config.json]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
HiDream-I1 是 HiDream.ai（智象未来）2025 年 4 月开源、5 月发技术报告的 **17B 参数稀疏 MoE 文生图基础模型**，核心创新是把 **Sparse Mixture-of-Experts（4 专家路由 top-2 + 1 共享专家）植入 MMDiT 双流+单流 DiT 骨干**，用 flow matching 训练、再用 **GAN-powered DMD 蒸馏**出 28/16 步快版。发布时在三大 benchmark 领先开源阵营：GenEval **0.83**、DPG-Bench **85.89**、HPSv2.1 平均 **33.82**。GenEval/DPG 两表上 overall 均超 FLUX.1-dev / SD3-Medium / Janus-Pro-7B / CogView4-6B；HPS 表 overall 第一（超 Flux.1-dev 32.47、Stable Cascade 32.95 等，该表未列 Janus-Pro-7B）。

## 背景与定位
当时第一梯队 SOTA（Midjourney、DALL·E 3、Imagen、[[flux-1]] 系、[[stable-diffusion-3]]）普遍以更大算力换质量，推理慢、部署成本高。HiDream-I1 的命题是 **在不牺牲质量的前提下做"高效"**——做法不是缩小模型，而是用 **稀疏激活的 MoE** 在 17B 总参里只激活一部分专家，让"等效容量大、单步算力可控"，再叠加蒸馏把 50 步压到 16 步实现"秒级出图"。

技术脉络上它直接站在 [[stable-diffusion-3]] 的 MMDiT（双流 rectified-flow transformer）和 [[flux-1]]（单流 DiT + Flux VAE）肩上：复用了 FLUX.1 [schnell] 的 VAE、借鉴 MMDiT 的双流设计与 QK-Norm，把二者的"双流→单流"拼成混合骨干，并在两段都换成 MoE FFN。与同期国产开源 [[cogview4]]（6B 单流 DiT）、字节 [[janus-pro]]（7B 统一理解+生成自回归）相比，HiDream-I1 走的是"纯扩散 + 大稀疏专家 + 四编码器超强 prompt 理解"的路线。其上还衍生出指令编辑模型 HiDream-E1 与对话式图像 agent HiDream-A1（vivago.ai）。

## 模型架构
基于 **flow matching**（Lipman 2022）在 latent 空间建模，骨干是自研 **Sparse DiT**。精确结构（来自 HF `transformer/config.json`，paper 正文未给全数字）：

**Hybrid Text Encoding（四编码器混合）**——这是 HiDream-I1 prompt 理解强的关键，集成四路文本表征：
1. **Long-Context CLIP-L/14 + CLIP-G/14**（Long-CLIP，Zhang 2024，支持更长 token），池化成全局向量 h_clip，经 **adaLN** 做全局条件注入；
2. **T5-XXL** encoder，输出序列级 token 嵌入 h_t5（4096 维）；
3. **Decoder-only LLM = Llama-3.1-8B-Instruct**，关键在于**从多个中间层抽特征** h_llm（config 中 `llama_layers` 列出层 0–31 再追加多次第 31 层，共 48 个 tap），保留末层易被稀释的细粒度语义。

T5 与所选 Llama 层的序列嵌入经线性投影后 **拼接**成主文本条件序列喂入 DiT；Long-CLIP 池化向量走 adaLN 全局调制。`caption_channels=[4096,4096]`（T5 + Llama），内部 `text_emb_dim=2048`。

**Sparse DiT Backbone**（在 patch 化 latent 上操作，patch_size=2，in/out_channels=16=FLUX VAE latent）：
- **Dual-stream DiT blocks（num_layers=16）**：仿 MMDiT，图像 patch token 与文本 token 走两条并行通路，各自独立特征抽取，在 attention 内交互；
- **Single-stream DiT blocks（num_single_layers=32）**：双流末层输出的图/文 token 沿序列维拼接，后续全部 block 在合并序列上统一处理；
- **attention**：`num_attention_heads=20`、`attention_head_dim=128`（hidden=2560），带 **RoPE**（paper/图3 标注 "Attention w RoPE"；config `axes_dims_rope=[64,32,32]` 表明 head_dim 沿 3 个轴分段做旋转位置编码），并用 **QK-Norm**（QK-normalization，引 Esser 2024=SD3）稳训练；
- **Sparse MoE FFN**：双流与单流 block 的 FFN 都换成 MoE——`num_routed_experts=4`、`num_activated_experts=2`（top-2 路由）外加 **1 个共享专家（shared expert）**，专家是 **SwiGLU**；router 轻量门控按 token 特征动态路由。这正是 17B 总参 + 稀疏激活"等效大容量、单步省算力"的来源。
- **条件与稳定性**：Long-CLIP 池化特征 + 正弦 timestep 嵌入经 adaLN 在每个 block 做 Scale&Shift 调制；QK-Norm 保稳。

**三个变体**：HiDream-I1-Full（50+ 步）、HiDream-I1-Dev（guidance 蒸馏，28 步）、HiDream-I1-Fast（16 步；注：摘要写 14 步、正文§5 与 README 写 16 步，存在不一致，以 16 步为最终发布口径）。

## 数据
四阶段数据预处理 pipeline（Figure 2）：
- **采集（Collection）**：web 来源数据集 + 内部版权图像；web 数据连同 tag/描述等文本一起抓；刻意覆盖多样风格、主题、分辨率、长宽比。**总规模未披露**。
- **去重（Deduplication）**：两阶段——(1) 用 SOTA **SSCD** 模型抽视觉特征，对 200 万特征子集做 **k-means 聚成 16000 簇**；(2) 簇内用 GPU 加速 **Faiss** 精确相似度搜索，超阈值判近重复删除。**共删约 20%** 图像。
- **过滤（Filtering）**：① NSFW 内容安全（LAION CLIP-NSFW 分类器）；② 美学打分（LAION aesthetic predictor）卡阈值；③ 水印检测（LAION-5B watermark detection）；④ 技术质量——Top-IQ 质量评估低分剔除 + 临时 JPEG 编码算 bytes-per-pixel，过低（细节差/压缩重）剔除。
- **标注（Annotation）**：用 **MiniCPM-V 2.6** VLM 重新打 caption，输入兼含图像内容与原有 metadata（用户 tag/短描述）以提精度降幻觉；用**新提示策略生成不同长度的 caption** 以贴近真实用户 prompt 分布。
- **后训练数据**：人工标注的高美学、富结构、文图对齐经人审核的高质量图文对（规模见训练节，20k 步）。

## 训练方法
**Latent Flow Matching** 目标：在 noise X0~N(0,I) 与目标图 X1 间走线性插值路径 Xt=(1−t)X0+t·X1，常速度场 Vt=X1−X0，模型预测速度场 u(Xt,y,t;θ)，最小化 MSE（式 1）。

**多阶段：**
1. **预训练（渐进分辨率）**——latent 由 **FLUX 预训练 VAE** 预先编码并缓存（加速）。三段渐进：
   - 256×256（保持长宽比的最大内接尺寸）：**600,000 步**，batch **24/GPU**；
   - 512×512：**200,000 步**，batch **8/GPU**；
   - 1024×1024：**200,000 步**，batch **2/GPU**。
   优化器 **AdamW**，lr=1e-4，1000 步线性 warmup，必要时衰减。
2. **后训练（对齐微调）**——在高美学/对齐人审高质数据上微调 **20,000 步**，lr=1e-5，global batch **64**，提升 prompt fidelity、美学与偏好对齐。（注：本报告**未用 RLHF/DPO/reward model**，后训练为有监督对齐微调。）

**推理加速——GAN-powered Diffusion Distillation**（核心创新之一）：
- 主蒸馏目标用 **DMD**（Distribution Matching Distillation，Yin 2024），把 student（Dev/Fast）的轨迹分布对齐 teacher（Full）；
- 叠加 **对抗损失 L_adv**：student 当生成器，配一个判别器判 VAE 解码图真实度，**判别器用冻结 teacher backbone 的多层特征**驱动分类——借 GAN 补回扩散蒸馏常丢失的细节与锐利边缘；
- 总目标 L_total = L_DMD + λ_adv · L_adv。把 Full 蒸成 Dev（28 步）与 Fast（16 步）。

## Infra（训练 / 推理工程）
- 分布式/精度：**FSDP（Fully Sharded Data Parallel）+ 混合精度 + 梯度检查点（gradient checkpointing）**；latent 预计算缓存以省 VAE 前向。
- **算力规模、GPU 卡数·时、吞吐均未披露**（report 仅列 batch/step）。Infra 贡献者：Fengbin Gao、Peihan Xu、Yimeng Wang、Kai Yu。
- 推理：Full 50 步、Dev 28 步、Fast 16 步；diffusers 集成（`HiDreamImagePipeline`，scheduler=`UniPCMultistepScheduler`），需 Flash Attention，推荐 CUDA 12.4。权重 bf16。部署形态：开源权重（MIT）+ HF Space + diffusers + vivago.ai 产品/agent。具体量化、缓存策略未单独披露。

## 评测 benchmark（把效果讲清楚）
数字均来自技术报告 Table 1–4 与 README（与论文一致）。

**DPG-Bench（prompt 对齐准确率 %，越高越好）** — HiDream-I1 **Overall 85.89 第一**：
| 模型 | Overall | Relation | Other |
|---|---|---|---|
| Flux.1-dev | 83.79 | 90.04 | 89.90 |
| SD3-Medium | 84.08 | 80.70 | 88.68 |
| Janus-Pro-7B | 84.19 | 89.32 | 89.48 |
| CogView4-6B | 85.13 | 91.14 | 87.29 |
| **HiDream-I1** | **85.89** | **93.74** | **91.83** |

强项在复杂关系（Relation 93.74，全场最高）与细节指令（Other 91.83）；Global 仅 76.44 相对偏弱。

**GenEval（组合生成准确率，越高越好）** — **Overall 0.83 第一**：
| 模型 | Overall | Single | Two Obj | Counting | Colors | Position | Color Attr |
|---|---|---|---|---|---|---|---|
| SD3-Medium | 0.74 | 0.99 | 0.94 | 0.72 | 0.89 | 0.33 | 0.60 |
| Janus-Pro-7B | 0.80 | 0.99 | 0.89 | 0.59 | 0.90 | **0.79** | 0.66 |
| **HiDream-I1** | **0.83** | **1.00** | **0.98** | **0.79** | **0.91** | 0.60 | **0.72** |

单/双物体、计数、颜色、颜色归属均最高；唯一短板是 **Position 0.60**（落后 Janus-Pro 的 0.79）。

**HPSv2.1（预测人类偏好，越高越好）** — **平均 33.82，五项全类第一**：
| 模型 | 平均 | Animation | Concept-art | Painting | Photo |
|---|---|---|---|---|---|
| Flux.1-dev | 32.47 | 33.87 | 32.27 | 32.62 | 31.11 |
| Stable Cascade | 32.95 | 34.58 | 33.13 | 33.29 | 30.78 |
| **HiDream-I1** | **33.82** | **35.05** | **33.74** | **33.88** | **32.61** |

超过 Midjourney V5/V6、SDXL、DALL·E 3、SD3、Flux.1-dev、Stable Cascade 等。

**HiDream-E1 编辑评测（GPT-4o 自动评，取"执行成功"与"无过度编辑"两项最小值，0–10）** — EmuEdit 平均 **6.40**、ReasonEdit **7.54**，均第一，超 OmniGen、UltraEdit、MagicBrush 及闭源 Gemini-2.0-Flash（EmuEdit 5.99 / ReasonEdit 6.95）；EmuEdit 子任务在 Global/Text/Color/Style/Remove/Local 多数类目居首。

**消融**：报告未给定量消融表（无 MoE vs 稠密、四编码器逐一拆解的对照数字），属本工作的披露缺口。

## 创新点与影响
**核心贡献：**
1. **Sparse MoE × MMDiT 双流+单流混合骨干**——把动态 MoE（4 专家 top-2 + 1 共享专家、专家为 SwiGLU）系统性引入文生图 DiT 双流与单流两段的开源工作（彼时同期开源 T2I 多为稠密 DiT），用稀疏激活把"17B 总参等效容量"与"可控单步算力"解耦，体现 paper 主打的"高效"（cost-effectiveness）主张。（注："等效容量"是论文论证而非实测，报告未给 MoE-vs-稠密的量化对照。）
2. **四编码器混合文本编码（Long-CLIP×2 + T5-XXL + Llama-3.1-8B 多中间层 tap）**——直接转化为 GenEval/DPG 上领先的 prompt-following。
3. **GAN-powered DMD 蒸馏**——把对抗学习引入 DMD 蒸馏，用冻结 teacher 多层特征当判别器，缓解扩散蒸馏丢细节/边缘的通病，做到 16 步秒级出图且不糊。
4. **完全开源（MIT）且商用友好**——Full/Dev/Fast 三档权重 + 代码 + diffusers 集成全开，发布即领先开源阵营，对社区影响大；衍生 HiDream-E1（编辑，in-context 侧拼 latent + 空间加权 loss，5M 三元组微调）与 HiDream-A1（Coordinator+Planner 的对话式图像 agent），形成"生成→编辑→agent"完整栈，对标 GPT-4o 的"说图即出"。

**已知局限：**
- DPG-Global（76.44）、GenEval-Position（0.60）相对偏弱；
- 训练**总数据量、算力规模、GPU·时全未披露**；
- **无定量消融**支撑 MoE/四编码器各自增益；
- 依赖外部组件（FLUX VAE、Llama-3.1-8B 需同意 license、T5-XXL）增加部署门槛；
- Fast 步数文档不一致（14 vs 16）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2505.22705
- arxiv_pdf: https://arxiv.org/pdf/2505.22705
- github: https://github.com/HiDream-ai/HiDream-I1
- hf: https://huggingface.co/HiDream-ai/HiDream-I1-Full
- hf_config: https://huggingface.co/HiDream-ai/HiDream-I1-Full/raw/main/transformer/config.json
- project: https://vivago.ai/studio
- 衍生: https://github.com/HiDream-ai/HiDream-E1

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2505.22705.pdf （技术报告 PDF，10 页，已精读全文）
- ../../../sources/omni/2025/hidream-i1--readme.md （GitHub README + benchmark 表）
- ../../../sources/omni/2025/hidream-i1--hf-modelcard.md （HF model card，含组件 license 与 benchmark）
- ../../../sources/omni/2025/hidream-i1--hf-config.json （HF transformer/config.json + model_index.json 摘录：精确架构数字）
