---
title: "ILVR: Conditioning Method for Denoising Diffusion Probabilistic Models"
org: "Seoul National University / Samsung SDS"
country: "South Korea"
date: "2021-08"
type: paper
category: method
tags: [diffusion, ddpm, training-free, conditioning, image-translation, editing, low-pass-filter, iccv2021]
url: "https://arxiv.org/abs/2108.02938"
arxiv: "https://arxiv.org/abs/2108.02938"
pdf_url: "https://arxiv.org/pdf/2108.02938"
github_url: "https://github.com/jychoi118/ilvr_adm"
hf_url: ""
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2108.02938.pdf, ilvr--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
ILVR（Iterative Latent Variable Refinement）是一种**training-free（学习无关）**的条件扩散采样方法：在无条件 DDPM 的每一步去噪后，用参考图像的**低频分量**替换采样结果的低频分量，从而把生成轨迹引导向"与参考图低频一致"的图像子集。单个无条件模型即可零额外训练地完成多域图像翻译、paint-to-image、scribble 编辑等任务（ICCV 2021 Oral）；FFHQ 上 N=4 时 FID 4.62、N=8 时 7.24，质量与无条件 baseline（FID 11.38）相当甚至更优。

## 背景与定位
2021 年扩散模型刚被证明在无条件生成上能匹敌 SOTA GAN（[[ddpm]]、[[improved-ddpm]]、guided-diffusion ADM），但**可控生成**仍是难题：DDPM 反向过程每步都注入随机噪声 z，即使从同一初始噪声出发，高层语义也会发散，无法稳定生成"想要的内容"。

当时控制生成模型有两条路线：
1. **训练条件模型**（segmentation/style/inpainting 条件，以及与本工作并行的 SR3 把 DDPM 训成超分模型）——效果好但每个任务都要重训，只能在训练设定内工作。
2. **利用预训练无条件模型**——已有大量基于 GAN 的工作（GANSpace、InterFaceGAN、Image2StyleGAN/PULSE 等）通过把图像投影到 StyleGAN/BigGAN 隐空间再操纵隐向量来编辑，但这套范式建立在 GAN 上，**从未在迭代式生成模型（DDPM）上探索过**。

ILVR 填的正是这个空白：它把"利用预训练无条件模型"的思路第一次搬到 DDPM 上，且**不需要隐空间反演、不需要分类器/分割等额外模型**，仅靠一个低通滤波器在采样循环里做"latent 匹配"。它与同期的 [[guided-diffusion-adm]]（classifier guidance）形成对照——guidance 需要额外训一个噪声鲁棒分类器并对 logits 求梯度，ILVR 则**完全无梯度、无额外网络**，是后续一大批 training-free 扩散编辑/复原方法（如 RePaint、SDEdit、DDRM、各类零样本逆问题求解）的早期源头之一。论文相关工作 5.1–5.4 把谱系梳理得很清楚（score-based → DDPM → 各类条件生成）。

## 模型架构
ILVR **本身不引入新网络**——它是一个采样时（inference-time）算法，作用于任意已训练好的无条件 DDPM。

- **Backbone**：直接复用 Ho et al. DDPM 的 U-Net（基于 Wide ResNet），含 group normalization、16×16 分辨率上的 self-attention 块、正弦位置编码、固定线性方差 schedule β₁..β_T（见附录 C.3）。开源实现（ilvr_adm）则基于 OpenAI guided-diffusion 的 ADM U-Net，给出的采样配置为：`attention_resolutions=16, num_channels=128, num_head_channels=64, num_res_blocks=1, resblock_updown=True, use_scale_shift_norm=True, learn_sigma=True, image_size=256, diffusion_steps=1000, linear noise schedule`。
- **核心算子 φ_N(·)**：一个线性**低通滤波**操作 = 下采样到 1/N 再上采样回原分辨率，**保持图像维度不变**。实现用 ResizeRight（Shocher）做正确的 bicubic 下/上采样。N 是唯一的"分辨率级"超参（论文用 N∈{4,8,16,32,64}）。
- **采样修正（Algorithm 1 / Eq.8）**：每步先按标准 DDPM 反向公式（Eq.5）采一个**无条件提案** x'_{t-1} ~ p_θ(·|x_t)；再把参考图 y 按前向扩散加噪到同一时刻得到 y_{t-1} ~ q(y_{t-1}|y)（Eq.3）；然后做 latent 匹配：
  `x_{t-1} = φ_N(y_{t-1}) + ( I − φ_N )(x'_{t-1})`
  即**用参考图的低频替换提案的低频，保留提案自己的高频**。如此每一步都强制 φ_N(x_{t-1}) = φ_N(y_{t-1})，等价于在条件子集 R_N(y)={x : φ_N(x)=φ_N(y)} 内采样。
