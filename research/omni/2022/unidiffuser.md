---
title: "UniDiffuser: One Transformer Fits All Distributions in Multi-Modal Diffusion"
org: "Tsinghua (TSAIL) / RUC / ShengShu / BAAI"
country: China
date: "2022-12"
type: paper
category: unified
tags: [unified, multimodal, diffusion, transformer, u-vit, t2i, i2t, joint-generation, latent-diffusion]
url: "https://arxiv.org/abs/2303.06555"
arxiv: "https://arxiv.org/abs/2303.06555"
pdf_url: "https://arxiv.org/pdf/2303.06555"
github_url: "https://github.com/thu-ml/unidiffuser"
hf_url: "https://huggingface.co/thu-ml/unidiffuser-v1"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2303.06555.pdf, unidiffuser--readme.md, unidiffuser--hf-v1-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
UniDiffuser 用**一个**扩散 Transformer（U-ViT，约 0.95B 参数）同时拟合图—文两模态的**所有**边缘 / 条件 / 联合分布，靠"给不同模态喂不同 timestep"这一极简改动，把 t2i、i2t、图文联合生成、无条件生成统一进单一网络与单一训练损失；在 MS-COCO zero-shot FID 上达到 9.71，优于 DALL·E 2（10.39）、与 Stable Diffusion（8.59）同档。

## 背景与定位
当时的多模态生成模型几乎都是"专才"（bespoke）：[[stable-diffusion-1]] / [[dall-e-2]] / Imagen 只做 t2i，captioning 模型只做 i2t，各自训练一个网络。要让一个模型同时覆盖全部任务，经典思路是**先学联合分布 q(x,y) 再用 MCMC 等额外采样推边缘 / 条件分布**——在 LAION 规模上不可行。

UniDiffuser 的核心洞见是把"学不同分布"统一成**同一件事——预测被加噪数据中的噪声，只是不同模态的加噪程度（timestep）可以不同**：
- 给某模态喂最大 timestep T ⇒ 等价于把它边缘化（无条件生成另一模态）；
- 给某模态喂 timestep 0（干净数据作条件）⇒ 等价于条件生成 q(x|y)；
- 两模态喂相同 t ⇒ 联合生成 q(x,y)。

因此训练时只要"对所有模态都加噪、各自独立采 timestep、预测所有模态的噪声"，推理时按需设置 timestep 即可退化成任意专才扩散模型。技术上它站在 [[ddpm]] 的噪声预测框架、[[latent-diffusion-ldm]] 的隐空间训练、[[classifier-free-guidance]] 之上，backbone 用同组作者的 U-ViT（All are Worth Words, CVPR'23）。最直接的竞品是 Versatile Diffusion（VD），后者用多流架构 + 传统多任务训练（多次前向、需手调各层梯度乘子），UniDiffuser 用统一视角把它简化为单损失、单次前向反向。

## 模型架构
两阶段隐空间方案（沿用 LDM 思路），先把图文编码进连续隐空间，再在隐空间上训扩散 Transformer。

**各模态编码 / 解码器（冻结 / 轻量微调）：** 作者强调编解码器训练成本低——训练图像编/解码器所需的数据量「不到 UniDiffuser 本身的 1%」（论文原文，指数据规模而非算力占比），故可在小代价下为每种模态获得高质量编解码器。
- **图像编码器 = 两部分拼接**：① Stable Diffusion 的 KL 图像 autoencoder 编码器 E_AE，得重建用 latent `x_AE`；② 图像 CLIP（ViT-B/32）抽 512 维语义 embedding `x_CLIP`。最终图像 latent `x0 = [x_AE, x_CLIP]`。作者经验：`x_AE` 足以经 SD 解码器 D_AE 重建图像，而额外的 `x_CLIP` 帮助 i2t 时理解图像语义（两者分工源自"重建 vs 与文本对齐"两种原始训练目标）。
- **文本编码器** = 与 SD 同款 text CLIP（ViT-L），输出 77×768；再加一层 linear 把每个向量降到 64 维得到文本 latent `y0`。
- **文本解码器** = 微调的 **GPT-2（124M）**，把 `y0` 当作 prefix embedding（ClipCap 式），自回归重建文本。冻结 CLIP、只训 linear + GPT-2。MS-COCO（Karpathy split）重建质量 BLEU-1 0.969 / BLEU-4 0.894。

**联合噪声预测网络 = U-ViT**：把两模态数据 token 与两个 timestep 都当作 token 输入，浅层↔深层用 long skip connection。相对原版 U-ViT 的关键改动：把 pre-LN 换成 **post-LN**，并在拼接 long skip connection 后再加一层 LayerNorm——因为 pre-LN 在混合精度下易 overflow，post-LN 稳定了训练。

