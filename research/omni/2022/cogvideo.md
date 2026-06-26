---
title: "CogVideo: Large-scale Pretraining for Text-to-Video Generation via Transformers"
org: "Tsinghua University / BAAI"
country: China
date: "2022-05"
type: paper
category: video
tags: [text-to-video, autoregressive, transformer, vqvae, cogview2, open-source]
url: "https://arxiv.org/abs/2205.15868"
arxiv: "https://arxiv.org/abs/2205.15868"
pdf_url: "https://arxiv.org/pdf/2205.15868"
github_url: "https://github.com/THUDM/CogVideo"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2205.15868.pdf, cogvideo--github-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CogVideo 是（据作者所称）**首个大规模开源预训练文生视频模型**：一个 94 亿参数的自回归 Transformer，通过**继承文生图模型 CogView2** 的权重 + 新增可训练的时序注意力通道（dual-channel attention）来避免从零训练，并提出**多帧率分层训练（multi-frame-rate hierarchical training）**对齐文本与动作语义。在 UCF-101 上 FVD 626 / IS 50.46，在 Kinetics-600 上 FVD 109.23；人评中 49.53% 评测者选其为最佳（VideoGPT 15.42%、TGANv2 5.6%）。它是后续 [[cogvideox]] 系列的源头。

## 背景与定位
2022 年文生视频仍处早期，自回归 Transformer（继 [[dall-e-1]]、[[cogview]] 之后）被尝试用于视频，代表作有 VideoGPT、GODIVA、NÜWA。但这类工作存在两个核心痛点，CogVideo 正是冲着它们去的：

1. **数据稀缺且弱相关**：最大的标注文本-视频集 VATEX 仅 4.1 万条；检索式（如 HowTo100M）文本只描述场景、不含时序信息。从零训练大模型既昂贵又难学到「动作」语义。
2. **固定帧数切片破坏对齐**：以往把视频按固定帧数切成多个 clip 共用同一文本训练。若把一段「喝水」视频切成「拿杯」「举起」「喝」「放下」四段都标注「drinking」，模型会被混淆，学不到动作的准确含义。作者由此提出假设：自回归 Transformer 善于学文-图关系却拙于学文-动作关系，**根因在数据与其使用方式**。

CogVideo 的两条主线对应这两个痛点：用**多帧率分层训练**修「对齐」，用**继承 CogView2 + dual-channel attention**修「数据/算力」。它建立在 [[cogview2]]（其 CogLM 双向掩码语言模型是关键依赖）之上，是文生图知识向文生视频迁移的首次系统性尝试，且不损害原图像生成能力。

## 模型架构
**Backbone**：自回归 Transformer（非 diffusion）。48 层，每个注意力通道 hidden size 3072，48 个注意力头，**总计 94 亿参数**；其中 60 亿参数固定为 CogView2 权重（含 FFN、空间通道注意力、首帧位置编码、全部图文词表 embedding）。Transformer 结构基本沿用 [[cogview]]：用 **Sandwich LayerNorm** 与 **PB-Relax** 稳定大模型训练。

**Visual tokenizer**：沿用 VQVAE 框架，用 **icetk** 对图文统一分词。每帧离散化为 **20×20=400 个图像 token**；空间分辨率训练时 160×160，可由 CogView2 的超分模块（cogview2-dsr）上采样到 **480×480**。

**Text encoder**：无独立文本编码器——文本与图像 token 在同一自回归序列中，前缀为 `{帧率 token}{文本}[B]{Frame1}...{FrameTs}`，`[B]`（Begin-of-image）分隔符继承自 CogView2。序列长度 2065 = 64 文本 token + 5 帧 × 400 图像 token + 1 分隔符。

**三大架构创新（方法核心）**：

