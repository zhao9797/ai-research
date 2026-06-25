---
title: "横向综述 · 数据：规模 · 配比 · 重标注 · 过滤"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [survey, data, re-captioning, synthetic-data, aesthetic-filter, nsfw, copyright, data-curation, laion, omni]
---

# 数据：规模 · 配比 · 重标注 · 过滤

> 横向综述章节。视觉/多模态生成这一代真正的"暗物质"不在网络结构，而在喂进去的图文对——**它有多大、长什么样、caption 是谁写的、过滤掉了什么、各阶段怎么配比**。本章把 2020→2026 的数据工程拉成一条线：从抓 alt-text 堆规模，到 LAION 公开化，到 [[dall-e-3]] 掀起的 re-captioning 浪潮，到合成数据与美学/安全/版权过滤的体系化，最后落到 [[qwen-image]]/[[ernie-image]] 把"分阶段配比"做成一等公民。核心判断：**到 2023 年起，数据质量（而非参数量或结构）成了 prompt-following 的主要抓手**，"谁把数据治理做透谁赢"。

---

## 1. 图文对规模演进：从百万到十亿

**第一阶段（2021，百万级，原生 alt-text）。** 起点是 Google 的 Conceptual Captions——CC3M（约 330 万对）/ CC12M（约 1200 万对），是早期几乎所有工作的公共起跑线。[[dall-e-1]]（OpenAI, 2021-02）把规模直接拉到 **2.5 亿图文对**（对标 JFT-300M，来源 = Conceptual Captions + Wikipedia 图文 + YFCC100M 过滤子集），但预备实验仍只用 CC3M 的 330 万对；它的过滤还很朴素——丢 caption 太短的、用 `cld3` 丢非英文的、丢长宽比不在 [1/2, 2] 的图（否则方形 crop 会裁掉 caption 提到的物体），**无 re-caption、无合成数据**。同期中文侧 [[cogview]]（清华/阿里, 2021-05）用约 **3000 万**中文图文对（约 50% 是英文经机器翻译，含 CC + ImageNet），并坦白"未去水印白边"。这一阶段的共识是：能拿到多少 alt-text 就喂多少，caption 噪声照单全收。

**第二阶段（2021–2022，LAION 公开化，四亿→五十亿）。** [[latent-diffusion-ldm]]（CompVis, 2021-12）的文生图模型在 **LAION-400M**（4 亿 CLIP-filtered 图文对）上训 1.45B 模型，这是 LAION 第一次成为开源 T2I 的事实数据底座。到 [[stable-diffusion-1]]（2022-08）切到 **LAION-2B(en)**（LAION-5B 的英文部分）及其子集，并第一次把"分阶段换数据集"写进 checkpoint 谱系：`v1-1` 先在 laion2B-en 256² 训 237k 步、再在 **laion-high-resolution**（LAION-5B 中分辨率 ≥1024² 的约 **170M** 例）512² 训 194k 步。LAION 的意义不只是规模，更是**可公开复现**（虽然只存 URL 导致 link rot）——这也是它后来被版权诉讼缠身、并催生 [[commoncanvas]] 等"clean data"反向工作的根源。

**第三阶段（2023→2026，各家内部十亿级，规模让位于治理）。** [[imagen]]（Google, 2022-05）已是内部 460M + LAION 400M ≈ **8.6 亿**；[[emu-quality-tuning]]（Meta, 2023-09）内部 **11 亿**图文对预训练。进入 2025–2026，旗舰一律是"数十亿"且**不再以规模为卖点**：[[qwen-image]]（阿里, 2025-08）"系统性收集并标注数十亿图文对，强调质量与均衡分布而非纯堆规模"；[[seedream-4-0]]（字节, 2025-09）"数十亿 text–image 对，跨多样 taxonomy"；[[emu3-5]]（BAAI, 2025-10）干脆把单位换成 **token**——预训练 **>13T 多模态 token**（含约 6300 万条视频、累计约 790 年素材）。**规模曲线在十亿级附近趋平，竞争焦点彻底转向 caption 质量、配比与过滤**——这一拐点的实证由 CommonCanvas 给出（见 §4 的"欠参数化"发现：10M→90M 样本 FID 几乎不再改善）。

