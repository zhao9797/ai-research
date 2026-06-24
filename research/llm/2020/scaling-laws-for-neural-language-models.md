---
title: Scaling Laws for Neural Language Models
org: OpenAI
country: US
date: 2020-01
type: paper
categories: [架构, 预训练数据, AI infra]
url: https://arxiv.org/abs/2001.08361
pdf_url: https://arxiv.org/pdf/2001.08361
github_url:
downloaded: [arxiv-2001.08361.pdf]
---

## 一句话定位
Kaplan 等提出语言模型性能随模型参数 N、数据量 D、算力 C 呈幂律（power-law）下降的经验规律，直接为后来 GPT-3 的“无脑放大”路线提供理论依据。

## 摘要（3-6 句）
论文对 Transformer 语言模型的交叉熵损失进行了大规模经验研究，发现损失与模型规模、数据集大小、训练算力三者均呈平滑的幂律关系，跨越超过 7 个数量级。模型形状（深度/宽度）等架构超参影响很小。更大的模型样本效率显著更高，因此在固定算力预算下，最优策略是训练非常大的模型、使用相对适中的数据量、并在收敛前提前停止。论文给出可据此分配算力/参数/数据的解析关系。

## 关键技术细节
- 核心幂律：L(N) ∝ N^(-0.076)，L(D) ∝ D^(-0.095)，L(C) ∝ C^(-0.050)（数值为论文经验拟合指数）。
- 损失主要由 N、D、C 决定，与网络深宽比、注意力头数等形状参数关系很弱（在合理范围内）。
- 样本效率：大模型用更少数据/步数即可达到相同损失，故算力最优解是“训大模型 + 不训到收敛”。
- 给定算力预算 C，最优分配：参数量应随 C 增长得较快，batch size 有一个随损失变化的“临界 batch size”。
- 过拟合可由 N 与 D 的联合幂律 L(N,D) 描述，给出避免过拟合所需的数据量随模型规模的标度。
- 实验基于 WebText2 数据，模型规模从约 768 到十亿级参数。

## 原始链接
- url: https://arxiv.org/abs/2001.08361
- pdf_url: https://arxiv.org/pdf/2001.08361

## 本地落盘文件
- ../../../sources/llm/2020/arxiv-2001.08361.pdf
