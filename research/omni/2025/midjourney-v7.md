---
title: "Midjourney V7"
org: Midjourney
country: US
date: "2025-04"
type: blog
category: t2i
tags: [t2i, closed-source, personalization, draft-mode, omni-reference, midjourney, aesthetics]
url: "https://www.midjourney.com/updates/v7-alpha"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version"
downloaded: [midjourney-v7--v7-alpha-blog.md, midjourney-v7--update-editor-exp.md, midjourney-v7--docs-version.md, midjourney-v7--docs-omni-reference.md, midjourney-v7--docs-draft-mode.md, midjourney-v7--docs-personalization.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Midjourney V7 是 Midjourney 第七代闭源文生图模型（2025-04-03 alpha、2025-06-17 成为默认），官方称"一个全新的模型"，最大产品创新是**默认开启个性化（personalization on by default）**、**Draft Mode（半价、约 10 倍速的草稿迭代/对话式生成）** 与 V7 专属的 **Omni Reference（角色/物体一致性参考）**；图像质量、文本理解、手/身体/物体一致性较 V6 显著提升。**模型架构、数据、训练方法、评测数字均未公开**——本页只呈现官方一手披露的内容，不臆造技术细节。

## 背景与定位
Midjourney 是商业闭源文生图产品的代表，自 V1 起按代际迭代（V5/V6/V6.1/V7/V8.1），通过 Discord 与官网 web 提供服务，**不发布论文、技术报告、模型权重或 benchmark**。V7 延续这一封闭策略：官方仅以**更新博客**与**帮助文档**披露能力与使用方式，从不公开 backbone、参数量、训练数据与定量指标。

V7 在产品脉络中的定位：
- **相对 V6/V6.1 的升级**：官方称 V7 是"一个全新的模型，有独特的优势（也可能有一些弱点），可能需要不同的 prompt 风格"——暗示它**不是在旧模型上微调，而是重新训练**，但官方未给出"from scratch / 全新架构"的明确技术声明，故此处只能按"entirely new model"的原话理解，不外推。
- **个性化范式转变**：V7 是**第一个默认开启模型个性化**的 Midjourney 模型。用户必须先"解锁"个性化档案（官方称约 5 分钟；在 Personalize 页的图片网格中点选喜欢的图，进度条满即解锁——**官方未给出具体张数**，仅说"选够足够多的图"且"选得越多越准"），之后所有生成都会偏向用户审美。可随时开关（`--p` 参数 / Imagine bar 按钮）。
- **与同期闭源 t2i 的关系**：处于 [[flux-1-1-pro]]、[[ideogram-3-0]]、[[imagen-4]]、[[reve-image]]、[[firefly-image-model-4]] 等 2025 年闭源/半闭源 t2i 的竞争带；Midjourney 的差异化在于**审美导向 + 个性化 + 强一致性参考**，而非可控编辑/排版能力。
- 与开源扩散/流匹配路线（[[ddpm]]、[[latent-diffusion-ldm]]、[[stable-diffusion-3]]、[[flux-1]]）相比，V7 不公开任何内部机制，无法对齐到具体的 DiT/MMDiT/flow-matching 技术谱系。

时间线（官方文档原文）：**2025-04-03 发布 V7 alpha**；2025-05-01 推出 V7 模型小更新 + 新版编辑器 + `--exp` 参数；随后上线 Omni Reference 与 Fast Mode；**2025-06-17 V7 成为默认版本**（V6.1 此前为默认）。

## 模型架构
**未披露。** Midjourney 从不公开 V7 的 backbone（U-Net / DiT / MMDiT / 自回归 / 掩码生成均未说明）、visual tokenizer / VAE、text encoder（是否用 T5 / CLIP / LLM 未知）、条件注入方式、参数量或多分辨率策略。

仅能从产品行为间接观察到的、与"架构层"相关的官方事实：
- 官方称 V7"更聪明地处理文本 prompt，图像 prompt 效果极佳"，"图像质量明显更高、纹理更漂亮，手/身体/各类物体的细节一致性显著更好"——指向更强的文本-图像对齐与细节连贯性，但**无任何机制说明**。
- **不再支持 Multi-Prompting（多 prompt `::` 权重）**（V6 支持，V7/V8.1 取消，见官方兼容性表），可能暗示 V7 的条件注入/文本编码方式与 V6 不同，但官方未解释原因——此处仅记录现象，不外推架构结论。
- **Character Reference（`--cref`）在 V7 不支持**，由 V7 专属的 **Omni Reference（`--oref`）** 替代；后者声称能把参考图中的人物/物体/车辆/非人生物放进新图，可见 V7 在"参考图条件注入"上做了重做，但实现细节（IP-Adapter 类 / 重训练 cross-attention / 其他）未披露。
- **Seed 行为**：V7 支持 `--seed`；官方称跨版本重跑旧 seed"可能保持一致但更好"。

> 严格说明：以上均为产品行为层观察，**不能据此声称 V7 用了某种具体架构**。

## 数据
**完全未披露。** 官方从未公开 V7 的训练数据来源、规模、图文对数量、配比、清洗/过滤流程、re-captioning 方案或合成数据使用。Midjourney 历来不公布数据集信息（且其训练数据来源在业界与多起版权诉讼中存在争议，但官方对 V7 无任何数据披露）。美学/安全过滤方面，官方仅在 Omni Reference 文档中提到"内容审核（moderation）会拦截看似无害的 prompt，被拦的 job 不扣费，只有出图才扣 GPU time"——属于**推理侧的内容安全过滤**，非训练数据披露。

## 训练方法
**完全未披露。** 训练目标（diffusion / flow matching / rectified flow / next-token / masked-token）、多阶段流程（预训练→continue→SFT→偏好对齐）、是否使用 RLHF/DPO/reward model、蒸馏与步数加速方案（consistency/LCM/ADD 等）均无官方说明。

可确证的、与"训练/对齐"间接相关的官方信息：
- **预发布"评级派对（pre-release rating party）"**：V7 alpha 博客明确感谢社区参与"V7 pre-release rating party"。Midjourney 历来用大规模社区图片偏好评分（ranking pairs）来构建审美偏好信号；V7 同样依赖这种**人类偏好数据**，但官方未说明它如何进入训练（是否用于 reward model / 偏好对齐 / 数据筛选均未明）。
- **个性化（Personalization）**：用户在 Personalize 页的图片网格里点选喜欢的图（进度条满即解锁，官方未给具体张数），生成一个个性化"profile"（`--p`），V7 默认应用它。官方把它描述为"风格助手"——这是**推理时的偏好条件**（per-user style steering），不是模型本体的训练改动，官方未把它描述为训练流程的一部分。
- **2025-05-01 的"V7 模型更新"**：官方称所有 `--v 7` 图像"质量、prompt 准确度、手部准确度、身体一致性都略有提升"，且"无需改动任何东西"。说明 V7 在 alpha 期后有过**模型层面的在线迭代/替换**，但未说明是重训练、continue-train 还是后处理改动。

## Infra（训练 / 推理工程）
**训练 infra 完全未披露**（GPU 规模、并行、精度、吞吐均无）。

推理/服务侧可量化的官方事实（按 GPU time 计费，单位"分钟"）：
- **运行模式**：V7 launch 时仅开放 **Turbo** 与 **Relax** 两种模式；标准 speed 模式"需要更多时间优化"延后上线。官方称 **Turbo job 比普通 V6 job 贵 2 倍**。
- **Draft Mode（V7）**：生成 4 张图，**GPU 成本为标准 V7 的一半**；官方在博客中称"半价、约 10 倍速渲染"。Draft 图质量低于标准模式但"行为与审美非常一致"，可作为可信的迭代方式；点 "Enhance" 可用标准质量重渲染相似结果，喜欢的草稿也可直接 upscale。
  - 对比 V8.1 的 Draft（一次出 24 张、512×512、每 prompt 0.4 分钟 GPU），**V7 的 Draft 是 4 张**——两代 Draft 机制不同。
- **Omni Reference（V7）**：比常规 V7 图**多花 2 倍 GPU time**；不兼容 Fast Mode、Draft/Conversational Mode、`--q 4`，也不兼容 inpainting/outpainting（这些仍走 V6.1）。
- **Quality 参数**：V7 支持 `--q 1 / 2 / 4`（V6 是 0.5 / 1 / 2），更高质量档对应更多算力。
- **`--exp` 参数（2025-05 上线）**：实验性"图像美学增强"参数，0–100（默认 0），与 `--stylize` 类似但更细节、更动态、更"tone mapped"；官方建议用 5/10/25/50/100，提示高值会牺牲 prompt 准确度与多样性。
- **回退到 V6/V6.1 的功能**：Upscaling、Editor、Retexture、Pan、Zoom Out、Vary Region 在 V7 期间**仍由 V6 / V6.1 模型处理**（官方兼容表明确标注 "Using V6.1"）——说明 V7 launch 时是"核心 t2i + Omni Reference 用 V7，编辑/放大类用旧模型"的拼接形态。
- **分辨率**：V7 **不支持 HD（2048px）图像**（该能力到 V8.1 才有）；最大宽高比 14:1（与 V6 相同）。
- **部署形态**：Discord bot + midjourney.com web 应用；Draft/Conversational/Voice mode 主要在 web 上。

## 评测 benchmark（把效果讲清楚）
**官方未报告任何定量指标。** Midjourney 不公布 FID、CLIPScore、GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore 或人评 ELO/Arena 等任何数字。V7 页面、更新博客与帮助文档中**没有一条 benchmark 数据**。

官方仅有的"效果"描述均为定性原话：
- V7 alpha 博客："much smarter with text prompts；image prompts look fantastic；image quality is noticeably higher with beautiful textures；bodies, hands and objects … significantly better coherence on all details"。
- 2025-05 更新："slightly improved image quality, prompt accuracy, hand accuracy, and body coherence"。
- 文档总结："text and image prompts are handled with stunning precision；richer textures and more coherent details—especially in bodies, hands, and objects"。

> 注：第三方榜单（如 LMArena Text-to-Image / Artificial Analysis Image Arena）在 V7 期间有过 Midjourney 的对局排名，但那不是 Midjourney 官方一手披露，本页不引用未抓取/非一手的数字。**官方源里没有任何可抠的 benchmark 数字——记为"未报告"。**

## 创新点与影响
**核心贡献（产品/体验层，非可验证的技术贡献）：**
1. **默认个性化（personalization by default）**：首个把"模型个性化"设为默认开关的 Midjourney 模型，把"per-user 审美偏好"从可选功能变成生成的默认条件，推动了"个性化生成"作为产品默认形态的行业话语。
2. **Draft Mode + Conversational/Voice Mode**：以半价、约 10 倍速的草稿出图 + 自然语言/语音对话改 prompt，把 t2i 从"写好 prompt 再生成"变成"边对话边迭代"的交互范式；这一草稿-迭代-增强（draft→enhance/vary→upscale）的工作流被后续 V8.1 继承并放大（24 张草稿）。
3. **Omni Reference**：把 V6 的 Character Reference 升级为可放入"人物/物体/车辆/非人生物"的统一参考，并提供 `--ow`（1–1000，默认 100）连续权重控制，强化了"主体一致性"这一闭源 t2i 的关键卖点。

**对后续工作的影响：** V7 的个性化默认、Draft/对话式迭代与 Omni Reference 直接被 V8.1 继承演进；它强化了"审美 + 一致性 + 个性化"作为 Midjourney 与其他 t2i（[[flux-1-1-pro]]、[[ideogram-3-0]]、[[imagen-4]]）差异化的产品轴线。

**已知局限（官方明示）：**
- launch 时**无标准 speed 模式**（仅 Turbo/Relax），Turbo 比 V6 普通 job 贵 2 倍。
- **编辑/放大/Pan/Zoom/Retexture/inpaint/outpaint 仍回退到 V6/V6.1**，V7 launch 时并非全功能闭环。
- **取消 Multi-Prompting 与 Character Reference**（cref）；**不支持 HD 2048px**。
- 官方坦承 V7 是"全新模型，有独特优势也可能有弱点，可能需要不同 prompt 风格"。
- **透明度局限（本页最大 gap）**：架构、数据、训练、infra、benchmark 全部闭源未披露，无法做任何机制级或定量级分析；本页所有内容均来自官方博客 + 帮助文档的产品层描述。

## 原始链接
- blog（V7 alpha 发布，2025-04-04 announcement）: https://www.midjourney.com/updates/v7-alpha
- blog（V7 模型更新 + 编辑器 + `--exp`，2025-05-01）: https://www.midjourney.com/updates/v7-update-editor-and-exp
- docs（Version 总览 + V6/V7/V8.1 功能兼容表 + V7 发布/默认日期）: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
- docs（Omni Reference，V7 专属一致性参考 + `--oref`/`--ow`）: https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference
- docs（Draft & Conversational Modes，V7 草稿/对话/语音模式）: https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes
- docs（Personalization，V7 默认个性化 `--p` 解锁/机制）: https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization

## 一手源存档（sources/）
- [v7-alpha-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/midjourney-v7--v7-alpha-blog.md)
- [update-editor-exp.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/midjourney-v7--update-editor-exp.md)
- [docs-version.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/midjourney-v7--docs-version.md)
- [docs-omni-reference.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/midjourney-v7--docs-omni-reference.md)
- [docs-draft-mode.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/midjourney-v7--docs-draft-mode.md)
- [docs-personalization.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/midjourney-v7--docs-personalization.md)
