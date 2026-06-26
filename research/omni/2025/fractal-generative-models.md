---
title: "Fractal Generative Models (FractalGen)"
org: "MIT CSAIL / Google DeepMind（何恺明组）"
country: US
date: "2025-02"
type: paper
category: method
tags: [fractal, autoregressive, mar, pixel-by-pixel, image-generation, imagenet, divide-and-conquer, likelihood]
url: "https://arxiv.org/abs/2502.17437"
arxiv: "https://arxiv.org/abs/2502.17437"
pdf_url: "https://arxiv.org/pdf/2502.17437"
github_url: "https://github.com/LTH14/fractalgen"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2502.17437.pdf, fractal-generative-models--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
FractalGen 提出"分形生成模型"这一**新的模块化抽象层次**——把"一个完整的生成模型"本身当作原子模块，递归地在生成模型里调用同类生成模型，形成跨层级自相似的分形架构；以自回归模型为原子模块实例化后，**首次实现了对高分辨率（256×256）图像逐像素（pixel-by-pixel）建模**，在 ImageNet 64×64 无条件似然达到 **3.14 bits/dim**（远超此前最佳 AR 的 3.40），256×256 类条件生成 FractalMAR-H 达 **FID 6.15 / IS 348.9**，单张 H100 平均 1.29 秒/图。

## 背景与定位
逐像素图像生成是生成建模的一块硬骨头：图像是 N=H×W×3 个像素的高维联合分布，且像素之间**没有天然的一维序列顺序**。此前把它当作长序列建模的工作（Sparse/Routing/Combiner Transformer、Perceiver AR、[[megabyte]] 等）受限于注意力的二次复杂度，在 64×64 上勉强能做似然估计、却几乎生成不出像样的图，更无法扩到 256×256（约 20 万像素）。主流绕过办法是先用 tokenizer/VAE 把图压到隐空间再建模（[[vqvae]]、[[latent-diffusion-ldm]]、[[taming-transformers-vqgan]]），但这会引入**重建误差天花板**。

FractalGen 的切入点是：自然图像具有**近分形（near-fractal）/多尺度自相似**结构——"图像由子图像组成，子图像本身又是图像"，因此"图像生成模型应当由本身也是图像生成模型的子模块组成"。作者把这一观察上升为**新的模块化原语**：以往模块化的粒度是"层"（残差块、Transformer 块）或"把扩散模型当作一个 token 的分布模块"（[[mar]]，本文同组前作）；本文则把**整个生成模型**当作原子模块递归复用。这与数学分形（Mandelbrot 的"生成器 generator"递归规则）、生物神经网络的尺度不变小世界结构相呼应，故命名为 fractal generative model。

与 FractalNet（Larsson 2016，递归卷积块做超深分类网络）的区别有两点：(1) FractalGen 的模块是**整个生成模型**而非卷积小块，是更高层次的模块化；(2) FractalNet 面向分类只输出低维 logits，而 FractalGen 利用分形的**指数级输出扩张**生成上百万像素。与"尺度空间自回归"（[[var]]、HART、Infinity）的区别：后者用**单个** AR 模型逐尺度预测、且在每个尺度上对整张 token 序列做全注意力（256×256 末尺度注意力矩阵 ≈ 4.29×10⁹），而 FractalGen 用**分治+递归子模块**，最细层只在 4×4 小 patch 内做注意力（总量 ≈ 1.05×10⁶），**在最细分辨率上算力效率高约 4000×**，这正是首次能逐像素建高分辨率图的关键。

## 模型架构
**核心抽象——分形生成器（fractal generator）。** 形式化定义：生成器 gᵢ 规定如何从上一层的一个输出 xᵢ 产生下一层的一组新数据 {xᵢ₊₁} = gᵢ(xᵢ)。每一层从单一输入产生多个输出，于是**层数线性增长 → 输出指数增长**，特别适合用很少的层数建模超高维数据。

**分治分解。** 设每层 AR 的序列长度为可控常数 k，总变量数 N = kⁿ，则递归层数 n = logₖ(N)。第一层把联合分布拆成 k 个子集（各含 kⁿ⁻¹ 个变量）：p(x₁,…,x_{kⁿ}) = Π p(子块 | 前缀块)，每个条件分布交给下一层 AR 建模，递归到底。这样用 n 层、每层长度仅 k 的 AR，就能高效建模 kⁿ 个变量的联合分布。

