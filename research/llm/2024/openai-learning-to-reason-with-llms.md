---
title: Learning to Reason with LLMs (OpenAI o1)
org: OpenAI
country: US
date: 2024-09
type: blog
categories: [后训练, agentic训练]
url: https://openai.com/index/learning-to-reason-with-llms/
pdf_url:
github_url:
downloaded: [openai-learning-to-reason-with-llms.md]
---

## 一句话定位
OpenAI 官方发布 o1（o1-preview）的研究博客，首次系统阐述用大规模强化学习训练模型"先思考再回答"（生成长内部思维链 CoT）的推理范式，奠定 test-time compute scaling 路线。

## 摘要
2024-09-12 发布。o1 是一种通过强化学习训练、能在回答前产生长内部思维链的新型大模型。其性能随训练时强化学习算力（train-time compute）与思考时算力（test-time compute）增加而平滑提升，这是一条与预训练 scaling 不同的新扩展轴。o1 在竞赛数学（AIME）、竞赛编程（Codeforces）和博士级科学问题（GPQA Diamond）上大幅超越 GPT-4o，部分基准超过人类博士水平。OpenAI 选择对用户隐藏原始 CoT，仅展示模型生成的摘要。

## 关键技术细节
- 训练方法：大规模强化学习（large-scale RL），数据效率极高，教模型用 CoT 进行有效思考；性能随 RL（train-time）与思考时间（test-time）两个维度 log-linear 提升。
- 评测（pass@1，最大 test-time compute）：AIME 2024 数学竞赛准确率较 GPT-4o 大幅提升（GPT-4o 约 13% → o1 显著更高，consensus@64 更优）；Codeforces 编程竞赛达到第 89 百分位（约 Elite 水平）；GPQA Diamond 博士级科学题超过人类博士专家准确率。
- 推理范式：模型在回应前生成可长达数千 token 的隐藏思维链，能识别并纠正自身错误、尝试不同策略、分解复杂步骤。
- 阴影区域为 64 样本多数投票（consensus/majority vote）；实线为 pass@1。
- 隐藏 CoT 决策：出于安全监控与竞争考虑，不在产品中向用户展示原始 CoT，仅显示摘要。
- 发布形态：o1-preview 与 o1-mini 面向 ChatGPT 与可信 API 用户。

## 原始链接
- url: https://openai.com/index/learning-to-reason-with-llms/

## 一手源存档（sources/）
- [openai-learning-to-reason-with-llms.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/openai-learning-to-reason-with-llms.md)
