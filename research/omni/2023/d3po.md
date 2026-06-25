---
title: "D3PO: Using Human Feedback to Fine-tune Diffusion Models without Any Reward Model"
org: "Tsinghua University (SIGS) / Parametrix Technology"
country: China
date: "2023-11"
type: paper
category: method
tags: [diffusion, rlhf, dpo, preference-alignment, reward-free, mdp, text-to-image, cvpr2024]
url: "https://arxiv.org/abs/2311.13231"
arxiv: "https://arxiv.org/abs/2311.13231"
pdf_url: "https://arxiv.org/pdf/2311.13231"
github_url: "https://github.com/yk7333/D3PO"
hf_url: "https://huggingface.co/datasets/yangkaiSIGS/d3po_datasets"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2311.13231.pdf, d3po--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
D3PO（Direct Preference for Denoising Diffusion Policy Optimization）把 LLM 的 [[dpo]] 直接搬到扩散模型上：**把去噪过程建模为多步 MDP，再把 DPO 的理论扩展进 MDP**，从而无需训练独立的奖励模型即可用成对人类偏好直接微调扩散模型。理论证明"不训奖励模型直接更新策略"等价于"先学到最优奖励模型再用它指导策略"；实验上仅靠相对偏好（不用真实奖励数值）就能取得与用真奖励训练的 [[ddpo]]/[[dpok]] 接近的效果，且在 prompt-image alignment 上人评偏好率达 **55.7%**（对比无微调 14.7%、Reward Weighted 18.7%）。CVPR 2024 接收。

## 背景与定位
**要解决的问题**：把 RLHF 用到扩散模型上，此前的主流路线（[[ddpo]]、[[dpok]]、ReFL/ImageReward、Reward-Weighted）都要先训一个奖励模型 $r_\phi$，再用 RL（policy gradient）去最大化奖励。但造一个鲁棒奖励模型需要大量成对数据、精心的架构与超参调优，代价高昂；某些任务（判断手是否畸形、图像是否安全/NSFW）甚至缺乏可靠的自动判别模型。

**为什么不能直接套 DPO**：NLP 里的 DPO（[[dpo]]，Rafailov 2023）绕开奖励模型、用偏好对 $(x, y_w, y_l)$ 直接优化语言模型。但 DPO 把整句话当作一个输出，需要存多次前向的梯度。扩散模型的一条去噪轨迹含 20–50 个 latent，每张图（即便用 LoRA）约占 6G 显存；若要对整条轨迹 $\pi_\theta(\sigma)=\prod_t \pi_\theta(s_t,a_t)$ 计算梯度，显存需求 >100G，几乎不可训。

**D3PO 的位置**：作者称这是**首个无需奖励模型即可微调扩散模型**的工作。技术脉络上，它沿用 [[ddpo]] 把去噪视作 MDP 的思路（Black et al. 2023），但把优化目标从"policy gradient 最大化奖励"换成"DPO-style 的逐步偏好对比"，是**扩散 DPO 的代表性早期工作之一**（与并行的 Diffusion-DPO 路线呼应）。基座生成器用 [[stable-diffusion]] v1.5。

## 模型架构
D3PO 是一个**微调/对齐算法**，不引入新生成架构；它作用在现成的扩散模型上：

- **基座生成器**：实验主用 Stable Diffusion v1.5（[[latent-diffusion-ldm]] 系 U-Net + VAE + CLIP text encoder）；为验证泛化性，畸形修复实验还用了 Anything v5（动漫风 SD 变体）。
- **可训练部分**：仅用 **LoRA** 微调 U-Net，**冻结 text encoder 与 autoencoder**。LoRA 只更新 U-Net attention block 内 **key/query/value 线性层**的参数，大幅压低显存。
- **策略概率的显式计算**：网络仍是标准 SD 的噪声预测器 $\epsilon_\theta$；反向一步建模为高斯 $p_\theta(x_{t-1}|x_t,c)=\mathcal N(x_{t-1};\mu_\theta(x_t,c,t),\sigma_t^2 I)$，其中均值由 $\epsilon_\theta$ 经 DDPM 公式 $\mu_\theta=\tfrac1{\sqrt{\alpha_t}}\!\big(x_t-\tfrac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta\big)$ 反推（Algorithm 1 第 28 行）。策略概率 $\pi_\theta(x_{t-1}|x_t)$ 即用该高斯密度显式计算，$\pi_{ref}$ 同理用冻结的 $\epsilon_{ref}$ 算——这使 DPO 的策略概率比 $\pi_\theta/\pi_{ref}$ 在每个去噪步可逐点求出。
- **MDP 映射（核心设计）**：把去噪一步对应成 MDP 一步——
  - 状态 $s_t \triangleq (c,\,t,\,x_{T-t})$（prompt、时间步、当前 latent）
  - 动作 $a_t \triangleq x_{T-1-t}$（下一步去噪结果）
  - 策略 $\pi(a_t|s_t)\triangleq p_\theta(x_{T-1-t}|c,t,x_{T-t})$
  - 转移为确定性 Dirac $\delta$；初始分布 $\rho_0=(p(c),\delta_0,\mathcal N(0,I))$。

  这套映射让"一条去噪轨迹"成为一段 MDP segment，从而可以在 segment 层面定义偏好。

