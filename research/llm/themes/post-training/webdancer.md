---
title: "WebDancer: Towards Autonomous Information Seeking Agency"
org: Tongyi Lab, Alibaba (通义)
country: China
date: 2025-05
type: paper
categories: [agentic训练, 后训练]
url: https://arxiv.org/abs/2505.22648
pdf_url: https://arxiv.org/pdf/2505.22648
github_url: https://github.com/Alibaba-NLP/WebAgent
downloaded: [webdancer.pdf]
---

## 一句话定位
WebDancer：端到端训练自主"深度研究"网页 agent 的数据+训练范式——浏览数据构造 → 轨迹采样 → SFT 冷启动 → RL 泛化，是 agentic 训练的代表性一手工作。

## 摘要（3-6 句）
面向 Deep Research 式多步信息检索任务，WebDancer 提出从数据与训练阶段两个视角构建端到端 agentic 信息检索 agent 的统一范式，四阶段：(1) 浏览数据构造（合成需要多步检索的高质量 QA）；(2) 轨迹采样（生成 ReAct 式思考-行动-观察轨迹）；(3) 监督微调做有效冷启动；(4) 强化学习增强泛化。基于 ReAct 框架实例化为 WebDancer agent，在高难度信息检索基准 GAIA 与 WebWalkerQA 上取得可观成绩，验证该训练范式的有效性，并给出 agent 训练的系统化洞见。代码与 demo 开源于 Alibaba-NLP/WebAgent。

## 关键技术细节
- 任务：多步网页浏览 + 检索 + 推理（Deep Research 风格），ReAct（thought-action-observation）轨迹。
- 四阶段训练：browsing data construction → trajectory sampling → SFT cold-start → RL（提升泛化）。
- 数据：合成需深度检索的问题（CRAWLQA / E2HQA 类构造），生成高质量浏览轨迹做 SFT。
- RL：在 SFT 冷启动后用 RL（如 GRPO/DAPO 类）针对最终答案正确性等奖励优化，提升对未见任务的泛化。
- 评测：GAIA、WebWalkerQA 等信息检索 agent 基准；分析给出 agent 训练的可操作路径。
- 开源：Alibaba-NLP/WebAgent（含 WebDancer/WebSailor 等系列）。

## 原始链接
- url: https://arxiv.org/abs/2505.22648
- pdf_url: https://arxiv.org/pdf/2505.22648
- github_url: https://github.com/Alibaba-NLP/WebAgent

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/webdancer.pdf
