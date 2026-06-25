---
title: "CommonCanvas: An Open Diffusion Model Trained with Creative-Commons Images"
org: "Cornell Tech & Databricks Mosaic (MosaicML)"
country: US
date: "2023-10"
type: paper
category: t2i
tags: [t2i, latent-diffusion, creative-commons, synthetic-caption, copyright, blip-2, stable-diffusion, data-efficient]
url: https://arxiv.org/abs/2310.16825
arxiv: https://arxiv.org/abs/2310.16825
pdf_url: https://arxiv.org/pdf/2310.16825
github_url: https://github.com/mosaicml/diffusion
hf_url: https://huggingface.co/common-canvas
modelscope_url:
project_url: https://github.com/mosaicml/diffusion/blob/main/assets/common-canvas.md
downloaded: [arxiv-2310.16825.pdf, commoncanvas--readme.md, commoncanvas--common-canvas-doc.md, commoncanvas--hf-xl-nc.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CommonCanvas 是**仅用 Creative-Commons 授权图像 + BLIP-2 合成 caption** 训练出来的开源 t2i 隐扩散模型族（沿用 SD2 / SDXL 的 U-Net 架构），核心创新是用"telephoning"（一种把无 caption 图像通过预训练 captioner "有损压缩"成文本标签的迁移学习）解决 CC 图像缺 caption 的问题；**最亮眼结果**：最大的 CommonCanvas-LNC（SDXL U-Net）在 PartiPrompts 人评上与 SD2-base **无统计学显著差异**，却只用了不到 LAION 数据量的 3%（约 7000 万张，比 SD2 少约 33 倍），并配套一套实现 **2.71× 训练加速**的工程 recipe。

## 背景与定位
当时主流 t2i（SD/SDXL）都在 web 抓取的 [[laion]]-2B/5B 上训练，存在两大悬而未决的问题：
- **版权**：LAION 图像来源不明，是否构成"合理使用（fair use）"美国法院尚无定论，且当时已有 Anderson v. Stability AI、Getty v. Stability AI 等多起诉讼。
- **可复现性**：LAION 数据集只存图像 URL 不存图像本身，存在严重 link rot，无法完整复现，还易被数据投毒攻击。

本文回答的问题是：**能否只用 CC 授权数据高效训出一个高质量 t2i 模型？** 这是首个（据作者所知）"完全只用开放授权数据训练 t2i"的公开工作。它的定位不是刷 SOTA 画质，而是给"绕开版权"提供一条可行路径，并附带证明了"扩散模型其实被严重欠参数化（underparameterized），用远少于 LAION 的数据就能饱和 SD2"这一发现。技术上承接 [[latent-diffusion-ldm]] / [[stable-diffusion]] / [[sdxl]]，captioner 用 [[blip-2]]。

两大子挑战：
1. **数据不完整（incompleteness）**：CC 图像几乎都没有训练 t2i 所需的 caption。
2. **数据稀缺（scarcity）**：高分辨率 CC 图像只有约 7000 万张，对比 LAION-2B 的约 20 亿。

## 模型架构
完全沿用 Stable Diffusion 的隐扩散（LDM）范式：VAE 把图压到 latent，U-Net 在 latent 空间做迭代去噪，文本编码器注入条件。模型族分两种规模：

- **CommonCanvas-S（Small）**：与 **SD2 完全同构**——相同参数量、相同结构、相同 VAE / tokenizer / U-Net 命名方案，甚至能直接把 SD2 权重载入本框架。U-Net 约 **8.66 亿（866M）可训练参数**。文本编码器为 SD2 的 OpenCLIP（hidden dim = 1024）。唯一改动：把归一化层降精度（见训练方法）。
- **CommonCanvas-L（Large，即 LNC）**：把 SD2 的 U-Net **替换为 SDXL 的 U-Net**（约 **25.67 亿 / 2567M 参数**），并采用 SDXL 改进版 VAE。为适配，把 cross-attention 维度从 SDXL 的 2048 改回 SD2 文本编码器的 1024；除此之外与 SD2 架构一致。**注意**：它没有照搬 SDXL 的多文本编码器 / aspect-ratio bucketing / micro-conditioning 等全套改造，只是"换了个更大的 U-Net 主干"。
- **分辨率策略**：两阶段，先在 256×256 训练，再切到 512×512 继续训。最终发布模型为 512×512。

命名规则 `CommonCanvas-<架构 S/L/XL>-<数据 C/NC>`：C = 仅商用许可子集，NC = 含非商用许可的更大子集。

捕获 caption 的 BLIP-2（用于造数据，非模型组件本身）由三部分组成：冻结视觉编码器 + 可训练 Q-Former transformer + 冻结 LLM（OPT-2.7B），只训练中间 transformer。

## 数据
**CommonCatalog 数据集**（本文同时开源）：
- **来源**：起点是 YFCC100M（1 亿张 CC 授权图 + Flickr ID）。但原始 YFCC 图分辨率低、且很多许可不允许分发衍生作品，不适合直接训 SD。作者**用 Flickr ID 按原图重新抓取（re-scrape）**，得到超 4K 的高分辨率原图。
- **许可分层与规模**（论文 Table 1，基于 YFCC 的 CC 许可统计）：
  - **CommonCatalog-C（商用）**：约 **26,232,417 张**（≈2600 万），其中 30.76% 自带 alt-text。只含 CC-BY-SA-2.0 + CC-BY-2.0 两类许可。
  - **CommonCatalog-NC（含非商用）**：约 **67,015,331 张**（≈6700 万），31.22% 自带 alt-text。在 C 基础上再加 CC-BY-NC-2.0、CC-BY-NC-SA-2.0。
  - **明确排除**约 3000 万张非衍生（ND, non-derivative）许可图像，不用于训练，但仍为它们生成 BLIP-2 caption 作为**评测集**发布。
- **合成 caption（核心）**：对比多个 captioner 后，基于 MS COCO 上的 SOTA 表现选定 **BLIP-2 OPT-2.7B**，为全部 YFCC CC 图像生成合成 caption。captioning 阶段先把图 center-crop + resize 到最大 512×512（原图整图 caption 太贵）；**但训练扩散模型时图像保持原生分辨率**。整个 captioning 花费约 **1,120 A100 GPU·时**。
- **caption 质量观察**：BLIP-2 合成 caption 往往比 LAION-2B 原始 alt-text 更贴近"人会怎么写"——原始 alt-text 常含产品名、无关细节、语法差（如相机自动生成的 "OLYMPUS+DIGITAL+CAMERA" 这类高频垃圾 caption）。代价是 **caption 多样性下降**（unique trigram 减少）。
- **过滤/安全**：主要是按许可类型过滤（剔除 ND），未报告专门的美学评分过滤或 NSFW 过滤管线；模型卡明确承认仍可能被诱导生成 NSFW，且数据偏向"接入互联网的西方国家"、global south 代表性不足、数据本身约 10 年陈旧（缺现代概念/近期事件/当代名人）。

## 训练方法
- **训练目标**：标准 SD2 的隐扩散（DDPM 式 ε/v-prediction 去噪损失），论文未引入新损失，**完全复刻 SD2 训练 recipe**。无 flow matching、无 next-token、无 masked-token。
- **多阶段**：256×256 预训练 → 512×512 继续训。**未做 SFT / RLHF / DPO / 奖励模型对齐**——这是纯预训练数据替换 + 工程优化的工作，不涉及偏好对齐或蒸馏加速。
- **数据稀缺消融（关键结论）**：在 LAION-1.1B 上训 SD2，对训练数据量做随机下采样实验，发现**从 1000 万增到 9000 万样本，COCO 上的 FID/KID/CLIP-FID 等指标几乎不再改善**（论文 Fig. 8）；低于约 1000 万样本时训练才开始不稳定（Fig. 15）。由此推断只需 <3% LAION-2B 即可"饱和" SD2，约 7000 万 CC 图足够。
- **欠参数化假说**（附录 A.1）：用 latent 空间记忆容量做估算，临界数据量 Nc ≈ 0.2M（SD2）/ 0.6M（CC-Large），远低于 YFCC 数据规模——说明这些扩散模型在该数据量下不会过拟合，larger model 反而更好（CC-LNC > CC-SNC），印证"模型被欠参数化"。
- **降精度 trick**：把通常用 float32 的 GroupNorm / LayerNorm **降到 float16**（前人 MosaicBERT 工作显示 LayerNorm float16 安全，作者发现 GroupNorm 同样安全），减少频繁 upcast 带来的瓶颈与显存。由 MosaicML Composer 库自动替换归一化层。
- **telephoning（数据侧方法，非训练 loss）**：把高维图像经 BLIP-2 "有损压缩"成短文本，再用该文本训另一个生成模型。因压缩有损，即便 BLIP-2 见过 LAION 里的 Snoopy，它产出的 caption（"a black and white cartoon dog with black ears"）也不含 "Snoopy"，下游模型据此生成的图也不像 Snoopy——作者据此论证可绕开 verbatim 版权风险。

## Infra（训练 / 推理工程）
这是本工作的重头，目标是把 SD2 训练成本从"几周到一个多月"压下来，最终相对自家 SD2 baseline 实现 **2.71× 加速**。四项核心优化（论文 §5.1、附录 D）：
- **Flash Attention（xFormers 实现）**：替换 U-Net 中大量 cross-attention，省算力省显存。
- **预计算 latents**：把整个数据集的 VAE latent 与文本编码 latent **离线预计算**，训练时不再每步重算（低分辨率阶段收益最大）。一次性预计算 VAE + CLIP latents 花约 **3,784 A100·时（≈$7,600）**；若边训边算，时间/成本约增 1.4×。（注：3,784 A100·时 / $7,600 / 1.4× 这组具体数字仅见于 GitHub README，论文正文只说"一次性固定开销"未给数。）
- **GroupNorm / LayerNorm 降到 float16**：减显存、提速。
- **FSDP（SHARD_GRAD_OP 模式）**：分片参数/梯度/优化器状态，在大规模（scale 上）收益显著、近线性扩展。
- **scheduled EMA**：只在训练最后 ~3.5%（约 5 万步）维护权重 EMA，避免全程 EMA 的读写开销，得到近乎等效的 EMA 模型。

**算力 / 吞吐（A100，下表为论文 Table 5；README 另有一张同结构表但所用图像数/天数/成本不同，如 8 卡 81.33 天 / $31,230，勿混用）**：U-Net 训练吞吐随 GPU 数从 8 扩到 128：
| A100 数 | 256×256 (img/s) | 512×512 (img/s) | 512×512+EMA | 训练天数 | 成本 |
|---|---|---|---|---|---|
| 8 | 1100 | 290 | 290 | 101.04 | $38,800 |
| 16 | 2180 | 585 | 580 | 50.29 | $38,630 |
| 32 | 4080 | 1195 | 1160 | 25.01 | $38,420 |
| 64 | 8530 | 2340 | 2220 | 12.63 | $38,800 |
| 128 | 11600 | 4590 | 3927 | 6.79 | $41,710 |

对比：Stability 报告训 SD2 约需 **200,000 A100·时**；无这套优化时同样训练成本约 **$90,000–$140,000**，优化后单次约 **$3.8–4.2 万**。低精度优化主要降显存从而能加大 microbatch 提升利用率；FSDP 在 scale 上贡献最大；latent 预计算在低分辨率贡献最大。
- **推理**：模型卡给出 diffusers `StableDiffusionXLPipeline` 用法，建议配合 perturbed-attention-guidance 自定义 pipeline，示例 25 步推理；提供 ComfyUI/A1111 用的 safetensors。**未报告**专门的步数蒸馏 / 量化 / consistency / LCM 等推理加速（本工作不做蒸馏）。
- 工程栈：MosaicML Composer（训练/自动替换层）+ Streaming（数据加载）+ PyTorch FSDP。

## 评测 benchmark（把效果讲清楚）
**自动指标**（MS COCO，30K 样本）：FID、KID、CLIP-FID 与 CLIP Score。整体 CommonCanvas 与 SD2-base **相当（comparable）**，但在 faces、general photography、paintings 几类（源自 Conceptual Captions 的 web 抓取 caption）上**偏弱**——存在 COCO caption 与 web caption 的 domain shift，且 CLIP-FID 本身偏向 SD2（CLIP 训练文本风格接近 LAION）。

**数据量消融**（Fig. 8）：在 LAION 上，**10M→90M 样本，FID/KID/CLIP-FID 在 guidance 1–8 全程几乎不改善**；且**合成 BLIP-2 caption 的 CLIP Score 高于原始 ground-truth caption**——合成 caption 反而提升了图文对齐。

**人评（PartiPrompts，pairwise 偏好，512×512）**——报"用户更偏好 CommonCanvas 而非 SD2-base 的比例"（论文 Fig. 7）：
- CommonCanvas-SC：**37%**
- CommonCanvas-SNC：**38%**
- CommonCanvas-LNC（SDXL U-Net）：与 SD2-base **无统计学显著差异**（约 0.5 上下，即基本打平）

作者强调：两个 Small 模型偏好率虽略低于 50%，但考虑到数据集只有 SD2 的 <3% 且全是合成 caption，37–38% 已"出乎意料地高"；而 LNC 打平 SD2 则是"存在性结果（existential result）"——证明可以用少几个数量级的数据匹配 SD2。

**版权/记忆性定性评测**（Fig. 1/2/10/11/14）：对 "Elsa from Frozen"、"the lion king"、Snoopy、Indiana Jones、Harry Potter 等诱导性 prompt，CommonCanvas 比 SD2 **更不容易生成 iconic 角色/版权形象**；对名人（Bill Gates、Elon Musk、Obama 等）合成能力也弱于 SD2（被作者定位为 feature 而非 bug）。

**消融小结**：(1) 数据 10M→90M 几乎无增益 → 扩散模型欠参数化；(2) 合成 caption 提 CLIP 对齐但降 n-gram 多样性；(3) 换大 U-Net（S→L）在小数据上不过拟合且更优。

## 创新点与影响
**核心贡献**：
1. **CommonCatalog**：首个完全开放授权（CC）、已知 provenance、可整体分发（解决 link rot）的大规模 t2i 训练数据集（C ≈2600 万 / NC ≈6700 万），含 BLIP-2 合成 caption，连同 ND 子集的 caption 一并作评测集发布。
2. **CommonCanvas 模型族**：首个（据作者所知）**只用开放授权数据 + 纯合成 caption** 训出的、画质与 SD2 相当的公开 t2i 模型族；LNC 在人评打平 SD2。
3. **telephoning**：把"用预训练生成模型造合成标签喂下游生成模型"这一日益普遍的模式命名化，并用其论证版权"有损压缩"绕开机制。
4. **数据效率发现**：实证扩散模型被欠参数化，<3% LAION-2B 即可饱和 SD2；配套 2.71× 工程加速 recipe + 完整成本表，降低复现门槛。

**影响**：成为"用 CC/开放授权数据回应 t2i 版权争议"的代表性实践，与后续 Adobe Firefly（自有/授权库）、Public Diffusion 等"clean data"路线呼应；synthetic re-captioning 思路与同期 DALL·E 3、PixArt-α 的 caption upsampling 相互印证（本文为其中"无任何 ground-truth caption"的极端版）。

**已知局限**（论文 §7 + 模型卡）：
- faces / 摄影 / 绘画类偏弱；难生成具体名人、知名艺术品、特定地点。
- YFCC 数据约 10 年陈旧，缺现代概念与近期事件；偏向西方、global south 代表性不足。
- 合成 caption 多样性下降；图中文字难读；复杂组合理解弱；主要英文。
- 仍可被对抗 prompt 诱导出 iconic 角色或 NSFW（只是概率低于 SD2）。
- BLIP-2 本身在 LAION 上预训练，"绕开版权"依赖"有损压缩使输出不 resemble 输入"的论证，作者把 fair use 判断"deferred to experts"。
- NC 变体**明确禁止商用**（cc-by-nc-sa-4.0）；只有 C 变体可商用。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2310.16825
- arxiv_pdf: https://arxiv.org/pdf/2310.16825
- github (MosaicML diffusion 训练代码): https://github.com/mosaicml/diffusion
- project_doc (repo 内 common-canvas.md): https://github.com/mosaicml/diffusion/blob/main/assets/common-canvas.md
- hf_org (模型与数据集): https://huggingface.co/common-canvas
- hf_model_card (旗舰 XL-NC): https://huggingface.co/common-canvas/CommonCanvas-XL-NC
- hf_space_demo: https://huggingface.co/spaces/common-canvas/CommonCanvas

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2310.16825.pdf
- ../../../sources/omni/2023/commoncanvas--readme.md
- ../../../sources/omni/2023/commoncanvas--common-canvas-doc.md
- ../../../sources/omni/2023/commoncanvas--hf-xl-nc.md
