---
title: "视频生成族横向对比（Sora · Veo · Wan · Movie Gen · HunyuanVideo · Kling · CogVideoX 及其谱系）"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [video-generation, text-to-video, image-to-video, diffusion-transformer, flow-matching, 3d-vae, vbench, sora, veo, wan, movie-gen, hunyuanvideo, kling, cogvideox, deep-dive]
---

# 视频生成族：从级联像素扩散到流匹配 DiT，再到音视频联合与自回归世界模型

> 本页是 omni 调研里"视频生成"这一族的横向综述，串起 2022→2026 的主干工作。每条硬数据都引自对应单工作页（[[slug]] 内链，slug=文件名去 `.md`），单页均已对抗式核过。脉络主线是**三次架构换挡**：① 级联像素扩散 / 离散 token（2022）→ ② 在预训练图像扩散上"加时间层"的潜空间 U-Net 视频扩散（2023）→ ③ 3D-VAE + DiT + Flow Matching 的端到端长视频生成（2024 至今），并在 2025 起分叉出**原生音视频联合生成**（Veo 3 / Sora 2 / Seedance）与**分块自回归世界模型**（MAGI-1 / SkyReels-V2 / Cosmos）两条新支线。

---

## 0. 一句话地图

- **范式奠基（2022）**：Google [[imagen-video]]（7 子模型级联、11.6B、像素空间）与 Meta [[make-a-video]]（伪 3D 因子化、UCF-101 零样本 FVD 367.23）确立"复用 T2I 先验 + 时空因子化"扩散路线；[[phenaki]]（C-ViViT + MaskGIT）开离散 token + 变长 story 视频先河；[[cogvideo]]（9.4B 自回归、首个开源 T2V）是 [[cogvideox]] 的源头。
- **潜空间 U-Net 视频扩散（2023）**：NVIDIA [[align-your-latents-vldm]] 提出"冻结空间层、只训时间层"的 Video LDM 范式（驾驶场景 FVD 356），其一二作随后在 Stability AI 工程化为 [[stable-video-diffusion]]（UCF-101 零样本 FVD 242.02，人评胜 Gen-2/Pika）；[[animatediff]] 把运动模块做成即插即用插件，长成开源生态基础设施。
- **DiT 大爆发（2024）**：OpenAI [[sora]] 用"时空潜 patch + DiT"点燃军备竞赛（无任何官方 benchmark）；开源侧 [[cogvideox]]（5B，Expert AdaLN + 3D 全注意力）、[[hunyuan-video]]（13B，发布时最大开源 T2V，建 T2I→T2V scaling law）、[[movie-gen]]（30B，LLaMa3 骨干 + Flow Matching，对 Sora 净胜 +8.2%）三足鼎立；[[mochi-1]] / [[ltx-video]] / [[allegro]] / [[open-sora-plan]] 撑起"可单卡跑"的开源长尾；商用 [[kling]] / [[gen-3-alpha]] / [[veo-2]] 各据一方。
- **2025+ 三条新主线**：
  1. **流匹配 DiT 集大成 + 消费级部署**：阿里 [[wan-2-1]]（VBench 86.22% 登顶超 Sora）→ [[wan-2-2]]（首个视频扩散 MoE，27B 总 / 14B 激活，4090 可跑 720p）；腾讯 [[hunyuanvideo-1-5]]（8.3B dense，SSTA 稀疏注意力，4090 峰显存 13.6GB）。
  2. **原生音视频联合**：Google [[veo-3]]（首个旗舰原生同步音频）、OpenAI [[sora-2]]（"GPT-3.5 时刻"）、字节 [[seedance-1-0]]→[[seedance-2-0]]（Arena T2V/I2V 双榜第一，双声道音频）。
  3. **分块自回归 / 世界模型**：[[magi-1]]（24B chunk-wise AR，Physics-IQ V2V 56.02 碾压）、[[skyreels-v2]]（扩散强制无限长，VBench 83.9%）、[[framepack]]（6GB 显存出 1800 帧）、NVIDIA [[cosmos-predict]]（物理 AI 世界模型，10000×H100·3 个月）。

---

## 1. 架构演进：三次换挡

### 1.1 第一代（2022）——级联像素扩散 / 离散 token，跨模型拼接

2022 年的共识是"视频太高维、(text,video) 配对太稀缺"，因此设计都围绕**省算力 + 借 T2I 先验**：

