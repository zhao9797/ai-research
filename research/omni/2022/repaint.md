---
title: "RePaint: Inpainting using Denoising Diffusion Probabilistic Models"
org: "ETH Zürich (Computer Vision Lab)"
country: Switzerland
date: "2022-01"
type: paper
category: edit
tags: [inpainting, diffusion, ddpm, training-free, resampling, image-editing, celeba-hq, imagenet]
url: "https://arxiv.org/abs/2201.09865"
arxiv: "https://arxiv.org/abs/2201.09865"
pdf_url: "https://arxiv.org/pdf/2201.09865"
github_url: "https://github.com/andreas128/RePaint"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2201.09865.pdf, repaint--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
RePaint 是一种**完全无需训练**（training-free）的扩散图像 inpainting 方法：直接拿一个**无条件预训练 DDPM** 当生成先验，只在反向去噪推理时把已知区域的加噪版本替换进去做条件注入；核心创新是 **resampling（来回跳采样 / harmonization）** 调度——在扩散时间上前后反复跳跃，让已知区与生成区充分协调。在 CelebA-HQ / ImageNet / Places2 的 6 种掩码、3 个数据集共 44 组对比中，用户研究里 **42/44 组以 95% 置信度胜过 AR 与 GAN SOTA**；极端掩码（Super-Resolve 2×、隔行）上 LPIPS 大幅领先（如 CelebA Super-Res LPIPS 0.029 vs LaMa 0.177）。

## 背景与定位
自由形式 inpainting（用任意二值掩码指定缺失区，生成新内容并与图像其余部分和谐）的难点在于**掩码泛化**：此前主流方法（GAN 系 [[diffusion-models-beat-gans]] 之前的 DeepFillv2 / AOT / LaMa，AR 系 DSI / ICT）都要在**某种掩码分布上训练**，遇到训练时没见过的掩码类型（如隔行、超分式 stride-2、只留中心 64×64）就严重退化、出棋盘伪影或只做纹理外推而缺乏语义。

RePaint 反其道而行：**不为 inpainting 任务训练任何东西**，只复用一个 off-the-shelf 的无条件 DDPM（[[ddpm]]，并基于 [[improved-ddpm]] 学方差 + Dhariwal & Nichol 的 guided-diffusion / ADM [[diffusion-models-beat-gans]] 的预训练权重）。这样有两个好处：(1) 推理期可泛化到**任意掩码形状**；(2) 借助强大的 DDPM 图像合成先验，生成更具**语义**的内容（而非简单纹理延伸）。

技术脉络上它属于"**用扩散先验做条件生成**"一支，并明确区分了几条相邻线：
- [[ilvr]]（ILVR）用条件图的低频信息引导，但 inpainting 里掩码区**高低频都缺失**，无法照搬；
- [[sdedit]]（SDEdit）从中间扩散时刻初始化并重复反向过程做 harmonization——但它**需要一张引导图**起步，inpainting 没有这张图；RePaint 论文把 SDEdit 的"重采样"改造成对照基线，证明自己的 resampling 在 Super-Res 掩码上 LPIPS 降低 53%+；
- 同期工作 GLIDE [[glide]]（classifier-free guidance 训条件模型）、Palette（image-to-image 条件 DDPM）都**要训条件模型**，RePaint 强调自己**只在反向过程中条件化、零训练**。

这个 resampling/harmonization trick 后来被大量编辑工作沿用，是 RePaint 最具影响力的遗产。

## 模型架构
RePaint **本身不引入新网络**——它是一个**推理调度算法**，架构完全来自所用的预训练 DDPM：

