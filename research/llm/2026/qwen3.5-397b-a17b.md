---
title: Qwen3.5-397B-A17B（Qwen3.5 旗舰开源权重模型）
org: 阿里巴巴 Qwen 团队
country: 中国
date: 2026-02
type: model-release
categories: [pretraining, architecture, infra, post-training, agentic, multimodal, moe, linear-attention]
url: https://qwen.ai/blog?id=qwen3.5
pdf_url: https://huggingface.co/Qwen/Qwen3.5-397B-A17B
github_url: https://github.com/QwenLM/Qwen3.5
downloaded: [files/qwen3.5-397b-a17b-modelcard.md, files/qwen3.5-blog.md]
---

# Qwen3.5-397B-A17B

## 一句话定位
阿里 Qwen 2026-02-16 发布的 Qwen3.5 系列首款开源权重旗舰：原生视觉-语言模型，采用「Gated DeltaNet 线性注意力 + 门控全注意力 + 稀疏 MoE」混合架构，3970 亿总参 / 170 亿激活，对标 GPT-5.2 / Claude 4.5 Opus / Gemini-3 Pro。

## 摘要
Qwen3.5 是 Qwen3 的跨代升级，首发模型 Qwen3.5-397B-A17B 为原生多模态（早期文本-视觉融合训练）旗舰。核心卖点：混合高效架构（线性注意力 + MoE）带来高吞吐低成本推理；RL 在「百万级智能体环境」上规模化、强调环境难度与可泛化性而非刷单一指标；语言覆盖从 119 种扩展到 201 种语言/方言；新一代训练基础设施（原生 FP8 流水线 + 异步 RL 框架）。API 托管版为 **Qwen3.5-Plus**（默认 1M 上下文、内置工具、自适应工具调用）。同系列还开源了 122B-A10B、35B-A3B（含 Base）、27B dense、9B、4B、2B、0.8B 等多档（HF createdAt 2026-02-16 ~ 02-28）。Qwen Chat 提供 auto / thinking / fast 三种模式。

> 注：完整训练细节（数据配比、token 量、RL 算法名）官方称将在「即将发布的技术报告」中详述；本页数字均取自官方 model card / config.json / 官方博客已披露内容。

## 关键技术细节（带数字）
来源：官方 HF model card「Model Overview」+ config.json（权威）+ 官方博客「预训练 / 基础设施」章节。

**规模与架构（语言模型部分）**
- 总参数 **397B**，激活参数 **17B**（每次前向）。
- 隐藏维 hidden_size = **4096**；层数 num_hidden_layers = **60**。
- 词表 vocab_size = **248320**（padded，约 25 万，对比 Qwen3 的 ~15 万；官方称在多数语言上带来约 10–60% 编解码效率提升）；tie_word_embeddings = False。
- 精度 dtype = **bfloat16**。
- 上下文：原生 **262,144（256K）**，可扩展至 **1,010,000（~1M）**；max_position_embeddings = 262144。
- 层布局（model card 表述）：15 × [ 3 ×(Gated DeltaNet → MoE) → 1 ×(Gated Attention → MoE) ]，即每 4 层中 3 层线性注意力 + 1 层全注意力。config.json 印证：layer_types 共 60 层 = **45 linear_attention + 15 full_attention**，full_attention_interval = 4。

**Gated DeltaNet（线性注意力层）**
- 线性注意力头数：V 头 **64**，QK 头 **16**（config: linear_num_value_heads=64, linear_num_key_heads=16）。
- 头维 head dim = **128**（linear_key_head_dim=128, linear_value_head_dim=128）。

**Gated Attention（全注意力层）**
- 注意力头：Q **32**，KV **2**（GQA，num_attention_heads=32 / num_key_value_heads=2）。
- 头维 head_dim = **256**；RoPE 维度 **64**；attn_output_gate=true（输出门控）。

**MoE**
- 专家总数 **512**；激活 **10 路由专家 + 1 共享专家**（num_experts=512, num_experts_per_tok=10，另含 1 shared）。
- 专家中间维 expert intermediate dim = **1024**（moe_intermediate_size=1024，shared_expert_intermediate_size=1024）。
- 训练含 **MTP（multi-token prediction，多步）**。

**预训练（官方博客「预训练」三维度）**
- 能力：更大规模视觉-文本语料，加强中英/多语言/STEM/推理数据 + 更严格过滤；Qwen3.5-397B-A17B 与 >1T 参数的 Qwen3-Max-Base 表现相当。
- 效率：基于 **Qwen3-Next 架构**（更高稀疏度 MoE、Gated DeltaNet + Gated Attention 混合、稳定性优化、MTP）。32k/256k 上下文下解码吞吐分别是 Qwen3-Max 的 **8.6× / 19.0×**，是 Qwen3-235B-A22B 的 **3.5× / 7.2×**，性能相当。
- 通用性：早期文本-视觉融合 + 扩展视觉/STEM/视频数据，原生多模态；语言覆盖 119→201。

**基础设施（官方博客「基础设施」）**
- 异构基础设施：视觉与语言组件解耦并行策略；利用稀疏激活实现跨模块计算重叠，混合文本-图像-视频数据下相比纯文本基线达**近 100% 训练吞吐**。
- **原生 FP8 流水线**：对激活、MoE 路由、GEMM 采用低精度，运行时监控对敏感层保留 BF16；约 **50% 激活显存降低**、**>10% 加速**，稳定扩展至**数万亿 token**。
- **异步 RL 框架**：训推分离解耦设计，支持全尺寸模型、文本/多模态/多轮场景；FP8 训推、Rollout 路由回放、投机采样、多轮 Rollout 锁定；端到端 **3×–5× 加速**；可扩展至**百万级 Agent 脚手架与环境**（RL environment scaling 是 Qwen3.5 后训练增益主因，强调环境难度与可泛化性）。

**部分基准（Qwen3.5-397B-A17B vs 前沿，官方博客自然语言表，节选）**
- MMLU-Pro 87.8 / IFBench 76.5（榜首）/ MultiChallenge 67.6（榜首）/ GPQA 88.4 / AIME26 91.3 / SWE-bench Verified 76.4 / BrowseComp 69.0（context-folding）→78.6（discard-all）/ TAU2-Bench 86.7。
- 视觉：MMMU 85.0 / MathVision 88.6（榜首）/ MathVista(mini) 90.3 / AndroidWorld 66.8。

**视觉编码器**（config vision_config）：含 deepstack_visual_indexes、patch_size、spatial_merge_size、temporal_patch_size 等（原生 VLM，image_token_id=248056）。

## 原始链接
- 官方博客（中/英）：https://qwen.ai/blog?id=qwen3.5
- HF 旗舰权重 + model card：https://huggingface.co/Qwen/Qwen3.5-397B-A17B
- HF config.json：https://huggingface.co/Qwen/Qwen3.5-397B-A17B/raw/main/config.json
- GitHub：https://github.com/QwenLM/Qwen3.5
- ModelScope：https://modelscope.cn/models/Qwen/Qwen3.5-397B-A17B

## 一手源存档（sources/）
- files/qwen3.5-397b-a17b-modelcard.md（HF model card 全文，1357 行）
- files/qwen3.5-blog.md（官方博客中文全文，含基准表 / 预训练 / 基础设施章节）
