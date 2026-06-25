---
title: "中国系文生图/编辑族横向对比：CogView · Qwen-Image · Hunyuan · Seedream · Kolors · ERNIE 及开源诸侯（2021–2026）"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [t2i, image-editing, chinese-text-rendering, mmdit, dit, flow-matching, llm-text-encoder, recaption, seedream, qwen-image, cogview, hunyuanimage, ernie, kolors, hidream, lumina, step1x-edit, comparison]
---

# 中国系文生图/编辑族横向对比

> 本页横向梳理 2021–2026 年六大「中国系」文生图/图像编辑模型族 + 三家开源诸侯，共 21 个工作。主线落在两条贯穿性的中国特色护城河上：**画面内文字渲染（尤其汉字）** 与 **中文语义理解**。每条硬线索都引自对应单工作页（slug 内链，单页已对抗式核过数字）。

覆盖工作（按族归组）：

- **CogView 族（智谱/清华）**：[[cogview]] · [[cogview2]] · [[cogview3]] · [[cogview4]]
- **Qwen-Image 族（阿里通义）**：[[qwen-image]] · [[qwen-image-edit]] · [[qwen-image-2-0]]
- **Hunyuan 族（腾讯混元）**：[[hunyuan-dit]] · [[hunyuanimage-2-1]] · [[hunyuanimage-3-0]]
- **Seedream 族（字节 Seed）**：[[seedream-3-0]] · [[seededit-3-0]] · [[seedream-4-0]] · [[seedream-5-0-lite]]
- **ERNIE 族（百度文心）**：[[ernie-vilg]] · [[ernie-vilg-2]] · [[ernie-image]]
- **单点开源诸侯**：[[kolors]]（快手）· [[hidream-i1]]（智象未来）· [[lumina-image-2-0]]（上海AI实验室）· [[step1x-edit]]（阶跃星辰）

---

## 一、一张大表：时间 / 参数 / 架构 / 关键指标

下表数字全部引自各单工作页（含官方一手源对抗式核过的口径）。"—"表示该工作未披露或不适用。

