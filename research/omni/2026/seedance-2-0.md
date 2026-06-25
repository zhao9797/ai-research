---
title: "Seedance 2.0"
org: "ByteDance Seed"
country: China
date: "2026-02"
type: tech-report
category: video
tags: [video, audio-video, multimodal, t2v, i2v, r2v, editing, binaural-audio, closed-source]
url: "https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0"
arxiv: "https://arxiv.org/abs/2604.14148"
pdf_url: "https://arxiv.org/pdf/2604.14148"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/en/seedance2_0"
downloaded: [arxiv-2604.14148.pdf, seedance-2-0--blog.md, seedance-2-0--project-page.md, seedance-2-0--eval-t2v.jpg, seedance-2-0--eval-i2v.jpg, seedance-2-0--eval-multimodal.jpg]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Seedance 2.0 是字节跳动 Seed 团队 2026-02-12（中国）发布的新一代**原生多模态音视频联合生成模型**，统一架构同时吃文/图/音/视四模态输入，单次最多可参考 9 张图 + 3 段视频 + 3 段音频，原生输出 4–15s、480p/720p 的**带双声道音频**视频；在第三方众包竞技场 **Arena.AI 的 T2V 与 I2V 榜单上均排名第 1**（Elo 1450±15 / 1449±11），且是用 720p 击败对手的 1080p 输出。

## 背景与定位
视频生成此前的主流是「短片段 + 弱可控」；Seedance 系列一路从 [[seedance-1-0]] 的视频基座、Seedance 1.5 Pro 的「音视频同步生成」走到 2.0 的「**统一多模态音视频联合生成**」。2.0 的定位是把范式从"生成受限可控性的短视频片段"推到"原生支持多种控制信号的高可控视频合成"，目标是服务字节内部 Doubao / 即梦(Jimeng) / 火山引擎(Volcano Engine) 上**亿级日活**的大规模创作引擎。

技术脉络上它属于字节 Seed 的"全栈生成媒体"家族（技术报告参考文献明确列出）：Seedance 视频系列、[[seedream-4-0]] 等 Seedream 图像/编辑系列、Seed-VL 多模态理解、以及用于视觉生成对齐的奖励/RL 基建 **RewardDance**（reward scaling）与 **DanceGRPO**（把 GRPO 用到视觉生成）。相对 1.5 Pro 的改进集中在：复杂运动/多主体交互的物理可信度、长时一致性、指令遵循、以及把音频从"同步"升级为"双声道高保真 + 多轨"。

> 重要说明：本工作的官方一手资料（arXiv 2604.14148 技术报告 + Seed 官方博客 + 产品页）以**评测报告 + 能力展示**为主体，**未公开模型架构、数据、训练、推理工程的具体技术细节**。下文凡涉及这些维度均如实标注"未披露"，不做臆测。

## 模型架构
- **总体**：官方表述为"a unified, highly efficient, and large-scale architecture for multi-modal audio-video joint generation"（统一、高效、大规模的多模态音视频联合生成架构）。博客进一步提到依赖"**sparse architecture**（稀疏架构）的效率"与"多模态联合训练的强泛化"——暗示是某种稀疏/MoE 类设计，但**未给出 backbone 类型（DiT/MMDiT/AR/掩码生成）、visual tokenizer / VAE、text/audio encoder、条件注入方式、参数量等任何结构细节，均未披露**。
- **多模态输入**：原生支持 text / image / audio / video 四模态混合输入。开放平台上限：最多 **3 段视频 + 9 张图 + 3 段音频** + 自然语言指令；模型可从输入素材中参考画面构图、镜头语言(cinematography)、运动节奏、特效、音频等元素，甚至可直接参考**文字分镜脚本(storyboard)**。
- **输出规格**：原生支持 **4–15 秒**、**480p / 720p** 分辨率的音视频；支持 **15s 高质量多镜头(multi-shot)** 音视频输出。
- **音频侧**：升级的音频生成模块集成**双声道(binaural / two-channel stereo)技术**，支持**背景音乐 / 环境音效 / 人物配音多轨并行输出**，并与画面节奏严格时间对齐。
- **加速版本**：提供 **Seedance 2.0 Fast**——为低延迟场景设计的加速变体（加速手段未披露）。
- **接入**：模型 id `doubao-seedance-2-0-260128`，已上线 Doubao / 即梦 / 火山引擎方舟(Ark)。

