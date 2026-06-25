---
title: "Midjourney V6 / V6.1"
org: Midjourney
country: US
date: "2023-12"
type: blog
category: t2i
tags: [t2i, diffusion, aesthetics, closed-source, text-rendering, midjourney]
url: "https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.midjourney.com"
downloaded: [midjourney-v6--docs-models.md, midjourney-v6--model-versions-wayback2024.md, midjourney-v6--v61-announcement-wayback.md, midjourney-v6--text-generation-doc.md, midjourney-v6--updates-index.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Midjourney V6（2023-12-20 发布）与 V6.1（2024-07-30 发布）是当年**美学标杆级闭源文生图模型**：相比 V5.2 显著提升了长 prompt 的指令遵循、画面连贯性（手/肢体/远景细节）、模型世界知识，并**首次支持用双引号在画面中渲染文字**；V6.1 在此基础上把连贯性与画质再推一档、出图速度提升约 25%。**无论文、无技术报告、无开源权重**，全部信息以官方文档与发布公告为准，几乎所有训练/架构/数据/infra 细节均**未披露**。

## 背景与定位
Midjourney 是一家自筹资金的小型研究实验室（David Holz 创立），产品长期以 Discord bot 形态分发，2024 年起迁移至网页端。其模型谱系 V1→V5.2→**V6（2023-12）→V6.1（2024-07）**→V7（2025-04）→V8/V8.1（2026），核心卖点始终是**默认美学（aesthetic）**而非可控性——历代模型自带一套"漂亮"的默认风格化，与同期 [[stable-diffusion-1]] / [[dall-e-3]] / [[sdxl]] 走"中性写实+强指令遵循"的路线形成差异化。

V6 解决的核心痛点是 V5.2 时代的两大短板：(1) **长 prompt 失效**——复杂多对象描述容易丢信息；(2) **无法画字**。官方文档原文将 V6 定位为"enhanced prompt accuracy for longer inputs, improved coherence and knowledge, and advanced image prompting and remixing capabilities"。在技术脉络上 V6 属于 [[latent-diffusion-ldm]] 范式的产品化迭代，与 [[sdxl]]、[[dall-e-3]]、[[ideogram]]（同期主打文字渲染）处于同一竞争位面，但 Midjourney 因不公开任何架构细节而无法归类到具体 backbone。

## 模型架构
**未披露。** Midjourney 从未发布 V6/V6.1 的论文、技术报告或模型卡，官方公告与文档中**不包含任何架构信息**——无 backbone 类型（U-Net / [[dit]] / [[mmdit]]）、无 VAE/tokenizer 规格、无 text encoder（T5/CLIP/LLM）、无参数量、无潜空间维度的任何官方陈述。

可从官方文档反推的**外部行为特征**（非架构本身）：
- **基于潜空间扩散**：V6 支持 `--style raw`（弱化默认美学，转向更"照片化/字面"的结果），支持 image prompt、remix、vary region、pan、zoom out、inpainting/outpainting，这些都是扩散式 latent 生成模型的典型可编辑能力。
- **文字渲染**：官方 Text Generation 文档明确"versions 6 and later"才支持在画面内渲染文字（用双引号 `" "` 包裹），且最佳实践是"标准拉丁字母、短词短语"——暗示其文本条件能力较 V5.2 显著增强（业界普遍推测与更强的文本编码器/重标注数据相关，但 Midjourney **未证实**）。
- **分辨率/长宽比**：V6 最大长宽比 14:1（docs Version 特性对比表）；具备 Subtle & Creative 两类 upscaler；V6.1 引入"新的 2x upscalers"（announcement 原文 "New 2x upscalers with much better image / texture quality"）。原生出图分辨率官方未明确给出数字（社区普遍认为 V6 默认约 1024 级别再经 upscale，本页不采信为官方口径），**官方未披露 V6/V6.1 原生分辨率**。
- **配套模型 Niji 6**：与 Spellbrush 合作的动漫向专用模型，与 V6 同期，定位 anime/插画美学——架构同样未公开。

## 数据
**几乎全部未披露。** 官方从未公布训练数据来源、规模、图文对数量、配比、清洗/过滤流程、re-captioning 策略或合成数据使用情况。

可确证的间接信息：
- Midjourney 的训练数据来源与版权问题在业界长期受争议（曾被艺术家集体诉讼），但**公司未在任何官方渠道披露数据组成**，本页不臆测具体来源。
- **社区驱动的偏好数据**：V6.1 公告明确该版本"has been guided by the priorities submitted and ranked by the community at midjourney.com/ideas"。Midjourney 还长期举办"ranking party"——在网页让用户对成对/单张图片做**审美二选一/打分**（updates 原文如 "click the one you find most beautiful on a personal level"、midjourney.com/rank-styles、rank-styles-individual），收集大规模美学偏好与风格标注。这被广泛视为其美学优势的数据飞轮，但**这些偏好数据具体如何进入 V6/V6.1 的训练（reward model / 偏好对齐 / 直接微调 / 仅用于 personalization 与 style 系统）官方从未说明**。
- **Personalization（个性化）数据**：V6.1 引入"a new personalization model with improved nuance, surprise, and accuracy"与个性化代码版本化（personalization code versioning），说明其有一套基于用户历史评分的个性化适配机制，技术细节未公开。

## 训练方法
**未披露。** 无任何关于训练目标（diffusion / flow matching / 其它）、训练阶段（预训练→SFT→偏好对齐）、蒸馏/加速方法、超参或 trick 的官方陈述。

仅能从行为层面推断的若干点（均非官方技术披露）：
- 极可能存在**基于人类审美偏好的对齐/调优环节**——海量 ranking-party 二选一排序数据是 Midjourney 区别于其它模型的标志性"默认美学"来源；但官方**从未确认**该数据是否用于（以及以何种方式用于）模型对齐，更未披露是 RLHF/DPO/reward model 中的哪一种，故"对齐环节"为合理推断而非官方陈述。
- V6.1 的 `--q 2`（quality）模式"takes 25% longer to (sometimes) add more texture at the cost of reduced image coherence"——说明 quality 参数在采样步数/计算量上做权衡，但底层是否涉及蒸馏/多步采样**未说明**。
- V6.1"roughly 25% faster for standard image jobs"——速度提升来源（架构精简 / 采样步数减少 / 推理优化 / 蒸馏）**未披露**。

## Infra（训练 / 推理工程）
**未披露。** 无训练算力规模、GPU 卡数/卡时、并行策略、精度、吞吐的任何官方数据；无推理侧步数/缓存/量化/蒸馏细节。

可确证的**部署形态与计费**信息：
- 部署为**托管 SaaS**：Discord bot + 网页端（2024 年逐步迁移到 midjourney.com 网页），无本地权重、无 API（官方长期不提供公开 API）。
- 推理计费以 **GPU 时间**计：分 Relax / Fast / Turbo 三档；标准 job 与 HD/quality 模式的 GPU 成本不同（文档中对后续版本给出过具体分钟数，但 V6/V6.1 时代的精确单位未在所抓取文档中列出）。
- V6.1 相比 V6 标准 job **快约 25%**（官方公告明确数字）。
- V6.1 的 inpainting/outpainting **没有同步更新**：使用 zoom/reframe/repaint/vary region 时会**回退到 V6.0 模型**（官方公告明确）。

## 评测 benchmark（把效果讲清楚）
**官方未报告任何定量 benchmark。** Midjourney 不发布 FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward / PickScore 等任何标准指标，也未公布人评 ELO/Arena 数字。本页严格不编造任何分数。

官方公告中**唯一的定量陈述**来自 V6.1（相对 V6 的自评，非第三方 benchmark）：
- **出图速度**：standard image jobs **快约 25%**。
- **新增 2x upscaler**：画质/纹理质量"much better"（定性）。
- **`--q 2` 模式**：耗时增加 **25%**，有时增加纹理但降低连贯性（定性权衡）。

官方对 V6 / V6.1 改进的**定性**描述（来自公告与文档原文）：
- **V6（vs V5.2）**：长 prompt 指令遵循更准；coherence 与世界知识提升；image prompting 与 remix 能力增强；首次支持双引号画字（`--style raw` 可转向更写实/字面结果）。
- **V6.1（vs V6）**："More coherent images (arms, legs, hands, bodies, plants, animals)"；"Much better image quality (reduced pixel artifacts, enhanced textures, skin)"；"More precise, detailed, and correct small image features (eyes, small faces, far away hands)"；"Improved text accuracy (when drawing words via quotations)"；整体"generally more beautiful"。

> 注：业界与第三方榜单（如社区 image-arena、设计师主观评测）在 2024 年普遍把 V6/V6.1 列为**美学质感最强的 T2I 之一**，但这些**不是 Midjourney 官方一手数据**，故不在本页给出具体名次/分数。

## 创新点与影响
**核心贡献：**
1. **美学标杆 + 偏好数据飞轮**：V6/V6.1 把"默认就很好看"做到行业天花板，背后是 Midjourney 独有的、规模化的**用户二选一审美排序数据 + personalization** 闭环——这套"以人类审美偏好驱动模型迭代"的产品化方法论，比同期开源模型的"中性写实"路线更早验证了偏好对齐在生成模型上的商业价值。
2. **文字渲染产品化**：V6 是较早把"画面内文字渲染（双引号语法）"落到消费级产品的 T2I 之一，与同期 [[ideogram]]、[[dall-e-3]] 共同推动了 2023–2024 年文生图"会写字"的浪潮。
3. **强可编辑工作流**：image prompt / remix / vary region / pan / zoom out / `--style raw` 构成一套成熟的迭代式创作工作流，影响了后续产品对"生成即编辑"的设计预期。
4. **V6.1 的连贯性专项优化**：把手/肢体/远景小特征（眼睛、远处的手）作为明确优化目标，回应了扩散模型长期的"手画不好"痛点。

**已知局限：**
- **完全闭源不可复现**：无论文/权重/API/数据披露，学术界无法在其上做研究或对照实验；本调研对其 infra/数据/训练/架构四个维度只能标"未披露"。
- **可控性弱于写实派**：强默认美学是双刃剑——想要"中性/可控"结果需依赖 `--style raw`、降低 stylize 等手段。
- **文字渲染受限**：官方明确仅对标准拉丁字母、短词短语效果好。
- **V6.1 编辑能力割裂**：inpainting/outpainting 仍回退 V6.0。
- **数据版权争议**：训练数据来源不透明，长期处于法律与伦理争议中。

## 原始链接
- doc (Version 总览，含 V6/V6.1 发布与默认时间线、特性对比表): https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- doc (Text Generation，确认 V6 起支持双引号画字): https://docs.midjourney.com/hc/en-us/articles/32502277092109-Text-Generation
- blog (V6.1 官方发布公告，2024-07-30，完整 What's new 列表): https://updates.midjourney.com/version-6-1/ （经 Wayback 2024-08-05 快照获取）
- doc (Wayback 2024-03-03 model-versions，含 V6 官方描述与日期): http://web.archive.org/web/20240303211046/https://docs.midjourney.com/docs/model-versions
- blog (Updates 索引页): https://www.midjourney.com/updates
- product: https://www.midjourney.com

## 本地落盘文件
- ../../../sources/omni/2024/midjourney-v6--docs-models.md
- ../../../sources/omni/2024/midjourney-v6--model-versions-wayback2024.md
- ../../../sources/omni/2024/midjourney-v6--v61-announcement-wayback.md
- ../../../sources/omni/2024/midjourney-v6--text-generation-doc.md
- ../../../sources/omni/2024/midjourney-v6--updates-index.md
