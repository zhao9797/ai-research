---
title: "<Work title — quote it if it contains a colon>"
org: <Organization>
country: <US | China | Europe | ...>
date: "YYYY-MM"
type: <paper | tech-report | blog | system-card | model-card>
# llm scope uses:  categories: [架构, 后训练, ...]
# omni scope uses: category: <t2i | video | edit | unified | 3d | audio | omni | method>
category: <one-category>
tags: [tag1, tag2]
url: "<canonical primary-source URL — the dedup key; must be unique within a scope>"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [<source-file-in-sources/.../>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## 一句话定位
<One-sentence positioning: what it is, the single key idea, the headline result.>

## 背景与定位
<Problem it solves; where it sits in the technical lineage. Use [[other-slug]] links.>

## 模型架构
<Architecture: backbone, key components, concrete numbers where disclosed.>

## 数据
<Data: scale, sources, mixture/ratio, cleaning/filtering, synthetic data — with numbers.>

## 训练方法
<Training objective, multi-stage pipeline, post-training/RL, distillation, key hyperparams.>

## Infra（训练 / 推理工程）
<Compute scale, parallelism, precision, throughput; inference/serving. "未披露" if not disclosed.>

## 评测 benchmark
<Quantitative results from the primary source. State plainly when none are reported.>

## 创新点与影响
<Core contribution, what it changed, known limitations.>

## 原始链接
- url: <primary URL>
- pdf_url / github_url / project_url as applicable

## 一手源存档（sources/）
- <link to the archived primary source under sources/<scope>/<year>/>
