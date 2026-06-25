---
title: "Goku: Flow Based Video Generative Foundation Models"
org: "字节跳动 / 港大 (HKU)"
country: China
date: "2025-02"
type: tech-report
category: video
tags: [video-generation, text-to-image, image-to-video, rectified-flow, dit, joint-image-video, 3d-vae, bytedance]
url: "https://arxiv.org/abs/2502.04896"
arxiv: "https://arxiv.org/abs/2502.04896"
pdf_url: "https://arxiv.org/pdf/2502.04896"
github_url: "https://github.com/Saiyan-World/goku"
hf_url: "https://huggingface.co/datasets/saiyan-world/Goku-MovieGenBench"
modelscope_url: ""
project_url: "https://saiyan-world.github.io/goku/"
downloaded: [arxiv-2502.04896.pdf, goku--paper-text.txt, goku--readme.md, goku--project.html, goku--moviegenbench-dataset.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Goku 是字节跳动 + 港大推出的**图像与视频联合生成基础模型族**（2B / 8B），核心创新是首次把 **rectified flow（修正流）** 形式化用于图文-视频联合生成，配 3D 图像-视频联合 VAU、全注意力 DiT 与工业级数据管线；text-to-video 在 VBench 拿到 **84.85** 总分（论文称 2025-01-25 口径居榜首、超多个商业模型；README 另称 2024-10-07 口径 No.2），text-to-image 在 GenEval **0.76**（带 prompt 改写）/ DPG-Bench **83.65**。

## 背景与定位
解决的是"用一套模型同时高质量生成图像和视频、并打到工业级（商用产品级）质量"的问题。技术脉络上它站在三条线交汇处：
- **扩散→流匹配**：从 [[ddpm]] 的 DDPM 到 [[rectified-flow]]/flow matching（Lipman、Liu 等），Goku 把 RF 从纯图像（如 [[sd3]] 的 MMDiT）推到图文-视频联合域。
- **DiT 路线**：架构基于 [[dit]]（Peebles & Xie 的 class-conditioned diffusion transformer）的扩展 GenTron，沿用 adaLN-Zero 注入时间步。
- **Sora 式 3D 隐空间视频生成**：借鉴 [[sora]] 用 3D VAE 在时空隐空间压缩，与开源 3D-VAE（CogVideoX、Open-Sora-Plan）同代。

相对前置工作的关键改进：（1）用**全注意力（plain full attention）**统一建模图像+视频 token，放弃"时空注意力分离"的省算力但建模次优的折中；（2）**rectified flow 替代 DDPM**，在 ImageNet-1K 概念验证上 40 万步即达到 DDPM 需 100 万步的 FID 水平，收敛显著更快；（3）一条带美学/OCR/运动多级阈值过滤 + MLLM 密集 re-caption 的工业数据管线。

## 模型架构
**Backbone：rectified-flow Transformer（DiT 谱系，扩展自 GenTron）。** 每个 block 含：self-attention（token 间相关）、cross-attention（注入文本条件）、FFN、以及逐层 **adaLN-Zero** 注入时间步。三个尺寸（Table 1）：

| 模型 | 层数 | model dim | FFN dim | 注意力头 |
|---|---|---|---|---|
| Goku-1B | 28 | 1152 | 4608 | 16 |
| Goku-2B | 28 | 1792 | 7168 | 28 |
| Goku-8B | 40 | 3072 | 12288 | 48 |

（1B 仅用于 RF vs DDPM 的概念验证 pilot 实验。）

**关键架构设计：**
- **3D 图像-视频联合 VAE**：把像素空间压到共享隐空间。视频压缩步幅 **8×8×4**（高×宽×时间），图像为 **8×8** 空间压缩——图像被当成 T=1 的特殊视频，从而图文-视频共享同一隐空间表示。原始输入 `x ∈ R^{T×H×W×3}`。
- **Plain Full Attention（全注意力）**：不做时空注意力分离，直接用全注意力建复杂时序运动；为应对长视频 token 数大，用 FlashAttention + sequence parallelism 优化显存与算力。
- **Patch n' Pack（仿 NaViT）**：把不同分辨率/长宽比/时长的图像与视频沿序列维 pack 进同一 minibatch，免去 data bucket。
- **3D RoPE 位置编码**：图像与视频 token 都用 3D RoPE，借其外推能力适配不同分辨率与时长；实测比正弦位置编码在跨训练阶段切换时收敛更快。
- **Q-K Normalization**：对 query/key 做 RMSNorm 再算注意力，抑制大模型训练的 loss spike（否则会出现严重伪影/纯噪声）。
- **Text encoder：Flan-T5**（论文正文 / GenTron 路线为 Flan-T5；T2I benchmark 表中标注 FLAN-T5 XL），通过 cross-attention 注入。

**Image-to-Video（Goku-I2V）**：用 clip 首帧作参考图，把图像 token 广播后与加噪视频 token **沿 channel 维拼接**；新增**单个 MLP 层**做通道对齐，其余结构与 Goku-T2V 完全一致以复用预训练知识。

## 数据
**最终规模：约 160M 图文对 + 36M 视频-文本对**（论文摘要/正文给出 36M video-text、160M image-text）。来源含公开学术集、互联网与合作方私有集。
- **T2I 数据**：100M 公开样本（LAION）用于预训练 + 60M 高质量内部样本用于微调。
- **T2V 数据**：11M 公开 clips（Panda-70M、InternVid、OpenVid-1M、Pexels）+ 25M 内部 clips；公开集也不直接用，全部过自家清洗管线。

**五阶段数据管线**：采集 → 抽帧/切片 → 过滤 → captioning → 分布平衡。
- **基础过滤阈值**（Table 3）：时长 ≥4s；min(H,W) ≥480；码率 ≥500 kbps；帧率 ≥24 FPS（或 23.976 NTSC）。统一转码 H.264。
- **两阶段切片**：先 PySceneDetect 做镜头边界检测得粗 clip；再每秒抽一帧算 DINOv2 特征相邻帧余弦相似度，低于阈值判定镜头切换再细分；clip 上限 10s；同源 clip 间用关键帧 perceptual hash 去重，保留美学分更高者。
- **多级分辨率阈值**（Table 4）：

| Stage | 数量 | 分辨率 | DINO-Sim | 美学分 | OCR 文字占比 | 运动分 |
|---|---|---|---|---|---|---|
| 480p | 36M | ≥480×864 | ≥0.85 | ≥4.3 | ≤0.02 | 0.3–20.0 |
| 720p | 24M | ≥720×1280 | ≥0.90 | ≥4.5 | ≤0.01 | 0.5–15.0 |
| 1080p | 7M | ≥1080×1920 | ≥0.90 | ≥4.5 | ≤0.01 | 0.5–8.0 |

- **美学过滤**：LAION aesthetic 模型对关键帧打分取均值，按分辨率分档丢弃低分。
- **OCR 过滤**：内部 OCR 模型算最大文字框面积占比，超阈值丢弃（剔除字幕/广告板过多的视频）。
- **运动过滤**：RAFT 算光流均值得运动分，过低（静态）/过高（剧烈）都剔除；**运动分还被写进 caption** 以便推理时用 prompt 控运动幅度。
- **Captioning（re-captioning 一等公民）**：图像用 InternVL2.0 生成密集 caption；视频先 InternVL2.0 出关键帧 caption，再 **Tarsier2** 出整段视频 caption（Tarsier2 能直接描述镜头运动如 zoom in/pan right，省掉单独的运镜预测模型），最后 **Qwen2** 合并关键帧与视频 caption。
- **数据平衡**：内部视频分类模型按 4 帧给语义标签，分 **9 大类 + 86 子类**（human/scenery/animals/food/urban life 为主）；对建模更难的 human 类加权，过采样欠表示子类、下采样过表示子类，欠表示者还用合成数据补。

## 训练方法
**训练目标：rectified flow（修正流 / velocity prediction）。** 前向是噪声 x0~N(0,1) 与真值 x1 的**线性插值** `x_t = t·x1 + (1−t)·x0`，模型预测速度 `v_t = dx_t/dt`。RF 相比 DDPM 收敛更快——**ImageNet-1K 256×256 概念验证**（Goku-1B）：RF 在 400k 步 FID-50K=2.157，DDPM 需 1000k 步才到 2.257 的同档水平（Table 2）。

**三阶段训练（multi-stage）：**
- **Stage-1 文本-语义对齐**：纯 text-to-image 预训练，先建立文本→视觉语义的基础对齐（物体属性/空间布局/上下文一致）。
- **Stage-2 图文-视频联合学习**：在统一全注意力框架下把图像与视频 pack 进同一 token 序列联合训练，用高质量图像的丰富信息提升视频帧质量（弥补高质量视频数据更稀缺的问题）。消融证明：从同一 T2I 权重出发，加联合训练的 T2V 帧明显更逼真，不加则帧质量低。
- **Stage-3 模态专属微调**：分别为 T2I（更出彩的画面）和 T2V（时序平滑、运动连续、稳定）做收尾微调。

**级联分辨率训练（cascaded resolution）**：Stage-2 内先在低分辨率 288×512 学核心"文本-语义-运动"关系（省算力），再渐进升到 480×864 → 720×1280。

**Image-to-Video 微调**：从 T2V 初始化，用约 **4.5M 文-图-视频三元组**微调，仅 **10k 步**即获得不错的图像动画化能力。

**蒸馏/步数加速**：论文未报告 consistency/LCM/ADD 等步数蒸馏；推理加速细节未披露。

## Infra（训练 / 推理工程）
**3D 并行**（序列 × 数据 × 模型）应对最长 **>220K tokens** 的超长序列：
- **Sequence Parallelism**：采用 **Ulysses**（DeepSpeed-Ulysses），从训练循环起即按序列维 shard，注意力阶段用 all-to-all 分发 Q/K/V，每 worker 处理全序列但只算部分注意力头，算完再 all-to-all 聚合。
- **FSDP（HYBRID_SHARD）**：shard 组内 FULL_SHARD、组间参数复制（等效 DP），用 all-gather 取参数、reduce-scatter 收梯度并与前后向重叠以省通信。
- **细粒度 Activation Checkpointing**：选择性激活检查点，最小化需存激活的层数、最大化 GPU 利用率，平衡计算/通信重叠。
- **容错（MegaScale）**：self-check 诊断、多级监控、快速重启/恢复，应对大集群高故障率。
- **ByteCheckpoint**：并行存取分片 checkpoint，支持 reshard（不同训练规模/rank 数/存储后端间无缝切换）；**8B 模型跨数千 GPU 存 checkpoint 阻塞训练 <4 秒**。

**算力规模**：论文称跨"**数千 GPU（thousands of GPUs）**"训练，但**未披露**具体 GPU 型号、卡数、GPU·时、吞吐与功耗。**推理加速/部署形态未披露。**

## 评测 benchmark
**Text-to-Image（Table 5，† = 带 prompt rewriting）：**
- **GenEval Overall**：Goku-T2I(2B) **0.70**（原始短 prompt）/ **0.76†**（改写 prompt）。对比 SD3 0.74、DALL-E 3 0.67†、EMU3 0.66、SDXL 0.55。
- **T2I-CompBench**（color/shape/texture）：0.7521/0.4832/0.6691（原始）→ 0.7561†/0.5759†/0.7071†。
- **DPG-Bench**：**83.65**，超 PixArt-α(71.11)、DALL-E 3(83.50)、EMU3(80.60)。
- 评测规模：GenEval 553 prompts/2212 图；DPG-Bench 1065 prompts/4260 图；T2I-CompBench 每属性 300 prompts×10 图。

**Text-to-Video — VBench（Table 7，总分对比）：**
- **Goku-T2V 总分 84.85**（Quality 85.60 / Semantic 81.87）。同表对比：CausVid 84.27、Luma 83.61、HunyuanVideo 83.24、Kling 81.85、CogVideoX-5B 81.61、Gen-3 82.32、Pika-1.0 80.69。
- 强项维度：Human Action 97.60、Dynamic Degree 57.08、Multiple Objects 76.11、Appearance Style 79.48、Quality Score 85.60。
- 排行榜口径有两个不同快照：README 称发布时（2024-10-07 口径）VBench No.2；论文（line 124）称"securing the top position on the leaderboard (as of 2025-01-25)"即 2025-01-25 居榜首，超多个领先商业模型。

**Text-to-Video — UCF-101 零样本（Table 6，FVD↓ / IS↑）：** 用 Tarsier-34B 为 UCF-101 生成详细 caption，再用 Goku-2B 生 13,320 视频，I3D(Kinetics-400) 提特征算 FVD。
- 128×128：**FVD 217.24**，IS 42.30（SOTA）；256×256：FVD 246.17，IS 45.77；240×360：FVD 254.47，IS 46.64。对比 SVD(240×360) 242.02、PixelDance 242.82、Emu-Video 317.10。

**Image-to-Video**：仅 10k 步微调即能动画化参考图并保持文本对齐与时序一致（无独立量化表，定性为主）。

**定性 / 消融**：
- **定性同 prompt 对比**：论文 Figure 6 用同一 prompt 把 Goku-T2V(8B) 与 CogVideoX1.5(5B)、Open-Sora-Plan(v1.3)、Pika、DreamMachine、Vidu、Kling(1.5) 并排比较（论文给的是单条珊瑚礁 drone prompt）。项目页另有 **MovieGenBench** demo 区，明确"用 Meta Movie Gen 的原始 prompt 集、不做任何修改"（全集发布为 HF 数据集 `saiyan-world/Goku-MovieGenBench`），但该区只放 Goku 自家生成视频、非并排对比。
- **模型缩放消融**：8B 比 2B 更少出现结构扭曲（手臂、车轮等）。
- **联合训练消融**：加图文-视频联合训练显著提升视频帧逼真度。
- T2V 可视化默认 4 秒 / 24 FPS / 720p。

> 注：论文**未报告** CLIPScore、MJHQ-30K、HPSv2、ImageReward、PickScore、人评 ELO/Arena 等指标，也未做 RLHF/DPO 偏好对齐（本工作无偏好对齐阶段）。

## 创新点与影响
**核心贡献：**
1. 首次将 **rectified flow** 系统性用于**图文-视频联合生成**基础模型，并以 1B 概念验证证明其相对 DDPM 的收敛优势。
2. **3D 图像-视频联合 VAE + 全注意力 DiT + Patch n' Pack + 3D RoPE** 的统一框架，把图像当 T=1 视频，实现跨模态共享隐空间与联合训练；用高质量图像数据反哺视频帧质量。
3. 工业级**数据管线**：多级分辨率阈值过滤（DINO/美学/OCR/运动）+ MLLM 链式 re-captioning（InternVL2.0 → Tarsier2 → Qwen2）+ 9 类/86 子类语义平衡；运动分写入 caption 实现运动可控。
4. 大规模**训练基建**：Ulysses 序列并行 + HYBRID_SHARD FSDP + 选择性 AC + MegaScale 容错 + ByteCheckpoint（8B 跨数千 GPU checkpoint <4s），支撑 >220K token 超长序列。

**影响**：字节系工业级视频生成基础模型，与 HunyuanVideo、CogVideoX、Open-Sora 同处 2024–2025 中文厂商视频生成研发潮，强化了"rectified flow + 全注意力 DiT + 图文-视频联合"的主流配方。**开放程度（按落盘源核对）**：GitHub `Saiyan-World/goku` 与 HF `saiyan-world/Goku-MovieGenBench` 存在；但已落盘的 README 只含论文摘要 + VBench 对比表 + BibTeX，**未提及发布代码/权重/推理脚本**，HF 链接也只是 **MovieGenBench 评测 prompt/视频数据集**而非模型权重——因此"开源代码/权重"在已落盘一手源中**无法证实**，仅数据集与项目页可确认开放。

**已知局限**：未做偏好对齐（RLHF/DPO）；推理步数/蒸馏/部署与具体算力规模未披露；评测以 VBench/UCF-101/GenEval/DPG 为主，缺人评 Arena 与编辑类基准；I2V 仅定性，无量化对比。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2502.04896
- arxiv_pdf: https://arxiv.org/pdf/2502.04896
- project_page: https://saiyan-world.github.io/goku/
- github: https://github.com/Saiyan-World/goku
- hf_dataset (MovieGenBench): https://huggingface.co/datasets/saiyan-world/Goku-MovieGenBench

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2502.04896.pdf （PDF，gitignore 不入 git，本地已落盘并精读）
- ../../../sources/omni/2025/goku--paper-text.txt （PDF 全文文本提取）
- ../../../sources/omni/2025/goku--readme.md （GitHub README）
- ../../../sources/omni/2025/goku--project.html （项目页快照）
- ../../../sources/omni/2025/goku--moviegenbench-dataset.md （HF 数据集卡）
