---
title: "Reve 2.0"
org: "Reve AI"
country: US
date: "2026-06"
type: blog
category: unified
tags: [t2i, layout, image-editing, 4k, diffusion, llm-planner, qwen, agentic, closed-source]
url: "https://blog.reve.com/posts/announcing-reve-2.0/"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/reve-ai"
hf_url: ""
modelscope_url: ""
project_url: "https://reve.com"
downloaded:
  - reve-2-0--announcement-blog.md
  - reve-2-0--the-layout-bet.md
  - reve-2-0--the-new-reve-vision.md
  - reve-2-0--model-landing-page.md
  - reve-2-0--arena-t2i-leaderboard.md
  - reve-2-0--github-org.md
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Reve 2.0 是 Reve AI（美国 Palo Alto）2026-06-03 发布的统一图像生成/编辑模型，核心创新是把「文本 prompt → 像素」的两段式范式替换为「**layout（结构化、代码式的中间表示）→ 像素**」：先用一个 **Large Layout Model（在开源 Qwen LLM 上继续预训练 + 后训练）** 把任意 layout/指令/图像输入推理成 layout，再用 diffusion 渲染器渲成**原生 4K×4K（16MP）**像素。结果：在 Arena 文生图榜首发即 **#2、Elo 1273**，较自家 v1.5（#20、1153）**+约 120–125 Elo**，且自称用「**少 10×的 GPU**」训练，是「sub-$1T 公司里最强的图像生成模型」。

## 背景与定位
主流图像模型（[[sdxl]] [[flux-1]] [[seedream]] [[nano-banana]] 一类）的内部范式是：LLM 把用户 prompt 扩写成长描述，diffusion 据此渲染。Reve 团队的判断是——**文本作为中间表示根本性地有歧义，而歧义是「可控」的天敌**：改一个词整张图就变，想精确指定某物的颜色/位置在纯文本里几乎做不到。

Reve 押的另一条路（"The Layout Bet"）是：**用 layout 替换英文散文做中间表示**。layout 是一个结构化、层级化的图像描述——每个元素都有位置、大小、局部描述，以及可选的图像引用 / 颜色等属性；它是图像的「骨架」，把**语义意图与像素渲染解耦**，正如 HTML 之于网页、SVG 之于矢量图。因为 layout 是可读的结构化格式，它成了「人 ↔ AI agent」共享的接口，既能用自然语言指令细化，也能**直接编辑 layout 结构**来编辑图。

技术脉络上的演进：
- **Reve Preview（2025-03）**：建立了 Reve 标志性的「电影感 / 胶片 / 新闻摄影」美学。
- **Reve 1.0**：不在 caption 上训练，而在「定义构图、关系、风格、文字等的稠密**数据结构**」上训练——验证了「把第一代 diffusion 的 alt-tag 越扩越稠密」并非可控生成的最优路径（这是 layout 思想的雏形）。
- **新 Reve（2025-09，"the-new-reve"）**：首次把愿景产品化，把图像分解为「代码式中间表示（layout representation）」，并打包成四件套——图像创作/remix、拖拽式直接操作编辑器（beta）、创意助手 agent、API（beta）。
- **Reve 2.0（2026-06）**：把图像规划（layout）与 diffusion 架构结合，**参数量 ×3、数据更多、算力更多**，并重建了编辑器。官方定位「Reve 2.0 替代此前所有模型」。

愿景层面，Reve 把图像生成类比为**程序合成（program synthesis）**：图像不该被当作「成品文件」，而该像**代码**一样——人和 agent 都能读、写、推理。layout 只是这条路的第一步。

## 模型架构
> 注：Reve 为闭源产品，无技术论文/权重/代码。以下来自官方博客（"The Layout Bet"）与 reve.com 模型页的自述，工程细节多未公开。

**两段式「planning → rendering」架构（分离关注点）：**

