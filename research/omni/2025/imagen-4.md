---
title: "Imagen 4 / Imagen 4 Ultra / Imagen 4 Fast"
org: "Google DeepMind"
country: US
date: "2025-05"
type: blog
category: t2i
tags: [text-to-image, diffusion, typography, imagen, google-deepmind, closed-source, synthid]
url: "https://deepmind.google/models/imagen/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/"
downloaded: [imagen-4--deepmind-model.md, imagen-4--blog-google-io-2025.md, imagen-4--vertex-ai-blog.md, imagen-4--vertex-model-docs.md, "gpt-image-1-mini-and-imagen-fast--imagen4-ga-googleblog.md (Imagen 4 全家桶 GA 公告，含 Fast 定价)"]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Imagen 4 是 Google DeepMind 第四代闭源文生图模型（2025 Google I/O 发布），在**文字渲染/排版**与**细节质量**上对前代 [[imagen-3]] 做了显著升级，支持**最高 2K 分辨率**与多宽高比，并以三档形态（标准 / Ultra / Fast，Fast 比 Imagen 3 快约 10×）覆盖"质量—速度—成本"权衡；作为闭源产品，其架构与训练细节**均未公开披露**，本页内容均来自官方博客与 Vertex AI 文档。

## 背景与定位
Imagen 系列是 Google 的旗舰文生图线：[[imagen]]（2022，基于级联扩散 + 大 T5 文本编码器）→ Imagen 2 → [[imagen-3]]（2024）。Imagen 4 于 **Google I/O 2025（2025-05-20）** 与 [[veo-3]]、Lyria 2 一同发布，定位"Google 最高质量的图像生成模型"。

它要解决的核心痛点是文生图长期的两块短板：
1. **文字与排版（typography）**——以往模型常拼错单词、无法在图内排布连贯长文本，难以直接产出海报/贺卡/漫画/演示稿等"带字"成品；
2. **细节保真**——精细纹理（织物、水珠、动物毛发）、光照、肤质等高频细节不够"可触摸"。

官方明确把 Imagen 4 的卖点压在"**stunning quality + superior typography**"上：显著改善拼写与排版、提升精细细节清晰度、原生支持多宽高比与最高 2K 分辨率（便于打印与演示）。在 Google 产品矩阵中，它是 Gemini app / Whisk / Vertex AI / Workspace（Slides、Vids、Docs）的底层图像引擎；与之并列的 [[nano-banana]]（Gemini 2.5 Flash Image）走"对话式生成 + 编辑"路线，而 Imagen 4 走"高质量纯文生图"路线。

> 注：本页是对一款**闭源产品**的分析。Imagen 4 **没有论文 / 技术报告 / GitHub / HuggingFace model card**；官方仅以博客 + API 文档形式披露能力与规格，工程内幕（架构、数据、训练、算力）几乎不公开。下文凡来源缺失处均明确标注"未披露"，不做任何臆测。

## 模型架构
**未披露。** 官方博客与 Vertex AI 文档均未公开 Imagen 4 的 backbone、文本编码器、tokenizer/VAE、参数量等任何架构信息。

可作背景的、**非 Imagen-4-专属**的已知线索（仅供脉络参考，不代表 Imagen 4 实现）：
- Imagen 初代采用"大语言模型文本编码器（T5-XXL）+ 级联扩散（base 64² → 超分到 256² → 1024²）"范式；Imagen 4 是否延续级联/扩散范式官方**未确认**。
- 从官方"up to 2k resolution"以及 Vertex 文档给出的两套分辨率档（1K 与 2K，见下表）来看，存在某种**多分辨率/超分**输出策略，但具体是级联超分还是原生高分扩散**未披露**。
- 文字渲染的大幅提升通常对应"更强文本编码器 + 高质量带字训练数据 + re-captioning"，但 Imagen 4 是否如此**未披露**。

**API 形态下可观测的规格（来自 Vertex AI 模型文档，GA 版本）：**

| 变体 | Model ID | 分辨率档（宽高比 → 像素） | 提示语言 |
|---|---|---|---|
| 标准 | `imagen-4.0-generate-001` | 1K：1:1=1024², 3:4=896×1280, 4:3=1280×896, 9:16=768×1408, 16:9=1408×768；**2K**：1:1=2048², 3:4=1792×2560, 4:3=2560×1792, 9:16=1536×2816, 16:9=2816×1536 | 英语；中(简/繁)、印地、日、韩、葡、西（preview） |
| Fast | `imagen-4.0-fast-generate-001` | **仅 1K**（同上 1K 档，无 2K） | 同上 |
| Ultra | `imagen-4.0-ultra-generate-001` | 1K + 2K（同标准档） | 同上 |

