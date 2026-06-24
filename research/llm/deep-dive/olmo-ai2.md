---
title: "OLMo / Dolma / Tülu 家族训练配方深挖（AI2 / Allen Institute for AI）"
type: source
tags: [OLMo, OLMo2, OLMo3, OLMoE, Dolma, Tulu, Tulu3, RewardBench, RLVR, OlmoRL, 全开放模型, AI2, allenai]
created: 2026-06-18
updated: 2026-06-18
family: OLMo/Dolma/Tülu (AI2)
note: 全部数字均摘自官方一手技术报告/arXiv/官方博客/GitHub/HF 官方组织页；查不到的明确标注"官方未公开"。
---

# OLMo / Dolma / Tülu 家族训练配方深挖（AI2）

> AI2（Allen Institute for AI，allenai）的"全开放"路线：不只放权重，而是把**数据 + 配方 + 代码 + 训练日志 + 中间检查点 + 评测**全部公开（"model flow / 全生命周期"）。本档案逐型号抠原文数字。
>
> **本家族最透明，几乎每一个数字都能在官方报告里找到。** 下面凡未标"官方未公开"的，均来自原文表格/正文。

---

## 家族演进脉络（时间线）

- **Tülu 1 (2023-06, "How Far Can Camels Go?")** — 横评 12 个开源指令数据集，发 LLaMA 基座的 Tülu，立开源后训练基准 + open-instruct 框架。
- **Tülu 2 / Tülu 2-DPO (2023-11, "Camels in a Changing Climate")** — Llama-2 基座，较早证明 DPO 可扩到 70B；UltraFeedback 偏好。
- **Dolma (2024-01)** — 3T token 开放英文预训练语料 + 开源 Rust curation 工具包，OLMo 的数据基础。
- **OLMo / OLMo 1 (2024-02)** — 首个"全开放"dense LM（1B / 7B），decoder-only，Dolma 训练。
- **RewardBench (2024-03)** — 首个系统评测 RLHF 奖励模型的基准 + 排行榜。
- **OLMo 0424 (2024-04)** — OLMo 中间迭代（改数据混合 + QKV clipping + 上下文 2048→4096）。
- **OLMoE-1B-7B (2024-09)** — 首个全开放稀疏 MoE（1.3B 激活 / 6.9B 总参，64 专家 top-8）。
- **Tülu 3 (2024-11)** — 全开放前沿后训练配方（Llama 3.1 基座 8B/70B/405B）；首次系统提出 **RLVR**（可验证奖励 RL），确立 SFT→DPO→RLVR 三段式。
- **OLMo 2 (2024-11 / 2501.00656)** — dense 7B/13B（后续 32B 0325、1B），稳定性架构（RMSNorm reorder + QK-Norm + Z-loss）、两阶段预训练（olmo-mix-1124 + Dolmino mid-train）、套用 Tülu 3 后训练。
- **OLMoE-1B-7B-0125 (2025-01)** — OLMoE 退火升级版（用 Dolmino 100B 退火）。
- **OLMo 2 32B (2025-03, 0325)** — 加入 GQA 的 32B；32B Instruct 用 GRPO 做 RLVR。
- **OLMo 3 (2025-11 / 2512.13961)** — 旗舰 7B/32B，Base/Think/Instruct/RL-Zero 四变体；Dolma 3 数据（6T）、SWA + YaRN 长上下文 65K、Delta Learning DPO、**OlmoRL**（GRPO+DAPO+Dr GRPO，4x 提速）。**Olmo 3.1 Think 32B 号称迄今最强全开放思考模型。**

---

## 各代关键参数对比（dense / MoE 主线）

| 型号 | 规模 | 层数 | 隐藏维 | 头(Q/KV) | 注意力 | 上下文 | RoPE θ | norm | 训练 token | tokenizer/vocab |
|---|---|---|---|---|---|---|---|---|---|---|
| OLMo 1B | 1B dense | 16 | 2048 | 16/16 | MHA | 2048 | 10k | 非参数 LayerNorm(输入) | 2T | GPT-NeoX 改 / 50,280(emb 50,304) |
| OLMo 7B | 7B dense | 32 | 4096(报告写 4086 疑笔误) | 32/32 | MHA | 2048 | 10k | 非参数 LayerNorm(输入) | 2.46T | GPT-NeoX 改 / 50,280 |
| OLMoE-1B-7B | 1.3B激活/6.9B总 | 16 | 2048 | 16/16 | MHA + MoE | 4096 | 10k | RMSNorm + QK-Norm | 5.133T(1.3 epoch) | GPT-NeoX 改 / 50,304 |
| OLMo 2 1B | 1B dense | 16 | 2048 | 16/16 | MHA | 4096 | 5e5 | RMSNorm(输出, reorder)+QK-Norm | 4T(+50B mid) | cl100k 改 / ~100k |
| OLMo 2 7B | 7B dense | 32 | 4096 | 32/32 | MHA | 4096 | 5e5 | 同上 | 4.05T(3.90T 预训) | cl100k 改 |
| OLMo 2 13B | 13B dense | 40 | 5120 | 40/40 | MHA | 4096 | 5e5 | 同上 | 5.6T(5T 预训) | cl100k 改 |
| OLMo 2 32B | 32B dense | 64 | 5120 | 40/8 | GQA | 4096 | 5e5 | 同上 | 6.6T(6.06T 预训) | cl100k 改 |
| OLMo 3 7B | 7B dense | 32 | 4096 | 32/32 | MHA + SWA(4096,3/4层) | 65K(扩展后) | 5e5 + YaRN(全注意层) | RMSNorm(输出)+QK-Norm | 5.93T 预训(+100B mid +50B 长ctx) | cl100k 改(同 OLMo 2) |
| OLMo 3 32B | 32B dense | 64 | 5120 | 40/8 | GQA + SWA | 65K | 5e5 + YaRN | 同上 | 5.5T 预训(+100B×2 mid +100B 长ctx) | cl100k 改 |

