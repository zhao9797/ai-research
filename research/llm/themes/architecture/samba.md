---
title: "Samba: Simple Hybrid State Space Models for Efficient Unlimited Context Language Modeling"
org: Microsoft / University of Illinois Urbana-Champaign
country: US
date: 2024-06
type: paper
categories: [架构]
url: https://arxiv.org/abs/2406.07522
pdf_url: https://arxiv.org/pdf/2406.07522
github_url: https://github.com/microsoft/Samba
downloaded: [samba.pdf]
---

## 一句话定位
Samba 把 Mamba（选择性 SSM）与 Sliding Window Attention（SWA）逐层交错，再配 SwiGLU MLP，构成线性时间、可无限上下文外推的混合架构；3.8B 模型在短上下文基准上反超同配方 Phi-3-mini，并能从 4K 训练长度零样本外推到 1M。

## 摘要（3-6 句）
高效建模无限上下文长期困难：要么二次复杂度、要么外推能力有限。Samba 提出一个简单的混合架构，逐层结合 Mamba（把序列压进固定大小循环状态，提供高效解码骨干）与 SWA（精确召回近期记忆、补足非循环依赖）。Samba 扩到 3.8B 参数、训练 3.2T token；在 4K 长度上预训练，可零样本外推到 1M 长度并改善困惑度（256× 外推比）。在 4K 上指令微调仅 500 步后即可外推到 256K 并在 Passkey Retrieval 上完美召回。作为线性时间模型，128K 提示下吞吐为 GQA Transformer 的 3.73×，生成 64K token 时加速 3.64×。被 ICLR 2025 接收。

## 关键技术细节
- 混合结构：逐层交错 Mamba + SWA + MLP（Samba），与对照的 Mamba-SWA-MLP、Mamba-MLP、纯 Mamba 对比；Samba/Mamba-MLP/Mamba 用 48 层，Mamba-SWA-MLP 用 54 层（均约 1.7B）。
- Mamba 层：选择性 SSM，含 Short Convolution 平滑输入信号，硬件感知并行扫描。
- SWA 层：滑动窗口 w=2048，窗口内用 RoPE（base 频率 10,000），FlashAttention-2 实现；2048 窗口在效率上与 Mamba 训练速度持平。
- MLP 层：全部用 SwiGLU；对 Mamba 与 SWA 捕获的不同信息分别用独立 MLP。Pre-Norm + 残差。
- 规模档位：421M、1.3B、1.7B、3.8B；训练 3.2T token，沿用 Phi-3 数据集与多阶段（multiphase）预训练，并套用 Phi-3-mini 后训练配方得到 Samba-3.8B-IT。
- 性能：Samba-3.8B-IT MMLU 71.9（5-shot）、GSM8K 87.6（8-shot CoT）、HumanEval 62.8（0-shot pass@1），全面超过 Phi-3-mini-4k-instruct。
- 长上下文：4K 预训练 → 1M 零样本外推（Proof-Pile 困惑度改善）；4K 指令微调 500 步 → 256K Passkey 完美召回；移除 RoPE 的 Samba-NoPE 在超训练长度后困惑度爆炸。
- 作者：Liliang Ren、Yang Liu、Yadong Lu、Yelong Shen、Chen Liang、Weizhu Chen。

## 原始链接
- url: https://arxiv.org/abs/2406.07522
- pdf_url: https://arxiv.org/pdf/2406.07522
- github_url: https://github.com/microsoft/Samba

## 一手源存档（sources/）
- samba.pdf  （PDF 不入 git，走 HF bucket）
