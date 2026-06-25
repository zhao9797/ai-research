---
title: "训练方法：目标函数·多阶段·偏好对齐·蒸馏"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [training, objective, flow-matching, rectified-flow, preference-alignment, rlhf, dpo, grpo, distillation, few-step, consistency, sampler, editing, survey, omni]
---

# 训练方法：目标函数 · 多阶段流程 · 偏好对齐 · 蒸馏与少步

> 横向综述章节。脉络：①**训练目标**怎么从「预测噪声 ε」一路演化到「回归直线速度场」和「预测下一个 token / 还原被掩 token」；②大模型怎么把训练拆成**预训练→分辨率渐进→SFT→偏好对齐**的多阶段课程；③**偏好对齐**这一从 LLM 搬来的「最后一段」如何在扩散/流/自回归上各自落地（reward-finetune / RL / DPO / GRPO）；④**蒸馏与少步**怎么把几十步采样压成 1–4 步，以及配套的快速采样器。所有数字均引自本调研下的单工作页（每页已对抗式核过），用 `[[slug]]` 内链。

---

## 一、训练目标：ε → v → flow matching/rectified flow → next-token → masked

### 1.1 起点——预测噪声 ε（2020）

现代生成式视觉训练目标的母体是 [[ddpm]]（UC Berkeley, 2020-06）：它把扩散模型重参数化为「网络预测加进去的噪声 ε」，配一个去权重的简化 MSE（L_simple），把训练目标压成一行均方误差，并揭示其与去噪分数匹配 + 退火 Langevin 的等价性——无条件 CIFAR-10 IS=9.46 / FID=3.17（当时 SOTA）。这套 ε-prediction 成为此后所有扩散 T2I（[[improved-ddpm]]、[[latent-diffusion-ldm]]、[[imagen]]、Stable Diffusion）的默认目标。[[elucidating-edm]]（NVIDIA, 2022-06）进一步把训练目标「解耦」：用 σ_data=0.5 归一化、c_skip/c_out/c_in 预处理外壳让网络在「预测干净信号 y」与「预测噪声 n」间自适应插值，并把训练噪声分布改成对数正态 `ln σ ~ N(-1.2, 1.2²)`、损失加权 `λ(σ)=1/c_out²`——这两项（config E）是 EDM 在 CIFAR-10 把 FID 从 config D 的 2.09 降到 1.88、最终配方刷到 conditional **1.79**、ImageNet-64 重训 **1.36** 的主因。EDM 的参数化此后被 [[consistency-models]]、SD3 等几乎所有现代扩散配方沿用。

### 1.2 高分辨率下的过渡——v-prediction（2022）

[[stable-diffusion-2]]（Stability AI, 2022-11）在 768×768 上把目标从 ε 换成 **v-prediction**（预测速度量 v 而非噪声 ε，来自 Salimans & Ho 的 Progressive Distillation, arXiv:2202.00512），因为高分辨率、高 guidance 下数值更稳；base 模型仍用 ε-pred、768-v 模型由 base 微调而来。v-prediction 是「ε 时代」走向「直线流时代」之间的过渡参数化。

### 1.3 范式跃迁——flow matching / rectified flow（2022→2024 上规模）

2022 年三件奠基工作几乎同时把目标从「匹配 score」改为「回归连接两分布的速度场」：
- [[rectified-flow]]（UT Austin, 2022-09）：对线性插值方向 `X1−X0` 做最小二乘回归学 ODE 漂移，把生成与域迁移统一成「运输映射」；配 **reflow** 迭代拉直轨迹 + 蒸馏，实现单步（1-NFE）生成——CIFAR-10 蒸馏后的 2-rectified flow **FID 4.85 / recall 0.50**（击败 TDPM 的 8.91），全步 1-rectified flow **FID 2.58 / recall 0.57**。
- [[flow-matching]]（Meta FAIR / Weizmann, 2022-10）：提出 simulation-free 的 **Conditional Flow Matching**（证明边际向量场损失与逐样本条件向量场损失梯度等价），并用最优传输（OT）直线路径替代扩散曲线路径——ImageNet-128 仅 500k iter 即超过 ADM 基线 4.36m iter 的训练量，FID **20.9**；FM-OT 在 NLL/FID/NFE 三项一致优于 DDPM/Score Matching/ScoreFlow。