---

## 2. Re-captioning 浪潮：把 alt-text 换成模型写的密集描述

这是本章的主轴。问题诊断最早由 [[dall-e-3]] 系统化提出：互联网 alt-text 只描述主体、漏掉背景/数量/位置/颜色/图中文字，甚至直接错误（广告、meme 混进 alt-text）。既然 caption 噪声大，**就用模型重新生成准确详尽的 caption 来训练**，把噪声"averaging"抹平。

**[[dall-e-3]]（OpenAI, 2023-10）——立范式。** 论文标题就叫 *Improving Image Generation with Better Captions*，明确声明"只覆盖 recaptioning 这一条贡献"。做法：先按 CoCa 思路训一个 bespoke captioner（CLIP image embedding 作条件），两轮 fine-tune 出 SSC（短合成 caption，只描述主体）和 DSC（长合成 caption，含背景/图中文字/风格/配色）；再给全量训练集重打 caption。**关键 trick 是混合比例**——100% 合成会让模型过拟合 captioner 的模态偏好（句长、标点、是否总以 "a/an" 开头），消融测了 65/80/90/95%，最终 **95% 合成 + 5% ground-truth**（合成比例越高 CLIP score 单调越好，65% 被砍）。效果是 prompt-following 人评 ELO 拉到 **153.3**，碾压 Midjourney 5.2（-104.8）、SDXL（-189.5），Drawbench long 准确率 81.0% vs DALL·E 2 的 52.4%。配套用 GPT-4 在推理期把用户短 prompt"上采样"成 15–80 词长描述，弥合"训练用长 caption / 用户输入短 prompt"的分布鸿沟。

**[[pixart-alpha]]（华为诺亚, 2023-09）——量化"概念密度"。** 与 DALL·E 3 同期独立提出，并把收益讲成可度量的"信息密度"：LAION 原始 caption 中 2.46M distinct nouns 仅 **8.5%** 有效（出现 >10 次），平均每图 6.4 个名词。用 VLM **LLaVA-7B** 以提示 "Describe this image and its style in a very detailed manner" 重写后，密度跃升——LAION-LLaVA 13.3% / 每图 20.9 名词，**SAM-LLaVA 18.6% / 每图 29.3 名词**（最高密度，故选 SAM 数据集做主力，因其"对象丰富多样"远胜 LAION 的简单产品图）。120 个文本 token（多数工作只 77）正是为承载更密 caption。它把"VLM re-caption + 高密度"做成低成本训练的关键一招，并开源 SAM-LLaVA-Captions10M。

**[[cogview3]]（智谱/清华, 2024-03）——自动造 recaption 数据。** 对标 DALL·E 3 但把"人工标注 recaption 指令"换成 **GPT-4V 自动构造** `<image, old_cap, new_cap>` 三元组（先让 GPT-4V 对图提若干问答、首问强制简要描述，再合成新 caption），共约 **7 万条**，微调 **CogVLM-17B** 得 recaption 模型，再重写整个训练集；替换比例同样 **95%**。这是 re-caption 流水线从"靠人写指令"到"靠强 VLM 自举"的过渡样本。

**[[commoncanvas]]（Cornell/MosaicML, 2023-10）——re-caption 的极端版（0% 原始 caption）。** CC 授权图几乎都没 caption，于是用 **BLIP-2 OPT-2.7B** 给全部 YFCC CC 图生成合成 caption（**纯合成，无任何 ground-truth**），花约 1120 A100·时。意外发现：合成 BLIP-2 caption 的 **CLIP Score 反而高于原始 alt-text**（原始 alt-text 常含 "OLYMPUS+DIGITAL+CAMERA" 这类相机自动垃圾），代价是 caption 多样性（unique trigram）下降。作者把这一模式命名为 **telephoning**——用预训练 captioner 把图像"有损压缩"成文本再喂下游，并据此论证版权"有损压缩"绕开机制（BLIP-2 给 Snoopy 写的 caption 是 "a black and white cartoon dog with black ears"，不含 "Snoopy"）。

