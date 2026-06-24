---
title: "DeepSeek-V3 Technical Report"
org: DeepSeek-AI
country: China
date: 2024-12
type: report
categories: [架构, 预训练数据, AI infra, 后训练]
url: https://arxiv.org/abs/2412.19437
pdf_url: https://arxiv.org/pdf/2412.19437
github_url: https://github.com/deepseek-ai/DeepSeek-V3
downloaded: [deepseek-v3.pdf]
---

## 一句话定位
DeepSeek-V3 是 671B 总参/37B 激活的开源 MoE 旗舰，用 MLA + DeepSeekMoE + 无辅助损失负载均衡 + 多 token 预测 (MTP)，并以 FP8 训练在仅 2.788M H800 卡时内完成 14.8T token 预训练。

## 摘要（3-6 句）
DeepSeek-V3 是 671B 总参、每 token 激活 37B 的 MoE 模型。架构沿用 V2 验证过的 MLA 和 DeepSeekMoE，并首创无辅助损失 (auxiliary-loss-free) 的负载均衡策略和多 token 预测 (MTP) 训练目标。预训练 14.8T 高质量多样 token，再做 SFT 与 RL。它性能超过开源模型、接近顶级闭源模型，而全程训练仅需 2.788M H800 GPU 卡时，且训练极稳定——无不可恢复 loss spike、无回滚。

## 关键技术细节
- 规模：671B 总参 / 37B 激活；256 路由专家 + 1 共享专家，每 token 选 8 个路由专家；128K 上下文。
- MLA：KV cache 压缩为低秩潜向量，解耦 RoPE。
- 负载均衡：auxiliary-loss-free（专家 bias 动态调整），避免干扰梯度；辅以序列级极小均衡损失。
- MTP（Multi-Token Prediction）：训练时预测多个后续 token，密化训练信号，并可用于推测解码。
- infra：FP8 混合精度训练；DualPipe 流水并行（计算-通信几乎全重叠）；定制跨节点 all-to-all（用 NVLink+IB）；EP（专家并行）+ PP + DP（ZeRO-1），未用昂贵 TP。
- 训练成本：14.8T token，总计约 2.788M H800 GPU 卡时（含预训练/扩长/后训练）。
- 后训练：从 DeepSeek-R1 蒸馏推理能力 + GRPO 强化学习。

## 原始链接
- url: https://arxiv.org/abs/2412.19437
- pdf_url: https://arxiv.org/pdf/2412.19437
- github_url: https://github.com/deepseek-ai/DeepSeek-V3

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/deepseek-v3.pdf
