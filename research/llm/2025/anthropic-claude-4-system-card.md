---
title: System Card - Claude Opus 4 & Claude Sonnet 4
org: Anthropic
country: US
date: 2025-05
type: system-card
categories: [后训练, agentic训练]
url: https://www.anthropic.com/system-cards
pdf_url: https://www-cdn.anthropic.com/6be99a52cb68eb70eb9572b4cafad13df32ed995.pdf
github_url:
downloaded: [files/anthropic-claude-4-system-card.pdf]
---

## 一句话定位
Anthropic 2025-05 发布的 Claude Opus 4 & Sonnet 4 官方 system card（123 页），首次纳入详尽的对齐评估（misalignment risks）与模型福祉（model welfare）评估，并据 Responsible Scaling Policy 给出 ASL 部署等级。

## 摘要
该 system card 描述两款 hybrid reasoning 模型的部署前安全测试：Usage Policy 违规行为测试、reward hacking 等具体风险评估、computer use 与编码的 agentic 安全评估；首次包含详细的对齐评估与模型福祉评估。基于测试结果，Opus 4 以 ASL-3 标准部署、Sonnet 4 以 ASL-2 标准部署。

## 关键技术细节（带数字）
- 模型：Claude Opus 4 与 Claude Sonnet 4（hybrid reasoning LLM）。
- 部署等级：Opus 4 → AI Safety Level 3 (ASL-3)；Sonnet 4 → ASL-2（依 Responsible Scaling Policy）。
- 评估范围：pre-deployment safety、Usage Policy 违规行为、reward hacking、agentic safety（computer use + coding）。
- 首次纳入：详细 alignment assessment（涵盖多类 misalignment 风险）+ model welfare assessment。
- 文档 123 页；不披露参数/层数等架构数字（Anthropic 闭源策略）。

## 原始链接
- 官方 PDF：https://www-cdn.anthropic.com/6be99a52cb68eb70eb9572b4cafad13df32ed995.pdf
- system cards 列表：https://www.anthropic.com/system-cards

## 一手源存档（sources/）
- anthropic-claude-4-system-card.pdf  （PDF 不入 git，走 HF bucket）
