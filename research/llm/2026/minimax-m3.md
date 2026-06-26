---
title: "MiniMax-M3（原生多模态，1M 上下文，MiniMax Sparse Attention）"
org: MiniMax (稀宇科技)
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练, 预训练数据]
url: https://huggingface.co/MiniMaxAI/MiniMax-M3
pdf_url: https://arxiv.org/abs/2606.13392
github_url: https://github.com/MiniMax-AI/MiniMax-M3
downloaded: [minimax-m3-readme.md, minimax-m3-config.json]
---

## 一句话定位
原生多模态、1M 上下文模型，~428B 总参 / ~23B 激活，用 **MiniMax Sparse Attention (MSA)** 把长上下文效率推到新高（M2 之后迭代；MSA 论文 2606.13392 已在库）。

## 架构（config.json，model_type=minimax_m3_vl）
- hidden 6144；**60 层**；64 注意力头 / 4 KV（GQA），head_dim 128；vocab 200064；上下文 **1M**（1,048,576）；rope_theta 5e6。
- **MoE**：每 token 选 4 专家 + 1 共享（dense_intermediate 12288，shared_intermediate 3072）。

## 预训练数据 / 训练
- **原生多模态**：从第一步起就做 mixed-modality 训练（text/image/video 深度语义融合），而非后接视觉。
- 具体 token 量/算力 card 未披露；方法细节见 MSA 技术报告 arXiv 2606.13392（已落盘 minimax-sparse-attention）。

## 架构创新 / AI infra：MSA（技术报告 2606.13392 全文）
- **机制**：建在 **GQA** 上的 **blockwise 稀疏注意力**，双分支——
  - **Index Branch**（轻量，仅给 GQA 加 2 个投影矩阵）：对 KV 按块打分（max-pooling），**每个 GQA 组独立选 top-k 块**，恒含 local 块（训练稳定）。
  - **Main Branch**：只对选中块做精确块稀疏注意力 → 每 query 注意力代价从 O(N) 降到 O(k·B_k)（固定预算，与序列长解耦）。部署 **B_k=128, k=16**。
- **训练**（top-k 不可导）：用 **KL 对齐 loss** 让 index 分布匹配 Main Branch 在选中 token 上的组平均分布；**Gradient Detach**（stop-grad index 输入，KL 只更新 indexer）+ **Indexer Warmup**（先全注意力两分支再切稀疏，也用于从全注意力 ckpt 转换）+ 强制 Local Block。
- **GPU kernel 协同**：**exp-free TopK**（softmax 序保持 → 跳过 exp）+ per-thread 寄存器 top-k；**KV-outer 稀疏注意力**（按 KV 块聚 query、预排 tile chunking、two-phase combine 无 atomics）；KL loss 的 LSE 融合进前向；动态负载均衡。top-k kernel 比 torch.topk 快 5.1×（128K）。
- **复杂度**：F_MSA = H_kv·d_idx·N²(Index) + 4·H_q·d_h·N·k·B_k(Main)；kB_k≪N 时相对 GQA 的差距随 N 增大。
- **效率**：MSA 论文在 **109B MoE（41 层/3 dense+38 MoE/200K vocab/~109B·6B 激活，3T token 从头训）**上验证，下游与 GQA 持平、**1M 上下文 per-token 注意力算力降 28.4×**，配套 kernel **H800 上 prefill 14.2× / decode 7.6×（vs GQA）**；支持从头训(MSA-PT)与从全注意力 ckpt 近无损转换(MSA-CPT)。
- M3 自身 card 口径：vs **M2** @1M **prefill 9× / decode 15×、per-token 算力 1/20**。GitHub MiniMax-AI/MSA。

## RL / 推理模式
- 三种 thinking 模式：`enabled` / `adaptive`（自动判断是否深思）/ `disabled`（最低延迟）。

## agentic
- 前沿级 long-horizon agentic（coding & cowork 双强）；配套 MiniMax Agent（agent.minimax.io）。

## Benchmark
- 官方 HF card 与 GitHub README 均**只以一张图披露**（figures/benchmark.jpeg，已落盘），无文本表；该图分辨率过高、视觉 OCR 两次均未能可靠读出数值，故此处不抄具体分数以免出错。定位为 frontier-level long-horizon agentic（coding & cowork）；逐项数字以技术报告 arXiv 2606.13392 为准。

## AI infra / 部署
- SGLang / vLLM / Transformers（`minimax_m3_vl`）/ KTransformers / unsloth；推理参数 temp 1.0 / top_p 0.95 / top_k 40；许可 minimax-community。

## 原始链接
- url: https://huggingface.co/MiniMaxAI/MiniMax-M3 · MSA 报告: https://arxiv.org/abs/2606.13392 · github: https://github.com/MiniMax-AI/MSA

## 一手源存档（sources/）
- [minimax-m3-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/minimax-m3-readme.md)
- [minimax-m3-config.json](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/minimax-m3-config.json)
