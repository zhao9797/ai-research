---
title: "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets"
org: "Stability AI"
country: EU
date: "2023-11"
type: paper
category: video
tags: [video, image-to-video, text-to-video, latent-diffusion, data-curation, open-source, edm, multi-view]
url: "https://arxiv.org/abs/2311.15127"
arxiv: "https://arxiv.org/abs/2311.15127"
pdf_url: "https://arxiv.org/pdf/2311.15127"
github_url: "https://github.com/Stability-AI/generative-models"
hf_url: "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt"
modelscope_url: ""
project_url: "https://stability.ai/news/stable-video-diffusion-open-ai-video-model"
downloaded: [arxiv-2311.15127.pdf, stable-video-diffusion--ar5iv-fulltext.md, stable-video-diffusion--github-readme.md, stable-video-diffusion--hf-xt-card.md, stable-video-diffusion--hf-svd-card.md, stable-video-diffusion--hf-xt-1-1-page.md, stable-video-diffusion--stability-blog.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Stable Video Diffusion（SVD）是 Stability AI 在 [[align-your-latents-vldm]]（Video LDM）基础上做的**开源高分辨率图生视频/文生视频底座**，核心贡献不是新架构而是把"潜空间视频扩散"**系统化为三阶段训练流水线（图像预训练 → 视频预训练 → 高质量微调）并配套一套可量化、靠人评消融出来的视频数据筛选方法**；其图生视频模型在人评中**优于当时闭源的 Runway GEN-2 与 Pika Labs**，文生视频在 UCF-101 上零样本 FVD=242.02 显著领先同期开源/闭源基线，并成为后续开源视频生成（SVD-XT/SV3D/SV4D、社区微调）的主力基座。

## 背景与定位
2023 年的视频扩散工作（[[align-your-latents-vldm]] / Make-A-Video / [[modelscope-t2v]] / [[i2vgen-xl]] / [[animatediff]]）已经普遍采用"拿预训练 T2I 模型 + 插入时序层 + 在小规模高质量视频上微调"的范式，但论文指出两大空白：

1. **架构插法被反复研究，数据策略却没人系统做**——各家训练数据、清洗方式、配比千差万别，领域没有公认的视频数据 curation 方案。
2. **缺乏对"预训练阶段是否值得、怎么筛"的可控对照实验**。

SVD 的定位正是补这个洞：它把训练显式拆成三阶段（Stage I 图像预训练 / Stage II 视频预训练 / Stage III 高质量视频微调），并用**人偏好（Elo / user preference）作为筛选信号**，逐一消融"图像预训练是否有用、数据筛选是否有用、筛选优势能否穿透到微调后"。结论是：**精心筛选的大规模预训练数据带来的优势在 50k 步高质量微调后依然保持**——这是该工作最重要的方法论断言。技术脉络上它是 [[align-your-latents-vldm]] 的直接工程化继承（沿用其时序层插入方式），并把 [[sdxl]] 时代的图像数据 curation 经验迁移到视频。

## 模型架构
- **Backbone：U-Net（非 DiT）**。以 **Stable Diffusion 2.1（SD 2.1）** 的空间 U-Net 为图像骨干，在其**每个空间层之后插入时序卷积 + 时序注意力层**（沿用 Video LDM [Blattmann et al.] 的精确设置）。
- **参数量**：插入的时序层共 **656M 新参数**，使 U-Net 总参数（空间+时序）达到 **1521M（约 1.5B）**。
- **Latent / VAE**：复用 SD 2.1 的**空间自编码器（KL-VAE，f8 下采样、潜通道 c=4）**逐帧编码，不引入 3D VAE；潜空间形状典型为 `c=4, h=52, w=128`（对应 576×1024 像素帧经 f8）。为缓解逐帧解码导致的闪烁，**额外微调了一个 f8 时序解码器（temporal decoder）以提升时间一致性**（HF model card 明确给出；同时也提供逐帧标准解码器 `svd_xt_image_decoder.safetensors`）。
- **文本/图像条件**：T2V 用 SD 2.1 的 CLIP 文本编码器做交叉注意力条件；**I2V 把文本 embedding 替换为条件帧的 CLIP 图像 embedding**，并把**经噪声增强（noise augmentation）的条件帧在通道维 concat 到 U-Net 输入**（条件帧过 SD 2.1 encoder，取分布均值，沿时间轴复制）。
- **Micro-conditioning**：在 [[sdxl]] 思路上引入对 **frame rate（fps）与 motion score** 的微条件，使推理时可调运动幅度与帧率。
- **分辨率策略**：图像预训练 512×512 → 256×384；视频预训练 14 帧 @256×384 → 320×576；高分辨率微调 576×1024（T2V 14 帧；I2V 14 帧 / 25 帧）。
- **运动控制**：在**时序注意力块上训练 Camera Motion LoRA（rank 16，5k 步）**，分 horizontal / zoom / static 三类，可对同一条件帧施加不同相机运动。
- **帧插值变体**：把输出帧从 14 降到 5（首尾为条件帧），用 mask embedding 构造 `{z_s, z_m, z_m, z_m, z_e}` 序列 concat 到噪声输入（U-Net 输入形状 (5,9,52,128)），学习在两帧间补 3 帧、把帧率提升 4×；仅需 ≈10k 步即收敛。

## 数据
论文最重要的部分。数据集自建，命名为 **Large Video Dataset (LVD)**：

- **初始采集与切分**：收集长视频，用 **PySceneDetect 级联式（三档 FPS）做镜头切分（cut detection）**，避免转场/淡入淡出泄漏进生成视频。处理后检出的切片数约为元数据切分的 **~4×**，说明原始视频含大量未标注切点。
- **合成字幕（每片 3 条）**：① 图像字幕器 **CoCa** 标注中间帧（擅长空间细节）；② 视频字幕器 **V-BLIP / VideoBLIP**（捕捉时序）；③ 用轻量 **LLM** 把前两者总结合并。用 Elo 评比三种字幕的下游收益。
- **LVD 规模**：正文称 **580M 个标注视频切片对**（Tab.1 的 #Clips 列精确给 **577M**，两数同指 LVD，正文取整），单片均时长 11.58s，总时长 **212.09 年**，均 325 帧、均每视频 11.09 切片。
- **额外标注用于过滤**：
  - **稠密光流（dense optical flow，2 FPS 计算）**→ 滤掉平均光流幅度低于阈值的**近静态切片**；
  - **OCR**→ 剔除含大量文字的切片；
  - 对首/中/尾帧抽 **CLIP embedding**，算**美学分数（aesthetics）与文本-图像相似度（CLIP score）**。
- **筛选方法（靠人评定阈值）**：从 LVD 随机抽 **9.8M 子集（LVD-10M）**，对每类标注（CLIP 分、美学分、OCR 率、光流分、字幕类型）**系统地删去最差的 12.5% / 25% / 50%**，对每个阈值各训一个同超参模型，用 **Elo 人偏好排名**选出每类最优阈值（字幕类型用 Elo 排名而非删比例）。把该方案施加到全量 LVD → **过滤后预训练集 LVD-F = 152M（1.52 亿）切片**。
- **高质量微调集**：约 **250K 高视觉保真预字幕切片**用于基模 Stage III；**~1M 高质量样本**（含大量物体运动、稳定相机运动、对齐良好的字幕）用于高分辨率 T2V/I2V 微调。
- **多视图数据**：Objaverse 子集 **150K** CC 授权 3D 物体（每个渲 21 帧 360° 轨道视频，仰角 [−5°,30°]）+ MVImgNet **~200K 训练/900 测试**。

## 训练方法
- **训练目标**：**连续噪声的 EDM 框架（Karras et al.）**。从 SD 2.1 的离散噪声调度迁移到连续噪声 + EDM preconditioning（σ_data=1）；噪声分布 `log σ ~ N(P_mean, P_std)`，权重 `λ(σ)=(1+σ²)σ⁻²`。
- **三阶段流水线**：
  - **Stage I 图像预训练**：以 SD 2.1 为底，先冻结、只训 time-embedding 1k 步（512×512）适配新 preconditioning，再全量训 30k 步（256×384），P_mean=−1.2, P_std=1。
  - **Stage II 视频预训练**：插入 656M 时序层后，在 **LVD-F** 上训 **14 帧 @256×384，150k 步，AdamW，lr=1e-4，batch=1536**，文本条件 dropout 15%（为 CFG）；再升到 **320×576 训 100k 步**，batch=768，**把噪声调度整体右移（增大 P_mean=0，加更多噪声）**。全程对 fps 与 motion score 做条件。
  - **Stage III 高质量微调**：在 ~1M 高质量集上 576×1024 微调（T2V 50k 步，batch=768，lr=3e-5，P_mean=0.5/P_std=1.4，EMA 0.9999；I2V 同设置但 P_mean=1.0/P_std=1.6，先在 320×576 预热 50k 步 P_mean=0.7）。
- **关键 trick**：
  - **高分辨率/强条件时把噪声调度右移**（更多噪声），印证 Hoogeboom et al. 对图像扩散的结论——SVD 把它确认到视频。
  - **I2V 的线性递增 guidance**：沿帧轴把 CFG scale 从小到大线性增大，缓解"过小→与条件帧不一致、过大→过饱和"。
  - I2V 不用 masking，条件帧沿时间轴直接复制；条件帧加 `log σ ~ N(−3.0, 0.5²)` 的小噪声后过 encoder。
- **未使用蒸馏/一致性加速**：论文未做 LCM/ADD 类步数蒸馏（SVD 的快速化由后续社区/SDXL-Turbo 线另行解决）。
- **SVD 1.1（HF xt-1-1）**：从 25 帧 XT 进一步微调，**固定条件 6FPS + Motion Bucket Id=127**，以在不调超参的情况下提升输出一致性。

## Infra（训练 / 推理工程）
- **整体训练算力规模论文未完整披露**（未给总 GPU·时 / 集群规模 / 并行策略 / 精度配置）。
- **多视图微调给了具体数字**：SVD-MV 全部模型训 **12k 步（~16 小时），8×A100 80GB，总 batch=16，lr=1e-5**；相比之下 SyncDreamer 在 Objaverse 上要训 4 天——SVD 视频先验让多视图微调收敛极快（1k 步即超越图像先验/无先验对照）。
- **推理与部署**：开源 `generative-models` 仓库提供 `simple_video_sample.py` 与 Streamlit demo；I2V XT 默认 25 帧 @576×1024；低显存可设 `--decoding_t=1 / --encoding_t=1`（逐帧编解码）或降分辨率到 512。官方说明可在 **3–30 FPS** 可调帧率下生成。推理步数等扩散采样细节走标准 EDM 采样器。

## 评测 benchmark（把效果讲清楚）
**数字均来自论文（arxiv-2311.15127.pdf）与 HF model card，未报告处明确标注。**

- **零样本文生视频 UCF-101（FVD↓，数值取自文献）：**
  | 方法 | FVD↓ |
  |---|---|
  | CogVideo (ZH) | 751.34 |
  | CogVideo (EN) | 701.59 |
  | MagicVideo | 655.00 |
  | [[align-your-latents-vldm]] (Video LDM) | 550.61 |
  | Make-A-Video | 367.23 |
  | PYOCO | 355.20 |
  | **SVD (ours)** | **242.02** |

  SVD 基模显著优于所有列出基线，验证其学到强运动表示。

- **图生视频人偏好（user preference study）**：25 帧 I2V 模型在视觉质量上**被人评偏好于 Runway GEN-2 与 Pika Labs（PikaLabs）两个闭源模型**（论文 Fig.6、HF card 复述）。具体胜率柱状图给出但未列精确百分比。

- **多视图 GSO 测试集（50 物体）：**
  | 方法 | LPIPS↓ | PSNR↑ | CLIP-S↑ |
  |---|---|---|---|
  | Zero123 | 0.18 | 14.87 | 0.87 |
  | Zero123XL | 0.20 | 14.51 | 0.87 |
  | SyncDreamer | 0.18 | 15.29 | 0.88 |
  | Scratch-MV | 0.22 | 14.20 | 0.76 |
  | SD2.1-MV | 0.18 | 15.06 | 0.83 |
  | **SVD-MV (ours)** | **0.14** | **16.83** | **0.89** |

  SVD-MV 在三项指标上均最优，且只需 12k 步/16 小时即超越需训 4 天的 SyncDreamer——证明**视频先验 > 图像先验 > 无先验**。

- **关键消融结论（全部基于人评 Elo / preference）：**
  - **图像预训练有用**：从预训练 SD 初始化空间层的视频模型，在质量与 prompt 跟随上都明显优于随机初始化（Fig.3a）。
  - **数据筛选有用且可跨规模**：四倍小的 **LVD-10M-F 击败 LVD-10M、WebVid-10M、InternVid-10M**（后两者还专门筛过美学，且大 4 倍）；在 50M 规模上 curated 同样胜 uncurated（Fig.4）。
  - **数据量也重要**：50M curated 优于 10M-F 同步数。
  - **预训练优势穿透微调**：50k 步高质量微调后，从 curated 预训练权重接续的模型 Elo 仍持续高于"从 uncurated 视频权重"和"直接从图像模型微调"（Fig.4e）。

## 创新点与影响
**核心贡献**
1. **系统化三阶段训练配方**（图像预训练 → 视频预训练 → 高质量微调），并用对照实验证明每一阶段的必要性与"预训练优势可穿透微调"。
2. **可量化、靠人评消融出阈值的视频数据 curation 流水线**（cut detection + 三路合成字幕 + 光流/OCR/CLIP/美学过滤），把 580M LVD 精炼为 152M LVD-F，证明"小而精"胜"大而杂"。
3. **强运动/多视图先验**：同一底座可低成本微调出 I2V、帧插值、Camera-Motion LoRA、多视图（SVD-MV），且多视图收敛极快。
4. **开源底座**：代码 + 权重开放（`generative-models`），14/25 帧 I2V、3–30 FPS 可调。

**影响**：SVD 成为开源视频生成事实标准底座，直接催生 Stability 自家 **SV3D / SV4D / SV4D 2.0**（GitHub README 已迭代到 SV4D 2.0），并被社区大量微调/适配（如配合 ControlNet、运动控制、长视频采样）。其"数据 curation 决定视频生成质量"的论断深刻影响后续视频模型的数据方法论；EDM + 噪声右移 + 线性 guidance 等工程 trick 被广泛借鉴。

**已知局限**（论文/官方明示）：
- 发布时官方定位为 **research preview，不建议真实/商用场景**（后续 license 才放开商用，见 HF card）。
- 生成视频可能**无运动或仅极慢相机平移**；可能无法完美写实、文本渲染差、人脸/人物可能畸变。
- 时序逐帧 VAE 解码会闪烁，需额外的时序 decoder 缓解。
- 训练总算力/集群/并行/精度等 infra 细节未在论文披露。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.15127
- arxiv_pdf: https://arxiv.org/pdf/2311.15127
- github: https://github.com/Stability-AI/generative-models
- hf (I2V-XT, 25 帧): https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt
- hf (I2V, 14 帧): https://huggingface.co/stabilityai/stable-video-diffusion-img2vid
- hf (XT-1.1): https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt-1-1
- official blog: https://stability.ai/news/stable-video-diffusion-open-ai-video-model

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.15127.pdf
- ../../../sources/omni/2023/stable-video-diffusion--ar5iv-fulltext.md
- ../../../sources/omni/2023/stable-video-diffusion--github-readme.md
- ../../../sources/omni/2023/stable-video-diffusion--hf-xt-card.md
- ../../../sources/omni/2023/stable-video-diffusion--hf-svd-card.md
- ../../../sources/omni/2023/stable-video-diffusion--hf-xt-1-1-page.md
- ../../../sources/omni/2023/stable-video-diffusion--stability-blog.md
