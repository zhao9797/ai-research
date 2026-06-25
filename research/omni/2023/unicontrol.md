---
title: "UniControl: A Unified Diffusion Model for Controllable Visual Generation In the Wild"
org: "Salesforce AI Research / Northeastern / Stanford"
country: US
date: "2023-05"
type: paper
category: edit
tags: [controllable-generation, controlnet, diffusion, multi-task, hypernet, moe, c2i, zero-shot]
url: "https://arxiv.org/abs/2305.11147"
arxiv: "https://arxiv.org/abs/2305.11147"
pdf_url: "https://arxiv.org/pdf/2305.11147"
github_url: "https://github.com/salesforce/UniControl"
hf_url: "https://huggingface.co/spaces/Robert001/UniControl-Demo"
modelscope_url: ""
project_url: "https://canqin001.github.io/UniControl-Page/"
downloaded: [arxiv-2305.11147.pdf, unicontrol--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
UniControl 是一个**单模型统一多种视觉条件可控生成（C2I）**的扩散基座模型：在 [[controlnet]] 之上引入 **MOE-style Adapter** 与 **task-aware HyperNet**，把 9 类视觉条件（Canny/HED/Sketch/Seg/Bbox/Pose/Depth/Normal/Outpainting）压进**一个 ~1.5B 参数模型**，等价于把 SD + 9 个 ControlNet（~4.3B）的能力压缩近 3 倍，且在 FID/感知距离/用户研究上多数任务**超过单任务 ControlNet**，并具备对未训练任务（去模糊、上色、修复、条件组合）的 **zero-shot 泛化**。NeurIPS 2023 收录。

## 背景与定位
[[stable-diffusion]] 用文本提示提供灵活语义控制，但对空间/结构/几何的像素级精确控制能力不足。[[controlnet]] 通过给 SD 增加可训练分支注入视觉条件（边缘图、深度图等）解决了这一点，但**每种条件需训练一个独立 ControlNet**，要处理 N 种模态就得部署 N 个模型（参数与时间成本随任务线性增长，且无法在模态间共享知识）。

UniControl 的核心观点：NLP 中的生成基座（InstructGPT/GPT-4）能在**单一统一模型**里多任务并 zero-shot 泛化，而视觉可控生成缺这种"统一基座"。它把多种 C2I 任务统一进一个模型，让不同视觉条件**编码到统一表示空间**，既享受参数/推理效率（模型大小不随任务数显著增长），又能利用条件之间的内在关联（如 depth 与 segmentation 共享几何信息）相互增强。相对并发工作 Prompt Diffusion（需两对额外 in-context 图像示例）的差异：UniControl **只需单张视觉条件**即可同时做多任务和 zero-shot。技术脉络上承 [[ddpm]] / [[ddim]] / [[latent-diffusion-ldm]]，直接基线是 ControlNet 与 Multi-ControlNet，并对比 GLIGEN、T2I-Adapter。

## 模型架构
**整体框架**：以冻结的 Stable Diffusion（SD v1.5，U-Net 去噪器 + VAE latent + CLIP 文本编码器）为基座，外挂一个 ControlNet 风格的可训练副本（trainable copy of SD encoder/middle blocks + zero-conv），并在此基础上加两个新模块。参数构成（论文 Tab.1）：

| 组件 | 参数量 |
|---|---|
| Stable Diffusion（冻结） | 1065.7M |
| ControlNet（可训练副本） | 361M |
| MOE-Adapter | 0.06M（每任务 ~70K，共 9 个 ≈0.63M 量级，论文记 0.06M 为总注记口径） |
| Task-aware HyperNet | 12.7M |
| **UniControl 合计** | **≈1.44B（实现描述 ~1.5B）** |
| Multi-ControlNet（9 任务等价） | SD 1065.7M + 361M×9 ≈ **4.32B** |

**1) MOE-Style Adapter（混合专家式适配器）**：一组**并行卷积模块**，每个任务对应一个专家（实现为 3 层连续 conv + 非线性激活，每个 ~70K 参数）。作用是吸收不同视觉条件的**低层特征错配**——例如分割图缺 3D 信息、深度图含 3D 信息，若共用一套浅层卷积会冲突。形式上 `F_Adapter(I_c^k) = Σ_i 1(i==k)·F_Cov1^(i)∘F_Cov2^(i)(I_c^k)`，用**指示函数硬路由**到对应任务的专家（**刻意去掉原始 MOE 的可学习门控权重**，因为可学习门控无法显式区分视觉条件）。处理完后其余参数在所有任务间共享。该硬路由设计也是 zero-shot 的关键：未见任务可**线性组合**相关预训练任务的专家（按估计的任务权重加权），从未见条件中抽取浅层特征。

