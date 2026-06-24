---
title: Language Models (Mostly) Know What They Know
org: Anthropic    country: US    date: 2022-07    type: paper
categories: [后训练]
url: https://arxiv.org/abs/2207.05221    pdf_url: https://arxiv.org/pdf/2207.05221    github_url:
downloaded: [lm-know-what-they-know.pdf]
---

## 一句话定位
Anthropic 研究 LLM 的自我评估与校准：大模型能较好预测自己答案对错（P(True)）及"是否知道"（P(IK)），为诚实性/幻觉缓解奠基。

## 摘要
研究语言模型能否评估自身主张的有效性、预测自己能否答对。首先表明在合适格式下，更大模型在多选与判断题上校准良好。于是可把自评推广到开放式采样：让模型先提出答案，再评估答案正确的概率 P(True)。发现 P(True) 在多样任务上有不错的性能、校准与缩放；当允许模型在预测前考虑自己的多个采样时，自评进一步改善。接着研究模型能否被训练预测 P(IK)——"我知道"某问题答案的概率，且无需参考特定答案。

## 关键技术细节
- 校准：大模型在格式恰当的多选/真假题上 well-calibrated（预测概率与实际正确率吻合）。
- P(True)：让模型评估自身答案为真的概率，作为自我验证信号；考虑多个候选采样后更准。
- P(IK)：训练模型预测"我知道答案"的概率，能跨任务泛化，部分反映模型对自身知识边界的认知。
- 这些自我知识随规模提升，是减少幻觉、做选择性回答（拒答）的基础。
- 属 Anthropic 诚实性（honesty）研究线，与 RLHF/CAI 互补。

## 原始链接
- url: https://arxiv.org/abs/2207.05221
- pdf_url: https://arxiv.org/pdf/2207.05221

## 本地落盘文件
- ../../../sources/llm/2022/lm-know-what-they-know.pdf
