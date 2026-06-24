---
title: 早期与全开（数据全公开）大模型训练配方深挖 — BLOOM/ROOTS · Pythia · GPT-NeoX · Falcon/RefinedWeb · MAP-Neo · OpenCoder · StarCoder/The Stack · RedPajama · DCLM
type: deep-dive
tags: [fully-open, open-data, pretraining, data-pipeline, BLOOM, Pythia, GPT-NeoX, Falcon, RefinedWeb, MAP-Neo, OpenCoder, StarCoder, The-Stack, RedPajama, DCLM]
created: 2026-06-18
updated: 2026-06-18
---

# 早期与全开（数据全公开）家族训练配方深挖

> 本档案聚焦"数据全公开/全开放"这一谱系：不仅放权重，还公开**预训练语料、数据处理代码、训练代码、检查点**。
> 所有数字均抠自官方一手报告/arXiv 原文/官方博客/官方 GitHub-model card；查不到的明确标注"官方未公开"。
> 注意：本谱系横跨"全开放模型"（BLOOM、Pythia、GPT-NeoX、MAP-Neo、OpenCoder、StarCoder、RedPajama-INCITE）与
> "全开放**数据集**项目"（The Pile、ROOTS、RefinedWeb、The Stack、RedPajama-Data、DCLM）。数据集本身就是这条线的灵魂，
> 所以每个数据集项目也单列处理 pipeline。

---

## 家族演进脉络（时间线）

- **2020-12 The Pile（EleutherAI）** — 825 GiB、22 个子集的英文语料，首个"按子集质量加权 + 公开 datasheet"的开放语料，为后续 GPT-Neo/NeoX/Pythia 奠基。
- **2022-02 GPT-NeoX-20B（EleutherAI）** — 在 Pile 上训练的 20B，开源 Megatron+DeepSpeed 代码栈与 RoPE/parallel-attn 架构，成为后续大量开源模型的"参考实现"。
- **2022-07 ROOTS / 2022-11 BLOOM（BigScience）** — 千人协作，1.61TB / 59 语种 ROOTS 语料 + 176B 多语模型，迄今最透明的百亿级工程之一（权重/数据/代码/日志全开）。
- **2022-11 The Stack v1（BigCode）** — 3.1TB → v1.2 6.4TB 许可宽松代码语料，带 opt-out 治理框架。
- **2023-04 Pythia（EleutherAI）** — 16 个同序数据 LLM（70M–12B × dedup/非dedup）+ 154 检查点/模型，训练动力学研究基石。
- **2023-05 StarCoder/StarCoderBase（BigCode）** — 15.5B 代码模型，8K 上下文、MQA、FIM，1T token。
- **2023-04/06 RedPajama-V1 + INCITE（Together）** — LLaMA-1 语料的开放复刻（1.2T），并在 Summit 超算上训出 3B/7B INCITE 模型。
- **2023-06 RefinedWeb / Falcon-1（TII）** — "纯 web 数据 + 严格去重即可媲美 curated 数据"，MDR pipeline，Falcon-7/40/180B。
- **2024-02 StarCoder2 + The Stack v2（BigCode×Software Heritage）** — 619 语种、67.5TB，3B/7B/15B，GQA + 长上下文 16K。
- **2024-05 MAP-Neo（M-A-P）** — 首个"全栈全开"中英双语 7B（语料 Matrix Data Pile + 处理代码 + 检查点 + DPO 全开）。
- **2024-06 DataComp-LM/DCLM（多方）** — 240T token 标准化测试平台，证明"model-based filtering"是关键；DCLM-Baseline 7B/2.6T → MMLU 64%。
- **2024-11 OpenCoder（INF/M-A-P 等）** — 完全可复现代码 LLM（RefineCode 960B + SFT 语料 + 检查点全开）。
- **2024-11 RedPajama-Data-V2 论文（Together）** — 100T+ token、40+ 质量信号的 web-only 巨型语料正式成文。
- **2024-12 Falcon 3（TII，开放权重）** — 1B/3B/7B/10B + Mamba-7B，14T token，Llama 兼容架构（数据未全开，仅作脉络补记）。

---

## 各代关键参数对比（速查表）

> 说明：除非注明，"上下文"指预训练原生长度；MoE 列除特殊说明外这一族**全部为 Dense**。

**模型（权重开放）**

- **GPT-NeoX-20B** — 20B(19.9B非emb) · 44层 · hid 6144 · 64头(MHA) · vocab 50257/50432 · ctx 2048 · RoPE(partial)+parallel-attn · 数据=The Pile · ~400B token(≈1.4 epoch) · 96×A100-40GB · fp16
- **BLOOM-176B** — 176B · 70层 · hid 14336 · 112头(MHA) · vocab 250680 · ctx 2048 · ALiBi+GELU+embedding-LN · 数据=ROOTS · 366B token · 384×A100-80GB · BF16
- **Pythia(70M–12B)** — 8尺寸×{dedup,非dedup}=16模型 · GPT-NeoX架构(RoPE+parallel-attn+FlashAttn+untied-emb) · 数据=Pile 300B / 207B(dedup,~1.5ep) · A100-40GB · 154检查点/模型
- **RedPajama-INCITE-3B/7B** — GPT-NeoX/Pythia 风格 dense · 数据=RedPajama-V1 1.2T · 3B训800B / 7B训1.001T token · Summit 6×V100节点 · fp16
- **Falcon-7B/40B/180B** — dense · 7B:32层/4544 · 40B:60层/8192 · 180B:80层/14848 · head_dim 64 · MQA(7B,nkv1)/multigroup-GQA(40&180B,nkv8) · vocab 65024 · ctx 2048 · RoPE+parallel-attn · 数据=RefinedWeb · 1.5T/1.0T/3.5T token · 384/384/4096×A100-40GB · BF16
- **StarCoderBase/StarCoder-15.5B** — 40层 · hid 6144 · 48头 · MQA · vocab 49152 · ctx 8192 · FIM · 数据=The Stack v1.2 · 1T token(+35B Python→StarCoder) · 512×A100-80GB · BF16
- **StarCoder2-3B/7B/15B** — 30/32/40层 · hid 3072/4608/6144 · 头24/36/48 · KV头2/4/4(GQA) · vocab 49152 · ctx 4k→16k(滑窗4k) · RoPE+FIM · 数据=The Stack v2 · 3.1/3.5/4.1T token(≈4-5 epoch) · A100-80GB
- **MAP-Neo-2B/7B** — 18/28层 · hid 2048/3072 · 头8/16 · KV头1(MQA)/16(MHA) · FFN=8×hid · vocab 64000 · ctx 8192 · RoPE+RMSNorm+SwiGLU · 数据=Matrix Data Pile · 7B训 4.5T token · 512×H800
- **OpenCoder-1.5B/8B** — 24/32层 · hid 2240/4096 · 头14/32 · KV头14(MHA)/8(GQA,类Llama-3.1) · SwiGLU · vocab 96640 · ctx 4096/8192 · RoPE θ=10000/500000 · 数据=RefineCode+web · 2.0T(4ep)/2.5T(3.5ep)+各100B退火 · 256×H800 / 512×H100
- **DCLM-Baseline-7B** — 32层 · hid 4096 · 32头 · head_dim 128 · dense(类Llama,OpenLM实现) · GPT-NeoX tokenizer · ctx 2048→8192 · z-loss · 数据=DCLM-Baseline · 2.6T token · H100

