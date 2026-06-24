---
title: "训练配方深挖 — NVIDIA Nemotron + Microsoft Phi 家族"
type: deep-dive
family: [Nemotron, Phi]
org: [NVIDIA, Microsoft]
created: 2026-06-18
updated: 2026-06-18
---

# NVIDIA Nemotron + Microsoft Phi 家族训练配方深挖

> 本文只采一手官方来源（arXiv 原文 / 官方 technical report / 官方博客 / 官方 GitHub·HF·model card）。
> 数字均抠自官方 PDF 原文；查不到的明确标注「官方未公开」。

两个家族被放在一起，是因为它们共享同一条主线信仰：**数据质量 / 合成数据 > 单纯堆规模**。
- **Microsoft Phi** 把这条路线发明出来（"Textbooks Are All You Need"）：用 GPT 系列生成"教科书质量"合成数据，小模型打大模型。
- **NVIDIA Nemotron** 把合成数据工业化：Nemotron-4 340B 的对齐 >98% 数据是模型自生成；并把"合成数据生成引擎 + 奖励模型 + 开源 pipeline"做成产品，后期再叠加 hybrid Mamba 架构、FP8/NVFP4 预训练、大规模 RLVR 与 on-policy 蒸馏。

---

## 家族演进脉络

### Microsoft Phi（小模型 / 数据质量路线）
- **phi-1 (2023-06)** — 1.3B 代码模型，"教科书质量"路线开山之作（HumanEval 50.6%，8×A100 训 4 天）。
- **phi-1.5 (2023-09)** — 1.3B，路线扩到常识推理；~30B token（其中 20B 全合成），无网络数据 → 毒性更低。
- **phi-2 (2023-12，仅博客)** — 2.7B，教科书数据 + 从 phi-1.5 做知识迁移；1.4T token，96×A100 训 14 天。
- **phi-3 (2024-04)** — mini 3.8B / small 7B / medium 14B，"data optimal regime"；mini 训 3.3T token 可跑手机；含 phi-3.5-mini / phi-3.5-MoE (16×3.8B) / phi-3.5-Vision。
- **phi-4 (2024-12)** — 14B，合成数据贯穿全程（~10T token，40% 合成），STEM QA 反超 teacher GPT-4o；后训练首创 Pivotal Token DPO。
- **phi-4-mini / phi-4-multimodal (2025-02)** — 3.8B 语言 + Mixture-of-LoRAs 多模态（文/图/音），词表扩到 200K，改用 GQA。
- **phi-4-reasoning / -plus (2025-04/05)** — 14B 推理模型；SFT(1.4M prompts，o3-mini 生成 CoT) + 短程 GRPO RL（仅数学，72,401 题）。
- **phi-4-reasoning-vision-15B (2026-03)** — 15B 多模态推理，构建于 Phi-4-Reasoning backbone + SigLIP-2，hybrid 推理/非推理 mode token。

### NVIDIA Nemotron（合成数据引擎 → hybrid 架构 → agentic 推理）
- **Nemotron-4 15B (2024-02)** — 15B 稠密多语言，8T token，GQA + squared ReLU + 256K 词表，384×DGX-H100。
- **Nemotron-4 340B (2024-06)** — 340B 稠密（Base/Instruct/Reward），9T token；对齐 >98% 合成数据，开源 SDG pipeline 与 RPO 算法；6144×H100。
- **Nemotron-H (2025-04→09)** — 8B & 56B/47B **hybrid Mamba-Transformer**；56B 首个全 FP8 预训练（20T token）；MiniPuzzle 剪枝蒸馏得 47B。
- **Nemotron Nano 2 / Nemotron-Nano-9B-v2 (2025-08/09)** — 12B hybrid Mamba 预训练(20T,FP8) → Minitron 压到 9B；推理模型，GRPO+DPO+RLHF，支持 thinking budget。
- **Llama-Nemotron (2025-05)** — LN-Nano 8B / Super 49B / Ultra 253B，从 Llama-3 出发：Puzzle NAS + 蒸馏 + 大规模 GRPO RL；reasoning toggle。
- **Nemotron-Cascade 2 (2026-03)** — 基于 Nemotron-3-Nano-30B-A3B 的后训练模型；Cascade RL + 多域 on-policy 蒸馏；IMO/IOI/ICPC 金牌级。
- **Nemotron 3 Super (2026-04)** — 120B-A12B hybrid Mamba MoE；首发 LatentMoE + MTP + NVFP4 预训练（25T token）；1M 上下文。
- **Nemotron 3 Nano Omni (2026-04/05)** — 基于 Nemotron 3 Nano 30B-A3B 的全模态（文/图/视频/音频）。
- **Nemotron 3 Ultra (2026-06)** — 550B-A55B hybrid Mamba MoE；20T token NVFP4 → 1M 上下文 → SFT+RLVR+MOPD（多教师在线策略蒸馏）。

---

## 各代关键参数对比（官方原文数字）

