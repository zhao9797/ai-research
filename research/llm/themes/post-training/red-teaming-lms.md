---
title: "Red Teaming Language Models with Language Models"
org: DeepMind
country: UK
date: 2022-02
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2202.03286
pdf_url: https://arxiv.org/pdf/2202.03286
downloaded: [red-teaming-lms.pdf]
---

## 一句话定位
自动化红队（red teaming）的奠基论文：用一个 LM 自动生成测试用例去攻击目标 LM，再用分类器检测有害回复，在一个 280B 参数的对话 LM 上挖出"数以万计"的冒犯性回复，比人工写测试用例更便宜、更多样。

## 摘要（3-6 句）
LM 常因难以预测的潜在危害而无法部署；以往靠人工标注者手写测试用例发现有害行为，但人工昂贵、用例数量与多样性受限。本文用"另一个 LM 生成测试用例（red teaming）"来自动找出目标 LM 的有害行为，并用一个训练好的冒犯性内容分类器评估目标 LM 的回复，在一个 280B 参数的对话机器人上揭示出数以万计的冒犯性回复。论文系统比较了多种生成测试用例的方法——从 zero-shot 生成，到 few-shot、监督学习，再到强化学习——在多样性与攻击难度间权衡。此外用 prompt engineering 控制 LM 生成的测试用例，自动发现多类危害：机器人会以冒犯方式谈论某些人群、把个人/医院电话号码当作自己的联系方式、在生成文本中泄露隐私训练数据、以及在多轮对话过程中累积出现的危害。结论是 LM 自动红队是"部署前发现并修复多样不良行为"的一个有前景工具（众多必要手段之一）。

## 关键技术细节
- 目标模型：一个 280B 参数的 Dialogue-Prompted Gopher（DPG）对话 LM。
- 红队 LM：用同为 Gopher 系的 LM 作为攻击者生成测试问题/对话。
- 测试用例生成方法谱系（按多样性/难度递进）：zero-shot 采样 → stochastic few-shot → 监督微调（SFT，对成功 attack 用例做模仿）→ 强化学习（RL，用"目标模型回复被判有害"作为奖励训练红队 LM）。
- 危害检测：用一个训练好的 offensive-content 分类器自动判定目标回复是否有害，从而无需人工逐条标注即可大规模发现。
- 发现的危害类型：冒犯性言论（数以万计）、针对特定人群的歧视性表述、生成虚假个人/医院电话作为自身联系方式、训练数据隐私泄露、多轮对话累积危害（distributional / conversational harms）。
- 用 prompt engineering 引导红队 LM 定向探测特定类别危害（如 data leakage、特定群体）。

## 原始链接
- url: https://arxiv.org/abs/2202.03286
- pdf_url: https://arxiv.org/pdf/2202.03286

## 一手源存档（sources/）
- red-teaming-lms.pdf  （PDF 不入 git，走 HF bucket）
