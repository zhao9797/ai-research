---
title: "CogView3: Finer and Faster Text-to-Image Generation via Relay Diffusion"
org: "Zhipu AI / Tsinghua University"
country: China
date: "2024-03"
type: paper
category: t2i
tags: [t2i, relay-diffusion, cascaded-diffusion, latent-diffusion, distillation, recaption, unet, dit, cogview]
url: "https://arxiv.org/abs/2403.05121"
arxiv: "https://arxiv.org/abs/2403.05121"
pdf_url: "https://arxiv.org/pdf/2403.05121"
github_url: "https://github.com/THUDM/CogView3"
hf_url: "https://huggingface.co/THUDM/CogView3-Plus-3B"
modelscope_url: "https://modelscope.cn/models/ZhipuAI/CogView3-Plus-3B"
project_url: ""
downloaded: [arxiv-2403.05121.pdf, cogview3--github.md, cogview3plus--modelscope-readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CogView3 是首个把 **relay diffusion（中继扩散）** 用于文生图的级联框架：先在 512×512 低分辨率生成、再用"加噪重启"的中继超分逐级放大到 1024 甚至 2048。在人评中以 **77.0% 胜率**超过 SDXL，且只用约 **1/2 推理时间**；蒸馏版本（base 8 步 + 超分 2 步 / 甚至 4+1 步）在保持相当质量下把推理时间压到 SDXL 的 **1/10**（最快 1.47s）。

## 背景与定位
单阶段高分辨率扩散（如 SDXL 直接在 1024×1024 上去噪）每一步都在高分辨率隐空间计算，推理成本随分辨率二次方增长。一条主流加速路线是蒸馏（[[latent-consistency-models]]、ADD），但纯蒸馏常掉质量，除非引入 GAN loss，而 GAN loss 又让蒸馏复杂、训练不稳。

CogView3 走另一条路——**级联**。传统级联扩散（[[cascaded-diffusion-models]]、[[imagen]]）的超分阶段在**每一步**都把低分辨率结果做通道拼接作为条件，需要噪声增强来弥合"真实低分图 vs base 阶段生成图"的分布差。CogView3 改用清华团队自家的 **relay diffusion**（Teng et al. 2023, arXiv:2309.03350）：超分阶段不是"逐步条件"，而是**对低分辨率生成结果加高斯噪声、从这个被污染的图直接起步扩散**。这样超分阶段天然能"修正"上一阶段产生的瑕疵，且只需从扩散日程的**中途点**起步，步数大幅减少。

CogView3 把 relay diffusion 从原版的**像素空间**搬到**隐空间**，并用**线性模糊（linear blurring）日程**替代原版的 patch-wise 模糊，配套推导了对应的采样器。它承上启下：上接 [[cogview]] / [[cogview2]] 自回归路线、下启基于 [[latent-diffusion-ldm]] 的扩散路线，并在开源仓库里演进出 DiT 版的 **CogView3-Plus-3B**（2024-09 开源），再到 CogView4-6B（2025-03）。论文被 **ECCV 2024** 接收。

技术脉络：[[ddpm]] → [[latent-diffusion-ldm]] → [[cascaded-diffusion-models]] → relay diffusion → CogView3。

## 模型架构
**论文版 CogView3（级联 UNet）：**
- **Backbone**：30 亿参数（3B）文生图扩散模型，采用 **3-stage UNet** 架构。base 阶段与超分阶段**共享同一套架构**（progressive 训练衍生出多个 stage）。
- **隐空间**：在像素空间 **8× 压缩**的隐空间运行，压缩器是一个 **KL 正则化的 VAE（variational KL-regularized autoencoder）**。
- **文本编码器**：用**冻结的 T5-XXL**（Raffel et al.）做文本编码，注入 UNet 的 cross-attention；输入 token 长度设为 **225**（为了容纳扩写后的长 prompt）。
- **两阶段流水线**：base 阶段生成 512×512；第二阶段做 **2× 超分**，512×512 → 1024×1024；超分阶段可**直接迁移到更高分辨率并迭代套用**，最终可达 **2048×2048**（更高如 4096×4096 需配 tiled diffusion）。
- **条件注入**：纯文本条件（T5-XXL embedding 进 cross-attention），无额外图像条件分支（超分通过隐空间中继的"起点"传递低分信息，而非通道拼接）。

**开源 CogView3-Plus-3B（DiT 版，与论文不同）：**
- README/model card 明确这是 **Diffusion Transformer（DiT）** 版本，单模型支持 **512–2048px**（宽高须 32 整除），不再是级联 UNet 中继结构。
- 文本编码器仍为 **T5-XXL**，prompt 语言英文，**224 token** 上限。精度 **BF16 / FP32**（FP16 会溢出导致黑图）。
- 注：CogView3-Plus 的 DiT 具体结构细节论文未覆盖（论文只写级联 UNet 版），仅在仓库/card 中以工程口径披露。再后续的 CogView4-6B 换成 **GLM-4-9B** 编码器、支持中英双语、1024 token。

## 数据
- **基础数据源**：**LAION-2B**（[[latent-diffusion-ldm]] 同源的 LAION 系列），先做安全过滤——用预定义子串列表屏蔽一批与不良图像关联的源链接，移除涉政、色情、暴力内容。
- **Re-caption（重写描述）**：对标 [[dall-e-3]] 的"better captions"思路。DALL-E-3 的重写模型的指令微调数据来自人工标注，CogView3 改为**自动用 GPT-4V** 构造 `<image, old_cap, new_cap>` 三元组：prompt GPT-4V 对图像提若干问答（第一问强制是简要描述），最后把答案与原 caption 合成新 caption。
- 共收集约 **70,000 条 recaption 三元组**，用来微调 **CogVLM-17B** 得到 recaption 模型（batch size 256、1,500 步，刻意"适度"微调防过拟合），再用它**重写整个训练集**。
- **替换比例**：训练时把 **95%** 的原始 caption 替换为新生成的长 caption（与 DALL-E-3 一致）。
- **美学微调数据**：release 版 base 模型在一个**高美学内部数据集**上额外微调 10,000 步。
- **Prompt 扩写（推理侧）**：因训练用长 recaption 而用户输入往往很短，存在训练/推理失配。推理前用 LLM 把用户短 prompt 扩成详细描述（保留原意），人评显示扩写后偏好更高。模板与示例见论文附录 B。

## 训练方法
**训练目标**：标准 latent diffusion 的 ε/x0 预测 MSE（base 阶段）；超分阶段用专门推导的 **latent relay diffusion** 目标。
- **中继前向过程**：给定图 x0 与其低分版 xL=Downsample(x0)，编码到隐空间 z0、zL，定义**线性模糊变换** z0^t = (Tr−t)/Tr · z0 + t/Tr · zL（t∈{0,…,Tr}，z0^{Tr} 恰好等于 zL），前向加噪 q(zt|z0)=N(z0^t, σt²I)。训练损失即 UNet 去噪器 D 对 z0 的重建 MSE（见论文式 6）。
- **采样器**：从 base 生成结果 X^L 双线性上采样到 xL，编码 z0^{Tr}=E(xL)，加噪得起点 z_{Tr}=z0^{Tr}+σ_{Tr}ε，按 DDIM 范式反向（系数 a_t、b_t、c_t 见 Algorithm 1），实践中取 δt=0 即 ODE 采样。附录 A 给了"采样器与前向过程一致"的归纳法证明。

**多阶段渐进训练**（仿 SDXL，省总成本，各 stage 共享架构）：
- base：256×256 训 **600,000 步**（bs 2048）→ 续训 512×512 **200,000 步**（bs 2048）→ 高美学内部集微调 **10,000 步**（bs 1024）得 release base。
- 超分：在预训练 512×512 模型基础上，先在 1024×1024 训 **100,000 步**（bs 1024）→ 再用 relay 超分损失微调 **20,000 步**（bs 1024）得最终超分模型。

**蒸馏与加速**：结合 **progressive distillation**（Salimans & Ho / Meng et al.）与 relay 框架。
- base 阶段按标准扩散蒸馏；超分阶段把模糊日程并入蒸馏训练，每轮把采样步数减半（teacher 两步 ↔ student 一步，见式 8/9，损失为 ẑ_{t−2} 与 z_{t−2} 的 MSE）。
- 把 **CFG 强度 w** 作为可学习投影 embedding 加到 timestep embedding 里（首轮蒸馏即融入、后续轮直接以 w 为条件），免去独立适配阶段。
- 因超分从中途起步、任务更易，最终步数可分配为 **base 8 + 超分 2** 步，甚至 **base 4 + 超分 1** 步，质量基本保留。

**关键超参（评测设置）**：总扩散日程 1000 步，中继**起点设在 500**（消融选出的中点最优）；base 采 50 步、超分采 10 步，CFG=7.5，对比均在 1024×1024。

## Infra（训练 / 推理工程）
- 论文**未披露**总算力/GPU·时/并行方案/混合精度等训练基础设施数字（仅给出各阶段步数与 batch size）。
- **推理成本**（batch size=4 实测，论文 Table 1/2）：CogView3 50+10 步 = **10.33s**（SDXL 50 步 19.67s，Stable Cascade 20+10 步 10.83s）；蒸馏版 4+1 步 = **1.47s**、8+2 步 = 1.96s（LCM-SDXL 4 步 2.06s）。低分辨率推理成本随分辨率二次方减小，是"省钱"的关键。
- **更高分辨率推理**：直接在 2048/4096 上跑超分会爆 CUDA 显存，改用 **tiled diffusion**（Mixture of Diffusers / MultiDiffusion）把单步切成重叠小块再融合，可在有限显存下出 2048×2048（4096×4096 留作未来工作）。
- **开源 CogView3-Plus-3B 工程口径**（ModelScope card）：A100 上 **1s/step**；BF16/FP32（FP16 溢出黑图）；显存占用（A100, bs=1, BF16）：512² 19GB/cpu-offload 11GB、1024² 23GB/11GB、2048² 25GB/11GB。CogView4-6B 的 DiT 显存（bs=4, BF16）：1024² 35GB（offload 后 20GB，text-encoder 4bit 13GB）。

## 评测 benchmark（把效果讲清楚）
所有数字来自已抓取的一手源（arXiv PDF + GitHub README）。机器指标用 **Aesthetic Score（Aes）、HPS v2、ImageReward、FID**，全部在 1024×1024、bs=4 计时。

**DrawBench / PartiPrompts（论文 Table 1）：**

| Model | Steps | Time | DrawBench Aes / HPSv2 / ImageReward | PartiPrompts Aes / HPSv2 / ImageReward |
|---|---|---|---|---|
| SDXL | 50 | 19.67s | 5.54 / 0.288 / 0.676 | 5.78 / 0.287 / 0.915 |
| StableCascade | 20+10 | 10.83s | 5.88 / 0.285 / 0.677 | 5.93 / 0.285 / 1.029 |
| **CogView3** | 50+10 | **10.33s** | **5.97 / 0.290 / 0.847** | **6.15 / 0.290 / 1.025** |
| LCM-SDXL | 4 | 2.06s | 5.45 / 0.279 / 0.394 | 5.59 / 0.280 / 0.689 |
| **CogView3-distill** | 4+1 | **1.47s** | 5.87 / 0.288 / 0.731 | 6.12 / 0.287 / 0.968 |
| **CogView3-distill** | 8+2 | 1.96s | 5.90 / 0.285 / 0.655 | 6.13 / 0.288 / 0.963 |

CogView3 在 ImageReward 上对 SDXL 提升明显（DrawBench 0.847 vs 0.676），多数指标领先，唯 PartiPrompts ImageReward 略输 Stable Cascade（1.025 vs 1.029）。

**COCO-5k（论文 Table 2，含 FID）：**

| Model | Steps | Time | FID↓ | Aes↑ | HPSv2↑ | ImageReward↑ |
|---|---|---|---|---|---|---|
| SDXL | 50 | 19.67s | 26.29 | 5.63 | 0.291 | 0.820 |
| StableCascade | 20+10 | 10.83s | 36.59 | 5.89 | 0.283 | 0.734 |
| **CogView3** | 50+10 | 10.33s | 31.63 | **6.01** | **0.294** | **0.967** |
| LCM-SDXL | 4 | 2.06s | 27.16 | 5.39 | 0.281 | 0.566 |
| CogView3-distill | 4+1 | 1.47s | 34.03 | 5.99 | 0.292 | 0.920 |
| CogView3-distill | 8+2 | 1.96s | 35.53 | 6.00 | 0.293 | 0.921 |

注：CogView3 的 **FID 31.63 高于 SDXL 的 26.29**（FID 越低越好），但 Aes/HPSv2/ImageReward 与人评均胜，作者据此论证 FID 不完全反映人类偏好。

**人评（DrawBench，pairwise win/lose/tie）：**
- vs SDXL：原始 prompt 平均胜率 **77.0%**（对齐 + 美学），扩写 prompt 胜率 **74.8%**。
- vs Stable Cascade：原始 prompt **78.1%**，扩写 prompt **82.1%**。
- 蒸馏版（8+2 步）人评显著优于 LCM-蒸馏 SDXL（4 步）。

**关键消融：**
- **中继起点**（DrawBench）：200/1000 偏模糊、800/1000 引入伪影，**500 最优**（HPSv2 0.290 / ImageReward 0.847）。
- **Prompt 扩写**：对 CogView3 显著提升指令跟随（因训练用长 recaption + 225 token 窗口），对 SDXL 几乎无益甚至受损（SDXL 仅 77 token 窗口，长 prompt 被截断）。
- **迭代/tiled 超分**：tiled diffusion（Mixture of Diffusers）在 2048×2048 上与直接超分质量相当但省显存。

**CogView3-Plus / CogView4 的 benchmark**：GitHub README 给出的 DPG-Bench（CogView4-6B 85.13）、GenEval（0.73）、T2I-CompBench、中文文本准确率等**均为 CogView4-6B 数据，并非论文版 CogView3 或 CogView3-Plus-3B**——CogView3-Plus-3B 自身的标准化 benchmark 分数在抓取到的一手源中**未单独报告**。

## 创新点与影响
**核心贡献：**
1. **首个把 relay diffusion 引入文生图**：用"加噪重启"的中继超分替代传统级联的"逐步通道拼接条件"，超分阶段能修正前阶段瑕疵，且只需从扩散日程中途起步，步数与成本大幅下降。
2. **隐空间 relay + 线性模糊日程**：把原版像素级 relay 搬进隐空间，用简单线性模糊变换 + 配套 ODE/DDIM 采样器（含一致性证明），工程上更轻。
3. **relay 友好的渐进蒸馏**：因超分从中途起步、误差更小，蒸馏后可压到 base 4 + 超分 1 步（1.47s ≈ SDXL 1/10 时间）仍保质量；并把 CFG 强度作为条件 embedding 融入，免独立适配阶段。
4. **数据侧 recaption pipeline**：GPT-4V 自动造 recaption 数据 → 微调 CogVLM-17B → 全量重写 + 推理侧 prompt 扩写，闭环对齐训练/推理分布。

**影响：**CogView3 是 Zhipu/清华 CogView 系列从自回归（[[cogview]]/[[cogview2]]）转向扩散的承上启下之作；开源后衍生出 DiT 版 **CogView3-Plus-3B**（2024-09）与双语 **CogView4-6B**（2025-03，GLM-4-9B 编码器、原生中文），并被集成进 diffusers（`CogView3PlusPipeline`）与 CogKit 微调工具链。中继思路为"低分主干 + 轻量高质超分"的效率范式提供了一个区别于纯蒸馏/纯级联的样本。论文获 **ECCV 2024**。

**已知局限：**
- FID 不及 SDXL（作者归因于 FID 与人类偏好脱节，但仍是客观短板）。
- 论文版仅英文、T5-XXL 编码、强依赖 prompt 扩写补齐短 prompt。
- 4096×4096 仅靠 tiled 推理、未端到端训练，留作未来工作。
- **训练 infra（算力/GPU·时/并行）全程未披露**；CogView3-Plus-3B 的 DiT 架构细节与独立 benchmark 也未在一手源中给全。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2403.05121
- arxiv_pdf: https://arxiv.org/pdf/2403.05121
- github: https://github.com/THUDM/CogView3 （现重定向至 https://github.com/zai-org/CogView4 ，托管 CogView4/CogView3-Plus/CogView3）
- hf_model: https://huggingface.co/THUDM/CogView3-Plus-3B
- modelscope_model: https://modelscope.cn/models/ZhipuAI/CogView3-Plus-3B
- relay_diffusion_precursor: https://arxiv.org/abs/2309.03350 （Relay Diffusion, Teng et al. 2023）

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2403.05121.pdf
- ../../../sources/omni/2024/cogview3--github.md
- ../../../sources/omni/2024/cogview3plus--modelscope-readme.md
