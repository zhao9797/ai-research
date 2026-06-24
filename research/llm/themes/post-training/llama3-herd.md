---
title: The Llama 3 Herd of Models
org: Meta
country: US
date: 2024-07
type: report
categories: [后训练, 预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2407.21783
pdf_url: https://arxiv.org/pdf/2407.21783
downloaded: [llama3-herd.pdf]
---

## 一句话定位
Llama 3 技术报告：Meta 把后训练简化为"SFT + 拒绝采样 + DPO 的多轮迭代"，明确放弃 PPO，详细公开数据配比、能力专项（代码/数学/工具/多语言）与安全对齐。

## 摘要（3-6 句）
Llama 3 系列含 8B/70B/405B 稠密模型，405B 用 15.6T tokens 预训练、上下文扩展到 128K。后训练采用多轮迭代：每轮先训奖励模型，用其做拒绝采样（rejection sampling）筛选高质量回答做 SFT，再用 DPO 做偏好对齐——Meta 明确表示因稳定性与可扩展性选择 DPO 而非 PPO。报告极详尽地公开了 SFT 数据构成、各能力（代码、数学/推理、工具使用、长上下文、多语言、事实性）的专项数据与方法，以及安全（Llama Guard 3、CyberSecEval）与红队流程。

## 关键技术细节
- 模型：8B/70B/405B 稠密；405B 预训练 15.6T tokens，上下文 128K，tokenizer 128K 词表，GQA。
- 训练算力：405B 用约 16K H100、BF16，约 3.8×10^25 FLOPs；4D 并行（TP+PP+DP+CP，context parallel）。
- 后训练循环：reward model → rejection sampling（best-of-N 取高 RM 分）→ SFT → DPO，迭代 6 轮（每轮换新偏好/SFT 数据）。
- 明确弃用 PPO：选 DPO 因更稳定、可扩展；DPO 中对格式 token 做 mask、加 NLL 正则。
- 能力专项：代码、数学与推理（含合成数据、step-wise 验证）、工具使用（Brave/Wolfram/Python）、长上下文、多语言、可控性、事实性。
- 安全：Llama Guard 3、Prompt Guard、CyberSecEval 2；系统级安全。

## 原始链接
- url: https://arxiv.org/abs/2407.21783
- pdf_url: https://arxiv.org/pdf/2407.21783

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/llama3-herd.pdf
