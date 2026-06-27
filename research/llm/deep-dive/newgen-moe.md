---
title: 新一代开源大 MoE 训练配方深挖（多方）
type: source
tags: [moe, llm, training-recipe, kimi-k2, minimax, hunyuan, skywork, step, dots-llm1, ling, ring, pangu, deep-dive]
created: 2026-06-18
updated: 2026-06-18
---

# 新一代开源大 MoE 训练配方深挖

> 范围：除 DeepSeek / Qwen / Llama 之外，2024–2026 各家"新生代"开源 / 开放权重大型 MoE。
> 收录：Kimi K2(Moonshot)、MiniMax-01(MiniMax)、Hunyuan-Large(腾讯)、Skywork-MoE(昆仑万维)、Step-3(阶跃)、dots.llm1(小红书 rednote-hilab)、Ling/Ring 2.0(蚂蚁 InclusionAI)、Pangu Pro/Ultra MoE(华为)。
> 所有数字均抠自官方技术报告 PDF / 官方 HF config / 官方 model card；查不到的明确标注"官方未公开"。

---

## 家族演进脉络

- **2024 H1 — 早期 upcycling / 经典 MoE**：Skywork-MoE(146B, 2024-06, 从 Skywork-13B upcycle，16 专家 top-2)，是这批里最早系统讨论"upcycle vs from scratch + gating logit normalization + adaptive aux loss"的报告。
- **2024 H2 — 蒸馏稀疏化、KV 压缩**：Hunyuan-Large(389B/52B, 2024-11) 引入 GQA+CLA 双重 KV 压缩、recycle routing、expert-specific LR；这一代仍以 SFT + DPO 为主，合成数据 1.5T。
- **2025 H1 — 线性 / 混合注意力 + 极致稀疏**：MiniMax-01(456B/45.9B, 2025-01) 用 lightning linear attention(7:1 混合 softmax)冲百万上下文；dots.llm1(142B/14B, 2025-06) 主打"无合成数据 + 三段式数据 pipeline"。
- **2025 H2 — 万亿稀疏 + Muon / FP8 + RLVR**：Kimi K2(1.04T/32B, 2025-07) 用 MuonClip 优化器实现万亿零 loss spike + 大规模 agentic 合成 + RLVR/自评 RL；Ling 2.0(16B→1T, 2025-10) 全程 FP8、Ling Scaling Law、WSM 调度、aux-loss-free + MTP；Step-3(316B/38B, 2025-07) 以 MFA + AFD 主打解码成本。
- **2025 H2 — 国产硬件自闭环**：华为 Pangu Pro MoE(72B/16B, MoGE 分组专家) 与 Pangu Ultra MoE(718B/39B, MLA+MTP+DSSN) 全部在 Ascend NPU 上从零训练；openPangu-Ultra-MoE-718B(2026 开源) ~19T tokens、快慢思考融合。
- **2025 Q4 — 万亿 thinking 模型**：Ring-1T(1T/50B, 蚂蚁) 在 Ling-1T-base 上做 long-CoT SFT + RLVR + 通用 RL（IcePop / C3PO++ / ASystem）。

### 各代关键参数对比（官方数字）

| 模型 | 发布 | 总参/激活 | 层数 | 隐藏维 | 注意力 | 专家(总/共享/激活) | vocab | 上下文 | 预训练 token | 精度 | 优化器 | 算力(芯片) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Skywork-MoE | 2024-06 | 146B / 22B | 52 | 4608 | MHA(36 头) | 16 / 0 / 2(top-2) | 65,536 | 8K | 条件训练(2T 检查点 upcycle) | 官方未公开(bf16+fp32) | Adam系 | 1536× A800 |
| Hunyuan-Large | 2024-11 | 389B / 52B | 64 | 6400 | GQA(80头/8KV)+CLA | 16专+1共享 / 1共享 / 1专(+1共享) | 128K | 256K | 7T(含 1.5T 合成) | 官方未公开 | 官方未公开 | 官方未公开 |
| MiniMax-01 | 2025-01 | 456B / 45.9B | 80 | 6144 | 混合(7 lightning : 1 softmax-GQA) | 32 / 0 / 2(top-2) | 200K | 1M(训练)/4M(外推) | ~11.5T | 官方未明示(MFU基于 H20) | AdamW | 1500–2500× H800 |
| dots.llm1 | 2025-06 | 142B / 14B | 62 | 4096 | MHA(32头/32KV)+QK-Norm | 128 / 2 / 6(+2 共享=8) | 152,064 | 32K | 11.2T(无合成) | 官方未明示 | AdamW | H800(数量未公开) |
| Step-3 | 2025-07 | 316B(LLM)/321B(VLM) / 38B | 61 | 7168 | MFA(64 Q头共享1 KV) | 48 / 1 / 3(top-3) | 128,815 | 64K | 官方未公开 | FP8(推理) | 官方未公开 | Hopper(H800/H20) |
| Kimi K2 | 2025-07 | 1.04T / 32.6B | 61 | 7168 | MLA(64头) | 384 / 1 / 8(top-8) | 163,840 | 128K(YaRN) | 15.5T | BF16(部分 FP8 存储) | MuonClip | H800(数量未公开) |
| Ling-1T | 2025-10 | 1.0T / 51B | 80 | 8192 | GQA+QKNorm+Partial RoPE | 256 / 1 / 8(top-8) | 156K | 128K(YaRN) | 20T+ | 全程 FP8 | AdamW | 2016× Hopper |
| Ring-1T | 2025-10 | 1T / ~50B | 80 | 8192 | (同 Ling-1T-base) | 256 / 1 / 8 | 156K | 长(64K SFT) | 基座=Ling-1T-base | (继承) | (RL) | Ascend(ASystem) |
| Pangu Pro MoE | 2025-06 | 71.99B / 16.5B | 48 | 5120 | GQA(40头/8KV) | 64 / 4 / 8(每组1, MoGE) | 153,376 | 32K | 13T | 官方未明示 | 官方未明示 | 4K× Ascend NPU |
| Pangu Ultra MoE | 2025-05 | 718B / 39B | 61 | 7680 | MLA(128头) | 256 / 1 / 8(top-8) | 官方未公开 | 官方未公开(arxiv) | ~19T(openPangu card) | 官方未明示 | 官方未明示 | 6K× Ascend NPU |

