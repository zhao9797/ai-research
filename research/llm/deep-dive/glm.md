---
title: GLM / ChatGLM 家族训练配方深挖（智谱 Zhipu / Z.ai）
type: deep-dive
family: GLM / ChatGLM
org: 智谱 AI（Zhipu AI，2025 起品牌 Z.ai） + 清华大学 KEG
tags: [GLM, ChatGLM, GLM-130B, GLM-4, GLM-4.5, GLM-4.6, GLM-5, GLM-Z1, CogVLM, MoE, RL, slime, Muon, DSA]
created: 2026-06-18
updated: 2026-06-18
---

# GLM / ChatGLM 家族训练配方深挖

> 只收录一手官方来源（arXiv 原文 / 官方技术报告 PDF / 官方博客 / 官方 GitHub & HuggingFace 组织页 zai-org & THUDM）。
> 技术数字均抠自原文；官方未公开者明确标注「官方未公开」。

---

## 家族演进脉络

智谱/清华的路线与「GPT 式纯解码器 + 标准 RLHF」长期并行，核心是 **GLM（General Language Model，自回归空白填充 autoregressive blank infilling）**：

- **2021-03 GLM**（arXiv 2103.10360）：提出自回归空白填充目标，用一个目标统一 BERT(自编码)/GPT(自回归)/T5(编码器-解码器)，配 2D 位置编码。开源 GLM-10B/GLM-large。是后续一切的架构起点。
- **2022-10 GLM-130B**（arXiv 2210.02414, ICLR 2023）：1300 亿双语 base，400B token，DeepNorm+Post-LN+RoPE+GeGLU，首创无训练后 INT4 量化（4×3090 可推理）。
- **2023 ChatGLM-6B → ChatGLM2-6B → ChatGLM3-6B**：每约 3 个月一代，全部从头预训练；从 1T 双语 token 起步，引入 MQA/FlashAttention（2 代 32K 上下文）、原生 Function Call/Code Interpreter/Agent（3 代）。
- **2024-01~06 GLM-4 系列**（arXiv 2406.12793）：GLM-4(0116/0520)、GLM-4-Air(0605)、开源 GLM-4-9B(128K/1M)；约 10T token，No-bias-except-QKV + RMSNorm + SwiGLU + GQA + 2D-RoPE；All Tools 原生工具调用。
- **2024-12 / 2025 GLM-4-Plus、GLM-4V/CogVLM/CogAgent**：多模态与 GUI Agent 线（CogVLM 视觉专家、CogAgent GUI）。
- **2025-04 GLM-4-32B-0414 + GLM-Z1-0414**：首批 MIT 开源 32B/9B dense；GLM-4-0414(15T token base) + GLM-Z1(推理/RLVR) + GLM-Z1-Rumination(深度研究/带搜索)。
- **2025-07/08 GLM-4.5 / GLM-4.5-Air**（arXiv 2508.06471）：首个 MoE 旗舰，355B-A32B / 106B-A12B，23T token，hybrid reasoning（thinking/非 thinking），slime RL 框架、Muon 优化器、专家模型迭代 + GRPO。
- **2025-08 GLM-4.5V / GLM-4.1V-Thinking**（arXiv 2507.01006 系；本地 glm-4.5v.pdf）：以 GLM-4.5-Air 为 LLM 的 106B-A12B 多模态推理模型，AIMv2 视觉编码器 + RLCS。
- **2025-09 GLM-4.6**（z.ai blog）：GLM-4.5 同架构（355B-A32B），上下文 128K→200K，coding/推理增强；后续 GLM-4.6V/4.6V-Flash。
- **2026-02 GLM-5**（arXiv 2602.15763）：744B-A40B MoE，MLA(+Muon Split) → DSA 稀疏注意力，28.5T token，异步 agent RL，全国产芯片适配；迭代 GLM-5.1(2026-04)、GLM-5.2(2026-06，1M 上下文 + IndexShare)。

整体趋势：架构从 GLM blank-infilling → GPT 式 dense（GLM-4）→ MoE（GLM-4.5）→ MoE+稀疏注意力 DSA（GLM-5）；后训练从 SFT+RLHF（PPO/DPO）→ 专家模型迭代 + GRPO（reasoning/agentic/general RL）→ 异步 agent RL + on-policy 跨阶段蒸馏；基础设施自研 slime（Megatron 训练 + SGLang rollout）。

---

## 各代关键参数对比（仅列官方原文给出的数字）

| 模型 | 类型 | 总参/激活 | 层数 | 隐藏维 | 注意力(头/KV头) | MoE(总/激活/共享) | 训练 token | 上下文 | tokenizer/vocab |
|---|---|---|---|---|---|---|---|---|---|
| GLM-130B | dense (GLM) | 130B | 70 | 12288 | 96 头(MHA) | — | 400B | 2048 | icetk/150000 |
| ChatGLM-6B | dense (GLM) | 6.2B | 官方未公开 | 官方未公开 | MHA | — | ~1T | 2048 | 官方未公开 |
| ChatGLM2-6B | dense (GLM) | 6B | 官方未公开 | 官方未公开 | MQA | — | 1.4T | 32K (对话 8K) | 官方未公开 |
| ChatGLM3-6B | dense (GLM) | 6B | 官方未公开 | 官方未公开 | MQA | — | 官方未公开 | 8K/32K | 官方未公开 |
| GLM-4-9B | dense | 9B | 官方未公开 | 官方未公开 | GQA | — | ~10T | 8K→128K/1M | BBPE/150000 |
| GLM-4(0520) | dense | 官方未公开 | — | — | GQA | — | ~10T | 128K | BBPE/150000 |
| GLM-4-32B-0414 | dense | 32B | 官方未公开 | 官方未公开 | 官方未公开 | — | 15T | 32K/128K | 151552(HF) |
| GLM-Z1-32B/9B-0414 | dense 推理 | 32B/9B | 同 0414 base | — | — | — | (继承 base) | 32K/128K | 151552 |
| GLM-4.5 | MoE | 355B/32B | 3 dense+89 MoE(+1 MTP) | 5120 | 96/8(GQA,partial RoPE,QK-Norm) | 160/8/1 | 23T | 128K | 151552 |
| GLM-4.5-Air | MoE | 106B/12B | 1 dense+45 MoE(+1 MTP) | 4096 | 96/8(GQA) | 128/8/1 | 23T | 128K | 151552 |
| GLM-4.5V | MoE 多模态 | 106B/12B | (=GLM-4.5-Air)+ViT | — | (=Air) | (=Air) | 官方未公开 | 8K→32K→64K | 151552+特殊token |
| GLM-4.6 | MoE | ~357B/32B | 92(=3 dense+89 MoE) | 5120 | 96/8(GQA,partial RoPE 0.5) | 160/8/1 | 官方未公开(增量) | 200K | 151552 |
| GLM-5 | MoE+DSA | 744B/40B | 80 | 官方未公开 | MLA(head_dim 256, ÷3 头) | 256/8(每token)/官方未公开 | 28.5T | 200K (5.2:1M) | 官方未公开 |
| CogVLM-17B | VLM(视觉专家) | 17B(7B LM+visual expert) | (=Vicuna-7B) | — | — | — | 1.5B 图文对 | — | (=Vicuna) |

