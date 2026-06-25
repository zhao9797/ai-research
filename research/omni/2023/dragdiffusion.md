---
title: "DragGAN / DragDiffusion: 基于点的交互式拖拽图像编辑"
org: "MPI-Informatics / NUS / ByteDance"
country: EU
date: "2023-05"
type: paper
category: edit
tags: [drag-editing, point-based, interactive-editing, stylegan, diffusion, lora, motion-supervision, point-tracking, dragbench]
url: https://arxiv.org/abs/2305.10973
arxiv: https://arxiv.org/abs/2305.10973
pdf_url: https://arxiv.org/pdf/2305.10973
github_url: https://github.com/XingangPan/DragGAN
hf_url: https://huggingface.co/spaces/radames/DragGan
modelscope_url:
project_url: https://vcai.mpi-inf.mpg.de/projects/DragGAN/
downloaded: [arxiv-2305.10973.pdf, arxiv-2306.14435.pdf, draggan--readme.md, dragdiffusion--readme.md, draggan--project-page.html]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
DragGAN（SIGGRAPH 2023，MPI/MIT/UPenn）开创"点对点拖拽"式交互编辑——用户在图上点几对 handle(红)→target(蓝) 点，模型把红点内容精确搬到蓝点，靠 **特征级 motion supervision + 基于 GAN 判别性特征的最近邻 point tracking** 两个零额外网络的组件在 StyleGAN2 latent 上做优化，单张 RTX 3090 几秒完成；后续 **DragDiffusion**（arXiv 2306.14435，NUS×字节，后中 CVPR 2024；落盘版即对应 CVPR 含逐类补充材料的版本）把同一拖拽框架迁到 Stable Diffusion，**只优化单个扩散步 (t=35) 的 latent** 并配 LoRA 身份保持 + reference-latent-control，把适用性从单类别 GAN 扩展到任意真实/生成图像，并发布首个 drag 评测基准 **DragBench**（205 图 / 349 对点）。

## 背景与定位
可控图像合成长期靠"标注数据监督"或"先验 3D 模型"来获得 GAN 可控性，缺乏灵活性/精度/通用性；文本引导（[[dall-e-2]] [[imagen]] [[latent-diffusion-ldm]]）能改高层语义但**无法精确指定"把某点移动 N 个像素"**这种空间属性。DragGAN 把问题归结为：给定任意数量 (handle, target) 点，把 handle 精确驱动到 target。与最接近的前作 UserControllableLT（Endo 2022）相比，多解决两个难点：(1) 支持**多点**约束；(2) 要求 handle **精确到达** target（前作常到不了）。

DragDiffusion 承接此框架，针对 DragGAN 的核心瓶颈——**受限于预训练 GAN 模型容量**（每个 StyleGAN 只覆盖一个类别，真实图像还要先做难度大的 GAN inversion）。同时区别于绝大多数扩散编辑方法（Prompt-to-Prompt、Imagic、[[pix2pix-zero]] 等只改 text embedding，限于高层语义/风格），DragDiffusion 是**首个用扩散模型做点级精确空间控制**的拖拽编辑方法。并发工作 DragonDiffusion（Mou et al. 2307.02421，DragDiffusion 论文 [30] 仅注明 "concurrent"、未细述其方法）走的是基于能量/score guidance 把编辑信号转梯度的路线，与本文"直接优化单步 latent"不同。

整体处于"交互式精确编辑"技术脉络：从网格变形(as-rigid-as-possible) → GAN latent 编辑 → 点级拖拽（DragGAN）→ 扩散点级拖拽（DragDiffusion）→ 去 tracking 的 FreeDrag 等。

## 模型架构

**DragGAN（GAN 路线）**
- Backbone：预训练 **StyleGAN2**。512 维 z 经 mapping network 得到中间 latent w∈R^512（W 空间），复制送入各层；也可各层用不同 w 得到更具表达力的 **W+ 空间（w∈R^{l×512}）**。本文统一在 **W+** 优化以利于 out-of-distribution 编辑。
- 关键洞察：**GAN 生成器的中间特征足够判别性**，无需任何额外网络（光流/tracking 网络）即可同时做运动监督与点追踪。
- 取 **StyleGAN2 第 6 个 block 之后的 feature map**（256×256 分辨率，双线性插值到图像尺寸），它在分辨率与判别性间折中最佳（消融见下）。
- 只更新 w 的**前 6 层**（决定空间属性），其余层固定以保住外观（借鉴 style-mixing）。
- 无 text encoder、无条件注入，纯靠 latent 优化；真实图像编辑通过 GAN inversion（PTI）先嵌入再编辑。