- **像素空间级联**：[[imagen-video]] 用 **7 个视频扩散子模型（base + 3 SSR + 3 TSR，共 11.6B）**，从 16×40×24@3fps 一路超分到 128×1280×768@24fps（≈5.3s）；冻结 T5-XXL（4.6B）注入全部 7 个模型。它验证了两条对后续普适的结论：**v-prediction 在高分辨率/视频上显著优于 ε-prediction**（避免跨帧色漂、FID 收敛更快），以及**带 guidance 的 progressive distillation**——蒸馏到每级 8 步后整条级联从 618s 降到 35s（约 18× 快、按 FLOPs 36×）。
- **伪 3D 因子化**：[[make-a-video]] 在 DALL·E-2 式 T2I 上堆 **1D 时间卷积（初始化为恒等）+ 时间注意力（投影初始化为零）**，做到"加时间维但初始行为不变"；最大卖点是**完全不用配对文本-视频数据**（用配对图文学外观、用无标注视频学运动），UCF-101 零样本 FVD 367.23、微调 81.25 取得 SOTA，MSR-VTT 零样本 FID 13.17 大幅超 CogVideo（23.59）。
- **离散 token + 掩码生成**：[[phenaki]] 的 **C-ViViT** 时空因果 tokenizer（首帧独立编码 + 时间维 causal attention）把 10 帧 token 从 2560 压到 1536、Moments-in-Time 重建 FVD 65.78 碾压逐帧 ViT-VQGAN 的 166.6；配 **MaskGIT 并行掩码生成**（12–48 步），1.8B 生成 1024 帧仅 4.1 分钟（TATS 需 30 分钟）。它首创"末 K 帧续生 + 换 prompt"的**变长 story 视频**范式。
- **自回归 Transformer**：[[cogvideo]]（9.4B，60 亿冻结自 CogView2）用 **dual-channel attention**（冻结空间通道 + 新增可训时序通道 + 共享 FFN + α 软融合）+ **多帧率分层训练** 修复"固定切片破坏文本-动作对齐"，是据作者所称的首个开源大规模 T2V；UCF-101 FVD 626、人评 49.53% 评测者选其最佳。

### 1.2 第二代（2023）——Video LDM：冻结空间层、只训时间层

[[align-your-latents-vldm]]（NVIDIA/LMU，CVPR 2023）把战场从像素空间搬进 LDM 潜空间，奠定影响最深的范式：

- **解耦空间/时间**：把视频当 B·T 帧塞进 batch 维过**冻结的图像 LDM 空间层**，只插入并训练**时间对齐层**（temporal attention + 3D 卷积 residual，时间核 3,1,1），用可学习系数 α 融合（推理令 α=1 即退回原图像模型）；文生视频版直接把 Stable Diffusion 变成 T2V，总参 ~4.1B 但仅 ~2.7B 在视频上训练，远小于 Imagen Video(11.6B)/CogVideo(9B)。
- **decoder 视频微调是关键**：加 3D 卷积时间判别器后，RDS 重建 FVD 从 390.88 暴降到 **7.61**（数量级提升）。
- **工程化为开源底座**：同作者（Blattmann/Rombach）随后在 Stability AI 做出 [[stable-video-diffusion]]——把训练显式拆成**三阶段（图像预训练→视频预训练→高质量微调）**，并用 Elo 人评消融出一套视频数据 curation（cut detection + 三路合成字幕 + 光流/OCR/CLIP/美学过滤），把 580M LVD 精炼到 152M LVD-F，证明"小而精胜大而杂"；UCF-101 零样本 FVD 242.02、I2V 人评胜闭源 Gen-2/Pika。
- **即插即用运动模块**：[[animatediff]] 在冻结 SD1.5 上插一支时序 Transformer（v1 运动模块 417M），训一次即可驱动社区任意个性化 T2I 出动画；配 **Domain Adapter**（LoRA 吸收 WebVid 的水印/模糊画质域差）与 **MotionLoRA**（20–50 段视频、~30M 存储学一种镜头运动）。它是 ComfyUI/WebUI 开源视频生态的基石。

### 1.3 第三代（2024 至今）——3D-VAE + DiT + Flow Matching

[[sora]]（2024-02）把 LLM 配方搬进视频：先用 VAE 压成潜空间，再分解为**时空潜 patch（spacetime latent patches）**当 DiT token，**单模型覆盖任意时长/分辨率/宽高比**（图像=单帧视频，最高 2048×2048 单帧），并提出"视频生成 = 世界模拟器"叙事。但 Sora 技术报告**明确不含实现细节**（参数量、tokenizer、text encoder 全未披露，无任何 FID/VBench 数字），真正把这套配方"抠到数字"的是随后的开源/工业报告：

**3D-VAE（视觉 tokenizer）的压缩比之争**——决定送进 DiT 的 token 数，是成本与质量的命门：