**逐像素实例化（4 个分形层）。** 以 256×256 为例：
- g₁（序列长 256）：把整图切成 16×16 个 patch（每 patch 16×16 像素），建模 patch 间依赖；
- g₂（序列长 16）：在每个 16×16 patch 内切成 4×4 个子 patch（每子 patch 4×4 像素）；
- g₃（序列长 16）：在每个 4×4 patch 内建模 16 个像素间依赖；
- g₄（序列长 3）：用极轻量 Transformer **逐通道自回归**地建模单像素的 RGB，对 0–255 的离散整数施加 **256-way 交叉熵**。

每个 AR 模块的输入 = 上一层生成器的输出（作为一个独立 token，置于序列最前）+ 当前图像 patch 切块嵌入；输出是给下一层各生成器的一组条件。为控制算力，**越往细层 width 与层数越小**（小 patch 更易建模）。大模型各层配置（IN256，来自论文 Table 1）：g₁/g₂/g₃/g₄ 的层数 = 32/8/4/1，hidden dim = 1024/512/256/64，参数量 ≈ 403M/25M/3M/0.1M，单样本前向 GFLOPs = 215/208/419/22。**关键结论：建 256×256 的总算力仅为建 64×64 的约 2 倍**（分形设计把分辨率提升的成本摊薄了）。

**两种原子 AR 变体（沿用 [[mar]] 的设计空间）：**
- **FractalAR**：raster-scan 顺序的 GPT 式因果 Transformer，可用 KV-cache 加速；
- **FractalMAR**：随机顺序的 BERT 式双向 Transformer（masked AR），双向注意力更契合图像、且能并行预测多个 patch，计算更高效；条件生成实验主用此变体。

**Backbone/Tokenizer/Text encoder：** 纯 Transformer 堆叠；**无 visual tokenizer、无 VAE、无 VQ**（直接在原始 RGB 像素上端到端训练，因此天然没有重建误差天花板）；类条件用 class token 注入，**无 T5/CLIP/LLM 文本编码器**（任务是类条件 ImageNet，非文生图）。模型规格：FractalAR/MAR(IN64) 432M；FractalMAR-B/L/H(IN256) = 186M/438M/848M。

## 数据
- **数据集：** 仅 **ImageNet**（Deng 2009），分辨率 64×64 与 256×256；做无条件与类条件生成。
- **训练数据形态：** 直接喂**原始图像像素**端到端训练，无 tokenizer 预处理、无 re-captioning、无合成数据、无美学/安全过滤管线——这是纯方法学论文，不涉及大规模图文对或数据配比工程。
- **规模/配比/清洗：** 未涉及（标准 ImageNet 训练集，未做额外数据工程披露）。

## 训练方法
- **训练目标：** 全程 **next-token / 离散自回归** 范式——RGB 通道当作 0–255 离散值，末层施 **256-way 交叉熵**；损失从最底层逐像素反传穿过**所有分形层**，端到端联合训练（breadth-first 遍历分形架构）。**不用 diffusion / flow matching**（这是与同组 [[mar]] 最大的方法差异：MAR 末端是扩散损失建模连续 token，FractalGen 末端是逐像素离散交叉熵）。
- **优化器/调度：** AdamW（wd=0.05，β=(0.9, 0.95)）；默认训 **800 epoch**（FractalMAR-H 训 600 epoch）；base lr = 5e-5（按 batch/256 线性缩放），40 epoch 线性 warmup 后接 cosine 衰减；batch size = 2048(IN64) / 1024(IN256)；attn_dropout=0.1、proj_dropout=0.1（见 README 训练脚本）。
- **关键 trick：**
  - **Guiding pixel（仅 IN256）：** 每个生成器先用上一层输出预测当前输入图块的**平均像素值**，再把它作为额外条件——让每层"先有全局上下文再画细节"，对高分辨率略有帮助。
  - **邻域条件（缓解 patch 边界 artifact）：** 给下一层生成器不仅喂当前 patch 的输出，还喂**周围 4 个 patch**的输出，显著减少切块导致的边界不连续。
  - **CFG（类条件）：** 训练时 10% 样本把类标签替换为 dummy token；推理用 l = lᵤ + ω·(l_c − lᵤ)，第一层用 linear CFG schedule；并配 temperature 缩放（各模型扫超参取最优）。
  - **CFG 数值稳定：** 概率极小的像素值会让 CFG 数值不稳——在 CFG 前对条件 logits 施 **top-p=0.0001** 截断。
