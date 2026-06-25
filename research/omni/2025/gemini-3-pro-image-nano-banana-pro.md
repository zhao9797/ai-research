---
title: "Gemini 3 Pro Image（Nano Banana Pro）"
org: "Google DeepMind"
country: US
date: "2025-11"
type: blog
category: edit
tags: [gemini, image-generation, image-editing, text-rendering, reasoning, search-grounding, multi-reference, 4k, synthid, closed-source, native-multimodal]
url: "https://blog.google/innovation-and-ai/products/nano-banana-pro/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://deepmind.google/models/gemini-image/pro/"
downloaded: [gemini-3-pro-image-nano-banana-pro--blog-google.md, gemini-3-pro-image-nano-banana-pro--developers-blog.md, gemini-3-pro-image-nano-banana-pro--enterprise-blog.md, gemini-3-pro-image-nano-banana-pro--image-gen-docs.md, gemini-3-pro-image-nano-banana-pro--api-modelcard.md, gemini-3-pro-image-nano-banana-pro--vertex-modelcard.md, gemini-3-pro-image-nano-banana-pro--artificialanalysis-t2i-arena.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Nano Banana Pro（正式名 **Gemini 3 Pro Image**，模型代码 `gemini-3-pro-image`）是 Google DeepMind 2025-11-20 发布的旗舰原生图像生成/编辑模型，**直接构建在 Gemini 3 Pro 多模态大模型之上**——首次把"思考（reasoning）+ Google 搜索实时接地 + 世界知识"系统性接入图像生成管线，主打**最强的图内文字渲染、可推理的信息图/构图、最多 14 张参考图融合、最高 4K 分辨率**。发布时为 Artificial Analysis 文生图竞技场（盲评 Elo）的头部模型；据官方称在文生图基准上"领先"，全部输出强制嵌入 SynthID 水印。

## 背景与定位
解决的问题：上一代 [[gemini-2-5-flash-image-nano-banana]]（"Nano Banana"，Gemini 2.5 Flash Image，2025-08）让自然语言图像编辑、角色一致性、老照片修复"出圈"，成为当时最受欢迎的图像编辑模型，但它定位是**快、便宜、好玩**的 Flash 档，在**复杂排版、长文本渲染、事实性信息图、专业产线高保真**上仍有明显短板。Nano Banana Pro 是同一谱系的"Pro 档"升级：不追求速度而追求**最高质量与可控性**，把图像生成从"出好看的图"推向"出正确、可用、有事实依据的内容"。

技术脉络上，它属于 **Gemini 原生多模态生成**一支（[[gemini-2-0-flash-native-image]] → Gemini 2.5 Flash Image → Gemini 3 Pro Image），区别于纯扩散文生图（[[imagen]]/[[imagen-3]]、[[flux-2]]、Seedream 系）的最大特点是：图像生成共享同一个会"思考"的 LLM backbone（Gemini 3 Pro），因此能继承其推理、长上下文、工具调用（Google 搜索）能力。官方反复强调的卖点不是"画质参数"，而是 **"用 Gemini 3 的推理和真实世界知识把信息可视化得更对"**——例如基于实时天气/赛事/食谱生成信息图，基于生物学/历史事实生成图解。定位上它与同期开源旗舰 [[flux-2]]（BFL，开源 32B rectified-flow）形成"闭源原生多模态 vs 开源扩散"的对照。

## 模型架构
**重要前提：Nano Banana Pro 是闭源产品模型，Google 未发布技术报告或论文，未披露 backbone 类型（DiT / 自回归 / 掩码生成）、参数量、tokenizer/VAE、文本编码器等架构细节。** 以下为官方博客 + Gemini API 文档可确证的事实，工程内部细节如实标注"未披露"。

- **底座**：明确"built on Gemini 3 Pro"。Gemini 3 Pro 是 Google DeepMind 的旗舰多模态大模型，Nano Banana Pro 即其**原生图像生成/编辑能力**的产品化封装。图像生成与文本理解共享同一多模态模型，这也是它能调用"推理"和"Google 搜索接地"的根因。其内部生成范式（扩散 / 自回归 token / 二者混合）官方未披露。
- **I/O 与上下文**（来自 Gemini API model card）：模型代码 `gemini-3-pro-image`；输入=图片+文本，输出=图片+文本；**输入 token 上限 65,536，输出 token 上限 32,768**；知识截止 **2025 年 1 月**；最后更新 2025 年 11 月（稳定版）。
- **"思考模式"（Thinking）**：API 文档明确该模型"利用『思考』过程来推理复杂提示，会生成临时的『想法图片』（thought images，后端可见、不计费），在产出最终高质量图前优化构图"。即把 LLM 的 chain-of-thought 思想迁移到图像——先内部草拟/推演再定稿，这是它相对 Flash 档与传统一步扩散的核心差异。
- **多参考图融合（最多 14 张）**：可混合至多 14 张参考图，Gemini 3 Pro Image 档位的容量拆分为：**最多 6 张高保真对象图**（要精确还原进画面的物体）+ **最多 5 张人物图**（保持人物身份/风格一致）+ **最多 3 张风格参考图**。企业版博客把这描述为"给设计师的 few-shot prompting"——一次性喂入整套品牌风格指南（logo、配色、人物三视图、产品图）。
- **分辨率与宽高比**：内置 **1K / 2K / 4K** 三档输出（`imageSize` 参数取值 `512/1K/2K/4K`，其中 512/0.5K 为后续 3.1 Flash 新增）；宽高比覆盖 1:1、2:3、3:2、3:4、4:3、4:5、5:4、9:16、16:9、21:9 等十余种（1:4/4:1/1:8/8:1 等极端比为后续 3.1 Flash 新增）。
- **能力矩阵**（model card）：支持 图片生成 / 搜索接地 / 结构化输出 / 思考；**不支持** 函数调用、上下文缓存、代码执行、URL 上下文、Live API、Maps 接地、音频生成。

## 数据
**未披露。** Google 未公开训练数据来源、规模、图文对数量、配比、清洗过滤、re-captioning、合成数据或美学/安全过滤的任何细节（闭源产品，无技术报告）。可间接确证的两点：(1) 模型继承 Gemini 3 Pro 的世界知识，知识截止为 **2025 年 1 月**；(2) 通过 **Google 搜索接地（grounding）**，推理时可检索实时网页内容作为生成依据，从而绕过训练数据时效性限制（见下"评测"中的 grounding 机制；注：把网络图片作为视觉上下文的"图片搜索接地"是后续 3.1 Flash 才有的能力，Pro 仅网页搜索接地）。训练语料本身的构成未报告。

## 训练方法
**未披露。** 训练目标（diffusion / flow matching / next-token / masked-token）、多阶段流程（预训练→continue→SFT→偏好对齐 RLHF/DPO/reward model）、蒸馏与步数加速等均未公开。仅能确证：模型作为 Gemini 3 Pro 的图像能力，理论上继承其后训练管线（Vertex 文档列出 Gemini 系支持 SFT / 强化学习微调 / 偏好调优 / 蒸馏等，但这些是平台对开发者开放的调优能力，**不等于** Nano Banana Pro 自身的训练配方）。具体 RL / reward model / 偏好数据如实标注"未报告"。

## Infra（训练 / 推理工程）
- **训练算力 / 并行 / 精度 / 吞吐：未披露。** 无任何 GPU·时、TPU 规模、分布式策略数字。
- **推理与部署形态**（可确证）：
  - 提供 **Batch API、Flex 推理、优先推理（Priority Inference）** 三种用量方案；企业版（Vertex AI）提供 **Provisioned Throughput（预留吞吐）+ Pay-As-You-Go** 与高级安全过滤。
  - "思考模式"会产生不计费的中间"想法图片"，相应地**延迟与成本高于 Flash 档**——官方明确建议：高速量产用 Nano Banana（2.5 Flash Image），最高质量产线用 Nano Banana Pro（更高成本与延迟）。
  - 部署面极广：Gemini App（"Create images" + "Thinking" 模型）、AI Mode in Search（美区 AI Pro/Ultra）、NotebookLM、Google Ads、Workspace（Slides/Vids）、Google AI Studio、Gemini API、Vertex AI、Google Antigravity（agentic 开发平台，编码 agent 可直接生成 UI mockup）、Flow（AI 影视工具）；第三方集成 **Adobe（Firefly/Photoshop）、Figma、Canva、Photoroom** 等。
  - 推理步数 / 缓存 / 量化 / 蒸馏等加速细节未披露。

## 评测 benchmark（把效果讲清楚）
**官方口径（定性，无可机读数字）**：开发者博客称 "Gemini 3 Pro Image excels on Text-to-Image AI benchmarks"，并配了一张相对竞品的文生图基准柱状图——但**该图为图片，未给出可抠取的具体分值；Google 官方未在博客/文档中以文本形式公布 FID、GenEval、DPG-Bench、T2I-CompBench、HPSv2 等标准分数**。因此本节标准学术指标一律记为"官方未报告"，不臆造数字。官方主张的能力优势集中在三点：**(1) 图内文字渲染**（号称是当时最强，支持短标语到整段文字、多语言、图内文字翻译/本地化）；**(2) 事实性 / 世界知识**（生成更"对"的信息图、图解、地图）；**(3) 一致性**（最多 5 人身份保持、14 图融合）。

**第三方盲评基准（Artificial Analysis 文生图竞技场，本地落盘快照 2026 年抓取）**——基于盲评 Elo（用户在不知模型名的情况下二选一投票）：
- **Nano Banana Pro (Gemini 3 Pro Image)：Elo 1,219**（95% CI ±9，6,241 样本，发布 Nov 2025），当前排名第 7、API 价 **$134 / 1k 图**（1024×1024 默认设置）。
- 同门 Nano Banana 2 (Gemini 3.1 Flash Image Preview，2026-02)：Elo 1,255，$67/1k 图。
- 上一代 Nano Banana (Gemini 2.5 Flash Image)：Elo 1,159，$39/1k 图。
- 对照 ByteDance Seedream 4.0：1,193（$30/1k）；Seedream 4.5：1,167。
- 榜首（快照时点）GPT Image 2 (high)：1,339。
- **解读**：此为 2026 年中的滚动快照，彼时榜单已被更晚的模型（GPT Image 2、Nano Banana 2、MAI-Image-2.5 等）刷新；**Nano Banana Pro 在 2025-11 发布当时是文生图竞技场头部模型之一**，Elo 1219 相对同代 Flash 档（1159）有约 60 分提升、相对 Seedream 4.0（1193）领先，但价格也明显更高（$134 vs $30–39 /1k）。把它当"发布即 SOTA、随后被次代追平/超越"理解最准确。

**Grounding 的机制性证据**（API 文档）：Nano Banana Pro（`gemini-3-pro-image`）model card 明确**支持"搜索接地"**（Google 搜索）；开启后响应返回 `groundingMetadata`，其 `groundingChunks` 给出用于"为生成图片提供依据"的**前 3 个网络来源**（`searchEntryPoint` 含搜索建议的 HTML/CSS）。这是"可推理图像生成"区别于纯文生图模型的硬功能，而非画质打分。

> **澄清（避免与 Nano Banana 2 混淆）**：文档里另外两项 grounding 增强——**"依托 Google 图片搜索接地"**（把图片搜索检索到的网络图片作为视觉上下文，注：不可用于搜索人物）与**"视频转图片生成"**（分析视频帧、最多 131,072 token）——文档均明确标注 **"此功能仅适用于 Gemini 3.1 Flash Image 模型"**，即后续的 Gemini 3.1 Flash Image（Nano Banana 2，2026-02），**并非 Nano Banana Pro 的能力**。此前版本曾误记为 Pro 功能，已更正。

**消融 / 对比结论**：官方未发布消融实验。唯一可确证的纵向对比是官方明确"Gemini 3 Pro Image 相对 2.5 Flash Image 在文字渲染上是显著飞跃（significant leap forward），把抽象图像生成变成可用的功能性资产"。

## 创新点与影响
**核心贡献**
1. **把"会思考的 LLM"直接当图像生成底座**：不是在扩散模型旁挂一个文本编码器，而是图像生成与 Gemini 3 Pro 推理共享同一多模态模型，带来"想法图片"式的内部推演、长上下文、结构化输出，以及最关键的——**工具调用（Google 搜索实时接地）**。这把图像生成从"凭训练记忆作画"推进到"检索事实后再作画"，对信息图/图解/地图等**强事实性场景**是范式级改变。
2. **图内文字渲染做到当时最强**：长段落、多语言、图内文字翻译与版式本地化（菜单/招牌/海报保留原艺术风格替换文字），把图像生成从"创意 demo"推向"营销/教育/产线可交付资产"。
3. **多参考一致性工程化**：14 图融合 + 5 人身份保持 + 风格/对象/人物三类参考拆分，等价于"给设计师的 few-shot"，直击品牌一致性这一企业最大痛点；配合 4K 输出直接对接印刷/广告产线。
4. **可信溯源默认开启**：每张图强制 SynthID 隐形水印，并支持"上传图片问 Gemini 是否为 Google AI 生成"的反向核验；免费/Pro 档加可见 Gemini sparkle 水印，Ultra/AI Studio 去可见水印。

**影响**：作为 2025 末闭源旗舰，它把"图像生成 = 多模态推理 + 检索 + 高保真渲染"的产品形态确立下来，迅速被 Adobe/Figma/Canva/Photoroom/Shopify/Wayfair/WPP 等接入成为"创意经济的基础设施层"；并通过 Antigravity 让编码 agent 直接产出 UI mockup，渗透 agentic 开发。它与开源阵营的 [[flux-2]]、字节 Seedream 系共同标记了 2025 下半年"文字渲染 + 多参考编辑 + 世界知识"成为图像模型新主战场。

**已知局限**：(1) **完全闭源、零技术披露**——架构/数据/训练/算力全部未知，不可复现，学术价值受限；(2) 成本与延迟高（$134/1k 图、思考模式更慢），不适合高并发量产，需与 Flash 档分工；(3) 官方未发布任何标准学术基准分数与消融，效果主要靠 demo 与盲评 Elo 佐证；(4) grounding 能力受限：Pro 仅支持网页搜索接地，**不含**"图片搜索接地"与"视频转图片"（二者为后续 3.1 Flash 独有），且 model card 列出不支持函数调用、上下文缓存、代码执行、URL 上下文、Live API、Maps 接地、音频生成；(5) 发布时的领先在数月内即被次代模型（含自家 Nano Banana 2）追平/超越，反映该赛道迭代极快。

## 原始链接
- blog（主发布，Google DeepMind）: https://blog.google/innovation-and-ai/products/nano-banana-pro/
- blog（开发者版，Gemini API/AI Studio/Vertex）: https://blog.google/innovation-and-ai/technology/developers-tools/gemini-3-pro-image-developers/
- blog（企业版，Google Cloud）: https://cloud.google.com/blog/products/ai-machine-learning/nano-banana-pro-available-for-enterprise
- model-card（Gemini API，硬规格 token/能力）: https://ai.google.dev/gemini-api/docs/models/gemini-3-pro-image
- docs（图片生成文档，分辨率/14图/思考/grounding 机制）: https://ai.google.dev/gemini-api/docs/image-generation
- model-card（Vertex AI / Gemini Enterprise）: https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/3-pro-image
- project（DeepMind 模型页）: https://deepmind.google/models/gemini-image/pro/
- benchmark（第三方盲评，Artificial Analysis 文生图竞技场）: https://artificialanalysis.ai/text-to-image/arena/leaderboard-text

## 本地落盘文件
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--blog-google.md
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--developers-blog.md
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--enterprise-blog.md
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--image-gen-docs.md
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--api-modelcard.md
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--vertex-modelcard.md
- ../../../sources/omni/2025/gemini-3-pro-image-nano-banana-pro--artificialanalysis-t2i-arena.md