**DragDiffusion（扩散路线）**
- Backbone：**Stable Diffusion 1.5**（LDM 框架：VAE 把图映到 latent，UNet 建模去噪，含 self/cross-attention）。亦验证在 SD1.5 的多个微调变体上工作（Counterfeit-V2.5、Majicmix Realistic、Realistic Vision、Interior Design Supermix、DVarch）。
- **核心架构性观察**：通过对"原图/拖拽后"两帧做 UNet 特征 PCA 可视化，发现**存在单一扩散步（如 t=35）的 UNet 特征即含足够语义+几何信息**支撑结构化空间控制 → 因此**只优化这一个时间步的 latent**（不像 universal guidance 等在多步 latent 上做梯度），效率高且精度好。
- 用于 motion supervision 的特征取 **UNet Decoder 第 3 个上采样 block**（消融最优：更浅 block 语义粗、更深 block 偏纹理）。
- 两个身份保持模块：(1) **identity-preserving fine-tuning** 用 **LoRA**（rank 16，注入所有 attention 的 q/k/v 投影）；(2) **reference-latent-control**——去噪时把优化 latent ẑ_t 的 self-attention 的 **key/value 替换成原图 latent z_t 的 k/v**（灵感来自 [[masactrl]]），让 query 去检索原图纹理，保证编辑前后一致性。

## 数据

**DragGAN**：不训练新模型，直接用现成预训练 StyleGAN2，覆盖数据集（括号为预训练分辨率）：FFHQ(512)、AFHQCat(512)、SHHQ(512)、LSUN Car(512)、LSUN Cat(256)、Landscapes HQ(256)、microscope(512)，以及 self-distilled 数据集的 Lion(512)/Dog(1024)/Elephant(512)。即"数据"即各 StyleGAN 的训练分布，编辑质量受其多样性限制。

**DragDiffusion**：同样无需训练数据（用预训练 SD）。其贡献是**评测数据集 DragBench**——首个 drag 编辑基准：共 **205 张图、349 对 handle/target 点**，分 10 类（animals、art works、buildings 城市/乡村、human 头部/上身/全身、interior design、landscape、其他物体）。**所有 human 图来自 Midjourney 生成以规避肖像法律风险**；其余为 unsplash/pexels/pixabay 的真实图。每图附 drag 指令（≥1 对点 + 可编辑区域 mask）。

## 训练方法

**DragGAN（推理时优化，无训练阶段）**——每个编辑是一个在线优化循环，每步两子步：
1. **Motion supervision**：在生成器特征图 F 上用"shifted patch loss"——把 handle p_i 周围半径 r1 的小块特征，监督其往 target 方向 d_i 移动一步：`L = Σ_i Σ_{q∈Ω1(p_i,r1)} ‖F(q) − F(q+d_i)‖_1 + λ‖(F−F0)·(1−M)‖_1`。第一项的 F(q_i) 不回传梯度（只推 p_i 往 p_i+d_i，不反向），第二项是 mask 外重建项保持不动区。该 loss 优化 latent w 一步。
2. **Point tracking**：运动监督后 handle 实际位置未知，在新特征 F′ 的半径 r2 patch 内对初始特征 f_i 做**最近邻搜索**更新 handle：`p_i := argmin_{q∈Ω2(p_i,r2)} ‖F′(q) − f_i‖_1`。
- 反复迭代直到所有 handle 距 target ≤ d 像素（d=1，>5 点时 d=2），通常 **30–200 次迭代**。
- 超参：Adam 优化 w，步长 2e-3（FFHQ/AFHQCat/LSUN Car）或 1e-3（其他）；λ=20，r1=round(3/512×size)，r2=round(12/512×size)；最大优化步在评测里设 300（paired-recon 设 100）。

**DragDiffusion（推理时优化 + 一次性 LoRA 微调）**——三阶段（见论文 Fig.3）：
1. **Identity-preserving fine-tuning**：对输入图做 LoRA 微调 UNet，目标即标准扩散重建 `L_ft = E_{ε,t} ‖ε − ε_{θ+Δθ}(α_t z + σ_t ε)‖_2^2`。**仅需 80 步**（远少于 DreamBooth 类的 1000 步），约 **25 秒/A100**（后优化到 ~20s）；之所以这么快是因为优化的是 inverted noisy latent，本身已含原图信息。
2. **Diffusion latent optimization**：先对真实图做 **DDIM inversion** 取 t=35 步 latent z_t；再照 DragGAN 思路在该单步 latent 上交替 motion supervision（`L_ms`，含 UNet 特征 patch loss + DDIM 去噪后 mask 外重建项，用 stop-gradient sg(·)）与 point tracking（UNet 特征最近邻）。学习率 0.01（Adam），最大 80 步；r1=1、r2=3、λ=0.1；DDIM 共 50 步、默认编辑 t=35。**真实图编辑时关闭 CFG**（CFG 会放大 DDIM inversion 数值误差）；编辑生成图时无需 LoRA 和 inversion（latent 现成），但要处理 CFG——把正/负 prompt 两路 UNet 特征沿 channel 拼接来监督。
3. **Reference-latent-control 去噪**：在所有去噪步的 UNet 上采样 block 用 k/v 替换引导，得到最终 ẑ_0。

