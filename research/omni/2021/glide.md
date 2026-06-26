---
title: "GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models"
org: OpenAI
country: US
date: "2021-12"
type: paper
category: t2i
tags: [diffusion, classifier-free-guidance, clip-guidance, text-to-image, inpainting, adm, openai]
url: "https://arxiv.org/abs/2112.10741"
arxiv: "https://arxiv.org/abs/2112.10741"
pdf_url: "https://arxiv.org/pdf/2112.10741"
github_url: "https://github.com/openai/glide-text2im"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2112.10741.pdf, glide--readme.md, glide--model-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GLIDE 是 OpenAI 首个文本条件扩散文生图系统，用一个 3.5B 参数的 64×64 文本条件扩散模型 + 1.5B 上采样模型把语言映射到像素，并系统对比 CLIP guidance 与 classifier-free guidance，结论是 **classifier-free guidance 更优**；在 MS-COCO 256×256 取得 **zero-shot FID 12.24**，人评中 **87% 偏好率胜过 DALL·E（即便 DALL·E 用 CLIP 重排）**，且把模型 fine-tune 即可做文本驱动的 inpainting 编辑。它是 [[dall-e-2]] 的直接技术前身。

## 背景与定位
2021 年的文生图主流是 GAN（AttnGAN/DF-GAN/XMC-GAN）和自回归离散隐码（[[dall-e-1]]，12B 参数 + dVAE + CLIP 重排）。GAN 难以稳定生成贴合复杂提示的照片级图像；DALL·E 走自回归路线、采样昂贵且需 CLIP rerank。与此同时扩散模型这条线刚刚证明能打：[[ddpm]] 奠定去噪目标，[[improved-ddpm]]（Nichol & Dhariwal 2021）学习方差以减少采样步数，**ADM（[[diffusion-models-beat-gans]]，Dhariwal & Nichol 2021）用 classifier guidance 在 class-conditional 设定下超过 BigGAN**。GLIDE 的核心动作是把"guided diffusion 能产生照片级样本"和"文生图能处理自由文本"两条线**合流**：将 ADM 架构扩展出文本条件，并把 class-conditional 的 guidance 思想迁移到文本条件下，逐一比较两种引导策略。

相对前置工作的关键改进：
- 不再依赖单独训练的分类器（classifier guidance）或自回归 + 离散隐码（DALL·E），用**单个扩散模型 + classifier-free guidance** 即可在文本引导下产生照片级结果。
- 提出 **noised CLIP**（在加噪图像上训练的 CLIP）作为 CLIP guidance 的正确梯度来源，解决社区"用公开 CLIP 引导扩散需大量 augmentation/perceptual loss"的痛点。
- 把生成模型 fine-tune 成显式 inpainting 模型，实现文本驱动的局部编辑，并可与 [[sdedit]] 结合做 sketch-to-image。

## 模型架构
**Backbone：ADM（Ablated Diffusion Model）U-Net**，沿用 Dhariwal & Nichol (2021) 的 ImageNet 64×64 架构，但加文本条件并把宽度放大到 512 通道，视觉部分约 **2.3B 参数**。这是 U-Net 时代的工作，无 DiT、无 latent / VAE 压缩——**直接在像素空间做扩散**（base 在 64×64 像素上）。

**文本编码与条件注入**：
- 文本先 tokenize 成 K 个 token，喂进一个独立的 **Transformer**（24 个 residual block，宽度 2048，约 **1.2B 参数**）。
- Transformer 输出**两路注入**：(1) 最后一个 token 的 embedding 替代 ADM 里的 class embedding（全局条件）；(2) 整层 token embeddings（K 个特征向量序列）分别投影到 U-Net 每个 attention 层的维度，**拼接到该层的 attention context**（细粒度 cross-attention 式条件）。

**两阶段级联（cascaded diffusion）**：
- Base 模型：文本条件，64×64，3.5B 参数（视觉 2.3B + 文本 1.2B）。
- Upsampler：64×64 → 256×256 的扩散上采样模型，**1.5B 参数**，同样文本条件但用更小文本编码器（宽度 1024 而非 2048），架构沿用 ADM ImageNet upsampler 但 base channel 提到 384。低分辨率输入经 bicubic 上采样后在通道维拼接进 upsampler。

