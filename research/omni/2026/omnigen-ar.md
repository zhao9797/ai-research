---
title: "OmniGen-AR: AutoRegressive Any-to-Image Generation"
org: "Fudan University + ByteDance Seed + HKU"
country: China
date: "2026-06"
type: paper
category: unified
tags: [autoregressive, any-to-image, unified-generation, next-token, visual-tokenizer, disentangled-causal-attention, image-editing, text-to-video, neurips-2025]
url: "https://arxiv.org/abs/2606.09156"
arxiv: "https://arxiv.org/abs/2606.09156"
pdf_url: "https://arxiv.org/pdf/2606.09156"
github_url: "https://github.com/wdrink/SimpleAR"
hf_url: ""
modelscope_url: ""
project_url: "https://wdrink.github.io/"
downloaded: [arxiv-2606.09156.pdf, omnigen-ar--author-homepage.md, omnigen-ar--github-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
OmniGen-AR 是一个**统一自回归（next-token）的 Any-to-Image 生成框架**：用**一个共享的图像-视频离散 tokenizer**（Cosmos-DV）把文本/空间条件（分割图、深度图）/视觉上下文（待编辑图、历史帧）全部离散成同一码本的 token，再用一个 decoder-only transformer（Qwen2.5 初始化）做下一 token 预测，单模型覆盖 T2I、T2V、帧预测、图像编辑、seg-to-image、depth-to-image 六类任务。最关键创新是 **Disentangled Causal Attention（DCA）**——一个仅训练期生效、不改推理流程的注意力掩码正则，抑制条件 token 向内容 token 的"信息泄漏/捷径"。最亮眼结果：1.5B 模型 **GenEval 0.63、VBench 总分 80.02**（首个用离散 token 的纯自回归模型在 VBench 破 80）。

## 背景与定位
现有自回归视觉生成（LlamaGen、SimpleAR、Emu3、VAR/Infinity）大多只支持**单一模态条件**（类别标签或文本 prompt），无法像真实应用那样响应分割掩码、参考图、历史帧等多样控制；而多条件的统一能力此前主要由 diffusion 侧承担（ControlNet、Uni-ControlNet、[[omnigen]] 等需要外挂适配器或分模态训练）。本文要回答的问题是：**能否在保持自回归"简单架构 + 简单优化目标 + 可交错生成"的前提下，用单一模型统一 any-to-image？**

技术脉络上它处在三条线交汇处：
- 离散 token 自回归视觉生成（VQ-VAE → Taming Transformer → LlamaGen → SimpleAR）。
- 统一多控制生成（ControlNet/Uni-ControlNet/[[omnigen]] 偏 diffusion；EditAR 偏 AR 但限于编辑/低层控制）。
- 统一多模态理解+生成（Chameleon、Emu3、Show-o、Janus、Transfusion）。

相对最接近的前作 **EditAR**（CVPR'25，也用 AR transformer 做多条件编辑），OmniGen-AR 的两点差异：① EditAR 专做图像编辑与低层控制（depth/edge/seg-to-image），OmniGen-AR 是覆盖更广输入模态（含 T2V/帧预测）的统一 Any-to-Image 框架；② EditAR 用蒸馏 loss 改善图文对齐，OmniGen-AR 用 DCA 这一**全新训练期注意力机制**防止信息泄漏。相对 diffusion 的 [[omnigen]]，系统级对比（论文 Table 1）显示 OmniGen-AR **额外支持视频生成**。

> 命名澄清：本工作与 BAAI/VectorSpaceLab 的 OmniGen（diffusion，arXiv 2409.11340，本文引用 [94]）**同名但非同一团队/同一模型**。OmniGen-AR 出自 **复旦大学 + 字节跳动 Seed + 香港大学**（Junke Wang 等），录用于 **NeurIPS 2025**。worklist 里登记的 org（BAAI/VectorSpaceLab）与 github（VectorSpaceLab/OmniGen）实为那篇前作 OmniGen，与本文无代码归属关系；作者主页给 OmniGen-AR 标的 Code 链接指向其 AR 基座仓库 `wdrink/SimpleAR`，本文未见独立官方代码仓。

## 模型架构
**整体 = 文本 tokenizer + 视觉 tokenizer + 自回归 transformer**（论文 Fig.2）。

- **Backbone**：decoder-only 自回归 transformer，标准多头注意力块，下一 token 预测。**用 Qwen2.5 同时作为文本 tokenizer 与 transformer 模型**（即语言模型权重初始化）。参数规模有 **0.5B 与 1.5B** 两档。
- **视觉 tokenizer（核心设计）**：采用**图像-视频联合离散 tokenizer Cosmos-DV（下采样 8×16×16）**。所有视觉输入——待生成图像 X、各类视觉条件 V（分割图、深度图、待编辑图、历史帧、视频）——都用**同一个 tokenizer / 同一个码本**离散成离散 token，使条件与内容、图像与视频共享统一表示。这与 ControlNet/ControlAR 给每种条件配单独 encoder 的做法相反，是"any-to-image"得以统一的关键。视觉条件 v∈R^N1 与待生成图像 x∈R^N2 满足 N1=N2。
- **文本 tokenizer**：Qwen2.5 的语言模型 tokenizer，得到文本 token t∈R^M。
- **序列构造（条件注入方式）**：把不同模态 token 沿序列维拼接。空间/图像条件任务用 `z=[t, v, x]`；纯文本条件任务用 `z=[t, x]`。无外挂模块、无 cross-attention 适配器——条件即"前缀 token"，靠自回归依赖建模。
- **Disentangled Causal Attention（DCA）**：把整条序列的因果掩码拆成**条件因果注意力**与**内容因果注意力**两段。设 A=[0,M) 文本、B=[M,M+N1) 条件、C=[M+N1,M+N1+N2) 内容；在普通下三角因果掩码基础上，**额外屏蔽 i∈C、j∈B 的注意力**（内容 token 不能看视觉条件 token），但内容 token 仍可看文本 token。直觉：编辑/帧预测里输出与输入高度重叠，普通因果注意力会让模型走捷径直接复制条件 token，而非真正按指令生成；DCA 切断"条件→内容"的泄漏路径，同时保留位置感知（条件 token 不像 CFG 那样被整体丢弃）。**DCA 只在训练期以一定概率替换普通因果掩码，推理仍是标准 next-token，不改变推理流程**——这点与 classifier-free guidance 明确区分。
- **分辨率策略**：SI/IV 阶段 512 分辨率，MT 阶段升到 1024。

## 数据
论文 4.1 节披露的训练数据（按三阶段组织，**全部图像/视频用 Qwen2-VL 重新打标 recaption**）：

- **第一阶段 单图（SI）预训练**：大规模图像集 CC3M、CC12M、OpenImages、SAM-1B、Megalith-HuggingFace（megalith-10m）；并纳入视频集 **Panda-70M 的 9M 子集**与 **HD-VILA-100M**，每条视频**随机取 1 帧**当图像用。
- **第二阶段 图-视频联合（IV）**：沿用一阶段数据集，但视频改为**每条采样 9 帧**（引入时序）。
- **第三阶段 多任务（MT）**：在多类高质量数据上联合训练——
  - 文生图：JourneyDB、Synthetic-dataset-1M（ProGamerGov DALL·E3 高质量 caption 集）、**10M 内部数据**；
  - 图像编辑：MagicBrush、InstructPix2Pix、SEED-Edit；
  - depth-to-image：MultiGen-Depth；
  - seg-to-image：MultiGen-ADE20K、MultiGen-COCOStuff；
  - 文生视频：OpenSora-pexels-45k、OpenVid-1M、**0.5M 高质量内部数据**。

**标注/再描述**：所有图像与视频都用 Qwen2-VL 重新生成 caption。**美学/安全过滤、配比权重、去重清洗等细节论文未披露**，仅交代了数据集清单与每阶段的帧采样策略。

## 训练方法
- **训练目标**：标准**语言建模损失（next-token prediction）** over 交错的多模态 token 序列；不同任务按 task-specific 格式拼 `z`。无 diffusion / flow-matching / masked-token 目标——是纯离散 AR。
- **三阶段课程**：① SI 单图预训练（512 分辨率，lr=1e-4）→ ② IV 图视频联合（512，引入 9 帧视频）→ ③ MT 多任务（**1024 分辨率，lr 降到 2e-5**）。**无 warmup、无 lr decay**。优化器 AdamW，全局 batch size 256（各阶段一致）。
- **DCA 作为训练正则**：在 IV 和 MT 阶段，以 **10% 概率**把标准因果掩码替换成 DCA 掩码；同样以 **10% 概率** drop 文本条件用于 classifier-free guidance。
- **推理**：逐 token argmax 采样 `ẑ_i = argmax p_θ(z_i | z_<i)`，再喂给视觉 tokenizer 的 decoder 还原图像；推理用 **CFG，scale=6.0**（沿用 LlamaGen/SimpleAR 做法）。
- **未使用**：本文**未报告** RLHF/DPO/reward model 偏好对齐，也**未做** consistency/LCM/ADD 等步数蒸馏（区别于其 AR 基座 SimpleAR 含 RL 阶段；OmniGen-AR 聚焦统一条件与 DCA，对齐/蒸馏留作未来工作，且作者把 scaling 与 CoT 列为 future work）。

## Infra（训练 / 推理工程）
- **算力**：**64× A100 GPU**，全局 batch size 256，三阶段共用。**总 GPU·小时数、训练时长、并行/分布式策略（TP/PP/FSDP 等）、混合精度与吞吐论文均未披露**。
- **推理加速**：依赖 CFG（scale 6.0）提质；**未报告** KV-cache 优化、量化、步数蒸馏等具体加速工程；自回归逐 token 解码的延迟数据未给出。
- **部署形态**：论文未提供开源权重/官方推理仓（作者主页 OmniGen-AR 的 Code 链接复用 SimpleAR 仓）。

## 评测 benchmark（把效果讲清楚）
全部数字来自已落盘 PDF（arxiv-2606.09156.pdf）的 Table 2–6，CFG=6.0，1.5B 为主力模型：

**文生图 · GenEval（Table 2）**
- Table 2 只列了四个数字列：Two-obj / Position / Color-attr / Overall（论文未把 Single-obj、Counting 列入表，故此处无 Counting 数字）。在 **<1B 参数档**，OmniGen-AR-0.5B 显著超越同档 diffusion 与 AR：Two-obj 0.74、Position 0.20、Color-attr 0.29、**Overall 0.55**，优于 SDv2.1（0.50）、LlamaGen-0.8B（0.32）、SimAR-SFT-0.5B（0.53）。
- 扩到 **1.5B 后 Overall 从 0.57 提到 0.63**（论文正文口径：0.5B→1.5B 提升体现可扩展性；1.5B 行各列 Two/Pos/Color/Overall = 0.94/0.30/0.40/0.63）。**注意**：Table 2 中 OmniGen-AR 的 Ours 行**未标 †**，即 0.63 **不使用 prompt rewriting**；表内仅 Infinity（0.73†）、Emu3（0.66†）用了 prompt rewriting。对比表里同 Overall 列：Show-o 0.68、Infinity 0.73†、Janus 0.61、Emu3 0.66†、SimAR-SFT 0.61、DALL·E2 0.52、LDM 0.37。即 OmniGen-AR 在**统一多任务模型里给出有竞争力的 T2I**，但单论 T2I 顶分并非全场最高。

**文生视频 · VBench（Table 3）**
- **0.5B**：Quality 76.60 / Semantic 67.20 / **Total 74.72**，已超 9B 的 CogVideo（67.01）约 11% 而参数远少。
- **1.5B**：Quality 81.51 / Semantic 78.08 / **Total 80.02**——**首个用离散 token 的纯自回归模型在 VBench 破 80**，超过 OpenSora V1.2（79.76）等 diffusion。对比：CogVideoX-5B 81.91、HunyuanVideo-13B 83.24、Wan2.1-1.3B 83.31（这几个更高，但 OmniGen-AR 是统一多任务且 AR 路线）。

**帧预测 · Kinetics-600（Table 4 左，FVD↓）**
- OmniGen-AR-1.5B **零样本 FVD 429**，优于 VideoPoet-8B 的 687（同为 zero-shot ∗）。

**图像编辑 · Emu-Edit test（Table 4 中）**
- OmniGen-AR-1.5B：**CLIP-text 相似度 CT=0.23、CLIP-image CI=0.84**，与 Emu-Edit（0.23/0.86）、[[omnigen]]（0.23/0.83）、MagicBrush（0.22/0.84）同级，属"有竞争力"区间。

**空间条件生成（Table 4 右）**
- seg-to-image（ADE20K，mIoU↑）：OmniGen-AR-1.5B **35.28**（ControlAR 39.95、[[omnigen]] 40.06 更高；优于 Uni-ControlNet 19.39、GLIGEN 23.78、EditAR 22.62、ControlNet 32.55）。
- depth-to-image（MultiGen-Depth，RMSE↓）：OmniGen-AR-1.5B **37.42**（ControlAR 29.01、[[omnigen]] 31.71 更优；说明纯 AR 在稠密空间条件下仍逊于专精 diffusion 控制）。

**关键消融**
- **DCA 替换概率扫描（0.5B，Table 5）**：0% → VBench 70.33 / Emu-CT 0.15 / Mask 24.76；**10%（默认）→ VBench 74.72 / Emu-CT 0.20 / Mask 25.33（最优区）**；20% 起回落、30% 明显下降。即 DCA 在 10% 概率时把编辑 CLIP-text 从 0.15 提到 0.20，并在 seg-to-image 上也有小幅增益。
- **Token Match Ratio（Fig.4）**：MagicBrush 上条件图与内容图同位置 token 大量重合（高 TMR 样本占比显著），佐证"信息泄漏"风险确实存在——这是 DCA 的动机证据。
- **联合 vs 分离训练（Table 6）**：联合训练**降低** T2I/T2V 单项（T2I 0.57→0.55、T2V 77.18→74.72，疑因编辑/空间数据视觉质量偏低），但**提升**编辑（Edit 0.18→0.20）与 seg（22.59→25.33）——说明强化文条件基础能力有助于下游泛化。
- **模型缩放（Fig.5 定性）**：0.5B→1.5B 在 T2I/depth/seg 上指令跟随与美感均提升。

**已知失败模式（Fig.8）**：① 细粒度指令落地失败（"移除长椅上的包"却把人移除）；② 稀疏空间控制下生成模糊/结构不一致（depth/seg-to-image），归因于噪声监督与训练覆盖不足。

## 创新点与影响
- **核心贡献**：① 用**共享图像-视频离散 tokenizer（Cosmos-DV）**把文本/空间/视觉上下文统一成同码本 token，实现单一 decoder-only AR 模型的 Any-to-Image（含 T2V/帧预测），保持 AR "简单目标 + 可交错生成"的优点而无外挂适配器；② **Disentangled Causal Attention**——首个面向"条件→内容信息泄漏"的训练期注意力正则，零推理开销、与 CFG 互补，10% 概率即在编辑/视频上稳定增益；③ 实证**纯离散 AR 首次在 VBench 破 80（80.02）**，并在 GenEval 0.63、Kinetics-600 帧预测、Emu-Edit 编辑上取得 SOTA 或竞争性结果。
- **影响/意义**：为"统一多控制生成"提供了 diffusion 之外的**纯自回归可行路径**，把 LLM 后端（Qwen2.5）与联合视觉 tokenizer（Cosmos-DV、OmniTokenizer 谱系）直接复用到多任务图像/视频生成，利于与多模态理解模型同栈统一；DCA 作为通用"防捷径"正则，对一切"输入与输出高度重叠"的条件生成任务（编辑、帧预测、inpainting）有借鉴价值。
- **已知局限**：① 稠密空间条件（depth/seg-to-image）仍逊于专精 diffusion 控制（ControlAR/OmniGen）；② 细粒度指令 grounding 与稀疏控制下画质不稳；③ 规模仅到 1.5B，未做偏好对齐/步数蒸馏；④ 训练 infra 细节（GPU·时、并行、吞吐）与数据配比/过滤未充分披露；⑤ 自回归逐 token 解码的推理效率未报告。作者把"扩大模型与数据建更强基座""引入 CoT 提升复杂 prompt 推理"列为后续方向。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2606.09156
- arxiv_pdf: https://arxiv.org/pdf/2606.09156
- author_homepage（确认 NeurIPS 2025 录用 + 作者 + Code 链接复用 SimpleAR 仓）: https://wdrink.github.io/
- code_repo（作者主页为 OmniGen-AR 标注的 Code，实为其 AR 基座 SimpleAR）: https://github.com/wdrink/SimpleAR
- 命名相关的前作 OmniGen（diffusion，不同团队，本文引用 [94]）: https://github.com/VectorSpaceLab/OmniGen ｜ https://arxiv.org/abs/2409.11340

## 一手源存档（sources/）
- [arxiv-2606.09156.pdf](https://arxiv.org/pdf/2606.09156) （OmniGen-AR 论文全文，已精读，PDF 不入 git）
- [author-homepage.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/omnigen-ar--author-homepage.md) （Junke Wang 主页快照，确认 NeurIPS'25 与归属）
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/omnigen-ar--github-readme.md) （前作 OmniGen diffusion 仓 README，仅作命名辨析与背景，非本文代码）
