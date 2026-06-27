# Qwen（通义千问，阿里巴巴）训练配方深挖

> 家族：Qwen / 通义千问，阿里巴巴 Qwen Team（前身达摩院）。
> 本文只收一手官方来源（arXiv 原文、官方 technical report、官方博客 qwenlm.github.io / qwen.ai、官方 GitHub / HF model card）。所有架构/数据/训练数字均抠自原文 PDF 或官方博客；查不到的标注「官方未公开」。
> 撰写日期：2026-06-18。2025 下半年及 2026 内容以联网检索官方博客为准。

---

## 家族演进脉络（一句话版）

- **Qwen (v1)，2023-08/09**：1.8B/7B/14B（后补 72B/1.8B）dense；3T token；首份技术报告确立 Qwen 架构基线（tiktoken cl100k 扩词表→152K、untied embedding、RoPE-FP32、QKV-bias、Pre-Norm+RMSNorm、SwiGLU 8/3h），SFT+RM+RLHF（PPO）。
- **Qwen1.5，2024-02**：把 Qwen 全系（0.5B→110B）+ 首个 MoE（A2.7B）以统一接口重发，无独立 paper（官方博客 + HF），引入 GQA 趋势、SwiGLU、32K 上下文实验，过渡版本。
- **Qwen2，2024-06**：0.5/1.5/7/72B dense + 57B-A14B MoE（upcycle 自 7B）；7T token（0.5B 用 12T）；全面 GQA、DCA+YaRN 长上下文（128K）、RoPE base 1e6；后训练 SFT(500K)+DPO（offline+online）。
- **Qwen2.5，2024-09/12**：0.5/1.5/3/7/14/32/72B dense + MoE（Turbo/Plus，未开权重）；**18T token**；后训练 SFT(>1M)+两阶段 RL（offline DPO 150K + online GRPO）；Turbo 上下文 1M。
- **专用线**：Qwen2.5-Coder（5.5T 代码，70:20:10 配比，FIM，三阶段）、Qwen2.5-Math（CoT+TIR，RM+GRPO）。
- **QwQ-32B，2025-03**：基于 Qwen2.5-32B 的推理模型，纯 RL scaling（math/code 用 verifier + 通用 RL），对标 DeepSeek-R1（671B）。
- **Qwen2.5-Max，2025-01**：超大 MoE，20T+ token，API only（未开权重）。
- **Qwen3，2025-04/05**：0.6/1.7/4/8/14/32B dense + 30B-A3B / 235B-A22B MoE；**36T token、119 语言**；架构去 QKV-bias、加 QK-Norm、MoE 无共享专家+global-batch load balance；后训练四阶段（long-CoT 冷启动→Reasoning RL(GRPO)→Thinking Mode Fusion→General RL）+ 强到弱蒸馏；hybrid thinking（/think、/no_think）。
- **Qwen3 "2507" 更新，2025-07**：放弃 hybrid thinking，改为分别发布 Instruct 与 Thinking 模型，扩 256K 上下文（如 Qwen3-235B-A22B-Instruct-2507 / Thinking-2507、Qwen3-30B-A3B-2507）。
- **Qwen3-Coder，2025-07**：480B-A35B MoE，7.5T（70% 代码），256K（YaRN→1M），大规模 agentic Code RL（2 万并行环境）。
- **Qwen3-Max，2025-09**：>1T 总参 MoE，36T token，API only；PAI-FlashMoE + ChunkFlow infra。
- **Qwen3-Next，2025-09**：80B-A3B 全新混合架构（Gated DeltaNet+Gated Attention 3:1）+ 极致稀疏 MoE（512 专家激活~3B）+ MTP；仅 15T token，GPU 算力为 Qwen3-32B 的 9.3%。
- **多模态线**：Qwen-VL(2023)→Qwen2-VL(2024)→Qwen2.5-VL(2025)；Qwen-Audio(2023)→Qwen2-Audio；Qwen2.5-Omni(2025, Thinker-Talker)→Qwen3.5-Omni(2026, Hybrid-Attn MoE 双塔)。

---

## 各代关键参数对比（dense/MoE 旗舰）

- **Qwen-14B (v1, 2023)**：dense；40 层 / hidden 5120 / 40 头 MHA；FFN=8/3·h；vocab≈152K；ctx 2048（推理外推 8K+）；训练 3.0T；SwiGLU/RMSNorm/RoPE-FP32/QKV-bias。
- **Qwen2-72B (2024)**：dense；80 层 / hidden 8192 / 64 Q 头 / 8 KV 头 (GQA)；FFN(inter) 29568；vocab 151646；ctx 128K(DCA+YaRN，RoPE base 1e6)；训练 7T。
- **Qwen2-57B-A14B (2024)**：MoE（upcycle 7B）；28 层 / hidden 3584 / 28Q4KV；64 路由专家(激活8)+8 共享专家；每专家 inter 2560；训练 4.5T。
- **Qwen2.5-72B (2024)**：dense；80 层 / 64Q8KV；vocab 151643（控制 token 3→22）；ctx 128K；训练 18T。
- **Qwen3-235B-A22B (2025)**：MoE；94 层 / 64Q4KV；128 专家(激活8)、无共享专家、global-batch LB；vocab 151669；ctx 128K（2507 版 256K）；训练 36T；QK-Norm、去 QKV-bias。
- **Qwen3-32B (2025)**：dense；64 层 / 64Q8KV；ctx 128K；训练 36T。
- **Qwen3-Coder-480B-A35B (2025)**：MoE；ctx 256K(YaRN→1M)；训练 7.5T(70% 代码)。
- **Qwen3-Next-80B-A3B (2025)**：混合(Gated DeltaNet:Gated Attn=3:1)+MoE 512 专家(10 路由+1 共享，激活~3B)；MTP；ctx 256K(YaRN→1M)；训练 15T。
- **Qwen3-Max (2025)**：MoE >1T 总参；训练 36T；API only。

