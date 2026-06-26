---
title: "Skywork UniPic 3.0: Unified Multi-Image Composition via Sequence Modeling"
org: "Kunlun Skywork (Skywork Multimodality Team)"
country: China
date: "2026-01"
type: tech-report
category: unified
tags: [unified, image-editing, multi-image-composition, hoi, sequence-modeling, mmdit, qwen-image, flow-matching, distillation, dmd, consistency-model, few-step]
url: "https://arxiv.org/abs/2601.15664"
arxiv: "https://arxiv.org/abs/2601.15664"
pdf_url: "https://arxiv.org/pdf/2601.15664"
github_url: "https://github.com/SkyworkAI/UniPic/tree/main/UniPic-3"
hf_url: "https://huggingface.co/Skywork/Unipic3"
modelscope_url: ""
project_url: "https://skywork-unipic-v3.github.io"
downloaded: [arxiv-2601.15664.pdf, skywork-unipic-3-0--hf-readme.md, skywork-unipic-3-0--github-readme.md, skywork-unipic-3-0--github-unipic3-readme.md, skywork-unipic-3-0--project-page.html]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Skywork UniPic 3.0 把"单图编辑"与"多图合成"统一为一个**序列建模**问题：将目标图的噪声 latent 与全部参考图（1~6 张）的 latent 沿序列维拼成一条长序列，用同一套 [[mmdit]] 架构与 flow-matching 目标完成条件生成；仅用 700K 量级精选数据训练，并把**轨迹映射(consistency)+分布匹配(DMD)**蒸馏进后训练，做到 **8 步推理、相对 50 步 12.5× 加速**。结果在单图编辑 ImgEdit-Bench 拿到 4.35（SOTA），并在自建多图合成 MultiCom-Bench 上以 **0.7255** 总分**超过闭源的 Nano-Banana(0.7224) 与 Seedream 4.0(0.7088)**。

## 背景与定位
2025–2026 年多图合成（multi-image composition）因 Nano-Banana、[[seedream-4-0]] 等闭源系统走红，社区需求从"单图编辑"转向"把多张参考图里的元素融成一张连贯高质图"。相比单图编辑（结构基本守恒），多图合成要调和不同来源图之间**冲突的语义、光照、视角、风格**，远更难；而闭源系统**不披露方法细节**，已有开源工作（如 Qwen-Image-Edit-2509）又受限于**固定分辨率/输入张数有限**（其官方建议最优为 2~3 张输入）。

UniPic 3.0 的统计分析发现：社区最关心的子任务是 **HOI（Human-Object Interaction，人-物交互）**——需要精确的空间关系、真实遮挡、自然交互。因此本作把 HOI 多图合成作为主攻方向，提出三点贡献：(1) 面向多图合成的数据策展流水线（215K 高质 HOI 样本，强调"质 > 量"）；(2) 统一**序列建模**范式（单图编辑与多图合成同架构同目标）；(3) 首次把**轨迹映射 + 分布匹配**联合蒸馏用到大规模多图合成，8 步出图。

技术脉络上，它是 Skywork UniPic 系列的第三代，但**换了路线**：
- **UniPic 1.0**（arXiv 2508.03320，2025-07）：1.5B 参数，**自回归统一建模**，单 transformer 同时做理解与生成。
- **UniPic 2.0**（arXiv 2509.04548，2025-08）：基于 SD3.5M-Kontext / MetaQuery 的高效架构 + 扩散后训练 + 在线 RL。
- **UniPic 3.0**（本作，2026-01）：直接**站在 [[qwen-image]] / Qwen-Image-Edit 之上**（MMDiT backbone + Qwen2.5-VL 条件编码器 + VAE），聚焦多图合成与少步推理，路线从"自回归/Kontext"切到"flow-matching MMDiT + 序列拼接"。

相关基础工作内链：[[ddpm]] [[latent-diffusion-ldm]] [[flow-matching]] [[rectified-flow]] [[consistency-models]] [[dmd]] [[qwen-image]] [[seedream-4-0]]。

