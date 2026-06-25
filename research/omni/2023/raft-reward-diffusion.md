---
title: "ImageReward & ReFL: Learning and Evaluating Human Preferences for Text-to-Image Generation"
org: "Tsinghua University / Zhipu AI"
country: China
date: "2023-04"
type: paper
category: method
tags: [t2i, reward-model, rlhf, refl, human-preference, alignment, diffusion]
url: https://arxiv.org/abs/2304.05977
arxiv: https://arxiv.org/abs/2304.05977
pdf_url: https://arxiv.org/pdf/2304.05977
github_url: https://github.com/THUDM/ImageReward
hf_url: https://huggingface.co/THUDM/ImageReward
modelscope_url:
project_url: https://huggingface.co/datasets/THUDM/ImageRewardDB
downloaded: [arxiv-2304.05977.pdf, raft-reward-diffusion--readme.md, raft-reward-diffusion--hf-datasetcard.md, raft-reward-diffusion--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
ImageReward 是**首个通用文生图人类偏好奖励模型（RM）**，用 137k 对专家偏好对比训练，偏好预测准确率 65.14%（CLIP score 54.82%、Aesthetic 57.35%、BLIP 57.76%）；配套提出 **ReFL（Reward Feedback Learning）——首个对扩散模型直接用 scorer 反向传播打分梯度的微调算法**，ReFL 微调后的 SD v1.4 在人评中以 **58.4% 胜率**击败原版，开启了 t2i 偏好对齐方向（NeurIPS 2023）。

## 背景与定位
彼时文生图（[[stable-diffusion-1]] / DALL-E 2 / [[latent-diffusion-ldm]]）已能出高保真图，但自监督预训练分布噪声大、与真实用户 prompt 分布有差异，导致四类顽疾：**文图对齐错误、肢体问题（body problem）、审美偏离、毒性与偏见**——这些靠改架构/堆预训练数据难以解决。NLP 侧 InstructGPT 的 RLHF（学一个 RM 再 PPO 对齐）已验证有效，但 t2i 领域几乎空白。

本工作填两个洞：
1. **评测/打分洞**——CLIP score、Aesthetic、BLIP score 都只看单一维度（文图相似度或美学），且 FID 需在整个数据集上平均、无法对单图选优，也不反映人类偏好。需要一个**综合对齐+保真+无害**的通用 RM。
2. **优化洞**——LDM 多步去噪**不产生整条生成的 likelihood**，无法照搬语言模型那套 PPO（依赖整条 generation 的似然）。同期工作只能走"间接"路线：用 RM 过滤数据再微调（RAFT [Dong et al. 2304.06767]、[Wu et al. 2303.14420]）或按质量给 loss 重加权（[Lee et al. 2302.12192]）。本工作给出**直接**梯度反馈方案 ReFL。

定位：它是 t2i 偏好对齐的开山之作之一，后续 [[hps-v2]]（HPSv2）、Pick-a-Pic、[[diffusion-dpo]]、[[ddpo]]、[[d3po]] 等都在此方向延伸；其下一代为 VisionReward（2024-12，扩展到 text-to-video 的细粒度多维 RM）。

## 模型架构
**ImageReward RM 架构**：
- **Backbone = BLIP**（不是 CLIP）。论文在预实验中发现 BLIP 显著优于 CLIP，原因有二：BLIP 训练做了 bootstrapping（自举清洗 caption），且其 **image-grounded text encoder（带 cross-attention 的特征编码器）**比 CLIP 的双塔独立编码器更能融合图文信息。
- 具体组件：BLIP 的 **ViT-L 图像编码器 + 12 层 transformer 文本编码器**；提取图、文特征后用 **cross attention** 融合，最后接一个 **MLP head** 输出标量偏好分。
- MLP head 按 N(0, 1/(d_model+1)) 初始化。
- 输出分大致服从标准正态（mean 0, var 1），README 据此提供"低于阈值过滤"功能。

**ReFL 不是新模型**，而是作用在已有 LDM（实验用 [[stable-diffusion-1]] v1.4）上的微调算法——把 ImageReward 当作可微的偏好损失项接入扩散训练循环。

## 数据
**ImageRewardDB（偏好标注数据集）**：
- **Prompt 来源**：全部采样自 **DiffusionDB**（1.8M 真实用户 prompt 的开源库）。为保证主题多样性，用基于图的算法选 prompt：每个 prompt 用 **Sentence-BERT** 编码为向量做顶点，连 k 近邻（k=150）建图，按"未被选中的邻居数"反复打分选点。因复杂度是样本数平方阶，先把全部 prompt 分成 100 组（每组约 20k），每组选 100 个 → 共 **10k 候选 prompt**，每个配 4~9 张 DiffusionDB 采样图 → **177,304 候选对**待标。
- **标注规模（最终）**：经 2 个月标注，得 **8,878 个有效 prompt、136,892 对图像比较**（即"137k 对专家比较"）。
- **标注流程三阶段**：① Prompt 标注（按 Parti 类目分类 + 标出模糊/有毒 prompt）；② 文图评分（每张图在 **对齐 alignment / 保真 fidelity / 无害 harmlessness** 三轴用 7 级 Likert 打分 + 问题勾选框，如 body problem）；③ 图像排序（同一 prompt 下从好到差排，并在标注文档里明确矛盾时的 trade-off，如"更对齐但更毒"则取更无害者）。
- **质控**：与专业标注公司合作；标注员需先学文档+通过与研究员一致性测试，低一致者不录用；**95.8% 标注专家有大专以上学历**；质检员逐条复核，无效标注重新分配。单人标注+质控策略（论文坦言多人拟合可能一致性更好）。
- **数据集发布（4 个规模子集，HF dataset card）**：train 分 1K/2K/4K/8K 四档；8K 档为 141.1K 对 / 49.9K 图 / 8K prompt（20.9GB）。**val 固定 412 prompt / 2.6K 图 / 7.32K 对；test 固定 466 prompt / 2.7K 图 / 7.23K 对**。全库共 62.6K 图。许可 apache-2.0，纯英文。

**ReFL 训练用数据**：
- 预训练正则项数据：**LAION-5B 中按美学分挑出的 625k 子集**。
- ReFL 的 prompt set：采样自 DiffusionDB。
- 公平对比时各微调方法都用同一份 20,000 样本，训练 1 epoch。

## 训练方法
**(A) ImageReward RM 训练（偏好学习）**
- 把排序标注转成成对比较：同一 prompt 有 k∈[4,9] 张排好序的图（x1 最好…xk 最差），无平局时最多 C(k,2) 对。损失为标准 Bradley-Terry/RM 形式：
  `loss(θ) = −E_(T,xi,xj)~D [ log σ( f_θ(T,xi) − f_θ(T,xj) ) ]`
  其中 f_θ(T,x) 是偏好标量。
- **关键训练 trick（论文专门强调"Training ImageReward is of no ease"）**：
  - **快速收敛即过拟合**——解法是**冻结部分 backbone transformer 层**。网格搜出**冻结 70% transformer 层 + lr=1e-5 + batch size=64** 时偏好准确率最高。
  - 对 lr/batch size 很敏感，在验证集上做了仔细网格搜索；lr 用 cosine 衰减。
- 数据划分：按标注员切分，挑出与研究员一致性更高的标注员的 466 prompt 作 test，其余 8k+ prompt 训练。

**(B) ReFL（Reward Feedback Learning）——核心方法创新**
- **核心 insight（Figure 4）**：观察 ImageReward 在去噪各步上对 `x_t → x_0'`（**直接预测**的原始 latent，而非真实去噪轨迹的 x_0）的打分随步数变化——
  - t≤15：所有生成分都一致地低，无法区分；
  - 15≤t≤30：高质图开始冒头但仍难判全部最终质量；
  - **t≥30：不同质量的生成在打分上已可区分**。
  即"在 40 步里走过 30 步后，直接预测出的图就足以可靠反映最终质量"。
- **算法（Algorithm 1）**：对每个 prompt，先 `x_T~N(0,I)`，**无梯度**地去噪到一个随机选的较后步 t（论文 t∈[30,40] / 实现里 [T1,T2]=[1,10] 配 T=40，即留最后 1~10 步）；只在那一步**带梯度**地预测 `x_{t-1}`，由 noise scheduler 直接得 x_0 → 解码成图 z → 喂给 RM 得分 → 把分当损失反传。
- **为什么随机选 t 而不固定最后一步**：只留最后一步梯度训练**极不稳定、结果差**。
- **最终损失（防过拟合 + 稳定）**：reward 损失与预训练损失联合：
  - `L_reward = λ·E_y( φ( r(y, g_θ(y)) ) )`，其中 φ=ReLU，λ=1e-3；
  - `L_pre =` 标准 LDM 去噪 MSE（取自 SD），用 LAION 子集做正则，防止崩坏与快速过拟合。
- **超参（ReFL on SD v1.4）**：8×A100-40GB，**半精度（half-precision）**，lr=1e-5，**总 batch 128（64 预训练 + 64 ReFL）**，φ=ReLU，λ=1e-3，T=40，[T1,T2]=[1,10]，PNDM scheduler，CFG=7.5 推理。
- 与三类间接方法对比：Dataset Filtering [Wu 2303.14420]、Reward Weighted [Lee 2302.12192]、**RAFT [Dong 2304.06767]**（reward-ranked finetuning，迭代式选高分样本微调）。

## Infra（训练 / 推理工程）
- **ImageReward RM 训练**：**4×40GB NVIDIA A100**，per-GPU batch size 16（总 64）。
- **ReFL 微调**：**8×40GB NVIDIA A100**，**half-precision**，总 batch 128，训练 1 epoch（公平对比设定）。
- 复现环境（README）：Driver 515.86.01 / CUDA 11.7 / torch 1.12.1+cu113，FID 类数值在不同环境末位约 ±0.1 浮动。
- **工程产物**：全部打包成 `image-reward` PyPI 包——3 行代码即可用 RM 打分、4 行代码跑 ReFL；并提供 **Stable Diffusion Web UI（AUTOMATIC1111）自定义脚本**，可在生成时打分、按阈值自动过滤低分图、在 PNG Info 查看历史分（落地为可用工具，而非纯论文）。
- 推理加速/量化/蒸馏：未涉及（RM 本身是轻量 BLIP+MLP 前向；ReFL 产出的是普通微调后 SD checkpoint，推理成本与原 SD 相同，省的是"生成多张再筛选"的开销）。

## 评测 benchmark（把效果讲清楚）
**1) ImageReward 作为偏好预测器（Table 3）**
> 注意（论文表注）：**Preference Acc. 列来自 466 prompt / 6,399 对比的 test set；Recall/Filter 列来自另一份 371 prompt × 每 prompt 8 图的 test set**，两组并非同一测试集，所有分数按 prompt 取平均。

