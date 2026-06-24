---
title: "BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models"
org: Salesforce Research
country: US
date: 2023-01
type: paper
categories: [架构]
url: https://arxiv.org/abs/2301.12597
pdf_url: https://arxiv.org/pdf/2301.12597
github_url: https://github.com/salesforce/LAVIS/tree/main/projects/blip2
downloaded: [blip2.pdf]
---

## 一句话定位
BLIP-2 用轻量的 Querying Transformer (Q-Former) 桥接冻结的图像编码器和冻结的 LLM，两阶段预训练，以远少的可训练参数达到 VL 任务 SOTA。

## 摘要（3-6 句）
端到端训练大规模视觉语言模型代价高昂。BLIP-2 提出从现成的冻结图像编码器和冻结 LLM 引导出 VL 能力，用一个轻量 Q-Former 跨越模态鸿沟。Q-Former 两阶段预训练：第一阶段从冻结图像编码器学视觉-语言表示对齐；第二阶段把视觉信息接入冻结 LLM 做视觉到语言的生成学习。BLIP-2 在多项 VL 任务上 SOTA，可训练参数远少于端到端方法（如比 Flamingo-80B 少约 54× 可训练参数）。

## 关键技术细节
- Q-Former：一组可学习 query token 通过 cross-attention 从冻结图像编码器抽取固定数量视觉特征，再喂给 LLM。
- 两阶段：① 视觉-语言表示学习（图文对比 + 匹配 + 图引导文本生成）；② 视觉到语言生成（接 OPT / FlanT5 等冻结 LLM）。
- 参数高效：图像编码器与 LLM 全冻结，只训 Q-Former；可训练参数远少于 Flamingo。
- 结果：VQAv2、图像字幕等 SOTA；具零样本图文对话与指令能力。

## 原始链接
- url: https://arxiv.org/abs/2301.12597
- pdf_url: https://arxiv.org/pdf/2301.12597
- github_url: https://github.com/salesforce/LAVIS/tree/main/projects/blip2

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/blip2.pdf
