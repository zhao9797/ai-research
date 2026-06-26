---
title: "GPT-4o 原生图像生成 (4o image generation / gpt-image-1)"
org: OpenAI
country: US
date: 2024-05
type: blog
category: omni
tags: [omni, autoregressive, native-image, image-generation, text-rendering, image-editing, multimodal, closed-source]
url: https://openai.com/index/hello-gpt-4o/
arxiv:
pdf_url: https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf
github_url:
hf_url:
modelscope_url:
project_url: https://openai.com/index/introducing-4o-image-generation/
downloaded: [gpt-4o-native-image--hello-gpt4o-blog.md, gpt-4o-native-image--gpt4o-system-card.md, gpt-4o-native-image--introducing-4o-image-gen-blog.md, gpt-4o-native-image-system-card.pdf, gpt-4o-native-image--image-gen-system-card-addendum.md, gpt-4o-native-image--gpt-image-1-api-blog.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GPT‑4o（"o" = omni）是 OpenAI 用单一神经网络端到端打通 text·audio·image·video 的全模态自回归模型；其中**原生图像生成**把"出图"做成语言模型的一等能力——2024-05 发布会上以"机器人打字机"连环图首次公开演示，2025-03 正式上线为 ChatGPT 默认出图器、2025-04 以 `gpt-image-1` 进 API。最亮眼的能力是**可靠文本渲染 + 多轮对话式编辑 + 一次摆放 10–20 个物体**（同期扩散系统通常只能稳定处理 5–8 个），上线首周即生成 7 亿张图、1.3 亿用户使用。

## 背景与定位
传统文生图（[[dall-e-3]]、[[stable-diffusion-3]]、[[flux-1]]、[[imagen-3]]）是**独立扩散模型 + 通过工具调用 (tool call) 挂在 LLM 旁边**：LLM 把 prompt 改写后丢给一个外部扩散模型，模型本身并不"看见"也不"记得"图。这导致三个老问题——文字渲染差、多轮编辑一致性差、复杂指令/多物体绑定差，且无法利用 LLM 的世界知识与对话上下文。

GPT‑4o 走的是另一条路：**把图像生成嵌进 omni 模型的架构深处**（natively embedded），让"出图"和"对话""推理"共享同一个 transformer 与同一套后训练栈。OpenAI 的论点是"图像生成应当成为语言模型的核心能力"。这条技术脉络上承学术界的**统一自回归多模态**路线（[[chameleon]] 早期融合 token、[[transfusion]] 文本自回归+图像扩散混合训练、[[emu3]] next-token 统一、[[parti]]/[[llamagen]] 的 AR 出图），下启 2025 各家"原生出图"军备竞赛（[[gemini-2-0-flash-native-image]] / Nano-Banana 等）。相对 [[dall-e-3]] 的核心改进：从"扩散 + 工具调用"变为"自回归 + 原生嵌入"，因而支持图生图变换、照片级写实、可靠文本与指令跟随、对话式迭代编辑。

> 时间线澄清：本词条以 2024-05-13《Hello GPT‑4o》为锚点（首次公开原生图像生成示例 + omni 架构），但**图像生成在发布日并未开放**——当天只放出"图文输入 / 文本输出"。真正交付是 2025-03-25《Introducing 4o image generation》（ChatGPT 默认出图）与 2025-04-23 `gpt-image-1`（进 API）。本页据三段官方博客 + 两份 system card 综合。

## 模型架构
**整体：单一自回归全模态 transformer。** GPT‑4o system card 原文："GPT‑4o 是一种自回归全模态模型，接受文本/音频/图像/视频的任意组合输入，生成文本/音频/图像输出的任意组合……所有输入和输出都由同一个神经网络处理。" 这与早先 ChatGPT 语音模式"ASR→LLM→TTS 三段式"形成对比——后者会丢掉语气、笑声、多说话人等信息；4o 把这些都收进同一网络。

**图像生成支路：自回归 token + 强解码器（autoregressive prior + powerful decoder）。** OpenAI 没有发架构论文，但 Native Image Generation System Card（即 4o image generation 附录的 PDF 正文，原文英文）给了关键定性结论——"Unlike DALL·E, which operates as a diffusion model, 4o image generation is an autoregressive model natively embedded within ChatGPT"（与作为扩散模型的 DALL·E 不同，4o image generation 是原生嵌入 ChatGPT 的自回归模型；落盘 `gpt-4o-native-image-system-card.pdf` §2.1，注：同名的 addendum 网页 `.md` 仅是落地页+PDF 链接，该句在 PDF 里）。发布博客的"白板"示例图（OpenAI 在《Introducing 4o image generation》正文里作为演示放出的 prompt）更直白地写出了设计直觉：

- 目标：用一个大自回归 transformer 直接建模 `p(text, pixels, sound)`；
- 收益：图像生成被海量世界知识增强、下一级别的文本渲染、原生 in-context learning、统一后训练栈；
- 代价：跨模态 bit-rate 不一致、算力不自适应；
- 修法（"Fixes"）：**建模压缩表示（model compressed representations）**、**把自回归先验与一个强解码器组合（compose autoregressive prior with a powerful decoder）**；
- 板上画的 pipeline：`tokens -> [transformer] -> [diffusion] -> pixels`。

也就是说，公开材料一致指向：**用自回归 transformer 预测图像的离散/压缩 latent token，再用一个扩散解码器把 token 渲染成像素**（AR prior + diffusion decoder 的混合范式，思路上接近 [[transfusion]] / 学术界统一模型，但具体 tokenizer、码本、解码器规模均未披露）。注意 system card 把整体称为"autoregressive"，与白板上的扩散解码器并不矛盾——主干预测是自回归的，diffusion 仅作末端像素渲染。

**text encoder / 条件注入：** 无独立 T5/CLIP 文本塔——文本就是 GPT‑4o 本体的语言能力，图像与文本在同一序列里联合建模，条件天然来自对话上下文与上传图像（因此能做 in-context learning 与多轮一致编辑）。

**参数量 / 分辨率 / tokenizer：** 均**未披露**。已知工程侧线索：(1) `gpt-image-1` 按 token 计费且把"生成的图片"也按 token 计量，印证图像被表示为 token 序列；(2) 出图较慢（博客称单图常需约 1 分钟），与自回归逐 token 解码 + 扩散渲染的两段式相符；(3) 支持指定宽高比、精确十六进制颜色、透明背景。

## 数据
来自 GPT‑4o system card（针对 omni 本体，图像生成数据细节未单列）：

- **训练数据截止 2023-10。** 来源两大类：
  1. **精选公开数据**——行业标准 ML 数据集 + 网络爬取；
  2. **数据合作伙伴专有数据**——付费内容、档案、元数据；明确点名**与 Shutterstock 合作共创并交付 AI 生成图像**（即正版授权图源参与训练）。
- 关键数据集：**网络数据**（多样视角/主题）、**代码与数学数据**（养推理）、**多模态数据**（图像/音频/视频，教模型解读非文本输入并生成非文本输出）。
- **图文联合分布训练**：4o image gen 博客称"对网络图像与文本的联合分布训练，使其不仅理解图像与语言的关联，更掌握图像彼此间的关系"——这正是 in-context 编辑/一致性的数据来源。
- **过滤与安全**：沿用既有图像生成系统做法，过滤数据集中的色情(explicit)与 CSAM；用 Moderation API + 安全分类器过滤有害/CBRN/仇恨/暴力内容；先进流程降低训练数据中的个人信息(PII)；**尊重 DALL·E 3 阶段用户的"不用于训练"opt-out**，对标记图像从 4o 系列训练集中移除。
- **后训练数据（偏差缓解）**：Native Image Generation System Card PDF（§2.4.4 Bias）明示计划"incorporating more diverse examples into the post-training mixture"（把更多样的样本纳入后训练混合）以改善人口学表征——侧证存在一个偏好/对齐导向的后训练阶段。
- **规模/配比/具体图文对数量/re-captioning 细节：未披露。**

## 训练方法
官方未发训练论文，可确认的方法学要点（来自三段博客 + 两份 card）：

- **预训练**：单网络在 text/code/math/multimodal 上联合训练；图像支路在**图文联合分布**上学习（见上）。主干为自回归 next-token 预测，图像末端配扩散解码器（白板 pipeline）。
- **后训练 (post-training)**：4o image gen 博客称"结合**强化的后期训练 (enhanced post-training)**，模型展现卓越视觉表现力，更实用、更一致、更懂上下文"。GPT‑4o system card 称后训练阶段做**人类偏好对齐**与红队驱动的合成数据训练。具体是 SFT / RLHF / DPO / reward model 中的哪几种、配比如何——**未披露**。
- **安全用的推理模型（deliberative alignment 思路）**：训练了一个**专门的推理 LLM**，直接依据人类编写、可解释的安全规范工作，对输入文本与输出图像做审核——这是"用推理提升安全性"的方法，与主出图模型协同（属对齐/部署层而非生成主干）。
- **蒸馏 / 步数蒸馏 / consistency / LCM / ADD 等加速**：**未提及、未披露**（自回归 + 扩散解码的两段式本身不是少步扩散范式，出图偏慢也印证未做激进步数蒸馏）。
- **多阶段红队即训练信号**：system card 显示红队分 4 阶段，随训练推进模型逐步解锁"音频/图像输出"，把对抗对话转成自动评测回灌——属安全后训练闭环。

## Infra（训练 / 推理工程）
- **训练算力 / GPU·时 / 并行策略 / 混合精度 / 吞吐：全部未披露**（闭源产品，无技术报告）。
- **推理 / 部署**：以工具形态原生集成进 ChatGPT 与 Sora，2025-04 起经 Image API 暴露为 `gpt-image-1`（API 博客称 Responses API 支持"即将推出 / coming soon"，发布时仅 Image API 全球可用）。
- **推理时延**：出图较慢，博客明示"因为生成更精细的图，单图常需最多约 1 分钟"——符合自回归逐 token + 扩散末端渲染的两段式开销。
- **推理定价（gpt-image-1，按 token 计费，文本/图像分开计价）**：
  - 文本输入 token：$5 / 1M
  - 图像输入 token：$10 / 1M
  - 图像输出 token：$40 / 1M
  - 等效到单张方形图：低/中/高质量约 **$0.02 / $0.07 / $0.19**。
  - moderation 参数可调（auto 默认 / low 宽松）。
- **量化 / KV cache / 缓存命中等推理优化细节：未披露。** system card 列出独立的 Inference 团队（leads: Brendan Quinn, Tomer Kaftan），但工程细节不公开。

## 评测 benchmark（把效果讲清楚）
OpenAI 对图像生成**没有公布 FID / GenEval / DPG-Bench / T2I-CompBench / HPSv2 / ImageReward 等标准学界指标**——发布材料以能力演示 + 安全/偏差量化为主。可抠到的一手数字：

**能力侧（定性 + 半定量，来自 4o image gen 博客）**
- **指令跟随/多物体绑定**：可同时协调 **10–20 个不同物体**，而"其他系统处理约 5–8 个物体已显吃力"（官方对比口径，未点名对手、未给标准 bench 分）。
- **文本渲染、多轮对话式编辑、in-context learning、世界知识**：均以 best-of-N 样例展示（如 best of 8 / best of ~16），无量化分。
- **采用度（产品指标）**：ChatGPT 出图上线**首周 >1.3 亿用户生成 >7 亿张图**（gpt-image-1 API 博客引 OpenAI COO 数据）。

**安全/偏差侧（来自 Native Image Generation System Card，有具体数字）**
- 安全栈 not_unsafe / not_overrefuse（外部人工红队，含 system 缓解 + chat 拒答）：**0.971 / 0.856**；自动红队 **0.975 / 0.830**；真实场景 **0.932 / 0.993**。
- 分项 not_unsafe（system+chat 拒答）：色情 0.979（人工）/0.992（自动）；暴力仇恨 0.952/0.968；违法指引 0.999/0.977。
- **photorealistic-person 分类器**（4000 张测试集）：photorealistic person precision 0.905 / recall 0.99；adult 0.80/0.776；child 0.80/0.97（偏保守，模糊样本判 child）。
- **偏差（vs [[dall-e-3]]，4o 全面更优）**：
  - 性别（individuals 男/女）：DALL·E 3 86%/14% → 4o 79%/21%；Shannon 熵 0.17→0.27、异质输出频率 35%→46%。
  - 种族（individuals White%）：DALL·E 3 90% → 4o 67%（Black 0%→19%）；熵 0.13→0.36、异质 52%→85%。
  - 肤色（individuals Light%）：90%→59%；熵 0.18→0.50、异质 61%→96%。
  - 历史/现实准确性（不该乱改人口学时的匹配率）：DALL·E 3 92% → 4o **97%**（4o 基本饱和该内部评测）。

**已知消融/对比结论**：官方未发标准消融表；可总结的因果链是"原生嵌入 + 图文联合分布 + 强化后训练 → 文本渲染/多轮一致/多物体绑定/世界知识显著优于扩散+工具调用范式"，但缺学界可复现的数值对比。

## 创新点与影响
**核心贡献**
1. **把图像生成做成 LLM 的原生一等能力**：自回归主干 + 扩散解码器，端到端嵌入 omni 模型，而非外挂扩散 + 工具调用。由此一举解决文本渲染、多轮对话式编辑一致性、复杂指令/多物体绑定、利用世界知识与上传图做 in-context 生成等扩散范式的老大难。
2. **产品级"实用出图"范式**：从"惊艳但中看不中用"的艺术图，转向徽标/图表/菜单/连环画/UI 等"工作型"图像，强调精准、可控、可迭代。
3. **omni 架构的公开里程碑**：GPT‑4o 把 text/audio/image/video 收进单网络（音频可 232ms 最快、平均 320ms 响应，接近人类对话延迟），为"一个模型干所有模态"提供了产品级证明。

**影响**
- 直接定义并点燃了 2025 年"原生出图"竞赛：[[gemini-2-0-flash-native-image]] / Nano-Banana、各开源统一模型（[[emu3]]/[[transfusion]]/[[chameleon]] 路线）均沿"自回归 + 原生多模态"方向加码。
- 把"对话式连续编辑 + 文本渲染 + 世界知识出图"立为新基线，重塑了文生图产品的能力预期。
- C2PA 来源元数据 + 内部溯源工具成为大厂出图的事实标配方向。

**已知局限（官方自陈）**
- 长图（如海报）底部偶被裁切过紧；高密度信息/小字体、精确制图、多语言文本渲染、超长 prompt 的高精度绑定与编辑精度仍有 hallucination；
- 人口学表征仍偏男性/浅肤色（虽优于 DALL·E 3）；
- 对在世艺术家风格做了保守拒答；编辑真人照片、生成未成年人照片级图像有严格限制；
- **架构/数据/训练/算力的工程细节几乎全部不公开**，外部只能据 system card 的"自回归"定性 + 博客白板的"AR prior + diffusion decoder"示意来推断。

## 原始链接
- blog (主, omni 发布): https://openai.com/index/hello-gpt-4o/
- system-card (omni 本体, 架构/数据/训练): https://openai.com/index/gpt-4o-system-card/
- blog (原生图像生成正式发布, 2025-03): https://openai.com/index/introducing-4o-image-generation/
- system-card-addendum 页 (2025-03): https://openai.com/index/gpt-4o-image-generation-system-card-addendum/
- system-card PDF (Native Image Generation): https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf
- blog (gpt-image-1 进 API, 2025-04, 定价/采用度): https://openai.com/index/image-generation-api/

## 一手源存档（sources/）
- [hello-gpt4o-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gpt-4o-native-image--hello-gpt4o-blog.md)
- [gpt4o-system-card.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gpt-4o-native-image--gpt4o-system-card.md)
- [introducing-4o-image-gen-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gpt-4o-native-image--introducing-4o-image-gen-blog.md)
- gpt-4o-native-image-system-card.pdf （PDF，.gitignore 排除，仅本地）  （PDF 不入 git，走 HF bucket）
- [image-gen-system-card-addendum.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gpt-4o-native-image--image-gen-system-card-addendum.md)
- [gpt-image-1-api-blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/gpt-4o-native-image--gpt-image-1-api-blog.md)