> 后训练系列(Llama 基座，非 AI2 预训练): **Tülu 1** LLaMA 6.7B/13B/30B/65B；**Tülu 2/2-DPO** Llama-2 7B/13B/70B；**Tülu 3** Llama 3.1 8B/70B/405B。

激活/norm 通用项：全家族 **SwiGLU**、**RoPE**、**无 bias**；OLMo 1/0424 用非参数 LayerNorm，OLMo 2 起改 RMSNorm + reorder(归一化放子层输出) + QK-Norm + Z-loss(权重 1e-5)。

---

## OLMo 1（OLMo: Accelerating the Science of Language Models, 2024-02, arXiv 2402.00838）

### 架构
- decoder-only Transformer，发 **1B 与 7B**（7B 有 4 个不同架构/优化器/硬件的变体；1B 一个）；所有发布模型至少训 2T token。
- **无 bias 项**（跟 LLaMA/PaLM）。
- **非参数 LayerNorm**（无 affine gain/bias）—— 作者称是当时最稳且最快的选择（对比过参数 LayerNorm 和 RMSNorm）。
- **SwiGLU**，FFN 隐藏维 ≈ (8/3)d，向上取 128 倍数（7B = 11,008；因门控实际输入维 2×11,008 = 22,016）。
- **RoPE**（替代绝对位置编码）。
- **tokenizer**：改版 GPT-NeoX-20B BPE，加 PII 屏蔽 token（电话/邮箱/IP）；vocab = **50,280**，embedding 矩阵补到 **50,304**（128 倍数）。
- 1B：16 层 / d=2048 / 16 头；7B：32 层 / d=4096(表写4086) / 32 头。
- weight tying：1B 是 yes，7B 是 no。

### 预训练数据（Dolma 2T 采样）
- 7B 训到 **2.46T token**（Dolma 单 epoch 约 2T，部分模型跑第二 epoch 不同 shuffle）。
- Dolma 构成（GPT-NeoX 计 token）：Common Crawl 2,180B / GitHub(The Stack) 342B / Reddit 80B / Semantic Scholar(peS2o) 57B / Gutenberg 5.2B / Wikipedia 3.7B，合计 **2,668B**（论文 Dolma 表）。
- 每来源单独保存（curation 与发布都分开）。

### 训练细节
- 框架：**ZeRO**（DeepSpeed 风格）经 **PyTorch FSDP** 分片权重+优化器态。
- 精度：混合精度（FSDP + AMP），softmax 等关键算子 FP32，其余 bfloat16；本地分片权重/优化器态保 FP32，前后向时才 cast bf16；梯度 FP32 reduce。
- global batch ≈ **4M token**（2048 条 × 2048 序列长），7B 单 GPU micro-batch 4096 token。
- 优化器 **AdamW**（β 0.9/0.95，ε 1e-5）；7B peak LR 3e-4 / 1B 4e-4；warmup 5000 步(~21B token，1B 2000 步)，之后线性衰减到 peak 的 1/10；warmup 后梯度裁剪 L2 norm ≤ 1.0。
- 末尾再 1000 步把 LR 线性降到 0 提升性能。
- 硬件（两套验证跨厂商可移植）：
  - **LUMI**：最多 256 节点 × 4 AMD MI250X(128GB)，800Gbps 互联。
  - **MosaicML/Databricks**：27 节点 × 8 NVIDIA A100(40GB)，800Gbps。
- 环境影响（旧报告）：OLMo 7B 104 MWh，碳 70t。

### 后训练（适配）
- 走 **TÜLU 数据与流程**：先指令微调（蒸馏+人写指令混合），再 **DPO**（蒸馏偏好数据）。完整 chat/safety 评测见原文 §4.3。
- 评测栈：Catwalk(下游) + Paloma(困惑度，585 域) + TÜLU eval(适配)。OLMo-7B 是当时最大做 Paloma 显式去污染的模型。

---

## OLMoE-1B-7B（OLMoE: Open Mixture-of-Experts Language Models, 2024-09, arXiv 2409.02060）

### 架构（首个全开放稀疏 MoE）
- decoder-only，FFN 换成 MoE 模块：**64 个细粒度小专家，每 token 选 top-8**。
- **激活参数 1.3B / 总参数 6.9B**（vocab 参数 103M）。
- **无共享专家**（实验表明共享专家无效）。
- 路由：**dropless token-choice**（无 token drop；token-based 优于 expert-based）。
- **不用 sparse upcycling**（从 dense 升 MoE 仅在小算力预算下有限有益）。
- 两个辅助损失：**load balancing loss(权重 0.01) + router z-loss(权重 0.001)**，与 CE 线性相加：L = L_CE + 0.01·L_LB + 0.001·L_RZ。
- 16 层 / d=2048 / **FFN 维仅 1024**(每专家) / 16 头 / vocab 50,304 / **QK-Norm + RMSNorm**(eps 1e-5) / RoPE θ 10,000 / 序列长 4096 / weight tying no。
- 初始化：截断正态 std 0.02，截断 ±0.06(±3σ)；AdamW ε 降到 **1e-8**（比 OLMo 的 1e-5 收敛更快）。

