---
title: "ERNIE-ViLG 2.0: Improving Text-to-Image Diffusion Model with Knowledge-Enhanced Mixture-of-Denoising-Experts"
org: "Baidu"
country: China
date: "2022-10"
type: paper
category: t2i
tags: [text-to-image, diffusion, latent-diffusion, mixture-of-experts, knowledge-enhanced, chinese, baidu, cvpr2023]
url: "https://arxiv.org/abs/2210.15257"
arxiv: "https://arxiv.org/abs/2210.15257"
pdf_url: "https://arxiv.org/pdf/2210.15257"
github_url: "https://github.com/PaddlePaddle/ERNIE/tree/ernie-kit-open-v1.0/Research/ERNIE-ViLG2"
hf_url: ""
modelscope_url: ""
project_url: "https://wenxin.baidu.com/ernie-vilg"
downloaded: [arxiv-2210.15257.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
百度提出的 24B 参数中文潜空间文生图扩散模型，两大创新——**知识增强**（用 POS 词性分析 + 目标检测把文本关键词与图像显著区域的对齐权重在训练期"加码"）与 **MoDE 去噪专家混合**（把 1000 步去噪切成 10 段、每段用独立 U-Net 专家，从而把参数扩到 24B 而推理时延几乎不变）。在 MS-COCO 256×256 上拿下当时 SOTA 的 **zero-shot FID-30k = 6.75**，并在中英双语 prompt 集 ViLG-300 的人评中对 [[dall-e-2]] 与 Stable Diffusion（[[latent-diffusion-ldm]]）均显著胜出。收录于 CVPR 2023（"highlight" 等级未在落盘 arXiv v2 中体现，存疑），是百度"文心一格"产品的底层模型。

## 背景与定位
2022 年文生图扩散方法（[[glide]]、DALL-E 2、Imagen、[[latent-diffusion-ldm]]）已能生成高保真高分辨率图，但论文指出两个未解问题：

1. **去噪步内：所有元素一视同仁。** 标准扩散 loss 让全部图像区域等权贡献、全部文本 token 等权交互。但一个视觉场景里不同元素（关键名词、显著物体）对语义表达的重要性不同；这种"无差别学习"易丢失关键元素，导致**文图错位 / 属性混淆**（attribute confusion，多物体多属性 prompt 尤甚，DALL-E 2 已知此问题）。
2. **去噪步间：不同阶段任务不同却共用一套参数。** 早期步（t 接近 T，输入近纯噪声）要从噪声里勾勒语义骨架与布局，相当于"生成"任务；后期步（t 接近 1，输入接近成品图）只需细化纹理细节。但既有方法都用**同一个 U-Net 跑全部步**，同一套参数被迫学习互异的能力，论文判断这是次优的。

ERNIE-ViLG 2.0 分别对症：知识增强解决问题 1，MoDE 解决问题 2。它是百度第一代 [[ernie-vilg]]（2021，VQGAN + 自回归 transformer 的统一双向生成）的扩散版换代，技术路线从自回归彻底转向 [[latent-diffusion-ldm]] 式潜空间扩散，并继承 ERNIE 系"知识增强预训练"的家族哲学（ERNIE-ViL 的 scene graph、ERNIE-Layout 的版面知识）。论文自称是**首个基于扩散的中文大规模文生图模型**。

## 模型架构
潜空间扩散（latent diffusion），整体沿用 [[latent-diffusion-ldm]] 框架，再叠加两项自有设计。

- **图像自编码器（VAE）**：先独立预训练一个图像 encoder，把像素图 `x ∈ R^(H×W×3)` 压到隐空间 `x̂ ∈ R^(H_l×W_l×4)`（4 通道隐表示），及对应 decoder 还原。训练扩散模型时 **autoencoder 冻结**，扩散只在隐空间生成 `x̂`，推理末端再用 decoder 解码成像素图。autoencoder 与扩散模型用同一份数据训练。
- **文本编码器**：Transformer，**1.3B 参数**；vocab 21128（中文 BERT 系词表），context 长度 77，width 2048，depth 24 层，32 个注意力头。**所有去噪专家共享同一个文本编码器**。
- **去噪网络（U-Net）**：标准条件 U-Net；model channels 512，head channels 64，channel multiplier [1,2,3,4]，attention resolutions [2,4,8]，每级 3 个 ResNet block，dropout 0。文本通过 **cross-modal attention**（U-Net 表示与文本表示拼接后过注意力层）注入，对应公式 (6)(7)。
- **MoDE（Mixture-of-Denoising-Experts）**：把 1000 个去噪 timestep **均匀切成 10 块**，每块连续 timestep 指派给一个 U-Net 专家（每个专家 **2.2B 参数**）。路由不是学习得来的 router，而是**用去噪步索引 t 作为固定路由**（`⌊t/100⌋` 选第几个专家）。推理时每步只激活一个专家，故增加专家数**不增加单步推理算力**——这是扩参数而不增时延的关键。
- **总参数 ≈ 24B**：1.3B 文本编码器 + 10×2.2B U-Net 专家 ≈ 24B。论文称这是当时**最大的文生图模型**。
- **分辨率**：可直接输出 **1024×1024**（对比 Stable Diffusion 当时 512×512；DALL-E 2 则靠 64×64 + 两级超分级联到 1024）。
- 推理用 **classifier-free guidance** + **DDIM** 采样，采样步数 50（noise schedule 线性，扩散步数 1000）。MS-COCO 最优 CFG scale = 2.1。

## 数据
- **规模**：1.7 亿（**170M**）图文对。
- **来源/配比**：包含公开**英文**数据集 LAION（[28] 即 LAION-400M 系）+ 一系列**内部中文**数据集。具体中英配比未披露。
- **语言处理**：对英文 caption 的样本，用**百度翻译 API** 译成中文，使全流程以中文 prompt 为输入。
- **knowledge 标注（仅训练期）**：
  - 文本侧——用开源 POS 工具 **jieba** 做词性分析，识别"实词关键词"（现代汉语的名词、动词、形容词、数词、量词、代词）。
  - 视觉侧——用目标检测器（Bottom-Up Attention，ref [1]）跑 **50% 训练样本**，启发式策略挑显著物体。
  - **re-captioning**：检测出的物体若没出现在原 caption 里（如图 2 的 "bowl"）就**追加到原描述**；另用图像描述模型 **OFA**（ref [38]）为图像生成 caption，**随机替换**部分原 prompt——因为合成 caption 往往比原 prompt 更简洁、语义更准。
- **美学/安全过滤**：未专门披露过滤管线；论文在"风险"一节承认数据为网络爬取的图 + alt-text，可能含社会文化偏见。

## 训练方法
标准 DDPM 噪声预测目标（预测 ε，ℓ2 loss），在此之上做两处**带权改造**和**两阶段训练**。

**训练目标改造（知识增强，均只作用于训练期）：**
- **文本知识 — 注入特殊 token + 加权注意力**：对选中的 **50%** 样本，在每个词前插入与其 POS 标签对应的特殊 token（如形容词 `[a]`、名词 `[n]`）；并在 cross-attention 里给"图像 token ↔ 关键词 token"对的注意力分数乘以缩放因子 `(1+w_a)`（公式 8-9），`w_a = 0.01`。
- **视觉知识 — 区域加权 loss**：对关键物体所在图像区域，在去噪 loss 上乘 `(1+w_l)`（公式 10-11），让模型更关注这些区域的生成，`w_l = 0.1`。（两个超参均从 {0.01, 0.1, 0.5, 1} 选出。）
- 这些增强**只在训练用**：推理时无需特殊 token、加权注意力或文本改写，模型已"内化"知识感知能力。消融显示文本知识主要提升细粒度语义控制、视觉知识主要提升保真度（且需配合合成描述才稳定），二者**互补**，合用同时拉高 fidelity 与 alignment 并**加速收敛**（带知识的模型在 100M 样本时≈baseline 200M 样本的效果）。

**两阶段训练（Algorithm 1）：**
- **第一阶段（step 0 → 350,000）**：训练 1 个 2.2B U-Net + 1.3B 文本编码器，timestep 从 [0,1000) 随机采样，同时优化文本编码器与去噪网络。
- **第二阶段（step 350,000 → 440,000，即 +90,000 步）**：用第一阶段参数初始化复制出 **10 个去噪专家**（Algorithm 1 line 5）；文本编码器**共享**，每步采样 t 后只优化第 `⌊t/100⌋` 个专家网络（90,000 步均摊到 10 专家，每专家约 9,000 步）。注：论文消融里另有"每专家 200M 样本"的设定，但那是**轻量消融模型**（500M 文本编码器 + 870M U-Net）的实验，与 24B 主模型的步数设定不是同一回事。
- **优化器**：AdamW，固定学习率 `0.9×10⁻⁴`，β1=0.9，β2=0.999，weight decay 0.01。
- **重排序（reranking，推理增强）**：受 DALL-E / Parti 启发，每个 prompt 仅采样 **4 张**图，用预训练 CLIP（ref [21]）算图文对齐分重排选最佳（对比 DALL-E 用 512 张、Parti 用 16 张——ERNIE-ViLG 2.0 用**更少候选**就更好）。
- **蒸馏/步数加速**：未采用 consistency/LCM/ADD 等蒸馏，仍是 50 步 DDIM。

## Infra（训练 / 推理工程）
- **算力**：**320 张 Tesla A100**，训练 **18 天**。
- **并行/分布式策略、混合精度、吞吐**：论文**未披露**具体并行方案与精度配置。
- **推理效率**：MoDE 的核心工程价值即"扩参数不增时延"——24B 总参数但每去噪步只激活 1 个 2.2B 专家 + 共享文本编码器，单步算力≈单专家模型；采样 50 步 DDIM。
- **部署形态**：作为百度"文心一格"（wenxin.baidu.com/ernie-vilg）线上产品的底层模型；代码/数据（ViLG-300）开放在 PaddlePaddle/ERNIE 仓库。模型权重未开源。

## 评测 benchmark（把效果讲清楚）

**MS-COCO 256×256 zero-shot FID-30k（CFG=2.1，越低越好，Table 3 —— 列出 #params + 是否 reranking）：**

| 模型 | #params | FID（w/o reranking） | FID（w/ reranking / #图） |
|---|---|---|---|
| DALL-E | 12B | 34.6 | 27.5 / 512 |
| LDM | 1.45B | 12.61 | — |
| GLIDE | 6B | 12.24 | — |
| Make-A-Scene | 4B | 11.84 | — |
| DALL-E 2 | 4.5B | 10.39 | — |
| Imagen | 6.6B | 7.27 | — |
| Parti | 20B | — | 7.23 / 16 |
| **ERNIE-ViLG 2.0（1 专家, 3.5B）** | 3.5B | **8.07** | 7.62 / 4 |
| **ERNIE-ViLG 2.0（10 专家, 24B）** | 24B | **7.23** | **6.75 / 4** |

（另：Table 1 是单列 zero-shot FID-30k 横评，除上表外还列了 CogView 27.10、LAFITE 26.94、ERNIE-ViLG v1 14.70、CogView2 24.00——论文未在 Table 1 标注这些值是否用 reranking，故不并入上表的 reranking 列。）

- 即便**不 reranking**，24B 版 FID 7.23 已打平/超过 DALL-E 2、Imagen；加 4 张 reranking 到 **6.75**，超过 Parti（7.23 用 16 张 reranking 且参数相近 20B）→ **新 SOTA**。
- 第一阶段结束的 3.5B 单专家模型 FID 8.07，已优于同量级的 DALL-E 2（10.39），佐证知识增强本身的增益；从 3.5B/1 专家（8.07）到 24B/10 专家（7.23）佐证 MoDE 扩参的增益。

**ViLG-300 人评（300 条中英双语 prompt，16 类；由 DrawBench 英文 + ERNIE-ViLG 中文集构造；5 名评审，盲评，含"无差别"选项；Fig 3，报 95% 置信区间）：**
- vs **DALL-E 2**：图文对齐偏好 ERNIE-ViLG 2.0 **56.5%±3.8%**，保真度 **58.8%±3.6%**。
- vs **Stable Diffusion**：图文对齐 **68.2%±3.8%**，保真度 **66.5%±3.5%**。
- 两个维度对两个对手**全面胜出**；分类细看在 Color、复杂场景（Complex）、Geography、Scene、Cartoon 类尤强。

**消融结论（Fig 5 / 表 5 / 附录 D，FID-10k + CLIP Score pareto 曲线）：**
- **知识增强**：textual / visual / all 逐项叠加，pareto 前沿持续右移（CLIP↑、FID↓）；仅 object 加权不稳，需配合合成 caption 才能稳定发挥视觉知识。各策略在不同类别上互补——文本知识对 Counterfactual/Color 增益最大，全量对 Complex/Counterfactual/Cartoon 增益最大（ΔCLIP 见表 5）。
- **MoDE 专家数**：1→2→5→10 专家，性能单调提升；且"**更多专家**"优于"**单专家看更多样本**"（如 2 专家×200M 优于 1 专家×400M 后期），证明解耦不同去噪阶段确有收益，而非单纯多见数据。
- **cross-attention 可视化（Fig 7）**：t≈1000 时注意力近均匀铺满全图（从噪声搭骨架），t≈1 时注意力集中到前景物体（填细节）——实证不同去噪步任务确实不同，支撑 MoDE 动机。

## 创新点与影响
**核心贡献：**
1. **知识增强扩散**——首次把"文本词性关键词 + 图像目标检测显著区域"作为可加权监督信号注入文生图扩散训练（加权注意力 + 区域加权 loss + 物体回填/OFA 重描述），缓解多物体多属性的属性混淆问题，且推理零额外开销。
2. **MoDE 去噪专家混合**——以"去噪步索引"为固定路由的 U-Net 专家混合，把模型扩到 24B（当时最大文生图模型）而推理时延几乎不变；提供了 diffusion 领域"按去噪阶段分工"的一种简单有效扩参范式。
3. **ViLG-300 双语评测集**——首个支持中英文生图模型公平横评的 300 条平行 prompt 集（DrawBench + ERNIE-ViLG，16 类），开源。
4. MS-COCO zero-shot FID **6.75** 新 SOTA；中文文生图工程落地（文心一格底座）。

**影响：** 百度文心一格商业产品底层；为后续把 MoE/专家分工思想引入扩散（按 timestep 而非按 token 分专家）提供早期范式；ViLG-300 成为中文文生图评测的一个参照。收录于 CVPR 2023。

**已知局限（论文第 5 节）：**
- **文字渲染弱**：中英混训导致难同时学好两种文字；仅能渲染常见简单字（"福"、数字"20"），复杂汉字只学会"在哪写"却画成无意义笔画。
- **数据偏见**：网络爬取图 + alt-text，可能含社会文化偏见，存在被滥用风险。
- **专家数受算力限制**仅到 10；作者认为更多专家、乃至"多文本编码器作专家"是值得探索的方向。
- 评测主要靠 FID + CLIP + 人评，CLIP 对多物体关系（如 counterfactual）捕捉不准，缺更精细的自动评测。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2210.15257
- arxiv_pdf: https://arxiv.org/pdf/2210.15257
- project（文心一格产品页）: https://wenxin.baidu.com/ernie-vilg
- code & ViLG-300 数据: https://github.com/PaddlePaddle/ERNIE/tree/ernie-kit-open-v1.0/Research/ERNIE-ViLG2

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2210.15257.pdf