无蒸馏/无步数压缩（两者本质都是推理时优化，非前馈模型）。

## Infra（训练 / 推理工程）

**DragGAN**：纯推理时优化，**不依赖 RAFT/PIPs 等额外 tracking 网络**故高效；多数情况单张 **RTX 3090 几秒**完成一次编辑，可支持 live 交互。提供 PyTorch 实现 + GUI（Gradio/visualizer），官方 repo 有 Docker 镜像（基于 NGC PyTorch，约 25GB）、Colab、HuggingFace Space、OpenXLab 在线 demo；支持 MacOS Silicon（MPS fallback）与纯 CPU。算法代码 CC-BY-NC，且要求保留 "AI Generated" 水印功能。

**DragDiffusion**：需 Nvidia GPU + Linux，约 **14 GB 显存**。A100 上各阶段耗时（512×512 真实图）：**LoRA 微调 ~25s（后优化到 ~20s）、latent 优化 10–30s（视拖拽幅度）、最终 reference-latent-control 去噪可忽略（1–2s）**。提供 Gradio UI（含 UI 内 LoRA 训练、任意宽高比、DPM++ solver、可选更好 VAE sd-vae-ft-mse、集成 [[freeu]] 提升生成图拖拽质量）；算法代码 Apache-2.0。两者均未涉及大规模分布式训练（无需训练新模型）。

## 评测 benchmark（把效果讲清楚）

**DragGAN（论文 Table 1，人脸关键点操控，主指标 Mean Distance 越低越好，单位像素；FID/Time 基于 1-point）**
| 方法 | 1 point MD | 5 points MD | 68 points MD | FID | Time(s) |
|---|---|---|---|---|---|
| No edit | 12.93 | 11.66 | 16.02 | — | — |
| UserControllableLT | 11.64 | 10.41 | 10.15 | 25.32 | **0.03** |
| Ours w. RAFT tracking | 13.43 | 13.59 | 15.92 | 51.37 | 15.4 |
| Ours w. PIPs tracking | 2.98 | 4.83 | 5.30 | 31.87 | 6.6 |
| **DragGAN (Ours)** | **2.44** | **3.18** | **4.73** | **9.28** | 2.0 |

→ MD 较 UserControllableLT 降一个数量级（11.64→2.44），FID 也最低（9.28 vs 25.32/51.37），即编辑更精确且图像质量更好；虽比前作慢（2.0s vs 0.03s）但仍交互可接受，且优于自家换 RAFT/PIPs tracking 的变体（证明 GAN 特征最近邻 tracking 更准）。

**DragGAN paired image reconstruction（Table 2，MSE×10² / LPIPS×10，越低越好）**
| | Lion | LSUN Cat | Dog | LSUN Car |
|---|---|---|---|---|
| UserControllableLT | 1.82/1.14 | 1.25/0.87 | 1.23/0.92 | 1.98/0.85 |
| **DragGAN (Ours)** | **0.66/0.72** | **1.04/0.82** | **0.48/0.44** | **1.67/0.74** |

→ 全类别全面领先。消融（Table 3）：motion sup. + tracking 均以 **StyleGAN2 第 6 block 特征最优**（MD 2.44）；r1 不敏感，r1=3 略好（Table 4）。

**DragDiffusion（DragBench 上，两指标）**——Mean Distance(MD，↓，用 DIFT 找对应点后算欧氏距离) 与 Image Fidelity(IF = 1−LPIPS，↑)。主论文 Fig.8 以坐标图报告"DragDiffusion 全面位于低 MD/高 IF 左上角"；**v6/CVPR'24 版的补充材料 Tab.1（IF）/Tab.2（MD）给出按 10 类的逐类数值**，DragGAN 用"按 CLIP 相似度选最匹配 StyleGAN"的 ensemble 评测（因每个 GAN 仅覆盖一类）。摘录如下（IF↑ / MD↓）：

| 类别 | DragGAN IF | DragDiff IF | DragGAN MD | DragDiff MD |
|---|---|---|---|---|
| art works | 0.71 | **0.88** | 59.51 | **30.74** |
| landscape | 0.84 | **0.88** | 47.60 | **36.55** |
| city | 0.74 | **0.89** | 41.94 | **26.18** |
| countryside | 0.79 | **0.88** | 46.96 | **43.21** |
| animals | 0.72 | **0.87** | 60.12 | **39.22** |
| human head | **0.91** | 0.85 | 65.14 | **36.43** |
| human upper body | 0.33 | **0.89** | 82.98 | **39.75** |
| human full body | 0.31 | **0.95** | 37.01 | **20.56** |
| interior design | 0.57 | **0.90** | 75.65 | **24.83** |
| other objects | 0.71 | **0.87** | 58.25 | **39.52** |

