---
title: "ToRL: Scaling Tool-Integrated RL"
org: "上海交通大学 / SII / GAIR"
country: CN
date: 2025-03
type: paper
categories: [后训练, agentic训练, 推理]
url: https://arxiv.org/abs/2503.23383
pdf_url: https://arxiv.org/pdf/2503.23383
github_url: https://github.com/GAIR-NLP/ToRL
downloaded: [torl-2503.23383.pdf]
---

## 一句话定位
直接从 base 模型（无任何 post-training）做"工具集成 RL"：让模型在 RL 中自主发现写代码、调解释器的最优策略，而非靠 SFT 模仿固定模式——TORL-7B 仅 7B 即在 AIME24 拿到 43.3%。

## 摘要
ToRL（Tool-Integrated Reinforcement Learning）训练 LLM 自主使用计算工具（写代码 → 调代码解释器 → 基于执行结果继续推理）。与基于 SFT 的方法不同，ToRL 直接从 base 模型（未经 post-training）通过无限制探索做 RL，让模型自行发现最优工具使用策略。在 Qwen2.5-Math base 模型上，TORL-7B 在 AIME24 达到 43.3% 准确率——比"无工具 RL"高 14%、比当时最佳 TIR（工具集成推理）模型高 17%，可与一些 32B RL 模型相当。还观察到策略性工具调用、对无效代码生成的自我调节、计算/分析推理的动态切换等涌现认知行为，均无需显式指令、纯由奖励驱动学得。

## 关键技术细节
- 基座：Qwen2.5-Math 系列 base 模型（1.5B 与 7B），直接从 base 起 RL（RL-from-base / zero 式），无前置 SFT。
- RL 算法：GRPO（Shao et al. 2024），训练框架用 veRL；代码解释器用 Sandbox Fusion。
- 超参：rollout batch size 128，每题 16 个采样；为增强探索，省略 KL loss、temperature 设为 1。
- 奖励设计：答案正确奖励（正确 +1 / 错误 -1）+ 代码可执行性奖励（可执行 0 / 不可执行 -0.5）。
- TIR 轨迹形式化：s_k = (r_1,c_1,o_1,...,r_k,c_k,o_k)，r=自然语言推理、c=生成代码、o=解释器执行结果，迭代直至最终答案。
- 主结果（Avg over AIME24/AIME25/MATH500/Olympiad/AMC23）：TORL-1.5B 48.5（较 TIR 基线 +7.2）；TORL-7B 在 AIME24 43.3%（+10.0 vs Qwen2.5-Math-7B-Instruct-TIR），整体超过 SimpleRL-Zero、rStar-Math-7B、Eurus-2-7B-PRIME 等。评测均 temperature=0。
- 关键洞见：训练中"用代码解题比例"与"可执行代码比例"稳步上升；模型自学减少无效代码；提高单题最大 tool call 数能显著提升性能但带来严重算力开销（效率-效果权衡）。

## 原始链接
- url: https://arxiv.org/abs/2503.23383
- pdf_url: https://arxiv.org/pdf/2503.23383
- github_url: https://github.com/GAIR-NLP/ToRL

## 一手源存档（sources/）
- [torl-2503.23383.pdf](https://arxiv.org/pdf/2503.23383)  （arXiv 原文 PDF，不入 git）
