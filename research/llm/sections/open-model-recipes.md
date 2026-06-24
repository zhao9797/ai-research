# 开源模型训练配方专章（数据 · 配比 · 训练 · SFT · RL）

> 本章浓缩自 12 份家族深挖档案（`deep-dive/` 目录），只用档案里的真实一手数字（arXiv/技术报告/官方 config）。
> 凡档案标注"官方未公开"者本章亦如实标注，不臆造。
> 组织方式：先看总览与开源透明度梯队，再按家族给出"架构要点 / 数据与处理与配比 / 训练 / SFT / RL"五段式浓缩，最后做跨家族横向对比。

---

## 一、总览：开源透明度梯队（全开数据 vs 仅开权重）

这批开源模型在"开放到什么程度"上存在巨大分层。本章把它们排成一条从最透明到最封闭的梯队：

**梯队 0 — 全栈全开（权重 + 预训练语料 + 处理代码 + 训练码 + 中间检查点 + 训练日志）**
- **AI2 OLMo/Dolma/Tülu**：最透明，几乎每一个数字都能在官方报告里找到（Dolma 语料、OLMo-core 训练码、Tülu 后训练码、逐 checkpoint、能耗碳排都公开）。
- **EleutherAI Pythia / GPT-NeoX-20B**：训练动力学研究基石，公开 154 检查点/模型 + dataloader 重建工具。
- **BigScience BLOOM/ROOTS**：千人协作，权重/1.61TB 语料/代码/完整训练日志全开。
- **M-A-P MAP-Neo、INF/M-A-P OpenCoder**：首批"全栈全开"的中英双语 / 代码 LLM（语料 + 处理 + ckpt + 对齐全开）。
- **数据集项目**（这条线的灵魂）：The Pile、RefinedWeb、The Stack v1/v2、RedPajama、DCLM —— 不放模型只放语料与处理 pipeline。

**梯队 1 — 开权重 + 详尽技术报告（数据来源/配比、训练超参、infra 大量公开，但语料本身不开放）**
- **DeepSeek**（V2/V3/R1 报告极详，连 FP8 量化粒度、DualPipe、卡时美元成本都给）。
- **Qwen**（v1/2/2.5/3 有 arXiv 报告，数据 pipeline、SFT/RL 配方详；但算力/并行多标"官方未公开"）。
- **NVIDIA Nemotron**（合成数据 pipeline、RPO、卡数卡型、FP8/NVFP4 配方都开源，连 RL 环境都放）。
- **InternLM2**（该家族最透明的一手文档：数据字节占比、COOL RLHF、PPO 全超参）。
- **新生代大 MoE 多数**：Kimi K2、MiniMax-01、Hunyuan-Large、Skywork-MoE、dots.llm1、Ling/Ring 2.0、Pangu —— 报告详尽程度不一，但普遍给架构表 + 数据 pipeline + RL 算法。

**梯队 2 — 开权重 + 中等报告（架构与方法公开，数据配比/算力多为定性）**
- **Llama**（LLaMA1/2/3 报告详，尤其 Llama3 的 infra/后训练；但 Llama4 无 arXiv 仅博客，大量"官方未公开"）。
- **Gemma**（架构表 + 蒸馏/QAT 细节公开，但 global batch、优化器、LR schedule、各域数据百分比"普遍未公开"）。
- **GLM/ChatGLM**（GLM-4.5/GLM-5 报告详于后训练与 RL，但算力/卡时/预训练精度多未公开）。
- **MiniCPM**（WSD/风洞/退火方法论极透明，但 GPU 卡时/并行基本未公开）。

**梯队 3 — 开权重 + 极简报告（刻意只给"架构表 + 评测"，数据/训练/RL 几乎全不写）**
- **Mistral/Mixtral**：一贯不透明，预训练 token 数、数据来源/配比、算力、并行、优化器、RL 超参"几乎从不公开"——这是 Mistral 的风格，不是检索不到。Phi-2 也只有博客（层/头/配比未公开）。

> 一个有趣的反差：**全开数据梯队（OLMo/Pythia/BLOOM）反而最敢公开能耗碳排与卡时**（OLMo3 Think 32B 公开"56 天 / 1024 H100 / ≈$2.75M"），而能力最强的旗舰（Mistral/Llama4/Gemma）反而对算力守口如瓶。DeepSeek 是少见的"既强又敢报成本"的例外（V3 全程 2.788M H800 卡时 ≈ $5.576M）。

---

## 二、各家族浓缩配方

### 1. DeepSeek（幻方）—— scaling law 立项 → MoE 降本 → MLA → FP8/DualPipe → GRPO/纯RL → DSA

**架构要点**
- 主线：MHA/GQA（LLM/Coder）→ **DeepSeekMoE 细粒度专家 + 共享专家隔离**（MoE 起，共享:路由=1:3）→ **MLA 多头潜注意力**（V2 起，KV cache 降 93.3%、训练降本 42.5%）→ **无辅助损失负载均衡 + MTP**（V3）→ **DSA 稀疏注意力**（V3.2，O(L²)→O(Lk)，每 query 取 top-k=2048）。
- V3 旗舰：671B/37B、61 层、MLA 128 头、1 共享 + 256 路由 / 激活 1+8、路由 affinity 用 Sigmoid；前 3 层 dense 其余 MoE。BBPE vocab 128K。

**数据与处理与配比**
- 激进去重：跨整个 Common Crawl（91 dump）去重，去重率从单 dump 22.2% 提到 89.8%。三步：去重 → 过滤 → remix（补欠表示领域）。
- token 量演进：LLM 2T → V2 8.1T → V3 **14.8T**（提高数学/编程占比、扩多语，文档打包，FIM rate 0.1）。
- DeepSeekMath 首创"代码续训先于数学训练能提升数学；训 arXiv 论文对数学无明显提升"；用迭代 fastText 召回从 CC 抠 120B 数学 token。

**训练（算力·并行·精度·阶段）**
- V3：**2048×H800**，16-way PP + 64-way EP + ZeRO-1，**无 TP**；**DualPipe** 双向流水隐藏 all-to-all 通信；跨节点 all-to-all kernel 仅用 20/132 个 SM。
- **FP8 训练**（首次超大模型验证）：三大 GEMM 走 FP8、细粒度量化（激活 1×128 tile、权重 128×128 block）、每 128 间隔提到 CUDA Core 做 FP32 累加、全张量 E4M3；相对 BF16 loss 误差 <0.25%。优化器矩用 BF16，master weight/梯度 FP32。
- 多步 LR（替代 cosine）：2K warmup → 恒定 2.2e-4 至 10T → cosine 降到 2.2e-5 → 末 500B 两段恒定。batch 前 469B 从 3072 增到 15360。
- **训练极稳：全程无不可恢复 loss spike、无回滚**。成本 2.788M H800 卡时 ≈ $5.576M。

