---
title: "Point·E: A System for Generating 3D Point Clouds from Complex Prompts"
org: OpenAI
country: US
date: "2022-12"
type: paper
category: 3d
tags: [text-to-3d, point-cloud, diffusion, transformer, glide, clip, image-to-3d]
url: "https://arxiv.org/abs/2212.08751"
arxiv: "https://arxiv.org/abs/2212.08751"
pdf_url: "https://arxiv.org/pdf/2212.08751"
github_url: "https://github.com/openai/point-e"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2212.08751.pdf, point-e--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Point·E 是 OpenAI 提出的「文本→合成视图→彩色点云」两段式扩散系统：先用微调过的 [[glide]] 生成一张 3D 渲染图，再用基于 Transformer 的点云扩散模型从该图采样出带 RGB 的 3D 点云。它在**单张 V100/A100 上约 1–2 分钟**就能出一个 3D 物体，比 [[dreamfusion]] 等 SDS 优化方法快 **1–2 个数量级**（后者要数小时 GPU），代价是质量更低（COCO 上 1B 模型 CLIP R-Precision ViT-L/14 仅 46.8%，DreamFusion 为 79.7%）。

## 背景与定位
当时的文生 3D 主要分两条路线，各有硬伤：
1. **直接在配对 (text, 3D) 或无标注 3D 数据上训生成模型**（Text2Shape、AutoSDF、LION、CLIP-Forge 等）：采样高效，但受限于 3D 数据稀缺，难以泛化到复杂多样的文本提示。
2. **用预训练文-图模型优化可微 3D 表示**（[[dreamfusion]]、DreamFields、CLIP-Mesh、[[magic3d]]）：能处理复杂提示，但每个样本都要跑昂贵的逐物体优化（多 GPU 小时），且缺乏强 3D 先验容易陷入局部极小、生成不连贯物体。

Point·E 的核心思路是**把两条路线拼起来**：文-图阶段用海量 (text, image) 对（继承 GLIDE/[[dall-e-2]] 的语言泛化），图-3D 阶段只需较小的 (image, 3D) 配对数据即可学到 3D 先验。生成时先采一张图、再据图采点云，两步都是**前馈采样无需优化**，所以快。它牺牲质量换速度，定位是「实用的速度-质量折中」与「开源高效文生 3D 的代表作」。生成框架建立在高斯扩散（[[ddpm]]）之上，采样器采用 [[elucidating-edm]]（Karras 2022）的二阶 Heun ODE solver，并全程使用 classifier-free guidance（[[classifier-free-guidance]]，drop 概率 0.1）。

## 模型架构
整条 pipeline 实为**三个扩散模型 + 一个 SDF 回归模型**：

**1) 视图合成 GLIDE（3B 参数）**：用 GLIDE 在「原数据集 + 自有 3D 渲染图」混合上微调，专门生成与训练分布一致的合成渲染视图。

**2) 点云基础扩散模型（Base，纯 Transformer）**——本文最核心的新架构：
- 把点云表示为 **K×6 张量**：内维是 (x,y,z) 坐标 + (R,G,B) 颜色，全部归一化到 [−1,1]。直接对该张量做扩散（从 K×6 高斯噪声去噪），**预测 ε 和 Σ**（均值+方差，承自 [[improved-ddpm]]）。
- 每个点过一个线性层映射到 D 维 → K×D 输入 token；timestep t 过小 MLP → 1 个 D 维 token 前置。
- **图像条件注入**：把条件图喂进**冻结的 ViT-L/14 CLIP**，取最后一层 embedding 网格 **256×D′**，线性投影成 256×D 后前置到 Transformer 上下文。最终上下文长度 **(K+257)×D**，取输出末尾 K 个 token 投影出每个点的 ε、Σ。
- **无位置编码** → 模型对输入点云**置换不变**（permutation-invariant，但输出顺序绑定输入顺序）。相比 PVD（Zhou 2021a）等 3D 专用架构，它**更简单、几乎不含 3D 专属结构**，且首次同时生成 RGB 颜色通道。
- 关键消融结论：用 **CLIP 网格 (256 个 token) 而非单个 CLIP image/text 向量**条件效果显著更好（因为点云模型受益于更多空间信息）。

**3) 点云上采样器（Upsampler，~40M）**：架构同 Base，但额外把 1K 低分辨率点云作为条件 token（走单独的线性嵌入层，以便区分条件点 vs 新生成点，无需位置编码）。它条件于 1K 点、再生成 3K 新点，凑成 4K 点。

