---
title: Qwen3 Technical Report
org: Qwen Team, Alibaba
country: China
date: 2025-05
type: report
categories: [后训练, 架构, 预训练数据]
url: https://arxiv.org/abs/2505.09388
pdf_url: https://arxiv.org/pdf/2505.09388
github_url: https://github.com/QwenLM/Qwen3
downloaded: [qwen3.pdf]
---

## 一句话定位
Qwen3：把"思考/非思考"两种模式统一进一个模型（thinking budget 可控），后训练用四阶段强到弱蒸馏 + RL，并提出 strong-to-weak distillation 把大模型推理蒸给小模型。

## 摘要（3-6 句）
Qwen3 系列含稠密（0.6B–32B）与 MoE（30B-A3B、235B-A22B）模型。核心创新是把 thinking mode（长 CoT 推理）与 non-thinking mode（快速直答）融合进同一模型，用户可设置"思考预算"（thinking budget）在二者间平滑权衡。后训练采用四阶段：长 CoT 冷启动 SFT → 推理 RL（可验证奖励）→ thinking/non-thinking 模式融合 SFT → 通用 RL。对小模型则用 strong-to-weak distillation（用大 Qwen3 的输出蒸馏），比直接 RL 更省更好。模型覆盖 119 种语言，旗舰 235B-A22B 达开放权重 SOTA。

## 关键技术细节
- 模型：稠密 0.6B/1.7B/4B/8B/14B/32B + MoE Qwen3-30B-A3B（3B 激活）、Qwen3-235B-A22B（22B 激活）。
- 预训练：约 36T tokens、119 种语言。
- 统一思考模式：单模型支持 thinking / non-thinking，thinking budget 可控（限制思考 token 数）。
- 后训练四阶段：(1) long-CoT 冷启动 SFT；(2) reasoning RL（GRPO 类，规则可验证奖励）；(3) thinking-mode fusion（把两模式融合的 SFT）；(4) general RL（覆盖 20+ 任务的通用对齐 RL）。
- strong-to-weak 蒸馏：旗舰/大模型 → 轻量模型，远比对小模型直接做 RL 高效。
- 结果：旗舰 235B-A22B 在代码、数学、agent 任务上对标顶尖开放/闭源模型。

## 原始链接
- url: https://arxiv.org/abs/2505.09388
- pdf_url: https://arxiv.org/pdf/2505.09388
- github_url: https://github.com/QwenLM/Qwen3

## 一手源存档（sources/）
- qwen3.pdf  （PDF 不入 git，走 HF bucket）
