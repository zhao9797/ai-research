---
title: "ChatGLM-6B: An Open Bilingual Dialogue Language Model（官方 GitHub）"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua KEG）
country: China
date: 2023-03
type: github
categories: [架构, 预训练数据, 后训练]
url: https://github.com/THUDM/ChatGLM-6B
pdf_url:
github_url: https://github.com/THUDM/ChatGLM-6B
downloaded: [chatglm-6b-readme.md]
---

## 一句话定位
ChatGLM-6B（2023-03）：智谱/清华首个开源中英双语对话模型，基于 GLM 架构、约 1T 双语 token，INT4 量化仅需 6GB 显存，是 2023 年初引爆国内开源大模型热潮的标志性一手发布。

## 摘要（3-6 句）
ChatGLM-6B 是基于 GLM 架构的开源、支持中英双语的对话语言模型，62 亿参数。结合模型量化技术，用户可在消费级显卡上本地部署（INT4 量化下最低仅需 6GB 显存）。模型经约 1T 标识符的中英双语训练，辅以监督微调、反馈自助、人类反馈强化学习等技术，已能生成相当符合人类偏好的回答。官方同时开源 P-Tuning v2 高效参数微调方法。

## 关键技术细节
- 架构：GLM（General Language Model）自回归空白填充目标；62 亿（6B）参数。
- 预训练：约 1 万亿（1T）中英双语标识符。
- 对齐：SFT + 反馈自助（feedback bootstrap）+ RLHF。
- 量化部署：FP16 约 13GB、INT8 约 8GB、INT4 约 6GB 显存，可消费级 GPU/本地部署。
- 微调：官方提供 P-Tuning v2 高效微调（INT4 下 7GB 显存即可微调）。
- 上下文：2048。
- 影响：2023-03 发布后迅速成为国内开源对话模型的事实标准起点，衍生 ChatGLM2/3、CodeGeeX2、VisualGLM 等。

## 原始链接
- url: https://github.com/THUDM/ChatGLM-6B
- github_url: https://github.com/THUDM/ChatGLM-6B
- blog: https://chatglm.cn/blog

## 本地落盘文件
- ../../../sources/llm/2023/chatglm-6b-readme.md
