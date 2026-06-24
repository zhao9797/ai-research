---
title: "Kimi K2.6（月之暗面：原生多模态 agentic，1T MoE，agent swarm）"
org: 月之暗面 Moonshot AI
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/moonshotai/Kimi-K2.6
github_url: https://github.com/MoonshotAI/Kimi-K2
downloaded: [kimi-k2.6-readme.md, kimi-k2.6-config.json]
---

## 一句话定位
开源**原生多模态 agentic** 模型，主打 long-horizon coding、coding-driven design、主动自主执行与 **agent swarm 群体编排**；1T MoE，K2.5 之后迭代。

## 架构（model summary + config.json）
- MoE，**总参 1T / 激活 32B**；**61 层**（含 1 dense 层）；attention hidden 7168；MoE 每专家中间维 2048。
- 64 注意力头，**MLA**；**384 专家，每 token 选 8，1 共享专家**；激活函数 SwiGLU；vocab 160K；上下文 **256K**。
- **视觉编码器 MoonViT（400M）** → 原生多模态（图、视频输入）。
- **Native INT4 量化**（同 Kimi-K2-Thinking 方案）。架构与 K2.5 一致，部署可直接复用。

## 数据 / 训练
- card 未细列预训练数据/算力；1T MoE 谱系承 Kimi K2，更细方法见 **Kimi K2.5 技术报告 arXiv 2602.02276**（评测 system prompt 即沿用之）。

## RL / 后训练 / 推理模式
- 承 K2 Thinking 的 agentic RL 路线；**preserve_thinking**（多轮保留完整 reasoning，提升 coding agent 表现）；**interleaved thinking + 多步 tool call**。
- 双模：Thinking（temp 1.0）/ Instant（temp 0.6，`thinking:disabled`）；top_p 0.95。

## agentic
- **Agent Swarm**：横向扩到 **300 个 sub-agents、4000 步**协同，动态分解为并行领域专精子任务，一次自主运行产出文档/网站/表格。
- 7×24 常驻后台 agent（自主管日程、跑代码、跨平台编排）；coding-driven design（prompt/视觉 → 生产级界面 + 动画）；long-horizon coding 跨 Rust/Go/Python。
- 最佳 agent 框架：Kimi Code CLI。

## Benchmark（thinking 模式；vs GPT-5.4 / Claude Opus 4.6 / Gemini 3.1 Pro / K2.5）
- **Agentic**：HLE-Full(w/tools) **54.0**；BrowseComp 83.2（**swarm 86.3**）；DeepSearchQA f1 **92.5** / acc **83.0**；WideSearch 80.8；Toolathlon 50.0；MCPMark 55.9；OSWorld-Verified 73.1；APEX-Agents 27.9。
- **Coding**（10 次平均）：SWE-Bench Verified **80.2** / Multilingual 76.7 / Pro 58.6；Terminal-Bench 2.0 66.7；LiveCodeBench v6 **89.6**；SciCode 52.2；OJBench 60.6。
- **推理&知识**：AIME 2026 96.4；HMMT Feb 2026 92.7；GPQA-Diamond 90.5；HLE-Full 34.7（text-only w/tools 55.5）。
- **视觉**：MMMU-Pro 79.4；MathVision 87.4（w/python 93.2）；V*(w/python) 96.9。
- 多数项较 K2.5 大幅提升（如 BrowseComp 74.9→83.2、MCPMark 29.5→55.9、Toolathlon 27.8→50.0）。

## AI infra / 部署
- vLLM / SGLang / KTransformers；`transformers>=4.57.1,<5`；native INT4；OpenAI/Anthropic 兼容 API（platform.moonshot.ai）。

## 原始链接
- url: https://huggingface.co/moonshotai/Kimi-K2.6 · blog: https://www.kimi.com/blog/kimi-k2-6.html
- 同代另有 **Kimi-K2.7-Code**、**Kimi-Linear-48B-A3B**；K2.5 报告 arXiv 2602.02276
- 许可 Modified-MIT

## 本地落盘文件
- ../../../sources/llm/2026/kimi-k2.6-readme.md
- ../../../sources/llm/2026/kimi-k2.6-config.json