| 工作 | 时间 | 机构 | 参数/规模 | 架构范式 | 文本编码器 | 训练目标 | 标志性硬指标 | 开源 |
|---|---|---|---|---|---|---|---|---|
| [[cogview]] | 2021-05 | 智谱/清华/DAMO | 4B | VQ-VAE + GPT 自回归 | 序列拼接（无独立编码器）| next-token | 模糊 COCO FID-2 **13.9**（DALL-E 45.5）| ✅ |
| [[cogview2]] | 2022-04 | 智谱/BAAI | 6B（系统 6B-9B-9B）| 分层自回归 + LoPAR | icetk 双语序列拼接 | 掩码 next-token | COCO 微调 FID-0 **17.5**；高分前向 3600→6 | ✅ |
| [[cogview3]] | 2024-03 | 智谱/清华 | 3B | 中继扩散级联 UNet | 冻结 T5-XXL（225 tok）| DDPM + relay | 人评 vs SDXL **77.0%** 胜；蒸馏 **1.47s** | ✅ |
| [[cogview4]] | 2025-03 | 智谱/清华 | 6B | MMDiT 单段 | **GLM-4-9B（1024 tok）** | flow matching | DPG **85.13**（开源 SOTA）；汉字 F1 **0.6168** vs Kolors 0.288 | ✅ |
| [[ernie-vilg]] | 2021-12 | 百度 | 10B | VQGAN + 双向自回归 | WordPiece 序列拼接 | next-token（双向）| COCO zero-shot FID **14.7**（DALL-E 27.5）| ❌ |
| [[ernie-vilg-2]] | 2022-10 | 百度 | **24B**（10×2.2B 专家）| 潜扩散 + MoDE 去噪专家 | 1.3B Transformer | DDPM ε-pred | COCO zero-shot FID **6.75**（SOTA）| ❌ |
| [[hunyuan-dit]] | 2024-05 | 腾讯混元 | 1.5B | DiT + cross-attn | **双语 CLIP + mT5** 拼接 | v-prediction | 人评综合 **59.0%**（开源最佳，>SD3 56.7）| ✅ |
| [[kolors]] | 2024-07 | 快手 | 2.6B（U-Net）| SDXL U-Net 潜扩散 | **ChatGLM3-6B-Base（256 tok）** | DDPM ε-pred | 人评总体满意 **3.59**、视觉吸引 **3.99**（>MJv6）| ✅ |
| [[lumina-image-2-0]] | 2025-03 | 上海AI实验室 | 2.6B | 单流统一 Next-DiT | **Gemma-2-2B** | flow matching | DPG **87.20**；GenEval 0.73；591 A100-day | ✅ |
| [[seedream-3-0]] | 2025-04 | 字节 Seed | —（未披露）| MMDiT | 自研双语（未披露）| flow matching + REPA | Arena ELO **1158**（全球第一）；1K 图 **3.0s** | ❌ |
| [[step1x-edit]] | 2025-04 | 阶跃星辰 | 12.43B（connector+DiT）| MLLM→connector→FLUX DiT | **Qwen2.5-VL-7B** | rectified flow | GEdit-EN G_O **6.97**（逼近 Doubao 6.98）| ✅ |
| [[hidream-i1]] | 2025-05 | 智象未来 | **17B 稀疏 MoE**（4 专家 top-2+1 共享）| 双流+单流 Sparse DiT | **4 编码器**（Long-CLIP×2+T5-XXL+Llama-3.1-8B）| flow matching | GenEval **0.83** / DPG **85.89** / HPSv2.1 **33.82** | ✅ |
| [[seededit-3-0]] | 2025-06 | 字节 Seed | —（未披露）| VLM + causal diffusion | Seed1.5-VL | rectified flow + reward loss | 真实图编辑可用率 **56.1%**（GPT-4o 37.1）| ❌ |
| [[qwen-image]] | 2025-08 | 阿里通义 | **20B** MMDiT | 双流 MMDiT | **冻结 Qwen2.5-VL（7B）** | flow matching + DPO/GRPO | GenEval **0.91**；中文字 ChineseWord **58.30**（GPT-Image 36.14）| ✅ |
| [[qwen-image-edit]] | 2025-08 | 阿里通义 | 20B 基座 | MMDiT + 双编码 | Qwen2.5-VL + VAE 双注入 | flow matching | GEdit-EN/CN G_O **7.56 / 7.52**（双榜第一）| ✅ |
| [[hunyuanimage-2-1]] | 2025-09 | 腾讯混元 | **17B** 单/双流 DiT | MMDiT + 32× VAE | **MLLM + ByT5(Glyph)** | flow + RLHF + meanflow 蒸馏 | SSAE **0.8888**（开源 SOTA，逼近 GPT-Image 0.8952）；原生 **2K**，8 步 | ✅ |
| [[hunyuanimage-3-0]] | 2025-09 | 腾讯混元 | **80B 总 / 13B 激活 MoE** | 自回归 LLM + 扩散（Transfusion 系）| Hunyuan-A13B 自身 | AR + flow + CoT | GSB vs 2.1 **+14.1%**，vs Seedream4.0 +1.17%；最大开源生成模型 | ✅ |
| [[seedream-4-0]] | 2025-09 | 字节 Seed | —（未披露）| efficient DiT + 高压 VAE | Seed1.5-VL（PE）| flow + 对抗蒸馏 | Arena 文生图+编辑双榜第一；2K 图 **1.4s**；>10× 加速 | ❌ |
| [[seedream-5-0-lite]] | 2026-02 | 字节 Seed | —（"相对小"）| 统一多模态（未披露）| —（未披露）| —（未披露）| 综合 Elo **超 Seedream 4.5**；首带深度思考+联网搜索；0.22 元/张 | ❌ |
| [[ernie-image]] | 2026-05 | 百度文心 | **8B** 单流 DiT | LDM 单流 DiT + FLUX.2 VAE | **Ministral-3（3B）** | flow + anchor-DPO + MT-DMD 蒸馏 | GenEval **0.8856**（榜首）；人评开源第一；24GB 可跑 | ✅ |
| [[qwen-image-2-0]] | 2026-05 | 阿里通义 | "7B/8B"（仅营销口径）| MMDiT + **f16c64 高压 VAE** | **冻结 Qwen3-VL** | flow + GRPO + DMD 4-NFE | LMArena ELO **1168**（全球第 9，中文第 1，超 Nano Banana）| ✅ |

