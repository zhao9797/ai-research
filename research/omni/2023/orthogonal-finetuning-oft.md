---
title: "Controlling Text-to-Image Diffusion by Orthogonal Finetuning (OFT / COFT)"
org: "MPI for Intelligent Systems · Cambridge · Tübingen"
country: EU
date: "2023-06"
type: paper
category: method
tags: [finetuning, peft, subject-driven, controllable-generation, dreambooth, controlnet, orthogonal, hyperspherical-energy, stable-diffusion]
url: "https://arxiv.org/abs/2306.07280"
arxiv: "https://arxiv.org/abs/2306.07280"
pdf_url: "https://arxiv.org/pdf/2306.07280"
github_url: "https://github.com/Zeju1997/oft"
hf_url: "https://huggingface.co/docs/peft/en/conceptual_guides/oft"
modelscope_url: ""
project_url: "https://oft.wyliu.com/"
downloaded: [arxiv-2306.07280.pdf, orthogonal-finetuning-oft--arxiv-html.md, orthogonal-finetuning-oft--project.md, orthogonal-finetuning-oft--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
OFT（Orthogonal Finetuning）是一种 PEFT（参数高效微调）方法：用一个**层共享的正交矩阵 R 左乘**预训练权重（`W = R·W⁰`），在适配下游任务的同时**可证明地保持「超球能量」（hyperspherical energy，即同层神经元两两夹角结构）不变**，从而比 [[lora]]/[[dreambooth]]/[[controlnet]] 更稳、收敛更快、样本效率更高。最亮眼结果：在 controllable generation 上**仅用 5% 数据即收敛**（LoRA/ControlNet 需要 50%），且第 8 epoch 即达到 LoRA 第 20 epoch 的水平；10000 步主体驱动微调时人评对 OFT 的「整体质量」偏好达 **87.6%**（DreamBooth 11.6% / LoRA 0.8%）。NeurIPS 2023，是后续 [[boft]]（Butterfly OFT）的方法基础。

## 背景与定位
大模型文生图扩散（[[stable-diffusion-1]]、[[imagen]]、[[dall-e-2]]）已能高保真生成，但纯文本引导对**细粒度可控**仍不够，论文聚焦两个下游微调任务：
- **Subject-driven generation（主体驱动）**：给几张主体图 + 文本，生成同一主体的新场景图（DreamBooth 设定）。
- **Controllable generation（可控生成）**：给额外控制信号（canny 边缘、分割图、人脸关键点等），按信号 + 文本生成（ControlNet/T2I-Adapter 设定）。

核心痛点：现有微调要么直接小学习率更新权重（DreamBooth），要么加可重参数的小分量（LoRA、ControlNet），**都无法保证保留预训练生成能力**，且缺乏量化「保留程度」的原则性度量——它们隐式假设「与预训练模型的欧氏距离越小越好」，因此都用极小学习率。

OFT 的核心论点：**欧氏距离不足以刻画语义保留**，应该用**结构性度量**。作者借用 [[hyperspherical-energy]]（超球能量，Liu et al. NeurIPS 2018）来刻画同层神经元在单位超球上的两两关系（成对夹角/余弦相似度之和），并提出假设：**好的微调应使超球能量相对预训练几乎不变**。关键洞察来自一个不变性——**对同层所有神经元施加同一个正交变换，两两夹角（因而超球能量）可证明保持不变**。这直接催生 OFT：只学层共享正交矩阵 R 旋转/反射神经元。方法谱系上承接作者团队此前的 [[orthogonal-over-parameterized-training]]（OPT, CVPR 2021），但目标相反——OPT 旨在「最小化」超球能量以提升分类泛化，OFT 旨在「保持」预训练超球能量以不破坏预训练语义结构。

直觉支撑还来自 2D 傅里叶变换：图像的相位谱（角度信息）承载主要语义，配随机幅度谱仍能重建——论文用一个标准卷积自编码器的 toy 实验（Oxford 102 Flower 1000 张图）验证：测试时仅用神经元**角度信息**几乎可完美恢复输入图，而幅度信息几乎无用（仅有轻微色偏）。结论：**改神经元方向 = 改语义**，而约束「保持成对夹角」可在灵活性与稳定性间取得平衡。

## 模型架构
OFT 本身是**模型无关的微调算子**，不引入新 backbone；实验基座是 **Stable Diffusion v1.5**（runwayml，v1-5-pruned.ckpt），即 U-Net 扩散 + VAE 隐空间 + CLIP text encoder。OFT 改的是各层的**前向计算方式**：

- **基本形式**：对预训练全连接权重 `W⁰ ∈ R^{d×n}`（n 个 d 维神经元），前向从 `z = (W⁰)ᵀx` 改为 `z = (R·W⁰)ᵀx`，约束 `RᵀR = RRᵀ = I`（R ∈ R^{d×d} 正交）。R 初始化为单位阵，保证从预训练权重起步（类比 LoRA 零初始化）。
- **正交参数化（关键工程点）**：直接 Gram-Schmidt 太贵，改用 **Cayley 变换** `R = (I+Q)(I−Q)⁻¹`，Q 为反对称矩阵（`Q = −Qᵀ`）。代价是只能生成行列式 +1 的特殊正交群（旋转，不含反射），实测不影响性能。
- **块对角结构（降参）**：R 直接是 d×d 仍参数过多，改为 **r 个等大块对角** `R = diag(R₁,…,Rᵣ)`，每块 `Rᵢ ∈ O(d/r)`。参数复杂度从 O(d²) 降到 O(d²/r)；块间共享（`Rᵢ=Rⱼ`）再降到 O(d²/r²)。**r=1 退化为标准正交阵**。主论文统一用 **r=4**（跨任务跨数据集都好用）。
- **注入位置**：与 LoRA 严格对齐，只注入注意力模块的线性层 `W_q, W_k, W_v, W_o`。OFT 也可注入卷积层（SD 的 ResNet block）——块对角 + 块共享在卷积层有「depth-wise / channel-sharing」的可解释含义（附录 D）。
- **COFT（Constrained OFT）**：加一条 ε-偏离约束 `‖R − I‖ ≤ ε`，把微调限制在预训练模型的小邻域内。借 Neumann 级数把约束等价转到 `‖Q‖ ≤ ε′`，用投影梯度下降实现。ε 越大越像 OFT、越小越像预训练模型；COFT 比 OFT 更稳。
- **Re-scaled OFT（附录 C）**：额外学每个神经元的**正幅度缩放** D=diag(s₁,…,sₙ)（`z=(RW⁰D)ᵀx`），因为缩放幅度不改超球能量，可修复纯角度更新带来的轻微色偏；每层仅加 (N×1) 个参数。
- **零推理开销**：推理时把 R 乘回权重得 `W=RW⁰`，模型结构与速度完全等同原 SD（不同于 ControlNet 需带 361M 额外控制网络）。

与 LoRA 的关系：可改写 `z=(RW⁰)ᵀx=(W⁰+(R−I)W⁰)ᵀx`，其中 `(R−I)W⁰` 类比 LoRA 的低秩更新——**LoRA 靠低秩、OFT 靠（块对角正交的）稀疏结构**实现参数高效，是两条不同路线；OFT 是「乘性、全秩、保角」更新，LoRA 是「加性、低秩」更新。

## 数据
OFT 不预训练，只在下游任务上微调 SD v1.5，各任务数据如下（附录 A）：
- **Toy 实验**：Oxford 102 Flower 随机 1000 张图，训练卷积自编码器演示角度信息重要性。
- **Subject-driven**：官方 DreamBooth 数据集，**30 个主体 / 15 类**，每主体若干图 + 25 条文本 prompt。需额外用主体类别 prompt 生成 **200 张图**做类别先验保留损失。
- **C2I（canny→图）**：完整 **COCO 2017，约 180K 图**，用与 ControlNet 相同的 canny 检测器生成控制信号。
- **S2I（分割→图）**：**ADE20K，约 24K** 图-分割掩码对。
- **L2F（关键点→人脸）**：**CelebA-HQ，30K** 图。
- **额外任务**：D2I（深度，COCO + MiDaS 生成深度图）、P2I（densepose，DeepFashion-MultiModal 约 44K 着装人像）、Sk2I（sketch，LAION-Aesthetics 子集约 350K 图）。
- **caption 处理**：所有 image-control 对统一用 **BLIP** 自动生成 caption 作为 text prompt（即便 COCO 自带 caption 也弃用，保持一致性）。

无新增大规模训练数据、无新清洗/配比/安全过滤披露（沿用各公开数据集）。

## 训练方法
- **训练目标**：沿用所基于的任务原损失，不引入新扩散目标。
  - Subject-driven：DreamBooth 的重建损失 + **类别先验保留损失**（class-specific prior preservation loss，式 5），只更新注入的正交矩阵。
  - Controllable：ControlNet 的训练目标；额外加一个小控制信号编码器——与 ControlNet 同款 **8 层浅卷积网络（SELU 激活）**，控制信号编码后与 SD U-Net 输入拼接一次。LoRA baseline 用同款编码器。
- **训练配置（精确数字）**：
  - Subject-driven：**1× Tesla V100-SXM2-32GB**，lr=6×10⁻⁵，batch=1，约 **1000 iter**；COFT 用 ε=6×10⁻⁵。
  - Controllable：**4× A100-SXM4-80GB**，lr=1×10⁻⁵；batch=4（L2I）/16（其余）；S2I·L2I·P2I 训 20 epoch，C2I·D2I 训 10 epoch，Sk2I 训 8 epoch；COFT 用 ε=1×10⁻³。
  - Style transfer（附录 I）：1× A100-80GB，lr=1×10⁻⁴，batch=1，梯度累积 4 步；Sketch Scene 训 20000 iter、Wikiart 训 30000 iter。
- **初始化**：R=I（Q=0）从预训练权重精确起步。
- **稳定性 trick**：COFT 的 ε-偏离约束是核心稳定器——OFT 虽远稳于基线，但在 9000 iter 时仍会塌（生成 collapsed 图），COFT 仍稳定产出可用图（附录 E）。
- 无 RLHF/DPO/reward model、无蒸馏/步数加速——这些不在本工作范围。

## Infra（训练 / 推理工程）
- **算力规模很小**（学术级）：主体驱动单张 V100 即可，可控生成 4×A100。未报告总 GPU·时、吞吐、并行策略、混合精度细节。
- **参数效率（附录 B，Table 3，S2I 任务）**：可训练参数随块数 r 变化——r=2→29.5M、**r=4→16.3M**、r=8→9.7M、r=16→6.4M；对比 ControlNet 的 **361.3M** 可训练参数。**推理参数**：OFT 各 r 均为 **1.06B（= SD 本体，零额外）**，ControlNet 为 1.42B（多 361M 控制网络）。
- **推理**：零额外开销（R 融进权重，速度=原 SD）。
- **已知瓶颈**：Cayley 参数化含矩阵求逆，限制可扩展性（块对角缓解但未根除）——这正是后续 BOFT 用蝴蝶分解替代的动机。
- **代码与生态**：官方 GitHub（Zeju1997/oft，原作仓 zqiu24/oft）2023-06-23 开源，**MIT 协议**；已**集成进 HuggingFace PEFT**（含官方 conceptual guide）。

## 评测 benchmark（把效果讲清楚）
**Subject-driven（Table 1，25 主体×30 prompt，DINO/CLIP-I 主体保真、CLIP-T 文本保真、LPIPS 多样性；30 随机种子重复）**：

| 方法 | DINO↑ | CLIP-I↑ | CLIP-T↑ | LPIPS↑ |
|---|---|---|---|---|
| Real Images | 0.703 | 0.864 | — | 0.695 |
| DreamBooth | 0.614 | 0.778 | 0.239 | 0.737 |
| LoRA | 0.613 | 0.765 | 0.237 | 0.744 |
| COFT | 0.630 | 0.783 | 0.235 | 0.744 |
| **OFT** | **0.632** | **0.785** | 0.237 | 0.746 |

OFT/COFT 在 DINO、CLIP-I（主体保真）明显优于 DreamBooth/LoRA，文本保真与多样性持平或略优。

**Controllable — 控制一致性（Table 2，论文新提「control consistency」指标：从生成图反算控制信号再与原信号比）**：

| 任务·指标 | SD | ControlNet | T2I-Adapter | LoRA | COFT | OFT |
|---|---|---|---|---|---|---|
| C2I IoU↑ | 0.049 | 0.189 | 0.078 | 0.168 | **0.195** | 0.193 |
| C2I F1↑ | 0.093 | 0.317 | 0.143 | 0.286 | **0.325** | 0.323 |
| S2I mIoU↑ | 7.72 | 20.88 | 16.38 | 22.98 | 26.92 | **27.06** |
| S2I mAcc↑ | 14.40 | 30.91 | 26.31 | 35.52 | 40.08 | **40.09** |
| S2I aAcc↑ | 33.61 | 61.42 | 51.63 | 58.03 | **62.96** | 62.42 |
| L2F Error↓ | 146.19 | 7.61 | 23.75 | 7.68 | **6.92** | 7.07 |

OFT/COFT 在三类控制任务上控制一致性均强于 ControlNet/T2I-Adapter/LoRA，且**可训练参数远少于 ControlNet**。

**收敛/样本效率**：L2F 上 OFT 第 8 epoch 即达 LoRA 第 20 epoch 水平；S2I 上 OFT 仅用 **5% ADE20K 数据**就收敛（ControlNet/LoRA 需 50%）。ControlNet 的可控性在第 8 epoch「突然涌现」，OFT/COFT 收敛平滑可预测。

**FID（Table 4，S2I/ADE20K，r=4）**：SD 41.2 → ControlNet 30.9 → T2I 33.1 → LoRA 30.9 → COFT 30.8 → **Re-scaled COFT 30.2**（幅度微调仅 1 epoch 即降 FID）。

**人评（Table 6，50 人，7 主体×4 prompt=28 任务，DreamBooth/LoRA/OFT 三选一）**：
- 1000 iter：主体保真 OFT 42.6% vs DB 42.0% vs LoRA 15.4%；文本对齐 OFT **56.7%**；整体质量 OFT 45.1%。
- 10000 iter（测长程稳定性）：主体保真 OFT **76.2%**（DB 22.4% / LoRA 1.4%）；文本对齐 OFT **96.0%**；整体质量 OFT **87.6%**——长程微调时 OFT 优势压倒性。

**关键消融**：
- 块数 r（Table 3）：r 小（更接近标准正交阵）通常更好，r=4 是灵活性/参数效率甜点；简单数据集可用更大 r。
- 正交性必要性（Fig 3）：去掉正交约束的「OFT」完全无法生成真实图、无控制效果，证明正交约束是关键。
- 卷积层（Table 5）：仅微调注意力 FID 30.8，仅卷积 39.8，两者都调 30.4（略好）。
- COFT vs OFT（附录 E）：OFT 在 9000 iter 会塌，COFT 仍稳定。

## 创新点与影响
**核心贡献**：
1. 提出**超球能量保持**作为微调时「预训练语义保留程度」的可量化、可证明度量，填补了此前只看欧氏距离的空白。
2. 提出 **OFT**——用层共享正交变换乘性更新权重，**可证明保持成对神经元夹角**，在灵活性与稳定性间取得平衡；**COFT** 加 ε-偏离约束进一步增稳；**re-scaled OFT** 补幅度自由度修色偏。
3. Cayley 参数化 + 块对角结构实现高效可微正交化，可训练参数与 LoRA 同量级、**远少于 ControlNet**，且**零推理开销**。
4. 提出 **control consistency** 评测指标（反算控制信号比对），更准地度量可控生成质量。

**影响**：
- 直接催生 **BOFT（Butterfly Orthogonal Finetuning, ICLR 2024）**，用蝴蝶分解构造更密更省参的正交矩阵，缓解 OFT 块对角的表达瓶颈与 Cayley 求逆的扩展性问题。
- **已集成进 HuggingFace PEFT**，成为 LoRA 之外一类正交/保结构 PEFT 的代表方法，被广泛用于 diffusion 微调与（后续被推广到）LLM 微调。
- 把「保持预训练几何结构」这一思路引入扩散模型微调，影响后续保结构/正交类适配研究。

**已知局限（作者自陈）**：
- Cayley 变换含矩阵求逆，限制可扩展性（块对角缓解但未根除，如何可微地加速求逆是开放问题）。
- 块对角结构虽省参，但引入额外偏置、限制灵活性，如何更优更少偏置地提参数效率仍待解。
- 多任务 OFT 正交矩阵可相乘仍正交，组合性（compositionality）潜力未充分验证。
- 仍有失败案例（附录 J，主体驱动与可控生成各 3 例）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2306.07280
- arxiv_pdf: https://arxiv.org/pdf/2306.07280 （v3, 2024-03-14）
- project_page: https://oft.wyliu.com/
- github: https://github.com/Zeju1997/oft （原作仓 https://github.com/zqiu24/oft，MIT）
- hf_peft_doc: https://huggingface.co/docs/peft/en/conceptual_guides/oft
- venue: NeurIPS 2023

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2306.07280.pdf
- ../../../sources/omni/2023/orthogonal-finetuning-oft--arxiv-html.md
- ../../../sources/omni/2023/orthogonal-finetuning-oft--project.md
- ../../../sources/omni/2023/orthogonal-finetuning-oft--readme.md
