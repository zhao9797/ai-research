---
title: "GLM-5.2（智谱旗舰：long-horizon + 1M 上下文 + IndexShare 稀疏注意力）"
org: 智谱 Z.ai (Zhipu)
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/zai-org/GLM-5.2
pdf_url: https://arxiv.org/abs/2602.15763
github_url: https://github.com/zai-org/GLM-5
downloaded: [glm-5.2-readme.md, glm-5.2-config.json, arxiv-2603.12201-glm-indexshare.pdf]
---

## 一句话定位
智谱最新旗舰，面向 long-horizon 任务，较 GLM-5.1 大幅提升并**首次在稳定 1M-token 上下文**上交付该能力；MIT 纯开源。基座方法见 GLM-5 技术报告《GLM-5: from Vibe Coding to Agentic Engineering》(arXiv 2602.15763)。

## 架构（config.json）
- `model_type=glm_moe_dsa`（DeepSeek 式稀疏注意力 MoE）；hidden 6144；**78 层**；rope_theta 8e6；上下文 **1M**（1,048,576）。
- 注意力 64 头 / 64 KV，**MLA 式**：qk_head_dim 256（nope 192 + rope 64），head_dim 192，index_head_dim 128。
- **MoE**：256 路由专家 + 1 共享，每 token 选 8，moe_intermediate 2048。
- **IndexShare**（arXiv 2603.12201，已落盘）：每 4 个稀疏注意力层**复用同一 indexer**，1M 上下文下 per-token FLOPs 降 **2.9×**。
- **改进 MTP**：投机解码 acceptance length 提升达 **20%**。

## 数据 / 训练 / RL
- 基座预训练数据、训练配方与 RL 对齐细节承自 **GLM-5 技术报告 (2602.15763)**（见库内 glm-5 页）；GLM-5.2 为其旗舰迭代。
- 新增能力：稳定 1M 长程上下文、**多档 thinking effort**（性能/延迟权衡）、更强 coding。

## Benchmark（vs GLM-5.1 / Qwen3.7-Max / MiniMax-M3 / DeepSeek-V4-Pro / Claude Opus 4.8 / GPT-5.5 / Gemini 3.1 Pro）
- **推理**：HLE 40.5（w/Tools 54.7）；AIME 2026 **99.2**（榜首）；HMMT Feb 2026 92.5；IMOAnswerBench **91.0**；GPQA-Diamond 91.2。
- **编码**：SWE-bench Pro 62.1；NL2Repo 48.9；DeepSWE 46.2；ProgramBench 63.7；Terminal-Bench 2.1 **81.0**（best harness 82.7）；FrontierSWE 74.4；SWE-Marathon 13.0。
- **Agentic**：MCP-Atlas 76.8；Tool-Decathlon 48.2。
- 评测多在 400K–1M 上下文、max effort 下进行；judge 用 GPT-5.5(medium)/Gemini-3.0-Pro。

## AI infra / 部署
- SGLang(0.5.13+) / vLLM(0.23+) / Transformers(`glm_moe_dsa`) / KTransformers / Unsloth；**Ascend NPU**（vLLM-Ascend / xLLM / SGLang）。
- 许可 **MIT**，无地域限制。

## 原始链接
- url: https://huggingface.co/zai-org/GLM-5.2 · blog: https://z.ai/blog/glm-5.2
- GLM-5 技术报告: https://arxiv.org/abs/2602.15763 · IndexShare: https://arxiv.org/abs/2603.12201

## 本地落盘文件
- ../../../sources/llm/2026/glm-5.2-readme.md
- ../../../sources/llm/2026/glm-5.2-config.json
- ../../../sources/llm/2026/arxiv-2603.12201-glm-indexshare.pdf
