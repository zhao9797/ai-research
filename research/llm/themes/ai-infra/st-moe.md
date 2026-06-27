---
title: "ST-MoE: Designing Stable and Transferable Sparse Expert Models"
org: Google
country: US
date: 2022-02
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2202.08906
pdf_url: https://arxiv.org/pdf/2202.08906
downloaded: [st-moe-2202.08906.pdf]
---

## 一句话定位
系统研究 MoE 的训练稳定性与微调可迁移性，提出 router z-loss 等技巧，训练 269B 稀疏 MoE（ST-MoE-32B）在多任务上达 SOTA。

## 摘要（3-6 句）
稀疏专家模型常有训练不稳定与微调过拟合两大痛点。ST-MoE 通过大量消融找出稳定性-质量折中，提出 router z-loss（约束 router logits 量级）显著稳定训练且略增质量，并给出微调超参与容量配置的经验法则。作者训练 ST-MoE-32B（269B 总参、约 32B 激活量级稀疏模型），在 SuperGLUE、ARC、推理与摘要等多基准上取得 SOTA，证明 MoE 可在 transfer learning 中可靠胜出。

## 关键技术细节
- router z-loss：惩罚 gating logits 的 log-sum-exp，抑制数值不稳定（成为后续 MoE 标配，如 DeepSeekMoE 也借鉴）。
- 训练稳定性消融：精度、初始化、capacity factor、专家数与质量-稳定 tradeoff。
- ST-MoE-32B：稀疏 encoder-decoder，269B 总参数；多任务 SOTA（SuperGLUE 等）。
- 微调建议：sparse 模型对超参更敏感，给出 batch size/学习率配方。

## 原始链接
- url: https://arxiv.org/abs/2202.08906
- pdf_url: https://arxiv.org/pdf/2202.08906

## 一手源存档（sources/）
- [st-moe-2202.08906.pdf](https://arxiv.org/pdf/2202.08906)  （arXiv 原文 PDF，不入 git）
