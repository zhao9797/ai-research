---
title: On-Policy Distillation
org: Thinking Machines Lab
country: US
date: 2025-10
type: blog
categories: [后训练]
url: https://thinkingmachines.ai/blog/on-policy-distillation/
downloaded: [thinkingmachines-on-policy-distillation.html]
---

## 一句话定位
Thinking Machines Lab 官方博客：系统阐述 on-policy distillation——在学生自己采样的轨迹上用教师逐 token 打分（reverse KL）做蒸馏，兼具 RL 的 on-policy 相关性与蒸馏的密集奖励。

## 摘要（3-6 句）
博客把后训练方法分为 on-policy（如 RL，从自己采样学习，但奖励稀疏）与 off-policy（如 SFT/标准蒸馏，密集监督但训练分布与自身不符）两类，指出 on-policy distillation 取两者之长：让学生模型自己采样轨迹，再用教师模型对学生每个 token 的分布做评分（最小化 reverse KL），得到密集的、与学生自身分布对齐的监督信号。相比 RL 的稀疏 0/1 奖励，它每步都有信息；相比离线蒸馏，它不受分布漂移困扰。文中给出数学推理、领域个性化（personalization）等实证：on-policy distillation 在远低于 RL 的算力下达到相近或更好的效果，并能在持续学习中缓解灾难性遗忘。

## 关键技术细节
- 定义：学生采样轨迹（on-policy）→ 教师对学生每个 token 的概率分布打分 → 最小化逐 token 的 reverse KL(student‖teacher)。
- 与 RL 对比：RL 奖励稀疏（整条轨迹一个标量），on-policy distillation 每 token 都有密集监督，样本效率高得多。
- 与 off-policy 蒸馏对比：标准蒸馏在教师轨迹上学，存在 train/inference 分布不匹配；on-policy 在学生自身分布上学，消除该 gap。
- reverse KL：选择 reverse KL 使学生"mode-seeking"，避免覆盖教师全部模式带来的不一致。
- 实证：数学推理（如蒸 Qwen 系列）用约 1/10 RL 算力达到相近性能；个性化/持续学习中保留通用能力、减少遗忘。
- 配套 Thinking Machines 的 Tinker 训练 API。

## 原始链接
- url: https://thinkingmachines.ai/blog/on-policy-distillation/

## 一手源存档（sources/）
- [thinkingmachines-on-policy-distillation.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/post-training/thinkingmachines-on-policy-distillation.html)
