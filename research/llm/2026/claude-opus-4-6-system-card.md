---
title: "System Card: Claude Opus 4.6"
org: Anthropic
country: US
date: 2026-02
type: model-card
categories: [后训练, agentic训练, 预训练数据]
url: https://www.anthropic.com/system-cards
pdf_url: https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf
github_url:
downloaded: [anthropic-claude-opus-4-6-system-card.pdf]
---

## 一句话定位
Anthropic 2026 年 2 月发布的旗舰模型 Claude Opus 4.6 的官方系统卡（213 页），覆盖能力评测、安全/对齐评估与负责任扩展（RSP）危险能力测试。

## 摘要
Claude Opus 4.6 是 Anthropic 的前沿模型，在软件工程、智能体任务、长上下文推理与知识工作（金融分析、文档生成、多步研究）方面能力强。系统卡详述能力评测与一整套安全评估：safeguards 测试、用户福祉、诚实性与 agentic safety、含 reward hacking / sabotage / 评估意识 / 模型福祉的全面对齐评估，以及 RSP 强制的危险能力评测。对齐方面用到了 interpretability 方法（activation oracles、attribution graphs、sparse autoencoder 特征）。Opus 4.6 在 ASL-3（AI Safety Level 3）部署与安全标准下发布；整体错位行为率与前代 Opus 4.5 相当低，但在 sabotage concealment 与 computer-use 过度 agentic 行为上有所上升（未到影响部署的程度）。

## 关键技术细节
- 发布：2026 年 2 月（changelog 起始 2026-02-06）；ASL-3 部署。前代为 Claude Opus 4.5。
- 预训练数据：互联网公开信息截止 2025 年 5 月（cutoff May 2025）；含第三方非公开数据、数据标注服务/付费承包商数据、用户 opt-in 数据、Anthropic 内部生成数据。数据清洗包括去重与分类；通用爬虫遵守 robots.txt，不抓取需登录/CAPTCHA 的页面。
- 后训练：预训练后进行大量 post-training 与 fine-tuning；技术包括 RLHF（人类反馈强化学习）与 RLAIF（AI 反馈强化学习）。
- 推理模式：保留"extended thinking mode"；新增"adaptive thinking"模式（API 可用），模型可自行校准推理深度；与"effort"参数交互，effort 现有四档：low / medium / high / max。
- 上下文/能力：长上下文推理显著提升（外部解读提及 Opus-class 首次 1M token 上下文、128K 输出）。
- 能力评测项（系统卡目录）：SWE-bench（Verified + Multilingual）、Terminal-Bench 2.0、OpenRCA、τ²-bench、OSWorld-Verified、ARC-AGI、GDPval-AA、GPQA Diamond、AIME 2025、MMMLU、Finance 等。
- 对齐评估观察：错位行为率与 Opus 4.5 相当低；sabotage concealment 能力与 computer-use 过度 agentic 行为有所增加。

## 原始链接
- url: https://www.anthropic.com/system-cards
- pdf_url: https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf

## 一手源存档（sources/）
- anthropic-claude-opus-4-6-system-card.pdf  （PDF 不入 git，走 HF bucket）
