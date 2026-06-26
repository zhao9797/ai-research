---
title: "RRHF: Rank Responses to Align Language Models with Human Feedback without tears"
org: Alibaba DAMO Academy / Tsinghua University
country: China
date: 2023-04
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2304.05302
pdf_url: https://arxiv.org/pdf/2304.05302
github_url: https://github.com/GanjinZero/RRHF
downloaded: [rrhf.pdf]
---

## 一句话定位
RRHF：用"对候选回复按条件概率打分 + 排序损失对齐人类偏好"的极简对齐范式，训练时只需 1~2 个模型、几乎无需复杂超参，可看作 SFT + 奖励建模的延伸，是 PPO 之外的早期 best-of-n 学习器代表。

## 摘要（3-6 句）
InstructGPT 式 RLHF 分 SFT→RM→PPO 三阶段，但 PPO 对超参敏感、标准实现需要同时维护多个模型（policy/ref/critic/RM），难训也难放大。RRHF 提出新范式：对来自不同来源的采样回复用"条件概率的对数（length-normalized log-prob）"打分，再用排序损失（ranking loss）让这些分数与人类偏好的排序对齐。RRHF 能利用多来源回复——模型自身、其他 LLM、人类专家译文——共同学习排序，训练期只需 1~2 个模型，无需复杂超参即可稳健对齐。论文在 Anthropic HH（Helpful & Harmless）数据集上验证，RRHF 在 RM 打分与人工标注上达到与 PPO 可比的对齐效果；实验表明其性能高度依赖采样质量，本质是一个 best-of-n 学习器。

## 关键技术细节
- 打分函数：对回复 y 的得分 = (1/|y|) Σ log p_π(y_t | x, y_<t)，即长度归一化的条件对数似然，由当前 policy 自身给出。
- 排序损失：对一组候选回复，按奖励模型/人工的偏好顺序，惩罚"打分顺序与偏好顺序不一致"的成对项（pairwise ranking / hinge-style loss）。
- 训练只需 1~2 个模型：相比 PPO 的 4 模型（policy + ref + critic + RM），RRHF 训练时无需 critic、可不维护 reference 模型，显存与工程复杂度大幅下降。
- 数据来源多样：候选回复可来自模型自采样、其他 LLM（如 ChatGPT/Alpaca）、人类专家；用一个 RM 或人工偏好给出排序标签。
- 同时含 SFT 项：对得分最高的回复加 BC/SFT 损失，避免只学排序而退化。
- 评测：在 Anthropic HH 数据集上，按 RM 分数与人工标注，对齐效果与 PPO 可比；性能与采样质量强相关（best-of-n learner）。

## 原始链接
- url: https://arxiv.org/abs/2304.05302
- pdf_url: https://arxiv.org/pdf/2304.05302
- github_url: https://github.com/GanjinZero/RRHF

## 一手源存档（sources/）
- rrhf.pdf  （PDF 不入 git，走 HF bucket）
