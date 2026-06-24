---
title: "RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn Reinforcement Learning"
org: "西北大学 / 斯坦福 / 微软 / 新加坡国立 等"
country: US
date: 2025-04
type: paper
categories: [后训练, agentic训练, AI infra]
url: https://arxiv.org/abs/2504.20073
pdf_url: https://arxiv.org/pdf/2504.20073
github_url: https://github.com/RAGEN-AI/RAGEN
downloaded: [ragen-2504.20073.pdf]
---

## 一句话定位
系统研究"多轮 agent RL"为何不稳：提出轨迹级 RL 框架 StarPO 与稳定化变体 StarPO-S，诊断出"Echo Trap"奖励崩塌，并给出训练稳定/推理涌现的可行配方。

## 摘要
把 LLM 训练成交互式 agent 面临长程决策与随机环境反馈等挑战；虽然 RL 已在静态任务取得进展，多轮 agent RL 训练仍未充分探索。RAGEN 提出 StarPO(State-Thinking-Actions-Reward Policy Optimization)——一个轨迹级 agent RL 通用框架，并给出模块化训练/评测系统 RAGEN。在四个风格化环境的研究得出三点核心发现：① agent RL 训练存在反复出现的"Echo Trap"——奖励方差骤降、梯度尖峰；用 StarPO-S(轨迹过滤、引入 critic、梯度稳定化)缓解。② rollout 的塑形受益于多样初始状态、中等交互粒度、更频繁采样。③ 没有细粒度、推理感知的奖励信号，多轮 RL 难以涌现真正推理，易出现浅层策略或幻觉思考。

## 关键技术细节
- 框架 StarPO：以"状态-思考-动作-奖励"为单位做轨迹级策略优化(trajectory-level RL)，兼容 PPO/GRPO 类更新。
- 诊断 Echo Trap：多轮 RL 中模型陷入自我重复、奖励方差崩塌、梯度爆炸的不稳定模式。
- StarPO-S 稳定化三招：基于不确定性的轨迹过滤、引入 critic(value baseline)、梯度稳定化(裁剪/KL)。
- rollout 配方：多样初始状态 + 中等交互粒度(每轮动作数适中) + 更高采样频率，利于稳定与泛化。
- 结论：奖励须细粒度且推理感知，否则"思考"不会真正涌现(出现幻觉式 reasoning)。
- 系统 RAGEN：模块化 agent RL 训练/评测基础设施，开源。

## 原始链接
- url: https://arxiv.org/abs/2504.20073
- pdf_url: https://arxiv.org/pdf/2504.20073
- github_url: https://github.com/RAGEN-AI/RAGEN

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/ragen-2504.20073.pdf
