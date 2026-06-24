---
title: "CogView: Mastering Text-to-Image Generation via Transformers"
org: 清华 (Tsinghua) / 阿里达摩院 (Alibaba DAMO) / BAAI 智源
country: China
date: 2021-05
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2105.13290
pdf_url: https://arxiv.org/pdf/2105.13290
github_url: https://github.com/THUDM/CogView
downloaded: [arxiv-2105.13290.pdf]
---

## 一句话定位
清华 + 阿里 + 智源的 CogView：40 亿参数 Transformer + VQ-VAE 的中文文本到图像生成模型（中国版 DALL·E），是悟道（WuDao）多模态生态的一部分。

## 摘要（3-6 句）
CogView 用 40 亿参数 Transformer 配 VQ-VAE tokenizer 解决通用领域文本到图像生成问题。论文展示了多种下游微调策略（风格学习、超分、图文排序、时尚设计）以及稳定预训练的方法（如消除 NaN loss）。在 blurred MS COCO 上取得 SOTA FID，优于此前 GAN 模型与同期的 DALL·E。

## 关键技术细节
- 参数：4B Transformer + VQ-VAE 离散图像 tokenizer。
- 方法：把图像离散化为 token，与文本 token 拼接做自回归生成（GPT 式），与 DALL·E 同期同路线。
- 训练稳定性：PB-Relax、Sandwich-LayerNorm 等技巧消除 NaN/上溢，稳定大模型混合精度训练。
- 下游：风格学习、超分辨率、图文 reranking、时尚设计等 finetuning。
- 结果：blurred MS COCO 上 FID SOTA，超过 GAN 与 DALL·E。
- 由清华（Jie Tang/Ming Ding 等）+ 阿里 DAMO + BAAI 联合，属悟道（WuDao）多模态成果，代码在 THUDM/CogView。

## 原始链接
- url: https://arxiv.org/abs/2105.13290
- pdf_url: https://arxiv.org/pdf/2105.13290
- github_url: https://github.com/THUDM/CogView

## 本地落盘文件
- ../../../sources/llm/2021/arxiv-2105.13290.pdf
