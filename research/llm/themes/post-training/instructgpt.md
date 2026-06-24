---
title: Training language models to follow instructions with human feedback (InstructGPT)
org: OpenAI
country: US
date: 2022-03
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2203.02155
pdf_url: https://arxiv.org/pdf/2203.02155
downloaded: [instructgpt.pdf]
---

## 一句话定位
现代指令对齐范式的奠基论文（SFT → RM → PPO 三段式 RLHF），证明 1.3B 的 InstructGPT 输出比 175B GPT-3 更受人类偏好，开启 ChatGPT 时代。

## 摘要（3-6 句）
作者用人类反馈微调 GPT-3 使其遵循指令：先收集标注者编写的演示做监督微调（SFT），再收集模型输出的人类排序训练奖励模型（RM），最后用 PPO 针对 RM 做强化学习。结果显示 1.3B 参数的 InstructGPT 在人类偏好上胜过 175B 的 GPT-3，同时在真实性、毒性上有改善，且在公开 NLP 数据集上的性能回退很小（"alignment tax" 可控）。这套 SFT→RM→PPO 流程成为后续几乎所有对话模型的标准后训练配方。

## 关键技术细节
- 基座：GPT-3，对齐版本含 1.3B / 6B / 175B。
- 数据：约 1.3 万条 SFT 演示（标注者+API 用户提示）、约 3.3 万条 RM 排序数据、约 3.1 万条 PPO 提示；标注团队约 40 人，强调标注者筛选与一致性。
- RM：从 6B SFT 初始化，损失为对每个提示的 K=4~9 个输出做成对排序（list-wise 转 pairwise）。
- PPO：reward = RM − β·KL(π‖π_SFT)；提出 "PPO-ptx" 变体，在 RL 目标中混入预训练梯度以缓解公开任务上的性能退化。
- 评测：人类偏好、TruthfulQA（真实性翻倍）、RealToxicityPrompts（毒性下降）。

## 原始链接
- url: https://arxiv.org/abs/2203.02155
- pdf_url: https://arxiv.org/pdf/2203.02155

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/instructgpt.pdf
