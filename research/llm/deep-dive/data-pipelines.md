# 预训练数据集与处理 Pipeline 深挖（FineWeb / DCLM / The Stack / RedPajama / Dolma / Nemotron-CC / RefinedWeb / C4 / CulturaX / ROOTS）

> 本档案聚焦「开放预训练数据集」家族，逐个数据集抠**抽取→清洗→去重→质量过滤→去毒→PII→污染检测**全 pipeline，以及**配比/消融/分类器阈值**等一手数字。
> 所有数字均来自官方 arXiv 技术报告 / 官方 HF 数据集卡 / 官方 GitHub。第三方解读一律不收。
> 注意：这些是「数据集」而非「模型」，因此「架构/SFT/RL」字段大多不适用（数据集本身不做 RLHF）。对于配套训练的消融模型/参考模型，我把其架构与训练细节写在「消融/参考模型」字段。

---

## 家族演进脉络（2019 → 2025）

- **2019 — C4（T5）**：Google 用 2019-04 Common Crawl WET 文件 + 一套朴素启发式规则（终结符标点、bad-words、langdetect≥0.99 英文、三句窗口去重）做出 ~750GB / 156B token 的 **C4**，奠定「Common Crawl + 规则清洗」范式，但**数据未随论文发布**（后由 AI2/HF 复刻）。
- **2020 — mC4 / OSCAR / CCNet / The Pile**：mT5 把 C4 扩到 101 语言（cld3 语言识别 + α=0.3 温度采样）；Meta 的 CCNet（FastText langID + KenLM 困惑度分 head/middle/tail）成为后续多语数据集的清洗内核；EleutherAI 的 The Pile 确立「多来源混合」。
- **2021–2022 — RefinedWeb / ROOTS / The Stack v1**：Falcon 团队的 **RefinedWeb** 证明「纯网页 + 极致过滤去重」可媲美精选语料（trafilatura 抽取 + 严格 MinHash + exact-substring，~90% 文档被丢弃）；BigScience 的 **ROOTS**（1.6TB / 59 语言）支撑 BLOOM；BigCode 的 **The Stack v1**（3.1TB→6.4TB / 358→384 语言代码）支撑 StarCoder。
- **2023 — RedPajama v1 / v2 + CulturaX**：Together 复刻 LLaMA 配方做出 **RedPajama-V1**（1.2T token），再做 **RedPajama-V2**（100T token 原始 + 40+ 质量信号 + MinHash/Bloom 去重标签）；UONLP 的 **CulturaX**（6.3T token / 167 语言，mC4+OSCAR 合并 + IQR 自动阈值 + MinHashLSH）。
- **2024 — Dolma / FineWeb / FineWeb-Edu / DCLM / The Stack v2**：数据透明化与「基于模型的过滤」成主流。AI2 **Dolma**（3T token，开源 Rust 工具）；HF **FineWeb**（15T token）发现**逐快照 MinHash 去重反而优于全局去重**，并用 Llama-3-70B 合成标注训出教育分类器做 **FineWeb-Edu**（1.3T token）；UW/Apple 的 **DCLM**（240T pool）用 fastText(OH-2.5+ELI5) 分类器证明「模型过滤 >> 启发式」；BigCode **The Stack v2**（67.5TB / 619 语言，基于 Software Heritage 存档）。
- **2024-末 — Nemotron-CC**：NVIDIA 把「质量」与「数量」同时拉满——分类器集成 + 合成数据 rephrasing，做出 6.3T token（4.4T 真实去重 + 1.9T 合成），其 1.1T 高质量子集 MMLU 比 DCLM 高 5.6。
- **2024-末 — FineWeb-2**：HF 把 FineWeb pipeline 扩到 1800+ 语言/方言。

> 一句话主线：**抽取**从 WET→WARC+trafilatura/resiliparse；**去重**从 line-level→exact-substring + 全局 MinHash→（FineWeb 反转）逐快照 MinHash；**过滤**从纯启发式（C4/Gopher）→ fastText 模型过滤（DCLM）→ LLM 合成标注训分类器（FineWeb-Edu）→ 分类器集成 + LLM rephrasing 合成（Nemotron-CC）。

---

## 各代关键参数对比

