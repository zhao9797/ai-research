---
title: "Voyager: An Open-Ended Embodied Agent with Large Language Models"
org: "NVIDIA / Caltech / Stanford / UT Austin / UW-Madison"
country: US
date: 2023-05
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2305.16291
pdf_url: https://arxiv.org/pdf/2305.16291
github_url: https://github.com/MineDojo/Voyager
downloaded: [voyager-2305.16291.pdf]
---

## 一句话定位
Minecraft 中首个 LLM 驱动的终身学习具身 agent：用自动课程 + 可执行代码技能库 + 迭代提示自我纠错，持续探索并积累可复用技能，无需任何梯度更新。

## 摘要
Voyager 是基于 GPT-4 的开放世界具身 agent，在 Minecraft 中持续探索、获取技能并自主发现新事物。它有三大组件：① 最大化探索的自动课程(automatic curriculum)；② 用于存储/检索复杂行为的可执行代码技能库(skill library)；③ 含环境反馈、执行错误与自我验证的迭代提示机制。Voyager 通过代码(JavaScript/Mineflayer API)与环境交互，避免梯度更新。结果：获得独特物品数量比前人多 3.3 倍，行程远 2.3 倍，解锁关键科技树里程碑速度快 15.3 倍，并能把学到的技能库零样本迁移到新世界解决新任务。

## 关键技术细节
- 基座：GPT-4(用于推理/写代码)，环境为 MineDojo/Mineflayer。
- 动作以可执行 JavaScript 程序(调用 Mineflayer API)表达——是"代码即动作(code-as-action)"的早期实践。
- 自动课程：依据当前状态/已有技能，由 GPT-4 提议下一目标，渐进难度、开放式。
- 技能库：把验证过的程序按功能存储并可检索复用、组合，形成可累积的"终身学习"能力。
- 迭代提示自我纠错：综合执行报错、环境反馈、自我验证结果不断改写代码。
- 量化：相对此前 SOTA，独特物品 ×3.3，探索距离 ×2.3，科技树里程碑解锁 ×15.3 速度。

## 原始链接
- url: https://arxiv.org/abs/2305.16291
- pdf_url: https://arxiv.org/pdf/2305.16291
- github_url: https://github.com/MineDojo/Voyager

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/voyager-2305.16291.pdf