| 模型 | 总参/激活 | 层/隐藏维 | 注意力(Q/KV) | 架构类型 | 预训练 token | 上下文 | 精度 | 词表/Tokenizer |
|---|---|---|---|---|---|---|---|---|
| phi-1 | 1.3B | 24 / 2048 | 32 MHA | 稠密 Transformer | ~7B(过 8 epoch≈50B) | 2048 | fp16 | codegen-mono tokenizer |
| phi-1.5 | 1.3B | 24 / 2048 | 32 MHA | 稠密 | 150B | 2048 | — | 同 phi-1 |
| phi-2 | 2.7B | 官方未公开 | — | 稠密 | 1.4T | 2048 | — | 官方未公开 |
| phi-3-mini | 3.8B | 32 / 3072 | 32 MHA | 稠密 | 3.3T | 4K→128K(LongRope) | bf16 | Llama-2 同款, 32064 |
| phi-3-small | 7B | 32 / 4096 | GQA(4q:1kv) | 稠密+blocksparse | 4.8T | 8192 | — | tiktoken, 100352 |
| phi-3-medium | 14B | 40 / 5120 | 40 heads | 稠密 | 4.8T | 4K | — | 32064 |
| phi-3.5-MoE | 42B / 6.6B | 官方未公开 | — | MoE 16×3.8B top-2 | 官方未公开(4.9T级) | 4K→128K | — | 32064 |
| phi-4 | 14B | 沿用 medium(40/5120) | 官方未公开 | 稠密 | ~10T | 4K→16K(midtrain) | — | tiktoken(cl100k), 100352 |
| phi-4-mini | 3.8B | 32 / 3072 | GQA 24q/8kv | 稠密(tied emb) | 5T | 128K(LongRoPE) | — | o200k_base, 200K |
| phi-4-reasoning | 14B | 沿用 phi-4 | — | 稠密 | (SFT on phi-4) | 32K | — | 同 phi-4 |
| phi-4-reasoning-vision-15B | 15B | Phi-4-Reasoning backbone | — | 稠密+SigLIP-2 | +200B 多模态 | 官方未公开 | — | 同 phi-4 |
| Nemotron-4 15B | 15B | 32 / 6144 | GQA 48q/8kv | 稠密 | 8T(+1T 继续) | 4096 | bf16 | SentencePiece BPE, 256K |
| Nemotron-4 340B | 340B | 96 / 18432 | GQA 96q/8kv | 稠密 | 9T(8T+1T) | 4096 | bf16(部署FP8) | SentencePiece, 256K |
| Nemotron-H-8B | 8B | 52(4 attn) / 4096 | GQA 32q/8kv | hybrid Mamba-2 | up to 20T | — | FP8/BF16 | (Nemotron) |
| Nemotron-H-56B | 56B | 118(10 attn) / 8192 | GQA 64q/8kv | hybrid Mamba-2 | 20T | 8192(→128K) | **FP8** | (Nemotron) |
| Nemotron-Nano-12B-v2 | 12B(→剪枝9B) | 62(6 attn) / 5120 | GQA 40q/8kv | hybrid Mamba-2 | 20T | 128K(A10G可跑) | FP8 | (Nemotron) |
| LN-Super | 49B | NAS(异构) | — | 稠密(Llama-3.3 派生) | +40B 蒸馏 | 128K | — | Llama-3 |
| LN-Ultra | 253B | NAS(异构) | — | 稠密(Llama-3.1 派生) | +65B 蒸馏 | 128K | BF16/FP8 | Llama-3 |
| Nemotron-Cascade-2 | 30B / 3B | (Nano-3 backbone) | — | hybrid Mamba MoE | (后训练) | up to 256K | — | (Nemotron) |
| Nemotron 3 Super | 120B / 12B | 88 / 4096 | 32q/2kv | hybrid Mamba MoE + LatentMoE | 25T | up to 1M | **NVFP4** | (Nemotron) |
| Nemotron 3 Ultra | 550B / 55B | 108 / 8192 | 64q/2kv | hybrid Mamba MoE + LatentMoE | 20T | up to 1M | **NVFP4** | (Nemotron) |

> MoE 配置（Nemotron 3）: Super 每层 512 总专家 / top-22 激活 / MoE latent 1024 / shared-expert-intermediate 5376 / 2 个 MTP 层；Ultra 每层 512 总专家 / top-22 激活 / MoE latent 2048 / shared 10240 / 2 个 MTP 层。

---

# Microsoft Phi 家族

## phi-1 (Textbooks Are All You Need, 2023-06)

- **定位**：1.3B 代码模型，证明"教科书质量数据可打破 scaling law"。
- **架构**（§2.3 原文）
  - decoder-only Transformer，FlashAttention 多头注意力（MHA），MHA 与 MLP 层**并行配置**（仿 CodeGen/PaLM/GPT-NeoX）。
  - phi-1（1.3B）：24 层、hidden 2048、MLP-inner 8192、32 个头（每头 dim 64）。
  - phi-1-small（350M）：20 层、hidden 1024、MLP-inner 4096、16 头。
  - RoPE（rotary dim 32）；与 codegen-350M-mono 同 tokenizer；除 FlashAttention 外不用其它新技术。
- **预训练数据**（核心创新）
  - CodeTextbook ≈ 7B token = **6B「教科书质量」筛选网络代码**（用 LM-based 分类器从 The Stack+StackOverflow 的 >35B token 中筛，标注 ~100k 样本质量）+ **<1B GPT-3.5 合成 Python 教科书**。
  - 微调集 CodeExercises ≈ **<180M token**（GPT-3.5 合成 Python 习题+解）。
- **训练**：8×A100，pretrain <4 天（8 epoch over CodeTextbook，总见 token >50B；phi-1-base 在 51B token / 770 GPU-hr 检查点）；微调额外 7 小时。
  - fp16 + AdamW，linear-warmup-linear-decay，attn/residual dropout 0.1。
  - pretrain：effective batch 1024、max LR 1e-3、warmup 750 步、weight decay 0.1。
  - finetune：max LR 1e-4、warmup 50 步、weight decay 0.01，6000 步。
- **评测**：HumanEval pass@1 50.6%，MBPP 55.5%。
- **来源**：arXiv https://arxiv.org/abs/2306.11644 ；PDF https://arxiv.org/pdf/2306.11644 ；本地 `../../../sources/llm/2023/textbooks-are-all-you-need-phi-1.pdf`

## phi-1.5 (Textbooks Are All You Need II, 2023-09)

- **定位**：1.3B，路线从代码扩到自然语言常识推理。
- **架构**：与 phi-1 完全相同（24 层 / 2048 / 32 头），仅训练目标/数据不同。
- **数据**
  - phi-1.5：~**150B token**，80% 来自新合成「教科书式」常识推理数据（~20B token，用 GPT-3.5 生成，20K 主题做种子，prompt 里掺 web 样本提多样性）+ 20% 来自 phi-1 的训练数据（含 6B 筛选代码）。**唯一非合成部分就是这 6B 代码**。
  - 对照模型 phi-1.5-web：另造 95B token 筛选网络数据（88B 来自 Falcon RefinedWeb + 7B 代码）；phi-1.5-web 最终配比≈ 筛选 web 40% / phi-1 代码 20% / 新合成 NLP 40%。
- **训练**：随机初始化，**常数 LR 2e-4（无 warmup）**，DeepSpeed ZeRO Stage 2，batch size 2048，训 150B token。
- **安全**：无 web 数据 → 毒性/偏见显著降低。
- **来源**：https://arxiv.org/abs/2309.05463 ；PDF https://arxiv.org/pdf/2309.05463 ；本地 `2023/files/phi-1-5.pdf`

