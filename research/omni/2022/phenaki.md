---
title: "Phenaki: Variable Length Video Generation from Open Domain Textual Descriptions"
org: Google Brain
country: US
date: "2022-10"
type: paper
category: video
tags: [text-to-video, video-generation, c-vivit, maskgit, masked-transformer, vq, story-generation, autoregressive]
url: "https://openreview.net/forum?id=vOEXS39nOF"
arxiv: "https://arxiv.org/abs/2210.02399"
pdf_url: "https://arxiv.org/pdf/2210.02399"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://phenaki.github.io/"
downloaded: [arxiv-2210.02399.pdf, phenaki--project-page.md, phenaki--openreview.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Phenaki 是 Google Brain 2022 年 10 月提出的开放域文生视频模型：用全新的 **C-ViViT**（causal ViViT）时空因果 tokenizer 把视频压成离散 token，再用 **MaskGIT 风格的双向掩码 Transformer** 由文本（T5X embedding）并行生成视频 token，最关键的创新是**可被一串随时间变化的文本提示（剧本/story）条件化、自回归续帧生成任意长（可达数分钟）的连贯视频**——这是论文声称的"首个研究 time-variable prompt 生成视频"的工作。最亮眼结果：1.8B 参数模型生成 1024 帧视频仅需 ~4.1 分钟（TATS-base 需 30 分钟），C-ViViT 在 Moments-in-Time 重建上 FVD=65.78 远超 per-frame 基线（ViT-VQGAN 166.6）且 token 数从 2560 降到 1536。

## 背景与定位
2022 年文生图已能从描述生成高分辨率图像（[[dall-e-1]]、Parti、Imagen、GLIDE），但文生视频仍难，论文点明三大障碍：
1. **数据稀缺**：图文对有 LAION-5B/JFT4B 这种十亿级，而文本-视频数据集小得多（WebVid ~10M），不足以覆盖开放域视频的复杂度；
2. **算力**：当时训 SOTA 文生图模型已逼近算力上限，留给视频（尤其变长视频）的空间极小；
3. **变长 + 故事性**：一句短 prompt 不足以描述一段长视频，理想的视频模型应能被"一串随时间变化的 prompt（story）"条件化，且能生成任意长度。

当时同期方法各有短板：
- **per-frame image encoder 路线**（GODIVA、NUWA、CogVideo 用 VQ-GAN 逐帧编码）：可变长但 token 在相邻帧高度冗余，实际只能短视频；把视频当"一串独立图像"，动态建模差、易有运动伪影。
- **fixed-length video encoder 路线**（VideoVQVAE）：token 更省但不支持变长。
- **diffusion 路线**（VDM，3D space-time U-Net 直接在像素上扩散）：只能定长，自回归扩展长视频时采样太慢不实用。

Phenaki 走的是 **离散 token + 掩码生成 Transformer** 路线（与 per-frame 自回归路线同一架构家族，但把"逐帧独立"改成"时间上自回归的时空 token"），并把生成式 Transformer 从自回归改成 MaskGIT 式并行掩码生成以大幅提速。相关脉络见 [[maskgit]]、[[vit-vqgan]]、[[parti]]、[[nuwa]]、[[cogvideo]]、[[video-diffusion-models-vdm]]。

## 模型架构
Phenaki 由两大组件构成（论文 Figure 2）：

### 1) C-ViViT —— 时空因果 video tokenizer（encoder-decoder + VQ）
核心创新。对 ViViT 的因果改造，目标是"既能时空压缩、又在时间上自回归（支持变长）"：
- **输入**：视频序列 `(tx+1)` 帧、分辨率 `hx×wx`、`cx` 通道（论文主设置 11 帧 / 128×128 / 3 通道）。
- **patch 化**：**第一帧**单独切 `wp×hp×cp` 空间 patch（默认 8×8），其余帧切 `tp×wp×hp×cp` 时空 patch（默认 2×8×8），线性投影到 `dz` 维。第一帧独立编码——这一点让"图文数据"能自然并入视频模型（单帧=图），也支持"给定起始若干帧做条件"。
- **空间 Transformer**：在空间维做 all-to-all 注意力。
- **时间 Transformer（因果！）**：在时间维用 **causal attention**，每个空间 token 只看此前帧的对应 token，从而整体自回归、支持任意帧数输入。这是相对 ViViT 的关键改动（ViViT 时间维是 all-to-all、要求定长，且只对 [CLS] token 跑时间 Transformer；Phenaki 去掉 [CLS]、对所有空间 token 跑因果时间 Transformer）。
- **量化**：对 encoder 输出做 vector quantization（VQVAE 的 VQ 目标），并采用 **ViT-VQGAN 的 factorized + L2-normalized codes** 提升码本利用率与重建质量；码本大小 |E|=8192。
- **解码器**：encoder 的"倒装"——token→embedding→时间 Transformer→空间 Transformer→单层无激活线性投影回像素。
- **压缩效果**：相对 per-frame，token 数减约 40%（Table 3：10 帧的 per-frame token 2560，C-ViViT 1536；token 数按 10 帧算，C-ViViT 因首帧独立按 11 帧算）。
- **规模**：tokenizer 主配置 = 4 层空间 + 4 层 temporal Transformer，512 hidden，8 头，2048 MLP，embedding dim 32（Table 6）；视频 token 维度 `tz,wz,hz = 6,16,16`。各重建基线约 50M 参数（论文未单列 C-ViViT 主配置参数量）。

### 2) 文生视频生成器 —— MaskGIT 式双向掩码 Transformer（MVTM）
- 把文生视频当 seq2seq：给定文本 embedding 预测视频 token。文本编码用**冻结的预训练语言模型 T5X**（非 CLIP），通过 **cross-attention** 注入视频 token。
- 不用自回归 Transformer（采样时间随序列线性增长、长视频不可行），而用 **双向 Transformer 并行预测**：训练时采样掩码比例 `γi`（0→1），随机把 `⌈γi·N⌉` 个 token 换成 [MASK]，对被掩 token 做交叉熵（MVTM，Masked Visual Token Modeling）；推理时先全标 [MASK]，每步并行预测全部掩码 token、保留置信度高的 `βi` 比例、其余重掩码再预测，迭代收敛。掩码/采样 schedule 沿用 MaskGIT。
- **采样步数比自回归少一个量级**：典型 12~48 步（论文图用 48 步，对比 NUWA 用 12 步），步数越多质量越好。
- **classifier-free guidance**：训练时 10% 概率丢弃文本条件；推理用 guidance scale λ 控制文本对齐。
- **主模型规模**：MaskGIT 主架构 = 24 层、2048 hidden、32 头、8192 MLP → **1.8B 参数**；与 NUWA 对比时缩小到 20 层/1536 hidden/24 头/6144 MLP → **0.9B**。序列长度 |z|=1536。

### 3) 任意长视频的自回归续帧（story 模式）
生成完第一段视频后，用 C-ViViT 重新编码**最后 K 帧（通常 5 帧）**作为已知 token，初始化 MaskGIT 继续生成后续 token，文本条件可换成**新 prompt**——从而在前后内容间平滑过渡，按一串 prompt 拼成"视觉故事"。这是 Phenaki 区别于"会动的图"的关键能力。

## 数据
- **训练配比（主 1.8B 模型）**：~15M 文本-视频对（8 FPS）+ ~50M 文本-图像 + ~400M 的 **LAION-400M** 图文对混训。具体配比：**视频数据占 80%，两个图像数据集各占 10%**。
- **联合图文+视频训练的动机与机制**：视频数据远不足以覆盖图文里的概念（如铅笔画/各种绘画风格只有图像里有）。Phenaki 动态调整 MVTM 目标，把图像和视频当作**同一个大数据集**——若只给单帧则只在前 `wz×hz` 个 token 上施加掩码与目标，给完整视频则在全部 token 上施加。这样图像里的概念（如铅笔画风格）能迁移到视频生成（Figure 3 的铅笔画熊猫）。
- **配比 trade-off（Table 2）**：纯视频 → FVD 最好（动态最佳）；加更多图像 → 文-视频/文-图对齐与图像 FID 更好但视频 FVD 变差。100%视频：T2V FVD 168.9；80/20：198.4；50/50：239.7。作者据此选 80% 视频配比。
- **重建评测数据**：Moments-in-Time（MiT，~802K 训练 / ~33K 验证 / ~67K 测试，25 FPS，高质量平衡、动词覆盖密）；评测时降采到 6 FPS、10 帧、128×128。
- **视频预测评测数据**：BAIR Robot Pushing（单帧→15 帧）、Kinetics-600（5 帧→11 帧）。
- **清洗/过滤/安全**：论文未详细披露图文/视频的清洗与美学过滤流程。伦理声明承认混入 LAION-400M（已知含暴力/色情/血腥偏置）会改善结果但带来风险，并称"正在训练的新版本用了能最小化此类问题的数据集"——但具体过滤方法**未披露**。无 re-captioning / 合成数据的描述。

## 训练方法
两阶段、各自独立训练：
1. **C-ViViT（tokenizer）训练**：损失 = VQ 目标 + 0.1·对抗损失（StyleGAN 判别器）+ 0.1·图像感知损失（LPIPS 类）+ 1.0·视频感知损失（I3D 网络作特征提取）+ 1.0·L2 像素损失。即 `L = LVQ + 0.1·LAdv + 0.1·LIP + 1.0·LVP + 1.0·L2`。优化器 AdamW（β1=0.9, β2=0.99），lr=1e-4，weight decay=1e-4，warmup 100K + cosine decay，目标 1M 步，batch 1028（Table 6 原文如此；重建基线训练 batch 128，warmup 100K + 余下 900K cosine——Appendix B.1.2），梯度裁剪 10。VQ commitment 权重 β=0.25。
2. **MaskGIT（生成器）训练**：MVTM 交叉熵目标 `Lmask = −Σ log p(ai | a_M̄, p)`（只对被掩 token），叠加 10% 文本 dropout 实现 CFG。优化器 AdamW（β1=0.9, β2=0.99），lr=1e-4，wd=1e-4，warmup 10K + cosine decay，目标 4M 步，batch 512，梯度裁剪 10。
- **主模型训练量**：1.8B 模型训了 **1M 步、batch 512、耗时 < 5 天**（论文用于可视化的模型）。
- **无扩散、无 flow matching、无 RLHF/DPO 等偏好对齐**——这是纯 token 级掩码生成方法（与 diffusion 路线正交）。也没有蒸馏/一致性加速；提速来自 MaskGIT 并行掩码生成本身（少一个量级的采样步数）。
- **推理超参（不同实验不同）**：对比 NUWA 用 λ=0.1、12 步、温度 4.0；图文配比消融用 λ=6、24 步、温度 4.0；论文所有展示视频用 λ=12、48 步、温度 8.0。

## Infra（训练 / 推理工程）
- **框架**：JAX + FLAX 实现。
- **算力规模**：论文**未披露**具体 GPU/TPU 型号、芯片数、并行/分布式策略、混合精度、吞吐——只给出"1.8B 模型 1M 步 batch 512 训练 < 5 天"这一总时长。
- **推理加速**：核心是 MaskGIT 并行掩码生成把采样步数压到 12~48 步（对比自回归路线少一个量级）。**生成 1024 帧视频耗时（OpenReview rebuttal 披露）**：Phenaki 1.8B = **4.1 分钟**，对比 TATS-base 30 分钟、TATS-hierarchical 7.5 分钟（作者注明加速器可能不同，数字不完全可比）。
- 无量化/缓存/步数蒸馏等部署优化的披露。模型/代码/数据/demo **均未开源发布**（见伦理声明，因偏置与滥用风险暂不释放）。

## 评测 benchmark（把效果讲清楚）

### 文生视频（Kinetics-400，零样本，Table 1）
Phenaki 用 0.9B 模型、50%视频+50%图像训练，**零样本**评测（基线 NUWA 等在 K400 上 finetune 过）：

| 方法 | FID-Image ↓ | FID-Video ↓ |
| --- | --- | --- |
| T2V | 82.13 | 14.65 |
| SC | 33.51 | 7.34 |
| TFGAN | 31.76 | 7.19 |
| NUWA | 28.46 | 7.05 |
| **Phenaki [0-shot]** | 37.74 | **3.84** |

零样本下 FID-Video 显著最优（3.84 vs NUWA 7.05），FID-Image 略逊于在 K400 上 finetune 的基线——作者据此说"在没训练该数据集的情况下达到可比/更优"。

### C-ViViT 视频重建（Moments-in-Time，Table 3）
| 方法 | FID ↓ | FVD ↓ | Token 数 ↓ |
| --- | --- | --- | --- |
| Conv VQ-GAN | 7.5 | 306.1 | 2560 |
| Conv VQ-GAN + Video loss | 13.7 | 346.5 | 2560 |
| ViT VQ-GAN | **3.4** | 166.6 | 2560 |
| ViT VQ-GAN + Video loss | 3.8 | 173.1 | 2560 |
| **C-ViViT VQ-GAN (Ours)** | 4.5 | **65.78** | **1536** |

结论：per-frame 方法 FID 略好（图像级），但 C-ViViT 的 **FVD 碾压**（65.78 vs 166.6，时空动态远好）且 token 数最少（1536 vs 2560）——印证时空联合建模 + 时间压缩的价值。

### 视频预测（Phenaki 非为此设计，但仍有竞争力）
- **Kinetics-600（Table 4，5→11 帧）**：Phenaki FVD=36.4±0.19；优于 CogVideo(109.2)、Video Transformer(170)、DVD-GAN-FP(69.1)、Video VQ-VAE(64.3)、CCVS(55.0)，逊于 TrIVD-GAN-FP(25.7)、Transframer(25.4)、RaMViD(16.5)、Video Diffusion(16.2)。作者强调 Phenaki 缺 U-Net skip-connection 等视频预测专用结构却仍 competitive。
- **BAIR Robot Pushing（Table 5，单帧→15 帧）**：Phenaki FVD=97.0；处于中段（优于 DVD-GAN 109.8、VideoGPT 103.3，逊于 RaMViD 84.2、NUWA 86.9、MCVD 89.5）。

### 对 TATS 的补充对比（OpenReview rebuttal，UCF-101 类条件视频生成）
| 方法 | FVD ↓ |
| --- | --- |
| TATS | 332 |
| Phenaki (345M, 训练到 540K 步未收敛) | **250** |

作者用一个更小的 345M 模型（未训完）即超过 TATS，并预期完整训练差距更大。

### 关键消融
- **图文配比**（Table 2，见"数据"节）：纯视频 FVD 最好但对齐差；加图像改善对齐与图像 FID 但 FVD 退化，故选 80% 视频。
- **tokenizer 类型**（Table 3）：C-ViViT 的时空因果结构 + 视频感知损失带来 FVD 的数量级提升。

## 创新点与影响
**核心贡献：**
1. **C-ViViT**：首个"时空压缩 + 时间因果（自回归）+ 首帧独立编码"的离散视频 tokenizer，同时解决"变长"与"少 token"两难，且首帧独立设计让图像数据天然融入视频训练。
2. **首次提出 time-variable prompt（story）条件的视频生成**：用"编码末 K 帧 + 换 prompt + MaskGIT 续生"实现按剧本生成任意长（数分钟）连贯视频——开创**长视频 / 故事视频生成**范式。
3. **MaskGIT 并行掩码生成用于视频**：把采样步数压到 12~48 步，1.8B 生成 1024 帧仅 4.1 分钟，远快于自回归与扩散自回归扩展。
4. **图文+视频联合训练**实证：用海量图文弥补视频数据稀缺，把图像域概念（绘画风格等）迁移到视频。

**影响：** Phenaki 是离散 token + 掩码生成路线在视频上的代表作，与同期扩散路线（[[video-diffusion-models-vdm]]、Make-A-Video、Imagen Video）形成对照；其"变长 + 故事化 + 末帧续生"思路深刻影响后续长视频/可控视频生成研究，"video tokenizer 做时间压缩"也成为后来众多视频生成与视频理解工作的基础设计（如各类 video VAE/tokenizer）。ICLR 2023 接收（poster），评审认可方法新颖、结果"史无前例的灵活性"。

**已知局限：**
- **未开源**：模型/代码/数据/demo 均不释放（偏置与深伪滥用风险），复现受限——这也是评审扣分点之一。
- **分辨率与时长**：训练片段仅 1.4 秒 / 128×128 / 8 FPS，长视频靠自回归外推，质量随长度衰减；2 分钟示例用的还是"旧版本模型"。
- **写作清晰度、MaskGIT 超参消融不足**（评审 metareview 指出）。
- 文生视频当时**无统一 benchmark**，与 CogVideo(9B)/NUWA 等规模、数据、设置差异大，难公平横比。
- 安全过滤方法未公开，承认混入 LAION-400M 偏置。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2210.02399
- arxiv_pdf: https://arxiv.org/pdf/2210.02399
- openreview (ICLR 2023, 含 decision + rebuttal/runtime/TATS 对比): https://openreview.net/forum?id=vOEXS39nOF
- project_page (原始 demo，已被域名抢注，下为 2022-10 Wayback 快照): https://web.archive.org/web/20221014223332/https://phenaki.video/
- canonical demo (论文内引用，视频示例): https://phenaki.github.io/

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2210.02399.pdf
- ../../../sources/omni/2022/phenaki--openreview.md
- ../../../sources/omni/2022/phenaki--project-page.md
