---
title: "Galactica: A Large Language Model for Science"
org: Meta AI
country: US
date: 2022-11
type: paper
categories: [预训练数据, 架构]
url: https://arxiv.org/abs/2211.09085
pdf_url: https://arxiv.org/pdf/2211.09085
github_url:
downloaded: [galactica.pdf]
---

## 一句话定位
Meta 在精选科学语料上训练的科学专用 LLM，在公式/引用/分子等技术任务上超越 GPT-3/Chinchilla；公开 demo 因幻觉争议三天下线。

## 摘要
科学知识的爆炸式增长使有用洞见难以发现。Galactica 是能存储、组合、推理科学知识的大模型，训练于论文、参考资料、知识库等大规模科学语料。在多项科学任务上超越现有模型：LaTeX 公式 68.2% vs GPT-3 49.0%；数学 MMLU 41.3% vs Chinchilla 35.7%；MATH 20.4% vs PaLM 540B 8.8%；PubMedQA 77.6%、MedMCQA dev 52.9% 均创 SOTA。尽管不在通用语料上训练，仍超过 BLOOM/OPT。

## 关键技术细节
- 模型规模：125M / 1.3B / 6.7B / 30B / 120B 五档，decoder-only Transformer。
- 训练数据：约 1060 亿 token 的高质量科学语料（4800 万篇论文、教科书、知识库、蛋白质序列、化学分子 SMILES 等），强调"质量优于规模"。
- 特殊 token：用 <work> 标记工作记忆/分步计算，[START_REF]/[END_REF] 标记引用，专门 token 处理化学分子、DNA、氨基酸序列。
- 仅训练 4 个 epoch 即可，未见过拟合（高质量小语料可多轮）。
- 公开 demo 上线 3 天后因生成看似权威但错误的科学内容（幻觉）引发争议被撤下，成为 LLM 可信度讨论的标志事件。

## 原始链接
- url: https://arxiv.org/abs/2211.09085
- pdf_url: https://arxiv.org/pdf/2211.09085

## 本地落盘文件
- ../../../sources/llm/2022/galactica.pdf
