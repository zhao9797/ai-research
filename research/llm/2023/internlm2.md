---
title: "InternLM2 Technical Report"
org: 上海人工智能实验室（Shanghai AI Laboratory）/ 商汤
country: China
date: 2024-03
type: paper
categories: [预训练数据, 架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2403.17297
pdf_url: https://arxiv.org/pdf/2403.17297
github_url: https://github.com/InternLM/InternLM
downloaded: [internlm2.pdf]
---

## 一句话定位
书生·浦语 InternLM2（1.8B/7B/20B）完整技术报告，详尽披露 InternEvo 训练框架、200K 长上下文、COOL RLHF（条件奖励模型 + 多轮 PPO），是 2023/24 中国大模型 infra 与对齐最透明的一手文档。（2024-03 发布，承接 2023 InternLM 工作。）

## 摘要（3-6 句）
InternLM2 开源 1.8B/7B/20B 三档模型，在 6 大维度 30 项基准、长上下文与开放式生成上超越前代。预训练涵盖文本、代码、长上下文数据：先 4k 后 32k 训练，最终在 200k "大海捞针"测试近乎完美。对齐阶段提出 COOL RLHF（COnditional OnLine RLHF）：用条件奖励模型协调冲突偏好、多轮 PPO 缓解 reward hacking，并同时发布 RLHF 前后（SFT / RLHF）模型。报告详细公开 InternEvo 训练框架与各阶段数据准备方法。

## 关键技术细节
- 规模：1.8B / 7B / 20B；全系采用 GQA 以降低长序列推理显存。
- 预训练数据：约 2.6T tokens（文本 + 代码 + 长文本）。
- 长上下文：预训练先 4k → 转 32k 高质量长文本；GQA 支持 200k 推理；"大海捞针" 200k 近满分；并在 SFT/RLHF 阶段构造 32k 数据。
- infra（InternEvo）：支持数据/张量/序列/流水线并行 + 参数/梯度/优化器状态分片（ZeRO 类）；
  - InternLM-7B 8 卡 4M batch 达 64% MFU；扩到 1024 卡仍保持 53% MFU（同条件 DeepSpeed 约 36%）。
  - 支持 256,000 序列长度训练，InternLM-7B 在 256k 序列下近 88% MFU；可处理百万 token 上下文训练。
  - 通信-计算重叠（AllGather 取下层参数同时算当前层，ReduceScatter/AllReduce 同步梯度）；显存碎片管理；容错 checkpoint（本地存储→冷存储）。
  - 重构 WQKV 矩阵布局以适配张量并行 head 切分，预训练加速 >5%。
- 后训练（COOL RLHF）：Conditional Reward Model（单一奖励模型按系统提示条件化以调和冲突偏好）+ Online RLHF 多轮 PPO（PPO 用 4 个等大模型、训练其中 2 个）以缓解 reward hacking；发布 SFT 与 RLHF 双版本。
- 数据流水线：原始数据标准化为 jsonl → 按类型/语言分类 → 启发式统计规则过滤得 Clean data → 去重/安全过滤。
- agentic：长上下文与 agent 任务联动；配套 InternLM 的 agent 框架（Lagent / AgentFLAN 体系）。

## 原始链接
- url: https://arxiv.org/abs/2403.17297
- pdf_url: https://arxiv.org/pdf/2403.17297
- github_url: https://github.com/InternLM/InternLM

## 一手源存档（sources/）
- internlm2.pdf  （PDF 不入 git，走 HF bucket）
