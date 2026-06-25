---
title: "InstantBooth: Personalized Text-to-Image Generation without Test-Time Finetuning"
org: "Adobe Inc."
country: US
date: "2023-04"
type: paper
category: edit
tags: [personalization, subject-driven, adapter, encoder-based, dreambooth, identity-preservation, tuning-free]
url: "https://arxiv.org/abs/2304.03411"
arxiv: "https://arxiv.org/abs/2304.03411"
pdf_url: "https://arxiv.org/pdf/2304.03411"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://jshi31.github.io/InstantBooth/"
downloaded: [arxiv-2304.03411.pdf, instantbooth--project.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
InstantBooth 是 Adobe 2023-04 提出的**免测试时微调（test-time-finetuning-free）的主体定制**方法：用一个可学习的图像编码器把输入概念压成一个**文本 token（concept embedding）**，再用**少量 adapter 层**把富局部特征注入冻结的 Stable Diffusion U-Net，从而单次前向就能生成保身份的个性化图像，**比 DreamBooth/Textual Inversion 快约 100 倍**（6 秒 vs ~600/1500 秒），在 person 类的 alignment（0.314 vs DB 0.309）与 face distance（1.19 vs DB 1.23）上还更优。是 encoder-based 个性化（与 ELITE/UMM-Diffusion/SuTI 同期）的代表作之一。

## 背景与定位
个性化（subject-driven / 主体定制）的目标：给定某概念的若干图，学到这个概念，再按文本 prompt 生成保持同一身份的新场景/姿态/风格。当时两条主流路线都受限：
- **反演到文本空间 + 微调**：[[dreambooth]] 微调整个扩散模型学一个唯一标识符；Textual Inversion 反演出一个文本 embedding。两者对每个新概念都要**在线优化几百~上千步、按概念存权重**，时间与存储不可扩展。
- **学图到图映射**：如 InstructPix2Pix 需要大规模"同主体不同姿态"的成对数据（极难获取），且偏像素级映射，难做大姿态/位置变化；ControlNet 能吃多模态条件但没展示身份保持能力。

InstantBooth 主张**把"学概念"的在线优化搬到离线训练**：训练一个泛化到未见概念的图像编码器（offline training-based design），推理时无需任何微调。与同期 concurrent work 的区别：ELITE 微调注意力层参数、UMM-Diffusion 只学一个视觉映射层但冻结生成器、SuTI 靠海量"专家模型生成的成对图"做 apprenticeship learning；**InstantBooth 用 adapter 把视觉信号紧耦合进生成器、冻结预训练参数，且不使用任何成对图像训练**。技术脉络上承 [[latent-diffusion-ldm]] / [[stable-diffusion]] 主干、[[dreambooth]] 的标识符思想、GLIGEN/Flamingo 的 adapter 注入思想。

## 模型架构
建立在冻结的 **Stable Diffusion V1-4**（公开可用的当时领先模型）之上，新增三组**可训练组件**，原模型（U-Net + CLIP 文本编码器）全程冻结。

**1) Concept Encoder $E_c$（概念→文本 token）**
- 用预训练 **CLIP 图像编码器**做 backbone + 一个随机初始化的全连接层（FC）。backbone 冻结，只训 FC。
- 把 N 张输入图各自的全局特征取平均，得到紧致概念向量 $f_c=\sum_i E_c(x^i_s)/N$。
- prompt 里插入唯一标识符 $\hat V$（用 "sks"，沿用 DreamBooth），格式 "... $\hat V$ [class noun] ..."（如 "A photo of a $\hat V$ person playing guitar"）。先过冻结 CLIP 文本编码器得 $c_s=\mathrm{CLIP}(p_s)$，再**把 $\hat V$ 位置的 embedding 替换成 $f_c$**，得到 concept-injected 文本 embedding $c$，作为 cross-attention 条件。

**2) Patch Encoder $E_p$ + Adapter（富局部特征→身份细节）**
- 单个文本 token 只含全局语义、丢失细节（部件形状、纹理、结构）。故另用一个 patch 编码器（同样 CLIP 图像编码器 backbone + FC）对每张输入图抽 **257 个 visual token**，把所有输入图的 token **拼接**成富 patch 序列 $f_p=\mathrm{Concat}(\{E_p(x^i_s)\})$。
- 在 U-Net 每个 Transformer block 的 self-attn 与 cross-attn **之间**插入一个可学习 **adapter 层**（zero-init gated 残差，思路同 Flamingo/GLIGEN）：
  $$y := y + \beta \cdot \tanh(\gamma)\cdot S([y, f_p])$$
  其中 $S$ 是 self-attention，$y$ 是视觉特征 token，$\gamma$ 是初始化为 0 的可学习标量（保证训练初期不破坏预训练行为），$\beta$ 是平衡 adapter 权重的常数。
- 与 GLIGEN 的关键区别：GLIGEN 给图像条件抽**全局特征**（提供风格/高层内容引导），InstantBooth 抽**富 patch token 序列**（为身份保持注入细粒度内容），且推理用不同采样调度。

