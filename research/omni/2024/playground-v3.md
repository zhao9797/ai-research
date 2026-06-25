---
title: "Playground v3: Improving Text-to-Image Alignment with Deep-Fusion Large Language Models"
org: Playground
country: US
date: "2024-09"
type: tech-report
category: t2i
tags: [t2i, diffusion, dit, deep-fusion, llm-text-encoder, llama3, graphic-design, text-rendering, capsbench, closed-source]
url: "https://arxiv.org/abs/2409.10695"
arxiv: "https://arxiv.org/abs/2409.10695"
pdf_url: "https://arxiv.org/pdf/2409.10695"
github_url: ""
hf_url: "https://huggingface.co/datasets/playgroundai/CapsBench"
modelscope_url: ""
project_url: "https://playground.com/pg-v3"
downloaded: [arxiv-2409.10695.pdf, playground-v3--capsbench-readme.md, playground-v3--blog.md, playground-v3--landing.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Playground v3（PGv3）是 Playground 推出的 24B 参数 DiT 文生图模型，核心创新是把一个冻结的 decoder-only LLM（Llama3-8B）以 **Deep-Fusion** 方式逐层"克隆并对接"进扩散主干——图像 Transformer 的每一层都从 LLM 对应层取 hidden states 做条件，彻底抛弃 T5/CLIP 文本编码器。配套自研 VLM 标注器（论文称 PG Captioner，产品名 Argus）做多级 re-caption，并发布细粒度图像描述评测 **CapsBench**。最亮眼结果：自建 DPG-bench Hard 上总分 **88.62%**（超 Flux-pro 78.69、Ideogram-2 80.12），文字合成准确率 **82%**，GenEval 0.76（>SD3 0.74），且在图形设计用户偏好上"超越人类设计师"。模型闭源（权重未发布），仅 CapsBench 评测集开源。

## 背景与定位
2023 年以来文生图主干从 [[unet]]/[[latent-diffusion-ldm]] 的 U-Net 转向 Transformer（[[dit]]）。提升"提示词跟随（prompt-following）"的主流路线有二：(1) 用 LLM 替换 T5/CLIP 当文本编码器；(2) 用 LLM 改写/扩写提示词喂给基于 T5/CLIP 的模型（如 ELLA、DALL·E 3 的 re-caption）。PGv3 走第一条路并推到极致：**完全不用任何 NLP 编码器（无 T5、无 CLIP）**，从训练第一步起就只靠 Llama3-8B 提供文本条件。

作者的论点是：T5/CLIP 通常只取最后一层（或倒数第二层）输出，但 Transformer 各层捕捉不同层级（词级/句级）的表征，"选哪几层做条件"在 decoder-only LLM 上尤其难调；而 LLM 的生成能力来自信息在**所有层**的连续流动，知识分散在全部层而非某一层。因此 PGv3 干脆复刻 LLM 的全部 Transformer block，让图像模型逐层吃 LLM 对应层的 hidden embedding，"完整利用 LLM 的思考过程"。这是相对 [[dall-e-3]]（re-caption）、[[stable-diffusion-3]]（MMDiT + T5/CLIP）、[[pixart-alpha]]/PixArt-Σ（T5）等同期工作的关键差异化。承接自家 [[playground-v2-5]]（PGv2.5）的美学/多宽高比经验。

## 模型架构
- **主干**：DiT 风格扩散 Transformer，规模 **24B 参数**（仅指训练的图像分支；LLM 部分冻结不算入可训练）。基于 [[latent-diffusion-ldm]] 框架，用 [[elucidating-edm]] 公式化（继承 PGv2.5，未转 flow matching）。
- **Deep-Fusion 文本条件（核心创新）**：图像模型每个 Transformer block 与所用 LLM（Llama3-8B）的对应 block **结构完全一致**——hidden 维度、注意力头数、头维度全部对齐。训练只更新图像分支，LLM 全程冻结。扩散采样时 **LLM 只需前向跑一次**生成所有中间层 hidden embedding 供图像分支逐层取用，推理开销可控。
- **简化的 block 与 joint attention**：每个 block 只含 1 个 attention 层 + 1 个 FFN 层（镜像 Llama3）。不像传统 CNN 扩散把图像 self-attn 与图文 cross-attn 分开，PGv3 用**单次 joint attention**：图像 query 同时 attend 到 [图像 key ‖ 文本 key] 的拼接，从合并池里取特征。作者指出这与晚于其定稿发表的 [[stable-diffusion-3]] 的 MMDiT 精神相近（图文跨全层持续交互），但 PGv3 更极简、文本编码器利用得更彻底。
- **架构 trick**：
  - **U-Net skip connection**：在所有图像 block 间加 U-Net 式跳连（参考 U-DiT）。
  - **中间层 token 下采样**：32 层中，中间层把图像 key/value 序列长度缩短 4 倍，使整网像只有一级下采样的卷积 U-Net，略加速训练/推理且无性能损失。
  - **位置编码**：用 2D RoPE。对比两种 2D-RoPE 变体——"interpolating-PE"（固定首尾位置 ID、中间插值，SD3 等用）会**严重过拟合训练分辨率、无法泛化到未见宽高比**；"expand-PE"（位置 ID 随序列长度线性增长、无归一化技巧）表现好、无分辨率过拟合。最终采用 expand-PE。
- **VAE**：自研 16 通道 VAE（继承 Emu 的 4→16 通道思路），不只在 256×256 训练，扩到 512×512 进一步提升重建。尝试过 Emu 的频率方法、用 CLIP/DINOv2 预训练图像编码器做 VAE——后者重建相当但 latent 空间会让扩散训练不稳定，遂放弃。
- **文本编码器**：Llama3-8B（decoder-only），冻结。还支持多语言（见下）。

## 数据
- 论文未披露训练数据总规模、来源、配比与清洗/安全过滤细节（闭源产品，仅给方法层面信息）。
- **多级 re-caption（关键数据方法）**：自研 VLM 标注器（PG Captioner / 产品名 **Argus**）给每张图生成 **6 种不同长度**的描述，从细粒度细节到粗概念。训练时每次迭代为每张图**随机采样其中一条**。目的：让模型学到更好的语言概念层级——既学词与图的对应，也学词之间的语义层级与关系；从而短提示词下输出更多样（风格/色调/人种等变化），长详细提示词下贴合度更高。在 SFT 等小数据阶段，多级 caption 还能防过拟合、把 SFT 数据的好画质泛化到其他图像域。
- **图形设计评测数据**：收集约 **4k** 张人类设计师在常见图形设计场景（monogram/sticker/T-shirt/mockup/壁纸/logo/卡片/海报等）做的高质量图，作为"人类设计师平均水平"的 ground truth。
- **多语言**：作者称多语言能力只需"几万张"多语言图文对即可充分激发（得益于 LLM 文本编码器天然跨语言对齐）；但**未在非英文文字渲染数据上训练**，因此模型通常不识别/不生成其他语言的文字（图中文字）。

## 训练方法
- **目标/噪声调度**：扩散，沿用 **[[elucidating-edm]] 噪声调度**（同 PGv2.5），未转 flow matching（作者称只是没遇到 EDM 的性能瓶颈，无特别理由）。试过 EDM2 的动态时间步加权，未见显著提升（猜测因其训练规模/数据远大于 EDM2 的 ImageNet setup）。
- **多宽高比训练**：先在 **256×256** 方图低分辨率训练，再在 **512×512** 与 **1024×1024** 用 online bucketing 多宽高比训练（继承 PGv2.5）。
- **后训练**：SFT 阶段配合多级 caption 防过拟合；提到 post-training 阶段做 **model merging（模型融合）**。论文未披露是否做 RLHF/DPO/reward model 等偏好对齐（未报告）。
- **训练稳定性（实战 trick）**：训练后期出现 **loss spike**——loss 异常增大但不出 NaN，模型进入无法生成有意义内容的状态。试过降 Adam beta、梯度裁剪、降学习率均无效。最终解法：每次迭代统计有多少参数梯度超过某阈值，**若超阈值的梯度数量超过预设计数阈值，则丢弃整个迭代（不更新权重）**。机理是观察到 spike 前几次迭代大梯度数量就开始上升、在 spike 处达峰；用 spike 前若干迭代的计数设阈值触发"丢批"。作者强调这比梯度裁剪更有效——裁剪只缩小幅度、不改变更新方向，权重仍可能朝崩溃移动；整批丢弃才能避免。
- **加速/蒸馏**：论文未报告步数蒸馏/consistency/LCM/ADD 等推理加速方案。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行策略 / 混合精度 / 吞吐**：均**未披露**（闭源产品技术报告未给训练硬件与分布式细节）。
- **推理工程**：Deep-Fusion 设计下，采样过程中冻结的 LLM **只前向一次**即生成全部层 hidden embedding，避免每个去噪步重复跑 LLM；joint attention（单次注意力替代分离的 self/cross-attn）也是为降计算与推理时间而设计。中间层 token 下采样 4×进一步省算力。
- **部署形态**：作为 Playground 产品线在线提供（playground.com），权重不公开。

## 评测 benchmark（把效果讲清楚）
数字均来自已落盘的 arXiv 报告（表 1–7）与官方 landing page（playground.com/pg-v3）。

- **DPG-bench（开源版，表 1）**：PGv3 总分 **87.04**，高于 DALL·E 3 的 83.50、SD3-Medium 的 84.08；各子项 Global 91.94 / Attribute 90.90 / Relation 90.00 / Other 92.72 多数领先（Entity 85.71 略低于 SD3-Medium 91.01）。
- **DPG-bench Hard（自建，GPT-4o 当 VQA 评判，表 2）**：这是作者认为更可信的内部基准（k-means 聚 120 簇取 2400 图、GPT-4o 生成 caption 与 yes/no 问题、每提示约 30 问、GPT-4o 误差 <5%；其中 40% 测试图属海报/广告/卡片/书封等图形设计类）。PGv3 **总分 88.62**，全面超越 Flux-pro 78.69、Ideogram-2.0 80.12、Ideogram-1.0 79.75、DALL·E 3 67.71、Midjourney v6.0 64.63、SD3-Medium 53.13。子项：Entity 94.45 / Global 93.64 / Relation 86.47 / Position 87.21 / Count 84.30 / **Text 82.09**（vs Flux-pro 69.47、Ideogram-2 75.32）。
- **文字合成（landing page 与表述）**：text-synthesis score **82%**，优于 Flux-pro 69%、Ideogram-2 75%；作者指出对手低分主因是提示词变长时**漏掉要求的文字元素**，凸显 PGv3 的提示词跟随。
- **GenEval（表 3）**：总分 **0.76**，高于 SD3 0.74、Flux-dev 0.68、DALL·E 3 0.67、SDXL 0.55。其中 Position 0.50（远超 SD3 0.33）、Two-object 0.95、Attribution 0.54、Colors 0.82、Counting 0.72。
- **Mario-text-1k 文字渲染（表 4，Kosmos-2.5 OCR 测）**：OCR-Fscore **40.35**（>Flux-pro 35.28、Flux-dev 34.98、SD3-Medium 18.29）；OCR-Precision 39.23、Recall 41.54、CLIP Score 33.89。
- **图形设计用户偏好（图 14 / landing page）**：用 PG Captioner 给 4k 人类设计图打 caption，再用同 caption 让 PGv3 重新生成，做成对人评（每对≥7 票多数表决）。**所有品类用户都更偏好 PGv3 而非人类设计师作品**，胜率：Stickers **80.5%**、Cards & invites 68.1%、Memes 68.3%、Logo 67.2%、Social media post 66.8%、Poster 65.5%、T-shirt 60.7%。
- **ImageNet FID（256，表 5）**：PGv3 **FID 14.67 / FD-DINOv2 102.91**，优于 PGv2.5（21.18 / 231.05）与加 CLIP 条件的 EDM2-xxl（16.37 / 118.74）。作者强调 ImageNet/MSCOCO 不能充分反映大规模 t2i 的综合能力。
- **MSCOCO 30k（表 6）**：1024 分辨率下，用 PG Captioner 长 caption，PGv3 **FID 8.58 / FD-DINOv2 82.59**，显著优于 Flux-dev（13.54 / 124.83）、SD3-Medium（14.42 / 128.28）、PixArt-Σ、Hunyuan-DiT、Lumina-Next、AuraFlow；FD-DINOv2 的大幅领先表明几何/物体形状更好。
- **VAE 重建（表 7）**：PGv3 16 通道 VAE 全面优于 SDXL 4 通道 VAE；1024×1024 上 LPIPS 0.060 / SSIM 0.939 / **PSNR 33.44**（SDXL-vae-ch4 为 0.116 / 0.840 / 28.11）。
- **CapsBench 描述评测（第 7 节，Claude-3.5 Sonnet 当问答评判、三次取共识）**：PG Captioner combined score **72.19%**，略高于 Claude-3.5 Sonnet 71.78%、GPT-4o 70.66%。CapsBench 揭示现有模型通病：caption 常缺物体**形状**（"brown wooden table"而非"brown rectangular wooden table"）、图中**尺寸感**、视觉**伪影**（噪声/镜头光晕）的描述。caption 长度分布上 GPT-4o 最短、Sonnet 平均约长一倍。
- **CapsBench 规模**：200 张图、2471 个问题（平均每图 ~12 问），覆盖 17 类（general / image type / text / color / position / relation / relative position / entity / entity size / entity shape / count / emotion / blur / image artifacts / proper noun(world knowledge) / color palette / color grading），多为 yes/no 题且多数答案为"yes"以给更清晰正确信号；评判时 LLM 仅依据候选 caption 答题，与参考答案比对算准确率。Claude/GPT 的 caption 用了带输出 schema 的详细指令、3-shot 示例与 CoT（先写图像分析再产 caption）；访问日期 2024-08-30。

**新能力（定性，第 5 节）**：照片真实感、长提示词跟随、文字渲染（海报/logo/贴纸/书封/PPT/meme）、**精确 RGB 颜色控制**（可对每个物体/区域指定精确 RGB 值或整体调色板）、**多语言提示输入**（英/西/菲/法/葡/俄，靠 LLM 跨语言理解，但不渲染非英文图中文字）。

## 创新点与影响
**核心贡献**：
1. **Deep-Fusion 文本条件**：逐层复刻冻结 LLM（Llama3-8B）并把每层 hidden states 作为对应图像层的条件，彻底取消 T5/CLIP，把"LLM 当文本编码器"推到逐层全融合的极致——这是 PGv3 区别于 SD3（MMDiT + T5/CLIP）、DALL·E 3（re-caption）的最大架构标识。
2. **多级（6 档长度）re-caption** 训练方法，缓解 caption 偏置、改善短/长提示词两端表现并防 SFT 过拟合。
3. **训练稳定性的"丢批"梯度策略**：基于"大梯度计数"预警 loss spike 并丢弃整次迭代，比梯度裁剪更有效，是大模型扩散训练的实用工程经验。
4. **expand-PE**（vanilla 2D-RoPE）相对 interpolating-PE 在分辨率/宽高比泛化上的明确结论。
5. **CapsBench**：面向长/细粒度描述、17 类、问答式（DSG/DPG 反向思路）的图像描述开源评测，填补现有 reference-based / reference-free / CLIPScore 指标在密集长 caption 上的盲区。
6. **DPG-bench Hard**：用 GPT-4o 当 VQA 评判、含 40% 图形设计类提示的更难提示词跟随基准。

**影响**：把"decoder-only LLM 逐层深融合进扩散主干"作为一条与 MMDiT 并列的文本条件路线公开验证，并以图形设计（文字/版式/配色/布局）为差异化战场，给出"超越人类设计师"的用户偏好证据；CapsBench 作为可复用的细粒度 captioning 评测留给社区。

**已知局限**：
- 模型权重闭源，训练数据规模/来源/配比、算力与分布式工程、是否做偏好对齐（RLHF/DPO）等均未披露，难复现。
- 不在非英文文字渲染数据上训练，故图中非英文文字通常无法正确生成。
- 仍用 EDM 调度而非 flow matching，未做步数蒸馏等推理加速的公开报告。
- 评测以自建 DPG-bench Hard / 内部图形设计人评为主，部分对比模型（Flux-pro/Ideogram-2）数字为作者自测；ImageNet/MSCOCO 作者自承不能充分反映综合能力。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2409.10695
- arxiv_pdf: https://arxiv.org/pdf/2409.10695
- arxiv_html: https://arxiv.org/html/2409.10695v1
- project (technical report landing): https://playground.com/pg-v3
- official blog (Introducing Playground v3, 2024-10-17): https://playground.com/blog/introducing-playground-v3
- CapsBench dataset (HF): https://huggingface.co/datasets/playgroundai/CapsBench

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2409.10695.pdf
- ../../../sources/omni/2024/playground-v3--capsbench-readme.md
- ../../../sources/omni/2024/playground-v3--blog.md
- ../../../sources/omni/2024/playground-v3--landing.md
