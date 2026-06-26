---
title: "Adobe Firefly Image Model 4 / 4 Ultra"
org: "Adobe"
country: US
date: "2025-04"
type: blog
category: t2i
tags: [t2i, firefly, adobe, commercially-safe, closed-source, creative-cloud, photorealism]
url: "https://blog.adobe.com/en/publish/2025/04/24/adobe-firefly-next-evolution-creative-ai-is-here"
arxiv: ""
pdf_url: "https://www.adobe.com/cc-shared/assets/pdf/business/teams/sdk/firefly-image-model-4-guide.pdf"
github_url: ""
hf_url: ""
modelscope_url: ""
project_url: "https://firefly.adobe.com/"
downloaded: [firefly-image-model-4--blog.md, firefly-image-model-4--press-release.md, firefly-image-model-4--gen-ai-approach.md, firefly-image-model-4-guide.pdf, firefly-image-model-4--api-generate-tutorial.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
Adobe Firefly **Image Model 4 / 4 Ultra** 是 Adobe 在 2025-04-24 伦敦 MAX 上发布的第四代商用文生图模型（闭源、托管式），主打"商业安全（commercially safe）"——**只用「授权内容（licensed content，含 Adobe Stock 及其他授权素材）+ 版权已过期的公共领域内容」训练，从不爬网、从不用客户内容**（官方 Guide 表述为 "Adobe Stock, public domain, and licensed material"）；相比上一代 [[adobe-firefly-image-3]] 在提示词遵循、人物/动物/建筑细节和真实感上大幅提升，支持**最高 2K（16:9 对应 2688×1536）分辨率**，并提供 Structure/Style Reference、相机角度、视觉强度（9 档）等强可控性，深度集成 Photoshop / Premiere Pro / Express / Firefly Services API。Ultra 版定位"复杂场景与极致细节"，标准版定位"快速 ideation，覆盖 90% 日常需求"。

## 背景与定位
Firefly 自 2023 年首发以来，是市场上极少数把"训练数据合规、可商用、企业 IP 赔付"作为第一卖点的生成式图像产品——其差异化不在某个 benchmark 数字，而在**法律与商业可用性**：面向 Deloitte、Tapestry、Paramount+、Pepsi、Estée Lauder 等品牌的生产环境内容。截至本次发布，Firefly 系列累计生成超过 **220 亿（22 billion）** 张资产。

Image Model 4 解决的核心问题是：在保持"商业安全"约束（不能像开放模型那样无差别吃全网数据）的前提下，把图像质量、提示遵循和可控性追到第一梯队。本次 MAX 发布是 Firefly 从"图像生成器"升级为"统一创意 AI 平台"的节点：同时官宣 [[firefly-video-model]] 正式 GA、Adobe Vector Model（Text-to-Vector）、Firefly Boards（协作 moodboard，原 Project Concept），并首次把**第三方模型**（OpenAI 图像、Google Imagen 3 / Veo 2、Black Forest Labs [[flux-1-1-pro]]）作为"非 Adobe 模型"接入 Firefly App，后续还规划 fal.ai、Ideogram、Luma、Pika、Runway。

技术脉络上，Firefly 属于商用闭源 t2i 阵营，与 [[midjourney]]、Google [[imagen-3]]、OpenAI 图像生成同列；其"licensed-data-only"路线与多数"爬全网"模型形成鲜明对照。**注意：Adobe 未公开 Firefly 任何架构/训练算法细节，本页凡涉及 backbone、损失函数、参数量、算力、benchmark 数字之处，官方均未披露，下文逐项标注"未披露"，不做推测。**

## 模型架构
**未披露。** Adobe 对 Image Model 4 / 4 Ultra 的网络结构（U-Net vs DiT/MMDiT vs 自回归）、visual tokenizer / VAE、text encoder（T5/CLIP/LLM）、条件注入机制、参数量、训练分辨率策略等**全部未公开**。官方仅披露面向用户/开发者的产品级事实：

- **两档模型一个家族**：
  - *Image Model 4*（标准）——定位"快速 ideation 与日常需求"，擅长简单插画、图标、单体物体照片、单主体肖像、单只动物，"快速且低成本覆盖约 90% 的典型创意需求"。
  - *Image Model 4 Ultra*——定位"复杂场景 + 小结构 + 极致细节"，擅长写实场景、人物肖像、中等人群，**优先精度而非速度**。
- **输出分辨率**：官方称"up to 2k resolution"，可裁切/重构图、可大幅面打印不掉质。Firefly Services v3 `generate` API 教程把 **2688×1536** 标注为 "A landscape (16:9) aspect ratio"（2K 量级；该尺寸为教程示例值，官方未在此处声明它是绝对上限）。
- **可控性（产品层）**：Structure Reference（构图参考）、Style Reference（风格参考，可从图库选或上传自有图）、相机角度/缩放控制、**视觉强度滑块（Visual Intensity，两端之间 9 档）**、Effects 预设、Composition Reference；可同时叠加 Composition + Style 参考。
- **接入形态**：Firefly Web App、即将上线的 Firefly 移动端（iOS/Android）、Photoshop Web / Express 导出、以及 Firefly Services 的 Text-to-Image API（`https://firefly-api.adobe.io/v3/images/generate`，基于 Image Model 4）。

## 数据
这是 Firefly 唯一被官方详细披露的维度（出自 Adobe "gen-ai-approach" 页与官方 Image Model 4 Guide）：

- **训练集只含授权 + 公共领域两大类**：① **授权内容（licensed content）**——以 Adobe Stock 为代表（单独许可协议，Adobe 对贡献者付费补偿），官方 gen-ai-approach 页表述为 "a dataset of licensed content, such as Adobe Stock"，官方 Guide 并列写为 "Adobe Stock, public domain, and licensed material"（即除 Adobe Stock 外还含其他授权素材）；② **版权已过期的公共领域内容**。
- **明确不做的事**：不爬网、不爬视频站、**从不用客户/用户内容训练**（在 General Terms of Use 2.2F、4.3C2 明文写入）；禁止第三方爬取托管在 Adobe 服务器（如 Behance）上的用户内容训练模型。
- **合规与安全**："commercially safe / IP-friendly"——在**训练前、生成中、prompt 阶段、输出阶段四个环节都部署 safeguard**，以避免生成侵犯版权/IP 的内容；对企业客户提供**知识产权赔付（IP indemnification）**。
- **数据规模 / 配比 / 清洗过滤 / re-captioning / 合成数据占比**：**均未披露**。仅有的能力性线索来自官方 Guide——"单主体效果最佳；中等/大型人群、人物动作、复杂文字渲染仍在持续打磨"，反映其数据/能力短板集中在多主体与文字渲染。
- 美学/安全过滤：官方提及"美学"相关的是用户侧的 Visual Intensity 与 Effects 控件，**训练侧的美学打分/安全过滤管线未披露**。

## 训练方法
**未披露。** Adobe 未公布任何训练目标（diffusion / flow matching / next-token / masked-token 不明）、多阶段流程（pre-train → SFT → 偏好对齐 / RLHF / DPO / reward model 不明）、蒸馏与加速方案（consistency / LCM / ADD / 步数蒸馏不明）、关键超参或 trick。官方仅以产品语言描述结果："the fastest, most controllable and most realistic Firefly image model yet"，并称标准版"fast"、Ultra"prioritizes precision over speed"——可推断两者在**速度/质量上做了差异化档位**，但具体是同模型不同采样配置、还是两套独立权重，Adobe 未说明。

## Infra（训练 / 推理工程）
**未披露。** 训练算力规模、GPU·时、并行/分布式策略、混合精度、吞吐均未公开；推理侧的步数、缓存、量化、蒸馏细节也未公开。可确认的部署事实：

- 纯**托管式云服务**，无权重下载（非开源、无 HF / ModelScope / GitHub 发布）。
- 通过 Firefly Web、Creative Cloud 桌面/Web 应用、移动端，以及 **Firefly Services REST API**（`v3/images/generate`，OAuth via `ims-na1.adobelogin.com`）对外暴露。
- 企业侧通过 Firefly Services（生成式 + 创意 API 集合）做规模化内容生产（批量改尺寸等），客户含 Accenture、dentsu、Gatorade/PepsiCo、Estée Lauder。
- 计费按生成额度（generation credits），具体定价见 Firefly plan 页面（本页未抓取定价细节）。

## 评测 benchmark（把效果讲清楚）
**未报告任何定量 benchmark。** Adobe 官方发布材料中**没有** FID / CLIPScore / GenEval / T2I-CompBench / DPG-Bench / MJHQ-30K / HPSv2 / ImageReward / PickScore / 人评 ELO 等任何数字，也未给出与同期 SOTA（Midjourney、Imagen 3、FLUX、GPT-image 等）的可比对照表。官方只有**定性主张**：

- 相对 [[adobe-firefly-image-3]]（Image Model 3）"显著提升"，提示词遵循（prompt fidelity）更强；
- 人物、动物、建筑元素渲染"精度、清晰度、真实感"明显更好；
- "fastest / most controllable / most realistic Firefly image model yet"。
- 官方 Guide 自陈的**已知短板**（可视为定性消融结论）：单主体效果最好；**中等/大型人群、人物动作、复杂文字渲染**仍在"finesse"阶段，效果未达标。

> 因此本维度只能记录"官方未公开任何量化评测"。第三方媒体（gigazine、redsharknews、aitoolssme 等）有主观评测，但非一手、未抓取，不录入数字。

## 创新点与影响
**核心贡献（产品/商业层，而非算法层）**：
1. **把"商业安全"做成可量化的产品承诺**：licensed-only 训练数据 + 四环节 safeguard + 企业 IP 赔付，是与几乎所有"爬全网"竞品的根本差异，也是其在品牌/企业生产环境被采用的护城河。
2. **质量 + 可控性并进**：在数据合规约束下把真实感/提示遵循追到第一梯队，同时提供 Structure/Style/Composition Reference、相机控制、9 档视觉强度等专业级控件；2K 输出满足印刷/裁切。
3. **标准/Ultra 双档**：用速度-质量分档覆盖"90% 日常 ideation"与"极致细节终稿"两类需求。
4. **平台化与开放第三方模型**：Firefly App 同时承载 Adobe 自家模型与 OpenAI/Imagen 3/Veo 2/FLUX 1.1 Pro 等第三方模型，配合 Content Credentials 做来源透明标注——这是闭源厂商少见的"模型聚合 + 溯源"策略。

**影响**：进一步把生成式图像推入企业级合规生产链路（Photoshop / Premiere Pro / Firefly Services API），并推动行业把"训练数据来源透明 + 内容凭证（C2PA / Content Credentials）"作为竞争维度。

**已知局限**：① **完全闭源、零技术披露**——无法复现、无法做学术对照，本页架构/训练/infra/benchmark 四维均因官方不公开而无法填实；② 多主体人群、人物动作、复杂文字渲染仍是弱项（官方自陈）；③ 受限于"只用授权 + 公共领域数据"，长尾概念覆盖可能不及爬全网模型（Adobe 未公开数据规模，无法量化此影响）。

## 原始链接
- blog（Adobe 官方博客，发布主稿）: https://blog.adobe.com/en/publish/2025/04/24/adobe-firefly-next-evolution-creative-ai-is-here
- press-release（Adobe Newsroom 新闻稿，含 2K 分辨率/能力定位）: https://news.adobe.com/news/2025/04/adobe-revolutionizes-ai-assisted-creativity-firefly
- gen-ai-approach（Adobe 官方"生成式 AI 方法"页，训练数据/商业安全权威来源）: https://www.adobe.com/ai/overview/firefly/gen-ai-approach.html
- guide-pdf（Adobe 官方 Image Model 4 Guide，模型分档/控件/能力短板）: https://www.adobe.com/cc-shared/assets/pdf/business/teams/sdk/firefly-image-model-4-guide.pdf
- api-tutorial（Firefly Services v3 generate API，含 2688×1536 最大尺寸与 endpoint）: https://developer.adobe.com/firefly-services/docs/firefly-api/guides/how-tos/firefly-generate-image-api-tutorial
- product（Firefly Web 入口）: https://firefly.adobe.com/

## 一手源存档（sources/）
- [blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/firefly-image-model-4--blog.md)
- [press-release.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/firefly-image-model-4--press-release.md)
- [gen-ai-approach.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/firefly-image-model-4--gen-ai-approach.md)
- firefly-image-model-4-guide.pdf （9.7 MB，.gitignore 排除，本地已落盘并精读）  （PDF 不入 git，走 HF bucket）
- [api-generate-tutorial.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2025/firefly-image-model-4--api-generate-tutorial.md)
