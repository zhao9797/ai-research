---
title: "Improved Techniques for Training Score-Based Generative Models (NCSNv2)"
org: "Stanford University"
country: US
date: "2020-06"
type: paper
category: method
tags: [score-based, denoising-score-matching, langevin-dynamics, ema, high-resolution, diffusion-precursor]
url: "https://arxiv.org/abs/2006.09011"
arxiv: "https://arxiv.org/abs/2006.09011"
pdf_url: "https://arxiv.org/pdf/2006.09011"
github_url: "https://github.com/ermongroup/ncsnv2"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2006.09011.pdf, ncsnv2--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
NCSNv2 是 Yang Song 与 Stefano Ermon（Stanford，NeurIPS 2020）对其 2019 年 [[ncsn]]（NCSN，基于分数匹配的生成模型）的系统改进：用一套**有理论支撑、可从数据自动计算**的设计准则（噪声尺度、噪声条件化、退火 Langevin 步长、EMA 权重平均），**首次把无需对抗训练的分数模型从 32×32 扩展到 256×256**（FFHQ），并把 CIFAR-10 FID 从 NCSN 的 25.32 降到 **10.87**，CelebA 64×64 人评 HYPE∞ 从 19.8 提升到 37.3（接近 ProgressiveGAN 的 40.3）。

## 背景与定位
分数模型（score-based model）通过学习数据分布的**分数函数** ∇x log p(x)（指向数据密度增长最快方向的向量场）来建模分布，训练靠**去噪分数匹配（denoising score matching, DSM）**，采样靠 **Langevin dynamics**——从白噪声出发，反复"加分数梯度 + 注入小噪声"逐步把噪声细化成图像。无需对抗优化是其相对 GAN 的核心优势。

但 2019 年的 NCSN 只能在低分辨率（≤32×32，论文里只测了 MNIST 28² 和 CelebA/CIFAR-10 32²）上工作，原因有几个：(1) 噪声尺度 {σi} 怎么选缺乏原则，[1] 推荐的 L=10、σ1=1、σL=0.01 在高分辨率上失效；(2) 退火 Langevin 在高维 + 不完美学习分数下可能不收敛或极慢；(3) 训练中样本质量不稳定，常出现**整张图统一偏色（color shift）**的伪影。

NCSNv2 不是换框架，而是给出**逐条可操作、跨数据集自适应、无需手调**的"训练/采样配方"。它是从 NCSN 走向 [[score-sde]]（Score SDE 统一连续框架，2020-11，把 NCSN/[[ddpm]] 统一为 SDE 离散化）的关键过渡工作——README 明确指出后续 score_sde 工作进一步提升了样本质量并支持精确对数似然。它与同期 [[ddpm]]（2020-06）属并行的两条扩散/分数路线，最终被 Score SDE 统一。

## 模型架构
- **Backbone：基于 RefineNet 的卷积分数网络**（RefineNet 本是语义分割架构，[24]）。NCSN 对其做了三处改造：每个卷积层加增强版条件实例归一化 **CondInstanceNorm++**、RefineNet block 里 max pooling 换 average pooling、ResNet backend 用空洞卷积（dilated conv）。激活函数全程用 **ELU**。
- **NCSNv2 的架构改动（配合 Technique 3）**：(i) 把 CondInstanceNorm++ 的类别数设为 1（即 **InstanceNorm++**，不再按噪声尺度分别存归一化参数）；(ii) average pooling 改回 max pooling；(iii) RefineNet block 内移除所有归一化层。后两者对结果影响不大，只是为贴近标准 RefineNet。基本单元命名为 ResBlock / RefineBlock。
- **分辨率自适应**：架构随分辨率加深加宽以保证感受野和容量。32²–64² / 96²–128² / 256² 三套配置（论文 Table 2/3），256² 版本层数与下采样最多（多个 dilation 2/4 的 ResBlock down + 512 通道）。
- **无 VAE / 无 text encoder / 无 tokenizer**：这是**像素空间、无条件**的图像生成模型，不涉及文本条件或潜空间（区别于后来的 [[latent-diffusion-ldm]]）。条件信息仅有噪声尺度 σ，且通过 Technique 3 以解析方式注入。
- **参数量**：论文未直接报告参数量数字（未披露具体 M 级别），仅以层数/通道数表（Table 2/3）描述容量。

