# DeepSeek（深度求索）开源大模型【训练配方】深挖档案

> 全部数字均来自官方一手来源（arXiv 原文、官方 technical report、官方 model card / 博客 / GitHub）。
> 凡官方未公开或本地原文未提及者，明确标注「官方未公开」。
> 本地原文路径见每个小节末尾「来源」。本档案为列表式，逐型号一个 `##` 小节。

---

## 家族演进脉络

DeepSeek-AI（幻方量化旗下）走的是一条「**先用 scaling laws 立项 → 用 MoE 降本 → 用 MLA 降 KV cache → 用 FP8 + DualPipe 极致压成本 → 用 GRPO/纯 RL 激发推理 → 用稀疏注意力 DSA 压长上下文成本**」的路线。

- **2024-01 DeepSeek-LLM（7B/67B 稠密）**：用自研 scaling laws 立项，2T 双语 token，HAI-LLM 框架，SFT+DPO。奠定数据 pipeline（去重/过滤/remix）与 100K BBPE tokenizer。
- **2024-01 DeepSeekMoE（2B/16B/145B）**：提出**细粒度专家切分 + 共享专家隔离**两大 MoE 创新，是后续所有 V2/V3 的 MoE 基座。
- **2024-01 DeepSeek-Coder（1.3B/6.7B/33B）**：仓库级代码语料 + FIM + 拓扑依赖排序，87 种语言，2T token。
- **2024-02 DeepSeekMath（7B）**：从 Coder-v1.5 续训 120B 数学 token；首次提出 **GRPO**（去掉 critic，组内相对优势），是 DeepSeek 全部 RL 的算法基石。
- **2024-05 DeepSeek-V2（236B/21B MoE）**：首次引入 **MLA（多头潜在注意力）**，KV cache 降 93.3%，训练降本 42.5%；8.1T token；GRPO 两阶段 RL。另发 V2-Lite（15.7B/2.4B）。
- **2024-06 DeepSeek-Coder-V2（16B/236B MoE）**：从 V2 中间 checkpoint 续训 6T，代码语言 86→338 种，上下文 16K→128K。
- **2024-12 DeepSeek-V3（671B/37B MoE）**：**无辅助损失负载均衡 + MTP（多 token 预测）+ FP8 训练 + DualPipe**；14.8T token；全程仅 2.788M H800 卡时（≈557.6 万美元）；后训练从 R1 蒸馏推理。
- **2025-01 DeepSeek-R1 / R1-Zero（基于 V3-Base）**：**纯 RL（无 SFT 冷启动）即可激发推理（R1-Zero）**；R1 用「冷启动 SFT → 推理 RL → 拒绝采样 SFT(800K) → 全场景 RL」多阶段；蒸馏出 6 个 Qwen/Llama 小模型。
- **2025-04 DeepSeek-Prover-V2（671B/7B）**：Lean 4 形式化证明，子目标分解递归求证 + GRPO。
- **2025-05 R1-0528 / 2025-03 V3-0324**：迭代更新版（官方博客）。
- **2025-08 DeepSeek-V3.1（671B/37B）**：在 V3 base 上**两阶段长上下文续训共 840B token**（32K 阶段 630B + 128K 阶段 209B），**混合推理（Think/Non-Think 一模两用）**，UE8M0 FP8 scale 格式。后续有 V3.1-Terminus。
- **2025-09 DeepSeek-V3.2-Exp**：在 V3.1-Terminus 上引入 **DSA（DeepSeek 稀疏注意力）**，长上下文 O(L²)→O(Lk)，API 降价 50%+。
- **2025-12 DeepSeek-V3.2（正式版）**：DSA 架构同 Exp；可扩展 RL（后训练算力 >10% 预训练）+ 大规模 agentic 任务合成；另发高算力变体 V3.2-Speciale（IMO/IOI 金牌级）。

> 注：DeepSeek-V4（2026-04 预览）与 DeepSeek-OCR 等不在本次目标范围（V4 报告/OCR PDF 已在 2026/ 目录，但本档案聚焦语言模型主线 LLM/MoE/V2/V3/R1/Coder/Math/Prover/V3.1/V3.2）。

---

## 各代关键参数对比（官方原文数字）

| 型号 | 总参/激活参 | 层数 | 隐藏维 | 注意力 | MoE(共享+路由/激活) | 训练token | 上下文 | tokenizer/vocab | 关键创新 |
|---|---|---|---|---|---|---|---|---|---|
| DeepSeek-LLM 7B | 6.9B 稠密 | 30 | 4096 | MHA 32头 | — | 2.0T | 4K | BBPE 100K(配置102400) | 多步LR、scaling laws |
| DeepSeek-LLM 67B | 67B 稠密 | 95 | 8192 | GQA 64头/8KV | — | 2.0T | 4K | BBPE 100K | 深而非宽、GQA |
| DeepSeekMoE 16B | 16.4B/2.8B | 28 | 2048 | MHA 16头 | 2共享+64路由/激活2+6 | 2.0T | 4K | BPE 100K | 细粒度专家+共享专家 |
| DeepSeek-Coder 33B | 33B 稠密 | 62 | 7168 | GQA(group 8) | — | 2.0T | 16K(RoPE base 1e5,线性×4) | BPE 32K | 仓库级+FIM(0.5 PSM) |
| DeepSeekMath 7B | 7B 稠密 | (同Coder7B) | — | — | — | +120B(续训500B) | 4K | BBPE 100K | GRPO |
| DeepSeek-V2 | 236B/21B | 60 | 5120 | **MLA** 128头 | 2共享+160路由/激活2+6 | 8.1T | 128K(YaRN) | BBPE 100K | MLA+DeepSeekMoE |
| DeepSeek-V2-Lite | 15.7B/2.4B | 27 | 2048 | MLA 16头 | 2共享+64路由/激活2+6 | 5.7T | 32K | BBPE 100K | MLA(不压Q) |
| DeepSeek-Coder-V2 | 236B/21B（Lite 16B/2.4B） | 同V2 | 同V2 | MLA | 同V2 | 4.2T+6T=10.2T | 128K | 同V2 | 续训扩码 |
| DeepSeek-V3 | 671B/37B | 61 | 7168 | MLA 128头 | 1共享+256路由/激活1+8 | 14.8T | 128K(YaRN两阶段) | BBPE 128K | 无辅损均衡+MTP+FP8 |
| DeepSeek-R1-Zero/R1 | 671B/37B(基于V3-Base) | 同V3 | 同V3 | MLA | 同V3 | (后训练) | 32K→64K(R1-Zero rollout) | 同V3 | 纯RL/多阶段RL |
| DeepSeek-Prover-V2 671B | 671B/37B(基于V3-Base) | 同V3 | 同V3 | MLA | 同V3 | (SFT 16K+RL 32K) | 32K(RL) | 同V3 | 子目标分解+GRPO |
| DeepSeek-Prover-V2 7B | 7B(基于Prover-V1.5-Base) | — | — | — | — | (RL rollout蒸馏) | 4K→32K | — | 同上小模型 |
| DeepSeek-V3.1 | 671B/37B | 同V3 | 同V3 | MLA | 同V3 | V3 + 840B续训 | 128K | 更新tokenizer | 混合推理+UE8M0 FP8 |
| DeepSeek-V3.2(-Exp) | 671B/37B | 同V3.1 | 同V3.1 | **MLA+DSA**(选top-2048) | 同V3 | (Exp续训:warmup 2.1B+sparse 943.7B) | 128K | 同V3.1 | 稀疏注意力DSA |

