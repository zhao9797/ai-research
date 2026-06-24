---
title: "openPangu-Ultra-MoE-718B (开源盘古 Ultra-MoE-718B)"
org: 华为盘古 Huawei Pangu (昇腾 Ascend)
country: China
date: 2026-04
type: model-card
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://huggingface.co/openpangu/openPangu-Ultra-MoE-718B-model
pdf_url: ""
github_url: https://ai.gitcode.com/ascend-tribe
downloaded: [openpangu-ultra-moe-718b-modelcard.md]
---

## 一句话定位
华为盘古旗舰开源 MoE 大模型 openPangu-Ultra-MoE-718B，718B 总参 / 39B 激活，基于昇腾 NPU 从零训练约 19T tokens，MLA + MTP + 大稀疏比，具备快慢思考融合能力。

## 摘要
openPangu-Ultra-MoE-718B（HuggingFace openpangu 官方组织，createdAt 2026-04-08）是华为基于昇腾（Ascend）NPU 从零训练的大规模 MoE 语言模型，总参 718B、激活 39B，训练约 19T tokens，具备快慢思考融合能力。架构采用业界主流的 Multi-head Latent Attention (MLA)、Multi-Token Prediction (MTP)、大稀疏比，并含两项特有设计：Depth-Scaled Sandwich-Norm + TinyInit（调整层归一化结构与参数初始化提升训练稳定性）、基于 EP-Group 的负载均衡策略（优化负载均衡损失改善专家特化）。推理在 Atlas 800T A2（64GB，≥32 卡）上以 Tensor Parallel + 昇腾 NPU 融合大算子、bfloat16、4 机 32 卡运行（vllm_ascend）。采用 OPENPANGU MODEL LICENSE AGREEMENT v1.0。同系列还有 openPangu-R-72B-2512、openPangu-Embedded-7B/1B、openPangu-7B-Diffusion、openPangu-VL-7B 等。

## 关键技术细节
- **规格**：718B 总参 / 39B 激活（MoE，大稀疏比）。
- **训练数据**：约 19T tokens；昇腾 NPU 从零训练（from scratch）。
- **能力**：快慢思考融合（默认慢思考；输入结尾加 ` /no_think` 标记切快思考）。
- **架构**：MLA（Multi-head Latent Attention）+ MTP（Multi-Token Prediction）+ 大稀疏比。
- **稳定性设计-Depth-Scaled Sandwich-Norm + TinyInit**：调整 LayerNorm 结构与参数初始化提升训练稳定性。
- **MoE 负载均衡-EP-Group**：基于 EP-Group 的负载均衡策略，优化负载均衡损失，改善专家特化。
- **AI infra/精度/并行**：Atlas 800T A2（64GB，≥32 卡）；Tensor Parallel + 昇腾 NPU 融合大算子；bfloat16；4 机 32 卡推理（vllm_ascend）；权重需提前切分。
- **许可**：OPENPANGU MODEL LICENSE AGREEMENT VERSION 1.0。
- **系列**：openPangu-R-72B-2512、openPangu-Embedded-7B-DeepDiver、openPangu-7B-Diffusion-Base、openPangu-VL-7B 等（HF openpangu 官方组织，2026-04）。

## 原始链接
- url: https://huggingface.co/openpangu/openPangu-Ultra-MoE-718B-model
- 联系: openPangu@huawei.com

## 本地落盘文件
- ../../../sources/llm/2026/openpangu-ultra-moe-718b-modelcard.md