### 预训练数据（OLMoE-MIX，4.06T 池）
- DCLM-Baseline(web) 3,860B / StarCoder(code) 101B / peS2o 57.2B / arXiv 21.1B / OpenWebMath 12.7B / Algebraic Stack 12.6B / Wikipedia 3.69B（GPT-NeoX 计 token，合计 ~4,060B）。来自 DCLM + Dolma 1.7。
- 过滤：移除有 ≥32 个重复 n-gram(n=1..13) 的文档；StarCoder 额外去 <2 stars 仓库、最高频词 >30% 或 top-2 >50% 的文档。

### 训练细节
- 共训 **5.133T token（1.3 epoch）**；第二 epoch 前 reshuffle。
- 退火：**最后 100B token** 把 LR 从 5e-4 线性降到 0。
- 优化器 AdamW(β 0.9/0.95，wd 0.1)，peak LR **4e-4**，min LR 4e-5，cosine，warmup 2500 步，梯度裁剪 1.0；batch 1024 条(~4M token)；梯度/优化器态 FP32。
- 硬件：**256 块 H100 训约 10 天**（NVLink + InfiniBand）；部分实验用 GCP TCPx 集群。

### 后训练（OLMoE-1B-7B-Instruct）
- 框架 open-instruct。SFT：BF16，global batch 128（4×8 H100，per-device 2，grad accum 2），2 epoch，constant LR 2e-5，token-level loss 聚合；SFT 滤掉 >4096 token 样本。
- SFT 数据：Tülu 2 SFT mix 326,154 + No Robots 9,500 + CodeFeedback-Filtered 156,526 + MetaMathQA 98,750 + Daring Anteater(非chat) 17,082（多加 code/math）。
- DPO：global batch 32，3 epoch，LR 5e-7，DPO β 0.1；偏好数据 UltraFeedback binarized(去 TruthfulQA 污染) 60,800；SFT+DPO 都含 load balancing loss。
- 也试了 KTO（RMSProp，1.3 epoch/5000 步）。
- 后训练硬件：32 H100，SFT 33h + DPO 14h（KTO 8 H100 ×30h）。

### MoE 分析（关键发现）
- 路由在预训练早期就饱和；专家很少共激活；专家有明显**领域/词汇专长**。

### OLMoE-1B-7B-0125（2025-01 升级）
- 第一阶段同 mix；之后用 **Dolmino**（与 OLMo 2 13B 同款 100B 退火样本）退火。Dolmino 采样：Filtered DCLM 50.2% / Dolmino Math 17.5% / Decontaminated FLAN 16.7% / peS2o 9.52% / Wiki 3.57% / StackExchange 2.47%。

---

## OLMo 2（"2 OLMo 2 Furious", 2024-11, arXiv 2501.00656；v3 2025-10）

发布：Base 7B/13B(1124)、32B(0325)；Instruct 同规模；另有 1B（附录）。完全开放（权重/数据/代码 OLMo-core/日志/checkpoint/OLMES 评测）。

### 架构（相对 OLMo 1 的稳定性改造）
全家族：decoder-only、无 bias、SwiGLU、RoPE。OLMo 2 关键改动（vs OLMo 1 / 0424）：
- **RMSNorm**（无 bias）替代非参数 LayerNorm。
- **Reordered norm**：归一化放在 attention/MLP **输出**处而非输入：h = x + RMSNorm(Attn(x))；h_out = h + RMSNorm(MLP(x))（Liu et al. 2021 风格，稳训练）。
- **QK-Norm**：对 Q、K 用 RMSNorm 归一化后再算注意力（防 attention logits 过大导致发散）。
- **Z-Loss** 正则，权重 **1e-5**。
- **RoPE θ 从 10,000 提到 500,000**（5e5，提升位置分辨率，对齐 Llama 3）。
- embedding 不做 weight decay。
- tokenizer 换成 **cl100k**（GPT-3.5/4 的 tokenizer，Apache-2.0）pre-tokenizer+vocab，保留 PII 屏蔽 token。

各规模（Table 3）：
- 7B：32 层 / d=4096 / **MHA 32/32** / batch 1024 / peak LR 3e-4 / cosine 5T。
- 13B：40 层 / d=5120 / **MHA 40/40** / batch 2048 / peak LR 9e-4 / cosine 5T。
- 32B：64 层 / d=5120 / **GQA 40/8** / batch 2048 / peak LR 6e-4 / cosine 6.5T(4T 后截断)。
- 1B(附录)：16 层 / d=2048 / MHA 16/16 / batch 512 / peak LR 4e-4；训到 4T(截断自 5T schedule)。
- 序列长全 4096；warmup 2000 步；梯度裁剪 1.0。

### 两阶段预训练数据
**Stage 1 预训练（≥90% FLOPs）OLMo 2 Mix 1124**（≈3.90T token，>95% web）：
- DCLM-Baseline 3.71T(95%) / StarCoder(OLMoE 版) 83.0B / peS2o 58.6B / arXiv 20.8B / OpenWebMath 12.2B / Algebraic Stack 11.8B / Wiki 3.7B。同 OLMoE 的 mix。
- 过滤：去 ≥32 重复 n-gram(防 loss spike，§3.1)；StarCoder 去 <2 stars 等。

**Stage 2 mid-training（5–10% FLOPs）Dolmino Mix 1124**（高质量退火）：
- 高质量子集 832.6B：DCLM-Baseline(FastText top7%+FineWeb≥2) 752B / FLAN(去污) 17.0B / peS2o 58.6B / Wiki 3.7B / StackExchange Q&A 1.26B。
- Math mix 10.7B：TuluMath / Dolmino SynthMath / TinyGSM-MIND 6.48B / MathCoder2 等合成 3.87B / Metamath / GSM8K train 等。
- 从 Dolmino 采 50B / 100B / 300B 三种规模退火。