> 注：表内"激活"为每 token 激活参数；Skywork-MoE 22B 激活；MiniMax-01 与 Skywork-MoE 无共享专家。

---

## Kimi K2（Moonshot AI）

**报告**：Kimi K2: Open Agentic Intelligence（arXiv:2507.20534v2, Kimi Team）。1.04T 总参 / 32.6B 激活的超稀疏 MoE，主打 agentic intelligence。

### 架构细节
- 总参 **1.04T**，激活 **32.6B**；**61 层**（其中 dense 层 1 层，first_k_dense_replace=1）。
- 隐藏维 **7168**，MoE 专家中间维 **2048**（dense FFN intermediate 18432）。
- 注意力：**MLA**（沿用 DeepSeek-V3 设计），**64 个注意力头**（DeepSeek-V3 为 128，K2 砍半以降推理开销）；kv_lora_rank=512，q_lora_rank=1536（HF config）。
- MoE：**384 路由专家 / 1 共享专家 / 每 token 激活 8 专家**（sparsity=48=384/8，由 sparsity scaling law 选定；DeepSeek-V3 为 256 专家）；**无 expert grouping**（DeepSeek-V3 有）。
- vocab **163,840**（HF config，DeepSeek-V3 为 129,280）；max_position_embeddings **131,072(128K)**，rope_theta 50000。
- 激活函数 SwiGLU，RMSNorm；注意力稳定性靠 **QK-Clip**（替代 QK-Norm，因 MLA 的 K 不全实例化）。
- **sparsity scaling law**：固定激活参数下，专家越多（稀疏越高）训练/验证 loss 越低；达到 val loss 1.5 时 sparsity 48 相对 sparsity 8/16/32 分别省 1.69×/1.39×/1.15× FLOPs。注意力头数=层数（不再像 DSv3 翻倍），翻倍只带来 0.5–1.2% loss 改善，不值长上下文推理代价。

### 预训练数据
- **15.5T tokens**，四大域：Web Text、Code、Mathematics、Knowledge；多数 pipeline 沿用 Kimi K1.5。
- **合成数据重写（rephrasing）**提升 token 利用率：
  - 知识域：风格/视角多样 prompting（仿 WRAP）+ chunk-wise 自回归重写（保全局连贯）+ fidelity 校验；每个语料最多重写 2 次。实验：原始 wiki 10 epoch=23.76 SimpleQA；重写 1 次×10 epoch=27.39；重写 10 次×1 epoch=28.94。
  - 数学域：高质量数学文档改写成 "learning-note" 风格（仿 SwallowMath）+ 把其他语种数学材料翻译成英文增多样性。

### 训练细节
- 集群：**NVIDIA H800**，每节点 2TB RAM、8 GPU（NVLink/NVSwitch 内连），节点间 8×400 Gbps RoCE。卡数未公开。
- 并行：**PP（虚拟阶段，interleaved 1F1B）+ 16-way EP + ZeRO-1**；BF16 存参 + FP32 梯度累积约 6TB GPU 内存，分布在 256-GPU 模型并行组。EP=16（取最小可行 EP 以保证 1F1B 阶段计算-通信全重叠）。
- 精度：BF16 计算；MoE up-proj 与 SwiGLU 的输入压成 **FP8-E4M3 仅做存储**（不做 FP8 计算，因前期观察到性能下降）；MoE down-proj 重计算省激活。
- 优化器 **MuonClip**（Muon + 权重衰减 + RMS 一致化 + QK-Clip）；**WSD 调度**；context window **4096**。
- LR：前 10T 常数 2e-4（500 步 warmup 后），后 5.5T cosine 2e-4→2e-5；weight decay 0.1 全程；**global batch 67M tokens**。
- 退火 + 长上下文激活：batch 保持 67M，LR 2e-5→7e-6；400B tokens @4k + 60B tokens @32k；再用 **YaRN** 扩到 128k。**全程零 loss spike**。

### SFT
- 用 **Muon 优化器**做 SFT（Muon 预训练的 checkpoint 配 Muon 微调最佳）。
- 大规模指令集，核心两原则：prompt 多样性最大化 + 回复高质量；用 K1.5 与内部专家模型生成候选，LLM/人类评审过滤。
- **大规模 agentic 数据合成 pipeline**：模拟真实工具使用场景，构造多样工具/智能体/任务/轨迹，rubric-based 任务生成 + LLM judge 按 rubric 过滤，生成数万条高保真可验证 agentic 交互。

