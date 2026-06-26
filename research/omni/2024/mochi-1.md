---
title: "Mochi 1 (preview)"
org: "Genmo"
country: US
date: "2024-10"
type: blog
category: video
tags: [text-to-video, diffusion-transformer, asymmdit, mmdit, 3d-attention, flow-matching, open-source, apache-2.0, video-vae]
url: "https://www.genmo.ai/blog/mochi-1-a-new-sota-in-open-text-to-video"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/genmoai/mochi"
hf_url: "https://huggingface.co/genmo/mochi-1-preview"
modelscope_url: ""
project_url: "https://www.genmo.ai/play"
downloaded: [mochi-1--blog-post.md, mochi-1--blog-index.md, mochi-1--github-models-readme.md, mochi-1--hf-modelcard.md, mochi-1--finetuner-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Mochi 1（preview）是 Genmo 于 **2024 年 10 月**在 Apache 2.0 下开源的 **10B 参数文生视频扩散模型**，基于自研 **Asymmetric Diffusion Transformer（AsymmDiT）** + **AsymmVAE**，是当时**最大的公开发布的视频生成模型**；以 480p / 30fps / 最长 5.4 秒、强运动质量与强 prompt 跟随著称，号称在开源里设新 SOTA 并逼近闭源系统。注意：官方仅有博客 + 代码/权重，**从未发布独立技术报告/arXiv 论文**（博客写"technical paper will follow"，实际未兑现）。

> 发布日期注：落盘一手源里 BibTeX 标 `year={2024}`，github News 最早两条为 2024-11-05 / 2024-11-26；当前抓到的博客页因站点改版顶部显示 "September 10, 2025"（CMS 重发时间，非真实首发）。**精确到日的发布日期未落在一手源内**，故本页只写到 "2024-10"（业界普遍记为 2024-10-22，但本页不以未落盘的口径断言）。

## 背景与定位
2024 年视频生成领域的两大短板是**运动质量（motion quality）**与**prompt 跟随（prompt adherence）**——多数模型只能产出 2–3 秒、运动幅度小或物理不连贯的片段。Mochi 1 的定位就是用一个**完全从零训练**的大模型把这两件事做好，并把"开源与闭源之间的差距"显著拉近。

技术脉络上它属于 **DiT 系视频扩散** 这条线（与 [[cogvideox]]、Sora、Gen-3 同期），核心架构借鉴了 Stable Diffusion 3 的 **MMDiT**（文/图双流、各自独立 MLP、在自注意力里联合）——但 Mochi 把它改成"不对称"的省显存版本。Genmo 团队由 [[ddpm]]、[[dreamfusion]]、[[emu-video]] 等工作的核心作者组成，技术顾问含 Ion Stoica、Pieter Abbeel、Joey Gonzalez；发布同时官宣 NEA 领投的 2840 万美元 A 轮。模型潜空间压缩沿用 [[latent-diffusion-ldm]] 的 latent 扩散范式，但用的是自研视频 VAE。

## 模型架构
**整体：T5-XXL 文本编码 → AsymmDiT（10B）在 AsymmVAE latent 空间做扩散 → AsymmVAE 解码出视频。** 480p、宽高 848×480、帧数为 6 的倍数（如 31/37/…/85 帧），30fps 下最长 5.4 秒。

**AsymmVAE（视频 VAE，362M）**——非对称编/解码器结构，**因果（causal）压缩**视频：
- 空间 8×8、时间 6× 压缩，输出 **12 通道 latent**。
- 总压缩率：README/HF model card 写 **"128x smaller"**，博客原文写 **"96x smaller"**——**两处官方口径不一致**。本页如实并列，不自行裁定哪个对（按 8×8×6 像素压缩、RGB 3 通道→12 通道 latent 反推得 384×3/12=96×，与博客一致；128× 的来历官方未给算式）。
- Enc base channels 64 / Dec base channels 128（解码器更重，符合"非对称"命名——把算力堆在重建质量上）。
- 解码支持 tiled（`tiled_spatial` / `tiled_full`）以省显存。

**AsymmDiT（主干，10B）**——MMDiT 的"非对称"变体：
- 48 层，24 个注意力头，**visual hidden dim 3072 / text hidden dim 1536**（视觉流隐维是文本流 2 倍；博客称视觉流参数约为文本流 **4 倍**）。
- 文/视觉**双流多模态自注意力**：联合 attend，但每模态学**独立 MLP**（同 SD3）。把更多网络容量集中到视觉推理，文本侧"瘦身"。
- 为统一两模态做 attention，用**非方阵（non-square）的 QKV 与输出投影**——这是"省推理显存"的关键设计。
- **单一 T5-XXL** 文本编码器（256 个 text token），不像很多模型叠多个文本塔（CLIP+T5），强调简洁。
- **全 3D 注意力**：在 **44,520 个 video token** 的上下文窗口上做 full 3D attention（联合空间+时间，无时空分解）。
- **3D RoPE**：把可学习的旋转位置编码扩展到 3 维，端到端学习空间/时间轴的 mixing frequencies。
- 借鉴 LLM scaling 的若干稳定性 trick：**SwiGLU** FFN、**QK-normalization**（query-key 归一化增强稳定性）、**sandwich normalization**（控制内部激活）。

设计哲学被反复强调为 "simple, hackable architecture"——便于社区改造与微调。

## 数据
**未披露。** 官方博客、README、HF model card 均未公开训练数据的来源、规模、图文/视频对数量、配比、清洗/过滤、re-captioning 或合成数据策略。仅在 Safety 段落笼统说"模型反映训练数据中的偏见/成见，已采取措施限制 NSFW 内容"。由于没有技术报告，数据维度基本是黑盒。可间接确认的只有：训练**完全从零（from scratch）**，非在已有模型上继续训练。

## 训练方法
**预训练目标 / 多阶段流程 / RL 对齐 / 蒸馏等核心训练细节均未披露**（无技术报告）。能从一手源确认的有限信息：

- **从零训练**的扩散 Transformer（diffusion model，10B）。推理用的采样调度 `linear_quadratic_schedule` + `sigma_schedule`（默认 64 步），CFG schedule 默认每步 6.0（README）/ 4.5（HF model card 的高质量 API 示例），暗示训练目标是连续时间扩散/flow 类（官方未明说是否 rectified flow）。
- 发布的是 **480p base model**，官方称 "Mochi 1 HD 将于年内推出"（更高分辨率版）。
- **未报告**：训练算力、GPU·时、数据并行/序列并行方案、batch、学习率、训练步数、SFT / 偏好对齐（RLHF/DPO）、步数蒸馏（consistency/LCM/ADD）等。

**LoRA 微调（官方提供 trainer，2024-11-26 加入）**——这是官方唯一公开细节的训练子流程：
- 单卡 LoRA 微调（1× H100/A100 80GB），**仅更新 Q/K/V 投影 + 输出投影**矩阵。
- 视频按 **30 FPS** 处理，帧数取 6 的倍数（25/31/37…85，最长 85 帧≈2.8s）。
- 学习率约 **1e-4 ~ 2e-4** 较有效；200–400 步开始见效，1000 步≈30 分钟。
- 显存/吞吐（1×H100 SXM，启用 gradient checkpointing，`num_qkv/ff/post_attn_checkpoint=48`）：37 帧 50GB / 1.67 s·it⁻¹；61 帧 64GB / 3.35 s·it⁻¹；79 帧 69–78GB / 4.92 s·it⁻¹；85 帧 80GB / 5.44 s·it⁻¹。`COMPILE_DIT=1`（torch.compile）省显存并加速。

## Infra（训练 / 推理工程）
- **推理（官方 harness）**：单卡约需 **60GB VRAM**（FP/bf16，本仓库"重灵活轻省显存"）；推荐至少 1× H100。提供**高效 context-parallel 实现**做多卡张量/序列并行（把模型切到多张卡）。
- **diffusers 集成**：标准精度需 ~42GB VRAM（最高质量）；**bf16 变体仅需 ~22GB VRAM**（质量略降）；配 `enable_model_cpu_offload` + `enable_vae_tiling` 进一步省显存。
- **消费级 GPU**：ComfyUI 集成可把显存压到 **<20GB**（官方 README 提及，社区 ComfyUI-MochiWrapper / mochi-xdit 进一步加速并行推理）。
- 部署形态：开放权重（HF / 直链 / magnet 种子）+ 官方 Playground（genmo.ai/play）+ Replicate 等 API 合作方。
- **训练 infra 规模未披露**（无技术报告，无 GPU·时/集群规模/并行细节）。

## 评测 benchmark（把效果讲清楚）
官方**只给了两条定性/相对评测维度，没有放任何绝对数字表**（无 FID/VBench/CLIPScore/具体 Elo 数值落到一手源）：

- **Prompt Adherence（prompt 跟随）**：用 **VLM-as-judge** 自动指标，方法学**沿用 OpenAI DALL-E 3 的协议**，评测裁判用 **Gemini-1.5-Pro-002**。官方称在开源里"exceptional alignment"、设 best-in-class，并与领先闭源"很有竞争力"——但**未公布具体分数**。
- **Motion Quality（运动质量）**：人评 **Elo**，按 **LMSYS Chatbot Arena 协议**计算；评审被要求只看运动（运动的趣味性、物理合理性、流畅度），不看单帧美学。官方称运动平滑、30fps/最长 5.4s、时间一致性强，能模拟流体动力学、毛发模拟、连贯人体动作，"开始跨越恐怖谷"——同样**未公布具体 Elo 数值**。

> 注：博客配图给了 "Prompt Adherence" 与 "Elo Score" 两张对比图，但图中竞品名称与数值未进入抓取到的文本，**故本页不复述任何具体分数**（源里没有就写"未报告"）。无 GenEval/T2I-CompBench/MJHQ/VBench 等标准化 benchmark 的官方数字，也无公开消融实验。

## 创新点与影响
**核心贡献：**
1. **AsymmDiT**：把 SD3 的对称 MMDiT 改造为"视觉流远重于文本流 + 非方阵 QKV/输出投影"的不对称设计，在保住文/视觉联合注意力质量的同时显著降低推理显存——是把 MMDiT 往"大视频模型可落地"方向推的一个实用工程化变体。
2. **AsymmVAE**：362M 的非对称因果视频 VAE，8×8 空间 + 6× 时间压缩到 12 通道 latent，解码器比编码器重，单独开源。
3. **全 3D 注意力 + 3D RoPE**：在 44,520 token 上做无时空分解的 full 3D attention，端到端学时空 mixing frequencies；叠加 SwiGLU/QK-norm/sandwich-norm 等 LLM 稳定性 trick。
4. **当时最大的开源视频模型（10B），Apache 2.0**：连同高效 context-parallel 推理 harness 一起放出，"hackable"定位直接催生 ComfyUI / xDiT / diffusers 生态与大量社区 LoRA 微调。

**影响：** 在 [[cogvideox]] 之后进一步抬高开源文生视频的天花板；Apache 2.0 + 可单卡（≥60GB，bf16 可 22GB，ComfyUI 可 <20GB）运行使其成为 2024 末社区研究/二创的主力底座之一；为机器人/自动驾驶合成数据等下游场景提供开源选项。

**已知局限（官方）：** 仅 480p（博客称 HD 版"coming later this year"，落盘源未含其后续是否兑现的信息）；极端运动下可能出现 minor warping/扭曲；**偏写实风格，动画/卡通内容表现差**；research preview，是"living and evolving checkpoint"。**深层局限是透明度**——无技术报告，数据/训练/算力/绝对评测数字全黑盒，难以复现与公平对比。

## 原始链接
- blog（最权威一手源）: https://www.genmo.ai/blog/mochi-1-a-new-sota-in-open-text-to-video
- blog index: https://www.genmo.ai/blog
- github（代码 / 权重 / 架构表 / 推理 harness）: https://github.com/genmoai/mochi （= github.com/genmoai/models，二者 README 完全相同）
- github LoRA fine-tuner README: https://github.com/genmoai/mochi/blob/main/demos/fine_tuner/README.md
- huggingface（model card + 权重 + diffusers 用法/显存）: https://huggingface.co/genmo/mochi-1-preview
- playground: https://www.genmo.ai/play
- 注：官方**无 arXiv 技术报告**（已核实；博客承诺的 paper 未发布）

## 一手源存档（sources/）
- [blog-post.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/mochi-1--blog-post.md)
- [blog-index.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/mochi-1--blog-index.md)
- [github-models-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/mochi-1--github-models-readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/mochi-1--hf-modelcard.md)
- [finetuner-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/mochi-1--finetuner-readme.md)