**各家 VLM 标注（2025→2026，从"用现成 VLM"到"自训专用 captioner"）。** 到旗舰时代，re-caption 已是标配，且越来越精细：
- [[qwen-image]] 用 Qwen2.5-VL 类 captioner 一次性产出自然语言 caption（含**带引号逐字转写可见文字**）+ 结构化 JSON 元数据（图像类型/风格/水印列表/异常元素），并在 S3 阶段分 Raw / Recaption / Fused 三路 caption（Raw 保留植物名、卡通 IP 等真实世界知识，Recaption 由 Qwen-VL 生成，Fused 融合）。
- [[seedream-4-0]] 训"文本质量分类器"检测原始 caption 低质文本，并"精炼 captioning 模型做更细粒度视觉描述"。
- [[emu3-5]] 视觉-文本对（约 5 亿图文对 + 3000 万视频文本对）用 **Qwen2.5-VL-7B 重新打标**；视频则用 Whisper ASR + Qwen2.5-VL 视觉字幕 + LLM 多模态摘要拼成"关键帧+ASR"交错序列。
- [[ernie-image]]（百度, 2026-05）用微调的 Qwen3 系 VLM 标注，**特别强调忠实识别图内文字**（幻灯片/海报/UI/文档），并提出核心洞察："**在训练早期就喂详细图像描述，不仅强化复杂指令遵循，还显著丰富模型的世界知识**"，因此"不刻意合成领域数据，而走更有针对性的标注策略"。后训练还用更大的 **Kimi K2.5** 把 caption 改写降采样成短关键词/自然语言/指令/详细构图四种风格，**对齐真实用户输入、缓解 captioner 引入的偏置**——这是对 DALL·E 3 "训练/推理分布对齐"问题的数据侧回应。

> 一句话脉络：**alt-text（≤2022）→ VLM 单轮重写（DALL·E 3 / PixArt-α / CommonCanvas, 2023）→ 自训专用 captioner + 多版风格 caption + 逐字文字转写 + 结构化元数据（2025–2026）**。re-caption 从"加分项"变成"不做就出局"。

---

## 3. 合成数据：从 caption 合成到像素合成

re-caption 是"合成文本"，更进一步是"合成像素/受控渲染"，但各家态度分裂：

- **激进派——[[janus-pro]]（DeepSeek, 2025-01）**：直接指出前作真实数据"质量差、噪声大导致文生图不稳、美感差"，引入约 **7200 万合成美学数据**，使统一预训练阶段 **真实:合成 = 1:1**，结论是合成数据让模型**收敛更快、输出更稳、美感显著提升**（合成 prompt 用公开的 Vivym/midjourney-prompts）。
- **保守派——[[qwen-image]]**：合成数据**仅占 5%**，且"明确排除其他 AI 模型生成的图像"，只指**受控文本渲染合成**——团队认为 AI 生成图带伪影、文字畸变、偏见、幻觉风险，会损害泛化。它的文本合成走三策略：纯渲染（动态版式渲染到干净背景，任一字符渲染失败则整段丢弃保字级保真）、组合渲染（文字印到纸/木板再合成进真实背景）、复杂渲染（PPT/UI mockup 程序化替换占位文本）。
- **知识补全派——[[seedream-4-0]]**：为知识中心概念（公式、教学图）专门合成——用 OCR 输出 + LaTeX 源码生成结构与分辨率各异的公式图，拓宽细粒度概念覆盖、缓解 top-down 重采样对自然图像的偏置。
- [[emu3-5]] 也加 FLUX 等开源 T2I 合成图文对，并自建 fully-real / semi-synthetic / fully-synthetic 三类 X2I 编辑数据（约 2735 万样本）。

