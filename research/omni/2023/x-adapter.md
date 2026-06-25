---
title: "X-Adapter: Adding Universal Compatibility of Plugins for Upgraded Diffusion Model"
org: "Show Lab (NUS) / Tencent AI Lab / Fudan"
country: China
date: "2023-12"
type: paper
category: method
tags: [adapter, plugin-compatibility, controlnet, lora, sdxl, sd15, training-free-plugin, feature-remapping, diffusion]
url: "https://arxiv.org/abs/2312.02238"
arxiv: "https://arxiv.org/abs/2312.02238"
pdf_url: "https://arxiv.org/pdf/2312.02238"
github_url: "https://github.com/showlab/X-Adapter"
hf_url: "https://huggingface.co/Lingmin-Ran/X-Adapter"
modelscope_url: ""
project_url: "https://showlab.github.io/X-Adapter/"
downloaded: [arxiv-2312.02238.pdf, x-adapter--readme.md, x-adapter--project-page.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
X-Adapter 是一个"通用升级器"：训练**一个**版本到版本的适配网络，就能让在旧底模（SD1.5）上预训练好的插件（[[controlnet]]、[[lora]]、T2I-Adapter、InstructPix2Pix 等）**免重训**直接作用于升级后的底模（[[sdxl]] / SD2.1），并因升级模型更强而带来质量与文图对齐增益（数字均来自论文 Tab.1）：ControlNet 任务 CLIP-score 0.2426→0.2632、FID 33.09→30.95（与 SDEdit 基线 30.86 接近）；LoRA 任务 FID 32.46→29.88、CLIP-score 0.25→0.2640、风格相似度 0.83（>SDEdit 0.72）。

## 背景与定位
**问题**：扩散社区里下游插件（plug-and-play 模块）的迭代速度远快于底模发布——ControlNet、LoRA、T2I-Adapter、IP-Adapter、AnimateDiff 等极大扩展了 [[stable-diffusion]] 的能力。但每当更大的底模（如 SDXL）发布，**所有插件都要为新底模重训**，维护成本极高。以 ControlNet 家族为例，要恢复原有能力得重训十几个不同网络。

**三大技术难点**（作者总结）：
1. **连接器维度不匹配**——训练不同版本扩散模型时不会考虑插件兼容性，旧插件的原始连接点在新底模里可能因维度不同而不存在；
2. **插件作用位置各异**——ControlNet 作用于去噪 UNet 的 encoder、T2I-Adapter 作用于 decoder、LoRA 加在每个线性层之后，难以设计统一插件；
3. **隐空间不一致**——尽管多数模型基于 [[latent-diffusion-ldm]]，但每个模型的 latent space 不同（像素扩散与隐扩散之间差距更大）。

**定位**：作者把这定义为大生成模型时代的一个**新任务**——"为不同底模升级插件"。X-Adapter 与"逐个重训插件"（Fig.2b）形成对照：只训一个 X-Adapter（Fig.2a），即可服务所有固定的下游插件。思想上受 [[controlnet]] 启发（把 X-Adapter 当作升级模型的额外控制器），受 SDEdit 启发设计两阶段推理。属于参数高效迁移学习（PETL）谱系，与 TaCA（升级视觉基座的任务无关兼容适配器）目标相近。

## 模型架构
**整体**：X-Adapter 由两部分组成——(a) 一份**冻结的旧底模副本**（SD1.5）+ (b) 连接两个 decoder 的**可训练 mapping layers（映射层）**。被升级的目标底模（SDXL）也整体冻结。

- **冻结旧底模副本**：X-Adapter 内嵌一份完整的 SD1.5（被冻结），目的是**完整保留各插件的连接器**。因为旧插件本就是为 SD1.5 设计的，把它们插进这份冻结副本里就能"原样工作"，不需要任何改造——这是绕开"连接器维度不匹配 / 插件位置各异"两大难点的关键。
- **Mapping layers（映射网络）**：在旧底模 decoder 的每一层训练一个额外映射网络，把旧模型特征映射到升级模型对应中间特征的维度，作为**guidance（引导特征）**。每个 mapper 由 **3 个堆叠的 ResNet 块**构成，用于维度匹配与特征提取。
- **特征融合公式**：给定旧模型多尺度特征 F_base，guidance 特征 F_mapper = F_n(F_base)；升级模型第 n 个 decoder 层的特征更新为 **F_up^n = F_up^n + F_mapper^n**（即逐元素**相加**融合，n∈{1..N}）。融合方式经消融对比了三种——(1) addition `c=a+b`；(2) guidance fusion `c=b+λ(a−b)`（λ可调）；(3) SPADE 式 `c=γ(a)·norm(b)+β(a)`——结论是 **addition 对条件还原最好**。
- **映射层插入位置**：实现中映射层放在**旧底模 decoder 的最后三个 decoder block**。消融了"插 encoder / 插 decoder / 两者都插"，结论是 **decoder-only 引导能力最强**（因为不破坏 encoder 的特征空间，只在生成阶段做引导）。

**底模本身**：基于 [[latent-diffusion-ldm]]（VAE encoder 把 RGB 压到 latent，UNet 去噪）。base = SD1.5（512×512），upgraded = SDXL base（1024×1024）；作者也训了 SD2.1 版本验证泛化。X-Adapter 本身**不引入新的 text encoder / tokenizer**，沿用各底模自带组件。

## 数据
- **训练数据**：从 **LAION-high-resolution** 中选取 **300k 张图像**子集用于 X-Adapter 训练（plugin-free 的纯文生图训练，不涉及任何插件）。
- **分辨率处理**：同一张输入图分别 resize 到 **1024×1024（喂升级模型）** 与 **512×512（喂旧底模）**，两路 latent 由各自 VAE encoder 编码，天然对齐（来自同一张图）。
- **配比 / 清洗 / re-captioning / 合成数据 / 美学与安全过滤**：论文**未披露**额外的清洗、重描述、配比或安全过滤细节（仅说明用 LAION-high-resolution 的 300k 子集）。

## 训练方法
**训练目标**：标准的 latent diffusion 去噪 MSE，但在升级模型上以"plugin-free"方式训练 X-Adapter 的映射层。

- **双 latent 训练**：给定输入图 I，先用 base 与 upgraded 各自 autoencoder 编码到 z0 与 z̄0；随机采样时间步 t∈[0,T]，分别加噪得到两路噪声 latent zt、z̄t；训练目标（式 4）：
  `E ‖ε − ε_θ( z̄t, t, c_u, XAdapter(z̄t, t, c_b) )‖²`
  即用升级网络 ε_θ 去预测加进去的噪声 ε，X-Adapter 学到的是"旧 latent 空间 → 升级空间"的 **offset（偏移）**。
- **null-text 训练策略（核心 trick）**：训练时把**升级模型的文本提示 c_u 全部设为空串**。这样升级模型只提供"空提示下的平均特征空间"，而 X-Adapter 学习"给定旧底模特征下的偏移量"，从而最大化 X-Adapter 的引导作用。消融验证：用 100% / 50% / 0% null 概率训练三个模型，**降低训练时升级模型的能力（提高 null 比例）能最大化 X-Adapter 的引导效果**（Null=100% 最佳）。注意：推理时 c_u **不必**为空，训练后 X-Adapter 对任意 c_u 都工作良好。
- **冻结策略**：训练时冻结旧底模副本参数（保证旧插件可无缝插入）+ 冻结升级模型参数（保护其高质量特征空间，类似 ControlNet/T2I-Adapter 的条件控制做法），**只训映射层**。
- **两阶段推理策略（推理期，非训练）**：训练时两路 latent 来自同一张图天然对齐；但推理时两路若各自随机采样初始 latent 会失配、损害插件功能与画质。受 SDEdit 启发：给定总步数 T，**第一阶段**先随机采 X-Adapter 的初始 latent z_T 并带插件运行到 T0=αT；在 T0 处把 base latent 经 `z̄_{T0}=E_up(D_base(z_{T0}))`（base decoder 解码→upgraded encoder 重编码）转换为升级模型 latent，作为第二阶段两路的对齐初值。经验最优 **T0 = (4/5)·T**，即 base 模型先 warmup 跑 20% 步数，余下时间走 X-Adapter 引导。消融显示：即使不做两阶段对齐，X-Adapter 也能大致重建条件；加上两阶段进一步提升条件准确度。
- **关键超参**：base=SD1.5、upgraded=SDXL base；映射层放 base 最后 3 个 decoder block；输入图 1024（升级）/512（base）；**AdamW，lr=1e-5，batch size=8，训练 2 个 epoch**。

## Infra（训练 / 推理工程）
- **训练算力**：**4× NVIDIA A100**，训练 **2 个 epoch**（300k 图子集）。论文未报告总 GPU·时 / 吞吐 / 并行策略 / 混合精度细节。
- **推理 / 部署**：官方 GitHub（2024-02-17）**只释出 inference 代码**（未开源训练代码）。环境：python 3.10 + torch 1.13.1+cu116 + torchvision 0.14.1，推荐安装 xformers 降显存提效率。提供 ControlNet（canny/depth）、LoRA、ControlNet-tile 的推理 bash 脚本。检查点托管在 HF `Lingmin-Ran/X-Adapter`。社区有 kijai 的 **ComfyUI** 实现（ComfyUI-Diffusers-X-Adapter）。
- 量化 / 蒸馏 / 缓存等推理加速：论文与仓库**未涉及**（X-Adapter 是兼容性方法，不做步数蒸馏）。两阶段推理会带来 base+upgraded 两路前向，存在额外推理开销，论文未给出具体延迟数字。

## 评测 benchmark（把效果讲清楚）
**实验设置**：选 **ControlNet（canny/depth，代表语义/稠密-稀疏条件控制）** 与 **LoRA（AnimeOutline / MoXin，代表风格控制）** 两类代表性插件。ControlNet 用 **COCO 验证集 5,000 张**评测；LoRA 每个选 civitai 上 20 个 prompt、每 prompt 用随机种子生成 50 张。指标：**FID**（图像质量，相对原始 SDXL 生成分布）、**CLIP-score**（文图对齐）、**Condition Reconstruction score**（按 ControlNet 做法衡量条件保真）、**Style Similarity**（按 StyleAdapter 做法，衡量与 base 模型生成的风格相似度）。

**Tab.1 — 对比 base 模型与 SDEdit 基线（数字逐格核对论文 Tab.1 原表渲染，2026-06-25 审稿修正：原稿把 ControlNet / LoRA 两张子表的 FID 列对调了，此处已纠正）**：

ControlNet 任务（COCO val 5000 张，canny+depth）：
| 方法 | FID ↓ | CLIP-score ↑ | Cond. Recon. ↑ |
|---|---|---|---|
| SD 1.5 | 33.09 | 0.2426 | **0.33 ± 0.16** |
| SDEdit + SDXL | **30.86** | 0.2594 | 0.14 ± 0.10 |
| **X-Adapter + SDXL** | 30.95 | **0.2632** | 0.27 ± 0.13 |

LoRA 任务（AnimeOutline / MoXin，风格控制）：
| 方法 | FID ↓ | CLIP-score ↑ | Style-Sim ↑ |
|---|---|---|---|
| SD 1.5 | 32.46 | 0.25 | — |
| SDEdit + SDXL | 30.11 | 0.2584 | 0.72 |
| **X-Adapter + SDXL** | **29.88** | **0.2640** | **0.83** |

> **读表要点（与论文原表一致）**：
> - **ControlNet**：X-Adapter 的 FID（30.95）几乎与 SDEdit 基线（30.86）持平、且略逊于它，但比 SD1.5（33.09）明显更好；真正拉开差距的是**条件保真 Cond. Recon. 0.27 vs SDEdit 0.14**——SDEdit 把 t0 调高换画质，却几乎丢光条件控制（0.14，远低于 SD1.5 原生的 0.33），X-Adapter 在保留条件的同时拿到画质增益。CLIP-score 0.2632 为三者最高。
> - **LoRA**：X-Adapter FID 29.88 三者最低（最好），CLIP-score 0.2640 最高，且**风格相似度 Style-Sim 0.83 > SDEdit 0.72**。
> - **核心结论**：X-Adapter 在"画质"与"插件功能保留（条件保真 / 风格保真）"之间取得平衡；SDEdit 随 t0 升高虽提画质但会丢失语义/风格控制（Cond. Recon. 仅 0.14、Style-Sim 仅 0.72）。注意 FID 是相对原始 SDXL 生成分布算的，故"更接近 SDXL 分布"即更低。

**Tab.2 — 用户研究（AHR 平均人评排名，1=最差 5=最好，5 名用户）**：
- ControlNet：Result Quality —— SD1.5 3.23 / SDEdit 4.14 / **X-Adapter 4.46**；Condition Fidelity —— SD1.5 4.21 / SDEdit 2.46 / **X-Adapter 3.92**（X-Adapter 在画质上最好，条件保真显著高于 SDEdit）。
- LoRA：Result Quality —— SD1.5 2.93 / SDEdit 3.92 / **X-Adapter 4.38**；Style Fidelity —— SDEdit 3.45 / **X-Adapter 4.14**（X-Adapter 画质与风格保真双优）。

**关键消融结论**（Fig.4/5/7/8/9/10）：
- **两阶段 t0 / SDEdit 对照**：t0 越高画质越好但 SDEdit 会丢失语义+风格控制；**X-Adapter 即便在高 t0 也保持可控性**（视觉与定量均验证）。
- **映射层位置**：decoder-only > encoder-only / both（不破坏 encoder 特征空间）。
- **融合方式**：对比 addition / guidance fusion / SPADE 三种，论文结论是 **addition 对条件还原最有效**（未给 guidance fusion 与 SPADE 之间的优劣排序，仅图示对比）。
- **null-text 比例**：null=100% 引导能力最强。
- **两阶段推理**：去掉也能大致重建条件，加上进一步提升条件准确度。
- **prompt 设置鲁棒性**：即使 SDXL 提示与 X-Adapter 提示语义冲突，仍能保持整体布局与风格一致。

未在论文报告的指标：GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 编辑 benchmark（GEdit/MagicBrush）/ 视频 VBench / Arena-ELO —— 这些**未报告**（该工作聚焦插件兼容性，评测围绕 FID/CLIP/条件保真/风格相似/人评展开）。

## 创新点与影响
**核心贡献**：
1. **提出新任务**——大生成模型时代"为升级底模升级插件"的版本兼容问题。
2. **通用免训练框架**——"冻结旧底模副本（保连接器）+ decoder 间可训练映射层（做特征 remapping 引导冻结的升级模型）"，**只训一个 adapter** 即可服务 ControlNet / LoRA / T2I-Adapter / InstructPix2Pix(ControlNet 版) / ControlNet-Tile / 部分个性化模型等多类插件，且对升级模型质量有正向增益。
3. **两套关键策略**——训练期 **null-text 训练**（用双 latent + 空提示学偏移）+ 推理期 **两阶段 latent 对齐**（受 SDEdit 启发）。
4. **跨版本 Plugin Remix**——因同时保留 base 与 upgraded 两个模型的连接器，可让 **SD1.5 的 ControlNet 与 SDXL 的 LoRA 协同工作**，打通不同发展阶段的社区资源。

**影响**：作为"插件生态兼容"的代表性工作，X-Adapter 为"底模升级而插件不必全量重训"提供了一条工程可行路径，缓解了 SD1.5→SDXL 迁移期的生态断层；有社区 ComfyUI 集成（kijai）。

**已知局限**（作者声明）：对依赖 **text-encoder 注入概念**的个性化插件（如 [[ip-adapter]]）**身份保持不佳**——因为这类插件作用在 text-encoder 上、其概念并非直接注入升级模型，而只能作为 guidance 融合进去；概念定制能力留作 future work。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2312.02238
- arxiv_pdf: https://arxiv.org/pdf/2312.02238
- project_page: https://showlab.github.io/X-Adapter/
- github: https://github.com/showlab/X-Adapter
- hf_checkpoint: https://huggingface.co/Lingmin-Ran/X-Adapter

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2312.02238.pdf
- ../../../sources/omni/2023/x-adapter--readme.md
- ../../../sources/omni/2023/x-adapter--project-page.md
