---
title: "ACE++: Instruction-Based Image Creation and Editing via Context-Aware Content Filling"
org: "Alibaba Tongyi Lab (ali-vilab)"
country: China
date: "2025-01"
type: tech-report
category: edit
tags: [instruction-edit, subject-reference, flux, inpainting, lora, diffusion, rectified-flow, dit]
url: "https://arxiv.org/abs/2501.02487"
arxiv: "https://arxiv.org/abs/2501.02487"
pdf_url: "https://arxiv.org/pdf/2501.02487"
github_url: "https://github.com/ali-vilab/ACE_plus"
hf_url: "https://huggingface.co/ali-vilab/ACE_Plus"
modelscope_url: "https://modelscope.cn/models/iic/ACE_Plus/summary"
project_url: "https://ali-vilab.github.io/ACE_plus_page/"
downloaded: [arxiv-2501.02487.pdf, ace-plus-plus--readme.md, ace-plus-plus--hf-modelcard.md, ace-plus-plus--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ACE++ 是通义实验室在 [[flux-1]] 上后训练出的统一指令编辑/参考生成框架：把前作 ACE 的 Long-context Condition Unit (LCU) 与 FLUX.1-Fill-dev 的 inpainting 通道拼接输入格式融合为 **LCU++**——把"图像+掩码+噪声"在**通道维**而非序列维拼接，再用**两阶段训练**（0-ref 预训练 → 全任务微调）把单一模型扩展到任意编辑 + 主体/人像参考生成 + 局部编辑。因是纯技术报告，只给定性结果（无 FID/GenEval 等定量数字），但其开源的 portrait/subject/local LoRA 与 FFT 模型成为社区主流的"免训练换脸/换装/贴 logo"方案，[[step1x-edit]] 等工作把它列为开源对照基线。

## 背景与定位
痛点：开源 T2I 基座（[[flux-1]]、SDXL）很强，但**通用图像编辑**模型落后；要充分用上生成先验，业界惯例是 fine-tune T2I 基座而非从零训。问题在于 T2I 与编辑任务的**输入输出格式不一致**，导致适配收敛慢、训练成本高。

技术脉络中的两条线被 ACE++ 缝合：
- **ACE（前作，arXiv 2410.00086）** 提出 LCU：把多模态条件（文本指令 + 多张图 + 掩码 + 噪声 latent）在 **token 序列维**拼接喂给 DiT，统一 8 类生成任务。代价：每个条件序列都进 attention，attention 阶段算力上升、适配训练贵。
- **FLUX.1-Fill-dev（[[flux-1-tools]]）** 做 inpainting 时，把"待编辑图 + 区域掩码 + 噪声 latent"沿**通道维**拼接到 T2I 模型上——这恰好不引入额外序列，适配快。

ACE++ 的核心 insight：把 ACE 里属于 **0-ref 任务**（无参考图，如可控生成、inpainting、单图编辑）的那部分 LCU，从"序列拼接"改成"通道拼接"，避免破坏 T2I 训练时养成的上下文感知，从而显著降低适配成本；再把这个范式扩展到 N-ref（带参考图）任务，得到 **LCU++**。相对前置工作的改进就是：统一性继承自 ACE，适配效率借自 FLUX-Fill 的通道拼接思路，二者合一。

相关工作对照（论文 Related Works）：[[omnigen2]] 系（OmniGen）用语言模型初始化联合建模文图；UniReal 把图像级任务当"不连续视频生成"沿序列维拼条件训全注意力；OminiControl 用参数复用注入条件但难以多任务——这些要么从零训成本高，要么多任务受限。ACE++ 主打"后训练 + 低成本统一"。

## 模型架构
- **Backbone**：直接复用 [[flux-1]]（FLUX.1-dev）的全注意力 **MMDiT / DiT** 框架；vertical LoRA 模型则在 **FLUX.1-Fill-dev**（FLUX.1-dev 上训出的 inpainting 模型）上轻量微调。Text encoder / VAE 均沿用 FLUX 原生组件（T5 + CLIP 文本编码、FLUX VAE，论文未单列改动）。
- **LCU++ 输入范式（核心创新，§3.2）**：
  - Conditional Unit `CU = {T, V}`，其中 `V = {[I_1;M_1], …, [I_N;M_N], [X_t;M_N]}`（T 文本指令，I 图，M 掩码，X_t 时刻 t 噪声 latent）。
  - 旧 ACE 的 0-ref 把条件序列 `[I_in;M_in]` 追加到噪声序列 `[X_t;M_in]`（**序列拼接**）。
  - LCU++ 改为 **通道维拼接**：`V++_0ref = {[I_in; M_in; X_t]}`，即图、掩码、噪声三者沿 channel 叠在一起，不增加注意力序列长度，不破坏 T2I 上下文感知。
  - 扩展到 N-ref：把多个 `V++` 沿目标上下文**序列拼接**——`V++ = {[I_1;M_1;X_t1], [I_2;M_2;X_t2], …, [I_N;M_N;X_tN]}`，每个参考各带一份噪声 latent。这样参考与目标共享一套 context-aware 机制。
- **条件注入与 tokenizing**：每个 CU 内 图/掩码/噪声沿通道拼成 CU feature map → 经 `x-embed` 层映射成 token → 所有 CU token 拼接送入 transformer 层（架构图 Fig.1）。
- **FFT 模型的通道工程（README + HF modelcard 披露，论文正文未提）**：为在同一权重内**区分 repainting 任务与 editing 任务**，额外引入 **64 个通道**：这 64 通道放被编辑图在像素空间的 latent 表示，其余通道与 repainting 任务保持一致。后果是 **FLUX-Fill-Dev 的输入通道从 384 增到 448**（见 `config/ace_plus_fft.yaml`）。modelcard 进一步给出**为什么需要这 64 通道**：repainting 任务在 VAE latent 里用**零像素值**填修改区，而 editing 任务在该区放**真实 RGB 像素**经 VAE 编码的 latent，其分布与 repainting 任务的"未修改部分"高度相似，导致模型难以区分两类任务；加这 64 通道专放被编辑图 latent 后，模型对不同任务的适配性显著提升。
- **参数量与分辨率**：未单列总参数量（基座为 FLUX.1-dev 约 12B 级 DiT，论文未复述）。分辨率/序列长度由 `MAX_SEQ_LEN`（= H/16 × W/16）控制；推理时 `max_seq_length` 范围 **2048–8192**，越大图越清晰、显存越高（README）。
- **训练目标与上下文重建（§3.3）**：噪声 latent `x_t = {X_t^i}` 由 `{I_1,…,I_{N-1}, I_o}` 线性插值构造（I_o 目标图，I_N 是待修改样本——编辑任务即待编辑图，参考生成任务则置为**全零样本**）。模型预测 velocity `u_t = dx_t/dt`（rectified-flow / flow-matching 风格）。损失分两部分：`L = L_ref + L_tar`，`L_ref` 是前 N-1 个参考样本的**重建损失**（0-ref 时为 0），`L_tar` 是目标样本预测损失。同时优化"重建参考"和"生成目标"是模型获得 context-aware 能力的关键设计。

## 数据
- **数据来源**：完全复用前作 **ACE（Han et al. 2024a）收集的多任务数据**，覆盖 ACE 归纳的 **8 大类生成任务**（可控生成、inpainting、单图编辑、参考生成、风格/语义编辑等）。论文未给数据条数、配比、清洗/过滤、re-caption、合成数据等任何具体规模数字——**这些维度未披露**。
- **任务划分**：分 **0-ref 任务**（无参考图）与 **N-ref 任务**（带参考图）两类，对应两阶段训练。
- **vertical 数据切分**：portrait（人像一致性）、subject（主体一致性）、local editing（局部重绘）三个垂域各自用 ACE 数据子集训 LoRA。
- 训练 CSV 字段（README）：`edit_image / edit_mask / ref_image / target_image / prompt / data_type(portrait|subject|local)`，用 `#;#` 分隔——可佐证数据是"参考图 + 待编辑图 + 掩码 + 目标图 + 指令"的多元组结构。

## 训练方法
- **训练目标**：flow-matching / rectified-flow 速度预测（见架构节损失 `L_ref + L_tar`），与 FLUX 一脉相承。
- **两阶段训练（§3.4，核心方法）**：
  1. **Stage 1 单条件预训练**：在 T2I 基座上只用 **0-ref 任务**数据训，让模型快速长出"条件输入"支持而不引入额外序列。社区里已有满足这一范式的现成模型（**FLUX.1-Fill-dev 主攻 inpainting，可直接当 Stage 1 初始化加速**）。
  2. **Stage 2 多条件微调**：在 Stage 1 模型上用 **全部 0-ref + N-ref 任务**做 full fine-tuning，习得通用指令跟随能力。
- **工具套件（§3.5）**：
  - **全功能 FFT 模型**：用 FLUX.1-dev 在 ACE 全量数据上**全参微调**的 all-in-one 模型。
  - **垂域 LoRA 模型**：论文（§1/§4.1/结论）把轻量模型定位为覆盖 **四个垂直场景**——portrait consistency / subject-driven / local editing / image variation(repainting)；**实际开源的是 3 个 LoRA**（portrait / subject / local editing），直接在 **FLUX.1-Fill-dev** 上做 LoRA 轻量微调（因 Fill-dev 已满足 Stage 1 的 0-ref 范式）。LoRA rank：portrait **lora64**、subject **lora16**、local **lora16**（README 文件名 `comfyui_portrait_lora64 / subject_lora16 / local_lora16`）。
- **关键超参（§4.1 + README）**：
  - 优化器 **AdamW**，weight decay **1e-2**，learning rate **1e-3**；梯度裁剪 L2 norm 阈值 **1.0**。
  - **CFG 蒸馏适配 trick**：FLUX.1-dev 是 guidance-distilled 模型，训练需混合条件/无条件。关键技巧是把 **guidance scale ω 设为 1.0、无条件概率设 0.1**——因为 `v_t = v_t(∅) + ω(v_t(c) − v_t(∅))`，当 ω=1.0 时 `v_t = v_t(c)`，即不再叠加 CFG 偏移，避免与蒸馏过的基座冲突。
  - LoRA 训练 `MAX_SEQ_LEN` 默认 **2048**（= H/16 × W/16），可开 gradient checkpointing 省显存。
- **加速/蒸馏**：未做步数蒸馏 / consistency / LCM；推理速度依赖 FLUX 基座本身。
- **诚实披露的训练困难（README News，一等公民信息）**：作者明确说**在 FLUX 上做后训练遇到重大挑战**——训练集与 FLUX 模型异质性高导致训练高度不稳定；FLUX-Dev 是蒸馏模型，其原始 negative prompt 对最终性能的影响不确定。因此 **FFT 模型在多数任务上性能反而不如 LoRA 模型**，官方推荐用 LoRA；FFT 仅供学术探索。后续 ACE 路线**改为在 Wan 系基座上后训练**，FLUX 路线的进一步开发已暂停。

## Infra（训练 / 推理工程）
- **训练显存**：默认配置下 **LoRA 训练显存 38–40GB**（README，单卡量级）。算力规模 / GPU 数 / GPU·时 / 并行策略 / 吞吐 / 混合精度——**均未披露**。
- **注意力后端**：`ATTN_BACKEND` 可选 `flash_attn`（需 flash-attn2）或 `pytorch`（PyTorch ≥2.4.0 用原生 SDPA）；可开 `USE_GRAD_CHECKPOINT` 省显存换速度。
- **推理工程**：基于 **Scepter** 框架（modelscope/scepter）；模型托管 HF（ali-vilab/ACE_Plus）与 ModelScope（iic/ACE_Plus），scepter_path 形如 `ms://iic/ACE_Plus@subject/comfyui_subject_lora16.safetensors`。
- **推理显存/清晰度权衡**：`max_seq_length` 2048–8192 直接控制 token 序列长度→显存与图像清晰度（越小越省显存、图越糊）。
- **部署形态**：Gradio GUI demo（`demo_lora.py` / `demo_fft.py`）、HF/ModelScope 在线 Space、以及大量社区 **ComfyUI** 工作流（官方提供 LoRA/FFT 多套 workflow JSON，且推荐 LoRA workflow 因结果更稳）。依赖基座 FLUX.1-Fill-dev，常与 **FLUX.1-Redux** 联用做参考生成/编辑。
- **量化**：官方未提供量化方案（社区 ComfyUI 工作流另行处理）。

## 评测 benchmark（把效果讲清楚）
- **本作为纯技术报告，全文只有定性可视化，无任何定量 benchmark 表**。论文 §4.2 仅展示三类能力的图例：
  - **参考生成 Reference Generation**（Fig.3 subject-driven / Fig.4 portrait-consistency）：在不同场景维持特定主体/人像身份一致性，应用于影视特效、广告、电商设计。
  - **局部 & 通用编辑 Local/General Editing**（Fig.5/Fig.6）：相比传统 inpainting，能在重绘掩码区时保留原结构信息；支持加/删物体、上色、改文字、透视变化、配色变化、换场景等开放式编辑。
  - **局部参考编辑 Local Reference Editing**（Fig.7）：对图像特定区域做参考引导生成（试穿 try-on、商品图、贴 logo、换脸），且**这些任务在训练阶段未专门训练，可零样本（zero-shot）支持**。
- **FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / GEdit / MagicBrush / Arena ELO**：本作**均未报告**（不得编造）。
- **第三方定量对照（不在本作来源内，仅作定位参考）**：本仓索引中的 [[step1x-edit]] 等后续编辑工作把 ACE++ 列为开源对照基线，具体分数见各自页面，不在此处臆测。
- **官方自评的相对优劣**：作者反复强调 **LoRA 模型 > FFT 模型**（FFT 因 FLUX 后训练不稳而退化），推荐生产用 LoRA。
- **已知缺陷（README Limitations）**：删除/新增物体时指令跟随有缺陷（推荐改用 local editing 的 repainting 方式）；生成结果可能有 artifact，**手部生成尤其容易扭曲变形**。

## 创新点与影响
- **核心贡献**：
  1. **LCU++ 输入范式**——把 0-ref 任务的条件从"序列拼接"改为"通道拼接"，避免破坏 T2I 上下文感知、降低适配成本；再扩展到 N-ref，统一任意编辑 + 参考生成。
  2. **两阶段训练**（0-ref 预训练借力 FLUX-Fill 现成权重 → 全任务微调），把后训练大规模多模态生成模型的成本与周期显著压低。
  3. **context-aware 双损失**（参考重建 `L_ref` + 目标生成 `L_tar`），让单模型同时学"记住参考"和"生成目标"。
  4. **开源工具套件**：1 个全功能 FFT + 3 个垂域 LoRA（portrait/subject/local），覆盖换脸、换装试穿、贴 logo、主体一致性、超分、深度/轮廓可控生成等。
- **影响**：成为开源社区**免 LoRA 训练、免 PuLID 的一致性换脸/换装/贴 logo 主流方案**，催生大量 ComfyUI 工作流与 B 站/YouTube 教程，并被后续开源编辑模型（[[step1x-edit]]、[[in-context-edit-icedit]] 等）当作对照基线。它把 FLUX-Fill 的通道拼接思路系统化为通用编辑范式，是"在强 T2I 基座上低成本后训练统一编辑器"路线的代表作之一。
- **已知局限**：纯定性、无定量评测难以横向量化；FFT 模型因 **FLUX 蒸馏基座 + 数据异质**导致训练不稳、性能反不如 LoRA；手部等细节有 artifact；删/增物体指令跟随弱。作者据此**暂停 FLUX 路线、转向 Wan 基座**（见 [[vace]] 等后续 Wan 系工作），是这条技术路线诚实的转折信号。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2501.02487
- paper (PDF v3, 2025-01-15): https://arxiv.org/pdf/2501.02487
- github: https://github.com/ali-vilab/ACE_plus
- hf model: https://huggingface.co/ali-vilab/ACE_Plus
- modelscope model: https://modelscope.cn/models/iic/ACE_Plus/summary
- project page: https://ali-vilab.github.io/ACE_plus_page/
- hf demo space: https://huggingface.co/spaces/scepter-studio/ACE-Plus
- base model FLUX.1-Fill-dev: https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev
- predecessor ACE (arXiv): https://arxiv.org/abs/2410.00086

## 一手源存档（sources/）
- [arxiv-2501.02487.pdf](https://arxiv.org/pdf/2501.02487)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ace-plus-plus--readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ace-plus-plus--hf-modelcard.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ace-plus-plus--project-page.md)