**2) Task-aware HyperNet（任务感知超网络）**：把**任务指令文本**（如 "canny edge to image"）经 CLIP 文本编码器投影为 task embedding，再仿 StyleGAN2 风格调制，**把 task embedding 注入 ControlNet 的 zero-conv 层**——embedding 长度等于 zero-conv 输入通道数，每个标量按输入通道**逐通道乘到卷积核**上，调制 N=7 个 zero-conv 层。理念是"control over control / meta-control"：让超网络学跨任务的**通用可泛化表示**与元知识。任务键到指令的映射在附录 A.2 明确给出（9 个 task→instruction 字典）。论文附录 B 给出**数值证明**：调制后的 ControlNet 仍保留 ControlNet 的**零初始化性质**（zero-conv 权重初始化为 0 时 `y_c=F_SD(x)`，与 HyperNet 初始化无关），且首次梯度更新后 zero-conv 与 HyperNet 参数均可正常学习——即调制不破坏 ControlNet 的训练稳定性。训练后期会**冻结 task-aware HyperNet 参数**以稳定动态。

**条件注入路径**：完整前向 `y_c = F_SD(x) + Z_θ1(G_SD(x + Z_θ2(c)·H(c_task)))·H(c_task)`，即视觉条件经 MOE-Adapter→ControlNet 副本，两处 zero-conv 输出都被 HyperNet 的 task embedding 调制。

**分辨率**：基于 SD v1.5，训练/数据过滤围绕 512 分辨率（剔除 <512 图像）。

## 数据
**MultiGen-20M**（自建，已开源）：>2000 万张 image-prompt-condition 三元组，总大小 >2TB（README 口径）。构建流程：
- 源图：下载 **Laion-Aesthetics-V2** 中**美学评分 >6** 的子集（附录称取其约 3/4），剔除分辨率 <512 的低清图，得到 **~2.8M image-text 源对**。
- 对源图用现成抽取器生成 9 类条件（每类一般 2.8M，部分任务因检测器覆盖较少而更少）：
  - **Canny**（2.8M）：Canny 边缘检测，阈值随机化。
  - **HED**（2.8M）：Holistically-nested edge detection。
  - **Sketch**：在 HED 图上做高斯滤波+二值阈值，模拟用户手绘草图。
  - **Depth**（2.8M）：MiDaS 单目深度估计。
  - **Normal**（2.8M）：基于 depth 结果估计表面法向。
  - **Segmentation**（2.8M）：Uniformer（ADE20K 预训练，150 类）。
  - **Object Bbox**（874K）：YOLOv4（COCO 预训练，80 类）。
  - **Human Skeleton**（1.3M）：OpenPose。
  - **Image Outpainting**（2.8M）：随机 20%~80% 比例的边界遮罩。
- **任务指令**：每个任务一一对应一个固定指令（如 "canny edge to image"），**不引入指令变体**以保训练稳定。
- **测试集**：每任务额外收集 100–300 张 image-condition-prompt 三元组，源自 Laion 与 COCO（用户研究中 2/3 取自 MSCOCO、1/3 取自 Laion，覆盖室内/室外/油画/肖像/铅笔画/动画/卡通等）。
- 注：README 显示 v1.1 checkpoint 已扩到 **12 个任务**（新增 Inpainting/Deblurring/Colorization），MultiGen-20M 也全量发布 12 任务；论文正文以 9 个预训练任务为准，后三者在论文中是 **zero-shot** 评测对象。

**已知数据偏差**：作者明确指出 Laion-Aesthetics 子集存在数据偏差，尽管做了关键词+图像过滤，仍可能生成有偏/低保真/有害内容；并部署了 Safety-Checker 作为输出安全闸。

