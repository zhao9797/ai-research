---
title: "HART: Efficient Visual Generation with Hybrid Autoregressive Transformer"
org: "MIT / NVIDIA / Tsinghua"
country: US
date: "2024-10"
type: paper
category: method
tags: [autoregressive, visual-tokenizer, residual-diffusion, var, t2i, efficient-inference, 1024px]
url: "https://arxiv.org/abs/2410.10812"
arxiv: "https://arxiv.org/abs/2410.10812"
pdf_url: "https://arxiv.org/pdf/2410.10812"
github_url: "https://github.com/mit-han-lab/hart"
hf_url: "https://huggingface.co/mit-han-lab/hart-0.7b-1024px"
modelscope_url: ""
project_url: "https://hanlab.mit.edu/projects/hart"
downloaded: [arxiv-2410.10812.pdf, hart-hybrid-ar--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
HART 用「混合 tokenizer + 残差扩散」把连续 latent 拆成「离散 token（大结构）+ 连续残差 token（细节）」，前者由可变分辨率的下一尺度自回归 transformer 建模、后者由仅 37M 参数 8 步的轻量残差扩散 MLP 补全，是**能直接生成 1024×1024 图像、质量逼平扩散模型的（早期）自回归模型**（论文自述 "early autoregressive model"，非"首个"——同期 Lumina-mGPT 亦做 1024px AR，HART 主打效率优势）：相对 VAR 把 1024px 重建 FID 从 2.11 砍到 0.30、生成 FID 从 7.85 降到 5.38（-31%），并比 SOTA 扩散模型快 3.1–5.9× 延迟、4.5–7.7× 吞吐、省 6.9–13.4× MACs（A100）。

## 背景与定位
视觉生成两大主流：扩散模型（[[ddpm]] [[latent-diffusion-ldm]] / DiT / [[stable-diffusion-3]]）质量高但推理贵（DiT-XL/2 用 DPM-Solver 仍需 20 步、1024px 下 86.2T MACs）；自回归（AR）模型借 LLM 范式（VQGAN→[[var]] / LlamaGen / Emu3 / Show-o）推理可并行更省算力（VAR 同分辨率仅 10.1T MACs，省 8.5×），但落后扩散两点：

1. **离散 tokenizer 重建上限低**——有限 VQ 码本难以还原人脸等高频细节，直接锁死了生成质量天花板；
2. **没有 AR 模型能高效直接产出 1024px**——以往要么靠超分（Parti/RQ-style），要么 one-token-per-step（Lumina-mGPT），代价高。

HART 的核心定位是**弥合 AR 与扩散的质量差，同时保住 AR 的效率**。它直接建在 [[var]]（next-scale prediction）之上，把 VAR 的「纯离散」改造成「离散主干 + 连续残差」的混合表示。与同期混合工作相比：MAR（Li et al. 2024b）用 AR 先验给扩散 MLP 当条件、但建模**全量**连续 token 且无离散码本、无 KV cache（基于 MaskGIT）；HART 只让扩散建模**残差**、AR 主干同时产离散 token 与扩散条件，因此残差远比全量 token 好学（8 步 vs MAR 的 30–50 步）。与 Transfusion / DART / LaVIT / SEED-X（用完整 1B/20 步扩散）相比，HART 用 37M/8 步的「微型」扩散 MLP 取得显著效率优势。

## 模型架构
HART = **混合 tokenizer** + **混合 transformer（可变分辨率 AR + 残差扩散）** 两大件，统一在一个 transformer 里同时建模离散与连续 token。

**1) 混合 tokenizer（Hybrid Visual Tokenization）**
- CNN 视觉编码器把图像编成连续 latent，再按 [[var]] 做多尺度向量量化得到离散 token；
- 累加后的离散特征与原连续特征之差 = **残差 token**（VQ 码本表达不了的部分），交给残差扩散建模；
- 训练时**解码器同时学会解离散与连续两条路**（见「训练方法」的交替训练），推理时只解连续 token = 离散 token 之和 + 残差 token；
- 直觉（Fig 3）：离散 token 抓整体结构，残差 token 补细节（眼睛、眉毛、头发等高频）。

