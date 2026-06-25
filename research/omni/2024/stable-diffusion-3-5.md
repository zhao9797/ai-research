---
title: "Stable Diffusion 3.5 (Large / Large Turbo / Medium)"
org: "Stability AI"
country: EU
date: "2024-10"
type: model-card
category: t2i
tags: [t2i, mmdit, rectified-flow, open-weights, qk-norm, distillation, sd3]
url: "https://stability.ai/news/introducing-stable-diffusion-3-5"
arxiv: "https://arxiv.org/abs/2403.03206"
pdf_url: "https://arxiv.org/pdf/2403.03206"
github_url: "https://github.com/Stability-AI/sd3.5"
hf_url: "https://huggingface.co/stabilityai/stable-diffusion-3.5-large"
modelscope_url: ""
project_url: "https://stability.ai/news/introducing-stable-diffusion-3-5"
downloaded: [sd35--blog.md, sd35--large-hfpage.md, sd35--large-turbo-hfpage.md, sd35--medium-hfpage.md, sd35--github-readme.md, arxiv-2403.03206.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Stable Diffusion 3.5 是 Stability AI 2024 年 10 月发布的开源 T2I 模型族（Large 8.1B / Large Turbo 蒸馏 4 步 / Medium 2.5B），在 [[stable-diffusion-3|SD3]] 的 MMDiT + rectified flow 基础上做产品化重训，核心工程改进是把 **QK-Normalization** 引入 transformer block 以稳定训练并大幅提升下游可微调性（fine-tune / LoRA），Medium 进一步用 **MMDiT-X**（前若干层加双注意力）+ 多分辨率渐进训练把 0.25–2MP 全量程做好，且仅需约 9.9GB VRAM（不含文本编码器）跑在消费级 GPU 上。它是 6 月 SD3 Medium 口碑翻车后的"将功补过"版本，定位社区可商用（<100 万美元年营收免费）的开源 T2I 主力之一。

## 背景与定位
- **前作教训**：2024 年 6 月 Stability 首发 SD3 Medium，官方在博客中直言"没有达到我们或社区的预期"（尤其人体解剖结构、复杂提示崩坏被广泛吐槽）。SD3.5 不是"快速补丁"，而是基于社区反馈重新训练的一代。
- **技术脉络**：SD3.5 沿用 SD3 论文 *Scaling Rectified Flow Transformers for High-Resolution Image Synthesis*（arXiv:2403.03206）确立的两大支柱——(1) **MMDiT**（Multimodal Diffusion Transformer，图像流与文本流双流、各自权重、在注意力处交互）；(2) **rectified flow**（直线噪声→数据路径 + logit-normal 时间步采样）。相对 [[latent-diffusion-ldm|LDM]]/[[sdxl|SDXL]] 的 U-Net + DDPM/EDM，SD3 系把骨干换成纯 transformer 并改用 flow matching 训练目标，并把 VAE 从 4 通道升到 16 通道 latent。
- **SD3.5 的增量**：在 SD3 框架内做了三件事——QK-Norm 稳定性改造、Medium 的 MMDiT-X 与多分辨率训练协议、以及对 Large 蒸馏出 Turbo。架构核心（rectified flow + MMDiT + 三文本编码器 + 16ch VAE）与 SD3 论文一致，SD3.5 本身**未发独立技术报告**，方法细节散落在官方博客与三张 HF model card。

## 模型架构
**骨干：MMDiT / MMDiT-X（多模态扩散 transformer）**
- **MMDiT（Large / Large Turbo）**：双流 transformer，图像流（latent patch token）与文本流（文本 token）各有独立的权重（QKV/MLP/AdaLN），但在每个 block 的注意力里把两流拼接做联合 self-attention，实现跨模态交互。沿用 SD3 论文：2×2 patch、2D 位置编码、AdaLN 式 modulation（"Modulation Linear" 把时间步 embedding 与池化文本表示注入每个 block，论文 Fig.2）。
- **MMDiT-X（Medium 专属）**：在原 MMDiT 上做两项改进——(1) 在 transformer 的**前 13 层引入额外的自注意力模块（dual / 双注意力块）**，增强多分辨率生成与整体图像连贯性（model card 文本两处分别写"first 13 layers"与"first 12 transformer layers"，以图示 mmdit-x.png 为准，指前若干层加双注意力）；(2) 配合多分辨率渐进训练（见训练方法）。
- **QK-Normalization（全系核心改造）**：在 transformer block 的注意力 query/key 上做归一化（RMSNorm 形式），目的有二——稳定大规模训练（防注意力 logit 爆炸），以及**简化下游 fine-tune**。官方明确这是为"可定制性"服务的设计取舍：代价是同一 prompt 不同 seed 输出方差更大（刻意保留更广知识面与风格多样性），prompt 不够具体时不确定性也更高。
- **文本编码器（三编码器，冻结）**：OpenCLIP-ViT/bigG + OpenAI CLIP-ViT/L（各 77 token）+ Google **T5-XXL**（训练不同阶段用 77 / 256 上下文）。三者拼接：CLIP 提供池化全局语义注入 AdaLN，T5 提供长序列细粒度文本 token 进入 MMDiT 联合注意力。Medium 推理时 T5 超过 256 token 边缘易出 artifact，官方建议控制长度。
- **VAE**：16 通道 latent autoencoder（SD3 论文证明 d=16 比传统 4/8 通道重建与 scaling 更好），SD3.5 参考实现的 VAE Decoder 去掉了 postquantconv 步骤（GitHub README）。
- **参数量 / 分辨率**：Large 8.1B（1MP / 1024×1024 专业级）；Large Turbo 同骨干蒸馏；Medium 2.5B（0.25–2MP，多分辨率）。Medium 在低分辨率阶段把位置编码空间扩展到 384×384（latent）并对位置编码做随机裁剪增广（如给 64×64 latent 从 192×192 嵌入空间随机裁 64×64 输入 x 流），以提升多分辨率/多宽高比鲁棒性。

## 数据
- 三张 model card 对数据的口径完全一致且简略：**"trained on a wide variety of data, including synthetic data and filtered publicly available data"**——合成数据 + 经过滤的公开可得数据。
- **未披露**：训练集规模、图文对数量、数据配比、re-captioning 比例、美学打分阈值、去重/版权过滤细节等具体数字 SD3.5 均未公开。
- 可借 SD3 论文外推（非 SD3.5 官方确认）：SD3 用了 50/50 原始 caption 与合成 caption（VLM re-caption）混合，并做美学过滤（去掉评分过低图）与去重；SD3.5 大概率延续此 pipeline，但官方未在 SD3.5 文档中确认。
- **重要差异**：官方明确 Medium 与 Large "训练数据分布不同"，故同一 prompt 两者响应可能不一致——说明 SD3.5 各尺寸不是简单同一数据蒸馏，而是各自重训。
- 安全：使用过滤后的数据集训练，配套 Integrity Evaluation 与内容安全护栏，但承认无法保证移除全部有害内容。

## 训练方法
- **训练目标**：rectified flow（conditional flow matching，预测从噪声到数据的直线速度场 v），配 **logit-normal 时间步采样**（对中间噪声水平加权，SD3 论文证明优于 uniform/EDM 采样）。SD3.5 沿用该目标，未改训练损失形式。
- **分辨率/时间步 shift**：高分辨率需要把时间步 schedule 向噪声端 shift（像素更多→需要更"晚"的噪声水平），SD3 论文在 1024² 训练与采样均用 shift α=3.0。SD3.5 沿用 resolution-dependent shift 策略。
- **Medium 的多分辨率渐进训练（SD3.5 特有、官方披露）**：
  - 渐进阶段 **256 → 512 → 768 → 1024 → 1440** 分辨率逐级提升；
  - 最后阶段混入 **mixed-scale 图像训练**以增强多分辨率生成；
  - 低分辨率阶段扩展位置编码到 384×384 并做随机裁剪增广（见架构）。
- **Large Turbo 蒸馏（方法已点名）**：Large Turbo 的 HF model card 明确写明用 **Adversarial Diffusion Distillation（ADD）**（card 链接 Stability 的 ADD 技术报告），从 Large 蒸馏出可 **4 步**生成的版本，card 原文称 ADD "allows sampling with 4 steps at high image quality"，并称该模型 "is an ADD-distilled MMDiT"。推理配置 card 给出：**4 步、guidance_scale=0.0**（diffusers 示例）。**未公开的是 ADD 的训练超参/判别器/教师步数等细节**（card 只点名方法 + 给 4 步推理，不含蒸馏训练配置数字）。注：此前 Stability 在 [[sdxl-turbo-add|SDXL-Turbo（ADD）]] / SD3-Turbo（Latent-ADD）即同一谱系。
- **稳定性/可微调 trick**：QK-Norm 是全系最关键的训练 trick（既稳训又利于下游 fine-tune/LoRA），是 SD3.5 相对 SD3 的主要差异之一。
- 偏好对齐（RLHF/DPO）：SD3.5 文档未提及对 3.5 做 DPO/reward 对齐（SD3 论文附录 C 有 DPO 实验，但属 SD3）。SD3.5 是否做偏好对齐**未报告**。

## Infra（训练 / 推理工程）
- **训练算力/并行/GPU 时**：SD3.5 **完全未披露**（无技术报告，博客与 card 均无 infra 数字）。
- **推理 / 部署（有具体数字）**：
  - Medium 仅需约 **9.9GB VRAM**（不含三文本编码器）即可发挥全部性能，官方主打消费级 GPU "out of the box"；
  - 各档默认推理配置（card diffusers 示例）：**Large 28 步 / guidance 3.5**；**Medium 40 步 / guidance 4.5**；**Large Turbo 4 步 / guidance 0.0**；
  - Large Turbo **4 步**（ADD 蒸馏）采样，为同尺寸最快推理之一；
  - 全系提供 **fp16 / fp8（e4m3fn）** T5 权重，model card 给出 diffusers 量化示例（降显存）；
  - Medium 推荐推理时用 **Skip Layer Guidance（SLG）** 提升结构与解剖连贯性（ComfyUI PR #5404）。
- **参考实现**：官方 GitHub `Stability-AI/sd3.5` 为 inference-only 精简参考库（含 CLIP-L/bigG/T5-XXL 文本编码器、16ch VAE Decoder、全新 MM-DiT 核心），2024-10-24 起改 MIT 许可；推荐生产用 ComfyUI / diffusers。2024-11-26 追加 SD3.5-Large 的 Blur/Canny/Depth ControlNet。
- **部署形态**：HF 自托管权重 + Stability API / Replicate / Fireworks / DeepInfra / ComfyUI，以及 Amazon SageMaker JumpStart。

## 评测 benchmark（把效果讲清楚）
- **SD3.5 官方未给出可抠的数值表**。官方博客只给定性结论 + 一张相对柱状图（prompt adherence / 图像质量人评，无绝对数字）：
  - SD3.5 **Large** 在 prompt adherence 上"领先市场"，图像质量可与更大模型比肩；
  - SD3.5 **Large Turbo** 同尺寸推理最快，质量/对齐对非蒸馏同尺寸模型仍有竞争力；
  - SD3.5 **Medium** 优于其他中等尺寸模型，质量/对齐取得平衡。
  - 这些均为官方自评、**无 FID/CLIP/GenEval 绝对值**，按一手源应记为"未报告具体数字"。
- **可引用的最近一手数字（SD3 论文，非 SD3.5，作为基线参考）**：SD3 8B 基座（depth=38，512² 评测）在 **GenEval** 上 Overall **0.68**，分项 Single 0.98 / Two 0.84 / Counting 0.66 / Colors 0.74 / Position 0.40 / Attribution 0.43，超过当时全部开源模型与 DALL·E 3（0.67）。SD3.5 Large 由该 8B 基座谱系重训而来，但 Stability **未单独公布 SD3.5 的 GenEval 数字**，故以上仅作 SD3 基线，不能等同 SD3.5 成绩。
- **关键消融（来自 SD3 论文，SD3.5 继承的设计依据）**：
  - rectified flow + logit-normal 采样在多种 formulation 对比中综合最优；
  - 16 通道 VAE 比低通道在 scaling 上更好；
  - 更大模型采样效率更高（depth=38 用 5/50 步相对 CLIP 下降仅 2.71%，远好于 depth=15 的 4.30%）。
- SD3.5 自身的消融（QK-Norm 对方差/可微调的影响、MMDiT-X 双注意力增益、多分辨率训练增益）**官方仅定性描述，无量化消融表**。

## 创新点与影响
- **核心贡献**：(1) 把 **QK-Normalization** 系统性引入 MMDiT，换取训练稳定 + 下游高可微调性，并坦诚说明随之而来的输出方差/确定性取舍——这是把扩散基座当作"可生态化底座"而非"调好就锁死"的产品哲学；(2) **MMDiT-X** 前层双注意力 + 多分辨率渐进训练（256→1440 + mixed-scale + 位置编码随机裁剪），把 2.5B 小模型的 0.25–2MP 全量程与连贯性做扎实；(3) 一次开源 8.1B 全尺寸基座 + 4 步蒸馏 Turbo + 消费级 Medium 三档，覆盖研究/爱好者/创业/企业，且 <100 万美元年营收免费商用。
- **影响**：成为 ComfyUI/diffusers 生态可商用开源 T2I 主力之一；QK-Norm + 高可微调定位催生大量社区 LoRA/微调/ControlNet（官方随后补 Large 的 Blur/Canny/Depth ControlNet）；与同期 [[flux-1|FLUX.1]]（Black Forest Labs，由原 SD3 团队部分成员创立）形成开源 MMDiT/flow 路线的双雄对照。
- **已知局限**：(1) 无独立技术报告，infra/数据/benchmark 绝对数字几乎全未披露，复现与横评困难；(2) 为可微调牺牲了确定性，prompt 不具体时输出方差大、美学不稳定；(3) Medium 长 prompt（T5>256 token）边缘 artifact；(4) Large Turbo 蒸馏方法 card 已点名为 ADD（4 步），但具体训练配置（判别器、教师步数、对抗权重等）未公开；(5) 权重为 gated（需同意社区许可），raw README 不可直取。

## 原始链接
- blog（一等公民，发布说明 + 自评图）: https://stability.ai/news/introducing-stable-diffusion-3-5
- hf model card · Large（8.1B 基座）: https://huggingface.co/stabilityai/stable-diffusion-3.5-large
- hf model card · Large Turbo（4 步蒸馏）: https://huggingface.co/stabilityai/stable-diffusion-3.5-large-turbo
- hf model card · Medium（MMDiT-X / 多分辨率）: https://huggingface.co/stabilityai/stable-diffusion-3.5-medium
- github 参考实现: https://github.com/Stability-AI/sd3.5
- 架构与训练目标来源论文（SD3，arXiv:2403.03206）: https://arxiv.org/abs/2403.03206
- community license: https://stability.ai/community-license-agreement

## 本地落盘文件
- ../../../sources/omni/2024/sd35--blog.md
- ../../../sources/omni/2024/sd35--large-hfpage.md
- ../../../sources/omni/2024/sd35--large-turbo-hfpage.md
- ../../../sources/omni/2024/sd35--medium-hfpage.md
- ../../../sources/omni/2024/sd35--github-readme.md
- ../../../sources/omni/2024/arxiv-2403.03206.pdf