**开放数据集项目**

- **The Pile** — 825.18 GiB · 22 子集 · 英文 · 子集质量加权(Wikipedia 最多 3 epoch)
- **ROOTS** — 1.61TB · 46 自然语+13 编程语(59) · BLOOM 用 ~341–366B token
- **RefinedWeb(MDR)** — 目标 3–6T，公开 600B extract · 纯 CommonCrawl · 去重后约移除 90% 文档
- **The Stack v1/v1.2/v2** — 3.1TB(30语)/6.4TB(358语)/67.5TB(619语,Software Heritage)
- **RedPajama-V1/V2** — 1.2T(LLaMA 复刻,7 域)/100T+(web-only,5 语,40+ 质量信号)
- **DCLM-Pool / DCLM-Baseline** — 240T token 池 / 3.8T 过滤后基线集

---

## The Pile（EleutherAI, 2020-12）— 全开语料的起点

- **定位**：825.18 GiB 英文语料，22 个多样子集，首个"显式按子集质量加权 + 公开 datasheet + 公开构建代码"的大规模开放语料。GPT-Neo/GPT-NeoX/Pythia/RedPajama 比较基线均源于此。
- **语料构成（22 子集，按字节占比加权，高质量子集多 epoch）**：
  - 新引入子集：Pile-CC（用 jusText 从 Web Archive WARC 重新抽取，质量优于原始 CC）、PubMed Central、ArXiv、GitHub、FreeLaw、Stack Exchange、USPTO、PubMed Abstracts、Ubuntu IRC、HackerNews、YouTube 字幕、PhilPapers、NIH ExPorter 等。
  - 既有 NLP 子集：BooksCorpus2、Books3、Project Gutenberg(PG-19)、OpenWebText2、Wikipedia(en)、OpenSubtitles、Enron Emails 等。
  - **加权策略**：高质量子集上采样（"epochs">1），如 Wikipedia 在一个完整 Pile epoch 内被见到最多 3 次；Pile-CC 等被下采样。"Effective Size"= 字节数 × epochs。
- **数据处理**：Pile-CC 用 jusText 抽正文；各子集做基础清洗；提供 datasheet 与构建脚本。
- **后续衍生**：GPT-NeoX/Pythia 直接用 Pile（含一份近去重 deduped Pile，约 207B token）。
- **来源**：arXiv https://arxiv.org/abs/2101.00027 · PDF https://arxiv.org/pdf/2101.00027 · 本地 `../../../sources/llm/2020/arxiv-2101.00027.pdf`

---

## GPT-NeoX-20B（EleutherAI, 2022-02）

### 架构细节
- **总参**：20B（其中 **19.9B** 非嵌入参数用于 scaling-law 分析）。
- **层/维/头**：**44 层 · hidden 6144 · 64 注意力头**（MHA，head_dim 96）。
- **位置编码**：**Rotary（RoPE），且为 partial rotary**（`rotary-pct`<1，仅对部分维度施加旋转，沿用 GPT-J 经验）。
- **结构创新**：**Parallel Attention + FF**（注意力与 FFN 并行计算，类 GPT-J），加速分布式训练。
- **激活/Norm**：GELU；LayerNorm（非 RMSNorm）。
- **tokenizer/vocab**：基于 **Pile 新训的 BPE tokenizer**，vocab 50257（embedding 维度 padding 到 50432）；改动包括更好地处理空白（对代码有利）。
- **上下文**：2048。MoE：无（dense）。

### 预训练数据
- **数据集**：**The Pile**（825 GiB，按原样使用，未额外去重——作者称小规模去重无明显增益）。
- **token 数**：batch 3.15M token × 150,000 步 ≈ **472B token 训练预算**，实际约 **400B token / ≈1.4 epoch**（训练含重复数据，作者称未见性能损失）。

### 数据处理 pipeline
- 直接用 Pile（含其内部清洗），未额外去重/分类器过滤——这是早期"信任语料、单 epoch 偏好"的代表做法。

### 训练细节
- **算力**：**12 台 Supermicro AS-4124GO-NART 服务器 × 8×A100-SXM4-40GB = 96 块 A100**；HDR InfiniBand（ConnectX-6，GPUDirect RDMA）。
- **并行**：**TP=2 · PP=4**（一个副本占 8 GPU）+ DP；**ZeRO**（DeepSpeed）。框架 = Megatron + DeepSpeed（PyTorch 1.10.0 / CUDA 11.1 / NCCL 2.10.3）。
- **精度**：**fp16**（混合精度，loss scaling；非 BF16，硬件为 40GB A100）。
- **优化器/LR**：AdamW（β=0.9/0.95，ε=1e-8），**WD 0.01**；LR **峰值 0.97e-4**（在 GPT-3 13B/175B LR 间插值得到），cosine 衰减到峰值 10%。
- **batch/序列**：global batch ≈ 3.15M token（1538 contexts × 2048）。
- **稳定性技巧**：用 Megatron 融合 CUDA 内核（scaled-upper-triang-masked-softmax-fusion 等）。
- 训练曾在第二个 epoch 边界附近继续训练（数据重复）。
- **GPU 时长/FLOPs**：官方未给确切卡时/FLOPs。

