---
title: "Imagen 4 Fast / Imagen 4(Ultra) GA 与 GPT Image 1 mini"
org: "Google / OpenAI"
country: US
date: "2025-08"
type: blog
category: t2i
tags: [t2i, closed-source, api, cost-tier, imagen-4, gpt-image-1, autoregressive, latent-diffusion, synthid, c2pa]
url: "https://developers.googleblog.com/en/announcing-imagen-4-fast-and-imagen-4-family-generally-available-in-the-gemini-api/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://developers.openai.com/api/docs/models/gpt-image-1-mini"
downloaded: [gpt-image-1-mini-and-imagen-fast--imagen4-ga-googleblog.md, gpt-image-1-mini-and-imagen-fast--openai-image-api.md, gpt-image-1-mini-and-imagen-fast--openai-model-doc.md, gpt-image-1-mini-and-imagen-fast--openai-imagegen-guide.md, native-image-generation-system-card.pdf]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
这是 2025 下半年两家 T2I 旗舰的**成本/速度档位扩展**（产品迭代条目，非新架构论文）：Google 在 **2025-08-15** 让 Imagen 4 全家族（Imagen 4 / Imagen 4 Ultra / 新增 **Imagen 4 Fast**）在 Gemini API GA，Fast 档把单图价压到 **\$0.02/张**，Imagen 4 / Ultra 支持到 **2K 分辨率**；OpenAI（2025 下半年）推出 **gpt-image-1-mini**，作为 [[dall-e-3]] 之后那款「原生自回归」`gpt-image-1` 的廉价档（官方模型文档定价已上线；具体发布日期不在已落盘一手源内，不在此断言），官方称 **API 成本比 gpt-image-1 便宜约 80%**，最低画质单图低至 **\$0.005/张**。两者都不是模型创新，而是**把高质量图像生成 API 的边际成本拉低一个数量级**的商业化动作。

## 背景与定位
2025 上半年两家分别把旗舰原生图像能力搬上 API：
- **OpenAI**：2025-03-25 在 ChatGPT 上线 4o 原生图像生成（[[dall-e-3]] 之后改用「自回归原生多模态」路线，见系统卡），首周 1.3 亿用户生成 7 亿张图；2025-04-23 通过 `gpt-image-1` 把同一原生多模态模型引入 Images API（文本输入 \$5/M tok、图像输入 \$10/M tok、图像输出 \$40/M tok，约合低/中/高质量正方图 \$0.02 / \$0.07 / \$0.19 每张）。
- **Google**：Imagen 4 家族继承 [[imagen-3]]（latent diffusion）旗舰，先在 Gemini API / AI Studio 进入 paid preview（preview 起始日不在已落盘一手源内，不在此断言），2025-08-15 才全家族 GA（本条目落盘的 GA 博客）。

本条目记录的是「**成本档位下探**」这一步：旗舰质量已就位后，两家都补一个**便宜/快**的档位去抢高并发、低单价的生产场景（电商、营销素材、批量生成）。它对应的技术脉络位置不是「更强」，而是「**更便宜/更快、把同代质量普惠化**」——与 [[flux-1-krea-dev]]、[[firefly-image-model-4]] 等同期「可用性/成本」导向的迭代同属一拨。相关同期/后续工作：[[gemini-3-pro-image-nano-banana-pro]]（Google 后续把图像能力并入 Gemini 原生多模态，Imagen 系列逐步被 gemini-2.5-flash-image / Nano Banana 取代）。

## 模型架构
两条产品线分属两种范式，且**均为闭源、官方均未为这两个具体档位发布技术报告或参数量**，只能给出可确证的范式与已披露事实：

**Imagen 4 / Fast / Ultra（Google，latent diffusion 路线）**
- 继承 [[imagen-3]] 的**潜空间扩散（latent diffusion）**家族（Imagen 自 [[imagen]] 的像素级联扩散切换到潜扩散始于 Imagen 3）。**Imagen 4 的 backbone（U-Net / DiT）、VAE/visual tokenizer、文本编码器（早期 Imagen 用 T5-XXL，是否沿用未声明）、参数量——全部未披露**，与 Google 闭源旗舰一贯的「架构当产品机密」风格一致。
- 官方仅披露**家族分档定位与产物规格**：Imagen 4 Fast 主打速度与高并发；Imagen 4 为旗舰，在文本渲染（text rendering）上较前代「substantial improvements」；Imagen 4 Ultra 主打最高细节与最严格的 prompt 对齐。Imagen 4 与 Ultra 支持**最高 2K 分辨率**（"up to 2K resolution"），Fast 档官方文案未强调 2K（重在低延迟）。
- API model id：`imagen-4.0-generate-001`、`imagen-4.0-fast-generate-001`、`imagen-4.0-ultra-generate-001`。

