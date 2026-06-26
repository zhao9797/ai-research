---
title: "ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs"
org: "清华大学 (THUNLP) / 人民大学 / 耶鲁 / 微信 / 智谱等"
country: China
date: 2023-07
type: paper
categories: [后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2307.16789
pdf_url: https://arxiv.org/pdf/2307.16789
github_url: https://github.com/OpenBMB/ToolBench
downloaded: [toolllm-2307.16789.pdf]
---

## 一句话定位
开源工具学习的里程碑：用 ChatGPT 自动构造覆盖 16000+ 真实 RESTful API 的指令微调数据集 ToolBench，配深度优先搜索决策树(DFSDT)与自动评测器 ToolEval，训练出可比肩 ChatGPT 的 ToolLLaMA。

## 摘要
ToolLLM 是面向工具使用的通用框架，含数据构造、模型训练、评测三部分。① API 收集：从 RapidAPI Hub 收集 16,464 个真实 RESTful API，覆盖 49 个类别；② 指令生成：用 ChatGPT 生成涉及这些 API 的多样指令，含单工具与多工具场景；③ 解法标注：用 ChatGPT 为每条指令搜索有效解法路径(API 调用链)。为增强推理，提出基于深度优先搜索的决策树算法(DFSDT)，让 LLM 评估多条推理轨迹、扩展搜索空间。基于 ToolBench 微调 LLaMA 得到 ToolLLaMA，并配神经 API 检索器；实验显示其能执行复杂指令、泛化到未见 API，性能可比 ChatGPT，并在分布外数据集 APIBench 上表现强零样本泛化。

## 关键技术细节
- 数据集 ToolBench：16,464 个真实 RESTful API，49 个类别，来源 RapidAPI Hub。
- 数据三阶段：API 收集 → 指令生成(单/多工具) → 解法路径标注，全程用 ChatGPT 自动化。
- DFSDT(Depth-First Search-based Decision Tree)：相对传统 ReAct/CoT 的线性推理，允许评估多分支、回溯，显著提升复杂多步工具调用成功率。
- 评测器 ToolEval：自动化评测工具使用(pass rate / win rate)。
- 模型 ToolLLaMA：LLaMA 微调 + 神经 API 检索器(API retriever)推荐合适 API。
- 结果：ToolLLaMA 接近 ChatGPT 的工具使用能力，并对未见 API/分布外集(APIBench)有强泛化。

## 原始链接
- url: https://arxiv.org/abs/2307.16789
- pdf_url: https://arxiv.org/pdf/2307.16789
- github_url: https://github.com/OpenBMB/ToolBench

## 一手源存档（sources/）
- [toolllm-2307.16789.pdf](https://arxiv.org/pdf/2307.16789)  （arXiv 原文 PDF，不入 git）