分歧的本质是"**用 AI 生成图训 AI 会不会模型坍塌/积累伪影**"——激进派赌"合成美学数据信噪比高于网络真图"，保守派把合成严格圈在"文本渲染/公式"这类真实数据稀缺的长尾。

---

## 4. 美学打分过滤：LAION-Aesthetics → 自研美学模型

**LAION-Aesthetics V2（2022）——起点。** [[stable-diffusion-1]] 的 `v1-2` 在 **laion-improved-aesthetics**（laion2B-en 子集，过滤条件：原始尺寸 ≥512²、**美学分 >5.0**、水印概率 <0.5）训 515k 步，`v1-4/v1-5` 进一步用 **laion-aesthetics v2 5+**——这是第一次把"美学打分阈值"写进生产配方。打分器是 LAION-Aesthetics Predictor V2（基于 CLIP embedding + 小回归头），此后成为开源界默认美学过滤工具。

**[[emu-quality-tuning]]（Meta, 2023-09）——把美学对齐独立成阶段。** 提出 **quality-tuning**：在 11 亿对预训练之上，只用 **约 2000 张人工精选极高美学图**做纯 SFT（batch 64、noise-offset 0.1、**≤15K 迭代早停**——过久会过拟合退化通用性），就让模型"只产出高美感图"。数据漏斗：数十亿 → 自动过滤（美学评分 + OCR 字数 + CLIP score + 尺寸/长宽比 + 视觉概念均衡 + 专有点赞信号）降到 200K → 通才标注员优化召回降到 20K → 专家标注员按 5 维摄影原则（构图/光照/色彩对比/主体背景/主观叙事）优化精度选出 2000 张并人工写 caption。**核心论点"质量>数量"的硬证据：仅 100 张图就把对 SDXL 的视觉吸引力胜率从 24.8% 拉到 60.3%**，2000 张达 67.0%；架构无关（LDM/像素扩散/掩码 transformer 通吃）。这把"美学之于 T2I ≈ 指令微调之于 LLM"确立为业界后训练常识。

**[[seedream-3-0]]（字节, 2025-04）——美学进 reward model。** 把美学从"过滤数据"推到"奖励建模"：用 VLM 做生成式 reward model（从 "Yes" token 归一化概率导出奖励），**系统性把 reward model 从 1B 扩到 >20B**，实证 **reward model scaling 的涌现**；偏好评测里美学维度（MPS 13.93 + 内部 Aes 27.68）**首次超过 Midjourney**，HPSv2 首次破 0.3（0.3011）。

**[[ernie-image]]（百度, 2026-05）——自研美学模型 + 去偏基准。** 不再用 LAION-Aes，而是自研 **ERNIE-Image-Aes**（从 8B VLM ArtiMuse 初始化微调），SRCC/PLCC **0.7445/0.7598** 碾压 LAION-AES（0.2944/0.3138）；并系统揭示既有美学预测器的偏置——**LAION-Aes 给 AI 生成图/随手拍打高分**，ArtiMuse/UniPercept 偏好黑白照片。配套发布 **ERIA-1K** 基准（1000 图，6 类别按真实世界分布配比：摄影 49.28% / 插画动漫 23.16% / 平面海报 11.14% / 混合网图 10.44% / 胶片 5.42% / 产品 0.56%，由央美/川美/中传背景标注者标），并用**瑞士轮（Swiss-system tournament）成对比较**替代有 score drift 的 Likert 绝对评分和需海量对比的 ELO。美学打分至此从"一个 CLIP 回归头"演化为"工业级美学评估基建"。

---

## 5. 安全 / NSFW / 版权过滤

