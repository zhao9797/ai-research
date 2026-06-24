---
title: "ChatGLM2-6B: An Open Bilingual Chat LLM（官方 GitHub）"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua KEG）
country: China
date: 2023-06
type: github
categories: [架构, 预训练数据, 后训练]
url: https://github.com/THUDM/ChatGLM2-6B
pdf_url:
github_url: https://github.com/THUDM/ChatGLM2-6B
downloaded: [chatglm2-6b-readme.md]
---

## 一句话定位
ChatGLM 第二代开源双语对话模型 ChatGLM2-6B：用 GLM 混合目标 + 1.4T 中英标识符预训练，引入 MQA 与 FlashAttention，上下文 2K→32K，是 2023 上半年中国开源对话模型代表（官方 GitHub 一手）。

## 摘要（3-6 句）
ChatGLM2-6B 是 ChatGLM-6B 的第二代版本。基座全面升级：采用 GLM 的混合目标函数，经 1.4T 中英标识符预训练 + 人类偏好对齐，相比初代在 MMLU(+23%)、C-Eval(+33%)、GSM8K(+571%)、BBH(+60%) 大幅提升。基于 FlashAttention 将上下文长度由 2K 扩到 32K（对话阶段用 8K 训练）；基于 Multi-Query Attention 提升推理速度并降低显存，INT4 量化下 6G 显存对话长度由 1K 提升到 8K。权重对学术研究完全开放，登记后允许免费商用。

## 关键技术细节
- 基座目标：GLM 混合目标函数（自回归空白填充）。
- 预训练量：1.4T 中英标识符 + 人类偏好对齐训练。
- 上下文：基于 FlashAttention，由 ChatGLM-6B 的 2K 扩展到 32K；对话阶段用 8K 训练；另发 ChatGLM2-6B-32K。
- 推理优化：Multi-Query Attention（MQA），推理速度较初代 +42%；INT4 量化下 6G 显存对话长度 1K→8K。
- 评测提升（相对初代）：MMLU +23%、C-Eval +33%、GSM8K +571%、BBH +60%。
- 生态：fastllm、chatglm.cpp、ChatGLM2-TPU（算能 BM1684X）等多端加速推理。
- 时间线：2023/06 ChatGLM2-6B；2023/07/31 ChatGLM2-6B-32K；衍生 CodeGeeX2（2023/07/25）。

## 原始链接
- url: https://github.com/THUDM/ChatGLM2-6B
- github_url: https://github.com/THUDM/ChatGLM2-6B

## 本地落盘文件
- ../../../sources/llm/2023/chatglm2-6b-readme.md