**2) 可变分辨率自回归 transformer（Scalable-Resolution AR Transformer）**
- 在 [[var]] 基础上扩到 T2I，并把 VAR 单个 class token 换成**文本 token 序列**，文本 token 对所有视觉 token 可见（concat 而非 cross-attention，比 STAR 的 cross-attn 方案省 25% 参数）；
- 用 Llama 风格 block 替换 VAR 的 attention/FFN；
- **关键：把 VAR 所有绝对位置编码换成可插值的相对编码**——step embedding（标识 token 属哪个分辨率尺度）用 sinusoidal（天然适配 256/512px 用 10 步、1024px 用 14 步的可变步数）；token index embedding 用混合方案：文本 token 用 1D RoPE、视觉 token 用 2D RoPE，视觉 token 位置索引直接接在文本 token 之后。这套相对编码让从低分辨率 checkpoint finetune 到高分辨率时收敛**显著加快**（Fig 8）。

**3) 残差扩散（Residual Diffusion）**
- 仅 **37M 参数的轻量 MLP**（非完整 DiT），条件来自 AR transformer 最后一层 hidden state + 上一 VAR 采样步预测的离散 token；
- 训练用 1000 步噪声调度，但推理仅需 **8 步**即达最优质量（MAR 需 30–50 步），扩散模块开销因此降低 4–6×；
- 这是与 MAR 的本质区别：MAR 建模全量连续 token、且其 AR transformer 只产扩散条件无离散码本、无 KV cache；HART 的 AR 主干两者都产，残差只需补细节，负担小很多。

**参数规模**：class-conditioned 版按 VAR 设 600M / 1B / 2B（即 HART-d20 ≈ 649M、d24 ≈ 1.0B、d30 ≈ 2.0B AR 参数），均外加 37M 扩散 MLP。T2I 版从 1B 起步、**移除所有 AdaLN 层（省 30% 参数）→ 732M（README 标 0.7B）**；文本编码器用 Qwen2-1.5B（论文）/ 仓库放出的是 Qwen2-VL-1.5B-Instruct，并按 LI-DiT 做 prompt 重格式化。**单一模型直接生成 1024px，无需超分级联。**

## 数据
- **Tokenizer 训练**：OpenImages（Kuznetsova et al. 2020）。
- **HART transformer 训练**：ImageNet（class-conditioned）+ JourneyDB（Pan et al. 2023）+ **内部 MidJourney 风格合成数据**（T2I）。
- **Re-captioning**：所有 T2I 训练数据用 **VILA1.5-13B** 重新生成 caption（图文对齐增强）。
- 具体图文对数量、配比、清洗/美学/安全过滤策略：**未披露**（论文未给规模与配比细节，仅列出数据源）。

## 训练方法
**混合 tokenizer——交替训练（Alternating Training，全文最关键的训练 trick）**
- 编码器、量化器（码本）、解码器均从预训练的**离散 VAR tokenizer** 初始化；
- **冻结编码器与量化器，只训解码器**；
- 每步以 **50% / 50%** 概率随机选「喂离散 token」或「喂连续 token」给解码器重建图像：连续路绕过 VQ 量化器（退化成普通连续 autoencoder），离散路即标准 VQ tokenizer；
- 效果：HART tokenizer 的连续 rFID 逼平 SDXL tokenizer、离散 rFID 保持原 VQ 水平——**生成上限被抬到扩散模型档位**；同时连续/离散 latent 从解码器视角足够相似，使残差更易建模。
- 消融（Fig 7 中/右）证明：交替训练的单解码器虽与「双解码器（离散解码器冻结）」方案 rFID 相近，但生成收敛**更快更好**（24000 步时 FID 5.30 vs 21.98）；「从连续 tokenizer 整体 finetune」或「训练时只解连续 latent」都和双解码器一样差。**低 rFID ≠ 高生成 FID，交替训练才是关键。**

**AR transformer**：next-scale prediction（沿 VAR），从低分辨率预训练 checkpoint finetune 到高分辨率（靠上述相对位置编码做分辨率插值，缓解 1024px 下 O(n⁴) 训练成本——分辨率翻倍 token 数 ×4、注意力计算 ×16）。

**残差扩散**：标准 diffusion 目标拟合残差 token，1000 步噪声调度训练。

**训练加速 trick**：发现 AR 注意力呈「sink + local」局部模式（见 Infra），故训练时在最后一个尺度**随机丢弃约 80% token、只对子采样 token 施加监督**，不掉点；512px 加速 1.4×、1024px 加速 1.9×，显存降 1.1×。

未披露：优化器/学习率/batch size/总训练步数/各阶段时长等具体超参。