## 数据
D3PO 是算法论文，**无大规模预训练数据集**；用到的是各任务的**成对偏好/标注样本**，规模都不大、由作者团队自采或人工标注：

- **可量化目标实验（§5.1，用相对目标值代替人评）**：每 epoch 生成 80 张样本，共 400 epoch；prompt 为 **45 种常见动物**（cat/dog/horse/…，附录全列）。目标含 compressibility（图像文件越小越好）、incompressibility（越大越好）、aesthetic（用 LAION 美学预测器打分）。
- **手部畸形修复（§5.2.1）**：prompt 仅用 `"1 hand"`；每 epoch 给 1000 张图人工分类是否畸形，跑 5 epoch。
- **动漫角色畸形（§5.2.1）**：用 Anything v5；初始从动漫游戏收集 **483 张插画**，过滤掉非角色后留 **442 张**，再用 SD-WebUI 的 autotagging 反推出 442 条 prompt。假设"未被选中（非畸形）的图优于畸形图"，但畸形/非畸形组内不再排序。
- **图像安全/NSFW（§5.2.2）**：用"擦边"模糊 prompt（如 `ambiguous beauty`、`provocative art`，附录列了一批）诱导模型生成正常或 NSFW 图；每 epoch 1000 张，跑 10 epoch。因人对"是否安全"判断分歧小，仅用 **2 名标注员**（1 标注 + 1 复核）。
- **Prompt-image alignment（§5.2.3）**：从 ImageReward（[60]）取 **10000 条 prompt**（涵盖艺术、人物、户外、动物等）；每 epoch 用 4000 条 prompt、每条生成 2 张图，由 **16 名标注员**给偏好，跑 10 epoch。
- **标注工具**：基于开源 `sd-webui-infinite-image-browsing` 自建网页做人工偏好标注；数据集已开源在 HF `yangkaiSIGS/d3po_datasets`。

清洗/配比/合成数据等细节：除上述各任务规模外**未额外披露**。

## 训练方法
**核心目标（reward-free 的逐步 DPO 损失）**——从 KL 正则的 RL 目标出发推导：
$$\max_\pi \mathbb E_{s\sim d^\pi,a\sim\pi}[Q^*(s,a)] - \beta D_{KL}[\pi(a|s)\,\|\,\pi_{ref}(a|s)]$$
其最优策略（Proposition 1）为 $\pi^*(a|s)=\pi_{ref}(a|s)\exp(\tfrac1\beta Q^*(s,a))$，反解出 $Q^*(s,a)=\beta\log\frac{\pi^*(a|s)}{\pi_{ref}(a|s)}$。把 Bradley-Terry 偏好里的累积奖励 $\sum_t r^*(s_t,a_t)$ 用 $Q^*(s_k,a_k)$ 替换，得到逐 segment 的损失：
$$L(\theta)=-\mathbb E\Big[\log\rho\big(\beta\log\tfrac{\pi_\theta(a_k^w|s_k^w)}{\pi_{ref}(a_k^w|s_k^w)} - \beta\log\tfrac{\pi_\theta(a_k^l|s_k^l)}{\pi_{ref}(a_k^l|s_k^l)}\big)\Big]$$
形式上与 LLM 的 DPO 完全同构，只是把"整句概率比"换成"MDP 中某 state-action 的策略概率比"。

