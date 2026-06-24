---
title: "Skywork R1V: Pioneering Multimodal Reasoning with Chain-of-Thought"
org: 昆仑万维 天工 (Kunlun Skywork AI)
country: China
date: 2025-04
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2504.05599
pdf_url: https://arxiv.org/pdf/2504.05599
github_url: https://github.com/SkyworkAI/Skywork-R1V
downloaded: [skywork-r1v.pdf]
---

## 一句话定位
昆仑天工把 R1 系列文本推理迁移到视觉：用轻量视觉投影器无需重训基座/视觉编码器即实现多模态适配，SFT+GRPO 混合优化 + 自适应长度 CoT 蒸馏。发布 2025-04-08。

## 摘要
Skywork R1V 将 R1 系列 LLM 推理能力扩展到视觉模态，采用高效多模态迁移：用轻量视觉投影器（visual projector）实现无缝多模态适配，无需重训语言基座或视觉编码器。提出混合优化策略——迭代 SFT + GRPO，显著提升跨模态对齐效率；并提出自适应长度 CoT 蒸馏方法动态优化推理链长度，提升推理效率、防止过度思考。

## 关键技术细节
- 多模态迁移：轻量 visual projector 连接已有 vision encoder 与 R1 系列 LLM，免重训。
- 混合优化：Iterative SFT + GRPO（Group Relative Policy Optimization）强化视觉-文本对齐。
- CoT 蒸馏：adaptive-length CoT distillation，动态优化推理链长度，防 overthinking。
- 任务：多模态链式思维推理（数学/科学图文题等）。
- 开源：GitHub SkyworkAI/Skywork-R1V（后续有 R1V2、R1V3）。

## 原始链接
- url: https://arxiv.org/abs/2504.05599
- pdf_url: https://arxiv.org/pdf/2504.05599
- github_url: https://github.com/SkyworkAI/Skywork-R1V

## 本地落盘文件
- ../../../sources/llm/2025/skywork-r1v.pdf