| 数据集 | 组织 | 年份 | 规模 | 来源/范围 | 抽取 | 去重 | 质量过滤 | 一手报告 |
|---|---|---|---|---|---|---|---|---|
| C4 (en) | Google | 2019 | ~750GB / 156B token | CC 2019-04 单快照 | WET 文件 | 三句窗口去重 | 启发式(终结标点/bad-words/langdetect≥0.99) | arXiv 1910.10683；记录: 2104.08758 |
| mC4 | Google | 2020 | 101 语言 | CC 71 快照 | WET | 跨文档行去重 | cld3 langID + 行长过滤 + α=0.3 采样 | arXiv 2010.11934 |
| RefinedWeb | TII(Falcon) | 2023 | 公开 600B / 全量 ~5T token | CC 纯英文网页 | trafilatura(WARC) | URL去重 + exact-substring + MinHash(20桶×450哈希, 5-gram) | URL黑名单(4.6M域) + Gopher/重复规则 | arXiv 2306.01116 |
| The Stack v1 | BigCode | 2022 | 3.1TB(许可)/6.4TB(全) / 30→384 语言 | GitHub(GHArchive→clone) | 原始文件 | exact + near-dedup(MinHash) | 许可过滤(SPDX/ScanCode) + PII + opt-out | arXiv 2211.15533 |
| The Stack v2 | BigCode | 2024 | 67.5TB全/32.1TB去重 / 619 语言 | Software Heritage 存档 + GitHub PR/Issue/Kaggle/Jupyter | 原始文件 | near-dedup(MinHash) | 许可(96.93%靠ScanCode文件级) + PII + opt-out | arXiv 2402.19173 |
| ROOTS | BigScience | 2022 | 1.6TB / 59 语言(46自然+13代码) | 38%来自OSCAR + 众包目录 + 伪爬 | 多 pipeline | SimHash(6-gram,海明≤4) + exact substring | native-speaker 人工过滤规则 + PII | arXiv 2303.03915 |
| RedPajama-V1 | Together AI | 2023 | 1.2T token | 复刻LLaMA(CC/C4/GitHub/Wiki/Books/ArXiv/StackEx) | 各源不同 | CCNet 分片去重 | Wikipedia-ref fastText 分类器 + CCNet head/middle | arXiv 2411.12372 |
| RedPajama-V2 | Together AI | 2023 | 100T token原始(50T带信号) / 5 语言 | CC 84 快照(2014–2023/04) | WET + CCNet | MinHash签名 + Bloom(exact) **标签** | **不过滤**, 提供40+质量信号 | arXiv 2411.12372 |
| CulturaX | UONLP | 2023 | 6.3T token / 167 语言 | mC4 v3.1.0 + OSCAR(20.19–23.01) | 继承 | MinHashLSH 文档级 | IQR 自动阈值(停用词/困惑度/langID) | arXiv 2309.09400 |
| Dolma | AI2 | 2024 | 3T token / 4.4亿+文档 | CC网页 + GitHub + Reddit + S2 + Gutenberg + Wiki | CCNet | URL/文档/段落级 Bloom filter | Gopher全规则 + C4 NoPunc + Jigsaw 毒性 + PII | arXiv 2402.00159 |
| FineWeb | Hugging Face | 2024 | 15T token / 96 CC 快照 | CC(2013–2024) 纯英文 | trafilatura(WARC) | **逐快照** MinHash(112哈希=14桶×8, 5-gram) | C4 + MassiveText + 3 条自定义过滤 + PII | arXiv 2406.17557 |
| FineWeb-Edu | Hugging Face | 2024 | 1.3T token(阈值3) | FineWeb 子集 | 继承 | 继承 | Llama-3-70B 合成标注训 linear-on-arctic-embed 分类器(阈值≥3) | arXiv 2406.17557 |
| FineWeb-2 | Hugging Face | 2024-末 | 1800+ 语言/方言 | CC 多语 | trafilatura | 逐语言去重 | 逐语言 FineWeb 风格 pipeline | HF 数据集卡 |
| DCLM(-Pool/-Baseline) | UW/Apple/TRI/AI2 等 | 2024 | Pool 240T → Baseline 3.8T token | CC(2008–2022) 纯英文 | **resiliparse** | Bloom(near-dup)；MinHash备选 | **fastText(OH-2.5+ELI5) 取top-10%** + RefinedWeb启发式 | arXiv 2406.11794 |
| Nemotron-CC | NVIDIA | 2024-末 | 6.3T token(4.4T真实+1.9T合成); 高质子集1.1T | CC 99 快照 | jusText | 全局 fuzzy + exact-substring | **分类器集成**(FineWeb-Edu类3个) + 5 桶 + LLM rephrasing | arXiv 2412.02595 |

---

## C4 / mC4（Google，T5/mT5）

### 概述
- **C4 = Colossal Clean Crawled Corpus**，T5 论文（arXiv 1910.10683）首次提出；**论文未直接发布数据**，仅发布 TensorFlow Datasets 复现脚本，后由 AllenAI/HF 重建并发布。
- **规模（C4.en）**：~750GB（T5 论文口径）；AI2 记录论文（2104.08758）实测 **156B token / 305GB**，来自 **3.65 亿个域名**。
- **来源**：Common Crawl **2019-04（April 2019）单一快照**的 **WET 文件**（已抽好正文）。

### 数据处理 pipeline（C4 启发式规则，全部为规则，无模型）
- 只保留**以终结标点（. ! ?）或引号结尾的行**；
- 丢弃**少于 5 句**的页面，只保留**≥3 词**的行；
- 删除含 **"List of Dirty, Naughty, Obscene or Otherwise Bad Words"** 黑名单词的页面；
- 删除含 **"lorem ipsum"** 占位文本、含 **"{" / javascript / "terms of use" / "cookie policy"** 的行/页；
- **langdetect**：仅保留判定为英文概率 **≥0.99** 的页面；
- **去重**：跨整个数据集，**移除重复的三句窗口（three-sentence span）**。