**U-ViT 配置（附录 Table 3）**：patch size 2 / 31 层 / hidden 1536 / MLP 6144 / 24 heads / **952M 参数**（README 称约 1B，可在 ≥10GB 显存 GPU 上推理）。图像 latent 的位置编码在 256×256 阶段用双线性插值适配。

**两个发布版本（README / HF card）**：
- **UniDiffuser-v0**：纯在 LAION-5B（含噪 webdata）上训，512×512。
- **UniDiffuser-v1**：从 v0 续训，额外用一批**更干净的内部图文对**；训练时用一个 data-type flag（0=webdata / 1=internal）区分两类数据，推理可选 flag。官方推荐用 v1。

## 数据
- **来源 = LAION-5B 的三个子集**（沿用 Stable Diffusion 的用法）：
  - `laion2B-en`：约 2B 英文图文对（GPT-2 文本解码器在此训，README/论文一处写约 2.3B 图文对）；
  - `laion-high-resolution`：约 170M，图像分辨率 ≥1024、多语言 caption；
  - `laion-aesthetics v2 5+`：laion2B-en 的子集，约 600M 高视觉质量图文对。
- **过滤 / 清洗**：沿 Stable Diffusion，进一步把 laion-aesthetics v2 5+ 过滤到分辨率 ≥512、估计水印概率 <0.5，留下约 **193M** 对；图像值从 [0,255] 归一化到 [−1,1]。
- **文本清洗**：LAION 文本噪声大，去除 URL / HTML 标签 / email / 括号内容 / 引号（保留 's）/ 除 `, . ? !` 外的符号；再用 CLIP 自带 byte-level BPE tokenizer。
- **latent 统计**：图文 latent 数值范围都在 [−2,2] 内、近似正态（图像 mean 0.0269 / std 0.7919，文本 mean 0.0127 / std 0.5957），范围相近故未额外归一化。
- **合成数据 / re-captioning**：论文未提及（全程为 LAION 真实图文对 + 文本清洗，未涉及合成或重述 caption）；v1 额外用的"内部数据"性质未详细披露。

## 训练方法
- **训练目标 = 标准 DDPM 噪声预测的联合版**：对 (x0,y0) 各自独立采 timestep (tx,ty)、各自加噪得 (x_tx, y_ty)，让网络 `ε_θ(x_tx, y_ty, tx, ty)` 回归两模态噪声 `[ε_x, ε_y]` 的 L2 损失（论文 Eq.5；训练算法 Algorithm 1）。损失和原始 DDPM 一样简单，单次参数更新只需**一次前向反向**即覆盖所有任务/分布；虽因两个独立 timestep 导致梯度估计方差略高，但未观察到收敛变慢。
- **免费的 Classifier-Free Guidance**：因为同一网络已经同时建模了条件模型（喂干净条件，ty=0）和无条件模型（喂纯噪声条件，ty=T），CFG 无需训练时引入 null token，可直接在条件与**联合**采样上施加（联合采样把联合 score 拆成两个条件 score 各自做 CFG）。实测最佳 guidance scale 在文本→图像约 3、在 v1 采样脚本默认 7、HF/diffusers 示例用 ~8、CFG 效果图里用约 6。
- **多阶段训练**（沿 Stable Diffusion）：
  1. 256×256，laion2B-en，250K steps，batch 11264，5K warmup；
  2. 512×512，laion-high-resolution，微调 200K steps，batch 2112，5K warmup；
  3. 从阶段 2 末（含 optimizer 状态）resume，512×512，laion-aesthetics v2 5+，220K steps，batch 2112。
- **优化器超参**（沿 U-ViT）：AdamW，lr 2e-4，weight decay 0.03，(β1,β2)=(0.9,0.9)；验证 loss 不再下降时把 lr 降 10 倍续训；全程混合精度。
- **GPT-2 文本解码器训练**：AdamW lr 2e-5，5K warmup，batch 768，235K steps，`y0` 维度 64；生成用 beam search（beam 5，max len 67）。
- **蒸馏 / 步数加速**：未引入专门蒸馏；推理统一用 DPM-Solver 50 步（见下）。

## Infra（训练 / 推理工程）
- **算力**：约 **88 张 A100（80GB）训练约 28 天**（即 ~2464 GPU·天 / ~5.9 万 A100·小时量级，未给精确 GPU·小时）。
- **混合精度**：全程 mixed precision；post-LN 改动正是为解决混合精度下 pre-LN overflow。
- **并行 / 吞吐 / 分布式细节**：未披露（仅给 batch size 与卡数）。
- **推理**：统一用 [[dpm-solver]] **50 步**（v1 脚本默认；diffusers 示例 20 步亦可）；attention 强烈建议装 xformers 加速（训练与推理皆受益）。约 0.95B 的 U-ViT 可在 **≥10GB 显存**单卡上推理；diffusers 提供 `UniDiffuserPipeline`（六种模式 t2i/i2t/joint/i/t/变体），支持 fp16。
- **量化 / 缓存**：未报告。

