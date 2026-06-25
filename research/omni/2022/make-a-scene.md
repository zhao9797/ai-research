---
title: "Make-A-Scene: Scene-Based Text-to-Image Generation with Human Priors"
org: "Meta AI Research"
country: US
date: "2022-03"
type: paper
category: t2i
tags: [t2i, autoregressive, vqgan, scene-control, segmentation, classifier-free-guidance, human-prior, meta]
url: "https://arxiv.org/abs/2203.13131"
arxiv: "https://arxiv.org/abs/2203.13131"
pdf_url: "https://arxiv.org/pdf/2203.13131"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2203.13131.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Make-A-Scene 是 Meta AI 2022 年的自回归 token-based 文生图模型（4B 参数 GPT-3 式 transformer），核心创新是把**语义分割图（"场景"）当作可选的隐式控制条件**与文本并列输入，并对 VQ tokenizer 注入"人脸/显著物体"的人类先验感知损失，再把无分类器引导（CFG）从扩散模型迁移到自回归 transformer——在 MS-COCO 零样本 FID 上达到 **7.55**（256×256 模型、含 MS-COCO 训练集设定；不含 MS-COCO 训练集的 filtered 设定为 11.84，仍是同组最低），并能直出 **512×512** 高分辨率图像，同时人评在画质/真实感/文本对齐三项上全面超过自家复现的 DALL-E 与 CogView。

## 背景与定位
2022 年初的文生图主流是自回归 token 模型（[[dall-e-1]]、[[cogview]]）与扩散模型（[[glide]]），但论文指出三个关键短板：
1. **可控性（Controllability）**——只接受文本输入，结构/形态/排布等空间信息只能"勉强用文字描述"，用户对画面缺乏掌控感；既有的额外控制（如 bounding box）只能给出粗糙、低分辨率结果。
2. **人类感知（Human perception）**——生成损失对全图均匀施加，与人类注意力（尤其是人脸像素的重要性）不匹配，导致人脸/显著物体生成质量差。
3. **画质与分辨率**——前序 SOTA（DALL-E/GLIDE）受限于 256×256，超分网络会进一步劣化质量。

Make-A-Scene 沿用 [[dall-e-1]] / [[cogview]] 的"两阶段 + 自回归 transformer"范式（先训 VQ tokenizer，再在离散 token 空间上自回归建模），但在三处做出改进：(i) 新增**场景 token（分割图）作为隐式条件**，(ii) 给 tokenizer 加**人脸/物体感知损失**提升重建上界，(iii) 把 [[classifier-free-guidance]]（Ho & Salimans 提出、由 GLIDE 用于扩散）适配到 transformer logits 上。技术谱系上它属于 VQGAN([[taming-transformers-vqgan]])+自回归一脉，是扩散全面接管 T2I（[[latent-diffusion-ldm]]/[[imagen]]/[[dall-e-2]]）之前 Meta 的代表性 T2I 工作。

## 模型架构
整体为**三段式自回归 transformer**（基于 GPT-3 架构），token 序列依次为 `[text tokens → scene tokens → image tokens]`，三个 token 空间相互独立、按顺序自回归生成：

- **Backbone（transformer）**：48 层、48 注意力头、embedding 维度 2560，约 **4B 参数**。序列长度 = 256 文本 token + 256 场景 token + 1024 图像 token。256×256 与 512×512 两个模型共享 transformer 架构，仅 VQ-IMG 与 object-aware 损失不同。
- **文本编码**：BPE 编码，长度 256（普通子词分词，非 CLIP/T5 文本编码器）。
- **场景表示与 tokenizer（VQ-SEG）**：场景由三组互补语义分割并集构成——**panoptic 全景分割（133 类）、human 人体解析（20 类）、face 人脸解析（5 类）**，外加 1 个**边缘通道**（分隔相邻同类实例、并对稀有重要类别加权，因为周长/边缘比像素面积更不偏向大类别）。VQ-SEG 是改造的语义分割 VQ-VAE，输入输出为 `m = 133+20+5+1` 通道，字典大小 1024。
- **图像 tokenizer（VQ-IMG）**：在 VQGAN 框架上改造，字典大小 8192，把图像编码为 1024 个 token。512×512 模型相比 256×256 在 encoder/decoder 各加一层下/上采样（channel multiplier 从 `[1,1,2,4]` 变为 `[1,1,2,4,4]`）。
- **条件注入方式**：场景是**隐式条件**——分割 token 与图像 token 之间**没有损失约束**绑定，transformer 可以选择忽略场景信息只看文本生成。论文强调这与 GAN 类方法（pix2pix/SPADE）的"显式分割条件"不同，隐式条件反而提升了样本多样性，同时仍能让文本与场景共同主导画面。推理时场景 token 可由 transformer 自行生成（纯文本输入），也可从输入图像/手绘草图提取，从而获得"先画场景再生成图"的可控能力。
- **分辨率策略**：直接训练 256×256 与 512×512 两套 VQ-IMG/transformer，512 靠 object-aware 感知损失把重建质量撑到高分辨率，无需级联超分。

