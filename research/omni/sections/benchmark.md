---
title: "评测 benchmark 演进与横向数字"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [benchmark, evaluation, fid, clipscore, geneval, dpg-bench, t2i-compbench, hpsv2, imagereward, pickscore, mjhq-30k, arena-elo, lmarena, ocr-text-render, gedit, magicbrush, imgedit, vbench, movie-gen-bench, wise, omni, survey]
---

# 评测 benchmark 演进与横向数字

> 一句话主线：视觉生成的"标尺"在 6 年里换了四代——**像素分布距离（FID/IS）→ 文图相似度（CLIPScore）→ 可验证的组合性/对齐（GenEval/T2I-CompBench/DPG）→ 学到的人类偏好（ImageReward/HPSv2/PickScore）→ 群体盲评 ELO（LMArena/AA Arena）**，并向编辑、视频、统一三个新战场扩张，最终在 2026 年由 [[qwen-image-bench]] 把目标从"generation（对齐）"重定义为"creation（创作）"。每换一代，都是因为上一代**与人评脱节、或被前沿模型刷饱和**。

---

## 0. 为什么标尺一直在换：FID 与人评的脱节是贯穿全程的暗线

判断一个指标好不好，硬标准是"它与人类偏好排序的相关性"。这条暗线把整部演进史串了起来：

- [[raft-reward-diffusion]]（ImageReward，2023-04）用 6 个 T2I 模型做 Spearman 相关性实测，给出最刺眼的一组数字：**zero-shot FID 对人评排序 ρ=0.09（几乎不相关）**，CLIP Score ρ=0.60，而学到的奖励模型 ImageReward ρ=1.00。这直接宣判了 FID 作为 T2I 横向标尺的死刑。
- [[sdxl]]（2023-07）从另一侧印证：SDXL 的 COCO zero-shot FID **反而是 SD 1.5/2.1 三者中最差**，CLIP-score 也只略升，但人评碾压前代——作者据此明确写"不要用 COCO FID 给文生图基座排座次"。
- 到 2024–2026，几乎所有顶级闭源模型（[[flux-1-kontext]]、[[hunyuanimage-3-0]]、[[gemini-2-5-flash-image-nano-banana]]、[[seedream-4-0]]、[[qwen-image-2-0]]）**主动拒报 FID/CLIPScore/GenEval**，改用自建基准 + 盲评 ELO，理由都是"自动指标与人评脱节、且已饱和"。

所以下面每一代标尺的诞生，本质都是在补"上一代与人评脱节"的洞。

---

## 1. 第一代：FID / IS —— 像素分布距离（2020–2022，无文本条件）

这一代评的是"生成分布像不像真实分布"，与文本对齐无关，主战场是无条件/类别条件的 CIFAR/ImageNet/LSUN/COCO。

- [[ddpm]]（2020-06）用 **CIFAR-10 无条件 FID=3.17、IS=9.46** 首次证明扩散能达 GAN 级质量（同期 StyleGAN2+ADA FID 2.67 仍微弱领先，但 DDPM 已超 BigGAN-deep 有条件的 14.73）。
- [[diffusion-models-beat-gans]]（ADM，2021-05）靠 classifier guidance 在 **ImageNet 256² 把 FID 推到 4.59，+ADM-U 到 3.94；512² 到 3.85**，全面反超 BigGAN-deep（256² 6.95 / 512² 8.43），且 recall（多样性）从 0.28/0.29 提到 0.52/0.53——这是"扩散打败 GAN"的标志数字。
- 文本条件时代由 **COCO zero-shot FID-30K** 接棒做 T2I 标尺：[[imagen]]（2022-05）刷到 **7.27**（超 DALL·E 2 的 10.39、GLIDE 的 12.24）；自回归路线 [[parti]]（2022-06）用 20B 参数追平到 **zero-shot 7.23 / finetuned 3.22**，并给出 350M→20B 的 FID 单调下降 scaling 证据（350M=14.10 → 3B=8.10 → 20B=7.23）。

**这一代的崩塌**：COCO FID 既不反映文图对齐，又（如 SDXL 案例）与人类美学负相关，于是 2023 年起被两路新标尺取代。

