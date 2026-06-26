---
title: "Seed3D 2.0: Advancing High-Fidelity Simulation-Ready 3D Content Generation"
org: "ByteDance Seed"
country: China
date: "2026-04"
type: tech-report
category: 3d
tags: [3d-generation, image-to-3d, pbr, vecset, rectified-flow, dit, moe, vae, articulation, scene-generation, simulation-ready, bytedance]
url: "https://seed.bytedance.com/en/seed3d_2_0"
arxiv: "https://arxiv.org/abs/2605.13862"
pdf_url: "https://arxiv.org/pdf/2605.13862"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://seed.bytedance.com/seed3d_2_0"
downloaded: [seed3d-2-0.pdf, seed3d-2-0--blog.md, seed3d-2-0--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Seed3D 2.0 是字节 ByteDance Seed 的新一代「单图→高保真、可仿真就绪（simulation-ready）3D 资产」基础模型：几何用 **coarse-to-fine 两段式 DiT + locality-aware VAE**，纹理用 **统一 PBR + MoE + VLM 先验**取代级联管线，再补上场景布局/部件分解/免训练关节化（articulation）三件套；在对 5 个商用模型（Hunyuan3D-2.5/3.1、Tripo 3.0、Rodin Gen2、HiTem v2.0）的人评盲测中，端到端带纹理资产生成胜率 **69.0%–89.9%**。

## 背景与定位
高质量 3D 资产在 XR 内容、3D 打印、机器人仿真、具身 AI、工业制造中需求激增，但既有方法（含字节自家 Seed3D 1.0）仍达不到「production-grade」。报告把 1.0 的不足归结为两个 gap：

- **质量 gap**：生产环境要求几何规整（sharp edges、薄壁、结构一致的曲面）+ 在不同光照下视觉一致的 PBR 材质；1.0 形状「貌似合理」但精细标准上持续不及格。
- **能力 gap**：静态整体网格不够用，下游需要多物体连贯场景、可功能分解的物体、支持部件级物理交互的资产；1.0 场景能力有限、无部件分解/关节化。

技术脉络上，几何分支沿用 **VecSet（3DShape2VecSet / Dora / TripoSG / Hunyuan3D 一系）** 范式 + [[rectified-flow]] / [[flow-matching]]；纹理分支沿用 1.0 的 MMDiT 双流。直接对标对象是同期商用闭源 3D 生成（[[hunyuan3d-2-1]]、Tripo、Rodin、HiTem）。产品形态为火山引擎（Volcano Engine）API，Model ID `doubao-seed3d-2-0-260328`，发布于 2026-04-23（arXiv 2605.13862，2026-04-22）。

## 模型架构
整体推理是多阶段串行管线：**几何生成 → 纹理合成 → UV 纹理补全**（继承 1.0）。

### 几何：Seed3D-VAE + Seed3D-DiT（VecSet 范式）
- **Seed3D-VAE**：双分支 perceiver 式 encoder–decoder，把连续 3D 几何压成紧凑 VecSet（一组 latent token）。
  - encoder 输入「表面点云 + 位置/法向/sharp-edge 采样」，映射成同时编码全局拓扑与细粒度结构的 latent token。
  - decoder 通过对 spatial query 点的 cross-attention 重建连续 **SDF（Signed Distance Field）**，最终用 **Dual Marching Cubes (DMC)** 抽 mesh。
  - **locality-aware latent aggregation**：利用 VecSet「同一空间邻域内 token 编码冗余信息」的性质，编码时跨邻域合并 token，把表示能力集中到几何复杂区域 → 比 1.0 VAE 用更少 token 取得更高重建质量。
  - 解码侧把 SDF query 对「全部 latent token」的 dense attention 换成 **content-adaptive sparse routing**（每个 query 只 attend 一个紧凑、空间连贯的 token 子集），显著降低解码延迟而保真度不掉。
- **Seed3D-DiT**：基于 [[rectified-flow]] 的扩散 transformer，建模「高斯噪声 → 结构化 latent」，并拆成 coarse-to-fine 两段（见下「训练方法」）。
  - Stage 1 用「放大版（scaled-up）的 Seed3D 1.0 DiT backbone」直接从图像条件生成粗 latent。
  - Stage 2 以 Stage 1 输出为几何锚点做细化，注入两类先验：① **Coarse Shape Prior**（Stage 1 latent 部分加噪后并入 Stage 2 扩散，作粗几何参考）；② **Voxelized Positional Encoding**（Stage 1 粗几何体素化得到的空间坐标，作为位置编码注入，把每个 latent token 锚到空间位置，促进结构规整）。

### 纹理：统一 PBR MMDiT + MoE + VLM 条件
- 把 1.0 的级联管线（Seed3D-MV 多视 RGB 合成 + Seed3D-PBR 材质估计）合并为 **一个统一 PBR 生成模型**，直接从「参考图 + 3D 几何」生成多视 **albedo** 与 **metallic-roughness (MR)** 贴图，消除中间多视 RGB 合成步骤与误差累积。
- 保留 1.0 的 **MMDiT 双流架构**，在共享 DiT block 内用 **modality-specific projection layer** 联合建模 albedo 与 MR。
- **MoE 扩展**：直接堆 dense 网络做高分辨率代价过高，故用稀疏专家路由（Mixture-of-Experts）扩容量、控激活算力 → 提升 albedo 质量、文字/图案等细粒度特征保真、MR 边界更干净。
- **VLM 语义条件**：未知光照下 PBR 估计是病态问题（同一外观可由不同光照×材质组合产生，常见失败为光照被错误烘进 albedo、非金属高光被误判为金属等）。引入 VLM 生成「材质类型/表面特性/物理属性」描述，编码成 conditioning token 注入 DiT block，与几何、参考图条件一起提供语义 grounding，稳定材质生成。

### Simulation-Ready 模型套件（场景→部件→关节）
- **Scene Layout Planning**：从文/图/视频预测空间一致的物体布局并合成连贯 3D 场景。视觉输入（尤其单段视频）用深度估计恢复场景几何 + 逐帧检测/分割得实例掩码 + VLM 生成每实例文本描述 + image inpainting 补遮挡，再过几何/纹理模型生成 mesh 并与深度图对齐定位与尺度；文本输入则 **微调一个 LLM 做空间推理**生成布局与逐物体描述。
- **Part-level Generation（perception-then-generation）**：
  - **Seed3D-PartSeg**（部件分割）：native 3D backbone（Point Transformer V3 / Sonata 类）从 mesh 表面采样提特征，分割头在稀疏点 prompt 条件下产 part mask，经 NMS 过滤后投影到 mesh 面并传播到未标注区域得完整表面分割。
  - **Seed3D-PartDiT**（部件补全）：[[rectified-flow]] 扩散，条件 = 「Seed3D-VAE 全局 shape latent（结构上下文）+ PartSeg 偏点云（空间引导）+ 输入图（外观）」；改造的 attention 同时强制 inter-part / intra-part 交互，全局 shape feature 还注入每个 DiT block 保部件间几何一致；各 part latent 经 VAE decoder 解码组装成 part-composited mesh。
- **Articulated Asset Generation（training-free）**：结合三类先验——VLM 语义先验、分解 mesh 几何先验、image-to-video 动态先验。流程：VLM 在渲染视图上把部件组织成运动学一致的部件并判定关节类型；按部件几何用预定义几何算子生成关节轴候选池，再让 VLM 选最合理者；运动范围用 **image-to-video 模型作运动先验**合成短片，再用 differentiable rendering 对生成运动序列拟合关节范围；连同 VLM 估计的质量/摩擦等物理属性导出为 **URDF**，可进 Isaac Sim 等物理引擎。

> 参数量未披露（报告仅说 Stage 1 用「放大版 1.0 DiT」、纹理用 MoE）；分辨率策略见下文。

## 数据
报告给出**六阶段数据预处理管线**（保证训练集质量与多样性），但未披露资产总量级数字：

1. **Format Canonicalization & Cleansing**：原始资产统一为「mesh 几何 + 多通道 PBR 纹理」；几何净化去除「pseudo-3D」广告牌伪影与多余结构（如底座 pedestal）；纹理校验剔除 UV 损坏/缺纹理通道的资产。
2. **Category-Specific Visual Deduplication**：对多视渲染的 2D 特征用**类别相关动态阈值**去重，避免在视觉同质类别上过滤过度，同时激进剔近重复。
3. **Advanced VLM Scoring & Captioning**：微调 VLM 从语义/结构/感知**六个维度**给每个资产打分（再用强 LLM 做 arbiter 仲裁），并生成标准化文本 caption；这些多维标签 + caption 既做下游 curation 依据，也做模型条件的语义先验。
4. **Asset Curation & Refinement**：分流为**预训练子集**与 **SFT 子集**；用 VLM tag 过滤低质并做定向 refinement（canonical orientation 对齐统一物体朝向、instance disentanglement 拆歧义多物体）；SFT 子集额外做细粒度**人工**几何/纹理验证。
5. **Sharpness-Preserved Watertight Remeshing**：curated mesh 转 DMC-compliant watertight 表示（全 GPU 加速）；不用常规 L2 距离最小化，而用 **inspired by L∞** 的保锐度公式以保 dihedral angle 与边缘不连续性；优化的 CUDA 管线 **15 秒内**完成 **1024³** 分辨率重建（多部件资产逐 part 独立 remesh）。
6. **Condition Rendering**：沿均匀相机轨迹生成 view-consistent 几何渲染 + albedo/roughness/metallic 多通道 PBR 纹理渲染，作为扩散条件信号。

> 数据来源/总规模/图文对数量/安全过滤细节均**未披露**（report 只给流程，不给数字）。

## 训练方法
统一目标为 [[rectified-flow]] / [[flow-matching]] 框架（report 引 Flow Matching, Lipman 2022 与 rectified flow），多阶段渐进训练 + 推理蒸馏。

### 几何（Seed3D-DiT 分层渐进）
- **Stage 1 Foundational Training（三相）**：
  - **Pre-Training (PT)**：从零训，base 分辨率 **256 latent token + 256 图像分辨率**，学 3D 形状基础分布与初步跨模态对齐。
  - **Continued Training (CT)**：latent 序列长度逐步升到 **4096**、图像分辨率升到 **512**，学更精细几何与更锐边缘。
  - **SFT**：在高质 curated 子集上降学习率微调，去表面扰动、改善整体拓扑。
- **Stage 2 Precision Refinement Training**：
  - **Init**：从 Stage 1 checkpoint 初始化，继承结构知识。
  - **CT with Regularization**：引入 Voxelized Positional Encoding（空间约束）+ partially diffused Stage 1 latent（粗几何锚）做细节恢复的 CT。
  - **Advanced SFT**：在精挑高质样本上微调，提锐度、几何规整性与对参考图的保真。

### 纹理（Seed3D-PBR 两段渐进）
- **Pre-Training**：MoE 统一 PBR 模型在大规模数据上学「多视 albedo + MR 生成（条件=参考图+3D 几何）」的基础能力，最大化覆盖多样 albedo 外观、MR 类别与光照。
- **SFT**：在精选高质子集降学习率微调，**此阶段才引入 VLM 生成的材质描述**作为额外条件——把 VLM 集成推迟到 SFT，让模型先在 PT 巩固通用纹理生成能力，再专攻复杂光照下的歧义材质分解。

### 推理加速：两段式渐进蒸馏（progressive distillation）
对几何与纹理的**全部 DiT**统一蒸馏：
- **Stage 1：蒸 CFG**——训 student 单次前向预测 CFG-combined 输出，每步算力减半同时保留引导采样的质量收益。
- **Stage 2：progressive step distillation**（按 Salimans & Ho 2022 的 curriculum）——每轮把采样步数减半，student 学在 1 步匹配 teacher 的 2 步输出；分级压缩避免单段激进蒸馏的训练不稳，更忠实逼近原轨迹。
- 蒸馏后模型在**视觉保真、多视一致性、参考图对齐**三维上与 full-step CFG 模型相当。

> 算力规模 / GPU-时 / 并行策略 / 混合精度 / 具体超参均**未披露**。

## Infra（训练 / 推理工程）
report 侧重算法与推理管线工程，集群级 infra（GPU 数、训练时长、分布式/并行/精度）**未披露**。已披露的推理工程：

- **几何推理**：Stage 1 DiT 出粗 VecSet latent → 在稀疏 **512³** grid 上 DMC 解出中间 mesh → 该粗 mesh 重新 VAE-encode 成 latent，并行做 GPU 加速体素化 + 形态学膨胀产空间占据先验 → 两信号条件化 Stage 2 做高分辨率生成；为支持**最高 1536³** 抽取，用 hierarchical 策略借 Stage 1 占据先验 + 多尺度过滤渐进剪 query 点，并在 cross-attention SDF query 里做 spatially-aware grouping 提效；最后用 GPU 加速 **QEM decimation** 简化到目标面数 + UV 展开。
- **纹理推理**：在 1.0 基础上做 **parallelized model execution** + 优化后处理算子，降端到端延迟而保质。
- **数据侧 infra**：remeshing 全 GPU 加速 CUDA 管线，1024³ 重建 < 15 秒。
- **部署形态**：火山引擎（Volcano Engine）API，模型 ID `doubao-seed3d-2-0-260328`，「方舟体验中心 → Vision Model → 3D Generation → Doubao-Seed3D-2.0」。

> 具体推理步数（蒸馏后步数）、量化、单资产端到端时延数字**未报告**。

## 评测 benchmark（把效果讲清楚）
评测为**人评盲测 user study**（report 未给 FID/Chamfer/F-score 等自动指标）：招募 **60 名有 3D 建模背景的评估者**，每个对比随机分配 **15 人**评估 **200+ 图像 prompt**，逐对判「更好 / 相当 / 更差」。对比 5 个近期商用模型 + Seed3D 1.0，分**仅形状（shape-only）**与**端到端带纹理资产**两组（数字来自 report Fig.1 与正文，及 blog）：

**形状（shape-only）Seed3D 2.0 胜率（Better）**：
- vs Hunyuan3D-2.5：**65.1%**
- vs Hunyuan3D-3.1：**55.2%**（最接近）
- vs Tripo 3.0：**92.8%**
- vs Rodin Gen2 v1.9：**89.6%**
- vs HiTem v2.0：**79.2%**
- vs Seed3D 1.0：**98.3%**（近乎全胜，印证 coarse-to-fine 两段 DiT + locality-aware VAE 的几何提升）

**端到端带纹理资产 Seed3D 2.0 胜率（Fig.1 全部六项）**：
- vs Hunyuan3D-2.5：**81.2%**
- vs Hunyuan3D-3.1：**69.0%**（最接近，即 report/blog 所称区间下界「69.0% 起」）
- vs Tripo 3.0：**81.1%**
- vs Rodin Gen2 v1.9：**89.9%**（区间上界）
- vs HiTem v2.0：**84.7%**
- vs Seed3D 1.0：**87.3%**

> 综合区间：端到端带纹理资产对**五个商用基线**胜率 **69.0%–89.9%**（report 正文与 abstract 均明示此区间端点为 vs Hunyuan3D-3.1 / vs Rodin Gen2 v1.9）。"comparable（相当）"判定占比一直很小 → 质量差异对人评普遍可感知。定性对比（Fig.6 形状 / Fig.7 纹理）显示 2.0 在复杂几何细边、薄壁、对输入图保真、纹理分解准确性与**文字渲染**上明显优于 Hunyuan3D-3.1 / Tripo 3.0 / Rodin v1.9。**消融**：report 未给数字化 ablation 表，仅以「对 Seed3D 1.0 的 98.3% 形状胜率」与「蒸馏后三维度持平」作为架构与蒸馏有效性的证据。

> 注：自动量化指标（FID/CLIP/Chamfer/F-score/Volume IoU 等）在本 report 中**未报告**。

## 创新点与影响
**核心贡献**：
1. **几何 coarse-to-fine 两段式 DiT**：把「全局结构」与「高频细节」解耦分别优化，配 Coarse Shape Prior + Voxelized PE 两先验，攻克 sharp edge / 薄壁 / 复杂拓扑。
2. **locality-aware VAE**：邻域 token 聚合 + content-adaptive sparse routing，更少 token 更高重建质量 + 更快解码。
3. **统一 PBR 生成模型**：取代级联 RGB→材质管线，直接出多视 albedo + MR，消除误差累积；MoE 扩容上分辨率、VLM 先验稳定病态材质分解。
4. **simulation-ready 套件**：scene layout planning（文/图/视频→布局）、Seed3D-PartSeg+PartDiT 部件分解补全、**training-free articulation**（VLM+几何+I2V 三先验→URDF），把生成 3D 接入 Isaac Sim 等物理引擎做部件级交互。
5. **两段式渐进蒸馏**（CFG 蒸馏 + 渐进步数蒸馏）支撑生产级部署。

**影响**：把 3D 生成从「单个静态资产」推进到「可仿真、可分解、可关节化、可组场景」，直接服务具身 AI / 机器人仿真 / XR / 工业制造；是字节 Seed「世界模型」路线（Jianfeng Zhang 主导）在 3D 资产层的落地。

**已知局限（report/blog 自述）**：几何细节精度与泛化仍有提升空间；纹理仍易出现遮挡与贴图错误；大规模部署受推理效率约束；真实世界用例覆盖仍是前沿。

## 原始链接
- project_page: https://seed.bytedance.com/en/seed3d_2_0
- tech_blog: https://seed.bytedance.com/en/blog/seed3d-2-0-released-higher-precision-and-greater-usability
- tech_report (arXiv abs): https://arxiv.org/abs/2605.13862
- tech_report (PDF, arXiv): https://arxiv.org/pdf/2605.13862
- tech_report (PDF, 官方 CDN): https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/pdf/Seed3D_v2.pdf
- product (Volcano Engine): https://exp.volcengine.com/ark/vision?mode=vision&modelId=doubao-seed3d-2-0-260328&tab=Gen3D
- 前置工作 Seed3D 1.0 (arXiv): https://arxiv.org/abs/2510.19944

## 一手源存档（sources/）
- seed3d-2-0.pdf（官方技术报告 PDF，= arXiv 2605.13862，18 页：正文 14 页 + 参考文献/贡献者，已精读）  （PDF 不入 git，走 HF bucket）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/seed3d-2-0--blog.md)（官方技术博客快照）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/seed3d-2-0--project-page.md)（官方项目页快照）
