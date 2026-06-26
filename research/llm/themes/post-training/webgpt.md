---
title: "WebGPT: Browser-assisted question-answering with human feedback"
org: OpenAI
country: US
date: 2021-12
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2112.09332
pdf_url: https://arxiv.org/pdf/2112.09332
downloaded: [webgpt.pdf]
---

## 一句话定位
早期"工具使用 + RLHF"代表作：让 GPT-3 在文本浏览器环境中检索网页回答长问题，用人类反馈训练奖励模型并做 rejection sampling / RL，是 agentic 训练与浏览检索的先声。

## 摘要（3-6 句）
WebGPT 把 GPT-3 微调成能操作一个基于文本的浏览环境（搜索、点击链接、引用、滚动）来回答开放式长问题（ELI5）。模型通过行为克隆（模仿人类演示）学会浏览动作，再用人类对答案的成对偏好训练奖励模型，并用 best-of-n（rejection sampling）与 RL 优化。模型生成的答案会附带引用来源，便于人类核查事实性。最佳模型的答案在 56% 的情况下被人类偏好于人类示范者，在 69% 的情况下被偏好于 Reddit ELI5 高赞答案。

## 关键技术细节
- 基座：GPT-3（760M、13B、175B 三档）。
- 动作空间：文本浏览器命令（Search、Clicked Link、Quote、Scroll、Back、End answer 等），动作序列即"agent 轨迹"。
- 训练方式：(1) 行为克隆 BC（人类演示）；(2) 奖励建模 RM（成对偏好）；(3) rejection sampling (best-of-n) 与 PPO RL；BC+RM+RL 组合最佳。
- 引用机制：答案必须给出来源引文，使事实性可被验证——是后来"可验证奖励"思想的早期体现。
- 评测：TruthfulQA 上比基线更真实、信息量更高；揭示了模仿人类检索偏差等问题。

## 原始链接
- url: https://arxiv.org/abs/2112.09332
- pdf_url: https://arxiv.org/pdf/2112.09332

## 一手源存档（sources/）
- webgpt.pdf  （PDF 不入 git，走 HF bucket）
