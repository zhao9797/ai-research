---
title: "RoFormer: Enhanced Transformer with Rotary Position Embedding"
org: Zhuiyi Technology (追一科技)
country: China
date: 2021-04
type: paper
categories: [架构]
url: https://arxiv.org/abs/2104.09864
pdf_url: https://arxiv.org/pdf/2104.09864
github_url: https://github.com/ZhuiyiTechnology/roformer
downloaded: [rope.pdf]
---

## 一句话定位
提出 Rotary Position Embedding (RoPE)，用旋转矩阵把绝对位置编码进 Q/K，使内积自然携带相对位置信息，成为后续几乎所有主流 LLM（LLaMA、Qwen、DeepSeek、GLM 等）的默认位置编码。

## 摘要（3-6 句）
论文系统对比了多种把位置信息注入 Transformer 的方法，提出 RoPE：用一个与位置相关的旋转矩阵作用于每一对维度，把绝对位置编码进 query 和 key 向量。由于旋转矩阵的性质，两个 token 的注意力内积只依赖它们的相对位置差，从而把绝对位置编码与相对位置依赖统一起来。RoPE 具备序列长度灵活、随相对距离衰减的 inter-token 依赖、且可用于线性注意力等优点。作者在长文本分类基准上验证 RoFormer 持续优于替代方案，并给出理论分析。

## 关键技术细节
- 核心机制：将隐维度两两分组，每组按角度 θ_i = 10000^(-2i/d) 旋转，旋转角度正比于 token 位置 m，即对 query/key 施加 R_Θ,m。
- 关键性质：⟨R_Θ,m q, R_Θ,n k⟩ 只依赖 (m−n)，因此注意力分数天然包含相对位置；这是 RoPE 兼容相对位置编码同时保留绝对位置形式的根本原因。
- 优点：长度外推灵活；远距离 token 依赖随相对距离衰减；可与线性自注意力结合（不像可学习绝对位置嵌入）。
- 已被 HuggingFace 集成；后续大量长上下文扩展工作（NTK、YaRN、位置插值）均基于 RoPE 的频率结构。
- 作者：苏剑林 (Jianlin Su) 等，追一科技，深圳。

## 原始链接
- url: https://arxiv.org/abs/2104.09864
- pdf_url: https://arxiv.org/pdf/2104.09864
- github_url: https://github.com/ZhuiyiTechnology/roformer

## 一手源存档（sources/）
- rope.pdf  （PDF 不入 git，走 HF bucket）
