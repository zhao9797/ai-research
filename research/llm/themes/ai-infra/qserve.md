---
title: QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving
org: MIT (Han Lab) / NVIDIA
country: US
date: 2024-05
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2405.04532
pdf_url: https://arxiv.org/pdf/2405.04532
github_url: https://github.com/mit-han-lab/omniserve
downloaded: [qserve-2405.04532.pdf]
---

## 一句话定位
W4A8KV4（4-bit 权重、8-bit 激活、4-bit KV cache）量化加系统协同设计的推理引擎，针对 GPU 反量化开销做算法重设计，在 A100/L40S 上大幅超越 TensorRT-LLM 吞吐。

## 摘要（3-6 句）
作者指出 W4A8/W4A4 慢的根因是反量化在 CUDA core 的开销。QServe 提出 QoQ（Quattuor-Octo-Quattuor）算法：渐进式分组量化、SmoothAttention（保护 KV 离群）、把反量化计算转到寄存器级以降开销，并做系统级 fuse。结果在 A100/L40S 上对 Llama/Qwen 等模型相对 TensorRT-LLM 吞吐提升最高 2.4-3.5×，并显著降低部署成本（可用更便宜的 L40S 替代 A100）。

## 关键技术细节
- 量化格式：W4A8KV4（权重 INT4、激活 INT8、KV cache INT4）。
- QoQ 算法：progressive group quantization + SmoothAttention（迁移 KV 离群）+ register-level dequant 减少 CUDA core 开销。
- 性能：A100 上 Llama-3-8B 1.2× / Qwen 等更高；相对 TensorRT-LLM 最高约 2.4-3.5× 吞吐；L40S 成本优势明显。
- 开源为 omniserve/QServe 引擎。

## 原始链接
- url: https://arxiv.org/abs/2405.04532
- pdf_url: https://arxiv.org/pdf/2405.04532
- github_url: https://github.com/mit-han-lab/omniserve

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/qserve-2405.04532.pdf
