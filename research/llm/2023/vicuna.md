---
title: "Vicuna: An Open-Source Chatbot Impressing GPT-4 with 90% ChatGPT Quality"
org: LMSYS Org（UC Berkeley / CMU / Stanford / UCSD / MBZUAI 联合）
country: US
date: 2023-03
type: blog
categories: [后训练, 数据, 评测]
url: https://lmsys.org/blog/2023-03-30-vicuna/
pdf_url: ""
github_url: https://github.com/lm-sys/FastChat
downloaded: [vicuna-lmsys-blog.html]
---

## 一句话定位
用 ShareGPT 上 7 万条真实用户-ChatGPT 多轮对话微调 LLaMA 得到的开源对话模型，训练成本仅约 300 美元，首次提出"GPT-4 当裁判"的自动评测框架，是 2023 上半年开源对齐路线的标志性工作（与 Alpaca 并列），后续催生 FastChat / Chatbot Arena / MT-Bench。

## 摘要
LMSYS 推出 Vicuna-13B：在 LLaMA 基座上用 ShareGPT.com 收集的约 70K 条用户分享的 ChatGPT 对话做指令微调。用 GPT-4 当裁判的初步评测显示，Vicuna-13B 达到 OpenAI ChatGPT / Google Bard 约 90%* 的质量，并在 90%* 的对比中胜过 LLaMA 与 Stanford Alpaca。13B 训练成本约 300 美元。代码（FastChat）与权重以非商用形式开放，并提供在线 demo。作者强调"GPT-4 评测"是有趣但非严谨的初步方法，仍需进一步研究。

## 关键技术细节
- 基座：LLaMA（7B / 13B），非自研预训练。
- 数据：约 70K 条 ShareGPT.com 用户分享的 ChatGPT 多轮对话；做 HTML→Markdown 还原、过滤低质/不当样本、长对话切分以适配最大上下文。
- 训练配方（在 Stanford Alpaca 脚本基础上改进）：
  - 多轮对话：调整训练损失，仅在 chatbot 输出 token 上计算微调 loss。
  - 上下文长度：从 Alpaca 的 512 扩展到 2048（显著增加显存压力），用 gradient checkpointing + flash attention 缓解。
  - 成本优化：用 SkyPilot managed spot 实例（自动抢占恢复/换区），把 7B 训练成本从约 $500 压到约 $140、13B 从约 $1K 压到约 $300。
- 训练算力：PyTorch FSDP，8×A100，约 1 天。
- 评测框架（GPT-4-as-a-judge 雏形）：设计 8 类问题（费米题、角色扮演、编码/数学等），每类 10 题共 80 题；收集 LLaMA / Alpaca / ChatGPT / Bard / Vicuna 五个模型答案，让 GPT-4 按 helpfulness/relevance/accuracy/detail 打分并给出解释。作者明确指出该方法尚不严谨（如 GPT-4 不擅长判断代码/数学）。
- 对比表（官方 Table 1）：LLaMA=公开数据 1T token；Alpaca=self-instruct from davinci-003，52K 样本；Vicuna=用户对话 70K 样本；LLaMA 训练成本 7B≈82K GPU-hours、13B≈135K GPU-hours。
- 服务系统：支持多模型、分布式 worker、跨本地集群与云的 GPU 插拔，容错 controller + SkyPilot spot 降本（后演化为 FastChat / Chatbot Arena）。

## 原始链接
- url: https://lmsys.org/blog/2023-03-30-vicuna/
- github_url: https://github.com/lm-sys/FastChat
- 注：Vicuna 本身以官方博客发布；其评测方法的严谨化版本见后续论文《Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena》(arXiv:2306.05685)。

## 一手源存档（sources/）
- [vicuna-lmsys-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/vicuna-lmsys-blog.html)
