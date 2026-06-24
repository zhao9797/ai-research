---
title: "WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents"
org: "Princeton University"
country: US
date: 2022-07
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2207.01206
pdf_url: https://arxiv.org/pdf/2207.01206
github_url: https://github.com/princeton-nlp/WebShop
downloaded: [webshop-2207.01206.pdf]
---

## 一句话定位
早期可扩展的网购 agent 环境(118 万真实商品 + 1.2 万众包指令)：把"看网页、搜索、改写查询、下单"作为语言落地任务，是 ReAct 等的标准实验床，承上启下到 WebArena。

## 摘要
现有"在交互环境中落地语言"的基准要么缺乏真实语言要素，要么因数据/反馈收集需大量人力而难以扩展。WebShop 构建了一个模拟电商网站环境，含 118 万真实商品与 12,087 条众包文本指令。给定指定商品需求的文本指令，agent 需浏览多种网页、发出多样动作来查找、定制并购买商品。WebShop 带来语言落地的若干挑战：理解组合式指令、查询(重)构造、理解并据噪声网页文本行动、执行策略性探索。作者训练并评测多种 agent(模仿学习、RL)，并展示其能零样本迁移到真实电商网站(amazon.com、ebay.com)。

## 关键技术细节
- 规模：1.18M 真实商品(爬自 Amazon)、12,087 条众包指令。
- 动作空间：search[query]、choose[option]、click[button] 等网页操作 + 商品定制/下单。
- 训练方法：模仿学习(IL) + 强化学习(RL)；奖励=购得商品与指令需求的匹配度。
- 挑战：组合式指令理解、查询重构、噪声文本鲁棒性、策略探索。
- 迁移：训练后的 agent 可零样本迁移到 amazon.com/ebay.com。
- 是 ReAct、AgentBench 等的标准评测环境之一，web agent 研究的早期基石。

## 原始链接
- url: https://arxiv.org/abs/2207.01206
- pdf_url: https://arxiv.org/pdf/2207.01206
- github_url: https://github.com/princeton-nlp/WebShop

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/webshop-2207.01206.pdf
