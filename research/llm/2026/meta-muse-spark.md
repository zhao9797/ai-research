---
title: "Introducing Muse Spark: Scaling Towards Personal Superintelligence"
org: Meta (Meta Superintelligence Labs)
country: US
date: 2026-04
type: blog
categories: [预训练数据, 架构, AI infra, 后训练, agentic训练]
url: https://ai.meta.com/blog/introducing-muse-spark-msl/
pdf_url:
github_url:
downloaded: [meta-muse-spark.html]
---

## 一句话定位
Meta Superintelligence Labs (MSL) 2026-04-08 发布的首个模型 Muse Spark——原生多模态推理模型，支持工具使用、视觉链式思维与多智能体编排（Contemplating mode），标志 Meta AI 从 Llama 转向"个人超级智能"的全栈重建。

## 摘要
Muse Spark 是 Muse 家族首个模型，由 Meta Superintelligence Labs 开发，是从研究、模型训练到基础设施（含 Hyperion 数据中心）的"自底向上"重建的首个产物。它是原生多模态推理模型，支持 tool-use、visual chain of thought 与 multi-agent orchestration，在多模态感知、推理、健康、agentic 任务上有竞争力（长周期 agentic 与编程仍是补强方向）。新增 Contemplating mode：并行编排多个 agent 推理，对标 Gemini Deep Think 与 GPT Pro，HLE 58%、FrontierScience Research 38%。健康能力与 1000+ 医生合作整理训练数据。博客详细给出三条 scaling 轴：预训练、强化学习、测试时推理。今日上线 meta.ai 与 Meta AI app，并开放私有 API preview。

## 关键技术细节
- 发布：2026-04-08（Meta Superintelligence Labs 首个模型）。15 分钟阅读博客。
- 模型类型：原生多模态推理模型；tool-use + visual CoT + multi-agent orchestration。
- Contemplating mode：并行编排多 agent 推理（对标 Gemini Deep Think、GPT Pro）；HLE 58%、FrontierScience Research 38%。
- 预训练（scaling 轴1）：过去 9 个月重建预训练栈（架构、优化、数据整理）；拟合 scaling law 后，达到相同能力所需训练 FLOPs 比前代 Llama 4 Maverick 少"一个数量级以上"（>10×），也显著优于对比基座。
- 强化学习（scaling 轴2）：新 RL 栈平滑可预测；训练集 pass@1 与 pass@16 呈 log-linear 增长（提升可靠性而不损推理多样性）；held-out 评估集增益可预测地泛化。
- 测试时推理（scaling 轴3）：RL 训练模型"先思后答"，测试时计算可扩展。
- 健康：与 1000+ 医生合作整理训练数据，生成交互式健康信息展示。
- Infra：跨全栈战略投入，含 Hyperion 数据中心。
- 可用性：meta.ai / Meta AI app；私有 API preview。评估方法学：ai.meta.com/static-resource/muse-spark-eval-methodology。

## 原始链接
- url: https://ai.meta.com/blog/introducing-muse-spark-msl/

## 本地落盘文件
- ../../../sources/llm/2026/meta-muse-spark.html
