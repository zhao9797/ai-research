---
title: "PixArt-Σ: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation"
org: "Huawei Noah's Ark Lab / HKU / DLUT / HKUST"
country: China
date: "2024-03"
type: paper
category: t2i
tags: [t2i, dit, diffusion-transformer, 4k, kv-compression, weak-to-strong, efficient, pixart]
url: "https://arxiv.org/abs/2403.04692"
arxiv: "https://arxiv.org/abs/2403.04692"
pdf_url: "https://arxiv.org/pdf/2403.04692"
github_url: "https://github.com/PixArt-alpha/PixArt-sigma"
hf_url: "https://huggingface.co/PixArt-alpha/PixArt-Sigma"
modelscope_url: ""
project_url: "https://pixart-alpha.github.io/PixArt-sigma-project/"
downloaded: [arxiv-2403.04692.pdf, pixart-sigma--readme.md, pixart-sigma--hf-1024ms.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
PixArt-Σ 是一个能**直接生成 4K (3840×2160) 分辨率图像**（无需级联超分/后处理）的 Diffusion Transformer (DiT) 文生图模型（摘要原文：「a DiT capable of directly generating images at 4K resolution」，未自称「首个 4K」）；在 [[pixart-alpha]] 预训练底座之上用「弱到强训练 (weak-to-strong training)」+「KV token 压缩」高效升级，仅 **0.6B 参数**（约 SDXL 2.6B 的 1/4、SD Cascade 5.1B 的 ~1/8），在自建 30K 高质量评测集上 FID 8.23、CLIP-Score 0.2797，人评/AI 评偏好显著超过 PixArt-α、SDXL、SD Cascade 等开源模型，且 1K 模型微调仅需 **9% 于 PixArt-α 的 GPU 天**。

## 背景与定位
从头训练一个顶级 T2I 模型代价高昂（SD1.5 从零训练约需 6000 A100 GPU 天），这对个人研究者是巨大壁垒。作者提出一个核心问题：当社区不断有更高质量数据集和更先进算法时，**如何在有限算力内把这些新元素高效注入一个已有模型，得到更强版本**——而不是每次推倒重训。

PixArt-Σ 的答案就是「弱到强训练」：以 [[pixart-alpha]]（首个能生成 1024px 高质量图的 Transformer-based T2I 模型，基于 [[dit-scalable-diffusion-transformers]] 架构）作为「弱」基线，通过引入更高质量数据 + KV 压缩等手段持续微调，演化为「强」模型。技术脉络上它属于 [[dit-scalable-diffusion-transformers]] / [[latent-diffusion-ldm]] 这条 Transformer 扩散主线，与 GenTron、Sora、[[stable-diffusion-3]] 共同验证了 DiT 在 T2I/视频的潜力。相比 [[pixart-alpha]] 的关键改进是：分辨率从 1K 推到 4K，画质与文本对齐显著提升，且首次系统化解决了超高分辨率下长序列 token 带来的计算复杂度问题。

相对前置高分辨率方案：Imagen/GigaGAN/Stable Diffusion 用额外超分网络、Stable Cascade 用多级扩散逐步升分辨率——这些级联方案会累积误差；SDXL/DALL·E 2/Playground/PixArt-α 直接生成但受限于复杂度上限 1024px。PixArt-Σ 把直接生成的边界推到 4K。

## 模型架构
**Backbone：DiT（Diffusion Transformer），沿用 PixArt-α 的网络结构**，主干结构基本不变（README 明确「main model structure is the same as PixArt-α」），核心新增是一个带 **KV token 压缩**的自注意力模块。

- **参数量**：0.6B（checkpoint 命名为 XL-2，沿用 PixArt-α 的 DiT-XL/2 配置；论文正文未给出层数，由消融的层索引区间（浅层 1~14 / 中层 7~20 / 深层 14~27）可推得 28 层 Transformer block）。模型族提供 256/512/1024/2K（论文表述含 4K）多分辨率版本，参数量均为 0.6B（「MS」= multi-scale 多宽高比；已公开发布的 checkpoint 为 256/512/1024/2K，4K 权重未在 HF 列出）。
- **VAE**：由 PixArt-α 的 SD1.5 VAE（ft-ema）**替换为 SDXL VAE**（madebyollin/sdxl-vae-fp16-fix），冻结使用，用于提取潜空间特征。
- **Text encoder**：沿用 Imagen / PixArt-α 的 **Flan-T5-XXL（T5 encoder）**作为文本编码器；不同于多数工作固定取 77 token，PixArt-Σ 把文本 token 长度从 PixArt-α 的 **120 扩展到 300**，以容纳 Internal-Σ 更密集的细粒度描述。T5 + SDXL-VAE 打包权重约 4.5B（diffusers 版 pixart_sigma_sdxlvae_T5_diffusers）。
- **条件注入**：延续 PixArt-α 的 cross-attention 注入文本条件 + AdaLN-single 注入 timestep 条件（PixArt-α 设计，本文未改动，README 称结构一致）。

**KV Token Compression（核心架构创新）**：
- **动机/观察**：把 KV 压缩直接套到预训练好的 PixArt-α 上仍能生成合理图像 → 说明特征存在冗余；相邻 R×R patch 内语义高度相似，窗口内特征可被合理压缩。
- **做法**：在 self-attention 中对 **Key 和 Value 做空间压缩**（压缩算子 f_c），而 **Query 全部保留**（避免信息损失）。注意力复杂度从 O(N²) 降到 O(N²/R²)，N = H×W。公式：Attention(Q,K,V)=softmax(Q·f_c(K)^T/√d_k)·f_c(V)。
- **压缩算子**：用 **stride=2 的 group convolution（"Conv 2×2"）**做局部聚合，把 2×2 token 压成 1 个 token。消融显示 Conv2×2 优于随机丢弃 (Token Discarding) 和平均池化 (Token Pooling)，因为可学习卷积核能更有效去冗余。
- **压缩位置**：只在**深层 (14~27 层)** 做 KV 压缩。消融发现深层压缩损失最小（FID 8.532 vs 浅层 9.278 / 中层 9.063 / 不压缩 8.244），原因是浅层编码细节纹理、深层抽象高层语义，而压缩主要伤画质不伤语义。
- **额外参数**：整套 KV 压缩仅增加 **0.018%** 参数。
- **专门初始化「Conv Avg Init」**：group conv 权重初始化为 w=1/R²（等价平均算子），使新加的压缩层从一开始就能产出粗略合理结果，加速从无压缩模型微调收敛。

## 数据
- **Internal-Σ 主数据集**：内部数据从 PixArt-α 的 **14M（Internal-α）扩展到 33M**。全部 **>1K 分辨率**，其中约 **2.3M 张分辨率约 4K**（即 Tab.1 中的 4K-Σ 子集 2.3M）。以高美学、多艺术风格为主。作者强调这相比 SD1.5 用的 ~2B 数据仍很小，证明「有限数据 + 有效训练策略」也能得到强模型。（论文未披露 Internal-Σ 的具体来源，只称 "sourced from the Internet"。）
- **4K 专用数据**：为支撑 4K 生成，**额外采集 8M 张真实摄影 4K 图**，用美学打分模型 (AES，improved-aesthetic-predictor) 过滤，**精炼出 2M 张超高分辨率高质量图**（论文未说明此 2M 与上面 2.3M 4K-Σ 子集的重叠/包含关系）。
- **Re-captioning（重标注，关键升级）**：把 PixArt-α 用的 **LLaVA 换成更强的 Share-Captioner (ShareGPT4V)**。论文用对比图说明 LLaVA 存在明显幻觉（描述图中不存在的物体/属性），Share-Captioner 标注更长更准。
  - 标注长度大幅提升：Internal-α 的 LLaVA 标注平均 98 词 → Internal-Σ 的 Share-Captioner 平均 **180 词**（ACL=Average Caption Length；同为 Share-Captioner 时 Internal-α ACL 为 184，可见增益主要来自换更强 captioner 而非数据扩量）。
  - 名词多样性提升（Tab.1，均为 Share-Captioner 标注）：Internal-Σ 有效不同名词 (VN，出现>10 次) 77K / 不同名词总数 (DN) 714K / 名词出现总次数 (Total Noun) 1804M / 平均 53.6 名词/图；4K-Σ 子集 VN/DN=24K/96K、ACL 163、49.5 名词/图。
- **长短标注混训**：训练时 **长标注 (Share-Captioner) : 短标注 (raw) = 60% : 40%** 混合，提升文本多样性、缓解纯生成式标注带来的偏置。
- **观察**：随图像分辨率升高，模型 FID 和 CLIP-Score 都改善——说明生成高分辨率本身有助于保真度与语义对齐。
- **高质量评测集（自建）**：作者另建 **30K 高质量、高美学的图文对评测集**，认为 MSCOCO 不足以反映美学与对齐能力，论文除非特别说明均在此集上评测。

## 训练方法
- **训练目标**：论文明确「Other implementation details are the same as PixArt-α」，沿用 PixArt-α 的标准 diffusion 训练范式（DDPM 风格 ε-prediction；本文未引入 flow matching，亦未单独复述训练目标公式——此处训练目标为据 PixArt-α 推得）。
- **从预训练继续微调（weak-to-strong 核心）**：从 PixArt-α 的 **256px 预训练 checkpoint** 出发，用 PE 插值技巧接续，逐步演化。三条关键迁移策略：
  1. **适配新 VAE（SD1.5→SDXL VAE）**：直接换 VAE 后继续微调扩散模型，**约 2K 步即快速收敛**（FID 从换 VAE 初期降到 8.91/CLIP 0.276，仅需极短训练），免去从零重训。
  2. **低分辨率→高分辨率**：换分辨率会因 PE（位置编码）不匹配导致性能退化；用 **"PE Interpolation" 技巧**（把 LR 的 PE 插值初始化 HR 的 PE），**100 步**即可得到可用图、**1K 步**收敛（256→512：1K 步 FID 9.75、100K 步 8.91）。
  3. **无 KV 压缩→有 KV 压缩**：配合 "Conv Avg Init"，**100 步**即出满意结果，最终 KV 压缩使训练/推理时间各减约 **34%**。
- **分阶段训练流程（附录 Tab.5，GPU 天逐阶段）**：
  | 阶段 | 分辨率 | 图量 | 步数 | LR | GPU 天 |
  |---|---|---|---|---|---|
  | VAE 适配 | 256² | 33M | 8K | 2e-5 | 5 V100 |
  | 文本-图对齐 | 256² | 33M | 80K | 2e-5 | 50 V100 |
  | 高美学 | 512² | 18M | 10K | 2e-5 | 30 V100 |
  | 高美学 | 1024² | 18M | 5K | 1e-5 | 50 V100 |
  | + KV 压缩 | 1024² | 18M | 5K | 1e-5 | **20 V100** |
  | 高美学 / +KV | 2K² | — | 300K | 2e-5 | 20→**14** A800 |
  | 高美学 / +KV | 4K² | — | 100K | 2e-5 | 25→**20** A800 |
  - KV 压缩显著省时：1024px 从 50→20 V100 天；2K 从 20→14、4K 从 25→20 A800 天。
- **优化器（关键 trick）**：用 **CAME 优化器**（Confidence-guided Adaptive Memory efficient，ACL 2023）而非常规 AdamW，weight decay=0，constant LR=2e-5。CAME 减小优化器状态维度，**降显存且不掉点**。
- **特征离线预提取**：VAE 特征和 T5 文本特征均离线提前算好，不计入训练 GPU 天（也是高效的工程手段）。
- **蒸馏/加速（附录扩展 + 代码）**：集成 **DMD (Distribution Matching Distillation)** 训练一步生成器 Gθ。关键发现：DMD 起始 timestep **T 的最佳值是 400 而非 999**（T 太小会偏离基模训练分布，存在权衡）。仓库还放出 PixArt-α-DMD 一步采样 checkpoint（512px）、LoRA/DoRA 训练代码。

## Infra（训练 / 推理工程）
- **算力规模**：最终模型（含 1K 分辨率）在 **32× V100** 上训练；2K/4K 模型额外用 **16× A100** 训练（附录用 A800 计 GPU 天）。整体训练成本极省——1K 高分辨率模型微调**只用 PixArt-α 9% 的 GPU 天**。
- **注意力实现**：KV 压缩注意力用 **xformers 的 memory_efficient_attention** 实现（附录伪代码 Algorithm 1），group conv 做 KV 下采样。
- **推理加速实测（Tab.3d，KV 压缩 ratio=4 vs 1）**：
  - 2K：训练 56→37 s/iter (-34%)，推理 58→38 s/img (-34%)
  - 4K：训练 191→125 s/iter (-35%)，推理 91→60 s/img (-34%)
  - 训练加速随分辨率升高而增大（1K 时 18%，4K 时 35%）。
- **一步推理 (DMD)**：512px 单步 0.11s（teacher 20 步 1.44s），见下表。
- **部署形态**：开源 PyTorch 权重（.pth + diffusers 版），HF 提供 256/512/1024/2K 多档 checkpoint；已并入官方 **🧨 diffusers (PixArtSigmaPipeline)**；提供 Gradio demo、HF Space 在线 demo、CPU offload 内存优化；License **openrail++**。

## 评测 benchmark（把效果讲清楚）
**FID / CLIP-Score（自建 30K High-Quality Eval 集，Tab.6）**：
| 模型 | #Params(B) | FID↓ | CLIP-Score↑ |
|---|---|---|---|
| Stable 1.5 | 0.9 | 17.03 | 0.2748 |
| Stable Turbo | 3.1 | 10.91 | 0.2804 |
| Stable XL (SDXL) | 2.6 | 7.38 | 0.2913 |
| Stable Cascade | 5.1 | 9.96 | 0.2839 |
| Playground-V2.0 | 2.6 | 8.68 | 0.2885 |
| Playground-V2.5 | 2.6 | 7.64 | 0.2871 |
| **PixArt-α** | 0.6 | 8.65 | 0.2787 |
| **PixArt-Σ** | **0.6** | **8.23** | **0.2797** |
- PixArt-Σ 以最小参数量 (0.6B) 取得 FID 8.23，优于 PixArt-α (8.65)，与 SDXL/Playground 等大模型相当或更好。注意 CLIP-Score 上 SDXL (0.2913) 仍最高，作者主打的是人评/AI 评偏好而非 FID/CLIP（认为后者不足以反映生成质量与美学）。

**人评 / AI(GPT-4V) 偏好研究（Fig.9）**：随机取 300 条 prompt，对比 PixArt-α、PixArt-Σ、SD1.5、Stable Turbo、SDXL、SD Cascade、Playground-V2.0 共 6 个开源模型。结论：人评（蓝条）显著偏好 PixArt-Σ；用 GPT-4V 作自动评委（橙/绿条）结论一致——PixArt-Σ 在画质与指令遵循上超越 PixArt-α，相比 Stable Cascade 等先进模型竞争力相当或更优。（论文以柱状图呈现，未给出具体偏好百分比数字。）

**一步蒸馏对比 PixArt+DMD vs PixArt+LCM（Tab.4，512×512，bs=1）**：
| 方法 | FID↓ | CLIP↑ | Speed↓ |
|---|---|---|---|
| PixArt+LCM (1 step) | 108.66 | 0.2247 | 0.11s |
| PixArt+LCM (2 step) | 17.95 | 0.2736 | 0.16s |
| PixArt+LCM (4 step) | 13.06 | 0.2797 | 0.26s |
| **PixArt+DMD (1 step)** | **13.35** | **0.2788** | **0.11s** |
| Teacher (20 steps) | 9.273 | 0.2863 | 1.44s |
- DMD 单步即逼近 LCM 4 步质量（FID 13.35 vs 13.06），但速度快一倍（0.11s vs 0.26s）；LCM 单步崩坏 (FID 108)。

**KV 压缩消融（Tab.3）**：
- 压缩层位置：深层最优（FID 8.532，不压缩基线 8.244）。
- 压缩算子：Conv2×2 (8.505) > Token Discarding (8.918) > Token Pooling (9.415)。
- 压缩比 vs 分辨率（512/1024/2K/4K，ratio 1/2/4/9）：CLIP-Score 几乎不变（压缩不伤文本对齐），FID 随压缩比略升（伤画质）；换来 18%~35% 训练提速，分辨率越高加速越明显。
- 与 4 个闭源产品（Adobe Firefly 2、Google Imagen 2、OpenAI DALL·E 3、Midjourney V6）定性对比（Fig.4/14/15），作者称 PixArt-Σ 生成质量「very competitive」，但仅定性图示对比，无量化分数。

**VAE 适配快收敛（Tab.2）**：256→512，1K 步 FID 9.75、100K 步 8.91，证明换 VAE 后短训练即可恢复高质量。

## 创新点与影响
**核心贡献**：
1. **「弱到强训练」范式**：系统化论证如何用极小算力（仅 PixArt-α 9% GPU 天）把已有模型升级为更强模型——通过换 VAE、PE 插值升分辨率、Conv Avg Init 接入 KV 压缩三套快速适配策略，各只需 100~2K 步即收敛。为「复用已有底座持续迭代」提供了可复制的工程方法论。
2. **KV Token Compression**：首个面向 DiT 高分辨率 T2I 的高效注意力设计，仅 +0.018% 参数把复杂度从 O(N²) 降到 O(N²/R²)，训练/推理省约 34%，且基本不伤画质与对齐——使 Transformer **直接生成 4K** 图像在可控成本内成为可能。
3. **极致参数/数据效率**：0.6B 参数 + 33M 内部数据，画质对标 SDXL(2.6B)/SD Cascade(5.1B) 及 DALL·E 3/MJ V6 级商业产品，是「小而强」高效 DiT T2I 的代表作。
4. **数据侧贡献**：Share-Captioner 重标注（治幻觉、标注 98→180 词）、长短标注 6:4 混训、T5 token 120→300、自建 30K 高美学评测集——这些数据工程经验被后续大量 T2I 工作借鉴。

**影响**：作为 PixArt 系列（α→[[pixart-delta]]→Σ）的高分辨率里程碑，与 GenTron、Sora、[[stable-diffusion-3]] 一同强化了 DiT 作为 T2I/视频主流架构的地位；KV 压缩思路（源自 PVT v2）为后续超高分辨率扩散注意力优化提供范例；其「弱到强 + 高质量再标注」配方成为低成本训练高质量 T2I 的常见 playbook。已并入 HuggingFace diffusers 主线，社区生态（LoRA/DoRA、DMD 一步、ControlNet 规划中）活跃。

**已知局限（论文 A.10）**：仍不擅长生成**文字和手部**；复杂 prompt 无法完全对齐；人脸生成可能有瑕疵；可能生成敏感内容。作者建议后续聚焦更高质量数据构建、扩大模型规模、用 super alignment 改善幻觉与安全。社会影响上 T2I 模型可能放大刻板印象/群体歧视，需谨慎数据采集缓解。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2403.04692
- arxiv_pdf: https://arxiv.org/pdf/2403.04692
- github: https://github.com/PixArt-alpha/PixArt-sigma
- project_page: https://pixart-alpha.github.io/PixArt-sigma-project/
- hf_models: https://huggingface.co/PixArt-alpha/PixArt-Sigma
- hf_1024ms: https://huggingface.co/PixArt-alpha/PixArt-Sigma-XL-2-1024-MS
- hf_demo_space: https://huggingface.co/spaces/PixArt-alpha/PixArt-Sigma
- toy_dataset: https://huggingface.co/datasets/PixArt-alpha/pixart-sigma-toy-dataset

## 一手源存档（sources/）
- [arxiv-2403.04692.pdf](https://arxiv.org/pdf/2403.04692)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/pixart-sigma--readme.md)
- [hf-1024ms.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/pixart-sigma--hf-1024ms.md)