> 说明：GLM-4.5/4.5-Air 计参时含 MTP 层、不含词嵌入与输出层（原文 Table 1 注）。GLM-4.6 的 357B 为 HF config 推算（92 层、其余与 4.5 一致）。

---

## GLM (2021)：架构基石

- **来源**：arXiv 2103.10360（ACL 2022），GitHub THUDM/GLM。本地：`../../../sources/llm/2021/arxiv-2103.10360.pdf`
- **核心目标**：autoregressive blank infilling —— 随机遮盖连续 span，自回归还原；可同时覆盖 NLU、有条件生成、无条件生成。
- **结构创新**：2D 位置编码（span 在原文中的位置 + span 内位置）；短 span（偏 NLU）+ 长 span（偏生成）混合多任务预训练；span 乱序。
- 是 GLM-130B / ChatGLM 的架构起点。

---

## GLM-130B (2022)

- **来源**：arXiv 2210.02414（ICLR 2023），GitHub THUDM/GLM-130B。本地 PDF：`../../../sources/llm/2022/glm-130b.pdf`

### 架构
- 130B 参数，**70 层**（9×8−2，为平衡 pipeline 把首尾各砍 1 层），隐藏维 **12288**。
- 注意力头 96（MHA），目标用 GLM blank-infilling（[MASK] 短空白 + [gMASK] 长空白）。
- **DeepNorm + Post-LN**：经 30+ 次 100B 级失败实验后，Post-LN 用 DeepNorm 初始化才稳定（DeepNorm(x)=LayerNorm(α·x+Network(x))）。
- **RoPE**（而非 ALiBi）；FFN 用 **GLU（GeGLU/GeLU）**。
- tokenizer：基于 icetk（SentencePiece，25GB 中英语料），vocab **150000**（前 20000 为图像 token，其余文本）。

### 预训练数据
- 共 **400B token**（中英各约 200B）：英文 **1.2T Pile**(train split)、中文 **1.0T WudaoCorpora**，外加从网络爬取的 250G 中文（百科/QA/论坛等）。
- 5% token 用 **MIP（Multi-Task Instruction Pre-training）**（T0/DeepStruct 等指令数据集），95% 为自监督 blank infilling。

### 训练细节
- 算力：**96 台 DGX-A100(8×40G) = 768×A100**，集群可用期 **60 天**。
- 并行：**3D 并行 = 4-way TP × 8-way PP(PipeDream-Flush) × DP**。
- 精度：混合精度 FP16（Apex O2，forward/backward FP16、优化器状态 FP32）；因 40G A100 选 FP16 而非 BF16。
- global batch **4224**（warmup 192→4224，前 2.5% 样本）；序列长 2048；优化器 AdamW(β1=0.9, β2=0.95, wd=0.1)；LR warmup 1e-7→8e-5。
- **稳定性技巧**：embedding gradient shrink（α=0.1，显著抑制早期 loss 尖峰）；DeepNorm 抑制深层梯度爆炸；公开完整训练日志。
- **量化**：独有无训练后 **INT4** 量化（权重 4-bit），几乎无损（LAMBADA −0.74%），4×3090(24G) 或 8×2080Ti(11G) 可推理。

### 对齐（后续）
- 先做指令微调；ChatGPT 后用 SFT + RLHF（prompt-response 由开发者从头标注），2023-03-14 上线 ChatGLM-130B。

---

## ChatGLM-6B / ChatGLM2-6B / ChatGLM3-6B (2023)

> 来源：官方 GitHub README（THUDM/ChatGLM-6B、ChatGLM2-6B、ChatGLM3）+ GLM-4 技术报告（2406.12793）第 2 节。本地：`2023/files/chatglm-6b-readme.md`、`chatglm2-6b-readme.md`、`chatglm3-readme.md`。架构细节（层/维/头）官方均未单独披露。

### ChatGLM-6B（2023-03）
- 架构：GLM blank-infilling，6.2B；上下文 2048。
- 预训练：约 **1T 中英双语 token**。
- 对齐：SFT + 反馈自助（feedback bootstrap）+ RLHF（GLM-4 报告：首代 prompt-response 多由开发者标注）。
- 部署：FP16 ~13GB、INT8 ~8GB、INT4 ~6GB；附 P-Tuning v2 高效微调。

