---
title: "GLM-5.2（智谱旗舰：长程任务 + 1M 上下文 + IndexShare 稀疏注意力）"
org: 智谱 Z.ai (Zhipu)
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/zai-org/GLM-5.2
pdf_url: https://arxiv.org/abs/2603.12201
github_url: https://github.com/zai-org/GLM-5
downloaded: [glm-5.2-readme.md, glm-5.2-config.json, arxiv-2603.12201-glm-indexshare.pdf]
---

## 一句话定位
智谱最新旗舰 GLM-5.2 —— 面向 long-horizon 任务，较 GLM-5.1 大幅提升并首次在**稳定 1M-token 上下文**上交付该能力；MIT 纯开源（晚于本次初版调研，属增量补录）。

## 摘要
GLM-5.2 是 GLM-5 之后的旗舰迭代（GLM-5 技术报告 arXiv 2602.15763）。核心升级：稳定支撑长程工作的 1M 上下文；架构上提出 **IndexShare**（arXiv 2603.12201）——每 4 个稀疏注意力层复用同一 indexer，1M 上下文下 per-token FLOPs 降 2.9×；改进 MTP 投机解码，acceptance length 提升达 20%。MIT 许可、无地域限制。SGLang/vLLM/Transformers/KTransformers/Unsloth + Ascend NPU 均支持。

## 关键技术细节
- **架构（config.json）**：`model_type=glm_moe_dsa`（DeepSeek 风格稀疏注意力 MoE）；hidden 6144；**78 层**；注意力 64 头 / 64 KV，**MLA 式**（qk_head_dim 256 = nope 192 + rope 64，head_dim 192）；**MoE 256 路由专家 + 1 共享专家，每 token 选 8**，moe_intermediate 2048；上下文 **1M**（max_position 1,048,576）；rope_theta 8e6。
- **IndexShare**：跨稀疏注意力层共享 indexer，长上下文降算力（arXiv 2603.12201）。
- **MTP**：改进多 token 预测层，投机解码 accept 长度 +20%。
- **评测**：AIME 2026、HMMT Feb 2026、HLE、SWE-Bench Pro（OpenHands，400K 上下文）等长程/agentic 基准。
- 许可 MIT；定位 long-horizon + agentic + coding。

## 原始链接
- url: https://huggingface.co/zai-org/GLM-5.2 · blog: https://z.ai/blog/glm-5.2
- GLM-5 技术报告: https://arxiv.org/abs/2602.15763 ; IndexShare: https://arxiv.org/abs/2603.12201

## 本地落盘文件
- ../../../sources/llm/2026/glm-5.2-readme.md
- ../../../sources/llm/2026/glm-5.2-config.json
- ../../../sources/llm/2026/arxiv-2603.12201-glm-indexshare.pdf
