---
title: "Seedream 4.0: Toward Next-generation Multimodal Image Generation"
org: "字节跳动 Seed"
country: China
date: "2025-09"
type: tech-report
category: unified
tags: [t2i, image-editing, multimodal, dit, high-compression-vae, joint-post-training, rlhf, adversarial-distillation, quantization, speculative-decoding, 4k, multi-image-reference, in-context-reasoning, closed-source]
url: "https://seed.bytedance.com/seedream4_0"
arxiv: "https://arxiv.org/abs/2509.20427"
pdf_url: "https://arxiv.org/pdf/2509.20427"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/seedream4_0"
downloaded: [arxiv-2509.20427.pdf, arxiv-2509.20427.txt, seedream-4-0--project-page.md, seedream-4-0--volcengine-docs.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Seedream 4.0 是字节 Seed 的「统一多模态图像生成系统」，把文生图（T2I）、单图编辑、多图组合/参考统一进一个 DiT 框架；靠「高效 DiT + 高压缩 VAE + 对抗蒸馏加速」相比 [[seedream-3-0]] 实现 >10× 训练/推理算力加速，原生支持 1K–4K 出图，**生成一张 2K 图最快 1.4 秒**（不含 LLM/VLM 做 PE），并在 Artificial Analysis Arena 的文生图与图像编辑两个榜单上同时排名第一（截至 2025-09-18），与 Google [[gemini-2-5-flash-image-nano-banana]]（Nano Banana）同台竞争为 2025 闭源 t2i/编辑顶流。

## 背景与定位
2025 年随着 GPT-4o 原生出图、Gemini 2.5 Flash Image（Nano Banana）相继发布，图像模型的需求从「高保真 T2I」迅速扩展到「可控编辑 + 多模态推理 + 多图参考」。报告指出当前模型普遍存在**可扩展性瓶颈**：要同时把分辨率、可控性、多模态能力都往上推，算力开销会爆炸。

Seedream 4.0 的定位是用「架构效率」破局——通过 efficient DiT backbone + 高压缩比 VAE，在大幅提升模型容量的同时把训练/推理 FLOPs 显著降下来，让模型能在 **数十亿 text–image 对**、**原生 1K–4K 分辨率**上稳定训练。技术脉络上它是字节 Seed 图像线的集大成：
- **预训练**沿用 [[seedream-3-0]] 的「双轴协同数据采样」（视觉形态 × 语义分布）并针对知识类数据重构 pipeline；
- **后训练**沿用并扩展 [[seededit-3-0]] 的「引入 VLM 理解多模态输入」架构（causal diffusion），把 T2I 与编辑做**联合后训练**；
- **加速**：对抗蒸馏框架整合自家 Hyper-SD、RayFlow、APT、ADM，PE 的投机解码另基于 Hyper-Bagel。
基础扩散范式可追溯到 [[ddpm]] → [[latent-diffusion-ldm]] → DiT。报告同时披露了一个进一步 scale 的强化版 **Seedream 4.5**（更大模型+更多数据，全面超过 4.0），但 4.5 的细节本报告未展开。

## 模型架构
**Backbone：efficient & scalable Diffusion Transformer (DiT)。** 报告强调这是一个「精心设计的 DiT」，在提升模型容量的同时显著降低训练/推理 FLOPs，相对 Seedream 3.0 取得 >10× 算力加速（注：3.0 用的是 MMDiT + flow matching；4.0 报告未明示是否仍为 MMDiT 双流结构，**DiT 内部 token 设计/层数/参数量未披露**）。

**VAE：高压缩比变分自编码器（关键设计）。** 4.0 自研了一个高压缩比 VAE，**大幅减少 latent 空间的 image token 数量**——这是它能在 1K–4K 高分辨率上高效训练/推理、并支持秒级 4K 出图的核心。token 数减少直接降低注意力的平方级开销，使「高分辨率 + 大容量」可同时成立。具体压缩倍率、latent 通道数未披露。

**多模态条件注入 / PE 模型：端到端 VLM。** 后训练阶段把一个「对多模态输入有强理解力的 VLM」并入系统（沿用 SeedEdit 3.0 的设计思路），并基于 **Seed1.5-VL** 训练了一个端到端的 **Prompt Engineering (PE) 模型**。该 VLM 接收用户输入（文本 prompt + 单张/多张参考图），输出参考图与目标图的 caption（思路同 SeedEdit 3.0），再喂给 DiT。PE 模型的职责包括：**任务路由（task routing）、prompt 改写（带 auto-thinking）、最优宽高比估计**。受 AdaCoT 启发，PE 会**按任务复杂度动态调整 thinking 预算**，在延迟与性能间平衡。

**统一框架：causal diffusion 下的 T2I + 编辑联合。** 在 DiT 框架内用一种 causal diffusion 设计，把 T2I 生成与图像编辑「联合后训练」，使二者互相增益、单模型即支持单图/多图输入、单图/多图输出。原生集成了过去需要 ControlNet 等专用模型才能做的可控生成（Canny 边缘、草图、inpainting mask、depth），无需外挂控制网络。

**分辨率 / 宽高比策略。** 原生支持 1K–4K；引入**自适应宽高比机制**（也支持用户指定尺寸），可按语义需求或参考物形状自动调整画布，避免不合适的比例造成构图退化。

## 数据
**规模：数十亿（billions）text–image 对**，跨多样 taxonomy 与知识中心概念，覆盖数百个垂直场景。

**继承 + 修正 Seedream 3.0 的双轴采样。** 3.0 的纯 top-down 重采样有两个缺陷：(1) 整体分布过度偏向自然图像；(2) 细粒度、知识中心概念（教学内容、数学公式）被低估。为此 4.0 专门为知识类数据（instructional images、公式）重构 pipeline：
- **知识数据分自然/合成两类。** 自然图：从 PDF 文档（自有教科书、研究论文、小说）中采高质量图表 → 先用低质分类器过滤（模糊/杂乱/噪声背景）→ 再训一个**三级难度分类器**（easy/medium/hard）标注全部图，对极难样本在预训练中**下采样**。合成图：用 OCR 输出 + LaTeX 源码（可得时）生成结构（布局、符号密度）与分辨率各异的公式图，拓宽细粒度概念覆盖、缓解 top-down 重采样偏差。

**模块级升级（相对前代）：**
1. 训练**文本质量分类器**，检测原始 caption 里的低质文本；
2. 去重 pipeline 中**结合语义 + 低层视觉 embedding**，提升去重效果、平衡细粒度分布；
3. 精炼 **captioning 模型**做更细粒度视觉描述；
4. 采用更强的**跨模态 embedding** 做图文对齐，显著改进多模态检索引擎。

**编辑数据（CT/SFT 用）：** 构造大量编辑样本，每条典型为「参考图 + 目标图 + 编辑指令」，对参考图与目标图都产出 caption。设计**三种不同详细程度的 caption** 作为训练期数据增广，并鼓励在 caption 中使用一致术语来描述参考图与目标图的相似处（利于一致性学习）。美学/安全过滤的更多细节未披露。

## 训练方法
分两大阶段：高效预训练 + 多阶段联合后训练，外加专门的加速训练。

**预训练（多阶段，提升训练效率，同 Seedream 3.0 思路）：**
- **第一阶段**：在平均分辨率 **512²**（多种宽高比）训练 DiT；
- **第二阶段**：在 **1024²–4096²** 的高分辨率上微调。得益于高效架构（高压缩 VAE + efficient DiT），即便训到 4K 仍然有效。
- 训练目标（diffusion / flow matching 的具体形式）报告未明示，但加速一节围绕「轨迹 / divergence / NFE」展开，结合 3.0 的 flow matching 传统，应为 rectified-flow 类目标（**未明确写出**）。

**后训练（多阶段联合，核心创新）：** 在预训练 DiT 上做密集后训练，**联合训练 T2I + 单图编辑 + 多图参考/输出**，每个子阶段性能持续显著提升，优于单任务训练：
1. **CT（Continuing Training / 继续训练）**：拓宽模型基础知识与多任务能力，**主要增强图像编辑的指令遵循**；
2. **SFT（Supervised Fine-Tuning）**：注入特定艺术品质，**进一步显著提升参考图与编辑图之间的一致性**；
3. **RLHF（Reinforcement Learning from Human Feedback）**：精细对齐人类偏好（引用了 Flow-GRPO、DanceGRPO、ImageReward、RewardDance 等 reward/RL 方法）；
4. **PE 模型**：基于 Seed1.5-VL 端到端训练，解锁多样用户输入的全部潜力（见架构节）。

**加速训练（Model Acceleration，核心工程创新）：** 目标是在 DiT 上做超快推理而不掉质量，整体框架以**对抗学习**为中心，整合 Hyper-SD、RayFlow、APT、ADM 的思想：
- 核心范式：让**每个样本走一条优化过的自适应轨迹**，而非共享地走向同一个高斯先验，借此减少轨迹重叠与不稳定；
- 用**对抗匹配框架**替代固定的 divergence 度量，规避 mode collapse、提升稳定性与多样性；
- 两阶段：① **ADP（Adversarial Distillation Post-training）**——用 hybrid discriminator 做稳定初始化；② **ADM（Adversarial Distribution Matching）**——用可学习的、基于扩散的 discriminator 做精细分布匹配，做到 few-step 采样，把 NFE 大幅降低，同时在美学、文图对齐、结构保真等关键维度匹配或超过需要数十步的 baseline。

## Infra（训练 / 推理工程）
**训练系统**（面向 DiT 大规模预训练，强调硬件效率、可扩展、鲁棒）：
- **并行 / 显存优化**：用 **HSDP（Hybrid Sharded Data Parallelism）** 分片权重，**不依赖张量并行或专家并行**即支持大规模训练；显存通过及时释放 hidden states、激活 offload、增强的 FSDP 支持来优化；
- **Kernel / 负载优化**：`torch.compile` + 手写 CUDA kernel + 算子融合，减少冗余访存；针对变长序列的负载不均，引入**全局贪心样本分配策略 + 异步流水线**，平衡每卡利用率；
- **容错**：多级容错——定期对 model/optimizer/dataloader 状态做 checkpoint、预启动健康检查剔除故障节点、降低初始化开销，保障长周期分布式训练稳定与吞吐。
- **算力规模 / GPU 数 / GPU·时未披露。**

**推理加速**（系统性、无质量损失）：
- **对抗蒸馏 few-step 采样**（ADP→ADM，见训练节），把 NFE 大幅压低；
- **硬件感知量化 + 稀疏**：采用**自适应 4/8-bit 混合量化**——离线 smoothing 处理 outlier、search-based 优化为敏感层找最佳粒度与 scaling、PTQ 定参，并与各 bit 宽/粒度的硬件专用算子协同设计；
- **PE 的投机解码（speculative decoding）**：基于 Hyper-Bagel，针对随机 token 采样带来的不确定性，把特征预测条件化在「前序特征序列 + 提前一个 timestep 的 token 序列」上给出确定性目标，提升预测准确率；并加 KV-cache 上的损失以高效复用、加 logits 上的辅助交叉熵损失精炼 draft model。
- **结果：生成 2K 图最快 1.4 秒**（不含 LLM/VLM 做 PE），相对 Seedream 3.0 整体 >10× 加速。

**部署形态：** 闭源 API/产品，已集成进 **豆包（Doubao）/ 即梦（Jimeng/Dreamina）**（截至 2025-09），并在**火山引擎方舟（Volcano Engine Ark）**开放 API（Model ID `Doubao-Seedream-4.0`）。据火山方舟图片生成 API 文档：支持单图/多图输入（最多 **14 张参考图**）、组图输出（`sequential_image_generation=auto`，输入参考图数+生成图数 ≤ 15 张）、宽高比范围 [1/16, 16]、单输入图 ≤ 30MB / 总像素 ≤ 6000×6000、出图分辨率 2K/4K（4.0），按「成功生成图片张数」计费、output_tokens = ⌊Σ(图宽×图高)/256⌋。

## 评测 benchmark（把效果讲清楚）
**Artificial Analysis Arena（公开众测，ELO）：Seedream 4.0 在文生图与图像编辑两个赛道均排名第一**（数据截至北京时间 2025-09-18 17:00）。同台对手包括 GPT-Image-1、[[gemini-2-5-flash-image-nano-banana]]（Gemini-2.5 Flash Image）、开源的 Qwen-Image、FLUX-Kontext（[[flux-2]] 同门 BFL 的编辑模型），以及自家 Seedream 3.0 / SeedEdit 3.0。（具体 Elo 分值在报告 Figure 1/3 的图中，正文未给出数值。）

**人评 MagicBench 4.0（自建多模态基准）：** 三大任务——T2I（325 prompts）、单图编辑（300 prompts）、多图编辑（100 prompts），每条 prompt 中英双语。
- **T2I**：除常规的 prompt 对齐、结构稳定性、视觉美学外，额外评 **dense text rendering（密集文本渲染）** 与 **content understanding（内容理解，需 in-context 推理/专业知识）**。结论：相比前代在所有维度显著提升，**视觉美学（visual aesthetics）大幅领先**竞品。
- **单图编辑**：核心权衡是「指令遵循 vs 一致性」。结论：**GPT-Image-1 指令遵循最高但一致性最低**（业界共识的局限）；**Gemini-2.5 善于保持但指令遵循弱**（尤其风格迁移/视角变换、中文文本编辑差）；**Seedream 4.0 各维度更均衡**，支持广泛编辑任务且一致性强，实用性更高。
- **多图编辑**：用 GSB（Good/Same/Bad）整体指标 + 三个客观维度（指令对齐、一致性、结构）。结论：**Seedream 4.0 全维度最高，在 GSB 指标上比 GPT-Image-1 / Gemini-2.5 高出近 20%**；且随参考图增多其它模型结构退化，**Seedream 4.0 在 >10 张参考图时仍保持稳定连贯结构**。

**自动评测 DreamEval（自建）：** 4 个生成场景、128 个子任务、1,600 prompts；打分拆成细粒度 VQA（更可解释、确定）；含分层难度（基础生成 / 高级生成 / 高阶理解推理）。关键结论：
1. Seedream 4.0 与 GPT-4o 在指令遵循上领先其它模型；Seedream 4.0 方差更大——**平均分略低但 best-of-4 更好**，说明用户可通过多次采样拿到更优结果；
2. Seedream 4.0 在 Easy/Medium 表现好，**Hard 级（尤其单图编辑）有所下降**——指出多模态理解与推理仍是后续 scaling（4.5 及后续）的改进方向。

**能力展示（定性，非打分）：** 精准编辑（增删改替 + 背景替换 + 人像精修）、灵活参考（2D/3D 跨域、变视角、ID/IP 一致性、衍生设计）、视觉信号可控生成（Canny/草图/mask/depth 单模型原生）、in-context 推理生成（物理/时间约束、3D 想象、解谜/填字/漫画续写）、多图参考（>10 图、抽象风格如折纸/巴洛克迁移、机械件组装）、多图输出（角色一致的分镜/漫画/表情包/IP 周边）、高级文本渲染（UI/海报/公式/化学方程/统计图）、自适应宽高比与 4K 出图。

## 创新点与影响
**核心贡献：**
1. **高效可扩展架构**：efficient DiT + 高压缩比 VAE，把高分辨率所需 image token 数大幅压低，做到 >10× 训练/推理加速（按 FLOPs）且性能更强，为「模态容量 × 任务覆盖 × 多模态泛化」的 scaling 打开空间。
2. **统一多模态生成**：在 SeedEdit 3.0 架构上扩展，用 causal diffusion 把 T2I 与编辑**联合后训练**，单模型支持单/多图输入与输出，且二者互相增益。
3. **专业 & 知识中心生成**：能产出图表、公式、设计素材等结构化/知识型内容，弥合创意生成与产业实用之间的鸿沟（这是其相对纯艺术图模型的差异化卖点）。
4. **极致推理加速**：对抗蒸馏 + 硬件感知量化 + 投机解码组合，2K 出图最快 1.4 秒，把图像生成/编辑推向「秒级交互」体验。

**影响：** 作为字节 Seed 在 GPT-4o 出图 / Nano Banana 时代的旗舰回应，Seedream 4.0 把「统一生成+编辑+多图参考」做成了可在 Artificial Analysis Arena 双榜登顶的闭源 SOTA，并通过豆包/即梦/火山方舟大规模落地；其「高压缩 VAE + 对抗蒸馏」的效率路线，与 Qwen-Image、FLUX-Kontext 等开/闭源竞品共同推动 2025 年「统一图像模型」成为主流范式。报告还展示了清晰的 scaling 收益（→ Seedream 4.5），印证架构可扩展性。

**已知局限（报告自述）：** (1) DreamEval Hard 级、尤其单图编辑上性能下降，**多模态理解/推理仍是短板**，需靠扩大模型与相关数据改善；(2) Seedream 4.0 指令遵循方差较大（best-of-4 才稳定占优）；(3) 架构内部参数量、VAE 压缩倍率、训练算力、具体扩散目标等**多项工程细节作为闭源产品未披露**。

## 原始链接
- 技术报告 (arXiv): https://arxiv.org/abs/2509.20427 （v3, 2025-12-10；初版 2025-09-24）
- 技术报告 PDF: https://arxiv.org/pdf/2509.20427
- 官方项目页 (Seed): https://seed.bytedance.com/seedream4_0
- 火山方舟图片生成 API 文档: https://www.volcengine.com/docs/82379/1666946 （现重定向至 Seedream 5.0 lite/4.5/4.0 共用的图片生成 API 文档）
- 产品入口: 豆包 https://www.doubao.com/chat/create-image ; 即梦 https://jimeng.jianying.com/ai-tool/image/generate
- 公开榜单: Artificial Analysis Arena https://artificialanalysis.ai/text-to-image/arena

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2509.20427.pdf
- ../../../sources/omni/2025/arxiv-2509.20427.txt
- ../../../sources/omni/2025/seedream-4-0--project-page.md
- ../../../sources/omni/2025/seedream-4-0--volcengine-docs.md
