---
title: "DDPO: Training Diffusion Models with Reinforcement Learning"
org: "UC Berkeley / MIT"
country: US
date: "2023-05"
type: paper
category: method
tags: [diffusion, rl, rlhf, rlaif, policy-gradient, ppo, mdp, text-to-image, reward-optimization, vlm-feedback]
url: "https://arxiv.org/abs/2305.13301"
arxiv: "https://arxiv.org/abs/2305.13301"
pdf_url: "https://arxiv.org/pdf/2305.13301"
github_url: "https://github.com/jannerm/ddpo"
hf_url: "https://huggingface.co/kvablack/ddpo-alignment"
modelscope_url: ""
project_url: "https://rl-diffusion.github.io/"
downloaded: [arxiv-2305.13301.pdf, ddpo--project-page.md, ddpo--bair-blog.md, ddpo--readme.md, ddpo-pytorch--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DDPO（Denoising Diffusion Policy Optimization）把扩散模型的**多步去噪过程重新建模为一个 T 步的 MDP**，从而能用策略梯度（REINFORCE / PPO 式重要性采样）**直接最大化任意黑盒奖励**（美学、压缩率、prompt 对齐），而不再依赖最大似然。它证明这种"逐步精确似然 + 策略梯度"显著优于"对最终样本做奖励加权似然"（RWR），并首次用 VLM（LLaVA）反馈在零人工标注下提升 prompt-image alignment——是扩散模型 RLHF/RLAIF 的奠基工作之一。

## 背景与定位
**要解决的问题**：扩散模型（[[ddpm]]、[[latent-diffusion-ldm]]）以变分下界近似最大似然来训练，目标是"匹配数据分布"。但大多数真实下游需求并不关心 likelihood，而关心**人感知质量、prompt 对齐、可压缩性、药效**等下游目标。这些目标往往：(1) 无法用 prompt 工程表达（如文件大小，因为训练语料里图像很少标注 file size）；(2) 难以程序化评估（如语义对齐），传统上要靠大规模人工标注。

**核心难点**：扩散模型的精确 likelihood（对整段去噪轨迹边缘化后的 $p_\theta(x_0|c)$）是**不可解的**，导致很多常规 RL 算法难以套用。

**DDPO 的关键洞察**：不要在"最终样本"层面计算似然，而是把**每一步去噪 $p_\theta(x_{t-1}|x_t,c)$ 当作一个可精确计算似然的策略动作**。标准采样器把单步反向过程参数化为各向同性高斯（见 [[ddpm]] 的 $\mathcal{N}(\mu_\theta, \sigma_t^2 I)$），所以单步对数似然及其梯度都是闭式可算的。

**技术脉络中的位置**：
- 对照前置工作 **Lee et al. (2023, "Aligning text-to-image models using human feedback")** —— 它对应"单轮 reward-weighted regression（RWR）"，DDPO 证明多步策略梯度显著超过它（即使 RWR 多轮交错训练也追不上）。
- 与 **[[dpok]]（Fan et al. 2023）并发**：两者都用策略梯度对齐扩散模型，但 DPOK 只考虑单一偏好奖励（ImageReward）、且主要为每个 prompt 训一个模型并加 KL 正则；DDPO 一次在多 prompt（最多 398 个）上训练、研究多种奖励函数、展示对未见 prompt 的泛化，且不用 KL 正则在 ImageReward 上反而全面超过 DPOK（附录 C）。
- 沿用 **Fan & Lee (2023)** 把去噪建为序列决策的思路，但把奖励从"GAN 判别器"推广为**任意黑盒奖励**。
- 是后续扩散偏好对齐（[[d3po]]、Diffusion-DPO 等）的直接前驱。

## 模型架构
DDPO 本身**是训练算法，不引入新网络架构**——它在现成的预训练 T2I 扩散模型上做 RL 微调。论文所有主实验的 backbone：

- **基座**：Stable Diffusion v1.4（[[stable-diffusion-1]]，潜空间 LDM，U-Net 去噪器 + 冻结的 VAE + 冻结的 CLIP text encoder）。仅微调 **U-Net 权重**，text encoder 与 autoencoder 全程冻结。
- **采样器与策略形式**：固定采样器，去噪步数 $T=50$，CFG guidance weight $w=5.0$。策略 $\pi(a_t|s_t)\triangleq p_\theta(x_{t-1}|x_t,c)$ 即去噪器输出的各向同性高斯——这正是能精确算单步似然的关键（相比 RWR 把整个 $p_\theta(x_0|c)$ 当策略，那是任意复杂分布、似然不可算）。
- **MDP 映射**（DDPO 的核心建模，把方法讲清楚）：
  - 状态 $s_t \triangleq (c, t, x_t)$（上下文/prompt、当前去噪时间步、当前噪声潜变量）
  - 动作 $a_t \triangleq x_{t-1}$（下一步去噪结果）
  - 转移 $P$ 是确定性的（Dirac），把 $t\to t-1$、$x_t\to x_{t-1}$
  - 初始状态 $\rho_0$：prompt 分布 $p(c)$ 与 $x_T\sim\mathcal{N}(0,I)$
  - 奖励 $R(s_t,a_t)= r(x_0,c)$ 仅在最后一步（$t=0$）给，其余步为 0；故整条轨迹累积奖励 = $r(x_0,c)$，最大化 RL 目标 = 最大化 $J_{\text{DDRL}}(\theta)=\mathbb{E}_{c\sim p(c),\,x_0\sim p_\theta(\cdot|c)}[r(x_0,c)]$。
- **PyTorch 复现版**额外支持 **LoRA**（kvablack/ddpo-pytorch），用 LoRA 微调 SD 时显存 < 10GB；附录 C 与 DPOK 对比那组实验也用 SD v1.5 + LoRA（学习率提到 3e-4）。

## 数据
DDPO 的特色是**几乎不需要训练数据集**——RL 微调的"数据"是模型自己在线采样的去噪轨迹 + 奖励函数打分，不需图文对、不需人工标注。具体"prompt 数据"很小：

- **Compressibility / Incompressibility**：prompt 从 ImageNet-1000 全部 **398 个动物**类别均匀采样。
- **Aesthetic Quality**：prompt 从 **45 个常见动物**的小列表均匀采样（论文附录 D.6 列全：cat/dog/horse/... 等）。
- **Prompt-Image Alignment**：prompt 形如"a(n) [animal] [activity]"，animal 取自同样 45 个动物，activity 取自 **3 个活动**（"riding a bike""playing chess""washing dishes"）。
- 采样分辨率固定 **512×512**（为使 file-size 奖励只由可压缩性而非分辨率决定）。
- **奖励函数即"标注来源"**（替代人工标注），四类：
  1. **JPEG 压缩率**（程序化，文件 kB 的负/正值）；
  2. **美学质量**——**LAION aesthetics predictor**（在 **176,000** 条人类图像评分上训练的线性模型，建在 CLIP embedding 上，打分 1–10），因为基于人类判断，故构成 RLHF；
  3. **prompt 对齐（RLAIF）**——用 **LLaVA** VLM 对生成图问"what is happening in this image?"，再用 **BERTScore recall** 衡量 VLM 描述与原 prompt 的语义相似度作为奖励，**完全无需额外人工标注/数据收集**；
  4. 附录 C 与 DPOK 对比时用 **ImageReward** 作奖励。
- 数据/安全过滤、re-captioning、合成数据等大规模数据工程**不适用**（DDPO 不做预训练，只做奖励驱动微调）。

## 训练方法
**核心目标**：直接最大化 $J_{\text{DDRL}}(\theta)$（期望奖励），而非似然。把方法讲清楚：

**（1）对照基线 RWR（reward-weighted regression）**——把去噪建为**单步 MDP**（状态=c，动作=最终样本 $x_0$），用标准 DDPM 去噪损失但按奖励加权：
- 软权重 $w_{\text{RWR}}=\frac{1}{Z}\exp(\beta r)$（指数化保非负，$\beta$ 为逆温度）；
- 稀疏权重 $w_{\text{sparse}}=\mathbb{1}[r\ge C]$（只保留奖励超阈值的样本，等价于反复"过滤式微调"）。
- 缺陷：DDPM 损失只是 log-likelihood 的**变分下界**而非精确似然，RWR 又只用最终样本忽略序列结构 → **两层近似**，理论不严格、效果差。

**（2）DDPO 两个变体**（在多步 MDP 上做策略梯度）：
- **DDPO_SF（score function / REINFORCE）**：$\nabla_\theta J = \mathbb{E}\big[\sum_{t=0}^T \nabla_\theta\log p_\theta(x_{t-1}|x_t,c)\,r(x_0,c)\big]$。每轮采样只能做**一步**梯度更新（必须 on-policy）。
- **DDPO_IS（importance sampling，PPO 式）**：引入重要性权重 $\frac{p_\theta(x_{t-1}|x_t,c)}{p_{\theta_{\text{old}}}(x_{t-1}|x_t,c)}$，允许在同一批数据上做**多步**更新。用 **PPO 式 clip** 实现 trust region，但需要**极小的 clip range = 1e-4**（远小于常规 RL 任务）。DDPO_IS 是最佳算法。

**关键实现 trick（多来自附录 D/E，论文没明说但很重要）**：
- **逐 prompt 奖励归一化**：奖励归一化到零均值单位方差，且**按每个 prompt 独立**用 running mean/std 跟踪（相当于策略梯度里的 value baseline / advantage-weighted regression）。这对"a dolphin riding a bike"这种初始零成功率 prompt 至关重要——靠跨 prompt 的可迁移学习才有信号。
- **CFG training（附录 E.1，关键工程发现）**：常规 CFG 在采样时混合条件/无条件预测 $\tilde\epsilon=w\epsilon_\theta(x_t,t,c)+(1-w)\epsilon_\theta(x_t,t)$。RL 里不该训无条件目标（奖励依赖 context），但**只训条件目标会导致第一轮微调后性能急剧崩坏**（猜测是每次更新后 guidance weight 失准、样本退化、毒害下一轮）。解决：固定 guidance weight，**训练时也用 guided ε-prediction**。该技巧对"多于一轮交错采样/训练"的方法必不可少。
- **数据分布（on-policy 程度，附录 E.2）**：DDPO 每轮只采 **256** 个样本（强 on-policy，策略梯度所需）；RWR 每轮采 **10,000** 个（off-policy）。消融显示 RWR 增加交错频率有帮助但到某点反而退化，且**任何交错程度都追不上 DDPO 的渐近性能**。
- **超参（附录 D.5）**：优化器 AdamW，lr=1e-5，weight decay=1e-4，β=(0.9,0.999)，grad clip norm=1.0。DDPO_SF：每轮 256 样本、1 次更新、batch 256；DDPO_IS：每轮 256 样本、拆 4 个 minibatch、4 次更新、batch 64、clip range 1e-4。梯度总是在单样本的所有去噪步上累积。
- **未做的事**：DDPO **不研究过优化（overoptimization）的防治**，也**不用 KL 正则**——论文坦言用"早停"（手动选模型开始退化前的最后一个 checkpoint）作为应对（附录 A），并把过优化防治列为重要 future work。
- **蒸馏/步数加速**：本工作**不涉及** consistency/LCM/ADD 等加速（去噪步固定 50）。

## Infra（训练 / 推理工程）
- **原始研究代码（JAX，jannerm/ddpo）**跑在 **Google Cloud TPU**：RWR 用 **TPU v3-128 pod**，DDPO 用 **TPU v4-64 pod**，二者均约 **4 小时**达到 50k 样本（计算由 Google TPU Research Cloud 捐赠）。conda 环境名 `ddpo-tpu`（`environment_tpu.yml`），README 明言**未在 GPU 上测试**。（更细的依赖清单未在已落盘源中给出。）
- **VLM 奖励的 LLaVA 推理**单独跑在一台 **DGX（8×80GB A100）** 机器上，通过 HTTP 请求调用（客户端在 `training/callbacks.py`，服务端为 kvablack/LLaVA-server 仓库）。
- **PyTorch 复现版（kvablack/ddpo-pytorch）**：支持 GPU + LoRA，LoRA 开启时单卡 < 10GB 显存即可微调 SD；作者用 **8×A100 DGX**，每个实验约 **4 小时 / 100 epochs**。所有 batch size 都是 per-GPU；每 epoch 生成图数 = `sample.batch_size × num_gpus × num_batches_per_epoch`，有效训练 batch = `train.batch_size × num_gpus × gradient_accumulation_steps`。需 Python ≥3.10、accelerate 启动。
- **推理加速**：DDPO 微调后的模型采样开销与普通扩散一致——附录 B 提到在 A100 上标准生成单图约 **4 秒**（对照 universal guidance 需近 **2 分钟/图**）。
- **生态**：HuggingFace `trl` 后来提供官方 `DDPOTrainer`（由 @metric-space 贡献，支持 LoRA），把 DDPO 纳入主流 RLHF 工具链。

## 评测 benchmark（把效果讲清楚）
DDPO 不用 FID/CLIPScore/GenEval 等标准 T2I 榜，而是**在自定义奖励曲线 + 与基线方法对比**上评估（抠论文里给出的具体数字）：

- **算法对比（图 4）**：在 compressibility / incompressibility / aesthetic 三任务上，**以"奖励函数查询次数"为横轴**（奖励评估是实际瓶颈），DDPO（两变体）在**全部三任务**都明显优于 RWR 两变体；DDPO 内部 **DDPO_IS 略胜 DDPO_SF**（因更新步数更多）。结论：把去噪建为多步 MDP 直接估策略梯度，比对"log-likelihood 变分下界"做奖励加权更有效。
- **vs Universal Guidance（附录 B，表 1，prompt "wolf"，50 样本均值±标准误）**：
  - Base model 美学分 **5.95 ± 0.03**
  - Universal guidance **6.14 ± 0.05**（仅小幅提升，且生成单图近 2 分钟）
  - **DDPO_IS @20k reward queries：6.63 ± 0.03**（提升大得多，且采样仅 4 秒/图）。
- **vs DPOK（附录 C，图 8）**：同 4 个 prompt（color/count/composition/location）、同用 ImageReward 训练、SD v1.5 + LoRA。**DDPO_IS 在 ImageReward 与 LAION 美学两个指标上全面超过 DPOK（across the board），且不用 KL 正则**。该实验同时充当过优化研究：用 ImageReward 训、用 LAION 美学评，发现 25k queries 内仅一个 prompt（count: "four wolves in the park"）出现明显过优化（美学分回落），整体过优化不严重；20k queries 时仍能出高质量图。
- **prompt 对齐（图 5）**：以 BERTScore 为奖励，训练中 BERTScore 随 reward queries 稳步上升（约 0.69→0.84 区间）；定性上样本对 prompt 的忠实度显著提升。注意有些 prompt（"a dolphin riding a bike"）基座模型零成功率、孤立训永远无信号，**只有跨 prompt 迁移**才让它们改善。
- **泛化（图 6 / 附录 F，图 12）**：仅用 45 动物训美学模型，能泛化到 **38 个未见动物**（泛化很好）与 **50 个日常物体**（toaster/chair/coffee cup 等，泛化稍弱）；prompt 对齐模型仅用 45 动物 × 3 活动训练，能泛化到未见动物、未见活动（"taking an exam"）乃至无生命物体。
- **过优化/reward hacking（附录 A，定性）**：优化 incompressibility 到后期模型退化为纯高频噪声、丢失语义；优化"n animals"计数对齐时 DDPO 学会**对 LLaVA 的 typographic attack**——直接在图上写"loosely resembling"目标数字的文字（如八只乌龟上写"sixx ttutttas"）来骗过 VLM。**无通用过优化防治法，靠人工早停。**
- 标准定量榜（FID、GenEval、T2I-CompBench、HPSv2、PickScore、人评 ELO 等）：**论文未报告**（这是一篇方法/RL 论文，不刷 T2I 榜）。

## 创新点与影响
**核心贡献**：
1. **把扩散去噪重构为 T 步 MDP**，用每步精确似然替代不可解的整体似然，使策略梯度（REINFORCE / PPO 式 IS）能**直接优化任意黑盒奖励**——理论与方法奠基。
2. 实证**多步策略梯度 > 奖励加权似然（RWR）**：序列建模 + 精确似然带来显著优化效率优势。
3. **VLM 反馈做 RLAIF**：用 LLaVA + BERTScore 在零人工标注下提升 prompt-image alignment，把语言模型 RLAIF（Constitutional AI 路线）迁移到扩散模型。
4. 揭示扩散 RL 的**意外泛化**（窄 prompt 训练泛化到未见对象/活动），呼应 LLM instruction-tuning 的跨语言泛化。

**对后续工作的影响**：DDPO 是扩散模型 RLHF/对齐的奠基性工作之一，直接催生了基于 DPO 的无奖励模型路线 [[d3po]]（D3PO 把 DPO 搬进 MDP）、Diffusion-DPO 等，以及把"pretrain + RL finetune"范式系统引入生成模型领域；HuggingFace `trl` 将其产品化为 `DDPOTrainer`。PyTorch + LoRA 复现把门槛降到单卡 <10GB。

**已知局限（作者自述）**：
- 实验规模小、prompt 多样性受限（多为"动物做活动"）；
- **过优化（reward hacking）严重且无通用解**——会退化成噪声或对 VLM 做 typographic attack，本工作只用手动早停规避；
- 未研究 KL 正则等防漂移手段（留给并发的 DPOK）；
- 奖励函数本身的质量/创造力决定上限（"the possibilities are limited only by the quality and creativity of your reward function"）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2305.13301
- arxiv_pdf: https://arxiv.org/pdf/2305.13301
- project_page: https://rl-diffusion.github.io/
- bair_blog（官方一等公民博客）: https://bair.berkeley.edu/blog/2023/07/14/ddpo/
- github（原始 JAX/TPU 代码）: https://github.com/jannerm/ddpo
- github（PyTorch + LoRA 复现）: https://github.com/kvablack/ddpo-pytorch
- hf_weights（4 个发布权重）: https://huggingface.co/kvablack/ddpo-alignment ｜ ddpo-aesthetic ｜ ddpo-compressibility ｜ ddpo-incompressibility
- llava_server: https://github.com/kvablack/LLaVA-server

## 一手源存档（sources/）
- [arxiv-2305.13301.pdf](https://arxiv.org/pdf/2305.13301)  （arXiv 原文 PDF，不入 git）
- [project-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/ddpo--project-page.md)
- [bair-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/ddpo--bair-blog.md)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/ddpo--readme.md)
- [ddpo-pytorch--readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/ddpo-pytorch--readme.md)