**GPT Image 1 mini（OpenAI，自回归原生多模态路线）**
- 与 `gpt-image-1` 同范式：**原生多模态、自回归（autoregressive）的图像生成**，而非扩散。系统卡原文（"4o image generation"）明确：「Unlike DALL·E, which operates as a diffusion model, 4o image generation is an autoregressive model natively embedded within」omnimodal GPT-4o——即文本与图像在同一自回归模型里联合建模，天然支持 image-to-image 变换、强指令遵从、可靠文本渲染。
- 官方模型文档把 gpt-image-1-mini 描述为「**A cost-efficient version of GPT Image 1. It is a natively multimodal language model that accepts both text and image inputs, and produces image outputs.**」——**输入：文本 + 图像；输出：图像**（不输出文本/音频/视频）。
- **mini 的具体瘦身方式（蒸馏 / 缩小 backbone / 减步数等）官方未披露**，仅以「cost-efficient version」「约便宜 80%」概括。参数量未披露。
- 端点：`v1/images/generations`、`v1/images/edits`，并可经 `v1/responses` / `v1/chat/completions` 调用；输出分辨率 1024×1024 / 1024×1536 / 1536×1024 三档。

## 数据
- **Imagen 4 家族**：训练数据来源/规模/配比/过滤/re-captioning 在 GA 博客中**未披露**。可参考的家族信息见 [[imagen-3]]（Gemini 生成合成 caption + 多级安全/质量过滤），但 Imagen 4 是否沿用同一管线**官方未声明，不臆测**。
- **GPT Image 1 mini**：训练数据**未披露**。系统卡仅说明其安全相关数据/红队流程（外部人工红队 + 自动红队 + 真实场景离线测试），不涉及训练语料构成。
- 两者均**未披露**图文对数量、美学/安全过滤的具体配比与合成数据占比。

## 训练方法
- **Imagen 4**：训练目标（扩散 / flow matching）、多阶段（预训练→SFT→偏好对齐）、蒸馏/加速方案**全部未披露**。Imagen 4 Fast 的「快」按官方仅说是「built for speed / low-latency」，**未公开其加速手段**（是否步数蒸馏 / 蒸馏小模型 / 缓存均未说明）。
- **GPT Image 1 mini**：作为 gpt-image-1 的「cost-efficient version」，其训练/蒸馏细节**未披露**。可确证的只有：与 gpt-image-1 共享同一套「原生自回归图像生成 + 安全栈」，并继承系统卡描述的安全后训练（chat 模型层 refusal + prompt blocking + output blocking + 安全推理监视器）。OpenAI 默认**不使用客户 API 数据训练**。

## Infra（训练 / 推理工程）
- **训练侧**：两个档位的算力规模 / GPU·时 / 并行策略 / 精度 / 吞吐——**均未披露**。
- **推理 / 部署形态（这才是本条目的实质）**：两者都是**纯托管 API**，无开源权重、无本地部署。
  - Imagen 4：Gemini API + Google AI Studio；GA 后三档并存（Fast / 标准 / Ultra，Ultra GA 初期文案仍标 preview/限单图，以官方变更日志为准）；所有产物打 **SynthID** 不可感知水印（DeepMind 的内嵌水印技术）。
  - gpt-image-1-mini：OpenAI Images API（`v1/images/generations` / `v1/images/edits`），模型文档同时列出 `v1/responses`、`v1/chat/completions`、`v1/batch` 等端点；所有产物含 **C2PA 元数据**（可验证来源，行业标准），并配 OpenAI 内部「是否本产品生成」的检测工具（系统卡「Our approach to provenance」：C2PA metadata on all assets + internal tooling）。
- 因此本条目的「infra 价值」集中在**单位经济（unit economics）**：把同代质量的单图边际成本压低约一个数量级，便于高并发批量生成场景规模化。

## 评测 benchmark（把效果讲清楚）
本条目两份一手发布材料（Google GA 博客、OpenAI 模型文档/4 月发布博客、系统卡）**均未给出 FID / GenEval / DPG-Bench / HPSv2 / Arena ELO 等量化对比数字**——它们是产品/价格公告，不是 benchmark 报告。能从一手源确证的「硬数字」是**价格与规格**，逐条列出（不编造质量分）：

**价格（单位经济，全部来自一手源）**
- **Imagen 4 Fast**：**\$0.02 / 输出图**（GA 博客原文 "$0.02 per output image"）。
- **gpt-image-1（参照，2025-04 博客）**：文本输入 \$5/M tok、图像输入 \$10/M tok、图像输出 \$40/M tok；约合低/中/高质量正方图 **\$0.02 / \$0.07 / \$0.19** 每张。
- **gpt-image-1-mini（官方模型文档）**：
  - token 价：文本输入 **\$2.00/M**（缓存 \$0.20）、图像输入 **\$2.50/M**（缓存 \$0.25）、图像输出 **\$8.00/M**。对比 gpt-image-1 的图像输出 \$40/M ⇒ 图像输出 token 价约为 **1/5**，与官方「约便宜 80%」口径一致。
  - 单图阶梯价（按质量×尺寸）：
    - **Low**：1024² **\$0.005**；1024×1536 / 1536×1024 各 **\$0.006**
    - **Medium**：1024² **\$0.011**；1024×1536 / 1536×1024 各 **\$0.015**
    - **High**：1024² **\$0.036**；1024×1536 / 1536×1024 各 **\$0.052**

