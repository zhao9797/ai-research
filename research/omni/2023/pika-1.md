---
title: "Pika 1.0"
org: "Pika Labs"
country: US
date: "2023-11"
type: blog
category: video
tags: [video, text-to-video, image-to-video, consumer-product, closed-source, generative-video]
url: "https://pika.art/blog"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://pika.art/"
downloaded: [pika-1--announcement-blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Pika 1.0 是 Pika Labs 2023 年 11 月 28 日发布的消费级"文本/图像/视频 → 视频"生成产品，核心卖点不是论文级技术指标，而是**易用的网页交互 + 多风格视频生成**（3D 动画、动漫、卡通、电影质感等）；发布即披露已有 50 万用户、每周数百万条生成视频，并完成 5500 万美元融资。它是 2023 年与 [[runway-gen1]]/Gen-2 并列的两大商业视频生成代表之一，定义了"AI 视频即消费产品"的产品形态。

## 背景与定位
2023 年视频生成的技术路线已由学术界铺好（[[align-your-latents-vldm]] 把 LDM 抬到视频、[[runway-gen1]] 做结构保真的视频到视频、[[emu-video]]/[[i2vgen-xl]] 做图到视频），但绝大多数仍停留在 demo 或 Discord bot 阶段。Pika 在 2023 年中（公司成立约在发布前 6 个月，即 ~2023 年 5 月）从一个 Discord 上的 `Pika Labs` 文生视频 bot 起步，迅速积累社区，到 11 月把它产品化为带网页界面的 **Pika 1.0**。

它要解决的问题，按官方表述是"高质量视频制作至今仍复杂且资源密集"——目标是让视频创作"毫不费力、人人可及"，让每个人都能成为"自己故事的导演"。因此 Pika 的差异化定位是**产品体验与可及性**（web 界面、低门槛、风格多样），而非公开可复现的技术领先。这与同期 Runway（更偏专业创作者工具链）形成对照。Pika 1.0 是该公司从"工具/bot"走向"消费级产品"的关键升级节点。

## 模型架构
**未披露。** Pika 1.0 是闭源商业产品，发布时只有一篇产品博客（《Announcing Pika》）和一支发布视频，没有技术报告、论文、model card、GitHub 或开源权重。官方原文只说 Pika 1.0 包含"a new AI model capable of generating and editing videos in diverse styles such as 3D animation, anime, cartoon and cinematic"，未公开：

- backbone（U-Net 还是 DiT / 是否时空注意力 / 是否级联超分）——未披露；
- 时序建模方式、是否潜空间扩散、VAE/tokenizer——未披露；
- text encoder（CLIP/T5/LLM）与条件注入方式——未披露；
- 参数量、输出分辨率/帧率/时长——未披露（同期 Pika 产品形态为短片段，约 3 秒、可延长，具体未在博客中给出确切数字，此处不臆测）。

可从公开信息合理框定的只有：它支持 **text-to-video、image-to-video、video-to-video** 三类输入，并以"风格化"（多种美术风格）为主打能力；这属于产品功能描述，不构成架构披露。学术血统上，公司的学术顾问包括 Stanford/Harvard 的 Chris Manning、Ron Fedkiw、Stefano Ermon、Alexander Rush（创始团队出自 Stanford AI Lab），但博客未将任何具体方法归因到某篇工作。

## 数据
**未披露。** 训练数据来源、规模、配比、清洗过滤、re-captioning、合成数据、美学/安全过滤等均无任何官方说明。博客仅披露**用户侧规模**（非训练数据）：发布时已有约 50 万用户、每周生成数百万条视频——这构成其自有的用户交互/反馈数据来源，但官方未说明是否用于模型训练。

## 训练方法
**未披露。** 训练目标（diffusion / flow matching / 其它）、多阶段流程（预训练→SFT→偏好对齐）、蒸馏与步数加速、关键超参与 trick 全部未公开。博客层面无任何训练细节，不做推测。

## Infra（训练 / 推理工程）
**未披露。** 算力规模、GPU·时、并行/分布式、混合精度、吞吐、推理加速（步数/缓存/量化/蒸馏）、部署架构等均无官方数据。可确证的工程/产品事实仅为：

- 部署形态：从 Discord bot（`Pika Labs`，beta 仍通过 Discord 提供）升级为**网页应用**（pika.art，发布时以候补名单 waitlist 形式逐步放量）；
- 服务规模佐证：每周数百万条视频的生成吞吐意味着相当规模的推理集群，但具体规模未披露；
- 公司当时为小团队，融资 5500 万美元（pre-seed/seed 由 Nat Friedman 与 Daniel Gross 领投，Series A 由 Lightspeed 领投），为算力/工程投入提供资金背景。

## 评测 benchmark（把效果讲清楚）
**未报告。** Pika 1.0 没有发布任何量化评测——无 FID、CLIPScore、VBench、人评 ELO/Arena 等公开数字，官方也未与同期 SOTA（[[runway-gen1]] Gen-2、Stable Video Diffusion、[[emu-video]] 等）做对照实验。其"效果"在发布时主要靠**发布视频 demo 与社区作品**呈现，属定性展示而非可比指标。

唯一可量化的"成绩"是**采用度/产品指标**，且来自官方一手博客：
- 发布时用户数：约 **50 万（half a million）**；
- 周生成量：**数百万条视频/周（millions of videos per week）**；
- 融资：**5500 万美元**（$55M）。

凡涉及画质/一致性/文本对齐等模型指标，一手源中**均无数据**，按要求记为"未报告"，不引用第三方非官方测评以免混入二手数字。

## 创新点与影响
**核心贡献（产品与生态层面，而非可复现方法）：**
- 把文/图→视频从"研究 demo / Discord bot"推成一个**有网页界面、面向大众的消费级产品**，显著降低 AI 视频创作门槛；
- 以**多风格生成 + 易用编辑**为卖点，强化了"AI 视频是创作工具而非玩具"的产品叙事；
- 与 [[runway-gen1]]/Gen-2 共同确立 2023 年商业 AI 视频生成的两强格局，并以小团队 + 顶级投资人/学界顾问阵容成为该赛道标志性创业公司。

**影响：** Pika 1.0 的发布（与 Runway Gen-2、Stable Video Diffusion 同期）共同把 2023 年底推成消费级 AI 视频的爆发起点，直接铺垫了 2024 年 OpenAI Sora 引爆全行业、以及 Pika 自身后续 Pika 1.5/2.x（Pikaffects、Scene Ingredients 等）的产品迭代节奏。

**已知局限：**
- 技术完全闭源、零量化披露，无法复现或客观对标；
- 发布时为短片段、需 waitlist，能力以风格化短视频为主，长时序一致性/物理合理性等当时业界共性短板未被官方量化讨论；
- 本页所有"模型/训练/数据/infra"维度因官方从未披露而留白——这是产品定位的必然结果，非资料缺失。

## 原始链接
- blog（官方发布公告，Announcing Pika / Pika 1.0，2023-11-28）: https://pika.art/blog
- product（产品主页 / waitlist）: https://pika.art/
- blog 存档（Wayback，2023-11-30 抓取）: http://web.archive.org/web/20231130190655/https://pika.art/blog

## 本地落盘文件
- ../../../sources/omni/2023/pika-1--announcement-blog.md
