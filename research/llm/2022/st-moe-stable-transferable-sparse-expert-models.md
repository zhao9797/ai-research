---
title: "ST-MoE: Designing Stable and Transferable Sparse Expert Models"
org: Google Research (Brain)
country: US
date: 2022-02
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2202.08906
pdf_url: https://arxiv.org/pdf/2202.08906
github_url:
downloaded: [st-moe.pdf]
---

## 一句话定位
解决 MoE 稀疏专家模型的训练不稳定与微调质量问题，269B 稀疏模型 ST-MoE-32B 首次在迁移学习上达到稠密 SOTA。

## 摘要
规模为 NLP 开辟新前沿但成本高昂。MoE 与 Switch Transformer 被提出作为通向更大更强模型的节能路径，但训练不稳定与微调质量不确定阻碍其推进 SOTA。本文聚焦这些问题并作为设计指南。最终将稀疏模型扩展到 269B 参数、计算成本相当于 32B 稠密 encoder-decoder（ST-MoE-32B）。首次让稀疏模型在迁移学习上达到 SOTA，覆盖推理（SuperGLUE、ARC）、摘要（XSum、CNN-DM）、闭卷 QA（WebQA、NQ）、对抗任务（Winogrande、ANLI R3）。

## 关键技术细节
- ST-MoE-32B：269B 总参数，计算成本约等于 32B 稠密模型；encoder-decoder 架构。
- 稳定性创新：router z-loss（抑制 logits 爆炸）改善训练稳定与质量；分析精度/初始化对稳定性的影响。
- 可迁移性：研究专家数、容量因子、微调超参对下游迁移的影响，给出系统设计指南。
- 路由：top-2 token routing；分析负载均衡损失。
- 是 2022 年 MoE 工程的集大成"设计手册"，影响后续 GLaM、Mixtral、DeepSeek-MoE 等。

## 原始链接
- url: https://arxiv.org/abs/2202.08906
- pdf_url: https://arxiv.org/pdf/2202.08906

## 本地落盘文件
- ../../../sources/llm/2022/st-moe.pdf
