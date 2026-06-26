---
title: "CM3: A Causal Masked Multimodal Model of the Internet"
org: "Meta (FAIR)"
country: US
date: "2022-01"
type: paper
category: unified
tags: [autoregressive, decoder-only, causal-masking, multimodal, html, vqvae-gan, zero-shot, infilling, entity-linking, unified]
url: "https://arxiv.org/abs/2201.07520"
arxiv: "https://arxiv.org/abs/2201.07520"
pdf_url: "https://arxiv.org/pdf/2201.07520"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2201.07520.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CM3 是 Meta FAIR 2022 年 1 月发布的**因果掩码（causally masked）多模态自回归模型**：把整篇 HTML 网页（文本 + 超文本标记 + 超链接 + 经 VQVAE-GAN 离散化的图像 token）按其在源码中**原始出现顺序**拼成单一序列，用 decoder-only Transformer 做生成式建模；最大 **13B 参数**（CM3-Large），在近 **1 TB** 简化 HTML 上训练。其核心创新是"因果 + 掩码"的混合训练目标——逐 token 左到右生成的同时把少量长 span 移到序列末尾生成，从而在生成时获得**双向上下文**。单一模型零样本即可恢复 DALL·E（文生图）、GENRE（实体链接）、HTLM（摘要）等多个专用模型的能力，并在零样本摘要、实体链接、实体消歧上刷新 SOTA。它是后续 **CM3Leon → [[chameleon]]** 统一多模态架构的直接前身。

## 背景与定位
2022 年前的多模态生成大多走两条窄路：要么**单模态**（纯文本 LM 如 GPT-3、纯图像如 [[image-gpt]]），要么**精心策展的图文对齐**数据（[[dall-e-1]] 用 2.5 亿图文对、CLIP 用对齐的 caption）。这些方法把"图"和"文"当作两个分离模态拼起来，丢掉了它们在真实网页里**天然共现的文档结构**（一段文字旁边就是配图、超链接指向某实体、alt 属性就是图的描述）。

CM3 的出发点是：互联网网页本身就是规模化、自带结构标注的多模态语料——HTML 里的 `<a title="...">` 是免费的实体链接监督、`<img alt="...">` 是免费的图文配对、`<title>`/`meta` 是免费的摘要监督。它直接把 FAIR 自家的 **HTLM**（Aghajanyan et al. 2021，用 BART 式目标在简化 HTML 上预训练的纯文本模型）扩展到多模态：(1) 通过 VQVAE-GAN（来自 [[taming-transformers-vqgan]]）把图像离散成 token 塞进 HTML 的 `src` 属性；(2) 把 HTLM 的 BART-like encoder-decoder 目标换成**新的 causally masked 目标 + decoder-only 架构**；(3) 规模放大一个数量级（HTLM 最大 400M → CM3 最大 13B）。

技术脉络上，CM3 处在"把非离散模态 token 化后用统一序列模型建模"这一脉（[[dall-e-1]] 对图像、Jukebox 对音乐、vq-wav2vec 对语音），但 CM3 第一次把**整篇带结构的网页文档**（文本 + 标记 + 链接 + 图）作为统一序列建模对象，是"用一个 decoder-only 模型统一图文生成与理解"思路的早期奠基工作。

## 模型架构
**decoder-only 因果 Transformer**，架构直接复用 Artetxe et al. 2021（FAIR 的 dense LM）的同名规格，无图文专用结构改动——这正是其"统一"哲学的体现：图像 token 和文本 token 共享同一套 Transformer，不设独立视觉编码器/交叉注意力。

- **训练 4 个规模**：125M、800M、2.7B（**CM3-Medium**）、13B（**CM3-Large**）；两个小模型仅用于定超参，所有下游评测只用 Medium 和 Large。
- **CM3-Large（13B）**：`decoder-embed-dim = 5120`，`ffn-embed-dim = 20480`（4× 宽），`layers = 40`，`attention-heads = 40`，pre-LayerNorm（normalize-before=True），共享输入输出 embedding，**正弦/固定位置编码**（learned-pos=False）。
- **CM3-Medium（2.7B）**：`embed-dim = 2560`，`ffn = 10240`，`layers = 32`，`heads = 32`，其余同上。
- **最大序列长度 2048 token**。

**视觉 tokenizer（VQVAE-GAN）**：
- 对文档里每个带合法 `src` 的 `<img>` 标签，下载图像 → resize 到 **256×256（随机裁剪）** → 用 [[taming-transformers-vqgan]] 的 VQVAE-GAN 离散成 **每图 256 个 token**，再把这 256 个 token 字符串（空格连接）写回 `src` 属性的值。
- 不限制图像数量与位置——图可以出现在文档任意处、任意多张，完全按 HTML 原始顺序。
- 附录 A.2 验证：图像 token 在码本上的分布**近似均匀**（与文本 token 的 Zipf 分布形成对比），这也是作者讨论 CM3 scaling law 偏离标准假设的原因之一。

