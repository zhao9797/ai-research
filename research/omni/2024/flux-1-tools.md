---
title: "FLUX.1 Tools (Fill / Canny / Depth / Redux)"
org: "Black Forest Labs"
country: EU
date: "2024-11"
type: blog
category: edit
tags: [flux, inpainting, outpainting, controlnet, structural-conditioning, image-variation, mmdit, flow-matching, guidance-distillation, redux, siglip]
url: "https://blackforestlabs.ai/flux-1-tools/"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/black-forest-labs/flux"
hf_url: "https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev"
modelscope_url: ""
project_url: "https://bfl.ai/models/flux-tools"
downloaded: [flux-1-tools--blog.md, flux-1-tools--github-readme.md, flux-1-tools--docs-fill.md, flux-1-tools--docs-structural-conditioning.md, flux-1-tools--docs-image-variation.md, flux-1-tools--docs-text-to-image.md, flux-1-tools--diffusers-docs.md, flux-1-tools--src-image_embedders.py, flux-1-tools--src-sampling.py, flux-1-tools--src-util.py, flux-1-tools--src-cli-fill.py, flux-1-tools--src-cli-control.py, flux-1-tools--src-cli-redux.py]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
FLUX.1 Tools 是 Black Forest Labs 在 2024-11-21 围绕基座 [[flux-1]] 推出的**可控编辑套件**——Fill（inpainting/outpainting）、Canny/Depth（结构条件）、Redux（图像变体/重混）四件套，每件都同时以**开源 guidance-distilled `[dev]` 权重 + 闭源 `[pro]` API** 双轨发布；核心创新不在于新网络，而在于**用「通道拼接条件 + 在 MMDiT 上微调」一套统一范式，把 ControlNet/IP-Adapter 那一类外挂能力直接「内化」进 FLUX 主干**，官方 ELO 人评称 Fill [pro] 为彼时 inpainting SOTA、Depth [pro] 超过 Midjourney ReTexture。

## 背景与定位
2024 年下半年 FLUX.1（[dev]/[schnell]/[pro]）以 12B 参数的 [[mmdit]] 架构成为开源 T2I 第一梯队，但它本身只能做"文生图"。社区当时已经用外挂方式给 FLUX 加可控性——典型如 AlimamaCreative 的 FLUX-Controlnet-Inpainting、各种 IP-Adapter——但这些都是第三方、质量参差、且与主干解耦。FLUX.1 Tools 的定位就是由**模型作者亲自**给 FLUX 补齐四类最高频的可控编辑能力，并把它做到"开源即 SOTA"：

- **Fill** 对位 inpainting/outpainting（对标 Ideogram 2.0、社区 FLUX-Controlnet-Inpainting）。
- **Canny / Depth** 对位 [[controlnet]] 式结构条件（对标 Midjourney ReTexture）。
- **Redux** 对位 IP-Adapter 式的图像变体/重混（image variation / restyling）。

技术脉络上，它属于"在强基座 DiT 上用条件注入做编辑"这一路线（与 [[instructpix2pix]] 的指令编辑、ControlNet 的残差注入并列），但实现手段更"重"也更"干净"：不是加旁路网络，而是**改输入通道并直接微调主干**（Canny/Depth/Fill），或**加一个轻量投影 adapter 把图像 token 拼进文本序列**（Redux）。它是后续 [[flux-1-kontext]]（2025，in-context 统一编辑）的前身——Kontext 进一步把"参考图"也搬进 token 序列、统一成单一模型，而 Tools 仍是"一个能力一个权重"。

## 模型架构
基座沿用 FLUX.1 的 **MMDiT（双流 + 单流混合 Transformer）**：`hidden_size=3072`、`num_heads=24`、双流 block `depth=19`、单流 block `depth_single_blocks=38`、3D RoPE `axes_dim=[16,56,56]`、`theta=10000`、带 `guidance_embed`（即 guidance 蒸馏后用一个标量 embedding 注入 CFG 尺度）。文本条件走 **T5-XXL（`context_in_dim=4096`）+ CLIP pooled（`vec_in_dim=768`）**；图像走 **16 通道 VAE**（`z_channels=16`，`scale_factor=0.3611`，`shift_factor=0.1159`），latent 再做 2×2 patch packing，所以 DiT 的图像 token 维度是 `16×4=64`。以下数字均来自官方实现 `src/flux/util.py` / `sampling.py` / `modules/image_embedders.py`。

四个工具的注入方式是**两种范式**：

