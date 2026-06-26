---
title: "Playground v2 (1024px Aesthetic)"
org: "Playground (Playground AI)"
country: US
date: "2023-12"
type: model-card
category: t2i
tags: [t2i, diffusion, sdxl, latent-diffusion, aesthetic, open-weights, mjhq-30k]
url: "https://huggingface.co/playgroundai/playground-v2-1024px-aesthetic"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: "https://huggingface.co/playgroundai/playground-v2-1024px-aesthetic"
modelscope_url: ""
project_url: "https://playground.com"
downloaded: [playground-v2--hf-card.md, playground-v2--mjhq30k-dataset-card.md, playground-v2--official-blog.md, playground-v2.5--arxiv-2402.17245-html.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Playground v2 是 Playground 团队 2023 年 12 月开源的文生图模型：**架构完全沿用 [[sdxl]]（潜在扩散 U-Net + 双文本编码器），但从零重训以增强美学质量**。核心卖点是**人评偏好显著优于 SDXL——在 2600+ prompt、上千用户的盲测中被偏好的次数是 SDXL 的 2.5 倍**；同时在团队自建的 MJHQ-30K 美学基准上 FID 7.07，优于 SDXL-refiner 的 9.55。它本身没有架构创新，价值在于"用更好的数据 + 训练配方把同一架构推到更高美学水位"，并顺带开源了一个被后续工作广泛采用的美学基准 MJHQ-30K。

## 背景与定位
2023 年下半年开源文生图的 SOTA 是 [[sdxl]]（Stability AI），社区普遍反馈其出图"美学/质感"不及闭源的 Midjourney v5 / DALL·E 3。Playground（一家以在线 AI 作图产品起家的公司，CEO Suhail Doshi）选择不动架构、只改数据与训练配方，从零重训一个与 SDXL 同构的模型，专门把**美学偏好**这一指标拉满，并以"商用可开源（community license）"的方式发布，对标 SDXL 在社区的生态位。

在技术脉络上，它属于"SDXL 之上的美学再训练/对齐"一类工作，与同期 Meta 的 [[emu-quality-tuning]]（quality-tuning，用小批量高质量图做 SFT 提升美学）思路同源——都承认"预训练最大化 log-likelihood ≠ 最大化人类美学偏好"，需要后期对齐。其直接后继 **Playground v2.5**（2024-02，arXiv:2402.17245）进一步把噪声调度换成 EDM、平衡多宽高比桶、引入类 Emu 的人类偏好对齐，把对 SDXL 的偏好比从 2.5x 拉到 4.8x——v2.5 报告中明确披露了 v2 的若干技术细节（见下）。

技术祖先链：[[ddpm]] → [[latent-diffusion-ldm]] → [[sdxl]] →（重训）→ Playground v2。

## 模型架构
**与 SDXL 完全相同的潜在扩散模型（Latent Diffusion Model）**，HF model card 明确写"It follows the same architecture as Stable Diffusion XL"：

- **Backbone**：SDXL 式 U-Net（卷积 + 自/交叉注意力的 UNet，非 DiT）。Diffusers 中通过 `StableDiffusionXLPipeline` 加载，pipeline tag = StableDiffusionXLPipeline。
- **文本编码器（双塔，固定/预训练，不微调）**：OpenCLIP-ViT/G（OpenCLIP）+ CLIP-ViT/L（OpenAI CLIP）——card 与 v2.5 报告均如此表述；SDXL 实际用的是 ViT-bigG/14，二者指同一编码器，本页统一沿用 card 写法 "ViT/G"。两路文本特征拼接后做交叉注意力条件注入——与 SDXL 一致。
- **VAE / latent**：沿用 SDXL 的潜在空间（card 未单独披露是否换 VAE，按"same architecture"理解为 SDXL VAE）。
- **分辨率策略**：原生 1024×1024 输出。团队还公开了两个**中间分辨率基座 checkpoint**：playground-v2-256px-base、playground-v2-512px-base（用于研究像素基础模型的训练曲线）。
- **条件注入**：与 SDXL 一致的尺寸/裁剪条件（size/crop conditioning）+ 双 CLIP 文本条件（card 未对此做额外披露，按同构理解）。
- **推荐采样**：官方建议 `guidance_scale=3.0`（比 SDXL 常用的 7.0~8.0 低，配合美学训练后的模型）。

注意：v2 **未改架构**这一点由 v2.5 技术报告反向确认——v2.5 也"chose not to change the underlying model architecture"，即 v2、v2.5、SDXL 三者同构。参数量未在 card 中单列，按 SDXL base 同构约 ~2.6B（UNet ~2.6B；官方未明确报数，标注**未披露**）。

## 数据
**几乎完全未披露。** HF model card 与数据集卡都未给出训练数据的来源、规模、配比、清洗/过滤、re-captioning 等任何细节——只说"trained from scratch by the research team at Playground"。这是该工作最大的信息缺口（作为商业产品团队，训练数据被刻意保密）。

可确证的与数据相关的事实仅有：
- 中间基座 checkpoint 的存在说明经历了 256px → 512px → 1024px 的多分辨率训练流程（典型 LDM 渐进式做法），但每阶段数据量**未报告**。
- v2.5 报告回溯提到 v2 已在"最后阶段加 offset noise"训练（见训练方法），但未涉及数据本身。

> 数据来源 / 规模 / 配比 / 美学过滤 / 安全过滤：**均未披露**（一手源中无任何数字）。

许可与可商用：官方博客明确 "We're providing **open weights**... **Commercial use is permitted**"，HF 上以 `playground-v2-community` 许可发布——这是 v2 区别于纯研究权重的一点（与 SDXL 社区生态位对标）。

## 训练方法
**"从零训练"的 SDXL 同构模型，训练目标与 SDXL 一致（DDPM/ε-prediction 式扩散）。** 关键可确证细节（部分由后继 v2.5 报告反向披露）：

- **噪声调度 = DDPM（Ho et al. 2020）**，并在**训练最后阶段加 offset noise**（与 SDXL 同策略）。v2.5 报告原文："SDXL adopts the strategy of adding offset noise in the last stage of the training, **as does Playground v2**"，且明确 v2 用的是 DDPM noise schedule + offset noise。
  - 这也是 v2 相对 v2.5 的已知短板：DDPM 调度在最大离散噪声时 SNR 仍偏高，导致难生成纯黑/纯白背景、色彩对比偏"灰" —— v2.5 正是为修这个问题才换成 EDM（Zero-Terminal-SNR 效果），所以这一缺陷在 v2 上仍存在。
- **多阶段渐进式训练**：256px-base → 512px-base → 1024px-aesthetic（由公开的中间 checkpoint 推断）。各阶段步数/学习率/batch **未披露**。
- **美学增强**：card 强调最终 checkpoint 名为 "1024px-aesthetic"，但**具体如何做美学增强（是否有专门的美学 SFT / 偏好对齐）在 v2 一手源中未披露**。对照 v2.5 才明确引入了类 [[emu-quality-tuning]] 的"用户评分自动筛高质量数据 + 人在环 SFT 对齐"——**v2 阶段是否已有此对齐，一手源未明确，不臆测**。
- **蒸馏 / 步数加速**：无。v2 是常规多步扩散模型（未做 LCM/ADD/consistency 蒸馏）。

> 训练目标的精确形式（ε-pred / v-pred）、优化器、总训练算力、各阶段超参：card **均未报告**。

## Infra（训练 / 推理工程）
**几乎完全未披露。**
- 训练算力 / GPU 数 / GPU·时 / 并行策略 / 混合精度 / 吞吐：一手源中**无任何数字**。
- 推理：标准 SDXL 推理路径，支持 Diffusers（`DiffusionPipeline`，fp16/bf16，`add_watermarker=False`，建议 `guidance_scale=3.0`）、Automatic1111 / ComfyUI（提供 `playground-v2.fp16.safetensors` 单文件）、以及本地 App（Draw Things、DiffusionBee）。
- 部署形态：开源权重（HF）+ Playground.com 在线产品。无官方推理加速/量化披露。

## 评测 benchmark（把效果讲清楚）
所有数字均来自 HF model card 与 MJHQ-30K 数据集卡（一手源）：

**1) 人评偏好（User Study，核心结果）**
- 设置：2600+ prompt、上千用户参与的成对盲测；评测两个维度——(1) 美学偏好、(2) 图文对齐。prompt 集为 PartiPrompts（公开）+ "Internal 1K"（Playground 自建、覆盖多类别）。
- 结果：**Playground v2 被偏好的次数是 SDXL 的 2.5 倍（2.5×）**。v2.5 报告复述了同一数字并把研究设置讲细（每对图≥7个独立用户投票，≥2票差才算"赢"，1票差算平局）。

