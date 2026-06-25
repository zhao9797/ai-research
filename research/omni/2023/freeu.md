---
title: "FreeU: Free Lunch in Diffusion U-Net"
org: "S-Lab, Nanyang Technological University"
country: China
date: "2023-09"
type: paper
category: method
tags: [freeu, training-free, unet, skip-connection, backbone, fourier, frequency, inference-time, diffusion, stable-diffusion, cvpr2024]
url: "https://arxiv.org/abs/2309.11497"
arxiv: "https://arxiv.org/abs/2309.11497"
pdf_url: "https://arxiv.org/pdf/2309.11497"
github_url: "https://github.com/ChenyangSi/FreeU"
hf_url: "https://huggingface.co/spaces/ChenyangSi/FreeU"
modelscope_url: ""
project_url: "https://chenyangsi.top/FreeU/"
downloaded: [arxiv-2309.11497.pdf, freeu--project-page.md, freeu--github-readme.md]
created: 2026-06-25
updated: 2026-06-25
reviewed: 2026-06-25
---

## 一句话定位
FreeU（南洋理工 S-Lab，CVPR 2024 Oral）是一个**完全免训练、零新增参数、零额外显存/采样耗时**的扩散质量增强技巧：在 U-Net 解码阶段对**主干（backbone）特征做放大、对 skip-connection 特征做频域抑制**，仅靠推理时调两个标量因子（实现里拆成 b1/b2/s1/s2 四个）就能显著提升 [[stable-diffusion]]/SDXL/[[modelscope-t2v]] 等模型的生成保真度。人评中 SD+FreeU 在图文对齐与画质两项上各拿到 **85.88% / 85.34%** 的偏好票（视频侧 ModelScope+FreeU 为 84.71% / 85.67%），仅需"几行代码"即可集成。

## 背景与定位
扩散模型（[[ddpm]]、[[latent-diffusion-ldm]]）的去噪网络几乎全是 **time-conditional U-Net**，但学界绝大多数工作把这个 U-Net 当黑盒直接拿去做下游应用，**其内部各组件对去噪的具体贡献长期未被剖析**。FreeU 的切入点正是这块空白：不改权重、不加训练，纯粹从"U-Net 内部 backbone 与 skip 各自起什么作用"出发，找一份免费午餐（free lunch）。

作者先把去噪过程搬到**傅里叶域**观察（图 2/3）：发现去噪过程中**低频分量变化缓慢**（承载全局结构、布局、平滑色彩，是图像本质，不该剧烈改动），而**高频分量变化剧烈**（承载边缘、纹理等细节，对噪声高度敏感）。在此基础上进一步拆解 U-Net 的两条信息通路，得到核心观察：

- **主干 backbone 主要负责"去噪"**：实验把 backbone 特征乘以缩放因子 b 后，画质明显提升；傅里叶分析显示**增大 b 会压制生成图的高频分量**，说明放大 backbone 特征等价于增强去噪能力。
- **skip-connection 主要往解码器灌"高频"**：skip 把编码器早期层的特征直连到解码器，傅里叶谱（图 7）显示这些特征**以高频信息为主**；而单独缩放 skip 因子 s（图 5）对画质几乎没影响。作者推测：训练时这些高频 skip 特征会"加速解码器收敛到噪声预测"，**但推理时却会喧宾夺主、削弱 backbone 固有的去噪能力**，导致异常细节/伪影。

定位：FreeU 不是新模型也不是新训练目标，而是一个**即插即用的推理时特征重加权（feature re-weighting）模块**，与 [[controlnet]]、[[dreambooth]]、[[latent-consistency-models]]（LCM）、ScaleCrafter 等并行使用。它属于"挖掘已训练扩散网络潜力"这一脉络，但走的是最轻量的一端——和需要蒸馏/微调的加速或质量增强方法（[[lcm-lora]]、ADD）截然不同，是真正的"免费"。

## 模型架构
FreeU **不引入任何新网络结构**，它是在现有 U-Net 解码器"concat 之前"插入两个特征调制算子。设解码器第 l 个 block：`x_l` 为来自上一层主干的 backbone 特征，`h_l` 为对应 skip-connection 传来的特征。

**(1) Backbone 特征放大 — 结构相关缩放（structure-related scaling）**
不是对 backbone 特征整体乘一个常数，而是按样本自适应：先沿通道维求均值特征图 `x̄_l`（论文式 4），再 min-max 归一化得到逐空间位置的 backbone 因子图

```
α_l = (b_l − 1) · (x̄_l − min(x̄_l)) / (max(x̄_l) − min(x̄_l)) + 1
```

