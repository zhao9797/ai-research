---
title: "Ideogram 3.0"
org: Ideogram
country: US
date: "2025-03"
type: blog
category: t2i
tags: [t2i, typography, text-rendering, style-reference, graphic-design, closed-source, diffusion, product-launch, inpaint, fine-tuning]
url: "https://about.ideogram.ai/3.0"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://ideogram.ai"
downloaded: [ideogram-3-0--blog.md, ideogram-3-0--blog-snapshot.html, ideogram-3-0--api-generate-v3.md, ideogram-3-0--api-edit-and-training.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Ideogram 3.0 是 Ideogram（前 Google Imagen / Brain 成员创办）于 **2025-03-26** 发布的第三代闭源前沿文生图模型，延续其招牌的**图内文字渲染 / 海报排版**优势，并在**真实感（photorealism）、图文对齐（prompt alignment）、风格一致性**三方面显著进步；最大新功能是 **Style Reference（上传至多 3 张参考图控制美学风格）+ 从 43 亿（4.3 billion）风格预设库随机探索 + Style Code 复用**。官方唯一公开的量化结论是：在覆盖多样能力/主题/风格/难度的提示集上做人评，**Ideogram 3.0 的 ELO 评分高于所有对比的文生图模型（排名第一）**——但博客**未给出具体 ELO 数值、对手名单或胜率**。

## 背景与定位
- **要解决的问题**：扩散类 T2I 长期的两块短板——(1) **图内文字**拼写错乱、版式失控（海报/书封/广告/Logo 等设计场景的硬门槛）；(2) **真实感**与**复杂构图/空间关系**不足。Ideogram 自 1.0 起把 **typography** 作为差异化主轴，[[ideogram-2|2.0]]（2024-08）补齐了真实感与颜色控制，3.0 在两条线上继续推高，并新增**风格可控性**这一新轴。
- **技术脉络中的位置**：与 2025 年同期的 [[flux-1|FLUX]] 系列、[[imagen-3|Imagen 3]]、Recraft V3、Midjourney v6/v7、[[gpt-4o-native-image|GPT-4o 原生图像]] 等竞争"设计向 / 文字向"T2I 高地。Ideogram 的核心壁垒始终是**文字渲染质量 + 排版美学**，3.0 把它从"能拼对短词"推进到"长文本/复杂版式仍准确且艺术化"。
- **相对前置工作的改进**（官方表述）：相比 2.0，3.0 在 **image-prompt alignment、photorealism、text rendering quality** 三个维度均有"significant advancements"；并把**风格控制**从纯文本 prompt 升级为**视觉参考图 + 风格码**的工作流。
- **形态**：闭源，仅以 **App（web + iOS）+ API** 形态提供，无权重/无技术报告/无论文。发布即对 ideogram.ai 全量用户与 iOS App 开放；随后（2025 年）以 `ideogram-v3` 端点上线 API，并提供完整编辑套件与**自定义模型微调**。

## 模型架构
**未披露。** Ideogram 从未发布 3.0 的任何架构论文或技术报告，官方博客只讲产品能力，不讲 backbone / tokenizer / text encoder / 参数量。以下为基于**一手 API 文档**可确证的工程事实，以及明确标注的合理推断：

- **可确证（来自 API 文档）的能力面**：
  - **分辨率策略**：v3 支持一组离散分辨率枚举（`ResolutionV3`，文档标注 **69 个枚举值**），最长边约 **1536px**（如 `1536x640`、`512x1536`、`736x1312` 等；含竖、横、方多种比例）；另有 **15 个 `aspect_ratio` 枚举**（与 `resolution` 互斥，默认 1:1）。
  - **风格控制接口**：`style_type ∈ {AUTO, GENERAL, REALISTIC, DESIGN, FICTION}`（默认 GENERAL）；`style_preset`（**62 个预设枚举**）；`style_codes`（8 位十六进制风格码，对应博客"Style Code"）；`style_reference_images`（参考图，总大小上限 10MB，对应博客"Style Reference"，App 端至多 3 张）。三者互斥使用。
  - **主体一致性**：`character_reference_images`（角色参考，目前**仅支持 1 张**，可选 `character_reference_images_mask` 灰度遮罩）——单角色一致性能力。
  - **提示增强**：`magic_prompt ∈ {AUTO, ON, OFF}`（MagicPrompt 自动改写/扩写提示词）；`negative_prompt`（负向提示）；`color_palette`（预设名或带权重的十六进制成员，注：明确标注 V_1/V_1_TURBO/V_2A/V_2A_TURBO 不支持，即颜色面板是 2.0 系/3.0 的新能力）。
  - **安全/版权**：`enable_copyright_detection`——生成后接 **Hive**（likeness + logo 检测），命中则 `is_image_safe=false`。
- **合理推断（非一手确证，标注为推断）**：3.0 极大概率是**潜空间扩散（latent diffusion）**家族（与 1.0/2.0 一脉相承的扩散路线），文字渲染优势通常来自**强 text encoder + 高质量带文字图文对训练数据 + 字形/排版导向的数据策展**；但 Ideogram 是否在 3.0 上换用 **DiT/MMDiT** 等新 backbone、用什么 VAE/分词器、参数量多少，**官方均未披露**，不作断言。

## 数据
**未披露。** 官方既无技术报告也无数据卡，训练数据来源/规模/配比/清洗/re-captioning 等**全部未公开**。可从一手材料确证的、与"数据"相关的间接信号仅有：
- **风格预设库规模**："a library of **4.3 billion** presets"（43 亿风格预设），用于 Random style 探索——这是**风格码/预设空间**的规模描述，**并非训练样本量**，不应混淆。
- **文字/版式专长**：博客强调能生成"complex and lengthy compositions"（复杂且长的文字版式），强烈暗示训练数据中**带文字/排版的图文对**占比高且经过专门策展——但**具体比例未披露**。
- **自定义微调数据规格**（来自 API 文档，针对用户侧 fine-tune，非 Ideogram 自身预训练）：自定义模型数据集**至少 10 张、至多 100 张**图，支持可选 `.txt` caption（按文件名 stem 配对）。这反映 3.0 底座支持**少样本风格微调**，但与基座预训练数据无关。

## 训练方法
**未披露。** 训练目标（diffusion / flow matching）、多阶段流程（预训练→SFT→偏好对齐）、是否用 RLHF/DPO/reward model、蒸馏与步数加速方案等**均无一手披露**。可确证的间接信号：
- **多档"渲染速度"**：v3 API 暴露 `rendering_speed ∈ {FLASH, TURBO, DEFAULT, QUALITY}`（默认 DEFAULT）。这是**质量/速度/价格的可调权衡**——FLASH/TURBO 为更快更省的低步数/加速档，QUALITY 为更高质量档。这种"多档加速"通常对应**步数蒸馏 / 不同采样配置**的工程实现，但 Ideogram **未说明** FLASH/TURBO 是否来自蒸馏（如 LCM/ADD/一致性模型）还是单纯的少步采样，不作断言。
- **自定义微调（用户侧）**：完整流程为四步——建 dataset（`POST /datasets`）→ 上传 10–100 张图（可选同名 `.txt` caption，**按文件名 stem 配对**，如 `sunset.txt` 配 `sunset.jpg`；亦支持 ZIP）→ `POST /v1/ideogram-v3/train-model` 起训 → 轮询模型 `status`（文档示例仅出现 **`COMPLETED` / `ERRORED`** 两态，`is_available_for_generation` 为 `true` 即可用；**未见 `PENDING` 字样**，不臆造中间态）→ 以 `custom_model_uri` 在 generate 端点调用。这表明 3.0 底座设计上支持**轻量风格微调**，但微调算法（LoRA / DreamBooth 类 / 全参）**未披露**。

## Infra（训练 / 推理工程）
**训练 infra 完全未披露**（无 GPU 规模 / GPU·时 / 并行 / 吞吐数据）。推理与部署侧可从一手材料确证：
- **部署形态**：闭源 SaaS——web App、iOS App、REST API（`api.ideogram.ai/v1/ideogram-v3/*`）、官方 **MCP server**（`developer.ideogram.ai/_mcp/server`，面向 Claude Code / Cursor 等 AI 客户端集成）。生成结果为限时有效的临时图片 URL（需自行下载留存）。
- **推理档位**：FLASH/TURBO/DEFAULT/QUALITY 四档渲染速度（速度↔质量↔价格权衡，见上）；单次可批量出图 `num_images`（OpenAPI 仅标 `default: 1`，**文档未给上下界**，不臆造具体范围）；App 端 **Batch Generation** 支持规模化批量出图。
- **安全管线**：生成后可选接 Hive（人物 likeness + logo 版权检测），增加少量延迟；组织级开关与单请求开关取 OR 逻辑。
- **量化 / 缓存 / 显存等底层推理优化**：未披露。

## 评测 benchmark（把效果讲清楚）
**这是本工作信息最稀薄的部分**——Ideogram 3.0 **没有发布任何标准学术 benchmark 数字**（无 FID、无 GenEval、无 T2I-CompBench、无 DPG-Bench、无 MJHQ-30K、无 HPSv2/ImageReward/PickScore 等）。一手博客中唯一的量化主张：

- **人评 ELO 第一**：在"a set of diverse prompts that probe a wide variety of capabilities, subjects, styles, use cases, and composition difficulty"上做 human evaluations，**Ideogram 3.0 的 ELO rating 在所有对比文生图模型中最高（排名第一）**。
  - **重要限定**：博客**未给出**具体 ELO 数值、**未列出**对比模型名单、**未给**胜率/置信区间、**未说明**评测人群与规模。官方页面仅以一张图表（图像形式）展示，**无可抄录的数字**。因此"ELO 第一"是**自报告、无可复核数字**的营销结论，不能当作严格 benchmark 引用。
- **能力性主张（定性，非量化）**：
  - 文字渲染：可生成"remarkable precision"的程式化、准确文字，含其他模型难以处理的复杂/长文本版式。
  - 真实感："blurs the line between generated and real imagery"，支持复杂空间构图、精细背景、精准光影与色彩、逼真环境细节。
  - 风格一致性：Style Reference + Style Code 实现跨次生成的稳定美学。
- **第三方对比**：本页严格只用一手源，故**不引入**外部第三方 arena（如 LMArena/Artificial Analysis）的 Ideogram 3.0 排名数字——这些**不在已抓取的一手材料内**，按规范记为"未在一手源中报告"。

> 小结：**官方一手源未提供任何可复核的标准 benchmark 数字**；唯一量化主张（ELO 第一）无数值、无对手名单、无方法细节。视为"未报告（量化层面）"。

## 创新点与影响
- **核心贡献**：
  1. **Style Reference 工作流**——把"难以用文字描述的风格"转为**视觉参考图（≤3 张）+ 可复用 Style Code + 43 亿预设随机探索**的可控、可复现风格系统，是 3.0 相对 2.0 最显著的产品级创新。
  2. **设计向文字/版式的进一步突破**——长文本、复杂多语种版式（博客示例含法语海报、书封、Logo 等）仍保持高准确度与艺术性，巩固 Ideogram 在"设计场景 T2I"的差异化壁垒。
  3. **真实感与复杂构图**的明显提升，使其从"擅长设计图"扩展到"可做摄影级真实图"。
  4. **完整生产级编辑/定制套件**（随 API 落地，端点名以官方 API 文档为准）：**Inpaint/Edit**（`/v1/ideogram-v3/inpaint`，按遮罩局部重绘；注：官网 App 把它叫 "Magic Fill"，但**该叫法不在已抓取的一手源中**，故仅以 API 名 Inpaint/Edit 为准）、**Replace Background**（`/replace-background`，替换背景；并支持 Remove Background 做透明抠图）、**Reframe**（`/reframe`，把图外扩到目标分辨率，即 outpaint）、**Remix**（`/remix`，以原图为基重生成，可调原图影响强度）、**Face Swap**（经 Edit 端点换脸）、以及 **10–100 张图的自定义风格微调**。这把 3.0 从"出图模型"做成"端到端创意/品牌资产工作流"。（注：原页曾列 "Layerize Text" 与独立 "Upscale" 端点——二者**均未在已抓取的一手 API 文档中出现**，已删除；`upscaled_resolution` 仅作为响应字段说明"若操作改变了尺寸"，不等于存在 Upscale 端点。）
- **对后续工作的影响**：强化了"**风格参考图 + 风格码**"作为 T2I 可控风格的主流交互范式（与 Midjourney `--sref`、各家 style/IP-adapter 路线呼应）；并示范了"**强文字渲染 + 设计套件 + 品牌微调**"打包成 B 端（中小企业/营销/POD）生产力产品的商业路径。
- **已知局限**：
  - **完全闭源、零技术披露**——无权重、无论文、无 benchmark 数字、无架构/数据/训练细节，**学术可复核性为零**，本页大量维度只能记"未披露"。
  - 唯一量化主张（ELO 第一）**不可复核**。
  - 角色一致性当前**仅支持单张角色参考**。
  - 由后续 Ideogram 4.0（2025 年晚些发布，官网已替换为 4.0 主推）可反推 3.0 已被自家迭代超越；原 `about.ideogram.ai/3.0` launch 页现已 404，本页正文依赖 **Wayback 2025-03-26 存档**与现行 **v3 API 文档**。

## 相关页面
- [[ideogram-2]] — 前代 Ideogram 2.0（2024-08），补齐真实感与颜色控制
- [[flux-1]] · [[imagen-3]] · [[gpt-4o-native-image]] — 同期"设计向 / 文字向"T2I 竞品

## 原始链接
- blog（官方发布页，原 URL 现 404）: https://about.ideogram.ai/3.0
- blog（Wayback 存档，发布当日 2025-03-26）: http://web.archive.org/web/20250326170835id_/https://about.ideogram.ai/3.0
- api-doc（Generate with Ideogram 3.0，含分辨率/风格/渲染速度/版权检测等全参数）: https://developer.ideogram.ai/api-reference/api-reference/generate-v3
- api-doc（Inpaint / Replace Background / Reframe / Remix v3 + 自定义模型微调）: https://developer.ideogram.ai/api-reference/api-reference/inpaint-v3 ；https://developer.ideogram.ai/tutorials/custom-model-training
- api-overview（能力总览：Generate/Remix/Edit/Reframe/Replace Background/Face Swap）: https://developer.ideogram.ai/ideogram-api/api-overview

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ideogram-3-0--blog.md) （launch 博客正文，Wayback 存档清洗为 markdown）
- [blog-snapshot.html](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ideogram-3-0--blog-snapshot.html) （launch 博客原始 HTML 存档，631KB）
- [api-generate-v3.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ideogram-3-0--api-generate-v3.md) （v3 generate 端点官方文档 markdown，含分辨率/风格/渲染速度/字符参考/版权检测）
- [api-edit-and-training.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/ideogram-3-0--api-edit-and-training.md) （v3 Inpaint/Replace Background/Reframe/Remix + 自定义模型训练 + API 总览，官方文档合并）
