---
title: "WizardLM: Empowering Large Language Models to Follow Complex Instructions (Evol-Instruct)"
org: Microsoft / Peking University
country: US
date: 2023-04
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2304.12244
pdf_url: https://arxiv.org/pdf/2304.12244
github_url: https://github.com/nlpxucan/WizardLM
downloaded: [wizardlm-evol-instruct.pdf]
---

## 一句话定位
Evol-Instruct：用 LLM 自动"进化"指令复杂度（深度+广度）来批量合成高难度指令微调数据，是合成指令数据生成的代表性方法。

## 摘要（3-6 句）
WizardLM 提出 Evol-Instruct，用 ChatGPT 等模型把简单指令逐步改写成更复杂的指令：包括深度进化（增加约束、深化、具体化、增加推理步骤、复杂化输入）和广度进化（生成全新主题指令）。通过多轮进化得到大量难度递增、多样化的指令-回答对，用于 SFT。在该数据上微调的 WizardLM 在复杂指令遵循上显著优于同规模基线（如 Alpaca/Vicuna），人类评测中部分场景接近 ChatGPT。该方法成为合成"高质量难指令"数据的标准范式之一。

## 关键技术细节
- Evol-Instruct 算子：深度进化（add constraints / deepening / concretizing / increase reasoning steps / complicate input）+ 广度进化（mutation 产生新指令）。
- 数据规模：从约 5.2 万 Alpaca 种子指令进化出约 25 万条指令数据（含中间多轮）。
- 难度过滤：用 ChatGPT 剔除"进化失败"（信息丢失、无意义、过难无法回答）的样本。
- 训练：在进化数据上对 LLaMA 做 SFT 得 WizardLM；后续衍生 WizardCoder、WizardMath（结合 RLEIF/PRM）。
- 评测：自建难指令评测集 + 人类评测，复杂指令场景胜率高。

## 原始链接
- url: https://arxiv.org/abs/2304.12244
- pdf_url: https://arxiv.org/pdf/2304.12244
- github_url: https://github.com/nlpxucan/WizardLM

## 一手源存档（sources/）
- wizardlm-evol-instruct.pdf  （PDF 不入 git，走 HF bucket）