### 已知偏差（AI2 记录论文 2104.08758 的发现）
- 黑名单词过滤**不成比例地删除少数族裔方言（AAE）/ LGBTQ 相关文本**；
- 含大量**机器生成文本**（最大单一来源 `patents.google.com`，>10% 专利来自非美国专利局，经机器翻译）；
- 含其他 NLP 评测集样本（污染）。

### 多语言版 mC4（mT5）
- **101 语言**，来自 CC **71 个月度快照**；语言识别用 **cld3**（≥100 语言）。
- 不用 C4 的「终结标点」过滤（多语不适用），改用**行长过滤**：页面须含 **≥3 行、每行 ≥200 字符**。
- 跨文档行去重（沿用 C4）。
- 语言采样：**温度采样 exponent α=0.3**（高/低资源平衡），与 XLM-R 一致。

### 来源
- T5/C4 原论文：https://arxiv.org/abs/1910.10683 ｜本地 `deep-dive/files/t5-c4-original-1910.10683.pdf`
- 「Documenting the English C4 Corpus」(AI2/UW/HF, 2021)：https://arxiv.org/abs/2104.08758 ｜本地 `deep-dive/files/c4-documenting-2104.08758.pdf`
- mT5/mC4：https://arxiv.org/abs/2010.11934 ｜本地 `deep-dive/files/mt5-mc4-2010.11934.pdf`

---

## RefinedWeb（TII / Falcon，2023）

### 概述
- 论文：「The RefinedWeb Dataset for Falcon LLM」（arXiv 2306.01116）。核心论点：**仅靠充分过滤去重的网页数据即可训出强模型，甚至超过用精选语料训练的模型**。
- **规模**：可从 CC 提取约 **5 万亿 token**；**公开发布 600B token 子集** + 配套训练的 1.3B / 7.5B 参考模型。
- **来源**：纯英文，**仅来自 Common Crawl**（不混精选语料），从 **WARC**（原始 HTML）读取（不用 WET）。

### 数据处理 pipeline（Macrodata Refinement / MDR；最终保留约原始的 ~10%）
- **抽取**：`warcio` 读 WARC → **trafilatura** 抽正文（作者发现 WET 含导航菜单等噪声）。
- **URL 过滤（清洗前先做，省算力）**：聚合 **4.6M 域名黑名单** + 基于关键词/严重度的 URL 评分，过滤欺诈/成人站。
- **语言识别**：fastText（CCNet 的字符 n-gram 模型，文档级）。
- **质量/重复过滤**：沿用 Gopher 的重复/启发式规则，移除行/段/n-gram 过度重复的文档；经过滤后 CC 仅剩约 **50%** 文档。
- **去重（极严格，exact + fuzzy 串联，合计移除约 90% 文档）**：
  - **exact substring**：后缀数组匹配最小长度子串（~50% 文档受影响）；
  - **fuzzy MinHash**：5-gram，**20 个桶 × 每桶 450 哈希**（≈9000 哈希）；
  - 还跨 CC 多个 dump 移除重复访问的 URL。
- 注：作者发现直接在 RW-Filtered 上做 MinHash 移除比例较低（~10%/26%），故拆分处理。

### 来源
- https://arxiv.org/abs/2306.01116 ｜本地 `deep-dive/files/refinedweb-2306.01116.pdf`

---

## The Stack v1（BigCode，2022）

### 概述
- 论文：「The Stack: 3 TB of permissively licensed source code」（arXiv 2211.15533）。是 StarCoder/StarCoderBase 的数据基础。
- **规模**：**3.1 TB 许可子集（permissively licensed）**，30 种编程语言；全量（all-license）**6.4 TB / 384 语言**（HF 卡口径）。
- **来源**：从 **GHArchive** 获取活跃 GitHub 仓库名 → 克隆，成功克隆 **137.36M 仓库**（克隆成功率 >62%）。

### 数据处理 pipeline
- **许可检测**：用 SPDX 标识 + go-license-detector；只保留 permissive 许可（MIT/Apache/BSD/Unlicense 等）做许可子集。
- **去重**：发布 **near-deduplicated（MinHash）版本**；论文实验证明**近去重显著提升下游 HumanEval/MBPP**（去重后仅用 permissive 数据即可匹配/超过 CodeParrot 等用全量数据的模型）。
- **数据治理**：提供 **opt-out 流程**（开发者可申请移除），关注 **PII 与恶意代码**。

### 来源
- https://arxiv.org/abs/2211.15533 ｜本地 `deep-dive/files/the-stack-2211.15533.pdf`
- HF: https://huggingface.co/datasets/bigcode/the-stack

---

## The Stack v2（BigCode，2024，StarCoder2 报告）

