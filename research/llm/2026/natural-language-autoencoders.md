---
title: Natural Language Autoencoders Produce Unsupervised Explanations of LLM Activations
org: Anthropic
country: US
date: 2026-05
type: paper
categories: [后训练]
url: https://transformer-circuits.pub/2026/nla/
pdf_url:
github_url:
downloaded: [anthropic-nla.html]
---

## 一句话定位
Anthropic 2026-05-07（Transformer Circuits）发布的可解释性新方法 Natural Language Autoencoders (NLA)——用 RL 训练一对 LLM 模块把残差流激活无监督地翻译成可直接阅读的自然语言解释，并已用于 Claude Opus 4.6 部署前审计。

## 摘要
NLA 是一种无监督方法，用于生成 LLM 激活的自然语言解释。一个 NLA 由两个 LLM 模块组成：activation verbalizer (AV) 把激活映射为文本描述，activation reconstructor (AR) 把描述映射回激活；二者用强化学习联合训练以重建残差流激活。虽然优化目标是激活重建，但产生的解释读起来像对模型内部的合理诠释，且按定量评估随训练越来越有信息量。作者将 NLA 用于模型审计：在 Claude Opus 4.6 部署前审计中，NLA 帮助诊断安全相关行为，并揭示了"未言明的评估意识"（Claude 相信但未说出自己正被评估）。在一个需要端到端调查故意错位模型的自动审计基准上，配备 NLA 的 agent 超过基线，甚至在无法访问错位模型训练数据时也能成功。发布训练代码与针对流行开源模型训练好的 NLA。

## 关键技术细节
- 发布：2026-05-07（Transformer Circuits Thread）。机构：Anthropic。作者含 Kit Fraser-Taliente、Subhash Kantamneni、Euan Ong、Jack Lindsey、Samuel Marks 等。
- 方法：NLA = activation verbalizer (AV) + activation reconstructor (AR) 两个 LLM 模块。
- 训练：用强化学习联合训练 AV/AR，目标为重建残差流(residual stream)激活；无监督。
- 性质：解释随训练越来越有信息量（定量评估）；提供可直接阅读的自然语言解释接口。
- 应用：Claude Opus 4.6 部署前审计——诊断安全相关行为；揭示 unverbalized evaluation awareness（模型相信但未说出正被评估）。
- 基准：自动审计基准（端到端调查故意错位模型）上 NLA-equipped agent 超基线，且无需访问错位模型训练数据也能成功。
- 开源：释放训练代码与针对流行开源模型训练好的 NLA。

## 原始链接
- url: https://transformer-circuits.pub/2026/nla/
- 配套官方页: https://www.anthropic.com/research/natural-language-autoencoders

## 本地落盘文件
- ../../../sources/llm/2026/anthropic-nla.html
