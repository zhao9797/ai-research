---
title: "Null-text Inversion for Editing Real Images using Guided Diffusion Models"
org: "Google Research / Tel Aviv University"
country: US
date: "2022-11"
type: paper
category: edit
tags: [diffusion, image-editing, inversion, classifier-free-guidance, ddim, prompt-to-prompt, stable-diffusion, training-free]
url: "https://arxiv.org/abs/2211.09794"
arxiv: "https://arxiv.org/abs/2211.09794"
pdf_url: "https://arxiv.org/pdf/2211.09794"
github_url: "https://github.com/google/prompt-to-prompt/#null-text-inversion-for-editing-real-images"
hf_url: ""
modelscope_url: ""
project_url: "https://null-text-inversion.github.io/"
downloaded: [arxiv-2211.09794.pdf, null-text-inversion--project-page.md, null-text-inversion--code-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Null-text Inversion 是一种**无需训练、无需微调模型权重**的真实图像扩散反演技术：用 guidance scale w=1 的 DDIM 反演轨迹作为「枢轴(pivot)」，再**只优化 classifier-free guidance 中的无条件(null-text) embedding** 来逐时刻贴合该枢轴轨迹，从而把任意真实照片精确反演进 [[stable-diffusion]] 的隐空间，让原本只能作用于「模型自己生成图」的 [[prompt-to-prompt]] 编辑首次可作用于真实照片。单图反演约 1 分钟(单卡 A100)，重建质量在 COCO 100 张子集上逼近 VQ-AutoEncoder 的重建上界，用户研究中 65.1% 的参与者认为其编辑效果最好(SDEdit 14.5% / Text2Live 16.6% / VQGAN+CLIP 3.8%)。

## 背景与定位
**要解决的问题**：text-to-image 扩散模型(Imagen / [[dall-e-2]] / [[stable-diffusion]])能生成高质量图，但要**编辑一张真实照片**，必须先把它「反演(invert)」回模型的噪声域——找到一个初始噪声向量 + 文本 prompt，使模型沿扩散过程能重建出这张图，同时保留可编辑性。

- **DDIM 反演为何不够用**：DDIM([[ddim]])提供了确定性的反向 ODE 求解，对**无条件**扩散模型反演误差可忽略。但有意义的文本编辑需要较大的 classifier-free guidance 尺度(w>1，SD 默认 w=7.5)，而 **CFG 会放大 DDIM 每步累积的误差**，导致重建出现明显伪影、且得到的噪声向量偏离高斯分布(降低可编辑性)。论文用 log-likelihood 量化:w 越大 z_T 越偏离标准正态、重建 PSNR 越差(附录 Fig.9)。
- **此前真实图编辑路线的缺陷**：
  - [[sdedit]](Meng et al.)给图加噪后从中间步去噪——细节(尤其人脸身份)保不住;
  - mask-based(Blended Diffusion / GLIDE / SD Inpaint)需要用户给精确 mask，且 mask 区域内的结构信息被丢弃;
  - [[textual-inversion]](Gal et al.)优化文本 token embedding——表示不可解释，难做直观 prompt 编辑;
  - Imagic / UniTune / [[dreambooth]] 等**微调模型权重**——复制整个模型、损伤先验、且 Imagic 每次编辑都要重新调参。
- **本工作定位**:在「不微调模型、不要 mask」的设定下，做到既高保真重建又高可编辑性，是真实图像扩散编辑的**关键使能技术(enabling technique)**——它本身不是编辑器，而是把 [[prompt-to-prompt]] 这类「合成图编辑」方法搬到真实照片上的桥梁。

技术脉络上，它把 GAN 反演里的 **Pivotal Tuning**(Roich et al., PTI)思想迁移到扩散模型，并独创性地把优化目标放在 CFG 的「无条件分支」上。

## 模型架构
本工作**不训练任何新模型**，完全复用公开的预训练组件，是一个推理期(inference-time)优化算法:

- **Backbone**:[[stable-diffusion]] v1.4 的隐空间 U-Net(latent diffusion，在 VQ-regularized autoencoder 的 latent 上做扩散，分辨率 64×64×4 latent → 512×512 像素)。
- **VAE/Tokenizer**:SD 自带的 VQ auto-encoder(VQAE),论文把它的重建质量作为反演的**上界**(z0 = E(x0) 视为 ground truth,不再优化 VQ decoder,因为那只对 SD 这一具体模型有效,本工作要通用算法)。
- **Text encoder**:SD 自带的预训练 CLIP 文本编码器作为语言模型 ψ。null-text 被 tokenize 为 start-token + end-token + 75 个 padding token(CLIP 与扩散模型都不做 masking,所以 padding token 也参与计算)。
- **条件注入**:标准 CFG 双分支——一次条件预测 ε_θ(z_t,t,C)、一次无条件预测 ε_θ(z_t,t,∅),再以 w 外推。
- **可优化变量(本工作唯一「被学」的东西)**:每个时间步一份的无条件 embedding {∅_t},t=1..T。**模型权重与条件 embedding C=ψ(P) 全程冻结**。

关键架构洞察:CFG 的最终结果「高度依赖无条件预测」这一被以往工作忽视的事实——别人都在改条件分支,本工作改无条件分支,既能高保真重建,又不破坏条件 embedding(从而保住 Prompt-to-Prompt 所需的语义 cross-attention map)。

## 数据
本工作**不涉及任何训练数据**(纯推理期算法)。其「数据」仅指评测用图:

- **消融与重建定量评测**:从 [[coco]] validation set 随机抽取的 **100 对 image-caption**。
- **编辑对比与用户研究**:100 个样本(图 + 输入 caption + 编辑 caption),部分取自 Bar-Tal et al.(Text2Live)用图,部分是作者从网上收集的含人/动物等结构化物体的照片。用户研究中 50 名 Prolific 参与者对 48 张图逐一打分。
- **source prompt 来源**:可由用户提供,也可用现成 captioning 模型(ClipCap 等)自动生成——论文证明反演对 caption 选择鲁棒(即便用随机 caption 也能收敛到接近 VQAE 上界的重建),但编辑时 caption 需包含要编辑的对象词才能产生可用的 attention map。

## 训练方法
没有「训练」,只有**推理期的逐时刻优化**。核心是两个组件的组合(完整流程见论文 Algorithm 1):

**1) Diffusion Pivotal Inversion(枢轴反演)**
- 先用 **guidance scale w=1** 做 DDIM 反演,得到一条枢轴轨迹 {z*_T, ..., z*_0}(z*_0 = z0 是输入图的 latent 编码)。选 w=1 是因为它给出「高可编辑、虽不精确」的近似(附录 Fig.9 验证 w=1 时 z_T 最接近正态、初始重建 PSNR 最高)。
- 不同于以往反演「把所有随机噪声都映射到同一张图」,本工作只围绕**单一枢轴轨迹**做局部优化——这是高效收敛的关键。

