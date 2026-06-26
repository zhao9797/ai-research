---
title: "Tongyi DeepResearch Technical Report"
org: "通义实验室(Tongyi Lab), 阿里巴巴"
country: CN
date: 2025-10
type: technical-report
categories: [模型发布, 后训练, agentic训练]
url: https://arxiv.org/abs/2510.24701
pdf_url: https://arxiv.org/pdf/2510.24701
github_url: https://github.com/Alibaba-NLP/DeepResearch
downloaded: [tongyi-deepresearch-2510.24701.pdf]
---

## 一句话定位
阿里通义开源的 deep research agentic 大模型：30.5B 总参 / 仅激活 3.3B（基于 Qwen3-30B-A3B-Base 的 MoE），用"agentic 中训练 + agentic 后训练"端到端范式 + 全自动数据合成，在 HLE/BrowseComp/GAIA 等深度研究基准上以更小参数拿到 SOTA。

## 摘要
Tongyi DeepResearch 是面向长时程、深度信息检索研究任务的 agentic 大模型。提出统一"agentic 中训练（mid-training）+ agentic 后训练（post-training）"的端到端训练框架：agentic 中训练用大规模高质量 agentic 数据培养内在 agentic 偏置，作为预训练到后训练的渐进过渡；agentic 后训练通过可扩展的多轮 RL 在强 base 上进一步释放潜力。配套一条完全自动、不依赖人工标注的高可扩展数据合成流水线，并为每个训练阶段构建定制环境保证交互稳定一致。模型仅 30.5B 总参、每 token 激活 3.3B，在多个 agentic deep research 基准上取得 SOTA，并完全开源模型、框架与方案。

## 关键技术细节
- 架构/规模：基于 Qwen3-30B-A3B-Base（MoE），总参 30.5B，每 token 仅激活 3.3B；上下文长度 128K tokens。开源于 HuggingFace `Alibaba-NLP/Tongyi-DeepResearch-30B-A3B` 与 ModelScope。
- 训练流水线：Pre-training → Mid-training（两阶段 Agentic CPT：Stage1 32K、Stage2 128K）→ Post-training（Agentic SFT 冷启动 → Agentic RL）。
- RL 算法：定制版 GRPO（token-level 目标、importance sampling ratio、非对称 clip ε_low/ε_high）。SFT 做行为克隆建立稳定基线，RL 与环境闭环、用奖励信号内化 agentic 规划与执行。
- 数据：全自动、可扩展的合成数据流水线，免人工标注，按各训练阶段目标定制（可构造超人类水平、分布稳定的数据集）。
- 评测设置：temperature=0.85、repetition penalty=1.1、top-p=0.95；单任务最多 128 次工具调用；上下文限 128K；每基准独立评 3 次报 Avg@3。
- 主结果（Avg@3）：Humanity's Last Exam 32.9、BrowseComp 43.4、BrowseComp-ZH 46.7、WebWalkerQA 72.2、GAIA 70.9、xbench-DeepSearch 75.0、FRAMES 90.6、xbench-DeepSearch-2510 55.0；在多项上超过 OpenAI-o3、DeepSeek-V3.1、GLM-4.5、Kimi-K2、Claude-4-Sonnet、OpenAI/Gemini DeepResearch 等。另报 AIME25/HMMT25/SimpleQA 等通用基准。

## 原始链接
- url: https://arxiv.org/abs/2510.24701
- pdf_url: https://arxiv.org/pdf/2510.24701
- github_url: https://github.com/Alibaba-NLP/DeepResearch
- HuggingFace: https://huggingface.co/Alibaba-NLP/Tongyi-DeepResearch-30B-A3B
- 官方博客: https://tongyi-agent.github.io/blog

## 一手源存档（sources/）
- [tongyi-deepresearch-2510.24701.pdf](https://arxiv.org/pdf/2510.24701)  （arXiv 原文 PDF，不入 git）
