---
title: "MiniMax-01: Scaling Foundation Models with Lightning Attention"
org: MiniMax
country: China
date: 2025-01
type: report
categories: [架构, AI infra]
url: https://arxiv.org/abs/2501.08313
pdf_url: https://arxiv.org/pdf/2501.08313
github_url: https://github.com/MiniMax-AI/MiniMax-01
downloaded: [minimax-01.pdf]
---

## 一句话定位
MiniMax-01 把 lightning attention（线性注意力）与 MoE 大规模结合，456B 总参/45.9B 激活，训练 1M 上下文、推理外推到 4M，是首个把线性注意力 scale 到数百亿激活的旗舰。

## 摘要（3-6 句）
MiniMax-01 系列（MiniMax-Text-01、MiniMax-VL-01）在长上下文处理上突出，核心是 lightning attention 及其高效扩展。为最大化算力，作者把它与 MoE 结合，构成 32 专家、456B 总参、每 token 激活 45.9B 的模型，并设计优化并行策略与计算-通信重叠技术，使数百亿参数模型可在百万级上下文上高效训练/推理。MiniMax-Text-01 训练时上下文达 1M token，推理可外推到 4M。视觉版 MiniMax-VL-01 通过 5120 亿视觉语言 token 继续训练得到。实验显示其匹敌 GPT-4o、Claude-3.5-Sonnet，同时上下文窗口长 20-32 倍。

## 关键技术细节
- lightning attention：I/O 感知的线性注意力实现（chunkwise），把注意力降到线性复杂度。
- 混合：每 7 层 lightning attention 配 1 层 softmax 注意力（hybrid），兼顾长程线性与精确回忆。
- 规模：456B 总参 / 45.9B 激活；32 专家 MoE。
- 上下文：训练 1M token，推理外推 4M token。
- infra：定制并行 + 计算通信重叠，支持百亿激活 + 百万上下文训练。
- 视觉版：512B 视觉语言 token 继续训练 → MiniMax-VL-01。
- 开源 MiniMax-01 权重。

## 原始链接
- url: https://arxiv.org/abs/2501.08313
- pdf_url: https://arxiv.org/pdf/2501.08313
- github_url: https://github.com/MiniMax-AI/MiniMax-01

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/minimax-01.pdf