---

## 2. 第二代：CLIPScore —— 文图相似度（2021– ，过渡指标）

CLIPScore（文本嵌入·图像嵌入余弦相似度）补上了 FID 不看文本的洞，成为 2021–2023 的标配过渡指标，但它只看"全局语义对不对得上"，对计数/位置/属性绑定等组合细节钝感（ImageReward 实测 CLIP Score 对人评 ρ 仅 0.60）。它从未独立支撑横向排序，更多是和 FID 配对画 Pareto 曲线（如 [[imagen]] 的 CLIP-FID Pareto 论证"放大 T5 文本编码器 > 放大 U-Net"）。CLIPScore 的真正归宿是被吸收进后续基准的子指标（如 CVTG-2K 的文图对齐列、HPS 的 backbone）。

---

## 3. 第三代：组合性 / 对齐基准 —— 可验证的细粒度对齐（2023–2025 主力）

这一代用"目标检测器/VQA 模型自动判定 prompt 里的物体、数量、颜色、空间关系是否被正确生成"，把"对齐"变成**可验证、可分项归因**的分数。三大标尺：

### GenEval（6 维：单物体/双物体/计数/颜色/位置/颜色绑定，0–1）
用 Mask2Former 检测器逐项验证，是 2023 起最被广泛引用的对齐榜。关键里程碑（数字均引自各页）：

- 专用扩散把基线立起来：[[stable-diffusion-3]]（2024-03）8B 旗舰 **0.74（1024²+DPO）**，超 [[dall-e-3]] 的 **0.67**（SDXL 仅 0.55、SDXL-Turbo 0.55）。SD3 还给出关键的数据消融——50/50 原始+合成 caption 把 d=15 模型从 **0.43 提到 0.50**（Color Attribution 11.75→24.75、Position 6.50→18.00）。
- 统一/自回归模型一路追平并反超扩散专用：[[janus]]（2024-10）1.3B 即 0.61；[[emu3]]（2024-09）裸 prompt 0.54、加 rewriter **0.66**（DPO 后自动指标反降到 0.64，与人评背离）；[[janus-pro]]（2025-01）7B **0.80**，正面超 DALL·E 3/SD3。
- 2025 进入"破 0.9"时代：[[qwen-image]]（2025-08）SFT 0.87、**经 Flow-GRPO 强化学习推到 0.91**（榜上唯一破 0.9 的基础模型，Counting 0.93/Two-Object 0.95）；统一模型 [[omnigen2]]（2025-06）仅 4B 可训练参数靠 RL 把 base 的 0.78 拉到 **0.95**（超 [[bagel]] 0.88、[[uniworld-v1]] 0.84）。注意：高分高度依赖 LLM prompt rewriter 与 RL 对齐，且 [[uniworld-v1]] 已批评"GenEval 强行绑定罕见共现物体"——这是它开始饱和的信号。

### T2I-CompBench（颜色/形状/纹理/空间/非空间/复杂，6 子项）
专攻"属性绑定 + 复杂组合"。[[pixart-alpha]]（2023-09）首个把 DiT 用于 T2I，仅 753 A100-days 就在 6 子项 **5 项取全表最优**（Texture 0.7044 大幅领先，对 SDXL 6 项全胜）；[[dall-e-3]] 报 T2I-CompBench Colors **81.1% / Shape 67.5% / Texture 80.7%**（远超 SDXL 的 59.2/54.7/63.7）。

### DPG-Bench（dense prompt，1065 条长描述，Overall 0–100）
补 GenEval/CompBench"prompt 太短"的洞（[[qwen-image-bench]] 指出 T2I-CompBench/HRS 平均 prompt 仅 12.65/16.43 token）。横向数字：[[qwen-image]] **88.32**（超 GPT Image 1 的 85.15、HiDream-I1 的 85.89）；统一模型 [[x-omni]]（2025-07）靠 GRPO 拿 **87.65 取统一模型 SOTA**（超 GPT-4o 86.23、[[bagel]] 85.07、[[janus-pro]] 84.19、专用 FLUX.1-dev 84.00）；[[metaqueries]] 的 MetaQuery-XL 82.05。