| 模型 | Preference Acc. | Recall@1/@2/@4 | Filter@1/@2/@4 |
|---|---|---|---|
| CLIP Score | 54.82 | 27.22 / 48.52 / 78.17 | 29.65 / 51.75 / 76.82 |
| Aesthetic Score | 57.35 | 30.73 / 53.91 / 75.74 | 32.08 / 54.45 / 76.55 |
| BLIP Score | 57.76 | 30.73 / 50.67 / 77.63 | 33.42 / 56.33 / 80.59 |
| **ImageReward (Ours)** | **65.14** | **39.62 / 63.07 / 90.84** | **49.06 / 70.89 / 88.95** |
- 65.14% 比随机（50%）高 15.14pt，约为 BLIP score 超随机部分（7.76pt）的两倍。论文摘要口径：ImageReward 在理解人类偏好上超 CLIP 38.6%、Aesthetic 39.6%、BLIP 31.6%（相对提升）。

**2) ImageReward 作为模型评测指标（6 个 t2i 模型与人评对齐，Table 1）**
- Spearman ρ 到人评排序：**ImageReward 1.00（完全一致）**，CLIP 0.60，**zero-shot FID 0.09**（FID 与人评几乎不相关）。
- 人评排序：Openjourney > SD 2.1-base > DALL-E 2 > SD 1.4 > Versatile Diffusion > CogView2；ImageReward 完美复现该序，FID/CLIP 都错位。
- 区分度（Figure 3）：ImageReward 单模型内打分的四分位距远大于 CLIP，更能区分单图质量。

