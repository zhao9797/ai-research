---
title: Magistral
org: Mistral AI
country: EU
date: 2025-06
type: report
categories: [后训练, AI infra]
url: https://arxiv.org/abs/2506.10910
pdf_url: https://arxiv.org/pdf/2506.10910
downloaded: [magistral.pdf]
---

## 一句话定位
Mistral 首个推理模型 Magistral：完全自研、不蒸馏外部推理模型的纯 RLVR 配方，提出改进版 GRPO 与可扩展异步 RL 基础设施，强调多语言推理保持。

## 摘要（3-6 句）
Magistral 是 Mistral AI 的首个推理模型与其自研可扩展 RL 系统。与多数复用 DeepSeek-R1 蒸馏轨迹的工作不同，Magistral 完全从零用 RLVR（可验证奖励 RL）在自家模型上训练，不依赖外部推理模型的蒸馏。报告公开训练栈、改进的 GRPO（去掉 KL 惩罚、归一化与裁剪调整等）、以及异步分布式 RL 基础设施细节。一个有趣发现是纯 RL 还能保留并提升多语言能力（让模型用提问语言思考）。发布 Magistral Small（开源权重，24B）与 Magistral Medium（企业版）。

## 关键技术细节
- 路线：纯 RLVR 从自家基座（Mistral Small/Medium 3）训练，不蒸馏外部推理模型轨迹。
- 算法：改进的 GRPO——去除 KL 惩罚、对 loss 做归一化、放宽上裁剪（类似 DAPO 的 clip-higher）、过滤零优势组、minibatch 归一化等。
- 奖励：可验证正确性（数学/代码）+ 格式与语言一致性奖励（鼓励用提问语言思考）。
- infra：异步分布式 RL 系统（generators / trainers / verifiers 解耦），高吞吐 rollout。
- 多语言：RL 后多语言推理能力保留甚至提升。
- 发布：Magistral Small 24B（Apache 2.0 开源权重）+ Magistral Medium（企业）。

## 原始链接
- url: https://arxiv.org/abs/2506.10910
- pdf_url: https://arxiv.org/pdf/2506.10910

## 一手源存档（sources/）
- magistral.pdf  （PDF 不入 git，走 HF bucket）
