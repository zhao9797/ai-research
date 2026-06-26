---
title: Llama 3.2 - Revolutionizing edge AI and vision with open, customizable models
org: Meta
country: US
date: 2024-09
type: blog
categories: [架构, 后训练]
url: https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
pdf_url:
github_url: https://github.com/meta-llama/llama-stack
downloaded: [meta-llama-3-2-blog.md]
---

## 一句话定位
Llama 3.2 发布博客：首个 Llama 视觉模型（11B/90B）+ 端侧轻量纯文本模型（1B/3B），并推出官方 Llama Stack 部署发行版。

## 摘要
2024-09-25（Meta Connect）发布。Llama 3.2 含中小型视觉 LLM（11B、90B）和适配边缘/移动端的轻量纯文本模型（1B、3B），均含预训练与指令微调版本。1B/3B 支持 128K 上下文，端侧（摘要/指令遵循/改写）同级 SOTA，首日支持高通、联发科硬件并为 Arm 优化。11B/90B 视觉模型可直接替换对应纯文本模型，在图像理解上超过 Claude 3 Haiku 等闭源模型；预训练与对齐版本均开放，可用 torchtune 微调、torchchat 本地部署。同时发布首个官方 Llama Stack 发行版（单节点/本地/云/端侧）。

## 关键技术细节
- 视觉模型：11B、90B（图像理解超 Claude 3 Haiku 级闭源模型）；视觉适配器架构，drop-in 替换对应文本模型。
- 轻量模型：1B、3B 纯文本，128K 上下文；为边缘/移动端设计，高通/联发科首日支持、Arm 优化。
- 工具链：torchtune 微调、torchchat 本地部署；Llama Stack 官方发行版（单节点经 Ollama，端侧经 PyTorch ExecuTorch），含 RAG/工具调用与集成安全。
- 生态合作：AWS、Databricks、Dell、Fireworks、Infosys、Together AI 等构建 Llama Stack 发行版。
- 安全：Llama Guard 3（含视觉版，见 arXiv 2411.10414）。

## 原始链接
- url: https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
- github: https://github.com/meta-llama/llama-stack

## 一手源存档（sources/）
- [meta-llama-3-2-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/meta-llama-3-2-blog.md)