## 数据
- **场景 transformer 训练集**：CC12m + CC（Conceptual Captions）+ YFCC100m 子集 + Redcaps 子集，合计约 **35M 图文对**。除非特别说明，评测在 **MS-COCO** 上进行。
- **VQ-SEG / VQ-IMG 训练集**：CC12m + CC + MS-COCO。
- **分割标注来源**：panoptic 用 Detectron2 提取，human parsing 用 Self-Correction for Human Parsing，face parsing/landmark 用 Bulat & Tzimiropoulos 的人脸对齐工具——即分割条件是**用现成模型自动标注**得到的，而非人工标注。
- 清洗/过滤/配比/美学/安全过滤等细节**未披露**。

## 训练方法
**两阶段范式**：先训两个 VQ tokenizer，再训自回归 transformer（next-token 预测，交叉熵）。

- **VQ-SEG**：训 600k 迭代，batch 48，字典 1024。引入**加权二元交叉熵人脸损失（LWBCE）**——对人脸部件类别（眉/眼/鼻/外嘴/内嘴，类别 154–158）权重设为 20，其余为 1，解决"人脸部件像素太少在重建中被丢弃"的类别不平衡问题（不直接用 focal loss，避免抬高"牙刷/水果"这类稀有但不重要的类别）。
- **Face-aware VQ（人脸感知损失 LFace）**：在 VQ-IMG 上对人脸区域施加**预训练人脸识别网络（VGGFace2）的特征匹配损失**，按层归一化系数 α_fl 加权，每图最多取 k_f 个人脸 crop 过人脸网络，注入人脸感知先验。
- **Object-aware VQ（物体感知损失 LObj）**：把人脸感知泛化到 panoptic 中的 "things" 物体——用 ImageNet 预训练 **VGG** 网络对物体 crop 做特征匹配损失（α_ol 取自 LPIPS）。通过对图像 crop 而非全图做特征匹配，得以从 256 扩到 **512×512** 分辨率。VQ-IMG256/512 分别训 800k / 940k 迭代，batch 192 / 128。
- **Scene-based transformer**：训 **170k 迭代**，batch **1024**，Adam（β1=0.9, β2=0.96，weight decay 4.5e-4）。学习率前 40k 为 4.5e-4，之后降到 1.5e-4。图像/文本 token 损失比 **7:1**。
- **Transformer Classifier-Free Guidance（核心 trick）**：把 CFG 适配到自回归 transformer——在**最后 30k 迭代**微调 transformer 时以概率 **p_CF = 0.2** 把文本 token 替换为 padding，从而获得无条件分支。推理时并行跑条件流（`logits_cond = T(t_y,t_z|t_x)`）与无条件流（`logits_uncond = T(t_y,t_z|∅)`），按 `logits_cf = logits_uncond + α_c·(logits_cond − logits_uncond)` 在 **logit 层面**引导后采样下一个 token（场景或图像）；引导尺度 α_c = 5（α_c = 3 亦可）。这使模型**无需 CLIP re-ranking 等生成后过滤**，更快且文本对齐更好。
- **采样**：每步取概率最高的一半 logits，softmax 后从多项分布采一个 token。
- 蒸馏/一致性加速等**未涉及**（该工作不做步数蒸馏，自回归本身是逐 token 解码）。

## Infra（训练 / 推理工程）
- 论文明确实验用 **4B 参数 transformer**，但**算力规模（GPU 数量/型号/GPU·时）、并行分布式策略、混合精度、吞吐量等训练工程细节均未披露**。
- 推理为自回归逐 token 解码 + CFG 双流（条件/无条件并行前向），相比依赖 CLIP re-ranking 的方案更快；具体延迟/吞吐数字未报告。
- **未开源代码与权重**，无官方部署形态披露（论文仅附演示视频与样本，无 GitHub/HF 模型发布）。

## 评测 benchmark（把效果讲清楚）
所有 FID 在 **MS-COCO 验证集文本 prompt 生成的 30k 图像子集**上计算、不做 re-ranking。人评每个问题用 500 对图、5 名评测者 → 每对比 2500 个判断，三维度：画质 / 真实感 / 文本对齐，报为"投我方为多数"的百分比。

**Table 1 — 与前序工作对比（MS-COCO zero-shot FID + 人评）**。两组：FID 列＝**含** MS-COCO 训练集训练；FID(filt.) 列＝**不含** MS-COCO 训练集（filtered）训练。人评三列为 Ours256 对该模型的多数票胜率（仅对 DALL-E / CogView 两组做了人评）：
| 模型 | FID↓ | FID↓(filt.) | 画质胜率 | 真实感 | 文本对齐 |
|---|---|---|---|---|---|
| AttnGAN | 35.49 | — | — | — | — |
| DM-GAN | 32.64 | — | — | — | — |
| DF-GAN | 21.42 | — | — | — | — |
| DM-GAN+CL | 20.79 | — | — | — | — |
| XMC-GAN | 9.33 | — | — | — | — |
| DALL-E（自家复现） | — | 34.60 | 81.8% | 81.0% | 65.9% |
| CogView256 | — | 32.20 | 92.2% | 94.2% | 92.2% |
| CogView512 | — | 36.53 | 91.1% | 88.2% | 87.8% |
| LAFITE | 8.12 | 26.94 | — | — | — |
| GLIDE | — | 12.24 | — | — | — |
| **Ours256** | **7.55** | **11.84** | — | — | — |
| Ground-truth（练/验子集间，实践下界） | 2.47 | — | — | — | — |

