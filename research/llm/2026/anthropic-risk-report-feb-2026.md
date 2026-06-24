---
title: "Risk Report: February 2026"
org: Anthropic
country: US
date: 2026-02
type: report
categories: [后训练, agentic训练]
url: https://www.anthropic.com/feb-2026-risk-report
pdf_url: https://www-cdn.anthropic.com/097c63b5fe7dd8b14866e1f15bb1910ec713658a.pdf
github_url:
downloaded: [anthropic-feb-2026-risk-report.pdf]
---

## 一句话定位
Anthropic 2026 年 2 月发布的"风险报告"（105 页，2026-05-26 更新），系统论证当前前沿模型在自主性威胁模型（破坏/sabotage）下的对齐评估、奖励黑客缓解与可解释性证据，是配合 Opus 4.6 部署的官方安全评估文档。

## 摘要
该报告以"主张-证据"结构评估前沿 AI 模型在自主性(autonomy)风险下的安全状况，第一大威胁模型为 Sabotage（破坏）。它给出预部署对齐发现：无危险的连贯错位目标、有限的上下文相关错位、低污染/Goodhart 风险；并评估模型破坏对齐评估的能力（评估意识与真实性、sabotage 能力与隐写、推理忠实性、模型有机体演练、探索性可解释性调查、共谋机会有限）以及不透明推理/agentic 能力（长周期软件任务能力有限、sandbagging 风险）。报告详述风险缓解：安全/监控/防护、对复杂计划与上下文相关错位传播的约束。报告还讨论奖励黑客(reward hacking)管理——包括对最高风险设置使用 inoculation prompting，以及用新可视化工具（含嵌入式 AI 协助）暴露 prompt 与 reward 不匹配供研究员关注。

## 关键技术细节
- 发布：2026-02（封面 "Risk Report: February 2026"；页面注明 Updated 2026-05-26）。105 页。机构：Anthropic。
- 威胁模型：Autonomy threat model 1 = Sabotage（破坏）；以 4 个 Claim 组织论证。
- 对齐评估发现：无危险连贯错位目标、上下文相关错位有限、低污染/Goodhart 风险。
- 评估稳健性证据：评估意识(evaluation awareness)与真实性、sabotage 能力与隐写(steganography)评估、推理忠实性、model organism 演练、探索性可解释性、共谋机会有限。
- 能力上限论证：不透明推理能力有限、长周期软件任务能力有限、sandbagging 风险讨论。
- 缓解：security/monitoring/safeguards；约束复杂计划与上下文相关错位的传播。
- 奖励黑客：最高风险设置用 inoculation prompting；新可视化工具（含 AI 协助）暴露 prompt-reward 不匹配。

## 原始链接
- url: https://www.anthropic.com/feb-2026-risk-report
- pdf_url: https://www-cdn.anthropic.com/097c63b5fe7dd8b14866e1f15bb1910ec713658a.pdf

## 本地落盘文件
- ../../../sources/llm/2026/anthropic-feb-2026-risk-report.pdf
