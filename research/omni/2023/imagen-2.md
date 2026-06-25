---
title: "Imagen 2"
org: Google DeepMind
country: US
date: "2023-12"
type: blog
category: t2i
tags: [text-to-image, diffusion, closed-source, google-deepmind, vertex-ai, synthid, inpainting, outpainting, aesthetics-conditioning, recaptioning]
url: "https://deepmind.google/technologies/imagen-2/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://cloud.google.com/blog/products/ai-machine-learning/imagen-2-on-vertex-ai-is-now-generally-available"
downloaded: [imagen-2--deepmind-original-page-wayback.md, imagen-2--vertex-ai-ga.md, imagen-2--imagefx-labs-blog.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Imagen 2 是 Google DeepMind 2023 年 12 月发布的第二代闭源文生图扩散模型，主打"更真实的细节 + 更强的图文对齐 + 文本渲染"，核心做法是**给训练集做更丰富的 caption 增强（re-captioning）+ 训练一个人类偏好美学打分模型做 aesthetics conditioning**；官方未公布参数量、FID 等任何定量指标，只以产品形态披露——同时落地 Bard、Search Generative Experience、ImageFX、Google Arts & Culture 与 Vertex AI。

## 背景与定位
- **解决的问题**：第一代 [[imagen]]（2022，arXiv:2205.11487）证明了"冻结大语言模型文本编码器（T5-XXL）+ 级联扩散超分"能拿到极强的图文对齐和当时 SOTA 的 COCO FID(7.27)，但它只是研究产物、未产品化，且在**手/脸的真实感、文本渲染、风格可控、图像编辑**上仍有明显短板。Imagen 2 是把这条扩散级联路线**工程化、产品化**的一代，目标是"我们迄今最高质量的图像"，并补齐编辑能力。
- **技术脉络中的位置**：处在 2023 年文生图竞赛白热化的节点——同期有 [[stable-diffusion-xl-sdxl]]、DALL·E 3、[[adobe-firefly]]、Midjourney v5/v6。Imagen 2 没有发论文，定位是 Google 内部统一文生图引擎（Bard / SGE / ImageFX 全部由它驱动），而非可复现的研究工作。
- **相对前作的改进**：① 用"加描述/多风格 caption"的方式重写训练 caption，强化图文理解（与同期 DALL·E 3 的 synthetic re-captioning、[[emu-quality-tuning]] 的质量微调思路同源）；② 引入人类偏好驱动的**美学打分条件**；③ 原生支持 **inpainting / outpainting** 与**参考图风格条件（fluid style conditioning）**；④ 文本渲染、多语言提示、logo 生成等企业向能力；⑤ 集成 **SynthID 隐形水印**。

## 模型架构
- **backbone**：官方明确称 Imagen 2 为 "text-to-image **diffusion** technology"（原页面与 Vertex 博客均用 diffusion 表述），延续 Imagen 家族的扩散路线。**具体网络结构（是否仍为 U-Net 级联超分、是否换 latent/DiT、各级分辨率）官方未披露**。考虑到它与 2022 年 Imagen 的级联超分架构同源、且 2023 年底 Google 尚未公开转向 latent/DiT，外界普遍推测仍是**像素空间级联扩散（base + 超分模块）**，但这一点**无一手来源确认，按"未披露"处理**。
- **text encoder**：未在 Imagen 2 文档中重申。前作 Imagen 使用冻结的 **T5-XXL**，Imagen 2 是否沿用未披露。
- **visual tokenizer / VAE / VQ**：未披露。
- **条件注入**：除文本条件外，官方披露了两类额外条件——**美学分数条件（aesthetics score conditioning）** 和**参考图风格条件（style reference image）**；编辑用 **mask 条件**（inpainting 给参考图+掩码、outpainting 向外扩展）。注入机制细节未公开。
- **参数量与分辨率策略**：**参数量未披露**。分辨率方面，已落盘源只给定性表述——DeepMind 页称"高质量"，Vertex GA 博客称"high-resolution"（line 139），**均未给出具体像素数**；具体输出分辨率（业界常引的 1024×1024 默认值出自 Vertex 产品文档，但该文档页未落盘）与训练/级联各级尺寸**在本页已落盘源中未报告**。

## 数据
- **核心做法——caption 增强 / re-captioning**：官方明说"我们给 Imagen 2 训练集的图像 caption **加了更多描述**，帮助模型学习不同的 captioning 风格、并泛化到更广的用户 prompt"，由此提升图文理解与上下文/细节把握。这与 DALL·E 3 的"训练专门的图像描述器重写 caption"是同一时代的同一思路，但 Imagen 2 **未公布**用什么模型生成描述、合成 caption 占比、原始/合成混合比例。
- **美学过滤与条件**：官方训练了一个**基于人类偏好的图像美学模型**，对"光照、构图、曝光、清晰度"等维度打分；每张训练图获得一个美学分数，用来**给训练集中高美学图像更大权重（条件化）**，从而提升生成质量。页面用"Flower"提示词的低→高美学分图例直观展示了该条件的作用。
- **数据来源 / 规模 / 配比 / 清洗**：图文对的**来源、规模、语言分布、清洗流水线均未披露**。官方仅强调"投入了训练数据安全（training data safety）"，并对训练数据施加安全过滤（避免有害内容、避免生成指名道姓的真实人物）。
- **安全数据治理**：对训练数据、输入 prompt、生成输出三个环节都加安全检查；Vertex AI 版本叠加了版权赔偿（indemnification）承诺与"两路版权赔偿"机制（间接暗示对训练来源做了合规处理，但具体来源仍未公开）。

## 训练方法
- **训练目标**：扩散（denoising diffusion），延续 Imagen 家族；**是否采用 v-prediction、classifier-free guidance、noise schedule 等具体目标/超参均未披露**。
- **关键训练 trick（已披露）**：
  - **Caption 增强**：训练前用更丰富、多风格的描述重写图像 caption，提升图文对齐与 prompt 泛化（见"数据"）。
  - **美学分数条件**：把人类偏好美学打分作为条件信号注入训练，使采样时可偏向高美学分布——这是把"质量微调/偏好对齐"思想以**条件化**而非后训练 RLHF 的形式实现的代表做法。
- **多阶段 / 偏好对齐 / RLHF / DPO**：**未提及**任何 SFT→RLHF/DPO 的后训练流程；美学优化是通过上述**条件化**而非显式偏好优化算法实现的。是否做步数蒸馏 / consistency / LCM / ADD 等加速训练**未披露**。
- **编辑能力的训练**：inpainting/outpainting 与风格条件被描述为"diffusion-based techniques 带来的灵活性"，但**未公开是否单独训练编辑头、用何种 mask 训练策略**。

## Infra（训练 / 推理工程）
- **算力 / GPU·时 / 并行 / 精度 / 吞吐**：**全部未披露**。Imagen 2 无技术报告、无 model card 级工程细节。
- **部署形态（已披露）**：作为 Google 统一文生图引擎，2023 年 12 月同时上线——
  - **消费端**：Bard（生成图像）、Search Generative Experience、Google Labs 的 **ImageFX**（带"expressive chips"提示交互）、Google Arts & Culture 的 Cultural Icons 实验；
  - **企业端**：**Vertex AI 的 Imagen API**（Vertex GA 博客日期 2023-12-14，对 allowlist 客户 GA），提供托管基础设施、内置隐私与安全、版权赔偿；
  - 早期客户：Snap（AI Camera Mode）、Shutterstock（站内 16,000+ 张 Imagen 图可授权）、Canva（170M+ 月活、已生成数百万张）。
- **推理加速 / 量化 / 缓存 / 步数蒸馏**：未披露。

## 评测 benchmark（把效果讲清楚）
- **官方未报告任何定量指标**：Imagen 2 的发布材料（DeepMind 技术页 + Vertex GA 博客 + ImageFX Labs 博客）**没有给出 FID / CLIPScore / GenEval / DrawBench / 人评 ELO 等任何数字**，也没有与同期模型（SDXL / DALL·E 3 / Firefly / Midjourney）的可对比评测。只有定性表述：
  - "我们迄今最高质量的图像（our highest-quality images yet）"；
  - 在"真实手部与人脸渲染、减少干扰性视觉伪影"等业界老大难方向上有改进（定性，附图例，无指标）；
  - "Flower"低→高美学分图例（定性消融，说明美学条件确实抬升观感，但**无量化打分对比**）。
- **结论**：作为闭源产品，效果只能定性描述；**任何 Imagen 2 的 FID/对齐分数若出现在第三方报道中均非官方一手数据，本页不予采信**。源里没有的数字一律记"未报告"。

## 创新点与影响
- **核心贡献（按可信度排序）**：
  1. **Caption 增强（re-captioning）作为图文对齐的主抓手**——与 DALL·E 3 同期、互为印证地确立了"重写训练 caption 提升 prompt-following"成为 2023—2024 文生图标准动作。
  2. **人类偏好美学打分 → 条件化注入**，提供了一条不走 RLHF/DPO、用"条件化"就能把质量偏好灌进扩散模型的轻量路径。
  3. **把级联扩散文生图工程化为统一产品引擎**：一个模型驱动 Google 全线（搜索、Bard、Labs、Cloud、Arts & Culture），并叠加企业级合规（版权赔偿）与 **SynthID 隐形水印**——后者推动了"生成图可溯源/可检测水印"的行业实践。
  4. 原生 **inpainting / outpainting + 参考图风格条件**，把编辑能力纳入主模型。
- **对后续的影响**：Imagen 2 是 Google 把文生图从研究（2022 Imagen）推进到产品矩阵的关键过渡，直接铺垫了后续 **Imagen 3（2024）/ Imagen 4** 以及与 Gemini 生态的融合（如后来的 Nano Banana / Gemini Image 路线）。其"re-caption + 美学条件 + 水印"组合成为 Google 系文生图的方法骨架。
- **已知局限**：
  - **完全闭源、零技术报告**：架构、参数量、数据规模、训练算力、所有 benchmark 均未公开，研究价值有限、不可复现；
  - 编辑能力（inpainting/outpainting）在发布时还在"2024 年内陆续上 Vertex AI"的路线图上，并非即时可用；
  - 安全策略偏保守（拒绝生成指名真实人物等），对部分用例形成约束。

## 原始链接
- blog (DeepMind 官方技术页，原始 2023-12 版本，经 Wayback 存档): https://web.archive.org/web/20240201205357/https://deepmind.google/technologies/imagen-2/ （原 live URL https://deepmind.google/technologies/imagen-2/ 现已 301 重定向到 Imagen 4 页面）
- blog (Google Cloud — Imagen 2 on Vertex AI is now generally available, 2023-12-13): https://cloud.google.com/blog/products/ai-machine-learning/imagen-2-on-vertex-ai-is-now-generally-available
- blog (Google Labs — Try ImageFX and MusicFX, 2023-12): https://blog.google/innovation-and-ai/products/google-labs-imagefx-textfx-generative-ai/

## 本地落盘文件
- ../../../sources/omni/2023/imagen-2--deepmind-original-page-wayback.md  （DeepMind 官方 Imagen 2 技术页，Wayback 2024-02-01 存档，含 caption 增强 / 美学条件 / 风格条件 / inpainting-outpainting / SynthID / 致谢作者名单）
- ../../../sources/omni/2023/imagen-2--vertex-ai-ga.md  （Vertex AI GA 博客，含文本渲染 / 多语言 / logo / captioning-QA / SynthID 水印 / 客户案例）
- ../../../sources/omni/2023/imagen-2--imagefx-labs-blog.md  （ImageFX Labs 博客，确认 ImageFX 由 Imagen 2 驱动、"expressive chips" 交互、最高质量定位）
