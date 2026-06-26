---
title: "FLUX.1 Krea [dev]"
org: "Black Forest Labs / Krea"
country: EU
date: "2025-07"
type: blog
category: t2i
tags: [text-to-image, rectified-flow, dit, flux, post-training, rlhf, dpo, aesthetics, photorealism, guidance-distillation, open-weights]
url: "https://www.krea.ai/blog/flux-krea-open-source-release"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/krea-ai/flux-krea"
hf_url: "https://huggingface.co/black-forest-labs/FLUX.1-Krea-dev"
modelscope_url: ""
project_url: "https://bfl.ai/announcements/flux-1-krea-dev"
downloaded: [flux-1-krea-dev--bfl-blog.md, flux-1-krea-dev--krea-blog.md, flux-1-krea-dev--github-readme.md, flux-1-krea-dev--hf-modelcard-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
FLUX.1 Krea [dev] 是 Black Forest Labs（BFL）与应用型 AI 公司 Krea 合作、2025-07-31 发布的开放权重文生图模型，是商用产品 Krea 1 的 guidance-distilled 开源版本；它的核心命题不是刷 benchmark，而是**用一套"opinionated"（有主见的）后训练流程系统性消除文生图的"AI 塑料感"（AI look）**——去掉过饱和纹理、蜡质皮肤、虚化背景、千篇一律的构图，换取摄影级真实感与美学多样性。最亮眼的结果是：在人类偏好评测中**与闭源的 FLUX1.1 [pro] 持平**，同时全程与 FLUX.1 [dev] 架构/生态完全兼容（drop-in 替换）。

## 背景与定位
作者团队提出一个 Goodhart 式的核心论点："当一个度量变成目标，它就不再是好度量"。过去几年文生图社区把精力放在"模型有多聪明"（能否让宇航员骑马、酒杯倒满、正确渲染文字），并用 [[fid]]、CLIPScore、GenEval、T2I-CompBench、DPG、GenAI-Bench 等 benchmark 把这些能力量化。但在这种"benchmark 优化"的追逐中，早期模型（如 DALLE-2）那种"凌乱但真实、风格多样、有创意"的气质反而退化了——这就是被称为 **"AI look"** 的现象（团队引用 arXiv:2506.15742）。

团队进一步指出**美学评分器本身有偏**：LAION-Aesthetics（业界常用来筛高质量训练图）被发现强烈偏向"女性主体 + 虚化背景 + 过软纹理 + 高亮图像"；PickScore / ImageReward / HPSv2 多为 [[clip]] 微调变体，只能处理 224×224 低分辨率、参数量有限，已跟不上当代生成模型的能力。**用这些评分器去 cherry-pick 训练数据，会把隐式偏见灌进模型先验。** 因此 Krea 的目标朴素而明确："Make AI images that don't look AI"，并据此设计整条后训练管线。

在 BFL 的 FLUX 家族谱系里，本模型属于 [[flux-1]] 生态的一个**美学特化分支**：它不改 backbone、不破坏 LoRA/ControlNet 兼容性，而是把"美学方向"作为后训练目标，证明了"基础模型实验室 + 应用型 AI 实验室"协作开发的价值（BFL 出 raw base，Krea 出美学后训练）。

## 模型架构
- **Backbone**：12B 参数的 **rectified-flow（整流流）扩散 transformer**（HF model card / GitHub 原文用词为 "rectified flow transformer"；MMDiT 是 FLUX.1 体系的常识性架构判断，本次四个一手源未明写"MMDiT"字样），与 [[flux-1]] [dev] 架构**完全一致**——HF model card 明确表示可作为任何支持 FLUX.1 [dev] 系统的"drop-in replacement"，pipeline（diffusers 的 `FluxPipeline` / ComfyUI）全部沿用。
- **Guidance distillation（引导蒸馏）**：与 FLUX.1 [dev] 同源，模型是 **CFG-distilled** 的——把 classifier-free guidance 蒸进单次前向，从而推理时无需跑两路（cond/uncond）即可获得引导效果，更高效。BFL 提供给 Krea 的起点 base（`flux-dev-raw`）本身就是"pre-trained + guidance-distilled 的 12B DiT"。
- **文本编码器 / VAE / tokenizer**：本次四个一手源（BFL 博客 / Krea 博客 / GitHub README / HF model card）**均未披露**这些子模块的具体构成或任何改动；因模型自称与 FLUX.1 [dev] 架构完全兼容、可 drop-in 替换，合理推断其继承 FLUX.1 [dev] 的同一套文本编码器 / VAE（FLUX.1 公开资料中为 T5 + CLIP 双文本编码器、潜空间 VAE，但此细节来自 FLUX.1 体系而非本次发布的一手源）。
- **参数量**：12B（与 FLUX.1 [dev] 同级）；权重约 22GB（HF 单文件 `flux1-krea-dev.safetensors`）。
- **分辨率策略**：官方推荐生成分辨率在 **1024–1280 像素**之间；diffusers 示例默认 1024×1024。

关键点：本模型的"创新"几乎不在架构层，而在**保持架构冻结的前提下，把美学/真实感作为后训练优化对象**——这是它与"换 backbone 刷分"路线最大的分野。

## 数据
官方按训练阶段分层披露（数字层面较克制，但方法描述详细）：

- **预训练数据（由 BFL 负责，产出 `flux-dev-raw`）**：团队主张预训练应追求 **"mode coverage / 世界理解"**，最大化多样性——风格、物体、地点、人物全覆盖。一个反直觉但被强调的观点：**预训练甚至应该见过"坏数据"**，只要这些不良属性被准确写进 conditioning。原因是负面提示（"too many fingers, deformed faces, blurry, oversaturated"）要生效，模型必须先见过这些"坏图"长什么样，否则负向引导无从着力。
- **SFT 数据（Krea 手工策展）**：手工精选**符合 Krea 美学标准的最高质量图像**。关键做法是**混入 Krea 1 的高质量合成样本**——团队发现合成图有助于**稳定 checkpoint 性能**。
- **偏好数据（RLHF 阶段）**：使用经过严格过滤的**内部高质量偏好数据**。标注者被要求"清楚当前模型的局限/改进点/强弱项"，且偏好标注界面里特意放入**多样化的图像集合**以获得聚焦的标注。
- **数据规模 / "少即是多"**：团队明确给出后训练数据量级——**< 1M（百万级以下）即可做好后训练**；数量主要帮助稳定性与去偏，但**质量远比数量重要**（呼应 LIMA 等"小而精"文献，引用 arXiv:2305.11206 / 2309.15807 / 2505.19297）。
- **安全过滤（model card 披露）**：(1) 预训练阶段 BFL 过滤多类 NSFW / 违法内容；(2) 后训练阶段 BFL 与 **Internet Watch Foundation（IWF）** 合作过滤已知 CSAM，并经多轮定向微调抑制 CSAM/NCII 生成；(3) 发布前做了内部 + 第三方对抗评测。
- **未披露**：训练图像总量、图文对数量、各域配比、re-captioning 具体做法、美学评分阈值等均未给出量化数字。

## 训练方法
整条管线的精神是 Michelangelo 式的——**"雕塑已在大理石中，我只是凿去多余部分"**：预训练负责"模式覆盖"，后训练负责"模式坍缩（mode collapse）"，即主动把分布偏向团队认为好看的那部分。

1. **从 raw base 起步**：刻意要一个**"未烘焙（not baked）"的 base**。团队批评现有开源模型大多已被重度微调/后训练（"too baked"），分布僵化、难以重塑，且已经带上了"AI 美学"。因此与 BFL 合作拿到 **`flux-dev-raw`**——一个 pre-trained + guidance-distilled 的 12B DiT。它本身质量远不及 SOTA，但具备三大优点：① 世界知识丰富（物体/动物/人/相机角度/介质）；② 已能生成连贯结构、基础构图、可渲染文字；③ **未被"烘焙"**，输出分布极其多样（从粗糙到惊艳都有），是理想的可塑画布。
2. **SFT（监督微调）**：在手工策展 + Krea 1 合成样本上微调。**关键工程难点**：因为 `flux-dev-raw` 是 **guidance-distilled** 模型，团队设计了一个**自定义损失，直接在 classifier-free-guided（CFG）分布上微调模型**（引用 CFG arXiv:2207.12598）。SFT 后图像质量显著提升，但还不够"对味"。
3. **RLHF / 偏好对齐**：采用一种自研的偏好优化变体，团队称之为 **TPO**（"a variant of preference optimization technique which we call TPO"，属 DPO 系思路，论文未单独发布）。用严格过滤的内部偏好数据，**多轮偏好优化**逐步校准输出。
4. **"opinionated（有主见）"的核心方法论**——这是全文最重要的方法贡献：
   - 团队实验发现，**在公开偏好数据集（PickScore/ImageReward/HF image-preferences 等）上训练会引入退化**：偏向对称/简单构图、模糊过软纹理、**色板坍缩（color palette collapse）**、整体回归"AI look"。
   - 论点：对**有客观真值**的目标（文字渲染、解剖结构、prompt 一致性），数据多样性与规模有益；但对**主观美学**目标，把不同审美口味混在一起几乎是"adversarial（相互对抗）"的——会得到一个让所有人都不满意的"边际偏好分布"（高时尚摄影爱好者 vs 极简插画爱好者，平均之后两边都不爽）。
   - 结论：**故意"过拟合"到一种明确的艺术方向**，按团队自己的审美口味、聚焦地采集偏好数据，比追求"全局用户偏好"更优。这就是"opinionated"一词的由来，也是它区别于其他后训练模型的本质。
5. **蒸馏为开源版**：发布的 FLUX.1 Krea [dev] 是从产品级 **Krea 1** 蒸馏而来的 **guidance/CFG-distilled** checkpoint，目标是"在保留美学与真实感的前提下匹配 Krea 1 的质量"，并保持与 FLUX.1 [dev] 的全兼容。
- **未披露**：TPO 的精确目标函数、轮数、学习率/超参、奖励模型细节、蒸馏的具体配方（步数蒸馏/一致性蒸馏等）均未公开。

## Infra（训练 / 推理工程）
- **训练 infra**：未披露算力规模、GPU·时、并行/分布式策略、混合精度等具体数字；致谢中提到依赖 Krea 的数据/基础设施/产品团队搭建的后训练管线，但无量化信息。
- **推理工程（官方推荐设置，来自 GitHub README）**：
  - 分辨率：**1024–1280** 像素之间；
  - 采样步数：**28–32 步**；
  - **CFG guidance：3.5–5.0**（diffusers 示例用 `guidance_scale=4.5`）。
  - 因是 guidance-distilled 模型，推理时单路前向即可获得引导效果，相对未蒸馏 CFG（双路）更省算力。
- **部署形态**：开放权重，22GB 单 safetensors；官方/社区支持 diffusers `FluxPipeline`、ComfyUI、Draw Things、DiffusionBee；多家云厂商（FAL、Replicate、Runware、DataCrunch、TogetherAI）提供 API 端点。diffusers 可用 `enable_model_cpu_offload()` 降显存。

## 评测 benchmark（把效果讲清楚）
**重要诚实声明**：本次发布**没有给出任何文本化的量化 benchmark 数字**（FID / GenEval / DPG / PickScore / HPSv2 等一概未在博客或 model card 中列出表格数值）。这与该工作的核心立场一致——团队明确认为现有自动 benchmark 与美学评分器对"AI look"问题是**误导性/不充分**的，因此刻意不以这些指标作为卖点。可核实的结论如下：

- **人类偏好（核心结论）**：BFL 官方称 FLUX.1 Krea [dev] **超越此前的开放权重文生图模型**，并在**人类偏好评估中与闭源的 FLUX1.1 [pro] 持平**（"on par with closed solutions like FLUX1.1 [pro] in human preference assessments"）。BFL 博客配有一张人类偏好对比图（图像形式，未给出具体 ELO/胜率数字）。
- **质量定性**：主打"摄影级真实感 + 独特美学 + 去过饱和纹理"，强调风格多样性与"pleasant surprises"。
- **安全评测（model card）**：第三方对抗评测聚焦"纯文本 prompt 诱发 CSAM/NCII"的鲁棒性；官方称最终发布的 checkpoint **对违规输入展现出很高的抵抗力，且高于其他同类开放权重模型**（同样未给数字表）。
- **消融性结论（方法层面，非数字）**：① 在公开偏好集上训练 → 引发构图对称化、纹理过软、色板坍缩、回归 AI look；② 混入 Krea 1 合成样本 → 稳定 SFT；③ < 1M 数据即可，质量 > 数量。

> 因此本页"benchmark"维度以**未报告具体数字**为准，仅有 BFL 的"与 FLUX1.1 [pro] 人类偏好持平"这一可核实定性结论。**未编造任何分数。**

## 创新点与影响
**核心贡献**
1. **系统性地把"AI look"问题工程化**：把"去塑料感/去过饱和/恢复美学多样性"从模糊抱怨变成一条可执行的后训练方法论（raw base → SFT → 多轮偏好优化）。
2. **"Opinionated 美学对齐"范式**：论证主观美学**不应**用全局/平均偏好对齐，而应**故意过拟合到一种明确艺术方向**；指出公开偏好集会导致色板坍缩等退化——这是对主流 RLHF-for-aesthetics 实践的有价值的反思。
3. **"raw / 未烘焙 base"的价值主张**：明确区分"baked"与"raw"基础模型，并通过 BFL 提供的 `flux-dev-raw` 验证了"可塑性 > 现成质量"对后训练的重要性。
4. **guidance-distilled 模型上的自定义 CFG-分布微调损失**：解决了"在已蒸掉 CFG 的模型上继续后训练"的实操问题。
5. **少数据后训练的实证**：< 1M 高质量数据即可显著改变美学，呼应 LIMA 类"小而精"结论。
6. **生态兼容的开源交付**：12B、drop-in 替换 FLUX.1 [dev]，LoRA/ControlNet/ComfyUI 生态零迁移成本，降低社区在"真实感美学"方向二次开发的门槛。

**影响**：作为 2025 年中开放权重 t2i 的重要节点，它把社区注意力从"prompt-following 刷分"重新拉回"图像气质/真实感"；"opinionated 后训练"成为后续美学特化与个性化（personalization）工作的参照。团队在后记中预告下一步走向**个性化 + 可控性**（让模型贴合每个用户的审美），并随后推出了 Krea 1 系列后续模型与实时视频（Krea Realtime 14B）等工作。

**已知局限（官方 + 推断）**
- 不提供事实性信息，可能放大社会偏见，prompt-following 受提示风格影响大（model card 明示）。
- "opinionated/过拟合"是双刃剑：默认美学很强，但若用户审美与团队不一致，仍需 prompt 或 LoRA 调整（团队自承 prompting 不足以覆盖所有风格）。
- 非商用许可（FLUX.1 [dev] Non-Commercial License），商用需另购 BFL 授权。
- 关键工程细节（TPO 目标函数、训练算力、数据量化配比、蒸馏配方）均未公开，复现门槛高。

## 原始链接
- blog (BFL 官方公告): https://bfl.ai/announcements/flux-1-krea-dev
- blog (Krea 技术报告，最深一手源): https://www.krea.ai/blog/flux-krea-open-source-release
- github (官方推理仓库): https://github.com/krea-ai/flux-krea
- hf (模型卡 + 权重): https://huggingface.co/black-forest-labs/FLUX.1-Krea-dev
- 引用："AI look" 论文: https://arxiv.org/abs/2506.15742 ；guidance distillation: https://arxiv.org/abs/2210.03142 ；CFG: https://arxiv.org/abs/2207.12598

## 一手源存档（sources/）
- [bfl-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/flux-1-krea-dev--bfl-blog.md)
- [krea-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/flux-1-krea-dev--krea-blog.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/flux-1-krea-dev--github-readme.md)
- [hf-modelcard-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/flux-1-krea-dev--hf-modelcard-page.md)