- **蒸馏/加速：** 未做步数蒸馏（consistency/LCM/ADD 等）；加速来自架构本身的分治（见 Infra）。

## Infra（训练 / 推理工程）
- **训练硬件：** README 注明训练脚本在 **4×8 = 32 张 H100** 上跑通；分布式用 **PyTorch DDP（torchrun，多机多卡）**，并开 `--grad_checkpointing`（梯度检查点省显存）。算力获得致谢 Google TPU Research Cloud(TRC) 与 Google Cloud Platform。具体 GPU·时未披露。
- **推理：** 逐像素生成按 **depth-first** 遍历分形架构。FractalAR 可用 **KV-cache**；FractalMAR 用双向注意力**并行预测多 patch**，更快。**吞吐：FractalMAR-H 在单张 Nvidia H100 PCIe、batch=1024 下平均 1.29 秒/图**（256×256）。
- **算力效率（核心工程卖点）：** 最细分辨率注意力量从尺度空间 AR 的 ~4.29×10⁹ 降到 ~1.05×10⁶，**约 4000× 更省**；3 层分形（IN64）单前向 438 GFLOPs，而 2 层方案 5516 GFLOPs、全长单 AR 约 29845 GFLOPs（且后者训练根本不可行）——即**层数越多反而算力越省、似然越好**（论文 Table 2）。
- **量化/部署：** 未披露。

## 评测 benchmark（把效果讲清楚）

**1) 似然估计（ImageNet 64×64 无条件，NLL bits/dim，越低越好）**

分形层数消融（Table 2）——更多层既更省算力又更好：

| 方法 | 序列长 (g₁/g₂/g₃) | GFLOPs | NLL↓ |
|---|---|---|---|
| AR / MAR, full-length | 12288 | 29845 | 训练不可行(N/A) |
| AR, 2-level | 4096/3 | 5516 | 3.34 |
| MAR, 2-level | 4096/3 | 5516 | 3.36 |
| **FractalAR (3-level)** | 256/16/3 | **438** | **3.14** |
| **FractalMAR (3-level)** | 256/16/3 | **438** | **3.15** |

与其他似然模型对比（Table 3）：iDDPM 3.53、VDM 3.40、Flow Matching 3.31、NFDM 3.20（扩散类）；PixelRNN 3.63、PixelCNN 3.57、Sparse Transformer 3.44、Routing Transformer 3.43、Combiner AR 3.42、Perceiver AR 3.40、MegaByte 3.40（AR 类）。**FractalAR 3.14 / FractalMAR 3.15**——比此前最佳 AR（3.40）大幅领先，且优于多数扩散模型、逼近最强扩散变体。

**2) 类条件生成质量（ImageNet 256×256，Table 4）** — FractalMAR 是表中**唯一逐像素**框架：

| 模型 | 类型 | #params | FID↓ | IS↑ | Pre.↑ | Rec.↑ |
|---|---|---|---|---|---|---|
| FractalMAR-B | fractal | 186M | 11.80 | 274.3 | 0.78 | 0.29 |
| FractalMAR-L | fractal | 438M | 7.30 | 334.9 | 0.79 | 0.44 |
| **FractalMAR-H** | fractal | 848M | **6.15** | **348.9** | 0.81 | 0.46 |
| （参考）BigGAN-deep | GAN | 160M | 6.95 | 198.2 | 0.87 | 0.28 |
| （参考）StyleGAN-XL | GAN | 166M | 2.30 | 265.1 | 0.78 | 0.53 |
| （参考）ADM | diffusion | 554M | 4.59 | 186.7 | 0.82 | 0.52 |
| （参考）VDM++ | diffusion | 2B | 2.12 | 267.7 | – | – |
| （参考）JetFormer | AR+flow | 2.8B | 6.64 | – | 0.69 | 0.56 |

