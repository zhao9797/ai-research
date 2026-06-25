---
title: "SDEdit: Guided Image Synthesis and Editing with Stochastic Differential Equations"
org: "Stanford University / Carnegie Mellon University"
country: US
date: "2021-08"
type: paper
category: edit
tags: [diffusion, image-editing, sde, score-based, img2img, training-free, stroke-to-image, compositing]
url: "https://arxiv.org/abs/2108.01073"
arxiv: "https://arxiv.org/abs/2108.01073"
pdf_url: "https://arxiv.org/pdf/2108.01073"
github_url: "https://github.com/ermongroup/SDEdit"
hf_url: ""
modelscope_url: ""
project_url: "https://sde-image-editing.github.io/"
downloaded: [arxiv-2108.01073.pdf, sdedit--readme.md, sdedit--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
SDEdit（Stochastic Differential Editing）提出了"先加噪、再去噪"（noise-then-denoise）的范式：用一个预训练好的、**完全无监督**的扩散/score-based 模型，把用户的引导图（涂鸦、笔触、拼贴）加到中间时刻 t₀ 的高斯噪声水平，再从该中间时刻反解 reverse-SDE 去噪，无需任何任务专属训练或 GAN 反演即可完成"草图→真实图"、笔触编辑、图像合成。人评中相对 SOTA GAN 方法在写实度上最高领先 **98.09%**、整体满意度领先 **91.72%**——这是后来 Stable Diffusion `img2img`、GLIDE 编辑等一切扩散图像编辑的方法源头。

## 背景与定位
引导式图像合成的核心矛盾是 **realism（写实）↔ faithfulness（忠于输入）** 的平衡。SDEdit 之前主流有两条路：

- **条件 GAN**（pix2pix、CycleGAN 类）：直接学"原图→编辑后图"的映射，但每个新任务都要收集成对数据并重训模型，成本高且无法即开即用。
- **GAN 反演**（Image2StyleGAN、in-domain GAN、e4e 等）：把输入图反演到预训练 GAN 的隐空间再修改隐码。问题是每个任务都要手工设计 loss 与优化流程，反演本身又慢又不准，常找不到忠实表示输入的隐码。

SDEdit 的关键洞察是"劫持"（hijack）score-based 生成模型的反向过程：reverse-SDE 不一定要从 t=1（纯噪声）开始解，可以从任意中间时刻 t₀∈(0,1) 起步——这是此前 SDE 生成模型没研究过的用法。给定引导图 x⁽ᵍ⁾，先加 σ(t₀) 量级的高斯噪声"抹平"不自然的笔触瑕疵但保留整体结构，再从 t₀ 反解 SDE 去噪，把"不真实的涂鸦"逐步投影回自然图像流形。整个过程**只需一个在无标注图像上训练的预训练 SDE 模型**，不需要测量函数（即不知道"真实图→用户涂鸦"的映射），因此区别于求解逆问题的方法（[[ilvr]] / SNIPS）和需要成对数据的方法。技术脉络上它直接站在 score-SDE（Song et al. 2021）与 [[ddpm]] 的肩上，是把扩散先验用于编辑的开山之作；后续被 [[glide]]、Stable Diffusion 的 img2img、distilled-SD 等广泛采用。SDEdit 发表于 arXiv 2021-08，正式收录 ICLR 2022。

## 模型架构
SDEdit **本身不训练任何网络**，它是一个推理期算法，套在现成的 score-based / 扩散模型上。具体用到的 backbone：

- **score 网络 sθ(x,t)**：直接复用 Song et al. 2021（score-SDE）、Ho et al. 2020（[[ddpm]]）、Dhariwal & Nichol 2021（[[diffusion-models-beat-gans]]）公开的预训练 checkpoint，均为 **U-Net** 结构的去噪/score 估计网络（DDPM 系 U-Net + 时间嵌入），在像素空间直接建模（非 latent，区别于后来的 [[latent-diffusion-ldm]]）。
- **两类 SDE 都支持**：
  - **VE-SDE（Variance Exploding）**：α(t)=1，σ(t)=σ_min·(σ_max/σ_min)ᵗ，σ_min=0.01；σ_max 按数据集取 380/378/348/1348（LSUN church / bedroom / FFHQ-CelebA-HQ 256 / FFHQ 1024）。论文正文以 VE-SDE 讲解。
  - **VP-SDE（Variance Preserving，即 DDPM 形式）**：dx = −½β(t)x dt + √β(t) dw，β(t)=β_min+t(β_max−β_min)，β_min=0.1、β_max=20。
- **条件注入方式**：没有显式条件分支，"条件"完全通过**初始化**注入——把引导图加噪后作为 reverse-SDE 的起点。这是 SDEdit 最简洁也最深刻的设计：用初值而非额外网络模块来携带用户意图。
- **掩码版（masked SDEdit）**：为保留图像中不想改的区域（图像合成 / 笔触局部编辑），引入二值掩码 Ω∈{0,1}^{C×H×W}（1=可编辑）。可编辑区正常跑 reverse-SDE，不可编辑区在每步用 (1−Ω)⊙(x₀+σ(t)z) 重新注入"原图+对应噪声水平"，因 σ(t)→0 当 t→0，故不可编辑区最终精确收敛回原像素，保证身份/背景不被改动（Algorithm 3 VE / Algorithm 5 VP）。
- **分辨率**：实验覆盖 256×256（LSUN bedroom/church、CelebA-HQ）与 1024×1024（FFHQ/CelebA-HQ），分辨率由所用预训练 checkpoint 决定。

## 数据
SDEdit **不训练模型，因此没有自己的训练数据**——这是它"免训练"卖点的根基。涉及的数据有两类：

- **预训练模型所用数据集**（来自他人公开 checkpoint）：LSUN bedroom、LSUN church outdoor、CelebA-HQ、FFHQ，均为开源公开数据集，按许可使用，未做任何重训。
- **评测用的"模拟涂鸦"数据**：为做大规模定量评估，作者设计了 **human-stroke-simulation 算法**自动从真实图生成涂鸦：对 256×256 图先做 kernel size=23 的中值滤波，再用自适应调色板把颜色降到 6 色，得到形似人手绘的涂鸦。应用于 LSUN bedroom / church 验证集，以及 CelebA(256×256) 测试集中随机选的 6000 张。"# of colors"越少（如 Table 4 中降到更少色）则引导越粗糙、越不精确。

数据清洗/配比/re-captioning/合成数据规模等不适用（无训练）。人手绘涂鸦引导图由人类用户提供（Fig. 5）。

## 训练方法
**核心一点：SDEdit 不做任何训练、微调、蒸馏或偏好对齐**——这正是相对条件 GAN（要重训）和 GAN 反演（要逐任务优化 loss）的核心优势。它纯粹是一个**推理期采样算法**：

- **采样目标**：Euler-Maruyama 法数值求解 reverse-SDE。
  - VE 更新式：x ← x + ε²·sθ(x,t) + ε·z，其中 ε=√(σ²(t)−σ²(t−Δt))。
  - VP 更新式：x_{n−1} = (x_n + β(t_n)Δt·sθ)/√(1−β(t_n)Δt) + √(β(t_n)Δt)·z。
- **唯一关键超参 t₀**（起始时刻 / 加噪量），它直接控制 realism↔faithfulness 权衡：
  - t₀ 越大 → 加噪越多、跑 SDE 越久 → 越写实但越不忠实（极端 t₀=1 退化为无条件采样）；t₀ 越小 → 越忠实但越不写实（极端 t₀=0 就是引导图本身）。
  - 论文给出**理论刻画（Proposition 1）**：在 ‖sθ‖²≤C 假设下，以至少 1−δ 概率，‖x⁽ᵍ⁾−SDEdit(x⁽ᵍ⁾;t₀,θ)‖² ≤ σ²(t₀)(Cσ²(t₀)+d+2√(−d·logδ)−2logδ)，说明偏差随 t₀ 单调增长——要写实就必须容忍一定的不忠实。
  - **甜区**：对合理引导，t₀∈[0.3,0.6] 普遍有效。t₀ 的选取可在交互式场景中对用户反馈做**二分搜索**；非交互大规模场景里在一张随机图上二分搜出 t₀ 后对同任务全部固定共享，经验上共享 t₀ 对同任务所有合理引导都好用。
- **K 次重复（Algorithm 2）**：可把整套"加噪→去噪"重复 K 次，K=1~3 都不错，K 越大越写实但算力越高。实验中绝大多数用 K=1。
- 各应用具体设置：
  - **笔触→图（stroke synthesis）**：SDEdit(VP)，K=1、N=500、t₀=0.5。
  - **笔触编辑（stroke editing）**：SDEdit(VP) t₀=0.5/N=500；SDEdit(VE) t₀=0.45/N=1000，K=1。
  - **图像合成（compositing）**：CelebA-HQ 256，用 FFHQ 预训练模型，SDEdit(VE) t₀=0.35、N=700、K=1。

无 SFT / RLHF / DPO / reward model / consistency / LCM / ADD 等——这些都是后续工作才引入的，SDEdit 时代尚不存在。

## Infra（训练 / 推理工程）
- **训练**：无（不训练任何模型，零 GPU·时训练成本）。
- **推理**：256×256 涂鸦生成单图 **29.1 秒 / 单张 2080Ti GPU**。对比同设备同设置：StyleGAN2-ADA 投影约 72.8s（SDEdit 更快），in-domain GAN-2 约 5.2s（SDEdit 更慢）。即比优化式 GAN 反演快、比编码器式 GAN 反演慢。
- 步数 N=500~1000 决定主要推理开销；作者明确指出 SDEdit 的速度"可由近期更快的 SDE 采样工作改进"——这一坑后来被 [[ddim]]、蒸馏等填上。
- 无并行/分布式/混合精度/量化等大规模工程细节（不适用，纯单卡推理算法）。

## 评测 benchmark（把效果讲清楚）
评测维度为 **realism（KID + MTurk 人评）** 与 **faithfulness（逐像素 L2，归一化到 [0,1]；部分用 LPIPS）**，并用 MTurk 成对比较测整体满意度（realism+faithfulness）。

**① 笔触生成 · LSUN bedroom，人手绘涂鸦（Table 1，L2 越低越忠实；右两列=偏好 SDEdit 的 MTurk 比例）：**

| 基线 | Faithfulness L2 ↓ | SDEdit 更写实 ↑ | SDEdit 更满意 ↑ |
|---|---|---|---|
| In-domain GAN-1 | 101.18 | 94.96% | 89.48% |
| In-domain GAN-2 | 57.11 | 97.87% | 89.51% |
| StyleGAN2-ADA | 68.12 | **98.09%** | **91.72%** |
| e4e | 53.76 | 80.34% | 75.43% |
| **SDEdit** | **32.55** | – | – |

**② 笔触生成 · 算法模拟涂鸦（Table 2，L2/KID 越低越好）：**

| 方法 | bedroom L2 ↓ | bedroom KID ↓ | church L2 ↓ | church KID ↓ |
|---|---|---|---|---|
| In-domain GAN-1 | 105.23 | 0.1147 | – | – |
| In-domain GAN-2 | 76.11 | 0.2070 | – | – |
| StyleGAN2-ADA | 74.03 | 0.1750 | 72.41 | 0.1544 |
| e4e | 52.40 | 0.0464 | 68.53 | 0.0354 |
| **SDEdit** | **36.76** | **0.0030** | **37.67** | **0.0156** |

SDEdit 在两个数据集的 L2 与 KID 上同时大幅领先，KID 几乎压低一个数量级（bedroom 0.0030 vs e4e 0.0464）。

**③ 图像合成 · CelebA-HQ（Table 3）：**

| 方法 | L2 ↓ | SDEdit 更写实 ↑ | SDEdit 更满意 ↑ | masked LPIPS ↓ |
|---|---|---|---|---|
| Laplacian Blending | 68.45 | 75.27% | **83.73%** | 0.09 |
| Poisson Blending | 63.04 | 75.60% | 82.18% | 0.05 |
| In-domain GAN | 36.67 | 53.08% | 73.53% | 0.23 |
| StyleGAN2-ADA | 69.38 | 74.12% | 83.43% | 0.21 |
| e4e | 53.90 | 43.67% | 66.00% | 0.33 |
| **SDEdit** | **21.70** | – | – | **0.03** |

合成任务上 SDEdit 的 L2（21.70）与 masked LPIPS（0.03，掩码外区域改动最小）都最优，整体满意度最高领先 83.73%。注意写实度上 SDEdit 略低于 e4e（e4e 43.67% 偏好 SDEdit，意味 e4e 略更写实），但因更忠实、掩码外改动更少，综合更优。

**消融/分析结论**：
- **realism-faithfulness 权衡曲线**（Fig. 3，LSUN church，扫 t₀ 从 0.01、0.1…1）：随 t₀↑，KID↓（更写实）但 L2↑（更不忠实），甜区 t₀∈[0.3,0.6]。
- **引导精度消融**（Table 4，church，降低 # of colors 使引导更粗糙）：SDEdit 在各精度引导下都稳定优于基线。
- **取证安全的副发现（伦理章节）**：现有针对 GAN 假图的取证检测器（Wang et al. 2020）几乎检不出 SDEdit 生成图——LSUN bedroom 上对 SDEdit 检出率 <3%，而对 GAN 生成图检出率高达 93%，作者据此呼吁发展面向 SDE 模型的取证方法。

（说明：CLIPScore / GenEval / T2I-CompBench / DPG / MJHQ-30K / HPS / ImageReward / PickScore / VBench 等指标均**未报告**——这些 benchmark 在 2021 年尚未出现或不适用；SDEdit 是无文本条件的像素空间编辑方法。）

## 创新点与影响
**核心贡献**：
1. **noise-then-denoise 编辑范式开山**：首次提出从中间时刻 t₀ 起步反解 reverse-SDE 来做引导编辑——把"加多少噪"当作 realism↔faithfulness 的连续旋钮，并给出理论刻画（Prop. 1）。
2. **完全免训练 / 免反演 / 免任务专属 loss**：单个无监督预训练扩散模型即插即用，一套算法（masked SDEdit）统一了"涂鸦→图、笔触编辑、图像合成"三类任务。
3. **强人评结果**：相对 SOTA GAN 编辑方法在写实度上最高领先 98.09%、满意度 91.72%，且掩码外改动（masked LPIPS）远低于所有基线。

**影响**：SDEdit 是后续一切扩散图像编辑的方法母体——**Stable Diffusion 的 `img2img`/strength 参数本质就是 SDEdit 的 t₀**；[[glide]]、distilled-SD 等文本引导编辑、以及大量 inpainting/局部编辑工作都建立在"加噪到中间步再去噪"之上。它把"扩散模型不止能从噪声生成，还能从任意中间态编辑"这一认知带入主流。

**已知局限**：
- 推理慢（单图 29.1s / 2080Ti），步数 N=500~1000，比编码器式 GAN 反演慢（后续靠 DDIM/蒸馏缓解）。
- t₀ 需要按任务调（虽可二分搜索），不存在对所有引导都最优的全局 t₀。
- 在像素空间直接操作、依赖域内预训练模型（LSUN/CelebA/FFHQ），跨域泛化与高分辨率受 checkpoint 限制；非文本条件，无法用语言指定编辑（这要到 GLIDE/SD 才补上）。
- 安全隐患：生成图难被现有 GAN 取证器识别，存在被滥用风险（论文伦理章节已自陈）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2108.01073
- arxiv_pdf: https://arxiv.org/pdf/2108.01073
- github: https://github.com/ermongroup/SDEdit
- project_page: https://sde-image-editing.github.io/
- colab(官方demo): https://colab.research.google.com/drive/1KkLS53PndXKQpPlS1iK-k1nRQYmlb4aO

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2108.01073.pdf
- ../../../sources/omni/2021/sdedit--readme.md
- ../../../sources/omni/2021/sdedit--project-page.md
