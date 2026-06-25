---
title: "GenTron: Diffusion Transformers for Image and Video Generation"
org: "Meta / HKU"
country: US
date: "2023-12"
type: paper
category: method
tags: [dit, diffusion-transformer, text-to-image, text-to-video, scaling, motion-free-guidance, t2i-compbench]
url: "https://arxiv.org/abs/2312.04557"
arxiv: "https://arxiv.org/abs/2312.04557"
pdf_url: "https://arxiv.org/pdf/2312.04557"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.shoufachen.com/gentron_website/"
downloaded: [arxiv-2312.04557.pdf, gentron--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GenTron 是 Meta 与香港大学把 [[dit-scalable-diffusion-transformers]]（Diffusion Transformer）从「类条件」推广到「自由文本条件」并系统扩到 3B+ 参数的工作，首次用**纯 Transformer**（无任何卷积/U-Net）做文生图与文生视频；对视频提出 **motion-free guidance（MFG）**新技术。最亮眼结果：在 SDXL 盲评中视觉质量 **51.1% 胜率**、文本一致性 **42.3% 胜率**，T2I-CompBench 综合均分 **49.99**（超 PixArt-α 48.15 / SDXL 44.41）。

## 背景与定位
2023 年视觉生成的主流 backbone 仍是 CNN-based U-Net（SD、SDXL、Imagen），这与 NLP（Transformer 一统）和视觉感知（ViT/Swin）的趋势相悖。Transformer 在感知与语言任务上已证明强可扩展性（最大 dense LLM 540B、最大 vision model 22B），但当时最大的 diffusion transformer——[[dit-scalable-diffusion-transformers]] 的 DiT-XL/2 仅 ~675M 参数，远落后于 3B+ 的 U-Net 扩散模型。GenTron 的目标就是**填补"视觉生成"在架构选择上与另外两个领域的鸿沟**，系统回答两个问题：(1) DiT 从类条件迁到文本条件时，条件机制该怎么选；(2) Transformer 扩散模型扩到 3B 能否带来质量提升。

技术脉络上，GenTron 直接建在 [[dit-scalable-diffusion-transformers]]（DiT-XL/2）之上，并继承 [[latent-diffusion-ldm]] 的潜空间扩散范式（VAE 压缩 + 在 latent 上去噪）；与**同期**的 PixArt-α 是并行工作——PixArt-α 主打三阶段高效训练，GenTron 则聚焦**条件策略设计 + 可扩展性**，并额外把探索延伸到视频（PixArt-α 不涉及）。视频侧建在 [[align-your-latents-vldm]]、VDM、Imagen Video、LaVie 等 latent video diffusion 谱系之上，但把时序建模做成了**纯 Transformer 的轻量时序自注意力**。

## 模型架构
**Backbone：纯 DiT（非层次化 Transformer），无 U-Net、无卷积。** 沿用 DiT-XL/2 设计：把 LDM 输出的 32×32×4 latent 经 2×2 patchify 切成不重叠 token 序列，过一串 transformer block，最后用标准 linear decoder 解回 latent。

**从「类条件」到「文本条件」——两个核心设计维度（论文最大的实证贡献）：**

1. **文本编码器选型。** 对比了多模态模型的语言塔 CLIP-L（MM）、纯 LLM Flan-T5-XXL（LLM），以及两者组合 CLIP-T5XXL（MM+LLM）。结论：T5 embedding 在组合性（compositionality）上优于 CLIP-L；**CLIP-L + T5-XXL 组合最佳**——多文本编码器时用 **interleaved cross-attention（交错交叉注意力）**：在一个 block 用 CLIP embedding，下一个 block 切到 Flan-T5 embedding，交替进行；训练与推理用同一设置（与 eDiff-I 训练用双编码器、推理可单可双不同）。

2. **条件注入方式。** 对比 adaLN-Zero vs. cross-attention：
   - **adaLN（adaptive layer norm）**：把条件 embedding 当作 feature channel 上的归一化参数，全局调制——这是 DiT 在类条件下的标准做法。但论文发现它在**自由文本条件下失效**（生成 panda 的例子明显劣化，T2I-CompBench 全指标落后）。原因：类条件只有有限固定信号（如 ImageNet 1000 类 one-hot），全局调制够用；而自由文本无限多样、需要空间细粒度对齐。
   - **cross-attention**：图像特征作 query、文本 embedding 作 key/value，逐空间位置动态调制——更适合文本条件，全指标占优。GenTron 的关键改动：**保留 adaLN 来单独建模 time embedding**（time 对所有空间位置一致，受益于 adaLN 的全局调制），同时把 pooled text embedding 加到 time embedding 上；这与 DiT 原版把 class+time 先 concat 的 cross-attn 不同。

**参数与配置（Table 1）：**
- **GenTron-XL/2**：depth 28、width 1152、MLP width 4608，**930.0M** 参数。
- **GenTron-G/2**：depth 48、width 1664、MLP width 6656，**3083.8M（3B+）** 参数——按 Zhai 等《Scaling ViT》的策略同时扩 depth/width/MLP-width，作者称这是"当时已知最大的 transformer-based diffusion 架构"。

**文本→视频（GenTron-T2V）架构改动（首个纯 Transformer 视频扩散尝试）：**
- 在每个 transformer block 里，于 cross-attention 之后、MLP 之前插入**轻量时序自注意力 TempSelfAttn**。不像传统做法（如 Align-your-latents）同时加 3D 时序卷积 + 时序 transformer，GenTron **只加 TempSelfAttn**。
- 用 einops rearrange 把 `(b t) n d → (b n) t d` 做时序注意力再 reshape 回来（b 批、t 帧、n 每帧 patch 数、d 通道）。作者发现单一 TempSelfAttn 足以捕获运动（与 LaVie 一致），且便于"开关"时序建模——这是 MFG 的前提。
- **初始化**：共享层用预训练 T2I 模型初始化；新增 TempSelfAttn 的输出投影层权重/偏置**置零**，保证微调初期等价于恒等映射（配合 shortcut）。

## 数据
- **图像（T2I）**：用 Meta **内部数据集**，规模 ~**550M** 图文对（论文在 Table 4 注明"GenTron 比 U-Net 的 SD v1.4 少用约 4 倍数据：550M vs 2B"）。来源/清洗/re-caption/美学过滤等细节**未披露**。
- **视频（T2V）**：约 **34M 视频**。预处理：短边 resize 到 512 像素、帧率 24 FPS；训练时每个 clip 取 **8 帧**、采样率 **4 FPS**。论文坦言公开视频数据在质量与数量上都远逊图像（举例：LAION 有 2B+ 英文图文对，而当时常用的 WebVid-10M 仅 10.7M 视频文本对，且大量帧有运动模糊与水印）。
- **合成数据 / 偏好数据**：未使用（无 RLHF/DPO/reward model 环节）。

## 训练方法
- **训练目标**：标准 DDPM 噪声预测（ε-prediction）的 latent diffusion；**未使用** flow matching / rectified flow / 一致性蒸馏等（2023 末，这些在 T2I 主线尚未普及）。
- **优化器与 LR**：AdamW，**恒定学习率 1×10⁻⁴**（全系列变体一致）。
- **多阶段课程（T2I，沿 LDM/SDXL 范式）**：
  - 低分辨率 256×256：batch size **2048**，**500K** 步；
  - 高分辨率 512×512：batch size **784**，**300K** 步。
- **T2V 微调（两个核心解法）：**
  1. **联合图-视频训练（Solution I）**：缓解视频数据短缺与图-视频域差异——运动被关闭的训练步加载图文对，把图像重复 T−1 次拼成"伪视频"；运动开启则加载真实 video clip 抽 T 帧。
  2. **Motion-Free Guidance / MFG（Solution II，本文最大视频创新）**：把"视频内的时序运动"类比为一种特殊条件信号（类似文本条件），借鉴 classifier-free guidance。训练时以概率 p_motion_free 把 TempSelfAttn 的注意力 mask 换成**单位矩阵**（motion-free mask，对角全 1、其余 0），从而把时序注意力限制在单帧内、等效关闭时序建模（因为 TempSelfAttn 是唯一的时序算子）。推理时同时有文本条件 c_T 与运动条件 c_M，按公式扩展 score：
     `ε̃ = ε(x,∅,∅) + λ_T·[ε(x,c_T,c_M) − ε(x,∅,c_M)] + λ_M·[ε(x,∅,c_M) − ε(x,∅,∅)]`，
     即文本与运动各有一个独立 guidance scale。实测**固定 λ_T = 7.5、逐样本调 λ_M ∈ [1.0, 1.3]** 效果最好。
- **超大模型显存优化（仅 GenTron-G/2）**：集成 **FSDP（Fully Sharded Data Parallel）+ activation checkpointing（AC）**。

## Infra（训练 / 推理工程）
- **并行/显存**：GenTron-G/2（3B+）用 **FSDP + activation checkpointing** 优化 GPU 显存；这是论文明确披露的工程手段。
- **视频数据 IO 优化**：视频预压到短边 512、24 FPS 落盘，以省存储、提升 data loading 效率；训练 batch 128 个 clip。
- **GPU 数量 / GPU·时 / 吞吐 / 混合精度 / 推理加速（步数蒸馏、缓存、量化）/ 部署形态**：均**未披露/未报告**。无开源代码与权重，无 serving 细节。

## 评测 benchmark（把效果讲清楚）

**(1) 条件策略与规模消融（Table 2，T2I-CompBench，统一 XL/2 除最后一行）——综合均分（Complex Mean）：**

| 配置 | 文本编码器 | 注入 | 规模 | Color | Shape | Texture | Spatial | Non-spatial | Complex | Mean |
|---|---|---|---|---|---|---|---|---|---|---|
| adaLN-zero | CLIP-L | adaLN | XL/2 | 36.94 | 42.06 | 50.73 | 9.41 | 30.38 | 36.41 | 34.32 |
| cross-attn | CLIP-L | cross | XL/2 | 73.91 | 51.81 | 68.76 | 19.26 | 31.80 | 41.52 | 47.84 |
| cross-attn | T5-XXL | cross | XL/2 | 74.90 | 55.40 | 70.05 | 20.52 | 31.68 | 41.01 | 48.93 |
| cross-attn | CLIP-T5XXL | cross | XL/2 | 75.65 | 55.74 | 69.48 | 20.67 | 31.79 | 41.44 | 49.13 |
| cross-attn | CLIP-T5XXL | cross | **G/2** | **76.74** | **57.00** | **71.50** | **20.98** | **32.02** | **41.67** | **49.99** |

（列含义：Color/Shape/Texture 为 attribute binding；Spatial/Non-spatial 为 object relationship；Complex 为复杂组合分；Mean 为综合均分。)

