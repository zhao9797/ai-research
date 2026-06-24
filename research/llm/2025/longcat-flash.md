---
title: LongCat-Flash Technical Report
org: 美团 (Meituan) LongCat
country: China
date: 2025-09
type: paper
categories: [架构, AI infra, 后训练, agentic训练]
url: https://arxiv.org/abs/2509.01322
pdf_url: https://arxiv.org/pdf/2509.01322
github_url: https://github.com/meituan-longcat/LongCat-Flash-Chat
downloaded: [longcat-flash.pdf]
---

## 一句话定位
美团首个开源大模型：560B MoE，引入"零计算专家"按需动态激活 18.6B–31.3B（均值 27B），Shortcut-connected MoE 扩大计算-通信重叠窗口，主打高效 + agentic。发布 2025-09-01。

## 摘要
LongCat-Flash 是 560B 参数 MoE，兼顾算力效率与高级 agentic 能力。两大创新：(a) Zero-computation Experts（零计算专家），按上下文需求动态分配算力预算，每 token 激活 18.6B–31.3B（平均 27B），优化资源利用；(b) Shortcut-connected MoE，扩大计算-通信重叠窗口，相比同规模模型在推理效率与吞吐上显著提升。开发了综合缩放框架（超参迁移、模型生长初始化、多管齐下稳定性套件、确定性计算）实现稳定可复现训练。

## 关键技术细节
- 架构：560B 总参 MoE；Zero-computation Experts 动态激活 18.6B–31.3B（均值 27B）；Shortcut-connected MoE（ScMoE）扩大计算-通信重叠。
- 缩放框架：hyperparameter transfer + model-growth initialization + 多重稳定性套件 + 确定性计算。
- 训练数据：约 20T+ tokens（30 天内完成训练）。
- 后训练：面向 agentic 能力的多阶段后训练（含 RL、tool use）。
- 开源：GitHub meituan-longcat/LongCat-Flash-Chat。

## 原始链接
- url: https://arxiv.org/abs/2509.01322
- pdf_url: https://arxiv.org/pdf/2509.01322
- github_url: https://github.com/meituan-longcat/LongCat-Flash-Chat

## 本地落盘文件
- ../../../sources/llm/2025/longcat-flash.pdf
