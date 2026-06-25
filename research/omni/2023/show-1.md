---
title: "Show-1: Marrying Pixel and Latent Diffusion Models for Text-to-Video Generation"
org: "Show Lab, National University of Singapore"
country: China
date: "2023-09"
type: paper
category: video
tags: [text-to-video, diffusion, pixel-diffusion, latent-diffusion, cascade, expert-translation, deepfloyd-if, webvid, vbench]
url: "https://arxiv.org/abs/2309.15818"
arxiv: "https://arxiv.org/abs/2309.15818"
pdf_url: "https://arxiv.org/pdf/2309.15818"
github_url: "https://github.com/showlab/Show-1"
hf_url: "https://huggingface.co/showlab"
modelscope_url: ""
project_url: "https://showlab.github.io/Show-1/"
downloaded: [arxiv-2309.15818.pdf, show-1--readme.md, show-1--hf-base-card.md, show-1--hf-interp-card.md, show-1--hf-sr1-card.md, show-1--hf-sr2-card.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Show-1 是第一个把**像素扩散（pixel VDM）与潜扩散（latent VDM）混搭**的文生视频级联框架：用低分辨率像素扩散生成"文本对齐强"的关键帧，再用潜扩散做高效超分。代价端最亮眼——推理峰值显存仅 **15GB（纯像素方案需 72GB）**，且在 UCF-101/MSR-VTT/VBench 上达到当时 SOTA，并且只用公开数据 WebVid-10M + InternVid、64×A100-40G 就训出来（同期 LaVie/VideoCrafter/ModelScope 用 128×A100-80G 内部数据）。

## 背景与定位
2023 年文生视频扩散模型（VDM）分两大流派，各有死结：
- **像素 VDM**（[[make-a-video]]、Imagen Video、PYoCo）直接在 RGB 空间去噪。优点：从极低分辨率（如 64×40）起步生成，运动与文本对齐准、运动保真度高；缺点：高分辨率阶段算力/显存爆炸。
- **潜 VDM**（[[align-your-latents-vldm]] / Video LDM、MagicVideo）在 VAE 压缩潜空间操作，省算力；但小潜空间（64×40 视频 → 8×5 潜码）装不下文本描述的丰富语义，**文本-视频对齐弱**；若直接生成较高分辨率（256×160）以扩容潜空间，模型又会偏重空间外观、忽略文本对齐。

Show-1 的核心洞察来自一项控制实验（论文 Fig.2 / Tab.4）：**在关键帧阶段，64×40 的像素 VDM（f=0）在 CLIP-SIM、文本对齐、运动保真度三项上全面碾压各种分辨率/压缩比的潜 VDM**，而潜 VDM 在最终高分辨率超分阶段才显出省显存的价值。于是 Show-1 提出"低分辨率用像素、高分辨率用潜"的混合级联，并配套一个让潜 VDM 能干净接管超分的 **expert translation（专家翻译）** 方法。技术脉络上它继承 [[ddpm]] 训练目标、[[latent-diffusion-ldm]] 的潜空间思想、Imagen Video 的级联+噪声条件增强、SDEdit 的加噪-去噪范式，并以 [[deepfloyd-if]] 作为像素阶段的强初始化。落盘版为 arXiv v3（2025-05-30，Springer 期刊模板）；据官方 README News，已于 2024-10-06（原文 `10/06/2024`，MM/DD）被 IJCV 接收。

## 模型架构
**总体：4 阶段级联，前 3 段像素 VDM，最后 1 段潜 VDM。** 所有阶段都把 T2I 的 2D UNet 改造成 Video UNet。

**Image-UNet → Video-UNet 改造（Fig.5）**：沿用强 T2I 模型的空间权重，在每个 UNet block 内插入时间层——
- 每个 ResNet2D 之后加一层 **temporal conv**（4 个沿时间维的 1D 卷积）；
- 每个空间 self-/cross-attention 之后加一层 **temporal attention**。
- 用 einops `rearrange` 在空间注意力（把时间维并入 batch）与时间注意力（把空间维并入 batch）之间切张量。文本经 cross-attention 注入（K、V 来自文本嵌入）。
- 训练时**只更新新增的时间层、冻结空间层**（frontmatter 截图中 ❄ 标注的 self/cross-attn 与 ResNet2D 即冻结部分）。

**四个阶段（Fig.4 / Fig.6）**：
1. **关键帧（base，像素）**：文本 → 8 帧 × 64×40 关键帧。低分辨率使模型不必操心清晰度/时序一致性，从而把注意力让给文本引导。论文论证为何此处用像素而非潜：64×40 若再过 8× VAE 压缩只剩 8×5，语义装不下；降低压缩比（2×）则效率与像素扩散相当、还得额外训 autoencoder，得不偿失。
2. **时间插帧（interpolation，像素）**：把关键帧从 2fps 插到 7.5fps（论文实现：8 帧→29 帧）。沿用关键帧 UNet 结构，**首层卷积输入通道扩容**以容纳"被 mask 的关键帧"作为条件——按通道拼接 `noisy(C) + cond关键帧(C) + mask(1)`，对每段 5 帧预测中间 3 帧。对条件关键帧加 **noise conditioning augmentation**（小幅随机噪声）缩小级联各阶段的域差。
3. **低分辨率超分（SR1，像素）**：64×40 → 256×160（4× 空间）。把双线性上采样后的低分视频按通道拼到噪声上 `[noisy, x_resized]` 输入 UNet；用 Imagen Video 式高斯噪声增强，采样时取固定信噪比（如 1 或 2）。因 24GB 卡装不下全部插帧，需切成 4 段分别超分，再用前一段最后一帧补到下一段首帧的额外通道实现**自回归衔接**。
4. **高分辨率超分（SR2，潜 + expert translation）**：256×160 → 576×320。这是唯一的潜 VDM，专门用来去除前序阶段的伪影/时序崩坏。

**Expert translation（本文最关键的方法创新，Sec.3.6）**：相对标准 SDx4 潜上采样器做两处改造——
- **改输入**：不再"低分视频+噪声按通道拼接喂 UNet"，而是按 **SDEdit** 把（编码后的）低分视频线性插值到高分、在某中间时刻 t（如 900）加噪，再从 t→0 去噪。这样直接复用低分视频的外观与文本对齐，不引入额外通道。
- **expert finetuning**：注意到不同扩散步分工不同（早期步恢复整体结构、后期步雕细节，引自 eDiff-I）。既然低分阶段已给出结构良好的视频，就把潜 VDM 训练**只覆盖 timestep 0–900**（满量程 1000），使其成为"高分辨率细节精修专家"。配合 SDEdit 从中间步 900 起跳推理，恰好不需要 900–1000 这段被裁掉的知识。

各阶段初始化（来自 HF model card，论文正文未逐段列出）：
- base ← **DeepFloyd/IF-I-L-v1.0**（像素级联 T2I）
- interpolation ← show-1-base
- SR1 ← **DeepFloyd/IF-II-M-v1.0**（首帧图像超分另用 IF-II-L-v1.0）
- SR2 ← **cerspense/zeroscope_v2_576w**（基于 ModelScope 的潜 VDM）

**文本编码器**：消融实验统一用 **T5**（Raffel et al. 2020）；与 SOTA 比较时整体以 DeepFloyd-IF 为初始化（IF 本身用 T5-XXL）。

**参数量（Tab.5，Make-A-Video / Show-1 对比）**：关键帧 3.1B/**1.7B**、插帧 3.1B/**1.7B**、SR1 1.4B/**0.8B**、最终超分 0.7B/**1.8B**，合计 9.6B/**6B**。

## 数据
- **训练数据全部公开**：核心是 **WebVid-10M**（Bain et al. 2021，10M 视频-文本对）；base/关键帧阶段额外使用 **InternVid**（OpenGVLab，来自 HF base model card）。interpolation、SR1、SR2 三阶段均在 WebVid-10M 上微调。
- **图像初始化来源**：消融统一从 **LAION** 预训练的图像模型权重起步；正式模型以 DeepFloyd-IF（其图像端在 LAION 上训练）为基础。
- **未披露**：未报告自建/合成数据、re-captioning、美学过滤、安全过滤等细节——本文定位是"用纯公开数据做到 SOTA"，数据工程不是其卖点。
- 论文反复强调对比公平性：消融中像素/潜 VDM 用**同一 T5、同一 LAION 初始化、同等参数量、同等训练步数**。

## 训练方法
- **训练目标**：标准 DDPM 噪声预测 ε-prediction（论文 Eq.1–3），文本条件化版本对 ε_θ(x_t, t, c) 做 L2 回归。插帧/SR1 阶段把条件（mask 关键帧 / 上采样低分视频）按通道拼进输入再预测噪声。
- **多阶段范式**：4 段**独立训练、级联推理**；非"预训练→SFT→RLHF"那套 LLM 流程，而是经典 cascaded diffusion。各阶段都用**噪声条件增强**（向上一阶段输出的条件帧注入随机噪声）来抹平训练真实数据与推理合成数据之间的域差——这是 Imagen Video 提出、本文沿用的级联关键 trick。
- **快速收敛 trick**：插帧模型复用关键帧权重（除首层卷积新增的 4 个输入通道外）做微调，加速收敛。
- **Expert finetuning**（见上）：SR2 只在 timestep 0–900 上训练，是本文独有的"扩散步专精"训练改动。Tab.6 消融证明其有效：SDx4+temporal（FVD 459 / IS 32.98）→ 仅改输入的 expert translation（FVD 423 / IS 33.83）→ 再加 expert finetuning（**FVD 383 / IS 35.67**）。
- **推理步数（Tab.5，本文/对手）**：关键帧 75 步、插帧 75 步、SR1 50 步、SR2 40 步。
- **未使用**：无 flow matching / rectified flow，无一致性蒸馏 / LCM / ADD 等步数蒸馏（2023-09 这些与本文并行或稍晚）。

## Infra（训练 / 推理工程）
- **训练算力**：**64×A100-40GB**。论文明确对比：LaVie / ModelScope / VideoCrafter 用 **>128×A100-80GB** 加大规模内部数据——Show-1 用更少的卡、更少的数据、纯公开语料即达到/超越它们，是其核心工程卖点。
- **推理显存（最大卖点）**：全流程峰值 **15GB**（混合方案）vs 纯像素方案 72GB（用像素 VDM 做最终超分）/ Make-A-Video 0.7B 像素超分仍需 52GB（本文复现，Tab.4/Tab.5）。关键帧阶段已确认可在 24GB 卡上跑；SR1 因显存限制需把帧分 4 段、用自回归衔接。
- **速度（Tab.5，复现 Make-A-Video 同架构对比）**：总推理时间 256s/**178s**（本文更快）；分阶段显存关键帧 18GB/**11GB**、插帧 14GB/**10GB**、SR1 52GB/**14GB**、最终超分 54GB/**15GB**。
- **部署形态**：开源权重（base/interpolation/sr1/sr2 四个 ckpt 在 HF showlab，CC-BY-NC-4.0），提供 diffusers 实现、Gradio Space、Colab、Replicate Demo；代码 `python run_inference.py` 自动拉取权重。
- 计算资源来自新加坡国家超算中心（NSCC）。**未披露**：精度（fp16/bf16）、并行/分布式策略、GPU·时、吞吐量化等具体工程数字。

## 评测 benchmark（把效果讲清楚）
**UCF-101 零样本（Tab.1，IS↑ / FVD↓）**：
- Show-1（resized）IS **35.67** / FVD **383.46**；Show-1（在方形视频上微调）FVD **369.33**。
- 对手（Tab.1，IS/FVD）：Make-A-Video 33.00 / 367.23、Video LDM 33.45 / 550.61、VideoFactory 36.02 / 410.00、MagicVideo —/655.00、CogVideo(En) 25.27 / 701.59。
- 结论：Show-1 仅用公开 WebVid-10M，IS/FVD 与依赖大规模内部数据的 Make-A-Video 持平或更优。

**MSR-VTT 零样本（Tab.2，FID-vid↓ / FVD↓ / CLIPSIM↑）**：
- Show-1：FID-vid **12.97**（第二好）、FVD **536**（**最佳**）、CLIPSIM **0.3104**（**最佳**）。
- 对手（仅列源表能可靠对位的值）：ModelScopeT2V FID-vid **11.09**（最佳）、FVD 550、CLIPSIM 0.2930；Make-A-Video CLIPSIM **0.3049**（FID-vid/FVD 本表未报告）；MagicVideo FID-vid 13.17、CLIPSIM 0.2929；CogVideo(En) FID-vid 23.59、CLIPSIM 0.2631；Video LDM CLIPSIM 本表未报告。（原表 FVD 列仅 4 值、FID-vid 列 6 值、CLIPSIM 列 7 值——部分方法对应指标缺测，逐方法对位以 ModelScopeT2V 技术报告同表为准。）
- Show-1 的 CLIPSIM 0.3104 超过有额外训练数据的 Make-A-Video（0.3049），体现强文本-视频语义一致性。

**VBench（Tab.3，16 维，对比 LaVie/ModelScope/VideoCrafter/CogVideo）**：Show-1 **16 项中领先 10 项**。代表性维度——Subject Consistency **95.53%**（最高）、Background Consistency **98.02%**、Multiple Objects **45.47%**（最高，次高 38.98%）、Spatial Relationship **53.5%**（远超次高 36.74%）、Temporal Flickering **99.12%**、Motion Smoothness **98.24%**、Object Class **93.07%**、Aesthetic Quality **57.35%**、Overall Consistency **27.46%**。弱项：Dynamic Degree 44.44%（VideoCrafter 89.72% 更高，说明 Show-1 运动幅度偏保守）、Appearance Style 23.06% 略低于 LaVie。

**人评（Fig.7，AMT，256 条复杂 prompt，三维度两两对比）**：在视频质量、文本-视频对齐、运动保真度**三项全部**胜过 ModelScope/ZeroScope/VideoCrafter0.9/LaVie。论文还称定性上匹配或超过闭源 Imagen Video、Make-A-Video，在文本-视频对齐上超过商用 Gen-2、Pika（Fig.8/9，Gen-2、Pika 难以在视频里正确渲染文字，Show-1 能精确写出 "Show Lab" 字样）。

**关键消融**：
- **关键帧空间/分辨率选择（Tab.4）**：64×40 像素 VDM（f=0）CLIP-SIM **0.3096**、文本对齐胜率 **36%**、运动保真胜率 **23%**、显存 15GB、UCF-FVD 383——全面优于各分辨率/压缩比的潜方案（如 64×40 latent f=8 仅 CLIP-SIM 0.2441、对齐 1%）。证实"低分用像素"的核心论点。
- **最终超分方式（Tab.6）**：expert translation 的两处改动逐项有效（见训练方法节）。

## 创新点与影响
**核心贡献**：
1. **首个像素+潜混合的文生视频框架**：用一组受控实验把"哪个阶段该用像素、哪个该用潜"量化清楚（低分→像素保对齐，高分→潜省显存），给后续级联视频模型提供了清晰的设计准则。
2. **Expert translation**：让标准 SDx4 潜超分器变成能修伪影、保对齐的"高分细节专家"——SDEdit 式改输入 + 仅 0–900 时间步的 expert finetuning，两步都被消融证明有效。
3. **资源效率范本**：推理 15GB、训练仅 64×A100-40G + 纯公开数据，做到 SOTA；对学术界/小团队复现高质量 T2V 是重要参照。
4. **运动定制 / 视频风格化**：仅微调关键帧 UNet 的**时间注意力层**即可把单条视频的运动蒸馏进模型（比 MotionDirector 需分别训空间+时间层更省），固定空间层则保留按文本换外观的能力（Fig.11/12）。

**影响**：开源权重 + diffusers/Colab/Replicate 生态使其成为 2023 年开源 T2V 的常用基线之一；据官方 README News，2024-10-06 被 IJCV 接收（GitHub 上的 Trendshift 收录亦可印证其社区热度）。"低分像素对齐 + 高分潜超分"的混合思路与 expert-translation 加噪精修，为后续级联视频生成与视频超分提供了方法借鉴。

**已知局限**：
- 级联结构推理步骤多、链路长（论文也承认比单阶段慢，但质量更高）；SR1 需把帧切 4 段+自回归衔接，工程上略繁琐。
- **Dynamic Degree 偏低（44.44%）**：运动幅度保守，倾向稳定但不够"动感"。
- 受 WebVid 训练数据制约，画质与多样性上限受公开数据约束；商用需向 NUS 单独申请授权（CC-BY-NC-4.0）。
- 数据工程（合成/重标注/过滤）几乎未涉及，是其相对同期闭源大模型的差距来源。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.15818
- arxiv_pdf: https://arxiv.org/pdf/2309.15818
- github: https://github.com/showlab/Show-1
- project: https://showlab.github.io/Show-1/
- hf_org: https://huggingface.co/showlab
- hf_base: https://huggingface.co/showlab/show-1-base
- hf_interpolation: https://huggingface.co/showlab/show-1-interpolation
- hf_sr1: https://huggingface.co/showlab/show-1-sr1
- hf_sr2: https://huggingface.co/showlab/show-1-sr2

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.15818.pdf
- ../../../sources/omni/2023/show-1--readme.md
- ../../../sources/omni/2023/show-1--hf-base-card.md
- ../../../sources/omni/2023/show-1--hf-interp-card.md
- ../../../sources/omni/2023/show-1--hf-sr1-card.md
- ../../../sources/omni/2023/show-1--hf-sr2-card.md