| VAE | 时空压缩(t×h×w) | latent 通道 | 像素→token 比 | 出处 |
|---|---|---|---|---|
| SVD（复用 SD2.1 2D VAE） | 1×8×8（逐帧） | 4 | — | [[stable-video-diffusion]] |
| CogVideoX 3D 因果 VAE | 4×8×8 | 16 | 1:48 | [[cogvideox]] |
| HunyuanVideo Causal 3D VAE | 4×8×8 | 16 | 1:48 | [[hunyuan-video]] |
| Movie Gen TAE（2.5D inflate） | 8×8×8 | 16 | 1:96 | [[movie-gen]] |
| Wan-VAE（127M，RMSNorm+feature cache，支持无限长流式） | 4×8×8 | 16 | — | [[wan-2-1]] |
| Wan2.2-VAE（叠 patchify 到 4×32×32） | 4×16×16 | — | — | [[wan-2-2]] |
| HunyuanVideo 1.5 VAE | 4×16×16 | 32 | — | [[hunyuanvideo-1-5]] |
| LTX-Video VAE（patchify 前移进 VAE） | 8×32×32 | 128 | **1:8192** | [[ltx-video]] |
| Seedance 1.0 VAE（去 DiT patchify） | 4×16×16 | 48 | — | [[seedance-1-0]] |
| Mochi AsymmVAE | 6×8×8 | 12 | — | [[mochi-1]] |
| MAGI-1 Transformer-VAE（纯 ViT，解码 12.28ms 最快） | 4×8×8 | 16 | — | [[magi-1]] |
| Cosmos Tokenizer（wavelet + FSQ 离散，词表 64000） | 8×8×8 / 8×16×16 | 16 / 6维 | — | [[cosmos-predict]] |

关键趋势：从"复用图像 2D VAE 逐帧编码"（SVD，省事但闪烁）→"从零训 3D 因果 VAE"（CogVideoX/HunyuanVideo，时空联合压缩、抑闪烁、重建 PSNR 全面更高，HunyuanVideo VAE ImageNet 33.14 dB 超 FLUX-VAE 32.70）→"极致高压缩"（[[ltx-video]] 把 patchify 前移到 VAE 做到 1:8192 像素-token 比，是同类 2 倍压缩、4 倍 token 比，2 秒在 H100 出 5 秒视频）。[[cogvideox]] 实测更激进的 16×16×8 压缩难收敛，[[open-sora-plan]] 的 Video DC-AE（4×32×32）在算力受限下扩散收敛被拖慢（loss 0.5 vs 原始 0.1），印证"压缩比 ≠ 越高越好"。

**DiT 骨干的三种文本融合方式**：

- **Cross-attention 注文本**（Wan / LTX-Video / Allegro / Cosmos）：文本 token 不进自注意力，长上下文下指令跟随稳；[[wan-2-1]] 还用**全共享 AdaLN**（所有 block 共享一个 MLP 预测 6 个调制参数）省约 25% 参数，消融证明"参数投在网络深度比投在 AdaLN 上更划算"。
- **双流→单流 MMDiT**（HunyuanVideo / Mochi / Open-Sora 2.0，借鉴 FLUX）：视频/文本 token 先各自走双流 block 学各自 modulation，再 concat 进单流 block 联合注意力；[[mochi-1]] 改成"不对称"——视觉流隐维 3072、文本流 1536（视觉流参数约 4× 文本流），用非方阵 QKV 省显存。
- **Expert AdaLN**（[[cogvideox]]）：文本/视频拼接但各设 Vision/Text Expert AdaLN 调制，用远少于 MMDiT 的参数对齐两模态特征空间。

**注意力：3D 全注意力 vs 时空分离 vs 稀疏**。CogVideoX 实测 **3D 全注意力**优于 2D+1D 分离（后者在 5B 规模训练易崩溃、大运动一致性差）；HunyuanVideo/Wan/Mochi/Allegro 均用全注意力。但全注意力对 token 数平方复杂度，催生稀疏化：[[hunyuanvideo-1-5]] 的 **SSTA（选块 + 滑窗双机制、无参数）** 在 10s/720p 端到端相对 FlashAttention-3 加速 1.87×（241 帧每步 5.51s→2.95s）；[[seedance-1-0]] 用"解耦空间/时间层 + 时间层窗口注意力"降开销；[[open-sora-plan]] 的 **Skiparse Attention**（Single/Group Skip 交替）把复杂度降到 1/k（k=4）。

**Text encoder 的换代**：早期统一用 T5-XXL（Imagen Video/LTX-Video/Allegro/CogVideoX/Mochi/Cosmos）或 umT5（Wan，因多语种 + "画面内文字"理解强，消融训练 loss 低于 Qwen2.5-7B/GLM-4-9B）；2024 末起转向 **decoder-only MLLM**——HunyuanVideo 用预训练 MLLM + 双向 token refiner 替代 T5/CLIP，[[hunyuanvideo-1-5]] 用 **Qwen2.5-VL（语义）+ Glyph-ByT5（视频内文字字形）** 双通道，[[seedance-1-0]] 用微调 decoder-only LLM。

---

## 2. 训练目标：从 DDPM/EDM 到 Flow Matching 的全面转向