---

## 二、技术脉络：三次架构换代，一条 LLM-as-encoder 暗线

中国系文生图五年走了三个清晰的架构世代，几乎与全球主线同步但各有「中文优先」的取舍。

### 世代一（2021–2022）：VQ-token + 自回归 Transformer

最早两家是智谱的 [[cogview]] 与百度的 [[ernie-vilg]]，与 OpenAI DALL-E 同期独立提出「把图像用 VQ-VAE/VQGAN 离散成 token、与文本 token 拼成序列做 GPT 式语言建模」的范式。两者都是「中文首个」级别的里程碑：

- [[cogview]] 用 **4B GPT 风格单向 Transformer**（48 层 / hidden 2560 / 40 头），图像 tokenizer 把 256×256 压成 32×32 离散 token（codebook 8192）。它最硬的方法贡献是 **PB-relax + Sandwich-LN**——把「4B 大模型 FP16 训练千步内必 NaN」救活的两个 trick，后来外推到 8.3B CogView-large 与 10B GLM。在模糊化 COCO 上 **FID-2=13.9**，远优于 DALL-E 的 45.5。
- [[ernie-vilg]] 走得更激进：**10B、文→图与图→文双向都用自回归且参数全共享**（靠 UniLM 式 attention mask），COCO zero-shot **FID 14.7**，比 12B 的 DALL-E 领先 12.8。它是百度「文心一格」的直接前身。

[[cogview2]] 是这一世代的收官之作，用 **CogLM 跨模态掩码语言模型 + 分层生成（LoPAR）** 把高分辨率自回归的速度短板基本抹平——高分辨率生成的模型前向次数从 **3600 降到 6**（1/600），整体比初代快约 10×，并引入 **icetk 150K 双语词典**（前 20K 是图像 token），是中文/双语开源文生图的早期基建。

### 世代二（2022–2024）：转向扩散，从 UNet 到 DiT

扩散统治文生图后，各家陆续切换。这一世代的过渡形态分两条：

1. **潜扩散 UNet（含 MoE/级联）**：[[ernie-vilg-2]] 是「首个基于扩散的中文大规模文生图模型」，最大创新是 **MoDE 去噪专家混合**——把 1000 步去噪均匀切成 10 段、每段一个 2.2B U-Net 专家，用去噪步索引 `⌊t/100⌋` 做固定路由，从而把参数扩到 **24B（当时最大文生图模型）而单步推理算力≈单专家**。配合知识增强（POS 关键词加权注意力 + 目标检测区域加权 loss），COCO zero-shot **FID 6.75**（4 张 reranking）成为新 SOTA。[[cogview3]] 则把清华自家的 **relay diffusion（中继扩散）** 首次用于文生图：超分阶段对低分结果加噪后从扩散日程中途起步，人评以 **77.0% 胜率**超 SDXL，蒸馏版（base 4 + 超分 1 步）压到 **1.47s**（≈SDXL 1/10 时间）。

2. **DiT 取代 UNet**：[[hunyuan-dit]]（2024-05，1.5B）是中国系第一个达到强质量的开源中英双语 **Diffusion Transformer**，把条件注入从 AdaLN 改成 cross-attention，用 **双语 CLIP + 多语 mT5 沿文本长度维拼接** + 2D RoPE 多分辨率。在 ≥50 人专业人评下综合通过率 **59.0%**，超所有开源对手，甚至超闭源 SD3 的 56.7%。