由于 `x̄_l` 本身携带结构信息（图 8 可视化证实），用它来引导放大可让"加强在结构区域、避免无差别放大"，从而缓解过度放大导致的**纹理过平滑（oversmoothing）**。关键 trick：**只对前一半通道施加放大**（论文式 5：`i < C/2` 时乘 α_l，否则不动），因为对全部通道无差别放大会牺牲高频细节、造成过平滑。

**(2) Skip 特征频域抑制 — 谱调制（spectral modulation）**
为进一步对冲"增强去噪带来的纹理过平滑"，对 skip 特征做傅里叶域低频抑制：

```
F(h_l,i) = FFT(h_l,i)
F'(h_l,i) = F(h_l,i) ⊙ β_l,i          # 频域掩码逐元素相乘
h'_l,i = IFFT(F'(h_l,i))
```

掩码 `β_l,i` 在阈值半径 `r_thresh` 以内取 `s_l`（<1，衰减低频），以外取 1（论文式 9）。直觉：skip 已被证明主要贡献高频，但其携带的低频成分会和 backbone 的去噪目标冲突，故选择性削弱 skip 的低频。

**最后**把调制后的 `x'_l`（主干放大）与 `h'_l`（skip 谱调制）拼接，送入后续层（图 4）。

**官方参考实现的若干工程细节**（来自 GitHub `Free_UNetModel`，比论文更具体）：
- 只在**解码器前两个 stage**生效，按通道宽度判定：`h.shape[1]==1280` 用 (b1, s1)，`h.shape[1]==640` 用 (b2, s2)；对应分别放大前 640 / 前 320 个通道（即"前一半通道"）。
- `Fourier_filter` 用的是 **方形中心窗 + threshold=1**（在 FFT shift 后的频谱中心 `±1` 像素的小窗内乘 scale），即只压制极低频的中心区域——这是论文式 9 radial 阈值的离散方形近似。
- 因此实际暴露给用户的是 **b1/b2/s1/s2 四个标量**（论文叙述时简化为 b、s 两类因子）。

无 text encoder / VAE / tokenizer 方面的改动——FreeU 完全寄生在宿主扩散模型（如 SD 的 CLIP text encoder + VAE）之上，对它们零侵入。

## 数据
**不适用 / 无训练数据**。FreeU 是纯推理时方法，**不训练、不微调、不引入任何数据集**。论文也未构建新数据集；所有实验都直接复用宿主模型（SD/SDXL/ModelScope/DreamBooth/ReVersion/Rerender）官方权重与官方设定，仅在推理阶段插入两个缩放因子。傅里叶域的分析样本来自 SD 自身的生成过程（如 "A squirrel eating a burger" 等 prompt 的逐步去噪可视化）。

## 训练方法
**无训练**。这正是 FreeU 的卖点——"no training, no fine-tuning, no additional parameters"。方法全部发生在**推理（inference）阶段**：在每个采样步、U-Net 解码器前两 stage 的 concat 之前，执行上述 backbone 放大 + skip 谱调制。因此不涉及任何 diffusion / flow-matching / 蒸馏的训练目标，也没有 SFT/RLHF/DPO/reward model。

**唯一的"超参"是 b1/b2/s1/s2**，需按宿主模型与风格手调。GitHub 给出的官方推荐值（s1=0.9、s2=0.2 在各模型一致）：

| 模型 | b1 | b2 | s1 | s2 |
|---|---|---|---|---|
| SD1.4 | 1.3 | 1.4 | 0.9 | 0.2 |
| SD1.5 | 1.5 | 1.6 | 0.9 | 0.2 |
| SD2.1 | 1.4 | 1.6 | 0.9 | 0.2 |
| SDXL  | 1.3 | 1.4 | 0.9 | 0.2 |

官方建议的可调范围：`1 ≤ b1 ≤ 1.2`、`1.2 ≤ b2 ≤ 1.6`、`s1 ≤ 1`、`s2 ≤ 1`（注：README 给的 b1 推荐表值与"范围"略有出入，作者明确说参数可按模型/风格/任务自行调整）。

## Infra（训练 / 推理工程）
- **训练 infra：无**（不训练，无 GPU·时 / 并行 / 混精相关披露）。
- **推理开销：近乎零**。FreeU 只多做两次轻量操作——逐通道求均值 + min-max 归一化（O(特征大小)）、以及对 skip 特征的一次 FFT/IFFT。论文反复强调"no increase in memory or sampling time"，即不增加显存、不增加采样步数与时延。
- **部署形态**：作为几行代码 patch 进宿主 U-Net 的 `forward`。官方提供 Gradio demo（`demos/app.py`）与 HF Space。MIT License。社区已把它集成进 **Diffusers（`pipe.enable_freeu(s1,s2,b1,b2)`）、ComfyUI、WebUI** 等几乎所有主流推理框架，并被验证可叠加 ControlNet / LCM / ScaleCrafter（4096×4096 SDXL 超分生成）等。

