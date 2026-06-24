# 预训练数据

> 本章汇编 frontmatter `categories` 含「预训练数据」的全部来源（从磁盘重读，年份目录为准）。涵盖四条主线：(1) 缩放律与数据/算力关系；(2) 数据集本身（开放语料、清洗/去重 pipeline、合成数据、专门语料）；(3) 英文/西方阵营基础模型的预训练语料规模、配比与多模态混合实践；(4) 中国阵营基础模型的预训练数据工程。themes/ 与博客重复条目并入年份目录的主条目。

## 概览：2020 → 2026 的演进脉络

2020 年的起点是「规模优先」：OpenAI 的缩放律把损失刻画为参数/数据/算力的幂律，催生 GPT-3 用约 3000 亿 token 训练 175B；同年 EleutherAI 的 The Pile 把「来源多样性」立为开放语料范式。2021–2022 年范式两度转向——MoE（GLaM 1.2T 稀疏、GLM-130B 双语）解耦总参与算力，而 Chinchilla（2022）用「参数与 token 等比例缩放」颠覆 Kaplan 的参数优先观，把「数据是瓶颈」写进共识，直接催生 LLaMA（2023）「小模型 + 万亿 token + 纯公开数据」的开源路线。2023 年起两股力量并行：一是「数据质量 > 规模」（phi 系列教材级合成数据、Galactica/Minerva/DeepSeekMath 的领域语料、Yi 的数据工程优先）；二是「数据透明化」（Pythia/OLMo/Dolma/FineWeb/DCLM/MAP-Neo/CCI3.0-HQ 把语料、清洗 pipeline、消融、中间 checkpoint 全部开放）。中国厂商从 2020 年 CPM（100GB 中文）一路追到 2023–2025 年的万亿 token 双语/多语 MoE（Qwen3 36T、DeepSeek-V3 14.8T、Kimi K2 15.5T、Llama 4 >30T）。2024–2026 年主题进一步收敛：合成数据贯穿全程（phi-4 反超 teacher、Hunyuan-Large 1.5T 合成、Nemotron-CC rephrasing）、token 推到 20–32T+（Hunyuan-A13B/Nemotron-Nano-2 20T、OLMo 2 课程化 mid-training）、原生多模态联合预训练（Gemini/Emu3/InternVL3/ERNIE 5.0/LongCat-Next）、以及 NVFP4/FP8 低精度预训练与百万 token 上下文（DeepSeek-V4、Nemotron 3、Qwen3.5-Omni）。

---

## 一、缩放律与数据-算力关系

- **Scaling Laws for Neural Language Models** (OpenAI, 2020-01, paper) — Kaplan 等首提语言模型损失对参数 N、数据 D、算力 C 的幂律（L(N)∝N^-0.076、L(D)∝N^-0.095、L(C)∝C^-0.050）；结论「固定算力下应训大模型、不训到收敛」，为 GPT-3 放大路线提供依据，基于 WebText2。 https://arxiv.org/abs/2001.08361
- **Scaling Laws for Autoregressive Generative Modeling** (OpenAI, 2020-10, paper) — 把缩放律从文本扩展到图像/视频/图文多模态/数学，证明 L = L∞ + (N0/N)^α 统一形式跨模态普适（L∞ 为数据熵下界）；预训练损失越低，迁移到分类等下游越好。 https://arxiv.org/abs/2010.14701
- **Training Compute-Optimal Large Language Models (Chinchilla)** (DeepMind, 2022-03, paper) — 训练 400+ 模型（70M–16B、5B–500B token）得「计算最优」定律：参数翻倍则数据也应翻倍（N∝C^0.5、D∝C^0.5）；据此训 Chinchilla 70B / 1.4T token，与 Gopher(280B) 同算力但 4× 数据，MMLU 67.5% 全面反超。 https://arxiv.org/abs/2203.15556
- **Towards Greater Leverage: Scaling Laws for Efficient MoE LMs** (蚂蚁 Ling Team / inclusionAI, 2025-07, paper) — 提出 Efficiency Leverage (EL) 量化 MoE 相对等效稠密模型的算力杠杆；训 300+ 模型（最大 28B）发现 EL 由专家激活比与总算力预算主导且服从幂律，专家粒度为非线性调节器，指导 Ling 系列。 https://arxiv.org/abs/2507.17702

---

## 二、开放语料与数据集 / 清洗 pipeline / 合成数据

### 开放语料与数据透明化

- **The Pile — An 800GB Dataset of Diverse Text** (EleutherAI, 2020-12, paper) — 825 GiB（约 800GB）多样化英文语料，22 个高质量子集（Pile-CC、PubMed、ArXiv、GitHub、Books3、Stack Exchange 等），确立「来源多样性优于单一爬取」；文档级去重 + 按质量赋采样权重，成为 GPT-Neo/J/NeoX 等的事实标准语料。 https://arxiv.org/abs/2101.00027
- **Pythia: A Suite for Analyzing LLMs Across Training and Scaling** (EleutherAI, 2023-04, paper) — 16 个模型（70M–12B，deduped/非 deduped 两套）全部在完全相同顺序的 The Pile（约 300B/207B token）上训练，每模型公开 154 个 checkpoint + 可精确重建的 dataloader，是训练动力学研究基石。 https://arxiv.org/abs/2304.01373
- **MAP-Neo** (M-A-P / 滑铁卢大学 / 武汉 AI 研究院 / 01.AI, 2024-05, paper) — 完全透明开源的 7B 双语模型，约 4.5T token，不只放权重还开放完整预训练语料 Matrix Data Pile + 去重/过滤流水线 + 中间 checkpoint + 训练/评测代码，对标 OLMo/Pythia 的「真开源」。 https://arxiv.org/abs/2405.19327
- **Dolma: an Open Corpus of Three Trillion Tokens** (AI2, 2024-01, paper) — 3T token 开放英文语料（CC 网页 + The Stack 代码 + peS2o 论文 + Gutenberg + Reddit + Wikipedia）；pipeline = 语言识别→质量/内容过滤→URL/文档/段落级 Bloom filter 去重→PII/去毒，开源 Rust curation 工具包，是 OLMo 的训练数据基础。 https://arxiv.org/abs/2402.00159
- **The FineWeb Datasets** (Hugging Face, 2024-06, paper) — 15T token 开放语料（96 个 CC 快照），完整公开去重/过滤消融；关键发现是逐快照 MinHash 去重（而非跨全量）反直觉地更优；衍生 FineWeb-Edu（用 Llama-3-70B 标注教育质量训分类器筛出 1.3T token），显著提升 MMLU/ARC。 https://arxiv.org/abs/2406.17557
- **DataComp-LM (DCLM)** (DataComp: UW/Apple/TRI/AI2 等, 2024-06, paper) — 240T token 标准化语料 + 统一 OpenLM 训练配方 + 53 项评测的受控测试平台；核心结论「基于模型的过滤（fastText 质量分类器）>> 启发式过滤」；DCLM-Baseline 让 7B 用 2.6T token 达 MMLU 64%，与 Llama 3 8B 相当但算力少 6.6×。 https://arxiv.org/abs/2406.11794
- **CCI3.0-HQ** (北京智源 BAAI, 2024-10, paper) — 500GB 高质量中文预训练语料（CCI3.0 精选子集），两阶段混合过滤流水线把 Qwen2-72B-instruct 的质量判别力蒸馏进 0.5B 紧凑分类器；用 100B token 从头训 0.5B 验证，10 项零样本基准超 CCI3.0/SkyPile/WanjuanV1，数据与分类器全开源。 https://arxiv.org/abs/2410.18505

### 数据质量 / 合成数据路线（phi 流派）

