---
title: "RWKV: Reinventing RNNs for the Transformer Era"
org: EleutherAI / Generative AI Commons (RWKV community)
country: US/other
date: 2023-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2305.13048
pdf_url: https://arxiv.org/pdf/2305.13048
github_url: https://github.com/BlinkDL/RWKV-LM
downloaded: [rwkv.pdf]
---

## 一句话定位
RWKV 把 RNN 与 Transformer 融合：训练时可像 Transformer 一样并行，推理时像 RNN 一样 O(1)/step，是早期最成功的非注意力大模型之一（验证到 14B）。

## 摘要（3-6 句）
Transformer 注意力随序列二次增长，RNN 推理高效但难并行训练。RWKV（Receptance Weighted Key Value）设计了一种线性注意力式的机制，使模型既能在训练时并行化（类 Transformer），又能在推理时以常数显存、线性时间逐 token 递归（类 RNN）。论文把 RWKV 扩展到 14B 参数（当时最大的纯 RNN 类 LLM），性能与同规模 Transformer 相当。

## 关键技术细节
- 核心：用 R（receptance）、W（time-decay 权重）、K、V 构造线性可递归的 token-mixing 与 channel-mixing；time-decay 提供类位置衰减。
- 双形态：训练用并行/卷积式公式；推理用递归式公式，显存与时间随长度线性、每步 O(1)。
- 规模：验证到 14B 参数，是当时最大的 RNN 类语言模型。
- 由社区（Bo Peng / BlinkDL 主导）+ EleutherAI 合作，后续迭代到 RWKV-5/6（Eagle/Finch）等。

## 原始链接
- url: https://arxiv.org/abs/2305.13048
- pdf_url: https://arxiv.org/pdf/2305.13048
- github_url: https://github.com/BlinkDL/RWKV-LM

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/rwkv.pdf