### SFT / RL / 对齐
- 无（GPT-NeoX-20B 仅为 base 预训练模型，无官方 SFT/RLHF）。

### AI infra
- 框架：GPT-NeoX 代码库（基于 Megatron + DeepSpeed），已开源；后被 Pythia/RedPajama-INCITE 等复用。

### 来源
- arXiv https://arxiv.org/abs/2204.06745 · 本地 `../../../sources/llm/2022/gpt-neox-20b.pdf`
- GitHub https://github.com/EleutherAI/gpt-neox

---

## ROOTS + BLOOM-176B（BigScience, 2022-07 / 2022-11）

### 架构细节（BLOOM-176B）
- **总参**：176B（精确 176,247M）；**decoder-only** Transformer。
- **层/维/头**：**70 层 · hidden 14336 · 112 注意力头**（MHA，head_dim 128）；序列长 2048。
- **位置编码**：**ALiBi**（不在 embedding 加位置信息，而是按 key-query 距离衰减注意力分；作者发现它不仅外推好，还使训练更平滑、loss 更低）。
- **结构创新**：**Embedding LayerNorm**（在 embedding 后加一层 LN，源于 104B 预实验的稳定性需要）；**tied embeddings**（输入输出 embedding 共享）。
- **激活/Norm**：**GELU**；LayerNorm。
- **tokenizer/vocab**：byte-level BPE，**vocab 250,680**（含 200 个预留 token，可用于 PII 占位）；多语共享词表，需被 128 整除（GPU）且被 4 整除（TP）。
- **上下文**：2048。MoE：无（dense）。
- **小尺寸**：同时放出 560M/1.1B/1.7B/3B/7.1B 等系列。

### 预训练数据（ROOTS 语料）
- **总量**：**1.61TB 文本**，**46 自然语言 + 13 编程语言 = 59 语种**；约 **341B token**（按 byte-fallback 计 ~366B token 训练）。
- **构成**：数百个源；约 **11% 为代码**；语言分布上英语占大头，含大量 Niger-Congo（非洲语）、Indic（印度语）等低资源语言（BigScience 显式优先纳入）。

### 数据处理 pipeline（ROOTS）
- **采购阶段**（sourcing）：社区驱动列出来源；**质量过滤**理念为"human-written for humans"（人写给人读），用一组质量指标剔除 spam/非自然语言。
- **处理阶段**：cleaning & filtering & deduplication；**两步去重 + PII 脱敏**（如社保号等）。
- 全套工具在 HF 上开源（含 process-pipeline 可视化）。

### 数据配比 / 阶段
- 单阶段预训练；语言占比由 ROOTS 决定；无 annealing/退火（早期做法）。

### 训练细节
- **算力**：法国 **Jean Zay 超算（IDRIS/CNRS）**；**48 节点 × 8×A100-80GB = 384 块 A100**；训练约 **3.5 个月（118 天）**，消耗 **1,082,990 GPU 卡时**。
- **并行**：**Megatron-DeepSpeed 3D 并行（DP+PP+TP）+ ZeRO stage 1**（仅优化器状态分片）。已知配置 **TP=4 · PP=12 · DP=8**（=384）。峰值达 **156 TFLOPs/GPU**（≈ A100 BF16 理论峰值 312 TFLOPs 的一半）。
- **精度**：**BF16 混合精度**（早期 V100 上的 104B 实验用 fp16 发散，A100 改 BF16 解决不稳定）。
- **batch/序列**：global batch 512（爬坡：256→512，序列 2048）；总 token 366B；warmup 375M token；decay 410B token。
- **优化器/LR**：Adam(β=0.9/0.95)，**WD 0.1**，gradient clipping 1.0；峰值 LR **6e-5**，**cosine** 衰减到 min 6e-6。
- **稳定性技巧**：BF16 + embedding LayerNorm + 融合 CUDA 内核；扩到 384 GPU 时关闭异步 CUDA 内核启动等。

### SFT / 多任务微调
- **BLOOMZ**：在 **xP3**（多语多任务 prompt 数据集，语言分布镜像 ROOTS）上做多任务 prompt 微调，获得跨语言 zero-shot 泛化。
- 衍生 SGPT-BLOOM（文本嵌入/检索）。
- 无 RLHF（早期）。

### AI infra
- 框架：Megatron-DeepSpeed（Megatron-LM 提供 Transformer/TP/dataloader，DeepSpeed 提供 ZeRO/PP）。从 S3 之外的 HPC 文件系统读数据。

### 来源
- arXiv（BLOOM）https://arxiv.org/abs/2211.05100 · PDF https://arxiv.org/pdf/2211.05100 · 本地 `../../../sources/llm/2022/bloom.pdf`
- ROOTS 语料论文 arXiv https://arxiv.org/abs/2303.03915
- HF 官方 https://huggingface.co/bigscience/bloom · BLOOMZ https://huggingface.co/bigscience/bloomz

---

## Pythia（EleutherAI, 2023-04）

### 架构细节
- **16 个模型**：8 个尺寸 **{70M, 160M, 410M, 1B, 1.4B, 2.8B, 6.9B, 12B}** × {Pile, deduped-Pile} 两套；同序数据是核心可控变量。
- **逐尺寸配置（层 / hidden / 头 / LR）**：
  - 70M：6 层 / 512 / 8 头 / LR 1.0e-3
  - 160M：12 层 / 768 / 12 头 / LR 6.0e-4
  - 410M：24 层 / 1024 / 16 头 / LR 3.0e-4
  - 1.0B：16 层 / 2048 / 8 头 / LR 3.0e-4
  - 1.4B：24 层 / 2048 / 16 头 / LR 2.0e-4
  - 2.8B：32 层 / 2560 / 32 头 / LR 1.6e-4
  - 6.9B：32 层 / 4096 / 32 头 / LR 1.2e-4
  - 12B：36 层 / 5120 / 40 头 / LR 1.2e-4
- **架构（沿用 GPT-NeoX）**：**RoPE** + **Parallel Attention+FF** + **Flash Attention**（训练吞吐）+ **untied embedding/unembedding**（解绑输入输出嵌入）。
- **tokenizer**：GPT-NeoX BPE（vocab 50432）。MoE：无。