### 美学侧的 MJHQ-30K（30K Midjourney 精选图算 FID）
[[playground-v2]]（2023-12）提出，用"在 Midjourney 高美学图上的 FID"逼近人类美学偏好（v2 整体 FID 7.07 优于 SDXL-refiner 9.55，且 FID 排名与人评一致），被 [[pixart-sigma]]、[[sana]]（DC-AE rFID 0.34）等大量沿用为美学/重建标尺。

---

## 4. 第四代：人类偏好奖励模型 —— 把"好不好看"学成可微分数（2023– ）

这一代直接训一个模型去拟合人类的成对偏好，既当评测指标又当 RLHF 奖励信号，是后续 DPO/GRPO 对齐的基础设施。三大标尺（"偏好三标尺"）：

- [[raft-reward-diffusion]]（ImageReward，2023-04）：**首个通用 T2I 偏好奖励模型**，BLIP backbone + 137k 专家对训练，偏好预测准确率 **65.14%**（CLIP 54.82/Aesthetic 57.35/BLIP 57.76）；并提出 ReFL，把奖励梯度直接反传进扩散微调，ReFL 后的 SD v1.4 人评胜率 **58.4%**。
- [[hps-v2]]（HPSv2，2023-06）：OpenCLIP ViT-H/14 末段层微调 + 798k 对去偏数据（HPD v2，含 9 个不同模型 + COCO 真实图），偏好预测准确率 **83.3%**，超 PickScore（79.8%）、HPS v1（77.6%）、ImageReward（74.0%）；并定义"4 风格×800 prompt"的稳定打榜协议。v2.1 进一步到 84.1%。
- PickScore（Pick-a-Pic 数据，38k prompt/584k 对）：在偏好三标尺中常作第三方对照，HPSv2 实测其 HPD v2 准确率 79.8%。

三者的本质局限：单一奖励模型代表不了人类审美多样性，且"奖励黑客"风险高——[[omnigen2]] 的消融直接示范了用 HPSv3 当奖励会把感知质量 PQ 刷到 8.22 但语义一致性/IC 崩溃（典型 reward hacking），故它刻意改用准确性奖励（GenEval/EditScore）。

---

## 5. 第五代：群体盲评 ELO —— 用规模化盲投票当终极标尺（2024– ，闭源主战场）

当奖励模型也会被刷、且前沿闭源模型拒报自动指标，群体盲评 ELO（用户匿名二选一投票，按 Elo 排名）成为事实上的"终极裁判"。两大平台：**LMArena**（含图像编辑 Arena）与 **Artificial Analysis（AA）Image Arena**。横向 ELO 快照：

- T2I：[[seedream-3-0]]（2025-04）发布即 AA Arena **ELO 1158（17K 对局）登顶**，超 GPT-4o/Imagen 3/MJ v6.1/FLUX1.1 Pro；[[qwen-image]] 作为唯一开源模型在自家 AI Arena 列第三（落后 Imagen 4 Ultra 约 30 Elo）；[[qwen-image-2-0]]（2026-02）LMArena **ELO 1168，全球第 9、中文第 1，超 Nano Banana**。
- 编辑：[[gemini-2-5-flash-image-nano-banana]]（Nano Banana，2025-08）发布即登顶 LMArena 图像编辑榜，落盘快照 **Elo 1296、累计 1085 万票**（得票遥遥第一，是 FLUX.1 Kontext Pro 642 万票的近 2 倍），把 AI 编辑推向消费级出圈；其前代 Gemini 2.0 Flash 仅 1081（+215 Elo 的跨代跃升）。
- 滚动榜的残酷迭代：[[gemini-3-pro-image-nano-banana-pro]]（Nano Banana Pro，2025-11）AA T2I Arena **Elo 1219**（领先 Seedream 4.0 的 1193），但数月内即被 Nano Banana 2（Gemini 3.1 Flash Image，1255/1387）、GPT Image 2、MAI-Image-2.5 等追平/超越——"发布即 SOTA、随后被次代刷掉"是这条榜的常态。