**关键 trick——sub-segment 数据增强**：人只能对**最终图 $x_0$** 给偏好，中间态是噪声/半成品无法判优。借鉴 AlphaGo/扑克 AI 等"赢则全程动作 $r=+1$、输则全程 $r=-1$"的思路，**假设若整段被偏好，则该段里每个 state-action 对都优于另一段对应的对**。于是把一条长为 $T$ 的轨迹拆成 $T$ 个 sub-segment $\sigma_i=\{s_i,a_i,...,s_{T-1},a_{T-1}\}$，对每个 $i\in[0,T-1]$ 都算一遍上式损失（Eq.14）。这使**单段轨迹的数据利用率提升 $T$ 倍**——这是 D3PO 相对"只更新 $\pi_\theta(\cdot|s_0)$"的关键改进。实现上偏好用 $h_k\in\{[1,-1],[-1,1],[0,0]\}$ 标记胜/负/平。

**理论保证**：Proposition 2 证明用 $Q^*$ 替换累积奖励后定义的偏好分布 $\tilde p^*$ 与真实 $p^*$ 的偏差被界在 $O\!\big(\tfrac{\xi}{\delta}(\exp(\sigma^2)-1)\big)$；当 $Q$ 估计方差 $\sigma^2\to0$ 时偏差趋于 0。这从理论上把"不训奖励模型"与"等价于用最优奖励模型"挂钩。

**训练流程**（Algorithm 1，无奖励模型版）：① 复制冻结一份 $\epsilon_{ref}=\epsilon_\theta$（requires_grad=False）；② 每 prompt 从同一初始噪声 $x_T$ 采多张图（distortion/safety 任务每 prompt 7 张，alignment 任务 2 张），采样阶段 **no grad**；③ 人工给偏好；④ 训练阶段对每个时间步、每条轨迹 **with grad** 算 $\pi_\theta/\pi_{ref}$ 并按 D3PO loss 更新 $\theta$。**每个 epoch 微调后的模型作为下一 epoch 的 reference model**（迭代式偏好对齐）。

**关键超参（Table 2）**：lr=3e-5；优化器 Adam（$\beta_1$=0.9, $\beta_2$=0.999，weight decay 1e-4）；梯度裁剪 norm=1.0；推理总步数 $T$=20；DPO 温度 $\beta$=0.1；per-GPU batch size=10；每 epoch batch 采样数 n=2；DDIM 的 $\eta$=1.0；梯度累积步=1；CFG 权重 w=5.0；有奖励模型微调跑 N=400 epoch；混合精度 fp16。

蒸馏/加速（consistency/LCM/步数蒸馏）：**不涉及**（本工作不做采样加速，仅 20 步 DDIM 推理）。

## Infra（训练 / 推理工程）
- **硬件**：4 × Tesla V100 32G（论文附录 E 明确给出）。算力规模相对很小——这正是"无需奖励模型 + LoRA + 逐步 MDP 分解"省显存带来的好处。
- **软件栈**：Python 3.10.12、PyTorch 2.0.1、Diffusers 0.17.1、Accelerate 0.22.0、huggingface-hub 0.16.4、Numpy 1.25.2、Torchmetrics 1.0.2。
- **显存控制**：仅 LoRA 微调 U-Net 的 attention q/k/v 线性层，冻结 text encoder 与 VAE；把 DPO 从"整条轨迹一次性反传（>100G）"改为"逐步 MDP 的 state-action 对反传"，是显存可行的关键。
- **分布式**：用 `accelerate` 做分布式/多卡训练（`accelerate config` + `accelerate launch`），支持单卡或多卡。
- **训练管线（无奖励模型）分两段**：先 `sample.py` 批量采样并落盘每张图的 latent 与 prompt 到 `/data`，人工网页标注后整理成 JSON，再 `train.py` 微调；有奖励模型版直接 `train_d3po.py`。
- **GPU·时 / 吞吐 / 量化部署**：未报告。

## 评测 benchmark（把效果讲清楚）
**1）可量化目标（§5.1，对比需奖励模型的方法）**：在 compressibility / incompressibility / aesthetic（LAION 美学分）三任务上，D3PO **仅用偏好的相对大小**（A 的目标值 > B 即偏好 A，不用奖励数值本身）训练，测试时所有方法都用真实奖励作为评测标准。结果（Figure 3，5 个种子）：D3PO 的曲线**与用标准奖励训练的 [[ddpo]]、[[dpok]]、Reward-Weighted 几乎持平**。结论：即便存在奖励模型，D3PO 也能持续抬高奖励、达到目标——说明"只用相对偏好"足以驱动有效对齐。

