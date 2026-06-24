---
title: Gemma 家族训练配方深挖（Google DeepMind）
type: source
tags: [llm, gemma, google-deepmind, training-recipe, distillation, open-weights]
created: 2026-06-18
updated: 2026-06-18
sources: [gemma-1-arxiv-2403.08295, gemma-2-arxiv-2408.00118, gemma-3-arxiv-2503.19786, codegemma-arxiv-2406.11409, paligemma-arxiv-2407.07726, paligemma2-arxiv-2412.03555]
---

# Gemma 家族训练配方深挖

> 仅采用一手官方来源：arXiv 原文 PDF + 官方 HF model card 的 `config.json`。所有架构/训练数字均从官方技术报告原文逐字抠出；官方未写的明确标注「官方未公开」。
> 共精读 6 篇官方技术报告 PDF（已下载到本地 `deep-dive/files/`）。

## 家族演进脉络

- **Gemma 1（2024-02）**：从 Gemini 的研究与技术「下放」到轻量开放权重模型。2B/7B，纯文本、纯英语为主，next-token 预测训练，6T/3T token。架构沿用 Gemini：RoPE、GeGLU、RMSNorm、256k 词表；2B 用 MQA、7B 用 MHA。后续放出 1.1 版（改进 RLHF）。
- **Gemma 2（2024-06）**：2B/9B/27B。引入**知识蒸馏**（2B/9B 从大教师蒸馏，27B from scratch）、**局部/全局注意力交替（1:1）**、**GQA**、**logit soft-capping**、**pre-norm + post-norm 双 RMSNorm**。这是 Gemma 训练范式的关键转折——「用蒸馏在远超 compute-optimal 的 token 量上训小模型」。
- **Gemma 3（2025-03）**：1B/4B/12B/27B。新增**多模态（SigLIP 视觉编码器）**、**128K 长上下文**、**更广多语言**；架构改为**5:1 局部/全局注意力**以压 KV cache，**QK-norm 取代 soft-capping**，全局层 RoPE base 提到 1M；全系蒸馏；后训练用 BOND/WARM/WARP + 可验证奖励（数学 ground-truth、代码执行反馈）；提供 QAT 量化版。
- **CodeGemma（2024-04/05）**：基于 Gemma 1 继续训练 500B–1T token 代码语料，2B（100% 代码、FIM 补全）/7B（80% 代码 +20% NL）PT 与 IT。
- **PaliGemma（2024-07）**：SigLIP-So400m（400M）视觉编码器 + Gemma-1 2B 解码器，<3B VLM，三阶段（unimodal→multimodal 1B 例→分辨率提升）+ transfer 微调。
- **PaliGemma 2（2024-12）**：SigLIP-So400m + Gemma-2（2B/9B/27B），即 3B/10B/28B 三档 × 224/448/896px 三分辨率，沿用 PaliGemma 同样三阶段配方。

### 各代关键参数对比（仅文本主干 / 官方原文）

| 维度 | Gemma 1 2B | Gemma 1 7B | Gemma 2 2B | Gemma 2 9B | Gemma 2 27B | Gemma 3 1B | Gemma 3 4B | Gemma 3 12B | Gemma 3 27B |
|---|---|---|---|---|---|---|---|---|---|
| 层数 | 18 | 28 | 26 | 42 | 46 | 26 | 34 | 48 | 62 |
| d_model | 2048 | 3072 | 2304 | 3584 | 4608 | 1152 | 2560 | 3840 | 5376 |
| FFN 维 | 32768 | 49152 | 18432 | 28672 | 73728 | 6912 | 10240 | 15360 | 21504 |
| 头数 | 8 | 16 | 8 | 16 | 32 | 4 | 8 | 16 | 32 |
| KV 头数 | 1 (MQA) | 16 (MHA) | 4 (GQA) | 8 (GQA) | 16 (GQA) | 1 (GQA) | 4 (GQA) | 8 (GQA) | 16 (GQA) |
| head size | 256 | 256 | 256 | 256 | 128 | 256 | 256 | 256 | 128 |
| 注意力 | MQA | MHA | 局/全 1:1 GQA | 局/全 1:1 GQA | 局/全 1:1 GQA | 局/全 5:1 GQA | 局/全 5:1 GQA | 局/全 5:1 GQA | 局/全 5:1 GQA |
| 上下文 | 8192 | 8192 | 8192 | 8192 | 8192 | 32K | 128K | 128K | 128K |
| 词表 | 256128 | 256128 | 256128 | 256128 | 256128 | 262144 | 262208 | 262208 | 262208 |
| 训练 token | 3T | 6T | 2T | 8T | 13T | 2T | 4T | 12T | 14T |
| 训练方式 | next-token | next-token | 蒸馏 | 蒸馏 | from scratch | 蒸馏 | 蒸馏 | 蒸馏 | 蒸馏 |

