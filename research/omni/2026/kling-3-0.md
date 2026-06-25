---
title: "可灵 3.0 系列模型（Kling 3.0：Video 3.0 / Video 3.0 Omni / Image 3.0 / Image 3.0 Omni）"
org: "快手（Kuaishou / 可灵 AI）"
country: China
date: "2026-02"
type: blog
category: video
tags: [video-generation, omni, multimodal, native-audio, multi-shot, character-reference, closed-source, kuaishou, kling]
url: "https://kling.ai/release-note/release-notes/whbvu8hsip"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://klingai.com"
downloaded: [kling-3-0--kuaishou-ir-press.md, kling-3-0--video-release-notes.md, kling-3-0--image-release-notes.md, kling-3-0--api-update-notice.md, kling-3-0--klingaio-blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
可灵 3.0 是快手 2026-02-05 全球上线的多模态视频/图片生成系列，核心是把"文生/图生/参考生/视频内编辑"等多任务统一进**单一原生多模态训练框架**（All-in-One），首次实现**原生音频 + 智能多镜头叙事 + 视频角色参考（Elements 3.0）**的端到端生成；最长 **15 秒**、支持中英日韩西五语种及方言口音的口型同步，图片侧原生 **2K/4K** 输出并引入视觉思维链（vCoT）。属闭源商业产品，**未发布技术报告/论文/权重**，故 infra、训练算力与定量 benchmark 均未披露。

## 背景与定位
可灵（Kling）自 2024-06 上线，是快手对标 [[sora]] / [[veo]] / [[seedance]] 的旗舰视频生成产品。截至 3.0 发布，官方披露累计服务全球 **6000 万+ 创作者**、生成 **6 亿+ 条视频**、合作 **3 万+ 企业客户**（Kuaishou IR 2026-02-05）。

3.0 的技术叙事是从"单模态拼接"转向"原生统一多模态"：
- 此前版本把音频、镜头控制、主体一致性当作**独立模块/后处理层**叠加；
- 3.0 把它们**统一进一个原生多模态训练框架**，对标 [[seedance]]、[[wan]]、谷歌 [[veo]] 的"导演模式 / 原生音画"路线，也呼应同期豆包 Seedance 2.0、Wan 2.7 的"统一生成-编辑"趋势。

版本对应关系（官方）：
- 视频 **2.6 → 3.0**（标准线）
- 视频 **O1 → 3.0 Omni**（高端参考线）
- 图片新增 **3.0 / 3.0 Omni**（其中 Image 3.0 Omni 由 IMAGE O3 演进，首引 vCoT）

定位口号："All in One, One for All" / "人人皆可当导演"。3.0 系列首发仅对 **Ultra 订阅用户**早期访问，随后向公众开放；API（开放平台）于 **2026-02-25** 上线 `kling-v3` / `kling-v3-omni`。

## 模型架构
> 注意：可灵闭源，**未公开 backbone（DiT/U-Net）、VAE/tokenizer、text encoder、参数量、扩散/flow 目标、分辨率分桶策略等任何架构细节**。以下为官方 release notes "Technical Approaches" 披露的**方法层**描述，非可验证的网络结构。

官方披露的三项视频侧技术路线（"VIDEO 3.0 Model Technical Approaches"，官方 release note）：

1. **原生多任务统一框架（Native Framework for Multi-Task）**：彻底重构底层架构与数据管线，原生支持多模态 prompt 的深度解析与跨任务融合；引入**统一的多模态 prompt 格式化方案（unified multimodal prompt formatting）**，使模型能解析复杂叙事逻辑，从而支撑长视频、灵活镜头控制与更高 prompt 遵循度。这是多镜头/长时长能力的关键使能技术。

2. **原生跨模态音频引擎（Native Cross-Modal Audio Engine）**：基于**跨不同模态的最优噪声采样区间（optimal noise sampling intervals across different modalities）**，新增**音频抽取与嵌入模块（audio extraction and embedding module）**；配合升级的端到端 prompt 参考系统，在音色保持与精确 prompt 参考上取得突破，实现音画深度一致。（"最优噪声采样区间"这一表述提示其底层为扩散/flow 类生成，但具体目标未说明。）

3. **多模态参考与解耦控制（Multimodal Reference & Decoupling Control）**：支持基于**视频参考**建主体、给主体绑定特定音色；通过**特征解耦与重组技术（feature decoupling and recombination）**，在不同场景间复杂、灵活地增删/编辑主体，保证主体与音视频特征在长视频中无缝融合。这是 Elements 3.0「视频角色参考」与跨场景一致性的核心。

图片侧（IMAGE O3 → Image 3.0 Omni）四项技术升级（"Technical Roadmap"，官方 release note）：

1. **视觉思维链 vCoT（Visual Chain-of-Thought）**：官方称"AI 生成领域首次"引入；生成前隐式做**场景拆解、常识推理、因果判断**（"先思考后渲染"），以处理抽象概念、结构化意图与复杂叙事逻辑。
2. **Deep-Stack 视觉信息流机制**：用 Transformer 动态融合细粒度感知信息与文本语义，获得**像素级**敏感度，精确还原复杂空间结构与微观纹理。
3. **叙事美学引擎**：新数据引擎 + 多维叙事框架（构图、视角、光影、情绪等），基于大规模定制数据集与精确图像描述，输出电影级画面。
4. **电影级 RL + 奖励模型**：见"训练方法"。

条件注入方式（多图/视频/音频参考、`@主体` 引用、storyboard 分镜参数）属产品交互层，官方未给网络级细节。

## 数据
官方仅给方法性描述，**规模/配比/清洗阈值/图文对数量等定量信息全部未披露**：
- 图片侧叙事美学引擎使用"**大规模定制数据集（large-scale customized dataset）+ 精确图像描述（re-captioning 性质）**"，覆盖构图、视角、光影、情绪等多维标注——指向系统性的电影化 re-caption 与美学维度标注，但未给数据量与来源。
- 视频侧称"重构底层架构**与数据管线**"，并提到**统一多模态 prompt 格式化**作为数据/输入侧关键改造，但未披露视频对数量、来源、采样、安全/版权过滤策略。
- 音频侧"audio extraction and embedding"模块依赖音视频配对数据训练以实现五语种 + 方言口音的口型同步，具体语料未披露。
- **结论：数据维度官方仅有定性叙述，无任何可引用的规模/配比数字（未披露）。**

## 训练方法
> 视频侧：官方**未披露**训练目标（diffusion / flow matching / rectified flow / next-token 等）、阶段划分（pretrain→SFT→对齐）、蒸馏/步数加速等任何细节。仅"optimal noise sampling intervals"一语暗示其为扩散/flow 类、并在多模态间做噪声调度，但无法据此断定具体损失。

图片侧官方明确披露了一条**强化学习 + 奖励模型**路径（"Technical Roadmap"第 4 点）：
- **电影级强化学习与奖励模型**：基于**真实感（realism）与电影质感（cinematic quality）双重奖励**，用 RL 注入美学偏好；
- 训练中对**权重平衡做动态优化（dynamic optimization of weight balancing）**，使模型从"视觉复现"演进到"叙事表达"。
- 这是一个典型的 **reward-model + RL（RLHF/偏好对齐类）** 后训练范式，但官方未给奖励模型规模、偏好数据量、算法（PPO/DPO/GRPO 等）与超参——均**未披露**。

vCoT 的"先思考后渲染"在训练上需要推理-生成联合监督，但官方未说明其训练形式（是否引入思维链监督数据 / RL）。蒸馏与加速：02 月发布的 3.0/3.0 Omni 未提加速蒸馏；2026-06-17 上线的 **Kling 3.0 Turbo**（"更快、更稳，端到端延迟降低，专为高频批量场景"）强烈暗示存在蒸馏/加速变体，但官方仅给定位话术，**未披露蒸馏方法与步数**。

## Infra（训练 / 推理工程）
**全部未披露**：官方未给训练算力规模、GPU·时、并行/分布式策略、混合精度、吞吐等任何训练 infra 信息（闭源产品常态）。

推理/部署侧可从 API 公告（官方开放平台）反推到的工程事实：
- **分辨率档位**：视频 3.0 标准/高品质模式，Omni 支持原生 **4K**（API 公告 2026-04-23：将 `mode` 参数置为 `4k` 即可生成 4K，每秒扣 3 积分）；3.0 Turbo 支持 **720P / 1080P** 文生/图生视频。
- **计费=按秒积分**（推理成本代理指标）：3.0/3.0 Omni 4K 每秒 3 积分；3.0 Turbo **720P 0.8 积分/秒、1080P 1.0 积分/秒**——Turbo 单价显著低于 4K 主模型，印证其面向高频批量的加速定位。
- **多镜头/参考参数**：`multi_shot=true` + `shot_type=intelligence` 触发智能分镜；参考视频时长 3～15s；建主体（Elements）升级为**异步服务**（`advanced-custom-elements` API），支持视频建主体 + 音色绑定。
- 部署形态：纯云端 SaaS（app.klingai.com / klingai.com）+ 开放平台 API，无本地权重/无端侧部署。

## 评测 benchmark（把效果讲清楚）
> **官方 release notes 与 IR 公告均未给出任何定量 benchmark**（无 VBench、无 ELO/Arena、无 FID/CLIPScore、无人评胜率）。可灵 3.0 是闭源产品发布，**没有可引用的一手定量评测数字**。唯一与外部模型对比的线索来自图片 release note 脚注：官方称构建了"覆盖不同参考类型与任务 prompt 的评测集"，并把 **IMAGE 3.0 Omni** 的文生图任务于 **1 月 26 日**、参考生图任务于 **1 月 31 日**与 **Dreamina 4.5** 做了对比——但**仅给对比对象与评测日期，未公开任何胜率/分数**（仍属"未报告"）。下列为官方声明的**定性能力**与**可核验的规格数字**，非 benchmark 分数：

可核验规格（官方 release notes / API）：
- **最长时长**：视频 3.0 / 3.0 Omni 均 **15s**（O1 上限为 10s，2.6 更短）；时长 3～15s 灵活可调。
- **多角色共指**：支持 **3+ 角色**共指（multi-character coreference），多角色多语言对话可指定内容、语调、发言顺序。
- **多语种口型**：中、英、日、韩、西 5 语种 + 英语多口音 + 中文方言；支持同场景双语对话（如游客用蹩脚西语问路）。
- **视频角色参考（Elements 3.0）**：上传/录制 **3–8s** 视频即可克隆角色外观 + 声音；多图建主体可额外上传 **≥3s** 音频抽取音色。
- **自定义分镜**：可逐镜头指定时长、景别、视角、叙事内容、运镜，单次生成拼成结构化多镜头叙事。
- **图片**：原生 **2K/4K** 直出；新增 **Image Series Mode**（单图/多图生成成组连贯故事板，支持批量统一优化）。

能力对比表（官方 release note，✅=新增/支持，❌=不支持）：

| 能力 | VIDEO 2.6 | VIDEO 3.0 | VIDEO O1 | VIDEO 3.0 Omni |
|---|---|---|---|---|
| 文生/图生/首尾帧/原生音频 | ✅ | ✅ | O1 无原生音频 | ✅ 原生音频+多镜头 |
| 多镜头 Multi-Shot | ❌ | ✅ | ❌ | ✅ |
| 多角色共指(3+) | ❌ | ✅ | — | ✅ |
| 多语种+方言口音 | ❌ | ✅ | — | ✅ |
| 视频角色参考(Video Element) | ❌ | ❌ | ❌ | ✅（上传/录制视频） |
| 主体音色控制 | ❌ | ❌ | ❌ | ✅ |
| 最长时长 | <15s | 15s | 10s | 15s |

**消融/对比结论：官方除"与 Dreamina 4.5 做过对比（仅给日期、无数字）"一句外，未提供任何带数字的对照实验，也无与 Veo/Sora/Seedance 等的定量对比；视频侧仅做自家版本能力勾选。第三方定量评测未在已抓取一手源中出现（未报告）。**

## 创新点与影响
**核心贡献（官方口径）**：
1. **原生统一多模态框架**：把文生/图生/参考生/视频内增删改统一进一个原生多模态训练模型，区别于"模块叠加"，是 3.0 全部新能力（多镜头、长时长、跨任务一致性）的底座。
2. **原生跨模态音频引擎 + 五语种方言口型**：把音频从"后处理"提到"原生生成"，并做到多语种/方言/多角色精确口型，是消费级 AI 视频里较激进的音画一体方案。
3. **Elements 3.0 视频角色参考**：用 3–8s 视频克隆角色的"动作 + 音色"，实现"数字分身"级表演一致性——比 O1 的静态多图参考前进一大步，是面向"自己出演 AI 短剧"的产品级杀手锏。
4. **智能/自定义多镜头分镜**：单次生成产出结构化多镜头叙事（正反打、交叉剪辑、旁白），把"导演调度"能力下放给普通用户。
5. **图片侧 vCoT + 电影级 RL**：把 LLM 式"先推理后生成"引入图像生成，配双奖励 RL 做电影化美学对齐。

**影响**：强化了 2026 年"视频生成 = 统一多模态 + 原生音频 + 导演级分镜"的行业范式（与 Seedance 2.0、Wan 2.7、Veo 同向竞争），把闭源商业视频模型的能力边界推到"15s 多镜头 + 音画同步 + 视频角色克隆"。后续 02-25 开放 API、03 月加动作控制 V3.0、06 月推 3.0 Turbo（低延迟批量）+ Omni 4K，形成完整商业化矩阵。

**已知局限 / 缺口**：
- **完全闭源**：无论文/技术报告/权重/HF/GitHub，架构、训练目标、数据规模、infra、定量 benchmark **全未披露**，技术可复现性为零，外部无法验证其方法主张。
- 时长仍限 15s；方言/口音的真实质量、长视频一致性的失败模式官方未量化。
- "vCoT""Deep-Stack""特征解耦"等均为官方营销化术语，**无网络结构或消融数据支撑**，需审慎引用。

## 原始链接
- ir-press (官方·最权威): https://ir.kuaishou.com/zh-hans/news-releases/news-release-details/keling30xiliemoxingquanmianshangxian （EN 版 .../kling-ai-launches-30-model-ushering-era-where-everyone-can-be）
- video-release-note (官方): https://kling.ai/release-note/release-notes/whbvu8hsip （= app.klingai.com/global/release-notes/whbvu8hsip）
- image-release-note (官方): https://kling.ai/release-note/release-notes/rz3idhopum
- api-update-notice (官方开放平台·落盘源实抓 URL): https://klingai.com/document-api/updates/api （另有镜像路径 .../apiReference/updateNotice）
- project_page (官方): https://klingai.com ；Omni 入口 https://www.klingai.com/app/omni/new
- klingaio-blog (第三方/二手，仅作交叉参考，非官方): https://klingaio.com/blogs/kling-3-release

## 本地落盘文件
- ../../../sources/omni/2026/kling-3-0--kuaishou-ir-press.md
- ../../../sources/omni/2026/kling-3-0--video-release-notes.md
- ../../../sources/omni/2026/kling-3-0--image-release-notes.md
- ../../../sources/omni/2026/kling-3-0--api-update-notice.md
- ../../../sources/omni/2026/kling-3-0--klingaio-blog.md （第三方二手快照，已在文件头标注 [THIRD-PARTY/SECONDARY]）
