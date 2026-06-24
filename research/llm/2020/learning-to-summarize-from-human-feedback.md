---
title: Learning to summarize from human feedback
org: OpenAI
country: US
date: 2020-09
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2009.01325
pdf_url: https://arxiv.org/pdf/2009.01325
github_url: https://github.com/openai/summarize-from-feedback
downloaded: [arxiv-2009.01325.pdf]
---

## 一句话定位
RLHF（基于人类反馈的强化学习）在语言生成上的奠基性实证工作：用人类偏好训练奖励模型，再用 PPO 优化策略模型做摘要，直接为后来 InstructGPT/ChatGPT 的对齐范式铺路。

## 摘要（3-6 句）
论文（Stiennon、Ouyang、Lowe 等）训练模型从 Reddit TL;DR 数据集生成摘要，采用收集人类对成对摘要的偏好 → 训练奖励模型 → 用 PPO 强化学习微调策略模型 的三步流程。结果显示用人类反馈训练的模型显著优于监督微调基线和参考摘要本身，并能良好迁移到 CNN/DailyMail 新闻摘要（零样本）。论文强调奖励模型随数据与模型规模可继续改进，并讨论了优化奖励模型导致的过优化（over-optimization）问题。

## 关键技术细节
- 流程：1) 在 TL;DR 上监督微调（SFT）；2) 收集人类对两个摘要的偏好对，训练奖励模型 RM；3) 用 PPO 以 RM 为奖励、加 KL 惩罚（防止偏离 SFT 策略过远）微调策略。
- RL 算法：PPO（Proximal Policy Optimization），奖励 = RM 分数 − β·KL(策略||SFT)。
- 模型规模：1.3B 与 6.7B 参数（GPT-3 系列同款架构）。
- 数据：Reddit TL;DR 摘要数据集，过滤后约 12.3 万条；收集了约 6.4 万条人类偏好比较。
- 关键发现：人类反馈模型在人类评价上胜过 10 倍大的监督模型；奖励模型与策略性能随规模提升；过度优化 RM 会导致真实质量下降（需 KL 约束）。
- 迁移：在 TL;DR 上训练的模型零样本迁移到 CNN/DM 新闻摘要仍优于该域监督模型。

## 原始链接
- url: https://arxiv.org/abs/2009.01325
- pdf_url: https://arxiv.org/pdf/2009.01325
- github_url: https://github.com/openai/summarize-from-feedback

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2009.01325.pdf