## 训练方法
- **训练目标**：沿用 [[latent-diffusion-ldm]] 的 ε-预测扩散损失，按任务定义
  `ℓ_k(θ) = E[‖ε − ε_θ(z_t, t, c_task, c_text, I_c)‖²]`，条件为"任务指令 c_task + 文本提示 c_text + 视觉条件 I_c"三元组。即**标准 DDPM/LDM 的噪声预测（非 flow matching、非 next-token）**。
- **多任务采样**：在 K=9 个任务上**均匀训练**——每步先随机选任务 k，从 D_k 采 mini-batch，按该任务损失优化 θ。
- **Classifier-free guidance**：训练时**随机丢弃 30% 文本提示**，以增强视觉条件的可控性（让条件而非文本主导结构）。
- **优化器/超参**：AdamW（PyTorch Lightning），学习率 **1e-5**，batch size **4**（每卡）。从头训练用 `cldm_v15_unicontrol_v11.yaml`，微调用更低 lr **1e-7**（README）。初始化沿用 ControlNet 的做法（用 SD v1.5 权重初始化可训练副本）。
- **迭代量**：多任务模型训练约 **900K** 迭代（保证每任务迭代量与单任务相当）；作为公平对照的单任务 ControlNet 各训 **100K** 迭代。
- **采样器**：推理用 DDIM，guidance weight **9**，**50 步**。
- **未涉及**：无 SFT/RLHF/DPO/reward model 等偏好对齐阶段，无一致性/LCM/ADD 等步数蒸馏（这是 2023.05 的可控生成基座工作，重点在统一架构而非加速）。

## Infra（训练 / 推理工程）
- **算力**：full-version 在 **16× NVIDIA A100-40G** 上训练，共约 **5,000 GPU 小时**——作者强调这与"分别训练各 ControlNet 的总成本相当"，即统一模型并未增加总训练开销。
- **框架**：PyTorch + PyTorch Lightning，AdamW 优化器。
- **推理/部署**：单模型即可切换 12 任务（README 给出每任务 `inference_demo.py --task xxx` 与 Gradio 全任务/单任务 demo）；提供 HuggingFace Space 在线 demo 与 safetensors 格式 checkpoint（unicontrol_v1.1.st）。checkpoint 体积 5.78GB（1.4B 参数）。
- **混合精度/并行细节**：论文未披露具体并行策略与吞吐数字（batch size 4 + 16 卡，未报 throughput）。

## 评测 benchmark（把效果讲清楚）
**1) 感知距离（LPIPS-style，Tab.2，越低越好，与 GT 结构相似度）**

| 方法 | Canny↓ | HED↓ | Normal↓ | Depth↓ | Pose↓ | Seg↓ |
|---|---|---|---|---|---|---|
| **UniControl** | **0.546** | **0.466** | **0.623** | **0.654** | **0.741** | 0.693 |
| ControlNet | 0.577 | 0.582 | 0.778 | 0.700 | 0.747 | 0.693 |

UniControl 在 5 个任务上更优，Seg 持平。

**2) FID（Tab.3，与单任务方法横评，越低越好）**

| 方法 | Canny↓ | HED↓ | Depth↓ | Normal↓ | Seg↓ | Pose↓ |
|---|---|---|---|---|---|---|
| GLIGEN | 24.9 | 27.8 | 25.8 | 27.7 | 27.1 | 28.9 |
| T2I-Adapter | 23.6 | 25.1 | 25.4 | 28.4 | 26.7 | 28.8 |
| ControlNet | 22.7 | 23.6 | 25.5 | 23.4 | 25.5 | 27.4 |
| **UniControl** | **22.9** | **23.6** | **21.3** | **23.4** | **25.5** | **27.4** |

UniControl 在多数任务上达到或超越所有单任务基线（Depth 提升最明显 25.5→21.3），且参数更省。

**3) 消融（Tab.4，FID，平均列尤其说明问题）**

| MoE-Adapter | TaskHyperNet | Canny↓ | HED↓ | Depth↓ | Normal↓ | Seg↓ | Pose↓ | Avg↓ |
|---|---|---|---|---|---|---|---|---|
| ✗ | ✗ | 27.2 | 29.0 | 27.6 | 28.8 | 29.1 | 30.2 | 28.7 |
| ✓ | ✗ | 24.5 | 26.1 | 23.7 | 24.8 | 26.9 | 28.3 | 25.7 |
| ✓ | ✓ | **22.9** | **23.6** | **21.3** | **23.4** | **25.5** | **27.4** | **24.0** |

