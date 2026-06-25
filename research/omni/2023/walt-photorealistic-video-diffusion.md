---
title: "W.A.L.T: Photorealistic Video Generation with Diffusion Models"
org: Google Research / Stanford University
country: US
date: 2023-12
type: paper
category: video
tags: [video-diffusion, latent-diffusion, transformer, dit, window-attention, causal-3d-vae, text-to-video, magvit-v2]
url: https://arxiv.org/abs/2312.06662
arxiv: https://arxiv.org/abs/2312.06662
pdf_url: https://arxiv.org/pdf/2312.06662
github_url:
hf_url:
modelscope_url:
project_url: https://walt-video-diffusion.github.io/
downloaded: [arxiv-2312.06662.pdf, walt-photorealistic-video-diffusion--blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
W.A.L.T（Window Attention Latent Transformer）是 Google Research + 斯坦福（Agrim Gupta、Lu Jiang、李飞飞等）在 2023-12 提出的**基于 Transformer 骨干的隐空间视频扩散模型**，两大设计：(1) 用**因果 3D 编码器把图像与视频压进同一个隐空间**实现图像/视频联合训练；(2) 用**窗口注意力**（空间窗 + 时空窗交替）替代全注意力降本。在 UCF-101、Kinetics-600、ImageNet 上**不使用 CFG** 即达到 SOTA；级联三段模型可生成 **512×896、8fps、3.6s 的写实文生视频**，UCF-101 零样本 FVD 258.1（3B），是 Sora 公布前最重要的"统一隐空间 DiT 式视频扩散"范式演示之一。

## 背景与定位
W.A.L.T 要解决的是视频扩散的核心张力：[[latent-diffusion-ldm]] 类方法的隐空间该如何选——

- **逐帧空间压缩（per-frame latent）**：可复用预训练图像自编码器 / 图像 LDM、可吃巨量图文对，但网络复杂度高、难用 Transformer 做高分辨率视频骨干，且逐帧独立编解码会产生**闪烁**伪影。
- **时空压缩（spatiotemporal）**：能缓解上述算力与闪烁问题，但**无法直接用图文对**（图文对远比视频文本对更大更丰富）。

此前所有主流视频扩散（[[video-diffusion-models]] Ho et al.、Imagen Video、Make-A-Video、Align-Your-Latents/Video-LDM）都以 **U-Net** 为骨干，因为全注意力 Transformer 的显存随序列长度二次增长，对高维视频成本过高。W.A.L.T 的定位：**第一个成功用 Transformer 骨干联合训练图像+视频隐扩散的实证**——既拿到时空压缩的效率，又通过"首帧独立编码"把静态图当成单帧视频，从而仍能吃图文对。论文与 [[dit-scalable-diffusion-transformers]]（Peebles & Xie）一脉相承（去 U-Net、纯 Transformer 去噪），与同期但晚几个月公布的 Sora 在"统一隐空间 + Transformer 视频扩散"思路上高度并行（作者 Lu Jiang、Lijun Yu 等亦是 [[magvit-v2]] 团队）。

## 模型架构
两阶段：第一阶段视觉 token 化（autoencoder），第二阶段 Transformer 去噪。

**第一阶段——因果 3D 自编码器（沿用 [[magvit-v2]] tokenizer）**
- 输入视频 x ∈ R^{(1+T)×H×W×C}，编码到 z ∈ R^{(1+t)×h×w×c}，空间压缩 fs=H/h=W/w、时间压缩 ft=T/t。
- **因果 3D CNN**：常规 3D 卷积核会同时看前后帧，无法独立处理首帧；因果卷积只看过去 kt−1 帧，于是**首帧总是被独立编码**，静态图像 x∈R^{1×H×W×C} 自然变成"单帧视频" z∈R^{1×h×w×c}——这是图像/视频共享隐空间的关键。
- 与 MAGVIT-v2 不同：**隐空间是实值、无量化（quantization-free）**，因为扩散模型可在连续隐空间上工作（不需要 codebook）。沿用 VQ-GAN 的对抗损失 + 感知损失提升重建。
- T2V 实配：fs=8、ft=4（即时间 4×、空间 8× 压缩），channel 128，channel multiplier (1,2,2,4)；隐通道维 c=8 是消融出的甜点。

**第二阶段——窗口注意力 Transformer（去噪骨干）**
- **Patchify**：对每个隐帧独立切成 hp×wp 个非重叠 patch，patch size p（消融显示 p 越小越好，T2V base 用 p=1）。位置编码 = 空间 + 时间可学习绝对位置编码之和，并额外叠加相对位置编码（原文 §4.2，配合 Swin 式窗口注意力）；图像只加首个时间位编码。
- **两类窗口注意力交替（核心）**：
  - **空间窗 SW**：限制在单个隐帧 1×hp×wp 内，建模图像与视频的空间关系（默认 1×16×16 窗）。
  - **时空窗 STW**：限制在 (1+t)×h'p×h'w 的 3D 窗内，建模视频帧间时间关系（默认 5×8×8 窗）。**对图像用 identity attention mask**——图像 latent 在 STW 层原样透传，使同一批可混合图像与视频。
  - 消融（Tab.3b）：局部窗注意力相比全自注意力 FVD 持平甚至更好，且**最高快 2×**、更省显存。
- **文本条件——空间 cross-attention**：在 self-attention 之外加 cross-attention 层；纯视频训练时 S/ST 块用 SW/STW cross-attn，**联合训练时只用 SW cross-attn**；cross-attn 把输入信号(query)与条件(key,value)拼接后再算（早期实验发现拼接更好）。文本编码器为 **T5-XL**（单一编码器，未用 CLIP 也未用 T5-XXL）。
- **AdaLN-LoRA（参数高效条件注入）**：标准做法是每层一个 MLP 回归 AdaLN 的 6 组 (γ1,γ2,β1,β2,α1,α2) 调制参数，参数量随层数线性、随 d_model 二次增长（ViT-g/1B 会多出 475M）。W.A.L.T 借鉴 [[lora]]：A1=MLP(c+t)，其余层 Ai=A1+Wbi·Wai·(c+t)（低秩 r≪d_model）。r=2 时把 ViT-g 的 AdaLN MLP 从 475M 压到 12M；消融显示 r 越大越好，但同等参数预算下"把参数给主干 + 小 r"比"独立 AdaLN"final loss 更低（Tab.4）。
- **Self-conditioning**：以概率 psc 先跑一次 z̃0=fθ(zt;0,c,t)，再把 stopgrad(z̃0) 沿通道维拼回做第二次前向 fθ(zt;z̃0,c,t)；与 v-prediction 配合效果好，psc 从 0→0.9 把 UCF FVD 改善 ~44%。

**模型规模与分辨率策略**
- 模型档（参数随 AdaLN 方案而变，原文 Tab.1/3d/4）：默认 **W.A.L.T-L + AdaLN-LoRA r=2 = 313M**（Tab.1/3d）；Tab.4 中"L+独立 AdaLN"=458M、"XL+LoRA r=2"=460M；ImageNet 版 W.A.L.T-L=460M（Tab.2）；T2V base=3B。ViT-g 配置约 1B（仅作 AdaLN-LoRA 省参举例）。
- T2V 级联三段（原文 §5.3）：base 在 **17×128×128（3B）**，两段 2× 超分 SR1 **17×128×224→17×256×448（L,1.3B）**、SR2 **17×256×448→17×512×896（L,419M）**。base 用方形宽高比训练，再在子集上微调到 9:16（插值位置编码 + 缩放窗口）。⚠ patch size 原文自相矛盾：正文 §5.3 称两段超分皆 p=2，而 Tab.8 列 SR1 p=2、SR2 p=4——本页训练方法节按 Tab.8 取值。
- 超分用级联 + **noise conditioning augmentation**（按 γ(t) 注噪、噪声等级 tsr~U(0,tmax) 喂给 AdaLN-LoRA），缓解推理时低分辨率输入与训练 GT 的分布差。
- **自回归长视频 / 图生视频**：训练时以概率 pfp 条件在过去帧上（条件 cfp=concat(mfp∘zt, mfp)，mfp 是二值掩码）；条件 1 个 latent 帧=图生视频，2 个 latent 帧=视频预测。推理先生 17 帧，再把最后 5 帧编码成 2 个 latent 帧驱动后续自回归，保证运动连续。

## 数据
- **T2V 训练集**：约 **970M 文本-图像对** + 约 **89M 文本-视频对**，来自"公开互联网 + 内部来源"。这是 W.A.L.T 联合训练的核心——图文对数量约为视频文本对的 10 倍，正是统一隐空间设计要吃下的红利。
- **学术 benchmark 训练**：UCF-101（类条件生成）、Kinetics-600（5 帧条件的视频预测）、ImageNet 256×256（类条件图像）均用各自标准训练集，保证公平对比。
- **清洗/过滤/re-caption/美学与安全过滤、合成数据占比**：论文**未披露**具体的数据清洗管线、字幕重写、美学/安全过滤细节与配比（仅说明图文+视频文本两路联合）。

## 训练方法
- **扩散目标**：Gaussian diffusion，全程用 **v-prediction**（v=√(1−γ)·ε − √γ·x0，遵循 Imagen-Video / progressive distillation 传统）。损失为标准 ‖y−fθ(xt;c,t)‖²。
- **零终端 SNR（zero terminal SNR）**：常规 LDM 噪声表在 t=1 时 γ(t)>0，仍泄露信号，训练-推理不匹配；视频时间冗余高，泄露危害更大。强制零终端 SNR 后 UCF FVD 从 91.0→60.7（Tab.3e），是关键 trick。
- **QK-norm + latent 归一化**：query-key normalization 稳定大模型训练；对 latent 先归一化再喂 Transformer（去掉 latent norm FVD 67.9 vs 60.7）。
- **联合训练（image+video）是一等贡献**：同为 419M 的 W.A.L.T-L，video-only 在 UCF-101 T2V 得 IS 26.8 / FVD 598.8，**video+image 联合后 IS 31.7 / FVD 344.5**（FVD 大幅改善），与 Ho et al. 在 U-Net 上的图像/视频联合训练结论一致。
- **多阶段**：先单段联合预训练（base），再训两段超分；超分用 noise conditioning augmentation。base 用方形训练后微调 9:16 宽高比。
- **训练时长/步数**（Tab.8）：T2V base 第二阶段 Transformer **52 层 / hidden 9216 / 16 头**，训 550k 步、batch 512、Adafactor、lr 2e-4、p=1；SR1 40 层 /1408、675k 步、p=2；SR2 24 层/1024、275k 步、p=4。UCF-101 模型训 60k 步（消融 35k 步），ImageNet 350 epoch。
- **采样**：DDIM 50 步；学术 benchmark **不用 CFG**，T2V 用 CFG（以 cfp 作条件做标准 CFG）。
- **蒸馏/一致性/步数蒸馏**：论文**未使用**（无 consistency/LCM/ADD 等加速蒸馏）；推理一律 50 DDIM 步。
- 关键超参（Tab.8）：扩散 1000 步、线性噪声表 β0=1e-4/β1000=0.02、Cosine lr、AdamW(benchmark)/Adafactor(T2V)、EMA（benchmark 段开、T2V 段关）、psc=0.9、c=8、r=2。

## Infra（训练 / 推理工程）
- **GPU 时 / 算力规模 / 并行分布式 / 混合精度 / 吞吐**：论文**未披露**具体 GPU 型号、卡数、GPU·时或并行策略（数据/张量/流水线并行均未报告）。仅可推断为 Google 内部 TPU/GPU 大规模集群（Adafactor 优化器、batch 512 等为大规模训练惯例）。
- **效率主张（来自消融）**：窗口注意力相比全自注意力**最高 2× 加速**、显存更省，是 Infra 层面的核心收益；Tab.3b 还报告了 steps-per-sec（sps，如 STW 5×8×8 为 2.00 sps vs 全注意力 1.20 sps）。
- **推理**：固定 50 DDIM 步、级联三段（base→2×→2×），自回归扩展长视频；无量化/缓存/蒸馏加速披露。
- **部署形态**：纯研究项目，**未开源权重，无官方 GitHub / HF / ModelScope**（官方仅提供 arXiv + 项目样例页）。

## 评测 benchmark（把效果讲清楚）
所有数字均来自已抓取的 arXiv 原文（Tab.1/2/5/7），不含 CFG 除非注明。

**视频生成（Tab.1，主指标 FVD↓；同表横跨两 benchmark 两列）**
- **Kinetics-600 帧预测（5 帧条件，K600 FVD↓ 列）**：W.A.L.T-L FVD **3.3±0.0**（**313M**，50 步），优于 RIN 10.8、Video Diffusion 16.2、TrIVD-GAN-FP 25.7、MAGVIT-v2 4.3 等（注：MAGVIT 的 9.9、Phenaki 的 36.4 在 Tab.1 中属 **K600 FVD** 列，非 UCF、非 IS）。
- **UCF-101 类条件（UCF FVD↓ 列）**：W.A.L.T-L FVD **46±2**（**313M**）、W.A.L.T-XL FVD **36±2**（**460M**，非 2B；原文 Tab.1 两个 W.A.L.T 行参数为 313M/460M），超越 TATS(332±18)、MAGVIT(76±2)、MAGVIT-v2(58±2)；以**更少参数 + 50 DDIM 步**达到 SOTA，且**不用 CFG**。

**类条件图像 ImageNet 256×256（Tab.2，无 CFG，指标 FID↓ / IS↑）**
- W.A.L.T-L **FID 2.56 / IS 215.1**（**460M**，50 步），优于 DiT-XL/2(FID 9.62)、ADM、MDT、MaskDiT、simple diffusion；仅 VDM++ FID 略低（2.40）但参数 2B。加 CFG（Tab.7）IS 进一步领先，FID 具竞争力。

**UCF-101 零样本文生视频（Tab.5，IS↑ / FVD↓）**
| 模型 | IS↑ | FVD↓ |
|---|---|---|
| CogVideo (English) | 25.3 | 701.6 |
| Make-A-Video | 33.0 | 367.2 |
| Video LDM | 33.5 | 550.6 |
| PYoCo | 47.8 | 355.2 |
| **W.A.L.T 419M (video only)** | 26.8 | 598.8 |
| **W.A.L.T 419M (video+image)** | 31.7 | 344.5 |
| **W.A.L.T 3B (video+image)** | **35.1** | **258.1** |

→ **FVD 超越所有此前工作**；IS 仅次于 PYoCo（作者归因 PYoCo 用了 CLIP+T5-XXL 双编码器，而 W.A.L.T 只用单 T5-XL）。同时验证：**联合训练 + 模型放大**对高质量 T2V 缺一不可（video-only→+image：FVD 598.8→344.5；419M→3B：FVD 344.5→258.1）。

**关键消融结论（Tab.3，UCF-101）**
- patch size：p=1（FVD 60.7） ≫ p=2(134.4) ≫ p=4(461.8)，越小越好。
- 时空窗：局部窗 ≥ 全自注意力质量、且快 2×（5×16×16 FVD 55.3 vs full 59.9）。
- self-cond：psc 0→0.9，FVD 109.9→61.4（~44% 改善）。
- AdaLN-LoRA：r 越大越好（r=2→256，FVD 60.7→52.5，参数 313M→357M）。
- 零终端 SNR：去掉则 FVD 91.0（vs 60.7），危害最大。
- latent 通道 c：重建 rFVD 随 c 增大单调下降（c=4→32：37.7→3.5），但生成 FVD 非单调（c=4/8/16/32 = 86.4/75.4/67.0/83.4，本表 UCF 上 c=16 最低 67.0）；论文据"过低/过高 c 都损 FVD、c=8 在多数数据集任务上最稳健"取 c=8 为默认甜点。
- **人评 / Arena ELO / VBench**：论文**未报告**（W.A.L.T 早于 VBench 流行，T2V 评测仅用 UCF-101 零样本 IS/FVD + 项目页定性视频）。

## 创新点与影响
**核心贡献**
1. **统一隐空间 + 因果 3D VAE 的"首帧独立编码"**：让图像（单帧视频）与视频共享 token 空间，吃下 10× 于视频文本对的图文对，同时享受时空压缩效率——后续 Sora、统一视频生成模型的共识范式。
2. **窗口注意力 Transformer 骨干替代 U-Net**：S/ST 窗交替 + 图像 identity mask，首个把纯 Transformer 隐视频扩散在公开 benchmark 做到 SOTA 的实证，质量与全注意力持平却 2× 提速。
3. **AdaLN-LoRA**：把扩散 Transformer 的 AdaLN 调制参数低秩化，为后续 DiT 系条件注入提供省参方案。
4. **工程 trick 组合**：v-prediction + 零终端 SNR + self-conditioning + QK-norm + latent norm 的协同。

**影响**：作为 **Sora（2024-02）公布前**最完整的"统一隐空间 DiT 式 T2V"公开证据，W.A.L.T 与 [[dit-scalable-diffusion-transformers]] [[magvit-v2]] 一起塑造了 2024 年视频扩散从 U-Net 转向 Transformer、从逐帧隐空间转向时空压缩隐空间的主流方向，并强化了"图像/视频联合训练 + scaling"的方法论。

**已知局限**
- base 仅 3B，作者自承**远小于头部 T2V 系统**（如 Imagen-Video base 5.7B），scaling 仍是未尽方向。
- **未开源**（无权重/代码/HF），数据清洗与算力细节大量未披露。
- 文本编码器仅单 T5-XL，IS 落后于用更强文本嵌入（CLIP+T5-XXL）的 PYoCo。
- 无蒸馏加速，推理固定 50 DDIM × 三级联，成本较高。
- T2V 评测仅 UCF-101 零样本 IS/FVD，缺人评/Arena/现代 T2V benchmark。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2312.06662
- paper (PDF): https://arxiv.org/pdf/2312.06662
- project page / blog（含样例视频 + 摘要 + 系统图）: https://walt-video-diffusion.github.io/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2312.06662.pdf
- ../../../sources/omni/2023/walt-photorealistic-video-diffusion--blog.md
