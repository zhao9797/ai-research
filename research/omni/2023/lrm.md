---
title: "LRM: Large Reconstruction Model for Single Image to 3D"
org: "Adobe Research / Australian National University"
country: US
date: "2023-11"
type: paper
category: 3d
tags: [3d-reconstruction, single-image-to-3d, triplane, nerf, transformer, feed-forward, objaverse]
url: "https://arxiv.org/abs/2311.04400"
arxiv: "https://arxiv.org/abs/2311.04400"
pdf_url: "https://arxiv.org/pdf/2311.04400"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://yiconghong.me/LRM/ (域名已过期被停放，原页失效)"
downloaded: [arxiv-2311.04400.pdf, openlrm--readme.md, lrm--project-page.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
LRM 是**第一个大规模前馈式（feed-forward）单图到 3D 重建模型**：用一个 5 亿参数的纯 Transformer 编解码器，把单张图片直接回归成 triplane-NeRF，**单卡 A100 5 秒出 3D mesh**，无需逐物体优化。在 GSO 100 物体评测上 FID 31.44 / PSNR 19.60 / Chamfer 0.053，全面碾压同期 Point-E、Shap-E、One-2-3-45。它开创了"用大数据+大模型学通用 3D 先验、像 GPT 一样把 3D 重建当回归任务"的 feed-forward 3D 范式。

## 背景与定位
单图到 3D 是工业设计、游戏、AR/VR 的长期目标，难点在于单视角下 3D 几何天然存在歧义。此前主流路线有两类，都很慢或泛化差：

1. **逐物体优化 / 蒸馏路线**：以 [[dreamfusion]]、[[magic3d]] 为代表的 SDS（Score Distillation Sampling），用预训练 2D 扩散模型监督逐物体优化一个 NeRF，质量受 2D 模型上限约束、需精细调参，且每个物体要优化数十分钟。
2. **多视图生成 + 重建路线**：Zero-1-to-3 / One-2-3-45 先用扩散模型生成多视图再重建，结果受生成一致性限制、细节偏糊。
3. **小规模类别专属重建**：早期用 point cloud / voxel / mesh / SDF / occupancy 在 ShapeNet 等小数据上按类别训练，只在特定类别表现好。

LRM 的洞见来自 NLP/CV 大模型成功的三要素——**可扩展的 Transformer + 海量数据 + 简单自监督式目标**。作者直接发问："给足够 3D 数据和大规模训练框架，能否学到一个通用 3D 先验，从单图重建任意物体?" 答案就是 LRM：**把 3D 当作一种新模态**，用大 Transformer 把 2D 图像特征通过 cross-attention 直接"接地"到 3D triplane，纯靠在新视图上的图像重建损失端到端训练，**不需要任何 3D 感知正则或精细超参调节**。

与同期大规模工作 [[point-e]]、Shap-E 的关键区别：Point-E/Shap-E 用非结构化点云表征（4K/16K 点作 token），LRM 用**结构化、与世界坐标对齐的 triplane**（仅 3×32×32=3072 token），天然便于 2D→3D 投影，且把 token 复杂度从体素的 O(N³) 降到 O(N²)。这是 LRM 能"数据高效地 scale"的核心。

> 注：LRM 是 ICLR 2024 接收工作。**Adobe 官方从未开源代码与权重**；社区开源复现 OpenLRM（3DTopia / 上海 AI Lab，Apache-2.0，权重 CC-BY-NC）是事实上的可用实现，本页架构超参也与 OpenLRM 的 small/base/large 配置交叉印证。原项目页 yiconghong.me/LRM 域名已过期被 GoDaddy 停放，**未能获取原 project page 内容**，相关结论均来自论文正文/附录与 OpenLRM。

## 模型架构
LRM 是一个**全 Transformer 的可微编解码框架**（论文 Fig.1），三段式：

**1) 图像编码器（image encoder）**
- backbone：预训练 **DINO（ViT-B/16）**，输入 512×512 RGB，输出 **1025 个 token**（1024 个 patch token + 1 个 [CLS]），维度 d_E=768。
- 选 DINO 而非 ImageNet-ResNet / CLIP，因 DINO 自蒸馏学到的注意力更关注结构与纹理细节，正是重建几何/颜色所需。**整条 patch 序列都用上**（不只 [CLS]）。
- （OpenLRM v1.1 实际改用 DINOv2 作 encoder。）