### RL / 对齐
- **RL 算法**：沿用 K1.5 的策略优化目标（对每个问题采 K 个回复，按 `r(x,yi)−r̄(x) − τ·log(πθ/πold)²` 优化，τ>0 正则；用 Muon 优化）。
- **可验证奖励 Gym（RLVR）**：数学/代码/STEM 等可验证任务；Coding/SWE 用 Kubernetes 沙箱（>10,000 并发）。
- **Self-Critique Rubric Reward**：K2 actor 生成、K2 critic 按 core rubrics + prescriptive rubrics（防 reward hacking）+ 人工 rubrics 做成对比较；critic 用 RLVR on-policy rollout 持续刷新（闭环把客观信号蒸进评判模型）。
- 额外机制：**Budget Control**（按任务类型设 per-sample 最大 token 预算，超出截断+惩罚）；**PTX Loss**（混入高质量精选数据防遗忘）；**Temperature Decay**（先高温探索后低温收敛）。
- RL infra：训练/推理引擎 **colocated** 同卡，互相 offload；全集群广播参数。

---

## MiniMax-01 / MiniMax-Text-01（MiniMax）

**报告**：MiniMax-01: Scaling Foundation Models with Lightning Attention（MiniMax）。混合 lightning(线性)注意力 + MoE，冲百万级上下文。

### 架构细节
- 总参 **456B**，激活 **45.9B**，**32 个专家，top-2 路由**（无共享专家），专家 FFN 中间维 **9216**。
- **80 层**；隐藏维 **6144**。每个注意力模块 **64 头，head dim 128**。
- **混合注意力**：每 7 个 lightning attention（线性，transnormer 块）block 后接 1 个 softmax attention block（softmax 层用 **GQA，group size 8**）。RoPE 仅作用于一半 head 维，base 频率 10,000。
- norm：**RMSNorm + DeepNorm**；MoE 取代 FFN 作为 feature-mixer。
- vocab **200K**（byte-level BPE）。上下文：训练可达 **1M**，推理外推 **4M**（NIAH 测试，仅训到 1M）。
- 用于质量打分的"上一代"reward labeler 本身是 5B 激活/60B 总参的 MoE。

### 预训练数据 / 处理
- 语料：学术文献、书籍、网页、代码；rule-based 清洗 + 去重（对齐 RefinedWeb/FineWeb/Gopher 实践）。
- **质量增强**：用上一代模型当 reward labeler 评多维度（连贯/简洁/教育价值/有用/知识丰富/类别相关），最终聚焦三维：**知识深度、实用有用性、类别分布**。
- 格式：不重格式化（重 Markdown 反降多样性），用嵌套文档模板做对话/QA。
- 数据混合：从均匀分布起步，再加权偏向高质内容但保类别覆盖；完全剔除低分内容反而损下游。
- tokenization：byte-level BPE，上采样多语；vocab 200K。

### 数据配比 / 阶段
- 长上下文三阶段（Table 6）：128K 阶段（RoPE base 5M, 300B tokens, Short 30%/Medium 70%/Long 0%）→ 512K（RoPE 10M, 32B, 35/35/30）→ 1M（RoPE 10M, 26B, 30/30/40）；各阶段末 20% 混 10% 高质量长上下文 QA。

### 训练细节
- 集群：动态变化的 **1500–2500 × H800**；MFU 端到端在 NVIDIA H20 上测。
- 并行：MoE all-to-all 用 **EP + ETP（Expert Tensor Parallel）**；提出 **EDP（Expert Data Parallel）**；长上下文用 **varlen ring attention + LASP+（Linear Attention Sequence Parallelism 增强版）+ data-packing**。
- 优化器 **Adam**；warmup 500 步到峰值 **2e-4**；**7.2T tokens 常数 LR** → 因异常梯度调到 1.3e-4 训剩 **3.2T** → fast decay 阶段训 **1T** 指数降到 3e-5（总 ≈11.5T）。
- batch：critical batch size 动态翻倍（按 loss-cbs 幂律），从初期到 4.7T 处达 **128M tokens**。MoE 辅助 loss 系数 0.01。

### SFT
- 见 §5.3（报告未给具体条数）；多 capability 覆盖；post-training RoPE base 全程保持 **10M**。

### RL / 对齐（多阶段）
- **Reward Model** 四维度评估。
- **Offline RL = DPO**：用 SFT 同分布 prompt，多温度采样后用 RM 选最优/最差构造偏好对。
- **Online RL = 改进版 GRPO**：偏好中等成功率 prompt、用 SFT-未训 prompt；三创新——重要性采样权重双侧裁剪、KL 散度重构（stop-gradient 形式降方差）、平衡优势估计。
- 后训练 5 阶段（Table 7）：Stage III 短上下文 DPO(8192) → Stage IV 长上下文 DPO(1,032,192 序列) → Stage V 短上下文 Online RL。安全用专门的 harmless reward model。

### AI infra
- 自研训练/推理框架；lightning attention 推理专用 CUDA kernel（>75% 利用率级别优化）；动态 H800 集群。

