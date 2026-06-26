---
title: Releasing 3B and 7B RedPajama-INCITE Family of Models
org: Together AI
country: US
date: 2023-05
type: blog
categories: [预训练数据, 后训练]
url: https://www.together.ai/blog/redpajama-models-v1
downloaded: [redpajama-incite-together.html]
---

## 一句话定位
Together 发布首批基于 RedPajama 开放数据集训练的 3B/7B 模型，复刻 LLaMA 配方，完全开源可商用。

## 摘要
Together 官方博客，发布首批用 RedPajama 基础数据集训练的模型：3B 与 7B 基础模型，尽量复刻 LLaMA 配方。3B 是同尺寸最强(甚至能在 5 年前的 RTX 2070 上跑)；7B(训练 80% 时)已超过 Pythia 7B，显示更大数据集与 RedPajama 数据的价值。均含 base/chat/instruct 变体，Apache 2.0 可商用。

## 关键技术细节
- 数据：RedPajama v1 开放数据集(复刻 LLaMA 配方，约 1.2T token)。
- 模型：RedPajama-INCITE-Base/Chat/Instruct，3B 与 7B 两档；架构同 Pythia 套件。
- 训练 token：3B 训到 800B(已稳定)；7B 训到 800B/1T(持续提升)。
- infra：在 Oak Ridge Summit 超算上训练(INCITE 项目)，用 EleutherAI 的 DeeperSpeed 代码库。
- 微调：Chat 用 OASST1(OpenAssistant)+Dolly 2.0；Instruct 用 GPT-JT 配方(剔除 HELM 重叠数据防污染)。
- 评测：HELM 上 7B 超基础 LLaMA 3 分；7B 超 Pythia 7B。
- 许可：Apache 2.0，研究 + 商用。

## 原始链接
- url: https://www.together.ai/blog/redpajama-models-v1

## 一手源存档（sources/）
- [redpajama-incite-together.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/redpajama-incite-together.html)
