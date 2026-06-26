---
title: "Qwen3 Technical Report"
org: Qwen Team, Alibaba Group
country: China
date: 2025-05
type: report
categories: [架构, 后训练, 预训练数据]
url: https://arxiv.org/abs/2505.09388
pdf_url: https://arxiv.org/pdf/2505.09388
github_url: https://github.com/QwenLM/Qwen3
downloaded: [qwen3.pdf]
---

## 一句话定位
Qwen3（2025-05）是 Qwen 第三代，dense + MoE 全谱（0.6B–235B），首创「thinking / non-thinking」统一模型 + thinking budget，并用旗舰蒸馏高效造小模型，119 语言、Apache 2.0。

## 摘要（3-6 句）
Qwen3 涵盖 dense 与 MoE 架构、0.6B 到 235B 参数。核心创新是把「思考模式」（复杂多步推理）和「非思考模式」（快速响应）统一进一个框架，免去在聊天模型与专用推理模型间切换，并可由查询或聊天模板动态切换。它引入 thinking budget 机制，让用户按任务复杂度自适应分配推理算力。通过从旗舰模型蒸馏知识，大幅降低小模型构建成本同时保持竞争力。Qwen3 在代码、数学、agent 等多基准 SOTA，多语言从 Qwen2.5 的 29 种扩到 119 种；全部 Apache 2.0 开放。

## 关键技术细节
- 规模档位：dense 0.6B/1.7B/4B/8B/14B/32B；MoE Qwen3-30B-A3B（30B 总参/3B 激活）与旗舰 Qwen3-235B-A22B（235B 总参/22B 激活）。
- 统一 thinking/non-thinking：单模型两模式，thinking budget 控制思考 token 预算（延迟-性能权衡）。
- 强到弱蒸馏（strong-to-weak distillation）：用旗舰模型蒸馏小模型，比从头 RL 省算力。
- 多语言：119 种语言/方言（Qwen2.5 为 29）。
- 后训练：长 CoT 冷启动 + 推理 RL + 模式融合 + 通用 RL 的多阶段流程。
- 架构沿用 GQA、SwiGLU、RoPE、RMSNorm、QK-Norm。

## 原始链接
- url: https://arxiv.org/abs/2505.09388
- pdf_url: https://arxiv.org/pdf/2505.09388
- github_url: https://github.com/QwenLM/Qwen3

## 一手源存档（sources/）
- qwen3.pdf  （PDF 不入 git，走 HF bucket）