关键结论：**adaLN→cross-attn 在文本条件下是质变**（34.32→47.84，第一行到第二行全指标碾压）；**T5 > CLIP-L**（compositionality）；**CLIP+T5 组合 > 单一**；**XL/2→G/2 扩参全指标稳定提升**（49.13→49.99）。

**(2) 与 SOTA 对齐对比（Table 3，T2I-CompBench）**：GenTron-CLIPT5XXL-G/2 在 attribute binding / object relationship / complex 全面领先；**color binding 比前 SOTA（PixArt-α）高 7%+**。综合均分 49.99 vs PixArt-α 48.15 vs SDXL 44.41。

**(3) 与主流 T2I 模型综合对比（Table 4）：**

| 方法 | #Param | FID-30K↓ | CLIP-Score↑ | T2I-CompBench↑ |
|---|---|---|---|---|
| SD v1.4 | 0.9B | 12.94 | 0.325 | 31.50 |
| SDXL | 2.6B | 17.82 | 0.329 | 44.41 |
| **GenTron-XL/2** | 0.9B | 14.21 | 0.326 | 49.13 |
| **GenTron-G/2** | 3.1B | 14.53 | **0.335** | **49.99** |

注：GenTron 的 FID-30K 略逊 SD v1.4（论文引用 Pick-a-Pic、SDXL 的观点，称 FID 常与人类审美偏好不符甚至负相关，故不应作为唯一标准）；但 **CLIP-Score 与 T2I-CompBench 全面领先**，且只用约 550M 数据（vs SD v1.4 的 2B）。

