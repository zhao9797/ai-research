---
title: "Ziya-Visual: Bilingual Large Vision-Language Model via Multi-Task Instruction Tuning"
org: 智源 IDEA 研究院 · 封神榜（IDEA / Fengshenbang）
country: China
date: 2023-10
type: paper
categories: [架构, 后训练]
url: https://arxiv.org/abs/2310.08166
pdf_url: https://arxiv.org/pdf/2310.08166
github_url: https://github.com/IDEA-CCNL/Fengshenbang-LM
downloaded: [ziya-visual.pdf]
---

## 一句话定位
IDEA 研究院封神榜 Ziya-Visual：面向中英双语的视觉语言模型，用多任务指令微调把视觉语义注入 LLM，弥补非英文多模态资源不足，是封神榜体系 2023 多模态一手论文。

## 摘要（3-6 句）
现有多模态成功多限于英文场景，因缺乏大规模高质量非英文多模态资源。Ziya-Visual 系列（Ziya-Visual-Base / Ziya-Visual-Chat）是双语大型视觉语言模型，将视觉语义融入 LLM 以支持多模态对话。模型采用 BLIP-2 的 Querying Transformer（Q-Former），并探索可学习指令的辅助作用，通过多任务指令微调提升中英双语视觉理解。

## 关键技术细节
- 基座：封神榜 Ziya-LLaMA 13B 语言模型 + 视觉编码器，桥接采用 BLIP-2 的 Q-Former。
- 数据工程：用翻译 + in-context learning（GPT 辅助）构造大规模中文图文指令数据，弥补中文多模态数据缺口。
- 多任务指令微调：图像描述、VQA、视觉对话等多任务联合，含可学习指令 token。
- 子模型：Ziya-Visual-Base（预训练对齐）+ Ziya-Visual-Chat（指令微调对话）。
- 双语能力：在中英多模态基准上表现优于同期纯英文导向 VLM 在中文场景的迁移。

## 原始链接
- url: https://arxiv.org/abs/2310.08166
- pdf_url: https://arxiv.org/pdf/2310.08166
- github_url: https://github.com/IDEA-CCNL/Fengshenbang-LM

## 本地落盘文件
- ../../../sources/llm/2023/ziya-visual.pdf
