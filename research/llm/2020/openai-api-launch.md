---
title: OpenAI API（GPT-3 商业化 API 发布）
org: OpenAI
country: US
date: 2020-06
type: blog
categories: [AI infra, 后训练]
url: https://openai.com/index/openai-api/
pdf_url:
github_url:
downloaded: [openai-api.html]
---

## 一句话定位
OpenAI 于 2020-06-11 推出首个商业化的通用“文本输入→文本输出” API，背后运行 GPT-3 权重，开启了大模型以 API 形式对外服务的商业模式。

## 摘要（3-6 句）
OpenAI 发布私有测试版 API，提供通用的 text-in/text-out 接口，可应用于几乎任意英文语言任务，用户仅需给出少量任务示例即可“编程”模型行为（few-shot prompting），也支持用自有数据集或人类反馈进一步微调特定任务。博客指出 API 当前以 GPT-3 系列权重运行，速度和吞吐相比论文版大幅提升。OpenAI 选择以受控 API（而非开源权重）发布，便于监控误用、终止有害用例并研究安全性。首批合作方包括 Algolia、Quizlet、Reddit 等。

## 关键技术细节
- 接口形态：通用 text-in/text-out completion API；通过 prompt 中的少量示例实现 few-shot in-context 编程。
- 底层模型：GPT-3 系列权重（链接到 arXiv 2005.14165），并强调相对论文版有显著速度/吞吐优化。
- 微调能力：支持用小/大规模自有数据集训练，或从用户/标注者的人类反馈中学习以提升特定任务表现（早期对齐与定制信号）。
- 发布策略：私有测试（private beta）而非开源，目的在于控制误用（骚扰、垃圾信息、激进化、虚假信息），可终止有害用例的访问权限。
- 安全工具：构建工具帮助用户控制返回内容，并研究语言技术的安全侧（分析、缓解、干预有害偏见）。
- 商业定位：API 收入用于支撑 OpenAI 使命，并降低构建有益 AI 产品的门槛。

## 原始链接
- url: https://openai.com/index/openai-api/

## 一手源存档（sources/）
- [openai-api.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2020/openai-api.html)
