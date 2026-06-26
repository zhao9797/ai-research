---
title: "OS-Genesis: Automating GUI Agent Trajectory Construction via Reverse Task Synthesis"
org: "上海AI实验室 / 香港大学 / 上海交大 / MMLab(港中文) 等"
country: China
date: 2024-12
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2412.19723
pdf_url: https://arxiv.org/pdf/2412.19723
github_url: https://github.com/OS-Copilot/OS-Genesis
downloaded: [os-genesis-2412.19723.pdf]
---

## 一句话定位
解决 GUI agent 训练数据瓶颈：反转传统采集流程——先无目标交互、再"逆向合成任务"，自动产出高质量多样化 GUI 轨迹，无需人工或预定义任务。

## 摘要
VLM 驱动的 GUI agent 已展现类人电脑控制能力，但训练的关键瓶颈是高质量轨迹数据采集。常见做法依赖人类监督或执行预定义任务的合成数据，要么耗资源、要么无法保证质量，且数据多样性有限、合成数据与真实环境差距大。OS-Genesis 提出一种新颖的 GUI 数据合成管线，反转传统轨迹采集：不依赖预定义任务再采轨迹，而是让 agent 先感知环境、执行逐步交互，再回溯地(retrospectively) 导出高质量任务，触发轨迹级别的探索("reverse task synthesis")。再用轨迹奖励模型保证生成轨迹质量。用 OS-Genesis 合成的数据训练 GUI agent，在 AndroidWorld、AndroidControl、WebArena 等基准上显著优于现有合成方法。

## 关键技术细节
- 核心思想 reverse task synthesis：先让 agent 在 GUI 中自由交互(action-first)，再据交互结果反向构造"对应的任务指令"，从而自动得到 (任务, 轨迹) 对。
- 质量控制：轨迹奖励模型(trajectory reward model) 对合成轨迹打分筛选。
- 优势：相比"预定义任务→采轨迹"，多样性更高、与真实环境差距更小、无需人工标注。
- 评测：在 AndroidWorld、AndroidControl、WebArena 上训练 agent，远超此前合成数据方法。
- 出自上海 AI Lab / 港大 OS-Copilot 团队。

## 原始链接
- url: https://arxiv.org/abs/2412.19723
- pdf_url: https://arxiv.org/pdf/2412.19723
- github_url: https://github.com/OS-Copilot/OS-Genesis

## 一手源存档（sources/）
- [os-genesis-2412.19723.pdf](https://arxiv.org/pdf/2412.19723)  （arXiv 原文 PDF，不入 git）