- **Textbooks Are All You Need (phi-1)** (Microsoft Research, 2023-06, paper) — 1.3B 代码模型，用约 7B token（6B 分类器筛选的教材质量网络代码 + 1B GPT-3.5 合成教材习题）+ 180M 合成练习微调，8×A100 训 4 天，HumanEval 50.6%；开启「数据质量 > 规模」的小模型流派。 https://arxiv.org/abs/2306.11644
- **Textbooks Are All You Need II (phi-1.5)** (Microsoft Research, 2023-09, paper) — 1.3B 常识推理模型，约 30B token（其中约 20B 为 GPT-3.5 合成的教材式常识推理数据，几乎无网络文本），性能媲美 5× 大模型，且因无 web 数据毒性更低。 https://arxiv.org/abs/2309.05463
- **Phi-2: The surprising power of small language models** (Microsoft Research, 2023-12, blog) — 2.7B，1.4T token（合成 + 精选网络），96×A100 训 14 天；教材级数据 + 从 phi-1.5 嵌入式知识迁移加速收敛，<13B 基础模型中推理/语言理解 SOTA。 https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/
- **Phi-3 Technical Report** (Microsoft, 2024-04, report) — phi-3-mini 3.8B / 3.3T token（重过滤网页 + 合成数据的「data optimal regime」），MMLU 69%、可手机本地运行；phi-3-small 7B / phi-3-medium 14B 训 4.8T token（MMLU 75%/78%）；含 phi-3.5-MoE 与 Vision。 https://arxiv.org/abs/2404.14219
- **Phi-4 Technical Report** (Microsoft, 2024-12, report) — 14B，约 10T token，合成数据贯穿预训练全程（多样化 prompt、自修订、指令逆转）；在 GPQA/MATH 等 STEM QA 上反超其 teacher GPT-4，证明数据生成 + 后训练超越纯蒸馏；后训练含 pivotal token DPO。 https://arxiv.org/abs/2412.08905
- **Phi-4-Mini Technical Report** (Microsoft, 2025-03, report) — 3.8B，高质量 web + 合成数据（侧重数学/编码），媲美 2× 大模型；词表扩到 200K 支持多语言 + GQA；Phi-4-Multimodal 用 Mixture-of-LoRAs 把文/视/音三模态融入单模型互不干扰，语音 LoRA 仅 460M 即登顶 OpenASR。 https://arxiv.org/abs/2503.01743
- **Phi-4-reasoning Technical Report** (Microsoft, 2025-04, report) — 14B 推理模型，SFT 用精选「可教(teachable)」prompts + o3-mini 生成的推理示范数据；reasoning-plus 再加 outcome-based RL 生成更长 trace；超更大的 DeepSeek-R1-Distill-Llama-70B、逼近完整 R1。 https://arxiv.org/abs/2504.21318
- **Phi-4-reasoning-vision-15B** (Microsoft Research, 2026-03, report) — 15B 紧凑多模态推理模型，强调「数据质量是性能首要杠杆」（系统化过滤 + 纠错 + 合成增强）；用显式 mode token 混合推理/非推理数据；高分辨率/动态分辨率视觉编码器带来一致增益。 https://www.microsoft.com/en-us/research/wp-content/uploads/2026/03/Phi-4-reasoning-vision-15B-Tech-Report.pdf

### 领域专门语料

- **Evaluating LLMs Trained on Code (Codex)** (OpenAI, 2021-07, paper) — 在 5400 万 GitHub 仓库的 159GB Python 上微调 GPT，发布 HumanEval（164 题，pass@k）；pass@1 28.8%、pass@100 70.2%；GitHub Copilot 底座。 https://arxiv.org/abs/2107.03374
- **CodeGen** (Salesforce Research, 2022-03, paper) — 350M–16.1B 代码模型，三阶段渐进式数据（自然语言 The Pile → 多语言代码 BigQuery → 单语 Python BigPython）；提出多轮程序合成范式与 MTPB 基准，开源 JAXFORMER。 https://arxiv.org/abs/2203.13474
- **Solving Quantitative Reasoning Problems (Minerva)** (Google Research, 2022-06, paper) — 在 PaLM(8B/62B/540B) 上用 118GB 数学/科学内容（arXiv LaTeX + 数学网页）继续预训练 26B–38.5B token，关键是保留 LaTeX/数学格式不剥离；MATH 50.3%（540B + 多数投票），不调外部工具。 https://arxiv.org/abs/2206.14858
- **Galactica: A Large Language Model for Science** (Meta AI, 2022-11, paper) — 125M–120B 科学专用模型，约 106B token 高质量科学语料（4800 万篇论文、教科书、知识库、蛋白序列、SMILES）；用 `<work>`/`[START_REF]` 等特殊 token，仅训 4 epoch（高质量小语料可多轮）；demo 因幻觉争议 3 天下线。 https://arxiv.org/abs/2211.09085
- **Code Llama** (Meta AI, 2023-08, paper) — 基于 Llama 2 继续训练 500B 代码 token（Python 版再 +100B），16k 训练序列经 RoPE θ=1e6 外推到 100k；7B/13B/70B 支持 FIM 填充；HumanEval 67%/MBPP 65%。（同工作博客版并入此条。） https://arxiv.org/abs/2308.12950
- **DeepSeek-Coder** (DeepSeek-AI, 2024-01, paper) — 1.3B–33B，2T token（87% 代码 + 10% 代码相关英文 + 3% 中文，87 种语言）；仓库级（repo-level）预训练 + FIM，16K 上下文；33B-Base 超 CodeLlama-34B。 https://arxiv.org/abs/2401.14196
- **DeepSeekMath** (DeepSeek-AI, 2024-02, paper) — 从 DeepSeek-Coder-Base-v1.5 7B 继续训练 500B token；自建 DeepSeekMath Corpus 120B 数学 token（用 fastText 从去重 CC 的 40B 页迭代召回 35.5M 数学网页），混合 56% 数学语料 + AlgebraicStack + arXiv + GitHub + CC；MATH 51.7%（无工具）；首提 GRPO。 https://arxiv.org/abs/2402.03300
- **DeepSeek-Coder-V2** (DeepSeek-AI, 2024-06, paper) — 从 DeepSeek-V2 中间 checkpoint 续训 +6T token（60% 源代码 + 10% 数学 + 30% 自然语言）；编程语言 86→338 种、上下文 16K→128K；代码任务比肩 GPT-4-Turbo。 https://arxiv.org/abs/2406.11931
- **Qwen2.5-Coder** (阿里 Qwen Team, 2024-09, paper) — 基于 Qwen2.5 续训 5.5T+ token（源代码 + 文本-代码 grounding + 合成数据 + 均衡配比）；next-token + FIM；六档 0.5B–32B，32B-Instruct 为当时最强开源代码模型。 https://arxiv.org/abs/2409.12186
- **Qwen2.5-Math** (阿里 Qwen Team, 2024-09, paper) — 1.5B/7B/72B，把「自我改进」贯穿全流程：预训练用 Qwen2-Math-Instruct 生成大规模高质量数学数据，后训练 RM 迭代演化 SFT 数据 + RL；支持中英 CoT 与 TIR（工具集成推理）。 https://arxiv.org/abs/2409.12122
- **Yi-Coder** (零一万物 01.AI, 2024-09, model-card) — 1.5B/9B（<10B）代码模型，从 Yi 系列基座持续预训练；支持 52 种编程语言、128K 上下文。 https://huggingface.co/01-ai/Yi-Coder-9B-Chat
- **DeepSeekMath-GRPO** (DeepSeek-AI, 2024-02, paper) — 见上 DeepSeekMath（同 arXiv 2402.03300，themes/ 的 GRPO 切面条目并入主条）。 https://arxiv.org/abs/2402.03300

---

## 三、英文/西方阵营基础模型预训练实践

### 2020–2021：早期大模型与对话/检索

- **Towards a Human-like Open-Domain Chatbot (Meena)** (Google Brain, 2020-01, paper) — 2.6B Evolved Transformer 对话模型，341GB 过滤社交媒体对话（比 GPT-2 数据多 8.5×）；提出 SSA 指标并发现困惑度与对话质量强相关（R²≈0.93）。 https://arxiv.org/abs/2001.09977
- **REALM — Retrieval-Augmented LM Pre-Training** (Google Research, 2020-02, paper) — 首次在预训练阶段端到端学神经检索器，MLM 时从约 1300 万 Wikipedia 文档块检索 top-k（检索为隐变量，MIPS 索引异步刷新）；提出 salient span masking 引导学世界知识。 https://arxiv.org/abs/2002.08909
- **ELECTRA** (Google Brain / Stanford, 2020-03, paper) — 用替换 token 检测(RTD)替代 BERT 的 MLM，损失作用于全部 token（而非 15% 掩码位）大幅提升样本效率；数据同 BERT/RoBERTa（Wikipedia + BookCorpus），small 版单 GPU 4 天超 GPT。 https://arxiv.org/abs/2003.10555
- **Dense Passage Retrieval (DPR)** (Meta FAIR/UW/Princeton, 2020-04, paper) — 双塔 BERT 稠密检索 + in-batch negatives + 困难负样本，top-20 准确率较 BM25 高 9–19 点；成为 RAG/REALM 标准检索组件。 https://arxiv.org/abs/2004.04906
- **Recipes for building an open-domain chatbot (BlenderBot)** (Meta FAIR, 2020-04, paper) — 90M/2.7B/9.4B 对话模型，约 15 亿条 Reddit 对话预训练 + Blended Skill Talk 微调，强调解码策略对质量影响巨大；人评胜 Meena。 https://arxiv.org/abs/2004.13637
- **RAG — Retrieval-Augmented Generation** (Meta FAIR/UCL, 2020-05, paper) — 把参数化记忆(BART)与非参数化记忆(DPR 检索的稠密 Wikipedia 索引，约 2100 万块)端到端结合；提出 RAG-Sequence/RAG-Token；可替换索引实现知识更新而无需重训。 https://arxiv.org/abs/2005.11401
- **Language Models are Few-Shot Learners (GPT-3)** (OpenAI, 2020-05, paper) — 175B 模型，约 3000 亿 token（CC 过滤后约 410B/权重 60%、WebText2 22%、Books1+2 16%、Wikipedia 3%，高质量数据采样权重高于占比）；CC 做相似度过滤 + 模糊去重 + 与评测集去重；证明纯规模即可 few-shot in-context learning。 https://arxiv.org/abs/2005.14165
- **Jurassic-1** (AI21 Labs, 2021-08, report) — J1-Jumbo 178B（76 层）/ J1-Large 7.5B，关键创新是 256K 超大 SentencePiece 词表（tokens-per-byte 效率远高于 GPT-3/T5 的 ~32K-50K），等价更快推理与更长有效上下文。 https://www.ai21.com/blog/announcing-ai21-studio-and-jurassic-1
- **Improving LMs by retrieving from trillions of tokens (RETRO)** (DeepMind, 2021-12, paper) — 用 2 万亿 token 检索数据库（MassiveText 同源）+ chunked cross-attention + 冻结 BERT 检索器增强自回归 LM，以约 25× 更少参数达 GPT-3/Jurassic-1 水平；可给已有 Transformer 后加检索（RETROfit），半参数化扩展路线代表。 https://arxiv.org/abs/2112.04426
- **GLaM: Efficient Scaling with Mixture-of-Experts** (Google, 2021-12, paper) — 稀疏 MoE 把总参扩到 1.2T（每 MoE 层 64 专家 top-2，每 token 激活约 97B），1.6T token 高质量语料（含来源混合权重）；训练能耗仅 GPT-3 的 1/3、推理 FLOPs 一半，29 任务综合超 GPT-3。 https://arxiv.org/abs/2112.06905
- **Scaling Language Models (Gopher)** (DeepMind, 2021-12, paper) — 280B 稠密 Transformer（80 层），所有模型训练 300B token，配套 MassiveText 语料（质量过滤 + 去重 + test-set overlap 移除）；规模在阅读理解/事实核查收益大、逻辑数学收益小。 https://arxiv.org/abs/2112.11446
- **Megatron-Turing NLG 530B (MT-NLG)** (Microsoft & NVIDIA, 2021-10 公告 / 2022-01 论文, paper) — 530B 稠密单体 Transformer，当时最大；DeepSpeed + Megatron 3D 并行，560 个 DGX A100（4480 GPU）bf16；强调精心设计的训练语料与数据清洗(去重)是成功关键。（2021/2022 两索引为同一工作，已合并。） https://arxiv.org/abs/2201.11990

