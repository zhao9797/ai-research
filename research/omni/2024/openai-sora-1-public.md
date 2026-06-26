---
title: "Sora（Sora Turbo）公开发布"
org: OpenAI
country: US
date: "2024-12"
type: system-card
category: video
tags: [video-generation, text-to-video, diffusion-transformer, dit, spacetime-patches, world-simulator, recaptioning, closed-source]
url: "https://openai.com/index/sora-is-here/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://openai.com/sora/"
downloaded:
  - openai-sora-1-public--blog.md
  - openai-sora-1-public--system-card.md
  - openai-sora-1-public--tech-report.md
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Sora 是 OpenAI 的文/图/视频→视频生成模型，2024-12-09 以 **Sora Turbo** 之名从研究预览转为公开产品（sora.com，面向 ChatGPT Plus/Pro），核心是**在压缩潜空间上对 spacetime patches 做扩散的 Diffusion Transformer（DiT）**，最亮眼能力是可生成**最长 20 秒、最高 1080p、任意宽高比（横/竖/方）**的高保真视频；产品发布时主打"原生尺寸训练+视频扩展/混合/storyboard"等交互能力，但 OpenAI 明确承认模型在复杂物理与长时序动作上仍有大量局限。

## 背景与定位
- Sora 最初于 2024-02-15 以研究报告《Video generation models as world simulators》（[[sora]]）亮相，定位为"通往通用物理世界模拟器"的一步，而非单纯的文生视频玩具。2024-12 的发布是把该研究路线**产品化**：训练了一个比 2 月预览版"显著更快"的新版本 **Sora Turbo**，作为独立产品上线。
- 技术脉络上，Sora 把 LLM 的"internet-scale 数据 + token 化 + transformer 可扩展性"范式迁移到视觉生成：LLM 用 text token，Sora 用 **visual patch**。它是 [[latent-diffusion-ldm]]（潜空间扩散）+ [[dit-scalable-diffusion-transformers]]（Diffusion Transformer, Peebles & Xie）+ [[ddpm]]（去噪扩散）+ DALL·E 3 recaptioning（[[dall-e-3]]）几条线的工程化集成，并把它们推到"原生变长/变分辨率/变宽高比的视频"这一新规模。
- 相对前置视频生成工作（RNN / GAN / 自回归 transformer / 早期视频扩散如 Imagen Video、Align-your-Latents）的最大改进：放弃"把视频统一 crop/resize 成固定尺寸（如 4s@256×256）"的做法，**用原生尺寸训练**，并验证 diffusion transformer 在视频上同样具备随算力扩展的 scaling 性质。
- 产品意义：Sora 是首个被广泛使用的"长时长、高保真、商用"文生视频产品，引爆了 2024–2025 视频生成军备竞赛（Kling、Runway Gen-3、Veo、即梦/可灵等），是该赛道的标杆事件。

> 注：截至 2026-04-26，发布博客页脚标注"Sora 产品已不再可用"（应指被后续 Sora 2 等迭代取代/下线），但本页记录的是 2024-12 这次公开发布的技术与产品事实。

## 模型架构
一手源对架构给的是**高层描述**，OpenAI 在技术报告中明确写"Model and implementation details are not included in this report"，因此**参数量、层数、具体 tokenizer 结构均未披露**。可确证的设计：

- **Backbone：Diffusion Transformer（DiT）**。Sora 是 diffusion model——从一段纯噪声"基底视频"出发，经多步去噪逐步还原；但它本质是**扩散 transformer**：在带噪 patch（+ 文本等条件）上训练，预测原始"干净"patch。系统卡强调"和 GPT 类似采用 transformer 架构，解锁了更优的 scaling"。
- **视觉表示：spacetime latent patches（时空潜 patch）**。流程分两步：
  1. **视频压缩网络（VAE 式 encoder/decoder）**：把原始视频在**时间和空间两个维度上同时压缩**到低维潜空间；Sora 在该压缩潜空间内训练与生成，再用配套 decoder 把生成的 latent 映射回像素。
  2. **时空 patch 提取**：对压缩后的视频切出一串 spacetime patch，作为 transformer 的 token。图像被当作"单帧视频"统一处理。
