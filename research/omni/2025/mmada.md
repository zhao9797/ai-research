---
title: "MMaDA: Multimodal Large Diffusion Language Models"
org: "Princeton University / Peking University / Tsinghua University / ByteDance Seed"
country: "USA / China"
date: "2025-05"
type: paper
category: unified
tags: [unified, discrete-diffusion, masked-diffusion, dllm, multimodal, t2i, reasoning, rl, grpo, neurips2025]
url: https://arxiv.org/abs/2505.15809
arxiv: https://arxiv.org/abs/2505.15809
pdf_url: https://arxiv.org/pdf/2505.15809
github_url: https://github.com/Gen-Verse/MMaDA
hf_url: https://huggingface.co/Gen-Verse/MMaDA-8B-Base
modelscope_url:
project_url: https://huggingface.co/spaces/Gen-Verse/MMaDA
downloaded: [arxiv-2505.15809.pdf, mmada--readme.md, mmada--hf-base-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
MMaDA 是首个把"文本推理 + 多模态理解 + 文生图"统一进**单一离散扩散（masked-token diffusion）骨干**的多模态基础模型——文本和图像都被离散 token 化后用同一个掩码预测目标训练，无模态特定组件；配套提出**混合长 CoT 冷启动 SFT** 与扩散原生的统一 RL 算法 **UniGRPO**。MMaDA-8B 在文本推理上超过 LLaMA-3-8B / Qwen2-7B 量级基线（GSM8K 73.4、MMLU 68.4），多模态理解超过 Show-o/SEED-X，文生图在 GenEval(0.63)、CLIP/ImageReward、以及世界知识生成 WISE-Cultural(0.67) 上超过 SDXL/Janus 等同期统一/专用基线。NeurIPS 2025 接收。

## 背景与定位
统一多模态基础模型此前主要走两条路线：(1) **纯自回归（AR）next-token**——如 Chameleon、Emu3、[[janus]]，把图像也离散化后用 NTP 一并建模，但视觉生成质量常落后于扩散；(2) **AR + 连续扩散混合**——如 [[show-o]] / Transfusion，文本用 AR、视觉用连续扩散，需在一个网络里塞两套异质目标（NTP + 连续 diffusion loss），机制复杂。两类工作的共同短板是**几乎只研究架构与预训练，缺乏对统一模型 post-training（CoT/RL）的系统探索**，尤其在非自回归（扩散）设定下。

MMaDA 选了第三条路：**全离散扩散一套损失**。它直接继承 [[llada]]（LLaDA-8B，纯文本的 masked diffusion LLM，即 dLLM）的思路并把它扩到多模态——文本和图像统一为离散 token，统一用"预测被 mask 的 token"这一个交叉熵目标训练。论文的核心主张是：**在统一扩散骨干上把 pretraining 和 post-training（混合 CoT + 扩散原生 RL）打通**，这是此前统一模型的空白。它是"用 diffusion-LLM 做统一生成"这条线（LLaDA → MMaDA → 后续 Lumina-DiMOO 等）上的关键一站，也是**第一个证明 diffusion-based MLLM 能有强理解能力**的工作。

## 模型架构
**骨干**：一个 modality-agnostic 的 Transformer 掩码 token 预测器 p_θ(·|x_t)，输入带 [MASK] 的混合序列，**一次并行预测所有被 mask 的 token**（图像 token 与文本 token 同等对待，无模态专用分支/适配器）。
- **权重初始化**：用 **LLaDA-8B-Instruct** 的预训练权重初始化（8B 参数），因此 MMaDA 本质是把一个已有的离散扩散文本 LLM 扩成多模态。
- **文本 tokenizer**：直接用 LLaDA 的 tokenizer（同骨干同词表）。
- **图像 tokenizer / VQ**：复用 **Show-o 提供的预训练图像量化器**，基于 **MAGVIT-v2** 架构。下采样因子 f=16，codebook 大小 8192；512×512 图像 → 32×32 = **1024 个离散语义 token**。图像 token 在"理解"和"生成"两类任务里都用同一套离散表示。
- **无独立 text encoder（T5/CLIP）**：与连续扩散 T2I 模型不同，MMaDA 没有外挂文本编码器，文本条件就是序列里的文本 token 本身，条件注入靠"prompt token 不被 mask、只对 response/图像 token 做 mask 预测"实现（类似 prefix 条件）。
- **统一概率形式**：前向加噪 = 按时间步 t∈[0,1] 随机把 token 替换成 [MASK]；反向 = 预测 mask 处原 token。训练损失只在被 mask 的 token 上计算交叉熵（式 1，Lunify）。这套形式对文本和图像完全一致，是"modality-agnostic"的来源。

## 数据
论文按训练阶段分别披露数据（未给出总 token 数 / 总图文对规模，属于**部分披露**）：
- **基础语言与多模态数据**：文本基础能力用 **RefinedWeb**；类条件图像生成用 **ImageNet-1k**；外加多个开源图文数据集（论文引用 [38–42]，未逐一展开）做 captioning / 图文对齐。
- **指令微调数据**：文本指令用 **Alpaca**；视觉指令用 **LLaVA-1.5** 指令数据。
- **推理数据（用于混合长 CoT SFT）**：
  - 文本数学/逻辑推理：**ReasonFlux、LIMO、s1k、OpenThoughts、AceMath-Instruct**。
  - 多模态推理：用 **LMM-R1** 模型在 **GeoQA、CLEVR** 上生成回答，**只保留答对的样本**（拒绝采样式过滤）。
  - **世界知识感知 T2I**：用 **GPT-4.1** 合成"事实条目—描述"配对（覆盖科学、文化、地标），并改写成统一 CoT 风格轨迹——这是 MMaDA 在 WISE 上强的直接来源。
- **RL 数据（UniGRPO）**：沿用上面的数学/逻辑/几何数据集（GSM8K 训练集、GeoQA、CLEVR 等）。
- **CoT 数据质量控制**：用开源 LLM/VLM 生成多样推理轨迹，再用 SOTA 模型当 verifier 过滤掉错误/浅显的推理，只留高质量长 CoT。
- 美学/安全过滤、去重等工业级清洗细节**未披露**。

## 训练方法
统一目标贯穿全程都是**离散扩散的掩码 token 预测（masked-token diffusion，等价于 absorbing-state discrete diffusion）**，分三大阶段（README 进一步细分为 6 个子阶段）：

**Stage 1 预训练（约 600K 步）**：
- 1.1 用 LLaDA-8B-Instruct 初始化，先在 **ImageNet-1k** 上做类条件图像生成，建立基础视觉能力（约 200K 步）。
- 1.2 把 ImageNet 换成更多样的图文对继续训练（约 400K 步），加入 RefinedWeb 文本与 captioning。
- 1.3 加入文本指令跟随训练。
- 损失：式(1) 的统一掩码交叉熵，t∼U[0,1] 均匀采样，仅对 mask token 计损。

**Stage 2 混合长 CoT 微调（Mixed Long-CoT SFT，约 50K 步）**：
- **统一 CoT 格式**（跨模态任务无关）：`|<special_token>| <reasoning_process> |<special_token>| <result>`，让文本推理、多模态推理、T2I 共用同一种"先推理后出结果"的结构，促成跨模态知识迁移（增强文本推理可直接提升生成图的事实正确性）。
- 训练机制：保留原始 prompt p0 不动，**只对 result（x0）独立做 token mask** 得到 r_t，输入 [p0, r_t] 让模型重建 r0（式 2，LMixed-SFT）。等价于把 prompt 当作干净 prefix 条件。
- README 透露 Stage 2 内部又分 2.1（先纯文本推理 + 提升图质）和 2.2（再加入多模态推理），是渐进式 curriculum。
- 作用：为最终 RL 阶段做 **cold-start**，让模型在 RL 之前就具备稳定的长链推理与统一输出格式。

**Stage 3 统一强化学习（UniGRPO，约 50K 步）**：这是论文方法上最核心的创新。把 GRPO 搬到离散扩散模型上要解决三个 AR-GRPO 不成立的难点：
1. **局部掩码依赖**——token 级 log-likelihood 只在被 mask 的位置才有定义；
2. **mask 比例敏感**——需对 response 采样一个 mask 比例来近似策略分布 π_θ；
3. **无 AR 链式法则**——序列级似然不能简单按 token 累乘。

UniGRPO 的三个关键设计：
- **结构化加噪（Structured Noising）**：对每条 response o_i，**均匀采样一个 mask 比例 p_i∈[0,1]** 构造扰动版（从几乎全 mask 到几乎全干净），让模型在 RL 时也覆盖多步去噪的各个阶段——充分利用扩散的多步生成能力。这一点区别于 d1（固定 mask 比例、只随机化问题端掩码，丢失了多步去噪信息）和 LLaDA 的 Monte-Carlo（对大量 mask 比例采样，如 128 次，算力昂贵）。
- **高效似然近似**：序列级 log-likelihood 用"对被 mask token 的 log p_θ 取平均"近似（式 3–4），避免 LLaDA 式昂贵采样。
- **结构化均匀时间步**：一次 prompt 内做 μ 步内更新，**先随机一个起始 timestep，再把剩余 timestep 在 [t1, T] 上均匀展开**（如起点 100、T=1000、5 步 → 100/300/500/700/900），比"完全随机 timestep"更稳、收敛更快（近似 MC 平均的效果，ablation 图 4 验证）。问题 q 始终不被 mask。
- **目标函数**（式 5）：标准 clipped surrogate + KL 正则（β·D_KL(π_θ‖π_ref)），advantage 用组内 reward 估计。

**Diversified Reward Modeling（统一 rule-based 奖励，式 6）**——按任务给不同奖励：
- 文本推理（GSM8K）：Correctness Reward 2.0（答对）+ Format Reward 0.5（符合 `<think>...</think>`）。
- 多模态推理（GeoQA/CLEVR）：同上 Correctness + Format；caption 类再加 CLIP Reward = 0.1·CLIP(image,text)。
- 文生图：CLIP Reward + Image Reward（人类偏好分），均 ×0.1 平衡量纲。

**推理期采样策略**（灵活、训练后免调）：
- **文本**：半自回归（semi-AR）去噪（沿用 LLaDA）——序列分块（block=64），块内按置信度低优先逐步 unmask；评测设 N=1024、512 步、每步 unmask 置信度最低的 2 个 token。半 AR 比定长非 AR 生成更细致。文本调度用 linear schedule。
- **图像**：纯并行非自回归——整张图当一个 block，low-confidence remasking + **cosine 噪声调度**（同 MAGVIT-v2），512×512 用 50 步去噪，CFG guidance scale=3.5。
- **关键超参**：64×A100(80GB)，global batch=1280，AdamW，lr=5e-5 + cosine 调度；扩散总 timestep T=1000。

## Infra（训练 / 推理工程）
- **算力**：主训练在 **64 张 A100 80GB** 上进行；global batch size 1280；提供 8 节点×8 GPU 的 DeepSpeed ZeRO-2 accelerate 配置（README）。RL 消融实验（UniGRPO vs d1）在 8×A100 上跑 GSM8K。
- **总 GPU·时 / 吞吐 / 并行细节未披露**（只给了步数：预训练 ~600K + SFT 50K + RL 50K 步）。混合精度具体设置未明示（用 HF accelerate + DeepSpeed ZeRO-2）。
- **推理加速**：扩散并行解码是天然优势——**每个去噪步并行出多个 token**，前向次数远少于 AR。论文用 Table 6 量化：图像生成从 1024 步降到 **50 步 CLIP 32.0、15 步 31.7**（vs 全 1024 步 32.8，几乎无损）；文本/多模态用 256–512 步（半/四分之一）即可（MMLU 512 步 66.3 vs 1024 步 66.9）。说明步数蒸馏空间大。
- **未做专门的步数蒸馏（consistency/LCM/ADD）**：加速来自扩散本身的并行性与降步，而非蒸馏。
- **部署形态**：开源（MIT license），HF 上有 Gradio Demo Space 与 MMaDA-8B-Base / MMaDA-8B-MixCoT 两个权重；支持 Apple MPS 推理（M4 实测）。UniGRPO 后续被整合进同组的 **dLLM-RL / TraceRL** 框架。

## 评测 benchmark（把效果讲清楚）
所有数字来自论文 Table 2–6（已抓取一手 PDF）。

**文本推理（Table 4，与 AR LLM 对比）**：
| 模型 | Arch | MMLU | ARC-C | TruthfulQA | GSM8K | MATH | GPQA |
|---|---|---|---|---|---|---|---|
| LLaMA-2-7B | AR | 45.9 | 46.3 | 39.0 | 14.3 | 3.2 | 25.7 |
| LLaMA-3-8B | AR | 64.5 | 53.1 | 44.0 | 53.1 | 15.1 | 25.9 |
| Qwen2-7B | AR | 70.3 | 60.6 | 54.2 | 80.2 | 43.5 | 30.8 |
| LLaDA-8B | Diffusion | 65.9 | 47.9 | 46.4 | 70.7 | 27.3 | 26.1 |
| **MMaDA-8B** | Diffusion | **68.4** | **57.4** | 43.1 | **73.4** | **36.0** | **28.4** |

MMaDA 在 MMLU/ARC-C 上接近 Qwen2-7B/LLaMA-3-8B，并在数学（GSM8K/MATH/GPQA）上**一致超过同源的 LLaDA-8B**（GSM8K 73.4 vs 70.7、MATH 36.0 vs 27.3），证明多模态联合训练 + CoT/RL 反而提升了纯文本推理。仅用开源文本数据、有限 task token，仍逊于 Qwen2 在 GSM8K/MATH 的强结果。

**多模态理解（Table 2）**：MMaDA 在 POPE 86.1、MME 1410.7、Flickr30k 67.6、VQAv2 76.7、GQA 61.3、MMMU 30.2、MMB 68.5、SEED 64.2 等上，与 LLaVA-v1.5 / InstructBLIP / Qwen-VL-Chat 等理解专用模型可比或更优，并在多个 benchmark 上一致超过统一模型 Show-o / SEED-X / Emu / Chameleon / LWM。论文强调这是**首次展示 diffusion-based MLLM 具备强理解能力**。

**文生图（Table 3）**：MMaDA Overall：
- **GenEval Overall 0.63**（Single 0.99 / Two 0.76 / Counting 0.61 / Colors 0.84 / Position 0.20 / Color-Attr 0.37），优于 SDXL(0.55)、Show-o、Janus、SDv2.1 等同期统一/专用基线（构图与计数尤强，得益于推理增强）。
- **CLIP Score 32.46**、**ImageReward 1.15**——在所有对比模型里最高（直接受益于 UniGRPO 把 CLIP/ImageReward 当奖励）。
- **WISE-Cultural 0.67**（世界知识感知生成）——显著超过先前方法（受益于文本推理联合训练 + GPT-4.1 合成事实 CoT 数据），是 MMaDA 最差异化的结果。

**消融（Table 5，分阶段叠加）**——清楚展示三阶段递进：
| 阶段 | GSM8K | MATH500 | GeoQA | CLEVR | CLIP Score | ImageReward |
|---|---|---|---|---|---|---|
| Stage 1 后 | 17.4 | 4.2 | 8.3 | 10.3 | 23.1 | 0.69 |
| + 混合长 CoT SFT | 65.2 | 26.5 | 15.9 | 27.5 | 29.4 | 0.84 |
| + UniGRPO（最终） | **73.4** | **36.0** | **21.0** | **34.5** | **32.5** | **1.15** |

混合 CoT SFT 带来巨大跃升（GSM8K 17.4→65.2、MATH500 4.2→26.5、CLIP Score 23.1→29.4），UniGRPO 再进一步全面提升（GSM8K→73.4、CLIP Score→32.5、ImageReward→1.15）——**推理与生成两类能力被同一 RL 同时拉高**。

**UniGRPO 设计消融（图 3/4，GSM8K reward 曲线）**：UniGRPO 全程 reward 高于 d1（diff-GRPO）——证明"不 mask 问题、只对答案做部分 mask、覆盖多步去噪"优于 d1 的固定 mask；"均匀展开 timestep"比"完全随机 timestep"更稳、收敛更快。

**任务扩展（无需额外微调）**：扩散骨干天然支持三模态 inpainting/外推（文本补全、VQA 答案补全、图像 inpainting），因为这些都等价于掩码预测，已内嵌训练目标——比 Show-o（仅图像 inpainting）更通用。

## 创新点与影响
**核心贡献**：
1. **首个全离散扩散的统一多模态基础模型**：文本 + 图像理解 + 图像生成共用一套掩码扩散损失、无模态特定组件，证明 diffusion-LLM 可同时做强理解、强推理、强生成。
2. **混合长 CoT 统一格式 SFT**：用 task-agnostic 的 `<reasoning>/<result>` 格式打通跨模态推理，作为 RL 冷启动；揭示"文本推理增强直接改善图像事实性"的跨模态协同。
3. **UniGRPO——扩散原生的统一 RL**：解决 AR-GRPO 在扩散上不成立的三难点（结构化加噪 + 均匀时间步 + 似然近似），并用多样化 rule-based 奖励统一推理与生成的 post-training，比 LLaDA(MC 昂贵)/d1(过简化) 更优。

**影响**：作为 LLaDA → MMaDA 这条 diffusion-LLM-for-unified-generation 主线的关键节点，把"统一扩散模型的 post-training（CoT+RL）"从空白推到可用；UniGRPO 后续被同组整合进 **dLLM-RL / TraceRL** 通用框架并衍生出 TraDo 系列；2025-11 又推出 **MMaDA-Parallel**（thinking-aware 并行图像编辑/生成，arXiv:2511.09611），把文本-图像在整条去噪轨迹上做双向交互。NeurIPS 2025 接收。

**已知局限**（作者自陈 + 数据可见）：
- **模型规模仅 8B**，作者明确表示需更大模型才能更强；纯文本推理仍逊于 Qwen2-7B 在 GSM8K/MATH 上的成绩。
- 生成分辨率仅 512×512（受 MAGVIT-v2 tokenizer + 1024 token 序列限制），GenEval 的 Position(0.20) 仍弱。
- 总训练 token / GPU·时 / 数据配比等工业细节**部分未披露**；UniGRPO 的 RL 仍依赖 rule-based 简单奖励（CLIP/ImageReward/规则正确性），无完整 reward model / 人类偏好 RLHF。
- 论文公开了 Base 与 MixCoT 权重，但 **MMaDA-8B-Max（UniGRPO 之后的最终版）截至 README 仍"coming soon"未放出**——即评测里的最佳数字对应权重未完全开源。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2505.15809
- pdf: https://arxiv.org/pdf/2505.15809
- github: https://github.com/Gen-Verse/MMaDA
- hf model (Base): https://huggingface.co/Gen-Verse/MMaDA-8B-Base
- hf model (MixCoT): https://huggingface.co/Gen-Verse/MMaDA-8B-MixCoT
- hf demo space: https://huggingface.co/spaces/Gen-Verse/MMaDA
- RL infra (dLLM-RL / TraceRL): https://github.com/Gen-Verse/dLLM-RL
- 后续工作 MMaDA-Parallel: https://arxiv.org/abs/2511.09611

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2505.15809.pdf
- ../../../sources/omni/2025/mmada--readme.md
- ../../../sources/omni/2025/mmada--hf-base-card.md