各规模总 token：**7B = 4.05T（3.90T 预训 + 退火）；13B = 5.6T（5T 预训）；32B = 6.6T（6.06T 预训）**。

### 训练阶段与"模型汤"(souping)
- Stage 1：random init 截断正态 mean 0 / std 0.02；LR warmup 2000 步到 peak，cosine 衰减到 peak 10%。
- Stage 2 mid-train：LR 线性降到 0。
- **Model souping（模型平均）**：用不同数据顺序多跑几次再平均。7B 退火 3 次×50B 取平均；13B 与 32B 平均 4 个 checkpoint（3×100B + 1×300B）。实证优于单 best。

### 稳定性技巧（§3）
- 过滤重复 n-gram；改 init（scaled→std 0.02）；RMSNorm；reorder norm；QK-Norm；Z-loss。这些联合把 loss/grad-norm spike 与缓慢发散压住，才能放大到 32B。

### 后训练（套 Tülu 3：SFT → DPO → RLVR）
- **SFT**：选最高质量现有指令集 + PersonaHub 合成数据。7B/13B 用 `tulu-3-sft-olmo-2-mixture`（**939,104 prompts**）；1B/32B 用 `...-0225`（866,138 prompts，去 date-cutoff/做 math majority-vote）。SFT effective batch 128、线性 LR、warmup 比例 0.3；7B sweep LR {1e-5,2e-5✓,3e-5}，OLMo 2 需要比 Llama 3.1 配方更高的 LR。
- **DPO**：扩展 UltraFeedback 流程；含 on-policy（采样 OLMo 2 SFT 自身生成）。prompts 7B 366.7k / 13B 377.7k；20 个模型池生成回答；**GPT-4o-2024-08-06 当 LM judge**，按 Argilla 法二值化。7B DPO LR 1e-6 / 13B 8e-7。
- **RLVR**：
  - 7B/13B 用 **PPO**，value function 从 RM 初始化（提升均分）；combined dataset = GSM8K + MATH train + 带约束 IF prompts；13B 还做两轮额外 RLVR（先 GSM8K 后 MATH）。
  - **1B/32B 用 GRPO**（免 RM）；32B 最终 LR 5e-7、KL β 0.1、每 prompt 16 样本。
  - PPO 超参（Table 18）：LR 13B 3e-7 / 7B 4e-7；effective batch 13B 248 / 7B 224；KL β 0.1/0.05 等；max episodes 13B 200k / 7B 100k；γ 1.0、GAE λ 0.95、PPO clip 0.2、无 EOS 罚 -10、max len 2048。

### AI infra（§6，"infra as research catalyst"）
- 训练栈：**OLMo-core**（第二代训练库，开源）。优化：torch.compile()、异步 bookkeeping(用 GLOO 旁路 NCCL)、显式 GC（disable 自动 GC 同步触发）、最小化 host-device sync。
- 两套集群：
  - **Jupiter**（Cirrascale，Austin）：128 节点 / **1,024 NVIDIA H100(80GB HBM3, 700W)**；2×Xeon 8468 + 2TB DDR5 + 18TB NVMe；800Gbps 本地网 + WEKA(1PB NVMe + 5PB HDD)；每节点 8×400Gbps InfiniBand(3200Gbps)，2-Tier Rail-Optimized 全双分；PUE 1.2。7B 大头在此。
  - **Augusta**（Google Cloud，Iowa）：160 节点 A3 Mega VM（每 8×H100）；GCS 存储；GPUDirect-TCPXO + gVNIC + Jupiter 数据中心网络；PUE 1.12。13B 大头在此。
- 调度：**Beaker**（自研 workload 管理，容器化，可跨 3 数据中心迁移，GPU 健康检查+cordoning）。
- 能耗：估算 7B+13B 预训约 **391 MWh**；7B 131 MWh/碳 52t，13B 257 MWh/碳 101t。
- 推理/serving 与量化：报告未专门展开（官方未公开细节）。

---

## OLMo 3（"Olmo 3", 2025-11, arXiv 2512.13961；v2 2026-04）

旗舰全开放 **7B / 32B**，强调"**model flow** 全生命周期开放"。四个变体：**Base / Think(思考) / Instruct / RL-Zero**。Olmo 3.1 Think 32B = 迄今最强全开放思考模型（接近 Qwen 3 32B thinking，token 量约其 1/6）。

### 架构（Table 33）
- decoder-only、SwiGLU、QK-Norm、RMSNorm(放输出)、Z-loss 权重 1e-5、embedding 不 wd、梯度裁剪 1.0。
- **7B：32 层 / d=4096 / MHA 32/32**；**32B：64 层 / d=5120 / GQA 40/8**。
- **Sliding Window Attention(SWA)**：窗口 **4096**，每 4 层有 3 层用 SWA，**最后一层始终 full attention**（降长序列训练 + 推理成本）。
- **RoPE θ 5e5**；长上下文用 **YaRN（仅作用在 full-attention 层）**扩到 **65K（65,536）**。
- tokenizer 同 OLMo 2（cl100k 衍生）。