> Gemma 3 的层数/维度/头数来自官方 HF gated repo `google/gemma-3-{1b,4b,12b,27b}-pt` 的 `config.json`（技术报告正文未列每模型表）。Gemma 1/2 来自报告 Table 1。激活均为 (近似) GeGLU，归一化均为 RMSNorm。

---

## Gemma 1（2B / 7B）

来源：`Gemma: Open Models Based on Gemini Research and Technology`，arXiv 2403.08295（2024-02-21）。

### 架构细节
- decoder-only Transformer。核心参数（Table 1）：2B → d_model 2048 / 18 层 / FFN 32768 / 8 头 / **KV 头 1（MQA）** / head size 256；7B → d_model 3072 / 28 层 / FFN 49152 / 16 头 / **KV 头 16（MHA）** / head size 256。
- 参数拆分（Table 2）：2B = embedding 524,550,144 + non-embedding 1,981,884,416；7B = embedding 786,825,216 + non-embedding 7,751,248,896。
- **Multi-Query Attention**：仅 2B 用 MQA（num_kv_heads=1），7B 用 MHA；依据「小规模下 MQA 表现良好」的消融（Shazeer 2019）。
- **RoPE**，每层旋转位置编码；输入输出 **embedding 共享（tied）** 以减小体积。RoPE base：官方未在 Gemma 1 报告中明确给出（Gemma 2 报告后续才注明沿用 10k 默认）。
- **GeGLU 激活**（用近似版替换标准 ReLU）。
- **RMSNorm**：对每个子层（注意力层、前馈层）的输入做归一化。
- 上下文长度 **8192**。
- tokenizer：Gemini 的 **SentencePiece** 子集，分割数字、不去多余空白、未知用 byte-level fallback；**vocab 256k**。

### 预训练数据
- 2B/7B 分别训练 **3T / 6T token**，主要为英语，来源：web 文档、数学、代码。**非多模态、非主打多语言**。
- 数据混合通过 2B/7B 上的一系列消融确定。**分阶段（staged）训练**：训练过程中改变语料混合，越到后期越加大「相关、高质量数据」的权重。

### 数据处理 pipeline
- 过滤目标：降低不安全/不良言论风险、剔除个人信息及敏感数据。
- 手段：**启发式 + 模型分类器**，移除有害或低质量内容。
- **从预训练混合中剔除所有评测集**，做**针对性污染分析**检查评测集泄漏；通过最小化敏感输出扩散降低 recitation 风险。
- PII：用 **Google Cloud Sensitive Data Protection** 工具识别个人/敏感数据（三级严重度，最高级=「sensitive」）。
- 分类器具体阈值：官方未公开。

### 数据配比
- 各领域百分比：官方未公开（只说 web/数学/代码三类）。
- 课程/退火：是，**stage training**，后期上采样高质量数据（具体阶段数与 token 量未公开）。

