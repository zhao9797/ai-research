---
title: "GPT Image 1 / 4o 原生图像生成（GPT-4o native image generation）"
org: OpenAI
country: US
date: "2025-03"
type: system-card
category: omni
tags: [autoregressive, omnimodal, text-rendering, image-editing, instruction-following, c2pa, gpt-4o, closed-source]
url: https://openai.com/index/introducing-4o-image-generation/
arxiv: ""
pdf_url: https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: https://openai.com/index/image-generation-api/
downloaded: [gpt-image-1--introducing-4o-image-generation.md, gpt-image-1--image-generation-api.md, gpt-image-1--system-card-addendum.md, gpt-image-1-native-image-generation-system-card.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
GPT-4o 原生图像生成（API 名 `gpt-image-1`）是 OpenAI 把图像生成「焊进」GPT-4o 全模态模型架构、用**自回归 transformer**而非独立扩散模型直接生图的产物，核心创新是把图像作为与文本同一序列里的 token 与世界知识/对话上下文统一建模，从而带来**业界领先的指令遵循（可稳定协调 10–20 个对象）、精确文字渲染、强 in-context 图生图**；上线一周即 1.3 亿用户生成 7 亿张图，引爆「吉卜力风」全网风潮。

## 背景与定位
此前 OpenAI 的图像生成走的是 [[dall-e-3]] 路线：一个独立的**扩散模型**，由 GPT 通过 tool-call 间接调用（GPT 改写 prompt → 扩散模型出图），图像生成与语言模型在架构上是两套系统。其代价是：图像模型不能直接「用上」语言模型的世界知识与对话上下文，文字渲染弱、多对象绑定差、难以做多轮对话式精修。

4o 原生图像生成是路线上的根本切换。System Card 原文明确：

> "Unlike DALL·E, which operates as a diffusion model, 4o image generation is an autoregressive model natively embedded within ChatGPT."（不同于作为扩散模型的 DALL·E，4o 图像生成是一个**原生嵌入 ChatGPT 的自回归模型**。）

发布博客白板照片（团队故意把方法论写在白板上拍出来）进一步点题，这是 OpenAI 对其方法最直接的一手披露：

> "Suppose we directly model p(text, pixels, sound) with one big autoregressive transformer. Pros: image generation augmented with vast world knowledge; next-level text rendering; native in-context learning; unified post-training stack. Cons: varying bit-rate across modalities; compute not adaptive. Fixes: model compressed representations; compose autoregressive prior with a powerful decoder. tokens → [transformer] → [diffusion] → pixels"

即：用**一个大自回归 transformer 直接对 p(文本, 像素, 声音) 联合建模**，好处是图像生成可调用海量世界知识、文字渲染上台阶、原生 in-context learning、统一的后训练栈；坏处是各模态比特率不一、算力不自适应；解法是对**压缩表示**建模、并把**自回归先验 + 一个强解码器**组合起来，流水线是 `tokens → [transformer] → [diffusion] → pixels`。它把 t2i / 图像编辑 / 多轮精修 / 图文混合理解统一进同一个 omni 模型，是 2025 年「统一多模态生成」浪潮（对比同年开源侧的 [[bagel]] / [[janus-pro]] / [[show-o2]]、闭源侧的 Gemini Nano-Banana 等）里影响力最大的一步。

## 模型架构
说明：OpenAI **未发布论文或技术报告**，没有公开参数量、tokenizer 细节、解码器结构、训练配方等硬指标。以下仅是一手源（发布博客白板 + System Card + API 博客）确凿披露/明示的部分，工程细节大量**未披露**。

- **范式：自回归（autoregressive），而非扩散主干。** System Card 明确把它与 DALL·E 的扩散范式对立。图像被当作 token 序列，与文本（白板上还写了 sound）由**同一个自回归 transformer** 在 `p(text, pixels, sound)` 联合分布上自回归建模——这正是「原生/native」「omnimodal」的含义：生成图像与 GPT-4o 的语言能力共享同一套权重与上下文，所以能直接调用世界知识、做对话式多轮精修、把上传图片作为 in-context 参考。
- **「自回归先验 + 强解码器」两段式。** 白板写明 `tokens → [transformer] → [diffusion] → pixels`：自回归 transformer 在**压缩表示（compressed representations）**层面预测图像 token（应对「各模态比特率不同」），再由一个**扩散解码器**把这些 token/潜表示渲染回像素。也就是说 4o 并非完全抛弃扩散，而是把扩散降级为**末端的 decoder**，自回归 transformer 才是承载语义/指令/文字的主体。注意：tokenizer/VQ、潜空间维度、解码器规模等**均未披露**。
- **条件注入 = 同一序列内的上下文。** 由于原生嵌入，文本指令、上传图片、历史对话都进入同一个 token 序列，「条件」不是外挂 cross-attention，而就是**自回归上下文本身**——这解释了其超强指令遵循与图生图一致性（如多轮设计游戏角色仍保持外观连贯）。
- **参数量 / 分辨率策略：未披露。** 仅知生成偏慢（博客称「单张常需最长约 1 分钟」），支持指定宽高比、十六进制精确配色、透明背景；裁剪是已知缺陷（长图如海报易被裁紧，尤其底部）。

## 数据
OpenAI 对训练数据披露极简，**几乎全部具体规模/配比/清洗细节未披露**，只有方向性表述：

- **联合分布训练（一手原文）：** 「我们对模型进行了网络图像与文本的联合分布训练（trained on the joint distribution of online images and text），使其不仅理解图像与语言的关联，更掌握了图像彼此间的关系」。这是少有的对训练目标的直接描述——图文联合 + 图-图关系。
- **风格覆盖：** 「通过对海量多样图像风格的训练，模型能够逼真地创建或转换各种风格」；解释了照片级写实与跨风格迁移（含引爆全网的吉卜力风）的来源。
- **后训练混合（post-training mixture）：** System Card 在「Bias」一节提到将通过「**incorporating more diverse examples into the post-training mixture**」改善人口学表征——确证存在一个独立的后训练数据混合阶段，但配比未公开。
- 规模、来源清单、re-captioning（DALL·E 3 曾重度依赖合成 caption，且核心作者 James Betker 在列）、美学/安全过滤管线：**均未披露**。合成数据是否参与 caption 生成可合理推测但**官方未确认**，不写入结论。

## 训练方法
同样**无论文**，按一手源能确定的：

- **训练目标：自回归 next-token（在压缩图像表示上）**，配末端扩散解码器；非纯 flow-matching/扩散端到端。具体 token 化方案、解码器是否走 consistency/蒸馏加速**未披露**。
- **强化的后训练（reinforced post-training）：** 发布博客原文「再结合强化的后期训练（enhanced post-training），最终模型展现出卓越的视觉表现力」。System Card 提到「post-training safety measures」「post-training mixture」「post-training mitigations」。可确认存在**多阶段后训练**（含安全对齐 + 偏差缓解 + 能力增强），但是否用 RLHF/DPO/reward model、用何种偏好数据**未披露**。
- **安全侧的「推理式对齐」：** 发布博客称采用类似 [[deliberative-alignment]] 的方法，**训练了一个专用推理 LLM**，直接依据人类编写、可解释的安全规范工作，用于在开发期识别政策模糊地带，并在部署期作为「safety-focused reasoning monitor」对输出图像做多模态审核（见 Infra）。
- 蒸馏/步数加速/缓存等推理优化细节：**未披露**（且生成偏慢，暗示未做激进步数蒸馏）。

## Infra（训练 / 推理工程）
- **训练算力 / GPU·时 / 并行策略：完全未披露。**
- **推理形态：** 作为工具内嵌于 ChatGPT/Sora，并以 `gpt-image-1` 经 Images API 暴露。生成延迟高（最长约 1 分钟/张），侧面说明是大模型自回归逐 token 出图 + 扩散解码，未走极致蒸馏。
- **多层安全栈（System Card 明确）：**
  1. **Chat model refusals**——主聊天模型作为第一道防线，可基于后训练安全策略直接拒绝触发生图；
  2. **Prompt blocking**——生图工具被调用后，文本/图像分类器命中违规即拦截；
  3. **Output blocking**——出图后用 CSAM 分类器 + **多模态推理监视器（custom-trained reasoning model）** 复核并拦截违规图；
  4. **未成年人加强防护** + 上传图的**写实人物分类器**（基于 Sora 的 under-18 分类器，三分类：无写实人物 / 写实成人 / 写实儿童；近 4000 张评测集）。
- **溯源（provenance）：** 所有产出图带 **C2PA 元数据**（可验证来源、行业标准）；另有内部检索/取证工具，用图像技术特征判断是否出自 OpenAI 产品。
- **API 计费与成本（一手）：** 按 token 计费，文本输入 \$5 / 图像输入 \$10 / 图像输出 \$40（每百万 token）；折合每张约 \$0.02（低）/ \$0.07（中）/ \$0.19（高，1024² 方图）。提供 `moderation` 参数（默认 `auto`，可调 `low` 放宽）。默认不拿客户 API 数据训练。

## 评测 benchmark（把效果讲清楚）
重要诚实说明：**OpenAI 未公布任何标准学术 benchmark 数字**（无 FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 编辑 benchmark / Arena ELO 等）。一手源里**唯一成体系的量化数据是 System Card 的安全与偏差评测**，以及发布博客对能力的定性描述。下列数字均直接来自已落盘一手源，不作外推。

**能力（定性，发布博客）：**
- 指令遵循：其他系统约 5–8 个对象就吃力时，4o 可同时协调 **10–20 个不同对象**，对象-属性-关系绑定更强。
- 文字渲染、多轮对话式精修一致性、in-context 学习（学上传图细节）、世界知识（结合文本+图像知识，如读 Three.js 代码后画出语义图）为四大亮点。
- 已知局限（博客「限制」节）：长图/海报易被**裁剪**过紧（尤其底部）；高对象数下偶发幻觉/绑定错误；精确制图、多语言文字渲染、编辑精度、密集小字仍有限。

**安全栈整体指标（System Card，两指标 not_unsafe / not_overrefuse，越高越好）：**
| 数据源 | 仅系统缓解 | 系统缓解+聊天模型拒绝 |
|---|---|---|
| 外部人工红队 | 0.955 / 0.941 | 0.971 / 0.856 |
| 自动红队 | 0.969 / 0.899 | 0.975 / 0.830 |
| 真实场景离线 | 0.929 / 0.996 | 0.932 / 0.993 |

（叠加聊天模型拒绝后 not_unsafe 升、not_overrefuse 降，体现安全-可用的 tradeoff。）

**分风险域安全评测（System Card 节选，not_unsafe / not_overrefuse）：**
- 色情内容：人工红队 364 例 0.971/0.912，+拒绝 0.979/0.884；自动 927 例 0.990/0.875。
- 暴力/辱骂/仇恨：人工 1266 例 0.914/0.917，+拒绝 0.952/0.795；自动 1627 例 0.959/0.889。
- 违法活动指引：人工 25 例 0.999/0.959；自动 309 例 0.972/0.974。
- 写实人物分类器（近 4000 图）：写实人物 precision 0.905 / recall 0.99；写实成人 0.80/0.776；写实儿童 0.80/0.97（刻意偏保守，模糊样本判为「儿童」）。

**偏差评测（System Card，全面优于 [[dall-e-3]]，Shannon 熵越高越均衡）：**
- 性别（individuals）类分布 男/女：DALL·E 3 86%/14% → 4o 79%/21%；熵 0.17→0.27；异质输出率 35%→46%。groups：61/35→56/44；熵 0.82→0.95；异质率 95%→100%。
- 种族（individuals）White：DALL·E 3 90% → 4o 67%，Black 0%→19%；熵 0.13→0.36；异质率 52%→85%。
- 肤色（individuals）Light：90%→59%，Dark 0%→12%；熵 0.18→0.50；异质率 61%→96%。
- 反历史/不真实偏差（命中预期属性比例，越高越好）：DALL·E 3 92% → 4o **97%**（4o 在内部该评测上接近饱和）。
- 结论：4o 在所有偏差指标上均优于 DALL·E 3，但**男性主体仍偏多、白人/浅肤色仍偏多**，OpenAI 称将靠更多元的后训练混合继续改进。

**采纳度（API 博客）：** 上线一周 1.3 亿用户、生成超 7 亿张图（首周）；Adobe(Firefly/Express)、Canva、Figma、Wix、GoDaddy、HubSpot、Instacart、invideo 等接入 `gpt-image-1`。

## 创新点与影响
- **核心贡献：把图像生成做成 LLM 的原生能力**——用单一自回归 transformer 联合建模文本+像素（+声音），扩散仅作末端解码器，从而第一次让生图直接吃到 LLM 的世界知识、对话上下文与统一后训练栈。这是与「扩散主干 + tool-call」范式（DALL·E 3、SD、Midjourney 等）的路线分野。
- **能力新标杆：** 强指令遵循（10–20 对象）、可靠文字渲染、对话式多轮一致编辑、in-context 图生图，把「实用型/工作型图像」（图表、UI、海报、徽标、示意图）从扩散模型的弱项变成强项。
- **产品与文化影响：** 引爆「吉卜力风」全民玩梗与现象级增长（首周 7 亿图），直接带动 2025 年「统一多模态生成」竞赛（开源侧 [[bagel]]/[[janus-pro]] 等、谷歌 Gemini 原生生图/Nano-Banana 等闭源跟进）；并把原生多模态从「能看图」推进到「能原生生图编辑」。
- **安全治理范式：** 多层安全栈（聊天拒绝 + prompt/output 双盲拦截 + 多模态推理监视器）、对未成年人/CSAM 的写实人物分类器、living-artist 风格拒绝、对公众人物从「一律封禁」放宽到「细粒度+可 opt-out」、全量 C2PA 溯源——成为后续生图产品安全设计的事实模板。
- **已知局限：** 生成慢（约 1 分钟/张）；长图裁剪、密集小字、精确制图、多语言渲染、编辑精度仍弱；偏差虽减但未消除；**架构/数据/训练/算力全部闭源，无可复现技术细节、无标准学术 benchmark**——这是从研究角度评估它的最大缺口。

## 原始链接
- blog（发布，含白板方法图，一手最权威）: https://openai.com/index/introducing-4o-image-generation/
- blog（API 上线 `gpt-image-1`，含定价/采纳度）: https://openai.com/index/image-generation-api/
- system-card-addendum（页面入口）: https://openai.com/index/gpt-4o-image-generation-system-card-addendum/
- system-card（PDF 正文，安全/偏差量化）: https://cdn.openai.com/11998be9-5319-4302-bfbf-1167e093f1fb/Native_Image_Generation_System_Card.pdf

## 一手源存档（sources/）
- [introducing-4o-image-generation.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/gpt-image-1--introducing-4o-image-generation.md)
- [image-generation-api.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/gpt-image-1--image-generation-api.md)
- [system-card-addendum.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/gpt-image-1--system-card-addendum.md)
- gpt-image-1-native-image-generation-system-card.pdf （PDF，.gitignore 排除，不入 git，本地精读）
