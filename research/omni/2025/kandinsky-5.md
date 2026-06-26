---
title: "Kandinsky 5.0: A Family of Foundation Models for Image and Video Generation"
org: "Sber AI / AIRI (Kandinsky Lab)"
country: EU
date: "2025-11"
type: tech-report
category: video
tags: [video-generation, text-to-video, image-to-video, text-to-image, image-editing, latent-diffusion, flow-matching, dit, crossdit, nabla, sparse-attention, open-source, russian]
url: "https://arxiv.org/abs/2511.14993"
arxiv: "https://arxiv.org/abs/2511.14993"
pdf_url: "https://arxiv.org/pdf/2511.14993"
github_url: "https://github.com/ai-forever/Kandinsky-5"
hf_url: "https://huggingface.co/kandinskylab"
modelscope_url: ""
project_url: "https://kandinskylab.ai/"
downloaded: [arxiv-2511.14993.pdf, kandinsky-5--techreport.txt, arxiv-2507.13546.pdf, kandinsky-5--nabla.txt, kandinsky-5--readme.md, kandinsky-5--hf-t2v-pro.md, kandinsky-5--hf-t2v-lite.md, kandinsky-5--hf-t2i-lite.md, kandinsky-5--habr.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Kandinsky 5.0 是 Sber AI（俄罗斯）开源的图像+视频生成基础模型族，统一采用「latent diffusion + Flow Matching + CrossDiT（带文本交叉注意力的扩散 Transformer）」架构，含 6 个模型（Image Lite 6B、Video Lite 2B、Video Pro 19B 三大系列，各含 T2I/T2V/I2V/编辑变体）；核心创新是自研稀疏注意力 NABLA（90% 稀疏下训练/推理 2.7× 提速且质量不掉），Video Lite 2B 在 MovieGen 人评 SBS 上视觉质量与运动动态超过 Wan 2.1 14B / Wan 2.2 A14B（参数量小 15 倍），Video Pro 在 LMArena T2V 榜登顶开源第一（2025/12/12）；全族 MIT 许可。

## 背景与定位
解决的问题：高分辨率、长时长（10 秒）视频生成在训练与推理上的算力瓶颈——时空全注意力随分辨率/时长呈二次（乃至立方）增长。Kandinsky 5.0 用一套统一架构覆盖 T2I/编辑/T2V/I2V 全任务，强调「质量 × 效率」平衡与完整开源（代码+各训练阶段权重）。

技术脉络中的位置：
- 继承 [[latent-diffusion-ldm]] 的潜空间扩散思路，扩散主干用 [[dit-scalable-diffusion-transformers]]（Diffusion Transformer），训练范式从扩散转向 Flow Matching（rectified flow）。
- 是 Kandinsky 家族首个基于 Flow Matching 的模型；相比 Kandinsky 4.0（首个 DiT、MMDiT-like、2024/12）改用 **CrossDiT**（文本走 cross-attention 而非 MMDiT 的拼接 self-attention），消除了拖慢训练的 concatenation，且更兼容稀疏注意力。
- Kandinsky 谱系：ruDALL-E/Malevich（2021，自回归）→ Kandinsky 1.0（2022.6, 12B 自回归）→ 2.0/2.1/2.2（2022–2023，首个扩散、多语言、image prior、MoVQ）→ 3.0/3.1（2023–2024，FLAN-UL2 编码器、Flash 蒸馏 ADD）→ Kandinsky 4.0（2024.12, 17.5B, MMDiT）→ 4.1（2025.6, 14B）→ **5.0**（2025.11）。
- 对标对象：开源 Wan 2.1/2.2、HunyuanVideo、CogVideoX、Mochi、Sora（闭源）；图像侧对标 FLUX.1 dev、Qwen-Image；编辑侧对标 FLUX.1 Kontext、Qwen-Image-Edit-2509；视频闭源对标 Veo 3 / Veo 3 fast、Sora。
- 一个鲜明定位：**俄语/俄罗斯文化代码（RCC）** 的最强开源理解者，专门构建 RCC 数据集（22.95 万视频场景 + 76.86 万图像）。

## 模型架构
**统一架构**：所有 6 个模型共用 latent diffusion + Flow Matching + **CrossDiT** 主干，仅 block 数与维度随规模变化。

**主干 CrossDiT（Cross-Attention Diffusion Transformer，自研）**：核心是一串 CrossDiT block，每个 block 是经典残差结构的三个子块顺序串联——**Self-Attention → Cross-Attention → MLP**（self/cross 注意力输出与输入视觉 latent 相加）。文本走 cross-attention 注入，而非 Kandinsky 4.0 用的 MMDiT 拼接式 self-attention——这样更兼容处理「同 batch 内不同长度视频」所需的稀疏注意力，并去掉了拖慢训练的 concatenation。

模型接收 4 类输入：
- **Text**：Qwen2.5-VL 文本 embedding → Linear+LayerNorm + 1D RoPE → **Linguistic Token Refiner（LTF）** 模块（一个去掉 cross-attention 的 CrossDiT block，用于增强文本表示、消除预训练文本编码器带来的位置偏置）→ 经 cross-attention 喂入主干。
- **Time**：扩散时间步经 Sinusoidal Encoding + MLP。
- **CLIP text embedding**：CLIP ViT-L/14 对整段描述的单一文本 embedding，与 time embedding 逐元素相加，连同末层输出送入 Adaptive Norm 层（AdaLN）。
- **Visual**：图像 latent（FLUX.1-dev VAE）或视频 latent（HunyuanVideo 3D VAE 编码器）→ 生成 3D RoPE 喂入每个 block。

**文本编码器**：Qwen2.5-VL（7B，embedding 维度 3584，**最大上下文仅 256 token**——这是后文 prompt following 短板的根因）；外加 CLIP ViT-L/14（embedding 768，上下文 77）。文本用 VLM 指令模板包裹（system 提示「You are a prompt engineer. Describe…」），更契合指令训练的 VLM 编码器。

**Visual tokenizer / VAE**：图像用 **FLUX.1-dev VAE**；视频用 **HunyuanVideo 3D VAE** 编码器（时序压缩、保持时序一致性）。

**三档规模（CrossDiT 超参，Table 3）**：

| 模型 | CrossDiT blocks | LTF blocks | Linear dim | model dim | time dim |
|---|---|---|---|---|---|
| Image Lite (6B) | 50 | 2 | 10240 | 2560 | 512 |
| Video Lite (2B) | 32 | 2 | 7168 | 1792 | 512 |
| Video Pro (19B) | 60 | 4 | 16384 | 4096 | 1024 |

**分辨率策略**：Lite 视频最高 768×512（SD）；Pro 视频最高 1280×768 / 1024×1024（HD）；Image Lite 出 1K（1280×768、1024×1024 等多种长宽比）。条件注入：T2I 加全零单通道 mask；I2V 首帧不加噪+全一 mask；编辑则把噪声图与 instruct 参考图按通道拼接+全一 mask。

**关键架构设计——NABLA（Neighborhood Adaptive Block-Level Attention，自研稀疏注意力）**：用于 >512px 或 >5 秒的高分辨率/长视频，替代二次复杂度的时空全注意力。三步构造 content-aware 稀疏 mask：
1. **块级降维**：Q/K 按 N=64（P×P，P=8）的块做 average-pool，注意力图计算量降 N²=4096 倍；
2. **CDF 自适应稀疏化**：对每个 head 的降维注意力图算 softmax 后的累积分布函数（CDF），按阈值 1−thr 二值化，逐 head 生成专属稀疏 pattern；
3. **边界伪影抑制**：可选与 **Sliding-Tile Attention（STA）** 的固定窗口 mask 取并集，抑制高分辨率下的块状边界伪影。
配套 **fractal flattening** token 重排（把每个 P×P 空间块的 64 token 排成连续序列，保留时序顺序，优化显存访问）。NABLA 无需自定义 CUDA kernel，直接接 PyTorch FlexAttention；相比 STA 的固定 pattern，能逐 head 自适应捕捉长程依赖，避免 STA 在高分辨率/长视频上的物体重复伪影。

## 数据
全部数据来自多套数据集，按训练阶段使用（来源/规模均来自技术报告与 Habr 官方博客）：

**Kandinsky T2I（图文，预训练）**：>5 亿张通用域图像（来源含 LAION、COYO 及大型图库）。处理流水线：短边 <256px 过滤 → 感知哈希去重 → 高级过滤（watermark_resnext101 + YOLO 水印检测；TOPIQ + Q-Align 技术/美学质量打分；CRAFT 文字过多过滤；SAM2+Sobel 复杂度过滤剔除空背景；YOLOv8+CLIP 分类）→ **合成英文 caption**（InternVL2-26B 生成、InternLM3-8B 精简；高分辨率图额外用 Qwen2.5-VL-32B 生成俄文 caption）→ 正则清洗 + 剔除含西里尔/中文字符的句子保英文纯度。按短边 256/512/1024 分目录存 Parquet 于 S3。

**Kandinsky T2V（视频，预训练）**：>2.5 亿视频场景，来自开源数据集+大型视频平台。PySceneDetect 切镜（每段 2–60 秒）→ 短边<256 过滤 + 视频感知哈希去重 → 高级过滤（水印；MS-SSIM 结构动态过滤过静/过动；DOVER+Q-Align 技术/美学质量；CRAFT 文字；YOLOv8+CLIP 分类；VideoMAE 训练的相机/物体/光色动态打分）→ **Tarsier2-7B 生成合成英文 caption** → InternVideo2-1B embedding + K-Means 聚 1 万簇做平衡采样。

**Habr 博客披露的原始漏斗（Video Lite 视角）**：原始采集 **60 亿图像 + 3500 万视频**，切成 **15 亿短场景**，过滤后选出 **1.24 亿最优场景 + 5.2 亿图像** 入预训练。

**Kandinsky RCC（俄罗斯文化代码）**：229,504 视频场景 + 768,555 图像，按自研 taxonomy 人工策展（信仰/语言/历史记忆/自然/建筑/人物等），人工写俄文描述再机译英文（专名特殊处理）；既用于预训练也用于专项微调。

**Kandinsky I2I（编辑指令对，预训练）**：从约 2.4 亿图像构建编辑对——CLIP/DINOv2/人脸相似度匹配 → 自适应阈值（聚 1 万簇）→ LoFTR+RANSAC 几何验证（内点 inlier 阈值）→ 质量过滤+排除近重复/简单 crop → 用 **GLM-4.5（LoRA 微调、无 reasoning）** 生成编辑指令 caption——选型时对 GPT-4o / GPT-4 Mini(reasoning) / Gemini 2.5 Pro / Qwen2.5-VL-32B / GLM-4.5 做 SBS 人评，**Gemini 2.5 Pro 质量排第一、GLM-4.5 紧随其后**，因性价比最优而选 GLM-4.5。最终约 **1.5 亿** 高质量编辑对。编辑 SFT 子集：Q-Align>4 & 美学>2 筛出约 60 万 → 人工精选。

**SFT 数据集（视频+图像，高质量人工精选）**：初始 93,296 视频场景 + 约 1000 万图像；图像走两阶段 captioning（Qwen2.5-VL-32B 写长描述 → Qwen3-32B 改写为「极长/长/中/短/极短」多版本，且中英双语同时输出）；视频用 SkyCaptioner-V1 + Qwen2.5-VL 32B/72B。经两阶段专家评估（技术筛查 + 影视/视觉艺术专家细评，问卷涵盖曝光/构图/光色/伪影/「wow factor」等）。**严格 v1**：2,833 视频 + 45,000 图像（仅保留约 3% 视频、5% 图像）；**放松 v2**：12,461 视频 + 153,000 图像。VLM（Qwen2.5-VL-32B）分 9 大域（animals/architecture/art/cartoons/food/interiors/nature/people/tech），T2I 再细分 2–9 子域，用于 model-soup 配比与课程学习。

## 训练方法
**训练目标**：Flow Matching（rectified flow），latent diffusion 管线。优化器 AdamW（betas=(0.9,0.95), eps=1e-8），梯度范数裁剪至 1，EMA 0.9999，无条件样本概率 0.1。

**多阶段流水线（Fig. 18）**：
- **Image Lite 6B**：低/中分辨率 T2I 预训练共享 backbone → T2I Lite 续高分辨率预训练 → SFT → **RL 后训练**；编辑模型从中分辨率 checkpoint 分叉，做中→高分辨率两阶段编辑微调（80% 编辑 + 20% T2I）+ SFT。
- **Video Lite 2B**：先低分辨率纯 T2I → 三任务联合训练（T2I 1% / T2V 79% / I2V 20%）覆盖低→高分辨率、5 秒；进入 10 秒预训练阶段启用 NABLA → I2V 微调 + 5 秒 SFT；并行训 10 秒三任务的 SFT+蒸馏 → 得 T2V Lite / I2V Lite / Video Lite Flash。
- **Video Pro 19B**：低分辨率 T2I 起步 → 4 阶段预训练（T2I 2% / T2V 77% / I2V 21%），分辨率升到 1024、时长 5→10 秒，高分辨率用 NABLA → I2V 专项微调 + SFT → 蒸馏得 Video Pro Flash。
- 预训练超参（Table 4 节选）：Image Lite 低分辨率 40 万步、batch 8000、lr 1e-4；Video Lite 低分辨率 22 万步 batch 8192、lr 1e-4；Video Pro 低分辨率 20 万步 batch 16384、lr 1e-4；高分辨率阶段 lr 降至 2e-5、weight_decay 0.001。

**SFT 关键 trick——Model Souping（权重平均）**：直接在整 SFT 集上全量微调会保留非真实感风格、退化文本对齐/文字渲染。改为按 9 域（图像再细分子域）分别全量微调（batch 64、lr 1e-5，验证集出伪影即停），再按「子域规模平方根」加权聚合域内模型，最后 9 个域模型等权平均。视频同理：各域单独训（个体过拟合、出伪影）但等权平均后稳定无过拟合——内部 SBS 上 souping 在视觉质量/运动一致性/伪影上胜过标准 SFT。标准 SFT 约 1 万步即过拟合（5 秒模型取第 1 万步 EMA checkpoint 最佳）。

**蒸馏与加速（视频）**：两类蒸馏模型——
1. **Guidance Distilled**：CFG 蒸馏（null prompt，最优 CFG=5.0），NFE 100→50（2× 提速），人评无可感退化。
2. **Diffusion Distilled（Flash）**：两阶段——先 **TSCD（Trajectory Segmented Consistency Distillation）** 把 CFG checkpoint 蒸到 16 NFE；再 **对抗后训练（受 LADD 启发）** 补视觉保真。对抗训练用 Hinge loss，RMSprop（生成器 lr 1e-6、判别器 1e-4），梯度裁剪 1.0；关键稳定化技巧是喂判别器前对真/假图都加 Logit-Normal(−4,1) 采样的高斯「re-noising」噪声，从而免去 R1 梯度惩罚。NFE 100→16（约 6× 提速）。

**RL 后训练（仅图像）**：
- **Reward model**：从 Qwen2.5-VL-7B 初始化的 VLM，输入两张标注图+文本，输出「图1是否更好」，取 token "Yes" 概率作为奖励 R=P("Yes"|x1,x2,y)；用 Reward Dance 方法。**免人工标注 trick**：用「pre-train 生成 < SFT 生成 < SFT 集真实图」的设计先验自动构造 (x_w, x_l, y) 偏好对。监控分数分布避免过拟合，选第 1300 步 checkpoint。
- **RL 微调**：用 **DRaFT-K**（K=10），只对生成最后 K 步反传梯度；以 SFT 真实图为参考，最大化「生成图被 reward 判为更好」的概率；加 SFT 模型与 RL 模型间的 KL 正则（flow-matching 形式 KL = Σ‖v_RL−v_SFT‖²），最优 β_KL=2e-2。消融发现「相对奖励 + SFT 真实图作参考」优于绝对奖励 / 双生成图方案。

## Infra（训练 / 推理工程）
**训练集群**：标准 NVIDIA 多节点集群，每节点 8 GPU + NVLink，节点间 InfiniBand。数据集规模 O(10) PB，用 S3 对象存储（弃 NFS，成本）经 100 Gbit/s 链路 streaming。

**数据存储/IO**：所有图像/视频**预先用 VAE 编码**，存 latent 而非像素，打包成大小近似均匀的 .tar（按分辨率/模态定每 tar 样本数：低分辨率图 1024/tar，高分辨率视频 1/tar）；S3 仅允约 O(10³) 并发连接，故设计成「少开对象、单连接高吞吐」。文本 embedding **在线计算**（单条文本 embedding 约为 256px 图 latent 的 50 倍大，存储会爆 S3）。DataLoader 两段式：worker 流式拉 .tar 解包推入按长宽比（1:1/16:9/4:3）分队列；主进程按 Σtᵢ≈t_max 动态拼不同长度视频成 batch（图像当长度 1、单独成 image-only batch、显式控制图像步占比），大幅降 GPU 空转，data loading 与计算 overlap 后达 **58.79% MFU**（model FLOPs utilization）。

**分布式与显存**：全程 **HSDP**；中分辨率起加 **Sequence Parallel**（选 SP 而非 TP，因每 block 仅 2 次集合通信）。DiT 权重切到 64 GPU、文本编码器切到 32 GPU，计算/通信全 overlap、per-GPU 显存极低。HD 10 秒训练用最大 SP=8 保证集合通信留在单 NVLink island。Checkpoint 非阻塞：64 进程各自直写权重分片，不在任何节点重建全量 state_dict。**激活检查点 + offloading**：预训练用经典 activation checkpointing；RL 阶段需保留整条生成轨迹激活，改用「block 输入在前/反向间异步搬到 host RAM」的 offloading 变体，显著降峰值激活显存且几乎不掉速。报告还给出训练步时与显存的**解析估计公式**（Eq.1/Eq.2，用于实验前选 batch/并行配置）。

**推理加速**（Table 5，单张 80GB H100）：
- **VAE 加速**：重写 HunyuanVideo VAE 编码器、优化 tiling + torch.compile，编码 **2.5×**（Habr 给 2.7×）提速，无需重训。
- **CrossDiT 优化**：profiling+重构消除 GPU 空转；**MagCache** 缓存扩散步 **46% 提速**且无可见质量降；SD/≤5 秒用 FlashAttention（2/3）或 SageAttention；>5 秒或 HD 用 NABLA（2.7×）。
- **Offloading**：把文本编码器/VAE 与 DiT 交替在 GPU/RAM 间搬，显存 **65→42GB（−35%）**，推理慢约 10%。
- Habr 实测累积（Video Lite SFT 5 秒）：torch.compile 重构 190→139s（−27%）→ MagCache 139→74s（−47%）。
- 量化：Qwen 文本编码器支持 bitsandbytes NF4，配合 VAE tiling/offloading 可在 12–24GB 显存上跑。
- 部署：HF Diffusers（Video Pro / Image Lite 已合入）、ComfyUI、多 GPU 分布式推理、Telegram bot beta。

**生成时延（H100, NFE）**：Video Lite 5s 100NFE=139s、Flash 16NFE=35s（约 4×）；Video Pro 5s SD=560s、HD(768×1280)=1241s，Flash=235s；Image Lite 1024² 100NFE=13s。

## 评测 benchmark（把效果讲清楚）
**重要说明**：Kandinsky 5.0 技术报告对自身模型**主要用人评 SBS**（Side-by-Side）而非报告单点硬指标（FID/CLIPScore/GenEval 等大多未给）。硬性 VBench/CLIP 数字来自配套 NABLA 论文（在 Wan2.1-14B 上的消融）。以下数字均来自已抓取一手源。

**人评 SBS（视频，MovieGen benchmark ~1003 prompts，Elementary 平台约 20 名非新手标注员）**：
- **Video Lite 2B vs Sora**：~6.5 万对判断、44 名标注员、239 人时、1002 prompt-video 对、5 路重叠，标注员一致率约 71%。Lite 在视觉质量/运动维度占优（具体分布为堆叠图，无单一总分）。
- **Video Lite 2B vs Wan 系列（Wan2.1 14B / Wan2.2 5B / Wan2.2 A14B）**：视觉质量、运动动态**全面占优**；prompt following 上 Wan2.2 A14B、Wan2.1 14B 更强（捕捉细粒度语义/动作更好）——明确的「视觉流畅度 vs 语义保真」权衡。Habr 强调 Lite 参数量比 Wan 14B 小 **15 倍**。
- **Video Lite 2B vs Kandinsky 4.1 Video**：运动动态 Lite 59% 胜 / 4.1 28% 胜 / 13% 平；伪影 55% 两者相当、Lite 更少伪影占 27% vs 4.1 仅 9%；总维度 Lite 视觉质量 0.59、运动动态 0.73、prompt following 0.50（持平）。
- **Video Pro 19B vs Veo 3 / Veo 3 fast**：Pro 在视觉质量、运动动态更高；**prompt following 显著落后** Veo 3 变体（报告坦承为相对短板）。
- **Video Pro 19B vs Wan 2.2 A14B**（T2V & I2V）：视觉质量、运动动态占优。
- **Video Lite Flash（蒸馏）vs 非蒸馏 Lite**：5s/10s 均有「可测但总体温和」的质量下降，主要在细节、时序一致性、复杂语义；轻 prompt/短时长几乎无可感差异。

**图像/编辑 SBS**：
- Image Lite vs FLUX.1 dev / Qwen-Image（PartiPrompts P2 扩展集）：视觉质量更强，prompt following 有竞争力。
- Image Editing vs FLUX.1 Kontext dev / Qwen-Image-Edit-2509（Kontext Bench）：表现有竞争力。
- 图像 RL 后训练在所有目标指标的 SBS 上均显著提升真实感、文本对齐、构图。

**排行榜**：Kandinsky 5.0 **Video Pro 在 LMArena Text-to-Video 榜登顶开源第一**（2025/12/12，README 披露）。

**NABLA 硬指标（在 Wan2.1-14B 720p 微调消融，4×H100；NABLA 论文 Table 1–4）**：
- 效率（Table 1）：Baseline 全注意力 8.35 min/推理；NABLA(0.7) 80.13% 稀疏 4.02 min；NABLA(0.5)+STA(11,40,40) 81% 稀疏 3.58 min；90%+ 稀疏档约 3.07–3.13 min（NABLA(0.4) 92.5% 3.07 / NABLA(0.2)+STA(11,24,24) 92.27% 3.13）。预训练单迭代 NABLA 7.5s vs 全注意力 10.9s（**1.46×**），且训练/验证 loss 收敛更优。
- 质量（Table 2，90% 稀疏）：CLIP score——Baseline 42.06 / NABLA(0.4) **42.08** / NABLA(0.2)+STA 41.98；STA-only 41.51（退化）。VBench Total——Baseline 83.16 / NABLA(0.4) **83.17** / NABLA+STA **83.22** / STA-only 82.39。VBench Semantic——Baseline 75.23 / NABLA(0.4) 75.76 / NABLA+STA 76.04 / STA-only 71.73（STA 在多物体/空间关系明显掉分）。
- 人评（Table 3，80% 稀疏 vs baseline，942 VBench prompts、50 人）：overall「NABLA 更好 18.4% / baseline 更好 20.3% / 两者都好 57.1% / 都差 4.1%」——感知上与全注意力基本持平。
- 结论：NABLA 在 ~90% 稀疏下**全量恢复**生成质量，2.7× 提速；优于固定 pattern 的 STA（尤其长程依赖、多物体/空间关系）。

## 创新点与影响
**核心贡献**：
1. **统一 CrossDiT 架构**覆盖 T2I/编辑/T2V/I2V 全任务，文本走 cross-attention（替代 MMDiT 拼接），更兼容稀疏注意力、去掉拖慢训练的 concatenation。
2. **NABLA 自适应块级稀疏注意力**：CDF 阈值化逐 head 动态稀疏 + STA 并集抑伪影 + fractal token 重排，纯 PyTorch FlexAttention 实现、无需自定义 CUDA kernel；~90% 稀疏 2.7× 提速且 VBench/CLIP/人评不掉——这是全篇最可复用的工程贡献。
3. **图像 RL 后训练免人工标注 trick**：用「pretrain<SFT<real」设计先验自动造偏好对训 reward model + DRaFT-K + flow-matching KL 正则。
4. **Model-soup 分域微调**：按 VLM 9 域（图像再细分子域）分别微调再平方根/等权平均，解决全量 SFT 退化文本渲染/真实感的问题。
5. **完整数据流水线披露**：T2I/T2V/I2I/RCC/SFT 五套数据集的采集→过滤→re-captioning→聚类全链路与具体模型/阈值。
6. **全栈开源（MIT）**：6 模型族各训练阶段权重（pretrain/SFT/nocfg/distilled/I2V）+ 代码 + Diffusers/ComfyUI 集成，俄系开源生成的代表作。

**影响**：作为参数高效（2B Lite 媲美 14B Wan）、强俄语/俄罗斯文化代码、全开源的视频生成族，降低了高质量视频生成的部署门槛（12–24GB 显存可跑）；NABLA 已被社区（CacheDiT、SimpleTuner 等）接入并可零样本/微调用于其他 DiT（论文中即在 Wan2.1 上验证）。Video Pro 登顶 LMArena 开源 T2V 第一。

**已知局限（报告自述）**：
- **文本对齐（prompt following）落后**：归因于 Qwen2.5-VL-7B 文本编码器**上下文仅 256 token**；计划换更强/更长上下文编码器 + RL 强化。
- **复杂动态时序一致性**：>10 秒视频对流体/布料等长程物理交互偶有伪影。
- **泛化不均**：受数据类别不平衡/风格偏置影响，跨风格/物体/场景表现不一。
- **未统一**：当前是任务专用模型族，长期目标是合一为统一多媒体生成基础模型。
- **算力效率**：消费级硬件高分辨率实时（24+ FPS）仍是挑战。

## 原始链接
- tech-report (arXiv abs): https://arxiv.org/abs/2511.14993
- tech-report (PDF): https://arxiv.org/pdf/2511.14993
- NABLA paper (arXiv abs): https://arxiv.org/abs/2507.13546
- NABLA paper (PDF): https://arxiv.org/pdf/2507.13546
- github: https://github.com/ai-forever/Kandinsky-5 （镜像 https://github.com/kandinskylab/kandinsky-5）
- hf (org): https://huggingface.co/kandinskylab
- hf (Video Pro sft 5s): https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Pro-sft-5s
- hf (Video Lite sft 5s): https://huggingface.co/kandinskylab/Kandinsky-5.0-T2V-Lite-sft-5s
- hf (Image Lite T2I): https://huggingface.co/kandinskylab/Kandinsky-5.0-T2I-Lite
- blog (Habr, Sber, Video Lite 公告 2025-09-30): https://habr.com/ru/companies/sberbank/articles/951800/
- project page: https://kandinskylab.ai/

## 一手源存档（sources/）
- [arxiv-2511.14993.pdf](https://arxiv.org/pdf/2511.14993) （技术报告 PDF，gitignore，本地精读）
- [techreport.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--techreport.txt) （技术报告全文提取）
- [arxiv-2507.13546.pdf](https://arxiv.org/pdf/2507.13546) （NABLA 论文 PDF，gitignore）
- [nabla.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--nabla.txt) （NABLA 论文全文提取）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--readme.md) （GitHub README）
- [hf-t2v-pro.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--hf-t2v-pro.md) （HF Video Pro model card）
- [hf-t2v-lite.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--hf-t2v-lite.md) （HF Video Lite model card）
- [hf-t2i-lite.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--hf-t2i-lite.md) （HF Image Lite model card）
- [habr.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/kandinsky-5--habr.md) （Habr 官方博客文本提取）
