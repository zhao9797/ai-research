---
title: "GLM-5: from Vibe Coding to Agentic Engineering"
org: 智谱 Z.ai (Zhipu / GLM-5-Team)
country: China
date: 2026-02
type: paper
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://arxiv.org/abs/2602.15763
pdf_url: https://arxiv.org/pdf/2602.15763
github_url: https://github.com/zai-org/GLM-5
downloaded: [arxiv-2602.15763-glm-5.pdf, glm-5.pdf, glm-5.2-modelcard.md]
---

## 一句话定位
智谱 GLM-5 旗舰基座技术报告（arXiv 2026-02-17，GLM-5-Team），把 "vibe coding" 推进到 "agentic engineering"。本页按一手报告全文（§1–4）整理：架构(DSA/MLA-Muon Split/MTP) · 数据 · 训练 infra · **完整后训练管线** · agentic engineering · 评测。

## 架构
- **规模**：256 专家、80 层、**744B 总参 / 40B 激活**（GLM-4.5 的 2×：355B/32B）。MoE。
- **MLA + Muon Split**：对 W^UQ/W^UK/W^UV 按头拆分后各自做矩阵正交化，使 MLA 在 Muon 优化器下匹配 GQA-8；GLM-5 注意力 logits 预训练全程稳定、无需 clipping。**MLA-256**：head_dim 192→256、头数 ÷3，保持训练算力与参数不变、降低解码算力。
- **MTP（参数共享）**：训练时共享 3 个 MTP 层、推理预测后 2 token；accept length **2.76**（DeepSeek-V3.2 为 2.55）。
- **DSA（DeepSeek Sparse Attention）**：以**续训**方式引入（避免从头训的天价成本），两阶段「dense 热身 + 稀疏适配」——热身 1000 步（14×202,752 token/步，lr 5e-3）+ 稀疏适配 20B token。长序列注意力算力降 ~1.5–2×、128K 上下文半 GPU 成本；**无损**（长上下文中 ~90% 注意力条目冗余）。
- **高效注意力消融**（GLM-9B 基座）：朴素 SWA 交错在长上下文灾难性退化；search-based SWA pattern / GDN / SimpleGDN 各有取舍，但在检索类任务仍有精度缺口；**DSA 因 lossless 胜出**。

## 预训练数据（§2.2，基座共 28.5T token）
- **Web**：在 GLM-4.5 pipeline 上加 **DCLM 句嵌入分类器** + **World Knowledge 分类器**（Wikipedia + LLM 标注）补长尾知识。
- **Code**：刷新代码托管快照 + 更多含码网页，**模糊去重 unique token +28%**；Software Heritage 元数据对齐 + 更准语言分类；对低资源语言（Scala/Swift/Lua 等）训专用分类器。
- **Math & Science**：网页/书/论文，refined 抽取 + PDF 解析；LLM 打分只留最 educational；长文档用 chunk-and-aggregate 打分；**严格不用合成/AI 生成/模板数据**。

## 中训练（§2.3，长上下文 + agentic）
- **三阶段扩上下文**：32K(1T token) → 128K(500B) → 200K(50B)；长文档 + 合成 agent 轨迹在后段上采样。
- **SWE 数据**：repo 级拼接（代码文件 + commit diff + issue + PR + 相关源文件），放宽 repo 级过滤、强化 issue 级过滤；**~10M issue–PR 对、issue-PR 部分 ~160B unique token**。
- **长上下文数据**：自然（书/论文，PPL/去重/长度多级过滤 + 上采样知识密集域）+ 合成（NextLong/EntropyLong，interleaved packing 缓解 lost-in-the-middle，200K 段加 MRCR-like 数据）。

## 训练基础设施（§2.4）
- **显存**：灵活 MTP 放置（输出层与主输出层 co-locate 共享参数）；pipeline ZeRO2 梯度分片（每 stage 仅存 1/dp 梯度 + 双缓冲）；Muon 优化器零冗余通信（只 all-gather 本 rank 持有的参数分片）；pipeline 激活 offload 到 host + 细粒度重算；序列分块输出投影降峰值显存。
- **并行**：deferred weight gradient 减 pipeline bubble；workload-aware 序列重排 + 动态注意力再分配 + 弹性 context-parallel 组；层级 all-to-all 重叠 intra/inter-node QKV 通信。
- **INT4 QAT**：SFT 阶段做 INT4 量化感知训练，量化 kernel 训练/推理 bitwise 一致。

## 后训练（§3，本报告重点；GLM-5.2 沿用此配方）
**渐进式对齐**：Base →「多任务 SFT」→ **Reasoning RL → Agentic RL → General RL** → **On-Policy Cross-Stage Distillation（最终精炼）**。

