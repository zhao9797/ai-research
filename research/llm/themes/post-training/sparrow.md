---
title: Improving alignment of dialogue agents via targeted human judgements (Sparrow)
org: Google DeepMind
country: US
date: 2022-09
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2209.14375
pdf_url: https://arxiv.org/pdf/2209.14375
github_url: https://deepmind.google/blog/building-safer-dialogue-agents/
downloaded: [sparrow.pdf, deepmind-sparrow-blog.html]
---

## 一句话定位
DeepMind 的 Sparrow：基于规则（rules）拆分的 RLHF 对话代理，引入"定向人类判断"+ 证据引用，把无害性拆成可独立标注的细粒度规则。

## 摘要（3-6 句）
Sparrow 是一个用 RLHF 训练的信息检索对话代理，核心创新是把对齐目标拆成一组具体"规则"（如不威胁、不冒充人类、不给医疗/财务建议等），让标注者针对单条规则做定向判断，从而获得更精准、更可解释的偏好与违规信号。模型还能从外部检索证据并在回答中引用，支持事实核查。作者训练两类奖励：偏好奖励（Preference RM）和规则违规分类器（Rule RM），联合用于 RL。结果显示 Sparrow 在 78% 情况下给出有证据支持的可信回答，并在对抗探测下违规率显著低于基线。

## 关键技术细节
- 基座：Chinchilla 70B 对话微调。
- 双奖励模型：Preference RM（成对偏好）+ Rule RM（针对约 23 条人写规则的违规判别）。
- 定向人类判断：标注者每次只评估一条规则是否被违反，降低标注歧义、提高对齐精度。
- 检索/证据：模型可调用 Google 搜索，回答附带证据片段与引用。
- RL：A2C/PPO 类策略优化 + KL 惩罚；adversarial probing 由人类红队针对单条规则探测。
- 评测：有证据可信回答率 78%；规则违规率随对抗探测仍维持较低水平。

## 原始链接
- url: https://arxiv.org/abs/2209.14375
- pdf_url: https://arxiv.org/pdf/2209.14375
- blog: https://deepmind.google/blog/building-safer-dialogue-agents/

## 一手源存档（sources/）
- sparrow.pdf  （PDF 不入 git，走 HF bucket）
- [deepmind-sparrow-blog.html](https://github.com/zhao9797/ai-research/blob/main/sources/llm/themes/post-training/deepmind-sparrow-blog.html)
