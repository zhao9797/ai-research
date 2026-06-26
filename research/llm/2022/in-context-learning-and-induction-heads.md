---
title: In-context Learning and Induction Heads
org: Anthropic
country: US
date: 2022-09
type: paper
categories: [架构]
url: https://arxiv.org/abs/2209.11895
pdf_url: https://arxiv.org/pdf/2209.11895
github_url:
downloaded: [induction-heads.pdf]
---

## 一句话定位
Anthropic 机制可解释性代表作：提出"归纳头"（induction heads）可能是 Transformer 大部分 in-context learning 的机制来源。

## 摘要
"归纳头"是实现简单算法 [A][B]…[A]→[B] 的注意力头。本文给出初步、间接的证据，论证归纳头可能构成大 Transformer 中绝大多数"in-context learning"（随 token 位置增加而损失下降）的机制。发现归纳头恰好在 in-context learning 能力骤升的同一时刻形成——表现为训练损失曲线上的一个"凸起"。提供六条互补证据，论证归纳头可能是任意规模 Transformer 通用 in-context learning 的机制源头：对小的纯注意力模型给出强因果证据；对带 MLP 的大模型给出相关性证据。

## 关键技术细节
- 归纳头：跨两层注意力组合（previous-token head + induction head）实现前缀匹配与复制的"模式补全"算法。
- 关键观察：训练中存在一个"phase change"——归纳头形成的窗口与 in-context learning 能力突增、训练损失出现 bump 同时发生。
- 六条证据链：从纯注意力小模型（强因果，可消融）到大模型（相关性）。
- 机制可解释性（mechanistic interpretability）里程碑，把"涌现能力"部分归因到具体电路。
- 后续影响 circuits / interpretability 研究主线。

## 原始链接
- url: https://arxiv.org/abs/2209.11895
- pdf_url: https://arxiv.org/pdf/2209.11895

## 一手源存档（sources/）
- induction-heads.pdf  （PDF 不入 git，走 HF bucket）
