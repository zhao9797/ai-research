---
title: "Imagen Video: High Definition Video Generation with Diffusion Models"
org: Google Research (Brain Team)
country: US
date: "2022-10"
type: tech-report
category: video
tags: [text-to-video, cascaded-diffusion, v-prediction, classifier-free-guidance, progressive-distillation, video-diffusion, u-net]
url: "https://imagen.research.google/video/"
arxiv: "https://arxiv.org/abs/2210.02303"
pdf_url: "https://arxiv.org/pdf/2210.02303"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://imagen.research.google/video/"
downloaded: [arxiv-2210.02303.pdf, imagen-video--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Imagen Video 是 Google 把 [[imagen]] 的「冻结 T5 文本编码 + 级联扩散 + CFG」范式扩展到时域的文生视频系统，用 **7 个视频扩散子模型（共 11.6B 参数）** 的空间/时间超分级联，从纯文本生成 **1280×768 分辨率、24fps、128 帧（约 5.3 秒）** 的高清视频；核心方法贡献是确认 **v-prediction 参数化** 与 **带 guidance 的 progressive distillation** 在视频上同样有效——蒸馏后整条级联仅需每级 8 步采样、整体快约 18×（FLOPs 省约 36×），且质量几乎无损。

## 背景与定位
2022 年文生图（[[dall-e-2]]、[[imagen]]、Parti、[[latent-diffusion-ldm]]）已成熟，但文生视频仍停留在受限数据集与中等分辨率：此前的视频扩散工作（Video Diffusion Models, Ho et al. 2022b）只能做到 64 帧、128×128、24fps。Imagen Video 要解决的是**把扩散模型扩展到高清、高帧率、强文本对齐的开放域视频生成**。

它在技术脉络上的位置：
- 直接继承 [[imagen]] 的两大支柱——**冻结的大语言模型文本编码（T5-XXL）** 和 **[[cascaded-diffusion-models]]（级联扩散 + 噪声条件增强）**，把它们从「图像超分级联」推广到「空间 + 时间双向超分级联」。
- 与同期工作 **[[make-a-video]]**（Meta，2022-09）形成对照：Make-A-Video 复用预训练文生图模型 + 无标注视频学运动；Imagen Video 则**从零训练 7 个原生视频扩散模型**，在视频-文本对上联合训练（并混入大规模图文对）。
- 相比早期自回归/RNN 路线（[[videogpt]]、[[cogvideo]]、GODIVA/NÜWA），它是**非自回归、整块帧同时生成**的纯扩散方案。
- 关键意义：验证了「级联扩散 + v-prediction + CFG + 蒸馏」这一套图像域成功配方在视频上的**可扩展性**，并给出视频扩散随参数量持续受益（未饱和）的 scaling 证据。

注：官方明确**未发布模型与代码**（出于安全/偏见顾虑），属闭源研究成果；本页全部数字来自 arXiv 技术报告与官方项目页。

## 模型架构
**整体：7 个视频扩散模型的级联，1 个冻结文本编码器，总计 11.6B 扩散参数。** 级联结构（frames×width×height）：

| 阶段 | 类型 | 参数 | 输出尺寸 | 帧率 |
|---|---|---|---|---|
| T5-XXL | 文本编码（冻结） | 4.6B | — | — |
| Base | 文生视频基模 | 5.6B | 16×40×24 | 3fps |
| TSR | 时间超分 | 1.7B | 32×40×24 | 6fps |
| SSR | 空间超分 | 1.4B | 32×80×48 | 6fps |
| SSR | 空间超分 | 1.2B | 32×320×192 | 6fps |
| TSR | 时间超分 | 780M | 64×320×192 | 12fps |
| TSR | 时间超分 | 630M | 128×320×192 | 24fps |
| SSR | 空间超分 | 340M | 128×1280×768 | 24fps |

（共 3 个 SSR + 3 个 TSR + 1 个 base；SSR 把全部帧做空间放大，TSR 在已有帧之间插值补帧。所有模型**整块帧同时去噪生成**，避免逐帧超分的时序伪影。）

- **Backbone：Video U-Net（时空可分离的 3D U-Net）**。在 2D U-Net（空间卷积 + 空间注意力）基础上，交错插入时间维度的注意力/卷积层（见论文 Fig.7 的 space-time separable block）：空间操作在各帧上独立、参数共享；时间操作跨帧混合激活。
- **base 模型用时间注意力（temporal attention）** 建模长程时序依赖；**SSR/TSR 模型用时间卷积（temporal convolution）** 替代时间注意力以省显存/算力，维持局部时序一致（作者初步实验发现超分阶段时间注意力无明显增益，归因于条件输入本身已高度时序相关）。
- **空间注意力**：base 与前两个 SSR 有空间注意力（提升保真）；**到最高分辨率改为全卷积**（fully-convolutional）以控显存。最高分辨率 SSR 在**随机低分辨率空间裁剪**上训练，采样时可泛化到全分辨率。
- **文本注入**：用冻结 **T5-XXL** 的上下文 embedding 作为条件，注入**所有 7 个模型**（不只 base），作者称对文本对齐至关重要，并观察到与 Imagen 一致的「深层语言理解」（如准确拼写文字、3D 物体理解）。
- **超分的条件注入方式**：把上采样后的低分辨率条件视频**按通道拼接**到带噪 latent zt（同 SR3 / Palette 机制）；空间上采样用双线性 resize，时间上采样用重复帧或填空白帧。

## 数据
- **训练数据**（Sec.3）：内部数据集 **1400 万 video-text 对** + **6000 万 image-text 对**，外加公开 **LAION-400M** 图文数据集。
- **图像-视频联合训练**：把单张图片当作「单帧视频」打包成与视频等长的序列，并通过 mask 跳过时间卷积残差块与时间注意力图，从而能在远大于视频-文本数据的图文数据上训练。作者报告联合训练**显著提升视频样本整体质量**，并带来**图像→视频的知识迁移**（如只在自然视频上学动态、但能从图片学到素描/油画等风格，进而生成各种风格的视频动态）。
- **数据预处理**：图像/视频用抗锯齿双线性 resize 到目标空间分辨率；视频通过**跳帧（frame skipping）** 调到各阶段所需时间分辨率。
- **配比/清洗/美学过滤/re-captioning**：未披露具体清洗与配比细节。安全方面提到 T5-XXL 与训练数据含「问题数据」（social bias / stereotype），内部试用阶段对**输入文本做 prompt 过滤、对输出视频做内容过滤**，但承认仍有难以检测的偏见，故决定不公开发布模型。

## 训练方法
- **生成框架**：连续时间扩散模型（采用 Kingma et al. 2021 的 VDM 公式 + 连续时间版 cosine 噪声调度）；训练目标为标准 noise-prediction 简单损失，但**全部模型用 v-prediction 参数化**（v ≡ α·ε − σ·x）。
- **v-prediction 的作用**（Sec.2.4 / 3.3）：数值更稳定、利于 progressive distillation；在高分辨率阶段**避免高分辨率扩散常见的颜色漂移**，在视频上避免「跨帧时序颜色漂移」；且**样本质量指标收敛更快**——论文 Fig.13 显示 80×48→320×192 SSR 上，ε-prediction 的 First-Frame FID 收敛明显慢于 v-prediction，且 ε-prediction 出现全局色偏与跨帧不一致。
- **噪声条件增强（noise conditioning augmentation）**：所有 SSR/TSR 在训练时对条件低分辨率视频加随机 SNR 的高斯噪声并把该 SNR 喂给模型；采样时用固定小幅增强（如 SNR=3 或 5）。作用是降低级联各阶段间的 domain gap、支持 7 个模型**并行独立训练**。
- **Classifier-Free Guidance（CFG）**（Sec.2.6.1）：以 dropout 文本条件方式联合训练条件/无条件模型，采样时 x̃ = (1+w)·x̂(z,c) − w·x̂(z)；可在 v-space / ε-space / x-space 等价执行。作者称 CFG 对高保真且贴合 prompt 至关重要。详见 [[classifier-free-guidance]]。
- **大 guidance 权重的处理**：大 w 会产生饱和伪影；除 Imagen 的 **dynamic thresholding（动态裁剪）** 外，提出 **oscillating guidance（振荡引导）**——前若干步用恒定大 w（如 15）打开模式、之后在大 w(15) 与小 w(1) 间交替，兼顾文本对齐与抑制饱和；仅在 base 与前两个 SR（≤80×48）上有效，更高分辨率反而变差。
- **Progressive Distillation（带 guidance + 随机采样器）**（Sec.2.7）：两阶段——① 先把「条件 + 无条件 + guidance 权重组合」蒸成单个模型（吸收 CFG，推理时只跑一次而非两次）；② 再做 progressive distillation，每轮把 N 步 DDIM 蒸到 N/2 步。蒸馏后用 Karras 式随机采样器（每步一次大步长确定性 DDIM 更新 + 一次原步长随机回退）。**最终 7 个模型全部蒸到每级 8 步**，感知质量无明显损失。
- **Scaling 发现**（Sec.3.2）：base 视频模型从 500M→1.6B→5.6B（增大基础通道数与深度），FVD 与 CLIP score（4096 样本）均持续改善——与 Imagen 文生图「U-Net scaling 收益有限」相反，说明**视频建模更难、当前规模尚未饱和**，预示进一步 scaling 有空间。

## Infra（训练 / 推理工程）
- **训练并行**：级联 7 个模型可**各自独立、并行训练**（噪声条件增强解耦了阶段间依赖）；超分模型是通用视频超分器，可作用于真实视频或其他生成模型（如 Parti）的输出。
- **算力规模 / GPU·时 / 加速器型号 / 吞吐**：技术报告**未披露**（仅在致谢中感谢 Erica Moreira 提供 compute 资源，未给 TPU/GPU 数量与训练时长）。
- **推理加速（有具体数字）**：原始级联一个 batch 采样 **618 秒**（base 256 步、SR 128 步，且每模型为 CFG 评估两次）；蒸馏级联每级 8 步、且把 guidance 吸收进单模型只评估一次——整条蒸馏级联仅 **35 秒**，**约 18× 更快**；按 FLOPs 计**约 36× 更高效**（因省去 CFG 的双次前向）。中间档（原始 base + 蒸馏 SR）约 135 秒。
- **采样器**：默认离散时间 ancestral sampler（带 γ 控制随机性）；可选确定性 DDIM；蒸馏后用上面的随机 N 步采样器。
- **部署形态**：闭源、未发布，仅论文 + 项目页 demo。

## 评测 benchmark（把效果讲清楚）
评测指标：逐帧 **FID**（Heusel 2017）、**FVD**（Unterthiner 2019，衡量时序一致性）、逐帧 **CLIP score** 与 **CLIP R-Precision**（top-1，R=1，视频各帧共享同一 prompt 标签）。

**Table 1（192×320、128 帧、24fps，prompt 来自测试集；4 次运行均值±标准误）**——比较原始 vs 蒸馏（绿底为蒸馏）：

| Guidance w | Base 步数 | SR 步数 | CLIP Score | CLIP R-Precision | 采样时间 |
|---|---|---|---|---|---|
| constant=6 | 256 | 128 | 25.19±.03 | 92.12±.53 | 618 sec |
| oscillate(15,1) | 256 | 128 | 25.02±.08 | 89.91±.96 | 618 sec |
| constant=6 | 256 | 8（蒸馏SR） | **25.29±.05** | 90.88±.50 | 135 sec |
| oscillate(15,1) | 256 | 8（蒸馏SR） | 25.15±.09 | 88.78±.69 | 135 sec |
| constant=6 | 8（全蒸馏） | 8 | 25.03±.05 | 89.68±.38 | 35 sec |
| oscillate(15,1) | 8（全蒸馏） | 8 | 25.12±.07 | 90.97±.46 | 35 sec |
| ground truth | — | — | 24.27 | 86.18 | — |

关键结论：
- **全蒸馏（8 步×8 步，35 秒）质量与原始级联（618 秒）几乎持平**：用 oscillating guidance 时全蒸馏甚至略好；用 fixed guidance 时全蒸馏略低但差距很小。**最高 CLIP score（25.29）来自「原始 base（fixed guidance）+ 蒸馏 SR」组合。**
- **所有生成样本的感知指标都高于 ground truth 视频**（CLIP score 25.x vs 24.27，R-Precision ~90 vs 86.18）——作者解释为 CFG 把采样分布向这些质量指标「倾斜」，而非精确逼近原数据分布。
- **Scaling（Fig.11）**：base 16×40×24 模型从 500M→1.6B→5.6B，FVD 与 CLIP（0–100 标度，4096 样本）均单调改善。
- **参数化消融（Fig.12–13）**：v-prediction 在高分辨率 SSR 上 FID 收敛远快于 ε-prediction，且无跨帧色偏。

**未与外部 SOTA 同表横评**：报告未给出与 Make-A-Video / CogVideo 等的同基准定量对比表（无 UCF-101/Kinetics FVD 对照、无 VBench——VBench 是更晚的基准）；定量评测集中在自家测试集的 CLIP/FVD/FID 与内部消融。定性能力（艺术风格迁移、3D 物体旋转理解、多种风格的文字动画）以样例展示为主。

## 创新点与影响
**核心贡献**：
1. 首次把 [[imagen]] 的「冻结大 LM 文本编码 + [[cascaded-diffusion-models]] + CFG」整套配方系统性地搬到**高清高帧率视频**（128 帧 1280×768 24fps，≈1.26 亿像素），并以 11.6B 参数的 7 模型级联实现。
2. **空间超分 + 时间超分交错级联**的设计，整块帧同时生成、超分时插帧补时间分辨率。
3. 给出对扩散模型有普遍意义的两个发现：**v-prediction 在视频/高分辨率下显著优于 ε-prediction**（收敛快、无色偏）；**带 guidance 的 progressive distillation 在视频上同样有效**（每级 8 步，18×/36× 加速）。
4. **图像-视频联合训练**带来的知识迁移（图片风格→视频动态）与 scaling 未饱和的证据。

**影响**：与同期 [[make-a-video]] 共同确立 2022 年扩散主导的开放域文生视频；v-prediction + 蒸馏的工程经验被后续视频/图像扩散广泛沿用；级联（像素空间多阶段超分）路线在后来逐渐被 **latent-space 视频扩散（如 Stable Video Diffusion / latent DiT 路线）** 取代，但本工作的 scaling 与时序设计仍是重要参照。

**已知局限**：
- **像素空间级联开销大**、7 模型管线复杂；3D 一致性「大致保持但不精确」。
- **闭源不发布**（安全/偏见顾虑），无法复现/二次开发。
- 训练算力、TPU 配置、数据清洗/配比等工程细节**未披露**；缺与外部模型的标准基准定量横评。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2210.02303
- arxiv_pdf: https://arxiv.org/pdf/2210.02303
- project_page: https://imagen.research.google/video/

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2210.02303.pdf
- ../../../sources/omni/2022/imagen-video--project-page.md
