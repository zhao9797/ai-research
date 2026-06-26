---
title: "SEED: Planting a SEED of Vision in Large Language Model"
org: "Tencent AI Lab / ARC Lab (Tencent PCG)"
country: China
date: "2023-07"
type: paper
category: unified
tags: [unified, visual-tokenizer, discrete-tokens, vq, multimodal-llm, autoregressive, q-former, image-to-text, text-to-image]
url: "https://arxiv.org/abs/2307.08041"
arxiv: "https://arxiv.org/abs/2307.08041"
pdf_url: "https://arxiv.org/pdf/2307.08041"
github_url: "https://github.com/AILab-CVC/SEED"
hf_url: "https://huggingface.co/AILab-CVC/SEED"
modelscope_url: ""
project_url: "https://ailab-cvc.github.io/seed/seed.html"
downloaded: [arxiv-2307.08041.pdf, seed-tokenizer--ar5iv-fulltext.txt, seed-tokenizer--readme.md, seed-tokenizer--project-homepage.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
SEED 是一个为「喂给 LLM 自回归」而专门设计的**离散视觉 tokenizer**：把一张图压成 **32 个带 1D 因果依赖的高层语义离散码**（码本 8192），让一个现成 LLM 只靠 LoRA 微调就同时具备「看图（image→text）」与「画图（text→image）」能力。原型 SEED-OPT₂.₇ᵦ 仅用 **5M 公开图文对 + 64×V100、44 小时** 训练，便在零样本图像描述/VQA 上逼近用 129M 数据训练的 BLIP-2，并涌现出从未训练过的开放式 VQA 能力。

## 背景与定位
2023 年中，多模态大模型（MLLM）想复刻 LLM 那种「下一词预测就能涌现」的成功，遇到一个核心障碍：**怎样把图像变成能和文字一起被同一个自回归 Transformer 处理的 token**。当时有两条路：

- **连续对齐路线**（[[blip-2]] 系、[[gill]]）：把 CLIP-ViT 特征对齐进 LLM 输入空间做理解，或把 LLM 输出空间对齐到冻结的 [[latent-diffusion-ldm]]/Stable Diffusion 做生成。理解强但和 LLM「下一词预测」的原生训练范式不统一。
- **离散 token 路线**（DALL-E/[[cogview]] 用的 VQ-VAE、Taming Transformers）：把图离散成 ID 序列，天然兼容自回归目标，但当时已"失宠"——VQ-VAE 重建像素、**只抓低层细节**（颜色/纹理/边缘），LLM 学起来收敛慢、要超大规模训练，且多模态理解明显弱于 BLIP-2。

SEED 的论点：**离散 token 路线本身没错，错在 tokenizer 设计**。作者用一个 pilot 实验直接证明这一点：把 VQ-VAE 离散码 vs. Beit v2（VQ-KD，重建高层特征）离散码分别对齐 OPT₂.₇ᵦ 在 CC3M 上训练，COCO 零样本图像描述 CIDEr 分别是 **34.0 vs. 42.0**——高层语义 tokenizer 完胜。于是 SEED 提出两条设计原则（也是全文的灵魂）：

1. **1D 因果依赖**：视觉 token 不应绑定 2D 物理 patch 位置（2D 上下文与 LLM 的单向注意力、文生图的 raster 顺序预测相冲突），而要排成一条带左到右因果依赖的序列，和 LLM 的自回归机制同构。
2. **高层语义**：视觉 token 要和「词」处在同一语义抽象层级（因为在 LLM 里二者要共享权重和训练目标），所以训练时同时优化**判别性（对比学习）**与**重建性**。

把这两条做对，就能让现成 LLM「用它原来的配方（next-word prediction）」无差别地吃多模态数据。SEED 是后续 Tencent ARC 一系列工作（SEED-LLaMA / SEED-X）以及更广义「统一离散 token 多模态」路线的奠基件。

## 模型架构
SEED tokenizer 由 **5 个部件** 串成，其中两端（编码/解码）直接复用预训练大模型、只训中间三件：

```
图 → [ViT 编码器(BLIP-2,冻结)] → 16×16=256 个 2D 特征
   → [Causal Q-Former] → 32 个因果语义 embedding
   → [VQ Codebook(8192)] → 32 个离散视觉码  ← 这就是给 LLM 的 token
   → [Reverse Q-Former] → 77 个 generation embedding (对齐 SD 文本特征空间)
   → [SD-UNet(unCLIP/SD,冻结)] → 重建/生成图像
```

- **ViT 编码器**：直接取自预训练 **BLIP-2** 的视觉编码器（输出 16×16=256 个 raster token），训练中**冻结**。论文未指明该 ViT 的具体规格（BLIP-2 原文用的是 EVA-CLIP ViT-g/14，但本篇未复述，此处不臆断）。
- **Causal Q-Former**（关键创新件）：从 BLIP-2 的 Q-Former 微调而来。32 个可学习 query embedding，**query 之间用带因果 mask 的自注意力**（只能看前面的 query → 这就是 1D 因果依赖的来源），并通过交叉注意力读取冻结的 ViT 图像特征，输出 32 个因果语义 embedding。把"2D raster 顺序"转成了"1D 因果顺序"。
- **VQ Codebook**：码本大小 **8192**，对 32 个因果 embedding 各取最近邻量化 → 32 个离散码。每张图 = 32 token。
- **Reverse Q-Former**（去 tokenize 件）：77 个可学习 query，自注意力 + 对 32 个离散码做交叉注意力，输出 **77 个 generation embedding**，目标是对齐冻结 Stable Diffusion 的**文本特征空间**（SEED-1 对齐的是 SD 的 77-token 文本 embedding；后续 SEED-2 改为对齐 unCLIP-SD 的单个图像 embedding，重建保真度更高，见下"创新与影响"）。
- **SD-UNet 解码器**：现成 Stable Diffusion / unCLIP-SD 的 UNet，**冻结**，吃 generation embedding 出图。

**给 LLM 接线方式（SEED-OPT₂.₇ᵦ）**：把离散视觉码当作"新词"加进词表；用一个全连接层把视觉码线性投影到 OPT 词 embedding 维度，与文本 token 拼接送入 LLM。LLM 主体（OPT-2.7B）**冻结**，只训 LoRA。出图时 LLM 自回归吐出视觉码 → Reverse Q-Former → SD-UNet。

## 数据
- **tokenizer 训练数据**：**5M 公开图文对**，由 **CC3M + Unsplash + COCO** 组成。三个阶段（Causal Q-Former 对比学习、VQ Codebook + Reverse Q-Former 重建）都用这同一份 5M 数据。
- **多模态自回归（SEED-OPT₂.₇ᵦ）数据**：同样是这 **5M 图文对（CC3M / Unsplash / COCO）**，预处理时先把图离散成视觉码再训。
- **评测/对比数据集**：检索用 Flickr30K、COCO；图像描述用 COCO Karpathy test、NoCaps；VQA 用 VQAv2 val、GQA test-dev；pilot 对齐实验用 CC3M 训练、COCO 评测。
- 清洗/过滤/re-caption/合成数据/美学与安全过滤：**论文未披露**（全部使用公开数据集原样）。值得强调的是 **数据极省**——对比 BLIP-2 的 129M，SEED 只用 5M（约 1/26）。
- （README 中提到的「用 GPT-4 改写 InstructPix2Pix 指令、用 GPT-4 基于 MMC4 生成指令」属于后续 **SEED-LLaMA** 的指令微调数据，不是本篇 SEED-1 论文的内容，此处不计入。）

## 训练方法
SEED tokenizer 分**两阶段**训练，LLM 接入是**第三阶段**。全程冻结 ViT 和 SD-UNet，只训 Causal Q-Former / VQ Codebook / Reverse Q-Former（LLM 端只训 LoRA）。

**Stage I — Causal Q-Former（对比学习）**
- 从预训练 BLIP-2 Q-Former 初始化微调。
- 目标：**图文对比损失（contrastive loss）**——最大化"最后一个因果 embedding"与对应 caption 文本特征的相似度，最小化与 batch 内其他 caption 的相似度。
- 作用：让 32 个因果 embedding 抓住判别性的高层语义；同时验证「因果依赖不掉点」。

**Stage II — Visual Quantization + De-tokenization（双重重建）**
- 训 VQ Codebook + Reverse Q-Former，对 Causal Q-Former 输出做量化。
- **双重重建目标**：
  1. **离散码↔连续因果 embedding 的重建**：一个多层 Transformer decoder 从离散码重建连续因果 embedding，训练时**最大化二者余弦相似度**（保住语义/判别信息不被量化丢掉）。
  2. **generation embedding↔SD 文本特征的重建**：Reverse Q-Former 输出的 77 个 generation embedding 与冻结 SD 的文本特征做 **MSE 损失** 对齐（保住生成所需信息）。
- 这一"判别 + 重建"双目标正是设计原则 (2) 的落地——既要能检索（判别）又要能出图（重建）。

**Stage III — 多模态自回归（SEED-OPT₂.₇ᵦ，LoRA）**
- 先做 **image→text 自回归**：视觉码经 FC 投影后，与前缀「A photo of」的词 embedding 拼接送入冻结 OPT-2.7B，目标是预测对应 caption 的下一个文本 token，只训 LoRA。作用是把视觉码本词表对齐到 OPT。
- 再做 **image→text + text→image 联合自回归**：text→image 方向用前缀「Generate an image」+ caption 喂入，目标是预测对应图像的下一个**视觉 token**，仍只训 LoRA。
- 推理：给「Generate an image」+ 文本，LLM 自回归生成视觉码 → Reverse Q-Former → SD-UNet 出图。
- **超参/优化器/学习率等细节**：论文未给出表格（未披露）。

蒸馏 / consistency / 步数蒸馏 / 偏好对齐（RLHF/DPO）：**本篇不涉及**（SEED-1 是 tokenizer 论文，不做生成加速也不做对齐）。

## Infra（训练 / 推理工程）
- **算力**：整套 SEED tokenizer（v1）训练 **5.7 天，64×V100**；下游 SEED-OPT₂.₇ᵦ 的多模态自回归只要 **44 小时，64×V100**（项目主页与 Fig.4 caption 一致）。论文以此强调"低成本、低碳、可规模化"。
- **并行/混合精度/吞吐**：**论文未披露**具体分布式策略。
- **推理 / 部署**：
  - tokenize → 视觉码 → de-tokenize 重建整条链路开源（`scripts/seed_tokenizer_inference.py`）。
  - 出图依赖现成 unCLIP SD-UNet（权重自动下载）。
  - README（属后续 SEED-LLaMA 工程）显示：经 **8-bit 量化 + 动态加载**，SEED-LLaMA-8B/14B 可在单张 **16GB/24GB** GPU 上跑——说明该 token 接口对部署友好（但这是 SEED-2/LLaMA 阶段的数字，非 SEED-1 本身）。
- **训练码**：tokenizer 训练基于 **Salesforce LAVIS** 框架；多模态 LLM 训练码支持 DeepSpeed 多节点大规模训练（2024-02 才放出，属 SEED-LLaMA）。

## 评测 benchmark（把效果讲清楚）
所有数字均出自已抓取的论文正文（ar5iv 全文 Table 1/2/3），未报告项明确标注。

**① 零样本图文检索（Table 1，判别性，Recall@mean，去掉了 BLIP-2 的 ITM rerank 以公平对比）**

| 模型 | Flickr30K I→T R@1 | Flickr30K R@mean | COCO I→T R@1 | COCO R@mean |
|---|---|---|---|---|
| BLIP-2 | 81.9 | 92.9 | 65.3 | 80.3 |
| SEED（因果 embedding，未量化） | **90.0** | **93.7** | **71.9** | **80.7** |
| SEED（因果码，量化后） | 86.3 | 91.7 | 65.7 | 77.4 |

结论：**因果 embedding 的检索性能不输甚至超过 BLIP-2 的双向注意力 embedding**（说明"加因果约束不掉点"）；量化后略有下降但仍有竞争力。

**② 图像生成（Table 2，CLIP 相似度，语义一致性，越高越好）**

| 模型 | COCO | Flickr30K |
|---|---|---|
| GILL | 67.45 | 65.16 |
| SD（上界） | 68.43 | 65.40 |
| **SEED** | 68.23 | 65.22 |

结论：SEED 的重建/生成几乎贴住 SD 上界（COCO 仅差 0.2），并**优于同期的 GILL**。

**③ 下游 SEED-OPT₂.₇ᵦ：零样本图像描述 + VQA（Table 3）**——SEED 用 5M 数据 vs. BLIP-2 用 129M 数据：

| 模型 | NoCaps overall (SPICE) | COCO Karpathy (CIDEr) | COCO (SPICE) | VQAv2 (Top-1) | GQA (Top-1) |
|---|---|---|---|---|---|
| BLIP-2 OPT₂.₇ᵦ（129M 对） | 13.8 | 131.0 | 22.9 | 51.9 | 32.6 |
| **SEED-OPT₂.₇ᵦ（5M 对）** | 12.3 | 119.0 | 22.0 | 42.8 | 28.8 |

结论：在 **约 1/26 的数据量**下，SEED-OPT₂.₇ᵦ 的图像描述/VQA 与 BLIP-2 处于同一量级（CIDEr 119 vs 131；SPICE 22.0 vs 22.9），且**没用任何 VQA 数据训练**就能做开放式 VQA（作者称之为**涌现能力**——区别于 CM3Leon 那样用 caption/VQA 数据做监督微调）。text→image 生成给的是定性示例（Fig.6），无定量 FID/GenEval。

**④ Pilot 消融**：VQ-VAE 离散码对齐 OPT₂.₇ᵦ 后 COCO 描述 CIDEr **34.0**，Beit v2（VQ-KD 高层特征）**42.0**——直接论证"tokenizer 必须抓高层语义"。

未报告：FID、GenEval、T2I-CompBench、DPG-Bench、HPSv2、ImageReward、PickScore、人评 ELO 等生成基准本篇**均未报告**（SEED-1 定位是 tokenizer 可行性验证，生成侧只给 CLIP 相似度 + 定性图）。

## 创新点与影响
**核心贡献**
1. **明确并验证了"LLM 友好视觉 tokenizer"的两条设计原则**：1D 因果依赖 + 高层语义（判别 + 重建双优化）。这是把"离散 token 多模态"从失宠状态重新激活的关键论证。
2. **Causal Q-Former**：用因果 mask 把 2D raster 特征转成 1D 因果序列，使视觉 token 在结构上与 LLM 的左到右自回归同构——既是方法创新，也被实验证明"不掉判别性"。
3. **双重重建 + 复用现成大模型**：ViT/SD-UNet 全冻结，只训中间三件 + LLM 端 LoRA，用极少数据/算力（5M、64×V100、几天）就让现成 LLM 同时会看会画，并**涌现开放式 VQA**。

**对后续工作的影响**
- 直接催生 **SEED-LLaMA**（arXiv 2310.01218，ICLR 2024）：把 SEED 升级为 **SEED-2 tokenizer**（generation embedding 改为对齐 **unCLIP-SD 的单个图像 embedding**，重建保真度显著优于 SEED-1 对齐 77-token 文本 embedding 的做法），并用 LLaMA/Vicuna 做大规模交错图文预训练 + 指令微调，涌现多轮 in-context 图文生成。
- 再到 **SEED-X**（arXiv 2404.14396，2024-04）：转向**连续视觉 embedding**，支持多粒度理解与生成。
- 在更广的语境里，SEED 与同期 Emu（2307.05222）、CM3Leon 一起，是「**用统一离散/连续 token + 自回归 LLM 做多模态理解与生成统一**」这条主线的早期奠基件，影响后续 Chameleon、Show-o、Janus 等统一模型。

**已知局限（作者自述 + 可见）**
- 定位是**初步探索/可行性验证**：未做大规模多模态预训练与指令微调（明确留作 future work），下游用的是小 LLM（OPT-2.7B）+ LoRA。
- 量化后检索性能相对未量化 embedding 有可观下降（COCO R@mean 80.7→77.4）。
- text→image 生成只给定性结果，缺生成质量定量基准。
- SEED-1 的 generation embedding 对齐**文本特征**，重建会丢失图像细节（这正是 SEED-2 改对齐图像 embedding 的动因）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2307.08041
- arxiv_pdf: https://arxiv.org/pdf/2307.08041
- ar5iv_fulltext: https://ar5iv.labs.arxiv.org/html/2307.08041
- github: https://github.com/AILab-CVC/SEED
- project_page: https://ailab-cvc.github.io/seed/seed.html
- huggingface: https://huggingface.co/AILab-CVC/SEED
- 后续工作 SEED-LLaMA: https://arxiv.org/abs/2310.01218 ；SEED-X: https://arxiv.org/abs/2404.14396

## 一手源存档（sources/）
- [arxiv-2307.08041.pdf](https://arxiv.org/pdf/2307.08041) （论文 PDF，6.4MB，本地存档，未入 git）
- [ar5iv-fulltext.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/seed-tokenizer--ar5iv-fulltext.txt) （ar5iv 全文，含全部表格/数字）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/seed-tokenizer--readme.md) （GitHub README 快照）
- [project-homepage.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/seed-tokenizer--project-homepage.md) （项目主页快照，含码本大小 8192/32 token）