### 三阶段 Base 数据（Dolma 3）
**Stage 1 预训练 Dolma 3 Mix（6T，实际 5.93T；9T 池）**(Table 4)：
- Common Crawl 4.51T(**76.1%**) / **olmOCR science PDFs** 805B(13.6%) / Stack-Edu(code) 409B(6.89%) / FineMath 3+ 152B(2.56%) / arXiv 50.8B(0.86%) / Wiki 2.51B(0.04%)。
- 三大新意：①万亿级**全局去重**新工具；②**token-constrained mixing + quality-aware upsampling** 两种选 token 法；③用 **olmOCR** 把学术 PDF 转线性化纯文本的新数据源。

**Stage 2 mid-training Dolma 3 Dolmino Mix（100B）**：提升 code/math/QA；含指令数据与思考 trace 为后训练铺路；方法 = 分布式单源反馈环 + 集中式集成测试。

**Stage 3 长上下文 Dolma 3 Longmino Mix（7B 50B / 32B 100B token）**：靠 olmOCR PDF 的长文档（>8K 的 22.3M 篇/640B token；>32K 的 4.5M 篇/380B token，号称最大开放长上下文集），扩到 65K。

### Dolma 3 数据 pipeline（§3.4 + 附录）
- CC：104 个 dump(2013-05~2024-12)，Resiliparse 抽 WET，初始 252.6B 文档。
- 启发式过滤：URL 过滤 + 长度/符号/spam 短语 + **fastText 语言分类(留英文)** + Madlad400 句级启发式。
- **去重三级**（Duplodocus，native-rust 分布式）：① exact(文档哈希全局去重)；② **MinHash** 模糊去重(32 shard + 跨 shard 兜底)；③ **substring**(后缀数组式模糊子串去重，57 shard)。设计上保留高质量文档的"重复度=质量信号"以便后续质量上采样。
- 质量/主题分类：**WebOrganizer** 分 24 主题；**DCLM 风格 fastText 质量分类器**；按 24 主题 × 20 质量档 = **480 子集**做细粒度上采样/重配比。
- olmOCR PDF：pre-filter + olmOCR(v0.1.49-0.1.53) 抽文 → MinHash 去重 → **文档类型感知的多阶段模型 PII 过滤** → 启发式过滤(去 >30% 表格等) → WebOrganizer 主题分桶。
- code：Stack-Edu(the-stack-v2 教育向再 curation)。math：用 **FineMath** 替换 OpenWebMath(保留数学记号，质量分≥3/4，cutoff 2024-09)。

### Base 训练细节（Table 34/35）
- 栈：**OLMo-core**；bfloat16 全程；torch.compile + 自定义 attention/LM-head kernel + 异步 metric/checkpoint。
- MFU：7B ~43% / 32B ~41%（seq 8192）；吞吐 7B 7700 TPS·GPU / 32B 1960 TPS·GPU。
- 并行：**HSDP（DP-rep × DP-shard）+ Llama3 风格 CP（context parallel，长上下文阶段用）**。
  - 7B：预训 DP-rep64×shard8=512 卡；mid 128 卡；长 ctx DP-rep32×CP8=256 卡。
  - 32B：预训 DP-rep16×shard64=1024 卡；mid 512 卡；长 ctx 1024 卡(含 CP8)。
- 集群：8×NVIDIA H100(80GB HBM3) 节点，**TCPXO 200Gbps/GPU**（Google Cloud）。
- 7B 预训：modified-cosine，前半 cosine over 5T，后半拉伸到 1 epoch(5.93T)；warmup 2000 步；peak LR 3e-4→final 3e-5；batch 512 条/4.19M token；seq 8192；总 5.93T。mid 100B(linear decay，LR 2.074e-4→0，batch 2.10M)；长 ctx 50B(seq 65536，batch 4.19M)。
- 32B 预训：cosine over 5.93T 在 **5.5T 截断**；peak LR 6e-4→final 6.21e-5；batch 1024 条/8.39M token；总 5.5T。mid **跑两次×100B**(不同种子后合并模型)；长 ctx 100B。
- 32B 的 peak LR 反而高于 7B，由更大 batch(8M vs 4M)补偿。

### 后训练总览（Base → 3 变体）
**评测**：自建 **OlmoBaseEval**（43 任务，比 OLMo 2 多 4 倍；任务聚类 + 小尺度 proxy(BPB) + SNR 分析；4 个 held-out：MMLU Pro/DeepMind Math/LBPP/BBH）。

- **Olmo 3 Think**（旗舰，生成思考 trace）：SFT → DPO(Delta Learning) → RLVR(OlmoRL)，每阶段都涨。数据集 **Dolci-Think-{SFT/DPO/RL}**。
- **Olmo 3 Instruct**：不出思考 trace，重 function calling、简洁；Dolci-Instruct-{SFT/DPO/RL}，DPO 含多轮偏好 + 控长干预。
- **Olmo 3 RL-Zero**：直接从 Base 做 RLVR（math/code/IF/general 四域），开 Dolci-RL-Zero + OlmoRL 代码做干净 benchmark（对 RL-zero 全程去污染）。

### Think SFT（Dolci Think SFT）
- prompt 跨 math/code/chat/safety/IF/science；reasoning trace 用模型生成（math 用 OpenThoughts3 / SYNTHETIC-2，最长 32K）。
- 规模(Table 17，部分)：OpenThoughts3 Math 752,997 / Python Algorithms 466,677 / OpenThoughts3 STEM 99,269 / SYNTHETIC-2-SFT-Verified 104,569 / OpenThoughts3 Code 88,900 / Persona Precise IF 223,123 / Precise IF 135,792 …(部分含上采样)。
- 训 2 epoch + LR sweep；最终是两个不同 LR checkpoint 的 **mergekit 线性加权合并**。

