---
title: "ReTool: Reinforcement Learning for Strategic Tool Use in LLMs"
org: "字节跳动 (ByteDance Seed)"
country: China
date: 2025-04
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2504.11536
pdf_url: https://arxiv.org/pdf/2504.11536
github_url: https://github.com/ReTool-RL/ReTool
downloaded: [retool-2504.11536.pdf]
---

## 一句话定位
字节用 outcome-driven RL 教推理模型"何时/如何调用代码解释器"：在长链推理中实时交错执行代码，32B 模型 400 步训练达 AIME 67%，超 o1-preview，并涌现代码自纠错"aha moment"。

## 摘要
纯文本 RL 推理模型(如 DeepSeek-R1)在需要结构化求解(几何、精确计算、复杂方程)时吃力，而代码解释器(CI)有优势。ReTool 用"工具集成学习(tool-integrated learning)"增强长链推理：① 在自然语言推理过程中动态交错实时代码执行；② 一套自动 RL 范式，让 rollout 支持多轮实时代码执行，并依据结果反馈教模型学会"何时、如何"调用工具。训练框架先用合成冷启动数据生成代码增强的长链推理轨迹微调基座，再用任务结果作奖励迭代精炼工具使用策略，无需人类先验。在 AIME 上，32B 模型 400 步达 67%，效率与性能均超文本 RL 基线(40%，1080 步)；扩展设置达 72.5%，超 o1-preview 27.9 个百分点。还观察到代码自纠错等涌现行为。

## 关键技术细节
- 基座：Qwen2.5-32B(及对比)；工具=沙盒代码解释器(Python)。
- 两阶段：① 合成冷启动 SFT(生成代码增强的长 CoT 轨迹)；② outcome-driven RL(rollout 内多轮实时执行代码，结果奖励)。
- RL：rollout 中真实执行代码、把 stdout 回填上下文；以最终答案正确性为奖励。
- 结果：AIME 32B 模型 400 步 67%(文本 RL 基线 40% 需 1080 步)；扩展设置 72.5%，比 OpenAI o1-preview 高 27.9 个百分点。
- 涌现行为：代码自纠错(code self-correction)、自主发现最佳工具调用时机("aha moment")。

## 原始链接
- url: https://arxiv.org/abs/2504.11536
- pdf_url: https://arxiv.org/pdf/2504.11536
- github_url: https://github.com/ReTool-RL/ReTool

## 一手源存档（sources/）
- [retool-2504.11536.pdf](https://arxiv.org/pdf/2504.11536)  （arXiv 原文 PDF，不入 git）
