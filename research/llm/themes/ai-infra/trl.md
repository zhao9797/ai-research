---
title: TRL — Transformer Reinforcement Learning
org: Hugging Face
country: US
date: 2020-03
type: github
categories: [后训练, AI infra]
url: https://github.com/huggingface/trl
github_url: https://github.com/huggingface/trl
downloaded: [trl-readme.md]
---

## 一句话定位
Hugging Face 官方的后训练库，提供 SFT、DPO/变体、PPO、GRPO、Reward Modeling 等 trainer，与 Transformers/PEFT/Accelerate 深度集成，是社区最易上手的对齐/RL 后训练栈。

## 摘要（3-6 句）
TRL（Transformer Reinforcement Learning）把主流后训练方法封装为与 HF Transformers 一致的 Trainer 接口：SFTTrainer、DPOTrainer（及 IPO/KTO/ORPO 等变体）、PPOTrainer、GRPOTrainer、RewardTrainer 等。它借助 Accelerate 支持多 GPU/多节点与 DeepSpeed ZeRO，借助 PEFT 支持 LoRA/QLoRA 低成本训练，并可用 vLLM 加速在线 RL 的生成。它是从单卡到集群、从 SFT 到 RLVR 的通用后训练工具，广泛用于开源模型对齐。

## 关键技术细节
- Trainer：SFT、DPO（+ KTO/IPO/ORPO/CPO 等）、PPO、GRPO、Reward Modeling、Online DPO。
- 集成：Transformers + Accelerate（多卡/DeepSpeed ZeRO/FSDP）+ PEFT（LoRA/QLoRA）+ vLLM（在线 RL 生成加速）。
- 支持量化训练（bitsandbytes）、长上下文、VLM 后训练。
- 与 HF Hub/datasets 无缝；社区对齐与 RLVR 复现的主流入口。

## 原始链接
- url: https://github.com/huggingface/trl
- github_url: https://github.com/huggingface/trl

## 本地落盘文件
- ../../../../sources/llm/themes/ai-infra/trl-readme.md