### 2022：稠密/MoE 旗舰与多模态/多语言

- **LaMDA: Language Models for Dialog Applications** (Google Research, 2022-01, paper) — 2B/8B/137B 对话模型，1.56T 词公开对话 + 网页预训练；安全微调（人类价值 + 安全分类器过滤）与事实接地（调用检索/计算器/翻译工具）显著优于单纯缩放。 https://arxiv.org/abs/2201.08239
- **PaLM: Scaling Language Modeling with Pathways** (Google Research, 2022-04, paper) — 540B 稠密 Transformer（118 层、MQA），780B token（网页/书籍/维基/对话/GitHub）；6144 TPU v4、MFU 46.2%；SwiGLU + RoPE + 并行 Attention/FFN + 256K 词表；BIG-bench 超人类平均。 https://arxiv.org/abs/2204.02311
- **GPT-NeoX-20B** (EleutherAI, 2022-04, paper) — 20B（44 层），在 the Pile 上训约 472B token；RoPE（部分维度）+ 并行 Attention/FFN；基于 Pile 重训的 BPE（50432 词表，对空白/代码友好），完整开源训练代码与权重。 https://arxiv.org/abs/2204.06745
- **Super-NaturalInstructions / Tk-Instruct** (AllenAI/UW 等, 2022-04, paper) — 1616 个 NLP 任务（76 类、55 语言）带专家指令的基准；Tk-Instruct(11B) 在未见任务上超 InstructGPT(175B) 约 9+ 点，证明指令多样性比纯规模更利于泛化。 https://arxiv.org/abs/2204.07705
- **Flamingo: a Visual Language Model for Few-Shot Learning** (DeepMind, 2022-04, paper) — 冻结视觉编码器(NFNet) + 冻结 LM(Chinchilla 70B) + Perceiver Resampler + gated xattn-dense；在 M3W 交错图文网页 + 图文对 + 视频文本上训练，支持多模态 in-context few-shot；3B/9B/80B。 https://arxiv.org/abs/2204.14198
- **OPT: Open Pre-trained Transformer** (Meta AI, 2022-05, paper) — 125M–175B，约 180B token（RoBERTa 语料 + Pile 子集 + PushShift Reddit）；OPT-175B 性能比肩 GPT-3 但碳足迹仅 1/7，992×A100 FP16，公开训练 logbook。 https://arxiv.org/abs/2205.01068
- **UL2: Unifying Language Learning Paradigms** (Google Research, 2022-05, paper) — Mixture-of-Denoisers（R/S/X 去噪器）+ mode switching 统一预训练目标；UL2-20B encoder-decoder 在 C4 上训约 1T token，超 T5-XXL 与 GPT-like baseline。 https://arxiv.org/abs/2205.05131
- **Beyond the Imitation Game (BIG-bench)** (Google 等 132 机构, 2022-06, paper) — 204 个任务、450 作者协作的评测套件，专测超出当前模型能力的任务；发现性能随规模平滑 + 部分任务涌现式提升，是 LLM 评测基础设施基石。 https://arxiv.org/abs/2206.04615
- **Atlas: Few-shot Learning with Retrieval Augmented LM** (Meta AI, 2022-08, paper) — Contriever 检索器 + Fusion-in-Decoder(11B) 阅读器联合预训练；64 例即在 NaturalQuestions 达 >42%（超 540B PaLM，参数少约 50×），文档索引可热更新。 https://arxiv.org/abs/2208.03299
- **Challenging BIG-Bench Tasks (BBH)** (Google Research/Stanford, 2022-10, paper) — 从 BIG-bench 筛 23 个模型尚未超人类的硬任务；加 CoT 后 PaLM 在 10/23、Codex 在 17/23 上超人类平均，说明瓶颈常是提示方式而非模型能力。 https://arxiv.org/abs/2210.09261
- **BLOOM: 176B 开放多语言模型** (BigScience, 2022-11, paper) — 176B（70 层），ROOTS 语料约 1.6TB / 约 366B token（46 自然语言 + 13 编程语言）；ALiBi + 250680 字节级 BPE 词表；Jean Zay 384×A100，Megatron-DeepSpeed 3D 并行训 118 天，权重/数据/过程全公开。 https://arxiv.org/abs/2211.05100
- **Whisper — Robust Speech Recognition** (OpenAI, 2022-12, paper) — encoder-decoder，680,000 小时弱监督音频-文本对（约 11.7 万小时多语言 + 12.5 万翻译）；用特殊 token 统一转写/翻译/语种/时间戳多任务，zero-shot 即媲美有监督 SOTA。 https://arxiv.org/abs/2212.04356

### 2023–2024：开源底座、多模态预训练、数据透明