### Think DPO（Delta Learning）
- **Delta Learning（Geng et al. 2025）**：偏好数据质量主要看 chosen 与 rejected 的"能力差(delta)"，而非各自绝对质量。
- 关键发现：直接在 Qwen3-32B 思考 trace 上再 SFT 反而**伤** Olmo 3 Think SFT —— 故把这些(现已无效)completion 当 chosen，与更差的 completion 配成对（制造 delta）。
- 算法：标准 **DPO**；训 1 epoch + LR/数据量 sweep（早停重要）。

### Think RLVR（OlmoRL，"the cherry on top"）
- **OlmoRL = GRPO + DAPO + Dr GRPO 等改进**：
  - **零梯度过滤**（去掉组内 reward 全同的 batch，DAPO）。
  - **active sampling**（在零梯度过滤下保持 batch 大小的高效 dynamic sampling）。
  - **token-level loss**（按 batch 总 token 归一化，避免长度偏差）。
  - **去掉 KL loss**（GLM-4.5/DAPO/Dr GRPO 做法，允许更大策略更新，未致 over-opt）。
  - **clip-higher**（上裁剪界略大于下界，DAPO）。
  - **truncated importance sampling**（校正 inference/training 引擎 logprob 差，Yao 2025）。
  - **不按组 std 归一化 advantage**（Dr GRPO，去难度偏差）。
- 数据 **Dolci-Think-RL ~104,869 prompts**（4 域，Table 20）：IF-RLVR 30,186 / 数学多源(Open-Reasoner-Zero/DAPO-Math/AceReason/Klear/OMEGA…) / 代码(AceCoder/Klear/Nemotron/SYNTHETIC-2) / general chat(Tülu3 SFT/WildChat-4.8M/Multi-Subject-RLVR)。
- **Verifiers**（按域）：数学=规则+SymPy 等价判定(0/1)；代码=测试用例(通过率 或 全过=1，**AWS Lambda 跑代码**)；IF=约束函数全满足=1；chat-有参考=LM judge 打 [0,1]；chat-开放=LM judge 无参考打分。LM judge 默认 **Qwen3-32B(关思考)** via vLLM。
- 7B 离线难度过滤(pass>62.5% 的剔)；32B 靠 active sampling + 复用 7B DPO-filtered 数据。
- **OlmoRL infra（Open Instruct）**：**全异步 off-policy**（中心 learner 用 DeepSpeed 分布，多 vLLM actor 池）；**continuous batching**（边完成边补，省 32K 生成的浪费 —— static batching 会浪费高达 54%）；inference 占大头（32B 用 8 节点训 + 20 节点推；learner 75% 时间等数据，推理算力≈训练 5x；7B 用 7 推 + 2 训，推理≈14x）。
- **4x 训练提速**：7B Think RL 旧 infra 约 15 天 → 新 infra(pipelineRL + truncated IS)约 **6 天** 同等性能。

### 成本（§2.4，少见的官方公开）
- Olmo 3 Think 32B 从训练开始到评测约 **56 天**（专用 1024 H100；$2/H100·h 折 ~**$2.75M**）。
- 预训 ~47 天（含 mid/长 ctx）：5.5T 预训约 9.5 天@512 GPU + 35 天@1024 GPU；mid 两路并行@512×2 各 100B 约 1.5 天；长 ctx 单跑@1024 约 +1 天。
- 后训 ~9 天：SFT 4 个 LR 候选并行@256 GPU 各 36h；DPO 全 LR sweep@64 GPU 约 18h/run；初版 Think 32B RL ~5 天；发布后又继续最优 RL run **21 天@224 GPU** 产出 Olmo 3.1 Think 32B。

---

## Dolma（Dolma: an Open Corpus of Three Trillion Tokens, 2024-01, arXiv 2402.00159）

3T token 开放英文预训练语料 + 开源 Rust curation 工具包。OLMo 1 的数据基础。

### 规模与构成（Dolma 1.x）
- 目标 2–3T token（OLMo 1 用 ~2.7T 的 GPT-NeoX 计 token）。
- web 子集 **2.28T token**（CC，用 2020-05~2023-06 的 **25 个 snapshot**）；code 411B(GitHub/The Stack)；social 80B(Reddit，2005-12~2023-03，378M 帖经 Pushshift)；另含 peS2o/Gutenberg/Wikipedia。

### Dolma 工具包（开源）
- 两类操作：**filter**（语言/质量/内容/PII 过滤，文档/段/句级）+ **mix**（up/down-sample、去重、去污染，Rust，**Bloom filter** 线性时间近似去重）。
- 性能：复刻 C4 配方约 122 CPU-h/TB；全 200TB raw 在 c6a.48xlarge(192 vCPU) 约 5 天。
- 配套：开源 WIMBD 数据分析工具。