这条路线在 2024 年被 [[stable-diffusion-3]]（Stability AI, 2024-03）**用大规模控制变量实验「坐实」**：61 种公式 × 2 数据集 × 多采样器横评，证明 **rectified flow + 中间步加权（logit-normal 时间采样）** 确实优于标准扩散；配 MMDiT（文/图各持一套权重、仅在注意力处拼接，双向信息流），depth=38 的 8B 模型在 GenEval 上 1024² w/DPO **0.74**（超 DALL·E 3 的 0.67）。此后旗舰几乎全转 flow：[[flux-1]]（BFL）与 [[qwen-image]]（阿里, 2025-08，20B MMDiT）都以 flow matching 为预训练目标——Qwen-Image 的损失即「latent z=E(x)、x1~N(0,I)、t 从 logit-normal 采样、插值 xt=t·x0+(1−t)·x1、回归目标速度 vt=x0−x1 的 MSE」，是 SD3 公式的标准复刻。

### 1.4 离散路线——next-token 与 masked-token

与「连续速度场」并行的是把图像离散成 token 后用语言建模目标：
- **next-token（自回归）**：[[emu3]]（BAAI, 2024-09，8B）把图/文/视频全离散成 token，用单一自回归解码器做纯 next-token 预测，不用扩散/CLIP/外接 LLM，图像生成超 SDXL、视频 VBench 80.96。[[x-omni]]（腾讯混元 X, 2025-07，Qwen2.5-7B）同样对图文 token 做同质 next-token，但用 RL 修复自回归的累积误差与量化信息损失（见 §三）。
- **masked-token（掩码生成）**：[[muse]]（Google, 2023-01）在 VQGAN 离散 token 上做掩码预测 + 交叉熵，掩码率从截断 arccos 分布采样（期望 **0.64**，强偏高掩码），推理时按置信度并行解码——base 仅 24 步、super-res 仅 8 步，3B 模型 512² 单图 1.3s（TPUv4，比 Imagen-3B/Parti-3B 快 >10×），zero-shot COCO FID 7.88。可视为以 `[MASK]` 为吸收态的离散扩散。

四种目标（ε/v 扩散、flow、next-token、masked）在 2024–2026 的统一/omni 模型里常被**混合**使用（如 [[transfusion]] 文走 next-token、图走扩散；[[bagel]]/[[show-o2]] 等混合路线），但训练目标本身的演化主线就是上面这条「从噪声预测到直线速度回归、再到离散 token 建模」。

---

## 二、多阶段流程：预训练 → 分辨率渐进 → SFT → 偏好对齐

早期方法论工作（[[ddpm]]/[[flow-matching]]/[[rectified-flow]]）都是**单阶段从头训练**，无 SFT/对齐。产业级 T2I 把训练拆成一条课程流水线，[[stable-diffusion-3]] 给出最清晰的四段式模板：

1. **预训练**：256² 低分辨率、batch **4096**、2×2 patch、预编码数据上训 500k 步（最大 depth=38/8B 模型在 3×10⁵ 步处调 lr 防发散）。
2. **高分辨率微调**：混合宽高比、加 QK-RMSNorm 稳定，目标分辨率上调到 512²/1024²；并按 **分辨率相关的 timestep shift**（高分辨率像素更多需更多噪声破坏信号，对应 log-SNR 偏移 `log(n/m)`，1024² 用 α=3.0）。
3. **偏好对齐**：1024² 上用 **Diffusion-DPO**（只给线性层加 LoRA rank=128，8B 微调 2k 步）——见 §三。
4.（采样侧）文本编码器训练时各以 46.3% 概率独立 drop，使推理可任取子集（去 T5 省 4.7B 显存，对美学无损但复杂排版掉到 38% win）。

