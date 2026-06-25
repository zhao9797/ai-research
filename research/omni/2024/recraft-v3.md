---
title: "Recraft V3 (red_panda)"
org: Recraft
country: US
date: "2024-10"
type: blog
category: t2i
tags: [t2i, closed-source, text-rendering, layout-control, vector-graphics, controlnet, design, api, ocr]
url: "https://www.recraft.ai/blog/recraft-introduces-a-revolutionary-ai-model-that-thinks-in-design-language"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.recraft.ai"
downloaded: [recraft-v3--blog.md, recraft-v3--ml-team-insights.md, recraft-v3--docs.md, recraft-v3--aa-leaderboard-snapshot.md, arxiv-2311.16465.pdf, arxiv-2404.04624.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位

Recraft V3（竞技场代号 **red_panda**）是美国初创 Recraft 于 2024-10-30 发布的闭源文生图产品级模型，核心创新是用**显式"文字版式图"（text layout）条件 + ControlNet 式注入**让模型从生成"几个单词"跃迁到**生成长段、可精确定位的可读文字**，配合矢量/品牌风格可控生成，主打专业平面设计场景；发布后 4 天内以 **ELO 1172** 登顶 Artificial Analysis（HF）文生图竞技场榜首，超过 Midjourney、OpenAI 等所有同期模型，并保持 **连续 5 个月第一**（官方文档口径）。

> 边界声明：Recraft **从未发布论文或正式技术报告**。本页所有方法细节来自两篇官方博客——发布公告（2024-10-30）与 ML 团队技术揭秘《How To Create SOTA Image Generation with Text》（2024-11-07）——以及 V3 文档页。架构骨干（U-Net/DiT、参数量、分辨率、算力）**官方完全未披露**，相应维度如实标注"未披露"。本页对其方法的描述忠于博客原文，**不臆造任何数字**。

## 背景与定位

Recraft V3 不是一篇研究发布，而是一次"**面向专业设计师的产品级闭源升级**"，要放进文生图"可读文字 + 可控版式"这条支线里理解：

- **痛点**：直到 2024 年，文生图模型渲染超过几个单词的文字仍极易失败——会把"Recraft"画成扭曲的乱码（官方拿前代 **Recraft 20B** 的失败例子做对照）。ML 博客把根因归到**训练条件不够细**：图文对的 caption 通常只泛泛描述内容、几乎不含图中文字的精确信息，模型只在"logo 名/标题"这种简单场景学会写字，其余情况就"幻觉"出乱码。人脑对文字错误尤其敏感（对手指数目、汉字错误的敏感度则不同），使文字错误格外刺眼。
- **解法路线选择**：博客明确——最理想的条件是"原图本身"（含全部文字信息），但这样模型只会学会复制而非生成；于是退而求其次选**"文字版式图（a drawing of a text layout）"**作为额外条件，把原图里所有文字按位置重绘成一张新图，在训练与推理时连同 caption 一起喂给生成模型。**灵感直接来自 [[TextDiffuser-2]]（arXiv:2311.16465，微软研究院）**——后者用语言模型做版式规划、用 LLM 在 line-level 编码文字位置/内容。
- **谱系位置**：Recraft V3 是把"显式版式条件渲染文字"（GlyphControl / TextDiffuser / TextDiffuser-2 一脉）**工程化到 SOTA 产品**、并叠加矢量生成与品牌风格控制的代表作。同期可对照的闭源旗舰是 [[flux-1-1-pro]]（BFL，2024-10）与 Ideogram v2（以文字渲染著称）。直接前代为 **Recraft 20B**（ML 博客称其为 "previous image generation model"，2024-03，竞技场 ELO 977；文档另列有独立的 "Recraft V2" 页，故 20B 与命名上的 V2 是否同一未在源中明确等同），V3 是从头重训的新一代。

## 模型架构

官方未公布骨干类型、参数量、分辨率与 tokenizer，以下是博客可考证的**系统级架构**（一个多组件流水线，而非单一网络）：

整个系统由**两条可独立训练的分支 + 一个生成主干**组成（ML 博客 Fig 3–5）：

1. **文字版式生成器（text layout generator）**——基于一个**大语言模型（LLM）**。输入是 caption，输出是"特定格式"的文字版式（每个词的内容 + 坐标）。它把用户 prompt 翻译成版式，供下游图像生成器使用，也可由用户在画布上**手动指定/微调**位置。
2. **图像生成主干（image generator）**——在 Recraft 原有图像生成器基础上，**额外接一路"文字版式图"输入**；版式以**图像形式**传入，注入方式"类似 [[ControlNet]] 架构"（arXiv:2302.05543）。这是把文字位置/内容显式编码进扩散过程的关键。骨干本身（U-Net vs DiT、VAE、text encoder）**未披露**。
3. **（数据侧）自训 OCR 模型 + 版式条件 captioning 模型**——见"数据"节，是为构造训练数据而训练的辅助模型。

**关键设计点（博客披露）**：
- 文字版式以"图"的形态作为 ControlNet 式控制信号，使文字"画在哪、画什么"成为可控条件，而非靠 caption 隐式学习——这是长文本可读 + 可定位的根本原因。
- 推理时版式有**两种来源**：用户手动在画布上摆放，或由 LLM 版式生成器自动产出（Fig 5），兼顾"精确控制"与"全自动"。
- **风格作为输入**：V3 接受"风格"作为模型输入，无需为捕捉某品牌风格而重训模型——可从一小组示例图抽取品牌风格并迭代调参（"style as an input"）。该能力 V2 已具备，V3 延续。
- **矢量生成**：支持从简笔 pictogram 到精细 vector art 的矢量图生成（产品层面，机制未公开是端到端矢量生成还是栅格→矢量化）。

## 数据

官方未给数据规模/配比/来源数字，但 ML 博客**详细披露了为"可读文字"专门构造数据集的完整管线**（Fig 2–3，是本工作信息量最大的部分）：

- **目标**：为每张训练图配一张**尽可能精确的文字版式图**。若版式不准，模型会像对待不准 caption 一样学会忽略它——所以"版式精度"是数据质量的命门。
- **自训 OCR 模型**：现有开源 OCR 模型"都不够好"——主因是 Recraft 的数据分布与这些模型的训练集差异很大。于是 Recraft **自己训了一个 OCR 模型**，方法基于论文 **《Bridging the Gap Between End-to-End and Two-Step Text Spotting》**（arXiv:2404.04624）——该法用锁参的独立 detector + recognizer，经零初始化 Bridge 网络连接，兼顾端到端性能与模块化（Total-Text 83.3%、ICDAR2015 89.5%）。Recraft 在自标注数据上重训，用它抽取图中所有文字及其位置。
- **OCR 预测过滤**：再训一个模型**过滤 OCR 预测**，从而得到大规模、高质量的文字版式数据集。
- **版式条件 captioning 模型**：这是管线里很巧的一环——caption 通常不含图中文字信息，若直接拿"caption→版式"训练版式生成器，它会像普通 t2i 一样**幻觉版式**。为此 Recraft 训了一个**可被文字版式 condition 的图像 captioning 模型**，让生成的 caption 显式包含版式里的所有词、与版式对齐，质量大幅提升。
- **整体逻辑**：数据准备阶段（OCR→过滤→版式条件 caption）与训练阶段恰好**互为逆过程**——数据准备模型的输出，正是新训模型的输入（Fig 3）。

具体图像/图文对数量、美学过滤、安全过滤、合成数据比例等：**均未披露**。

## 训练方法

- **训练目标 / 范式（diffusion vs flow-matching、步数蒸馏等）**：**官方完全未披露**。仅知图像主干是"在 Recraft 原有图像生成器基础上加文字版式输入"，是从头重训的新一代模型（"trained a new SOTA model from scratch"）。
- **两分支独立训练**：文字版式生成器与图像生成器**可分别独立训练**。
- **文字版式生成器（LLM）训练的两大工程难点**（博客明确）：
  1. **输出顺序**：LLM 逐 token 输出，但文字版式本质**无序**，仅凭坐标难以自动决定阅读/书写顺序。解法是**让版式词序与对应 caption 对齐**——借助 captioning 模型把词正确分组排序（例：caption 里"K"先于"koala"出现，预测版式里"K"就排在前）。
  2. **输出格式与性能**：最初用 **JSON** 格式输出版式，推理比最终格式**慢 10 倍**；优化为"尽量少预测 token"的紧凑格式后大幅提速。
- **图像主干训练**：在原图像生成器上加一路文字版式图输入，以 ControlNet 式方式训练其遵循版式。
- **超参 / 优化器 / RLHF / DPO / 蒸馏加速**：**均未披露**。文档侧仅提到 V3 有 **Artistic level** 参数（推理可调，控制构图的"非常规程度"），属产品参数而非训练 trick。

## Infra（训练 / 推理工程）

- **算力 / GPU·时 / 并行 / 精度 / 吞吐**：**全部未披露**。
- **推理**：版式生成器输出格式从 JSON 改为紧凑格式后**快约 10×**（上文）；其余步数/缓存/量化/部署细节未公开。
- **部署形态（已知）**：桌面 Web 端（Canvas）、iOS / Android App、以及 **API**。V3 是"业界首个支持风格一致性 + 矢量图生成的 API"（官方口径）；API 同时支持栅格与矢量格式、带文字的图像生成、自定义风格/品牌色，并提供矢量化、放大、画质增强、抠图等编辑能力。

## 评测 benchmark

Recraft **未公布任何自动指标**（无 FID / CLIPScore / GenEval / DPG-Bench / T2I-CompBench / HPS / ImageReward 等）。唯一对外成绩是**第三方人评竞技场 ELO**：

- **Artificial Analysis（Hugging Face）文生图竞技场**：发布后 4 天内以 **ELO 1172** 拿下 **#1**，高于 Midjourney、OpenAI 及所有主要厂商（官方博客）。竞技场用访客两两对比图像打 ELO，是公开人评 ELO（非自动指标）。
- **持续领先**：V3 文档称其在该榜"**连续 5 个月排名第一**"。
- **当前快照（本页抓取于 2026-06，仅供时间坐标，非发布期成绩）**：同一榜单上 **Recraft V3 现为 ELO 1,068（Oct 2024 发布，7,871 样本，$40/1k 图）**，已被大量更新模型（Recraft V4/V4.1、FLUX.2 系列、Ideogram 4 等）超过——属正常代际更替，**与发布期 #1 不矛盾**（榜单随新模型加入而下移）。
- **官方主张的强项维度**（定性，无数字）：长文本渲染（发布博客口径"全世界唯一能生成长文本的模型"；文档页口径更克制——"首个能准确渲染 mid-size 文字"、"截至 2025 年唯一能把文字放到指定位置的模型"）、解剖正确性（手指/四肢数目、比例、空间一致）、prompt 遵循（物体计数/颜色/位置）、高美学价值（对标 Midjourney 历来的强项）。
- **消融 / 对照**：仅有定性对照——前代 Recraft 20B 渲染"Recraft generates text amazingly good!"失败（Fig 1）；引入文字版式条件后长文本可读。无量化消融。

> 上述所有数字（ELO 1172 / 1068、连续 5 个月第一、JSON 慢 10×）均来自已落盘的官方博客 / 文档 / 竞技场快照；官方未报告的指标本页一律标"未报告/未披露"。

## 创新点与影响

**核心贡献**
1. **把"显式文字版式条件"做到产品级 SOTA**：用 OCR 自动抽取 → 自训 OCR + 过滤 → 版式条件 captioning → ControlNet 式版式注入 的完整闭环，解决长文本/可定位文字这一长期难题，思路承自 [[TextDiffuser-2]] 但在数据工程与产品化上推到 #1。
2. **文字版式的双来源（手动 / LLM 自动）**：既给设计师逐字定位的精确控制，又能全自动生成，是其"thinks in design language"定位的技术落点。
3. **设计向能力栈**：长文本排版 + 文字精确定位 + 矢量生成 + 品牌风格一致（无需重训）+ 全套编辑工具（Eraser/Inpaint/Outpaint/Upscale/抠图），并首发支持风格一致性与矢量的 API。

**影响**
- 把"可读文字 + 可控版式"确立为 2024 年闭源文生图竞争的关键维度之一，与 Ideogram、后续 [[flux-1-tools]] / GPT-Image 的文字能力形成对照。
- 验证了"为特定能力（文字）专门构造高精度条件数据 + 训练辅助模型（OCR/captioner）"这一数据工程范式的有效性。
- 商业上确立 Recraft 在专业设计垂直赛道的位置，并延续到 V4 / V4.1。

**已知局限**
- **闭源 + 无技术报告/论文**：骨干架构、参数、分辨率、训练目标、算力、数据规模全部不可考，复现与严肃比较受限。
- **无自动 benchmark**：唯一成绩是人评 ELO，缺 GenEval/DPG 等可比量化指标。
- 方法核心（版式条件、OCR）的具体网络与超参仅作高层描述，关键工程细节未公开。

## 原始链接

- blog（发布公告）: https://www.recraft.ai/blog/recraft-introduces-a-revolutionary-ai-model-that-thinks-in-design-language
- blog（ML 团队技术揭秘，一等公民）: https://www.recraft.ai/blog/how-to-create-sota-image-generation-with-text-recrafts-ml-team-insights
- docs（V3 文档页）: https://www.recraft.ai/docs/recraft-models/recraft-V3
- benchmark（Artificial Analysis 文生图竞技场）: https://huggingface.co/spaces/ArtificialAnalysis/Text-to-Image-Leaderboard ｜ https://artificialanalysis.ai/text-to-image/arena/leaderboard-text
- 方法灵感（TextDiffuser-2，非 Recraft 自有）: https://arxiv.org/abs/2311.16465
- 自训 OCR 基础（Bridging Text Spotting，非 Recraft 自有）: https://arxiv.org/abs/2404.04624

## 本地落盘文件

- ../../../sources/omni/2024/recraft-v3--blog.md
- ../../../sources/omni/2024/recraft-v3--ml-team-insights.md
- ../../../sources/omni/2024/recraft-v3--docs.md
- ../../../sources/omni/2024/recraft-v3--aa-leaderboard-snapshot.md
- ../../../sources/omni/2024/arxiv-2311.16465.pdf
- ../../../sources/omni/2024/arxiv-2404.04624.pdf
