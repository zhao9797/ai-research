---
title: "GLM-4.6: Advanced Agentic, Reasoning and Coding Capabilities"
org: 智谱 AI / Z.ai (Zhipu AI)
country: China
date: 2025-09
type: blog
categories: [后训练, agentic训练, 架构]
url: https://z.ai/blog/glm-4.6
pdf_url:
github_url: https://huggingface.co/zai-org/GLM-4.6
downloaded: [glm-4.6-blog.md]
---

## 一句话定位
智谱旗舰 GLM-4.5 的升级版 GLM-4.6：上下文 128K→200K，编程/推理/agent 全面增强，对标 DeepSeek-V3.2-Exp 与 Claude Sonnet 4。发布 2025-09-30。

## 摘要
官方博客：相比 GLM-4.5，GLM-4.6 关键改进——上下文窗口 128K→200K（应对更复杂 agentic 任务）；编程性能更强（Claude Code、Cline、Roo Code、Kilo Code 等真实应用表现更好，含前端页面美观度）；推理增强且支持推理时工具调用；agent（tool use、search agent）能力更强、更好融入 agent 框架；写作更贴合人类偏好。在覆盖 agent/推理/编程的 8 个公开 benchmark 上较 GLM-4.5 明显提升，相对 DeepSeek-V3.2-Exp、Claude Sonnet 4 等有竞争力。技术报告沿用 GLM-4.5 ARC 论文。

## 关键技术细节
- 上下文：128K → 200K tokens。
- 编程：code benchmark 提升 + Claude Code/Cline/Roo/Kilo 真实场景增强（含前端视觉）。
- 推理：支持推理时 tool use；推理 benchmark 明显提升。
- Agent：tool-using / search agent 更强，更好适配 agent 框架。
- 基座：延续 GLM-4.5 的 355B MoE / 32B 激活 ARC 架构（技术报告 arXiv 2508.06471）。
- 开源：HuggingFace zai-org/GLM-4.6。

## 原始链接
- url: https://z.ai/blog/glm-4.6
- tech report: https://arxiv.org/abs/2508.06471
- github_url: https://huggingface.co/zai-org/GLM-4.6

## 一手源存档（sources/）
- [glm-4.6-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/glm-4.6-blog.md)