### 预训练数据
- **Pile（非去重）= 299,892,736,000 ≈ 300B token**；**deduped-Pile = 207B token**（去重后跑 ≈1.5 epoch）。
- **所有 16 个模型见到完全相同顺序的数据**——这是套件的关键设计，使 checkpoint 间可严格对照。

### 数据处理 pipeline
- 复用 Pile / deduped-Pile（near-deduplication）；公开完整 dataloader，可精确重建任意训练步的 batch。

### 训练细节
- **batch/序列**：**所有尺寸统一 batch 1024 × 2048 = 2,097,152 token**（作者发现大 batch 不损收敛，反而大幅缩短墙钟时间）。
- **checkpoint**：每模型 **154 个**（log 间隔的早期密集点 + 之后每 2.1B token/1000 iter 一个均匀点）。
- **优化器**：**Adam + ZeRO**；Flash Attention。
- **算力**：A100-40GB GPU（论文给出每模型 GPU 数表，但未给总卡时/FLOPs）。
- 修订记录：≤2.8B 模型 LR 衰减到峰值 10%；6.9B/12B 早期存在 min-LR 不一致后已修正。
- 6.9B 用 model-parallel-size=2，12B 用 model-parallel-size=4。

### SFT / RL
- 无（Pythia 为纯研究用 base 套件）。

### AI infra
- 框架：开源 GPT-NeoX + DeepSpeed；公开训练/分析代码与 dataloader 重建工具。

### 来源
- arXiv https://arxiv.org/abs/2304.01373 · PDF https://arxiv.org/pdf/2304.01373 · 本地 `../../../sources/llm/2023/pythia.pdf`
- GitHub https://github.com/EleutherAI/pythia

---

## RedPajama-V1/V2 + RedPajama-INCITE（Together AI, 2023 / 2024-11 成文）

### RedPajama-V1（LLaMA-1 训练语料的开放复刻）
- **总量**：**1.2T token**，7 个域（精确 token 数）：
  - **CommonCrawl 878B · C4 175B · GitHub 59B · ArXiv 28B · Books 26B · Wikipedia 24B · StackExchange 20B**。
- **数据处理**：严格复刻 LLaMA 描述：
  - CommonCrawl：选 5 个英文快照（2019-30/2020-05/2021-04/2022-5），过 **CCNet pipeline**（分片去重 + 困惑度桶），再用 Wikipedia 引用页训 **fastText 一元分类器**，过滤掉分数 <0.25 的文档。
  - C4：直接纳入（提供另一版 CommonCrawl 处理）。
- 衍生：**SlimPajama**（对 V1 进一步清洗+去重）；Dolma/Zyda 也复用其 ArXiv/StackExchange 等切片。

### RedPajama-INCITE-3B/7B（与 ORNL 合作，Summit 超算）
- **架构**：decoder-only（GPT-NeoX/Pythia 风格 dense）。
- **训练算力**：**Oak Ridge Summit 超算**（4608 个 6×V100 节点）；**7B 用 512 节点=3072 GPU，3B 用 256 节点=1536 GPU**。
- **并行**：7B 用 **12-way PP + 2-way TP**；3B 用 **6-way PP + 2-way TP**。
- **精度**：**fp16**（Summit V100 不支持 BF16——作者认为这是 7B 落后原版 LLaMA-7B 的部分原因）。
- **batch/token**：global batch **4M token**；**3B 训 800B token，7B 训 1.001T token**；LR 线性 warmup 后线性衰减（匹配 LLaMA 设置）。
- **SFT/对齐**：放出 Instruct 与 Chat 版（INCITE-Instruct / INCITE-Chat），指令微调；无 RLHF 细节披露。

### RedPajama-V2（web-only 巨型语料，2024-11 论文）
- **总量**：**100T+ token**（其中带质量信号的子集约 50T），**5 种语言**（英、德、法、西、意）。
- **来源**：CommonCrawl **84 个月度快照（2014—2023-04）**，过 **CCNet pipeline**。
- **质量信号（40+ 个，随文档发布，供用户自行过滤）**：
  - **自然语言类**（剔除 JS/菜单/样板）、**重复度类**、**内容类**（如是否命中 UT1 黑名单 NSFW 域）、**ML 启发式类**（fastText 分类器 + importance weights，target=Wikipedia/参考链接等高质量域 vs source 的对数似然比）。
  - **去重**：包含**不同相似度档的 MinHash 签名（模糊去重）** + **Bloom filter（精确去重，FPR 见论文）** 的文档 ID（精确去重基于 .wet 文档哈希，在过滤前完成）。
- **消融**：用 468M（24 层/16 头）/1.6B dense（Llama-2 架构，seq 2048）模型验证质量信号价值。

### 来源
- RedPajama-Data 论文 arXiv https://arxiv.org/abs/2411.12372 · PDF https://arxiv.org/pdf/2411.12372 · 本地 `../../../sources/llm/deep-dive/redpajama-data-2411.12372.pdf`
- GitHub https://github.com/togethercomputer/RedPajama-Data
- INCITE 官方博客 https://www.together.ai/blog/redpajama-models-v1 · 本地（HTML 快照）`../../../sources/llm/2023/redpajama-incite-together.html`

---

## RefinedWeb + Falcon-7B/40B/180B（TII, 2023-06 / 2023-11）

### RefinedWeb 数据集（MacroData Refinement, MDR pipeline）
- **核心论点**：**仅用过滤+严格去重的 web 数据，即可媲美 curated 数据**（挑战"必须精选语料"的共识）。
- **规模**：目标 **3–6T token（英文）**，公开 **600B token extract**。
- **MDR pipeline 三大块**（从 CommonCrawl WARC 起，最终约**移除 90% 文档**）：
  1. **文档准备**：URL 过滤（**4.6M 域名聚合黑名单 + URL 评分**，屏蔽成人/常见高质量来源以免污染）→ 用 **warcio + trafilatura** 从 WARC 抽正文 → **fastText 语言识别**。
  2. **过滤**：document-wise 启发式规则（借鉴 Gopher/CCNet）+ **line-wise 逐行修正**（去广告/导航等）。
  3. **去重**：**模糊去重 MinHash（5-gram，20 桶 × 450 hashes）≈ 移除 50%** + **精确子串去重（后缀数组）** + URL 去重。