**SFT**
- V3：1.5M 实例分域定制；推理数据用内部 R1 生成（专家模型 + 高温 RL 融合 + 拒绝采样）；非推理数据用 V2.5 生成 + 人核。2 epoch，cosine 5e-6→1e-6。

**RL 对齐**
- **GRPO**（DeepSeekMath 发源）：去掉 critic，用组内相对优势 A_i=(r_i−mean)/std；是 DeepSeek 全部 RL 的算法基石。
- **R1-Zero**：纯 RL（绕过 SFT）即激发推理；纯规则奖励（accuracy+format），LR 3e-6、KL 0.001、温度 1、每 question 16 输出、batch 512、共 ~10400 步。AIME24 pass@1 15.6%→77.9%。
- **R1 多阶段**：冷启动 SFT → 推理 RL（GRPO clip ε=10 + 语言一致性奖励）→ 拒绝采样 SFT(800K=600K 推理+200K 非推理) → 全场景 RL（温度降 0.7，model-based 奖励仅最后 400 步加入防 hacking）。
- 蒸馏 6 个 Qwen/Llama 小模型（只 SFT 不 RL）。
- V3.2：**Mixed RL 单阶段**（推理+agent+对齐合并防遗忘）+ Specialist Distillation 六域专家；Scaling GRPO 稳定性技巧（Keep Routing、Off-Policy Sequence Masking、修正 K3 KL）。

---

### 2. Qwen（阿里）—— 数据规模狂飙 + DPO/GRPO 两阶段 RL + hybrid thinking → 极致稀疏混合架构

**架构要点**
- v1：MHA + RoPE-FP32 + QKV-bias + SwiGLU(8/3h) + tiktoken 扩词表≈152K。Qwen2 全面 GQA。
- Qwen3：去 QKV-bias、加 **QK-Norm**；MoE **128 专家激活 8、取消共享专家、global-batch load balancing**；235B-A22B / 30B-A3B。
- Qwen3-Next（80B-A3B）：**Gated DeltaNet 线性 + Gated Attention 混合 3:1 + 512 专家极致稀疏（激活~3B）+ MTP + Zero-Centered RMSNorm**。

**数据与处理与配比**
- token 狂飙：v1 3T → Qwen2 7T → Qwen2.5 **18T** → Qwen3 **36T、119 语言**。
- 用模型自过滤：Qwen2 用 Qwen 本身过滤低质 + 合成；Qwen2.5 用 Qwen2-Instruct 当多维质量打分器；Qwen3 用 Qwen2.5-VL OCR 抽 PDF + 三个 Qwen2.5 模型合成数万亿 token，按 educational value 多维标注 + instance-level mixture 优化。
- Qwen2.5-Coder：消融 100:0:0 vs 85:10:5 vs **70:20:10**（Code:Text:Math）选 70:20:10，5.5T。
- Qwen3 预训练三阶段：General(>30T,4096) → Reasoning(+~5T 高质,加速 LR 衰减) → Long Context(数千亿,32768,RoPE base 1e6,YaRN+DCA)。

**训练（算力·并行·精度·阶段）**
- 全系 BF16；FlashAttention 全系；长上下文标配 RoPE ABF + YaRN + DCA。
- **算力/并行/卡时官方一贯未公开**（v1-v2.5/Qwen3 报告均不给 GPU 数字）。
- Qwen3-Max 首次公开自研 infra：PAI-FlashMoE（MFU 相对 +30%）、ChunkFlow（长序列吞吐 3×，支持 1M 训练）；全程无 loss spike。

**SFT**
- Qwen2 >500K 例；Qwen2.5 **>1M 例**，2 epoch、seq 32768、LR 7e-6→7e-7。9 大方向，含 rejection sampling + execution feedback。

**RL 对齐（两阶段）**
- **Offline DPO**（约 150K 训练对，Online Merging Optimizer 缓解 alignment tax）+ **Online GRPO**（每 query 8 响应，global batch 2048）。
- QwQ-32B：纯 RL scaling（math 用 accuracy verifier、code 用 execution server，不用 RM）→ 通用 RL；32B 对标 DeepSeek-R1 671B。
- Qwen3 后训练四阶段：Long-CoT 冷启动 → **Reasoning RL（仅 3,995 query-verifier 对，GRPO，170 步把 AIME24 70.1→85.1）** → Thinking Mode Fusion（/think、/no_think）→ General RL。+ **Strong-to-Weak 蒸馏**（on-policy 对齐 teacher logits，比四阶段省 ~9/10 GPU hours）。
- Qwen3-Coder：阿里云**同时跑 20,000 个独立环境**做 Long-Horizon Agent RL。

---

### 3. Llama（Meta）—— 纯公开数据立 SOTA → 工业级 RLHF → 弃 PPO 改 DPO 迭代 → 原生多模态 MoE

**架构要点**
- 三件套奠基：Pre-norm RMSNorm + SwiGLU + RoPE。Llama2 起 34B/70B 引入 GQA(8 KV)。
- Llama3：稠密 8B/70B/405B（**刻意不用 MoE 求稳定**），GQA 8 KV + 文档掩码 + 128K 词表 + RoPE θ=500,000。
- Llama4：**首个原生多模态 MoE（early fusion）**：Scout(17B激活/109B总/16专家)、Maverick(17B/400B/128专家+1共享)、Behemoth(288B激活/≈2T/16专家 teacher)；**iRoPE**（交错 NoPE + RoPE）+ FP8 + MetaP + co-distillation。

**数据与处理与配比**
- LLaMA1：约 1.4T 纯公开数据（CC 67% + C4 15% + GitHub/Wiki/Books/ArXiv/StackExchange）。
- Llama3：约 **15T（405B 实训 15.6T）**，data mix = 通用知识 50% / 数学推理 25% / 代码 17% / 多语 8%。三级去重（URL→文档 MinHash→行级）+ fasttext/DistilRoberta 质量分类器 + 代码/推理专项分类器。
- Llama4：整体混合 **>30T**（文本+图+视频，是 Llama3 的 2 倍多），预训练 200 语言。

**训练（算力·并行·精度·阶段）**
- Llama2：累计 **3,311,616 A100-80GB 卡时**，539 tCO2eq（全抵消）。
- Llama3-405B：最多 **16K×H100**、BF16、峰值 **3.8×10²⁵ FLOPs**；**4D 并行 [TP, CP, PP, DP]**，8192 GPU 时 MFU 43%；三阶段（初始 → 长上下文分 6 阶段扩到 128K 约 800B token → **退火**最后 40M token LR 退到 0 + Polyak 平均）。54 天内 466 次中断 >90% 有效训练时间。
- Llama4：FP8；Behemoth FP8 + 32K GPU 达 390 TFLOPs/GPU；其余并行/batch/路由"官方未公开"。

**SFT**
- Llama2："Quality Is All You Need"，仅 27,540 条高质量标注，2 epoch。
- Llama3：拒绝采样（K=10–30 取 RM 最高）+ 合成数据；代码训 code expert（约 1T token >85% 代码）。

