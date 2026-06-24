---
title: Towards Greater Leverage: Scaling Laws for Efficient Mixture-of-Experts Language Models
org: 蚂蚁集团 Ling Team / inclusionAI (Ant Group)
country: China
date: 2025-07
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2507.17702
pdf_url: https://arxiv.org/pdf/2507.17702
github_url: https://github.com/inclusionAI/Ling-V2
downloaded: [ling-moe-scaling-laws.pdf]
---

## 一句话定位
蚂蚁 Ling 团队的 MoE 缩放律研究：提出 Efficiency Leverage (EL) 量化 MoE 相对稠密模型的算力优势，训 300+ 模型给出可预测的 EL 幂律，指导 Ling 系列设计。发布 2025-07-23。

## 摘要
MoE 通过解耦总参与计算成本成为主流缩放架构，但给定 MoE 配置（专家激活比、粒度等）的模型容量难以预测。论文提出 Efficiency Leverage (EL) 量化 MoE 相对等效稠密模型的算力优势，并做大规模实证（训练 300+ 个、最大 28B 参数的模型）系统研究 MoE 架构配置与 EL 的关系。发现 EL 主要由专家激活比与总算力预算驱动，二者均遵循可预测的幂律；专家粒度作为非线性调节器。据此给出统一缩放律，并据其设计/验证 Ling 系列模型。

## 关键技术细节
- 核心指标：Efficiency Leverage (EL) = MoE 相对等效 dense 的算力杠杆。
- 实证规模：训练 300+ 模型，最大 28B 参数。
- 发现：EL 由 expert activation ratio 与 total compute budget 主导，均服从幂律；expert granularity 为非线性因子。
- 产出：MoE 统一缩放律，指导蚂蚁 Ling（如 Ling-lite / Ling-plus / Ling-1T）系列 MoE 配置。
- 机构：蚂蚁集团 inclusionAI / Ling Team。

## 原始链接
- url: https://arxiv.org/abs/2507.17702
- pdf_url: https://arxiv.org/pdf/2507.17702
- github_url: https://github.com/inclusionAI/Ling-V2

## 本地落盘文件
- ../../../sources/llm/2025/ling-moe-scaling-laws.pdf
