---
title: "Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material"
org: 腾讯混元 (Tencent Hunyuan)
country: China
date: "2025-06"
type: tech-report
category: 3d
tags: [image-to-3d, shape-generation, pbr-texture, flow-matching, dit, vae, multi-view-diffusion, open-source, tencent]
url: https://arxiv.org/abs/2506.15442
arxiv: https://arxiv.org/abs/2506.15442
pdf_url: https://arxiv.org/pdf/2506.15442
github_url: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
hf_url: https://huggingface.co/tencent/Hunyuan3D-2.1
modelscope_url: ""
project_url: https://3d-models.hunyuan.tencent.com/
downloaded: [arxiv-2506.15442.pdf, hunyuan3d-2-1--readme.md, hunyuan3d-2-1--hf-modelcard.md, hunyuan3d-2-1--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Hunyuan3D 2.1 是腾讯混元于 2025-06 开源的**生产级单图到带 PBR 材质 3D 资产生成系统**，把流程拆成"形状生成 + 纹理合成"两段：形状段用 mesh VAE（[[3dshape2vecset]] 向量集表征）+ 流匹配 DiT（Hunyuan3D-DiT，3.3B）出几何，纹理段用多视图 PBR diffusion（Hunyuan3D-Paint，2B）出 albedo/metallic/roughness 三套材质图。最大卖点是**首个完整开源权重 + 训练代码 + 数据处理流程的 PBR 纹理 3D 大模型**。最亮眼数字：形状 ULIP-I **0.1395**、Uni3D-I **0.3213** 全面领先 TripoSG / Trellis / Step1X-3D / Direct3D-S2；纹理 CLIP-FID **24.78**、LPIPS **0.1211**，显著优于自家上一代 Hunyuan3D-2.0（26.44 / 0.1261）。

## 背景与定位
2D 图像/视频生成已有 Stable Diffusion、[[hunyuan-video]]、[[wan]] 等繁荣开源生态，但 3D 生成长期碎片化、缺一个可扩展的开源 foundation。CLAY（SIGGRAPH 2024）首次验证 diffusion 做高质量 3D 生成可行，但权重/代码不开放。本作把自己定位为"**填补 3D 领域开源空白**"，并以"tutorial（手把手教程）"的姿态把数据处理、模型架构、训练策略、评测一次性讲透，让社区能直接微调/扩展。

技术脉络上它是 Hunyuan3D 系列的第三代：
- **Hunyuan3D 1.0**（2024-11，arXiv:2411.02293）：多视图扩散 + 重建的统一 text/image-to-3D 框架。
- **Hunyuan3D 2.0**（2025-01，arXiv:2501.12202）：把"形状 + 纹理"两段式做成 ShapeVAE + DiT + 多视图纹理 paint，但纹理是 **RGB**。
- **Hunyuan3D 2.1**（本作）：在 2.0 的两段式骨架上做两大升级——① **全开源**（首次放出全部权重 + 训练代码）；② 纹理从 RGB 升级为 **PBR 物理材质**（基于 Disney Principled BRDF，输出 albedo/metallic/roughness，可在引擎里量产做电影级光影）。

两段式（先几何后纹理）相比"大重建模型一次性出带色 mesh"更模块化：用户可只要无纹理白模、也可给自定义网格单独上纹理，对游戏/工业管线更友好。直接对标的同期工作：TripoSG、Trellis、Step1X-3D、Direct3D-S2、Craftsman 1.5、Michelangelo（形状），SyncMVD-IPA、TexGen、3DTopia-XL（纹理）。

## 模型架构
系统由两个独立可用的 foundation 组成。

### 形状段：Hunyuan3D-ShapeVAE + Hunyuan3D-DiT
**Hunyuan3D-ShapeVAE（mesh autoencoder）**——把多边形网格压成一段连续 token，沿用 [[3dshape2vecset]] 的"向量集（vector set）"表征，亦借鉴 Dora。
- **Encoder**：输入是从 mesh 表面采样的点云——**均匀采样点云 Pu** + **重要性采样点云 Pi**（两者各做 FPS 最远点采样得到 query 点 Qu/Qi）；点云用傅里叶位置编码 + 线性投影，经 cross-attention 与 self-attention 得到隐表征 Hs；再按 VAE 框架投影出隐空间的均值/方差，得到 latent shape embedding Zs。输入除 3D 坐标外还含**法向量**。
- **Decoder**：从 Zs 经线性投影 + self-attention，再用 point perceiver 模块查询一个 3D 网格 Qg，输出神经场 Fg，最后线性投影成 **SDF**，推理时用 marching cubes 转三角网格。
- **关键设计**：① **mesh 表面重要性采样**强化锐利边缘；② **可变 token 长度（variational token length）**——多分辨率训练，latent token 序列长度动态变化，**最大序列长度 3072**，以提升复杂几何细节。

**Hunyuan3D-DiT（流匹配扩散）**——在 ShapeVAE 隐空间上、以图像为条件预测 token 序列。
- **条件编码器**：用大图像编码器 **DINOv2 Giant**，输入分辨率 **518×518**；输入图先去背景、resize 居中、白底填充。
- **DiT block**：借鉴 [[hunyuan-dit]] 与 TripoSG，堆 **21 层 Transformer**；每层用**维度拼接（dimension concat）做 latent code 的 skip connection**；用 **cross-attention** 把图像条件注入 latent；额外加 **MoE 层**增强 latent 表征学习。架构图里 DiT 主干 21 层、VAE decoder 含 16× self-attention 后接 cross-attention 出 query points → 3D shape。
- **规模**：Shape 模型 **3.3B**（README 模型库标注）。

### 纹理段：Hunyuan3D-Paint（多视图 PBR diffusion）
建立在 Hunyuan3D-2 的多视图纹理架构上，把 RGB 升级为 **PBR 材质**，遵循 **Disney Principled BRDF**，同时输出 albedo / roughness / metallic 多视图材质图。
- **底座**：从 **Stable Diffusion 2.1 的 Zero-SNR checkpoint** 初始化，是 UNet 架构（非 DiT），规模 **2B**（README）。
- **条件注入**：保留 ReferenceNet 的参考图特征注入；同时把**几何渲染的法线图 + CCM（canonical coordinate map，标准坐标图）与 latent noise 拼接**作为几何条件。
- **Spatial-Aligned Multi-Attention（空间对齐多注意力）**：用预训练 VAE 压多通道材质图，跑一个**并行双分支 UNet**（albedo 分支 + MR 即 metallic-roughness 分支）。每分支都有 self-attention / multi-view attention / reference attention 三种并行注意力；为了对齐 albedo 与 MR 的物理关系与空间，**直接把 albedo 的 reference-attention 输出传播给 MR 分支共享**。
- **3D-Aware RoPE（来自 RomanTex）**：在多视图 attention 里注入 3D 空间信息——对 3D 坐标体下采样，构造与 UNet 各层级对齐的多分辨率 3D 坐标编码，加性融合进 hidden state，把跨视图交互拉到 3D 空间里，**消除接缝与重影、提升跨视图一致性**。
- **分辨率/视图**：默认 **6 视图、512×512**（README 默认配置 max_num_view=6, resolution=512）。

## 数据
**形状生成数据**：收集 **100K+** 带纹理与无纹理 3D 数据，公开集主要来自 **ShapeNet / ModelNet40 / Thingi10K / Objaverse(-XL)**，外加自有自定义数据。预处理流程（论文 Algorithm 1）：
- **归一化**：算轴对齐包围盒，统一缩放到原点为中心的单位立方体（保持长宽比）；点云做中心化 + 按最大欧氏距离归一。
- **Watertight 封闭化**：用 IGL 库从缺陷几何构建 **SDF**，以广义缠绕数（generalized winding number，ω>0.5 判内部）判内外符号，零等值面 marching cubes 抽出无边界破洞的封闭网格。
- **SDF 采样**：query 点分两种——贴近表面 + [−1,1]³ 均匀分布；贴面点抓细节、均匀点抓整体结构。算法里 **N_near = N_uniform = 249,856** 点。
- **表面采样**：50% 均匀 + 50% 在高曲率特征处重要性采样（按局部曲率自适应密度），保证锐边/角充分表征；**N = 124,928** 点（random + sharp 各一套）。
- **条件渲染**：用 **Hammersley 序列**在球面均匀采 **150 个相机**（带随机偏移 δ），FoV 随机 **U(10°,70°)**，相机半径在 **[1.51, 9.94]** 间调整以保持取景一致。

**纹理合成数据**：从 Objaverse / Objaverse-XL 经**严格人工标注高质量筛选**得 **70K+** 条（论文 §2.3 措辞为 Objaverse + Objaverse-XL；§2.1 仅写 Objaverse-XL，两处略有不一致）。每个物体在 4 个仰角（−20°、0°、20°、一个随机角）下、每个仰角取 **24 个方位均匀视图**，渲染对应 **albedo / metallic / roughness 图 + HDR/点光源图，分辨率 512×512**。参考图按概率渲染：随机视点（仰角 [−30°, 70°]）；光照随机——点光源 p=0.3 或 HDR 环境贴图 p=0.7。

数据配比/清洗的更细致权重（如各公开集占比、人工标注标准的具体规则）**未进一步披露**。

## 训练方法
**形状 ShapeVAE**：两个损失监督——① 重建损失，预测 SDF 与 GT SDF 的 **MSE**；② **KL 散度损失** L_KL 让隐空间紧致连续。总损失 Lr = E[MSE(Ds(x|Zs), SDF(x))] + γ·L_KL（γ 为 KL 权重）。用**多分辨率训练**：latent token 序列长度动态变化，最大 3072。

**形状 DiT**：训练目标是**流匹配（flow matching）**。用仿射路径 + conditional optimal transport schedule：xt=(1−t)·x0 + t·x1，速度场 ut=x1−x0；损失 L = E[‖uθ(xt,c,t) − ut‖²₂]，t∼U(0,1)，c 为条件（图像）。推理时随机采起点，用**一阶 Euler ODE solver** 解出 x1。

**纹理 Paint**：
- 从 **SD2.1 Zero-SNR checkpoint** 初始化，**AdamW**，学习率 **5×10⁻⁵**，**2000 步 warm-up**。
- **Illumination-Invariant 光照不变训练策略（来自 MaterialMVP）**：核心直觉是同一物体在不同光照下渲染结果不同，但其**内在材质属性应一致**。于是用同一物体在不同光照下渲染的两套参考图，计算**一致性损失**，从而产出去光照/去阴影的"光照无关 albedo"和准确的 MR 图。

蒸馏/步数加速（consistency/LCM/ADD 等）在报告中**未提及**。整体仍是标准 flow-matching（形状）+ diffusion（纹理）训练，未报告 SFT/RLHF/DPO/偏好对齐等后训练阶段。

## Infra（训练 / 推理工程）
- **纹理 Paint 训练算力**：报告明确给出**约 180 GPU-days**（未说明具体 GPU 型号与卡数）。
- **形状 Shape 训练算力**：**未披露** GPU·时/卡数/并行策略。
- **并行/混合精度/吞吐**：**未报告**（论文以 tutorial 口吻讲方法，未给分布式工程细节）。
- **推理显存（部署形态，来自 README）**：形状生成 **10 GB VRAM**、纹理生成 **21 GB**、形状+纹理合计 **29 GB**；提供 `--low_vram_mode` 低显存模式。支持 macOS / Windows / Linux，给出 diffusers 风格 API 与 Gradio App；测试环境 Python 3.10 + PyTorch 2.5.1+cu124。
- **加速依赖**：纹理管线用到 custom_rasterizer、DifferentiableRenderer、Real-ESRGAN x4 超分（README 安装步骤）。
- **推理步数/缓存/量化**：报告**未给具体扩散步数与量化方案**。

## 评测 benchmark（把效果讲清楚）
评测分三块：形状生成、纹理合成、端到端整图。

### 形状生成（Table 1，论文）
用 **ULIP** 与 **Uni3D** 度量"生成网格 ↔ 输入图/文本"相似度：从生成网格采 8,192 表面点作点云模态，文本取自 VLM 给的图像 caption。ULIP-T/Uni3D-T 是点云-文本相似度，ULIP-I/Uni3D-I 是点云-图像相似度（越高越好）：

| Model | ULIP-T ↑ | ULIP-I ↑ | Uni3D-T ↑ | Uni3D-I ↑ |
|---|---|---|---|---|
| Michelangelo | 0.0752 | 0.1152 | 0.2133 | 0.2611 |
| Craftsman 1.5 | 0.0745 | 0.1296 | 0.2375 | 0.2987 |
| TripoSG | 0.0767 | 0.1225 | 0.2506 | 0.3129 |
| Step1X-3D | 0.0735 | 0.1183 | 0.2554 | 0.3195 |
| Trellis | 0.0769 | 0.1267 | 0.2496 | 0.3116 |
| Direct3D-S2 | 0.0706 | 0.1134 | 0.2346 | 0.2930 |
| **Hunyuan3D-DiT** | **0.0774** | **0.1395** | **0.2556** | **0.3213** |

（论文 Table 1 该行记作 Hunyuan3D-DiT；GitHub README 同表记作 Hunyuan3D-Shape-2.1，数字一致。）

Hunyuan3D-DiT 在四项指标上**全部第一**，ULIP-I（0.1395）相对次优 Craftsman（0.1296）领先明显；定性上能准确捕捉不倒翁细节、计算器按键数、耙齿数、战斗机结构，并产出可直接用于下游的 watertight 网格。

### 纹理合成（Table 2，论文）
用 **CLIP-FID / CMMD / CLIP-I / LPIPS** 度量生成纹理与 GT 的相似度（给定无纹理形状 + 单图）：

| Method | CLIP-FID ↓ | CMMD ↓ | CLIP-I ↑ | LPIPS ↓ |
|---|---|---|---|---|
| SyncMVD-IPA | 28.39 | 2.397 | 0.8823 | 0.1423 |
| TexGen | 28.24 | 2.448 | 0.8818 | 0.1331 |
| Hunyuan3D-2.0 | 26.44 | 2.318 | 0.8893 | 0.1261 |
| **Hunyuan3D-Paint** | **24.78** | **2.191** | **0.9207** | **0.1211** |

Hunyuan3D-Paint **四项全优**，相对自家上一代 Hunyuan3D-2.0 在所有指标上均改善（CLIP-FID 26.44→24.78、CLIP-I 0.8893→0.9207）。
> 注：GitHub README 给出的纹理表与论文 Table 2 一致（CLIP-FiD/CMMD/CLIP-I/LPIPS 数字相同）。

### 端到端 image-to-3D
与开源 Step1X-3D、3DTopia-XL，及两个匿名商业模型（Model 1 / Model 2）做**定性对比**（论文 Fig.6/Fig.7），结论是本作 PBR 材质保真度最高，且对低质量几何更鲁棒，端到端效果更好。**此块为定性可视化对比，论文未给端到端定量分数/人评 ELO**。

**消融**：报告未列独立的消融实验表；3D-Aware RoPE、spatial-aligned multi-attention、illumination-invariant 训练这三项创新的单独增益**未单独量化**（相关消融在其引用的 MaterialMVP / RomanTex 原文中）。

## 创新点与影响
**核心贡献**：
1. **首个完整开源的生产级 PBR-纹理 3D 生成系统**——同时放出全部模型权重 + 训练代码 + 数据处理流程，把此前 CLAY/商业方案封闭的能力开放给社区，可直接微调下游。
2. **PBR 材质合成管线**——遵循 Disney Principled BRDF，输出 albedo/metallic/roughness，做到金属反光、次表面散射等物理光影，满足游戏/工业级量产精度（取代 2.0 的 RGB 纹理）。
3. **纹理三连技术**：spatial-aligned multi-attention（albedo↔MR 对齐）、3D-Aware RoPE（跨视图一致、消接缝）、illumination-invariant 训练（产出去光照 albedo）。
4. **形状 ShapeVAE 的可变 token 长度 + 重要性采样**，兼顾锐边与复杂细节。

**影响**：作为 2025 年开源 3D 的代表作，提供了可复现基线，催生大量社区生态（ComfyUI 插件、Unity XR 支持等），并被同月发布的 HunyuanWorld-1.0（沉浸式 3D 世界生成）等后续工作延续；官方网站后续还推出"混元3D Omni"等迭代。

**已知局限**：
- 两段式（先几何后纹理）非端到端，几何误差会传导到纹理。
- 形状段训练算力、分布式工程细节、形状/纹理三项创新的独立消融**均未在本报告披露**。
- 纹理 paint 仍是 SD2.1-UNet 底座（非 DiT），分辨率受限于 512×512、6 视图。
- 推理需 ~29 GB 显存做完整流程，对消费级硬件门槛偏高（虽有 low_vram 模式）。
- 报告以 tutorial 形式写作，正文偏方法讲解，端到端定量/人评较薄。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.15442
- arxiv_pdf: https://arxiv.org/pdf/2506.15442
- github: https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1
- hf: https://huggingface.co/tencent/Hunyuan3D-2.1
- project_page: https://3d-models.hunyuan.tencent.com/
- official_site: https://3d.hunyuan.tencent.com

## 一手源存档（sources/）
- [arxiv-2506.15442.pdf](https://arxiv.org/pdf/2506.15442)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuan3d-2-1--readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuan3d-2-1--hf-modelcard.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/hunyuan3d-2-1--project-page.md)