1. **规划端 —— Large Layout Model（统一大 layout 模型）**
   - 一个**统一的自回归 LLM**，用于「agentic 的视觉理解与生成」。
   - 输入：**任意组合的 layout + 指令 + 图像**。
   - 过程：从内部「**thinking trace**（思维轨迹）」中**推导出 layout**（即把规划当成一段可读的推理 + 结构化输出），再交给渲染器。
   - 底座：**在开源 Qwen LLM 上做 continued pretraining + post-training**（官方原文致谢「thank you, Qwen team!」），让模型学会围绕 layout 表示的**空间推理**能力。
   - 因为图像被表示为 layout（代码式），模型是 **agent-native** 的：agent 既能「看见」图，也能「推理」图（类比 LLM 在 code 上远比在 direct computer-use 上强）。

2. **渲染端 —— diffusion 渲染器**
   - 一个**新颖且高性能的渲染架构**，把 layout 渲成像素。
   - **原生 4K×4K（16MP）**输出，号称「世界上最快的 4K 图像模型」；4K 被当作**一等公民 primitive**，而非后处理 upscaling 步骤（避免 upscale 时细节漂移）。
   - 同一渲染架构被设计为**抗退化（resist collapse）**：在反复以生成图作引用的迭代工作流中，比其他模型更稳定。

**Diffusion + Autoregressive 的「取长补短」论述（官方原文）：**
- Diffusion：图美但「不够智能、不可控（steerable）」。
- Autoregressive LLM：极智能但「图不够美学，且延迟高、创意迭代痛苦」。
- Reve 2.0：**用 layout 把「规划（LLM 擅长，且可读可改可参与）」与「渲染（diffusion 出图）」分离**，既得 LLM 的智能/可控，又得 diffusion 的美学。

**参数与分辨率策略：**
- 参数量：Reve 2.0 较前代（Reve 1.0）**约 3×**（"3x the number of parameters"）。绝对参数量**未披露**。
- 分辨率：原生 4K×4K = 16MP，print-ready；landing 页给出 1080p/2K/4K 对比。
- text encoder / VAE / visual tokenizer 的具体形态、layout 的具体 schema（字段/序列化格式）**均未披露**。

## 数据
- **规模**：在「**数十亿（billions of）图像**」上构建了一条**新颖数据管线**。
- **bootstrap 方式**：管线**由稠密的人工标注（dense human annotations）bootstrap**——即先有人工密集标注作为种子，再放大。
- **layout 数据**：Reve 1.0 即已用「定义构图、关系、风格、文字等的稠密数据结构」训练（而非 caption），2.0 在此基础上「**更多数据**」。
- **来源 / 配比 / 清洗过滤 / 合成数据 / 美学与安全过滤**：**均未披露**具体细节。
- 标注层面强调的能力指向：layout 需要每元素的位置/大小/局部描述/引用/颜色等结构化标签，因此数据管线本质是「图像 → layout 结构」的大规模标注/反标注（具体自动化程度未披露）。

## 训练方法
- **整体范式**：两段式独立训练——
  - **Layout 模型**：在**开源 Qwen LLM** 上做 **continued pretraining + post-training**，习得围绕 layout 表示的**空间推理**（next-token 式自回归，含 thinking trace / 推理轨迹）。
  - **Diffusion 渲染器**：新颖渲染架构（训练目标 diffusion/flow-matching 之具体形式**未披露**）。
- **多阶段脉络**（跨版本，非单次 run）：alt-tag→稠密 caption（早期 diffusion）→ 稠密数据结构（Reve 1.0）→ layout 规划 + diffusion 渲染、×3 参数 + 更多数据 + 更多算力（Reve 2.0）。
- **偏好对齐 / RLHF / DPO / reward model / 蒸馏加速（consistency/LCM/ADD/步数蒸馏）等**：**均未披露**。渲染器「世界最快 4K」暗示有强力推理加速，但手段未公开。
- **关键超参 / trick**：未披露。

## Infra（训练 / 推理工程）
> 官方未公开 Reve 2.0 的算力/并行/精度细节；以下区分「官方明示」与「从 GitHub fork 推断」。

