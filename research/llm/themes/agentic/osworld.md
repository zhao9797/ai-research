---
title: "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments"
org: "香港大学 / 上海交大 / Salesforce Research 等 (XLANG Lab)"
country: China
date: 2024-04
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2404.07972
pdf_url: https://arxiv.org/pdf/2404.07972
github_url: https://github.com/xlang-ai/OSWorld
downloaded: [osworld-2404.07972.pdf]
---

## 一句话定位
computer-use agent 的标准评测环境：真实操作系统(Ubuntu/Windows/macOS)中 369 个跨应用任务，执行级判定，成为 Claude computer use / OpenAI CUA / UI-TARS 等争锋的核心赛场。

## 摘要
OSWorld 是首个可扩展的真实计算机环境，用于多模态 agent，支持任务设置、基于执行的评测、跨操作系统(Ubuntu/Windows/macOS)的交互式学习。基于 OSWorld，作者构建含 369 个真实计算机任务的基准，涉及真实 web/桌面应用、操作系统文件 I/O、跨多个应用的工作流；每个任务都有详细的初始状态配置与定制的执行级评测脚本，保证可靠可复现。对 SOTA 的 LLM/VLM agent 的评测显示其作为计算机助手存在严重不足：人类可完成 72.36% 的任务，而最好的模型仅 12.24%，主要卡在 GUI grounding 与操作知识。

## 关键技术细节
- 环境：真实 OS 虚拟机(Ubuntu 主、含 Windows/macOS)，支持任意应用；agent 以屏幕截图/a11y 树为观察，键鼠/代码为动作。
- 任务：369 个真实计算机任务，跨 web+桌面 app、文件 I/O、多应用工作流；每任务带初始状态脚本 + 执行级评测脚本。
- 基线(论文时)：人类 72.36% vs 最优模型 12.24%；主要瓶颈是 GUI grounding(精确定位元素)与操作知识。
- 影响：成为 computer-use agent 的事实标准——OpenAI CUA 报 38.1%、Claude computer use 报 14.9%、UI-TARS 报 22.7-24.6% 等均以 OSWorld 为基准。
- 项目页：https://os-world.github.io

## 原始链接
- url: https://arxiv.org/abs/2404.07972
- pdf_url: https://arxiv.org/pdf/2404.07972
- github_url: https://github.com/xlang-ai/OSWorld

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/osworld-2404.07972.pdf
