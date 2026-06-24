---
title: Hunyuan-A13B Technical Report
org: 腾讯混元 (Tencent Hunyuan)
country: China
date: 2025-06
type: report
categories: [架构, 预训练数据, 后训练, agentic训练]
url: https://github.com/Tencent-Hunyuan/Hunyuan-A13B
pdf_url: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan-A13B/main/report/Hunyuan_A13B_Technical_Report.pdf
github_url: https://github.com/Tencent-Hunyuan/Hunyuan-A13B
downloaded: [hunyuan-a13b-report.pdf]
---

## 一句话定位
腾讯混元开源细粒度 MoE：80B 总参 / 13B 激活（A13B），32 层、1 共享 + 64 细粒度专家（每 token 激活 8），20T token 预训练、256K 上下文，支持 fast/slow 双模式思考，四阶段 SFT+RL（GRPO）主打推理与 agent。2025-06 发布。

## 摘要
Hunyuan-A13B 是腾讯混元开源的稀疏 MoE，总参约 80B、每 token 激活约 13B，在保持高性能的同时大幅降低推理成本。预训练用严格过滤、强化 STEM 的 20T token 语料（从中抽取 2500 亿高质量 STEM token），随后经快速退火 + 长上下文阶段把窗口扩到 256K。后训练采用四阶段流程：推理向 SFT → 推理向 RL → 全场景 SFT → 全场景 RL；RL 用 GRPO，结合 outcome reward model（结果验证器，二元奖励）与多领域奖励模型。支持 fast thinking / slow thinking 双模式。base 与 instruct 权重开源。

## 关键技术细节
- 架构（Table 1）：稀疏 MoE；hidden size 4096；32 层；32 attention heads + 8 KV heads（GQA，省 KV cache）；FFN hidden size 3072；1 共享专家（训练时常驻）+ 64 细粒度专门专家，每 token 激活 8 个专门专家；词表 128K（与 Hunyuan-Large 同一 tokenizer）。
- 规模：13B 激活参数 / 80B 总参。
- 预训练：20T tokens；学习率先 warmup 到峰值，在 13.5T token 上以 3e-5 衰减，余下保持最小 LR；退火阶段 300B token 余弦衰减到 8e-6；之后两阶段长上下文（32K → 256K），RoPE alpha 分别设 50（32K）与 1000（256K）。
- 上下文：原生 256K。
- 后训练四阶段：Stage1 Reasoning-oriented SFT → Stage2 Reasoning-oriented RL（GRPO，binary outcome reward + outcome reward model；RL context 24K→32K）→ Stage3 All-Scenarios SFT → Stage4 All-Scenarios RL（多领域奖励模型：文本理解一致性模型、翻译、长上下文幻觉奖励、多语言 GRM、金融/法律/医疗一致性奖励等）。
- 双模式推理：fast thinking（快思考）/ slow thinking（慢思考，CoT 长度可控）。
- 开源：Hunyuan-A13B-Instruct / Pretrain / FP8 量化版本。

## 原始链接
- url: https://github.com/Tencent-Hunyuan/Hunyuan-A13B
- pdf_url: https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan-A13B/main/report/Hunyuan_A13B_Technical_Report.pdf
- github_url: https://github.com/Tencent-Hunyuan/Hunyuan-A13B

## 本地落盘文件
- ../../../sources/llm/2025/hunyuan-a13b-report.pdf
