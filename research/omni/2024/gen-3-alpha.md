---
title: "Runway Gen-3 Alpha"
org: "Runway"
country: US
date: "2024-06"
type: blog
category: video
tags: [text-to-video, image-to-video, video-generation, closed-source, world-model, diffusion, c2pa]
url: "https://runwayml.com/research/introducing-gen-3-alpha"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://runwayml.com/research"
downloaded: [gen-3-alpha--blog.md, gen-3-alpha--blog.html, gen-3-alpha--prompting-guide.md, gen-3-alpha--creating-t2v-i2v.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Gen-3 Alpha 是 Runway 2024-06-17 发布的**新一代视频基础模型**，在「新搭建的大规模多模态训练基础设施」上、用**视频与图像联合训练**得到，相比 [[gen-2]] 在**保真度、一致性、运动**上大幅提升，并被官方定位为「迈向通用世界模型（General World Models, GWM）的一步」。它是当时商用视频生成的代表产品，但**完全闭源**：无论文、无技术报告、无模型卡、无 benchmark 披露——本页所有内容均来自官方博客与官方帮助文档，架构/数据/训练/infra/评测的具体方法与数字**官方均未公开**，凡未披露处一律如实标注。

## 背景与定位
**解决的问题**：Gen-2（2023）虽率先把文/图生视频做成可商用产品，但运动幅度小、时间一致性弱、人物表情与镜头语言难控。Gen-3 Alpha 的目标是把生成质量推到「电影级」并强化可控性。

**技术脉络中的位置**：
- 它对标的是 2024 年初 OpenAI [[sora]] 演示所确立的「DiT 长视频生成」范式，以及同期的 [[stable-video-diffusion]]、Pika、Luma Dream Machine、快手可灵（Kling）、[[cogvideox]]（开源对照组）。
- Runway 自身脉络：Gen-1（视频到视频，2023-02）→ Gen-2（文/图生视频，2023）→ **Gen-3 Alpha（2024-06，blog 标注 June 17, 2024）**，随后推出加速版 **Gen-3 Alpha Turbo**（落盘源未给出 Turbo 发布日期，业界为 2024-07），再到 Gen-4 / Gen-4.5（Gen-4.5 见落盘源 EOL 公告中的替代项）。
- 官方明确把 Gen-3 Alpha 归入「Gen-3 系列模型家族」，并作为通往 **General World Models（能模拟一切可能世界与经验的基础模型）**愿景的一步——这是 Runway 区别于纯「视频生成工具」厂商的研究叙事。

**相对前置工作（Gen-2）的改进**（官方博客原话）：fidelity（保真度）、consistency（一致性）、motion（运动）三方面的「major improvement」；新增**高度描述性、时间上密集（temporally dense）的字幕**带来的细粒度时间控制；显著增强的**写实人物**生成能力。

## 模型架构
**官方未披露。** 博客与帮助文档**未公开** backbone 类型（U-Net / DiT / 自回归）、visual tokenizer / VAE、text encoder、参数量、注意力设计、条件注入等任何架构细节。

可从一手材料确证的、与架构相关的事实仅有：
- **多模态联合训练**：模型「在视频和图像上联合训练（trained jointly on videos and images）」，因此同一基础模型同时驱动 Runway 的 **Text to Video、Image to Video、Text to Image** 三类工具。
- **统一基座驱动多种控制模式**：同一 Gen-3 Alpha 支撑 Motion Brush、Advanced Camera Controls、Director Mode 等现有控制模式，以及后续对**结构、风格、运动**做更细粒度控制的工具。
- **图生视频条件**：输入图像默认作为视频**首帧**（Turbo 上必填，Alpha 上可选）；关键帧（Keyframes）模式 Alpha 支持「首帧或末帧」，Turbo 支持「首/中/末帧」。

> 推断（非官方）：业界普遍认为 Gen-3 属潜空间扩散 + Transformer（DiT 类）路线，但 Runway 从未在任何一手渠道证实，故本页**不作架构断言**。

## 数据
**规模、来源、配比、清洗过滤、合成数据等均未披露。** 官方仅给出两条与数据/标注相关的确定信息：

1. **视频+图像联合数据**：模型「jointly trained on videos and images」，但具体图文/视频对数量、数据来源与采集方式**未公开**（Runway 因训练数据来源问题长期受外界争议，官方始终未披露语料构成）。
2. **时间密集字幕（核心数据工程）**：Gen-3 Alpha「以**高度描述性、时间上密集的字幕（highly descriptive, temporally dense captions）**训练」，正是这一标注方式带来了「富有想象力的转场」与「场景中元素的精确关键帧化（precise key-framing）」——即模型能理解 prompt 中「先……然后……」的时序描述。这与 [[dall-e-3]]、Sora 等「用合成 re-caption 提升 prompt 跟随」的思路同源，但 Runway 未公开 caption 的生成模型、长度或覆盖率。

美学过滤、安全过滤、去重等数据处理细节**官方未报告**。

## 训练方法
**训练目标、阶段划分、偏好对齐、蒸馏加速等均未披露。** 帮助文档给出的训练目标函数（diffusion / flow matching / next-token）、是否有 SFT / RLHF / DPO、是否做步数蒸馏等**官方一概未说明**。

可确证的训练叙事仅有：
- **新基础设施上训练**：Gen-3 Alpha 是「Runway 在**为大规模多模态训练新建的基础设施**上训练的下一代基础模型中的第一个」——说明这是一次从头搭训练栈的工作，但该基础设施的规模/形态未公开。
- **跨学科协作训练**：官方强调训练是「研究科学家、工程师与**艺术家**组成的跨学科团队的协作成果」，并刻意让模型能解读**广泛的风格与电影术语（cinematic terminology）**——这指向训练/标注阶段对镜头语言（如 FPV、tracking shot、low angle、50mm lens、lens flare 等，见下文 prompt 关键词体系）的针对性对齐，但无方法层面的披露。
- **加速版 Turbo**：**Gen-3 Alpha Turbo** 被官方帮助文档描述为「Gen-3 Alpha 家族中更快、成本更低的模型（a faster model… that generates at a lower cost）」，价格为 Alpha 的一半（Alpha 10 credits/秒 → Turbo 5 credits/秒，二者均见落盘 spec 表）；落盘源只说「更快」，**未给出具体加速倍数**。这强烈暗示采用了某种推理加速/蒸馏，但 Runway **未公开** Turbo 的加速方法（是否 consistency / 步数蒸馏 / ADD 等均未说明）。

## Infra（训练 / 推理工程）
**训练算力、GPU·时、并行策略、混合精度、吞吐均未披露。** 仅有定性表述「为大规模多模态训练新建的基础设施（new infrastructure built for large-scale multimodal training）」。

推理/部署形态（来自官方帮助文档，确定）：
- **部署形态**：纯云端 SaaS，无本地权重；落盘 spec 表列出的平台为 **Web、iOS**（Runway 另有 API，但不在该 spec 表的「Platform availability」中）。文本输入上限 **1000 字符**（spec 表）。
- **生成规格**（Gen-3 Alpha）：时长 **5 秒或 10 秒**（默认 10s）；输出分辨率 **1280×768**；帧率 **24 fps**；计费 **10 credits/秒**。
- **视频扩展**：单条最多续接 3 次，每次 5 或 10 秒增量，**最长可扩展到 40 秒**；扩展时自动以上一段末帧为输入。
- **Turbo 对照**：分辨率 1280×768 与 768×1280（竖屏）；扩展增量 8 秒、最长 34 秒；5 credits/秒；输入图像必填。
- **生命周期**：官方公告 Gen-3 Alpha / Turbo 将于 **2026-07-30 下线**，由 Gen-4.5 等替代——一手快照保留了这一 EOL 信息。

## 评测 benchmark（把效果讲清楚）
**Runway 未发布任何定量 benchmark。** 官方博客与帮助文档中**没有** FID、CLIPScore、GenEval、VBench、人评 ELO/Arena 等任何数字，也没有与 Sora / Kling / Pika 的量化对比。本页**不引用第三方评测数字**（非一手源），以免与「数字必须来自已抓取一手源」的要求冲突。

官方给出的、仅为定性的效果主张（来自博客）：
- **相对 Gen-2 的「major improvement」**：保真度、一致性、运动三维定性提升（无数字）。
- **细粒度时间控制**：依托时间密集字幕，可做想象力转场与精确关键帧（示例 prompt：「一只蚂蚁从巢穴钻出，镜头后拉揭示山丘外的街区」「以 10 倍速第一人称冲向房屋前门」）。
- **写实人物**：擅长生成富表现力的人物，覆盖广泛动作、手势与情绪（多条人物特写示例）。
- **风格与电影语言广度**：可解读油画、日式动画、定格、微距等多种风格与镜头术语。
- **行业定制**：与头部影视/媒体机构合作，提供可定制（custom / fine-tuned）版本，用于更受控且一致的角色与特定叙事需求——但定制方法、数据量、效果均未公开。

> 说明：所有页面上的示例视频均由 Gen-3 Alpha 直接生成、官方声明「无任何修改」，但这是定性展示，非可复现 benchmark。

**Prompt 接口（官方帮助文档，体现可控性设计）**：
- 推荐结构 `[camera movement]: [establishing scene]. [additional details].`，并强调**正向描述**（不支持 negative prompt，写「晴朗蓝天」而非「天空无云」）、**描述式而非对话/命令式**。
- 内置丰富**镜头/光线/运动关键词体系**：镜头如 Low/High angle、Overhead、FPV、Handheld、Wide angle、Macro、Over the shoulder、Tracking、50mm lens、SnorriCam；光线如 Diffused、Silhouette、Lens flare、Back/Side lit、gel lighting——印证了「训练阶段针对电影术语对齐」的叙事。

## 创新点与影响
**核心贡献（基于一手定性材料）**：
1. **时间密集字幕驱动的时序可控性**：把「细粒度时间控制 / 精确关键帧」做成可用产品能力，是 Gen-3 相对前代最被强调的进步，也代表了 2024 年视频生成「靠高质量密集 caption 提升时序与 prompt 跟随」的共识方向（与 Sora / DALL·E 3 同源思路）。
2. **统一多模态基座 + 多控制模式**：一个联合训练的基础模型同时驱动 T2V / I2V / T2I 与 Motion Brush、相机控制、Director Mode 等，把「视频生成」从单点功能扩展为可控创作工作流。
3. **商用化与安全合规先行**：发布即配套**新的自研视觉审核系统**与 **C2PA 内容溯源标准**，在生成视频的来源标注/合规上走在前列。
4. **世界模型叙事**：把视频生成明确纳入「通用世界模型（GWM）」研究路线，影响了后续行业把视频生成与世界模拟/具身智能联系起来的叙事（Runway 后续推出 GWM-1）。

**对后续工作的影响**：Gen-3 Alpha（及其 Turbo）是 2024 下半年商用视频生成的标杆之一，与可灵、Luma、Pika、[[cogvideox]]（开源侧）共同把「电影级 10 秒可控视频」推向大众，并直接演进为 Gen-4 / Gen-4.5。

**已知局限 / 待澄清**：
- 单次最长 10 秒、需多次扩展才能到 40 秒，长视频一致性仍依赖续接；
- **完全闭源、零技术披露**：架构、数据来源、训练目标、算力、benchmark 全部未公开，外界无法复现或独立核验，数据来源亦长期受争议；
- Turbo 的加速方法未说明。

## 原始链接
- blog（一手，主源）: https://runwayml.com/research/introducing-gen-3-alpha
- prompting-guide（官方帮助文档）: https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide
- creating-t2v-i2v（官方规格文档）: https://help.runwayml.com/hc/en-us/articles/30266515017875-Creating-with-Text-Image-to-Video-on-Gen-3-Alpha-and-Turbo
- research-index（GWM 叙事来源）: https://runwayml.com/research

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gen-3-alpha--blog.md)
- [blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gen-3-alpha--blog.html)
- [prompting-guide.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gen-3-alpha--prompting-guide.md)
- [creating-t2v-i2v.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gen-3-alpha--creating-t2v-i2v.md)