## phi-2 (官方博客, 2023-12)

> 只有官方博客，无技术报告，架构内部数字大多未公开。
- **规模**：2.7B，Transformer，next-token 目标。
- **训练 token**：1.4T，来自合成数据 + 网络数据（NLP 与代码），多次遍历。
- **infra**：96×A100，训练 14 天。
- **知识迁移**：从 1.3B 的 phi-1.5 嵌入知识到 phi-2（embedding 扩展）以加速收敛、提分。
- **数据哲学**："textbook-quality" 合成数据 + 高教育价值网络数据筛选。
- **后训练**：未做 RLHF / 指令微调，base 模型即评测；毒性低于已对齐模型。
- **官方未公开**：层数 / 隐藏维 / 头数 / tokenizer / 数据具体配比。
- **来源**：官方博客 https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/ ；本地 `2023/files/phi-2-microsoft-blog.html`

## phi-3 / phi-3.5 系列 (2024-04)

- **架构**
  - **phi-3-mini (3.8B)**：decoder-only，hidden 3072、32 头、32 层；默认 context 4K（LongRope 扩 128K = phi-3-mini-128K）；与 **Llama-2 同 tokenizer，词表 32064**（生态可直接复用）；bfloat16 训 3.3T token；4-bit 量化 ~1.8GB 可手机本地跑。
  - **phi-3-small (7B)**：hidden 4096、32 头、32 层；改用 **tiktoken 词表 100352**（多语言更好）；默认 context 8192；**GQA（4 query 共享 1 key）**；GEGLU 激活 + **muP**（小 proxy 调参再迁移）；**新设计 blocksparse attention**，dense 层与 blocksparse 层交替（省 KV cache + 长上下文检索）；训 4.8T token。
  - **phi-3-medium (14B)**：40 头、40 层、hidden 5120；与 mini 同 tokenizer/架构（词表 32064）；训 4.8T token（略多 epoch）。
  - **phi-3.5-MoE**：16 个专家、top-2 路由（每专家是独立 GLU），**6.6B 激活 / 42B 总参**；用 **SparseMixer** 训练稀疏路由；与 mini/medium 同词表 32064；比肩 Gemini-1.5-Flash / GPT-4o-mini。
  - **phi-3.5-Vision**：4.2B，由 phi-3.5-mini 派生；SFT 多模态 ~33B token + 文本/多模态 DPO。
- **数据 pipeline & 哲学**："data optimal regime"——重过滤公开网络 + LLM 合成数据；
  - **两阶段不相交预训练**：Phase-1 以 web 源为主（教通识与语言理解）；Phase-2 把更重过滤的 web 子集 + 合成数据混合（教逻辑推理与小众技能）。
  - 过滤思路：用 LLM-based filtering 把 web 数据卡到「正确的知识水平」（如某场球赛结果对前沿模型有用、对小模型则浪费容量，应剔除）。
- **后训练（mini）**：两阶段 = SFT + DPO。
  - SFT：高度精选高质量数据，覆盖 math/coding/reasoning/对话/模型身份/安全，从英文样本起步。
  - DPO：覆盖 chat-format、推理、Responsible-AI；用不良输出作 rejected 来"避坏"。
  - 安全：post-training 安全对齐 + 微软 AI Red Team 多轮迭代红队 + 自动测评。
- **来源**：https://arxiv.org/abs/2404.14219 ；PDF https://arxiv.org/pdf/2404.14219 ；本地 `2024/files/2404.14219.pdf`

## phi-4 (2024-12)

- **定位**：14B，把合成数据贯穿训练全程，STEM QA 反超 teacher GPT-4o（非纯蒸馏）。
- **架构**（§3 Pretraining details）
  - decoder-only Transformer，14B，默认 context 4096（midtrain 扩到 16K）。
  - 架构**紧贴 phi-3-medium**，但改用 **tiktoken（cl100k 系），padded 词表 100,352**；4K 范围内用 full attention（phi-3-medium 是 2K 滑窗）。
- **预训练数据（核心）**
  - ~**10T token**，linear warmup/decay schedule。
  - 创建 **50 类合成数据集**，累计约 **400B unweighted 合成 token**（multi-stage prompting，自修订、指令逆转等；seed 来自 web/书/代码）。
  - **最终数据配比**：合成 **40%** / web+web-rewrites **30%**（两者各半）/ code **20%**（合成+原始混合）/ targeted（学术+书）**10%**。
  - 按 token 量：合成 cluster ~1.3T、code ~820B、targeted ~580B、web-rewrites 与 synthetic 各 ~290B（注：此处不同口径，原文给出多组数字，整体合成占比最高）。
  - 长上下文 midtrain：30% 新长上下文数据 + 70% recall 数据。
  - 关键发现：对小模型，多 epoch 合成数据 > 补新鲜 web token。
- **后训练（创新）**
  - 一轮 SFT（chatml 格式，~**8B token**，覆盖 40 语言）→ 一轮 **Pivotal Token DPO** → 一轮 full-length preference DPO。
  - **Pivotal Token Search (PTS)**：找出决定答案对错的"关键 token"，只针对该单 token 构造 DPO 偏好对（query=Q+t1..ti-1，单 token tacc/trej）；用于 ground-truth 可得任务（数学等）。
  - **Judge-Guided DPO**（第二轮）：~**850k** 对，用 GPT-4o 作 judge 标注正负，基于 rejection sampling + LLM 评估。
- **官方未公开**：精确层数/头数（仅说"closely follows phi-3-medium"=40/40/5120 量级）、GPU 数与卡时。
- **来源**：https://arxiv.org/abs/2412.08905 ；PDF https://arxiv.org/pdf/2412.08905 ；本地 `2024/files/2412.08905.pdf`

## phi-4-mini / phi-4-multimodal (2025-02)

- **定位**：3.8B 语言模型 + 通过 **Mixture-of-LoRAs** 扩展的多模态（文/图/音）。
- **架构（phi-4-mini）**
  - decoder-only，**32 层、hidden 3072、tied input/output embedding**；支持 128K context（LongRoPE）。
  - **GQA：24 query heads / 8 KV heads**（KV cache 减 1/3）；**fractional RoPE**——25% 注意力头维度保持 position-agnostic（更平滑长上下文）。
  - **tokenizer o200k_base（tiktoken），词表 200K**（强化多语言）。
