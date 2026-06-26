---
title: "Step-Audio-R1.5 Technical Report"
org: 阶跃星辰 StepFun
country: China
date: 2026-04
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2604.25719
pdf_url: https://arxiv.org/pdf/2604.25719
github_url: https://huggingface.co/stepfun-ai
downloaded: [step-audio-r1.5.pdf]
---

## 一句话定位
阶跃星辰 Step-Audio-R1.5，音频推理大模型，识别并反思 RLVR 在音频上的"可验证奖励陷阱"——纯客观奖励会牺牲对话自然度/韵律/情感连续性。

## 摘要
Step-Audio-R1.5（arXiv 2026-04-28，作者 Yuxin Zhang 等 19 人）研究把 Chain-of-Thought 推理扩展到听觉域的大音频语言模型。主流范式（受文本推理模型成功驱动）压倒性依赖 Reinforcement Learning with Verified Rewards (RLVR)，但当模型被严格优化为把丰富连续的听觉上下文蒸馏成孤立可验证文本标签时，提出根本问题："verifiable reward trap"（可验证奖励陷阱）。RLVR 在标准化客观 benchmark 上得分亮眼，却系统性地损害音频模型真实世界的对话质感：把动态交互降为机械"应答机"，严重损害韵律自然度、情感连续性与用户沉浸感。论文围绕该陷阱给出方法与改进。同系列还有 Step-Audio-R1.1（HF 2026-01）。

## 关键技术细节
- **定位**：大音频语言模型（LALM）的音频 CoT 推理 + RL 后训练反思。
- **核心发现-verifiable reward trap**：RLVR 把连续听觉上下文压成孤立可验证文本标签，损害真实对话质感。
- **后训练-RLVR 局限**：客观 benchmark 高分但损害韵律自然度、情感连续性、用户沉浸感（"应答机"化）。
- **改进方向**：在保留可验证收益同时恢复声学细节/情感连续性（音频对齐与奖励设计）。
- **系列**：Step-Audio-R1.1（2026-01）→ Step-Audio-R1.5（2026-04）。

## 原始链接
- url: https://arxiv.org/abs/2604.25719
- pdf_url: https://arxiv.org/pdf/2604.25719
- HF: https://huggingface.co/stepfun-ai

## 一手源存档（sources/）
- step-audio-r1.5.pdf  （PDF 不入 git，走 HF bucket）
