---
title: "DeepSeek-Coder: When the Large Language Model Meets Programming -- The Rise of Code Intelligence"
org: 深度求索（DeepSeek-AI）
country: China
date: 2024-01
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2401.14196
pdf_url: https://arxiv.org/pdf/2401.14196
github_url: https://github.com/deepseek-ai/DeepSeek-Coder
downloaded: [deepseek-coder.pdf]
---

## 一句话定位
DeepSeek 的开源代码大模型系列（1.3B–33B），从零在 2T token（87% 代码）上训练，采用仓库级（repo-level）预训练与 Fill-in-the-Middle，是 2023/24 年最强开源代码模型之一。（2024-01 发布，属 2023 工作的跨年报告。）

## 摘要（3-6 句）
DeepSeek-Coder 由一系列 1.3B 到 33B 的开源代码模型组成，从零在 2 万亿 token 上训练，其中代码占比 87%、代码相关自然语言占 13%。采用 16K 上下文窗口和 Fill-in-the-Middle（FIM）目标以支持项目级代码补全与填空。通过仓库级别（而非文件级别）的数据组织，模型能利用跨文件依赖。DeepSeek-Coder-Base 33B 在多项编程基准上超过 CodeLlama-34B，指令微调版超过 GPT-3.5-Turbo。

## 关键技术细节
- 规模：1.3B / 5.7B / 6.7B / 33B；上下文窗口 16K。
- 数据：2T token；87% 源代码 + 10% 代码相关英文 + 3% 中文；覆盖 87 种编程语言。
- 仓库级预训练：按代码仓库组织、做拓扑排序解析跨文件依赖，构造仓库级样本。
- 训练目标：Next-token prediction + Fill-in-the-Middle（FIM，PSM 模式）支持填空式补全。
- 架构：基于 DeepSeek LLM 的 Transformer（RoPE、SwiGLU、GQA 用于大模型）；RoPE 经线性缩放扩到 16K。
- 后续 v1.5：在 DeepSeek-LLM-7B-Base 上继续用 2T token 训练得到 DeepSeek-Coder-Base-v1.5 7B（DeepSeekMath 的初始化模型）。
- 性能：33B-Base 超 CodeLlama-34B；Instruct 超 GPT-3.5-Turbo（HumanEval 等）。

## 原始链接
- url: https://arxiv.org/abs/2401.14196
- pdf_url: https://arxiv.org/pdf/2401.14196
- github_url: https://github.com/deepseek-ai/DeepSeek-Coder

## 一手源存档（sources/）
- deepseek-coder.pdf  （PDF 不入 git，走 HF bucket）