> 关键结论：在"是否用 MS-COCO 训练集"两种设定下本文 FID 均为同组最低——含 MS-COCO 训练时 **7.55**（vs DM-GAN+CL 20.79、XMC-GAN 9.33），不含时 **11.84**（filtered，vs DALL-E 34.60、CogView256 32.20、CogView512 36.53、GLIDE 12.24、LAFITE 26.94）。真实数据子集间的实践下界为 2.47。人评（多数票胜率，三维度全报）：对自家复现 DALL-E 画质/真实感/文本对齐 = **81.8% / 81.0% / 65.9%**；对 CogView256 = **92.2% / 94.2% / 92.2%**；对 CogView512（用对应 512 模型比）= **91.1% / 88.2% / 87.8%**——三个对手、三维度全部过半占优。

**Table 2 — 消融（FID + 人评胜率，逐步加组件）**：
| 设定 | FID↓ | 画质胜率 | 真实感 | 文本对齐 |
|---|---|---|---|---|
| Base | 18.01 | — | — | — |
| +Scene tokens | 19.16 | 57.3% | 65.3% | 58.3% |
| +Face-aware | 14.45 | 63.6% | 59.8% | 57.4% |
| +CF（classifier-free guidance） | **7.55** | 76.8% | 66.8% | 66.8% |
| +Obj-aware512 | 8.70 | 62.0% | 53.5% | 52.2% |
| +CF with scene input | **4.69** | — | — | — |

**关键消融结论**：
- 加场景 token 后 FID 略升（18.01→19.16）但人评全面变好——说明场景的价值在可控性与人类偏好，而非 FID 单指标。
- **人脸感知损失**把 FID 从 19.16 大幅降到 14.45（+人评提升）。
- **Classifier-free guidance 是最大单点增益**：FID 14.45→7.55，画质胜率 76.8%、真实感/对齐均 66.8%，是拿到 SOTA FID 的关键。
- 512 的 object-aware 模型 FID（8.70）虽不如 256（7.55）低，但**人评在画质上更受偏好**——作者据此采用 512 模型，体现"FID 最优 ≠ 人类最偏好"。
- 当**额外给定场景输入**（而非纯文本）时，FID 进一步降到 **4.69**，逼近 2.47 的实践下界，量化证明场景条件确实拉近了与真实分布的差距。

**新能力（定性，非数值）**：复杂场景生成、克服分布外（OOD）文本提示（用近似类别如"大象"代"老鼠"、"猫"代"狮子"画出"老鼠猎狮"）、场景编辑（替换/新增类别）、anchor 场景 + 文本编辑、以及作者自写童书的故事插画生成（保持跨帧一致性）。

## 创新点与影响
**核心贡献**：
1. **场景作为隐式可控条件**：首次把语义分割图（panoptic+human+face 三组并集 + 边缘通道）作为与文本并列的 token 序列、且**不加绑定损失**地隐式注入自回归 T2I，兼得可控性与多样性——把"用草图/分割控制布局"带进 token-based 文生图。
2. **人类先验的 tokenizer 感知损失**：在 VQ tokenizer 阶段对人脸（VGGFace2 特征匹配 + 加权 BCE）与显著物体（VGG/LPIPS 特征匹配）施加 region-aware 感知损失，抬高重建上界、并把分辨率推到 **512×512** 而无需级联超分。
3. **Transformer 版 Classifier-Free Guidance**：把 CFG 从扩散迁移到自回归 transformer 的 logit 层面，**省掉 CLIP re-ranking 的生成后过滤**，是涨点最大的单项。

**影响**：Make-A-Scene 是扩散方法（[[latent-diffusion-ldm]]/[[dall-e-2]]/[[imagen]]）接管 T2I 之前、自回归 token 路线上"可控生成 + 人类偏好对齐 + 高分辨率"的代表作，其"分割/草图条件 + 隐式注入 + transformer CFG"思路对后续可控生成（ControlNet 类布局控制、token 化统一多模态生成）有铺垫意义；它也是 Meta 后续 [[emu]] / Make-A-Video 等生成线的早期积累。

**已知局限**：
- 仍是自回归逐 token 解码，推理不如扩散/蒸馏快；
- 场景控制依赖固定分割类别表，OOD 物体只能用近似类别"借位"（如猫代狮子），无法真正生成不存在的类别；
- 依赖现成分割模型自动标注，标注质量受限；
- 未开源、训练算力与工程细节未公开；512 模型 FID 反不及 256，需在指标与人评间权衡。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2203.13131
- arxiv_pdf: https://arxiv.org/pdf/2203.13131

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2203.13131.pdf