### ChatGLM2-6B（2023-06）
- 预训练 **1.4T 中英 token** + 人类偏好对齐。
- **MQA（Multi-Query Attention）**：推理 +42%、显存下降（INT4 下 6G 对话长度 1K→8K）。
- 基于 **FlashAttention** 上下文 2K→32K（对话阶段 8K 训练）；另发 ChatGLM2-6B-32K。
- 相对初代：MMLU +23%、GSM8K +571%、BBH +60%（GLM-4 报告）。

### ChatGLM3-6B（2023-10）
- 基座 ChatGLM3-6B-Base：更多样数据 + 更充分训练步数 + 更优策略，10B 以下最强（GLM-4 报告：曾在多代探索中训练 1.5B/3B/12B/32B/66B/130B 以建立 scaling law）。
- 全新 Prompt 格式（system/user/assistant/observation 角色），**原生 Function Call + Code Interpreter + Agent**。
- 开源：ChatGLM3-6B / -Base / -32K。

---

## GLM-4 系列 (2024)

- **来源**：arXiv 2406.12793《ChatGLM: A Family of LLMs from GLM-130B to GLM-4 (All Tools)》。本地 PDF：`../../../sources/llm/2024/glm-4.pdf`。开源 GLM-4-9B：GitHub/HF THUDM。

### 架构（GLM-4 采用的设计）
- 相对 GLM-130B 的改动：
  - **No Bias Except QKV**：除注意力 QKV 外去掉所有 bias（提速，长度外推略好）。
  - **RMSNorm + SwiGLU**（替代 LayerNorm + ReLU）。
  - **2D-RoPE**（把 RoPE 扩到二维以配合 GLM 的 2D 位置）。
  - **GQA 替代 MHA**：降 KV cache；GQA 参数少，于是把 FFN 放大，d_ffn = 隐藏维 ×10/3。
- tokenizer：byte-level BPE，分别学中文/多语 token 后与 tiktoken 的 cl100k_base 合并为统一 vocab **150000**。
- 上下文扩展链：2K(ChatGLM)→32K(2/3 代)→128K & 1M(GLM-4)：位置编码扩展 + 长文本继续训练 + 长上下文对齐（LongAlign）。
- GLM-4-9B：隐藏维 8192 训练上下文，pre-train ~10T 多语 token，后训练用与 GLM-4(0520) 相同 pipeline/数据；额外发 GLM-4-9B-Chat-1M。

### 预训练数据
- 多语（主英中）+ 24 种语言少量；来源：网页、Wikipedia、书籍、代码、论文。
- pipeline 三段：**去重（精确 + 模糊）→ 过滤（网页去噪：冒犯语言/占位文本/源码等）→ tokenization**。
- 最终对高质量/教育性来源（书籍、Wikipedia）**re-weight 上采样**。
- 总量约 **10T token**。

### SFT / 对齐
- 多阶段后训练：SFT + RLHF。SFT 强调用真实人类 prompt 与交互（而非模板/模型生成）。
- 首代 prompt-response 多为开发者标注；后续为内部标注 + 第三方专有数据（严格质控），多维评分（安全/事实/相关/有用/人类偏好）。
- **配套技术（官方各有论文）**：
  - ChatGLM-RLHF：把 **PPO + DPO** 用于 LLM 对齐（官方实践）。
  - Self-Contrast：免人工偏好，目标 LLM 自生成大量负样本做 RLHF。
  - ChatGLM-Math：self-critique 选数据提升数学。
  - LongAlign：长上下文对齐配方（达 128K）。
  - AgentTuning（AgentInstruct 数据集）、APAR（并行自回归生成加速）。
- **All Tools**：进一步对齐，自主理解意图、规划、调用 web 浏览器 / Python 解释器 / 文生图 / 自定义函数；GLMs 平台支持自建 agent。
- 评测部署：BF16。

### AI infra
- 框架细节官方未在该报告披露算力/卡时/并行细节（GLM-4 报告偏能力评测）。

---

## GLM-4-32B-0414 + GLM-Z1-0414 (2025-04，首批 MIT dense 开源)

- **来源**：官方 HF model card `zai-org/GLM-4-32B-0414`、`zai-org/GLM-Z1-32B-0414`、`zai-org/GLM-Z1-9B-0414`、`zai-org/GLM-Z1-Rumination-32B-0414`；HF config（vocab 151552）。z.ai 官方博客。

### GLM-4-32B-Base-0414（base）
- 32B；**预训练 15T 高质量数据**，含大量「推理型合成数据」，为后续 RL 打基础。
- 后训练：对话场景人类偏好对齐 + **拒绝采样 + RL**，强化指令遵循、工程代码、function calling（agent 原子能力）。
- 官方称：部分基准（代码生成/特定 QA）可比肩 GPT-4o、DeepSeek-V3-0324(671B)。
- 架构（HF config glm4）：vocab 151552；层/维官方未在 card 文字披露（按 glm4 dense 配置）。

### GLM-Z1-32B-0414（推理模型）
- 基于 GLM-4-32B-0414，经 **cold start + 扩展 RL**，在数学/代码/逻辑任务上继续训练，数学与复杂任务能力显著提升。
- 训练中额外引入 **基于成对排序反馈（pairwise ranking）的通用 RL** 提升通用能力。

### GLM-Z1-Rumination-32B-0414（深度研究 / 对标 Deep Research）
- 「rumination（反复思考）」深度推理：比常规深思更长更深，处理开放复杂问题。
- 训练：**端到端 RL 扩展**，奖励来自 ground-truth 答案或 rubric（评分量表）；深思过程中可调用搜索工具。

### GLM-Z1-9B-0414
- 用上述全部技术训练的 9B；同尺寸开源中数学推理/通用任务表现领先。

> 注：0414 系列官方未公开层/隐藏维/头数/具体 RL 算法名（PPO/GRPO）与 RL token 量等细节，以 model card 文字描述为准。

---

## GLM-4.5 / GLM-4.5-Air (2025-07/08)