- **LLaMA: Open and Efficient Foundation LM** (Meta AI, 2023-02, paper) — 7B/13B/33B/65B，1.0–1.4T token 全公开数据（CC 67% + C4 15% + GitHub 4.5% + Wikipedia 4.5% + Books 4.5% + ArXiv 2.5% + StackExchange 2%）；RMSNorm + SwiGLU + RoPE；13B 超 GPT-3(175B)，开启开源浪潮。 https://arxiv.org/abs/2302.13971
- **GPT-4 Technical Report** (OpenAI, 2023-03, paper) — 多模态自回归 Transformer，刻意不披露架构/数据/token/算力/上下文具体数字；亮点是可预测扩展（用 <1/1000 算力的小模型外推 GPT-4 的 loss 与 HumanEval）。 https://arxiv.org/abs/2303.08774
- **PaLM 2 Technical Report** (Google, 2023-05, report) — 遵循 Chinchilla 计算最优（参数比 PaLM 540B 小但数据更多，具体数字未明示）；mixture of objectives 训练目标，更高比例多语言与代码数据（数百种语言）；驱动 Bard/Duet/Med-PaLM 2。 https://arxiv.org/abs/2305.10403
- **RedPajama-INCITE 3B/7B** (Together AI, 2023-05, blog) — 用复刻 LLaMA 配方的开放数据集 RedPajama v1（约 1.2T token）训练，3B/7B 各含 base/chat/instruct；7B 训到 800B 即超 Pythia 7B，Apache 2.0 可商用。 https://www.together.ai/blog/redpajama-models-v1
- **Llama 2** (Meta AI, 2023-07, paper) — 7B/13B/34B/70B，预训练 2.0T token（比 Llama1 多 40%），4096 上下文；34B/70B 用 GQA；约 3.3M GPU-hours；含详尽 RLHF/安全方法论。 https://arxiv.org/abs/2307.09288
- **Effective Long-Context Scaling (Llama 2 Long)** (Meta AI, 2023-09, paper) — 从 Llama 2 继续预训练约 400B token（长文本上采样 + 增大 RoPE base θ）扩到 32k 上下文；关键发现「预训练里大量长文本非关键，长上下文继续预训练比从头长序列更高效」；70B 长任务超 gpt-3.5-turbo-16k。 https://arxiv.org/abs/2309.16039
- **Gemini: A Family of Highly Capable Multimodal Models** (Google DeepMind, 2023-12, report) — Ultra/Pro/Nano 三档，原生多模态（文/图/音/视频从一开始联合训练而非视觉适配器拼接）；Ultra MMLU 90.0%（首超人类专家）；TPUv4/v5e + Jax/Pathways。 https://arxiv.org/abs/2312.11805
- **Nemotron-4 15B** (NVIDIA, 2024-02, report) — 15B，8T token（英文 + 53 种语言 + 43 编程语言）；RoPE + squared ReLU + GQA + 256K SentencePiece 词表；多语言同级最佳（超 4× 大模型）。 https://arxiv.org/abs/2402.16819
- **OLMo: Accelerating the Science of Language Models** (AI2, 2024-02, paper) — 真正全开放：权重 + Dolma 数据 + 训练/评估代码 + W&B 日志 + 中间 checkpoint；1B/7B（7B 训约 2.46T token），无 bias + SwiGLU + RoPE。 https://arxiv.org/abs/2402.00838
- **MM1: Methods, Analysis & Insights from Multimodal LLM Pre-training** (Apple, 2024-03, paper) — 多模态预训练系统消融：image-caption + 交错图文 + 纯文本的混合对 few-shot 至关重要，图像分辨率/image token 数/编码器 >> 视觉语言连接器设计；3B/7B/30B（含 MoE）。 https://arxiv.org/abs/2403.09611
- **Introducing DBRX** (Databricks/Mosaic, 2024-03, blog) — 细粒度 MoE，132B 总参/36B 激活，16 专家选 4（比 Mixtral/Grok 更细粒度）；12T token（估计 token-for-token 比 MPT 数据好至少 2×）+ 课程学习调整数据混合；32K 上下文。 https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm
- **The Llama 3 Herd of Models** (Meta, 2024-07, paper) — 405B 稠密 Transformer（另 8B/70B），约 15.6T token，128K 词表 + 28K 额外；数据配比约 50% 通用知识 + 25% 数学/推理 + 17% 代码 + 8% 多语言；405B 用 3.8×10^25 FLOPs、最多 16K H100、4D 并行 BF16。（8B/70B/405B 官方博客并入此条。） https://arxiv.org/abs/2407.21783
- **OLMoE: Open Mixture-of-Experts Language Models** (AI2, 2024-09, paper) — 全开放稀疏 MoE，1B 激活/7B 总参，64 细粒度专家 top-8，5T token 预训练（含 load balancing/router z-loss）；dropless 路由优于共享专家，超 Llama2-13B-Chat。 https://arxiv.org/abs/2409.02060
- **MM1.5** (Apple, 2024-09, paper) — 以数据为中心研究全训练周期数据混合：高质量 OCR + 合成 caption 持续预训练 + 优化的视觉指令微调；1B–30B（含 MoE），出 Video 与 UI 专用变体。 https://arxiv.org/abs/2409.20566
- **Molmo and PixMo** (AI2, 2024-09, paper) — 完全开放（权重+数据）VLM，不依赖闭源 VLM 蒸馏；PixMo 含高细节 caption（语音转写）、自由问答、创新的 2D pointing 数据；72B 超 Claude 3.5 Sonnet/Gemini 1.5 Pro，仅次于 GPT-4o。 https://arxiv.org/abs/2409.17146
- **Pixtral 12B** (Mistral AI, 2024-10, paper) — 首个多模态、从零训练的 Pixtral-ViT(400M) 可按原生分辨率/宽高比处理图像（RoPE-2D），128K 上下文处理任意数量图片，纯文本能力不退化；超 Llama-3.2 90B（小 7×），Apache 2.0。 https://arxiv.org/abs/2410.07073
- **Movie Gen: A Cast of Media Foundation Models** (Meta, 2024-10, report) — 30B 视频生成 Transformer（flow matching，最大 73K 视频 token = 16s@16fps）+ 13B 音频模型；时空压缩 TAE 潜空间；文本编码器组合 UL2/ByT5/MetaCLIP。 https://arxiv.org/abs/2410.13720
- **Byte Latent Transformer (BLT)** (Meta FAIR/UW/U.Chicago, 2024-12, paper) — 无 tokenizer 字节级 LLM，按「下一字节熵」动态切成可变长 patch 作为计算单元；首个 FLOP 受控的字节级扩展研究（8B、4T 字节），等 FLOP 匹配 BPE 模型且更鲁棒。 https://arxiv.org/abs/2412.09871

### 2025：低成本预训练、全开放数据课程、原生多模态

- **OLMo 2 (2 OLMo 2 Furious)** (AI2, 2025-01, report) — 7B/13B/32B 全开放稠密模型（权重+完整训练数据+代码+日志全公开）；两阶段数据课程：大规模 web 预训练 olmo-mix-1124 + 高质量 mid-training dolmino-mix-1124（含数学专项 mix）；架构/初始化改动(RMSNorm/QK-norm)提升稳定性；后训练 Tülu 3 风格 SFT+DPO+RLVR。 https://arxiv.org/abs/2501.00656
- **OLMo 2 32B** (AI2, 2025-03, blog) — OLMo 2 家族最大模型，训至 6T token + Tülu 3.1 后训练；首个完全开放且在多技能学术基准超 GPT-3.5-Turbo 与 GPT-4o mini 的模型，训练成本约 Qwen 2.5 32B 的 1/3。 https://allenai.org/blog/olmo2-32B
- **OpenAI GPT-4.5 System Card** (OpenAI, 2025-02, system-card) — 规模最大、知识最广的非推理 GPT 模型，靠扩展无监督学习（更多算力+数据+架构优化）减少幻觉；用「从更小模型蒸馏数据训更大模型」的可扩展对齐技术；不披露参数/token 等架构数字，Preparedness 评级 Medium。 https://openai.com/index/gpt-4-5-system-card/
- **The Amazon Nova Family of Models** (Amazon AGI, 2025-03, technical-report) — Pro/Lite/Micro 理解模型 + Canvas(图像)/Reel(视频) 生成模型族；强调 agentic、长上下文与多模态（Lite/Pro 支持图像/视频/文档/文本输入），含负责任 AI 实践。 https://www.amazon.science/publications/the-amazon-nova-family-of-models-technical-report-and-model-card
- **Gemma 3 Technical Report** (Google DeepMind, 2025-03, technical-report) — 1B–27B 轻量多模态开放模型，新增视觉理解 + ≥128K 长上下文；提高 local:global 注意力层比 + 缩短 local 跨度抑制长上下文 KV-cache 爆炸；知识蒸馏训练 + 新 post-training 配方；27B-IT ≈ Gemini-1.5-Pro。 https://arxiv.org/abs/2503.19786
- **Llama 4 herd (Scout/Maverick/Behemoth)** (Meta AI, 2025-04, blog) — 首批原生多模态(early fusion)+ 首次 MoE 的开放 Llama；>30T token（>2× Llama 3）、200 种语言（多语 token ≈10× Llama 3）、FP8 预训练；Scout 10M 上下文，Behemoth ~2T 总参作蒸馏教师；iRoPE + MetaP 超参迁移。 https://ai.meta.com/blog/llama-4-multimodal-intelligence/
- **Apple Foundation Models 2025** (Apple, 2025-07, technical-report) — ~3B 端侧模型（KV-cache 共享 + 2-bit QAT）+ Parallel-Track MoE (PT-MoE) 服务器模型；训练于大规模多语言多模态数据（负责任 web 爬取 + 授权语料 + 高质量合成数据），SFT + 异步 RL，支持图像理解与工具调用。 https://machinelearning.apple.com/research/apple-foundation-models-tech-report-2025
- **Nemotron Nano 2** (NVIDIA, 2025-08, technical-report) — 基于 Nemotron-H 的 hybrid Mamba-Transformer 推理模型，先 FP8 在 20T token 上预训练 12B 基座再 Minitron 压缩蒸馏到 9B；单张 A10G 可 128k 推理，reasoning 吞吐相对 Qwen3-8B 最高 6×；多数预/后训练数据集随权重开源。 https://arxiv.org/abs/2508.14444

### 2026：低精度预训练、百万上下文、个人超智能