## 评测 benchmark（把效果讲清楚）
**Zero-shot FID on MS-COCO（论文 Table 1，CFG scale=3）**：

| 模型 | 类型 | FID ↓ |
|---|---|---|
| GLIDE | 专才 | 12.24 |
| Make-A-Scene | 专才 | 11.84 |
| **DALL·E 2** | 专才 | 10.39 |
| Versatile Diffusion† | 通用 | 10.09 |
| **UniDiffuser (ours)** | 通用 | **9.71** |
| Stable Diffusion† | 专才 | 8.59 |
| Imagen | 专才 | 7.27 |
| Parti | 专才 | 7.23 |

（† = 作者用官方实现复现）结论：UniDiffuser 作为**通用**模型，t2i 上 FID 9.71 优于 DALL·E 2、优于直接竞品 VD（10.09），与专才 Stable Diffusion（8.59）同档，但仍逊于 Imagen / Parti。FID 用 MS-COCO 验证集随机 10K prompt 算，CLIP score 用 30K（t2i）/ 随机 10K 图（i2t）算。

**与 Versatile Diffusion 直接对比**（最核心的"通用 vs 通用"对照）：
- 文本→图像：在**所有** CFG scale 下，UniDiffuser 的 CLIP score↑ 与 FID↓ 都一致优于 VD（论文 Fig.5）；定性上 UniDiffuser 对代表性 prompt 语义对齐更好而 VD 失败（Fig.7）。
- 图像→文本：相同 CFG scale 下 UniDiffuser 的 CLIP score 一致高于 VD（Fig.6）。
- 作者据此论证：UniDiffuser 的"time-condition"统一策略在统计上比 VD 的多任务策略更高效。

**关键消融 / 结论**：
- CFG "免费"可用并显著提升联合与条件采样的样本质量和图文对齐（Fig.3，最佳 scale ~6）。
- GPT-2 文本解码器重建 BLEU-1 0.969 / BLEU-4 0.894（latent 维度仅 64 仍重建良好）。
- 局限：作者自述生成文本"不够流畅"，主因 LAION 文本本身噪声大（v1 引入内部干净数据正是为缓解）。

**未报告**：GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 人评 ELO 等（2022 年这些 benchmark 多数尚未普及）；i2t 未报告 CIDEr/SPICE 等 captioning 标准指标，只报告 CLIP score。

## 创新点与影响
**核心贡献**
1. **统一视角**：把扩散模型对边缘 / 条件 / 联合分布的学习统一为"预测加噪噪声、各模态 timestep 可不同"，对原 DDPM 仅作极小改动即覆盖全部生成任务，单损失、单次前向反向、与原 DDPM 同效率。
2. **CFG for free**：因同一网络天然含条件与无条件模型，无需 null token 即可在条件与联合采样上做 CFG（并首次给出联合采样的 CFG 形式）。
3. **一个 Transformer（U-ViT）通吃**：把两模态数据与各自 timestep 都 token 化，post-LN + skip-connection LN 解决大规模混合精度训练稳定性；规模化到 LAION-5B 验证可行。

**影响**：UniDiffuser 是**早期"统一多模态扩散"的代表作**，证明了"单网络拟合所有分布"在大规模真实数据上可行且不牺牲单任务性能，为后续 unified / any-to-any 生成（统一图文理解+生成、omni 模型）提供了概念范式；U-ViT 也是把 Transformer（而非 U-Net）用作扩散 backbone 的早期工作，与 DiT 同期推动了扩散 backbone 向纯 Transformer 迁移。已并入 HuggingFace `diffusers`（`UniDiffuserPipeline`）。

**已知局限**：生成文本流畅度受限于 LAION 噪声文本；联合训练梯度方差略高；i2t 质量未用标准 captioning 指标量化；模态数仅扩到图文两种，更多模态与半监督学习留作未来工作；许可证 agpl-3.0。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2303.06555
- pdf: https://arxiv.org/pdf/2303.06555
- github: https://github.com/thu-ml/unidiffuser
- hf (v1): https://huggingface.co/thu-ml/unidiffuser-v1
- hf (v0): https://huggingface.co/thu-ml/unidiffuser-v0
- diffusers 文档: https://huggingface.co/docs/diffusers/main/en/api/pipelines/unidiffuser

## 一手源存档（sources/）
- [arxiv-2303.06555.pdf](https://arxiv.org/pdf/2303.06555)  （arXiv 原文 PDF，不入 git）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/unidiffuser--readme.md)
- [hf-v1-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2022/unidiffuser--hf-v1-card.md)
