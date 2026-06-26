---
title: "Stable Cascade (Würstchen v3)"
org: "Stability AI"
country: EU
date: "2024-02"
type: model-card
category: t2i
tags: [text-to-image, latent-diffusion, cascade, wuerstchen, efficient, convnext, vqgan, semantic-compressor, open-weights]
url: "https://stability.ai/news/introducing-stable-cascade"
arxiv: "https://arxiv.org/abs/2306.00637"
pdf_url: "https://arxiv.org/pdf/2306.00637"
github_url: "https://github.com/Stability-AI/StableCascade"
hf_url: "https://huggingface.co/stabilityai/stable-cascade"
modelscope_url: ""
project_url: "https://stability.ai/news/introducing-stable-cascade"
downloaded: [stable-cascade--blog.md, stable-cascade--readme.md, stable-cascade--train-readme.md, stable-cascade--models-readme.md, stable-cascade--hf-modelcard.md, arxiv-2306.00637.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Stable Cascade 是 Stability AI 2024-02 发布的开源文生图模型，落地 [[wuerstchen]] 的三级级联架构（Würstchen v3）：把文本条件扩散放在 **42× 高压缩潜空间**（1024×1024 图 → 24×24 latent）里训练，**最大模型比 SDXL 还多 14 亿参数却推理更快**；据官方人评，在 prompt 对齐和美学质量上几乎全面优于 SDXL / Playground v2 / SDXL Turbo / Würstchen v2，且训练成本相比同规模 Stable Diffusion 降低约 16×。

## 背景与定位
传统潜扩散模型 [[latent-diffusion-ldm]] 用一个 VAE 把图像压到压缩因子 8 的潜空间（1024→128），扩散模型直接在这个空间训练。问题是：潜空间越大，训练和推理越贵；而 VAE 压缩因子再往上提通常会严重损伤重建质量。

Würstchen（ICLR 2024，OpenReview gU58d5QeGv；arXiv:2306.00637 v2 2023-09；Pernias 独立研究者 / Rampas（TH Ingolstadt + Wand Technologies）/ Richter、Pal（Mila）/ Aubreville（TH Ingolstadt），Stability AI 提供算力）提出的核心洞见是：**把"文本→图像语义"的生成 与 "语义→高清像素"的解码彻底解耦**。语义生成放在一个极小的、压缩因子 42 的潜空间里做，而高分辨率重建交给两级解码器。语义潜表示比纯文本嵌入携带的图像细节信息丰富得多，因此能在极小空间内给出强引导，从而大幅省算力。论文里 1B Stage C 仅用 24,602 A100 GPU-时训练，对比 SD 2.1 的 200,000 GPU-时，约 8× 提效。

Stable Cascade 是该架构的第三代（v3）——由 Stability AI 重训并放大：Stage C 扩到 **3.6B**（同时给 1B Lite 版），Stage B 给 **1.5B / 700M** 两档，于 2024-02 以"研究预览（非商用许可）"形式开源，并一并放出训练 / 微调 / ControlNet / LoRA 全套代码。它是 SDXL 与 SD3 之间，Stability 在 t2i 效率路线上的一次开源押注。

## 模型架构
三个模型构成一条"级联"，命名也由此而来。**核心是 Stage A & B 充当"高压缩 VAE 的替代品"，Stage C 在压缩潜空间里做文本条件扩散**。

**Stage A — VQGAN 潜空间解码器（v3 README 称为 VAE，20M 参数；论文 18M）**
- f4 VQGAN：把 3×1024×1024 图像编码为 256×256 离散 token，码本大小 8,192。
- 训练后丢弃量化（quantization drop），Stage B 在其"未量化"的连续潜空间里工作；Stage A 把 4×256×256 的潜图解回 1024×1024 像素。
- 参数极小、固定不动；它存在的意义是让 Stage B 在 4× 更小的空间（4×256×256 而非 3×1024×1024）里学，更快更省，且实测 Stage B 加 Stage A 比直接在像素空间学收敛更快。

**Stage B — 潜扩散重建器（v3：700M / 1.5B；论文 1B）**
- U-Net 架构，4 个 encoder/decoder stage，通道宽度 320/640/1280/1280；每个 building block = ConvNeXt block + 时间步条件块 + cross-attention（文本 + 图像嵌入）。第一 stage 仅做时间条件、无 cross-attention。归一化用 GlobalResponseNorm，激活用 GELU。各 stage cross-attention 头数 -, 10, 20, 20。
- 条件来源：**Semantic Compressor**（一个 EfficientNetV2-S 主干，ImageNet 预训练并在 Stage B 训练时一并更新权重）把图像（1024 经 bicubic 缩到 786×786 输入）编码成 R^{1280×24×24}，再经 1×1 卷积归一化投影到 **C_sc ∈ R^{16×24×24}**。这个高压缩语义嵌入与文本嵌入一起，通过 cross-attention + 拼接注入到 Stage B 各残差块，引导其把 24×24 语义解回 256×256 潜图。
- 训练 Stage B 时对语义嵌入间歇性加噪（教模型容忍 Stage C 生成的"不完美"嵌入），并随机 drop C_sc 以支持 classifier-free guidance。

**Stage C — 文本条件潜生成器（v3：1B / 3.6B；论文 1B）**
- **关键创新：放弃 U-Net**。因为输入已被压到 42×，再下采样有害，所以 Stage C 是 **16 个 ConvNeXt block 的简单堆叠，全程不下采样**，工作在固定的 24×24 latent 分辨率上；网络宽度 1280 通道，每个 block 后接时间条件 + 文本 cross-attention（16 头）。
- 文本编码器：**未池化的 CLIP-H（OpenCLIP ViT-H/14）文本嵌入**，维度 1024。（注：v3 还可用 CLIP 图像嵌入做 image variation。）
- 训练目标是直接在 Semantic Compressor 的 16×24×24 潜空间里生成；推理时 EfficientNetV2-S 被丢弃，Stage C 的输出直接替代 Semantic Compressor 去条件化 Stage B。
- ControlNet 实现也因这种"纯残差块、无 U-Net"而简化：通过 `controlnet_blocks` 指定在哪些 block 注入控制信息（例如 `[0,4,8,12,51,55,59,63]`），不需要像 SD 那样整份复制 U-Net encoder，参数量更省（train README 明确说明）。

**整体压缩**：24×24 语义潜空间 → 1024×1024 像素，空间压缩因子 1024/24 ≈ **42.67**（对比 SD 的 8）。

## 数据
- **数据集**：全部 stage 都在 **improved-aesthetic LAION-5B**（Schuhmann 等 2022）的**去重子集**上训练（论文 Appendix E）。
- **清洗 / 过滤**：训练代码暴露的 `dataset_filters` 支持按 `aesthetic_score`（如 `> 4.5`）和 `nsfw_probability`（如 `< 0.01`）过滤；Stage C 的**第四阶段训练专门在"美学艺术作品"进一步过滤后的子集**上做（提升美学质量）。
- **规模（论文 v2/1B 口径）**：Stage C 训练 24,602 A100 GPU-时；Stage B 约 318M 训练样本 / 11,000 GPU-时。论文 Table 2 给 Würstchen **总训练样本 1.42B**（= 各阶段 step×batch 累加，远少于 SD 1.4 的 4.8B、SD 2.1 的 3.9B）。
- **re-captioning / 合成数据**：未披露（论文与 v3 README 均未提及对 LAION 做合成重标注）。
- **v3 放大版（3.6B Stage C / 1.5B Stage B）的具体数据规模与配比**：Stability 官方博客与 README **未单独披露**，仅说"most work was put into 3.6B 的 finetuning"。

## 训练方法
**训练顺序与推理相反**：先 Stage A，再 Stage B，最后 Stage C。

- **Stage A（VQGAN）**：单次 500,000 步，AdamW，lr 1e-4，batch 256，输入 128×128 crop（图先 resize 到 256×256）。三损失：MSE + 对抗损失(AL) + 感知损失(PL)；前 10k 步权重 (1.0, 0.0, 0.1)，之后激活 AL（权重升到 0.01）。训练中以 10% 概率随机丢弃量化（为之后去量化做准备）。
- **Stage B（潜扩散）**：AdamW，lr 1e-4，10k 步线性 warmup。先 457,000 步 @ 512×512（batch 512），再追加 300,000 步 @ 1024×1024（batch 128）；Semantic Compressor 对应输入 384×384 / 768×768。标准 LDM 训练。
- **Stage C（文本条件扩散）**：**4 次连续训练**，AdamW lr 1e-4。
  1. 500,000 步 @ 12×12 latent（compressor 输入 384×384），batch 1536；
  2. 追加 364,000 步 @ 24×24 latent（输入 768×768），batch 1536；
  3. 仅 4,000 步做多宽高比适配（每 batch 随机取 768×1280 / 1280×768 / 768×768），batch 768；
  4. 最后 50,000 步在美学艺术子集上提升美学，batch 384，768×768（24×24 latent）。
  - **最终模型是第 3 次与第 4 次训练权重的 50:50 插值**（在写实与美学/艺术之间取折中），同时开源参与插值的两个端点模型。
- **扩散公式与目标**：标准 DDPM 前向加噪，**cosine 噪声调度（Nichol & Dhariwal）+ 连续时间步**。Stage C 采用了一个改写的噪声预测目标 ε̄ = (X_t − A)/(|1−B|+1e-5)，A,B = f_θ(...)，使模型初始返回输入、对高噪声时间步 loss 更小，训练更稳定。损失为 MSE + **p2 loss weighting**（高噪声层贡献更大）。文本条件 5% 概率 drop 成 null-label 以支持 CFG。
- **v3 训练工程超参（来自官方 train README 的配置文件）**：lr 1e-4，batch_size 256，image_size 768，multi-aspect-ratio 列表 [1/1, 1/2, 1/3, 2/3, 3/4, ...]，updates 500,000，EMA（ema_start 5000 / ema_iters 100 / ema_beta 0.9），FSDP 可选，webdataset（支持 S3）。
- **加速 / 蒸馏**：v3 本体未做步数蒸馏，但 README 明确"LoRA / ControlNet / IP-Adapter / **LCM** 等扩展均可用"。

## Infra（训练 / 推理工程）
- **算力（论文 v2/1B 口径，一手数字）**：Stage C 24,602 A100 GPU-时；Stage B ≈11,000 GPU-时；估算碳排约 2,276 kg CO2eq —— 对比 SD 1.4 的 150,000 GPU-时 / 11,250 kg、SD 2.1 的 200,000 GPU-时 / 15,000 kg。
- **分布式**：v3 训练代码用 PyTorch **FSDP**（Fully Sharded Data Parallel）做大模型分布式，配 slurm 脚本；EMA 模型；webdataset 支持 S3/本地 tar 大规模流式读取。
- **v3 放大模型（3.6B Stage C）的具体 GPU 数 / 训练时长**：**未披露**。
- **推理**：官方称 VRAM 需求约 **20GB**（用最大 Stage B/C），换小变体可进一步降低（牺牲质量）。精度上**只支持 bfloat16 或 float32**，目前 float16 会溢出（models README）。diffusers 里推荐配置：Prior(Stage C) 20 步 + guidance 4.0，Decoder(Stage B) 10 步 + guidance 0.0；支持 model CPU offload。论文采样默认 Stage C τ_C=60、Stage B τ_B=12（w=4），均用 DDPM。
- **推理速度**：尽管最大模型比 SDXL 多 14 亿参数，官方 inference-speed 图显示 Stable Cascade（30 步）整体比 SDXL（50 步）/ Playground v2 更快；论文也称 Würstchen 推理比 SD 2.1 快 2× 以上（极小的 24×24 主生成空间是主因）。

## 评测 benchmark（把效果讲清楚）
**v3 官方人评（Stable Cascade 博客 / README，无具体数字，仅结论）**：用 parti-prompts + 美学 prompt 混合，做人类偏好评测；**Stable Cascade（30 步）在 prompt 对齐与美学质量上几乎全面优于** Playground v2（50 步）、SDXL（50 步）、SDXL Turbo（1 步）、Würstchen v2（30 步）。官方未公布 ELO / 具体胜率数字。

**底层 Würstchen 论文（v1/v2，1B Stage C，一手数字）**：
- **PickScore 二选一胜率**（Würstchen vs 对手，越高越偏好 Würstchen）：
  - COCO-30k：vs DF-GAN 99.8% / vs GALIP 98.1% / vs SD 1.4 78.1% / vs SD 2.1 64.4% / **vs SDXL 仅 39.4%**（SDXL 更强）。
  - Localized Narratives-COCO-5K：vs SD 1.4 79.9% / vs SD 2.1 70.0% / vs SDXL 39.1%。
  - Parti-prompts：vs SD 1.4 82.1% / vs SD 2.1 74.6% / vs SDXL 39.0%。
  - 解读：Würstchen 在同等/更小算力规模下显著优于 SD 1.4/2.1，但仍逊于更大的 SDXL（论文坦承 SDXL 容量更大、数据/算力未知，对比不完全公平，故后续实验剔除 SDXL）。
- **COCO-30k 自动指标（Table 2，∗为论文自测）**：Würstchen 0.99B，60 步，**FID@256² = 23.6**，**IS@299² = 40.9**。对比：Baseline LDM(ours) 0.99B FID 43.5 / IS 20.1；SD 1.4 0.8B FID 16.2 / IS 40.6；SD 2.1 0.8B FID 15.1 / IS 40.1；SDXL 2.6B FID > 18（IS 未报告）；LDM 1.45B FID 12.63 / IS 30.3；CogView2 FID 24.0 / IS 25.2。Würstchen 的 **IS 在论文这张表里最高**（论文原文：on COCO30K achieve a higher Inception Score than all other models in the comparison），但 FID 相对偏高——论文归因于其生成图偏"平滑"、高频细节少，在 COCO 这类真实照片上 FID 吃亏。
- **人类偏好研究**：90 名参与者，Parti-prompts 3343 次、COCO 2262 次对比（仅对 Würstchen vs SD 2.1）。Parti-prompts 上 Würstchen 被明显偏好（更贴近目标使用场景）；MS-COCO 总体偏好不分明（短/模糊 prompt 使偏好更主观），但按个人偏好统计（仅取对比数 ≥30/51 的上 50% 用户）后，Würstchen 在两个数据集上均被偏好。
- **关键消融/对照**：自建 Baseline LDM（同 ~25,000 GPU-时、U-Net、SD 2.1 first-stage）被 Würstchen 全面碾压（PickScore 96.5%+、FID 43.5→23.6），证明**架构本身（而非算力）带来效率提升**。

**注**：GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward 等 benchmark 在一手源中**均未报告**。

## 创新点与影响
**核心贡献**
1. **极致潜空间压缩（42× vs SD 的 8×）下仍保持可用重建**——靠两级解码器（Stage A VQGAN + Stage B 潜扩散 + EfficientNetV2-S 语义压缩器）而非单一 VAE。
2. **文本生成与高分辨率解码彻底解耦**：文本条件扩散（Stage C）只在 24×24 上做，使训练成本相比同规模 SD 降 ~16×（v3 口径）/ Stage C 相比 SD 2.1 降 ~8×（论文口径）；微调 / LoRA / ControlNet 只需训 Stage C。
3. **Stage C 抛弃 U-Net，用 16 个无下采样 ConvNeXt block**——证明在已高度压缩的空间里不需要多尺度 U-Net；ControlNet 因此可仅在指定 block 注入、参数更省。
4. 改写的 A/B 噪声预测目标 + p2 loss weighting，提升小空间扩散训练稳定性。

**影响**
- 在 Stability 自家路线上，是 SDXL → SD3 之间效率方向的开源实验；强化了"高压缩潜空间 + 级联/两级解码"这一省算力范式（与 PixArt / 后续 cascade 思路呼应）。
- 开源全套训练 / 微调 / ControlNet / LoRA 代码 + 多档权重，配合 diffusers 集成，降低了消费级硬件上玩转 t2i 的门槛。
- Würstchen 把"训练效率/碳排"作为一等评测维度，推动社区关注可持续生成式 AI。

**已知局限**
- **人脸/人物常生成不佳**；自编码部分有损（HF card 明确）。
- 生成图偏平滑、高频细节弱，真实照片域 FID 偏高。
- 图像质量绝对值仍逊于更大的 SDXL（论文承认）。
- 仅 **bfloat16/float32**，float16 溢出不可用。
- 许可证为 **Stability AI 非商用研究社区许可**（仅研究/非商用），代码 MIT。

## 原始链接
- blog（官方发布，一等公民）: https://stability.ai/news/introducing-stable-cascade
- github（StableCascade 代码 + 训练/推理/ControlNet/LoRA）: https://github.com/Stability-AI/StableCascade
- hf model card（stable-cascade，Stage B decoder）: https://huggingface.co/stabilityai/stable-cascade
- hf prior（Stage C）: https://huggingface.co/stabilityai/stable-cascade-prior
- paper（底层 Würstchen，方法/实验/Appendix E 训练细节来源）: https://arxiv.org/abs/2306.00637 ｜ OpenReview: https://openreview.net/forum?id=gU58d5QeGv

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/stable-cascade--blog.md)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/stable-cascade--readme.md)
- [train-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/stable-cascade--train-readme.md)
- [models-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/stable-cascade--models-readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/stable-cascade--hf-modelcard.md)
- [arxiv-2306.00637.pdf](https://arxiv.org/pdf/2306.00637) （PDF 不入 git，已本地落盘精读）