**输入预处理**：把概念物体从原图裁出（crop）并**抠掉背景**（用 entity segmentation mask），$x^i_s := x^i_s\cdot m^i_s$；训练时对 masked image 做重度随机增强 $A$，原始未裁未抠的整图 $X_t$ 作 ground-truth。

**推理期三项设计**：
- **任意张数输入**：训练时每概念只用 1 张（N=1），但靠 adapter 的拼接 + self-attention 本质，推理可吃任意张条件图。
- **Balanced Sampling（调 $\beta$）**：训练 $\beta=1$；推理时 $\beta=1$ 会过强重建、削弱语言对齐，故推理**降低 $\beta$** 让 adapter 同时吸收预训练先验与条件图信息——$\beta$ 是平衡"语言理解 vs 身份保持"的主要旋钮。
- **Concept Token Renormalization（调 $\alpha$）**：即便调了 $\beta$，concept token 仍可能在 cross-attention 里**主导**（attention 权重远高于 "night"/"witcher" 等关键词，导致 language forgetting）。故对 $f_c$ 乘缩放因子 $\alpha\in(0,1]$：$f_c:=\alpha\cdot f_c$（因 cross-attn 前只有线性映射，等价于重缩放 concept token 与视觉 token 的 cross-attention）。最终取 **$\beta=0.3,\alpha=0.4$** 作折中。

## 数据
- **只用文本-图像对训练，不用同主体成对图**（这是核心便利，规避了"同主体不同姿态成对数据极难获取"的瓶颈）。
- 对 **person** 与 **cat** 两个类各收集文本-图像对：图含该类物体、prompt 含该类的粗类名词（person 类包括 person/man/woman/baby/girl/boy/lady 等；cat 类包括 cat/kitten 等）。
- 用 entity segmentation 模型（在高质量 entity segmentation 数据集上训练）给所有图收实体分割 mask。
- **过滤**：剔除目标物体区域占比 <0.1 或 >0.7 的图；剔除含多个物体的图（简化训练）。
- **规模**：person 类 **1.43M** 文本-图像对，cat 类 **0.37M**。
- 来源/版权/美学过滤等细节**未披露**（Adobe 内部数据，论文未说明具体出处）。
- **测试集**：person 用公开 **PPR10K**（1681 个身份的高质量人像，每身份多图），从 test split 选 **50 个身份**、每个取命名顺序前 5 张作输入。

## 训练方法
- **训练目标**：标准扩散去噪损失（latent ε-prediction / DDPM 目标），$L=\mathbb E_{z,t,c,X_s,\eta}\lVert\eta-\eta_\theta(z_t,t,c,X_s)\rVert_2^2$。无 flow matching、无 RL、无偏好对齐、无蒸馏——只是**冻结大模型 + 训练新增小组件**。
- 因无同主体成对图，**每概念用 1 张图训练（N=1）**：把 masked 增强图作条件 $X_s$、原整图作 GT，让模型学"从被抠背景的局部视图重建带背景的完整图"，从而把身份信息编进 adapter/encoder 而非死记背景。
- **可训练参数**：只有两个图像编码器的 FC 层 + 所有 adapter 层；CLIP 文本编码器、CLIP 图像 backbone、U-Net 全冻结。
- **超参**：person 训 **320k iters**、cat 训 **200k iters**；adapter 学习率 **1e-6**、视觉编码器 FC 学习率 **1e-4**；batch size **16**。
- **关键 trick**：(a) 训练 masking 背景（消融显示无 mask 则身份/语言能力被背景噪声拖累、重建分虚高而对齐降）；(b) zero-init $\tanh(\gamma)$ 门控保证训练稳定；(c) 重度增强提升泛化。

## Infra（训练 / 推理工程）
- **训练算力**：**4× A100 GPU**，batch size 16。未披露总 GPU·时、并行/混合精度/吞吐等细节。
- **推理**：单次前向即可，无需任何 per-concept 优化；实测**约 6 秒/张**（同一硬件下 DreamBooth ~600s、Textual Inversion ~1500s，即 **~100× 加速**）。adapter 拼接机制使推理可变长支持任意张条件图。
- **部署形态**：论文未发布代码/权重/Demo（项目页无 GitHub/HF 链接，仅论文 PDF）。属研究原型，工程化与服务化细节未公开。

## 评测 benchmark（把效果讲清楚）
**指标定义**：Reconstruction = 输入图与生成图的 CLIP 视觉特征相似度（默认 prompt "A photo of $\hat V$ [class noun]"，越高越好）；Face distance = 人脸专用，用强人脸检测器 + 在 VGGFace2 上预训练的 Inception-ResnetV1 抽脸 embedding，算成对脸的平均 L2 距离（越低越好）；Alignment = 图文 CLIP 相似度（覆盖背景改写/风格变换/组合 prompt，越高越好）。

