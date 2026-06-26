---
title: "WebSailor: Navigating Super-human Reasoning for Web Agent"
org: "阿里巴巴 通义实验室 (Alibaba Tongyi Lab / Alibaba-NLP)"
country: China
date: 2025-07
type: paper
categories: [后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2507.02592
pdf_url: https://arxiv.org/pdf/2507.02592
github_url: https://github.com/Alibaba-NLP/DeepResearch
downloaded: [websailor-2507.02592.pdf]
---

## 一句话定位
通义 DeepResearch 的后训练方法论：用"信息混淆"造高不确定性任务 + RFT 冷启动 + 高效 agentic RL 算法 DUPO，让开源 web agent 在 BrowseComp 等极难信息检索任务上逼近 DeepResearch 级闭源系统。

## 摘要
超越人类认知极限是 LLM 训练的关键前沿。专有 agentic 系统(如 DeepResearch)在极复杂信息检索基准 BrowseComp 上展现超人能力，作者认为其成功源于开源模型缺乏的一种推理模式：在浩瀚信息中系统性地降低极端不确定性的能力。据此提出 WebSailor——一套完整的后训练方法，旨在赋予这种关键能力。方法包括：通过结构化采样与信息混淆(information obfuscation)生成新颖的高不确定性任务、RFT 冷启动、以及高效的 agentic RL 算法 DUPO(Duplicating Sampling Policy Optimization)。借助这一整合管线，WebSailor 显著超过所有开源 agent，匹配专有 agent 的表现，弥合能力差距。

## 关键技术细节
- 任务构造：结构化采样 + 信息混淆(刻意制造高不确定性、需要多跳消歧的检索任务)。
- 两阶段后训练：RFT(Rejection sampling Fine-Tuning) 冷启动 → agentic RL。
- RL 算法 DUPO(Duplicating Sampling Policy Optimization)：高效的 agentic 强化学习，针对多轮检索 rollout 做采样复用以提升效率。
- 评测：BrowseComp(英/中)、GAIA 等高难信息检索基准；开源模型逼近专有 DeepResearch。
- 隶属 Alibaba-NLP/DeepResearch 系列，与 WebDancer、WebWalker 同源，构成通义"深度研究"开源栈。

## 原始链接
- url: https://arxiv.org/abs/2507.02592
- pdf_url: https://arxiv.org/pdf/2507.02592
- github_url: https://github.com/Alibaba-NLP/DeepResearch

## 一手源存档（sources/）
- [websailor-2507.02592.pdf](https://arxiv.org/pdf/2507.02592)  （arXiv 原文 PDF，不入 git）
