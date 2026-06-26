---
title: "StyleDrop: Text-to-Image Generation in Any Style"
org: Google Research
country: US
date: "2023-06"
type: paper
category: edit
tags: [style-tuning, personalization, few-shot, adapter, peft, muse, masked-transformer, t2i, feedback]
url: "https://arxiv.org/abs/2306.00983"
arxiv: "https://arxiv.org/abs/2306.00983"
pdf_url: "https://arxiv.org/pdf/2306.00983"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://styledrop.github.io/"
downloaded: [styledrop--ar5iv.md, styledrop--project-page.md, arxiv-2306.00983.pdf]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
StyleDrop 是 Google Research 2023 年提出的「单图学风格」方法：在 [[muse]]（基于 MaskGIT 的离散 token 文生图 Transformer）上做 **adapter 微调**（可训练参数 < 1% 总参数，最小仅 0.23M），用**一张**风格参考图就能让模型在任意文本提示下稳定复现该风格，并通过「带反馈的迭代训练」抑制内容泄漏。在 6 个风格、190 个 Parti prompt 上，StyleDrop(HF) 的 CLIP Style score 达 **0.694**（vs Muse 基线 0.556、Imagen 上 DreamBooth 的 0.644），用户研究中风格一致性偏好高达 **86%** 压过 Imagen 上的 DreamBooth。

## 背景与定位
文生图模型能画很多「热门风格」（anime、steampunk、梵高），但大量细腻风格（配色、光照、笔触、设计图案）**难以用文字描述**，且「梵高」这种词会随机命中某一种风格或混搭多种风格，不可控。已有的个性化方法各有短板：

- **[[textual-inversion]]**（Textual Inversion）：只学一个文本 embedding，不改模型参数，风格保真度有限；
- **[[dreambooth]]**（DreamBooth）：微调整个文生图扩散模型，表达力强但需多张图、易过拟合内容；
- 这些工作大多只在**绘画类**风格上验证，且需要十几张参考图；神经风格迁移（NST）则用一张图引导**内容空间结构**，与文本驱动的内容生成范式不同。

StyleDrop 的定位：(1) 把 PEFT（adapter tuning）的「风格调优」框架第一次系统性地搬到**非自回归生成视觉 Transformer**（Muse/MaskGIT 一族）上；(2) 把适用范围从绘画拓展到 3D 渲染、设计插画、雕塑等多媒材；(3) 把所需样本压到**单张**。论文还给出一个反直觉的发现：在「少样本风格迁移」这件事上，离散 token 的 Muse 比同样用 T5-XXL、同样训练数据的扩散模型 [[imagen]] 更高效——这也是它选 Muse 作为 backbone 的核心理由。名字 StyleDrop 取自取色器（eyedropper），寓意「从一张图里一键吸取风格」。

## 模型架构
**Backbone：[[muse]]（masked generative image Transformer）**，不是扩散、不是自回归，而是 **MaskGIT 式的并行掩码 token 解码**。Muse 由两级合成模块组成：base（256×256）与 super-resolution（512×512 / 1024×1024）。每级含五个部件：
- 文本编码器 `T` = **T5-XXL**（冻结）；
- VQGAN 的图像编码器 `E` / 解码器 `D`（把图像映射到离散 visual token 序列再还原，冻结）；
- 生成 Transformer `G`（**被微调的对象**）；
- 采样器 `S`（迭代并行解码，base 36 步、super-res 12 步）。

训练目标是 **masked visual token modeling**（带掩码的交叉熵，只在被掩码 token 上求和，式 2）。推理用 token 级 classifier-free guidance（式 1，含负向 prompt `n` 与 guidance scale λ）。

**StyleDrop 的改动 = 给 `G` 插 adapter（其余 E/D/T 全冻结）。** Adapter 结构（附录 B.1.1，Flax 伪码）非常轻：

```
prj = einsum('...d,dh->...h', emb, wd)   # 下投影 D->H
prj = gelu(prj)
prj = einsum('...h,hd->...d', prj, wu)   # 上投影 H->D
return emb + prj                          # 残差
```

每个 Transformer 层插**两个 adapter**：一个在 cross-attention block 之后、一个在 MLP block 之后（沿用 Houlsby 2019 的 adapter 范式）。初始化：上投影 `wu` 全 0（保证初始等同原模型），下投影 `wd` 用 std=0.02 截断正态。