**主对比（person 类，Table 1）**：

| 方法 | Align ↑ | Face dist ↓ | Recon ↑ | Time(s) ↓ |
|---|---|---|---|---|
| Textual Inversion | 0.2556 | 1.5462 | 0.7832 | ~1500 |
| DreamBooth | 0.3088 | 1.2281 | **0.8335** | ~600 |
| **InstantBooth (Ours)** | **0.3140** | **1.1901** | 0.7329 | **6** |
| Ours + Mask 输入 | 0.3135 | **1.1899** | — | 6 |

要点：**Alignment 与 Face distance 均最优**；Reconstruction 低于 DB/TI，但论文解释这是因为训练抠了背景、模型只重建前景人物不重建背景玻璃墙，并非身份能力差——脸相似度（face dist）反而显著更优。

**User Study（person 类，AMT，344 个有效样本，1–5 打分，Table 2）**：

| 方法 | Quality ↑ | Alignment ↑ | Identity ↑ |
|---|---|---|---|
| Textual Inversion | 2.69 | 2.72 | 2.70 |
| DreamBooth | 3.55 | 3.44 | 3.48 |
| **Ours** | **3.89** | **3.72** | **3.56** |

三项全面领先。

**消融（Table 3，person）**——基线 InstantBooth Align 0.3140 / Recon 0.7329：
- w/o train mask：0.3127 / 0.7485（重建虚高、对齐降，证明 mask 必要）
- w/o patch feature（仅用 CLS 全局特征喂 adapter）：0.3269 / **0.6494**（重建大幅崩，证明富 patch 特征对身份关键）
- w/o adapter（纯靠 $\hat V$ 扛身份）：0.3242 / **0.5468**（重建最崩）
- $\hat V$ before CLIP（在文本编码器**前**注入）：0.3127 / 0.7495（视觉变差，身份信息被冻结 CLIP 文本编码器稀释）
- Tune CLIP Vis Enc：0.3266 / 0.6425（解冻视觉 backbone 反而身份变差）
- Tune U-Net：0.3142 / 0.7265（微调 U-Net 也变差——印证冻结预训练权重才能保住原模型能力）
- 1 Image Test：0.3140 / 0.7261（单图输入 alignment 不变、重建略降——多图能提供更多前景细节）

**$\beta$/$\alpha$ 权衡（Table 4）**：$\beta$ 或 $\alpha$ 越大→身份越强但语言理解越弱（极端 $\beta{=}1,\alpha{=}1$ 时 Align 跌到 0.2087）；最终选 $\beta{=}0.3,\alpha{=}0.4$（Align 0.3140 / Recon 0.7329）。

**附录定性**：去掉 $\hat V$ 标识符训练会导致模型混淆"哪个物体该对齐输入图"（如生成 Joe Biden 时把 Biden 的脸画成输入女性的脸），证明 $\hat V$ 标识符是必要的对齐锚点。

> 注：未报告 FID / GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward / PickScore 等通用 T2I 指标——本文聚焦个性化专用指标（Recon/Face dist/Align）+ 人评。cat 类无定量表，仅给定性图。

## 创新点与影响
**核心贡献**：
1. 早期实现**免测试时微调**的主体定制之一——把"学概念"从 per-concept 在线优化转为离线训练一个泛化编码器，**~100× 提速**且无需 per-concept 存权重。
2. **双路条件设计**：concept embedding（全局语义→文本 token）+ rich patch feature via adapter（细节→视觉注入），并指出"单 token 不足以保细节、需富局部特征"这一关键洞见。
3. **只用文本-图像对训练、不用同主体成对图**即可泛化到未见概念，规避成对数据瓶颈。
4. 推理期两旋钮 **balanced sampling（$\beta$）+ concept renormalization（$\alpha$）**，定量定位并缓解 concept token 主导 cross-attention 导致的 language forgetting。

**影响**：与同期 ELITE、UMM-Diffusion、SuTI 共同开创 **encoder-based / tuning-free 个性化**范式，是后续 IP-Adapter、PhotoMaker、InstantID、Subject-Diffusion 等"即时主体定制"工作的思想前身（图像编码器→token/adapter 注入冻结主干）。"zero-init gated adapter 注入视觉条件"也成为该方向的常见模块。

**已知局限**（作者自陈）：
- **每类单独训练**（person/cat 各一套），未做跨类通用模型——需用更多类别数据联合训练解决。
- adapter 设计只接受**单一概念**提供身份细节（不支持多主体组合）。
- Reconstruction 指标偏低（因抠背景），作为身份度量不够直观。
- 未开源代码/权重，复现门槛高；仅在 person/cat 两类验证，泛化广度未充分检验。
- 作者计划把方法扩到个性化图像编辑与视频生成。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2304.03411
- arxiv_pdf: https://arxiv.org/pdf/2304.03411
- project_page: https://jshi31.github.io/InstantBooth/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2304.03411.pdf
- ../../../sources/omni/2023/instantbooth--project.md