**1) Canny / Depth — 通道拼接 + 微调主干（in_channels 64→128）**
- 把条件图（canny 边缘图 / depth 图）当成一张普通图像，用**同一个 VAE 编码**成 latent，再 2×2 packing 成 64 通道；与噪声 latent 的 64 通道**沿通道维拼接**，得到 `in_channels=128`（`out_channels=64`）。
- Canny 边缘由 OpenCV `cv2.Canny`（阈值 `min_t=50, max_t=200`）现场抽取；Depth 由 **Depth-Anything-Large（`LiheYoung/depth-anything-large-hf`）**现场推理出深度图。即条件抽取器是**冻结的现成模型**，不在训练范围内。
- 这与 ControlNet 的本质区别：**没有旁路网络、没有 residual 注入**，而是直接把主干的输入卷积/线性层从 64 通道扩到 128 通道后**整体微调**（或用 LoRA 版只微调低秩增量）。diffusers 官方文档明确点出："Canny Control is *not* a ControlNetModel … an alternate architecture … by using channel-wise concatenation with input control condition"。
- 每类都发布**全量微调权重**与**FLUX.1 [dev] LoRA**两版（LoRA 需先下载 [dev] 基座）。

**2) Fill — 掩码图 + 二值掩码通道拼接（in_channels 64→384）**
- 输入三部分沿通道维拼接成 384：① 噪声 latent 64；② **被掩码遮挡的原图** `img_cond = img·(1−mask)` 经 VAE 编码 + 2×2 packing → 64；③ **二值掩码**先做 8×8 pixel-unshuffle（`b (h ph)(w pw)→b (ph pw) h w`, ph=pw=8）变成 64 通道再 2×2 packing → 64×4 = **256 通道**。即 64+64+256=384（`out_channels=64`）。这种"masked-image latent + 显式 mask 通道"的设计让模型既知道"保留区域内容"也知道"待生成区域几何"，outpainting 就是把 mask 设到画布外。

**3) Redux — SigLIP 图像 token 投影后拼进文本序列（不改 DiT 输入通道）**
- 用 **SigLIP-SO400M（`google/siglip-so400m-patch14-384`）** 视觉编码器取 `last_hidden_state`（dim=1152），过两层投影：`redux_up`（1152→4096×3=12288）→ SiLU → `redux_down`（12288→4096），得到与 T5 同维（4096）的图像 token。
- 推理时 `txt = cat(t5_text_tokens, redux_image_tokens, dim=序列维)`——图像 token 被当成"额外的文本 token"拼到 T5 序列后面，喂给**未改动的 FLUX 主干**。所以 Redux 是**纯 adapter**（只训练那两层投影 + SigLIP 可冻结），可挂在 [dev] 与 [schnell] 上；这也是它能即插即用、并被 FLUX1.1 [pro] Ultra 用作"restyling"后端的原因。

> 小结：Canny/Depth/Fill 走"扩输入通道 + 微调主干"，是**重微调**；Redux 走"投影 + token 拼接"，是**轻 adapter**。四者共享同一基座、同一 VAE、同一文本编码器。

## 数据
**未披露。** 官方博客与 GitHub/模型卡均未公布 FLUX.1 Tools 的训练数据来源、规模、配比、清洗/过滤、重描述（re-captioning）或合成数据细节。可确证的仅有方法层面的"数据构造逻辑"：
- Canny/Depth 的训练对必然是 (条件图=对原图抽取的 canny/depth, 目标图=原图, 文本=描述) 三元组——因为推理时正是用 `cv2.Canny` / Depth-Anything 现场抽取，训练抽取器与之一致是合理推断（注：这是基于推理实现的合理推断，训练细节官方未明示）。
- Fill 的训练对为 (原图, 随机二值掩码, 文本)，遮挡区由模型重建。
- Redux 的训练目标是让 SigLIP 图像 token 经投影后能驱动主干"重建/变体"输入图。
以上构造逻辑可从实现倒推，但**具体数据集、样本量、美学/安全过滤策略 BFL 未公开**，不作编造。

## 训练方法
- **训练目标**：继承 FLUX.1 的 **rectified flow / flow matching**（latent 空间的整流流匹配），非 DDPM 式 ε-预测。Tools 是在已训好的 FLUX.1 基座上**继续训练 / 微调**得到，而非从零训练。
- **Guidance 蒸馏**：所有开源 `[dev]` 变体都是 **guidance-distilled**（diffusers 文档明确标注 Fill/Canny/Depth-dev 为 "Guidance-distilled"，Redux 为 "Adapter"）。即把 classifier-free guidance 蒸馏进模型，使其无需跑两遍（cond/uncond）就能享受 CFG 效果，推理时 guidance 作为一个标量 embedding 注入（`guidance_embed=True`）。这是 [dev] 系"开源即高效"的关键。
- **微调粒度**：
  - Canny/Depth 提供**全量微调**与 **LoRA** 两档；LoRA 版只在 FLUX.1 [dev] 上加低秩增量，便于二次开发。
  - Fill 为全量微调（输入通道 64→384，必须改主干）。
  - Redux 只训练 `redux_up`/`redux_down` 两层投影（SigLIP 可冻结），是最轻的一档。