---

## Hunyuan-Large（腾讯）

**报告**：Hunyuan-Large: An Open-Source MoE Model with 52 Billion Activated Parameters by Tencent。389B/52B，支持 256K。

### 架构细节（Table 1）
- 总参 **389B**，激活 **52B**；**64 层**；隐藏维 **6400**；激活 SwiGLU；vocab **128K**。
- 注意力头 **80**，KV 头 **8**（**GQA**）；**KV 压缩双管齐下**：GQA(8 组) + **CLA（Cross-Layer Attention，每 2 层共享 KV cache）**，相比 MHA 省近 **95% KV cache**。
- MoE：**1 共享专家 + 16 specialized 专家**，每 token 激活 1 共享 + 1 specialized。RoPE 位置编码。
- tokenizer：128K（100K 来自 tiktoken + 自建），比 LLama3.1 tokenizer 压缩率更优。

### 预训练数据
- 共 **7T tokens**，含近 **1.5T 高质量合成数据**（"orders larger than"前作）。
- 合成数据 4 步：指令生成 → 指令演化 → 回复生成 → **Step 4 回复过滤（critique 模型）**。

### 训练细节
- **MoE 缩放定律**：用 critical batch size Bcrit(L) + isoFLOPs 拟合最优激活参数与 token 量，得出 389B 激活/7T tokens 的最优配置。
- LR 调度三段：warmup → 长缓降 → 末 5% **annealing**。
- **Recycle Routing**：top-k 容量溢出被丢的 token 不丢弃，回收重路由。
- **Expert-Specific LR Scaling**：共享/specialized 专家有不同 effective batch size，故对 specialized 专家 LR 做缩放（按 effective batch 除以激活比例修正）。
- **长上下文预训练**：annealing 后两段 32K→256K，各约 **10B tokens**；256K 阶段 **RoPE base 频率放大到 1 billion**；语料 25% 自然长文本(书/代码) + 75% 常规。
- 算力（GPU 型号/卡数/框架）：**官方未公开**（本报告未披露）。

### SFT
- SFT 数据 **>100 万条**，覆盖数学/代码/逻辑/QA/agent/写作/角色扮演/长文等。
- 处理：指令抽取（专门抽取模型）→ 指令泛化（简↔难映射）→ 指令平衡（多维标签，>1000 万条指令）→ 质量控制（rule-based + 基于 70B dense 的 critique 四级打分 + 人工）。
- 训练：**3 epoch**，LR 2e-5→2e-6；attention dropout 0.1、hidden dropout 0.2（MoE 比 dense 更受益于 dropout）。

### RL / 对齐
- **DPO（单阶段，offline+online 一体）**：预编译偏好集 + 当前 policy 多采样后 RM 选最优/最差。
- 稳定性：chosen response 上加 **SFT loss 项**；用 **EMA** 防 reward hacking、减 alignment tax。

---

## Skywork-MoE（昆仑万维 / Kunlun）

**报告**：Skywork-MoE: A Deep Dive into Training Techniques for Mixture-of-Experts Language Models（arXiv:2406.06563）。146B/22B，从 Skywork-13B **upcycle**。

### 架构细节（Table 2）
- 总参 **146B**，激活 **22B**；从 Skywork-13B dense **upcycle**，Llama-like（RoPE + RMSNorm + SwiGLU）。
- vocab **65,536**；隐藏维 **4608**；FFN 维 **12288**；head dim 128；**36 头**；**52 层**；**16 总专家 / 2 路由(top-2)**；MoE layer frequency 1；native 序列长 **8192**。

### 训练 / 数据
- 语料：SkyPile 的 **condensed 子集**；最终模型训了 **3.2T tokens**（in-house 版本）。
- **upcycle vs from scratch**：决策应同时考虑现有 dense checkpoint 性能与 MoE 训练预算；100B 预算下 from scratch ≈ upcycle-100B；300B 预算下结论随终端 LR 变化。
- 两大创新：
  - **Gating Logit Normalization**：对 gating logits 归一化（控制 std，由 λ 调），提升专家多样化。
  - **Adaptive Auxiliary Loss Coefficients**：逐层自适应调辅助 loss 系数。
- **Expert LR scaling**（负面结果探讨）：MoE 层有效 batch 比名义小 k/n 倍，理论应按 √(k/n) 缩放（如 32 专家 top-2 时 ×0.25）；试了 baseline 6e-3 / Expert lr×0.25(MoE 1.5e-3, 非 MoE 6e-3) / global×0.25 三档。

### AI infra
- 自研 **Skywork-Megatron**（基于 Megatron-LM 23.06 分支）；自研 **EDP（Expert Data Parallel，SizeEP=SizeTP）**；非均匀 PP 切分（[5,5,5,5,4] 比 [6,6,6,6] 省 ~10% bubble）；逐阶段差异化梯度重计算。
- 集群：**192 节点 × 8 = 1536 × A800-80G SXM**，节点内 400 GB/s NVLink、节点间 800 Gb/s RoCE；**12-way PP + 4-way tensor-expert(EDP) + 32-way DP + ZeRO-1**；**MFU 38%**，690 tokens/GPU/s。

---

## Step-3（阶跃星辰 StepFun）

