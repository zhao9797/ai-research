---
title: "CodeGeeX2: A More Powerful Multilingual Code Generation Model（官方 GitHub）"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua KEG）
country: China
date: 2023-07
type: github
categories: [架构, 预训练数据]
url: https://github.com/THUDM/CodeGeeX2
pdf_url:
github_url: https://github.com/THUDM/CodeGeeX2
downloaded: [codegeex2-readme.md]
---

## 一句话定位
CodeGeeX2-6B：基于 ChatGLM2-6B 架构 + 600B 代码预训练的第二代多语言代码模型，6B 参数即超过 15B 的 StarCoder，HumanEval Python 35.9%，是智谱 2023 代码模型一手资料。

## 摘要（3-6 句）
CodeGeeX2 是多语言代码生成模型 CodeGeeX 的第二代。不同于一代完全在国产昇腾平台训练，CodeGeeX2 基于 ChatGLM2-6B 架构加入代码预训练实现，得益于 ChatGLM2 更优性能，在多项指标全面提升（+107% > CodeGeeX；仅 60 亿参数即超过 150 亿参数的 StarCoder-15B 近 10%）。继承 ChatGLM2-6B 特性，支持中英文输入、最大 8192 序列，量化后仅需 6GB 显存。

## 关键技术细节
- 基座：ChatGLM2-6B（6B 参数），在其上继续做 600B 代码数据预训练。
- 性能：相比一代 +107%；HumanEval-X 六语言全面提升（Python +57%、C++ +71%、Java +54%、JS +83%、Go +56%、Rust +321%）；Python Pass@1 达 35.9%，超过 StarCoder-15B。
- 上下文：最大 8192 序列长度；推理速度较一代 CodeGeeX-13B 大幅提升。
- 部署：量化后仅需 6GB 显存，支持轻量本地化部署。
- 工具/插件：CodeGeeX 插件（VS Code / JetBrains）支持 100+ 编程语言，新增上下文补全、跨文件补全、Ask CodeGeeX 交互问答。
- 关系：CodeGeeX（一代，arXiv 2303.17568，昇腾训练）→ CodeGeeX2（基于 ChatGLM2，本页）。

## 原始链接
- url: https://github.com/THUDM/CodeGeeX2
- github_url: https://github.com/THUDM/CodeGeeX2

## 一手源存档（sources/）
- [codegeex2-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/codegeex2-readme.md)
