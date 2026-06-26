---
title: "MiMo-V2.5-Pro"
org: 小米 Xiaomi MiMo
country: China
date: 2026-04
type: model-card
categories: [架构, agentic训练]
url: https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro
pdf_url: ""
github_url: https://github.com/XiaomiMiMo
downloaded: [mimo-v2.5-pro-modelcard.md]
---

## 一句话定位
小米 MiMo-V2.5-Pro，1.02T 总参 / 42B 激活的开源 MoE 大模型，采用 MiMo-V2-Flash 的混合注意力 + 3 层 MTP，最高 1M 上下文，面向 agent / 长上下文 / 代码。

## 摘要
MiMo-V2.5-Pro（HuggingFace XiaomiMiMo 官方组织，createdAt 2026-04-27，blog mimo.xiaomi.com/mimo-v2-5-pro）是小米开源的 MoE 语言模型，1.02T 总参、42B 激活参数。它沿用 MiMo-V2-Flash 引入的 hybrid attention 架构与 3 层 Multi-Token Prediction (MTP)，上下文长度最高 1M token，标签覆盖 text-generation / agent / long-context / code，双语（en/zh）。MIT 许可，配套小米 MiMo API 平台与 MiMo Studio。同系列还含 MiMo-V2.5（标准版）、MiMo-V2.5-Base、MiMo-V2.5-Pro-Base、MiMo-V2.5-ASR，以及 2026-06 的 MiMo-V2.5-Pro-FP4-DFlash 量化版。

## 关键技术细节
- **规格**：1.02T 总参 / 42B 激活（MoE）。
- **架构**：hybrid attention（混合注意力）+ 3 层 Multi-Token Prediction (MTP)，沿用 MiMo-V2-Flash。
- **上下文**：最高 1,000,000 token。
- **定位标签**：text-generation / agent / long-context / code；双语 en+zh。
- **系列矩阵**：MiMo-V2.5 / MiMo-V2.5-Pro / MiMo-V2.5-Base / MiMo-V2.5-Pro-Base / MiMo-V2.5-ASR（2026-04）；MiMo-V2.5-Pro-FP4-DFlash（2026-06，FP4 量化）。
- **许可/生态**：MIT；platform.xiaomimimo.com（API）、aistudio.xiaomimimo.com（Studio）。

## 原始链接
- url: https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro
- blog: https://mimo.xiaomi.com/mimo-v2-5-pro
- github_url: https://github.com/XiaomiMiMo

## 一手源存档（sources/）
- [mimo-v2.5-pro-modelcard.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/mimo-v2.5-pro-modelcard.md)
