---
title: Nemotron 3 Super: Open, Efficient Mixture-of-Experts Hybrid Mamba-Transformer Model for Agentic Reasoning
org: NVIDIA    country: US    date: 2026-04    type: paper
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://arxiv.org/abs/2604.12374    pdf_url: https://arxiv.org/pdf/2604.12374    github_url:
downloaded: [arxiv-2604.12374.pdf]
---

## 一句话定位
NVIDIA 2026-04 发布的 Nemotron 3 Super——120B 总 / 12B 激活的混合 Mamba-Attention MoE 模型，是 Nemotron 3 家族首个 NVFP4 预训练 + LatentMoE + MTP 的模型，1M 上下文，全开源。

## 摘要
Nemotron 3 Super 是 120B 总参数（12B 激活）的混合 Mamba-Attention MoE 模型。它是 Nemotron 3 家族首个：1) 用 NVFP4 预训练；2) 采用 LatentMoE（同时优化 accuracy/FLOP 与 accuracy/参数）；3) 含 MTP 层（通过原生投机解码加速推理）。预训练用 25T token，随后用 SFT + RL 后训练。最终模型支持 1M 上下文，在常见基准上精度相当，同时相比 GPT-OSS-120B 与 Qwen3.5-122B 推理吞吐分别高达 2.2× 与 7.5×。数据集与 base/post-trained/quantized 检查点在 HuggingFace 开源。

## 关键技术细节
- 提交日期：2026-04-14（PDF 标注 2026-4-15）。机构：NVIDIA。
- 规模：120B 总参数 / 12B 激活；混合 Mamba-Attention MoE。
- 预训练：25T token；首次 NVFP4 精度预训练。
- 架构创新：LatentMoE（优化每 FLOP 与每参数精度）；MTP 层（原生投机解码）。
- 上下文：up to 1M。
- 后训练：SFT + RL。
- 性能：吞吐相比 GPT-OSS-120B 2.2×、相比 Qwen3.5-122B 7.5×；精度 comparable。
- 开源：数据集 + base/post-trained/quantized 检查点（HuggingFace）。
- 配套技术报告：research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3-Super-Technical-Report.pdf。

## 原始链接
- url: https://arxiv.org/abs/2604.12374
- pdf_url: https://arxiv.org/pdf/2604.12374

## 本地落盘文件
- ../../../sources/llm/2026/arxiv-2604.12374.pdf
