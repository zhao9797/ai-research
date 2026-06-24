---
title: Announcing Mistral 7B
org: Mistral AI
country: EU
date: 2023-09
type: blog
categories: [架构, AI infra]
url: https://mistral.ai/news/announcing-mistral-7b/
downloaded: [mistral-7b-blog.html]
---

## 一句话定位
Mistral AI 首发公告，官方解释 SWA/GQA 工程细节与 Llama 2 对比，Apache 2.0 开放下载。

## 摘要
Mistral AI 官方发布 Mistral 7B 的公告博客。Mistral 7B 在所有基准超 Llama 2 13B，在推理/数学/代码上等同 Llama 34B，MMLU 上等效 3x+ 参数的 Llama 2。用滑动窗口注意力与对 FlashAttention/xFormers 的改造实现高效长序列。提供 chat 微调版超 Llama 2 13B chat。Apache 2.0，可自由下载与部署。

## 关键技术细节
- 参数：7.3B；Apache 2.0。
- 全面超 Llama 2 13B、等同 Llama 34B(推理/数学/代码)；MMLU 等效 3x+ 大的 Llama 2。
- SWA：每层注意前 4096 个隐状态；线性计算成本 O(sliding_window·seq_len)；借层堆叠扩大有效感受野。
- 工程：改 FlashAttention/xFormers，16k 序列 4k 窗口下约 2x 提速。
- Rolling buffer cache：缓存固定为窗口大小。
- Instruct 版：在公开 HF 指令数据上微调，MT-Bench 超所有 7B、媲美 13B chat。

## 原始链接
- url: https://mistral.ai/news/announcing-mistral-7b/

## 本地落盘文件
- ../../../sources/llm/2023/mistral-7b-blog.html