[[qwen-image]] 把这套课程写得更细——「**progressive curriculum** 沿四条轴渐进」：分辨率 256→640→1328；文本从无→有→段落级；数据质量从海量→精炼；数据分布从不均衡→均衡（并用合成数据补长文本等稀缺分布）。预训练后接 **SFT（专攻短板、引导高写实/细节）+ RL（DPO 大规模离线 + Flow-GRPO 小规模精修）** 两阶段后训练，GenEval 从 SFT 的 0.87 经 RL 升到 **0.91**（榜上唯一破 0.9 的基础模型）。离散路线的多阶段同理：[[x-omni]] 是「预训练 3 阶段（42B→629B→42B 退火 token）→ SFT（1.5B token）→ RL（GRPO 200 步）」；[[muse]] 是「VQGAN → base 掩码 Transformer → super-res Transformer → 微调 VQGAN 解码器」的顺序训练（base 3B 训 1.5M 步）。

值得注意：**SFT 阶段的「质量微调」在高质量底模上可能反而有害**——[[diffusion-dpo]] 报告，在 Pick-a-Pic 赢图上做 SFT 能提升 vanilla SD1.5（胜率 55.5%），但**对 SDXL 任何程度的 SFT 都会变差**（因 Pick-a-Pic 图质量低于 SDXL-1.0 base），这与原 DPO 论文「已对齐模型不再受益于 preferred-FT」一致，也是多阶段流水线必须用「偏好对齐」而非「再 SFT」来做最后一段的实证依据。

---

## 三、偏好对齐与奖励：从 reward-finetune 到 RL/DPO/GRPO

把 LLM 的「RLHF 最后一段」搬到生成模型，2023 年涌现出三条并行路线，外加一套支撑它们的奖励/评测标尺。

### 3.1 奖励模型与评测标尺：ImageReward / HPS-v2 / PickScore

- [[raft-reward-diffusion]]（ImageReward & ReFL，清华/智谱, 2023-04）是**首个通用 t2i 人类偏好奖励模型**：BLIP backbone（cross-attention 融合图文，优于 CLIP 双塔）+ MLP head，用 137k 对专家比较（覆盖「对齐/保真/无害」三轴）训练，偏好预测准确率 **65.14%**（CLIP 54.82 / Aesthetic 57.35 / BLIP 57.76）；并论证 zero-shot FID 与人评几乎脱节（Spearman ρ=0.09，而 ImageReward ρ=1.00）。配套的 **ReFL** 是首个对扩散模型直接反传 scorer 梯度的微调算法——利用「去噪后段（t≥30）直接预测图已可区分质量」的洞见，只在随机选的较后一步带梯度解码打分反传，微调后 SD v1.4 人评胜率 **58.4%**（RAFT 随迭代加深过拟合 RM 而崩到 20.97%）。
- [[hps-v2]]（CUHK MMLab/SenseTime, 2023-06）针对图像来源偏差（纳入 9 模型 + COCO 真实图）与 prompt 偏差（ChatGPT 清洗风格词）做去偏，在 OpenCLIP ViT-H/14 上微调（只解冻图像塔末 20 层 + 文本塔末 11 层，4000 步），偏好预测准确率 **83.3%**（>PickScore 79.8 / HPS v1 77.6 / ImageReward 74.0），并给出 4 风格×800 prompt 的稳定打榜协议。

ImageReward / HPS-v2 / PickScore 三者构成 t2i 偏好的「三大标尺」，既当评测又当奖励信号——后面 RL/DPO/GRPO 路线几乎都用它们打分。

### 3.2 RL 路线：DDPO / D3PO