**RL 对齐**
- Llama2：工业级 RLHF 首次完整公开 —— **双奖励模型（Helpfulness + Safety RM）+ 拒绝采样 + PPO（V4 后叠加）+ Ghost Attention**；偏好数据 1.4M Meta + 开源共 2.9M；RM loss 带 margin 项。
- Llama3：**弃 PPO 选 DPO，迭代 6 轮**（每轮 RM→拒绝采样→SFT→DPO）；DPO LR 1e-5、β=0.1、mask 格式 token + NLL 正则；数学用 stepwise PRM + MCTS。
- Llama4：**轻量 SFT → online RL → 轻量 DPO**（SFT/DPO 会过约束限制 RL 探索，故 Llama-as-judge 去掉 >50% easy 数据）；全异步 online RL 框架，训练效率较前代约 10×。

---

### 4. GLM/ChatGLM（智谱 Z.ai）—— blank-infilling → GPT式dense → MoE → MoE+DSA；Muon + slime

**架构要点**
- 主线：blank-infilling GLM（GLM-130B：DeepNorm+Post-LN+RoPE+GeGLU）→ GPT 式 dense（GLM-4：no-bias-except-QKV + RMSNorm + SwiGLU + GQA + 2D-RoPE）→ MoE（GLM-4.5）→ MoE+稀疏（GLM-5：MLA+Muon Split → DSA）。
- GLM-4.5：355B/32B，3 dense+89 MoE，**loss-free routing + sigmoid 门控、降宽增深、2.5× 注意力头（5120 维配 96 头）、QK-Norm、MTP 当 MoE 层**；160 专家激活 8 + 1 共享。
- GLM-5：744B/40B、256 专家、层数降到 80（减 EP 通信）；**MLA + Muon Split**（按头拆分正交化追平 GQA-8）；DSA 从 dense base 继续预训练引入（dense warm-up 1000 步 + sparse adaptation **仅 20B token**，远小于 DeepSeek-V3.2 的 943.7B）。

**数据与处理与配比**
- GLM-4.5：**23T token**。Web 仿 Nemotron-CC 分质量桶（最高桶训练贡献 >3.2 epoch）+ SemDedup；代码全用 FIM；数学按"教育性比例"打分上采样。两阶段预训练 + Mid-training（repo-level 代码 500B + 合成推理 500B + 长上下文&agent 100B）。
- GLM-5：**28.5T**，加 DCLM 句嵌入分类器；代码模糊去重唯一 token +28%。

**训练（算力·并行·精度·阶段）**
- **优化器 Muon**（GLM-4.5/GLM-5，Newton-Schulz N=5、μ=0.95、update RMS 缩到 0.2）；LR cosine（WSD 在 SimpleQA/MMLU 欠拟合）；batch warmup 500B 内 16M→64M。
- GLM-5：INT4 QAT（SFT 阶段，bitwise 训练/推理一致）；**国产 7 平台首日适配**（昇腾/摩尔线程/海光/寒武纪/昆仑/沐曦/燧原）。
- **算力/卡时除 GLM-130B（768×A100、60 天）外均官方未公开**；pre-train 主精度未明示（仅 RL rollout 用 FP8）。

**SFT**
- 专家模型迭代两阶段：分别训 Reasoning/Agent/General 三专家（各 cold-start SFT + 专家 RL）→ 自蒸馏融成一个 hybrid reasoning 模型。Function call 用 XML 风格特殊 token。

**RL 对齐**
- **GRPO（去掉 KL loss 项）**；Reasoning RL 用难度课程两阶段（中等 16 样本 → 极难题 512 样本）+ 单阶段 64K 输出长度 RL（多阶段会不可逆掉点）。
- GLM-5：**GRPO + IcePop**（区分 π_train/π_infer 去 KL，β=2、ε_low 0.2/ε_high 0.28、全 on-policy group 32）+ 异步 agent RL（TITO gateway、Direct Double-sided Importance Sampling）+ **on-policy 跨阶段蒸馏**。
- DSA RL 洞见：indexer 用确定性 torch.topk（非确定性 CUDA top-k 几步内崩溃）；RL 期默认冻结 indexer。
- **自研 slime**（Megatron 训练 + SGLang rollout + Data Buffer，BF16 训练 / FP8 rollout，同步 colocated 与异步 disaggregated 双模式）。

---

### 5. OLMo/Dolma/Tülu（AI2）—— 全开放标杆 + RLVR 范式发源 + OlmoRL 提速

**架构要点**
- 全家族：decoder-only、SwiGLU、RoPE、无 bias。OLMo2 起的稳定性改造：**RMSNorm + reordered norm（归一化放子层输出）+ QK-Norm + Z-loss(1e-5) + RoPE θ 10k→500k**。
- OLMoE-1B-7B：首个全开放稀疏 MoE，64 细粒度专家 top-8、激活 1.3B/总 6.9B、**无共享专家、dropless token-choice、不用 sparse upcycling**。
- OLMo3：SWA（窗口 4096，每 4 层 3 层 SWA，末层 full）+ YaRN（仅 full-attention 层）扩到 65K。

**数据与处理与配比**
- Dolma 3T（CC 2.28T + code 411B + Reddit 80B + peS2o/Gutenberg/Wiki），开源 Rust 工具（Bloom filter 线性去重）。
- OLMo2 两阶段：Stage1 OLMo2 Mix 1124（3.90T，>95% web，DCLM-Baseline 95%）→ **Stage2 mid-training Dolmino**（高质量退火 50B/100B/300B）。
- OLMo3 三阶段：Dolma3 Mix（6T：CC 76.1% + olmOCR PDF 13.6% + Stack-Edu 6.89% + FineMath 2.56%）→ Dolmino 100B → Longmino 长上下文。三大新意：万亿级全局去重新工具、token-constrained mixing、olmOCR 把学术 PDF 转纯文本。

**训练（算力·并行·精度·阶段）**
- OLMoE：256 H100 ~10 天。OLMo2：两套集群（Jupiter 1024 H100 + Augusta 160×A3），7B+13B 预训约 391 MWh；OLMo-core 训练栈。
- OLMo3：HSDP + Llama3 风格 CP；MFU 7B~43%/32B~41%；**model souping**（多种子退火后平均）。
- **罕见公开成本**：OLMo3 Think 32B 训到评测约 **56 天 / 1024 H100 / ≈$2.75M**。

**SFT**
- 套 Tülu 配方；Tülu3 SFT mix **939,344 prompt**（用 PersonaHub ~250K personas 合成技能定向 prompt），LR 8B 5e-6/70B 2e-6、2 epoch、**sum loss**。