**2) 图像到 triplane 解码器（image-to-triplane decoder）**——核心创新
- 16 层 Transformer decoder，隐维 d_D=1024。
- 维护一组**可学习的空间位置 embedding** f_init，形状 (3×32×32)×1024，作为 query。
- 每层结构：`cross-attention（query=triplane hidden，K/V=图像特征 h_i）→ self-attention（triplane token 之间）→ MLP`，全部残差连接。
  - cross-attention 把图像信息链接到 triplane，**不预设任何 2D↔3D 空间对齐**，让模型自己学 2D→3D 对应（把 3D 当独立模态）。
  - self-attention 建模 triplane 内部空间结构关系。
- **相机调制（camera modulation）**：相机特征 c∈R²⁰（4×4 外参矩阵 flatten=16 维 + 焦距 foc_x,foc_y + 主点 pp_x,pp_y），经 MLP 升维成 c̃；借鉴 [[dit-scalable-diffusion-transformers]]（DiT）的 adaLN，对每个 attention 子层做 **ModLN**（`LN(f)·(1+γ)+β`，γ/β 由 MLP_mod(c̃) 产生）。相机控制整体朝向/畸变，图像特征负责细粒度几何/颜色——两类条件分工。
- 设计接近 Perceiver，但**全程保持高维表征**，不像 Perceiver 压到 latent 瓶颈。
- 输出 f_out 经一个可学习反卷积上采样 + reshape，得到最终 triplane。

**3) Triplane-NeRF + 体渲染**
- triplane 表征沿用 **EG3D**（Chan et al. 2022）：三个轴对齐特征面 T_XY/T_YZ/T_XZ，每面 **64×64×80**（dT=80）。
- 任意 3D 点（NeRF bbox [-1,1]³）投影到三面，双线性插值取特征拼接（3×80），送入 **MLP_nerf（10 层，隐维 64，ReLU）** 输出 RGB+密度 σ（4 维）。
- 体渲染（标准 NeRF 积分，可微）：每条 ray 均匀采 **128 点**，训练时渲 **128×128** 图像监督。

**参数量**：>5 亿（500M）可学习参数。OpenLRM 三档与之印证：small（12 层/dim 512/trip 32/224 输入）、base（12/768/48/336）、large（16/1024/80/448）。论文主模型对应 large 量级。

## 数据
- **合成 3D**：Objaverse。每个 asset 归一化到 [-1,1]³，渲 **32 个随机视图**（同一相机指向物体、任意位姿），分辨率 **1024×1024**；相机采样自半径 [1.5,3.0] 的球、高度 [-0.75,1.60]；**纯白背景**（不建模背景）。
- **真实视频**：MVImgNet（真实世界物体的多视图视频帧）。用预测的物体 mask 裁剪居中、相应调整相机参数，用 off-the-shelf 包（rembg）去背景。
- **规模**：预处理后共 **730,648 个 3D asset + 220,219 个视频** ≈ **百万级 3D 数据**。全部公开可得。
- **训练采样配比**：每个 epoch 含 1 份 Objaverse 渲染 + **3 份** MVImgNet 视频帧（人为平衡合成/真实比例，因合成数据量是真实的 3 倍多）。
- **消融结论（关键）**：去掉真实数据所有指标明显下降（PSNR 19.0→15.5，LPIPS 19.1→29.3），尽管合成数据是真实数据 3 倍——真实数据在光照、目标尺寸、相机位姿上的变化对学习帮助很大；**合成+真实组合显著优于单一来源**。
- **评测数据**：从 Objaverse / MVImgNet 各取 50 个未见物体做数值分析；GSO（Google Scanned Objects）100 物体做与 SOTA 的定量对比；可视化还用了 ImageNet、ABO、手机实拍、Adobe Firefly 生成图。

