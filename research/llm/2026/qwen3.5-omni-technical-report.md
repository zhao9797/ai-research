---
title: "Qwen3.5-Omni Technical Report"
org: 阿里巴巴 Qwen (Qwen Team / Alibaba)
country: China
date: 2026-04
type: paper
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2604.15804
pdf_url: https://arxiv.org/pdf/2604.15804
github_url: https://qwenlm.github.io
downloaded: [qwen3.5-omni.pdf]
---

## 一句话定位
阿里 Qwen 全模态旗舰 Qwen3.5-Omni，扩展到数千亿参数、256k 上下文，Thinker-Talker 双塔均用 Hybrid Attention MoE，音频/音视频理解 215 项子任务 SOTA。

## 摘要
Qwen3.5-Omni（arXiv 2026-04-17，作者 "Qwen Team"）是 Qwen-Omni 系列最新一代。相比前代显著演进，规模扩展到数千亿参数、支持 256k 上下文，利用海量异构 text-vision 数据与超过 1 亿小时音视频内容训练，具备稳健全模态能力。Qwen3.5-Omni-plus 在 215 个音频与音视频理解/推理/交互子任务上达 SOTA，关键音频任务超越 Gemini-3.1 Pro。架构上 Thinker 与 Talker 均采用 Hybrid Attention Mixture-of-Experts，支持长序列高效推理；支持 10+ 小时音频理解、400 秒 720P 视频（1 FPS）。为解决流式语音合成不稳定/不自然问题（源于文本与语音 tokenizer 编码效率差异），提出 ARIA 动态对齐机制。同期 Qwen 还发布 Qwen3.7-Plus 多模态智能体（官网 2026-06-01）。

## 关键技术细节
- **规模**：扩展到 hundreds of billions 参数；上下文 256k。
- **预训练数据**：海量异构 text-vision 对 + 超过 100M 小时音视频内容。
- **架构**：Thinker 与 Talker 均为 Hybrid Attention Mixture-of-Experts（混合注意力 MoE），高效长序列推理。
- **多模态能力**：支持 >10 小时音频理解、400 秒 720P 视频（1 FPS）。
- **评测**：Qwen3.5-Omni-plus 在 215 个音频/音视频子任务上 SOTA；关键音频任务超 Gemini-3.1 Pro，综合音视频理解持平。
- **流式语音-ARIA**：动态对齐 text 与 speech token，缓解流式 TTS 不稳定与不自然问题。
- **同系列其他 2026 H1 发布**：Qwen3.7-Plus（多模态智能体，官网 qwen.ai 2026-06-01，在 Qwen3.7 文本能力基础上升级 VL 与 agentic 能力）；Qwen-Robot Suite（RobotNav/RobotManip/RobotWorld，2026-06-16）。

## 原始链接
- url: https://arxiv.org/abs/2604.15804
- pdf_url: https://arxiv.org/pdf/2604.15804
- Qwen 官网研究页: https://qwen.ai/research

## 本地落盘文件
- ../../../sources/llm/2026/qwen3.5-omni.pdf
