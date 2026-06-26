---
title: "FLUX.2 [klein]"
org: Black Forest Labs
country: Germany
date: "2026-01"
type: model-card
category: unified
tags: [flux, rectified-flow, mmdit, step-distillation, image-editing, multi-reference, apache-2.0, consumer-gpu]
url: https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
arxiv: ""
pdf_url: ""
github_url: https://github.com/black-forest-labs/flux2
hf_url: https://huggingface.co/black-forest-labs/FLUX.2-klein-4B
modelscope_url: ""
project_url: https://bfl.ai/models/flux-2-klein
downloaded:
  - flux-2-klein--blog.md
  - flux-2-klein--flux2-announce-blog.md
  - flux-2-klein--vae-research-blog.md
  - flux-2-klein--docs-overview.md
  - flux-2-klein--klein-training-doc.md
  - flux-2-klein--kv-cache-doc.md
  - flux-2-klein--github-readme.md
  - flux-2-klein--hf-4b-card.md
  - flux-2-klein--flux2-dev-card.md
  - flux-2-klein--hf-collection-api.md
  - flux-2-klein--src-model.py
  - flux-2-klein--src-util.py
  - flux-2-klein--src-text_encoder.py
  - flux-2-klein--src-autoencoder.py
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
FLUX.2 [klein] 是 Black Forest Labs 2026-01-15 发布的「最快 FLUX 图像模型」家族——把 32B 的 FLUX.2 base 通过**尺寸蒸馏 + 步数蒸馏 + 引导蒸馏**压成 4B / 9B 的 rectified-flow MMDiT，统一文生图、单图编辑、多图参考编辑于一个模型；4B 在消费级 GPU（RTX 3090/4070，约 13GB 显存）上 **4 步、亚秒（<0.5s）** 生成/编辑，且 4B 全权重以 **Apache-2.0** 开源。官方称其在 Elo×延迟×显存的帕累托前沿上匹敌或超越尺寸 5 倍的模型。

## 背景与定位
延续 BFL 的「open core」路线：用开放权重模型（[[flux-1]] dev 是全球最受欢迎的开源图像模型）拉社区，用闭源 API（pro/flex/max）做商业。2025-11-25 发布的 **FLUX.2** 重构了整条栈——新 32 通道 latent VAE、用 VLM 当文本/图像条件编码器、单一 checkpoint 同时做生成与编辑、支持最多 10 张参考图、4MP 输出。FLUX.2 [dev]（32B）是其开源旗舰但需 H100 级显存。

klein 解决的是**「交互式视觉智能」的延迟与可达性问题**：随着 agent 越来越能用图，需要能实时响应、快速迭代、跑在普通硬件上的生成模型。klein（德语「小」）既指模型小也指延迟低。它不是从头训练的小模型，而是从 FLUX.2 base **蒸馏**而来，因此「比同尺寸从头训练的模型更强，保留教师模型的大部分能力」（官方公告原话）。相对前置工作：相比 [[flux-1-kontext]] 的「编辑专用」分支，klein/FLUX.2 把 T2I 与编辑彻底统一进一个 checkpoint；相比 [[latent-diffusion-ldm]] / SDXL 系，换成 rectified-flow + MMDiT + VLM 文本编码器 + 32ch latent 的新栈。

## 模型架构
**Backbone：rectified-flow Transformer，MMDiT 式双流→单流结构**（源码 `src/flux2/model.py` 实测）。三档参数共享同一架构骨架，仅缩放宽度/深度（`axes_dim` 恒为 [32,32,32,32]，RoPE `theta=2000`，`mlp_ratio=3.0`）：

| 配置 | hidden_size | num_heads | double-stream blocks (`depth`) | single-stream blocks | context_in_dim | guidance_embed |
|---|---|---|---|---|---|---|
| FLUX.2 [dev/base] 32B | 6144 | 48 | 8 | 48 | 15360 | True |
| [klein] 9B | 4096 | 32 | 8 | 24 | 12288 | **False** |
| [klein] 4B | 3072 | 24 | 5 | 20 | 7680 | **False** |

