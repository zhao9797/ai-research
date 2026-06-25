---
title: "Reve Image 1.0 (Halfmoon)"
org: "Reve AI, Inc."
country: US
date: "2025-03"
type: blog
category: t2i
tags: [t2i, closed-source, prompt-adherence, typography, intent-driven, palo-alto, startup, halfmoon]
url: "https://reve.com/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://reve.com/"
downloaded: [reve-image--venturebeat-launch.md, reve-image--ainews-halfmoon.md, reve-image--reve2-landing.md, reve-image--about.md, reve-image--art-page.html, reve-image--artificialanalysis-arena.md, reve-image--artificialanalysis-t2i-leaderboard.md, reve-image--overchat-summary-secondary.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Reve Image 1.0 是 Palo Alto 创业公司 Reve AI（前 Adobe / Stability 团队）于 2025-03-25 发布的首款闭源文生图模型，发布前以匿名代号「Halfmoon」潜入 Artificial Analysis Image Arena 并冲上 **#1**（击败 Midjourney v6.1、Google Imagen 3、Recraft V3、FLUX 1.1 [pro]）；卖点是**提示遵循 + 美学 + 文字渲染**三项同时拉满，技术理念是把图像当「代码」一样用一个可推理、可编辑的**语义中间表征**来规划再渲染。**注意：Reve 1.0 从未发布技术报告或论文，下文架构/数据/训练细节官方基本未披露，绝大多数「数字」无一手出处。**

## 背景与定位
2025 年初的文生图格局里，闭源 SaaS 三强（[[midjourney-v6]] 系、[[ideogram-3-0]] 前代 Ideogram 2、Recraft V3）各有侧重：Midjourney 美学最强但提示遵循弱、Ideogram 专精排版文字、Recraft 偏设计/矢量；开源侧 [[flux-1-1-pro]] 与 [[stable-diffusion-3]] 提供高质量 backbone。Reve 的差异化主张是「单点全能」——同一个模型在**提示遵循、美学、文字渲染**三个传统上互相牵制的维度上同时领先。

更深层的定位来自团队的「creative intent / 语义中间表征」理念。联合创始人 Michaël Gharbi（研究科学家，Adobe 系）在发布时表述使命为「invent the future of intent-driven visual creation」，核心论点是：

- 「捕捉创作意图需要机器对自然语言和交互的深度理解；把意图变成画面需要交互式系统，它要对自己生成的视觉世界有深刻理解，从而能**迭代修改**它。」
- 创始团队成员 Taesung Park（Adobe 系；据公开履历为 pix2pix / CycleGAN / SPADE 等图像生成经典工作作者，**此谱系信息为外部常识，落盘源仅称其为 researcher / 团队成员，未列著作**）补充：「今天的文生图本质是个**随机的世界切片生成器，没有智能；这既是数据问题也是表征问题。我们需要图像版的『完整文档』表征，但目前没有好的表征。Reve 的使命是给视觉生成模型注入逻辑（logic）。」

这套「语义中间表征」思路在初代是隐性的，到 Reve 2.0（落地页本页采集时已上线；**确切发布日期落盘源未给**）才被明确为「images as code」：用类代码的数据结构显式定义构图、元素关系、风格、文字，再渲染为像素——这正是 Reve 1.0 已经在做、但 2.0 才讲清楚的事（见下）。技术脉络上 Reve 属于「[[latent-diffusion-ldm]] 系扩散渲染 + 上游语义/规划层」的组合范式，而非纯 end-to-end 文→像素。

## 模型架构
**官方对 Reve 1.0 的架构未做任何正式披露**（无论文、无技术报告、无 model card、无开源权重、无参数量）。可确证的只有 Reve 2.0 落地页对 1.0 的**回溯性描述**，以及发布期社区/媒体的观察：

- **「图像即代码」的中间表征（一手，来自 Reve 2.0 落地页回溯 1.0）**：Reve 2.0 页面明确写道——「Our previous model, **Reve 1.0, was trained not on captions, but on detailed data structures that define composition, relationships, style, text, and more**.」即 1.0 的训练条件不是稠密 caption，而是一套**结构化（类代码）的数据结构**来表达构图、元素关系、风格、文字。该页同时把这层叫做「a highly detailed, highly manipulatable, intermediate representation expressed as code」，并说这是「可控生成与可控编辑」的关键，而非「更稠密的 prompt」。
- **规划 + 渲染分离（planning vs. rendering）**：Reve 的设计哲学是先把图像「meticulously laid out」（布局/规划）再渲染，这样人或 agent 可以检查、参与、编辑布局来编辑图像。1.0 已体现这一思想（结构化数据结构作为条件），2.0 把它显式化为可见的 layout/code 层。
- **可能是「composite / 复合系统」而非单一模型**：AINews（2025-03-25）观察「There's no suggestion that it's a single model, but rather some composite of models」，与 Taesung Park「先用强语言能力理解意图、再生成」的两段式表述一致——即上游一个理解意图的语言/规划组件 + 下游一个扩散渲染组件。**这是合理推断，非官方确认。**
- **底层渲染器**：从 VentureBeat 实测「rapid generation speed」「支持参考图、风格匹配、用自然语言改色/改字/换视角」推断为隐空间扩散渲染器（与 [[latent-diffusion-ldm]] 系一致），但 backbone 是 U-Net 还是 DiT/MMDiT、VAE 规格、text encoder（T5/CLIP/LLM）均**未披露**。
- **参数量**：**官方未披露。** 二手站点（overchat，secondary）声称「12B 参数混合系统 / 多模态 + 并行 diffusion transformer」，但无任何一手出处，**视为不可信营销文案，不予采信**。唯一有方向性的一手信息是 Reve 2.0 落地页称 2.0 相对 1.0「3x the number of parameters」——即 2.0 参数是 1.0 的约 3 倍，但 1.0 的绝对值仍未公开。

关键架构理念可总结为一句：**不是「prompt 越稠密越好」，而是用一个人和机器都能理解、推理、操作的结构化语义中间层来规划图像，再交给扩散渲染器。**

## 数据
**官方未披露**数据来源/规模/配比/清洗过滤。可确证的唯一一手信息：

- Reve 1.0 的**训练条件不是 caption（alt-tag 扩写式稠密描述），而是「detailed data structures」**（结构化数据，定义构图、关系、风格、文字）。Reve 团队明确反对「把第一代扩散模型训练用的 alt-tag 越扩越长」这条路线，认为它不是细粒度创作控制的最优解（一手，Reve 2.0 落地页回溯）。这意味着 1.0 的数据管线很可能包含将图文对**重标注为结构化/类代码表征**的步骤（re-captioning → re-structuring），但具体生成方式、是否用合成数据、人工标注比例**均未披露**。
- 美学过滤、安全过滤、训练集规模、图文对数量：**全部未披露。**

## 训练方法
**官方未披露**训练目标、阶段划分、对齐方法、蒸馏方案。无法从一手源给出 diffusion / flow matching / next-token 的确切选择。可推断的极少量信息：

- 既然渲染端是扩散式（rapid generation、参考图、风格匹配），训练目标大概率是某种 **diffusion / flow-matching** 去噪目标 + **以结构化中间表征为条件**（而非纯文本 caption 条件）。
- 上游「理解意图」的语言/规划组件如何训练（是否复用现成 LLM、是否联合训练）**未披露**。
- 偏好对齐（RLHF/DPO/reward model）、步数蒸馏（consistency/LCM/ADD）等加速/对齐 trick：**未报告**。VentureBeat 提到产品默认开启「prompt text enhancement」（自动把用户输入扩写成更丰富的视觉描述），这是**推理时的 prompt upsampling**（类似其他模型的 prompt rewriter），不是训练方法。

**结论：训练方法这一维度官方近乎空白，本页不编造任何超参或目标函数。**

## Infra（训练 / 推理工程）
- **训练算力 / GPU·时 / 并行策略 / 混合精度 / 吞吐**：**全部未披露。**
- **推理 / 部署形态**：发布时仅通过官网 `preview.reve.art`（后并入 `reve.com`）**网页端免费预览**提供，**发布当时无 API、无定价、无开源**（VentureBeat 明确：「has not yet announced API access or long-term pricing plans, nor is it clear if the model will be proprietary or made open source」）。生成速度被实测者描述为「rapid」，VentureBeat 头图即用 Reve 现场生成。后续才逐步上线 API（截至本页采集，Artificial Analysis 仍标 Reve Image (Halfmoon)「No API available」，说明 1.0 这一档长期未开放标准 API）。
- 推理加速（步数、缓存、量化、蒸馏）：**未报告。**

## 评测 benchmark（把效果讲清楚）
Reve 官方**未发布任何标准学术 benchmark 数字**（无 GenEval / DPG-Bench / T2I-CompBench / FID / CLIPScore / HPSv2 / ImageReward 等）。效果证据全部来自**第三方人评 Arena（Artificial Analysis Image Arena，ELO 制对战投票）**：

- **发布即 #1（2025-03，一手 VentureBeat + AINews + Artificial Analysis 官方贺词）**：在 Artificial Analysis Image Arena「image generation quality」榜，Reve（即 Halfmoon）登顶 **#1**，超越 **Midjourney v6.1、Google Imagen 3（[[imagen-3]]）、Recraft V3（[[recraft-v3]]）、Black Forest Labs FLUX.1.1 [pro]（[[flux-1-1-pro]]）**。Artificial Analysis 官方在 X 上称其为「the world's leading image generation model」，并特别点名其**文字渲染、提示遵循、美学**三项突出。
- **at-launch 具体 ELO**：**一手源（VentureBeat / Artificial Analysis 贺词）只给「#1」，未给确切分值。** 二手站点 overchat 称 launch ELO≈**1167**，无一手佐证，**仅作参考、不作为结论**。
- **当前（本页采集时，2026 年中）位置**：Artificial Analysis Text-to-Image Leaderboard 上「Reve Image (Halfmoon)，Released Mar 2025」**ELO ≈ 1,097（95% CI ±9，4,109 samples），排名约第 66 位，「No API available」**——这是榜单一年多大幅迭代后的相对位置（榜首已是 GPT Image 2 ≈1,339、Nano Banana 2、HiDream-O1 等），并不代表它发布时的实力，仅说明它仍在榜内且为 2025-03 的产物。
- **媒体实测定性结论（VentureBeat，一手）**：
  - 文字渲染「on-par or better than Ideogram」「far surpassing Midjourney」——这是它最被认可的强项。
  - 提示遵循、多角色/复杂场景处理优于多数前代模型；生成快、易用。
  - **已知短板（实测，一手）**：透明材质等复杂物体（如盛满的酒杯）易出错；难以还原特定虚构角色（游戏角色会画成泛化形象）；多物体构图偶有细节错位。
- **消融 / 对照实验**：官方无任何消融披露。

**一句话：Reve 1.0 的「效果」证据是人评 Arena 登顶 + 媒体定性实测，没有任何官方学术指标数字。凡见到 1.0 的精确 benchmark 数（如「文字准确率 98%」「细节保留 92%」「27 种风格」等）均出自无出处的二手营销页，本页不采信。**

## 创新点与影响
**核心贡献 / 创新点：**
1. **「intent-driven / images-as-code」范式的第一个出圈产品**：用一个人和机器都可理解、可推理、可编辑的**结构化语义中间表征**（而非越来越稠密的 caption）来规划图像，再渲染——把「文→像素」的黑箱拆成「规划 → 渲染」，为后续可控编辑/agentic 图像奠定理念基础。这在 Reve 2.0「images as code + agent-native + 直接操作编辑器」上被推到极致。
2. **「单模型三项全能」的产品定位**：在 2025 年初首次让一个模型在提示遵循、美学、文字渲染上**同时**对标并超越各自的专精 SOTA（Ideogram 排版、Midjourney 美学、Recraft 设计），打破了「文字好就不美、美就不准」的传统取舍印象。
3. **隐身发布 + Arena 登顶的发布学**：以匿名「Halfmoon」先在第三方 Arena 刷出 #1 制造悬念再揭面，成为新创公司用第三方盲评背书冷启动的范例。

**团队与谱系（值得记一笔）**：据 AINews（标题即「ex-Adobe/Stability trio」）与 VentureBeat，创始团队是 **ex-Adobe / ex-Stability 三人组**——Christian Cantrell（Stability AI 前产品 VP，一手 AINews）、**Taesung Park**（一手源仅称 researcher；据公开履历为 pix2pix / CycleGAN / SPADE 等图像生成经典工作作者，**此著作信息为外部常识、不在落盘源**）、**Michaël Gharbi**（Co-Founder / 研究科学家，一手 VentureBeat），加上工程师 Hunter Loftis（一手 VentureBeat/AINews）等；公司即 **Reve AI, Inc.，Palo Alto**（一手 about 页）。名字取自法语「rêve」（梦，一手 AINews：「from rêve」）。这条「Adobe 创意工具 + GAN 时代生成研究」的血统，解释了它对「creative intent / 可控编辑 / 与产品共同设计模型」的执着。

**局限：**
- 完全闭源、无技术报告，外界对其架构/数据/训练**几乎一无所知**，可复现性为零，研究价值受限于黑箱。
- 发布期无 API、长期未开放标准 API，影响其作为基础设施被集成的广度。
- 实测短板（透明材质、虚构角色、多物体细节错位）说明其「语义中间表征」在 1.0 阶段仍不足以保证物理/语义完全一致——这正是 2.0 用「3x 参数 + 更多数据 + code 化 layout」要解决的问题。
- 在快速迭代的赛道里，发布一年多后已从 Arena #1 跌至中游，凸显纯产品/数据驱动、无公开方法护城河的模型生命周期之短。

## 原始链接
- blog / 产品落地页（Reve 2.0，含对 1.0 的回溯性描述）: https://reve.com/
- about（公司信息 Reve AI, Inc., Palo Alto）: https://reve.com/about
- 原始预览发布页（已并入 reve.com）: https://preview.reve.art/
- 第三方榜单（Artificial Analysis Image Arena；**注：落盘的 arena.md 仅抓到导航框架、无榜体数据，"#1"实证来自 VentureBeat/AINews/AA 官方 X 贺词，非此页面截图**）: https://artificialanalysis.ai/image/arena
- 第三方榜单（Text-to-Image Leaderboard，当前 ELO/排名）: https://artificialanalysis.ai/image/leaderboard/text-to-image
- 媒体发布报道（VentureBeat, Carl Franzen, 2025-03-25）: https://venturebeat.com/ai/the-new-best-ai-image-generation-model-is-here-say-hello-to-reve-image-1-0
- 技术社区总结（AINews / buttondown，含创始团队与理念）: https://buttondown.com/ainews/archive/ainews-halfmoon-is-reve-image-a-new-sota-image/
- 创始人 X 串（Michaël Gharbi, 理念阐述）: https://x.com/m_gharbi/status/1904213903384695280
- 二手综述（overchat，仅交叉参考，数字不可信）: https://overchat.ai/ai-hub/reve-image-generator

## 本地落盘文件
- ../../../sources/omni/2025/reve-image--venturebeat-launch.md
- ../../../sources/omni/2025/reve-image--ainews-halfmoon.md
- ../../../sources/omni/2025/reve-image--reve2-landing.md
- ../../../sources/omni/2025/reve-image--about.md
- ../../../sources/omni/2025/reve-image--art-page.html
- ../../../sources/omni/2025/reve-image--artificialanalysis-arena.md
- ../../../sources/omni/2025/reve-image--artificialanalysis-t2i-leaderboard.md
- ../../../sources/omni/2025/reve-image--overchat-summary-secondary.md