- **来源**：arXiv 2508.06471《GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models》。本地 PDF：`../../../sources/llm/2025/glm-4.5.pdf`（另 `themes/agentic/files/glm-4.5-2508.06471.pdf`）。GitHub/HF zai-org/GLM-4.5。

### 架构（原文 Table 1）
| | GLM-4.5 | GLM-4.5-Air |
|---|---|---|
| 总参 | 355B | 106B |
| 激活参 | 32B | 12B |
| Dense 层 | 3 | 1 |
| MoE 层 | 89 | 45 |
| MTP 层 | 1 | 1 |
| 隐藏维 | 5120 | 4096 |
| Dense FFN 维 | 12288 | 10944 |
| MoE FFN 维 | 1536 | 1408 |
| 注意力 head dim | 128 | 128 |
| 注意力头 | 96 | 96 |
| KV 头 | 8 | 8 |
| 总专家 | 160 | 128 |
| 每 token 激活专家 | 8 | 8 |
| 共享专家 | 1 | 1 |
| QK-Norm | 是 | 否 |

- MoE：**loss-free balance routing（无辅助损失负载均衡）+ sigmoid 门控**。
- 设计取向：相对 DeepSeek-V3/Kimi-K2 **降宽（隐藏维、路由专家数）增深（层数）**，因更深模型推理更强。
- 注意力：**GQA + partial RoPE**；**2.5 倍注意力头**（5120 维配 96 头）——虽不降训练 loss，但持续提升 MMLU/BBH 等推理基准；加 **QK-Norm** 稳定 attention logits。
- **MTP 层用作 MoE 层**支持推理期投机解码。
- vocab 151552（HF config），上下文 128K。

### 预训练数据（23T token）
- 来源：网页、社媒、书籍、论文、代码仓库。
- **Web**：仿 Nemotron-CC 分质量桶；最高质桶训练中贡献 **>3.2 epoch**；丢弃最低桶；模板批量生成网页 MinHash 去不掉，额外用 **SemDedup（文档 embedding）** 去重。
- **多语**：自爬 + FineWeb-2；教育价值分类器上采样高质量。
- **代码**：GitHub 等；规则过滤 + 语言专属质量模型分三档（高/中/低），上采样高质、剔除低质；全部源码用 **FIM(Fill-In-the-Middle)** 目标；代码相关网页两阶段检索（HTML code 标签 / FastText 分类器 → 专用质量模型分档）+ 细粒度 parser 重解析保格式。
- **数学&科学**：LLM 给「教育性比例」打分 → 训练小分类器预测 → 超阈值上采样。
- 两阶段预训练：①主训网页通用文档；②上采样 GitHub 源码 + 代码/数学/科学网页。

### Mid-training（提升推理 & agentic）
中等规模领域数据（含指令数据）：
- **Repo-level 代码训练**：同仓代码文件拼接学跨文件依赖；加入模型过滤的 issues/PR/commit（diff 形式拼接），序列长 4K→32K。
- **合成推理数据训练**（约 500B）：数学/科学/竞赛代码问答，用推理模型合成推理过程。
- **长上下文 & Agent 训练**（约 100B）：32K→128K，上采样长文档 + 大规模合成 agent 轨迹。
- 图示数据规模：通用预训练 15T + 代码&推理继续预训练 7T + repo-level 代码 500B + 合成推理 500B + 长上下文&agent 100B。
- 预训练阶段不用 best-fit packing（随机截断当数据增强）；mid-training 用 best-fit packing 避免截断推理/repo 代码。

### 训练超参
- **优化器：Muon**（除 word embedding/bias/RMSNorm 权重外全部用）；Newton-Schulz 迭代 N=5，动量 μ=0.95，update RMS 缩放至 0.2（收敛快、容大 batch）。
- LR：**cosine decay**（非 WSD，WSD 在 SimpleQA/MMLU 上欠拟合）；warmup 0→2.5e-4，衰减至 2.5e-5（至 mid-training 结束）。
- **batch warmup**：前 500B token 内 16M→64M token，之后恒定。
- weight decay 0.1，无 dropout。
- 序列长：pre-train 4096；mid-training 扩到 32768 与 131072。32K 起 **RoPE base 10000→1,000,000**。
- loss-free routing：bias 更新率前 15T token 为 0.001，之后 0.0；额外序列级均衡 aux loss 权重 0.0001。
- MTP loss 权重 λ：前 15T 为 0.3，之后 0.1。
- 算力/卡时/集群规模：**官方未公开**（pre-train 精度 BF16/FP8 也未明示；仅 RL infra 提到 FP8 rollout）。

### 后训练：专家模型迭代（两阶段）
- **Stage 1 专家训练**：分别训 Reasoning / Agent / General chat 三个专家（各自 SFT cold start + 专家 RL）。
- **Stage 2 统一训练**：**自蒸馏（self-distillation）** 把多专家融成一个 hybrid reasoning 通用模型（thinking + 直答两种模式）。

#### SFT
- Cold-start SFT：小批带长 CoT 的 SFT 数据给每个专家打底。
- Overall SFT：百万级样本（reasoning/general chat/agentic/long-context），最大上下文 128K；混合「带完整推理」与「无显式思考」数据 → hybrid reasoning。
- **Function call 模板**：用 XML 风格特殊 token 标签包裹 key/value，大幅减少代码段转义负担（不损 function call 性能）；含 `<tool_call>/<arg_key>/<arg_value>/<think>` 等。
- **拒绝采样**多级过滤：去重复/过短/截断/格式非法 → 客观题正确性校验 → reward model 过滤主观题 → tool 调用校验是否到达期望终态。
- Prompt 选择 + 回复级缩放：去掉响应长度后 50% 的简单 prompt（数学/科学 +2~4%，数据减半）；难 prompt 每条生成 4 回复再 +1~2%。
- 自动 agentic SFT 数据构造：框架&工具收集（真实 API + MCP + LLM 模拟工具）→ 任务合成 → 轨迹生成（LLM + 用户模拟器）→ 多 judge agent 过滤只留成功轨迹。