### 训练细节
- 硬件：**TPUv5e**，pod = 256 chips（16×16 2D torus）。7B 跨 **16 pod = 4096 TPUv5e**；2B 跨 **2 pod = 512 TPUv5e**。
- 并行：7B pod 内 **16-way model sharding + 16-way data replication**；2B 用 **256-way data replication**；optimizer state 用 **类 ZeRO-3** 进一步 shard；跨 pod 走 **Pathways** 的 data-replica reduce。
- 软件栈：JAX + Pathways「single controller」，**GSPMD partitioner**，**MegaScale XLA** 编译器。
- 精度/global batch/优化器/LR schedule/warmup：**官方未公开**（报告未列）。
- 碳足迹 ~131 tCO₂eq。

### SFT 细节
- 在「纯文本、纯英语」的合成 + 人工 prompt-response 对上做 SFT。
- 数据混合用 **LM-based side-by-side 评测**（大模型做裁判，CoT + rubric/constitution 对齐人类偏好）筛选。
- 合成数据做多级过滤：剔除 PII、不安全/有毒输出、错误自我认知、重复样本；加入鼓励「in-context 归因、hedging、拒答」的子集降低幻觉。

### RL / 对齐细节
- **RLHF**：人工偏好对 → 训练 **Bradley-Terry 奖励模型**（英语偏好数据）；策略用「一种新颖的 RL 算法」优化（未具名）。
- 用高容量模型做 automatic rater 与 baseline side-by-side 比较，缓解 reward hacking。
- KL/超参/算法名：官方未公开。
- 1.1 版：改进的 RLHF（报告主结果用 1.1 IT）。

### Formatting / 模板
- 控制 token：`<start_of_turn>`、`<end_of_turn>`，角色 `user`/`model`。

### AI infra
- 训练：JAX/Pathways/GSPMD/MegaScale XLA；推理/serving 开源 codebase（随模型发布）。量化：Gemma 1 报告未涉及。

---

## Gemma 2（2B / 9B / 27B）

来源：`Gemma 2: Improving Open Language Models at a Practical Size`，arXiv 2408.00118（2024-06-27，v3 2024-10）。

### 架构细节（Table 1 / Table 2）
- decoder-only。2B → d_model 2304 / 26 层 / FFN 18432 / 8 头 / **KV 头 4** / head size 256；9B → 3584 / 42 层 / 28672 / 16 头 / **KV 头 8** / head 256；27B → 4608 / 46 层 / 73728 / 32 头 / **KV 头 16** / head **128**。
- 参数拆分：2B = 590,118,912 + 2,024,517,888；9B = 917,962,752 + 8,324,201,984；27B = 1,180,237,824 + 26,047,480,320。
- **局部滑窗 / 全局注意力交替（每隔一层）**，比例 **1:1**。局部滑窗 = **4096** token，全局 span = **8192** token。
- **GQA**，num_groups = 2（消融显示推理更快、下游不掉点）。
- **Logit soft-capping**：`logits ← cap·tanh(logits/cap)`，自注意力层 cap=**50.0**，最终层 cap=**30.0**。
- **Pre-norm + Post-norm 双 RMSNorm**：每个子层输入和输出都归一化。
- RoPE、近似 GeGLU、上下文 8192、**tied embedding**，沿用 Gemma 1/Gemini。
- 「wide vs deep」消融：同参数量下**更深更好**，故选更深架构（Table 9）。

### 预训练数据
- token 量：**27B → 13T，9B → 8T，2B → 2T**，主要英语。来源：web 文档、代码、科学文章。非多模态、非主打多语言。
- tokenizer：同 Gemma 1/Gemini 的 **SentencePiece**（split digits、保留空白、byte-level），**vocab 256k**。
- 数据混合通过类 Gemini 1.0 的消融确定。

### 数据处理 pipeline
- 与 Gemma 1 同：过滤不安全言论、剔除 PII/敏感数据、从混合中**去污染评测集**、最小化敏感输出扩散降低 recitation。具体阈值未公开。

