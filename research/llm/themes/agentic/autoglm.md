---
title: "AutoGLM: Autonomous Foundation Agents for GUIs"
org: "智谱 AI / 清华大学 (Zhipu / THUDM)"
country: China
date: 2024-10
type: report
categories: [架构, 后训练, agentic训练]
url: https://arxiv.org/abs/2411.00820
pdf_url: https://arxiv.org/pdf/2411.00820
github_url: https://github.com/THUDM/AutoGLM
downloaded: [autoglm-2411.00820.pdf]
---

## 一句话定位
智谱 ChatGLM 家族的 GUI 基础 agent：主张分离"规划"与"grounding"的中间接口设计 + 自进化在线课程 RL 渐进训练，落地为可用的网页/手机自主控制系统。

## 摘要
AutoGLM 是 ChatGLM 家族的新系列，设计为通过 GUI 自主控制数字设备的基础 agent。基础模型擅长获取人类知识，但在动态真实环境的决策上吃力，限制其迈向 AGI。AutoGLM 聚焦 Web 浏览器与手机两个代表性 GUI 场景，构建可交付用户的实用基础 agent 系统。两点关键洞见：① 设计合适的"中间接口(intermediate interface)"对 GUI 控制至关重要——它把规划(planning)与 grounding 行为分离，二者分别需要面向灵活性与精度的优化；② 提出新的渐进训练框架，支持 AutoGLM 的自进化在线课程强化学习(self-evolving online curriculum RL)。评测显示其有效：网页浏览 VAB-WebArena-Lite 成功率 55.2%(二次尝试 59.1%)、OpenTable 任务 96.2%；Android 设备控制 AndroidLab(VAB-Mobile) 36.2%、热门中文 App 常见任务 89.7%。

## 关键技术细节
- 基座：ChatGLM 家族。
- 中间接口设计：把"规划(决定做什么)"与"grounding(把意图映射到屏幕具体操作)"解耦，分别优化灵活性与精度。
- 训练：渐进训练框架 + 自进化在线课程 RL(与 WebRL 同源思路，从失败任务自动生成课程)。
- 结果：VAB-WebArena-Lite 55.2%(retry 59.1%)、OpenTable 96.2%；AndroidLab 36.2%、中文热门 App 89.7%。
- 是智谱"AutoGLM"商用 agent 产品(手机/网页自动化)背后的技术报告。

## 原始链接
- url: https://arxiv.org/abs/2411.00820
- pdf_url: https://arxiv.org/pdf/2411.00820
- github_url: https://github.com/THUDM/AutoGLM

## 本地落盘文件
- ../../../../sources/llm/themes/agentic/autoglm-2411.00820.pdf