### 世代三（2024–2026）：MMDiT/Flow Matching + LLM 当文本编码器

这是当前主线，几乎所有新作都是 **SD3 系 MMDiT + rectified flow/flow matching**，差异主要在「用哪个 LLM 当文本编码器」与「VAE 压缩比」。

一条贯穿全族的**暗线是「LLM-as-text-encoder」**：从 [[kolors]] 用 **ChatGLM3-6B-Base**（2024-07，第一个明确论证「问题出在文本编码器而非 backbone」、把文本长度提到 256）、[[cogview4]] 用 **GLM-4-9B**（1024 token，成为首个能渲染汉字的开源 T2I）、[[lumina-image-2-0]] 用 **Gemma-2-2B**、[[hidream-i1]] 用 **Llama-3.1-8B 多中间层 tap + Long-CLIP×2 + T5-XXL** 四编码器，到阿里把整个 **Qwen2.5-VL（[[qwen-image]]）→ Qwen3-VL（[[qwen-image-2-0]]）** 冻结当条件编码器，再到 [[hunyuanimage-3-0]] 干脆把图像生成直接长在 80B MoE LLM 主干上（AR + 扩散统一）。

这条暗线的逻辑很硬：多语 T5 训练语料里中文占比不足 2%（[[kolors]] 的诊断），bilingual CLIP 撑不起复杂长 prompt；换成真正双语预训练的 LLM（ChatGLM3 用了 >1.4 万亿双语 token），中文语义与汉字字形理解才能上来。

### 平行子线：统一理解-生成 / 推理式出图（2025–2026）

最新一代不再满足于「文生图」，向 **统一多模态 + 思维链生成** 演进：[[hunyuanimage-3-0]] 把 native CoT「先想后画」内置进 80B LLM；[[seedream-4-0]] 用 causal diffusion 把 T2I + 单图编辑 + 多图参考联合后训练；[[qwen-image-2-0]] 把生图支线与编辑支线**合流成单一 omni 模型**；[[seedream-5-0-lite]]（2026-02）更首次把**深度思考（视觉推理，能算围棋下一手）+ 实时联网搜索**带进图像生成。

---

## 三、文字渲染与中文能力：本族最硬的护城河

这是中国系文生图区别于 FLUX/SD/Midjourney 的核心战场。可以按时间看到「谁在什么时间把汉字渲染推到多少」的清晰阶梯。

### 早期：知道难，但还做不到（2021–2024）

- [[ernie-vilg-2]] 已坦白「**文字渲染弱**」：中英混训导致难同时学好两种文字，仅能渲染「福」「20」这类简单字，复杂汉字只学会「在哪写」却画成无意义笔画。
- [[kolors]] 是第一个把中文字渲染当系统工程做的：选 **5 万个最常用中文词**合成**数千万级**中文图文对（仅概念学习阶段引入），再用 OCR+MLLM 给海报/场景文字图重描数百万样本，已能稳定渲染「我爱和平」「天道酬勤」。

### 转折点：CogView4 成为「首个开源汉字渲染」（2025-03）

[[cogview4]] 靠把文本编码器换成 GLM-4-9B，成为**首个能在画面中渲染汉字的开源文生图模型**。其官方 vs Kolors 的中文文字准确率评测把代差讲得很清楚：

| 模型 | Precision | Recall | F1 | Pick@4 |
|---|---|---|---|---|
| [[kolors]] | — | — | 0.288 | 0.163 |
| [[cogview4]] | 0.6969 | 0.5532 | **0.6168** | **0.3265** |

即 F1 从 0.288 翻倍到 0.6168，Pick@4 从 0.163 翻倍到 0.3265。

