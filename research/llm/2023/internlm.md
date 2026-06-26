---
title: "InternLM: A Multilingual Language Model with Progressively Enhanced Capabilities"
org: 上海人工智能实验室（Shanghai AI Lab）& 商汤（SenseTime），联合港中文/复旦/上交大
country: China
date: 2023-06
type: technical-report
categories: [架构, 预训练数据, AI infra, 后训练]
url: https://github.com/InternLM/InternLM-techreport
pdf_url: https://github.com/InternLM/InternLM-techreport/raw/main/InternLM.pdf
github_url: https://github.com/InternLM/InternLM-techreport
downloaded: [internlm-techreport.pdf, internlm-techreport-readme.md]
---

## 一句话定位
书生·浦语 InternLM 第一代官方技术报告（2023-06）：104B 参数、1.6T token、自研 Uniscale-LLM 训练系统、多阶段渐进式预训练，在 MMLU/AGIEval/C-Eval/GAOKAO 等综合考试上超过开源模型并优于 ChatGPT；是 InternLM2(2024-03) 之前的奠基工作，目录里此前只有 InternLM2，本篇补齐第一代。

## 摘要
报告提出 InternLM——一个 104B 参数的多语言基础语言模型，在 1.6T token 的大规模高质量多语料上以"多阶段渐进式"流程预训练，再经对齐微调以符合人类偏好。为支撑训练，团队自研 Uniscale-LLM 训练系统，可在 2048 张 GPU 上稳定训练 200B+ 参数模型。在 MMLU、AGIEval、C-Eval、GAOKAO-Bench 等面向人类的综合考试基准上，InternLM 不仅显著超过开源模型，还优于 ChatGPT；并在知识理解、阅读理解、数学、代码等多维度取得 SOTA，对中文语言与文化理解尤为突出。

## 关键技术细节
- 参数规模：104B（选择 104B 是为在合理时间内完成 1.6T token 训练）。
- 架构：82 层 Transformer，每层 80 个注意力头（n=82 layers / n=80 heads）。
- 训练数据：1.6T token 多语言高质量语料（网页、书籍、学术论文、代码等子集）。
- Tokenizer：基于 BPE 的词表，65.5K token 词条，全程统一使用。
- 上下文长度：2K（报告坦承相对 GPT-4 的 32K 在长文档理解等维度仍落后）。
- 训练系统 Uniscale-LLM：专为大模型训练定制，可在 2048 GPU 上稳定训练 >200B 参数模型；压力测试下在 1024 GPU 上稳定吞吐 203.6 tokens/gpu/sec，并可近线性扩展到 2048 GPU。
- 多阶段渐进式预训练（Multi-phase Progressive Pretraining）：把训练切成多个阶段，每阶段聚焦某项能力目标；各阶段数据配比与学习设置依据上一阶段与旁支实验经验动态调整；若某阶段未达预期可从该阶段末断点续训。
- 学习率：cosine 调度，每阶段末学习率衰减到峰值的 10%。
- 三大开发阶段：①数据准备（构建大规模高质量语料）②预训练（训练基座）③对齐。
- 对齐三步：
  - SFT：约 5M 条 prompt 的指令数据集做监督微调。
  - 奖励模型（RM）：从 SFT 模型初始化，替换最后投影层用于打分。
  - RLHF：基于 RM 用 PPO 进一步微调；实验证明 RLHF 可降低输出毒性。
- 评测：在 MMLU、AGIEval（含 AGIEval-GK 高考子集）、C-Eval、GAOKAO-Bench 四大综合考试，以及知识问答(TriviaQA/NQ)、阅读理解(RACE)、中文理解(CLUE/FewCLUE)、数学(GSM8K/MATH)、代码(HumanEval/MBPP) 上评测；C-Eval 截至 2023-06-01 排行榜领先。

## 原始链接
- url: https://github.com/InternLM/InternLM-techreport
- pdf_url: https://github.com/InternLM/InternLM-techreport/raw/main/InternLM.pdf
- github_url: https://github.com/InternLM/InternLM-techreport

## 一手源存档（sources/）
- internlm-techreport.pdf  （PDF 不入 git，走 HF bucket）
- [internlm-techreport-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2023/internlm-techreport-readme.md)
