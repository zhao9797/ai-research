---
title: "UI-TARS: Pioneering Automated GUI Interaction with Native Agents"
org: "字节跳动 (ByteDance Seed) / 清华大学"
country: China
date: 2025-01
type: paper
categories: [架构, 后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2501.12326
pdf_url: https://arxiv.org/pdf/2501.12326
github_url: https://github.com/bytedance/UI-TARS
downloaded: [ui-tars-2501.12326.pdf]
---

## 一句话定位
字节的端到端原生 GUI agent 模型：纯看截图做人类式键鼠操作，靠大规模 GUI 数据 + 统一动作建模 + System-2 推理 + 反思式在线轨迹迭代训练，在 10+ GUI 基准夺 SOTA，超过 GPT-4o/Claude 框架。

## 摘要
UI-TARS 是原生 GUI agent 模型，仅以截图为输入，执行人类式交互(键鼠)。不同于依赖重度包装的商用模型(GPT-4o)+ 专家提示/工作流的 agent 框架，UI-TARS 是端到端模型，且超过这些复杂框架。在 OSWorld 上 50 步得 24.6、15 步得 22.7，超过 Claude(22.0 与 14.9)；在 AndroidWorld 上 46.6，超过 GPT-4o(34.5)。四大创新：① 增强感知(大规模 GUI 截图数据集做上下文理解与精确描述)；② 统一动作建模(跨平台标准化动作空间，大规模动作轨迹做 grounding)；③ System-2 推理(把刻意推理融入多步决策，含任务分解、反思、里程碑识别等多种推理模式)；④ 反思式在线轨迹迭代训练(在数百台虚拟机上自动采集/过滤/反思精炼新轨迹，突破数据瓶颈)。

## 关键技术细节
- 输入/输出：纯截图输入 → 统一动作空间(click/type/drag/hotkey 等，跨 桌面/网页/移动 平台标准化)。
- 训练四支柱：增强感知(海量 GUI 截图+元素标注) / 统一动作建模(大规模动作轨迹做 grounding) / System-2 推理(任务分解、反思思考、里程碑识别) / 迭代反思在线训练(数百 VM 自动收集-过滤-反思-精炼轨迹，reflection tuning)。
- 模型规模：发布 2B / 7B / 72B 版本(基于 Qwen2-VL 系)。
- 基准：OSWorld 24.6(50步)/22.7(15步) > Claude computer use(22.0/14.9)；AndroidWorld 46.6 > GPT-4o 34.5；并在 ScreenSpot、GUI grounding 等 10+ 基准 SOTA。
- 后续：UI-TARS-1.5(2025-04，seed-tars.com/1.5) 进一步用强化学习提升，OSWorld 大幅提高。

## 原始链接
- url: https://arxiv.org/abs/2501.12326
- pdf_url: https://arxiv.org/pdf/2501.12326
- github_url: https://github.com/bytedance/UI-TARS

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/ui-tars-2501.12326.pdf