### 数据配比 / 阶段
- 各领域百分比：官方未公开。是否退火：报告未明示（Gemma 1 的 staged 做法可能延续，但 Gemma 2 报告只说「数据混合由消融确定」）。

### 训练细节（Table 3）
- 硬件：**TPUv4 / v5e / v5p**。
  - 2B：TPUv5e 2×16×16 = **512 chips**，**512-way data replication + 1-way model sharding**。
  - 9B：TPUv4 8×16×32 = **4096 chips**，**1024-way data + 4-way model sharding**。
  - 27B：TPUv5p 8×24×32 = **6144 chips**，**768-way data + 8-way model sharding**。
- optimizer state 用 **类 ZeRO-3**；跨 pod 走 Pathways data-replica reduce；JAX single-controller + GSPMD + MegaScale XLA。
- 精度 / global batch / 优化器 / LR schedule / warmup：**官方未公开**。
- 碳足迹 **1247.61 tCO₂eq**。

### 知识蒸馏（核心创新）
- 2B 与 9B **用蒸馏代替 next-token 预测**：以大语言模型为教师，最小化教师/学生 token 分布的负对数似然 `min Σ −P_T(x|x_c) log P_S(x|x_c)`。
- 关键思路：在**远超 compute-optimal 的 token 量**上蒸馏，以「模拟超出可用 token 数的训练」（2B/9B 训练 token 约为理论 compute-optimal 的 **50×**）。
- 27B **from scratch**（不蒸馏，13T token）。
- 消融：2B 在 500B token（约 compute-optimal 的 10×）上蒸馏（教师 7B）显著优于 from scratch（3 项均值 67.7 vs 60.3，Table 6）；蒸馏增益随模型规模保持（Table 7）。

### SFT 细节
- 在「纯文本、纯英语」合成 + 人工 prompt-response 对上做 SFT；扩展自 Gemma 1.1 的后训练数据，加入内外部公开数据。
- 用 **LMSYS-chat-1M 的 prompt（但不用其 answer）**。
- **行为克隆（behavioral cloning）**：在合成 + 真实 prompt 上，response **主要由教师（更大模型）合成生成**；还在学生分布上做**从教师的蒸馏**（on-policy distillation，Agarwal 2024 / Gu 2024）。

### RL / 对齐细节
- **RLHF**：算法类似 Gemma 1.1，但奖励模型**比策略大一个数量级**，且更偏向多轮对话能力；策略基于与 SFT 同样的 prompt。
- **Model merging（模型平均）**：对不同超参跑出的多个模型做权重平均（Ramé 2024），并把各阶段后的模型平均以提升整体性能。
- 偏好数据：英语偏好数据；规模/KL/具体超参：官方未公开。
- Formatting：同 Gemma 1 控制 token，但模型显式以 `<end_of_turn><eos>` 结束生成（Gemma 1 只生成 `<eos>`）。

### AI infra
- 训练框架同 Gemma 1（JAX/Pathways/GSPMD/MegaScale XLA）。
- 推理：滑窗大小可在推理时调小（消融显示 4096→1024 困惑度仅 1.63→1.64，可换取速度，Table 10）。

---

## Gemma 3（1B / 4B / 12B / 27B，多模态）

来源：`Gemma 3 Technical Report`，arXiv 2503.19786（2025-03-12）。架构每模型数字来自官方 HF gated repo `google/gemma-3-{1b,4b,12b,27b}-pt` 的 `config.json`。

### 架构细节
- decoder-only，沿用前两代大方向 + GQA + pre/post-norm 双 RMSNorm。
- 参数拆分（Table 1）：1B = 视觉 0 + emb 302M + non-emb 698M；4B = 视觉 417M + emb 675M + non-emb 3,209M；12B = 视觉 417M + emb 1,012M + non-emb 10,759M；27B = 视觉 417M + emb 1,416M + non-emb 25,600M。
- **每模型主干配置**（官方 config.json）：

