---
title: "MiMo: Unlocking the Reasoning Potential of Language Model -- From Pretraining to Posttraining"
org: 小米 (Xiaomi) MiMo / LLM-Core Team
country: China
date: 2025-05
type: paper
categories: [预训练数据, 后训练, AI infra]
url: https://arxiv.org/abs/2505.07608
pdf_url: https://arxiv.org/pdf/2505.07608
github_url: https://github.com/XiaomiMiMo/MiMo
downloaded: [xiaomi-mimo.pdf]
---

## 一句话定位
小米 MiMo-7B：从预训练到后训练全链路为推理优化的 7B 模型，RL 后超越 32B 模型甚至 OpenAI o1-mini，提出 MTP 加速 + test-time RL infra（Seamless Rollout）。发布 2025-05-12（v2 2025-06-05 扩 SFT 至 6M）。

## 摘要
MiMo-7B 证明小模型也能有强推理。预训练侧优化数据 pipeline、多维数据过滤、加入合成推理数据，并用三阶段数据混合在约 25T token 上训练；引入 Multiple-Token Prediction (MTP) 目标增强性能并加速推理。后训练侧精选 13 万可验证数学/代码题，用 test-time-scaling RL；提出 test difficulty driven reward 缓解难题稀疏奖励，并用 data re-sampling 稳定训练。开发 Seamless Rollout 引擎加速 RL 训练与验证。MiMo-7B-RL 在数学/代码推理上超越更大的 32B 模型，甚至匹敌/超过 OpenAI o1-mini。

## 关键技术细节
- 规模：7B dense；MTP（Multiple-Token Prediction）训练目标 + 推理加速（投机解码）。
- 预训练数据：约 25T tokens，三阶段数据混合，多维过滤 + 合成推理数据；强化 reasoning pattern 密度。
- RL 后训练：13 万可验证数学/代码题；test difficulty driven reward（按难度加权缓解稀疏奖励）；data re-sampling。
- RL infra：Seamless Rollout Engine，加速 rollout 与 reward 计算（GPU 利用率提升）。
- 成绩：MiMo-7B-RL 数学/代码超 32B 模型，匹敌/超 OpenAI o1-mini。
- 开源：base / SFT / RL 全套 checkpoint（GitHub XiaomiMiMo/MiMo）。

## 原始链接
- url: https://arxiv.org/abs/2505.07608
- pdf_url: https://arxiv.org/pdf/2505.07608
- github_url: https://github.com/XiaomiMiMo/MiMo

## 一手源存档（sources/）
- xiaomi-mimo.pdf  （PDF 不入 git，走 HF bucket）
