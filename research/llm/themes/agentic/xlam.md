---
title: "xLAM: A Family of Large Action Models to Empower AI Agent Systems"
org: "Salesforce AI Research"
country: US
date: 2024-09
type: report
categories: [架构, 后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2409.03215
pdf_url: https://arxiv.org/pdf/2409.03215
github_url: https://github.com/SalesforceAIResearch/xLAM
downloaded: [xlam-2409.03215.pdf]
---

## 一句话定位
Salesforce 的"大动作模型(LAM)"系列：从 1B 到 8x22B 专为 agent 任务(函数调用/工具使用)训练，配统一的数据处理与增强管线，多个登顶 Berkeley Function-Calling Leaderboard。

## 摘要
自主 agent 处理复杂任务需要 LLM 具备强大的规划与工具使用能力。xLAM 是一系列专为 AI agent 任务设计的大动作模型(Large Action Models)。其核心是可扩展、灵活的数据处理流水线，用于统一、增强并合成多样的 agent 数据集，提升数据质量与一致性。基于此训练并发布 xLAM 系列：从面向移动端的 1B 稠密模型到 8x22B 的 MoE 模型，覆盖多种规模与架构。实证显示 xLAM 在多个 agent 能力基准上表现优异——在 Berkeley Function-Calling Leaderboard(BFCL) 上多个 xLAM 模型登顶/名列前茅，超过 GPT-4、Claude-3 等。

## 关键技术细节
- 模型规模：xLAM 1B/7B/8x7B/8x22B(含稠密与 MoE)；基座主要为 Mistral / Mixtral / DeepSeek 等。
- 数据管线：统一格式化(unify) + 增强(augment) + 合成(synthesize) 多源 agent/函数调用数据，强调质量一致性与多样性。
- 训练任务：函数调用、工具使用、多轮 agent 交互。
- 结果：BFCL 上 xLAM-8x22B 等登顶；小模型(1B)亦适合端侧 agent。
- 出自 Salesforce AI Research，是工业界系统化"agent 专用基座 + 数据工程"的代表。

## 原始链接
- url: https://arxiv.org/abs/2409.03215
- pdf_url: https://arxiv.org/pdf/2409.03215
- github_url: https://github.com/SalesforceAIResearch/xLAM

## 一手源存档（sources/）
- [xlam-2409.03215.pdf](https://arxiv.org/pdf/2409.03215)  （arXiv 原文 PDF，不入 git）
