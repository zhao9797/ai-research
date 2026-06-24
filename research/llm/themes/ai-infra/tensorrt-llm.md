---
title: NVIDIA TensorRT-LLM
org: NVIDIA
country: US
date: 2023-08
type: github
categories: [AI infra]
url: https://github.com/NVIDIA/TensorRT-LLM
github_url: https://github.com/NVIDIA/TensorRT-LLM
downloaded: [tensorrt-llm-readme.md]
---

## 一句话定位
NVIDIA 官方 LLM 推理优化库，提供 Python API 定义模型并编译为高性能 TensorRT 引擎，集成量化、in-flight batching、PD 分离、投机解码等 SOTA 推理优化。

## 摘要（3-6 句）
TensorRT-LLM 让用户用 Python API 定义 LLM 并应用 NVIDIA GPU 上的一系列 SOTA 推理优化，生成 Python/C++ 运行时高效执行。它支持 FP8/FP4/INT8/INT4（含 SmoothQuant、AWQ、GPTQ）量化、in-flight（continuous）batching、paged KV cache、张量/流水/专家并行、speculative decoding、PD 分离等。配合 Triton Inference Server 部署，是 NVIDIA 在 Hopper/Blackwell 上的旗舰推理栈，也是众多 MLPerf Inference 记录的基础。

## 关键技术细节
- 模型定义：Python API（类 PyTorch）→ 编译为 TensorRT engine；含手工优化的 fused kernel。
- 量化：FP8/FP4、INT8/INT4，集成 SmoothQuant、AWQ、GPTQ；KV cache 量化。
- 推理优化：in-flight batching、paged KV cache、chunked prefill、speculative decoding、PD 分离。
- 并行：TP / PP / EP（MoE）；与 Triton Inference Server、NeMo、Dynamo 集成；支持 Llama/Qwen/DeepSeek/Mixtral 等。

## 原始链接
- url: https://github.com/NVIDIA/TensorRT-LLM
- github_url: https://github.com/NVIDIA/TensorRT-LLM

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/tensorrt-llm-readme.md
