---
title: Ling 2.0 — Every Activation Boosted: Scaling General Reasoner to 1 Trillion Open Language Foundation (含 Ling-1T)
org: 蚂蚁集团 百灵 / inclusionAI (Ant Group Ling Team)
country: China
date: 2025-10
type: paper
categories: [架构, 预训练数据, AI infra, 后训练]
url: https://arxiv.org/abs/2510.22115
pdf_url: https://arxiv.org/pdf/2510.22115
github_url: https://github.com/inclusionAI/Ling-V2
downloaded: [ling-2.0.pdf]
---

## 一句话定位
蚂蚁百灵 Ling 2.0 系列（16B 到 1T 统一 MoE 范式），含旗舰 Ling-1T，高稀疏 + 跨尺度一致 + 经验缩放律，活跃算力效率较稠密最高 7 倍。发布 2025-10-25。

## 摘要
Ling 2.0 是面向推理的语言基座系列，秉持"每次激活都增益推理能力"理念，在统一 MoE 范式下从数百亿扩展到 1 万亿参数，强调高稀疏、跨尺度一致性与经验缩放律指导的效率。系列含三个 non-thinking（instruct）模型——Ling-mini-2.0、Ling-flash-2.0、Ling-1T（16B 到 1T 总参），相比稠密对应模型实现最高 7 倍的活跃算力效率。整合了架构、训练、infra 等多项协同创新。

## 关键技术细节
- 统一 MoE 范式：16B（mini）/ 100B 级（flash）/ 1T（Ling-1T）跨尺度一致设计；高稀疏（low activation ratio）。
- 设计依据：经验缩放律（与 Ant 的 Efficiency Leverage 缩放律一脉相承）。
- 效率：活跃算力效率较 dense 最高 7×。
- 训练：大规模高质量预训练 + 后训练；FP8 等 infra 优化。
- 定位：non-thinking（instruct）系列，强通用推理。
- 开源：GitHub inclusionAI/Ling-V2。

## 原始链接
- url: https://arxiv.org/abs/2510.22115
- pdf_url: https://arxiv.org/pdf/2510.22115
- github_url: https://github.com/inclusionAI/Ling-V2

## 本地落盘文件
- ../../../sources/llm/2025/ling-2.0.pdf
