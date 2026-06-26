---
title: "UltraEdit: Instruction-based Fine-Grained Image Editing at Scale"
org: "PKU / BIGAI / THU"
country: China
date: "2024-07"
type: paper
category: edit
tags: [image-editing, instruction-edit, dataset, region-based, diffusion, sdxl-turbo, prompt-to-prompt, neurips-2024]
url: "https://arxiv.org/abs/2407.05282"
arxiv: "https://arxiv.org/abs/2407.05282"
pdf_url: "https://arxiv.org/pdf/2407.05282"
github_url: "https://github.com/HaozheZhao/UltraEdit"
hf_url: "https://huggingface.co/datasets/BleachNick/UltraEdit"
modelscope_url: ""
project_url: "https://ultra-editing.github.io/"
downloaded: [arxiv-2407.05282.pdf, ultraedit--readme.md, ultraedit--hf-model-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
UltraEdit 是一个 ~410 万样本（757,879 条唯一指令、9+ 编辑类型）的**自动化构建的指令式图像编辑数据集**（NeurIPS 2024 D&B track），核心创新是用**真实图像作锚点（real image anchor）**抑制 T2I 生成偏置 + 引入**区域级（mask）编辑数据**，并用 **SDXL-Turbo + Prompt-to-Prompt** 把数据生产做到比 InstructPix2Pix 快约 100 倍。用它训练的标准扩散编辑模型在 MagicBrush 与 Emu Edit Test 上刷新记录——仅 ~450K 子集训练的 SD1.5 即超过用私有 1000 万数据训练的 Emu Edit。

## 背景与定位
指令式图像编辑（给一张源图 + 一句自然语言指令，输出编辑后图）的瓶颈在**数据**。本工作把矛头对准前序数据集（[[instructpix2pix]]、MagicBrush、HQ-Edit）三个痛点：

1. **指令多样性受限**：MagicBrush 靠人工标注（仅 ~10K，难规模化）；InstructPix2Pix 靠 GPT-3 生成指令（可规模化但被 LLM 能力上界框死，类型单一，仅 ~4 类编辑）。
2. **图像隐式偏置**：前作的源图/目标图**全部由 T2I 模型生成**，而 T2I 模型自带域偏置（例如偏卡通），训出来的编辑模型在自然场景上表现差，且数据分布失衡。
3. **缺区域级编辑**：现有数据集几乎只有 free-form（整图）编辑，缺少"在指定 mask 内编辑"的样本，而后者对精细编辑至关重要。

UltraEdit 用一条系统化自动流水线同时解决这三点，位置上是 **InstructPix2Pix 数据范式的"真实锚点 + 区域增强 + 极速生产"升级版**；技术栈承接 [[latent-diffusion-ldm]] / SDXL / SDXL-Turbo（ADD 蒸馏）/ Prompt-to-Prompt / SDEdit / GroundingDINO / SAM。它本身**不提出新模型架构**，而是"数据为中心"的工作——训练侧只用现成的 InstructPix2Pix 式扩散编辑器作为基线来验证数据质量。

## 模型架构
UltraEdit 的"架构"分两层：**数据生产流水线**（多个现成模型拼装）与**验证用的编辑基线模型**。

**数据生产流水线（无新网络，组合现成组件）**
- **指令生成**：LLM（论文未点名具体型号）+ 人工写的 in-context 示例。
- **图像生成 backbone**：**SDXL-Turbo**（SDXL 经 Adversarial Diffusion Distillation 蒸馏），只需 2-4 步即可达到接近 SDXL 的质量——这是流水线提速 ~100× 的关键。
- **编辑控制**：**Prompt-to-Prompt (P2P)** 交叉注意力控制，让源图/目标图共享同一初始噪声 `z_T`，保证编辑前后只改该改的部分。
- **源图锚定**：用 **SDEdit** 式 Img2Img——把真实锚点图 `I*` 加噪得到 `z_T`，再以源 caption 去噪，使生成的源图"像"真实图，从而把真实图的多样性注入进来。
- **区域标注**：Recognize-Anything（RAM）识别物体 → LLM 判定待编辑目标 → **GroundingDINO** 出 bbox → **SAM** 出细粒度 mask；bbox mask 与细 mask 融合成 **soft mask**，平滑修补区与非修补区的过渡。

**验证用的编辑基线模型（标准 InstructPix2Pix 范式）**
- backbone：**Stable Diffusion v1.5** 的 U-Net（latent diffusion）。论文为公平对比，沿用 InstructPix2Pix 的 U-Net 与训练数据量。
- **支持区域输入的改造**：给 U-Net **额外加 4 个输入通道**接收 region mask 的 latent。最终 U-Net 输入是 `[noisy latent z_T ; 源图 latent z_I ; region mask latent M_s]` 的通道拼接；新增的 8 个通道（源图 4 + mask 4）卷积权重随机初始化，其余从预训练 SD 初始化。free-form 编辑时喂入全白（blank）mask 表示整图编辑。
- 开源还放出了 **SDXL 版**与 **SD3 版**（`StableDiffusion3InstructPix2PixPipeline`，HF: `BleachNick/SD3_UltraEdit_w_mask`，见 README / HF 模型卡）；SD3 backbone 即 MMDiT（SD3 论文背景知识，本文正文未细述其架构）。人评中 SD3 版分数最高（见下）。

## 数据
**规模与构成**（Table 11）
- 总计 **4,108,262** 条指令编辑样本，**757,879** 条唯一指令，**9+ 编辑类型**。
- free-form（无 mask）：**4,000,083** 条（724,326 唯一指令）。
- region-based（带 mask）：**108,179** 条（33,553 唯一指令）——论文称这是**首个大规模区域级编辑数据集**。
- 是当时**公开最大**的指令编辑数据集（对比：InstructPix2Pix 313K、HQ-Edit 197K、MagicBrush 10K、EditBench 240）。

**真实图像锚点来源**（Table 7，过滤后约 **160 万**高质量图文对）：MS COCO（164K，人工）、Flickr30K（31,783，人工）、NoCaps（45K，人工）、VizWiz Caption（23,431，人工）、TextCaps（28,408，人工）、Localized Narratives（849K，人工）、ShareGPT4V（1,200K，GPT-4V caption）、LAION-LVIS（220K，GPT-4V caption）。过滤掉 caption 过长/过短的图。

**编辑类型（9 类）**：Add、Change Global、Change Local、Change Color、Transform Global、Transform Local、Replace、Turn、Others（含文字编辑、改数量等）。各类型占比 free-form 与 region-based 略有差异（如 Replace 在 free-form 占 17.09%、region 占 23.80%）。

**指令生成细节（Appendix A.2）**：先由人工就 COCO 图文写数百条种子指令 → LLM 扩展到 ~100K 在线 in-context 示例；每次采样 50 条指令 + 10 个编辑示例作 ICL，对每条真实图 caption 生成"原 caption; 编辑指令; 目标 caption"三元组，最终产出 **416 万条纯文本指令数据**。

**质量过滤（Section 2.3）**：每个样本跑 **100 次**扩散生成再筛优，用多指标过滤：源/目标图的 DINOv2 相似度、CLIP 图像相似度、SSIM（保证语义与像素一致性）；图-caption 的 CLIP 相似度（保证编辑落实到指令）；**CLIP Directional Similarity**（保证图像变化与 caption 变化一致）。数据集自评分（Table 3）：free-form CLIPimg 0.8427 / SSIM 0.6401 / DINOv2 0.7231；region-based 全面更好（SSIM 0.7413、DINOv2 0.7688），印证区域引导带来更好的内容保持。

**许可与责任**：论文附 Datasheet（Appendix）；锚点数据各自带原许可（CC BY 4.0 / Apache-2.0 / 自定义等），ShareGPT4V 为 CC BY-NC 4.0。

## 训练方法
**数据生产（生成式，非梯度训练）**
- free-form：源图 = SDEdit Img2Img（锚点加噪 `z_T` + 源 caption 去噪）；目标图 = 同一 `z_T` 上跑 P2P（目标 caption 控制），SDXL-Turbo 2-4 步。
- region-based：在 free-form 基础上加**改造的 inpainting 流水线**，交替执行常规扩散与"仅 mask 内修补"以避免边缘伪影，公式（latent 空间 mask `M`）：
  `z_{t-1} = (1-M)·z_T + M·D_M(z_t)`（当 `t mod 2 == 0`）；否则 `z_{t-1} = D_M(z_t)`。
  与 P2P + SDXL-Turbo 兼容，3-7 步出图。**soft mask** = GroundingDINO 的 bbox（粗掩码）与 SAM 细掩码（扩张成 contour）融合而成，用以平滑修补区与其余区域的过渡（论文未给出具体融合超参；并会过滤过大/过小/碎裂的掩码）。

**编辑模型训练（标准扩散微调，Appendix A.4）**
- 在 SD1.5 上用 Diffusers 微调，**沿用 InstructPix2Pix 全部超参**。
- 硬件：**8 × 80GB A100**，总 batch size **256**。
- 分辨率：**训练 256×256，生成 512×512**。
- 训练目标：标准的扩散去噪（InstructPix2Pix 范式，带 classifier-free guidance 的双重引导——image guidance + text guidance；推理示例 image_guidance_scale=1.5、guidance_scale=7.5、50 步）。
- region 版：混合 free-form + region-based 数据训练，新增通道随机初始化。
- **未使用** RLHF/DPO/reward model 等偏好对齐（这是 HIVE 的做法，本文作为 baseline 对比）；也无步数蒸馏/一致性蒸馏到编辑模型上（蒸馏只发生在数据生产侧的 SDXL-Turbo）。

## Infra（训练 / 推理工程）
- **训练算力**：8×A100-80GB，batch 256；论文未报告总 GPU·时与训练步数。
- **数据生产吞吐**：得益于 SDXL-Turbo（2-4 步）与实现优化，整条流水线比 InstructPix2Pix 式生产**快约 100×**；但每样本仍跑 100 次再筛优，故总生成量很大（4M 留存背后是更大规模的候选）。具体 GPU 规模/总耗时**未披露**。
- **推理形态**：开源 Diffusers pipeline（SD1.5 / SDXL / SD3 三套权重 + 改版 diffusers），HF 提供 Gradio Demo（`jeasinema/UltraEdit-SD3`）。推理示例 50 步、fp16。**量化/缓存/部署级工程未涉及**。

## 评测 benchmark（把效果讲清楚）
两大基准：**MagicBrush test**（与 GT 图比，指标 L1/L2/CLIP-I/DINO）与 **Emu Edit Test**（无 GT，与源图+目标 caption 比，指标 CLIPdir/CLIPout/L1/CLIPimg/DINO）。CLIP 用 ViT-B/32、DINO 用 dino_vits16，对所有方法重跑对齐。

**MagicBrush（Table 4，单轮 / 多轮，越低越好 L1/L2，越高越好 CLIP-I/DINO）**
- 单轮：UltraEdit「eval w/ region」L1=**0.0575**、L2=**0.0172**、CLIP-I=**0.9307**、DINO=**0.8982**；对比 IP2P（0.1141/0.0371/0.8512/0.7437）、IP2P w/ MagicBrush（0.0625/0.0203/0.9332/0.8987）。
- 多轮：UltraEdit「eval w/ region」L1=**0.0745**、L2=**0.0236**、CLIP-I=**0.9045**、DINO=**0.8505**，在更难的多轮设置上刷新记录。即使仅 ~450K 子集训练、且不输 region 也已显著超过 IP2P。
- 注：论文指出 MagicBrush benchmark 对其训练集有偏（IP2P w/ MagicBrush 在 MagicBrush 上虚高但在 Emu Edit 上崩盘——见下）。

**Emu Edit Test（Table 5，scaling 实验）**
- 基线：InstructPix2Pix(450K) CLIPdir 0.0784 / CLIPout 0.2742；MagicBrush(450+20K) CLIPdir 0.0658 / CLIPout 0.2763（CLIPdir 反而最低，印证过拟合）；**Emu Edit(私有 10M) CLIPdir 0.1066 / CLIPout 0.2843**。
- UltraEdit 随数据量从 450K→3M 单调提升编辑性指标：CLIPdir 0.0823→0.0862→0.0952→0.0960→0.0997→**0.1076**（3M），CLIPout 0.2778→…→**0.2832**。**3M 数据训练的 SD1.5 在 CLIPdir 上超过用私有 10M 训练的 Emu Edit（0.1076 vs 0.1066）**。
- 趋势解读：内容保持指标（L1/CLIPimg/DINO）随规模非单调——作者假设模型先学会"敢编辑"（硬编辑），到一定规模后才开始大改，故先升后降；UltraEdit 模型能在高 CLIPdir/CLIPout（编辑到位）的同时保持较低 L1（不乱改），说明是"带上下文地编辑"而非凭空造内容。

**消融（Emu Edit Test）**
- **真实图锚点（Table 6）**：带锚点在 450K/1M/1.5M 三档全面更优，且**只有用锚点时才显现 scaling 效应**（无锚点版扩规模反而不涨，因偏置更重）。例：1.5M 时带锚点 CLIPdir 0.0952 vs 无锚点 0.0720。
- **region-based 数据**：仅 ~100K 区域数据即可显著帮助 free-form 编辑；但要拿到峰值需保证足量区域数据 + 足量 free-form 数据（CLIPout 为主指标）。

**人评（TrueSkill，500 样本，3 选 1：First/Second/Tie）**
- MagicBrush（Table 13）：Ours w/ UltraEdit **25.5±0.8** > MagicBrush 23.7±0.7 > InstructPix2Pix 22.6±0.7。
- Emu Test（Table 14）：**SD3 w/ UltraEdit 26.7±0.7** > SDXL w/ UltraEdit 26.5±0.7 > SD1.5 w/ UltraEdit 26.0±0.7 > Emu Edit 25.1±0.7。三种 backbone 的 UltraEdit 模型均胜过 Emu Edit，且 backbone 越强分越高。

## 创新点与影响
**核心贡献**
1. **真实图像锚点（real image anchor）**：用 SDEdit 把真实图注入 T2I 生成，系统性抑制纯生成数据的域偏置——消融证明这是 scaling 能奏效的前提。
2. **大规模区域级（mask）编辑数据**：首个大规模 region-based 编辑数据集（108K），配套"改造 inpainting + soft mask"生产法与"U-Net 加 4 通道"训练改造，显著提升精细/局部编辑与多轮编辑。
3. **极速数据生产**：SDXL-Turbo（2-4 步）+ P2P 把生产提速 ~100×，使 4M 规模可行。
4. **数据为中心的结论**：仅用现成 IP2P 式 SD1.5 基线，靠数据质量+规模即在 MagicBrush/Emu Edit 上刷新记录，超过私有 10M 数据的 Emu Edit。

**影响**：成为开源指令编辑领域的标准大规模数据资源，后续大量编辑模型（含统一/Omni 编辑方向）将其纳入训练数据；其"真实锚点 + 区域掩码 + 蒸馏快产"三件套成为编辑数据合成的常用配方。SD3/SDXL/SD1.5 三套权重 + 改版 diffusers + Gradio Demo 全开源，落地门槛低。

**已知局限**
- 数据为合成（源/目标图仍由扩散模型生成，只是被真实图锚定），并非真实编辑对，仍可能继承 backbone 风格倾向。
- region 数据相对小（108K vs free-form 4M），论文将"扩充区域数据 + 自举训练"列为未来工作。
- 训练侧基线较弱（SD1.5、256 训练分辨率），未探索更强 backbone 的上限（虽人评显示 SD3 更优）。
- 训练总算力/GPU·时、数据生产端算力规模未披露；编辑模型未做偏好对齐/蒸馏加速。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2407.05282
- arxiv_pdf: https://arxiv.org/pdf/2407.05282
- github: https://github.com/HaozheZhao/UltraEdit （另镜像 github.com/pkunlp-icler/UltraEdit）
- project_page: https://ultra-editing.github.io/
- hf_dataset: https://huggingface.co/datasets/BleachNick/UltraEdit
- hf_model (SD3 w/ mask): https://huggingface.co/BleachNick/SD3_UltraEdit_w_mask
- hf_demo: https://huggingface.co/spaces/jeasinema/UltraEdit-SD3

## 一手源存档（sources/）
- [arxiv-2407.05282.pdf](https://arxiv.org/pdf/2407.05282) （论文 PDF，已精读正文+附录）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/ultraedit--readme.md) （GitHub README）
- [hf-model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/ultraedit--hf-model-card.md) （HF SD3 模型卡）