## 模型架构
**整体沿用 Qwen-Image 的三件套**（论文 4.2 节明确"Our model architecture follows that of Qwen-Image"）：
- **条件编码器**：Qwen2.5-VL（多模态 LLM）作为 condition encoder，编码文本指令（多图合成里指令还要描述空间排布/遮挡/光照）。
- **图像 tokenizer**：VAE 编码器，把每张图编成 latent 张量 `z ∈ R^{1×C×H'×W'}`（C 为 latent 通道，(H',W') 为下采样空间分辨率）。
- **主干**：MMDiT（multimodal diffusion transformer）扩散模型。

**核心创新——统一视觉序列（Unified Visual Sequence）：**
1. **Latent 编码**：目标图 O 与 K 张参考图 {I₁…I_K} 各自过 VAE 编码成 latent。
2. **Patch-wise packing**：沿用 Qwen-Image 的 `pack(·)`，把 latent 的 2×2 空间邻域重排成 token，得到序列 `s ∈ R^{N×D}`（该操作给定空间元数据可逆）。
3. **序列拼接**：把目标与全部参考的 packed latent **沿序列维直接 concat** 成一条长序列
   `S = [s_O ‖ s₁ ‖ … ‖ s_K] ∈ R^{N_tot×D}`，其中 `N_tot = N_O + Σ N_k`。
4. **形状描述子**：维护 `H = {h_O, h₁,…,h_K}`，每个 h 编码对应图的 latent 高/宽，喂进 transformer 以保留空间结构、支持精确 unpack 重建。
5. **推理时**：把真实目标 latent 替换为纯高斯噪声、保留全部参考 latent，对长序列做 flow-matching 采样还原目标图。

这套设计的好处：(a) **天然支持可变输入张数**（1~6）与**任意输出分辨率**——只要总像素预算 ≤ 1024×1024；(b) **单图编辑 = K 较小（含 1）的特例**，与多图合成共用一套架构与训练目标，便于跨任务知识迁移；(c) 不需要任务专用模块。

**参数量**：论文、model card、GitHub README **均未给出参数量数字**，仅说架构"follows that of Qwen-Image"（基座 Qwen-Image / Qwen-Image-Edit 的 MMDiT）——记为"未披露具体参数量"（已落盘源中无任何参数量数字，故不臆测）。
**分辨率策略**：任意 1~6 输入、任意输入分辨率、任意输出分辨率，约束在 1024×1024 总像素预算内。

## 数据
论文 4.1 节给出**三阶段数据策展流水线**（Collection → Filtering → Synthesis），最终产出 **215K 高质量三元组**（源图集合, 指令, 目标图），主打 HOI。

**1) 数据采集（Collection）——人/物分治：**
- **人物子集**：从 **CC12M** 取真实人本图（姿态/外观/真实场景丰富），用 **InternVL3.5-38B** 生成密集、结构感知的 caption（显式描述人的属性、衣着、姿态、场景上下文）。
- **物体子集**：先用 **GPT-4o** 生成 **300 个**适合与人交互的细粒度物体类别（服饰、手持工具、乐器、家具、运动器材等）；每类再让 GPT-4o 产 **5,000** 条强调外观/材质/典型用法的文本 prompt；这些 prompt 喂 **Qwen-Image** 合成 **150K 物体图**。人/物分治保证交互类型覆盖均衡且都是高真实感。

**2) 数据过滤（Filtering）——多级严筛：**
- 用 InternVL3.5-38B 给每张图打 0~100 整体质量分（分辨率/清晰度/美学/语义清晰度），**< 75 直接删**。
- 人物图：用专门的人脸/人体检测器，剔除**头部截断（人脸可见 < 90%）、主体被遮挡（前景占比 < 60%）、背景杂乱（背景复杂度分 > 0.7）**。
- 物体图：强制最小分辨率（> 768² 像素），用 **CLIPScore** 交叉校验 prompt-图对齐，剔低相似度对。
- 严筛后仅保留 **18K 人物图 + 120K 物体图**，构成"可合成就绪"库存。

