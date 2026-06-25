---
title: "Kosmos-G: Generating Images in Context with Multimodal Large Language Models"
org: "Microsoft Research"
country: US
date: "2023-10"
type: paper
category: unified
tags: [mllm, subject-driven, personalization, zero-shot, image-as-foreign-language, score-distillation, alignernet, kosmos, stable-diffusion]
url: "https://arxiv.org/abs/2310.02992"
arxiv: "https://arxiv.org/abs/2310.02992"
pdf_url: "https://arxiv.org/pdf/2310.02992"
github_url: "https://github.com/microsoft/unilm/tree/master/kosmos-g"
hf_url: ""
modelscope_url: ""
project_url: "https://xichenpan.github.io/kosmosg/"
downloaded: [arxiv-2310.02992.pdf, kosmos-g--readme.md, kosmos-g--project-page.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Kosmos-G（Microsoft Research，ICLR 2024）用一个 1.6B 的多模态大语言模型（MLLM，承接 [[kosmos-1]]）感知**任意交错的多图+文本**输入，再通过一个 ~225M 的 **AlignerNet** 把 MLLM 输出空间对齐到冻结的 Stable Diffusion v1.5 的 CLIP 文本条件空间，从而实现**零样本、免测试时微调、可多主体（multi-entity）的主体驱动生成**——它是首个把零样本主体驱动生成扩展到多主体交错场景的模型；DreamBench 上主体保真度 **CLIP-I 0.847** 甚至略优于微调版 DreamBooth/BLIP-Diffusion，但文本可控性 **CLIP-T 0.287 反而低于** DreamBooth(0.305)/BLIP-Diffusion(0.302)；且因为只换 CLIP 不动 U-Net，可即插即用 ControlNet / LoRA。

## 背景与定位
主体驱动（subject-driven）/ 个性化生成此前两条主流路线都有硬伤：
- **测试时微调派**（Textual Inversion、[[dreambooth]]、Custom Diffusion、Break-A-Scene 等）：每个新主体都要在参考图上重新微调，慢、不可零样本、难扩展到多主体。
- **特征注入派**（ELITE、FastComposer、Re-Imagen、[[blip-diffusion]] 等）：把图像特征注入 U-Net，但**把图、文引导割裂**，难以联合建模图文，更难扩展到多个实体。BLIP-Diffusion 虽能零样本，但其输入模板与训练数据设计限制了它向多实体的扩展。

Kosmos-G 的核心主张是"**image as a foreign language in image generation**"（把图像当作一门外语喂进生成）。它不去改 CLIP 文本编码器，而是直接用一个**预训练 MLLM** 替换 CLIP：理由有三——(1) 复用 MLLM 内部已对齐的视觉-语言表征；(2) MLLM 架构天然支持交错多图+文本输入；(3) 预训练 MLLM 能在上下文中建模多模态输入。技术脉络上它处在 [[latent-diffusion-ldm]] / [[stable-diffusion]] 之上、与 [[gill]]、[[emu-multimodal]]、[[dreamllm]] 等"MLLM 接图像解码器"的统一生成工作同期，但 Kosmos-G 专注于**主体保真的条件生成**而非自回归出图像 token。

## 模型架构
整体由三部分组成（橙=可训练，蓝=冻结）：

**1) MLLM 主干（承接 Kosmos-1）**——基于 Transformer 的因果（left-to-right）语言模型，作为多模态输入的通用接口：
- 输入序列用特殊 token 统一编码：`<s>`/`</s>` 标记序列起止，`<image>`/`</image>` 标记图像嵌入的起止。文本 token 走 lookup table；图像走一个 **ViT 视觉编码器**（用预训练 **CLIP ViT-L/14**，1024 维特征，输入 224×224），再经 **Resampler**（Flamingo 式 attentive pooling）压缩图像 token 数量。
- 解码器：**24 层、隐藏维 2048、FFN 中间维 8192、32 注意力头**，自回归处理序列，softmax 分类头预测下一个 token。训练损失**只对离散文本 token 计算**。
- backbone 用 **MAGNETO**（Foundation Transformer 变体，与 Kosmos-1 一致）以保证大规模训练稳定。
- **MLLM 总参数 ~1.6B**（论文正文原话 "about 1.6B"）。论文表 1 里 COCO 行把模型记作 **KOSMOS-G-1.9B**——该整体口径推测为 MLLM(~1.6B) + AlignerNet(~225M) ≈ 1.8B 取整，但论文未明确拆解 1.9B 的构成。CLIP 除最后一层外其余冻结。

