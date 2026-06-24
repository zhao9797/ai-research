---
title: The Lessons of Developing Process Reward Models in Mathematical Reasoning
org: Qwen Team, Alibaba
country: China
date: 2025-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2501.07301
pdf_url: https://arxiv.org/pdf/2501.07301
github_url: https://huggingface.co/Qwen/Qwen2.5-Math-PRM-7B
downloaded: [prm-lessons-qwen.pdf]
---

## 一句话定位
Qwen 团队对过程奖励模型（PRM）的系统复盘：揭示 MC-估计自动标注与 best-of-n 评测的缺陷，提出共识过滤机制，发布 Qwen2.5-Math-PRM。

## 摘要（3-6 句）
本文系统研究 PRM 的训练与评测陷阱。发现：(1) 用蒙特卡洛估计自动标步骤标签（如 Math-Shepherd 式）效果不如人工/LLM-as-judge，因为 MC 估计把"最终答案对"误判为"过程对"，引入大量标签噪声；(2) 常用 best-of-n 评测会偏向"答案对但过程错"的样本，无法真实反映 PRM 的过程纠错能力。为此提出结合 MC 估计与 LLM-as-judge 的共识过滤（consensus filtering），只保留两者一致的步骤标签，显著提升 PRM 质量。基于此发布 Qwen2.5-Math-PRM-7B / 72B，在 ProcessBench 等过程评测上 SOTA。

## 关键技术细节
- 发现一：纯 MC 估计标注的 PRM 不如人工/LLM judge——MC 把"能导出正确答案"当作步骤正确，混淆结果正确与过程正确。
- 发现二：best-of-n 评测有偏，奖励"对答案错过程"样本，掩盖 PRM 真实定位错误步骤的能力。
- 共识过滤：同时用 MC 估计与 LLM-as-judge 标步骤，仅保留二者一致的样本训练 PRM，降噪。
- 评测改进：用 ProcessBench 等直接评估"找到第一个错误步骤"的能力，而非仅 best-of-n。
- 产出：Qwen2.5-Math-PRM-7B / 72B，开源；在过程错误定位上超过同类 PRM。

## 原始链接
- url: https://arxiv.org/abs/2501.07301
- pdf_url: https://arxiv.org/pdf/2501.07301
- model: https://huggingface.co/Qwen/Qwen2.5-Math-PRM-7B

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/prm-lessons-qwen.pdf