- [[ddpo]]（UC Berkeley/MIT, 2023-05）把多步去噪重建模成 **T 步 MDP**（状态=(c,t,x_t)、动作=x_{t-1}、奖励只在末步给），从而用策略梯度（REINFORCE 的 DDPO_SF / PPO 式重要性采样 DDPO_IS，clip range 极小 1e-4）直接最大化任意黑盒奖励。它证明「多步策略梯度 > 对最终样本做奖励加权（RWR）」，并首次用 VLM（LLaVA + BERTScore）做 **RLAIF** 零人工标注提升 prompt 对齐（如 wolf 美学分从 base 5.95 提到 6.63）。代价：reward hacking 严重（优化计数时学会对 LLaVA 做 typographic attack），无通用过优化防治、靠手动早停。
- [[d3po]]（清华 SIGS, 2023-11, CVPR 2024）把 DPO 直接扩进 MDP，**无需训练奖励模型**：证明「直接按偏好更新策略」等价于「先学最优奖励模型再指导更新」，并用 **sub-segment 增强**（假设整段被偏好则段内每个 state-action 对都更优）把数据利用率提升 T 倍，使 4×V100 + LoRA 可训。Prompt-image alignment 人评偏好率 **55.7%**（vs 不微调 14.7%、Reward-Weighted 18.7%），且能做「手部畸形修复」「NSFW 安全」等缺乏自动判别器的任务。

### 3.3 DPO 路线：Diffusion-DPO

[[diffusion-dpo]]（Salesforce/Stanford, 2023-11）把 LLM 的 DPO 首次严格推广到扩散模型：用 ELBO + 前向近似把 intractable 的链上偏好似然化简为只需「赢/输两张图各加噪一次、各算一次 ε-预测」的可微闭式损失（Eq.14），无在线 rollout、无显式奖励模型。在 Pick-a-Pic v2 的 85.1 万对上对齐 SDXL，PartiPrompts 通用偏好胜率 **70.0%**（vs SDXL-base），并以 3.5B 打赢 6.6B 的 SDXL(base+refiner) 完整管线（胜率 69%）；其隐式奖励模型偏好分类准确率 72.0% 甚至超过 PickScore（64.2%）。这一目标稳定、可离线、零额外推理开销，迅速成为产业旗舰的标配最后一段——[[stable-diffusion-3]] 的第 4 阶段用的就是它（LoRA rank=128）。

### 3.4 Flow-GRPO：流模型上的 RL（2025）

到 2025，旗舰把 RL 从「DPO 离线」升级为「DPO + GRPO」两段：[[qwen-image]] 先用 DPO 大规模离线对齐（基于 flow matching 准则构造 DPO 目标），再用 **Flow-GRPO** 做小规模细粒度精修——组内 G 张图算标准化优势，并把无随机性的 flow 采样**改写为 SDE 过程（Euler-Maruyama）以引入探索随机性**，KL 项有闭式解。离散自回归侧，[[x-omni]] 用 **GRPO**（200 步、每 prompt 16 rollout、KL β=0.01）配多分量奖励（HPSv2 + Unified Reward + Qwen2.5-VL-32B 图文对齐 + GOT-OCR2.0/PaddleOCR 文字准确率），证明 RL 能修复离散 AR 图像生成长期的低保真/畸变/文字渲染差，DPG-Bench 87.65 取统一模型 SOTA 且无需 CFG。

> 一句话脉络：奖励标尺（ImageReward→HPS-v2→PickScore）打底，RL（DDPO/D3PO）与 DPO（Diffusion-DPO）两条路线在 2023 年并起，2025 年在 flow/AR 模型上收敛为「DPO 离线 + GRPO 精修」的产业范式。

---

## 四、蒸馏与少步：把几十步压成 1–4 步

扩散/流模型的迭代采样是部署瓶颈。加速分两支：**改采样器**（免训练，§4.3）与**蒸馏**（训练换步数，§4.1–4.2）。

### 4.1 一致性路线：Consistency → LCM → LCM-LoRA

