---
title: "Nemotron 3 Nano Omni: Efficient and Open Multimodal Intelligence"
org: NVIDIA
country: US
date: 2026-04
type: paper
categories: [架构, AI infra, 后训练, 预训练数据]
url: https://arxiv.org/abs/2604.24954
pdf_url: https://arxiv.org/pdf/2604.24954
github_url:
downloaded: [arxiv-2604.24954.pdf]
---

## 一句话定位
NVIDIA 2026-04 发布的 Nemotron 3 Nano Omni——Nemotron 多模态系列首个原生支持音频（连同文/图/视频）的全模态模型，建立在 Nemotron 3 Nano 30B-A3B backbone 上，强调低延迟高吞吐与 agentic computer use。

## 摘要
Nemotron 3 Nano Omni 是 Nemotron 多模态系列最新模型，也是首个原生支持音频输入（与文本、图像、视频并列）的全模态模型。它在所有模态上较前代 Nemotron Nano V2 VL 一致提升，得益于架构、训练数据与配方的改进；在真实文档理解、长音视频理解、agentic computer use 上领先。构建于高效的 Nemotron 3 Nano 30B-A3B backbone，加上 C-RADIOv4-H1 视觉编码器与 Parakeet-TDT-0.6B-v2 音频编码器，并引入多模态 token 缩减技术显著降低推理延迟、提高吞吐。发布 BF16、FP8、FP4 三种格式的检查点，以及部分训练数据与代码。

## 关键技术细节
- 提交日期：2026-04-27（PDF 标注 2026-5-12）。机构：NVIDIA。
- backbone：Nemotron 3 Nano 30B-A3B（30B 总 / 3B 激活）语言模型。
- 视觉编码器：C-RADIOv4-H1；音频编码器：Parakeet-TDT-0.6B-v2。
- 模态：原生 文本 + 图像 + 视频 + 音频（首次原生音频）。
- 效率：多模态 token-reduction 技术，降低推理延迟、提高吞吐。
- 能力：真实文档理解、长音视频理解、agentic computer use 领先同尺寸模型。
- 发布格式：BF16 / FP8 / FP4 检查点 + 部分训练数据 + 代码（Megatron-Bridge、NeMo-RL、示例数据管线）。

## 原始链接
- url: https://arxiv.org/abs/2604.24954
- pdf_url: https://arxiv.org/pdf/2604.24954

## 本地落盘文件
- ../../../sources/llm/2026/arxiv-2604.24954.pdf
