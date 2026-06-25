---
title: "Gemini 2.5 Flash Image（Nano Banana）"
org: "Google DeepMind"
country: US
date: "2025-08"
type: blog
category: edit
tags: [gemini, image-generation, image-editing, character-consistency, multi-image-fusion, conversational-editing, world-knowledge, synthid, closed-source, native-multimodal]
url: "https://blog.google/products-and-platforms/products/gemini/updated-image-editing-model/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://ai.google.dev/gemini-api/docs/image-generation"
downloaded: [gemini-2-5-flash-image-nano-banana--developers-blog.md, gemini-2-5-flash-image-nano-banana--blog-google.md, gemini-2-5-flash-image-nano-banana--model-page.md, gemini-2-5-flash-image-nano-banana--api-docs.md, gemini-2-5-flash-image-nano-banana--vertex-modelcard.md, gemini-2-5-flash-image-nano-banana--lmarena-image-edit.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Nano Banana（正式名 **Gemini 2.5 Flash Image**，模型代码 `gemini-2.5-flash-image`）是 Google DeepMind 2025-08-26 发布的**原生多模态图像生成/编辑模型**——把图像生成直接嵌进会"理解世界"的 Gemini LLM 里，主打**角色/对象一致性、多图融合、自然语言对话式局部编辑、世界知识驱动的编辑**，定价仅 **$0.039/图**（每图 1290 输出 token、$30/百万 token）。发布即登顶 LMArena 图像编辑竞技场（盲评 Elo）第一，成为 2025 年最现象级的闭源生成图像模型，并把"AI 图像编辑"推向大众消费级出圈。

## 背景与定位
解决的问题：早前的 [[gemini-2-0-flash-image]]（Gemini 2.0 Flash 原生图像，2025 年初）证明了"把图像生成做进 LLM"在**低延迟、低成本、易用**上的价值，但用户反馈**画质不够高、创意控制力不足**。Nano Banana 是同一谱系的画质与可控性升级：在保持 Flash 档"快、便宜、对话式"的前提下，补齐**一致性（character consistency）、多图融合、精确局部编辑、世界知识**四大短板。

技术脉络上它属于 **Gemini 原生多模态生成**一支（[[gemini-2-0-flash-image]] → **Gemini 2.5 Flash Image** → [[gemini-3-pro-image-nano-banana-pro]]）。与纯扩散文生图（[[imagen-4]]、[[flux-2]]、ByteDance Seedream 系、Qwen-Image 系）的根本区别在于：**图像生成与文本理解共享同一个 Gemini 多模态 backbone**，因此能直接复用 LLM 的世界知识与指令遵循能力——官方反复强调的卖点不是"画质参数"，而是"模型真的懂这张图里发生了什么"（能读懂手绘草图、按真实世界常识补全、一步完成复杂编辑指令）。在编辑赛道上，它与同期的 [[flux-1-kontext]]（BFL 的指令编辑模型）、ByteDance SeedEdit、Qwen-Image-Edit 直接竞争，并在盲评中大幅领先。

定位差异化：相对后来的 Pro 档 [[gemini-3-pro-image-nano-banana-pro]]，2.5 Flash Image 是**"快、便宜、好玩"的海量低延迟档**——官方明确建议高速量产/对话式编辑用本模型，最高质量专业产线才上 Pro 档。

## 模型架构
**重要前提：Nano Banana 是闭源产品模型，Google 未发布技术报告或论文，未披露 backbone 类型（DiT / 自回归 token / 掩码生成）、参数量、visual tokenizer / VAE、文本编码器等任何架构细节。** 以下为官方博客 + Gemini API model card 可确证的事实，工程内部细节如实标注"未披露"。

- **底座**：本模型是 **Gemini 2.5 Flash 多模态大模型的原生图像生成/编辑能力**的产品化封装。图像生成与文本/图像理解共享同一模型，这正是它能"用 Gemini 的世界知识来生成与编辑图像"的根因（官方："the model benefits from Gemini's world knowledge"）。其内部生成范式（扩散 / 自回归视觉 token / 二者混合）**官方未披露**。
- **I/O 与上下文**（来自 Gemini API model card）：模型代码 `gemini-2.5-flash-image`；**输入=图片+文本，输出=图片+文本**（原生交错多模态输出，一次响应里可同时返回文字解释与图片）；**输入 token 上限 65,536，输出 token 上限 32,768**；**知识截止 2025 年 6 月**；最后更新 2025 年 10 月（稳定版）。preview 版本 `gemini-2.5-flash-image-preview` 已弃用。
- **输出图像规格**：发布时每张图固定计为 **1290 输出 token**（发布博客确证的唯一硬数字）；官方发布材料**未直接给出**该 token 数对应的像素尺寸，业界普遍按 Gemini 后续文档的 "1K" 档（约 1MP / 1024px 级）反推，但这只是**推断、非官方报告值**。**注意：2K/4K 高分辨率、512(0.5K) 小分辨率、以及 1:4/4:1/1:8/8:1 等极端宽高比，均为后续 [[gemini-3-pro-image-nano-banana-pro]] / Gemini 3.1 Flash Image 才引入的能力（落盘的 api-docs 已明确将 2K/4K/512 与新宽高比归属于 Gemini 3.1 Flash Image），不属于本模型发布形态**——当前 Gemini API 文档已是 Gemini 3 时代的合并版，引用其 `imageSize=4K` 等参数时需注意不要误植到 2.5 Flash Image 头上。
- **能力矩阵**（model card）：支持 图片生成 / 上下文缓存（Caching）/ 结构化输出 / Batch API / Flex 推理 / Priority 推理；**不支持** 函数调用、代码执行、File Search、URL 上下文、Live API、搜索接地、Maps 接地、思考（Thinking）、音频生成。即本模型**没有** Pro 档的"思考/想法图片"机制，也**没有** Google 搜索实时接地——这两项都是后续 Gemini 3 Pro Image 才加入的。
- **四大原生能力**（官方博客明确列出）：
  1. **角色/对象一致性（character consistency）**：同一人物/宠物/产品在不同环境、姿态、年代、服装下保持"还是 ta 本人"的外观——官方强调消费者对"close but not quite"的人脸高度敏感，这是本次升级的核心攻坚点。
  2. **多图融合（multi-image fusion）**：理解并融合多张输入图，把一个对象放进新场景、用某图的配色/纹理重塑房间、把多张照片合成一张新场景。
  3. **自然语言局部编辑（prompt-based editing）**：模糊背景、去污渍、抠掉某个人、改姿态、黑白上色等精确局部变换，且保留其余部分不变。
  4. **世界知识驱动编辑（native world knowledge）**：读懂手绘示意图、按真实世界常识回答并编辑、一步完成复杂指令（demo 把画布变成交互式教学辅导）。
- **多轮对话式编辑（multi-turn）**：可在同一会话里连续编辑——空房间→刷墙→加书架→放家具，每一步只改指定部分、保留其余，本质是把 LLM 的多轮对话能力迁移到图像迭代。

## 数据
**未披露。** Google 未公开训练数据来源、规模、图文对数量、配比、清洗过滤、re-captioning、合成数据、美学/安全过滤的任何细节（闭源产品，无技术报告）。唯一可间接确证：模型继承 Gemini 2.5 Flash 的世界知识，**知识截止为 2025 年 6 月**；训练语料本身的构成、规模与处理流程一律记为"未报告"，不臆测。

## 训练方法
**未披露。** 训练目标（diffusion / flow matching / next-token / masked-token）、多阶段流程（预训练→continue→SFT→偏好对齐 RLHF/DPO/reward model）、蒸馏与步数加速等均未公开。可确证的仅有两类间接信息，但都**不等于**本模型自身的训练配方：
- 模型是 Gemini 2.5 Flash 的图像能力，理论上继承其后训练管线；Vertex AI 平台对 Gemini 系开放 SFT / 强化学习微调 / 偏好调优 / 蒸馏等**开发者侧调优能力**，但这是平台功能，不能反推 Nano Banana 内部用了哪些。
- 官方在发布时坦承的已知短板（见"局限"）暗示其优化重点：**长文本图内渲染、更可靠的角色一致性、事实性细节**仍在改进中——这三项恰是 Pro 档后续重点攻克的方向。
具体 RL / reward model / 偏好数据 / 一致性训练技巧一律记为"未报告"。

## Infra（训练 / 推理工程）
- **训练算力 / 并行 / 精度 / 吞吐：未披露。** 无任何 TPU/GPU 规模、分布式策略、训练时长数字。
- **定价与成本**（可确证，发布时口径）：**$30.00 / 百万输出 token**，每张图 **1290 token = $0.039/图**；输入与其它模态按 Gemini 2.5 Flash 标准计价。这是本模型最硬的差异化——把高质量图像编辑做到了约 4 美分一张的消费级单价。
- **推理与部署形态**：
  - 用量方案：支持 **Batch API、Flex 推理、Priority 推理**；上下文缓存（Caching）支持。
  - 部署面极广：**Gemini App**（消费端图像编辑，输出含可见水印 + SynthID）、**Google AI Studio**（含 "build mode" 一句话 vibe-code 出图像 App，官方放出 PastForward/Pixshop/Co-drawing/Home-canvas 等模板）、**Gemini API**、**Vertex AI**（企业版）。
  - **第三方分发**：发布首日即上线 **OpenRouter**（官方称这是 OpenRouter 480+ 模型中第一个能生成图像的）与 **fal.ai**，触达数百万开发者。
  - 推理步数 / 缓存 / 量化 / 蒸馏等加速细节未披露（闭源）。
- **水印 / 溯源**：所有生成或编辑的图像都强制嵌入**不可见 SynthID 数字水印**；Gemini App 端额外叠加**可见水印**，以标识 AI 生成/编辑来源。

## 评测 benchmark（把效果讲清楚）
**官方口径（定性，无可机读学术分数）**：Google 博客**未公布** FID、GenEval、DPG-Bench、T2I-CompBench、HPSv2、ImageReward、PickScore 等任何标准学术指标，仅以"state-of-the-art image generation and editing model""top-rated image editing model in the world"等定性表述 + 一张引用 LMArena 的柱状图（图片形式，无可抠取数字）作为依据。因此本节标准学术指标**一律记为"官方未报告"，不臆造**。官方主张的能力优势集中在前述四点（一致性 / 多图融合 / 局部编辑 / 世界知识）。

**第三方盲评基准（LMArena Image Edit Arena，盲评 Elo，用户在不知模型名下二选一投票）——本地落盘快照（2026-06 抓取）显示其当前长期表现**：
- **`gemini-2.5-flash-image-preview` (nano-banana)：Elo 1296±2，累计票数 10,854,084** —— 这是整个图像编辑竞技场中**得票数遥遥领先的第一名**（第二多的 Flux.1 Kontext Pro 约 642 万票、SeedEdit-3.0 约 495 万票，皆不及其六成），直接量化了它"现象级出圈"的真实使用规模。
- 截至快照时点（已是 2026 年中、众多新模型上线后）该模型在 49 个模型中排名第 18；**发布当时（2025-08）它是该榜单第一名的图像编辑模型**（官方博客与发布期 LMArena 均如此），后被自家 [[gemini-3-pro-image-nano-banana-pro]]（nano-banana-pro，1385–1388）、Gemini 3.1 Flash Image（nano-banana-2，1387）、以及 gpt-image-2 / Seedream-4.5 / Qwen-Image-Edit 等新一代陆续超越。
- 同框对照（同一快照）：上一代 `gemini-2.0-flash-preview-image-generation` 仅 1081±2（rank 47），印证 2.5 Flash Image 相对前代的巨大跃升（+215 Elo）；开源 BAGEL 1026、Step1X-Edit 998 垫底。

**消融 / 机制结论**：官方未提供可量化消融；定性上唯一明确的对比是相对 Gemini 2.0 Flash 原生图像的全面提升（画质 + 一致性 + 控制力），以及相对纯扩散编辑模型在"世界知识 / 复杂指令一步完成"上的优势。

## 创新点与影响
**核心贡献**：
1. **把高质量图像编辑做到消费级单价与延迟**（$0.039/图、Flash 档低延迟），并以原生多模态形态把"图像生成"嵌进会理解世界的 LLM，使**对话式、世界知识驱动的编辑**成为可能。
2. **角色/对象一致性的工程突破**：让"同一个人/宠物/产品跨场景保持本人外观"达到大众可用水平，直接催生了换装、换龄、合影、品牌资产批量生成等大量消费与商用玩法。
3. **多图融合 + 多轮对话式局部编辑**：把 LLM 的多轮 + 多输入能力迁移到图像迭代，重塑了"AI P 图"的交互范式。

**影响**：
- 发布即登顶 LMArena 图像编辑榜并在数月内积累**逾千万次盲评投票**，是该竞技场史上得票最多的模型，"Nano Banana"成为破圈级网红名，把 AI 图像编辑推向主流消费市场。
- 确立了 Google 在生成图像赛道的"原生多模态"路线优势，直接铺垫了 2025-11 的 Pro 档 [[gemini-3-pro-image-nano-banana-pro]]（继承"Nano Banana"品牌，加上思考 + 搜索接地 + 4K + 14 图融合 + 最强图内文字）。
- 推动行业把**一致性、世界知识、对话式编辑**列为图像模型的一等评测维度（而不仅是 FID/美学）。

**已知局限**（官方主动披露）：发布时**长文本图内渲染、角色一致性的稳定性、事实性细节（图中精细信息的正确性）**仍在改进中——这三项正是后续 Pro 档重点攻克的方向。此外本模型**无搜索接地、无思考机制、原生分辨率约 1MP（无 2K/4K）**，复杂排版与高保真专业产线场景受限。

## 原始链接
- blog（Gemini App 消费端发布，The Keyword）: https://blog.google/products-and-platforms/products/gemini/updated-image-editing-model/
- blog（开发者发布，Google Developers Blog）: https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/
- model card（Gemini API 模型页）: https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash-image
- docs（Gemini API 图像生成指南，Nano Banana）: https://ai.google.dev/gemini-api/docs/image-generation
- model card（Vertex AI / Gemini Enterprise Agent Platform）: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/2-5-flash-image
- benchmark（LMArena Image Edit Arena 盲评 Elo）: https://lmarena.ai/leaderboard/image-edit

## 本地落盘文件
- ../../../sources/omni/2025/gemini-2-5-flash-image-nano-banana--blog-google.md
- ../../../sources/omni/2025/gemini-2-5-flash-image-nano-banana--developers-blog.md
- ../../../sources/omni/2025/gemini-2-5-flash-image-nano-banana--model-page.md
- ../../../sources/omni/2025/gemini-2-5-flash-image-nano-banana--api-docs.md
- ../../../sources/omni/2025/gemini-2-5-flash-image-nano-banana--vertex-modelcard.md
- ../../../sources/omni/2025/gemini-2-5-flash-image-nano-banana--lmarena-image-edit.md