**2) Null-text Optimization(无条件 embedding 优化)**
- 用**默认 w=7.5**,从 t=T 到 t=1 逐时刻优化无条件 embedding ∅_t,目标是让当前去噪一步的结果 z_{t-1}(z̄_t, ∅_t, C) 尽量贴近枢轴 z*_{t-1}:
  min_{∅_t} || z*_{t-1} − z_{t-1}(z̄_t, ∅_t, C) ||²₂
- **每步用上一步优化结果作为起点**:每个 t 优化完后计算 z̄_{t-1} = z_{t-1}(z̄_t, ∅_t, C) 传给下一步,并用 ∅_t 初始化 ∅_{t-1}(否则推理时轨迹接不上)。
- **per-timestamp ∅_t 优于 global ∅**:论文证明用一份全局 ∅(Global null-text)难以收敛、表达力不足;逐时刻 {∅_t} 显著提升重建质量。

**关键超参(附录 D)**:扩散步数 T=50;CFG 默认 w=7.5;每个时间步内优化 N=10 次迭代;学习率 0.01;早停阈值 ε=1e-5(loss 降到该值即停)。整图反演 40s–120s(单 A100)。消融显示 250 次总迭代(≈1 分钟)即达高质量,500 次(N=10)逼近 VQAE 上界。

**没有用到的东西(刻意强调的「无」)**:不微调 U-Net、不微调 VAE、不优化条件 embedding、不要 mask、无 RLHF/DPO/蒸馏。一次反演得到的 {∅_t} 可复用于对同一张图的**多次**编辑。

## Infra(训练 / 推理工程)
- **硬件**:全部实验在**单卡 A100**(代码注明 Tesla V100 16GB 亦可,≥12GB 显存即可跑);无分布式训练需求(本身就是推理期算法)。
- **时间开销**:反演 ≈1 分钟/图;之后每次编辑约 10 秒;同一图的多次编辑共享同一次反演。推理时间是论文自陈的主要局限(达不到实时)。
- **效率对比(附录 C, Tab.2「Inference time comparison」原始单元格)**:

  | 方法 | 反演时间 | 编辑时间 | 支持多次编辑 |
  |---|---|---|---|
  | VQGAN+CLIP | — | ~1m | No |
  | Text2Live | — | ~9m | No |
  | SDEdit | — | 10s | Yes |
  | Imagic | ~5m | 10s | No |
  | **Ours** | **~1m** | **10s** | **Yes** |

  本工作 1 分钟反演 + 每次编辑 10 秒、且一次反演可复用于多次编辑,综合最优;仅 SDEdit(不做反演)更快但保真度差,Imagic 每次编辑都要 ~5 分钟微调。
- **实现栈**:基于 HuggingFace diffusers 的预训练 SD v1.4 / LDM,Python 3.8 + PyTorch 1.11,以 Jupyter notebook(`null_text_w_ptp.ipynb`)形式开源在 google/prompt-to-prompt 仓库。
- **部署形态**:研究原型(notebook),官方注明「非 Google 官方支持产品」。无量化/缓存等部署优化披露。

