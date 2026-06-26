---
title: "Uni-ControlNet: All-in-One Control to Text-to-Image Diffusion Models"
org: "HKU / Microsoft"
country: China
date: "2023-05"
type: paper
category: edit
tags: [controllable-generation, adapter, diffusion, stable-diffusion, multi-condition, composable, spade, clip, neurips2023]
url: "https://arxiv.org/abs/2305.16322"
arxiv: "https://arxiv.org/abs/2305.16322"
pdf_url: "https://arxiv.org/pdf/2305.16322"
github_url: "https://github.com/ShihaoZhaoZSH/Uni-ControlNet"
hf_url: "https://huggingface.co/shihaozhao/uni-controlnet"
modelscope_url: ""
project_url: "https://shihaozhaozsh.github.io/unicontrolnet/"
downloaded: [arxiv-2305.16322.pdf, uni-controlnet--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Uni-ControlNet 在冻结的预训练 T2I 扩散模型（Stable Diffusion）上只额外微调 **两个 adapter**，就把 7 种局部空间条件（Canny/MLSD/HED/sketch/Openpose/depth/segmentation）和 1 种全局条件（CLIP 图像 embedding）统一进一个模型，可任意组合且无需联合训练；只用 1000 万 LAION 图文对训练 1 个 epoch，在 COCO 上 FID/可控性/CLIPScore 全面优于逐条件各训一个 adapter 的 [[controlnet]]/[[gligen]]/[[t2i-adapter]]，且 adapter 数量恒为 2（其它方法随条件数 N 线性增长）。NeurIPS 2023。

## 背景与定位
T2I 扩散模型（[[latent-diffusion-ldm]]、Stable Diffusion）虽强，但纯文本难以精确表达细粒度空间布局（多物体位置、边缘、深度、姿态）。给冻结 SD 加可控性有两条路线：

- **从头训练**：Composer（Huang et al. 2023）在十亿级数据上训练一个大扩散模型，可控性强但 GPU 成本巨大，研究者难以复现。
- **微调轻量 adapter**：[[controlnet]]、[[gligen]]、[[t2i-adapter]] 在冻结 SD 上挂轻量模块。问题是它们 **每个条件一个独立 adapter**——条件数 N 增加时微调成本与模型体积线性增长，且不同 adapter 彼此隔离，**可组合性（composability）差**。论文实测 Multi-ControlNet 与 CoAdapter（联合训练的 T2I-Adapter）在双条件融合时仍表现不佳。GLIGEN 干脆不支持多条件组合。

Uni-ControlNet 走第二条路线但解决上述痛点：把所有条件归为 **局部条件（local，有空间结构）** 与 **全局条件（global，无空间结构，类似文本的整体语义控制）** 两大类，对应只加两个共享 adapter，无论条件多少。论文用 Table 1 总结：唯有 Uni-ControlNet 同时满足"微调"+"可组合"+"微调成本=2"+"adapter 数=2"。技术上它直接 build upon [[controlnet]]（局部 adapter 复制 SD encoder 的思路来自 ControlNet），全局 adapter 把 CLIP 图像 embedding 当作扩展文本 token，与稍晚（2023-08）的 [[ip-adapter]] 思路相邻（都把参考图 CLIP embedding 注入 cross-attention，但注入方式不同：Uni 把图像 token 直接 concat 进扩展 prompt 喂所有 cross-attn，IP-Adapter 用解耦的独立 cross-attn 分支）。

## 模型架构
基座是 **Stable Diffusion** 的 U-Net 去噪网络（encoder F + middle block M + decoder G，encoder/decoder 各 12 个 block，带 skip-connection）。README 明确**发布的预训练权重基于 Stable Diffusion v1.5**。SD 主体全程**冻结**，只训练两个 adapter。

**局部控制 adapter（Local Control Adapter）** —— 灵感来自 [[controlnet]] 但有关键改动：
- 复制 SD 的 encoder 和 middle block 权重得到 `F'`、`M'`，把它们的输出在 decoder 解码阶段注入主干（通过 zero convolution，权重从 0 渐增以稳定训练）。decoder 第 i 块输入改为 `concat(m+m', f_j + zero(f'_j))`（i=1）或 `concat(g_{i-1}, f_j + zero(f'_j))`（2≤i≤12）。
- **多尺度条件注入（multi-scale injection）**：先把 7 个局部条件沿通道维 concat，送入一个堆叠卷积的特征提取器 H，在 4 个分辨率（64×64、32×32、16×16、8×8）各取条件特征。
- **FDN（Feature Denormalization）注入模块**：借鉴 SPADE 的空间自适应归一化思想——用条件特征去调制归一化后的噪声特征：`FDN_r(Z_r, c_l) = norm(Z_r)·(1 + conv_γ(zero(h_r(c_l)))) + conv_β(zero(h_r(c_l)))`，即条件特征生成空间敏感的 scale γ 和 shift β。这与 ControlNet 仅在输入层把条件加到噪声上、或 T2I-Adapter 仅在输入注入不同——Uni-ControlNet 在**每个分辨率层级都注入**，缓解深层信息丢失。
- 局部 adapter 内部结构（附录 Fig.19/20）：特征提取器为多层 Conv+SiLU；Copied Encoder 每个分辨率的 ResBlock 内嵌 FDN，并经 zero conv 接回主干。

**全局控制 adapter（Global Control Adapter）**：
- 把全局条件（参考图的 CLIP image embedding）经一个**条件编码器 h_g**（堆叠 feedforward 层，结构见附录 Fig.21：LayerNorm + GEGLU Feedforward ×2）投影，reshape 成 **K 个全局 token（默认 K=4）**，与原始 K0 个文本 token concat 成"扩展 prompt" `y_ext = [y^t_1..y^t_{K0}, λ·y^g_1..λ·y^g_K]`。
- 该扩展 prompt 同时喂给 **主干 SD 和控制 adapter 的所有 cross-attention 层**（`K=W_k(y_ext)`, `V=W_v(y_ext)`）。λ 是全局条件权重超参。
- 设计理念：文本本身就是一种无空间结构的"全局控制"，所以把图像参考也变成 token 与文本对齐，是最自然的注入方式。

**参数/分辨率**：训练与推理分辨率 512×512；论文未给出 adapter 的精确参数量数字（**未报告**），但反复强调"adapter 数恒为 2、模型体积不随条件数增长"是核心卖点。

## 数据
- 训练数据：从 **LAION** 随机采样 **1000 万（10M）图文对**，训练 **1 个 epoch**。
- 条件标注是**自动从自然图像抽取**的（用各自检测器/标注器作为 ControlNet 风格的伪标签）：Canny、MLSD、HED、sketch、Openpose、Midas depth、UPerNet 分割。
- **sketch 的特殊处理**：直接标注手绘 sketch 困难，故先取图像的 HED boundary，再用 sketch simplification 方法生成训练用 sketch。
- **pose 的特殊处理**：因为数据集中并非所有图都含人，训练时**不对 pose 条件做 dropout**，以保证 pose 充分训练。
- 全局条件由 CLIP image encoder 直接抽 image embedding，无需额外标注。
- 美学/安全过滤、配比等细节**未披露**（直接用 LAION 子集）。
- 消融实验用 10M 的 **1M 子集**训练 1 epoch；条件扩展实验（R1–R4）用 **300k** 样本重训练。

## 训练方法
- 训练目标：标准 **DDPM 扩散去噪损失**（[[ddpm]]）——预测加到样本上的高斯噪声；继承自冻结的 SD，未改动损失形式（未用 flow matching / 蒸馏）。
- 优化器 **AdamW**，学习率 **1×10⁻⁵**，分辨率 512×512。
- **分开训练（separate fine-tuning）是关键 trick**：局部 adapter 与全局 adapter **各自单独**微调，推理时直接合并即可组合两类条件，**无需任何联合微调**。论文发现联合训练（Train-S1）会让全局条件学得不充分（局部条件信息更丰富，模型会"偏心"局部），可控性变差；先分训再联合微调（Train-S2）相比默认分训**几乎没有额外增益**，所以默认就分训。
- **条件 dropout 训练**：训练每个 adapter 时，以预定义概率随机 drop 每个条件，再加一个额外概率"全保留或全丢弃"；被丢的条件对应输入通道置 0。这让模型学会基于任意单条件或多条件子集生成（即同时支持 1 个或多个条件）。
- 超参 λ：训练时固定为 1；**推理时**——无文本 prompt 时 λ=1，有文本 prompt 时调到约 **0.75**（在文本与全局条件间权衡，λ 越大全局条件越主导，见附录 Fig.9）。
- 采样：推理用 **[[ddim]]** 50 步，[[classifier-free-guidance]] scale **7.5**。
- **条件扩展能力**：已训好的模型要加新条件（如从 6 种扩展到 +Canny），论文消融 R1–R4 发现——**只重训特征提取器 H 的第一层卷积**（R3，用 300k 数据）就足以纳入新条件，不必重训整个提取器，进一步降低扩展成本。

## Infra（训练 / 推理工程）
- 训练规模：10M 图文对 ×1 epoch，论文据此强调"轻量、可负担"，与 Composer 的十亿级从头训练对比。
- **具体 GPU 型号、卡数、GPU·小时、并行/混合精度、吞吐量均未披露**。
- 推理：DDIM 50 步、CFG 7.5；**未报告单图推理耗时/显存/量化/缓存等工程数字**。
- 部署形态：开源代码提供 Gradio demo（`src/test/test.py`），自动检测条件并交互生成；权重需放 `./ckpt/`，基座 SD v1.5。训练需先用 `prepare_weights.py` 从 SD 权重初始化局部/全局 adapter，分别训练后再 `integrate` 合并成 Uni-ControlNet。

## 评测 benchmark（把效果讲清楚）
评测集：**COCO2017 验证集**（5k 图，512×512，每图随机取一个 caption），仅测单条件。基线：ControlNet（Multi-ControlNet）、GLIGEN、T2I-Adapter（CoAdapter）。Composer 因未开源且从头训练，未纳入对比。

**生成质量 FID（越低越好，Table 2）**——Uni-ControlNet 在多数条件上最优：

| 方法 | Canny | MLSD | HED | Sketch | Pose | Depth | Seg | Style\Content |
|---|---|---|---|---|---|---|---|---|
| ControlNet | 18.90 | 31.36 | 26.59 | 22.19 | 27.84 | 21.25 | 23.08 | 31.17 |
| GLIGEN | 24.74 | – | 28.57 | – | 24.57 | 21.46 | 27.39 | 25.12 |
| T2I-Adapter | 18.98 | – | – | 18.83 | 29.57 | 21.35 | 23.84 | 28.86 |
| **Uni-ControlNet** | **17.79** | **26.18** | **17.86** | 20.11 | **26.61** | **21.20** | **23.40** | **23.98** |

**可控性（Table 3）**——按条件类型用不同指标，论文称 Uni-ControlNet 在 8 项中赢 4 项（ControlNet 赢 3，T2I-Adapter 赢 1）。Uni 拿下的 4 项是 Canny/HED/Sketch 的 SSIM 与 Content 的 CLIP Score：
- Canny/HED/MLSD/Sketch 用 **SSIM**（越高越好）：Uni 的 Canny 0.4911（最优，ControlNet 0.4828）、HED 0.5197（最优，ControlNet 0.4719）、Sketch 0.5923（最优，T2I-Adapter 0.5148）；MLSD 0.6773 < ControlNet 0.7455（ControlNet 更优）。
- Pose 用 **mAP(OKS)**：Uni 0.2164，T2I-Adapter 0.5283 更高（Uni 弱项）。
- Depth 用 **MSE**（常规越低越好）：Uni 91.05，是三家里最高的（ControlNet 87.57 / GLIGEN 88.22 / T2I 89.82）；论文 Table 3 把 Uni 的 91.05 加粗为"best"与 MSE 越低越好的常识及"4/8"口径冲突，按越低越好读则该项归 ControlNet（**原文存在排版/口径不一致，此处按越低越好计**）。
- Seg 用 **mIoU**（越高越好）：Uni 0.3160 < ControlNet 0.4431（ControlNet 更优）。
- Content 用 **CLIP Score**（越高越好）：Uni 0.7753（最优）。
- 即 ControlNet 赢 MLSD-SSIM / Depth-MSE / Seg-mIoU 共 3 项，T2I-Adapter 赢 Pose 1 项。
- 关键背景：ControlNet/GLIGEN/T2I-Adapter **每条件各训一个专用模型**，而 Uni-ControlNet **单模型** 就达到整体更优。

**CLIP Score（Table 7，越高越好）**——Uni-ControlNet 多数条件领先（如 Canny 0.2539、MLSD 0.2485、Sketch 0.2542、Content 0.2402 等），与质量/可控性结论一致。

**与 SD2.1 原生条件版对比（Table 5/6）**：SD2-depth、SD2-unclip 是**整模型微调**（非冻结 adapter），各自只支持一种条件。
- **Depth**：仅 **depth-FID** SD2-depth 更优（17.76 < Uni 21.20）；**depth-CLIP** 反而 Uni 0.2561 > SD2-depth 0.2516（Uni 更优）。即整模型微调的 SD2-depth 只在 FID 上压过 Uni，CLIP 维度 Uni 反超。
- **Content**：结果互有胜负——content-FID **Uni 23.98 反而更优**（< SD2-unclip 24.12，Table 5 把 Uni 加粗为 best）；content-CLIP SD2-unclip 0.2497 > Uni 0.2402（SD2-unclip 更优）。
- 结论：整模型微调在单一条件（尤其 depth-FID）上仍可领先，但代价是全模型微调且只支持一种条件；Uni 单模型支持全部条件，content 维度甚至 FID 反超 SD2-unclip。

**用户研究（附录 G，20 用户 ×20 案例 ×单/多条件）**：在"生成质量/与文本匹配/与条件对齐"三指标上，单条件设置 Uni-ControlNet 得票均居首（如生成质量 30.2%/121 票，对条件匹配 34.5%/138 票）；多条件设置同样显著优于 Multi-ControlNet 与 CoAdapter。

**关键消融**：
- **局部注入策略**：本文多尺度 FDN 注入 > Injection-S1（直接插值后 SPADE，破坏条件信息）> Injection-S2（仅输入层注入，类似 ControlNet/T2I-Adapter，深层丢信息、组合不和谐），FID/CLIP 多数条件本文最优。
- **全局注入**：必须把扩展 prompt 同时注入主干 SD（Injection-S3 仅注入 adapter 不注入主干 → 全局条件根本无法体现在结果里）。
- **训练策略**：分训（默认）≈ 分训后再联合微调 ≫ 直接联合训练（联合训练让全局条件欠学）。
- **条件冲突分析**（附录 B，仅分析用途）：条件"强度"排序为 HED > Canny > sketch > depth > MLSD > segmentation > Openpose（Openpose 最弱，冲突时常被忽略）。

## 创新点与影响
- **核心贡献**：把可控生成的条件**二分为 local/global 两类**，对应只需 **2 个共享 adapter**（恒定，不随条件数 N 增长），首个在单模型内统一多种局部+全局条件且**真正可组合**的微调式框架；同时大幅省微调成本与模型体积。
- **方法创新**：① 局部条件的**多尺度 FDN（SPADE 式）注入**，比 ControlNet 的单点注入对齐更好、组合更和谐；② 全局条件作为**扩展文本 token** 注入所有 cross-attention；③ **分开训练即可组合**的反直觉发现，免去联合训练成本；④ **只重训特征提取器首层卷积**即可扩展新条件。
- **影响**：与 ControlNet/T2I-Adapter/[[ip-adapter]] 一起成为 2023 年"冻结 SD + adapter 可控生成"范式的代表作，证明了"统一多条件 + 可组合"在轻量微调路线上可行，为后续统一可控/多条件融合工作提供了 local/global 二分与共享 adapter 的设计参考。开源（NeurIPS 2023，代码+预训练权重已放出，基座 SD v1.5）。
- **已知局限**：① 工程数字（参数量、GPU·时、推理耗时）**几乎未披露**；② Pose/Seg 等指标弱于专用 ControlNet（单模型通才 vs 专才的权衡）；③ 条件冲突时强弱不均（Openpose 最易被忽略）；④ 整模型微调的 SD2-depth 在 depth-FID 上仍领先 Uni（17.76 vs 21.20），说明冻结 adapter 路线相对全模型微调有上限（但仅限部分指标，content-FID 与 depth-CLIP 上 Uni 反而占优）；⑤ sketch 训练用 HED+简化合成、与真实手绘有分布差（实测泛化尚可但存在 gap）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2305.16322
- arxiv_pdf: https://arxiv.org/pdf/2305.16322
- github: https://github.com/ShihaoZhaoZSH/Uni-ControlNet
- project_page: https://shihaozhaozsh.github.io/unicontrolnet/
- hf_model: https://huggingface.co/shihaozhao/uni-controlnet

## 一手源存档（sources/）
- [arxiv-2305.16322.pdf](https://arxiv.org/pdf/2305.16322)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/uni-controlnet--readme.md)
