---
title: NVIDIA Nemotron Nano 2 (Nemotron-Nano-9B-v2)
org: NVIDIA
country: US
date: 2025-08
type: technical-report
categories: [架构, 预训练数据, 后训练, AI infra]
url: https://arxiv.org/abs/2508.14444
pdf_url: https://arxiv.org/pdf/2508.14444
github_url:
downloaded: [files/nemotron-nano-2.pdf]
---

## 一句话定位
NVIDIA 2025-08 的 Nemotron Nano 2 技术报告：基于 Nemotron-H 架构的 hybrid Mamba-Transformer 推理模型 Nemotron-Nano-9B-v2，FP8 在 20T token 上预训练 12B 再压缩，单张 A10G 即可 128k 推理、reasoning 吞吐最高 6x。

## 摘要
Nemotron-Nano-9B-v2 在 Nemotron-H 架构上（大多数自注意力替换为 Mamba-2 层）为推理工作负载提升吞吐：先用 FP8 配方在 20T token 上预训练 12B 基座（Nemotron-Nano-12B-v2-Base），对齐后用 Minitron 策略压缩蒸馏，目标是单张 A10G（22GiB、bf16）上做到 128k token 推理。相较 Qwen3-8B，推理吞吐最高 6x（8k 输入/16k 输出场景）而精度持平或更优。多数预/后训练数据集随权重一并开源。

## 关键技术细节（带数字）
- 模型：Nemotron-Nano-9B-v2（hybrid Mamba-Transformer，基于 Nemotron-H，多数 self-attention 替换为 Mamba-2）。
- 预训练：先训 12B（Nemotron-Nano-12B-v2-Base），FP8 训练配方，20 万亿（20T）tokens。
- 压缩：对齐后用 Minitron 策略剪枝/蒸馏到 9B。
- 部署：单张 NVIDIA A10G（22GiB、bfloat16）上支持最高 128k tokens 推理。
- 吞吐：reasoning 场景（8k 输入/16k 输出）相对 Qwen3-8B 最高 6x，精度持平或更优。
- 开源：Nemotron-Nano-9B-v2 / 12B-v2-Base / 9B-v2-Base 检查点 + 大部分预/后训练数据集（Hugging Face）。
- 发布日期：2025-08（arXiv:2508.14444）。

## 原始链接
- arXiv：https://arxiv.org/abs/2508.14444
- PDF：https://arxiv.org/pdf/2508.14444

## 本地落盘文件
- ../../../sources/llm/2025/nemotron-nano-2.pdf
