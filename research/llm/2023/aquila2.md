---
title: "Aquila2 series（BAAI 悟道·天鹰，官方 GitHub）"
org: 北京智源人工智能研究院（BAAI / FlagOpen）
country: China
date: 2023-10
type: github
categories: [预训练数据, 架构, AI infra]
url: https://github.com/FlagAI-Open/Aquila2
pdf_url:
github_url: https://github.com/FlagAI-Open/Aquila2
downloaded: [aquila2-readme.md]
---

## 一句话定位
智源 BAAI 悟道·天鹰 Aquila2（7B/34B/70B-Expr）：开源中英双语基座 + AquilaChat2 对话/长文本模型，强调"训练数据严格不含测试集"的数据洁净度，是智源 2023 大模型一手资料（FlagOpen 体系）。

## 摘要（3-6 句）
Aquila2 系列开源，包含基座（Aquila2-7B / 34B / 70B-Expr）与对话模型 AquilaChat2（含 7B/34B 及 16K 长文本版）。2023/10/25 发布的 Aquila2-34B v1.2 在客观评测提升 6.9%，在 MMLU、TruthfulQA、CSL、TNEWS、OCNLI、BUSTM 等分别提升 12%/14%/11%/12%/28%/18%；Chat 模型在 8 个子能力维度上达到或超过 GPT-3.5 水平。团队严格遵循"训练数据不含测试数据"，对全部 2T token 训练数据排查了 20+ 个测试集污染。

## 关键技术细节
- 规模：Aquila2-7B / Aquila2-34B / Aquila2-70B-Expr；对话版 AquilaChat2-7B/34B 及 16K 长文本版。
- 数据洁净度：对全部 2 万亿 token 训练数据，针对 WTM22、CLUEWSC、HellaSwag、OpenBookQA、PIQA、MMLU、C-Eval、CMMLU、CSL、HumanEval 等 20+ 测试集做污染排查，确保训练不含测试集。
- 长上下文：AquilaChat2-7B/34B-16K（PI + SFT 扩展到 16K），LongBench 风格评测接近 GPT-3.5-16K。
- 评测方法：参考 Stanford HELM，强调上下文理解与指令遵循，不符指令格式记 0 分。
- 训练框架：FlagScale（基于 Megatron-LM）+ FlagAttention + BMTrain 等 FlagOpen 开源工具链。
- 版本迭代：Aquila2-34B v1.2（2023/10/25）相对 v1 客观评测 +6.9%。

## 原始链接
- url: https://github.com/FlagAI-Open/Aquila2
- github_url: https://github.com/FlagAI-Open/Aquila2

## 本地落盘文件
- ../../../sources/llm/2023/aquila2-readme.md