### 概述
- 论文：「StarCoder 2 and The Stack v2: The Next Generation」（arXiv 2402.19173）。
- **规模**：全量 **67.5 TB**，去重版 **32.1 TB**（HF 卡）；训练子集 train(full) **~900B 唯一 token**（比 The Stack v1 训练集大 4×），train(smol) 17 语言、~200B token。
- **来源**：建立在 **Software Heritage（SWH）源码存档**之上（覆盖 **619 种编程语言**），并补充 **GitHub Issues、Pull Requests、Kaggle/Jupyter notebooks、代码文档、中间表示（IR）、小型数学/代码数据集**。
- **透明度**：发布 **SWHID（Software Heritage 持久标识符）**而非原始代码本身。

### 数据处理 pipeline
- **许可检测**：先从 GHArchive 取 repo 级许可；**96.93% 仓库无 repo 级许可**，改用 **ScanCode Toolkit 做文件级检测**（图 1 给出文件级许可判定逻辑：repo 许可空→文件级检测→是否全部 permissive）。
- **去重**：`the-stack-v2-dedup` 在原始基础上做 **near-deduplication（MinHash）**；文档站点合并前先对不同 HTML 页抽取内容近去重（MinHash LSH **阈值 0.7**）；Jupyter notebook 近去重后剩 4M（转脚本）/ 4.6M（结构化）。
- **过滤**：低质代码启发式过滤 + **PII 编辑（redact）** + 恶意代码移除 + 开发者 opt-out。
- **PR**：包含 ≤100K 字符（约 25k token）的 PR；GitHub Issues 处理后约 **11.4M 问题 / >10B token**。

### 配套模型 StarCoder2（3B/7B/15B）
- 训练 **3.3–4.3T token**（远超 Chinchilla 计算最优，"Harm's law"过训）；上下文 **4K**（预训练阶段）；两阶段训练。
- StarCoder2-3B 超 StarCoderBase-15B；15B 匹配/超 CodeLlama-34B。

### 来源
- https://arxiv.org/abs/2402.19173 ｜本地 `deep-dive/files/starcoder2-2402.19173.pdf`
- HF: https://huggingface.co/datasets/bigcode/the-stack-v2

---

## ROOTS（BigScience，2022，BLOOM 语料）

### 概述
- 论文：「The BigScience ROOTS Corpus: A 1.6TB Composite Multilingual Dataset」（arXiv 2303.03915）。用于训练 BLOOM 176B。
- **规模**：**1.6 TB**，**59 语言（46 自然语言 + 13 编程语言）**，语言选择由众包社区驱动。
- **来源构成**：**38% 来自预处理网页爬取 OSCAR**（由 native speaker 协助过滤）；其余来自 BigScience Catalogue 众包目录（498 个构成数据集）+ **伪爬（pseudo-crawl）**（192 目录条目 + 456 站点提案，去重后 614 唯一域名）+ GitHub/StackExchange 代码（BigQuery）。

### 数据处理 pipeline
- **质量过滤**：每语言由 native speaker 设计**人工过滤规则**（停用词比例、字符等），各语言移除文档比例见论文 Table 1。
- **去重**：先对 OSCAR（已 exact-dedup）用 **SimHash（6-gram，海明距离阈值 4）**，约移除 **0.7% 文档**；再做 substring 精确去重；跨 pipeline 去重（移除伪爬的 Wikipedia/GitHub，保留更优版本）；移除处理后 <2MB 的整个域名。
- **PII**：专门的 PII 过滤初创（regex 等，论文附录 D）。
- HTML 处理：从 DOM 移除 `<script>`/`<style>` 等子树。

### 来源
- https://arxiv.org/abs/2303.03915 ｜本地 `deep-dive/files/roots-bigscience-2303.03915.pdf`

---

## RedPajama-V1 & RedPajama-V2（Together AI，2023）

> 论文：「RedPajama: an Open Dataset for Training Large Language Models」（arXiv 2411.12372，2024 发布的正式报告，回顾 2023 发布的 v1/v2）。

### RedPajama-V1（LLaMA 配方开放复刻）
- **规模**：约 **1.2T token**；组成（Table 2）：**CommonCrawl 878B + C4 175B + GitHub 59B + Books 26B + ArXiv 28B + Wikipedia 24B + StackExchange 20B**。
- **CommonCrawl**：复刻 LLaMA 的 **5 个快照（2017–2020）**，经 **CCNet pipeline**（分片去重 + 用 Wikipedia 训的 5-gram Kneser-Ney 困惑度分 head/middle/tail，**只保留 head + middle**）。
- **质量分类器**：下载最新英文 Wikipedia 快照 → CCNet 适度清洗 → 训 **fastText unigram 分类器**，过滤掉分数过低的文档（复刻 LLaMA 的 Wikipedia-reference 分类器）。
- 衍生：**SlimPajama**（进一步清洗去重 v1）。
- 已知 gap：3B 规模可比，**7B 与原版 LLaMA-7B 仍有差距**（作者推测部分因需用 FP16 精度训练，以及原 LLaMA 语料细节缺失）。