- **理论近似（附录 A）**：作者证明这一步对真正的条件转移 p_θ(x_{t-1}|x_t, φ_N(x_0)=φ_N(y)) 是一个合理近似——利用 x_0 的闭式估计 f_θ(x_t,t)=(x_t−√(1−ᾱ_t)·ε_θ)/√ᾱ_t 与 φ 的线性性，把"约束最终图像低频"局部化为"约束每步 latent 低频"。
- **条件注入**：没有 cross-attention、没有 text encoder、没有 VAE/tokenizer——它是**像素空间**的 DDPM，条件信息纯粹通过"低频替换"注入。这是它与后来 [[latent-diffusion-ldm]] 系（文本条件、隐空间）路线完全不同的地方。

**两个可控旋钮**（3.2 节，给用户对"与参考的语义相似度"的控制）：
1. **下采样因子 N**：N 越大 → 条件子集 R_N 越宽（R_N ⊂ R_M for N≤M）→ 样本越多样、只共享粗粒度信息（色调）；N 越小 → 越贴近参考的细节（发型、瞳色、耳环）。
2. **条件步数范围 [b,a]**：只在部分时间步施加匹配（如 1000→500）。限制范围 → 子集变宽（R_N ⊂ R_{N,(T,k)} ⊂ μ），对多样性是比改 N **更细粒度**的控制；narrow 于 1000→500 后样本开始偏离参考。

## 数据
ILVR 不需要成对/标注数据，**底层无条件 DDPM 在单一目标域上训练即可**。论文为演示各任务训了多个无条件模型（附录 C.2）：

- **FFHQ**：70,000 张高清人脸，训练 1.2M steps（用于人脸生成/翻译/scribble 编辑）。
- **MetFaces**：1,000 张高清肖像画；为避免过拟合，从 FFHQ 预训练模型 **fine-tune 20k steps**（用于 face↔portrait 翻译）。
- **AFHQ**：15,000 张动物脸，均分 dog/cat/wild 三类；**只在 dog 训练集上训**，再用 cat/wild 测试集作参考演示"任意动物→狗"的多域翻译。
- **Places365 的 waterfall 类别**：约 5,000 张，训一个模型用于 paint-to-image。
- **LSUN-Church**：126,227 张教堂图，训 1M steps（scribble 编辑）。
- 此外直接复用公开的 **guided-diffusion**（ADM）在 LSUN Bedroom/Horse/Cat 上的无条件 checkpoint，证明 ILVR 可即插即用于任意预训练 DDPM。
- 参考图（人脸/油画/水彩/clip art/scribble）多取自网络，**训练时未见过**——这正是 ILVR 能从"未见域"翻译的关键（参考图只需在学习数据分布的低分辨率空间内匹配，Property 1）。

未涉及 re-captioning、美学/安全过滤、合成数据等（该时期纯无条件像素扩散，无文本对、无 CLIP 标注）。

## 训练方法
- **ILVR 自身 = 零训练**：方法核心是 inference-time 算法，不引入任何可学习参数、不做 SFT/RLHF/DPO/蒸馏。这正是其标题"learning-free / training-free"的含义。
- **底层 DDPM 训练目标**：标准 DDPM 的简化噪声预测损失（ε-prediction，等价于带固定方差的变分下界），与 Ho et al. 2020 一致；固定线性 β schedule，T=1000 扩散步。
- **训练配置**（附录 C.2）：所有模型在 256² 分辨率、**batch size 8** 下训练；步数随数据集规模而定（FFHQ 1.2M、LSUN-Church 1M、MetFaces 仅 fine-tune 20k）。README 提到部分模型用了 **P2-weighting**（作者另一项工作的损失加权）训练。
- **采样加速 trick**：演示中常用 `timestep_respacing`（如 100 步 respacing，或 LSUN 实验用 250 步 uniform stride，遵循 IDDPM），把 1000 步压缩以加速——但这是 DDPM 通用加速，非 ILVR 专属。无 consistency/LCM/ADD 类蒸馏（2021 年尚未出现）。
- **对滤波核鲁棒**：附录 Fig.D 消融了 bicubic / lanczos2 / lanczos3 / bilinear 四种下/上采样核（N=4 与 N=32 两组），结果仅有"牙齿、头发的确切位置"等极微差异 → **方法对核选择鲁棒**。

## Infra（训练 / 推理工程）
- **训练**：未报告 GPU 型号、卡数、GPU·时、并行策略、混合精度等细节。仅知 256² + batch size 8 + 百万级 steps（FFHQ 1.2M / LSUN-Church 1M），属当时单机多卡可承受的规模。
- **推理**：ILVR 每步只比原始 DDPM 多两次 resize（φ_N 的下采样+上采样）和一次加法，**额外开销可忽略**；不增加任何网络前向。瓶颈仍是 DDPM 本身的多步采样（演示用 respacing 到 100/250 步）。
- **依赖**：开源实现基于 OpenAI improved-diffusion + guided-diffusion，resize 用 ResizeRight；可直接加载 guided-diffusion 的公开 checkpoint。无特殊量化/缓存/部署工程。
- **未披露**：吞吐、显存、单图采样耗时等均未在论文中给出。