- **DDPM / v-prediction**（2022–2023 主流）：Imagen Video（v-pred）、Make-A-Video（像素 DDPM）、CogVideoX（v-prediction + zero-SNR）、Open-Sora Plan v1.3（v-pred + zero-terminal-SNR + min-SNR γ=5.0）。
- **EDM**（连续噪声）：[[stable-video-diffusion]]（从 SD2.1 离散迁到 EDM，高分辨率/强条件时把噪声调度右移）、[[cosmos-predict]]（EDM score matching + 不确定性逐噪声级加权，论文明言与 flow matching 理论等价）。
- **Flow Matching / Rectified Flow**（2024 末起全面主导）：[[movie-gen]] 大规模验证其相对扩散质量 +16.5%/文本对齐 +7.1%；[[hunyuan-video]] / [[wan-2-1]] / [[wan-2-2]] / [[goku]] / [[ltx-video]] / [[seedance-1-0]] / [[skyreels-v2]] / [[magi-1]] / [[hunyuanvideo-1-5]] 全部采用，统一形态是"线性插值 xt=t·x1+(1−t)·x0、预测速度场、timestep 取 logit-normal"。[[goku]] 给了最干净的对照证据：ImageNet-1K 上 RF 40 万步即达 DDPM 100 万步的 FID 档（2.157 vs 2.257）。

**渐进式多阶段训练**几乎是标配：先低分辨率 T2I 打底（学文-图语义对齐与几何），再图-视频联合、分辨率/时长逐级上调。典型如 [[cogvideox]] 四阶段（256→480→768px，10s）、[[hunyuanvideo-1-5]] 六阶段（256p 图 50 亿 → 720p 24fps 视频）、[[wan-2-1]] 三阶段课程。[[hunyuan-video]] 还发现直接在 512px 微调会劣化 256px 生成，故提 **mix-scale training**。

**偏好对齐（视频 RLHF）的兴起**——2025 起从"靠高质量 SFT + 模型平均"升级为显式 RL：

- [[movie-gen]] **不做 RLHF**，靠高质量 SFT 数据 + 人评筛 + Model Averaging。
- [[seedance-1-0]] 是视频 RLHF 的代表：**三专门奖励模型（Foundational/Motion/Aesthetic）+ 直接最大化复合奖励**（论文称比 DPO/PPO/GRPO 更高效）+ 多轮 RM-扩散迭代 + 对加速后 refiner 也做 SR-RLHF。
- [[hunyuanvideo-1-5]] 做 T2V/I2V 差异化对齐：I2V 用在线 **MixGRPO**（混合 ODE-SDE 求解器）+ VLM 四维奖励，T2V 先离线 DPO 再在线 RL。
- [[skyreels-v2]] 专攻运动质量：半自动偏好数据（对真视频施加渐进失真造 rejected）+ BTT 奖励模型 + 三阶段 **Flow-DPO**。

**蒸馏与加速**几乎人手一套：Imagen Video 的 progressive distillation（8 步、18×）；[[wan-2-1]] 的 LCM/VideoLCM 蒸到 4 步（配 Streamer 达 10–20× 加速、8–16 FPS，4090+int8+TensorRT 实时 20 FPS）；[[seedance-1-0]] 三段蒸馏（TSCD + Score Distillation + 对抗，端到端 >10×，1080p/5s 仅 41.4s@L20）；[[hunyuanvideo-1-5]] 步数蒸馏（480p I2V 8/12 步，4090 约 75s）；[[movie-gen]] 的 Linear-Quadratic schedule（50 步逼近 250 步、~20× 免训练加速），[[hunyuan-video]] 的 time-step shifting 在 10 步极低步数下更优。

---

## 3. 2025+ 三条新主线

### 3.1 流匹配 DiT 集大成 + 消费级部署（阿里 Wan / 腾讯 HunyuanVideo 1.5）

[[wan-2-1]] 是 2025 开源里程碑：Wan-VAE（127M，RMSNorm+feature cache 支持无限长 1080p 流式编解码，重建速度 2.5× HunyuanVideo VAE）+ cross-attention DiT + 全共享 AdaLN + umT5，**VBench 86.22% 登顶**（超 Sora 84.28%、HunyuanVideo 83.24%、Kling 81.85%），1.3B 小模型仅 8.19GB 显存跑 480p；还是首个能生成中英文"画面内文字"的视频模型。它演进出 [[wan-2-2]]——**首个把 MoE 引入视频扩散**：按 SNR/去噪时间步路由"高噪专家（管布局）+ 低噪专家（管细节）"两个 14B 专家（总 27B、每步激活 14B、推理成本同 14B dense），消融证明完整双专家验证损失最低；配 4×16×16 高压缩 Wan2.2-VAE + 5B dense TI2V，**单张 RTX 4090 < 9 分钟出 5 秒 720p@24fps**。

