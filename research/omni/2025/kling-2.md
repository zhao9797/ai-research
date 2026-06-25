---
title: "可灵 Kling 2.0 / 2.1 / 2.5 Turbo"
org: "快手 Kuaishou（可灵 Kling AI）"
country: China
date: "2025-04"
type: blog
category: video
tags: [video-generation, t2v, i2v, dit, closed-source, kuaishou, kling, mvl, video-editing]
url: "https://www.nasdaq.com/press-release/kling-ai-advances-20-era-empowering-everyone-tell-great-stories-ai-2025-04-15"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.klingai.com/"
downloaded: [kling-2--pr-20.md, kling-2--pr-21.md, kling-2--ir-25turbo.md, kling-2--ir-revenue.md, kling-2--api-doc-models.md, kling-2--about.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
快手可灵第二代视频生成模型族（2.0 / 2.1 / 2.5 Turbo，2025 年 4–9 月陆续上线），以 **DiT（Diffusion Transformer）视频底座 + 多模态视觉语言（MVL）交互 + 多模态视频编辑** 为核心卖点，把运动质量、语义遵循与镜头/编辑可控性提升到 2025 年闭源视频第一梯队——官方盲测中 2.0 图生视频对 Google Veo2 胜负比 182%、对 Runway Gen-4 178%；2.5 Turbo 文生视频对 Seedance 1.0 mini / Veo3-fast / Seedance 1.0 胜负比达 285% / 212% / 160%，同时单价比 2.1 再降约 30%。

## 背景与定位
可灵（Kling）2024 年 6 月上线，是官方所称"全球首个面向用户开放的 DiT 视频生成模型"，也是中国首个面向 C 端与专业创作者的付费 AI 视频工具。截至 2025 年 4 月 2.0 发布时全球用户已超 2200 万，企业 API 客户过万。第三方基准 Artificial Analysis 2025-03-27 榜单上，可灵 1.6 Pro（高品质模式）以 Arena ELO 1000 位列图生视频第一，Veo2、Pika 居二三位——这是 2.0 发布的竞争背景。

第二代不是单点升级，而是一条快速迭代的产品线（官方称至 2.5 Turbo 已累计 30+ 次迭代）：
- **2.0（2025-04-15，"从想象到银幕"发布会，北京）**：底座大升级 + 提出 MVL 交互范式 + 多模态视频编辑 + Master 版；同场发布图像模型 Kolors（可图）2.0。
- **2.1（2025-06-04）**：主打"高质量 × 高性价比 × 高速度"，大幅降价提速。
- **2.5 Turbo（2025-09-23 上线，09-26 公告）**：再一次质量跃迁 + 再降价约 30%，并对标字节 Seedance 1.0 与 Google Veo3。

技术脉络上，可灵属于潜空间扩散视频生成路线，与 [[latent-diffusion-ldm]]、[[ddpm]]、Sora 类 [[dit-scalable-diffusion-transformers]] 视频模型同源，但走的是闭源产品化 + 强工程迭代 + 强编辑/可控性路线，而非发表论文。它与同期 Veo（Google）、Runway Gen-3/4、Seedance/Seaweed（字节）、Hailuo/MiniMax、Wan（阿里）正面竞争。

> 注意边界：本页覆盖到 2.5 Turbo。2025 年 12 月初"Omni Launch Week"发布的 Kling Video O1（首个统一多模态视频模型）、Kling Image O1、Kling Video 2.6（音画同生）、可灵数字人 2.0 属下一代统一/全模态工作，归入 [[kling-omni]] 等独立条目，本页不展开。

## 模型架构
快手对可灵底座**未发表技术报告或论文**，架构细节多来自官方发布会口径与开发者文档，工程内部实现未披露。可确证要点：

- **骨干：Diffusion Transformer（DiT）**。官方在 2.0 发布稿中明确称可灵为"全球首个面向用户开放的 DiT 视频生成模型"（pr-20），即采用 Transformer 替代 U-Net 作为扩散去噪骨干。这是落盘源里唯一可确证的架构事实；**具体层数、注意力设计、参数量官方均未披露**（3D VAE / 3D 时空压缩等更细的底座结构常见于第三方解读，但无官方一手依据，本页不作事实陈述）。
- **多模态视觉语言 MVL（Multi-modal Visual Language）**：2.0 引入的核心交互/条件注入范式。官方把 MVL 拆为两部分（pr-20）：**TXT（Pure Text，纯文本）** 与 **MMW（Multi-modal-document as a Word，把多模态文档当作一个"词"）**，前者设定生成的基础方向、后者做精细化控制。把文本之外的**图像参考、视频片段**（官方称 MMW 将进一步扩展到**声音、运动轨迹**）作为统一的"视觉语言"输入，用来表达身份、外观、风格、场景、动作、表情、镜头运动等创作意图。本质是把多模态条件统一编码后注入生成过程，使"复杂创意意图"能直接、精确传达给模型，而非只靠 prompt 文本。这是 2.x 区别于纯 T2V 模型的关键产品/交互设计（注：官方仅给出交互范式描述，未公开 MVL 在模型侧的条件编码/注入实现）。
- **多模态视频编辑**：基于 MVL，2.0 Master 版支持对已生成视频中的元素做"增/删/改/替换"——用户给一段视频片段，再用图像或文本指定要添加、删除或替换的内容元素即可。属生成式视频编辑能力，需要模型在条件注入侧支持局部内容编辑与一致性保持。
- **图像底座 Kolors（可图）2.0**：与视频模型协同发布。官方称图生视频占可灵创作量约 85%，故图像质量直接决定视频效果。Kolors 2.0 强化复杂语义理解、电影级画质、可控风格化生成，支持局部重绘、扩图、风格化转录（一键换艺术风格并保留语义内容）。
- **模型版本编号（开发者 API 口径）**：官方 `model_name` 枚举确证第二代家族包含 `kling-v2-master`、`kling-v2-1`、`kling-v2-1-master`、`kling-v2-5-turbo`（更早为 v1/v1-5/v1-6，更晚为 v2-6/v3）。即 2.0 与 2.1 均区分"标准/Master"档，2.5 走"Turbo"加速档。文生视频与图生视频共用该模型族。

**未披露**：tokenizer/VAE 压缩比与具体结构、text encoder 选型（T5/CLIP/LLM）、参数量、原生分辨率与训练分辨率策略、注意力实现（full/window/factorized）等架构细节官方均未公开。

## 数据
**完全未披露**。快手未公开可灵 2.x 的训练数据来源、规模、图文/视频对数量、配比、清洗过滤、re-captioning、合成数据、美学与安全过滤等任何细节。可间接参考的背景：快手自有海量短视频内容生态（MAU 7.12 亿、DAU 4.41 亿，1Q25），通常被认为是其视频数据来源优势，但官方未确认用于训练，**不作事实陈述**。

## 训练方法
**几乎未披露**。官方仅给出能力层面的定性描述，未公开训练目标（diffusion / flow matching 等）、多阶段流程（预训练→继续训练→SFT→偏好对齐）、是否用 RLHF/DPO/reward model、蒸馏与步数加速方案、关键超参。可确证的"对齐/评测方法学"线索：

- **评估方法学**：官方采用 **GSB（Good-Same-Bad）** 与专业人评盲测（blind test）作为内部多指标评测口径，并据此报告"胜负比（win-loss ratio）"。这说明其迭代以人类偏好对齐为导向，但具体是否将偏好信号回灌入训练（reward model / RLHF）未说明。
- **2.5 Turbo 的"Turbo"**含义官方未技术性展开，从"质量提升 + 单价降约 30% + 高品质模式 <1 分钟出片"推断包含推理加速/蒸馏类优化，但**官方未确认采用 consistency/LCM/步数蒸馏等具体方案**，此处不做断言。

## Infra（训练 / 推理工程）
**训练侧未披露**（算力规模、GPU·时、并行/分布式、精度、吞吐均无官方数据）。推理/部署侧可确证的工程指标：

- **速度**：2.1 高品质模式下 5 秒视频渲染"不到 1 分钟"，官方称领先同业。
- **成本/计费**（推理经济性是 2.x 的明确工程目标）：
  - 2.1：5 秒视频 = 20 灵感值（720p）/ 35 灵感值（1080p）。
  - 2.5 Turbo：每个 5 秒 1080p 视频 25 灵感值，较 2.1 的 35 灵感值降约 30%。
- **部署形态**：Web（klingai.com / kling.ai，全球站已迁至 kling.ai）+ 移动端 App（iOS/Android）+ 开发者 API（`model_name` 指定版本，支持 T2V/I2V、multi_prompt 分镜、负向提示等）。企业通过 API 集成，合作方包括小米、AWS、阿里云、Freepik、蓝色光标等。

## 评测 benchmark（把效果讲清楚）
官方主要以**内部专业人评盲测的胜负比（win-loss ratio）**报告效果（A 对 B 胜负比 = 胜场/负场，>100% 即占优），均来自快手官方稿件，第三方独立复现数字有限。

**Kling 2.0（图生视频 I2V，内部 GSB/多指标评测）**：
- 对 Google **Veo2**：胜负比 **182%**。
- 对 Runway **Gen-4**：胜负比 **178%**。
- 优势维度：语义响应（semantic responsiveness）、视觉质量、动态质量。
- 第三方背景（非 2.0 本身）：发布前 Artificial Analysis 2025-03-27 榜单，可灵 1.6 Pro 高品质模式以 Arena ELO **1000** 居图生视频第一（Veo2、Pika 二三位）。

**Kling 2.5 Turbo（专业人评盲测）**：
- 文生视频 T2V 胜负比：对 **Seedance 1.0 mini 285%**、对 **Veo3-fast 212%**、对 **Seedance 1.0 160%**。
- 图生视频 I2V 胜负比：对同样三者分别 **208% / 289% / 164%**。
- 提升维度（官方定性）：prompt 遵循（能处理复杂多步指令与因果关系）、运动表现（更大幅度运动与镜头运动、更准的真实物理模拟，擅长格斗/奔跑+镜头跟拍、花滑/花游/群舞等复杂动作）、风格一致性（更准捕捉参考图色彩/光照/纹理/氛围）、美学质量（光影与构图）。

**图像模型 Kolors 2.0**：官方称在多次内部胜负比评审中对 Midjourney V7、FLUX 1.1 Pro、Reve 等业界领先图像模型保持显著优势（具体数字未给）。

**说明/局限**：以上数字均为快手**内部盲测胜负比**，非公开学术基准（无 VBench / FID / FVD / CLIPScore 等标准指标的官方报告，**官方未报告**这些）。胜负比依赖评测集与评委构成，跨厂商可比性有限，应作"官方自报"看待。本页未抓到 2.0/2.1/2.5 在 VBench 等公开 leaderboard 的官方数字（gap）。

## 创新点与影响
**核心贡献**
- **MVL（多模态视觉语言）交互范式**：把"用图像/视频/声音/运动轨迹+文本统一表达创意意图"产品化，重新定义了视频生成的人机交互语言，是 2.x 最具辨识度的方法/产品创新。
- **多模态视频编辑**：在生成式视频上做元素级"增删改替"，把可灵从"一次性出片"推向"可迭代编辑"的创作工具。
- **质量×成本双轮迭代**：2.0 抓质量天花板，2.1/2.5 Turbo 抓性价比与速度（2.5 Turbo 单价较 2.1 降 ~30%、5s/1080p 仅 25 灵感值），把高质量视频生成的使用门槛持续压低。

**影响（官方披露的商业/生态数据）**
- 商业化：1Q25 可灵单季收入超 1.5 亿元（近 70% 来自付费订阅）；**ARR 2025-03 达 1 亿美元（上线 10 个月）→ 2025-12 达 2.4 亿美元（上线 19 个月）**。
- 生态规模（截至 2025-12）：服务 **6000 万+ 创作者**、累计生成 **6 亿+ 视频**、合作企业 **3 万+**。
- 行业落地：广告营销、专业创作、影视短剧、动画、游戏、智能设备等；驱动全球首部 AI 生成剧集《New World Is Loading》（播放 2 亿+），并受邀在釜山国际电影节 ACFM 预览 2.5 Turbo。

**已知局限**
- 闭源、无技术报告，架构/数据/训练/infra 工程细节几乎全部不可见，复现与独立评估困难。
- 官方评测只给内部盲测胜负比，缺乏公开标准基准的可比数字。
- 物理一致性、复杂动作稳定性虽逐代改善，但官方亦承认 AIGC 视频在稳定性与复杂创意精确表达上"仍有诸多挑战"。

## 原始链接
- pr-2.0（官方 GlobeNewswire 经 Nasdaq）: https://www.nasdaq.com/press-release/kling-ai-advances-20-era-empowering-everyone-tell-great-stories-ai-2025-04-15
- pr-2.1（Kuaishou 经 EQS Newswire）: https://www.eqs-news.com/news/corporate/ai-emerges-as-a-mid-to-long-term-growth-engine-kling-2-1-sets-new-standard-for-cost-efficient-video-generation/da7c7b5a-8054-454a-9992-74436bdb6a03_en
- ir-2.5 Turbo（Kuaishou 投资者关系官网）: https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-launches-25-turbo-video-model-industry-leading
- ir-revenue（ARR 里程碑 + Omni Launch Week 背景）: https://ir.kuaishou.com/news-releases/news-release-details/kling-ai-annualized-revenue-run-rate-hits-usd240-million/
- 开发者 API 文档（model_name 版本枚举）: https://app.klingai.com/cn/dev/document-api/apiReference/model/imageToVideo
- 产品首页（落盘的 about.md 实际抓取的是 kling.ai 首页，非 /about）: https://kling.ai/ ， https://www.klingai.com/
- 列于 worklist 但未能获取（登录/区域门控、SPA 仅渲染外壳）: https://app.klingai.com/global/release-notes

## 本地落盘文件
- ../../../sources/omni/2025/kling-2--pr-20.md
- ../../../sources/omni/2025/kling-2--pr-21.md
- ../../../sources/omni/2025/kling-2--ir-25turbo.md
- ../../../sources/omni/2025/kling-2--ir-revenue.md
- ../../../sources/omni/2025/kling-2--api-doc-models.md
- ../../../sources/omni/2025/kling-2--about.md
