---
title: "GLM-5: from Vibe Coding to Agentic Engineering"
org: 智谱 Z.ai (Zhipu / GLM-5-Team)
country: China
date: 2026-02
type: paper
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2602.15763
pdf_url: https://arxiv.org/pdf/2602.15763
github_url: https://github.com/zai-org/GLM-5
downloaded: [glm-5.pdf, glm-5.2-modelcard.md]
---

## 一句话定位
智谱 GLM-5 旗舰基座模型技术报告，目标是把"vibe coding"推进到"agentic engineering"，核心是 DSA 稀疏注意力 + 异步 RL 基础设施 + 异步 agent RL 算法。

## 摘要
GLM-5（arXiv 2026-02-17，作者 "GLM-5-Team"，187 人）是智谱新一代基座模型。在前代 ARC（agentic/reasoning/coding）能力基础上，GLM-5 采用 DSA（稀疏注意力）显著降低训练与推理成本，同时保持长上下文保真度。为提升对齐与自主性，团队构建了全新异步强化学习基础设施，通过解耦 generation 与 training 大幅提升后训练效率，并提出新颖的异步 agent RL 算法以从复杂长程交互中学习。GLM-5 在主流开源 benchmark 上达 SOTA，在真实端到端软件工程任务上超越既有 baseline。后续迭代 GLM-5.1（HF 2026-04）、GLM-5.2（HF 2026-06，1M 上下文 + IndexShare 架构）。代码模型见 github.com/zai-org/GLM-5。

## 关键技术细节
- **架构-DSA**：采用 DSA（稀疏注意力）降低训练 + 推理成本，保持长上下文保真。
- **AI infra-异步 RL**：全新异步强化学习基础设施，解耦 generation 与 training，大幅提升后训练效率。
- **后训练/agentic-异步 agent RL 算法**：新颖异步 agent RL 算法，从复杂长程（long-horizon）交互中学习。
- **能力定位**：从 vibe coding → agentic engineering，真实端到端软件工程任务超越 baseline。
- **后续迭代 GLM-5.2（model card，2026-06-16）**：
  - 旗舰长程任务模型，首次在 1M token 上下文上稳定支撑长程工作。
  - **IndexShare**（arXiv 2603.12201）：每 4 层稀疏注意力复用同一 indexer，在 1M 上下文下把每 token FLOPs 降低 2.9×；改进 MTP 层用于投机解码，接受长度提升最多 20%。
  - 多档 thinking effort 平衡性能与延迟；MIT 开源。
  - 评测（节选，GLM-5.2）：AIME 2026 99.2、HLE 40.5 / HLE(w/Tools) 54.7、GPQA-Diamond 91.2、SWE-bench Pro 62.1。
- **开源**：HF zai-org 官方组织（GLM-5 / GLM-5-FP8 / GLM-5.1 / GLM-5.2 等），MIT。

## 原始链接
- url: https://arxiv.org/abs/2602.15763
- pdf_url: https://arxiv.org/pdf/2602.15763
- github_url: https://github.com/zai-org/GLM-5
- GLM-5.2 blog: https://z.ai/blog/glm-5.2 ; model card: https://huggingface.co/zai-org/GLM-5.2

## 本地落盘文件
- ../../../sources/llm/2026/glm-5.pdf
- ../../../sources/llm/2026/glm-5.2-modelcard.md