- **backbone**：[[diffusion-models-beat-gans]] 的 guided-diffusion U-Net（ADM）。模型在像素空间直接建模 256×256 图像（非 latent 扩散，不涉及 VAE / VQ tokenizer）。
- **预测目标**：U-Net 输入 (x_t, t)，输出 6 通道张量，含 x_{t-1} 的均值与方差信息（沿用 improved-DDPM 的**学习方差**设计，方差范围再做区间调整）。均值由估计的 x_0 与 x_t 加权得到。
- **无 text encoder**：纯无条件模型；ImageNet 模型可做**类别条件**生成（论文 5.5 展示对 "Granny Smith" 等类的 Expand 掩码补全），但 inpainting 主流程不依赖任何文本/类别条件。
- **条件注入方式（核心）**：每个反向步把图像拆成已知/未知两部分，已知区用前向公式直接加噪到当前噪声水平 x_{t-1}^known，未知区用 DDPM 反向步采样 x_{t-1}^unknown，再用掩码 m 拼接：
  - x_{t-1} = m ⊙ x_{t-1}^known + (1−m) ⊙ x_{t-1}^unknown
  - 关键在于：已知区的加噪 x_{t-1}^known 与未知区的生成共享**同一噪声水平**，所以二者可以无缝 join，且不修改、不微调网络本身。
- **分辨率**：论文主结果全部 256×256（CelebA-HQ / ImageNet / Places2）。
- **参数量**：未单独报告（即 ADM 256×256 模型规模）。

## 数据
RePaint **不训练 inpainting 模型**，所以"数据"主要指它复用的预训练 DDPM 所用数据集，以及评测数据：

- **ImageNet**：直接用 guided-diffusion 官方提供的 256×256 预训练模型（OpenAI [[diffusion-models-beat-gans]]），未自行训练。
- **CelebA-HQ**：作者自训一个无条件 DDPM，沿用 ImageNet 同套超参，256×256 crop，**250,000 iter**，约 5 天。
- **Places2**：自训无条件模型，**300k iter**、batch size 4、4×V100，约 6 天（论文附录 D）。
- 数据来源/清洗/配比/re-captioning/合成数据：**不适用 / 未涉及**（无条件像素扩散，无图文对、无标注流程）。
- 已知偏置：ImageNet 模型**偏向把缺失区补成狗**（ImageNet 狗类图像占比高），论文与 README 都明确标注为 failure case 与数据偏置。

评测数据：CelebA-HQ / ImageNet / Places2 各取 **100 张 256×256 测试图**（消融用 32 张 CelebA validation），掩码沿用 LaMa benchmark 的 Wide / Narrow 设置，并新增 Super-Resolve 2×、Alternating Lines、Half、Expand 共 6 种。

## 训练方法
**整体方法 = 零训练 + 推理期 resampling 调度**，这是本文的全部"方法"重心：

**1. 已知区条件化（Section 4.1）**——见上"条件注入"。直接朴素地按掩码拼接，但论文观察到：已知区的采样**没有考虑已生成的未知区内容**，每步都引入不和谐；而越往后扩散方差 β_t 越小、可修正余地越少，导致边界不和谐无法收敛——纹理对了但**语义错了**（如狗图缺口被补成毛发纹理但结构不对）。

**2. Resampling / Harmonization（Section 4.2，核心创新）**——为让已知与生成充分协调：把已经去噪一步得到的 x_{t-1} **再前向加噪回 x_t**（x_t ~ N(√(1−β_t)·x_{t-1}, β_t I)），然后重新去噪。这一"退一步再进一步"让网络有机会把已知区信息扩散进未知区。
- **jump length j**：一次跳跃覆盖的扩散时间步数（j=1 为最朴素的单步来回；最终用 **j=10**）。
- **resample 次数 r（论文也记作 n / U）**：每段重复来回的次数（最终用 **r=10**）。
- 直觉：去噪一步 → 把已知区按当前噪声水平加噪 → join → 再加噪回 x_t → 再去噪……反复 r 次后才真正推进到下一个更低噪声水平。
- 论文给出完整 **Algorithm 1** 与附录 B 的时间调度伪代码（j=10, r=10 时，时间序列形如 [249,248,249,248,247,248,…]，前后反复跳）。