[[hunyuanvideo-1-5]] 走另一条路——**8.3B dense 而非 MoE**：靠数据策展 + SSTA 稀疏注意力 + glyph-aware 双语文本编码 + Muon 优化器（来自 Kimi K2，半数训练步达更低 loss）+ 级联超分到 1080p，把"逼近闭源 + 消费级可跑"统一（720p 121 帧峰显存 13.6GB / 4090 可跑）。GSB 上 T2V 对 Wan2.2 净胜 +17.1%、I2V +12.7%，但对 Veo3 仍 −10.32%（落后顶级闭源）。

### 3.2 原生音视频联合生成（Veo 3 / Sora 2 / Seedance）

2024 旗舰几乎都"只出画面不出声"，音频靠后期或独立配音模型（如 [[movie-gen]] 的 13B V2A 用 DiT + DAC-VAE 单独训）。2025 的范式跃迁是**单模型一次生成画面 + 对白 + 音效 + 环境音且时间对齐**：

- [[veo-3]]（Google，2025-05 I/O）首发"Video, meet audio"——首个旗舰原生同步音频 + 精准对口型（lip sync），输出 4/6/8s、720p/1080p（3.1 增 4k）；架构/数据/训练全闭源（无论文/model card），仅家族旁证为"latent diffusion + transformer 去噪、音视频 latent 联合扩散"。
- [[sora-2]]（OpenAI，2025-09）自比"GPT-3.5 时刻"，强调物理一致性（投篮不中会真实反弹、能"模拟失败"）、cameo 角色注入、跨多镜头世界状态一致；同样零方法透明度，唯一定量数字是系统卡的安全评测（如成人内容输出端 not_unsafe 96–98%）。
- [[seedance-1-0]]（字节，2025-06）以**单一统一模型**做 T2V+I2V+原生多镜头，2025-06-10 在 Artificial Analysis **T2V/I2V 双榜同时登顶**（I2V 较 Veo 3/Kling 2.0 领先 100+ Elo）；[[seedance-2-0]]（2026-02）升级为**统一多模态音视频联合**（单次最多 9 图+3 视频+3 音频参考、双声道音频），Arena T2V Elo 1450、I2V 1449 双榜第一，且用 720p 击败对手 1080p 输出——但 2.0 报告"评测+能力为主、架构/数据/训练全未披露"。

闭源商业线 [[kling]]→[[kling-2]]（2.0 提 MVL 多模态视觉语言交互、多模态视频编辑；2.5 Turbo 文生视频对 Veo3-fast 胜负比 212%）→[[kling-3-0]]（2026-02，原生音频 + 智能多镜头 + 角色参考，All-in-One 统一框架）持续迭代，但全程无技术报告，评测多为内部 GSB 胜负比。

### 3.3 分块自回归 / 世界模型（MAGI-1 / SkyReels-V2 / FramePack / Cosmos）

主流双向全序列去噪不适合流式/长视频（峰值显存随时长涨、忽视因果），2025 起的反向探索：

- [[magi-1]]（Sand AI，24B）**分块自回归扩散**：视频切成 24 帧/秒的 chunk，"越往后噪声越大"单调去噪，前 chunk 去噪到一定程度即流水线启动下一 chunk（最多 4 并行），**峰值开销与视频时长无关**；统一 T2V/I2V/续帧仅靠"干净 chunk 占比"区分。VBench-I2V 总分 89.28 排第一、**Physics-IQ V2V 模式 56.02 碾压**（VideoPoet 29.5、Sora 10.0），定量验证"自回归利于因果/物理建模"。配自研 MagiAttention（FFA + 零冗余通信）。
- [[skyreels-v2]]（昆仑万维）把全序列扩散**微调成扩散强制（Diffusion Forcing）模型**做"理论无限长"视频（吸收 AR-Diffusion 非递减约束把搜索空间从 O(1e48) 砍到 O(1e32)），直接复用 [[wan-2-1]] 的 VAE/text encoder；配镜头语言结构化 captioner SkyCaptioner-V1 + 运动质量 Flow-DPO，VBench 总分 83.9%（开源最高），单 prompt 生成 >30s。
- [[framepack]]（Stanford/MIT，ControlNet 作者）不训新基座，在 HunyuanVideo/Wan 上加"帧上下文打包"——按时间邻近度对历史帧渐进压缩（改 patchify 3D 卷积核），使上下文收敛到**与视频长度无关的固定上限**（流式 O(1)），13B 模型在 **6GB 笔记本显存**出 1 分钟 1800 帧；配"规划端点/反向采样/历史离散化（K=128）"三招防漂移。
- [[cosmos-predict]]（NVIDIA）把视频生成做成**物理 AI 世界基础模型**：一次开源数据策展管线 + wavelet/FSQ 因果 tokenizer + 扩散(7B/14B DiT) 与自回归(4B/12B GPT) 双路线 + 下游 post-training；**10000 张 H100 训约 3 个月、预训练约 9000T token / 2000 万小时视频**；自建 3D 一致性与物理对齐 benchmark（而非 FID/美学），并发现"更大模型在物理对齐上并不更好"。

