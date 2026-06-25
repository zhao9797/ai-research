---
title: "Open-Sora Plan / Open-Sora（2024 开源复现 Sora）"
org: "PKU-YuanGroup（北大-兔展）/ HPC-AI Tech（潞晨）"
country: China
date: "2024-12"
type: tech-report
category: video
tags: [video, t2v, i2v, dit, diffusion, sora-reproduction, open-source, wf-vae, skiparse-attention, rectified-flow]
url: https://arxiv.org/abs/2412.00131
arxiv: https://arxiv.org/abs/2412.00131
pdf_url: https://arxiv.org/pdf/2412.00131
github_url: https://github.com/PKU-YuanGroup/Open-Sora-Plan
hf_url: https://huggingface.co/LanguageBind/Open-Sora-Plan-v1.3.0
modelscope_url: https://modelers.cn/models/linbin/Open-Sora-Plan-v1.3.0
project_url: https://github.com/hpcaitech/Open-Sora
downloaded: [arxiv-2412.00131.pdf, arxiv-2412.20404.pdf, arxiv-2503.09642.pdf, arxiv-2411.17459.pdf, open-sora-plan--readme.md, open-sora-hpcai--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
两个同名为「Open-Sora」的中国开源团队（北大-兔展 **Open-Sora Plan** 与潞晨 **HPC-AI Tech Open-Sora**）在 2024 年 OpenAI Sora 发布后率先发起的开源复现项目，把"长时高分辨率视频生成"的完整技术栈（VAE / DiT / 数据管线 / 训练 trick）开源到社区。两条线最亮眼的数字：Open-Sora Plan v1.3 的 **WF-VAE** 在 4×8×8 压缩下编码吞吐比 CogVideoX / OD-VAE / Allegro 快 **4–7.8×**、显存降 **5–8×**（v1.5 才升到 8×8×8 更高压缩）；潞晨 **Open-Sora 2.0（11B）** 仅用 **$200K（约 4160 H200 GPU·天）** 训练，在 VBench 上把与 OpenAI Sora 的差距从 4.52% 压到 **0.69%**，人评与 HunyuanVideo 11B / Step-Video 30B 持平。

> 注：本 slug 同时覆盖两个独立项目（GitHub `PKU-YuanGroup/Open-Sora-Plan` 与 `hpcaitech/Open-Sora`），二者代码与权重不互通，仅"复现 Sora、开源全栈"的目标相同。下文以一手技术报告为准分别叙述，并在每节标注归属。

## 背景与定位
2024 年 2 月 OpenAI 发布 Sora 技术报告（仅有 showcase、无方法细节），在视频生成社区引发震动并指明"spacetime patches + DiT + 大规模数据"的方向。当时开源的视频生成多停留在低分辨率短片段（[[animatediff]] 类、Stable Video Diffusion）。两个国内团队几乎同时（2024.03）发起开源复现：

- **Open-Sora Plan（北大-兔展 PKU-YuanGroup，项目负责人 Li Yuan/袁粒）**：定位"复现一个强大的 Sora 式模型"，强调把整条管线拆成可替换组件（VAE / 去噪器 / 条件控制器），并在华为昇腾 NPU 上训练（v1.5 起"纯血昇腾"）。版本线：v1.0（2024.04，2+1D）→ v1.1（2024.05，加长加质）→ v1.2（2024.07，转 **Full 3D Attention**，720p）→ v1.3（2024.10，**WF-VAE + Skiparse 稀疏注意力 + prompt refiner**，arXiv 2412.00131）→ v1.5（2025.06，**SUV/Skiparse-3D + 更高压缩 WFVAE**，8B，对标开源 HunyuanVideo）→ Helios（2026，单 H100 19.5 FPS 分钟级长视频）。
- **HPC-AI Tech Open-Sora（潞晨，Yang You/尤洋）**：定位"democratizing efficient video production"，强调低成本与完全可复现（数据/训练/推理全开源）。版本线：v1.0（2024.03，2s 512² 仅 3 天训练）→ v1.1（2024.04，**STDiT** 时空解耦，2–15s 多分辨率）→ v1.2（2024.06，**3D-VAE + rectified flow + score condition**，arXiv 2412.20404）→ v1.3（2025.02，shift-window attention + 统一时空 VAE，1B）→ **Open-Sora 2.0（2025.03，11B，$200K，arXiv 2503.09642）**。

两线的共同贡献是把 Sora 报告里语焉不详的工程（数据清洗、causal 3D VAE、多分辨率分桶训练、长视频条件控制）做成可跑通的开源实现，并直接孵化了下游工作（如 rhymes-ai 的 [[allegro]] 其论文明言"builds upon the VideoDiT architecture introduced in OpenSora-Plan v1.2.0"，即沿用 OSP v1.2.0 的 VideoDiT 架构再自行三阶段 T2I→T2V 训练）。技术脉络承自 [[ddpm]] [[latent-diffusion-ldm]] [[dit-scalable-diffusion-transformers]] [[pixart-alpha]]，与同期 [[cogvideox]] [[hunyuan-video]] [[gen-3-alpha]] [[ltx-video]] 并列。

## 模型架构

### A. Open-Sora Plan v1.3（北大-兔展，2412.00131）
三大组件 + 一组辅助策略：

**1. Wavelet-Flow VAE（WF-VAE，arXiv 2411.17459）** — 把视频先做**多层 Haar 小波变换**分解到频域，低频「主能量流」通过金字塔结构经 concat 注入卷积 backbone，从而以更少卷积换取压缩。压缩率 4×8×8（两层 3D 小波 + 一层 2D 小波组合），通道数 4 或 16。用 **causal 3D 卷积**（首帧单独处理 + 块间缓存）统一图像/视频。提出 **Causal Cache** 解决 tiling 分块推理导致的 latent 断裂——做到**与直接推理数值完全一致的无损分块重建**（区别于 OD-VAE 的 overlap-fusion 会掉点）。损失 = L1+感知重建 + 对抗 + KL + 新增 **WL loss**（小波层能量流一致性正则）；对抗权重按 decoder 末层梯度幅度动态平衡。

**2. Joint Image-Video Skiparse Denoiser**（去噪器，DiT 式）：
- patchify：3D 卷积 kernel/stride (kt=1, kh=2, kw=2)，latent C→D。
- 文本编码器 **mT5-XXL**（最大长度 512，经单层 MLP 投到 D）。
- **3D RoPE**：把 D 维分 3 份分别施加时间/高/宽 RoPE 再拼接。
- block：pre-norm transformer（self-attn + cross-attn + FFN），timestep 经 adaLN-Zero 映射两组 scale/shift/gate。v1.2 起从 2+1D 转 **Full 3D Attention** 显著提升运动连贯；为降二次复杂度提出 **Skiparse（Skip-Sparse）Attention**：在除首尾两层外的层交替做 **Single Skip / Group Skip** 两种稀疏操作，序列长降到 1/k、batch 增 k 倍，自注意力理论复杂度降到 1/k。提出 **Average Attention Distance（AD_avg）** 量化稀疏注意力距 Full 3D 的差距（Full 3D=1，2+1D≈1.957，Skiparse k=4 时 AD_avg=1.563，优于同 k 的 Skip+Window）。实现取 **k=4**。

**3. 条件控制器**：
- **Image Condition Controller**：把 I2V/视频转场/视频续写统一成"时间维度上的 inpainting"。仅改 DiT 输入通道（拼 mask + masked video），**不注入 CLIP 语义特征**（作者发现语义注入反而限制运动幅度）。6 种 mask（Clear/T2V/I2V/Transition/Continuation/Random）支持一框架多任务。
- **Structure Condition Controller**：轻量 encoder（3D 卷积下采样 + K 个 transformer block 提高层表征）+ projector（M 个 token-wise 变换），把 canny/depth/sketch 等结构信号的注入特征**直接加到**预训练 DiT 各 block 输出 X^j ← X^j + F^j。相比 ControlNet 复制半个 base 模型省去近 50% 硬件开销。

参数量：v1.3 报告对比表中 OpenSoraPlan v1.3 为 **2.7B**（去噪器）；v1.5 升到 **8B**（SUV/Skiparse-3D）。

### B. HPC-AI Tech Open-Sora（潞晨）
- **STDiT（Open-Sora 1.1/1.2）**：Spatial-Temporal DiT，**时空注意力解耦**（空间 attn + 时间 attn 串联），text encoder 用 **T5**，遵循 Sora「3D 自编码器 + DiT」框架。
- **3D-VAE（Open-Sora 1.2）**：复用 SDXL 预训练 2D VAE（先 8×8 空间压缩）再叠 **Magvit-v2 架构的 3D VAE（300M）做 4× 时间压缩**，合计 384M、causal 卷积；用 identity loss 让 3D VAE 特征对齐 2D VAE 加速收敛。
- **Open-Sora 2.0（11B，2503.09642）**：架构改为 **FLUX 式 MMDiT 混合 transformer**（dual-stream 分模态 + single-stream 跨模态融合）+ **3D RoPE**，text encoder = **T5-XXL + CLIP-Large**；**用开源 Flux.1（11B 文生图）初始化 T2V 模型**（即便是蒸馏模型也有效）。自编码器先用 **HunyuanVideo VAE（4×8×8）**，后自研 **Video DC-AE（4×32×32 高压缩，128/256 通道，EfficientViT block + pixel-shuffle 残差）**——5s/24fps/768px 视频 token 数从 76K 降到 19K，训练吞吐 ×5.2、推理 >10×；patch size=1（Sana 启发，不再 patch）。

## 数据

### Open-Sora Plan v1.3（2412.00131，Tab.4 data card）
- **图像 ~18M**：SAM 11.1M（caption=LLaVA）、Anytext 1.8M（OCR，过滤英文约半）、Human-images 0.1M（从 Laion-5B 挑 160k 高分辨率/高美学/无水印/有人物）、Internal 5.0M。
- **视频 ~24.8M**：Panda70M 子集 21.2M（横屏，caption=QWen2-VL/ShareGPT4Video）、VIDAL 2.8M（YouTube Shorts 竖屏）、StockVideo 0.8M（Mixkit/Pexels/Pixabay，CC0 无水印）。
- **数据清洗管线**（Tab.5 各步保留率）：视频切 16s 片 → **LPIPS 跳变检测**（去 jump cut，保留 97%，z 阈值 2.0/3.2）→ 运动计算 + OCR 字幕检测（边缘最多裁 20%）→ **美学过滤 Laion Aesthetic v2 阈值 4.75（剔约 40%，降到 49%）** → **DOVER 技术质量分 >0（降到 44%）** → 运动二次复核（最终约 42%）。
- **标注/re-caption**：InternVL2 + QWen2-VL-7B 生成 dense caption；早期 v1.1 用 ShareGPT4Video-7B；去掉"This image/The video"前缀。
- **Prompt Refiner**：用 GPT-4o 造 短→长 配对文本，对 **LLaMA-3.1-8B 做 LoRA（rank 64，1 epoch，bs=32，lr=1.5e-4，单卡 NPU/GPU 1 小时内完成）** 微调；训练集 COCO 12k + DiffusionDB 6k + JourneyDB 3k + Dense Captions 0.5k。解决训练用 dense caption 与用户短输入（VBench 多数 <30 词）的分布差，并支持多语→英翻译。

### HPC-AI Tech Open-Sora
- **Open-Sora 1.2**：共 **30M 视频片（2–16s，总 80k 小时）+ 约 3M 图**。来源 WebVid-10M、Panda-70M（取 20M 高质子集）、HD-VG-130M、MiraData(77k 长视频)、Vript(400k)、Inter4K、Pexels/Pixabay/Mixkit；图像 LAION（美学>6.5 子集）+ Unsplash-lite。清洗：PySceneCut 切场景 + LAION 美学 + UniMatch 光流（运动） + DBNet++/MMOCR 去多字幕；caption 用 GPT-4V + PLLaVA-13B，光流检测相机运动并追加到 caption。
- **Open-Sora 2.0**：**分层数据金字塔**（loose→strict 多级过滤构造越来越纯净的子集）。过滤器：美学/运动/模糊/OCR/相机抖动；预处理剔除 <2s、bpp<0.02、fps<16、宽高比超 [1/3,3]，按 FFmpeg 场景分切 ≤8s 片。标注：256px 用 LLaVA-Video、768px 用 **Qwen-2.5-Max**（幻觉更少）按 6 维（主体/动作/背景/光照/相机/风格）生成 caption；运动分附在 caption 后作为可控信号。训练量：256px T2V 用 70M、256px T/I2V 用 10M、768px T/I2V 用 5M。

## 训练方法

### Open-Sora Plan v1.3
- **目标**：全程 **v-prediction + zero terminal SNR**（Lin 2024）+ **min-SNR 加权 γ=5.0**；AdamW β=(0.9,0.999)。
- **多阶段渐进**（图→视频）：
  1. T2I 预训练：先在 256² 训 Full 3D Attention 约 150k 步；继承权重把 Full 3D 换成 Skiparse，调约 100k 步（bs=1024, lr=2e-5），数据 SAM+Anytext+Human-images。
  2. T2I&V 联合预训练：最大 93×640×640，约 200k 步（bs=1024, lr=2e-5），图像几乎全 SAM、视频用原始 Panda70M。
  3. T2V 微调：约 100k 步近收敛；用清洗 re-caption 后的 Panda70M + 高质数据，固定 93×352×640，30k 步 lr=1e-5，**256 NPU/GPU，总 bs=1024**。
- **WF-VAE 训练**：三阶段（25f 256² → 49f 半 FPS 增动态 → 调 λ_lpips=0.1）；首阶段 800k 步、后两阶段各 200k 步，**8 NPU/GPU**，从头训 3D 判别器。
- **I2V 控制器**：v-pred 同设置，256 NPU、bs=512，两阶段渐进 mask 难度（低分辨多简单任务 → 高分辨 I2V/转场），微调时给条件图加轻微高斯噪声增泛化。

### HPC-AI Tech Open-Sora
- **Open-Sora 1.2**：训练目标改 **rectified flow（取代 1.0/1.1 的 DDPM）**+ score condition + 多分辨率/时长/宽高比分桶（bucket）训练。
- **Open-Sora 2.0**：**flow matching**（同 SD3，预测速度 X0−X1，timestep 取 logit-normal 并按 T×H×W 缩放）。AdamW β=(0.9,0.999) ε=1e-15、无 weight decay；lr 5e-5（前 40k 步）→3e-5（后 45k）→Stage3 1e-5；grad-norm clip=1。三阶段省钱 pipeline：**(1) 256px 低分辨学运动 → (2) 低分辨 T/I2V → (3) 高分辨 I2V 微调**（发现 I2V 比 T2V 更高效地适配高分辨，因条件图让模型专注学运动）；用 Flux 初始化、PixArt 式高质数据加速。条件框架把 image/video 条件作为附加通道拼接（区别于 OS1.2 直接替换 noisy 输入），I2V 推理用解耦 CFG（g_img=3, g_txt=7.5）+ 引导振荡 + 按帧/步动态 g_img。Video DC-AE 适配用 **DINOv2 latent 蒸馏**对齐第三层 latent 加速扩散收敛。

## Infra（训练 / 推理工程）

### Open-Sora Plan
- **训练算力**：v1.3 T2V 微调 **256 NPU/GPU（华为昇腾 Ascend 910 系 / GPU），总 bs=1024**；VAE 与结构控制器仅 8 卡。v1.3 仅用 **数据并行 DP**（作者在 limitation 中坦言尚未上序列/张量并行，未来计划 DeepSpeed/FSDP Zero3 撑 10–15B、或 MindSpeed/Megatron-LM 撑 30B）。v1.5 起**全栈昇腾 + MindSpeed-MM 框架**训练推理。
- **效率 trick**：**Min-Max Token 策略**（在同一 bucket 内聚合不同分辨率/时长，保证每 global batch token 数恒定，使各卡算时几乎一致、降同步开销，且数据采样与模型代码解耦）；**自适应梯度裁剪**（按 EMA + 3-sigma 检测离群 batch 梯度，异常则置零并按 N/M 重缩放再 all-reduce，消除 loss spike 而不丢整个 iteration）。
- **推理**：v1.3 支持 **93×480p 在 24G 显存**内跑；Causal Cache 做无损分块 VAE 推理。Helios（2026）单 H100 达 **19.5 FPS** 分钟级长视频。

### HPC-AI Tech Open-Sora
- **框架 ColossalAI**（潞晨自研并行系统）+ PyTorch compile + Triton kernel。OS2.0 硬件 **H200（141GB）**；VAE 用张量并行（按通道切卷积权重），MMDiT 用 **ZeRO-DP + Context Parallelism（CP，按序列维切分）**。Stage1/2 用 DP+ZeRO-2 达 **MFU 38.19%**，Stage3 ZeRO-2+CP=4 达 **35.75%**；含 selective activation checkpointing、自动故障恢复、pinned-memory dataloader。
- **成本（OS2.0，Tab.2，按 H200 $2/卡·时）**：256px T2V（85k 步, 224 卡, 2240 GPU·天 = $107.5K）+ 256px T/I2V（13k 步, 192 卡, 384 GPU·天 = $18.4K）+ 768px T/I2V（13k 步, CP=4, 192 卡, 1536 GPU·天 = $73.7K）= **共 4160 GPU·天 / $199.6K**，比 Movie Gen（~1.25M H100·时）/ Step-Video（~500k）低 **5–10×**。
- **推理效率（OS2.0，H100/H800，50 步）**：256² 单卡 60s/52.5GB；768² 单卡 1656s、8 卡序列并行降到 276s/44.3GB。

## 评测 benchmark（把效果讲清楚）

### WF-VAE 重建（Open-Sora Plan v1.3，Tab.6/7，WebVid-10M，33f）
| Channel | 模型 | 吞吐 T↑ | 显存↓(GB) | PSNR↑ | LPIPS↓ | rFVD↓ |
|---|---|---|---|---|---|---|
| 4 | CV-VAE | 1.85 | 25.00 | 30.76 | 0.0803 | 369.23 |
| 4 | OD-VAE | 2.63 | 31.19 | 30.69 | 0.0553 | 255.92 |
| 4 | Allegro | 0.71 | 54.35 | 32.18 | 0.0524 | 209.68 |
| 4 | **WF-VAE-S** | **11.11** | **4.70** | 31.39 | 0.0517 | 188.04 |
| 4 | **WF-VAE-L** | 5.55 | 7.00 | 32.32 | 0.0513 | **186.00** |
| 16 | CogVideoX | 1.02 | 35.01 | 35.76 | 0.0277 | 59.83 |
| 16 | **WF-VAE-L** | **5.55** | **7.00** | **35.79** | **0.0230** | **54.36** |

要点：WF-VAE-S 编码吞吐超 CV-VAE/OD-VAE 约 6×/4×、显存降约 5×/7×；WF-VAE-L 超 Allegro 7.8× 吞吐、显存约 1/8。**Causal Cache 分块推理 PSNR/LPIPS 与直接推理数值完全相同（OD-VAE 分块掉 1.8 dB）**。

### T2V（Open-Sora Plan v1.3，VBench + ChronoMagic-Bench-150，Tab.8）
仅选 VBench 的 Object Class / Human Action / Multiple Objects / Aesthetic / Spatial / Scene 等维度（作者认为 VBench 多数指标饱和、参考价值低），运动维度改用 ChronoMagic（GPT4o-MTScore）。列序与 Tab.8 一致（"CH GPT4o" 为 ChronoMagic 的 GPT4o 一致性分）：

| 模型 | Size | Aesthetic | Object Class | Action | Multiple Obj | CH GPT4o | Spatial | Scene | MTScore |
|---|---|---|---|---|---|---|---|---|---|
| OpenSora v1.2 | 1.2B | 56.18 | 85.8 | 83.37 | 67.51 | 42.47 | 58.41 | 51.87 | 2.50 |
| CogVideoX-2B | 1.7B | 58.78 | 89.0 | 78.00 | 53.91 | 38.59 | 48.48 | 38.60 | 3.09 |
| CogVideoX-5B | 5.6B | 56.46 | 77.2 | 76.85 | 45.89 | 41.44 | 46.43 | 48.45 | 3.36 |
| Mochi-1 | 10.0B | 56.94 | 94.6 | 86.51 | 69.24 | 36.99 | 50.47 | 28.07 | **3.76** |
| **OpenSoraPlan v1.3** | 2.7B | 59.00 | 81.8 | 70.97 | 44.46 | 28.56 | 35.87 | **71.00** | 2.64 |
| **OpenSoraPlan v1.3\*** | 2.7B | **60.70** | 86.4 | **84.72** | 49.63 | 52.92 | 44.57 | 68.39 | 2.95 |

（\* = 用 prompt refiner。）要点：v1.3 在美学、scene 还原上领先（Scene 71.00 远超对手），但单/多物体与动作语义遵循未用 refiner 时偏弱；prompt refiner（v1.3*）让人体动作/空间关系提升 >5%、单/多物体语义遵循 +15%/+10%、场景生成 +25%（作者原文表述，对应 480p 评测）。运动幅度（MTScore 2.64/2.95）仍弱于 Mochi-1（3.76）/CogVideoX（3.09/3.36），是其已知短板。

### HPC-AI Tech Open-Sora 2.0（11B，2503.09642）
- **VBench（图 10，Total Score）**：OpenAI Sora 85.5 居首；**Open-Sora 2.0 把对 Sora 的差距从 1.2 时的 4.52% 压到 0.69%**（论文正文原话，对应 Total≈84.9），且 VBench 分数高于 CogVideoX1.5-5B 与 HunyuanVideo（图中 HunyuanVideo 83.2 / CogVideo 81.3 / Open-Sora 1.2 79.8）。注：图 10 为图像，各模型 Total/Quality/Semantic 的精确小数无法从文字层逐一核出，此处仅保留正文可验证的"gap 0.69%、超 HunyuanVideo 与 CogVideoX1.5-5B"。
- **人评（图 1，100 prompt 覆盖 视觉质量/prompt 遵循/运动质量 三维；每模型单次推理、不 cherry-pick）**：以 win-rate（偏好率）对多个顶尖模型（Runway Gen-3 Alpha、Luma Ray2、Vidu-1.5、Hailuo 等）作对比，论文结论为"在三维上均表现 favorably"，与 HunyuanVideo 11B / Step-Video 30B 持平（README 表述为 on-par）。注：原文未披露评测人数/是否盲评，此处不再臆测。
- **Video DC-AE 重建（Tab.1，256px）**：4×32×32、128ch：LPIPS 0.051 / PSNR 30.538 / SSIM 0.863；256ch：0.049 / 30.777 / 0.872，逼近 HunyuanVideo VAE（4×8×8：0.046 / 30.240）但 token 数大降。

## 创新点与影响
**核心贡献**
- **Open-Sora Plan**：WF-VAE（小波能量流 + Causal Cache 无损分块）、Skiparse Attention（介于 2+1D 与 Full 3D 之间、AD_avg 度量稀疏-密集差距）、统一 inpainting 式 I2V/转场/续写条件控制、加法式轻量结构控制器、Min-Max Token 分桶 + 自适应梯度裁剪 + LoRA prompt refiner 等可复用工程策略；坚持华为昇腾 NPU 全栈训练（国产算力闭环样本）。
- **HPC-AI Tech Open-Sora**：STDiT 时空解耦、2D→3D VAE 知识迁移、rectified flow/score condition、**Video DC-AE 高压缩**，以及最具影响力的 **Open-Sora 2.0「$200K 训出商业级 11B 视频模型」的全成本拆解**——证明顶级视频模型训练成本高度可控，并完全开源 checkpoint + 训练代码 + 数据管线。

**对后续工作的影响**：作为最早一批 Sora 开源复现，两线显著降低了视频生成的入门门槛，直接孵化 [[allegro]]（沿用 OSP v1.2.0 的 VideoDiT 架构）等下游；其数据清洗管线、多分辨率分桶、causal 3D VAE、prompt refiner 已成为开源视频生成的"标配模板"。Open-Sora 2.0 的成本核算成为后续低成本视频训练的常引基准。

**已知局限**（作者自述）
- Open-Sora Plan v1.3 的 2B 去噪器训练后期**性能饱和**，**物理规律理解差**（牛奶溢杯、行走等）；归因于「图文联合从头训、视频数据仅 10M 级别不足」「模型需继续 scale（5B 比 2B 更懂物理）」「v-pred vs flow matching 待消融」。Panda70M 域窄（采样 2000 条中行走视频 <10 条、约 80% 是多人半身对话），数据多样性不足。Skiparse 加速仅在 ≥480p 长序列才显著，多数低分辨预训练阶段收益有限；v1.3 仅用 DP 无序列/张量并行。缺音频等跨模态。
- Open-Sora 2.0 因算力约束**未完全收敛**（高压缩 AE 版 loss 0.5 vs 原始 0.1），高压缩 Video DC-AE 会拖慢扩散收敛（通道增大需更多数据）。

## 原始链接
- arxiv (Open-Sora Plan v1.3): https://arxiv.org/abs/2412.00131
- arxiv (WF-VAE): https://arxiv.org/abs/2411.17459
- arxiv (HPC-AI Open-Sora 1.2): https://arxiv.org/abs/2412.20404
- arxiv (HPC-AI Open-Sora 2.0): https://arxiv.org/abs/2503.09642
- github (PKU-YuanGroup): https://github.com/PKU-YuanGroup/Open-Sora-Plan
- github (HPC-AI Tech): https://github.com/hpcaitech/Open-Sora
- hf (OSP v1.3): https://huggingface.co/LanguageBind/Open-Sora-Plan-v1.3.0
- hf (OSP v1.5): https://huggingface.co/LanguageBind/Open-Sora-Plan-v1.5.0
- hf (Open-Sora v2): https://huggingface.co/hpcai-tech/Open-Sora-v2
- modelscope (Open-Sora v2): https://modelscope.cn/models/luchentech/Open-Sora-v2
- 后续 (Helios, 2026): https://github.com/PKU-YuanGroup/Helios （arXiv 2603.04379）

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2412.00131.pdf （Open-Sora Plan v1.3 技术报告）
- ../../../sources/omni/2024/arxiv-2411.17459.pdf （WF-VAE 论文）
- ../../../sources/omni/2024/arxiv-2412.20404.pdf （HPC-AI Open-Sora 1.2 技术报告）
- ../../../sources/omni/2024/arxiv-2503.09642.pdf （HPC-AI Open-Sora 2.0 技术报告）
- ../../../sources/omni/2024/open-sora-plan--readme.md （PKU-YuanGroup README，含全版本时间线）
- ../../../sources/omni/2024/open-sora-hpcai--readme.md （hpcaitech README，含成本/VBench/推理效率表）
