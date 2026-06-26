---
title: DeepSeek-V3 Technical Report
org: DeepSeek-AI
country: China
date: 2024-12
type: report
categories: [架构, AI infra, 后训练, 预训练数据]
url: https://arxiv.org/abs/2412.19437
pdf_url: https://arxiv.org/pdf/2412.19437
github_url: https://github.com/deepseek-ai/DeepSeek-V3
downloaded: [deepseek-v3.pdf]
---

## 一句话定位
DeepSeek-V3：671B MoE 基座（37B 激活），后训练阶段首次把 DeepSeek-R1 的长 CoT 推理能力蒸馏进通用模型，是"从推理模型蒸馏 → 通用模型"的一手范例；同时是 R1 的基座。

## 摘要（3-6 句）
DeepSeek-V3 是 6710 亿参数的 MoE 模型（每 token 激活 370 亿），用 14.8T tokens 预训练，训练总成本约 278.8 万 H800 GPU 小时。架构上沿用 MLA（多头潜在注意力）与 DeepSeekMoE，并首创无辅助损失的负载均衡（auxiliary-loss-free load balancing）与多 token 预测（MTP）训练目标；训练用 FP8 混合精度与 DualPipe 高效流水并行。后训练含 SFT 与 RL（GRPO），并把 DeepSeek-R1 系列的长链推理能力通过蒸馏注入 V3，使其在保持通用性的同时显著提升推理。V3 也是 DeepSeek-R1 的基座模型。

## 关键技术细节
- 架构：MoE 671B 总参 / 37B 激活；MLA（低秩 KV 压缩注意力）+ DeepSeekMoE（细粒度专家 + 共享专家）；MTP 多 token 预测。
- 负载均衡：auxiliary-loss-free 策略（用可学习偏置动态均衡），避免辅助损失损害性能。
- 预训练：14.8T tokens；FP8 混合精度训练；DualPipe 流水并行 + 跨节点 all-to-all 通信优化；上下文扩展到 128K。
- 算力：总训练约 278.8 万 H800 GPU·小时（≈557 万美元，按租用价）。
- 后训练：SFT + RL（GRPO）；关键是从 DeepSeek-R1 蒸馏长 CoT 推理（reasoning distillation）进 V3，提升数学/代码。
- 并行/精度：EP（专家并行）+ PP + DP（ZeRO-1）+ FP8。
- 开源：基座与 chat 权重。

## 原始链接
- url: https://arxiv.org/abs/2412.19437
- pdf_url: https://arxiv.org/pdf/2412.19437
- github_url: https://github.com/deepseek-ai/DeepSeek-V3

## 一手源存档（sources/）
- deepseek-v3.pdf  （PDF 不入 git，走 HF bucket）
