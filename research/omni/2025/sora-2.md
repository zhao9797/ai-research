---
title: "Sora 2"
org: OpenAI
country: US
date: "2025-09"
type: system-card
category: video
tags: [video, audio, text-to-video, world-model, diffusion, synced-audio, cameo, closed-source]
url: "https://openai.com/index/sora-2/"
arxiv: ""
pdf_url: "https://cdn.openai.com/pdf/50d5973c-c4ff-4c2d-986f-c72b5d0ff069/sora_2_system_card.pdf"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://sora.com"
downloaded: [sora-2--blog.md, sora-2--system-card.md, sora-2--system-card-full.md, sora-2-system-card.pdf, sora-2--launching-responsibly.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Sora 2 是 OpenAI 2025 年 9 月发布的第二代旗舰**音视频联合生成模型**——首次实现与画面**原生同步的对白/音效音频**、显著更强的物理一致性（投篮不中会真实反弹而非"瞬移进筐"）和多镜头可控性，被官方定位为视频生成的"**GPT-3.5 时刻**"；配套发布以"角色（cameo）"为核心的 Sora 社交 iOS App。技术细节几乎全部未披露（无论文、无技术报告、无权重），下文严格区分"官方明确陈述"与"未披露"。

## 背景与定位
- **解决的问题**：把视频生成从"会动但反物理"推进到"能模拟失败、遵守动力学"的世界模拟器方向，并补齐前代缺失的**音频**模态，使单模型一次生成画面+对白+环境声+音效。
- **技术脉络**：OpenAI 将 2024-02 的初代 [[sora]]（[[openai-sora-1-public]]）类比为视频生成的"GPT-1 时刻"——首次证明"扩展预训练算力"能在视频上涌现物体持久性等简单行为；Sora 2 自比"GPT-3.5 时刻"，强调继续扩大视频神经网络规模带来质变。官方反复将其框定为通往"通用世界模拟器 / 物理世界 AI"的里程碑，而非单纯的内容生成工具。
- **相对前作的改进**（官方陈述）：更精准的物理（physical accuracy）、更高真实感（sharper realism）、**音画同步音频**、更强可操控性（steerability，可遵循跨多镜头的复杂指令并保持世界状态一致）、更广风格范围（写实/电影感/动漫）。一个被强调的定性观察：模型的"错误"更像是其隐式建模的**内部智能体**所犯的错误，而非画面层面的崩坏——即它开始模拟"失败"而非只模拟"成功"。
- **同期对手**：与 Google [[veo-2]]（及更新的 Veo 3 同样主打原生音频）、Meta [[movie-gen]]、快手 [[kling-2]]、字节 [[seedance-1-0]]、腾讯 [[hunyuanvideo-1-5]] 同处 2025 视频生成第一梯队；Sora 2 与 Veo 3 一道把"**带同步音频**"确立为该代视频模型的新基线能力。

## 模型架构
**官方未披露任何架构细节**——没有论文、技术报告或 model card 公开 backbone、tokenizer、文本编码器、条件注入方式或参数量。以下为基于官方公开陈述可确认/合理推断的范围，并明确标注性质：

- **可确认（官方陈述）**：
  - 是**单一的音视频联合生成模型**（"general-purpose audio-video generation system"），同一模型产出视频与**时间对齐的对白/音效/背景声场**，而非视频+独立配音管线。
  - 支持**文生视频**、**图生视频**（含照片上传，发布期对"含写实人物的图片上传"做限制）；发布时**不支持视频到视频（video-to-video）**。
  - 支持 **cameo / 角色**：用户在 App 内做一次简短音视频录制采集肖像+声纹后，可在任意生成场景中高保真复现其外貌与声音；该能力"对任何人、动物或物体通用"，即一种基于参考的身份/外观注入机制（具体实现未公开）。
  - 提供更高画质/性能的实验版 **Sora 2 Pro**（面向 ChatGPT Pro，先上 sora.com）。
- **未披露**：backbone（DiT / 自回归 / 掩码生成无从确认）、visual tokenizer / VAE、text encoder（T5/CLIP/LLM）、音频如何与视频在 latent 层耦合、参数量、最大时长与分辨率上限、是否多分辨率/可变长训练。延续初代 [[sora]] 的"时空 patch + diffusion transformer"路线属合理猜测，但 **Sora 2 官方未确认**，本页不据此填充数字。

## 数据
官方仅在系统卡给出**笼统**口径，无规模/配比/清洗细节：
- **来源**（系统卡原文）：与其它 OpenAI 模型一致，训练数据包括「互联网上公开可得的信息」「与第三方合作获取的信息」「用户 / 人工训练员 / 研究员提供或生成的信息」三类。
- **过滤**：数据处理管线含"严格过滤以保证数据质量、降低潜在风险"，并用**一组安全分类器**阻止使用/生成有害或敏感内容（明确点名排除 CSAM——负责任地筛源以排除儿童性虐待材料，并与 NCMEC 合作）。
- **音频数据、视频对数量、再描述（re-captioning）、合成数据、美学过滤**等：**未披露**。
- 训练是否使用用户上传内容做后续训练：系统卡把"用户/训练员生成的信息"列入训练数据来源，但未说明具体范围与比例。

## 训练方法
**未披露**。官方没有公开训练目标（diffusion / flow matching / next-token / masked-token 均未确认）、是否多阶段（预训练→continue→SFT→偏好对齐）、是否做 RLHF/DPO/奖励模型、是否做步数蒸馏/一致性蒸馏等加速。

可确认的**唯一方法论线索**来自发布博客的叙事：Sora 2 的核心进步被归因于「**在视频数据上进一步扩展预训练算力 / 神经网络规模**」（scaling pretraining compute），并把"攻克大规模视频数据的预训练与后训练技术"列为关键里程碑——即官方明确承认存在**预训练 + 后训练**两段范式，但**后训练的具体做法（SFT/RL/对齐）完全未公开**。除此之外的训练细节本页一律标注"未披露"，不作编造。

> 产品侧另有一个独立的「自然语言可控推荐算法」用于 Sora App 的 feed（基于 OpenAI 现有 LLM 构建，用户可用自然语言指令调整推送）——这是**应用层**系统，与 Sora 2 视频生成模型的训练无关，列此仅为厘清边界。

## Infra（训练 / 推理工程）
**几乎全部未披露**：算力规模、GPU·时、并行/分布式策略、混合精度、吞吐、推理步数、缓存/量化/蒸馏加速均无公开数据。可确认的仅为**部署形态**：
- 通过 **sora.com** 网页端、**独立 iOS「Sora」App** 提供，后续接入 **API**；初代 **Sora 1 Turbo 仍保留可用**。
- 分档：免费档（较宽松但受总算力限制的额度）+ 面向 ChatGPT Pro 的 **Sora 2 Pro**（更高画质/性能的实验版）；需求超出算力时拟以"付费生成额外视频"作为唯一变现手段。
- 发布采**邀请制、按地域分批**（首发美国/加拿大）以匹配算力供给。
- 团队规模信息：博客署名显示 Sora 由 **Bill Peebles（Sora 负责人；学界以 DiT/Diffusion Transformer 一作著称，非本次源披露）**、Connor Holmes（Systems）、Rohan Sahai/Thomas Dimson（Product）、Aditya Ramesh（Organization）领衔；研究署名共 26 人（含 James Betker、Will DePue、Gabriel Petersson、Cheng Lu 等），侧面反映这是一个大型工程。
- 备注：Sora 产品已于 **2026-04-26 正式关停**（官方在快照页注明），但模型本身的能力评估仍以 2025-09 发布信息为准。

## 评测 benchmark（把效果讲清楚）
**OpenAI 未发布任何生成质量基准**：无 FID / VBench / GenEval / 人评 ELO / 与竞品的定量对比。发布博客全部以**定性演示**说明能力（奥运体操、桨板后空翻的浮力/刚度模拟、头顶猫的三周跳、投篮不中的真实反弹、跨镜头世界状态一致、写实/电影/动漫多风格、复杂背景声场与对白），**没有可引用的生成质量数字**——此维度按要求标注"**未报告**"，不引用任何第三方榜单以免混入非一手数据。

**唯一一组官方定量数字来自系统卡的安全评测**（用数千条对抗性 prompt，经"helpful-only"版模型生成后由生产安全栈在**输出端**判定；两项指标：not_unsafe=有效拦截不安全内容的召回，not_overrefuse=良性内容不被误拦）：

| 类别 | not_unsafe（输出端） | not_overrefuse（输出端） |
| --- | --- | --- |
| 成人裸露/性内容（不涉肖像） | 96.04% | 96.20% |
| 成人裸露/性内容（涉肖像） | 98.40% | 97.60% |
| 自残 | 99.70% | 94.60% |
| 暴力与血腥 | 95.10% | 97.00% |
| 违规政治劝服 | 95.52% | 98.67% |
| 极端主义/仇恨 | 96.82% | 99.11% |

这些是**安全有效性**指标，非生成质量指标；引用自 `sora-2-system-card.pdf` / `deploymentsafety.openai.com/sora-2`。

## 创新点与影响
**核心贡献（官方层面）**
1. **原生音画同步**：单模型一次生成画面+对白+环境声+音效且时间对齐，把"带音频"确立为该代视频模型新基线（与 Veo 3 同期）。
2. **物理一致性 / 可模拟失败**：从"为服从文本而扭曲现实"转向遵守动力学、能模拟失败而非只模拟成功，强化"视频模型即世界模拟器"的叙事。
3. **cameo / 角色**：基于一次性参考录制的、带**同意与撤销控制**的身份/外观注入，并由此长出一个"协同创作 / remix"的社交 App 形态——把生成模型产品化为社交网络，是产品层面的最大创新。
4. **可控性**：可遵循跨多镜头的复杂指令并维持世界状态一致，跨写实/电影/动漫风格。

**安全工程（系统卡，可引用细节）**
- 溯源三件套：所有输出带 **C2PA 元数据** + 从 sora.com/App 下载的视频带**可见移动水印** + OpenAI **内部反向图音检索**溯源工具。
- 多模态审核：对 prompt、输出视频帧、音频转写、评论、场景描述文本做输入拦截 + 输出拦截（含 CSAM 分类器 + 自定义训练的**多模态推理监控**，即一个针对内容政策做推理的多模态推理模型）。
- 音频专项：自动扫描生成语音的转写文本以检违规，**阻止模仿在世艺术家**及生成受版权保护的现有音乐，并尊重创作者的下架请求（见 launching-responsibly）。
- 肖像与未成年人：发布期**不支持 video-to-video**、不支持公众人物文生视频、屏蔽非同意真人；对疑似未成年人收紧阈值、限滚动时长、家长控制。
- 红队：与 OpenAI Red Team Network 外部成员就性内容、裸露、极端主义、自残、暴力血腥、政治劝服、青少年安全、肖像滥用等做对抗测试。

**已知局限**
- 模型"远非完美、仍会犯错"（官方自陈），物理一致性是进步而非解决。
- 技术不透明：无论文/报告/权重/基准，外界无法复现或定量对比。
- 发布期能力受限（无 v2v、无公众人物、邀请+地域限制），更多受产品/安全约束而非模型能力上限。
- 滥用风险（非同意肖像、误导性内容）是其逼真度与音频带来的新风险面，官方以迭代部署应对。

## 原始链接
- blog（发布公告，含"GPT-3.5 时刻"叙事与能力演示）: https://openai.com/index/sora-2/
- system_card（索引页，指向 PDF/部署安全页）: https://openai.com/index/sora-2-system-card/
- system_card（完整正文，含安全评测表/数据口径/溯源）: https://deploymentsafety.openai.com/sora-2
- system_card PDF: https://cdn.openai.com/pdf/50d5973c-c4ff-4c2d-986f-c72b5d0ff069/sora_2_system_card.pdf
- safety blog（Launching Sora responsibly，cameo 同意/水印/C2PA/音频安全细节）: https://openai.com/index/launching-sora-responsibly/

## 本地落盘文件
- ../../../sources/omni/2025/sora-2--blog.md
- ../../../sources/omni/2025/sora-2--system-card.md
- ../../../sources/omni/2025/sora-2--system-card-full.md
- ../../../sources/omni/2025/sora-2-system-card.pdf
- ../../../sources/omni/2025/sora-2--launching-responsibly.md
