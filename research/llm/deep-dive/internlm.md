# InternLM 书生（上海 AI Lab）训练配方深挖

> 家族：InternLM / 书生·浦语（Shanghai AI Laboratory + SenseTime + 港中文/复旦/上交/清华/南大）
> 范围：InternLM(v1) → InternLM2 → InternLM2.5 → InternLM3；多模态 InternVL 1.5 → 2.5 → 3；科学多模态 Intern-S1。
> 原则：仅一手官方来源（arXiv 技术报告原文 PDF、HF 官方组织 model card、官方 GitHub README、官方 config.json）。所有数字均抠自原文/配置文件；查不到的明确标注"官方未公开"。
> 最近核对：2026-06-18（联网核对 InternLM3 / InternLM2.5 / Intern-S1 官方页面与配置）。

---

## 家族演进脉络

- **InternLM v1（2023-06，技术报告）**：104B 稠密、1.6T token、2K 上下文、自研 Uniscale-LLM 训练系统、多阶段渐进式预训练 + InstructGPT 式 SFT→RM→PPO。奠基之作（开源版另发布过 7B/20B）。
- **InternLM2（2024-01 模型 / 2024-03 技术报告 arXiv 2403.17297）**：1.8B/7B/20B 稠密，全系 GQA，对齐 LLaMA 架构（RMSNorm+SwiGLU），GPT-4(cl100k) 改造词表(≈100k)，4k→32k 两段预训练 + RoPE base 50k→1M 外推到 200K，自研 InternEvo 框架，提出 **COOL RLHF**（条件奖励模型 + 多轮在线 PPO）。这是该家族**最透明的一手训练文档**。
- **InternLM2.5（2024-07/08）**：1.8B/7B/20B，沿用 InternLM2 架构（`model_type=internlm2`），强化数学推理、**1M 上下文**、强工具使用（MindSearch / Lagent）。无独立 arXiv 论文，复用 2403.17297。
- **InternLM3（2025-01-15）**：仅开源 8B-Instruct，新架构（`model_type=internlm3`，GQA KV=2、FFN=10240、vocab=128512、RoPE θ=5e7），**仅 4T 高质量 token**（号称省 75% 训练成本），首次内置**深度思考(long-CoT)+常规**双模式。无独立 arXiv 论文，仍引用 2403.17297。
- **InternVL 1.5（2024-04，arXiv 2404.16821）**：多模态，InternViT-6B(45 层,5.5B) + **InternLM2-20B** 经 MLP，动态高分辨率(1–40 tile,448²)，4K 输入。
- **InternVL 2.5（2024-12，arXiv 2412.05271）**：1B–78B，ViT-MLP-LLM，LLM 后端含 **InternLM2.5** 与 Qwen2.5；三段式训练(MLP warmup→ViT 增量→全模型 SFT)，渐进式扩展，随机 JPEG 增强、数据打包、square averaging。
- **InternVL3（2025-04，arXiv 2504.10479）**：1B–78B，**原生多模态预训练**（文本+多模态单阶段联合），**V2PE** 可变视觉位置编码，后训练 SFT+**MPO**，LLM 后端含 **InternLM3-8B** 与 Qwen2.5；约 200B 预训练 token（50B 文本+150B 多模态，1:3 比例）。
- **Intern-S1（2025-08，arXiv 2508.15763）**：科学多模态 MoE，**Qwen3-235B-A22B(241B 总/28B 激活) + InternViT-6B + 动态分子/蛋白 tokenizer + 时序编码器**，继续预训练 **5T token（≥2.5T 科学）**，后训练离线 RL(BoN-SFT)→在线 RL，提出 **Mixture-of-Rewards(MoR)** + **OREAL+KL-Cov** 在 InternBootCamp 1000+ 任务上 RLVR。Intern-S1-mini 用 Qwen3-8B + InternViT-300M。

> 注：知识库 2026 目录另有 `intern-s1-pro`（arXiv 2603.25040，万亿级科学多模态旗舰）与 `internvl-u`（arXiv 2603.09877，统一理解/推理/生成/编辑）两条 2026-H1 条目；本档已下载/精读的是 2025-08 的 Intern-S1。Pro/U 两篇本地 PDF 已落盘但属 2026 预印本，超出本次"InternLM/InternLM2/2.5/3 + InternVL"核心范围，未逐数字展开，见结尾"未覆盖/gaps"。

### 各代关键参数对比（纯语言主线，数字来自原文/config.json）