### 数据处理 pipeline（web 子集，关键阈值）
1. **采集+语言过滤**：CCNet → **fastText 语言 ID，英文分 ≥0.5**（去掉 61.7% 字节）；CCNet 段级去重去掉 ~70% 段（多为页眉/导航）；CCNet 整体滤掉 CC 84.2%（175.1TB→27.7TB）。
2. **质量过滤**（启发式，不用模型质量过滤器）：**Gopher All + 单条 C4 NoPunc**(去不以标点结尾的段)。消融显示 C4-NoPunc 单独优于 C4-All/Gopher-All，二者组合最佳。Gopher All 标 15.23% 字符删除，C4 NoPunc 标 22.73%。
3. **内容过滤（去毒）**：自训 **两个 fastText 分类器**（Jigsaw Toxic Comments 上训 hate + NSFW），对 CC 句子打分超阈删。两阈值消融：高阈 τ=0.4(删 5.5–7.3%)、低阈 τ=0.0004(删 29.1–34.9%)；为保规模采高阈。
4. **PII**：正则(快、牺牲精度)针对邮箱/IP/电话；≤5 个 PII span 的文档替换为特殊 token(影响 0.02% 文档)；密度高的整文档删(影响 0.001%)。
5. **去重**（web，三级，Bloom filter）：exact URL 去 53.2% 文档；exact 文档去 14.9%；exact 段落去 18.7% 段。先 URL/文档级(便宜)，最后段级。
- code：从已去重的 The Stack(2023-03) 起；质量启发式用 RedPajama v1 + StarCoder 规则；PII 同 web + detect-secrets 去密钥；去重用 **MinHash + LSH**。
- social/Reddit：原子内容(submission/comment 各独立文档)最优；过滤短文(comment <500 / submission <400 字符)、>40k 字符、<3 票、删除/NSFW/26,123 个 banned subreddit。
- 数据消融用 1.2B OLMo 模型训到 150B token 早停，8 任务评测。

---

## Tülu 系列（后训练配方）

### Tülu 1（"How Far Can Camels Go?", 2023-06, arXiv 2306.04751）
- 横评 **12 个开源指令数据集**（SuperNI、Flan V2、CoT、Dolly、OpenAssistant、Self-Instruct、Alpaca、Code-Alpaca、GPT4-Alpaca、Baize、ShareGPT 等）。
- 模型基于 **LLaMA 6.7B/13B/30B/65B**（含全参微调 65B Tülu）。
- 评测维度：MMLU/GSM8K/BBH/TyDiQA/HumanEval/AlpacaEval + 人评。
- 结论：无单一数据集全维最优；最佳模型平均达 ChatGPT 87% / GPT-4 73%。开源 open-instruct 框架。

### Tülu 2 / Tülu 2-DPO（"Camels in a Changing Climate", 2023-11, arXiv 2311.10702）
- 基座 **Llama-2 7B/13B/70B**；SFT 精选混合(FLAN/OpenAssistant/ShareGPT/Evol-Instruct/CoT)。
- **DPO 用 UltraFeedback** 偏好；较早证明 **DPO 可扩到 70B**（MT-Bench/AlpacaEval 显著提升，几乎不损公开任务）。

### Tülu 3（"Tülu 3: Pushing Frontiers in Open Language Model Post-Training", 2024-11, arXiv 2411.15124；v5 2025-04）

全开放前沿后训练；基座 **Llama 3.1 8B / 70B / 405B**。结果超 Llama 3.1-Instruct/Qwen 2.5/Mistral，逼近/超 GPT-4o-mini、Claude 3.5-Haiku（405B 对标 DeepSeek V3 / GPT-4o）。

**四阶段**：数据 curation(去污染+技能定向) → SFT → 偏好微调(DPO) → **RLVR**。

**核心技能**：knowledge / reasoning / math / coding / IF / general chat / safety；评测分 development + unseen(含新 IFEval-OOD、HREF)，全程去污染。

#### 数据（Tülu 3 SFT mix）
- 源池约 **23.3M prompt → 最终 SFT 939,344 prompt**（偏好用 425,145），Table 7 含：OpenAssistant 7,132 / WildChat(GPT-4) 100,000 / FLAN v2 89,982 / SciRIFF 10,000 / TableGPT 5,000 / **Persona MATH 149,960 / Persona GSM 49,980 / Persona Algebra 20,000 / NuminaMath-TIR 64,312 / Persona Python 34,999 / CoCoNot(safety) 10,983 / Aya(多语) 100,000 / Persona IF 29,980** 等。
- 用 **PersonaHub ~250K personas** 合成技能定向 prompt。
- 消融：WildChat(多样真实 chat)对 AlpacaEval 重要；safety 与通用正交；Persona/Math 数据明显提目标技能。

#### SFT 配方（Table 11）
- LR 8B **5e-6** / 70B **2e-6**；线性 schedule；effective batch **128**；max len 4096；warmup 比例 0.03；**2 epoch**；**sum loss**（token 等权，优于 mean）。
- 硬件：4–16 个 8×H100 节点；8B 32 GPU 6h / 70B 64 GPU 50h。
- 合并实验用 mergekit 线性平均（但最终用单 best SFT run）。

#### 偏好微调（DPO）
- **length-normalized DPO**（缓解长度偏差）；扩展 UltraFeedback 流程合成偏好；含 **on-policy**（采 Tülu SFT 自身）+ off-policy。
- 流程：选 prompt → 多模型池生成回答 → **LLM-as-judge** 多维评分(helpful/truthful/honest/IF) → 均值二值化。
- 最终偏好混合(Table 15)：总 prompt 354,192；**8B DPO 271,409 / 70B DPO 334,302**。规模(unique prompt)越大越好；复制 prompt(同 prompt 不同回答)增益有限。
- infra：缓存 reference logprob、chosen/rejected 分开前向以省显存(8×H100 验证)。

