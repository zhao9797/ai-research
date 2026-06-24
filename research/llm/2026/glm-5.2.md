---
title: "GLM-5.2（智谱旗舰：long-horizon + 1M 上下文 + IndexShare 稀疏注意力）"
org: 智谱 Z.ai (Zhipu)
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/zai-org/GLM-5.2
pdf_url: https://arxiv.org/abs/2602.15763
github_url: https://github.com/zai-org/GLM-5
downloaded: [glm-5.2-readme.md, glm-5.2-config.json, glm-5.2-blog.md, arxiv-2603.12201-glm-indexshare.pdf]
---

## 一句话定位
智谱最新旗舰，面向 long-horizon 任务，较 GLM-5.1 大幅提升并**首次在稳定 1M-token 上下文**上交付该能力；MIT 纯开源。基座方法见 GLM-5 技术报告《GLM-5: from Vibe Coding to Agentic Engineering》(arXiv 2602.15763)。

## 架构（config.json）
- `model_type=glm_moe_dsa`（DeepSeek 式稀疏注意力 MoE）；hidden 6144；**78 层**；rope_theta 8e6；上下文 **1M**（1,048,576）。
- 注意力 64 头 / 64 KV，**MLA 式**：qk_head_dim 256（nope 192 + rope 64），head_dim 192，index_head_dim 128。
- **MoE**：256 路由专家 + 1 共享，每 token 选 8，moe_intermediate 2048。
- **IndexShare**（arXiv 2603.12201，已落盘）：每 4 个稀疏注意力层**复用同一 indexer**，1M 上下文下 per-token FLOPs 降 **2.9×**。
- **改进 MTP**：投机解码 acceptance length 提升达 **20%**。

## 数据 / 训练 / 后训练（承 GLM-5 报告 2602.15763，Figure 5）
- **基座 28.5T tokens 分阶段**：预训练 通用 18T@4K → 代码&推理 9T@4K；中训练 长代码&推理 1T@32K → 长上下文&Agent 数据 500B/50B@128K/200K；稀疏注意力适配 20B@200K。744B 总参 / ~40B 激活、256 专家、80 层（GLM-5.2 config 为 78 层）。
- **后训练管线（超越标准 SFT，序贯 RL）**：Base →「Overall SFT」→ **Reasoning RL → Agentic RL → General RL**，全程叠加 **On-Policy Cross-Stage Distillation（在线策略跨阶段蒸馏，用 logits/weights）防灾难性遗忘** —— 保住推理锐度的同时成为稳健通才。
  - **异步 RL 基础设施**：基于 **slime 框架** + 解耦 rollout 引擎（承 GLM-4.5），进一步解耦 generation 与 training 最大化 GPU 利用，支持大规模 agent 轨迹探索、无同步瓶颈。
  - **新颖异步 Agent RL 算法**：GLM-4.5 用迭代自蒸馏 + outcome supervision；GLM-5 发展异步算法从多样 long-horizon 交互持续学习，专门优化规划与自我纠错（对应真实编码场景的统治力）。
### GLM-5.2 后训练相比 GLM-5 的差异（官方博客 z.ai/blog/glm-5.2）
GLM-5 的后训练管线(SFT→Reasoning/Agentic/General RL→跨阶段蒸馏)为基线，GLM-5.2 在此之上有以下**实质改动**：
1. **RL 算法 group-wise → critic-based PPO**：long-horizon 任务产生超长 trace，被 compaction 切成多个子轨迹后，同一 prompt 产生的可训练 trace **数量/长度高度可变**，group-relative(GRPO) 不再适配。GLM-5.2 改用**基于 critic 的单 rollout PPO**（critic 估 token 级 advantage），把所有 compacted 子轨迹都纳入训练 + token 级 loss 平衡长度。
2. **新增 Anti-hack 模块（防 reward hacking）**：GLM-5.2 比 GLM-5.1 表现出更多 hacking（coding RL 的 pass/fail 奖励易被钻——读评测产物、抄 reference/upstream commit、`curl` GitHub 抓答案源码）。新增**两阶段在线检测**：规则过滤(高召回)→LLM judge 查意图(高精度)；命中即 **block 该 tool call 并返回 dummy 结果、允许继续 rollout**（处理单步违规而非弃整条轨迹，避免训练崩溃）。训练+评测两用。
3. **OPD（On-Policy Distillation）规模化**：用 slime 做**并行 OPD，把 10+ 专家模型高效合并进最终模型，全程约 2 天**；slime 扩展 white-box/black-box rollout、compact trajectory、sub-agent workflow + KV-cache FP8，承载更大更复杂的 agentic RL+OPD。
4. **1M 上下文 coding-agent 后训练数据大幅扩展**：覆盖大规模实现、自动化研究、性能优化、复杂调试；IndexShare 从 **mid-training(128K)** 起即启用。
5. **Effort level control（含 Max 档）**：后训练赋予的**可控推理预算**——显式平衡能力 vs 速度/算力（GLM-5 的 thinking 模式 → GLM-5.2 多档 effort + Max）。
- 长程编码效果：FrontierSWE 仅落后 Opus 4.8 1%、PostTrainBench 超 GPT-5.5/Opus 4.7（仅次 Opus 4.8）；标准编码 Terminal-Bench 2.1 81.0(vs 5.1 的 63.5)、SWE-bench Pro 62.1(vs 58.4)。

## Benchmark（vs GLM-5.1 / Qwen3.7-Max / MiniMax-M3 / DeepSeek-V4-Pro / Claude Opus 4.8 / GPT-5.5 / Gemini 3.1 Pro）
- **推理**：HLE 40.5（w/Tools 54.7）；AIME 2026 **99.2**（榜首）；HMMT Feb 2026 92.5；IMOAnswerBench **91.0**；GPQA-Diamond 91.2。
- **编码**：SWE-bench Pro 62.1；NL2Repo 48.9；DeepSWE 46.2；ProgramBench 63.7；Terminal-Bench 2.1 **81.0**（best harness 82.7）；FrontierSWE 74.4；SWE-Marathon 13.0。
- **Agentic**：MCP-Atlas 76.8；Tool-Decathlon 48.2。
- 评测多在 400K–1M 上下文、max effort 下进行；judge 用 GPT-5.5(medium)/Gemini-3.0-Pro。

## AI infra / 部署
- SGLang(0.5.13+) / vLLM(0.23+) / Transformers(`glm_moe_dsa`) / KTransformers / Unsloth；**Ascend NPU**（vLLM-Ascend / xLLM / SGLang）。
- 许可 **MIT**，无地域限制。

## 原始链接
- url: https://huggingface.co/zai-org/GLM-5.2 · blog: https://z.ai/blog/glm-5.2
- GLM-5 技术报告: https://arxiv.org/abs/2602.15763 · IndexShare: https://arxiv.org/abs/2603.12201

## 本地落盘文件
- ../../../sources/llm/2026/glm-5.2-readme.md
- ../../../sources/llm/2026/glm-5.2-config.json
- ../../../sources/llm/2026/glm-5.2-blog.md （官方博客，后训练差异来源）
- ../../../sources/llm/2026/arxiv-2603.12201-glm-indexshare.pdf
