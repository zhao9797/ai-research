---
title: "Hunyuan-TurboS: Advancing Large Language Models through Mamba-Transformer Synergy and Adaptive Chain-of-Thought"
org: Tencent (腾讯混元)
country: China
date: 2025-05
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2505.15431
pdf_url: https://arxiv.org/pdf/2505.15431
downloaded: [hunyuan-turbos.pdf]
---

## 一句话定位
腾讯 Hunyuan-TurboS：Mamba-Transformer 混合 MoE 架构 + 自适应长短 CoT，后训练含多阶段 SFT 与 RL（含可验证奖励），实现"按难度决定是否深思考"。

## 摘要（3-6 句）
Hunyuan-TurboS 采用 Mamba-Transformer 混合架构（Mamba 擅长长序列、低成本，Transformer 擅长上下文建模）的 MoE 大模型，并引入自适应思维链（adaptive CoT）：对简单问题走 no-thinking 快速路径，对复杂问题自动切换到深度思考，兼顾效率与能力。后训练流程含监督微调、自适应长短 CoT 融合、以及多轮强化学习（含数学/代码等可验证奖励与通用偏好对齐）。在多项基准上达到顶尖水平，是混合架构 + 推理后训练的代表。

## 关键技术细节
- 架构：Mamba-Transformer 混合 MoE（约 560B 总参 / 56B 激活，按报告），结合 SSM（Mamba2）与注意力层。
- adaptive CoT：根据问题复杂度自适应决定是否进行长思考（no-think 快路径 vs deep-think）。
- 后训练：SFT → 长短 CoT 融合 → 多阶段 RL（数学/代码可验证奖励 + 通用奖励模型对齐）。
- 优势：混合架构降低长上下文推理成本；自适应思考平衡 token 效率与准确率。
- 评测：在数学、推理、对齐等基准达到与顶尖模型相当水平（详见报告表）。

## 原始链接
- url: https://arxiv.org/abs/2505.15431
- pdf_url: https://arxiv.org/pdf/2505.15431

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/hunyuan-turbos.pdf