---

## DeepSeek-LLM（7B / 67B，稠密）

**定位**：用自研 scaling laws 指导、从零训练的开源稠密双语 LLM（对标 LLaMA-2 70B）。

### 架构细节
- 7B：30 层、d_model=4096、32 注意力头、32 KV头（MHA）；67B：95 层、d_model=8192、64 头、**8 KV头（GQA）**。
- 微观设计沿用 LLaMA：Pre-Norm + **RMSNorm**、**SwiGLU**（FFN 中间维 = 8/3 · d_model）、**RoPE** 位置编码。
- 宏观差异：67B 通过**加深网络（95层）而非加宽 FFN** 来扩参，便于流水线切分。
- 初始化标准差 0.006。
- tokenizer：**Byte-level BPE（BBPE）**，基于 HuggingFace tokenizers；常规词表 100000，加 15 特殊 token = 100015，训练时配置 vocab=102400；在约 24GB 多语语料上训练；预分词防止跨字符类合并（仿 GPT-2），数字按位拆分（仿 LLaMA）。
- 上下文长度 4096。

### 预训练数据
- **2T token**，以中英为主。
- 三阶段：去重（deduplication）→ 过滤（filtering）→ 重混（remixing）。

### 数据处理 pipeline
- **激进去重**：跨整个 Common Crawl 去重而非单 dump；跨 91 个 dump 去重比单 dump 多删 4 倍文档（去重率：1 dump 22.2% → 91 dumps 89.8%）。
- 过滤：结合语言学 + 语义评估，从个体与全局两个视角评文档质量。
- 重混：增加欠表示领域占比以平衡数据。

### 数据配比
- 官方未公开具体领域百分比；论文强调 remix 提升欠表示领域。
- 「scaling laws with different data」实验显示：数据质量越高，应越多算力分给模型而非数据（早期数据 a=0.450/b=0.550；当前数据 a=0.524/b=0.476；OpenWebText2 a=0.578/b=0.422）。

### 训练细节
- 优化器 AdamW（β1=0.9, β2=0.95, weight_decay=0.1），梯度裁剪 1.0。
- **多步学习率调度（替代 cosine）**：2000 warmup 步达峰值，处理 80% token 后降至 31.6%，90% 后降至 10%（便于续训复用第一阶段）。
- 7B：LR 4.2e-4、batch 2304、序列 4096；67B：LR 3.2e-4、batch 4608、序列 4096。
- batch/LR 随算力的幂律拟合：η_opt = 0.3118·C^(-0.1250)，B_opt = 0.2920·C^(0.3271)。
- 精度：**bf16 训练，fp32 累积梯度**；in-place cross-entropy（bf16 logits 在 CUDA kernel 内即时转 fp32）。
- 模型规模度量用「非嵌入 FLOPs/token M」替代参数 N：M = 72·n_layer·d² + 12·n_layer·d·l_seq。

### SFT 细节
- 收集约 **150万（1.5M）** 中英指令实例；其中 helpful 120万（通用31.2%、数学46.6%、代码22.2%），safety 30万。
- 7B 训 4 epoch、67B 仅 2 epoch（67B 过拟合严重）；LR 7B=1e-5、67B=5e-6。
- 观察：数学 SFT 数据越多重复率越高，用两阶段微调 + DPO 缓解。

### RL/对齐细节
- **DPO**（非 PPO/GRPO）：构造 helpfulness + harmlessness 偏好数据，用 DeepSeek Chat 模型生成候选回复。
- DPO 训 1 epoch，LR 5e-6，batch 512，warmup + cosine。

### AI infra
- **HAI-LLM** 自研框架：DP + TP + SP + 1F1B 流水线并行（仿 Megatron）；FlashAttention；ZeRO-1 分片优化器状态；算子融合（LayerNorm/GEMM/Adam）。
- 每 5 分钟异步存 checkpoint；支持从不同 3D 并行配置恢复。
- 评测：生成任务用 vLLM，非生成任务用 continuous batching。

### 来源
- arXiv 2401.02954 《DeepSeek LLM: Scaling Open-Source Language Models with Longtermism》
- 本地：`../../../sources/llm/2023/deepseek-llm.pdf`

---

## DeepSeekMoE（2B / 16B / 145B）

**定位**：DeepSeek 的 MoE 架构奠基论文，提出后续 V2/V3 沿用的两大核心创新。

### 架构细节（两大创新）
1. **细粒度专家切分（Fine-Grained Expert Segmentation）**：把每个专家 FFN 切成 m 个更小专家（中间维降到 1/m），激活专家数同步 ×m，保持总计算不变；组合灵活度暴增（N=16 top-2 仅 120 种组合 → 切4后 top-8 有 44 亿+ 种）。
2. **共享专家隔离（Shared Expert Isolation）**：隔离 K_s 个**始终激活的共享专家**捕获公共知识，减少路由专家冗余。
- 负载均衡：**专家级 balance loss（α1）+ 设备级 balance loss（α2）**（注意：此时还用辅助损失，V3 才改无辅助损失）。
- 共享:激活路由专家比例定为 **1:3**。
- 16B 配置：28 层、d_model=2048、16 头（每头 128 维）、**首层不替换为 MoE**（首层负载均衡收敛慢）；每 MoE 层 = **2 共享 + 64 路由**专家，每专家 0.25×标准 FFN，每 token 激活 **2 共享 + 6 路由**；总参 16.4B，激活 2.8B。
- 2B 验证配置：9 层、d_model=1280、10 头；1 共享 + 63 路由、激活 1+7；总参 2.0B、激活 0.3B。
- tokenizer：BPE，16B 用 vocab=100K（2B 验证用 8K）。

