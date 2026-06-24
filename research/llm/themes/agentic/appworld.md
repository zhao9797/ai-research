---
title: "AppWorld: A Controllable World of Apps and People for Benchmarking Interactive Coding Agents"
org: "Stony Brook University / 等"
country: US
date: 2024-07
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2407.18901
pdf_url: https://arxiv.org/pdf/2407.18901
github_url: https://github.com/StonyBrookNLP/appworld
downloaded: [appworld-2407.18901.pdf]
---

## 一句话定位
"交互式编码 agent"的高保真世界：9 个日常 app、457 个 API、约 100 个虚构用户的模拟数字生活，要求 agent 写带复杂控制流的代码迭代完成 750 个真实任务。

## 摘要
处理日常数字任务(如为家庭订杂货)的自主 agent，不仅要通过 API 操作多个 app(笔记、消息、购物等)，还要基于与环境的交互迭代地生成带复杂控制流的丰富代码。现有工具使用基准不足，仅覆盖简单的 API 调用序列。为弥补，作者构建 AppWorld Engine——一个高质量执行环境(6 万行代码)，含 9 个可通过 457 个 API 操作的日常 app，并填充模拟约 100 个虚构用户数字生活的真实数字活动。在此之上创建 AppWorld Benchmark(4 万行代码)——750 个自然、多样、有挑战性的任务，需要丰富且交互式的代码生成。GPT-4o 等强基线只能解决约 49% 的简单任务、约 30% 的完整任务，凸显该基准的难度。

## 关键技术细节
- 引擎：AppWorld Engine，6 万行代码；9 个日常 app(Amazon、Gmail、Spotify、Venmo、SimpleNote、电话、文件等)，457 个 API。
- 世界状态：约 100 个虚构用户的逼真数字生活(联系人、消息、交易历史等)，支持有状态的多 app 交互。
- 任务：AppWorld Benchmark 750 个任务(4 万行代码)，分难度；要求 agent 写带控制流的代码、按环境反馈迭代。
- 评测：执行级 + 鲁棒性检查(检测意外副作用，如误删/误付)。
- 基线：GPT-4o 完整任务通过率约 30%，凸显交互式编码 agent 的挑战。

## 原始链接
- url: https://arxiv.org/abs/2407.18901
- pdf_url: https://arxiv.org/pdf/2407.18901
- github_url: https://github.com/StonyBrookNLP/appworld

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/appworld-2407.18901.pdf