## 数据
纯图像数据集，无文本配对，无 re-captioning，无合成数据：
- **CIFAR-10**：50000 训练 + 10000 测试，32×32。
- **CelebA**：162770 训练 + 19962 测试；预处理先中心裁剪到 140×140 再 resize 到 64×64。
- **LSUN**：取 church_outdoor / bedroom / tower 三类，训练图各 126227 / 3033042 / 708264 张，各 300 验证图；预处理先把短边 resize 到 96（church）或 128（bedroom/tower）再中心裁剪成正方形。
- **FFHQ**：70000 张 1024×1024 高质量人脸，resize 到 256×256；因无官方 test split，随机取 63000 训练 / 7000 测试。
- **数据增强**：所有数据集都用随机水平翻转。
- **关键数据驱动设计**：σ1 直接取**训练集所有样本对之间的最大欧氏距离**（Technique 1）；当训练数据超过 60000 张时，随机抽 10000 张算最大成对距离作为 σ1。无美学/安全过滤的描述（这是 2020 年纯学术无条件生成工作，未涉及）。

## 训练方法
**训练目标：去噪分数匹配（DSM），无对抗训练。** 对一组降序噪声尺度 {σi}（σ1>…>σL），用单一**噪声条件分数网络（NCSN）** sθ(x,σ) 联合估计所有加噪分布 pσi 的分数，损失为各尺度 DSM 的加权平均（每尺度权重 σi²）：
L(θ)=1/(2L) Σi E[ ‖σi·sθ(x̃,σi) + (x̃−x)/σi‖² ]，x̃ = x + σi·噪声。

**五大改进技术（NCSNv2 = NCSN + Technique 1–5）：**
1. **Technique 1（初始噪声尺度）**：把 σ1 取为训练数据**最大成对欧氏距离**。理论（Prop. 1）证明：要让 Langevin 能在数据模式（mode）间转移以保证多样性，σ1 必须与数据点间最大距离数量级相当。例 CIFAR-10 中位成对距离 ~18，原 NCSN 的 σ1=1 会令模式间转移概率 E[r] < 10⁻¹⁷，几乎不可能产生多样样本；改用 σ1=50 后合成样本平均成对距离 18.65，逼近真实数据 17.78（σ1=1 时仅 10.12）。
2. **Technique 2（其余噪声尺度）**：取**几何级数**，公比 γ 满足 Φ(√(2D)(γ−1)+3γ) − Φ(√(2D)(γ−1)−3γ) ≈ 0.5。理论（Prop. 2，高维下 ‖x‖₂ ≈ N(√D·σ, σ²/2)）保证相邻噪声尺度的"半径分布"有足够重叠（按 3-sigma 法则），让从 pσi-1 采得的样本能可靠初始化 pσi 的 Langevin。该约束直接推出"等公比几何级数"是最优形式。D 越大需要的 L 越多。
3. **Technique 3（噪声条件化）**：把分数网络参数化为 **sθ(x,σ) = sθ(x)/σ**——只用一个**无条件**网络，输出除以 σ。依据是理论上 E[‖∇x log pσ(x)‖₂] ≈ √D/σ，且经验上训练好的 NCSN 满足 ‖sθ‖∝1/σ，故按 1/σ 缩放即可注入噪声信息。好处：易实现、内存不随 L 线性增长（原 NCSN 每尺度存一组归一化参数）、可处理任意多甚至**连续**的噪声尺度。深网络很难自动学这种跨数个数量级的缩放，显式给出更稳。
4. **Technique 4（选 T 与 ε）**：退火 Langevin 每尺度跑 T 步、步长 αi = ε·σi²/σL²。理论（Prop. 3）给出 xT 方差闭式解 sT²/σi²，几何级数下该比值跨尺度相同且与维度 D 无关。做法：先按算力预算选 T（典型 T×L 为数千），再网格搜索 ε 让 sT²/σi² 尽量逼近 1（推荐网格搜索而非梯度优化）。
5. **Technique 5（EMA）**：对模型参数维护**指数滑动平均**（θ' ← m·θ' + (1−m)·θ，典型 **m=0.999**），采样时用 EMA 权重。这直接修复了 vanilla NCSN 训练中 FID 剧烈波动与统一偏色伪影，跨数据集普适有效。

**采样：退火 Langevin dynamics**（Algorithm 1）：从噪声出发，按 σ1→σL 逐尺度跑 T 步 Langevin，上一尺度结果初始化下一尺度。NCSNv2 还采纳了 [9] 提出的**额外去噪步（denoising step）**：最后返回 xT + σ_T²·sθ(xT,σ_T)（论文 Algorithm 1 记号，σ_T 即最小/最后一个噪声尺度 σL；Tweedie 公式去掉残余 N(0,σ_T²I) 噪声），显著改善 FID 而不改变视觉外观。