**noised CLIP（用于 CLIP guidance 分支）**：64×64 的 ViT-L（patch 4×4），在加噪图像上训练 image encoder f(x_t, t)，与原始 CLIP 同目标，使其在采样过程遇到的带噪中间图像上仍给出正确梯度。

**inpainting 改造**：在 base U-Net 上新增 4 个输入通道——第二组 RGB（已知区域）+ 1 个 mask 通道；新增通道的输入权重初始化为 0 再 fine-tune。upsampler 始终拿到完整低分辨率图，但高分辨率只给未遮挡区域。

参数量总览：base 3.5B / upsampler 1.5B / GLIDE (small) 与 GLIDE (filtered) 各约 300M。

## 数据
- **主模型（GLIDE，未公开权重）**：与 DALL·E 相同的内部数据集（原文 §4.1 仅写 "train our model on the same dataset as DALL-E"，**未在本文披露该数据集精确规模与配比**），仅说"训练算力大致等同于 DALL·E"。
- **noised CLIP（最终 ViT-L）**：在 Radford et al.(2021) 的 CLIP 数据集与 DALL·E 数据集 **50%-50% 混合**上训练；训练后再在更广的互联网图像上 fine-tune。
- **GLIDE (filtered)（公开发布的 300M 安全版）**：从互联网收集数亿图文对（largely disjoint 于 CLIP/DALL·E 的数据集），经过多重过滤后约 **67M 图文对**。
- **公开 noised CLIP（ViT-B）**：GLIDE (filtered) 数据集 + 过滤版原始 CLIP 数据集，合计约 **137M 对**。

**过滤/清洗（Appendix F，为安全发布而做）**：
- **去人像**：先标几千个布尔标签，把图像缩放到短边 224 后沿长边取 3 个 crop，喂 CLIP ViT-B/16 取特征做 mean-pool，再用 RBF 核 SVM 分类，调 bias 到 <1% 假阴率；在 1024 张独立测试上做到 0 假阴。（注：早期用 ViT-B/32 会漏掉低光/遮挡人物，换成隐状态分辨率更高的 ViT-B/16 后修复。）
- **去暴力物体**：CLIP 检索 "weapon"/"violence" 等词，收集正负例训 SVM，主动学习在决策边界附近补样本，迭代多轮，调 bias 到 <1% 假阴；1024 测试 0 假阴。
- **去仇恨符号**：CLIP 关键词检索发现数据源里这类图很少（说明上游已部分过滤），只针对 swastika 与 confederate flag 训 SVM。
- 论文未报告美学评分过滤或 re-captioning，也未用合成数据。

## 训练方法
**训练目标**：标准 DDPM 简化目标 `L_simple = E[‖ε − ε_θ(x_t, t)‖²]`（预测加进去的噪声），并采用 [[improved-ddpm]] 的**可学习方差 Σ_θ** 以便用更少步数采样。属经典 ε-prediction 扩散，**非 flow matching / rectified flow**（那是后来的工作）。

**两种引导策略对比（核心实验）**：
- **Classifier-free guidance（CFG）**：训练时以固定概率把文本 caption 换成空序列 ∅；采样时按 `ε̂_θ(x_t|c) = ε_θ(x_t|∅) + s·(ε_θ(x_t|c) − ε_θ(x_t|∅))` 外插，s≥1 为 guidance scale。
- **CLIP guidance**：用 noised CLIP 的 image·caption 点积梯度扰动反向过程均值 `μ̂ = μ + s·Σ·∇(f(x_t)·g(c))`。
- 结论：CLIP guidance 能把"CLIP score"刷得很高，但论文判断这是**在评测用 CLIP 上找对抗样本**；人评中 **CFG 在 photorealism 和 caption similarity 上都显著更优**（见下表 Elo），故论文最终样本一律用 CFG。