| | 1B | 4B | 12B | 27B |
|---|---|---|---|---|
| 层数 | 26 | 34 | 48 | 62 |
| hidden_size | 1152 | 2560 | 3840 | 5376 |
| intermediate(FFN) | 6912 | 10240 | 15360 | 21504 |
| 头数 | 4 | 8 | 16 | 32 |
| KV 头 | 1 | 4 | 8 | 16 |
| head_dim | 256 | 256 | 256 | 128 |
| sliding_window | 512 | 1024 | 1024 | 1024 |
| max_position | 32768 | 131072 | 131072 | 131072 |
| rope_theta(global) | 1e6 | 1e6 | 1e6 | 1e6 |
| rope_local_base | 1e4 | 1e4 | 1e4 | 1e4 |
| query_pre_attn_scalar | 256 | 256 | 256 | 168 |
| vocab | 262144 | 262208 | 262208 | 262208 |

- **5:1 局部/全局注意力**：每 5 个局部滑窗层配 1 个全局层，第一层为局部层。局部 span 仅 **1024**（27B/12B/4B；1B 为 512），只有全局层 attend 长上下文 → 压制 KV-cache 爆炸。消融显示 5:1 甚至 7:1 对困惑度影响极小（Fig 3）。
- **QK-norm**：用 QK-norm **替换 Gemma 2 的 soft-capping**（受 Dehghani 2023 / Wortsman 2023 / Chameleon 启发）。
- **长上下文**：context 128K（1B 为 32K）。**全局层 RoPE base 从 10k 提到 1M**，局部层保持 10k。不从头训 128K，而是**先 32K 预训，末段把 4B/12B/27B 扩到 128K 并按位置插值 rescale RoPE（scaling factor = 8）**。
- tokenizer：**同 Gemini 2.0** 的 SentencePiece（split digits、保留空白、byte-level），**vocab 262k**，对非英语更均衡。
- 激活近似 GeGLU、RMSNorm 沿用。

### 视觉模态
- **SigLIP 400M 变体**（ViT，CLIP-loss 变体训练），输入 **896×896** 方图；4B/12B/27B **共享同一视觉编码器并冻结**；1B 无视觉。
- 图像→**256 个 soft token**（高分辨率编码器用 average pooling 压到 256）。
- **Pan & Scan（P&S）**：推理期自适应窗口，把非方形/高分图切成等大不重叠 crop 各 resize 到 896×896，仅按需启用、可关闭。提升 DocVQA/InfoVQA 等读图文任务（27B w/ P&S DocVQA +4.8、InfoVQA +17.0，Table 8）。

### 预训练数据
- token 量：**27B → 14T，12B → 12T，4B → 4T，1B → 2T**（比 Gemma 2 略多，含图文混合）。
- **增加多语言数据**（单语 + 平行语料），用 Chung 2023 启发的策略处理语言不平衡。
- 来源：web/代码/科学等（同前代基调）；图文混合。

### 数据处理 pipeline
- 同前代：过滤不安全言论、剔除 PII/敏感数据、**去污染评测集**、最小化敏感输出降 recitation。
- 新增 **质量重加权（quality reweighing）** 步骤（受 Sachdeva 2024 启发）降低低质数据出现频率。
- 分类器/阈值具体值：官方未公开。

### 数据配比 / 阶段
- 各领域百分比：官方未公开。**重新调整数据混合以增强多语言**。
- 长上下文为**末段阶段**（32K→128K rescale），见上。

### 训练细节（Table 2）
- 硬件：**TPUv4 / v5e / v5p**，每配置优化以最小化 step 时间。
  - 1B：TPUv5e 512 chips，sharding data 16 / seq 16 / replica 2。
  - 4B：TPUv5e 2048 chips，16 / 16 / 8。
  - 12B：TPUv4 6144 chips，16 / 16 / 24。
  - 27B：TPUv5p 6144 chips，data 24 / seq 8 / replica 32。