**RL 对齐**
- **首次系统提出 RLVR（可验证奖励 RL）**：v=验证器，正确给 α=10 否则 0；确立 SFT→DPO→RLVR 三段式。
- Tülu3 RLVR 用 PPO，value 从 general RM 初始化；数据 ~30K（GSM8K+MATH+IF verifiable）。
- OLMo2：7B/13B 用 PPO、1B/32B 用 GRPO。
- OLMo3 **OlmoRL = GRPO + DAPO + Dr GRPO**（零梯度过滤 + active sampling + token-level loss + 去 KL + clip-higher + truncated importance sampling + 不按组 std 归一化）；**全异步 off-policy + continuous batching**（static batching 浪费高达 54%）；**4x 提速**（7B Think RL 旧 infra 15 天 → 新 6 天）。
- Think DPO 用 **Delta Learning**（偏好看 chosen/rejected 的能力差而非绝对质量）。

---

### 6. Gemma（Google DeepMind）—— 从 Gemini 下放 + 知识蒸馏范式 + QAT

**架构要点**
- 沿用 Gemini：RoPE + GeGLU + RMSNorm + 256k 词表。Gemma1 2B 用 MQA、7B 用 MHA。
- Gemma2：**局部/全局注意力交替 1:1**（局部窗 4096）+ GQA + **logit soft-capping**（attn cap 50、final cap 30）+ pre-norm+post-norm 双 RMSNorm。
- Gemma3：**5:1 局/全注意力**（局部窗仅 1024，压 KV cache）+ **QK-norm 取代 soft-capping** + 全局层 RoPE base 提到 1M + SigLIP 视觉编码器 + 128K 上下文。

**数据与处理与配比**
- token 量：Gemma1 2B/7B = 3T/6T；Gemma2 2B/9B/27B = 2T/8T/13T；Gemma3 1B/4B/12B/27B = 2T/4T/12T/14T。主英语，web/数学/代码三类。
- 过滤：启发式 + 模型分类器 + 去污染评测集 + Google Cloud Sensitive Data Protection 查 PII。Gemma3 新增质量重加权。
- **各域数据百分比官方未公开**。

**训练（算力·并行·精度·阶段）**
- 硬件 **TPUv4/v5e/v5p**（pod=256 chips）；JAX/Pathways/GSPMD/MegaScale XLA + 类 ZeRO-3。Gemma2-27B 用 6144 chips。
- **精度/global batch/优化器/LR schedule/warmup 普遍官方未公开**（QAT 5000 步除外）。
- **QAT**：随 raw ckpt 放出量化版（每模型额外微调约 5000 步，以非量化 ckpt 概率为目标），三种表示 per-channel int4 / per-block int4 / switched fp8。

**SFT**
- 在纯文本纯英语合成+人工对上 SFT；**行为克隆**（response 主要由教师合成）+ on-policy distillation。

**RL 对齐**
- **核心创新是知识蒸馏**：Gemma2 的 2B/9B 用蒸馏代替 next-token（在远超 compute-optimal 50× 的 token 量上蒸馏），27B from scratch；Gemma3 每 token 采样 256 个 logits 按教师概率加权学。
- RLHF：奖励模型比策略大一个数量级 + Model merging。
- Gemma3 RL 用 **BOND/WARM/WARP** + 多奖励：WARM（人类反馈）+ 代码执行反馈 + **数学 ground-truth 可验证奖励（即 RLVR 路线，明确引用 DeepSeek-AI 2025）**。

---

### 7. Mistral/Mixtral（Mistral AI）—— 极简报告 + SWA + 经典 top-2 MoE

**架构要点**
- 共性：decoder-only + RMSNorm + RoPE + SwiGLU + GQA(8 KV)；RoPE base 从 7B 时代后统一升到 1e6。
- Mistral 7B：**滑动窗口注意力 SWA（窗口 4096）+ 滚动缓冲缓存**（32k 序列缓存内存降 8×）。
- Mixtral：SMoE，每层 FFN 换 8 专家 top-2（8x7B=47B/13B，8x22B=141B/39B），**有负载均衡辅助损失 router_aux_loss_coef=0.001，无共享专家**；Mixtral 8x7B 起改全密集 32k（不再 SWA）。
- Tokenizer 换代：SentencePiece(32000) → 32768 → **Tekken/tiktoken 131072**（NeMo/Pixtral 起）。

**数据与处理与配比**
- **几乎全部官方未公开**——预训练 token 数、数据来源/配比、pipeline 刻意不写。唯一披露：Mixtral 8x7B"显著上采样多语言数据"；Codestral 80+ 编程语言；Mistral Large 2"非常大比例代码 + 大比例多语言"。

**训练（算力·并行·精度·阶段）**
- **几乎全部官方未公开**。仅致谢透露用 CoreWeave/Scaleway/Leonardo 超算。全部 BF16；NeMo 额外 QAT 支持 FP8 推理。

**SFT / RL 对齐**
- 唯一明确公开的 RL 算法是 **Mixtral 8x7B 的 SFT→DPO**（无偏好数据规模/β/KL）。其余型号只说"微调与对齐"，未公开是否 DPO/PPO，**无 RLVR/GRPO 迹象**。Mistral Large 2 重点做了减少幻觉对齐（信息不足时承认"不知道"）。

---

### 8. InternLM（上海 AI Lab）—— 最透明的国产一手文档 + COOL RLHF + InternEvo

**架构要点**
- v1：104B 稠密 GPT 式（82 层/10240/80 头/65.5K 词表/2K 上下文）。
- InternLM2：对齐 LLaMA（RMSNorm+SwiGLU）+ 全系 GQA（KV 一律 8）+ GPT-4 cl100k 改造词表(92544) + 合并 Wq/Wk/Wv 加速 >5% + 按 head 交错布局便于改 TP。
- InternLM3-8B：新 `internlm3`，深度 GQA（KV=2）、vocab 128512、**RoPE θ=5e7**、内置 long-CoT + 常规双模式。
- Intern-S1：科学多模态 MoE（Qwen3-235B + InternViT-6B + 动态分子/蛋白 tokenizer + 时序编码器）。

**数据与处理与配比**
- InternLM2 给出按字节的精确配比：en-webpages 67.51% / zh-webpages 18.95% / zh-techlit 4.94% / en-techlit 4.27% / zh-books 2.71% / en-books 1.63%。代码按打分分 High/Moderate/Low 差异化 epoch。
- pipeline：Trafilatura 抽正文 → 规则过滤 → **MinHash LSH（128 哈希、5-gram、阈值 0.7）** → 安全过滤（13M 不安全域名 + 36,289 词黑名单 + BERT 毒性/色情分类器）→ 质量过滤（广告/流畅度分类器）。长上下文用 **PPL diff 过滤**段间连贯。
- InternLM3：**仅 4T 高质量 token，号称省 >75% 训练成本**。

**训练（算力·并行·精度·阶段）**
- 三阶段：4k 上下文（~90% 步）→ 长上下文 32k（~9% 步，RoPE base 50k→1M）→ 能力定向增强（24.4B token：检索 STEM 65% + 特定域 8% + 高质 26%）。
- **InternEvo**（自研）：自适应分片（Full/Full-Sharding/Partial）+ 执行模拟器自动搜并行；7B 8卡 64% MFU、1024 卡 53% MFU；支持 256K 序列（7B@256k 近 88% MFU）。
- **GPU 型号/卡数/卡时/FLOPs 三代均官方未公开**。

