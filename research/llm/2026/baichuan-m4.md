---
title: "Baichuan-M4: A Clinical-Grade Medical Agent System for Continuous Care"
org: 百川智能 Baichuan Intelligence
country: China
date: 2026-06
type: paper
categories: [后训练, agentic训练, 架构]
url: https://arxiv.org/abs/2606.08982
pdf_url: https://arxiv.org/pdf/2606.08982
github_url: https://huggingface.co/baichuan-inc
downloaded: [baichuan-m4.pdf]
---

## 一句话定位
百川 Baichuan-M4，临床级医疗 agent 系统，面向"持续照护"而非单轮问答，由 Baichuan-Harness 运行时 + 连续照护 RL 核心推理模型 + 临床工具层三支柱构成。

## 摘要
Baichuan-M4（arXiv 2026-06-08，作者 Aiyuan Yang 等 28 人）是百川智能的临床级医疗大模型，面向连续照护而非单轮医疗问答，构建为协调的医疗 agent 系统，围绕三大支柱：(1) Baichuan-Harness——统一运行时，让 RL 训练与真实部署保持一致，强制 action 约束、工具使用、长期患者记忆与多 agent 协调；(2) 核心推理模型——用连续照护 RL 框架训练，整合 span-level 奖励建模（SPAR++）、推理路径压缩、课程学习、稳定化策略优化；(3) 临床工具层——患者记忆管理、权威循证检索、跨文档/X 光/皮肤科的多模态医疗感知。在跨维度医疗评测套件上在静态医学知识与安全、动态 OSCE 式问诊、长上下文临床记忆、循证检索、医疗文档 OCR、多模态影像等取得领先。前代 Baichuan-M3（arXiv 2026-02）见独立条目。

## 关键技术细节
- **系统定位**：临床级医疗 agent 系统，连续照护（continuous care）而非单轮 QA。
- **支柱1-Baichuan-Harness**：统一运行时，对齐 RL 训练与真实部署；强制 action 约束、工具使用、长期患者记忆、多 agent 协调。
- **支柱2-核心推理模型**：连续照护 RL 框架，含 span-level reward modeling (SPAR++)、reasoning-path compression、课程学习、稳定化策略优化。
- **支柱3-临床工具层**：患者记忆管理、循证检索、多模态医疗感知（文档/X 光/皮肤科）。
- **评测**：静态医学知识与安全、动态 OSCE 问诊、长上下文临床记忆、循证检索、医疗 OCR、多模态影像均领先。
- **前代 Baichuan-M3（arXiv 2602.06570，2026-02）**：医疗增强 LLM，主动信息获取 + 长程推理 + 自适应幻觉抑制；HealthBench/HealthBench-Hallu/ScanBench SOTA，超 GPT-5.2 于临床问诊/咨询/安全；HF baichuan-inc 开源。

## 原始链接
- url: https://arxiv.org/abs/2606.08982
- pdf_url: https://arxiv.org/pdf/2606.08982
- Baichuan-M3: https://arxiv.org/abs/2602.06570 ; https://huggingface.co/collections/baichuan-inc/baichuan-m3

## 一手源存档（sources/）
- baichuan-m4.pdf  （PDF 不入 git，走 HF bucket）
- baichuan-m3.pdf  （PDF 不入 git，走 HF bucket）
