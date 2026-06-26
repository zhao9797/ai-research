---
title: "OPT: Open Pre-trained Transformer Language Models"
org: Meta AI
country: US
date: 2022-05
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2205.01068
pdf_url: https://arxiv.org/pdf/2205.01068
github_url: https://github.com/facebookresearch/metaseq
downloaded: [opt.pdf]
---

## 一句话定位
Meta 开源 125M–175B 的 decoder-only Transformer 套件，OPT-175B 对标 GPT-3 但碳足迹仅 1/7，并公开训练日志。

## 摘要
OPT 是一套 125M 到 175B 参数的 decoder-only 预训练 Transformer，Meta 力图负责任地向研究者完整开放权重。OPT-175B 性能与 GPT-3 相当，但开发碳足迹仅为 GPT-3 的 1/7。Meta 同时公开了记录基础设施挑战的训练 logbook 与全部模型的实验代码。

## 关键技术细节
- 模型规模：125M、350M、1.3B、2.7B、6.7B、13B、30B、66B、175B。
- 训练数据：约 180B token（约 800GB），混合 RoBERTa 语料、Pile 子集、PushShift Reddit。
- Infra：OPT-175B 在 992 块 NVIDIA A100 80GB 上训练，使用 Megatron-LM 张量并行 + 全分片数据并行（FSDP）；训练中频繁遇到 loss 发散、硬件故障，需多次重启（日志公开）。
- 精度：FP16 训练。
- 碳足迹：约为 GPT-3 训练的 1/7。
- 开放：175B 需研究申请，<66B 权重直接公开；training logbook 详述工程踩坑。

## 原始链接
- url: https://arxiv.org/abs/2205.01068
- pdf_url: https://arxiv.org/pdf/2205.01068
- github_url: https://github.com/facebookresearch/metaseq

## 一手源存档（sources/）
- opt.pdf  （PDF 不入 git，走 HF bucket）
