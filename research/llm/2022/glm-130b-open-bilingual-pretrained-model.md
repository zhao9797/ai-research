---
title: "GLM-130B: An Open Bilingual Pre-trained Model"
org: 清华大学 / 智谱 (Tsinghua KEG & Zhipu)
country: China
date: 2022-10
type: paper
categories: [预训练数据, 架构, AI infra]
url: https://arxiv.org/abs/2210.02414
pdf_url: https://arxiv.org/pdf/2210.02414
github_url: https://github.com/THUDM/GLM-130B
downloaded: [glm-130b.pdf]
---

## 一句话定位
清华/智谱开源的 1300 亿双语（中英）模型，基于 GLM 自回归填空目标，首个实现无训练后 INT4 量化、可在 4×RTX 3090 上推理的百亿级模型。

## 摘要
GLM-130B 是 1300 亿参数的中英双语预训练模型，目标是开源一个不低于 GPT-3 davinci 的 100B 级模型，并揭示如何成功训练。论文详述训练过程、设计选择、效率与稳定性策略，以及应对 loss 尖峰/发散的工程经验。GLM-130B 在英文基准上显著超越 GPT-3 175B（davinci），在中文基准上显著超越 ERNIE TITAN 3.0 260B。利用其独特缩放性质实现无训练后 INT4 量化，几乎无性能损失，可在 4×RTX 3090(24G) 或 8×RTX 2080 Ti(11G) 上推理。

## 关键技术细节
- 架构：基于 GLM（通用语言模型，自回归空白填充目标），非纯 GPT 式；70 层，隐藏维度 12288，150 亿参数 → 实为 130B；多目标统一。
- 关键设计：DeepNorm 稳定深层训练、旋转位置编码（RoPE）、GeLU；后归一化（Post-LN）+ DeepNorm。
- 训练数据：4000 亿（400B）token，中英各约一半（中文 200B + 英文 200B）。
- Infra：96 块 NVIDIA DGX-A100（8×40G）节点，共 768 块 A100；4-way 张量并行 + 8-way 流水并行；训练 60 天。
- 稳定性：使用 embedding gradient shrink、混合精度（FP16）应对 loss 尖峰；公开训练日志。
- 量化：独有的 INT4 无训练后量化（权重量化到 4-bit），几乎无损，大幅降低推理门槛。
- 开放：权重、代码、训练日志、数据处理工具公开。

## 原始链接
- url: https://arxiv.org/abs/2210.02414
- pdf_url: https://arxiv.org/pdf/2210.02414
- github_url: https://github.com/THUDM/GLM-130B

## 本地落盘文件
- ../../../sources/llm/2022/glm-130b.pdf
