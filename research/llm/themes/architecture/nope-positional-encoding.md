---
title: "The Impact of Positional Encoding on Length Generalization in Transformers (NoPE)"
org: Mila / McGill University / IBM Research / ServiceNow Research
country: US/other
date: 2023-05
type: paper
categories: [架构]
url: https://arxiv.org/abs/2305.19466
pdf_url: https://arxiv.org/pdf/2305.19466
github_url: https://github.com/McGill-NLP/length-generalization
downloaded: [nope.pdf]
---

## 一句话定位
该研究系统对比五类位置编码对长度泛化的影响，意外发现 decoder-only Transformer「不用任何显式位置编码 (NoPE)」反而长度外推最好——NoPE 概念由此流行（被 Llama 4 iRoPE 等采用）。

## 摘要（3-6 句）
长度泛化（从短训练上下文泛化到长上下文）是 Transformer 的关键挑战，位置编码 (PE) 被认为是主因，但不同 PE 在下游任务外推上的确切影响不清楚。论文系统比较了 decoder-only Transformer 在五种位置编码（含 ALiBi、RoPE、T5 相对偏置、绝对位置、以及 NoPE 无显式 PE）下的长度泛化。结果发现：在这些推理类任务上，常用的显式 PE 并不利于长度外推，而完全不加位置编码 (NoPE) 反而泛化最好；论文进一步分析 NoPE 的因果注意力如何隐式学到位置信息。

## 关键技术细节
- 对比五种 PE：absolute、ALiBi、RoPE、T5's relative bias、NoPE（无显式位置编码）。
- 关键发现：在合成推理任务上，NoPE 的长度泛化最佳；显式 PE 反而拖累外推。
- 理论：证明因果（causal）注意力 + 自回归本身能隐式编码绝对位置，故 NoPE 仍可用。
- 影响：NoPE 思想被后续长上下文架构借鉴（如 Llama 4 iRoPE 在部分层用 NoPE）。
- 作者：Amirhossein Kazemnejad、Siva Reddy 等。

## 原始链接
- url: https://arxiv.org/abs/2305.19466
- pdf_url: https://arxiv.org/pdf/2305.19466
- github_url: https://github.com/McGill-NLP/length-generalization

## 一手源存档（sources/）
- nope.pdf  （PDF 不入 git，走 HF bucket）
