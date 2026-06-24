---
title: DeepSeek-V3 Technical Report
org: DeepSeek
country: China
date: 2025-02
type: paper
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://arxiv.org/abs/2412.19437
pdf_url: https://arxiv.org/pdf/2412.19437
github_url: https://github.com/deepseek-ai/DeepSeek-V3
downloaded: [deepseek-v3.pdf]
---

## 一句话定位
DeepSeek 的 671B MoE 旗舰基座，以极低训练成本（约 2.788M H800 GPU 小时）训练，是 R1 的底座，2025 年中国开源大模型的成本标杆。（v1 2024-12-27，v2 修订 2025-02-18。）

## 摘要
DeepSeek-V3 是 671B 总参、每 token 激活 37B 的 MoE 模型，采用 MLA（Multi-head Latent Attention）与 DeepSeekMoE 架构，引入无辅助损失的负载均衡策略（auxiliary-loss-free load balancing）与多 token 预测（MTP）训练目标。在 14.8T token 上预训练，FP8 混合精度训练，全程无不可恢复 loss spike、无回滚。总训练成本约 2.788M H800 GPU 小时。

## 关键技术细节
- 架构：MLA（压缩 KV cache）+ DeepSeekMoE（细粒度专家 + 共享专家）；总参 671B，激活 37B。
- 负载均衡：auxiliary-loss-free 策略，靠可学习 bias 动态调节专家路由，避免辅助损失损害性能。
- 训练目标：Multi-Token Prediction (MTP)，每步预测多个未来 token，可用于推理加速（投机解码）。
- 预训练数据：14.8T tokens；上下文 128K（两阶段扩展 4K→32K→128K）。
- Infra/精度：FP8 混合精度训练框架（细粒度量化）；DualPipe 流水并行 + 高效跨节点 all-to-all 通信，重叠计算-通信。
- 训练算力：预训练 2.664M H800 小时 + 上下文扩展/后训练共约 2.788M H800 小时，约 557.6 万美元（按 $2/GPU·h）。
- 后训练：从 DeepSeek-R1 系列蒸馏推理能力 + SFT + RL（GRPO）。

## 原始链接
- url: https://arxiv.org/abs/2412.19437
- pdf_url: https://arxiv.org/pdf/2412.19437
- github_url: https://github.com/deepseek-ai/DeepSeek-V3

## 本地落盘文件
- ../../../sources/llm/2025/deepseek-v3.pdf