**官方明示：**
- **训练用「比竞争对手少 10× 的 GPU」**，自称是「sub-$1T 公司里最强图像生成模型」——核心卖点之一就是**算力效率**（layout 范式 + 规模更小）。
- 团队位于 **Palo Alto, California**，由研究员/创意者/工程师组成。
- 产品形态：reve.com Web 编辑器（流式渲染、对象级直接操作编辑器）+ **官方 API（beta，含 create/edit/remix；SDK 仓库 `reve-ai/reve-sdk`）**。API(beta) 与四件套形态见 "the-new-reve" 博客；具体安装命令官方源未列，故略。

**从 `github.com/reve-ai` 公开仓库推断（非 2.0 模型确证，仅技术栈信号；仓库名已落盘核对，fork 上游关系因需 JS 渲染未逐仓确证）：**
- org 下有 **sglang / SpecForge**（推理服务 + 投机解码）→ LLM/规划端可能用 SGLang 系服务。
- org 下有 **megablocks**（MoE block-sparse）→ 规划端可能含 MoE。
- org 下有 **tilelang / tvm / flash-attention**（算子编译/内核）→ 自研/定制 kernel。
- org 下有 **torchft**（容错训练）、**jax-tpu-hacks**（JAX/TPU 实验）→ 训练侧或有容错与 TPU 路线探索。
- 这些仓库名与知名上游开源项目同名，是「公司在用」的强信号，但**未被官方与 Reve 2.0 直接绑定**，写入仅作背景，不当作 2.0 的确证配置。

**算力规模 / GPU·时 / 并行策略 / 混合精度 / 推理步数·缓存·量化**：均**未披露**。

## 评测 benchmark（把效果讲清楚）
**Arena（arena.ai）文生图榜，官方称首发 #2；独立快照（页面标注 "Jun 5, 2026"，全榜 5,391,418 票；榜单含 70+ 模型，确切数未在静态 HTML 给出）核对如下：**

| 排名 | 模型 | 厂商 | Elo | 票数 | 备注 |
|---|---|---|---|---|---|
| 1 | gpt-image-2 (medium) | OpenAI | **1385** ±6 | 45,100 | Preliminary |
| **2** | **reve-2.0** | **Reve** | **1273** ±9 | 4,759 | **Preliminary** |
| 3 | gemini-3.1-flash-image-preview (nano-banana-2) | Google | 1269 ±4 | 75,713 | |
| 4 | mai-image-2.5 | Microsoft AI | 1253 ±6 | 12,100 | Preliminary |
| 5 | gemini-3-pro-image-preview-2k (nano-banana-pro) | Google | 1245 ±4 | 114,130 | |
| 6 | gpt-image-1.5-high-fidelity | OpenAI | 1241 ±4 | 118,438 | |
| 16 | flux-2-max | Black Forest Labs | 1163 ±4 | 115,675 | |
| **20** | **reve-v1.5** | **Reve** | **1153** ±6 | 18,677 | |

- **+125 Elo over v1.5**（官方原话，as of 2026-06-03）：快照里 reve-2.0 1273 − reve-v1.5 1153 = **+120 Elo**（与官方 +125 一致，差异因快照日期/票数变化）。**v1.5 自身排名 #20**，2.0 跳到 **#2**，即一代跨越约 18 个名次。
- **超越的同期对手**：Google nano-banana-2 / nano-banana-pro 系、Microsoft mai-image-2.5、OpenAI gpt-image-1.5、xAI grok-imagine、BFL flux-2 全系、Alibaba qwen-image-2.0-pro、Ideogram 4.0、Luma uni-1.1 等；仅落后 OpenAI **gpt-image-2 (medium) 1385**。
- 注：reve-2.0 仍标 **Preliminary（4,759 票，置信区间 ±9 较宽）**，名次后续可能微调。

**官方自做的消融（"The Layout Bet"，无外部可复现的标准 benchmark 数字，FID/GenEval/DPG 等未报告）：**
- **大规模 ablation：layout 模型在同等参数下持续优于「基于 prompt 的生成器」**，「全面显著更好」。
- **重建质量（CLIP similarity by region count，纯 layout、零像素输入下重建原图）**：
  - 0 regions → 0.865；10 → 0.905；20 → 0.913；30 → 0.923；40 → 0.927；50 → 0.929。
  - 即**区域数越多，重建越精细**；而「纯文本 prompt 无论多详细都无法忠实重建原图」。提供像素时（编辑场景）layout 更强，可做精确定点编辑。
