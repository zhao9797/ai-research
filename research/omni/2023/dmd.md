---
title: "One-step Diffusion with Distribution Matching Distillation (DMD)"
org: "MIT / Adobe Research"
country: US
date: "2023-11"
type: paper
category: method
tags: [diffusion-distillation, one-step, distribution-matching, vsd, score-distillation, text-to-image, acceleration]
url: "https://arxiv.org/abs/2311.18828"
arxiv: "https://arxiv.org/abs/2311.18828"
pdf_url: "https://arxiv.org/pdf/2311.18828"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://tianweiy.github.io/dmd/"
downloaded: [arxiv-2311.18828.pdf, dmd--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DMD（Distribution Matching Distillation）把一个多步扩散教师蒸馏成**单步**图像生成器：核心是用两个扩散模型分别估计真实分布与"假"分布的 score，二者之差即"更真实、更不假"的梯度（一个近似 KL 散度的梯度），再叠加一项 LPIPS 回归损失稳住模式。结果：ImageNet 64×64 **FID 2.62**（教师 EDM 用 512 次前向得 2.32，DMD 仅差 0.3 却快 512×）、零样本 COCO-30k **FID 11.49**（接近 SD v1.5 教师的 8.78，但单步推理 90ms、约 30× 加速、FP16 下 20 FPS）。CVPR 2024。

## 背景与定位
扩散模型质量高但采样慢，需要几十到几百次网络前向（[[ddpm]]/[[score-sde]] 的迭代去噪本质）。加速路线有两类：(1) 快采样器（[[dpm-solver]]/UniPC，把 1000 步降到 20–50 步，但再压步数质量崩）；(2) 蒸馏。已有蒸馏几乎都在**学 noise→image 的逐点映射**——Progressive Distillation（逐次折半步数）、Rectified Flow/InstaFlow（拉直 ODE 流）、[[consistency-models]]（自一致约束），痛点是要么跑完整去噪轨迹代价高，要么蒸出来的学生质量仍落后教师。

DMD 换了思路：**不要求学生复刻教师的逐点映射，只要求学生生成的整体分布与教师不可区分**。这与 GMMN / GAN 的"分布匹配"动机一致，但绕开了在大规模文生图上训 GAN 的不稳定难题——做法是直接复用一个**已在大规模图文上训好的扩散模型**来提供分布匹配的梯度。其直接前置是 ProlificDreamer 的 **VSD（Variational Score Distillation）**（原用于文本→3D 的 test-time 优化），DMD 把同一思路从"优化单个 3D 物体"扩展为"训练一整个生成网络"，并引入回归损失专门服务于扩散蒸馏。与同期 Diff-Instruct、Score Mismatching 是并行工作，DMD 的差异化在于回归损失 + 文生图 SOTA。后续有 DMD2（项目页明确指向 https://tianweiy.github.io/dmd2/）。

## 模型架构
DMD 本身**不是一个新架构，而是一套蒸馏算法**，复用教师的 denoiser 架构：

- **一步生成器 Gθ**：架构与教师 denoiser 完全相同，但**去掉时间步条件**（time-conditioning）。用教师权重初始化，且初始化为教师在最大噪声处的预测：`Gθ(z) = µ_base(z, T-1)`。输入纯高斯噪声 z，一次前向直出图像。
- **两个 score 网络（critic 角色）**：
  - **real score** `s_real`：固定不动的教师扩散模型 `µ_base` 拷贝，给出真实分布在各噪声尺度下的 score（`s_real = -(x_t - α_t·µ_base)/σ_t²`，mean-prediction 形式，ε-prediction 经变量替换等价）。
  - **fake score** `s_fake`：从教师初始化、**训练中动态更新**的扩散模型 `µ_fake^φ`，追踪生成器当前输出的分布（随训练漂移）。
- **教师/底座**：ImageNet/CIFAR 用 [[elucidating-edm]]（Karras 2022）的预训练模型；文生图用 **Stable Diffusion v1.5**（[[latent-diffusion-ldm]]，潜空间扩散 + VAE + CLIP 文本编码器）。因此文生图版的 text encoder / VAE / 潜空间设计都直接继承 SD v1.5，DMD 不改这些组件。
- **分辨率**：CIFAR-10 32×32、ImageNet 64×64、文生图 512×512（SD 潜空间）。
- 适用范围：作者声称该法**对任何带确定性采样的扩散模型通用**。

关键设计：把 KL 的梯度表达为两个 score 之差（Eq.7）——`∇θ D_KL ≈ E[w_t·α_t·(s_fake - s_real)]·dG/dθ`，其中 `s_real` 把样本推向真实分布的众数，`-s_fake` 把样本"摊开"避免坍缩。

## 数据
DMD 不引入新的训练图像数据集，而是**复用教师 + 用教师离线生成"配对蒸馏数据"**：

- **回归用的 noise–image 配对集（离线预生成）**：用教师以确定性 ODE 采样器跑出 {z, y} 对。
  - CIFAR-10：100k 对（class-cond）/ 500k 对（uncond），Heun 18 步（EDM）。
  - ImageNet 64×64：25k 对，Heun 256 步。
  - LAION-Aesthetic-6.25+：50万对，PNDM 50 步，guidance=3；每对对应该数据集前 50 万条 prompt。底层图像集约 **300 万张**。
  - LAION-Aesthetic-6+：**1200 万对**，PNDM 50 步，guidance=8；底层约 **1200 万张**。
- **分布匹配损失用的数据是"无配对"的**：每步现采高斯噪声经 Gθ 生成 fake 样本即可，不需要真实图像（real score 完全由固定教师提供）。
- 论文强调：配对集**只用不到训练算力的 1%**（以 CIFAR 为例）即可作为有效正则。未涉及人工标注 / re-captioning / 美学或安全过滤等额外数据工程（数据美学筛选已在 LAION-Aesthetic 子集层面完成）。

## 训练方法
三条损失协同（Algorithm 1）：

1. **分布匹配损失 L_KL（生成器主损失）**：对 Gθ 输出 x 注入随机量噪声得 x_t，分别过 real/fake 两个 denoiser 得去噪预测，梯度 = `(pred_fake - pred_real)/weighting`，反传给 Gθ。
   - **时间步采样** `t ~ U(T_min, T_max)`，`T_min=0.02T, T_max=0.98T`（沿用 DreamFusion）。
   - **梯度加权 w_t（关键 trick）**：`w_t = σ_t²/α_t · CS/‖µ_base(x_t,t)-x‖₁`（按去噪图与输入的逐元素平均绝对误差归一化梯度幅度），跨噪声尺度归一化。消融显示比 DreamFusion 的 `σ_t/α_t`、ProlificDreamer 的 `σ_t³/α_t` 好约 **0.9 FID**（CIFAR 2.66 vs 3.60/3.71）。
2. **回归损失 L_reg（防模式坍缩）**：对配对 {z,y}，`L_reg = LPIPS(Gθ(z), y)`（VGG backbone，输入双线性上采到 224×224）。它把住"大尺度结构"，确保覆盖所有模式（消融图 3/5：去掉它会模式坍缩、多样性骤降）。
   - 生成器总目标：`D_KL + λ_reg·L_reg`，**λ_reg = 0.25**（CIFAR uncond 用 0.5）。两路损失用不同数据流：分布匹配走无配对 fake 样本，回归走配对样本。
3. **fake score 的去噪损失 L_denoise（在线训 critic）**：`µ_fake^φ` 用标准去噪目标 `‖µ_fake(x_t,t)-x₀‖²`（按时间步加权，权重 SNR+1/0.5² for EDM、SNR for SD）持续拟合当前生成分布。每个训练步：先更新 Gθ，再更新 µ_fake。

**训练目标本质是分布匹配（近似 KL）而非 diffusion/flow-matching/next-token**；蒸馏对象是确定性 ODE 采样的教师。

**CFG 蒸馏**：文生图教师带 classifier-free guidance。做法 = 用**带 guidance 的教师**生成配对集；计算 ∇θ D_KL 时 real score 用 guided model 的 mean-prediction 替换，fake score 公式不变；用**固定 guidance scale** 训练（低指导版 scale=3，高质量版 scale=8）。

**关键超参**：AdamW，wd=0.01，β=(0.9,0.999)，warmup 500 步，grad clip L2=10，dropout 关闭（随 CM）。学习率：CIFAR 5e-5、ImageNet 2e-6、LAION 1e-5。迭代数：CIFAR 300k、ImageNet 350k、LAION-6.25+ 20k、LAION-6+ 约 165k（分 12 个版本逐步调 reg pair 数/reg 权重/Max DM step/VAE 类型，FID 从 23.88 降到 14.93，见论文 Table 5）。

## Infra（训练 / 推理工程）
- **训练算力**：
  - CIFAR / ImageNet：7 张 GPU，batch 392 / 336。
  - LAION-Aesthetic-6.25+（低指导，FID 优化版）：**72 张 A100**，总 batch 2304（分布匹配）+ 1152（回归），约 **36 小时**。
  - LAION-Aesthetic-6+（高指导，质量版）：约 **80 张 A100，约两周**。
- **显存优化**：gradient checkpointing + 混合精度（FP16/AMP）；为省显存，回归损失里解码生成 latent → 图像时用 **Tiny VAE（TAESD）** 而非标准 SD VAE（高指导版后期 V9 起才切回标准大 VAE）。局限里也点明：同时微调 fake score 网络 + 生成器导致训练显存占用大，LoRA 是潜在解。
- **推理**：单步前向。512×512 文生图单图 **90ms / 0.09s**（batch=1），FP16 下 **20 FPS**；相对 SD v1.5 教师的 PNDM 50 步 **2590ms（2.59s）** 约 **30×**（文生图含 CFG 实为 100 次网络前向→1，论文另称 "100× reduction in neural network evaluations"）；ImageNet 单步对教师的 512 次前向约 **512×** 提速（论文 abstract）。无需缓存/量化等额外手段——单步本身就是极致加速。

## 评测 benchmark（把效果讲清楚）
指标用 FID（图像质量）+ CLIP Score（文图对齐），均来自论文一手数据。

**ImageNet 64×64（Table 1，"# Fwd Pass" 为前向次数）**：
- DMD **FID 2.62**（1 次前向）；教师 EDM† 512 次前向 2.32；BigGAN-deep 1 次前向 4.06；ADM 250 步 2.07。
- 对比同期蒸馏（均 1 次前向）：Consistency Model 6.20、TRACT 7.43、Diff-Instruct 5.57、Progressive Distillation 15.39、Meng et al. 7.54、BOOT 16.30、DFNO 7.83。**DMD 比 Consistency Model 好约 2.4×**（6.20→2.62，论文 abstract/intro 明写），且与教师仅差 0.3 FID、按前向次数提速 512×（论文 "512-fold increase in speed"）。

**零样本 COCO-30k，512×512（Table 3，guidance=3，单步 0.09s）**：
- DMD **FID 11.49**；SD v1.5 教师（PNDM 50 步）8.78，latency **2.59s**（DMD 与教师仅差约 2.7 FID，论文原话 "within 2.7 FID"）。
- 同速/同级别对比（均 512 分辨率）：InstaFlow-0.9B 13.10（0.09s）、UFOGen 12.78（0.09s）、StyleGAN-T 13.90（0.10s）、GigaGAN 9.09（0.13s）、LCM-LoRA(4 步) 23.62（0.19s）、DPM++(4 步) 22.36（0.26s）、UniPC(4 步) 19.57（0.26s）。DMD **超过所有已发表的少步扩散加速法**（InstaFlow/UFOGen/StyleGAN-T 等），仅 GigaGAN 的 9.09 更低（但 GigaGAN 是从零训的大 GAN，非蒸馏加速法）。

**COCO-30k，guidance=8 高质量版（Table 4，FID/CLIP，自测）**：
- DMD：FID **14.93**、CLIP **0.320**，0.09s。
- DPM++(4 步) FID 22.44/CLIP 0.309；UniPC(4 步) 23.30/0.308；LCM-LoRA 1 步 77.90/0.238、2 步 24.28/0.294、4 步 23.62/0.297；SD v1.5 教师 13.45/0.322。DMD 单步在 CLIP 上几乎追平教师（0.320 vs 0.322），FID 远好于 4 步竞品。

**CIFAR-10（Table 6，均 1 次前向）**：DMD-conditional **2.66**、unconditional **3.77**；EDM 教师 35 次前向 1.84。优于多数单步 GAN/蒸馏（BigGAN 14.7、Diffusion-GAN 14.6、TRACT 3.78、Consistency Model 3.55），与 StyleGAN2-ADA(2.42)/StyleGAN-XL(1.85) 仍有差距。附录另测：回归损失用 L2 而非 LPIPS，FID 2.78 vs 2.66，说明对距离函数鲁棒。

**关键消融**：
- 去掉分布匹配损失 → CIFAR 3.82 / ImageNet 9.21，图像缺乏真实感与结构完整性。
- 去掉回归损失 → CIFAR 5.58 / ImageNet 5.61，模式坍缩、多样性骤降（图 5b 大量重复灰车）。
- 完整 DMD → CIFAR 2.66 / ImageNet 2.62。**两者缺一不可**：分布匹配负责真实感，回归损失负责模式覆盖与教师对齐（图 3 三模式实验直观印证）。
- 加权策略消融见上文（Eq.8 比基线好 0.9 FID）。

## 创新点与影响
**核心贡献**：
1. 把 VSD 的"双 score 之差 = 分布匹配梯度"从 test-time 3D 优化，**首次成功用于训练一整个一步生成网络**，且 scale 到 LAION 大规模文生图。
2. 提出"real score（固定教师）+ fake score（在线 critic）+ LPIPS 回归"三件套，回归损失专治分布匹配的模式坍缩并保证与教师对齐（可做实时设计预览）。
3. 新的梯度幅度归一化加权策略，跨噪声尺度稳住优化。
4. 实证：单步蒸馏可逼近多步教师（ImageNet 差 0.3 FID），改写了"蒸馏必然显著掉点"的认知。

**影响**：成为**单步/少步扩散蒸馏的代表方法**之一，与 Consistency Models、InstaFlow、ADD（SDXL-Turbo）并列为该方向标杆；其"用扩散模型当 score-based critic、避免对抗博弈"的范式被广泛沿用。直接催生作者团队的 **DMD2**（项目页指向 https://tianweiy.github.io/dmd2/ ，本页未落盘其原文，具体改动以 DMD2 论文为准），并影响后续 SD3-Turbo、各类实时文生图工作。

**已知局限**（论文 Limitations）：
- 与 100/1000 步精细离散的教师相比仍有轻微质量差距。
- 训练需同时微调 fake score 网络与生成器，**显存开销大**（建议用 LoRA 缓解）。
- 一步生成器牺牲了多步采样的可控性（如逐步细化），固定 guidance scale。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.18828
- arxiv_pdf: https://arxiv.org/pdf/2311.18828
- project_page: https://tianweiy.github.io/dmd/
- follow-up (DMD2, 项目页指向): https://tianweiy.github.io/dmd2/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.18828.pdf
- ../../../sources/omni/2023/dmd--project-page.md