ELO 的代价：不可分项归因、依赖巨量众包流量、对小厂/开源不公平，且评的是"整体偏好"而非"是否真的对"。

---

## 6. 专项战场（一）：文字渲染 —— 中英 OCR / CVTG（2024– 爆发）

文字渲染长期是"AI 通病"，2024 起成为独立硬指标，用 OCR（GOT-OCR2.0/PaddleOCR/Qwen2.5-VL）算字符准确率/编辑距离。这是中文模型集中发力、且区分度极高的赛道：

- [[qwen-image]] 把它做成 SOTA 护城河：中文 ChineseWord 总分 **58.30**（Level-1 字准确率 97.29%）**碾压 GPT Image 1（36.14）与 Seedream 3.0（33.05）**；LongText-Bench-ZH **0.946**（榜首）、EN 0.943；CVTG-2K（英文）Word Accuracy 0.8288 / NED 0.9116，与 GPT Image 1 相当。
- 统一模型 [[x-omni]]（2025-07）成为**首个能精确渲染长文本的统一模型**：OneIG 文字渲染英文 0.901/中文 0.895（超 GPT-4o 的 0.857；开源统一模型 [[bagel]] 仅 0.244、Show-o2 0.002）；LongText-Bench 中文 0.814 大幅领先所有其他模型（GPT-4o 仅 0.619）。
- [[qwen-image-bench]] 用方差证据盖章：L3 层**区分度最高的 facet 第一名就是 Text Accuracy**，L2 层方差最高的是 Text Rendering——文字渲染是当前前沿模型分化最剧的轴之一。

---

## 7. 专项战场（二）：图像编辑 —— GEdit / MagicBrush / ImgEdit（2023– ）

编辑评测要同时量"指令是否执行（语义一致 SC）"与"非编辑区是否保住（感知质量 PQ）"，靠 GPT-4.1/VIEScore 等 MLLM 评判：

- 早期 [[magicbrush]]（2023-06）提供首个人工标注的指令编辑数据集做基准基线。
- **GEdit-Bench** 由 [[step1x-edit]]（2025-04）提出（606 真实 Reddit 用户指令、中英双语、GPT-4.1+Qwen2.5-VL-72B 双评），迅速成为编辑横向标尺。GEdit-Bench-EN Overall（G_O）横向：[[qwen-image-edit]] **7.56**（SC 8.00/PQ 7.86）领先；[[omnigen2]] 7.21（超 Gemini-2.5-Flash-Image 7.10）；[[bagel]] 6.52（与 Step1X-Edit 持平）；GPT-4o 7.53、Gemini-2.0-Flash 6.32。Step1X-Edit 自身从 v1.0 的 6.44 迭代到 v1.2(thinking+reflection) 的 **7.58**。
- **ImgEdit**（9 类编辑/734 测例，1–5 分）：[[qwen-image-edit]] 总分 **4.27**（略超 GPT Image 1 High 的 4.20）；[[uniworld-v1]] 仅 2.7M 训练样本拿 3.26（超 BAGEL 3.20、Step1X-Edit 3.06）；[[omnigen2]] 3.69。
- 闭源 [[flux-1-kontext]]（2025-05）则又拒报通用指标，自建 **KontextBench（1026 对真实众包 image-prompt）**，重申现有 InstructPix2Pix/MagicBrush/Emu-Edit/GEdit "真实分布覆盖不足"。

---

## 8. 专项战场（三）：视频 —— VBench / Movie Gen Bench（2023– ）

视频比图像更难自动评，FVD/IS 与人评几乎不相关（[[movie-gen]] 明确论证），故分裂成两路：

