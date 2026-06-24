---
title: BitNet: Scaling 1-bit Transformers for Large Language Models
org: Microsoft Research
country: US
date: 2023-10
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2310.11453
pdf_url: https://arxiv.org/pdf/2310.11453
downloaded: [bitnet.pdf]
---

## 一句话定位
微软 1-bit Transformer，BitLinear 从头训练 1-bit 权重，开启极端低比特 LLM 路线。

## 摘要
大模型尺寸带来部署与能耗挑战。BitNet 是可扩展、稳定的 1-bit Transformer 架构：引入 BitLinear 作为 nn.Linear 的即插替换，从头训练 1-bit 权重。语言建模实验显示 BitNet 在大幅降低显存与能耗的同时性能有竞争力(对比 8-bit 量化与 FP16 baseline)，且展现类全精度 Transformer 的 scaling law，具备扩展到更大模型的潜力。

## 关键技术细节
- BitLinear：权重二值化(±1)，激活量化为 8-bit；训练时用 STE 直通估计反传、保留 latent 高精度权重。
- 关键：是“从头训练 1-bit”而非训练后量化(PTQ)。
- 收益：显存与能耗显著下降，矩阵乘可用加法实现。
- scaling：1-bit BitNet 随规模增长呈现与 FP16 Transformer 类似的 scaling law。
- 对比：优于 8-bit 量化方法与 FP16 baseline 的能效/显存权衡。
- 后续：通向 2024 的 BitNet b1.58(三值 {-1,0,1})。

## 原始链接
- url: https://arxiv.org/abs/2310.11453
- pdf_url: https://arxiv.org/pdf/2310.11453

## 本地落盘文件
- ../../../sources/llm/2023/bitnet.pdf