## 评测 benchmark（把效果讲清楚）
所有数字均来自论文正文 Table 1/2 与附录 Table A/B（FID 用 50k real + 50k generated，pytorch-fid）：

**生成质量 — FID（越低越好，Table 1）**，各下采样因子 N vs 无条件 baseline：

| N | FFHQ FID | METFACES FID |
|---|---|---|
| baseline（无条件） | 11.38 | 37.39 |
| 4 | **4.62** | **11.85** |
| 8 | 7.24 | 16.94 |
| 16 | 10.35 | 22.68 |
| 32 | 12.05 | 32.77 |

→ 结论：ILVR 条件化**不损害**生成质量；低因子（N=4/8）FID 甚至**显著优于**无条件 baseline（因生成图几乎完美对齐参考），高因子接近 baseline。

**多样性 — pairwise LPIPS（越高越多样，Table 2，每张参考生成 10 图、45 对取均值）**：

| N | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|
| LPIPS | 0.011 | 0.039 | 0.101 | 0.185 | 0.299 | 0.439 |

→ N 越大多样性越高，定量印证 Property 2/Eq.12（高因子=更宽子集=更多样、与参考相似度更低）。

**生成质量（无参考度量）— NIQE（越低越好，附录 Table A）**，从 16×/64× 下采图复原：

| N | HR（原图） | Nearest | Bicubic | PULSE | **ILVR** |
|---|---|---|---|---|---|
| 16↓ | 5.25 | 17.56 | 8.09 | 4.34 | **4.06** |
| 64↓ | 5.25 | 14.15 | 12.45 | 4.10 | **4.02** |

→ ILVR 感知质量最高，甚至优于原始 256² HR 参考图；优于 StyleGAN 反演法 PULSE。

**图像翻译 — FID（cat→dog, AFHQ-dog 测试集，附录 Table B）**：

| CycleGAN | MUNIT | CUT（SOTA） | **ILVR** |
|---|---|---|---|
| 85.9 | 104.4 | 76.2 | **79.8** |

→ ILVR 与 SOTA 的 CUT 相当（79.8 vs 76.2），**但 ILVR 只需在 dog 单域上训练的模型**，而其他方法都要在 cat+dog 双域训练。翻译任务统一取 N=32（保留粗结构），paint-to-image 取 N=64（仅保留色调），scribble 编辑取 N=8 且步数 1000→200（既保细节又融合涂鸦）。

**关键消融**：
- 滤波核（附录 Fig.D）：bicubic/lanczos/bilinear 差异极小 → 鲁棒。
- 条件步数范围（Fig.5）：比改 N 更细粒度地控制多样性；窄于 1000→500 后样本偏离参考。
- 即插即用（Fig.9）：直接用 guided-diffusion 公开 LSUN 模型，N=16/64 分别共享细/粗语义 → 证明可用于任意无条件 DDPM 无需重训。

## 创新点与影响
**核心贡献**
1. 提出 **ILVR**：在 DDPM 每步采样后用参考图低频替换提案低频（Eq.8），首次实现**完全无训练、无额外模型、无梯度**的条件 DDPM 采样。
2. 用低通滤波因子 N 与条件步数范围 [b,a] 两个旋钮，给出对"与参考语义相似度/多样性"的可解释、可控调节（Property 1–3 的子集嵌套理论 R_N ⊂ R_M ⊂ μ）。
3. 证明**单个无条件 DDPM** 可零额外学习地胜任多域图像翻译（含未见源域）、paint-to-image、scribble 编辑、超分等多任务，质量与多样性均有竞争力。

**影响**
- 是把"利用预训练无条件生成模型"的范式从 GAN 迁移到扩散模型的**早期奠基性工作之一**，开启了一大批 **training-free 扩散编辑/逆问题** 研究（RePaint、DDRM、零样本复原、各类 guidance 变体常引用并对比 ILVR）。
- "在采样轨迹中替换/投影低频或已知分量"的思想被后续 inpainting、超分、复原方法反复采用与推广。
- 开源 `ilvr_adm`（ICCV 2021 Oral）基于 guided-diffusion，易复现，成为常用 baseline。

**已知局限**
- 条件信息**仅为低频/结构**，无法做文本驱动或精细语义编辑（无 text encoder、无语义控制）；只能"参考图引导"。
- 受限于底层无条件 DDPM 的能力与训练域——参考图必须落在学习数据分布的低分辨率空间内（Property 1）才有效。
- 多步像素空间采样慢；2021 年尚无步数蒸馏，实用性受采样开销限制。
- Eq.7 的"局部条件近似"是近似而非精确条件采样；高因子下与参考的语义对齐较松。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2108.02938
- arxiv_pdf: https://arxiv.org/pdf/2108.02938
- github: https://github.com/jychoi118/ilvr_adm

## 本地落盘文件
- ../../../sources/omni/2021/arxiv-2108.02938.pdf
- ../../../sources/omni/2021/ilvr--readme.md
