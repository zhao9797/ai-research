---
title: "HunyuanVideo: A Systematic Framework For Large Video Generative Models"
org: Tencent
country: China
date: 2024-12
type: tech-report
category: video
tags: [video, t2v, dit, flow-matching, mmdit, 3d-vae, open-source, scaling-law]
url: https://arxiv.org/abs/2412.03603
arxiv: https://arxiv.org/abs/2412.03603
pdf_url: https://arxiv.org/pdf/2412.03603
github_url: https://github.com/Tencent-Hunyuan/HunyuanVideo
hf_url: https://huggingface.co/tencent/HunyuanVideo
modelscope_url:
project_url: https://aivideo.hunyuan.tencent.com
downloaded: [arxiv-2412.03603.pdf, arxiv-2412.03603.txt, hunyuan-video--readme.md, hunyuan-video--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
HunyuanVideo 是腾讯混元 2024 年 12 月开源的 **13B 参数**文生视频基础模型——发布时**最大的开源视频生成模型**，用 Causal 3D VAE + 「双流→单流」全注意力 DiT + Flow Matching，系统性地披露了数据、架构、scaling law 与 infra。在 1,533 prompt、60 名专业评测员的人评里，**整体满意度第一（41.3%）**，超过 Gen-3 alpha、Luma 1.6 及三家中国头部闭源商业模型，尤其在运动质量上领先。

## 背景与定位
2024 年视频生成领域的强模型（Sora、Gen-3、Luma、MovieGen 等）几乎全是闭源，开源社区缺乏一个像 [[stable-diffusion-1]] / [[flux-1]] 之于 T2I 那样的强基础模型，导致视频生成方向的算法创新停滞。HunyuanVideo 的目标就是「弥合开源与闭源视频基础模型的差距」（报告副标题），把数据管线、架构、scaling、训练、infra 一整套系统全部开源开放，让社区能在强 base 上做下游探索。

技术脉络上它沿用了图像生成成熟范式并迁移到视频：[[latent-diffusion-ldm]] 的隐空间扩散思想 → [[dit-scalable-diffusion-transformers]] 的 Transformer backbone → [[flux-1]] 的「双流到单流」MMDiT 设计 → [[stable-diffusion-3]] 的 Flow Matching / logit-normal 时间步采样。相对前置工作的关键改进：（1）从零训练 Causal 3D VAE（不复用预训练图像 VAE），重建质量超过 FLUX-VAE / CogVideoX-1.5 / Cosmos-VAE；（2）系统性建立 **T2I→T2V 两段式扩散 scaling law**，把「随机堆数据/算力/参数」的成本降低最多 **5×**；（3）用 **MLLM（decoder-only）替代 T5/CLIP** 作主文本编码器。

## 模型架构
**整体管线**：像素视频/图像 → Causal 3D VAE 压到隐空间 → patchify 成 1D token 序列 → DiT backbone（文本作条件）→ 输出隐变量 → 3D VAE 解码回视频。

**Causal 3D VAE（视觉 tokenizer）**
- 用 CausalConv3D，把 (T+1)×3×H×W 的视频压成 (T/4+1)×16×(H/8)×(W/8)，即时间压缩 ct=4、空间压缩 cs=8、隐通道 C=16。这种高压缩比大幅减少送进 DiT 的 token 数，使其可在原始分辨率与帧率上训练。
- **从零训练**（不用预训练图像 VAE 初始化），视频:图像数据按 **4:1** 混合。损失 = L1 + 0.1·LPIPS + 0.05·GAN对抗损失 + 1e-6·KL。课程学习：从低分辨率短视频逐步到高分辨率长视频；为改善高速运动重建，随机用 1~8 的采样间隔抽帧。
- 推理用 **时空 tiling**（空间/时间维切重叠 tile，重叠区线性混合）解决单卡 OOM，可在任意分辨率/时长下编解码；并额外加一个「训练时随机启/停 tiling」的微调阶段消除 tiling 伪影。
- 重建 PSNR：ImageNet 256×256 达 **33.14**（FLUX-VAE 32.70、CogVideoX-1.5 31.73、Cosmos-VAE 30.07）；MCL-JCV 视频 **35.39**（CogVideoX-1.5 33.22、Cosmos-VAE 32.76），视频/图像均 SOTA。

**Diffusion backbone（13B DiT）**
- 采用**统一全注意力（Full Attention）**而非时空分离注意力，理由：性能更好、图像/视频统一生成、可复用 LLM 加速生态。图像被当作单帧视频统一处理。
- 「**双流→单流**」混合设计（借鉴 [[flux-1]]）：双流阶段视频 token 与文本 token 各自走多个 Transformer block 学各自的 modulation；单流阶段把两者 concat 进后续 block 做多模态融合。
- 位置编码用 **3D RoPE**：把特征通道分成 (dt, dh, dw) 三段，分别乘以时/高/宽坐标的旋转频率再拼接，支持多分辨率、多宽高比、多时长生成。
- 架构超参（Table 2）：**20 个双流 block + 40 个单流 block**，model dim 3072，FFN dim 12288，**24 个注意力头**，head dim 128；3D RoPE 的通道分段 (dt,dh,dw)=(16,56,56)（三段相加 = head dim 128）。patchify 用 kt×kh×kw 的 3D 卷积核（报告未给出具体核尺寸数值）。

**文本编码器**
- 主编码器用**预训练 MLLM（decoder-only，因果注意力）替代 T5-XXL**。优势：视觉指令微调后的 MLLM 图文对齐更好、细节描述与复杂推理能力强、可作 zero-shot learner（在 user prompt 前加 system instruction 引导）。因 MLLM 是因果注意力，额外加一个**双向 token refiner** 增强文本特征。
- 同时保留 **CLIP-Large** 的池化全局文本特征（取最后非 padding token），扩维后加到 timestep embedding，注入双流与单流 block 作全局引导。

## 数据
- **图文视频联合训练**。视频分 5 组、图像分 2 组，分别适配不同训练阶段。
- **来源与合规**：原始视频覆盖人物/动物/植物/风景/车辆/物体/建筑/动画等领域；数据获取遵循 GDPR，使用数据合成与隐私计算保障合规。采集时设最低时长等基础阈值，部分子集用更严标准（空间质量、特定宽高比、构图/色彩/曝光的专业标准）。
- **分层过滤管线**（Figure 4）：PySceneDetect 切单镜头片段 → OpenCV Laplacian 选清晰起始帧 → 内部 VideoCLIP 算 embedding 去重 → OCR/清晰度/运动等多重过滤器，**逐阶段提高阈值**构建 256p / 360p / 540p / 720p **四个训练数据集**（视频空间分辨率从 256×256×65 升到 720×1280×129），每阶段会过滤掉上一阶段 1/2 到 4/5 的数据。图像复用大部分过滤器（去掉运动相关），从数十亿图文对里构建两个图像训练集（第一阶段数十亿、第二阶段数亿）。
- **SFT 微调集**：约 **100 万样本**，全程人工标注，按美学（色彩和谐、光照、主体强调、空间布局）与运动（运动速度、动作完整性、运动模糊）两个维度分解评分，挑视觉佳且运动细节丰富的片段。
- **结构化 re-captioning**：自研 in-house VLM 生成 **JSON 结构化字幕**，含短描述、密集描述（含转场/运镜）、背景、风格、镜头类型、光照、氛围 7 个维度，外加来源/质量等元数据标签；用 dropout + 排列组合机制合成长短/句式各异的字幕，提升泛化防过拟合。另训一个**14 类运镜分类器**（zoom in/out、pan、tilt、around、static、handheld 等），高置信预测写入 JSON 实现运镜控制。

## 训练方法
- **训练目标：Flow Matching**（rectified flow 框架）。t 从 logit-normal 分布采样，x0~N(0,I)，xt 用线性插值构造，模型预测速度场 ut=dxt/dt，损失为预测速度 vt 与真值 ut 的 MSE。推理用一阶 Euler ODE solver 积分得 x1。
- **多阶段渐进训练**：
  1. **图像预训练 stage 1（256px）**：低分辨率多宽高比训练，学更多低频概念。
  2. **图像预训练 stage 2（混合尺度）**：发现直接在 512px 微调会严重劣化 256px 生成，故提出 **mix-scale training**——每个 global batch 含 256px、512px 两种 anchor 尺度的 multi-aspect bucket，并对不同尺度 micro batch 用动态 batch size 提利用率。
  3. **视频-图像联合训练（渐进课程）**：用 T2I 参数初始化，按「低分辨率短视频 → 低分辨率长视频 → 高分辨率长视频」逐步加难度；每阶段按比例混入图像做联合训练，缓解高质量视频数据稀缺、防止图像语义灾难性遗忘。数据按时长×宽高比分桶（BT×BAR 个 bucket），每桶设防 OOM 的最大 batch size，每步随机取桶保持泛化。
- **High-performance fine-tuning**：从全量数据精选 4 个子集，自动过滤 + 人工复审，配合多种优化策略提升高质量动态视频与连续运动/角色动画能力。
- **Prompt Rewrite**：用 **Hunyuan-Large** 做 prompt 改写（训练-free，靠详细指令 + ICL），做多语言适配、结构标准化、复杂术语简化，再用 self-revision 对比原始/改写版精炼；另用收集的高质量改写对 LoRA 微调一个 Hunyuan-Large 加速。
- **加速/蒸馏**：
  - **推理步数缩减**：用 time-step shifting `t'=s·t/(1+(s-1)·t)`，s>1 让模型更关注早期步；步数低时需更大 s（50 步 s=7，<20 步 s=17）。在极低步数（如 10 步）下比 MovieGen 的 linear-quadratic scheduler 效果更好。
  - **文本引导蒸馏（CFG distill）**：把条件+无条件的组合输出蒸馏进单 student 模型（与 teacher 同结构、用 1~8 随机 guidance scale 训练），约带来 **1.9× 加速**。

## Infra（训练 / 推理工程）
**训练**
- 训练框架基于腾讯 Angel 机器学习团队的大规模预训练框架 **AngelPTM**；用腾讯**星脉（XingMai）网络**做高效服务器间通信，GPU 调度走腾讯 Angel ML 平台。
- **5D 并行**：TP（张量并行）+ SP（序列并行，切 LayerNorm/Dropout 重复计算）+ CP（上下文并行，用 Ring Attention 切序列维支持长序列）+ DP + **ZeroCache**（在 DP 基础上削减模型状态冗余，统一 GPU 显存使用）。
- **优化**：FusedAttention 加速注意力（长序列下注意力是主要瓶颈）；重计算（指定层重算、释放/重建前向激活）+ 基于层的**激活 offload**（把激活卸到 host 内存，不损性能进一步省显存）。
- **自动容错**：自动检测硬件故障、快速换健康节点拉起训练，**训练稳定性 99.5%**。
- 注：报告**未披露**具体 GPU 型号、卡数、总 GPU·时与训练吞吐数字。

**推理（来自 GitHub/HF README）**
- 单卡 80GB GPU 即可推理；**显存峰值**：720p×1280×129f 需 **60GB**，544p×960×129f 需 **45GB**。默认 50 步采样。发布支持的分辨率覆盖 540p/720p × {9:16, 16:9, 4:3, 3:4, 1:1}（如 720p 推荐 720×1280×129f）。
- **多卡并行推理**借助 **xDiT**（USP 统一序列并行），支持 ulysses-degree × ring-degree 多种配置（如 8 卡 8×1/4×2/2×4/1×8）。
- 2024-12-18 发布 **FP8 权重**进一步省显存；社区生态有 ComfyUI wrapper、GPU-Poor 版、Sparse-VideoGen、FramePack 等。许可证为自定义的 **tencent-hunyuan-community**（非 Apache/MIT）。

## 评测 benchmark（把效果讲清楚）
**Scaling law（核心定量结论）**
- 自建 **DiT-T2X** 模型族（7 档，92M~6.6B），用 T5-XXL 文本编码器 + 3D VAE、cross-attention 注入、DDPM + v-prediction、256px 训练，按 Hoffmann 方法拟合 `N_opt=a1·C^b1, D_opt=a2·C^b2`（单位：N/D 为 billion，C 为 PetaFLOPs）。
  - **T2X(I)（图像）**：a1=5.48e-4, b1=0.5634, a2=0.324, b2=0.4325。
  - **T2X(V)（视频，用各档最优图像 ckpt 初始化）**：a1=0.0189, b1=0.3618, a2=0.0108, b2=0.6289。
- 结合两套 scaling law、并权衡训练消耗与推理成本，**最终定模型规模 13B**，并据此算出图像/视频训练 token 量。

**主结果——专业人评（Table 3，唯一的主榜评测）**
- 1,533 个 prompt 单次推理（不挑选），60 名专业评测员，按文本对齐 / 运动质量 / 视觉质量三项打分：

| 模型 | 时长 | 文本对齐 | 运动质量 | 视觉质量 | 整体 | 排名 |
|---|---|---|---|---|---|---|
| **HunyuanVideo（本文）** | 5s | 61.8% | **66.5%** | 95.7% | **41.3%** | **1** |
| CNTopA (API) | 5s | 62.6% | 61.7% | 95.6% | 37.7% | 2 |
| CNTopB (Web) | 5s | 60.1% | 62.9% | 97.7% | 37.5% | 3 |
| GEN-3 alpha (Web) | 6s | 47.7% | 54.7% | 97.5% | 27.4% | 4 |
| Luma 1.6 (API) | 5s | 57.6% | 44.2% | 94.1% | 24.8% | 5 |
| CNTopC (Web) | 5s | 48.4% | 47.2% | 96.3% | 24.6% | 6 |

- **整体满意度第一**，运动质量优势最明显（66.5%，显著高于所有对手）。注：评的是 HunyuanVideo 高质量版，与开源的 fast 版不同。

**VAE 重建**（已在「模型架构」列出，图像 33.14 dB / 视频 35.39 dB，均 SOTA）。

**注意**：技术报告**未报告** T2V 模型在 VBench / FID / FVD / CLIPScore 等自动化指标上的数字，主评测为上述人评；GitHub/HF README 也未给 VBench 跑分。

**消融/关键结论**：从零训 3D VAE 优于复用图像 VAE；mix-scale 图像预训练避免 512px 微调劣化 256px；time-step shifting 在 10 步极低步数下优于 linear-quadratic；CFG 蒸馏带来约 1.9× 加速。

## 创新点与影响
**核心贡献**
1. 发布时**最大的开源视频基础模型（13B）**，且把数据/架构/scaling/训练/infra 一整套系统性地公开，真正对标闭源模型并在人评上夺冠。
2. **首次系统建立 T2I→T2V 两段式扩散 scaling law**，把视频生成的算力需求最多降低 5×，给社区提供了「按算力预算定模型/数据规模」的方法论。
3. 从零训练的高压缩比 **Causal 3D VAE**（4×8×8、C=16）重建超过 FLUX-VAE/CogVideoX/Cosmos。
4. 用 **decoder-only MLLM + 双向 refiner** 替代 T5/CLIP 作主文本编码器，改善指令跟随与图文对齐。
5. 「双流→单流」全注意力 DiT + 3D RoPE 的统一图像/视频架构，及 time-step shifting、CFG 蒸馏等推理加速。

**影响**：成为 2024 年底至 2025 年开源视频生态的主力 base，催生大量社区生态（ComfyUI wrapper、GPU-Poor 版、I2V 控制 LoRA、Sparse-VideoGen、FramePack 等）与下游应用（V2A 视频配音、I2V、肖像驱动、Avatar 动画）。其结构化字幕、运镜分类、分层过滤管线、5D 并行 + ZeroCache 等工程实践被后续开源视频模型广泛参考。

**已知局限**：报告未公开训练卡数/GPU·时/吞吐等关键算力数字；未给 VBench 等自动化指标；scaling law 仅覆盖第一阶段（低→高分辨率渐进训练的 scaling 留待未来）；开源的是 fast 版，与人评所用高质量版有差异；许可证为自定义社区协议而非完全宽松开源。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2412.03603
- arxiv_pdf: https://arxiv.org/pdf/2412.03603
- github: https://github.com/Tencent-Hunyuan/HunyuanVideo
- hf_model: https://huggingface.co/tencent/HunyuanVideo
- project_page: https://aivideo.hunyuan.tencent.com

## 一手源存档（sources/）
- [arxiv-2412.03603.pdf](https://arxiv.org/pdf/2412.03603)  （arXiv 原文 PDF，不入 git）
- [arxiv-2412.03603.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/arxiv-2412.03603.txt)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/hunyuan-video--readme.md)
- [hf-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/hunyuan-video--hf-modelcard.md)