#### RLVR（本工作核心创新）
- 目标：max E[v(x,y) − β·KL(π||π_ref)]，**v=验证器**：正确给 α(**α=10**，未调)，否则 0。用 **PPO** 优化。
- 数据(Table 22，~30k)：**GSM8K train 7,473 + MATH train 7,500 + IF verifiable 14,973**（各带程序验证器：数学抽答案精确匹配，IF 用约束模板验证器）。
- 实现细节(借 Huang et al. 2024)：**value model 从 general RM 初始化**(最优)；RM/RL 训练 dropout=0；可多 epoch(消融跑 ~13 epoch)；非 EOS 罚 -10；advantage whitening。
- 关键发现：RLVR 在目标域提升且不太伤其他；value 从 general RM 初始化最好；**别**把 RM 分加到可验证奖励上；从 DPO 起比从 SFT 起 KL 更小、test 更好；KL 降太多会 over-optimization。
- **RLVR infra**：**ZeRO-3** 装模型；3 个模型(policy/reference/value)；**Ray 分配专用推理 GPU 跑 vLLM PagedAttention**；**异步 RL 训练**(推理/训练并发，用第二新数据保可复现)；scale 到 405B 借 OpenRLHF 风格 model allocation。
- RL 算力：8B RM 9h@8 H100；最终 RL 8B 65h@8 GPU / 70B 60h@48 GPU / 405B 46h@256 GPU。
- 405B scaling 见 §8.1。

---

## RewardBench（"RewardBench: Evaluating Reward Models for Language Modeling", 2024-03, arXiv 2403.13787；v2 2024-06）

首个系统评测 RLHF **奖励模型(RM)** 的基准 + 排行榜 + 代码库。

- 数据：**prompt-chosen-rejected 三元组**，部分含可验证理由(bug/错误事实)；报告每子集 win 率。
- **五大区(前四组成主分)**：
  - **Chat**（358）：AlpacaEval Easy/Length/Hard、MT Bench Easy/Medium。
  - **Chat Hard**（456）：MT Bench Hard + LLMBar(Natural + 4 个对抗子集)。
  - **Safety**（740）：Refusals Dangerous/Offensive、(应)拒答类、Do Not Answer 136 等。
  - **Reasoning**（1431）：PRM Math 447(人 vs buggy LLM) + HumanEvalPack 6 语言各 164(对 vs buggy code)。
  - **Prior Sets**：Anthropic Helpful 6192、HHH、MT Bench 等历史集求平均。
- 支持 RM 类型：**序列分类 RM(MLE)** 与 **DPO 隐式 RM**(策略/参考 log-ratio 当奖励)。
- 产出 leaderboard + code + dataset(HF allenai/reward-bench)，成 RM/对齐标准评测；后续有 RewardBench 2（本档案未抠其原文，官方未在此覆盖）。

---

## 来源（一手官方）

| 主题 | URL | 本地文件 |
|---|---|---|
| OLMo 1 (2402.00838) | https://arxiv.org/abs/2402.00838 ; pdf https://arxiv.org/pdf/2402.00838 | ../../../sources/llm/2024/2402.00838.pdf |
| Dolma (2402.00159) | https://arxiv.org/abs/2402.00159 | ../../../sources/llm/2024/2402.00159.pdf |
| OLMoE (2409.02060) | https://arxiv.org/abs/2409.02060 | ../../../sources/llm/2024/2409.02060.pdf |
| Tülu 3 (2411.15124) | https://arxiv.org/abs/2411.15124 | ../../../sources/llm/2024/2411.15124.pdf ; 同 themes/post-training/files/tulu-3.pdf |
| OLMo 2 (2501.00656) | https://arxiv.org/abs/2501.00656 | ../../../sources/llm/themes/architecture/olmo2.pdf ; 同 themes/post-training/files/olmo2.pdf |
| OLMo 3 (2512.13961) | https://arxiv.org/abs/2512.13961 ; pdf https://arxiv.org/pdf/2512.13961 | ../../../sources/llm/deep-dive/olmo3-arxiv-2512.13961.pdf |
| RewardBench (2403.13787) | https://arxiv.org/abs/2403.13787 | ../../../sources/llm/2024/2403.13787.pdf |
| Tülu 1 (2306.04751) | https://arxiv.org/abs/2306.04751 | ../../../sources/llm/2023/tulu-camels.pdf |
| Tülu 2 (2311.10702) | https://arxiv.org/abs/2311.10702 | ../../../sources/llm/themes/post-training/tulu2-dpo.pdf |
| OLMo 3 官方博客 | https://allenai.org/blog/olmo3 | — |
| Olmo 3 HF collection | https://huggingface.co/collections/allenai/olmo-3 ; https://huggingface.co/allenai/Olmo-3-1125-32B | — |
| OLMo / 训练代码 | https://github.com/allenai/OLMo ; https://github.com/allenai/OLMo-core | — |
| open-instruct (后训练) | https://github.com/allenai/open-instruct | — |
| OLMES (评测) / Dolma toolkit | https://github.com/allenai/olmes ; https://github.com/allenai/dolma | — |
| Duplodocus / datamap-rs (Dolma 3) | https://github.com/allenai/duplodocus | — |
| RewardBench leaderboard | https://hf.co/spaces/allenai/reward-bench | — |

---

## 未覆盖 / 官方未公开（gaps）
- OLMo 1/OLMoE 的**确切总卡时/总 FLOPs** 未逐一给全（OLMoE 给"256 H100 ~10 天"；OLMo 1 给集群规模未给总卡时）。
- 各模型的**推理/serving 栈、量化方案**官方报告基本未展开（OLMo 2/3 着墨于训练 infra；RL 推理用 vLLM）。
- OLMo 2 13B 各阶段精确 token 拆分给了总数；32B 0325 的后训练在主报告后补充（用 GRPO）。
- **RewardBench 2** 未抠原文（如需，arXiv/官方页另补）。
- Tülu 3 各 SFT 子集"final mix 内具体百分比"以 prompt 计数给出，未逐项给 token%。
- OLMo 3 各 Dolci 数据集的**逐项 token 数**部分以 prompt 数给出，部分未公开 token 级配比。
