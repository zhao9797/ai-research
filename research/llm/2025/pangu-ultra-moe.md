---
title: Pangu Ultra MoE - How to Train Your Big MoE on Ascend NPUs
org: 华为 (Huawei) 盘古
country: China
date: 2025-05
type: paper
categories: [架构, AI infra, 后训练]
url: https://arxiv.org/abs/2505.04519
pdf_url: https://arxiv.org/pdf/2505.04519
github_url:
downloaded: [pangu-ultra-moe.pdf]
---

## 一句话定位
华为 718B 稀疏 MoE（每 token 激活 39B），全程在昇腾 NPU 上训练；用仿真驱动选型 + 5D 并行 + Hierarchical EP All-to-All 把训练 MFU 做到 30.0%、吞吐 1.46M tokens/s（6K 昇腾 NPU），性能与 DeepSeek-R1 相当。arXiv 2505.04519，发布 2025-05-07。

## 摘要
论文目标是在昇腾 NPU 上找出训练接近万亿参数稀疏 MoE 的"配方"。两条主线：模型架构设计 + 系统优化。架构上用仿真（先在昇腾上验证单算子，再自底向上预测端到端吞吐/MFU）来比较各种超参 trade-off，免去昂贵的反复真机实验，据此得到 718B 的 Pangu Ultra MoE。系统上深挖 Expert Parallelism，提出 Hierarchical EP All-to-All（分离节点间 Allgather 与节点内 All-to-All）+ Adaptive Pipe Overlap（细粒度计算-通信重叠）+ tensor swapping 显存优化 + 动态设备级负载均衡（实时预测专家负载并自适应放置）。最终在 6K 昇腾 NPU 上达到 MFU 30.0%、TPS 1.46M，性能比肩 DeepSeek-R1。

## 关键技术细节
- 规模：718B 总参 / 每 token 激活 39B（论文 Table 6 对比：DeepSeek-V3/R1 为 671B/37B，MiniMax-Text-01 为 456B/46B）。
- 注意力：MLA（Multi-Head Latent Attention）；论文指出 MLA 在昇腾上比 GQA 更贴近 roofline。
- MoE：256 路由专家（消融显示 256 优于 64/128，512 收益递减）+ 1 共享专家；每 token topk=8（含共享专家结构）；专家中间维 2048（细粒度小专家、高稀疏率）。
- 层数/维度：最终选 61 层（model 7，比 66 层吞吐高约 15%）、hidden size 7680；含 MTP（Multi-Token Prediction）层，使总层数从 61 增至约 64。
- 并行：5D 并行 = PP（含 VPP）+ TP + EP + DP + CP；实际训练采用 TP=8、PP=16、VPP=2、EP=4、MBS=2；TP×EP=32 通信组，配 TP-extend-EP 与 hierarchical EP All-to-All。
- 负载均衡：对比 auxiliary loss 策略，α=1e-2 更好控负载；718B Dropless vs Drop-and-Pad，drop rate 约 8%（20B baseline 为 6%）；大模型比小模型更易丢 token。
- 效率：训练 MFU 30.0%、TPS 1.46M（6K 昇腾 NPU），相对 baseline MFU 显著提升。
- 成绩：与 DeepSeek-R1 相当——MMLU 91.5、MMLU-Pro 83.5、AIME2024 81.3、AIME2025 70.0、GPQA-Diamond 75.3、MATH500 97.4；行业评测 MedQA 87.1 略超 R1。

## 原始链接
- url: https://arxiv.org/abs/2505.04519
- pdf_url: https://arxiv.org/pdf/2505.04519

## 本地落盘文件
- ../../../sources/llm/2025/pangu-ultra-moe.pdf