- **预训练数据**：构建 **5T token** 语料，合成配方强调高质量数学/代码。
- **多模态（phi-4-multimodal）**：encoder + projector + **modality-specific LoRA**（vision LoRA、speech/audio LoRA），冻结语言 backbone；speech/audio LoRA 仅 460M 参数即登 OpenASR 榜首；支持 (vision+language)/(vision+speech)/(speech/audio)。Vision 数据约 0.5T token。
- **reasoning 增强版（实验，预览）**：三阶段——Distill 预训练 → Distill 微调 → **Roll-Out DPO**（300K 偏好样本）；3.8B 即逼近 DeepSeek-R1-Distill-Qwen-7B，超 DeepSeek-R1-Distill-Llama-8B。
- **来源**：arXiv "Phi-4-Mini Technical Report" https://arxiv.org/abs/2503.01743 ；本地 `2025/files/phi-4-mini.pdf`

## phi-4-reasoning / phi-4-reasoning-plus (2025-04 / 05)

- **定位**：14B 推理模型，在 phi-4 上做推理 SFT；plus 再加短程 RL。
- **基座/架构**：在 Phi-4 (14B) 上 SFT；为长 CoT 把**上下文扩到 32K**（plus 也是 32K）。
  - **reasoning token**：把 base 模型两个占位 token 改造为 `<think>` 和 `</think>`；训练时用 reasoning-specific system message 强制把推理放进 `<think>...</think>`。
- **SFT 配方**
  - **>1.4M prompts**，答案为 **o3-mini 生成的长推理链**；prompt 经精选覆盖不同难度，落在 base 模型能力边界。
  - 领域：STEM（含数学）、coding、safety。把 web seed 改写成"可验证合成题"用于 SFT 与 RL。
  - SFT 训练：max 长度 32K token。
- **RL（仅 phi-4-reasoning-plus）**
  - 算法 **GRPO**（Group Relative Policy Optimization），outcome-based，**仅数学**。
  - seed：**72,401 道**可验证数学题；约 **16K 步**，global batch **32**，context 32K，AdamW。
  - **rule-based reward**（避免神经 RM 的 reward hacking）：核心是 length-aware accuracy reward（cosine scaling，Rmin 0.5→Rmax 1.0）；format 违规（缺 `<think>` / 缺 `\boxed{}`）惩罚 Racc=-1.0；外加 5-gram 重复惩罚。
  - 结果：plus 比 reasoning 数学更准但平均多用 ~1.5× token；IFEval 比 base phi-4 高 22 分。
- **来源**：arXiv "Phi-4-reasoning Technical Report" https://arxiv.org/abs/2504.21318 ；本地 `2025/files/phi-4-reasoning.pdf`

## phi-4-reasoning-vision-15B (2026-03)

- **定位**：15B 紧凑开放权重多模态推理模型，擅长科学/数学推理与 UI 理解。
- **架构**
  - **mid/late-fusion**：SigLIP-2 视觉编码器（Tschannen et al. 2025）+ **Phi-4-Reasoning backbone**；视觉 token 投影进语言空间。
  - 系统消融显示**高分辨率 + 动态分辨率**视觉编码器带来一致增益（精确感知是高质量推理前提）。
  - **hybrid 推理/非推理数据 + 显式 mode token**：单模型可在"快速直答"与"链式推理"间切换。
- **数据/算力对比**（原文亮点）：用约 **200B 多模态 token**，叠加 Phi-4-Reasoning（用 16B token 训）和核心 Phi-4（400B unique token）——总量远低于"用 >1T token 训练"的同类多模态模型。
- **数据策略**：系统化过滤 + 错误纠正 + 合成增强；"数据质量是性能首要杠杆"。
- **官方未公开**：精确层/头/MoE（沿用 phi-4 14B 量级 + 视觉编码器）、RL 细节。
- **来源**：官方报告 https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf ；HF https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B ；GitHub https://github.com/microsoft/Phi-4-reasoning-vision-15B ；本地 `2026/files/phi-4-reasoning-vision-15b-tech-report.pdf`

---

# NVIDIA Nemotron 家族

## Nemotron-4 15B (2024-02)

- **定位**：15B 稠密多语言通用模型，8T token，主打超同级多语言。
- **架构**（Table 1）
  - 标准 decoder-only Transformer，causal mask；**32 层、hidden 6144、48 attention heads、8 KV heads（GQA）**、seq 4096、**词表 256,000**。
  - 3.2B embedding 参数 + 12.5B 非 embedding 参数；**RoPE、squared ReLU 激活、无 bias、dropout=0、untied input-output embedding**；SentencePiece BPE tokenizer（在 8T 数据上训，强化低资源语言覆盖）。
- **预训练数据**：**8T token**，配比 **英文自然语言 70% / 多语言 15%（53 种语言）/ 源代码 15%（43 种编程语言）**；用 LM-based filtering（仿 CCNet）清洗。
- **算力/并行**：**384 台 DGX H100（3072×H100 80GB SXM5，峰值 989 TFLOP/s·卡 bf16）**；**8-way Tensor Parallelism + Data Parallelism**（DP 从 96 渐增到 384 随 batch ramp）；3 阶段 batch-size ramp。
- **Continued Training**：在 8T 之后再做小量**继续训练**——切换数据分布 + 用更陡的 LR decay schedule（两套数据分布，第一套占多数 = 已见过的高质量数据），显著提质。
- **来源**：https://arxiv.org/abs/2402.16819 ；PDF https://arxiv.org/pdf/2402.16819 ；本地 `2024/files/2402.16819.pdf`

## Nemotron-4 340B (Base / Instruct / Reward, 2024-06)

- **定位**："合成数据生成引擎"；对齐 >98% 合成数据，开源整套 SDG pipeline + 奖励模型；可单台 8×H100 FP8 部署。
- **架构**（Table 1）
  - 标准 decoder-only，**340B 稠密（非 MoE）**；**96 层、hidden 18432、96 attention heads、8 KV heads（GQA）**、context 4096、**词表 256,000**。
  - RoPE、SentencePiece、squared ReLU、无 bias、dropout=0、untied embeddings。
