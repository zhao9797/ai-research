---
title: "DeepNet: Scaling Transformers to 1,000 Layers (DeepNorm)"
org: Microsoft Research
country: US
date: 2022-03
type: paper
categories: [架构]
url: https://arxiv.org/abs/2203.00555
pdf_url: https://arxiv.org/pdf/2203.00555
github_url: https://github.com/microsoft/torchscale
downloaded: [deepnet.pdf]
---

## 一句话定位
提出 DeepNorm 归一化与配套初始化，稳定训练极深 Transformer，首次把 Transformer 扩展到 1000 层。

## 摘要
提出简单有效的方法稳定极深 Transformer：引入新归一化函数 DeepNorm 修改残差连接，并配合理论推导的初始化。理论分析表明模型更新可被稳定地界定。该方法兼具 Post-LN 的好性能与 Pre-LN 的训练稳定。成功将 Transformer 扩展到 1,000 层（2,500 个注意力与 FFN 子层），比此前深一个数量级。在含 7,482 个翻译方向的多语言基准上，200 层 3.2B 模型显著超越 48 层 12B SOTA 模型 5 个 BLEU，指出有前景的"深度"缩放方向。

## 关键技术细节
- DeepNorm：在残差连接中对子层输出乘以常数 α 放大、对初始化按 β 缩小（α、β 随层数 N 解析给定），界定模型更新幅度。
- 结合 Post-LN 性能与 Pre-LN 稳定性。
- 扩展到 1000 层（2500 子层），训练无发散。
- 多语言翻译（7482 方向）：200 层/3.2B 超过 48 层/12B 达 +5 BLEU，证明深而瘦优于浅而宽。
- 被 GLM-130B 等后续大模型采用以稳定训练；并入微软 TorchScale 库。

## 原始链接
- url: https://arxiv.org/abs/2203.00555
- pdf_url: https://arxiv.org/pdf/2203.00555
- github_url: https://github.com/microsoft/torchscale

## 一手源存档（sources/）
- deepnet.pdf  （PDF 不入 git，走 HF bucket）
