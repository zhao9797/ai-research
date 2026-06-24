---
title: "AgentTuning: Enabling Generalized Agent Abilities for LLMs"
org: 智谱AI / 清华 KEG（Zhipu AI / Tsinghua）
country: China
date: 2023-10
type: paper
categories: [后训练, agentic训练]
url: https://arxiv.org/abs/2310.12823
pdf_url: https://arxiv.org/pdf/2310.12823
github_url: https://github.com/THUDM/AgentTuning
downloaded: [agenttuning.pdf]
---

## 一句话定位
智谱/清华 AgentTuning：用 AgentInstruct 交互轨迹数据集 + 混合指令微调，在不损害通用能力的前提下显著提升 LLM 的 agent 能力，是中国 agentic 训练的代表性一手论文。

## 摘要（3-6 句）
开源 LLM 在通用任务上表现好，但作为 agent 处理真实复杂任务时远逊于 GPT-4。已有方法多是为特定 agent 任务设计 prompt，缺乏从模型本身提升 agent 能力（且不损害通用能力）的研究。AgentTuning 提出轻量指令微调方法：构建 AgentInstruct（含 CoT 推理轨迹的高质量多任务交互数据集），并采用"agent 轨迹数据 + 通用指令数据"的混合微调策略，得到 AgentLM（基于 Llama2）。AgentLM 在未见 agent 任务上泛化强，同时保持通用能力。

## 关键技术细节
- AgentInstruct 数据集：覆盖 6 类 agent 任务、1866 条经验证的高质量交互轨迹（含 ReAct 式 CoT 推理）；由 GPT-4 生成 + 自检/人验筛选。
- 混合微调（hybrid instruction-tuning）：将 AgentInstruct 与通用领域指令（ShareGPT 等）混合，平衡专精 agent 能力与通用对话能力。
- 模型：AgentLM-7B/13B/70B，基于 Llama2-Chat 微调。
- 评测：在 AgentBench 的 held-out（未训练）agent 任务上显著提升，泛化到全新环境；通用 NLP 基准（MMLU 等）不退化。
- 关键发现：少量高质量 agent 轨迹 + 通用数据混合，即可"解锁"开源模型潜在 agent 能力，接近 GPT-3.5。

## 原始链接
- url: https://arxiv.org/abs/2310.12823
- pdf_url: https://arxiv.org/pdf/2310.12823
- github_url: https://github.com/THUDM/AgentTuning

## 本地落盘文件
- ../../../sources/llm/2023/agenttuning.pdf