**报告**：Step-3: Model-system Co-design for Cost-effective Decoding（StepFun）。316B(LLM)/321B(VLM)，38B 激活；重点是 **MFA + AFD** 解码成本协同设计（预训练数据细节披露很少）。

### 架构细节（Table 1 + 官方 HF config）
- 总参 **316B(LLM) / 321B(含 5B 视觉编码器, VLM)**，激活 **38B/token**。**61 层**；隐藏维 **7168**。
- 注意力 **MFA（Multi-Matrix Factorization Attention）**：**64 个 query 头共享 1 个 K、1 个 V 头**（HF config: num_attention_groups=1），**head dim 256**；Query 从 7168 下投影到低秩 **2048** 再归一化后上投影到 64×256。号称 attention effective rank 最高（与 DSv3 同级）。
- MoE：HF config 显示 **48 routed experts / top-3 / 1 共享专家**，moe_intermediate_size **5120**；MoE 层用于除前 4 层和最后 1 层外的所有 FFN。
- vocab **128,815**；max_seq **65,536(64K)**；rope_theta **500000**（均 HF config）。激活/norm：报告未细述（HF: Step3TextForCausalLM）。

### 预训练 / 数据 / RL
- **官方未公开**预训练 token 数、数据配比、SFT / RL 配方（本报告聚焦推理系统；阶跃称后续再放模型侧细节）。

### AI infra（核心贡献）
- **AFD（Attention-FFN Disaggregation）**：把 attention 层与 FFN 层部署到不同 GPU 集合，各用最适并行（attention 实例可随上下文长度弹性扩缩，FFN 独立保持高 MFU），层间高速网络传 hidden state，形成紧耦合流水线（基于 Prefill-Decoding 解耦思想）。
- Hopper 上 4K 上下文、FP8、无 MTP 时解码吞吐达 **4039 tokens/s/GPU**（50ms TPOT SLA）；可跨 H800/H20/A800/Ascend 910B 混部搜索最佳部署；支持 MTP 进一步加速（attention 效率可翻倍）。
- 量化：FP8 解码；讨论 KV 量化 + MTP 的取舍。

---

## dots.llm1（小红书 rednote-hilab）

**报告**：dots.llm1 Technical Report（rednote-hilab）。142B/14B，主打**完全不用合成数据**的预训练 + 三段式数据 pipeline + 每 1T tokens 开源中间 checkpoint。

### 架构细节（Table，对比 DeepSeek-V3）
- 总参 **142B**，激活 **14B**；**62 层**（第 1 层 dense FFN，其余 MoE）；隐藏维 **4096**；FFN 维 **10944**；MoE FFN 维 **1408**。
- 注意力 **vanilla MHA（32 头 / 32 KV 头）+ QK-Norm**（对 Q/K 投影做 RMSNorm 防 logits 爆炸）；有 attention bias=No；vocab **152,064**；RoPE。
- MoE：**128 路由专家 + 2 共享专家**，每 token top-6 路由 + 2 共享 = **8 激活专家**；专家是细粒度两层 FFN+SwiGLU；**gating 用 FP32** 算（非 BF16）保数值稳定。
- 负载均衡：**aux-loss-free（每专家 bias 动态调，DeepSeek 风格）+ sequence-wise balance loss**；训练全程不丢 token。
- init std 0.006；序列长预训 **8192**。

### 预训练数据（无合成）
- **11.2T tokens，全部非合成**；预训练 1:1 中英平衡。
- **三段式数据 pipeline**（Appendix C）：
  1. **Document Preparation**：URL 过滤（毒性域名黑名单+人工核验）→ trafilatura 正文抽取（自定义 HTML/关键词/长度优化）→ fastText(CCNet) 语言识别（置信<0.65 丢弃）→ MD5 精确去重（去标点+NFD+小写+去多余空格）。
  2. **Rule-Based**：行级跨文档去重（首尾各 5 行，频次>200 只留前 200）→ RefinedWeb/Gopher 风格启发式过滤（空内容/广告/注册提示/meta/wiki-code diff/结构异常/质量；前 1000 站点占 60% 流量做人工定制清洗）→ **MinHash+LSH 模糊去重**（Jieba 分词 5-gram，2048 MinHash 值、128 band×16 row，Jaccard 80% 阈值，碰撞概率 97.42%）。
  3. **Model-Based**：1.5B web-type 分类模型（只留 text-rich detail 页）→ 1.5B web clutter removal（逐行打 0-1 分）→ 1.5B 质量模型（k-fold + AUC 选阈值）→ **语义去重（BGE-M3 嵌入 + KMeans + 簇内 cosine, 阈值 0.95）→ Category Balancing（200 类分类器，上采知识/事实、下采小说/商品描述）**。

### 数据配比 / 阶段
- 主训 11.2T @8K → **两段 annealing 共 1.2T tokens**（显著上采推理/知识数据）→ **长上下文扩展 128B tokens（UtK 策略，文档分块，无需改数据集），8K→32K**，常数 LR。
- batch ramp：64M → 90M(?报告写 8.3T 处再增) → 96M tokens。

### 训练细节
- 框架自研 **Cybertron（基于 Megatron-Core）**；**interleaved 1F1B all-to-all 通信-计算重叠**（warmup 加一步，无额外 bubble/激活内存，与 NVIDIA 合作并入 Megatron-Core）；H800 上对比 Transformer Engine 2.1 的 grouped GEMM 有提升。
- 超参（Table）：WSD 调度；warmup 4000 步；峰值 LR **3.0e-4**；AdamW(β1 0.9, β2 0.95)；weight decay 0.1；init std 0.006。

