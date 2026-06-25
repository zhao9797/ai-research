---
title: "Qwen-Image-Edit / Qwen-Image-Edit-2509"
org: "阿里巴巴 Qwen 团队"
country: China
date: "2025-08"
type: model-card
category: edit
tags: [image-editing, mmdit, flow-matching, text-rendering, dual-encoding, qwen2.5-vl, instruction-edit, controlnet]
url: "https://huggingface.co/Qwen/Qwen-Image-Edit"
arxiv: "https://arxiv.org/abs/2508.02324"
pdf_url: "https://arxiv.org/pdf/2508.02324"
github_url: "https://github.com/QwenLM/Qwen-Image"
hf_url: "https://huggingface.co/Qwen/Qwen-Image-Edit"
modelscope_url: "https://modelscope.cn/models/Qwen/Qwen-Image-Edit"
project_url: "https://qwenlm.github.io/blog/qwen-image-edit/"
downloaded: [arxiv-2508.02324.pdf, qwen-image-edit--hf-card.md, qwen-image-edit-2509--hf-card.md, qwen-image-edit--blog.md, qwen-image--github-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Qwen-Image-Edit 是基于 20B 的 [[qwen-image]] 基座（MMDiT + Qwen2.5-VL + Wan2.1-VAE）扩展出的指令式图像编辑模型，核心创新是把输入图像**同时喂给 Qwen2.5-VL（语义控制）和 VAE Encoder（外观/像素控制）的双编码机制**，从而在「语义编辑」（IP 创作、旋转视角、风格迁移）与「外观编辑」（增删改局部、其它区域不变）两条路径上都成熟，并把基座的中英文精准文字渲染能力延伸到「改图里的字」。在公开编辑基准 GEdit-Bench 上取得 EN 8.00/7.86/7.56、CN 7.82/7.79/7.52（SC/PQ/O，GPT-4.1 评分）的 SOTA，ImgEdit 总分 4.27（略高于 GPT Image 1 [High] 的 4.20）。

## 背景与定位
指令式图像编辑（text-image-to-image, TI2I）面临两难：
1. **视觉一致性（visual consistency）**——只改目标区域、其它像素必须保持（如改发色不能动脸）；
2. **语义连贯性（semantic coherence）**——做结构变化时全局语义要守住（如改姿态但保人物身份与场景）。

技术报告指出，即便 GPT Image 1、Seedream 3.0 这类闭源 SOTA 在多行文字、非字母语言（中文）、局部插字、图文融合等场景仍吃力。Qwen-Image-Edit 站在 [[flux-1-kontext]]（首次系统化「in-context 编辑」并验证 VAE embedding 有助一致性）与 [[step1x-edit]]、[[seededit]] 等工作之上，把编辑统一进基座的多任务训练范式（T2I + TI2I + I2I 重建），并靠基座本身极强的中文文字渲染拉开「文字编辑」这一差异化优势。它本质是 Qwen-Image 技术报告里 §4.3 Multi-task training + §5.2.3 Image Editing 章节落地的开源权重，2025-08-18 开源，Apache-2.0。

技术脉络位置：扩散/整流流编辑路线（相对 [[latent-diffusion-ldm]]→[[stable-diffusion-3]] MMDiT→FLUX.1 Kontext 编辑），强调「编辑即统一多任务」而非单独训一个编辑头。

## 模型架构
完全复用 Qwen-Image 基座的三件套（technical report Fig.6 / Table 1）：

- **Backbone：MMDiT（双流 Multimodal Diffusion Transformer）**，60 层、24/24（Q/KV）头、head size 128、intermediate 12288、patch/scale factor 2、**20B 参数**。RMSNorm 做 QK-Norm，其余归一化用 LayerNorm。
- **条件编码器（text/语义流）：Qwen2.5-VL（7B）**，整体冻结，取语言主干最后一层 hidden state 作为条件 latent。选 Qwen2.5-VL 而非纯语言 Qwen3 的三个理由：①视觉/语言空间已对齐，更适合 T2I；②语言建模能力没退化；③天生支持多模态输入，从而可解锁图像编辑——编辑时用户图像的 visual patch 经其内置 ViT 编码、与文本 token 拼成序列送入文本流。
- **图像 tokenizer：Wan2.1-VAE**，单编码器/双解码器（图像+视频共享 encoder，各自 decoder），**8×8 压缩、latent 通道 16**。冻结 encoder，仅微调 image decoder（在 PDF/PPT/海报等富文本语料 + 合成段落上训），用重建损失+感知损失（动态调比例、放弃对抗损失），专为小字/细节重建服务。Qwen-Image-VAE 在 ImageNet-256 PSNR 33.42 / SSIM 0.9159、富文本集 PSNR 36.63 / SSIM 0.9839，均为对比 SOTA。
- **位置编码：MSRoPE（Multimodal Scalable RoPE）**——文本作为对角线上的 2D token（两维同 position id），图像从中心开始编码，兼得分辨率缩放优势与文本侧等价于 1D-RoPE。**编辑（TI2I）专属改动**：在 height/width 之外**新增一个 frame 维度**区分「编辑前/编辑后」多张图（technical report Fig.14 右）。

**编辑的核心条件注入——双编码（dual-encoding）机制**（这是 Edit 区别于纯 T2I 的关键，HF 卡 + blog + report §4.3 三方一致）：
- 输入图像经 **Qwen2.5-VL** 抽**语义特征**（高层场景理解、上下文），送入文本流 → 负责 instruction following + 语义编辑；
- 同一张输入图像经 **VAE Encoder** 抽**重建特征**（低层像素细节），其 latent **沿序列维与 noised image latent 拼接**送入图像流 → 负责保真度与结构一致性。
- 报告的经验结论：MLLM 语义 embedding 让指令遵循更好，叠加 pixel-level VAE embedding 进一步提升视觉保真与结构一致——二者互补，正是「语义编辑 + 外观编辑双路成熟」的来源。

**分辨率策略**：基座做 256p→640p→1328p 渐进，多宽高比（1:1/2:3/3:2/3:4/4:3/9:16/16:9/1:3/3:1）。

**2509 版（Qwen-Image-Edit-2509，2025-09-22）架构层面的增量**（来自 HF 卡）：
- **多图编辑**：在 Edit 架构上**通过图像拼接（image concatenation）继续训练**得到，支持「人+人」「人+商品」「人+场景」，最佳 1~3 张输入；推理走 `QwenImageEditPlusPipeline`。
- **原生 ControlNet**：深度图、边缘图、关键点图等作为条件原生支持（此前需外挂）。
- **单图一致性增强**：人物 ID/姿态、商品身份、文字（除内容外还可改字体/颜色/材质）。

## 数据
编辑模型未单独公布编辑数据集规模，数据细节均出自基座技术报告（编辑沿用同一数据/管线 + TI2I 任务数据）：

- **总规模**：数十亿（billions）图文对；强调质量与分布均衡而非纯堆量。四大域：**Nature ~55%**（物体/风景/城市/植物/动物/室内/食物）、**Design ~27%**（海报/UI/PPT/绘画雕塑数字艺术，富文字与复杂版式）、**People ~13%**（肖像/运动/人类活动）、**Synthetic ~5%**（仅指受控文字渲染合成，**明确排除其它 AI 模型生成图**以避伪影/幻觉）。
- **七阶段过滤管线（S1–S7）**：S1 初筛（破损/文件大小/分辨率<256p/去重/NSFW）；S2 画质（旋转/清晰度/亮度 Luma/饱和度/熵/纹理）；S3 图文对齐（Raw/Recaption/Fused 三路 caption + Chinese-CLIP & SigLIP2 过滤 + token 长度/无效 caption 过滤）；S4 文字渲染增强（按语言切 EN/ZH/Other/Non-text 四路，引入合成文字数据，密集文字/小字过滤）；S5 高分辨率精修（640p，画质/分辨率/美学/异常元素如水印二维码过滤）；S6 类别均衡与肖像增强（General/Portrait/Text 三类重平衡、检索补патч、人脸去马赛克）；S7 平衡多尺度（640p+1328p 联合，WordNet 式层级分类 + 文字长尾重采样）。
- **标注（re-captioning）**：用 Qwen2.5-VL 做单遍同时产出自然语言 caption + 结构化 JSON 元数据（图像类型/风格/水印/异常元素），verbatim 转写图中可见文字并加引号。
- **文字合成（针对中文长尾低频字）三策略**：Pure Rendering（纯净背景渲染段落，任一字渲染失败则整段丢弃）、Compositional Rendering（文字合成进真实场景/纸张木板再用 Qwen-VL 配 caption）、Complex Rendering（基于 PPT/UI 模板的程序化占位替换，造多行/结构化版式）。

## 训练方法
- **训练目标：Flow Matching（Rectified Flow）**。latent z=E(x)，噪声 x1~N(0,I)，timestep t 从 logit-normal 采样，xt=t·x0+(1-t)·x1，速度 vt=x0-x1，MSE 回归预测速度 vθ(xt,t,h)。
- **多任务训练范式（编辑落地的关键，§4.3）**：在 T2I 之外加入 **I2I 重建**与 **TI2I 编辑**，三者共享同一 latent 空间，从而对齐 Qwen2.5-VL 与 MMDiT 的表征。编辑任务用专门 system prompt（report Fig.15：先描述输入图关键特征，再解释指令应如何改图，在保持原图一致的前提下生成）。
- **预训练课程学习（progressive / curriculum）**：低→高分辨率（256→640→1328p）、无文字→有文字、海量→精refined、不均衡→均衡、真实→补合成。
- **后训练两阶段**：
  - **SFT**：层级语义类目 + 精细人工标注，专攻模型短板，要求清晰/细节丰富/明亮/写实。
  - **RL**：双策略——**DPO**（基于 flow-matching 的离线偏好，人工从多 seed 候选里选最好/最差，做大规模偏好学习，计算高效）+ **GRPO**（按 Flow-GRPO 框架，把 flow 采样重写成 SDE 引入随机性以探索，reward model 打分、组内归一优势，小规模精修）。GenEval 上 RL 把 0.87→0.91（唯一破 0.9 的基座）。
- **加速/蒸馏（生态，非官方主仓核心但官方 README 列为一等支持）**：社区 **Qwen-Image-Lightning**（LightX2V/ModelTC，diffusion distillation）对 Edit-2511 实现 **DiT NFE 降 25×、整体 42.55× 提速**，号称可实时编辑；推理默认步数 Edit=50、Edit-2509=40。

关键超参/trick：true_cfg_scale=4.0、negative_prompt 用空格、Edit-2509 加 guidance_scale=1.0；官方强烈建议对编辑指令做 **prompt rewriting**（`polish_edit_prompt`，由 Qwen-VL-Max 驱动）以稳住编辑结果。

## Infra（训练 / 推理工程）
基座训练工程（编辑沿用，technical report §4.1）：
- **Producer–Consumer 框架（Ray 思想）**：Producer 端做过滤 + VAE/MLLM 编码 + 按分辨率分桶缓存到位置感知共享存储，经自定义 HTTP transport（原生 RPC 语义）做异步零拷贝调度；Consumer 端在 GPU 密集集群专注训练，各 data-parallel 组异步拉预处理 batch。支持训练中热更新数据管线。
- **分布式**：Megatron-LM 训练；**混合并行 = 数据并行 + 4-way 张量并行**（MMDiT 用 Transformer-Engine 构建，可自动切换 TP 度数）；多头自注意力用 **head-wise 并行**降同步/通信开销。
- **显存权衡（实测，256 多分辨率设定）**：开 activation checkpointing 每卡显存 71GB→63GB（降 11.3%），但每 iter 时间 2s→7.5s（**慢 3.75×**）；因此**关闭 activation checkpointing、只用 distributed optimizer**。all-gather 走 bf16、gradient reduce-scatter 走 fp32（兼顾效率与数值稳定）。
- **总算力/GPU 卡数/GPU·时：未披露**（报告只给并行策略与单卡显存数字，无集群规模与训练 token/步数总量）。

推理/部署：
- 官方提供 **Multi-GPU API Server**（Gradio + 多 GPU 并行 + 队列 + 自动 prompt 优化，`NUM_GPUS_TO_USE` 默认 4）。
- 生态优化（官方 README 列出）：**DiffSynth-Studio** 逐层 offload 可 4GB 显存推理 + FP8 量化 + LoRA/全参训练；**DiffSynth-Engine** FBCache 加速 + CFG 并行；**vLLM-Omni / SGLang-Diffusion** day-0 高性能推理（长序列并行、缓存加速、fast kernel）；LeMiCa 缓存近 3× 无损加速。

## 评测 benchmark（把效果讲清楚）
编辑专项基准（technical report §5.2.3，全部由 **GPT-4.1** 评分；编辑模型即「Qwen-Image 的多任务编辑版」）：

**GEdit-Bench（11 类真实用户指令；SC=语义一致性, PQ=感知质量, O=总分=SC×PQ 几何均值，0–10）**
| 模型 | EN SC | EN PQ | EN O | CN SC | CN PQ | CN O |
|---|---|---|---|---|---|---|
| Instruct-Pix2Pix | 3.58 | 5.49 | 3.68 | — | — | — |
| MagicBrush | 4.68 | 5.66 | 4.52 | — | — | — |
| OmniGen2 | 7.16 | 6.77 | 6.41 | — | — | — |
| BAGEL | 7.36 | 6.83 | 6.52 | — | — | — |
| FLUX.1 Kontext [Pro] | 7.02 | 7.60 | 6.56 | 5.43 | 6.78 | 5.36 |
| Step1X-Edit | 7.66 | 7.35 | 6.97 | 7.34 | 6.85 | 6.50 |
| GPT Image 1 [High] | 7.85 | 7.62 | 7.53 | 7.67 | 7.56 | 7.30 |
| **Qwen-Image** | **8.00** | **7.86** | **7.56** | **7.82** | **7.79** | **7.52** |

→ EN/CN 双榜第一；CN 上对 FLUX.1 Kontext [Pro]（中文弱，CN O 仅 5.36）大幅领先。

**ImgEdit（9 类编辑任务、734 真实测例，1–5 分，指令遵循/质量/细节保留）**
| 模型 | Overall | 代表项 |
|---|---|---|
| OmniGen2 | 3.44 | — |
| FLUX.1 Kontext [Pro] | 4.00 | Replace 4.56 / Hybrid 3.68 |
| GPT Image 1 [High] | 4.20 | Add 4.61 / Style 4.93 |
| **Qwen-Image** | **4.27** | Replace 4.66 / Style 4.81 / Action 4.69 / Add 4.38 |

→ 总分第一，略高于 GPT Image 1 [High]。

**统一在 TI2I 框架下的 3D/感知任务（佐证编辑泛化）**：
- 新视角合成 GSO：PSNR **15.11** / SSIM **0.884** / LPIPS **0.153**，优于 FLUX.1 Kontext [Pro]（14.50/0.859/0.201）、BAGEL、GPT Image 1，并超 Zero123/CRM 等专用 3D 模型。
- 深度估计（仅 SFT，DepthPro 当 teacher）：在 NYUv2/KITTI/ScanNet/DIODE/ETH3D 上与判别式专用模型可比（如 NYUv2 AbsRel 0.055 / δ1 0.967）。

**文字渲染（编辑文字能力的根基，T2I 榜）**：中文 ChineseWord 总分 **58.30**（GPT Image 1 36.14、Seedream 3.0 33.05）；Level-1 字准确率 **97.29%**。LongText-Bench ZH **0.946** / EN 0.943。GenEval 0.91（RL）、DPG 88.32、OneIG-ZH 0.548 / EN 0.539。

**人评（AI Arena Elo，仅 T2I）**：Qwen-Image 作为唯一开源模型排第 3，落后 Imagen 4 Ultra 约 30 Elo，但领先 GPT Image 1 [High] 与 FLUX.1 Kontext [Pro] 30+ Elo（注：编辑维度的 Arena 当时尚未上线）。

**关键消融/结论**：① 双编码缺一不可——只给 MLLM 语义 embedding 指令遵循好但保真不足，叠加 VAE pixel embedding 才同时拿到结构/视觉一致性；② VAE 只微调 decoder（冻 encoder）即可显著提升小字重建，是文字编辑的底座；③ activation checkpointing 因 3.75× 时间代价被弃用。

**2509 版定量数字：HF 卡未给基准表**（仅定性 showcase + 能力清单：多图/一致性/ControlNet），相对 Edit 的提升幅度官方**未报告**具体分数。

## 创新点与影响
**核心贡献**
1. **双编码（dual-encoding）条件注入**：Qwen2.5-VL（语义）+ VAE Encoder（外观）双路并行，单模型同时拿下「语义编辑」与「外观编辑」，是该工作最核心的方法创新。
2. **编辑统一进多任务训练**（T2I+I2I+TI2I 共享 latent + MSRoPE 加 frame 维），而非外挂编辑头，复用 20B 基座能力。
3. **把强中文文字渲染延伸到「编辑图中文字」**：可改内容并保留字体/字号/风格，中文海报小字也能精修；链式编辑可逐步纠正生成错字（如《兰亭集序》书法纠错）。
4. **2509 增量**：图像拼接训练实现多图（人+人/人+物/人+景）编辑、原生 ControlNet、人物/商品/文字一致性增强。

**影响**
- 成为开源指令编辑的强基座，催生大量社区 LoRA（2511 已把热门 LoRA 直接内置）；被 vLLM-Omni / SGLang-Diffusion / DiffSynth / LightX2V 等推理栈 day-0 支持，Lightning 蒸馏把编辑推到近实时（NFE 25× / 42.55× 提速）。
- 月度迭代节奏（Edit→2509→2511）+ Apache-2.0，推动 TI2I 在中文生态落地。
- 论证「生成式框架可统一做理解类任务」（深度估计/新视角即编辑的特例），呼应 Qwen-Image 作为 Qwen 系列「生成支柱」补全理解-生成一体化的定位。

**已知局限**
- Edit-2509 多图最佳仅 1~3 张；编辑结果不稳定，官方强依赖 prompt rewriting。
- 编辑专项数据集规模、训练算力/GPU·时**官方未披露**；2509 相对 Edit 的定量增益**未报告**。
- 20B 基座推理重，原始未蒸馏版步数 40~50，落地需靠量化/蒸馏/offload。

## 原始链接
- arxiv (tech report, 基座+编辑方法/实验): https://arxiv.org/abs/2508.02324
- pdf: https://arxiv.org/pdf/2508.02324
- hf (Edit): https://huggingface.co/Qwen/Qwen-Image-Edit
- hf (Edit-2509): https://huggingface.co/Qwen/Qwen-Image-Edit-2509
- modelscope (Edit): https://modelscope.cn/models/Qwen/Qwen-Image-Edit
- github: https://github.com/QwenLM/Qwen-Image
- blog (Edit, 2025-08-19): https://qwenlm.github.io/blog/qwen-image-edit/ （现重定向至 qwen.ai，正文与 HF 卡一致）
- demo: https://huggingface.co/spaces/Qwen/Qwen-Image-Edit

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2508.02324.pdf （Qwen-Image 技术报告全文 46 页，已精读；PDF 不入 git）
- ../../../sources/omni/2025/qwen-image-edit--hf-card.md
- ../../../sources/omni/2025/qwen-image-edit-2509--hf-card.md
- ../../../sources/omni/2025/qwen-image-edit--blog.md
- ../../../sources/omni/2025/qwen-image--github-readme.md