**3) ImageReward vs 其他打分器的人评选优（Figure 5）**
- top-3 选优胜率（平均）：对 Random **77.1%**、对 CLIP **69.3%**、对 Aesthetic **69.8%**、对 BLIP **65.8%**。

**4) ReFL vs 其他 LDM 优化方法（人评，Table 4 / Figure 6）**
- 对 SD v1.4 baseline 的 WinRate：**ReFL 58.49%（#Win 808）**，Dataset Filtering 55.17%，RAFT(iter1) 49.86%、(iter2) 30.85%、(iter3) 20.97%（**RAFT 随迭代加深过拟合 RM 而崩**），Reward Weighted 39.52%。
- README 口径：**ReFL 微调后 SD 对原版人评胜率 58.4%**。
- 关键结论：RAFT 与 Reward Weighted 在本文更广分布的真实用户 prompt 上**反而不如 baseline**（它们各自论文里有效，但都没用真实用户 prompt 微调）；RAFT 受限于构造数据集/专家生成器质量，Reward Weighted 因奖励系数被约束在[0,1]、非偏好图影响消不掉，Dataset Filtering 是间接的。ReFL 直接给梯度反馈故最优。

**消融**
- **Backbone（Table 2b）**：BLIP 全面胜 CLIP——CLIP 4k/8k 训练集只到 61.87/62.98 acc；BLIP 1k/2k/4k/8k 为 63.07/63.18/64.71/**65.14**。
- **数据规模**：扩数据持续涨点（暗示再标更多还能更好）。
- **冻结层比例**：冻结 70% transformer 层为最优配置（防过拟合）。
- 标注一致性（Table 2a）：研究员↔标注员一致率 65.3%，annotator ensemble↔研究员 73.4%——说明偏好虽主观但有可达成的共识上限。

## 创新点与影响
**核心贡献**
1. **首个通用 t2i 人类偏好 RM（ImageReward）+ 公开 137k 专家比较数据集（ImageRewardDB）**：建立了一套系统的"对齐/保真/无害"三维标注流水线与质控，把 NLP 的 RM 范式首次扎实地搬到 t2i，并证明 BLIP backbone + 冻结部分层是有效配方。
2. **ReFL——首个对扩散模型用 scorer 直接反传打分梯度的微调算法**：用"后段去噪步打分已可区分质量"的洞见，绕开 LDM 无 likelihood、无法做 PPO 的障碍，比同期"过滤数据/重加权"的间接法更直接有效。
3. **提出用 RM 替代 FID/CLIP 作 t2i 自动评测**：论证 FID（ρ=0.09）与人评几乎脱节，ImageReward（ρ=1.00）可作单图选优 + 跨模型排序的零样本指标。

**影响**
- 与 HPS、Pick-a-Pic 共同奠定 t2i 偏好对齐方向；ReFL 的"可微 reward 直接反传"思路成为后续 reward-finetuning（如 DRaFT、AlignProp）一脉的起点，与 RL 系（[[ddpo]]/[[d3po]]）、偏好系（[[diffusion-dpo]]）并列三条对齐路线。
- 工程上 `image-reward` 包 + SD Web UI 脚本被社区广泛用作打分/筛图工具；ImageReward 成为大量后续 t2i 论文的标配评测指标。
- 下一代 VisionReward（2024-12）扩展到细粒度多维、覆盖 text-to-video，做更稳定的视觉生成 RLHF。

**已知局限（论文 Appendix H）**
- 标注规模/多样性仍不足，prompt 全采自 DiffusionDB 存在偏置（真实使用远比"试奇怪 prompt"丰富）；单人标注+质控，多人拟合可能更一致。
- RM 训练受过拟合困扰，靠冻结层缓解；期待参数高效微调与更强更大图文 backbone 进一步提升。
- ReFL 仍是对原始 RLHF 的近似，缺乏严格理论保证，需要无偏高效的反馈学习算法。
- 单一 RM 不能代表人类审美多样性（Broader Impact 自述），缓解办法是训多个 RM 并限制单一 RM 的使用。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2304.05977
- arxiv_pdf: https://arxiv.org/pdf/2304.05977
- github: https://github.com/THUDM/ImageReward
- hf_model: https://huggingface.co/THUDM/ImageReward （已抓到 raw README，是 GitHub README 的严格子集，无独有信息）
- hf_dataset (ImageRewardDB): https://huggingface.co/datasets/THUDM/ImageRewardDB
- 中文博客（官方）: https://zhuanlan.zhihu.com/p/639494251 （知乎 JS 反爬，curl 直连/代理均返回挑战页，**未能获取**；需交互式无头浏览器。其为论文同内容的中文科普，无新数字）
- 下一代: https://github.com/THUDM/VisionReward

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2304.05977.pdf
- ../../../sources/omni/2023/raft-reward-diffusion--readme.md
- ../../../sources/omni/2023/raft-reward-diffusion--hf-datasetcard.md
- ../../../sources/omni/2023/raft-reward-diffusion--hf-modelcard.md
