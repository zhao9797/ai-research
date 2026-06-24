---
title: Voyager: An Open-Ended Embodied Agent with Large Language Models
org: NVIDIA / Caltech
country: US
date: 2023-05
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2305.16291
pdf_url: https://arxiv.org/pdf/2305.16291
github_url: https://github.com/MineDojo/Voyager
downloaded: [voyager.pdf]
---

## 一句话定位
NVIDIA 的 Voyager：Minecraft 中首个 LLM 终身学习智能体，靠自动课程+技能库代码实现持续自我提升。

## 摘要
Voyager 是 Minecraft 中首个 LLM 驱动的终身学习 embodied agent，无人干预地持续探索、习得技能、做新发现。三组件：(1)最大化探索的自动课程；(2)存取可执行代码的不断增长的技能库；(3)结合环境反馈/执行错误/自验证的迭代提示机制。通过黑盒查询 GPT-4，无需微调参数。技能时序可扩展、可解释、可组合。比此前 SOTA 多得 3.3x 独特物品、走 2.3x 远、解锁科技树快 15.3x；可在新世界复用技能库解新任务。

## 关键技术细节
- 训练方式：无梯度——纯黑盒 GPT-4 查询 + 代码技能库（in-context lifelong learning）。
- 自动课程：GPT-4 依据当前状态提出渐进任务目标。
- 技能库：把成功行为存成可执行 JS 代码，向量检索复用，缓解灾难性遗忘。
- 迭代提示：环境反馈 + 执行报错 + 自验证 → 改进程序。
- 结果：独特物品 3.3x、行程 2.3x、科技树里程碑速度 15.3x（vs ReAct/Reflexion/AutoGPT）。

## 原始链接
- url: https://arxiv.org/abs/2305.16291
- pdf_url: https://arxiv.org/pdf/2305.16291
- github_url: https://github.com/MineDojo/Voyager

## 本地落盘文件
- ../../../sources/llm/2023/voyager.pdf
