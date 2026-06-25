---
title: "Scalable Diffusion Models with Transformers (DiT)"
org: "UC Berkeley / New York University (Meta AI FAIR)"
country: US
date: "2022-12"
type: paper
category: method
tags: [dit, diffusion-transformer, latent-diffusion, adaln-zero, scaling, imagenet, backbone, vit]
url: "https://arxiv.org/abs/2212.09748"
arxiv: "https://arxiv.org/abs/2212.09748"
pdf_url: "https://arxiv.org/pdf/2212.09748"
github_url: "https://github.com/facebookresearch/DiT"
hf_url: "https://huggingface.co/spaces/wpeebles/DiT"
modelscope_url: ""
project_url: "https://www.wpeebles.com/DiT"
downloaded: [arxiv-2212.09748.pdf, dit-scalable-diffusion-transformers--readme.md, dit-scalable-diffusion-transformers--project.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
把潜空间扩散模型（[[latent-diffusion-ldm]]）里那个"理所当然"的卷积 U-Net backbone 整个换成一个标准 Vision Transformer（DiT），证明 U-Net 的归纳偏置并非必需，且 **FID 随模型 Gflops 单调下降**（相关系数 −0.93）；最大的 DiT-XL/2（118.6 Gflops）在 ImageNet 256×256 类条件生成上拿到 **FID 2.27** 的当时 SOTA，512×512 上 FID 3.04，成为后来 MMDiT/SD3、PixArt、Hunyuan-DiT、Lumina、Sora 等几乎所有现代扩散 Transformer 的架构祖先。

## 背景与定位
2020–2022 年扩散模型（[[ddpm]] → [[improved-ddpm]] → [[diffusion-models-beat-gans]] → [[latent-diffusion-ldm]]）在图像生成上全面超越 GAN，但**所有这些模型的 backbone 都是从 PixelCNN++ 继承来的卷积 U-Net**（ResNet 块 + 低分辨率处插入的自注意力块）。与此同时，Transformer 已在语言、视觉（ViT）、RL 等几乎所有领域取代了领域专用架构，并展现出极好的"模型/算力/数据"三轴 scaling 性质——唯独图像级扩散生成仍是 Transformer 的"钉子户"。

DiT 的核心问题是：**U-Net 或卷积本身，对扩散模型是否不可或缺？** 论文的回答是否定的。它在 LDM 框架内（即在冻结 VAE 的潜空间里训练扩散模型）把 U-Net 直接替换为标准 Transformer，用 **Gflops 而非参数量**作为复杂度度量（参数量是图像模型复杂度的差代理，因为它不反映分辨率/token 数），系统性地刷遍 DiT 设计空间，给出"架构去神秘化 + 可复用的 scaling 经验基线"。前置最相关工作是 Nichol & Dhariwal 对 U-Net 类做的 Gflop/scaling 分析（[[improved-ddpm]] / [[diffusion-models-beat-gans]]），DiT 把同样的视角搬到 Transformer 类上。

论文中稿 ICCV 2023（Oral）。第一作者 William Peebles 此工作为 Meta AI FAIR 实习期间完成，后成为 OpenAI Sora 团队负责人之一。

## 模型架构
**Backbone：纯 Transformer（基于 ViT），无卷积、无 U-Net 跳连。** 整体管线是"现成卷积 VAE + Transformer 扩散模型"的混合体。

- **潜空间 / VAE**：直接用 Stable Diffusion 的现成预训练 VAE（LDM 的 "f8" 模型），下采样因子 8——256×256×3 图像编码为 32×32×4 的潜表示 z，扩散始终在此 Z-space 进行，采样后用 VAE 解码器还原像素。VAE 共 84M 参数（不计入 DiT 的参数/Flop 统计）。DiT 也可不加修改地直接作用于像素空间，但出于算力效率选择潜空间。
- **Patchify（token 化）**：DiT 第一层把 I×I×C 的噪声潜表示切成 p×p 的 patch，线性嵌入为 T=(I/p)² 个 d 维 token，再加 ViT 的标准 sine-cosine 频率位置编码。patch size **p∈{2,4,8}**：减半 p 会让 token 数翻 4 倍、Gflops 至少翻 4 倍，但**几乎不改变参数量**——这是后文"算力而非参数才是关键"论点的实验杠杆。
- **条件注入（四种 block 设计，关键消融）**：扩散模型要吃 timestep t 和类别标签 c。论文比较四种把条件塞进 ViT block 的方式：
  1. **In-context**：把 t、c 的嵌入当成两个额外 token 拼进序列（类似 cls token），最后一层后丢掉。几乎不增 Gflops。
  2. **Cross-attention**：把 t、c 拼成长度 2 的序列，在自注意力后加一层 multi-head cross-attention（类似原版 Transformer / LDM 的条件方式）。Gflops 开销最大，约 +15%。
  3. **adaLN（adaptive layer norm）**：不直接学 LayerNorm 的 scale γ / shift β，而是从 t+c 的嵌入和**回归**出 γ、β。Gflops 增量最小、最省算力，但对所有 token 施加同一函数。
  4. **adaLN-Zero（最终采用）**：在 adaLN 基础上**额外回归一组逐维缩放系数 α**，作用在每个残差连接之前；并把回归 α 的 MLP **零初始化**，使每个 DiT block 初始即为恒等函数（借鉴 ResNet/扩散 U-Net 的零初始化加速大规模训练的做法）。
  
  结论：**adaLN-Zero 在所有训练阶段都显著优于其余三者**——400K 步时其 FID 几乎是 in-context 的一半；且初始化很重要，adaLN-Zero 明显胜过 vanilla adaLN。全文后续模型一律用 adaLN-Zero。
- **DiT block 实现细节**：timestep 用 256 维频率嵌入 + 两层 MLP（SiLU 激活，维度 = hidden size）；每个 adaLN 层把 t、c 嵌入之和过 SiLU + 线性层，输出维度为 hidden size 的 **4×（adaLN）或 6×（adaLN-Zero）**（即 γ/β/α 各一份）；核心 Transformer 用 tanh 近似的 GELU。
- **Transformer decoder（输出头）**：最后一层（带 adaLN 的）LayerNorm 后，线性解码每个 token 到 p×p×2C，重排回原始空间布局，得到**噪声预测 + 对角协方差预测 Σ**（沿用 ADM 的学习协方差方案）。
- **模型规模（沿用 ViT 配置）**：四档联合缩放深度 N / 宽度 d / 头数——

| Config | Layers N | Hidden d | Heads | 参数量 | Gflops (I=32, p=4) |
|---|---|---|---|---|---|
| DiT-S | 12 | 384 | 6 | 33M | 1.4 |
| DiT-B | 12 | 768 | 12 | 130M | 5.6 |
| DiT-L | 24 | 1024 | 16 | 458M | 19.7 |
| DiT-XL | 28 | 1152 | 16 | 675M | 29.1 |

  命名约定 DiT-XL/2 = XLarge 配置 + patch size 2。DiT-XL/2 在 256×256 上 token 数 = (32/2)²=256，Gflops=118.6；512×512 上潜表示 64×64×4、p=2 → 1024 token、Gflops=524.6。整个设计空间 = {patch size} × {block 设计} × {模型规模}。

## 数据
- **训练集**：**ImageNet**（类条件，1000 类），256×256 与 512×512 两种分辨率。这是纯类条件生成 benchmark，不涉及文本，也不涉及网络爬取图文对。
- **数据增广**：**仅水平翻转**，无其他增广。
- **清洗 / re-caption / 合成数据**：不适用（ImageNet 标注现成，无文本标注、无 re-captioning、无合成数据、无美学/安全过滤环节）。DiT 是方法/架构论文，数据维度刻意保持极简以隔离"架构"这一变量。

## 训练方法
- **训练目标**：标准 DDPM。沿用 ADM（[[diffusion-models-beat-gans]]）的做法——噪声预测网络 ε_θ 用简单 MSE 损失 L_simple = ‖ε_θ(x_t) − ε‖²；同时学习反向过程的协方差 Σ_θ，用完整变分下界 L（含 D_KL 项）训练 Σ。报告的训练损失曲线即"噪声 MSE + D_KL"之和。无 flow matching、无 rectified flow（这些是 DiT 之后才被后继工作如 SD3 引入潜空间 Transformer 的）。
- **采样与引导**：[[classifier-free-guidance]]（CFG）——训练时随机 dropout 条件 c 换成可学习的 "null" 嵌入 ∅；推理时 ε̂ = ε(x_t,∅) + s·(ε(x_t,c) − ε(x_t,∅))，s>1。一个有趣的工程细节：**最终结果用的 CFG 只施加在潜表示的前 3 个通道**（而非全部 4 通道），论文发现三通道引导 scale=(1+x) 可被四通道 scale=(1+¾x) 很好地近似、二者效果相当（三通道 scale=1.5 → FID 2.27；等价的四通道 scale=1.375 → FID 2.20，四通道反而略低，论文称"对元素子集施加引导仍能取得不错效果"颇有意思，留作 future work）。
- **单阶段、无多阶段后训练**：纯从头训练，**没有** continue-pretrain / SFT / RLHF / DPO / reward model / 蒸馏。EMA 权重衰减 0.9999，所有报告结果用 EMA 模型。
- **超参（全配置共享，几乎照搬 ADM）**：AdamW，**恒定学习率 1e-4，无 weight decay，batch size 256**，无 lr warmup、无正则化。作者强调即便没有 warmup/正则，**训练在所有规模上都极稳定，未见 Transformer 常见的 loss spike**——这是 DiT"可直接继承 ViT 训练配方"的有力证据。未调 lr / decay / warmup / Adam β / weight decay。
- **采样步数**：对比 SOTA 时用 250 步 DDPM；scaling 分析用 [16,32,64,128,256,1000] 步做消融。
- **scaling 关键发现（训练侧）**：增大 DiT 的 Gflops（无论靠加深加宽还是减小 patch 增 token）都让**训练损失下降更快、收敛到更低值**——与语言模型 scaling 规律一致。

## Infra（训练 / 推理工程）
- **原始训练（论文）**：JAX 实现，在 **TPU-v3 pod** 上训练。最重的 DiT-XL/2 在 **TPU v3-256 pod** 上约 **5.7 iter/s**（global batch 256）。
- **训练算力 / 时长**：256×256 的 DiT-XL/2 最终训到 **7M 步**（即便只训 2.35M 步、与 ADM 相当时仍达 FID 2.55，已超所有前作）；512×512 训到 **3M 步**。两个 XL/2 模型作者称"FID 从未饱和，尽可能一直训"。训练算力估计公式：model Gflops × batch × steps × 3（×3 近似反传约为前传 2 倍）。
- **算力效率（vs U-Net 基线）**：DiT-XL/2 在 256×256 仅 **118.6 Gflops**，远低于像素空间 U-Net 的 ADM（1120 Gflops）、ADM-U（742 Gflops），也略低于潜空间 LDM-4（103.6 Gflops）但 FID 更好；512×512 上 XL/2 仅 524.6 Gflops vs ADM 1983 / ADM-U 2813 Gflops。**结论：大 DiT 比小 DiT 更省算力**——小模型即便训更久最终也会变得算力低效（XL/2 在约 10¹⁰ Gflops 后超过 XL/4）。
- **推理侧 scaling**：增加采样步数**无法弥补模型算力的不足**——DiT-L/2 用 1000 步（80.7 Tflops/图）的 FID-10K=25.9，仍输给 DiT-XL/2 用 128 步（15.2 Tflops/图，5× 更省）的 23.7。
- **官方开源工程（GitHub README）**：原模型 JAX/TPU 训练，发布的权重直接从 JAX 移植到 PyTorch；PyTorch DDP 训练脚本，复现实验用 **8× A100 训 XL/2、4× A100 训 B/4**，与 JAX 结果相当（XL/2 400K 步 JAX FID 19.5 vs PyTorch 18.1，更好）。提醒 A100 用户在脚本顶部开启 TF32 matmul 大幅加速。移植后 FP32 重测甚至略优于论文（**2.21 vs 2.27 FID**）。社区衍生 `fast-DiT` 加入梯度检查点、混合精度、预抽 VAE 特征，单张 A100 即可 0.84 step/s 训 DiT-XL/2。README 列为"待加"的优化包括 Flash Attention、torch.compile、AMP/bf16——**原版未用这些**。
- **部署形态**：开源 PyTorch 权重（256/512 两档 DiT-XL/2，CC-BY-NC）、HF Space、Colab、Replicate；并已并入 HuggingFace `diffusers` 的 DiT pipeline。

## 评测 benchmark（把效果讲清楚）
评测协议：FID-50K，250 步 DDPM 采样，导出样本后用 **ADM 的 TensorFlow 评测套件**计算（保证可比），辅以 sFID、Inception Score、Precision/Recall。

**ImageNet 256×256 类条件（带 CFG，源：论文 Table 2）**

| 模型 | FID↓ | sFID↓ | IS↑ | Prec↑ | Rec↑ |
|---|---|---|---|---|---|
| BigGAN-deep | 6.95 | 7.36 | 171.4 | 0.87 | 0.28 |
| StyleGAN-XL | 2.30 | 4.02 | 265.1 | 0.78 | 0.53 |
| ADM-G, ADM-U | 3.94 | 6.14 | 215.8 | 0.83 | 0.53 |
| LDM-4-G (cfg=1.50) | **3.60**（前 SOTA） | – | 247.7 | 0.87 | 0.48 |
| DiT-XL/2（无引导） | 9.62 | 6.85 | 121.5 | 0.67 | 0.67 |
| DiT-XL/2-G (cfg=1.25) | 3.22 | 5.28 | 201.8 | 0.76 | 0.62 |
| **DiT-XL/2-G (cfg=1.50)** | **2.27** | 4.60 | 278.2 | 0.83 | 0.57 |

把扩散模型前 SOTA（LDM 3.60）刷到 **2.27**，并在所有 CFG scale 下 recall 都高于 LDM-4/LDM-8。

**ImageNet 512×512 类条件（带 CFG，源：论文 Table 3）**

| 模型 | FID↓ | sFID↓ | IS↑ | Prec↑ | Rec↑ |
|---|---|---|---|---|---|
| StyleGAN-XL | 2.41 | 4.06 | 267.8 | 0.77 | 0.52 |
| ADM-G, ADM-U | **3.85**（前 SOTA） | 5.86 | 221.7 | 0.84 | 0.53 |
| **DiT-XL/2-G (cfg=1.50)** | **3.04** | 5.02 | 240.8 | 0.84 | 0.54 |

512×512 上把 ADM-U 的 3.85 刷到 **3.04**。

**关键消融结论（抠数字）**：
- **条件注入**：DiT-XL/2 在 400K 步（无引导）下，in-context 35.24 / cross-attn 26.14 / adaLN 25.21 / **adaLN-Zero 19.47**（论文 Table 4）——adaLN-Zero 完胜。
- **Gflops ↔ FID 强相关**：12 个模型（S/B/L/XL × p=8/4/2）在 400K 步的 FID 与 Transformer Gflops 相关系数 **−0.93**；Gflops 相近的不同配置（如 DiT-S/2 与 DiT-B/4）FID 也相近——**算力而非参数决定质量**（减小 patch 时参数几乎不变甚至略降，但 Gflops 与 FID 都大幅改善）。Inception Score、Precision 受规模提升尤其明显。
- **VAE 解码器消融**（Table 5，256×256，cfg=1.5）：original 2.46 / ft-MSE 2.30 / **ft-EMA 2.27**——不同预训练解码器结果相当，最终指标用 ft-EMA。
- **训练时长**：XL/2 仅训 2.35M 步（≈ADM 量级）FID 已 2.55，超所有前作；训满 7M 步降到 2.27（FP32 移植版 2.21）。

## 创新点与影响
**核心贡献**
1. **首个证明纯 Transformer 可替代 U-Net 做扩散 backbone**，且不丢性能、反而拿 SOTA——"U-Net 归纳偏置非必需"。
2. **adaLN-Zero 条件注入**：把 timestep/class（后续工作扩展到 text）通过零初始化的自适应 LayerNorm 调制注入，成为后续 DiT 系几乎标配的条件机制。
3. **建立"FID ~ Gflops"的扩散 scaling law 视角**：用 Gflops（而非参数量）刻画复杂度，证明加深加宽或减小 patch（增 token）都单调降 FID，且大模型更算力高效、采样算力无法替代模型算力。
4. **可复用、极简的训练配方**：直接继承 ViT/ADM 的超参（恒定 lr、无 warmup、无正则、仅水平翻转），训练高度稳定无 loss spike——为后续大规模 DiT 训练扫清门槛。

**对后续工作的影响（significance）**：DiT 是现代扩散 Transformer 的**架构祖先**——MMDiT/SD3、PixArt-α/Σ、Hunyuan-DiT、Lumina、以及 OpenAI Sora（Peebles 本人主导）等当代 T2I/视频扩散模型基本都建立在 DiT/patchify+adaLN(-Zero) 范式之上；论文结尾即明确预言 DiT 可作为 DALL·E 2、Stable Diffusion 这类文生图模型的 drop-in backbone，这一预言此后被业界大规模兑现。

**已知局限**：
- 实验**仅限 ImageNet 类条件生成**，未验证文生图（论文把它列为 future work，但实践已证明可行）。
- 仍依赖**现成冻结 VAE**，未联合训练 tokenizer；扩散目标仍是 DDPM（噪声+协方差），未用后来更优的 flow matching / rectified flow。
- 原版**未用 Flash Attention / torch.compile / bf16** 等工程加速（开源后由社区 fast-DiT 等补齐）。
- adaLN 对所有 token 施同一调制函数，表达力受限（cross-attention 更灵活但更贵）——这一权衡在后续带文本条件的工作中被重新设计（如 MMDiT 的双流注意力）。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2212.09748
- paper PDF: https://arxiv.org/pdf/2212.09748
- project page (含 latent walk 视频): https://www.wpeebles.com/DiT
- code (官方 PyTorch): https://github.com/facebookresearch/DiT
- HF Space (在线 demo): https://huggingface.co/spaces/wpeebles/DiT
- diffusers DiT pipeline: https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/dit.mdx
- 预训练权重: https://dl.fbaipublicfiles.com/DiT/models/DiT-XL-2-256x256.pt ， https://dl.fbaipublicfiles.com/DiT/models/DiT-XL-2-512x512.pt

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2212.09748.pdf
- ../../../sources/omni/2022/dit-scalable-diffusion-transformers--readme.md
- ../../../sources/omni/2022/dit-scalable-diffusion-transformers--project.md
