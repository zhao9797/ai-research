---
title: "WebRL: Training LLM Web Agents via Self-Evolving Online Curriculum Reinforcement Learning"
org: "清华大学 / 智谱 AI (THUDM / Zhipu)"
country: China
date: 2024-11
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2411.02337
pdf_url: https://arxiv.org/pdf/2411.02337
github_url: https://github.com/THUDM/WebRL
downloaded: [webrl-2411.02337.pdf]
---

## 一句话定位
清华/智谱用"自进化在线课程 RL"把开源模型训成强力网页 agent：从失败任务自动生成新任务 + 结果监督奖励模型，让 Llama-3.1-8B 在 WebArena-Lite 成功率从 4.8% 飙到 42.4%，超过 GPT-4-Turbo。

## 摘要
现有 LLM 网页 agent 严重依赖昂贵的闭源 API，而开源 LLM 决策能力不足。WebRL 是一个自进化的在线课程强化学习框架，用开源 LLM 训练高性能网页 agent。它解决三大挑战：训练任务稀缺、反馈信号稀疏、在线学习的策略分布漂移。具体方法：① 自进化课程——从失败的尝试中生成新任务；② 鲁棒的结果监督奖励模型(ORM)；③ 自适应 RL 策略保证持续改进。应用 WebRL 把开源 Llama-3.1 与 GLM-4 转化为高效网页 agent：在 WebArena-Lite 上，Llama-3.1-8B 成功率从 4.8% 提升到 42.4%，GLM-4-9B 从 6.1% 提升到 43%。这些开源模型显著超过 GPT-4-Turbo(17.6%) 与 GPT-4o(13.9%)，并优于此前基于开源 LLM 的 SOTA(AutoWebGLM 18.2%)。

## 关键技术细节
- 基座：Llama-3.1-8B、GLM-4-9B。
- 三组件：① 自进化课程(self-evolving curriculum)——用失败轨迹自动合成难度匹配的新任务，缓解任务稀缺；② 结果监督奖励模型(ORM)——判定任务是否完成，缓解稀疏反馈；③ 自适应 RL(基于 KL 约束的策略更新 + 经验回放)缓解分布漂移。
- 评测：WebArena-Lite。Llama-3.1-8B 4.8%→42.4%；GLM-4-9B 6.1%→43%。均超 GPT-4-Turbo(17.6%)、GPT-4o(13.9%)、AutoWebGLM(18.2%)。
- 是 AutoGLM 等智谱 GUI agent 产品背后的关键 RL 训练技术之一。

## 原始链接
- url: https://arxiv.org/abs/2411.02337
- pdf_url: https://arxiv.org/pdf/2411.02337
- github_url: https://github.com/THUDM/WebRL

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/webrl-2411.02337.pdf
