---
title: "Baichuan 2: Open Large-scale Language Models"
org: 百川智能（Baichuan Inc.）
country: China
date: 2023-09
type: paper
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2309.10305
pdf_url: https://arxiv.org/pdf/2309.10305
github_url: https://github.com/baichuan-inc/Baichuan2
downloaded: [baichuan2.pdf]
---

## 一句话定位
百川智能 Baichuan 2（7B/13B）技术报告，2.6T token 从零训练，并公开发布从 200B 到 2.6T token 的中间检查点，是研究训练动态的重要一手资料。

## 摘要（3-6 句）
Baichuan 2 是一组 7B 与 13B 参数的多语言大模型，从零开始在 2.6 万亿 token 上训练。在 MMLU、CMMLU、GSM8K、HumanEval 等公开基准上达到或超过同规模开源模型，并在医疗、法律等垂直领域表现突出。报告公开全部预训练检查点（含中间阶段）以帮助社区理解训练动态。还提出 NormHead、Max-z loss 等稳定训练技巧。

## 关键技术细节
- 规模与数据：Baichuan 2-7B 与 13B，均在 2.6T token 上训练（远超 Baichuan 1）。
- 架构表（Table）：7B 用 RoPE，hidden 4096 / FFN 11008 / 32 heads / 32 层 / seq 4096 / maxLR 2e-4；13B 用 ALiBi，hidden 5120 / FFN 13696 / 40 heads / 40 层 / seq 4096 / maxLR 1.5e-4。
- 位置编码差异：7B 用 RoPE，13B 用 ALiBi；作者称两者最终性能接近。
- 激活：SwiGLU（三矩阵 bilinear，FFN 隐维从 4× 降为 8/3×）。
- Tokenizer：BPE（SentencePiece），词表从 64,000 扩至 125,696，字符覆盖率 0.9999，最大 token 长度 32，加入纯空白 token。
- 训练稳定性：NormHead（对输出 embedding/head 做归一化，缓解稀有 token 范数不稳定）；Max-z loss 抑制 logits 漂移。
- 后训练：SFT + RLHF，得到 Baichuan 2-7B-Chat / 13B-Chat。
- 透明度：公开 200B→2.6T 全过程检查点；7B 在 2.6T token 时性能仍在提升。

## 原始链接
- url: https://arxiv.org/abs/2309.10305
- pdf_url: https://arxiv.org/pdf/2309.10305
- github_url: https://github.com/baichuan-inc/Baichuan2

## 本地落盘文件
- ../../../sources/llm/2023/baichuan2.pdf
