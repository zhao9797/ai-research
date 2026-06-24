---
title: Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models (BIG-bench)
org: Google 等 132 机构协作    country: US/International    date: 2022-06    type: paper
categories: [预训练数据]
url: https://arxiv.org/abs/2206.04615    pdf_url: https://arxiv.org/pdf/2206.04615    github_url: https://github.com/google/BIG-bench
downloaded: [big-bench.pdf]
---

## 一句话定位
204 个任务、450 名作者、132 机构协作的超大评测套件 BIG-bench，专测被认为超出当前 LLM 能力的任务。

## 摘要
语言模型随规模既有量变也有新质变能力，但这些新能力尚缺刻画。为给未来研究提供信息、为颠覆性能力做准备、缓解社会危害，理解 LLM 当前与近未来能力极其重要。BIG-bench 由 204 个任务组成，450 名作者来自 132 个机构贡献，任务主题多样（语言学、儿童发展、数学、常识、生物、物理、社会偏见、软件开发等），聚焦被认为超出当前模型能力的任务。

## 关键技术细节
- 规模：204 个任务（含 BIG-bench Lite 子集），450 作者，132 机构，社区协作开源。
- 评测对象：OpenAI GPT 系列、Google 稠密 Transformer、Switch 稀疏模型，横跨多个数量级规模。
- 发现：性能随规模平滑提升 + 部分任务"突变式"（涌现）提升；模型在多数任务上仍远逊人类专家；社会偏见随规模/上下文变化。
- 校准随规模改善；few-shot vs zero-shot 系统比较。
- 衍生 BBH（BIG-Bench Hard, 2210.09261），是 LLM 评测基础设施基石。

## 原始链接
- url: https://arxiv.org/abs/2206.04615
- pdf_url: https://arxiv.org/pdf/2206.04615
- github_url: https://github.com/google/BIG-bench

## 本地落盘文件
- ../../../sources/llm/2022/big-bench.pdf
