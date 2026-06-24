---
title: DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models (GRPO)
org: DeepSeek-AI
country: China
date: 2024-02
type: paper
categories: [后训练, 预训练数据]
url: https://arxiv.org/abs/2402.03300
pdf_url: https://arxiv.org/pdf/2402.03300
github_url: https://github.com/deepseek-ai/DeepSeek-Math
downloaded: [deepseekmath-grpo.pdf]
---

## 一句话定位
GRPO（Group Relative Policy Optimization）的提出论文：用同一 prompt 的一组采样的组内相对奖励替代 critic，省去价值网络，是 DeepSeek-R1 等 RLVR/reasoning RL 的核心算法。

## 摘要（3-6 句）
DeepSeekMath-7B 在 DeepSeek-Coder-Base-v1.5 7B 上继续预训练 120B 数学相关 token，在不借助外部工具与投票的情况下 MATH 基准达 51.7%（64 采样自一致性 60.9%），逼近 Gemini-Ultra 与 GPT-4。其数学能力源于两点：(1) 精心设计的 Common Crawl 数学数据筛选管线；(2) 提出 GRPO——PPO 的变体，去掉价值网络，用同一问题一组采样输出的相对奖励（组内归一化优势）来估计优势并更新策略，既提升推理又大幅降低 RL 显存。GRPO 后来成为 DeepSeek-R1、QwQ、众多开源 reasoning 模型的标准 RL 算法。

## 关键技术细节
- 基座/数据：DeepSeek-Coder-Base-v1.5 7B + 120B 数学 token（自建数学语料筛选管线，迭代式 fastText 召回 + 去污染）。
- GRPO：对每个问题采样一组 G 个输出，优势 Â_i = (r_i − mean(r))/std(r)（组内标准化），无需 critic；目标含 PPO 式裁剪 + 直接对策略加 KL 正则项。
- 显存：相比 PPO 省去与策略同规模的价值网络，大幅降低训练成本。
- 奖励：可用结果正确性（rule-based，数学答案可验证）或过程/RM 奖励。
- 结果：MATH 51.7%（无工具）、self-consistency@64 = 60.9%；GSM8K 等同步提升。
- 统一视角：论文给出 SFT/RFT/DPO/PPO/GRPO 的统一梯度形式分析。

## 原始链接
- url: https://arxiv.org/abs/2402.03300
- pdf_url: https://arxiv.org/pdf/2402.03300
- github_url: https://github.com/deepseek-ai/DeepSeek-Math

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/deepseekmath-grpo.pdf
