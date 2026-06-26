---
title: "Yi-Coder-9B-Chat (Model Card)"
org: 零一万物 (01.AI)
country: 中国
date: 2024-09
type: model-card
categories: [预训练数据, 架构]
url: https://huggingface.co/01-ai/Yi-Coder-9B-Chat
pdf_url:
github_url: https://github.com/01-ai/Yi-Coder
downloaded: [files/yi-coder-hf-readme.md]
---

## 一句话定位
零一万物 2024-09 发布的开源代码模型（1.5B/9B），9B 在 10B 以下开源代码模型中编程能力领先，支持 128K 上下文与 52 种语言。

## 摘要
Yi-Coder 是 Yi 系列的代码专用模型，提供 1.5B 与 9B 两档（Base 与 Chat）。官方 model card 称其为参数 100 亿以下开源代码模型中性能领先者，支持长上下文工程级编程与多语言代码理解/生成。

## 关键技术细节（带数字）
- 规模：Yi-Coder-1.5B 与 Yi-Coder-9B（均含 Base/Chat），均为 <10B 参数。
- 编程语言：支持 52 种主要编程语言。
- 上下文：128K（长上下文工程级代码理解）。
- 性能：Yi-Coder-9B-Chat 在 LiveCodeBench 上 pass 率 23%，是唯一突破 20% 的 <10B 开源代码模型；超过 DeepSeek-Coder-33B-Ins(22.3%)、CodeGeeX4-9B(17.8%)、CodeLlama-34B-Ins(13.3%)、CodeQwen1.5-7B-Chat(12%)。
- 关联：Yi-Coder 基座持续预训练自 Yi 系列（论文 arXiv:2403.04652）。

## 原始链接
- HF model card: https://huggingface.co/01-ai/Yi-Coder-9B-Chat
- GitHub: https://github.com/01-ai/Yi-Coder

## 一手源存档（sources/）
- [yi-coder-hf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/yi-coder-hf-readme.md)
