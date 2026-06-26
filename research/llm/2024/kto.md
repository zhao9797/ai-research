---
title: "KTO: Model Alignment as Prospect Theoretic Optimization"
org: Stanford / Contextual AI
country: US
date: 2024-02
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2402.01306
pdf_url: https://arxiv.org/pdf/2402.01306
github_url: https://github.com/ContextualAI/HALOs
downloaded: [2402.01306.pdf]
---

## 一句话定位
KTO：用 Kahneman-Tversky 前景理论的人类效用函数做对齐，仅需"好/坏"二元信号（无需成对偏好），在 1B-30B 上匹配或超过 DPO。

## 摘要
卡尼曼与特沃斯基的前景理论指出人类以有偏但确定的方式感知随机变量（如损失厌恶）。作者证明，对齐 LLM 的目标隐式包含了许多这类偏置——DPO 等之所以优于交叉熵，部分因为它们属于一类称为 human-aware losses（HALOs）的损失函数。但这些方法赋予人类的效用函数仍与前景理论文献不同。作者用 Kahneman-Tversky 人类效用模型，提出直接最大化生成效用（而非最大化偏好的对数似然）的 HALO，称为 KTO。KTO 在 1B-30B 规模上匹配或超过基于偏好的方法，尽管只从"输出是否可取"的二元信号学习。更广义地，没有一个 HALO 普适最优，最佳损失取决于场景的归纳偏置。

## 关键技术细节
- 数据需求：只需每条样本的二元 desirable/undesirable 标签，无需成对 chosen/rejected——更易获取数据。
- 损失：用 KT 价值函数（含损失厌恶系数 λ）构造 HALO，参考点为 KL 散度估计。
- 鲁棒性：对数据中好坏样本不平衡更稳健；可处理 1:10 等极端比例。
- 结果：1B-30B 上匹配或超过 DPO，即便后者用成对数据。

## 原始链接
- url: https://arxiv.org/abs/2402.01306
- pdf_url: https://arxiv.org/pdf/2402.01306
- github: https://github.com/ContextualAI/HALOs

## 一手源存档（sources/）
- [2402.01306.pdf](https://arxiv.org/pdf/2402.01306)  （arXiv 原文 PDF，不入 git）
