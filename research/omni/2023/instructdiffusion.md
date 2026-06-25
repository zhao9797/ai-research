---
title: "InstructDiffusion: A Generalist Modeling Interface for Vision Tasks"
org: "Microsoft Research Asia"
country: China
reviewed: 2026-06-25
date: "2023-09"
type: paper
category: edit
tags: [instruction-editing, unified-vision, diffusion, segmentation, keypoint, generalist, instructpix2pix]
url: "https://arxiv.org/abs/2309.03895"
arxiv: "https://arxiv.org/abs/2309.03895"
pdf_url: "https://arxiv.org/pdf/2309.03895"
github_url: "https://github.com/cientgu/InstructDiffusion"
hf_url: ""
modelscope_url: ""
project_url: "https://gengzigang.github.io/instructdiffusion.github.io/"
downloaded: [arxiv-2309.03895.pdf, instructdiffusion--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
InstructDiffusion 把检测、分割、关键点估计、图像编辑、低层视觉（去模糊/去噪/去水印）等异质视觉任务统一为「按自然语言指令操作像素」的扩散生成过程——输出空间是灵活的、可人评的像素空间而非各任务专属的坐标/掩码/类别。它在以 Stable Diffusion v1.5 为底座、48 张 V100 训练 4 天的单一模型上，对**未见任务**（检测、分类、人脸对齐）和**未见数据集**（HumanArt、AP-10K 动物关键点、RefClef）展现出超越前代 generalist（Unified-IO、Painter）的泛化能力，是 InstructPix2Pix 之后「指令式像素操作」范式向「通用视觉接口」推进的关键一步。

## 背景与定位
NLP 用 GPT 一个框架统一了多任务，但视觉任务难以统一，原因有三：(1) 输出格式差异大（坐标、二值掩码、图像、类别）；(2) 方法论割裂（生成靠 GAN/DDPM，理解靠分类/检测专用头）；(3) 输入输出多为连续量，离散化（VQ-VAE）会引入量化误差。

此前的统一路线分两类：一类是序列化路线 [[pix2seq]]、Unified-IO，把所有输出离散成 token 序列，但把「semantic segmentation」「keypoint detection」当**任务指示符**而非真正指令，泛化靠记忆而非理解；另一类是 in-context/inpainting 路线（Painter、视觉提示 inpainting），靠样例图传递任务，难以精确反映人类意图、且对未见类别不知该用什么颜色。

InstructDiffusion 选择第三条路：直接继承 [[instructpix2pix]] 的「按指令编辑图像」范式，并把它从「语义编辑」泛化到**全部视觉任务**。核心洞察是：DDPM 的输入输出本就连续（无量化误差），而把分割写成「给最右边的狗盖一层半透明蓝色掩码」、把关键点写成「用红色圈出这个人的左肩」这类**高度详细的指令**，能让模型去「理解每个元素的语义」而非「记住整条指令的固定映射」——这正是其泛化到未见任务的根源。技术脉络上它站在 [[ddpm]] → [[latent-diffusion-ldm]]（Stable Diffusion）→ [[instructpix2pix]] 这条线之上，与同期 Painter、PromptDiffusion、Unified-IO 直接对标。

## 模型架构
- **Backbone**：直接复用 Stable Diffusion v1.5 的 **U-Net（latent diffusion）**，并非 DiT。VAE/text-encoder 也沿用 SD v1.5（VAE 把图像编码到 latent，文本编码器为 CLIP ViT-L/14）。
- **条件注入方式**：沿用 InstructPix2Pix 的做法——把**源图像 si**经 VAE 编码后的 latent 与噪声 latent **在通道维拼接**，因此扩大了 U-Net 第一层卷积的输入通道数；文本指令 ci 走原 cross-attention 注入。即一个网络同时吃「指令文本 + 源图 latent + 噪声 latent」，预测目标图 latent 的噪声。
- **统一输出表示**：模型只输出 **3 通道 RGB 图像**，作者据此把三类输出统一编码进 RGB：(1) RGB 图（编辑/增强直接就是图）；(2) 二值掩码 → 在目标物体上叠加**透明度 0.5 的半透明彩色掩码**（半透明而非不透明，既利于人评也实测提升分割精度）；(3) 关键点 → 在关键点位置画**指定颜色的小圆圈**。
- **后处理模块**：评测时需要标准格式（精确坐标/二值掩码），故训练一个**轻量 U-Net 后处理器**，把生成图反解为多通道 heatmap（关键点）或每物体二值掩码（分割），再算 AP / IoU。检测/分类则用「类似 referring segmentation 的提示」取被标记区域的上下左右边界得到 bbox。
- **分辨率策略**：训练用 256×256；发布的 checkpoint 与推理在 **512** 分辨率运行，单张 >9GB 显存的 GPU 即可推理（README）。
- **参数量**：论文/README 未单列总参数，按 SD v1.5 U-Net 约 8.6 亿参数量级（未在原文明确给出，故标注**未单独披露**）。

## 数据
作者明确表态这是 **proof-of-concept**：目的是验证「异质任务在像素统一表示下能否相互增益」，而非把数据规模推到极限。各任务采用公开数据集，按指令模板构造 ground-truth 目标图，并按数据量差异**手工设置采样权重**做平衡。各任务的「有效训练样本数」（Table 1）：关键点 245k / 分割 239k / 图像增强 46k / 图像编辑 425k。

各任务数据来源：
- **关键点检测**：COCO（149K 图、每图 17 点）、CrowdPose（35K、14 点）、MPII（22K、16 点）、AIC（378K、14 点）。每图随机选 1–5 个关键点、随机配色，目标图按颜色画小圆。
- **分割**：语义分割用 COCO-Stuff；指代分割用 gRefCOCO + RefCOCO。掩码透明度 0.5、随机配色。
- **图像增强**：去模糊用 GoPro（2103 图）+ REDS（24,000 图）；去噪用 SIDD（320 图）；去水印用 CLWD（60,000 图）。
- **图像编辑（7 个数据集）**：过滤后的 InstructPix2Pix（561K）、MagicBrush 训练集（8K）、GIER（5K）、GQA inpainting（131K）、VGPhraseCut（85K）、自建生成集（51K）、内部真实编辑场景集（23K triplets）。

**自建数据集 IEIW（Image Editing in the Wild，约 159,000 对）**，三条来源管线：
1. **物体移除**：借鉴 Inst-Inpaint，用指代分割集 PhraseCut 取区域做掩码，用 **LAMA** inpaint 抹掉物体得到 (有→无) 对；并**反向**交换输入输出、把「remove the blue bird」反写成「add a blue bird」补充「添加」数据。
2. **物体替换**：基于 SA-1B 与 OpenImages 的语义区域建一个图块 gallery；给定源图随机选一个语义区域作 query patch，检索近邻图块作参考，喂给 **PaintByExample** 生成替换后的目标图；再用 **BLIP2** 给源/目标图打 caption，交给 LLM 生成形如「请把奔跑的狗换成黑白条纹的猫」的指令。
3. **网络爬取**：在 Google 搜「photoshop request」，收集真实用户请求 + 资深 PS 师傅的成品，得 **23,000+** triplets，缩小训练-推理域差。

**指令多样性**：每个任务先**手写 10 条**指令，再用 **GPT-4 改写扩写**，训练时随机抽一条，显著增强多任务融合能力。

**质量过滤**（被作者称为「至关重要」）：用 **LAION-Aesthetics-Predictor** 算美学分、在 LAION-600M 上建 **KNN-GIQA** 模型算 GIQA 分，剔除两类：(i) 目标图质量分过低；(ii) 源图与目标图质量分差距过大。

## 训练方法
**三阶段 + 人类对齐**的流水线（Figure 2）：

1. **预训练适配（Pretraining adaptation）**：SD v1.5 原本只会生成自然图，但目标图可能含「分割掩码/关键点标记」这类非自然图。此阶段用现有分割/关键点数据集造出「带前景掩码」「带特殊标记」的图，并给原 caption 加后缀（如「with a few different color patches here and there」「surrounded with a red circle」），微调 SD 让其输出分布覆盖到期望域，同时保留原 T2I 能力。

2. **任务特定训练（Task-specific training）**：在所有任务数据上联合微调。按通道拼接源图（同上），优化标准 latent diffusion 目标：
   `L = E[‖ε − ε_θ(z_t, t, s_i, t_i)‖₂²]`，其中 `z = E(t_i)` 为目标图 latent，`z_t` 为加噪 latent。各数据库按手工采样权重平衡。

3. **人类对齐（Human alignment / instruction tuning）**：借鉴 LLM 的 instruction tuning，但做法不同——对 benchmark 每个样本用 **20 个不同 classifier-free guidance 采样**生成多个编辑结果，请人从中**选 0–2 张最佳**构成对齐数据集（全集仅 **1000 张图**），用它再微调约 **10 epochs**。实测把编辑的 CLIP-Sim 从 29.6 提升到 29.9，约 10 epoch 达峰（Figure 10）。

**关键超参**（4.1 + README）：SD v1.5 初始化；输入预处理到 256×256；学习率固定 1e-4；EMA rate 0.9999（人类对齐阶段降到 0.99 以便快速适应）；batch size **3072**；共 **200 epochs**。指令通过 CFG（推理 cfg-text 3.5 / cfg-image 1.25、50 步，README 推荐值）控制。论文未用 flow matching/蒸馏/RLHF/DPO；「人类对齐」是 SFT 式选优微调，非 reward model/PPO。

**两个核心消融**：
- **详细指令 vs 简单指示符**（Table 6）：把详细指令换成「semantic segmentation」「keypoint detection」式指示符 + 固定配色后，性能崩塌——关键点 COCO 71.2→22.7、HumanArt 51.4→7.0、AP-10K 15.9→5.2；语义分割 ADE-150 33.62→13.65、VOC 72.55→20.22。证明「让模型理解元素语义」是泛化关键。
- **多任务 vs 单任务**（Figure 8）：只在分割上训练 vs 联合训练，在 4 个未见集上联合训练全面更优（如 ADE-847 15.1→19.7、PC-459 24.4→28.3、ADE-150 29.7→33.6、RefClef 大幅提升）；且多任务还反哺编辑（联合训练能更准确判断该编辑哪个物体，受益于指代分割）。

## Infra（训练 / 推理工程）
- **训练算力**：**48 张 NVIDIA V100（每张 32GB）**，约 **4 天**完成 200 epochs，batch size 3072。README 给出多机训练命令（torch.distributed.launch、`--nproc_per_node=8`，示例 6 台机器即 48 卡），单机 8 卡也支持。开发环境 Python 3.8 / Ubuntu 18.04。
- **EMA / checkpoint**：EMA rate 0.9999；提供 `convert_ckpt.py` 从 `ckpt_epoch_200/state.pth` 导出最终 EMA 推理权重。开源两个 checkpoint：任务训练版与人类对齐版（`v1-5-pruned-emaonly-adaption-task[-humanalign].ckpt`），托管在 USTC 的 OneDrive（`mail.ustc.edu.cn`，故一作 Zigang Geng 实为 USTC↔MSRA 联合；论文 v1 署名栏仅列 Microsoft Research Asia）。
- **推理**：单张 **>9GB 显存** GPU 即可在 512 分辨率推理；默认 **50 步采样**（README 只给 `--steps 50`，未注明具体 sampler，继承自 InstructPix2Pix 的 k-diffusion 采样），cfg-text 3.5 / cfg-image 1.25。提供 Gradio web demo。
- **未披露**：未报告精确 GPU·时总量、并行策略细节（数据并行为主，未提 ZeRO/张量并行）、混合精度配置、吞吐数字，也无量化/步数蒸馏/缓存等推理加速（非该工作重点）。

## 评测 benchmark（把效果讲清楚）
所有数字来自已落盘的 arXiv PDF（2309.03895）。评测对手区分 specialized（专用模型）与 generalist（通用模型），InstructDiffusion 的核心卖点是 generalist 中最强 + 强未见泛化。

**关键点检测（AP，用 GT bbox，Table 2）**：

| 模型 | COCO val | HumanArt | AP-10K（动物，未见）|
|---|---|---|---|
| ViTPose（专用）| 82.0 | 64.1 | 14.7 |
| Unified-IO（generalist）| 25.0 | 15.7 | 7.6 |
| Painter（generalist）| 70.2 | 12.4 | 15.3 |
| **Ours** | **71.2** | **51.4** | **15.9** |

仅在人体关键点上训练，却在动物 AP-10K 与艺术风格 HumanArt 上大幅领先其他 generalist（HumanArt 51.4 vs Painter 12.4）；对专用模型在 COCO 上略逊（定位精度受限）。

**指代分割（cIoU，Table 3，节选）**：Ours 在 gRefCOCO val **67.36** vs Unified-IO 17.31；RefCOCO val 61.74 vs 46.42；RefClef（未见域）testA 54.73 / testB 54.82，全面大幅超 Unified-IO，部分接近/优于专用 LAVT、ReLA。

**语义分割（mcIoU，Table 4，节选）**：

| 模型 | ADE-847 | PC-459 | ADE-150 | PC-59 | VOC | COCO-Stuff |
|---|---|---|---|---|---|---|
| Painter（gen.）| 5.00 | 8.68 | 25.89 | 33.67 | 4.67 | 11.91 |
| PromptDiffusion（gen.）| 0.99 | 2.19 | 36.50 | 13.07 | 11.69 | 2.71 |
| Unified-IO（gen.）| 8.96 | 13.69 | 38.79 | 27.21 | 31.46 | 22.52 |
| **Ours** | **19.68** | **28.29** | 33.62 | **59.00** | **72.55** | **53.17** |

generalist 中除 ADE-150（Painter/PromptDiffusion 在该集专门训过）外全面领先；VOC 72.55 远超其他。作者指出 Painter/PromptDiffusion 靠样例图传色，对未见类别「不知道该用什么颜色」，而 InstructDiffusion 用文本指令直接指定颜色，故开集显著更优。

**图像编辑 + 低层视觉（Table 5）**：编辑用 CLIP-Sim / AP Score（自建 1000 样本 benchmark，分 replace/remove/add）；增强用 PSNR。
- 编辑：Ours Replace 30.19/4.90、Remove 28.88/4.65、Add 30.39/4.87——CLIP-Sim 优于 InstructPix2Pix、与 MagicBrush 持平；且**没有任何其他 generalist 能做编辑**。
- 低层视觉 PSNR：去模糊 23.58（VAE 上界 29.54）、去噪 38.66、去水印 34.26（VAE 上界 36.56）。作者明确指出增强性能**受 VAE 信息损失制约**，故在括号里给出「GT 经 VAE 重建」的上界作参照（这是诚实的局限标注）。

**未见任务泛化（4.9 / Figure 11）**：检测、分类、人脸对齐均未在训练中出现，靠「类指代分割」提示即可定位 bbox / 验证类别 / 圈人脸部位（甚至适用于动物脸）——这是其「一定程度 AGI 能力」的核心证据，但这部分主要是定性展示，未给系统化数字。

**未报告**：FID、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2/ImageReward/PickScore、人评 ELO/Arena、视频 VBench 等当代 T2I/编辑常用指标均未涉及（该工作年代较早且非纯 T2I，评测以各视觉任务的传统指标 AP/IoU/PSNR/CLIP-Sim 为主）。

## 创新点与影响
**核心贡献**：
1. **统一接口范式**：首次把理解类（分割、关键点）与生成类（编辑、增强）视觉任务**全部**统一为「按详细指令操作像素」的扩散过程，输出落在连续、可人评的像素空间，绕开了序列化路线的量化误差与「指示符=记忆」的泛化瓶颈。
2. **「详细指令 → 理解 → 泛化」假设**并用消融实证：详细自然语言指令（而非任务名指示符）是泛化到未见任务/数据集的关键，配 GPT-4 指令扩写。
3. **三类输出统一进 RGB**（半透明掩码 + 彩色圆点 + RGB 图）+ 轻量 U-Net 后处理反解标准格式。
4. **IEIW 数据集（约 159K）**与三条编辑数据构造管线（LAMA 移除 + 反向加回、PaintByExample 替换 + BLIP2/LLM 配指令、爬取真实 PS 请求），以及美学+GIQA 双重质量过滤。
5. **多任务联合训练增益**与**1000 样本人类对齐**的轻量有效性验证。

**影响**：作为 InstructPix2Pix 之后「指令式像素操作」走向「通用视觉接口」的代表作，启发了后续把视觉理解/生成统一进生成式框架的工作（如各类 unified vision generalist 与 instruction-based editing 模型）。其「半透明掩码做分割」「彩色圆点做关键点」的输出编码、以及「详细指令优于任务指示符」的结论被后续广泛参考。

**已知局限**（作者自陈 + 数据）：
- 对专用模型在 in-domain 上仍有差距（如关键点定位精度，COCO 71.2 vs ViTPose 82.0）。
- 低层视觉性能被 **VAE 重建上界**死死压住（去模糊 23.58 vs 上界 29.54），是 latent diffusion 范式的固有信息损失。
- proof-of-concept 定位，数据规模未推满；未用 flow matching/蒸馏/RLHF 等当代手段。
- 未见任务（检测/分类/人脸对齐）多为定性展示，缺系统化定量评测。
- 作者列出的未来方向：探索更优的统一输出编码、引入自监督/无监督以利用大规模无标注数据。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.03895
- arxiv_pdf: https://arxiv.org/pdf/2309.03895
- github: https://github.com/cientgu/InstructDiffusion
- project_page: https://gengzigang.github.io/instructdiffusion.github.io/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.03895.pdf
- ../../../sources/omni/2023/instructdiffusion--readme.md
