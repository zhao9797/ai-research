---
title: "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity"
org: Google
country: US
date: 2021-01
type: paper
categories: [架构, AI infra]
url: https://arxiv.org/abs/2101.03961
pdf_url: https://arxiv.org/pdf/2101.03961
github_url: https://github.com/google-research/t5x
downloaded: [switch-transformer.pdf]
---

## 一句话定位
Switch Transformer 把 MoE 路由简化为 top-1（每 token 只选 1 个专家），稳定训练到 1.6 万亿参数，并提出选择性精度等技巧让稀疏模型训练 7 倍提速。

## 摘要（3-6 句）
论文主张把 MoE 的 top-2 路由简化成 top-1（Switch routing），降低路由计算、通信和复杂度，同时通过容量因子、选择性 bfloat16 精度、专家 dropout 等技巧稳定训练。在相同算力下，Switch-Base 比 T5-Base 预训练快约 7 倍。作者把模型扩展到 1.6 万亿参数（Switch-C），并展示稀疏专家模型在多任务、多语言上的优势，还给出向稠密模型蒸馏的方法。

## 关键技术细节
- 路由：top-1（Switch）路由，每 token 只送 1 个专家，简化 GShard 的 top-2。
- 规模：最大 Switch-C 达 1.6T 参数；展示了在固定算力下相对 T5 约 7× 的预训练加速。
- 稳定性技巧：capacity factor、选择性 bf16（路由器用 fp32）、专家初始化缩放、expert dropout。
- load balancing：可微分的辅助负载均衡损失，鼓励均匀路由。
- 蒸馏：把稀疏大模型蒸馏回稠密小模型，保留约 30% 的质量增益。

## 原始链接
- url: https://arxiv.org/abs/2101.03961
- pdf_url: https://arxiv.org/pdf/2101.03961
- github_url: https://github.com/google-research/t5x

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/switch-transformer.pdf
