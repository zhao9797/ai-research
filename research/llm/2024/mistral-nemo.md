---
title: "Mistral NeMo"
org: Mistral AI / NVIDIA
country: EU
date: 2024-07
type: blog
categories: [架构, AI infra]
url: https://mistral.ai/news/mistral-nemo/
pdf_url:
github_url:
downloaded: [mistral-nemo-blog.md]
---

## 一句话定位
Mistral NeMo（12B）发布博客：与 NVIDIA 合作的 12B 模型，128K 上下文，新 Tekken tokenizer，量化感知训练支持无损 FP8 推理，Apache 2.0。

## 摘要
2024-07-18 发布。Mistral NeMo 是与 NVIDIA 合作的 12B 模型，最大 128K 上下文，其推理、世界知识、编码准确率在同尺寸类别 SOTA。采用标准架构，可作为 Mistral 7B 的 drop-in 替换。base 与 instruct 检查点以 Apache 2.0 发布。用量化感知训练（QAT）训练，支持无性能损失的 FP8 推理。面向全球多语言应用（英/法/德/西/意/葡/中/日/韩/阿/印地等），训练了函数调用。引入新 tokenizer Tekken（基于 Tiktoken，训于 100+ 语言），对自然语言与源码压缩比 SentencePiece 更高：代码、中文、意/法/德/西/俄约高 30%，韩语/阿语分别高 2×/3×；对约 85% 语言比 Llama 3 tokenizer 更优。

## 关键技术细节
- 规模：12B（标准 decoder-only），128K 上下文，Mistral 7B 的 drop-in 替换。
- tokenizer：Tekken（基于 Tiktoken，100+ 语言），压缩率显著优于 SentencePiece。
- 量化：QAT 训练，支持无损 FP8 推理。
- 能力：函数调用、多语言。
- 合作/发布：NVIDIA 合作；HuggingFace 开放权重；打包为 NVIDIA NIM 微服务；Apache 2.0。

## 原始链接
- url: https://mistral.ai/news/mistral-nemo/

## 一手源存档（sources/）
- [mistral-nemo-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2024/mistral-nemo-blog.md)
