---
title: "DeepSpeed-MoE: Advancing Mixture-of-Experts Inference and Training to Power Next-Generation AI Scale"
org: Microsoft (DeepSpeed)
country: US
date: 2022-01
type: paper
categories: [AI infra]
url: https://arxiv.org/abs/2201.05596
pdf_url: https://arxiv.org/pdf/2201.05596
github_url: https://github.com/deepspeedai/DeepSpeed
downloaded: [deepspeed-moe-2201.05596.pdf]
---

## 一句话定位
DeepSpeed 的端到端 MoE 训练+推理方案：新 MoE 架构（PR-MoE）+ 模型压缩（MoS）把模型缩小最高 3.7×，配高度优化的推理系统，让超大 MoE 既省训练又能低延迟低成本服务。

## 摘要（3-6 句）
当 dense 巨模型逼近硬件极限，MoE 因「同等质量下训练成本远低于 dense」成为最有前景的架构之一——本工作在自回归语言模型上展示约 5× 训练成本节省。但 MoE 模型更大、架构特殊，快速推理一直是难题，限制了实用性。DeepSpeed-MoE 作为 DeepSpeed 库的一部分，提出新 MoE 架构设计与模型压缩技术，把 MoE 模型尺寸最高缩小 3.7×，并以高度优化的推理系统相比现有 MoE 推理方案带来 7.3× 更优的延迟与成本。相比同等质量的 dense 模型，DeepSpeed-MoE 推理最高快 4.5×、便宜 9×，为「从 dense 转向稀疏 MoE」开辟了路径。论文发表于 ICML 2022。

## 关键技术细节
- 训练成本：自回归语言模型上 MoE 相比同质量 dense 约 5× 训练成本节省。
- 架构创新 PR-MoE（Pyramid-Residual MoE，金字塔-残差 MoE）：不同层用不同专家数（金字塔式，靠后层更多专家），并以「残差」方式让每 token 固定走一个 dense MLP + 一个被门控的专家，从而在更少参数下保持质量。
- 压缩 MoS（Mixture-of-Students）：对 PR-MoE 做知识蒸馏得到学生模型，配合架构改造把 MoE 模型尺寸最高缩小 3.7×。
- 推理系统：相比现有 MoE 推理方案 7.3× 更好的延迟与成本；相比同质量 dense 推理最高快 4.5×、便宜 9×。系统结合专家并行（EP）+ 张量并行 + 数据并行等多维并行与通信优化服务大规模 MoE。
- 工程并行组合（DeepSpeed MoE 训练支持）：E（专家）/ E+D（专家+数据）/ E+Z（专家+ZeRO 数据并行，切分非专家参数）/ E+D+M（再加模型并行支持超大 hidden）/ E+D+Z 等组合，应对不同基座规模。

## 原始链接
- url: https://arxiv.org/abs/2201.05596
- pdf_url: https://arxiv.org/pdf/2201.05596
- github_url: https://github.com/deepspeedai/DeepSpeed
- 会议版: https://proceedings.mlr.press/v162/rajbhandari22a （ICML 2022）

## 一手源存档（sources/）
- [deepspeed-moe-2201.05596.pdf](https://arxiv.org/pdf/2201.05596)  （arXiv 原文 PDF，不入 git）