- **[pro] vs [dev]**：`[pro]` 为闭源、API-only、性能上限更高的版本；`[dev]` 是其 guidance-distilled 开源对应物。官方称 Fill [dev] 已"outperforming proprietary solutions while being more efficient at inference"。
- **关键推理超参（均为 [dev]，数值取自官方 `flux` 仓库 CLI 默认值，已落盘核对）**：
  - Fill（`cli_fill.py`）：`num_steps: int = 50`，`guidance: float = 30.0`。
  - Canny/Depth（`cli_control.py`）：`num_steps = 50`；guidance 默认按模型分支——canny/canny-lora `=30.0`，depth/depth-lora `=10.0`。
  - Redux（`cli_redux.py`）：`guidance = 2.5`；`num_steps = 4 if name=="flux-schnell" else 50`（即挂 [dev] 走 50 步、挂 [schnell] 走 4 步）。
  - （旁证：diffusers 文档示例 Canny `steps=50/guidance=30`、Redux `steps=50/guidance=2.5` 与上一致；但 diffusers Depth 示例用 `steps=30`，与 BFL CLI 的 50 不同——此处以 BFL 官方 CLI 默认值为准。）
- **蒸馏/加速**：除上述 guidance 蒸馏外，官方未披露步数蒸馏（如 LCM/ADD/Turbo）细节；Redux 可挂在 4 步的 [schnell] 上获得快速变体。

## Infra（训练 / 推理工程）
- **训练算力/GPU·时/并行策略：未披露。**
- **推理工程（已披露）**：
  - 官方 `flux` 仓库提供最小推理代码 + Streamlit/Gradio demo。
  - **TensorRT 加速**：官方提供 BF16 / **FP8 / FP4** 三档精度的 TRT 引擎导出（需用 NVIDIA PyTorch 镜像 + enroot 安装），并随后与 NVIDIA 合作推出 "Lightning-Fast FLUX"（Blackwell）进一步优化。ONNX 权重托管在 `FLUX.1-*-dev-onnx` 仓库。
  - **量化**：FP8/FP4 TRT 路径即面向消费级/数据中心 GPU 的低精度部署。
  - **部署形态**：① 开源权重（HF，本地/diffusers）；② BFL API（[pro]）；③ 第三方托管 fal.ai / Replicate / Together.ai / Freepik / krea.ai。
  - 商用需 BFL 月度授权，仓库内置 `--track_usage` 用量上报逻辑。

## 评测 benchmark（把效果讲清楚）
官方评测以**人评 ELO（人类偏好打分）**为主，原始对比 PDF 托管在 Google Drive（链接见下"原始链接"），博客只给出结论性 ELO 柱状图，**未公布 FID / CLIPScore / GenEval 等自动指标的数值**。已抓取一手源能确证的结论：

- **Fill（inpainting/outpainting）**：在自建 benchmark 上，**FLUX.1 Fill [pro] ELO 第一**，号称"the state-of-the-art inpainting model to date"，超过 Ideogram 2.0 与开源 FLUX-Controlnet-Inpainting；**Fill [dev] ELO 第二**，"outperforming proprietary solutions while being more efficient at inference"。（具体 ELO 数值博客未以文本给出，仅图示。）
- **Depth（结构条件，retexture）**：**FLUX.1 Depth [pro] 超过 Midjourney ReTexture**，且 [pro] 输出多样性更高；**Depth [dev]** 在 depth-aware 任务上结果更一致。
- **Canny**：**FLUX.1 Canny [pro] best-in-class**，**Canny [dev]** 次之。
- **Redux（image variation）**："achieves state-of-the-art performance in image variation"（ELO，图示）。
- **对比口径**：均为 BFL 自建评测集 + 内部/众包 ELO，对手覆盖 Ideogram 2.0、Midjourney ReTexture、社区 ControlNet-Inpainting 等同期方案。

> 诚实标注：**无任何公开的 FID/CLIP/GenEval/MJHQ/HPSv2/PickScore 等标准基准数值**——BFL 一贯只发 ELO 人评，博客正文只给结论文字与 ELO 柱状图（图片），具体 ELO 分数未以文本/表格给出。外链 Google Drive 的 benchmark "PDF" 实为约 400MB 的图像对比资源包（本次尝试下载确认其为图像 side-by-side 集，并非可抽取的 ELO 数据表，故未落盘）。源里没有的数字一律记为"未报告"，不编造。

