---
title: "UL2: Unifying Language Learning Paradigms"
org: Google Research (Brain)
country: US
date: 2022-05
type: paper
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2205.05131
pdf_url: https://arxiv.org/pdf/2205.05131
github_url: https://github.com/google-research/google-research/tree/master/ul2
downloaded: [ul2.pdf]
---

## 一句话定位
提出 Mixture-of-Denoisers（MoD）统一预训练目标 + mode switching，得到 20B 的 UL2，超越 T5/GPT 式单一目标模型。

## 摘要
现有预训练模型通常只擅长某类问题，业界对"正确架构与预训练设置"尚无共识。UL2 提出统一框架：先解耦架构原型与预训练目标，再用统一视角把不同自监督目标互相转化，并提出 Mixture-of-Denoisers（MoD）把多种预训练范式（前缀语言建模、不同 span 长度的去噪）混合，配合"mode switching"在下游微调时切换模式。大量消融表明 UL2 推开 Pareto 前沿，超过 T5 与 GPT 式基线。

## 关键技术细节
- MoD：混合三类去噪器——R-denoiser（常规 span corruption）、S-denoiser（顺序/前缀 LM）、X-denoiser（极端去噪，长 span/高 mask 率）。
- Mode switching：用特殊 paradigm token 在预训练和微调时指定使用哪类去噪模式。
- 模型：UL2-20B，encoder-decoder 架构，约 32 层，在 C4 上训练约 1T token。
- 结果：在 50+ NLP 任务上超越 T5-XXL 与 GPT-like baseline；支持 in-context learning 与 CoT（后续 Flan-UL2、U-PaLM 沿用）。
- 公开 20B 检查点。

## 原始链接
- url: https://arxiv.org/abs/2205.05131
- pdf_url: https://arxiv.org/pdf/2205.05131
- github_url: https://github.com/google-research/google-research/tree/master/ul2

## 本地落盘文件
- ../../../sources/llm/2022/ul2.pdf
