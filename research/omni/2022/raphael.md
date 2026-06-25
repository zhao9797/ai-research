---
title: "RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"
org: "SenseTime Research / HKU"
country: China
date: "2023-05"
type: paper
category: t2i
tags: [t2i, diffusion, mixture-of-experts, space-moe, time-moe, latent-diffusion, edge-supervised, coco-fid]
url: "https://arxiv.org/abs/2305.18295"
arxiv: "https://arxiv.org/abs/2305.18295"
pdf_url: "https://arxiv.org/pdf/2305.18295"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://raphael-painter.github.io/"
downloaded: [raphael--paper-ar5iv.md, raphael--project-page.md, raphael--paper.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
RAPHAEL 是 SenseTime/港大提出的文生图扩散模型，核心创新是在 U-Net 的每个 transformer block 里同时叠 **space-MoE（按文本 token→图像区域路由）** 和 **time-MoE（按扩散时间步路由）**，把 16 层 ×6 个空间专家组合出 6^16（数十亿）条"扩散路径（diffusion paths）"，每条路径像一个"画师（painter）"负责把某个文本概念画到某个图像区域的某个时间步上，从而把文本概念精确绑定到图像区域；3B 参数单模型在 1000 张 A100 上训两个月，刷新 MS-COCO **zero-shot FID-30k = 6.61**（彼时 SOTA，超过 DeepFloyd 6.66 / ERNIE-ViLG 2.0 6.75 / eDiff-I 6.95 / Imagen 7.27 / DALL-E 2 10.39）。

> 注：归 2022（首版年份）按 worklist 约定记账；arXiv 公开版 abs 标注 2023-05（2305.18295），date 字段记 2023-05。

## 背景与定位
2022 末–2023 初的文生图竞赛里，纯扩散模型（[[imagen]] 像素空间、[[latent-diffusion-ldm]]/Stable Diffusion 潜空间、[[dall-e-2]] 两段式）已经把 COCO FID 推到 7–10 区间，但论文指出一个共性痛点：当 prompt 同时含**多个名词、形容词、动词**时，现有模型常**丢概念 / 概念错位**（文本与图像区域绑定不准）。RAPHAEL 把这个"概念—区域"对齐问题显式地交给 MoE 路由来解：
- **space-MoE** 解决"哪个概念画在哪个区域"——把每个文本 token 连同它对应的图像区域（二值 mask）送进不同的空间专家。
- **time-MoE** 解决"同一概念在不同噪声水平下该怎么画"——思想承袭 [[ediff-i]] 与 [[ernie-vilg-2]] 的"按时间步分专家"，但**改用可学习的门控自动分配时间步**，而非 eDiff-I/ERNIE-ViLG 2.0 的手工划分。
- 额外提出 **edge-supervised learning（边缘监督）** 进一步提升画质与美学。

在技术脉络上：架构落在 LDM 潜空间扩散范式之上（沿用 [[latent-diffusion-ldm]] 的 VAE 压缩 + Stable Diffusion 的美学过滤/清洗），方法学上是把语言模型里的稀疏 MoE（Shazeer 2017、Switch Transformer）和"按时间步分专家"（eDiff-I/ERNIE-ViLG 2.0）这两条线**统一到一个 block 里并组合成海量路径**，这是它区别于前作的核心定位。

## 模型架构
- **Backbone**：U-Net 形式的扩散去噪网络，主体由 **16 个 transformer block** 组成。每个 block 含四件套：① self-attention ② cross-attention（注入文本）③ **space-MoE** ④ **time-MoE**；每个 block 还带 **edge-supervised cross-attention** 监督。block 内顺序为 cross-attention → time-MoE → space-MoE（time-MoE 输出 h′ 喂给 space-MoE）。
- **潜空间（latent diffusion）**：用 VAE（VQ/VAE，引 van den Oord 2017）把图像从像素空间压到潜空间，扩散在潜空间进行，再用 decoder 解回——沿用 LDM 范式以降训练/采样开销。
- **Text encoder**：**OpenCLIP-g/14**，文本 token 数 n_y=77，token 维度 d_y=1024；文本通过 cross-attention 的 key/value 投影注入图像 token。
- **Space-MoE（空间专家，核心）**：
  - 每个文本 token y_i 经门控 route(y_i) 选 1 个空间专家 e；该专家只作用在该 token 对应的图像区域（二值 mask M̂_i）上：层输出 = (1/n_y) Σ_i e_{route(y_i)}( h′(x_t) ∘ M̂_i )，∘ 为 Hadamard 积。
  - **区域 mask 怎么来**：用 cross-attention 的注意力图 M（M_{j,i} 为第 j 个图像 token 与第 i 个文本 token 的相关度）做阈值，阈值 η_i = α·max(M_{*,i})，α 为可调超参（消融定 α=0.2）；相关度高于阈值的图像 token 即划入该文本 token 的区域。
  - **专家规模/路径数**：16 层 space-MoE，每层 **6 个空间专家** → 6^16 ≈ 数十亿条空间扩散路径。作者用一个小实验证明路径与概念强绑定：把 100 个形容词各生成 100 张图、收集其 16 维路径向量当特征训 XGBoost，5 折交叉验证对开放世界形容词分类准确率 >93%；附录里对 COCO 80 类名词、50 个动词同法分类，准确率分别 **94.3%**、**97.5%**（Appendix 7.5），印证"不同类别激活不同路径"的异质现象。
- **Time-MoE（时间专家）**：在每个 block 的 space-MoE 之前。时间门控 t\_router(t_i) = argmax(softmax(G′(E′_θ(t_i)) + ε)) 按时间步 embedding 把特征路由给某个时间专家；加随机噪声 ε 防 mode collapse。论文统计发现专家会**按噪声水平自发分工**：如第一个 block 里第 1 个专家专管高噪声段（DDIM 前 59% 步），其余专家管低噪声段（后 41% 步）。
- **Edge-supervised learning（边缘监督）**：用一个 N=5 层卷积的模块 P_θ(M) 从 cross-attention 注意力图预测**边缘图**，以 GT 边缘（边缘检测算法得到）作监督，用 **Focal Loss**（α=0.5, γ=2）训练；只在扩散时间步较小（t < T_c=500，即噪声较低）时启用，避免在高噪声步学边缘。目的是逼模型在注意力图里保留清晰的物体边界，从而提升细节与美学。
- **参数量与分辨率**：单模型 **~3B 参数**；训练用 **多尺度 bucketing**（见数据），生成原生分辨率落在各 bucket（如 640×640、512×768 等）；配合定制 **SR-GAN（Real-ESRGAN 系）** 可把输出超分到 **4096×6144**。
- **可扩展性**：支持 LoRA、ControlNet（canny）、SR-GAN 扩展；论文称其 LoRA 比 Stable Diffusion 更抗过拟合。

## 数据
- **来源**：**LAION-5B** + 部分**内部数据集**（internal datasets，规模/构成未披露）。
- **清洗 / 过滤**：
  - **美学过滤**：用与 Stable Diffusion 相同的 aesthetic scorer，剔除美学分 **< 4.7** 的图文对。
  - **去水印**：移除带水印的图。
  - **文本清洗**：LAION-5B 文本噪声大，去掉 URL、HTML 标签、email 等无用信息（借鉴 LDM / eDiff-I / UniDiffuser 的做法）。
- **多尺度 bucketing**：不像 LDM 那样裁到固定尺寸，而是把图 resize 到最近的 bucket 尺寸，共 **9 个尺度**：[448,832]、[512,768]、[512,704]、[640,640]、[576,640]、[640,576]、[704,512]、[768,512]、[832,448]（[h,w]）。GPU 资源按各 bucket 图像数自动分配以提升利用率。
- **图文对数量 / 配比 / 合成数据 / re-captioning**：均**未披露**（论文未给最终训练集规模，也未提及合成/重写 caption）。

## 训练方法
- **训练目标**：标准 DDPM 风格的潜空间扩散去噪（T=1000 时间步，反向 t=T→1 逐步去噪）；非 flow matching、非自回归、非 masked-token。
- **优化器与超参（Appendix Table 2）**：
  - 优化器 **AdamW**，betas (0.9, 0.999)，**weight decay = 0.0**，**learning rate = 1e-4**，**warmup 20000 步**。
  - **batch size = 2000**；**1000 张 A100**，训练 **2 个月**。
  - T=1000，n_y=77，d_y=1024，**T_c=500**（边缘监督截止时间步），**α=0.2**（space-MoE 阈值系数）。
  - **space 专家数 = 6**，**time 专家数 = 4**，**transformer block 数 = 16**。
  - 专家与门控网络结构 = FFN，激活 = GELU；开启梯度 checkpoint；开启多尺度训练。
  - Focal Loss：α=0.5, γ=2（边缘监督）。
- **多阶段 / 偏好对齐 / 蒸馏**：论文**未报告** SFT/RLHF/DPO/reward model 等偏好对齐阶段，也**未报告** consistency/LCM/ADD 等步数蒸馏；公开 demo 版仅提到"在更多高美学数据上 fine-tune"。
- **采样**：用 **DDIM** 采样器；评测时扫 classifier-free guidance 权重 {1.5, 3.0, 4.5, 6.0, 7.5, 9.0} 画 FID-CLIP 权衡曲线。

## Infra（训练 / 推理工程）
- **算力**：**1000× NVIDIA A100，训练 2 个月**（约 ~1000 GPU × ~60 天，量级 ~10^6 A100·hour，论文未给精确 GPU·时）。
- **框架 / 并行**：PyTorch 实现；开启 gradient checkpoint 省显存；**多尺度 bucketing 下按 bucket 图像数自动分配 GPU 资源**。具体并行/分布式策略（DP/TP/PP、ZeRO 等）、混合精度、吞吐量**未披露**。
- **推理 / 加速**：以 DDIM 多步采样为主；**未报告**量化、缓存、步数蒸馏等加速手段。论文给了 space 专家数与推理速度/FID-5k 的权衡：用满全部空间专家时，专家数为 6 时**推理速度下降约 24%** 但换来更高保真度，且**仍快于 Imagen、eDiff-I** 等前作扩散模型（space-MoE 的计算复杂度在专家用满后不再随 token 数增长）。
- **部署形态**：发布过公开 demo（在更多高美学数据上微调过的最新版）；未开源权重/代码。

## 评测 benchmark（把效果讲清楚）
**① MS-COCO 256×256 zero-shot FID-30k（Table 1，越低越好）**：

| 模型 | 类型 | zero-shot FID-30k |
| --- | --- | --- |
| LDM | Diffusion | 12.63 |
| GLIDE | Diffusion | 12.24 |
| DALL-E 2 | Diffusion | 10.39 |
| Stable Diffusion | Diffusion | 8.32 |
| Muse-3B | Non-AR | 7.88 |
| Imagen | Diffusion | 7.27 |
| eDiff-I | Diffusion Experts | 6.95 |
| ERNIE-ViLG 2.0 | Diffusion Experts | 6.75 |
| DeepFloyd（商业产品，2023-05） | Diffusion | 6.66 |
| **RAPHAEL** | **Diffusion Experts** | **6.61（SOTA）** |

（同表另列 GAN/AR 基线：DF-GAN 21.42、DM-GAN+CL 20.79、LAFITE 8.12、Make-A-Scene 7.55，为非 zero-shot FID-30k。）

**② 人评 ViLG-300（中英双语 300 prompt，盲评）**：用 ViLG-300 与 DALL-E 2、Stable Diffusion XL、ERNIE-ViLG 2.0、DeepFloyd 做 user study，从 **image-text alignment** 和 **image quality & aesthetics** 两维让专业画师盲评偏好率（报告 95% 置信区间）。结论：RAPHAEL 在两维上**均优于所有对手**。（论文以图 5 给出条形偏好率，未在正文给逐对手数值，本页不臆造具体百分比——具体数字见原文 Fig.5。）

**③ 消融（CLIP–FID 权衡曲线，Fig.6）**：
- 完整 RAPHAEL vs 去掉 space-MoE / time-MoE / edge-supervised 三个变体逐一对比，**三个模块均有效**。
- **space-MoE** 显著抬高 CLIP score，并把最优 guidance 权重从 3.0 推到 4.5；同 guidance 下 space-MoE 明显降低 FID（画质大涨）。
- **α 与 T_c 选择**（Fig.6a）：α=0.2 最佳，T_c=500 最佳。
- **专家数 vs 速度/FID**（Fig.6c）：复杂度主要由空间专家数决定；专家用满后复杂度不再增长；专家=6 时速度 -24% 换更高保真。
- **edge-supervised**（Fig.7 第四张）：在 ViLG-300 上做带/不带边缘监督的人评，边缘监督**显著提升美学偏好率**（具体数值见原文图，本页不编造）。

> 未报告：GenEval、T2I-CompBench、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore、Arena ELO 等（这些 benchmark 在 2023-05 尚未成为主流，论文未涉及）。

## 创新点与影响
**核心贡献**
1. **space-MoE × time-MoE 组合出海量"扩散路径"**：首次把"文本 token→图像区域"的空间路由与"时间步→噪声段"的时间路由**统一进同一个 transformer block**，6^16 数十亿条路径让每条路径专责一个"概念×区域×时间步"，显著改善多概念 prompt 的概念绑定与不丢概念。
2. **可学习的时间门控**：相比 eDiff-I / ERNIE-ViLG 2.0 手工划分时间步专家，RAPHAEL 用门控网络**自动**学习时间步→专家分配，并观察到专家按噪声水平自发分工。
3. **edge-supervised learning**：用注意力图预测边缘并以 Focal Loss 监督（仅低噪声步启用），是一个轻量但有效的美学/细节增强 trick。
4. **结果**：刷新 COCO zero-shot FID-30k 到 6.61，ViLG-300 人评全面领先，验证了"为扩散模型显式做概念—区域对齐 + 稀疏专家放大容量"这条路。

**影响**：把稀疏 MoE 用于扩散 U-Net 的"按区域/按时间分专家"思路（接续 eDiff-I/ERNIE-ViLG 2.0），是 MMDiT/大规模文生图走向"专家化、概念对齐显式化"的早期代表之一；空间注意力 mask 路由的思想也与后续 regional control / 概念绑定类工作相通。

**已知局限**
- **闭源**：权重与代码未开源，复现门槛极高（1000×A100×2 月）。
- **工程细节披露不全**：并行策略、混合精度、精确 GPU·时、内部数据构成、最终训练集规模均未公开。
- **专家路由开销**：空间专家增多带来推理变慢（专家=6 时 -24%），是容量—速度的固有权衡。
- 评测局限于 COCO FID + ViLG-300 人评，未覆盖后来更细的组合性/对齐 benchmark。

## 相关页面（内链）
- 前作 / 基线：[[imagen]]、[[latent-diffusion-ldm]]、[[dall-e-2]]、[[ediff-i]]、[[ernie-vilg-2]]
- 关联方法：[[stable-diffusion-1]]（美学过滤/数据清洗沿用其做法）

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2305.18295
- arxiv_pdf: https://arxiv.org/pdf/2305.18295
- project_page: https://raphael-painter.github.io/

## 本地落盘文件
- ../../../sources/omni/2022/raphael--paper.pdf  （arXiv 官方 PDF，2305.18295，~20MB；与 ar5iv 文本逐项核对一致，6.61 / 3B / 1000×A100×2月 / 美学分<4.7 等均已对核；按本仓约定 PDF 不入 git，备份走 HF bucket）
- ../../../sources/omni/2022/raphael--paper-ar5iv.md  （ar5iv 渲染的论文全文 HTML→markdown，含方法/实验/附录/超参表 Table 2/FID 表 Table 1，精读主源）
- ../../../sources/omni/2022/raphael--project-page.md  （官方项目页 cloakbrowser 快照，含 COCO FID 图、ViLG-300 人评图、LoRA 对比图）
