---
title: "Qwen-Image-Bench: From Generation to Creation in Text-to-Image Evaluation"
org: "Alibaba Qwen"
country: China
date: "2026-05"
type: paper
category: method
tags: [t2i, benchmark, evaluation, judge-model, mllm-judge, creator-centric, qwen]
url: "https://arxiv.org/abs/2605.28091"
arxiv: "https://arxiv.org/abs/2605.28091"
pdf_url: "https://arxiv.org/pdf/2605.28091"
github_url: "https://github.com/QwenLM/Qwen-Image-Bench"
hf_url: "https://huggingface.co/datasets/Qwen/Qwen-Image-Bench"
modelscope_url: "https://www.modelscope.cn/datasets/Qwen/Qwen-Image-Bench"
project_url: ""
downloaded: [arxiv-2605.28091.pdf, qwen-image-bench--github-readme.md, qwen-image-bench--hf-dataset-readme.md, qwen-image-bench--hf-judge-model-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Qwen-Image-Bench 是阿里 Qwen 团队联合 80 名美院专业标注者打造的"创作者中心" T2I 评测基准：在传统的质量/美学/文图对齐之外，新增 **Real-world Fidelity（真实世界忠实度）** 与 **Creative Generation（创意生成）** 两大应用驱动维度，构成 5 大支柱 → 23 个二级子能力 → 56 个三级可验证 rubric 的三层能力树；用 1000 条中英双语长短分层 prompt + 一个基于 Qwen3.6-27B 微调、由 13 万+ 专家标注训练的统一裁判模型 **Q-Judger**（与人类专家排序 Spearman ρ=0.92）逐 facet 打分。实证显示 GPT Image 2 以 64.7 总分居首且五维全面领先，而 Creative Generation 维度组间方差是 Quality 的 11 倍以上，证明新增的两个应用维度正是现有基准看不见的区分点。

## 背景与定位
T2I 生成已从"画得像"进化为专业创作工作流的核心能力，但评测严重滞后。论文指出现有基准三大缺陷：
1. **基础语义轴饱和、区分度塌缩**——前沿模型在常见 prompt-following 套件上接近天花板，强模型被压进难以区分的分数带，甚至出现 benchmark drift（分数与人类判断脱节）。
2. **真实世界忠实度刻画不足**——很少有套件能把"看起来合理"与"真正尊重物理常识/文化背景/事实结构"分开。
3. **创意生成缺乏明确评测协议与专家监督**——更危险的是越来越多 pipeline 把单个 MLLM 当唯一裁判，甚至直接拿它的标签训奖励模型（点名 UniGenBench++ 用 Gemini-2.5 既当评估器又当标签源），导致系统性偏差被原样继承，只是"把一个 MLLM 的世界观规模化复制"。

定位上，它对标的不是 [[geneval]] / T2I-CompBench 这类侧重物体属性的早期基准，也不只是 TIFA / DSG-1k / DPG-Bench / UniGenBench++ 等 VQA/MLLM 评测，而是要做一个**由专业艺术家共同设计、扎根真实创作场景、能可信区分前沿商用模型**的评测框架。它把评测目标从"generation（生成对齐）"推进到"creation（创作）"。注意：这是**评测方法工作（benchmark + judge model），不是 T2I 生成模型本身**。

## 模型架构
本工作的"模型"指评测裁判模型 **Q-Judger**，而非图像生成器：

- **Backbone**：从多模态基座 **Qwen3.6-27B** 微调而来（HF model card 明确 `base_model: Qwen/Qwen3.6-27B`，`pipeline_tag: image-text-to-text`）。它是一个视觉-语言模型（VLM），输入 = prompt + 生成图像 + 完整 taxonomy-aware checklist（含全部 L2/L3 层级与每个 facet 的 rubric），输出 = 针对 56 个三级 facet 的结构化分数向量（JSON）。
- **输入结构**：system 角色定义 + 生成 prompt + 生成图像 + 打分 rubric + 维度专属评测 checklist（编码完整 L2/L3 层级）。
- **打分输出**：每个 facet 取 4 值之一——0(Fail，明显缺陷)、1(Pass，无可见缺陷达基线)、2(Excel，卓越执行)、N/A(不适用)。
- **Thinking 模式**：开启 `enable_thinking=True`，先 chain-of-thought 推理再输出最终 JSON，而非直接打分。
- 训练框架用 **MS-SWIFT**（多模态微调框架）。具体微调超参（学习率/epoch/上下文长度/LoRA 与否）**未披露**。

三层能力树（核心架构创新，非神经网络架构）：
- **5 个 L1 支柱**：Quality、Aesthetics、Alignment、Real-world Fidelity、Creative Generation。
- **23 个 L2 子能力**，例如 Real-world Fidelity 下的 World Knowledge / Fairness / Safety & Compliance；Creative Generation 下的 Imagination / Text Rendering / Design Applications / Visual Storytelling 等。
- **56 个 L3 可验证 facet**，每个由精确 rubric 定义可观察评分标准；其中 **28 个落在两大应用驱动支柱**（覆盖世界知识、设计应用、视觉叙事、文字渲染等高频创作场景）。
- 设计哲学是 top-down 对齐专业艺术工作流的分阶段推理（ideation 立意 → styling 风格化 → iterative refinement 迭代细化），而非平铺 checklist，从而更系统、更穷尽、重叠更少，且每个 facet 是原子级、可逐级确定性上卷。

## 数据
基准的"数据"分两部分：评测 prompt 集 + 训练 Q-Judger 的标注集。

**评测 Prompt 集（1000 条）——专家在环 prompt 工厂（四阶段流水线）**：
1. **Facet 定向采样**：从 56 个 L3 facet 集合中为每条 prompt 采样目标子集 C_p（k≥3），在平衡约束下让每个 facet、每个 L1 支柱在最终 1000 条中被大致等频访问；尽量让 C_p 跨至少 3 个 L1 支柱，使单条 prompt 同时压测如对齐准确、构图美学、真实忠实等多维。
2. **双语起草**：用 **Qwen3-Max 与 ChatGPT-5.2** 生成语义对齐的中英草稿，并附显式 instantiation note d_i（精确记录 facet c_i 如何在草稿中被实现），强制 prompt 内容与评测目标显式映射而非靠推断。
3. **专家审改与再验证**：专业艺术家作为"共同作者"过 gate——丢弃 trivial/歧义/区分度不足的 prompt，重写对 C_p 实例化弱或泛化的 prompt，并对照 rubric 再验证每个目标 facet 被真正激发。只有过 gate 才入库。
4. **长度变体扩展**：用阈值（中文 70 字符 / 英文 235 字符）分长短；长变体由 LLM 在语义保持约束下扩展，再重对齐 facet 映射（k'≤k+5）。

最终 **1000 条 prompt，均分 500 短 + 500 长，每条中英双语**；prompt 范围覆盖 17 个应用域，锚定真实付费创作场景（产品设计、漫画创作、分镜、时尚设计、游戏设计、世界知识、镜头/影视风格、文字渲染等）。平均每条 prompt 同时考查跨 3–5 个 L1 支柱的 facet。论文还对比指出：HRS-Bench / T2I-CompBench 平均 prompt 仅 16.43 / 12.65 token，DPG-Bench / UniGenBench++ 这类 dense 套件也通常封顶在 80–160 token，难以承载真实创作请求的丰富场景上下文。

**Q-Judger 训练标注集（13 万+ 对）**：
- **超过 130,000 条**双语人工标注的 prompt-image 对，采样以平衡模型来源、难度等级、L3 facet 覆盖。
- **80 名专业标注者**，全部持美院学位，背景为摄影、导演、纯艺。
- **blind labeling（去除模型身份）** + 每对至少 **3 名独立专家交叉评审**。
- 标注协议 checklist-driven、taxonomy-aware："facet-by-facet, rubric-by-rubric"，每个训练标签都锚定具体可验证证据而非整体印象；prompt 预分配的 L3 facet（及其上卷的 L2）连同 rubric 一并暴露给标注者。
- 关键立场：**所有训练标签由人类专家产生，零 MLLM 自动标注**——这正是它与 UniGenBench++ 等"MLLM 当裁判+标签源"路线的根本区别。

## 训练方法
- **裁判模型训练目标**：监督微调（SFT）——以 Qwen3.6-27B 为初始，在 13 万+ 专家标注对上做多模态指令微调，让模型对每个 L3 facet 在 {0,1,2,N/A} 四值上做 rubric-grounded 预测。训练框架 MS-SWIFT。论文/卡片**未披露**学习率、epoch、batch、上下文长度、是否 LoRA、训练算力等具体超参与配置。
- **推理（评测时）确定性解码**：seed=42、temperature=0、top_k=1、top_p=1、repetition_penalty=1.05、max_new_tokens=4096、`enable_thinking=True`、max_batch_size=24（对应 ms-swift CLI flag），保证可复现。
- **分数归一化（非线性映射）**：0→0、1→60、2→100、N/A 排除。**1(Pass) 故意映射到 60 而非中点 50**——把"不可接受 vs 可接受"(0 vs 60) 的差距相对"可接受 vs 卓越"(60 vs 100) 放大，反映用户体验中 Fail/Pass 之差远比 Pass/Excel 之差更要紧。
- **多粒度自底向上聚合**：单次 Judge 推理即产出三层全部分数。逐样本：L2 = 其被激活子 facet 的均值；L1 = 其被激活子能力均值；overall = 被激活支柱（每条 prompt 激活 3–5 个）的**无权重均值**。模型级 = 对所有 1000 条 prompt 的样本级分数求均。每个聚合分数都能数值一致地回溯到具体 L3 facet，保证可解释与可诊断。
- 不涉及扩散/flow matching/蒸馏等生成式训练（被评测的 18 个生成模型各自方法不在本工作范围）。

## Infra（训练 / 推理工程）
- **训练**：基于 MS-SWIFT 框架微调 Qwen3.6-27B。GPU 规模、卡时、并行/分布式、混合精度、吞吐**均未披露**。
- **推理/部署**：开源工具包（`judge.py` 跑裁判推理、`compute_scores.py` 从预生成响应复算分数），后端为 ms-swift 的 `PtEngine`，默认 `max_batch_size=24`、`max_new_tokens=4096`。输入要求 ID/prompt/image_path 三列（ID 1–1000 须匹配 bench metadata，决定该 prompt 适用哪些维度）。输出三文件：逐行 `_judged`、聚合 `_bench_scores.json`、Excel `_bench_scores.xlsx`。
- **可离线评测**：同时开源 Judge Model + 完整 prompt 集 + 18 模型预生成图像与裁判响应（HF/ModelScope，Apache-2.0），支持完全离线复现榜单，宣称"显著降低评测成本同时贴近专业标准"。具体单图推理延迟/吞吐数字未报告。

## 评测 benchmark（把效果讲清楚）
**裁判模型与人类一致性（Table 1，N=18 模型，p<1e-4）**：Spearman ρ——Quality 0.89、Aesthetics 0.89、Alignment 0.89、Real-world Fidelity 0.92、Creative Generation 0.92、**Overall 0.92**。两个新增应用维度上一致性最高（0.92）。

**18 个前沿 T2I 模型总榜（Table 2，[0,100]，按 overall 排序，加粗为各列最佳）**——
注意：HF 卡片注明该榜单基于**中文 prompt** 生成图计算，英文 prompt 结果"即将发布"。

| 排名 | 模型 | Quality | Aesthetics | Alignment | Real-world Fidelity | Creative Generation | Overall |
|---|---|---|---|---|---|---|---|
| 1 | GPT Image 2 | **58.65** | **67.53** | **65.85** | **57.38** | **75.23** | **64.69** |
| 2 | Nano Banana 2.0 | 54.77 | 61.08 | 62.40 | 54.28 | 67.05 | 59.82 |
| 3 | GPT Image 1.5 | 55.14 | 60.88 | 61.72 | 53.95 | 66.35 | 59.65 |
| 4 | Nano Banana Pro | 55.67 | 60.26 | 61.25 | 54.07 | 66.23 | 59.45 |
| 5 | Qwen Image 2.0 Pro | 54.39 | 58.67 | 59.28 | 51.83 | 64.94 | 57.84 |
| 6 | Seedream 5.0 | 52.55 | 58.40 | 58.90 | 51.92 | 65.29 | 57.22 |
| 7 | Seedream 4.5 | 54.41 | 58.72 | 57.31 | 51.69 | 60.64 | 56.78 |
| 8 | Seedream 4.0 | 54.01 | 58.81 | 56.64 | 51.05 | 58.15 | 56.21 |
| 9 | FLUX 2 Max | 53.64 | 56.85 | 57.35 | 49.35 | 56.50 | 55.33 |
| 10 | FLUX 2 Pro | 52.30 | 56.94 | 57.01 | 47.29 | 56.18 | 54.57 |
| 11 | GPT Image 1 | 52.34 | 55.09 | 56.28 | 48.14 | 55.78 | 54.07 |
| 12 | Qwen Image 2512 | 51.76 | 54.74 | 52.72 | 47.00 | 50.19 | 52.06 |
| 13 | Imagen 4.0 Ultra | 50.90 | 54.25 | 54.02 | 45.59 | 51.14 | 51.99 |
| 14 | HunyuanImage 3.0 | 50.35 | 53.57 | 52.00 | 44.31 | 49.12 | 50.81 |
| 15 | Imagen 4.0 | 50.16 | 52.68 | 51.64 | 44.84 | 47.94 | 50.29 |
| 16 | Qwen Image | 48.44 | 52.25 | 50.72 | 43.16 | 47.30 | 49.23 |
| 17 | Kling Image 2.1 | 49.11 | 50.15 | 49.18 | 44.74 | 44.67 | 48.26 |
| 18 | GLM Image | 49.26 | 50.64 | 47.90 | 44.69 | 45.23 | 48.19 |

**关键结论**：
- **[[gpt-image-2|GPT Image 2]] 总分 64.69 居首，领先第 2 名 Nano Banana 2.0 近 5 分，且五个 L1 支柱全部第一**（无明显短板，在 18 模型中罕见）。GLM Image 垫底，与榜首拉开 **16.5 分**，证明基准全谱区分力。
- 18 模型自然分 **5 个 tier**：T1(64+)=GPT Image 2；T2(59–60)=Nano Banana 2.0/GPT Image 1.5/Nano Banana Pro；T3(56–58)=Qwen Image 2.0 Pro/Seedream 5.0/4.5/4.0；T4(54–56)=FLUX 2 Max/Pro、GPT Image 1；T5(48–52)=其余 7 个。
- **方差驱动的区分力分析（Fig.5，核心卖点）**：L1 层 **Creative Generation 的组间方差是 Quality 的 11 倍以上、Aesthetics 的 4 倍以上**——Quality 已成"table-stakes"，Creative Generation 才是模型分化最剧处。Creative Generation 的 leader–bottom 跨度达 **30.6 分**（五支柱中最大）。L3 层最具区分度的 facet 依次是 **Text Accuracy（Creative Generation）、Information Visualization（Real-world Fidelity）、Cross-lingual Generation（Creative Generation）**；方差最高的 15 个 L3 facet 中有 **12 个**属于这两大新增支柱。L2 层方差最高的是 Text Rendering，其次 Style Control / Logical Resolution / World Knowledge——top6 中 4 个属新增支柱。
- **系统性天花板（4–5 个 facet 全员塌陷）**：Anatomical Fidelity（最佳仅 20.9）、Physical Logic（最佳 31.9）、Objects（最佳 41.9）、Animals（最佳 42.6）、Contact Interaction（最佳 43.3）——即便最强模型这几项也 **<44**，且跨 Aesthetics/Quality/Real-world Fidelity/Alignment 四个支柱，反映当前 T2I 在细粒度物理与生物结构/逻辑上的共性短板。
- **"想象 vs 执行精度"鸿沟（以 [[qwen-image-2-0|Qwen Image 2.0 Pro]] 为例）**：在视觉风格类 facet（Art Design、Camera/Lens Style、Cinematic Style、Graphic Design）有竞争力，但在创意精度类 facet（Text Accuracy、Font、Product Design、Comic Creation、Game Design、Information Visualization）显著内陷——其 Creative Generation 前 10 facet 均值 76.5、后 5 facet 仅 55.5，**同一支柱内落差 >21 分**。
- **设计应用类 L3 细化（Fig.6b）**：Game Design 阈值效应最极端（GPT Image 2 达 91.8，第 7 名起跌破 66）；Graphic Design 第 1 到中位差 >30 分；Fashion Styling 梯度最平（leader–bottom 仅 13 分）；Product Design 跨度 32 分；Art Design 第 2–4 名相差不足 1 分（风格迁移在前沿模型间已较成熟）。
- **版本演化权衡（被多支柱评测显式暴露）**：Seedream 4.5 在 Quality/Aesthetics 上反超 5.0，而 5.0 在 Creative Generation 上反超 4.5 超过 4 分——说明新版以基础画质为代价换取创意能力，单分数基准会掩盖这一 trade-off。

## 创新点与影响
**核心贡献**：
1. **把 T2I 评测从"生成对齐"推进到"创作"**：首次以"创作者中心"显式、联合评测 Real-world Fidelity 与 Creative Generation 两大应用维度，并用方差证据量化证明它们正是现有基准看不见的区分轴。
2. **专业艺术家共同设计的三层能力树**（5/23/56），对齐真实创作工作流的分阶段推理，使诊断可解释、可定位到具体艺术子技能，且可单次推理产出三层全部排名。
3. **统一、全人类专家监督的裁判模型 Q-Judger**：逐 56 facet 出可归因分数向量而非单一不透明分；坚持零 MLLM 自动标注（80 美院专家 / 13 万+ 对 / blind+三审），与人类排序 ρ=0.92，从根上规避"MLLM 当唯一裁判"的系统性偏差与 benchmark drift。
4. **可复现工程**：非线性 0/60/100 映射 + 确定性解码 + 自底向上聚合 + 完全离线可复现（开源 Judge/prompt/预生成响应，Apache-2.0）。

**影响**：为生产级 T2I 研发提供可信优化信号，并指出 Physical Logic、Anatomical Fidelity、Animals、Contact Interaction 等行业级共性天花板作为后续攻关方向；其"专家在环 + 人类监督裁判 + 方差驱动区分力"范式对后续 T2I/编辑评测基准有方法论参考价值。

**已知局限**：
- 公布榜单基于**中文 prompt**，英文 prompt 结果尚未发布（HF 卡片注明 coming soon），跨语言对称性结论待补。
- 裁判模型微调的具体训练超参/算力**未披露**，第三方完全复现训练受限。
- ρ=0.92 一致性仅在 18 个模型的排序层面验证；裁判模型本身是否存在 Qwen 系列偏好（其基座为 Qwen3.6-27B、prompt 起草用 Qwen3-Max，被评 Qwen 模型并非榜首，偏好风险较低但未做专门去偏审计）属潜在隐忧。
- 系统性天花板 facet 上裁判分数本身的可靠性（模型在自身弱项 facet 上的判别力）未单独评估。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2605.28091
- arxiv_pdf: https://arxiv.org/pdf/2605.28091
- github: https://github.com/QwenLM/Qwen-Image-Bench
- hf_dataset: https://huggingface.co/datasets/Qwen/Qwen-Image-Bench
- hf_judge_model: https://huggingface.co/Qwen/Qwen-Image-Bench
- modelscope_dataset: https://www.modelscope.cn/datasets/Qwen/Qwen-Image-Bench
- modelscope_model: https://modelscope.cn/models/Qwen/Qwen-Image-Bench

## 一手源存档（sources/）
- [arxiv-2605.28091.pdf](https://arxiv.org/pdf/2605.28091)  （arXiv 原文 PDF，不入 git）
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/qwen-image-bench--github-readme.md)
- [hf-dataset-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/qwen-image-bench--hf-dataset-readme.md)
- [hf-judge-model-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2026/qwen-image-bench--hf-judge-model-card.md)
