---
title: Training Compute-Optimal Large Language Models (Chinchilla)
org: DeepMind
country: UK/US
date: 2022-03
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2203.15556
pdf_url: https://arxiv.org/pdf/2203.15556
github_url:
downloaded: [chinchilla.pdf]
---

## 一句话定位
提出"计算最优"缩放律：在给定算力预算下，模型参数量与训练 token 数应等比例缩放，证明当时主流大模型（GPT-3、Gopher）严重训练不足。

## 摘要
通过训练 400+ 个语言模型（70M 到 16B+ 参数，5B 到 500B token），DeepMind 发现：每当模型规模翻倍，训练数据量也应翻倍（即参数 N 与 token D 同幂指数缩放，约 N∝C^0.5、D∝C^0.5）。据此训练出 Chinchilla（70B 参数、1.4T token），与 Gopher 用相同算力但 4 倍数据。Chinchilla 在大量下游任务上全面显著超越 Gopher(280B)、GPT-3(175B)、Jurassic-1(178B)、MT-NLG(530B)。MMLU 平均准确率 67.5%，比 Gopher 提升 7%+。

## 关键技术细节
- 计算最优定律：对给定 FLOPs C，最优模型大小 N_opt 与最优 token 数 D_opt 大致随 C 的相同幂次（约 0.5）缩放；"每翻倍模型规模，数据也翻倍"。
- 三种估计方法（固定模型大小变数据、IsoFLOP 曲线、参数化损失拟合）一致得出该结论。
- Chinchilla：70B 参数，训练 1.4 万亿（1.4T）token，与 Gopher（280B）算力相同。
- Chinchilla 推理/微调成本远低于 Gopher，因参数仅 1/4。
- 训练超过 400 个模型，规模 70M–16B，token 5B–500B。
- MMLU：Chinchilla 67.5%（SOTA），较 Gopher 提升 >7%。
- 影响：颠覆 Kaplan(2020) 的"参数优先"缩放观，开启"数据是瓶颈"的认知，奠定后续 LLaMA 等"小模型多数据"路线。

## 原始链接
- url: https://arxiv.org/abs/2203.15556
- pdf_url: https://arxiv.org/pdf/2203.15556

## 一手源存档（sources/）
- chinchilla.pdf  （PDF 不入 git，走 HF bucket）