---

## Qwen (v1) — 2023-08/09

来源：Qwen Technical Report（arXiv 2309.16609）。本地：`../../../sources/llm/2023/qwen-technical-report.pdf`

### 架构细节（Table 1）
- 规格：**1.8B**（hidden 2048 / 16 头 / 24 层），**7B**（hidden 4096 / 32 头 / 32 层），**14B**（hidden 5120 / 40 头 / 40 层）；注意力为 MHA（v1 未用 GQA）。
- FFN：SwiGLU，FFN 维度由 4h 降为 **8/3·h**。
- Embedding：**untied** input/output（不共享权重，换性能）。
- 位置编码：**RoPE**，逆频率矩阵用 **FP32**（而非 BF16/FP16）以保精度。
- Bias：多数层去 bias（follow PaLM），但**注意力 QKV 层保留 bias** 以增强外推。
- Norm：**Pre-Norm + RMSNorm**。
- Tokenizer：BBPE，起点 tiktoken **cl100k_base**，扩充中文等多语言，数字按单字拆分，最终 vocab **≈152K**。
- 上下文：训练 ctx **2048**；推理期免训练扩展——**NTK-aware 插值 + dynamic NTK + LogN-Scaling + 分层 window attention**（低层短窗、高层长窗），可保持 8192+ 低 PPL。

### 预训练数据
- 总量 **up to 3T token**（多领域文本+代码，多语言，英中为主）。
- 来源：public web、百科、书籍、代码等。
- 数据处理 pipeline：HTML 抽文本→语言识别→去重（normalize 后 exact-match + **MinHash+LSH** 模糊去重）→质量过滤（规则 + ML：语言模型打分、文本质量打分模型、识别冒犯/不当内容模型）+ 人工抽检；对高质量来源**选择性上采样**；混入高质量指令数据；用 13-gram overlap 做**测试集去污染**。

### 训练细节
- 优化器 AdamW（β1=0.9, β2=0.95, ε=1e-8）；cosine LR，峰值 LR=**3.0e-4**（三个尺寸同）；衰减到峰值 10%；batch size **4M**；**BF16** 混合精度；FlashAttention。
- 训练 token：1.8B=2.2T，7B=2.4T，14B=3.0T。
- 算力/并行/卡时：**官方未公开**。

### SFT
- ChatML 风格模板；人工标注多风格对话（含 safety）；刻意排除可能限制能力的 prompt 模板化数据。
- 训练：next-token，掩码 system/user 输入；AdamW，seq len 2048，**batch 128，4000 steps**，LR warmup。

### RL/对齐
- 流程：SFT → 训 **奖励模型 RM**（Qwen-PMP 偏好预训练 → Qwen-RM）→ **RLHF（PPO）**。产出 Qwen-Chat 与 Qwen-Chat-RLHF。
- RM/PPO 具体超参（KL 系数等）报告未细列。

### 专用模型
- **Code-Qwen 7B/14B**（代码继续预训练）+ Code-Qwen-Chat；**Math-Qwen 7B/14B-Chat**（数学 SFT，GSM8K 接近 GPT-3.5）。
- **Qwen-VL / Qwen-VL-Chat**（见多模态小节）。

来源 URL：https://arxiv.org/abs/2309.16609 ｜ pdf https://arxiv.org/pdf/2309.16609 ｜ github https://github.com/QwenLM/Qwen

---

## Qwen1.5 — 2024-02（过渡版，无独立 paper）

- 性质：**官方博客 + HF model card 形式**发布，无独立技术报告（官方在 Qwen2 报告中以 "Qwen1.5 (Qwen Team, 2024a)" 引用）。
- 尺寸：0.5B / 1.8B / 4B / 7B / 14B / 32B / 72B / **110B** dense + 首个 **Qwen1.5-MoE-A2.7B**（fine-grained experts + 共享专家路由，14.3B 总参激活 2.7B，upcycle）。
- 架构要点（据官方博客/HF config 与 Qwen2 报告回溯）：SwiGLU、RoPE、RMSNorm、QKV-bias；部分尺寸用 GQA；统一支持 **32K 上下文**实验；vocab 同 Qwen ≈151.6K。
- 预训练数据：约 **3T token**（Qwen2 报告称 Qwen1.5 用 3T，Qwen2 扩到 7T）。
- 后训练：SFT + DPO（官方博客口径）。
- 大量精确数字（各尺寸层数/头数/训练 token、卡时）官方未在统一报告中公开，需查各 HF config。

来源：官方博客 https://qwenlm.github.io/blog/qwen1.5/ ｜ MoE https://qwenlm.github.io/blog/qwen-moe/ ｜ github https://github.com/QwenLM/Qwen1.5（本地无落盘）

---

## Qwen2 — 2024-06