- **双流→单流**：前若干层（depth）文本 token 与图像 token 各走一支（double-stream），随后拼接进单流块（single-stream）联合注意力——典型 MMDiT 设计；图像/文本/参考图的位置由 N 维 RoPE（`EmbedND`）编码。
- **guidance embedding 全档关闭**（三档 klein 的 `Klein4BParams`/`Klein9BParams` 均 `use_guidance_embed=False`，源码实测）：distilled 档引导已蒸进权重，推理 `guidance=1.0`、4 步、无需 CFG 双前向；klein-base 档同样 `use_guidance_embed=False`（故权重里无 `guidance_in` 模块，`util.py` 默认传的 `guidance=4.0` 在前向中被忽略），但 `guidance_distilled=False` 且默认 50 步采样（见下「训练方法」）。对照之下 FLUX.2 [dev] 的 `Flux2Params` 才是 `use_guidance_embed=True`。

**Visual tokenizer / VAE（FLUX.2 autoencoder，Apache-2.0）**：`src/flux2/autoencoder.py` 实测为卷积式 VAE，`ch=128`、`ch_mult=[1,2,4,4]`（8× 空间下采样）、`z_channels=32`、`num_res_blocks=2`、含中段自注意力。**32 通道 latent**（FLUX.1 为 16 通道），再经 2×2 patchify → transformer `in_channels=128`（32×2×2）。BFL 称重训 latent space 是为「同时拿到更好的可学习性与更高画质」，逼近「可学习性–画质–压缩率」三难。BFL 另以独立 repo `black-forest-labs/FLUX.2-small-decoder` 发布轻量 VAE 解码器（HF API 实证存在，likes 151）。

**Text encoder：用 LLM 隐状态当条件，且 klein 与 base 用的 LLM 不同（关键差异）**：
- FLUX.2 [dev/base] 用 **Mistral-Small-3.2-24B-Instruct** 作 VLM，取第 [10,20,30] 层隐状态拼接 → 15360 维。
- **[klein] 改用 Qwen3 嵌入器**（`load_qwen3_embedder`）：[klein] 4B 用 `Qwen/Qwen3-4B-FP8`，[klein] 9B 用 `Qwen3-8B-FP8`；取第 **[9,18,27] 三层隐状态拼接**（`rearrange "b c l d -> b l (c d)"`）→ 4B 7680 维（3×2560）、9B 12288 维（3×4096）。klein blog 原文：「9B flow model with 8B Qwen3 text embedder」。文本最大长度 `MAX_LENGTH=512` token。
- 多图编辑：参考图经 VAE 编码成 token 与噪声 token 拼接做联合注意力；[klein] 9B KV 变体把参考 token 的 K/V 缓存下来跨步复用（详见 Infra）。

**条件注入**：time 与（base 档的）guidance 经 256 维 sinusoidal → MLPEmbedder 注入；无单独的 pooled CLIP 向量分支（与 FLUX.1 不同，文本完全来自 LLM 隐状态）。klein **不含 prompt upsampling**（官方文档明确），需用户写详细 prompt。

## 数据
官方未披露训练数据来源/规模/配比/合成数据比例等细节（HF card、blog、公告均未给数字）。仅披露**安全相关的数据处理**（HF model card「Responsible AI」节）：
- **预训练阶段**：过滤多类 NSFW 与已知 CSAM；与 IWF（Internet Watch Foundation）合作过滤已知 CSAM。
- **后训练阶段**：多轮定向 fine-tuning 做安全对齐，抑制 T2I/I2I 两路的滥用行为。
- LoRA 微调指南（面向用户，非 BFL 预训练）建议数据：1024px+ 高分辨率、详细 caption、含 trigger word、多样化姿态/光照——可侧面反映其偏好的数据特征，但非官方训练集说明。
- 训练规模、图文对数量、re-captioning 方法、美学过滤具体口径：**未披露**。

## 训练方法
**训练目标：latent rectified flow / flow matching**（公告原文「latent flow matching architecture … rectified flow transformer」）。klein 的核心是**三重蒸馏 pipeline**，把 32B FLUX.2 base 教师压成小学生：

1. **尺寸蒸馏（size distillation）**：从 FLUX.2 base 蒸出 4B / 9B 容量的 flow 模型——「size-distilled from the FLUX.2 base model」（公告）。这是 klein 区别于「从头训小模型」的关键，使其继承教师的世界知识与编辑能力。
2. **步数蒸馏（step distillation）**：distilled 档蒸到 **4 步**推理（`num_steps=4`，`fixed_params` 锁定）；base 档不蒸、保留 **50 步**全采样信号。klein blog：「step-distilled to 4 inference steps」。
3. **引导蒸馏（guidance distillation）**：distilled 档把 CFG 蒸进权重（`guidance_distilled=True`，`use_guidance_embed=False`，推理 `guidance=1.0`），免去无分类器引导的双前向，直接砍一半算力。（FLUX.2 [dev] 也用 guidance distillation——见 dev card 第 4 条。）

