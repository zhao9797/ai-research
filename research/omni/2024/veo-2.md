---
title: "Veo 2"
org: "Google DeepMind"
country: US
date: "2024-12"
type: blog
category: video
tags: [video-generation, text-to-video, image-to-video, closed-source, cinematography, latent-diffusion, synthid, 4k]
url: "https://blog.google/innovation-and-ai/models-and-research/google-labs/video-image-generation-update-december-2024/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://deepmind.google/technologies/veo/veo-2/"
downloaded: [veo-2--blog-google-dec2024.md, veo-2--deepmind-veo2-wayback20241220.md, veo-2--deepmind-veo2.md, veo-2--vertex-ai-model-card.md, veo-3-tech-report-family-context.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Veo 2 是 Google DeepMind 2024-12-16 发布的旗舰闭源文/图生视频模型，主打**强物理真实感、电影级镜头语言控制（指定镜头/焦段/景深）、最高 4K 分辨率、分钟级时长、更少幻觉伪影**；在 Meta 的 **MovieGenBench（1003 条 prompt，720p 人评）** 头对头评测中，整体偏好度与 prompt 跟随度均居首，是与 [[sora]] 正面竞争的产品级发布。技术细节几乎全部未公开。

## 背景与定位
- **前置**：Veo 1 于 2024-05 Google I/O 发布；同期视频生成赛道由 OpenAI [[sora]]（2024-02 预览，2024-12 公测见 [[sora]]）、Meta [[movie-gen]]、快手 [[kling]] 等领跑，Google 早期工作有 [[imagen-video]] / [[make-a-video]] 一脉。
- **要解决的问题**：上一代视频模型普遍存在物理不真实、运动不连贯、"幻觉"出多余手指/物体、对镜头语言（运镜、焦段、景深）控制弱等痛点。Veo 2 的卖点正是**对真实世界物理与人体运动表情的更好理解**，以及**对电影摄影术语的精确响应**。
- **技术脉络中的位置**：Veo 系列属潜空间扩散（latent diffusion）路线（见下"模型架构"，依据后续 Veo 3 技术报告对家族方法的披露），与 [[ddpm]] → [[imagen-video]] 的扩散视频生成谱系一脉相承，但 Veo 2 本身无公开论文/技术报告，定位是**产品发布而非学术发布**。

## 模型架构
**官方未披露 Veo 2 的具体架构**（无技术报告、无 model card 架构章节、无参数量）。可确证的产品级能力规格如下：

- **任务形态**（据 Vertex AI `veo-2.0-generate-001` GA model card，2025-05-27 正式版口径）：支持 **text-to-video、image-to-video、prompt rewrite（提示重写）、参考样式图/素材图、向视频插入对象**；**明确"不支持"延长视频（extend）与首尾帧生成（first & last frame）**（这两项在 Veo 2 GA 端点上未开放，是 Veo 3 才补齐的能力）。⚠️ 本页早前版本把 extend / 首尾帧列为 Veo 2 生产能力，与官方 model card 的"不支持"相矛盾，已更正。
- **分辨率与时长**：博客称研究模型可达 **"up to 4K" 与 "extended to minutes in length"**（一手见 blog 正文）；但**生产 API（Vertex AI）实际规格为 720p（输入/输出均 720p）/ 24 FPS / 视频时长 5–8 秒 / 单次每 prompt 最多 4 条视频 / 提示语言仅英语 / 宽高比 16:9 与 9:16 / MIME video/mp4**（逐项见 model card 规格表）——4K 与分钟级是研究模型上限/演示口径，落地产品受限于 720p·8s。
- **镜头控制**：通过自然语言精确响应电影摄影术语——可指定 genre、镜头运动（low-angle tracking shot、dolly、spiral 等）、焦段（"18mm lens" 自动出广角、"35mm" 等）、景深（"shallow depth of field" 虚化背景）、胶片质感（"Kodak Portra 400"、"70mm film"）。这是 Veo 2 相对同期模型最突出的可控性卖点。

**家族架构旁证（来自 Veo 3 技术报告，非 Veo 2 官方口径，仅作方法谱系参考）**：Veo 系列采用**潜空间扩散（latent diffusion）**——视频经各自的编码器压缩为**时空视频 latent**，训练时用**基于 transformer 的去噪网络**在 latent 上做扩散（Veo 3 进一步把音频 latent 与视频 latent 联合扩散）。据此推断 Veo 2 大概率为 latent-diffusion + transformer 去噪骨干，但**具体 backbone（U-Net / DiT / MMDiT）、tokenizer/VAE、text encoder、参数量在 Veo 2 时点均未公开**。⚠️ 网络上流传的"Veo 2 = MM-DiT + 3D 时空 VAE + causal attention"等说法多源自第三方推测或搜索引擎 AI 摘要，**非 Google 官方对 Veo 2 的披露**，本页不予采信为事实。

## 数据
**Veo 2 训练数据未披露**（来源/规模/配比/清洗均无官方说明）。

家族级做法旁证（Veo 3 技术报告，方法谱系参考，非 Veo 2 数字）：在**图像+视频+标注**的大规模数据上训练；用**多个 Gemini 模型**对数据做**不同详细程度的文本 caption**（multi-level captioning）；用**合成 caption** 提升概念多样性；做**跨来源语义去重**以降低过拟合特定训练样本的风险；对训练视频做**合规、安全、质量过滤**，剔除不安全 caption 与 PII。Veo 2 时点这些细节均未单独发布。

## 训练方法
**Veo 2 训练目标/多阶段/对齐/蒸馏细节全部未披露**。

- 仅从家族方法可知走**扩散（latent diffusion）**目标；transformer 去噪网络（Veo 3 报告口径）。
- 安全/对齐：官方强调"安全与负责任开发"贯穿 Veo 2，做了**预训练数据安全过滤**与**后训练缓解**（family 做法对齐 Gemini）；输出统一加 **SynthID 隐形水印**。但**是否做 RLHF/DPO/reward model、是否做步数蒸馏/一致性蒸馏加速、关键超参——均未报告**。
- 部署节奏强调"刻意保守地逐步放量"（measured rollout），先在 VideoFX / YouTube / Vertex AI 小范围灰度以评估质量与安全。

## Infra（训练 / 推理工程）
**未披露**：算力规模、GPU·时、并行/分布式策略、混合精度、训练吞吐、推理加速（步数/缓存/量化/蒸馏）等工程细节，Google 在 Veo 2 发布时**均无公开**。

可确证的部署形态：通过 Google Labs **VideoFX** 工具灰度（候补名单），并计划次年扩展到 **YouTube Shorts**（均见 blog 正文）；企业侧通过 **Vertex AI**（`veo-2.0-generate-001`）开放，GA model card 给出的配额/限制为**每基础模型每分钟区域级在线预测请求数 = 10**（注：非早前误写的 20）、**每 prompt ≤4 条视频**、**image-to-video 输入图 ≤20 MB**、使用类型为**固定配额**（不支持 provisioned throughput / 标准按需付费）。

## 评测 benchmark（把效果讲清楚）
官方唯一公开的量化评测在 deepmind.google/technologies/veo/veo-2 页（已落盘 wayback 快照）：

- **基准数据集**：Meta 发布的 **MovieGenBench**，**1003 条 prompt** 及对应视频，由**人类评审（human raters）**做头对头偏好打分。
- **结论**：Veo 2 在**整体偏好（overall preference）**与**prompt 跟随准确度（prompt following）**两项上**均表现最佳**，优于当时一众领先视频生成模型。
- **评测设置（重要可比性说明）**：所有对比在 **720p** 分辨率下进行；**Veo 采样时长 8s，VideoGen 为 10s，其余模型为 5s**，评审看完整时长视频。
- **对手覆盖**：页面图表与上述设置表明对比对象包含 Meta Movie Gen / VideoGen 等（具体对手集合以图表为准）。
- **质量主张**：官方称 Veo 2 相比其他模型**显著减少幻觉伪影**（更少出现多余手指/意外物体），细节、真实感、运动准确度均更强。

⚠️ **具体胜率百分比（如各项 win-rate %）仅以图表（chart 图片）形式发布，正文未给数字**；本页据已抓取的一手文本只能确证"整体偏好与 prompt 跟随均居首"的定性结论，**不编造具体百分比**。亦**无 FID / VBench / CLIPScore 等自动指标的官方报告**（Veo 2 未报告自动化基准数字）。

**局限（官方自述）**：在生成高度真实、动态或精细的视频、以及在复杂场景/复杂运动中**保持完全一致性**方面仍有挑战，Google 表示会持续改进。

## 创新点与影响
- **核心贡献**：将**电影摄影术语级的可控性**（镜头运动 + 焦段 + 景深 + 胶片质感）与**更强物理/人体运动真实感 + 更少幻觉**结合，并把分辨率上限推到 4K；以产品形态在 MovieGenBench 人评上压过同期 SOTA，确立 Google 在视频生成赛道与 Sora 正面竞争的地位。
- **影响**：Veo 2 是 Veo 产品线规模化落地（VideoFX → YouTube Shorts → Vertex AI 企业 API）的关键一步，奠定了 2025 年 **Veo 3**（首份公开技术报告、引入**原生音频联合生成**）的方法与产品基础；其"用自然语言精确指定运镜/焦段"的范式被后续产品广泛跟进。
- **已知局限**：① 技术完全闭源，架构/数据/训练/infra 几乎零公开，学术可复现性为零；② 复杂运动/长时序一致性仍不稳定；③ 生产 API 实际开放规格（720p·8s·英文）远低于"4K·分钟级"的演示口径；④ 官方量化评测仅一项人评偏好、无自动指标、胜率数字未文字化。

## 原始链接
- blog（发布稿，核心一手源）: https://blog.google/innovation-and-ai/models-and-research/google-labs/video-image-generation-update-december-2024/
- product/benchmark page（原始 Veo 2 页，含 MovieGenBench 设置）: https://deepmind.google/technologies/veo/veo-2/ ；存档版 http://web.archive.org/web/20241220153421/https://deepmind.google/technologies/veo/veo-2/
- model index（现已跳转至 Veo 3.1）: https://deepmind.google/models/veo/
- Vertex AI 官方 model card（生产规格）: https://cloud.google.com/vertex-ai/generative-ai/docs/models/veo/2-0-generate-001
- 家族架构旁证（Veo 3 技术报告，非 Veo 2 口径）: https://storage.googleapis.com/deepmind-media/veo/Veo-3-Tech-Report.pdf

## 本地落盘文件
- ../../../sources/omni/2024/veo-2--blog-google-dec2024.md （2024-12-16 发布博客，核心一手源：4K/分钟级/电影术语/SynthID/measured rollout）
- ../../../sources/omni/2024/veo-2--deepmind-veo2-wayback20241220.md （**原始 Veo 2 产品页 wayback 快照**，唯一含 MovieGenBench 1003 prompt 人评设置的一手文本）
- ../../../sources/omni/2024/veo-2--deepmind-veo2.md （⚠️ 抓取时该 URL 已重定向，内容实为 **Veo 3/3.1 现行页**，非 Veo 2 原页；仅留作链路记录，正文 Veo 2 结论不据此页）
- ../../../sources/omni/2024/veo-2--vertex-ai-model-card.md （Vertex AI / Gemini Enterprise `veo-2.0-generate-001` GA 规格表：720p·5–8s·24FPS·≤4 视频·英语·配额 10/min；2026-06-25 重抓，原抓取仅得导航 chrome 已修复）
- ../../../sources/omni/2024/veo-3-tech-report-family-context.pdf （PDF，.gitignore 排除不入 git，仅本地；**Veo 3 技术报告**，仅作家族 latent-diffusion 方法谱系旁证，非 Veo 2 口径）
