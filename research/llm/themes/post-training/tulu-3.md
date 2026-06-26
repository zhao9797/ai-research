---
title: "Tulu 3: Pushing Frontiers in Open Language Model Post-Training"
org: AI2 (Allen Institute for AI)
country: US
date: 2024-11
type: report
categories: [后训练]
url: https://arxiv.org/abs/2411.15124
pdf_url: https://arxiv.org/pdf/2411.15124
github_url: https://github.com/allenai/open-instruct
downloaded: [tulu-3.pdf]
---

## 一句话定位
Tulu 3：完全开源的前沿后训练配方，首次系统提出并开源 RLVR（Reinforcement Learning with Verifiable Rewards），确立"SFT → DPO → RLVR"三段式开放后训练标准。

## 摘要（3-6 句）
Tulu 3 是 AI2 完全开放的后训练套件（数据、配方、代码、评测全开源），在 Llama 3.1 基座上建立四阶段流水线：精选 prompt → SFT → 偏好数据上的 DPO → RLVR。最关键创新是 RLVR：对有"可验证答案"的任务（数学、精确指令遵循等），用规则验证答案正确性给二元奖励做 RL（基于 PPO/GRPO），绕开易被 hack 的奖励模型。Tulu 3 8B/70B 超过同规模开放模型，并逼近/超过 Llama 3.1 Instruct、Qwen2.5 Instruct 等闭源后训练模型。论文还给出 decontamination、评测框架与每阶段消融。

## 关键技术细节
- 四阶段：data curation（去污染、技能定向）→ SFT → DPO（on/off-policy 偏好，规模化 UltraFeedback 类数据）→ RLVR。
- RLVR：对可验证任务（GSM8K/MATH、IFEval 风格精确指令）用 verifier 给 0/1 奖励做 RL（PPO/GRPO 实现），只在答案被验证正确时给奖励。
- 数据：开源 Tulu 3 SFT mix、偏好数据、RLVR prompts；强调技能定向数据合成（数学、代码、指令遵循、安全等）。
- 规模：8B 与 70B（基于 Llama 3.1）；后续追加 405B。
- 评测：开源 Tulu 3 Eval 套件（含开发/未见测试集划分以防过拟合）。
- 全开放：权重、数据、训练代码（open-instruct）、评测代码全部公开。

## 原始链接
- url: https://arxiv.org/abs/2411.15124
- pdf_url: https://arxiv.org/pdf/2411.15124
- github_url: https://github.com/allenai/open-instruct

## 一手源存档（sources/）
- tulu-3.pdf  （PDF 不入 git，走 HF bucket）
