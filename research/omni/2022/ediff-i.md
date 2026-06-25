---
title: "eDiff-I: Text-to-Image Diffusion Models with an Ensemble of Expert Denoisers"
org: NVIDIA
country: US
date: "2022-11"
type: tech-report
category: t2i
tags: [diffusion, text-to-image, ensemble-of-experts, cascaded-diffusion, t5, clip, paint-with-words, edm, nvidia]
url: "https://arxiv.org/abs/2211.01324"
arxiv: "https://arxiv.org/abs/2211.01324"
pdf_url: "https://arxiv.org/pdf/2211.01324"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://research.nvidia.com/labs/dir/eDiff-I/"
downloaded: [arxiv-2211.01324.pdf, ediff-i--project-page.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
eDiff-I 是 NVIDIA 2022.11 的级联文生图扩散模型，核心创新是**按去噪阶段切换的"专家去噪器集成"（Ensemble of Expert Denoisers）**——在不增加单步推理算力的前提下扩容模型，并在同一模型内**同时使用 T5-XXL + CLIP 双文本编码器 + CLIP 图像编码器**（论文列为三大贡献之一），外加 training-free 的 **paint-with-words** 空间控制。在 MS-COCO 256×256 zero-shot FID-30K 上达到 **6.95**（Config-D），优于同期 [[imagen]]（7.27）与 Parti（7.23）。

## 背景与定位
2022 年大规模文生图扩散模型（[[glide]]、[[dalle-2]]、[[imagen]]、[[latent-diffusion-ldm]] / Stable Diffusion）已证明扩散模型在文本对齐与零样本泛化上的统治力，业界共识是"scale 即正义"（论文引用 Sutton 的 bitter lesson）。但单纯加深/加宽去噪网络会**线性放大采样开销**——因为采样要解一个反向 ODE/SDE，去噪网络要被调用很多次（NFE 很高）。eDiff-I 要解决的核心问题是：**如何在不增加测试时单步算力的前提下扩容文生图扩散模型**。

论文的关键经验观察（它的立论基石）：**文生图扩散的去噪行为随噪声尺度 σ 发生质变**。
- 采样早期（σ 大、输入近纯噪声）：模型主要**依赖文本提示**来确定文本对齐的全局内容；
- 采样后期（σ 小）：粗结构已成形，模型**几乎忽略文本**，转而靠视觉特征补高频细节。

论文用两个证据验证：(1) 可视化 cross-attention 热力图——高噪声段文本 token 注意力强，低噪声段几乎全注意力落到 null token（图 3）；(2) prompt-switching 实验——在去噪最后 7% 段切换 caption，输出几乎不变；在前 40% 段切换，输出完全改变（图 4）。既然两个阶段是"截然不同的任务模式"，**用一套共享参数+简单时间嵌入去拟合全过程并非最优**——这就引出了按阶段切换专家的设计。

它处在扩散模型缩放方法谱系里的"稀疏专家"一侧：和 MoE（per-input 路由）不同，eDiff-I 是 **per-noise-level 路由**——同一张图的不同采样步用不同专家，单步仍只跑一个网络，因而扩参不增推理算力。

## 模型架构
**整体形态：三段级联扩散（pixel-space cascade）**，沿 [[imagen]] 的级联思路（非 latent 空间）：
- **Base 模型**：生成 64×64 图像。架构是改造版 Dhariwal & Nichol（[[diffusion-models-beat-gans]]，ADM "Diffusion Beats GANs"）的 U-Net。
- **SR256**：上采样 64→256，改造版 Imagen 的 Efficient U-Net。
- **SR1024**：上采样 256→1024，Efficient U-Net；训练时用随机 256×256 patch、推理时整图 1024×1024。SR1024 **去掉自注意力只保留交叉注意力**（自注意力在 1024 分辨率推理太贵）。

**条件注入（双路）**：
1. **全局条件（加到时间嵌入上）**：pooled CLIP 文本嵌入 + CLIP 图像嵌入。注意**不用** pooled T5（论文论证 CLIP 文本与图像对齐更适合做全局向量）。
2. **交叉注意力（多分辨率）**：在 Dhariwal U-Net 每个自注意力块后**新增交叉注意力块**，key/value 是三种嵌入拼接——**CLIP L/14 文本（77 token）+ T5-XXL（113 token）+ pooled CLIP 图像（1 token）**，再加一个**可学习 null embedding**（当模型不需要条件时可注意它，自然支持 classifier-free guidance）。

**文本/图像编码器**：T5-XXL（语言建模目标，擅长长描述、组合/计数）+ CLIP L/14 文本（图文对齐，擅长全局观感）+ CLIP L/14 图像（风格迁移）。论文指出二者**互补**：CLIP-only 前景对象对，但缺组合/计数/文字渲染；T5-only 组合好但前景对象（如狗的品种）易错；**T5+CLIP 取两者之长**。这三种嵌入对全数据集**离线预计算**（在线算太贵）。

**专家集成（核心创新，见下"训练方法"）**：base 与 SR256 各被拆成若干个"专家去噪器"，每个专家只负责一个噪声区间。最终系统典型形态是 **3 个 base 专家**：低噪声专家 + 高噪声专家 + 一个覆盖中间所有噪声段的专家。**单步推理只调用当前 σ 所属的那一个专家**，故推理 NFE/单步算力与单模型相同。

**参数量（Table 1，含文本编码器）**：eDiff-I 各配置 6.8B / 7.1B / 8.1B / 9.1B（Config-A→D）。对比 Imagen 7.9B、Parti 20B、DALL·E 2 6.5B、Stable Diffusion 1.4B。

**U-Net 关键超参（附录 A）**：
- Base（64×64，Table 2）：channel mult [1,2,4,4]，基础通道 256，每级残差块 3，self/cross-attention 在分辨率 [32,16,8]，use scale-shift norm。
- SR256（Table 3）：channel mult [1,2,4,8]、block mult [1,2,4,4]，基础通道 128，残差块 2，self/cross-attention 仅在 [32]。
- SR1024（Table 4）：patch 256×256，channel mult / block mult [1,2,4,4]，基础通道 128，残差块 2，**仅 cross-attention 在 [32]，无 self-attention**。

## 数据
- **规模**：约 **10 亿（~1B）图文对**。来源是**公开 + 专有数据集的混合**（具体数据集名称未披露）。
- **过滤/清洗**：用预训练 **CLIP 模型算图文对齐分**，再用**美学打分器（aesthetic scorer）排图像质量**；**剔除低于预设 CLIP 分阈值与美学分阈值的图文对**。
- **分辨率筛选与各模型用数据**：所有图像最短边 > 64px，全部用于训练 base；最短边 > 256px 用于 SR256；最短边 > 1024px 用于 SR1024。
- **预处理**：base 与 SR256 用 resize + center-crop（先 resize 使最短边等于目标边）；SR1024 训练随机裁 256×256 区域。
- **超分训练增广**：SR 模型训练时对低分辨率条件输入施加**随机退化/腐蚀**（degradation，参考 Real-ESRGAN 思路），以便推理时去除 base 输出里的伪影、提升泛化。
- **评测留出**：COCO、Visual Genome **不在训练集**中（保证 zero-shot 评测）。
- 数据配比细节、各源占比、人工标注/re-caption 均**未披露**。

## 训练方法
**扩散框架：EDM（Karras et al. 2022）连续噪声形式 + 预条件去噪器**，而非离散 DDPM εθ。
- 训练目标：去噪回归 `E[λ(σ)·‖D(x_clean+σε; e, σ) − x_clean‖²]`，σ 从 **log-normal** 采样 `ln(σ)~N(Pmean=−1.2, Pstd=1.2)`，σ_data=0.5（自然图像像素标准差近似），λ(σ) 抵消 Fθ 的输出加权。预条件 `D(x;e,σ)=c_skip·x + c_out·Fθ(...)`，遵循 EDM 公式。

**专家集成的"二叉树分支"高效训练策略（Sec 4.1 + 附录 B，核心 trick）**：
1. 先训一个**全噪声区间共享的基础模型**（base 训到 ~1.45M / 总 1.9M 迭代）。
2. 把噪声分布 p(σ)（按面积）二等分，**用共享模型初始化**两个 level-1 专家（低噪/高噪），各 fine-tune 较少步数。
3. 递归二分、继续从父节点初始化、继续 fine-tune，构成二叉树（level l 理论上 2^l 个模型）。
4. **关键省算力 trick**：不训满整棵树——发现中间区间的专家对最终系统贡献小，于是**只从二叉树最左与最右节点继续生长**（最高噪声段对文本对齐最关键、最低噪声段对锐度最关键），中间所有噪声段用**一个互补模型**（记 −(9,511) 即"除该叶子外所有噪声"）覆盖。
5. 训练计划（Table 5，base）举例：共享模型 500K → 各级专家 fine-tune 40K~190K 不等；最终典型形态 = `E0`（低噪）+ `E(9,511)`（高噪叶子）+ 中间互补模型 `M^C`。因为专家是从父模型初始化再短 fine-tune，**总训练开销远小于从头训多模型**。
- 关键对照设定：为公平比较，"4 专家集成训 600K 步" vs "baseline 训 800K 步"——保证两者**看过相同数量的训练样本**。

**优化超参（Table 7）**：AdamW，lr=1e-4，weight decay=0.01，betas=(0.9,0.999)，EMA=0.9999，batch size=2048，开启 gradient checkpointing。**条件 dropout 独立施加**：CLIP 文本 0.2 / T5 文本 0.25 / CLIP 图像 0.9（dropout 时整个 embedding 张量置零；三者全 drop = 无条件训练，供 CFG）。CLIP 图像 0.9 的高 dropout 让模型大部分时候不依赖参考图，仅在需要风格迁移时启用。
- 迭代数：base 1.9M、SR256 2M、SR1024 1.7M。

**Paint-with-words（training-free，Sec 4.3）**：无需额外训练。用户在画布上为选定短语涂二值 mask，构造 attention 矩阵 A∈R^{Ni×Nt}（mask 双线性下采样匹配各层分辨率），把 A 加到所有交叉注意力层：`softmax((QKᵀ + w·A)/√dk)·V`。权重调度 `w = w0·log(1+σ)·max(QKᵀ)`——**高噪声段权重更大**（因核心布局在高噪声段形成），并让 A 的影响与 Q/K 尺度无关。直觉：在某区域涂某短语，该区域图像 token 更倾向注意该短语 token，对应语义更可能出现在该位置。

## Infra（训练 / 推理工程）
- **算力**：base 模型用 **256× NVIDIA A100**，两个 SR 模型各用 **128× A100**。
- **框架**：基于 NVIDIA **Imaginaire** 库（PyTorch）。开启 gradient checkpointing 省显存。
- **嵌入预计算**：全数据集的 T5/CLIP-text/CLIP-image 嵌入**离线预算并缓存**（在线计算太贵），是大规模训练的关键工程优化。
- **推理采样器（Table 7）**：base 用 **DEIS（Zhang et al.）+ 3-kutta，order 6，25 步**；SR 用 **DEIS + 3-kutta，order 3，10 步**。采样从 N(0, σ_max²·I) 起，反解生成 ODE，σ 从 σ_max 退火到 σ_min≈0；亦可走 SDE。
- **核心工程卖点（图 13）**：在 A100 上对 base 网络做 100 次前向计时——"加深网络"方案随参数量 1B→6B **单步前向时间线性上涨**；而"加专家"方案**单步前向时间恒定**（因为每步只跑一个专家）。这就是 eDiff-I "扩参不增推理算力"的实测依据。
- 总 GPU-hours、吞吐量、量化/蒸馏加速**未披露**（论文未做步数蒸馏类加速，纯靠 DEIS 少步采样）。

## 评测 benchmark（把效果讲清楚）
**主结果：MS-COCO 2014 validation，256×256，zero-shot FID-30K（30K 随机 caption；越低越好；参数量含文本编码器）— Table 1**：

| 模型 | 参数量 | Zero-shot FID-30K ↓ |
|---|---|---|
| GLIDE | 5B | 12.24 |
| Make-A-Scene | 4B | 11.84 |
| DALL·E 2 | 6.5B | 10.39 |
| Stable Diffusion | 1.4B | 8.59 |
| Imagen | 7.9B | 7.27 |
| Parti | 20B | 7.23 |
| **eDiff-I Config-A**（baseline，无专家） | 6.8B | **7.35** |
| **eDiff-I Config-B**（SR256 用 2 专家） | 7.1B | **7.26** |
| **eDiff-I Config-C**（base 2 专家 + SR256 2 专家） | 8.1B | **7.11** |
| **eDiff-I Config-D**（base 3 专家 + SR256 2 专家） | 9.1B | **6.95** |

结论数字：
- baseline（Config-A，7.35）已优于 GLIDE/DALL·E 2/Make-A-Scene/Stable Diffusion，略逊于 Imagen/Parti。
- 仅对 SR256 加 2 专家（Config-B，7.26）即**略胜 Imagen**。
- base 加 2 专家（Config-C，7.11，参数量≈Imagen）**同时超过 Imagen 与 Parti**（分别低 0.16 / 0.12）。
- base 加 3 专家（Config-D）拿到**全表最优 6.95**。（注：正文一处叙述把 best 写作 "7.04"，与 Table 1 的 6.95 存在不一致，以 Table 1 数字为准。）

**消融与 trade-off 曲线**：
- **专家集成 vs baseline（图 7）**：在 COCO 与 Visual Genome 上扫 CFG（0~10）画 FID-5K vs CLIP-g/14 score 折中曲线；"4 专家训 600K" 在**整条折中曲线上**一致优于 "baseline 训 800K"（同样本量对照）。
- **文本编码器消融（图 8、图 18）**：T5+CLIP > T5-only ≈/> CLIP-only。COCO 上 T5-only 与 CLIP-only 接近、T5+CLIP 明显最好；Visual Genome（caption 平均 61.92 词，远长于 COCO 的 10.62 词）上 **T5-only 明显优于 CLIP-text-only**（长描述更吃语言模型），但 T5+CLIP 仍最佳。定性：CLIP-only 前景对、缺组合/计数/文字；T5-only 组合好但前景对象易错。
- **专家数效应**：随专家数增加，标准图像质量指标改善，而推理单步算力恒定（图 13）。
- **定性对比（图 9~12）**：与 Stable Diffusion / DALL·E 2 比，eDiff-I 在**多实体属性绑定**（不混淆属性）、**英文文字渲染**（"NVIDIA rocks" 等，对手常拼错/漏字）、**长描述**三类难例上更准（人工挑最优样本展示）。

注：论文**未报告** GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 人评 ELO 等后续才流行的 benchmark（2022 年这些尚未成为标准）；评测口径只有 zero-shot FID-30K（COCO）+ FID-CLIP 折中曲线（COCO/VG）。

## 创新点与影响
**核心贡献**：
1. **Ensemble of Expert Denoisers**：基于"去噪行为随 σ 质变"的观察，把扩散去噪器按噪声区间拆成多个专家，**扩容而不增推理单步算力**；并用二叉树分支 + 父模型初始化 + 只长两端 + 中间用互补模型，把多专家训练成本压下来。这是 per-noise-level 的"稀疏专家"，区别于经典 MoE 的 per-input 路由。
2. **三编码器混合条件**：在同一文生图模型里**同时用 T5-XXL + CLIP 文本 + CLIP 图像**（论文将"ensemble of encoders"列为三大贡献之一），论证 T5（组合/计数/文字）与 CLIP（全局观感）互补，CLIP 图像嵌入额外解锁**即时风格迁移**（用参考图风格条件化）。
3. **Paint-with-words**：training-free 的交叉注意力调制，让用户涂语义 mask 控对象空间布局，单次前向从零生成多概念整图（不像 inpainting 需从已有图起步）。

**影响**：
- "去噪不同阶段任务模式不同"这一观察，启发了后续一批**多专家 / 阶段化扩散**工作（如把时间步分段用不同模型/不同 CFG 调度），也呼应了后来 SDXL 的 base+refiner（按噪声段分工）、以及 MoE-Diffusion / 时间步路由类研究。
- T5+CLIP 双编码器、CLIP 图像嵌入做风格条件，成为后续多模态条件注入的常见配方之一。
- Paint-with-words 的交叉注意力 mask 调制，是早期 training-free 空间可控生成（与 Prompt-to-prompt、attention 控制系列同期）的代表手法之一。

**已知局限**：
- **闭源**：权重与代码均未公开（NVlabs 无官方仓库，README 404），无法复现/直接使用，影响力主要在方法层面而非生态层面。
- 仍是 **pixel-space 级联**（非 latent），三段模型 + 大量 A100，训练/部署门槛高；同期 latent diffusion（Stable Diffusion）路线在效率与开源生态上更占优，长期主导了社区。
- 评测仅 FID/CLIP，缺组合性专项 benchmark 与人评 Arena 的系统量化。
- 数据来源/配比、总算力开销不透明。
- 多专家带来存储/部署复杂度（需切换加载多套权重）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2211.01324
- arxiv_pdf: https://arxiv.org/pdf/2211.01324
- project_page: https://research.nvidia.com/labs/dir/eDiff-I/ （重定向至 https://research.nvidia.com/labs/cosmos-lab/ediff-i/）
- video: https://youtu.be/WbaVvlgxbl4

## 本地落盘文件
- ../../../sources/omni/2022/arxiv-2211.01324.pdf （论文全文，v5 / 2023-03-14；PDF 不入 git，本地精读）
- ../../../sources/omni/2022/ediff-i--project-page.md （NVIDIA 官方项目页 cloakbrowser 快照）
