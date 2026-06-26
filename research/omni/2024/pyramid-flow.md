---
title: "Pyramid Flow:金字塔式流匹配的高效视频生成"
org: "PKU / Kuaishou / BUPT"
country: China
date: "2024-10"
type: paper
category: video
tags: [video-generation, flow-matching, pyramidal-flow, autoregressive, dit, mm-dit, efficient-training]
url: "https://arxiv.org/abs/2410.05954"
arxiv: "https://arxiv.org/abs/2410.05954"
pdf_url: "https://arxiv.org/pdf/2410.05954"
github_url: "https://github.com/jy0205/Pyramid-Flow"
hf_url: "https://huggingface.co/rain1011/pyramid-flow-miniflux"
modelscope_url: ""
project_url: "https://pyramid-flow.github.io"
downloaded: [arxiv-2410.05954.pdf, pyramid-flow--readme.md, pyramid-flow--hf-miniflux-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Pyramid Flow（金字塔式流匹配，ICLR 2025）用**单个统一 DiT**把视频去噪轨迹重新诠释为一串"金字塔阶段"——只有最后一个阶段在全分辨率运行，早期高噪声步骤在压缩低分辨率上算，配合**时间金字塔**压缩自回归历史条件；最终只用 **20.7k A100 GPU 小时、纯开源数据**就训出 768p/24fps、最长 10 秒的视频生成模型，VBench 总分 81.72 / 质量分 84.74（质量分超过 Gen-3 Alpha 的 84.11、并优于 2 倍体量的 CogVideoX-5B）。

## 背景与定位
视频生成需要建模庞大的时空空间，计算与数据开销巨大。主流降本路线是**级联架构**（cascaded）：先在高压缩潜空间生成低分辨率，再用额外的超分模型逐级上采样（如 [[cascaded-diffusion]]、Würstchen、Relay Diffusion）。级联虽避免了全分辨率直训，但**每个分辨率要单独训一个模型**，牺牲灵活性与可扩展性，且子模型分开优化**阻碍知识共享**。

作者的核心观察（论文 Fig.1a）：扩散/流模型**早期时间步非常嘈杂且信息量低**，全程都在全分辨率上算是浪费。于是把生成轨迹重新解释为一系列在不同尺度压缩表示上运行的金字塔阶段——只有最后一阶段全分辨率，早期阶段低分辨率，大幅削减冗余计算。相比级联模型有两点本质改进：(1) 各阶段轨迹**互相衔接**，后一阶段从前一阶段的结果继续生成，而非每阶段都从纯噪声重生；(2) 用**单一统一模型**端到端联合优化所有金字塔阶段，而非每个分辨率一个模型。

技术脉络上它站在 [[flow-matching]]（Lipman / Liu rectified flow）、[[dit-scalable-diffusion-transformers]]、[[stable-diffusion-3]]（MM-DiT）、[[flux-1]] 与自回归长视频（Diffusion Forcing、GameNGen）的交叉点上，把"图像金字塔"思想（FPN、image pyramid）首次以纯流匹配目标统一进单 DiT。机构为北京大学 + 快手 + 北邮，第一作者 Yang Jin，通讯 Yadong Mu / Zhouchen Lin。

## 模型架构
- **Backbone**：MM-DiT，基于 **SD3 Medium**，24 层 Transformer，总参数 **2B**；权重由 SD3 Medium 初始化（后续 miniFLUX 版本改为 FLUX 结构从头训，见下）。空间维用正弦位置编码，时间维加 **1D RoPE** 以支持不同时长的弹性训练。
- **Text encoder**：沿用 FLUX.1 的做法，**T5 + CLIP** 双编码器做 prompt embedding。
- **3D VAE（自研，从头训）**：结构类 **MAGVIT-v2**，3D 因果卷积（每帧只依赖前序帧），非对称 encoder-decoder + KL 正则，时空压缩率 **8×8×8**（像素→潜空间）。在 WebVid-10M + 6.9M SAM 图像上从头训练。
- **注意力设计**：得益于金字塔表示带来的 token 锐减，**直接用全序列注意力**（而非 Latte 那种时空分解注意力）；同时在每层 Transformer 用**分块因果注意力（blockwise causal attention）**——token 不能 attend 到后续帧，这是自回归视频生成的关键（消融见下）。
- **位置编码的金字塔适配**（Fig.3b）：在**空间金字塔上外推（extrapolate）**位置编码以保留细粒度细节，在**时间金字塔输入上插值（interpolate）**位置编码以让历史条件在空间上对齐。
- **金字塔阶段数 K=3**（所有实验固定）。第一帧天然充当图像条件，因此模型虽只为 t2v 训练，推理时**天然支持文本+图像→视频（i2v）**，无需额外微调。
- **分辨率/时长策略**：384p 版生成 5 秒（temp≤16），768p 版最长 10 秒，均 24fps；miniFLUX 版另支持 1024p 图像。

**金字塔式流匹配（核心方法）**：标准流匹配学一个速度场 v_t 把噪声 x0 沿 ODE 映到数据 x1，线性插值路径 x_t=t·x1+(1−t)·x0。本文把它推广为**在不同分辨率之间插值**：把 [0,1] 切成 K 个时间窗，第 k 窗在相邻两级分辨率间做分段流（piecewise flow），起点是"上采样自更低分辨率、更噪、像素化的潜变量"，终点是"该级分辨率、更干净、去像素化的潜变量"（论文 Eq.5–11）。这样**只有最后一阶段在全分辨率运行**，均匀划分下空间金字塔把计算降到约 1/K。所有阶段用**同一个统一流匹配目标**在单 DiT 上联合优化，实现"生成"与"解压/超分"的统一。为增强轨迹直线性，对端点的噪声做**耦合采样**（同一方向噪声 n）。

**跳点 renoising（保证概率路径连续）**：跨阶段分辨率切换处（jump points）需保持概率路径连续。把上一阶段低分辨率端点上采样后，其分布与当前阶段起点分布只差一个线性变换；论文推导出在最近邻上采样下，加一个带负相关结构（γ=−1/3，块内去相关）的**校正高斯噪声**即可匹配两者的均值与协方差，得到更新式（Eq.15）：x̂_{s_k}=(1+s_k)/2·Up(x̂_{e_{k+1}})+√(3(1−s_k))/2·n′，其中 e_{k+1}=2s_k/(1+s_k)。消融显示去掉校正噪声会产生块状伪影、模糊。

**时间金字塔（自回归历史压缩）**：视频自回归生成把全分辨率历史作为条件，开销巨大；但早期帧多提供高层语义、与外观细节关联弱，存在高冗余。于是用**逐渐升分辨率的历史条件**：越早的历史帧压得越狠（Eq.16，如 i−2 帧用 2^{k+1} 下采样、i−1 帧用 2^k），训练时给历史潜变量加少量噪声（强度均匀采自 [0,1/3]）以缓解自回归误差累积；推理用干净生成帧做条件。T 个历史潜变量分布在 K 级分辨率上，多数帧在最低 1/2^K 分辨率上算，训练 token 数最多降 1/4^K，训练效率最高提升 16^K/T 倍。

## 数据
**纯开源数据**训练（这是核心卖点之一）。
- **图像**：LAION-5B 高美学子集（论文正文称该子集，附录训练流程具体用 180M LAION-5B 图像）、CC-12M 的 11M、SA-1B 非模糊子集 6.9M、JourneyDB 4.4M、以及 14M 公开合成数据。
- **视频**：WebVid-10M、OpenVid-1M、另有 1M 高分辨率无水印视频（主要来自 Open-Sora Plan）。后处理后约 **10M 单镜头视频**可用于训练。
- **Re-captioning**：用 **Video-LLaMA2**（SOTA 视频理解模型）对每条视频重新打标。论文坦承所用为"粗粒度合成 caption"，这导致语义分（color、appearance style、human action 等细粒度跟随）相对偏低——可在后续阶段用更优 caption 的图像数据单独修补（因自回归框架把视频拆成"首帧生成 + 后续帧生成"，图像质量问题可独立处理）。
- **3D VAE 训练数据**：WebVid-10M + 6.9M SAM 图像，从头训。

## 训练方法
**目标**：统一的金字塔式**流匹配（flow matching / rectified flow）**目标，regress 速度场 v_t 到分段条件向量场 u_t=x̂_{e_k}−x̂_{s_k}（Eq.11），一个目标同时学会生成与解压/超分。

**三阶段训练流程**（共 128×A100，总约 20.7k A100·h）：
1. **图像训练**：纯图像数据（180M LAION-5B + 11M CC-12M + 6.9M SA-1B + 4.4M JourneyDB），保留原始宽高比按 bucket 排布，训 50k 步，约 **1,536 A100·h**（12h），让模型先学会视觉像素依赖以加速后续视频收敛。
2. **低分辨率视频训练**：WebVid-10M + OpenVid-1M + 1M Open-Sora Plan 无水印视频，Video-LLaMA2 重打标；每 batch 混入 **12.5% 图像数据**。先训 80k 步 2 秒视频，再训 120k 步 5 秒视频，共约 **11,520 A100·h**（90h）。
3. **高分辨率视频训练**：同策略在高分辨率、时长 5–10s 的视频上继续微调 50k 步，约 **7,680 A100·h**（60h）。

**关键超参（Table 4）**：优化器 AdamW（阶段1 β=(0.9,0.999)；阶段2/3 β=(0.9,0.95)，ε=1e-6）；global batch 阶段1=1536、阶段2=768、阶段3=384；学习率阶段1/2=1e-4、阶段3=5e-5，constant with warmup（1k warmup 步）；weight decay 1e-4；梯度裁剪 1.0；bf16。

**训练 trick**：
- 各金字塔阶段**每次迭代均匀采样**联合训练。
- 自回归框架天然支持图文联合训练（视频首帧=图像）。
- 用 **Patch n' Pack（NaViT）** 思想把不同 token 数样本打包成长度均衡 batch。
- 历史条件加 [0,1/3] 噪声缓解自回归退化（关键）。
- 推理用 CFG 增强时间一致性与运动平滑。
- 未使用蒸馏/一致性模型/步数蒸馏（论文未涉及 LCM/ADD 类加速）。

## Infra（训练 / 推理工程）
- **训练算力**：128×NVIDIA A100，全流程合计 **约 20.7k A100 GPU·h**（1.5k 图像 + 11.5k 低分辨率视频 + 7.7k 高分辨率视频）。对比 Open-Sora 1.2 需 4.8k Ascend + 37.8k H100·h 才训出 97 帧生成、且质量更差——本文计算量不到其一半。
- **效率分析**：全序列扩散有 TN 个 token、T²N² 计算；本文即便末阶段也只用约 TN/4^K token、T²N²/16^K 计算。10 秒 241 帧视频，训练 token 从全序列的 119,040 降到 ≤15,360。
- **长视频分布式**：把很长视频 scatter 到多 GPU 分摊计算（类 CogVideoX 做法）。
- **推理速度**：单 A100 生成 5 秒 384p 约 **56 秒**；5 秒 768p/24fps 单 A100 约 5.5 分钟，4×A100 序列并行降到 **2.5 分钟**。
- **显存友好部署**（README 工程贡献，多为社区 PR）：`cpu_offloading=True` 可在 **<12GB** 显存推理；`enable_sequential_cpu_offload()` 可在 **<8GB** 显存推理；多 GPU 序列并行省显存并加速。
- **代码栈**：Python 3.8.10 / PyTorch 2.1.2；开源训练 VAE + 微调 DiT（含自回归与非自回归两版，后者无时间金字塔、更稳但效率低）。训 VAE / 微调 DiT 均建议 ≥8×A100。

## 评测 benchmark（把效果讲清楚）
评测用 **VBench**（16 维度）与 **EvalCrafter**（~17 项指标），t2v 每 prompt 生成 5 秒 121 帧；另做 20+ 人、1411 条有效偏好的人评。

**VBench（Table 1，蓝色=公开数据训练中最高）**：
| 模型 | 公开数据 | 总分 | 质量分 | 语义分 | 运动平滑 | 动态度 |
|---|---|---|---|---|---|---|
| Kling | × | 81.85 | 83.38 | 75.68 | 99.40 | 46.94 |
| Gen-3 Alpha | × | 82.32 | 84.11 | 75.17 | 99.23 | 60.14 |
| CogVideoX-5B | × | 81.61 | 82.75 | 77.04 | 96.92 | 70.97 |
| Open-Sora 1.2 | ✓ | 79.76 | 81.35 | 73.39 | 98.50 | 42.39 |
| T2V-Turbo | ✓ | 81.01 | 82.57 | 74.76 | 97.34 | 49.17 |
| **Pyramid Flow** | ✓ | **81.72** | **84.74** | 69.62 | 99.12 | **64.63** |

要点：总分 81.72 居公开数据训练第一；**质量分 84.74 全表最高**（超 Gen-3 Alpha 84.11），且超过 2 倍体量的 CogVideoX-5B（82.75）；动态度 64.63 公开数据训练第一、全表第二（仅次 CogVideoX-5B 的 70.97），运动平滑 99.12。**短板**：语义分 69.62 偏低（粗粒度合成 caption 所致）；细粒度 VBench 子项里 color、appearance style、human action 相对弱（human action 受 SD3-Medium 初始化"人体结构"老问题拖累）。

**EvalCrafter（Table 2，Final Sum）**：Pyramid Flow 244 分，公开数据训练中最高（VideoCrafter2 243、LaVie 234、Show-1 229、ModelScope 218），且视觉质量 67.94、运动质量 55.31、时间一致性 63.41 多数项领先公开/闭源模型；raw 指标中 Motion AC-Score 全表第二、BLIP-BLUE / CLIPScore 语义对齐进前二（含闭源 Gen-2）。**唯一明显短板**：face consistency 偏低，源于时间金字塔压缩历史条件。

**人评（Fig.4，胜率，6 个 baseline）**：vs Open-Sora Plan v1.1 美学 96.4%/运动 92.8%/语义 81.3%（基本碾压）；vs Open-Sora 1.2 美学 76.7%/运动 83.1%/语义 59.2%；vs Pika 1.0 美学 67.6%/运动 49.2%/语义 63.5%；vs CogVideoX-2B 美学 57.0%/运动 56.6%/语义 42.1%；vs CogVideoX-5B 美学 52.3%/运动 55.4%/语义 38.6%；vs Kling 美学 63.6%/运动 32.5%（弱于 Kling）/语义 63.4%。整体在开源模型中优势明显，运动平滑尤其突出（得益于 token 节省后能跑 24fps，而基线常只能 8fps）。

**消融**：
- **空间金字塔 vs 标准流匹配**（同数据/同 batch token 数/同超参/同架构 t2i）：MS-COCO 3K prompt 上 FID 收敛**快近 3 倍**（Fig.7）。
- **时间金字塔 vs 全序列扩散**（同实验设定）：100k 低分辨率视频步时本文视觉质量与时间一致性显著更好，全序列基线远未收敛、运动碎裂（Fig.8）；MSR-VTT 上 FVD 收敛更快（Fig.12b）。
- **校正 renoising**：去掉则全局结构对但细节模糊、块状伪影（Fig.10）。
- **分块因果注意力 vs 双向注意力**：双向注意力的视频主体形状/颜色不断漂移、缺时间连贯；因果注意力的历史条件固定、稳定自回归（Fig.11）。

## 创新点与影响
**核心贡献**：
1. **金字塔式流匹配**——首次用一个纯流匹配目标，把"低分辨率生成 + 逐级超分/解压"统一进**单个 DiT 端到端训练**，替代多模型级联，实现知识共享、训练大幅加速且实现优雅。
2. **跳点校正 renoising**——给出闭式的校正噪声推导（γ=−1/3），保证跨分辨率阶段的概率路径连续，无伪影。
3. **时间金字塔**——用逐级压缩的低分辨率历史做自回归条件，把长视频训练 token / 显存开销降一个量级，支持弹性时长生成。
4. **极致性价比 + 全开源**：20.7k A100·h、纯开源数据训出可比肩 Kling / Gen-3 Alpha 的 768p/24fps/10s 视频；代码、VAE 训练、DiT 微调、两版（自回归/非自回归）checkpoint 全开放。

**演进（README News）**：
- 2024.10.10 发布技术报告 + SD3 版 checkpoint；10.11 HF demo；10.13 多 GPU 推理 + CPU offload。
- 2024.10.29 放出训练代码（VAE + DiT 微调）与 **FLUX 结构从头训**的新 checkpoint。
- **2024.11.13 发布 miniFLUX 版**：把 backbone 从 SD3 换成 mini-FLUX 并从头训，**专门修复人体结构问题**，并在人体结构与运动稳定性上明显改善；支持 1024p 图像 + 384p（5s）/ 768p（10s）视频。这是对论文中"human action 受 SD3 初始化拖累"短板的直接工程修正。

**已知局限**：语义/细粒度跟随受限于粗粒度视频 caption；face consistency 因历史压缩偏弱；SD3-Medium 版人体结构问题（miniFLUX 已缓解）；未做步数蒸馏，推理仍需多步采样；K=3 固定、未探更深金字塔。其"早期步用低分辨率算"的洞见、统一流匹配目标与时间金字塔，对后续高效视频生成（尤其自回归 + flow 结合、跨分辨率联合训练）有清晰借鉴价值。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2410.05954
- arxiv_pdf: https://arxiv.org/pdf/2410.05954
- github: https://github.com/jy0205/Pyramid-Flow
- project_page: https://pyramid-flow.github.io
- hf_miniflux: https://huggingface.co/rain1011/pyramid-flow-miniflux
- hf_sd3: https://huggingface.co/rain1011/pyramid-flow-sd3
- hf_demo: https://huggingface.co/spaces/Pyramid-Flow/pyramid-flow

## 一手源存档（sources/）
- [arxiv-2410.05954.pdf](https://arxiv.org/pdf/2410.05954)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/pyramid-flow--readme.md)
- [hf-miniflux-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/pyramid-flow--hf-miniflux-card.md)