来源：Qwen2 Technical Report（arXiv 2407.10671）。本地：`../../../sources/llm/2024/qwen2.pdf`

### 架构（Table 1）
| 配置 | 0.5B | 1.5B | 7B | 72B | 57B-A14B(MoE) |
|---|---|---|---|---|---|
| Hidden | 896 | 1536 | 3584 | 8192 | 3584 |
| 层数 | 24 | 28 | 28 | 80 | 28 |
| Q 头 | 14 | 12 | 28 | 64 | 28 |
| KV 头 (GQA) | 2 | 2 | 4 | 8 | 4 |
| Head size | 64 | 128 | 128 | 128 | 128 |
| Inter size | 4864 | 8960 | 18944 | 29568 | 2560(每专家) |
| 路由专家 | - | - | - | - | 64 |
| 激活专家 | - | - | - | - | 8 |
| 共享专家 | - | - | - | - | 8 |
| Embed tying | True | True | False | False | False |
| Vocab | 151646 | 同 | 同 | 同 | 同 |
| 训练 token | 12T | 7T | 7T | 7T | 4.5T |

- 全面改用 **GQA**（替代 v1 MHA）；保留 SwiGLU/RoPE/QKV-bias/RMSNorm+Pre-Norm。
- MoE：**fine-grained experts**（细粒度专家）+ **shared & routing experts**（共享+路由专家）；57B-A14B 由 **Qwen2-7B upcycle**（每 fine-grained 专家随机重初始化 50% 参数引入多样性）。
- 长上下文：**DCA（Dual Chunk Attention）+ YaRN**；ctx 4096→32768（收尾阶段），RoPE base **10000→1000000**；推理可达 **131072**。

### 预训练数据 / pipeline
- 总量从 Qwen1.5 的 3T 扩到 **7T token**（曾试 12T 但收益不显著，仅 0.5B 用 12T；MoE 额外 4.5T）。
- 约 **30 种语言**。
- 质量提升：启发式 + model-based 过滤，**用 Qwen 模型本身过滤低质并合成高质量数据**；小模型实验优化数据 mixture（distribution improvement）。混入高质量多任务指令数据。

### 训练细节
- scaling law / LR / batch / 卡时 / 并行：报告未给完整数字（**算力与并行策略官方未公开**）。

### SFT
- 指令数据 **>500,000 例**（指令遵循、代码、数学、逻辑、角色扮演、多语言、安全）；2 epoch，seq len 32768，LR 7e-6→7e-7，weight decay 0.1，grad clip 1.0。
- 数据构造：协同标注（InsTag 本体抽取→指令选择→指令自进化→人工排序）+ 自动合成（**Rejection Sampling**、Execution Feedback、Data Repurposing、Constitutional Feedback）。

### RL/对齐
- **两阶段 DPO**：offline DPO（预编译偏好集）+ online DPO（policy 采样多答案、RM 选最优/最劣组对，每 episode DPO）；用 **Online Merging Optimizer** 缓解 alignment tax。

来源 URL：https://arxiv.org/abs/2407.10671 ｜ pdf https://arxiv.org/pdf/2407.10671 ｜ github https://github.com/QwenLM/Qwen2

---

## Qwen2.5（+ Coder / Math）— 2024-09 / 2024-12

来源：Qwen2.5 Technical Report（arXiv 2412.15115）。本地：`../../../sources/llm/2024/qwen2.5.pdf`

### 架构（Table 1，开权重 dense）
| 模型 | 层数 | Q/KV 头 | Tie Emb | Ctx/Gen | License |
|---|---|---|---|---|---|
| 0.5B | 24 | 14 / 2 | Yes | 32K/8K | Apache2.0 |
| 1.5B | 28 | 12 / 2 | Yes | 32K/8K | Apache2.0 |
| 3B | 36 | 16 / 2 | Yes | 32K/8K | Qwen Research |
| 7B | 28 | 28 / 4 | No | 128K/8K | Apache2.0 |
| 14B | 48 | 40 / 8 | No | 128K/8K | Apache2.0 |
| 32B | 64 | 40 / 8 | No | 128K/8K | Apache2.0 |
| 72B | 80 | 64 / 8 | No | 128K/8K | Qwen |

- GQA + RoPE + SwiGLU + QKV-bias + RMSNorm/Pre-Norm（沿用 Qwen2）。MoE（Turbo/Plus）用 fine-grained + 共享专家路由（**未开权重**）。
- Tokenizer：BBPE，vocab **151643**，控制 token 从 3 扩到 **22**（含 2 个 tool token），全系统一词表。
- 长上下文：两阶段（4096→32768，RoPE base 1e6 ABF）；**Turbo 渐进式** 32K→64K→128K→**262144**（RoPE base 1e7，40% 当前最长+60% 短）；推理 YaRN+DCA，Turbo 达 **1M**。

### 预训练数据 / pipeline
- 总量从 Qwen2 的 7T 扩到 **18T token**。
- 改进：(1) 用 **Qwen2-Instruct 当多维质量打分过滤器**；(2) 并入 Qwen2.5-Math / Qwen2.5-Coder 数据；(3) Qwen2-72B-Instruct + Qwen2-Math-72B-Instruct 合成数据，再用 general RM + Qwen2-Math-RM-72B 过滤；(4) **数据 mixture 优化**：下采样过曝领域（电商/社媒/娱乐），上采样高价值领域（科技/科学/学术）。
- 去污染：n-gram，LCS≥13 且 LCS≥0.6·min(|st|,|se|) 则剔除。
- **scaling law for 超参**：用 44M~14B dense、44M~1B 激活 MoE，0.8B~600B token 数据，预测最优 LR/batch。

