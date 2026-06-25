---
title: "TRELLIS: Structured 3D Latents for Scalable and Versatile 3D Generation"
org: "Microsoft Research / Tsinghua / USTC"
country: China
date: "2024-12"
type: paper
category: 3d
tags: [3d-generation, slat, rectified-flow, dit, sparse-voxel, dinov2, image-to-3d, text-to-3d, gaussian-splatting, mesh]
url: "https://arxiv.org/abs/2412.01506"
arxiv: "https://arxiv.org/abs/2412.01506"
pdf_url: "https://arxiv.org/pdf/2412.01506"
github_url: "https://github.com/microsoft/TRELLIS"
hf_url: "https://huggingface.co/microsoft/TRELLIS-image-large"
modelscope_url: ""
project_url: "https://microsoft.github.io/TRELLIS/"
downloaded: [arxiv-2412.01506.pdf, trellis--readme.md, trellis--hf-card.md, trellis--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
TRELLIS 提出统一的**结构化潜表示 SLAT（Structured LATent）**——稀疏 3D voxel 网格上挂载 DINOv2 多视图视觉特征——配合**两阶段 rectified flow transformer** 生成，单套潜空间可解码出 3D Gaussian / Radiance Field / Mesh 三种格式，文/图→高质量 3D 约 10 秒一件；最大 2B 参数，在 Toys4k 上全面碾压同期方法（image-to-3D 用户研究偏好率 **94.5%**，文生 3D **67.1%**），是 2024 末开源 3D 生成 SOTA（CVPR 2025 Highlight）。

## 背景与定位
3D 生成长期落后于 2D：根因是 3D 表示碎片化（mesh / 点云 / [[nerf]] Radiance Field / 3D Gaussian 各自为政），不像 2D 图像那样能在统一 latent 空间里做生成（如 [[latent-diffusion-ldm]] 的范式共识）。已有路线各有短板：
- **2D 辅助路线**（DreamFusion 蒸馏、LGM/InstantMesh 多视图重建）泛化好但几何差，受多视图不一致拖累；
- **原生 3D latent 路线**：偏几何的（CLAY、3DShape2VecSet）外观弱、需额外贴图；偏外观的（LN3Diff triplane、GaussianCube）几何不可靠；3DTopia-XL 用 latent primitive 同时编码几何外观，但 pre-fitting 既昂贵又有损。

TRELLIS 的核心主张：**在 latent 空间显式引入稀疏 3D 结构**（active voxel 勾勒粗结构，便于高分辨率建模与局部编辑），并用**强视觉基础模型 DINOv2** 为这些 voxel 编码细节，从而绕开专用 3D encoder、消除逐资产对齐 3D 的昂贵 pre-fitting（论文称 "fitting-free training"）。一个 latent → 多种输出格式，做到"表示无关"的资产建模。技术骨架直接承接 [[stable-diffusion-3]]（SD3 的 rectified flow transformer、QK-Norm、logitNorm 时间步采样）与 [[dit-scalable-diffusion-transformers]]（adaLN 调制、packing）。

## 模型架构
整体分两大块：**编解码（SLAT 表示学习）** 与 **生成（两阶段 flow transformer）**。

**SLAT 表示。** 3D 资产 O 编码为 `z = {(z_i, p_i)}`，p_i 是与物体表面相交的 active voxel 在 N×N×N 网格中的位置索引，z_i∈R^C 是挂在该 voxel 上的局部 latent。默认 **N=64**，因稀疏性平均仅 **L≈20K** 个 active voxel（L≪N³），从而支持高分辨率建模。

**视觉特征聚合（编码入口）。** 对每个资产渲染密集多视图，用**预训练 DINOv2** 提取特征图；每个 active voxel 投影回多视图特征图、取对应位置特征的**均值**作为体素特征 f_i，分辨率与 SLAT 一致（64³）。论文强调：DINOv2 特征 + active voxel 粗结构，足以高保真重建原资产，无需专用 3D encoder。

**Sparse VAE（结构化 latent 编解码）。** transformer-based VAE：encoder E 把 f 编为 z（带 KL 正则），decoder D 解回 3D。处理稀疏：把 active voxel 序列化为变长 token + 正弦位置编码，块内用 **3D 平移窗口注意力（3D shifted-window attention，Swin 风格）**——把 64³ 空间切成 8³ 窗口，相邻层窗口平移 (4,4,4) 重叠，既增强局部交互又比全注意力高效。VAE 主体 12 层、dim 768、12 头（E/D 各约 85M 参数）。

**多格式解码器**（三者架构相同、仅输出层不同）：
- **D_GS（3D Gaussian）**：每个 z_i 解出 K=32 个 Gaussian（位置偏移 o、颜色 c、尺度 s、不透明度 α、旋转 r），用 `x = p_i + tanh(o)` 把 Gaussian 约束在所属 voxel 邻域保持局部性。
- **D_RF（Radiance Field）**：每 voxel 预测 4 个正交向量，构成 8³ 局部辐射体积的 **CP 分解**（rank R=16，参考 Strivec），组装成 512³ 辐射场；自研 CUDA 可微渲染器把排序/ray marching/积分/CP 重建融成单 kernel 实时渲染。
- **D_M（Mesh）**：输出 **FlexiCubes** 的柔性参数 w∈R^45 与 8 顶点 SDF 值 d∈R^8；在 transformer 后接两层稀疏卷积上采样把分辨率提到 **256³**，从 0 等值面提网格，并额外预测顶点颜色/法线。

实践上：**用 Gaussian 端到端训练 encoder+decoder**，再**冻结 encoder、各格式 decoder 从头单训**——尽管 latent 是 Gaussian 学出来的，仍能高保真重建 RF/mesh（强可扩展性）。

**两阶段生成。**
- **Stage 1 稀疏结构生成 G_S**：先把 active voxel 转成稠密二值网格 O∈{0,1}^64³，再用一个 3D 卷积 VAE（U-Net 形，64³→16³，通道 8）近无损压成连续 latent 网格 S，喂给 transformer 去噪。架构是标准 DiT 风：序列化 + 位置编码，时间步用 adaLN+gating 注入，条件经 **cross-attention** 注入。
- **Stage 2 局部 latent 生成 G_L（sparse flow transformer）**：在给定结构上生成 z_i。先用稀疏卷积下采样把 2³ 局部 latent 打包成更短序列（类 DiT packing 提效），过若干 time-modulated transformer 块，末尾稀疏卷积上采样 + skip connection 恢复 64³。
- **条件注入**：文本用 **CLIP** 特征，图像用 **DINOv2** 特征，均经 cross-attention 当 K/V。两阶段独立用 CFM 目标训练，推理时顺序生成。

**条件编码器**：文本 CLIP、图像 DINOv2。**模型规模/分辨率**：SLAT 默认 64³×channel 8；三档总参数 **342M(B) / 1.1B(L) / 2B(XL)**（HF 标 image-large 总参 1.2B）。XL 版 G_S≈975M、G_L≈1073M（text 版）。训练稳定性借鉴 SD3 用 **QK-Norm（RMSNorm 作用于 Q/K）** 抑制注意力 norm 爆炸。

## 数据
**TRELLIS-500K**（已开源数据集 + 制备工具）：从 4 个公开 3D 数据集严选约 **500,777** 个高质量资产：
- **Objaverse-XL**：仅取 Sketchfab(Objaverse-V1) 与 GitHub 两个子集（其余太脏）。原始 sketchfab 796,031、github 5,238,768，经美学过滤后留 **sketchfab 168,307 + github 311,843**（美学阈值 5.5）。
- **ABO**（亚马逊艺术家家具，63 类，原始约 8K）→ 留 **4,485**（阈值 4.5）；
- **3D-FUTURE**（设计师家具，约 16.5K）→ 留 **9,472**；
- **HSSD**（人工合成室内场景，约 14K）→ 留 **6,670**。
- 评测集 **Toys4k**（约 4K，105 类，从不参与训练）过滤后 3,229；重建实验抽 **500** 个 Toys4k 实例，生成实验用 **1,250** 个 Toys4k 子集 + **5,000** 个训练集子集分别评测。

**清洗过滤**：每资产渲 4 张均匀视角图，用预训练 **aesthetic predictor**（improved-aesthetic-predictor）打分，取 4 视图均分；低分者多为缺纹理/几何过简。阈值 Objaverse-XL=5.5、其余=4.5。

**Re-captioning**：用 **GPT-4o** 三段式标注——(1) 对渲染图产出超详细 `<raw_captions>`；(2) 蒸馏成 ≤40 词 `<detailed_captions>`；(3) 再总结成**长度递减的 10 个版本**（首条约 12 词、末条 ≤5 词）做训练增强。论文给出了完整 prompt（强调 avoid hallucination）。

**渲染设置**：VAE 训练每资产渲 **150** 张图（半径 2、FoV 40°、Blender 平滑面光，均匀球面分布）；图像条件生成模型另渲一套 **FoV 10°–70° 增强**的图作为 image prompt。数据增强对文本（不同长度摘要）和图像（不同 FoV）双向施加。

## 训练方法
**生成目标：rectified flow（CFM）。** 前向线性插值 `x(t)=(1−t)x₀+tε`，网络回归向量场，最小化条件流匹配损失 `L = E‖v_θ(x,t) − (ε−x₀)‖²`。消融证实 rectified flow 在两个 stage 均优于 DiT 扩散基线（Stage1 FD_dinov2 113.42 vs 132.71；Stage2 95.97 vs 100.88）。**时间步采样**：把 SD3 用的 logitNorm(0,1) 换成 **logitNorm(1,1)**，更适配本任务（Stage1 FD 269.56 vs 287.33）。CFG drop rate 0.1。

**VAE/decoder 训练目标**（多损失）：
- **Sparse-structure VAE**：当作二值分类，正负样本极不平衡（active voxel 稀疏），用 **Dice loss**。
- **D_GS**：`L_recon = L1 + 0.2(1−SSIM) + 0.2·LPIPS` + 体积正则 L_vol + 不透明度正则 L_α（防 Gaussian 退化/过大/过透明）；参考 Mip-Splatting 设最小 scale 9e-4、屏幕空间方差 0.1 抗锯齿。
- **D_RF**：与 GS 类似的渲染重建损失。
- **D_M**：`L_M = L_geo + 0.1·L_color + L_reg`，其中 L_geo 含 mask L1 + 10×Huber(深度) + 法线重建；L_reg 含一致性/FlexiCubes deviation/0.01×TSDF 三项稳定早期训练。

**优化超参**：AdamW，lr 1e-4，混合精度（配置文件均 fp16）。**XL 模型**：64×A100(40G) 训 **400K steps**、batch size 256。**推理**：CFG strength=3，sampling steps=50（仓库 minimal example 默认 12 步 + cfg 7.5/3 也可，约 10 秒出件）。

**未涉及**：无 SFT/RLHF/DPO/偏好对齐（纯生成式重建训练，3D 领域无人评奖励微调）；无步数蒸馏/consistency/LCM（论文与仓库均未报告加速蒸馏，靠原生 50 步采样）。

## Infra（训练 / 推理工程）
- **算力**：XL 在 **64× A100 40G**、batch 256、400K steps（总 GPU·时未披露）。仓库注明训练在 A100。
- **注意力后端**：默认 **flash-attn**，不支持的卡（如 V100）退 **xformers**（设 `ATTN_BACKEND=xformers`）。3D shifted-window attention 借现代 attention 实现处理变长窗口 token。
- **稀疏算子**：spconv（稀疏卷积）做 G_L 的下/上采样与 D_M 的分辨率提升；自研 **diffoctreerast**（CUDA 实时可微 octree 渲染器，由 diff-gaussian-rasterization 派生）渲染 radiance field；mesh 用 **nvdiffrast** + 改版 **FlexiCubes**（支持顶点属性）。
- **分布式**：train.py 支持多节点多卡（`--num_nodes/--node_rank/--master_addr/--master_port`），自动跨可见 GPU 分发。
- **部署/推理形态**：开源 pipeline `TrellisImageTo3DPipeline`，输出字典含 gaussian/radiance_field/mesh，可导出 .glb（烘焙 GS 外观到 mesh，texture 1024、simplify 0.95）与 .ply；提供 Gradio web demo 与 HF Space Live Demo。**单卡 ≥16GB**（A100/A6000 验证），约 **10 秒/件**。`SPCONV_ALGO=native` 可跳过 benchmark 提速。**未披露**：量化、KV cache、步数蒸馏等推理加速。

## 评测 benchmark（把效果讲清楚）
评测集 **Toys4k**（训练集外）。指标：FD/KD（特征提取器 Inception-v3 / DINOv2 / PointNet++）、CLIP score（prompt 对齐）。

**重建保真度（Tab.1，500 实例）**——SLAT vs 其他大规模 latent：
| 方法 | PSNR↑ | LPIPS↓ | CD↓ | F-score↑ | PSNR-N↑ | LPIPS-N↓ |
|---|---|---|---|---|---|---|
| LN3Diff | 26.44 | 0.076 | 0.0299 | 0.9649 | 27.10 | 0.094 |
| 3DTopia-XL | 25.34† | 0.074† | 0.0128 | 0.9939 | 31.87 | 0.080 |
| CLAY | – | – | 0.0124 | 0.9976 | 35.35 | 0.035 |
| **TRELLIS(SLAT)** | **32.74/32.19** | **0.025/0.029** | **0.0083** | **0.9999** | **36.11** | **0.024** |

SLAT 全面领先，几何上甚至超过专攻 shape 的 CLAY。

**生成质量（Tab.2，Toys4k）**——节选关键列：

Text-to-3D：CLIP↑ / FD_incep↓ / FD_dinov2↓
- Shap-E 25.04 / 37.93 / 497.17；InstantMesh 25.56 / 36.73 / 478.92；GaussianCube 24.91 / 27.35 / 460.07；
- **TRELLIS-L 26.60 / 20.54 / 238.60**；**TRELLIS-XL 26.70 / 20.48 / 237.48**（FD_dinov2 较最强基线降约一半）。

Image-to-3D：CLIP↑ / FD_incep↓ / FD_dinov2↓
- InstantMesh 84.43 / 20.22 / 264.36；LGM 83.97 / 26.31 / 322.71；3DTopia-XL 78.45† / 37.68 / 437.37；
- **TRELLIS-L 85.77 / 9.35 / 67.21**（FD_incep 约为次优的 1/2、FD_dinov2 约 1/4）。

**用户研究（104 人，2701 trials，68 文本 prompt + 67 图像 prompt，无 curation）**：
- Text-to-3D：**TRELLIS 67.1%**（905 选），次优 GaussianCube 10.3%、InstantMesh 9.1%；
- Image-to-3D：**TRELLIS 94.5%**（1277 选），次优 InstantMesh 2.2%。

**关键消融**：
- **SLAT 尺寸**（Tab.3）：32³ 通道从 16→64 提升有限（PSNR 31.64→31.85），切到 **64³×ch8** 显著跳到 PSNR 32.74 / LPIPS 0.0250，故选 64³。
- **rectified flow vs diffusion**（Tab.4）：任一 stage 换成 RF 都提升质量与对齐。
- **模型规模**（Tab.5）：B→L→XL 在训练分布与 Toys4k 上单调提升（Toys4k FD_dinov2 265.26→238.60→237.48，L→XL 收益渐平）。
- **时间步分布**（Tab.7）：logitNorm(1,1) 优于 (0,1)。
- 定性对比 commercial Rodin Gen-1（仅 image-to-3D）：TRELLIS 在复杂样例几何更细，且仅用开源数据训练。

## 创新点与影响
**核心贡献**：
1. **SLAT 统一结构化潜表示**——稀疏 voxel 结构（粗几何 + 高分辨率 + 局部性）与 DINOv2 稠密视觉特征（细外观/几何）融合，**一个 latent 解码到 GS/RF/Mesh 三格式**，且 fitting-free（无需逐资产对齐 3D 的昂贵 pre-fitting）。
2. **rectified flow transformer 用于 3D 大规模生成**的成功验证（把 SD3 的 RF + QK-Norm + logitNorm 范式迁到稀疏 3D，并定制稀疏注意力/打包）。
3. **两阶段（结构→latent）稀疏生成 pipeline** + 基于 Repaint 的 tuning-free **局部 3D 编辑**（删/增/替换区域）与 detail variation。
4. **TRELLIS-500K 数据集 + GPT-4o 多粒度 captioning + 美学过滤**全套开源工具链。

**影响**：作为 2024 末开源 3D 生成 SOTA（CVPR 2025 Highlight），SLAT 范式成为后续原生 3D 生成的重要参考；MIT 许可 + 全量开源（代码/模型/数据/训练代码，2025-03 追加放出训练代码与 TRELLIS-text 系列），被社区广泛二次开发（ComfyUI 插件、各类 image-to-3D 服务）。其"表示无关、稀疏结构 + 视觉基础模型特征"的思路推动了 3D latent 生成从碎片化表示走向统一范式。

**已知局限**（论文 §E）：
- 两阶段 pipeline 不如端到端高效；
- image-to-3D **不分离光照**，参考图的阴影/高光被烘进资产；改进方向是更强光照增强 + 预测 PBR 材质（留作 future work）；
- 文本条件模型因数据限制"创造力/细节弱于"图像条件版，官方推荐"文→图→3D"（先用 T2I 出图再走 image-to-3D）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2412.01506
- arxiv_pdf: https://arxiv.org/pdf/2412.01506
- github: https://github.com/microsoft/TRELLIS
- hf (image-large model card): https://huggingface.co/microsoft/TRELLIS-image-large （worklist 指向 JeffreyXiang/TRELLIS-image-large 镜像）
- project_page: https://microsoft.github.io/TRELLIS/
- hf demo (live): https://huggingface.co/spaces/Microsoft/TRELLIS

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2412.01506.pdf
- ../../../sources/omni/2024/trellis--readme.md
- ../../../sources/omni/2024/trellis--hf-card.md
- ../../../sources/omni/2024/trellis--project-page.md