### SFT（无 RL）
- **~400K 指令实例**（开源+内部标注），多语多轮/知识 QA/复杂指令/数学代码；少量低质开源回复用 DeepSeek-V3-0324 teacher 精修。
- 两阶段：① 对 400K 上采样 + 多 session 拼接，**2 epoch**；② 数学/代码做 **rejection sampling fine-tuning(RFT) + verifier**。cosine LR 5e-6→1e-6。
- **本报告未做 RL 阶段**（仅 SFT + RFT）。

---

## Ling 2.0 / Ling-1T（蚂蚁 InclusionAI）

**报告**：Ling 2.0 Technical Report — Every Activation Boosted（arXiv:2510.22115v2, Ling Team / Inclusion AI）。统一 MoE 范式从 16B→1T（Ling-mini-2.0 16B / Ling-flash-2.0 103B / Ling-1T 1000B），non-thinking instruct 系列；Ring 系列在同基座上做 thinking。

### 架构细节（Table 1）
- 统一"高稀疏 + 细粒度"：**全系列 256 路由专家 + 1 共享专家，每 token 激活 8 专家**（≈3.5% 激活率）。MTP depth 1，MTP loss 权重 0.1。
- 注意力 **GQA（8/16/32 KV 头按规模）+ QKNorm + Partial RoPE（仅前 64 维加旋转）**；attention head dim 固定 128；SwiGLU + RMSNorm pre-norm。
- vocab **156K**（BBPE，从 Ling 1.5 的 128K 扩到 156K，加约 2TB 多语数据）。
- 负载均衡 **aux-loss-free**（bias 中心化于 0，`bi = bi + u·sign(ei) − mean(sign(e))`）+ router gate scaling=2.5 + dropless routing + group routing。
- 三档配置：
  | | Ling-mini | Ling-flash | Ling-1T |
  |---|---|---|---|
  | 层数 | 20 | 32 | 80 |
  | 注意力头 | 16 | 32 | 64 |
  | dense 层 | 1 | 1 | 4 |
  | 隐藏维 | 2048 | 4096 | 8192 |
  | 中间维 | 5120 | 9216 | 18432 |
  | 专家中间维 | 512 | 1024 | 2048 |
  | 总参 (B) | 16 | 103 | 1000 |
  | 激活 (B) | 1.4 | 6.1 | 51.0 |
  | LR | 3.36e-4 | 2.61e-4 | 1.86e-4 |
  | batch | 4400 | 8352 | 18144 |

### 预训练数据 / 配比
- **20T+ tokens**；推理导向语料（Ling Math / Ling Code 等高质子集，带来 5-8% 推理 benchmark 提升）。
- 自建 web data 实测优于 nemotron-cc、TxT360（同条件 MMLU 等更高）。

### 训练细节
- **Ling Scaling Laws**：近千次实验（compute ≤3e20 FLOPs）拟合最优 LR/batch 幂律；固定 64 专家(4 活)+1 共享做超参搜索；只用 1% full compute 验证新想法。
- **WSM（Warmup-Stable-Merge）调度**：linear warmup 2000 步到峰值 → 常数 LR 到底 → **用 checkpoint 合并替代 LR 衰减做"退火"**（比 WSD 平均高 +1~+2 分，无需预定衰减策略）。
- 多阶段：① 通用预训练 4K context 前 20T tokens；② mid-training 扩到 32K（前 150B tokens 含 20% 32K 数据）再 **YaRN 扩到 128K**；mid-training 后 600B tokens 提前注入推理/CoT 数据"预激活"。
- bias-update γ：预训 0.001，context 扩展后 0.0001；AdamW(β1 0.9 β2 0.95, wd 0.1, grad clip 1.0)；batch ramp 前 ~500B tokens。
- **全程 FP8 训练**（号称最大全 FP8 开源模型）：细粒度量化（激活/梯度 [1,128]、权重 [128,128]）；2016 × Hopper GPU；改版 Megatron 0.11 + MTP 支持 + 细粒度异构 PP。

### 后训练（DFT → Evo-CoT → GAR）
- **Stage 1 DFT（Decoupled Fine-Tuning）**：双系统 prompt——Instant Response(think off) 与 In-Depth Reasoning(think on, `<think>...</think><answer>...</answer>`)，建立专用深推理模式；SFT 数据三类（Reasoning / General / Industrial 金融医疗供应链）；用 **ApexEval** 选 RL 起点 checkpoint。
- **Stage 2 Evo-CoT（Evolutionary RL）**：从 DFT instant 模式起步演化推理深度；目标 `arg max E[J(R(x,y),θ)] − β·KL(πθ‖πref)`。
- **LPO（Linguistic-unit / Sentence-level Policy Optimization）**：以句子(detokenize 后标点切)为策略单元的 policy gradient，比 token 级更平滑、收敛更快（AIME2025 更高）。
- **Stage 3 GAR（Group Arena Reward）**：组内成对比较的人类偏好对齐 + **RubriX**（rubric 评分），高并发奖励服务（40K+ 并发）。

