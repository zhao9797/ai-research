---
title: SWE-RL: Advancing LLM Reasoning via Reinforcement Learning on Open Software Evolution
org: Meta (FAIR / GenAI)
country: US
date: 2025-02
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2502.18449
pdf_url: https://arxiv.org/pdf/2502.18449
github_url: https://github.com/facebookresearch/swe-rl
downloaded: [swe-rl.pdf]
---

## 一句话定位
SWE-RL：首个把 R1 式 RL 扩展到真实软件工程的方法，用"开源软件演化数据 + 轻量规则奖励（与真实补丁的相似度）"训练，Llama3-SWE-RL-70B 在 SWE-bench Verified 达 41.0%。

## 摘要（3-6 句）
SWE-RL 把 RL-based 推理从竞赛代码/数学扩展到真实世界软件工程。它利用海量开源软件演化数据（代码快照、代码变更、issue 与 PR 等完整生命周期记录），用轻量规则化奖励——LLM 生成补丁与真实补丁（ground-truth）的相似度分数——训练模型自主复现开发者的推理与解决方案。基于 Llama 3 训练得到 Llama3-SWE-RL-70B，在人工核验的 SWE-bench Verified 上解出 41.0%，是当时 <100B 模型最佳、可比肩 GPT-4o。值得注意的是，尽管只在软件演化数据上做 RL，模型还涌现出泛化推理能力，在函数级编码、库使用、代码推理、数学、通用语言理解 5 个域外任务上均有提升，而 SFT 基线反而平均退化。

## 关键技术细节
- 基座：Llama 3（70B）。
- 数据：GitHub 开源软件演化记录（snapshots、code changes、issues、PRs），构造"看 issue + 代码上下文 → 生成修复补丁"任务。
- 奖励：规则化、轻量——生成补丁与真实补丁的相似度（如基于 difflib 的序列相似度）作为连续奖励，格式不符给 −1；无需训练奖励模型、无需执行测试。
- RL 算法：GRPO 类策略优化（R1 风格）。
- 结果：Llama3-SWE-RL-70B 在 SWE-bench Verified 41.0%（<100B SOTA）；域外 5 任务泛化提升，SFT 基线退化。
- 意义：证明在真实工程数据上做 RL 可获得可迁移的通用推理能力。

## 原始链接
- url: https://arxiv.org/abs/2502.18449
- pdf_url: https://arxiv.org/pdf/2502.18449
- github_url: https://github.com/facebookresearch/swe-rl

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/swe-rl.pdf
