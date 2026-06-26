---
title: "VideoGPT: Video Generation using VQ-VAE and Transformers"
org: "UC Berkeley"
country: US
date: "2021-04"
type: paper
category: video
tags: [video-generation, vq-vae, autoregressive, transformer, gpt, axial-attention, likelihood-based]
url: "https://arxiv.org/abs/2104.10157"
arxiv: "https://arxiv.org/abs/2104.10157"
pdf_url: "https://arxiv.org/pdf/2104.10157"
github_url: "https://github.com/wilson1yan/VideoGPT"
hf_url: ""
modelscope_url: ""
project_url: "https://wilson1yan.github.io/videogpt/index.html"
downloaded: [arxiv-2104.10157.pdf, videogpt--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
VideoGPT 把图像生成里成熟的 **VQ-VAE（离散化压缩）+ GPT（自回归 prior）** 两段式范式以最小改动迁移到视频：用带 3D 卷积和轴向注意力（axial attention）的 VQ-VAE 把视频压成时空离散 token，再用类 GPT 的 Sparse Transformer 自回归建模这些 token。它在 BAIR Robot Pushing 上取得 **FVD 103.3**（与当时 SOTA 的 GAN 模型 TrIVD-GAN-FP 持平），证明 likelihood-based 的 token 自回归路线在视频上同样可行，是一个极简、可复现的视频生成基线。

## 背景与定位
2021 年时，自然图像/音频/文本的生成建模都有显著进展，但**高保真自然视频**是少数没跟上的模态——视频需要同时建模空间和时间的相关性、输入维度极高、算力需求大。作者面临三个递进的设计选择，并把理由写得很明确：

1. **likelihood-based vs adversarial**：选 likelihood-based（而非 GAN）。理由不是"似然模型更好"，而是其训练目标明确、对 batch size 不敏感、易优化易评估，能让作者把精力集中在架构建模上而非训练稳定性上。
2. **在 likelihood 家族里选自回归**：自回归模型在离散数据上效果好、样本质量高（引 DALL-E），且有成熟的 Transformer 训练配方。
3. **在下采样的 latent 空间 vs 像素级建模**：选前者。自然图像/视频有大量时空冗余（这正是 JPEG/MPEG 压缩能工作的原因），4× 时空下采样可带来 64× 的分辨率缩减，把算力花在更少、更有用的比特上。VQ-VAE 已证明即便是有损解码器也能重建出足够真实的样本，这套路线当时刚被 DALL-E 用在文生图上验证。

由此得到 VideoGPT：**VQ-VAE + GPT 在视频上的最小适配**。它的定位不是刷 SOTA，而是给出一个"简单、易训练、可复现"的 Transformer 视频生成参考实现，对标当时复杂难复现的 VQ-VAE-2 多尺度层级方案和需要巨大采样开销的 Subscale Video Transformer。技术脉络上承接 [[vq-vae]]、[[image-gpt]]、[[dall-e-1]]（同期文生图离散 token 路线），并与 GAN 系（DVD-GAN、TrIVD-GAN、MoCoGAN）对照。

## 模型架构
整体是**两阶段、两个独立网络**（训练时先后训练，推理时先采 latent 再解码），见论文 Fig 2。

**阶段一：3D VQ-VAE（时空离散化压缩）**
- **编码器**：一系列在时空上做下采样的 **3D 卷积**，后接若干 **attention residual block**（论文 Fig 4）。注意力块用 LayerNorm + **轴向注意力（axial attention）**——把 3D 时空体积上的全注意力分解为沿 T、H、W 各轴分别做注意力，大幅降低复杂度。
- **解码器**：编码器的镜像——attention residual block 后接一系列 **3D 转置卷积**做时空上采样。
- **位置编码**：学习得到的**时空位置嵌入**，在编码器和解码器的所有轴向注意力层之间共享。
- **量化**：编码器输出经最近邻查表离散化到一个 codebook（码本）。BAIR 上码本大小 1024、embedding 维度 256；MNIST 用 512 码 ×64 维；UCF/TGIF 用 1024 码 ×256 维。论文主结果用**单码本**（消融显示单码本优于多码本，见下文）。
- 下采样配置依数据集而定：BAIR 在 H/W/T 三个维度各下采样 2×（latent 8×32×32）；MNIST 时空各 4×（latent 4×16×16，64× 总缩减）；UCF/TGIF latent 4×32×32。

**阶段二：类 GPT 自回归 prior（建模离散 latent 序列）**
- 把 VQ-VAE 编码得到的离散 latent 网格 flatten 成一维序列，用 **Image-GPT 架构**（标准 multi-head self-attention + pointwise MLP 前馈块）自回归建模 `p(x)=∏ p(xᵢ|x<ᵢ)`，目标是最大似然。
- 相对 Image-GPT 唯一改动：在前馈块和注意力块后**加 dropout 做正则**。
- 实际训练用 **Sparse Transformer**（Child et al. 2019）的跨时空 local + strided 稀疏注意力。
- prior 规模随数据集变化：BAIR 用 hidden 512、16 层、4 头、前馈 2048；UCF/TGIF 用 embedding 1024、20 层、8 头、前馈 4096。

**条件注入（conditional prior）**：VQ-VAE 本身无条件训练，但 prior 可做成条件模型，两种方式：
- **Cross Attention**（帧条件）：把条件帧先喂进一个 **3D ResNet**，再在 prior 训练时对 ResNet 输出做交叉注意力。用于以过去帧为条件的视频预测。
- **Conditional Norms**（动作/类别条件）：仿 GAN 的条件 BN，把 Transformer 里 LayerNorm 的 gain/bias 参数化为条件向量的仿射函数。用于 action-conditional 和 class-conditional 模型。

参数与分辨率：除 UCF-101 外，所有数据集都在 **64×64 分辨率、序列长 16 帧**上训练；**UCF-101** 同时训练了 64×64 和 **128×128**（短边缩到 128 后中心裁剪）。论文 Fig 1 展示 64×64 与 128×128 样本，UCF-101 的 128×128 样本见 Fig 7；TGIF 展示的是 64×64 样本（Fig 8）。

## 数据
论文用了多个数据集做训练/评测（无单一大规模预训练语料，每个数据集单独训练模型）：
- **Moving MNIST**：合成数据，做单帧条件的轨迹生成演示。
- **BAIR Robot Pushing**（Ebert et al. 2017）：主定量 benchmark，机器人臂推动物体，常用于视频预测，能考察物体-机器人交互、物体永久性、机械臂运动等。
- **ViZDoom**：作者**自行采集**——在 Health Gathering Supreme 和 Battle2 两个环境各训练策略并收集 rollout，共 **1000 条 length-100 轨迹**，按 8:1:1 划分 train/val/test。训练无条件与 action-conditioned 两种 prior。
- **UCF-101**（Soomro et al. 2012）：13,320 个视频、101 类动作分类数据集。训练无条件模型（64×64 和 128×128）。原视频短边缩到 128 后中心裁剪。论文坦承 VideoGPT **在 UCF-101 上严重过拟合**（train loss 3.40 / test loss 3.12），说明该数据集相对其复杂度而言太小。
- **TGIF（Tumblr GIF）**（Li et al. 2016）：103,068 个精选 GIF，约 **10 万小时视频**。是论文里最大、最复杂的自然视频集；这里**未过拟合**（train loss 2.87 / test loss 2.86），能捕捉镜头移动、场景切换、人物与物体动态。

**数据处理**：所有图像数据训练前缩放到 [−0.5, 0.5]。**未披露**美学过滤、安全过滤、re-captioning 或合成数据增广等——这是 2021 年的纯无条件/弱条件视频建模工作，没有文本-视频对，也无现代多模态数据流水线。

## 训练方法
**两阶段顺序训练**，不是端到端。

**阶段一 VQ-VAE 训练**（标准 VQ-VAE 目标）：
损失 `L = ‖x−D(e)‖² + ‖sg[E(x)]−e‖² + β‖sg[e]−E(x)‖²`，三项分别是重建损失、码本损失、commitment 损失（β=0.25）。其中码本更新用 **EMA（指数滑动平均）** 而非码本损失梯度——经验上收敛更快。几个稳定性 trick：
- **embedding 随机重启**（random restarts）+ 用编码器 latent 复制做码本初始化（沿用 Jukebox 的做法）；
- 用 **Normalized MSE**（MSE 除以数据集方差）做重建损失，发现能显著减少**码本坍缩（codebook collapse）**。

**阶段二 prior 训练**：在冻结的 VQ-VAE 编码出的离散 token 序列上，用**最大似然 / next-token 交叉熵**训练类 GPT Transformer。

**关键超参（附录 Table 8/9）**：
- VQ-VAE：batch 32、lr 7e-4、240 hidden units、128 residual units、4 residual layers（BAIR/UCF/TGIF）、训练 100K 步（MNIST 20K）。
- Prior（BAIR）：batch 32、lr 3e-4、16 层、512 embedding、2048 前馈、dropout 0.2、训练 150K 步；UCF/TGIF prior 训练 200K/600K 步、dropout 0.2。
- 梯度裁剪阈值 1。代码侧支持混合精度训练（README：`--amp_level O1 --precision 16`）。
- **未使用** RLHF/DPO/reward model/偏好对齐，也**未使用**一致性/LCM/步数蒸馏等加速——这些在 2021 年视频生成里都还没出现。自回归采样本身较慢（逐 token），论文未做采样加速。

## Infra（训练 / 推理工程）
- **算力极小**：论文明确所有结果用**最多 8 张 Quadro RTX 6000（24 GB）** 完成。这是该工作"极简、可复现"卖点的一部分——不需要大集群。
- 分布式：代码基于 PyTorch Lightning，支持多 GPU DDP（README `--gpus`、`--sync_batchnorm`）。
- 混合精度：支持 NVIDIA Apex O1 + fp16（`--amp_level O1 --precision 16`）。
- 稀疏注意力：可选 DeepSpeed 的 sparse attention（`DS_BUILD_SPARSE_ATTN=1`，`--attn_type sparse`），N 维 strided 稀疏布局，给受限算力场景用。
- **推理**：两步——先从 prior 自回归采一条 latent 序列，再用 VQ-VAE 解码器解成视频。自回归逐 token 采样是主要推理瓶颈，论文未报告吞吐/延迟数字。
- 部署：开源代码、Colab、HuggingFace Spaces（Gradio demo）。提供 `kinetics_stride2x4x4`、`kinetics_stride4x4x4` 等预训练 VQ-VAE checkpoint 可直接 `load_vqvae` 编解码。
- **GPU·时 / 具体吞吐 / 并行策略细节**：未披露。

## 评测 benchmark（把效果讲清楚）
评测指标：BAIR/Kinetics 用 **FVD（Fréchet Video Distance，越低越好）**，UCF-101 用 **Inception Score（IS，越高越好）**。

**BAIR Robot Pushing — FVD（Table 1，越低越好）**：
| 方法 | FVD ↓ |
|---|---|
| SV2P | 262.5 |
| LVT (Latent Video Transformer) | 125.8 |
| SAVP | 116.4 |
| DVD-GAN-FP | 109.8 |
| **VideoGPT (ours)** | **103.3** |
| TrIVD-GAN-FP | 103.3 |
| Video Transformer | 94 ± 2 |

VideoGPT 的 FVD 103.3 与当时最强 GAN（TrIVD-GAN-FP）打平，仅次于 Video Transformer（94），优于一众视频预测/GAN 基线。论文另报：用真实样本评测得 **FVD 103**，用 VQ-VAE 重建样本作参照得 **FVD\* 94**。论文坦言未达 SOTA，但样本质量已与最佳 GAN 竞争，且能从同一初始帧采出**多样化轨迹**（非简单复制数据）。

**UCF-101 — Inception Score（Table 2，越高越好）**：
| 方法 | IS ↑ |
|---|---|
| VGAN | 8.31 ± 0.09 |
| TGAN | 11.85 ± 0.07 |
| MoCoGAN | 12.42 ± 0.03 |
| Progressive VGAN | 14.56 ± 0.05 |
| TGAN-F | 22.91 ± 0.19 |
| **VideoGPT (ours)** | **24.69 ± 0.30** |
| TGANv2 | 28.87 ± 0.67 |
| DVD-GAN | 32.97 ± 1.7 |

VideoGPT 的 IS 24.69 超过多数早期 GAN，但落后 TGANv2 和 DVD-GAN（且如前述在 UCF-101 上过拟合）。

**消融研究（论文核心贡献之一，均在 BAIR 上）**：
- **VQ-VAE 轴向注意力有用**（Table 3）：加注意力使 NMSE 0.0041→0.0033、重建 FVD 15.3→14.9（已控制参数量公平对比）。
- **prior 越大越好**（Table 4）：Transformer 层数 2→4→8→16，bits/dim 单调降 2.84→2.52→2.39→2.05；FVD 在 8 层左右饱和（120.4→110.0→103.3→103.6）。8 层是性价比点。
- **时空均衡下采样最佳**（Table 5）：在 latent 总数相同时，2×2×2 均衡下采样（latent 8×32×32）样本质量最好（FVD 103.6），优于只在空间或只在时间下采样；整体最佳甜点也在 8×32×32 附近——latent 太大重建好但 prior 受算力限制采样差，太小则重建瓶颈。
- **码本数量增大无助于样本质量**（Table 6）：码数 256/1024/4096，重建 R-FVD 改善（18.2→14.9→11.3）但 FVD 几乎不变（≈103.8/103.6/103.9）——BAIR 上 256 码已过阈值。
- **单码本优于多码本**（Table 7）：在 latent 空间总大小固定下，码本数 1/2/4/8，FVD 103.6→106.3→131.4→135.7、bits/dim 2.05→2.41→2.68→2.97，单码本最佳；作者推测多码本可能在更大数据集或不同架构下才显出优势。

VideoGPT 还展示了 **action-conditional**（BAIR、ViZDoom）和单帧条件（Moving MNIST、BAIR）的定性能力，能捕捉复杂 3D 相机运动与环境交互。

## 创新点与影响
**核心贡献**：
1. **首个简洁、可复现的 VQ-VAE 视频生成范式**：把"离散化 + 自回归 prior"这条文生图（[[dall-e-1]]）刚验证的路线干净地搬到视频，证明 likelihood-based token 生成在自然视频上可行，质量与同期最佳 GAN 竞争。论文 Related Work 明确点出 VQ-VAE-2（多尺度层级 + SNAIL）复杂难复现，故选单尺度离散 latent + Transformer prior，"这一设计选择也被 DALL-E 采用"。
2. **3D VQ-VAE + 轴向注意力**的时空压缩设计，及其上的系统性消融（注意力、latent 尺寸、时空下采样比、码本数/码本数量），为后续视频 tokenizer 设计提供了经验依据。
3. **极低门槛**：≤8 张 RTX 6000、开源代码 + Colab + HF Spaces，刻意做成"最小参考实现"。

**影响**：VideoGPT 成为离散 token + 自回归视频生成的经典基线，被后续 [[cogvideo]]、[[nuwa]]、[[maskvit]]、[[magvit]] 等大量"视频 tokenizer + 序列模型"工作引用和对照；它确立的两阶段（视频 VQ tokenizer → 序列 prior）思路，也是后来 MAGVIT/MAGVIT-v2 这类视频生成 tokenizer 和自回归/掩码生成路线的直接前身之一。

**已知局限**（作者明确指出）：
- **未达 SOTA**，BAIR 上略逊 Video Transformer，UCF-101 IS 落后 DVD-GAN。
- **小数据易过拟合**（UCF-101），需更大数据集验证 scaling。
- 主结果分辨率低（64×64，部分 128×128），序列短（16 帧），未做文本条件。
- 自回归逐 token 采样慢，论文未做采样加速。
- 多码本/更大 latent 的潜力受当时算力限制未充分释放。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2104.10157
- arxiv_pdf: https://arxiv.org/pdf/2104.10157
- github: https://github.com/wilson1yan/VideoGPT
- project_page (samples/website): https://wilson1yan.github.io/videogpt/index.html
- paper-repro repo（论文复现代码，非主仓）: https://github.com/wilson1yan/VideoGPT-Paper
- HF Spaces demo: https://huggingface.co/spaces/akhaliq/VideoGPT

## 一手源存档（sources/）
- [arxiv-2104.10157.pdf](https://arxiv.org/pdf/2104.10157)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2021/videogpt--readme.md)