- [[consistency-models]]（OpenAI, 2023-03）提出「自一致性」：学一个把 PF-ODE 轨迹上任意点直接映回原点的函数 f，从而单步生成。两种训练——CD（蒸馏现成扩散，借 target network + EMA + stopgrad 稳定）与 CT（完全独立、无需扩散教师），均无对抗、无需预构合成数据集。CIFAR-10 单步 **FID 3.55**、ImageNet-64 单步 **6.20**（一致优于 Progressive Distillation 的 8.34/15.39）。
- [[latent-consistency-models]]（清华 IIIS, 2023-10）把一致性蒸馏搬进 Stable Diffusion 潜空间，提出**一阶段引导蒸馏**（把 CFG 直接蒸进网络输入，推理每步只一次前向）+ **Skipping-Step**（约束「当前步与 k 步外」一致，k=20，把上千步时间表压到几十），仅 **~32 A100 卡时（4000 步）** 就蒸出 768² 的 2–4 步高清模型——512² 4 步 **FID 11.10**（DDIM 22.38 / Guided-Distill 15.12）。
- [[lcm-lora]]（清华/Hugging Face, 2023-11）把蒸馏结果固化为 LoRA「加速向量」（SDXL 可训练参数 3.5B→**197M**），并发现它能与风格 LoRA 做免训练线性叠加（task arithmetic，λ1=0.8/λ2=1.0），成为通用 PF-ODE 求解器插件——4090 上 SDXL 从 3.4s（25 步）降到 **0.7s（4 步）**。

### 4.2 对抗/分布匹配路线：ADD → DMD；以及无蒸馏的 MeanFlow

- [[sdxl-turbo-add]]（Stability AI, 2023-11）的 **ADD（Adversarial Diffusion Distillation）** 把「对抗损失（hinge + R1，判别器用冻结 DINOv2 特征 + 轻量头 + text/image 双条件）+ 分数蒸馏（λ=2.5，等价 SDS）」合成混合目标，**从预训练扩散权重初始化学生**（随机初始化直接坍塌：FID 293.6 vs 20.6）。SDXL-Turbo 单步即胜过 4 步 LCM-XL、4 步胜过 50 步教师 SDXL，A100 上端到端 512² **207ms**（单次 U-Net 前向 67ms），推理免 CFG。其潜空间续作 LADD 见 [[sd3-5-turbo-adversarial-diffusion-distillation]]。
- [[dmd]]（MIT/Adobe, 2023-11）的 **DMD（Distribution Matching Distillation）** 不要求学生复刻教师逐点映射，只要分布不可区分：用 real score（固定教师）− fake score（在线 critic）之差当近似 KL 梯度，再加 LPIPS 回归损失防模式坍缩（两者缺一不可：去回归损失 ImageNet 5.61→坍缩、去分布匹配 9.21→缺真实感）。ImageNet-64 单步 **FID 2.62**（教师 EDM 512 步 2.32，仅差 0.3 却快 512×），零样本 COCO-30k 单步 **11.49**（教师 SD1.5 50 步 8.78），512² 单图 90ms / 20 FPS。
- [[mean-flows]]（CMU+MIT 何恺明组, 2025-05）走「**无蒸馏、从零、单阶段**」：用「平均速度场」替代瞬时速度，从定义直接推出 MeanFlow Identity（用 JVP + stop-gradient 高效计算，仅 ~16% 额外开销）当训练目标，并把 CFG 烘焙进真值场保持严格 1-NFE。ImageNet-256 单步 **FID 3.43**（XL/2, 676M；相对 Shortcut 10.60 提升近 70%、IMM 7.77 提升 >50%），2-NFE 2.20（已与 250×2 步的 DiT/SiT 同档）——几乎抹平单步与多步差距，且不依赖任何预训练教师。

> 三条蒸馏路线的对照：一致性（约束「同轨迹输出一致」）→ 对抗+分数（拿 GAN 单步速度 + 扩散质量/组合性）→ 分布匹配（双 score 之差当 KL 梯度，避开对抗博弈）；MeanFlow 则跳出「蒸馏」框架，用原理性的平均速度恒等式直接从零训单步模型。教师轨迹的来源，正是下面的快速采样器。

