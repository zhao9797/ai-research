---
title: "Wonder3D: Single Image to 3D using Cross-Domain Diffusion"
org: "HKU / VAST / Tsinghua"
country: China
date: "2023-10"
type: paper
category: 3d
tags: [image-to-3d, multi-view-diffusion, cross-domain, normal-maps, sdf, stable-diffusion, objaverse]
url: "https://arxiv.org/abs/2310.15008"
arxiv: "https://arxiv.org/abs/2310.15008"
pdf_url: "https://arxiv.org/pdf/2310.15008"
github_url: "https://github.com/xxlong0/Wonder3D"
hf_url: "https://huggingface.co/flamehaze1115/wonder3d-v1.0"
modelscope_url: ""
project_url: "https://www.xxlong.site/Wonder3D/"
downloaded: [arxiv-2310.15008.pdf, wonder3d--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Wonder3D 用一个**跨域扩散模型（cross-domain diffusion）同时生成 6 个视角的法线图（normal map）与对应彩色图**，再经一套几何感知的法线融合（normal fusion）算法优化 SDF，在 **2~3 分钟**内从单张图像重建出高细节带纹理网格；在 GSO 数据集上 Chamfer Distance 0.0199、Volume IoU 0.6244、新视角合成 PSNR 26.07，全面超越 [[syncdreamer]]/[[zero-1-to-3]] 等同期方法（CVPR 2024 Highlight）。

## 背景与定位
单图 3D 重建是 ill-posed 问题，需要推断可见与不可见部分的几何。2023 年主流路线有两类，各有硬伤：

- **SDS 蒸馏路线**（[[dreamfusion]]、Magic3D、[[prolificdreamer]]、Magic123、RealFusion）：用 2D 扩散先验做 per-shape 优化。问题是**慢**（数万次迭代、几十分钟到数小时）且易出 **Janus（多面）问题**——2D 先验每次只看一个视角、强迫每个视角都像输入图，缺乏显式 3D 监督。
- **直接 3D 推断路线**（Point-E、Shap-E、One-2-3-45）：从头在 3D 资产上训扩散，或用 SparseNeuS 直接回归 SDF。问题是**公开 3D 数据规模小**，泛化差、几何粗糙缺细节。

Wonder3D 接续 [[syncdreamer]]、MVDream 的**多视角 2D 生成**思路（生成一致的多视角图再重建），但点出它们的核心短板：**只生成彩色图**会受纹理歧义影响，难恢复几何细节或代价巨大（SyncDreamer 需密集视角、几何模糊；MVDream 仍要 1.5 小时 SDS 蒸馏）。

Wonder3D 的关键洞见：把 3D 资产分布 $p_a(z)$ 建模成**多视角法线图 + 对应彩色图的联合分布** $p_{nc}(n_{1:K}, x_{1:K} | y)$。法线图**显式编码几何起伏**（彩色图做不到），所以从法线恢复几何天然高保真；同时整套表示仍是 2D，可直接站在 Stable Diffusion 的十亿级图像先验上做 zero-shot 泛化。相关前置工作：[[ddpm]]、[[latent-diffusion-ldm]]、[[zero-1-to-3]]、[[syncdreamer]]、[[dreamfusion]]、[[prolificdreamer]]。

## 模型架构
**整体 pipeline 两阶段**：(1) 跨域多视角扩散生成 6 视角法线 + 彩色；(2) 几何感知法线融合优化 SDF 抽网格。

**Backbone：U-Net（基于 Stable Diffusion Image Variations 微调）**，非 DiT。条件输入有四路：
- 单张 RGB 输入图 $y$（图像条件，沿用 SD Image Variations 的 image-conditioning）；
- CLIP 文本/图像 embedding；
- 6 个视角的相机参数 $\pi_{1:K}$；
- **domain switcher** $s$（域开关）。

**三大架构设计：**

1. **多视角注意力（multi-view self-attention）**：把原始 self-attention 层扩成"全局感知"——不同视角的 Key/Value 互相拼接做注意力，隐式编码多视角依赖，使 6 个视角的彩色图与法线图几何/视觉一致（消融显示去掉后背面视角会生成不真实结果）。

2. **Domain switcher（域开关）—— 核心创新**：如何让单域的 SD 同时输出法线和彩色两个域？论文系统对比了几种朴素方案并指出其缺陷：
   - *扩通道*（UNet 输出加 4 个通道同时出法线+彩色）→ 扰动 SD 预训练权重、收敛慢、灾难性遗忘、泛化差；
   - *序列模型*（先生成法线再条件生成彩色，或反之）→ 两阶段引入计算开销且性能下降，存在 stage-1 输出与 stage-2 训练数据的域间隙（domain gap）。

   最终方案：$s$ 是一个**一维向量标签**，标记当前要生成的域（法线 $s_n$ / 彩色 $s_c$）；它先经**位置编码**，再与 time embedding 拼接注入 UNet。于是 $f(y,\pi_{1:K},s_n)$ 出法线、$f(y,\pi_{1:K},s_c)$ 出彩色。这个"微调式"修改几乎不改动 SD 预训练先验，换来快收敛 + 强泛化。

3. **跨域注意力（cross-domain self-attention）**：domain switcher 解决了"能出两个域"，但同一视角的法线和彩色不保证几何一致。跨域注意力层结构同原 self-attention，**插在每个 transformer block 的 cross-attention 之前**；它把法线域与彩色域的 Key/Value 合并做注意力，强制两域紧密相关，从而保证几何一致。Transformer block 结构（Fig 4）：ResBlock → 多视角自注意力 → 跨域自注意力 → 交叉注意力。

**视角与相机策略**：6 个固定视角（front/back/left/right/front-right/front-left），方位角 0/45/90/180/-90/-45 度；采用**输入视角相关坐标系**（非 MVDream/SyncDreamer 的全局规范系），6 视角都在输入相机系 0 仰角平面，**故无需估计输入图仰角**；假设**正交相机（orthographic）**，使模型对非真实图（草图/卡通）保持强泛化，代价是真实照片偶有焦距畸变。分辨率 **256×256**（资源所限）。

**网格抽取**：优化一个**神经隐式 SDF**（基于 instant-NGP 的 instant-nsr-pl，亦提供 NeuS 版），从 6 视角 2D 法线+彩色融合出干净几何。

## 数据
- **训练集**：Objaverse 的 **LVIS 子集**，清洗后约 **30,000+ 个物体**。论文强调：即便只在这个相对小规模数据上微调，泛化也很稳健（得益于站在 SD 的十亿级图像先验之上）。
- **渲染流程**：每个物体先归一化到居中、单位尺度；用 **BlenderProc** 从 6 视角（front/back/left/right/front-right/front-left）渲染**法线图 + 彩色图**；训练时对 3D 资产施加随机旋转以增加多样性。
- **评测集**：Google Scanned Object（GSO）数据集 **30 个物体**（与 SyncDreamer 评测集一致，从日常用品到动物），每物体渲一张 256×256 作输入；外加从网上收集的不同风格图（草图/卡通/动物）测泛化。
- 美学/安全过滤：未披露（3D 资产渲染数据，非图文对话来源）。

## 训练方法
**训练目标**：标准 DDPM 式扩散（**ε-prediction**，沿用 SD Image Variations 的策略），非 flow matching。

**两阶段训练（README 明确）**：
- **Stage 1**：训练多视角注意力——随机给定法线 flag 或彩色 flag（即让模型先学会在 domain switcher 控制下生成多视角法线**或**彩色），脚本 `train_mvdiffusion_image.py` + `configs/train/stage1-mix-6views-lvis.yaml`。
- **Stage 2**：往 SD 中**加入跨域注意力模块，只优化新增参数**（冻结其余），让两域联合一致，脚本 `train_mvdiffusion_joint.py` + `stage2-joint-6views-lvis.yaml`。

**初始化**：从 **Stable Diffusion Image Variations Model** 起步微调（该模型此前已用图像条件微调过），保留其 optimizer 设置与 ε-prediction 策略。**训练超参**：图像尺寸 256×256，total batch size 512，微调 **30,000 步**。

**几何融合阶段的优化（论文 §4.3，重点 trick）**——SDF 优化总损失：
$$L = L_{normal} + L_{rgb} + L_{mask} + R_{eik} + R_{sparse} + R_{smooth}$$

- **几何感知法线损失（geometry-aware normal loss）**：靠 SDF 二阶梯度算出 SDF 法线 $\hat g$，最大化与生成法线 $g$ 的余弦相似度做 3D 监督；引入**几何感知权重** $w_k$——给与视线夹角更大的法线赋更高权重（法线朝外、视线朝内，夹角应 ≥90°，偏离即说明法线不准）。容忍各视角生成法线的细微误差，缓解多视角法线不一致带来的几何模糊。
- **离群点丢弃损失（outlier-dropping loss）**：每次迭代不直接对所有采样光线误差求和，而是**降序排序后丢弃 top 一定比例的最大误差**。动机：错误预测与其他视角不一致、难被优化、表现为大误差，丢掉它们可消除孤立错误几何与扭曲纹理。
- 其余正则：Eikonal（SDF 梯度单位长度）、sparsity（避免 floater）、3D smoothness（SDF 梯度平滑）。

**关键工程修复（README 记录，对复现重要）**：
- 训练 bug：`zero_init_camera_projection` 必须为 **False**，否则域控制与位姿控制在训练中失效。
- 推理 bug（2024.08.29 修）：CFG 推理时跨域注意力失效导致 RGB 与法线错位——需把 RGB 与法线域输入分别放在 batch 的前半与后半（不同于常规 CFG 把无条件/有条件放前后半）。

## Infra（训练 / 推理工程）
- **训练算力**：整个微调约 **3 天**，在 **8× Nvidia Tesla A800 GPU** 集群上完成。混合精度/并行细节未单独披露；训练用 HuggingFace `accelerate`（`8gpu.yaml` 配置）。
- **推理形态**：HF Diffusers 自定义 pipeline（`flamehaze1115/wonder3d-v1.0` + custom_pipeline `flamehaze1115/wonder3d-pipeline`），float16，启用 xformers memory-efficient attention；**默认 20 步推理，guidance_scale=1.0**。前景分割用 SAM（`sam_vit_h`）或 rembg/Clipdrop。
- **端到端耗时**：从单图到带纹理网格 **2~3 分钟**（含扩散生成 + instant-nsr SDF 优化，默认 3000 步，可加到 10000 步换更好纹理）。NeuS 版更省显存、表面更平滑但更慢、纹理略糊。
- 提供 HF Demo、Colab、Windows/Docker 部署。

## 评测 benchmark（把效果讲清楚）
全部数据来自论文表 1/表 2（GSO 数据集，30 物体）。

**单图 3D 重建几何质量（表 1，Chamfer Distance↓ / Volume IoU↑）：**

| 方法 | Chamfer Dist.↓ | Volume IoU↑ |
|---|---|---|
| RealFusion | 0.0819 | 0.2741 |
| Magic123 | 0.0516 | 0.4528 |
| One-2-3-45 | 0.0629 | 0.4086 |
| Point-E | 0.0426 | 0.2875 |
| Shap-E | 0.0436 | 0.3584 |
| Zero123 | 0.0339 | 0.5035 |
| SyncDreamer | 0.0261 | 0.5421 |
| **Wonder3D (Ours)** | **0.0199** | **0.6244** |

**新视角合成质量（表 2，PSNR↑ / SSIM↑ / LPIPS↓）：**

| 方法 | PSNR↑ | SSIM↑ | LPIPS↓ |
|---|---|---|---|
| RealFusion | 15.26 | 0.722 | 0.283 |
| Zero123 | 18.93 | 0.779 | 0.166 |
| SyncDreamer | 20.05 | 0.798 | 0.146 |
| **Wonder3D (Ours)** | **26.07** | **0.924** | **0.065** |

Wonder3D 在两项几何指标和三项 NVS 指标上**全面领先**，PSNR 较次优 SyncDreamer 高出 6 个点，LPIPS 仅 0.065（次优的 0.146 的不到一半）。

**效率对比**：Wonder3D 端到端 2~3 分钟，对比 MVDream 1.5 小时 SDS 蒸馏、SDS 系方法几十分钟到数小时；One-2-3-45 虽快但几何粗糙缺细节。

**关键消融结论：**
- *跨域扩散方案*（论文 Fig 7）：(a) 带跨域注意力的跨域模型 > (b) 不带跨域注意力 > (c)(d) 序列模型。跨域注意力显著提升彩色与法线的几何一致性（冰淇淋、法老雕像等细节明显）；序列模型 rgb→normal 会有彩色色差、normal→rgb 会出不合理几何。
- *多视角注意力*（Fig 9）：去掉后背面视角彩色图出现不真实预测。
- *法线融合*（Fig 8，复杂狮子模型）：baseline 表面有大量孔洞与噪声；单用几何感知法线损失或单用离群点丢弃损失都能缓解；**两者结合最佳**，得干净表面同时保留细节。
- *泛化*：草图、卡通、动物等多风格图均能稳定生成多视角法线+彩色并重建高质量几何。

未报告：GenEval / T2I-CompBench / FID / 人评 ELO 等（非该任务相关指标，论文未涉及）。

## 创新点与影响
**核心贡献：**
1. **跨域扩散（cross-domain diffusion）范式**：首次把单图 3D 重建建模为**多视角法线图 + 彩色图的联合分布**，用法线显式承载几何、用 SD 2D 先验保泛化，兼顾了生成质量、效率、泛化、一致性四个维度。
2. **Domain switcher**：以极轻量（一维向量 + 位置编码拼 time embedding）的方式让单域 SD 输出多域，不破坏预训练先验、快收敛——比扩通道/序列建模都更优，成为后续跨域生成的常用范式。
3. **跨域注意力**：保证同视角法线与彩色的几何一致。
4. **几何感知法线融合**（几何感知法线损失 + 离群点丢弃 + 多正则）：在含噪/稀疏（仅 6 视角）2D 生成结果上稳健抽 SDF 表面。

**影响**：Wonder3D（CVPR 2024 Highlight）是 2023-2024 **image-to-3D / "法线+彩色"跨域多视角生成**路线的代表作，直接催生作者团队的系列后续——**Era3D**（512×512、自动估计焦距与仰角避免畸变）、**Wonder3D++**（进阶版）、**GeoWizard**（联合产深度与法线）、**CraftsMan3D**（原生 3D 扩散）。"生成多视角法线再融合重建"成为该时期高保真单图重建的主流套路之一。

**已知局限：**
- 仅 6 视角、256×256 低分辨率——对**很薄结构、严重遮挡**的物体难以准确重建（6 视角覆盖不全）；增加视角需更多训练算力。
- 对输入图**朝向敏感**：正面图效果最好；遮挡多则更差。
- 正交相机假设使对**真实照片**偶有焦距畸变（后续 Era3D 专门修这点）。
- 多视角注意力扩展到更多视角的效率是待解问题（作者列为 future work）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.15008
- arxiv_pdf: https://arxiv.org/pdf/2310.15008
- github: https://github.com/xxlong0/Wonder3D
- project_page: https://www.xxlong.site/Wonder3D/
- hf_checkpoint: https://huggingface.co/flamehaze1115/wonder3d-v1.0
- hf_demo: https://huggingface.co/spaces/flamehaze1115/Wonder3D-demo

## 一手源存档（sources/）
- [arxiv-2310.15008.pdf](https://arxiv.org/pdf/2310.15008)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/wonder3d--readme.md)