### RedPajama-V2（纯网页、原始 + 质量信号）
- **规模**：**100T token 原始、几乎未过滤文本**；其中 **50T token 子集附带质量信号**。
- **范围**：CC **84 个月度快照（2014 – 2023/04）的 WET 文件**，经 CCNet（保留全部困惑度桶）；**5 语言：英、法、德、意、西**。
- **设计哲学**：**不做强过滤**，而是为每文档提供 **40+ 质量信号**（来自 C4、Gopher、RefinedWeb、Pretrainer's Guide、DSIR），分为：自然语言度量、重复度、内容类（NSFW）、ML 启发式（fastText 分类器 + DSIR importance weights）、去重。
- **去重标签**：提供 **MinHash 签名（不同相似度）** + **Bloom filter exact-dup ID**（基于 .wet 文档哈希，先于质量过滤）。消融用 MinHash LSH（word 13-gram，128 哈希，9 bands × 13 rows）。
- 消融（468M 参数模型）结论：**Gopher 规则 + fuzzy(MinHash) 去重组合表现最稳**。

### 来源
- https://arxiv.org/abs/2411.12372 ｜本地 `deep-dive/files/redpajama-data-2411.12372.pdf`
- 模型博客（RedPajama-INCITE）：https://www.together.ai/blog/redpajama-models-v1

---

## CulturaX（UONLP，2023）

### 概述
- 论文：「CulturaX: A Cleaned, Enormous, and Multilingual Dataset for Large Language Models in 167 Languages」（arXiv 2309.09400）。
- **规模**：**6.3T token，167 语言**。
- **来源**：合并 **mC4 v3.1.0** + **全部可用 OSCAR**（distributions 20.19 / 21.09 / 22.01 / 23.01）。

### 数据处理 pipeline（两大步：清洗 + 去重）
- **语言识别**：mC4 用 **cld3**（语言置信度 <0.95 的页被剔除）；OSCAR 用 FastText。
- **清洗（metric-based）**：用 **IQR（四分位距）方法自动选阈值**，针对各项度量（**停用词比例、数据困惑度、语言识别分**）；外加 URL 过滤、document refinement。
- **去重（关键贡献）**：现有 mC4/OSCAR/CC100 都**缺文档级模糊去重**；CulturaX 用 **MinHashLSH 在文档级做 near-dedup**（同语言内），消除冗余。
- 还发布 27B token 的清洗去重子集（HF）。

### 来源
- https://arxiv.org/abs/2309.09400 ｜本地 `deep-dive/files/culturax-2309.09400.pdf`

---

## Dolma（AI2，2024，OLMo 语料）

### 概述
- 论文：「Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research」（arXiv 2402.00159，针对 v1.6）。
- **规模**：**3.059T LLaMA-token / 约 4.367 亿（437M）文档 / 11.5TB UTF-8**（从约 200TB 原始文本清洗到 11TB）。
- **来源构成（Table 1，LLaMA tokenizer 计 token）**：

| 来源 | UTF-8 (GB) | 文档(百万) | Llama token(十亿) |
|---|---|---|---|
| Common Crawl 网页 | 9,812 | 3,734 | **2,479** |
| GitHub 代码 | 1,043 | 210 | **411** |
| Reddit 社媒 | 339 | 377 | **89** |
| Semantic Scholar(peS2o)论文 | 268 | 38.8 | **70** |
| Project Gutenberg 图书 | 20.4 | 0.056 | **6.0** |
| Wikipedia/Wikibooks | 16.2 | 6.2 | **4.3** |
| **合计** | 11,519 | 4,367 | **3,059** |

### 数据处理 pipeline
- **抽取/语言/初步去重**：网页用 **CCNet**（FastText langID 模型，移除语言分 ≤0.5 的内容 → 按字节移除 **61.7%**；CCNet 总体把 CC 从 **175.1TB 过滤到 27.7TB，即过滤 84.2%**）。
- **质量过滤（启发式）**：保留**全部 Gopher 规则（Gopher All）** + **C4 的单条「移除不以标点结尾段落」规则（C4 NoPunc）**（而非 C4 全规则）。
- **去毒（自训分类器）**：在 **Jigsaw Toxic Comments** 上训 **两个 FastText 分类器**（"hate" 与 "NSFW"），分高/低阈值版本。
- **去重（3 阶段，Bloom filter）**：**URL 级 → 文档级 → 段落级**，全部用自实现的、与 mixer 兼容的 **Bloom filter**（段落定义为以 `\n` 结尾的文本跨度；段落级去重移除约 **70% 段落**）。
- **PII**：聚焦 **email / IP / 电话号码** 三类高精度可检测 PII。文档内 **≤5 个 PII span** → 用特殊 token 替换（如 `|||EMAIL_ADDRESS|||`，影响 **0.02%** 文档）；PII 密度更高的文档整篇丢弃（影响 **0.001%**）。
- **工具**：开源高性能 **Rust 工具包（dolma toolkit）**，内置 mixer 可一站做上/下采样、去重、去污染；复刻 C4 配方时过滤速率约 **122 CPU-小时/TB**。