#### Reasoning RL
- 算法：**GRPO 框架，去掉 KL loss 项**。
- **难度课程（两阶段）**：先中等难度（samples_per_prompt=16），后切极难题（pass@8=0 但 pass@512>0，samples_per_prompt=512），第二阶段题严格取自「已验证正确答案」池；AIME24 81.8→83.4。
- **单阶段 64K 输出长度 RL**（非多阶段渐进增长）：多阶段会让模型「忘掉」长上下文不可逆掉点；直接 64K 持续提升。
- **动态采样温度**：reward 稳定即判为收敛 → 升温增多样性；用 held-out 验证集控质，取「掉点 <1%」的最大温度。
- **Code RL**：token-weighted mean loss（优于 sequence-mean，收敛更快、抑制 base-case 退化）。
- **Science RL**：只用专家验证的多选题（优于混质数据），GPQA-Diamond 62.9→65.8。

#### Agentic RL
- 数据：web-search（知识图谱多跳自动合成 + 人在环抽取/选择性混淆）；SWE（GitHub PR/issue + 可执行单测，硬化 sandbox 分布式隔离）。
- 算法：group-wise policy optimization（仅对模型生成 token 优化，忽略环境反馈 token）。
- **结果监督 + process 格式惩罚**：web 用最终答案正确率；coding 用可验证测试用例；tool 格式错则中止并给 0 reward。
- **迭代自蒸馏**：cold-start 模型先 RL → 用 RL 后模型回答替换 cold-start 数据做更优 SFT → 再 RL，难度渐增。
- 测试时计算按「交互轮数」扩展（BrowseComp 随 browsing effort 平滑提升）。

#### General RL
- 多源反馈：rule-based + RLHF（人类偏好 RM）+ RLAIF（model-based）。
- Holistic RL：约 5000 prompt（7 一级/33 二级/139 三级类目），人+AI 反馈混合。
- Instruction Following RL：7 大/151 小约束类型分类法；deterministic 规则 + RM + critique model 混合反馈，GRPO 下抑制 reward hacking（SysBench-ISR 升）。
- Function Calling RL：step-wise 规则 RL（严格 reward：格式正确且与 ground-truth 完全匹配才给 1）+ end-to-end 多轮 RL（先训专家再蒸馏）。
- Pathology RL（最后阶段）：针对语言混杂/重复/格式错，curate 高触发 prompt 集做高效惩罚。

### RL infra（slime，自研开源）
- **slime**（github.com/THUDM/slime）：Training(Megatron) + Rollout(SGLang + Router) + Data Buffer 三模块。
- 支持 **colocated 同步**（reasoning/math/code，配动态采样减 GPU 空闲）与 **disaggregated 异步**（agentic/SWE，rollout 直连 agent 环境）双模式，基于 Ray 调度。
- **混合精度**：训练 BF16、**rollout 推理 FP8**（每次策略更新前对参数做在线 block-wise FP8 量化）。
- Agent RL：高并发 Docker 隔离环境 + 全异步训练 loop（rollout/training GPU 分离，定期同步权重）+ 统一 HTTP 端点 + 中心化 data pool。

---

## GLM-4.5V / GLM-4.1V-Thinking (2025-08，多模态)

- **来源**：本地 PDF `../../../sources/llm/2025/glm-4.5v.pdf`（报告同时涵盖 GLM-4.1V-9B-Thinking、GLM-4.5V-106B-A12B、GLM-4.6V-Flash-9B、GLM-4.6V）。HF zai-org/GLM-4.5V。

### 架构
- 三件套：**ViT 视觉编码器 + MLP adapter + LLM 解码器**。
- 视觉编码器初始化用 **AIMv2-Huge**；LLM：9B 版用 GLM-4 系列 9B，**GLM-4.5V/4.6V 用 GLM-4.5-Air（106B-A12B）**。
- ViT 仿 Qwen2-VL：2D 卷积换 **3D 卷积**（视频时序 2× 下采样，单图复制保一致）；ViT 自注意力加 **2D-RoPE**（支持任意分辨率/极端长宽比 >200:1、>4K）；位置嵌入双三次插值适配变分辨率。
- LLM 侧把 RoPE 扩到 **3D-RoPE**；视频每帧插时间戳字符串 token。
- 特殊 token：`<think></think> <answer></answer> <|begin_of_box|><|end_of_box|>` 加入 vocab（GLM-4.5V 去掉 answer 标签）。

### 多模态预训练数据
- 图文 caption：从 >100 亿图文对起，规则过滤（最小分辨率/纯色检测/caption 长度/图级去重）→ CLIP-Score>0.3 相关性过滤 → 概念均衡重采样（仿 MetaCLIP）→ 事实导向重写 caption。
- 交错图文：MINT/MMC4/OmniCorpus 多阶段清洗 + 高知识密度图分类器；>1 亿数字化书籍（STEM）深度 PDF 解析。
- OCR：**2.2 亿图**（合成文档 + 自然场景 PaddleOCR + arXiv 学术文档 Nougat 式）。
- Grounding：自然图 4000 万（LAION-115M + GLIPv2）；GUI（CommonCrawl 截图 + Playwright 解析 DOM bbox）>1.4 亿 QA。
- Instruction tuning：5000 万样本（细粒度 taxonomy + 复杂场景增强 + 数据污染检查）。

