---
title: "GLM-4-Voice: Towards Intelligent and Human-Like End-to-End Spoken Chatbot"
org: 智谱 AI (Zhipu AI) / 清华大学
country: 中国
date: 2024-12
type: arxiv
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2412.02612
pdf_url: https://arxiv.org/pdf/2412.02612
github_url: https://github.com/THUDM/GLM-4-Voice
downloaded: [files/glm-4-voice.pdf]
---

## 一句话定位
端到端中英双语语音对话模型，用超低比特率（175bps）单码本语音 tokenizer + 语音-文本交错预训练，实现实时、可控情感/语速/方言的语音交互。

## 摘要
GLM-4-Voice 是端到端、类人语音聊天机器人，支持中英双语实时语音对话，可按指令变化情感、语调、语速、方言。其语音 tokenizer 由 ASR 模型加 vector-quantized bottleneck 改造而来，超低比特率 175bps、单码本、12.5Hz 帧率。为高效把文本知识迁移到语音模态，从已有文本预训练语料合成"语音-文本交错"数据，并在预训练好的文本模型上继续预训练。

## 关键技术细节（带数字）
- 语音 tokenizer：单码本、175bps 超低比特率、12.5Hz 帧率（基于 ASR + VQ bottleneck）。
- 训练：从文本预训练语料合成 speech-text interleaved 数据，在文本基座（GLM-4-9B）上继续预训练。
- 解码：流式 speech decoder（基于 flow-matching），低延迟。
- 能力：实时双语语音对话，可控情感/语调/语速/方言。

## 原始链接
- arXiv: https://arxiv.org/abs/2412.02612
- PDF: https://arxiv.org/pdf/2412.02612
- GitHub: https://github.com/THUDM/GLM-4-Voice

## 一手源存档（sources/）
- glm-4-voice.pdf  （PDF 不入 git，走 HF bucket）
