---
title: "MambaByte: Token-free Selective State Space Model"
org: Cornell University
country: US
date: 2024-01
type: paper
categories: [架构]
url: https://arxiv.org/abs/2401.13660
pdf_url: https://arxiv.org/pdf/2401.13660
downloaded: [mambabyte.pdf]
---

## 一句话定位
MambaByte 把 Mamba（选择性 SSM）直接在原始字节序列上自回归训练，去掉子词分词的归纳偏置；凭借固定大小的循环记忆状态，避开字节序列变长后 Transformer 内存随长度暴涨的问题，在语言建模上与子词 Transformer 竞争甚至反超。

## 摘要（3-6 句）
Token-free 模型直接从原始字节学习、移除子词分词偏置，但字节序列显著更长，标准自回归 Transformer 因有效内存随长度增长而扩展性差。Mamba 的 SSM 提供固定大小记忆状态与高效解码，是理想替代。MambaByte 是 Mamba SSM 在字节序列上的 token-free 适配；建模上与 SOTA 子词 Transformer 竞争甚至更优，同时保留 token-free 的优点（如对噪声更鲁棒）。效率上，作者提出带「分词草稿 + 字节级验证」的投机解码适配，使标准 MambaByte 推理加速 2.6×，解码效率逼近子词版 Mamba。发表于 COLM 2024。

## 关键技术细节
- 词表：字节级 vocab = 256，无子词分词器；输入即原始 UTF-8 字节。
- 骨干：Mamba 选择性 SSM（A、B、C 共享于各维，Δ 各异，softplus 保正），固定大小循环状态独立于上下文长度。
- 模型档位：MambaByte-353M、972M、1.6B；基准在 PG19（8,192 连续字节）上评测。
- 对照基线：与 MegaByte（用固定 patch 压缩字节作子词类比，如 patch=4/8）、Gated-S4D、字节级 Transformer、PerceiverAR 比较；分 compute-matched 与 parameter-matched 两种公平设置。MambaByte-972M 相对 MegaByte-1.3B+350M 的训练 FLOPs 比约 0.54:1。
- 投机解码：tokenized drafting + byte-level verification，推理加速 2.6×，解码效率与子词 Mamba 接近。
- 鲁棒性：对字符级噪声更鲁棒，体现 token-free 优势。
- 作者：Junxiong Wang、Tushaar Gangavarapu、Jing Nathan Yan、Alexander M. Rush。

## 原始链接
- url: https://arxiv.org/abs/2401.13660
- pdf_url: https://arxiv.org/pdf/2401.13660

## 一手源存档（sources/）
- mambabyte.pdf  （PDF 不入 git，走 HF bucket）
