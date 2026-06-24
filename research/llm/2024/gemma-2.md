---
title: "Gemma 2: Improving Open Language Models at a Practical Size"
org: Google DeepMind
country: US
date: 2024-07
type: report
categories: [架构, 后训练]
url: https://arxiv.org/abs/2408.00118
pdf_url: https://arxiv.org/pdf/2408.00118
github_url:
downloaded: [2408.00118.pdf]
---

## 一句话定位
Gemma 2 技术报告：2B/9B/27B 开放模型，交错 local sliding window + global 注意力 + GQA + logit soft-capping；对 2B/9B 用知识蒸馏替代 next-token 预测，以小数据获大模型质量，同尺寸 SOTA 且能与 2–3× 大模型竞争。

## 摘要
Gemma 2 是 Gemma 系列新成员，规模 2B、9B、27B。对 Transformer 应用多项改进：交错的 local-global 注意力（每隔一层在 local sliding window 与 global attention 间切换）与分组查询注意力（GQA）。对 2B 与 9B 用知识蒸馏（大模型作 teacher）训练而非标准 next-token 预测，使其在远小于"compute-optimal"的 token 量上仍达到高质量。结果模型在同规模上最佳，甚至能与 2–3 倍大的模型竞争。全部模型开放发布。

## 关键技术细节
- 规模与配置（Table 1/2，列为 2B/9B/27B）：层数 26/42/46；d_model 2304/3584/4608；注意力头 8/16/32；KV 头 4/8/16；head size 256/256/128；非嵌入参数 2.02B/8.32B/26.05B（嵌入 0.59B/0.92B/1.18B）。
- 注意力：交错 local sliding window（4096）与 global attention（span 8192），每隔一层切换；GQA（num_groups=2）；context length 8192；RoPE。
- 稳定性：logit soft-capping —— self-attention 层 soft_cap=50.0，最终 logit 层 soft_cap=30.0；RMSNorm（pre + post norm，每个注意力/FFN 子层前后都加）。
- tokenizer：SentencePiece，词表 256,128（与 Gemma 1/Gemini 同）。
- 训练数据：27B 训 13T token、9B 训 8T、2B 训 2T（主要英文网页/代码/数学）。
- 知识蒸馏：2B 与 9B 用大模型 teacher 蒸馏（替代 next-token 预测），训练 token 量远超 compute-optimal（>50× Chinchilla 量级）。
- 算力：27B 用 TPUv5p（6144 芯片，data replica 768、model shard 8）；9B/2B 用 TPUv5e。
- 后训练：SFT + RLHF + model merging（WARP）。
- 表现：同尺寸 SOTA，可与 2–3× 规模模型竞争。

## 原始链接
- url: https://arxiv.org/abs/2408.00118
- pdf_url: https://arxiv.org/pdf/2408.00118

## 本地落盘文件
- ../../../sources/llm/2024/2408.00118.pdf