**版权干净数据的两条代表路线。** [[adobe-firefly]]（Adobe, 2023-03）走"**商业版权安全**"——只在 Adobe Stock 授权图（数亿张）+ 公开授权内容 + 版权过期公共领域内容上训，明示 "We do not mine the web or video hosting sites for content"，从不训练用户内容，并对 Adobe Stock 贡献者给训练补偿（Firefly Contributor Bonus，业内首创"训练数据付费"），输出默认写入 Content Credentials（C2PA）。代价是数据多样性受限、技术全程闭源（无论文/权重/benchmark）。[[commoncanvas]] 走"**纯 Creative-Commons**"——CommonCatalog 数据集只含 CC 授权图（商用子集 C ≈2632 万、含非商用 NC ≈6702 万），明确排除约 3000 万 ND 非衍生许可图，从 YFCC100M 按 Flickr ID 重抓 4K 高分辨率原图；最大的 CommonCanvas-LNC（SDXL U-Net）在 PartiPrompts 人评与 SD2-base **无统计学显著差异**，却只用 <3% LAION 数据量。它的副产品发现极重要——**扩散模型被严重欠参数化**：在 LAION 上 10M→90M 样本 FID/KID 几乎不再改善，约 7000 万 CC 图足够"饱和" SD2，**这从数据角度解释了为何 §1 的规模曲线会趋平**。

**NSFW / 偏见过滤的反直觉教训。** [[dall-e-3]] 系统卡有一个反常识改动：**调低了笼统过滤器的阈值**，改用针对细分子类（露骨性化、仇恨图像）的精确过滤器——因为笼统过滤器把大量女性图像误删，反而**加重了模型对女性生成的偏置**；放宽后既扩大可用数据又减轻偏置。它还用 Microsoft Cognitive Service 打分 + 1024 张人工校准阈值 + cut-paste 数据提升对小面积冒犯区域的召回。早期工作（[[stable-diffusion-1]]）则坦承"含成人内容、未去重、存在记忆化"，安全主要靠推理期 Safety Checker。

**"缺陷即丢弃 → 局部屏蔽梯度"的数据回收。** [[seedream-3-0]] 的 **defect-aware training** 是过滤范式的一次重要反转：2.0 严格丢弃含水印/叠字/字幕/马赛克的图（约占原始数据 **35%**），3.0 改为训一个缺陷检测器（基于 active learning 挑选的 15000 条人工标注样本）定位缺陷 bbox，当缺陷面积 <图像 20% 时保留这些原本被弃的图，并**在 latent 空间用空间注意力掩码屏蔽缺陷区域的梯度**——使**有效训练数据扩增 21.7%**。从"过滤=删图"到"过滤=局部屏蔽"，是数据稀缺压力下的精细化。

---

## 6. 分阶段数据配比：把"什么阶段喂什么数据"做成显式课程

到 2025–2026，旗舰把数据配比从"隐式经验"升级为"显式、可消融的课程"。

**[[pixart-alpha]] 的三阶段分解（早期范式）。** 把 T2I 拆成三个子任务、各配最匹配的数据与算力：Stage1 像素依赖（1M ImageNet 类条件，学自然图像分布）→ Stage2 文本-图像对齐（**10M SAM-LLaVA** 高密度 caption）→ Stage3 高美学（14M HQ = 4M JourneyDB + 10M 内部数据）。这是"分阶段配比"的源头之一。

**[[qwen-image]] 的 55/27/13/5 域配比（最清晰的横向标杆）。** 数据按四大域显式配比：**Nature 自然 ~55%**（通用域，现实多样性根基）/ **Design 设计 ~27%**（海报/UI/PPT/绘画，文本渲染与版式能力的关键来源）/ **People 人物 ~13%** / **Synthetic 合成 ~5%**（仅受控文本渲染，排除 AI 生成图）。配合**七阶段过滤流水线 S1–S7**（随训练推进逐步收紧，合成数据从 S4 引入）：S1 初筛去 NSFW/低分辨率 → S2 画质（清晰度/亮度/熵/纹理）→ S3 图文对齐（Chinese-CLIP + SigLIP 2 过滤错配）→ S4 文本渲染增强 → S5 高分辨率精修（去水印/二维码/条码）→ S6 类别均衡与肖像增强 → S7 均衡多尺度训练（WordNet 启发的层级分类，对文本渲染数据重采样应对 token 长尾）。课程沿分辨率（256→640→1328）、文本（无→有→段落级）、质量（海量→精炼）、分布（不均衡→均衡）四轴渐进。GenEval 由此 SFT 0.87 → RL 0.91（榜上唯一破 0.9 的基础模型），中文 ChineseWord 总分 58.30 碾压 GPT Image 1（36.14）。

