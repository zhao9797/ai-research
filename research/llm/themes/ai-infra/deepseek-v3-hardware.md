---
title: Insights into DeepSeek-V3: Scaling Challenges and Reflections on Hardware for AI Architectures
org: DeepSeek-AI
country: China
date: 2025-05
type: paper
categories: [AI infra, 架构]
url: https://arxiv.org/abs/2505.09343
pdf_url: https://arxiv.org/pdf/2505.09343
downloaded: [deepseek-v3-hardware-2505.09343.pdf]
---

## 一句话定位
DeepSeek 从 V3 训练实践出发，反思 LLM 与硬件的协同设计（内存、算力、互联），系统披露 FP8 训练、MLA、MoE、Multi-Plane 网络拓扑等 infra 细节，是面向硬件架构师的总结。

## 摘要（3-6 句）
论文以 DeepSeek-V3（2048×H800 训练）为例，分析当前硬件在内存容量、算力效率、互联带宽上的瓶颈，并展示 hardware-aware 模型协同设计如何缓解。关键创新包括：MLA 提升内存效率、MoE 优化算力-通信权衡、FP8 混合精度训练释放硬件潜力、Multi-Plane 网络拓扑降低集群网络成本。论文还对下一代硬件给出建议（如更鲁棒的低精度、scale-up/scale-out 融合、网络拓扑），是少见的厂商一手硬件协同设计反思。

## 关键技术细节
- 训练集群：2048×NVIDIA H800；分析 memory wall、compute、interconnect 三大约束。
- MLA 减小 KV cache（内存效率）；MoE 在固定算力下增大有效容量并平衡通信。
- FP8 混合精度训练的工程要点与精度保持；对硬件 FP8/低精度支持的诉求。
- Multi-Plane Fat-Tree 网络拓扑降低互联成本与拥塞；对未来 AI 硬件（scale-up domain、网络、低精度）的建议。

## 原始链接
- url: https://arxiv.org/abs/2505.09343
- pdf_url: https://arxiv.org/pdf/2505.09343

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/deepseek-v3-hardware-2505.09343.pdf
