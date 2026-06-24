---
title: Improving alignment of dialogue agents via targeted human judgements (Sparrow)
org: DeepMind    country: UK    date: 2022-09    type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2209.14375    pdf_url: https://arxiv.org/pdf/2209.14375    github_url:
downloaded: [sparrow.pdf]
---

## 一句话定位
DeepMind 的对话智能体 Sparrow：用 RLHF + 把"好对话"拆成细粒度规则 + 检索证据支撑事实，训练更有用、正确、无害的助手。

## 摘要
Sparrow 是信息检索型对话智能体，相比提示式基线更有用、正确、无害。用 RLHF 训练，并引入两项新机制帮助人类评分者判断行为：(1) 把"好对话"的要求拆解为一组自然语言规则，让评分者对每条规则分别判断——这使收集的人类判断更有针对性，并支持规则条件化的奖励模型；(2) 智能体在收集偏好时对事实性陈述提供支撑证据来源。对事实性问题，Sparrow 提供的证据 78% 的时间支撑其回答。Sparrow 比基线更受偏好，且对人类对抗探测更鲁棒——被探测时仅 8% 违反规则。

## 关键技术细节
- 基座：Chinchilla 70B。
- RLHF：在 Chinchilla 上做偏好建模 + RL；同时用 per-rule 分类器奖励（规则条件化奖励模型）。
- 规则拆解：把无害/有用拆成约 23 条细粒度自然语言规则，分别采集人类判断，缓解模糊整体评分。
- 检索增强：可调用 Google 搜索，引用证据支撑事实主张（证据 78% 支撑回答）。
- 鲁棒性：对抗探测下仅 8% 违规；比纯提示基线更受偏好。
- 是 DeepMind 在 ChatGPT 之前的对话对齐代表作，强调"证据 + 规则"。

## 原始链接
- url: https://arxiv.org/abs/2209.14375
- pdf_url: https://arxiv.org/pdf/2209.14375

## 本地落盘文件
- ../../../sources/llm/2022/sparrow.pdf