三档共同的接口限制：单请求最多返回 **4 张图**；输入图 ≤ **10 MB**；文生图提示文本上限 **480 token**。三档均支持**人像生成（preview）**、可配置安全过滤、SynthID 水印、以及 **prompt rewriter（提示重写器，preview）**；三档均**不支持**蒙版编辑/inpainting/outpainting/主体定制/风格迁移/upscale 等编辑能力（即 Imagen 4 是纯 t2i，编辑能力需走其他 Imagen 编辑模型或 Nano Banana）。

> 命名/时间线注记：I/O（2025-05-20）发布时只提到"标准 Imagen 4"与"即将推出的 Fast 变体"，并以 public preview 形式上 Vertex AI，preview 模型 ID 为 `imagen-4.0-generate-preview-05-20`（后另有 `imagen-4.0-generate-preview-06-06`）。**Imagen 4 Ultra** 是后续随 API GA 一并明确的"最高指令遵循精度"档，I/O 博客原文未点名 Ultra。Google Developers Blog 后续公告 **Imagen 4 全家桶（标准/Ultra/Fast）在 Gemini API 与 AI Studio 正式 GA**，并首发 Fast 档；GA 后模型 ID 统一为 `...-001`。

## 数据
**未披露。** 训练数据来源、规模、图文对数量、配比、清洗/过滤、标注与 re-captioning、合成数据占比、美学/安全过滤策略等**全部未公开**。官方仅以效果侧描述间接暗示数据侧的投入方向："significantly better at spelling and typography"（暗示带字/排版样本与标注的强化）、"remarkable clarity in fine details like intricate fabrics, water droplets, and animal fur"（暗示高分辨率、高质量细节样本）、多语言提示支持（暗示多语种图文数据）。具体数字一律无一手来源。

## 训练方法
**未披露。** 训练目标（diffusion / flow matching / 其它）、多阶段流程（预训练→continue→SFT→偏好对齐）、是否使用 RLHF/DPO/reward model、蒸馏与加速方案等**均未公开**。

可间接观察到的工程化痕迹（来自规格而非方法披露）：
- **Fast 变体"比 Imagen 3 快约 10×"**——强烈暗示采用了某种**步数蒸馏 / 加速采样**（consistency / ADD / LCM 一类），但官方**未确认**具体技术；且 Fast 仅支持 1K（牺牲 2K 高分辨率换速度）。
- **prompt rewriter / prompt enhancement**——API 侧内置提示重写器（preview），即在送入模型前用 LLM 扩写/规范化提示以提升出图质量与一致性；这是产品层能力，非模型训练细节。
- 三档（标准/Ultra/Fast）的差异在官方口径里是"质量 vs 速度 vs 成本"权衡：Ultra 主打**最高指令遵循/精度**，Fast 主打吞吐与延迟。三者是否同源蒸馏、是否独立训练**未披露**。

## Infra（训练 / 推理工程）
**训练 infra 未披露**（算力规模、GPU/TPU·时、并行策略、精度、吞吐均无公开数据；以 Google 体量推测多半基于 TPU，但官方未确认，不作断言）。

**推理/部署侧（可观测）：**
- 部署形态多样：Gemini app、Whisk、Vertex AI（Media Studio / Gen AI SDK）、Google Workspace（Slides/Vids/Docs）、Google AI Studio / Gemini API。
- Vertex 上提供**预配吞吐量（Provisioned Throughput）**与**动态共享配额（Dynamic Shared Quota）**两种用量模式（即企业可买断吞吐保延迟，或走共享池）。
- Fast 变体即"推理加速"的产品化体现：以约 10×（相对 Imagen 3）的速度服务"快速试错/批量探索"场景。
- **定价（仅 Fast 档有官方一手数字）**：Google Developers Blog 公布 **Imagen 4 Fast = $0.02 / 张输出图**（"low-latency images at just $0.02 per image"）；标准档与 Ultra 档的单价官方公告未给，需查 Vertex/Gemini API 定价页（本次未抓取，记为"未报告"）。
- 单请求至多 4 图、提示 ≤480 token、上传图 ≤10 MB 等为服务侧硬限制。