**多阶段训练流程（主模型）**：
1. **预训练**：base 2.5M iters @ batch 2048；upsampler 1.6M iters @ batch 512；16-bit 混合精度 + 传统 loss scaling，训练稳定。
2. **Fine-tune 支持 CFG / 无条件生成**：与预训练完全一致，但 **20% 的文本 token 序列替换为空序列**，使模型同时保留有条件与无条件生成能力。
3. **Fine-tune inpainting**：随机擦除训练样本区域，把剩余部分 + mask 通道作为额外条件喂入（新通道权重初始化为 0）。

**GLIDE (filtered) 训练超参（Appendix B）**：预训练 1.1M iters，再 fine-tune 500K iters（同时做 CFG + inpainting）；小 upsampler（192 base channel / 512 文本 channel）训 400K iters。**noised CLIP**（ViT-L）：390K iters @ batch 32K，weight decay 0.0125，训完再 fine-tune 30K iters。

**采样超参（Appendix B.2）**：论文图样本 base 用 150 步（inpainting 100 步）；评测用 250 步（FID 略好）。**upsampler 用特殊 strided schedule 仅 27 步**——把过程分 5 段，每段取 {10, 10, 3, 2, 2} 个均匀步（即 (800,1000] 只采 2 步、(0,200] 采 10 步），由内部验证集 FID sweep 选出。论文未涉及 consistency / LCM / ADD 等步数蒸馏（属后续工作）。

## Infra（训练 / 推理工程）
- **训练算力**：未给精确 GPU·时，仅说 base+upsampler 总训练算力**大致等同于 DALL·E**（DALL·E 为 12B 参数自回归模型）；GLIDE 用 3.5B 参数 + 大致相同算力，**参数量约为 DALL·E 的 1/3.4**。
- **精度/吞吐**：16-bit 精度 + 传统 loss scaling 训练稳定；具体并行/分布式策略、batch 的硬件映射、吞吐数字均未披露。
- **推理延迟**：未优化版本在**单张 A100 上采样一张图约 15 秒**——论文明确指出这远慢于 GAN 的单次前向，是扩散路线的主要工程短板。
- **部署形态**：公开发布 GLIDE (filtered) 300M 权重 + 公开 noised CLIP（ViT-B）权重 + 代码（github.com/openai/glide-text2im），含 text2im / inpaint / clip_guided 三个 notebook；主 3.5B 模型与内部数据**不公开**（出于 deepfake / disinformation 安全考量）。

## 评测 benchmark（把效果讲清楚）
**MS-COCO 256×256 zero-shot FID（Table 2，30k caption 采样，对比整个验证集）**：
| 模型 | FID |
|---|---|
| AttnGAN | 35.49 |
| DM-GAN | 32.64 |
| DF-GAN | 21.42 |
| DM-GAN+CL | 20.79 |
| XMC-GAN | 9.33 |
| LAFITE | 8.12 |
| DALL·E | ~28（zero-shot） |
| LAFITE | 26.94（zero-shot） |
| **GLIDE** | **12.24（CFG scale 1.5，zero-shot）** |
| GLIDE（验证集去重后）| 12.89 |

GLIDE 从未在 MS-COCO 上训练，zero-shot FID 12.24 大幅领先同为 zero-shot 的 DALL·E(~28) 与 LAFITE(26.94)（在 MS-COCO 上专门训练的 XMC-GAN/LAFITE 的 FID 更低属常规非零样本设定）。验证集按 DALL·E 做法去除与训练集相似图（减 21% 验证样本）后 FID 仅从 12.24 微升到 12.89。

**人评 Elo（Table 1，256×256，MS-COCO 验证 prompt，CFG scale 3.0 / CLIP guidance scale 2.0）**：
| Guidance | Photorealism | Caption |
|---|---|---|
| Unguided | -88.6 | -106.2 |
| CLIP guidance | -73.2 | 29.3 |
| **Classifier-free guidance** | **82.7** | **110.9** |
→ CFG 在两维度都大幅领先，验证了"CLIP guidance 高 CLIP score 是对抗样本假象"的判断。