**SFT**
- v1 约 5M、InternLM2 **10M** 指令样本，ChatML 格式，1 epoch、LR 4e-5。

**RL 对齐**
- **COOL RLHF**：① 条件奖励模型（单 RM 用不同 system prompt 调和 helpful/harmless/code/math 冲突偏好，240 万偏好对、焦点排序损失 γ=2）② 在线多轮 PPO（Fast Path 快修 reward hacking + Slow Path 提 RM 上界，共 3 轮）。
- PPO 细节：4 等大模型、~20 万 query/~400 迭代、critic 先预训 50 迭代、加 pre-train loss(系数 0.5) 防遗忘、KL 系数 0.01、actor LR 1e-6/critic 5e-6、不做 value clipping/advantage normalization。
- Intern-S1：**Mixture-of-Rewards(MoR)** 统一 1000+ 任务异质奖励 + 自研 **OREAL + KL-Cov**（发现 GRPO 直接用于大 MoE 会崩溃：推理/训练引擎数值差 + FP8 + 动态路由放大 → token 级裁剪不可靠）；RL 全程 FP8、冻 ViT 与 MoE router。

---

### 9. MiniCPM（面壁/OpenBMB）—— WSD + 模型风洞 + 退火数据注入 + 端侧极致

**架构要点**
- 招牌方法论：**Model Wind Tunnel（µP 风洞搜超参）+ WSD（Warmup-Stable-Decay）调度 + 两阶段预训练 + 退火数据注入**。
- v1：深瘦网络（2.4B 40 层 MHA；1.2B 52 层 GQA）+ 共享输入输出 embedding。
- MiniCPM3：改用 **MLA**（62 层极深瘦）。MiniCPM4：**InfLLM v2 可训练稀疏注意力**（KV 分块 Top-K 块选择 + 语义核，号称比 NSA 省 60% 计算）+ µP（dim_model_base=256）。
- MiniCPM-SALA：InfLLM-V2 稀疏 + Lightning 线性混合 1:3 + HyPE，1M 上下文。

**数据与处理与配比**
- v1：稳定段 ~1T 粗质量数据 + 退火段混入高质量知识/SFT 数据。**消融：退火段加 SFT 数据远优于只在 SFT 阶段加**；退火约占 10% token 足够。
- **数据-模型比 ≈ 192:1**（远高于 Chinchilla 的 ~20:1）。
- MiniCPM4：**8.3T token**（UltraFineWeb），UltraClean 高效验证策略——不从头训 LLM 验数据，而是先用 WSD 训 1B 到 1.1T，再用退火段性能增益当质量指标，把单次验证从 1200 GPU·h 降到 ~110 GPU·h；FastText 分类器全 web 规模过滤。

**训练（算力·并行·精度·阶段）**
- WSD：稳定段恒定高 LR（MiniCPM4 8B 7e-3），退火段指数衰减（T=5000 步=20B token）。
- MiniCPM4 四阶段：稳定 7T → 退火 1T → 长上下文 32K(20B,LongRoPE) → 混合 SFT+RL。**FP8 混合精度**（仿 DeepSeek-V3，仅线性投影用 FP8，参数梯度用 BF16）+ MTP。
- **预训练 GPU 卡时基本未公开**（仅 RL 段披露 64×A800）。

**SFT**
- v1 约 6B token；MiniCPM4 用 **UltraChat v2**（五能力轨：知识/推理/指令/长上下文/工具）。

**RL 对齐**
- v1：DPO（1 epoch，LR 1e-5，UltraFeedback）。
- MiniCPM4：先 SFT long-CoT 冷启动 → **改进版 GRPO**（Dynamic Sampling + Clip-Higher + Token-level loss + Overlong Filtering）+ **Chunk-wise Rollout**（限每轮 rollout 输出，未完成存重放下轮续，负载均衡）；**RLVR**（数学用 SymPy 验证、代码在 Firejail 沙箱跑测试）。

---

### 10. NVIDIA Nemotron + Microsoft Phi —— 数据质量/合成数据信仰（小模型打大模型）

**架构要点**
- Phi：基本保持稠密 Transformer（靠数据 + 后训练取胜），仅 phi-3.5-MoE 例外（16×3.8B top-2）。phi-4-mini 改 GQA(24q/8kv) + o200k 词表 200K。
- Nemotron 架构演进：稠密(4-15B/340B，**squared ReLU + 256K 词表**) → **hybrid Mamba-Transformer**（H/Nano2，约 8% 层是 self-attention，其余 Mamba-2 + FFN，无位置编码）→ **hybrid Mamba MoE + LatentMoE + MTP**（3 Super/Ultra，512 专家 top-22）。

**数据与处理与配比**
- **共同信仰：数据质量/合成数据 > 堆规模**。Phi 发明"教科书质量"合成路线（phi-1 用 GPT-3.5 合成 Python 教科书）；phi-4 合成占 **40%**（50 类合成数据集 ~400B token）；Nemotron-4-340B 对齐 **>98% 合成数据**；Nemotron-H 的 6.3T CC 中 **1.9T 为合成改写**。
- Nemotron-4 15B：8T，配比英文 70% / 多语 15% / 代码 15%。Nemotron-H：最高 20T，全局去重 + 5 桶 model-based 分类器集成 + 低质改写提质（比 DCLM 高 5.6 MMLU 点）；**4 阶段 phased data-blending** 比随机序好 3.4%。
- Nemotron-Nano-CC-Math-v1：133B 数学 token（Lynx+LLM 标准化为 LaTeX）。

**训练（算力·并行·精度·阶段）**
- Nemotron-4 15B：384×DGX-H100（3072 H100），8-way TP + DP。Nemotron-4 340B：768×DGX-H100（6144 H100），8-way TP + 12-way PP。
- **精度路线领跑**：Nemotron-H-56B 首个全 FP8 预训练（hybrid FP8：权重/激活 E4M3、梯度 E5M2、per-tensor 动态量化）；**Nemotron 3 全系 NVFP4**（E2M1 元素 + 16 元素 micro-block + E4M3 micro-block scale + FP32 global scale，wgrad 做 Random Hadamard Transform + stochastic rounding，稳到 25T token）。
- Phi：phi-1 8×A100 训 4 天；phi-2 96×A100 训 14 天；其余 GPU 数/卡时未公开。

**SFT / RL 对齐**
- Nemotron-4-340B 首创 **RPO（Reward-aware Preference Optimization）**：用 RM 的奖励差当目标 margin；两阶段 SFT（Code SFT 800K → General SFT 200K）+ Iterative Weak-to-Strong Alignment；奖励模型用 5 维 HelpSteer 回归头，发布时 RewardBench 居首。
- Llama-Nemotron/Nano2/Cascade-2/3 系列用 **GRPO**（Cascade-2 完全去 KL 退化为 token-level REINFORCE）；3 Ultra 用多环境 RLVR + **MOPD（Multi-teacher On-Policy Distillation）**（>10 个领域专用 teacher dense token-level 蒸馏）。
- Phi-4：**Pivotal Token DPO**（只针对决定答案对错的关键 token 构造 DPO 对）+ Judge-Guided DPO（~850k 对）。Phi-4-reasoning-plus：**GRPO 仅数学**（72,401 题、~16K 步、batch 32、rule-based length-aware accuracy reward）。