**参数效率细节（关键）**：用一个 `AdapterGenerator` 通过 `nn.Embed` 跨层生成 adapter 权重，并支持 `is_shared` 跨层共享（把深度、emb、prj 因子化），开启后参数量约缩小到原来的 1/层数。最终各阶段可训练参数量极小：

| 阶段 | d_prj（瓶颈维 H） | is_shared | adapter 参数量 |
| --- | --- | --- | --- |
| Base Round 1 | 4 | True | **0.23M** |
| Base Round 2 | 32 | False | 12.6M |
| Super-res | 32 | False | 6.3M |

即第一轮单图学风格只需训练 **0.23M** 参数（论文反复强调「< 1% 总参数」）。

**两个核心生成式创新（不是单纯插 adapter）**：

1. **内容 / 风格解耦的文本构造（§3.2.1）**：训练时不像 DreamBooth 用同一个 prompt 描述所有图，而是给每张图拼「内容描述 + 风格描述」，如「A cat in *watercolor painting style*」。把内容写进 prompt，逼着 adapter 参数 θ 只去建模**风格**。可用罕见 token（[V*]）替代风格词，效果相当，但用**描述性风格词**能额外解锁「风格属性编辑」（生成时删掉某个词，如去掉 "melting"）。

2. **双 θ 采样：My Subject in My Style（§3.4）**：把 StyleDrop（风格 adapter θ_s）和 [[dreambooth]]（内容 adapter θ_c）**分别独立训练**，推理时按 `l_k = (1-γ)·l_k^s + γ·l_k^c` 在每个解码步线性混合两路 logits（式 5/6，γ∈0.5~0.7）。这避免了 Custom Diffusion / SVDiff 那种「内容+风格联合训练」的耦合，组合更灵活——任意预训练 adapter 即插即组。

推理用**双 guidance scale**（式 4）：λ_A 控制对微调分布的风格适配强度（对比微调 Ĝ 与原始 G），λ_B 控制文本对齐（对比正负 prompt）。默认 λ_A=0~2.0、λ_B=5.0。

## 数据
StyleDrop 本体**不训练新基座**，所有大规模数据来自冻结的 Muse 预训练（论文未在本文披露 Muse 的训练集明细，仅指出 Muse 与 Imagen「在同一批 image/text 对、同一文本编码器 T5-XXL 上训练」）。StyleDrop 自身的「数据」就是**风格调优样本**：

- **风格参考集**：作者自行收集**几十张**多媒材风格图——水彩/油画、扁平插画、3D 渲染、不同材质雕塑等，刻意超出 NST 偏好的纯绘画范围；图源与版权在附录 Tab. S1 标注。
- **每个风格的训练集 D_tr**：Round 1 仅用 **1 张**风格图（配人工拼写的「内容+风格」prompt）。
- **迭代训练（IT）用的合成数据**：用 Round 1 模型生成大量图（CLIP/random：每个 prompt 从 30 个 prompt × 64 张里挑 1 张；human：从同一池里挑约 10 张，每个风格人工选片约 3 分钟），用这「几十张高质量合成对」组成 Round 2 训练集。
- **My-Subject 实验的内容图**：每个 object 用 5~6 张图（teapot/vase 等取自 DreamBooth 数据集）。

无大规模清洗/re-captioning/美学过滤管线——这是小样本微调工作，"数据"就是手工挑的几张到几十张图加手写 caption。

## 训练方法
**训练目标**：沿用 Muse 的**带掩码 token 交叉熵**（masked visual token modeling，式 3），只更新 adapter 参数 θ、冻结 G/E/D/T。注意这里**不是 diffusion / flow matching / next-token**，而是离散 token 的 masked-token 目标。

**多阶段 = 带反馈的迭代训练（§3.3，本文最核心的训练 trick）**：
1. **Round 1**：单张风格图上训 adapter（1000 步）。问题：会过拟合内容——生成图常把参考图里的房子/背景一起泄漏出来（content leakage）。但「成功的样本」往往风格-内容解耦得很好（高精度、低召回）。
2. **挑样本**：从 Round 1 大量采样里挑出解耦良好的图，用三种反馈信号：
   - **CLIP feedback (CF)**：选 CLIP（图文）score 最高的图，自动、高效，提升文本保真但抓不住细腻风格；
   - **Human feedback (HF)**：人工选 < 12 张，约 3 分钟/风格，能补 CLIP 抓不到的微妙风格属性；
   - **Random**：随机选（baseline）。