## 评测 benchmark（把效果讲清楚）
**官方未在博客/文档中报告任何量化基准数字**（无 FID / GenEval / DPG-Bench / T2I-CompBench / HPSv2 / ImageReward / PickScore 等指标，也未给出与同期 SOTA 的数值对比表）。Imagen 4 作为闭源产品，效果描述全部为定性：

- "Google 最高质量的图像生成模型"（Vertex 博客）；
- "outstanding text rendering and prompt adherence"（出色的文字渲染与提示遵循）；
- "remarkable clarity in fine details"（精细细节的卓越清晰度），擅长写实与抽象两类风格；
- 显著改善拼写与排版，可直接产出贺卡/海报/漫画等带字成品；
- 原生多宽高比 + 最高 2K 分辨率；
- 多语言提示支持（英、中简繁、印地、日、韩、葡、西）。

**第三方人评/Arena 数字（如 LMArena 文生图 ELO）在本次抓取的一手源中未出现**，故不在此列出具体排名/分数，以免编造。客户侧侧证（Vertex 博客引用 Klarna / Kraft Heinz / Envato 等）属营销案例，非可比基准。**结论：六维中"benchmark"维度官方数据缺失，记为"未报告"。**

## 创新点与影响
**核心贡献（产品/能力层面，非方法层面）：**
1. **把"文字与排版"从文生图老大难做到可用级**——拼写正确、可在图内排布连贯文本与版式，直接服务海报/贺卡/漫画/演示稿等"带字"生产场景，是 Imagen 4 相对前代最被强调的跃迁。
2. **质量—速度—成本三档产品化**（标准 / Ultra / Fast）：Ultra 追求最高指令遵循精度，Fast 以约 10×（vs Imagen 3）速度服务快速探索（GA 时定价 $0.02/图），覆盖从精修到批量的不同需求。
3. **原生 2K 多宽高比输出**：面向打印/演示等真实落地诉求（Fast 档为换速度而仅保 1K）。
4. **全量 SynthID 水印 + SynthID Detector**：所有输出携带不可见水印，配合 I/O 同期上线的检测门户，强化生成内容溯源——这是 Imagen 4 在"负责任生成"上的工程一等公民（SynthID 累计已水印 100 亿+图/视频/音频/文本）。

**影响：** 作为 Gemini app / Whisk / Workspace / Vertex 的底层图像引擎，Imagen 4 让"高质量带字图"在 Google 生态内规模化可用，与对话式编辑路线的 Nano Banana 形成"纯高质量文生图 vs 多轮编辑"的产品分工。

**已知局限：**
- **纯文生图，无原生编辑**（inpainting/outpainting/主体定制/风格迁移/upscale 均不支持，需另用编辑模型）；
- 提示上限仅 480 token、单请求至多 4 图；
- Fast 档不支持 2K；
- **架构/数据/训练/算力/基准全部不透明**，无法做学术级复现或横向定量对比；多语言均为 preview 级支持。

## 原始链接
- blog (DeepMind 模型页): https://deepmind.google/models/imagen/
- blog (Google I/O 2025 生成媒体发布): https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/
- blog (Vertex AI 发布 Veo3/Imagen4/Lyria2): https://cloud.google.com/blog/products/ai-machine-learning/announcing-veo-3-imagen-4-and-lyria-2-on-vertex-ai
- docs (Vertex AI Imagen 4 模型规格，含三档 model ID/分辨率/语言/限制): https://cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate
- blog (Google Developers — Imagen 4 全家桶 GA + Imagen 4 Fast 发布，含 $0.02/图 定价): https://developers.googleblog.com/en/announcing-imagen-4-fast-and-imagen-4-family-generally-available-in-the-gemini-api/

## 本地落盘文件
- ../../../sources/omni/2025/imagen-4--deepmind-model.md
- ../../../sources/omni/2025/imagen-4--blog-google-io-2025.md
- ../../../sources/omni/2025/imagen-4--vertex-ai-blog.md
- ../../../sources/omni/2025/imagen-4--vertex-model-docs.md
- ../../../sources/omni/2025/gpt-image-1-mini-and-imagen-fast--imagen4-ga-googleblog.md （Imagen 4 全家桶 GA + Fast 定价，文件名前缀沿用同批抓取的 work item）
