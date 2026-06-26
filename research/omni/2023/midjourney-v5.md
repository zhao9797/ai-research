---
title: "Midjourney V5 / V5.1 / V5.2"
org: Midjourney
country: US
date: "2023-03"
type: blog
category: t2i
tags: [t2i, diffusion, closed-source, commercial, photorealism, outpainting, style-tuner, discord]
url: "https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.midjourney.com"
downloaded: [midjourney-v5--docs-version.md, midjourney-v5--docs-legacy-features.md, midjourney-v5--docs-zoom-out.md, midjourney-v5--wayback-2023-03-v5-launch.md, midjourney-v5--wayback-2023-06-model-versions.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Midjourney V5（2023-03-15 发布）及其迭代 V5.1（2023-05-04）/ V5.2（2023-06）是 Midjourney 这家小团队闭源商业文生图（t2i）产品的标志性一代——**把"AI 出图能不能像照片"这件事第一次大规模坐实**：相比 V4 大幅提升真实感、细节、手部与连贯性（coherency），原生输出 **1024×1024**、可上采到 **2048²/4096²**；V5.1 加默认美学与 `--style raw`、Style Tuner，V5.2 引入 **Zoom Out（外扩/outpainting）** 等编辑功能。**注意：Midjourney 从未发布任何论文、技术报告、模型权重或架构白皮书，也从未公开任何标准 benchmark 数字**——本页所有内容均来自官方文档/发布说明一手源，架构/数据/训练/infra/评测的工程细节绝大多数**未披露**，下文逐条标注。

> 取证说明：原 `docs.midjourney.com/docs/model-versions` 旧 URL 现已 404，V5.x 描述被搬到新帮助中心的 [Legacy Features](https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features) 与 [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version) 页；原始 2023-03 / 2023-06 发布期文案通过 Wayback Machine 快照取回并落盘。

## 背景与定位
2022 下半年 t2i 三强格局成型：[[dall-e-2]]（OpenAI）、[[stable-diffusion-1]]（Stability/CompVis 开源）、Midjourney。Midjourney 走的是**纯托管、Discord 机器人交互、订阅制**的闭源产品路线，靠"开箱即出好看图"的强默认美学迅速积累用户。

- **V4（2022-11，V5 的前置）**：官方文档明确称其是"*an entirely new codebase and brand-new AI architecture designed by Midjourney and trained on the new Midjourney AI supercluster*"（全新代码库 + 全新 AI 架构 + 自建超算训练）。这是 Midjourney 关于其底层系统**唯一一次接近"架构/基础设施"层面的官方表述**，但仍未点名具体范式。
- **V5（2023-03-15）的定位**：在 V4 已经"很会画"的基础上，把**照片级真实感（photorealism）、更高分辨率、更强自然语言理解、更好的手部/解剖**作为卖点。彼时社区对 AI 出图"五根手指画成七根""塑料感"的吐槽极多，V5 被广泛视为"AI 画手第一次基本能看"的转折点，significance 正在于此。
- 技术脉络上，Midjourney 与同期主流一样建立在**潜空间扩散文生图**（思路同 [[latent-diffusion-ldm]] / [[ddpm]] / [[stable-diffusion-1]]）的范式之上——但**这是业界共识/推测，Midjourney 官方从未确认 V5 是不是 latent diffusion、是不是 U-Net**。它的差异化护城河不在公开的算法创新，而在**自有训练数据 + 强默认美学调校（aesthetic tuning）+ 产品化（Discord/网页交互、Upscale、Zoom Out、Style Tuner、Remix）**。
- 同期可对比：[[stable-diffusion-2]]（开源、512/768）、[[dall-e-2]] 之后的 [[dall-e-3]]（2023 下半年、强 prompt 跟随）、[[adobe-firefly]]（2023-03、主打商业版权安全）。Midjourney V5 在"出图美学/真实感的主观观感"上长期被社区评为同期最强之一，但**缺乏任何官方量化对比**。

## 模型架构
**官方未披露任何架构细节。** 帮助文档对 V5/V5.1/V5.2 的描述全部是产品/效果层面的措辞，没有 backbone、tokenizer、text encoder、参数量等任何技术字段：

- **backbone**：未披露（U-Net / DiT / 自回归 / 掩码生成均未说明）。结合 2023 年初的技术水位与"扩散式 t2i"的业界惯例，外界普遍推测 V5.x 为**潜空间扩散 U-Net**（类 [[latent-diffusion-ldm]] / [[stable-diffusion-1]]），但**Midjourney 从未官方确认**，亦未排除自研定制结构。
- **visual tokenizer / VAE / VQ**：未披露。
- **text encoder（T5 / CLIP / LLM）**：未披露。V5 文档强调"excels at interpreting natural language prompts / 对自然语言提示理解更好"，但未说明用何种文本编码器。
- **参数量**：未披露。
- **分辨率策略（这是官方有明确数字的少数一项）**：V5.x 系列**原生生成 1024×1024 像素**；通过 `Upscale (2x)` / `Upscale (4x)` 工具放大到 **2048×2048 / 4096×4096**（来源：Legacy Features 页"Midjourney model versions 5.x produce 1024 x 1024 pixel images... Upscale (2x) or Upscale (4x)... 2048×2048... 4096×4096"）。相比 V4 的更低原生分辨率，这是 V5 "higher resolution / 2x 分辨率"说法的官方依据。
- **条件注入 / 美学调校**：未披露机制。但 V5.1 引入的 `--style raw` 参数被官方描述为"reduce Midjourney default aesthetic（削弱默认美学滤镜）"，间接说明 Midjourney 在模型层之上叠加了一层**默认审美偏置**（很可能是审美偏好数据上的微调/对齐，但**具体方法未披露**）。
- **Niji 系列**：V5 时代并行有 Niji 5（与 Spellbrush 合作的动漫向模型），有 `--style cute/scenic/original/expressive` 等子风格——属同代但独立的模型分支，方法同样未披露。

## 数据
**完全未披露。** Midjourney 从未公布训练数据来源、规模、配比、清洗/过滤、标注或 re-captioning 任何信息。

- 与 [[adobe-firefly]]（明示只用 Adobe Stock 授权图）不同，Midjourney **从未声明数据来源是否授权**；2023 年起 Midjourney 是多起艺术家集体诉讼（如 Andersen v. Stability/Midjourney/DeviantArt）的被告之一，原告主张其在未授权的网络图像上训练——但这属诉讼指控，**非官方披露**，本页不作为事实采信。
- 美学/安全过滤、合成数据、图文对数量：均未披露。
- 唯一可作为旁证的官方表述仍是 V4 文档那句"trained on the new Midjourney AI supercluster"——说明有自建训练集群，但训练**数据**本身只字未提。

## 训练方法
**完全未披露。** 训练目标（diffusion / flow matching / next-token）、多阶段流程（预训练→SFT→偏好对齐）、是否有 RLHF/DPO/reward model、蒸馏与加速（consistency/LCM/ADD/步数蒸馏）、关键超参——**Midjourney 一律未公开**。

- 可推断但未证实：V5→V5.1→V5.2 是同一基座的渐进迭代（V5.1"stronger default aesthetic"、V5.2"more detailed, sharper, better colors/contrast/compositions, 对 `--stylize` 全范围更敏感"），这些**效果层面的改进描述**暗示主要在**美学对齐/微调**与采样/上采管线上做了优化，而非每代都从零重训——但官方未说明每代是重训、续训还是仅微调。
- V5.2 的 Style Tuner（`/tune` 命令，Discord 功能）官方称是"developing Personalization, Moodboards, Style Explorer 的最早步骤之一"，本质是让用户在一组风格方向上投票生成个性化 `--style code`——属**个性化/可控生成**的产品功能，底层训练机制未披露。

## Infra（训练 / 推理工程）
**几乎完全未披露。** 仅有的官方碎片：

- **训练 infra**：V4 文档提到"the new Midjourney AI supercluster（Midjourney 自建 AI 超算集群）"，说明 V4/V5 时代由 Midjourney 自有算力训练——但**GPU 型号/数量/GPU·时/并行方式/混合精度/吞吐全部未披露**。
- **推理 / 部署形态**：V5.x 时代主要通过 **Discord 机器人**交付（后期迁移到网页 alpha.midjourney.com / midjourney.com）；GPU 速度分 Fast / Relax / Turbo 模式（按 GPU 分钟计费），但这是**计费/调度产品概念**，非底层推理工程披露。推理步数、缓存、量化、蒸馏等加速手段**均未披露**。
- 默认参数（Legacy Features 页，V5.x）：Aspect Ratio 默认 1:1（range any）、Chaos 0（0–100）、Quality 1（0.25/0.5/1）、Seed random、Stop 100（10–100）、Stylize 100（0–1000）。

## 评测 benchmark（把效果讲清楚）
**Midjourney 从未报告任何标准 benchmark 数字**——FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore、人评 ELO/Arena 等**一律未报告**。官方只有**定性效果描述**：

- **V5（2023-03-15，官方原文）**："the newest and most advanced model... very high Coherency, excels at interpreting natural language prompts, is higher resolution, and supports advanced features like repeating patterns with `--tile`"；后续文档补充 V5"produces more photographic generations **than the V5.1 model**（比 V5.1 更照片化——V5.1 用默认美学换取了部分写实度）... closely match the prompt but may require longer prompts（更贴提示但可能需要更长提示词）"。
- **V5.1（2023-05-04，官方原文）**："stronger default aesthetic（更强默认美学，简单提示也好用）... high coherency, excels at accurately interpreting natural language prompts, fewer unwanted artifacts and borders（更少伪影/黑边）, increased image sharpness（更锐）"，并支持 `--tile` 无缝平铺。
- **V5.2（2023-06，官方原文）**："more detailed, sharper results with better colors, contrast, and compositions（更细、更锐、配色/对比/构图更好）... slightly better understanding of prompts... more responsive to the full range of the `--stylize` parameter（对 stylize 全范围更敏感）"。
- **MJHQ-30K 这个 benchmark 反而是别人拿 Midjourney 当"标杆参照"**：后来 Playground/社区构建的 MJHQ-30K 数据集就是以 Midjourney 输出为高质量参照来评测其它模型——侧面印证 V5 时代 Midjourney 在主观图像质量上的标杆地位，但这**不是 Midjourney 官方发布的数字**。
- **消融**：无任何官方消融。`--style raw`（V5.1）vs 默认是官方给出的唯一"对照"，但只有示例图、无量化指标。

**结论：V5/V5.1/V5.2 在公开渠道没有任何可引用的量化评测；其"标杆"地位来自社区主观共识与第三方把它当参照，而非官方 benchmark。**

## 创新点与影响
**核心贡献（产品 + 观感层面，非公开算法创新）：**
1. **照片级真实感的拐点**：V5 被广泛视为 t2i 第一次"出图能逼真到难辨真假"、且**手部/解剖明显改善**的一代，把"AI 生成图能不能商用/能不能骗过眼睛"的讨论推到主流。
2. **更高原生分辨率 + 强上采管线**：1024² 原生 + 2x/4x 上采到 4096²，配合强默认美学，使"开箱即用、无需炼丹"成为差异化体验。
3. **产品化编辑闭环**：V5.2 的 **Zoom Out（外扩 outpainting，缩放值 1.0–2.0）**、Pan、Vary Region、Remix，加上 V5.1 的 **Style Tuner / `--style raw`**，把单纯 t2i 扩成可迭代编辑的创作工作流——这些后来演化为 V6+ 的 Personalization / Moodboards / Style Reference / Editor。

**影响：**
- 成为**闭源商业 t2i 的事实标杆**，长期作为第三方评测（如 MJHQ-30K）的高质量参照系，直接刺激 [[stable-diffusion-2]] 之后开源阵营（SDXL 等）和 [[dall-e-3]]、[[adobe-firefly]] 的竞争。
- 验证了"小团队 + 闭源 + 自有数据/美学调校 + 强产品交互"路线在 t2i 赛道的商业可行性。

**已知局限：**
- **零透明度**：无论文、无权重、无 benchmark、无架构/数据披露，学术与工程可复现性为零；本页大量维度只能写"未披露"。
- **数据来源争议**：陷入多起版权诉讼（指控未授权数据训练），与 Firefly 的"商业安全"定位形成鲜明对照——但具体训练数据 Midjourney 始终未公开。
- **提示控制偏弱**：V5 官方自承"may require longer prompts"，相比同期主打 prompt 跟随的 [[dall-e-3]]，早期 V5 在复杂构图/精确指令遵循上不如对手（后续 V6 才大幅改善长提示与文字渲染）。

## 原始链接
- blog/doc（现行 Version 页，含 V6+ 与版本时间线）: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- blog/doc（现行 Legacy Features 页，V5/V5.1/V5.2 官方描述 + 默认参数 + Style Tuner）: https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features
- doc（Zoom Out / 外扩，V5.2 引入的编辑功能）: https://docs.midjourney.com/hc/en-us/articles/32595476770957-Zoom-Out
- wayback（2023-03-24 快照，V5 原始发布文案 "released March 15th, 2023"）: https://web.archive.org/web/20230324093404/https://docs.midjourney.com/docs/model-versions
- wayback（2023-06-05 快照，V5.1 默认 + `--style raw` + V5 photographic 描述 + Niji 5）: https://web.archive.org/web/20230605075612/https://docs.midjourney.com/docs/model-versions
- product: https://www.midjourney.com

## 一手源存档（sources/）
- [docs-version.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/midjourney-v5--docs-version.md)
- [docs-legacy-features.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/midjourney-v5--docs-legacy-features.md)
- [docs-zoom-out.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/midjourney-v5--docs-zoom-out.md)
- [wayback-2023-03-v5-launch.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/midjourney-v5--wayback-2023-03-v5-launch.md)
- [wayback-2023-06-model-versions.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/midjourney-v5--wayback-2023-06-model-versions.md)