- **scaling laws 适用于 layout 模型**：模型越大质量越高；且**输出区域数越多（= 更大的「视觉思考上下文」）图像质量越高**。
- **能力侧（landing 页定性，无量化）**：原生 4K 细节、跨多张 reference 锁定风格/角色/外观、街景/招牌/包装/车牌等**环境排版文字**清晰可读、抗迭代退化（image reference 下退化更少；无 reference 时「锁定元素、零退化」）。

**未报告**：FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore、GEdit/MagicBrush 等标准编辑评测——官方一概未给。唯一外部第三方数字即 Arena Elo。

## 创新点与影响
**核心贡献：**
1. **Layout-as-intermediate-representation**：用结构化、代码式 layout 替代自然语言 prompt 做生成/编辑的中间层，把「规划」与「渲染」解耦——这是与 FLUX/Seedream/Imagen/Nano-Banana 等「LLM 扩写 prompt + diffusion 渲染」主流范式的根本路线分歧。
2. **Large Layout Model**：在开源 Qwen LLM 上继续训练得到「会做空间推理、产出 layout」的统一自回归规划模型；图像因此**agent-native**（可被 agent 读写推理）+ **可直接拖拽操作**（同一表示既支持 NL 编辑也支持像素级直接操作）。
3. **算力效率**：自称少 10× GPU 取得 Arena #2，把「范式优势 → 训练成本优势」作为卖点。
4. **原生 4K（16MP）渲染** + **抗迭代退化**：把高分辨率与编辑稳定性当一等公民，而非 upscaling 后处理。
5. **模型即产品**：layout（代码）= 模型输出，reve.com = 编辑器，模型与产品共同设计。

**影响：**
- 为「图像生成 = 程序合成」提供了一个有 Arena 实证支撑的路线样本，可能推动业界重估「越来越长的 prompt」这条路。
- layout 作为「人 ↔ agent 共享接口」，对 agentic 创意工作流（自动排版、可控编辑、可审查的生成过程）有方法论启发。

**已知局限 / 风险：**
- **闭源 + 无技术论文**：layout schema、diffusion 渲染器目标、数据来源/配比、训练超参、算力具体数全部未公开，难以复现与外部核验。
- **benchmark 单一**：仅 Arena Elo（且 2.0 仍 Preliminary、票数偏少 ±9），缺标准自动化指标横向对照。
- **「少 10× GPU」无算力明细佐证**，属厂商自述。
- 仍落后 OpenAI gpt-image-2，绝对参数量与训练规模未知。

## 原始链接
- blog（发布公告）: https://blog.reve.com/posts/announcing-reve-2.0/
- blog（技术故事 "The Layout Bet"，含 ablation/CLIP 数字/BibTeX）: https://blog.reve.com/posts/the-layout-bet/
- blog（愿景 "Introducing the New Reve"，layout representation 概念）: https://blog.reve.com/posts/the-new-reve/
- project_page（reve.com 模型页，最详尽技术自述 + 4K/编辑/美学论述）: https://reve.com
- benchmark（Arena 文生图榜，独立核对 Elo/名次）: https://arena.ai/leaderboard/text-to-image
- org GitHub（仅公开仓库/SDK，无 2.0 权重代码；仓库名落盘核对、推断技术栈）: https://github.com/orgs/reve-ai/repositories
- API SDK（产品形态确证）: https://github.com/reve-ai/reve-sdk

## 本地落盘文件
- ../../../sources/omni/2026/reve-2-0--announcement-blog.md
- ../../../sources/omni/2026/reve-2-0--the-layout-bet.md
- ../../../sources/omni/2026/reve-2-0--the-new-reve-vision.md
- ../../../sources/omni/2026/reve-2-0--model-landing-page.md
- ../../../sources/omni/2026/reve-2-0--arena-t2i-leaderboard.md
- ../../../sources/omni/2026/reve-2-0--github-org.md
