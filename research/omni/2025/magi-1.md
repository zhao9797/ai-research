---
title: "MAGI-1: Autoregressive Video Generation at Scale"
org: Sand AI
country: China
date: "2025-05"
type: tech-report
category: video
tags: [video, autoregressive, diffusion, flow-matching, chunk-wise, world-model, streaming, open-weights]
url: "https://arxiv.org/abs/2505.13211"
arxiv: "https://arxiv.org/abs/2505.13211"
pdf_url: "https://arxiv.org/pdf/2505.13211"
github_url: "https://github.com/SandAI-org/MAGI-1"
hf_url: "https://huggingface.co/sand-ai/MAGI-1"
modelscope_url: ""
project_url: "https://sand.ai"
downloaded: [magi-1--arxiv-html.md, arxiv-2505.13211.pdf, magi-1--github-readme.md, magi-1--hf-modelcard.md, magi-1--hf-papers.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
MAGI-1 是 Sand AI 推出的**分块（chunk-wise）自回归扩散视频生成世界模型**：把视频切成固定 24 帧（1 秒@24FPS）的 chunk，按"越往后噪声越大"的单调时序对每个 chunk 做整体去噪，一旦前一 chunk 去噪到一定程度即可流水线启动下一 chunk（最多 4 个 chunk 并行）；最大 24B 参数、支持 400 万 token 上下文，开源权重（Apache-2.0），在 **VBench-I2V 拿到 89.28 总分排名第一**，在 **Physics-IQ 物理基准 V2V 模式 56.02 分**远超 VideoPoet（29.5）/Sora（10.0）等所有模型。

## 背景与定位
主流大规模视频扩散模型（Sora、Wan、HunyuanVideo 等）几乎都是**双向（bidirectional）全序列去噪**：整段视频用统一噪声水平、推理时需要访问完整序列。这种设计忽视了时间数据固有的因果结构，不适合流式 / 实时 / 自回归场景，且生成长视频时峰值显存随时长增长。

MAGI-1 沿着**自回归 + 因果建模**这条线（[[diffusion-forcing]]、FVDM、CausVid 是同期探索），但把这些早期工作"规模小、缺乏 chunk 级抽象、未统一 T2V/I2V/续帧"的问题一次性解决：它是据作者所述**首个从零训练、分块自回归的大规模扩散视频模型**，在严格因果约束下统一了 text-to-video、image-to-video、video continuation 三类任务（无需任务专属微调）。核心卖点：

- **强时序因果**：每个 chunk 只能看历史 chunk（block-causal），天然支持续帧、物理因果推理。
- **流式 / 实时**：chunk 流水线 + KV cache，**峰值推理开销与视频总长无关**（恒定显存足迹），可做实时流式生成。
- **可控性**：chunk-wise prompting（逐秒文本控制）、通过调 KV range 实现可控镜头转场、长视频（近 30 秒叙事级 demo）。

技术谱系上，它建立在 [[latent-diffusion-ldm]]（潜空间去噪）、[[dit]]（DiT backbone）与 flow-matching / rectified flow 之上，并大量借鉴 LLM 工程（GQA、SwiGLU、QK-Norm、KV cache、Ulysses 序列并行）。

## 模型架构

### 整体 pipeline（分块自回归去噪）
视频在潜空间生成，逐 chunk 流水线进行。每个 chunk = 24 原始帧（=1 秒@24FPS）。chunk i 的去噪条件是**所有在它之前的 chunk**（block-causal）；当 chunk 去噪到一定程度（不必完全干净）下一 chunk 即可启动，因此最多 4 个 chunk 并发。block-causal 注意力掩码 = chunk 内 full attention + chunk 间 causal attention。这一设计让 T2V / I2V / 续帧仅通过"干净 chunk 占比"不同来区分（I2V 即"只有首 chunk 首帧干净"的续帧特例），统一进单次预训练。

### Transformer-based VAE（关键差异化点）
- 不用主流的卷积 / U-Net VAE，改用**纯 Transformer VAE**（ViT 风格），因为现代 GPU 上 transformer 比同规模卷积更快。
- Encoder：先用 3D 卷积 embedding（kernel 8×8×4、stride 8×8×4，输出 1024 通道）→ 加绝对位置编码 → 堆 **24 个 transformer block**（自注意力用 QKV norm 稳定）→ LayerNorm → 线性投影到 32 通道（前 16 = mean，后 16 = log-variance）。
- 压缩率：**空间 8×、时间 4×**；潜空间 16 通道。
- Decoder 对称结构，最后用 pixel shuffle + 3×3×3 3D 卷积还原像素；图像（单帧）输入时把帧沿时间复制 4 份（比补 3 空帧效果好）。
- 训练两阶段：阶段一固定 16 帧 256×256；阶段二图像 + 视频联合、可变分辨率/宽高比（像素总数 ~256² 或 384²，宽高比 [0.25,4.0]）。损失 = L1 + KL + LPIPS + GAN。推理用滑窗（空间 256×256 / stride 192 即 25% 重叠，时间不重叠）支持任意分辨率。
- 性能：614M 参数（比对比 VAE 都大），但 **平均解码 12.28ms 最快**，PSNR 36.55 排第二（对比 HunyuanVideo 37.27 PSNR/47ms 解码、CogVideoX 35.99/142ms、Wan2.1 35.95/79ms）。

### 自回归去噪 DiT（主干）
基于 DiT，针对自回归 + 大规模稳定性做了一系列改造（这些是 MAGI-1 的核心架构创新）：
- **Block-Causal Attention**：chunk 内 full、chunk 间 causal；位置编码用**可学习 3D RoPE**（base frequency 可学习）。因现有 attention 实现不高效支持 block-causal，作者自研 **Flexible-Flash-Attention（FFA）** 内核，基于 FlashAttention-3。
- **Parallel Attention Block**：时空自注意力与（外部条件的）交叉注意力并行设计——query 投影只算一次同时供两种注意力使用，把每 block 的 Tensor Parallel 通信从 2 轮降到 1 轮，降低 GPU 同步开销、提升大模型可扩展性。
- **QK-Norm + GQA**：对 Q/K 归一化提升训练稳定性；用 grouped-query attention 替代 MHA 省显存（128 头 / 8 组，时空注意力与交叉注意力都用）。
- **Sandwich Normalization in FFN**：模型变大后 FFN 易出数值问题，故在 FFN 输入输出前后各加 LayerNorm。
- **SwiGLU**：24B 模型 FFN 用 SwiGLU（4.5B 用 GLU）。
- **Softcap Modulation**：标准 DiT 用 adaLN 注入 timestep，大模型下会放大激活幅度、加剧数值不稳；故对缩放因子加 Softcap 约束到 [-1,1]，并因已用 QK-Norm 去掉 adaLN 的 input modulation。
- 文本编码器用 **T5**；timestep 用正弦位置编码。

### 模型规格（Table 2）
| | 4.5B | 24B |
|---|---|---|
| Layers | 34 | 48 |
| Model Dim | 3072 | 6144 |
| FFN 激活 | GLU | SwiGLU |
| FFN Dim | 12288 | 16384 |
| Attention | GQA+QK-Norm | GQA+QK-Norm |
| Block-Causal 头/组 | 128/8 | 128/8 |
| Cross-Attn 头/组 | 128/8 | 128/8 |
| 位置编码 | 可学习 3D RoPE | 可学习 3D RoPE |
| Optimizer | AdamW(wd 0.1, β=0.9/0.95) | AdamW(wd 0.1, β=0.9/0.95) |
| Peak LR | 1e-4 | 1e-4 |
| Warm-up | 1000 步 | 10000 步 |

24B 最大变体支持上下文长度 **最高 4M tokens**。

## 数据
- **规模**：从"数十 PB（tens of petabytes）"原始视频 + 图像中清洗出训练集（来源广泛，未披露绝对样本数）。
- **处理 pipeline**：PySceneDetect 切单镜头短片 → 一系列过滤 actor 去低质/去重 → MLLM 作为更强过滤器 → 通过的数据由 MLLM 打标注。
- **过滤 actors（很细，覆盖工业级质检）**：
  - 视觉质量 DOVER（仅用 technical score 最有效）；美学 LAION aesthetic（取首帧）；过曝/欠曝（HSI 亮度）；
  - 运动强度 RAFT 光流（8FPS 降采样后算）+ 显著性模型区分前/背景运动，取**适中运动**（避开过静/过动），分整体/前景/背景三种统计设上下阈值；
  - 相机稳定性（相邻帧光流一致性，滤手持抖动）；幻灯片式漂移（光流散度长期偏低则剔）；边框检测（边缘+霍夫变换）；文本检测（字幕也单独识别剔除）；Logo 检测（Florence-2 开放词表）；角落人脸检测（剔解说员）；转场检测。
- **去重（De-duplication）**：单独章节，移除重复片段。
- **标注（caption）**：
  - **高描述性 caption**：每视频抽 4–12 关键帧组成图像序列喂 MLLM；视频两阶段提示（先按预定义属性——场景数/转场/景别/相机运动/主体识别/主体属性/位置/动作做结构化分析，再生成最终描述）；图像直接生成。
  - **自回归 caption（AR caption）**：逐秒细粒度描述（首秒详细描述，后续秒只描述相对上一秒的变化），用于支撑 chunk-wise 文本可控性。
- **训练分阶段数据配置（Table 5）**：

| | stage-1 | stage-2 | stage-3 |
|---|---|---|---|
| 分辨率 | 256p/360p | 480p | 720p |
| 时长 | ≤8s | ≤8s | ≤16s |
| 图:视频比 | 4:1 | 4:1 | 4:1 |
| AR caption 比 | 0% | 10% | 10% |

- **动态分布调整**：训练中持续监测各语义概念表现（如发现"风景易学、人物表情难学"），动态调高欠拟合子集比例。多阶段则后期数据量递减、过滤更严、时长延到 16s。

## 训练方法
- **训练目标：flow-matching（rectified flow）**。对 n 个 chunk 各采独立高斯噪声，线性插值 xᵢᵗ=(1−t)xᵢ⁰+t·xᵢ¹，预测速度场 v*=xᵢ¹−xᵢ⁰。关键差异：施加**单调噪声约束** tᵢ<tⱼ（i<j，越往后越噪），且 chunk i 的速度预测**仅条件于其前序 chunk**（而非双向模型那样条件于全序列）。
- **多任务统一**：T2V/I2V/续帧只是"干净 chunk 占比"不同，单次预训练覆盖，无需任务专属微调。
- **多阶段训练**（以 4.5B 为例，三阶段）：阶段一/二分别 360p/480p、≤8s；阶段三 720p、≤16s；全程图像-视频联合训练。LR 先 1000 步 warmup 到 1e-4，前两阶段恒定（视觉评估无明显提升即切阶段），第三阶段验证 loss 平台期后逐步降到 1e-5。
- **训练 timestep 采样器**：视频比图像冗余多，故把采样分布**更偏向噪声侧**；经验上 t=0.3 模型已能出较清晰视频，故**~70% 训练算力分配在 t<0.3 区域**（m=0, s=0.5, w=1/3）。
- **蒸馏：Shortcut Model（捷径模型）**。单网络预测速度场 v(xᵗ|t,s)，额外条件于步长 s∝Δt；用 bootstrap 自一致性约束（一大步 = 两小步之和）学会近似不同步长的 flow-matching 轨迹。最小 s=1/64（标准 64 步设置），蒸馏步长**循环采样自 [1/64]×8 ∪ [1/32, 1/16, 1/8]**，使**单个蒸馏模型支持 64/32/16/8 步**多档推理预算；最小步长时引入 **CFG 蒸馏**保持条件对齐。
- **未涉及 RLHF/DPO/reward model**：MAGI-1 论文未报告偏好对齐 / RL 后训练阶段（区别于很多对齐流程；其"对齐"主要靠 caption 质量 + 动态数据分布 + CFG 调参）。

### 推理技巧
- **扩散引导（CFG）**：把引导分解为三项——无条件先验、前序 chunk 时序引导 w_prev、文本引导 w_text（公式 9）。发现 chunk 间有细微错位伪影，故把 **w_prev 提到 1.5**（>1.0 时显著改善 chunk 对齐、减闪烁；过大则饱和/画面变静止）；w_text=7.5。
- **推理 timestep 采样**：在 t'=w·tᵏ/(1−(1−w)tᵏ) 上加可调幂变换，**w=1/3、k=2** 视觉最好。
- **引导强度细粒度控制**：t≈0.3 后画面结构语义已基本成型（剩余步类似超分），故 t>0.3 时把 w_prev→1.0、w_text→0.0（只留 ∇log p(xᵢ|x<ᵢ)），显著缓解长视频（>5 秒）累积伪影。
- **KV Cache**：chunk 充分去噪后特征缓存复用；**限制 KV range**（如设 8 即每个新 chunk 只依赖前 8 秒）使长视频计算成本线性增长、峰值开销恒定；动态调不同去噪阶段的 KV range 还能实现可控转场（高噪阶段 KV range=1 → 换镜头保主体；低噪阶段 KV range=1 → 保布局换细节）。
- **Prompt Enhancement**：训练用高描述性 caption，但用户输入参差，故推理时用 SOTA MLLM 做提示增强（I2V 双子流程：描述图像内容 + 预测时序演变），再**蒸馏到 ~7B 小模型**（约 200 万样本语料），质量相当但延迟大降。

## Infra（训练 / 推理工程）
MAGI-1 的工程栈是其核心贡献之一（独立开源 MagiAttention）。

### 训练 Infra
- 不直接套用 Megatron/DeepSpeed（为 LLM 设计）：MAGI 架构更复杂（gating、cross-attn、block-causal），单条视频样本 token 量是文本的几十~几百倍且不能随意截断/拼接。
- **并行**：DP + CP（context parallelism）+ TP 组合。
- **分布式 Packing & Padding（PnP）**：在线把多条变长短序列打包成 batch（First-Fit Decreasing 贪心近似 bin-packing），减少冗余 padding、缓解 DP 负载不均与 GPU bubble。
- **MagiAttention**（独立开源 https://github.com/SandAI-org/MagiAttention）：面向超长 + 异构 mask 的分布式注意力，号称对 CP size 线性可扩展。四大组件：
  1. **Flex-Flash-Attention（FFA）**：基于 FA3，用 (QRange, KRange, MaskType) 三元组的 AttnSlice 公式表达各种 mask（含 varlen block-causal）；用 Hopper TMA + slice-level 并行 + 原子操作，MFU 与 FA3 相当。
  2. **Dispatch solver**：chunk-wise 可置换分片，O(n log n) 贪心做计算负载均衡。
  3. **Group-Cast / Group-Reduce 零冗余通信原语**：替代 ring-style P2P 的冗余通信，用 all-to-all-v 原型实现零冗余前后向通信。
  4. **Adaptive Multi-Stage Overlap**：可调 num_stages 自适应隐藏通信延迟。
- **DTensor 重构思路**：讨论用 PyTorch DTensor（Replicated/Shard/Partial 三种 placement）解耦"建模"与"并行"，让算法研究者与 infra 工程师解耦协作，并提出"可验证数值精度对齐非分布式 oracle"作为一等设计目标。
- **训练集群规模 / GPU·时 / MFU 等绝对数字：论文正文未披露**（VAE 与推理评测在单卡 H800 上做；训练用 H100/H800 类硬件但未给总卡数与训练时长）。

### 推理 Infra（两大场景，抠到具体数字）
- **场景一：H100/H800 实时流式**。两关键指标：TTFC（首 chunk 时延）、TPOC（后续每 chunk 时延）。要把 TPOC 压到 <1s，每秒视频约需 **9 PFLOPS** 算力，远超单卡，故 24B 模型用 **3 节点 24×H100** 部署。
  - **异构 serving**：T5 + MAGI 放高性能 GPU，VAE 放低成本硬件并发解码。
  - **量化**：W8A8 SmoothQuant 把权重/激活量化到 FP8（除首尾层），**提速 30% 且不掉质**。
  - **多节点并行**：Ulysses 序列并行，通信几乎完全重叠（未重叠 <3%）；24×H100/H800 上生成 480p(3:4) 16 步 KV range=5 时 **TPOC <1s**。
  - **首 chunk 优化**：首 chunk 仅几百 token、CPU-bound，用 CUDA Graph 降 30.4% 延迟；VAE 解码用 tile 并行 + torch.compile 从 1s 降到 ~70ms；**TTFC 最终 2.3~2.37s**。
  - 延迟优化表（Table 6）：自回归去噪模型 TPOC 从 baseline 45.49s → KV Cache 23.94s(1.9×) → Ulysses 1.26s(18×) → SmoothQuant 0.98s；端到端 TTFC 2.37s / TPOC 0.98s。
- **场景二：RTX 4090 低成本部署**。瓶颈是显存。技巧：SmoothQuant 量化 + **KV-offload（KV cache 放 CPU 内存按需调回）** + 混合并行（PP 切权重 + CP 切激活）+ **Context Shuffle Overlap（CSO）**（把每 chunk 均匀打散到所有 GPU，比朴素 Ulysses 更细粒度重叠，缓解 PCIe 瓶颈）。
  - 结果（arxiv v1 口径）：4.5B 单卡 4090 峰值 **19.07GB**；24B 在 **8×4090** 上峰值 19.29GB、**MFU 最高 66%**。（注：sand.ai 官网 PDF（2025-04-25 版，static.magi.world）的对应数字略有差异——4.5B 峰值 21.94GB、24B MFU 58%；24B 峰值 19.29GB 一致。本页采用 arxiv v1 数字。）

## 评测 benchmark（把效果讲清楚）

### VBench-I2V（Table 9，生成 4s/24FPS/16:9）
MAGI-1(2×decoder，2560×1440) **总分 89.28，VBench-I2V 排名第一**；MAGI-1(1×decoder，1280×720) 总分 88.88。
- 关键分项（2×/1×decoder）：Quality Score 82.44 / 81.67；I2V Score 96.12 / 96.08；**Dynamic Degree 68.21 / 63.41（显著领先 VisualPi 49.93、StepFun 48.78）**；Aesthetic Quality 64.74 / 61.89；Motion Smoothness 98.68；I2V-Subject 98.39；I2V-Background 99.00。
- 亮点：在保持高视觉质量（美学、运动平滑）的同时 Dynamic Degree 大幅领先——破解了"加大运动幅度往往掉画质"的常见 trade-off，作者归因于自回归去噪对复杂运动更强的建模能力。

### Physics-IQ 物理基准（Table 10，前 3s 条件、预测后 5s）
| Model | Phys.IQ↑ | Spatial IoU↑ | Spatio-Temporal↑ | Weighted IoU↑ | MSE↓ |
|---|---|---|---|---|---|
| **MAGI(V2V)** | **56.02** | 0.367 | 0.270 | 0.304 | 0.005 |
| VideoPoet(V2V) | 29.50 | 0.204 | 0.164 | 0.137 | 0.010 |
| Lumiere(V2V) | 23.00 | 0.170 | 0.155 | 0.093 | 0.013 |
| **MAGI(I2V)** | **30.23** | 0.203 | 0.151 | 0.154 | 0.012 |
| Kling1.6(I2V) | 23.64 | 0.197 | 0.086 | 0.144 | 0.025 |
| Gen3(I2V) | 22.80 | 0.201 | 0.115 | 0.116 | 0.015 |
| Wan2.1(I2V) | 20.89 | 0.153 | 0.100 | 0.112 | 0.023 |
| Sora(I2V) | 10.00 | 0.138 | 0.047 | 0.063 | 0.030 |
| GroundTruth | 100.0 | 0.678 | 0.535 | 0.577 | 0.002 |

- **V2V 模式 56.02 分压倒性领先**（比同样支持 V2V 的前 SOTA VideoPoet 高约 27 分）；即便仅图像条件(I2V) 30.23 仍是所有模型最高。作者归因：物理建模需要关注因果而非相关，自回归天然促进因果推理；VideoPoet 虽也自回归但主打与 LLM 集成、视频建模效率受限，而 MAGI 专为视频生成而建。
- **消融**：增加历史上下文（调大 KV range）总体提升物理分，但**最显著增益出现在 KV range=2**——短期历史常已足够。
- 局限：能抓主运动（抛射、旋转、形变），但难处理复杂二次效应（精确碰撞响应、材料特定反应、形变后行为）；不过即便偏离 GT，常生成"物理上合理的替代结果"。

### 人评（in-house human evaluation，100 image-prompt pairs，成对 Win/Tie/Lose）
- 整体优于开源 Wan-2.1；**略逊于商业 Kling1.6(HD)**；明显优于 Hailuo(i2v-01) 与 HunyuanVideo。
- 强项是**指令遵循**与**运动质量**；视觉质量相对顶尖模型仍有提升空间。
- README 口径：在开源（Wan-2.1、HunyuanVideo）与闭源 Hailuo 中达 SOTA，尤其指令遵循与运动质量出色，是 Kling 等商业模型的有力竞争者。

## 创新点与影响
**核心贡献**：
1. **首个从零训练的大规模分块自回归扩散视频模型**，在严格因果约束下用单次预训练统一 T2V/I2V/续帧（仅靠干净 chunk 占比区分），免任务专属微调。
2. **单调噪声 + chunk 流水线**带来真正的流式 / 实时能力与**与视频时长无关的恒定峰值开销**（KV cache + 限 KV range）。
3. **一整套大模型稳定性架构改造**（Parallel Attention Block、Softcap Modulation、Sandwich Norm、QK-Norm/GQA、可学习 3D RoPE）。
4. **Shortcut 蒸馏**单模型支持 8/16/32/64 多档步数。
5. **开源 MagiAttention**（FFA + 负载均衡 dispatch + 零冗余通信原语 + 自适应 overlap），对超长异构 mask 训练有独立价值。
6. **物理基准上自回归对因果建模的优势被定量验证**（Physics-IQ 大幅领先），强化了"视频生成→世界模型"的论点。
7. **开放程度高**：Apache-2.0 权重（24B / 4.5B 及 distill / distill+fp8_quant），可在单卡 RTX 4090 跑 4.5B、8×4090 跑 24B。

**影响 / 后续**：作为"分块自回归扩散"路线的规模化样板，与 Diffusion Forcing / CausVid / Wan 自回归变体一起推动了"因果视频生成 + 实时流式"方向。README 显示项目持续迭代：2025-05 发 4.5B distill/quant、加 ComfyUI 支持；**2026-06-17 开源 MAGI-1.1 24B**（蒸馏前 base + 蒸馏后 + 量化版，本页技术分析基于 v1 技术报告/2505.13211，MAGI-1.1 的具体改动论文未覆盖）。

**已知局限**：视觉质量略逊 Kling 等顶尖商业模型；物理上难处理复杂二次效应（碰撞/材料反应/形变后行为）；训练侧绝对算力规模 / GPU·时未公开；未做 RLHF/DPO 类偏好对齐。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2505.13211
- arxiv_pdf: https://arxiv.org/pdf/2505.13211
- arxiv_html(精读源): https://arxiv.org/html/2505.13211v1
- 官方技术报告 PDF: https://static.magi.world/static/files/MAGI_1.pdf （28MB，可达；与 arxiv 同名报告，但为 2025-04-25 较早修订，部分数字与 arxiv v1 不同——见上文 4090 内存/MFU 注。本页统一以 arxiv v1 为准，arxiv v1 PDF 已落盘）
- github: https://github.com/SandAI-org/MAGI-1
- github(MagiAttention): https://github.com/SandAI-org/MagiAttention
- hf model card: https://huggingface.co/sand-ai/MAGI-1
- hf papers: https://huggingface.co/papers/2505.13211
- 产品: https://sand.ai ， https://magi.sand.ai
- 公司主页: https://sand.ai

## 本地落盘文件
- ../../../sources/omni/2025/magi-1--arxiv-html.md   （arxiv v1 全文 markdown，约 255KB，主精读源）
- ../../../sources/omni/2025/arxiv-2505.13211.pdf   （arxiv v1 PDF，28.3MB，本页所有数字以此为准；*.pdf 不入 git，备份 HF bucket）
- ../../../sources/omni/2025/magi-1--github-readme.md   （GitHub README，含 model zoo / 评测表 / MAGI-1.1 更新日志）
- ../../../sources/omni/2025/magi-1--hf-modelcard.md   （HF model card）
- ../../../sources/omni/2025/magi-1--hf-papers.md   （HF papers 页面快照）
