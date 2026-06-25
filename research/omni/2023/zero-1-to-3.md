---
title: "Zero-1-to-3: Zero-shot One Image to 3D Object"
org: "Columbia University / Toyota Research Institute"
country: US
date: "2023-03"
type: paper
category: 3d
tags: [novel-view-synthesis, image-to-3d, diffusion, view-conditioned, sjc, objaverse, zero-shot, nerf]
url: "https://arxiv.org/abs/2303.11328"
arxiv: "https://arxiv.org/abs/2303.11328"
pdf_url: "https://arxiv.org/pdf/2303.11328"
github_url: "https://github.com/cvlab-columbia/zero123"
hf_url: "https://huggingface.co/cvlab/zero123-weights/tree/main"
modelscope_url: ""
project_url: "https://zero123.cs.columbia.edu/"
downloaded: [arxiv-2303.11328.pdf, zero-1-to-3--readme.md, zero-1-to-3--project.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Zero-1-to-3（Zero123）通过在合成多视图数据上微调 [[stable-diffusion]]，把"相对相机视角变换"作为一个可控条件"螺栓"挂载到大规模扩散模型上，从而用**单张 RGB 图**做零样本新视角合成（NVS）与单图 3D 重建。其核心论点：大规模 2D 扩散模型在仅看 2D 图像的情况下已隐含学到丰富的 3D 几何先验，只需学一个视角控制机制即可"解锁"。在 Google Scanned Objects 上 NVS 的 PSNR 18.378 / LPIPS 0.088 / FID 0.027，全面碾压 DietNeRF、Image Variation、SJC-I 等基线，开启了"2D 扩散 → image-to-3D"的范式。

## 背景与定位
单图 3D 重建与新视角合成是高度欠约束（under-constrained）问题，需要极强的先验。此前主流路线有两类局限：
- **闭世界 3D 监督**：依赖昂贵的 CAD 模型、stereo、相机位姿或类别先验（DeepSDF、PixelNeRF 等），数据规模与多样性远不及互联网图文数据，泛化差。
- **2D 扩散蒸馏 text-to-3D**：[[dreamfusion]]、Magic3D、SJC 等用 SDS/PAAS 把文本扩散模型蒸馏成 NeRF，但是文生 3D，缺少对"输入图像 identity"的保持，且存在 **Janus（多面）问题**——文生图模型天然偏好正面规范姿态（论文 Figure 2 展示 DALL·E 2 / SD v2 对 "a chair" 几乎只出正面椅子）。

Zero-1-to-3 的关键洞察与改进：把 NVS 重新表述为**视角条件下的 image-to-image 翻译**任务，用合成数据**显式建模相机外参的相对变换**，而不是靠 "a back view of" 这类 prompt trick。由于显式注入了相机视角且在 Objaverse 上微调以保证视角变换后的一致性与精度，它**从根本上缓解了 Janus 问题**（README 专门讨论）。技术脉络上，它站在 [[latent-diffusion-ldm]]（LDM/Stable Diffusion）、[[dreamfusion]]（SDS）、SJC（PAAS score）、Objaverse（大规模 3D 资产）这几项工作的交汇点上，并**反转了"先重建 3D 再渲染新视角"的顺序**——先快速生成新视角，再（可选）蒸馏成 3D。

## 模型架构
**Backbone：U-Net 的隐空间条件扩散（latent diffusion）**，直接复用 Stable Diffusion 的 encoder E / 去噪 U-Net θ / decoder D，不改主干结构，只"挂载"视角控制。

视角与图像信息通过**混合（hybrid）双流条件注入**：
- **高层语义流（cross-attention）**：取输入图的 **CLIP 图像 embedding**（维度 768），与相对相机外参 (R, T) 拼接，构成"posed CLIP" embedding `c(x, R, T)`，经 cross-attention 注入去噪 U-Net，提供物体类型/结构等高层语义。
- **低层细节流（channel concat）**：把**输入图直接在通道维与正在去噪的隐变量拼接**（channel-concatenate），帮助模型保持物体 identity 与纹理细节。这是 image-conditioned SD 的做法，借用了 Lambda Labs 的 image-variations 检查点起步。

**相机位姿编码**：用球坐标系 (θ 极角, φ 方位角, r 半径) 表示相机位置。相对变换为 (θ₂−θ₁, φ₂−φ₁, r₂−r₁)。因方位角不连续，φ 编码为 [sin φ, cos φ]，最终送入模型的是 4 维向量 **[θ, sin φ, cos φ, r]**。相机始终指向物体中心，故外参由相机位置唯一确定；假设水平 FOV 49.1°，pinhole 相机模型。

**架构改动细节（附录 C）**：原始 SD 不接受图像多模态条件，先用 image-variations 的已有改造，再为接收"图像 CLIP emb + 相机位姿"额外加一个全连接层 **(768+4=772 → 768)**，这层学习率放大到其余层的 **10×**，其余网络结构与原版 SD 保持不变。

**分辨率策略**：训练用 256×256（latent 32×32），而非 SD 原生 512×512（latent 64×64）——为的是把 batch 撑大以稳定训练（见训练方法）。参数量论文未单独披露，约等于 SD v1/v2 的 U-Net 量级。

**3D 重建模块**：把视角条件扩散模型作为先验，配合 **SJC（Score Jacobian Chaining）** 优化一个 **voxel radiance field（VoxelRF）**，随机采样视角做体渲染 → 加高斯噪声 → 用 U-Net 去噪算 PAAS score `∇L_SJC` 监督 NeRF；再对输入视角加 MSE loss，并加 depth smoothness loss 与 near-view consistency loss 正则。最后用 marching cubes 从密度场抽 mesh。

## 数据
- **微调数据集：Objaverse**——大规模开源 3D 数据集，含 **80 万+（800K+）3D 模型**，由 **10 万+（100K+）艺术家**创建，几何丰富、含细粒度细节与材质属性，但无显式类别标签（区别于 ShapeNet）。
- **渲染流程（附录 B）**：对每个物体随机采样 **12 个相机外参**（指向物体中心），用 **Blender 的 Cycles 引擎**渲染，每条光线 **128 samples + 去噪步**，分辨率 **512×512**，透明背景填白。施加**随机面光源**照明。资产先归一化进 XYZ 单位立方体 [−0.5, 0.5]³，相机视角在单位球上均匀采样：θ ∈ [0, π]、φ ∈ [0, 2π]，r 在 [1.5, 2.2] 均匀采样。渲染脚本继承自 Objaverse 作者公开的 objaverse-rendering 仓库。
- **总规模**：共渲染约 **10M（千万）张图**用于微调。训练时对每个物体取两张不同视角图组成图对 (x, x_{R,T})，其相对视角变换 (R, T) 由两个外参直接推出。
- **清洗/标注/合成**：数据完全是**合成渲染**（无真实照片），无 re-captioning 等文本标注流程（本工作不依赖文本）。测试集（GSO、RTMV、in-the-wild）均在 Objaverse 之外，故评测结果可视为零样本。美学/安全过滤：未报告。

## 训练方法
- **训练目标**：标准 **DDPM/LDM 去噪 ε-prediction**。在 t ∼ [1, 1000] 时间步上最小化 `E_{z∼E(x),t,ε} || ε − ε_θ(z_t, t, c(x,R,T)) ||₂²`（论文式 (2)），即在 image+pose 条件下预测噪声。推理时从高斯噪声迭代去噪，条件为 `c(x, R, T)`。
- **微调而非从零训练**：从 image-conditioned Stable Diffusion 检查点（Lambda Labs 的 image-variations，即 `sd-image-conditioned-v2.ckpt`）起步微调，**复用互联网级预训练的几何/语义先验**，这是零样本泛化的根。
- **Classifier-free guidance（CFG）**：按 InstructPix2Pix 的做法，训练时**随机把输入图像与 posed CLIP embedding 置为 null 向量**，推理时放大条件信号，实现 CFG。
- **关键超参（附录 C.1）**：优化器 **AdamW**，学习率 **1e-4**。一个重要 trick——**大 batch 对稳定训练 SD 至关重要**：先试 batch 192 + 原始 512×512，但收敛慢、batch 间方差大；因原版 SD 训练用 batch 3072，遂**把图缩到 256×256（latent 32×32）以把 batch 撑到 1536**，显著改善训练稳定性与收敛速度。
- **算力与时长**：在 **8×A100-80GB** 机器上微调 **7 天**。README 进一步披露公开的 `300000.ckpt`（30 万步）约耗 **6000 A100 小时**；并提示训练更久的检查点会过拟合训练集、损害零样本泛化（默认推荐用 105000.ckpt）。
- **无 RL/偏好对齐、无步数蒸馏/一致性蒸馏**：本工作不涉及 RLHF/DPO/reward model，也未做 LCM/ADD 等加速蒸馏（属基础范式工作）。
- **3D 重建训练 trick（附录 D）**：相对原版 SJC 去掉了 "emptiness loss" 与 "center loss"；对可微渲染的 depth map 加 smoothness loss（利用"几何比纹理低频"的先验，有效去洞）；加 near-view consistency loss 提升跨视角纹理一致性。SJC 蒸馏沿用 DreamFusion 思路把 CFG 值设得**远高于常规**，牺牲多样性换取重建保真度。

## Infra（训练 / 推理工程）
- **训练算力**：8×A100-80GB，7 天/次微调；公开 30 万步检查点 ≈6000 A100 小时（README）。分布式细节（并行策略/混合精度/吞吐）论文未单独披露，训练脚本为 8 GPU 单节点、每卡 80GB。
- **推理（NVS）**：生成一张新视角图在 **RTX A6000 上仅需约 2 秒**——因为它**反转了顺序**（先生成新视角而非先训 NeRF），所以 NVS 又快又能在不确定性下保留多样性。
- **推理（3D 重建）**：完整跑一次单图 3D 重建（SJC 优化 VoxelRF + marching cubes 抽 mesh）在 **RTX A6000 上约 30 分钟**。mesh 抽取：先在 200³ 分辨率查询密度网格，做 (7,7,7) 均值滤波 + (5,5,5) 腐蚀，再 marching cubes（GSO 阈值 8d̄、RTMV 4d̄）。
- **部署形态**：开源 gradio demo + HuggingFace Spaces live demo（HF 资助）。经简单优化后**显存约 22GB，可在单张 RTX 3090/4090(Ti) 上跑**。in-the-wild 输入推理前用 off-the-shelf 背景去除工具预处理。
- **后续**：README 更新提及 **Zero123-XL** 检查点与 **Objaverse-XL** 数据（更大规模重训），以及社区 threestudio / stable-dreamfusion 的复现集成（属本页之外的衍生工作）。

## 评测 benchmark（把效果讲清楚）
评测两个任务，全部零样本（测试集在 Objaverse 之外）。**NVS 指标**：PSNR↑/SSIM↑/LPIPS↓/FID↓；**3D 重建指标**：Chamfer Distance(CD)↓ / 体素 IoU↑。Benchmark：**Google Scanned Objects (GSO)** 高质量扫描家居件、**RTMV** 复杂场景（每个由 20 个随机物体组成，对 Objaverse OOD）。

**新视角合成 — GSO（Table 1）**：

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | FID↓ |
|---|---|---|---|---|
| DietNeRF | 8.933 | 0.645 | 0.412 | 12.919 |
| Image Variation | 5.914 | 0.540 | 0.545 | 22.533 |
| SJC-I | 6.573 | 0.552 | 0.484 | 19.783 |
| **Ours (Zero123)** | **18.378** | **0.877** | **0.088** | **0.027** |

**新视角合成 — RTMV（Table 2，OOD）**：

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ | FID↓ |
|---|---|---|---|---|
| DietNeRF | 7.130 | 0.406 | 0.507 | 5.143 |
| Image Variation | 6.561 | 0.442 | 0.564 | 10.218 |
| SJC-I | 7.953 | 0.456 | 0.545 | 10.202 |
| **Ours** | **10.405** | **0.606** | **0.323** | **0.319** |

即便在 OOD 的 RTMV 上，各项指标仍显著领先（PSNR 10.405 vs 次优 7.953；FID 0.319 vs 5.143）。

**单图 3D 重建 — GSO（Table 3）**：

| 方法 | CD↓ | IoU↑ |
|---|---|---|
| MCC | 0.1230 | 0.2343 |
| SJC-I | 0.2245 | 0.1332 |
| Point-E | 0.0804 | 0.2944 |
| **Ours** | **0.0717** | **0.5052** |

**单图 3D 重建 — RTMV（Table 4）**：

| 方法 | CD↓ | IoU↑ |
|---|---|---|
| MCC | 0.1578 | 0.1550 |
| SJC-I | 0.1554 | 0.1380 |
| Point-E | 0.1565 | 0.0784 |
| **Ours** | **0.1352** | **0.2196** |

**关键消融/分析结论**：
- 体素 IoU 上对所有基线大幅领先（GSO 0.5052 vs Point-E 0.2944）。Point-E 虽零样本泛化不错且 CD 相对好，但只生成 4096 点的稀疏非均匀点云，表面常有洞，故 IoU 偏低；Zero123 结合多视图扩散先验 + NeRF 式表征，CD/IoU 双赢。
- MCC 能较好估计输入视角可见表面，但常无法推断物体背面几何；SJC-I 经常无法重建出有意义的几何。
- RTMV（杂乱多物体场景）上所有方法都不算好，但 Zero123 仍最佳——尽管它**并未针对 3D 重建任务显式训练**。
- 论文还定性展示了对印象派油画、DALL·E 2 生成图（text→image→3D）等 in-the-wild/OOD 输入的强泛化，以及在欠约束下采样多样性（同一固定视角可生成多种合理的几何/外观补全）。
- 与同期 NVS-with-diffusion 工作（Watson et al. 的 [56]）相比，Zero123 的差异是**用合成数据学视角控制 + 零样本泛化到野外图**；与并发的 RealFusion/NeRDi/NeuralLift-360 等相比，它不依赖 textual inversion / language-guided prior。
- 注：本工作未报告 GenEval、T2I-CompBench、HPSv2、ImageReward 等 T2I 文本对齐类指标（任务不相关）；亦无人评 ELO/Arena。

## 创新点与影响
**核心贡献**：
1. **证明大规模 2D 扩散模型隐含丰富 3D 几何先验**——仅在 2D 图上训练却能被"解锁"出视角控制能力，这是论文的首要论点。
2. **视角条件 image-to-image 扩散范式**：把相对相机外参 (R, T) 作为可"螺栓挂载"的控制条件，混合 CLIP-cross-attn（语义）+ channel-concat（细节）双流注入，保持输入 identity 的同时改变视角。
3. **零样本单图 NVS + 单图 3D 重建**：用合成 Objaverse 渲染微调即可泛化到 GSO/RTMV/野外照片/油画/DALL·E 生成图，反转"先 3D 后渲染"的传统顺序，使 NVS 快至 ~2s。
4. **从根本缓解 Janus 问题**：显式建模视角变换，规避了文生图模型的正面姿态偏置。

**对后续工作的影响**：Zero-1-to-3 是 **image-to-3D 扩散路线的开山之作**，直接催生了 Zero123-XL（Objaverse-XL 重训）、One-2-3-45、Magic123、SyncDreamer、Wonder3D、以及多视图一致扩散（MVDream、Zero123++）等一大批工作；被 Stability AI 的 threestudio、stable-dreamfusion 等主流 3D 生成框架集成为标准组件。它确立了"用 2D 扩散先验 + 视角条件 + SDS/SJC 蒸馏做 3D 生成"的工程模板。

**已知局限（作者自述 §5.1）**：
- 训练数据是**单物体 + 纯背景**，对带复杂背景的场景泛化仍是挑战（RTMV 上质量明显下降）。
- 静态物体导向，不建模动态场景/视频几何（作者展望从 scene 到 video 的方向）。
- 多视图一致性仍非严格几何一致（每个视角独立采样），后续 Zero123++/SyncDreamer 等正是为补这块短板。
- 3D 重建依赖 SJC 蒸馏，CFG 需调得很高，单图重建约 30 分钟，速度与一致性仍有提升空间。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2303.11328
- arxiv_pdf: https://arxiv.org/pdf/2303.11328
- github: https://github.com/cvlab-columbia/zero123
- project_page: https://zero123.cs.columbia.edu/
- hf_weights: https://huggingface.co/cvlab/zero123-weights/tree/main
- hf_demo: https://huggingface.co/spaces/cvlab/zero123-live

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2303.11328.pdf
- ../../../sources/omni/2023/zero-1-to-3--readme.md
- ../../../sources/omni/2023/zero-1-to-3--project.md
