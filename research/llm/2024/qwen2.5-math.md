---
title: "Qwen2.5-Math Technical Report: Toward Mathematical Expert Model via Self-Improvement"
org: 阿里巴巴 Qwen Team
country: 中国
date: 2024-09
type: arxiv
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2409.12122
pdf_url: https://arxiv.org/pdf/2409.12122
github_url: https://github.com/QwenLM/Qwen2.5-Math
downloaded: [files/qwen2.5-math.pdf]
---

## 一句话定位
数学专用模型系列，核心是"自我改进（self-improvement）"贯穿预训练→后训练→推理，支持 CoT 与 TIR（工具集成推理）。

## 摘要
Qwen2.5-Math 及 Instruct 版（1.5B/7B/72B）把"自我改进"理念贯穿全流程：(1) 预训练用 Qwen2-Math-Instruct 生成大规模高质量数学数据；(2) 后训练用对 Qwen2-Math-Instruct 大规模采样训练奖励模型（RM），并用 RM 迭代演化 SFT 数据，再做 RL；(3) 推理用 RM 指导采样。支持中英双语，CoT 与 Tool-Integrated Reasoning（TIR）。

## 关键技术细节（带数字）
- 规模：1.5B / 7B / 72B（Base 与 Instruct）。
- 自我改进闭环：Qwen2-Math-Instruct 生成数据 → 训练 RM → RM 迭代演化数据 → SFT + RL → RM 指导推理。
- 后训练：奖励模型 + GRPO 强化学习。
- 推理模式：CoT + TIR（工具集成推理，调用 Python）。
- 性能：Qwen2.5-Math-72B-Instruct 在 MATH/AIME/AMC 等竞赛级基准达开源 SOTA。

## 原始链接
- arXiv: https://arxiv.org/abs/2409.12122
- PDF: https://arxiv.org/pdf/2409.12122
- GitHub: https://github.com/QwenLM/Qwen2.5-Math

## 一手源存档（sources/）
- qwen2.5-math.pdf  （PDF 不入 git，走 HF bucket）