- 视觉编码器**预计算 embedding** 后直接训练，对 LM 训练零额外开销。
- optimizer state 用 **ZeRO-3 实现**；多 pod 走 Pathways data-replica reduce；JAX single-controller + GSPMD + MegaScale XLA。
- 精度 / global batch / 优化器 / LR / warmup：**官方未公开**（QAT 阶段除外，见下）。

### 蒸馏（全系）
- 全部 Gemma 3 模型用知识蒸馏。**每 token 采样 256 个 logits**，按教师概率加权；学生用 cross-entropy 学这些采样内的教师分布；非采样 logits 概率置零并重归一化。
- 「小 vs 大教师」消融：短训程小教师更好，长训程大教师更好（Fig 8）。

### 量化感知训练（QAT）
- 随 raw checkpoint 同时放出 QAT 量化版：每个模型**额外微调约 5000 步**，以**非量化 checkpoint 的概率为目标**，数据匹配预/后训练分布。
- 三种权重表示：**per-channel int4、per-block int4、switched fp8**（面向 llama.cpp 等开源量化引擎）。
- 显存对比见 Table 3（如 27B bf16 54GB → int4 14.1GB）。

### SFT / 后训练
- PT→IT 用「改进版后训练」（优于此前 recipe）。
- **从大 IT 教师做改进版知识蒸馏**（Agarwal 2024 / Anil 2018 / Hinton 2015）+ **RL 微调阶段**。
- 数据过滤：剔除 PII、不安全/有毒输出、错误自我认知、重复样本；加 in-context 归因/hedging/拒答子集降幻觉。

### RL / 对齐细节
- RL 微调基于改进版 **BOND（Sessa 2024）、WARM（Ramé 2024b）、WARP（Ramé 2024a）**。
- 多种奖励函数提升 helpfulness/数学/代码/推理/指令遵循/多语言，**最小化有害性**，包括：
  - **权重平均奖励模型（WARM）** 用人类反馈数据训练；
  - **代码执行反馈**（Gehring 2024）；
  - **数学 ground-truth 可验证奖励**（引用 DeepSeek-AI 2025 与 Lambert 2024 → 即 RLVR 路线）。
- 偏好数据规模 / KL / 具体超参：官方未公开。

### Formatting / 模板
- IT：`<start_of_turn>user … <end_of_turn>`、`<start_of_turn>model … <end_of_turn>`；PT/IT 文本前需显式加 `[BOS]`（`add_bos=True`）。PT 模型以 `<eos>` 结束，IT 模型以 `<end_of_turn>` 结束。

### AI infra
- 训练 JAX/Pathways/GSPMD/MegaScale XLA + ZeRO-3。
- 长上下文工程：5:1 局/全 + 短局部滑窗 + 全局层 RoPE 1M + 末段 32K→128K RoPE rescale（factor 8），把 32K 时 KV-cache 开销从 global-only 的 ~60% 降到 1:3+sw1024 的 <15%（Fig 5）。
- serving/量化：int4/fp8 QAT，面向 llama.cpp 等。

---

## CodeGemma（2B / 7B，基于 Gemma 1）

来源：`CodeGemma: Open Code Models Based on Gemma`，arXiv 2406.11409（2024-05-08，v2 2024-06）。

### 架构细节
- **完全沿用 Gemma 1 架构**（2B/7B 同款），无新结构。报告强调 2B 的速度优势来自 Gemma 基座的架构选择。

### 预训练数据
- 从 Gemma 1 PT 继续训练：**v1.0 全部 +500B token**（以英语 web/数学/代码为主）；**2B v1.1 训练 1T token**。
- 配比：**所有 2B 模型 100% 代码**；**7B 模型 80% 代码 + 20% 自然语言**。
- 代码语料来自公开代码仓库。