1. **Dual-channel attention（双通道注意力）**：在 CogView2 每层注意力上**只新增一个时空注意力通道（attention-plus，时序通道）**，原通道（attention-base，空间通道）权重**全部冻结**。两通道按可学习混合系数 α 融合：
   - `x̃ = α·attention-base(LN(x_in)) + (1−α)·attention-plus(LN(x_in))`，`x_out = x_in + LN(x̃)`。
   - α 是逐维向量 ∈(0,1)，由 `α = sigmoid(a)` 重参数化；attention-plus 初始化为与 attention-base 相同，使模型初始行为完全等同 CogView2，避免训练初期大梯度破坏预训练权重（作者强调：直接 finetune CogView2 因时序注意力模式不同会快速毁掉预训练权重）。
   - 两通道**共享 FFN**：FFN 是重参数模块、含大量视觉知识，图像与视频相似，共享可把图像知识带给时序通道，同时减参、提速、省显存。

2. **Multi-frame-rate hierarchical 两阶段生成**（见「训练方法」详述对齐动机）：
   - **Stage 1 顺序生成**：按低帧率 + 文本顺序生成 Ts=5 个关键帧。
   - **Stage 2 递归插帧**：把已生成帧作为**双向注意力区域**重新输入，在相邻帧间递归插入过渡帧；通过不断**对半降低帧率**实现越来越细的插值，生成多帧长视频。两模型共享结构与训练流程，仅注意力掩码不同（得益于 CogLM 的统一性）。

3. **基于 CogLM 的双向/单向注意力划分 + 3D Swin 自回归注意力**：
   - 借 [[cogview2]] 的 **CogLM**（Cross-Modal General Language Model）把 token 分为单向区与双向区：双向区可注意所有双向区，单向区可注意所有双向区 + 自身之前的单向区。Stage 2 插帧依赖双向上下文（已知帧对所有帧可见），弥补 GPT 式纯单向的缺陷。
   - 将 **Swin Attention** 从非自回归扩展到自回归时序场景：在 shifted window 内施加自回归掩码（插帧模型窗口 10×10）。一个意外收益是**远距离不同帧的 token 可并行生成**——满足 `(x1−x2)Y+(y1−y2) ≥ (t2−t1+1)(Ax·Y+Ay)` 时后帧 token 无需等前帧全部生成完，最多可并行生成 `⌊X·Y/(Ax·Y+Ay)⌋` 个 token，显著加速推理。

## 数据
- **规模/配比**：在 **540 万条带字幕视频（5.4M captioned videos）**上预训练，空间分辨率 160×160。论文未披露数据来源域、采集渠道、清洗/过滤流程、美学或安全过滤细节，也未说明 caption 来源（人工/检索/合成），这些维度**均未披露**。
- **关键设计——帧率自适应采样以保对齐**：预定义一组帧率，对每个文本-视频对**选能采到至少 5 帧的最低帧率**，使一个训练样本尽量包含完整动作（修复固定切片破坏对齐的问题）。Stage 1 调整每样本帧率以容纳整段视频（最低 1 fps）；Stage 2 把视频切成不同长度 clip 以适配 2/4/8 fps 的多帧率预测。
- **不引入额外图像数据**：作者明确**不像 Video Diffusion Model / NÜWA 那样混入文本-图像对**（那会显著增加大规模预训练成本），而是改为**继承预训练图像模型的权重**来获得空间语义——这是其数据效率的关键取舍。
- 评测微调用到的标注数据集：UCF-101（13320 视频 / 101 动作类）、Kinetics-600（约 35 万训练 + 5 万测试视频 / 600 类）、VATEX（背景对比）。

## 训练方法
- **训练目标**：自回归 next-token 预测（VQVAE 离散 token 序列上的语言建模），**非 diffusion / 非 flow matching**。Stage 2 插帧模型用 CogLM 的双向掩码 + 自回归混合目标。
- **多帧率分层训练（核心方法，修对齐）**：训练样本固定 5 帧 token，但**给文本前缀加一个帧率 token**并按该帧率采样组成定长序列。动机两点：(1) 固定帧率直接切片常导致语义错配（文本完整但 clip 动作不完整）；(2) 相邻帧高度相似，巨变会带来大 loss，使模型倾向「复制上一帧」走捷径、不去探索长程关联。帧率 token 同时在生成时**控制连续帧变化的强度**。低帧率生成可能不连贯，故再训一个插帧模型补过渡帧。
- **两模型分开预训练**（均 7.7B 参数，其中 6B 固定为 CogView2，故各自 1.7B 可训、合计 9.4B 不同参数）：
  - **Stage 1（顺序生成）**：先以最低帧率 0.25 fps 预训练 **76,000 步**，再以最低帧率 1 fps 训练 **15,000 步**。
  - **Stage 2（递归插帧）**：以 2/4/8 fps 预训练 **78,500 步**。