**2）Prompt-image alignment（§5.2.3，Table 1，唯一给出绝对数字的对比表）**：

| 方法 | CLIP score ↑ | BLIP score ↑ | ImageReward ↑ | 人评偏好 ↑ |
|---|---|---|---|---|
| 不微调 | 30.7 | 1.95 | 0.04 | 14.7% |
| 用 preferred images 微调 | 31.0 | 1.97 | 0.08 | 11% |
| Reward Weighted | 31.5 | 2.01 | 0.17 | 18.7% |
| **D3PO** | **31.9** | **2.06** | **0.27** | **55.7%** |

D3PO 在四项指标上全面最优；**人评偏好率 55.7% 远超次优**，ImageReward 分（0.27）也显著高于 Reward-Weighted（0.17）。指标用 torchmetrics 的 CLIP score、BLIP（model_base.pth）、ImageReward（THUDM/ImageReward）计算；人评由额外 5 名评估者对 300 条 prompt 逐对判优。

**3）无奖励模型的难任务（人评/通过率曲线，无对照基线绝对数字表）**：
- **手部畸形修复**：5 epoch 内手部"正常率"明显上升、五指正确率提高（Figure 4/9）。
- **动漫角色畸形（Anything v5）**：畸形率随 epoch 先快速下降后趋稳（Figure 4/6）。
- **图像安全**：10 epoch 后模型稳定产出安全图、无 explicit 内容（Figure 5/10）。

**消融/关键结论**：核心消融即 Eq.12（只用 $s_0$）vs Eq.14（sub-segment 全程），后者把数据利用率提升 $T$ 倍，是方法奏效的关键。FID/GenEval/T2I-CompBench/MJHQ-30K/HPSv2/PickScore 等标准生成 benchmark **均未报告**（本工作聚焦定制对齐任务而非通用 T2I 刷榜）。

## 创新点与影响
**核心贡献**：
1. **首个无需奖励模型微调扩散模型**的方法：把 DPO 从 NLP 迁到扩散，绕开"先训奖励模型"的昂贵环节。
2. **DPO→MDP 的理论扩展**：证明在 MDP 中直接按偏好更新策略，等价于"先学最优奖励模型再指导更新"（Prop 1/2），为 reward-free 对齐提供理论基础。
3. **逐步 MDP 分解 + sub-segment 增强**：把整轨迹 DPO（>100G 显存）化为逐 state-action 对的可训目标，并通过 sub-segment 把数据利用率提升 $T$ 倍，使在 4×V100 上 LoRA 微调成为可能。
4. **打开"无自动奖励"任务**：手/全身畸形、NSFW 安全等缺乏可靠判别模型的任务，可纯靠人工成对反馈对齐。

**影响**：D3PO 是 2023 年底"扩散 DPO/reward-free 偏好对齐"潮流的代表工作之一（与 Diffusion-DPO 等并行），CVPR 2024 接收，代码与数据开源，被后续扩散偏好对齐研究广泛引用/对比，推动了"把 LLM 对齐范式（DPO）系统性迁移到生成模型"的方向。

**已知局限**：
- **sub-segment 假设较强**——"整段被偏好则段内每一步都更优"对中间噪声态不一定成立，可能引入噪声梯度；理论界依赖 $Q$ 估计方差小。
- **重度依赖人工标注**：难任务（畸形/安全）仍需人逐张选图，规模化成本高；论文也承认对手/美学这类任务缺可靠 RLAIF 判别模型才退回人评。
- **评测覆盖窄**：只在自定义任务上验证，未报告通用 T2I 标准 benchmark；基座限于 SD v1.5 / Anything v5（U-Net 系），未验证 DiT/大模型。
- 推理仍 20 步 DDIM，不含采样加速。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.13231
- arxiv_pdf: https://arxiv.org/pdf/2311.13231
- github: https://github.com/yk7333/D3PO
- hf_dataset（README 引用）: https://huggingface.co/datasets/yangkaiSIGS/d3po_datasets

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2311.13231.pdf
- ../../../sources/omni/2023/d3po--readme.md