**3) 数据合成（Synthesis）——构造源组合 + 生成目标：**
- 每个合成采 **2~6 张**源图，并施加硬性 **HOI 兼容约束**：用人工策展的"冲突矩阵"排除物理不合理（如一个人不能同时穿两双鞋、同一只手玩两件乐器）。
- 对每个合法组合，用 InternVL3.5-38B 生成连贯的合成 prompt（描述自然空间排布、真实遮挡关系、和谐光照），弥合不同源图的语义鸿沟。
- **混合合成策略（关键经验）**：作者实测 **Nano-Banana 在 >3 输入时人脸身份保持退化**，而 **Seedream 4.0 在 4~6 图时一致性更好**。故 **Nano-Banana 生成 75K（2~3 图子集）**、**Seedream 4.0 生成 140K（4~6 图子集）**。
- 每张合成目标过自动质检（美学分 + 人脸身份保持），失败的重合成或丢弃。

**训练总数据（5.1 节）**：
- 多图合成 **338K** = 内部构造 215K + **Mico-150K**[46]。
- 单图编辑 **381K**（开源）= **Nano-consistent-150K**[53] + **Pico-Banana-400K**[26] 的子集。

## 训练方法
**生成目标：flow matching**（论文 3 节，αₜ = 1−t、σₜ = t，t∈[0,1]，xₜ = αₜx + σₜε），目标
`L_FM = E‖F_θ(xₜ,t) − (ε − x)‖²`。

**整体三阶段流水线**（Base → Consistency Model → DMD）：

**阶段 1 · 基座全参微调（Base / Teacher）**
- 对 MMDiT 做**全参数**微调，**80K 步**，全局 batch size **64**，学习率 **1×10⁻⁴**。
- 优化器 AdamW（β₁=0.9, β₂=0.95, ε=1e-8, weight decay 0.05），cosine 退火。
- 产物即 HF 上的 `Skywork/Unipic3`（Teacher，多步 50 步采样，重质量不重速度）。

**阶段 2 · 连续时间一致性训练（Consistency Tuning for Flow Matching）**
- 在 flow-matching 模型上做**连续时间 CM**。作者指出 SANA-Sprint 那种把 FM 转 TrigFlow（三角调度）的做法会引入**额外梯度项、数值不稳**；本作改用更"原则化"的 consistency flow matching 参数化：`f_θ(xₜ,t) = xₜ − t·F_θ(xₜ,t)`，从而 `∇_θ f_θ = −t∇_θ F_θ`，并推出切向量 `df_θ⁻/dt` 的显式形式（论文式 9）。
- 一致性损失（式 11）：`L_CM = ‖F_θ(xₜ,t) − ε − x − t·(dF_θ⁻/dt)‖²`，其中 `dF_θ⁻/dt` 用**有限差分**近似 `(1/2ε)(F_θ⁻(x_{t+ε}) − F_θ⁻(x_{t−ε}))`，默认 **ε = 5×10⁻³**。
- 超参（5.1 节）：**10K 步**，全局 batch **256**，学习率 **1×10⁻⁶**。（GitHub 代码默认值另给 train_steps=20000、ema_rate=0.95、guidance_scale=1.75、accum_steps=4、可选 tangent_norm——以论文 5.1 报告值为准，代码默认值仅作参考。）
- 产物：`Skywork/Unipic3-Consistency-Model`（8 步）。

**阶段 3 · 分布匹配蒸馏（DMD）**
- 在 CM 之上再做 **reverse-KL 分布匹配蒸馏**，进一步提升保真度。
- 用一个 **fake score network** F_φ（从 teacher 初始化 + 加 **LoRA**，只训 LoRA）近似学生分布；学生与 fake-score 交替更新。
- 梯度项（式 13）：`g = ((1−t)/t)·(F_teacher^CFG(xₜ,t) − F_φ(xₜ,t))`，其中 teacher 用 **CFG**；DMD 损失（式 14）：`L_DMD = ½‖G_θ − G_θ⁻ + g‖²`。
- 超参（5.1 节）：**10K 步**，全局 batch **64**；学生 lr **2×10⁻⁶**、fake-score lr **4×10⁻⁷**；**teacher CFG 尺度 w = 6.0**。
- 产物：`Skywork/Unipic3-DMD`（8 步，部署友好）。