→ MD 全 10 类 DragDiffusion 更低（DragGAN 在 human upper/full body 上 MD 高达 82.98/37.01，IF 仅 0.33/0.31，体现 GAN ensemble 对真实人像容量不足）；IF 仅 human head 一类 DragGAN(0.91) 略高。逐类均值约 IF 0.89 vs 0.66、MD 33.7 vs 57.5（自算未加权，主论文 Fig.8 报告的样本加权均值数值略有不同）。

**消融（主论文 Fig.8/Fig.7，坐标图，无精确数表）**
- 去掉 identity-preserving fine-tuning → **MD 灾难性升高**；去掉 reference-latent-control → 主要是 **IF 下降**。两模块各司其职（精度 vs 一致性）。
- inversion 步 t 消融（t=10/20/30/40/50）：IF 随 t 单调下降、MD 先降后升，**有效区间 t∈[30,40]**，故选 t=35（最低 MD 兼顾 IF）。
- LoRA 微调步消融（0/20/40/60/80/100）：MD 陡降、IF 上升后双双 plateau，**80 步**性价比最佳。
- UNet 特征 block 消融：**Decoder 第 3 block** MD 最低、IF 较高（浅 block 语义粗、深 block 偏纹理）。

## 创新点与影响

**核心贡献**
- DragGAN：首次把"点对点精确拖拽"做成通用、跨类别的交互编辑范式；**两个零额外网络组件**——基于生成器判别性特征的 motion supervision 与最近邻 point tracking，在 GAN 图像流形上做编辑故输出真实（能幻想遮挡内容、按物体刚性形变）；point tracking 本身也超过 RAFT/PIPs。
- DragDiffusion：把该范式**迁到大规模扩散模型**，突破单类别 GAN 容量瓶颈，覆盖任意真实/生成图与多种风格；提出**单步 latent 优化**（基于"某一扩散步特征即足够"的关键观察）+ LoRA 身份保持 + reference-latent-control；发布**首个 drag 评测基准 DragBench**（205 图/349 对点）。

**影响**：DragGAN 发布即病毒式传播（GitHub 高星、引爆 "drag-based editing" 方向），直接催生 DragDiffusion、DragonDiffusion、FreeDrag（去 point-tracking）、StableDrag 等一长串后续工作；DragBench 成为该方向标准评测。MD/IF 评测协议与"特征最近邻 tracking""单步 latent 优化"成为后续常用 building block。

**已知局限**
- DragGAN：编辑质量受预训练数据多样性限制（极端 out-of-distribution 姿态会出现腿/手畸变）；**纹理贫乏区域 handle 点 tracking 易漂移**（建议选纹理丰富点）；社会影响——可被滥用伪造人物姿态/表情（论文强调须遵守肖像权与隐私法规，代码强制保留 "AI Generated" 水印）。
- DragDiffusion：偶尔部分 handle 点无法精确到达 target（多对点时 tracking 不准或 latent 优化困难）；需 LoRA 微调一步（虽仅 ~20–25s）；显存 ~14GB。

## 原始链接
- arxiv_abs (DragGAN): https://arxiv.org/abs/2305.10973
- arxiv_pdf (DragGAN): https://arxiv.org/pdf/2305.10973
- project_page (DragGAN): https://vcai.mpi-inf.mpg.de/projects/DragGAN/
- github (DragGAN): https://github.com/XingangPan/DragGAN
- hf_space (DragGAN): https://huggingface.co/spaces/radames/DragGan
- arxiv_abs (DragDiffusion): https://arxiv.org/abs/2306.14435
- arxiv_pdf (DragDiffusion): https://arxiv.org/pdf/2306.14435
- github (DragDiffusion): https://github.com/Yujun-Shi/DragDiffusion
- project_page (DragDiffusion): https://yujun-shi.github.io/projects/dragdiffusion.html

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2305.10973.pdf （DragGAN 论文 PDF，已精读）
- ../../../sources/omni/2023/arxiv-2306.14435.pdf （DragDiffusion 论文 PDF，已精读）
- ../../../sources/omni/2023/draggan--readme.md （DragGAN 官方 GitHub README）
- ../../../sources/omni/2023/dragdiffusion--readme.md （DragDiffusion 官方 GitHub README，含 release 日志/参数表）
- ../../../sources/omni/2023/draggan--project-page.html （DragGAN 官方项目页 HTML 快照）