## Infra（训练 / 推理工程）
- **算力**：NVIDIA 捐赠的 DGX 服务器；论文未披露 GPU 数量与总 GPU·时。所有质量/效率指标在 **A100** 上测（latency/throughput 用 batch=8）。
- **注意力模式分析（附录 A.1，工程价值高）**：可视化预训练 VAR 注意力发现「**sink + local**」结构——每个尺度的注意力集中在「当前尺度 + 前一尺度 + 最初三个尺度」（类似 StreamingLLM 的 attention sink）；且在最后一个尺度内部，注意力高度**局部化**（每 token 主要看相邻 token，近似卷积）。这解释了为何训练时丢 80% token 不掉点（全局交互本就少），也证明显式把注意力限制到「前 3 尺度 + 2 个局部尺度」不影响结果——为未来用稀疏注意力 kernel 进一步加速训练留了口子。
- **推理 kernel 融合**：相对位置编码引入多个 memory-bound GPU kernel 调用（VAR 的绝对编码只需一次），HART 把它们融成两个 kernel（一个算 sinusoidal、一个算 rotary），端到端提速 7%；再把 RMSNorm 所有算子融成单 kernel，总运行时提速 10%。
- **推理特性**：AR 主干支持 **KV caching**（MAR 因基于 MaskGIT 不支持），残差扩散仅 8 步。论文给出的总体开销结论是「**5% 参数 / 约 10% 运行时**」（正文 §3.2）；class-conditioned ImageNet 上更大模型（d≥24）残差扩散开销仅占总运行时 4–11%（Table 4 脚注）。
- **部署**：开源推理代码 + Gradio demo（hart.mit.edu），demo 用 Google ShieldGemma-2B 做不安全 prompt 过滤。**训练代码未开源**（仅放出推理与 0.7b-1024px checkpoint）。

## 评测 benchmark（把效果讲清楚）

**Tokenizer 重建（rFID↓，Table 1，越低越好；ImageNet/MJHQ-30K 均为训练未见数据集）**

| Tokenizer | MJHQ 256 | MJHQ 512 | MJHQ 1024 | ImageNet 256 | ImageNet 512 |
|---|---|---|---|---|---|
| VAR（纯离散） | 1.42 | 1.19 | 2.11 | 0.92 | 0.58 |
| SDXL（连续） | 1.08 | 0.54 | 0.27 | 0.69 | 0.28 |
| HART（纯离散版） | 1.70 | 1.64 | 1.09 | 1.04 | 0.89 |
| **HART（混合）** | **0.78** | **0.67** | **0.30** | **0.41** | **0.33** |

→ 1024px rFID 2.11→0.30，逼平 SDXL（0.27），生成上限抬到扩散档。

**T2I 主结果（Table 2，MJHQ-30K / GenEval / DPG-Bench）**

| 模型 | 类型 | #Params | 分辨率 | FID↓ | CLIP↑ | GenEval↑ | DPG↑ |
|---|---|---|---|---|---|---|---|
| SD-XL | Diff | 2.6B | 1024 | 8.76 | 28.60 | 0.55 | 74.65 |
| PixArt-Σ | Diff | 630M | 1024 | 6.34 | 27.62 | 0.52 | 79.46 |
| Playground v2.5 | Diff | 2B | 1024 | 6.84 | 29.39 | 0.56 | 76.75 |
| SD3-medium | Diff | 2B | 1024 | 11.92 | 27.83 | **0.62** | **85.80** |
| Show-o | AR | 1.3B | 256 | 14.99 | 27.02 | 0.53 | 67.48 |
| **HART** | AR | **732M** | 512 | **5.22** | **29.01** | 0.56 | 80.72 |
| **HART** | AR | **732M** | 1024 | **5.38** | **29.09** | 0.56 | 80.89 |

→ HART 的 MJHQ-30K FID（5.38）**优于所有列出的扩散模型**；CLIP score（29.09）超过 3.6× 更大的 SD-XL；GenEval / DPG 与 <2B 扩散模型相当（SD3-medium 在 GenEval/DPG 仍领先，但 FID 差很多且慢得多）。

**效率（Table 3，A100，越快越好）**：512px 下 HART（10 步，0.3s 延迟 / 10.6 img·s⁻¹ / 3.2T MACs）相对 SD3-medium 吞吐高 **9.3×**；1024px 下（14 步，0.75s / 2.23 img·s⁻¹ / 12.5T MACs）相对扩散模型延迟低 ≥3.1×。综合：**5.0–9.6× 吞吐 / 4.0–4.7× 延迟（512px）；4.5–7.7× 吞吐 / 3.1–5.9× 延迟（1024px）**，MACs 低 6.9–13.4×。相对同尺寸 PixArt-Σ：延迟快 3.6×、吞吐高 5.6×（贴近理论 5.8× MACs 下降）。

**Class-conditioned（ImageNet 256，Table 4）**