### 来源
- https://arxiv.org/abs/2402.00159 ｜本地 `deep-dive/files/2402.00159.pdf`（亦在 `2024/files/`）
- GitHub: https://github.com/allenai/dolma

---

## FineWeb & FineWeb-Edu（Hugging Face，2024）

### 概述
- 论文：「The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale」（arXiv 2406.17557）。
- **FineWeb 规模**：**15T token**，来自 **96 个 Common Crawl 快照（2013–2024）**，纯英文。
- **FineWeb-Edu 规模**：**1.3T token**（阈值=3 的教育子集）。
- 全开放：数据 + `datatrove` 处理库 + 全部消融检查点。

### FineWeb 数据处理 pipeline（每步均有消融）
- **抽取**：从 **WARC** 用 **trafilatura** 抽正文（消融证明 trafilatura-WARC 优于 CC 的 WET 文件）。
- **语言过滤**：fastText 语言分类器，**英文分数 ≥0.65** 才保留。
- **质量过滤**：应用 **MassiveText（Gopher）的质量与重复过滤**（用原始阈值）。
- **C4 过滤**：采用 C4 多数规则，**但去掉「终结标点」过滤**（因其会删过多数据，移除 30% token；FineWeb 改用更温和版本，仅删「以标点结尾行占比 <0.12」的文档，移除 10.14% token）。
- **3 条自定义启发式过滤**（从 50+ 候选中系统性筛选，用指标分布卡阈值）：
  1. **以标点结尾行占比 < 0.12** → 删（10.14% token 被移除）；
  2. **重复行中的字符占比 ≥ 0.1** → 删（12.47% token 被移除）；
  3. **短于 30 字符的行占比 ≥ 0.67** → 删（3.73% token 被移除）；
  - 三者合用约移除 **22% token**，聚合分提升约 1%。
- **去重（核心反直觉发现）**：MinHash，**5-gram（英文词 tokenizer）+ 共 112 个哈希函数 = 14 桶 × 每桶 8 哈希**（同桶 8 哈希全同即判重，再用并查集连通）。
  - **全局去重（96 快照一起）反而更差**：全局去重会**上采样低质数据**——某快照被全局去重后留下的 10% 数据，质量实际比被删的 90% 更差；
  - **改为逐快照独立去重（per-snapshot / individual）**，性能更好。这是 FineWeb 最重要的工程结论。
- **PII**：用 regex **匿名化 email 与 public IP 地址**。

### FineWeb-Edu 教育分类器（LLM 合成标注 → 训轻量分类器）
- 用 **Llama-3-70B-Instruct** 对 **460,000** 个随机网页打**教育价值分 0–5**（prompt 聚焦小学/初中知识水平，附录 F.1）。
- 在 **Snowflake-arctic-embed-m embedding** 之上训 **linear regression 分类器**：用 **410,000** 条 Llama-3 标注微调 **20 epoch，LR=3e-4**（冻结 embedding），在剩余 **50,000** 验证集评估，输出四舍五入到 0–5 整数。
- **阈值=3** 给出最佳 性能/数据量 权衡（验证集 **F1=82%**），由此得 1.3T token 的 FineWeb-Edu。

### FineWeb-2（多语扩展）
- HF 后续把 FineWeb pipeline 扩到 **1800+ 语言/方言**（逐语言去重 + 逐语言过滤），见官方数据集卡。

### 来源
- https://arxiv.org/abs/2406.17557 ｜本地 `deep-dive/files/2406.17557.pdf`（亦在 `2024/files/`）
- FineWeb HF: https://huggingface.co/datasets/HuggingFaceFW/fineweb
- FineWeb-Edu HF: https://huggingface.co/datasets/HuggingFaceFW/fineweb-edu
- FineWeb-2 HF: https://huggingface.co/datasets/HuggingFaceFW/fineweb-2

---

## DataComp-LM / DCLM（UW / Apple / TRI / AI2 等，2024）

### 概述
- 论文：「DataComp-LM: In search of the next generation of training sets for language models」（arXiv 2406.11794）。
- **本质是「受控数据集实验测试平台」**：标准化语料 **DCLM-Pool** + 统一 OpenLM 训练配方 + 53 项评测；规模档 **412M / 1B / 3B / 7B（含 7B-2x）**。
- **DCLM-Pool**：**240T GPT-NeoX token**（**200B 文档 / 370TB gzip**），来自 Common Crawl（2008–2022），是当时最大公开语料。
- **DCLM-Baseline**：**3.8T token**（基线最优过滤结果）。

