---
title: "DeepFloyd IF"
org: "Stability AI / DeepFloyd"
country: EU
date: "2023-04"
type: model-card
category: t2i
tags: [text-to-image, cascaded-diffusion, pixel-diffusion, t5-xxl, imagen-style, open-source, text-rendering, super-resolution]
url: "https://github.com/deep-floyd/IF"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/deep-floyd/IF"
hf_url: "https://huggingface.co/DeepFloyd/IF-I-XL-v1.0"
modelscope_url: ""
project_url: "https://stability.ai/news/deepfloyd-if-text-to-image-model"
downloaded: [deepfloyd-if--github-readme.md, deepfloyd-if--stability-blog.md, deepfloyd-if--hf-blog.md, deepfloyd-if--hf-IF-I-L-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DeepFloyd IF 是 Stability AI 旗下 DeepFloyd Lab 2023 年 4 月开源的 **Imagen 风格像素级级联扩散** 文生图模型：用**冻结的 T5-XXL（v1.1，~4.5B）做文本编码 + 三级像素扩散 U-Net（64→256→1024）**，是首个能可靠把**正确文字渲染进图像**的开源模型，零样本 COCO **FID-30K = 6.66**（IF-I-XL），刷新当时开源 SOTA。

## 背景与定位
2022 年文生图分成两条技术路线：一条是 [[latent-diffusion-ldm]] / [[stable-diffusion-1]] 走的 **latent 空间扩散 + CLIP 文本编码**（高效但文字渲染差、细节受 VAE 压缩限制）；另一条是 Google [[imagen]] 走的 **像素空间级联扩散 + 大语言模型 T5 文本编码**（细节/文字/语义理解更强，但闭源、参数量巨大）。DeepFloyd IF 明确选择复刻并开源后者——README 与 HF 博客都直言"架构强烈受 Google 闭源的 Imagen 启发"，模型卡 frontmatter 里 `arxiv: 2205.11487`（即 Imagen 论文）。

相对 [[stable-diffusion-2]] 的两点关键差异（HF 官方博客原话）：
1. **直接在像素空间去噪**（在未压缩图像上做扩散），而非 LDM 的 latent 空间——避免 VAE 压缩带来的高频细节损失，因此人脸、手部、细密纹理更好；
2. **用更强的 T5-XXL 取代 CLIP 文本编码器**——T5 对长 prompt、空间关系、拼写的理解显著更强，使 IF 成为**首个能可靠生成"图中带正确文字"的开源模型**（README 的招牌 demo 是袋鼠举着写有 "very deep learning" 的牌子）。

代价是参数量与显存暴涨：T5、Stage-1 U-Net、Stage-2 U-Net 分别 **4.5B / 4.3B / 1.2B** 参数，对比 SD 2.1 的文本编码器 + U-Net 仅 400M + 900M。技术谱系上 IF 把 [[cascaded-diffusion-models]]（级联超分扩散）、[[ddpm]]（离散扩散框架）与 Imagen 的"T5 + 像素级联"组合在开源世界完整落地。注意：**IF 自始至终未发表正式论文/技术报告**（README 写 "Research Paper (Soon)" 但从未兑现），全部一手技术细节来自 GitHub README、HF 模型卡 Training 段、Stability 官方博客与 HF 工程博客。

## 模型架构
**整体：模块化（modular）+ 级联（cascaded）+ 像素（pixel）+ 扩散（diffusion）三级流水线**，所有阶段共用同一个冻结文本编码器：

- **文本编码器：冻结 T5-v1.1-XXL**（Stability 博客写作 "T5-XXL-1.1"，约 4.5B 参数，完全由 Google 训练、IF 训练全程冻结）。Prompt 先过 T5 得到隐状态（非池化输出）。
- **文本注入 U-Net 的两条路**（IF-I-L 模型卡 Training 段精确描述）：
  1. **非池化输出**经一个**无激活的线性投影层**后，通过 **U-Net 主干里"受控的混合 self- 与 cross-attention"** 注入；
  2. **池化输出**经 **attention-pooling（64 个 head）** 得到全局特征，作为**额外特征加入 time embedding**（即把文本全局信息也喂给时间步条件）。
- **三级级联**（"player + amplifiers" 比喻：基模型出低分辨率底图，超分模型逐级放大）：
  - **Stage 1（base，IF-I）**：text → **64×64** 像素图。有三档：IF-I-M **400M** / IF-I-L **900M** / **IF-I-XL 4.3B**（招牌款）。
  - **Stage 2（super-res，IF-II）**：text-conditional **Efficient U-Net**，64×64 → **256×256**。两档：IF-II-M **450M** / **IF-II-L 1.2B**。超分阶段同样接收文本 embedding（文本引导超分）。
  - **Stage 3（super-res，IF-III）**：256×256 → **1024×1024**，原计划 IF-III-L **700M**，但**官方从未发布该权重**；实际管线用 Stability 已有的 **Stable Diffusion x4 Upscaler** 顶替（它自带独立文本编码器，不复用 T5 embedding，需重传原始 prompt）。
- **架构亮点**：README 的结论是"在级联扩散的**第一阶段用更大的 U-Net** 收益显著"——即把算力堆在 64×64 基模型（4.3B）而非超分阶段，是 IF 拿到 FID 6.66 的关键设计选择。
- **额外组件**：所有阶段输出过一个 **IFWatermarker 水印器**；Stage-1 自带 safety_checker / feature_extractor（CLIP-based NSFW 过滤）。

## 数据
- **数据集 LAION-A**：Stability 博客称在"自建高质量 LAION-A 数据集"上训练，**约 10 亿（image, text）对**；IF-I-L 模型卡更精确写 **1.2B text-image pairs（基于 LAION-A + 少量额外内部数据集）**。
- **LAION-A 构成**：[[stable-diffusion-1]] 同源的 **LAION-5B 英文部分的美学子集（aesthetic subset）**，经过：基于相似度哈希的**去重（deduplication via similarity hashing）**、额外清洗、以及对原数据集的其他改造。
- **安全过滤**：DeepFloyd 自建过滤器移除了**带水印（watermarked）、NSFW、其他不当内容**。
- **数据处理（训练时，IF-I-L 卡）**：图像用 **shifted-center-crop 增强**裁成正方形（从中心随机偏移最多 0.1 倍尺寸），再用 `Pillow==9.2.0` 的 **BICUBIC 重采样**（`reducing_gap=None` 以避免锯齿）缩到 64px，转成 BxCxHxW 张量。
- **CFG 数据条件**：训练时**随机 10% 的文本被替换为空字符串**，以习得 classifier-free guidance 能力。
- **评测数据隔离**：所有 cascade/stage 的训练都不使用任何 test/valid 划分；COCO 的 valid 部分仅用于在线监控 loss（catch incident），从不参与训练。
- 局限自述：主要为**英文 caption**（少量罗曼语系），主要训练自 **LAION-2B(en)**，非英文 prompt 表现明显更差，并继承 LAION-5B 的成人/暴力/性内容与西方/白人为默认的偏见。

## 训练方法
（以下数字来自 **IF-I-L-v1.0 模型卡 Training 段**——这是唯一披露完整训练配方的一手源；IF-I-XL 仅披露 batch/steps/FID。）

- **训练目标**：标准 DDPM 框架——**扩散过程限定 1000 个离散步，cosine beta（noising）schedule**；损失为 **noise 的重构目标（reconstruction objective）**，即 U-Net 预测被加入图像的噪声与真实噪声之间的回归（ε-prediction）。
- **文本端**：T5-v1.1-xxl **全程冻结**；10% 文本 dropout 实现 CFG。
- **训练步数**：IF-I-L checkpoint = **2,500,000 步 + 额外 500,000 步**，全程在 **64×64 分辨率**、所有数据集上训练。
  - 各档原始表（README Model Zoo）：IF-I-M 2.5M 步 / IF-I-L 3.0M 步 / IF-I-XL **2.42M 步**；IF-II-M、IF-II-L 各 2.5M 步；IF-III-L 1.25M 步。
- **Batch size**：IF-I-L **3200**；IF-I-XL **3072**；IF-II 系 **1536**；IF-III **3072**（README 表）。
- **优化器**：**AdamW8bit（8-bit 块量化优化器，arXiv 2110.02861）+ DeepSpeed ZeRO-1**。
- **激活省显存 trick**：**few-bit backward GELU activations**（反向传播时低比特存储 GELU 激活）。
- **学习率调度（OneCycleLR / one-cycle cosine 策略）**：
  - 主 2.5M 步：warmup 10,000 步，`start_lr=4e-6 → max_lr=1e-4 → final_lr=1e-8`；
  - 额外 500K 步：warmup 50,000 步，`start_lr=1e-8 → max_lr=4e-6 → final_lr=4e-8`（即用很低的 LR 继续精修）。
- **未披露**：IF-I-XL/IF-II 的具体 LR 曲线、总训练时长（GPU·小时）、是否有偏好对齐/RLHF/DPO（**无**——纯预训练扩散模型，无 SFT/偏好对齐阶段）；蒸馏/一致性加速（**未做**，IF 发布时仍是多步采样）。

## Infra（训练 / 推理工程）
**训练（IF-I-L 模型卡）：**
- **硬件：20 × 8 × A100 GPU = 160 张 A100**。
- **并行/省显存**：DeepSpeed **ZeRO-1**（优化器状态分片）+ **AdamW8bit**（8-bit 优化器状态）+ **few-bit backward GELU**——三者叠加把 160×A100 上训练 4.3B/4.5B 级像素扩散变得可行。
- **算力规模/总 GPU·时未披露**；README 致谢 Stability AI 提供 GPU compute 与基础设施（Richard Vencu 团队）、LAION 提供数据集。

**推理 / 部署（HF 工程博客，给出极细的显存账）：**
- **全 fp32 权重总计约 40GB**：T5-XXL text encoder 20GB / Stage-1 U-Net 17.2GB / Stage-2 U-Net 2.5GB / Stage-3（SD x4 upscaler）3.4GB。
- **fp16**：T5 11GB、Stage-1 8.6GB、Stage-2 1.25GB。
- **8-bit 量化 T5**：用 `bitsandbytes` 把 T5 checkpoint 压到 **~8GB**，使免费 Colab（13GB CPU RAM + 15GB T4 VRAM）也能跑完整 >10B 管线。
- **关键工程模式**：diffusers **逐组件模块化加载 + model CPU offload**——每一步只把当前需要的组件搬到 GPU（先 T5 出 embedding → del → 再 Stage-1 U-Net → ...），最低 **14GB VRAM** 即可跑全流程；HuggingFace 团队还把 U-Net 加载时间优化了 80%（README 致谢）。
- **生产推荐**：单张 **40GB A100**、所有组件常驻 GPU 不 offload（官方 Demo Space 即此配置）；xformers memory-efficient attention（`FORCE_MEM_EFFICIENT_ATTN=1`，torch<2.0 时）。
- **采样加速**：用 "smart" timestep respacing（如 Stage-1 `smart100`、Stage-2 `smart50`、Stage-3 `75` 步）减少采样步数；各阶段独立 CFG（典型 guidance_scale：Stage-1 7.0 / Stage-2 4.0 / Stage-3 9.0）。
- **可微调**：diffusers 支持 DreamBooth + 参数高效微调，单卡 ~28GB VRAM 即可给 IF 注入新概念。

## 评测 benchmark（把效果讲清楚）
**核心指标：零样本 COCO FID-30K（越低越好）**——来自 README Model Zoo 表与模型卡 Evaluation：

| 模型 | Cascade | 参数 | FID-30K | Batch | Steps |
|---|---|---|---|---|---|
| IF-I-M | I | 400M | **8.86** | 3072 | 2.5M |
| IF-I-L | I | 900M | **8.06** | 3200 | 3.0M |
| **IF-I-XL** | I | **4.3B** | **6.66** | 3072 | 2.42M |
| IF-II-M | II | 450M | — | 1536 | 2.5M |
| IF-II-L | II | 1.2B | — | 1536 | 2.5M |
| IF-III-L（未发布） | III | 700M | — | 3072 | 1.25M |

- **FID-30K = 6.66（IF-I-XL）** 是当时**开源 SOTA**——README 与模型卡均以此作为"outperforms current state-of-the-art models"的核心论据。IF 的像素级联 + 大 U-Net 路线把开源模型推到与同期闭源 SOTA（Imagen/Parti 等同走 T5 文本编码、报告的零样本 COCO FID 同在 7 附近）同档甚至更优的 FID 区间。注：**6.66 系 IF 自报的零样本 COCO FID-30K，未与他模型在同一 pipeline 下复测**；Imagen/Parti 等的对照数字来自各自原论文，**本页落盘源中并无 Imagen/Parti 论文**，故此处仅作量级参照、不列具体小数。
- **趋势结论**：Stage-1 base U-Net 越大 FID 越低（400M→8.86，900M→8.06，4.3B→6.66），印证"把算力堆在第一阶段大 U-Net"的设计判断。
- **定性能力**（官方博客/README 强调，非定量）：
  - **文字渲染**：首个能可靠把正确文字写进图的开源模型（拼写无误，inpainting 改牌子文字也准）；
  - **深层 prompt 理解**：多对象 + 不同属性 + 复杂空间关系；
  - **非标准长宽比**（竖/横/方）；
  - **零样本图生图 / 风格迁移 / 超分 / inpainting**：无需微调，靠"缩到 64px → 前向加噪 → 反向用新 prompt 去噪"实现（inpainting 仅在 mask 局部去噪）。
- **未报告**：GenEval、T2I-CompBench、DPG-Bench、HPSv2/ImageReward/PickScore、人评 ELO/Arena 等当时尚未流行或官方未做的指标；亦无与 SD/Midjourney 的人评对比（IF 无论文，未做这些 benchmark）。

## 创新点与影响
**核心贡献：**
1. **首个开源复刻 Imagen 路线**——把"冻结 T5-XXL + 像素空间级联扩散"在开源世界完整落地，证明非 latent 路线在开源也能达到 SOTA FID。
2. **首个可靠文字渲染的开源文生图模型**——T5-XXL 文本编码 + 像素空间使拼写正确率大幅领先同期 SD，直接启发后续对"文本编码器强度"的重视（与一年后 Stable Diffusion 3 引入 T5 一脉相承）。
3. **工程民主化**——配合 diffusers/transformers/accelerate/bitsandbytes，把 >10B 像素扩散塞进免费 Colab，示范了大模型模块化加载 + 8-bit 量化 + CPU offload 的范式。
4. **明确实证**："级联扩散把大 U-Net 放在第一阶段"收益最大。

**影响：** 成为像素级联 T2I 的开源代表，被大量后续工作当作 baseline（如 IterInv 等专门研究像素级 T2I 的反演）；其"T5 强文本编码 + 文字渲染"思路影响了 SD3、Pixart 等后续模型对 T5/强文本编码器的采用。

**已知局限：**
- **参数量/显存巨大**（T5 4.5B + Stage-1 4.3B），推理慢、部署重，是它未像 SD 那样大规模流行的主因；
- **像素级联多步采样**，无蒸馏加速，速度劣于 latent 模型；
- **未达完美 photorealism**；主要英文、非英文显著更差；继承 LAION-5B 偏见与不当内容风险；
- **限制性研究许可证**（DeepFloyd IF License，非商用）+ **Stage-3 1024px 权重从未发布**——开放度不及 SD，限制了社区生态；承诺的"完全开源 + 正式论文"均未兑现；
- DeepFloyd 团队后随 Stability AI 经营动荡逐渐沉寂，IF 未有 v2 迭代。

## 原始链接
- github: https://github.com/deep-floyd/IF
- hf (model card, gated): https://huggingface.co/DeepFloyd/IF-I-XL-v1.0
- hf (IF-I-L, 含完整 Training 配方): https://huggingface.co/DeepFloyd/IF-I-L-v1.0
- blog (Stability 官方发布): https://stability.ai/news/deepfloyd-if-text-to-image-model
- blog (HuggingFace 工程博客，含显存/部署细节): https://huggingface.co/blog/if
- inspired-by (Imagen 论文，模型卡 arxiv 字段): https://arxiv.org/abs/2205.11487
- 注：DeepFloyd IF **无独立论文/技术报告**（README "Research Paper (Soon)" 从未发布）。

## 一手源存档（sources/）
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/deepfloyd-if--github-readme.md)
- [stability-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/deepfloyd-if--stability-blog.md)
- [hf-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/deepfloyd-if--hf-blog.md)
- [hf-IF-I-L-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/deepfloyd-if--hf-IF-I-L-card.md)