3. **Round 2**：在挑出的「几十张高质量合成对」上重训新 adapter（同样目标），显著降低内容泄漏、提升召回。论文默认的「StyleDrop」指的就是**用 HF 挑 ≤10 张合成图训出的 Round 2 模型**。

这本质是一种**自蒸馏 / 拒绝采样式的对齐**：用模型自己生成 → 用反馈（CLIP 或人）筛选 → 回训自己，思想上呼应 LLM 的 RLHF/拒绝采样，但实现极简（无 reward model、无 RL，只是数据筛选 + 重训）。

**关键超参（附录 Tab. S3）**：Adam，lr=3e-5（base，作者强调高于此易过拟合内容、低于此收敛慢）/ 1e-4（super-res）；batch size 8；1000 步；解码 temperature 4.5；base 解码 36 步、super-res 12 步。基线对照：Imagen 上 DreamBooth 训 300 步（少于原文推荐的 1000 步以缓解过拟合）；SD 上 LoRA-DreamBooth 训 400 步（UNet lr 2e-4、CLIP lr 5e-6）。

无步数蒸馏 / consistency / LCM 等加速（推理速度靠 Muse 本身的并行 token 解码，几十步即可）。

## Infra（训练 / 推理工程）
- **训练硬件**：batch size 8 = **TPU v3 每 core 1 个样本**（即 8 核 TPU v3）。论文明确指出 StyleDrop **也能在单张 A100 GPU、batch size 1** 上训练——因为只训 0.23M~12.6M 个 adapter 参数，显存与算力门槛极低。
- **训练时长**：1000 步（极短）；人工选片环节约 **3 分钟/风格**。整体「学一个新风格」的代价以分钟计。
- **代码框架**：JAX / Flax（附录给出 Flax 伪码）。
- **推理**：Muse 的并行掩码解码，base 36 步 + super-res 12 步，远少于扩散模型的几十~上百步去噪；双 logits 混合（My-Subject）只是每步多算一路 forward。
- **未披露**：具体训练墙钟时间、吞吐、Muse 基座的算力规模、量化/部署形态（StyleDrop 未开源官方权重与代码，仅有项目页；社区有第三方 PyTorch 复现，非官方）。

## 评测 benchmark（把效果讲清楚）
**评测协议**：自建（作者称此前缺少系统的 style-tuning 评测）。从 [[parti]] PartiPrompts 取 **190** 个基础构图 prompt（剔除 abstract/arts/people/world-knowledge），在 **6 个**风格参考图上、每 prompt 生成 8 张，共 **1520** 张图。两类指标：

**1) CLIP 双指标（Tab. 2 下半，↑ 越高越好）**：Text = 图文 CLIP 余弦相似度（文本保真）；Style = 合成图与风格参考图的 CLIP 视觉相似度（风格保真）。

| Method | Text | Style |
| --- | --- | --- |
| Imagen（prompt 引导风格） | 0.337 | 0.569 |
| DreamBooth on Imagen | 0.335 | **0.644** |
| Muse（prompt 引导风格） | 0.323 | 0.556 |
| **StyleDrop on Muse, Round 1** | 0.313 | **0.705** |
| **StyleDrop (HF)** | 0.322 | **0.694** |
| **StyleDrop (CF)** | 0.329 | 0.673 |
| StyleDrop (Random) | 0.316 | 0.678 |

要点：StyleDrop(HF) 的 Text 0.322 ≈ Muse 基线 0.323（几乎不损文本能力），Style 0.694 ≫ 0.556（大幅提升风格一致）。Round 1 的 Style 最高（0.705）但因轻微 mode collapse 文本分降到 0.313；**迭代训练（IT）用文本分换风格分**——CF/HF 把 Text 拉回 0.322~0.329，Style 略降。**关键对比**：StyleDrop on Muse 的风格分增益（0.556→0.694）远大于 DreamBooth on Imagen（0.569→0.644），论文据此论证「在 Muse 上做风格微调比在 Imagen 上更有效」。

**2) 人评（Tab. 2 上半，3 组 A/B test，6 风格 × 50 query = 300 query × 5 rater = 4500 答案）**：
- **StyleDrop(R1) vs DreamBooth-on-Imagen**：Style 偏好 **86.0%** : 9.7%（tie 4.3%）；Text 偏好 31.7% : 23.3%（tie 45%）——风格上碾压。
- **StyleDrop(R1) vs StyleDrop(HF)**：HF 的 Text 偏好更高（56% tie，R1 20.7% vs HF 23.3%），R1 的 Style 偏好更高（62.3% vs 30.3%）——即 IT 用风格换文本，看到明显「风格漂移」。
- **StyleDrop(HF) vs StyleDrop(CF)**：HF 留住更多 Style（60.9% vs 30.8%），CF 留住更多 Text——印证 CLIP/人评的取舍。
- 结论：CLIP score 是用户研究的良好代理。

