---
title: "Contrastive Preference Optimization: Pushing the Boundaries of LLM Performance in Machine Translation (CPO)"
org: Johns Hopkins University / Microsoft
country: US
date: 2024-01
type: paper
categories: [后训练]
url: https://arxiv.org/abs/2401.08417
pdf_url: https://arxiv.org/pdf/2401.08417
github_url: https://github.com/fe1ixxu/ALMA
downloaded: [cpo.pdf]
---

## 一句话定位
CPO（Contrastive Preference Optimization）：在机器翻译场景提出的偏好优化方法，针对 SFT 只会"模仿参考译文（含其质量缺陷）"的局限，训练模型主动避免生成"够用但不完美"的译文，用 ALMA-R 仅 22K 平行句就追平/超过 WMT 冠军与 GPT-4。

## 摘要（3-6 句）
作者指出 7B/13B 中等规模 LLM 翻译已有潜力，但即便最强的 13B 翻译模型（如 ALMA）仍不及传统 SOTA 编码器-解码器系统或更大的 GPT-4。论文先剖析 SFT 用于翻译的缺陷：参考数据虽由人类生成，但质量并不完美，SFT 一味模仿参考会把这些缺陷一起学进去。CPO 与 SFT 相反，不是模仿参考，而是训练模型"避免生成够用但不完美的译文"，本质是一种带正则项的对比式偏好损失，被作者论证为对 DPO 的近似但显存/实现更省。把 CPO 应用到 ALMA 模型、仅用 22K 平行句和 12M 可训练参数，得到的 ALMA-R 在 WMT'21/'22/'23 测试集上可匹配或超过 WMT 竞赛冠军与 GPT-4。

## 关键技术细节
- 基座：ALMA 系列（基于 LLaMA-2 的翻译模型），CPO 阶段为偏好微调。
- 训练数据：仅 22K 平行句（preference triplet），可训练参数约 12M（LoRA 量级），成本极低。
- 偏好数据构造：对每个源句采集三方候选（参考译文、GPT-4 译文、模型自采样译文），用参考无关的质量评估器（如 KIWI-XXL / XCOMET 等 reference-free metric）打分，挑出最优(preferred)/最差(dispreferred)构成偏好对——关键洞见是"参考译文不一定是最优"。
- CPO 损失：在 DPO 偏好项基础上加一个对 preferred 译文的 SFT/BC 正则（behavior cloning regularizer），并丢弃 DPO 中需要的参考模型（reference-free 近似），从而省去存第二份 policy 的显存。
- 结果：ALMA-R 在 WMT'21/'22/'23 多语向上匹配或超过 WMT 竞赛获胜系统与 GPT-4；论证 SFT 参考数据的质量天花板可被偏好优化突破。

## 原始链接
- url: https://arxiv.org/abs/2401.08417
- pdf_url: https://arxiv.org/pdf/2401.08417
- github_url: https://github.com/fe1ixxu/ALMA

## 一手源存档（sources/）
- cpo.pdf  （PDF 不入 git，走 HF bucket）