### 预训练数据
- 16B：**2T token**（与 LLaMA-2 7B 对齐）；2B 验证：100B token 子集。
- 语料来自 DeepSeek-AI 多语语料（中英为主 + 其它语言），含 web、数学、代码、文献等。

### 训练细节
- AdamW（β1=0.9, β2=0.95, wd=0.1），warmup-and-step-decay（2K warmup，80%/90% 处各 ×0.316），梯度裁剪 1.0，无 dropout。
- 16B：max LR 4.2e-4、batch 4.5K、序列 4K（每 batch 18M token）、106449 步达 2T；专家级 balance factor=0.001（很小，因流水线下高 factor 反伤效率）。
- 2B：max LR 1.08e-3、batch 2K、序列 2K、25000 步达 100B；balance factor=0.01；单 GPU 部署所有专家，不丢 token。

### AI infra
- HAI-LLM：TP + ZeRO DP + PipeDream 流水线 + **专家并行（EP，DP×TP 组合）**；自研 CUDA/Triton kernel 做 gating 与跨专家线性层融合。
- 集群：NVIDIA A100 或 H800（每节点 8 GPU，NVLink/NVSwitch + InfiniBand 跨节点）。
- 16B 可单卡 40GB GPU 部署（无需量化）。

### 来源
- arXiv 2401.06066 《DeepSeekMoE: Towards Ultimate Expert Specialization in Mixture-of-Experts Language Models》
- 本地：`../../../sources/llm/2023/deepseekmoe.pdf`

---

## DeepSeek-Coder（1.3B / 6.7B / 33B，稠密）

**定位**：开源代码模型系列，仓库级语料 + FIM。

### 架构细节
- 1.3B：24 层、hidden 2048、中间维 5504、16 头、MHA；6.7B：32 层、hidden 4096、中间维 11008、32 头、MHA；33B：62 层、hidden 7168、中间维 19200、56 头、**GQA(group 8)**。
- 框架同 DeepSeek-LLM：decoder-only、RoPE、SwiGLU、FlashAttention v2。
- tokenizer：**BPE，vocab=32000**。
- 上下文 16K（RoPE 重配后理论 64K，实际可靠 16K 内）。

### 预训练数据
- **2T token**，组成：**87% 源代码 + 10% 英文代码相关 NL（GitHub Markdown + StackExchange）+ 3% 中文 NL**。
- 87 种编程语言；GitHub 公开仓库（2023-02 前创建）；清洗后 798GB / 6.03 亿文件。

### 数据处理 pipeline
- 流程：数据爬取 → 规则过滤（仿 StarCoder，过滤后仅剩原始 32.8%）→ **依赖解析（拓扑排序排列同仓库文件，import/using/include 正则提取）** → **仓库级近似去重（而非文件级，保仓库结构完整）** → 质量筛选（编译器 + 质量模型 + 启发式，去语法错/低可读/低模块化）。
- **去污染**：n-gram 过滤，含 HumanEval/MBPP/GSM8K/MATH 的 10-gram 完全匹配即删；3~10gram 用精确匹配。

### 训练策略
- **下一 token 预测 + FIM（Fill-In-Middle）**：FIM rate 0.5，PSM 模式（实验对比 0/50%/100% FIM + 50% MSP，最终选 50% PSM）。FIM sentinel：`<｜fim_start｜>...<｜fim_hole｜>...<｜fim_end｜>`。
- AdamW（β1=0.9, β2=0.95），三阶段 LR（2000 warmup，末段降至初始 10%，每阶段 ×√(1/10)）；batch/LR：1.3B(1024/5.3e-4)、6.7B(2304/4.2e-4)、33B(3840/3.5e-4)。
- 长上下文：RoPE 线性 scaling 1→4、base 10000→100000，额外训 1000 步（batch 512、序列 16K）。

### SFT（Instruct）
- Alpaca 指令格式，多轮用 `<|EOT|>` 分隔；cosine 调度、100 warmup、初始 LR 1e-5、batch 4M token、共 2B token。

### AI infra
- HAI-LLM：TP + ZeRO DP + PipeDream；A100/H800 集群（NVLink/NVSwitch + InfiniBand）。

### 来源
- arXiv 2401.14196 《DeepSeek-Coder: When the Large Language Model Meets Programming》
- 本地：`../../../sources/llm/2023/deepseek-coder.pdf`

---

## DeepSeekMath（7B）——GRPO 发源地

**定位**：从 DeepSeek-Coder-Base-v1.5 7B 续训数学语料；**首次提出 GRPO**。

### 架构细节
- 与 DeepSeek-LLM 同框架；7B 由 Coder-Base-v1.5 7B 初始化（论文也用 1.3B「DeepSeek-LLM 1.3B」做语料对比实验）。
- 上下文 4K；tokenizer vocab 100K（语料大小按此 tokenizer 计）。

### 预训练数据
- **DeepSeekMath Corpus：120B 数学 token**（35.5M 数学网页），从 Common Crawl 提取，比 Minerva 数学网页大 ~7 倍、比 OpenWebMath 大 ~9 倍，多语（中英为主）。
- 续训总量 **500B token**，配比：**56% DeepSeekMath Corpus + 4% AlgebraicStack + 10% arXiv + 20% GitHub 代码 + 10% CC 中英 NL**。

### 数据处理 pipeline（迭代 fastText 召回）
1. 用 OpenWebMath 做种子，随机 50万正例 + 50万 CC 负例训 **fastText**（dim=256, lr=0.1, n-gram≤3, min-count=3, epoch=3）。
2. URL 去重 + 近似去重把 CC 压到 **40B HTML 页**，按 fastText 分排序保 top（实验对比 top 40B/80B/120B/160B，首轮保 top 40B）。
3. 发现数学域（>10% 页被召回的 domain，如 mathoverflow.net）→ 人工标注数学 URL path → 加入种子。
4. 4 轮迭代后得 120B（第 4 轮 98% 已在第 3 轮收集，停止）。
- 去污染：仿 Coder，10-gram 完全匹配 GSM8K/MATH/CMATH/AGIEval 即删，3~10gram 精确匹配。
- 关键发现：**代码续训先于数学训练能提升数学（含工具与非工具）；训 arXiv 论文对所有数学 benchmark 无明显提升**。

### SFT 细节
- 数学指令数据 **776K** 例：CoT + PoT（program-of-thought）+ TIR（tool-integrated reasoning），中英；中文 K-12 覆盖 76 子主题。
- 训 500 步、batch 256、恒定 LR 5e-5、最大上下文 4K。