**优化器/超参（Table 4，均按 Technique 1–4 自动算出）**：Adam；用 Technique 3 时学习率 **1e-4**（避免 loss 爆炸），否则 1e-3；Adam 的 ε 在 FFHQ 用 1e-3、其余 1e-8。各数据集 NCSNv2 配置：
- CIFAR-10 32²：σ1=50, L=232, T=5, ε=6.2e-6, batch 128, 300k iters
- CelebA 64²：σ1=90, L=500, T=5, ε=3.3e-6, batch 128, 210k iters
- LSUN church 96²：σ1=140, L=788, T=4, ε=4.9e-6, batch 128, 200k iters
- LSUN bedroom/tower 128²：σ1=190, L=1086, T=3, ε=1.8e-6, batch 128, 150k iters
- FFHQ 256²：σ1=348, L=2311, T=3, ε=0.9e-7, batch 32, 80k iters
（对照：原 NCSN 全部用 σ1=1, L=10, T=100, ε=2e-5。NCSNv2 的 L 从 10 暴增到上千，T 从 100 降到个位数。）高分辨率（128²/256²）loss 接近收敛时训练可能不稳——这是 Adam 的已知问题，可用 AMSGrad 缓解。

## Infra（训练 / 推理工程）
- **硬件：Nvidia Tesla V100 GPU。** 按数据集规模用 2–8 卡（Table 6）。
- **训练耗时（wall-clock）**：CIFAR-10 2×V100 → 22h；CelebA 4×V100 → 29h；LSUN church/bedroom/tower 8×V100 → 各 52h；FFHQ 8×V100 → 41h。
- **采样耗时**：CIFAR-10 2min、CelebA 7min、church 17min、bedroom/tower 各 19min、FFHQ 50min（一批样本）。退火 Langevin 总步数 = L×T（如 FFHQ 2311×3 ≈ 6933 步），属**慢采样**——这是分数/扩散模型的共性瓶颈，本文未做步数蒸馏或加速（蒸馏/一致性采样是后续工作如 LCM/Consistency Models 的范畴）。
- **混合精度 / 并行策略 / 吞吐量**：论文未披露（无 FP16、ZeRO、张量并行等细节，2020 年纯学术多卡数据并行）。
- **参数量、显存占用**：未直接报告。
- 部署形态：开源 PyTorch 实现（main.py 统一训练/采样/快速 FID），提供 Google Drive 预训练 checkpoint。

## 评测 benchmark（把效果讲清楚）
**CIFAR-10 32×32 无条件生成（Table 1，FID↓ / Inception↑）：**

| 模型 | Inception↑ | FID↓ |
|---|---|---|
| PixelCNN | 4.60 | 65.93 |
| IGEBM | 6.02 | 40.58 |
| WGAN-GP | 7.86 | 36.4 |
| SNGAN | 8.22 | 21.7 |
| NCSN [1] | **8.87** | 25.32 |
| NCSN (w/ denoising) | 7.32 | 29.8 |
| **NCSNv2 (w/o denoising)** | 8.73 | 31.75 |
| **NCSNv2 (w/ denoising)** | 8.40 | **10.87** |

- NCSNv2（带去噪步）把 CIFAR-10 FID 从 NCSN 的 25.32 大幅降到 **10.87**，代价是 Inception 略降（8.87→8.40）。注意：**去噪步对 FID 影响极大**（10.87 vs 不带去噪 31.75），印证 FID 对微小噪声扰动敏感、不一定对齐视觉质量。
- **CelebA 64×64 FID（Table 1，下半部分，源中数字：NCSN w/o denoising 26.89、w/ denoising 25.30；NCSNv2 w/o denoising 28.86、w/ denoising 10.23）**：NCSNv2 带去噪步把 CelebA FID 降到 **10.23**。但有趣的是**不带去噪步时 NCSNv2 的 FID(28.86) 反而比 NCSN(26.89) 略差**，而视觉上 NCSNv2 明显更好——作者据此强调 FID 与人眼判断未必一致。

**人评 HYPE∞（CelebA 64×64，Table 5，越高越好）：**

| 模型 | HYPE∞(%) |
|---|---|
| StyleGAN* | 50.7 |
| ProgressiveGAN* | 40.3 |
| **NCSNv2** | **37.3** |
| NCSN | 19.8 |
| BEGAN | 10 |
| WGAN-GP | 3.8 |

