---
title: Introducing GPT-5.5
org: OpenAI
country: US
date: 2026-04
type: blog
categories: [后训练, agentic训练]
url: https://openai.com/index/introducing-gpt-5-5/
pdf_url:
github_url:
downloaded: [openai-gpt-5-5.html]
---

## 一句话定位
OpenAI 2026-04-23 发布的旗舰模型 GPT-5.5（及 GPT-5.5 Pro / GPT-5.5 Thinking），主打"智能体化办公"——长周期自主规划、调用工具、自我核查，覆盖编程/知识工作/科研。

## 摘要
GPT-5.5 是 OpenAI 截至发布时最智能的模型，强调智能体编程（agentic coding）、计算机使用（computer use）与科研工作流。官方称其在真实应用中单 token 延迟与 GPT-5.4 持平但智能大幅领先，且完成相同 Codex 任务消耗 token 更少、成本更低（在 Artificial Analysis Coding Agent Index 上以竞品一半成本达到领先智能）。同步发布迄今最完善的安全方案，通过了 Preparedness Framework 全套评估并做了网络安全/生物领域红队。模型先向 ChatGPT/Codex 的 Plus/Pro/Business/Enterprise 用户开放，API 稍后上线。这是一篇产品/能力博客，未披露参数量/架构等预训练细节。

## 关键技术细节
- 发布日期：2026年4月23日（官方页面标注）。家族：GPT-5.5、GPT-5.5 Pro、GPT-5.5 Thinking。
- 定位为"agentic AI infrastructure"，强调自主规划→调用工具→核查结果→在模糊边界中找最优路径的长周期闭环。
- 效率：真实环境单 token 延迟与 GPT-5.4 持平；相同 Codex 任务 token 消耗显著下降。
- 智能体编程基准（vs GPT-5.4 / Claude Opus 4.7 / Gemini 3.1 Pro）：
  - Terminal-Bench 2.0：82.7%（GPT-5.4 75.1%，Opus 4.7 69.4%，Gemini 3.1 Pro 68.5%）
  - SWE-Bench Pro：58.6%
  - Expert-SWE（内部，人类中位完成约20小时的长周期编程）：超过 GPT-5.4（73.1%）
  - OSWorld-Verified：78.7%（GPT-5.4 75.0%，Opus 4.7 78.0%）
  - GDPval（44种职业经济价值知识工作，胜出或平局）：84.9%（GPT-5.5 Pro 82.3%）
  - Toolathlon 55.6%；BrowseComp 84.4%（GPT-5.5 Pro 90.1%）
  - FrontierMath Tier 1–3：51.7%（Pro 52.4%）；Tier 4：35.4%（Pro 39.6%）
  - CyberGym 81.8%
- 知识工作：Tau2-bench Telecom 98.0%（无提示词微调，用 GPT-4.1 作 user model）；FinanceAgent 60.0%；内部投行建模 88.5%；OfficeQA Pro 54.1%。
- 科研：GeneBench（遗传/定量生物多阶段数据分析新评估）较 GPT-5.4 跨越式提升；BixBench 名列前茅；内部定制框架版本发现并以 Lean 形式化验证了关于非对角 Ramsey 数的新渐近证明。
- 安全/对齐：发布前通过 Preparedness Framework 全套安全评估 + 内外红队（高级网络安全、生物技术），并收集近200家合作伙伴真实场景反馈。
- 部署：在 NVIDIA GB200 NVL72 系统上构建与部署（NVIDIA 高管引述）。

## 原始链接
- url: https://openai.com/index/introducing-gpt-5-5/

## 一手源存档（sources/）
- [openai-gpt-5-5.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/openai-gpt-5-5.html)