**GLIDE vs DALL·E 人评胜率（Table 3，GLIDE 的 win probability）**：
| 设置 | DALL·E Temp | Photorealism | Caption Similarity |
|---|---|---|---|
| 均无 rerank | 1.0 / 0.85 | 91% / 84% | 83% / 80% |
| DALL·E 用 CLIP rerank | 1.0 / 0.85 | 89% / 87% | 71% / 69% |
| DALL·E rerank + GLIDE 过 dVAE 模糊 | 1.0 / 0.85 | 72% / 66% | 63% / 61% |
→ 即便给 DALL·E 大量测试时算力（512 选 16 的 CLIP rerank）并人为劣化 GLIDE（过 DALL·E 的 dVAE 让其变模糊），GLIDE **在所有设置都被偏好**。摘要常引用的"87% photorealism / 69% caption"即来自此表（reranked、temp 平均口径）。

**消融结论**：
- Pareto 前沿（Fig.6，MS-COCO 64×64）：在 FID-vs-IS、Precision-vs-Recall 上 CFG 近乎 Pareto 最优；唯独 CLIP-score-vs-FID 上 CLIP guidance 看似更优——但人评推翻之。
- **CFG 比放大模型更划算（Table 4）**：300M 模型 + CFG 的 Elo 提升 > 把模型放大 ~10×（3.5B）；论文原话"classifier-free guidance gives a larger Elo boost than scaling the model by roughly 10x"。
- **noised CLIP > 公开 CLIP guidance（Appendix D）**：用 noised ViT-B CLIP 引导 + 上采样，比社区用未加噪 CLIP + augmentation/perceptual loss 的方案质量相当或更高，且更简单。
- 失败案例（Fig.8）：对极不寻常对象（八条腿的猫、三角形车轮）仍会失真。

## 创新点与影响
**核心贡献**：
1. **确立 classifier-free guidance 为文生图引导的主流方案**——通过严谨人评证明 CFG 在 photorealism 与 caption 一致性上优于 CLIP guidance，并量化出"CFG 比 10× 模型规模更有效"，深刻影响其后几乎所有扩散文生图（Imagen / Stable Diffusion / DALL·E 2/3）默认采用 CFG。
2. **OpenAI 首个扩散文生图**，把 ADM（class-conditional 击败 GAN）成功迁到自由文本条件，并以 1/3 参数、相近算力、无需 CLIP rerank 全面胜过自回归的 DALL·E，标志生成范式从自回归/GAN 向**扩散**转向。
3. **noised CLIP**：指出公开 CLIP 在加噪中间图上是 OOD，提出在加噪图上训练 CLIP 以获得正确引导梯度。
4. **文本驱动 inpainting 编辑**：显式 fine-tune inpainting（含 mask 通道、零初始化新权重），并与 SDEdit 结合做 sketch-to-image，开启"生成 + 迭代局部编辑"工作流。

**对后续工作的影响**：GLIDE 是 [[dall-e-2]]（unCLIP，2022.04）的直接技术前身——DALL·E 2 复用了 GLIDE 的扩散 decoder 与 CFG 思路并前置 CLIP prior。其"文本条件 U-Net + 级联上采样 + CFG"模板被 Imagen 等延续；CFG 成为后续所有主流 t2i/视频扩散模型的标配。

**已知局限**：
- 像素空间扩散，单 A100 一张图约 15 秒，远慢于 GAN（latent diffusion 才解决此问题）。
- 复杂/不寻常提示仍会失败；属性绑定与组合能力在小模型上明显更差。
- 安全/偏见：即便过滤掉人像，GLIDE (filtered) 仍放大数据偏见（"toys for girls"更多粉色、"religious place"偏向教堂且被 CFG 放大），呈现强 Western 偏见；过滤只覆盖 swastika/confederate flag 两类仇恨符号，且会副作用地削弱无关符号（"recycling symbol"/"orange triangle"）的生成保真度。
- 主 3.5B 模型与内部数据未公开，仅放出 300M filtered 版与 noised ViT-B CLIP。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2112.10741
- arxiv_pdf: https://arxiv.org/pdf/2112.10741
- github: https://github.com/openai/glide-text2im
- model-card: https://github.com/openai/glide-text2im/blob/main/model-card.md

## 一手源存档（sources/）
- [arxiv-2112.10741.pdf](https://arxiv.org/pdf/2112.10741)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/glide--readme.md)
- [model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/glide--model-card.md)