### 4.3 配套采样器：DDIM / DPM-Solver

- [[ddim]]（Stanford, 2020-10）把 DDPM 的马尔可夫扩散推广为非马尔可夫族，得到确定性（σ=0）采样器：训练目标与 DDPM 完全相同、无需重训，却能把 1000 步压到 20–100 步——CelebA 20 步 DDIM ≈ 100 步 DDPM（10×–50× 加速）。其确定性轨迹还赋予可逆性（DDIM inversion），成为 prompt-to-prompt / null-text inversion 等编辑的基石，也为后续一致性/ADD/DMD 提供「教师 ODE 轨迹」。
- [[dpm-solver]]（清华 TSAIL/人大, 2022-06）利用扩散 ODE 的「半线性」结构（线性部分解析求解、非线性部分化成指数加权积分），用指数积分器的高阶 Taylor 展开把高质量采样压到约 **10–20 步**（CIFAR-10 10 NFE FID 4.70 / 20 NFE 2.87，约 5× 于此前最佳求解器），并证明 **DDIM ≡ DPM-Solver-1**。其改进版 DPM-Solver++（数据预测参数化 + 动态阈值 + 多步法）解决大引导尺度下的失稳，成为 diffusers / Stable Diffusion 的默认快速采样器。

注意三者关系：**采样器（DDIM/DPM-Solver）≠ 蒸馏**——它们改的是「怎么解 ODE」、不重训模型、留全部信息；蒸馏（CM/LCM/ADD/DMD）改的是「训一个少步学生」、固化为特定步数。前者常作为后者的教师。

---

## 五、编辑训练范式：指令编辑 / 多任务 / 条件控制

图像编辑的训练范式区别于纯 T2I，主要在「如何造监督信号」和「如何注入条件」：

- [[instructpix2pix]]（UC Berkeley, 2022-11）开创**指令式编辑**：核心不在模型而在**全合成数据**——用微调后的 GPT-3 生成「指令 + 改前/改后 caption」三元组（45 万+条），再用 Stable Diffusion + [[prompt-to-prompt]]（共享注意力保证两次生成一致）造配对图（CLIP 三道阈值过滤，发布版 313,010 对）。模型从 SD v1.5 微调，第一层卷积加输入通道（zero-init）拼接输入图 latent，训练目标仍是标准 ε-pred 去噪；关键 trick 是**双条件 CFG**（图像 s_I、文本 s_T 各一个 scale），仅 10,000 步 / 8×A100 / 25.5h。
- [[emu-edit]]（Meta, 2023-11）把编辑升级为**多任务生成**：16 种「编辑 + 识别（检测/分割/深度）+ 生成」任务统一成生成任务，自建 1000 万样本数据集（Llama-2-70B 造指令 + Grounded Precise Editing 用 DINO+SAM 预生成精确 mask + 四道过滤掉 70%）。核心创新是 **learned task embedding**（每任务一个可学习向量，与 U-Net 联合训练注入，消解指令歧义）+ **task inversion**（冻结主干只学新 embedding，单样本即可适配新任务）。实证「加入 CV 识别任务能反哺编辑精度」，自建 benchmark 上人评对 InstructPix2Pix 偏好率 **77.3%**。
- [[controlnet]]（Stanford, 2023-02, ICCV 2023 最佳论文）解决「小数据微调大模型不灾难性遗忘」：**冻结底模 + 克隆可训练编码器副本 + 零初始化 1×1 卷积（zero convolution）**接回——训练第一步两个零卷积输出为 0，底模行为完全不变，随后从 0「生长」。深度条件 ControlNet 仅 20 万样本 + 单张 3090Ti + 5 天，就与「千 GPU-时 / 1200 万图」的工业 SD2-Depth 几乎无法区分（用户辨别精度 0.52±0.17≈瞎猜）。其消融揭示「深 encoder 的价值在无 prompt 时仍能从条件图识别语义」（Guess Mode）。

