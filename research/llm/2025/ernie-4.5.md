---
title: ERNIE 4.5 Technical Report
org: 百度 文心 (Baidu ERNIE)
country: China
date: 2025-06
type: report
categories: [架构, 预训练数据, 后训练, AI infra]
url: https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf
pdf_url: https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf
github_url: https://github.com/PaddlePaddle/ERNIE
downloaded: [ernie-4.5-report.pdf]
---

## 一句话定位
百度文心 4.5 系列技术报告：10 个开源变体（含 424B / 47B 激活的文本 MoE、多模态异构 MoE、0.3B 稠密），创新模态隔离路由的异构 MoE，基于飞桨 PaddlePaddle 训练，Apache 2.0。2025-06 开源。

## 摘要
ERNIE 4.5 是百度新一代多模态大模型家族，开源 10 个变体：文本 MoE（最大 424B 总参 / 47B 激活，即 ERNIE-4.5-300B-A47B 的更大配置）、视觉语言 MoE（如 ERNIE-4.5-VL-424B-A47B）、以及 0.3B 稠密模型。核心创新是异构 MoE 结构与模态隔离路由（modality-isolated routing），使文本与视觉专家各自学习又共享底层；基于飞桨 PaddlePaddle 深度学习框架做大规模训练，配套 FP8 混合精度与多维并行。全系 Apache 2.0 开源（HuggingFace baidu / GitHub PaddlePaddle/ERNIE）。

## 关键技术细节
- 模型矩阵：文本 MoE（ERNIE-4.5-300B-A47B：300B 总参 / 47B 激活；以及更大 424B-A47B 配置）、多模态 VL MoE、0.3B dense；共 10 个变体。
- 架构创新：异构 MoE + 模态隔离路由（modality-isolated routing），文本/视觉专家分置 + 共享专家。
- Infra：基于 PaddlePaddle（飞桨）；最大语言模型预训练 MFU 达 47%；FP8 混合精度 + 多维混合并行 + 异构流水；开源工业级开发工具链（多硬件兼容）。
- 后训练：SFT + RLHF/RL（含 UPO/PPO 类）。
- 开源协议：Apache 2.0；HuggingFace baidu 组织 + GitHub PaddlePaddle/ERNIE。

## 原始链接
- url: https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf
- pdf_url: https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf
- github_url: https://github.com/PaddlePaddle/ERNIE
- model card: https://huggingface.co/baidu/ERNIE-4.5-300B-A47B-Base-PT

## 本地落盘文件
- ../../../sources/llm/2025/ernie-4.5-report.pdf