**Distilled vs Base 两条产品线**：
- **Distilled（4-step, guidance=1.0）**：生产/实时，最快；输出多样性略低。
- **Base（50-step, undistilled, `guidance_distilled=False`）**：保留完整训练信号，输出多样性最高，适合 LoRA/全量微调与研究（`util.py` 默认 `guidance=4.0` 但因 `use_guidance_embed=False` 在前向中不生效）。base 仍开权重（4B base Apache-2.0，9B base NCL）。

**安全后训练**：发布前多轮针对 CSAM/NCII 的安全 fine-tuning，并经第三方对抗评测（T2I、单参考图、多参考图三路）后才定版；BFL 称最终 klein checkpoint 对违规输入的抵抗力高于主流开源权重模型。

具体训练算力、优化器、学习率、batch、训练步数等超参：**未披露**（仅 LoRA 用户微调指南给了 LR 8e-5~1e-4 等，非 BFL 预训练超参）。

## Infra（训练 / 推理工程）
**训练算力/并行/GPU·时**：**未披露**。

**推理加速**（一手数字）：
- **步数**：distilled 4 步；推理代码 README 注明在 **GB200 / CUDA 12.9 / Python 3.12** 上测试。基准速度「measured on a GB200 in bf16」。
- **量化（与 NVIDIA 合作）**：发布全家 FP8 与 NVFP4 版本，针对 RTX GPU 优化（RTX 5080/5090，T2I 1024×1024 基准）：
  - **FP8**：最高 **1.6× 提速、显存最高省 40%**。
  - **NVFP4**：最高 **2.7× 提速、显存最高省 55%**。
  HF 上已上线 fp8 / nvfp4 全套（4B/9B/base/kv 各档）。
- **KV 缓存（[klein] 9B KV 变体）**：编辑时参考图 token 跨去噪步不变，标准做法每步都重算其注意力是浪费。KV 变体分两阶段——step 0 `forward_kv_extract` 全前向并缓存参考 token 的 K/V；step 1+ `forward_kv_cached` 仅算输出+文本 token、拼接复用缓存 KV。实测提速（参考图各 1024×1024）：

  | #Refs | 输出512² | 768² | 1024² | 1440² |
  |---|---|---|---|---|
  | 1 | 1.78× | 1.57× | 1.40× | 1.21× |
  | 2 | 2.16× | 1.97× | 1.77× | 1.46× |
  | 3 | 2.43× | 2.21× | 1.99× | 1.69× |
  | 4 | 2.66× | 2.44× | 2.22× | 1.85× |

  参考图越多、输出分辨率越小，收益越大。BFL 称 9B KV 在多参考编辑上「比 4B 还快、同等质量」。
- **显存/部署**：4B distilled ~**13GB VRAM**（RTX 3090/4070 起）；`enable_model_cpu_offload()` 可进一步省显存。已接入 ComfyUI 与 🤗 Diffusers（`Flux2KleinPipeline`）。
- **部署形态**：BFL API（preview 端点 `flux-2-klein-9b-preview` 默认带 KV 缓存）+ 开放权重本地运行；4B/9B distilled API 定价 $0.014~0.015/图 + $0.001~0.002/MP。

## 评测 benchmark（把效果讲清楚）
BFL 仅以**人评 Elo + 延迟/显存帕累托图**呈现，**未公布 FID / GenEval / DPG-Bench / CLIPScore 等标量分**（一手源中无这些数字，故标「未报告」）。一手可引述的结论：
- **三任务 Elo（T2I / 单参考编辑 / 多参考生成）vs 延迟与 vs 显存**（speed 在 GB200 bf16 上测）：
  - klein **匹敌或超越 Qwen（[[qwen-image]]）的质量，但延迟与显存只是其一小部分**；
  - klein **在质量上超过 Z-Image**，且同时支持 T2I 与（多参考）编辑这一统一能力（Z-Image 不具）；
  - **9B distilled「匹配或超过尺寸 5 倍模型，且在半秒内」**（klein blog 原话，未给被比模型的具体表名）。