---

## 4. 横向对比总表

> 规格/参数/指标均引自对应单工作页；"—"表示该工作页明确标注未披露。VBench 为各页报告的 Total Score；多数闭源商业模型只给内部胜负比/Arena Elo，无公开自动指标。

| 模型 | 时间 | 机构 | 架构 / 目标 | 参数 | tokenizer 压缩 | 时长·分辨率 | 关键指标（引自单页） | 开放 |
|---|---|---|---|---|---|---|---|---|
| [[cogvideo]] | 2022-05 | 清华/BAAI | 自回归 Transformer + dual-channel | 9.4B(1.7B 可训) | VQVAE 逐帧 | 4s·160→480p | UCF FVD 626 / IS 50.46；人评 49.53% 最佳 | 开源 |
| [[make-a-video]] | 2022-09 | Meta | 像素级联扩散 + 伪3D | —(未披露) | — | 76 帧·768² | UCF 零样本 FVD 367.23；MSR-VTT FID 13.17 | 闭源 |
| [[imagen-video]] | 2022-10 | Google | 7 子模型级联像素扩散 / v-pred | 11.6B | — | 128 帧·1280×768·24fps | 蒸馏 8 步 35s（18×）；无外部横评 | 闭源 |
| [[phenaki]] | 2022-10 | Google | C-ViViT + MaskGIT 离散 token | 1.8B | C-ViViT 时空因果 | 变长(数分钟)·128² | MiT 重建 FVD 65.78；1024 帧 4.1min | 闭源 |
| [[align-your-latents-vldm]] | 2023-04 | NVIDIA/LMU | Video LDM(冻空间训时间) | ~4.1B(2.7B 训) | SD VAE 逐帧 | 113 帧·1280×2048 | 驾驶 FVD 356；UCF 零样本 FVD 550.61 | 闭源 |
| [[animatediff]] | 2023-07 | CUHK/上海AI Lab | SD1.5 + 即插即用运动模块 | 运动模块 417M/453M | SD VAE | 16 帧·256/512/1024 | CLIP domain 87.29 / smooth 98.00 | 开源 |
| [[stable-video-diffusion]] | 2023-11 | Stability AI | Video LDM 三阶段 + EDM | 1.5B(U-Net) | SD2.1 VAE 逐帧 | 14/25 帧·576×1024 | UCF 零样本 **FVD 242.02**；人评胜 Gen-2/Pika | 开源 |
| [[sora]] | 2024-02 | OpenAI | 时空潜 patch + DiT / 扩散 | —(未披露) | —(VAE 时空压缩) | ≤60s·≤1080p | **无任何官方 benchmark** | 闭源 |
| [[kling]] | 2024-06 | 快手 | DiT + 自研3D VAE + 时空全注意力 | —(未披露) | 3D VAE | ≤2min·30fps·1080p | AA Arena ELO 1000(1.6 Pro 图生视频登顶) | 闭源 |
| [[gen-3-alpha]] | 2024-06 | Runway | DiT 视频(闭源) | — | — | — | 无官方数字 | 闭源 |
| [[cogvideox]] | 2024-08 | 智谱/清华 | DiT + Expert AdaLN + 3D 全注意力 / v-pred | 5B/2B | 3D 因果 4×8×8 | 10s·768×1360·16fps | VBench Human Action 96.8；人评胜 Kling 2.74 vs 2.17 | 开源 |
| [[allegro]] | 2024-10 | Rhymes AI | VideoDiT + T5 + 3D 全注意力 / 扩散 | 2.8B | 自训 4×8×8 | 88 帧·720p·15fps | **VBench 81.09**（开源 SOTA，美学第一）；单卡 9.3GB | 开源 |
| [[mochi-1]] | 2024-10 | Genmo | AsymmDiT(非对称 MMDiT) / flow 类 | 10B | AsymmVAE 6×8×8 | 5.4s·480p·30fps | 无绝对数字（VLM-judge/Elo 图未落地） | 开源(Apache2) |
| [[movie-gen]] | 2024-10 | Meta | **LLaMa3 骨干** + Flow Matching | 30B(视频)+13B(音频) | TAE 8×8×8 | 16s·1080p·含音频 | 对 Sora **净胜 +8.2%**、Runway +35.0%、与 Kling1.5 持平 | 闭源 |
| [[ltx-video]] | 2024-11 | Lightricks | DiT + cross-attn / Rectified Flow | 1.9B(13B 后续) | **8×32×32(1:8192)** | 5s·768×512(实时) | t2v 人评胜率 85%（vs CogVideoX-2B/PyramidFlow） | 开源 |
| [[open-sora-plan]] | 2024-12 | 北大/潞晨 | DiT(WF-VAE/Skiparse；OS2.0 MMDiT) | 2.7B/8B / 11B | WF-VAE 4×8×8 / DC-AE 4×32×32 | 多档 | OS2.0 VBench 距 Sora gap **0.69%**；$200K 训 11B | 开源 |
| [[veo-2]] | 2024-12 | Google DeepMind | latent diffusion(闭源) | — | — | 8s·720p(演示 4K/分钟) | MovieGenBench 人评偏好/prompt 跟随居首 | 闭源 |
| [[hunyuan-video]] | 2024-12 | 腾讯 | 双流→单流全注意力 DiT + MLLM / Flow | 13B | Causal 3D 4×8×8 | 5s·720p | 人评整体满意度第一 41.3%（超 Gen-3/Luma）；建 T2I→T2V scaling law | 开源 |
| [[cosmos-predict]] | 2025-01 | NVIDIA | DiT + AR 双路线 / EDM·next-token | 4B–14B | wavelet+FSQ 8×8×8 | 物理 AI 世界模型 | 3D 一致性超真实视频；Physics 对齐 benchmark | 开放权重 |
| [[goku]] | 2025-02 | 字节/港大 | 全注意力 DiT / **Rectified Flow** | 2B/8B | 3D 联合 8×8×4 | 4s·720p | VBench **84.85**；GenEval 0.76†；UCF FVD 217.24 | 数据集开放 |
| [[wan-2-1]] | 2025-03 | 阿里 | DiT + cross-attn + 共享 AdaLN / Flow | 1.3B/14B | Wan-VAE 4×8×8(127M) | 5s·480/720p | **VBench 86.22% 登顶**（超 Sora 84.28）；1.3B 仅 8.19GB | 开源(Apache2) |
| [[skyreels-v2]] | 2025-04 | 昆仑万维 | Diffusion Forcing(基于 Wan) / Flow | 1.3B/5B/14B | 复用 Wan-VAE | 无限长·720p | **VBench 83.9%**（开源最高）；I2V 人评开源 SOTA | 开源 |
| [[framepack]] | 2025-04 | Stanford/MIT | 帧上下文打包(基于 HunyuanVideo/Wan) | 基座 13B | 复用基座 | 1800 帧·30fps | 反向防漂移 ELO 1220；**6GB 显存出 1 分钟** | 开源 |
| [[kling-2]] | 2025-04 | 快手 | DiT + MVL(闭源) | — | — | ≤2min·1080p | 2.5T 文生视频对 Veo3-fast 胜负比 212%（内部 GSB） | 闭源 |
| [[veo-3]] | 2025-05 | Google DeepMind | latent diffusion + **原生音频**(闭源) | — | — | 4/6/8s·720p/1080p(3.1 4k) | 仅图表，无可抽取数字 | 闭源 |
| [[magi-1]] | 2025-05 | Sand AI | **分块自回归扩散** / Flow | 4.5B/24B | Transformer-VAE 4×8×8 | 流式(近30s)·恒定显存 | **VBench-I2V 89.28 第一**；Physics-IQ V2V 56.02 | 开源(Apache2) |
| [[seedance-1-0]] | 2025-06 | 字节 Seed | 解耦时空 MMDiT + 视频 RLHF / Flow | —(未披露) | 4×16×16, C=48 | 480→1080p·多镜头 | AA **T2V/I2V 双榜第一**；1080p/5s 41.4s | 闭源 |
| [[wan-2-2]] | 2025-07 | 阿里 | **视频扩散 MoE**(高/低噪双专家) / Flow | 27B 总/14B 激活；5B | Wan2.2-VAE 4×16×16 | 5s·720p@24fps | Wan-Bench 2.0 称超闭源；5B **4090 <9min** | 开源(Apache2) |
| [[sora-2]] | 2025-09 | OpenAI | 音视频联合(闭源) | — | — | 含同步音频·多镜头 | 仅安全评测数字，无生成质量 benchmark | 闭源 |
| [[hunyuanvideo-1-5]] | 2025-11 | 腾讯 | **8.3B dense** DiT + SSTA 稀疏 / Flow | 8.3B | Causal 3D 4×16×16, C=32 | 5–10s·480→1080p | GSB T2V 对 Wan2.2 **+17.1%**；对 Veo3 −10.32%；4090 13.6GB | 开源 |
| [[seedance-2-0]] | 2026-02 | 字节 Seed | 统一多模态音视频(稀疏架构) | —(未披露) | — | 4–15s·480/720p·双声道 | **Arena T2V/I2V 双榜第一**(Elo 1450/1449) | 闭源 |
| [[kling-3-0]] | 2026-02 | 快手 | 原生多模态 All-in-One(闭源) | — | — | ≤15s·原生音频·多镜头 | 无公开 benchmark | 闭源 |

