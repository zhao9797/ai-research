---
title: The Llama 4 herd (Scout, Maverick, Behemoth)
org: Meta AI
country: US
date: 2025-04
type: blog
categories: [架构, 预训练数据, 后训练, AI infra]
url: https://ai.meta.com/blog/llama-4-multimodal-intelligence/
pdf_url:
github_url: https://github.com/meta-llama/llama-models
downloaded: [files/meta-llama-4-blog.md]
---

## 一句话定位
Meta 2025-04-05 发布的 Llama 4 官方博客：首批原生多模态、首次采用 MoE 架构的开放权重 Llama 模型——Scout、Maverick 已发布，Behemoth（教师模型）仍在训练。

## 摘要
Llama 4 是 Meta 首个 MoE + 原生多模态（early fusion 文本/图像/视频）模型家族。Scout（17B 激活/16 专家/109B 总参）单卡 H100 可跑、10M token 上下文；Maverick（17B 激活/128 专家/400B 总参）单 H100 host 可跑；Behemoth（288B 激活/16 专家、约 2T 总参）作为蒸馏教师，仍在训练。引入 iRoPE（交错注意力 + 部分层无位置编码）、MetaP 超参迁移、FP8 训练，post-training 采用 lightweight SFT → online RL → lightweight DPO。

## 关键技术细节（带数字）
- Llama 4 Scout：17B 激活 / 16 专家 / 109B 总参；单张 H100（Int4 量化）；上下文 10M tokens（预/后训练用 256K）。
- Llama 4 Maverick：17B 激活 / 128 routed 专家 + 1 共享专家 / 400B 总参；交替 dense 与 MoE 层；单 H100 host 部署。
- Llama 4 Behemoth：288B 激活 / 16 专家 / ~2T 总参；作为 Scout/Maverick 的蒸馏教师（仍在训练）。
- 架构创新：iRoPE（interleaved attention 层 + 部分层 NoPE 无位置编码 + 推理时 attention 温度缩放），早期融合（early fusion）多模态，视觉编码器基于 MetaCLIP。
- 超参：MetaP 技术使 per-layer 学习率/初始化跨 batch size/宽度/深度/token 数稳定迁移。
- 预训练：>30T tokens（>2x Llama 3）；200 种语言（>100 种各超 1B token，多语 token ≈10x Llama 3）；FP8 精度。
- 算力：Behemoth 预训练用 32K GPU、FP8，达 390 TFLOPs/GPU。
- 后训练：lightweight SFT → online RL → lightweight DPO；用 Llama 当 judge 剔除 >50% 易样本；持续 online RL + 自适应难度过滤。
- 发布日期：2025-04-05；llama.com / Hugging Face 开放下载。

## 原始链接
- 官方博客：https://ai.meta.com/blog/llama-4-multimodal-intelligence/
- 下载：https://www.llama.com/llama-downloads/

## 一手源存档（sources/）
- [meta-llama-4-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2025/meta-llama-4-blog.md)