### SFT
- **>1,000,000 例**；2 epoch，seq len 32768，LR 7e-6→7e-7，wd 0.1，grad clip 1.0。
- 9 大方向：长序列生成（≤8192，back-translation 造 query）、数学（Qwen2.5-Math CoT + rejection sampling）、代码（Qwen2.5-Coder，~40 语言多 agent + 多语言沙箱单测）、指令遵循（代码验证 + execution-feedback rejection sampling）、结构化数据、逻辑推理（70K 新 query）、跨语言、鲁棒系统指令、响应过滤（critic + 多 agent 评分）。

### RL/对齐（两阶段）
- **Offline RL（DPO）**：聚焦推理/事实/指令遵循等 RM 难评任务；复用 execution-feedback + answer-matching 流水，SFT 模型重采样，过检为正/不过为负；约 **150,000 训练对**；1 epoch，**Online Merging Optimizer**，LR 7e-7。
- **Online RL（GRPO）**：RM 标注准则（truthfulness/helpfulness/conciseness/relevance/harmlessness/debiasing）；query 按 RM 打分方差排序（高方差优先），每 query 采 **8 个响应**；**global batch 2048、每 episode 2048 样本**。
- 长上下文 SFT 两阶段（短≤32K → 短+长≤262144），RL 仅用短指令（长上下文 RL 太贵 + 缺 RM）。

来源 URL：https://arxiv.org/abs/2412.15115 ｜ pdf https://arxiv.org/pdf/2412.15115 ｜ github https://github.com/QwenLM/Qwen2.5

### Qwen2.5-Coder（arXiv 2409.12186）
本地：`../../../sources/llm/2024/qwen2.5-coder.pdf`
- 尺寸：0.5/1.5/3/7/14/32B（架构衍生自 Qwen2.5）；vocab 151646；新增 FIM/repo 特殊 token（`<|fim_prefix/middle/suffix/pad|>`、`<|repo_name|>`、`<|file_sep|>`，ID 151659-151664）。各尺寸训练 **5.5T token**。
- 数据：5 类（Source Code / Text-Code Grounding / Synthetic / Math / Text）；GitHub 公开仓库（2024-02 前，**92 种语言**），规则过滤 + 弱模型分类器/打分器。
- **数据配比**：实验 100:0:0 vs 85:10:5 vs 70:20:10 → 选 **Code:Text:Math = 70:20:10**，最终训练集 **5.2T token**。
- 三阶段训练：① File-Level（seq 8192，5.2T，next-token + FIM）② Repo-Level（ctx 8192→32768，RoPE base 10000→1000000，YaRN→128K，~300B 长上下文）③ Alignment（SFT + DPO）。
- 指令数据：CodeBERT 语言识别（~100 语言）、GitHub 代码片段反向造指令、多语言多 agent 协同合成、checklist 评分、多语言沙箱静态检查+单测。
- URL：https://arxiv.org/abs/2409.12186 ｜ pdf https://arxiv.org/pdf/2409.12186

### Qwen2.5-Math（arXiv 2409.12122）
本地：`../../../sources/llm/2024/qwen2.5-math.pdf`
- 尺寸：1.5B/7B/72B + Qwen2.5-Math-RM；从 Qwen2.5 base 初始化继续预训练（ctx **4K**）。
- 预训练语料：**Qwen Math Corpus v1 ≈700B**（Qwen2-Math 用）→ **v2 >1T**（Qwen2.5-Math 用）；FastText 分类器迭代召回 Common Crawl 数学数据 + URL meta 扩池 + MinHash 去重 + Qwen2-0.5B-Instruct 质量过滤 + Qwen2-72B-Instruct 合成 QA。
- 后训练：**CoT + TIR（Tool-Integrated Reasoning，Python 解释器）** 联合 SFT（3 epoch，seq 4096；72B batch 256 LR 5e-6，1.5B/7B batch 128 LR 2e-5，衰减到 7e-7）；CoT 集 580K 英文 + 500K 中文（MuggleMath 进化、难度打分），最终 2000K 英 + 500K 中。
- RL：训 **Qwen2.5-Math-RM**（大规模采样）→ rejection sampling 造 SFT 数据 + **GRPO** RL + 推理期 best-of-N。
- URL：https://arxiv.org/abs/2409.12122 ｜ pdf https://arxiv.org/pdf/2409.12122

---

## QwQ-32B — 2025-03（推理模型，纯 RL scaling）

来源：官方博客 https://qwen.ai/blog?id=qwq-32b （原 https://qwenlm.github.io/blog/qwq-32b/）
- 性质：基于 **Qwen2.5-32B** 的开放权重推理模型（Apache 2.0），**32B 参数对标 DeepSeek-R1 671B（激活37B）**。
- 架构：沿用 Qwen2.5-32B dense（64 层 / 40Q8KV / 128K ctx）；无新结构创新（重点在 RL）。
- 训练方法：从 **cold-start checkpoint** 出发，**outcome-based reward 驱动的 RL scaling**：
  - 第一阶段：math/code 专项 RL，**不用 RM**，math 用 **accuracy verifier**（校验最终答案正确性），code 用 **code execution server**（跑预设测试用例）。
  - 第二阶段：通用能力 RL，用 **general reward model + 规则 verifier**，少量 step 即可提升指令遵循/对齐/agent，不损 math/code。
  - 集成 agent 能力（边思考边用工具、按环境反馈调整推理）。