### 训练 recipe
- 多模态预训练：GLM-4.5V/4.6V 设 EP=8、PP=4；loss-free routing（router bias 1e-3，序列级 aux loss 1e-4）；序列长 8192，global batch 1536，**120000 步**（不含视频）。
- 长上下文继续训练：加视频 + >8K 交错数据，序列长升 32768、CP=4，再 10000 步（batch 1536）；GLM-4.6V 扩 131072（再 2000 步，batch 128）。
- **SFT**：长 CoT 语料做 cold start（对齐思考/回答风格，刻意不做 short-CoT SFT）；标准化 `<think>/<answer>` 格式 + boxed 答案。
- **RL**：**RLCS（Reinforcement Learning with Curriculum Sampling）** = 课程学习 + 难度感知采样，结合 **RLVR（可验证奖励）+ RLHF**，跨多模态域大规模 RL；强调精准 reward 系统（域专属）。

---

## GLM-4.6 (2025-09)

- **来源**：官方博客 `https://z.ai/blog/glm-4.6`（本地 `2025/files/glm-4.6-blog.md`）；HF zai-org/GLM-4.6（config.json）；技术细节复用 GLM-4.5 报告 arXiv 2508.06471。
- **架构**：与 GLM-4.5 同（HF config 实测）：隐藏维 5120、96 头 / 8 KV、head_dim 128、partial_rotary_factor 0.5、160 路由专家 / 每 token 8 激活 / 1 共享、MoE FFN 1536、首 3 层 dense、**num_hidden_layers 92**、vocab 151552、rope_theta 1,000,000。总参约 357B / 激活 32B。
- **相对 GLM-4.5 改进**（博客）：
  - 上下文 **128K→200K**（config max_position 202752）。
  - 代码能力提升（Claude Code/Cline/Roo/Kilo 实测更好、前端更精致）。
  - 推理增强，**推理中支持工具调用**。
  - agent/搜索能力更强；写作更贴人类偏好、角色扮演更自然。
  - token 效率：完成任务比 GLM-4.5 少约 15% token。
- CC-Bench 扩展版：对 Claude Sonnet 4 近乎打平（48.6% 胜率）。
- 训练数据/算力增量官方未单列；推理框架 vLLM/SGLang，与 GLM-4.5 同推理方式。

---

## GLM-5 / GLM-5.1 / GLM-5.2 (2026)

- **来源**：arXiv 2602.15763《GLM-5: from Vibe Coding to Agentic Engineering》（GLM-5-Team，187 作者）。本地 PDF：`../../../sources/llm/2026/glm-5.pdf`。GLM-5.2 model card：`2026/files/glm-5.2-modelcard.md`。GitHub/HF zai-org/GLM-5。

### 架构
- **744B 总参 / 40B 激活**（GLM-4.5 的两倍总参）；**256 专家**、每 token 激活 8（共享专家数官方未在正文单列）；**层数降到 80**（减少 EP 通信开销）。
- **注意力：MLA（Multi-latent Attention）+ Muon Split**：原 Muon 对 W_UQ/W_UK/W_UV 整体正交化 → 拆成各头小矩阵分别正交化，使 MLA 追平 GQA-8（且 attention logits 训练全程稳定、无需 clip）。MLA head dim 192→**256**、头数 ÷3（保持训练计算/参数不变、降 decode 计算）。
- **MTP 参数共享**：训练时共享 3 个 MTP 层参数预测后 3 token（draft 模型显存与 DeepSeek-V3 单 MTP 一致但接受率更高；接受长度 GLM-5 2.76 > DeepSeek-V3.2 2.55，4 步投机）。
- **DSA（DeepSeek Sparse Attention）**：从 mid-training 末的 dense base 做「**继续预训练**」引入——两阶段 dense warm-up（1000 步，每步 14×202752 token，max LR 5e-3，仅训 indexer）+ sparse adaptation（沿用 mid-training 数据，仅 **20B token**，远小于 DeepSeek-V3.2 的 943.7B 即可追平 MLA）；DSA 对长序列降注意力计算约 1.5–2×，128K 上下文 GPU 成本减半，且 lightning indexer token 级稀疏「无损」（可全层用）。
- 高效注意力消融（基于 GLM-9B）：搜索式 SWA pattern（beam=8）显著优于固定 interleave；SimpleGDN 复用预训练权重最佳；但所有高效注意力在细粒度检索仍有损，DSA 因构造无损胜出。

### 预训练数据（28.5T token）
- base 训练共 **28.5T token**（图示 Base 始于 27T），早期偏重代码与推理。
- **Web**：在 GLM-4.5 pipeline 上加 DCLM 句嵌入分类器聚合更多高质数据；World Knowledge 分类器（Wikipedia + LLM 标注优化）从中低质数据蒸长尾知识。
- **Code**：刷新主流代码平台快照 + 更多含代码网页，模糊去重唯一 token **+28%**；修 Software Heritage 元数据对齐、更准语言分类；为低资源语言（Scala/Swift/Lua 等）训专属分类器。
- **数学&科学**：精修网页抽取 + PDF 解析；LLM 打分只留最教育性；长文档用 chunk-and-aggregate 打分；严格剔除合成/AI 生成/模板数据。

### Mid-training
- 上下文三段渐进：**32K(1T token) → 128K(500B) → 200K(50B)**（GLM-4.5 上限 128K，新增 200K 段）。
- 软件工程数据：放宽 repo 级筛选得约 **1000 万 issue–PR 对**，强化单 issue 级质量过滤；issue–PR 部分约 **160B unique token**。
- 长上下文：自然（书/论文/文档，PPL+去重+长度多级过滤）+ 合成（仿 NextLong/EntropyLong，交错 packing 缓解 lost-in-the-middle；200K 段加少量 MRCR-like 数据）。

### 训练基础设施
- **内存**：灵活 MTP 放置（输出层与主输出层共置末段）、Pipeline ZeRO2 梯度分片、Muon 分布式优化器零冗余通信、pipeline 激活 offload 到 host、序列分块输出投影。
- **并行**：deferred 权重梯度计算减 pipeline 气泡；长序列 workload-aware 重排 + 动态注意力重分配 + 灵活 CP 分组 + 分层 all-to-all。
- **INT4 QAT**：SFT 阶段做 INT4 量化感知训练，自研量化 kernel 保证训练/推理 bitwise 一致。
- 精度（rollout）：**FP8**；训练精度（BF16/FP8）、卡时/集群规模官方未明示。
- **国产芯片**：首日全栈适配华为昇腾、摩尔线程、海光、寒武纪、昆仑芯、沐曦、燧原 7 大平台（kernel→推理框架）。

