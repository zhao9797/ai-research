---
title: "Emu: Generative Pretraining in Multimodality"
org: "BAAI (智源) + 清华 THU + 北大 PKU"
country: China
date: "2023-07"
type: paper
category: unified
tags: [unified, autoregressive, lmm, multimodal-generation, interleaved, video-text, eva-clip, llama, stable-diffusion, in-context-learning]
url: "https://arxiv.org/abs/2307.05222"
arxiv: "https://arxiv.org/abs/2307.05222"
pdf_url: "https://arxiv.org/pdf/2307.05222"
github_url: "https://github.com/baaivision/Emu"
hf_url: "https://huggingface.co/BAAI/Emu"
modelscope_url: ""
project_url: "https://emu.ssi.plus/"
downloaded: [arxiv-2307.05222.pdf, emu-multimodal--readme.md, emu-multimodal--emu1-readme.md, emu-multimodal--hf-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Emu（智源 BAAI，2023-07，ICLR 2024）是一个 14B 的多模态基础模型，用**统一自回归目标**在图文/视频交错序列上「预测下一个元素」——文本 token 走交叉熵分类、连续视觉 embedding 走 ℓ2 回归——从而**同一个模型既能理解又能生成图像**。零样本 COCO captioning CIDEr 达 112.4（大幅领先同期 Kosmos-1/Flamingo-9B），指令微调版 Emu-I 仅 14B 即在 VQAv2(62.0)、VizWiz(38.3)、MSVDQA(37.0) 上超过 Flamingo-80B（56.3/31.6/35.6），并在 MM-Vet(36.3) 上超过 LLaVA-65B(35.5)。

## 背景与定位
2023 年主流大型多模态模型（LMM，如 Flamingo、Kosmos-1、BLIP-2/InstructBLIP、LLaVA、MiniGPT-4）的范式是：**冻结视觉编码器 + LLM，只在文本 token 上算 next-token loss，视觉端无监督**。这有两个局限：(1) 视觉部分得不到生成式监督，限制了模型容量与图像生成能力；(2) 训练数据多为图文 pair 或文档，**忽视了视频这一天然的、规模可扩展的交错多模态数据源**（视频帧 + 字幕本身就是按时间戳排序的图文交错序列）。

Emu 的核心主张：把所有模态（文本 token、连续图像 embedding、视频帧）统一成**一条交错序列**，用「预测下一个元素」的单一自回归目标端到端训练，让**视觉信号也进入 loss**。这样既能吃下 image-text pair、交错文档（MMC4）、video-text pair，还能吃下作者新引入的**交错视频-文本数据 YT-Storyboard-1B**，并让同一个模型成为「图生文 + 文生图」双向的 generalist interface，天然带 in-context（少样本）图像/文本生成能力。

技术脉络上，Emu 是「**用连续视觉 embedding 做生成式统一**」路线的早期代表，与同期 DreamLLM、GILL、Kosmos-G 等并列；区别于后来 Chameleon/[[chameleon-cm3leon]]、Emu3 走的「把图像也离散化成 token、纯 next-token」路线——Emu1 刻意**不在像素空间做离散 token 自回归**，而是回归连续 embedding，再用 [[latent-diffusion-ldm]]（Stable Diffusion v1.5）把 embedding 解码成图像。它直接复用 EVA-CLIP（视觉编码）、LLaMA-13B（多模态建模）、SD v1.5（视觉解码）三个预训练模块拼装而成。

## 模型架构
Emu 由四部分组成（论文 Fig.2）：

1. **Visual Encoder（视觉编码器）**：EVA-01-CLIP 的 1B 版本（40 层 ViT），把图像/视频帧编码成密集视觉特征。**输入分辨率固定 224×224**。注意是**连续特征，不离散化**。
2. **Causal Transformer（因果变换器）**：本工作的关键设计。原始图像是 2D 结构、缺乏文本那样的从左到右因果依赖，直接按 raster 顺序自回归效果差。该模块把 2D 空间视觉信号转成 **1D 因果潜空间序列**：以 EVA-CLIP 编码 g(I) 作为 condition，接受一组随机初始化 embedding {e1…eN} 作 query，经 **causal self-attention → cross-attention（视觉 embedding 作 key/value）→ FFN** 输出 N 个捕获因果依赖的视觉 embedding {z1…zN}。共 **12 个 block**，随机初始化。视频的 T 帧编码为 T×N 个因果 embedding。每张图像/帧前后加 `[IMG]` / `[/IMG]` 特殊 token。
3. **Multimodal Modeling LLM（多模态建模主干）**：LLaMA-13B（decoder-only Transformer），用其权重初始化。视觉因果 embedding 与文本 token 交错成序列，序列首尾加 `<s>`/`</s>`，统一自回归建模。**文本走 language modeling head 分类，视觉走单独 regression head 回归**。
4. **Visual Decoder（视觉解码器）**：用 Stable Diffusion v1.5 初始化的 latent diffusion model。把 Emu 生成的 N 个视觉 embedding 作为条件喂给扩散模型解码成真实图像——具体做法是**把 SD 的 cross-attention 里原来接 text embedding 的线性投影换成新线性层**，以适配 Emu 的 embedding 维度。冻结视觉编码器、LLM 与 SD 的 VAE，**仅训练 U-Net**。

参数量：总计 **14B，端到端训练**（视觉编码器 1B + Causal Transformer + LLaMA-13B；视觉解码器 U-Net 单独 finetune）。视觉 token 数为「固定数量 N」——论文正文与附录均以符号 N 描述，**未在主文给出 N 的具体数值**（按此系列实现通常 N=32，但原文未明示，此处标注未明确报告）。

生成接口：给定多模态上下文，若期望输出文本 → 用 LM head 自回归生成文本 token；若期望输出图像 → 在序列末尾追加 `[IMG]` token，模型自回归生成 N 个视觉 embedding，再送视觉解码器解码成图像。

## 数据
Emu 预训练混合四类、共约 **82M 样本 / 150B token**：

- **图文 pair**：**LAION-2B**（LAION-5B 英文子集，含网络噪声 alt-text）+ **LAION-COCO**（LAION-2B 的 600M 子集，用 BLIP+CLIP ensemble 重新 caption，文本更流畅但语义/世界知识多样性下降）。两者并用以兼顾流畅度与世界知识。
- **视频-文本 pair**：**WebVid-10M**。用启发式规则去掉无关元数据（原视频分辨率、相机参数等）；约 100 万条需清洗，先用词表过滤，再用 **Vicuna-13B 改写** 提升流畅度与质量。
- **交错图文文档**：**MMC4（Multimodal-C4）**，约 75M 文档、400M 图像、38B token。沿用 OpenFlamingo 的做法按 **CLIP 相似度阈值 0.32** 过滤图像；每文档采样长度 L=1024、取前 N=5 张图，另采样 N=5 图+对应句子构成 L=512 子序列。
- **交错视频-文本（本工作新建）YT-Storyboard-1B**：用 YT-Temporal-1B 提供的 video-id，从 YouTube 抓取 **18M 视频** 的 **storyboard 缩略图（约 1.8B 张）+ 字幕文件**。storyboard 缩略图采样间隔固定，字幕带起止时间戳，二者按时间戳排序、相邻字幕合并，构成天然的图文交错序列。采用 storyboard 而非原始视频可**免去视频解码、存储成本降低约 20 倍**。

视觉解码器训练数据：**LAION-COCO（高图文相关性）+ LAION-Aesthetics（高美学质量）**，配比 **7:2**；过滤掉文本长度 >150 的 prompt（弃 ~8% LAION-Aesthetics、~0.01% LAION-COCO）。

指令微调数据（公开数据集组合）：语言指令 ShareGPT(~70K)、Alpaca(52K)；图像指令 LLaVA（conversation/detailed-description/complex-reasoning 三类）；视频指令 VideoChat、Video-ChatGPT。

## 训练方法
**统一自回归目标**：对交错多模态序列 u=(u1…um)，最大化 ∑ log P(ui | u<i; θ)。两类 loss：
- **文本 token → 交叉熵分类 loss**（LM head，在预定义词表上）；
- **连续视觉 embedding → ℓ2 回归 loss**（独立 regression head）。

注意 Emu **不在原始像素空间做生成式预训练**，而是先用 Causal Transformer 把 2D 图像转成 1D 因果潜 embedding，再插回序列对应位置，对这些连续 embedding 算回归 loss——这是它与「图像离散化 + next-token 分类」路线的根本差异。

**训练分三阶段**：
1. **预训练**（端到端 14B）：iterations 10k；各数据集 batch size 分别 128/128/64/16/16（LAION-2B / LAION-COCO / MMC4 / WebVid-10M / YT-Storyboard-1B）。每个视频随机采 8 帧；图文 pair/交错数据中图像随机放在句子前或后。学习率：视觉编码器 peak 4e-5、LLaMA 3e-5、Causal Transformer 1e-4；warmup ratio 0.2、cosine decay；AdamW(β=0.9/0.98, ε=1e-6)、weight decay 0.05。
2. **视觉解码器微调**：冻结视觉编码器/LLM/VAE，**仅训 U-Net** 把视觉 embedding 解码成图像（文生图任务）。iterations 15k；batch size 50×4×8；分辨率 512×512；学习率前 5k warmup 到 1e-4，10k/14k 处降到 5e-5/1e-5；ε-prediction 目标；AdamW(β=0.9/0.999)、weight decay 1e-2。**训练时 10% 概率丢弃 image embedding 条件，以支持 classifier-free guidance**。
3. **指令微调（Emu-I）**：冻结全部预训练参数，**只训 LoRA 模块**，且 LoRA 只挂在 LLM 的 self-attention 层（不动视觉编码器，因指令对齐与视觉特征关系不大）。模板 `<System Message> [USER]: <Instruction> [ASSISTANT]: <Answer>`，`[USER]`/`[ASSISTANT]` 特殊 token 用 'user'/'assistant' 词嵌入初始化，**只对 `<Answer>` 算 loss**。

**未涉及**偏好对齐（RLHF/DPO/reward model）与步数蒸馏/一致性蒸馏——属同期未做范畴。

## Infra（训练 / 推理工程）
- **预训练算力**：128× NVIDIA A100-80G，10k steps，约 82M 样本 / 150B token，**约 2 天** 完成。
- **视觉解码器**：32× A100-40G，15k iterations。
- **推理**：文生图用 PNDM scheduler、50 步；采用 classifier-free guidance，scale factor Emu 设 5.0（对比 SDv1.5 设 3.0）。
- 并行策略、混合精度、吞吐、量化、部署形态等**未在论文披露**。模型权重已开源：Emu w/ Decoder（HF，约 34GB）、Emu-I（约 27GB），受 LLaMA-1 license 约束。

## 评测 benchmark（把效果讲清楚）
**零样本多模态理解（Table 1，CIDEr/Acc，* 表示用两条去掉图像的文本示例做 prompt）**：
- COCO captioning CIDEr：**Emu 112.4 / Emu\* 120.4**（NoCaps 96.5/108.8，Flickr30K 72.0/77.4），大幅领先 MetaLM(82.2)、Kosmos-1(84.7)、Flamingo-9B(79.4)。
- VQAv2：Emu 52.0 / Emu\* 52.9 / **Emu-I 57.2 / Emu-I\* 62.0**；OKVQA 38.2/42.8/43.4/49.2；VizWiz 34.2/**34.4**/32.2/**38.3**（vs Kosmos-1 29.2、Flamingo-9B 28.8）；VisDial 47.4/47.8/43.0/51.1。
- 视频 QA：MSVDQA 18.8/34.3/34.6/37.0；MSRVTTQA 8.3/17.8/16.8/21.2；NExTQA 19.6/23.4/5.8/19.9（注：Emu-I 无 * 时 NExTQA 仅 5.8，加文本示例 prompt 后回到 19.9，疑为输出格式问题，原文未解释）。
- **关键结论：仅 14B 的 Emu-I 在多项上超过 Flamingo-80B**——VQAv2 62.0 vs 56.3、VizWiz 38.3 vs 31.6、MSVDQA 37.0 vs 35.6。

**MM-Vet 实景能力（Table 4，5 次评测均值±std）**：Emu-I-14B 总分 **36.3±0.3**，超过 DreamLLM-7B(35.9)、LLaVA-65B(35.5)、InstructBLIP-14B(25.6)、MiniGPT-4-14B(24.4)；分项 Rec 45.5（最高）、Know 36.7（最高）、Gen 35.9（最高），但 OCR(19.2)、Spat(25.2)、Math(3.8) 偏弱。

**零样本文生图（Table 2，MS-COCO val 随机 30k prompt 算 FID↓）**：**Emu FID 11.66**，优于同为「LLM 生图」的并发工作 GILL(12.20)、GLIDE(12.24)、Make-A-Scene(11.84)；但**仍逊于 SDv1.5(9.93)、DALL·E 2(10.39)、Imagen(7.27)、Parti(7.23)**。作者归因：视觉解码器的条件空间（image embedding）偏离了 SD 初始化所用的条件空间（text embedding），且只训了较短的 15k steps。

**少样本（Table 3，RICES 选例，k=2/4/8）**：Emu 几乎在所有场景优于 Flamingo-9B 与 Kosmos-1。如 VQAv2 4-shot 58.4（+2.1 vs Flamingo-9B）、VizWiz 4-shot 41.3（+6.4）、MSRVTTQA 4-shot 21.8 vs Flamingo 18.2；shot 数 k 与性能正相关，验证 in-context 学习能力。

**消融（Table 6，Emu-7B w/ vs w/o YT-Storyboard-1B）**：加入交错视频-文本数据后，COCO 110.8→112.9、MSVDQA 16.9→17.9、MSRVTTQA(4-shot) 19.9→20.8 等普遍提升，且 4-shot 提升更明显——**证明引入交错视频数据既提零样本也增强 in-context 能力**。

## 创新点与影响
**核心贡献**：
1. **统一自回归目标覆盖视觉**：首批在交错序列上对**文本(分类) + 连续视觉 embedding(回归)** 同时算 loss 的工作，让视觉端获得生成式监督，使**理解与生成统一在一个模型**里。
2. **Causal Transformer**：把 2D 图像编码转成 1D 因果潜序列，规避「像素 raster 顺序自回归」的不自然，是连续 embedding 路线下统一建模的关键模块。
3. **video 作为可扩展交错数据源 + YT-Storyboard-1B**：用 storyboard 缩略图+字幕构造图文交错序列，免视频解码、省 20× 存储，并经消融验证有效。
4. **generalist interface + in-context 双向生成**：同一接口完成 caption / VQA / video-QA / 文生图，并涌现 in-context 图文生成、image blending（猫+虎合成「虎猫」）等新能力。

**影响**：Emu 是「连续视觉 embedding 统一生成」路线的代表作之一，与 DreamLLM/GILL/Kosmos-G 并立，直接催生了后续 **Emu2**（CVPR 2024，更大规模、in-context learner）与 **Emu3**（2024-09，转向纯 next-token 离散化路线）。它把「视频交错数据」推上多模态预训练的重要数据源位置。代码/权重开源（github.com/baaivision/Emu，权重受 LLaMA-1 license 约束）。

**已知局限（作者明示）**：与其它 LMM 一样易产生视觉/语言幻觉；自回归推理慢；预训练后知识不再更新；文生图 FID 仍逊于专用扩散模型（SDv1.5/Imagen），归因于条件空间偏移与解码器训练步数短；OCR/空间/数学能力弱；以英文数据为主，多语言能力薄弱。模型定位为研究用途，需先做风险分析再落地应用。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2307.05222
- arxiv_pdf: https://arxiv.org/pdf/2307.05222
- github: https://github.com/baaivision/Emu （Emu1 子目录 https://github.com/baaivision/Emu/tree/master/Emu1）
- hf: https://huggingface.co/BAAI/Emu
- demo/project: https://emu.ssi.plus/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2307.05222.pdf
- ../../../sources/omni/2023/emu-multimodal--readme.md （仓库顶层 README）
- ../../../sources/omni/2023/emu-multimodal--emu1-readme.md （Emu1 子目录 README）
- ../../../sources/omni/2023/emu-multimodal--hf-card.md （HF BAAI/Emu model card）