### 数据处理 pipeline（构建 DCLM-Baseline 的关键消融结论）
- **抽取**：用 **resiliparse**（而非 trafilatura / WET）。resiliparse 与 trafilatura 下游相当，但 **resiliparse 快 8×**；两者都比 WET 抽取在 Core 上高 ≥2.5 点。
- **启发式过滤**：直接采用 **RefinedWeb 的启发式过滤规则**（消融中 RefinedWeb 在 7B-1x 上最优）。
- **去重**：用 **Bloom filter（near-dup）做 DCLM-Baseline**（与 MinHash 在 7B-2x 上仅差 0.2 Core 点，但 Bloom filter 更易扩展到 >10TB）；其他实验用 MinHash + 后缀数组。
- **质量过滤（核心结论：模型过滤 >> 启发式 / 其他方法）**：
  - 对比了 7 类方法（PageRank、SemDedup、BGE-embedding 分类器、AskLLM、Perplexity、top-k 平均 logits、fastText 二分类器）；
  - **fastText 二分类器**胜出。训练用约 **400k 文档**（正负各半），负样本固定为 RefinedWeb 复刻的随机采样；
  - **正样本最优组合 = OpenHermes-2.5(OH-2.5) + r/ExplainLikeImFive(ELI5) 高分帖**（指令风格数据），比传统选择（GPT-3 用的 Wikipedia/OpenWebText2/RPJ-Books 混合）**在 Core 上高 3.5 个百分点**；
  - **阈值：保留 fastText 分数 top-10%**（优于 top-15% / top-20%）。这一步直接产出 DCLM-Baseline。
- **去污染**：发布去污染工具（针对 MMLU、HellaSwag 做 n-gram overlap 移除）；不直接对 Pool 去污，而要求所有提交披露去污报告。实测对 MMLU/HellaSwag 去 overlap **不影响性能**。

### 扩展到万亿 token（DCLM-Baseline + 数学/代码 + 退火）
- 把 **3.8T DCLM-Baseline 与 StarCoder + ProofPile2** 组合，训 7B 模型 **2.6T token → MMLU 5-shot 64%**（开放数据 SOTA，接近 Mistral-7B-v0.3 的 63% / Llama-3-8B 的 66%，但算力少 **6.6×**）。
- **冷却（cool-down）阶段**：最后 200B/270B token 用调整后分布——**70% DCLM-Baseline（更严 fastText 阈值）+ 30% 数学数据集**（退火/课程的体现，附录 Q）。

### 来源
- https://arxiv.org/abs/2406.11794 ｜本地 `deep-dive/files/2406.11794.pdf`（亦在 `2024/files/`）
- GitHub: https://github.com/mlfoundations/dclm

---

## Nemotron-CC（NVIDIA，2024-末）

### 概述
- 论文：「Nemotron-CC: Transforming Common Crawl into a Refined Long-Horizon Pretraining Dataset」（arXiv 2412.02595）。
- 动机：FineWeb-Edu / DCLM 偏「高质量」但**激进过滤丢弃了大量 token，不利于 15T 这种长程训练**；Nemotron-CC 同时拉满**质量与数量**。
- **规模**：**6.3T token = 4.4T 全局去重的真实 token + 1.9T 合成生成 token**，来自 CC **99 个快照**；高质量子集 **1.1T token**。

### 数据处理 pipeline（三大手法：分类器集成 + 合成 rephrasing + 减少启发式）
- **抽取**：用 **jusText**（对比 trafilatura，jusText 产出更多 token，高质量 token 多 +28.6%，对长程训练重要）。
- **去重**：**全局 fuzzy 去重 + 对八分之一片段做 exact-substring 去重**。
- **质量打分（分类器集成）**：用**多个 model-based 分类器集成**——基于 **FineWeb-Edu 分类器**重训的 3 个变体（如 `nemocurator-fineweb-nemotron-4-edu-classifier`、`nemocurator-fineweb-mixtral-edu-classifier`）；集成可选出更大且更高质的 token 集。
- **分桶**：按质量分把文档分到 **5 个质量桶**；用 **annealing（退火）评估每个桶的下游价值**来定档。
- **合成数据 rephrasing（1.9T token，关键创新）**：
  - 用 **Mistral-NeMo-12B-instruct**（部分用 Nemotron-4-340B-instruct）对文本改写，**不是把 LLM 当知识库，而是改写已有文本**；
  - 对**高质量数据**用 **Wikipedia 风格 prompt** 改写，产生「新鲜的唯一 token」；
  - 4 种合成 prompt：**(1) Diverse Question-Answer pairs、(2) Distill（精炼重写）、(3) Extract Knowledge、(4) Knowledge list**；
  - 对**低质量数据**改写以降噪纠错；
  - 后处理移除「Here is a paraphrased version:」等前缀、去引号、过滤过短输出。
- **减少启发式**：对高质量数据**关闭传统非学习型启发式过滤器**，进一步提升高质量 token 产出。

### 效果（消融）
- **1.1T 高质量子集**：8B 模型训 1T token，**MMLU 比 DCLM 高 5.6**；
- **全量 6.3T**：MMLU 匹配 DCLM 但**唯一 token 多 4×**；
- 用其加权版训 8B 模型 **15T token**，十项任务平均超 Llama-3.1-8B（同样 15T token）。
- 工具：开源 **NeMo Curator**（Apache 2.0）。

### 来源
- https://arxiv.org/abs/2412.02595 ｜本地 `deep-dive/files/nemotron-cc-2412.02595.pdf`
- HF: https://huggingface.co/datasets/nvidia/nemotron-cc

