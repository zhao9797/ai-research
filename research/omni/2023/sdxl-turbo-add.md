---
title: "SDXL-Turbo / Adversarial Diffusion Distillation (ADD)"
org: "Stability AI"
country: EU
date: "2023-11"
type: paper
category: method
tags: [t2i, distillation, diffusion, gan, few-step, real-time, sdxl, score-distillation]
url: "https://arxiv.org/abs/2311.17042"
arxiv: "https://arxiv.org/abs/2311.17042"
pdf_url: "https://arxiv.org/pdf/2311.17042"
github_url: "https://github.com/Stability-AI/generative-models"
hf_url: "https://huggingface.co/stabilityai/sdxl-turbo"
modelscope_url: ""
project_url: "https://stability.ai/research/adversarial-diffusion-distillation"
downloaded: [arxiv-2311.17042.pdf, sdxl-turbo-add--hf-readme.md, sdxl-turbo-add--blog.md, sdxl-turbo-add--research-page.md, sdxl-turbo-add--github-readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
ADD（Adversarial Diffusion Distillation）把"对抗损失 + 分数蒸馏"合成一个混合目标，将预训练大扩散模型（SDXL）蒸成 **1–4 步实时采样器**——SDXL-Turbo 用 **单步**就在人评中胜过 4 步的 LCM-XL，用 **4 步**胜过 50 步的教师 SDXL-Base；A100 上端到端生成一张 512×512 图仅 **207ms**（其中单次 U-Net 前向 67ms），是第一个用基础模型实现"单步实时文生图"的方法。

## 背景与定位
扩散模型质量强但迭代采样慢（数十步），阻碍实时应用；GAN 单步快但质量与文本对齐落后、难以规模化（容量饱和、训练不稳）。此前的少步化路线各有硬伤：
- 进度蒸馏 / 引导蒸馏（progressive / guidance distillation）能压到 4–8 步但掉点且需迭代式训练；
- 一致性模型 [[consistency-models]] / [[latent-consistency-models-lcm]]（LCM/LCM-LoRA）在 4 步表现强，但 1–2 步时样本模糊、有伪影；
- InstaFlow 用 Rectified Flow 改进蒸馏；纯单步 GAN（StyleGAN-T、GigaGAN）速度快但质量逊于扩散且无 CFG。

ADD 的定位：**保留扩散模型的样本质量与组合性、又拿到 GAN 的单步速度**。做法是把判别器提供的"真实数据流形信号"与扩散教师提供的"结构/组合性知识"结合，并且从预训练扩散权重初始化学生（而非从零训 GAN），从而吃到扩散模型平滑的 scaling law。它建立在 [[ddpm]] / [[latent-diffusion-ldm]] / [[sdxl]] 的基础上，蒸馏对象是公开的 Stable Diffusion 与 SDXL。

## 模型架构
- **学生 / backbone**：标准扩散 U-Net（不是 GAN 的 decoder-only 结构），从**预训练扩散模型权重初始化**。论文训了两档容量：
  - **ADD-M**：860M 参数，消融用 SD2.1 backbone，与基线公平对比时用 SD1.5；
  - **ADD-XL**：3.1B 参数，SDXL backbone（即对外发布的 **SDXL-Turbo**，HF 卡注明 "distilled version of SDXL 1.0"）。
- **三网络结构**（训练期）：① ADD-student（可训权重 θ，从预训 U-Net 初始化）；② 判别器（可训权重 φ）；③ DM-teacher（冻结权重 ψ，即原始扩散模型）。
- **判别器设计**（沿用 StyleGAN-T 的范式）：一个**冻结的预训练特征网络 F**（消融发现 DINOv2 ViT 最佳）+ 一组**轻量可训判别头** D_{φ,k}，作用在 F 不同层的特征 F_k 上。判别器可做**投影式条件注入**：文本条件 c_text 用 **CLIP-ViT-g-14** 文本编码器；图像条件 c_img 用 **DINOv2 ViT-L 的 CLS 嵌入**（对 τ<1000 的带噪输入，学生能从原图 x0 拿到信号，故可在判别器上注入图像信息，鼓励学生有效利用输入）。
- **采样/条件**：训练时从学生时间步集合 T_student={τ1,…,τN}（N=4）均匀采样 s；强制 **zero-terminal-SNR**、令 τn=1000，使推理可从纯噪声起步。**推理不使用 classifier-free guidance（CFG）**，因此显存更省（HF 卡：`guidance_scale=0.0`、不用 negative prompt）。
- **分辨率策略**：所有实验标准化在 **512×512**；更高分辨率的对比模型下采样到该尺寸。发布的 SDXL-Turbo 固定输出 512×512（HF 卡列为已知局限）。保留扩散框架使其天然支持**迭代细化**（多步逐步提升细节/一致性，是相对纯单步 GAN 的优势）。

## 数据
- **判别器/对抗分支**用真实图像 x0：通过前向扩散 x_s = α_s·x0 + σ_s·ε 得到带噪输入喂给学生；x0 直接喂判别器作"真"样本。
- **蒸馏分支不需额外标注**：教师在学生输出的再加噪样本上做去噪预测，作为重建目标。
- **训练数据集来源/规模/配比/清洗过滤/re-caption/美学与安全过滤**：论文与官方博客**均未披露**具体训练数据集构成（仅说"leveraging real data through the discriminator"）。GAN 基线 StyleGAN-T++ 的训练规模有披露（见下），但 ADD 主模型的数据细节未报告。

## 训练方法
- **总目标（Eq.1）**：`L = L_adv^G(x̂θ(x_s,s), φ) + λ·L_distill(x̂θ(x_s,s), ψ)`，全程 **λ=2.5**。
- **对抗损失（hinge loss）**：学生要骗过判别头；判别器最小化 hinge 损失 + **R1 梯度惩罚**（强度 γ=1e-5，且 R1 作用在**每个判别头的输入**而非像素值上——发现输出分辨率 >128² 时 R1 尤其有益）。
- **分数蒸馏损失（Eq.4）**：`L_distill = E_{t,ε'}[ c(t)·d(x̂θ, x̂ψ(sg(x̂θ,t); t)) ]`，距离 d 用 L2。关键细节——教师**不是直接作用在学生输出上**，而是先把学生样本再加噪到 x̂θ,t = α_t·x̂θ + σ_t·ε'，再让教师去噪，避免 OOD。附录 A 证明：取特定权重 c(t) 时该损失**等价于 SDS（Score Distillation Sampling）目标**。权重函数 c(t) 比较了 exponential（c(t)=α_t，高噪声贡献小，FID 更低/更多样）、SDS、NFSD 三种；**最终模型采用 NFSD 权重**（消融默认用 exponential）。
- **核心 trick**：① **学生必须从预训练扩散权重初始化**——随机初始化直接坍塌（FID 293.6 vs 20.6，CLIP 0.065 vs 0.319，Table 1c），这正是相对纯 GAN 的可规模化优势；② 蒸馏损失在**像素空间**计算（即便是 LDM，因为像素空间梯度更稳）；③ 单损失都不行——纯蒸馏损失几乎无效（FID 315.6），必须与对抗损失组合（Table 1d）；④ 教师**单步**即足够（多走几步不一定更好，Table 1f）。
- **训练规模（消融配置）**：4000 iterations，batch size 128（Table 1 脚注）。主模型完整训练时长未单独披露。

## Infra（训练 / 推理工程）
- **训练算力/GPU·时/并行/混合精度**：论文与博客**未披露** ADD 主模型的 GPU 数量、训练时长、并行策略。仅消融给出 4000 iters × bs128 的设定；GAN 基线 StyleGAN-T++ 披露了 ~2M iters × bs2048（对标 GigaGAN schedule），但那是基线不是 ADD 学生本身。
- **推理加速形态**：核心就是把采样步数从 50 压到 1–4 步、且推理**不开 CFG**（少一半前向、省显存）。
- **推理速度（官方博客，A100，fp16）**：端到端生成一张 512×512 图 **207ms** = prompt 编码 + 单次去噪步 + VAE 解码；其中**单次 U-Net 前向仅 67ms**。论文 Fig.7 用 A100 mixed precision 报告各模型生成单张 512×512 的速度（与 ELO 联合可视化）。
- **部署**：HF 以非商用研究许可（sai-nc-community）发布权重+代码；官方 `generative-models` 仓库提供 `scripts/demo/turbo.py`（streamlit demo）；Clipdrop 上线实时 demo。Diffusers 集成（`AutoPipelineForText2Image` / `Image2Image`，1 步即可）。
- **量化/缓存/TensorRT**：官方文档**未提及**专门的量化或缓存方案。

## 评测 benchmark（把效果讲清楚）
**指标口径**：自动指标用 **COCO2017 zero-shot FID5k（FID，↓）+ CLIP score（CS，↑，用在 LAION-2B 上训练的 ViT-g-14）**，单学生步评估；主对比改用**人评**（更可靠），在 **100 条 PartiPrompts**（排除 basic 类）上做 1v1，每对平均 4 票，分"图像质量"与"prompt 跟随"两题，用 **ELO**（K=1、Rinit=1000、1000 次 bootstrap）排名。

**消融关键数字（Table 1，单步，COCO FID5k / CLIP）**：
- 判别器特征网（1a）：DINOv2 ViT-S 最佳（FID 20.6 / CS 0.319），优于 DINOv1 ViT-S（21.5/0.312）、DINOv2 ViT-L（24.0/0.302）、CLIP ViT-L（23.3/0.308）。
- 判别器条件（1b）：text+image 双条件最好（FID 20.6 / CS 0.319），优于无条件（21.2/0.302）、仅 text（21.2/0.307）、仅 image（21.1/0.316）——图像条件单独已优于文本条件。
- 学生初始化（1c）：预训练 20.6/0.319 vs 随机 293.6/0.065（坍塌）。
- 损失项（1d）：仅 L_adv 20.8/0.315；仅 L_distill 315.6/0.076（失效）；L_adv+λL_distill,exp 20.6/0.319；+sds 22.3/0.325；+nfsd 21.8/0.327（exp 偏 FID/多样性，sds/nfsd 偏质量与文本对齐）。
- 教师类型（1e）：学生会"继承"教师特性——SDXL 教师 FID 偏高但 CLIP 更高（student SDXL/teacher SDXL：28.41/0.325）。
- 教师步数（1f）：1 步即足够（FID 20.6），2/4 步无明显增益。

**蒸馏方法横评（Table 2，均基于 SD1.5，COCO FID5k/CLIP，含 A100 时间）**：
- DPM-Solver 25 步：0.88s，FID 20.1 / CLIP 0.318；8 步：0.34s，31.7/0.320。
- Progressive Distillation 1/2/4 步：FID 37.2 / 26.0 / 26.4。
- CFG-Aware Distillation 8 步：24.2/0.300。
- InstaFlow-0.9B/1.7B（1 步）：23.4/0.304、22.4/0.309。
- UFOGen（1 步）：22.5/0.311。
- **ADD-M（1 步）：0.09s，FID 19.7 / CLIP 0.326** —— 同基座下击败所有其他方法，甚至优于 DPM-Solver 8 步。

**人评 / ELO（Fig.5–7）核心结论**：
- **ADD-XL 单步**在质量与 prompt 跟随上胜过当时所有少步基线（LCM-XL 1/2/4 步、InstaFlow、StyleGAN-T++、16 步 OpenMUSE）；单步即胜过 **4 步的 LCM-XL**。
- **ADD-XL 4 步**在多数对比中胜过其**教师 SDXL（50 步，base 无 refiner）**，成为单步与多步两个设定下的 SOTA。Fig.7 速度-质量曲线：ADD-XL 在最快档位仍占 ELO 高位。
- 代价：ADD-XL 增强真实感（毛发/织物/皮肤纹理更好、减少过平滑）但**样本多样性略降**。

**GAN 基线（附录 C）**：自训的 StyleGAN-T++（改进判别器 + 每头 R1，~2M iters×bs2048）在 zero-shot FID 与 CLIP 上超过此前最佳 GAN（StyleGAN-T、GigaGAN）。

**已知局限（HF 卡）**：固定 512×512、非完美写实、无法渲染清晰文字、人脸/人物可能生成不佳、VAE 自编码有损。

## 创新点与影响
- **核心贡献**：首次把**对抗损失 + 分数蒸馏**统一进一个混合目标，且**从预训练扩散权重初始化学生**——既拿到 GAN 单步速度，又保留扩散的质量/组合性与"可迭代细化"能力，且推理免 CFG。这是**第一个用基础模型解锁单步实时文生图**的方法。
- **方法洞见**（被后续广泛沿用）：判别器用冻结 DINOv2 特征 + 轻量头、text+image 双条件投影；蒸馏在像素空间算更稳；蒸馏损失与 SDS 的等价性给出统一视角。
- **影响**：开启"少步/单步实时 t2i"范式与 *-Turbo 命名；直接催生并被对比于后续少步蒸馏工作（如 SD3-Turbo 的 [[latent-adversarial-diffusion-distillation-ladd]]（LADD，把对抗蒸馏搬到潜空间）、SDXL-Lightning、[[hyper-sd]] 等），也与一致性蒸馏路线 [[latent-consistency-models-lcm]] 形成两大技术分支。实时交互式生成（边打字边出图）由此走向产品化（Clipdrop demo）。
- **已知局限/未公开**：训练数据集构成、主模型训练算力与时长均未披露；固定低分辨率、文字渲染弱、多样性下降；权重为非商用研究许可。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2311.17042
- arxiv_pdf: https://arxiv.org/pdf/2311.17042
- official_report_page: https://stability.ai/research/adversarial-diffusion-distillation （PDF: https://stability.ai/s/adversarial_diffusion_distillation.pdf）
- blog: https://stability.ai/news/stability-ai-sdxl-turbo
- hf_model_card: https://huggingface.co/stabilityai/sdxl-turbo
- github: https://github.com/Stability-AI/generative-models
- demo: http://clipdrop.co/stable-diffusion-turbo

## 一手源存档（sources/）
- [arxiv-2311.17042.pdf](https://arxiv.org/pdf/2311.17042)  （arXiv 原文 PDF，不入 git）
- [hf-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/sdxl-turbo-add--hf-readme.md)
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/sdxl-turbo-add--blog.md)
- [research-page.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/sdxl-turbo-add--research-page.md)
- [github-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/sdxl-turbo-add--github-readme.md)