## 评测 benchmark(把效果讲清楚)
所有数字均来自已抓取的论文 PDF(arxiv-2211.09794)。

**重建质量(消融,COCO 100 对,指标 PSNR,Fig.4)**——以 PSNR vs 迭代次数曲线呈现,关键结论:
- 上界 **VQAE 重建**(SD 自带 auto-encoder 的天花板);下界 **DDIM inversion**(w=7.5 时重建很差,作为起点)。
- **本工作(Null-text, ours)**:500 次总迭代(N=10)收敛到接近 VQAE 上界;250 次(≈1 分钟)已达高质量。绿线在所有变体中最优、收敛最快。
- 各消融变体(均劣于完整方法):**Random pivot**(用随机轨迹代替 DDIM 枢轴)收敛慢得多——证明 DDIM 初始化对快速收敛至关重要;**Global null-text**(单一 ∅)难收敛;**Textual inversion**(优化条件 embedding + 随机噪声,即 Gal et al. 路线)收敛远慢于本工作、重建质量差;**Random caption**(随机不相关 caption)仍能收敛到接近 VQAE 上界——证明反演对 caption 鲁棒。
- **Null-text optimization without pivotal inversion**(去掉枢轴、用随机噪声优化 ∅)**完全失效**,结果甚至劣于 DDIM 基线(附录 Fig.13/14)——说明 null-text 优化表达力弱、强依赖高效的枢轴反演。
- 注:论文以 PSNR 曲线图呈现,未在正文给出单一数值表;具体逐点 PSNR 值需读图。

**编辑效果用户研究(Tab.1,50 人 × 48 图,问「哪种方法编辑更好且最大程度保留原细节」)**:
- **Ours 65.1%** / Text2Live 16.6% / SDEdit 14.5% / VQGAN+CLIP 3.8%。

**与 SDEdit 结合(Fig.8,100 例,LPIPS↓ vs CLIPScore↑)**:在 SDEdit 编辑前先做 null-text 反演,可在相同 CLIP 分下显著降低 LPIPS(更保原图细节,人脸身份保住)。证明本工作不绑定 Prompt-to-Prompt,可作为通用反演前置。

**与 Imagic 对比(附录 Fig.11)**:用非官方 SD 版 Imagic 评测,本工作 LPIPS 更低(更保真原图);Imagic 对插值参数 α 敏感(α=0.6/0.7/0.8/0.9),高 α 损图、低 α 损文,单一 α 难适配所有样本。

**消融的方法学结论**:(i) 枢轴(DDIM 初始化)是快速收敛与可行性的前提;(ii) per-timestamp ∅_t 优于 global ∅;(iii) 优化无条件 embedding(null-text)比优化条件 embedding(textual)有更准的 cross-attention map、从而编辑更好;(iv) DDIM 反演用 w=1 是甜点。

## 创新点与影响
**核心贡献**:
1. **Diffusion Pivotal Inversion**——把 GAN 的 pivotal tuning 思想引入扩散模型,只围绕单一 DDIM 枢轴轨迹做局部优化,把「映射所有噪声到一张图」的低效问题变成高效的单轨迹拟合。
2. **Null-text Optimization**——首次指出并利用「CFG 结果高度依赖无条件分支」,把可学变量放在无条件 embedding ∅_t 上,从而**冻结模型权重与条件 embedding**:既高保真又不破坏模型先验、不复制模型、保住 P2P 所需的语义 attention。
3. 二者结合,**首次让 Prompt-to-Prompt 这类文本编辑技术作用于真实照片**,且无需微调、无需 mask。

**影响**:成为 2022–2024 真实图像扩散编辑的标准基线/前置组件,「优化 null-text / 无条件 embedding 做反演」与「pivotal inversion」被后续大量编辑工作(及各种加速变体,如 Negative-prompt Inversion、ProxEdit、直接反演方法等)继承或对照;也启发了对 CFG 无条件分支可学性的进一步研究。代码合并进官方 google/prompt-to-prompt 仓库,影响力随 P2P 一同扩散。

**已知局限(论文 Sec.6)**:
- 推理慢(反演 ≈1 分钟/图),不满足实时应用;
- 受限于 SD 的 VQ auto-encoder——人脸等细节会产生伪影(优化 VQ decoder 被列为 out-of-scope);
- 受限于 P2P——SD 的 attention map 不如 Imagen 精准(词可能对错区域),复杂结构修改(如把坐着的狗变站立)做不到;
- 需要一个 source caption(可自动生成,但要编辑的词得在 caption 里)。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2211.09794
- arxiv_pdf: https://arxiv.org/pdf/2211.09794
- project_page: https://null-text-inversion.github.io/
- code(official): https://github.com/google/prompt-to-prompt/#null-text-inversion-for-editing-real-images

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2211.09794.pdf
- ../../../sources/omni/2022/null-text-inversion--project-page.md
- ../../../sources/omni/2022/null-text-inversion--code-readme.md
