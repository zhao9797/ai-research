---
title: OpenAI o3-mini 发布
org: OpenAI
country: US
date: 2025-01
type: blog
categories: [后训练, agentic训练]
url: https://openai.com/index/openai-o3-mini/
pdf_url:
github_url:
downloaded: [files/openai-o3-mini-blog.md]
---

## 一句话定位
OpenAI 2025-01-31 发布的小型推理模型 o3-mini 官方博客，主打 STEM 推理、低成本与可调"推理强度"，首次将带函数调用/结构化输出的推理模型推向 API。

## 摘要
o3-mini 面向 STEM（数学、编码、科学），中等推理强度下与 o1 相当但更快。首次支持 reasoning effort 三档（low/medium/high），并在推理模型中支持函数调用、结构化输出、开发者消息。专家评测中 56% 偏好 o3-mini 胜过 o1-mini，重大错误减少 39%。

## 关键技术细节（带数字）
- 推理强度三档：low / medium / high（`o3-mini-high` 在 ChatGPT 中对付费用户开放）。
- 数学 AIME 2024：high 档 83.6%；low 档≈o1-mini，medium 档≈o1。
- GPQA Diamond（PhD 级科学）：high 档 77.0%。
- 专家盲评：56% 偏好 o3-mini 而非 o1-mini；重大错误减少 39%。
- 能力：支持 function calling、Structured Outputs、developer messages；面向技术领域精度与速度。
- 发布日期：2025-01-31。

## 原始链接
- 官方博客：https://openai.com/index/openai-o3-mini/

## 本地落盘文件
- ../../../sources/llm/2025/openai-o3-mini-blog.md
