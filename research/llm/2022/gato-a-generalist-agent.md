---
title: A Generalist Agent (Gato)
org: DeepMind
country: UK
date: 2022-05
type: paper
categories: [agentic训练, 架构]
url: https://arxiv.org/abs/2205.06175
pdf_url: https://arxiv.org/pdf/2205.06175
github_url:
downloaded: [gato.pdf]
---

## 一句话定位
DeepMind 的 Gato：单一网络同权重处理文本、图像、Atari、机器人控制等多模态多任务多形态，是"通才智能体"的早期里程碑。

## 摘要
受大规模语言建模进展启发，DeepMind 将类似方法用于构建超越纯文本输出的单一通才智能体。Gato 是多模态、多任务、多形态（multi-embodiment）的通才策略：同一网络同一权重能玩 Atari、给图像配字幕、聊天、用真实机器人臂码积木等，根据上下文决定输出文本、关节力矩、按键还是其他 token。报告描述模型与数据，并记录其当前能力。

## 关键技术细节
- 模型：约 1.2B 参数的 decoder-only Transformer（相对小，强调通用性而非规模）。
- 统一序列化：把所有模态（文本、图像 patch、离散/连续动作、本体感觉）token 化为统一序列，自回归预测下一 token。
- 训练任务：604 个不同任务，跨模拟控制（DM Control、Meta-World）、Atari、机器人堆叠、图像字幕、对话等。
- 同一权重跨任务/跨形态切换，依靠 prompt/上下文确定当前任务。
- 上下文长度 1024 token；图像用 ResNet patch 嵌入。
- 意义：把"序列建模 = 通用智能体"的范式推向多模态控制，预示后续具身/agent 方向。

## 原始链接
- url: https://arxiv.org/abs/2205.06175
- pdf_url: https://arxiv.org/pdf/2205.06175

## 本地落盘文件
- ../../../sources/llm/2022/gato.pdf