---

### 11. 新生代大 MoE（Kimi K2 / MiniMax / Hunyuan / Skywork / Step-3 / dots / Ling-Ring / Pangu）

**Kimi K2（Moonshot，1.04T/32.6B）**
- 架构：MLA 64 头（DeepSeek-V3 砍半）、**384 路由 + 1 共享 top-8**（sparsity=48，由 sparsity scaling law 选定，比 sparsity 8 省 1.69× FLOPs）、无 expert grouping、vocab 163,840。
- 数据：15.5T，合成数据重写（知识域 chunk-wise 自回归重写 + fidelity 校验，每语料最多重写 2 次；实验重写 1 次×10 epoch=27.39 SimpleQA 优于原始 23.76）。
- 训练：H800、PP + 16-way EP + ZeRO-1、BF16（MoE up-proj/SwiGLU 输入压 FP8 仅存储不计算）、**优化器 MuonClip**（Muon + QK-Clip）、WSD、global batch 67M、**全程零 loss spike**。
- RL：K1.5 策略目标 + **可验证奖励 Gym（RLVR，Coding 用 K8s 沙箱 >10,000 并发）+ Self-Critique Rubric Reward**（actor/critic 闭环把客观信号蒸进评判模型）+ Budget Control + PTX Loss + Temperature Decay。

**MiniMax-01（456B/45.9B）**
- 架构：**混合 7 lightning(线性) : 1 softmax-GQA**，32 专家 top-2 无共享，RMSNorm+DeepNorm；训练 1M 上下文，推理外推 4M。
- 训练：1500–2500×H800、EP+ETP+EDP、AdamW、~11.5T（7.2T 常数 LR 2e-4 → 调到 1.3e-4 训 3.2T → fast decay 1T 到 3e-5），critical batch 动态翻倍到 128M。
- RL：四维 RM + Offline DPO + Online 改进版 GRPO（重要性采样双侧裁剪 + KL 重构 stop-gradient + 平衡优势估计），后训练 5 阶段（含长上下文 DPO 序列 1,032,192）。

**Hunyuan-Large（腾讯，389B/52B）**
- 架构：**GQA(80/8) + CLA（每 2 层共享 KV cache）双重 KV 压缩省近 95%**；1 共享 + 16 specialized 专家激活 1+1；256K 上下文。
- 数据：7T（含 1.5T 合成，4 步：指令生成→演化→回复→critique 过滤）。**Recycle Routing**（溢出 token 回收重路由）+ **Expert-Specific LR Scaling**。
- RL：DPO 单阶段（offline+online 一体），chosen 上加 SFT loss + EMA 防 reward hacking。

**Skywork-MoE（昆仑万维，146B/22B）**
- 从 Skywork-13B upcycle，16 专家 top-2。两创新：**Gating Logit Normalization** + **Adaptive Auxiliary Loss Coefficients**（逐层自适应）。系统讨论 upcycle vs from scratch。
- 1536×A800、12-way PP + 4-way tensor-expert(EDP) + 32-way DP + ZeRO-1，MFU 38%。

**Step-3（阶跃，316B/38B）**
- 架构：**MFA（64 query 头共享 1 KV，head dim 256）**、48 专家 top-3 + 1 共享。核心是 **AFD（Attention-FFN Disaggregation）**解码成本协同设计（Hopper FP8 解码 4039 tokens/s/GPU）。预训练数据/RL 配方官方未公开。

**dots.llm1（小红书，142B/14B）**
- 主打**完全不用合成数据**：11.2T 全非合成，1:1 中英。MHA(32/32)+QK-Norm，128 路由 + 2 共享 top-6（=8 激活），aux-loss-free + sequence-wise balance。
- **三段式数据 pipeline**：Document Preparation（trafilatura + fastText + MD5 去重）→ Rule-Based（行级去重 + MinHash+LSH 2048 值 128×16）→ Model-Based（1.5B web/clutter/质量三模型 + BGE-M3 语义去重 + 200 类 Category Balancing）。
- **仅 SFT + RFT 无 RL**（~400K 指令，2 epoch + rejection sampling fine-tuning + verifier）。

**Ling/Ring 2.0（蚂蚁 InclusionAI，16B→1T）**
- 统一"高稀疏 + 细粒度"：全系 256 路由 + 1 共享 top-8（≈3.5% 激活）+ MTP；GQA+QKNorm+Partial RoPE（仅前 64 维）；aux-loss-free。
- **全程 FP8 训练**（号称最大全 FP8 开源模型）、2016×Hopper、**Ling Scaling Laws** + **WSM（Warmup-Stable-Merge，用 checkpoint 合并替代 LR 衰减做退火，比 WSD 高 +1~+2 分）**；20T+ token。
- 后训练 DFT→Evo-CoT→GAR；**LPO（句子级 policy 优化）**。
- Ring-1T：首个万亿级开源 thinking 模型（Ling-1T-base + long-CoT SFT 64k + RLVR + 通用 RL）；**IcePop（GRPO 双侧 masking 校准）+ C3PO++ + ASystem 异步框架**。

**Pangu（华为，Ascend NPU 自闭环）**
- Pangu Pro MoE（72B/16B）：**MoGE（分组专家，每组激活相同数量专家实现完美设备负载均衡）**，4K×Ascend NPU，13T 三阶段（general 9.6T → reasoning 3T → annealing 0.4T）。
- Pangu Ultra MoE（718B/39B）：MLA 128 头 + MTP + **DSSN（Depth-Scaled Sandwich-Norm）+ TinyInit + EP-Group 负载均衡损失**；**6K×Ascend NPU，MFU 30.0%**，仿真选 TP=8/PP=16/VPP=2/EP=4；Hierarchical EP All-to-All + Adaptive Pipe Overlap；openPangu ~19T token。

---

## 三、跨家族横向对比（共性与差异）

### 3.1 架构演进的趋同与分叉

**位置编码**：ALiBi（BLOOM）几乎绝迹 → **RoPE 一统天下**；长上下文工程趋同到 **RoPE base 放大（1e4→1e6/1e7/5e7）+ YaRN/DCA/LongRoPE 外推**。Llama4 的 iRoPE（交错 NoPE+RoPE）、Gemma3 的局部层保 10k/全局层提 1M 是少数分叉。

