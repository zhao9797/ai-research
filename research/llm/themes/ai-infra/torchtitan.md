---
title: TorchTitan: One-stop PyTorch native solution for production ready LLM pre-training
org: Meta (PyTorch)
country: US
date: 2024-10
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2410.06511
pdf_url: https://arxiv.org/pdf/2410.06511
github_url: https://github.com/pytorch/torchtitan
downloaded: [torchtitan-2410.06511.pdf]
---

## 一句话定位
Meta/PyTorch 官方推出的 PyTorch 原生大模型预训练框架，整合 4D 并行、FSDP2、torch.compile、FP8 等，作为 Megatron 之外的 native 方案。

## 摘要（3-6 句）
TorchTitan 用 PyTorch 原生组件（DTensor、FSDP2、Tensor/Pipeline/Context Parallel、torch.compile、Float8）统一实现可组合的 4D 并行训练。它强调模块化与可组合性，让研究者用少量代码切换并行策略并叠加优化。论文在 Llama 3.1 系列（8B/70B/405B）上验证，相对优化基线在 8B/128GPU 上提速 65.08%，70B/256GPU 上 12.59%，405B/512GPU(H100) 上 30%。它是 PyTorch 社区对标 Megatron-LM 的官方训练栈。

## 关键技术细节
- 4D 并行：FSDP2（数据/参数分片）× Tensor Parallel × Pipeline Parallel × Context Parallel，全部基于 DTensor 可组合。
- 性能优化：torch.compile、Float8（FP8）训练、async TP、selective activation checkpoint、分布式 checkpoint。
- 实测加速（vs 优化基线）：Llama3.1-8B/128 H100 +65.08%；70B/256 +12.59%；405B/512 +30%。
- 目标：production-ready、PyTorch-native、易扩展，降低自研 3D 并行门槛。

## 原始链接
- url: https://arxiv.org/abs/2410.06511
- pdf_url: https://arxiv.org/pdf/2410.06511
- github_url: https://github.com/pytorch/torchtitan

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/torchtitan-2410.06511.pdf
