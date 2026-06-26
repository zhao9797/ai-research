---
title: Learning to Reason with LLMs (OpenAI o1)
org: OpenAI
country: US
date: 2024-09
type: blog
categories: [后训练]
url: https://openai.com/index/learning-to-reason-with-llms/
downloaded: [openai-learning-to-reason-o1.html]
---

## 一句话定位
OpenAI o1 官方发布博客：首个大规模"用强化学习训练长思维链（chain-of-thought）推理"的前沿模型，确立 test-time compute / inference-time scaling 新范式。

## 摘要（3-6 句）
o1 是用强化学习训练的新型大模型，在回答前会先产生很长的内部思维链。官方展示 o1 的两条 scaling 曲线：性能随训练期 RL 计算量增加而提升，也随推理期"思考时间"（test-time compute）增加而提升——这是区别于纯预训练 scaling 的新轴。o1 在 AIME、竞赛编程（Codeforces）、博士级科学问题（GPQA Diamond）上大幅超越 GPT-4o，部分达到人类专家水平。RL 让模型学会识别并纠正错误、拆解难题、切换策略。官方为防止"对齐其思维链"破坏其可监控性，选择不向用户展示原始 CoT。

## 关键技术细节
- 训练范式：大规模 RL 优化长 CoT，"reasoning tokens"在输出前生成；RL 让模型学会自我纠错、分解问题、尝试不同方法。
- 两条 scaling 律：train-time RL compute ↑ 与 test-time（思考 token）↑ 都使准确率近似 log-linear 提升。
- 评测（o1 vs GPT-4o）：AIME 2024 从 13% 提升到 74%（单样本）/ 83%（共识采样）/ 93%（重排 1000 样本）；Codeforces Elo 约 1807（89 百分位）；GPQA Diamond 78%，超过博士专家。
- 安全：CoT 提供可解释/可监控窗口；官方刻意不对 CoT 做对齐训练以保其忠实，仅展示摘要而非原始 CoT。
- 未公开具体算法/规模（博客未给参数/数据细节），属官方一手定性发布。

## 原始链接
- url: https://openai.com/index/learning-to-reason-with-llms/

## 一手源存档（sources/）
- [openai-learning-to-reason-o1.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/post-training/openai-learning-to-reason-o1.html)