**注意力压缩路线（KV cache 是核心矛盾）**：
- MHA → **GQA**（几乎成默认）→ MHA 时代的 MQA（Falcon-7B/StarCoder/Gemma1-2B）。
- **MLA（潜注意力）**：DeepSeek 发明 → Kimi K2、Pangu Ultra、MiniCPM3、GLM-5、Step-3(MFA 变体) 跟进。
- **混合线性注意力**：MiniMax(lightning 7:1)、Qwen3-Next(Gated DeltaNet 3:1)、MiniCPM-SALA(Lightning 1:3)、Nemotron(Mamba-2 hybrid) —— 都为长上下文/解码成本。
- **稀疏注意力**：DeepSeek DSA（top-k 2048）→ GLM-5 跟进（继续预训练引入，sparse adaptation 仅 20B vs DeepSeek 943.7B）；GLM-5.2 IndexShare（每 4 层复用同 indexer，1M 下每 token FLOPs 降 2.9×）。
- **局/全交替 + SWA**：Gemma2(1:1)/Gemma3(5:1)、OLMo3(每 4 层 3 SWA)、Mistral 7B(纯 SWA)。

**MoE 配方对比（关键分歧点）**：

| 维度 | DeepSeekMoE 系（V3/Kimi/Ling/dots/GLM-4.5） | Qwen3/OLMoE | Mixtral 系 | Gemma/Pangu/Nemotron3 |
|---|---|---|---|---|
| 专家粒度 | 细粒度多专家（256–384 路由） | 细粒度（128/64） | 粗粒度 8 专家 | 64–512 |
| 共享专家 | **有**（1–2 个常激活） | Qwen3/OLMoE **取消**共享 | 无 | Pangu 有 4 / Nemotron3 有 shared |
| 负载均衡 | **无辅助损失（bias 动态调）** | global-batch LB | **有 aux loss 0.001** | MoGE 分组 / EP-Group aux |
| upcycle | 多为 from scratch | Qwen2 upcycle 7B | from scratch | Skywork upcycle / MiniCPM upcycle |
| 特殊 | MTP（V3/Kimi/Ling/GLM/Nemotron3） | — | — | LatentMoE（Nemotron3，latent 维路由） |

> 趋势很明确：**"细粒度多专家 + 共享专家 + 无辅助损失 + MTP"成为新一代万亿 MoE 的事实标准配方**（DeepSeek-V3 定义，Kimi/Ling/GLM-4.5/dots 跟进）；而 Qwen3 和 OLMoE 反其道取消共享专家、改用 global-batch load balancing 促专家特化。Mixtral 是上一代"粗粒度 + 有 aux loss"的代表。

**优化器**：绝大多数仍是 AdamW；**Muon 是新变量**（GLM-4.5/GLM-5、Kimi K2 的 MuonClip）—— 这是 2025 年最显著的优化器分叉。

### 3.2 数据：从"信任语料单 epoch"到"过滤范式 + 退火 + 合成"

**过滤范式迁移**（贯穿全档的主线）：
- 纯启发式（Pile/ROOTS/RefinedWeb/Gopher/C4 规则）→ **基于模型的分类器过滤（fastText/DistilRoberta）成胜负手**。DCLM 是分水岭论文：证明 model-based filtering 是关键，DCLM-Baseline 7B/2.6T → MMLU 64%（开放数据 SOTA，算力少 6.6×）。此后 MAP-Neo/OpenCoder/Llama3/Nemotron/dots/GLM 全用召回式 fastText。

**去重**（web 数据的灵魂，几乎人人用）：**MinHash-LSH（模糊）+ 精确去重（后缀数组/Bloom filter/MD5）**。极致案例：RefinedWeb 移除 90% 文档；DeepSeek 跨 91 个 CC dump 去重率 89.8%。代码侧共识：**file-level 去重 > repo-level**（OpenCoder/StarCoder）。

**合成数据的工业化**（数据质量信仰）：
- Phi 发明"教科书质量"合成 → Nemotron 工业化（340B 对齐 >98% 合成、H 的 1.9T CC 改写）→ Qwen3（三模型合成数万亿）、Kimi K2（知识/数学 chunk-wise 重写）、Hunyuan（1.5T 合成）。
- **反向标杆**：dots.llm1 **完全不用合成数据**（11.2T 全非合成）证明纯真实数据也能到 142B/14B SOTA。

**退火（annealing）/ WSD 的兴起**（2024 起的范式转变）：
- 早期单 epoch + cosine（NeoX/BLOOM/Pythia/LLaMA）→ **多阶段 + 退火段注入高质量数据 + WSD**。
- MiniCPM 系统化提出 **WSD + 退火数据注入**（消融证明退火段加 SFT 数据 >> 只在 SFT 加）；OLMo2/3 的 Dolmino mid-training；Llama3 的 40M token 退火 + Polyak 平均；GLM 的 mid-training；Ling 的 **WSM（用 checkpoint 合并替代 LR 衰减）**。
- **数据-模型比**：MiniCPM 实测 compute-optimal ≈ 192:1（远高于 Chinchilla 20:1），印证"小模型训更多 token"的 Llama 路线。

**配比数字（少数公开精确百分比的）**：Llama3（通用 50%/数学推理 25%/代码 17%/多语 8%）、Nemotron-4 15B（英 70%/多语 15%/代码 15%）、InternLM2（en-web 67.51%/zh-web 18.95%…）、Qwen2.5-Coder（70:20:10）、DeepSeekMath（56% 数学 + 20% GitHub…）。多数大厂（Qwen/DeepSeek/Gemma/Mistral/GLM）只给定性。

### 3.3 训练精度：BF16 → FP8 → NVFP4 的低精度竞赛

- 早期 fp16（NeoX/INCITE/GLM-130B，受 40GB A100 硬件所限）→ A100/H 时代 **BF16**（BLOOM/Falcon/StarCoder/Llama/Qwen/InternLM）。
- **FP8 训练浪潮**：DeepSeek-V3 首次超大模型验证（细粒度量化 + E4M3 + FP32 累加）→ Nemotron-H-56B 首个全 FP8 → Ling（最大全 FP8 开源）、MiniCPM4、Intern-S1、GLM/Kimi 的 FP8 rollout。
- **NVFP4 前沿**：Nemotron 3 全系（E2M1 + 16 micro-block + E4M3 scale + FP32 global，稳到 25T token）—— NVIDIA 在低精度上领跑一代。
- **量化感知训练 QAT**：Gemma3（int4/fp8）、Mistral NeMo（FP8 推理）、MiniCPM BitCPM4（三值）、GLM-5（INT4 QAT bitwise 一致）。

### 3.4 并行与 infra：从 Megatron-DeepSpeed 到自研框架

