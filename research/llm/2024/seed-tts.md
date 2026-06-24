---
title: "Seed-TTS: A Family of High-Quality Versatile Speech Generation Models"
org: 字节跳动 Seed (ByteDance Seed)
country: 中国
date: 2024-06
type: arxiv
categories: [架构, 后训练]
url: https://arxiv.org/abs/2406.02430
pdf_url: https://arxiv.org/pdf/2406.02430
github_url: https://github.com/BytedanceSpeech/seed-tts-eval
downloaded: [files/seed-tts.pdf]
---

## 一句话定位
字节 Seed 团队的大规模自回归 TTS 基础模型族，语音自然度/相似度逼近真人，并提出语音因子分解的自蒸馏与 RL 增强鲁棒性。

## 摘要
Seed-TTS 是大规模自回归文本转语音模型族，生成语音几乎与真人无异，在 speaker similarity 与 naturalness 上的客观/主观指标达到甚至匹配真人录音；微调后主观分更高。擅长语音 in-context learning（zero-shot 音色克隆），对情感等属性可控，能为任意说话人生成富表现力的多样语音。还提出用于语音因子分解的自蒸馏方法，以及增强模型鲁棒性/相似度/可控性的强化学习方法。另含全扩散变体 Seed-TTS_DiT（非自回归、端到端时长控制）。

## 关键技术细节（带数字）
- 架构：大规模自回归 TTS（语音 token + 声码器）；另含全扩散变体 Seed-TTS_DiT。
- 能力：zero-shot 语音 in-context learning（音色克隆），speaker similarity / naturalness 匹配真人。
- 自蒸馏：用于 speech factorization（分解音色/内容等因子）。
- 强化学习：RL 增强鲁棒性、说话人相似度与可控性。
- 可控：情感、表现力可控的多样化语音生成。

## 原始链接
- arXiv: https://arxiv.org/abs/2406.02430
- PDF: https://arxiv.org/pdf/2406.02430
- 官方页: https://bytedancespeech.github.io/seedtts_tech_report/

## 本地落盘文件
- ../../../sources/llm/2024/seed-tts.pdf
