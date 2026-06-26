---
title: "GET3D: A Generative Model of High Quality 3D Textured Shapes Learned from Images"
org: NVIDIA
country: US
date: "2022-09"
type: paper
category: 3d
tags: [3d, gan, textured-mesh, dmtet, differentiable-rendering, stylegan, triplane, nvidia]
url: "https://nv-tlabs.github.io/GET3D/"
arxiv: "https://arxiv.org/abs/2209.11163"
pdf_url: "https://arxiv.org/pdf/2209.11163"
github_url: "https://github.com/nv-tlabs/GET3D"
hf_url: ""
modelscope_url: ""
project_url: "https://nv-tlabs.github.io/GET3D/"
downloaded: [arxiv-2209.11163.pdf, get3d--readme.md, get3d--project.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GET3D（NeurIPS 2022，NVIDIA Toronto AI Lab）是一个 **GAN** 框架，**仅用 2D 图像集合**训练却能**直接生成显式带纹理的 3D 三角网格**（arbitrary topology + 高质量几何 + 高保真纹理），把 DMTet 可微表面抽取 + Nvdiffrast 可微光栅化 + StyleGAN 2D 判别器三者串成端到端可训练的管线。最亮眼结果（Tab.2，main 版"Ours"）：ShapeNet Car FID 10.25、Chair 23.28、Motorbike 65.60、Animal 28.33；因 GET3D 直出网格，其 FID-Ori 与 FID-3D 相等，而 NeRF 系基线的 FID-3D 远高于 FID-Ori——在"实际 3D 形状质量"（FID-3D）维度上**一个数量级地超过** EG3D（EG3D Car FID-3D 21.89、Chair 46.06、Mbike 89.97、Animal 83.47 vs GET3D 10.25/23.28/65.60/28.33），生成的网格可直接导入 Blender/Maya 使用。

## 背景与定位
3D 内容创作成本高、难规模化是游戏/影视/机器人/虚拟世界的痛点。一个"实用"的 3D 生成模型理想上应同时满足三点（论文 Tab.1）：(a) 能生成有细节几何且**任意拓扑/任意 genus** 的形状；(b) 输出是图形软件原生消费的**带纹理网格**；(c) 能用更易获得的 **2D 图像**做监督。此前工作各取子集、无人全占：

- **点云/体素/隐式场生成**（PointFlow、OccNet、3D-GAN 等）：多数无纹理、需后处理转网格、且常需 3D 监督；体素受内存限制难高分辨率。
- **模板形变出纹理网格**（Textured3DGAN、DIB-R）：拓扑被模板锁死，无法变 genus。
- **3D-aware 图像合成**（GRAF、Pi-GAN、[[eg3d]]、StyleNeRF、GIRAFFE）：基于神经体渲染（NeRF 系），目标是生成多视一致的 2D 图像，**不保证能抽出有意义的 3D 形状**；即便 marching cubes 抽出几何，纹理也难提取。

GET3D 的定位是首次"三点全占"：用 **DMTet（[[dmtet]]）** 解决"显式网格 + 任意拓扑可微抽取"，用 **Nvdiffrast 可微光栅化**解决"从 2D 图像反传梯度"，从而能把成熟的 StyleGAN 2D 判别器拿来当监督。它与同期同实验室的 **DreamFusion/SDS 扩散路线**并列为非扩散的 3D 生成里程碑——GET3D 走 GAN + 显式网格，结果直接进图形管线。技术血缘上承 DefTet（NeurIPS 2020）、DMTet（NeurIPS 2021）、nvdiffrec（CVPR 2022）、DIB-R++（NeurIPS 2021）、[[stylegan2]]。

## 模型架构
整体是 `M, E = G(z)`：把高斯采样映射到带纹理网格 `M` + 纹理 `E`。采两个独立噪声 `z1, z2 ∈ R^512`（分别管几何/纹理），经两个 8 层 MLP 映射网络 `f_geo`、`f_tex`（每层 512 维 + leaky-ReLU，沿用 StyleGAN）得到 `w1 = f_geo(z1)`、`w2 = f_tex(z2)`。生成器分两支：

**几何生成器（基于 DMTet）**
- DMTet 把几何表示为定义在**可形变四面体网格**上的 **SDF**，每个顶点 `v_i` 带 SDF 值 `s_i` 和形变 `Δv_i`，通过**可微 Marching Tetrahedra** 抽出显式网格——当边两端 SDF 符号不同时插值出面，`sign(s_i)≠sign(s_j)` 即可生成任意拓扑/genus；插值公式可微，梯度能回传到 `s_i` 与 `Δv_i`。四面体网格分辨率 `tet-res=90`。
- 网络：从一个**可学习的共享特征体** `F_geo ∈ R^{4×4×4×256}` 出发，经 4 个 ModBlock3D（StyleGAN2 风格的调制/解调 3D 卷积 + 3D ResNet，每块上采 2×）升到 `F'_geo ∈ R^{32×32×32×64}`（由 `w1` 调制）；对每个四面体顶点做三线性插值取特征，拼接 `[sin(p),cos(p)]` 位置编码，经 3 个 ModFC 解出 `s` 与 `Δv`（末层 tanh 把 SDF 归一到 [-1,1]、形变归一到 ±1/tet-res）。沿用 DefTet/DMTet 实践，**用两份结构相同的几何生成器**分别出 `Δv` 和 `s`。
- **体细分（Volume Subdivision）**：对薄结构（如摩托车轮辐）需高分辨率时，把命中表面的四面体一分为八，新顶点 SDF 取边中点均值，再用额外 3D 卷积升 `F'_geo` 到 `64×64×64×8` 预测 SDF/形变残差 `s'=s+δs, Δv'=Δv+δv`。

**纹理生成器（triplane 纹理场）**
- 纹理建模为**纹理场** `c = f_t(p, w1⊕w2)`：给定表面点 3D 坐标 `p`，**同时条件于几何码 w1 和纹理码 w2**，输出 RGB。这样几何变了纹理也能随之变化。
- 用 **tri-plane 表示**（承 EG3D）：StyleGAN2 backbone 6 个 ModBlock2D 把可学习特征网格 `F_tex ∈ R^{4×4×512}` 升到三张 `256×256×32` 的轴对齐正交特征平面（N=256、C=32）；表面点投影到三平面双线性插值并求和得 `f_t ∈ R^32`，再经 3 个 ModFC（隐层 16 维）解出 RGB。
- **关键效率点**：与 EG3D/NeRF 系沿光线密集采样不同，GET3D **只在表面点采样一次**纹理场，大幅降低高分辨率渲染开销，且**天然多视一致**。

**判别器**：沿用 StyleGAN 判别器架构，**用两个独立判别器**（一个判 RGB 图、一个判 silhouette 掩膜），实验证明比单判别器稳定得多。可选地用 camera pose 条件化判别器（主要为评测时形状对齐到 canonical，去掉只掉 1.38 FID）。

**改进版生成器（Appendix A.5）**：原版几何→纹理信息流仅靠 w1⊕w2 拼接，太弱，导致几何/纹理解耦差（纹理生成器甚至会忽略纹理码）。改进版让**几何与纹理共享同一 StyleGAN2 backbone**（承 SemanticGAN），每个 ModBlock2D 分出 tGEO/tTEX 两支输出两张 triplane，几何顶点投影到几何 triplane 解 SDF/形变。共享 backbone 显著改善解耦，且在 Tab.2 上多数类 FID 更好（Chair 23.28→22.41、Mbike 65.60→48.90、Animal 28.33→27.18；Car 10.25→10.60 略升）。注：improved G 结果是论文评审后补充的。

## 数据
**只用 2D 图像 + silhouette 掩膜监督**，训练数据来自三个合成/扫描 3D 数据集的渲染图（每类单独训练一个模型）：

| 数据集 | 类别 | 形状数 | 每形状视角 | 旋转角 | 仰角 |
|---|---|---|---|---|---|
| ShapeNet (v1 Core) | Car | 7497 | 24 | [0,2π] | [π/3, π/2] |
| ShapeNet | Chair | 6778 | 24 | [0,2π] | [π/3, π/2] |
| ShapeNet | Motorbike | 337 | 100 | [0,2π] | [π/3, π/2] |
| TurboSquid | Animal | 442 | 100 | [0,2π] | [π/4, π/2] |
| TurboSquid | House | 563 | 100 | [0,2π] | [π/3, π/2] |
| RenderPeople | Human | 500 | 100 | [0,2π] | [π/3, π/2] |

- **划分**：每类 train/val/test = 70%/10%/20%，并从 test 集剔除与 train 重复的形状。形状少的类（Motorbike 337）用更多视角（100）补偿。House/Human 仅做定性评测，全部用于训练。
- **预处理**：每个形状按最长边缩放到 `e_m`（Car/Motorbike/Human 0.9、House 0.8、Chair/Animal 0.7）；用 Blender 固定光照渲染 RGB + silhouette，相机半径固定 1.2、fov 49.13°、从上半球采样。
- ShapeNet 纹理简单，故额外用 TurboSquid Animal（猫/狗/狮/熊/鹿，纹理更细）测试高保真纹理能力。
- **未用合成/re-caption 数据，无美学/安全过滤**（学术 benchmark 数据集），无图文对（非文本条件主路）。

## 训练方法
- **训练目标：对抗（GAN）**，**非扩散非 flow**。非饱和 logistic loss `g(u)=-log(1+exp(-u))` + **R1 正则**（lazy regularization，每 16 步对判别器施加一次）。总损失 `L = L(D_rgb,G) + L(D_mask,G) + μ·L_reg`。
- **可微渲染监督**：假设相机分布 C 已知，每步随机采相机，用 **Nvdiffrast** 高效可微光栅化把生成网格渲成 silhouette 和"每像素含对应 3D 表面点坐标"的图，再用这些坐标查纹理场得 RGB；因 R 可微，梯度从 2D 图反传到两个 3D 生成器。
- **几何正则 L_reg**：对四面体网格中 SDF 符号不同的唯一边集 `S_e`，用 SDF 邻居间的交叉熵惩罚，去掉视图中不可见的内部浮动面（承 nvdiffrec）；`μ=0.01`。
- **超参**（Appendix A.6）：Adam，lr 0.002，β=0.9。**R1 权重 γ 逐类不同**：Chair 3200、Car 80、Animal 40、Motorbike 80、RenderPeople 80、House 200（注：官方 README 训练命令对 Car 用 `--gamma=40`，与论文文本 80 不一致；按论文文本录入）。batch size 32。**从零训练，不用 progressive growing、不用预训练 checkpoint 初始化**。实现基于 StyleGAN2 官方 PyTorch + StyleGAN3 的 CUDA 扩展。
- **无蒸馏/无步数加速**（GAN 单步前向，本就快），无 SFT/RLHF/DPO（非 LLM 范式）。
- **应用扩展的训练技巧**：
  - **无监督材质生成**：把纹理生成器改成输出 5 通道反射率场（Disney BRDF：base color R³ + metallic R + roughness R），用 DIB-R++ 的 spherical-Gaussian deferred 渲染管线（每张 HDR 全景拟 32 个 SG lobe）渲出 view-dependent 光照图喂判别器，**无材质标注**即学出合理材质分解。
  - **文本引导**：fine-tune 预训练 GET3D，沿用 StyleGAN-NADA 双生成器（可训 `G_t` + 冻结 `G_f`），16 个随机相机渲图，最小化方向 CLIP loss；采 500 对噪声，先少步筛 top-50 再优化 300 步。

## Infra（训练 / 推理工程）
- **训练算力**：所有实验 **8× A100 GPU，batch 32，单模型约 2 天收敛**（每类单独训）。开发/测试用 V100 或 A100。
- **核心工程依赖**：Nvdiffrast（高性能可微光栅化，使可训到 **1024×1024** 高分辨率渲染——隐式/NeRF 系难做到）、Kaolin、StyleGAN3 的自定义 CUDA 扩展（需 CUDA 11.1+、PyTorch 1.9.0、Python 3.8）。后续（2023-09）加入 **FlexiCubes** 作为 DMTet 的 drop-in 替代等值面表示（`--iso_surface flexicubes`）。
- **推理**：单 GPU 16GB 显存即可做推理可视化（batch 4）。GAN 单次前向直接出网格，无多步去噪/缓存/量化需求；可一键导出带纹理网格（用 **xatlas** 求 UV，把 3D 网格 warp 到 2D 平面再查纹理场离散成纹理图）。
- **部署形态**：开源官方 PyTorch 实现 + Docker 镜像 + ShapeNet 预训练权重（2022-10 发布），NVIDIA Source Code License。

## 评测 benchmark（把效果讲清楚）
**指标**：几何用 Chamfer Distance(CD) 与 Light Field Distance(LFD) 配 **COV（覆盖率/多样性，↑）** 与 **MMD（最小匹配距离/质量，↓）**；纹理+几何整体用 **FID**——其中 **FID-Ori**（用 baseline 自己的神经体渲染出图，偏袒 NeRF 系）与本文提出的 **FID-3D**（从隐式场 marching cubes 抽网格、再用像素射线交点 3D 坐标查网络取 RGB，更反映真实 3D 形状质量；对直出网格的 GET3D 二者相同）。每类渲 50k 图算 FID。

主结果（Tab.2 逐字录入；MMD-CD ×10³；FID 列 Ori/3D 对直出网格的 GET3D 二者相等；"Ours"=main 即两个独立几何生成器，"improved G"=共享 backbone 改进版，"Subdiv."=加体细分）：

| 类别 | 方法 | COV-LFD↑ | COV-CD↑ | MMD-LFD↓ | MMD-CD↓ | FID-Ori↓ | FID-3D↓ |
|---|---|---|---|---|---|---|---|
| **Car** | EG3D | 60.16 | 49.52 | 1527 | 0.72 | 15.52 | 21.89 |
| | **Ours** | 66.78 | 58.39 | 1491 | 0.71 | **10.25** | **10.25** |
| | Ours+Subdiv. | 62.48 | 55.93 | 1553 | 0.72 | 12.14 | 12.14 |
| | Ours(improved G) | 59.00 | 47.95 | 1473 | 0.81 | 10.60 | 10.60 |
| **Chair** | EG3D | 58.31 | 50.14 | 3444 | 4.72 | 38.87 | 46.06 |
| | **Ours** | 69.08 | 69.91 | 3167 | 3.72 | 23.28 | 23.28 |
| | Ours+Subdiv. | 71.59 | 70.84 | 3163 | 3.95 | 23.17 | 23.17 |
| | Ours(improved G) | 71.96 | 71.96 | 3125 | 3.96 | **22.41** | **22.41** |
| **Mbike** | EG3D | 38.36 | 34.25 | 4199 | 2.21 | 66.38 | 89.97 |
| | **Ours** | 67.12 | 67.12 | 3631 | 1.72 | 65.60 | 65.60 |
| | Ours+Subdiv. | 63.01 | 61.64 | 3440 | 1.79 | 54.12 | 54.12 |
| | Ours(improved G) | 69.86 | 65.75 | 3393 | 1.79 | **48.90** | **48.90** |
| **Animal** | EG3D | 74.16 | 58.43 | 4889 | 3.42 | 40.03 | 83.47 |
| | **Ours** | 79.77 | 78.65 | 3798 | 2.02 | 28.33 | 28.33 |
| | Ours+Subdiv. | 66.29 | 74.16 | 3864 | 2.03 | 28.49 | 28.49 |
| | Ours(improved G) | 74.16 | 82.02 | 3767 | 1.97 | **27.18** | **27.18** |

（3D-监督基线 PointFlow / OccNet 不输出纹理网格故无 FID；3D-aware 基线 Pi-GAN/GRAF 行见 PDF，被 GET3D 全面超过。）

**关键结论**：
- 对 **3D-aware 图像合成 baseline**：Pi-GAN/GRAF 在所有类所有指标被**大幅碾压**；与最强的 EG3D 比，论文自述 **FID-Ori（纯 2D 图）相当**，但 **FID-3D（真实 3D 形状质量）GET3D 一个数量级地领先**（Car 10.25 vs 21.89、Chair 23.28 vs 46.06、Mbike 65.60 vs 89.97、Animal 28.33 vs 83.47——EG3D 用 marching cubes 抽网格后 FID 暴涨数倍），证明 GET3D 真在学有意义的 3D 几何+纹理，而非"看着像但抽不出形状"。
- 对 **3D 监督 baseline**：胜 OccNet（COV/MMD 全面更好、几何更细）；PointFlow 在 MMD-CD 上更优（它直接优化点位置偏袒 CD），但 GET3D 在 MMD-LFD 更好。

**消融**：
- **图像分辨率**（Tab.3）：分辨率越高指标越好——Car 从 128² 到 1024²，FID 39.21→10.25、COV-LFD 9.28→66.78，印证高分辨率训练对捕捉细节关键（隐式法难利用高分辨率）。
- **体细分**：对薄结构类（Motorbike）显著提升，对 Chair/Car 无增益（初始 tet 分辨率已够）。
- **双判别器**（Fig.H/I）：单判别器训练严重不稳甚至发散；双判别器大幅稳住训练。
- **相机条件**（Tab.B）：去掉相机条件 FID 11.63 vs 有 10.25，仅掉 1.38，主要价值在便于 canonical 评测。
- **鲁棒性**（Tab.C）：相机加噪 FID 10.25→19.53；用 Detectron2/PointRend 预测掩膜（Mask-Black IoU 97.4 / Mask-Random IoU 95.8）FID 升到 29.68/33.16，但视觉质量仍接近，说明对不完美相机/掩膜有一定鲁棒性。
- **"真实"图像**（GANverse3D 生成的 car 数据 + DatasetGAN 掩膜 + SfM 相机）：可训出合理结果，展示走向真实数据的潜力。
- **Human Body**（Tab.D）：FID-Ori EG3D 13.77 / GET3D 14.27（相当），FID-3D EG3D 60.42 / GET3D 14.27（GET3D 远胜）。

## 创新点与影响
**核心贡献**：
1. **首个**同时满足"任意拓扑显式带纹理网格 + 仅 2D 图像监督 + 直接进图形管线"的 3D 生成模型；把 DMTet 可微表面抽取 + Nvdiffrast 可微光栅化 + StyleGAN 2D 判别器组装成端到端 GAN。
2. 几何/纹理双码 + triplane 纹理场**只在表面点采样一次**的设计，使其能高效训到 1024² 高分辨率，并天然多视一致。
3. 提出 **FID-3D** 评测协议，更公正地衡量 3D-aware 方法的"真实 3D 形状"质量（暴露 NeRF 系 FID-Ori 好但 FID-3D 崩的问题）。
4. 灵活可扩展：无监督材质分解（Disney BRDF + SG 渲染）、CLIP 文本引导 3D 生成、潜空间插值/局部编辑。

**影响**：作为非扩散路线的 3D 生成代表作，与同期 DreamFusion/SDS 扩散线并列里程碑；其 DMTet+可微渲染+GAN 范式被后续大量"显式网格生成 / image-to-3D / 文本到 3D"工作沿用，FlexiCubes 也由本实验室作为等值面升级回灌到 GET3D。开源代码 + 预训练权重推动了 3D 生成工程化落地。

**已知局限**（作者明说）：
- 训练仍**依赖 2D silhouette 和已知相机分布**，因此论文**只在合成数据上评测**（real-world 仅 GANverse3D 间接实验）；要上真实数据需借助实例分割 + 相机位姿估计。
- **每类单独训练**，未做跨类联合，难表达类间多样性。
- 涉及生成 3D 人体等敏感应用时需谨慎去偏（继承训练数据偏见）。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2209.11163
- paper (PDF): https://arxiv.org/pdf/2209.11163
- project page: https://nv-tlabs.github.io/GET3D/ （= https://research.nvidia.com/labs/toronto-ai/GET3D/）
- github: https://github.com/nv-tlabs/GET3D

## 一手源存档（sources/）
- [arxiv-2209.11163.pdf](https://arxiv.org/pdf/2209.11163)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/get3d--readme.md)
- [project.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/get3d--project.md)
