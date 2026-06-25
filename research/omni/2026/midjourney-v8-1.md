---
title: "Midjourney V8.1"
org: "Midjourney"
country: "US"
date: "2026-04"
type: "blog"
category: "t2i"
tags: [t2i, midjourney, closed-source, aesthetic-preference, hd, fast-inference]
url: "https://updates.midjourney.com/v8-1-alpha/"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.midjourney.com"
downloaded: [midjourney-v8-1--version-docs.md, midjourney-v8-1--alpha-post.md, midjourney-v8-0--alpha-post.md, midjourney-v8-1--default-model.md, midjourney-v8-1--updates-apr30.md, midjourney-v8-1--draft-mode.md, midjourney-v8--rating-party.md, midjourney-v8-1--high-res-rating.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Midjourney V8.1 是 Midjourney 2026 年 V8 系列的第二个迭代（基座 V8.0 于 2026-03-17 内测，V8.1 于 2026-04-30 发布、2026-06-10 成为默认模型），是一款**闭源**文生图产品模型；最关键的卖点是**速度**——官方称标准任务渲染比旧版快约 4–5 倍，SD（标准）出图约 4 秒、HD（原生 2K）约 12 秒，HD 模式相比 V8.0 alpha 提速并降价约 3 倍；同时保持与 V7 一致的审美风格、更强的提示词遵循和文本渲染。架构、数据与训练的工程细节**均未公开**。

## 背景与定位
Midjourney 一贯**不发表论文 / 技术报告 / model card**，模型为纯闭源 SaaS（Web + Discord），所有可考信息只来自官方更新博客（updates.midjourney.com）与帮助文档（docs.midjourney.com）。因此本页对“数据 / 架构 / 训练目标 / infra / 标准 benchmark”等维度只能给出官方博客披露的定性信息与零散数字，**严禁推测具体技术实现**。

技术脉络上，V8.1 延续 Midjourney 自 [[midjourney-v6]]、V6.1、V7 一路演进的产品迭代：
- **V6**（2023-12）：长提示词准确性、连贯性、图像提示与 remix。
- **V6.1**（2024-07）：连贯性与细节提升，比 V6 快约 25%。
- **V7**（2025-04 发布、2025-06 默认）：文本/图像提示精度大幅提升，纹理与肢体/手部连贯性改善；docs 明确 V7 **引入 Draft Mode 与 Omni Reference**（个性化 Personalization 在 V6 已支持，非 V7 新增）。
- **V8.0 alpha**（2026-03-17，仅在 alpha.midjourney.com 内测）：全新模型，号称比此前快约 5 倍；新增原生 2K 的 `--hd` 模式与提供额外连贯性的 `--q 4` 模式；强调通过个性化、风格参考（sref）、moodboard 理解用户审美；引号内文本渲染显著改善。
- **V8.1**（2026-04-30）：在 V8.0 基础上做审美回调与效率优化，找回 V7 风格的稳定一致性，回归社区喜欢的 image prompt / image weight 等功能，并将 HD 设为默认（后因服务器迁移又临时改回 SD 默认）。

V8.1 在 Midjourney 自家版本谱系中的定位是“**最快的 Midjourney 模型**”，主打**快速探索/迭代**的体验（官方称 V8.1 SD 满质量的速度相当于 V7 的 draft 模式），同时把原生高分辨率（2K）作为常态化能力。它与同期开源/可控的扩散家族（如 [[latent-diffusion-ldm]]、[[rectified-flow]]/[[flow-matching]] 路线、[[latent-consistency-models]] 加速）属于**完全不同的披露范式**——后者公开方法与权重，Midjourney 只公开产品行为。

## 模型架构
**未披露。** 官方从未公布 V8/V8.1 的 backbone（U-Net / DiT / MMDiT / 自回归 / 掩码生成均无确认）、visual tokenizer / VAE、text encoder（T5 / CLIP / LLM）、条件注入方式、参数量或具体分辨率策略。可从博客观察到的、与架构能力相关的产品级事实：

- **分辨率档位**：V8.1 支持两档——
  - **SD（标准分辨率）**：默认快速档；
  - **HD**：**原生 2K（2048px）渲染、无需 upscale**（与 V6/V7 不支持原生 HD 形成对比）。官方称“HD 模式下 V8.1 输出是 V7 图像的 2 倍尺寸、4 倍分辨率”。HD 的最大宽高比限制为 4:1（SD 仍为 14:1）。
- **额外连贯性档**：V8.0 alpha 引入 `--q 4` 模式提供“一点额外连贯性”（V8.1 的 Quality 参数表标为不适用，疑随版本调整；见“局限”）。
- **控制/条件能力**（产品层）：支持 `--chaos`、`--weird`、`--exp`、`--raw`（去默认风格化、提升提示遵循）、`--stylize`、`--tile`、`--sref`（Style Reference，含 sref code）、Moodboard、Personalization profile、Image Prompt + Image Weight、Seed（V8.1 标注 seed 复现“99% 一致”）。
- **不向后兼容/复用的能力**：V8.1 的 **Character Reference / Character Weight 不支持**；**Omni Reference 在 V8.1 下回退使用 V7 模型**（官方说明“V8 改进版 Omni Reference 仍在训练中”）；**Editor / Pan / Zoom Out 在 V8.1 下复用 V6.1 的对应模型**（docs 对照表标注 “Using V6.1”）；**Upscaler 在 V8.1 仅作用于 SD 图像**（docs 标 “SD Images”，并非复用 V6.1）；不支持 Turbo 模式、不支持 Multi-Prompting、不支持 `--niji`。

这些都属于行为/接口层面的观察，**不能据此反推内部网络结构**。

## 数据
**未披露。** 官方从未公布训练数据来源、规模、配比、清洗过滤、re-captioning 或合成数据策略。唯一可考的、与“数据”相关的一手信息是**人类审美偏好数据的众包采集机制**（详见“训练方法”）：Midjourney 通过“Rating Party”让社区对成对图像做美学偏好打分，作为模型优化的训练信号。除此之外，图文对数量、版权来源、安全/NSFW 过滤等均无官方数字。

## 训练方法
**训练目标 / 多阶段流程 / 蒸馏方案均未披露。** 不过 Midjourney 公开了其标志性的**人类审美偏好对齐数据闭环**，这是其训练方法中可考的核心部分：

- **Rating Party（成对偏好打分）**：发布前与发布后，官方在 `midjourney.com/rank-v8`、`rank-v8-1` 等页面投放成对图像，让社区用户选择“更美”的一张（键 1 = 左、2 = 右、3 = 跳过）。官方强调：
  - 用于 ranking 的图像“**并不代表即将发布的模型**”，而是刻意做得**平淡/无个性甚至偏差**，以帮助系统学习社区想要的方向、并“给垃圾图打标签”是流程中很重要的一环；
  - 这些评分“**很认真**”，被当作严肃的训练数据。
- **原生 2K 偏好采集**：因为此前的 rating party 从未在满 2K 分辨率下做过，官方专门发起 **High-res rating**（2026-04-27），让用户在“从零生成的 raw 2K 图像”上排序，以把模型调到**原生 HD/2K 层面就“漂亮”**（而非靠 upscale）。这条直接对应 V8.1/V8.2 的 HD 画质提升。
- **持续在线迭代**：V8.1 Updates（2026-04-30）明确“你们提供的评分数据正在持续帮助我们改进 **V8.2** 的质量”，说明偏好数据是跨版本持续喂入的在线闭环。
- **审美回调**：V8.1 相对 V8.0 的一个显式训练目标是“**找回 V7 风格的一致与熟悉审美**”，让 moodboard 与 sref 表现“超级稳定”；V8.1 Updates 又进一步“提升锐度与画质”（对 sref/moodboard 与 HD 最明显）。

**注意**：官方从未说明这套偏好数据具体是用作 reward model + RL（RLHF/DPO 等）还是仅用于数据筛选/再训练；扩散/flow/自回归等底层训练目标、蒸馏与步数加速方案（速度提升的来源）**均未披露**，不得编造。速度的工程化（“升级了 Web 界面来支撑这一速度”、“为 Relax 与更便宜的渲染做新服务器集群”）只见于产品层描述。

## Infra（训练 / 推理工程）
**训练算力 / GPU 时 / 并行策略 / 精度 / 吞吐均未披露。** 可考的只有**推理与计费侧**的产品事实（以 GPU 分钟与端到端时延衡量）：

- **端到端时延**（官方“默认模型”公告）：V8.1 **SD 约 4 秒出图、HD 约 12 秒**。
- **相对提速**：标准任务比旧版快约 **4–5 倍**（docs）；V8.0 alpha 已号称比此前快约 **5 倍**；V8.1 相对 V8.0，**HD 提速并降价约 3 倍**、**SD 提速 50% 且便宜 25%**。
- **GPU 时计费**（docs，按“GPU 分钟”计）：V8.1 **HD = 1.3 分钟 GPU 时**，**SD = 0.8 分钟 GPU 时**。
- **Draft 模式**（2026-06-16）：单次 draft 生成 **24 张**低分辨率/低质量图，整体只花 V8.1 SD 任务**一半的 fast hours**；点 “Vary” 再把选中图渲染成全质量全分辨率。
- **服务器集群 / 模式**：V8.0 alpha 初期 **Relax 模式尚不支持**，官方在建“新服务器集群”支持 Relax 与更便宜的渲染档；V8.1 上线后 Relax/Fast 可用、**Turbo 不可用**。V8.1 Updates 提到“为节省一次服务器迁移期间的算力，暂时把 SD 设为默认”。
- 早期 V8.0 alpha 的相对计费：`--hd`、`--q 4`、sref、Moodboard 任务约为常规任务的 4 倍慢、4 倍价；`--hd` 与 `--q 4` 同开为 16 倍——这些是 V8.0 内测期数据，V8.1 已大幅下调（HD 降为 1.3 分钟）。

底层是否做了步数蒸馏 / 缓存 / 量化以达成 4 秒出图，**官方未说明**。

## 评测 benchmark（把效果讲清楚）
**没有任何标准化学术 benchmark 数字。** Midjourney 不报告 FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore、GEdit/MagicBrush 等任何指标；也没有官方公布的 LMArena / Artificial Analysis 图像竞技场 ELO（小规模检索未找到针对 V8.1 的清晰一手榜单数据）。本页**不编造任何评测数字**。

官方给出的“效果”只能以**定性主张 + 产品级量化（速度/分辨率/计费）**呈现：

| 维度 | V7 | V8.1 | 来源 |
| --- | --- | --- | --- |
| SD 出图时延 | —（V8.1 SD≈V7 draft 速度） | ~4 秒 | 默认模型公告 |
| HD 出图时延 | 不支持原生 HD | ~12 秒 | 默认模型公告 |
| 原生分辨率 | 无原生 2K | 原生 2K（2048px），相对 V7 为 2×尺寸 / 4×分辨率 | 默认模型公告 / docs |
| 相对速度 | 基准 | 比旧版快 ~4–5× | docs |
| GPU 计费 | — | SD 0.8 分钟 / HD 1.3 分钟 | docs |
| 提示遵循 / 文本渲染 | 较 V6 强 | “更聪明、更连贯、更好遵循细节提示、文本渲染前所未有地好” | 默认模型公告 |
| sref/moodboard 稳定性 | 基准 | “super stable”，与 V7 风格一致 | V8.1 Alpha post |

其余如“锐度/画质提升”（V8.1 Updates，对 sref/moodboard 与 HD 最明显）均为官方主观描述，无量化对照。**严谨结论：V8.1 的“效果”在公开层面无法用学术指标量化，只能引用官方的相对速度/分辨率/计费数字与定性主张。**

## 创新点与影响
- **核心可考贡献**：(1) 把**原生 2K（HD）**做成常态能力并大幅降本提速（HD 1.3 分钟 GPU 时、约 12 秒），(2) **速度优先**的产品定位（SD 约 4 秒、相对旧版 4–5×），(3) **审美一致性回调**（V8.0→V8.1 找回 V7 风格、sref/moodboard 稳定），(4) 成体系的**社区成对审美偏好打分（Rating Party）闭环**，且专门在 2K 分辨率上重做 ranking 以提升“原生 HD 美感”。
- **影响**：作为头部闭源审美向 t2i 产品，V8.1 强化了“**人类审美偏好众包 → 持续在线对齐**”这一与开源学术路线（公开方法/权重/benchmark）截然不同的范式；其“draft（24 图低成本探索）→ vary（精修）”工作流也是产品化的探索-精修范式样本。
- **已知局限 / 缺口**：
  - **能力回退**：V8.1 下 **Character Reference 不支持**；**Omni Reference 回退用 V7**（V8 版仍在训练）；**Editor/Pan/Zoom Out 复用 V6.1**；**Upscaler 仅作用于 SD 图像**（非复用 V6.1）；不支持 Turbo、Multi-Prompting、`--niji`。
  - **HD 编辑降采样**：对 HD 图使用 inpaint/outpaint（Pan/Zoom/Vary Region）会**降采样回 SD**，需再 Upscale 才回到 HD。
  - **内测属性**：V8 系列长期标注“早期测试、可能无预告变动”；HD vs SD 默认随服务器迁移反复。
  - **披露缺口（本页确认未获取/未披露的维度）**：模型架构、训练目标与蒸馏方案、训练数据来源/规模/配比、训练算力/并行/精度、所有标准化 benchmark 与第三方 ELO——**Midjourney 官方一律未公开**。

## 原始链接
- blog (V8.1 Alpha, 2026-04-14, 最权威发布说明): https://updates.midjourney.com/v8-1-alpha/
- blog (V8.0 Alpha, 2026-03-17, 基座模型说明): https://updates.midjourney.com/v8-alpha/
- blog (V8.1 is now the default model, 2026-06-11, 速度/分辨率数字): https://updates.midjourney.com/v8-1-is-now-the-default-model/
- blog (V8.1 Updates, 2026-04-30, 画质提升 + V8.2 偏好数据): https://updates.midjourney.com/v8-1-updates/
- blog (Draft mode for V8.1 + --preview, 2026-06-16): https://updates.midjourney.com/draft-mode-for-v8-1-and-new-feature-previews/
- blog (V8 Rating Party, 2026-02-14, 成对偏好打分机制): https://updates.midjourney.com/v8-rating-party/
- blog (High-res rating, 2026-04-27, 原生 2K 偏好采集): https://updates.midjourney.com/high-res-rating/
- docs (Version, 含 V8.1 计费/分辨率/特性对照表): https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- project_page: https://www.midjourney.com

## 本地落盘文件
- ../../../sources/omni/2026/midjourney-v8-1--alpha-post.md
- ../../../sources/omni/2026/midjourney-v8-0--alpha-post.md
- ../../../sources/omni/2026/midjourney-v8-1--default-model.md
- ../../../sources/omni/2026/midjourney-v8-1--updates-apr30.md
- ../../../sources/omni/2026/midjourney-v8-1--draft-mode.md
- ../../../sources/omni/2026/midjourney-v8--rating-party.md
- ../../../sources/omni/2026/midjourney-v8-1--high-res-rating.md
- ../../../sources/omni/2026/midjourney-v8-1--version-docs.md
