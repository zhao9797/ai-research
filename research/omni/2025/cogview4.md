---
title: "CogView4-6B"
org: "智谱 AI / 清华大学 KEG"
country: China
date: "2025-03"
type: model-card
category: t2i
tags: [t2i, dit, mmdit, flow-matching, glm, bilingual, chinese-text-rendering, open-source]
url: "https://github.com/THUDM/CogView4"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/THUDM/CogView4"
hf_url: "https://huggingface.co/THUDM/CogView4-6B"
modelscope_url: "https://modelscope.cn/models/ZhipuAI/CogView4-6B"
project_url: "https://docs.bigmodel.cn/cn/guide/models/image-generation/cogview-4"
downloaded: [cogview4--github-readme.md, cogview4--github-readme-zh.md, cogview4--hf-modelcard.md, cogview4--transformer-config.json, cogview4--vae-config.json, cogview4--scheduler-config.json, cogview4--model_index.json, cogview4--diffusers-transformer.py, cogview4--bigmodel-docs.md, arxiv-2403.05121.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CogView4-6B 是智谱 2025-03 开源的 6B 参数文生图 DiT，最大创新是把文本编码器从纯英文 T5-XXL 换成**双语 GLM-4-9B（4096 维、1024 token）**并用 MMDiT 式联合注意力 + flow matching 训练，成为**首个能在画面中渲染汉字的开源文生图模型**，原生支持中英双语、任意分辨率（512–2048、面积 ≤2²¹），发布时在 **DPG-Bench 综合 85.13 拿下开源 SOTA**。

## 背景与定位
此前主流开源文生图（SDXL、SD3、Flux）几乎都用英文 text encoder（CLIP / T5），中文需翻译且无法渲染汉字；少数中文模型（如 Kolors）字符准确率也很低（README 评测 Kolors F1 仅 0.288）。CogView4 在 [[ddpm]]→[[latent-diffusion-ldm]]→DiT/MMDiT（[[stable-diffusion-3]]、[[flux-1]]）的脉络上，做了两件事：(1) 用 GLM-4-9B 这种解码器式双语 LLM 当文本编码器，吃透中文语义并能把汉字字形写进画面；(2) 采用「任意长度 caption × 任意分辨率」混合训练范式，统一了多分辨率与原生中文。

它直接接续智谱自家的 [[cogview3]]（2024，3B、级联/接力扩散 relay diffusion、UNet + T5-XXL）与 CogView3-Plus-3B（DiT + T5-XXL）。**注意 CogView4 与 CogView3 是不同架构**：CogView3 是两段式 relay diffusion 的 UNet，CogView4 是单段式 MMDiT。官方未单独发布 CogView4 技术报告，README/模型卡仅引用 CogView3 论文（arXiv:2403.05121），架构细节须从 README、diffusers 参考实现与 HF config 还原。

## 模型架构
**Backbone：MMDiT 式 Diffusion Transformer（非 relay、非 UNet）。** 由 diffusers `CogView4Transformer2DModel` 与 HF `transformer/config.json` 还原的确切规格：

- 层数 `num_layers=28`，注意力头 `num_attention_heads=32`，`attention_head_dim=128` → **隐藏维 inner_dim = 32×128 = 4096**。
- Patchify：`patch_size=2`，`CogView4PatchEmbed` 把 `in_channels(16)×2×2` 线性投影到隐藏维；输出通道 16。
- **联合注意力（MMDiT/SD3 风格）**：每个 `CogView4TransformerBlock` 里，文本 token 与图像 token **拼接**（`torch.cat([encoder_hidden_states, hidden_states], dim=1)`）后做一次共享自注意力，两个模态各有**独立的 AdaLN 归一化与门控参数**（`norm_context`、`norm2_context`、独立门控 `c_gate_msa/c_gate_mlp`）；注意前馈网络 `self.ff` 在两模态间**共享权重**（源码中图像/文本两支均调用同一 `self.ff`），并非 SD3 那样每模态独立 FFN。文本侧用 `text_proj` 把 4096 维 GLM 表征投影进序列；RoPE 只施加于图像/latent 流（`query[:, :, text_seq_length:, :]`），文本 token 不加位置编码。
- **条件注入**：时间步 + 分辨率经 `CogView4AdaLayerNormZero`（AdaLN-Zero）注入；`condition_dim=256`，`pooled_projection_dim = 3×2×condition_dim`，即把 (原始尺寸 / 目标尺寸 / 裁剪坐标) 各自做 sincos 嵌入（SDXL 式 micro-conditioning），支撑「任意分辨率」。
- **位置编码：2D RoPE**（`CogView4RotaryPosEmbed`，`rope_axes_dim=(256,256)`，theta=1e4），按 patch 后的 H/W 网格生成，天然适配可变分辨率/长宽比；注意力含 **QK-LayerNorm**（`qk_norm="layer_norm"`）稳训。

**文本编码器：GLM-4-9B**（HF `THUDM/glm-4-9b-hf`，pipeline 里类名 `GlmModel`），输出维 `text_embed_dim=4096`，提示词上限 **1024 token**（CogView3-Plus 为 T5-XXL、224 token）。这是 CogView4 与同类开源模型最本质的差异。

**VAE：`AutoencoderKL`，16 通道潜空间**（`latent_channels=16`，`block_out_channels=[128,512,1024,1024]`，4 个下采样块 → **8× 空间压缩**，无 quant/post-quant conv），与 SD3/Flux 同代的 16-ch VAE 一脉。

**分辨率策略**：H、W ∈ [512,2048]，需被 32 整除，且 H×W ≤ 2²¹（约 209 万像素）；推理仅支持 BF16/FP32（FP16 会溢出出全黑图）。

## 数据
官方未发布 CogView4 专门的数据技术报告，仅在 bigmodel.cn 产品页与 README 披露要点：
- **中英双语图文训练**：明确「将文本编码器从纯英文 T5 换为双语 GLM-4 encoder，并通过中英双语图文进行训练」，使模型具备双语提示词能力与汉字渲染。
- **任意长度 caption × 任意分辨率混合训练范式**：官方称「实现了任意长度的文本描述（caption）和任意分辨率图像的混合训练范式」，既让创作更自由，也「提升了训练效率」。
- **长合成描述（re-caption）**：README 明确「CogView4 系列模型都是通过长篇合成图像描述进行训练的」，因此强烈建议推理前用 LLM（glm-4-plus）重写/扩写提示词以对齐训练分布。这一 re-caption 方法承自 [[cogview3]]：CogView3 论文披露用 GPT-4V 自动产 <image, old_cap, new_cap> 三元组约 7 万条、微调 CogVLM-17B 得 re-caption 模型，再对全量数据重写，并把 **95% 原始 caption 替换为合成 caption**（base 数据源为 LAION-2B 并过滤政治敏感/色情/暴力）。CogView4 具体数据规模、配比、来源、美学/安全过滤细节**未披露**。

## 训练方法
- **训练目标：Flow Matching / Rectified Flow。** 由 `scheduler/scheduler_config.json` 确证为 `FlowMatchEulerDiscreteScheduler`，`num_train_timesteps=1000`。与 CogView3 的 DDPM/relay-diffusion 目标不同，CogView4 走的是 SD3/Flux 同代的 rectified-flow 路线。
- **动态分辨率时间步偏移（dynamic shifting）**：`use_dynamic_shifting=true`，`base_shift=0.25`、`max_shift=0.75`，按图像序列长度（`base_image_seq_len=256` → `max_image_seq_len=4096`）线性插值偏移噪声调度——即分辨率越高、序列越长，噪声时间表越往高噪端偏移。这是支撑「任意分辨率」训练/采样的关键技巧。
- **多阶段 / SFT / 偏好对齐 / 蒸馏**：CogView4 官方**未披露**是否做了美学微调、SFT、RLHF/DPO、reward model 或步数蒸馏（CogView3 论文报告过对 relay 阶段做渐进式蒸馏，但那是 CogView3 的方法，不能直接套到 CogView4）。CogView4 仓库「Project Plan」中 ControlNet 训练代码仍为 TODO。
- **推理超参（官方示例）**：`num_inference_steps=50`、`guidance_scale=3.5`、1024×1024。微调由官方 CogKit（LoRA/SFT）或社区 finetrainers（单卡 4090 低显存）支持。

## Infra（训练 / 推理工程）
- **训练算力/并行/GPU·时：未披露**（无技术报告）。
- **推理显存（BF16, batchsize=4，官方实测）**：
  - 512² / 1024² / 1920×1280：不开 offload 约 33–39GB；开 `enable_model_cpu_offload` 降到 20GB；再叠加 text encoder 4-bit 量化进一步降到 13–14GB。
  - 另建议设备 ≥32GB 内存防 OOM 被杀。
- **量化/部署**：官方推理脚本支持 BNB int4 加载 text encoder、TorchAO int8/int4 加载 text encoder+transformer；VAE 支持 slicing/tiling 省显存。部署形态：HF diffusers `CogView4Pipeline`（pipeline 组成 = GLM text encoder + `CogView4Transformer2DModel` + 16-ch `AutoencoderKL` + `FlowMatchEulerDiscreteScheduler`）、HF/ModelScope Space、智谱 MaaS API（模型码 `cogView-4-250304`，0.06 元/次）。

## 评测 benchmark（把效果讲清楚）
数字均来自官方 README / 模型卡 / bigmodel 产品页（CogView4-6B 行）：

- **DPG-Bench（综合 85.13，开源 SOTA / 表内第一）**：
  CogView4 85.13 > Janus-Pro-7B 84.19 > SD3-Medium 84.08 > Flux.1-dev 83.79 > DALL·E 3 83.50 > SDXL 74.65 > PixArt-α 71.11。子项里 Attribute 91.17、Relation 91.14 为表内最高；Global(83.85)、Other(87.29) 偏弱。官方明确称发布时 DPG-Bench 综合评分**开源 SOTA**。
- **GenEval（Overall 0.73）**：落后 Janus-Pro-7B（0.80）、SD3-Medium（0.74），优于 Flux.1-dev（0.66）、DALL·E 3（0.67）、SDXL（0.55）。Single Obj 0.99（并列最高）；Position 0.48、Color attribution 0.58 中游。
- **T2I-CompBench**：Numeracy **0.6626（表内最高）**、Complex 3-in-1 **0.3869（最高）**；Color 0.7786、Texture 0.6983、Shape 0.5880 与 SD3/DALL·E 3 接近；2D-Spatial 0.3075、3D-Spatial 0.3708 中游。
- **中文文字渲染准确率**（官方自建评测，vs Kolors）：Precision **0.6969**、Recall **0.5532**、F1 **0.6168**、Pick@4 **0.3265**，**全面碾压 Kolors**（F1 0.288、Pick@4 0.163），印证「首个开源汉字渲染」的定位。
- 关键对比结论：CogView4 在**复杂指令跟随（DPG-Bench）与中文/汉字渲染**上是亮点；在 GenEval 这类对象/计数/空间组合上略逊 Janus-Pro-7B、SD3-Medium。
- **未报告**：FID、CLIPScore、MJHQ-30K、HPSv2/ImageReward/PickScore、人评 ELO/Arena，官方 README 与产品页均未给出；消融实验也未公开（无技术报告）。

## 创新点与影响
- **核心贡献**：(1) 用双语 **GLM-4-9B LLM 替代 T5** 作文本编码器，把中文语义理解与**汉字字形渲染**带进开源文生图，1024 token 长提示；(2) MMDiT 联合注意力 + 2D RoPE + AdaLN-Zero + 16-ch VAE 的现代 DiT 架构；(3) **flow matching + 动态分辨率偏移**实现「任意长度 caption × 任意分辨率」混合训练，原生支持 512–2048 任意尺寸；(4) Apache-2.0 全开源（权重 + diffusers 集成 + CogKit 微调），6B 单卡可跑（量化后 13GB）。
- **影响**：作为首个开源汉字渲染 T2I，迅速被 diffusers 官方集成、ComfyUI 封装、finetrainers/CogKit 支持，成为中文海报/电商/广告/文旅创意场景的开源基座；其「LLM 当 text encoder + flow matching DiT」思路也与同期 SD3/Flux 的工程取向汇流。
- **已知局限**：(1) **无独立技术报告**，数据规模/配比、训练算力、是否做偏好对齐/蒸馏等均未披露；(2) GenEval 上对象/计数/空间组合弱于 Janus-Pro-7B、SD3-Medium；(3) 推理显存偏高（不量化需 33GB+），FP16 不可用；(4) ControlNet/编辑能力发布时仍为 TODO；(5) 强依赖 LLM 提示词扩写以对齐长合成 caption 训练分布。

## 原始链接
- github: https://github.com/THUDM/CogView4
- hf (model card): https://huggingface.co/THUDM/CogView4-6B
- modelscope: https://modelscope.cn/models/ZhipuAI/CogView4-6B
- 官方产品页 / MaaS 文档: https://docs.bigmodel.cn/cn/guide/models/image-generation/cogview-4
- diffusers 参考实现: https://github.com/huggingface/diffusers/blob/main/src/diffusers/models/transformers/transformer_cogview4.py
- 谱系论文 (CogView3, relay diffusion + re-caption 方法): https://arxiv.org/abs/2403.05121
- CogKit 微调工具: https://github.com/THUDM/CogKit

## 本地落盘文件
- ../../../sources/omni/2025/cogview4--github-readme.md
- ../../../sources/omni/2025/cogview4--github-readme-zh.md
- ../../../sources/omni/2025/cogview4--hf-modelcard.md
- ../../../sources/omni/2025/cogview4--transformer-config.json
- ../../../sources/omni/2025/cogview4--vae-config.json
- ../../../sources/omni/2025/cogview4--scheduler-config.json
- ../../../sources/omni/2025/cogview4--model_index.json
- ../../../sources/omni/2025/cogview4--diffusers-transformer.py
- ../../../sources/omni/2025/cogview4--bigmodel-docs.md
- ../../../sources/omni/2025/arxiv-2403.05121.pdf
