---
title: Improved Baselines with Visual Instruction Tuning (LLaVA-1.5)
org: Microsoft Research / University of Wisconsin-Madison
country: US
date: 2023-10
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2310.03744
pdf_url: https://arxiv.org/pdf/2310.03744
github_url: https://github.com/haotian-liu/LLaVA
downloaded: [llava-1-5.pdf]
---

## 一句话定位
LLaVA-1.5：简单的 MLP 连接器 + 学术 VQA 数据，单 8-A100 节点一天训出 11 项 SOTA 的开源多模态模型。

## 摘要
对视觉指令微调下的多模态大模型(LMM)设计做首个系统研究(LLaVA 框架)。发现 LLaVA 的全连接视觉-语言连接器出乎意料地强且数据高效。简单改动——用 CLIP-ViT-L-336px + MLP 投影、加入带响应格式提示的学术 VQA 数据——即建立更强 baseline，在 11 个基准达 SOTA。最终 13B checkpoint 仅用 1.2M 公开数据，单 8-A100 节点约 1 天训完。

## 关键技术细节
- 视觉编码器：CLIP-ViT-L-336px（更高分辨率）。
- 连接器：由线性层升级为两层 MLP 投影(关键改动)。
- 数据：加入学术 VQA(VQAv2/GQA/OKVQA 等) + 响应格式提示，共约 1.2M 公开数据。
- 底座 LLM：Vicuna-13B。
- 训练成本：单 8×A100 节点约 1 天。
- 结果：11 个 benchmark SOTA(开源 LMM)；数据高效。

## 原始链接
- url: https://arxiv.org/abs/2310.03744
- pdf_url: https://arxiv.org/pdf/2310.03744
- github_url: https://github.com/haotian-liu/LLaVA

## 一手源存档（sources/）
- llava-1-5.pdf  （PDF 不入 git，走 HF bucket）