## 评测 benchmark（把效果讲清楚）
FreeU 论文是一篇**以可视化 + 人评为主、未报告自动指标**的方法论文。需要明确：

- **未报告 FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / VBench 等任何自动量化指标**。论文正文与附录均无这些数字，源里没有就不编。
- **唯一的量化结果是用户研究（35 名参与者，同 seed 配对对比、随机顺序消偏）**：
  - 文生图（Table 1，SD vs SD+FreeU 的偏好票占比）：**图文对齐 14.12% : 85.88%；画质 14.66% : 85.34%**——绝大多数票投给 FreeU。
  - 文生视频（Table 2，ModelScope vs ModelScope+FreeU）：**视频-文本对齐 15.29% : 84.71%；视频质量 14.33% : 85.67%**。
- **定性覆盖范围很广**：SD1.4 / SDXL 文生图、ModelScope 文生视频、[[dreambooth]] 个性化、ReVersion 关系反演、Rerender 视频到视频翻译，以及项目页额外展示的 ControlNet、LCM、ScaleCrafter（4096×4096）。典型修复案例：消除"蓝色汽车"屋顶伪影、"母兔抚育幼兔"正常体态、ModelScope"卡通大象"两条象鼻被纠正为一条、ReVersion"狗在篮子里"去伪影等。

**关键消融（傅里叶 + 特征可视化驱动，图 15–18）**：
1. **FreeU 的去噪本质**：图 15 显示加 FreeU 后，去噪每一步的高频分量都被进一步压制——印证 FreeU 增强了去噪；图 16 显示 FreeU 的特征图含更明显的结构信息。
2. **b vs b&s（组件消融，图 17）**：只加 backbone 因子 `b` 已显著改善细节，但有时纹理过平滑；再加 skip 因子 `s`（b&s）能减低频、缓解过平滑，得到更真实的结果（如 synthwave 落日天空更自然）。
3. **常数缩放 vs 结构相关缩放（图 18）**：用固定常数放大 backbone 虽提升画质，但会**严重过平滑 + 颜色过饱和**；改用 structure-related 的逐位置因子图 α_l 后，二者皆缓解，细节更生动。
4. **半通道放大**：对全部通道无差别放大会过平滑；只放大前一半通道是必要 trick（论文式 5）。

## 创新点与影响
**核心贡献**：
1. **首次系统剖析扩散 U-Net 内部分工**——用傅里叶域视角证明 backbone 主管去噪、skip 主管高频注入，且 skip 高频在推理时会反噬去噪能力。这是一个被后续大量工作引用的"机理性"洞见。
2. **提出极简的推理时重加权方法 FreeU**：backbone 结构相关放大（仅半通道）+ skip 傅里叶低频抑制，免训练、零参数、零额外开销。
3. **极强的通用性与落地度**：对 SD/SDXL/ModelScope/DreamBooth/ReVersion/Rerender 全适用，几行代码集成，被 Diffusers/ComfyUI/WebUI 等几乎所有推理栈原生支持，成为社区"标配"质量开关之一。CVPR 2024 Oral。

**影响**：FreeU 把"扩散 U-Net 内部 skip/backbone 频率特性"这一分析范式带火，催生了一批"训练-free 调制 U-Net 特征/频谱"的后续工作；它本身因"近乎零成本即提质"被广泛默认开启，是推理侧 free-lunch 类技巧的代表作。

**已知局限**：
- **b1/b2/s1/s2 需手调**，最优值随模型、风格、prompt、任务而变，没有自适应/自动搜参（README 也坦承"will be updated soon"、给的是经验范围）。调过头会过平滑或颜色失真。
- **缺乏自动量化评测**：仅有小规模（35 人）用户研究，没有 FID/CLIPScore 等可复现的标准指标，效果的客观幅度难精确量化。
- **强绑定 U-Net 架构**：方法依赖 U-Net 的 skip-connection 结构与"1280/640 通道前两 stage"等具体形状假设，对 DiT/MMDiT 等无 skip 的纯 Transformer 扩散骨干不直接适用。
- 改善以"修复伪影、增强细节真实感"为主，**不改变语义/构图能力**，不是对齐或可控性方法。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2309.11497
- arxiv_pdf: https://arxiv.org/pdf/2309.11497
- project_page: https://chenyangsi.top/FreeU/
- github: https://github.com/ChenyangSi/FreeU
- hf_demo: https://huggingface.co/spaces/ChenyangSi/FreeU

## 本地落盘文件
- ../../../sources/omni/2023/arxiv-2309.11497.pdf
- ../../../sources/omni/2023/freeu--project-page.md
- ../../../sources/omni/2023/freeu--github-readme.md