- **预训练**：**9T token = 前 8T 正式预训练 + 末 1T 继续预训练**（同 15B 的"切数据分布+陡降 LR"策略，两套分布）；含单语+平行多语 + 43 种编程语言。
- **算力/并行**：**768 台 DGX H100（6144×H100 80GB SXM5）**；**8-way Tensor Parallelism + 12-way Pipeline Parallelism**；bf16 训练，部署可 FP8 单机 8×H100。
- **后训练（>98% 合成数据，全程仅 ~20K 人工：10K SFT + 10K HelpSteer2）**
  - **两阶段 SFT**：① Code SFT（~800K 样本，1 epoch，提代码/推理且不干扰其它任务）② General SFT（200K 混合 + 2% 上一阶段代码，1 epoch）。
  - **偏好微调**：DPO + 自研 **RPO（Reward-aware Preference Optimization）**——不止用 chosen/rejected 二元序，还用 RM 给出的**奖励差**作为目标 margin（近似 reward gap，防过拟合）。偏好集 **160K** 样本，1 epoch，global batch 256，常数 LR 调在 [3e-8,3e-7]。
  - **Iterative Weak-to-Strong Alignment**：用当前模型迭代生成更优数据再训下一代（340B-Interm-1/2 自增强）。
  - 多轮对话偏好集：构造两轮/三轮 prompt（迭代 role-play）。
  - 补充能力数据：Topic following（CantTalkAboutThis）、PRM800K/SciBench 等许可子集。
- **奖励模型 Nemotron-4-340B-Reward**：在 Base 上换 **regression reward head**，输出 **5 维 HelpSteer 属性（Helpfulness/Correctness/Coherence/Complexity/Verbosity）**；用 10K HelpSteer2 人工偏好训练；发布时 **RewardBench 主榜居首**（超 GPT-4o-0513、Gemini-1.5-Pro-0514）。
- **开源**：合成数据生成 pipeline（合成 prompt→回复/对话生成→质量过滤→偏好排序）、HelpSteer2 数据、Reward 模型；NVIDIA Open Model License。
- **来源**：https://arxiv.org/abs/2406.11704 ；PDF https://arxiv.org/pdf/2406.11704 ；本地 `2024/files/2406.11704.pdf`、`themes/post-training/files/nemotron4-340b.pdf`；HF https://huggingface.co/nvidia/Nemotron-4-340B-Instruct

## Nemotron-H (8B & 56B/47B, 2025-04→09 v4)

- **定位**：hybrid **Mamba-Transformer** 家族，给定精度降低推理成本（最高 3× 更快）。
- **架构**（Table 1，§2.1）
  - 由 **Mamba-2 + self-attention + FFN** 三种层混合；**约 8% 的层是 self-attention**，其余 Mamba-2 与 FFN 各半，均匀分散。
    - 8B：**52 层（其中 4 attn）、hidden 4096、FFN 21504、32 query heads、Mamba state dim 128**。
    - 56B：**118 层（其中 10 attn）、hidden 8192、FFN 32768、64 query heads、Mamba state dim 256**。
  - 两者均 **GQA 8 KV heads、Mamba-2 groups=8、squared ReLU**；**无位置编码**（Mamba 提供位置信息）；Mamba head dim 64、expansion 2、conv window 4；**RMSNorm**、separate embedding/output、无 dropout、无 bias、每层有 residual。
  - 对照基线 Nemotron-T-8B 是纯 Transformer（32 层，用 RoPE）。
- **预训练数据**（§2.2）
  - 最高 **20T token**；四类 curation pipeline：web crawl / math / code / academic。
  - **English Common Crawl = 6.3T token**（4.4T 全局去重"真"token + **1.9T rephrased 合成数据**），用 model-based 分类器**集成**分 5 个质量桶 + 启发式/困惑度过滤；低质 token 改写提质。比 DCLM 高 5.6 MMLU 点，或在同质量下 4× 更多 unique token。
  - 数据类目 7-8 种：web crawl / math / wiki / code / academic / crawl++（OpenWebText/BigScience/Reddit）/ multilingual（9 语）/ 合成 SFT-style。
  - **230B 合成 SFT-style token**（174B 数学 + 35B 代码 + 21B 通识；用 Qwen2.5、Mixtral-8x22B、Nemotron-4-340B、DeepSeek-R1[仅 56B] 生成）。
- **数据配比/课程**：**4 阶段 phased data-blending**——Phase1 求多样性；Phase2/3 转高质量数据（Wikipedia 等），在 60% 点切 Phase2、80% 点切 Phase3，Phase4 为最后 380B token。phased 比随机数据序好 3.4%。
- **训练**：seq 8192；8B peak LR 8e-4 / warmup 8.3B token；56B peak LR 4e-4 / warmup 25B token；20T horizon。
- **FP8 recipe**（56B 首个全 FP8 预训练）
  - 除前 4 层 + 后 4 层保 BF16 外，其余 GEMM 用 FP8；**hybrid FP8：权重/激活 E4M3，梯度 E5M2**；**per-tensor 动态量化**（算 scale = FP8 max / 张量绝对值最大）；太小则 flush-to-zero。
  - FP8 与 BF16 下游精度持平或更优（56B 上 FP8 评测甚至反超 BF16）。
- **压缩 MiniPuzzle**：从 56B 剪枝+蒸馏得 **47B-Base**（仅 63B 训练 token + FP8），精度近 56B 但快 20%。
- **长上下文/对齐**：可几百步内学会更长上下文（128K RULER）；另有 8B-Instruct、8B-VLM、56B-VLM。
- **来源**：arXiv https://arxiv.org/abs/2504.03624 （v4 2025-09）；本地 `2025/files/nemotron-h.pdf`

## Nemotron Nano 2 / Nemotron-Nano-9B-v2 (2025-08 / 09 v4)

- **定位**：hybrid Mamba-Transformer **推理**模型；12B 预训练 → Minitron 压到 9B，单张 A10G(22GiB) 跑 128K，推理吞吐比 Qwen3-8B 高 3-6×。
- **架构**（Table 1，§2.1，承自 Nemotron-H）
  - Nemotron-Nano-12B-v2-Base：**62 层 = 6 self-attention + 28 FFN + 28 Mamba-2**；**hidden 5120、FFN 20480、GQA 40 query / 8 KV heads**；Mamba groups 8、state dim 128、head dim 64、expansion 2、conv window 4；squared ReLU、无位置编码、RMSNorm、separate emb、无 dropout/bias。