**2) AlignerNet（~225M，本文新组件）**——把 MLLM 的输出空间 S 桥接到 CLIP 文本编码器目标空间 T（也即 SD U-Net 的条件输入空间）。由编码器 M 和解码器 N 组成，二者各是一个 **12 层 Transformer encoder + 12 层 Transformer decoder**，输入维 d=768、隐藏维 3072。
- 因为 MLLM 对交错多图文本输出的是**变长嵌入**，GlueNet（GlueGen）那种 MLP 对齐不适用，所以 AlignerNet 用 Transformer 架构 + **变长可学习 latent query**（M 中 Q_M∈R^{l_t×d}，N 中 Q_N∈R^{l_s×d}）在 cross-attention 里匹配不同的序列长度与嵌入维度。
- 用线性层把 MLLM 输出维投到 d=768。

**3) 图像解码器（冻结）**——**Stable Diffusion v1.5 的 U-Net + VAE 全程冻结，不改任何架构与权重**。Kosmos-G 仅替换掉原 SD 的 CLIP 文本编码器。正因解码器冻结、且接口仍是 CLIP 文本空间，Kosmos-G 能无缝叠加 ControlNet、社区 LoRA 等一切针对 SD U-Net 的技术。

## 数据
**阶段一（多模态语言建模）**：与 Kosmos-1 同设置，网页级多模态语料——纯文本语料 + 图文对 + 图文交错数据。

**阶段二（图像解码器对齐）**：只用图文对里的 **caption（纯文本）**来训练 AlignerNet。

**阶段三（指令微调）的构造数据**：
- **图文对来源**：English LAION-2B、LAION-400M、COYO-700M、Conceptual Captions（CC3M/CC12M）——均从 Common Crawl 提取图像 + alt-text。
- **组合生成（compositional）指令数据构造管线**（图 4）：取 **Open Images V7 约 9M 张图**→ 用 **BLIP-2-OPT-6.7B** 生成 caption → 用 **MPT-7B-Instruct** 从 caption 中抽取实体（tags）→ 用文本提示分割模型 **CLIPSeg** 对每个实体名得到对应的分割图。最终数据形如 `<s> A cat <image>猫的图像嵌入</image> and a dog <image>狗的图像嵌入</image> sleeping in the garden <image>花园嵌入</image> </s>`。
- **编辑数据**：复用 InstructPix2Pix 构造的图像编辑数据，格式 `<s> caption <image>原图嵌入</image> 编辑指令 </s>`，以增强编辑能力。
- 还混入部分纯文生图数据，保持已有的语言对齐。
- **数据增强 / 鲁棒性**：构造数据里以 0.5 概率随机丢弃实体文本；以 0.5 概率保留被分割实体的背景。
- **安全过滤**：对训练数据做了严格过滤，清除露骨图像与冒犯性语言（Ethics 声明）。

## 训练方法
"**align before instruct**"，三阶段：

**阶段一 多模态语言建模**——从零预训练 MLLM（next-token prediction，最大化 token 对数似然，仅文本 token 计损）。超参（附录 A）：batch **120 万 token**（文本 0.5M + 图文对 0.5M + 交错 0.2M），训 **300,000 步 ≈ 3600 亿 token**；AdamW（β=0.9/0.98）、weight decay 0.01、dropout 0.1；峰值 lr 2e-4，375 步 warm-up 后线性衰减到 0；SentencePiece 分词，full-sentence 拼接。

**阶段二 图像解码器对齐**——**冻结 MLLM，只训 AlignerNet**，且**只用纯文本 caption**。文本作"锚"：用编码器 M 把 Kosmos-G 文本源嵌入 s 拉近 CLIP 文本目标嵌入 t（L_mse = ‖t − M(s)‖²），用解码器 N 重建源嵌入（L_rec，防止特征判别性塌缩）。因为图文在 MLLM 内已对齐，仅对齐文本即可**让图像嵌入也自然对齐**到解码器输入空间。超参：batch **3584 句**、训 300,000 步 ≈ 10 亿句、峰值 lr 1e-3。