**3. 训练目标**：被复用的 DDPM 用标准 L_simple = E[‖ε − ε_θ(x_t,t)‖²] + improved-DDPM 的学习方差 VLB 项训练（[[ddpm]] / [[improved-ddpm]]）；RePaint **不引入新损失、不对生成区加任何引导 loss**，因此生成多样、可"自由幻想"任何语义对齐训练集的内容。

**关键消融结论（方法层）**：
- **resampling vs 单纯放慢扩散**：在**相同算力预算**下，把步数从 250 拉到 1000（slow-down, r=1）几乎不改善 LPIPS（0.168→0.161）；而把预算用于 resampling（T=250, r=4）显著降到 0.134——证明收益来自**和谐化而非单纯更多算力**（Table 2 / Fig 7）。
- **jump 长度**：j=10 优于 j=1；j=1 时图像更模糊（Table 3）。
- **resample 次数**：r 越大越好，约 **n≈10 处收益饱和**（Fig 3）。
- **vs SDEdit 重采样**：在 Super-Resolution 掩码上 LPIPS 降低 **53%+**（Table 4）。

## Infra（训练 / 推理工程）
- **训练算力**（仅自训的两个无条件模型）：CelebA-HQ 256×256，3 batch × 4×V100，250k iter ≈ 5 天；Places2 256×256，batch 4 × 4×V100，300k iter ≈ 6 天。ImageNet 模型直接用 OpenAI 现成权重，零训练成本。致谢 Nvidia GPU grant + Huawei Technologies Oy (Finland) 项目 + ETH Zürich Fund。
- **最终推理配置**：T=250 timesteps，r=10 次 resampling，jump size j=10。
- **推理代价（核心局限）**：resampling 把反向过程的转移次数大幅放大（T=250 + j=10,r=10 的调度，单图约 **4000 次状态转移**，见附录 Fig 10 横轴），加上每张图独立优化（per-image DDPM），比 GAN/AR 慢得多，**不适合实时**。论文 §6 把加速寄望于 DDPM 效率改进（引用 [23,24]）的后续工作。
- **实现**：代码基于 OpenAI guided-diffusion，依赖 torch 1.7.1+cu110；提供 ImageNet / CelebA-HQ / Places2 三套模型与 thin/thick/隔行/超分/expand/half 掩码的现成 config。加速旋钮：降 t_T、降 jump_n_sample、用 start_resampling 仅在后期才 resample。
- 量化/缓存/部署形态：**未涉及**。

## 评测 benchmark（把效果讲清楚）
评测口径：**用户研究投票**（每图 5 人、每问题问两遍、自一致性<75% 的被试丢弃，1000 票/对比，报 95% 置信区间）+ **LPIPS**（AlexNet 特征距离，越低越好）。下列数字均来自论文 Table 1 / Table 4 / Table 5。投票 % 指"相对 RePaint（Reference）被偏好的比例"，越低说明 RePaint 越被偏好。

**CelebA-HQ（Table 1，节选 LPIPS↓）**：

| Mask | AOT | DSI | ICT | DeepFillv2 | LaMa | **RePaint** |
|---|---|---|---|---|---|---|
| Wide | 0.104 | 0.067 | 0.063 | 0.066 | **0.045** | 0.059 |
| Narrow | 0.047 | 0.038 | 0.036 | 0.049 | 0.028 | **0.028** |
| Super-Res 2× | 0.714 | 0.128 | 0.483 | 0.119 | 0.177 | **0.029** |
| Alt. Lines | 0.667 | 0.049 | 0.353 | 0.049 | 0.083 | **0.009** |
| Half | 0.287 | 0.211 | 0.166 | 0.209 | **0.138** | 0.165 |
| Expand | 0.604 | 0.487 | 0.432 | 0.467 | **0.342** | 0.435 |

**ImageNet（Table 1，LPIPS↓）**：Wide DSI 0.117 / ICT 0.107 / LaMa **0.105** / RePaint 0.134；Super-Res LaMa 0.272 / RePaint **0.183**；Alt. Lines LaMa 0.121 / RePaint **0.089**；Half LaMa **0.254** / RePaint 0.304；Expand LaMa **0.534** / RePaint 0.629。
**Places2（Table 5，LPIPS↓）**：Super-Res LaMa 0.369 / RePaint **0.099**；Alt. Lines LaMa 0.138 / RePaint **0.051**。