## 创新点与影响
**核心贡献**
1. **把"外挂可控性"内化为"主干原生能力"的统一范式**：用最朴素的"VAE 编码条件图 + 沿通道维拼接 + 微调 MMDiT"取代 ControlNet 旁路网络（Canny/Depth/Fill），用"SigLIP 投影 token 拼进文本序列"取代 IP-Adapter（Redux）。证明在足够强的 DiT 基座上，**条件注入可以极简**而仍达 SOTA。
2. **开源 + 商用双轨且"开源即 SOTA"**：每个工具同时放出 guidance-distilled [dev] 权重（含 LoRA）与 [pro] API，[dev] 版本即超过若干闭源方案，极大降低社区做编辑应用的门槛。
3. **Fill 的"masked-image latent + 显式 256 通道 mask"设计**与 **Canny/Depth 的通道拼接式 control**，成为后续诸多 FLUX 衍生编辑工作的事实模板；Redux 的"图像 token 当文本 token"思路直接通向 [[flux-1-kontext]] 的 in-context 编辑。

**对后续工作的影响**：diffusers 等框架原生集成 `FluxFillPipeline` / `FluxControlPipeline` / Redux；社区围绕四件套衍生大量 LoRA/工作流（ComfyUI 等）。2025 年 BFL 用单一 in-context 模型 [[flux-1-kontext]] 统一了 Tools 的多数能力（编辑、参考图、保持一致性），可视为 Tools 范式的收敛升级。

**已知局限**
- 训练数据、算力、自动评测指标全部未披露，可复现性与"真实 SOTA 程度"难以独立核验。
- "一个能力一个权重"，Canny/Depth/Fill/Redux 不可单模型组合（需切换权重或叠 LoRA），不如后来的统一编辑模型灵活。
- Canny/Depth 依赖外部冻结抽取器（cv2.Canny / Depth-Anything），条件质量受其上限约束。
- 开源 [dev] 为非商用许可（FLUX.1-dev Non-Commercial License），商用需 BFL 授权。

## 原始链接
- blog（官方发布，2024-11-21，经 Wayback 存档）: https://blackforestlabs.ai/flux-1-tools/ （新站 404，存档 https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-1-tools/ ；产品页 https://bfl.ai/models/flux-tools ）
- github（官方推理代码 + 各工具 docs）: https://github.com/black-forest-labs/flux
- hf model（Fill，gated）: https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev
- hf model（Canny）: https://huggingface.co/black-forest-labs/FLUX.1-Canny-dev
- hf model（Depth）: https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev
- hf model（Canny/Depth LoRA）: https://huggingface.co/black-forest-labs/FLUX.1-Canny-dev-lora ; https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev-lora
- hf model（Redux）: https://huggingface.co/black-forest-labs/FLUX.1-Redux-dev
- diffusers 官方文档（独立佐证：channel-wise concat、guidance-distilled）: https://huggingface.co/docs/diffusers/main/en/api/pipelines/flux
- benchmark PDF（ELO，外链，未下载）: Fill https://drive.google.com/file/d/1y4CyrvBgy_QXRc7BllYTCyv0PnHb7xeX/view ; Depth https://drive.google.com/file/d/1DFfhOSrTlKfvBFLcD2vAALwwH4jSGdGk/view ; Canny https://drive.google.com/file/d/1dRoxOL-vy3tSAesyqBSJoUWsbkMwv3en/view ; Redux https://drive.google.com/file/d/1rqbyUjXqYatn2oMqkdjHCLfbsKMsjBla/view

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--blog.md) （官方发布博客，Wayback 存档全文）
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--github-readme.md) （flux 仓库 README，含模型表/许可/引用）
- [docs-fill.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--docs-fill.md) （Fill 用法/权重 sha256）
- [docs-structural-conditioning.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--docs-structural-conditioning.md) （Canny/Depth 用法 + TRT FP8/FP4）
- [docs-image-variation.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--docs-image-variation.md) （Redux 用法）
- [docs-text-to-image.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--docs-text-to-image.md) （基座 t2i 上下文）
- [diffusers-docs.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--diffusers-docs.md) （diffusers Flux 管线文档，独立佐证）
- [src-image_embedders.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--src-image_embedders.py) （Depth/Canny/Redux 编码器实现）
- [src-sampling.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--src-sampling.py) （prepare_fill/control/redux 条件构造）
- [src-util.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--src-util.py) （各变体 ModelSpec：in_channels 64/128/384 等）
- [src-cli-fill.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--src-cli-fill.py) （Fill CLI：`num_steps=50` / `guidance=30.0` 默认值出处）
- [src-cli-control.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--src-cli-control.py) （Canny/Depth CLI：guidance 按模型分支 canny=30 / depth=10、`num_steps=50`）
- [src-cli-redux.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/flux-1-tools--src-cli-redux.py) （Redux CLI：`guidance=2.5`、`num_steps = 4 if schnell else 50`）
