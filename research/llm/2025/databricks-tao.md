---
title: TAO - Using test-time compute to train efficient LLMs without labeled data
org: Databricks (Mosaic AI Research)
country: US
date: 2025-03
type: blog
categories: [后训练]
url: https://www.databricks.com/blog/tao-using-test-time-compute-train-efficient-llms-without-labeled-data
pdf_url:
github_url:
downloaded: [files/databricks-tao-blog.md]
---

## 一句话定位
Databricks 2025-03-25 的 AI Research 博客：提出 TAO（Test-time Adaptive Optimization）——用 test-time compute + 强化学习在"无标注输出"的情况下微调 LLM，仅靠企业已有的输入样本即可提升质量并降本。

## 摘要
TAO 针对企业缺乏标注数据、难以做标准微调的痛点：核心是用 test-time compute 让模型对每个任务探索多个候选响应，再用评分（含 Databricks 自研 reward model DBRM + 可选自定义规则/verifier）筛选，最后用强化学习训练模型，使其后续以低推理成本直接执行任务。仅需数千输入样本即可运行。多任务 TAO 在无标签下把 Llama 3.3 70B 提升 2.4%，在 FinanceBench / DB Enterprise Arena / BIRD-SQL 上对 Llama 3.1 8B 与 3.3 70B 取得显著增益，优于带标注的微调。

## 关键技术细节（带数字）
- 方法：TAO = Test-time Adaptive Optimization——test-time compute 探索候选响应 + 评分筛选 + RL 训练。
- 评分：Databricks 自研 reward model DBRM（可叠加自定义规则/verifier）。
- 数据需求：仅需"数千"输入样本（无需标注输出），可来自部署应用或合成。
- 多任务效果：无标签将 Llama 3.3 70B 整体提升 2.4%。
- 评测：FinanceBench、DB Enterprise Arena、BIRD-SQL（Databricks SQL 方言），覆盖 Llama 3.1 8B 与 3.3 70B，超过有标注微调。
- 关键点：虽用 test-time compute，但用于"训练"模型，推理时低成本直接执行（可用更小模型降本）。
- 发布日期：2025-03-25。

## 原始链接
- 官方博客：https://www.databricks.com/blog/tao-using-test-time-compute-train-efficient-llms-without-labeled-data

## 一手源存档（sources/）
- [databricks-tao-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/databricks-tao-blog.md)
