---
title: "Chameleon: Mixed-Modal Early-Fusion Foundation Models"
org: FAIR at Meta
country: US
date: 2024-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2405.09818
pdf_url: https://arxiv.org/pdf/2405.09818
downloaded: [chameleon.pdf]
---

## 一句话定位
Chameleon 是早融合、token 化的混合模态基础模型：把图像也量化成离散 token，与文本 token 放进同一 Transformer，单模型原生理解并生成任意交错的图文。

## 摘要（3-6 句）
Chameleon 是一族早融合 (early-fusion)、基于 token 的混合模态模型，能以任意顺序理解和生成图像与文本。论文给出从零开始的稳定训练方法、对齐配方，以及为早融合 token 化混合模态设计的架构参数化（如 QK-Norm、norm 重排等稳定技巧）。在视觉问答、图像字幕、文本生成、图像生成和长篇混合模态生成上评测，Chameleon 表现广泛：图像字幕 SOTA，纯文本超过 Llama-2、与 Mixtral 8x7B/Gemini-Pro 竞争，并能做图像生成；在长篇混合模态生成的人评中匹敌或超过 Gemini Pro、GPT-4V。

## 关键技术细节
- 早融合 token 化：用 image tokenizer（VQ）把图像编码成离散 token，与文本 token 共用统一词表，单一 Transformer 自回归建模二者。
- 训练稳定性：针对混合模态提出 QK-Norm、调整 LayerNorm 位置、dropout/z-loss 等以避免发散（早融合训练比单模态更难稳）。
- 单模型同时支持图文理解 + 图文生成 + 任意交错序列。
- 规模：训练到 7B、34B；34B 在多模态与纯文本上均强。
- 与「late-fusion」（视觉编码器接 LLM）路线对立，代表 native multimodal 方向。

## 原始链接
- url: https://arxiv.org/abs/2405.09818
- pdf_url: https://arxiv.org/pdf/2405.09818

## 一手源存档（sources/）
- chameleon.pdf  （PDF 不入 git，走 HF bucket）