- **变长/变分辨率/变宽高比的统一建模**：patch 表示天然支持不同分辨率、时长、宽高比的混合训练；推理时通过**把随机初始化的 patch 排布成目标尺寸的网格**来控制输出尺寸。可采样 1920×1080、竖屏 1080×1920 及中间各种比例，同一模型还能**先低分辨率快速预览再出全分辨率**。
- **图像生成作为特例**：把高斯噪声 patch 排成"时间维度=1 帧"的空间网格即可生成图像，最高支持 **2048×2048**。
- **文本条件注入**：文本经 captioner/GPT 改写后作为条件输入（见数据/训练）；具体 text encoder（T5/CLIP/自家 LLM）未披露。
- **产品端规格（发布版 Sora Turbo）**：输出最长 **20 秒**、最高 **1080p**，支持横/竖/方多宽高比；支持纯文生视频、图生视频（动画化静图）、视频扩展（前/后向补帧、做无缝循环）、视频混合/插值、以及 storyboard 逐帧控制等。

## 数据
来自系统卡"Model Data"小节，规模/配比/具体清单**未披露**，但来源结构与处理流程明确：

- **数据组成（三类混合）**：
  1. **精选公开数据**——多取自业界标准 ML 数据集与网络爬取。
  2. **数据合作伙伴的专有数据**——通过合作获取非公开数据；系统卡点名与 **Shutterstock、Pond5** 合作（原文措辞为"on building and delivering AI-generated images"），并委托/定制符合需求的数据集（"commission and create datasets fit for our needs"），另有部分自研数据集（"developed in-house"）。
  3. **人类数据**——来自 AI trainer、红队、员工的反馈。
- **核心数据范式**：借鉴 LLM"internet-scale 数据 + token 化"思路，把视频统一压成低维 latent 再切 spacetime patch，使"diverse 类型的视频/图像"能在同一表示下大规模训练（patch 被论证为高度可扩展的视觉表示）。
- **Re-captioning（关键数据手段）**：沿用 **DALL·E 3 的 recaptioning**——先训练一个**高描述性的 captioner 模型**，给训练集**所有视频**重新生成高度详细的字幕；OpenAI 发现"在高描述性字幕上训练"同时提升**文本一致性（text fidelity）和整体视频质量**。推理期再用 **GPT 把用户短 prompt 扩写成长详细描述**送入视频模型，提升指令遵循。
- **预训练数据过滤**：训练前所有数据集都过一道过滤，剔除最露骨/暴力/敏感内容（如部分仇恨符号），是 DALL·E 2/3 过滤方法的延伸；并针对 CSAM 做负责任的数据来源治理（Thorn/NCMEC 体系）。
- 训练数据**总时长/对数/Token 数均未披露**。

## 训练方法
- **训练目标：扩散去噪**。给定带噪 patch 与条件信息，模型训练去预测原始"干净"patch（标准 diffusion 目标）。一手源**未说明**是否用 v-prediction、EDM 参数化或 flow matching/rectified flow——参考文献里列了 DDPM、Improved-DDPM、Karras EDM 等，但未指明 Sora 具体采用哪种参数化。
- **原生尺寸训练（核心 trick）**：不做统一 crop/resize，直接在数据原生时长/分辨率/宽高比上训练。消融观察：**裁成方形 crop 训练的版本**常把主体只放进画面一部分（构图被切坏），而原生宽高比训练的 Sora **构图与取景明显更好**（定性对比，无数值）。
- **Scaling 验证**：固定 seed 与输入，对比 base / 4× / 32× compute 三档，**样本质量随训练算力提升显著变好**（定性，OpenAI 未给损失/FID 曲线数值）——这是把 DiT 的 scaling 性质迁移到视频的关键经验结论。
- **多任务统一**：同一模型同时支持文生视频、图生视频、视频扩展（前/后向）、视频到视频编辑（用 SDEdit 零样本改风格/环境）、视频插值连接、纯图像生成——靠 patch 表示+条件 patch 拼接实现，而非多个专用模型。
- **Sora Turbo（发布版）**：相对 2 月预览版"**显著更快**"，OpenAI 称仍在努力降低成本以普惠。**加速手段（步数蒸馏 / consistency / 量化等）未披露**，仅知更快。
- **多阶段/SFT/RLHF/DPO/reward model**：一手源**未报告**视频生成本体是否有偏好对齐阶段；系统卡描述的"对齐"主要是**安全侧**（红队反馈调阈值、prompt 改写、分类器）而非生成质量的 RLHF。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行策略 / 混合精度 / 吞吐：全部未披露**。技术报告明确不含实现细节。可定性确证的只有"随算力扩展质量提升"以及发布版 Sora Turbo 在推理速度上相比预览版有大幅优化。
- **推理控制**：尺寸通过排布随机 patch 网格控制；支持低分辨率快速预览→全分辨率出片的同模型工作流。
- **部署形态**：云端产品 sora.com，含 Plus/Pro 订阅分级——Plus 每月最多 50 条 480p（或更少的 720p）视频，Pro 给 10× 用量、更高分辨率与更长时长。所有输出带 **C2PA 元数据** + 默认**可见动态水印**，并配套内部"反向视频检索"溯源工具。
- **可用性限制（发布时）**：仅 18+；首发在英国、瑞士、欧洲经济区不可用；人物上传（likeness）仅作为小范围 pilot 灰度。

