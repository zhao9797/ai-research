---
title: "ST-MoE: Designing Stable and Transferable Sparse Expert Models"
org: Google
country: US
date: 2022-02
type: paper
categories: [架构]
url: https://arxiv.org/abs/2202.08906
pdf_url: https://arxiv.org/pdf/2202.08906
downloaded: [st-moe.pdf]
---

## 一句话定位
ST-MoE 系统解决稀疏专家模型的训练不稳定与微调迁移差问题，提出 router z-loss，训练出 269B 参数（32B 激活）的 ST-MoE-32B，在多项 NLP 基准上达 SOTA。

## 摘要（3-6 句）
稀疏 MoE 虽算力高效，但训练不稳定、微调时质量不如稠密模型。ST-MoE 提出 router z-loss（惩罚路由 logits 的过大数值）显著提升训练稳定性且不损质量，并系统研究微调超参、容量因子、专家数等设计选择。作者训练出 269B 总参、约 32B 激活的 ST-MoE-32B，在 SuperGLUE、摘要、闭卷问答等多个迁移任务上取得 SOTA，是首个在迁移学习上稳定超过稠密模型的大型稀疏模型。

## 关键技术细节
- router z-loss：对 router logits 的对数配分函数加正则，抑制数值爆炸，稳定 bf16 训练。
- 规模：ST-MoE-32B，269B 总参数、约 32B 激活参数。
- 系统研究：稀疏模型微调易过拟合，需更小 batch、更高学习率；容量因子、专家 dropout 的取舍。
- 结果：SuperGLUE、XSum、CNN-DM、ARC、闭卷 TriviaQA 等多任务 SOTA。
- 给出稀疏模型设计的实用配方，影响后续大量 MoE 工作。

## 原始链接
- url: https://arxiv.org/abs/2202.08906
- pdf_url: https://arxiv.org/pdf/2202.08906

## 一手源存档（sources/）
- st-moe.pdf  （PDF 不入 git，走 HF bucket）