### Falcon 模型架构（逐尺寸，Table 16）
| | Falcon-7B | Falcon-40B | Falcon-180B |
|---|---|---|---|
| 层数 | 32 | 60 | 80 |
| dmodel | 4544 | 8192 | 14848 |
| head_dim | 64 | 64 | 64 |
| 查询头 nq | 71 | 128 | 232 |
| KV 头 nkv | **1（MQA）** | **8（multigroup/GQA）** | **8** |
| vocab | 65,024 | 65,024 | 65,024 |
| ctx | 2048 | 2048 | 2048 |
- **结构创新**：**multiquery → multigroup attention**（nkv=TP，便于张量并行下的 K,V-cache 缩减）；**parallel attention + 双 LayerNorm**（7B 后改单 LN）；**RoPE**；tied embeddings；无 dropout；激活=GeLU（实验后未采用 SwiGLU，认为对 cost-efficient 训练不划算）。

### Falcon 训练细节
- **token / 算力（Table 1）**：
  - 7B：**1,500B token** · 730 PF-days · **384×A100-40GB**
  - 40B：**1,000B token** · 2,800 PF-days · **384×A100-40GB**
  - 180B：**3,500B token** · 43,500 PF-days · **4,096×A100-40GB**（迄今公开记录最大的训练 run 之一）
- **优化器/LR/batch（Table 16）**：AdamW（融合内核），**WD 0.1**；LR **6e-4 / 1.85e-4 / 1.25e-4**（7/40/180B，cosine÷10）；ramp-up 4B token；global batch **2304 / 1152 / 2048**；**batch-size warm-up 30B(7B) / 100B(40&180B)**；gradient clipping **1.0 / 0.6 / 0.4**；**z-loss=1e-4** 助稳定。
- **并行（Table 16）**：7B TP=1/PP=1/DP=192；40B **TP=8/PP=2/DP=192**；180B **TP=8/PP=8/DP=64**。
- **精度**：BF16 混合精度。
- **自研 infra "Gigatron"**：基于 PyTorch 的专有训练框架，**3D 并行 + ZeRO 优化器分片**；在 **AWS p4d（8×A100-40GB/节点，50Gbps/GPU EFA）** 上训练，**直接从 S3 流式读数据**（无分布式文件系统）；选 40GB A100 因可用性/性价比更高（4×A100 节点因 TP 度受限吞吐更低）。

### Falcon SFT / RL
- Falcon-1 系列主放 base + Instruct 微调（Falcon-7B/40B-Instruct，在对话/指令混合数据上 SFT）；无官方 RLHF/DPO 细节。

### Falcon 数据混合
- 主体 RefinedWeb；可掺 5–10% 代码/多语而不显著损英文（消融结论）。

### 来源
- RefinedWeb 论文 arXiv https://arxiv.org/abs/2306.01116 · PDF https://arxiv.org/pdf/2306.01116 · 本地 `../../../sources/llm/deep-dive/refinedweb-2306.01116.pdf`
- Falcon series 论文 arXiv https://arxiv.org/abs/2311.16867 · PDF https://arxiv.org/pdf/2311.16867 · 本地 `../../../sources/llm/deep-dive/falcon-series-2311.16867.pdf`
- HF 数据集 https://huggingface.co/datasets/tiiuae/falcon-refinedweb · 模型 https://huggingface.co/tiiuae

---

## The Stack v1/v2 + StarCoder / StarCoder2（BigCode, 2022-11 / 2023-05 / 2024-02）

### The Stack 数据集
- **v1（2022-11）**：3.1TB 许可宽松源码，30 语种（首发）；治理框架含 **"Am I in The Stack" 工具 + opt-out 流程**。
- **v1.2（StarCoder 用）**：**6.4TB / 358 语种**（含 54GB GitHub issues）。
- **v2（2024-02，与 Software Heritage 合作）**：构建于 SWH Merkle-DAG 全去重存档，**619 语种、原始 67.5TB（10× v1）**。

### StarCoder / StarCoderBase-15.5B
- **架构**：**40 层 · hidden 6144 · intermediate 24576 · 48 头 · Multi-Query-Attention(MQA)**；max-pos/ctx **8192**；**vocab 49152**（byte-level BPE，含 sentinel/FIM token）；**GPTBigCode** 架构；支持 **FIM（Fill-in-the-Middle）**。
- **数据**：The Stack v1.2，**80+ 编程语言 + GitHub issues/commits/Jupyter**；**StarCoderBase=1T token**；**StarCoder=在此基础上 +35B Python token（2 epoch，LR 5e-5）**。
- **数据处理（代码专用）**：
  - 语言选择：从 358 语种选 86（>2MB 才入，Swift 因数据量排除）。
  - **近去重**：对所有源码文件算 **MinHash + LSH**，Jaccard 阈值 **0.85** 聚类去重。
  - **PII**：自建 **StarPII** 检测模型（先收 PII 标注数据集训 NER），脱敏 names/emails/keys 等。
  - opt-out：处理时已有 44 人退出（v1.2）。
- **训练**：250k 步，**global batch 4M token**（512 seq × 8192），总 1T token；Adam(β=0.9/0.95, ε=1e-8)，**WD 0.1**；LR **3e-4 → 3e-5 cosine**（线性 warmup）。**512×A100-80GB / 64 节点**；**3D 并行（TP+PP rank 4 → 16 GPU/副本）**；**BF16**（明知比 fp16 慢 10% 仍用以避不稳定，因 Megatron 分布式优化器要求 FP32 梯度规约）。