### RL/对齐细节——GRPO
- **GRPO（Group Relative Policy Optimization）**：PPO 变体，**去掉 critic（value）模型**，从同一 query 的一组输出 {o_1..o_G} 的**组内奖励**估计 baseline/advantage：A_i = (r_i − mean(r)) / std(r)。
- 目标含 clip(ε) + KL 正则（β，用无偏 K3 估计器，直接加在 loss 上而非逐 token 奖励）。
- DeepSeekMath-RL：仅用 GSM8K/MATH 的 CoT 指令数据做 RL，GSM8K 82.9%→88.2%、MATH 46.8%→51.7%，且 OOD（CMATH 84.6%→88.8%）也提升。
- 提出统一范式理解 RFT/DPO/PPO/GRPO（皆为直接/简化 RL）。

### AI infra
- HAI-LLM；max LR 续训 4.2e-4、batch 10M token；多步 LR 调度（同 LLM）。

### 来源
- arXiv 2402.03300 《DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models》
- 本地：`../../../sources/llm/2023/deepseekmath.pdf`（另有 `/2024/files/deepseekmath-grpo.pdf` 与 `/themes/*/files/deepseekmath-grpo-2402.03300.pdf`）

---

## DeepSeek-V2（236B/21B MoE）+ V2-Lite（15.7B/2.4B）

**定位**：首次引入 **MLA**，省 KV cache 93.3%、省训练 42.5%、生成吞吐 ×5.76。

### 架构细节
- **236B 总参，21B 激活**；60 层、d_model=5120；初始化 std=0.006。
- **MLA（Multi-head Latent Attention）**：n_h=128 头、每头 d_h=128；**KV 压缩维 d_c=512**、**Q 压缩维 d'_c=1536**；**解耦 RoPE**（decoupled query/key 每头 d^R_h=64）。KV cache 仅 (d_c + d^R_h)·l 元素 ≈ GQA 2.25 组，但性能强于 MHA。在压缩潜向量后加额外 RMSNorm + width bottleneck scaling factor 稳训练。
- **DeepSeekMoE**：除首层外所有 FFN 替为 MoE；每层 **2 共享 + 160 路由**专家（每专家中间维 1536），每 token 激活 **2 共享 + 6 路由**。
- **设备受限路由（device-limited routing）**：每 token 至多发往 M=3 设备。
- 负载均衡：仍用辅助损失——**专家级（α1=0.003）+ 设备级（α2=0.05）+ 通信均衡（α3=0.02）**三种 loss + **设备级 token-dropping**（capacity factor=1.0，约 10% 序列永不丢 token）。
- tokenizer：BBPE vocab=100K（同 DeepSeek-67B）。
- 上下文：4K 预训练 → **YaRN 扩到 128K**。
- V2-Lite：27 层、hidden 2048、16 头（**不压缩 Q**）、d_c=512、d^R_h=64；2 共享 + 64 路由、激活 2+6；总参 15.7B、激活 2.4B；上下文 32K。

### 预训练数据
- **8.1T token**；数据阶段同 DeepSeek-67B 但扩量提质，**显著增加中文**（中文 token 比英文多约 12%）；过滤掉争议性/特定地区文化内容以减偏。
- V2-Lite：与 V2 同语料，训 **5.7T token**。

### 数据配比
- 官方未公开具体领域百分比；强调恢复「误删数据」、提质过滤。

### 训练细节
- AdamW（β1=0.9, β2=0.95, wd=0.1），梯度裁剪 1.0。
- warmup-and-step-decay：2K warmup，约 60% token 后 ×0.316，约 90% 后再 ×0.316；**max LR 2.4e-4**。
- **batch size 调度**：前 225B token 从 2304 增到 9216，之后维持 9216；序列 4K。
- 流水线并行部署各层，路由专家均分 8 设备（D=8）。
- 训练成本：每 1T token 仅 **172.8K H800 卡时**（vs DeepSeek-67B 300.6K，省 42.5%）。

### AI infra
- **HAI-LLM**：**16-way 零气泡流水线（zero-bubble PP）+ 8-way 专家并行（EP）+ ZeRO-1 DP**；激活参数少 + 重计算 → **无需 TP**；共享专家计算与 EP all-to-all 通信重叠；自研通信/路由/融合线性 CUDA kernel；改进版 FlashAttention-2 适配 MLA。
- 集群：H800（每节点 8 GPU，NVLink/NVSwitch + InfiniBand）。
- 长上下文：YaRN（scale s=40, α=1, β=32，目标 160K，仅作用于解耦共享 key k^R_t；长度缩放 √t=0.0707·ln s+1）；额外训 1000 步（序列 32K、batch 576 序列）。
- 推理部署：参数转 **FP8** + KV cache 量化（平均 6 bit/元素）；单节点 8×H800 生成吞吐 >50K token/s。

### SFT 细节
- **150万（1.5M）** 实例（120万 helpful + 30万 safety）；2 epoch、LR 5e-6。

### RL/对齐细节——GRPO 两阶段
- **GRPO**（同 DeepSeekMath），目标含 KL(β) 正则。
- **两阶段 RL**：①推理对齐（先训 code/math 推理奖励模型 RM_reasoning）；②人类偏好对齐（多奖励：helpful RM + safety RM + rule-based RM，加权 c1/c2/c3）。
- 偏好数据：代码用编译器反馈、数学用 ground-truth；RM 由 V2 Chat(SFT) 初始化，point-wise 或 pair-wise loss。
- RL infra：**hybrid engine（训练/推理不同并行）+ vLLM 大 batch 推理后端 + CPU 卸载调度**。

### 来源
- arXiv 2405.04434 《DeepSeek-V2: A Strong, Economical, and Efficient MoE Language Model》
- 本地：`../../../sources/llm/2024/deepseek-v2.pdf`（另 `/themes/architecture/files/deepseek-v2.pdf`、`/themes/ai-infra/files/deepseek-v2-2405.04434.pdf`）

---

## DeepSeek-Coder-V2（16B / 236B MoE）+ Lite

**定位**：从 DeepSeek-V2 中间 checkpoint 续训，代码语言 86→338 种，上下文 16K→128K，代码/数学比肩 GPT-4-Turbo。

### 架构细节
- 架构同 DeepSeek-V2：236B 版对应 V2、16B(Lite) 版对应 V2-Lite（MLA + DeepSeekMoE，激活 21B / 2.4B）。
- 续训曾遇**指数归一化致训练不稳/梯度尖峰 → 退回常规归一化**。
- 16B 用 NTP + FIM（0.5 PSM）；236B 仅 NTP。
- 上下文扩到 128K（YaRN，s=40/α=1/β=32）。