- **超参**：均 **FP16**，batch size **416**；Adam，max lr = **2×10⁻⁴**，β1=0.9，β2=0.95，weight decay = 1×10⁻²。
- **下游微调**：UCF-101 全集微调 10,000 步（batch 192，用类标签当文本）；Kinetics-600 训练集微调 12,000 步（batch 640）。
- **加速/蒸馏**：本文不涉及 diffusion 蒸馏（consistency/LCM/ADD 等）；加速来自上述 **3D 自回归 Swin 注意力的并行生成**，以及冻结 6B 参数带来的训练显存/时间下降（消融图 6 显示 CogView2 初始化使 loss 下降更快、收敛更好）。

## Infra（训练 / 推理工程）
- 计算资源由 **BAAI 提供**（致谢中提及 Hanxiao Qu 维护机器、BAAI 支持算力），但**具体 GPU 型号、卡数、GPU·时、训练总时长、并行/分布式策略未披露**。
- 已知工程要点：**FP16 混合精度**；Sandwich-LN + PB-Relax 稳定训练；冻结 60 亿 CogView2 参数大幅降低显存与时间开销。
- **推理加速**：3D 自回归 Swin 注意力允许远距帧 token 并行解码（突破标准自回归一次一 token 的限制）。
- **推理硬件（README 披露）**：训练 GPU 规模论文未披露，但 README 明确**推理推荐用 Nvidia A100**（也可在算力较弱的 GPU 上用更小的 `--max-inference-batch-size`/`--batch-size` 跑，或训更小模型）；提供 Docker 镜像与本地 local-attention CUDA kernel 编译流程。推理支持 classifier-free guidance（`--use-guidance-stage1`，README 强烈建议开启）。
- **部署形态**：开源代码 + 两阶段模型权重（cogvideo-stage1 / cogvideo-stage2）+ CogView2 超分（cogview2-dsr），经 `SAT_HOME` 环境变量自动下载（cogvideo-stage1/2 托管在 aminer LFS，cogview2-dsr 在 model.baai.ac.cn），另有 aminer 在线 demo 与 HuggingFace Space。**仅支持简体中文输入**（README 明确）；demo 输出为 4 秒 / 32 帧的视频片段。论文承认局限：因模型规模大 + GPU 显存限制，**输入序列长度仍受限**。

## 评测 benchmark（把效果讲清楚）
评测指标：FVD（基于 Kinetics-400 训练的 I3D）与 IS（基于 Sports-1M 预训练 + UCF101 微调的 C3D）。

**UCF-101（类标签作文本输入，FVD over 2048 样本 / IS over 10000 样本）：**

| 方法 | IS ↑ | FVD ↓ |
|---|---|---|
| VideoGPT | 24.69 | — |
| DVD-GAN | 27.38 | — |
| TGANv2* | 28.87 | 1209 |
| MoCoGAN-HD | 32.36 | 838 |
| DIGAN* | 29.71 | 655 |
| DIGAN | 32.70 | 577 |
| TATS-base | 79.28 | 332 |
| **CogVideo** | **50.46** | **626** |
| CogVideo（GT=tokenizer 重建）** | — | 545 |

（CogVideo 的 IS 50.46 大幅超越多数 GAN/VQ 基线，但 FVD 不及当时最强的 TATS-base 332；作者主打开域通用性与人评优势而非单点 FVD 刷榜。）

**Kinetics-600（16 帧、以前 5 帧为引子，FVD↓）：**

