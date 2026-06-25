---
title: "GPT Image 2 / ChatGPT Images 2.0（含 Thinking mode）"
org: OpenAI
country: US
date: "2026-04"
type: system-card
category: unified
tags: [native-image-gen, autoregressive, thinking-mode, agentic, image-editing, text-rendering, 4k, c2pa, watermark, closed-source]
url: https://openai.com/index/introducing-chatgpt-images-2-0/
arxiv: ""
pdf_url: https://deploymentsafety.openai.com/chatgpt-images-2-0/chatgpt-images-2-0.pdf
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: https://developers.openai.com/api/docs/models/gpt-image-2
downloaded: [gpt-image-2--blog-zh.md, gpt-image-2--system-card.pdf, gpt-image-2--system-card.txt, gpt-image-2--system-card-toc.md, gpt-image-2--api-model-doc.md, gpt-image-2--image-generation-guide.md, gpt-image-2--pricing.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ChatGPT Images 2.0（API 名 `gpt-image-2`，2026-04-21 发布）是 OpenAI 继 [[gpt-image-1]]（4o 原生图像生成）、ChatGPT Images 1.5 之后的新一代**原生图像生成/编辑模型**，最大新增是把**推理 + 工具调用引入生图过程**的 **Thinking mode**——可联网搜索、由一条 prompt 生成多张图、用 reasoning stack 把粗略 prompt 自主"调研"成深思熟虑的成图；同时把支持分辨率拉到 **4K（3840×2160）**、对图像输入**强制高保真处理**。OpenAI **未发布论文/技术报告**，仅有 System Card（偏安全）+ 发布博客（图廊）+ API 文档，**架构/数据/训练配方几乎全部未披露**。

## 背景与定位
OpenAI 的原生图像生成路线：[[dall-e-3]]（独立扩散模型，GPT 通过 tool-call 间接调用）→ [[gpt-image-1]]（即 "GPT-4o Image Generation 1.0"，2025-03，把生图**焊进** GPT-4o 全模态模型、用**自回归 transformer** 而非独立扩散主干直接生图）→ **ChatGPT Images 1.5** → **ChatGPT Images 2.0**（本页，2026-04）。System Card 明确把谱系写为 "past GPT-4o Image Generation (1.0) and 1.5 deployments"，2.0 是同一原生路线的延续与放大。

2.0 解决/推进的问题，按一手源（System Card + 发布博客 caption + API 文档）可确认的方向：
- **更强的世界知识与指令遵循**：System Card 开篇即称 "significantly enhanced world knowledge, instruction following, and generating detail and complexity such as dense text"（显著增强的世界知识、指令遵循，以及生成密集文字这类细节与复杂度）。发布博客图廊用大量"杂志跨页/信息图/学术海报/多语言排版"样例佐证密集文字与版式能力。
- **Thinking mode = 把图像生成 agent 化**：把 reasoning + tool use 引入生图，是本次发布相对 1.0/1.5 最关键的范式增量（详见"训练方法/Infra"）。
- **更高分辨率与更高保真编辑**：API 支持到 4K、对参考图/编辑输入恒为高保真处理（见"模型架构/Infra"）。

技术脉络上，它属于 2025–2026"统一/原生多模态生成"浪潮里闭源最前沿的一档，对位同期 Google Gemini 系原生图像（Nano-Banana 线）、以及开源侧的 [[bagel]] / [[janus-pro]] / [[internvl-u]] 等统一模型；但 OpenAI 这条线在工程细节披露上一贯最少。

## 模型架构
**重要说明：OpenAI 对 ChatGPT Images 2.0 未发布任何论文或技术报告，未公开 backbone 类型、参数量、tokenizer/VAE、解码器结构、text encoder、分辨率训练策略等任何硬指标。** 本节只整理一手源（System Card + API 文档）能确认的事实，其余按谱系合理标注"未披露/沿袭推测"。

- **谱系沿袭的范式（推测，官方对 2.0 未重述）**：前作 [[gpt-image-1]] 的 System Card/发布白板明确其为"原生嵌入 ChatGPT 的**自回归** transformer，在 `p(text, pixels, sound)` 联合分布上建模，流水线 `tokens → [transformer] → [diffusion] → pixels`"（自回归先验 + 末端扩散解码器）。2.0 的官方材料**未重新声明架构**，仅以"a major step forward in image generation capabilities"概括；因此 2.0 仍属原生自回归路线只能作为**谱系推断**，OpenAI 未对 2.0 单独确认，更未披露是否更换主干/tokenizer/解码器。
- **多模态 I/O（API 文档确认）**：`gpt-image-2` 的模态为 **Text（仅输入）+ Image（输入与输出）**，Audio/Video 不支持；定位标注 Performance=Highest、Speed=Medium。即它是一个"图像专用"端点，而非把图像生成挂回主线 LLM——主线 LLM（如 gpt-5.5）通过 Responses API 的 `image_generation` 内置工具来调用它。
- **图像输入恒为高保真（API 文档确认，与前作的关键差异）**：`input_fidelity` 参数对 `gpt-image-2` **不可调**——"the model processes every image input at high fidelity automatically"。代价是编辑/参考图请求的 image input token 显著偏高。前作 gpt-image-1.5 需手动开 `input_fidelity=high`，2.0 把高保真做成了默认且强制。
- **分辨率与尺寸约束（API 文档确认）**：支持**任意分辨率**，约束为——最长边 ≤ `3840px`；两边均为 `16px` 的倍数；长短边比 ≤ `3:1`；总像素数在 `655,360`–`8,294,400` 之间。常用档：`1024×1024`(方)、`1536×1024`(横)、`1024×1536`(竖)、`2048×2048`(2K 方)、`2048×1152`(2K 横)、`3840×2160`(4K 横)、`2160×3840`(4K 竖)，及 `auto`(默认)。**输出总像素超过 `2560×1440`（`3,686,400`，官方称之为 2K）即标注为 experimental（实验性）**。
- **质量档**：`low`/`medium`/`high`/`auto`，`auto` 由模型按 prompt 自选。`size`/`quality`/`background` 均支持 `auto`。
- **已知架构层面限制（API 文档确认）**：**不支持透明背景**（`background:"transparent"` 对本模型不可用——这与前作 gpt-image-1 支持透明背景相比是个回退）；版式精排、跨图角色/品牌一致性、精确文字定位仍是弱项（见"评测/限制"）。
- 主干/参数量/tokenizer/解码器/text encoder/潜空间维度：**全部未披露**。

## 数据
**完全未披露。** System Card 是安全文档，不含训练数据章节；发布博客是图廊，无数据描述；API 文档只讲用法与计费。OpenAI 对 ChatGPT Images 2.0 **没有公开任何训练数据来源、规模、配比、清洗过滤、re-captioning、合成数据、美学/安全过滤**的细节。

可作背景的谱系信息（来自前作 [[gpt-image-1]]，非 2.0 官方确认）：4o 原生图像生成曾自述"在网络图像与文本的**联合分布**上训练"、存在独立的"post-training mixture"。2.0 是否沿用、是否扩充多语言/版式/密集文字数据，官方**未说明**——尽管发布博客重点宣传多语言文字渲染（日/中/阿/韩/天城体/西里尔/孟加拉/希腊等）与杂志级版式，暗示数据侧大概率强化了富文本/多语种/设计类样本，但这**只是从产物反推，官方未确认，不写入结论**。

## 训练方法
**训练目标/扩散 vs 自回归/多阶段配方/RL 细节：均未披露。** 但 System Card 对 **Thinking mode 的训练取向**与**安全后训练**给了少量可确认信息：

- **Thinking mode = reasoning + tool use 进入生图（System Card 确认）**：随模型一同推出的 thinking mode "adds reasoning and tool use to the image generation process, allowing the system to integrate live web search data, generate multiple images from a single prompt, and use our reasoning stack to turn a basic prompt into a well-researched and thought-through final image"。即用 OpenAI 的 reasoning 栈，把"基础 prompt"先**联网调研 + 推理规划**，再生成（可一条 prompt 出多张图）。这是把图像生成 **agent 化**的关键一步——不是更强的扩散采样，而是在生图前接入工具与思维链。
- **Safe Completions 取向训练（System Card 确认）**：thinking 模型被训练为"safely transform (via **Safe Completions**) adversarial requests into safe ones rather than simply producing the requested violative content"。其直接后果是：在对抗评测里，thinking mode 上游产出的真正违规图比例只有 6.7%，远低于 instant mode 的 22.0%（见"评测"）——因为它会把越界请求**改写成安全版本**而非照单生成。这是训练层（而非纯过滤层）的安全增益。
- **安全栈与安全推理模型的持续训练（System Card 确认）**：2.0 的安全栈"based on the same foundations as our ChatGPT Images 1.5 safety stack"，并新增针对更高真实感的防护。近期改进包括"continuously improved the safety classifier, safety policies, and overall safety stack with new training"、把评测从"raw taxonomy-matching"转向"outcome-based"（更贴近真实有害产出风险）、扩大线上/线下监控。核心审核器是一个"**safety-focused multimodal model trained to reason about content policies**"（专门训练来对内容政策做推理的多模态安全推理模型）。
- **生图主体的训练目标（扩散/flow/next-token）、SFT/偏好对齐(RLHF/DPO)、reward model、蒸馏/步数加速**：**均未披露**。仅从延迟（复杂 prompt 可达 2 分钟，见 Infra）可推测未做激进步数蒸馏，但官方无说明。

## Infra（训练 / 推理工程）
**训练侧 infra（算力/GPU·时/并行/精度/吞吐）完全未披露。** 推理与部署侧由 API 文档/System Card 可确认：

- **两条调用路径（API 文档）**：① **Image API**（`v1/images/generations` 生成、`v1/images/edits` 编辑），直接选 `gpt-image-2`；② **Responses API**，作为内置工具 `image_generation` 被主线模型（如 gpt-5.5）调用，工具自行选 GPT Image 模型，支持多轮编辑、接受 File ID 作为输入图。Responses 路径的计费 = 主线模型 token + 图像生成费。
- **流式部分图（API 文档）**：支持 streaming，`partial_images` 可设 0–3，边生成边返回中间图，做交互式预览。
- **编辑/inpainting（API 文档）**：支持带 mask 的局部编辑，编辑图与 mask 需同格式同尺寸、<50MB；多张参考图编辑（因恒为高保真，input token 偏高）。
- **输出格式与压缩（API 文档）**：默认 `png`，可选 `jpeg`/`webp`；jpeg/webp 可设 `output_compression` 0–100%；jpeg 比 png 快，延迟敏感优先用 jpeg。
- **延迟（API 文档）**："Complex prompts may take up to 2 minutes to process"（复杂 prompt 最长约 2 分钟），方图通常最快。
- **快照与版本（API 文档）**：别名 `gpt-image-2` → 快照 `gpt-image-2-2026-04-21`。
- **限速（API 文档）**：按 tier 给 TPM/IPM——Tier1: 100k TPM / 5 IPM；Tier2: 250k / 20；Tier3: 800k / 50；Tier4: 3M / 150；Tier5: 8M / 250；Free 不支持。不支持 streaming(函数式)、function calling、structured outputs、fine-tuning、predicted outputs（指作为通用 LLM 能力，非指图像流式）。
- **使用门槛**：调用 GPT Image 系列需完成 API 组织验证（Organization Verification）。
- **计费（Pricing 页，按每 100 万 token）**：`gpt-image-2` 图像 **输入 $8.00 / 缓存输入 $2.00 / 输出 $30.00**；文本 输入 $5.00 / 缓存 $1.25。Batch 价腰斩：图像 输入 $4 / 缓存 $1 / 输出 $15。对比 `gpt-image-1.5`（图像输出 $32）略低；远高于 `gpt-image-1-mini`（图像输出 $8）。

## 评测 benchmark（把效果讲清楚）
**关键提醒：OpenAI 未发布任何能力 benchmark（无 GenEval / DPG-Bench / T2I-CompBench / FID / 人评 ELO 等数字）。** System Card 只有**安全/对抗评测**数字，发布博客只有定性宣传 + 图廊。因此本节"能力 SOTA 对比"维度只能写**未报告**，下面是源里**确有**的安全评测硬数字（来自 System Card Table 1，对抗 prompt 专门设计来诱导违规，**不代表真实流量分布**）：

- **Instant mode（gpt-image-2 标准模式）**：3112 条对抗 prompt → 685/3112（**22.0%**）产出被评判为违规（V）。其中图像层(IT)拦截 598/685（**87.3%**）、prompt 层(PT) 529/685（77.2%）、prompt 层增量(PI) 60/685（8.8%）、**组合召回(CT) 658/685（96.1%）**、漏检(RU) 27/685（3.9%）；**最终 3085/3112（99.1%）对抗 prompt 落到安全产出**。
- **Thinking mode**：因首轮 3112 条只产生极少违规图，重跑累计 6944 次生成 → 464/6944（**6.7%**）违规（远低于 instant 的 22%，归因于 Safe Completions 把越界请求改写为安全版）。图像层(IT) 357/464（76.9%）、prompt 层(PT) 222/464（47.8%）、增量(PO) 49/464（10.6%）、**组合(CT) 406/464（87.5%）**、漏检 58/464（12.5%）；**最终 6886/6944（99.2%）安全产出**。
- **生物安全 Preparedness（System Card）**：在生物/化学域，少数情况下生成的信息图被生物武器专家判定"准确到可能对新手提供 uplift"，故 OpenAI 按"**高生物能力**"设防——新增 image-specific 生物风险安全政策，对所有输入/输出用安全推理模型审查；用 772 张该类风险图评测安全监视器，召回/精度与其文本侧生物风险系统相当。网络安全/AI 自我改进域判定无实质风险（图像模型无法执行代码扩展攻击）。
- **能力侧 benchmark（GenEval / DPG / CompBench / FID / CLIPScore / 人评 Arena / 编辑评测 等）**：**官方全部未报告**。发布博客仅定性宣称"更高精度与控制力""更强多语言文字渲染""更逼真的写实与风格表现"，无任何量化对比。
- **官方自述能力限制（API 文档）**：① 延迟（复杂 prompt 可达 2 分钟）；② 文字渲染虽大幅改善仍可能在精确定位/清晰度上出错；③ 跨多次生成的角色/品牌**一致性**仍可能不稳；④ 结构化/版式敏感构图的**元素精确摆位**仍有困难。

## 创新点与影响
- **核心创新 = Thinking mode：把推理 + 工具调用引入生图。** 这是本次发布最实质的范式增量——生图前先**联网搜索 + reasoning 规划 + 多图生成**，把"文生图"从一次性采样升级为 agentic 的"调研→构思→成图"。配套的 Safe Completions 取向使越界请求被改写为安全版（对抗集违规产出率 22.0%→6.7%）。
- **工程能力跃迁**：分辨率到 4K、图像输入**恒高保真**、多轮对话式高保真编辑、流式部分图——把它做成更适合"设计资产生产"的产品形态（杂志跨页、信息图、多语言海报、品牌物料）。
- **provenance（System Card）**：持续 C2PA 元数据（参与 C2PA Conformance Program）+ **不可感知、鲁棒、内容相关的水印** + 内部溯源工具，用于判定图像是否出自 OpenAI 产品。延续 [[gpt-image-1]] 的 C2PA 承诺并加水印。
- **对后续工作的影响**：把"reasoning + tools"接入生成式视觉，是 2026 年图像生成 agent 化方向的一个高曝光范例，呼应"thinking 模型 + 工具栈统一应用到多模态产出"的趋势。
- **已知局限**：① OpenAI **零技术披露**（无论文/架构/数据/训练/能力 benchmark），外界无法核验方法与真实 SOTA 位置；② 不支持透明背景（较前作回退）；③ 一致性/精确版式/文字定位仍有缺陷；④ 高保真强制 → 编辑/参考图请求 token 成本偏高；⑤ 复杂 prompt 延迟可达 2 分钟。

## 原始链接
- blog（发布公告，图廊为主，少量定性文案）: https://openai.com/index/introducing-chatgpt-images-2-0/
- system-card（HTML，含 TOC + PDF 入口）: https://deploymentsafety.openai.com/chatgpt-images-2-0
- system-card（PDF 全文）: https://deploymentsafety.openai.com/chatgpt-images-2-0/chatgpt-images-2-0.pdf
- api-model-doc（模态/快照/限速）: https://developers.openai.com/api/docs/models/gpt-image-2
- image-generation-guide（分辨率/质量/保真/编辑/流式/限制）: https://developers.openai.com/api/docs/guides/image-generation
- pricing（按 token 计费）: https://developers.openai.com/api/docs/pricing

## 本地落盘文件
- ../../../sources/omni/2026/gpt-image-2--blog-zh.md
- ../../../sources/omni/2026/gpt-image-2--system-card.pdf
- ../../../sources/omni/2026/gpt-image-2--system-card.txt
- ../../../sources/omni/2026/gpt-image-2--system-card-toc.md
- ../../../sources/omni/2026/gpt-image-2--api-model-doc.md
- ../../../sources/omni/2026/gpt-image-2--image-generation-guide.md
- ../../../sources/omni/2026/gpt-image-2--pricing.md
