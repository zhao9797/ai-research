---
title: "Step 3.7 Flash"
org: 阶跃星辰 StepFun
country: China
date: 2026-05
type: model-card
categories: [架构, agentic训练, 后训练]
url: https://huggingface.co/stepfun-ai/Step-3.7-Flash
pdf_url: ""
github_url: https://static.stepfun.com/blog/step-3.7-flash/
downloaded: [step-3.7-flash-modelcard.md]
---

## 一句话定位
阶跃星辰 Step 3.7 Flash，198B 稀疏 MoE 视觉语言模型（196B 语言主干 + 1.8B 视觉编码器），11B 激活、400 tok/s 高吞吐、256k 上下文、三档推理，面向高频生产级 agentic 工作流。

## 摘要
Step 3.7 Flash（HuggingFace stepfun-ai 官方组织，createdAt 2026-05-23，blog static.stepfun.com/blog/step-3.7-flash/）是一款 198B 参数稀疏 MoE 视觉语言模型，由 196B 语言主干 + 1.8B 视觉编码器组成，支持原生图像理解。面向高频生产负载，每 token 激活约 11B、吞吐高达 400 tok/s，支持 256k 上下文与 low/medium/high 三档推理，便于在速度、成本、认知深度间权衡。为需要把感知/搜索/推理结合的可扩展 agentic 工作流设计：单次解析海量财报、多步搜索循环+跨源验证、高吞吐并发 coding agent。开源（Apache-2.0），支持 vLLM/SGLang/Transformers/llama.cpp，并进入 NVIDIA Nemo / NIM 生态。同系列 2026 H1 还有 Step-3.5-Flash（2026-02/03）、Step-Audio-R1.5（arXiv 2026-04，见独立条目）。

## 关键技术细节
- **规格**：198B 稀疏 MoE VLM；196B 语言主干 + 1.8B 视觉编码器；激活约 11B/token。
- **吞吐/上下文**：最高 400 tokens/s；256k 上下文。
- **推理档位**：low / medium / high 三档可选。
- **多模态**：原生图像理解；SimpleVQA(Search) 79.2 第一、V*(Python) 95.3、解析 UI/GUI/图表映射到代码。
- **agentic/工具**：ClawEval-1.1 67.1（领先次名 59.8）；Toolathlon 49.5；HLE w. Tool 48.1；Terminal-Bench 2.1 59.5。
- **代码**：SWE-Bench PRO 56.3（第二名）；GDPVal-AA 45.8。
- **定价**：输入 cache miss $0.20/M、cache hit $0.04/M、输出 $1.15/M。
- **部署/开源**：Apache-2.0；vLLM/SGLang/Transformers/llama.cpp；NVIDIA Nemo（AutoModel/Megatron Core/Megatron Bridge）+ NIM 微服务；可在 DGX Station / Mac Studio(≥128GB) 本地运行。

## 原始链接
- url: https://huggingface.co/stepfun-ai/Step-3.7-Flash
- blog: https://static.stepfun.com/blog/step-3.7-flash/
- 平台: https://platform.stepfun.com (CN) / https://platform.stepfun.ai (Global)

## 本地落盘文件
- ../../../sources/llm/2026/step-3.7-flash-modelcard.md
