---
title: "WebThinker: Empowering Large Reasoning Models with Deep Research Capability"
org: "中国人民大学 / 北京智源研究院(BAAI) / 华为 Poisson Lab"
country: CN
date: 2025-04
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2504.21776
pdf_url: https://arxiv.org/pdf/2504.21776
github_url: https://github.com/RUC-NLPIR/WebThinker
downloaded: [webthinker-2504.21776.pdf]
---

## 一句话定位
让大推理模型（LRM）在推理中自主"搜网页 + 点链接深探 + 边想边写报告"的 deep research agent，用迭代在线 DPO 端到端优化工具使用（NeurIPS 2025）。

## 摘要
WebThinker 针对 LRM（如 o1、DeepSeek-R1）依赖静态内部知识、难以做深度网络信息检索与撰写综合报告的问题，提出让 LRM 在推理过程中自主搜索网页、在页面间导航、并实时起草报告。核心是 Deep Web Explorer 模块（搜索 + 点击链接/按钮导航 + 抽取信息，可基于结果发起后续搜索并深入更深链接）与 Autonomous Think-Search-and-Draft 策略（推理、搜集、写报告实时交错，而非搜完一次性成文）。为进一步释放 LRM 主干潜力，提出基于迭代在线 DPO 的 RL 训练策略。

## 关键技术细节
- 主干：QwQ-32B（开源 o1 类 LRM）；最终模型记为 WebThinker-32B。会议：NeurIPS 2025。
- RL 训练：迭代在线 DPO（iterative online Direct Preference Optimization）。用装好研究工具的 LRM 从复杂任务采样大规模推理轨迹，依据推理/工具使用/最终输出的准确性构造 preference pairs，做迭代 on-policy DPO 训练（非 GRPO/PPO）。
- 报告写作工具三件套：(1) 起草特定章节内容；(2) 检查当前报告；(3) 编辑报告——使模型在推理中动态维护报告的全面性、连贯性与对新发现信息的适应性。
- 复杂推理基准结果（Overall）：WebThinker-32B 在 GPQA 70.7、GAIA 48.5、WebWalkerQA 46.5、HLE 15.8，全面超过 QwQ-32B / RAG-QwQ-32B / Search-o1-32B。
- 科学报告生成（Glaive，1–10 分）：在 Comprehensiveness/Thoroughness/Factuality/Coherence 上均优于 RAG-Qwen2.5-72B、Grok3 DeeperSearch、Gemini2.0 Deep Research。

## 原始链接
- url: https://arxiv.org/abs/2504.21776
- pdf_url: https://arxiv.org/pdf/2504.21776
- github_url: https://github.com/RUC-NLPIR/WebThinker

## 一手源存档（sources/）
- [webthinker-2504.21776.pdf](https://arxiv.org/pdf/2504.21776)  （arXiv 原文 PDF，不入 git）