### 后训练（渐进对齐：SFT → Reasoning RL → Agentic RL → General RL → 跨阶段蒸馏）
- **SFT**：相对 GLM-4.5 大幅扩 Agent & Coding 数据；上下文扩到 **202752**；三种思考模式：Interleaved Thinking（每次响应/工具调用前思考）、Preserved Thinking（coding agent 跨轮保留思考块，复用推理）、Turn-level Thinking（按轮开关思考）。错误轨迹片段保留但 loss mask（学纠错不强化错误）。
- **Reasoning RL**：GRPO + **IcePop**（缓解 train/infer 分布不匹配，区分 π_train 与 π_infer，去 KL 项）；β=2、ε_low=0.2、ε_high=0.28；**全 on-policy，group size 32、batch 32**。混合四域（数学/科学/代码/TIR），二元 outcome reward；难度过滤（GLM-4.7 很难做对但强 teacher 如 GPT-5.2/Gemini-3-Pro 能做对）。
- **DSA RL 洞见**：indexer top-k（k=2048）replay 不现实 → 用**确定性 torch.topk**（非确定性 CUDA top-k 会几步内崩溃、熵骤降）；RL 期默认**冻结 indexer**。
- **Agentic RL**：全异步解耦框架（中心 Multi-Task Rollout Orchestrator）；TITO（Token-in-Token-out）gateway 消除 re-tokenize 失配；**Direct Double-sided Importance Sampling**（token 级 clip 控 off-policy 偏差，不追历史 checkpoint）；DP-aware 路由提升 KV-cache 复用；可验证环境覆盖 >1 万真实 SWE/terminal/多跳搜索。group-wise policy optimization（仅优化模型生成 token）。
- **General RL**：三维目标（foundational correctness / emotional intelligence / task-specific quality）；混合 reward = 规则 + ORM + GRM；引入专家人类回答作风格锚（防「模型味」）。
- **On-Policy 跨阶段蒸馏（最后阶段）**：以各前序阶段最终 checkpoint 为 teacher，advantage 替换为 teacher/student log-prob 差（stop-grad）；group size=1、**batch 1024** 增吞吐。

### RL 基础设施（slime）
- 继续用 **slime**：高度可定制 rollout（多轮/工具/环境反馈/verifier 分支）+ HTTP 服务化 rollout；尾延迟优化（多节点 EP64/DP64 over 8 节点供 KV-cache、FP8 rollout、MTP 对小 batch decode 收益大、PD 解耦防 prefill/decode 干扰）；heartbeat 故障容错。
- 异步 agent RL：训练/推理引擎不同 GPU；rollout 持续生成，达阈值发训练引擎；每 K 次梯度更新同步权重，控 policy lag。

### GLM-5.1 / GLM-5.2（迭代）
- **GLM-5.1**：HF 2026-04（HLE 31、SWE-bench Pro 58.4 等，见 5.2 card 对比列）。
- **GLM-5.2**（HF 2026-06-16，MIT）：旗舰长程任务模型，首次在**实打实 1M token 上下文**稳定支撑长程工作。
  - **IndexShare**（arXiv 2603.12201）：每 4 层稀疏注意力**复用同一 indexer**，1M 上下文下每 token FLOPs 降 **2.9×**；改进 MTP 层用于投机解码，接受长度提升最多 **20%**。
  - 多档 thinking effort 平衡性能/延迟。
  - 评测（节选）：AIME 2026 99.2、HLE 40.5 / HLE(w/Tools) 54.7、GPQA-Diamond 91.2、SWE-bench Pro 62.1、Terminal Bench 2.1 81.0。
  - 部署：SGLang/vLLM/Transformers/KTransformers，及 Ascend NPU（vLLM-Ascend/xLLM/SGLang）。
  - 总参俗称约 744B/753B 级（与 GLM-5 同族 MoE+DSA）。

---

## CogVLM / CogAgent（视觉 / GUI Agent 线，2023）

- **来源**：CogVLM arXiv 2311.03079（本地 `2023/files/cogvlm.pdf`）；CogAgent arXiv 2312.08914（本地 `2023/files/cogagent.pdf`、`themes/agentic/files/cogagent-2312.08914.pdf`）。

### CogVLM-17B
- 架构四件套：ViT 编码器 + MLP adapter（2 层 SwiGLU）+ 预训练 LLM（**Vicuna-1.5-7B**）+ **visual expert module**（每层加一套 QKV + MLP，形状同 LLM 并由其初始化；图文深度对齐，参数翻倍但 FLOPs 不变）。
- ViT：**EVA2-CLIP-E**（去掉最后一层 CLS 聚合层）；所有图像 token 在 LLM 内共享同一 position id。
- 预训练数据：LAION-2B + COYO-700M，清洗（去坏链/NSFW/噪声 caption/政治偏见/长宽比 >6 或 <1/6）后约 **15 亿图**；另自建 **4000 万图视觉 grounding 数据集**（spaCy 抽名词 + GLIPv2 预测 bbox）。
- 17B = 7B LM + ~10B visual expert（合 17B）；开源 SFT 数据集。

### CogAgent-18B（GUI Agent）
- 基于 CogVLM 增高分辨率分支（小型高分辨率 cross-attention 编码器），支持 1120×1120 截图理解，面向 GUI 操作（识别图标/按钮/文本）；详见本地 cogagent.pdf。

---

## 跨代要点速记