**2) MJHQ-30K（团队新提出的自动美学基准，整体 FID）**

| Model | Overall FID ↓ |
| --- | --- |
| SDXL-1-0-refiner | 9.55 |
| **playground-v2-1024px-aesthetic** | **7.07** |

- 基准构成：从 Midjourney 精选 10 类 × 3000 张 = 30K 高质量图（类别：animals, art, fashion, food, indoor, landscape, logo, people, plants, vehicles），用 aesthetic score + CLIP score 过滤保证画质与图文对齐。
- FID 全部在 1024×1024 计算，用 clean-fid 工具（生成图 vs 参考图）。
- 结论：v2 在整体 FID 及**全部 10 个类别**的 FID 上都优于 SDXL-refiner，**在 people 和 fashion 类别提升最显著**；且 FID 排名与人评偏好一致（说明 MJHQ-30K FID 与人类美学偏好相关）。

**3) 中间基座 checkpoint（MSCOCO14 评测集上的 FID / CLIP Score，仅供参考）**

| Model | FID ↓ | CLIP Score ↑ |
| --- | --- | --- |
| SDXL-1-0-refiner | 13.04 | 32.62 |
| playground-v2-256px-base | 9.83 | 31.90 |
| playground-v2-512px-base | 9.55 | 32.08 |