### 标杆：Qwen-Image 把中文字渲染做成 SOTA（2025-08）

[[qwen-image]] 是把「中文密集文字渲染」推到顶点的工作，靠的是数据工程（七阶段过滤 S1–S7 + 三策略文本合成 + 富文本 VAE 解码器微调 + 无文本→段落级课程学习）。其中文字级评测对 GPT Image 1 的优势是**碾压级**：

| 指标（中文）| [[qwen-image]] | GPT Image 1 | [[seedream-3-0]] |
|---|---|---|---|
| ChineseWord L1 字准 | **97.29** | 68.37 | 53.48 |
| ChineseWord Overall | **58.30** | 36.14 | 33.05 |
| LongText-Bench ZH | **0.946** | 0.619 | — |

GPT Image 1 在中文长文本上仅 0.619，差距悬殊；英文 LongText 上 GPT Image 1（0.956）反而略胜 Qwen-Image（0.943），印证西方模型「英文强中文弱」的典型分布。

值得注意的对照：FLUX.1 Kontext 因中文能力弱，在 GEdit-Bench CN 上 G_O 仅 **1.23**（[[qwen-image]] 页引），而 FLUX.2-klein-9B 在 LongText-Bench 的中文渲染 ZH 仅 **0.218**（[[ernie-image]] 页引）——这是「西方模型中文渲染崩塌」的两个硬数字。

### 2025–2026 的中文文字军备竞赛

到这一阶段，中文文字渲染成了各家比拼的标配维度：

- [[hunyuanimage-2-1]] 用 **MLLM + ByT5(Glyph-SDXL-v2) 双编码器** + OCR agent + IP RAG 结构化 caption，SSAE 语义对齐 **0.8888**（开源 SOTA，逼近 GPT-Image 0.8952），GSB 对 Qwen-Image 胜率 +2.89%。
- [[ernie-image]]（8B）在 **LongText-Bench Overall 0.973**（EN 0.980 / ZH 0.966），仅次于闭源 Seedream 4.5（0.988），高于 Nano Banana 2.0（0.965）、Qwen-Image-2512（0.960），且中英差距极小。
- [[qwen-image-2-0]] 把「超长/多语种文字渲染」做成卖点（1K-token 指令直出 PPT/海报/信息图/漫画），归纳为「准、多、美、真、齐」五特性，典型结论是「只有 Qwen-Image-2.0 能在《兰亭集序》全文小楷上同时保证字符级准确 + 行序正确 + 版面协调」。
- [[seedream-3-0]] 的中文密集小字排版护城河也很硬：中英文**可用率均 94%**（中文较 2.0 提升 16%），擅长密集小字长文本，且与 GPT-4o 对比时「GPT-4o 中文字体明显受限」。

---

## 四、各族纵向脉络速写（抠机制与数字）

### CogView 族：自回归先驱 → 中继扩散 → 汉字渲染 MMDiT

智谱/清华这一族横跨三个世代（4B AR → 6B 分层 AR → 3B relay 扩散 → 6B MMDiT），是观察「中国系架构换代」的最佳切片。[[cogview]] 的 PB-relax/Sandwich-LN 是被反复复用的通用大模型稳训技术；[[cogview2]] 的 LoPAR 把高分前向 3600→6；[[cogview3]] 首引中继扩散且蒸馏到 1.47s；[[cogview4]] 换 GLM-4-9B 成为首个开源汉字渲染、DPG 综合 **85.13** 开源 SOTA。注意 CogView3→CogView4 是**架构换代**（级联 UNet → 单段 MMDiT，DDPM → flow matching），并非小迭代。

### Qwen-Image 族：开源 20B 标杆 → omni 合流