| 方法 | FVD ↓ |
|---|---|
| Latent Video Transformer | 224.73 |
| Video Transformer | 170 |
| DVD-GAN-FP | 69.15 |
| TriVD-GAN-FP | 25.74 |
| **CogVideo** | **109.23** |
| CogVideo（GT=tokenizer 重建）** | 59.55 |

**人评（90 名匿名评测者，UCF101 随机 30 类，对比 TGANv2、VideoGPT；从帧纹理、动作真实感、语义相关性 1-5 打分 + 整体 1-10 分）：**
- **49.53%** 评测者选 CogVideo 为最佳，VideoGPT 仅 15.42%、TGANv2 仅 5.6%。
- CogVideo 在帧纹理、动作真实感、语义相关性三项及整体质量均显著领先。

**消融（Kinetics-600 测试集 5000 样本子集，11 帧、引子 5 帧，11000 步 / batch 160；FVD↓）：**

| 设置 | FVD ↓ |
|---|---|
| **CogVideo（完整）** | **108.27** |
| − 分层（1-stage，Noverlap=1） | 137.13 |
| − 分层（1-stage，Noverlap=2） | 120.82 |
| − 视频预训练（仅用 CogView2 初始化） | 124.92 |
| − 预训练 − CogView2（随机初始化） | 166.13 |

**消融结论**：(1) 分层多帧率生成明显优于 1-stage 滑窗（无论 Noverlap 取值）；(2) CogView2 初始化的 FVD 显著低于随机初始化（166.13→124.92），且 loss 下降更快、收敛更好——双双验证「分层训练」与「继承文生图权重」两大核心设计的有效性。附录注意力可视化进一步显示：时序通道许多头不太关注帧自身，说明模型在时空特征上发生了一定**解耦**（空间通道管帧内特征、时序通道管跨帧关系），且对 CogView2 计算的空间特征高度依赖。

## 创新点与影响
**核心贡献**：
1. 据作者所称的**首个开源、通用开域、大规模预训练文生视频 Transformer**（9.4B）。
2. **首次系统地把预训练文生图模型迁移到文生视频**而不损害其图像生成能力——dual-channel attention（冻结空间通道 + 新增可训时序通道 + 共享 FFN + α 软融合），避免昂贵的从零预训练，降低能耗与碳排。
3. **多帧率分层训练**：用帧率 token 对齐文本-动作语义、控制变化强度，并以两阶段（顺序生成 + 递归插帧）生成连贯长视频。
4. 把 **Swin 注意力扩展到自回归时序场景**，在训练与推理上都获得并行加速。

**影响**：CogVideo 是 **[[cogvideox]] 系列的直接源头**，奠定了「文生图知识迁移到文生视频」「分层/多阶段生成」的技术路线，也是 2022 年与 Make-A-Video、Imagen Video 同期、但**开源**的代表性工作。其「冻结预训练 backbone + 新增轻量时序适配」的思路在后续视频生成（含 diffusion 时代）中反复出现。

**已知局限**：(1) 自回归 + 大模型导致**输入序列长度受 GPU 显存限制**；(2) 基础分辨率仅 160×160（靠 CogView2 超分到 480×480）；(3) 训练文本为中文（图 1 标注「actual text inputs are in Chinese」），跨语言通用性未充分验证；(4) FVD 单点不及当时最强专用模型（如 TATS-base）；(5) 误用/虚假信息风险，作者建议训判别分类器缓解。数据来源/清洗、算力规模等工程细节未披露。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2205.15868
- arxiv_pdf: https://arxiv.org/pdf/2205.15868
- github: https://github.com/THUDM/CogVideo （原始 CogVideo 分支；仓库现已迁移/更名为 zai-org/CogVideo，原工作在 `CogVideo` 分支）
- 模型权重（README 给出）: cogvideo-stage1 / cogvideo-stage2（aminer LFS）、cogview2-dsr（model.baai.ac.cn）

## 一手源存档（sources/）
- [arxiv-2205.15868.pdf](https://arxiv.org/pdf/2205.15868) （论文 PDF，已精读正文+附录）
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/cogvideo--github-readme.md) （原始 CogVideo 分支 README 快照，cloakbrowser 抓取）
