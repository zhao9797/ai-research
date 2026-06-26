---
title: "Rerender A Video: Zero-Shot Text-Guided Video-to-Video Translation"
org: "NTU S-Lab"
country: China
date: "2023-06"
type: paper
category: video
tags: [video-to-video, zero-shot, stylization, diffusion, optical-flow, cross-frame-attention, ebsynth, controlnet, siggraph-asia]
url: "https://arxiv.org/abs/2306.07954"
arxiv: "https://arxiv.org/abs/2306.07954"
pdf_url: "https://arxiv.org/pdf/2306.07954"
github_url: "https://github.com/williamyang1991/Rerender_A_Video"
hf_url: "https://huggingface.co/spaces/Anonymous-sub/Rerender"
modelscope_url: ""
project_url: "https://www.mmlab-ntu.com/project/rerender/"
downloaded: [arxiv-2306.07954.pdf, rerender-a-video--ar5iv.md, rerender-a-video--readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
Rerender A Video（NTU S-Lab，SIGGRAPH Asia 2023）是一个**完全零样本、免训练/免优化**的文本引导视频风格化框架：用「关键帧扩散翻译 + 非关键帧光流传播」的混合管线，把现成图像扩散模型（Stable Diffusion + ControlNet）适配到视频；核心创新是**分层跨帧约束（hierarchical cross-frame constraints）**在扩散采样的不同阶段分别约束风格、形状、纹理、颜色，配合一个**保真度导向的零样本图像编码（fidelity-oriented image encoding）**抑制 VAE 反复编解码的误差累积。在零样本 V2V 评测上 Pixel-MSE 0.069（同期最低）、用户主观偏好三项均超 65%。

## 背景与定位
直接把图像扩散模型逐帧套到视频上会产生**严重闪烁（flickering）**，因为每帧独立去噪、局部纹理无约束。当时三类方案各有短板：
1. **从头训视频模型**（[[video-diffusion-models]]、Imagen Video）——算力巨大、且与现成图像模型不兼容；
2. **单视频微调图像模型**（[[tune-a-video]]）——长视频低效、易过拟合损伤原模型；
3. **零样本方法**（[[text2video-zero]]、Pix2Video、FateZero）——免训练、兼容现成模型，但当时的跨帧约束只作用在 latent 上做**全局风格**对齐，无法保证**低层纹理/细节**一致，整体风格一致但局部仍闪。

本工作选择零样本路线（为兼容现成 SD/LoRA/ControlNet 生态），主攻第 3 类的核心痛点——**低层时序一致性**。关键 insight：用**光流（optical flow）**施加稠密的跨帧约束，以「上一渲染帧」作低层参考、以「首个渲染帧（anchor）」作锚点防止外观漂移；并把约束**分层**落到扩散采样的早/中/晚不同阶段。相关前置工作：[[latent-diffusion-ldm]]（SD backbone）、[[controlnet]]（结构引导）、[[sdedit]]（加噪初始化）、[[ddim]]（确定性采样）、Ebsynth/Stylizing-Video-by-Example（基于样例的逐帧传播）。

## 模型架构
**不训练任何新网络**——整套方法是对现成图像扩散模型推理过程的「外科手术式」改造。组件：

- **Backbone**：Stable Diffusion 1.5（latent diffusion，U-Net 噪声预测 $\epsilon_\theta$，在 VQ/KL-VAE 的 latent 空间 $\mathcal{D}(\mathcal{E}(\cdot))$ 上去噪）。可直接替换为 civitai 上的微调/LoRA 模型（如 revAnimated_v11、realisticVisionV20）做定制风格。
- **结构引导**：[[controlnet]] 旁路注入 HED/Canny 边缘等条件 $c_f$，使噪声预测变为 $\epsilon_\theta(x_t,t,c_p,c_f)$；为视频提供逐帧结构对齐（之所以选 ControlNet 而非 InstructPix2Pix，是因为 ControlNet 与定制 SD 模型正交）。
- **光流**：用 **GMFlow** 估计帧间光流 $w_j^i$，并用前后向一致性校验（forward-backward consistency check）得到遮挡掩码 $M_j^i$。
- **传播器**：**Ebsynth**（Jamriška et al. 2019 的「Stylizing Video by Example」）做关键帧到非关键帧的引导式 patch-matching 传播 + 时序融合。

**核心架构创新——分层跨帧约束（落在 T 步采样的不同区间，见论文 Fig.4(b)）：**

1. **风格层 / Style-aware cross-frame attention（全程）**：把 U-Net 的 self-attention 换成 cross-frame attention。query 仍来自当前帧 $v_i$，但 key/value 取自**首帧 $v_1$ 与前一帧 $v_{i-1}$ 的拼接** $[v_1;v_{i-1}]$。直觉：self-attn 是帧内 patch 匹配投票，cross-frame attn 则从其它帧借相似 patch，使 $I_i'$ 继承 $I_1'$、$I_{i-1}'$ 的全局风格。
2. **形状层 / Shape-aware latent fusion（早期步 $T_s=0.1T_{max}$ 起）**：在 latent 空间按光流 warp + 遮挡掩码融合预测的 $\hat{x}_{t\to0}$：$\hat{x}_{t\to0}^i \leftarrow M_j^i\cdot\hat{x}_{t\to0}^i + (1-M_j^i)\cdot w_j^i(\hat{x}_{t\to0}^j)$。实验发现用 anchor 帧（$j{=}0$）比前一帧更稳；只在早期步做（latent 插值在晚期会致模糊/形变），用于粗对齐物体运动。
3. **像素层 / Pixel-aware latent fusion（中期步 $T_{p0}{=}0.5T_{max}\sim T_{p1}{=}0.8T_{max}$）**：不在 latent 里 warp，而是把 anchor 帧与前帧的**像素结果** warp 到当前帧、叠加到一张粗渲染帧上，得到融合帧 $\tilde{I}_i'$，再**当作结构引导 inpainting 问题**：掩码外区域要匹配 $\tilde{I}_i'$、掩码内（$M_i=M_0^i\cap M_{i-1}^i$）交给 ControlNet 生成。latent 更新 $x_{t-1}^i \leftarrow M_i\cdot x_{t-1}^i + (1-M_i)\cdot \tilde{x}_{t-1}^i$。这是实现**像素级时序一致**的关键。
4. **颜色层 / Color-aware adaptive latent adjustment（晚期步 $T_a=0.8T_{max}$）**：对 $\hat{x}_{t\to0}^i$ 做 **AdaIN**，把逐通道均值/方差对齐到首帧 $\hat{x}_{t\to0}^1$，保证整段关键帧色调一致（可选，让用户决定跟首帧还是跟输入色）。

**关键子模块——保真度导向的零样本图像编码 $\mathcal{E}^*$**：像素层融合需要反复「warp→编码回 latent」，而 SD 的有损 VAE 每次编解码引入失真/偏色并沿帧累积（编解码 10 次后明显劣化）。本文 insight：**每次自编码丢失的信息量近似恒定**，故可预测并补偿。对图像 $I$ 编解码两次得 $x_0^r=\mathcal{E}(I)$、$I^r=\mathcal{D}(x_0^r)$、$x_0^{rr}=\mathcal{E}(I^r)$，假设从无损 $x_0$ 到 $x_0^r$ 的损失线性于 $x_0^r$ 到 $x_0^{rr}$ 的损失，定义补偿编码 $\mathcal{E}'(I):=x_0^r+\lambda_\mathcal{E}\,\mathcal{E}(x_0^r-x_0^{rr})$（取 $\lambda_\mathcal{E}=1$ 即可），再加掩码 $M_\mathcal{E}$（仅在重建误差低于阈值处补偿，防补偿带来的新伪影）得到 $\mathcal{E}^*(I):=x_0^r+M_\mathcal{E}\cdot\lambda_\mathcal{E}(x_0^r-x_0^{rr})$。免微调，对 f8-ft-MSE 与原始 kl-f8 两种 VAE 均有效。

**分辨率/参数**：不改模型参数量（SD 1.5 + ControlNet 现成权重）。输入视频短边 resize 到 512、按 512×512 处理。采样用 **20 步 DDIM**；起点按 [[sdedit]] 用输入帧的加噪 latent $x_T=\sqrt{\bar\alpha_T}x_0+\sqrt{1-\bar\alpha_T}z_T$，通过调 $T$ 控制保留多少原始细节（$T$ 小则更像原视频）。

## 数据
**本工作不做任何训练，故无训练数据集。** 涉及的"数据"仅为：
- **评测/演示视频**：取自 [pexels.com](https://www.pexels.com/) 与 [pixabay.com](https://pixabay.com/)（短边 resize 到 512）；用户研究用 8 段测试视频。
- **保真编码定量评测**：用 **MS-COCO 验证集前 1,000 张图**测多次编解码的 MSE。
- **基模型**：Stable Diffusion 1.5 官方权重 + civitai 社区微调/LoRA 模型（revAnimated_v11、realisticVisionV20 等）；ControlNet 官方权重。
- 论文未提供大规模训练数据来源、配比、清洗或 re-captioning——因为方法本身零训练，**该维度对本工作不适用**。

## 训练方法
**无训练、无优化、无微调——这是本工作的核心卖点（zero-shot）。** 所有"方法"都发生在**推理期**：

- **采样目标**：复用预训练 SD 的 diffusion 去噪目标，本身不引入新 loss。基于 [[ddim]] 确定性采样、20 步。
- **改造点全在采样过程**：上节四层跨帧约束 + 保真编码，均为对 $\hat{x}_{t\to0}$ / $x_{t-1}$ 的算子级注入，不更新任何权重。
- **可与现成训练技术叠加**：因不动预训练权重，与 [[dreambooth]]、[[lora]]（定制主体/风格）、[[controlnet]]（结构引导）正交可组合；README 后续还集成了 **Loose cross-frame attention**（在更少层用 cross-frame attn，更贴合大运动输入、减少 ghosting）与 **[[freeu]]**（免训练提升对比度/饱和度/细节）。
- **关键超参（默认值）**：$T_s=0.1T_{max}$、$T_{p0}=0.5T_{max}$、$T_{p1}=0.8T_{max}$、$T_a=0.8T_{max}$（$T_{max}=1000$）；DDIM 20 步；关键帧间隔默认 $K=10$；补偿系数 $\lambda_\mathcal{E}=1$；每段视频单独微调 $T$ 与 ControlNet 控制权重。
- **加速/蒸馏**：不涉及 consistency/LCM/步数蒸馏；"加速"来自混合管线——只对 1/K 的帧跑扩散，其余用廉价的 Ebsynth 传播。

## Infra（训练 / 推理工程）
- **硬件**：实验在**单卡 NVIDIA Tesla V100** 上完成；WebUI 实测需 **24GB 显存**（可用 xformers / 限制分辨率降显存）。
- **无训练算力开销**（零样本），故无 GPU·时 / 并行 / 混合精度等训练 infra 数字——本工作不适用。
- **推理速度（512×512）**：关键帧翻译约 **14.23s/帧**，非关键帧（Ebsynth 传播）约 **1.49s/帧**；整段平均 $1.49+12.74/K$ s/帧——$K=10$ 时约 **2.76s/帧**，$K$ 越大越快但质量下降。
- **全视频传播工程**：Ebsynth 部分支持**多进程并行**（独立脚本 `video_blend.py` 暴露 `--n_proc` 参数控制最大进程数；README 未给推荐值）；融合采用 Ebsynth 三步法的**前两步**（按 patch-match 误差选色/梯度 + 直方图保持的对比度融合），**刻意去掉第三步 Poisson 泊松融合**（作者发现其在非平坦区致伪影且耗时；WebUI 仍保留为可选项 gradient blending）。
- **部署形态**：开源 PyTorch 实现 + Gradio WebUI（三步式工作流：Run 1st Key Frame → Run Key Frames → Run Propagation）+ 🤗 HF Space 在线 demo；2023/12 已被官方 **Diffusers community pipeline** 收录。

## 评测 benchmark（把效果讲清楚）
**对比对象**：4 个同期零样本 V2V 方法——vid2vid-zero、FateZero、Pix2Video、[[text2video-zero]]，在关键帧翻译（$K=5$）上比较。注意：前三者官方代码不支持 ControlNet、加载定制模型时崩坏，故仅 Text2Video-Zero 与本方法用了相同定制模型 + ControlNet（公平对比）。

**定量指标**（沿用 FateZero/Pix2Video）：Fram-Acc（CLIP 帧级编辑准确率）、Tem-Con（相邻帧 CLIP 余弦相似度，越高越一致）、Pixel-MSE（对齐相邻帧的均方像素误差，越低越一致）。

| Metric | v2v-zero | FateZero | Pix2Video | T2V-Zero | **Ours** |
|---|---|---|---|---|---|
| Fram-Acc ↑ | 0.862 | 0.556 | **0.995** | 0.963 | 0.979 |
| Tem-Con ↑ | 0.975 | 0.979 | 0.953 | 0.983 | **0.983** |
| **Pixel-MSE ↓** | 0.098 | 0.085 | 0.216 | 0.084 | **0.069** |
| User-Balance ↑ | 3.8% | 5.9% | 9.2% | 15.4% | **65.8%** |
| User-Temporal ↑ | 3.8% | 9.6% | 4.2% | 10.8% | **71.6%** |
| User-Overall ↑ | 2.9% | 4.2% | 4.2% | 15.0% | **73.7%** |

- **结论**：本方法取得**最佳时序一致性**（Pixel-MSE 0.069 最低、Tem-Con 并列最高）、**次佳帧编辑准确率**（0.979，仅次于 Pix2Video 0.995——但 Pix2Video 过度修改输入致形变）。30 人用户研究（8 段视频）三项主观偏好**全部第一且大幅领先（65.8%/71.6%/73.7%）**。

**关键消融**：
- **分层约束逐项消融（Fig.10）**：cross-frame attn 保全局风格 → AdaIN 保发色一致 → SA fusion 对齐物体运动 → **PA fusion 才实现像素级一致**（发丝、痘痘等细节）；说明全局约束无法捕捉局部运动，PA fusion 不可或缺，且关键帧的像素一致还能**减少非关键帧传播的 ghosting**。
- **保真编码消融（Fig.13–15）**：在 MS-COCO 1000 图上多次编解码，$\mathcal{E}^*$ 相比裸编码**显著降低误差累积**，对 f8-ft-MSE（修伪影）与 kl-f8（修偏色）两种 VAE 均生效。
- **关键帧间隔 $K$（Table 3）**：$K$ 越大插帧越多、Pixel-MSE 越低（一致性更好）但 Fram-Acc 下降（$K{=}100$ 时 0.890）；**推荐 $K\in[5,20]$**（$K{=}10$：Fram-Acc 1.000 / Pixel-MSE 0.025）。

（注：无 FID/CLIPScore/GenEval/VBench 等指标——本工作是 V2V 编辑/风格化，评测体系以一致性 + CLIP 编辑准确率 + 用户研究为主，论文未报告生成式 T2I/T2V 常用 benchmark。）

## 创新点与影响
**核心贡献**：
1. **首个同时实现全局风格 + 低层纹理时序一致的零样本 V2V 框架**，免训练/免优化，且兼容现成图像扩散生态（SD/LoRA/DreamBooth/ControlNet）。
2. **分层跨帧一致性约束**——在扩散采样早/中/晚阶段分别约束形状/纹理/颜色，把"用光流施加稠密跨帧约束"这一思想落到 latent 算子级。
3. **混合「扩散生成 + patch 传播」管线**——扩散负责内容创造、Ebsynth 负责高效像素传播，在质量与效率间取平衡。
4. **保真度导向的零样本图像编码**——免微调即可抑制 VAE 反复编解码的误差累积，可被其它 diffusion 方法复用。

**影响**：作为 2023 年零样本视频编辑的代表作之一（与 Text2Video-Zero、TokenFlow、CoDeF 等同期），被 Diffusers 官方收录为 community pipeline，成为「免训练 V2V 风格化」的常用基线/工程参考；其"光流 warp + inpainting 注入 + Ebsynth 传播"的混合范式影响了后续一批一致性视频编辑工作。会议版后还持续加 Loose cross-frame attention、FreeU 等特性。

**已知局限**（论文 Sec.5.5）：
- **强依赖光流**：光流估计失败（大运动/无对应）→ PA fusion 失效、刺绣等细节无法保全。
- **假设翻译前后光流不变**：外观大改时该假设破裂，可能导致错误运动；关键帧间的光流错配会在 Ebsynth 融合后留下 ghosting。
- **细节/微动作丢失**：饰品、眼球转动等小细节难保留。
- **均匀采样关键帧非最优**：若某物体（如手）不在任何关键帧中出现，传播无法凭空创造——建议用户交互式指定关键帧。
- 不是端到端视频生成，**需逐视频调 $T$ 与 ControlNet 权重**；非关键帧靠插值，无法在帧间创造新内容。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2306.07954
- arxiv_pdf: https://arxiv.org/pdf/2306.07954
- ar5iv (full text): https://ar5iv.labs.arxiv.org/html/2306.07954
- github: https://github.com/williamyang1991/Rerender_A_Video
- project_page: https://www.mmlab-ntu.com/project/rerender/
- hf_space (demo): https://huggingface.co/spaces/Anonymous-sub/Rerender
- supplementary_video: https://youtu.be/cxfxdepKVaM
- diffusers community pipeline: https://github.com/huggingface/diffusers/tree/main/examples/community#Rerender_A_Video

## 一手源存档（sources/）
- [arxiv-2306.07954.pdf](https://arxiv.org/pdf/2306.07954)  （arXiv 原文 PDF，不入 git）
- [ar5iv.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/rerender-a-video--ar5iv.md)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2023/rerender-a-video--readme.md)
