---
title: "Midjourney (公测 V1–V4)"
org: Midjourney
country: US
date: 2022-07
type: blog
category: t2i
tags: [t2i, closed-source, diffusion, discord, aesthetic, midjourney, niji, commercial]
url: https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: https://www.midjourney.com/
downloaded: [midjourney-v1-v4--home.md, midjourney-v1-v4--docs-version.md, midjourney-v1-v4--docs-legacy-features.md, midjourney-v1-v4--docs-model-versions-2023jan-wayback.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Midjourney 是 David Holz 创立的「社区众筹型独立研究实验室」（官网自述 "community-funded research lab of 60 people"、"lean, self-funded, distributed team"，即约 60 人、自筹资金）于 2022-07 在 Discord 上开放公测的闭源商业文生图产品；2022-11 发布的 **V4**「全新代码库与全新 AI 架构、在自建的 Midjourney AI 超算集群上训练」，凭借**开箱即用的强烈美学默认风格**与 Discord 多人公开生成的病毒式体验，把 AI 绘画从研究圈带向大众消费市场。**关键一手事实**：Midjourney 从未发表论文、技术报告、代码或权重，也从未公布任何架构 / 数据 / 训练 / benchmark 数字——以下技术细节绝大部分为**官方未披露**，本页严格区分「官方文档明示」与「未公开」。

## 背景与定位
- **时间线（官方文档明示）**：V1 默认期 2022-02→04（极度抽象、笔触感、低一致性）；V2 默认期 2022-04→07（有创意、色彩浓、笔触感、低一致性）；V3 默认期 2022-07→11（高创意构图、中等一致性）；`--test` / `--testp` 测试模型于 2022-08 引入；**V4 于 2022-11 发布**、默认期 2022-12-20→2023-03-30；Niji 4（首个 Niji，与 Spellbrush 合作的动漫模型）2022-12-20 上线。（以上日期均出自落盘的 Legacy Features 与 2023-01 存档 model-versions 两页。）
- **公测开放日期（外部公认，非落盘官方文档）**：Midjourney 于 **2022-07-12** 进入 open beta（Discord 服务器更早于 2022-03-14 上线）。此日期为业界/维基百科广泛记载的历史事实，但**不在本页四个落盘一手源中**（官方现行文档仅给出 V3「07/22–11/22」默认期，未直述「公测开放日」），故单列标注其外部来源属性。
- **要解决的问题**：让非技术用户**无需写复杂 prompt / 不调参**就能得到「好看」的图。与同期 [[stable-diffusion-1]]（开源、可控、需要 prompt 工程与负面词）和 [[dall-e-2]]（更写实、API 受限）相比，Midjourney 选择**牺牲可控性、强化默认审美**的产品路线。
- **技术脉络中的位置**：V1–V3 被官方与社区普遍认为画风「抽象、笔触、低一致性」，更接近早期 VQGAN+CLIP / 扩散探索期的观感；**V4 是质变拐点**——一致性（coherency）与对复杂多对象 prompt 的处理大幅提升，确立了 Midjourney「电影感 / 高细节 / 强氛围」的标志性美学，并直接催生了 2023 年 V5（转向更写实）的迭代。属于扩散文生图浪潮（[[ddpm]] [[latent-diffusion-ldm]] [[glide]] [[dall-e-2]] [[imagen]]）中的**闭源消费级代表**。

## 模型架构
**官方从未公布 V1–V4 的网络结构、参数量、tokenizer / VAE / text encoder 等任何细节。** 文档中唯一的架构性表述（来自 2022-11 V4 发布期、2023-01 存档的官方 model-versions 页，以及现行 Legacy Features 页，措辞一致）：

> "The Midjourney V4 model is an entirely new codebase and brand-new AI architecture designed by Midjourney and trained on the new Midjourney AI supercluster."

可从官方文档**确证**的工程/产品层事实：
- **分辨率与「网格→放大」范式**：V1–V3 初始网格 **256×256px**；V4 初始网格 **512×512px**；早期模型先生成 4 张低分辨率候选网格，再用 Upscaler 放大补细节（V4 默认放大到 1024×1024，Beta Upscale 到 2048×2048；V1–V3 Light/Beta Upscale 到 1024×1024、Max Upscale 到 1664×1664）。这是 V1–V4 的核心交互形态，而非端到端高分辨率直出。
- **V4 的三种风格「flavor」**：通过 `--style 4a / 4b / 4c` 切换风格化微调。发布初期默认是 `--style 4b`（2023-01 存档页明示 "`--v 4 --style 4b` is the current default"），后期文档把默认更新为 **4c**（支持到 1:2 / 2:1 宽高比；4a、4b 仅支持 1:1、2:3、3:2）。这说明 V4「同一模型 + 多种风格分支」的产品化设计，但**底层是否多模型 / LoRA / 不同 checkpoint，官方未说明**。
- **Niji（动漫向）**：与 [[spellbrush]]（Spellbrush）合作的独立模型分支，「对动漫风格、动漫审美有更多知识」，专长动态 / 动作镜头与角色构图；Niji 不支持 `--stylize`，最大宽高比 3:2 / 2:3。Niji 是**另训的独立模型**，非简单风格开关。
- **`--test` / `--testp` 测试模型（2022-08）**：`--test` 官方描述为「通用艺术模型、一致性好」，`--testp` 为「写实主义模型、一致性好」；两者可配合 `--creative` 得到更多变构图；不支持 multi-prompt / image-prompt，最大宽高比 3:2 / 2:3，且 prompt 前部词权重更高。这两个实验模型被广泛认为是 V4 能力（尤其写实与一致性）的前哨验证。
- **底层生成范式**：官方从未确认 V1–V4 是否为扩散模型。社区与第三方普遍推测为基于扩散 / latent diffusion 路线（与「初始网格 + 渐进放大」「`--stop` 可按百分比提前结束生成得到更柔和图像」等行为一致），但**这属于推测，非官方一手信息**，本页不作为事实。`--stop`（10–100，按完成百分比提前停止得到更软更少细节的图）是文档明示的、与迭代式去噪过程一致的参数。

## 数据
**官方完全未披露 V1–V4 的训练数据来源、规模、配比、清洗 / 过滤、标注或 re-captioning 流程。** 文档对 V4 的唯一相关表述是定性的能力描述——「比此前版本掌握更多关于生物、地点、物体等的知识，能更好地处理细节，能处理含多个角色 / 物体的复杂 prompt」——但**未给出任何训练集规模或来源**。Midjourney 一贯不公开数据细节（该公司后续因训练数据来源在版权诉讼中受到关注，但此为外部事件，非官方一手披露，本页不展开）。**数据维度：官方未披露。**

## 训练方法
**官方完全未披露训练目标、训练阶段（预训练 / 微调 / 偏好对齐）、损失函数、优化器、超参、蒸馏 / 加速等任何方法细节。** 可确证的仅有：
- V4 是「全新代码库 + 全新架构」，在自建超算集群上训练（见上）。
- 产品迭代采用**社区反馈驱动**：通过 `--test` / `--testp` 等测试模型在 Discord 上向社区放出、收集反馈再改进（官方文档明示「introduced ... as part of an effort to gather community feedback and improve upon new features」）。这是一种以**真实用户大规模在线评分 / 偏好信号**反哺模型审美调优的产品化训练闭环，但**具体如何把反馈用于训练（是否构成偏好对齐 / reward model）官方未说明**。
- 各版本默认参数（文档明示）：V4 默认 `--stylize 100`（范围 0–1000）、`--quality 1`、`--chaos 0`、`--stop 100`、`--seed random`；V3 的 `--stylize` 默认 2500、范围 625–60000（区间与默认值与 V4 截然不同，侧面反映 V3 与 V4 是不同代际的模型）；`--test/--testp` 的 `--stylize` 范围 1250–5000、默认 2500。
- **训练方法维度：除上述外，官方未披露。**

## Infra（训练 / 推理工程）
- **训练 infra（官方明示但无数字）**：V4 在「the new Midjourney AI supercluster」上训练——官方承认自建了 AI 超算集群，但**未公布 GPU 型号 / 数量 / GPU·时 / 并行策略 / 吞吐 / 训练时长**。
- **推理 / 部署形态（产品事实）**：V1–V4 时期完全以 **Discord 机器人**为交付形态——用户在公开频道用 `/imagine` 触发，每个 Job 生成 4 图网格，再点击 `U1–U4` 放大、`V1–V4` 变体。这种「公开频道 + 多人围观 + 网格选择」的形态本身是 Midjourney 增长飞轮的关键工程/产品决策，但**GPU 调度、推理步数、量化、缓存等工程细节官方未披露**。Fast / Relax GPU 计费模式存在（按 GPU 分钟计费）但属计费层信息，非推理优化披露。
- **Infra 维度：除「自建超算 + Discord 部署」外，官方未披露。**

## 评测 benchmark（把效果讲清楚）
**Midjourney 从未发布任何定量评测**——无 FID、CLIPScore、GenEval、HPSv2、ImageReward、PickScore、人评 ELO 等任何数字，官方文档全部为定性描述。**本维度无任何一手数字可引用（官方未报告）。**

官方文档可确证的**定性对比 / 演进结论**：
- **一致性（coherency）阶梯**（官方措辞）：V1「very abstract and painterly, low coherency」→ V2「creative, colorful, painterly, low coherency」→ V3「highly creative compositions, moderate coherency」→ **V4「very high coherency, excels with Image Prompts」**。即 V4 在「画面逻辑自洽 / 解剖与构图合理性」上是相对前三代的质变。
- V4 相对前代的能力提升（官方）：更广的世界知识（生物 / 地点 / 物体）、更准的小细节、可处理含多角色 / 多对象的复杂 prompt、支持 image prompting 与 multi-prompts。
- 风格分支定位（官方）：`--testp`「写实主义」、`--test`「通用艺术」、`--style 4a/4b/4c` 为 V4 的三档审美微调。
- **第三方 / 社区评测**（非官方、本页不作为一手数字）：业界普遍以「人评偏好 / 美学评分」口碑认为 V4 在「氛围感 / 出图即好看」上领先同期 SD 1.5 与部分情况下的 DALL·E 2，但这些**无官方数字背书**，仅作背景。

## 创新点与影响
**核心贡献（多为产品 / 体验层，而非可复现的技术）**：
1. **「美学默认值」范式**：把审美调优内置进模型默认行为，让小白用最简 prompt 就能出「好看」的图——重新定义了消费级 AItext-to-image 的成功标准（从「可控 / 写实」转向「开箱即美」）。
2. **Discord 公开生成的增长飞轮**：用聊天机器人 + 公共频道 + 4 图网格 + 多人围观，把生成过程社交化、可炫耀化，实现病毒式增长，几乎不靠传统营销；并以社区反馈直接驱动模型迭代。
3. **社区众筹 / 独立实验室模式**：官网自述「community-funded research lab of 60 people」「lean, self-funded」，靠订阅盈利、自筹资金的小团队却做出现象级产品，成为「小而美、利润优先」AI 公司的范本。
4. **V4 的美学拐点**：确立 Midjourney 标志性的「电影感、高细节、强氛围」风格，使其在 2022 年底成为 AI art 的代名词之一，并直接推动 2023 年 V5（转向写实可控）与后续 V6/V7/V8 的快速迭代。

**已知局限（部分官方、部分公认）**：
- **完全闭源 / 不可复现 / 不可自托管**：无论文、无代码、无权重、无 API（公测期仅 Discord），技术上对学术界几乎零贡献，无法做受控对比。
- **V1–V3 一致性差**（官方自述 low/moderate coherency），手部、文字、解剖结构常出错（V1–V4 时期文本渲染基本不可用）。
- **V4 早期可控性弱**：强默认审美意味着难以精确还原写实 / 特定构图，需到 V5 才补强 prompt 跟随与写实。
- **分辨率受限**：初始仅 256/512px，靠 upscaler 补，原生高分辨率直出能力弱。
- **数据 / 训练黑盒**：数据来源完全不透明，后续引发版权争议（外部事件）。

## 原始链接
- blog/product (官网，关于页): https://www.midjourney.com/
- docs (现行 Version 文档，含 V6+ 时间线): https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- docs (现行 Legacy Features 文档，V1–V4 全量时间线 / 分辨率 / 默认参数 / test 模型 / niji / upscaler——本页主源): https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features
- docs (2023-01-30 Wayback 存档的 V4 发布期 model-versions 原始页，含「全新代码库 / 超算」原话与 `--style 4a/4b` 默认): http://web.archive.org/web/20230130031205/https://docs.midjourney.com/docs/model-versions
- updates/blog (官方更新博客，Ghost；V4 原始公告未能获取): https://updates.midjourney.com/ —— 现行首页仅列 2026 年近期帖；Wayback 对该子域最早快照为 2024-03（API 查 20221115 返回 closest=20240328），无 2022 年存档。V4 的原始发布实为 2022-11 的 Discord 公告，无对应官方博客文章可落盘，故本页 V4 架构原话以「2023-01 存档 model-versions 页」为一手依据。

## 本地落盘文件
- ../../../sources/omni/2022/midjourney-v1-v4--home.md
- ../../../sources/omni/2022/midjourney-v1-v4--docs-version.md
- ../../../sources/omni/2022/midjourney-v1-v4--docs-legacy-features.md
- ../../../sources/omni/2022/midjourney-v1-v4--docs-model-versions-2023jan-wayback.md