- 具体 RL 算法名/卡时/数据规模：博客未细列（**官方未公开**，仅作为 Qwen RL scaling 首步）。

---

## Qwen2.5-Max — 2025-01（API only，未开权重）

来源：官方博客 https://qwen.ai/blog?id=qwen2.5-max （原 https://qwenlm.github.io/blog/qwen2.5-max/）。本地：`../../../sources/llm/2025/qwen2.5-max-blog.html`
- 架构：大规模 **MoE**（具体专家数/激活/层数 官方未公开）。
- 预训练数据：**>20T token**。
- 后训练：精选 **SFT + RLHF**。
- 对标 DeepSeek-V3 / GPT-4o / Claude-3.5-Sonnet（base 对比 DeepSeek-V3 / Llama-3.1-405B / Qwen2.5-72B）。
- 交付：阿里云 API + Qwen Chat，**未开源权重**。

---

## Qwen3（+ "2507" 更新）— 2025-04/05

来源：Qwen3 Technical Report（arXiv 2505.09388）。本地：`../../../sources/llm/2025/qwen3.pdf`

### 架构（Table 1/2）
**Dense**：Qwen3-0.6B/1.7B（28 层 16Q8KV，tie，32K）、4B（36 层 32Q8KV，tie，128K）、8B（36 层 32Q8KV，128K）、14B（40 层 40Q8KV，128K）、32B（64 层 64Q8KV，128K）。
**MoE**：30B-A3B（48 层 32Q4KV，128 专家/激活8，128K）、235B-A22B（94 层 64Q4KV，128 专家/激活8，128K；总参 235B / 激活 22B）。
- GQA + SwiGLU + RoPE + RMSNorm/Pre-Norm（沿用 Qwen2.5）；**去 QKV-bias，新增 QK-Norm** 保证稳定。
- MoE：fine-grained expert segmentation；**128 总专家激活 8**；**取消共享专家**（与 Qwen2.5-MoE 不同）；采用 **global-batch load balancing loss** 促专家特化。
- Tokenizer：BBPE，vocab **151669**。

### 预训练数据 / pipeline
- 总量 **36T token、119 语言/方言**（Qwen2.5 的 2 倍 token、3 倍语言；29→119 语言）。
- 来源构成：code、STEM、reasoning、books、多语言、合成数据；用 **Qwen2.5-VL OCR** 抽 PDF 文本 + Qwen2.5 精修（数万亿 token）；用 Qwen2.5 / Qwen2.5-Math / Qwen2.5-Coder 合成数万亿 token（教材/QA/指令/代码）。
- 多语言数据标注系统：对 **>30T token** 按 educational value / fields / domains / safety 多维标注；**instance-level 数据 mixture 优化**（小代理模型消融，而非 source/domain 级）。

### 预训练三阶段
1. **General (S1)**：>30T token，seq len 4096，119 语言。
2. **Reasoning (S2)**：提高 STEM/code/reasoning/合成占比，**+~5T 高质 token**，seq 4096，**加速 LR 衰减**。
3. **Long Context**：数千亿 token，seq **32768**；语料 75% 在 16384-32768、25% 在 4096-16384；RoPE base **10000→1000000** (ABF)；推理 **YaRN+DCA** 4 倍扩展。
- scaling law 预测每个 dense/MoE 模型的最优 LR scheduler 与 batch size。
- 算力/卡时/集群/并行策略：报告未给具体 GPU 数字（**官方未公开**）。

### 后训练（四阶段 pipeline + 强到弱蒸馏）
旗舰走完整四阶段：
1. **Long-CoT Cold Start**：math/code/逻辑/STEM，每题配可验证答案/测试用例；两阶段过滤（query filtering 用 Qwen2.5-72B-Instruct 去不可验证/无需 CoT 的题；response 用 **QwQ-32B** 生成 N 候选，按 6 条标准严筛）；少样本少步冷启动。
2. **Reasoning RL**：**仅 3,995 个 query-verifier 对**，**GRPO** 更新；大 batch + 高 rollout + off-policy 提样本效率；控制 entropy 稳步上升。例：Qwen3-235B-A22B 的 AIME'24 从 70.1→85.1（170 步）。
3. **Thinking Mode Fusion**：在 Reasoning RL 模型上继续 SFT 融合「非思考」能力；thinking 数据由 Stage2 模型 rejection sampling 生成，non-thinking 数据多任务精选；chat template 引入 **/think、/no_think** 标志 + thinking budget（达阈值插入停止指令，能力 emergent）。
4. **General RL**：>20 类任务定制评分；三类 reward——**Rule-based**、**Model-based with reference**（Qwen2.5-72B-Instruct 打分）、**Model-based without reference**（训 RM）；覆盖指令/格式遵循、偏好对齐、agent（多轮真实环境反馈）、RAG。
- **Strong-to-Weak Distillation**（轻量模型 0.6/1.7/4/8/14B + 30B-A3B）：① off-policy 蒸馏（teacher /think+/no_think 输出）② **on-policy 蒸馏**（student 采样，对齐 teacher Qwen3-32B / 235B-A22B 的 logits，最小化 KL）。比四阶段省 **~9/10 GPU hours**。
- 采样：thinking 模式 T=0.6/top-p0.95/top-k20；non-thinking T=0.7/top-p0.8/top-k20/presence penalty1.5。

