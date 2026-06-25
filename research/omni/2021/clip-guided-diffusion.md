---
title: "CLIP-Guided Diffusion (Katherine Crowson / 社区版)"
org: "Community (Katherine Crowson, RiversHaveWings) / EleutherAI"
country: US
date: "2021-05"
type: method
category: method
tags: [clip-guidance, classifier-guidance, diffusion, text-to-image, training-free, community, ablated-diffusion]
url: "https://colab.research.google.com/drive/1QBsaDAZv8np29FPbvjffbE1eytoJcsgA"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/crowsonkb/clip-guided-diffusion"
hf_url: ""
modelscope_url: ""
project_url: "https://colab.research.google.com/drive/1QBsaDAZv8np29FPbvjffbE1eytoJcsgA"
downloaded: [clip-guided-diffusion--2021-colab.md, clip-guided-diffusion--crowsonkb-readme.md, guided-diffusion--openai-readme.md, diffusion-models-beat-gans--arxiv-abs.md, diffusion-models-beat-gans--model-card.md, arxiv-2105.05233.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
CLIP-Guided Diffusion 是 Katherine Crowson(RiversHaveWings)2021 年放出的一套**训练免费(training-free)**文生图方法：把 [[diffusion-models-beat-gans]](Dhariwal & Nichol)的"分类器引导(classifier guidance)"中的 ImageNet 分类器梯度,替换成 **CLIP 图文相似度的梯度**,从而用任意文本 prompt 去引导一个**无条件 ImageNet 扩散模型**生成与文字相符的图像。它本身不训练任何新模型、不发论文,只是一份 Colab notebook + 一份 512×512 无条件扩散权重,却是 [[glide]] / [[stable-diffusion]] 之前社区跑通"扩散 + CLIP = 文生图"的关键实践,直接催生了后来的 Disco Diffusion 等一系列民间生成工具。

## 背景与定位
2021 年初文生图的两条主线:一是自回归 token 路线([[dall-e-1]] / [[cogview]] / [[godiva]]),需要海量算力从头训练;二是 [[clip]](OpenAI 2021-02)发布后兴起的"**CLIP 引导优化**"路线——用 CLIP 当可微的"图文打分器",反向传播去优化一个图像生成器,代表作是 Crowson 等人更早的 **VQGAN+CLIP**(把 CLIP 梯度回传到 VQGAN 的 latent)。

与此同时,OpenAI 的 [[diffusion-models-beat-gans]](arXiv 2105.05233, 2021-05)首次让扩散模型在 ImageNet 上 FID 超过 GAN,并提出**分类器引导**:在采样的每一步,用一个在带噪图上训练的分类器 `p_φ(y|x_t)` 的梯度 `∇_{x_t} log p_φ(y|x_t)` 去把采样均值往目标类 `y` 推(Algorithm 1)。该论文还公开了 64/128/256/512 各分辨率的 ImageNet 扩散权重与代码(`openai/guided-diffusion`),为社区提供了高质量的扩散 backbone。

Crowson 的关键洞察:**分类器引导里的"类别梯度",可以换成 CLIP 的"图文对齐梯度"**。CLIP 本质上就是一个开放词表的零样本分类器/打分器,把 `log p_φ(y|x_t)` 换成"图像 CLIP 嵌入与文本 CLIP 嵌入的相似度",`y` 就从 1000 个 ImageNet 类标签变成了**任意一句自然语言 prompt**。于是无需重新训练扩散模型,就能做开放词表文生图。值得一提的是,OpenAI 自己在该模型的 model card 里也"探测"过这个用法(把去噪预测喂给 CLIP 并对全过程求导),但结论是"难以从 CLIP 提取信息";而 Crowson 用 **多裁剪(cutouts)+ 辅助正则项** 的工程手法把它真正跑成了可用的文生图——这正是社区版相对官方探测的价值所在。

技术脉络中的位置:VQGAN+CLIP(latent 优化)→ **CLIP-Guided Diffusion(扩散采样引导)**→ [[glide](OpenAI,把文本条件直接训进扩散模型 + classifier-free guidance)] → [[stable-diffusion]]。它是"CLIP 当外挂打分器"范式在扩散模型上的落地,也是"扩散文生图民间化"的起点。

## 模型架构
本方法**不引入新网络**,而是把两个现成模型组合到采样回路里:

- **扩散 backbone:OpenAI Ablated Diffusion Model(ADM)U-Net**。来自 [[diffusion-models-beat-gans]] 的改进 U-Net(Colab 实际 `git clone` 的是 Crowson fork `crowsonkb/guided-diffusion`,在 OpenAI 原版上加了 `cond_fn_with_grad` 等钩子,网络结构与官方一致),具体配置(见 Colab `model_config`):
  - `image_size=512`,`num_channels=256`(变宽),`num_res_blocks=2`,`learn_sigma=True`(同时预测均值与方差 Σ),`noise_schedule='linear'`,`diffusion_steps=1000`;
  - **多分辨率注意力**:`attention_resolutions='32,16,8'`,`num_head_channels=64`(每头 64 通道);
  - **BigGAN 风格上/下采样残差块**(`resblock_updown=True`)、**AdaGN(adaptive group norm)** 把时间步嵌入注入残差块(`use_scale_shift_norm=True`);
  - `use_fp16=True`,`class_cond=False`(**无条件**)。
  - 权重为 `512x512_diffusion_uncond_finetune_008100.pt`——并非 OpenAI 官方发布,而是社区(RiversHaveWings)从 OpenAI **512×512 类条件** ImageNet 扩散模型 **fine-tune 8100 步去掉类条件** 得到的无条件版本,托管在 the-eye.eu / `models.rivershavewings.workers.dev`。
- **文本/图像编码器:CLIP ViT-B/16**(`clip.load('ViT-B/16')`),冻结、不回传到其参数。CLIP 把 prompt 编成文本嵌入 `target_embeds`,把候选图的裁剪编成图像嵌入,用于计算对齐损失。
- **条件注入方式:采样时梯度引导(training-free)**,而非把文本编码喂进 U-Net。每个扩散步在 U-Net 的去噪估计上,叠加一个由 CLIP/正则损失反传得到的梯度修正项(下文"训练方法"详述)。这与 [[glide]] 把文本 token 经 Transformer 编码后**训练进** U-Net 的 cross-attention/AdaLN 形成鲜明对比——本方法零训练。

辅助组件:`MakeCutouts`(随机多尺度裁剪,缓解 CLIP 对单一全图嵌入的对抗脆弱性)、`lpips`(VGG LPIPS,可选 init-image 损失)。

## 数据
本方法**不做任何训练数据收集**,因此无数据集构建。涉及数据仅限于所复用模型的预训练语料:

- **扩散 backbone 数据**:ImageNet(ILSVRC 2012 子集,约 100 万张、1000 类;大量动植物与自然物,常含未被标签反映的人物)——见 [[diffusion-models-beat-gans]] model card。社区 fine-tune 仅在 ImageNet 自身上跑了 8100 步去类条件,**未引入额外文本-图像配对数据**。
- **CLIP 数据**:OpenAI 内部 WIT(WebImageText)约 4 亿图文对(本页未单独抓取 CLIP 论文,数字引自公认事实,具体见 [[clip]])。
- 清洗/配比/美学过滤/合成数据:**不适用**(无新训练)。

## 训练方法
**核心是采样,而非训练**(zero-shot / training-free guidance)。逐步说明(源自 Colab `cond_fn` 与 `do_run`,文件 `clip-guided-diffusion--2021-colab.md`):

1. **去噪估计混合**:在步 `t`,取 U-Net 的 `pred_xstart`(对 x₀ 的预测)与当前噪声图 `x` 做加权混合
   `x_in = pred_xstart * fac + x * (1 - fac)`,其中 `fac = sqrt_one_minus_alphas_cumprod[t]`。这样高噪声步用更接近去噪结果的图喂给 CLIP(对应论文里"对去噪预测求导"的做法)。
2. **多裁剪 CLIP 打分**:用 `MakeCutouts` 取 `cutn=32` 个随机尺度裁剪(`cut_pow=0.5`),CLIP-normalize 后用 CLIP ViT-B/16 编码,得到一批图像嵌入;重复 `cutn_batches=2` 批做梯度累积。
3. **球面距离损失(spherical_dist_loss)**:对 L2 归一化后的图像/文本嵌入,计算
   `2·arcsin(‖x̂ − ŷ‖/2)²`(即单位球面上大圆距离的平方),按 prompt 权重加权求和——比直接用 cosine 更利于引导稳定。
4. **辅助正则**:`tv_loss`(L2 total variation,平滑度,`tv_scale=150`)、`range_loss`(惩罚超出 [-1,1] 的 RGB,`range_scale=50`),可选 `LPIPS` init-image 损失(`init_scale`)。
5. **求梯度并注入采样**:`grad = -∇_x [clip_guidance_scale·spherical_dist + tv·tv_scale + range·range_scale]`(`clip_guidance_scale=1000`),把 `grad` 作为 `cond_fn` 传入 `diffusion.p_sample_loop_progressive`(DDPM 随机采样)或 `ddim_sample_loop_progressive`(DDIM)。这与 [[diffusion-models-beat-gans]] Algorithm 1 完全同构:采样均值由 `μ` 移到 `μ + s·Σ·∇log p(y|x)`,只是把"分类器对数似然梯度"换成"CLIP 对齐(负)损失梯度"。

> 与官方分类器引导的差异:OpenAI 用**专门在带噪图上训练的噪声分类器**;Crowson 直接用**冻结的、在干净图上训练的 CLIP**,靠"对去噪预测求导 + 多裁剪 + TV/range 正则"来弥合"CLIP 没见过带噪图"的分布鸿沟。无任何 SFT / RLHF / 蒸馏 / 偏好对齐——所有"训练"都发生在被复用的 ADM 与 CLIP 里。

加速/蒸馏:原始 2021 版无蒸馏,靠 `timestep_respacing`(如改成 `ddim50`)减步;v2 重写版(2023)改用 **k-diffusion + 自适应步长的 DPM-Solver++(3) SDE** 求解器,并对高阶修正项不做引导(splitting method),以更少步数获得相近质量。

## Infra(训练 / 推理工程)
- **训练算力**:本方法 0 训练,无 GPU·时开销;社区 fine-tune 去类条件仅 8100 步(具体卡数/时长**未披露**)。OpenAI 原 backbone 的训练算力见 [[diffusion-models-beat-gans]]。
- **推理形态**:单卡 Colab 即可跑,`use_fp16=True` 半精度,512×512 单张默认 `timestep_respacing='1000'`(满 1000 步,可改小)。Colab 明确标注本 512² 版**需 16 GB 显存**(配不到则改用 256×256 版 notebook)。CLIP 多裁剪(`cutn=32 × cutn_batches=2`)是显存与时延主要开销;`clip_guidance_scale` 越高,采样越往 prompt 收敛但越慢。
- **部署**:以 Google Colab notebook 形式分发,一键 `curl` 拉权重(the-eye.eu)+ `pip install` OpenAI guided-diffusion / CLIP,门槛极低——这正是它能在社区病毒式传播的工程关键。
- v2 重写版支持 `torch.compile()`、`--device` 自动选择、多 CLIP 模型集成、权重改用 safetensors。
- 量化/缓存等推理优化:**未涉及**。

## 评测 benchmark
**本方法没有发布任何定量评测**(无 FID / CLIPScore / GenEval / 人评 ELO 等)——它是一份社区 notebook,效果靠示例图与社区口碑(例如 README 示例 prompt "chrysanthemum supernova, trending on ArtStation"、"A landscape resembling the Death tarot card by Gerardo Dottori")。下列数字均为其**所依赖 backbone** 的官方指标,用于交代质量底座,**不可当作本方法自身分数**:

- [[diffusion-models-beat-gans]](已抓 `arxiv-2105.05233.pdf`)ImageNet 类条件 + 分类器引导 FID:128² 2.97、256² 4.59、512² 7.72;配合上采样栈进一步到 256² 3.94 / 512² 3.85。其无条件 256² 模型也是 SOTA 级。
- 论文关于引导强度的关键结论(可类比 CLIP 引导尺度的作用):无条件模型上把分类器梯度尺度从 1.0 提到 10.0,Pembroke Welsh corgi 类 FID 从 33.0 降到 12.0——**说明"引导尺度"需 >1 才能让样本真正对上目标**,这与 Colab 里 `clip_guidance_scale=1000` 这种大尺度同理(尺度越大越贴 prompt、多样性越低)。
- 本方法 vs 同期:相对 VQGAN+CLIP,扩散引导给出更自然的纹理/更少"CLIP 伪影";相对随后 [[glide]](其 MS-COCO 256² zero-shot FID 12.24 一数引自 [[glide]] 页/GLIDE 论文 Table 2,**本目录未单独落盘 GLIDE PDF**;GLIDE 把文本训进模型 + classifier-free guidance),本方法**质量与文本贴合度更弱**(CLIP 与扩散模型的分布不匹配、需大量裁剪/正则 hack),但**零训练、可即时换 backbone/CLIP**。本方法**自身从未在 MS-COCO 等标准 benchmark 上报告任何 FID/CLIPScore**。
- 关键"消融"(来自 Colab 默认超参,非正式实验):`tv_scale=150` 控平滑、`range_scale=50` 控 RGB 越界、`cutn=32 / cut_pow=0.5` 控 CLIP 视角多样性、`skip_timesteps`≈200–500 用于 init-image 引导——这些是社区反复调出的经验值,**无量化消融表**。

## 创新点与影响
**核心贡献**
1. **把 classifier guidance 推广为开放词表的 CLIP guidance**:用冻结 CLIP 的图文相似度梯度替代固定类标签分类器梯度,使**任意一个无条件扩散模型 + 任意 CLIP** 在零训练下就能做文生图。
2. **一套让"干净图 CLIP"对齐"带噪扩散"的工程配方**:对去噪预测 `pred_xstart` 求导、多尺度随机裁剪(抗 CLIP 对抗脆弱性)、球面距离损失、TV/range/LPIPS 正则——把 OpenAI model card 里"难以从 CLIP 提取信息"的悲观结论变成了可用产品。
3. **极低门槛的分发**:一份 Colab + 一份社区 fine-tune 的 512×512 无条件权重,普通人单卡即可玩文生图。

**影响**
- 直接催生 **Disco Diffusion**(在此 notebook 基础上加多模型集成、3D 动画、调度器),成为 2021–2022 AI 艺术浪潮的核心工具之一;与 VQGAN+CLIP 一起把"输入一句话出图"带进大众视野。
- 在范式上为 [[glide]] / [[stable-diffusion]] 铺路:验证了"扩散 + CLIP 文本对齐"的可行性,也暴露了"外挂 CLIP 引导"的上限(分布不匹配、需大量 hack、慢),促使后续把文本条件**直接训进**扩散模型(GLIDE 的 classifier-free guidance、SD 的 cross-attention text-conditioning)。
- 让 Katherine Crowson 成为开源扩散生态的关键人物(后续 k-diffusion 采样器库、HDiT 等)。

**已知局限**
- 文本贴合度与可控性弱于原生文本条件模型(CLIP 与扩散分布不匹配,靠裁剪/正则硬凑);
- 采样慢(每步要多次 CLIP 前向 + 反传);
- backbone 只在 ImageNet 上训过,人脸/复杂场景质量差(继承 ImageNet 偏置,见 model card 局限),提示工程依赖 "trending on ArtStation" 这类 magic words;
- 无任何官方定量评测,质量评估全凭主观/社区共识。

## 原始链接
- colab (原始 2021 方法,一手): https://colab.research.google.com/drive/1QBsaDAZv8np29FPbvjffbE1eytoJcsgA
- github (v2 重写版 + 指向 2021 Colab): https://github.com/crowsonkb/clip-guided-diffusion
- github (扩散 backbone 来源,OpenAI guided-diffusion): https://github.com/openai/guided-diffusion
- paper (理论基础,Diffusion Models Beat GANs / classifier guidance): https://arxiv.org/abs/2105.05233
- model-card (backbone 数据与 CLIP-guidance 探测说明): https://github.com/openai/guided-diffusion/blob/main/model-card.md
- 依赖 (CLIP): https://github.com/openai/CLIP  ·  k-diffusion(v2): https://github.com/crowsonkb/k-diffusion

## 本地落盘文件
- ../../../sources/omni/2021/clip-guided-diffusion--2021-colab.md
- ../../../sources/omni/2021/clip-guided-diffusion--crowsonkb-readme.md
- ../../../sources/omni/2021/guided-diffusion--openai-readme.md
- ../../../sources/omni/2021/diffusion-models-beat-gans--arxiv-abs.md
- ../../../sources/omni/2021/diffusion-models-beat-gans--model-card.md
- ../../../sources/omni/2021/arxiv-2105.05233.pdf  (Diffusion Models Beat GANs 全文,40MB,.gitignore 排除不入 git)
