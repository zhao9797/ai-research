---
title: "Large Enough (Mistral Large 2)"
org: Mistral AI
country: EU
date: 2024-07
type: blog
categories: [架构, 后训练]
url: https://mistral.ai/news/mistral-large-2407/
pdf_url:
github_url:
downloaded: [mistral-large-2-blog.md]
---

## 一句话定位
Mistral Large 2（123B）发布博客：单节点推理设计、128K 上下文、80+ 编程语言，专门针对减少幻觉与提升指令遵循做了对齐。

## 摘要
2024-07-24 发布。Mistral Large 2 有 128K 上下文，支持数十种自然语言（法/德/西/意/葡/阿/印地/俄/中/日/韩等）与 80+ 编程语言（Python/Java/C/C++/JS/Bash 等）。123B 参数，为单节点长上下文高吞吐推理设计。强调在代码与推理上的大幅提升，并专门训练以在缺乏信息时承认"不知道"而非编造，从而减少幻觉；还加强了指令遵循与对话能力。以 Mistral Research License 发布（研究/非商用可用、修改），商用自部署需商业许可。

## 关键技术细节
- 规模：123B 参数（稠密），单节点高吞吐推理。
- 上下文：128K token。
- 语言：数十种自然语言 + 80+ 编程语言。
- 对齐：减少幻觉（信息不足时承认不知）、更强指令遵循、更简洁回复。
- 能力：代码与数学大幅提升，比肩 GPT-4o/Claude 3 Opus/Llama 3.1 405B。
- 许可：Mistral Research License（研究/非商用）；商用需 Mistral Commercial License。

## 原始链接
- url: https://mistral.ai/news/mistral-large-2407/

## 一手源存档（sources/）
- [mistral-large-2-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/mistral-large-2-blog.md)
