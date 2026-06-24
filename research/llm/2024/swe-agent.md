---
title: "SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering"
org: Princeton University
country: US
date: 2024-05
type: paper
categories: [agentic训练]
url: https://arxiv.org/abs/2405.15793
pdf_url: https://arxiv.org/pdf/2405.15793
github_url: https://github.com/princeton-nlp/SWE-agent
downloaded: [2405.15793.pdf]
---

## 一句话定位
SWE-agent：提出"agent-computer interface（ACI）"概念——为 LM agent 专门设计的命令接口能大幅提升其软件工程能力，在 SWE-bench 上刷新 SOTA。

## 摘要
LM agent 越来越多用于自动化数字环境中的复杂任务。正如人类靠 IDE 等强工具完成软件工程，作者主张 LM agent 是有自身需求与能力的新型终端用户，应有专门设计的接口。论文研究接口设计如何影响 LM agent 性能，并据此提出 SWE-agent：让 LM agent 自主操作计算机解决软件工程任务的系统。其自定义的 agent-computer interface（ACI）显著增强 agent 创建/编辑文件、浏览整个仓库、执行测试与程序的能力。在 SWE-bench 与 HumanEvalFix 上达 SOTA，pass@1 分别为 12.5% 与 87.7%，远超此前非交互式 LM。还分析了 ACI 设计如何影响 agent 行为与性能。

## 关键技术细节
- 核心概念：ACI（agent-computer interface）—— 为 agent（而非人）定制的 LM-friendly 命令集与反馈格式。
- ACI 设计要点：简洁的文件查看/编辑命令、带行号与编辑后反馈、防止无效操作的护栏、上下文管理。
- 评测：SWE-bench pass@1 12.5%（远超此前非交互 LM）、HumanEvalFix 87.7%。
- 发现：接口质量对 agent 表现的影响可与底层模型相当；好的 ACI 能让同一模型表现大幅提升。
- 开源：代码与 ACI 实现公开。

## 原始链接
- url: https://arxiv.org/abs/2405.15793
- pdf_url: https://arxiv.org/pdf/2405.15793
- github: https://github.com/princeton-nlp/SWE-agent

## 本地落盘文件
- ../../../sources/llm/2024/2405.15793.pdf
