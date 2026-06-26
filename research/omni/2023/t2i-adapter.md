---
title: "T2I-Adapter: Learning Adapters to Dig out More Controllable Ability for Text-to-Image Diffusion Models"
org: "Tencent ARC Lab (PCG) / 北京大学"
country: China
date: "2023-02"
type: paper
category: edit
tags: [controllable-generation, adapter, plug-and-play, stable-diffusion, conditional-control, sketch, depth, segmentation, pose, color, sdxl]
url: "https://arxiv.org/abs/2302.08453"
arxiv: "https://arxiv.org/abs/2302.08453"
pdf_url: "https://arxiv.org/pdf/2302.08453"
github_url: "https://github.com/TencentARC/T2I-Adapter"
hf_url: "https://huggingface.co/TencentARC"
modelscope_url: ""
project_url: "https://huggingface.co/blog/t2i-sdxl-adapters"
downloaded: [arxiv-2302.08453.pdf, t2i-adapter--readme.md, t2i-adapter--hf-sdxl-blog.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
T2I-Adapter 是与 [[controlnet]] 同期（2023-02）提出的轻量级可控生成范式：冻结预训练 T2I 扩散模型（[[stable-diffusion-1]]），只训练一个 ~77M 参数、~300M 存储的小适配器，把外部控制信号（草图/深度/分割/姿态/颜色）与模型内部知识对齐，多条件可直接加权组合且无需重训；在 COCO 上 text+segmentation 取得 FID 16.78 / CLIP 0.2652，全面优于原始 SD（FID 24.68）。相比 ControlNet，它**整个去噪过程只前向一次**、参数小一个量级，后续在 SDXL 上把 1251M 的 ControlNet-SDXL 压到 79M（参数降 93.69%、存储降 94%）。

## 背景与定位
- **要解决的问题**：大规模 T2I 模型（SD/Imagen/DALL·E）生成质量很高，但只靠 text prompt 无法精细、稳定地控制结构与颜色；对"A car with flying wings""Iron Man with bunny ears"这类需要精确结构引导的想象性场景，纯 SD 经常失败。作者的核心论点是——SD **不是没有**生成此类结构的能力，而是 text 无法提供准确的结构引导。
- **作者的洞察**："dig out"（挖掘）模型隐式学到的从低层（纹理）、中层（边缘）到高层（语义）的能力，用一个小 adapter 学习"外部控制信号 ↔ 内部知识"的**对齐（alignment）映射**，而不是去学新的生成能力——因此可以用很少的数据、很低的成本完成。
- **技术脉络**：adapter 思想源自 NLP（Houlsby 等 2019 的 parameter-efficient transfer learning、BERT-PALs），CV 里有 ViT-Adapter；本文是把低成本 adapter 首次用到预训练 T2I 扩散模型上做条件控制。
- **与并行工作的关系**：论文明确把 [[controlnet]]（Zhang & Agrawala，arXiv 2302.05543，早 6 天）和 Composer（Huang 等 2023，retrain 一个 diffusion 条件模型）列为 concurrent work。三者共同开创了"在冻结 SD 上做空间可控生成"的范式；T2I-Adapter 的差异化卖点是**更小、更快、可组合、可泛化**。基于 [[latent-diffusion-ldm]] 的两阶段 latent 扩散框架。

## 模型架构
- **Backbone（被冻结）**：Stable Diffusion v1.4（两阶段 latent diffusion）= 一个 autoencoder（图像 ↔ latent）+ 一个 U-Net 去噪器；text 经 CLIP text encoder 编码、通过 cross-attention 注入。SD 全程**参数冻结**，只训练 adapter。
- **Adapter 结构（可训练，~77M）**：
  - 输入：原始条件图 512×512。先用 **pixel unshuffle**（亚像素下采样）降到 64×64。
  - 主体 = **4 个特征提取块 + 3 个下采样块**；每个尺度由 1 个卷积层 + 2 个残差块（RB）组成，逐级提取多尺度条件特征 Fc = {F1,F2,F3,F4}，4 个尺度分别为 64×64 / 32×32 / 16×16 / 8×8。
  - **条件注入**：Fc 的维度与 U-Net **encoder** 各尺度中间特征 Fenc 对齐，直接逐尺度相加：F̂enc_i = Fenc_i + Fc_i（i∈{1,2,3,4}）。注入只发生在 U-Net **encoder 端**（消融见下，注入 encoder 比注入 decoder 路径更短、效果更好；同时注入 enc+dec 会导致控制过强、纹理变差）。
  - **不引入 time embedding**：作者发现给 adapter 加 time embedding 能增强引导，但会要求 adapter 参与每一步迭代，违背"简单/小"的初衷；改用训练采样策略（见训练方法）规避。
- **空间颜色调色板（spatial color palette）**：为控制色调（hue）与颜色空间分布，用 64× 双三次下采样去掉语义/结构信息、只保留颜色，再用最近邻上采样还原尺寸，得到"色块排布"作为颜色条件图。
- **多 adapter 组合**：Fc = Σ_k ω_k · F_AD^k(C_k)，ω_k 为可调权重，**无需任何额外训练**即可叠加多条件（如 sketch 控结构 + color 控颜色，depth + keypose 等）。
- **模型规模档位（消融，论文 Fig.12）**：base 77M / 300M存储（其它结构条件用）、small 18M / 72M存储（×4 压缩，颜色这种粗粒度条件用）、tiny 5M / 20M存储（×8 压缩）。tiny 版在 sketch 引导上仍有可观控制力。（注：README 又给出 color adapter 仅 17M、style/canny/openpose 等 Adapter Zoo 系列。）
- **SDXL 版（2023-08~09，与 HF diffusers 合作）**：沿用**同一配方**，用 79M（部分 77M）adapter 驱动 2.6B 的 [[sdxl]]，分辨率提到 1024×1024，依然单次前向。

## 数据
五类条件，各自的训练数据（来自论文 4.1）：
- **Sketch（草图）**：COCO17，约 164K 图；草图用 PiDiNet（边缘预测，文献[41]）生成后以 0.5 阈值二值化。
- **Semantic segmentation（语义分割）**：COCO-Stuff，约 164K 图；80 thing 类 + 91 stuff 类 + 1 unlabeled。
- **Keypose / Color / Depth**：从 **LAION-Aesthetics** 选 **600K** 图文对。keypose 用 MMPose 提取，depth 用 MiDaS 生成。
- 每个训练样本是三元组（原图 X0、条件图 C、文本 prompt y）。
- **SDXL 版数据（HF 官方博客）**：博客里提到的多数 SDXL adapter 用 **LAION-Aesthetics V2** 的 **3M 高分辨率图文对**训练。
- 安全/美学过滤、re-captioning 等细节：论文与博客**未披露**（条件图均由现成检测器自动生成）。

## 训练方法
- **训练目标**：与 SD 一致的 latent 扩散 ε-预测 MSE，但只优化 adapter，SD 冻结：
  L_AD = E[ ‖ε − ε_θ(Z_t, t, τ(y), F_c)‖² ]，Z_t 由 Z0 加噪而来，F_c 为 adapter 输出的条件特征。
- **关键 trick — 非均匀（cubic）时间步采样**：作者把 DDIM 采样均分为 beginning/middle/late 三阶段做引导实验，发现**主体内容在早期采样步就基本定型**，中/晚期加引导几乎无效。若训练时 t 均匀采样，落在晚期的样本会"学不到"引导。于是改用 cubic 分布 `t = (1 − (t/T)³)·T, t∼U(0,T)` 提高 t 落在早期的概率。消融显示：均匀采样引导偏弱（尤其颜色控制），cubic 采样显著纠正这一弱点。这是本文一个标志性 trick。
- **超参（SD v1.4，论文）**：训练 10 epoch，batch size 8，Adam，lr 1e-5，输入与条件图 resize 到 512×512；**4×NVIDIA Tesla V100 32G，3 天内完成**。
- **超参（SDXL，README + HF 博客）**：
  - README 训练命令：`accelerate launch`，SDXL-base-1.0，分辨率 1024，lr 1e-5，max_train_steps 60000，train_batch_size 1，gradient_accumulation_steps 4，fp16，4×A100。
  - HF 博客（多数 SDXL adapter）：train steps 20000–35000，单卡 batch 16 × 8 卡数据并行 = 总 batch 128，constant lr 1e-5，fp16。
- **不蒸馏、无 RLHF/DPO/偏好对齐、无 consistency/LCM 步数蒸馏**：本工作是纯条件适配器训练，不涉及加速蒸馏或人类偏好对齐。

## Infra（训练 / 推理工程）
- **训练算力**：SD v1.4 版 = 4×V100-32G × 3 天（极低成本，呼应"low training cost"卖点）；SDXL 版 = 4×A100，fp16 混合精度（HF 博客是 8 卡数据并行总 batch 128）。
- **推理效率（核心优势）**：adapter 在**整个去噪过程只前向一次**（条件特征在采样开始时算好后注入各步），与 SD 共享 U-Net 前向；对比 [[controlnet]] 需在**每个去噪步**同时跑 ControlNet + U-Net，T2I-Adapter 显著更省算力。
- **参数/存储效率（HF 官方博客实测对比表）**：

  | 模型 | 参数 | 存储(fp16) |
  | --- | --- | --- |
  | ControlNet-SDXL | 1251 M | 2.5 GB |
  | ControlLoRA (rank 128) | 197.78 M (↓84.19%) | 396 MB (↓84.53%) |
  | **T2I-Adapter-SDXL** | **79 M (↓93.69%)** | **158 MB (↓94%)** |

- **部署**：已并入 HuggingFace `diffusers`（`StableDiffusionXLAdapterPipeline` / `T2IAdapter`），SDXL 推理至少需 15GB 显存；提供 HF Gradio 在线 demo 与 Doodly 涂鸦 demo。Stability AI 的 **Stable Doodle**（ClipDrop，2023-07）即基于 T2I-Adapter + SDXL。
- **推理可调旋钮（diffusers/HF 博客）**：`adapter_conditioning_scale`（控制条件影响强度）与 `adapter_conditioning_factor`（控制前多少比例的步施加条件，0–1，=1 即全程、=0.5 即仅前 50% 步）——后者正是上文"早期步定型"结论的工程落地。

## 评测 benchmark（把效果讲清楚）
**COCO validation（5000 图）上 FID↓ / CLIP Score↑（ViT-L/14），论文 Table 1：**

| 方法 | 条件 | FID↓ | CLIP↑ |
| --- | --- | --- | --- |
| SPADE | segmentation | 23.44 | 0.2314 |
| OASIS | segmentation | 18.71 | 0.2274 |
| PITI | segmentation | 19.36 | 0.2287 |
| PITI | sketch | 21.21 | 0.2129 |
| SD（仅 text） | text | 24.68 | 0.2648 |
| **Ours** | **text+segmentation** | **16.78** | **0.2652** |
| **Ours** | **text+sketch** | 17.36 | **0.2666** |

- **结论**：T2I-Adapter（text+seg）FID 16.78 全表最佳，且**比纯 SD（24.68）更低**——加结构引导不仅带来可控性，还顺带提升了生成质量与规整度；CLIP Score（0.2652/0.2666）也优于所有 GAN/扩散对比方法。
- **消融 1 — 引导注入位置（Table 2，固定 sketch）**：
  - mode1 仅 encoder 4 尺度：FID 17.36（最佳，最终采用）
  - mode2 仅 decoder 4 尺度：18.32
  - mode3 enc+dec 都注入：18.08（控制过强、纹理受限）
  - 尺度数减少：4→3→2→1 尺度 FID 17.86→18.77→**22.66**（单尺度明显劣化，多尺度有正向作用）。
- **消融 2 — 模型复杂度**：base(77M)/small(18M)/tiny(5M) 三档，tiny 在 sketch 引导上仍保持可观控制力，证明条件图稀疏、可用更轻的提取器。
- **消融 3 — cubic vs uniform 时间步采样**：可视化显示 uniform 引导偏弱（颜色控制尤甚），cubic 显著纠正（定性，未给数值）。
- **应用层面（定性）**：单/多 adapter 控制、局部编辑（擦除区域 + 注入 adapter 引导走 SD inpainting）、可组合控制（depth+keypose、sketch+color）、可泛化（SD-V1.4 训练的 sketch adapter 直接用于 SD-V1.5 与 Anything-V4.0 等同源微调模型）。
- **未报告**：GenEval / T2I-CompBench / DPG-Bench / HPSv2 / ImageReward / PickScore / 人评 ELO 等现代偏好与组合基准，论文时代尚未流行，**均未报告**；SDXL 版亦未给出量化基准，HF 博客只展示定性结果与参数/存储对比。

## 创新点与影响
- **核心贡献**：
  1. 提出"alignment 而非 re-learning"的可控生成新视角——小 adapter 把外部控制信号映射到冻结 T2I 模型已有的内部知识。
  2. 极致的轻量与高效：~77M 参数、整个去噪过程**仅一次前向**，训练 4×V100×3 天即可。
  3. 五大类条件统一框架（sketch/depth/seg/keypose/color）+ **免训练可加权组合** + **跨同源模型泛化**。
  4. cubic 非均匀时间步采样、encoder 端多尺度注入两项实用 trick。
- **影响**：
  - 与 [[controlnet]] 共同确立"冻结 SD + 外挂条件模块"的可控生成主流范式；T2I-Adapter 成为"轻量/快"路线的代表，被并入 `diffusers`，并直接催生 Stability AI 的 Stable Doodle 产品。
  - 启发了一系列 adapter 式条件注入工作；同组随后的 [[ip-adapter]] 把同一"小适配器对齐内部知识"思路推广到图像 prompt（image conditioning）。
  - "整个采样只前向一次"的设计为后续追求实时/低延迟可控生成提供了范本。
- **已知局限（作者明示）**：多 adapter 组合时各条件的融合权重 ω 需**手动调节**，缺乏自适应融合；作者将"多模态引导的自适应融合"列为 future work。SDXL 版受算力限制，作者自述 adapter"仍需进一步改进"。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2302.08453
- arxiv_pdf: https://arxiv.org/pdf/2302.08453
- github: https://github.com/TencentARC/T2I-Adapter
- hf_official_blog（一等公民，含 SDXL 训练细节与参数/存储对比表）: https://huggingface.co/blog/t2i-sdxl-adapters
- hf_models: https://huggingface.co/TencentARC （t2i-adapter-{sketch,canny,lineart,openpose,depth-midas,depth-zoe}-sdxl-1.0）
- diffusers_docs: https://huggingface.co/docs/diffusers/main/en/api/pipelines/stable_diffusion/adapter

## 一手源存档（sources/）
- [arxiv-2302.08453.pdf](https://arxiv.org/pdf/2302.08453)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/t2i-adapter--readme.md)
- [hf-sdxl-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/t2i-adapter--hf-sdxl-blog.md)
