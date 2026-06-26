---
title: "Human Preference Score v2 (HPS v2): A Solid Benchmark for Evaluating Human Preferences of Text-to-Image Synthesis"
org: "CUHK MMLab / CPII / SenseTime"
country: China
date: "2023-06"
type: paper
category: method
tags: [t2i, human-preference, reward-model, benchmark, clip, rlhf, evaluation, dataset]
url: "https://arxiv.org/abs/2306.09341"
arxiv: "https://arxiv.org/abs/2306.09341"
pdf_url: "https://arxiv.org/pdf/2306.09341"
github_url: "https://github.com/tgxs002/HPSv2"
hf_url: "https://huggingface.co/spaces/xswu/HPSv2"
modelscope_url: ""
project_url: "https://tgxs002.github.io/hpd_test_vis/"
downloaded: [arxiv-2306.09341.pdf, hps-v2--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
HPS v2 = **大规模去偏（论文措辞 less biased，非"完全无偏"）人类偏好数据集 HPD v2（798k 对偏好选择 / 433k 图）+ 在其上微调 OpenCLIP ViT-H/14 得到的偏好打分模型**，把文生图的"好不好看/对不对齐"做成一个可复现、统计稳定的评测指标与奖励信号；在 HPD v2 测试集上偏好预测准确率 **83.3%**，超过 PickScore（79.8%）、HPS v1（77.6%）、ImageReward（74.0%），并配套发布一套 4 风格×800 prompt 的标准评测榜单。

## 背景与定位
传统生成质量指标 IS、[[fid]]、CLIP Score 与人类对文生图结果的偏好相关性很差（论文引用 ImageReward/HPS v1/Pick-a-Pic 的结论），而文生图同一 prompt 不同随机种子质量差异很大，"人类偏好"这一维度长期缺乏可靠度量。

此前同类工作各有偏差（论文 Tab.5 头对头对比）：
- **HPS v1**（同组前作 align_sd，2023）：从 Discord 收集 25k top-1 选择，图全来自 Stable Diffusion，prompt 风格高度偏置。
- **ImageReward**（THUDM）：9k prompt / 137k 对，图仍只来自 Stable Diffusion。
- **Pick-a-Pic**（PickScore 的数据）：38k prompt / 584k 对，来自 web 应用用户，prompt 重复严重（34.9% 实例的 prompt 重复 50 次以上）。

HPD v2 针对两类偏差做"去偏"：
1. **图像来源偏差**——以往数据集几乎只含 Stable Diffusion 及其变体，无法验证打分模型的跨分布泛化。HPD v2 纳入 **9 个不同架构/规模的生成模型 + COCO 真实图**。
2. **prompt 偏差**——DiffusionDB 用户 prompt 充斥风格词（15.0% 含 "Greg Rutkowski"、28.5% 含 "artstation"）且常自相矛盾（"renaissance oil painting" 与 "realism/hyper realistic" 冲突），对没用过这些训练数据的模型不公平。HPD v2 用 **ChatGPT 清洗** prompt，去掉风格/分辨率/作者/平台等修饰词，改写成一句通顺描述。

定位：它不是生成模型，而是文生图领域的**偏好评测标准 + 奖励模型**。后续 RLHF/DPO 类对齐工作（如 [[ddpo]] / DPOK / [[diffusion-dpo]] 思路）常把 HPS v2 既当奖励又当评测，与 ImageReward、PickScore 并列为 t2i 偏好三大标尺之一。

## 模型架构
HPS v2 **不引入新架构**，核心是把 CLIP 当作"prompt–图像"打分函数 s 来微调：
- **骨干**：OpenCLIP **ViT-H/14**（在 LAION-2B 上由 OpenCLIP 项目预训练）。模型卡（论文 Tab.8）：
  - 图像塔：输入 224×224、patch 14、**32 层 transformer**、width 1280、16 heads；
  - 文本塔：context length 77、词表 49408、**24 层 transformer**、width 1024、16 heads；
  - 联合 embedding 维度 1024。
- **打分定义**：sθ(p,x) = Enc_txt(p)·Enc_img(x) / τ，τ 为 CLIP 学到的温度标量；用于打榜时写成 sθ(p,x)=Enc_txt(p)·Enc_img(x)×100（即把余弦相似度乘 100，对应 README 榜单里 23~28 量级的分数）。
- **偏好预测**：对同一 prompt 的两张图 {x1,x2}，把两者得分过 softmax 得到 ŷ，监督信号是 one-hot 偏好标签 y。
- 没有 VAE/VQ tokenizer、没有 text encoder 替换——它评的是别人生成的图，自身是判别式打分器。

## 数据（HPD v2，本工作的核心贡献）
**规模**：798,090 条二选一偏好选择，覆盖 433,760 张图、107,515 个 prompt（图/prompt 总数及 645,090 train + 153,000 test 的拆分均出自附录 H Datasheet H.2）；号称同类最大。**注：Datasheet 自相矛盾——同一段先写"There are 789,090 instances ... 789,090 comparisons"，又给 433,760 images / 107,515 prompts；而正文 Sec.3.4 与摘要/README 用 798,090（≈798k）**。本页主数用 798k（正文/README 口径），789,090 视为 datasheet 笔误。

**Prompt 来源与清洗**：
- 来自 **DiffusionDB**（用户 prompt）+ **COCO Captions**（真实图描述）。
- DiffusionDB prompt 全部用 **ChatGPT** 清洗：去风格/分辨率/作者/平台等修饰，改写成一句话，并分类到 paintings / anime-cartoon / real photo / concept-art / others（附录 A 给出完整指令）。
- NSFW 过滤：先用 Detoxify NSFW 阈值 0.4 过滤；生成阶段再过 **DALL·E 2 的安全检查器**二次清理。清洗后高 NSFW 桶、artist/platform 风格词频率、ChatGPT 判定的"冲突 prompt"占比均显著下降（Fig.2/3）。

**图像来源**（论文 Tab.2，共 10 类）：
| 来源 | split | 参数量 | 类型 | 图数 |
| --- | --- | --- | --- | --- |
| CogView2 | train&test | 24B | 自回归 | 73,697 |
| DALL·E 2 | train&test | 3.5B | 扩散 | 101,869 |
| GLIDE(mini) | test | 0.94B | 扩散 | 400 |
| SD v1.4 | train&test | 0.89B | 扩散 | 101,869 |
| SD v2.0 | train&test | 0.89B | 扩散 | 101,869 |
| LAFITE | test | 0.75B | GAN | 400 |
| VQGAN+CLIP | test | 0.73B | GAN | 400 |
| VQ-Diffusion | test | 0.37B | 扩散 | 400 |
| FuseDream | test | 0.35B | GAN | 400 |
| COCO Captions | train&test | – | 真实图 | 28,272 |

- **训练集**：每组 4 张（来自 4 个 train 模型或真实图），由 1 名标注者排序 → 645,090 对；其中 28,172 prompt 来自 COCO。
- **测试集**：400 组、每组 9 张（COCO 组额外加 1 张真实图），**每组由 10 名不同标注者各排序一次** → 153,000 对。**5 个仅出现在 test 的模型**（GLIDE/LAFITE/VQGAN+CLIP/VQ-Diffusion/FuseDream）专门用来测打分模型的泛化。

**标注**：57 名合同工（50 标注 + 7 质检），录用率 61%；入职前做 300 组排序测试，质检按 recall@2 抽查 ≥10% 任务。标注准则（附录 B）：综合考虑文图对齐 + 视觉吸引力，画质严重失真优先级低于对齐；冲突时偏向文图对齐。标注者画像有完整统计（性别 25 男/32 女、年龄段、全/兼职等），工资 20 CNY/h（标注）、25 CNY/h（质检）。
- **标注一致性**（Fig.4/5、Tab.4）：质量差距大的模型对之间一致性高、质量接近时一致性低；与 HPS v2 分数差绝对值正相关。

## 训练方法
- **目标函数**：把偏好预测当二分类，最小化预测分布 ŷ 与 one-hot 标签 y 的 **KL 散度**（即 pairwise 偏好交叉熵），公式见正文 Eq.1–3。
- **微调对象**：OpenCLIP ViT-H/14，**只解冻末段层**——图像编码器最后 **20 层**、文本编码器最后 **11 层**（常见"冻结前几层"做法，在有限数据上更稳）。
- **超参**：AdamW，**lr 3.3×10⁻⁶**、weight decay 0.35、batch 128、warmup 500 步、cosine 调度，**总共仅 4,000 步**。所有超参由 **贝叶斯优化**以 HPD v2 测试集准确率为目标搜得。
- **消融**（附录 F）：
  - 学习率（Tab.10）：3.3×10⁻⁶ 取到峰值 83.27%，过大/过小都掉点（0.5×10⁻⁶ 跌到 81.79%）。
  - 图像编码器解冻层数（Tab.11）：0 层（全冻）只有 78.37%，25 层 83.23%、20 层 83.27%，**解冻太多反而无增益**。
  - 文本编码器解冻层数（Tab.12）：16 层 83.29%，11 层 83.27%，全冻 82.89%；总体不如图像塔敏感。
- 无扩散/flow matching、无蒸馏——这是判别式 reward 模型，不涉及生成训练。

## Infra（训练 / 推理工程）
- **算力**：论文正文未给具体 GPU 数/卡时；NeurIPS checklist 中作者承诺"资源消耗在 GitHub 仓库报告"（本次抓取的 README 未见明确卡时数字，记为**未披露**）。训练本身只 4,000 步、batch 128，对 ViT-H 量级是轻量微调。
- **训练脚本**：仓库提供 `configs/HPSv2.sh`，支持本地 8 卡与 slurm（`bash configs/HPSv2.sh train 8 ${quota_type}`）。
- **推理/部署**：发布 **PyPI 包 `hpsv2`**（`pip install hpsv2`，`hpsv2.score(imgs, prompt, hps_version)`）；HuggingFace Space 提供在线 demo；提供**压缩 checkpoint** `HPS_v2_compressed.pt`。许可证 **Apache 2.0**（代码与数据）。
- 评测设计本身就是工程优化点：每风格 800 prompt 分 10 组（每组 80）跑均值±方差，作者论证 800 prompt 足以让分数**统计稳定**又不至于算力过大。

## 评测 benchmark（把效果讲清楚）
**(1) 偏好预测准确率**（论文 Tab.6 / README，越高越好）：
| 模型 | ImageReward 测试集 | HPD v2 测试集 |
| --- | --- | --- |
| CLIP ViT-H/14（零样本） | 57.1 | 65.1 |
| Aesthetic Score Predictor | 57.4 | 76.8 |
| ImageReward | 65.1 | 74.0 |
| HPS v1 | 61.2 | 77.6 |
| PickScore | 62.9 | 79.8 |
| 单人 vs 单人 | 65.3 | 78.1 |
| 单人 vs 平均排名 | 53.9 | 85.0 |
| **HPS v2** | **65.7** | **83.3** |

要点：HPS v2 在两个分布迥异的测试集上都最好，**在 HPD v2 上甚至超过"单个真人 vs 单个真人"的 78.1%**——因为它学的是多人平均偏好，能逼近群体倾向（但仍低于"单人 vs 平均排名"的 85.0%，说明天花板尚在）。

**(2) HPS v2 基准榜**（论文 Tab.7 / README，对 20 个文生图模型按 Animation/Concept-art/Painting/Photo 四风格打分，分数×100 量级）。摘录平均分（README v2.0 榜）：Dreamlike Photoreal 2.0 **27.86** > SDXL Refiner 0.9 27.80 > Realistic Vision 27.77 > SDXL Base 0.9 27.73 > Deliberate 27.67 …… DALL·E 2 26.95、SD v1.4 26.95、Latent Diffusion 25.78、GLIDE 23.55（垫底）。论文还附 DrawBench 列做参考。
- 关键观察：**社区模型（Dreamlike/Realistic Vision/Deliberate 等）系统性优于学术模型**；CogView2 美学高但可控性差（CLIP Score 低），是有趣反例。

**(3) v2.1 更新**（README 更新日志日期 09/02/2024 并附 "Happy new year"，按 m/d/y 即 2024-02-09 发布；在更高质量数据上重训，分数尺度与 v2.0 不可直接比）：拉大了模型间区分度（SDXL Refiner 0.9 平均 31.34 vs GLIDE 14.51）；偏好预测准确率进一步升到 ImageReward 66.8 / HPD v2 84.1。

**(4) pairwise 泛化**（附录 E Tab.9）：HPS v2 在大多数模型对之间与人类选择高度一致（如 SD v2.0 vs GLIDE 达 98.8%、SD v2.0 vs LAFITE 97.0%），但质量接近的模型对（如 FuseDream vs VQGAN+CLIP 51.5%、VQ-Diffusion vs VQGAN+CLIP 51.5%）一致性低，与人类标注者间一致性规律吻合。

**(5) 灵敏度验证**（附录 G Tab.13，基线 SD v1.4）：两个算法改进都能被 HPS v2 量化——① **retrieval initialization**（用强社区模型 Dreamlike Photoreal 2.0 生成先验图、编码进 latent 再叠噪初始化，纠正训练/推理噪声 schedule 不一致），效果小：Animation 27.26→27.39、Painting 26.66→26.71、Photo 27.27→27.46 微升，**Concept-art 反而 26.61→26.59 微降**（四风格非一致上升）；② **HPS v1 的 human-aligned tuning** 带来更大且一致提升（Animation 27.26→27.80、Concept-art 26.61→27.16、Painting 26.66→27.24、Photo 27.27→27.60）。证明 HPS v2 对真实算法改进敏感。

## 创新点与影响
**核心贡献**：
1. **HPD v2**——最大规模、来源最广（9 模型+真实图）、prompt 经 ChatGPT 去偏、标注者画像透明的人类偏好数据集；显式拆出 5 个 unseen 模型评测泛化。
2. **HPS v2**——一个准确率领先、跨分布泛化好、对算法改进敏感的偏好打分/奖励模型，方法极简（CLIP 末段层微调 + pairwise KL）。
3. **标准评测协议**——4 风格×800 prompt、分 10 组报均值±方差的稳定打榜方案，解决了 DrawBench 太小、DiffusionDB prompt 有偏的问题。

**影响**：HPS v2/v2.1 成为文生图领域事实上的偏好评测与奖励标准之一，与 ImageReward、PickScore 三足鼎立，被大量 t2i 对齐（RLHF/DPO/reward fine-tuning）与新模型发布的论文引用作为评测指标。

**已知局限**（论文第 6 节）：prompt 仅来自 DiffusionDB+COCO，遗漏 logo/平面设计等品类；ChatGPT 清洗可能引入潜在偏差；57 名标注者本身带偏；**未研究图像分辨率对偏好的影响**（随生成分辨率上升影响可能很大）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2306.09341
- arxiv_pdf: https://arxiv.org/pdf/2306.09341
- github: https://github.com/tgxs002/HPSv2
- hf_space_demo: https://huggingface.co/spaces/xswu/HPSv2
- hf_dataset(HPD v2): https://huggingface.co/datasets/ymhao/HPDv2
- pypi: https://pypi.org/project/hpsv2
- test_vis: https://tgxs002.github.io/hpd_test_vis/

## 一手源存档（sources/）
- [arxiv-2306.09341.pdf](https://arxiv.org/pdf/2306.09341)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/hps-v2--readme.md)