- **base vs distilled**：base 变体牺牲速度换全可定制性与更高输出多样性，更适合研究与适配。
- **量化对比**：FP8/NVFP4 在 RTX 5080/5090、1024² T2I 上的提速/省显存倍数见 Infra 节。
- 具体 Elo 数值、对手清单、各 benchmark 标量分、消融实验：**官方未在 blog/card 中给出表格数字**（仅图示），故无法抠出精确分数。

## 创新点与影响
**核心贡献**：
1. **「蒸馏出来的小模型」范式**：用尺寸+步数+引导三重蒸馏，把 32B 前沿模型压成 4B/9B，使「消费级 GPU、亚秒、统一生成+多参考编辑」三者首次同时成立——填补了「小而强且通用」的空档。
2. **统一架构**：单 checkpoint 同时做 T2I、单图编辑、多参考编辑（klein 最多 4 张参考），无需切换模型或额外 ControlNet 分支。
3. **KV 缓存编辑加速**：把 LLM 推理里的 KV-cache 思想搬到 diffusion 多参考编辑，参考 token 一次编码跨步复用，2~2.7× 提速且不掉质量——对「多图一致性」这一最贵场景特别有效。
4. **Qwen3 作图像生成文本编码器**：klein 用 Qwen3-4B/8B 隐状态（而非 base 的 Mistral-24B），在小模型上保留强语义条件，验证了「换更小但够强的 LLM 当 text embedder」的可行性。
5. **开放度**：4B 全档（含 base 与量化）**Apache-2.0**，可商用、可微调，外加 NVIDIA 合作的 FP8/NVFP4，社区可达性极高（HF `FLUX.2-klein-4B` 近 30 天下载 ~516k、753 likes，HF API 查询于 2026-06-25；注意此为 HF 的滚动 30 天计数，非自发布以来累计）。

**对后续工作的影响**：把「交互式视觉智能 / agentic 视觉」拉到可落地——实时设计工具、agent 边生成边迭代、边缘部署；Apache-2.0 + LoRA 友好的 base 档会催生大量风格/角色微调生态（AI-Toolkit、Diffusers DreamBooth 已支持）。

**已知局限（官方明示）**：不提供事实性信息；文本渲染可能失真；可能放大训练数据偏见；prompt following 受 prompt 风格影响大；**klein 无 prompt upsampling**，依赖用户写详细 prompt；多参考上限 klein 仅 4 张（pro/max 为 8~10）；训练数据/算力/标量 benchmark 均未公开，复现与横评受限。

## 原始链接
- blog（klein 发布，一手主源）: https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
- blog（FLUX.2 base/dev 公告，架构与 VLM 来源）: https://bfl.ai/blog/flux-2
- research（FLUX.2 VAE / latent space 报告，页面 JS 未渲染出正文）: https://bfl.ai/research/representation-comparison
- docs（FLUX.2 overview，定价/多参考/KV preview 端点）: https://docs.bfl.ai/flux_2/flux2_overview
- docs（klein 训练/LoRA 指南）: https://docs.bfl.ai/flux_2/flux2_klein_training
- github（KV cache 文档，提速表）: https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_klein_kv_cache.md
- github README: https://github.com/black-forest-labs/flux2
- github 源码（架构 ground truth）: src/flux2/model.py, util.py, text_encoder.py, autoencoder.py
- hf model card（4B）: https://huggingface.co/black-forest-labs/FLUX.2-klein-4B
- hf collection（含 fp8/nvfp4/kv/small-decoder 全档）: https://huggingface.co/collections/black-forest-labs/flux2
- hf API（下载/likes 计数快照，2026-06-25）: https://huggingface.co/api/models?author=black-forest-labs&search=FLUX.2

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--blog.md)
- [flux2-announce-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--flux2-announce-blog.md)
- [vae-research-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--vae-research-blog.md)
- [docs-overview.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--docs-overview.md)
- [klein-training-doc.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--klein-training-doc.md)
- [kv-cache-doc.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--kv-cache-doc.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--github-readme.md)
- [hf-4b-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--hf-4b-card.md)
- [flux2-dev-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--flux2-dev-card.md)
- [hf-collection-api.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--hf-collection-api.md)
- [src-model.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--src-model.py)
- [src-util.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--src-util.py)
- [src-text_encoder.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--src-text_encoder.py)
- [src-autoencoder.py](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/flux-2-klein--src-autoencoder.py)