**4) SDF 网格提取模型（仅用于渲染评测）**：encoder-decoder Transformer——8 层 encoder 把点云当无序序列编码，4 层 cross-attention decoder 取 3D 查询坐标 + 隐向量预测 SDF 值（每个查询点独立处理，便于批量）；对 SDF 跑 marching cubes（128³ 网格）抽出 mesh，顶点颜色取最近点颜色。

**参数量**（附录 Table 2）：Base 40M（width 512 / depth 12）、300M（1024/24）、1B（2048/24，精确 1,244,311,564）、Upsampler 40.5M（512/12）。

## 数据
- **规模**：「数百万个 3D 模型」(several million) 及其元数据。SDF 回归模型在其中 **240 万个 manifold mesh** 子集上训练。具体数据集来源/版权未披露。
- **统一格式化**：用 **Blender** 把每个 3D 模型从 **20 个随机相机角度**渲染成 **RGBAD 图像**（含深度+alpha）。Blender 脚本将模型归一化到包围立方体、配标准光照、用内置实时渲染引擎导出。
- **点云构造**：对每张 RGBAD 图按像素反投影出稠密点云（数十万非均匀点），再用 **farthest point sampling** 下采样到均匀 4K 点。直接从渲染图建点云（而非从 mesh 采样），规避了采到模型内部点、奇怪文件格式等问题。
- **质量过滤**（两道启发式）：① 对每个点云做 SVD，**最小奇异值低于阈值的「扁平物体」剔除**；② 用 CLIP 特征（每个物体对所有渲染图取平均）对数据集聚类，人工把簇分到不同质量桶，最终用**加权混合**各质量桶作为训练集。
- **文本标注**：3D 数据集自带 caption（用于纯文本消融模型），主流程的文-图阶段则继承 GLIDE 的大规模 (text,image) 数据。无显式 re-captioning 披露。
- **域内渲染 trick**：因 3D 渲染图相对 GLIDE 原训练集很小，微调时**仅 5% 概率采 3D 渲染图、95% 用原数据集**；并给每张 3D 渲染图的 prompt 加一个**特殊「3D render」token**，测试时带该 token 采样以确保始终出域内渲染图。微调 100K 迭代（对 3D 数据集走过若干 epoch，但从未见过同一精确视角两次）。

## 训练方法
- **目标函数**：标准高斯扩散（DDPM），模型预测噪声 ε **和**方差 Σ。全程 classifier-free guidance（训练时随机丢条件，drop 概率 0.1）。
- **扩散步数/调度**：所有扩散模型训练用 **1024 个 timestep**；Upsampler 用 [[ddpm]] 线性噪声调度，Base 用 [[improved-ddpm]] 的 cosine 调度。
- **统一超参**（附录 Table 2）：batch size 64，训练 **1,300,000 迭代**；学习率 Base-40M 1e-4 / 300M 7e-5 / 1B 5e-5 / Upsampler 1e-4。
- **多阶段/层级**：借鉴图像扩散的「低分辨率 base + 上采样」层级——先 1K 点 base、再上采到 4K 点。计算量随点数线性增长，故生成 4K 点比 1K 点贵 4×（同模型规模下）。
- **SDF 模型训练**：在 240 万 manifold mesh 上训，点云加 σ=0.005 高斯噪声做增强；**加权 L1 目标**——`f(x)>y` 权重 1、`f(x)≤y` 权重 4（论文定义表面外侧 SDF 为负，故惩罚预测偏低更重 → 不确定时倾向判「点在表面内」），避免 mesh 忽略细/噪声部位。
- **未使用** RLHF/DPO/偏好对齐、蒸馏或一致性加速（2022 年的工作，主要靠少步 ODE 采样而非蒸馏提速）。

## Infra（训练 / 推理工程）
- **训练算力**：论文未披露 GPU 数量、GPU·时或并行/混合精度方案。仅给出 batch=64 × 1.3M iter 的规模与各模型超参。
- **推理速度**（附录 Table 4，单 V100 秒数）：GLIDE 视图合成 **46.28s**、Upsampler(40M) 12.58s、Base-40M 3.35s、Base-300M 12.78s、Base-1B 28.67s。**端到端 1B 全栈约 1.5 V100-min**（GLIDE 46s + Base-1B 28.67s + Upsampler 12.58s ≈ 87s）。这就是「单 GPU 1–2 分钟」的来源。
- **采样设置**（附录 Table 3）：点云 Base/Upsampler 用 **Karras 2022 二阶 Heun sampler，64 步（128 次函数评估）**，guidance scale 3.0，S_churn=3(base)/0(upsampler)，σ∈[1e-3,120/160]；GLIDE 用 150 步 base + 50 步上采样（不走 Karras sampler）。P-FID/P-IS 评测则用全噪声调度的随机 DDPM 采 10K 样本。
- **部署**：开源发布预训练点云扩散模型 + 评测代码/模型，提供 image2pointcloud、text2pointcloud（小而弱的纯文生 3D 模型）、pointcloud2mesh 三个示例 notebook。

