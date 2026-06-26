---
title: "Introducing OpenAI o3 and o4-mini"
org: OpenAI
country: US
date: 2025-04
type: blog
categories: [后训练, agentic训练]
url: https://openai.com/index/introducing-o3-and-o4-mini/
pdf_url:
github_url:
downloaded: [openai-o3-o4-mini.html]
---

## 一句话定位
OpenAI 首批"会自己用全套工具"的推理模型：o3/o4-mini 经训练能在思考中自主调用并组合 ChatGPT 内全部工具(网搜、Python、视觉推理、图像生成)，并学会判断何时/如何用工具——是 ChatGPT 走向自主 agent 的关键一步。

## 摘要
2025-04-16，OpenAI 发布 o3 与 o4-mini。这是首次让推理模型能自主调用并组合 ChatGPT 内的全部工具：网络搜索、用 Python 分析上传文件与数据、对视觉输入做深度推理、甚至生成图像。模型经训练学会判断何时以及如何使用工具，通常在一分钟内给出经思考的详尽回答，从而更有效地处理多维问题，朝着"能代表用户独立执行任务"的更自主 ChatGPT 迈进。o3 是其最强推理模型，在 Codeforces、SWE-bench(无需定制框架)、MMMU 等创 SOTA；o4-mini 小而高效，在 AIME 2024/2025 表现最佳——允许调用 Python 时，o4-mini 在 AIME 2025 取得 99.5% pass@1、100% consensus@8。

## 关键技术细节
- 关键突破：首批能"agentic 地"自主使用 ChatGPT 全部工具(web search、Python 数据分析、图像推理、图像生成)并组合多次调用的推理模型。
- 训练：经强化学习训练"何时/如何调用工具"以恰当输出格式作答；可在搜索-观察-再搜索之间灵活转换策略。
- o3：最强推理模型，Codeforces / SWE-bench(无定制 scaffold) / MMMU SOTA；对高难真实任务比 o1 重大错误率降 20%。
- o4-mini：AIME 2025 允许 Python 时 99.5% pass@1 / 100% consensus@8；o3 同设置 98.4% pass@1 / 100% consensus@8。
- SWE-bench 评测用固定的 n=477 verified 子集(内部基础设施验证)。

## 原始链接
- url: https://openai.com/index/introducing-o3-and-o4-mini/

## 一手源存档（sources/）
- [openai-o3-o4-mini.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/agentic/openai-o3-o4-mini.html)