**蒸馏总结（论文式总结段）**：先用一致性损失（式 11）得到少步生成器，再做 DMD（式 14）提升保真——这是 Hyper-SD 式"轨迹映射 + 分布匹配"混合框架，但作者声称给了"更原则化的公式与更高效的实现"。最终 **8 步出图，相对标准 50 步采样 12.5× 加速**，质量不降。

## Infra（训练 / 推理工程）
- **训练框架**：FSDP（GitHub 给出 `qwen_image_edit/train_fsdp_bsz1.py`，单卡 batch=1 + 梯度累积/分片）；分布式依赖环境变量 `MLP_WORKER_NUM / MLP_ROLE_INDEX / MLP_WORKER_0_HOST / MLP_WORKER_0_PORT`（字节系 MLP 训练平台约定）。
- **显存优化**：gradient checkpointing（CM/DMD 脚本均可开），EMA（CM 代码默认 ema_rate=0.95），DMD 阶段 fake-score 只训 LoRA（省显存/省算力）。
- **算力规模 / GPU·时 / 并行拓扑 / 吞吐**：论文与 README **均未披露**具体 GPU 数、卡时、精度（bf16/fp16）与吞吐——记为"未披露"。
- **推理形态**：Teacher 50 步（true_cfg_scale 4.0）；CM / DMD 8 步（`Skywork/Unipic3-Consistency-Model/ema_transformer`、`Skywork/Unipic3-DMD/ema_transformer`），支持 `torch.distributed` 批量推理；**12.5× 端到端加速**来自 50→8 步 + 蒸馏。
- **开放程度**：代码、三档权重（Base/CM/DMD）、数据集均开源（MIT License）。

## 评测 benchmark（把效果讲清楚）
数字全部来自论文 Table 1 / Table 2（已抓取一手 PDF）。

**单图编辑 — ImgEdit-Bench / GEdit-Bench（Table 1，分越高越好）**

| Model | ImgEdit Overall ↑ | GEdit G_SC | G_PQ | G_O |
|---|---|---|---|---|
| Qwen-Image-Edit | 4.25 | 8.18 | 7.87 | 7.68 |
| Qwen-Image-Edit-2509 | 4.31 | 8.12 | 8.01 | 7.61 |
| Nano-Banana | 4.22 | 7.43 | 8.14 | 7.20 |
| Seedream 4.0 | 4.11 | 8.24 | 7.86 | 7.66 |
| UniPic 2.0 | 4.06 | 7.63 | 7.17 | 7.10 |
| **UniPic 3.0** | **4.35** | 8.12 | 7.79 | **7.55** |

- UniPic 3.0 **ImgEdit-Bench Overall 4.35**（最高），分项里 Style 4.97、Action 4.69 等领先；GEdit-Bench Overall 7.55。说明统一多图能力**没有牺牲**单图编辑性能。

**多图合成 — MultiCom-Bench（Table 2，作者自建，0~1，越高越好）**

| Model | 2–3 图 | 4–6 图 | Overall |
|---|---|---|---|
| Qwen-Image-Edit | 0.7705 | 0.4793 | 0.6249 |
| Qwen-Image-Edit-2509 | 0.8152 | 0.2474 | 0.5313 |
| Nano-Banana | 0.7982 | 0.6466 | 0.7224 |
| Seedream 4.0 | 0.7997 | 0.6197 | 0.7088 |
| **UniPic 3.0** | **0.8214** | **0.6296** | **0.7255** |

- **总分 0.7255 全场最高**，超过闭源 Nano-Banana(0.7224)、Seedream 4.0(0.7088)。
- **2~3 图子集 0.8214** 显著领先（Seedream 0.7997 / Nano-Banana 0.7982），说明少输入精度更高。
- 4~6 图子集 0.6296：**该列第一是 Nano-Banana(0.6466)**，UniPic 居第二（高于 Seedream 0.6197）；UniPic 靠 2~3 子集领先与更高总分取胜，4~6 子集并非最优。
- **关键对照结论**：Qwen-Image-Edit 本不支持多图合成，但用本作的推理范式可"涌现"出 2~3 图能力（4~6 图崩塌至 0.4793）；Qwen-Image-Edit-2509 在 2~3 图次于 UniPic（0.8152），但 4~6 图暴跌到 **0.2474**——印证现有开源在多输入下的脆弱，而 UniPic 3.0 的序列建模保持了 4~6 图的稳定。

