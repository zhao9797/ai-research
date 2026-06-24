---
title: "Qwen-AgentWorld-35B-A3B（首个语言世界模型：agent 环境仿真）"
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
Qwen-AgentWorld —— **首个覆盖 7 个 agent 交互域的「语言世界模型 (LWM)」**：用 long CoT 仿真 agentic 环境，给定 agent 动作与历史预测下一环境状态；环境建模从 CPT 阶段起就是训练目标而非事后外挂（晚于初版调研，增量补录）。

## 摘要
不同于「在通用模型上加 agent 能力」，AgentWorld 把**环境建模本身**作为训练目标。三阶段流水线：**CPT 注入环境知识 → SFT 激活 next-state-prediction 推理 → RL 锐化仿真保真度**。关键发现：在**单轮非 agentic 轨迹上做 LWM RL warm-up，可迁移到多轮 tool-calling agentic 任务**（7 个 benchmark，含 3 个完全 OOD），即作为 agent 基础模型。35B 总参 / 3B 激活，Apache-2.0。

## 关键技术细节
- **架构（config.json，model_type=qwen3_5_moe）**：**35B 总 / 3B 激活** MoE；hidden 2048；**40 层**；16 注意力头 / 2 KV，head_dim 256；**混合线性注意力**（linear_key/value_head_dim 128，承 Qwen3-Next 线路）；**256 专家，每 token 选 8** + 共享专家；MTP 1 层；vocab 248320；上下文 256K（262144）；rope 1e7。
- **训练**：CPT（环境知识）→ SFT（次态预测推理）→ RL（仿真保真度）；native world model。
- **意义**：把「自主探索/环境仿真」做成可训练、可迁移的 agent 基础能力，是 agentic 训练范式的新方向。
- 配套 AgentWorldBench 评测集。

## 原始链接
- url: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B · blog: https://qwen.ai/blog?id=qwen-agentworld
- paper: https://arxiv.org/abs/2606.24597 · github: https://github.com/QwenLM/Qwen-AgentWorld

## 本地落盘文件
- ../../../sources/llm/2026/qwen-agentworld-readme.md
- ../../../sources/llm/2026/qwen-agentworld-config.json
- ../../../sources/llm/2026/arxiv-2606.24597-qwen-agentworld.pdf
