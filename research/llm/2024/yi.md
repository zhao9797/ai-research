---
title: "Yi: Open Foundation Models by 01.AI"
org: 零一万物 (01.AI)
country: 中国
date: 2024-03
type: arxiv
categories: [预训练数据, 架构, 后训练]
url: https://arxiv.org/abs/2403.04652
pdf_url: https://arxiv.org/pdf/2403.04652
github_url: https://github.com/01-ai/Yi
downloaded: [files/yi.pdf]
---

## 一句话定位
零一万物 Yi 基础模型家族（6B/34B），核心叙事是"数据工程优先"——以高质量数据 + 精细去重/过滤打造强力开源双语模型。

## 摘要
Yi 模型家族基于 6B 和 34B 预训练语言模型，并扩展出 chat、200K 长上下文、深度放大（depth-upscaled）与视觉语言模型。性能归因于以数据质量为中心：预训练用 3.1T 高质量中英 token（级联式去重 + 质量过滤）；微调用经多轮打磨、规模约 1 万条的小而精指令数据集（每条人工校验）。

## 关键技术细节（带数字）
- 规模：6B 与 34B（标准 Transformer，GQA、SwiGLU、RoPE）。
- 预训练数据：3.1T tokens 中英双语；强调级联数据清洗（启发式 + 学习式过滤 + 去重）。
- 上下文：从 4K 扩展到 200K（长上下文版）。
- 微调：约 10K 条精挑指令数据，人工逐条校验（quality over quantity）。
- 衍生：Yi-VL（视觉）、Yi-34B-Chat、depth-upscaling 版。

## 原始链接
- arXiv: https://arxiv.org/abs/2403.04652
- PDF: https://arxiv.org/pdf/2403.04652
- GitHub: https://github.com/01-ai/Yi

## 一手源存档（sources/）
- yi.pdf  （PDF 不入 git，走 HF bucket）
