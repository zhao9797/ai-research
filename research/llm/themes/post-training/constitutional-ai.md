---
title: "Constitutional AI: Harmlessness from AI Feedback"
org: Anthropic
country: US
date: 2022-12
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2212.08073
pdf_url: https://arxiv.org/pdf/2212.08073
downloaded: [constitutional-ai.pdf]
---

## 一句话定位
Constitutional AI（CAI）：用一部"宪法"（自然语言原则）让模型自我批评-修订生成无害数据，并用 AI 反馈代替人类无害性标注（RLAIF 的源头）。

## 摘要（3-6 句）
CAI 用一组人写的原则（"宪法"）来训练无害助手，几乎不用人类无害性标签。分两阶段：(1) 监督阶段——模型对有害提示先回答，再依据宪法原则自我批评并修订，得到修订后回答用于 SFT；(2) RL 阶段（RLAIF）——让模型依据宪法对成对回答做偏好判断，生成 AI 偏好标签训练偏好模型，再做 RL。结果是模型既无害又不过度回避（会解释拒绝理由而非简单回绝），且无害性偏好数据完全由 AI 生成，大幅减少人类标注有害内容的需要。

## 关键技术细节
- 两阶段：SL-CAI（自我批评+修订 → SFT）+ RL-CAI（AI 反馈偏好 → 偏好模型 → RL）。
- 宪法：约十余条自然语言原则（基于人权、避免有害/歧视/操纵等）；偏好判断时随机采样原则作为评判依据。
- AI 反馈：用 few-shot prompt 让模型在成对回答中选更符合宪法者，产出偏好标签（无害性维度）。有用性仍用人类偏好。
- 链式思维：偏好评判时让模型先 CoT 推理再给判断，提升一致性。
- 效果：相比纯 RLHF 基线，在无害性-有用性 Pareto 前沿上更优，且回答更"非回避式"（non-evasive）。

## 原始链接
- url: https://arxiv.org/abs/2212.08073
- pdf_url: https://arxiv.org/pdf/2212.08073

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/constitutional-ai.pdf
