---
title: "AndroidWorld: A Dynamic Benchmarking Environment for Autonomous Agents"
org: "Google DeepMind / Google Research"
country: US
date: 2024-05
type: paper
categories: [agentic训练, agentic环境与数据]
url: https://arxiv.org/abs/2405.14573
pdf_url: https://arxiv.org/pdf/2405.14573
github_url: https://github.com/google-research/android_world
downloaded: [androidworld-2405.14573.pdf]
---

## 一句话定位
Google 的 Android 移动 GUI agent 评测环境：在真实 Android 模拟器中对 20 个真实 app 的 116 个程序化任务给奖励信号，任务可参数化、用自然语言无限变体表达，是 mobile agent 的标准床。

## 摘要
能控制计算机执行人类任务的自主 agent 可提升生产力与可访问性，但该领域进步需要真实、可复现的基准。AndroidWorld 是一个完整可用的 Android 环境，为跨 20 个真实 Android 应用的 116 个程序化任务提供奖励信号。不同于提供静态测试集的现有交互环境，AndroidWorld 动态构造参数化、可用无限种自然语言方式表达的任务，从而支持在更大、更真实的任务集上测试。为保证可复现，每个任务都有专门的初始化、成功检测与清理逻辑，对设备系统状态进行修改与检查。作者用基线 agent 实验并给出初步结果。

## 关键技术细节
- 环境：真实 Android 模拟器；20 个真实 app(含设置、联系人、日历、Markor、文件管理等)。
- 任务：116 个程序化任务，参数化(同一任务可生成无限自然语言变体)，每任务带 init/success-check/tear-down，检查设备系统状态做执行级判定。
- 奖励信号：可用于训练与评测移动 GUI agent。
- 是 UI-TARS(AndroidWorld 46.6)、各移动 agent 对标的核心基准；与 OSWorld(桌面) 互补。
- 出自 Google(Rawles 等)，与 AndroidControl/AitW 一脉相承。

## 原始链接
- url: https://arxiv.org/abs/2405.14573
- pdf_url: https://arxiv.org/pdf/2405.14573
- github_url: https://github.com/google-research/android_world

## 一手源存档（sources/）
- [androidworld-2405.14573.pdf](https://arxiv.org/pdf/2405.14573)  （arXiv 原文 PDF，不入 git）
