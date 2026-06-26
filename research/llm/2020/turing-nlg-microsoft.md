---
title: Turing-NLG — A 17-billion-parameter language model by Microsoft
org: Microsoft (Project Turing)
country: US
date: 2020-02
type: blog
categories: [架构, AI infra]
url: https://www.microsoft.com/en-us/research/blog/turing-nlg-a-17-billion-parameter-language-model-by-microsoft/
pdf_url:
github_url: https://github.com/microsoft/DeepSpeed
downloaded: [ms-turing-nlg.html]
---

## 一句话定位
T-NLG（170 亿参数）是 2020-02 时点公开发布的最大语言模型，由 DeepSpeed + ZeRO + NVIDIA Megatron-LM 张量并行联合训练，是大模型工程化（infra 决定模型规模）的标志性案例。

## 摘要（3-6 句）
微软 Project Turing 发布 17B 参数的生成式 Transformer 语言模型 T-NLG，在 WikiText-103 困惑度与 LAMBADA 下一词预测准确率上刷新 SOTA，并在零样本问答、自由文本生成、抽象式摘要等实用任务上表现优异。训练依赖三项突破：NVIDIA DGX-2（InfiniBand 互联）硬件、Megatron-LM 张量切分、以及 DeepSpeed/ZeRO 优化器。ZeRO 使模型并行度从 16 降到 4、每节点 batch 提升 4 倍、训练时间缩短 3 倍，并使原本因注意力头数（28）不被并行度（16）整除而无法运行的模型变得可训练。

## 关键技术细节
- 参数：17B；架构：78 层 Transformer，隐藏维度 4256，注意力头 28 个。
- 训练设置：与 Megatron-LM 相同超参与学习率调度，自回归生成损失，30 万步，batch size 512，序列长度 1024 tokens；FP16 混合精度。
- 学习率：3200 步线性 warmup 到峰值 1.5e-4，随后 50 万步 cosine 衰减。
- 硬件：NVIDIA DGX-2 + InfiniBand；用 DeepSpeed+ZeRO 仅需 256 块 NVIDIA GPU 即可在 batch 512 下训练，而单用 Megatron-LM 需 1024 块。
- 并行：张量切分（tensor slicing）跨 4 块 V100，DeepSpeed ZeRO 把模型并行度从 16 降到 4。
- 任意 >1.3B 参数模型无法放入单张 32GB GPU，必须模型并行。
- 下游：多任务方式在约 400 万条公开摘要样本上微调，ROUGE 对比 PEGASUS；直接式问答只需约 10 万条 QA 三元组即可超越 LSTM 基线。
- 仅向少量学术界用户开放私有 demo（自由生成 / 问答 / 摘要）。

## 原始链接
- url: https://www.microsoft.com/en-us/research/blog/turing-nlg-a-17-billion-parameter-language-model-by-microsoft/
- github_url: https://github.com/microsoft/DeepSpeed

## 一手源存档（sources/）
- [ms-turing-nlg.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2020/ms-turing-nlg.html)
