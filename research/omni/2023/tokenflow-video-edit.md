---
title: "TokenFlow: Consistent Diffusion Features for Consistent Video Editing"
org: "Weizmann Institute of Science"
country: EU
date: "2023-07"
type: paper
category: video
tags: [video-editing, diffusion-features, zero-shot, training-free, temporal-consistency, stable-diffusion, plug-and-play, iclr2024]
url: "https://arxiv.org/abs/2307.10373"
arxiv: "https://arxiv.org/abs/2307.10373"
pdf_url: "https://arxiv.org/pdf/2307.10373"
github_url: "https://github.com/omerbt/TokenFlow"
hf_url: "https://huggingface.co/spaces/weizmannscience/tokenflow"
modelscope_url: ""
project_url: "https://diffusion-tokenflow.github.io/"
downloaded: [arxiv-2307.10373.pdf, tokenflow-video-edit--project.md, tokenflow-video-edit--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
TokenFlow 是一个**无需训练 / 微调**的文本驱动视频编辑框架，核心创新是发现"RGB 空间的时间一致性与扩散模型内部特征空间的一致性高度相关"，于是在去噪过程中**显式地按原视频帧间对应关系传播被编辑的扩散特征（self-attention tokens）**，使编辑后视频在保持原始布局与运动的前提下实现细粒度时间一致；在 61 个文本-视频对上 warp-error 仅 3.0×10⁻³，user study 对各基线时间一致性偏好率 70–94%，是 zero-shot video editing 的代表作（ICLR 2024）。

## 背景与定位
2023 年文生图扩散模型（[[stable-diffusion-1]] / [[latent-diffusion-ldm]]）已能高质量编辑图像，但视频生成/编辑仍落后：原生文生视频模型（Gen-1、Imagen Video、Align-your-Latents）受限于分辨率、长度与可控性。把图像扩散模型**逐帧**套用做视频编辑的最大难题是**时间一致性**——理想情况下 3D 世界中每个物理点在不同帧应被一致地修改。

此前与同期工作主要靠**扩展 self-attention 到多帧（self-attention inflation）**来获得全局外观一致（Tune-A-Video、Text2Video-Zero、FateZero、Pix2Video、Video-P2P）。论文指出这只能"隐式"约束运动，不足以达到细粒度时间一致，会产生 jitter（抖动）。另一类基于光流/图集（NLA、Text2LIVE、Rerender-A-Video）的方法：图集训练慢（NLA 约 10 小时）且只适用简单运动；光流在远距离帧上估计不可靠，导致关键帧编辑不一致。

TokenFlow 的定位：不依赖光流、不训练图集、不微调模型，而是**直接利用扩散模型内部已经"免费"提供的帧间特征对应关系**来传播编辑，把图像编辑技术（PnP、SDEdit、ControlNet 等）即插即用地升级为时间一致的视频编辑。它属于"通过操纵扩散特征实现可控生成"这一脉络（PnP-Diffusion、Prompt-to-Prompt、MasaCtrl、Diffusion Hyperfeatures）的视频化延伸。

## 模型架构
TokenFlow **本身不是一个新网络，而是一套在固定预训练模型上推理时操纵特征的算法**。

- **Backbone**：直接用冻结的 [[stable-diffusion-1]] **v2.1** 官方 HuggingFace checkpoint（U-Net 架构：residual + self-attention + cross-attention 块），在 LDM 隐空间操作。无任何参数被训练或微调。
- **被操纵的"token"**：指 U-Net 各层 **self-attention 模块的输出特征**（output tokens）。论文的关键经验观察是：
  - 自然视频经 DDIM 逆向后，从**最高分辨率解码层**抽取的 self-attention 特征在时间上高度一致（PCA 可视化中对应区域跨帧编码相似，见 Fig.3）；
  - 这些特征提供**细粒度帧间对应**——用最近邻搜索（cosine 距离）即可在源帧与邻帧特征间建立对应，且特征是**可互换的**：把目标帧特征替换为源帧对应特征即可忠实重建目标帧（Fig.2）。
- **两个核心模块**（每个去噪步交替执行，作用于**所有层的所有 self-attention 块**）：
  1. **关键帧联合编辑（Extended/Joint Attention）**：每步随机采样一组关键帧，把 self-attention 扩展为跨关键帧联合注意（拼接所有关键帧的 K、V，每个关键帧 query 所有关键帧），让它们共享全局外观，得到一组编辑后 token 集合 `T_base`。
  2. **TokenFlow 传播（特征传播）**：对每帧，预先用原视频特征计算它与前/后最近关键帧的 NN field γ⁺/γ⁻，再把 `T_base` 中对应位置的 token 按距离加权线性组合（权重 wᵢ = σ(d⁻/(d⁺+d⁻))，sigmoid 平滑过渡）传播过去，**替换该帧本应生成的 token**。注意：因每个 self-attention 块有残差连接，必须在**每一层**都做传播。
- **文本编码 / 条件注入**：沿用 SD 自带的 CLIP text encoder 与 cross-attention；编辑信号来自所搭配的图像编辑技术（论文主结果用 **PnP-Diffusion**，README 还支持 **ControlNet、SDEdit**）。
- **分辨率**：处理 384×672 或 512×512 像素视频，40–200 帧。

## 数据
**本工作无训练，故没有训练数据集**。"数据"仅指评测素材：

- 评测集来自 **DAVIS** 视频（Pont-Tuset et al. 2017）+ 互联网视频（动物、食物、人物、各类运动物体），共 **61 个文本-视频对**。
- 每个视频配多种目标 prompt（如"A Van Gogh portrait""A robotic wolf""Ice sculpture of a car"）以获得多样编辑。
- 视频规格：分辨率 384×672 或 512×512，长度 40–200 帧。
- 无数据清洗/配比/re-captioning/合成数据等概念（不适用）。预训练数据即 SD v2.1 所用数据（LAION 系，论文未展开）。

## 训练方法
**完全 training-free / zero-shot，没有任何训练、微调、蒸馏或偏好对齐**。这正是其相对 Tune-A-Video（需对每个测试视频微调）、NLA/Text2LIVE（需 ~10 小时 test-time training）的核心优势。

推理时的"流程算法"（Algorithm 1）：

1. **预处理 / DDIM 逆向**：对每帧做 DDIM 确定性逆向以抽 token；逆向用 **1000 forward steps + classifier-free guidance scale = 1**（follow PnP / FateZero，是运行时主瓶颈），得到各帧噪声 latent 序列与各层 self-attention token，并据此建立帧间 NN 对应。（注：随后的去噪采样统一用 **50 DDIM steps**——Appendix A 明确"所有实验 DDIM 确定性采样 50 步"，1000 步仅用于逆向。）
2. **去噪采样**（t = T…1，每步）：
   - 随机采样 k(<n) 个关键帧索引（固定帧间隔 = 8）；
   - 用图像编辑技术 ε̂θ（如 PnP）+ extended-attention 联合编辑关键帧，抽取 `T_base`；
   - 对全部帧执行 TokenFlow 传播（Eq.5），用传播得到的 token 替换每层 self-attention 输出，再喂回网络去噪一步。
   - 采样时 classifier-free guidance scale = 7.5。
- **生成目标**：沿用底层扩散模型的标准 DDPM/DDIM 去噪目标，本身不引入新 loss；"一致性"靠特征传播这一推理算子强制，而非训练。
- **关键 trick**：①**每步随机化关键帧**（而非固定均匀关键帧）——避免把视频人为切成关键帧间的短片段，提升对困难帧的鲁棒性（每帧由多帧共同贡献生成）；②交替"关键帧编辑↔传播"形成正反馈——每步特征更一致，下一步采样的关键帧编辑也更一致。

## Infra（训练 / 推理工程）
- **算力**：无训练开销，无需大规模 GPU 集群。论文未明示单卡型号；致谢提到 NVIDIA Applied Research Accelerator Program（推断在单张 NVIDIA GPU 上运行）。实现基于 **PyTorch ≥ 1.10**（README）。
- **推理运行时（Table 3，40 帧视频，均用 50 steps）**：
  - TokenFlow 总计 **237 s**（预处理 50 s + 采样 187 s）；
  - 对比：PnP 逐帧 208 s、Text2Video-Zero 198 s、Rerender-A-Video 285 s、FateZero 349 s、**Tune-A-Video 2684 s**（因需微调，慢一个数量级）。
- **效率来源**：因为只在**关键帧**上计算 self-attention 输出（其余帧的 token 由传播得到），采样时间比逐帧 PnP 反而**降低约 20%**。
- **瓶颈**：1000-step 的 DDIM 逆向是主要耗时来源；论文指出很多情况下用更少步数（如 50）即可，存在加速空间。
- **部署形态**：开源 PyTorch 代码（preprocess.py 做逆向 + run_tokenflow_{pnp,controlnet,SDEdit}.py 做编辑，YAML 配置）；提供 **HuggingFace Spaces demo**（weizmannscience/tokenflow）。

## 评测 benchmark（把效果讲清楚）
评测两维度：**编辑保真度**（CLIP：编辑帧与目标 prompt 的 CLIP 嵌入相似度）与**时间一致性**（warp-error：用 RAFT 光流把编辑帧按原视频运动 warp 后的误差；+ AMT 2AFC 用户研究，每基线 2000–3000 次判断）。

**Table 1（主结果，warp-err ×10⁻³ / 用户更偏好 TokenFlow 的比例 / CLIP↑）：**

| 方法 | Warp-err↓ | 用户偏好 TokenFlow | CLIP↑ |
|---|---|---|---|
| LDM recon.（仅过自编码，参考上界） | 2.0 | — | 0.23 |
| PnP-Diffusion（逐帧） | 11.3 | 94% | 0.33 |
| Text2Video-Zero | 12.5 | 78% | 0.33 |
| Tune-A-Video | 30.0 | 82% | 0.31 |
| FateZero | 6.9 | 71% | 0.32 |
| Gen-1 | — | 70% | 0.32 |
| Rerender-A-Video | 1.8 | 71% | 0.32 |
| Ours w/ joint attention（消融） | 5.9 | 90% | 0.33 |
| Ours w/o random keyframes（消融） | 3.7 | — | 0.33 |
| **Ours（TokenFlow）** | **3.0** | — | **0.33** |

要点：
- **CLIP 0.33 并列最高**，说明编辑结果忠实贴合 prompt。
- **warp-error 3.0**：除 Rerender-A-Video（1.8，但它**直接优化 warp-error 且依赖光流**，会在远帧产生肉眼可见的长程不一致/伪影，未被 warp-error 反映）外最低。论文强调：用户研究中各基线被压倒性偏好 TokenFlow（即便 Rerender 的 warp-err 更低，用户仍 71% 选 TokenFlow）。
- Gen-1 因其商用平台输出帧数/帧率与输入不一致，**无法计算 warp-error**（如实标注）。

**Table 2（视频重建质量，去掉关键帧编辑、仅跑传播管线做重建）：**

| 方法 | PSNR↑ | LPIPS↓ |
|---|---|---|
| LDM recon. | 31.13 | 0.03 |
| DDIM inversion | 25.32 | 0.14 |
| **Ours（TokenFlow recon.）** | **25.74** | **0.13** |

TokenFlow 重建**略优于 vanilla DDIM 逆向**，证明其特征表示鲁棒——得益于关键帧随机化（每帧由多帧重建，对困难帧更稳）。

**消融结论**（Table 1 下半）：
- 去掉 TokenFlow 传播、改用纯 extended-attention（"w/ joint attention"）→ warp-err 从 3.0 升到 5.9，证明**仅靠 self-attention inflation 不足以达到细粒度时间一致**（这是对前序方法路线的直接反驳）。
- 固定关键帧（"w/o random keyframes"）→ warp-err 升到 3.7，证明**关键帧随机化**对一致性有贡献。

**对比基线**：Tune-A-Video、PnP（逐帧）、Gen-1、Text2Video-Zero、FateZero、Rerender-A-Video、Text2LIVE、单关键帧+Jamriška 传播。定性上 TokenFlow 同时满足"贴合 prompt"与"时间一致"，而其它方法多在两者间二选一（逐帧 PnP 编辑精美但完全无时间一致；Text2Video-Zero/FateZero 严重抖动；Gen-1 帧质量明显差于文生图模型且仍有不一致）。

## 创新点与影响
**核心贡献：**
1. **关键经验发现**：自然视频的时间一致性程度与其在扩散模型 self-attention 特征空间中的一致性程度**紧密相关**；且原视频特征提供可直接用最近邻获取的、可互换的细粒度帧间对应。这是对扩散特征性质的新颖实证分析。
2. **TokenFlow 算子**：在去噪过程中按原视频对应关系**显式传播编辑后的 self-attention token**，把"时间一致"从隐式（靠 attention inflation）变为显式约束。
3. **完全 training-free、即插即用**：可与任意现成扩散图像编辑技术（PnP / SDEdit / ControlNet）组合，无需光流、无需图集训练、无需对视频微调，在多样真实视频上取得 SOTA 编辑一致性。

**影响**：作为 2023 年 zero-shot / training-free 视频编辑的代表作（ICLR 2024 收录），TokenFlow 把"操纵扩散内部特征实现可控生成"从图像推广到视频，论证了 self-attention inflation 路线的不足，启发了后续大量"利用图像模型先验做视频任务"与一致性视频编辑的研究；其"特征对应即免费监督"的思路也影响了 diffusion correspondence/feature 方向。开源代码 + HF Demo 使其易复现、被广泛作为基线。

**已知局限**（论文 Discussion / Fig.7）：
- **只能保运动、不能改结构**：方法按原视频特征对应传播，无法处理需要结构形变的编辑（如把物体变成形状差异很大的另一物体，Fig.7 "A tractor"失败）。
- **强依赖底层图像编辑技术保结构**：若底层技术（如 PnP 因 DDIM 逆向不准）未能保住每帧结构，TokenFlow 会强制无意义的对应，产生伪影。
- **LDM 解码器引入高频闪烁（flicker）**：源自 LDM 自编码器；论文建议换更好的解码器或用现成 deflickering 后处理缓解。
- 逆向 1000 步是运行时瓶颈。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2307.10373
- arxiv_pdf: https://arxiv.org/pdf/2307.10373
- project_page: https://diffusion-tokenflow.github.io/
- github: https://github.com/omerbt/TokenFlow
- hf_demo: https://huggingface.co/spaces/weizmannscience/tokenflow

## 一手源存档（sources/）
- [arxiv-2307.10373.pdf](https://arxiv.org/pdf/2307.10373)  （arXiv 原文 PDF，不入 git）
- [project.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/tokenflow-video-edit--project.md)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/tokenflow-video-edit--readme.md)
