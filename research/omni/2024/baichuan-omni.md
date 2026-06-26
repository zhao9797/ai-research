---
title: "Baichuan-Omni"
org: Baichuan Inc.（百川智能，联合西湖大学 / 浙江大学）
country: China
date: "2024-10"
type: tech-report
category: omni
tags: [omni, mllm, audio, video, image, speech, open-source, vita, siglip, whisper, conv-gmlp]
url: https://arxiv.org/abs/2410.08565
arxiv: https://arxiv.org/abs/2410.08565
pdf_url: https://arxiv.org/pdf/2410.08565
github_url: https://github.com/westlake-baichuan-mllm/bc-omni
hf_url: https://huggingface.co/papers/2410.08565
modelscope_url:
project_url:
downloaded: [arxiv-2410.08565.pdf, baichuan-omni--readme.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Baichuan-Omni 是百川智能 2024 年 10 月放出的**首个开源 7B 全模态（图像 / 视频 / 音频 / 文本）理解大模型**，主打"一个模型同时吃四种模态 + 支持实时语音/视频流交互"，目标是做 GPT-4o 的开源对标基线。其核心亮点是用 **Whisper-large-v3 音频编码器 + 自研 Conv-GMLP 音频投影器**做激进 token 压缩仍几乎不掉点（下采样率 8× 时 ASR 平均 WER 仅 8.0%），并在中文 ASR（WenetSpeech test_net CER 7.1% vs VITA 12.2%）、视频开放问答（ActivityNet-QA 58.6%，超 Gemini 1.5 Pro 56.7%）等多个 omni benchmark 上超过当时唯一的开源 omni 模型 VITA（8×7B，12B 激活）。

## 背景与定位
2024 年 GPT-4o 把"多模态 + 自然语音交互"推成事实标准，但开源世界缺一个能**同时**处理图/视/音/文且能实时交互的模型——当时最接近的开源 omni 模型是 [[vita]]（MoE，8×7B，约 12B 激活参数）。视觉侧有 [[qwen2-vl]]、LLaVA、InternVL、MiniCPM-V 等强 VLM，音频侧有 Qwen-Audio / SALMONN / SpeechGPT，但都各管一摊。

Baichuan-Omni 的定位就是**填这个空白**：用一个仅 7B 的稠密 LLM 做底座，通过"分支对齐预训练 + omni 联合对齐 + 多任务 SFT"的训练范式，把图像、视频、音频三条编码链都接进来，并探索"先预测语音输入边界、视觉流式编码"的实时交互机制。相对 VITA 的改进是：**更小（7B 稠密 vs 12B 激活 MoE）、中文能力大幅领先、音频侧引入新投影器、视频/音频多个 benchmark 反超**。它也是后续 [[baichuan-omni-1.5]]（2025-01）的前身。

需要诚实标注的一点：论文/仓库自称"open-source"，但发布当时（2024-10）GitHub 仓库的 Model Zoo / Inference / Requirements 章节全是空占位，**权重与推理代码"coming soon"未实际放出**；真正可下载的 base + alignment 权重要到 2025-01-26 随 Baichuan-Omni-1.5 才公开（见 README News）。所以"首个开源 omni MLLM"在论文发布时点更准确的说法是"首个开源技术报告/路线"。

## 模型架构
整体是经典 **"模态编码器 → 模态投影器 → 共享 LLM 解码器（自回归 Transformer）"** 的理解型 MLLM 架构（非生成扩散模型），不含任何图像/音频生成头。LLM 底座是百川自研的 **7B 稠密语言模型**（论文通篇称 "7B model"，未点名具体版本号）。三条模态链：

**图像分支（Image-Language）**
- 视觉编码器：**Siglip-so400m-patch14-384**（428M），输入 384×384，经"两层 MLP + 2×2 卷积池化层"组成的视觉投影器输出 **182 个 token**。
- 任意分辨率：采用 **AnyRes**——把高分图切成网格分块，再拼一张降采样全局图提供全局上下文，显著改善 OCR/文档类细节任务。
- 投影器选型经消融最终用 **Mean Pool**（卷积 stride=2 池化 + 两层 MLP）：每个子图压到 182 token，比 MLP（729 token）省 token；MLP 虽在中文 OCR 学习上最强（排序 MLP > Mean Pool > Concat > C-abs），但 token 太多，权衡后取 Mean Pool。

**视频分支（Video-Language）**
- 复用与图像分支**同一个** Siglip-384px 编码器（训练视频投影器时冻结）。
- 采样：**1 fps，最多 48 帧**；每帧最大分辨率 384×768；投影器前加 2×2 卷积控制序列长度，每段视频 token 数 **182–546**。

**音频分支（Audio-Language）**
- 音频编码器：**Whisper-large-v3**，处理 30s / 128 维 mel 谱，输出 1280 通道特征。
- 音频投影器：**自研 Conv-GMLP**（论文核心架构创新之一）。传统做法是 stride=n 的池化下采样减少 token，但激进压缩会丢音频信息；Conv-GMLP 把 gated MLP 里的线性层换成卷积层，两层卷积各把序列长度缩 n 倍、特征维度按比例扩 n 倍（如下采样率 4 → 序列变 1/4、通道变 4×），并加 **residual shortcut** 改善梯度回传，从而在激进下采样下仍保住音频信息。

**交互机制（实时 omni）**：模型先**预测音频输入的起止边界（start/end）**；在该窗口内，流入的图像/视频被流式编码成特征喂进 MLLM 参与 attention 计算；音频输入结束后再把音频特征送进 MLLM 推理——以此支持音视频的流式输入。论文把这块定位为"early-stage research"。

## 数据
百川自建了一套涵盖 text / image-text / video-text / audio-text 及其交叉的高质量跨模态数据集，混合**开源 + 合成 + 内部标注**三类来源。

**图像数据**：分 Caption / 交错图文（Interleaved）/ OCR / Chart 四类。
- 开源：Stage I 用 PIN-14M、MINT-1T、LAION-5B、OBELIC 等；Stage II/III 用 Cauldron、Monkey、ArxivQA、TGDoc、MM-Self-Instruct、MMTab 等。
- 合成：一部分从书籍/论文解析出交错图文、OCR、Chart（知识密度高）；另一部分训练专用模型生成多视角详细图像 caption。

**视频数据**：QA（NExTVideo、ActivityNet-QA 训练集）+ Caption（ShareGPT4Video、WebVid）；并用 **GPT-4o** 给 YouTube 采集的视频生成多样 caption。采样比按各数据集相对大小定。

**音频数据**：从各种媒体抽取音频，覆盖不同录音环境/语言/口音/说话人。建了含**说话人录音、方言识别、口音识别、音效检测、质量评估**的处理流水线；用内部 ASR + 多个开源模型生成多版转写，再用 model ensemble 做文本过滤与纠错。

**文本数据**：网页、书籍、论文、代码等，按多样性 + 高质量两条准则筛选去冗余。

**跨模态交互数据（合成）**：image-audio-text 与 video-audio-text 两类。
- 图文：把文本按 **1:3** 切分，前 1/4 用 **TTS（44 种音色）** 转成音频描述，任务是"听完音频 + 看图后补全剩下 3/4 文本描述"。
- 视频：直接抽取视频原声作为跨模态音频。

**SFT 数据**：覆盖 **200+ 任务、约 600K** 条样本，跨纯文本 / 音频 / 图文 / 视频文本 / 图像-音频。
- 图像 SFT 主用 **vFLAN**（191 任务），做 **loss-based 高斯过滤**：用预训练模型算 loss 拟合高斯，剔除落在 μ±σ 之外的样本（< μ−σ 多为 prompt/response 雷同的平凡样本，> μ+σ 多为反转或幻觉），筛后部分翻成中文 + 人工重标。
- 关键 trick：发现塞太多模型本不掌握的外部世界知识会导致**收益递减甚至掉点**，因此采用基于"模型是否已掌握该事实"的过滤法 [27] 剔除"unknown"数据。
- 视频 SFT 主用 VideoInstruct100K，做语义去重 + 中译增多样性；音频 SFT 多用 TTS 合成（再用 ASR 回转校验保留准确样本）+ 真人录音补方言/口音/噪声。

## 训练方法
训练目标是标准的**自回归 next-token 预测**（理解模型，无 diffusion / flow matching）。整体两大阶段：**多模态对齐预训练 → 多模态多任务 SFT**。对齐预训练对三个分支分别训练后再做 omni 联合对齐：

**图像分支三阶段**
- Stage I：冻结 LLM + 视觉编码器，**只训视觉投影器**（lr=1e−3），用图像 caption 任务建立初步图文对齐。
- Stage II：冻结 LLM，**训投影器 + 视觉编码器**（lr=1e−5）；除通用 VQA 外，专门合成 **130k 高质量 OCR/Chart QA**；引入交错数据与 caption 缓解解冻编码器后特征空间漂移。
- Stage III：**解冻 LLM，全参数更新**（lr=1e−5）；加入交错数据 + 纯文本数据，保住 LLM 原有能力。

**视频分支**：冻结 Siglip 编码器 + LLM，**只训视频投影器**（lr=4e−6）。采两阶段：先用图文预训练数据强化视觉理解，再逐步混入"图文 + 视频文本"对训练（消融证明优于直接只用视频文本对）。

**音频分支**：冻结 LLM，**只训音频编码器 + Conv-GMLP 投影器**，用长音频文本序列（最长 4K token），cosine lr 调度。

**Omni 联合对齐**：在三分支各自训完后，把所有模块一起在高质量图文/视频文本/音频文本混合数据上联合训练，建立综合多模态理解。

**多任务 SFT**：用上述 600K 跨模态数据做有监督微调；选数据时只保留"预训练模型已能掌握"的样本（避免引入未知知识掉点）。工程上用 **packing**——靠 flash-attention2 的 `cu_seqlen` 做样本隔离，把多条样本拼进一个大 batch 同时保证各样本计算互不串扰，加速训练并优化显存。

加速/蒸馏：**未使用** consistency/LCM/步数蒸馏等（理解模型不适用）；推理加速主要靠音频侧 Conv-GMLP 的 token 压缩。

## Infra（训练 / 推理工程）
论文对训练算力披露很少：**未报告** GPU 型号、卡数、GPU·小时、并行/分布式策略、混合精度配置、吞吐等具体数字。可确认的工程点有限：
- SFT 阶段用 **flash-attention2 + cu_seqlen 样本隔离的 packing** 加速并省显存。
- 音频侧 Conv-GMLP 的激进 token 下采样（率 8× 仍几乎不掉点）本身就是**推理/序列成本的工程优化**——把音频帧数压到 1/8 仍保住 WER。
- 部署形态：发布时（2024-10）仅放技术报告，权重/推理代码标注"coming soon"；可运行权重随 2025-01 的 1.5 版才公开。
- 一致性消融在 **1.5B** 小 audio-language 模型上做（验证下采样率鲁棒性），主模型为 7B。

总体：**Infra 维度基本未披露**，是本报告最弱的一环。

## 评测 benchmark（把效果讲清楚）
评测全部 zero-shot，视觉统一用 VLMEvalKit。下面抠关键数字（B-Omni = Baichuan-Omni 7B）。

**纯语言（综合）**——对比 VITA(8×7B)：
- CMMLU **72.2%**（VITA 46.6%）、C-Eval **68.9%**（VITA 56.7%）、AGIEval **47.7%**（VITA 46.2%）、MMLU 65.3%。中文优势巨大。

**图像理解（13 个 benchmark）**——对比 VITA / Qwen2-VL(7B) / MiniCPM-V 2.5：
- MCQ/Yes-No：MMBench **76.2**（VITA 74.7）、MMBench-CN **74.9**（VITA 71.4）、SEED-IMG **74.1**、MMMU(val) **47.3**（VITA 45.3）、HallusionBench **47.8**、M3GIA **34.7**（VITA 27.7）、MME 2186.9。
- VQA：MMVet **65.4**（VITA 41.6）、MathVista-mini **51.9**（VITA 44.9）、RealWorldQA **62.6**（VITA 59.0）、TextVQA 74.3、ChartQA 79.6、OCRBench 70.0。
- 结论：**全面超过 VITA**，多数任务追平/超过图像专用的 MiniCPM-V 2.5；但相对 **Qwen2-VL(7B) 仍有明显差距**（如 MMBench 86.4、MathVista 58.2），与闭源 GPT-4o 差距更大。

**视频理解**——对比 VITA / Qwen2-VL / GPT-4V / Gemini 1.5 Pro：
- 通用 VQA：MVBench **60.9**（VITA 53.4）、Egoschema **58.8**（VITA 53.9，且超 GPT-4V 55.6）、VideoMME **58.2**（VITA 56.1）、Perception-Test **56.8**。General Video QA **全项超 VITA，平均约 +4%**。
- 开放问答：ActivityNet-QA **58.6 / 3.7**（VITA 55.0；**超 Gemini 1.5 Pro 56.7**）、MSVD-QA **72.2 / 4.0**（开源 SoTA，VITA 63.9）。

**音频理解**——对比 Qwen2-Audio-Instruct / VITA / Whisper-large-v3 / SALMONN：
- ASR（WER/CER ↓）：Fleurs test-zh **7.0**（Qwen2-Audio 9.0）、test-en **4.7**（Qwen2-Audio 15.7）；WenetSpeech test_net WER **6.9** / CER **7.1**（VITA CER 12.2，Qwen2-Audio 11.0/11.3）；test_meeting WER **8.4** / CER **8.9**（VITA 16.5）；KeSpeech 方言平均 CER **6.7**。中文 ASR 全面领先。
- S2TT（BLEU ↑）：Covost2 en2zh **40.2**（Qwen2-Audio 34.1，**+约 7 BLEU**）、zh2en 22.1（与 Qwen2-Audio 23.3 相当）。
- AIR-Bench Chat（Score ↑）：speech **7.42** / sound **7.26**（均超 Qwen2-Audio 7.18 / 6.99）；music 6.12、mix-audio 5.76 偏弱。

**关键消融**：
- 视觉编码器：14 个候选里 **Siglip-so400m-384** 平均分最高（OCR 尤强），故选它。
- **AnyRes** 对文档/OCR 提升巨大：DocVQA 72.6→87.5、InfographicVQA 47.5→62.8。
- 视频：帧数 64→48 平均掉 54.7→50.1；AnyRes vs 固定 384px 平均 +约 5%；去掉视频预训练 MVBench 掉约 6%。
- 音频 Conv-GMLP 下采样率消融（1.5B 模型）：率 2 平均 WER **7.7%**，率 4 为 8.3%，率 8 反而 **8.0%**（优于率 4）——证明 Conv-GMLP 序列压缩鲁棒性极强。
- SFT vs IFT（Table 11/12）：图像 MMVet 55.0→65.4、MMBench-CN 69.3→74.9；视频 MSVD-QA 66.6→72.2、ActivityNet-QA 55.4→58.6，多数指标提升（个别如 MMMU 48.3→47.3、MVBench 61.3→60.9 微降）。

## 创新点与影响
**核心贡献**
1. **首个开源 omni MLLM 路线**：一个 7B 稠密底座同时支持图/视/音/文理解 + 中英双语，给开源社区一个可对标 GPT-4o 的 baseline 与完整训练配方（数据构造 → 分支对齐 → omni 对齐 → 多任务 SFT）。
2. **Conv-GMLP 音频投影器**：用卷积版 gated MLP + residual 替代池化下采样，在激进 token 压缩（8×）下仍几乎不掉 ASR，是音频侧最实在的架构创新。
3. **跨模态交互数据合成范式**：1:3 切分 + TTS（44 音色）造图-音-文交互数据；以及"已知知识"过滤（剔除 unknown，避免 SFT 掉点）的数据策略。
4. **流式 omni 交互雏形**：先预测语音边界、视觉流式编码进 attention 的实时交互机制。

**影响**：直接催生 [[baichuan-omni-1.5]]（2025-01，权重正式开源），推动了 2024H2–2025 开源 omni 方向（与 VITA-1.5、MiniCPM-o、Qwen2.5-Omni 等同期演进）。其"复用同一视觉编码器跨图像/视频 + 分支独立对齐再联合"的范式被后续工作沿用。

**已知局限**——论文 Conclusion 明确自述 4 条：(1) 文字提取能力待加强；(2) 需支持更长视频（当前最多 48 帧）；(3) **没有端到端 TTS**——只能理解音频、不能直接生成语音（与 GPT-4o 的语音输出差距），列为 future work；(4) 对自然环境声（流水、鸟鸣、碰撞声）理解弱、当前主要懂人声。
另由本页从其评测表读出的短板（非论文自述）：(5) 图像理解相对 Qwen2-VL 仍有明显差距、与闭源差距更大（见 Table 2/3）；(6) Infra/算力细节几乎未披露；(7) AIR-Bench 的 music 6.12 / mix-audio 5.76 偏弱。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2410.08565
- arxiv_pdf: https://arxiv.org/pdf/2410.08565 （v4, 2024-12-27）
- github: https://github.com/westlake-baichuan-mllm/bc-omni
- hf_paper: https://huggingface.co/papers/2410.08565
- 后续版本: https://github.com/baichuan-inc/Baichuan-Omni-1.5 （2025-01-26 权重开源）

## 一手源存档（sources/）
- [arxiv-2410.08565.pdf](https://arxiv.org/pdf/2410.08565) （技术报告全文 PDF，已精读正文/实验/消融/附录表）
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/baichuan-omni--readme.md) （GitHub bc-omni README，含 News/架构概述/引用）
