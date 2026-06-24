---
title: "GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models"
org: "智谱 AI / Z.ai (Zhipu / THUDM)"
country: China
date: 2025-08
type: report
categories: [架构, 预训练数据, 后训练, agentic训练]
url: https://arxiv.org/abs/2508.06471
pdf_url: https://arxiv.org/pdf/2508.06471
github_url: https://github.com/zai-org/GLM-4.5
downloaded: [glm-4.5-2508.06471.pdf]
---

## 一句话定位
智谱以"agentic/推理/编码(ARC)"为目标的开源 MoE 旗舰：355B 总参/32B 激活，混合推理(思考+直答)，23T token 预训练 + 专家模型迭代 + RL 后训练，agentic 基准排名仅次于第一梯队闭源。

## 摘要
GLM-4.5 是开源 MoE 大模型，355B 总参、32B 激活，采用混合推理方法支持"思考"与"直接响应"两种模式。通过 23T token 的多阶段训练与含专家模型迭代(expert model iteration)和强化学习的全面后训练，GLM-4.5 在 agentic、推理、编码(ARC) 任务上表现强劲：TAU-Bench 70.1%、AIME 24 91.0%、SWE-bench Verified 64.2%。在参数远少于多个竞品的情况下，总体排名第 3、agentic 基准排名第 2。同时发布紧凑版 GLM-4.5-Air(106B 参数)。

## 关键技术细节
- 架构：MoE，GLM-4.5 355B 总参 / 32B 激活；GLM-4.5-Air 106B(12B 激活)。
- 混合推理(hybrid reasoning)：单模型支持 thinking 模式(复杂任务)与 direct response(快速)。
- 预训练：23T token 多阶段训练。
- 后训练：专家模型迭代(expert model iteration，先训专精模型再蒸/合) + 强化学习(RL)。
- agentic/推理/编码三靶基准：TAU-Bench 70.1%、AIME 24 91.0%、SWE-bench Verified 64.2%。
- 排名：总体第 3、agentic 第 2(论文评测口径)，参数显著少于竞品。
- 开源 GLM-4.5(355B) 与 GLM-4.5-Air(106B)。

## 原始链接
- url: https://arxiv.org/abs/2508.06471
- pdf_url: https://arxiv.org/pdf/2508.06471
- github_url: https://github.com/zai-org/GLM-4.5

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/glm-4.5-2508.06471.pdf
