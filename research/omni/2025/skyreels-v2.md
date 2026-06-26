---
title: "SkyReels-V2: Infinite-Length Film Generative Model"
org: "昆仑万维 Skywork AI"
country: China
date: "2025-04"
type: tech-report
category: video
tags: [video, diffusion-forcing, autoregressive, flow-matching, dit, dpo, long-video, open-source]
url: "https://arxiv.org/abs/2504.13074"
arxiv: "https://arxiv.org/abs/2504.13074"
pdf_url: "https://arxiv.org/pdf/2504.13074"
github_url: "https://github.com/SkyworkAI/SkyReels-V2"
hf_url: "https://huggingface.co/collections/Skywork/skyreels-v2-6801b1b93df627d441d0d0d9"
modelscope_url: "https://www.modelscope.cn/collections/SkyReels-V2-f665650130b144"
project_url: "https://www.skyreels.ai/home"
downloaded: [arxiv-2504.13074.pdf, skyreels-v2--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
SkyReels-V2 是昆仑万维 Skywork 推出的「无限长影视级视频生成框架」，核心创新是把**全序列扩散模型微调成扩散强制（Diffusion Forcing）模型** + **专为镜头语言设计的结构化 captioner（SkyCaptioner-V1）** + **专攻运动质量的 RL/DPO 后训练**，号称首个采用扩散强制架构、且在公开模型中 V-Bench 总分最高（83.9%）的开源视频模型，开源 1.3B/5B/14B 多尺寸、可单 prompt 生成 >30s 乃至理论无限长视频。

## 背景与定位
视频生成长期有「不可能三角」：提示遵循、画质、运动动态、时长四者难以兼顾——为了画质牺牲运动幅度、为了分辨率压缩时长（典型只有 5–10s）、通用 MLLM 看不懂电影镜头语法（景别/机位/运镜/表情）。两大范式各有短板：纯扩散模型画质高但时序上「碎片化」、固定长度；自回归（AR）模型时序连贯但误差累积、分辨率退化，都做不出长片。

[[diffusion-forcing]]（Chen et al. 2024）提出给每个 token 分配**独立噪声级别**，把扩散的高画质和 AR 的可无限延展结合起来，但其组合式噪声调度导致训练搜索空间巨大、训练不稳。SkyReels-V2 站在 [[wan-2-1]] 架构之上（直接复用 Wan2.1 的 VAE 与 text encoder，只从头训 DiT），并吸收 AR-Diffusion 的非递减时间步约束把搜索空间从 O(1e48) 砍到 O(1e32)，从而把扩散强制真正用在影视级长视频上。技术脉络上紧接 [[latent-diffusion-ldm]] → [[dit-scalable-diffusion-transformers]] → [[flow-matching]] → [[hunyuan-video]]/[[wan-2-1]] 这条开源视频线，定位是「补齐镜头语言 + 运动质量 + 无限时长」三块短板。

## 模型架构
- **Backbone**：DiT（扩散 Transformer），**直接采用 Wan2.1 的模型架构**，只从头训练 DiT 主干，保留 Wan2.1 预训练的 VAE 与文本编码器。
- **生成范式**：Flow Matching（rectified flow），用 logit-normal 采样时间步、线性插值构造中间 latent、预测速度场（详见训练方法）。
- **Text encoder**：沿用 Wan2.1 的 **umT5**（论文提到条件为「512 维 umT5 features」）。
- **VAE**：沿用 Wan2.1 VAE（diffusers 中即 `AutoencoderKLWan`，时间×空间下采样的视频 VAE）。
- **扩散强制 Transformer（DFoT）**：把全序列扩散模型微调成每帧（每 token）可带独立噪声级别的模型。零噪声 token = 完全可见（条件），满噪声 token = 完全掩码，模型学会用干净 token 引导恢复噪声 token。全序列同步扩散是其特例（所有 token 同噪声级），故可从全序列扩散权重直接 finetune 得到。
- **因果注意力优化**：信息流天然有方向（噪声样本依赖更干净的历史），双向注意力非必需。先用双向注意力训练 DFoT，再 finetune 成 **context-causal attention**，推理时可**缓存历史样本的 K/V 特征**，省去冗余计算。
- **FPS 解耦**：DiT 增加**可学习的 frequency embedding**（与 timestep embedding 加性交互）以解耦帧率依赖；高质量 SFT 阶段只用 FPS-24 数据后，这些 frequency embedding 被移除。
- **参数量与分辨率**：开源 1.3B / 5B / 14B 三档；分辨率走「256p→360p→540p→720p」渐进式（540P 推荐 544×960×97f，720P 推荐 720×1280×121f）。
- **I2V 条件注入**（SkyReels-V2-I2V）：仿 Wan2.1 I2V，把首帧参考图过 VAE 得 image latent，与 noise latent 及 **4 个二值 mask 通道**（首帧 1、其余 0）拼接；对新增卷积层和 cross-attention 中「image-context→value」投影做**零初始化**、其余新组件随机初始化，以保护原 T2V 能力。
- **SkyCaptioner-V1**：基于 Qwen2.5-VL-7B-Instruct 微调的结构化视频 captioner（独立模型，非生成主干的一部分），见「数据」。

## 数据
**数据来源（原始约 O(100M) 规模）**：
1. 通用数据集：开源 Koala-36M、HumanVid + 额外网络爬取视频；
2. 自采媒体：**28 万+ 部电影、80 万+ 集电视剧**，横跨 120+ 国家，估计总时长 **620 万+ 小时**；
3. 高质量艺术素材库。
另收集 **O(100M) concept-balanced 图像数据**用于早期加速建立生成能力。

**处理流水线（渐进式 loose→strict 过滤，边过滤边降量提质）**：
- **Shot 切分**：PySceneDetect + TransNet-V2 切成单镜头 clip；
- **结构化标注**：用 SkyCaptioner-V1（见下）打标；
- **质量问题三大类**：基础质量（低分辨率/低帧率/黑白静帧/抖动等）、视频类型问题（监控/游戏录屏/动画/无意义内容/静态）、后处理伪影（字幕/logo/调色/分屏/黑边/画中画/变速/特效马赛克）；
- **过滤器**：黑屏/静帧/美学（aesthetic-predictor-v2-5）/去重（copy-detection embedding）/OCR/马赛克/特效贴纸专家模型 + VQA/IQA/VTSS 质量评分模型，不同训练阶段设不同阈值；
- **字幕/logo 裁剪**：CRAFT OCR 检字幕、MiniCPM-o 检 logo，用单调栈算法求最大内部矩形（覆盖>80% 且宽高比接近原图才裁，否则丢弃）——避免直接丢弃浪费数据；
- **概念平衡**：后训练阶段按主体类别平衡，**数据量减半**；平衡前后人类主体占比从 84.8% 降到 63.2%（Human / Scenery / Animal 等大类重新配比）。

**人在回路（Human-In-The-Loop）抽检**：预训练阶段抽 0.01%（万分之一）手检，要求总坏例 <15%（基础质量<3% / 类型问题<5% / 后处理<7%）；后训练抽 0.1%（千分之一），要求总坏例 <3%（基础<0.5% / 类型<1% / 后处理<1.5%）。

**SkyCaptioner-V1（结构化视频 captioner）**：
- 基座 Qwen2.5-VL-72B-Instruct 生成初始结构化字段（subjects 的类型/外观/动作/表情/位置 + shot metadata：景别/机位/机位方向/运镜/环境/光照），部分字段用**子专家模型**替换以提精度；
- 子专家：① Shot captioner（景别5类/角度3类/机位6类，分别 82.2%/78.7%/93.1% 测试精度）；② Expression captioner（7 类情绪 + 强度 + 面部特征 + 时序，情绪分类 85% 精度，基于 S2D 框架 + InternVL2.5 + CoT）；③ Camera Motion captioner（6DoF×3 速度档 = 2187 种组合，五轮主动学习，单类运动 89% 精度）；
- 把通用 captioner + 专家知识**蒸馏进 Qwen2.5-VL-7B-Instruct** 得到 SkyCaptioner-V1：训练集从 1000 万样本里精选约 **200 万**概念平衡视频；T2V 出 dense caption、I2V 聚焦「主体+时序动作/表情+运镜」，每字段 10% drop rate 模拟用户描述不全。最终用 Qwen2.5-32B-Instruct 做 caption 融合。

## 训练方法
**训练目标（Flow Matching / rectified flow）**：给定 latent x1，从 logit-normal 采时间步 t∈[0,1]，噪声 x0~N(0,I)，线性插值 `xt = t·x1 + (1−t)·x0`，真值速度 `vt = x1 − x0`，模型预测速度场 uθ(xt,c,t)，损失 `L = E‖uθ(xt,c,t) − vt‖²`。

**渐进分辨率预训练（3 阶段，只训 DiT）**：
- 双轴 Bucketing（时长 bins × 宽高比类别）+ FPS 归一化（按 16/24 取余最小选目标帧率）+ 自适应 batch 防 OOM；
- Stage1 256p：图视频联合训练，学低频概念，视频偏糊；
- Stage2 360p：图视频联合 + 更严过滤（时长/运动/OCR/美学/质量），清晰度显著提升；
- Stage3 540p：纯视频目标 + 来源过滤（去 UGC 留电影数据），增强真人纹理与电影质感；
- 优化器 AdamW：Stage1 lr 先 1e-4（wd=0）收敛后转 5e-5（wd=1e-4），Stage2/3 降到 2e-5。

**四阶段后训练（前 3 阶段 540p，最后 720p）**：
1. **HQ 540p SFT**（在 RL 之前）：用概念平衡数据做「概念均衡器」，为后续阶段提供好初始化，并移除 FPS embedding 精简架构；
2. **运动质量强化学习（RL/DPO）**：只针对运动质量（因主要缺陷是大幅可变形运动处理差 + 违反物理）。
   - **半自动偏好数据流水线**：人标（失败模式分类学 + LLM 扩写同类 prompt，每 prompt 历史 checkpoint 池生成 4 个样本配对，专业标注员打 Better/Worse/Tie；筛选会丢掉约 80% 数据对）+ 自动生成（用 CLIP 相似度从已有数据取「ground-truth 真视频」做 chosen，对真视频施加**渐进式可控失真**造 rejected：V2V 最轻 / I2V 中等 / T2V 最重；还用倒放挑战物理、Tea-Cache 调参注噪破坏局部细节、改帧采样率造运动幅度异常）；
   - **奖励模型**：基于 Qwen2.5-VL-7B-Instruct，3 万样本对，用 **Bradley-Terry-with-Ties（BTT）** 训练，运动质量与上下文无关故不含 prompt；
   - **Flow-DPO**：沿用 VideoAlign 的 flow 版 DPO，只优化运动质量、不动文本对齐与画质。**分阶段 DPO**：模型易区分 chosen/rejected（性能 plateau）时刷新 reference 模型，每阶段 2 万训练数据，共 **3 阶段**；
3. **扩散强制训练（DFoT）**：用 **FoPP（Frame-oriented Probability Propagation）** 时间步调度器训练（先均匀采 (帧索引 f, 时间步 t)，再用动态规划在非递减约束下传播前后帧时间步概率）；推理用 **AD（Adaptive Difference）** 调度器，把相邻帧时间步差当自适应变量 s（s=0 即同步扩散，s=T 即纯自回归），可在异步 AR 与同步生成间自适应；
4. **HQ 720p SFT**：扩散强制后做 720p 高质量 SFT，提升最终画质。

**长视频稳定化**：滑动窗口（条件于前 fprev 帧 + prompt 生成后 fnew 帧），对已生成帧打**轻微噪声**防误差累积；推理时 `--addnoise_condition 20`（≤50）增强长视频一致性，`--overlap_history 17`。

**蒸馏加速**：用 **DMD 蒸馏**（去掉回归损失、用高质量视频而非纯噪声作 student 输入加速收敛，fake/student 更新比 5:1，4 步生成器配 flow matching 专调调度；小 lr + 大 batch 稳训练）。

## Infra（训练 / 推理工程）
**训练优化**：
- 显存：算子融合降 kernel launch；梯度检查点（GC，只存 transformer block 输入，fp32→bf16 省 50% 显存）；激活异步 offload 到 CPU（但因 8 GPU 共享 CPU 内存，与 GC 选择性结合）；
- 稳定性：自愈框架（实时检测隔离故障节点 + 备用算力动态再分配 + checkpoint 恢复迁移）；
- 并行：预计算 VAE 与 text encoder 结果；FSDP 分布式存 DiT 权重与优化器状态；720p 时因大临时张量碎片化严重，引入 **Sequence Parallel（DeepSpeed-Ulysses）** 缓解激活显存压力；
- 规模数字：captioner 训练用 **64×A800**（global batch 512，micro batch 4，梯度累积 2，lr 1e-5，2 epoch）；I2V finetune 仅 **1 万 iteration on 384 GPUs**；Camera Director finetune **384 GPUs × 3000 iter**（约 100 万平衡 SFT 样本）。**主模型预训练总算力/GPU 卡时未披露**。

**推理优化**：
- VRAM：RTX 4090（24GB）单卡服务 14B 模型——FP8 量化 + 参数级 offload 实现 720p 单卡生成；
- 量化：linear 层 FP8 动态量化 + FP8 GEMM（vs bf16 1.10× 加速）；attention 用 **SageAttention2-8bit**（1.30× 加速）；
- 并行：Content Parallel + CFG Parallel + VAE Parallel，4→8 张 4090 时整体延迟降 1.8×；
- 蒸馏：DMD 4 步生成器大幅降延迟（原扩散 30–50 步、5s 视频 >5 分钟）；
- 开源工程：多 GPU 推理用 **xDiT USP**；缓存加速用 **TeaCache**（README 默认脚本 `--teacache --teacache_thresh 0.3 --use_ret_steps`）；prompt enhancer 基于 Qwen2.5-32B-Instruct（开启需 64G+ 显存）；
- 实测峰值显存（README）：540P 下 1.3B 约 14.7GB、14B 约 51.2GB（DF）/ 43.4GB（T2V）。

## 评测 benchmark（把效果讲清楚）
**VBench 1.0（长 prompt 版，50 步、guidance 6）—— T2V 总分超所有开源对手：**

| 模型 | Total | Quality | Semantic |
|---|---|---|---|
| CogVideoX1.5-5B | 80.3% | 80.9% | 77.9% |
| OpenSora-2.0 | 81.5% | 82.1% | 78.2% |
| HunyuanVideo-13B | 82.7% | 84.4% | 76.2% |
| Wan2.1-14B | 83.7% | 84.2% | **81.4%** |
| **SkyReels-V2** | **83.9%** | **84.7%** | 80.8% |

总分(83.9%)与质量分(84.7%)均第一；语义分略低于 Wan2.1-14B，作者归因 V-Bench 对镜头场景语义考核不足（人评中 SkyReels-V2 反超 Wan2.1）。

**SkyReels-Bench 人评（1020 prompt，20 名专业评审，1–5 分）—— T2V：**

| 模型 | Average | 指令遵循 | 一致性 | 画质 | 运动质量 |
|---|---|---|---|---|---|
| Runway-Gen3 Alpha | 2.53 | 2.19 | 2.57 | 3.23 | 2.11 |
| HunyuanVideo-13B | 2.82 | 2.64 | 2.81 | 3.20 | 2.61 |
| Kling-1.6 STD | 2.99 | 2.77 | 3.05 | 3.39 | **2.76** |
| Hailuo-01 | 3.0 | 2.8 | 3.08 | 3.29 | 2.74 |
| Wan2.1-14B | 3.12 | 2.91 | 3.31 | **3.54** | 2.71 |
| **SkyReels-V2** | **3.14** | **3.15** | **3.35** | 3.34 | 2.74 |

SkyReels-V2 在**指令遵循(3.15)与一致性(3.35)**领先，运动质量(2.74)与闭源 Kling/Hailuo 持平，画质略逊 Wan2.1。

**SkyReels-Bench 人评 —— I2V：**

| 模型 | Average | 指令遵循 | 一致性 | 画质 | 运动质量 |
|---|---|---|---|---|---|
| HunyuanVideo-13B | 2.84 | 2.97 | 2.95 | 2.87 | 2.56 |
| Wan2.1-14B | 2.85 | 3.10 | 2.81 | 3.00 | 2.48 |
| Hailuo-01 | 3.05 | 3.31 | 2.58 | 3.55 | 2.74 |
| Kling-1.6 Pro | 3.4 | 3.56 | 3.03 | 3.58 | 3.41 |
| Runway-Gen4 | 3.39 | 3.75 | 3.2 | 3.4 | 3.37 |
| **SkyReels-V2-DF** | 3.24 | 3.64 | 3.21 | 3.18 | 2.93 |
| **SkyReels-V2-I2V** | 3.29 | 3.42 | 3.18 | 3.56 | 3.01 |

I2V 两个变体均为**开源 SOTA**（远超 HunyuanVideo-13B 2.84 / Wan2.1-14B 2.85），I2V 均分 3.29 逼近闭源 Kling-1.6(3.4)、Runway-Gen4(3.39)。

**SkyCaptioner-V1 标注精度**（1000 样本人评，vs Qwen2.5-VL-7B/72B、Tarsier2-recap-7B）：平均精度 **76.3%**（基座 72B 仅 58.7%），镜头相关字段碾压——shot type 93.7%、shot angle 89.8%、shot position 83.1%、camera motion 85.3%。

**关键消融/结论**：① 非递减噪声调度把扩散强制组合空间从 O(1e48)→O(1e32)，使长视频训练可收敛；② 异步推理（ar_step>0）经验上提升指令遵循与视觉一致性但更慢；③ 长视频靠 addnoise_condition + overlap_history 抑制误差累积。**注：论文未报告 FID/CLIPScore/GenEval 等单帧图像指标**（视频模型，以 VBench + 人评为主）。

## 创新点与影响
**核心贡献**：
1. **镜头语言结构化 captioner**：SkyCaptioner-V1 把通用 MLLM + 镜头/表情/运镜子专家蒸馏成 7B 模型，大幅提升「电影语法」提示遵循（这是与一般视频模型最大的差异化）；
2. **运动质量专项 RL**：半自动偏好数据流水线（人标 + 渐进失真合成 rejected）+ BTT 奖励模型 + 3 阶段 Flow-DPO，专攻运动而不伤画质/文本对齐；
3. **扩散强制后训练适配**：不从头训扩散强制，而是从全序列扩散模型 finetune，配 FoPP/AD 时间步调度 + 非递减约束 + 因果注意力 KV 缓存，实现工程可落地的**理论无限长**视频；
4. **全栈开源**：SkyCaptioner-V1 + SkyReels-V2 系列（DF/T2V/I2V/Camera Director/Elements2Video，1.3B/5B/14B），自称首个用扩散强制架构且 V-Bench 开源最高分的模型。

**影响**：为开源社区提供了「长视频 + 镜头可控 + 运动质量优化」的完整范式参考，扩散强制 + 因果注意力缓存的工程方案被后续长视频工作借鉴；衍生出 SkyReels-A1（音频/姿态驱动肖像）、SkyReels-A2（Elements2Video 任意元素合成）、SkyReels-Audio，并已迭代到 SkyReels-V3（2026-01 开源）。

**已知局限**：扩散强制框架**仍存在长时生成的误差累积**，限制了高质量输出的实际可用长度（作者明示为未来工作重点）；语义分仍略逊 Wan2.1；部分变体（5B 全系、Camera Director、蒸馏模型 checkpoint）截至技术报告时「Coming Soon」未放出。**主模型预训练总 GPU 卡时未披露**。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2504.13074
- arxiv_pdf: https://arxiv.org/pdf/2504.13074
- github: https://github.com/SkyworkAI/SkyReels-V2
- huggingface: https://huggingface.co/collections/Skywork/skyreels-v2-6801b1b93df627d441d0d0d9
- modelscope: https://www.modelscope.cn/collections/SkyReels-V2-f665650130b144
- playground: https://www.skyreels.ai/home

## 一手源存档（sources/）
- [arxiv-2504.13074.pdf](https://arxiv.org/pdf/2504.13074)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/skyreels-v2--readme.md)