**清晰的 scaling 趋势：** 186M→848M 时 FID 从 11.80→6.15、Recall 从 0.29→0.46。**IS（348.9）与 Precision（0.81）很强**（保真/细节好），但 **FID/Recall 偏弱、多样性不足**——作者归因于逐像素建近 20 万像素的极端难度，且因无 tokenizer 而无重建上限、预期继续 scale 可缩小 FID/Recall 差距。

**3) 类条件 ImageNet 64×64（Table 5，FID↓）：** FractalAR 5.30、**FractalMAR 2.72**；对比 iDDPM 2.92、MAR 2.93、StyleGAN-XL 1.51、Consistency Model 4.70。FractalMAR 已与经典强模型同档。（与 README 提供的 checkpoint 指标一致：FractalAR-IN64 FID 5.30 / IS 56.8；FractalMAR-IN64 FID 2.72 / IS 87.9。）

**4) 关键消融：**
- **AR vs MAR：** MAR 整体优于 AR（IN64 条件 FID 2.72 vs 5.30），故 256×256 主用 MAR。
- **像素通道顺序（Table 6，IN64 训 400 epoch）：** RGB/GRB/BGR 的 NLL 均 ≈3.17 几乎无差；FID 略有差异（G→R→B 3.14、R→G→B 3.15、B→R→G 3.32、YCbCr 3.55）——因 Inception 网络对红绿通道更敏感；总体顺序鲁棒。
- **最优 CFG（IN256）：** FractalMAR-B 用 cfg=29.0、L 用 21.0、H 用 19.0 取得最佳 FID（见 README）。

**5) 条件逐像素预测（定性，Fig.5/8）：** 支持 inpainting / outpainting / uncropping / **类条件编辑**（如按狗的类标签把猫脸替换成狗脸），展示了像素级可控、可交互编辑能力——无需为编辑任务单独训练。

## 创新点与影响
**核心贡献：**
1. **提出"分形生成模型"这一新抽象层次**——把整个生成模型递归地当作原子模块复用，产生跨层级自相似架构；这是继"层→块→（MAR）把扩散当 token 分布模块"之后又一次模块化升维。
2. **用分治把高维非序列数据的联合分布递归拆解**，使输出随层数指数增长、算力随层数线性增长，**首次让高分辨率（256×256）逐像素图像生成在算力上可行**（最细层注意力省约 4000×）。
3. **无 tokenizer、无 VAE、端到端原始像素建模**，规避了隐空间方法的重建误差天花板，给出"可解释、逐元素"的生成过程（更接近人类可理解，便于可控编辑）。
4. **强实证：** IN64 似然 3.14 bits/dim（AR SOTA）、IN256 逐像素 FID 6.15，并展现清晰 scaling 趋势。

**更广意义：** 作者强调像素生成只是 testbed——分形分治范式天然适配**任何具有内在结构、可分治、跨尺度自相似的非序列数据**（分子构象、蛋白质、生物神经网络等），暗示其潜在的跨域通用性。代码、4 个预训练模型与 Colab demo 全部开源。

**已知局限：**
- **多样性偏弱**：FID/Recall 相对扩散/GAN SOTA 仍有差距（256×256 FID 6.15 vs SiD2 1.38、VDM++ 2.12），逐像素建近 20 万像素是根因。
- **推理仍偏慢**：1.29 秒/图（H100，逐像素深度优先），相比一次性出图的扩散/单步蒸馏模型慢。
- **仅在 ImageNet 类条件设定验证**：未做文生图、未接文本编码器、未在更大数据/更高分辨率上扩展；非序列数据的跨域潜力仍是 future work。
- 未做步数/采样蒸馏，加速完全依赖架构分治。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2502.17437
- arxiv_pdf: https://arxiv.org/pdf/2502.17437
- github: https://github.com/LTH14/fractalgen
- colab_demo: http://colab.research.google.com/github/LTH14/fractalgen/blob/main/demo/run_fractalgen.ipynb

## 一手源存档（sources/）
- [arxiv-2502.17437.pdf](https://arxiv.org/pdf/2502.17437)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/fractal-generative-models--readme.md)
