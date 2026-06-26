---
title: "WebGLM: Towards An Efficient Web-Enhanced Question Answering System with Human Preferences"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua）
country: China
date: 2023-06
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2306.07906
pdf_url: https://arxiv.org/pdf/2306.07906
github_url: https://github.com/THUDM/WebGLM
downloaded: [webglm.pdf]
---

## 一句话定位
智谱/清华 WebGLM：给 GLM 装上"网页检索 + 引用生成 + 人类偏好打分"的高效联网问答系统，对标并改进 OpenAI WebGPT，是中国"工具/检索增强 agent"一手论文（KDD'23）。

## 摘要（3-6 句）
WebGLM 是基于 GLM 的网页增强问答系统，目标是在真实部署高效的前提下为 LLM 加上网页搜索与检索能力。其三大组件：LLM 增强的检索器、自举式生成器、以及人类偏好感知的打分器。作者识别并改进了 WebGPT（OpenAI）的局限，使 WebGLM 在准确性、效率与成本上更优。

## 关键技术细节
- LLM-augmented Retriever：两阶段检索——粗排（基于搜索引擎 + 检索）+ 用 GPT-3 蒸馏出的细排器对参考文献打分。
- Bootstrapped Generator：用少量人工示范 + LLM-in-the-loop 自举构造大规模带引用的长答案数据集（WebGLM-QA），训练 GLM-10B 生成带引用的回答，避免昂贵人工标注。
- Human Preference-aware Scorer：在用户点赞/偏好数据上训练打分器，对候选回答按人类偏好排序，提升回答质量。
- 基座：GLM-10B / GLM-2B。
- 评测：在效率、成本、人评质量上对标 WebGPT-13B/175B，达到可比甚至更优，且推理成本显著更低。
- 联网/工具属性：属检索增强 + 工具调用式 agent 系统的早期中国一手工作。

## 原始链接
- url: https://arxiv.org/abs/2306.07906
- pdf_url: https://arxiv.org/pdf/2306.07906
- github_url: https://github.com/THUDM/WebGLM

## 一手源存档（sources/）
- webglm.pdf  （PDF 不入 git，走 HF bucket）