### Qwen3 "2507" 更新（2025-07）
- 放弃 hybrid thinking 单模型，改为**分别发布 Instruct 与 Thinking 模型**（如 Qwen3-235B-A22B-Instruct-2507 / Thinking-2507、Qwen3-30B-A3B-Instruct/Thinking-2507）。
- 原生上下文扩到 **256K**。性能较 4 月版显著提升。（来源：Qwen3-Next/Qwen3-Max 官方博客均引用 2507 系列）

来源 URL：https://arxiv.org/abs/2505.09388 ｜ pdf https://arxiv.org/pdf/2505.09388 ｜ github https://github.com/QwenLM/Qwen3

---

## Qwen3-Coder — 2025-07

来源：官方博客 https://qwen.ai/blog?id=qwen3-coder （原 https://qwenlm.github.io/blog/qwen3-coder/）。本地：`../../../sources/llm/2025/qwen3-coder-blog.html`
- 旗舰 **Qwen3-Coder-480B-A35B-Instruct**：MoE 总参 **480B / 激活 35B**；原生 **256K**，YaRN 扩到 **1M**；对标 Claude Sonnet 4，agentic coding 开源 SOTA。
- 预训练 scaling：
  - **数据扩展**：总计 **7.5T token，代码占 70%**（保通用+数学）。
  - **上下文扩展**：原生 256K（YaRN→1M），为仓库级与动态数据（PR）优化。
  - 用 Qwen2.5-Coder 清洗/重写低质数据（官方博客口径）。
- 后训练 RL：
  - **Scaling Code RL**（"Hard to Solve, Easy to Verify"）：执行驱动的大规模 RL，自动扩展测试样例造大量高质实例。
  - **Scaling Long-Horizon RL（Agent RL）**：真实软件工程任务（SWE-Bench 式多轮交互），借阿里云基础设施**同时运行 20,000 个独立环境**提供可验证 RL 反馈；SWE-bench Verified 开源 SOTA。
- 工具：开源 **Qwen Code** CLI（fork 自 Gemini CLI，定制 prompt 与 function-calling 协议），兼容 Claude Code / Cline。
- 具体 RL 算法名/层数/头数/卡时：博客未列（**官方未公开**）。
- URL：https://qwen.ai/blog?id=qwen3-coder ｜ github https://github.com/QwenLM/Qwen3-Coder

---

## Qwen3-Max — 2025-09（API only，未开权重）

来源：官方博客 https://qwen.ai/blog?id=qwen3-max （2025-09-24）
- **Qwen3-Max-Base**：总参 **>1T**，预训练 **36T token**；沿用 Qwen3 MoE 结构 + **global-batch load balancing loss**。
- 训练稳定性：MoE 结构使预训练 loss 平滑，**全程无 loss 尖刺、无回退、无改数据分布**。
- AI infra：**PAI-FlashMoE** 多级流水并行（MFU 较 Qwen2.5-Max-Base 相对 +30%）；长序列用 **ChunkFlow**（较序列并行吞吐 3×，支持 1M 长上下文训练）；SanityCheck / EasyCheckpoint / 调度优化使大集群硬件故障时间损失降为 Qwen2.5-Max 的 1/5。
- 后训练：Instruct（SWE-Bench Verified 69.6、Tau2-Bench 74.8）；Thinking（Heavy，集成 code interpreter + 并行 test-time compute，AIME25/HMMT 满分）。
- 交付：阿里云 API（模型名 `qwen3-max`）+ Qwen Chat，**未开源权重**。层数/专家数/激活参数 **官方未公开**。

---

## Qwen3-Next（80B-A3B）— 2025-09

来源：官方博客 https://qwen.ai/blog?id=qwen3-next 。本地：`../../../sources/llm/2025/qwen3-next-blog.html`
- 定位：面向 **Context Length Scaling + Total Parameter Scaling** 的全新结构，**Qwen3-Next-80B-A3B-Base** 总参 80B / 激活约 3B，性能≈Qwen3-32B dense 而训练 GPU hours <1/10、32K+ 推理吞吐 10×+。
- 四项核心改进：
  1. **混合注意力**：**Gated DeltaNet（线性注意力）+ Gated Attention**，**3:1**（75% 层 Gated DeltaNet，25% 层标准注意力）。Gated DeltaNet 比 Sliding Window Attention / Mamba2 有更强 in-context learning。标准注意力增强：输出门控（消除 attention sink/极大激活）、头维 128→256、仅前 25% 位置维度加 RoPE 提外推。
  2. **极致稀疏 MoE**：总参 80B 激活~3B（~3.7%）；**512 总专家 + 10 路由专家 + 1 共享专家**（Qwen3 为 128/8 无共享）；global-batch load balance。
  3. **训练稳定性**：**Zero-Centered RMSNorm** + 对 norm weight 加 weight decay；初始化时归一化 MoE router 参数。
  4. **MTP（Multi-Token Prediction）**：原生 MTP，既提主干性能又得高接受率投机解码模块；训练-推理一致多步训练。
