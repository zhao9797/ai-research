---
title: Zephyr: Direct Distillation of LM Alignment
org: Hugging Face H4
country: EU
date: 2023-10
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2310.16944
pdf_url: https://arxiv.org/pdf/2310.16944
github_url: https://github.com/huggingface/alignment-handbook
downloaded: [zephyr.pdf]
---

## 一句话定位
Zephyr-7B：用"蒸馏式 SFT + 蒸馏式 DPO（dDPO）"在无任何人类标注下对齐 Mistral-7B，确立开源界 SFT→DPO 的标准两段式配方。

## 摘要（3-6 句）
Zephyr 展示纯蒸馏对齐：先用更强教师模型（GPT-4/ChatGPT）生成的对话数据做蒸馏式 SFT（dSFT，基于 UltraChat），再用 GPT-4 偏好标签（UltraFeedback）做蒸馏式 DPO（dDPO），全程不用人类反馈与在线 RL。得到的 Zephyr-7B-β 在 MT-Bench 与 AlpacaEval 上超过同期 7B 模型，部分指标接近 70B Llama-2-Chat。该工作把 DPO 推为开源对齐主流，并催生 HuggingFace alignment-handbook 配方。

## 关键技术细节
- 基座：Mistral-7B。
- dSFT：用 UltraChat（GPT-3.5/4 生成的多轮对话）做监督微调，并清洗噪声样本。
- dDPO：用 UltraFeedback 的 GPT-4 偏好（取最高分为 chosen、随机较低分为 rejected）直接做 DPO，β≈0.1。
- 关键发现：dDPO 几乎不增加额外采样成本即大幅提升对齐；过训练 DPO 反而有害（需早停/监控）。
- 评测：MT-Bench 7.34、AlpacaEval 胜率高，7B 级别 SOTA。
- 配套开源 alignment-handbook，使 SFT+DPO 流程可复现。

## 原始链接
- url: https://arxiv.org/abs/2310.16944
- pdf_url: https://arxiv.org/pdf/2310.16944
- github_url: https://github.com/huggingface/alignment-handbook

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/zephyr.pdf
