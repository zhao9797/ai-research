---
title: "Byte Latent Transformer: Patches Scale Better Than Tokens (BLT)"
org: FAIR at Meta / University of Washington / University of Chicago
country: US
date: 2024-12
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2412.09871
pdf_url: https://arxiv.org/pdf/2412.09871
github_url: https://github.com/facebookresearch/blt
downloaded: [blt.pdf]
---

## 一句话定位
BLT 是 Meta 的无 tokenizer 字节级 LLM：用「下一字节熵」动态切分成可变长 patch 作为计算单元，首次在规模上匹配基于 token 的 LLM 并提升推理效率与鲁棒性。

## 摘要（3-6 句）
BLT 直接在原始字节上建模，不用固定词表。它把字节编码成动态大小的 patch（按下一字节的熵切分：数据越可预测、patch 越长），patch 成为主要计算单元，从而在可预测处省算力、在复杂处分配更多算力。论文给出首个 FLOP 受控的字节级模型扩展研究，规模到 8B 参数、4T 训练字节。结果表明无固定词表的字节模型可扩展，训练与推理效率都因动态长 patch 而提升，且对噪声/拼写更鲁棒。

## 关键技术细节
- 架构：local encoder（字节→patch 表示）+ 大 latent transformer（在 patch 上计算）+ local decoder（patch→字节）。
- 动态 patch 切分：用一个小字节级语言模型估计下一字节熵，按熵阈值切 patch（entropy-based patching），可变长。
- 扩展研究：FLOP-controlled，最大 8B 参数、4T 字节训练；在等 FLOP 下匹配 BPE token 模型并随 patch 变长更省。
- 鲁棒性：对字符级噪声、低资源语言、拼写任务比 BPE token 模型更强。
- 无固定 tokenizer，避免词表偏置与多语种不公平切分。

## 原始链接
- url: https://arxiv.org/abs/2412.09871
- pdf_url: https://arxiv.org/pdf/2412.09871
- github_url: https://github.com/facebookresearch/blt

## 一手源存档（sources/）
- blt.pdf  （PDF 不入 git，走 HF bucket）
