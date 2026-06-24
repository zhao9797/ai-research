---
title: "A General Language Assistant as a Laboratory for Alignment"
org: Anthropic
country: US
date: 2021-12
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2112.00861
pdf_url: https://arxiv.org/pdf/2112.00861
github_url:
downloaded: [arxiv-2112.00861.pdf]
---

## 一句话定位
Anthropic 成立后的首批论文之一：把"通用语言助手"当作对齐研究的实验台，系统比较模仿学习/二元判别/偏好建模等对齐目标的 scaling 趋势，提出 HHH（helpful, honest, harmless）框架。

## 摘要（3-6 句）
论文研究如何朝着对齐人类价值（helpful, honest, harmless，HHH）的通用文本助手前进。作为初步探索，先研究 prompting 等简单 baseline，发现温和干预的收益随模型规模增大、可泛化到多种对齐评测、且不损害大模型性能。接着比较几种对齐相关训练目标的 scaling 趋势：模仿学习（imitation learning）、二元判别（binary discrimination）、排序偏好建模（ranked preference modeling）。结论是偏好建模显著优于模仿学习且随规模更优；二元判别与模仿学习表现相近。最后研究"偏好模型预训练"（preference model pre-training）阶段。

## 关键技术细节
- HHH 对齐框架：helpful / honest / harmless，并配套对齐评测。
- 对齐目标对比：ranked preference modeling > imitation learning（且 scaling 更好）；binary discrimination ≈ imitation learning。
- 提出 preference model pre-training（PMP）阶段，提升样本效率。
- 发现 prompting 等"温和干预"收益随规模增大、可泛化、不损害性能。
- Anthropic（2021 成立，由 Dario/Daniela Amodei 等创立）的早期对齐路线一手文献，是后续 RLHF / Constitutional AI 的前置。

## 原始链接
- url: https://arxiv.org/abs/2112.00861
- pdf_url: https://arxiv.org/pdf/2112.00861

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2112.00861.pdf
