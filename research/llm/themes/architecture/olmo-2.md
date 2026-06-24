---
title: "2 OLMo 2 Furious (OLMo 2 Technical Report)"
org: Allen Institute for AI (Ai2) / University of Washington
country: US
date: 2025-01
type: report
categories: [架构, 预训练数据, 后训练]
url: https://arxiv.org/abs/2501.00656
pdf_url: https://arxiv.org/pdf/2501.00656
github_url: https://github.com/allenai/OLMo
downloaded: [olmo2.pdf]
---

## 一句话定位
OLMo 2 是 Ai2 的完全开放（权重 + 数据 + 代码 + 日志）dense 模型族（7B/13B/32B），引入 reordered norm + QK-norm 稳定训练、两阶段预训练，并用 RLVR 做对齐。

## 摘要（3-6 句）
OLMo 2 是 Ai2 下一代完全开放语言模型，含 7B、13B、32B dense 自回归模型，发布完整训练细节。相比初代 OLMo，OLMo 2 改进了训练稳定性（架构归一化重排 + QK-Norm）、采用两阶段预训练（大规模通用预训练 olmo-mix-1124 + 高质量退火 midtrain dolmino-mix-1124）、以及完整后训练栈（SFT → DPO → RLVR）。在同等算力下，OLMo 2 处于开放模型的帕累托前沿，32B 接近/超过同规模开放权重模型。

## 关键技术细节
- 架构稳定性：RMSNorm 重排（norm 放在子层输出处的 reordered/post-norm 风格）+ QK-Norm（对 Q、K 归一化），防止 loss spike。
- 规模：7B、13B、32B（dense）；32B 为 2025-03 加入（OLMo-2-0325-32B）。
- 两阶段预训练：olmo-mix-1124（预训练）+ dolmino-mix-1124（midtrain/退火，注入高质量数学/代码/指令数据）。
- 后训练：Tülu 3 配方——SFT + DPO + RLVR（Reinforcement Learning with Verifiable Rewards）。
- 完全开放：权重、预训练/退火/后训练数据、训练代码（OLMo-core）、评测（OLMES）、训练日志全开。

## 原始链接
- url: https://arxiv.org/abs/2501.00656
- pdf_url: https://arxiv.org/pdf/2501.00656
- github_url: https://github.com/allenai/OLMo

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/olmo2.pdf