## 评测 benchmark（把效果讲清楚）
**端到端指标用 CLIP R-Precision（COCO 评测 prompt）**，并新提两个点云指标 **P-IS / P-FID**（点云版 Inception Score / FID，用加宽 2× 的 PointNet++（~16M 参数）在 ModelNet40 上训得的分类器抽特征）。

**与他法对比（Table 1，COCO prompt）：**

| 方法 | CLIP R-Prec (ViT-B/32) | (ViT-L/14) | 采样延迟 |
|---|---|---|---|
| DreamFields | 78.6% | 82.9% | ~200 V100-hr |
| CLIP-Mesh | 67.8% | 74.5% | ~17 V100-min |
| DreamFusion | 75.1% | 79.7% | ~12 V100-hr |
| **Point·E (40M, text-only)** | 15.4% | 16.2% | 16 V100-sec |
| **Point·E (40M)** | 36.5% | 38.8% | 1.0 V100-min |
| **Point·E (300M)** | 40.3% | 45.6% | 1.2 V100-min |
| **Point·E (1B)** | 41.1% | 46.8% | 1.5 V100-min |
| 条件图本身 (上限参考) | 69.6% | 86.6% | — |

要点：Point·E **质量明显逊于 SOTA**（最好 1B 仅 46.8% vs DreamFusion 79.7%），但**快 1–2 个数量级**（1.5 min vs 12 V100-hr）。论文给出两点免责：① 不像多视图优化方法那样对每个视角都对齐文本，某些角度不易识别会压低 R-Precision；② 点云转 mesh 会丢信息。条件图本身的 86.6% 是 pipeline 的性能上限——说明瓶颈在图→点云一步。

**消融（Sec 5.1，P-FID/P-IS/R-Precision over training）：**
- **纯文本条件（无文-图步）显著最差**（text-only 仅 16.2%），证明文-图中介至关重要。
- **CLIP 网格 token > 单 CLIP image/text 向量**（image vec. 这种单 token 方式更差），即空间信息有用。
- **scaling 有效**：模型越大，P-FID 收敛越快、最终 R-Precision 越高（40M→300M→1B 单调提升）。
- P-IS 上限：训练集本身 P-IS 仅 12.95，模型最好约 13，已近上限。

**典型失败模式（Fig 5）：** ① 误判物体各部位相对比例（把矮长的狗生成高个狗）；② 看不到遮挡部位时错误推断（交通锥底部生成镜像第二个锥）。用 DALL·E 2 图当条件时（附录 D）会把阴影误认成深色地面，物体占图太满会变形——加白边可改善。

## 创新点与影响
**核心贡献：**
1. **两段式「文→图→3D」范式**：用预训练文-图模型作中介，把文本泛化与 3D 先验解耦，绕开 3D 配对数据稀缺，同时避免逐物体优化——这是「快速文生 3D」的关键思路。
2. **极简纯 Transformer 点云扩散架构**：无 3D 专用结构、无位置编码、置换不变，首次直接扩散生成带 RGB 的彩色点云（K×6 张量），且证明 CLIP 网格条件优于单向量。
3. **P-IS / P-FID 点云评测指标**：为点云生成提供 IS/FID 类比，被后续工作沿用。
4. **数量级提速**：把单样本生成从「多 GPU 小时」压到「单 GPU 1–2 分钟」，并开源模型/代码/评测，成为高效文生 3D 的开源基线。

**影响：** 启发了 OpenAI 自家后续的 **Shap·E**（直接生成隐式函数/NeRF+mesh，质量与可用性更高）以及一系列「图→3D 前馈生成」工作；其「先生成图再升维 3D」的思路与点云扩散范式被广泛引用。也可作为优化类方法（如 DreamFusion）的**初始化**以加速收敛（论文明确指出此用途）。

**已知局限：** ① 需合成渲染图作中介（未来可改条件于真实图）；② 输出是低分辨率点云，不含细粒度形状/纹理，转 mesh 易丢薄/稀疏部件；③ 质量整体落后优化类 SOTA；④ 继承 DALL·E 2/数据集偏见（如纯文本模型对「a woman」生成更细长物体），且可被滥用于 3D 打印危险物（论文专设伦理小节）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2212.08751
- arxiv_pdf: https://arxiv.org/pdf/2212.08751
- github: https://github.com/openai/point-e

## 一手源存档（sources/）
- [arxiv-2212.08751.pdf](https://arxiv.org/pdf/2212.08751)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/point-e--readme.md)