- **GPT-5.5 Instant System Card** (OpenAI, 2026-05, model-card) — ChatGPT 默认模型；训练数据为互联网公开信息 + 第三方合作 + 用户/训练员数据，用先进过滤减少个人信息、安全分类器减少有害内容(含 CSAM)；首个按网络安全与生化 Preparedness「High」处理的 Instant 模型。 https://openai.com/index/gpt-5-5-instant-system-card/
- **System Card: Claude Opus 4.6** (Anthropic, 2026-02, model-card) — 预训练数据截止 2025-05（公开信息 + 第三方非公开 + 标注承包商 + 用户 opt-in + 内部生成），去重/分类清洗，爬虫遵守 robots.txt；后训练 RLHF + RLAIF；新增 adaptive thinking 模式 + 四档 effort。 https://www.anthropic.com/system-cards
- **Gemini 3 Pro Model Card** (Google DeepMind, 2026-05 更新, model-card) — 稀疏 MoE Transformer，原生多模态；预训练数据为大规模多领域多模态（公开网页/文本/代码/图像/音频/视频 + 商业授权 + Google 产品用户数据）；后训练含指令微调 + RL（多步推理/定理证明）+ 人类偏好；TPU + JAX/Pathways。 https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Pro-Model-Card.pdf
- **Molmo2** (AI2/UW, 2026-01, paper) — 完全开放（权重/数据/代码）视频-语言模型（4B/8B/O-7B），训练于迄今最大的开放视频中心多模态语料之一（9 个新数据集：密集视频字幕、长视频 QA、开放词表 pointing/tracking）；支持像素级 grounding。 https://arxiv.org/abs/2601.10611
- **DeepSeek-OCR 2: Visual Causal Flow** (DeepSeek, 2026-01, paper) — DeepEncoder V2 让视觉编码器具备因果推理、按图像语义动态重排视觉 token，打破固定光栅扫描顺序；提出把 2D 图像理解建模为视觉因果流。 https://arxiv.org/abs/2601.20552
- **Stable-DiffCoder** (字节跳动 Seed, 2026-01, paper) — 8B 代码扩散 LLM，建立在 Seed-Coder 架构/数据/pipeline 上，引入 block diffusion 持续预训练（CPT）+ 定制 warmup + block-wise clipped noise schedule；相同数据/架构下扩散训练可超越纯 AR 代码模型。 https://arxiv.org/abs/2601.15892
- **Introducing Muse Spark** (Meta Superintelligence Labs, 2026-04, blog) — 原生多模态推理模型，9 个月重建预训练栈（架构/优化/数据整理），拟合 scaling law 后达同等能力所需训练 FLOPs 比 Llama 4 Maverick 少 >10×；三条 scaling 轴 + Contemplating 多 agent 模式；健康数据与 1000+ 医生合作整理。 https://ai.meta.com/blog/introducing-muse-spark-msl/
- **Nemotron 3 Super** (NVIDIA, 2026-04, paper) — 120B 总/12B 激活混合 Mamba-Attention MoE，25T token，首次 NVFP4 精度预训练 + LatentMoE + MTP；1M 上下文，吞吐相比 GPT-OSS-120B 2.2×/Qwen3.5-122B 7.5×，全开源。 https://arxiv.org/abs/2604.12374
- **Nemotron 3 Nano Omni** (NVIDIA, 2026-04, paper) — 建立在 Nemotron 3 Nano 30B-A3B backbone，首个原生支持音频（连同文/图/视频）的全模态模型；C-RADIOv4-H1 视觉 + Parakeet-TDT-0.6B-v2 音频编码器 + 多模态 token 缩减；BF16/FP8/FP4 检查点。 https://arxiv.org/abs/2604.24954
- **Nemotron 3 Ultra** (NVIDIA, 2026-06, paper) — 550B 总/55B 激活 MoE 混合 Mamba-Attention，20T 文本 token + 扩到 1M 上下文；NVFP4 预训练 + LatentMoE + MTP；后训练 SFT + RL + 多教师在线策略蒸馏(MOPD) + 推理预算控制；吞吐相比 SOTA 最高约 6×，全开源（含数据+配方）。 https://arxiv.org/abs/2606.15007

---

## 四、中国阵营基础模型预训练实践

### 2020–2021：中文大模型起步、国产算力、多模态

- **CPM** (清华 / BAAI, 2020-12, paper) — 中国首个大规模生成式中文模型，最大 2.6B（CPM-Large 32 层），约 100GB 中文语料（百科/网页/电子书/新闻/对话）；中文 tokenizer 先分词再建子词词表（约 3 万）避免序列过长；开源权重。 https://arxiv.org/abs/2012.00413
- **M6: A Chinese Multimodal Pretrainer** (阿里 / 清华, 2021-03, paper) — 中文图文多模态预训练，构建当时最大中文多模态语料（>1.9TB 图像 + 292GB 文本）；统一多模态 Transformer 做 VQA/图文匹配/图像描述/文生图等，是阿里后续万亿/十万亿 MoE(M6-T) 的基础。 https://arxiv.org/abs/2103.00823
- **PanGu-α** (华为 / 鹏城实验室, 2021-04, report) — 最大 200B 中文自回归模型（另 2.6B/13B），1.1TB 高质量多领域中文语料；2048×Ascend 910 + MindSpore 五维自动并行；自回归 + query layer。 https://arxiv.org/abs/2104.12369
- **CogView: Mastering Text-to-Image Generation** (清华 / 阿里 / BAAI, 2021-05, paper) — 4B Transformer + VQ-VAE 的中文文生图（中国版 DALL·E），把图像离散化为 token 与文本拼接自回归；PB-Relax/Sandwich-LayerNorm 稳定训练；blurred MS COCO FID SOTA。 https://arxiv.org/abs/2105.13290
- **ERNIE 3.0** (百度, 2021-07, paper) — 10B 知识增强统一预训练，融合自回归 + 自编码网络（理解 + 生成共享底层）；4TB 语料 = 纯文本 + 大规模知识图谱注入（universal knowledge-text prediction）；54 个中文任务 SOTA。 https://arxiv.org/abs/2107.02137
- **HyperCLOVA** (NAVER, 2021-09, paper) — 首个面向韩语的十亿至千亿级（最大约 82B）GPT-3 式模型，用 NAVER 自建大规模韩语语料训练；探索 prompt-based learning 与 in-context learning，配韩语专用 tokenizer。 https://arxiv.org/abs/2109.04650
- **Yuan 1.0 (源 1.0)** (浪潮 Inspur, 2021-10, paper) — 245B 中文单体稠密模型（2021 年最大中文稠密），5TB 高质量中文语料（自研清洗管线）；把分布式训练性能纳入架构协同设计；calibration + label expansion 提升 zero/few-shot。 https://arxiv.org/abs/2110.04725

### 2022：双语 MoE 与多模态生成

- **GLM-130B: An Open Bilingual Pre-trained Model** (清华 / 智谱, 2022-10, paper) — 130B 中英双语（GLM 自回归空白填充目标，70 层），400B token（中英各约 200B）；DeepNorm + RoPE 稳定深层训练；768×A100 训 60 天；独创无训练后 INT4 量化可在 4×RTX 3090 推理。 https://arxiv.org/abs/2210.02414
- **ERNIE-ViLG 2.0** (百度, 2022-10, paper) — 约 24B 中文文生图扩散模型，细粒度文本/视觉知识增强 + 去噪专家混合(MoDE，按时间步分段用不同专家)；MS-COCO zero-shot FID 6.75 SOTA。 https://arxiv.org/abs/2210.15257

### 2023：开源底座爆发、双语数据透明、代码/多模态

