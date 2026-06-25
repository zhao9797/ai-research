---
title: "Veo 3 与 Veo 3.1"
org: Google DeepMind
country: US
date: "2025-05"
type: blog
category: video
tags: [video-generation, text-to-video, image-to-video, native-audio, audiovisual, diffusion, closed-model, google-deepmind, flow]
url: "https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://deepmind.google/models/veo/"
downloaded: [veo-3--blog-generative-media-io2025.md, veo-3--vertex-ai-announce.md, veo-3--deepmind-model.md, veo-3--deepmind-evals.md, veo-3--gemini-api-video-docs.md, veo-3--vertex-model-reference.md, veo-3-1--blog-veo-updates-flow.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Veo 3 是 Google DeepMind 于 2025 年 5 月 Google I/O 发布的旗舰视频生成模型，**首个能原生（natively）同步生成对白、音效与环境音的旗舰级文/图生视频模型**——"Video, meet audio"；基础版（`veo-3.0-generate-001`）输出 4/6/8 秒、720p/1080p、24 FPS、含精准对口型（lip sync）与真实物理表现，10 月迭代为 Veo 3.1（更强叙事控制 + 全功能音频 + 帧间编辑，并在 API 侧新增 4k 与多参考图/首尾帧/扩展），是 2025 年视频生成的事实标杆之一。

## 背景与定位
2024 年的视频生成军备竞赛（[[sora]]、[[movie-gen]]、[[kling]]、[[veo-2]]）已把"高保真无声短视频"做到可用，但几乎所有旗舰模型都**只出画面、不出声**——音频要么靠后期配，要么靠独立的"视频配音"模型二次生成，难以与画面口型/动作严丝合缝。Veo 3 的核心突破正在于此：在同一个生成过程内**原生联合生成视频与音频**（对白、音效、环境音、配乐），并做到对白与人物口型对齐（accurate lip syncing）。

定位上 Veo 3 是 [[veo-2]] 的直接升级：官方表述为"不仅在质量上超越 Veo 2，且首次能生成带音频的视频"。它面向影视/广告创作者，配套发布 AI 影视工具 **Flow**（聚合 Veo + [[imagen-4]] + Gemini）与 Imagen 4、Lyria 2，构成 Google "生成式媒体"全栈。相对前置工作，关键改进是把"视听"从"先生视频再配音"的两段式，变成**单模型联合生成的端到端视听**，并在物理真实感、提示词遵循上继续拉高。

技术脉络上，Veo 系列属于在隐空间做扩散/流匹配的视频生成范式（参见 [[latent-diffusion-ldm]] / [[ddpm]] 的扩散基底），但 Veo 3 的具体架构 Google **未公开论文/技术报告**，本页架构与训练细节多为基于官方博客+API 行为的推断，逐处标注。

## 模型架构
Veo 3 / Veo 3.1 是**完全闭源的商用产品**，Google **未发布技术报告、论文或 model card**，以下为一手官方材料能确证的部分，其余明确标注"未披露"：

- **能力形态**：单一模型同时支持文生视频（text-to-video）与图生视频（image-to-video），并在**同一次生成中联合产出视频帧与配套音轨**（对白/音效/环境音/配乐）。这意味着模型的生成目标空间包含视觉与音频两个模态，且二者需对齐（口型、动作—音效同步）——这是相对竞品最关键的架构层差异。具体的视听联合建模方式（是统一 token 序列、双分支扩散、还是音频条件/联合 latent）**官方未披露**。
- **backbone / tokenizer / text encoder**：**均未披露**。Veo 团队此前未公开 Veo 系列的 backbone 是 DiT 还是 U-Net、是否用 3D VAE、文本编码器用何种 LLM/T5。按 Google 一贯做法（[[imagen-3]]/[[imagen-4]] 用大语言模型做条件、视频走时空隐空间扩散）可合理推测 Veo 3 走"隐空间时空扩散 + 强语言条件"，但**无一手出处，本页不作为结论**。
- **参数量**：未披露。
- **分辨率与时长策略**（硬规格，来自 Vertex AI model reference 与 Gemini API 文档）：
  - **基础 Veo 3（`veo-3.0-generate-001`，及 Fast 档 `veo-3.0-fast-generate-001`）**：单段时长 **4 / 6 / 8 秒**（非"仅 8 秒"）；输出分辨率 **720p / 1080p**（基础版无 4K）；帧率 **24 FPS**；宽高比 **16:9 / 9:16**；单次最多产出 **4** 段；图生视频输入图片上限 20 MB；MIME `video/mp4`。Vertex 上为 **GA**，发布日 **2025-07-29**（I/O 首发时为 private preview）。
  - **Veo 3.1（`veo-3.1-generate-preview`，对应 Gemini API 文档）**：单段 **8 秒**；分辨率增至 **720p / 1080p / 4k**（4k 不支持 Veo 3.1 Lite 轻量版）；宽高比 16:9（默认）/ 9:16。视频"扩展/延伸"（extend）当前仅限 720p。
- **Veo 3.1 新增的条件注入能力**（官方文档/博客）：
  - **多参考图（最多 3 张）**："Ingredients to Video"，用人物/角色/产品/风格的参考图控制并保持主体外观一致性（可配合 [[gemini-2-5-flash-image-nano-banana]] 生成的参考图）。
  - **首尾帧控制**："Frames to Video"，给定起始帧与结束帧，模型生成桥接二者的连续视频（适合转场）。
  - **视频扩展（scene extension）**：在已生成的 Veo 视频基础上续接延长。
  - **场景内编辑**：Flow 内的 "Insert"（向场景中加入新元素，自动处理阴影与场景光照）与 "Remove"（移除对象并重建背景，发布时标注为 soon）。

## 数据
**完全未披露**。Google 没有公开 Veo 3 的训练数据来源、规模、视频—文本对数量、配比、清洗/过滤策略、re-captioning 流程，也未披露音频训练数据（如何获得"画面—声音"对齐的视听训练对，是该模型最关键、最被业界好奇的环节，官方只字未提）。官方仅强调与影视/音乐/艺术/YouTube 创作者"深度合作以负责任地塑造模型"，但未说明这是否进入训练集。美学/安全过滤未在数据层披露（安全见下文 Infra/安全段）。

## 训练方法
**未披露**。Google 没有公开训练目标（扩散 / 流匹配 / 自回归）、训练阶段（预训练→continue→SFT→偏好对齐）、是否使用 RLHF/DPO/reward model、以及任何蒸馏/步数加速方案。

可确证的间接信号：
- Veo 3.1 官方称"建立在 Veo 3 之上（builds on Veo 3），具有更强提示词遵循、在图生视频时更好的视听质量"——表明 3.1 是在 3 的基础上的迭代而非全新重训，但具体做法（继续训练 / 微调 / 数据扩充）未说明。
- "richer audio, more narrative control, enhanced realism, true-to-life textures"为 3.1 的官方卖点，属能力描述而非方法披露。

## Infra（训练 / 推理工程）
- **训练算力 / GPU·时 / 并行策略 / 精度 / 吞吐**：全部未披露。可合理假设训练与推理跑在 Google TPU 上（Google 自研全栈），但**无一手出处确认**。
- **推理与部署形态**（一手可确证）：异步长任务式 API——Gemini API 通过 `predictLongRunning` 提交后轮询 operation 状态（`operation.done`），完成后下载视频 URI；Vertex 侧模型 ID 家族含 `veo-3.0-generate-001` / `veo-3.0-fast-generate-001`（基础+Fast，均 GA）、`veo-3.1-generate-001` / `veo-3.1-fast-generate-preview` 等（preview 端点逐步并入 `-001` GA）。计费档：Vertex 支持 Provisioned Throughput 与 Standard pay-as-you-go（不支持 Fixed quota）。
- **可用渠道**：消费者侧 Gemini app（Veo 3 发布时仅限美国 Ultra 订阅用户）、AI 影视工具 Flow（Google AI Pro / Ultra 订阅，先美国后扩展）；开发者侧 Gemini API；企业侧 Vertex AI（发布时为 private preview，逐步放量）。
- **水印 / 溯源**：所有 Veo（及 Imagen 4 / Lyria 2）输出默认嵌入 **SynthID** 不可见水印；官方称 SynthID 自 2023 年已为超 100 亿（over 10 billion）张图像/视频/音频/文本加水印，并上线 SynthID Detector 验证门户。注：Vertex model reference 标注基础 Veo 3 **不支持 Content Credentials (C2PA)** 元数据标准（即只有 SynthID，无 C2PA）。
- **安全过滤**：输入提示与输出内容均经一组安全过滤器（Vertex 上过滤强度与"人物生成"控制可配置）。

## 评测 benchmark（把效果讲清楚）
**这是本工作披露最薄弱的一环。** Google 没有发布带数值表的技术报告；DeepMind 官网设有 Veo evals 页（`deepmind.google/models/veo/evals/`，本页已抓取快照），但其 MovieGenBench/人评胜率等对比**以 JS 图表/SVG 形式渲染，无法以文本形式抽取到具体百分比数字**，故本页**不给出胜率数值以免编造**。可确证的定性/规模数据：

- **核心定性卖点**（官方反复强调，属对比 Veo 2 的相对改进，非绝对分数）：更强真实感与保真度、真实世界物理、**精准对口型**、跨文本/图像提示的更好质量、显著更强的**提示词遵循（prompt adherence）**。
- **首创性主张**："for the first time, can also generate videos with audio"——旗舰模型中首个原生同步出音频（对白/音效/环境音）。
- **采用度 / 规模指标**（一手）：截至 Veo 3.1 发布（2025-10-15），AI 影视工具 **Flow 内累计生成超 2.75 亿（275 million）个视频**（官方脚注明确：该数含 Veo 2 与 Veo 3 两代生成量，非 Veo 3 单独）；企业客户案例中 Kraft Heinz 称创意流程从"8 周缩到 8 小时"，Brandtech/Jellyfish（David Jones）称试点平均降本 / 缩短上市约 **50%**（均为客户自述营销数据，非模型基准；另有 Klarna、Envato 等案例）。
- **第三方基准（FID/VBench/MovieGenBench 胜率、与 [[kling-2]]/[[sora-2]]/Runway 等的 head-to-head 数字）**：官方一手源**未以文本形式给出**，本页标注"未报告（仅图表形式）"。

> 说明：诸如 FID、VBench、CLIPScore 等学术指标在 Veo 3 的官方材料中均未出现——这是闭源旗舰产品的常态，Google 以"产品体验 + SynthID + 客户案例"替代了学术基准披露。

## 创新点与影响
**核心贡献**
1. **原生同步视听生成**：把"会动的画面"推进到"会动会响、且口型/动作—声音对齐"的视听片段，单模型一次生成对白+音效+环境音+配乐，免去二段式配音，是视频生成范式上的标志性一步。
2. **创作链路产品化**：以 Flow 把 Veo + Imagen + Gemini 串成"导演式"工作流（管理角色/场景/对象/风格"配料"，自然语言指挥分镜），Veo 3.1 进一步加入多参考图一致性、首尾帧桥接、场景延伸与帧内增删编辑，向"可迭代、可精修"的非线性创作靠拢。
3. **可信赖基建**：默认 SynthID 水印 + 安全过滤 + SynthID Detector，把生成式视频的溯源/合规做成默认项。

**影响**
- 重新定义了 2025 年视频生成的"及格线"：竞品（[[kling-2]]、[[sora-2]]、Wan 系列 [[wan-2-2]]、[[hunyuanvideo-1-5]]）此后纷纷把"原生音频/有声视频"列为关键卖点，"出声"从加分项变为标配方向。
- 把视频模型从"出片段"推向"出可编辑工程"（参考图一致性、首尾帧、增删对象），与图像侧的指令式编辑（[[gemini-2-5-flash-image-nano-banana]]）合流。

**已知局限**
- **几乎零方法透明度**：无论文/技术报告/model card，架构、数据（尤其视听对齐数据如何获取）、训练、算力全闭源，学术可复现性为零。
- 单段时长短（基础 Veo 3 为 4/6/8 秒，Veo 3.1 为 8 秒）；4k 与"扩展"等能力分档受限（扩展仅 720p，4k 仅 Veo 3.1 且不支持 Lite，基础 Veo 3 顶到 1080p）。
- 发布初期地域/订阅门槛高（美国 Ultra 起步）；编辑类能力（Remove/部分 API 功能）发布时仍为"soon/暂不可用"。

## 原始链接
- blog (I/O 2025 发布，主一手源): https://blog.google/innovation-and-ai/products/generative-media-models-io-2025/
- blog (Veo 3.1 发布 + Flow 更新): https://blog.google/innovation-and-ai/products/veo-updates-flow/
- blog (Vertex AI 企业侧发布，含能力清单/客户案例/安全): https://cloud.google.com/blog/products/ai-machine-learning/announcing-veo-3-imagen-4-and-lyria-2-on-vertex-ai
- product (DeepMind Veo 模型页): https://deepmind.google/models/veo/
- product (DeepMind Veo evals 页，含图表式人评对比，数值无法文本抽取): https://deepmind.google/models/veo/evals/
- docs (Gemini API 视频文档，含分辨率/时长/宽高比/模型ID 等硬规格): https://ai.google.dev/gemini-api/docs/video
- docs (Vertex AI Veo 3 模型参考，含 4/6/8s · 720p/1080p · 24 FPS · GA 2025-07-29 等硬规格): https://cloud.google.com/vertex-ai/generative-ai/docs/models/veo/3-0-generate-001?hl=en

## 本地落盘文件
- ../../../sources/omni/2025/veo-3--blog-generative-media-io2025.md
- ../../../sources/omni/2025/veo-3--vertex-ai-announce.md
- ../../../sources/omni/2025/veo-3--deepmind-model.md
- ../../../sources/omni/2025/veo-3--deepmind-evals.md
- ../../../sources/omni/2025/veo-3--gemini-api-video-docs.md
- ../../../sources/omni/2025/veo-3--vertex-model-reference.md （原中文快照仅含导航；审稿时已补抓英文版正文的 Veo 3 技术规格表）
- ../../../sources/omni/2025/veo-3-1--blog-veo-updates-flow.md