## 评测 benchmark（把效果讲清楚）
**Sora 是闭源产品，OpenAI 未发布任何生成质量基准数字**——没有 FID、CLIPScore、VBench、人评 ELO 等可比指标；技术报告与发布博客只给**定性能力展示**与**定性局限**，发布博客与系统卡里出现的所有数值都属于**安全分类器评测**，不是生成质量。如实记录如下：

- **生成质量基准**：FID / CLIPScore / VBench / GenEval / 人评 Arena 等**全部未报告**。能力以定性方式描述：最长 1 分钟高保真（研究版能力上限）、产品版 20s/1080p、3D 一致性、长程一致性与物体永存（遮挡/出画后仍保持主体）、单样本内同一角色多镜头一致、可零样本模拟 Minecraft 等数字世界。
- **明确披露的局限（定性）**：不能准确模拟很多基础物理交互（如玻璃破碎）；吃东西等交互不总能正确改变物体状态；长时长样本会出现不连贯、物体凭空出现等失败模式；复杂动作在长时序上易崩。
- **安全侧评测数字（来自系统卡，均为分类器/审核效果，非生成质量）**：
  - **未成年人（under-18）图像分类器**：5000 张近似样本上——Realistic Child 准确率 97.86%、Realistic Adult 99.28%、Fictitious Adult 97.37%、Fictitious Child 69.24%；总体 **Precision 80.95% / Recall 97.86%**。
  - **裸露与暗示性内容（Nudity & Suggestive）**：输入端准确率 97.25%，端到端（输出）**97.59%**（每类约 200 个违规样本）。
  - **欺骗性选举内容 LLM 过滤器**：**Recall 98.23% / Precision 88.80%**（N≈500，合成数据 prompt），命中即阻断输出。
  - 输出审核以**每秒 2 帧**（CSAM/儿童安全）或**每秒 1 帧**（选举内容）扫描视频。
- **红队规模**：9 国外部红队，从 2024-09 持续到 12 月，测试 **15,000+ 次生成**；早期 alpha 艺术家计划覆盖 60+ 国 300+ 用户、**500,000+ 模型请求**。
- **消融结论（定性）**：原生宽高比训练 > 方形 crop（构图更好）；高描述性 recaption 提升文本一致性与质量；算力越大质量越高。**均无配套数值**。

## 创新点与影响
- **核心贡献**：
  1. 把"潜空间扩散 + Diffusion Transformer + spacetime patch token"组合工程化到**原生变长/变分辨率/变宽高比视频**，验证 DiT 的 scaling 性质在视频域成立——"质量提升纯靠规模，无需为 3D/物体显式注入归纳偏置"。
  2. 把 DALL·E 3 的 recaptioning（训练侧重写字幕 + 推理侧 GPT 扩写 prompt）系统迁移到视频，显著改善指令遵循。
  3. 统一表示带来的多任务能力：文生/图生/视频扩展/视频编辑（SDEdit）/插值/图像生成同模型完成。
  4. 提出"**视频生成模型作为物理世界模拟器**"的叙事，把视频生成与世界模型/AGI 路线挂钩，并展示 3D 一致性、物体永存、Minecraft 零样本模拟等涌现能力。
- **影响**：作为首个广泛使用的长时长高保真商用文生视频产品，确立了 DiT+latent+patch 的视频生成事实标准范式，直接推动 2024–2025 视频生成赛道（Kling/可灵、Runway Gen-3、Google Veo、字节即梦等）军备竞赛；其 C2PA+可见水印+溯源工具也成为视频生成内容来源治理的早期模板。
- **已知局限**：物理不准、长时序崩坏、成本高（OpenAI 自承未做到人人可负担）；闭源——参数、算力、训练细节、生成质量基准全不公开，外部无法复现或客观横评；发布时区域/人物上传受限。

## 原始链接
- blog（发布公告）: https://openai.com/index/sora-is-here/
- system_card: https://openai.com/index/sora-system-card/
- tech-report（2024-02 研究报告，架构方法一手源）: https://openai.com/index/video-generation-models-as-world-simulators/
- project（产品页）: https://openai.com/sora/
- bibtex: https://openai.com/bibtex/videoworldsimulators2024.bib

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/openai-sora-1-public--blog.md)
- [system-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/openai-sora-1-public--system-card.md)
- [tech-report.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/openai-sora-1-public--tech-report.md)
