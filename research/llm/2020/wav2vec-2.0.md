---
title: wav2vec 2.0 — A Framework for Self-Supervised Learning of Speech Representations
org: Meta / Facebook AI Research (FAIR)
country: US
date: 2020-06
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2006.11477
pdf_url: https://arxiv.org/pdf/2006.11477
github_url: https://github.com/facebookresearch/fairseq
downloaded: [arxiv-2006.11477.pdf]
---

## 一句话定位
wav2vec 2.0 用对比式自监督在原始语音波形上预训练 + 离散量化码本 + Transformer 上下文网络，仅需极少标注即达强 ASR 性能，是语音自监督预训练的里程碑。

## 摘要（3-6 句）
wav2vec 2.0 先用 CNN 特征编码器把原始波形编码为隐表示，再对其做掩码并用 Transformer 上下文网络预测被掩码片段的量化表示（对比学习目标 + 码本多样性损失）。预训练后只用很少标注数据微调即可在 LibriSpeech 上取得 SOTA。仅用 10 分钟标注（加 5.3 万小时无标注预训练）即可达到 test-clean/other 词错率 4.8%/8.2%，展示了语音领域“无标注预训练 + 少量微调”的巨大潜力。

## 关键技术细节
- 结构：CNN 特征编码器（原始波形 → 隐表示）→ 掩码 → Transformer 上下文网络；量化模块用乘积量化（Gumbel-softmax 选码字）。
- 目标：对比损失（在掩码位置区分真实量化表示 vs 干扰项）+ 码本多样性损失（鼓励均匀使用码字）。
- 模型：BASE（约 95M）/ LARGE（约 317M）参数。
- 数据：LibriSpeech 960h 或 LibriVox 5.3 万小时无标注预训练。
- 关键结果：全部 960h 标注下 test-clean/other WER 1.8%/3.3%；仅 10 分钟标注 + 53k 小时无标注预训练即达 4.8%/8.2%。
- 端到端联合学习离散语音单元与上下文表示。

## 原始链接
- url: https://arxiv.org/abs/2006.11477
- pdf_url: https://arxiv.org/pdf/2006.11477
- github_url: https://github.com/facebookresearch/fairseq

## 一手源存档（sources/）
- [arxiv-2006.11477.pdf](https://arxiv.org/pdf/2006.11477)  （arXiv 原文 PDF，不入 git）
