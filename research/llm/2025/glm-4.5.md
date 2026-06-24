---
title: "GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models"
org: 智谱 AI / Z.ai (Zhipu AI)
country: China
date: 2025-08
type: paper
categories: [架构, 预训练数据, 后训练, agentic训练]
url: https://arxiv.org/abs/2508.06471
pdf_url: https://arxiv.org/pdf/2508.06471
github_url: https://github.com/zai-org/GLM-4.5
downloaded: [glm-4.5.pdf]
---

## 一句话定位
智谱 355B MoE / 32B 激活旗舰，混合推理（thinking + direct），主打 agentic/reasoning/coding（ARC），23T token 训练 + expert model iteration + RL；同发 106B 的 GLM-4.5-Air。发布 2025-08-08。

## 摘要
GLM-4.5 是开源 MoE 大模型，355B 总参、32B 激活，支持 thinking 与 direct response 双模式的 hybrid reasoning。经 23T token 多阶段训练与"专家模型迭代 + 强化学习"的综合后训练，在 agentic / reasoning / coding（ARC）任务上表现强劲：TAU-Bench 70.1%、AIME 24 91.0%、SWE-bench Verified 64.2%。以远少于多个竞品的参数，综合排名第 3、agentic benchmark 第 2。同时开源 GLM-4.5（355B）与紧凑版 GLM-4.5-Air（106B）。

## 关键技术细节
- 架构：355B 总参 / 32B 激活 MoE；hybrid reasoning（thinking + direct 双模式）；相比 DeepSeek-V3/Kimi 采用更深、更窄（更多层、更小 hidden）设计 + 更多注意力头。
- 训练数据：23T tokens 多阶段预训练。
- 后训练：expert model iteration（先训练专精 reasoning / agent / coding 的专家模型，再蒸馏融合）+ 大规模 RL。
- Agentic RL：在可验证环境（SWE 任务、tool use）做 RL，slime RL infra。
- 成绩：TAU-Bench 70.1、AIME24 91.0、SWE-bench Verified 64.2。
- 开源：GLM-4.5（355B）+ GLM-4.5-Air（106B），MIT 协议。

## 原始链接
- url: https://arxiv.org/abs/2508.06471
- pdf_url: https://arxiv.org/pdf/2508.06471
- blog: https://z.ai/blog/glm-4.5
- github_url: https://github.com/zai-org/GLM-4.5

## 本地落盘文件
- ../../../sources/llm/2025/glm-4.5.pdf
