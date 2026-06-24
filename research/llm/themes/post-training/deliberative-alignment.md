---
title: Deliberative Alignment: Reasoning Enables Safer Language Models
org: OpenAI
country: US
date: 2024-12
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2412.16339
pdf_url: https://arxiv.org/pdf/2412.16339
downloaded: [deliberative-alignment.pdf]
---

## 一句话定位
Deliberative Alignment：教推理模型在回答前显式"推理安全规范（safety spec）"再作答，把安全策略文本直接喂给模型做 CoT 审议，是 o 系列模型的安全对齐方法。

## 摘要（3-6 句）
Deliberative Alignment 让模型在推理链中显式回忆并应用人写的安全规范，再给出答案，而非仅靠隐式学到的拒绝模式。训练分两步：(1) SFT——用 (prompt, 含引用安全规范的 CoT, 回答) 数据教模型在思考时引用规范；这些 CoT 数据由模型自生成、用一个"裁判"模型按规范打分筛选，无需人工标注 CoT；(2) RL——用按安全规范打分的奖励模型做强化学习，进一步优化审议质量。该方法显著提升 o1 类模型对越狱的鲁棒性与对良性请求的不过度拒绝，且对分布外安全场景泛化更好。

## 关键技术细节
- 核心：把安全 spec（policy 文本）直接给模型，让其在 CoT 中显式推理"该请求是否违规、应如何回应"。
- 阶段一 SFT：用 (prompt, CoT-with-spec-citation, output) 训练；数据由基础推理模型生成 + judge 模型按 spec 过滤（合成、无需人工标 CoT）。
- 阶段二 RL：reward model 依据安全 spec 给信号，强化高质量审议；用 o 系列的 RL 训练机制。
- 优势：对越狱（StrongREJECT 等）更鲁棒、对良性边界请求过度拒绝更少、对未见安全场景泛化更好。
- 适用：OpenAI o1 / o3-mini 等推理模型的安全对齐方案，把"安全"也变成可推理的任务。

## 原始链接
- url: https://arxiv.org/abs/2412.16339
- pdf_url: https://arxiv.org/pdf/2412.16339

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/deliberative-alignment.pdf