**文本侧**：无独立 text encoder（不用 T5/CLIP），文本就是 BPE token，和图像 token 同处一条序列。HTML 标签、属性、超链接全部作为普通文本 token 参与建模。

**条件注入**：CM3 没有"条件"这一独立机制——所有任务都通过**提示词（prompt）构造**实现。例如文生图就是给 `<img alt="{prompt}` 让模型续写 `src` 里的图像 token；captioning 就是给图像 token 让模型填 `alt`/`title`；实体链接就是在 `<a title="<mask:0>">实体</a>` 处填掩码。

## 数据
作者**主动放弃**处理整个 Common Crawl——援引 Birhane et al. 2021 对 CC 多模态数据集的批评（含大量露骨/种族歧视的图文对），出于伦理考虑只 **opt-in** 两个相对干净的来源：

| 来源 | 文档(M) | 大小(GB) | 唯一图像(M) | token(B) |
|---|---|---|---|---|
| CC-NEWS（Common Crawl 新闻子集） | 45 | 460 | 18 | 121 |
| En-Wikipedia（全量英文维基） | 16 | 383 | 7 | 102 |
| **合计** | **61** | **843** | **25** | **223** |

- **总规模约 843 GB（近 1 TB）、6100 万文档、2500 万唯一图像、2230 亿 token**。注意：作者明确说 CM3 的唯一图像数比 DALL·E **少约一个数量级**（论文原文 "an order of magnitude less unique images than DALL-E"；CM3 = 25M，DALL·E-1 论文用 2.5 亿图文对）——CM3 因此不擅长生成虚构图像，且因图像只来自新闻/维基，覆盖面偏窄。
- **HTML 清洗（沿用 HTLM 的 minimal-HTML 变换）**：对每篇文档的 DOM 多遍剥离——删除所有不含文本元素的节点；过滤 header/footer/版权/表单/对话框/iframe；把连续 `<div>` 折叠成单个（合并属性）；**剥离每个元素上"非来自结构化图谱"的属性，只保留 OpenGraph / Schema / Twitter 这类结构化图谱来源的属性**（论文原文："strip all the attributes … which are not derived from structured graphs such as OpenGraph, Schema and Twitter"——即保留而非删除这三类）。目标是保留"语义最大价值"的最小 HTML 子集。
- **图像处理**：见架构节（256×256 随机裁剪 → VQVAE-GAN → 每图 256 token 写回 src）。
- **去重测试集**：每个来源各切 **两个测试集、每个 10,000 篇唯一文档**，并尽力与训练集去重。
- **标注/合成数据**：纯用网页原生的 HTML 结构与 alt-text，**无 re-captioning、无合成数据、无人工对齐**——这正是 CM3"用互联网原生结构当免费监督"的核心主张。

## 训练方法
**核心创新：Causally Masked 目标（因果掩码）。** 这是 causal LM 与 masked LM 的混合：

1. 对一篇长度为 `s` 的文档，采 `n ~ Clamp(Poisson(1), 1, 16)` 个掩码（平均很少、约 1 个），每个掩码取一段 span `m ~ (Uniform(0,s), Uniform(0,s))`，各 span 互不相交。设计意图是"选少量但较长的 span"，逼模型学会长 span 填充（infill 整张图或整个结构化文本块）。
2. 按 span 在原文中的出现顺序，把每段 span **替换为编号掩码 token**（`<mask:0>`、`<mask:1>`…），并把被替换的 span 内容**移到文档末尾**，后接一个唯一的文档结束 token。
3. 然后做**标准的从左到右因果 LM**（逐 token 预测，每个 token 都算 loss，不像 BERT 只解码 15%）。

关键收益：当模型生成被移到末尾的 mask 内容时，它能看到 mask 原位置**两侧的全部上下文**（因为这些上下文在序列里都排在 mask 内容之前），于是在保持"全生成式 + 每 token 受训"的同时获得了**双向上下文**——这正是纯 causal LM（如 [[dall-e-1]] 的左到右）做不到的图像/结构 infilling 能力。

