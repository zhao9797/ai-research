---
title: "Baichuan-7B: 开源可商用大规模预训练语言模型（官方 GitHub）"
org: 百川智能（Baichuan Inc.）
country: China
date: 2023-06
type: github
categories: [预训练数据, 架构]
url: https://github.com/baichuan-inc/Baichuan-7B
pdf_url:
github_url: https://github.com/baichuan-inc/Baichuan-7B
downloaded: [baichuan-7b-readme.md]
---

## 一句话定位
百川智能首个开源模型 Baichuan-7B（2023-06）：1.2T token 训练的 7B 中英双语基座，C-Eval/MMLU 同尺寸最佳，是 Baichuan 2 之前的奠基一手发布。

## 摘要（3-6 句）
Baichuan-7B 是百川智能开发的开源可商用大规模预训练语言模型，基于 Transformer 结构，在约 1.2 万亿 tokens 上训练的 70 亿参数模型，支持中英双语，上下文窗口 4096。在标准中英 benchmark（C-Eval / MMLU）上取得同尺寸最佳效果。2023-09 百川进一步发布 Baichuan 2（7B/13B）。

## 关键技术细节
- 规模：7B 参数；上下文窗口 4096。
- 数据：约 1.2T token，中英双语。
- 架构：标准 Transformer（Decoder-only）；RoPE 位置编码、SwiGLU 激活、RMSNorm（LLaMA 风格）。
- Tokenizer：BPE（SentencePiece），词表约 64,000。
- 性能：C-Eval / MMLU 同尺寸最佳（5-shot）。
- 商用：开源可商用。
- 后续：2023-09-06 发布 Baichuan 2（见 baichuan2.md，2.6T token、NormHead 等）。

## 原始链接
- url: https://github.com/baichuan-inc/Baichuan-7B
- github_url: https://github.com/baichuan-inc/Baichuan-7B

## 本地落盘文件
- ../../../sources/llm/2023/baichuan-7b-readme.md