---

## 5. 指标对照：VBench / FVD / 人评的横向位置

**VBench Total Score（各页报告，注意评测时间/prompt 集略有差异，仅作量级参照）**：

- Wan 2.1-14B **86.22%**（[[wan-2-1]]，超 Sora 84.28、HunyuanVideo 83.24、Kling 81.85、Gen-3 82.32、CogVideoX1.5-5B 82.17）
- Goku-T2V **84.85%**（[[goku]]，Quality 85.60 / Semantic 81.87）
- SkyReels-V2 **83.9%**（[[skyreels-v2]]，Quality 84.7% 第一、Semantic 80.8% 略逊 Wan2.1-14B 81.4%）
- Open-Sora 2.0 距 OpenAI Sora gap **0.69%**（[[open-sora-plan]]，对应 Total≈84.9，超 HunyuanVideo 83.2 / CogVideo 81.3）
- HunyuanVideo-13B 82.7%、Allegro **81.09%**（[[allegro]]，开源 SOTA，Aesthetic 63.74 全表第一）、CogVideoX-5B 80.91%

**VBench-I2V**：[[magi-1]] MAGI-1(2×decoder) **89.28 排第一**（Dynamic Degree 68.21 显著领先），亮点是"大运动幅度不掉画质"。

**UCF-101 零样本 FVD↓**（早期 T2V 的硬基准，越低越好）：SVD **242.02** < Make-A-Video 367.23 < PYOCO 355.20 < Video LDM(SD2.1) 550.61 < MagicVideo 655 < CogVideo(EN) 701.59；[[goku]] 在 128×128 设置达 FVD 217.24。

