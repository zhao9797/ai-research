---
title: "Marigold: Repurposing Diffusion-Based Image Generators for Monocular Depth Estimation"
org: "ETH Zürich (Photogrammetry and Remote Sensing)"
country: EU
date: "2023-12"
type: paper
category: method
tags: [depth-estimation, diffusion, latent-diffusion, fine-tuning, zero-shot, dense-prediction, generative-prior, affine-invariant]
url: "https://arxiv.org/abs/2312.02145"
arxiv: "https://arxiv.org/abs/2312.02145"
pdf_url: "https://arxiv.org/pdf/2312.02145"
github_url: "https://github.com/prs-eth/Marigold"
hf_url: "https://huggingface.co/prs-eth/marigold-depth-v1-1"
modelscope_url: ""
project_url: "https://marigoldmonodepth.github.io"
downloaded: [arxiv-2312.02145.pdf, marigold--readme.md, marigold--hf-depth-v1-1-card.md, marigold--hf-lcm-card.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Marigold 把一个预训练文生图模型（Stable Diffusion v2）**仅微调 U-Net、保持 VAE/latent 空间不变**，几天单卡、**只用合成 RGB-D 数据**就改造成单目深度估计器；它从生成先验中继承了"百科全书式"的视觉世界知识，在 5 个真实数据集上**零样本 SOTA**（个别场景误差降幅 >20%），是"生成先验迁移到稠密预测"范式的标志性工作，获 CVPR 2024 Oral + 最佳论文奖候选。

## 背景与定位
单目深度估计是从单张图回归每像素深度，几何上欠定，必须靠先验（物体常见形状/尺寸、场景布局、遮挡关系）才能求解——本质上需要"场景理解"。此前的"通用深度估计"路线（[[midas]] / [[dpt]] / Omnidata）走的是**堆数据**：混合多个真实 RGB-D 数据集训练高容量网络，从 CNN 演进到大 ViT，并加辅助任务来积累视觉知识。但这类模型对训练分布外的内容/布局仍易失效。

Marigold 换了一条路：**不再自己攒大数据集，而是复用文生图扩散模型里已经压缩好的互联网级视觉先验**。其直觉是——既然现代图像扩散模型（在 LAION-5B 上训过 [[latent-diffusion-ldm]] / Stable Diffusion）已经"懂"各种场景的样子，那就应该能从它里面"提取"出一个泛化良好的深度估计器。关键洞察是**保持 latent 空间不动**，只微调去噪 U-Net，就能在不"遗忘"视觉先验的前提下完成任务适配。它做的是 **affine-invariant depth**（深度值仅差一个全局 offset 与 scale），这是 in-the-wild（相机内参未知）场景下的合理折中。技术脉络上承 [[ddpm]] / [[ddim]] / [[latent-diffusion-ldm]]，与同期把 SD 当特征提取器的 VPD、把扩散用于度量深度的 DepthGen/DDVM/DiffusionDepth 形成对比——后者多只在各自训练域内有效，Marigold 强调跨域零样本。

## 模型架构
**Backbone：U-Net（Stable Diffusion v2 的 latent diffusion）**，非 DiT。整套设计的原则是"对预训练模型改动最小"：

- **VAE/tokenizer：完全冻结、原封不动复用 SD 的 VAE**。这是全文的核心赌注——作者实验证明 SD 的图像 VAE 不经任何改动就能编码/解码深度图，重建误差可忽略（Hypersim 上 MAE = 0.0095 ± 0.0091，远低于当前深度估计误差）。深度图是单通道，于是把它**复制成 3 通道**伪装成 RGB 喂入 VAE；推理时把解码出的 3 通道**取平均**作为最终深度（附录测得 3 通道间不一致性极小，std≈0.0022–0.0027）。
- **条件注入：latent 通道拼接（concat）**。把图像 latent z(x)=E(x) 与含噪深度 latent z_t^(d) 沿特征维拼接成 cat(z_t^(d), z^(x)) 一起喂 U-Net，于是去噪器学的是 ε_θ(z_t^(d), z^(x), t)。为此把 U-Net **第一层输入通道数翻倍**；为避免第一层激活幅度膨胀、尽量保留预训练结构，**把输入层权重张量复制一份并整体除以 2**。这是唯一改动 U-Net 结构的地方。
- **Text encoder：禁用文本条件**（去掉 prompt 分支），任务是纯图像条件的稠密回归，不需要文本。
- **分辨率策略**：SD 在 768×768 上效果最好，推理脚本默认把输入 resize 到处理分辨率再贴回原分辨率；训练时 Hypersim resize 到 480×640、Virtual KITTI crop 到 KITTI 基准分辨率。
- **参数量**：论文未单独报告 Marigold 的总参数量，约等于 SD v2 的 U-Net（约 8.65 亿）+ 冻结 VAE，差异仅在第一层翻倍的少量参数（论文"未单独披露"具体数字）。

## 数据
**只用合成数据，不用任何真实深度。** 总计约 **74K 合成深度样本**：

- **Hypersim**：照片级真实感的合成室内数据集，461 个室内场景；用官方 split 中 365 个场景约 **54K** 样本训练，过滤掉不完整样本，并把"相对焦点的距离"换算成"相对焦平面的常规深度"。
- **Virtual KITTI 2**：合成街景数据集，5 个场景含天气/视角变化；用 4 个场景约 **20K** 样本，crop 到 KITTI 分辨率，远平面设 80m。

**为何坚持合成数据**（两条理由）：① 合成深度**稠密且完整**——每个像素都有有效 GT，而 SD 的 VAE 无法处理含无效像素的图（真实 LiDAR/双目深度普遍有缺失与噪声）；② 合成深度是"最干净"的深度形态，能在短微调过程中**减少梯度噪声**。

**混合采样配比（消融关键结论）**：每个 batch 先按伯努利概率选数据集再采样。仅 Hypersim 即可得到强室内结果；只要掺入约 **5%–10% 的 Virtual KITTI**，室外性能就显著提升，**10% 是甜点**（室内室外同时改善）；Virtual KITTI 比例再升高反而整体下降（两数据集场景多样性/渲染质量不同所致）。

**归一化（affine-invariant 的来源）**：对 GT 深度做线性归一化到约 [−1,1]，用每张图的 **2% 与 98% 分位数**（d₂, d₉₈）做仿射变换 d̃=((d−d₂)/(d₉₈−d₂)−0.5)×2。目的有二：匹配 SD VAE 的输入值域；强制一个与数据统计无关的、规范化的 affine-invariant 表示。

## 训练方法
**训练目标：标准 DDPM 去噪扩散（ε-prediction），在 latent 空间进行。** 把深度估计建模为条件去噪生成 D(d|x)：前向对深度 latent 加噪，反向用 ε_θ(z_t^(d), z^(x), t) 逐步去噪，损失是经典 L2 噪声预测 L = E‖ε−ε̂‖²。骨干沿用 SD v2 原预训练设置的 **v-objective**。

**关键 trick：Annealed Multi-Resolution Noise（退火多分辨率噪声）**——这是论文最重要的训练侧创新之一。
- **多分辨率噪声**：把若干不同尺度的随机高斯噪声图金字塔上采样后叠加，第 i 层权重为 sⁱ（0<s<1）。
- **退火调度**：为了让噪声在去噪末端回归标准高斯，把 i>0 层在时刻 t 的权重改为 (s·t/T)ⁱ——越接近无噪端、低分辨率层权重越小。
- 消融（Tab.2）：标准高斯 → 多分辨率噪声，NYUv2 AbsRel 7.7→5.8、KITTI 14.2→12.1；再加退火 → 5.6 / 11.3。退火噪声还显著提升不同初始噪声下预测的一致性。

**其余超参**：DDPM 训练用 1000 步噪声调度；batch size 32（单卡靠 16 步梯度累积凑出）；Adam，lr=3·10⁻⁵；18K 训练迭代；随机水平翻转增强；约 **2.5 天收敛于单张 RTX 4090**。

**蒸馏/加速（后续 release，非原 CVPR 正文）**：
- 2024-03 发布 **LCM（Latent Consistency Model）蒸馏 checkpoint** `marigold-depth-lcm-v1-0`，把推理压到 1–4 步。
- 2025-05 的 **v1.1** 用更新的噪声调度（**zero-SNR + trailing timesteps**）与增强重训，使**深度仅需 1 步去噪**（`--denoise_steps 1`）即可用于学术对比，法线 4 步、IID 4 步。

## Infra（训练 / 推理工程）
- **训练算力极低**：单张消费级 GPU（RTX 4090）约 **2.5 天**，PyTorch 实现。这是它"affordable / 资源高效"标签的核心卖点——对比堆数据路线动辄多卡多天。
- **混合精度**：推理支持 `--fp16` 半精度（更快、更省显存，但可能略损质量）。
- **推理加速**：训练用 1000 DDPM 步，但推理用 **DDIM 重定时仅 50 步**即可得 SOTA；消融显示 **10 步以内即到边际收益拐点**（比图像生成常用的 50 步还少）；后续 LCM 蒸馏 / v1.1 zero-SNR 进一步压到 **1–4 步**。
- **推理速度（附录 Fig.S2）**：随 ensemble size 与步数线性增长，单卡每样本数秒级（RTX 4090/3090），作者坦承相比前馈方法是"慢但质量高"的取舍。
- **部署形态**：已并入 HuggingFace **`diffusers` 核心**（v0.28.0 起），提供 HF Space 在线 demo、Colab、`nvidia-docker` 本地容器；代码 Apache-2.0、模型 RAIL++-M / OpenRAIL++。

**Test-time ensembling（推理侧关键设计）**：利用生成模型对初始噪声的随机性，对同一输入跑 N 次推理得到 N 个 affine-invariant 预测，再**无需 GT** 地联合估计各自的 scale ŝ/shift t̂ 做空间对齐，逐像素取中位数合并，并加正则项 R=|min(m)|+|1−max(m)| 防止塌缩。消融（Fig.6）：单次预测已不错，10 次 ensemble 把 NYUv2 AbsRel 降约 8%、20 次降约 9.5%，10 次后边际递减。

## 评测 benchmark（把效果讲清楚）
**协议**：affine-invariant 评测——先用最小二乘把合并预测对齐到 GT（disparity 方法对齐到逆深度），再算 **AbsRel↓** 和 **δ1↑**（max(aᵢ/dᵢ, dᵢ/aᵢ)<1.25 的像素占比）。在 **5 个训练中未见过的真实数据集**上零样本评测：NYUv2、KITTI(Eigen split)、ETH3D、ScanNet、DIODE。

主表（Tab.1，AbsRel% / δ1%，**Ours w/ ensemble**）：

| 数据集 | Marigold AbsRel↓ | Marigold δ1↑ | 前 SOTA 对比 |
|---|---|---|---|
| NYUv2 | **5.5** | **96.4** | 此前最好 Omnidata 7.4 / 94.5、HDN 6.9 / 94.8 |
| KITTI | **9.9** | **91.6** | DPT 10.0 / 90.1（论文表中 Marigold 此处 AbsRel 与 δ1 均为加粗最优） |
| ETH3D | **6.5** | **96.0** | DPT 7.8 / 94.6 |
| ScanNet | **6.4** | **95.1** | HDN 8.0 / 93.9、DPT 8.2 / 93.4 |
| DIODE | 30.8 | 77.3 | DPT 18.2 / 75.8（DIODE 上 AbsRel 不占优，但 δ1 最高） |
| **Avg. Rank** | **1.4** | — | Ours w/o ensemble 2.5；最佳竞品 HDN 3.2、DPT 3.9 |

要点：**平均排名 1.4 全场第一**；NYUv2/ETH3D/ScanNet 三个数据集 AbsRel 与 δ1 双双 SOTA；而且训练样本仅 74K（合成），对手用 30 万~1190 万（多为真实）样本——**用最少且零真实深度的数据拿到最好综合表现**。摘要所称">20% 提升"指个别场景/指标的相对降幅。注：DIODE 上 AbsRel 不如 DPT，论文将"远景/远处场景处理"列为已知局限。

**关键消融**：
- **训练噪声**（Tab.2）：annealed multi-res noise 最优（见上）。
- **去噪步数**（Fig.7）：50 步收敛，10 步以内即达边际拐点，可降到 ≤10 步换效率。
- **ensemble size**（Fig.6）：单调改善，10 次后递减；预测一致性也随退火噪声提升。
- **训练数据域**（Tab.3 / S3）：仅 Hypersim 已强；掺 5–10% Virtual KITTI 室内外双升，10% 甜点；加入异域数据不仅提升新域、也回馈原域。
- **VAE 适配性**（附录 B.1/B.2）：SD VAE 直接编解码深度的重建 MAE=0.0095、3 通道一致性 std≈0.002，证明 latent 空间天然适合深度表示。

## 创新点与影响
**核心贡献**：① 提出一个**简单、资源高效的微调协议**，把预训练 LDM 图像生成器改造成图像条件的稠密预测器——**冻结 VAE、只微调 U-Net、latent concat 注入、第一层权重复制减半**；② 给出 SOTA 且通用的单目深度模块，证明"文生图模型里的视觉先验"足以支撑跨域零样本深度估计；③ 配套 affine-invariant 归一化、合成数据训练、退火多分辨率噪声、test-time ensembling 等系列设计。

**影响**：Marigold 把"**repurpose 生成模型先验做判别/稠密任务**"这一范式做成了可复现、低成本的模板，直接催生了一批后续工作——把同套协议扩展到**表面法线、内在图像分解（albedo/shading/材质）**等更多模态（团队自己的 2025 follow-up *"Marigold: Affordable Adaptation of Diffusion-Based Image Generators for Image Analysis"*, arXiv 2505.09358，发布 normals v1.1、IID-appearance/lighting v1.1 模型），也启发了 GeoWizard、DepthFM、E2E-FT 等"扩散先验做几何"的方向，并被并入 `diffusers` 成为社区标准件。CVPR 2024 Oral + 最佳论文奖候选印证了其范式意义。

**已知局限**（作者自陈）：① 推理慢（生成式多步 + ensemble，相比前馈方法），需靠步数压缩/蒸馏改善（后续 LCM、zero-SNR 1 步已大幅缓解）；② 生成式带来的输出不确定性——相似输入未必产生一致输出，需 ensemble 抑制方差；③ 远景/远处场景处理较弱（DIODE 上 AbsRel 落后）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2312.02145
- arxiv_pdf: https://arxiv.org/pdf/2312.02145
- github: https://github.com/prs-eth/Marigold
- project_page: https://marigoldmonodepth.github.io
- hf_model (depth v1.1): https://huggingface.co/prs-eth/marigold-depth-v1-1
- hf_model (LCM v1.0): https://huggingface.co/prs-eth/marigold-depth-lcm-v1-0
- follow-up paper (2025, image analysis 全模态): https://arxiv.org/abs/2505.09358

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2312.02145.pdf
- ../../../sources/omni/2023/marigold--readme.md
- ../../../sources/omni/2023/marigold--hf-depth-v1-1-card.md
- ../../../sources/omni/2023/marigold--hf-lcm-card.md
