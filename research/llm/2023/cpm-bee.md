---
title: "CPM-Bee: 百亿参数的中英文双语基座大模型（官方 GitHub）"
org: 面壁智能 / 清华 OpenBMB（ModelBest / OpenBMB）
country: China
date: 2023-05
type: github
categories: [预训练数据, 架构, AI infra]
url: https://github.com/OpenBMB/CPM-Bee
pdf_url:
github_url: https://github.com/OpenBMB/CPM-Bee
downloaded: [cpm-bee-readme.md]
---

## 一句话定位
OpenBMB/面壁 CPM-Bee（10B）：完全开源可商用的百亿参数中英双语基座，CPM-Live 训练的第二个里程碑，在超万亿 token 上预训练，配套 OpenBMB 全栈训练/压缩/推理工具，是面壁 MiniCPM 前身体系一手资料。

## 摘要（3-6 句）
CPM-Bee 是完全开源、允许商用的百亿参数中英文基座模型，是 CPM-Live 训练的第二个里程碑。采用 Transformer 自回归架构，在超万亿（trillion）高质量语料上预训练，中英双语表现优异。配套 OpenBMB 大模型系统生态（高性能预训练、适配、压缩、推理工具链）。在 CPM-Bee 基座上微调可获得强对话与工具使用能力，并支持下游领域适配（如 WebCPM 在网络检索序列上适配得复杂问答与上网检索能力）。

## 关键技术细节
- 规模：约 100 亿（10B）参数；中英双语基座。
- 架构：Transformer 自回归（auto-regressive）。
- 数据：超万亿（>1T）高质量语料，经严格筛选、清洗、配比与后处理。
- 训练框架：OpenBMB 全栈工具（BMTrain 高性能训练、BMCook 压缩、BMInf 推理）。
- 工具/对话：在基座上微调得到具对话与工具使用能力的实例模型。
- agentic 衍生：WebCPM（以 CPM-Bee 为基座，在人类网络检索序列化数据上适配，获得复杂问答与上网检索能力）。
- 多模态衍生：VisCPM（2023/06/30，基于 CPM-Bee 的多模态对话与文生图）。
- 体系定位：CPM-Live → CPM-Bee → 后续 MiniCPM（2024-01）的前身脉络。

## 原始链接
- url: https://github.com/OpenBMB/CPM-Bee
- github_url: https://github.com/OpenBMB/CPM-Bee

## 本地落盘文件
- ../../../sources/llm/2023/cpm-bee-readme.md