- NCSNv2 的 HYPE∞=37.3 接近 ProgressiveGAN（40.3），远超 NCSN（19.8）——人评排序与 FID 排序**完全相反**（FID 上 NCSN 不带去噪步还略优），强力佐证"不应只看 FID"。

**消融（Section 6 / Fig. 5、9）**：把技术分三组——(i) Technique 5(EMA)、(ii) Technique 1,2,4(噪声尺度+步长)、(iii) Technique 3(噪声条件化)。从 NCSNv2 依次移除 (iii)(ii)(i)，每组技术都优于 vanilla NCSN；FID 数值因 FID 不可靠并非严格单调，但**视觉检查（Appendix C.4）确认逐组移除样本质量下降，全部组合最优**。EMA 单独即可稳定 FID 曲线、消除偏色伪影。

**高分辨率突破**：论文称分辨率**超过 96×96 时原 NCSN 完全失败**（结构/颜色崩坏，Fig. 7，原文 "resolutions beyond 96 × 96"），CelebA 64² 也有明显偏色；NCSNv2 在 96²–256² 都能生成高保真、结构正确的样本（FFHQ 256²、LSUN 128²、church 96²）。泛化性验证：训练/测试 loss 曲线贴合（无过拟合）、最近邻检索（InceptionV3 特征 ℓ2，含水平翻转）证明非记忆、可做平滑插值（在退火 Langevin 注入的高斯噪声上做球面插值）。

## 创新点与影响
**核心贡献：**
1. **从数据自动计算噪声尺度**：σ1 = 最大成对距离（Tech 1），其余取满足重叠条件的几何级数（Tech 2），把原本靠手调的关键超参变成有理论依据的解析公式。
2. **优雅的噪声条件化 sθ(x)/σ（Tech 3）**：单个无条件网络 + 解析缩放，内存不随 L 增长，支持任意多/连续噪声尺度——这一"输出按 σ 缩放"的思想直接启发了后续 [[score-sde]] 的连续噪声参数化（NCSN++/preconditioning）。
3. **退火 Langevin 步长的闭式分析（Tech 3 Prop. 3 + Tech 4）**：给出 sT²/σi² 闭式解并据此选 T、ε。
4. **EMA 稳定训练（Tech 5）**：成为此后扩散/分数模型的**标配**（DDPM、Score SDE、几乎所有后续扩散工作都用 EMA 采样）。
5. **首次把无对抗、像素空间分数模型扩展到 256×256**，证明分数/扩散路线在高分辨率上可与 GAN 一较高下。

**影响**：NCSNv2 是 NCSN → [[score-sde]] 统一框架（Score SDE 把 NCSN 的"多噪声尺度 DSM + 退火 Langevin"识别为 VE-SDE 的离散化，与 [[ddpm]] 的 VP-SDE 并列）的关键铺垫，其噪声尺度设计、噪声条件化与 EMA 都被后续连续时间扩散模型继承。它与同年 [[ddpm]] 共同点燃了 2020 年后扩散模型的爆发，最终通向 [[latent-diffusion-ldm]] / Stable Diffusion 等大规模 T2I 体系。

**已知局限**：(1) 采样仍慢（L×T 数千步，FFHQ 单批 50min），无加速/蒸馏；(2) 纯无条件、像素空间，无文本条件、无潜空间、无 classifier-free guidance；(3) 高分辨率（128²/256²）Adam 收敛附近训练不稳，需 AMSGrad 等缓解；(4) FID 与视觉/人评经常背离，作者反复强调需谨慎解读评测；(5) 未报告参数量、混合精度、吞吐等工程细节；(6) 继承训练数据偏差（如 CelebA 性别不均衡）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2006.09011
- arxiv_pdf: https://arxiv.org/pdf/2006.09011
- github: https://github.com/ermongroup/ncsnv2
- 预训练 checkpoint（README 给出）: https://drive.google.com/drive/folders/1217uhIvLg9ZrYNKOR3XTRFSurt4miQrd
- 前置工作 NCSN: https://arxiv.org/abs/1907.05600
- 后续工作 Score SDE: https://arxiv.org/abs/2011.13456 ([code](https://github.com/yang-song/score_sde))

## 本地落盘文件
- ../../../sources/omni/2020/arxiv-2006.09011.pdf
- ../../../sources/omni/2020/ncsnv2--readme.md