### 数据处理 pipeline
- 在 Gemma 处理基础上对代码额外处理：**去重 + 过滤**剔除评测代码污染与部分 PII/敏感数据。
- **FIM（Fill-in-the-Middle）预处理**：基于 Bavarian 2022 改进；**FIM rate 多数模型 80%，2B v1.1 为 90%**；支持 PSM 与 SPM 两种模式；控制 token：`<|fim_prefix|>`/`<|fim_middle|>`/`<|fim_suffix|>`/`<|file_separator|>`。
- **多文件打包**：依赖图打包（提 import、suffix 匹配最长路径、去环、全对最短路、拓扑排序线性化）+ 单测词法打包（TestFoo.java 紧挨 Foo.java）。

### SFT 细节
- 数据 = 开源数学数据集 + 合成代码 + Gemma 的微调数据。
- **数学数据集**：MATH（12,500 题）、GSM8k（8,500 题）、MathQA、合成代数数据 → 提升逻辑/解题。
- **合成代码**：按 OSS-Instruct（Wei 2023）生成自包含 QA 对，再用 LLM 对 helpfulness/correctness 做 post-filtering。

### RL / 对齐细节
- SFT + **RLHF**（7B v1.1 的 RL 算法基于 **Gemma 1.1**，与 v1.0 不同，且合成数据生成细节不同）。
- 具体 RL 超参：官方未公开。

### Inference
- PT 用于代码补全（FIM）；IT 用 `<start_of_turn>`/`<end_of_turn>`。

---

## PaliGemma（3B VLM，SigLIP + Gemma-1 2B）

来源：`PaliGemma: A versatile 3B VLM for transfer`，arXiv 2407.07726（2024-07，v2 2024-10）。

### 架构细节
- 三件套：① **SigLIP-So400m** 视觉编码器（公开 checkpoint，shape-optimized ViT-So400m，约 400M，sigmoid 对比 loss 预训练）；② **Gemma-2B v1.0 raw PT** 解码器；③ **零初始化线性投影**把 SigLIP 输出映射到 Gemma 词嵌入维度（消融显示 MLP 无明显优势，故用最简线性层）。
- 图像 resize 到固定方形 224/448/896 → 分别 **256/1024/4096 image token**，放在序列最前。
- **Prefix-LM masking**：图像 + prefix 全（双向）注意力，suffix 自回归（含 PAD）。
- SEP token 单独 tokenize，BOS 标记文本起点。

### 训练流程（4 阶段）
- **Stage 0 unimodal**：直接用现成 SigLIP + Gemma checkpoint，不做自定义单模态预训练。
- **Stage 1 multimodal**：合并后**全模型联合训练**（不冻结视觉编码器，反常规——为多学技能；对图像编码器 LR 做缓慢 warm-up 防初期错位梯度破坏其表征）。分辨率 224px（256 img token）、序列长 N_txt=128、**共 1B 例**。
- **Stage 2 分辨率提升**：先 448×448 **+50M 例**，再 896×896 **+10M 例**；同 Stage1 任务混合但上采样高分任务，序列长增到 512。
- **Stage 3 transfer**：全参数微调到具体任务。可调超参（重要性降序）：分辨率/checkpoint、epoch(1/3/10/30/100)、LR(3e-5/1e-5/3e-6)、label smoothing(0/0.1/0.3)、LLM dropout(0/0.1/0.3)、weight decay(0 或 0.1×LR)、是否冻结 ViT、captioning 可用 beam-search。

### 预训练任务混合（Stage1/2）
- caption {lang}（WebLI 100+ 语言、CC3M-35L）、ocr（公开 OCR 系统转写全图文本）、answer en {question}（CC3M-35L 生成 VQA，35 语言提问/英文答）、OpenImages 物体中心问答、detection、segmentation 等。目标是**练「技能」而非开箱即用**；移除所有 transfer 数据集近重复图像防污染。

### 训练细节
- 硬件：Cloud TPUv5e（PaliGemma 2 报告追溯说明）。精度/卡数/优化器：PaliGemma 报告未详列（部分见 PaliGemma 2）。