## 训练方法
- **训练目标极简**：只在 V 个视图（输入视图 + V-1 个随机侧视图）上做**图像重建损失**，无任何 3D 正则：
  - `L_recon = (1/V) Σ [ L_MSE(x̂_v, x_GT_v) + λ·L_LPIPS(x̂_v, x_GT_v) ]`
  - L_MSE 为归一化逐像素 L2，L_LPIPS 为感知损失，**λ=2.0**。
  - 消融：去掉 LPIPS，CLIP-Sim/SSIM/LPIPS 退化到 74.7/76.4/29.4，**LPIPS 损失影响巨大**。
- **单阶段端到端**，无 SFT / 无偏好对齐 / 无蒸馏（这是确定性回归模型，非生成模型，不涉及 RLHF/DPO）。
- **相机归一化（核心 trick）**：训练时把输入相机位姿归一化（Objaverse 统一归到位置 [0,-2,0]、相机竖轴对齐世界 z 轴上方；视频归到 [0,-dis,0]，dis 为原始物-相机距离）。消融 Table 8：不做归一化 PSNR 仅 15.3，随机旋转增广 18.0，**归一化 19.0**——归一化让所有图像从同一方向投影到 triplane，模型才能充分学到跨物体先验。推理时对未知相机直接套用 Objaverse 的归一化相机参数。
- **超参**：AdamW（β2=0.95），lr=4e-4，cosine schedule + 3000 步 warmup，梯度裁剪 1.0，weight decay 0.05（不作用于 bias 和 LN），**BF16 混合精度**。每样本用 V=4（3 侧视图）监督。
- **训练分辨率增益 trick**：把 512×512 参考新视图随机缩到 128–384 之间，只让模型重建随机选的 128×128 区域，等效提升有效分辨率。
- 消融趋势：侧视图越多越好（1→4：PSNR 18.7→19.1）；训练视图数 16 后饱和；渲染分辨率 32→128 提升明显（PSNR 18.8→19.4，LPIPS 20.1→18.0）；NeRF MLP 层数 2–4 即够（甜点在 2 层）；decoder cross-attn 层数加深对 CLIP/LPIPS 略有提升；triplane 分辨率（仅靠反卷积上采）越高图像质量越好但增益有限。

## Infra（训练 / 推理工程）
- **训练算力**：**128 张 NVIDIA A100（40G）**，batch size **1024**（1024 个不同物体/iter），训 **30 epoch ≈ 3 天**。
- **显存优化**：用 ARF 的 **deferred back-propagation（延迟反传）** 省 GPU 显存；BF16 混合精度。
- **代码基础**：整合公开 codebase——threestudio、x-transformers、DINO（论文 Reproducibility Statement）。
- **推理**：单张 A100，输入任意图（去背景、裁方），假设未知相机=Objaverse 归一化相机，从 triplane-NeRF 查询 **384×384×384** 点、Marching Cubes 提 mesh，**全过程 < 5 秒**，无任何后处理优化。
- OpenLRM 复现用 8 GPU + bf16（accelerate），并接入 xFormers 的 memory-efficient attention 加速 DINOv2 encoder。

## 评测 benchmark（把效果讲清楚）
**主结果——GSO 100 物体、20 参考视图（论文 Table 1，越↑/↓越好）：**

| 模型 | FID↓ | CLIP-Sim↑ | PSNR↑ | LPIPS↓ | Chamfer↓ |
|---|---|---|---|---|---|
| [[point-e]] | 123.70 | 0.741 | 15.60 | 0.308 | 0.099 |
| Shap-E | 97.05 | 0.805 | 14.36 | 0.289 | 0.085 |
| One-2-3-45 | 139.24 | 0.713 | 12.42 | 0.448 | 0.123 |
| **LRM (ours)** | **31.44** | **0.902** | **19.60** | **0.163** | **0.053** |