**(4) 人类盲评 vs SDXL（图 7，共 3000 份回答，PartiPrompt2 标准 prompt 各生成 100 图）：**
- **视觉质量**：胜 **51.1%** / 平 19.8% / 负 **29.1%**（三者和 100%）。
- **文本一致性（text faithfulness）**：胜 **42.3%** / 平 42.9% / 负 **14.8%**（三者和 100%）。

**(5) 视频 MFG 消融（图 8）**：带 MFG 的 GenTron-T2V 在视觉质量上明显优于不带——更聚焦 prompt 中的主体、把主体放在更显眼中心位置、细节更足。视频侧**未报告 VBench 等量化指标**（2023 末 VBench 尚未成体系），仅有定性与 MFG 内部对比。

## 创新点与影响
**核心贡献：**
1. **系统化把 DiT 从类条件迁到自由文本条件**：用扎实消融证明 cross-attention（保留 adaLN 处理 time）远优于纯 adaLN，且 CLIP-L+T5-XXL 的 interleaved cross-attention 组合最佳——为后续 Transformer-based T2I 的条件设计提供了清晰的实证依据。
2. **扩散 Transformer 的可扩展性实证**：把 DiT 从 ~900M 扩到 3B+（GenTron-G/2，当时最大的 transformer 扩散架构），验证扩参带来稳定质量提升。
3. **首个纯 Transformer 文生视频扩散** + **motion-free guidance（MFG）**：把"运动"当作可独立 guidance 的条件信号，配合联合图-视频训练，缓解视频微调导致的逐帧画质退化。

**影响**：与同期 PixArt-α 一道，是把 [[dit-scalable-diffusion-transformers]] 推向工业级文生图/视频的关键过渡性工作，为 2024 年 MMDiT（SD3）、纯 DiT 视频（如 Sora 路线公开后的大量复现）奠定了"Transformer 可替代 U-Net 且更可扩展"的认知。MFG 的"把某条件 mask 成恒等以做 CFG"思路也被后续视频/可控生成借鉴。

**已知局限：**
- FID-30K 不及 SD v1.4（作者归因于 FID 与审美偏好脱节，但仍是事实）。
- 视频侧缺乏量化 benchmark（仅人评/定性），评估强度弱于图像侧。
- **闭源**：用 Meta 内部数据、无开源代码与权重；数据来源/清洗/re-caption、算力规模、推理加速等工程细节均未公开，复现门槛高。
- 仍是标准 DDPM ε-prediction，未涉及 flow matching / 步数蒸馏等后续加速范式。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2312.04557
- arxiv_pdf: https://arxiv.org/pdf/2312.04557
- project_page: https://www.shoufachen.com/gentron_website/

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2312.04557.pdf
- ../../../sources/omni/2023/gentron--project-page.md
