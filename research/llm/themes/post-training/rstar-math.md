---
title: "rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking"
org: Microsoft Research Asia
country: US
date: 2025-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2501.04519
pdf_url: https://arxiv.org/pdf/2501.04519
github_url: https://github.com/microsoft/rStar
downloaded: [rstar-math.pdf]
---

## 一句话定位
rStar-Math：用 MCTS + 代码增强 CoT + 过程偏好模型（PPM）做四轮自进化，让 1.5B/7B 小模型数学推理逼近甚至超过 o1。

## 摘要（3-6 句）
rStar-Math 让小语言模型通过"深度思考"自我进化获得强数学推理：用蒙特卡洛树搜索（MCTS）做带验证的推理，policy SLM 生成步骤，过程偏好模型 PPM 给步骤打分引导搜索。它提出三项创新：(1) 代码增强 CoT——每步生成 Python 代码并执行，只保留代码可运行且结果正确的步骤作为高质量训练数据；(2) PPM——用步骤的 Q 值偏好对训练过程奖励，避免人工或噪声标注；(3) 四轮自进化——策略模型与 PPM 互相迭代提升。结果：Qwen2.5-Math-7B 从 58.8% 提升到 90.0%（MATH），AIME 2024 解出约 53.3%（前 20% 选手水平），1.5B 模型也超过 o1-preview。

## 关键技术细节
- MCTS 推理：每个数学问题用 MCTS 展开多步解，节点为推理步骤，Q 值由 rollout 成功率估计。
- 代码增强 CoT：每步附 Python 代码并执行，过滤掉不能运行/结果错误的步骤，保证训练数据正确性（"verified reasoning trajectories"）。
- 过程偏好模型 PPM：用同一步的高 Q/低 Q 步骤构造偏好对训练，避免直接拟合带噪 Q 分数。
- 自进化：4 轮——用上一轮模型生成更高质量 MCTS 数据，重训 policy SLM 与 PPM。
- 结果：Qwen2.5-Math-7B MATH 90.0%、AIME 2024 ~53.3%（约 8/15）；Qwen2.5-Math-1.5B MATH 89.4%，均超 o1-preview。

## 原始链接
- url: https://arxiv.org/abs/2501.04519
- pdf_url: https://arxiv.org/pdf/2501.04519
- github_url: https://github.com/microsoft/rStar

## 一手源存档（sources/）
- rstar-math.pdf  （PDF 不入 git，走 HF bucket）
