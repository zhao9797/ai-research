---
title: "UNO: Less-to-More Generalization — Unlocking More Controllability by In-Context Generation"
org: ByteDance Intelligent Creation
country: China
date: "2025-04"
type: paper
category: edit
tags: [subject-driven, customization, in-context-generation, dit, flux, lora, rope, multi-subject, data-synthesis]
url: https://arxiv.org/abs/2504.02160
arxiv: https://arxiv.org/abs/2504.02160
pdf_url: https://arxiv.org/pdf/2504.02160
github_url: https://github.com/bytedance/UNO
hf_url: https://huggingface.co/bytedance-research/UNO
modelscope_url: ""
project_url: https://bytedance.github.io/UNO/
downloaded: [arxiv-2504.02160.pdf, arxiv-2504.02160.txt, uno--readme.md, uno--hf-model-card.md, uno-1m--hf-dataset-card.md, uno--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
UNO 是字节跳动 Intelligent Creation 团队提出的「单主体→多主体」统一的 subject-to-image（主体驱动）定制生成模型：它从 T2I 的 [[flux-1]] (FLUX.1-dev) DiT 出发，用一条「模型-数据协同进化」(model-data co-evolution) 的高一致性合成数据流水线把模型迭代训练成 S2I 模型，核心创新是**渐进式跨模态对齐 (progressive cross-modal alignment)** + **通用旋转位置编码 UnoPE**。在 DreamBench 单主体上以零样本拿到 **DINO 0.760 / CLIP-I 0.835** 的最高分，是 2025 年被广泛采用的开源 subject-driven 基线（ICCV 2025 接收）。

## 背景与定位
主体驱动生成（给定一张/多张参考主体图，按文本生成包含该主体的新图）长期受两个瓶颈制约：
1. **数据可扩展性**：从单主体配对数据扩到多主体配对数据并放大规模极难——真实多主体配对图几乎无法采集，合成数据又常分辨率低（≤512×512）、域窄。
2. **主体可扩展性**：多数方法只针对单主体设计，难迁移到多主体场景。

早期 per-subject 微调流派（[[dreambooth]]、Textual Inversion、LoRA）需对每个新主体逐一微调，推理慢、不可部署；后续大数据训练流派（IP-Adapter、BLIP-Diffusion）用额外 image encoder 注入参考图，实现免微调实时定制，但受限于训练数据，常在「主体相似度 vs 文本可控性」间权衡或生成不稳定。

UNO 的关键洞察借鉴 LLM 的「合成数据自我增强」：弱（less-controllable）的前代模型可以系统性合成更好的定制数据，去训练出更强（more-controllable）的后代模型，形成模型与数据的持续协同进化。技术上它沿着 DiT in-context 生成这条线（[[in-context-lora]]、OminiControl 已证明 DiT 自身可作 image encoder / 参考图引擎），把单主体扩展到多主体，并以最小架构改动保留 DiT 的可扩展性。相关前置工作：[[latent-diffusion-ldm]]、[[dit-scalable-diffusion-transformers]]、[[stable-diffusion-3]](MM-DiT)、[[flux-1]]。

## 模型架构
- **Backbone**：基于 MM-DiT 的 **FLUX.1-dev**（[[flux-1]]）。MM-DiT 把文本 token 与图像 token 拼接后做多模态注意力（Q/K/V 在全部 token 上计算 attention，Z=[z_t, c]），文本与图像各自在自己空间内表达又互相感知。
- **Text encoder**：T5（FLUX 原生），训练中冻结；推理代码另需 CLIP-ViT-L/14（来自 FLUX 文本侧）。
- **Tokenizer / VAE**：沿用 FLUX 的 VAE，目标图 I_tgt 由 VAE 编码为 noisy latent z_t；参考图 I_ref^i 同样过 VAE 编码为 z_ref^i。
- **条件注入（核心）**：UNO 不引入额外 image encoder 或 adapter，而是**把参考图的 VAE latent 直接拼到 DiT 输入序列里**，复用 DiT 的 in-context 注意力做条件感知。
  - Stage I（单主体）：`z1 = Concat(c, z_t, E(I_ref^1))`
  - Stage II（多主体）：`z2 = Concat(c, z_t, z_ref^1, z_ref^2, …, z_ref^N)`，论文中 N=2（但合成数据里偶有 >2 参考图，赋予了更多主体的泛化）。
- **UnoPE（通用旋转位置编码，关键架构设计）**：FLUX 用 RoPE，给文本 token 固定位置 (0,0)，给 noisy 图像 token 分配 (i,j)，i∈[0,w−1], j∈[0,h−1]。UNO 给新引入的参考图 token 复用同一编码格式以继承隐式位置对应，但**从 noisy 图像 token 的最大宽高处沿对角线起始**偏移：第 N 个参考 latent 的位置索引为 `(i', j') = (i + w·(N−1), j + h·(N−1))`。这一对角线偏移既避免参考图过度「拷贝」其原始空间结构，又让模型在多参考图存在语义间隔时**从文本而非参考图布局里获取 layout 信息**，从而缓解多主体放大时的「属性混淆 (attribute confusion)」。消融显示这是 UNO 的关键涨点项（见下文）。
- **参数化**：UNO 不全参微调 FLUX，而是用 **LoRA（rank=512）** 训练；架构改动「最小且有效」，保留 base 模型可扩展性。
- **分辨率策略**：单主体推理参考图最长边默认 512，多主体场景 320；训练在 512 bucket 内但多尺度，推理可外推到 512/568/704 等多种分辨率与宽高比。

## 数据
UNO 的核心贡献之一就是**合成数据流水线**与公开的 **UNO-1M** 数据集（~1M 配对图，已开源于 HF）。

- **Taxonomy Tree（分类树）**：以 Object365 的 **365 个通用类**为根，再用 LLM 按年龄/职业/着装等细粒度扩展出大量 subject 实例与场景描述（creative / realistic / text-decorated 三种风格 system prompt 生成 subject，另用 system prompt 按 subject 生成每个 8 条场景描述）。配合预定义 diptych 文本模板，得到数百万条 T2I prompt。
- **单主体 in-context 生成**：用 FLUX.1 的 in-context 能力 + diptych（双联画）模板，让模型一次生成左右（或上下）两格、含同一 subject1 的一致图对，并**直接产出三种高分辨率**：1024×1024、1024×768、768×1024（区别于 OminiControl 只产 512×512 单主体数据）。生成后用 Hough Transform 切成参考图 I_ref^1 与目标图 I_tgt。
- **多主体 in-context 生成**：用上一阶段训出的 S2I 模型反过来造多主体数据——先用开放词表检测器 (OVD) 在 I_tgt 里检出 subject2 并裁剪，再把裁剪图 + subject prompt 喂给 S2I 模型**重新生成**一张同主体但换场景的 I_ref^2（而非直接用裁剪图），以规避「copy-paste」问题（直接用裁剪图会让模型不读文本、只粘贴主体）。
- **多阶段过滤（关键）**：① 先用 **DINOv2** 算参考图与目标图余弦相似度，阈值滤掉一致性显著偏低的对；② 再用 **VLM + 三轮 CoT** 打分（按 appearance / details / attributes 等自动维度逐部件 0–4 评分取均值）。论文训练**只保留满分（score=4）数据**；HF 数据卡建议一般使用取 score_final ≥ 3.5。统计显示 CoT 过滤后约 **35.43% 数据被保留**（VLM 分布：[4.0]=35.43%、[3.5,4.0)=12.66%、[3.0,3.5)=23.51%、[2.5,3.0)=13.02%、[2.0,2.5)=8.67%）。
- **训练实际用量**：Stage I 用 **230k** 单主体对，Stage II 用 **15k** 多主体对（均由上述流水线合成）。
- **UNO-1M 数据集**：~1M 配对图，>365 类，~1024×1024 可变分辨率，附逐部件 consistency 分解分与最终一致性分；官方标注其可用于 T2I、subject-driven、scored-filter 训练，乃至**一致性 reward model 训练**。
- 数据来源说明：绝大多数图为生成或授权图。许可分层：**代码 Apache 2.0**；**模型权重 CC BY-NC 4.0**（且 FLUX.1-dev 衍生须遵循其原始许可）；UNO-1M 数据集卡标注 `license: apache-2.0`。

## 训练方法
- **训练目标**：沿用 FLUX 的扩散/rectified-flow 去噪目标（论文未单独改写损失，VAE 编码目标图加噪后由 DiT 去噪），方法重心在条件注入与位置编码而非损失函数。
- **渐进式跨模态对齐 (progressive cross-modal alignment，两阶段)**：直接把多张参考图塞进 DiT 会破坏原模型的收敛分布、导致训练不稳/次优，故采用「简单到困难」的渐进策略——
  - **Stage I**：用单主体配对数据，把预训练 T2I 微调成能读单参考图+文本的 S2I 模型（cross-modal alignment 初始阶段）；
  - **Stage II**：在多主体配对数据上继续训练，让模型读多张参考图并把信息注入各自 latent 空间。
  - 这一渐进训练「解锁」了 T2I 模型固有的 in-context 生成能力。消融表明：跳过渐进对齐直接喂多图会让 DINO/CLIP-I 显著掉点；且渐进对齐反而**抬高了单主体场景的上限**（同样步数下 DINO 0.730→0.760、CLIP-I 0.821→0.835）。
- **超参 / trick**：
  - 学习率 1e-5，total batch size 16；
  - Stage I 训 **5,000 步**，Stage II 再训 **5,000 步**；
  - 全程 **LoRA rank=512**（rank 消融：4→512 持续涨点，到 128 后趋缓，最终取 512 平衡性能与资源）。
- 未涉及 RLHF/DPO/偏好对齐、未做步数蒸馏（UNO 本身是 LoRA 微调，非加速方法）。

## Infra（训练 / 推理工程）
- **训练算力**：整个实验在 **8× NVIDIA A100** 上完成；两阶段各 5k 步、batch 16、LoRA rank 512。论文未报告精确 GPU·时与吞吐。
- **推理 / 部署**：
  - 开源 Gradio demo + HF Space（UNO-FLUX）；
  - 提供 **fp8 模式 + offload** 的低显存路径，峰值显存约 **16GB**（消费级 GPU 可跑）；在 RTX 3090 上 fp8+offload 端到端推理 **40s–1min**；
  - 全部 checkpoint（含 FLUX.1-dev、文本编码器、CLIP、UNO LoRA）约占 37GB 磁盘。
- 量化/缓存等更深推理优化论文未展开（README 标注「may try further inference optimization later」）。

## 评测 benchmark（把效果讲清楚）
评测指标：DINO、CLIP-I（主体相似度）、CLIP-T（文本一致性）。单主体在 DreamBench（zero-shot），多主体沿用 MIP-Adapter/Subject-Diffusion 协议：DreamBench 中 30 组两两主体组合 × 25 prompt × 6 图 = **4,500 image groups**。

**单主体（DreamBench，Table 1，节选）**
| 方法 | DINO↑ | CLIP-I↑ | CLIP-T↑ |
|---|---|---|---|
| Oracle（参考图） | 0.774 | 0.885 | — |
| DreamBooth | 0.668 | 0.803 | 0.305 |
| RealCustom++ | 0.702 | 0.794 | 0.318 |
| OmniGen | 0.693 | 0.801 | 0.315 |
| OminiControl | 0.684 | 0.799 | 0.312 |
| FLUX.1 IP-Adapter | 0.582 | 0.820 | 0.288 |
| **UNO (Ours)** | **0.760** | **0.835** | 0.304 |

UNO 的 DINO 0.760、CLIP-I 0.835 均为对比方法中最高（zero-shot），逼近 Oracle 上界；CLIP-T 0.304 处于有竞争力区间（部分方法 CLIP-T 略高但主体相似度大幅落后）。

**多主体（Table 2，节选）**
| 方法 | DINO↑ | CLIP-I↑ | CLIP-T↑ |
|---|---|---|---|
| MS-Diffusion | 0.525 | 0.726 | 0.319 |
| MIP-Adapter | 0.482 | 0.726 | 0.311 |
| OmniGen | 0.511 | 0.722 | 0.331 |
| **UNO (Ours)** | **0.542** | **0.733** | 0.322 |

UNO 在多主体上同样拿到最高 DINO / CLIP-I，CLIP-T 有竞争力。

**消融（核心结论）**
- *合成数据 vs 裁剪图*（多主体基准，Table 3）：用 OVD 裁剪图替代生成 I_ref^2 → DINO 0.542→0.529、CLIP-I 0.733→0.730，并出现严重 copy-paste（图上几乎不响应文本）。
- *去掉渐进跨模态对齐*（Table 3）：DINO 掉到 0.511、CLIP-I 0.721。
- *去掉 UnoPE*（直接克隆目标图位置索引，Table 3）：**DINO 暴跌到 0.386、CLIP-I 0.674**——生成图能跟文本但几乎不参考输入图，是掉点最猛的一项。
- *位置偏移形式对比*（Table 5/6，DreamBench / 多主体）：w/o offset（DINO 0.470 / 0.386）、w/ width-offset、w/ height-offset 均不如 UNO 的对角线偏移（DINO 0.730 / 0.542），验证对角线 UnoPE 最优。
- *渐进对齐抬升单图上限*（Table 4）：single-only DINO 0.730 → +cross-modal alignment 0.760。
- *LoRA rank*（附录 Fig.18）：rank 4→512 持续涨点，128 后趋缓，最终选 512。
- **用户研究**：30 名评估者对 300 组（单+多主体）按文本一致性（主体/背景）、主体相似度、构图、视觉吸引力五维排名，UNO 在主体相似度与文本一致性领先，其余维度亦强（雷达图 Fig.8）。

## 创新点与影响
**核心贡献**
1. **模型-数据协同进化范式**：用弱前代模型系统性合成高质量定制数据去训更强后代模型，破解 subject-driven 的数据瓶颈，可持续放大可控性。
2. **高一致性 in-context 合成数据流水线**：diptych 模板 + FLUX in-context 直出三种高分辨率配对图；单主体→多主体渐进合成；DINOv2 粗滤 + VLM 三轮 CoT 细滤；并开源 UNO-1M（~1M 对）。
3. **UNO 架构**：对 DiT 最小改动（LoRA rank 512）即统一单/多主体；**渐进式跨模态对齐**两阶段训练 + **UnoPE 对角线位置偏移**有效缓解多主体属性混淆。

**影响**
- 训练/推理/权重/数据/合成流水线全开源（代码 Apache 2.0、权重 CC BY-NC 4.0），ICCV 2025 接收（2025.06.26 官宣），成为 2025 年被广泛复现/二次开发的开源 subject-driven 基线（README 列出 5 个社区 ComfyUI 节点实现）。
- 衍生出一系列后续工作：RealCustom（伴随项目）、**USO**（任意主体 × 任意风格）、**UMO**（一对多身份 × 任意主体组合，号称更强 UNO/OmniGen2）。
- 「DiT 自身即 image encoder + 拼 latent 做 in-context 条件 + RoPE 位置偏移防 copy-paste」成为后续多参考图定制的通用范式参考。

**已知局限（作者自述）**
- 训练数据以 subject-driven 为主，**编辑(editing)与风格化(stylization)配对数据有限**，泛化受合成数据类型约束；
- 论文 N=2，多于 2 主体主要靠数据随机性带来的泛化；
- 因 FLUX 基座，虚拟试穿/身份保持/风格化等能力多为零样本「涌现」，非专门训练，仍有提升空间。

## 原始链接
- paper (arXiv abs): https://arxiv.org/abs/2504.02160
- pdf: https://arxiv.org/pdf/2504.02160
- github: https://github.com/bytedance/UNO
- hf model: https://huggingface.co/bytedance-research/UNO
- hf dataset (UNO-1M): https://huggingface.co/datasets/bytedance-research/UNO-1M
- hf demo (Space): https://huggingface.co/spaces/bytedance-research/UNO-FLUX
- project page: https://bytedance.github.io/UNO/

## 一手源存档（sources/）
- [arxiv-2504.02160.pdf](https://arxiv.org/pdf/2504.02160)  （arXiv 原文 PDF，不入 git）
- [arxiv-2504.02160.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/arxiv-2504.02160.txt)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/uno--readme.md)
- [hf-model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/uno--hf-model-card.md)
- [uno-1m--hf-dataset-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/uno-1m--hf-dataset-card.md)
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/uno--project-page.md)
