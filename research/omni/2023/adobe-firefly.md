---
title: "Adobe Firefly（首个图像模型 + Photoshop Generative Fill）"
org: Adobe
country: US
date: "2023-03"
type: blog
category: t2i
tags: [t2i, diffusion, commercial-safe, generative-fill, editing, closed-source, adobe-stock, content-credentials]
url: "https://news.adobe.com/news/news-details/2023/adobe-unveils-firefly-a-family-of-new-creative-generative-ai"
arxiv: ""
pdf_url: ""
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://www.adobe.com/products/firefly.html"
downloaded: [adobe-firefly--press-release.md, adobe-firefly--launch-blog.md, adobe-firefly--gen-ai-approach.md, adobe-firefly--photoshop-generative-fill.md, adobe-firefly--max-2023-firefly-update.md, adobe-firefly--vs-stable-diffusion.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Adobe Firefly 是 Adobe 2023 年 3 月推出的**商业版权安全文生图（t2i）模型家族**，首个图像模型为**扩散模型（diffusion model）**，只在 **Adobe Stock 授权图、公开授权内容与版权过期的公共领域内容**上训练；最大产品意义是 5 月把它做成 Photoshop 的 **Generative Fill（生成式填充）**——基于选区 + 文本提示做无损的增/删/扩内容，自动匹配透视/光照/风格。截至 2023 年 10 月 Adobe MAX，初代模型已生成**逾 30 亿张图像**，号称同期"为商业安全设计"的最受欢迎图像生成模型。

> 注意：Firefly 是**闭源商业产品**，Adobe **从未发布技术论文 / 技术报告 / 模型权重 / 架构白皮书**，也**未公开任何标准 benchmark 数字**（FID / CLIPScore / GenEval / 人评 ELO 一律未报告）。本页所有内容均来自 Adobe 官方博客 / 新闻稿 / 产品页一手源；"扩散模型""Adobe Stock 训练"这两条是官方明示，其余工程细节大多**未披露**，下文逐一标注。

## 背景与定位
2022—2023 年 t2i 爆发（[[dall-e-2]]、[[stable-diffusion-1]]、Midjourney），但这批模型都在**网络抓取的大规模图文数据**（如 LAION）上训练，引发版权/IP 争议——尤其对 Adobe 的核心客户群（专业设计师、品牌方、企业创意团队）而言，"输出能否安全用于商业"是刚需。Firefly 的差异化定位正是把"**commercially safe（商业安全）**"做成第一卖点：

- 与 [[stable-diffusion-1]] / [[dall-e-2]] 不同，Firefly **不抓取网络/视频站内容**，只在有授权或版权已过期的数据上训练，避免生成基于他人作品/品牌/IP 的内容（官方 gen-ai-approach 页明确："We do not mine the web or video hosting sites for content"）。
- 技术上不是新范式创新，而是把成熟的**潜空间扩散文生图**（思路同 [[latent-diffusion-ldm]] / [[stable-diffusion-1]]）落到**干净授权数据 + 深度产品集成 + 内容溯源（Content Credentials / C2PA）**这条工程化路线上。
- 与同期纯生成模型相比，Firefly 真正的护城河是**集成进 Photoshop / Illustrator / Express 的编辑工作流**：Generative Fill 把 t2i 变成基于选区的局部编辑（概念上类似 [[stable-diffusion-img2img-inpaint]] 的 inpainting，但产品体验上做成"上下文任务栏一键生成 + 生成图层非破坏式编辑"）。

## 模型架构
**官方仅披露：Firefly 首个图像模型是"diffusion model（扩散模型）"。** 来自 Adobe 官方页面 firefly-vs-stable-diffusion："*Firefly is a diffusion model, which is designed to create images from text prompts*"。

除此之外，架构细节**全部未披露**：
- **backbone**：未披露是 U-Net 还是 DiT/MMDiT。结合 2023 年初的技术水位与"diffusion model"表述，业界普遍推测初代为**潜空间 U-Net 扩散**（latent diffusion，类 [[latent-diffusion-ldm]]），但 **Adobe 从未官方确认**。
- **visual tokenizer / VAE / VQ**：未披露。
- **text encoder（T5 / CLIP / LLM）**：未披露。
- **参数量**：未披露。
- **分辨率策略**：未披露具体训练/输出分辨率；官方仅强调 Adobe Stock 为"高分辨率（high-resolution）专业级图像"。
- **条件注入 / 控制**：产品层面暴露的可控项包括——内容类型三选一（**Photo / Graphic / Art**）、Styles（艺术流派如立体主义/极繁主义）、Lighting、composition、以及材质（fur/clay 等）控制；这些是 UI 控件，底层如何注入条件未披露。

**Generative Fill（Photoshop，2023-05）的产品机制**（非底层架构，官方博客描述）：集成进 Photoshop 的**每一个选区工具**；做出选区后弹出 **Contextual Task Bar（上下文任务栏）**；可带或不带文本提示生成；生成结果落在新的 **Generative Layer（生成图层）**实现非破坏式编辑；"Photoshop 分析选区周边区域，自动生成带合适阴影、反射、光照、透视的新内容"；每次生成给 **3 个候选**（Firefly 网页版每个 prompt 给 **4 个变体**）。

## 数据
**这是 Firefly 唯一被详细披露的维度，也是其核心卖点。**

- **训练数据来源（官方明示，press release + gen-ai-approach + vs-SD 三处一致）**：
  1. **Adobe Stock** 图库——"数亿张（hundreds of millions of）专业级、授权、高分辨率图像"，依 Stock Contributor License 协议使用；
  2. **公开授权内容（openly licensed content）**；
  3. **版权已过期的公共领域内容（public domain where copyright has expired）**。
- **明确不用**：不抓取网络（"publicly available online data"）、不抓视频站、**从不在用户/客户内容上训练**（官方反复声明，并写进 General Terms of Use 第 **2.2F / 4.3C2** 条；另第 **4.2** 条申明 Adobe 不主张对用户用 Firefly 生成内容的所有权——属"不主张版权"条款，与"不训练"是两回事，gen-ai-approach 页分别列出）。
- **规模/配比/清洗**：除"数亿张 Adobe Stock 图"外，**精确数量、三类数据配比、去重/清洗/美学过滤流程均未披露**。
- **标注 / re-captioning / 合成数据**：**未披露**是否做了 re-caption 或引入合成数据。
- **安全过滤**：官方称在**训练前、生成时、prompt 时、输出时**四个环节都部署 safeguard，防止生成侵犯版权/IP 的内容、并测试以减少有害偏见（harmful bias）；具体过滤器实现未披露。还对 Adobe Stock 做了审核策略整改，禁止引用/复制其他艺术家姓名与风格的内容入库。
- **创作者补偿**：对内容被用于训练的 Adobe Stock 贡献者给予补偿（2023-09 落地 **Firefly Contributor Bonus**），属业内首创的"训练数据付费"机制。
- **衍生模型数据**：2023-10 推出的 **Firefly Design Model**（驱动 Express 的 Text to Template）在"**数十万张高质量 Adobe Express 模板**"上训练——再次印证 Adobe"用自家授权资产训练专用模型"的打法。同期 MAX 还发布了 **Firefly Vector Model**（驱动 Illustrator 的 Text to Vector Graphic，号称"业界首个矢量图生成模型"）与 **Firefly Image 2 Model**（初代图像模型的继任，官方仅定性称"more model capacity / 更好图像质量"，可在 Firefly web app 与 Image 1 切换对比；具体数据/架构同样未披露）。本页焦点仍是 **2023-03 的初代图像模型**。

## 训练方法
**几乎全部未披露。** Adobe 未公开任何训练目标、阶段划分、对齐方法或加速技术：
- **训练目标**：仅知是 diffusion model（即扩散去噪目标），**未披露**是标准 DDPM-style ε-prediction、v-prediction 还是 flow matching / rectified flow。
- **多阶段（预训练→SFT→偏好对齐 RLHF/DPO/reward model）**：**未披露**是否有 SFT / 偏好对齐 / reward model。
- **蒸馏与加速（consistency / LCM / ADD / 步数蒸馏）**：**未披露**。Generative Fill 宣传"seconds（数秒）"出图，但未说明是否做了步数蒸馏。
- **"powerful style engine"**：launch blog 提到给模型增配了一个"强大的风格引擎"来支持 color/tone/lighting/composition 控制，但**未给任何技术细节**。
- 一句话：训练方法维度 Adobe 基本**全程不透明**，无法抠出任何超参或 trick。

## Infra（训练 / 推理工程）
**未披露。** 算力规模、GPU·时、并行/分布式策略、混合精度、训练吞吐——Adobe **一概未公开**。

- 推理/部署形态可见：**Firefly 独立网页应用**（firefly.adobe.com）+ **嵌入 Creative Cloud / Document Cloud / Experience Cloud / Adobe Express 各 App**（Photoshop Generative Fill、Illustrator Generative Recolor / Text to Vector、Lightroom Generative Remove、Express Text to Template / Generative Fill）+ **对外开放 API**（后演化为 Firefly Services for Business）。
- 推理加速（步数/缓存/量化/蒸馏）**未披露**。
- 规模佐证：初代模型 2023-03 beta 上线后到 2023-10 累计生成 **逾 30 亿张图像**，支持 **100+ 种语言的文本提示**（Firefly 网页应用 UI 支持 20 种语言）——侧面说明其推理服务承载量很大，但具体工程未公开。

## 评测 benchmark（把效果讲清楚）
**Adobe 没有公布任何标准学术 benchmark 数字。**

- **FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 人评 ELO / Arena**：**全部未报告**（一手源里完全没有）。Firefly 作为闭源商业产品，没有进入也没有自报这些 benchmark。
- **官方"效果"仅以使用量与定性表述呈现**：
  - 生成图像累计 **> 30 亿张**（2023-03 beta → 2023-10 MAX），自称"**为商业安全设计的、最受欢迎的 AI 图像生成模型**"（口径限定在"safe for commercial use"这一细分）；
  - 支持 **100+ 语言**提示词；
  - Generative Fill 自称"自动匹配透视、光照、风格"，结果"realistic"；但**无任何量化对比或消融实验**。
- **消融结论**：无（Adobe 未发任何论文/技术报告，自然无消融）。
- 第三方独立评测（如有）不在本次一手源范围内，按规范不在此编造。**结论：benchmark 维度 = 未报告。**

## 创新点与影响
**核心贡献（更多是产品/商业模式创新，而非技术创新）：**
1. **"商业版权安全"作为产品第一原则**：首个把"训练数据干净（仅授权 + 公共领域）→ 输出可安全商用 → 企业 IP 赔付（indemnification）"做成完整闭环的主流 t2i，给企业客户解决了 SD/Midjourney 时代最大的法务顾虑。
2. **生成式编辑的工作流落地（Generative Fill）**：把 t2i 从"独立出图"推进到"嵌入专业编辑器、基于选区、非破坏式、上下文一键"的形态，重新定义了 Photoshop 的选区与图层范式——这是 Firefly 影响力最大的部分，被广泛认为是把生成式 AI 真正带进数亿专业创作者日常工作流的标志性产品。
3. **创作者补偿 + 内容溯源**：Firefly Contributor Bonus（训练数据付费）+ 默认写入 **Content Credentials（C2PA 防篡改元数据）**+ 倡导"Do Not Train"标签 + FAIR Act 立法倡议，建立了一套"负责任生成式 AI"的产业范式。

**对后续工作的影响**：确立了"授权数据 + 深度产品集成 + 内容溯源"这条与开源/抓取路线并行的商业路线；Generative Fill 直接推动了同类 inpainting-as-product 的竞品跟进。

**已知局限**：
- **技术透明度极低**：无论文、无权重、无架构、无 benchmark，外界无法复现或客观对比其生成质量；
- 初代在 beta 期"**不可商用、不向 18 岁以下开放、不在中国提供、仅支持英文提示**"（Generative Fill 2023-05 免责声明），早期可用性受限；
- 质量上限受"仅授权数据"约束——数据多样性/规模不及网络级数据，可能在长尾概念/名人/特定风格上弱于抓取网络数据训练的竞品（Adobe 官方亦承认"generative AI is not right for every scenario"）。

## 原始链接
- press-release（官方新闻稿，2023-03-21）: https://news.adobe.com/news/news-details/2023/adobe-unveils-firefly-a-family-of-new-creative-generative-ai
- launch-blog（发布博客，David Wadhwani，2023-03-21）: https://blog.adobe.com/en/publish/2023/03/21/bringing-gen-ai-to-creative-cloud-adobe-firefly
- gen-ai-approach（Adobe 生成式 AI 方法/数据来源页）: https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html
- generative-fill（Photoshop Generative Fill 发布博客，2023-05-23）: https://blog.adobe.com/en/publish/2023/05/23/future-of-photoshop-powered-by-adobe-firefly
- max-2023-update（Adobe MAX Firefly 更新，30 亿张/100+ 语言/Design Model，2023-10-10）: https://blog.adobe.com/en/publish/2023/10/10/future-is-firefly-adobe-max
- vs-stable-diffusion（Adobe 官方对比页，明示"Firefly is a diffusion model"）: https://www.adobe.com/products/firefly/discover/firefly-vs-stable-diffusion.html
- product（产品页）: https://www.adobe.com/products/firefly.html

## 本地落盘文件
- ../../../sources/omni/2023/adobe-firefly--press-release.md
- ../../../sources/omni/2023/adobe-firefly--launch-blog.md
- ../../../sources/omni/2023/adobe-firefly--gen-ai-approach.md
- ../../../sources/omni/2023/adobe-firefly--photoshop-generative-fill.md
- ../../../sources/omni/2023/adobe-firefly--max-2023-firefly-update.md
- ../../../sources/omni/2023/adobe-firefly--vs-stable-diffusion.md