- **§3.1 SFT**：扩大 Agent/Coding 数据；三类语料：General Chat、Reasoning(数学/编程/科学)、Coding & Agent；SFT 期最大上下文扩到 **202,752**。三种思考特性：**Interleaved Thinking**（每次回复/工具调用前思考）、**Preserved Thinking**（编码 agent 多轮保留全部思考块，免重推）、**Turn-level Thinking**（按轮开关）。Reasoning 用可验证问题 + 难度过滤（只留对 GLM-4.7 仍难的）；Coding/Agent 建大量执行环境、专家 RL + 拒绝采样，**错误片段保留但 loss 中 mask 掉**（学纠错而不强化错误动作）。
- **§3.2 Reasoning RL**：算法 **GRPO + IcePop**（缓解 training-inference mismatch），**去掉 KL 项**加速；`pop()` 抑制 mismatch 过大的样本；β=2、ε_low=0.2、ε_high=0.28，**全 on-policy，group 32 / batch 32**。**DSA RL**：indexer 用**确定性 top-k（torch.topk）**解决 train-infer 失配并冻结 indexer。**混合 4 域**：数学/科学/代码/工具集成推理(TIR)；难度过滤（GLM-4.7 难、更强 teacher 如 GPT-5.2 xhigh/Gemini 3 Pro 能解）；代码来自 TACO + SYNTHETIC-2-RL；**二元 outcome reward**，四域均衡。
- **§3.3 Agentic RL**：**全异步、解耦** RL（中央 Multi-Task Rollout Orchestrator，>1k 并发 rollout）；稳定性双机制：**TITO（Token-in-Token-out）gateway**（消除 re-tokenization 失配、保 action 级对应）+ **Direct Double-sided Importance Sampling**（token 级裁剪 [1−εℓ,1+εh]，无需追历史 ckpt）；丢弃过 off-policy（版本差 > τ）与环境崩溃样本；**DP-aware routing** 复用 KV-cache。环境：>10K 真实 SWE + terminal + 高难多跳 search。
- **§3.4 General RL**：三维目标（foundational correctness / emotional intelligence / task-specific quality）；**混合奖励**：rule-based + 结果奖励模型(ORM) + 生成式奖励模型(GRM)；**human-in-the-loop**（用专家人写回复做风格锚，避免"模型味"）。
- **§3.5 On-Policy Cross-Stage Distillation**：作为**最终阶段**防多阶段 RL 的能力遗忘；teacher = 前序阶段(Reasoning RL/General RL)终点 ckpt，advantage 用 log(π_teacher^infer / π^train) 替代；group 1 / batch 1024。
- **§3.6 RL infra: slime 框架**：统一后训练栈；自由形 rollout 定制（多轮交互/工具调用/环境反馈/verifier 分支）+ server-based HTTP rollout；混精训练/rollout + MTP + **Prefill-Decode(PD)分离**；多节点 no-queue 推理 + **DP-attention（EP64/DP64 over 8 nodes）**；FP8 rollout 降尾延迟；heartbeat 容错。

## Agentic Engineering（§4，环境规模化）
- **SWE 环境**：RepoLaunch 自动建可执行环境 + 生成 F2P/P2P 测试，**>10K 可验证环境、跨数千 repo、9 种语言**（Py/Java/Go/C/CPP/JS/TS/PHP/Ruby）。
- **Terminal 环境**：Harbor 格式；种子合成（draft→构造→refine，Docker 构建准确率 >90%）+ web-corpus 闭环合成（构造 agent 自验证）。
- **Search 任务**：Web Knowledge Graph（>2M 高信息网页，语义解析建图）→ 采样低/中频实体扩多跳子图 → 转高难多跳 QA；三阶段难度过滤 + 验证。
- **Search agent 上下文管理**：分层 = keep-recent-k(k=5) + discard-all(阈值 T=32K)，把 BrowseComp 从 55.3%(无) → 62.0%(keep-recent) → **75.9**(分层，超所有开源带上下文管理的模型)。

## Benchmark（§1 + Fig 1–2）
- **Artificial Analysis Intelligence Index v4.0 = 50**，**首个达到 50 的开放权重模型、开源第一**（GLM-4.7 为 42，+8）。
- 8 项 agentic/reasoning/coding：HLE 50.4 · SWE-bench Verified 77.8 · SWE-bench Multilingual 70.2 · Terminal-Bench 2.0 56.2 · BrowseComp 75.9 · MCP-Atlas 67.8 · τ²-Bench 89.7 · Vending-Bench 2 余额 $4,432。
- 平均较 GLM-4.7 提升 ~20%，与 Claude Opus 4.5 / GPT-5.2(xhigh) 相当、优于 Gemini 3 Pro；LMArena Text & Code 均开源第一。

## 国产 GPU 生态
- 从底层 kernel 到上层推理框架全栈适配：**华为昇腾 Ascend、摩尔线程、海光 Hygon、寒武纪 Cambricon、昆仑芯 Kunlunxin、沐曦 MetaX、燧原 Enflame**。

## 原始链接
- url: https://arxiv.org/abs/2602.15763 · pdf: https://arxiv.org/pdf/2602.15763 · github: https://github.com/zai-org/GLM-5
- GLM-5.2（旗舰迭代，1M + IndexShare）见 [[glm-5.2]]

## 一手源存档（sources/）
- [arxiv-2602.15763-glm-5.pdf](https://arxiv.org/pdf/2602.15763)  （arXiv 原文 PDF，不入 git）
- [glm-5.2-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/glm-5.2-modelcard.md)