**Physics-IQ（物理对齐）**：[[magi-1]] V2V 56.02 远超 VideoPoet 29.5、I2V 模式 30.23 超 Kling1.6 23.64 / Sora 10.0——印证自回归对因果/物理建模的优势；但 [[cosmos-predict]] 反向发现"更大模型物理对齐并不更好，所有 WFM 都难严格遵守物理"。

**人评（最被各家信任的口径）**：[[movie-gen]] 对 Sora 净胜 +8.2%、与 Kling1.5 持平；[[hunyuan-video]] 1533 prompt 专业人评整体满意度 41.3% 第一（运动质量 66.5% 优势最大）；[[hunyuanvideo-1-5]] GSB 对 Wan2.2 T2V +17.1% 但对 Veo3 −10.32%（开源逼近闭源、仍差顶级）；[[seedance-1-0]]/[[seedance-2-0]] 与 Veo3/Kling 同处第一梯队并在 Arena 真人偏好双榜登顶。

---

## 6. 主线脉络小结

1. **架构收敛**：2022 的"级联像素扩散 / 离散 token / 自回归 Transformer"百花齐放，到 2024 收敛为 **3D-VAE + DiT + (Flow Matching)** 的事实标准模板（Sora 定调、HunyuanVideo/CogVideoX/Movie Gen 把数字做实）；2025 的差异化转向**注意力稀疏化（SSTA/Skiparse）、MoE（Wan2.2 按 SNR 路由）、消费级部署（4090 可跑）**。
2. **训练目标**：DDPM/v-pred（2022–23）→ EDM（SVD/Cosmos）→ **Flow Matching 一统天下**（2024 末起），并普遍叠加渐进式多阶段课程 + 视频 RLHF（Seedance/HunyuanVideo 1.5/SkyReels）+ 步数蒸馏。
3. **VAE 压缩比**是成本-质量的隐形战场：从逐帧 1×8×8 → 3D 4×8×8 → 4×16×16/4×32×32 高压缩（Wan2.2/LTX 把 token 数压到极限换实时），但 CogVideoX/Open-Sora 实证"压缩过激难收敛"。
4. **三条 2025+ 新主线**：原生音视频联合（Veo3/Sora2/Seedance2，"出声"从加分项变标配）、分块自回归世界模型（MAGI-1/Cosmos/SkyReels，攻长视频/流式/物理因果）、消费级开源（Wan/HunyuanVideo 1.5/FramePack，把 720p 长视频拉到单卡 4090 / 6GB 笔记本）。
5. **闭源 vs 开源的透明度鸿沟**：Sora/Sora 2/Veo/Kling 几乎零方法披露（只给定性演示或安全评测），而 HunyuanVideo/Wan/Movie Gen/Cosmos/MAGI-1 把数据管线、scaling law、3D/5D 并行、infra 抠到工业级颗粒度——开源报告才是这族真正"有硬数字"的知识来源。

---

## 关联页

- 上游使能方法：[[ddpm]] · [[latent-diffusion-ldm]] · [[dit-scalable-diffusion-transformers]] · [[rectified-flow]] · [[flow-matching]] · [[classifier-free-guidance]] · [[stable-diffusion-3]]（MMDiT）· [[flux-1]]（双流→单流）
- 同期图像族横向：见 omni `deep-dive/` 下其它族综述
- 全量来源索引：[[01-INDEX]]
