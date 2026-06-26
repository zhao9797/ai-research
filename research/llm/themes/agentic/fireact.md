---
title: "FireAct: Toward Language Agent Fine-tuning"
org: "System2 Research / 剑桥 / 蒙特利尔大学 / Princeton"
country: US
date: 2023-10
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2310.05915
pdf_url: https://arxiv.org/pdf/2310.05915
github_url: https://github.com/anchen1011/FireAct
downloaded: [fireact-2310.05915.pdf]
---

## 一句话定位
系统性论证"微调比 prompt 更能造 agent"：用多任务、多方法(ReAct/CoT/Reflexion)生成的 agent 轨迹微调小模型，显著提升其工具使用与鲁棒性。

## 摘要
当前语言 agent 大多直接用现成 LLM 做 few-shot prompting，FireAct 则探索对 LM 做微调来打造 agent。作者用 GPT-4 在问答任务(配 Google 搜索 API)上生成多样的 ReAct 轨迹，对较小的开源模型(如 Llama-2、GPT-3.5)做微调。核心发现：微调能持续提升 agent 表现；用多种提示方法(ReAct、CoT、Reflexion)与多任务来源混合生成的轨迹微调，能让 agent 学到更丰富、更鲁棒的行为模式（如根据问题难度自适应选择推理路径长度）。FireAct 系统研究了微调数据规模、来源多样性、基座模型大小等因素的影响。

## 关键技术细节
- 微调数据：用 GPT-4 生成 agent 轨迹（HotpotQA 等 QA 任务 + Google 搜索 API），含 ReAct/CoT/Reflexion 多种方法、多数据源。
- 基座：Llama-2 (7B/13B)、GPT-3.5 等小模型微调。
- 关键结论：① 仅微调 500 条 GPT-4 轨迹即可让 Llama-2-7B 的 HotpotQA 表现大幅提升（相对 few-shot prompting）；② 混合多方法/多任务的轨迹比单一来源更能提升鲁棒性与泛化；③ 微调后 agent 对噪声工具反馈更稳健。
- 定位：是"agent fine-tuning"方向的早期系统性研究，与 AgentTuning 同期互补。

## 原始链接
- url: https://arxiv.org/abs/2310.05915
- pdf_url: https://arxiv.org/pdf/2310.05915
- github_url: https://github.com/anchen1011/FireAct

## 一手源存档（sources/）
- [fireact-2310.05915.pdf](https://arxiv.org/pdf/2310.05915)  （arXiv 原文 PDF，不入 git）
