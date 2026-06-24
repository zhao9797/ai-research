---
title: AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration
org: MIT (Han Lab) / SJTU / others
country: US
date: 2023-06
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2306.00978
pdf_url: https://arxiv.org/pdf/2306.00978
github_url: https://github.com/mit-han-lab/llm-awq
downloaded: [awq-2306.00978.pdf]
---

## 一句话定位
激活感知的权重量化：依据激活分布找出约 1% 的“重要权重通道”并按 per-channel 缩放保护它们，无需反向传播即可 4-bit 量化且优于 GPTQ，配套 TinyChat 推理引擎。

## 摘要（3-6 句）
AWQ 观察到权重重要性由激活幅度决定：保护约 1% 显著通道即可大幅减小量化误差。它通过逐通道缩放（等价数学变换）在量化前放大显著通道，避免混合精度的硬件低效，且不依赖反向传播或重构数据，泛化性好（对指令微调/多模态模型也稳）。AWQ 4-bit 在多种 LLM 上优于 GPTQ，配套的 TinyChat 引擎在桌面与移动 GPU 上相对 FP16 实现 3× 以上加速。MLPerf/边缘部署广泛采用。

## 关键技术细节
- 核心：activation-aware per-channel scaling，保护 top-~1% salient weight channel；纯权重 4-bit（INT4，group-wise）。
- 不需反传/重构集，校准数据少、抗过拟合，泛化到 instruction-tuned 与 multimodal 模型。
- TinyChat 引擎：on-the-fly 反量化 + kernel fusion，桌面/移动端 3-4× over FP16。
- 优于 GPTQ 的低比特精度，尤其在小校准集与跨域设置下。

## 原始链接
- url: https://arxiv.org/abs/2306.00978
- pdf_url: https://arxiv.org/pdf/2306.00978
- github_url: https://github.com/mit-han-lab/llm-awq

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/awq-2306.00978.pdf