---

## 横向对比：关键技术维度

### 抽取（HTML → 正文）演进
- **WET 文件**（C4/mC4/RedPajama-V2/Dolma 经 CCNet）→ **WARC + trafilatura**（RefinedWeb/FineWeb）→ **WARC + resiliparse**（DCLM，快 8×）→ **jusText**（Nemotron-CC，token 产出最高）。

### 去重策略谱系
- **行/三句窗口**（C4）→ **CCNet 分片去重**（RedPajama-V1/Dolma 网页）→ **exact-substring（后缀数组）+ MinHash**（RefinedWeb，最严，删 ~90%）→ **URL/文档/段落级 Bloom filter**（Dolma）→ **逐快照 MinHash**（FineWeb，反直觉地优于全局）→ **Bloom near-dup**（DCLM-Baseline）→ **全局 fuzzy + exact-substring**（Nemotron-CC）。
- **MinHash 参数对比**：RefinedWeb = 5-gram / 20 桶 × 450 哈希；FineWeb = 5-gram / 14 桶 × 8 哈希(=112)；RedPajama-V2 消融 = 13-gram / 128 哈希 / 9 bands × 13 rows；The Stack v2 文档站 = LSH 阈值 0.7。

### 质量过滤谱系（最关键的演进轴）
- **纯启发式规则**（C4 终结标点/bad-words；Gopher 规则）→ **fastText 参考分类器**（RedPajama-V1 用 Wikipedia 正样本；DCLM 用 **OH-2.5+ELI5 正样本取 top-10%**，证明指令风格正样本 +3.5pp）→ **LLM 合成标注训轻量分类器**（FineWeb-Edu：Llama-3-70B 标 0–5 教育分 → arctic-embed + 线性回归，阈值 3）→ **分类器集成 + LLM rephrasing 合成**（Nemotron-CC）。

### 去毒 / PII / 污染检测
- **去毒**：C4 用 bad-words 黑名单（有偏）；RefinedWeb 用 NSFW URL 黑名单；Dolma 用 Jigsaw 自训 hate/NSFW fastText 分类器。
- **PII**：Dolma/FineWeb 匿名化 email/IP（Dolma 加电话，特殊 token 替换）；The Stack v1/v2 做 PII redaction + opt-out。
- **污染检测**：DCLM 提供去污染工具（MMLU/HellaSwag n-gram overlap）；C4 记录论文揭示其含评测集污染与机器生成文本。

---

## 总结：每个数据集的「一句话定位」

- **C4/mC4**：规则清洗 CC 单快照的范式起点（数据由社区复刻发布）。
- **RefinedWeb**：证明「纯网页 + 极致去重过滤」可媲美精选语料（删 90%）。
- **The Stack v1/v2**：可许可、可 opt-out、可溯源（SWHID）的开放代码语料基石。
- **ROOTS**：众包驱动的 59 语言 BLOOM 语料，强调 native-speaker 人工规则。
- **RedPajama-V1/V2**：v1 复刻 LLaMA 配方；v2 提供 100T 原始 + 40+ 质量信号让用户自选过滤。
- **CulturaX**：167 语言 + IQR 自动阈值 + 文档级 MinHash 去重，补齐多语去重缺口。
- **Dolma**：3T token 多源 + 开源 Rust 工具，三级 Bloom 去重，OLMo 的数据基础。
- **FineWeb / FineWeb-Edu**：15T token + 全消融；最大贡献是「逐快照去重」反直觉发现与「LLM 合成标注训教育分类器」。
- **DCLM**：把数据 curation 变成可竞赛的 benchmark；证明「fastText 模型过滤 >> 启发式」，正样本用指令风格数据。
- **Nemotron-CC**：质量与数量双拉满，分类器集成 + LLM rephrasing 合成 1.9T token，为 15T 长程训练优化。

---

## 本地落盘文件清单

- `deep-dive/files/t5-c4-original-1910.10683.pdf`（T5/C4）
- `deep-dive/files/c4-documenting-2104.08758.pdf`（C4 记录论文）
- `deep-dive/files/mt5-mc4-2010.11934.pdf`（mT5/mC4）
- `deep-dive/files/refinedweb-2306.01116.pdf`（RefinedWeb）
- `deep-dive/files/the-stack-2211.15533.pdf`（The Stack v1）
- `deep-dive/files/starcoder2-2402.19173.pdf`（The Stack v2 / StarCoder2）
- `deep-dive/files/roots-bigscience-2303.03915.pdf`（ROOTS）
- `deep-dive/files/redpajama-data-2411.12372.pdf`（RedPajama v1+v2）
- `deep-dive/files/culturax-2309.09400.pdf`（CulturaX）
- `2024/files/2402.00159.pdf`（Dolma）
- `2024/files/2406.17557.pdf`（FineWeb / FineWeb-Edu）
- `2024/files/2406.11794.pdf`（DCLM）
- `deep-dive/files/nemotron-cc-2412.02595.pdf`（Nemotron-CC）
