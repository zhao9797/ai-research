---
title: ZeRO & DeepSpeed — New system optimizations enable training models with over 100 billion parameters
org: Microsoft
country: US
date: 2020-02
type: blog
categories: [AI infra]
url: https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/
pdf_url: https://arxiv.org/abs/1910.02054
github_url: https://github.com/microsoft/DeepSpeed
downloaded: [ms-zero-deepspeed.html]
---

## 一句话定位
DeepSpeed 开源库与 ZeRO（Zero Redundancy Optimizer）发布：通过把优化器状态/梯度/参数在数据并行进程间分片而非复制，把可训练模型规模推到 1000 亿参数级别，是现代大模型分布式训练的核心 infra。

## 摘要（3-6 句）
微软 2020-02 开源 DeepSpeed（兼容 PyTorch），其核心 ZeRO 是一种新的并行优化器，通过消除数据并行中模型状态的内存冗余，大幅降低显存占用并提升吞吐。ZeRO 可在当代 GPU 集群上以 3-5 倍吞吐训练 1000 亿参数模型，并给出训练万亿参数的清晰路径。博客分三个累进优化阶段（Pos、Pos+g、Pos+g+p）说明显存节省与通信量权衡，并报告了相对 Megatron-LM 的实测加速。首发实现了 ZeRO stage-1（ZeRO-OS）。

## 关键技术细节
- ZeRO 三阶段（累进启用）：
  - Stage 1 优化器状态分片（Pos）：显存降 4 倍，通信量与数据并行相同。
  - Stage 2 + 梯度分片（Pos+g）：显存降 8 倍，通信量不变。
  - Stage 3 + 参数分片（Pos+g+p）：显存随数据并行度 Nd 线性下降（如 64 GPU 降 64 倍），通信量增加约 50%。
- 首发实现 stage-1（ZeRO-OS），已验证支持 100B 参数模型。
- 万亿参数估算：1T 参数 + Adam(FP16) 约需 16TB 显存；16TB/1024 = 16GB/GPU，可在 1024 块 GPU 上训练。
- 实测加速：低带宽互联（无 NVLink/InfiniBand）下 1.5B GPT-2 相比单用 Megatron-LM 提升 3.75 倍吞吐；DGX-2 高带宽下 20-80B 模型快 3-5 倍。
- 对比基准：GPT-2(1.5B)、Megatron-LM(8.3B)、T5(11B)；ZeRO stage-1 支持到 100B（约 10 倍）。
- 单用 Megatron 跨节点扩展性差：40B 参数跨 DGX-2 节点仅约 5 TFLOPS/GPU。
- 易用性：几行代码改动即可接入；不限制注意力头数/隐藏维度/batch；6B 参数以下可仅用 ZeRO 数据并行（标准数据并行 >1.3B 即 OOM）。
- 配套训练出 Turing-NLG（17B）。

## 原始链接
- url: https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/
- pdf_url (ZeRO 论文): https://arxiv.org/abs/1910.02054
- github_url: https://github.com/microsoft/DeepSpeed

## 本地落盘文件
- ../../../sources/llm/2020/ms-zero-deepspeed.html