| 模型 | FID↓ | IS↑ | #Params | #Step | MACs | 推理(s, bs=64) |
|---|---|---|---|---|---|---|
| DiT-XL/2 | 2.27 | 278.2 | 675M | 250 | 57.2T | 113 |
| VAR-d30 | 1.92 | 323.1 | 2.0B | 10 | 1.4T | 2.6 |
| MAR-L | 1.78 | 296.0 | 479M | 64 | 16.0T | 34.9 |
| **HART-d20** | 2.39 | 316.4 | 649M | 10 | 579G | 1.5 |
| **HART-d24** | 2.00 | 331.5 | 1.0B | 10 | 858G | 1.9 |
| **HART-d30** | **1.77** | **330.3** | 2.0B | 10 | 1.5T | 2.7 |

→ HART-d30 FID 1.77 优于 MAR-L（1.78）且 **MACs 低 10.7×、运行时快 12.9×**；相对 VAR 全系 FID 改善 4.3–7.8%、IS 稳定提升，仅 4% 运行时开销；比 DiT-XL/2 快 3.3×。

**关键消融**
- **残差扩散有效性（Table 5）**：ImageNet 256 加残差使 FID 改善 10–14%、IS 升至 +6.4%；T2I 上 256px FID +11.1%、512px +17.0%、**1024px +31%**（原 VAR tokenizer 在 1024px 重建差时增益最大）；即便对更强的「HART 纯离散」基线，残差仍带来 6.1% FID 改善。
- **残差扩散效率（Fig 7 左）**：HART 仅 **3 步**扩散即超过 MAR **60 步**的 IS，连续 token 学习运行时降 **20×**——证明残差比全量 token 好学得多。
- **可变分辨率 transformer（Fig 8）**：相对位置编码使高分辨率 finetune 收敛显著加快。

## 创新点与影响
**核心贡献**
1. **混合 tokenizer + 残差分解**：把连续 latent 拆成「离散主干（VQ 可表达）+ 连续残差（VQ 表达不了）」，用极轻量（37M/8 步）残差扩散补残差，**根本性抬高了 AR 模型的重建/生成上限到扩散档**，而非另起炉灶。
2. **交替训练单解码器**：以 50/50 概率同时训练离散/连续解码路径，是「低 rFID 真正转化为高生成质量」的关键，也让残差易学——一个被消融充分验证的非平凡发现。
3. **可变分辨率 AR transformer**：用 sinusoidal step PE + 文本 1D-RoPE / 视觉 2D-RoPE 的相对编码替换 VAR 绝对编码，实现单模型直接 1024px 生成、且支持低→高分辨率快速 finetune，绕开超分/one-token-per-step 的低效路线。
4. **系统级效率**：训练侧 80% token 子采样（基于 sink+local 注意力分析）、推理侧 kernel 融合 + KV cache，把混合架构的额外开销压到 5% 参数 / 约 10% 运行时。

**影响**：HART 是「next-scale AR + 连续残差扩散」混合范式的代表作，证明 AR 路线可在 1024px T2I 上以 <1B 参数、个位数步数逼平甚至超过同期扩散模型的 FID/CLIP，且效率高出近一个数量级；为后续「离散 + 连续混合 token」「AR 主干 + 微型扩散 head」的统一/全模态生成（与 MAR、Transfusion、Show-o 同处一条技术线）提供了高效模板，并把注意力 sink+local 等 LLM 推理优化经验迁移到视觉 AR。

**已知局限**
- GenEval / DPG-Bench 的**组合/语义对齐**仍落后最强扩散（SD3-medium 0.62/85.80 vs HART 0.56/80.89），即「数得清、跟得准」的强语义控制尚有差距。
- **仅开源推理代码与 0.7b-1024px checkpoint，训练代码未放出**；数据规模/配比、训练超参、总算力均未披露，复现训练受限。
- 稀疏注意力 kernel 加速被列为 future work，尚未落地。
- 标题自称「early autoregressive model」，定位为早期探索（preprint, work in progress）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2410.10812
- pdf: https://arxiv.org/pdf/2410.10812
- github: https://github.com/mit-han-lab/hart
- project: https://hanlab.mit.edu/projects/hart
- demo: https://hart.mit.edu
- hf (model): https://huggingface.co/mit-han-lab/hart-0.7b-1024px
- hf (text encoder): https://huggingface.co/mit-han-lab/Qwen2-VL-1.5B-Instruct

## 一手源存档（sources/）
- [arxiv-2410.10812.pdf](https://arxiv.org/pdf/2410.10812)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/hart-hybrid-ar--readme.md)