- 预训练：Qwen3 的 **36T 语料均匀采样子集，仅 15T token**；GPU hours <Qwen3-30B-A3B 的 80%、为 Qwen3-32B 的 **9.3%**。
- 上下文：原生 **262144 (256K)**，YaRN 验证到 **1M**。
- 推理：prefill 4K 上下文吞吐≈Qwen3-32B 的 7×、32K+ 10×+；decode 类似。
- 后训练：发布 Instruct（≈Qwen3-235B-A22B-Instruct-2507）+ Thinking（>Qwen3-30B-A3B-Thinking-2507/Qwen3-32B-thinking，超 Gemini-2.5-Flash-Thinking）；解决了混合注意力+高稀疏 MoE 在 RL 训练的稳定性/效率难题（具体 RL 算法/卡时未细列）。
- Serving：SGLang / vLLM 支持 MTP 投机解码（NEXTN / qwen3_next_mtp）。
- URL：https://qwen.ai/blog?id=qwen3-next ｜ github https://github.com/QwenLM/Qwen3-Next

---

## 多模态线

### Qwen-VL / Qwen-VL-Chat — 2023（arXiv 2308.12966）
本地：`../../../sources/llm/2023/qwen-vl.pdf`
- 架构：LLM=**Qwen-7B** 初始化；Vision Encoder=**ViT-bigG（OpenCLIP，1.9B）**，patch stride 14；**Position-aware VL Adapter**（单层 cross-attention + 256 个可训练 query，把图像特征压到固定 **256** 长度，2D 绝对位置编码）。总参 **9.6B**（ViT 1.9B + Adapter 0.08B + LLM 7.7B）。
- 输入输出：`<img></img>` 包裹图像特征；bounding box 归一化到 [0,1000) 字符串，`<box></box>`/`<ref></ref>` 标记 → 支持 grounding。
- 三阶段训练：① 低分辨率图文对预训练（原始 50 亿对 → 清洗后 **14 亿**，英 77.3% 中 22.7%）② 多任务高分辨率预训练（解冻全部）③ 高分辨率指令微调（冻 ViT，只调 LLM+Adapter）。
- URL：https://arxiv.org/abs/2308.12966

### Qwen2-VL — 2024（arXiv 2409.12191）
本地：`../../../sources/llm/2024/qwen2-vl.pdf`
- 尺寸：2B / 7B / **72B**；LLM 用 Qwen2；ViT **~675M**（DFN 初始化，绝对位置→RoPE-2D）。
- 创新：**Naive Dynamic Resolution**（任意分辨率→变长视觉 token，ViT 去绝对位置加 **2D-RoPE**，MLP 把相邻 2×2 token 压成 1 个，224×224→66 token）；**M-RoPE**（多模态旋转位置编码，分解为 temporal/height/width）；统一图像+视频（每视频≤16384 token，动态调帧分辨率）。
- 训练：三阶段（① 只训 ViT ② 全解冻 ③ 冻 ViT 只调 LLM 指令微调）；数据 cutoff 2023-06。预训练 token：阶段一 ~**600B**，阶段二 +**800B**，累计 **1.4T**（含图像 token，仅监督文本 token）。ChatML 指令微调。
- URL：https://arxiv.org/abs/2409.12191

### Qwen2.5-VL — 2025（arXiv 2502.13923）
本地：`../../../sources/llm/themes/architecture/qwen2.5-vl.pdf`
- 尺寸：3B / 7B / 72B；ViT 各训练 **4.1T token**，patch 14。
- 创新：重设计 ViT（**window attention**，仅 4 层全注意力，计算随 patch 线性而非二次；窗口 112×112=8×8 patch）；ViT 对齐 LLM 设计用 **RMSNorm + SwiGLU**；ViT **从头训**（CLIP 预训练→VL 对齐→端到端微调）；**Native Dynamic Resolution + 动态 FPS**；**MRoPE 对齐绝对时间**（temporal ID 对齐绝对时间戳，做时序 grounding）；视频两帧合一。
- 数据：从 1.2T 扩到 **~4T token**；三阶段（Visual Pre-Training 1.5T 训 ViT → Multimodal Pre-Training 2T 训 ViT+LLM → Long-Context Pre-Training 0.6T 训 ViT+LLM）。
- 后训练：双阶段对齐（SFT + DPO/RL，报告口径）。
- URL：https://arxiv.org/abs/2502.13923

### Qwen-Audio / Qwen2-Audio — 2023/2024
- Qwen-Audio（arXiv 2311.07919，本地 `/2023/files/qwen-audio.pdf`）：Whisper-large-v2 风格音频编码器 + Qwen-7B LLM；多任务统一框架。Qwen2-Audio 为其升级（语音聊天 + 音频分析），并入 Omni 线作为音频编码器来源。

### Qwen2.5-Omni — 2025（arXiv 2503.20215）
本地：`../../../sources/llm/2025/qwen2.5-omni.pdf`
- 架构：**Thinker-Talker**。Thinker=Transformer decoder（文本生成）+ 音频编码器（来自 Qwen2-Audio，25ms 窗/10ms hop）+ 视觉编码器（来自 Qwen2.5-VL）；Talker=**dual-track 自回归 Transformer**，流式接收 Thinker 高维表示 + 采样文本 token，输出离散语音 token；端到端联合训练。
- **TMRoPE**（Time-aligned Multimodal RoPE）：3D 位置（temporal/height/width）+ 音视频 time-interleaving（按秒交错音频与视频表示）。
- 主力 **7B**；vocab 151643；支持流式语音合成。
- URL：https://arxiv.org/abs/2503.20215