### StarCoder2-3B/7B/15B（Table 6/7）
| | SC2-3B | SC2-7B | SC2-15B |
|---|---|---|---|
| hidden | 3072 | 4608 | 6144 |
| n_heads | 24 | 36 | 48 |
| n_kv_heads | **2(GQA)** | **4(GQA)** | **4(GQA)** |
| 层数 | 30 | 32 | 40 |
| vocab | 49152 | 49152 | 49152 |
| ctx | base 4k→long 16k | 同 | 同 |
| RoPE θ | 1e5 | 1e5 | **1e4（配置解析 bug）** |
| batch | 2.6M | 3.5M | 4.1M |
| token | **3.1T** | **3.5T** | **4.1T** |
| epoch | 4.98 | 5.31 | 4.49 |
| FLOPs | 5.94e22 | 1.55e23 | 3.87e23 |
- **结构**：**GQA**（KV 头压到 2/4/4 以降推理开销）；**RoPE**；**FIM = repo-context file-level**（仓库 50% 概率成 FIM 候选，再 50% 概率对 chunk 施加 FIM）。
- **训练**：Adam(0.9/0.95) WD 0.1 无 dropout；LR 3e-4 cosine（1000 步 warmup）；按 Muennighoff 结论**重复数据 ~4–5 epoch**。
- **长上下文阶段**：base 用 4096 训完后，**再训 200B token，ctx=16384、滑动窗口 4096、FlashAttention-2、增大 RoPE θ**。
- **算力**：A100-SXM4-80GB（base 累计 97,120 GPU 时；亦有部分 H100 计算 145,152 时）。
- **The Stack v2 处理**：去重（MinHash+LSH）、PII 脱敏、**benchmark 去污染**、**malware 移除**、opt-out 删除（截止后删 1,561 个仓库）；HTML/网页类源用 MinHash-LSH 阈值 0.7 去近重。

### StarCoder SFT/对齐
- 主放 base；社区有 StarChat 等微调，但官方 BigCode 报告未含 RLHF/DPO。

### 来源
- The Stack v1 论文 arXiv https://arxiv.org/abs/2211.15533 · PDF https://arxiv.org/pdf/2211.15533 · 本地 `../../../sources/llm/deep-dive/the-stack-2211.15533.pdf`
- StarCoder 论文 arXiv https://arxiv.org/abs/2305.06161 · PDF https://arxiv.org/pdf/2305.06161 · 本地 `.../deep-dive/files/starcoder-2305.06161.pdf`
- StarCoder2 + The Stack v2 论文 arXiv https://arxiv.org/abs/2402.19173 · PDF https://arxiv.org/pdf/2402.19173 · 本地 `.../deep-dive/files/starcoder2-2402.19173.pdf`
- GitHub https://github.com/bigcode-project · HF https://huggingface.co/bigcode

---

## MAP-Neo-2B/7B（M-A-P, 2024-05）— 全栈全开中英双语

### 架构细节（Table 5）
| | MAP-Neo 2B | MAP-Neo 7B |
|---|---|---|
| 层数 | 18 | 28 |
| 头数 | 8 | 16 |
| dmodel | 2048 | 3072 |
| FFN dims | 16384 | 24576（=8×dmodel） |
| KV 头 | **1（MQA）** | **16（MHA）** |
- **位置/激活/Norm**：**RoPE + SwiGLU + RMSNorm**（每个 sub-layer 都归一化）。
- **上下文**：**8192**。
- **tokenizer**：BPE（基于 SentencePiece 实现），**vocab 64000**，max sentence-piece 长度限 16（改善中文）；给代码/数学/高质量数据更高采样权重；max length 截到 64K。

### 预训练数据（Matrix Data Pile）
- **总量**：7B 训于 **4.5T 高质量 token**。
- **构成**：**52.55% Common Crawl · 22.29% 编程代码 · 其余=学术论文/书籍/印刷材料**。英文 web 子集主要取自 **RedPajama-V2** 的英文内容。

### 数据处理 pipeline
- **抽取**：自建稳定 **OCR 系统**（公式用 Pix2Text/TrOCR，文档用 PP-OCRv4），含 OCR 后处理（重接断句、修复 Markdown 数学公式）。
- **去重**：
  - 英文：用 **Spark**；**精确文档去重 + MinHash LSH 模糊去重**（n-gram 构集）；逐行（similar-line）去重。
  - 中文：**精确文档去重 + MinHash LSH + Bloom Filter（FPR=0.001）** + 相似行去重。
- **质量过滤**：英/中各一套**启发式规则**（详见附录 A.1/A.2，如归一化后字符数/词数 [50,10000] 等阈值）+ 结合标注。
- **数据召回（DeepSeek-Math 风格）**：以高质量数据为正例、随机 CC 为负例训 **FastText 二分类器**，对 CC 打分按置信度从高到低保留，对识别率>10% 的域回访补样，迭代扩充正例。

### 数据配比 / 阶段（两阶段预训练）
- **Fundamental Phase（基础阶段）**：通用大语料获取通用能力；**两段式 LR**：warmup 从 2e-5 线性升到峰值 **2e-4（2k 步）** → cosine 衰减回 2e-5（约 365k 步）。
- **Decay Phase（退火阶段）**：随 **Stack V2** 发布纳入高质量指令数据；**处理约 778B token**；**代码占比从 14.77% 提到 17.04%**；LR 从某点起按 MiniCPM 风格衰减；此阶段也修正了 tokenizer 早期缺陷（改善代码指标）。

### 训练细节
- **算力**：**512×NVIDIA H800 / 64 节点**（双 Intel Xeon + 8×H800/节点），NCCL 后端；minipod ≥512 H800 互联。
- **batch/序列**：seq 8192，batch 512。
- **框架**：改进版 **Megatron-LM**（增强分布式鲁棒性）。
- 附 scaling law 研究（Chinchilla/OpenAI/自提方法拟合）。

### SFT 细节（两阶段）
- **Foundational Phase**：**2M+ 条指令数据**，3 epoch，batch 4096 起（含全量 OpenHermes-2.5（剔 TheoremQA 防泄漏）+ 全量 Code-Feedback + WebInstructSub 子集），强化代码/数学基础。
- **Chat Phase**：**100k+ 真实多轮对话** 1 epoch（再混 5k 数学/代码以保基础能力），提升 MT-Bench/AlpacaEval。
- 模板：next-token，**对 system/user 输入加 loss mask**；seq 8192，AdamW。

### RL / 对齐细节
- **Iterative DPO（迭代式 DPO）**：从 SFT 模型起，用偏好对 (yw, yl) 直接 MLE 优化；**3 轮迭代**，AlpacaEval LC 胜率逐轮提升（9.77 → 10.02 → 15.59 → 16.65）。无 PPO/RM。

### AI infra
- 全开：数据 curation/cleaning 代码（中英）、Matrix Data Pile 语料、tokenizer/base/SFT/对齐训练码、改进的 Megatron-LM、评测码、中间检查点。