阿里通义这一族是 2025–2026 开源 T2I 的核心标杆。[[qwen-image]]（20B MMDiT，冻结 Qwen2.5-VL，MSRoPE 把文本编码放对角线）GenEval 经 RL（DPO+GRPO 的 Flow-GRPO）从 0.87 拉到 **0.91**（榜上唯一破 0.9 的基础模型），AI Arena 人评是唯一开源前三。[[qwen-image-edit]] 的核心是 **双编码机制**（Qwen2.5-VL 语义 + VAE Encoder 像素双注入），GEdit-Bench EN/CN G_O **7.56/7.52** 双榜第一。[[qwen-image-2-0]]（2026-05）合流生图+编辑两条支线，换 Qwen3-VL，VAE 升级到 **f16c64 高压缩残差自编码器**（16× 压缩、latent 64 通道、语义对齐损失、去 GAN），DMD 蒸到 **4-NFE ≈ 40 步 teacher**，LMArena ELO **1168** 全球第 9、中文第 1、超 Nano Banana。

### Hunyuan 族：DiT → 高效 2K 扩散 → 80B AR 统一

腾讯混元三连跳的架构落差最大：[[hunyuan-dit]]（1.5B DiT，双语 CLIP+mT5）→ [[hunyuanimage-2-1]]（17B DiT，**32× 高压缩 VAE** 让 2K 图 token 长度≈别家 1K，REPA/DINOv2 对齐加速 + meanflow 工业级蒸馏到 8 步，24GB 可跑 2K）→ [[hunyuanimage-3-0]]（**80B 总 / 13B 激活 MoE**，AR+扩散统一，native CoT 先想后画，是最大开源生成模型）。3.0 的 GSB 相对 2.1 胜率 **+14.1%**，对闭源 Seedream 4.0 / Nano Banana / GPT-Image 也分别 +1.17% / +2.64% / +5.00%。

### Seedream 族：闭源旗舰，速度 + 编辑 + 推理三连进

字节 Seed 这一族是闭源工业旗舰路线。[[seedream-3-0]]（MMDiT + flow + REPA + VLM 生成式奖励模型从 1B→>20B 的 scaling 涌现 + 实例轨迹加速）Arena ELO **1158** 全球第一、1K 图 3.0s。[[seededit-3-0]]（真实图编辑可用率从 SeedEdit 1.6 的 38.4% 拉到 **56.1%**，反超 GPT-4o 37.1 / Gemini2.0 30.3，靠 meta-info 数据混合 + diffusion loss + reward loss 联训 + 8× 蒸馏量化）。[[seedream-4-0]]（**efficient DiT + 高压 VAE 做 >10× 加速、2K 图 1.4s**，causal diffusion 联合 T2I+编辑+多图，Arena 文生图+编辑双榜第一，多图编辑 GSB 比 GPT-Image-1/Gemini2.5 高近 20%）。[[seedream-5-0-lite]]（2026-02，首带深度思考视觉推理+联网搜索，综合 Elo 超 4.5，0.22 元/张产品化）。注意 Seedream 族几乎不披露参数量/算力/数据规模——是闭源代价。

### ERNIE 族：双向自回归先驱 → MoE 扩散 → 数据挖掘小模型

百度文心这一族跨度最长（2021→2026）且每代都换范式：[[ernie-vilg]]（10B 双向自回归，COCO zero-shot FID 14.7）→ [[ernie-vilg-2]]（24B MoDE 去噪专家扩散，FID 6.75 SOTA）→ [[ernie-image]]（2026-05，**8B 单流 DiT，主张「数据挖掘 > 参数堆叠」**，自底向上 10k 类细粒度数据挖掘 + 稳定化 **anchor-DPO**（β=0.05 抑制 reward hacking）+ **MT-DMD 多教师蒸馏**缓解 capability drift，GenEval **0.8856** 榜首、人评开源第一、24GB 可跑）。ERNIE-Image 复用了 FLUX.2 VAE 与 3B Ministral 文本编码器，是「小模型 + 后训练工程对抗大模型 scaling」的代表。

### 单点开源诸侯：四条差异化路线