- **VBench**（多维自动指标：主体一致性/动态程度/多物体/美学等）：开源视频的主战场。[[wan-2-1]]（2025-03）14B 以 **VBench 总分 86.22% 登顶**，超 Sora（84.28%）、HunyuanVideo；[[emu3]] 作为唯一自回归选手 VBench 80.96 超多数开源扩散模型；[[cogvideox]]（2024-08）5B 取多项开源 SOTA。注意 [[hunyuan-video]] 等部分顶级模型**主动不报 VBench**，只给人评。
- **Movie Gen Bench**（[[movie-gen]] 自建，1000 prompt，3× 于前作）+ **人评净胜率（net win rate = win%−loss%）**：闭源/大模型偏好这条路。[[movie-gen]] 30B 对 Runway Gen3 总体净胜 **+35.0%**、对 Sora +8.2%、与 Kling1.5 持平，并用净胜率证明 LLaMa3 骨干优于 DiT（质量 +18.6%、文本对齐 +12.6%）。[[cogvideox]] 用 0/0.5/1 三档人评对闭源 Kling 全维度胜出（总分 **2.74 vs 2.17**）。

---

## 9. 收口：统一理解-生成基准 与 从 generation 到 creation（2025–2026）

统一模型需要专门考"世界知识驱动的生成"和"理解-生成是否真打通"：

- **WISE**（世界知识推理 T2I，6 维：文化/时间/空间/生物/物理/化学，Overall 0–1）：[[metaqueries]]（2025-04）的 MetaQuery-XL 是**首个在 WISE 上超过 SD-3.5/FLUX 等纯 T2I 模型的统一模型**（WiScore 0.55，远超 Janus-Pro 的 0.35）；[[bagel]] 非 CoT 0.52、带 Self-CoT **0.70**（开源最强，仅次于 GPT-4o 的 0.80），并示范"CoT thinking 一致提分"（WISE +0.18、IntelligentBench 44.9→55.3）；[[uniworld-v1]] 0.55（Space 维 0.73 全场第二，仅次 GPT-4o）。
- **[[qwen-image-bench]]**（2026-05）是这条演进的终点站与方法论总结：80 名美院专家 + 13 万+ 标注训出统一裁判 **Q-Judger**（与人类排序 Spearman **ρ=0.92**），把目标从"generation（对齐）"推进到"**creation（创作）**"，新增 Real-world Fidelity 与 Creative Generation 两大应用维度（5 支柱/23 子能力/56 facet）。它用方差证据回答了"为何旧标尺该退场"：**Creative Generation 的组间方差是 Quality 的 11 倍以上**——Quality 已成 table-stakes，创意生成才是分化最剧处；并坚持零 MLLM 自动标注以规避"把一个 MLLM 的世界观规模化复制"的系统性偏差（点名批评 UniGenBench++ 用 Gemini-2.5 既当评估器又当标签源）。

---

## 横向数字表：关键模型 × 关键指标

> 同一指标内可直接比较；跨指标不可。多数 GenEval 高分依赖 LLM prompt rewriter 与 RL 对齐。"—"= 该源未报告该指标（多为闭源拒报或基准尚未出现）。数字均引自对应单工作页（各页已对抗式核过）。