这三者代表编辑训练的三种范式：**合成配对数据 + 微调**（InstructPix2Pix）、**多任务 + task embedding**（Emu Edit）、**冻结底模 + 旁路条件网络**（ControlNet）。2025 年的 [[flux-1-kontext]]/[[qwen-image-edit]]/[[seededit-3-0]] 等把它们与 flow matching、in-context 拼接、MLLM 语义嵌入进一步融合，但训练范式的根仍在这三条线上。

---

## 附：本章硬线索速查

| 维度 | 谁 / 时间 | 用什么方法 | 把什么指标推到多少 |
| --- | --- | --- | --- |
| 训练目标 | [[ddpm]] 2020 | ε-prediction + L_simple | CIFAR-10 FID 3.17 |
| 训练目标 | [[elucidating-edm]] 2022 | lognormal σ + λ=1/c_out² | CIFAR-10 cond FID 1.79 / ImageNet-64 1.36 |
| 训练目标 | [[rectified-flow]] 2022 | 直线速度回归 + reflow | 单步蒸馏 FID 4.85（CIFAR-10） |
| 训练目标 | [[flow-matching]] 2022 | CFM + OT 直线路径 | ImageNet-128 FID 20.9（500k iter） |
| 目标上规模 | [[stable-diffusion-3]] 2024 | RF + 中间步加权 + MMDiT | GenEval 0.74（1024² w/DPO） |
| 多阶段 | [[qwen-image]] 2025 | 课程预训练 + SFT + DPO + Flow-GRPO | GenEval 0.87→0.91 |
| 奖励模型 | [[raft-reward-diffusion]] 2023 | BLIP RM + ReFL | 偏好准确率 65.14%，ReFL 人评 58.4% |
| 奖励模型 | [[hps-v2]] 2023 | OpenCLIP ViT-H 末层微调 | 偏好准确率 83.3% |
| RL | [[ddpo]] 2023 | 去噪 MDP + 策略梯度 + RLAIF | wolf 美学 5.95→6.63 |
| reward-free RL | [[d3po]] 2023 | DPO→MDP + sub-segment | 对齐人评偏好率 55.7% |
| DPO | [[diffusion-dpo]] 2023 | ELBO 重写偏好似然 | PartiPrompts 胜率 70.0% |
| 一致性蒸馏 | [[consistency-models]] 2023 | 自一致性 CD/CT | CIFAR-10 单步 FID 3.55 |
| 潜空间蒸馏 | [[latent-consistency-models]] 2023 | LCD + Skipping-Step | 512² 4 步 FID 11.10（~32 A100h） |
| LoRA 加速器 | [[lcm-lora]] 2023 | task arithmetic | SDXL 4 步 0.7s（4090） |
| 对抗蒸馏 | [[sdxl-turbo-add]] 2023 | ADD（对抗+分数蒸馏） | 单步 207ms，单步胜 4 步 LCM-XL |
| 分布匹配蒸馏 | [[dmd]] 2023 | real−fake score 差 + LPIPS | ImageNet-64 单步 FID 2.62 |
| 无蒸馏单步 | [[mean-flows]] 2025 | MeanFlow Identity（JVP） | ImageNet-256 单步 FID 3.43 |
| 采样器 | [[ddim]] 2020 | 非马尔可夫确定性采样 | 20 步≈DDPM 100 步 |
| 采样器 | [[dpm-solver]] 2022 | 半线性 + 指数积分器 | CIFAR-10 20 NFE FID 2.87 |
| 指令编辑 | [[instructpix2pix]] 2022 | GPT-3+SD+P2P 合成数据 + 双 CFG | 45 万对，10k 步微调 |
| 多任务编辑 | [[emu-edit]] 2023 | 16 任务 + task embedding | 对 IP2P 人评偏好 77.3% |
| 条件控制 | [[controlnet]] 2023 | 冻结底模 + 零卷积旁路 | 20 万样本/单卡 5 天≈工业模型 |