- **ChatGLM-6B** (智谱 / 清华 KEG, 2023-03, github) — 首个开源中英双语对话模型，GLM 架构 6B，约 1T 双语 token + SFT/反馈自助/RLHF；INT4 量化仅需 6GB 显存，引爆国内开源热潮。 https://github.com/THUDM/ChatGLM-6B
- **CodeGeeX** (智谱 / 清华 KEG, 2023-03, paper) — 13B 多语言代码模型（39 层 + Top Query Layer），158B token 代码语料（23 种语言）训练消耗 850B token；完全在 1536×Ascend 910 + MindSpore 训约两月，国产算力训大模型代表；配套 HumanEval-X 多语言基准。 https://arxiv.org/abs/2303.17568
- **MOSS** (复旦大学 OpenMOSS, 2023-04, github) — 中国首个公开支持插件/工具调用的开源对话模型，moss-moon-003-base 16B 约 700B 单词预训练（约 6.67×10²² FLOPs）；110 万条多轮对话 SFT + 30 万条插件增强对话 + 偏好模型。 https://github.com/OpenMOSS/MOSS
- **CPM-Bee** (面壁 / 清华 OpenBMB, 2023-05, github) — 10B 中英双语基座，>1T 高质量语料（严格筛选/清洗/配比）；配 OpenBMB 全栈工具(BMTrain/BMCook/BMInf)；衍生 WebCPM/VisCPM，是 MiniCPM 前身脉络。 https://github.com/OpenBMB/CPM-Bee
- **InternLM (第一代)** (上海 AI Lab / 商汤, 2023-06, technical-report) — 104B 参数 / 1.6T token 多语言高质量语料（网页/书籍/学术/代码），多阶段渐进式预训练；自研 Uniscale-LLM 可在 2048 GPU 稳定训 200B+；综合考试基准超开源且优于 ChatGPT。 https://github.com/InternLM/InternLM-techreport
- **Baichuan-7B** (百川智能, 2023-06, github) — 首个开源模型，7B / 约 1.2T token 中英双语，4096 上下文；LLaMA 风格(RoPE+SwiGLU+RMSNorm)，64K BPE 词表；C-Eval/MMLU 同尺寸最佳。 https://github.com/baichuan-inc/Baichuan-7B
- **ChatGLM2-6B** (智谱 / 清华 KEG, 2023-06, github) — GLM 混合目标 1.4T 中英标识符 + 人类偏好对齐；FlashAttention 把上下文 2K→32K（对话 8K 训练），MQA 推理提速 42%；相对初代 GSM8K +571%、MMLU +23%。 https://github.com/THUDM/ChatGLM2-6B
- **CodeGeeX2** (智谱 / 清华 KEG, 2023-07, github) — 基于 ChatGLM2-6B 架构 + 600B 代码预训练，6B 即超 15B StarCoder 近 10%（HumanEval Python 35.9%）；8192 上下文，量化后 6GB 显存可部署。 https://github.com/THUDM/CodeGeeX2
- **Qwen-VL** (阿里 / Qwen Team, 2023-08, paper) — Qwen-7B + OpenCLIP ViT-bigG + 位置感知视觉适配器（压缩到 256 query）；三阶段训练（VL 预训练 → 多任务高分辨 448 → SFT），对齐 image-caption-box 三元组实现 grounding 与 OCR。 https://arxiv.org/abs/2308.12966
- **XVERSE-13B** (深圳元象, 2023-08, github) — 多语言模型支持 40+ 语言，8K 上下文（后扩 256K）；v2 版训练量 1.4T→3.2T token + 工具调用；100534 BPE 词表原生多语言，千卡 MFU 58.5%。 https://github.com/xverse-ai/XVERSE-13B
- **Qwen Technical Report** (阿里 / Qwen Team, 2023-09, paper) — 1.8B/7B/14B（分别训 2.2T/2.4T/3.0T token），多领域文本+代码，exact-match + MinHash 去重 + 语言判别后增配高质量数据；tokenizer 基于 cl100k_base 扩中文，词表约 152K。 https://arxiv.org/abs/2309.16609
- **Baichuan 2** (百川智能, 2023-09, paper) — 7B/13B 从零训练 2.6T token；7B 用 RoPE、13B 用 ALiBi；BPE 词表 64K→125696；NormHead + Max-z loss 稳定训练；公开 200B→2.6T 全过程 checkpoint。 https://arxiv.org/abs/2309.10305
- **Skywork-13B** (昆仑万维 天工, 2023-10, paper) — 13B / 3.2T token 双语，两阶段训练（通用 → 领域增强）；开源 SkyPile-150B（约 600GB/150B token，已知最大开源中文网页语料）+ 中间 checkpoint；提出基于 LM loss 的数据泄漏检测。 https://arxiv.org/abs/2310.19341
- **Aquila2** (BAAI / FlagOpen, 2023-10, github) — 悟道·天鹰 7B/34B/70B-Expr + AquilaChat2，强调数据洁净度：对全部 2T token 排查 20+ 测试集污染；FlagScale + FlagAttention + BMTrain 工具链；16K 长文本版。 https://github.com/FlagAI-Open/Aquila2
- **CogVLM** (智谱 / 清华 KEG, 2023-11, paper) — 视觉专家模块（在每层注意力/FFN 为图像 token 加独立 QKV+FFN）实现深度融合且不损 NLP 能力，冻结 LLM + EVA2-CLIP-E 编码器；CogVLM-17B 在 10 个跨模态基准 SOTA。 https://arxiv.org/abs/2311.03079
- **Qwen-Audio** (阿里 / Qwen Team, 2023-11, paper) — Qwen-7B + Whisper-large-v2 音频编码器；多任务统一框架（分层标签解码条件）覆盖 30+ 音频任务（语音/自然声/音乐/歌曲），缓解任务干扰。 https://arxiv.org/abs/2311.07919
- **TigerBot** (虎博科技, 2023-12, paper) — 7B/13B/70B/180B（7B/13B 基于 Llama-2，180B 基于 BLOOM）续训，清洗多语言中英语料 + 扩中文词表；相对 Llama-2 英文 +6%、中文 +20%，开源数据/工具。 https://arxiv.org/abs/2312.08688

### 2023 跨年（2024 初发布）：DeepSeek/Yi/InternLM 数据工程

- **DeepSeek LLM** (DeepSeek-AI, 2024-01, paper) — 7B/67B，预训练 2.0T token 中英为主（持续扩充）；scaling law 指导超参与数据/模型规模分配（用非 embedding FLOPs/token 刻画规模）；BBPE 词表 102400；67B 用 95 层深网络 + GQA。 https://arxiv.org/abs/2401.02954
- **DeepSeekMoE** (DeepSeek-AI, 2024-01, paper) — 提出「细粒度专家切分 + 共享专家隔离」MoE 架构；16B 版 2T token、每 MoE 层 2 共享 + 64 routed（激活 6），仅约 40% 计算即媲美 DeepSeek-7B/LLaMA2-7B；成为 DeepSeek-V2/V3 MoE 基础。 https://arxiv.org/abs/2401.06066
- **Yi: Open Foundation Models** (零一万物 01.AI, 2024-03, paper) — 6B/34B，3.1T 高质量中英 token，「数据工程优先」：级联去重 + 质量过滤 + 无监督语义聚类打质量标签（偏好 3T 精炼数据胜 10T 未充分过滤）；GQA + RoPE ABF + 10B token 轻量续训扩 200K 上下文。 https://arxiv.org/abs/2403.04652
- **InternLM2** (上海 AI Lab / 商汤, 2024-03, paper) — 1.8B/7B/20B，预训练先 4k → 转 32k 高质量长文本（GQA 支持 200K，「大海捞针」近满分）；数据流水线 jsonl 标准化→按类型/语言分类→启发式过滤→去重/安全过滤；InternEvo 框架 1024 卡 53% MFU。 https://arxiv.org/abs/2403.17297

### 2024：万亿 token MoE、端侧小模型、多模态数据工程