| 模型（年月） | GenEval↑ | DPG↑ | T2I-CompBench / 其他对齐 | 文字渲染（OCR/长文本） | 编辑 GEdit-EN G_O↑ | 偏好/Arena | 源页 |
|---|---|---|---|---|---|---|---|
| DALL·E 3（2023-10） | 0.67 | — | CompBench Color **81.1%** | T5 整词 token，缺字 | — | prompt-follow ELO 153.3 | [[dall-e-3]] |
| PixArt-α（2023-09） | — | — | CompBench 6 项 **5 项最优**（Texture 0.7044） | — | — | COCO FID 7.32 | [[pixart-alpha]] |
| SD3 8B（2024-03） | **0.74**（1024²+DPO） | — | — | — | — | 人评胜 DALL·E 3/MJv6 | [[stable-diffusion-3]] |
| Emu3 8B（2024-09） | 0.66（rewriter） | 80.60 | 超 SDXL/对标 DALL·E 3 | — | — | VBench 80.96（视频） | [[emu3]] |
| Janus-Pro 7B（2025-01） | 0.80 | 84.19 | — | — | — | MMBench 79.2 | [[janus-pro]] |
| MetaQuery-XL（2025-04） | 0.80 | 82.05 | WISE 0.55（首超纯T2I） | — | — | MJHQ FID 6.02 | [[metaqueries]] |
| BAGEL 14B（2025-05） | 0.88 | 85.07 | WISE 0.52→**0.70**(CoT) | — | 6.52 | IntelligentBench 55.3 | [[bagel]] |
| UniWorld-V1（2025-06） | 0.84（rewriter） | — | WISE 0.55 / ImgEdit 3.26 | — | — | 仅 2.7M 训练样本 | [[uniworld-v1]] |
| OmniGen2 4B（2025-06） | **0.95**（RL） | 83.57 | WISE 高 / ImgEdit 3.69 | — | 7.21（超 Gemini-2.5） | OmniContext 7.95 | [[omnigen2]] |
| X-Omni 7B（2025-07） | 0.83（rewriter） | **87.65**（统一SOTA） | — | OneIG-EN 0.901 / LongText-ZH 0.814 | — | 首个统一长文渲染 | [[x-omni]] |
| Qwen-Image 20B（2025-08） | **0.91**（GRPO） | 88.32 | OneIG-EN 0.539 | ChineseWord **58.30** / LongText-ZH 0.946 | — | AI Arena 第三（唯一开源） | [[qwen-image]] |
| Qwen-Image-Edit（2025-08） | 0.91 | 88.32 | — | ChineseWord 58.30 | **7.56**（SC 8.00） / ImgEdit 4.27 | 超 GPT Image 1 High | [[qwen-image-edit]] |
| Step1X-Edit（2025-04） | — | — | — | — | 6.44→7.58（v1.2 think+reflect） | 提出 GEdit-Bench | [[step1x-edit]] |
| Seedream 3.0（2025-04） | — | 88.27 | — | ChineseWord 33.05 | — | AA Arena **ELO 1158** 登顶 | [[seedream-3-0]] |
| HunyuanImage 3.0（2025-09） | 拒报 | 拒报 | 自研 SSAE（持平领先） | hy-OCR 自研 | — | 拒报标准指标 | [[hunyuanimage-3-0]] |
| Nano Banana（2025-08） | 拒报 | 拒报 | — | — | LMArena 编辑 **Elo 1296**（1085万票） | 登顶编辑榜 | [[gemini-2-5-flash-image-nano-banana]] |
| Nano Banana Pro（2025-11） | 拒报 | 拒报 | — | 最强图内文字（官方称） | AA T2I **Elo 1219** | 发布即头部 | [[gemini-3-pro-image-nano-banana-pro]] |
| Qwen-Image-2.0（2026-02） | 拒报 | 拒报 | — | 1K-token 超长/多语种 | 生图编辑二合一 | LMArena **ELO 1168**（中文第1，超Nano Banana） | [[qwen-image-2-0]] |
| GPT Image 2（2026-04→评于 QIBench） | — | — | **Q-Judger Overall 64.69**（五维全第一） | Text Accuracy 强 | — | QIBench 榜首 | [[gpt-image-2]] / [[qwen-image-bench]] |

**读表三条硬结论**：
1. **GenEval 已饱和**：2024 的 SOTA 0.74（SD3）到 2025 的 0.91（Qwen-Image）/0.95（OmniGen2 RL），一年多就把上限刷到天花板，强模型被挤进 0.88–0.95 的窄带，区分力塌缩——这正是 [[qwen-image-bench]] 要换标尺的实证理由。
2. **拒报潮**：2025-09 之后的顶级闭源/部分开源（HunyuanImage 3.0、Nano Banana 系、Qwen-Image-2.0、Seedream 4.0/5.0）**集体拒报 GenEval/DPG/FID**，横向比较只剩盲评 ELO + 自建定性基准，可复现性与可比性双双下降。
3. **中文文字渲染是 2025–2026 最锋利的区分轴**：ChineseWord 上 Qwen-Image 58.30 vs GPT Image 1 36.14（差距 22 分）、LongText-ZH 上 X-Omni 0.814 vs GPT-4o 0.619，远大于 GenEval 上的零点几之差——印证 [[qwen-image-bench]] "Text Rendering 方差最高"的判断。