LRM 在全部 5 个指标上大幅领先：FID 比次优（Shap-E 97.05）低 3 倍，Chamfer 距离仅 0.053（几何质量最好）。作者特别强调：在网络/数据规模上 LRM 并不占优（5 亿参数 vs Point-E/Shap-E 也有数亿参数；1M 公开数据 vs 它们数百万未公开数据），**胜在 triplane 紧致结构化表征 + 端到端可微框架带来的有效 scaling**。

**消融用小基线（32×A100/15 epoch 的缩小版）的未见集结果（PSNR/CLIP-Sim/SSIM/LPIPS）：**
- Final（主模型）20.1 / 91.0 / 79.7 / 16.0；Baseline 19.0 / 87.8 / 77.4 / 19.1。
- 数据：合成 15.5 / 真实 17.5 / **合成+真实 19.0** PSNR。
- 相机归一化：None 15.3 / Random 18.0 / **Normalized 19.0** PSNR。

**定性**：与 One-2-3-45 对比（直接用对方论文/demo 提供的输入图避免 cherry-pick），LRM 细节更锐、表面更一致；能对非对称物体（长颈鹿、企鹅、熊）推断语义合理的遮挡区域，说明学到了有效跨物体先验。

**局限/失败案例**（论文 Fig.4 & Limitations）：① 遮挡区纹理模糊（单图到 3D 本质是概率问题，确定性模型输出"平均模式"）；② 推理套固定相机内外参，与真实不符（尤其裁剪缩放改变 FoV/主点）会导致形状畸变；③ 只处理无背景物体，不建模背景/复杂场景；④ 假设 Lambertian、省略视角相关建模，无法重建金属/陶瓷等高光材质。

## 创新点与影响
**核心贡献**
1. **首个大规模前馈 3D 重建范式**：把单图到 3D 从"逐物体优化/多视图生成"变成"一次前馈回归"，5 秒出结果，确立 feed-forward 3D LRM 路线。
2. **3D 作为新模态 + triplane Transformer**：用 cross-attention 把 2D 图像特征直接接地到结构化 triplane，无需预设 2D↔3D 对齐，token 数极小（3072）却高效可 scale。
3. **极简训练配方**：仅靠多视图图像重建损失（MSE+LPIPS）端到端训练，无 3D 正则、无精细调参；相机归一化是泛化关键。
4. **证明 3D 也吃 scaling law**：用 GPT 式"大模型+大数据+简单目标"在 3D 重建上同样奏效。

**影响**：LRM 直接催生了一整条 feed-forward 3D 工作链——Instant3D、PF-LRM、DMV3D、TripoSR、InstantMesh、GS-LRM/高斯版 LRM 等大量后续把 triplane 换成 3DGS、把单图扩到多视图、把 NeRF 换成更快表征，均沿用 LRM 的"大 Transformer 回归 3D 表征"骨架。社区开源 **OpenLRM**（3DTopia）让该范式可用化，HF 上有 small/base/large × {Objaverse, Objaverse+MVImgNet} 共 6 个权重。LRM 也为"文本→图像→3D"（接 text-to-image 前端）和"triplane latent 直接桥接语言做 text-to-3D"指明方向。

**已知局限**：确定性导致遮挡区糊、固定相机假设导致畸变、不建模背景与视角相关材质——这些恰是后续概率化/多视图/高斯化工作要解决的问题。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.04400
- arxiv_pdf: https://arxiv.org/pdf/2311.04400
- project_page: https://yiconghong.me/LRM/ （域名已过期被 GoDaddy 停放，原内容失效，未能获取）
- 开源复现（非官方）OpenLRM: https://github.com/3DTopia/OpenLRM
- OpenLRM 权重: https://huggingface.co/zxhezexin

## 一手源存档（sources/）
- [arxiv-2311.04400.pdf](https://arxiv.org/pdf/2311.04400)  （论文全文，PDF 不入 git）
- [openlrm--readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/openlrm--readme.md)  （开源复现 README，含模型配置表）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/lrm--project-page.md)  （原项目页抓取结果——已被停放，仅留作证据）