- **DeepSeek-VL** (DeepSeek-AI, 2024-03, paper) — 1.3B/7B 视觉语言模型，强调真实世界场景数据构建（web 截图/PDF/OCR/图表/教材/专家知识）+ 混合视觉编码器(SigLIP + SAM-B 高效处理 1024×1024)；联合视觉-语言预训练保持语言能力。 https://arxiv.org/abs/2403.05525
- **MiniCPM** (面壁 / OpenBMB / 清华 THUNLP, 2024-04, paper) — 1.2B/2.4B 端侧小模型，核心是 WSD（Warmup-Stable-Decay）学习率调度 + 模型风洞（小模型网格搜超参外推大模型）；退火期引入高质量 SFT 风格数据；性能抗衡 7B–13B。 https://arxiv.org/abs/2404.06395
- **Tele-FLM (FLM-2)** (BAAI / 中国电信 TeleAI, 2024-04, paper) — 52B 多语言模型，2T token 全程除硬件故障无 loss 不稳定；主打「50B+ 规模、最小试错成本」的稳定高效预训练范式，借鉴 FLM 家族 growth 训练 + μP 超参迁移；公开数据配比/架构/超参。 https://arxiv.org/abs/2404.16645
- **InternVL 1.5** (上海 AI Lab / OpenGVLab, 2024-04, paper) — 三大改进缩小与 GPT-4V 差距：强视觉编码器 InternViT-6B 连续学习 + 动态高分辨率（1–40 个 448×448 tile，最高约 4K）+ 高质量中英双语数据集（自然场景 + 文档 OCR）。 https://arxiv.org/abs/2404.16821
- **ChatGLM (GLM-4)** (智谱 / 清华, 2024-06, paper) — GLM-4/Air/9B 系列，约 10T token（中英为主，覆盖 24 种语言）；128K 扩到 1M 上下文；中文 AlignBench 超 GPT-4；GLM-4 All Tools 做 agent 对齐（自主规划+工具调用）。 https://arxiv.org/abs/2406.12793
- **Qwen2** (阿里 / Qwen Team, 2024-07, paper) — 0.5B–72B 稠密 + 57B-A14B MoE，7T token（0.5B 版 12T）；全系 GQA + Dual Chunk Attention + YARN 扩 128K；多语言约 30 种；Qwen2-72B 基座 MMLU 84.2。 https://arxiv.org/abs/2407.10671
- **CogVideoX** (智谱 / 清华, 2024-08, paper) — diffusion transformer 文生视频（10 秒、16fps、768×1360）；3D VAE 时空压缩 + expert transformer + 渐进式多分辨率训练 + 自建视频 caption 流水线构造高质量 video-text 对，显著改善语义对齐。 https://arxiv.org/abs/2408.06072
- **CogVLM2** (智谱 / 清华, 2024-08, paper) — 图像与视频理解家族（CogVLM2 / CogVLM2-Video / GLM-4V），继承 visual expert 架构并改进预训练/后训练配方，最高 1344×1344；视频模型用多帧 + 时间戳实现时序定位与视频问答。 https://arxiv.org/abs/2408.16500
- **LongWriter** (智谱 / 清华, 2024-08, paper) — 诊断出长上下文 LLM 输出长度受 SFT 样本最大长度限制；用 AgentWrite 流水线（任务拆子任务）构造 LongWriter-6k（6000 条、输出 2k–32k 字 SFT 数据），让模型稳定输出 1 万字以上。 https://arxiv.org/abs/2408.07055
- **MiniCPM-V** (面壁 / OpenBMB / 清华 THUNLP, 2024-08, paper) — 端侧 MLLM 系列，MiniCPM-Llama3-V 2.5（8B）在 OpenCompass 11 项基准超 GPT-4V-1106/Gemini Pro/Claude 3；强 OCR（1.8M 像素任意宽高比）；RLAIF-V + VisCPM 实现低幻觉与 30+ 语言。 https://arxiv.org/abs/2408.01800
- **Emu3: Next-Token Prediction is All You Need** (北京智源 BAAI, 2024-09, paper) — 把图像/文本/视频统一 tokenize 到离散空间，仅用单一 Transformer 在混合多模态 token 序列上做 next-token 预测从头训练；文生图超 SDXL、视觉理解超 LLaVA-1.6，无需 diffusion/CLIP 组合。 https://arxiv.org/abs/2409.18869
- **Qwen2-VL** (阿里 / Qwen Team, 2024-09, paper) — 2B/7B/72B 视觉语言模型，提出 Naive Dynamic Resolution（任意分辨率→可变视觉 token，ViT 约 675M）+ 多模态旋转位置编码 M-RoPE 融合文/图/视频位置。 https://arxiv.org/abs/2409.12191
- **Hunyuan-Large** (腾讯混元, 2024-11, paper) — 389B 总参 / 52B 激活开源 MoE，256K 上下文；7T token 中约 1.5T 为高质量多样合成数据（远超以往规模）；KV cache 压缩(GQA+CLA) + 专家专属学习率 + recycle routing；比肩 Llama3.1-405B。 https://arxiv.org/abs/2411.02265
- **DeepSeek-V3 Technical Report** (DeepSeek-AI, 2024-12, paper) — 671B MoE/37B 激活，预训练 14.8T token（两阶段扩上下文 4K→32K→128K）；MLA + DeepSeekMoE + 无辅助损失负载均衡 + MTP；FP8 混合精度，全程零 loss spike，约 2.788M H800 小时（约 557.6 万美元）。 https://arxiv.org/abs/2412.19437
- **DeepSeek-VL2** (DeepSeek-AI, 2024-12, paper) — 视觉侧 dynamic tiling 处理任意宽高比高分辨率图像，语言侧用带 MLA 的 DeepSeekMoE 压 KV cache 为 latent；在改进的视觉-语言数据集上训练，同激活规模多模态理解 SOTA。 https://arxiv.org/abs/2412.10302
- **InternVL 2.5** (上海 AI Lab / OpenGVLab, 2024-12, paper) — 沿用 ViT-MLP-LLM 架构（1B–78B），从模型/数据质量/测试时扩展三方面提升（强调数据质量过滤 + 多模态配方）；78B 版 MMMU 突破 70%，首个达此水平的开源 MLLM。 https://arxiv.org/abs/2412.05271
- **GLM-4-Voice** (智谱 / 清华, 2024-12, paper) — 端到端中英双语语音对话模型，超低比特率(175bps)单码本语音 tokenizer(12.5Hz)；从文本预训练语料合成「语音-文本交错」数据在 GLM-4-9B 基座上继续预训练，实现实时可控情感/语速/方言。 https://arxiv.org/abs/2412.02612
- **HunyuanVideo** (腾讯混元, 2024-12, paper) — 13B+ 参数开源视频基础模型（当时最大开源视频生成），整合分层数据筛选流水线（多阶段质量过滤）+ 渐进式模型放大 + 高效 infra；生成性能比肩闭源。 https://arxiv.org/abs/2412.03603

### 2025：万亿 token MoE、低成本预训练、原生多模态、国产算力

- **MiniMax-01** (MiniMax 稀宇科技, 2025-01, paper) — lightning attention（线性）+ MoE（32 专家、456B 总参/45.9B 激活），训练上下文 1M、推理外推 4M token；VL-01 续训 512B 视觉语言 token。 https://arxiv.org/abs/2501.08313
- **Qwen2.5-Max** (阿里 / Qwen Team, 2025-01, blog) — 大规模 MoE，预训练 20T+ token + 精选 SFT/RLHF；对标 DeepSeek-V3/GPT-4o/Claude-3.5-Sonnet（云 API，未开源权重）。 https://qwenlm.github.io/blog/qwen2.5-max/
- **Qwen2.5 Technical Report** (阿里 / Qwen Team, 2024-12, paper) — 0.5B–72B 全尺寸，预训练语料从 7T 扩到 18T token；后训练 100 万+ SFT + 多阶段 RL（offline DPO + online GRPO）；Qwen2.5-72B-Instruct 逼近 Llama-3.1-405B。 https://arxiv.org/abs/2412.15115
- **DeepSeek-V3 Technical Report** (DeepSeek, 2025-02, paper) — 见上 2024-12 同名报告（arXiv 2412.19437，2025 索引并入主条）：671B MoE/37B 激活，14.8T token，MLA + DeepSeekMoE + FP8，约 557.6 万美元。 https://arxiv.org/abs/2412.19437
- **MiMo** (小米 Xiaomi, 2025-05, paper) — 7B，从预训练到后训练全链路为推理优化；约 25T token 三阶段数据混合 + 多维过滤 + 合成推理数据（强化 reasoning pattern 密度）+ MTP；RL 后超 32B 模型、匹敌 o1-mini。 https://arxiv.org/abs/2505.07608
- **Hunyuan-TurboS** (腾讯混元, 2025-05, paper) — Transformer-Mamba2 混合 MoE（560B 总参/56B 激活，128 层 AMF/MF block），16T 高质量 token，256K 上下文；业界首个工业落地的大规模 Mamba 模型，自适应长短 CoT。 https://arxiv.org/abs/2505.15431
- **Qwen3 Technical Report** (阿里 / Qwen Team, 2025-05, paper) — 0.6B–235B（dense + MoE，旗舰 235B-A22B），预训练约 36T token、119 种语言（Qwen2.5 为 18T/29 语言）；thinking/non-thinking 统一 + thinking budget；strong-to-weak 蒸馏，Apache 2.0。 https://arxiv.org/abs/2505.09388
- **dots.llm1** (小红书 hi lab, 2025-06, paper) — 142B MoE/14B 激活，11.2T 高质量 token 且预训练全程不用合成数据（自研高效数据 pipeline）；性能对标 Qwen2.5-72B，每 1T token 开放中间 checkpoint。 https://arxiv.org/abs/2506.05767
- **ERNIE 4.5** (百度文心, 2025-06, report) — 10 个开源变体（最大文本 MoE 424B/47B 激活、VL MoE、0.3B 稠密）；异构 MoE + 模态隔离路由（文本/视觉专家分置 + 共享专家）；基于 PaddlePaddle，FP8 混合精度，语言模型预训练 MFU 47%，Apache 2.0。 https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf
- **Hunyuan-A13B** (腾讯混元, 2025-06, report) — 80B 总参 / 13B 激活细粒度 MoE（1 共享 + 64 专家选 8），20T token（含 2500 亿高质量 STEM token）严格过滤语料 + 快速退火 + 长上下文扩 256K；四阶段 SFT+RL(GRPO)，fast/slow 双模式思考。 https://github.com/Tencent-Hunyuan/Hunyuan-A13B
- **Kimi K2** (月之暗面 Moonshot AI, 2025-07, paper) — 1T 总参/32B 激活 MoE（384 专家选 8，MLA），预训练 15.5T token；MuonClip 优化器全程零 loss spike，强调 token 效率（rephrasing）；后训练大规模 agentic 数据合成 pipeline。 https://arxiv.org/abs/2507.20534
- **GLM-4.5** (智谱 AI / Z.ai, 2025-08, paper) — 355B MoE/32B 激活（另 106B Air），23T token 多阶段预训练；hybrid reasoning（thinking + direct）；更深更窄设计 + 更多注意力头；专家模型迭代 + 大规模 agentic RL，MIT 协议。 https://arxiv.org/abs/2508.06471
- **Qwen3-Next** (阿里 / Qwen Team, 2025-09, blog) — 80B/约 3B 激活，混合注意力（Gated DeltaNet + Gated Attention 3:1）+ 极致稀疏 MoE（512 专家激活 3.7%）+ MTP；预训练仅 15T token（Qwen3 36T 均匀子集），GPU 算力仅 Qwen3-32B 的 9.3%；256K 上下文。 https://qwen.ai/blog?id=qwen3-next
- **Pangu Ultra** (华为盘古, 2025-04, paper) — 135B 稠密 Transformer（94 层），13.2T token；depth-scaled sandwich normalization 消除深层 loss spike；8192×昇腾 NPU 训练，超 Llama 405B/Mistral Large 2，证明国产 NPU 可高效训百亿级稠密模型。 https://arxiv.org/abs/2504.07866
- **InternVL3** (上海 AI Lab / OpenGVLab, 2025-04, paper) — native multimodal pre-training：单一预训练阶段从多模态 + 纯文本联合习得语言与多模态能力（免去事后改造 LLM 为 MLLM）；V2PE 可变视觉位置编码 + SFT + MPO；1B–78B。 https://arxiv.org/abs/2504.10479
- **Ling 2.0 (含 Ling-1T)** (蚂蚁百灵 / inclusionAI, 2025-10, paper) — 统一 MoE 范式跨 16B→1T 一致设计，高稀疏 + 经验缩放律指导；活跃算力效率较稠密最高 7×，大规模高质量预训练 + FP8 infra。 https://arxiv.org/abs/2510.22115

