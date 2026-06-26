---
title: "GLM-4.5V and GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning"
org: 智谱 AI / Z.ai (Zhipu AI)
country: China
date: 2025-07
type: paper
categories: [架构, 后训练, agentic训练]
url: https://arxiv.org/abs/2507.01006
pdf_url: https://arxiv.org/pdf/2507.01006
github_url: https://github.com/zai-org/GLM-V
downloaded: [glm-4.5v.pdf]
---

## 一句话定位
智谱视觉语言推理模型家族（GLM-4.1V-Thinking / GLM-4.5V / GLM-4.6V），提出 RLCS（带课程采样的 RL），GLM-4.5V 在 42 个公开 benchmark 多数达开源同尺寸 SOTA。发布 2025-07-01。

## 摘要
报告呈现 GLM-4.1V-Thinking、GLM-4.5V、GLM-4.6V 视觉语言模型家族，分享 reasoning-centric 训练框架的关键发现。先大规模预训练构建强视觉基座（决定性能上界），再提出 Reinforcement Learning with Curriculum Sampling (RLCS) 释放潜力，全面提升 STEM 解题、视频理解、内容识别、编程、grounding、GUI agent、长文档理解。GLM-4.5V 在 42 个公开 benchmark 上近乎全面达到同尺寸开源 SOTA，在编程与 GUI Agent 等难任务上对标甚至超越 Gemini-2.5-Flash；小尺寸 GLM-4.1V-9B-Thinking 亦表现优异。

## 关键技术细节
- 模型家族：GLM-4.1V-9B-Thinking、GLM-4.5V（基于 GLM-4.5-Air 106B MoE）、GLM-4.6V。
- 训练框架：大规模视觉预训练 → SFT → RLCS（Reinforcement Learning with Curriculum Sampling），课程采样按难度调度。
- 能力：STEM、视频理解、OCR/识别、编程、视觉 grounding、GUI agent、长文档。
- 评测：42 个公开 benchmark，开源同尺寸近全面 SOTA；GUI Agent / Coding 对标 Gemini-2.5-Flash。
- 开源：GitHub zai-org/GLM-V。

## 原始链接
- url: https://arxiv.org/abs/2507.01006
- pdf_url: https://arxiv.org/pdf/2507.01006
- github_url: https://github.com/zai-org/GLM-V

## 一手源存档（sources/）
- glm-4.5v.pdf  （PDF 不入 git，走 HF bucket）