- **架构主线**：blank-infilling GLM（130B/ChatGLM）→ GPT 式 dense（GLM-4：no-bias-except-QKV/RMSNorm/SwiGLU/GQA/2D-RoPE）→ MoE（GLM-4.5：loss-free routing + sigmoid 门 + 降宽增深 + 2.5× 头 + QK-Norm + MTP）→ MoE + 稀疏注意力（GLM-5：MLA+Muon Split → DSA；GLM-5.2 IndexShare）。
- **tokenizer/vocab**：130B icetk 150000 → GLM-4 BBPE+cl100k 合并 150000 → GLM-4.5/4.6 vocab 151552。
- **优化器**：130B/GLM-4 AdamW；**GLM-4.5/GLM-5 改用 Muon**（GLM-5 加 Muon Split 适配 MLA）。
- **RL 演进**：RLHF(PPO+DPO)/Self-Contrast（GLM-4）→ 专家迭代 + **GRPO(去 KL)** 三阶段 reasoning/agentic/general RL + 自蒸馏（GLM-4.5）→ **GRPO+IcePop** + 异步 agent RL + on-policy 跨阶段蒸馏（GLM-5）；多模态用 **RLCS + RLVR + RLHF**。
- **自研基础设施**：**slime**（Megatron 训练 + SGLang rollout + Data Buffer，BF16 训练 / FP8 rollout，同步 colocated 与异步 disaggregated 双模式）。

---

## 来源清单（一手）

### arXiv 原文 / 官方技术报告（含本地 PDF）
- GLM（2103.10360）：https://arxiv.org/abs/2103.10360 — 本地 `2021/files/arxiv-2103.10360.pdf`
- GLM-130B（2210.02414）：https://arxiv.org/abs/2210.02414 — 本地 `2022/files/glm-130b.pdf`
- ChatGLM/GLM-4 报告（2406.12793）：https://arxiv.org/abs/2406.12793 — 本地 `2024/files/glm-4.pdf`
- GLM-4.5（2508.06471）：https://arxiv.org/abs/2508.06471 — 本地 `2025/files/glm-4.5.pdf`、`themes/agentic/files/glm-4.5-2508.06471.pdf`、`themes/post-training/files/glm-4.5.pdf`
- GLM-4.5V / GLM-4.1V-Thinking 报告：本地 `2025/files/glm-4.5v.pdf`（arXiv GLM-4.1V-Thinking 2507.01006）
- GLM-5（2602.15763）：https://arxiv.org/abs/2602.15763 — 本地 `2026/files/glm-5.pdf`
- IndexShare（GLM-5.2）：https://arxiv.org/abs/2603.12201
- CogVLM（2311.03079）：本地 `2023/files/cogvlm.pdf`
- CogAgent（2312.08914）：https://arxiv.org/abs/2312.08914 — 本地 `2023/files/cogagent.pdf`、`themes/agentic/files/cogagent-2312.08914.pdf`

### 官方博客 / GitHub / HuggingFace（zai-org / THUDM）
- GLM-4.6 博客：https://z.ai/blog/glm-4.6 — 本地 `2025/files/glm-4.6-blog.md`
- GLM-4.6 model card/config：https://huggingface.co/zai-org/GLM-4.6
- GLM-4.5 GitHub：https://github.com/zai-org/GLM-4.5 ；slime：https://github.com/THUDM/slime
- GLM-5 GitHub：https://github.com/zai-org/GLM-5 ；GLM-5.2 model card：https://huggingface.co/zai-org/GLM-5.2 — 本地 `2026/files/glm-5.2-modelcard.md`
- GLM-4-32B-0414 / GLM-Z1-32B-0414 / GLM-Z1-Rumination-32B-0414 / GLM-Z1-9B-0414 model card：https://huggingface.co/zai-org/GLM-4-32B-0414 等
- ChatGLM-6B：https://github.com/THUDM/ChatGLM-6B — 本地 `2023/files/chatglm-6b-readme.md`
- ChatGLM2-6B：https://github.com/THUDM/ChatGLM2-6B — 本地 `2023/files/chatglm2-6b-readme.md`
- ChatGLM3：https://github.com/THUDM/ChatGLM3 — 本地 `2023/files/chatglm3-readme.md`

---

## 主要 gap（官方未公开或本次未查到）

- **算力/集群/卡时/FLOPs**：除 GLM-130B（768×A100、60 天）外，GLM-4 / GLM-4.5 / GLM-4.6 / GLM-5 均未公开 GPU 型号、卡数、卡时或总 FLOPs。
- **预训练精度**：GLM-4.5/GLM-5 正文只明示 RL rollout 用 FP8、训练 BF16（RL infra），pre-train 主精度（BF16 vs FP8）未单独声明。
- **并行配置（pre-train）**：GLM-4.5 pre-train 的 TP/PP/DP/EP 具体并行度未给（仅 GLM-4.5V 给 EP=8/PP=4/CP=4、GLM-5 给方法但无具体并行度数字）。
- **ChatGLM-6B/2/3 架构内参**：层数/隐藏维/头数/具体 tokenizer 官方 README 未列；ChatGLM3 训练 token 量未公开。
- **GLM-4-0414/GLM-Z1 细节**：层/维/头、具体 RL 算法名（PPO/GRPO）、cold start 与 RL 的 token 量、偏好数据规模均未在 model card 公开。
- **GLM-5 内参**：隐藏维、共享专家数、Muon LR schedule 具体值、各 RL 阶段 token 量、总卡时未公开。
- **GLM-4.6 增量**：相对 GLM-4.5 新增训练 token 量、数据配比变化、RL 配方差异未公开（博客仅给能力/上下文/效率结论）。
- **GLM-4.5 数据语言/领域百分比**：只给质量桶/上采样策略与各 mid-training 阶段 token 量，未给「中/英/代码/数学」精确占比百分数。
- **GLM-5.1**：无独立技术报告，仅在 GLM-5.2 card 对比表出现分数。