- **预训练数据**（开源数据集）
  - **20T token，FP8 精度**，**Warmup-Stable-Decay (WSD)** LR schedule，seq 8192，global batch 768（6,029,312 token/batch，无 batch ramp）。
  - 新数据集：**Nemotron-CC-v2**（8 个额外 CC 快照 + 合成改写，多语言）、**Nemotron-CC-Math-v1（133B token 数学，Lynx+LLM pipeline，标准化为 LaTeX）**、**Nemotron-Pretraining-Code-v1**（多阶段过滤+去重，含 11 语言代码 Q&A）。合成改写从 Qwen3-30B-A3B 生成。
- **长上下文 CPT**：base 后做长上下文继续预训练到 128K（8B 用 512K seq 做 CPT 更佳；8-way TP + 16-way context parallelism，global batch 12，保持每 batch token 数与预训练一致）。
- **后训练**（约 **90B token**，主体单轮 prompt-response 带推理）
  - **多阶段 SFT**（3 阶段）：Stage1 通用多域；Stage2 工具调用/长上下文；Stage3 强化长上下文 + **截断推理（约 5% 数据推理链被截到 1-2K token 保留终答）** → 实现**推理预算（thinking budget）控制**。
  - **GRPO**（指令遵循/对话）、**DPO**（强化工具调用，含 WorkBench 多步可验证工具环境的迭代 DPO）、**RLHF**。
- **压缩 Minitron**：从对齐后的 12B 剪枝+蒸馏得 9B（用 1024 样本校准）。
- **来源**：arXiv https://arxiv.org/abs/2508.14444 （v4 2025-09）；本地 `2025/files/nemotron-nano-2.pdf`

## Llama-Nemotron (LN-Nano 8B / Super 49B / Ultra 253B, 2025-05)

- **定位**：从 Llama-3 出发的开放高效**推理**模型族；NAS 压缩 + 蒸馏 + 大规模 RL；运行时 reasoning toggle。
- **来源模型**：LN-Nano=Llama-3.1-8B、LN-Super=Llama-3.3-70B、LN-Ultra=Llama-3.1-405B；上下文 128K。
- **五阶段构建**
  1. **Puzzle NAS**（neural architecture search）：从 Llama-3 做 block-wise local distillation，搜出异构架构（LN-Super 单 H100 TP1 跑，5× 吞吐 vs Llama-3.3-70B；LN-Ultra 适配整 8×H100 节点）。
  2. **Post-NAS 训练**：知识蒸馏 + 继续预训练（LN-Super 40B token KD；**LN-Ultra 先 KD 65B token** 再继续预训练）。
  3. **推理 SFT**：标准指令数据 + 来自强 teacher（**DeepSeek-R1**、Qwen2.5-Math 等）的推理轨迹；数学题 16 代/题（R1），代码 R1 多代生成 + 答案校验（Qwen2.5-32B 判等价）；seq packing，effective seq 32k，global batch 256。
  4. **大规模 RL（GRPO，主要 LN-Ultra）**：科学/数学可验证奖励；rollout prompt size 72、每 prompt 采 16 响应（temp=1,top_p=1）、global batch 576、每 rollout 2 次梯度更新；**accuracy reward + format reward**（仿 DeepSeek-R1）；**curriculum**（动态调 pass-rate 目标分布）；训到收敛。
  5. **短对齐 RL**：指令遵循 + 人类偏好（RLOO/iterative online RPO，用 HelpSteer2）。LN-Super: LR 4e-7、KL β 1e-5、reward scale 3.0、batch 64、500 步、2 轮；LN-Ultra GRPO: 采 8 响应、30 步、LR 3e-7、batch 288、KL β 1e-3。
- **AI infra 亮点**：自研 RL 框架支持**在线 FP8 generation（vLLM）**——峰值 32 tokens/s/GPU/prompt，generation 1.8× 提速（FP8 单项 1.4× + 额外 0.4×）。
- **reasoning toggle**：system prompt `detailed thinking on/off` 切换长 CoT 与直答。
- **开源**：权重 + 后训练数据集 + 训练代码（NeMo / Megatron 对齐栈）。
- **来源**：arXiv https://arxiv.org/abs/2505.00949 ；本地 `2025/files/llama-nemotron.pdf`、`themes/post-training/files/llama-nemotron.pdf`；HF https://huggingface.co/collections/nvidia/llama-nemotron

## Nemotron-Cascade 2 (2026-03)

- **定位**：基于 **Nemotron-3-Nano-30B-A3B-Base（30B 总 / 3B 激活 MoE hybrid）** 的开放后训练模型；Cascade RL + 多域 on-policy 蒸馏；IMO/IOI/ICPC 金牌级（开放权重中第二个，前为 DeepSeek-V3.2-Speciale-671B）；20× 更少参数。
- **SFT**：覆盖数学/代码/科学/工具使用/agentic/SWE + 多轮对话/知识 QA/创意写作/角色扮演/安全/指令遵循；**所有样本 pack 到 ≤256K token，单阶段训练，~1.5 epoch 最优**。
  - chat template 改动：移除 `/think` `/no_think` 标签；在前面预置空 `<think></think>` 块来激活 non-thinking 模式；工具调用用 `<tools></tools>`。
- **Cascade RL + MOPD**（核心）
  - **Cascade RL**（承自 Cascade 1）：按域顺序做 domain-wise RL；Cascade 2 大幅扩展覆盖更广推理 + agentic 域。
  - **算法 GRPO**，但**完全去掉 KL 项** → 退化为带 group-normalized reward 的 token-level REINFORCE（Williams 1992）；缓解 entropy collapse。
  - **Multi-domain On-Policy Distillation (MOPD)**：在 Cascade RL 全程，对每个域取**最强中间 teacher** 做在线策略蒸馏，恢复基准回退、保持增益；相似响应格式的任务组做 multi-domain RL。
  - Code RL：对有 test case 的 prompt 做 correctness filtering（只留生成正确代码的 teacher 轨迹）。
  - IF-RL（指令遵循）：纯 "thinking mode" 训练，不用 reward model；显著提升指令遵循。
  - 还有 execution-based RL for agentic SWE scaffold。
