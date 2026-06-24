---
title: Robust Speech Recognition via Large-Scale Weak Supervision (Whisper)
org: OpenAI
country: US
date: 2022-12
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2212.04356
pdf_url: https://arxiv.org/pdf/2212.04356
github_url: https://github.com/openai/whisper
downloaded: [whisper.pdf]
---

## 一句话定位
OpenAI 用 68 万小时弱监督多语言多任务音频训练的 Whisper，zero-shot 即媲美有监督 SOTA，开源权重与推理代码。

## 摘要
研究仅用"预测大量互联网音频转写"训练的语音处理系统的能力。当扩展到 68 万小时多语言多任务监督时，所得模型泛化良好，在标准基准上常与此前全监督结果竞争，但是在 zero-shot 迁移设置下无需任何微调。与人类相比，模型接近其准确率与鲁棒性。OpenAI 发布模型与推理代码作为后续稳健语音处理的基础。

## 关键技术细节
- 架构：标准 encoder-decoder Transformer（seq2seq），把语音识别/翻译/语种识别/时间戳统一为序列预测任务。
- 训练数据：680,000 小时弱监督音频-文本对（其中约 11.7 万小时多语言、12.5 万小时翻译数据）。
- 多任务格式：用特殊 token 指定任务（转写/翻译/语种/时间戳），单模型多任务。
- 规模：tiny→large 多档（最大 1.55B 参数）。
- zero-shot：无需针对数据集微调，鲁棒性显著优于有监督模型（对口音、噪声、领域偏移）。
- 开源：权重 + 推理代码全公开，成为业界事实标准 ASR。

## 原始链接
- url: https://arxiv.org/abs/2212.04356
- pdf_url: https://arxiv.org/pdf/2212.04356
- github_url: https://github.com/openai/whisper

## 本地落盘文件
- ../../../sources/llm/2022/whisper.pdf
