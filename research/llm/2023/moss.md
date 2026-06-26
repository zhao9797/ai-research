---
title: "MOSS: An open-source tool-augmented conversational language model from Fudan University（官方 GitHub）"
org: 复旦大学（Fudan University / OpenMOSS）
country: China
date: 2023-04
type: github
categories: [预训练数据, 后训练, agentic训练]
url: https://github.com/OpenMOSS/MOSS
pdf_url:
github_url: https://github.com/OpenMOSS/MOSS
downloaded: [moss-readme.md]
---

## 一句话定位
复旦 MOSS（moss-moon-003，16B）：中国首个公开的支持插件/工具调用的开源对话语言模型，含基座、SFT、插件增强 SFT、偏好模型（PM）全链路，是 2023 agentic/工具增强对话一手资料。

## 摘要（3-6 句）
MOSS 是复旦大学开源的工具增强对话语言模型。moss-moon-003-base 基座在约 700B 单词高质量中英语料上自监督预训练（约 6.67×10²² FLOPs）；在约 110 万条多轮对话上 SFT 得到 moss-moon-003-sft；再加约 30 万条插件增强多轮对话训练出 moss-moon-003-sft-plugin，具备搜索引擎、文生图、计算器、解方程四种插件能力。还训练了偏好模型 moss-moon-003-pm，并据此得到最终的 moss-moon-003 / moss-moon-003-plugin。

## 关键技术细节
- 基座 moss-moon-003-base：约 160 亿（16B）参数；预训练语料约 700B 单词；计算量约 6.67×10²² 次浮点运算。
- SFT：moss-moon-003-sft 在约 110 万条多轮对话数据上微调（指令遵循 + 多轮对话 + 规避有害请求）。
- 插件增强（agentic）：moss-moon-003-sft-plugin 额外用约 30 万条插件增强多轮对话训练，支持搜索引擎、文生图、计算器、解方程四类插件。
- 偏好对齐：moss-moon-003-pm 偏好模型 → moss-moon-003 / moss-moon-003-plugin（更强事实性/安全性/意图理解）。
- 量化部署：int4（约 12GB 显存）/ int8（约 24GB 显存）版本。
- 开源数据：moss-002-sft-data（约 57 万英文 + 59 万中文，text-davinci-003 生成）、moss-003-sft-data（约 110 万条，基于约 10 万真实用户输入 + gpt-3.5-turbo 构造）、moss-003-sft-plugin-data（约 30 万条插件对话）。
- 工具生态：MOSS WebSearchTool 搜索引擎插件部署方案；衍生 WebCPM 等。

## 原始链接
- url: https://github.com/OpenMOSS/MOSS
- github_url: https://github.com/OpenMOSS/MOSS

## 一手源存档（sources/）
- [moss-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/moss-readme.md)
