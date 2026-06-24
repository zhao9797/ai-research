---
title: "DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence"
org: DeepSeek (深度求索)
country: China
date: 2026-04
type: report
categories: [架构, AI infra, 后训练, 预训练数据]
url: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro
pdf_url: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf
github_url: https://github.com/deepseek-ai
downloaded: [deepseek-v4-technical-report.pdf, deepseek-v4-pro-modelcard.md]
---

## 一句话定位
DeepSeek 2026 上半年旗舰预览版 MoE 大模型，主打"百万 token 长上下文 + 极致推理效率"，含 1.6T 的 V4-Pro 与 284B 的 V4-Flash 两个规格，全部支持 1M 上下文。

## 摘要
DeepSeek-V4 系列是 DeepSeek 发布的预览版（preview）旗舰模型，包含两款 MoE 语言模型：DeepSeek-V4-Pro（1.6T 总参 / 49B 激活）与 DeepSeek-V4-Flash（284B 总参 / 13B 激活），均支持 100 万 token 上下文。其核心是混合注意力架构（CSA + HCA）、流形约束超连接（mHC）与 Muon 优化器，在 1M 上下文下相比 V3.2 仅需约 27% 的单 token 推理 FLOPs 和 10% 的 KV cache。两款模型均在 32T+ token 上预训练，后训练采用"领域专家独立培养 + on-policy 蒸馏统一整合"的两阶段范式。模型卡（HF deepseek-ai 官方组织，135k 关注）createdAt 为 2026-04-22。

## 关键技术细节
- **规格**：DeepSeek-V4-Pro 1.6T 总参 / 49B 激活；DeepSeek-V4-Flash 284B 总参 / 13B 激活；对比 DeepSeek-V3.2 为 671B/37B。
- **上下文**：两款均原生支持 1,000,000 token。
- **架构-混合注意力**：Compressed Sparse Attention (CSA) + Heavily Compressed Attention (HCA)，1M 上下文下 V4-Pro 仅需 ~27% 单 token 推理 FLOPs、~10% KV cache（相对 V3.2）。
- **架构-mHC**：Manifold-Constrained Hyper-Connections（流形约束超连接），增强残差信号跨层传播稳定性。
- **优化器**：采用 Muon optimizer（更快收敛 + 训练稳定性）。
- **预训练数据**：32T+ 多样高质量 token。
- **精度**：Base 为 FP8 Mixed；Instruct（Pro/Flash）为 FP4 + FP8 Mixed（MoE 专家参数用 FP4，其余多数 FP8）。
- **后训练**：两阶段范式——(1) 领域专家独立培养，通过 SFT + RL（GRPO）；(2) 通过 on-policy distillation 统一整合为单一模型。
- **推理档位**：Pro/Flash 各支持三档 reasoning effort 模式；最大档位 DeepSeek-V4-Pro-Max 自称"当前最强开源模型"。
- **基座评测（节选）**：MMLU 90.1 / MMLU-Pro 73.5 / C-Eval 93.1（V4-Pro-Base，对比 V3.2-Base 87.8 / 65.5 / 90.4）；SimpleQA-verified 55.2（vs V3.2 28.3）；FACTS Parametric 62.6（vs 27.1）；LongBench-V2 51.5（vs 40.2）。
- **发布矩阵**：Base 与 Instruct 各自的 Pro/Flash 共 4 个权重，HuggingFace + ModelScope 同步开源，MIT 许可。

## 原始链接
- url: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro
- pdf_url: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf
- github_url: https://github.com/deepseek-ai

## 本地落盘文件
- ../../../sources/llm/2026/deepseek-v4-technical-report.pdf
- ../../../sources/llm/2026/deepseek-v4-pro-modelcard.md