### Qwen3.5-Omni — 2026（arXiv 2604.15804，已落盘）
本地：`../../../sources/llm/2026/qwen3.5-omni.pdf`
- 规模扩到 hundreds of billions 参数、ctx 256K；用 >100M 小时音视频训练。
- 架构：**Thinker 与 Talker 均为 Hybrid Attention MoE**；提出 **ARIA** 动态对齐缓解流式 TTS 不稳定。
- Qwen3.5-Omni-plus 在 215 个音频/音视频子任务 SOTA，关键音频任务超 Gemini-3.1 Pro。
- 注：该 arXiv ID（2604.xxxxx）与日期为本地资料库已记录的 2026 条目，撰写本档时未二次联网核验其权重开放状态，按已有官方落盘资料引用。
- URL：https://arxiv.org/abs/2604.15804

---

## 跨代 AI infra / 训练框架小结（官方口径）

- **训练框架**：早期基于 Megatron-LM 风格 3D 并行（v1-v2.5 报告未公开具体并行配置，标注官方未公开）；FlashAttention 全系使用。
- **长上下文工程**：RoPE ABF（base 1e6/1e7）+ **YaRN + DCA（Dual Chunk Attention）**（Qwen2 起标配），推理 4 倍扩展；v1 用免训练 NTK-aware + LogN + 分层 window attention。
- **Qwen3-Max 公开自研 infra**：**PAI-FlashMoE**（多级流水并行，MFU 相对 +30%）、**ChunkFlow**（长序列吞吐 3×、支持 1M 训练）、SanityCheck / EasyCheckpoint（容错）。
- **Serving / 投机解码**：Qwen3-Next 原生 MTP，SGLang / vLLM 支持（NEXTN / qwen3_next_mtp）。
- **量化 / 精度**：预训练全系 **BF16** 混合精度（v1 明确，后续沿用）；FP8 训练在公开报告中未明确（官方未公开）；推理量化（GPTQ/AWQ/GGUF）由社区+官方 HF 提供。

---

## 官方一手来源清单（URL + 本地落盘）

- Qwen TR：https://arxiv.org/abs/2309.16609 ｜ `2023/files/qwen-technical-report.pdf`
- Qwen-VL：https://arxiv.org/abs/2308.12966 ｜ `2023/files/qwen-vl.pdf`
- Qwen-Audio：https://arxiv.org/abs/2311.07919 ｜ `2023/files/qwen-audio.pdf`
- Qwen1.5 博客：https://qwenlm.github.io/blog/qwen1.5/ ｜ MoE https://qwenlm.github.io/blog/qwen-moe/ （本地无）
- Qwen2 TR：https://arxiv.org/abs/2407.10671 ｜ `2024/files/qwen2.pdf`
- Qwen2-VL：https://arxiv.org/abs/2409.12191 ｜ `2024/files/qwen2-vl.pdf`
- Qwen2.5 TR：https://arxiv.org/abs/2412.15115 ｜ `2024/files/qwen2.5.pdf`
- Qwen2.5-Coder：https://arxiv.org/abs/2409.12186 ｜ `2024/files/qwen2.5-coder.pdf`
- Qwen2.5-Math：https://arxiv.org/abs/2409.12122 ｜ `2024/files/qwen2.5-math.pdf`
- QwQ-32B 博客：https://qwen.ai/blog?id=qwq-32b （原 qwenlm.github.io/blog/qwq-32b/）
- Qwen2.5-Max 博客：https://qwen.ai/blog?id=qwen2.5-max ｜ `2025/files/qwen2.5-max-blog.html`
- Qwen2.5-VL：https://arxiv.org/abs/2502.13923 ｜ `themes/architecture/files/qwen2.5-vl.pdf`
- Qwen2.5-Omni：https://arxiv.org/abs/2503.20215 ｜ `2025/files/qwen2.5-omni.pdf`
- Qwen3 TR：https://arxiv.org/abs/2505.09388 ｜ `2025/files/qwen3.pdf`
- Qwen3-Coder 博客：https://qwen.ai/blog?id=qwen3-coder ｜ `2025/files/qwen3-coder-blog.html`
- Qwen3-Max 博客：https://qwen.ai/blog?id=qwen3-max
- Qwen3-Next 博客：https://qwen.ai/blog?id=qwen3-next ｜ `2025/files/qwen3-next-blog.html`
- Qwen3.5-Omni：https://arxiv.org/abs/2604.15804 ｜ `2026/files/qwen3.5-omni.pdf`
- 官方 GitHub 组织：https://github.com/QwenLM ｜ HF：https://huggingface.co/Qwen

## 增量补录（2026-06+，初版调研后）
- **Qwen-AgentWorld-35B-A3B** — **首个语言世界模型(LWM)**，覆盖 7 个 agent 交互域；CPT→SFT→RL 三阶段、环境建模即训练目标；单轮非 agentic RL warm-up 可迁移到多轮 tool-calling；35B/3B 激活，`qwen3_5_moe` 混合线性注意力，256 专家/8。arXiv 2606.24597。详见 [2026/qwen-agentworld.md](llm/2026/qwen-agentworld.md)。