### 来源
- arXiv https://arxiv.org/abs/2405.19327 · PDF https://arxiv.org/pdf/2405.19327 · 本地 `../../../sources/llm/deep-dive/mapneo-2405.19327.pdf`
- 项目页/GitHub https://github.com/multimodal-art-projection/MAP-NEO

---

## OpenCoder-1.5B/8B（INF / M-A-P 等, 2024-11）— 完全可复现代码 LLM

### 架构细节（Table 4）
| | OpenCoder-1.5B | OpenCoder-8B |
|---|---|---|
| 层数 | 24 | 32 |
| dmodel | 2240 | 4096 |
| 头数 | 14 | 32 |
| KV 头 | **14（MHA）** | **8（GQA，近 Llama-3.1-8B）** |
| 激活 | SwiGLU | SwiGLU |
| vocab | 96640 | 96640 |
| RoPE θ | 10000 | **500000** |
| ctx | 4096 | 8192 |

### 预训练数据（RefineCode + 召回文本）
- **RefineCode**：**960B token、607 种编程语言**，含 **130+ 语言专属规则**及定制权重。
- 另含从 CommonCrawl/FineWeb/Skypile 召回的代码相关文本（用同款召回 pipeline）。8B 额外用了 code-related recall 数据（1.5B 因数据未完工而缺）。
- 退火阶段加入 **Algorithmic Corpus（算法题代码，强逻辑低依赖）** + **合成数据**。

### 数据处理 pipeline（代码专用，激进 file-level 去重）
- **预处理 → 去重 → 转换 → 过滤 → 重组**；保留 607 种语言文件。
- **去重（优先且激进，file-level 优于 repo-level）**：
  - **精确去重**：GitHub 中约 **75% 文件完全重复**，先做精确去重。
  - **模糊去重**：5-gram 切片，算 **2048 个 MinHash 函数**（沿用通用 pipeline 的 LSH 设置）。
  - 结论：repo-level 去重保留的 token 约是 file-level 的 3 倍，但其中 ~68.4% 可进一步去重，且 file-level 性能更好；chunk-level 去重无额外收益。
- **PII 脱敏**：复杂正则检测 passwords/emails/IP，替换为占位符。
- **质量过滤**：自然语言过滤规则 + 针对 607 语言各自属性的过滤；fastText 模型用于代码 vs 非代码召回。

### 数据配比 / 阶段（含退火）
- **通用预训练 + 快速 LR 退火（annealing）阶段**：退火阶段从原分布重采 RefineCode，并加入 Algorithmic Corpus 与合成数据（高质量代码片段、知识改写——CodeExercises 思路，强 LLM 以算法语料为种子合成，T=1.0）。

### 训练细节
- **LR schedule = WSD（Warmup-Stable-Decay，MiniCPM 风格）**：warmup 2000 步/8B token，峰值 LR **3e-4** 恒定，退火期指数衰减到 **1e-5**。
- **1.5B**：训于 **2.0T token（4 epoch）+ 100B 退火**；micro-batch 4 / global batch 1024；**256×H800 / 109.5 小时 = 28,034 GPU 时**；前 130k 步 seq=4096/batch=2048。
- **8B**：训于 **2.5T token（3.5 epoch）+ 100B 退火**；micro-batch 1 / **TP=2** / seq 8192 / global batch 1024；**512×H100 / 187.5 小时 = 96,000 GPU 时**。
- **框架**：**Megatron-LM**（distributed optimizer + DDP gradient overlap）。

### SFT 细节（两阶段指令微调）
- **Stage 1**：1 epoch，batch **4096**，LR **2e-5**，warmup 100 步，cosine（大规模多样指令合成数据：先用 LLM 清洗无关上下文，再模板化生成多样 prompt）。
- **Stage 2**：3 epoch，batch **512**，LR **5e-5**，warmup 100 步，cosine（高质量代码 SFT 数据）。
- 结论：两阶段指令微调显著优于单阶段。

### RL / 对齐
- 官方报告主述 SFT；未含 RLHF/DPO（OpenCoder 重点在数据+SFT 全开）。

### AI infra
- 全开：数据清洗/去重代码、RefineCode 数据、大规模 SFT 语料、中间检查点、训练代码。

### 来源
- arXiv https://arxiv.org/abs/2411.04905 · PDF https://arxiv.org/pdf/2411.04905 · 本地 `../../../sources/llm/deep-dive/opencoder-2411.04905.pdf`
- 项目页 https://opencoder-llm.github.io · GitHub https://github.com/OpenCoder-llm/OpenCoder-llm

---

## DataComp-LM / DCLM（多方：UW/Apple/TRI/AI2 等, 2024-06）

### 定位
- **数据中心化测试平台**：固定训练配方与评测，只让参赛者改"数据"，从而隔离"数据质量"这一变量。证明 **model-based filtering（基于模型的过滤）是组装高质量训练集的关键**。

### 数据集 / 池
- **DCLM-Pool**：**240T token**（从 CommonCrawl 抽取，迄今最大公开池）。
- **DCLM-Baseline**：过滤后 **3.8T token** 的基线集。
- **竞赛尺度**：412M / 1.4B / 2.8B / 6.9B / 6.9B-2x，对应训练 token 8.2B / 28.8B / 55.9B / 138B / 276B（FLOPs=6ND），用 OpenLM 框架报 H100 卡时。

### DCLM-Baseline 数据处理 pipeline（关键消融结论）
- **正文抽取**：用 **resiliparse**（比 WET 文件好 ≥2.5 分 CORE；与 trafilatura 效果相当但**快 8 倍**）。
- **启发式过滤**：采用 **RefinedWeb 的启发式质量过滤器**。
- **去重**：DCLM-Baseline 用 **Bloom filter**（消融用 MinHash / 后缀数组）。
- **基于模型的过滤（最关键）**：对比 PageRank/SemDedup/AskLLM/多种 fastText 后，选 **fastText 分类器（正例=OpenHermes-2.5 指令 + r/ELI5；负例=随机 CC）**；用**严格阈值保留 top-10% 文档**（比启发式过滤多 +3.5 分 CORE）。结果即 DCLM-Baseline。

