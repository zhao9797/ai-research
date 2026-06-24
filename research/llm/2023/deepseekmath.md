---
title: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models"
org: 深度求索（DeepSeek-AI）
country: China
date: 2024-02
type: paper
categories: [后训练, 预训练数据, agentic训练]
url: https://arxiv.org/abs/2402.03300
pdf_url: https://arxiv.org/pdf/2402.03300
github_url: https://github.com/deepseek-ai/DeepSeek-Math
downloaded: [deepseekmath.pdf]
---

## 一句话定位
DeepSeekMath 7B 首次让开源模型在竞赛级 MATH 突破 50%，并首次提出 GRPO（Group Relative Policy Optimization）——后来 DeepSeek-R1 等推理模型的核心 RL 算法，是中国后训练/RL 最具影响力的一手论文。（2024-02 发布，承接 2023 DeepSeek-Coder 工作。）

## 摘要（3-6 句）
DeepSeekMath 7B 在 DeepSeek-Coder-Base-v1.5 7B 上继续预训练 120B 数学相关 token（取自 Common Crawl）+ 自然语言与代码数据，在不借助外部工具与投票的情况下于竞赛级 MATH 取得 51.7%，64 样本自洽达 60.9%，接近 Gemini-Ultra 与 GPT-4。论文提出 GRPO（PPO 的变体），去掉 critic/价值模型、用同组样本的平均奖励作 baseline，大幅降低 RL 训练资源，并将 GSM8K 46.8%→51.7%（MATH）等指标显著提升。

## 关键技术细节
- 数据：DeepSeekMath Corpus = 120B 数学 token；用 fastText 分类器从去重后 Common Crawl（40B HTML 页）迭代召回，迭代得 35.5M 数学网页；最终训练混合 = 56% DeepSeekMath Corpus + 4% AlgebraicStack + 10% arXiv + 20% Github 代码 + 10% CC 自然语言。
- 基座：从 DeepSeek-Coder-Base-v1.5 7B 继续训练 500B token。
- 性能：MATH 51.7%（Top1，无工具/无投票）、64 样本自洽 60.9%；GSM8K 88.2%（RL 后）；超越所有 7B–70B 开源模型及多数闭源模型。
- GRPO（核心贡献）：
  - PPO 的高效变体，去掉与策略模型等大的价值函数（critic），改用同一问题采样的一组输出（G 个）的平均奖励作 baseline，显著省显存/算力。
  - 优势估计：Â_{i,t} =（r_i − mean(r)）/ std(r)（outcome supervision）；亦支持 process supervision（按步给奖励，token 优势 = 后续步归一化奖励之和）。
  - KL 正则直接加到 loss（而非奖励里），KL 系数 0.04。
  - 支持 iterative RL：用策略模型采样结果持续更新奖励模型（10% 历史回放）。
  - RL 超参：policy LR 1e-6、reward model LR 2e-5、每问题采样 64 输出、max len 1024、batch 1024、144K 个 GSM8K/MATH CoT 问题。
- 统一范式：把 SFT/RFT/Online-RFT/DPO/PPO/GRPO 统一为"直接或简化 RL"，分析 online vs offline、outcome vs process、单轮 vs 迭代 RL；发现 RL 主要提升 Maj@K 而非 Pass@K。

## 原始链接
- url: https://arxiv.org/abs/2402.03300
- pdf_url: https://arxiv.org/pdf/2402.03300
- github_url: https://github.com/deepseek-ai/DeepSeek-Math

## 本地落盘文件
- ../../../sources/llm/2023/deepseekmath.pdf