**结论模式**：
- **薄掩码（Super-Res 2×、隔行）**：RePaint 几乎全面碾压，用户研究在这两类掩码上拿到 **73.1%–99.3%** 偏好（论文 §5.3），其它方法彻底失败或出棋盘伪影。**Wide/Narrow 标准掩码**：论文称 RePaint 在 CelebA-HQ 与 ImageNet 上 Wide/Narrow 均以 95% 显著性胜出（投票偏好约 57%–66%，见 Table 1 各 baseline 的 Votes 列）。
- **厚掩码（Half / Expand）**：LaMa 在 LPIPS 上反而更低。论文明确解释这是**指标失真**——RePaint 会生成语义合理但与 GT 差异很大的内容，LPIPS（逐图与 GT 比）对这种多样化生成不公平；用户研究里 Half/Expand 上 RePaint 仍多数被偏好。
- **总体**：用户研究 6 掩码 × 3 数据集 = 44 组对比中，**42 组以 95% 置信胜出**，仅 2 组不确定（CelebA "Half" vs ICT；Places2 "Wide" vs LaMa 52.4% 几乎打平）。

**多样性 / 扩散性消融（附录 Table 6，DS = diversity score 越高越多样）**：RePaint 在多数掩码上 DS 高于 DSI/ICT（如 SR 2× DS 19.84 vs DSI 12.38 / ICT 8.70），且 LPIPS 更低——同时更准更多样。

未报告：FID（论文指出可靠 inpainting FID 需 >1000 张图，当时 DDPM 推理太慢不可行）、GenEval/CLIPScore/HPS 等文本对齐指标（无文本条件，不适用）。

## 创新点与影响
**核心贡献**：
1. **Training-free 扩散 inpainting**：首次系统性证明只用无条件预训练 DDPM，无需任何 inpainting/掩码专属训练，就能做高质量自由形式补全，并对**任意掩码**泛化；
2. **Resampling / harmonization 调度**：在扩散时间上"前后跳跃"反复 re-noise→denoise 来协调已知与生成区——这是被后续编辑工作（如各类 diffusion inpainting pipeline、[[stable-diffusion-img2img-inpaint]] 风格的方法、blended diffusion 系 [[blended-latent-diffusion]]）广泛借鉴的"重采样 trick"；
3. 配套提出**相同算力下 resampling 优于放慢扩散**、jump/resample 数量的可复现消融，给出明确推荐 (T=250, j=10, r=10)；
4. 公开 CelebA-HQ / Places2 自训模型与完整 config、掩码、LaMa-style benchmark 扩展（6 掩码）。

**影响**：把"用预训练扩散先验 + 推理期条件化"这一范式做实，成为 latent 空间编辑、blended diffusion、SD inpaint 等后续工作的概念与工程参照；resampling/harmonization 思想渗透进大量 training-free 编辑方法。

**已知局限**（论文 §6 / README）：
- **慢**：per-image 优化 + resampling 放大转移次数，远慢于 GAN/AR，不能实时；
- **极端掩码下生成可能严重偏离 GT**，使 LPIPS 等逐图指标失效，可靠 FID 又因推理慢而难算；
- **继承训练集偏置**：ImageNet 模型倾向补成狗；可能反映性别/年龄/种族偏置（也可正向用于人脸匿名化）。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2201.09865
- paper (PDF, v4 extended): https://arxiv.org/pdf/2201.09865
- github: https://github.com/andreas128/RePaint
- 依赖基座: OpenAI guided-diffusion https://github.com/openai/guided-diffusion （RePaint 复用其预训练 ADM 与反向步实现）

## 一手源存档（sources/）
- [arxiv-2201.09865.pdf](https://arxiv.org/pdf/2201.09865)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/repaint--readme.md)