平均 FID 从 28.7（裸多任务 ControlNet）→25.7（加 MOE-Adapter）→**24.0**（再加 TaskHyperNet），两模块各自有效且叠加增益。

**4) 用户研究（Amazon MTurk）**：3 名 master worker 多数投票，共 7,035 张投票（294 张 ×7 任务 + Pose 100 + Bbox 187）。
- vs 官方/复现 ControlNet（6 任务，Fig.6）：**所有任务 UniControl 胜出**，Depth/Normal 上优势尤其明显。
- vs 复现单任务 Ours-single（8 任务，Fig.7）：多数任务胜出，**seg-to-image 与 outpainting 增益最大**；投 Ours-multi 的 **p-value=0.0028（<0.05，统计显著）**。

**5) Zero-shot 泛化（定性，无定量分数）**：
- **混合条件组合**：depth+skeleton、segmentation+skeleton 双条件同时输入，配合 prompt 里 "background/foreground" 关键词，能同时保留 3D 结构与人体骨架/分割边界。
- **未见任务**：去模糊（deblurring）、灰度上色（colorization）、修复（inpainting）均能产出可用结果。上色示例靠**手工指定 MOE 权重 "depth:0.6, seg:0.3, canny:0.1"** 线性组合相关专家实现。论文还展示了未训练的 scribble-to-image 泛化能力。这些 zero-shot 任务无 FID/数值报告，仅案例分析。

## 创新点与影响
**核心贡献**
1. **首个把多种视觉条件统一进单一可控扩散基座**的工作之一：9 任务（后扩至 12）压进 ~1.5B 单模型，相对 Multi-ControlNet（~4.3B）参数压缩近 3 倍，且效果不降反升。
2. **MOE-style Adapter**：用**去门控的硬路由专家卷积**解决多条件低层特征错配，并使 zero-shot 可通过专家线性组合实现。
3. **task-aware HyperNet**："control over control"——用任务指令文本调制 ControlNet 的 zero-conv，学跨任务元知识，附录给出保零初始化与可学习性的数值证明。
4. **MultiGen-20M 数据集**：>20M（>2TB）image-prompt-condition 三元组、9/12 任务全开源，成为后续多条件可控生成的常用数据资源。
5. 验证了"条件间内在关联（depth↔seg 等）可相互增强"这一多任务学习直觉在可控生成上的有效性，并展示 zero-shot 任务/条件组合泛化。

**影响**：UniControl 是 2023 年"统一可控生成基座"方向的代表作之一，与 UniControlNet、Cocktail、T2I-Adapter 等同期工作共同推动了"单模型多条件控制"范式，为后来 OmniControl、统一编辑/可控生成模型提供了 MOE-adapter + 指令调制的设计参考。MultiGen-20M 被多个后续可控生成工作沿用。

**已知局限**：
- 继承扩散模型固有缺陷；受限于 Laion-Aesthetics 子集的**数据偏差**，可能产出有偏/低保真/有害内容（已加关键词+图像过滤与 Safety-Checker）。
- **高质量人像生成仍受限**（作者明示）。
- 仍基于 SD v1.5（512 分辨率、U-Net 架构），未升级到 SDXL/DiT；推理仍需 50 步 DDIM，无加速蒸馏。
- zero-shot 任务的专家权重部分靠**人工指定**，自动化（按指令 embedding 相似度估权）虽提出但案例以手工权重为主。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2305.11147
- arxiv_pdf: https://arxiv.org/pdf/2305.11147
- github: https://github.com/salesforce/UniControl
- project_page: https://canqin001.github.io/UniControl-Page/
- hf_demo: https://huggingface.co/spaces/Robert001/UniControl-Demo
- dataset(MultiGen-20M): gs://sfr-unicontrol-data-research/dataset
- checkpoint: https://storage.googleapis.com/sfr-unicontrol-data-research/unicontrol_v1.1.ckpt

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2305.11147.pdf
- ../../../sources/omni/2023/unicontrol--readme.md