**MultiCom-Bench 构造**：200 个高质 HOI 三元组（100 个 2~3 源图 + 100 个 4~6 源图），按 VIEScore 范式设计稳定评测模板，评三维——**指令遵循、图像质量、人脸一致性**；该 benchmark 将开源。

**消融 / 定性**：论文以定性图（Fig.4 与 Nano-Banana/Seedream/Qwen-Image-Edit 对比；Fig.5 展示 8 步蒸馏结果）佐证少步保真，**未提供逐项消融数表**（数据规模/各阶段贡献的定量 ablation 未报告）。

## 创新点与影响
**核心贡献**
1. **统一序列建模范式**：把单图编辑与多图合成都化为"目标噪声 latent + 参考 latent 沿序列维拼接"的条件生成，单架构单目标支持 1~6 任意输入与任意输出分辨率（1024² 像素预算内），这是相对 Qwen-Image-Edit-2509（固定/有限输入）的关键灵活性突破。
2. **质 > 量的 HOI 数据流水线**：仅 215K 精选 HOI 样本（人/物分治采集 + 多级严筛 + 冲突矩阵约束合成 + Nano-Banana/Seedream 混合蒸馏式合成）即达 SOTA，给出可复现的多图合成数据方法论。
3. **首次把"轨迹映射(consistency FM)+分布匹配(DMD)"联合蒸馏用于大规模多图合成**，并给出比 SANA-Sprint TrigFlow 更稳的一致性 FM 参数化，**8 步、12.5× 加速**且质量不降。
4. **开源全栈**：Base/CM/DMD 三档权重 + 训练/推理代码 + 数据 + MultiCom-Bench（MIT），首个系统性公开多图合成方法的工作，直接对标并在 benchmark 上超越闭源 Nano-Banana / Seedream 4.0。

**影响**：为开源社区提供了一个**可复现的多图合成强基线**与评测协议（MultiCom-Bench）；其"长序列拼接 + flow-matching MMDiT + 混合蒸馏"是后续统一编辑/合成模型的可借鉴模板；HOI 冲突矩阵 + VLM 合成 prompt 的数据范式对多主体一致性生成有迁移价值。

**已知局限**
- **未披露参数量、算力/卡时、训练精度与吞吐**，工程可复现性有缺口。
- MultiCom-Bench 为**自建**，且部分训练目标数据由 Nano-Banana/Seedream 合成（蒸馏自闭源教师），"超越闭源"的结论需注意评测构造与数据来源的耦合。
- 4~6 图子集仍略逊于 Nano-Banana（0.6296 vs 0.6466），多输入高复杂度仍有提升空间。
- 总像素预算 1024² 限制了大尺寸/高分辨率输出。
- 缺少定量消融，各组件（数据规模、CM、DMD）的边际贡献未量化。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2601.15664
- arxiv_pdf: https://arxiv.org/pdf/2601.15664
- project_page: https://skywork-unipic-v3.github.io
- github (UniPic-3): https://github.com/SkyworkAI/UniPic/tree/main/UniPic-3
- github (repo root): https://github.com/SkyworkAI/UniPic
- hf (Teacher/Base): https://huggingface.co/Skywork/Unipic3
- hf (Consistency Model): https://huggingface.co/Skywork/Unipic3-Consistency-Model
- hf (DMD): https://huggingface.co/Skywork/Unipic3-DMD
- hf (collection + dataset): https://huggingface.co/collections/Skywork/skywork-unipic3
- 前作: UniPic 1.0 arXiv 2508.03320 ; UniPic 2.0 arXiv 2509.04548

## 一手源存档（sources/）
- [arxiv-2601.15664.pdf](https://arxiv.org/pdf/2601.15664)  （arXiv 原文 PDF，不入 git）
- [hf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/skywork-unipic-3-0--hf-readme.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/skywork-unipic-3-0--github-readme.md)
- [github-unipic3-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/skywork-unipic-3-0--github-unipic3-readme.md)
- [project-page.html](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/skywork-unipic-3-0--project-page.html)
