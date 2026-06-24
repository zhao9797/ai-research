---
title: "Emu3: Next-Token Prediction is All You Need"
org: 北京智源 (BAAI)
country: 中国
date: 2024-09
type: arxiv
categories: [架构, 预训练数据]
url: https://arxiv.org/abs/2409.18869
pdf_url: https://arxiv.org/pdf/2409.18869
github_url: https://github.com/baaivision/Emu3
downloaded: [files/emu3.pdf]
---

## 一句话定位
智源 Emu3——把图像/文本/视频统一 tokenize 后，仅用单一 Transformer 做 next-token 预测，同时在生成与感知任务上超越任务专用模型，证明"下一 token 预测足矣"。

## 摘要
尽管 next-token prediction 被视为通往 AGI 的路径，但多模态任务仍由扩散模型（如 Stable Diffusion）与组合方法（CLIP+LLM）主导。Emu3 仅用 next-token prediction 训练单一 Transformer：把图像、文本、视频 tokenize 到离散空间，在混合多模态序列上从头训练。Emu3 在生成（文生图）与感知（视觉理解）任务上均超越 SDXL、LLaVA-1.6 等成熟的任务专用模型，无需扩散或组合架构。

## 关键技术细节（带数字）
- 范式：统一 next-token prediction（单一 Transformer Decoder）。
- tokenizer：自训练视觉 tokenizer，把图像/视频离散化为 token，与文本统一词表。
- 训练：在图像/文本/视频混合 token 序列上从头训练。
- 性能：文生图超越 SDXL；视觉理解超越 LLaVA-1.6；支持视频生成与续帧。
- 意义：无需 diffusion / CLIP 组合即达 SOTA，验证 next-token prediction 的多模态潜力。

## 原始链接
- arXiv: https://arxiv.org/abs/2409.18869
- PDF: https://arxiv.org/pdf/2409.18869
- GitHub: https://github.com/baaivision/Emu3

## 本地落盘文件
- ../../../sources/llm/2024/emu3.pdf
