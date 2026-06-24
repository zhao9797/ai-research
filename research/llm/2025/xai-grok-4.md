---
title: Grok 4
org: xAI
country: US
date: 2025-07
type: blog
categories: [AI infra, 后训练, agentic训练]
url: https://x.ai/news/grok-4
pdf_url:
github_url:
downloaded: [files/xai-grok-4-blog.md]
---

## 一句话定位
xAI 2025-07-09 发布的 Grok 4 官方博客：在 20 万 GPU 的 Colossus 集群上把强化学习扩展到"预训练规模"，原生工具使用，并推出多 agent 的 Grok 4 Heavy。

## 摘要
延续 Grok 3 的下一 token 预训练 + RL 推理，Grok 4 首次把 RL 训练扩到 pretraining 规模：用 Colossus 20 万 GPU 集群运行 RL，靠新基础设施与算法把训练计算效率提升 6x，并把可验证训练数据从数学/编码大幅扩展到更多领域。Grok 4 经 RL 训练原生使用工具（代码解释器、网页/X 浏览），并推出并行多 agent 的 Grok 4 Heavy。在 Humanity's Last Exam 等前沿基准领先。

## 关键技术细节（带数字）
- RL 规模：用 Colossus 20 万（200,000）GPU 集群运行 RL，将 RL 扩到 pretraining 规模。
- 效率：基础设施 + 算法创新使训练计算效率提升 6x；总训练算力较以往高出"一个数量级以上"。
- 数据：大规模可验证（verifiable）训练数据采集，从数学/编码扩展到更多领域。
- 原生工具使用：RL 训练学会调用 code interpreter、web/X 浏览，自主选择搜索查询。
- Grok 4 Heavy：并行运行多个 agent 协作求解的版本。
- 基准：Humanity's Last Exam（2025-04-03 full set，带 Python + 联网工具）领先；含 AIME/GPQA 等。
- 发布日期：2025-07-09；含 Grok 4 API 与语音模式。

## 原始链接
- 官方博客：https://x.ai/news/grok-4

## 本地落盘文件
- ../../../sources/llm/2025/xai-grok-4-blog.md