- 通用底座：3D 并行（TP+PP+DP）+ ZeRO；Megatron(-DeepSpeed) 是最广基础（BLOOM/StarCoder/MAP-Neo/OpenCoder/InternLM/GLM）。
- **自研框架百花齐放**：DeepSeek HAI-LLM（DualPipe + 自研 all-to-all kernel）、Falcon Gigatron（AWS p4d + S3 流式）、InternLM InternEvo、AI2 OLMo-core、GLM slime、Kimi/Ling 改版 Megatron、dots Cybertron、Skywork-Megatron、Qwen3-Max PAI-FlashMoE+ChunkFlow。
- **MoE 专属并行**：EP（专家并行）+ EDP/ETP（Skywork/MiniMax）；DeepSeek-V3 用 64-way EP 无 TP；Pangu Hierarchical EP All-to-All。
- **解码成本协同设计**：Step-3 AFD（attention 与 FFN 部署到不同 GPU）、DeepSeek 预填/解码分离。
- **MFU 参考**：Llama3 43%、InternLM 7B 53–64%、Skywork-MoE 38%、Pangu Ultra 30%、OLMo3 41–43%、BLOOM 50%。

### 3.5 SFT 配方共性

- **数据量两极**：Llama2"少而精"（27,540 条，Quality Is All You Need）vs DeepSeek/InternLM/Qwen2.5 的百万级（1.5M / 10M / >1M）。
- **拒绝采样（rejection sampling）+ execution feedback 成标配**：Llama3/Qwen2.5/Nemotron/GLM/dots 都用 verifier/沙箱筛 SFT 数据。
- **大模型蒸小模型**：Llama2 用 70B 拒绝采样数据微调小模型；R1 蒸 6 个小模型；Gemma/Nemotron 大量 on-policy 蒸馏。
- **loss 聚合**：Tülu/OLMoE 用 sum/token-level loss（优于 mean）；普遍对 prompt token 加 loss mask。
- **两阶段/多阶段 SFT**：OpenCoder（Stage1 多样 → Stage2 高质）、MAP-Neo（Foundational → Chat）、Nemotron（Code SFT → General SFT）、Nano2（三阶段含截断推理实现 thinking budget）。

### 3.6 RL 对齐：从 RLHF-PPO 到 GRPO/RLVR 的范式革命

**算法演进主线**：
- **第一代 RLHF**：双 RM + PPO（Llama2 工业级标杆、InternLM COOL RLHF 条件 RM + 多轮 PPO）。
- **DPO 取代 PPO**：Llama3 弃 PPO 迭代 6 轮 DPO；Mixtral SFT→DPO；MiniCPM/Tülu2/Qwen offline DPO。Llama3 论据：DPO 大模型更省算力、IFEval 更好。
- **GRPO 成新主流**（DeepSeekMath 发明，去 critic 用组内相对优势）：DeepSeek 全系、Qwen3、GLM-4.5/5、OLMo（1B/32B）、Phi-4-reasoning、Nemotron 系、MiniCPM4、Pangu、Hunyuan(改进)、MiniMax(改进)。
- **GRPO 的去 KL 化趋势**：GLM-4.5/GLM-5（去 KL loss）、OLMo3 OlmoRL（去 KL）、Nemotron-Cascade-2（完全去 KL 退化为 REINFORCE）、DAPO/Dr GRPO 系改进。

**RLVR（可验证奖励 RL）范式**（本批最重要的对齐创新）：
- **AI2 Tülu3 首次系统提出 RLVR**（v=验证器，对则 α=10 否则 0），确立 SFT→DPO→RLVR 三段式。
- 此后成行业共识：DeepSeek-R1（纯规则奖励）、Qwen QwQ/Qwen3（verifier）、Kimi K2（可验证 Gym + K8s 沙箱）、Phi-4-reasoning（rule-based length-aware）、MiniCPM4（SymPy+Firejail）、GLM/Ling/Nemotron/Pangu。
- **纯 RL 激发推理**：DeepSeek-R1-Zero 证明绕过 SFT 直接 RL 即可涌现 reasoning（"aha moment"），是范式级发现。
- **MoE 上的 RL 稳定性**是新难题：推理/训练引擎数值差 + FP8 + 动态路由 → token 级裁剪不可靠 → 多家给出方案：Intern-S1 OREAL+KL-Cov、GLM-5 IcePop、Ring-1T IcePop、DeepSeek-V3.2 Keep Routing、Nemotron MOPD。

**Reward 形态对比**：
- 规则/可验证（数学装箱、代码沙箱、IF 约束）—— RLVR 主体。
- model-based RM：Llama2 双 RM、Nemotron 5 维 HelpSteer 回归头、Kimi Self-Critique Rubric、GLM RubriX、Ling Group Arena Reward。
- 防 reward hacking 技巧：DeepSeek model-based 奖励只最后 400 步加；Hunyuan EMA；Kimi prescriptive rubrics；Phi rule-based 避神经 RM。

**RL infra**：解耦 rollout/training（DeepSeek 四模块、GLM slime 双模式、Tülu/OLMo 异步 off-policy + continuous batching）；vLLM/SGLang rollout 几乎人人用；FP8 rollout（GLM/Kimi/Llama-Nemotron 在线 FP8 generation）。

### 3.7 一句话总结各家族"招牌动作"

| 家族 | 招牌配方 |
|---|---|
| DeepSeek | MLA + 无辅损 MoE + MTP + FP8 + DualPipe + GRPO/纯RL + DSA |
| Qwen | 数据规模狂飙(36T) + 模型自过滤/自合成 + DPO→GRPO + hybrid thinking + 强到弱蒸馏 |
| Llama | 纯公开数据 + 工业级双RM-RLHF(L2) → 弃PPO迭代6轮DPO(L3) → 原生多模态MoE+iRoPE(L4) |
| GLM | blank-infilling 起家 + Muon + 降宽增深 MoE + 专家迭代+自蒸馏 + slime + 国产芯片 |
| OLMo/AI2 | 全栈全开标杆 + RLVR 范式发源 + Delta Learning DPO + OlmoRL 4x 提速 |
| Gemma | Gemini 下放 + 知识蒸馏(50× compute-optimal token) + 局/全注意力 + QAT |
| Mistral | 极简报告(只给架构+评测) + SWA + 经典 top-2 MoE + SFT→DPO |
| InternLM | 最透明国产文档 + COOL RLHF 条件RM + InternEvo + 科学多模态 MoR |
| MiniCPM | WSD + µP 风洞 + 退火数据注入 + 192:1 数据模型比 + InfLLM 稀疏 + 端侧 |
| Nemotron+Phi | 合成数据信仰(小模型打大模型) + FP8/NVFP4 领跑 + RPO/MOPD + Pivotal Token DPO |
| 新生代大MoE | 万亿稀疏(Kimi/Ling) + 线性混合(MiniMax) + 无合成(dots) + 国产硬件(Pangu) + MuonClip/WSM/IcePop |

---

## 来源

本章所有数字均出自 `../deep-dive` 下 12 份家族深挖档案：
`fully-open.md`、`deepseek.md`、`qwen.md`、`llama.md`、`glm.md`、`olmo-ai2.md`、`gemma.md`、`mistral.md`、`internlm.md`、`minicpm.md`、`nvidia-phi.md`、`newgen-moe.md`。
各档案内含 arXiv 原文 / 官方技术报告 / 官方 config 的逐条一手出处与本地 PDF 路径。