- [[kolors]]（快手 2.6B）：第一个论证「换 LLM 文本编码器（ChatGLM3-6B-Base）解决中文」、自研高分辨率噪声调度（扩散步数 1000→1100 保 αt 曲线形状），人评视觉吸引力 3.99 略超 MJ-v6。刻意不上 DiT、不优化 FID（COCO FID-30K 23.15 反而较差，论文论证 FID 与美学负相关）。
- [[hidream-i1]]（智象未来 17B）：唯一把 **Sparse MoE（4 专家 top-2+1 共享 SwiGLU）植入 MMDiT 双流+单流** 的开源工作，**4 编码器混合**（Long-CLIP×2+T5-XXL+Llama-3.1-8B 多层 tap），GAN-powered DMD 蒸馏到 16 步。GenEval **0.83** / DPG **85.89** / HPSv2.1 **33.82** 三榜开源领先。
- [[lumina-image-2-0]]（上海AI实验室 2.6B，ICCV 2025）：**Unified Next-DiT 单流 joint self-attention 彻底去掉 cross-attention** + 专为 T2I 设计的 UniCap 重描述系统，仅 2.6B 即 DPG **87.20**（本批最高）、GenEval 0.73。提出「caption 长度≈可控模型容量」的动态 FFN 理论解释；总算力仅 **591 A100-day**（少数披露算力的）。
- [[step1x-edit]]（阶跃星辰 12.43B）：**MLLM(Qwen2.5-VL-7B)→token refiner→FLUX DiT** 三段式编辑框架 + 自建 20M→1M HQ 编辑数据管线 + GEdit-Bench 真实用户指令基准（已成事实标准）。GEdit-EN G_O v1.1 **6.97** 逼近 Doubao 6.98、超 Gemini2 Flash 6.51；CN 上 6.983 超 Doubao 6.84。

---

## 五、几条横向观察（机制层面）

1. **VAE 高压缩成为 2025–2026 的效率主战场**。从 [[hunyuanimage-2-1]] 的 **32× VAE**（2K token≈别家 1K）、[[seedream-4-0]] 的高压 VAE（>10× 加速、2K 图 1.4s）、[[hunyuanimage-3-0]] 的 16× 单 VAE，到 [[qwen-image-2-0]] 的 **f16c64 残差 VAE**（16× 压缩、64 通道、语义对齐损失、SOTA 重建：文字域 PSNR 32.81 大幅领先所有 16× 对手）——高压缩 VAE 是「原生 2K/4K 高效扩散」的共同地基。其中 [[qwen-image]] 系列还反复验证「大规模 VAE 训练中对抗损失冗余，去 GAN 更稳」。

2. **奖励/偏好对齐与蒸馏成为后训练标配**。reward scaling 的实证最早见 [[seedream-3-0]]（VLM 生成式 RM 从 1B→>20B 的涌现）；[[qwen-image]] 用 DPO+Flow-GRPO；[[ernie-image]] 给出 anchor-DPO 抑制 reward hacking 的工程超参；蒸馏侧 meanflow（[[hunyuanimage-2-1]] 首次工业级、[[hunyuanimage-3-0]] 扩到 80B 到 4–8 步）与 DMD（[[ernie-image]] MT-DMD、[[qwen-image-2-0]] 4-NFE）两条线并行。

3. **re-caption + prompt enhancer 是中文/复杂指令对齐的统一手段**。从 [[cogview3]] 的 GPT-4V 造三元组微调 CogVLM-17B、[[kolors]] 的 CogVLM 重写 + 50/50 配比、[[hunyuan-dit]] 的 MLLM 结构化 re-caption，到独立 PE 模块（[[hunyuanimage-2-1]] 的 PromptEnhancer-32B、[[ernie-image]] 的 Ministral-3B PE、[[qwen-image-2-0]] 的 Qwen3.5-9B PE + 逆向工程数据 pipeline）——「短 prompt 扩写成结构化长 prompt」几乎是所有现代中文 T2I 的标配前置。

