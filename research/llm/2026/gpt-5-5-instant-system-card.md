---
title: GPT-5.5 Instant System Card
org: OpenAI
country: US
date: 2026-05
type: model-card
categories: [后训练, 预训练数据]
url: https://openai.com/index/gpt-5-5-instant-system-card/
pdf_url: https://deploymentsafety.openai.com/gpt-5-5-instant/gpt-5-5-instant.pdf
github_url:
downloaded: [openai-gpt-5-5-instant-system-card.pdf, openai-gpt-5-5-instant-system-card.html]
---

## 一句话定位
OpenAI 2026-05-05 发布的 GPT-5.5 Instant（默认 ChatGPT 模型）系统卡——首个被 OpenAI 在网络安全与生物/化学 Preparedness 类别按"High capability"对待并部署相应防护的 Instant 模型。

## 摘要
GPT-5.5 Instant 是 OpenAI 最新的 Instant 模型，更新了 ChatGPT 默认模型，更智能/更准确、减少幻觉、改进个性化控制。系统卡（21 页 PDF）涵盖 Model Data and Training、Safety（Disallowed Content、Vision、对抗用户模拟的动态心理健康基准）、Robustness（越狱、prompt injection）、Health（HealthBench）、Hallucinations、Inclusivity/Bias 与 Preparedness 能力评估（生物化学、网络安全、AI 自我改进）。这是首个被作为网络安全与生化 Preparedness "High" 处理的 Instant 模型并实施相应 safeguards。对照基线为 GPT-5.3 Instant（无 GPT-5.4 Instant）；GPT-5.5（Thinking）为另一模型。

## 关键技术细节
- 发布：2026-05-05（PDF 内标 May 4, 2026）。Instant 系列；对照基线 GPT-5.3 Instant。
- Preparedness：首个在 Cybersecurity 与 Biological & Chemical 两类按 "High capability" 处理的 Instant 模型，部署对应 safeguards（生物安全、网络安全 safeguards）。
- 训练数据：多样数据集——互联网公开信息、第三方合作数据、用户/人工训练员/研究员提供或生成的数据；严格过滤维持质量、降低风险；用先进过滤减少训练数据中的个人信息；用安全分类器减少有害/敏感内容（含 CSAM）。
- 评测维度：Disallowed Content（含 challenging prompts 生产基准）、Vision、动态心理健康基准（对抗用户模拟）、Jailbreaks、Prompt injection、HealthBench、Hallucinations、Bias。
- Preparedness 能力评测项：生物化学（Multimodal Troubleshooting Virology、ProtocolQA Open-Ended、Tacit Knowledge、TroubleshootingBench）、网络安全（CTF、CVE-Bench、Cyber range）、AI Self-Improvement。
- 命名说明：GPT-5.5（Thinking）≠ GPT-5.5 Instant；二者分别有系统卡。

## 原始链接
- url: https://openai.com/index/gpt-5-5-instant-system-card/
- pdf_url: https://deploymentsafety.openai.com/gpt-5-5-instant/gpt-5-5-instant.pdf

## 一手源存档（sources/）
- openai-gpt-5-5-instant-system-card.pdf  （PDF 不入 git，走 HF bucket）
- [openai-gpt-5-5-instant-system-card.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/openai-gpt-5-5-instant-system-card.html)
