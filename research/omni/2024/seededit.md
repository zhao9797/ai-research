---
title: "SeedEdit: Align Image Re-Generation to Image Editing"
org: ByteDance
country: China
date: "2024-11"
type: tech-report
category: edit
tags: [image-editing, instruction-editing, diffusion, t2i-bootstrap, self-distillation, causal-attention, iterative-alignment, bytedance-seed]
url: "https://arxiv.org/abs/2411.06686"
arxiv: "https://arxiv.org/abs/2411.06686"
pdf_url: "https://arxiv.org/pdf/2411.06686"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/en/seededit"
downloaded: [arxiv-2411.06686.pdf, seededit--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
SeedEdit（作者 Yichun Shi、Peng Wang、Weilin Huang，ByteDance Seed Team；arXiv v1 2024-11-11）是字节 Seed 团队提出的指令式图像编辑扩散模型，核心思想是把"图像编辑"重新表述为**重建（reconstruction）与再生成（re-generation）之间的最优平衡**——从一个弱的 T2I 生成器自举出多样化的编辑配对数据，再通过**迭代对齐（iterative alignment）**逐步蒸馏成强编辑器。在 HQ-Edit 基准上 GPT 编辑成功分达到 **78.54**（in-house DiT 基座），显著超越 InstructPix2Pix（47.50）、MagicBrush（47.51）、UltraEdit（54.17），是 Seed 系列编辑模型（后续 SeedEdit 1.6 / 3.0）的开端。

## 背景与定位
图像编辑长期落后于图像生成与图像理解两端。论文把已有方法分为两类，并各自指出瓶颈：

1. **Training-free 方法**：依赖 DDIM Inversion（[[ddim]] 反演）、test-time 微调（DreamBooth/Imagic）、注意力控制（[[prompt-to-prompt]] / MasaCtrl）来"先重建输入图、再按新文本重生成"。问题在于重建与再生成两个过程**各自都不稳定**，组合后误差累积，输出常常既不忠于输入也不忠于目标描述。
2. **数据驱动方法**（[[instructpix2pix]]、MagicBrush、[[ultraedit]]、Emu Edit、Paint-by-Inpaint 等）：用大规模配对编辑数据训练指令扩散模型。核心困难是**编辑配对数据极稀缺**——不像图像可从互联网海量采集，几乎不可能收集到覆盖所有编辑类型的高质量配对集，因此现有工作用 Prompt-to-Prompt 或 inpainting 等工具合成数据，性能上限被这些"本身也不令人满意"的工具卡死。

SeedEdit 的定位是**绕开"采集/合成高质量配对数据"这一硬瓶颈**：把 T2I 模型视为一个"弱编辑器"（换个 prompt 重新生成即完成最朴素的"编辑"），再通过对齐把它蒸馏成"在保留原图与服从指令之间取得最优平衡"的强编辑器。作者明确把任务的本质刻画为一条从「完全重建」到「完全再生成」的连续轴，编辑就是在这条轴上找最优点。它是 ByteDance Seed 图像编辑路线的第一代工作；官方页面已显示后续迭代到 SeedEdit 1.6 与 **SeedEdit 3.0**（2025-06 发布，见"创新点与影响"）。

## 模型架构
**Causal Diffusion Model with Image Input（带图像输入的因果扩散模型）** 是本文的关键架构贡献。

- **基座**：论文用两个基座做实验——开源 **SDXL**（U-Net 架构）和一个字节**自研的基于 DiT 的 in-house T2I 模型**（架构取向 DiT / SD3 风格的 [[mmdit]]，引用 Peebles & Xie 的 DiT 与 Esser 等的 rectified-flow transformer）。因此架构图给出两种形态：**(a) Causal U-Net** 与 **(b) Causal MM-DiT**。
- **条件注入方式（与 InstructPix2Pix 的关键区别）**：IP2P 是给 U-Net **额外增加输入通道**来注入条件图像；SeedEdit 不增加输入通道，而是**复用 self-attention**——用**两条共享参数（shared parameters）的扩散分支**，一条处理输入图、一条处理带噪声的输出图，两条分支通过一个**因果自注意力（Causal Self-Attention，MM-DiT 形态下为 Causal MM-SelfAttention）**结构互相通信、基于中间特征建立联系。指令文本通过 cross-attention 注入。
- **设计动机与好处**：该设计灵感来自 training-free 的互注意力控制（MasaCtrl）。经验上它在**几何形变（geometric deformation）类编辑任务上表现更好**，且**引入的新参数更少**。"因果"体现在：若**丢掉输入分支**就退化回原始 T2I 扩散模型，从而允许**编辑数据与纯 T2I 数据混合训练**（mixed training）——这点对保留 T2I 的再生成能力很关键。
- **参数量 / 分辨率策略**：**未披露**（论文未给出基座与编辑模型的具体参数量、训练/推理分辨率）。

## 数据
SeedEdit 的数据完全靠**自举生成 + 过滤**，不依赖外部采集的配对集：

- **初始配对数据生成**：用预训练 T2I 模型当编辑模型，按"编辑前/编辑后"各自对应一段文本描述来生成图像对，思路类似 [[instructpix2pix]]。但朴素的"换 prompt 重生成"会导致前后两图**一致性差**。
- **多样性策略**：为覆盖尽可能多的编辑类型，作者**组合多种再生成技术与参数**（prompt-to-prompt、注意力控制等），并刻意**注入更多随机性**生成大规模配对数据集，再用**过滤器（filters）挑选好样本**用于训练与对齐。论文用 CLIP 指标（Fig.3）说明：对齐后的模型能在相近/更高的 CLIP Direction Score（指令服从）下取得**明显更高的 CLIP 图像相似度**，即"以更好的一致性换取同等的编辑强度"。
- **迭代数据再生成**：进入迭代对齐阶段后，**用当前编辑模型按同一流程生成新一批数据**，再标注、过滤、回灌微调（细节见"训练方法"）。
- **数据规模 / 配比 / 清洗细节 / re-caption 具体做法 / 美学与安全过滤**：论文均**未披露具体数字**（"large-scale pairwise dataset" 仅为定性描述）。
- 注：官方项目页现描述的是后续 **SeedEdit 3.0** 的数据方案（多源数据 + meta-info 多粒度标签：data-level task label / text-level recaption / pixel-level tagging，融合合成数据、专业编辑、传统编辑算子、视频帧/多片段抽取的图像对），这是 3.0 的工作，**不属于本文 1.0**，此处仅作脉络对照，不计入 1.0 的数据披露。

## 训练方法
SeedEdit 的训练范式可概括为「**弱 T2I 编辑器 → 蒸馏出初始编辑模型 → 多轮迭代对齐**」：

1. **初始蒸馏**：用 T2I 生成的配对数据，把 T2I 蒸馏成一个**图像条件化的编辑模型**（image-conditioned editing model），即上文的因果扩散模型。由于数据本身有噪，初始模型"能覆盖多样编辑任务，但成功率有限、鲁棒性不足"。
2. **Iterative Alignment（迭代对齐）**：渐进式地为编辑模型加额外几轮微调。每一轮：用**当前编辑模型**按相同流程生成新配对数据 → 标注 + 过滤 → 微调编辑模型（架构同上） → 重复，**直到模型收敛**（在 CLIP / GPT 指标上不再提升）。本质是一个自蒸馏 / 自举闭环，逐步把"重建 vs 再生成"的平衡点推到最优，并提升成功率。
3. **训练目标**：论文以扩散框架表述（diffusion model）；in-house 基座引用 rectified-flow transformer（[[rectified-flow]] / SD3 路线），但**未明确给出 1.0 的具体损失形式（DDPM ε-pred / v-pred / flow-matching）、步数蒸馏或一致性蒸馏（LCM/ADD）等加速细节、以及超参**——均**未披露**。
4. 对比之下，官方页面披露的 SeedEdit **3.0** 才引入"**diffusion loss 与 reward model 联合学习（joint learning of diffusion loss and reward models）**"的偏好对齐管线——这是 3.0 的方法，1.0 论文中**没有** RLHF/DPO/reward model 环节。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行与分布式策略 / 混合精度 / 吞吐**：论文**完全未披露**。
- **推理加速（步数 / 缓存 / 量化 / 蒸馏）**：1.0 论文未给出具体推理步数或加速方案；Fig.3 的绿色曲线提到通过**采样不同 CFG（classifier-free guidance）** 来画出编辑模型的"一致性-编辑强度"权衡曲线，说明推理时用 CFG 调节强度，但无量化工程数据。
- **部署形态**：1.0 为研究型技术报告，无开源权重/代码（无 GitHub / HF / ModelScope 仓库）；产品化形态在豆包 / 即梦（Dreamina）等字节产品中落地，后续迭代为 SeedEdit 1.6 / 3.0（3.0 主打"Fast and High-Quality"，强调推理速度，但属后续工作）。

## 评测 benchmark（把效果讲清楚）
**评测基准**：两个公开数据集——
- **HQ-Edit**（Hui et al. 2024）：293 张 DALL·E 3 生成图，是 SeedEdit 主打的应用场景（修订 T2I 生成图）。
- **Emu Edit**（Sheynin et al. 2024）：535 张真实 in-the-wild 输入图，主要是真实场景的局部编辑——与 SeedEdit 训练分布差异大，作者把它当作 **Out-of-Domain（OOD）** 测试。

**指标**：① CLIP 类——**CLIP Direction Score（CLIPdir，衡量指令服从）** + **CLIP image similarity（CLIPimg，衡量一致性/内容保留）**；② **LLM-as-evaluator**——用 **GPT** 替代 CLIP Direction Score 来判定编辑是否成功（GPT 分）。

**主结果（Table 1，↑ 越高越好）**：

| Model | HQ-Edit GPT↑ | HQ-Edit CLIPdir↑ | HQ-Edit CLIPimg↑ | Emu Edit GPT↑ | Emu Edit CLIPdir↑ | Emu Edit CLIPimg↑ |
|---|---|---|---|---|---|---|
| Prompt-to-Prompt | 26.93 | 0.0811 | 0.7462 | 12.69 | 0.0488 | 0.6568 |
| Instruct-Pix2Pix | 47.50 | 0.1224 | 0.8390 | 31.39 | 0.0726 | 0.8092 |
| MagicBrush | 47.51 | 0.1287 | 0.8008 | 44.25 | 0.0856 | 0.7930 |
| Emu Edit | N/A | N/A | N/A | 64.51 | 0.1094 | 0.8206 |
| UltraEdit | 54.17 | 0.1473 | 0.8281 | 46.95 | 0.0933 | 0.8072 |
| **SeedEdit (SDXL)** | **71.24** | **0.1656** | **0.8698** | 66.48 | 0.1162 | 0.8025 |
| **SeedEdit (in-house T2I)** | **78.54** | **0.1766** | 0.8524 | **75.03** | 0.1137 | 0.7875 |

关键结论：
- **HQ-Edit（主场景）全面领先**：in-house DiT 基座 GPT=78.54、CLIPdir=0.1766，均为全表最高；SDXL 基座的 CLIPimg=0.8698 也是最高，说明在编辑强度更高的同时**内容保留也更好**——印证了"重建 vs 再生成最优平衡"的核心主张。
- **Emu Edit（OOD）依然有竞争力**：SeedEdit(in-house) GPT=75.03 超过原版 Emu Edit（64.51），但作者坦言**所有方法（含自家）在 Emu Edit 上生成质量都不令人满意**，由此论证"先解决修订 T2I 图，再去做任意真实图编辑"是更合理的路线。
- **基座影响**：in-house DiT 基座在 GPT 成功分上明显优于 SDXL 基座，但 SDXL 基座在部分 CLIPimg 上更高，体现基座质量对编辑上限的影响。
- **与商用工具对比（Fig.7，定性 + 内部用户研究）**：与 DALL·E 3 Edit、Midjourney Web Editor 对比——DALL·E 3 / Midjourney 倾向于引入指令之外的非预期改动（Midjourney 更美观、DALL·E 3 更服从指令），SeedEdit 取得更好平衡、编辑更精确；**内部用户研究显示对 SeedEdit 结果有强偏好**（无公开 ELO/Arena 数字）。
- **消融**：论文未给出独立的消融表，但 Fig.3 用 CLIP 曲线证明"对齐后模型 > 朴素再生成"，并通过架构设计说明（复用 self-attention 比加输入通道在几何形变上更好、且新参数更少）。**FID / GenEval / T2I-CompBench / MJHQ / HPSv2 等 T2I 通用指标未报告**（本文聚焦编辑，非纯 T2I 生成）。

## 创新点与影响
**核心贡献**：
1. **任务再表述**：首次把指令图像编辑明确刻画为「重建 ↔ 再生成」连续轴上的最优平衡问题，并以"把 T2I 当作弱编辑器再对齐"的视角绕开配对数据稀缺难题。
2. **Causal diffusion with image input**：用共享参数双分支 + 因果自注意力复用 self-attention 注入图像条件（而非加输入通道），在几何形变任务上更强、新参数更少，且可与 T2I 数据混合训练。
3. **迭代对齐自举管线**：用当前模型生成→过滤→回灌微调的多轮闭环，把弱编辑器渐进对齐成强编辑器，在 HQ-Edit 上大幅领先开源 SOTA。

**影响**：
- 是 **ByteDance Seed 图像编辑系列的开端**，直接催生 SeedEdit **1.6** 与 **SeedEdit 3.0**（官方 2025-06-06 发布，主打 "Fast and High-Quality Generative Image Editing"）。3.0 在此基础上引入：**meta-info 范式 + meta-info embedding** 融合多源数据、**VLM（视觉语言模型）+ causal diffusion + connector** 的双层架构（VLM 抽高层语义、causal diffusion 复用扩散过程当 image encoder 抓细节）、以及 **diffusion loss 与 reward model 联合学习** 的偏好对齐；并以真实图基准对比 GPT-4o、Gemini 2.0，宣称取得最佳权衡。这条"用 reward / RL 强化编辑对齐 + VLM 接入"的路线正是 1.0"对齐视角"的自然延伸。
- 工程上落地于豆包 / 即梦等字节生图产品的编辑能力。

**已知局限**：
- 主场景受限于"修订 T2I 生成图"，对**真实 in-the-wild 图像的编辑质量仍不理想**（Emu Edit 上所有方法包括自家都不满意），作者本人将其列为后续要解决的难点。
- **闭源**：无开源权重/代码/HF/ModelScope；数据规模、训练超参、算力 infra 均未披露，复现性受限。
- 评测依赖 CLIP 与 GPT-as-judge + 内部用户研究，缺乏公开 Arena/ELO 与大规模标准化人评数字。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2411.06686
- arxiv_pdf: https://arxiv.org/pdf/2411.06686
- project_page (现为 SeedEdit 3.0，含 1.0→3.0 脉络): https://seed.bytedance.com/en/seededit （原 https://team.doubao.com/seededit 已重定向至此）

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2411.06686.pdf
- ../../../sources/omni/2024/seededit--project-page.md
