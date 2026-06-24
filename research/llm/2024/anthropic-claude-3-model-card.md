---
title: The Claude 3 Model Family - Opus, Sonnet, Haiku (Model Card)
org: Anthropic
country: US
date: 2024-03
type: model-card
categories: [架构, 后训练]
url: https://www.anthropic.com/claude-3-model-card
pdf_url: https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf
github_url:
downloaded: [anthropic-claude-3-model-card.pdf]
---

## 一句话定位
Claude 3（Opus/Sonnet/Haiku）官方模型卡 PDF，给出基准全表、训练方法（含 Constitutional AI）、安全评估与负责任 scaling 说明。

## 摘要
Claude 3 模型卡详述三档模型的能力、训练与评估。模型在推理、数学、编程、多语言和视觉上达到 SOTA，统一 200K 上下文。训练数据为公开网络（截至 2023-08）、第三方授权数据与内部标注数据的混合；对齐采用人类反馈 + Constitutional AI（含 Anthropic 的 constitution 增加了一条关于行星福祉的原则）。卡片含完整基准表、长上下文召回、多模态评测、以及按 ASL（Responsible Scaling Policy）的安全分级。

## 关键技术细节
- 模型档位：Opus / Sonnet / Haiku，全部 200K 上下文。
- 训练数据：截至 2023-08 的公开网络数据 + 非公开第三方数据 + 数据标注/内部生成数据；用了数据去重与分类器过滤。
- 对齐：RLHF + Constitutional AI（Constitutional AI 用模型自身依据"宪法"进行偏好标注）。
- 多模态：图像/图表/照片/文档理解。
- 基准（Opus，5-shot/CoT 视基准）：MMLU 86.8%（5-shot）、GPQA Diamond、GSM8K、MATH、HumanEval 84.9% 等领先值（详见卡内表）。
- 安全：按 Responsible Scaling Policy 评为 ASL-2；含红队、偏见（BBQ）、可信度评估。

## 原始链接
- url: https://www.anthropic.com/claude-3-model-card
- pdf_url: https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf

## 本地落盘文件
- ../../../sources/llm/2024/anthropic-claude-3-model-card.pdf