---

## PaliGemma 2（3B / 10B / 28B VLM，SigLIP + Gemma-2）

来源：`PaliGemma 2: A Family of Versatile VLMs for Transfer`，arXiv 2412.03555（2024-12-04）。

### 架构细节
- **SigLIP-So400m/14**（patch 14px，与 PaliGemma 同款视觉编码器）+ **Gemma 2（2B/9B/27B）** 解码器 + 线性投影。
- 三档总参（Table 1）：**3B（视觉+Gemma2-2B）/ 10B（9.7B，Gemma2-9B）/ 28B（27.7B，Gemma2-27B）**。
- 三分辨率：224/448/896px → 256/1024/4096 image token。
- 视觉编码器参数相对小，但 LLM 内的 vision token 主导算力。

### 训练流程（与 PaliGemma 完全相同的三阶段）
- **Stage 0**：单模态预训练的现成 SigLIP-So400m + Gemma 2 **raw checkpoint（无后训练）**。
- **Stage 1**：224px²，多模态任务混合 **1B 例**，不冻结任何参数。
- **Stage 2**：448px² **50M 例** → 896px² **10M 例**，上采样高分任务、增长输出序列（练长 OCR）。
- **Stage 3**：对具体目标任务微调。

### 训练细节
- 硬件：Cloud **TPUv5e** pod slice；**28B 在 896px² 用 TPUv5p**（假设单芯 2.3× 加速）。
- 相对训练成本（每例，Table 1）：3B 1.0/4.6/23.5；10B 3.7/18.3/67.7；28B 18.9/63.5/~155.6（对应 224/448/896）。
- 发现：几乎所有任务都吃算力；**大模型最优 transfer LR 更低**；分析了分辨率 vs 模型规模对不同任务的增益差异。
- 还做了 CPU 端低精度部署基准（Sec 4.9）。
- 精度/优化器/global batch：官方未详列。

---

## 来源清单

| 型号 | 官方来源 URL | 本地文件 |
|---|---|---|
| Gemma 1 | https://arxiv.org/abs/2403.08295 (PDF https://arxiv.org/pdf/2403.08295) | `deep-dive/files/gemma_2403.08295.pdf` / `.txt` |
| Gemma 2 | https://arxiv.org/abs/2408.00118 (PDF https://arxiv.org/pdf/2408.00118) | `deep-dive/files/gemma_2408.00118.pdf` / `.txt` |
| Gemma 3 | https://arxiv.org/abs/2503.19786 (PDF https://arxiv.org/pdf/2503.19786) | `deep-dive/files/gemma_2503.19786.pdf` / `.txt` |
| CodeGemma | https://arxiv.org/abs/2406.11409 (PDF https://arxiv.org/pdf/2406.11409) | `deep-dive/files/gemma_2406.11409.pdf` / `.txt` |
| PaliGemma | https://arxiv.org/abs/2407.07726 (PDF https://arxiv.org/pdf/2407.07726) | `deep-dive/files/gemma_2407.07726.pdf` / `.txt` |
| PaliGemma 2 | https://arxiv.org/abs/2412.03555 (PDF https://arxiv.org/pdf/2412.03555) | `deep-dive/files/gemma_2412.03555.pdf` / `.txt` |
| Gemma 3 每模型 config.json | https://huggingface.co/google/gemma-3-1b-pt / -4b-pt / -12b-pt / -27b-pt（gated；config 字段值与 unsloth 等开放镜像字节一致，已逐字核对） | — |

> 说明：Gemma 系列各报告**普遍未公开**：精确 global batch、优化器名与 LR schedule/warmup（QAT 5000 步除外）、各领域数据百分比、RL 的 KL/具体超参与偏好数据规模、Gemma 1/2 的 RoPE base 数值（Gemma 3 明确 global 1M / local 10k）、训练总卡时/FLOPs/训练时长。这些已在各小节标注「官方未公开」。