### 预训练数据
- 续训 **6T token**，配比 **60% 源代码 + 10% 数学 + 30% NL**（NL 直接采自 V2 语料）。
- 新代码语料 **1170B code token**（GitHub + CC，338 种语言）：821B 代码 + 185B 代码相关文本（markdown/issues）；GitHub 仓库（2023-11 前）。
- 数学：用 DeepSeekMath pipeline 收 **221B 数学 token**（约 2× DeepSeekMath 120B）。
- **总曝光 10.2T token**（V2 中间 checkpoint 4.2T + 续训 6T）。

### 数据处理 pipeline
- 同 DeepSeek-Coder 的规则过滤 + 近似去重；CC 代码/数学用 fastText 迭代召回（StackOverflow/PyTorch docs/StackExchange 做种子，BPE tokenizer 提升中文召回；3 轮迭代收 70B code + 221B math web；GitHub 再 2 轮收 94B 源代码）。

### 训练细节
- AdamW（β1=0.9, β2=0.95, wd=0.1）；**cosine 衰减（2000 warmup，降至 10%）**；batch/LR 按 V2 规格。
- 长上下文两阶段：①序列 32K、batch 1152、1000 步；②序列 128K、batch 288、1000 步（上采样长上下文数据）。

### SFT 细节
- 指令集：20K 代码 + 30K 数学（来自 Coder/Math）+ V2 通用数据；共 **300M token**；cosine、100 warmup、LR 5e-6、batch 1M token、共 1B token。

### RL/对齐细节
- **GRPO**；prompt 约 40K（code+math，每 code prompt 带测试用例）。
- **奖励建模**：数学用 ground-truth；代码——虽编译器给 0-1，但测试用例覆盖不全致噪声，故**训奖励模型给信号（实测 RM 信号 > 原始编译器信号）**。

### 来源
- arXiv 2406.11931 《DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence》
- 本地：`../../../sources/llm/2024/deepseek-coder-v2.pdf`

---

## DeepSeek-V3（671B/37B MoE）——旗舰

**定位**：无辅助损失负载均衡 + MTP + FP8 训练 + DualPipe，全程 2.788M H800 卡时（≈557.6 万美元）。

### 架构细节
- **671B 总参，37B 激活**；61 层、d_model=7168；初始化 std=0.006。
- **MLA**：n_h=128 头、每头 d_h=128；KV 压缩维 d_c=512、Q 压缩维 d'_c=1536、解耦 RoPE d^R_h=64。
- **DeepSeekMoE**：除**前 3 层**外所有 FFN 替为 MoE；每层 **1 共享 + 256 路由**专家（每专家中间维 2048），每 token 激活 **1 共享 + 8 路由**，至多发往 4 节点；路由 affinity 用 **Sigmoid**（V2 是 Softmax）后归一化。
- **无辅助损失负载均衡（auxiliary-loss-free）**：每专家加可学偏置 b_i 只用于 top-K 路由（不进 gating value）；每步末按过载/欠载以 bias update speed γ 增减 b_i（γ=0.001 前 14.3T token，后 500B 设 0）。另加极小的**序列级**互补 balance loss（α=0.0001）。
- **MTP（Multi-Token Prediction）**：D=1（除下一 token 外多预测 1 个）；用顺序 MTP 模块、保持完整因果链；MTP 模块与主模型**共享嵌入层与输出头**；MTP loss 权重 λ（前 10T=0.3，后 4.8T=0.1）。推理时可丢弃或用于投机解码。
- **不丢 token**（训练与推理均不丢）。
- tokenizer：**BBPE，扩展 vocab=128K**；新预分词器合并标点 + 换行（并随机拆分缓解 token boundary bias）。
- 预训练序列 4K → **YaRN 两阶段扩到 32K 再 128K**。

### 预训练数据
- **14.8T token**；相比 V2 提高数学/编程占比、扩多语；文档打包（不用跨样本 attention mask）；FIM rate 0.1（PSM）。
- R1 论文补充：V3-Base **预训练只用纯网页 + 电子书，不含合成数据**（但部分网页含 OpenAI 模型生成答案，cooldown 阶段亦为自然爬取数据）；知识截止 2024-07。

### 数据配比
- 官方未公开各领域具体百分比；只说提高数学/代码比例、扩多语。

### 训练细节
- AdamW（β1=0.9, β2=0.95, wd=0.1），梯度裁剪 1.0；序列 4K。
- **LR 调度**：前 2K 步 0→2.2e-4 线性升 → 恒定 2.2e-4 直到消耗 10T token → 在 4.3T token 内 cosine 降到 2.2e-5 → 末 500B：前 333B 恒 2.2e-5，后 167B 恒 7.3e-6。
- **batch 调度**：前 469B token 从 3072 增到 15360，之后维持 15360。
- 路由专家均分 64 GPU（8 节点）；node-limited M=4。
- **训练极稳：全程无不可恢复 loss spike、无回滚**。
- 训练成本（按 H800 租金 $2/卡时）：预训练 2664K 卡时($5.328M) + 长上下文 119K($0.238M) + 后训练 5K($0.01M) = **2788K 卡时 / $5.576M**；每 1T token 仅 180K 卡时（2048 卡 ≈3.7 天）。

### AI infra（重头戏）
- 集群：**2048 NVIDIA H800**（每节点 8 GPU，NVLink/NVSwitch + InfiniBand）。
- **HAI-LLM**：**16-way PP + 64-way EP（跨 8 节点）+ ZeRO-1 DP**；**无 TP**。
- **DualPipe**：双向流水线，把 attention/all-to-all dispatch/MLP/all-to-all combine 四段重叠（backward 再拆 input/weight），气泡 ≈ (PP/2−1)(F&B+B−3W)，几乎全隐藏 all-to-all + PP 通信；代价是保两份参数 + 峰值激活内存 ×(1/PP)。
- **跨节点 all-to-all kernel**：限每 token 至多 4 节点；先 IB 传同 in-node index GPU、再 NVLink 转发（NVLink 160GB/s ≈ 3.2× IB 50GB/s）；warp specialization，仅用 **20 个 SM（132 中）/10 通道**做通信；自定义 PTX + auto-tune chunk。
- **FP8 混合精度训练（首次在超大模型验证）**：三大 GEMM（Fprop/Dgrad/Wgrad）走 FP8；**细粒度量化**——激活按 1×128 tile、权重按 128×128 block；**累加提升精度**（每 N_C=128 间隔从 Tensor Core 提到 CUDA Core 做 FP32 累加，因 H800 FP8 累加仅 ~14bit）；**全张量用 E4M3**（非 E4M3/E5M2 混合）；**online 量化**；优化器一阶/二阶矩用 **BF16**，master weight/梯度仍 FP32；激活/通信 FP8（部分用 E5M6）。相对 BF16 loss 误差 <0.25%。
- 内存优化：RMSNorm 与 MLA up-proj 重计算、EMA 参数放 CPU 异步更新、MTP 与主模型共享嵌入/输出头同 PP rank。
- 推理部署（预填/解码分离）：**预填**最小单元 4 节点 32 GPU（attention TP4+SP+DP8，MoE EP32，32 冗余专家）；**解码**最小单元 40 节点 320 GPU（attention TP4+SP+DP80，MoE EP320，每 GPU 1 专家，64 GPU 托冗余+共享专家，IBGDA 降延迟，共享专家视为始终选中的路由专家 → 每 token 选 9 专家）。