- **Loss 改造**：把预测 `<mask:i>` 占位 token 本身的交叉熵权重置 **0**（它们被放在随机位置，不携带序列建模信息）。
- **Size Hints（来自 HTLM）的取舍**：HTLM 在 mask 后插一个概率性长度估计 token 引导生成；CM3 实验发现 size-hint **同时损害困惑度和零样本性能**，故弃用，改用"隐式 size hint"——让模型先因果生成 `max_seq_len - size_hint` 个 token 再放 `<mask:0>`。
- **训练配置**：PyTorch + **fairseq** + **fairscale**；per-GPU batch=8，max seq len=2048；**polynomial-decay** LR 调度，1500 warmup；梯度裁剪 1.0；Adam（β1=0.9, β2=0.98）。
- **无 SFT / RLHF / DPO / 偏好对齐 / 蒸馏**——纯预训练 + 任务级 prompt（下游 GLUE 等才做 fine-tuning）。
- **Scaling law**：作者指出 CM3 打破了标准 LM scaling 的三个假设——(a) 图像 token 近均匀分布而文本 token 服从 Zipf，token 分布不同质；(b) 图文位置不受限带来不可预测的复杂度；(c) 因果掩码本质是通过 shuffle 文档来算联合概率。即便如此，四个规模的困惑度曲线呈现"健康的、类 Kaplan et al. 2020 的 scaling"，无病态，暗示继续放大仍有收益（深入分析留作 future work）。

## Infra（训练 / 推理工程）
- **算力（注：论文此处把模型误写为 "HTLM-Medium/Large"，按上下文即 CM3-Medium/Large）**：
  - CM3-Medium（2.7B）：**240 张 V100，训练 28 天**。
  - CM3-Large（13B）：**384 张 A100，训练 24 天**。
- 框架 fairseq + fairscale（FAIR 自家大规模训练栈）。
- **推理/采样**：图像生成温度 0.85、直接采样；条件文生图对每个 prompt 采 **32 个候选用 CLIP 重排取 top-4**（同 DALL·E 的 CLIP rerank 思路）；captioning 用 beam=5 在两类 prompt 上取最小困惑度，或采 128 个 caption（masked/causal prompt 各 64）再用 CLIP 选最优。无量化/蒸馏/缓存等推理加速披露。
- **未披露**：吞吐（tokens/s）、GPU·时总量、并行策略细节（TP/PP/DP 配置）、混合精度精度位宽——论文均未报告。

## 评测 benchmark（把效果讲清楚）
CM3 用"单一模型零样本恢复多个专用模型"作为卖点，评测横跨图像、图文、纯文本三类。

**图像生成（MS-COCO 256×256 零样本 FID，越低越好；Table 2）**：
- **CM3 自家**：Unconditional CM3-Medium **40.65**（表中另有一行同名 36.51，疑为两种 prompt/采样设置）；Conditional CM3-Medium **36.78**；Conditional CM3-Large **29.56**。（注意：表中 CM3 全部列在 "Zero-shot FID" 列。）
- 同表对照（"Zero-shot FID" 列）：DALL·E **~28**（论文原文只写 "∼ 28"，无更精确小数）、LAFITE **26.94**、[[glide]] **12.24**。非零样本列（"FID"，专门为 COCO 训练/优化）：XMC-GAN **9.33**、LAFITE **8.12**、AttnGAN 35.49、DM-GAN 32.64、DF-GAN 21.42、DM-GAN+CL 20.79。
- 结论：CM3-Large 条件生成零样本 FID **29.56，逼近 DALL·E（~28）**，且唯一图像**少约一个数量级**（CM3 25M；DALL·E-1 论文用 2.5 亿图文对——论文原文只说 "an order of magnitude less"，250M 系据 DALL·E-1 反推的交叉引用），但明显落后于同期扩散 SOTA（[[glide]] 12.24）。CM3 定位是"统一模型顺带能画图"，非画质 SOTA。

**零样本 image captioning（MS-COCO，BERTScore，Table 3）**：
- CM3-Caption-Beam：P/R/F1 = **0.781 / 0.789 / 0.785**。
- CM3-Caption-CLIP（128 候选 CLIP 选优）：**0.863 / 0.866 / 0.864**。
- 用 BERTScore 而非 BLEU/METEOR，因零样本 caption 的词汇/句式与 COCO 标注不兼容但语义相近。

**实体消歧（Named Entity Disambiguation，InKB Micro-F1，Table 4；6 测试集均值）**：
- **零样本（self-supervision，0-shot）** CM3-Large 平均 **79.0**（AIDA 80.1 / MSNBC 80.8 / AQUAINT 77.7 / ACE2004 82.8 / CWEB 72.4 / WIKI* 80.2），非平凡——纯靠 Wikipedia HTML 里 `<a title>` 的天然监督。
- **微调后（Direct Supervision）** CM3-Large 平均 **89.8**（AIDA 94.8、MSNBC 94.8、AQUAINT 91.1、ACE2004 91.4、CWEB 78.4、WIKI* 88.7），**超过此前最佳专用模型**（同表 De Cao et al. 2020 / GENRE 均值 **88.8**；更早的 Yang et al. 2018 为 88.0），刷新该任务 SOTA。

