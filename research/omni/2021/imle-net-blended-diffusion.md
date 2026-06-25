---
title: "Blended Diffusion for Text-driven Editing of Natural Images"
org: "The Hebrew University of Jerusalem & Reichman University"
country: IL
date: "2021-11"
type: paper
category: edit
tags: [image-editing, inpainting, clip-guided-diffusion, ddpm, training-free, mask-based, local-editing]
url: "https://arxiv.org/abs/2111.14818"
arxiv: "https://arxiv.org/abs/2111.14818"
pdf_url: "https://arxiv.org/pdf/2111.14818"
github_url: "https://github.com/omriav/blended-diffusion"
hf_url: "https://huggingface.co/omriav/blended-diffusion"
modelscope_url: ""
project_url: "https://omriavrahami.com/blended-diffusion-page/"
downloaded: [arxiv-2111.14818.pdf, imle-net-blended-diffusion--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Blended Diffusion 是首个面向**通用自然图像**的「掩码 + 文本」局部编辑方法：给一张真实照片、一个 ROI 掩码和一句文本，仅在掩码内按文本改、掩码外像素**完全不动**。核心创新是**在扩散每一步把"CLIP 引导的前景噪声潜变量"与"输入图同噪声级的背景潜变量"按掩码空间混合（blend）**，靠下一步去噪重新拉回自然流形以缝合接缝。整套方法**零训练**——直接复用预训练 [[ddpm]]（OpenAI guided-diffusion 的 256×256 无条件 ImageNet 模型）+ CLIP（ViT-B/16），用户研究中真实感 3.93/5、背景保持 4.73/5、文本匹配 4.63/5，三项全面超过 PaintByWord 等基线（CVPR 2022 收录）。

## 背景与定位
2021 年文本驱动图像编辑的两大主流路线都有硬伤：

- **GAN + CLIP（如 StyleCLIP）**：只能处理 GAN 训练域内的图（人脸/卧室），编辑真实图需先做 GAN inversion，而 inversion 存在"重建保真度 vs 可编辑性"的权衡；且 StyleCLIP 是**全局**编辑，无法指定空间区域。
- **Paint By Word（Bau et al. 2021）**：虽然支持掩码定位，但（1）主要在生成图上演示、对真实图不开箱即用；（2）背景仍会变；（3）不能为同一输入生成多个结果。

作者立了 5 条硬要求：(1) 操作**真实图**；(2) **不限定域**；(3) 只改用户指定区域、其余完美保留；(4) 接缝**无缝/全局连贯**；(5) 同一输入能**一对多**多样化生成。本工作是第一个同时满足这 5 条的方案。

技术上它站在两块基石上：[[diffusion-models-beat-gans]]（Dhariwal & Nichol 的 classifier-guidance 扩散，证明扩散质量超过 GAN，并提供了可用的预训练模型）与 CLIP（4 亿图文对训练的共享嵌入空间）。它与 [[glide]]、DiffusionCLIP（Kim & Ye）、Semantic Diffusion Guidance（Liu et al.）是**并行工作**——但 GLIDE 为编辑**专门训练**了扩散模型，而 Blended Diffusion 强调**完全不训练、纯推理期引导**。它也是后续 [[latent-diffusion-ldm]] 时代区域编辑（含作者自己的后续 Blended Latent Diffusion）的直接前身。

> 注：worklist slug 写作 `imle-net-blended-diffusion`，但论文正式名为 *Blended Diffusion for Text-driven Editing of Natural Images*（Avrahami, Lischinski, Fried），与 ECG 领域的 IMLE-Net 无关，slug 中的 "imle-net" 前缀疑为编目串号笔误。

## 模型架构
**无新训练模型**——全部复用现成组件，方法体现在采样算法而非网络结构：

- **生成 backbone**：OpenAI guided-diffusion 的 **U-Net DDPM**，**无条件**、ImageNet 训练、分辨率 **256×256**（附录另演示可换 OpenAI 的 512×512 无条件模型，对 one-hot 类别条件喂全零向量来"禁用"类别条件）。学习方差 Σ_θ（按 Improved-DDPM 在上下界间插值）。
- **文本-图像引导器**：**CLIP ViT-B/16**（OpenAI 发布版），原样使用、不改任何参数、不做 prompt engineering。
- **条件注入方式（关键）**：CLIP 在干净图上训练，无法直接吃含噪潜变量 x_t。于是每一步用 DDPM 的噪声预测从 x_t **解析估出干净图** x̂₀ = (x_t − √(1−ᾱ_t)·ε_θ)/√ᾱ_t，再把 x̂₀ 喂 CLIP 算损失，对 x̂₀ 求梯度回注采样（即 classifier-guidance 范式换成 CLIP-guidance）。
- **两路损失**：
  - 掩码内 **CLIP 损失** D_CLIP = 文本嵌入与"被掩码裁出的估计图"图像嵌入的**余弦距离**；
  - 掩码外 **背景保持损失** D_bg = ½·(MSE + LPIPS)，只在 1−m 区域计。
- **参数量/分辨率**：沿用 256×256（或 512×512）guided-diffusion 模型本身的体量；分辨率策略靠"图像外推（extrapolation）"用平移+反射填充+逐段 inpaint 把图扩到任意宽。

## 数据
**本工作不训练，故无自建训练数据集**。涉及的数据均来自被复用的预训练模型与评测素材：

- 生成 backbone 的训练数据：ImageNet（继承自 OpenAI guided-diffusion）。
- CLIP 的训练数据：4 亿网络图文对（继承自 OpenAI CLIP）。
- **评测/演示素材**：论文中除 Figure 5（来自 Paint By Word 的 GAN 生成图）外，其余输入均为**真实图**，且均以 Creative Commons 自由许可发布；掩码与文本 prompt 由作者/用户提供。
- 数据清洗/配比/re-captioning/合成数据/美学过滤：**不适用**（无训练阶段）。

## 训练方法
**核心贡献是采样（推理期）算法，而非训练**。三步演进：

1. **Local CLIP-guided diffusion（Algorithm 1，基线）**：在 classifier-guidance 框架里把引导损失换成 `D_CLIP(x̂₀,d,m) + λ·D_bg(x,x̂₀,m)`，梯度只取掩码内部分。问题：D_CLIP 虽在掩码内算，但梯度会影响全图；λ 存在两难——λ 太小（100）整图全变、λ 太大（10000）前景改不动且背景仍不完美，中间值（1000）也只是"大致保住背景、前景受限"。

2. **Blended Diffusion（Algorithm 2，主方法）**：受 Laplacian 金字塔混合（Burt & Adelson）启发，把混合搬到**扩散的各个噪声级**上做。每一步：
   - 跑一次 CLIP 引导去噪得到前景潜变量 x_{t−1,fg}；
   - 用前向加噪公式从输入图直接采到**同噪声级的背景** x_{t−1,bg} ~ N(√ᾱ_t·x₀, (1−ᾱ_t)I)；
   - 按掩码空间混合：x_{t−1} = x_{t−1,fg}⊙m + x_{t−1,bg}⊙(1−m)。
   - **关键洞见**：单步混合结果未必落在自然流形上，但**紧接的下一步去噪会把它投影回下一级流形**，自动修复接缝不连贯。最后一步把掩码外整块换成原图，从而**严格保证背景零改动**。

3. **Extending Augmentations（消融证明有效）**：直接对像素求 CLIP 梯度易出"对抗样本"（降了 CLIP loss 但没产生语义变化）。解法：对估计的 x̂₀ 先缩放到 CLIP 输入尺寸 224×224，再做 **N=16** 份不同的**随机投影变换（projective transform）**副本（掩码同步变换），分别算 CLIP 梯度后**平均**——要"骗过" CLIP 就得在所有增广下都骗过，难度大增，逼出真正的高层语义变化。

4. **Result ranking（一对多）**：一次生成 **64** 个样本，用 D_CLIP（去掉增广）对最终结果排序取高分。排序粗糙（top 20% 稳定优于 bottom 20%，但单图粒度不绝对准），实操从 top 10 里人工挑。

**关键超参**：扩散步数 k=75（背景编辑 67、scribble 编辑 60）；快速采样取 100 步（按 Improved-DDPM，100 步在 ImageNet 上近最优 FID）；增广数 N=16；总采样 64；PaintByWord++ 基线用 Adam lr=0.1 优化 VQGAN 潜变量 500 步。**无任何模型权重更新、无 SFT/RLHF/蒸馏**。

## Infra（训练 / 推理工程）
- **训练算力**：无（零训练）。
- **推理时间**：单图（Algorithm 1/2）在 **1×NVIDIA A10** 上约 **27 秒**（100 步快速采样）；PaintByWord++ 基线 78 秒。论文正文另提"约 30 秒"的口径。
- **批量与并行加速**：(1) **批生成**——一次扩散 pass 内复制输入多份并行出多结果（靠扩散随机性自然多样）；(2) **多卡并行**——各样本独立，实验用 **4×A10** 并发。组合后 **64 张约 6 分钟（<6 秒/张）**。
- **精度/吞吐**：未单独报告混合精度与吞吐数字。
- **部署形态**：开源 PyTorch（≥1.9.0）脚本，MIT 许可；权重托管在 HF（`omriav/blended-diffusion` 的 `256x256_diffusion_uncond.pt`）。无在线产品/API。
- **DDIM 对比**：附录把 Blended Diffusion 移植到 DDIM（Algorithm 3）；结论是 100 步时 DDPM 优于 DDIM，<50 步时 DDIM 更好——与 Improved-DDPM 的结论一致。

## 评测 benchmark（把效果讲清楚）
本工作**未报告 FID / CLIPScore / GenEval 等自动指标**，主评测是**用户研究（user study）**，这是其评测维度的最大局限：

- **用户研究（Likert 1–5，35 名参与者，素材取自 Paint By Word 论文图例）** —— 三项均为越高越好（均值 ± 标准差）：

  | 方法 | 真实感 Realism↑ | 背景保持 Background↑ | 文本匹配 Text match↑ |
  |---|---|---|---|
  | PaintByWord [Bau et al.] | 3.31 ± 1.38 | 3.25 ± 1.33 | 3.14 ± 1.31 |
  | Local CLIP GD（本文 Alg.1 基线） | 3.50 ± 1.19 | 3.11 ± 1.24 | 3.86 ± 1.32 |
  | PaintByWord++（本文复现增强基线） | 1.94 ± 1.36 | 3.37 ± 1.30 | 3.01 ± 1.38 |
  | **Ours（Blended Diffusion）** | **3.93 ± 1.08** | **4.73 ± 0.61** | **4.63 ± 0.77** |

  本方法三项全胜，且背景保持（4.73）与文本匹配（4.63）大幅领先。统计上：Kruskal-Wallis 检验 p < 10⁻¹³⁰；Tukey HSD 两两比较显示本方法相对所有基线在所有维度均显著（多为 p<0.001）。

- **关键消融**：
  - **Extending augmentations（Figure 7/31）**：同随机种子下，带增广的结果明显更自然、与背景更连贯——证明增广是抑制对抗结果的关键。
  - **λ 权衡（Figure 3）**：直观展示 Alg.1 单纯加背景损失无法两全，引出 blended 方案。
  - **Naïve blending（Figure 27）**：先无约束生成再硬贴回背景会出"狗头在框内、身子在框外"的不连贯——证明必须逐噪声级混合。
  - **DDPM vs DDIM（Figure 29）**：100 步 DDPM 更优。
  - **scribble 的扩散步数 k（Figure 32）**：k 大（80）更真实多样但丢涂鸦颜色，k 小（20）几乎照搬涂鸦。

- **失败案例**：(1) 排序只看编辑区→局部物体也可能高分；(2) **排版偏见（typographic bias）**——继承 CLIP 弱点，求"rubber toy"可能生成写着"rubber"的牌子；(3) 比例失调（如生成的葡萄相对豹子过大）、阴影不连贯。

## 创新点与影响
**核心贡献**：
1. 提出**首个**面向通用真实自然图像的"掩码 + 文本"**局部**编辑方案，不限域、可一对多。
2. **逐噪声级空间混合（blended diffusion）**——把经典 Laplacian 金字塔混合思想搬进扩散过程，靠"混合后下一步去噪自动投影回流形"实现无缝缝合，并通过末步硬替换**严格保证背景零改动**。
3. **Extending augmentations**——用多投影增广平均梯度，让基于梯度的 CLIP 引导扩散摆脱对抗样本，使纯推理期引导真正可用。
4. 全程**零训练**，复用现成 DDPM + CLIP，证明强大编辑能力可不靠专门训练获得。

**影响**：奠定了"训练自由 + 掩码 + 文本"区域级扩散编辑的范式，是后续大量 inpainting/局部编辑工作的参照与基线；直接催生作者团队的 **Blended Latent Diffusion**（迁到 [[latent-diffusion-ldm]] 潜空间，质量更高、速度大幅提升）。被 CVPR 2022 收录（pp. 18208–18218）。

**已知局限**：
- **推理慢**：DDPM 顺序采样，单图约 27–30 秒，且要生成 64 张挑最优，难上实时/移动端。
- **排序不准**：CLIP 排序只看编辑区、不看全图上下文，部分物体也能拿高分。
- **继承 CLIP 偏置**：排版攻击等弱点；比例/阴影不连贯。
- **评测偏弱**：仅用户研究、无 FID/CLIPScore 等标准自动指标，可复现的定量对比有限。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2111.14818
- arxiv_pdf: https://arxiv.org/pdf/2111.14818
- github: https://github.com/omriav/blended-diffusion
- project_page: https://omriavrahami.com/blended-diffusion-page/
- hf_weights: https://huggingface.co/omriav/blended-diffusion

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2111.14818.pdf
- ../../../sources/omni/2021/imle-net-blended-diffusion--readme.md
