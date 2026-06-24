---
title: Introducing ChatGPT (官方发布博客)
org: OpenAI    country: US    date: 2022-11    type: blog
categories: [后训练]
url: https://openai.com/index/chatgpt/    pdf_url:    github_url:
downloaded: [openai-chatgpt-blog.html]
---

## 一句话定位
2022-11-30 OpenAI 发布 ChatGPT 的官方博客：以对话方式交互、可追问/认错/拒绝不当请求的助手，引爆全球大模型应用浪潮。

## 摘要
OpenAI 训练了名为 ChatGPT 的模型，可通过对话方式交互。对话形式使其能回答追问、承认错误、质疑错误前提、拒绝不当请求。ChatGPT 是 InstructGPT 的"兄弟模型"，经训练遵循提示中的指令并给出详细回复。OpenAI 以研究预览形式免费发布以收集用户反馈、了解优缺点。

## 关键技术细节
- 发布日期：2022 年 11 月 30 日（研究预览，免费）。
- 训练方法：与 InstructGPT 同样的 RLHF——先用人类 AI 训练师扮演双方收集对话示范做 SFT，再让训练师对模型多个候选回复排序构建奖励模型，用 PPO 做多轮 RLHF 微调（博客明确说基于 GPT-3.5 系列）。
- 基座：GPT-3.5 系列（在 2022 年初完成训练的模型上微调），运行于 Azure AI 超算。
- 能力：多轮对话、追问、承认错误、质疑错误前提、拒绝不当请求。
- 局限：会写出"看似合理但错误"的答案、对措辞敏感、可能冗长、对模糊问题倾向猜测而非反问。
- 迭代部署理念：以受控发布 + 用户反馈持续改进对齐与安全。

## 原始链接
- url: https://openai.com/index/chatgpt/

## 本地落盘文件
- ../../../sources/llm/2022/openai-chatgpt-blog.html