### 2026：百万上下文、统一原生多模态、连续/离散扩散语言模型

- **DeepSeek-V4** (DeepSeek, 2026-04, report) — V4-Pro 1.6T/49B 激活、V4-Flash 284B/13B 激活，均 1M 上下文，预训练 32T+ token；混合注意力(CSA+HCA) + mHC + Muon 优化器，1M 上下文下仅约 27% 单 token 推理 FLOPs/10% KV cache；Base FP8、Instruct FP4+FP8 混合。 https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro
- **openPangu-Ultra-MoE-718B** (华为盘古, 2026-04, model-card) — 718B 总参/39B 激活 MoE，昇腾 NPU 从零训练约 19T token；MLA + MTP + 大稀疏比 + Depth-Scaled Sandwich-Norm/TinyInit + EP-Group 负载均衡；快慢思考融合。 https://huggingface.co/openpangu/openPangu-Ultra-MoE-718B-model
- **Qwen3.5-Omni** (阿里 / Qwen, 2026-04, paper) — 全模态旗舰扩到数千亿参数、256K 上下文，海量异构 text-vision + >1 亿小时音视频训练；Thinker/Talker 均用 Hybrid Attention MoE；215 个音频/音视频子任务 SOTA，ARIA 动态对齐缓解流式 TTS。 https://arxiv.org/abs/2604.15804
- **ERNIE 5.0** (百度, 2026-02, paper) — 原生自回归统一多模态（文/图/视频/音频从零联合训练，next-group-of-tokens prediction）；超稀疏 MoE + 模态无关专家路由 + 弹性训练范式（单次预训练学出不同深度/容量/稀疏度的子模型族）。 https://arxiv.org/abs/2602.04705
- **ERNIE-Image** (百度, 2026-05, paper) — 8B 单流 DiT 文生图；bottom-up 预训练数据 pipeline（细粒度图像分类 + 丰富 caption + 美学评估 + 分层采样，降噪保长尾）+ top-down 后训练 pipeline + 稳定化 DPO；ERNIE-Image-Turbo 8-NFE 生成。 https://arxiv.org/abs/2605.25347
- **Kimi K2.5: Visual Agentic Intelligence** (月之暗面 Moonshot AI, 2026-02, paper) — 开源多模态 agentic 模型，joint text-vision pre-training（文本+视觉联合预训练互增强）+ zero-vision SFT + joint text-vision RL；Agent Swarm 自主并行编排框架（延迟降最多 4.5×）；后继 K2.6 为 1T/32B MoE。 https://arxiv.org/abs/2602.02276
- **Intern-S1-Pro** (上海 AI Lab / InternLM, 2026-03, paper) — 万亿规模科学多模态基座（Intern-S1 旗舰升级），统一处理文本 + 科学专业模态（分子/化学/物理/生物），面向跨学科科学推理。 https://arxiv.org/abs/2603.25040
- **InternVL-U** (上海 AI Lab / OpenGVLab, 2026-03, paper) — 统一多模态模型，把理解/推理/生成/编辑整合到单一框架，目标「民主化」统一多模态模型，承接 InternVL 系列向「理解+生成」一体化扩展。 https://arxiv.org/abs/2603.09877
- **LongCat-Next: Lexicalizing Modalities as Discrete Tokens** (美团 LongCat, 2026-03, paper) — 提出 DiNA（离散原生自回归）框架把文/视/音统一到共享离散空间，单一自回归目标建模；dNaViT 任意分辨率把连续视觉转分层离散 token，工业级原生多模态基座。 https://arxiv.org/abs/2603.27538
- **LongCat-Flash-Thinking-2601** (美团 LongCat, 2026-01, paper) — 560B MoE 推理模型，统一训练框架「领域并行专家训练 + 后续融合」，数据/环境/算法/infra 从预训练到后训练端到端 co-design；agentic search/tool use/TIR 开源 SOTA。 https://arxiv.org/abs/2601.16725
- **Skywork UniPic 3.0** (昆仑万维 Skywork, 2026-01, paper) — 统一多模态框架（单图编辑 + 多图合成），支持任意 1~6 张输入/任意输出分辨率；统计分析识别 Human-Object Interaction 为社区最需类别，配完整数据收集/过滤/合成 pipeline。 https://arxiv.org/abs/2601.15664
- **Cola-DLM (Continuous Latent Diffusion Language Model)** (字节跳动 Seed, 2026-05, paper) — 层次化连续潜空间扩散语言模型，Text VAE（文本↔连续潜序列）+ block-causal DiT prior 通过 Flow Matching 在连续潜空间做扩散建模，偏离离散 token AR/掩码扩散主流。 https://arxiv.org/abs/2605.06548
- **MiniMax-M2 Series** (MiniMax 稀宇科技, 2026-05, paper) — 旗舰 M2 总参 229.9B/仅 9.8B 激活 MoE，面向 agentic 部署；agent 驱动数据 pipeline 产出大规模可验证轨迹（agentic coding + cowork，基于可执行 workspace + artifact 对齐奖励）；Forge agent-native RL 系统 + 可自我演化的 M2.7。 https://arxiv.org/abs/2605.26494

---

## 多模态视觉/编码器与数据集祖先组件

- **Image GPT — Generative Pretraining from Pixels** (OpenAI, 2020-06, blog) — GPT-2 同构 Transformer 直接在像素序列上自回归预训练（无卷积、无 2D 先验），图像下采样 + 512 色码本量化；iGPT-XL 约 6.8B，证明生成式序列建模跨模态通用（ImageNet linear probe 72.0%）。 https://openai.com/index/image-gpt/
- **mT5** (Google Research, 2020-10, paper) — T5 多语言版，mC4 语料（101 种语言，源自 Common Crawl）+ 约 250K 统一 SentencePiece 词表，温度 α=0.3 重采样平衡高/低资源语言；small–13B(XXL)。 https://arxiv.org/abs/2010.11934
- **Vision Transformer (ViT)** (Google Research, 2020-10, paper) — 图像切 16×16 patch 当 token 喂纯 Transformer；ViT-Base/Large/Huge，需大规模数据（ImageNet-21k / JFT-300M）补偿缺失的卷积归纳偏置，大数据下超 ResNet SOTA（ImageNet top-1 约 88.5%）。 https://arxiv.org/abs/2010.11929
- **wav2vec 2.0** (Meta FAIR, 2020-06, paper) — CNN 特征编码器 + 掩码 + Transformer 上下文网络 + 乘积量化码本，对比学习自监督；LibriVox 5.3 万小时无标注预训练，仅 10 分钟标注即达 test-clean WER 4.8%。 https://arxiv.org/abs/2006.11477
- **CLIP** (OpenAI, 2021-02, paper) — 4 亿图文对（自建 WIT）对称 InfoNCE 对比学习，图像/文本双塔；ImageNet zero-shot 76.2%；其视觉编码器（CLIP/SigLIP）是几乎所有现代 VLM 的视觉主干。 https://arxiv.org/abs/2103.00020
- **DeepSeek-V2 (MLA)** (DeepSeek-AI, 2024-05, report) — 236B 总参/21B 激活 MoE，8.1T token，128K 上下文；首提 MLA（KV cache 压缩 93.3% + 解耦 RoPE）+ DeepSeekMoE 细粒度/共享专家，训练成本较 67B 降 42.5%。 https://arxiv.org/abs/2405.04434

---

> 去重说明：(1) MT-NLG 530B（arXiv 2201.11990）在 2021/2022 两处索引为同一工作，已合并；(2) DeepSeek-V3、Qwen2.5、Llama 3、DeepSeek-V2、CLIP、BLT、DeepSeekMath/GRPO 等在 themes/ 或 2024/2025 年份目录存在重复条目，本章以一条主条目合并；(3) Code Llama 博客、Meta Llama 3 / 3.1 博客并入对应论文条目（500B 代码 token、15T token 等数据细节已写入主条）。
