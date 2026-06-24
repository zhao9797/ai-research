---
title: "Qwen2.5-VL Technical Report"
org: Qwen Team, Alibaba Group
country: China
date: 2025-03
type: report
categories: [架构]
url: https://arxiv.org/abs/2502.13923
pdf_url: https://arxiv.org/pdf/2502.13923
github_url: https://github.com/QwenLM/Qwen2.5-VL
downloaded: [qwen2.5-vl.pdf]
---

## 一句话定位
Qwen2.5-VL（2025-03）是 Qwen 视觉语言旗舰，强化精确目标定位、文档/表格结构化解析、小时级长视频理解，引入绝对时间编码与原生分辨率窗口注意力 ViT。

## 摘要（3-6 句）
Qwen2.5-VL 在基础能力与创新功能上大幅提升：增强视觉识别、精确目标定位（bounding box / point）、稳健文档解析、长视频理解。亮点是能用框或点精确定位对象，从发票/表单/表格做结构化数据抽取，并分析图表/版面。为处理复杂输入，引入动态分辨率处理与绝对时间编码，可处理任意尺寸图像和数小时长视频并做秒级事件定位。模型提供 3B/7B/72B 档位。

## 关键技术细节
- ViT 改造：原生动态分辨率 + window attention（多数层用窗口注意力降算力，少数层全局），重训视觉编码器。
- 绝对时间编码（absolute time encoding）：把 M-RoPE 的时间维与视频绝对时间戳对齐，支持小时级视频秒级事件定位。
- 强结构化输出：发票/表单/表格/图表/版面解析，输出结构化数据；精确 grounding（框/点）。
- 规模：3B、7B、72B；72B 多模态基准对标 GPT-4o、Claude-3.5-Sonnet 并多项领先。
- 发布于 2025-03-05。

## 原始链接
- url: https://arxiv.org/abs/2502.13923
- pdf_url: https://arxiv.org/pdf/2502.13923
- github_url: https://github.com/QwenLM/Qwen2.5-VL

## 本地落盘文件
- ../../../../sources/llm/themes/architecture/qwen2.5-vl.pdf
