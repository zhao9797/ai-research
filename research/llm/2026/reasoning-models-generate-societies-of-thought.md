---
title: Reasoning Models Generate Societies of Thought
org: Google (Paradigms of Intelligence Team) / University of Chicago / Santa Fe Institute
country: US
date: 2026-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2601.10825
pdf_url: https://arxiv.org/pdf/2601.10825
github_url:
downloaded: [arxiv-2601.10825.pdf]
---

## 一句话定位
Google "Paradigms of Intelligence" 团队 2026-01 的 arXiv 论文，论证推理模型的能力提升并非仅来自更长的测试时计算，而来自其推理轨迹中隐式模拟的多智能体式"思想社会"（society of thought）。

## 摘要
论文用分类输出 + 机制可解释性方法分析推理模型（DeepSeek-R1、QwQ-32B、OpenAI o 系列等）的推理轨迹，发现增强的推理来自隐式的复杂多智能体式交互——具备不同人格特质与领域专长的内部认知视角间的"有意多样化与辩论"。推理模型相比基线/纯指令微调模型表现出更大的视角多样性，激活更广泛的人格/专长相关特征间冲突。这种多智能体结构体现在问答序列、视角切换、冲突调和等对话行为以及社会-情感角色上，通过直接与间接方式促进认知策略，从而带来准确率优势。受控 RL 实验进一步显示：仅以推理准确率为奖励时，基座模型会自发增加对话式行为；用"对话式脚手架"微调比单调（monologue）式推理微调能显著加速推理能力提升。

## 关键技术细节
- arXiv ID：2601.10825（2026-01）。作者：Junsol Kim, Shiyang Lai, Nino Scherrer, Blaise Agüera y Arcas, James Evans。机构：Google Paradigms of Intelligence Team / University of Chicago / Santa Fe Institute。112 页。
- 核心论点：推理增益来自隐式多智能体交互（society of thought），而非单纯更长链式思维/测试时计算。
- 方法：对推理轨迹做分类输出统计 + 机制可解释性（mechanistic interpretability）分析；对比 base / instruction-tuned / reasoning-reinforced 模型的"视角多样性"。
- 观测对象：DeepSeek-R1、QwQ-32B、OpenAI o 系列等推理强化模型。
- RL 实验：仅奖励推理准确率 → base 模型自发增加对话式行为；用 conversational scaffolding 微调 > monologue-style 微调，显著加速推理改进。
- 结论：思想的"社会组织"使推理空间的探索更有效，是推理能力的关键机制。

## 原始链接
- url: https://arxiv.org/abs/2601.10825
- pdf_url: https://arxiv.org/pdf/2601.10825

## 一手源存档（sources/）
- [arxiv-2601.10825.pdf](https://arxiv.org/pdf/2601.10825)  （arXiv 原文 PDF，不入 git）
