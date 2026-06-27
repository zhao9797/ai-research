---
title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
org: "Princeton University / Stanford"
country: US
date: 2024-05
type: paper
categories: [架构, agentic训练]
url: https://arxiv.org/abs/2405.15793
pdf_url: https://arxiv.org/pdf/2405.15793
github_url: https://github.com/SWE-agent/SWE-agent
downloaded: [swe-agent-2405.15793.pdf]
---

## 一句话定位
提出"Agent-Computer Interface(ACI)"概念：为 LM agent 专门设计的命令行式接口(浏览/编辑/测试)显著放大其软件工程能力，证明接口设计本身是 agent 性能的关键变量。

## 摘要
SWE-agent 研究"界面设计如何影响 LM agent 表现"。作者主张 LM agent 是一类新型最终用户，应有专门为其打造的接口。SWE-agent 的自定义 Agent-Computer Interface(ACI) 显著增强 agent 创建/编辑代码文件、浏览整个仓库、运行测试和程序的能力。在 SWE-bench 与 HumanEvalFix 上达到 SOTA：pass@1 分别为 12.5% 与 87.7%，远超此前非交互式 LM。论文还分析了 ACI 设计如何影响 agent 行为与表现(如简洁的反馈、带 lint 的编辑命令、文件查看窗口等)。

## 关键技术细节
- 核心概念 ACI(Agent-Computer Interface)：类比人类用 IDE，给 agent 设计专用命令(查看文件片段、跳转、编辑并带语法 lint 反馈、搜索、运行测试)。
- 关键设计原则：动作要简洁高效、反馈要紧凑信息密集、对错误(如编辑语法错)给即时 lint 反馈防止级联失败。
- 结果：SWE-bench pass@1 = 12.5%(基于 GPT-4)，HumanEvalFix pass@1 = 87.7%，均为当时 SOTA。
- 消融：去掉 ACI 的关键设计(如带 lint 的编辑、文件窗口)显著降低成功率，证明"接口设计"对 agent 性能影响巨大。
- 是开源 coding agent 的奠基工作之一，与 SWE-bench 同组。

## 原始链接
- url: https://arxiv.org/abs/2405.15793
- pdf_url: https://arxiv.org/pdf/2405.15793
- github_url: https://github.com/SWE-agent/SWE-agent

## 一手源存档（sources/）
- [swe-agent-2405.15793.pdf](https://arxiv.org/pdf/2405.15793)  （arXiv 原文 PDF，不入 git）