- **开源**：Nemotron-Cascade-2-30B-A3B（后训练模型）、Nemotron-Cascade-2-SFT-Data、Nemotron-Cascade-2-RL-Data。
- **来源**：arXiv https://arxiv.org/abs/2603.19220 ；本地 `2026/files/arxiv-2603.19220.pdf`

## Nemotron 3 Super (120B-A12B, 2026-04)

- **定位**：120B 总 / **12B 激活** hybrid Mamba-Attention MoE；Nemotron 3 家族首个 ① NVFP4 预训练 ② LatentMoE ③ MTP；1M 上下文。
- **架构**（Table 1）
  - **88 层、Model Dimension 4096**；**Q-heads 32 / KV-heads 2 / head dim 128**（GQA）；Mamba state dim 128、groups 8、Mamba heads 128、Mamba head dim 64。
  - **MoE（LatentMoE）**：每层 **总专家 512、top-22 激活**、Expert Hidden 2688、Shared-Expert-Intermediate 5376、**MoE Latent Size 1024**；**2 个 MTP 层（共享权重）**。
  - 88 层周期性交错：MoE 层与 Mamba-2 层配对，少量 self-attention 层作"global anchors"实现全 token 交互（应对 KV cache 二次增长）。
  - **LatentMoE**（Elango et al. 2026）：把 hidden 投到压缩 latent 维 ℓ 再路由到扩展专家集（专家数 N→N·d/ℓ、激活 K 按比例放大），在 latent 维完成专家计算；门控/共享专家/非专家层仍用全 hidden d——兼顾 accuracy/FLOP 与 accuracy/参数。
- **预训练数据**：**25T token，2 阶段**——Phase1 占 80%（20T，求多样/广覆盖）；Phase2 占 20%（5T，高质量+benchmark 导向）。base 超 GLM-4.5-Air-Base 等同级。
- **NVFP4 预训练 recipe**（§2.2）
  - 用 Transformer Engine 开源 NVFP4 GEMM kernel；**权重 2D block scaling、梯度/激活 1D block（沿 GEMM reduction 轴）**；wgrad 输入做 **Random Hadamard Transform**，梯度做 **stochastic rounding**。
  - **NVFP4 格式 = E2M1 元素 + 16 元素 micro-block + E4M3 micro-block scale + 第二级 FP32 global scale**；稳定训练至 25T token。
- **MTP**：原生投机解码加速 + 提质。
- **AI infra/性能**：吞吐相比 GPT-OSS-120B 高 2.2×、相比 Qwen3.5-122B 高 7.5×（B200 上 vLLM/TRT-LLM 测）；RL infra 改进支持大规模异步训练。RLHF 用 GenRM（Qwen3-Nemotron-235B-A22B-GenRM-2603）。
- **后训练**：SFT + RL（细节见报告，扩大 RL 环境广度与数据质量）。
- **开源**：Base BF16 / 后训练 BF16/FP8/NVFP4 检查点 + 数据集 + RL 环境 + GenRM。
- **来源**：arXiv https://arxiv.org/abs/2604.12374 ；配套 https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf ；本地 `2026/files/arxiv-2604.12374.pdf`

## Nemotron 3 Nano Omni (2026-04 / 05)

- **定位**：Nemotron 多模态系列首个**原生支持音频**（文/图/视频/音频）的全模态模型。
- **架构**：encoder-projector-decoder；**Nemotron 3 Nano 30B-A3B（30B 总 / 3B 激活 MoE hybrid）LLM backbone** + **C-RADIOv4-H1 视觉编码器** + **Parakeet-TDT-0.6B-v2 音频编码器**。
  - 相比前代 Nemotron Nano V2 VL（dense 12B backbone）换成 30B-A3B MoE backbone。
  - **上下文从 128K 扩到 256K**；多模态 **token-reduction** 技术降延迟提吞吐。
- **训练**：分阶段渐进引入新模态并扩上下文（staged）；发布 reasoning 版。
- **性能**：B200 上单流输出吞吐比 Qwen3-Omni 高 3×、固定交互目标下每 GPU 输出吞吐高 9×；比 Nemotron Nano V2 VL 高 3×。
- **发布**：BF16 / FP8 / NVFP4 检查点 + 部分训练数据 + 代码（Megatron-Bridge、NeMo-RL、示例 pipeline）。
- **来源**：arXiv https://arxiv.org/abs/2604.24954 ；本地 `2026/files/arxiv-2604.24954.pdf`

## Nemotron 3 Ultra (550B-A55B, 2026-06)

- **定位**：家族最大最强；550B 总 / **55B 激活** hybrid Mamba-Attention MoE；为长时自主 agentic 优化，1M 上下文，全开源。
- **架构**（Table 1）
  - **108 层、Model Dimension 8192**；**Q-heads 64 / KV-heads 2 / head dim 128**（GQA）；Mamba state dim 128、groups 8、Mamba heads 256、Mamba head dim 64。
  - **LatentMoE**：每层 **总专家 512、top-22 激活**、Expert Hidden 5120、Shared-Expert-Intermediate 10240、**MoE Latent Size 2048**；**2 个 MTP 层（共享权重）**。
  - 全 Nemotron 3 关键技术：NVFP4 预训练 + LatentMoE + MTP。
- **预训练**：**20T token，NVFP4，WSD schedule**，2 阶段（Phase1 15T 求多样，Phase2 高质量精炼）；LR warmup 200B token。
- **长上下文扩展（LC-Phase）**：扩到 **1M token**；常数 LR 2.5e-6；**32-way context parallelism + 8-way tensor parallelism + 128-way expert parallelism + 2-way pipeline parallelism**，GB200 GPU 上训；blend = 长上下文 46% + Phase2 数据 54%（不用 RULER-style 数据）；MTP loss scaling 0.1，2 个 MTP 层。
- **后训练（核心：SFT + RLVR + MOPD）**
  - 初始 SFT 培育推理/工具使用/自主任务完成。
  - **统一 RLVR**：覆盖 reasoning/agentic/code/safety/usability/chat 多环境（multi-environment RLVR）。
  - 同时训 **>10 个领域专用 teacher**（含基于专门 agentic SFT path 的 agentic teacher）。
  - **MOPD（Multi-teacher On-Policy Distillation）**：通过 dense token-level 指导把多个 teacher 整合进 Ultra；含 MTP Boosting。
  - **reasoning budget control**（推理预算控制）。