## 数据
**未披露**。技术报告与官方博客均未公开训练数据的来源、规模、图文/视频/音频对数量、配比、清洗过滤、re-captioning、合成数据、美学/安全过滤等任何细节。仅在结论中提到模型依赖"extensive world knowledge（大量世界知识）"与"multimodal joint training（多模态联合训练）的强泛化"。

## 训练方法
**训练目标 / 多阶段流程 / 蒸馏加速等核心方法均未在本次发布中披露**。可由参考文献间接推断的对齐/RL 基建（属字节 Seed 既有工作，非本报告新方法）：
- **RewardDance**（arXiv 2509.08826）：视觉生成中的奖励缩放(reward scaling)。
- **DanceGRPO**（arXiv 2505.07818）：将 GRPO 应用于视觉生成的强化学习。
报告结论明确表示团队将"持续探索大模型与人类反馈之间的深度对齐"，暗示评测背后存在 RLHF / 偏好对齐链路，但 **2.0 的具体训练目标(diffusion / flow matching / next-token)、阶段划分、奖励模型、超参与 trick 均未公开**。

## Infra（训练 / 推理工程）
**未披露**。算力规模 / GPU·时 / 并行分布式 / 混合精度 / 吞吐、推理加速（步数、缓存、量化、蒸馏）等均无一手数据。唯一相关线索：提供 **Seedance 2.0 Fast** 加速变体面向低延迟场景；服务部署形态为云端 API（Doubao / 即梦 / 火山引擎），支撑"亿级日活"产品生态。

## 评测 benchmark（把效果讲清楚）
官方用两套评测：自建专家基准 **SeedVideoBench 2.0**（覆盖 T2V / I2V / R2V，与媒体行业专家共建评测集与协议）+ 第三方众包 **Arena.AI（前 LMArena）**。

**Arena.AI 真人偏好榜（2026-04-08 访问）**——以 Dreamina/即梦 Seedance 2.0 720p 参评：
- **T2V 榜第 1**：Elo **1450 (±15)**，领先第二名 veo-3.1-audio-1080p **79 分**。
- **I2V 榜第 1**：Elo **1449 (±11)**，领先 grok-imagine-video-720p **29 分**。
- 关键点：在 **720p** 分辨率下击败运行在 **1080p** 的对手，官方据此论证"运动动态与视觉连贯性的提升比单纯分辨率在感知上更显著"。两榜 Rank Spread 均为 1↔1（稳定居首）。

**SeedVideoBench 2.0 — T2V 总体（1–5 分制，Table 1，Seedance 2.0 行）**：Motion **3.75**、Video Prompt Following **3.43**、Aesthetics **3.67**、Audio Quality **3.63**、Audio-Visual Sync **3.75**、Audio Prompt Following **3.56**——在六个子维度上为参评模型（Kling 2.6 / Kling 3.0 / Sora2 Pro / Veo3.1 / Seedance 1.5）中最高。可用率(usability, score≥3)上 Seedance 2.0 是**唯一六维 usability 均 >83%** 的模型（运动质量达 97.55%；Table 2）。

**SeedVideoBench 2.0 — I2V（Table 10 等）**：Seedance 2.0 是**唯一六维 usability 均 >87% 的模型**。音频维度差距尤其大——**音频质量 usability 97.42% / satisfaction 57.08%**，而 Kling 2.6、Wan 2.6 的音频 usability < 28%（大部分音频被判不可接受）；音频指令遵循 satisfaction 63.52%，是 Seedance 1.5 Pro(37.77%) 的 1.7×、Kling 2.6(5.70%) 的 10× 以上。

