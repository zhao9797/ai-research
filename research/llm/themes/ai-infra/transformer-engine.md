---
title: NVIDIA Transformer Engine (FP8 Training Library)
org: NVIDIA
country: US
date: 2022-09
type: github
categories: [AI infra]
url: https://github.com/NVIDIA/TransformerEngine
github_url: https://github.com/NVIDIA/TransformerEngine
downloaded: [transformer-engine-readme.md]
---

## 一句话定位
NVIDIA 的 FP8/FP4 训练与推理加速库，在 Hopper/Ada/Blackwell 上为 Transformer 提供 FP8 building block 与自动混合精度式 API，是 H100 时代 FP8 大模型训练的官方底座。

## 摘要（3-6 句）
Transformer Engine（TE）为 NVIDIA GPU 提供高度优化的 Transformer 算子，核心是把 Hopper 引入的 FP8 精度落地：用 per-tensor 缩放 + delayed/current scaling 自动管理 FP8 动态范围，在保持收敛精度的同时相比 FP16 提速并省显存。它提供 PyTorch/JAX 的 Python 模块与框架无关的 C++ API，可被 Megatron-LM、NeMo、DeepSpeed、torchtitan、HF Accelerate 等集成。Blackwell 上进一步支持 FP4。仓库展示了 FP8 训练 loss 与 BF16 收敛一致。

## 关键技术细节
- FP8 支持：E4M3/E5M2 两种 FP8 格式；自动缩放（amax history、delayed scaling）维持动态范围。
- Hopper（SM90）/Ada/Blackwell（含 FP4）；fused attention（含 FlashAttention 后端）、LayerNorm、GEMM 等优化算子。
- API：Python（PyTorch/JAX）高层模块 + framework-agnostic C++ 库；可无缝插入现有训练代码。
- 集成：Megatron-LM、NeMo、DeepSpeed、torchtitan、MosaicML 等；FP8 收敛与 BF16 对齐。

## 原始链接
- url: https://github.com/NVIDIA/TransformerEngine
- github_url: https://github.com/NVIDIA/TransformerEngine

## 一手源存档（sources/）
- [transformer-engine-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/ai-infra/transformer-engine-readme.md)
