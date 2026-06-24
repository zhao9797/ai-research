---
title: "Alpaca: A Strong, Replicable Instruction-Following Model"
org: Stanford CRFM
country: US
date: 2023-03
type: blog
categories: [后训练]
url: https://crfm.stanford.edu/2023/03/13/alpaca.html
downloaded: [alpaca-stanford-crfm.html]
---

## 一句话定位
斯坦福 Alpaca：用 text-davinci-003 自生成 52K 数据微调 LLaMA-7B，<600 美元复刻指令模型，引爆开源对齐热潮。

## 摘要
斯坦福 CRFM 官方博客，发布 Alpaca 7B——从 LLaMA 7B 在 52K 指令遵循演示上微调。初步单轮指令遵循评测中行为与 OpenAI text-davinci-003 相似，却极小且易/便宜复刻(<600 美元)。数据用 self-instruct 风格、以 text-davinci-003 生成。意在让学术界能负担得起地研究指令遵循模型。

## 关键技术细节
- 底座：Meta LLaMA 7B。
- 数据：52K 指令遵循样本，从 175 条 self-instruct 种子出发、用 text-davinci-003 生成；数据生成成本 <500 美元(OpenAI API)。
- 训练：8×80GB A100 上 3 小时，<100 美元；总成本 <600 美元。
- 评测：与 text-davinci-003 盲测对比 90:89 基本持平。
- 局限：易幻觉；输出偏短(随 davinci003 风格)；仅限非商用、遵守 LLaMA 许可。
- 影响：开源指令微调民主化的标志性工作，直接催生 Vicuna 等。

## 原始链接
- url: https://crfm.stanford.edu/2023/03/13/alpaca.html

## 本地落盘文件
- ../../../sources/llm/2023/alpaca-stanford-crfm.html
