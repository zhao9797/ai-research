---
title: "WebDancer: Towards Autonomous Information Seeking Agency"
org: "阿里巴巴 通义实验室 (Alibaba Tongyi Lab / Alibaba-NLP)"
country: China
date: 2025-05
type: paper
categories: [后训练, agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2505.22648
pdf_url: https://arxiv.org/pdf/2505.22648
github_url: https://github.com/Alibaba-NLP/DeepResearch
downloaded: [webdancer-2505.22648.pdf]
---

## 一句话定位
通义 DeepResearch 系列之一：给出"数据构造→轨迹采样→SFT 冷启动→RL 泛化"四阶段端到端配方，基于 ReAct 训出能多步深度检索的 web agent，在 GAIA/WebWalkerQA 上表现强。

## 摘要
解决复杂真实问题需要深度信息检索与多步推理。受 Deep Research 类系统启发，WebDancer 从数据中心与训练阶段视角给出构建端到端自主信息检索 agent 的统一范式，四阶段：① 浏览数据构造(browsing data construction)；② 轨迹采样(trajectories sampling)；③ 监督微调做有效冷启动(SFT cold start)；④ 强化学习增强泛化(RL)。该框架实例化为基于 ReAct 的 web agent WebDancer。在 GAIA 与 WebWalkerQA 等高难信息检索基准上表现强劲，验证了该训练范式的有效性，并给出 agent 训练的系统性洞见。

## 关键技术细节
- 范式四阶段：browsing data construction → trajectory sampling → SFT cold start → RL。
- agent 框架：ReAct(思考-动作-观察)，动作含搜索、点击、读取页面等。
- 数据：自动构造高质量浏览/检索轨迹用于冷启动 SFT，再 RL 提升泛化。
- 评测：GAIA、WebWalkerQA(深度网页遍历问答)等。
- 隶属阿里 Alibaba-NLP/DeepResearch(WebAgent) 系列，与 WebWalker、WebSailor 同源。

## 原始链接
- url: https://arxiv.org/abs/2505.22648
- pdf_url: https://arxiv.org/pdf/2505.22648
- github_url: https://github.com/Alibaba-NLP/DeepResearch

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/webdancer-2505.22648.pdf
