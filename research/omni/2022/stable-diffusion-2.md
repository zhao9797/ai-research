---
title: "Stable Diffusion 2.0 / 2.1"
org: "Stability AI"
country: EU
date: "2022-11"
type: model-card
category: t2i
tags: [latent-diffusion, text-to-image, open-weights, ldm, unet, openclip, v-prediction, upscaler, depth2img, laion]
url: "https://stability.ai/news/stable-diffusion-v2-release"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/Stability-AI/stablediffusion"
hf_url: "https://huggingface.co/stabilityai/stable-diffusion-2-1"
modelscope_url: ""
project_url: "https://stability.ai/news/stable-diffusion-v2-release"
downloaded: [stable-diffusion-2--blog.md, stable-diffusion-2--github-readme.md, stable-diffusion-2--hf-2base-card-wayback.md, laion-5b--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Stable Diffusion 2.0/2.1 是 [[stable-diffusion-1]] 的"重训"迭代：U-Net 参数量与 LDM 框架基本不变（865M），但**把文本编码器从闭源的 OpenAI CLIP ViT-L/14 换成完全开源的 OpenCLIP ViT-H/14**、**原生支持 768×768 出图**（用 v-prediction 目标重训）、并随发布一次性放出 **4× latent 超分、depth2img（MiDaS 深度引导）、文本引导 inpainting** 三个配套扩散模型，把"开源全栈生图工具箱"补齐。SD 2.1 在 2.0 基础上用**更宽松的 NSFW 过滤**重新微调（官方 README 明确的唯一差异）；社区普遍认为这缓解了 2.0 出人像质量下滑的问题（此因果为社区观察，非官方明文）。

## 背景与定位
SD v1 引爆开源生图生态后，最大的"卡脖子"是文本编码器：v1 用的是 OpenAI 闭源 CLIP ViT-L/14，权重不可商业自由再训。SD 2 的核心动机之一就是**用 LAION 自训的全开源 OpenCLIP 替换掉它**，让整条链路（VAE + U-Net + text encoder + 数据）都可开源复现。

技术脉络上，SD 2 仍是 [[latent-diffusion-ldm]]（CVPR'22 LDM）的工程化版本：先用下采样因子 8 的 KL-VAE 把图像压到潜空间，再在潜空间里训扩散 U-Net，条件通过交叉注意力注入；扩散本身建立在 [[ddpm]] / [[classifier-free-guidance]] 之上。相对 v1 的改进集中在三处：(1) **更强且开源的文本编码器**；(2) **原生高分辨率 + v-prediction 训练目标**（来自 Salimans & Ho 的 Progressive Distillation, arXiv:2202.00512，在高分辨率下数值更稳）；(3) **附带超分/深度/inpainting 模型**，把 v1 时代要靠社区拼凑的能力官方化。

官方明确指出：SD 2 由 Robin Rombach（Stability，原 CompVis）与 Patrick Esser（Runway）领衔，延续 LMU Munich CompVis 实验室的 LDM 工作，Katherine Crowson（k-diffusion 作者）参与，LAION 提供数据与 OpenCLIP，DeepFloyd 团队负责筛选训练子集。

## 模型架构
**整体框架：latent diffusion**。下采样因子 8 的 KL-VAE 把 512×512 图像编码到 64×64×4 潜空间（768 模型则在更高分辨率潜空间上工作），扩散在潜空间进行，最后由 VAE 解码回像素。这一点与 v1 一致。

**U-Net 主干**：865M 参数（README 原文："a downsampling-factor 8 autoencoder with an 865M UNet and OpenCLIP ViT-H/14 text encoder"）。README 同时强调 **U-Net 参数量与 SD 1.5 相同**——架构没有放大，变化主要在条件与训练目标。

**文本编码器（最关键的变化）**：**OpenCLIP ViT-H/14**（由 LAION 的 Romain Beaumont 训练，见 LAION large-OpenCLIP 博客），替换 v1 的 OpenAI CLIP ViT-L/14。条件取自 **倒数第二层（penultimate）文本嵌入**（README："conditioned on the penultimate text embeddings of a CLIP ViT-H/14 text encoder"），通过交叉注意力注入 U-Net。ViT-H 文本表征维度更大、语义更强，是 2.0 相对 v1 出图质量提升的主要来源。

**两套主模型 / 训练目标**：
- **SD 2.0-base**：512×512，标准 **噪声预测（ε-prediction / noise-prediction）** 模型，是其他衍生模型的微调基座。
- **SD 2.0-v**：768×768，**v-prediction** 模型（预测速度量 v 而非噪声 ε，高分辨率下更稳定），由 SD 2.0-base **微调**而来。README 指出 v-model 经验上可以用更高的 guidance scale 采样。

**配套衍生模型（均随 2.0 发布）**：
- **x4 latent 超分扩散模型**（`stable-diffusion-x4-upscaler`）：文本引导的 4× 上采样潜扩散模型，128×128 → 512×512；与文生图串联可到 2048×2048 甚至更高。训练为 **1.25M 步、10M LAION 子集（图 >2048×2048）、512×512 crop**（2-base 卡）；额外接受 `noise_level` 输入，采样时对合成图建议用更高 `noise_level`（如 100）。
- **depth2img**（`stable-diffusion-2-depth`，从 2.0-base 微调 200k 步）：先用现成的 **MiDaS（dpt_hybrid）** 单目深度估计推断输入图深度，再把（相对）深度作为额外条件喂给扩散模型，做**结构保持**的 img2img / 形状条件合成；strength=1.0 时完全丢弃像素信息，只依赖文本 + 深度。机制上是给 **U-Net 加一条额外输入通道**承载深度图、该新增通道**零初始化**（2-base 卡）。
- **inpainting 模型**（`stable-diffusion-2-inpainting`，从 2.0-base 微调 200k 步）：文本引导局部重绘；采用 **LAMA 的 mask 生成策略**，把被遮掩图的 VAE latent 作额外条件，新增 U-Net 输入通道同样**零初始化**（2-base 卡）。
- （后续）**Stable unCLIP 2.1**（2023-03，基于 SD2.1-768 微调）：仿 [[dall-e-2]] 的 unCLIP 架构，以 CLIP 图像嵌入为条件做图像变体/混合，分 unCLIP-L / unCLIP-H 两版（分别条件于 CLIP ViT-L / ViT-H 图像嵌入）。

**SD 2.1**：与 2.0 **同架构同参数量**（README："based on the same number of parameters and architecture as 2.0"），在 2.0 基础上**继续微调**，README 明确的唯一区别是训练数据的 **NSFW 过滤更宽松**（社区认为这是为找回 2.0 退化的人物生成质量，但官方未明文如此归因）。同样分 2.1-v（768）与 2.1-base（512）两套。README 提示 2.1-v 的 vanilla attention 在 fp16 下可能数值不稳，需 `ATTN_PRECISION=fp16`。

水印：参考采样脚本对输出加 **invisible-watermark**，标记机器生成。许可证：代码 MIT，权重 CreativeML Open RAIL++-M。

## 数据
训练数据基于 **LAION-5B 的美学子集**（aesthetic subset），该子集由 Stability 的 DeepFloyd 团队从 LAION-5B 中筛出，再用 **LAION 的 NSFW 过滤器**进一步去除成人内容（官方博客原文）。HF 模型卡（Wayback 取回）给出**精确过滤阈值**：用 LAION-NSFW 分类器 **`punsafe=0.1`（保守阈值）** 去除显式色情内容、并要求 **aesthetic score ≥ 4.5**（improved-aesthetic-predictor）。各分辨率阶段细节见"训练方法"。

LAION-5B 本身（一手 LAION 博客）：**58.5 亿（5.85B）CLIP 过滤的图文对**，其中 23 亿（2.3B）为英文、22 亿为其他 100+ 语言、约 10 亿无法判定语言；从 500+ 亿 Common Crawl 候选中按 **CLIP 余弦相似度阈值**（英文 0.28，用 CLIP ViT-B/32；多语 0.26，用 mCLIP）过滤掉约 90% 得到。数据集附带 **punsafe（NSFW 概率，CLIP-based 检测器，>0.5 判为 unsafe）** 与 **pwatermark（水印概率，>0.8 判为有水印）** 标签——SD2 的"美学+安全"过滤正是基于这些标签做的。

**SD 2.0 vs 2.1 的数据差异**：README 唯一明确的差异是 2.1 在 2.0 基础上用**更宽松的 NSFW 过滤**重新微调（原文："fine-tuned on 2.0, on a less restrictive NSFW filtering of the LAION-5B dataset"）。一手源**只给出"过滤更宽松"这一定性表述**，没有披露 2.0/2.1 各自的 punsafe 具体阈值；"2.0 因过滤过严导致人像质量退化、2.1 借此找回人物生成能力"是社区广泛观察与合理推断（非一手），具体阈值标注为**未报告**。

精确的子集**样本量**（多少图）一手源未给（卡片只给训练步数与阈值，未给样本计数）；x4 超分用的是单独的 **10M LAION 子集（图像 >2048×2048）**（见训练方法）。注意 SD-2 系列 punsafe/aesthetic 阈值（2.0 卡）已确证为 `punsafe=0.1` / aesthetic ≥4.5；2.1 卡因 gated 未能直接核到其放宽后的具体阈值，**仅 README 定性"less restrictive"**。

## 训练方法
（以下步数/超参均来自 HF SD-2-base 模型卡 Training Procedure 段，Wayback 取回。）
- **目标函数**：base 模型用标准 **噪声预测（ε-pred）**；768 的 -v 模型用 **v-prediction / v-objective**（arXiv:2202.00512），高分辨率与高 guidance 下数值更稳。
- **多阶段流程（带精确步数）**：
  - ① **512-base-ema**（从头训）：先 **550k 步 @ 256×256**（LAION-5B 子集，NSFW `punsafe=0.1`、aesthetic ≥4.5），再 **850k 步 @ 512×512**（同数据集中分辨率 ≥512 的图）。
  - ② **768-v-ema**：从 512-base **resume**，先 **150k 步用 v-objective**，再 **resume 140k 步在 768×768 子集**上。
  - ③ **512-depth-ema**：从 512-base resume，**finetune 200k 步**；给 U-Net **加一条额外输入通道**喂 MiDaS(`dpt_hybrid`) 的相对深度，新增通道**零初始化**。
  - ④ **512-inpainting-ema**：从 512-base resume，**再训 200k 步**；采用 **LAMA 的 mask 生成策略**，把被遮掩图的 VAE latent 作为额外条件，新增通道同样**零初始化**。
  - ⑤ **x4-upscaling-ema**：**1.25M 步**，训练数据是 **10M LAION 子集（图 >2048×2048）**，在 **512×512 crop** 上训；额外接受 `noise_level` 输入。
  - ⑥ **SD 2.1** = 在 2.0 基础上用**更宽松 NSFW 过滤**的数据继续微调（2.1 卡 gated，步数未核到）。
- **训练超参（来自 2-base 卡）**：**Hardware 32×8 A100**；**Optimizer AdamW**；**Gradient Accumulations = 1**；**Batch = 32×8×2×4 = 2048**；**LR 前 10,000 步 warmup 到 1e-4 后恒定**。
- **EMA**：发布的推理 checkpoint 为 **EMA-only**（README 明确推理 config 设 `use_ema=False` 因为权重本身已是 EMA）。
- **采样器**：参考脚本默认 **DDIM**，50 步出 768×768。社区可换 [[dpm-solver]] / k-diffusion（PLMS 等）加速。

## Infra（训练 / 推理工程）
- **推理工程（README 实证）**：强烈建议装 **xformers memory-efficient attention**（U-Net 与 autoencoder 的自/交叉注意力自动走 memory-efficient kernel），在 A100 + CUDA 11.4 上测试通过。官方延续 v1 的目标——**让模型在单张 GPU 上可跑**，面向消费级可达性。
- 提供 **Intel IPEX + TorchScript** CPU 优化路径（channel-last、bf16），用于在 Intel CPU 上采样。
- 2.1-v 在 fp16 下 vanilla attention 可能数值不稳，需 `ATTN_PRECISION=fp16`。
- 代码库**重度复用 OpenAI guided-diffusion (ADM) codebase** 与 lucidrains 的 denoising-diffusion-pytorch。
- **训练算力规模**：2-base 卡给出 **Hardware 32×8 = 256 张 A100**、global batch 2048、AdamW；但**未直接给总 GPU·时 / 吞吐 / 并行策略**。卡片"Environmental Impact"段（A100 PCIe 40GB、20 万小时、AWS us-east、15000 kg CO2）**实为沿用 SD v1 的估算**（卡内标题明确写 "Stable Diffusion v1"），**不应当作 v2 的实测算力**——故 v2 自身的总 GPU·时仍标注为**未报告**。

## 评测 benchmark（把效果讲清楚）
官方未发布技术报告。HF 2-base 卡的 Evaluation Results 段确认：**评测在 COCO2017 验证集随机 10000 prompt、512×512、50 步 DDIM 下做**，但**明确"Not optimized for FID scores"，且只给出各 checkpoint 的相对改进 pareto 图（`model-variants.jpg`），未列任何具体 FID / CLIPScore 数值**——故无可引用的定量 benchmark 数字。

唯一定量性"评测"即上述**相对改进曲线**：在 8 个 classifier-free guidance scale（1.5/2.0/3.0/4.0/5.0/6.0/7.0/8.0）× 50 步 DDIM 下对比各 checkpoint 的相对提升（README 与 2-base 卡均引此图，本地快照未含图片内数值）。官方博客的主张为定性："OpenCLIP 文本编码器**大幅提升了生成图像质量**（相比 v1）"、"x4 upscaler 可把 128×128 提升到 512×512、配合文生图可达 2048×2048"。

社区普遍观察（非一手，仅作背景，不计入数字）：SD 2.0 在人像/常见 prompt 上口碑反而不如 1.5（NSFW 过滤过严 + prompt 习惯被打乱），2.1 部分修复——这也是 2.1 紧随 2.0 两周（11/24 → 12/7）发布的直接原因。

## 创新点与影响
- **全开源文本编码器**：用 OpenCLIP ViT-H/14 替换 OpenAI CLIP，让 SD 全栈（数据/VAE/U-Net/text encoder）可开源复现，是后续可商用开源生图（含 SDXL）的基础。
- **v-prediction + 原生 768**：把高分辨率扩散训练目标引入主流开源模型，为 SDXL 等更高分辨率工作铺路。
- **"开源工具箱"范式**：一次发布超分 + 深度引导 + inpainting 多个官方配套模型，把 v1 时代靠社区拼装的能力官方化、标准化。depth2img 用 MiDaS 深度做结构保持，是后来 ControlNet 系列结构控制思路的前身之一。
- **已知局限 / 争议**：① 2.0 因 NSFW 过滤过激导致人像/解剖结构质量退化，社区接受度一度不如 SD 1.5，迫使两周后发 2.1；② prompt 习惯相对 v1 改变（换了 text encoder），早期迁移成本高；③ 官方未发技术报告与定量 benchmark，复现/对比依赖模型卡与社区评测；④ 仍只是"重训迭代"，架构未升级，真正的架构跃迁要到 SDXL（双 text encoder + refiner）。

## 原始链接
- blog（官方发布，一手）: https://stability.ai/news/stable-diffusion-v2-release
- github（原仓库，现 404 已下线；本次经忠实 fork 取回原始 README）: https://github.com/Stability-AI/stablediffusion
- hf（SD 2.1，现 gated；raw 返回需登录，未能直接抓取）: https://huggingface.co/stabilityai/stable-diffusion-2-1
- hf（SD 2.0-base 模型卡，现 gated；经 Wayback 取回，见落盘）: http://web.archive.org/web/20240101233658/https://huggingface.co/stabilityai/stable-diffusion-2-base
- hf（SD 2.0，现 404）: https://huggingface.co/stabilityai/stable-diffusion-2
- hf（x4 upscaler）: https://huggingface.co/stabilityai/stable-diffusion-x4-upscaler
- hf（depth2img）: https://huggingface.co/stabilityai/stable-diffusion-2-depth
- hf（inpainting）: https://huggingface.co/stabilityai/stable-diffusion-2-inpainting
- 数据一手（LAION-5B 博客）: https://laion.ai/blog/laion-5b/
- v-prediction 出处（Progressive Distillation, Salimans & Ho）: https://arxiv.org/abs/2202.00512
- OpenCLIP（LAION 训练的开源 CLIP）: https://laion.ai/blog/large-openclip/

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/stable-diffusion-2--blog.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/stable-diffusion-2--github-readme.md)
- [hf-2base-card-wayback.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/stable-diffusion-2--hf-2base-card-wayback.md)
- [laion-5b--blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/laion-5b--blog.md)
