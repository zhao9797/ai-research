---
title: "Recraft V4"
org: Recraft
country: US
date: "2026-02"
type: blog
category: t2i
tags: [t2i, closed-source, design, vector-graphics, svg, raster, text-rendering, aesthetics, api, no-tech-report]
url: "https://www.recraft.ai/blog/introducing-recraft-v4-design-taste-meets-image-generation"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/recraft-ai/ComfyUI-RecraftAI"
hf_url: ""
modelscope_url: ""
project_url: "https://www.recraft.ai"
downloaded: [recraft-v4--blog.md, recraft-v4--docs.md, recraft-v4--choosing-a-model.md, recraft-v4--v4-1-docs.md, recraft-v4--aa-leaderboard-snapshot.md, recraft-v4--comfyui-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位

Recraft V4 是美国设计向初创 Recraft 于 **2026-02** 发布的闭源文生图新一代旗舰，定位是把"**设计品味（design taste）**"作为核心卖点——在与专业设计师协作下调优**构图、配色关系、明暗、材质真实感、细节层级**，让输出"像被艺术指导过"而非千篇一律的图库感；产品上提供**栅格 + 矢量双输出**（V4 / V4 Pro / V4 Vector / V4 Pro Vector 四档），并自称是**唯一能从 prompt 直接生成可编辑、生产级 SVG** 的模型。第三方 Artificial Analysis 文生图竞技场快照（2026-06）显示 **Recraft V4 Pro ELO 1,144（7,371 样本）、Recraft V4 ELO 1,137（7,448 样本）**。

> 边界声明：Recraft **从未发布论文或技术报告**，V4 亦然（SERP 仅返回产品/营销页，无 arXiv/技术报告）。本页**所有方法与数字均来自已落盘的官方博客 / 文档 / 第三方竞技场快照**。骨干架构、参数量、训练目标、数据规模、算力等**官方全部未披露**，相应维度如实标注"未披露"，**不臆造任何数字**。

## 背景与定位

Recraft V4 是 [[recraft-v3]]（2024-10，竞技场代号 red_panda）的从头重建（"ground-up rebuild" / "ground-up rebuild focused on… visual taste"）后继，要放进"**设计垂直赛道的闭源文生图旗舰**"这条支线理解：

- **问题诊断（官方口径）**：博客明确指出，当下主流图像模型"are optimized for broad, general preference（为广义、大众化偏好优化）"——这对大众吸引力有效，但**不一定符合品牌系统、营销活动、生产级设计工作所需的标准**。Recraft 的解法不是再卷"prompt 遵循准确率"，而是补上**视觉判断（visual judgment）**这一维：构图、光照、配色关系、材质真实感都要"有品味"。这是它与 [[gemini-3-pro-image-nano-banana-pro]]、[[gpt-image-2]]、[[seedream-4-0]]、[[flux-2]] 等"通用偏好优化"旗舰的差异化叙事。
- **谱系位置**：V4 延续 V3 的"设计语言（thinks in design language）+ 矢量生成 + 文字渲染"定位，但**重心从"长文本可读 / 文字精确定位"转向"整体审美品味"**。值得注意：V4 **暂不支持** V3 招牌的若干能力——Style creation（自定义/品牌风格创建）、Prompt-based editing（提示词编辑）、Image sets、Artistic level control（构图非常规度调节）；官方"选模型"指南因此仍建议"需要风格一致性 / 精确文字定位 / artistic level 时用 V3"。即 V4 是新审美主干，但功能栈尚未完全覆盖 V3。
- **代际位置**：V4（2026-02）之后 Recraft 又于 **2026-05-14** 发布 [[recraft-v4-1]]（V4.1，新增 Utility 简化变体、更克制的写实与更短 prompt 响应），故 V4 是 V4 系列的奠基代，本页聚焦 V4 本体。

## 模型架构

**官方未公布任何架构细节**——backbone（U-Net / DiT / MMDiT / 自回归 / masked）、参数量、VAE/tokenizer、text encoder、条件注入方式**全部未披露**。仅能从产品文档归纳出**系统级形态**：

- **四档同源模型**：V4 与 V4 Pro"share the same creative capabilities and design taste"，"the difference is resolution and scale"——即 Pro 与 Standard 共享同一审美主干，差异在**分辨率与算力规模**，而非两套独立模型。
  - **Recraft V4（Standard）**：栅格，**1024×1024**，约 10 秒/图。
  - **Recraft V4 Pro**：栅格，**2048×2048**（原生高分辨率），约 28–30 秒/图；官方称其"perfecting anatomy issues and improving realism across complex scenes"、更适合复杂构图与印刷级（print-ready）高保真。
  - **Recraft V4 Vector / V4 Pro Vector**：矢量输出，约 15 秒 / 45 秒。
- **矢量生成**：V4 称是"the only AI model that generates editable vector files from a prompt"——产出**真正的 SVG**（结构化图层、干净几何、离散色块），可直接导出 web/print 或在专业设计软件二次编辑，**无需 tracing / cleanup / 转换**。机制（端到端矢量生成 vs 栅格→矢量化）**官方未说明**；从"discrete color regions / structured layers / scalable geometry"的措辞看更像面向矢量结构的专门生成路径，但无源证实，标注**未披露**。
- **文字作为结构组件**：博客强调 V4"treats typography as a structural component of the composition rather than a purely decorative overlay"——长 prompt 下让文字与构图（如压向画框边缘、跨水线桥接上下空间）产生空间张力。这是 V3"显式文字版式 + ControlNet 式注入"思路的延续，但 **V4 未披露是否仍沿用 V3 的 text-layout/ControlNet 管线**，标注未披露。
- **Exploration Mode（探索模式）**：V4 独有的产品级能力——单条 prompt 一次产出 **8 张**多方向变体（multiple visual directions），用于创作早期快速比选风格/构图/概念。属推理/产品层特性，非架构机制。

> 输出格式（产品层）：SVG、PNG、JPG、PDF、TIFF、Lottie。

## 数据

**官方完全未披露** V4 的数据来源 / 规模 / 配比 / 清洗过滤 / re-captioning / 合成数据比例 / 美学与安全过滤等任何信息。

唯一可考证的、与数据相关的高层方法陈述：博客称模型是"developed in close collaboration with designers, tuning it around design aesthetics and professional expectations"——即**以专业设计师参与的方式围绕"设计审美与专业预期"调优**。这指向某种**设计师偏好驱动的对齐/调优**（很可能含人评偏好数据），但官方未说明是 SFT、偏好数据规模、还是 RLHF/DPO 形态，**亦无任何数字**，故训练数据维度整体记为"未披露"。

（对照：[[recraft-v3]] 曾详细披露过为"可读文字"专门构造的 OCR→过滤→版式条件 captioning 数据管线；V4 博客**未重述也未扩展**该数据工程，是否沿用未知。）

## 训练方法

**训练目标 / 范式**（diffusion / flow-matching(rectified flow) / next-token / masked-token）、多阶段流程（预训练→continue→SFT→偏好对齐）、蒸馏与步数加速、超参与 trick——**官方全部未披露**。可确证的仅两点高层陈述：

- **从头重建**："a ground-up rebuild"——V4 是相对 V3 重新构建的新一代主干，而非微调。
- **设计师协同调优**："developed… in close collaboration with designers, tuning it around design aesthetics and professional expectations"，目标"not just accurate prompt interpretation, but stronger visual judgment across composition, lighting, color relationships, and material realism"。这强烈暗示存在一个**面向"设计品味"的偏好对齐/审美调优阶段**（区别于"broad general preference"优化），但**具体方法（reward model / DPO / RLHF / 人评数据规模）官方未公开**，标注未披露。

> 推理速度可作为加速能力的间接旁证：Standard 1024² 约 10s、Pro 2048² 约 28–30s、Vector 15s/45s——但官方未公开步数、是否做了 consistency/步数蒸馏，故不能据此断言加速手段，记为未披露。

## Infra（训练 / 推理工程）

- **训练 infra**：算力规模 / GPU·时 / 并行分布式 / 混合精度 / 吞吐——**全部未披露**。
- **推理 / 部署（已知）**：
  - 推理时延（官方文档，V4 发布期口径）：V4 ~10s（1024²）、V4 Pro ~28–30s（2048²，博客 ~28s / V4 文档 ~30s）、V4 Vector ~15s、V4 Pro Vector ~45s。注：后发布的 V4.1 文档「Model Inference Time」表给出的是**中位时延**且明显更低（V4 11s、V4 Pro 16s、V4 Vector 16s、V4 Pro Vector 19s），与发布期"约 N 秒"口径不一致（疑为后续推理优化或测量口径差异），两组数字均来自已落盘官方源，此处并列存证、不强行二选一。
  - 部署形态：**Recraft Studio 网页端 + API**（全平台），并有 iOS / Android App；全部 V4 模型对**所有套餐（含 Free 计划）**开放。
  - 第三方 ComfyUI 节点（recraft-ai/ComfyUI-RecraftAI）通过 Recraft API 调用（其 README 截至 2026-06-25 抓取时仍只描述 "Recraft V3（code-named red_panda）"、零处提及 V4，已落盘核对）。
  - 计费（第三方 Artificial Analysis 报价，2026-06 快照）：Recraft V4 **$40/1k 图**、Recraft V4 Pro **$250/1k 图**；Studio 内 Exploration Mode 每图 2 credits、每次固定 8 图共 16 credits。
- 步数 / 缓存 / 量化 / 蒸馏等推理加速工程细节：**未披露**。

## 评测 benchmark（把效果讲清楚）

**Recraft 自身未公布任何自动指标**（无 FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore 等），延续 V3"只给定性对比、不给自动数字"的一贯做法。可用的量化成绩来自**第三方 Artificial Analysis 文生图竞技场（人评 ELO）**，以下为本页抓取的 **2026-06 快照**（非发布期成绩，仅作时间坐标 + 竞争位次）：

| 模型 | ELO | 95%CI | 样本 | 发布 | API 报价 |
|---|---|---|---|---|---|
| **Recraft V4 Pro** | **1,144** | -9/9 | 7,371 | Feb 2026 | $250/1k |
| **Recraft V4** | **1,137** | -8/8 | 7,448 | Feb 2026 | $40/1k |
| Recraft V4.1 Pro（参照后代） | 1,155 | -10/10 | 3,206 | May 2026 | $210/1k |
| Recraft V4.1（参照后代） | 1,148 | -10/10 | 3,536 | May 2026 | $35/1k |
| Recraft V3（参照前代） | 1,068 | -8/8 | 7,873 | Oct 2024 | $40/1k |

- **代际进步**：V4（1,137）较 V3（1,068）在同一榜单上提升约 **+69 ELO**，V4 Pro 1,144 再高一档；后续 V4.1 系列（1,148/1,155）再小幅领先 V4，与"V4 奠基、V4.1 精修"的官方叙事一致。
- **竞争位次（2026-06 快照同榜头部，供对照，非 Recraft 数据）**：GPT Image 2(high) **1,339（#1）**、Nano Banana 2 1,256、Nano Banana Pro 1,220、Seedream 4.0 1,194、FLUX.2[max] 1,193、Imagen 4 Ultra 1,174、Ideogram 4.0 Quality 1,169。V4/V4 Pro 在该综合人评榜处于**中上游**（约第 40–43 名档），明显落后于 2026 年最新通用旗舰——这与 Recraft 的定位自洽：它优化的是**"设计师品味 / 生产可用性 / 矢量输出"**这类**通用 Arena 不直接奖励**的维度，而非通用大众偏好 ELO。
- **官方主张的强项（定性，无数字，来自发布博客的逐对比对）**：
  - **写实人像的情绪氛围**：V4 Pro 产出"cinematic frames with distinct emotional atmosphere"，对照 Nano Banana Pro"technically compliant, yet feels less expressive"。
  - **短 prompt 下的审美自主**：极简 prompt 时 V4"delivers images with strong visual identity, intentional styling… could find its way into a fashion editorial"，对手则"safe / stock-like / commercially polished"。
  - **排版作为结构**：长 prompt（如 OVERTHINK 3D 海报、TIDELINE 编辑海报）中 V4 让文字"压向画框 / 跨水线桥接空间"，与构图形成张力，而非贴图式叠加。
  - **多产品 mockup 的合规与一致**：BOTANICA LAB 案例中 V4 Pro 准确产出"3 瓶 + 1 罐 + 一致 label/logo"，对照 Nano Banana Pro"产品数量错误、漏掉一瓶品牌标识"。
  - **矢量**：唯一从 prompt 直出可编辑生产级 SVG。
- **消融 / 自动量化对照**：**无**。官方仅有"V4 vs Nano Banana Pro / GPT Image / Midjourney"的**主观逐图对比**，均为 Recraft 自选样例的定性叙述，**无量化消融、无独立第三方自动评测**。

> 上表 ELO / 样本 / 报价均来自已落盘的 Artificial Analysis 竞技场快照（2026-06）；官方未报告的自动指标本页一律标"未报告"，**不编造**。

## 创新点与影响

**核心贡献（基于官方一手叙事）**
1. **把"设计品味"显式作为优化目标**：相对"broad general preference"优化的主流旗舰，V4 以**专业设计师协同调优**为路线，把构图/配色/明暗/材质/细节层级的**视觉判断**当一等优化对象——这是它在拥挤的 2026 文生图赛道的差异化叙事（"true visual taste to AI image generation"）。
2. **生产级矢量直出**：自称唯一从 prompt 直接生成**可编辑结构化 SVG**（图层/几何/离散色块），免 tracing/cleanup，面向品牌资产、图标、插画、产品设计的真实生产流水线。
3. **同源四档（Standard/Pro × Raster/Vector）+ Exploration Mode**：共享审美主干、按分辨率/算力分档（1024² ↔ 2048²），并以单 prompt 出 8 变体降低创作早期试错成本，把"设计工作流"产品化。

**影响**
- 与 [[recraft-v3]] 的"文字版式 / 矢量"卖点一脉相承，进一步把 Recraft 在**专业设计垂直赛道**的位置坐实；并直接催生后代 [[recraft-v4-1]]（2026-05）。
- 给"通用 Arena ELO 不等于专业可用性"提供了又一案例：V4 在综合人评榜处中上游，却以"设计师品味 + 矢量 + 生产可用"另辟评价维度——提示评测体系对**设计/生产场景**覆盖不足。

**已知局限**
- **闭源 + 无技术报告/论文**：骨干、参数、分辨率策略、训练目标、数据规模、算力**全部不可考**，无法复现或做严肃技术比较。
- **功能栈相对 V3 有缺口**：V4 暂不支持 Style creation、Prompt-based editing、Image sets、Artistic level control（官方仍建议这些需求回退 V3）。
- **无自动 benchmark**：Recraft 一贯不出 GenEval/DPG/FID 等可比量化指标，唯一第三方量化成绩是综合人评 ELO，在该榜上落后于 2026 最新通用旗舰（GPT Image 2 / Nano Banana 2 等）。
- **文字能力相对 V3 表述更克制**：V4 文档称"短/中长短语高保真"，未再主张 V3"全世界唯一能生成长文本"的口径。

## 原始链接

- blog（V4 发布公告，唯一官方公告，一等公民）: https://www.recraft.ai/blog/introducing-recraft-v4-design-taste-meets-image-generation
- docs（V4 官方文档页：版本/分辨率/特性/限制/计费）: https://www.recraft.ai/docs/recraft-models/recraft-V4
- docs（选模型指南：V4 vs V4 Pro vs V3 vs V2）: https://www.recraft.ai/docs/recraft-models/choosing-a-model
- docs（V4.1 文档页，后代/谱系对照）: https://www.recraft.ai/docs/recraft-models/recraft-v4-1
- benchmark（Artificial Analysis 文生图榜，第三方人评 ELO，源自 Image Arena 盲投；本页快照即此页）: https://artificialanalysis.ai/image/leaderboard/text-to-image
- project（Recraft 官网/Studio/API）: https://www.recraft.ai
- github（第三方 ComfyUI 节点，经 API 调用，无 V4 模型细节）: https://github.com/recraft-ai/ComfyUI-RecraftAI

## 本地落盘文件

- ../../../sources/omni/2026/recraft-v4--blog.md
- ../../../sources/omni/2026/recraft-v4--docs.md
- ../../../sources/omni/2026/recraft-v4--choosing-a-model.md
- ../../../sources/omni/2026/recraft-v4--v4-1-docs.md
- ../../../sources/omni/2026/recraft-v4--aa-leaderboard-snapshot.md
- ../../../sources/omni/2026/recraft-v4--comfyui-readme.md