### SFT 细节
- 指令集 **150万（1.5M）** 实例，分域定制：
  - **推理数据**：用内部 **DeepSeek-R1** 生成；先为每域（code/math/general）训「专家模型」（SFT+RL pipeline），生成两类样本（<problem, original response> 与 <system prompt, problem, R1 response>），RL 高温采样融合 R1 与原始模式，最后**拒绝采样**筛高质量 SFT。
  - **非推理数据**（写作/角色扮演/简单 QA）：用 **DeepSeek-V2.5** 生成 + 人工核验。
- 2 epoch；cosine LR 5e-6→1e-6；样本打包但用 sample masking 互相隔离。

### RL/对齐细节
- **奖励**：rule-based RM（数学装箱验证、LeetCode 编译器）+ model-based RM（自由答案/创意写作，从 V3 SFT checkpoint 训，含 CoT 防 reward hacking）。
- **GRPO**（同前），prompt 涵盖 coding/math/writing/role-play/QA。
- **从 R1 蒸馏推理**：将 R1 长 CoT 的验证/反思模式蒸入 V3，同时控制输出风格与长度。

### 来源
- arXiv 2412.19437 《DeepSeek-V3 Technical Report》
- 本地：`../../../sources/llm/2024/deepseek-v3.pdf`（另 `/2025/files/deepseek-v3.pdf`、`/themes/architecture|ai-infra|post-training/files/deepseek-v3*.pdf`）
- 补充硬件论文：arXiv 2505.09343（本地 `/themes/ai-infra/files/deepseek-v3-hardware-2505.09343.pdf`）

---

## DeepSeek-R1-Zero / DeepSeek-R1（基于 V3-Base，671B/37B）

**定位**：R1-Zero 证明**纯 RL（无 SFT）即可激发推理**；R1 用多阶段流水线对齐人类偏好；并蒸馏 6 个小模型。

### 架构细节
- 基座 = **DeepSeek-V3-Base**（671B/37B，架构同 V3）；R1 复用 V3 SFT 的非推理数据。
- R1-Zero rollout 最大长度 32,768（8.2k 步前）→ 65,536（之后）。

### DeepSeek-R1-Zero（纯 RL）
- **GRPO**，**绕过 SFT 直接在 V3-Base 上 RL**；奖励纯**规则**（accuracy + format，等权），不用神经 RM（防 reward hacking）。
- 模板：`<think>推理</think><answer>答案</answer>`。
- 超参：**LR 3e-6、KL 系数 0.001、采样温度 1**；每 question 采 16 输出；每步 32 question → **batch 512**；每 400 步用最新 policy 替换 reference；rollout 每次生成 8192 输出，随机分 16 mini-batch、单内层 epoch；共 **10400 步 ≈ 1.6 epoch**。
- 涌现「aha moment」、思考长度自增；AIME 2024 pass@1 15.6%→77.9%（cons@16 86.7%）。

### DeepSeek-R1（多阶段）
**流水线**：V3-Base →(冷启动 SFT)→ R1-Dev1 →(推理RL)→ R1-Dev2 →(拒绝采样SFT)→ R1-Dev3 →(全场景RL)→ R1。
1. **冷启动数据**：数千条长 CoT，第一人称、语言一致；用 R1-Zero 高温(1.0)生成 → sympy 校验答案 + 规则去重复/语言混合过滤 → 人工改写成对话风 → LLM 仿写 → 二次人工核验。
2. **第一 RL 阶段**：LR 3e-6、KL 0.001、**GRPO clip ε=10（大 clip 由 Zhibin Gou 提出）**、温度 1、16 输出、32 question/步（batch 512）、每 400 步换 reference；加**语言一致性奖励**（目标语词占比，直接加到最终奖励）。
3. **拒绝采样 SFT（800K）**：从第一阶段 RL checkpoint 拒绝采样得 **~600K 推理样本**（部分用 V3 做 generative RM 判定、过滤混语/长段/代码块）+ **~200K 非推理样本**（复用 V3 SFT，含软件工程/程序修复/前端）。
4. **第二 RL 阶段（全场景）**：温度降到 0.7，共 1700 步，model-based 偏好奖励仅在**最后 400 步**加入（防 reward hacking）；奖励 = reasoning(规则) + general(RM+format) + language。

### 奖励模型
- **Helpful RM**：arena-hard 格式生成偏好对，每对查 V3 四次取平均、保 Δ>1，控长度偏差；**66,000 对**；pair-wise loss、batch 256、LR 6e-6、1 epoch、max seq 8192。
- **Safety RM**：**106,000** prompt（safe/unsafe 标注），point-wise loss，超参同 helpful RM。

### RL 数据配方（B.3.1）
- 推理 RL 数据 4 类：**数学 26K**（avg 122 prompt token，对则 reward 1）、**代码 17K 算法竞赛 + 8K bug 修复**（隐藏测试用例）、**STEM 22K**（4~8 选择题，物理15.5%/生物30.7%/化学46.5%/其它7.3%，avg 161 token）、**逻辑 15K**。

### 蒸馏小模型（Table 6）
- 直接对小模型 SFT（用 R1 生成数据），**不做 RL**；max 上下文 32768、batch 64：
  - R1-Distill-Qwen-1.5B ← **Qwen2.5-Math-1.5B**（LR 1e-4）
  - R1-Distill-Qwen-7B ← **Qwen2.5-Math-7B**（8e-5）
  - R1-Distill-Qwen-14B ← **Qwen2.5-14B**（7e-5）
  - R1-Distill-Qwen-32B ← **Qwen2.5-32B**（6e-5）
  - R1-Distill-Llama-8B ← **Llama-3.1-8B**（5e-5）
  - R1-Distill-Llama-70B ← **Llama-3.3-70B-Instruct**（2e-5）