**SeedVideoBench 2.0 — R2V 多模态参考/编辑（Table 24）**：Seedance 2.0 在全部五维居首——Multimodal Task Following **2.50**、Prompt Following **2.52**（1–3 制），Editing Consistency **3.54**、Reference Alignment **3.03**、Motion Quality **3.24**（1–5 制）。对比 Kling 3 Omni / Kling O1 / Vidu Q2 Pro：编辑一致性差距最小（Kling 3.0 落后 0.17），运动质量差距最大（对手落后 0.86–0.94），参考对齐落后 0.66–1.24。任务覆盖面也最广——Table 25 报告 Seedance 2.0 **支持 22 类输入任务中的 20 类**（Kling 3 Omni 9/22、Vidu Q2 Pro 13/22、Kling O1 10/22），独家支持**视效/创意参考(3 个变体) + 续拍/延展(4 个变体) 共 7 类任务**（图+音组合参考非独家，竞品亦支持；全模型均不支持的两类为「主体音视频+音频参考」「视频音频编辑」）。

**雷达图（官方图，三张已落盘）**：T2V/I2V/R2V 三张雷达图中 Seedance 2.0 的包络线均在最外层、各维领先；对手覆盖 Sora 2 Pro、Veo 3.1、Kling 3.0/2.6、Wan 2.6、Vidu Q2 Pro、Kling O1 等。

> 注意：官方**未报告** FID / FVD / CLIPScore / VBench 等传统自动化指标（报告明确说 Arena 不依赖 FVD/CLIPScore 这类指标），评测以专家打分 + 真人偏好为主。以上数字全部来自已抓取的一手报告/图，未做任何编造；报告未给出的项写为"未报告/未披露"。

## 创新点与影响
- **核心贡献**：把视频生成从"音视频同步"推进到"**统一多模态音视频联合生成**"——同一架构吞文/图/音/视四模态、单次混合多素材参考(最多 9 图 + 3 视频 + 3 音频)，并把**双声道高保真 + 多轨音频**做进原生输出；在复杂运动/多主体交互的物理可信度与长时一致性上取得明显提升。
- **可控性范式**：支持**视频编辑**（对指定片段/角色/动作/剧情做定向修改）、**视频延展/续拍(extension/continuation)**、prompt 驱动的自动镜头规划(directorial/cinematographic reasoning)，把"导演级控制"交给普通用户。
- **影响**：作为闭源产品级旗舰，刷新了 Arena T2V/I2V 真人偏好榜并以 720p 胜 1080p，给同期 Sora 2 Pro / Veo 3.1 / Kling 3.0 / Wan 2.6 等设定了新的"音视频一体 + 多模态参考"标杆；其 SeedVideoBench 2.0 评测协议（含音频维度、R2V 22 类任务）也是一个可对标的能力清单。
- **已知局限**（官方自述）：细节稳定性、超写实质感、动态生命力仍需打磨；偶发音频失真；多主体一致性、文字渲染准确率、复杂编辑效果仍有优化空间。**且本次发布未公开任何架构/数据/训练/推理工程细节**，从研究复现角度信息密度低——本质是一份"评测+能力"报告而非方法论文。

## 原始链接
- blog（官方发布）: https://seed.bytedance.com/en/blog/official-launch-of-seedance-2-0
- project_page（产品页 / SeedVideoBench 2.0 雷达图）: https://seed.bytedance.com/en/seedance2_0
- tech-report（arXiv 2604.14148, "Seedance 2.0: Advancing Video Generation for World Complexity", v1 2026-04-15）: https://arxiv.org/abs/2604.14148
- pdf: https://arxiv.org/pdf/2604.14148
- 接入页（火山引擎方舟，model id doubao-seedance-2-0-260128）: https://www.volcengine.com/experience/ark?mode=vision&modelId=doubao-seedance-2-0-260128&tab=GenVideo

## 本地落盘文件
- ../../../sources/omni/2026/arxiv-2604.14148.pdf
- ../../../sources/omni/2026/seedance-2-0--blog.md
- ../../../sources/omni/2026/seedance-2-0--project-page.md
- ../../../sources/omni/2026/seedance-2-0--eval-t2v.jpg
- ../../../sources/omni/2026/seedance-2-0--eval-i2v.jpg
- ../../../sources/omni/2026/seedance-2-0--eval-multimodal.jpg