**[[ernie-image]] 的"自底向上挖掘 + 层级采样"（数据挖掘 > 参数 scaling）。** 主张用 8B 小模型 + 数据工程逼近闭源旗舰：训一个图像分类器把每张图归入 **10,000 个细粒度视觉类别**作为均衡的语义划分，用 ERNIE-Image-Aes 给全部图打美学分，再做**两级层级采样**——类间权重由"语料规模 + 聚合美学质量"联合决定（防高频类主导、给高质类更多概率），类内按美学分采样让高质样本更频繁。后训练 SFT 反过来用"自顶向下"——先圈定海报/游戏截图/人像/产品/动漫等高需求品类，再精挑高一致性数据。这套"bottom-up 挖掘 + top-down 精修"+ 稳定化 DPO（anchor loss）+ MT-DMD 蒸馏，让 8B 的 GenEval **0.8856 居榜首**、人评开源第一，**实证了"细粒度数据挖掘可替代参数堆叠"**。

**其它配比信号。** [[seedream-3-0]] 的**双轴协同采样**——视觉侧用层次聚类保证视觉模式均衡、语义侧用 TF-IDF 解决描述长尾；[[emu3-5]] 给出最细的多模态采样比（视频交错 0.55 为最核心，纯文本约 3T token 保语言能力，SFT 按 General 29.7B / X2I 56.2B / 视觉叙事 10.1B 等任务分配）。

---

## 7. 一条容易被忽略的支线：用"尺寸/裁剪条件"代替"丢小图"

数据过滤不止"删什么"，还有"怎么不删"。[[sdxl]]（Stability AI, 2023-07）发现按 256² 阈值丢小图会丢掉 **39%** 训练数据，于是提出 **size-conditioning + crop-conditioning**：不丢小图，而是把原始尺寸、裁剪坐标作为标量条件（Fourier 编码后加到 timestep embedding）喂进 U-Net，既回收了被丢的数据，又消除了随机裁剪的伪影泄漏。这与 §5 Seedream 的"缺陷局部屏蔽"是同一思路的两个版本——**在数据稀缺压力下，把"硬过滤"换成"软条件化"**，是数据工程贯穿始终的隐线。

---

## 小结：数据这条线的三个拐点

1. **2021–2022 规模拐点**：alt-text 堆到 LAION-400M/2B/5B，开源界有了公共底座，但 caption 噪声照单全收。
2. **2023 质量拐点**：[[dall-e-3]] / [[pixart-alpha]] 用 VLM re-caption 证明"数据质量 > 结构"，[[emu-quality-tuning]] 证明"2000 张精图就能做美学对齐"，[[commoncanvas]] 证明"扩散模型欠参数化、<3% LAION 就饱和"——三者合力把竞争从"堆规模"逼向"治数据"。
3. **2025–2026 体系化拐点**：[[qwen-image]]（55/27/13/5 + 七阶段过滤）、[[ernie-image]]（10k 类挖掘 + 层级采样 + ERIA-1K 去偏美学）、[[seedream-4-0]]（知识数据重构）把"规模/配比/重标注/过滤"做成可消融、可复现的工业流水线，并把自研 captioner、自研美学模型、合成文本/公式渲染、缺陷回收全部内化为标准件。

贯穿全程的隐线：**当规模收益趋平（CommonCanvas 的欠参数化发现），治理成为唯一仍在涨点的杠杆**——re-caption 治"图文对齐与世界知识"，美学过滤治"默认观感"，安全/版权过滤治"可商用性"，分阶段配比治"训练效率与长尾覆盖"。这四者的合力，就是 2026 年开源模型能用 8B 参数（[[ernie-image]]）逼平闭源旗舰的根本原因。
