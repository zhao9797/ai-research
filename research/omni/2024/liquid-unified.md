---
title: "Liquid: Language Models are Scalable and Unified Multi-modal Generators"
org: "HUST / ByteDance / HKU"
country: China
date: "2024-12"
type: paper
category: unified
tags: [unified-multimodal, autoregressive, vqgan, discrete-token, next-token-prediction, scaling-law, text-to-image, t2i, mllm]
url: "https://arxiv.org/abs/2412.04332"
arxiv: "https://arxiv.org/abs/2412.04332"
pdf_url: "https://arxiv.org/pdf/2412.04332"
github_url: "https://github.com/FoundationVision/Liquid"
hf_url: "https://huggingface.co/Junfeng5/Liquid_V1_7B"
modelscope_url: ""
project_url: "https://foundationvision.github.io/Liquid/"
downloaded: [arxiv-2412.04332.pdf, arxiv-2412.04332.txt, liquid-unified--readme.md, liquid-unified--Data.md, liquid-unified--TRAIN.md, liquid-unified--eval.md, liquid-unified--hf-card.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Liquid 把图像用 VQGAN 离散成与文本同一词表/同一嵌入空间的 token，**不改任何结构、只扩词表 + 低成本 continue-train**，就让一个普通 LLM（Gemma/Qwen2.5/Llama3）同时做文本生成、图像生成、图像理解；首次系统验证了"统一多模态生成遵循 LLM 同款 power-law scaling 律"，且统一带来的语言-视觉冲突随模型增大而消失、理解与生成互相增益。Liquid-7B 仅用 30M 图文对，MJHQ-30K FID=5.47，优于 SD-XL/SD v2.1 及全部离散 AR 统一模型。

## 背景与定位
统一多模态（理解 + 生成）此前主流路线有三类（论文 Fig.1 给出谱系）：
- **(a) 外挂扩散**（DreamLLM/SEED-X/VL-GPT/MetaMorph）：LLM 只出语义 feature，图像由外部 diffusion 生成，生成上限被冻结扩散模型锁死，训练目标不统一。
- **(b)-(e) 半统一**：Transfusion/Show-o 引入 diffusion 建模导致视觉/文本目标不一致；Janus/Janus-Pro 用独立视觉编码 + 分离 head；VILA-U/TokenFlow/SynerGen-VL 需要额外的语义对齐预训练或 token 折叠等前后处理。
- **(f) 纯离散 next-token**：LWM、Chameleon 用 VQVAE 把图像变成离散码，与文本共用 next-token-prediction loss，是最干净的统一形态——但它们都**从头训练**，代价极高（Chameleon 数 T token），且理解/生成质量偏弱。

Liquid 站在 (f) 这一脉，核心主张是：**不必从头训，现成 LLM 已是极强起点**，只要扩 8192 个图像 token、用少量高质量数据 continue-train，即可获得生成+理解能力，省下约 100× 训练成本，同时语言能力不退化。它进一步做了 Chameleon/LWM 都没做的事——把"统一"本身当研究对象，量化 scaling、冲突、协同三件事。相关脉络见 [[chameleon]] [[emu3]] [[janus]] [[show-o]] [[var]] [[llamagen]] [[taming-transformers-vqgan]]。

## 模型架构
**总体**：decoder-only 自回归 Transformer，直接基于现成 LLM，**不改任何内部结构**，唯一改动是嵌入层与 LM head 各扩 8192 维。

- **Image tokenizer**：直接复用 **Chameleon 的 VQGAN**。把 512×512 图像编码为 32×32 离散码（codebook=8192），flatten 成 1024 个图像 token 喂给 LLM。VQGAN 既做 tokenize 也做 detokenize，建立像素↔离散码双向映射（类比 BPE 之于文本）。
- **统一词表**：以 Gemma 为例，原词表 256,000，扩成 256,000+8,192；前者文本、后者图像。文本经 BPE、图像经 VQGAN，最终都是离散 ID 序列，经同一 embedding 层索引 → 嵌入空间彻底统一。LM head 同步扩 8192 维，使模型在同一空间内既预测文本也预测图像 token。
- **特殊 token**：加 `[boi]`/`[eoi]`（image 开始/结束，论文记为 \<boi\>/\<eoi\>）和一个 `<unconditional>` token（用于 CFG 训练的无条件分支）。这些 token 直接占用原 tokenizer 的 `<unusedX>` 槽位，**不新增 tokenizer 词条**（图像 token 由 VQGAN 产生，不进文本 tokenizer）。
- **条件注入**：无 cross-attention、无 adapter——文本 token 与图像 token 直接拼成一条序列，靠 causal self-attention 在统一序列里交互。T2I 输入格式：`[bos] {text token} [boi] {image token} [eoi][eos]`。
- **分辨率策略**：因为是 next-token 可变长生成，**把分辨率写进 prompt**（如 "length is: width is:"），模型学会按指定行列数生成对应数量的码，从而支持任意宽高比（512×512、640×960、1280×480、480×1280 等，见论文 Fig.8）。
- **参数量与模型族**：三大族六个尺寸——Qwen2.5(0.5B/7B/32B)、Llama3(1B)、Gemma-2(2B/9B)、Gemma-7B。主力发布模型 **Liquid-7B 基于 Gemma-7B**。`max context length=2048`（受限于 1024 图像 token + 文本）。

## 数据
**预训练数据（continue-pretrain，共 60M 条 / 约 60B 文本 token + 30B 图像 token）：**
- **文本 30M（≈60B token）**：DCLM 15M + SlimPajama 12M + StarCoderData 代码 3M。目的是维持原 LLM 语言能力不退化。
- **图文对 30M（≈30B 图像 token）**：JourneyDB + 内部 MidJourney-style 合成数据，构成高质量 T2I 语料。
  - **关键 re-captioning**：仓库 Data.md 明确说"仅用 JourneyDB 无法复现 Liquid 的 T2I 性能"，他们额外用了高质量数据并用 **InternVL2.0 重新打 caption**才达标——这是论文正文没强调、但落地必须的细节。
  - 反向利用：把 **20% 的 T2I 数据反转成 captioning 任务**（图→文），以增强视觉理解。
- **图像预处理**：center-crop 到 512×512 后离线抽 VQ code；多分辨率版本按预设分桶尺寸就近裁剪并记录裁剪尺寸到 metadata。大数据集走 HuggingFace `IterableDataset` 避免 OOM。

**scaling 实验数据切分**：每个尺寸独立训三版——30M 纯文本 / 30M 纯 T2I / 60M 混合——以隔离并对比语言与视觉能力。协同实验用 10M text + 10M gen + 10M und 做 baseline，再各加 10M。

**理解 SFT 数据（3.5M 混合指令）**：LMSYS 1M 纯文本指令 + 1M 高质量 T2I 数据 + MiniGemini 的 1.5M 多模态指令。

**安全/美学过滤**：论文未披露专门的美学评分或安全过滤管线（数据来源 JourneyDB/MidJourney-style 本身偏美学），此维度**未充分披露**。

## 训练方法
- **训练目标**：**纯 next-token-prediction + 标准交叉熵**，与 LLM 完全一致——图像 token 和文本 token 用同一个 loss，无 diffusion / flow-matching / masked-token 等异质目标。这是 Liquid 相对 Transfusion/Show-o 的"目标统一"卖点。
- **continue-pretrain（而非 from-scratch）**：从现成 LLM 权重出发，仅新增 8192 个可学习图像 embedding；扩词表时用 `mean_resizing=True`（新 embedding 初始化为旧 embedding 均值，降低扩词表前后 next-token 概率的 KL，使初始 loss 更低）。
- **稳定性 trick（重要）**：7B 及以上模型在 continue-pretrain 早期会出现 **loss spike**，严重拖慢收敛。对策：(1) 大模型 **max grad norm 降到 0.5**；(2) 用 **max-z loss**（来自 Baichuan2）归一化 logits 稳定训练。
- **关键超参**：lr=2e-5；scaling 实验用 constant lr，其余用 cosine schedule；global batch size=1024；max context=2048；优化用 **DeepSpeed ZeRO-3**。
- **多阶段**：Pretrain model（混合 60M 数据，得语言+生成能力）→ 在其上做 **SFT（3.5M 混合指令）** 得理解能力（IT 模型）。仅做 SFT，**未做 RLHF/DPO/reward model 等偏好对齐**（论文未报告）。
- **蒸馏/步数加速**：**无**。Liquid 走纯 AR，未引入 consistency/LCM/ADD/步数蒸馏（这是 AR-token 路线的固有推理慢点，论文未处理）。
- **推理**：标准 AR 采样 + **CFG**（用 `<unconditional>` 分支）。论文 Fig.10 给出 CFG scale 消融：CFG↑（如 15）文图一致性更强但结构混乱、风格化重、真实感差；CFG↓ 真实感与纹理细节更好但语义对齐弱——需折中。

## Infra（训练 / 推理工程）
- **框架极简**：刻意不写新 wrapper，保持原 LLM 的 HuggingFace 加载方式；训练栈 `torch==2.1.0` / `transformers==4.39.2` / `flash-attention==2.5.8`，DeepSpeed ZeRO-3。
- **数据工程是瓶颈**：强调大规模图文对 + 预抽 VQ code 会吃满磁盘/内存，必须用 `IterableDataset` 流式加载；VQ code 离线多 GPU/多机抽取（`extract_vqcodes.sh`）。
- **算力规模**：论文**未披露**总 GPU·时/卡数/吞吐，只给"省 100× 训练成本 vs Chameleon"这一相对量级。
- **推理部署**：本质就是一个 HF 格式语言模型，只需 `transformers` 即可跑；<30GB 显存可开 `load_in_8bit`。生成 MJHQ-30K 的 3 万张图在 8 卡机上约需 **10–30 小时**（取决于卡），印证 AR-token 路线逐 token 解码 1024 个图像 token 的推理偏慢。无量化/缓存/蒸馏加速披露。

## 评测 benchmark（把效果讲清楚）
**① 图像生成 — MJHQ-30K（FID↓，Table 3）**：Liquid-7B **FID=5.47**，训练图仅 30M。
- 优于全部 AR 模型：LWM 17.77、VILA-U(256) 12.81、VILA-U(384) 7.69、Janus 10.10；
- 优于离散扩散 Show-o 15.18；
- 优于多数扩散模型：SD-XL 9.55、PixArt 6.14；仅次于 Playground v2.5（4.48）。

**② 文图对齐 — GenAI-Bench VQAScore（Table 2）**：Liquid-7B（30M 训练图）
- basic prompts **Overall 0.83**，超 SD v2.1(0.77)、SD-XL(0.83 持平)，超全部 AR（VILA-U 256=0.78、Show-o=0.70、LWM=0.63）；
- advanced prompts **Overall 0.65**，仍领先全部 AR 与 SD v2.1(0.62)/SD-XL(0.63)；仅次于 Midjourney v6(0.69)/DALL·E 3(0.70)。

**③ 世界知识 — WISE WiScore（Table 4，归一化）**：Liquid **Overall 0.41**，在"理解&生成"统一模型里**全面领先**——Emu3* 0.39、Janus-Pro-7B 0.35、Janus-Pro-1B 0.26、Show-o 0.30、VILA-U-7b 0.31；甚至超过纯生成专用模型 FLUX.1-schnell(0.40)、SD-XL-base(0.43 接近)、SD-3-medium(0.42)，仅落后 FLUX.1-dev(0.50)/Playground-v2.5(0.49)。说明保留语言能力带来更强的知识驱动生成。

**④ 视觉理解（Table 6，zero-shot）**：Liquid（Gemma-7B，res 512）VQAv2 68.0 / GQA 56.1 / TextVQA 40.4 / POPE 81.1 / MME 1107.2。
- 在离散 token 统一模型里**超 LWM、Chameleon、Show-o**；
- †（多训一个 epoch）提升到 VQAv2 71.3 / TextVQA 42.4 / MME 1119.3 —— 说明混合预训练本身起到了类 CLIP 的对齐作用；
- ‡（把 VQGAN 换成与 CLIP 语义对齐的 **UniTok**，基座换 Llama2-7B/res 256）VQAv2 76.8 / GQA 61.1 / TextVQA 51.6 / POPE 83.2 / MME 1448.0，**超 VILA-U、逼平 LLaVA**——验证"视觉-语义空间对齐"对理解至关重要。
- 仍落后用连续 CLIP 特征的 LLaVA-1.5/VILA（这是离散 token 路线的已知短板，作者坦承）。

**⑤ 纯文本能力（Table 5）**：Liquid 多模态混合预训练后**语言能力不退化**——Gemma-7B 版 mix-train 与 text-only 版几乎持平（如 HellaSwag 76.1 vs 77.2、ARC-c 49.0 vs 48.8、MMLU 56.0 vs 55.5），**全面超 Llama2-7B/13B**，并在多数任务超 Chameleon-7B（后者用海量数据 mix 预训练）。

**核心消融/发现（三大 Finding）：**
- **Finding 1（scaling，§3.1 / Fig.3）**：0.5B→32B 混训后，视觉生成的 validation loss 随 FLOPs 呈清晰 **power-law**（与 LLM 一致），VQAScore 随 loss 下降单调上升（R²=0.9051）；同 FLOPs 下小模型更快到低 loss，但大模型上限更高。
- **Finding 2（冲突，§3.2 / Fig.5-6）**：混训确实损害语言能力（小模型明显）也抬高视觉 val loss，但**这种 trade-off 随模型增大而消失**——大模型容量足以同时容纳两空间。
- **Finding 3（协同，§3.3 / Table 1）**：理解与生成互相增益。baseline(10M+10M+10M) gFID 19.9；**Add Gen.→gFID 12.8** 同时把 VQAv2 60.7→64.5；**Add Und.→VQAv2 63.5** 同时把 gFID 降到 14.9、GenAI Overall 0.60→0.66。即加任一方数据，两边一起涨。
- **跨模态 ICL（§4.4）**：加入交错图文数据预训练后涌现跨模态 in-context learning（给"图1晴/图2雨/图3?"能推出"雪"），无需显式对齐监督。

## 创新点与影响
**核心贡献：**
1. **最小改动统一范式**：现成 LLM + 扩 8192 词表 + 低成本 continue-train，无外挂模块、无语义预训练、无分离 head、无异质训练目标，把理解/生成/纯文本三件事压进一个 next-token loss。省约 100× 训练成本。
2. **首次给出统一多模态生成的 scaling 律**：证明视觉生成在 LLM 里同样遵守 power-law，且**语言-视觉冲突随规模递减乃至消失**——为"用大 LLM 做统一生成"提供了 scaling 信心。
3. **理解↔生成协同的实证**：统一 token 空间下两任务互相增益，推翻了此前 Janus 等"必须解耦视觉编码以避冲突"的前提，是后续 unified-MLLM 设计的重要反例证据。
4. **工程可复现**：本质是 HF 语言模型，开源 7B-IT 权重 + 训练/评测脚本，门槛极低。

**对后续工作的影响**：为"统一离散 token + 现成 LLM continue-train"这条最简路线背书，与 Emu3、Janus-Pro、Chameleon 共同构成 2024-2025 unified-MLLM 的主要技术坐标系；其"tokenizer 语义对齐决定理解上限"的结论（†/‡ 实验）直接指向后续 UniTok/TokenFlow/VILA-U 等语义对齐 tokenizer 的研究方向。

**已知局限：**
- 离散 token 理解能力仍逊于连续 CLIP 特征路线（需更强语义对齐 tokenizer 弥补）。
- AR 逐 token 解码 1024 个图像 token，**推理慢**（30K 图 8 卡 10–30h），无步数蒸馏/缓存加速。
- 分辨率受 max context 2048 限制，单图 1024 token，难直接上更高分辨率。
- 未做偏好对齐（RLHF/DPO），未公开总算力/GPU·时；0.5B~32B 的 Pretrain checkpoint 截至仓库 README 仍标记未发布（只发了 7B-IT）。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2412.04332
- arxiv_pdf: https://arxiv.org/pdf/2412.04332
- github: https://github.com/FoundationVision/Liquid
- project_page: https://foundationvision.github.io/Liquid/
- hf_model: https://huggingface.co/Junfeng5/Liquid_V1_7B
- hf_demo: https://huggingface.co/spaces/Junfeng5/Liquid_demo
- github_data_doc: https://github.com/FoundationVision/Liquid/blob/main/Data.md
- github_train_doc: https://github.com/FoundationVision/Liquid/blob/main/TRAIN.md
- github_eval_doc: https://github.com/FoundationVision/Liquid/blob/main/evaluation/EVAL.md

## 一手源存档（sources/）
- [arxiv-2412.04332.pdf](https://arxiv.org/pdf/2412.04332)  （arXiv 原文 PDF，不入 git）
- [arxiv-2412.04332.txt](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/arxiv-2412.04332.txt)
- [readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/liquid-unified--readme.md)
- [Data.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/liquid-unified--Data.md)
- [TRAIN.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/liquid-unified--TRAIN.md)
- [eval.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/liquid-unified--eval.md)
- [hf-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/liquid-unified--hf-card.md)
