---
title: Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku
org: Anthropic
country: US
date: 2024-10
type: blog
categories: [后训练, agentic训练]
url: https://www.anthropic.com/news/3-5-models-and-computer-use
pdf_url:
github_url:
downloaded: [anthropic-3-5-models-and-computer-use.md]
---

## 一句话定位
Anthropic 发布升级版 Claude 3.5 Sonnet、新模型 Claude 3.5 Haiku，并首推 "computer use"（让模型像人一样看屏幕、移动光标、点击、输入）公开 beta —— 首个提供 computer use 的前沿模型。

## 摘要
2024-10-22 发布。升级版 Claude 3.5 Sonnet 全面提升，尤其编码：SWE-bench Verified 从 33.4% 提升到 49.0%（超过 o1-preview 等所有公开模型），TAU-bench retail 62.6%→69.2%、airline 36.0%→46.0%。Claude 3.5 Haiku 在多项评测上达到此前最大模型 Claude 3 Opus 水平。computer use 作为公开 beta 上线 API：模型通过看截图、移动光标、点击、键入来操作计算机；Asana、Canva、Cognition、DoorDash、Replit、The Browser Company 等已开始探索数十至数百步的任务。

## 关键技术细节
- agentic 编码：SWE-bench Verified 33.4%→49.0%（领先 o1-preview 与专用 agentic 系统）。
- agentic 工具使用：TAU-bench retail 62.6%→69.2%；airline 36.0%→46.0%。
- computer use（公开 beta）：通过屏幕截图感知 + 光标/点击/键入动作操作 GUI；首个提供该能力的前沿模型，仍处实验阶段。
- Claude 3.5 Haiku：多项评测达 Claude 3 Opus 水平，价格 $0.80/M 输入、$4/M 输出（12/03 修订后）。
- 可用性：升级 Sonnet 全量上线；computer use beta 在 Anthropic API、Amazon Bedrock、Google Vertex AI 可用。

## 原始链接
- url: https://www.anthropic.com/news/3-5-models-and-computer-use

## 本地落盘文件
- ../../../sources/llm/2024/anthropic-3-5-models-and-computer-use.md
