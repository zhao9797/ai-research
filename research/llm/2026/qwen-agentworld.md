---
title: "Qwen-AgentWorld-35B-A3B（首个语言世界模型 LWM：agent 环境仿真）"
org: 阿里巴巴 Qwen
country: China
date: 2026-06
type: paper
categories: [agentic训练, 架构, 后训练, 预训练数据]
url: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B
pdf_url: https://arxiv.org/abs/2606.24597
github_url: https://github.com/QwenLM/Qwen-AgentWorld
downloaded: [qwen-agentworld-readme.md, qwen-agentworld-config.json, arxiv-2606.24597-qwen-agentworld.pdf]
---

## 一句话定位
**首个覆盖 7 个 agent 交互域的「语言世界模型 (Language World Model, LWM)」**：用 long CoT 仿真 agentic 环境，给定 agent 动作 + 交互历史预测**下一环境状态**；环境建模从 CPT 起即训练目标，而非在通用 LLM 上事后外挂。35B/3B（另有 397B/17B 版）。

## 架构（config.json + model card）
- 基座 **Qwen3.5-35B-A3B-Base**；35B 总 / 3B 激活 MoE；hidden 2048；**40 层**；vocab 248320（padded）；上下文 **262,144**。
- **混合层布局**：`10 × (3 ×(Gated DeltaNet → MoE) → 1 ×(Gated Attention → MoE))` —— 线性注意力(Gated DeltaNet) 与门控全注意力 3:1 交替（承 Qwen3-Next 线路）。
  - Gated DeltaNet：线性注意力头 V 32 / QK 16，head_dim 128。
  - Gated Attention：16 Q / 2 KV 头，head_dim 256，RoPE dim 64，rope_theta 1e7。
- **MoE**：256 专家，每 token 8 路由 + 1 共享，专家中间维 512；MTP 1 层。

## 预训练数据 / 处理
- 训练数据 = 跨 **7 域**（MCP 工具调用 / Search / Terminal / SWE / Android / Web / OS，含文本与 GUI 环境）的环境交互轨迹；配套数据集 **AgentWorldBench**（HF dataset）。
- 明确声明：**训练管线不含任何外部 API 服务的输出**（no distillation from external APIs）。
- 更细的数据构造见技术报告 arXiv 2606.24597（已落盘 PDF）。

## 训练（三阶段）
- **CPT**：注入环境知识；**SFT**：激活 next-state-prediction 推理；**RL**：用 **GSPO**（Group Sequence Policy Optimization）锐化仿真保真度。
- 是 **native world model**：环境建模自 CPT 阶段起就是目标，而非事后适配。

## RL / agentic
- **LWM RL warm-up 关键发现**：在**单轮、非 agentic 轨迹**上做 RL warm-up，可迁移到**多轮 tool-calling agentic 任务**（7 个 benchmark，含 3 个完全 OOD），即作为 agent 基础模型。
- 可控扰动 + 虚构世界构建，效果超越在真实环境上训练；对 OOD 环境（如 OpenClaw）零样本泛化。
- 默认 thinking 模式（`<think>…</think>`）先推理状态转移再产出预测观察。

## Benchmark（AgentWorldBench，开放式评测，5 维 rubric：Format/Factuality/Consistency/Realism/Quality，0-100）
- **Qwen-AgentWorld-397B-A17B Overall 58.71**（榜首，超 GPT-5.4 58.25、Claude Opus 4.8 56.59）；MCP 68.24 / Search 37.82 / SWE 68.49 最强项。
- **Qwen-AgentWorld-35B-A3B Overall 56.39**（35B 即与 Claude Opus 4.8 同档），显著高于同基座 Qwen3.5-35B-A3B（47.73）。
- judge 用 gpt-5.2；评测三步 infer→judge→score（QwenLM/Qwen-AgentWorld eval）。

## AI infra / 部署
- SGLang / vLLM `tp=4`、`max-model-len 262144`、`reasoning-parser qwen3`；建议 ≥128K 上下文以支撑多轮环境仿真；输出长度建议 32K。

## 原始链接
- url: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B · blog: https://qwen.ai/blog?id=qwen-agentworld
- paper: https://arxiv.org/abs/2606.24597 · github: https://github.com/QwenLM/Qwen-AgentWorld · dataset: Qwen/AgentWorldBench

## 本地落盘文件
- ../../../sources/llm/2026/qwen-agentworld-readme.md
- ../../../sources/llm/2026/qwen-agentworld-config.json
- ../../../sources/llm/2026/arxiv-2606.24597-qwen-agentworld.pdf
