---
title: Generative Language Modeling for Automated Theorem Proving (GPT-f)
org: OpenAI
country: US
date: 2020-09
type: paper
categories: [agentic训练, 后训练]
url: https://arxiv.org/abs/2009.03393
pdf_url: https://arxiv.org/pdf/2009.03393
github_url:
downloaded: [arxiv-2009.03393.pdf]
---

## 一句话定位
GPT-f：用 Transformer 语言模型驱动形式化定理证明器在证明搜索中生成下一步策略，是“语言模型 + 搜索 + 自我迭代（专家迭代）”这类 agentic 推理训练的早期代表，且首次让神经网络给出的证明被 Metamath 形式化库正式收录。

## 摘要（3-6 句）
论文（Polu、Sutskever）将自动定理证明视作语言建模问题，用 GPT 风格的 Transformer 在 Metamath 形式化数学库上学习生成证明步骤，并结合证明搜索（best-first / 树搜索）。模型规模越大、预训练越充分，证明成功率越高。通过迭代地用模型自己找到的新证明再训练（专家迭代 / iterative refinement），性能进一步提升。该系统发现的部分更短证明被 Metamath 主库正式接受。

## 关键技术细节
- 任务形式：把证明步骤序列化为文本，语言模型自回归生成下一条证明策略（proof step），由形式化验证器校验。
- 搜索：模型作为策略/价值给分器，配合 best-first search 进行证明树搜索。
- 规模实验：测试到约 7.74 亿（774M）参数级别的 Transformer，规模越大证明率越高。
- 预训练：在 WebMath（GitHub、arXiv、Math StackExchange 等数学文本）上预训练对形式化证明任务有显著迁移收益。
- 自我迭代：用模型新发现的证明回灌训练集再训练（专家迭代），在 Metamath set.mm 上证明率持续提升。
- 成果：在 Metamath 测试集上达到约 56% 的证明率（论文报告值），并贡献了若干被官方收录的更短证明。

## 原始链接
- url: https://arxiv.org/abs/2009.03393
- pdf_url: https://arxiv.org/pdf/2009.03393

## 一手源存档（sources/）
- [arxiv-2009.03393.pdf](https://arxiv.org/pdf/2009.03393)  （arXiv 原文 PDF，不入 git）
