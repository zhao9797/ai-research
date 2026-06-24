---
title: "Baichuan-M2: Scaling Medical Capability with Large Verifier System"
org: 百川智能 (Baichuan AI)
country: China
date: 2025-09
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2509.02208
pdf_url: https://arxiv.org/pdf/2509.02208
github_url: https://huggingface.co/baichuan-inc/Baichuan-M2-32B
downloaded: [baichuan-m2.pdf]
---

## 一句话定位
百川医疗大模型 M2：用"大型验证器系统"+ 动态交互式 RL 弥合医疗 LLM 静态考试分数与真实临床决策的差距，基于 Qwen2.5-32B。发布 2025-09-02。

## 摘要
针对医疗 LLM 在 USMLE 等静态 benchmark 表现与真实临床决策效用之间的差距，Baichuan-M2 提出动态验证框架：超越静态答案验证器，构建大规模高保真交互式 RL 系统。框架含两个核心组件——患者模拟器（基于真实病历构建虚拟患者）与临床评分生成器（动态评估），使模型在多轮医疗问诊中通过 RL 提升真实临床决策能力。基于 Qwen2.5-32B 训练。

## 关键技术细节
- 核心：Large Verifier System——动态验证框架，含 Patient Simulator（病历驱动虚拟患者）+ Clinical Rubrics Generator（临床评分量表生成）。
- RL：大规模交互式强化学习，奖励来自多轮临床对话的动态评估（非静态答案匹配）。
- 基座：Qwen2.5-32B。
- 目标：弥合静态医考分数与真实临床决策效用的 gap。
- 开源：Baichuan-M2-32B（HuggingFace baichuan-inc）。

## 原始链接
- url: https://arxiv.org/abs/2509.02208
- pdf_url: https://arxiv.org/pdf/2509.02208
- github_url: https://huggingface.co/baichuan-inc/Baichuan-M2-32B

## 本地落盘文件
- ../../../sources/llm/2025/baichuan-m2.pdf