- **性能**：推理吞吐相比公开 SOTA 最高约 6×，精度持平（GB200 上 NVFP4）。
- **开源**：Base / 后训练 / NVFP4 量化检查点 + 训练 recipe + 数据 + RL 环境（HuggingFace）。
- **来源**：arXiv https://arxiv.org/abs/2606.15007 ；本地 `2026/files/arxiv-2606.15007.pdf`

---

## 跨家族技术主线总结

- **数据质量信仰**：Phi（合成"教科书"）与 Nemotron（合成数据工业化 + 集成质量分类器 + edu 打分 + 改写提质）殊途同归；phi-4 合成占 40%、Nemotron-4-340B 对齐 >98% 合成、Nemotron-H 的 6.3T CC 中 1.9T 为合成改写。
- **合成数据 pipeline**：Nemotron-4-340B 开源完整 SDG（prompt 合成→回复→质量过滤→偏好排序）；Nemotron-H/Nano2 用 Qwen/Mixtral/340B/DeepSeek-R1 造 SFT-style token。
- **去重/过滤**：Nemotron-H 全局去重 + 5 桶 model-based 分类器集成 + 启发式/困惑度过滤 + 低质改写；数学用 Lynx+LLM 高保真抽取（Nemotron-CC-Math）。
- **架构演进**：Nemotron 从稠密(4-15B/340B) → hybrid Mamba-Transformer(H/Nano2) → hybrid Mamba MoE + LatentMoE + MTP(3 Super/Ultra)。Phi 基本保持稠密 Transformer，靠数据 + 后训练取胜，仅 phi-3.5-MoE 例外。
- **精度路线**：Nemotron-H-56B 首个全 FP8；Nemotron 3 全系 NVFP4（E2M1 + 16 micro-block + E4M3 scale + FP32 global）；Phi 用 bf16/fp16，未公开 FP8/FP4。
- **RL/对齐**：Nemotron-4-340B 首创 RPO；Llama-Nemotron / Nano2 / Cascade-2 / 3 Super/Ultra 用 GRPO（Cascade-2 去 KL 退化为 REINFORCE）；3 Ultra 用多环境 RLVR + 多教师 MOPD；Phi-4 用 Pivotal Token DPO，Phi-4-reasoning-plus 用 GRPO + rule-based length-aware reward。
- **蒸馏**：Nemotron 大量用 on-policy 蒸馏（MOPD）与压缩蒸馏（MiniPuzzle/Minitron/Puzzle NAS）；Phi 早期蒸馏 GPT teacher，phi-4 起声称"超越纯蒸馏"。

## 主要 gap（官方未公开或本次未查到精确数字）

- **phi-2**：层/头/隐藏维/tokenizer/数据精确配比全未公开（仅博客）。
- **phi-4 / phi-4-reasoning / phi-4-reasoning-vision**：精确层/头/MoE、训练 GPU 数与卡时未公开；reasoning-vision 的 RL 细节、精确 token 配比未给。
- **phi-3.5-MoE**：精确层数、训练 token 总量未单列。
- **Nemotron 3 Nano 30B-A3B backbone**：本次未下载其独立技术报告，30B-A3B 的层/专家/预训练 token 精确表来自该独立 Nano 报告（Cascade-2 与 Nano-Omni 仅引用）；建议补下 Nemotron 3 Nano 单独报告。
- **Nemotron 3 Super/Ultra 的 vocab/tokenizer 字符串、各阶段 RL 超参（KL/LR/batch）**：报告正文以方法为主，部分超参在附录或未逐一列出。
- **Nemotron 3 全系**的逐项数据来源百分比（仅给 Phase1/Phase2 大比例），细分领域 % 未全列。

---

## 来源清单（一手官方）

### Microsoft Phi
- phi-1: https://arxiv.org/abs/2306.11644 · `2023/files/textbooks-are-all-you-need-phi-1.pdf`
- phi-1.5: https://arxiv.org/abs/2309.05463 · `2023/files/phi-1-5.pdf`
- phi-2 (博客): https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/ · `2023/files/phi-2-microsoft-blog.html`
- phi-3: https://arxiv.org/abs/2404.14219 · `2024/files/2404.14219.pdf`
- phi-4: https://arxiv.org/abs/2412.08905 · `2024/files/2412.08905.pdf`
- phi-4-mini: https://arxiv.org/abs/2503.01743 · `2025/files/phi-4-mini.pdf`
- phi-4-reasoning: https://arxiv.org/abs/2504.21318 · `2025/files/phi-4-reasoning.pdf`
- phi-4-reasoning-vision-15B: https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf · HF https://huggingface.co/microsoft/Phi-4-reasoning-vision-15B · `2026/files/phi-4-reasoning-vision-15b-tech-report.pdf`

### NVIDIA Nemotron
- Nemotron-4 15B: https://arxiv.org/abs/2402.16819 · `2024/files/2402.16819.pdf`
- Nemotron-4 340B: https://arxiv.org/abs/2406.11704 · HF https://huggingface.co/nvidia/Nemotron-4-340B-Instruct · `2024/files/2406.11704.pdf`
- Nemotron-H: https://arxiv.org/abs/2504.03624 · `2025/files/nemotron-h.pdf`
- Nemotron Nano 2: https://arxiv.org/abs/2508.14444 · `2025/files/nemotron-nano-2.pdf`
- Llama-Nemotron: https://arxiv.org/abs/2505.00949 · HF https://huggingface.co/collections/nvidia/llama-nemotron · `2025/files/llama-nemotron.pdf`
- Nemotron-Cascade 2: https://arxiv.org/abs/2603.19220 · `2026/files/arxiv-2603.19220.pdf`
- Nemotron 3 Super: https://arxiv.org/abs/2604.12374 · https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf · `2026/files/arxiv-2604.12374.pdf`
- Nemotron 3 Nano Omni: https://arxiv.org/abs/2604.24954 · `2026/files/arxiv-2604.24954.pdf`
- Nemotron 3 Ultra: https://arxiv.org/abs/2606.15007 · `2026/files/arxiv-2606.15007.pdf`
