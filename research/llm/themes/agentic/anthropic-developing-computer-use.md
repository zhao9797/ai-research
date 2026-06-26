---
title: "Developing a computer use model"
org: Anthropic
country: US
date: 2024-10
type: blog
categories: [后训练, agentic训练]
url: https://www.anthropic.com/news/developing-computer-use
pdf_url:
github_url: https://github.com/anthropics/anthropic-quickstarts
downloaded: [anthropic-developing-computer-use.html]
---

## 一句话定位
Anthropic 官方首发"computer use"能力：Claude 3.5 Sonnet 看屏幕截图、数像素移动光标、点击/键入，像人一样操作任意软件——把"工具使用+多模态"推进到通用计算机操作的前沿。

## 摘要
2024-10-22，Anthropic 宣布最新版 Claude 3.5 Sonnet 能"使用计算机"：在合适软件配置下，按用户指令移动光标、点击屏幕位置、用虚拟键盘输入，模拟人类与电脑的交互方式(公开 beta)。博客分享了研发与安全方面的洞见。该能力建立在此前工具使用与多模态工作之上：操作电脑需要看懂屏幕图像、并推理何时/如何执行操作。训练 Claude 准确"数像素"以正确定位光标是关键。团队发现仅用计算器、文本编辑器等少量简单软件做训练，模型就能快速泛化到更复杂软件，并在遇到障碍时自我纠错重试(训练期出于安全未让模型联网)。

## 关键技术细节
- 模型：Claude 3.5 Sonnet(升级版)，公开 beta；通过 API 提供 computer use 工具。
- 交互方式：输入=屏幕截图(多模态)，输出=光标移动(按像素计数定位)、点击、键盘输入等。
- 关键训练点：让模型准确"数像素"以给出正确鼠标坐标(类比"banana 里有几个 A")。
- 泛化：仅用计算器、文本编辑器等少量简单软件训练即泛化到更多软件；会自我纠错重试。
- 性能：OSWorld 上 Claude 得 14.9%(同类"像人一样看屏幕操作"的模型中最高，次优仅 7.7%)；人类约 70-75%。
- 安全：训练期不让模型联网；强调 prompt injection、滥用等当下风险的缓解。
- 配套开源 quickstart(参考实现的 agent loop + Docker 环境)。

## 原始链接
- url: https://www.anthropic.com/news/developing-computer-use
- github_url: https://github.com/anthropics/anthropic-quickstarts

## 一手源存档（sources/）
- [anthropic-developing-computer-use.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/agentic/anthropic-developing-computer-use.html)