---

## Ring-1T（蚂蚁 InclusionAI）

**报告**：Ring-1T Technical Report — ... Learning for Trillion-Scale Thinking Model（Ling Team）。首个万亿级开源 thinking 模型，1T 总参 / ~50B 激活，**建立在 Ling 2.0 架构、从 Ling-1T-base 训练**。

### 架构 / 基座
- 架构同 **Ling-1T-base**（80 层 / 8192 隐藏维 / 256 专家+1 共享 top-8 / GQA+QKNorm+Partial RoPE / MTP）；1T 总参、~50B 激活。
- IMO-2025 评测（AWorld）拿到银牌级（正确解题）。

### 训练流程（三阶段）
- **Long-CoT SFT**：在 Ling-1T-base 上做长链思维 SFT，数据 pack 成 **64k 长度**，多领域推理轨迹，给 RL 打底。
- **Reasoning RL（RLVR）**：数学/代码/科学/逻辑可验证任务；采样大量推理轨迹用可验证奖励（多领域 verifier）精炼策略。
- **General RL**：可验证任务大规模 RL 后，做通用 RL（含 IFEval/AutoIF/WMT 等数据集，RLVR-IFEval）。

### RL 算法创新
- **IcePop**：GRPO 变体，**双侧 masking 校准**——只更新 train/infer 概率比落在 [α,β] 区间的 token，超出区间的"噪声梯度"全丢弃（解决 MoE RL 训练-推理不一致导致的灾难性失配）；目标含 `clip(ri,t, 1−ε, 1+ε)·Âi,t − γ·DKL(πθ‖πref)`。
- **C3PO++**：预算控制的 rollout 调度，动态切分 rollout，消除 rollout 长尾，提升资源利用率。
- **ASystem**：为万亿级 RL 设计的高性能分布式 RL 框架（含 AReaL/AState/ARollout/AData 等组件，全异步、多阶段 masking 加速）。

---

## Pangu Pro MoE（华为，72B/16B，MoGE）

**报告**：Pangu Pro MoE: Mixture of Grouped Experts for Efficient Sparsity on Ascend NPUs。72B 总参 / 16.5B 激活，核心是 **MoGE（分组专家）**为 Ascend 硬件做设备级负载均衡。

### 架构细节（Table 1）
- 总参 **71.99B**，激活 **16.5B**；**48 层**；隐藏维 **5120**；中间维 1344；head size 128。
- 注意力 **GQA：40 query 头 / 8 KV 头**。
- **MoGE（Mixture of Grouped Experts）**：64 路由专家分成 M 个等大组，**每组激活相同数量专家**（每 token 共激活 8 路由 + 4 共享）——全局 softmax 算分后在每组内 top-K′ 选，未选置零；组按 device 分布以实现完美设备负载均衡。**Routed 64 / Activated 8 / Shared 4**。
- vocab **153,376**（domain-aware 词表策略）。

### 预训练数据 / 配比
- **13T tokens**；来源：网页/书籍/多语/代码/STEM/工业域/推理/合成。
- **三阶段（认知发展论）**：① general 阶段 **9.6T**（4K 序列，含大量工业域数据）；② reasoning 阶段 **3T**（32K 序列，大增 STEM/代码/内部数据，合成长短 CoT）；③ annealing 阶段 **0.4T**（指令风格数据增到 ~20%，curriculum 采样，高级 STEM 占 18%；用 7B proxy 做数据消融）。
- 数据评估：domain-aware 模型评估（微调 Pangu 系列当各域 evaluator，胜过单一评估器）。

### 训练细节
- LR 三段：general 3e-4→3e-5（batch 4M tokens）→ reasoning 3e-5→1e-5（batch 增到 16M）→ annealing 1e-5→1e-7（batch 16M）。
- 算力：**4K × Ascend NPU**（300I Duo / 800I A2 平台）；为流水线插 2 个 no-op 层使总层数变 50。
- 推理：MulAttention + SwiftGMM kernel；1148 tokens/s/卡（800I A2），加 speculative/MTP 到 **1528 tokens/s/卡**。

### 后训练
- **SFT**：reasoning : non-reasoning = **3:1**；用同一 SFT 训练轨迹的同质中间 checkpoint 分组(按 epoch)做加权合并。
- **RL = GRPO** + 多源奖励：correctness（数学混合判分、代码在线解释器跑测试用例，stage/continuous reward）+ preference（LLM-as-judge RM）+ auxiliary（format validator）；按 pass rate/loss 做难度采样，缓解 GRPO 全相同奖励退化为 behavior cloning 问题。

---

## Pangu Ultra MoE（华为，718B/39B，MLA+MTP+DSSN）

**报告**：Pangu Ultra MoE: How to Train Your Big MoE on Ascend NPUs（arXiv）。+ openPangu-Ultra-MoE-718B 官方 model card（2026 开源）。718B 总参 / 39B 激活，全程 Ascend NPU 从零训练。

