---
title: DeepSeek-V3 Technical Report
org: DeepSeek-AI
country: China
date: 2024-12
type: report
categories: [架构, AI infra, 后训练, 预训练数据]
url: https://arxiv.org/abs/2412.19437
pdf_url: https://arxiv.org/pdf/2412.19437
github_url: https://github.com/deepseek-ai/DeepSeek-V3
downloaded: [deepseek-v3-2412.19437.pdf]
---

## 一句话定位
671B 总参 / 37B 激活的 MoE 旗舰，含 MLA、DeepSeekMoE、无辅助损失负载均衡、MTP、FP8 训练、DualPipe，仅用 278.8 万 H800 卡时完成训练，是国产 infra 协同设计的标杆。

## 摘要（3-6 句）
DeepSeek-V3 是 671B 总参、每 token 激活 37B 的 MoE 模型，沿用 V2 验证的 MLA 与 DeepSeekMoE 架构，首创无辅助损失（auxiliary-loss-free）负载均衡与多 token 预测（MTP）目标。在 14.8T 高质量 token 上预训练，再经 SFT 与 RL。其训练以 FP8 混合精度 + DualPipe 双向流水线 + 高效跨节点 all-to-all 完成，总成本仅 2.788M H800 GPU·hr，且全程无不可恢复 loss spike、无回滚。性能比肩闭源头部模型。

## 关键技术细节
- 规模：671B 总参 / 37B 激活；61 层；MoE 含 1 个共享专家 + 256 路由专家、每 token 选 8 个；预训练 14.8T token，上下文先 4K 后扩到 128K（YaRN）。
- 架构：MLA（KV 压缩到低维 latent，省 KV cache）；DeepSeekMoE 细粒度专家 + 共享专家；auxiliary-loss-free 负载均衡（用 bias 调整路由）；MTP 多 token 预测。
- 训练 infra：FP8 混合精度训练（细粒度 tile/block-wise 量化）；DualPipe 双向流水把计算与通信全重叠、减气泡；定制高效 all-to-all + 受限 cross-node EP；2048×H800 集群。
- 成本：预训练 2.664M + 上下文扩展 0.119M + 后训练 0.005M = 2.788M H800 GPU·hr。
- 后训练：从 DeepSeek-R1 蒸馏推理能力到 V3，RL 阶段。

## 原始链接
- url: https://arxiv.org/abs/2412.19437
- pdf_url: https://arxiv.org/pdf/2412.19437
- github_url: https://github.com/deepseek-ai/DeepSeek-V3

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/deepseek-v3-2412.19437.pdf
