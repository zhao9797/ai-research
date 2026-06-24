---
title: "Jamba-1.5: Hybrid Transformer-Mamba Models at Scale"
org: AI21 Labs
country: other
date: 2024-08
type: report
categories: [架构, AI infra]
url: https://arxiv.org/abs/2408.12570
pdf_url: https://arxiv.org/pdf/2408.12570
github_url: https://huggingface.co/ai21labs/AI21-Jamba-1.5-Large
downloaded: [jamba-1.5.pdf]
---

## 一句话定位
Jamba-1.5 把 Transformer-Mamba 混合 MoE 架构 scale 到 398B 总参/94B 激活（Large），256K 有效上下文，提出 ExpertsInt8 量化让 Large 跑在单机 8×80GB。

## 摘要（3-6 句）
Jamba-1.5 是基于 Jamba 混合架构的指令微调模型：Transformer-Mamba MoE 混合，跨上下文长度高吞吐、低显存，同时质量不输纯 Transformer。两档：Jamba-1.5-Large（94B 激活）与 Jamba-1.5-Mini（12B 激活），都微调用于对话与指令，有效上下文 256K（开源权重中最长）。为低成本推理，作者提出 ExpertsInt8 量化，使 Large 能在 8×80GB GPU 上处理 256K 上下文而不掉质量。在学术与聊天基准上表现优异、吞吐高、长上下文超过其他开放权重模型。

## 关键技术细节
- 架构：Jamba block 混合 Mamba 层 : 注意力层 ≈ 7:1，周期性插 MoE 层。
- 规模：Jamba-1.5-Large 总参 398B / 激活 94B；Jamba-1.5-Mini 总参 52B / 激活 12B。
- 上下文：256K 有效上下文，长上下文吞吐显著高于同规模 Transformer。
- ExpertsInt8：把 MoE 专家与 MLP 权重存为 INT8、计算时反量化为 BF16 的量化方案，无质量损失，Large 可在 8×80GB 上服务 256K。
- 开放权重（Jamba Open Model License）。

## 原始链接
- url: https://arxiv.org/abs/2408.12570
- pdf_url: https://arxiv.org/pdf/2408.12570
- github_url: https://huggingface.co/ai21labs/AI21-Jamba-1.5-Large

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/jamba-1.5.pdf
