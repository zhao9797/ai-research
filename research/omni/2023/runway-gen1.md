---
title: "Gen-1: Structure and Content-Guided Video Synthesis with Diffusion Models"
org: Runway
country: US
date: "2023-02"
type: paper
category: video
tags: [video-editing, video-to-video, latent-diffusion, depth-conditioning, temporal-layers, structure-content, clip, runway]
url: "https://arxiv.org/abs/2302.03011"
arxiv: "https://arxiv.org/abs/2302.03011"
pdf_url: "https://arxiv.org/pdf/2302.03011"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://research.runwayml.com/gen1"
downloaded: [arxiv-2302.03011.pdf, runway-gen1--project-page.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Gen-1 是 Runway 提出的「结构 + 内容引导」视频到视频（V2V）扩散编辑模型：把输入视频用单目深度（MiDaS）表示其**结构**、用 CLIP 图像嵌入表示其**内容**，在一个扩展了时序层的 latent diffusion U-Net 上推理时完成风格化/重渲染，无需逐视频微调；用户研究中相对 SDEdit/Text2Live/Depth-SD 等基线被偏好约 3/4（最高 91% over IVS、88.24% over Text2Live），是商业视频风格化/编辑工具的奠基论文。

## 背景与定位
解决的问题：视频编辑（风格化、换环境、换主体）耗时且难做到时序一致。当时把图像扩散模型搬到视频上的两条路都有硬伤——(1) 逐视频微调（[[tune-a-video]]、SinFusion）成本高、不能即时处理任意视频；(2) 把图像编辑结果跨帧传播（Text2Live + Layered Neural Atlases）依赖易错的对应关系/神经图层，算一个 atlas 约 10 小时，且编辑常无法准确反映 prompt。

Gen-1 的定位是「**推理时编辑、无需逐视频训练**」：在大规模无字幕视频 + 配对图文数据上训练一个通用模型，对任意输入视频在约 1 分钟内完成编辑。技术脉络上它是 [[latent-diffusion-ldm]] 在时空域的扩展（一作 Patrick Esser 正是 LDM/Stable Diffusion 作者之一），并把 [[video-diffusion-models]]（Ho 2022）、Make-A-Video、Imagen Video 的「给预训练图像模型加时序层 + 图像/视频联合训练」思路用到**编辑**而非从零生成；同时借鉴 [[unclip-dalle2]] 的「CLIP 图像嵌入 + prior 把文本嵌入映射到图像嵌入」做内容条件。它是 Runway 商业 Gen 系列（Gen-2 文生视频、后续 Gen-3/Gen-4）的研究起点。

## 模型架构
**Backbone：扩展了时序层的 latent diffusion U-Net。** 在固定的图像自编码器 latent 空间里做扩散：编码器 E 把 RGB 图像（3×H×W）下采样 8 倍、输出 4 通道 latent（4×H/8×W/8），扩散 U-Net 在这个更小的 latent 上运行以省显存（对视频的时间轴尤为关键）。自编码器在视频上**逐帧独立**处理、训练中保持冻结。

**时序扩展（核心架构）。** 图像 U-Net 由残差块与 transformer 块组成，Gen-1 在每个构件里加一组只对视频输入激活的「时序层」，其余层在图像/视频间共享参数：
- 残差块：每个 2D 空间卷积后加一个 1D 时序卷积；
- transformer 块：每个 2D 空间注意力块后加一个 1D 时序自注意力块（沿时间轴模仿其空间对应物），并向时序 transformer 块输入可学习的「帧索引位置编码」。
- 工程上把 b×n×c×h×w 的张量在空间层 reshape 为 (b·n)×c×h×w，在时序卷积时 reshape 为 (b·h·w)×c×n，在时序自注意力时 reshape 为 (b·h·w)×n×c。把图像视为「单帧视频」，从而统一处理图像与视频。

**条件注入（结构 vs 内容用两种机制）：**
- **结构 s（concatenation）**：结构占据帧的大量空间信息，用「拼接」注入——把（扰动后的）深度图重采样到 RGB 分辨率、用 E 编码成 latent，与噪声输入 z_t 在通道维拼接给 U-Net；同时额外拼接 4 个通道，装结构模糊等级 t_s 的正弦嵌入。
- **内容 c（cross-attention）**：内容与具体位置无关，用交叉注意力注入——U-Net 空间 transformer 块里每个含两个注意力：先空间自注意力，再以 CLIP 图像嵌入算 K/V 的交叉注意力。

**结构表示 = 单目深度（MiDaS DPT-Large）。** 选深度而非边缘图，因为深度比边缘携带更少的内容信息（边缘会带纹理，限制内容编辑自由度），从而更好解耦结构与内容；代价是深度图会泄露物体轮廓，故大幅改变物体形状的编辑受限。

**内容表示 = CLIP 图像嵌入。** 训练时随机取输入视频的一帧、用 CLIP 编码其图像嵌入做内容条件；CLIP 嵌入对语义/风格敏感、对精确几何（大小、位置）更不变，恰与「结构正交」。要支持文本编辑时，再训一个 prior 模型把 CLIP 文本嵌入映射成图像嵌入（沿用 unCLIP/Make-A-Video 思路）。

**参数量/分辨率**：论文未披露 U-Net 参数量（基于预训练文本条件 LDM/Stable Diffusion 初始化）。主训练分辨率 448×256（视频 8 帧、隔 4 帧采一帧）；图像分支用 320×320、384×320、448×256 及其翻转长宽比。

## 数据
- **内部图像集 240M 张** + **自建视频集 6.4M 个视频片段**（均为无字幕视频——论文明确指出当时缺乏与图像数据（如 LAION）同质量的大规模「视频-文本」配对集，故只用无字幕视频）。
- 由于既没有「视频+编辑 prompt+输出」三元组、也没有「视频-字幕」对，训练时**结构与内容都从训练视频自身导出**：s = s(x)（深度）、c = c(x)（随机一帧的 CLIP 嵌入），自监督地学 p(x|s,c)。
- 数据清洗/过滤/美学/安全过滤、配比细节、视频时长分布等**均未披露**。评测/构造编辑 prompt 用到 DAVIS 数据集与各类 stock footage：先用 BLIP captioning 得到原视频内容描述，再用 GPT-3 生成「编辑后」的 prompt。

## 训练方法
**训练目标：latent 扩散去噪。** 标准 DDPM 变分下界重加权损失，预测反向过程的均值；**参数化用 v-parameterization**（早期实验发现 v 预测能改善视频样本的颜色一致性，与 Imagen Video 的发现一致）。条件扩散把 s、c 作为模型额外输入，前向加噪过程不变。

**多阶段训练（关键）：**
1. 用预训练的**文本条件 LDM（Stable Diffusion）权重初始化**；
2. 把条件从「CLIP 文本嵌入」换成「CLIP 图像嵌入」，**仅图像**微调 15k 步；
3. 引入时序连接（§3.2 的时序层），在**图像+视频联合**训练 75k 步；
4. 加结构条件 s（先固定 t_s≡0），训 25k 步；
5. 最后把结构模糊等级 t_s 在 [0,7] 均匀采样，再训 10k 步。
- batch：图像 batch 9216、视频 batch 1152（8 帧、隔 4 帧）；训练中以 12.5% 概率采图像 batch。

**结构保真可调（信息销毁过程）：** 为控制「保留多少结构」，对 MiDaS 深度图做 t_s 次「模糊+下采样」（用模糊算子而非加噪，作者称比加噪更稳定，呼应 Cold Diffusion）；t_s 像扩散时间步一样作为模型输入。训练时随机采 t_s∈[0,T_s]，推理时调 t_s 即可在「严格贴合结构」与「更自由的内容编辑」之间权衡（t_s 越大、内容越不被输入结构决定、prompt 一致性越高）。

**采样 / 引导：** 推理用 DDIM；用 classifier-free guidance（CFG）提样本质量，内容引导尺度 ω（实验多用 7.5）。

**新颖之处——时序一致性可控的自定义引导（temporal guidance ω_t）：** 因为同一套参数同时是图像模型与视频模型，作者把 CFG「在无条件与有条件预测间外推」的思路迁移到时序：设 μ_θ 为视频模型预测、μ^π_θ 为逐帧应用的图像模型预测，按式 (8) 组合——
`μ̃ = μ^π_θ(∅,s) + ω_t·(μ_θ(∅,s) − μ^π_θ(∅,s)) + ω·(μ_θ(c,s) − μ_θ(∅,s))`，
通过 ω_t 在「图像模型（逐帧、更尖锐/手绘感）」与「视频模型（更平滑、时序更稳）」之间外推，从而在推理时直接控温度时序平滑度（ω_t 越大帧间一致性越高）。这是论文首次展示「图像+视频联合训练 → 推理时控时序一致性」。

**定制化（customization）：** 类似 DreamBooth，在 15–30 张图上微调，每个 batch 一半是定制主体、一半是原训练数据以防过拟合；结合较高 t_s 可在驱动视频主体与目标主体差异较大时仍获得准确动画。

## Infra（训练 / 推理工程）
- **算力规模 / GPU·时 / 并行策略 / 混合精度 / 吞吐：均未披露**（论文只给了 batch size 与训练步数，未给硬件与机时）。
- **推理速度**：编辑任意视频约 **1 分钟**（论文 §4.1 对比 Text2Live 算神经 atlas 需约 10 小时，凸显其推理时编辑、免逐视频训练的工程优势）；自编码器逐帧处理、latent 下采样 8× 降低显存。采样用 DDIM（少步数）。
- **部署形态**：作为 Runway 商业产品上线（项目页「Try Gen-1 in Runway」），具体服务化/量化/蒸馏细节未公开。

## 评测 benchmark（把效果讲清楚）
评测核心是**「帧一致性 vs prompt 一致性」**两维 trade-off + AMT 用户研究（35 个代表性编辑 prompt，每例 5 名标注者多数投票）。两指标均基于 CLIP：
- **Frame consistency** = 输出视频相邻帧 CLIP 图像嵌入的平均余弦相似度；
- **Prompt consistency** = 输出各帧 CLIP 图像嵌入与编辑 prompt 的 CLIP 文本嵌入平均余弦相似度。

Gen-1 在二维图上位于右上象限（两者兼优），并在用户研究中「平均约 3/4 被偏好」。表 S1 关键数字（±为 n=35 的标准误）：

| 方法 | frame consistency | prompt consistency | ours preferred（Gen-1 胜率） |
|---|---|---|---|
| Deforum | 0.9087 ±0.0079 | 0.2693 ±0.0075 | 77.14% |
| SDEdit, strength=50% | 0.9277 | 0.2454 | 85.29% |
| SDEdit, strength=75% | 0.9189 | 0.2754 | 73.53% |
| IVS, strength=50% | 0.9673 | 0.2401 | 79.41% |
| IVS, strength=75% | 0.9668 | 0.2556 | **91.18%** |
| Depth-SD | 0.9126 | 0.2871 | 74.29% |
| Text2Live | 0.9683 | 0.2732 | 88.24% |
| ours, ∼s（去结构条件消融）, strength=50% | 0.9541 | 0.2703 | 67.65% |
| ours, ∼s, strength=75% | 0.9482 | 0.2769 | 64.71% |

> 项目页对外宣传口径取了其中两项：**73.53% 偏好优于 Stable Diffusion 1.5**、**88.24% 偏好优于 Text2Live**。其中 73.53% 在表 S1 里对应的正是「SDEdit, strength=75%」一行（即把 SD 逐帧 SDEdit 当作 "Stable Diffusion 1.5" 基线）；表里另有一条 Depth-SD 路线胜率为 74.29%，与宣传口径的 73.53% 不是同一项。

**关键消融（ω_t、t_s 对两指标的影响，Gen-1 自身配置）：**
- 固定 t_s=0、ω=7.5，调时序尺度 ω_t：0.50→0.9238、0.75→0.9521、1.00→0.9648、1.25→0.9702、1.50→0.9722——**ω_t 越大帧一致性单调上升**（对应 prompt 一致性 0.2820→0.2822→0.2805→0.2793→0.2754，除 0.75 处略有抬升外整体随 ω_t 增大而下降，确证 trade-off）。论文图 4 同时显示：ω_t 增大时，相邻帧 CLIP 相似度单调升、用光流 warp 后的帧间 MSE 单调降；低 ω_t（0.5）偏「手绘感」、高 ω_t（1.5）更平滑。
- 固定 ω_t=1.0、ω=7.5，调结构尺度 t_s：t_s=0→prompt 0.2805 / frame 0.9648；t_s=4→0.2866 / 0.9678；t_s=6→0.2854 / 0.9717；t_s=7→0.2766 / 0.9790——**t_s 增大帧一致性继续升、prompt 一致性先升后降**。
- **去结构条件消融（ours, ∼s = 在不带结构条件的视频模型上跑 SDEdit）**：胜率掉到 64.71–67.65%，明显低于带结构条件的完整模型对各基线 73–91% 的胜率，说明**显式结构（深度）条件是 Gen-1 偏好度的主要来源**。

> 注：论文未报告 FID / FVD / VBench / GenEval 等生成式定量指标——Gen-1 是**编辑**而非从零生成模型，评测以帧/prompt 一致性 + 人评为主。

## 创新点与影响
**核心贡献：**
1. 把 latent diffusion 扩展到时空域，用「图像 U-Net 加时序卷积/时序自注意力 + 图像/视频联合训练」做**视频编辑**（而非从零生成），实现推理时编辑、免逐视频训练（约 1 分钟 vs 神经 atlas 约 10 小时）。
2. **结构=深度 / 内容=CLIP 图像嵌入**的解耦表示 + 两种条件注入（结构 concat、内容 cross-attn），并用「深度图模糊 t_s」在推理时控结构保真度。
3. 提出**时序一致性可控的自定义引导 ω_t**，首次证明图像/视频联合训练可在推理时调时序平滑度。
4. 支持文本/图像两种内容指定（CLIP prior 把文本嵌入→图像嵌入）、masked 局部编辑、以及 DreamBooth 式少样本定制。

**影响：** Gen-1 是 Runway 商业 Gen 系列的研究奠基，把「可控视频风格化/重渲染」推进为可用产品；其「给预训练图像扩散模型加时序层 + 图像视频联合训练 + 深度/CLIP 解耦条件」的范式，启发了后续 video-to-video / 可控视频生成与编辑的一大类工作。一作 Patrick Esser 之后主导 Stable Video Diffusion 与 SD3。

**已知局限：** 深度图泄露物体轮廓 → 难做大幅改变物体形状的编辑；只用无字幕视频自监督（缺高质量视频-文本配对）；评测仅 35 prompt 的 CLIP 指标 + AMT 主观投票，无 FVD/VBench 等标准生成式定量；算力/机时/参数量等工程细节未公开；作者自述不希望被用于有害用途、承认滥用风险。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2302.03011
- arxiv_pdf: https://arxiv.org/pdf/2302.03011
- project_page: https://research.runwayml.com/gen1 （重定向至 https://runwayml.com/research/gen-1）

## 一手源存档（sources/）
- [arxiv-2302.03011.pdf](https://arxiv.org/pdf/2302.03011)  （arXiv 原文 PDF，不入 git）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/runway-gen1--project-page.md)