### 架构细节
- 总参 **718B**，激活 **39B**（arxiv 对比表确认 39B）。
- 经系统仿真选定 "模型 7"：**61 层**、**隐藏维 7680**、**256 路由专家**（512 收益饱和故选 256；64/128 loss 更高）、**每 token 激活 8 专家 + 1 共享专家**（有共享专家 loss 更低）；专家(共享+路由)中间维 **2048**。
- 注意力 **MLA，128 头**；**MTP 层**（可把总层 61→64 算入流水线 bubble 优化）。
- 特有设计（model card）：**Depth-Scaled Sandwich-Norm（DSSN）+ TinyInit**（调层归一化结构与初始化提稳定性）；**EP-Group 负载均衡损失**（在 EP-group 级算 aux loss，α=1e-2 最有效；优于 micro-batch 级与 DP-group 级）。
- vocab：arxiv **官方未公开**；上下文长度 arxiv **官方未明示**。

### 预训练数据
- arxiv 报告聚焦 Ascend 系统，预训练数据/配比披露少；**openPangu model card：约 19T tokens**，具备"快慢思考融合"能力。

### 训练细节 / infra（核心贡献）
- 算力：**6K × Ascend NPU**，**MFU 30.0%**、TPS 1.46M（基线 4K NPU 时 MFU 18.9% / TPS 0.61M）；性能对标 DeepSeek R1。
- 仿真选定并行：**TP=8, PP=16, VPP=2, EP=4, MBS=2**。
- 系统优化：**Hierarchical EP All-to-All**（分离机内/机间通信优化带宽）、**Adaptive Pipe Overlap**（细粒度通信-计算重叠）、动态设备级负载均衡（实时专家负载预测 + 自适应专家放置）。
- openPangu 推理部署：Atlas 800T A2(64GB, ≥32 卡)，CANN 8.1.RC1，torch-npu 2.1.0。

### 后训练
- arxiv 未细述 SFT/RL；openPangu card 给出慢思考评测（C-Eval 91.06、AIME25 75.21、MATH-500 97.40、LiveCodeBench 61.14），但具体 SFT/RL 配方**官方未公开**。

---

## 来源（一手官方）

### 已下载本地文件（PDF / config / model card）
- Kimi K2: `../../../sources/llm/2025/kimi-k2.pdf` (arXiv:2507.20534v2)；HF config `/tmp/moe-txt/k2-config.json`（moonshotai/Kimi-K2-Instruct）
- MiniMax-01: `../../../sources/llm/2025/minimax-01.pdf`
- Hunyuan-Large: `../../../sources/llm/2024/hunyuan-large.pdf`
- Skywork-MoE: `../../../sources/llm/2024/skywork-moe.pdf` (arXiv:2406.06563)
- Step-3: `../../../sources/llm/2025/step-3.pdf`；HF config `/tmp/moe-txt/step3-config.json`（stepfun-ai/step3）
- dots.llm1: `../../../sources/llm/2025/dots-llm1.pdf`
- Ling 2.0: `../../../sources/llm/2025/ling-2.0.pdf` (arXiv:2510.22115v2)
- Ring-1T: `../../../sources/llm/2025/ring-1t.pdf`
- Pangu Pro MoE: `../../../sources/llm/2025/pangu-pro-moe.pdf`
- Pangu Ultra MoE: `../../../sources/llm/2025/pangu-ultra-moe.pdf`
- openPangu-Ultra-MoE-718B model card: `../../../sources/llm/2026/openpangu-ultra-moe-718b-modelcard.md`

### 官方 URL
- Kimi K2: https://arxiv.org/abs/2507.20534 ；https://huggingface.co/moonshotai/Kimi-K2-Instruct
- MiniMax-01: https://github.com/MiniMax-AI （MiniMax-01 报告 PDF）
- Hunyuan-Large: 腾讯混元官方报告（Tencent）；https://huggingface.co/tencent/Tencent-Hunyuan-Large
- Skywork-MoE: https://arxiv.org/abs/2406.06563
- Step-3: StepFun 官方报告；https://huggingface.co/stepfun-ai/step3
- dots.llm1: rednote-hilab 官方报告；https://huggingface.co/rednote-hilab/dots.llm1.inst
- Ling 2.0: https://arxiv.org/abs/2510.22115 ；https://github.com/inclusionAI/Ling-V2 ；https://huggingface.co/collections/inclusionAI/ling-v2
- Ring-1T: https://huggingface.co/inclusionAI/Ring-1T ；https://github.com/inclusionAI/AWorld
- Pangu Pro MoE: https://gitcode.com/ascend-tribe/pangu-pro-moe
- Pangu Ultra MoE: 华为 Ascend 官方报告（arXiv）；openPangu 开源页

> 说明：本档所有架构/训练数字均来自上述 PDF 正文表格与官方 HF config/model card。第三方解读、评测聚合站一律未采用。

## 增量补录（2026-06+，初版调研后）
- **Kimi K2.6**（月之暗面）— 1T MoE / 32B 激活，384 专家+1 共享(8/tok)，MLA，61 层，256K；原生多模态 agentic，**agent swarm 300 子 agent / 4000 步**协同。另有 K2.7-Code。详见 [[llm/2026/kimi-k2.6|2026/kimi-k2.6.md]]。
- **MiniMax-M3** — ~428B / ~23B 激活，60 层，64 头 / 4 KV，**1M 上下文**，**MiniMax Sparse Attention**（vs M2：prefill 9×、decode 15× @1M，per-token 算力 1/20，arXiv 2606.13392）。详见 [[llm/2026/minimax-m3|2026/minimax-m3.md]]。
