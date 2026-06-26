---
title: "DeepSeek-V3 Technical Report"
org: DeepSeek-AI
country: 中国
date: 2024-12
type: arxiv
categories: [架构, AI infra, 预训练数据, 后训练]
url: https://arxiv.org/abs/2412.19437
pdf_url: https://arxiv.org/pdf/2412.19437
github_url: https://github.com/deepseek-ai/DeepSeek-V3
downloaded: [files/deepseek-v3.pdf]
---

## 一句话定位
671B 总参 / 37B 激活的开源 MoE 旗舰，首创 auxiliary-loss-free 负载均衡 + 多 token 预测（MTP），并以 FP8 + DualPipe 把全程训练压到 2.788M H800 GPU 小时。

## 摘要
DeepSeek-V3 是 671B 总参、每 token 激活 37B 的 MoE 模型，沿用 V2 验证过的 MLA 与 DeepSeekMoE，并新增两项创新：无辅助损失（auxiliary-loss-free）的负载均衡策略，以及多 token 预测（multi-token prediction, MTP）训练目标。在 14.8T 多样高质 token 上预训练，随后 SFT + RL。性能超越所有开源模型，比肩顶级闭源模型（GPT-4o、Claude-3.5-Sonnet）。全程训练仅需 2.788M H800 GPU 小时，且训练极其稳定（无不可恢复 loss spike、无 rollback）。

## 关键技术细节（带数字）
- 规模：671B 总参，37B 激活/token；61 层 Transformer，每层 DeepSeekMoE（1 shared expert + 256 routed experts，每 token 激活 8 个 routed）。
- 注意力：MLA（low-rank KV 压缩）。
- 负载均衡：auxiliary-loss-free 策略（用偏置项动态调节，避免辅助损失损害性能）。
- 训练目标：multi-token prediction（MTP）。
- 训练数据：14.8T tokens。
- 算力：2.788M H800 GPU 小时（pre-training 2.664M + context extension 0.119M + post-training 0.005M）。
- Infra：FP8 混合精度训练；DualPipe 流水线并行 + 跨节点 all-to-all 通信优化；显存极致优化。
- 基准：MMLU 88.5、MMLU-Pro 75.9、GPQA 59.1；从 DeepSeek-R1 蒸馏推理能力。
- 后训练：SFT + RL。

## 原始链接
- arXiv: https://arxiv.org/abs/2412.19437
- PDF: https://arxiv.org/pdf/2412.19437
- GitHub: https://github.com/deepseek-ai/DeepSeek-V3

## 一手源存档（sources/）
- deepseek-v3.pdf  （PDF 不入 git，走 HF bucket）