**端到端实体链接（Entity Linking，InKB Micro-F1 in GERBIL，Table 5）**：
- 微调 CM3-Large 平均 **59.3**（7 个测试集），超过 De Cao et al. 2020 等专用模型，设新 SOTA；零样本平均 26.7（远低但非平凡，证明训练隐式学到实体链接）。

**零样本摘要（ROUGE-1/2/L，Table 6）**：
- CM3-L-Manual：Gigaword **32.12/10.95/28.78**、CNN/DM **38.88/16.27/34.16**、XSum **24.86/6.08/16.32**。
- **在 Gigaword、CNN/DM、XSum 三个新闻类数据集上刷新零样本 SOTA**（超 PEGASUS-0S 与 HTLM-Manual-S；prompt 直接沿用为 HTLM 调好的、未改）。
- Reddit-TIFU 较差（12.14/2.12/7.98），作者归因于预训练只含 CC-NEWS + Wikipedia，缺 Reddit 式摘要分布。

**微调 GLUE（dev set，Table 7）**：
- CM3-Large-RXF-Prompt：MNLI 91.9/91.5、QNLI 96.4、SST-2 97.3、CoLA 70.8 等，与同参数量 T5（T5-11B）**整体相当**——证明因果掩码目标 + 联合建模图像 token **不损害**可微调的文本表征质量。

**偏见评测（GWEAT/GSEAT，Table 8/9）**：
- 6 项性别（Table 8）+ 7 项种族（Table 9）偏见测试中，显著偏见计数（p<0.05）：CM3-Medium **0 性别 + 1 种族 = 1**，CM3-Large **2 性别 + 3 种族 = 5**，均**显著低于** VisualBERT（5 性别 + 4 种族 = 9）和 ViLBERT（6 性别 + 5 种族 = 11）。作者归因于只用 Wikipedia + 近期 CC-NEWS 这类相对干净的来源（并提示 Medium 的低偏见可能部分源于欠拟合）。

**关键消融/观察**：(1) size-hint 弃用——同时降困惑度与零样本性能；(2) 无条件生成时模型**倾向先自动生成 alt 描述再生成图像 token**，且这种"自带 caption"能提升图像质量；(3) image infilling 在文本条件（Infilling-C）下显著优于无条件（Infilling-U）；(4) 离散 token 化导致细节/纹理丢失（图中文字模糊），是 captioning/生成失败的主因之一。

## 创新点与影响
**核心贡献**：
1. **首个超文本（hyper-text）图文模型**——把整篇带 HTML 结构（标记 + 超链接 + 图）的网页作为统一序列建模，证明"互联网原生文档结构"可直接当大规模、自带标注的多模态监督。
2. **Causally Masked 目标**——causal LM 与 masked LM 的混合，在保持"全生成式 + 每 token 受训 + 可规模化"的同时，为 mask 内容提供双向上下文，解锁 decoder-only 模型的**图像/结构 infilling**能力。
3. **单模型多任务零样本统一**——一个 CM3 经不同 prompt 即可恢复 DALL·E（文生图）、GENRE（实体链接）、HTLM（摘要）的功能，并在零样本摘要/实体链接/实体消歧上刷新 SOTA。
4. 开源代码与模型（论文承诺 "release all code and models"）。

**影响**：CM3 是 FAIR"用 decoder-only 自回归统一图文"路线的奠基之作，是后续 **CM3Leon**（2023，把 CM3 思路放大并加检索增强/CFG/对比解码做高质量文生图与图文理解）和 **[[chameleon]]**（2024，early-fusion token-based 混合模态基础模型）的**直接前身**——三者一脉相承，共同构成"统一 token、混合模态、单 Transformer"的技术谱系，并与同期 Google Parti/Muse 等自回归 T2I 形成对照。其"网页 HTML 即免费多模态监督"的数据哲学也影响了后续大量混合模态预训练工作。

**已知局限**：
- 图像质量落后同期扩散 SOTA（COCO FID 29.56 vs [[glide]] 12.24），且唯一图像仅 25M、只来自新闻/维基，**不擅长虚构/罕见图像**。
- VQVAE-GAN 离散化丢纹理细节（文字模糊），限制了 captioning 与生成的保真度。
- 零样本实体链接绝对分数仍远低于微调版（26.7 vs 59.3）。
- Infra 细节（吞吐、并行策略、精度）与完整 scaling law 分析均未披露/留作 future work。
- 论文 §3.3 把 CM3-Medium/Large 的算力误标为 "HTLM-Medium/Large"（笔误）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2201.07520
- arxiv_pdf: https://arxiv.org/pdf/2201.07520

## 一手源存档（sources/）
- [arxiv-2201.07520.pdf](https://arxiv.org/pdf/2201.07520)  （arXiv 原文 PDF，不入 git）