**阶段三 组合指令微调（score distillation instruction tuning）**——**MLLM 与 AlignerNet 联合训练，解码器全程冻结**。目标用冻结 SD U-Net 上的标准 **diffusion loss**（L_diff = E‖ε − ε_θ(z_t,t)‖²），但其梯度本质等价于 **Score Distillation Sampling（SDS，承自 DreamFusion）**：把冻结 U-Net 当作 score metric，将其已学到的数据分布**蒸馏**进 Kosmos-G（等价于最小化条件分布与 score function 之间的 KL）。直观上像在"预训练一个泛化版 Textual Inversion"，所有条件都可学。这一步让模型不再只停留在语义层，而能利用图像编码器的**细粒度特征忠实复现实体**。
- 三类数据配比 **构造数据 : InstructPix2Pix : caption = 2:2:1**。
- 超参：batch **1024 张图**、训 200,000 步 ≈ 2 亿张图、峰值 lr 1e-3。

**关键设计取舍**：作者发现直接端到端用 diffusion 梯度微调 MLLM 会导致"平凡对齐 + 画质受损"；引入 AlignerNet + CLIP 监督才接近原版 SD（见消融）。也可在 AlignerNet 帮助下直接用 diffusion loss 端到端对齐，但更费算力且同等 GPU-days 下效果更差。

## Infra（训练 / 推理工程）
- **算力**：整个训练（阶段二+三）约 **4 天 × 256 张 NVIDIA V100**——其中图像解码器对齐 1 天、指令微调 3 天。（阶段一 MLLM 预训练算力论文未单列。）
- **框架**：基于 Microsoft **TorchScale** 大规模训练库；backbone 用 MAGNETO/Foundation Transformer；开源实现依赖 torchscale / fairseq / open_clip / infinibatch（README）。
- **推理**：DreamBench 评测用 CFG scale **7.5 + 100 步 DPM-Solver**；MS-COCO 文生图用 CFG scale **3.0 + 250 步 DDIM**。提供 Gradio 本地 demo（`runapp.sh`），并放出 stage1/stage2/final 三个 checkpoint。
- **部署形态**：纯研究项目，官方明确**不打算产品化或对外开放访问**。

## 评测 benchmark（把效果讲清楚）
**DreamBench（单实体主体驱动，30 主体 × 25 模板 = 750 prompt，每 prompt 生 4 图共 3000 图；DINO/CLIP-I 测主体保真，CLIP-T 测文本保真）**——Kosmos-G 只输入单张参考图（从 4–7 张里挑无遮挡的清晰图），并轻改 prompt 模板以贴合训练数据分布：

| 方法 | 类型 | DINO↑ | CLIP-I↑ | CLIP-T↑ |
|---|---|---|---|---|
| Real Images (Oracle) | — | 0.774 | 0.885 | — |
| Textual Inversion | 微调 | 0.569 | 0.780 | 0.255 |
| DreamBooth | 微调 | 0.668 | 0.803 | 0.305 |
| BLIP-Diffusion | 微调 | 0.670 | 0.805 | 0.302 |
| Re-Imagen* | 免微调 | 0.600 | 0.740 | 0.270 |
| SuTI* | 免微调 | 0.741 | 0.819 | 0.304 |
| BLIP-Diffusion* | 免微调(零样本) | 0.594 | 0.779 | 0.300 |
| **Kosmos-G*（单图输入）** | 免微调(零样本) | **0.694** | **0.847** | **0.287** |

（* = 零样本方法）结论：零样本 Kosmos-G **超过 Textual Inversion、Re-Imagen**，在 **CLIP-I（0.847，全表最高的非 Oracle 值）** 上甚至略优于微调版 DreamBooth/BLIP-Diffusion，整体与 SuTI 相当但**无需昂贵的 apprenticeship learning 监督**；CLIP-T 稍逊于 DreamBooth/SuTI。

