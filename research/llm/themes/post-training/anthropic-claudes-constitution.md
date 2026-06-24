---
title: Claude's Constitution
org: Anthropic
country: US
date: 2023-05
type: blog
categories: [后训练]
url: https://www.anthropic.com/news/claudes-constitution
downloaded: [anthropic-claudes-constitution.html]
---

## 一句话定位
Anthropic 官方公布 Claude 所用"宪法"的具体条款来源与设计理念，是 Constitutional AI 在产品（Claude）上落地的一手说明。

## 摘要（3-6 句）
本文公开了训练 Claude 时使用的"宪法"——一组用于指导模型行为、由 AI 反馈对齐（CAI/RLAIF）所依据的自然语言原则。原则取材自《世界人权宣言》、Apple/DeepMind Sparrow 等的服务条款与安全规则、其他实验室的最佳实践，以及 Anthropic 自研原则（如鼓励无害、诚实、避免给出危险信息、尊重非西方视角等）。文章解释了宪法在 CAI 流程中的作用（模型在自我批评-修订与 AI 偏好判断时引用这些原则），以及为何用明确成文的原则比隐式人类标注更透明、可审计、可迭代。

## 关键技术细节
- 宪法来源：世界人权宣言、其他平台信任与安全准则、DeepMind Sparrow 规则、Anthropic 自研原则等的综合。
- 在 CAI 中的角色：监督阶段自我批评-修订与 RL 阶段 AI 偏好判断都以宪法原则为评判依据（对应 arXiv:2212.08073）。
- 设计理念：以明确成文原则替代大量人类无害性标注，提升透明度、可审计性与可迭代性。
- 局限说明：宪法非最终版、会持续修订；不同原则间存在张力需权衡。
- 这是 CAI 学术论文之外的官方产品化一手说明。

## 原始链接
- url: https://www.anthropic.com/news/claudes-constitution

## 本地落盘文件
- ../../../../sources/llm/themes/post-training/anthropic-claudes-constitution.html
