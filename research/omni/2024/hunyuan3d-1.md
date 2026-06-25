---
title: "Hunyuan3D 1.0: A Unified Framework for Text-to-3D and Image-to-3D Generation"
org: Tencent
country: China
date: "2024-11"
type: tech-report
category: 3d
tags: [3d-generation, image-to-3d, text-to-3d, multi-view-diffusion, sparse-view-reconstruction, triplane, sdf, feed-forward]
url: "https://arxiv.org/abs/2411.02293"
arxiv: "https://arxiv.org/abs/2411.02293"
pdf_url: "https://arxiv.org/pdf/2411.02293"
github_url: "https://github.com/Tencent-Hunyuan/Hunyuan3D-1"
hf_url: "https://huggingface.co/Tencent/Hunyuan3D-1"
modelscope_url: ""
project_url: "https://3d.hunyuan.tencent.com"
downloaded: [arxiv-2411.02293.pdf, hunyuan3d-1--readme.md, hunyuan3d-1--hf-modelcard.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Hunyuan3D 1.0 是腾讯混元的统一**文/图 → 3D** 生成框架：把单图 3D 生成拆成「多视图扩散 + 前馈稀疏视图重建」两阶段，最快 **10 秒**（lite，约 25 秒 std）从一张图产出带纹理的显式网格；在 GSO / OmniObject3D 两个公开数据集的 Chamfer Distance 与 F-score 上取得当时前馈方法的 SOTA（GSO 上 std 版 CD=0.175、F-score@0.1=0.735），并接入 [[hunyuan-dit]] 作为文生图前端实现「文/图统一」。是国产开源 3D 生成代表作、后续 Hunyuan3D-2 的基础。

## 背景与定位
当时 3D 生成的两条主流路线各有硬伤：
- **2D 提升 / SDS 优化路线**（[[dreamfusion]]、ProlificDreamer 等）：用 2D 扩散先验做 Score Distillation Sampling 蒸馏出 NeRF，质量与泛化好，但**单个物体优化要 5 分钟到 1 小时**，且存在过饱和、Janus 等问题。
- **前馈大重建模型路线**（LRM、TripoSR、InstantMesh、LGM 等）：秒级出网格，但**对未见物体泛化差**，难以生成薄片状结构，质量受限。

Hunyuan3D 1.0 走的是「**多视图扩散 → 前馈稀疏视图重建**」的解耦路线（与 Instant3D、Wonder3D、Zero123++ 同脉络）：先用 2D 扩散先验生成多视图 RGB，把「单视图重建」松弛为「多视图重建」以缓解泛化难题；再用一个前馈 transformer 重建网络从这些（并不完全一致的）多视图里恢复 3D，避免 SDS 的逐物体优化。论文指出此前少有工作把这两个子任务**组织成一个统一框架**并同时解决二者的痛点——多视图扩散的不一致与慢去噪、稀疏重建只吃带位姿 RGB 的局限。Hunyuan3D 1.0 正是针对这两点做系统性改进。

数据上也点明了 3D 领域的根本瓶颈：最大的 3D 数据集 Objaverse-XL 仅约 1000 万资产，远小于语言/图像/视频规模——因此「借 2D 生成先验」是必由之路。

## 模型架构
整体为**两阶段流水线**，两个模型分开训练。

### 阶段一：多视图扩散模型（Multi-view Diffusion）
- **Backbone**：在大规模 2D 扩散模型上微调。**lite 版用 SD-2.1**，**standard 版用 SD-XL**；std 版参数量约为 lite 及现有同类模型的 **3 倍**。
- **生成方式**：把多视图组织成**网格图一次性生成**（grid），遵循 Zero-1-to-3++ 的做法并把模型换成 3× 更大的版本。
- **固定相机轨道（0 仰角）**：渲染目标视图为**仰角 0°、方位角 {0°,60°,120°,180°,240°,300°}** 的 6 个视图，白底；排成 **3×2 网格**——lite 网格尺寸 960×640，std 为 1536×1024。0 仰角设计是为了**最大化生成视图之间的可见区域重叠**（与 Era3D 的 row-wise attention 同思路）。
- **Reference Attention（参考注意力）**：沿用 Zero-1-to-3++，把条件图过一遍去噪 UNet，将其 self-attention 的 K/V 矩阵附加到对应注意力层，引导生成图与参考图共享语义与纹理。
- **注意力设计**：论文图 2 列出 Row-wise / Full-pixel / Mix-up Attention 三类，配合跨视图信息交互。

### 阶段二：稀疏视图重建模型（Sparse-view Reconstruction, SVRM）
基于 **transformer 的前馈大重建模型**，约 **2 秒**恢复 3D 形状。
- **图像特征编码**：用 **DINO** 编码器提取多视图图像特征。
- **中间表征**：**triplane（三平面）** 隐式 latent。
- **Hybrid Inputs（混合输入，核心创新）**：同时吃**带标定**的生成多视图（相机嵌入在阶段一训练时预定义）与**不带标定**的用户条件图（unposed）。条件图走一条独立的 **view-agnostic 分支**，在注意力里用**全零相机嵌入**作为标记，让模型区分条件图与生成图。因为 0 仰角轨道**看不到顶/底视图**，引入条件图信息可补足不可见区域。
- **Triplane Super-resolution（超分模块）**：初始解码出 **64×64 分辨率、1024 通道**的 triplane，再用一个**线性 unpatchify 层**把每个低分辨率 token 解成 **4×4 个高分辨率 token**，得到 **256×256 分辨率、120 通道**的 triplane。关键 trick：**不在高分辨 triplane 上做 self-attention**，从而保持对输入尺寸的**线性复杂度**（而非二次），在不增加显存/算力的前提下补充细节、缓解 triplane 的混叠（aliasing）问题。
- **3D 表征 = SDF → 显式网格**：用 NeuS 的 **Signed Distance Function** 表示形状，经 **Marching Cube** 转成显式 mesh，再 UV unwrap 出 UV 图，便于纹理映射与艺术家二次编辑。论文明确主张「隐式表征（NeRF/Gaussian Splatting）不是 3D 生成的终点，只有显式表征才能被艺术家直接用」。

### 统一文/图 → 3D
文生 3D 时，前端接 [[hunyuan-dit]]（Hunyuan-DiT，多分辨率扩散 transformer，支持中英双语、细粒度中文理解）先文生图，再走上述 image-to-3D 流水线，从而以同一套后端支持文/图两种条件。

## 数据
- **训练集**：使用**与 Objaverse 类似的内部数据集**（"internal dataset analogous to Objaverse"）。**具体规模、来源构成、配比未披露**。
- **清洗过滤**：过滤掉**复杂场景、缺乏有意义纹理、存在不合理畸变**的 3D 数据；所有物体**缩放归一到单位球**内再渲染。
- **渲染（用 Blender，固定分辨率 1024×1024）**：
  - **条件图渲染（随机化）**：相机仰角从 **[-20°, 60°]** 随机采样，方位角 **[0°, 360°]**；HDR 环境光从一组 HDR 中随机；FOV ~ U(47, 0.01)、相机距离 ~ U(1.5, 0.1)。
  - **目标图渲染（固定）**：渲 **24 张**图，方位角在 {0,15,30,...,345}° 均匀采样、仰角固定 0°；FOV=47.9°、相机距离固定 1.5、统一光照以保证一致性。
- **re-captioning / 合成数据 / 美学与安全过滤**：未披露。

## 训练方法
- **训练目标**：标准扩散去噪（多视图扩散，基于 SD-2.1 / SD-XL 微调）；重建模型用渲染监督（RGB & Normal，论文图 2 标注重建分支输出 RGB 与 Normal）。**未使用 flow matching / SFT / RLHF/DPO 等后训练对齐**（这是一篇 2024 年 11 月的纯重建式 3D 工作）。
- **两阶段分开训练**：
  - **多视图扩散**：RGB 组成 3×2 网格；条件图训练时随机缩放到 [256,512]、推理时固定 512；目标图全部 resize 到 320×320。
  - **稀疏视图重建**：先用 **256×256** 多视图输入训练，再用 **512×512** 多视图输入 **finetune**。
- **Adaptive Classifier-free Guidance（自适应 CFG，核心创新之一）**：观察到「小 CFG 利纹理但出 artifact，大 CFG 利几何但毁纹理；且不同视图最优 CFG 不同——高 CFG 让前视图保留更多条件图细节，却让后视图发暗」。因此对**不同视图、不同时间步**设不同 CFG：
  - 前视图随去噪曲线 `w_t = 2 + 16 * (t/1000)^5`（早期时间步 CFG 高、随去噪推进降低）；
  - 其他视图按视距缩放 `w_{t,v} = w_t * τ_v`，τ_v ∈ [0.5, 1]，τ_front=1、τ_back=0.5。
  - 这一调度比 Consistent123 的 time-adaptive CFG 更进一步，**显式考虑了视图间关系**，避免「把前视图 logo 复制到后视图」等问题。
- **对齐评测的后处理**：因部分基线需手动重标定，未知位姿时用 **ICP（迭代最近点）** 把预测形状与 GT 对齐。
- **蒸馏/加速**：开源计划列了 "Distillation Version" 与 "TensorRT Version"（截至 README 仍未勾选完成）；论文本身**未报告步数蒸馏 / consistency / LCM** 等加速方法。

## Infra（训练 / 推理工程）
- **训练算力 / GPU·时 / 并行策略 / 混合精度 / 吞吐**：**全部未披露**。
- **推理速度（核心卖点）**：
  - 阶段一多视图扩散约 **4 秒**，阶段二前馈重建约 **2 秒**（论文正文一处也写「约 7 秒」恢复 3D），单图 → mesh **最佳约 10 秒**。
  - 端到端：**lite 约 10 秒、std 约 25 秒**（HF model card 注明在 **单卡 NVIDIA A100** 上；均**不含** UV unwrap + 纹理 baking 的约 **15 秒**）。文生 3D 还要叠加前端 Hunyuan-DiT 文生图时间。
- **推理显存（来自 GitHub README）**：
  - Std-pipeline 需 **30GB VRAM**（开 `--save_memory` 降到 24GB）；
  - Lite-pipeline 需 **22GB VRAM**（`--save_memory` 18GB）；
  - 模块分离串行运行可压到 **16G / 14G / 10G**（不同脚本）。
- **部署形态**：开源 inference 代码 + 三个 checkpoint（`lite` / `std` 多视图模型、`svrm` 重建模型）于 HF `Tencent/Hunyuan3D-1`；提供 Gradio app、HF Space Demo、官网 `3d.hunyuan.tencent.com`；可选 xformers / flash_attn 加速；纹理 baking 用 **Dust3R** 做匹配与 warping（Dust3R 为 **CC BY-NC-SA 4.0 非商用**许可，该 baking 模块因此不可商用）。模型许可为 **tencent-hunyuan-community**，且 **EU 区域被禁用**（HF model card `extra_gated_eu_disallowed: true`）。

## 评测 benchmark（把效果讲清楚）
评测在两个公开数据集 **GSO** 与 **OmniObject3D** 各随机抽约 70 个物体，Marching Cubes 提网格后采 10,000 点，算 **Chamfer Distance（CD↓）** 与 **F-score（FS↑，阈值 τ=0.1/0.2/0.5）**。

**GSO（表 1，节选；越低/越高越好）**

| 方法 | CD↓ | FS@0.1↑ | FS@0.2↑ | FS@0.5↑ |
|---|---|---|---|---|
| SyncDreamer | 0.518 | 0.306 | 0.543 | 0.852 |
| TripoSR | 0.356 | 0.511 | 0.727 | 0.920 |
| Wonder3D | 0.573 | 0.277 | 0.489 | 0.809 |
| CRM | 0.262 | 0.538 | 0.800 | 0.977 |
| LGM | 0.409 | 0.442 | 0.658 | 0.881 |
| OpenLRM | 0.214 | 0.605 | 0.840 | 0.997 |
| InstantMesh | 0.216 | 0.670 | 0.862 | 0.977 |
| **Ours-lite** | 0.199 | 0.661 | 0.877 | 0.986 |
| **Ours-std** | **0.175** | **0.735** | **0.910** | 0.987 |

**OmniObject3D（表 2，节选）**

| 方法 | CD↓ | FS@0.1↑ | FS@0.2↑ | FS@0.5↑ |
|---|---|---|---|---|
| TripoSR | 0.157 | 0.776 | 0.915 | 0.999 |
| OpenLRM | 0.158 | 0.754 | 0.940 | 0.992 |
| InstantMesh | 0.187 | 0.678 | 0.897 | 0.990 |
| **Ours-lite** | 0.150 | 0.786 | 0.938 | 0.997 |
| **Ours-std** | **0.136** | **0.814** | **0.948** | 0.998 |

- **结论**：std 版在两个数据集的 CD 与 F-score（尤其 FS@0.1/0.2）上**全面领先**当时所有前馈基线（SyncDreamer / TripoSR / Wonder3D / CRM / LGM / OpenLRM / InstantMesh），取得新 SOTA；lite 版也优于多数基线。
- **User Study**：在 5 个指标上 Hunyuan3D 1.0 获**最高用户偏好**（图 5，雷达图，具体分值未给数值表）。
- **质量 vs 速度**：图 6 的 runtime–F-score 散点显示其位于「速度/质量」最优前沿。

**消融结论：**
- **Adaptive CFG**：固定 CFG 易让后视图出暗影；Consistent123 的 time-adaptive CFG 改善了暗影但忽视视图关系（会把前视图 logo 复制到后视图）。本文按视距动态调 CFG，前/后视图可控性与多样性更平衡，多视图更连贯。
- **Hybrid Inputs**：在 0 仰角轨道下缺顶视图信息，重建出的「大蒜」顶部会被压平；加入条件图（含顶视）信息后能恢复蒜根处的凹陷，显著提升不可见区域的重建准确度。
- **Triplane 超分**：图 3 显示高分辨 triplane（256×256）相比低分辨能捕捉更丰富细节并改善几何。

（注：本文为重建式 3D 工作，**不报告** FID / CLIPScore / GenEval / VBench 等图像/视频生成指标——这些维度对本任务不适用。）

## 创新点与影响
**核心贡献（论文自述四点）：**
1. **统一框架**：单一框架同时支持文条件与图条件 3D 生成（图条件直接走流水线，文条件经 Hunyuan-DiT 文生图）。
2. **0 仰角位姿分布**：固定 6 视图、0 仰角轨道，最大化生成视图间可见区域重叠，利于下游重建。
3. **View-aware / Adaptive CFG**：按视图与时间步动态调 CFG，平衡可控性与多样性。
4. **Hybrid Inputs**：把未标定的条件图作为辅助视图引入稀疏重建，补足生成多视图中看不见的部位。
（外加 triplane 线性超分模块在不增成本下补细节。）

**影响：**
- **速度/质量平衡的国产开源标杆**：10–25 秒出带 UV 的显式网格，且坚持「显式 mesh 才能落地工业管线」的取向，对游戏/影视/电商/机器人等下游友好。
- **后续工作的基础**：直接演进出 **Hunyuan3D 2.0**（2025-01，shape+texture 两阶段、效果大幅提升）与 **Hunyuan3D 2.1**（2025-06，号称首个生产级 3D 资产生成）、乃至 **HunyuanWorld-1.0**（2025-07，沉浸式 3D 世界生成）。是腾讯混元 3D 系列的起点。
- 生态上很快被第三方接入 ComfyUI（多个 wrapper）。

**已知局限：**
- 0 仰角轨道对**顶/底视图信息天然缺失**，需靠 hybrid input 补偿，复杂遮挡/凹陷仍可能受限。
- 多视图扩散仍有**多视图不一致**残留，靠重建网络「学着容忍噪声/不一致」来缓解，而非根除。
- 数据/算力细节几乎全未披露，难以复现训练；baking 依赖非商用 Dust3R；模型许可非完全开放（社区许可 + 禁 EU）。
- 输出受网格面数上限（默认 90000）与固定 6 视图约束。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2411.02293
- arxiv_pdf: https://arxiv.org/pdf/2411.02293
- github: https://github.com/Tencent-Hunyuan/Hunyuan3D-1
- hf_model: https://huggingface.co/Tencent/Hunyuan3D-1
- hf_demo: https://huggingface.co/spaces/Tencent/Hunyuan3D-1
- project: https://3d.hunyuan.tencent.com

## 本地落盘文件
- ../../../sources/omni/2024/arxiv-2411.02293.pdf
- ../../../sources/omni/2024/hunyuan3d-1--readme.md
- ../../../sources/omni/2024/hunyuan3d-1--hf-modelcard.md