**MS-COCO（2014 val，3 万随机 caption，零样本 FID）**——与其他 CLIP-aligned VL2I 模型比：

| 模型 | FID↓ |
|---|---|
| GILL-8B | 12.20 |
| Emu-14B | 11.66 |
| **Kosmos-G-1.9B** | **10.99** |

Kosmos-G 在同类 CLIP-aligned VL2I 模型里 FID 最优。（作者自测的 SD v1.5 在同种子同设置下 FID 9.34，作为参照而非可比项，因为 Kosmos-G 接的就是 SD v1.5 解码器。）

**消融（MS-COCO FID，验证 AlignerNet 与对齐策略的必要性）**：
| 设置 | FID↓ |
|---|---|
| SD v1.5（参照） | 9.34 |
| E2E 不带 AlignerNet | Failed（无法生成有意义图像）|
| E2E 带 AlignerNet | 11.30 |
| 12 层 decoder-only | Failed |
| 12 层 AlignerNet | 9.89 |
| 24 层 AlignerNet | 9.55 |

结论：(1) 直接端到端微调或仅用 decoder 架构**完全失败**；(2) 引入 AlignerNet + CLIP 监督后效果接近原版 SD；(3) 端到端虽可行但因额外算 U-Net 而更贵、同 GPU-days 下更差；(4) AlignerNet 层数越深效果越好（24 层优于 12 层）。另有定性消融（图 6）：不做指令微调时，Kosmos-G 只能生成"语义对齐但实体不忠实"的图，SD baseline 同样停在语义层无法复现实体。

**定性结果**：图 1/5/9 展示重上下文化、风格化、改装、配饰添加，以及 **3–4 张图交错的多实体场景**——后者即便对 DreamBooth 这类微调方法也极难，Kosmos-G 是首个零样本做到的模型。

## 创新点与影响
**核心贡献**：
1. **用 MLLM 做主体驱动生成**：把交错多图+文本统一当"外语"喂给预训练 MLLM，复用其内生视觉-语言对齐，天然支持多图上下文。
2. **组合指令微调任务**：caption + 实体分割图交错的训练格式，解锁**零样本多实体**主体驱动生成（业界首次）。
3. **Score distillation instruction tuning**：训练时**不改图像解码器一个参数**，使 Kosmos-G 成为 CLIP 的**即插即用替代**——可无缝叠加 ControlNet（canny 等条件控制）、社区 LoRA 等任意 SD U-Net 生态技术（图 7 验证）。

**影响**：把生成的条件接口从"文本条件"推向"视觉-语言条件"，是 2023 年"MLLM 对齐扩散解码器以做统一生成/个性化"这一波（[[gill]] [[emu-multimodal]] [[dreamllm]] [[blip-diffusion]]）中专攻**主体保真 + 多图上下文**的代表作；"冻结解码器、只对齐编码侧"的范式对后续可插拔个性化模块有借鉴意义。被 ICLR 2024 接收，代码并入 microsoft/unilm。

**已知局限**：
- 解码器锁死在 **SD v1.5（512 分辨率级、U-Net）**，未升级到 SDXL / DiT；天花板受 SD v1.5 限制。
- CLIP-T（文本可控性）略逊于 DreamBooth/SuTI；prompt 前缀（如 "a"）会影响编辑/定制表现（与 BLIP-2 captioner 习惯写 "a photo of" 有关）。
- 评测仍偏 DreamBench/COCO 的传统指标（DINO/CLIP-I/CLIP-T/FID），未涉及后来的 GenEval/DPG-Bench/人评 ELO 等。
- 官方不产品化、不开放公测，仅研究用途。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.02992
- arxiv_pdf: https://arxiv.org/pdf/2310.02992
- project_page: https://xichenpan.github.io/kosmosg/
- github（官方代码，已并入 unilm）: https://github.com/microsoft/unilm/tree/master/kosmos-g
- github（作者原 repo，重定向到 unilm）: https://github.com/xichenpan/Kosmos-G

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2310.02992.pdf
- ../../../sources/omni/2023/kosmos-g--readme.md
- ../../../sources/omni/2023/kosmos-g--project-page.md
