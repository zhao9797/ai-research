---
title: "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models"
org: "浙江大学 / 腾讯 AI Lab / 西湖大学 等"
country: China
date: 2024-01
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2401.13919
pdf_url: https://arxiv.org/pdf/2401.13919
github_url: https://github.com/MinorJerry/WebVoyager
downloaded: [webvoyager-2401.13919.pdf]
---

## 一句话定位
首批端到端多模态网页 agent 之一：用大多模态模型(GPT-4V)看带标注框的截图直接操作真实网站，并提出可由 GPT-4V 自动评测的在线真实网站任务集，被 OpenAI CUA 等引为基准。

## 摘要
WebVoyager 是基于大多模态模型(LMM)构建的端到端网页 agent，能在真实世界网站上端到端完成用户指令。此前 web agent 多只处理单一输入模态、或在简化模拟环境/受限网页上评测。WebVoyager 用视觉(带 Set-of-Mark 标注的网页截图)+ 文本观察来与真实网站交互。作者还提出一个新的评测协议：用 GPT-4V 对开放式网页任务的完成情况做自动评测(与人类评测高度一致)。在覆盖 15 个真实网站的任务集上，WebVoyager(GPT-4V) 取得 59.1% 的任务成功率，显著超过纯文本或仅 GPT-4V 基线。

## 关键技术细节
- 基座：GPT-4V(多模态)。
- 观察：网页截图 + Set-of-Mark(给可交互元素加编号标注框)，便于模型指向具体元素。
- 动作：点击、输入、滚动、跳转等真实浏览器操作。
- 任务集：15 个真实常用网站(Amazon、Apple、ArXiv、GitHub、Google Map/Search、Booking 等)的开放式任务。
- 自动评测：用 GPT-4V 作 judge 判定任务是否完成，与人工评测一致性高。
- 结果：成功率 59.1%(GPT-4V)，确立"多模态截图驱动的端到端 web agent"路线；被后续 OpenAI CUA(WebVoyager 87%) 等引用对比。

## 原始链接
- url: https://arxiv.org/abs/2401.13919
- pdf_url: https://arxiv.org/pdf/2401.13919
- github_url: https://github.com/MinorJerry/WebVoyager

## 一手源存档（sources/）
- [webvoyager-2401.13919.pdf](https://arxiv.org/pdf/2401.13919)  （arXiv 原文 PDF，不入 git）