- card 注明：因 prompt list 不同，这里的 SDXL 数字可能与 SDXL 原论文报数有差异；发布中间 checkpoint 旨在促进"像素基础模型"研究。

> 未涉及的指标：GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward / PickScore / Arena ELO 等在 v2 一手源中**均未报告**（v2 的评测核心是自家人评 + MJHQ-30K FID）。

## 创新点与影响
**核心贡献**
1. **"同架构 + 更好训练配方 → 显著更高美学偏好"的有力实证**：证明在不改 SDXL 架构、不做架构创新的前提下，靠数据与训练配方就能把人评偏好做到 SDXL 的 2.5 倍，成为当时开源美学最强的 SDXL 同构模型。
2. **开源 MJHQ-30K 美学基准**：从 Midjourney 精选 10 类 × 3K 的高质量图、用 FID 衡量美学质量。该基准被后续大量文生图工作（含 PixArt 系列、PlaygroundAI 自家 v2.5 等）采用，成为"美学质量"的常用自动评测，是 v2 留下的最持久影响。
3. **开源中间训练 checkpoint（256px/512px base）+ 评测指标**，方便社区研究像素基础模型的训练动力学。

**影响**
- 发布后社区反响强烈，v2.5 报告披露 v2 在发布后"上个月 HuggingFace 下载量超过 135,000 次"，并被 Stable Cascade 等 SOTA 工作引用。
- 直接催生 **Playground v2.5**（2024-02）：保持同架构，换 EDM 噪声调度（修色彩对比/纯色背景）、平衡多宽高比桶、类 Emu 人类偏好对齐，把对 SDXL 偏好比拉到 4.8×，并新增 People-200 基准。

**已知局限**
- **架构无创新**，纯重训工作；所有提升来自数据/配方，而数据细节完全保密，可复现性差。
- **DDPM 噪声调度 + offset noise 的固有缺陷**：色彩对比偏灰、难生成纯黑/纯白背景与纯色背景主体——这正是 v2.5 要修的问题，说明 v2 在该维度仍有明显短板。
- **训练数据、算力、对齐方法等关键信息几乎全部未披露**（商业团队保密），本页多个维度只能标"未披露"。
- 评测以自家人评 + 自建基准为主，缺少 GenEval/DPG 等图文对齐组合泛化的标准基准结果。

## 原始链接
- hf (model card, 一手主源): https://huggingface.co/playgroundai/playground-v2-1024px-aesthetic
- hf (MJHQ-30K 数据集卡, 一手): https://huggingface.co/datasets/playgroundai/MJHQ-30K
- blog (官方原博客, 一手, 在线): https://blog.playgroundai.com/playground-v2/ （HTTP 200，发布于 2023-12-05，全文已抓取落盘；内容含 2.5x 偏好、PartiPrompts、MJHQ-30K 介绍、"open weights / commercial use permitted"、256px/512px 预训练权重发布、团队署名）。注意 worklist 中给的 https://playground.com/blog/playground-v2 现已 **404**，正确可用地址是 blog.playgroundai.com 这个。
- arxiv (后继 v2.5 技术报告，反向披露 v2 细节): https://arxiv.org/abs/2402.17245
- project: https://playground.com
- intermediate base models: https://huggingface.co/playgroundai/playground-v2-256px-base ; https://huggingface.co/playgroundai/playground-v2-512px-base

## 一手源存档（sources/）
- [hf-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/playground-v2--hf-card.md)
- [mjhq30k-dataset-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/playground-v2--mjhq30k-dataset-card.md)
- [official-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/playground-v2--official-blog.md)
- [playground-v2.5--arxiv-2402.17245-html.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/playground-v2.5--arxiv-2402.17245-html.md)
