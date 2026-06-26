---
title: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)"
org: DeepSeek-AI / Peking University / Tsinghua University
country: China
date: 2024-02
type: paper
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2402.03300
pdf_url: https://arxiv.org/pdf/2402.03300
downloaded: [deepseekmath-grpo-2402.03300.pdf]
---

## 一句话定位
提出 GRPO（Group Relative Policy Optimization）——去掉 critic、用同 prompt 多采样的组内相对优势做 RL，成为 DeepSeek-R1 及众多推理模型 RL 的核心算法。

## 摘要（3-6 句）
DeepSeekMath 在 7B 模型上以 120B 数学 token 继续预训练，在 MATH 上达 51.7%，逼近当时闭源水平。其 RL 阶段提出 GRPO：放弃价值网络（critic），对同一 prompt 采样一组输出，用组内奖励的标准化相对值作为优势估计，显著降低 RL 显存与计算成本且稳定。论文还系统讨论了数学预训练数据构建（DeepSeekMath Corpus，从 Common Crawl 召回）。GRPO 后被 DeepSeek-R1、Qwen、众多 RLVR 工作沿用，是 2024-2025 推理 RL 的算法基石。

## 关键技术细节
- GRPO：无 critic；对每 prompt 采 G 个输出，优势 A_i = (r_i − mean(r))/std(r)（组内归一化）；KL 直接加在 loss。
- 相比 PPO：省去 value model，显存/算力近半，训练更稳。
- 数据：DeepSeekMath Corpus 120B token（迭代式从 CommonCrawl 召回 + fastText 分类）。
- 结果：DeepSeekMath-7B 在 MATH 51.7%（不借助外部工具/投票），开源 7B SOTA。

## 原始链接
- url: https://arxiv.org/abs/2402.03300
- pdf_url: https://arxiv.org/pdf/2402.03300

## 一手源存档（sources/）
- [deepseekmath-grpo-2402.03300.pdf](https://arxiv.org/pdf/2402.03300)  （arXiv 原文 PDF，不入 git）
