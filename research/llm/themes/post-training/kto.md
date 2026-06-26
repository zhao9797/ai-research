---
title: "KTO: Model Alignment as Prospect Theoretic Optimization"
org: Stanford / Contextual AI
country: US
date: 2024-02
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2402.01306
pdf_url: https://arxiv.org/pdf/2402.01306
github_url: https://github.com/ContextualAI/HALOs
downloaded: [kto.pdf]
---

## 一句话定位
KTO（Kahneman-Tversky Optimization）：把前景理论的人类损失厌恶引入对齐，只需"单条样本好/坏"的二元信号即可训练，无需成对偏好。

## 摘要（3-6 句）
作者提出 HALOs（human-aware losses）框架，指出 DPO/PPO 等隐含人类效用模型，可由前景理论（Kahneman-Tversky）统一解释。基于此提出 KTO：直接最大化"生成的人类效用"，只需要每条样本被标为可取（desirable）或不可取（undesirable）的二元标签，而非成对偏好对。KTO 在 1B–30B 规模上匹配或超过 DPO，且对类别不平衡鲁棒、数据更易获得（真实场景中点赞/点踩这类二元反馈远多于成对偏好）。

## 关键技术细节
- 理论：HALOs 框架将对齐损失写成"价值函数 v + 参考点"的形式，DPO/PPO 为其特例。
- KTO 损失：基于 KT 价值函数（对增益/损失非对称、损失厌恶），对 desirable 样本奖励其相对参考点的对数比，对 undesirable 样本惩罚，参考点用 batch 内 KL 估计。
- 数据形态：每条 (x, y, 好/坏) 二元标签即可，无需 (chosen, rejected) 配对。
- 鲁棒性：对正负样本比例不均衡、噪声更稳健；可超采样稀缺类别（λ_D/λ_U 权重）。
- 结果：在多规模上与 DPO 相当或更优；尤其适合工业界海量单边反馈数据。

## 原始链接
- url: https://arxiv.org/abs/2402.01306
- pdf_url: https://arxiv.org/pdf/2402.01306
- github_url: https://github.com/ContextualAI/HALOs

## 一手源存档（sources/）
- kto.pdf  （PDF 不入 git，走 HF bucket）
