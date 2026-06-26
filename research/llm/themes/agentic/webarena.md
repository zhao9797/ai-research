---
title: "WebArena: A Realistic Web Environment for Building Autonomous Agents"
org: "Carnegie Mellon University"
country: US
date: 2023-07
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2307.13854
pdf_url: https://arxiv.org/pdf/2307.13854
github_url: https://github.com/web-arena-x/webarena
downloaded: [webarena-2307.13854.pdf]
---

## 一句话定位
高度真实、可复现的网页 agent 环境：自托管真实功能网站(电商/论坛/Gitlab/CMS/地图)，用 812 个长程任务做执行级(功能正确性)评测，暴露当时 agent 与人类的巨大差距。

## 摘要
WebArena 构建了一个高度真实、可复现的 web agent 评测环境，包含四类常用域的完整功能网站：电子商务(OneStopShop)、社交论坛(Reddit-like)、协作软件开发(GitLab)、内容管理(CMS)，并集成地图、计算器、文档(维基)等工具与知识源。基于此环境，作者标注 812 个真实长程任务(自然语言意图)，并设计基于功能正确性的执行级评测(检验任务是否真正完成，而非文本匹配)。实验显示当时最好的 GPT-4 agent 端到端任务成功率仅 14.41%，远低于人类的 78.24%，凸显 LLM agent 处理真实网页长程任务的不足。

## 关键技术细节
- 环境：自托管的真实可用网站(电商 OneStopShop、论坛、GitLab、CMS) + 地图/计算器/Wiki 等工具，完全可控可复现。
- 任务：812 个长程网页任务，含跨站、多步操作；以"执行结果功能正确性"评测(信息检索类 + 状态改变类)。
- 基线结果：GPT-4 agent 成功率 14.41%；人类 78.24%；GPT-3.5 更低。
- 意义：相对此前 MiniWoB/WebShop 等简化环境，WebArena 更贴近真实网站复杂度，成为 web agent 训练/评测的标准床。
- 衍生：WebArena-Lite(子集，被 WebRL、AutoGLM 等用作训练/评测)。

## 原始链接
- url: https://arxiv.org/abs/2307.13854
- pdf_url: https://arxiv.org/pdf/2307.13854
- github_url: https://github.com/web-arena-x/webarena

## 一手源存档（sources/）
- [webarena-2307.13854.pdf](https://arxiv.org/pdf/2307.13854)  （arXiv 原文 PDF，不入 git）