### AI infra / 训练成本
- **RL 框架**四模块（解耦）：Rollout（vLLM workers，MoE EP 跨节点 + 热点专家冗余 + MTP 自投机解码）、Inference（RM/reference 前向）、Rule-based Reward（code executor/answer matcher/format checker，异步重叠）、Training（actor + 可选 critic，Best-Fit 数据打包 + DualPipe）；模块间用完即从 VRAM 卸载到内存/磁盘。
- 训练成本：预实验用 A100（30B 小模型）；**R1-Zero：64×8 H800 ≈198 小时**；**R1：同 64×8 H800 ≈80 小时（约 4 天）**；SFT 数据集 5K 卡时。
- 去污染：10-gram 过滤；数学域单独删了约 600 万潜在预训练文本；后训练数学 SFT/RL prompt 仅取 2023 前竞赛。

### PPO vs GRPO 对比（附录）
- GRPO 去掉与 policy 同尺寸的 value 模型；KL 用无偏 K3 估计器直接进 loss（PPO 是逐 token KL 罚进奖励，会隐式罚长度）；周期性把 reference 更新为最新 policy；MATH 任务上 PPO(λ=0.95 默认)远逊 GRPO，λ=1.0 调优后接近。

### 来源
- arXiv 2501.12948 《DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning》（本地为 Nature 扩充版，含完整 RL 超参与数据配方）
- 本地：`../../../sources/llm/2025/deepseek-r1.pdf`（另 `/themes/*/files/deepseek-r1*.pdf`、`/agentic/files/deepseek-r1-2501.12948.pdf`）

---

## DeepSeek-R1-0528（2025-05-28，官方迭代版）

### 已公开要点（官方博客 / model card）
- R1 的迭代更新：**benchmark 性能提升、前端能力增强、幻觉减少、支持 JSON 输出与 function calling**。
- 权重：`https://huggingface.co/deepseek-ai/DeepSeek-R1-0528`。
- API 用法不变（thinking mode）。
- 具体训练数据/算力/超参变化：**官方未公开**（仅博客式发布说明，无独立技术报告）。

### 来源
- 官方 API 文档 News《DeepSeek-R1-0528 Release》`https://api-docs.deepseek.com/news/news250528`
- 本地：`../../../sources/llm/2025/deepseek-r1-0528.html`

---

## DeepSeek-Prover-V2（671B / 7B，Lean 4 形式化证明）

**定位**：子目标分解递归求证 + GRPO，把非形式推理与形式证明统一进一个模型。

### 架构细节
- **671B 版**：基于 **DeepSeek-V3-Base-671B**（架构同 V3，671B/37B MLA+MoE）。
- **7B 版**：基于 **DeepSeek-Prover-V1.5-Base-7B**，上下文 **4096 → 扩到 32768**。
- 两种生成模式：non-CoT（快，专家迭代）+ CoT（强，冷启动+RL）。

### 数据 / 冷启动 pipeline
- 用 **DeepSeek-V3** 做子目标分解 + Lean 4 形式化（生成 have...sorry 子目标），**7B prover 模型**做每个子目标的证明搜索（降算力）。
- **课程学习**：用分解子目标生成两类推测定理（含/不含前序子目标为前提），渐进加难，纳入**专家迭代（expert iteration）**。
- **冷启动**：选 7B 端到端解不出但子目标全解的难题，拼接所有子目标证明 + V3 的 CoT → 数百条高质量合成冷启动数据。

### 训练细节
- **671B SFT**：在 V3-Base-671B 上，恒定 **LR 5e-6、上下文 16384**；语料 = non-CoT（专家迭代 Lean 代码）+ 冷启动 CoT。
- **671B RL**：**GRPO**，二值奖励（Lean 验证对=1/错=0）；早期加**一致性奖励**（强制最终证明含所有分解 have 引理）；每轮采 256 题、每题 32 候选、max 序列 32768。
- **7B**：先把 V1.5-Base-7B 上下文 4096→32768，用 671B RL rollout 数据微调（CoT+non-CoT），再做同样 RL。

### 结果
- 671B：MiniF2F-test **88.9% pass**（CoT、32 样本 82.4% SOTA）；PutnamBench 47/658；ProverBench-AIME 24&25 解 6/15。

### 来源
- arXiv 2504.21801 《DeepSeek-Prover-V2: Advancing Formal Mathematical Reasoning via Reinforcement Learning for Subgoal Decomposition》
- 本地：`../../../sources/llm/2025/deepseek-prover-v2.pdf`

---

## DeepSeek-V3.1（671B/37B，混合推理）

**定位**：在 V3 base 上长上下文续训 + 混合推理（一模两用），首个「agent 时代」步骤。

### 架构细节
- 架构同 V3（671B/37B MLA+MoE，HF 模型类型 `deepseek_v3`，fp8）；上下文 128K。
- **混合推理**：同一模型经 chat template 切换 **Think / Non-Think** 两模式（API：deepseek-chat=非思考、deepseek-reasoner=思考）。
- tokenizer 与 chat template 更新（新 tokenizer_config）。

### 预训练 / 续训数据
- V3.1-Base = 在**原 V3 base checkpoint** 上做**两阶段长上下文扩展续训**（沿用 V3 报告方法，扩充长文档数据）：
  - **32K 扩展阶段：增至 630B token（较 V3 增 10×）**
  - **128K 扩展阶段：增至 209B token（较 V3 增 3.3×）**
  - 合计约 **840B token** 续训（官方博客「840B tokens continued pretraining」一致）。

### 训练细节
- **UE8M0 FP8 scale 数据格式**用于**模型权重与激活**，兼容 microscaling 格式（配合 DeepGEMM）。
- 其余预训练超参（LR/batch 等）：官方未公开独立报告，仅 model card + 博客。

### 后训练
- 在 V3.1-Base 上后训练；**post-training 优化工具调用 / 多步 agent**；V3.1-Think 答案质量比肩 R1-0528 但更快。
- 具体 SFT/RL 配方数字：**官方未公开**（无独立技术报告，V3.2 报告将其作为 baseline 引用）。
- 衍生：**DeepSeek-V3.1-Terminus**（V3.1 末版，作为 V3.2 续训起点）。

### 来源
- 官方 model card `https://huggingface.co/deepseek-ai/DeepSeek-V3.1-Base`、`https://huggingface.co/deepseek-ai/DeepSeek-V3.1`
- 官方 API News《DeepSeek V3.1 Release》`https://api-docs.deepseek.com/news/news250821`
- 本地：`../../../sources/llm/2025/deepseek-v3.1.html`

---

## DeepSeek-V3.2-Exp / DeepSeek-V3.2（DSA 稀疏注意力）

**定位**：V3.2-Exp 在 V3.1-Terminus 上引入 **DSA（DeepSeek Sparse Attention）**；V3.2 正式版架构与 Exp 完全一致，并加可扩展 RL + agentic 合成。

