---
title: PaLM 2 Technical Report
org: Google
country: US
date: 2023-05
type: report
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2305.10403
pdf_url: https://arxiv.org/pdf/2305.10403
downloaded: [palm-2.pdf]
---

## 一句话定位
Google 第二代 PaLM，强调计算最优、多语言与推理，背后是 Gemini 之前的旗舰底座（驱动 Bard/Duet）。

## 摘要
PaLM 2 是新一代 SOTA 语言模型，多语言与推理能力更强、比 PaLM 更省算力。基于 Transformer、用混合目标(mixture of objectives)训练。在英文与多语言、推理任务上跨尺寸全面提升，同时推理更快更省。在 BIG-Bench 等推理任务大幅超越 PaLM；在 responsible AI 评测稳定，支持推理期毒性控制。

## 关键技术细节
- 训练范式：遵循 Chinchilla 计算最优，参数量比 PaLM(540B) 小但数据更多（具体参数量官方未明示）。
- 训练目标：mixture of objectives（不仅是因果 LM）。
- 数据：更高比例多语言与代码数据，覆盖数百种语言。
- 尺寸：Gecko / Otter / Bison / Unicorn 等多档（report 未给具体参数数字）。
- 能力：多语言、推理(BIG-Bench Hard)、代码、翻译显著提升；首次实现推理期可控毒性而不损能力。
- 产品落地：驱动 Bard、Workspace Duet AI、Med-PaLM 2、Sec-PaLM 等。

## 原始链接
- url: https://arxiv.org/abs/2305.10403
- pdf_url: https://arxiv.org/pdf/2305.10403

## 本地落盘文件
- ../../../sources/llm/2023/palm-2.pdf
