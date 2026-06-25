---
title: "Kling (可灵) 视频生成大模型"
org: Kuaishou (快手)
country: China
date: "2024-06"
type: blog
category: video
tags: [video-generation, t2v, i2v, dit, 3d-vae, spatiotemporal-attention, closed-source, kuaishou]
url: "https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-unveils-proprietary-video-generation-model-kling/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://kling.kuaishou.com/"
downloaded: [kling--ir-press-release.md, kling--ir-press-release-zh.md, kling--globenewswire-2-0.md, kling--product-en.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Kling（可灵）是快手 2024 年 6 月 10 日发布的自研视频生成大模型，采用 **DiT 架构 + 自研 3D VAE（时空同步压缩）+ 计算高效的全注意力时空建模模块**，首发即支持「最长 2 分钟 / 30fps / 1080p / 多宽高比」的高保真生成，是**全球首个面向公众开放可用的 DiT 视频生成产品**（早于 Sora 公测），上线 10 个月全球用户破 2200 万，Kling 1.6 Pro 于 2025-03-27 在 Artificial Analysis 图生视频 Arena 以 ELO 1000 登顶（压过 Google Veo 2、Pika）。

## 背景与定位
2024 年 2 月 OpenAI 公布 [[sora]] 演示，把「长时长、高保真、物理一致」的视频生成推向风口，但 Sora 当时不可用。快手依托其短视频平台的海量视频数据与工程能力，于 4 个月后（2024-06-10）在自家剪辑 App「快影」内开放可灵邀测——成为**第一个真正能让普通用户用上的高质量 DiT 视频模型**，填补了 Sora「只见 demo 不见产品」的真空，引发广泛关注，被视为国产视频生成的标志性突破。

技术脉络上，可灵延续了 2023 年起视频生成从 U-Net 扩散（如 AnimateDiff、SVD）转向 [[dit-scalable-diffusion-transformers]] 主干 + [[latent-diffusion-ldm]] 范式的大趋势，并以**自研 3D VAE 做时空联合压缩**、**全注意力时空建模**两点对齐 Sora 路线。它是快手 AI 大模型矩阵的一员：此前快手已发布 1750 亿参数通用语言模型「快意 KwaiYii」与文生图模型「可图 KeTu」（后演进为 [[kolors]]），可灵与可图/Kolors 在产品上深度联动（官方称约 85% 的视频创作来自「图生视频」，图像质量直接决定视频效果）。

> 注：可灵为**闭源商业产品**，快手未公开论文 / 技术报告 / 权重 / 代码。本页技术内容均来自快手官方信息披露（IR 新闻稿、Kling 2.0 发布稿、官网产品页），工程内幕（参数量、算力、数据规模与配比、训练细节）官方**未披露**，下文如实标注。

## 模型架构
官方对 2024 年首发版本披露的架构要点（来自快手 IR 新闻稿中英文版，措辞一致）：

- **主干：DiT（Diffusion Transformer）**。可灵采用基于扩散的 Transformer 架构，并在此基础上对「隐空间编/解码」与「时序建模」两大模块做了「升维处理」（即扩展到时空维度）。
- **视觉 tokenizer / VAE：自研 3D VAE**。在隐空间编/解码上快手自研 3D VAE 网络，实现**时空同步压缩**（spatiotemporal compression），在重建质量与训练性能/效果之间取得平衡。这是承载「长时长 + 高分辨率」的关键——3D VAE 把视频在空间与时间维度一起压缩进 latent，显著降低 DiT 需要建模的 token 数。
- **时序建模：计算高效的全注意力（full-attention）时空建模模块**。官方称设计了一款「计算高效的全注意力机制」作为时空建模模块，**融合时间与空间信息**，既能捕捉帧内局部空间特征，又能捕捉跨帧时间动态特征。注意：官方原文是「3D 时空全注意力」语义（significance 字段称「3D 时空注意力」），即把视频 token 在时间 + 空间上做联合注意力，而非分离的 spatial/temporal 交替注意力——这与 Sora 的「spacetime patches + 联合注意力」思路一致；但具体是否做了稀疏化/分块以「计算高效」，官方**未披露实现细节**。
- **文本编码器 / 条件注入**：官方**未披露** text encoder 选型（T5 / CLIP / LLM）与条件注入方式（cross-attention / adaLN）。
- **参数量与分辨率策略**：可灵**模型参数量官方未披露**。首发即支持**最长 2 分钟、30fps、最高 1080p、多种宽高比**（这是 2024 年同期产品中时长与分辨率上限的领先指标）。
- **能力定位**：官方强调可灵能生成「大幅度的合理运动」并「模拟物理世界特性」，对快速移动物体、剧烈场景变化、复杂人物动作均能精确捕捉——即把「运动幅度 + 物理一致性」作为核心卖点。

后续迭代（非 2024 版，作为脉络补充）：2025-04 Kling 2.0 提出 **MVL（Multimodal Visual Language，多模态视觉语言）** 交互范式，由 TXT（纯文本）与 MMW（Multi-modal-document as a Word，把图像/视频片段当作「词」）组成，支持图像参考、视频片段等多模态输入以表达身份/外观/风格/场景/动作/运镜等，并落地「多模态视频编辑」（用图或文增删替换视频元素）。这些**架构层面的实现细节官方仍未公开**。

## 数据
- **数据来源/规模/配比/清洗/re-caption/合成数据：官方全部未披露。** 快手作为头部短视频平台天然拥有海量视频数据，业界普遍推测可灵受益于此，但快手**未公开**训练数据来源、规模、过滤与标注流程，本页**不臆测具体数字**。
- 官方仅在产品层面说明可灵在「运动合理性」「物理真实感」上的优势，未给出数据侧支撑细节。

## 训练方法
- **训练目标**：基于扩散（diffusion）的 DiT，官方未说明是否用 flow matching / rectified flow，也未披露多阶段训练（预训练→continue→SFT→偏好对齐）的具体配置。
- **偏好对齐 / RLHF**：2024 首发稿未提及。Kling 2.0 发布稿提到团队用 **GSB（Good-Same-Bad）** 方法做内部多指标人评以驱动迭代，但这属于评测/对齐评估方法，**训练侧 RLHF/DPO/reward model 的具体做法官方未披露**。
- **蒸馏 / 加速（consistency/LCM/ADD/步数蒸馏）**：官方**未披露**。官方稿中 Kling 1.6 Pro 标注为「high-quality mode（高质量模式）」，暗示产品侧存在速度-质量分档（可能涉及步数或蒸馏），但具体档位划分与实现细节官方均未公开（本页不臆测「高性能模式」等未见于一手源的命名）。
- **迭代节奏**：官方称自 2024-06 上线后做了**超过 20 次迭代**（1.0→1.5→1.6→2.0…），持续提升画质清晰度与新功能。这是快手对「持续后训练 + 数据飞轮」工程能力的体现，但每次迭代的训练改动**未逐一披露**。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行分布式 / 混合精度 / 吞吐：官方全部未披露。**
- **推理 / 部署形态**：可灵以**云端商业服务**形态交付——中国区初期在「快影」App 内邀测，后开放可灵官网（kling.kuaishou.com / klingai.com / kling.ai 海外站）网页与 App；面向企业提供 **API**。截至 2025-04，官方称全球已有 **1.5 万+ 开发者与企业客户**接入 Kling API，累计生成约 **1200 万张图、4000 万+ 条视频**；合作客户包括小米、AWS、阿里云、Freepik、蓝色光标等。
- 3D VAE 的时空同步压缩本身即是**推理工程优化**的一部分（降低 token 数→降低长视频生成成本），但具体推理加速手段（缓存、量化、步数蒸馏）官方**未公开**。

## 评测 benchmark（把效果讲清楚）
可灵闭源，官方未公布 FID/CLIPScore/VBench 等学术指标，主要以**第三方 Arena 排名**与**内部人评（GSB）**作为效果证据：

- **Artificial Analysis 视频 Arena（第三方权威人评 Arena）**：2025-03-27 发布的全球视频生成大模型排名中，**快手 Kling 1.6 Pro（高质量模式）以 Arena ELO 1000 分登顶图生视频（Image-to-Video）类目**，Google Veo 2、Pika 分列二、三名（数据出自快手 Kling 2.0 官方发布稿引述）。
- **内部 GSB（Good-Same-Bad）人评**：Kling 2.0 在图生视频类目对 **Google Veo 2 的胜负比达 182%**、对 **Runway Gen-4 达 178%**，官方称在语义响应、视觉质量、动态质量等维度显著领先（数据为快手内部评测，**非独立第三方**，需谨慎看待）。
- **图像侧（Kolors 2.0）**：官方称在内部胜负评中相对 Midjourney V7、FLUX 1.1 Pro、Reve 等领先模型保持显著优势（同为内部评测）。
- **用户规模代理指标**：上线 10 个月全球用户超 **2200 万**（2025-04），被官方作为「全球首个用户可用 DiT 视频模型」的市场验证。

> 说明：上述 ELO 1000、182%/178% 等数字均来自快手**官方披露**（其中 ELO 引自 Artificial Analysis，胜负比为快手内部 GSB 评测）。学术 benchmark（VBench、FID 等）官方**未报告**，故本页不列。

## 创新点与影响
**核心贡献**
1. **工程落地的「DiT + 3D VAE + 时空全注意力」长视频方案**：在 Sora 仅有 demo 时，快手用自研 3D VAE 时空同步压缩 + 计算高效全注意力，把 2 分钟 / 30fps / 1080p 的高保真视频生成做成了**真正可用的产品**。
2. **「全球首个用户可用 DiT 视频模型」**：把前沿视频生成从论文/演示推进到大规模消费级与企业级（API）服务，定义了 2024 年国产视频生成的标杆。
3. **MVL 多模态视觉语言（2.0 起）**：提出以图像/视频片段作为「视觉词」的多模态输入交互范式，推动视频生成从「纯文本提示」走向「多模态意图表达 + 可控编辑」。

**影响**
- 引爆并加速了 2024 下半年国产视频生成竞赛——与同期 [[hunyuan-video]]（腾讯）、[[cogvideox]]（智谱）、Vidu（生数）、Gen-3（Runway）等形成正面竞争；可灵长期位居第三方视频 Arena 头部。
- 以「图生视频为主（约 85%）」的产品形态，把图像模型（Kolors）与视频模型绑定，形成「文生图→图生视频→编辑」的工业化创作流水线，被影视/广告团队规模化嵌入生产。

**已知局限**
- **完全闭源**：无论文/权重/代码，架构与训练细节大量「未披露」，学界难以复现或独立核验。
- **评测多为内部 GSB**：除 Artificial Analysis ELO 外，多数对比为快手自评，缺乏独立第三方学术 benchmark。
- 工程内幕（参数量、算力、数据来源与规模、推理加速）官方均**未公开**。

## 原始链接
- blog/press（官方英文 IR 首发稿，2024-06-10）: https://ir.kuaishou.com/news-releases/news-release-details/kuaishou-unveils-proprietary-video-generation-model-kling/
- blog/press（官方中文 IR 首发稿）: https://ir.kuaishou.com/zh-hans/news-releases/news-release-details/kuaishouziyanshipinshengchengdamoxingkelingkaifangceshi
- blog/press（Kling 2.0 官方发布稿，GlobeNewswire，2025-04-15）: https://www.globenewswire.com/news-release/2025/04/15/3062142/0/en/kling-ai-advances-to-the-2-0-era-empowering-everyone-to-tell-great-stories-with-ai.html
- product（可灵 AI 官网产品页）: https://kling.kuaishou.com/  ·  https://klingai.com/  ·  https://kling.ai/
- benchmark（第三方）: Artificial Analysis Video Arena — https://artificialanalysis.ai/text-to-video/arena （Kling 1.6 Pro 图生视频登顶，2025-03-27，官方引用）

## 本地落盘文件
- ../../../sources/omni/2024/kling--ir-press-release.md       （官方英文 IR 首发稿）
- ../../../sources/omni/2024/kling--ir-press-release-zh.md    （官方中文 IR 首发稿）
- ../../../sources/omni/2024/kling--globenewswire-2-0.md      （Kling 2.0 官方发布稿）
- ../../../sources/omni/2024/kling--product-en.md             （可灵 AI 官网产品页快照）
