---
title: "Cosmos World Foundation Model Platform for Physical AI (Cosmos-Predict1)"
org: NVIDIA
country: US
date: "2025-01"
type: tech-report
category: video
tags: [world-model, physical-ai, video-generation, diffusion, autoregressive, dit, tokenizer, robotics, autonomous-driving, open-weight]
url: "https://arxiv.org/abs/2501.03575"
arxiv: "https://arxiv.org/abs/2501.03575"
pdf_url: "https://arxiv.org/pdf/2501.03575"
github_url: "https://github.com/nvidia-cosmos/cosmos-predict1"
hf_url: "https://huggingface.co/collections/nvidia/cosmos-predict1-67c9d1b97678dbf7669c89a7"
modelscope_url: ""
project_url: "https://research.nvidia.com/labs/dir/cosmos-predict1"
downloaded: [arxiv-2501.03575.pdf, cosmos-predict--predict1-readme.md, cosmos-predict--github-readme.md, cosmos-predict--nvidia-blog.md, cosmos-predict--hf-card-page.md, cosmos-predict--hf-diffusion-7b-t2w.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
NVIDIA Cosmos 是面向「物理 AI（机器人 / 自动驾驶）」的**世界基础模型（World Foundation Model, WFM）平台**，一次性开源了一整套流水线：视频数据策展管线 + 因果视频 tokenizer 家族 + 两条并行技术路线的预训练世界模型（**扩散式 DiT** 与 **自回归 GPT**，规模 4B–14B）+ 下游 post-training 示例（相机控制 / 机器人操作 / 自动驾驶）+ guardrail 安全系统。模型在 **10,000 张 H100 上训练约 3 个月**、预训练语料约 **9000 万亿（9000T）token / 2000 万小时视频**，并以 NVIDIA Open Model License 开放权重，是把「video2world 视频预测」当作物理世界数字孪生来系统工程化的标志性开源工作。

## 背景与定位
物理 AI（带传感器与执行器、能感知并改变物理世界的 AI，如机器人/自动驾驶）的核心瓶颈是**数据规模化困难**：真实世界采集「观测-动作」交错序列代价高、且探索性动作有安全风险。WFM 的定位是做一个「物理世界的数字孪生」——给定过去观测 $x_{0:t}$ 与当前扰动 $c_t$（动作/文本/随机扰动），预测下一帧观测 $\hat{x}_{t+1}$，从而让策略可以安全地在模型里被评估、初始化、训练（RL）、做 MPC 规划，以及生成合成数据。

技术脉络上，Cosmos 把 WFM 落到**条件视频生成模型**这一现代范式（相对早期 Ha & Schmidhuber 的 RNN 世界模型），并明确采取「预训练通才 WFM → 下游小数据 post-training 专才」的两段式策略。它同时押注扩散与自回归两条路线——前者承袭 [[latent-diffusion-ldm]] / DiT（[[scalable-diffusion-dit]]）/ EDM 体系，后者承袭 LLM/VideoPoet 的离散 token next-token 范式——并把对比留给社区。与同期 Sora、HunyuanVideo、MovieGen、Kling 等「美学向」文生视频不同，Cosmos 明确**牺牲艺术表现力换取物理真实性**（官方称输出"lack artistic flair"但贴近真实世界物理），评测维度也独创性地加入 **3D 一致性** 与 **物理对齐**，而非只看 FID/美学。

注：本页对象是论文/worklist 中的 **Cosmos-Predict1**（2025-01 首发）。NVIDIA 后续于 2026 年发布了统一 MoT 架构的 Cosmos 3（Reasoner+Generator omnimodal），属另一代工作，本页不展开。

## 模型架构

平台含三大可学习组件：**视频 tokenizer**、**扩散 WFM**、**自回归 WFM**，外加 prompt upsampler 与 diffusion decoder 两个辅助件。全套模型见下表（论文 Tab.10）：

| 路线 | 基座 | 衍生 Video2World | tokenizer | 增强件 |
|---|---|---|---|---|
| 扩散 | Predict1-7B / 14B-Text2World | →7B / 14B-Video2World | Cosmos-Tokenize1-CV8×8×8-720p（连续） | Cosmos-UpsamplePrompt1-12B（Mistral-NeMo-12B 微调） |
| 自回归 | Predict1-4B / 12B | →5B / 13B-Video2World | Cosmos-Tokenize1-DV8×16×16-720p（离散） | Predict1-7B-Decoder（DV→CV 扩散解码器） |

### 1) Cosmos Tokenizer（因果视频 tokenizer 家族）
- **统一因果设计**：用因果时序卷积 + 因果时序注意力，保证当前帧 token 只依赖过去帧。好处有二——(a) 单一网络同时是图像 tokenizer（输入单帧 $T=0$）和视频 tokenizer，使图文联合训练成为可能；(b) 因果性天然契合物理 AI 的因果世界。
- **wavelet 空间操作**：输入先过 2 级 3D Haar 小波变换（沿 x/y/t 各 ×4 降采样），在更紧凑、去冗余的表示上做后续语义压缩；编码器为残差块 + 下采样块，用**时空分解 3D 卷积**（先 $1\times k\times k$ 空间卷积，再 $k\times1\times1$ 时序卷积，左 padding $k-1$ 保证因果）+ 时空分解因果自注意力；激活用 Swish，归一化用 LayerNorm（而非 GroupNorm，避免 latent 局部出现大幅值）。
- **量化**：连续 tokenizer 用 vanilla AE（latent 维度 16，**不用 KL 先验损失**）；离散 tokenizer 用 **FSQ**（Finite-Scalar-Quantization，6 维 latent、levels=(8,8,8,5,5,5)）→ **词表 64,000**（不用 VQ-VAE 的 commitment loss）。
- **压缩档位**：图像 8×8 / 16×16；视频 4×8×8 / 8×8×8 / 8×16×16（记号 $T\times H\times W$）。支持 1:1、3:4、4:3、9:16、16:9 多宽高比，且时序长度无关（推理可超训练长度）。WFM 主用：扩散用 CV8×8×8-720p，自回归用 DV8×16×16-720p。

### 2) 扩散 WFM（DiT 改造，denoiser $D_\theta$）
基于 DiT，改造用于可控视频生成：
- **3D patchification**：latent $T\times C\times H\times W$，用 $p_t{=}1, p_h{=}p_w{=}2$ 的 cube 线性投影展平成 1D 时空序列。
- **混合位置编码**：3D 分解 RoPE（特征维度三等分，分别沿 t/h/w 施加，复用 LLM RoPE kernel；按 FPS 缩放时序频率以支持变帧率）+ 每块额外的**可学习绝对位置编码**（降 loss、减 morphing 伪影）；渐进训练换分辨率时借 NTK-RoPE 可 5,000 步快速收敛。
- **文本注入**：每个 transformer 块 = 自注意力 → 交叉注意力（**T5-XXL** embedding 作 K/V，序列定长 512 零填充）→ FFN（GELU），由 AdaLN（scale/shift/gate）按时间步调制。
- **稳定性 trick**：QK-Norm（RMSNorm + 可学习 scale）抑制注意力 logit 爆炸；**AdaLN-LoRA** 把 AdaLN 的 dense 投影低秩化——7B 模型据此从 11B 砍到 7B（**参数量 −36%** 且指标无损）。
- **Video2World**：在 Text2World 基础上，把条件帧沿时序维拼接进生成帧、沿通道维拼二值 mask 区分条件/生成帧，对条件帧加噪声增广（$P_{mean}{=}-3.0, P_{std}{=}2.0$），loss 仅算生成帧；训练时随机条件帧数，推理可接 1 帧（图）或多帧。
- **配置**（Tab.11）：7B = 28 层 / dim 4096 / FFN 16384 / 32 头；14B = 36 层 / dim 5120 / FFN 20480 / 40 头；AdaLN-LoRA 维度 256。

### 3) 自回归 WFM（Llama3-style GPT，next-token）
把视频转成离散 token 序列做 next-token 预测（NLL loss），架构刻意贴近 LLM 以复用其生态：
- **位置编码**：3D 分解 RoPE（$\theta{=}500{,}000$，时序轴用 **YaRN** 外推扩长）+ 3D 正弦绝对位置编码（APE，与扩散侧的可学习 APE 不同）。
- **文本注入**：每个自注意力层后插交叉注意力，K/V 来自 **T5-XXL**（基座 4B/12B 是纯视频 next-token、无语言理解，Video2World 版才加文本 cross-attn）。
- **稳定性**：QK-Norm（学习 scale $\gamma$ 替代固定 $1/\sqrt{d_k}$）+ **z-loss**（$\lambda{=}3\times10^{-4}$，约束 logit 防梯度爆炸，扩到多节点时关键）。
- **配置**（Tab.14）：4B = 16 层 / dim 4096；12B = 40 层 / dim 5120；统一 SwiGLU、FFN 14336、32 头 / **8 KV 头（但论文明确说没用 MQA/GQA）**、序列 12,800 token、词表 64,000、固定分辨率 640×1024。

### 4) 两个辅助件
- **Prompt Upsampler**：训练用的是 VLM 生成的长 caption，与用户短 prompt 分布有 gap。Text2World 侧微调 **Mistral-NeMo-12B-Instruct**（用 VLM 把长 prompt 反向生成短 prompt 造配对数据）；Video2World 侧直接零样本用开源 **Pixtral-12B**（开箱即用，未微调）。
- **Diffusion Decoder**：离散 tokenizer 压得太狠（8×16×16）会糊，故微调 Predict1-7B-Text2World 做一个「DV8×16×16 → CV8×8×8」的条件扩散解码器：把离散 token 嵌成 16 维向量、2× 上采样后沿通道维与噪声连续 latent 拼接做条件，去噪还原出更清晰的连续 token 视频，再用 CV tokenizer 解出 RGB。

## 数据

- **原始规模**：约 **2000 万小时**原始视频（720p–4k），来自专有数据集 + 公开互联网开放域视频。官方博客折算为**约 9000 万亿（9000T）token**预训练语料。
- **领域配比**（面向物理 AI 精心配比）：驾驶 11% / 手部动作与物体操作 16% / 人体动作与活动 10% / 空间感知与导航 16% / 第一人称视角 8% / 自然动态 20% / 动态相机运动 8% / 合成渲染 4% / 其他 7%。
- **5 步策展管线**（Sec.3，对应开源 NeMo Curator / cosmos-curator）：
  1. **Split 切分**：用 **TransNetV2**（自建 ShotBench 基准上 F1 最高、对重剪辑视频更稳，胜过 PySceneDetect/Panda70M/AutoShot）做 shot 检测，<2s 丢弃、>60s 再切；GPU 转码统一成 h264_nvenc mp4（用 PyNvideoCodec 替代 ffmpeg 调度 NVDEC/NVENC，转码吞吐提升约 **6.5×**）。
  2. **Filtering 过滤**：运动过滤（TensorRT 加速光流 + ViT 分类器，去静态/抖动并打 pan/zoom/tilt 标签）；视觉质量过滤（DOVER 去底部 15% 失真、LAION 美学模型阈值 3.5）；叠加文字过滤（InternVideo2 embedding + MLP 分类器去后期加字幕的视频）；视频类型过滤（按自建 taxonomy 上采样人物交互、下采样风景/动画/游戏画面）。
  3. **Annotation 标注**：用内部 **13B VILA**（FP8 TensorRT-LLM 引擎，吞吐 ×10）给每 256 帧出一条 caption，平均 559 字符 / 97 词；每 256 帧一条、聚焦事实细节，避免依赖 alt-text。
  4. **Dedup 去重**：复用 InternVideo2 embedding，GPU k-means（$k{=}10{,}000$）做语义去重（SemDeDup/DataComp 方案），**删掉约 30%** 数据；同 embedding 还建了文本/视频检索引擎用于调试。
  5. **Sharding 分片**：按分辨率/宽高比/长度打包成 webdataset；另用更严格过滤造高质量微调集。
- **产出**：预训练约 **1 亿（10^8）clip**（2–60s），微调约 **1000 万（10^7）clip**；图文数据联合训练以提升画质、加速收敛。
- **下游 post-training 数据**：机器人用 Cosmos-1X（指令跟随）/ Bridge（动作条件）数据集；自动驾驶用内部 **RDS（Real Driving Scene）**——约 360 万条 20s 六视角环视视频（约 2 万小时），含 ego 运动/天气/光照/车速/路型等属性标签并二次挖掘罕见路况。

## 训练方法

- **总规模**：所有模型在 **10,000 张 NVIDIA H100** 集群上、约 **3 个月**完成（论文原文）。
- **扩散侧目标**：采用 **EDM**（Karras 2022/2024）的去噪 score matching，preconditioning 与噪声分布 $\ln\sigma\sim\mathcal{N}(P_{mean},P_{std}^2)$ 按 EDM；引入**基于不确定性的逐噪声级加权**（MLP 参数化 $u(\sigma)$，把多噪声级当多任务学习，自适应平衡）。论文指出 EDM score matching 与 flow matching 理论等价、实践无性能瓶颈。
- **扩散侧训练策略**：
  - **图文联合训练**：交替图/视频 batch；用域特定归一化对齐图/视频 latent 分布、对视频做逐帧逐通道标准化逼近各向同性高斯；视频 batch 噪声级按帧数平方根缩放以补偿视频收敛慢。
  - **渐进训练 3 阶段**（Tab.12）：512p/57 帧（ctx 10,240）→ 720p/121 帧（ctx 56,320）→ 720p/121 帧高质量微调（$\mathcal{O}(10k)$ 步、LR 线性衰减）。
  - **多宽高比**：5 个 bucket，每个 DP 进程组采一个 bucket，longest-side resize + 反射填充 + padding mask。
  - **混合精度**：BF16 前反向 + FP32 主权重/优化器态 + FP32 EMA；loss 放大 ×10、调小 AdamW 的 $\beta$/$\epsilon$ 抑制 loss spike（14B 训练几乎无不可恢复 spike）。
  - **CFG**：Text2World 用 classifier-free guidance，但**不随机置零文本**（靠推理负 prompt + 高质量数据达成 mode-seeking 效果）；图像生成低 guidance 即可，视频因高质量数据稀缺需较高 guidance。
  - 超参（Tab.11）：base LR $2^{-15}$（7B）/ $2^{-16}$（14B），weight decay 0.1/0.2，warmup 2500 步，AdamW $\beta{=}(0.9,0.99), \epsilon{=}10^{-10}$。
- **自回归侧训练策略**（多阶段，Tab.14）：
  - Stage 1：单帧条件预测 16 帧（ctx 17 帧）→ Stage 1.1：扩到 34 帧（YaRN 扩时序）→ Stage 2：加文本 cross-attn（新初始化）、图文联合，固定 640×1024。
  - **Cooling-down**：仿 LLM，预训练后用高质量图-视频对、LR 线性衰减到 0，跑 **30,000** 步。
  - base LR $1\times10^{-3}$（基座）/ $3$–$5\times10^{-4}$（Video2World），weight decay 0.01，warmup 5000 步。
  - 经验：自回归 Text2World 用 upsampled prompt **不涨点**（推测因大部分训练是纯视频生成、对文本利用不够强）。

## Infra（训练 / 推理工程）

- **数据 infra**：基于 **AnyScale Ray** 的流式管线，解耦数据传输与计算、支持跨地理分布集群；用扩展版 Fragmentation Gradient Descent 调度做多资源（网络带宽 / NVDEC / GPU）并发分配与自动扩缩，平衡各专用加速器吞吐。
- **扩散并行**：14B 模型参数+梯度+优化器态约 **280GB**、激活约 **310GB**（720p 预训练），远超 H100 80GB。用 **FSDP**（sharding 因子 7B=32 / 14B=64，把 280GB 降到约 4GB/卡）+ **Context Parallelism**（CP_SIZE=8，用 TransformerEngine 的 P2P 变体重叠通算，把激活 310GB 降到约 40GB/卡；CP 组放在 NVLink 内、与 FSDP rank 重叠；图像短上下文关 CP，cross-attn 不用 CP）。**刻意不用 TP/SP**（相比 HunyuanVideo/MovieGen 更精简）却仍达可比 MFU。参数 10 bytes/参数（FP32+BF16+EMA）。
- **自回归并行**：12B 参数+梯度+优化器态约 **192GB**，用 **TP + Sequence Parallelism**（Megatron 体系）切分；未来才上 CP/PP 扩更大模型。
- **推理加速（自回归侧重点）**：
  - KV cache + TP + `torch.compile`（gpt-fast）。
  - **Medusa 推测解码**：加多个 Medusa head（单层 FFN+SiLU+残差，并入统一 FFN；不用 tree attention；只解冻最后 2 层 transformer + unembedding 微调）。**9 个 head** 性价比最佳：4B 提速达 **2.0× 吞吐 / 4.6× 减前向**，5B 达 **3.2× 吞吐 / 6.1× 减前向**（8×H100、50 段 640×1024 测试视频）。
  - **低分辨率实时**：把 tokenizer 与 4B WFM 微调到 320×512 + Medusa，8×H100 上达 **806 tokens/s ≈ 10 帧/s**，**实现 10 FPS 实时生成**。
- **扩散推理（HF 卡，单 H100，端到端）**：7B-Text2World **约 380 秒**、14B-Text2World **约 590 秒**生成一段；显存：全 offload 后扩散模型峰值约 24.4–39.0GB（可在 RTX 3090/4090 24GB 上跑全 offload）。
- **部署形态**：开源代码（Apache 2.0）+ 开放权重（NVIDIA Open Model License）发布于 HF / NGC；guardrail 含 Llama Guard 3 单独许可；亦提供 NeMo Framework 训练栈、NeMo Curator 数据栈、NVIDIA API catalog。

## 评测 benchmark（把效果讲清楚）

Cosmos 不走传统 FID/美学评测，而是自建 **3D 一致性** 与 **物理对齐** 两套 benchmark（基线统一为 VideoLDM）。

### Tokenizer 重建质量（DAVIS / TokenBench，论文 Tab.5/6）
- 连续视频 tokenizer 在 DAVIS 上 +4 dB PSNR 超现有 SOTA、最高 **12× 更快**；单张 A100 80GB 可一次性编 1080p 8s / 720p 10s。
- Cosmos-Tokenize1-CV8×8×8-720p（121 帧）DAVIS **PSNR 31.28 / SSIM 0.868 / rFVD 23.49**；CV4×8×8-360p 达 **PSNR 35.85**（对比 CogVideoX-CV4×8×8 PSNR 29.29、Omni-Tokenizer 22.23）。
- 离散 DV8×16×16-720p（49 帧）DAVIS PSNR 25.49；DV4×8×8-360p PSNR 32.97（FSQ 优于 VQ：Omni/VideoGPT 的 VQ 同档明显更低）。

### 3D 一致性（500 段 RealEstate10K 静态场景，论文 Tab.19 / 博客 Tab.1）
| 模型 | Sampson Error ↓ | 位姿估计成功率 ↑ | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
|---|---|---|---|---|---|
| VideoLDM（基线） | 0.841 | 4.4% | 26.23 | 0.783 | 0.135 |
| **Predict1-7B-Text2World** | **0.355** | 62.6% | **33.02** | **0.939** | **0.070** |
| Predict1-7B-Video2World | 0.473 | **68.4%** | 30.66 | 0.929 | 0.085 |
| Predict1-4B（AR） | 0.433 | 35.6% | 32.56 | 0.933 | 0.090 |
| Predict1-5B-Video2World（AR） | 0.392 | 27.0% | 32.18 | 0.931 | 0.090 |
| 真实视频（参考） | 0.431 | 56.4% | 35.38 | 0.962 | 0.054 |

→ 7B 扩散模型的 Sampson error / 位姿成功率甚至优于真实视频参考值，几何 3D 一致性显著超基线。

### 物理对齐（PhysX + Isaac Sim 造 8 类物理场景、800 段 1080p，论文 Tab.20 / 博客 Tab.2）
- 指标：PSNR / SSIM（像素级）、DreamSim（特征级）、Avg. IoU（SAMURAI 跟踪算的物体级），33 帧上算。
- 关键结论（**而非"越大越好"**）：(a) 9 帧条件 > 1 帧条件（能估出速度/加速度）；(b) **扩散 WFM 像素级优于自回归 WFM**（与画质观察一致）；(c) **更大模型在物理对齐上并不更好**——所有 WFM 都同样难以严格遵守物理（缺物体恒存性、接触动力学不准），需更好数据策展与模型设计。例：7B-Video2World prompt+9 帧 PSNR 21.06 / IoU 0.592；14B prompt+9 帧 IoU 0.598。

### 下游 post-training 评测
- **机器人指令跟随**（Cosmos-1X，10 人评 23 episode）：Predict1-7B-Video2World-Instruction **78.3%** 总体偏好 vs VideoLDM-Instruction 13.0%；5B 版 56.5%；四维度（指令跟随/物体恒存/真实性/总体）全面胜出。
- **机器人动作条件**（Bridge，100 episode，Tab.23）：7B-ActionCond **PSNR 21.14 / SSIM 0.82 / FVD 190**，5B 版 FVD 434，均胜基线 IRASim-Action（FVD 593）。
- **自动驾驶多视角**（RDS，Tab.24/25）：7B-Text2World-MultiView **FID 32.16 / FVD 210.23**（基线 VideoLDM-MultiView 60.84 / 884.46）；多视角一致性 TSE 0.68 / CSE 2.11（接近真实视频 0.69 / 1.71）；加 trajectory 条件后轨迹跟随误差 **TFE 20.20cm**（真实 oracle 13.49cm，仅差 <7cm）；20 段视频 157 个物体跟踪**零物理不可能现象**。
- **相机控制**（Sec.6.1）：相机位姿条件 post-training 后位姿估计成功率较基线**翻倍**（博客亦确认 "twofold increase"）。

## 创新点与影响

**核心贡献**
1. **平台化开源**：把「数据策展 → tokenizer → 预训练 WFM → 下游 post-training → guardrail」整条物理 AI 世界模型流水线一次性开源/开权重（Apache 2.0 代码 + NVIDIA Open Model License 权重），并配 NeMo Curator/Framework，显著降低物理 AI 数据规模化门槛。
2. **双路线并举**：在同一平台同时给出扩散（画质更高、易接多种控制信号与多视角输出）与自回归（可继承 LLM 世界知识、可用 LLM 推理加速做实时/交互）两条 WFM，并系统对比其优劣（论文明确：扩散当前画质更优，自回归潜力未释放，且二者边界可融合）。
3. **因果 wavelet tokenizer + FSQ**：统一图像/视频、因果、多档压缩、多宽高比，DAVIS +4dB / 12× 提速，为下游物理 AI 因果设定量身打造。
4. **新评测维度**：把 3D 一致性（Sampson error / 位姿 / 新视角合成）与物理对齐（PhysX 仿真对比 + 物体级 IoU）引入视频世界模型评测，比纯美学/FID 更贴合物理 AI 需求。
5. **工程 trick 集**：AdaLN-LoRA（−36% 参数）、不确定性加权 EDM、Medusa 视觉自回归加速（首批把 Medusa 用于视觉 AR 并达 3.2× 吞吐、10FPS 实时）、扩散 decoder 救离散压缩损失。

**影响**：作为 Cosmos WFM 三大分支（[predict 预测 / transfer 迁移 / reason 推理]）之一，Predict1 成为机器人/自驾领域世界模型与合成数据生成的开源基座之一，被广泛 fine-tune；其因果 tokenizer、物理对齐 benchmark、双路线方法论影响后续工作；NVIDIA 据此演进出 Cosmos-Transfer1、Cosmos-Reason1，并最终统一为 2026 的 Cosmos 3（MoT，omnimodal Reasoner+Generator）。

**已知局限**（论文 Sec.9 + 博客）：当前 WFM 仍非可靠物理模拟器——缺物体恒存性、接触密集动力学不准、指令跟随不稳；生成的真实感不总等同于遵守引力/光照/流体等物理定律；输出偏低分辨率、"缺艺术表现力"；评测本身难（人评物理真实度主观、与下游指标未必正相关），未来方向是多模态 LLM 自动评测器 + 物理仿真器闭环；论文也坦言只给出平台与组件，policy evaluation/initialization/RL 等 WFM 下游用法尚未给实证结果（留作 future work）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2501.03575
- arxiv_pdf: https://arxiv.org/pdf/2501.03575
- paper_website: https://research.nvidia.com/labs/dir/cosmos-predict1
- github (cosmos-predict1 原仓库): https://github.com/nvidia-cosmos/cosmos-predict1
- github (Cosmos 总仓库，现指向 Cosmos 3): https://github.com/NVIDIA/Cosmos
- nvidia_blog (发布博客，2025-01-09): https://developer.nvidia.com/blog/advancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform/
- hf (Cosmos-Predict1 collection): https://huggingface.co/collections/nvidia/cosmos-predict1-67c9d1b97678dbf7669c89a7
- hf (示例模型 model card): https://huggingface.co/nvidia/Cosmos-1.0-Diffusion-7B-Text2World
- product: https://www.nvidia.com/en-us/ai/cosmos/

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2501.03575.pdf （论文全文，43MB，已 pdftotext 精读）
- ../../../sources/omni/2025/cosmos-predict--predict1-readme.md （cosmos-predict1 原仓库 README，含完整模型清单/许可）
- ../../../sources/omni/2025/cosmos-predict--github-readme.md （NVIDIA/Cosmos 总仓库 README，现已升级到 Cosmos 3）
- ../../../sources/omni/2025/cosmos-predict--nvidia-blog.md （NVIDIA 官方发布博客快照，含 9000T token / NeMo 栈 / 评测表）
- ../../../sources/omni/2025/cosmos-predict--hf-card-page.md （HF 示例模型卡页面快照，含输出规格/H100 推理耗时/显存）
- ../../../sources/omni/2025/cosmos-predict--hf-diffusion-7b-t2w.md （HF raw README，gated 提示，仅留痕）
