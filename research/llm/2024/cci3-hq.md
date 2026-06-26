---
title: "CCI3.0-HQ: a large-scale Chinese dataset of high quality designed for pre-training large language models"
org: 北京智源 (BAAI)
country: 中国
date: 2024-10
type: arxiv
categories: [预训练数据]
url: https://arxiv.org/abs/2410.18505
pdf_url: https://arxiv.org/pdf/2410.18505
github_url: https://huggingface.co/datasets/BAAI/CCI3-HQ
downloaded: [files/cci3-hq.pdf]
---

## 一句话定位
智源开源的 500GB 高质量中文预训练语料（CCI3.0 的精选子集），用两阶段混合过滤流水线把 Qwen2-72B 的质量判别能力蒸馏进 0.5B 分类器。

## 摘要
CCI3.0-HQ 是 Chinese Corpora Internet 3.0（CCI3.0）的 500GB 高质量子集，用新颖的两阶段混合过滤流水线显著提升数据质量。评估方式：从头训练 0.5B 模型在 100B token 上，于 10 个零样本基准上超过用 CCI3.0、SkyPile、WanjuanV1 训练的模型。该过滤流程把 Qwen2-72B-instruct 的判别能力有效蒸馏进 0.5B 紧凑分类器，在中文网页数据分类上取得最优 F1。

## 关键技术细节（带数字）
- 规模：500GB 高质量中文语料（CCI3.0 子集）。
- 过滤：两阶段混合过滤流水线（规则 + 学习式质量分类器）。
- 质量分类器：0.5B 模型，蒸馏自 Qwen2-72B-instruct，中文网页分类 F1 最优。
- 验证：用 100B token 从头训 0.5B 模型，10 项零样本基准超过 CCI3.0/SkyPile/WanjuanV1。
- 开放：数据集与分类器开源（HF: BAAI/CCI3-HQ）。

## 原始链接
- arXiv: https://arxiv.org/abs/2410.18505
- PDF: https://arxiv.org/pdf/2410.18505
- HF 数据集: https://huggingface.co/datasets/BAAI/CCI3-HQ

## 一手源存档（sources/）
- cci3-hq.pdf  （PDF 不入 git，走 HF bucket）