| 型号 | 参数 | 层数 | 隐藏维 | FFN维 | 头(Q) | KV头 | 注意力 | vocab | 上下文 | RoPE θ | 训练token | 架构基调 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| InternLM v1 | 104B 稠密 | 82 | 10240 | 官方未公开(SwiGLU) | 80 | 80(MHA) | MHA | 65.5K (BPE) | 2K | 官方未公开 | 1.6T | GPT 式 decoder |
| InternLM2-1.8B | 1.8B | 24 | 2048 | 官方未列(SwiGLU) | 16(=8×2) | 8 | GQA | 92544 | 4k→32k(→200K) | 50k→1M | 2.0–2.6T | LLaMA 式 |
| InternLM2-7B | 7B | 32 | 4096 | 14336 | 32(=8×4) | 8 | GQA | 92544 | 4k→32k(→200K) | 50k→1M | 2.0–2.6T | LLaMA 式 |
| InternLM2-20B | 20B | 48 | 6144 | 官方未列(SwiGLU) | 48(=8×6) | 8 | GQA | 92544 | 4k→32k(→200K) | 50k→1M | 2.0–2.6T | LLaMA 式 |
| InternLM2.5-7B | 7B | 32 | 4096 | 14336 | 32 | 8 | GQA | 92544 | 32K(→**1M**) | 1e6 | 官方未公开(总量) | 同 InternLM2 |
| InternLM3-8B | 8B | 48 | 4096 | 10240 | 32 | **2** | GQA | 128512 | 32K | **5e7** | **4T** | 新 `internlm3` |
| Intern-S1 (S1) | 241B 总/**28B 激活** MoE | 94 | 4096 | moe 1536×(128专家,8激活) | 64 | 4 | GQA+MoE | 153216 | 65536 | 1e6 | **5T**(继续预训练) | Qwen3-235B 改造 |

> 说明：InternLM2 头数 = `nq_per_head × nkv_heads`（论文 Table 3：1.8B=2×8,7B=4×8,20B=6×8；KV 头一律 8）。FFN 维仅 7B 有公开 config（14336），1.8B/20B 论文未单列。InternLM2.5 复用 InternLM2 架构与词表；InternLM3 是全新 `internlm3` 实现。Intern-S1 词表 153216 是动态 tokenizer 在 Qwen3 词表基础上为科学模态扩展所致。

---

## InternLM v1（书生·浦语 第一代，2023-06）

来源：InternLM 技术报告（GitHub `InternLM/InternLM-techreport`，PDF 已落盘）。

### 架构细节
- 104B 稠密 decoder-only（GPT 式）；选 104B 是为在合理时间内吃完 1.6T token（引 Chinchilla 计算最优）。
- 层数 nlayers=82；每层 nheads=80，head_dim=128 ⇒ dmodel=10240。
- Tokenizer：基于多语言语料用 **BPE** 训出 **65.5K** 词表，全程统一。
- 上下文长度：**2K**（报告坦承相对 GPT-4 的 32K 在长文档/复杂推理上落后）。
- 激活/norm：报告未单列；属 GPT 系 decoder（注：v1 早于全面对齐 LLaMA 架构，未明确写 RMSNorm/SwiGLU）。官方未公开 FFN 维。

### 预训练数据（总 1.6T，论文 Table 1）
| 子集 | token(B) | 占比 |
|---|---|---|
| Massive web text 网页 | 1205.3 | 75.1% |
| Encyclopedia 百科 | 78.2 | 4.9% |
| Books 书籍 | 72.7 | 4.5% |
| Academic papers 论文 | 52.7 | 3.3% |
| Code 代码 | 122.2 | 7.6% |
| Others 其它 | 73.8 | 4.6% |
| 合计 | 1604.9 | — |
- 多语言（重英/中），含其它语种提升多语能力。

### 数据处理 pipeline（4 步）
1. 语言分类（英/中/其它）以便语言感知处理；
2. 规则启发式过滤去低质；
3. **模型打分过滤**：用在 gold 语料上训的小语言模型挑高质文档；
4. 去重：去近重文档与精确重复段落（明确称重复会损性能）。

### 数据配比 / 训练策略
- **多阶段渐进式预训练（Multi-phase Progressive Pretraining）**：整体切多阶段，每阶段以某能力为目标、控制各类数据比例；阶段不达预期可从该阶段末断点续训；调比例时保证同数据不被重采样；变长句打包成定长序列（特殊符分隔）。

### 训练细节
- **优化器**：AdamW，β1=0.9、β2=0.95，weight decay 在 **0.01–0.1** 浮动。
- **LR**：cosine，峰值 LR 在 **2e-4 ~ 4e-5** 之间（按阶段），每阶段末衰减到峰值 10%。
- **warmup ratio=0.025**、**grad clip=1.0**，全阶段恒定。
- **算力/系统**：自研 **Uniscale-LLM**，集成 DP+TP+PP+ZeRO、异步 checkpoint（每 1 小时或数小时）、故障/loss spike 恢复；压力测试可在 **2048 GPU** 稳定训 >200B 参数；训 InternLM 时 **1024 GPU 稳定 203.6 tokens/gpu/sec**，可近线性扩到 2048 GPU。（GPU 型号/卡时/FLOPs 官方未公开。）

### SFT / RL 对齐（InstructGPT 三步）
- **SFT**：约 **5M** 条 prompt+response（含单轮 QA 与多轮对话），用 self-instruct 扩多样性。
- **RM**：以 3H（helpful/harmless/honest）打分；线上对话采 prompt + 自建毒性 prompt，人/模型生成多响应并标注偏好；RM 从 SFT 模型初始化、替换最后投影层为新 FC。
- **RLHF**：基于 RM 用 **PPO** 微调 SFT 模型；经验证 RLHF 可降毒。

---

## InternLM2（1.8B/7B/20B，2024-01 模型 / 2024-03 报告 arXiv 2403.17297）

来源：InternLM2 Technical Report（arXiv 2403.17297，PDF 已落盘）。该家族训练配方最详尽的一手文档。

### 架构细节（论文 §2.2 + Table 3）
- 规模 1.8B / 7B / 20B，全系采用 **GQA**（为长序列低显存推理）。
- 对齐 **LLaMA 架构**：**RMSNorm + SwiGLU**。
- 头/KV：KV 头一律 8；每 KV 头对应的 Q 头数 1.8B=2 / 7B=4 / 20B=6（即总 Q 头 16/32/48）。
- 层数/隐藏维：1.8B(24,2048) / 7B(32,4096) / 20B(48,6144)。7B config FFN=14336。
- 工程结构创新：**合并 Wq/Wk/Wv**（预训练加速 >5%）；并把 WQKV 改成**按 head 交错**布局，使切/拼最后一维即可改 TP size（提升张量并行灵活性）。
- **Tokenizer**：采用 **GPT-4 的 cl100k** 思路——从 cl100k 选 top 60004 token + 加 32397 中文 token + 147 备用 = **92544**（256 的整数倍，便于训练）。
- **上下文/RoPE**：预训练先 4k 后转 32k；长上下文阶段把 **RoPE base 从 50,000 调到 1,000,000**；再靠位置编码外推在 **200K "大海捞针"** 近满分。

### 预训练数据（文本，论文 Table 1，按字节）
| 来源 | 文档(M) | 字节(GB) | 字节占比 |
|---|---|---|---|
| en-webpages | 3614.07 | 9129.39 | 67.51% |
| zh-webpages | 928.94 | 2562.86 | 18.95% |
| zh-techlit | 89.59 | 668.19 | 4.94% |
| en-techlit | 59.27 | 576.48 | 4.27% |
| zh-books | 0.71 | 366.82 | 2.71% |
| en-books | 0.50 | 220.14 | 1.63% |
- 中英网页合占 **86.46%**（主力）；书籍/技术文献量小但文档长、质量高。
- 代码：来自 GitHub 直爬 + 公开数据集 + Q&A/教程/API 文档；按打分模型分 High/Moderate/Low —— 高质量(105.6GB,16.8%)多次训练、中质量(440.1GB,69.9%)训一次、低质量(83.85GB,13.3%)丢弃。

### 数据处理 pipeline（论文 §3.1，Figure 3）
标准化(Format)→规则启发式过滤(Clean)→**LSH 去重(Dedup)**→安全过滤(Safe)→质量过滤(High-quality)。
- **格式化**：网页主来自 Common Crawl，解压 WARC → **Trafilatura** 抽正文 → **pycld2** 语言识别 → jsonl。
- **规则过滤**：仿 Gopher/C4/RefinedWeb，针对分隔/换行异常、异常字符频率、标点分布。
- **去重**：**MinHash**（LSH），128 个哈希函数、文档 5-gram 签名、阈值 **0.7**；保留更新数据（优先大 CC dump 号）。
- **安全过滤**：~**13M 不安全域名**黑名单 + **36,289** 不安全词黑名单；BERT 微调出**毒性分类器**（Kaggle Toxic Comment 数据）+ **色情分类器**（用 Perspective API 标注 Dedup 子集训练），二次过滤低于阈值的数据。
- **质量过滤**：人工标注后 BERT 微调出**广告分类器** + **流畅度分类器**（一致性/噪声/信息量/语法 4 维），低于阈值剔除。
- **代码**：统一转 markdown；**文件级**去重（强调好 tokenizer 是通用去重前提）；规则+模型混合多级打分（约 **5 万**标注样本训打分器，3 轮迭代标注；仅对人模一致的语言用模型打分）；按 import 关系**拓扑排序拼接整仓**为一个长 markdown。
- **长上下文数据**：选 >32K 字节样本 → 统计过滤（连接词/语篇结构词等）→ **困惑度差(PPL diff)** 过滤（用 P(S2|S1) 与 P(S2) 之差判段间连贯，仅用差不用绝对 PPL 以抵消估计器偏差）；阈值**按域/语言分别设定**；长上下文数据是标准语料子集，至少被学两次。

### 数据配比 / 阶段划分（论文 §3.3）
- 总训练 token **2.0T–2.6T**（按规模），三阶段，每阶段混英/中/代码：
  1. **4k 上下文阶段**：约 **90% 步数**，数据长度 ≤4096（超长截断后余部也用）。
  2. **长上下文阶段**：约 **9% 步数**，转 32k 语料（仍保留 50% <4096 数据）；RoPE base 50k→1M；4K→32K 训练速度只降 ~40%。
  3. **能力定向增强(Capability Specific Enhancement)**：精选高质量检索数据 + HF 开源数据共 **24.4B token**（检索 STEM 15.97B/65%、检索特定域 2.17B/8%、精选高质 6.26B/26%），用更小 LR 与 batch；做污染检测、剔测试集相关；发布增强前(Base)/后()两版 checkpoint。

### 训练细节（论文 §3.2 + Figure 1）
- 超参（Table 3）：LR 1.8B/7B=3e-4、20B=3e-4；batch 1.8B/7B=4M token、20B=5M token；**AdamW** β1=0.9,β2=0.95,ε=1e-8,wd=0.1；**cosine** 衰减到峰值 10%。
- **精度**：BF16 混合精度 + FlashAttention。
- **infra（InternEvo）**：DP+TP(Megatron)+SP+PP + ZeRO 分片；自适应分片（Full-Replica/Full-Sharding/Partial-Sharding，参数/梯度/优化器状态各自独立选分片与设备网格）+ 执行模拟器自动搜最优并行；通信-计算重叠（AllGather 预取下层参数同时算当前层，梯度 ReduceScatter+AllReduce）。
- **效率**：InternLM-7B 8 卡 4M batch **64% MFU**；1024 卡同 batch 仍 **53% MFU**（同条件 DeepSpeed-ZeRO1+MiCS 约 36%）；支持 **256,000** 序列长训练，7B@256k 近 **88% MFU**（DeepSpeed-Ulysses/Megatron 约 65%）；最长可训 **百万 token** 上下文。
- **稳定性/容错**：内存池 + 主动碎片整理防 OOM；六个月数据中心 trace 研究后做 LLM 参与的故障诊断+自动恢复 + 评测解耦调度；异步保存（本地→远端分布式存储，热存→冷存）；支持改并行配置后无缝续训。（GPU 型号/总卡数/卡时/FLOPs 官方未公开。）

### SFT 细节（论文 §4.1）
- **10M（1000 万）** 条指令样本，经 helpful/harmless 筛选；覆盖通用对话/NLP 任务/数学/代码生成/函数调用等；转 **ChatML** 格式；7B 与 20B 各训 **1 epoch**，AdamW，初始 LR **4e-5**。

### RL / 对齐（COOL RLHF，论文 §4.2）
- **条件奖励模型(Conditional Reward Model)**：单个 RM 用不同 system prompt 条件化（helpful/harmless/code/math 各一条），在一个模型里调和冲突偏好；从 SFT 模型初始化、输出层换 1 维线性；**焦点排序损失**（加难度衰减系数 γ=2）+ 对数障碍惩罚（把分数限在 -5~5，λ=0.02）；训练数据达 **240 万(2.4M)** 二元偏好对；batch 固定总长 16384 token、最大上下文 8192；cosine LR 1e-5→5e-6，wd 0.01，1 epoch。
- **在线 RLHF（多轮 PPO）**：Fast Path（每轮后比对早/晚期 PPO 模型构造 20–100 偏好对快速修补 reward hacking）+ Slow Path（SFT/早/晚 PPO 多模型响应人工标偏好提升 RM 上界）；共 **3 轮**精炼。
- **PPO 细节**：4 模型（actor/critic/reference/reward，等大），仅训 actor+critic；遍历约 **20 万 query / ~400 迭代**；critic 从 RM 初始化并先 50 迭代预训练（冻 actor）；加 **pre-train loss**（系数 0.5、数据量约为 PPO 的 50%）防遗忘；**KL 系数 0.01**；actor LR 1e-6 / critic 5e-6；PPO λ=0.99、top_p=0.9；不做 value clipping / advantage normalization。
- **长上下文微调**：SFT/RLHF 阶段也用长上下文数据（书籍 + DS-1000 核心仓相关的 GitHub >10k star 仓库，按 DFS+依赖拼到 32k）。
- **工具/agent**：改 ChatML 加 `environment` 角色 + `<|interpreter|>`/`<|plugin|>` 关键字；用 **Agent-FLAN** 对齐 agent 语料、按能力解耦细粒度训练；数学走 **RICO**（推理与编码交织）+ 迭代难例挖掘（InternLM-Math）。
- 发布 SFT 版（InternLM2-Chat-{size}-SFT）与 RLHF 版（InternLM2-Chat-{size}）便于社区对比。

### AI infra
- 训练框架 **InternEvo**（已开源）；RLHF 阶段基于 InternEvo+**Ray** 自研可扩展 RLHF 框架（4 模型各自最优配置、可接多种执行引擎）。

---

## InternLM2.5（1.8B/7B/20B，2024-07/08）

来源：HF 官方 model card `internlm/internlm2_5-7b-chat`、`internlm2_5-7b` config.json、官方 GitHub README（无独立 arXiv，仍引 2403.17297）。

### 架构细节（config.json）
- 沿用 **InternLM2 架构**（`model_type=internlm2`）：7B = 32 层、hidden 4096、FFN 14336、32 头、**8 KV 头(GQA)**、SiLU(SwiGLU)、RMSNorm(eps 1e-5)、vocab **92544**、`max_position_embeddings=32768`、**RoPE θ=1e6**、`rope_scaling type=dynamic factor=2.0`、bf16、不绑定词嵌入。
- 规模档：1.8B / 7B / 20B（含 -Chat、以及 **7B-Chat-1M** 长上下文版）。
- 上下文：32K 原生，长版**外推到 1M**（"百万大海捞针"近满分，配 LMDeploy 推理）。

### 训练 / 后训练（官方 model card 公开点）
- 三大特性：**强数学推理**（超 Llama3、Gemma2-9B）、**1M 上下文**、**强工具使用**（支持从 >100 网页聚合信息，对应实现见 **MindSearch**；工具选择/反思能力强，配 **Lagent**）。
- 具体预训练总 token 数、数据配比%、SFT/RL 配方：官方未发独立技术报告，**官方未公开**（沿用 InternLM2 体系方法）。

---

## InternLM3-8B-Instruct（2025-01-15）

来源：HF 官方 model card `internlm/internlm3-8b-instruct` + config.json + 官方 GitHub README（无独立 arXiv，引 2403.17297）。

### 架构细节（config.json）
- 新实现 `model_type=internlm3`（`InternLM3ForCausalLM`）。
- **48 层**、hidden **4096**、FFN(intermediate) **10240**、**32 头**、**num_key_value_heads=2**（深度 GQA）、head_dim **128**、SiLU(SwiGLU)、RMSNorm(eps 1e-5)、bias=false/qkv_bias=false。
- **vocab 128512**（较 InternLM2 的 92544 显著扩大）。
- 上下文 `max_position_embeddings=32768`；**RoPE θ=50,000,000**（5e7，远高于 InternLM2 的 1e6）；`rope_scaling type=dynamic factor=6.0`。bf16，不绑定词嵌入。

### 预训练数据 / 训练
- **仅 4 万亿(4T) 高质量 token** 训练，官方称**省 >75% 训练成本**（vs 同量级 LLM），主打"高质量数据 + 低成本 SOTA"。
- 总数据配比%、清洗 pipeline 细节、并行/精度/GPU/卡时：**官方未公开**（无独立技术报告）。

### 后训练 / 能力
- **双模式**：深度思考(deep thinking / long chain-of-thought) 用于复杂推理 + 常规响应模式用于流畅对话（model card 提供 thinking-mode system prompt 与少样本示例切换）。
- License：Apache-2.0；推理栈支持 transformers≥4.48 / LMDeploy / vLLM / SGLang / Ollama。
- SFT 数据规模/来源、是否合成、RL 算法(PPO/DPO/RLVR)等具体配方：**官方未公开**。

---

## InternVL 1.5（2024-04，arXiv 2404.16821 "How Far Are We to GPT-4V?"）

来源：arXiv 2404.16821 PDF（已落盘 `2024/files/internvl-1-5.pdf`）。

### 架构细节
- **ViT-MLP-LLM**：**InternViT-6B-448px-V1.5** + MLP projector + **InternLM2-20B**（语言后端，故其 LLM 训练配方见上 InternLM2 节）。
- **InternViT-6B-448px-V1.5**：在 V1.2 基础上继续预训练；V1.2 时把 InternViT-6B 从 48 层裁到 **45 层**、分辨率 224→448、并曾接 Nous-Hermes-2-Yi-34B 训练；隐藏 3200、25 头、RMSNorm、NTP loss、约 **5.5B 参数**。
- **动态高分辨率**：按长宽比把图切成 1–40 个 **448×448** tile（最高 4K 输入）+ 额外缩略图全局视图；**pixel shuffle** 把每 tile 的 1024 视觉 token 压到 **256**。
- 整模型 **25.5B** 参数。

### 数据 / 训练
- 三大改进：①InternViT-6B 持续学习强视觉表征；②动态高分辨率；③高质量**双语**数据集（覆盖场景/文档/图表，中英 QA 标注）+ 自研开源-LLM 数据翻译 pipeline。
- 具体训练阶段/超参/token 数：报告以三改进为主，**细粒度 stage 超参在 2.5 报告中才系统化公开**（见下）。

---

## InternVL 2.5（1B–78B，2024-12，arXiv 2412.05271）

来源：arXiv 2412.05271 PDF（已落盘 `2024/files/internvl-2-5.pdf`）。

### 架构 / 后端（论文 Table 1/2）
- **ViT-MLP-LLM**，pixel unshuffle 把 1024 视觉 token/tile 压到 256（448² tile=256 token）。
- 视觉后端 **InternViT-300M-448px-V2.5**（0.3B,24 层,hidden 1024,16 头,LayerNorm）或 **InternViT-6B-448px-V2.5**（5.5B,45 层,hidden 3200,25 头,RMSNorm）；均 NTP 增量预训练。
- LLM 后端含 **InternLM2.5**（internlm2_5-1_8b/7b/20b-chat）与 Qwen2.5；MLP 为随机初始化 2 层。
- 各档构成例：2.5-8B=InternViT-300M-V2.5 + internlm2_5-7b-chat；2.5-26B=InternViT-6B-V2.5 + internlm2_5-20b-chat；2.5-78B=InternViT-6B-V2.5 + Qwen2.5-72B-Instruct。

### 训练策略（论文 §3，Table 3，**全档超参公开**）
- **三段式**：Stage 1 MLP warmup（冻 ViT+LLM，只训 MLP，LR 2e-4）→ Stage 1.5 ViT 增量学习（可选，训 ViT+MLP，LR 1e-5）→ Stage 2 全模型指令微调（LR 2e-5~4e-5）。
- 全程动态高分辨率、Packed Batch Size **512**（Stage1.5 用 1024）、Context Length **16384**、Image Tile Threshold 48、weight decay 0.01→0.05。
- **训练 token（极省）**：78B 全程仅约 **120B token**（明确对比 Qwen2-VL 累计 1.4T，不到其 1/10）；各档 Table 3 列出每 stage token，如 8B 约 22B(S1)+76B(S1.5)+44B(S2)。
- **渐进式扩展**：ViT 先随小 LLM(如 20B)训好，再共享权重接大 LLM(如 72B)免重训，大模型可跳过 Stage1.5。

### 训练增强 / 数据组织（论文 §3.4–4）
- **随机 JPEG 压缩**（质量 75–100）做增强（仅图像，视频/文本关）。
- **Loss reweighting / square averaging**：wi=1/x^0.5，平衡长短响应（缓解 token/sample averaging 的长短偏置）。
- **数据组织三参数**：data augmentation 开关、最大 tile 数 nmax（多图/文档 24~36、普通图 6~12、视频 1）、repeat factor r∈(0,4]（上/下采样调各数据集 epoch）。
- **多模态数据打包(packing)**：select→search→pack→maintain，按 LLM 序列长 + ViT tile 双约束拼包，包内样本不互相 attend、位置索引独立维护，提升 GPU 利用率。
- **数据过滤**：发现 LLM 比 ViT 对噪声敏感得多，Stage2 全参可训时仅几千条**重复模式**样本就会致模型推理循环/异常；专门设计过滤 pipeline 去重复生成等低质样本（对 test-time scaling 尤其关键）。数据集从 2.0 到 2.5 规模翻倍但严格过滤提质。
- Stage 3（偏好优化等后训练）2.5 报告留待未来——在 InternVL3 落地为 MPO。

### infra
- 基于 **InternEVO**（扩展自 InternLM 的 ZeRO 框架）；DP/TP/SP/PP 任意组合。

---

## InternVL3（1B–78B，2025-04，arXiv 2504.10479）

来源：arXiv 2504.10479 PDF（已落盘 `2025/files/internvl3.pdf`）。

### 架构细节（论文 Table 1）
- **ViT-MLP-LLM**，沿用 pixel unshuffle（448² tile=256 token）。LLM 与 ViT 均从**基座（非 instruct）**初始化，MLP 随机初始化 2 层。
- 视觉后端 InternViT-300M-V2.5 或 InternViT-6B-V2.5；LLM 后端含 **InternLM3-8B**（→ InternVL3-9B）与 Qwen2.5-0.5B~72B。
- **V2PE（Variable Visual Position Encoding）**：视觉 token 用更小位置增量 δ（文本 token 仍 +1，视觉 token +δ，δ<1，训练时从 {1,1/2,1/4,…,1/256} 随机取、单图内 δ 恒定，推理按序列长选 δ）——支持更长多模态上下文。

### 原生多模态预训练（论文 §2.2，核心创新）
- **单阶段联合**：文本-only 语料 + 多模态语料(图文/视频文/交织)交织，**全参数联合优化**（不冻任何层），免去"先训文本 LLM 再多模态改造"的对齐难题。
- 损失只在**文本 token** 上算（视觉 token 仅作条件上下文）；token 权重用 **square averaging**(wi=1/l^0.5)。
- **数据**：多模态部分沿用 InternVL2.5 预训练语料(图说/QA/数学/图表/OCR/知识/文档/多轮/医疗)+ 新增 GUI/工具/3D/视频；纯文本主要来自 **InternLM2.5** 预训练数据 + 开源文本集。
- **配比**：两阶段定比例——先各自单模态训小模型定模态内最优，再固定总预算定模态间比例；实验得**语言:多模态 = 1:3** 最佳；**总约 200B token**（语言 ~50B + 多模态 ~150B）。

### 后训练（论文 §2.3）
- 两阶段：**SFT → MPO**。
- **SFT**：沿用 InternVL2.5 的随机 JPEG、square loss、数据打包；扩工具/3D/GUI/长上下文/视频/科学图/创意写作/多模态推理样本；样本量从 2.5 的 **16.3M 增至 21.7M**。
- **MPO（Mixed Preference Optimization）**：L=wp·Lp+wq·Lq+wg·Lg —— 偏好损失用 **DPO**(KL 系数 β)、质量损失用 **BCO**(含 reward shift δ=历史奖励滑动均值)、生成损失=LM loss；用 InternVL3-8B/38B/78B 的 SFT 版生成 rollout 造偏好对，数据基于 **MMPR v1.2**，MPO 阶段约 **300K** 样本，全档同一数据集。

### Test-Time Scaling（论文 §2.4）
- **Best-of-N**，用 **VisualPRM-8B**（视觉过程奖励模型，逐步打分取均值，多轮 chat 形式）选最优响应；VisualPRM 用 **VisualPRM400K**（基于 MMPR v1.2）训练，并用 InternVL3-8B/38B rollout 扩充。

### AI infra（论文 §2.5）
- 扩展 **InternEVO**（原为 LLM ZeRO 优化）支持 MLLM：ViT/MLP/LLM 解耦灵活分片、通信计算重叠；支持 DP/TP/SP/PP 任意组合；为 32K 序列用 head-parallel + sequence-parallel；动态平衡视觉/文本 token 计算负载；相比训 2.5 同规模**提速 50%–200%**。

---

## Intern-S1（科学多模态 MoE，2025-08，arXiv 2508.15763）

来源：arXiv 2508.15763 技术报告 PDF（已下载 `deep-dive/files/intern-s1.pdf`）+ HF `internlm/Intern-S1` model card + config.json。

### 架构细节（论文 §2 + config.json）
- **多模态 MoE**：LLM 后端 **Qwen3-235B-A22B MoE**（Intern-S1）/ Qwen3-8B（Intern-S1-mini）。config 显示总体 `interns1`：**94 层、hidden 4096、64 头、4 KV 头(GQA)、128 专家 / 每 token 激活 8 专家、moe FFN 1536、vocab 153216、max_position_embeddings 65536、RoPE θ=1e6、head_dim 128**。
- 论文口径：**241B 总参 / 28B 激活参**（model card 简写为"235B MoE(Qwen3)"，差异源于附加视觉/科学模块与扩展词表）。
- **视觉编码器**：**InternViT-6B**（mini 用 InternViT-300M）；448² 固定或动态分辨率；pixel unshuffle 把 448² 图压到 256 视觉 token；MLP projector 对齐；图文阶段 ViT 联合训练。
- **动态 tokenizer（创新）**：对科学串（SMILES/FASTA 等）用规则检测/特殊标签(`<SMILES>`,`<FASTA>`)切换切分策略，且**各模态 embedding 空间正交**；SMILES 压缩比 2.64 vs Qwen3/GPT-OSS/DeepSeek-R1 的 ~1.44–1.51（提升 >70%）。
- **时序编码器（创新）**：处理地震波/引力波/光变曲线/EEG 等连续数值信号；自适应下采样 + transformer 块。
- 支持 4 类模态：文本/图像/分子蛋白(离散科学串)/时序。

### 继续预训练数据（论文 §4.1，Figure 6）
- **继续预训练 5T 高质量文本 token，其中科学数据 ≥2.5T**（图示 2.3T 通用 + 0.7T + 2.5T 科学的拆分）；六大重点科学域：数学/物理/化学/生命科学/地球科学/材料科学（按自然分布差异，对生命科学严过滤、对材料科学松过滤）。
- 图文 CPT 阶段约 **250B token**（语言 70B + 交织图文 180B，其中科学 30B）。

### 数据处理 pipeline（论文 §4.1）
- **页级 PDF 解析**：低成本解析器(MinerU) 先解析每页 → 公式/符号检测器判断难页 → 难页喂高成本 VLM(InternVL/Qwen-VL，慢 20×) → 规则/小 LLM 清洗合并；页级图去重去版权页；archived 库去掉约 20% token(乱码+去重)，web PDF 用 edu 打分器保留 ~50%；archived 5% / web 3% 页走高成本解析。
- **域中心 web 解析**：按 URL 域聚合，采样数百页喂 LLM-agent，按标注**整域 discard/rewrite/retain** + 常规规则/去重/质量/格式分类。
- **科学数据召回过滤**：三级 taxonomy 树，每域用强 LLM 标 silver set 训轻量分类器(fastText + 1.5B LLM) + 用 in-domain/OOD 验证集自动优化 prompt；把目标域数据纯度 **从 ~2% 提到 ~50%**（人工评）。
- 多模态科学数据：保留图/公式/符号/表/图表结构，页/图/片段级图文对齐；exam-style 结构完整性过滤(题干/选项/答案/解析)，公式渲染校验，规则去坏例。

### 训练细节（论文 §3 + §4.2）
- **四阶段**：Text CPT(单模态) → Image-text CPT → Image-text SFT → Image-text RL（仅第一阶段单模态，其余多模态联合）。
- **infra**：自研 **XTuner**；预训练/SFT 用 **FSDP**；**FP8** GEMM(per-tile 1×128 动态缩放，ViT 保 BF16)；TMA-Adaptive FP8 Grouped GEMM(MoE)、Liger fused CE kernel、FlashAttention-3 变长；**VLBS 变长均衡策略**(分桶+滑窗+桶内按长排序)平均提速 2×。
- **batch warmup**：前期小 batch 学得好、后期大 batch 效率高；按 critical batch size 与 WSD 关系，处理 **400B token 后把 batch 从 66M 切到 132M**(论文另处也写 4M→10M 的小模型验证)。
- **LR scheduler**：**WSD(Warmup-Stable-Decay)**；用 Scaling Law 拟合 L(Ω) 反解整段 LR；**全程零 loss spike**，按拟合预测终损 ~1.16、实际落 1.17–1.18（精度达 0.02）。
- **起点选择**：从**指令模型**(Qwen3-instruct)继续训略优于 base（仅 coding 域有明显优势；base 初始熵 0.19 vs CPT-on-instruct 0.15）；ViT 取 InternViT。
- 多模态 CPT 全参联合(不冻 LLM/ViT)，损失只在文本 token、square averaging。
- GPU 型号/总卡数/卡时/FLOPs：**官方未公开**。

### SFT / 离线 RL（论文 §5.1）
- 把 SFT 视为**离线 RL**：每条响应经 **best-of-N(BoN)** 按 accuracy/fluency/safety 选出（强调响应都"被奖励过"）。
- 指令数据 pipeline：Filtering(规则+模型去重复/截断/幻觉) → Labeling(≥3 级类目层级 + 用小模型多 rollout 的 passrate 定难度) → Enhancement(分层采样均衡 + 重构/合成补足)；覆盖 Agent/Code/对话/指令跟随/数学/推理/长文/安全/化学/生命/物理。
- 多模态指令数据沿用 InternVL3 + 用增强版 **SOPHIA** 造 VL 推理数据(拒绝采样/去重/长度格式约束/自洽/可验证)。
- 数据混合两步：原子能力验证(增量加各域看是否提分，baseline 从 **InternLM3 的 SFT 数据**按比例采样的 core set) → 组合能力验证(合并解冲突、style alignment + 课程学习定最优配比)。
- 同用随机 JPEG + squared loss；**最大上下文 32K**。

### 在线 RL / 对齐（论文 §5.2，核心创新）
- **Mixture-of-Rewards(MoR)**：统一 1000+ 任务的异质奖励为单一标量。易验证任务用规则 verifier / LLM verifier(**CompassVerifier**) / 环境反馈；难验证任务(创意写作/对话)用 **POLAR-7B**(策略判别学习奖励模型，预训练 3.6T 合成语料 + 150K 带参考偏好对微调)。
- **任务/环境**：**InternBootCamp** 提供 1000+ 种可无限生成的合成推理任务(算法/密码/图形谜题/棋类/逻辑/物理化学医学等)，每任务造 >10 万样本下采样到共 >2 万；指令跟随用 passrate@64∈[0.2,0.8] 选题；多模态 RLVR 用 OREAL-RL-Prompts/DAPO-Math-17k/Skywork-OR1 + MMPR/MMK12 等，部分选择题转填空去随机猜测噪声。
- **算法**：发现 GRPO 类直接用于大 MoE 会**训练崩溃**(推理/训练引擎数值差 + FP8 + 动态路由放大 → 专家激活不一致 → token 级裁剪不可靠)；采用自研 **OREAL**(正样本行为克隆 SFT loss + 负样本策略梯度，无 token 级 log-prob 比裁剪) + 借 CPGD 策略漂移与**KL-Cov**熵控制(只对协方差 top-k 的 token 加 KL，k=0.2、β=0.01) 防熵崩溃；总损失 = λ_sft·L_sft(正) + λ_pg·L_pg(负) + L_KL-Cov。
- **混合离线-在线过滤**：离线用 dense+MoE SFT 各 8 rollout，丢 br=1.0(太易) 与 br≤0.25(噪声)；在线每题 8 rollout 丢全对/全错与乱码/无限重复；对比 DAPO 在 Qwen2.5-32B 上 AIME2024 提升更快。
- **RL 超参**：每 prompt **8 rollout**，**train batch 4096**(分 8 mini-batch)，**AdamW LR 5e-7、wd 0.1、β=(0.9,0.95)**，**RL 全程 FP8**(rollout+train)，**冻 ViT 与 MoE router**，**训 600 步**；grad-norm>0.3 的 batch 丢弃(~3% 样本)；最后多 checkpoint **权重平均**。
- **RL infra**：FSDP + **1-way EP**(消除专家间通信、防 dropless MoE+大 EP 显存爆炸)；HybridFlow 式 train/infer **colocate**(每步 train mesh↔rollout mesh 重分布)；rollout 用 **LMDeploy EP8**、FP8 存权重、CPU offload + 连续批处理 + 动态再平衡防 straggler。号称比近期工作**省 10× RL 训练时间**。

### 推理 / serving / 量化
- 推理栈：LMDeploy(≥0.9.2)/vLLM(≥0.10.1)/SGLang/Ollama；FP8 权重；评测用 OpenCompass + VLMEvalKit，启用 thinking 模式，max tokens 65536、temp 0.7(mini 0.8)、top_p 0.95、top_k 50。
- 支持思考/非思考双模式切换 + 工具调用。

---

## 未覆盖 / gaps（明确标注，未编造）

- **InternLM v1**：GPU 型号/卡数/卡时/FLOPs、FFN 维、是否 RMSNorm/SwiGLU、各阶段 token 切分明细——官方未公开（报告偏方法）。
- **InternLM2/2.5/3**：训练用 GPU 型号、总卡数、卡时、总 FLOPs——三者均**官方未公开**（InternLM2 报告详述 InternEvo 效率与并行，但未给集群规模/卡时）。
- **InternLM2.5**：无独立技术报告，预训练总 token、数据配比%、SFT/RL 具体配方未单独公开。
- **InternLM3**：无独立技术报告，除"4T 高质量 token / 省 75% 成本 / 双思考模式"外，数据 pipeline、并行/精度、SFT 规模、RL 算法(PPO/DPO/RLVR)等均**官方未公开**。
- **InternVL 1.5**：细粒度 stage 超参/各阶段 token 在 1.5 报告未系统列(2.5 报告才公开)；语言能力依赖 InternLM2-20B(其配方见 InternLM2 节)。
- **Intern-S1**：训练 GPU 型号/卡数/卡时/总 FLOPs 未公开；CPT 各阶段精确 token 切分(除 5T/2.5T/250B 等总量)与各科学域具体百分比仅以饼图示意。
- **2026-H1 预印本（超出本次核心范围，PDF 已落盘但未逐数字展开）**：
  - **Intern-S1-Pro**（arXiv 2603.25040，万亿级科学多模态旗舰）：本地 `2026/files/intern-s1-pro.pdf`。
  - **InternVL-U**（arXiv 2603.09877，统一理解/推理/生成/编辑）：本地 `2026/files/internvl-u.pdf`。
  这两篇为 2026 较新预印本，编号(2603.*)需以官方最终发布为准；如需可单独深挖。

---

## 来源清单（仅一手官方）

### 技术报告 / arXiv
- InternLM v1 技术报告：https://github.com/InternLM/InternLM-techreport ｜本地 `2023/files/internlm-techreport.pdf`（文本 `deep-dive/files/internlm-techreport.txt`）
- InternLM2 Technical Report（arXiv 2403.17297）：https://arxiv.org/abs/2403.17297 ｜ PDF https://arxiv.org/pdf/2403.17297 ｜本地 `2024/files/internlm2.pdf`（文本 `deep-dive/files/internlm2.txt`）
- InternVL 1.5（arXiv 2404.16821）：https://arxiv.org/abs/2404.16821 ｜本地 `2024/files/internvl-1-5.pdf`（文本 `deep-dive/files/internvl-1-5.txt`）
- InternVL 2.5（arXiv 2412.05271）：https://arxiv.org/abs/2412.05271 ｜本地 `2024/files/internvl-2-5.pdf`（文本 `deep-dive/files/internvl-2-5.txt`）
- InternVL3（arXiv 2504.10479）：https://arxiv.org/abs/2504.10479 ｜本地 `2025/files/internvl3.pdf`（文本 `deep-dive/files/internvl3.txt`）
- Intern-S1 Technical Report（arXiv 2508.15763）：https://arxiv.org/abs/2508.15763 ｜ PDF https://arxiv.org/pdf/2508.15763 ｜本地 `deep-dive/files/intern-s1.pdf`（文本 `deep-dive/files/intern-s1.txt`）

### 官方 HF model card / config / GitHub
- InternLM3-8B-Instruct：https://huggingface.co/internlm/internlm3-8b-instruct ｜ config https://huggingface.co/internlm/internlm3-8b-instruct/raw/main/config.json ｜本地 `deep-dive/files/internlm3-8b-config.json`
- InternLM2.5-7B-Chat：https://huggingface.co/internlm/internlm2_5-7b-chat ｜ config(internlm2_5-7b) https://huggingface.co/internlm/internlm2_5-7b/raw/main/config.json ｜本地 `deep-dive/files/internlm2_5-7b-config.json`
- Intern-S1：https://huggingface.co/internlm/Intern-S1 ｜ config https://huggingface.co/internlm/Intern-S1/raw/main/config.json ｜本地 `deep-dive/files/intern-s1-config.json` ｜ GitHub https://github.com/InternLM/Intern-S1
- InternLM 主仓 GitHub README（版本时间线/model zoo）：https://github.com/InternLM/InternLM
- InternVL 主仓 GitHub：https://github.com/OpenGVLab/InternVL