**关键消融**：
- **§4.4.1 为什么 Muse 比 Imagen 强**：在 Imagen 上，单张图 + 罕见 token 学不到「melting」属性，需要 10 张合成图 + 描述性风格词才学得到；而 Muse 单图即可。说明 StyleDrop 的优势主要来自 **Muse 在少样本下极高的微调数据效率**，而非 prompt engineering。
- **§4.4.2 风格属性编辑**：用描述性风格词训练，生成时删词即可剥离某个风格属性（如去掉 "melting" 只保留 "golden 3d rendering"），罕见 token 做不到。
- **§4.4.3 反馈信号对比**：Round 1 Text 0.303→ Random 0.322 / CLIP 0.339 / Human 0.328；（Style 分在此场景会被内容泄漏误导而偏高，不能单看）。IT 各信号都降内容泄漏，CF 偏文本、HF 偏风格。
- **§4.4.4 细粒度风格控制**：对同一设计师的 4 张「色偏/渐变/尖角」微差风格图，HF 能逐一捕捉，证明可控到细微属性。
- **附录 B.3.1 CFG 消融**：λ_A 大或 λ_B 小时 Round 1 会内容泄漏；HF（Round 2）模型对 guidance scale 变化更鲁棒。

## 创新点与影响
**核心贡献**：
1. **首个把 PEFT（adapter tuning）风格调优系统化搬到非自回归掩码生成 Transformer（Muse/MaskGIT 系）的工作**，并实证其在「单图少样本」下优于扩散基座（Imagen/SD）——为「离散 token 生成模型更适合少样本风格迁移」提供了一手证据。
2. **极致样本/参数效率**：单张图 + < 1% 参数（最小 0.23M）+ 1000 步 + 可单卡 A100，分钟级学一个新风格。
3. **带反馈的迭代训练（自生成→筛选→回训）**：以极简方式（无 RL/无 reward model）解决单图微调的内容泄漏，CLIP 与人评互补；思想上是把 RLHF 的「反馈对齐」搬进文生图风格定制。
4. **内容/风格解耦的描述性 prompt**：附带解锁「风格属性编辑」这一新能力。
5. **双 θ 组合采样（My Subject in My Style）**：风格 adapter 与内容 adapter 独立训练、推理期线性组合，免联合训练，组合自由。

**影响**：StyleDrop 是 2023 年「风格化生成 / 少样本定制」的代表作之一，常与 DreamBooth、Textual Inversion、[[hyperdreambooth]]、IP-Adapter、StyleAligned 等一同被引为风格/主体个性化的基线与对照；它对「掩码生成 Transformer vs 扩散」在定制任务上的优劣讨论，也为后续统一/离散 token 路线提供了论据。社区有第三方 PyTorch 复现（官方未放代码与权重）。

**已知局限（作者自述）**：
- 视觉风格的多样性远超本文覆盖，缺乏对「形式属性 / 媒材 / 历史时期 / 艺术流派」的系统性风格体系研究；
- 「生成式视觉 Transformer 优于扩散」的结论**并非定论**，需更深入的跨模型对比；
- IT 因人工/CLIP 选片的选择偏置会导致**风格漂移**（Style 分下降）；
- 单图微调仍可能内容泄漏（靠 IT 缓解而非根除）；
- **社会风险**：可在未经艺术家同意下复制其个人风格，作者呼吁负责任使用。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2306.00983
- arxiv_pdf: https://arxiv.org/pdf/2306.00983
- project_page: https://styledrop.github.io/
- ar5iv（全文 HTML，含附录）: https://ar5iv.labs.arxiv.org/html/2306.00983

## 一手源存档（sources/）
- [ar5iv.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/styledrop--ar5iv.md) （ar5iv 全文 markdown：正文 §1-5 + 附录 B，含 adapter 伪码/超参表/CFG 消融——主精读来源）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/styledrop--project-page.md) （styledrop.github.io 项目页快照）
- [arxiv-2306.00983.pdf](https://arxiv.org/pdf/2306.00983) （arXiv 官方 PDF，28 页完整版，已直连重抓修复，pdftotext 可正常提取；全文表格/超参数已逐一核对）