**质量/规格（一手源确证项）**
- Imagen 4：官方称较前代在**文本渲染**上有「实质性改进」；Imagen 4 / Ultra 支持**最高 2K 分辨率**。
- gpt-image-1-mini：官方模型卡的相对定位标注为「Performance: Higher」「Speed: Slowest」——即在 OpenAI 图像档里偏质量但**不是最快**（"mini" 指便宜，不等于最快）。

**安全侧量化（系统卡，针对 4o/gpt-image-1 原生生成，mini 共享同一安全栈）**
- 外部红队数据：仅系统缓解（prompt+output blocking）not_unsafe **0.955** / not_overrefuse 0.941；叠加 chat 模型 refusal 后 not_unsafe **0.971** / not_overrefuse 0.856。
- 自动红队：系统缓解 0.969 / 0.899；叠加 refusal 0.975 / 0.830。
- 真实场景：系统缓解 0.929 / 0.996；叠加 refusal 0.932 / 0.993。
- 照片级人物分类器（child/adult 判别，评测集近 4000 张图）：系统卡只报 **precision/recall**（非单一 accuracy）——「Photorealistic person (adult or child)」n=2033，precision **0.905** / recall **0.99**；「Photorealistic adult」n=919，precision **0.80** / recall **0.776**；「Photorealistic child」n=1113，precision **0.80** / recall **0.97**。

> 质量类基准对比（GenEval / DPG / Arena ELO 等）：**两家一手发布材料均未报告**，故此处不列任何质量分数以免编造。

## 创新点与影响
- **核心贡献（产品/商业，非算法）**：把 2025 同代旗舰质量的 T2I 推到「**\$0.005–0.02/张**」的价位，单位经济较各自旗舰档下探约一个数量级，使**高并发、低单价的批量生成**（电商主图、营销素材、批量个性化）在 API 上经济可行；并配齐合规水印/溯源（Imagen=SynthID，OpenAI=C2PA + 内部检测工具）。
- **范式对照价值**：同一「便宜档」诉求下，Google 走 **latent diffusion**（Imagen 4 Fast，加速手段未公开），OpenAI 走 **原生自回归多模态**（gpt-image-1-mini），是 2025 年两条主流 T2I 路线在「成本档」上的并行落地样本。
- **影响**：成本档下探加速了 T2I 从「单张创作」走向「生产管线 / agent 工具」的规模化使用；Google 侧随后把图像能力进一步并入 Gemini 原生多模态（[[gemini-3-pro-image-nano-banana-pro]]），Imagen 独立系列逐步被 gemini-flash-image / Nano Banana 取代。
- **已知局限 / 信息缺口**：两者均**闭源、无权重、无技术报告**；模型架构、参数量、训练/蒸馏/加速细节、训练数据构成、以及质量类 benchmark 数字**均未披露**——本条目能落地的硬事实主要是**价格、规格与安全评测**三类。gpt-image-1-mini 官方文案标 "Speed: Slowest"，说明「便宜」未必「最快」，对延迟敏感场景需实测取舍。

## 原始链接
- blog (Google, Imagen 4 Fast + 家族 GA, 2025-08-15): https://developers.googleblog.com/en/announcing-imagen-4-fast-and-imagen-4-family-generally-available-in-the-gemini-api/
- blog (OpenAI, gpt-image-1 引入 Images API, 2025-04-23): https://openai.com/index/image-generation-api/
- model-doc (OpenAI, gpt-image-1-mini 官方模型/定价文档): https://developers.openai.com/api/docs/models/gpt-image-1-mini
- guide (OpenAI, Image generation 指南): https://developers.openai.com/api/docs/guides/image-generation
- system-card (OpenAI, Native image generation, GPT-4o addendum, 2025-03-25, gpt-image-1/mini 共享其架构与安全栈): https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf
- (worklist 原列 Google URL `imagen-4-now-generally-available-gemini-api/` 实测 404；正确 GA 博客已替换为上方 announcing-… 链接)

## 本地落盘文件
- ../../../sources/omni/2025/gpt-image-1-mini-and-imagen-fast--imagen4-ga-googleblog.md
- ../../../sources/omni/2025/gpt-image-1-mini-and-imagen-fast--openai-image-api.md
- ../../../sources/omni/2025/gpt-image-1-mini-and-imagen-fast--openai-model-doc.md
- ../../../sources/omni/2025/gpt-image-1-mini-and-imagen-fast--openai-imagegen-guide.md
- ../../../sources/omni/2025/native-image-generation-system-card.pdf