### 基线模型架构（DCLM-Baseline-7B，Table 10）
- **decoder-only（类 Llama / GPT-2，OpenLM 实现）**：**32 层 · dmodel 4096 · 32 头 · head_dim 128**（dense）。
- **tokenizer**：**GPT-NeoX**（作者注：多数实验只用了这一个 tokenizer）。
- **上下文**：预训练 2048，后**继续学习扩到 8192**。
- **逐尺度超参（Table 10）**：
  - 400M-1x：24 层/8 头/1024 维，warmup 2000，LR 3e-3，WD 0.033，z-loss 1e-4，batch 512
  - 1B-1x：24 层/16 头/2048 维，warmup 5000，LR 3e-3，WD 0.033，z-loss 1e-4，batch 256
  - 3B-1x：32 层/32 头/2560 维，warmup 5000，LR 3e-3，WD 0.033，z-loss 1e-4
  - 7B：32 层/32 头/4096 维，warmup 5000，LR 2e-3，WD 0.05，z-loss 5e-6

### 训练细节
- **优化器**：Adam；**z-loss**（鼓励 logit 量级，Chowdhery 风格）助稳定；用 cooldown=3e-5；LR/WD 经 sweep（最终 7B 用 LR 3e-4 / WD 0.33 训长 run；Table 11 sweep）。
- **最终成绩**：**DCLM-Baseline 7B 训 2.6T token → MMLU 5-shot 64%**（开放数据 SOTA），与 Mistral-7B-v0.3(63%)/Llama-3-8B(66%) 相当但**算力少 6.6×**；比 MAP-Neo 高 6.6pt 且少 40% 算力；7B 训 280B token 即比 Llama-2-7B 高 5pt MMLU 且少 7× 算力。
- **算力**：OpenLM + H100（逐尺度卡时见 Table 1）。

### AI infra
- 框架：**OpenLM**（开源预训练框架）；公开 240T 池、过滤模型、训练/评测全代码（53 项下游评测套件）。

### 来源
- arXiv https://arxiv.org/abs/2406.11794 · PDF https://arxiv.org/pdf/2406.11794 · 本地 `../../../sources/llm/2024/2406.11794.pdf`
- 项目页 https://www.datacomp.ai/dclm/ · GitHub https://github.com/mlfoundations/dclm

---

## 附：Falcon 3（TII, 2024-12，开放权重，数据未全开）

> 列于此仅补全 Falcon 谱系；其预训练**数据未全公开**，严格说不属"数据全开"族。仅记官方博客披露的配方要点。

- **家族**：Falcon3-1B/3B/7B/10B-Base + Falcon3-**Mamba-7B**-Base（纯 SSM）。decoder-only，**transformer 变体与 Llama 架构兼容**。
- **预训练**：**对 7B 做单次大规模预训练，用 1024×H100，14T token**（web/code/STEM/curated/多语）。
- **关键技巧**：
  - **Depth up-scaling**：把 7B 复制冗余层升到 **10B**，再用 **2T 高质量 token** 续训 → Falcon3-10B-Base。
  - **剪枝 + 知识蒸馏**：用 **<100GT** 高质量数据得到 1B/3B-Base（高 pre-training 效率）。
  - **Mamba-7B**：在原 Falcon-Mamba-7B 上再训 **1.5T 高质量 token**，支持 **32K 上下文**。
- **架构特征**：**head_dim 256**（为 FlashAttention-3 优化吞吐）；transformer 18–40 层、Mamba 64 层；**SwiGLU**；**vocab 131K（Mamba-7B 为 65K）**；ctx 最高 32K（1B 为 8K）。
- **来源**：官方 HF 博客 https://huggingface.co/blog/falcon3 · 官方站 https://falcon-lm.github.io/blog/falcon-3/ · HF 组织 https://huggingface.co/tiiuae

---

## 全家族横向洞察（要点）

- **"全开"的两条腿**：模型全开（权重+码+ckpt：GPT-NeoX/Pythia/MAP-Neo/OpenCoder/StarCoder/INCITE）与**数据集全开**（Pile/ROOTS/RefinedWeb/Stack/RedPajama/DCLM）。后者是这条线真正的护城河。
- **位置编码演进**：ALiBi（BLOOM）→ RoPE 成主流（NeoX/Pythia/Falcon/StarCoder2/MAP-Neo/OpenCoder/DCLM）。
- **注意力演进**：MHA → MQA（Falcon-7B/StarCoder/MAP-Neo-2B）→ multigroup/GQA（Falcon-40&180B/StarCoder2/OpenCoder-8B），全为推理期 K,V-cache 缩减。
- **去重是 web 数据的灵魂**：MinHash-LSH（几乎人人用）+ 精确去重（后缀数组 / Bloom filter）。RefinedWeb 把去重做到"移除 90% 文档"的极致；代码侧 OpenCoder/StarCoder 强调 **file-level 去重 > repo-level**。
- **过滤范式迁移**：纯启发式（Pile/ROOTS/RefinedWeb 启发式部分）→ **基于模型的分类器过滤（fastText）成胜负手**（DCLM 的核心论点，MAP-Neo/OpenCoder 也用召回式 fastText）。
- **训练精度**：早期 fp16（NeoX/INCITE，硬件所限）→ A100/H 时代 BF16（BLOOM/Falcon/StarCoder）。
- **退火/WSD 的兴起**：早期单 epoch、cosine（NeoX/BLOOM/Pythia）→ 2024 起多阶段 + 退火/WSD + 高质量数据上采样（MAP-Neo decay phase、OpenCoder WSD、DCLM cooldown）。
- **对齐深度**：早期几乎只有 base/SFT（NeoX/Pythia/StarCoder/Falcon-1/RedPajama 多为 base）；到 MAP-Neo 出现完整 **SFT 两阶段 + Iterative DPO**；这一族整体**未见 PPO/GRPO/RLVR**（reasoning-RL 是更晚的 Qwen/Llama/OLMo 等谱系的事）。
- **infra 自研**：Falcon 的 Gigatron（AWS p4d + S3 流式 + 3D 并行/ZeRO）是"云上训百亿"的代表；BLOOM/NeoX/StarCoder/MAP-Neo/OpenCoder 多基于 Megatron(-DeepSpeed)；DCLM/RedPajama-消融用 OpenLM。
