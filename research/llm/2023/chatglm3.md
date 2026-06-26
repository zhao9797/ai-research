---
title: "ChatGLM3 series: Open Bilingual Chat LLMs（官方 GitHub）"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua KEG）
country: China
date: 2023-10
type: github
categories: [架构, 后训练, agentic训练]
url: https://github.com/THUDM/ChatGLM3
pdf_url:
github_url: https://github.com/THUDM/ChatGLM3
downloaded: [chatglm3-readme.md]
---

## 一句话定位
ChatGLM3-6B：智谱/清华第三代开源对话模型，全新 Prompt 格式原生支持 Function Call、Code Interpreter 与 Agent 任务，是中国开源模型 2023 年原生 agentic 能力的代表（官方 GitHub 一手）。

## 摘要（3-6 句）
ChatGLM3 是智谱 AI 与清华 KEG 联合发布的对话预训练模型。ChatGLM3-6B 在保留前两代流畅对话、低部署门槛的基础上：(1) 基座 ChatGLM3-6B-Base 采用更多样训练数据、更充分训练步数与更合理训练策略，在 10B 以下基座中性能最强；(2) 采用全新设计的 Prompt 格式，原生支持工具调用（Function Call）、代码执行（Code Interpreter）和 Agent 任务等复杂场景；(3) 开源序列更全：对话模型、基座 ChatGLM3-6B-Base、长文本 ChatGLM3-6B-32K。

## 关键技术细节
- 基座：ChatGLM3-6B-Base，10B 以下基座中性能最强（语义/数学/推理/代码/知识多维评测）。
- 全新 Prompt 格式：定义 system/user/assistant/observation 等角色，支撑多轮 + 工具调用结构化交互。
- 原生 agentic 能力：Function Call（工具调用）、Code Interpreter（代码执行）、Agent 任务。
- 开源序列：ChatGLM3-6B（对话）、ChatGLM3-6B-Base（基座）、ChatGLM3-6B-32K（长文本）。
- 时间线：2023/10 发布；后续技术报告统一于 ChatGLM 家族论文（arXiv 2406.12793，2024）。
- 生态：智谱清言（chatglm.cn）线上提供 GLM-4 / GLM-3-Turbo 的 System Prompt / Function Call / Retrieval / Web_Search 等。

## 原始链接
- url: https://github.com/THUDM/ChatGLM3
- github_url: https://github.com/THUDM/ChatGLM3

## 一手源存档（sources/）
- [chatglm3-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/chatglm3-readme.md)