4. **闭源 vs 开源的披露落差极大**。Seedream 全族、ERNIE-ViLG 1/2 几乎不给参数量/算力/数据规模；而 [[lumina-image-2-0]]（591 A100-day）、[[hidream-i1]]（各阶段 step/batch）、[[hunyuan-dit]] 是少数给出部分训练细节的。即便开源旗舰 [[qwen-image]] / [[cogview4]] 也未披露总 GPU·时——这是中国系（乃至全行业）文生图报告的共同短板。

5. **评测方法论的中国特色**：因 FID 被反复论证「与人类偏好脱节」（[[cogview]]/[[cogview2]]/[[cogview3]]/[[kolors]] 都专门论证过），各家纷纷自建评测——SSAE（混元）、ViLG-300（百度）、KolorsPrompts（快手）、GEdit-Bench（阶跃，已成事实标准）、Bench-377/MagicBench/DreamEval（字节）、AI Arena ELO（阿里）。GenEval/DPG-Bench 仍是开源横评的最大公约数。

---

## 六、时间轴总览（19 个时点）

```
2021-05  CogView (4B AR, FID-2 13.9)              ── 自回归世代开端
2021-12  ERNIE-ViLG (10B 双向 AR, FID 14.7)
2022-04  CogView2 (6B 分层 AR, LoPAR 3600→6)
2022-10  ERNIE-ViLG 2.0 (24B MoDE 扩散, FID 6.75) ── 转向扩散
2024-03  CogView3 (3B relay 扩散, 蒸馏 1.47s)
2024-05  Hunyuan-DiT (1.5B DiT, 人评 59.0%)       ── DiT 取代 UNet
2024-07  Kolors (2.6B U-Net, ChatGLM3, 视觉 3.99) ── LLM-as-encoder 暗线起
2025-03  CogView4 (6B MMDiT, 首个开源汉字渲染)    ── flow matching 世代
2025-03  Lumina-Image 2.0 (2.6B 单流, DPG 87.2)
2025-04  Seedream 3.0 (闭源, Arena ELO 1158)
2025-04  Step1X-Edit (12.4B, MLLM→DiT 编辑)
2025-05  HiDream-I1 (17B Sparse MoE, GenEval 0.83)
2025-06  SeedEdit 3.0 (闭源编辑, 可用率 56.1%)
2025-08  Qwen-Image (20B MMDiT, GenEval 0.91, 中文字 58.30) ── 开源标杆
2025-08  Qwen-Image-Edit (双编码, GEdit 7.56/7.52)
2025-09  HunyuanImage 2.1 (17B, 32× VAE, 原生 2K)
2025-09  HunyuanImage 3.0 (80B/13B MoE, AR+扩散统一) ── 统一/CoT 子线
2025-09  Seedream 4.0 (闭源, 2K 1.4s, 双榜第一)
2026-02  Seedream 5.0 Lite (深度思考 + 联网搜索)
2026-05  ERNIE-Image (8B, 数据挖掘>scaling, GenEval 0.8856)
2026-05  Qwen-Image-2.0 (omni 合流, f16c64 VAE, ELO 1168)
```

---

## 附：本页引用的单工作页

CogView 族 [[cogview]] [[cogview2]] [[cogview3]] [[cogview4]] · Qwen-Image 族 [[qwen-image]] [[qwen-image-edit]] [[qwen-image-2-0]] · Hunyuan 族 [[hunyuan-dit]] [[hunyuanimage-2-1]] [[hunyuanimage-3-0]] · Seedream 族 [[seedream-3-0]] [[seededit-3-0]] [[seedream-4-0]] [[seedream-5-0-lite]] · ERNIE 族 [[ernie-vilg]] [[ernie-vilg-2]] [[ernie-image]] · 开源诸侯 [[kolors]] [[hidream-i1]] [[lumina-image-2-0]] [[step1x-edit]]