### 架构细节——DSA
- **唯一架构改动 = 在 MLA 上引入 DSA**（V3.2 与 V3.2-Exp 架构完全相同；相对 V3.1-Terminus 仅此一处）。
- **DSA 两组件**：
  1. **lightning indexer（闪电索引器）**：算 query h_t 与前序 token h_s 的 index 分 I_{t,s} = Σ_j w^I_{t,j}·ReLU(q^I_{t,j}·k^I_s)；indexer 头数少、**可用 FP8**、ReLU 激活（吞吐考虑）。
  2. **细粒度 token 选择**：每 query 只取 index 分 **top-k=2048** 的 KV 条目做注意力。
- **在 MLA 的 MQA 模式下实例化 DSA**（每个潜向量在该 token 所有 query 头间共享）。
- 复杂度从 O(L²) 降到 **O(Lk)**（lightning indexer 仍 O(L²) 但远轻于 MLA）。
- 上下文 128K。

### 继续预训练（从 V3.1-Terminus 128K checkpoint）
- 数据分布**完全对齐 V3.1-Terminus 的 128K 长上下文扩展数据**。
- **① Dense warm-up 阶段**：冻结除 lightning indexer 外所有参数，保持 dense attention，用 KL 散度 loss 对齐 indexer 与主注意力分布；**LR 1e-3、1000 步、每步 16 序列 × 128K = 共 2.1B token**。
- **② Sparse 训练阶段**：引入 top-k 选择，优化全部参数；indexer 仍对齐（仅在选中集 S_t 上）；indexer 输入从计算图 detach；**LR 7.3e-6、每 query 选 2048 KV、15000 步、每步 480 序列 × 128K = 共 943.7B token**。

### 后训练（V3.2）
- 维持与 V3.2-Exp 相同 pipeline：**Specialist Distillation + Mixed RL**。
- **Specialist Distillation**：先为每域从同一 V3.2-base 微调专家模型（六域：数学、编程、通用逻辑推理、通用 agent、agentic coding、agentic search，皆含 thinking/non-thinking），各以大规模 RL 训练，再用专家生成最终模型的领域数据。
- **Mixed RL（单阶段）**：仍用 **GRPO**，把推理 + agent + 人类对齐合并为一个 RL 阶段（避免多阶段灾难性遗忘）；推理/agent 用规则 outcome 奖励 + 长度惩罚 + 语言一致性；通用任务用带 rubric 的 generative RM。
- **后训练算力 >10% 预训练**（官方强调可扩展 RL）。
- **Scaling GRPO 稳定性技巧**：无偏 KL 估计（修正 K3）、Off-Policy Sequence Masking（按 KL 阈值 δ 屏蔽高散度负样本）、**Keep Routing**（训练强制用采样时的专家路由，自 V3-0324 起采用，对 MoE RL 稳定性关键）、**Keep Sampling Mask**（保留 top-p/top-k 截断 mask 对齐 π_old 与 π_θ 动作空间）。
- **Thinking in Tool-Use**：思考上下文管理（避免每轮工具调用重复推理）+ 大规模 agentic 任务合成（**>1800 环境 + 85000 复杂 prompt**）。

### 变体
- **DeepSeek-V3.2-Speciale**：仅用推理数据 + 减小长度惩罚的 RL；并入 **DeepSeekMath-V2**（Shao et al., 2025）的数据与奖励法增强数学证明；达 IMO 2025 / IOI 2025 / ICPC World Final 2025 / CMO 2025 金牌级。

### 推理 / 成本
- DSA 在 H800（$2/卡时）上长上下文端到端显著提速；V3.2-Exp 发布即 **API 降价 50%+**。
- 开源关键 GPU kernel（TileLang + CUDA）。

### 来源
- arXiv 2512.02556 《DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models》
- V3.2-Exp 技术报告 `https://github.com/deepseek-ai/DeepSeek-V3.2-Exp/blob/main/DeepSeek_V3_2.pdf`、model card `https://huggingface.co/deepseek-ai/DeepSeek-V3.2-Exp`
- 官方 API News《DeepSeek-V3.2-Exp Release》`https://api-docs.deepseek.com/news/news250929`、《DeepSeek-V3.2 Release》
- 本地：`../../../sources/llm/2025/deepseek-v3.2.pdf`、`deepseek-v3.2-exp.html`（另 `/themes/architecture/files/deepseek-v3.2*.pdf`）

---

## 跨代「训练配方」要点速记

- **算法主线**：DPO（LLM）→ GRPO（DeepSeekMath 起，V2/Coder-V2/V3/R1/Prover/V3.2 全用）→ 纯 RL（R1-Zero）/RLVR 规则奖励（R1）。
- **架构主线**：MHA/GQA（LLM/Coder）→ DeepSeekMoE 细粒度+共享专家（MoE 起）→ MLA（V2 起）→ 无辅损均衡+MTP（V3）→ DSA 稀疏注意力（V3.2）。
- **精度主线**：bf16+fp32 累积（LLM）→ FP8 推理（V2）→ FP8 训练 E4M3 细粒度量化（V3）→ UE8M0 FP8 scale（V3.1）。
- **基座复用链**：Coder-Base-v1.5 → DeepSeekMath；V2 中间 ckpt → Coder-V2；V3-Base → R1/R1-Zero/Prover-V2-671B；V3 base → V3.1（续训）→ V3.1-Terminus → V3.2（DSA 续训）。
- **框架**：自始至终 **HAI-LLM**（自研）；V3 起 DualPipe + 自研 all-to-all kernel；RL 用 vLLM rollout + 解耦四模块框架。

### 主要官方来源 URL 汇总
- DeepSeek-LLM：https://arxiv.org/abs/2401.02954
- DeepSeekMoE：https://arxiv.org/abs/2401.06066
- DeepSeek-Coder：https://arxiv.org/abs/2401.14196
- DeepSeekMath（GRPO）：https://arxiv.org/abs/2402.03300
- DeepSeek-V2：https://arxiv.org/abs/2405.04434
- DeepSeek-Coder-V2：https://arxiv.org/abs/2406.11931
- DeepSeek-V3：https://arxiv.org/abs/2412.19437
- DeepSeek-V3 硬件：https://arxiv.org/abs/2505.09343
- DeepSeek-R1：https://arxiv.org/abs/2501.12948
- DeepSeek-Prover-V2：https://arxiv.org/abs/2504.21801
- DeepSeek-V3.2：https://arxiv.org/abs/2512.02556
- 官方 GitHub：https://github.com/deepseek-ai
- 官方 HF：https://huggingface.co/deepseek-ai
- 官方 API News：https://api-docs.deepseek.com/news/
