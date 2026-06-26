---
title: "DALL·E 3 系列产品化(ChatGPT 集成 / API)"
org: OpenAI
country: US
date: "2024"
type: blog
category: t2i
tags: [t2i, latent-diffusion, recaptioning, prompt-following, chatgpt, closed-source, openai, safety, system-card]
url: https://openai.com/index/dall-e-3/
arxiv:
pdf_url: https://cdn.openai.com/papers/dall-e-3.pdf
github_url: https://github.com/openai/dalle3-eval-samples
hf_url:
modelscope_url:
project_url: https://openai.com/index/dall-e-3/
downloaded: [dalle-3--blog.md, dalle-3-paper--text.md, dalle-3-paper-improving-image-generation.pdf, dalle-3-system-card--text.md, dalle-3-system-card.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DALL·E 3 是 OpenAI 把 **「合成 caption 重标注 + LLM 提示词改写」** 作为核心方法做到极致的闭源 T2I 系统:核心技术是用一个自训的 bespoke captioner 给训练集重写成高度描述性的合成 caption,并以 **95% 合成 + 5% 真值** 的混合比训练一个三阶段 latent-diffusion U-Net(T5-XXL 文本条件);2024 年它全面进入 **ChatGPT(Plus/Team/Enterprise)与 API**,由 GPT-4 在前面自动把用户的口语化请求改写成详细 prompt。结果上,DALL·E 3 在 T2I-CompBench 的颜色/形状/纹理绑定全 SOTA(如 Color 81.1% vs SDXL 61.9%),人评 prompt-following ELO **153.3**,远超 Midjourney 5.2(-104.8)与 SDXL(-189.5)。

## 背景与定位
2023 年前的 T2I 系统(含 [[dall-e-2]]、[[stable-diffusion-1]]/[[sdxl]]、[[imagen]])有一个共性顽疾:**prompt following 差**——会忽略词、混淆词义、搞错计数与空间关系,逼着用户去学 prompt engineering。论文(Betker, Goh, Jing et al., *Improving Image Generation with Better Captions*)给出的诊断是:**问题不在生成模型本身,而在训练集的图文配对质量太差**——网络 alt-text 往往只描述主体、忽略背景/数量/颜色/图中文字,甚至直接是广告或 meme,与图像内容不符。

DALL·E 3 的核心论点因此是:**用合成的、高度描述性的 caption 重标注训练集,就能可靠提升 prompt following**。这条路线区别于 [[imagen]] 走「换更强文本编码器(T5)」、[[parti]] 走「自回归扩规模」的思路;它把 [[dall-e-2]]/[[latent-diffusion-ldm]] 的扩散骨架基本沿用,而把杠杆压在 **数据 caption 工程**上。2024 年的「产品化」叙事则是另一条:把图像生成做成 **ChatGPT 的一个工具**,让 [[gpt-4]] 充当用户与 DALL·E 3 之间的「提示词改写器 + 头脑风暴搭档」,这也成为后续闭源 T2I 商用产品(以及自家 [[gpt-4o-native-image]])的标准范式。

> 注:论文与 system card 均署日期 2023-10(模型本体 2023 末发),本页按 worklist 归到 2024 年——对应其全面进入 ChatGPT 与 API 的产品化年份。

## 模型架构
论文明言:本文聚焦「重标注对 prompt following 的影响」,**不覆盖 DALL·E 3 模型完整的训练/实现细节**;架构信息主要来自附录 A/B。

- **生成骨架(image decoder)**:文本条件的 **三阶段 U-Net latent-diffusion 模型**(text-conditioned U-Net latent diffusion,[[latent-diffusion-ldm]] 路线),非 DiT。
- **VAE / latent 空间**:直接复用 [[latent-diffusion-ldm]](Rombach et al. 2022)的 **VAE**,做 **8× 下采样**;在「合成 caption 消融实验」里训 256px 图像 → latent 输入尺寸 **32×32**。
- **文本编码器**:**T5-XXL**(非 CLIP 文本塔)。文本先过 T5-XXL 得到 latent,再由生成网络通过 **cross-attention**(论文称 "xfnet")注入。
- **时间步条件**:**调制式 GroupNorm**(modulated GroupNorm)——按 timestep 信号学到一个 scale/bias 施加到 GroupNorm 输出。
- **专属 latent 解码器(DALL·E 3 latent decoder)**:在 VAE 的 latent 空间之上,OpenAI **自训了一个 diffusion decoder**(卷积 U-Net,结构同 [[ddpm]]/Ho et al. 2020),用来把 latent 解回像素。论文报告:相比 VAE 自带解码器,**diffusion decoder 显著改善精细细节**(尤其是图中文字与人脸)。该 diffusion decoder 通过 **consistency distillation**([[consistency-models]],Song et al. 2023)蒸馏到 **仅 2 步去噪**。注意:这个 latent decoder **只用于 DALL·E 3 正式版,不用于论文的合成-caption 消融实验**。
- **参数量 / 分辨率策略**:**未披露** 具体参数量。论文只说 DALL·E 3 是「上述消融模型的放大版,外加若干其它改进」,这些改进「因时间/算力原因未做消融」。生产环境支持的输出分辨率(按官方产品形态,1024×1024 及横/竖宽幅)在论文/system card 中**未给出数字**。
- **安全相关网络组件**(system card):输出端有一个 **bespoke racy 分类器**——**冻结的 CLIP 图像编码器**([[clip]])抽特征 + 一个小型辅助安全打分头。

## 数据
- **来源**:image-caption 对取自 **公开可得 + 授权(licensed)来源** 的组合(system card 原文)。规模、配比、具体数据集**未披露**。
- **核心:重标注(recaptioning)**——这是 DALL·E 3 的方法主轴:
  - 先训一个 **bespoke image captioner**:本质是一个以 CLIP 图像嵌入 F(i) 为条件的语言模型,按 CoCa(Yu et al. 2022a)方法**联合用 CLIP 目标 + 语言建模目标**预训练。
  - 两级微调,得到两种合成 caption:**SSC(short synthetic captions,只描述主体)** 与 **DSC(descriptive synthetic captions,长、描述主体+背景+图中文字+风格+配色等)**。
  - 把 captioner 应用到训练集**每张图**,生成合成 caption 替换原 alt-text。
- **合成 vs 真值的混合比(关键消融)**:
  - caption 类型对比:分别用 100% 真值 / 95% SSC / 95% DSC 训练,**两种合成 caption 都让 CLIP score 略升(真值评测)、明显升(DSC 评测)**;合成 caption 评测曲线方差更低——支持「重标注 ≈ 一种平均化操作」。
  - 混合比:试 65%/80%/90%/95% DSC 混真值;**65% 明显落后被中途砍掉**;结论是 **合成比例越高,CLIP score 越好**。
  - **DALL·E 3 正式版采用 95% 合成 + 5% 真值**。混入真值的作用是 **正则化**——纯合成会让模型过拟合 captioner 的模态特征(大小写、是否句号结尾、长度、总以 "a/an" 开头等),少量真值把输入分布拉回人类书写风格。
- **安全过滤**(system card):在 [[dall-e-2]] 过滤算法基础上扩展。**降低**了「性/暴力」宽泛过滤器的阈值,改用更细分的子类过滤器(露骨性化、仇恨图像)。这样做的副作用是好的:可**扩大训练集**,并**减少对女性生成的模型偏见**(因为被宽过滤器误删的性化图像里女性占比过高,过度删除会让模型「学不到」女性)。
- **racy 分类器的训练数据工程**(system card,少见的细节):初版用「文本 moderation API 标 prompt → 标图」噪声大;改用 **微软 Cognitive Service API** 打分清洗,人工抽检 1,024 张定阈值;再针对「图中只有一小块违规区域」的难例,**人工 cut-paste**——在 10 万非 racy + 10 万 racy 中,把 racy 区域(20% 面积)随机贴到非 racy 图上做正样本,并用「非 racy 贴非 racy」做负样本,逼分类器看局部内容而非整体 pattern。

## 训练方法
- **训练目标**:扩散(diffusion / 去噪),latent 空间,U-Net 骨架——非 flow matching、非 next-token、非 masked-token。
- **多阶段**:论文未给「预训练→continue→SFT→偏好对齐」式完整流程(明确说不覆盖训练细节)。可确认的两条 pipeline:
  1. **captioner 训练**:CLIP+LM 联合预训练 → 两级微调(SSC、DSC)。
  2. **生成模型训练**:在 95%/5% 合成-真值混合 caption 上训扩散模型;消融模型「全部训到 **500,000 步、batch 2048**,合计 **10 亿张训练图**」。
- **加速 / 蒸馏**:latent 解码器用 **consistency distillation 蒸到 2 步**(见架构)。生成主干本身的步数蒸馏**未披露**。
- **推理期的「提示词上采样」(inference-time trick,极关键)**:因为模型训练分布是长 DSC,在长描述 prompt 上采样效果最好。OpenAI 用 **GPT-4**(见附录 C 的 prompt 模板)把任意短 caption **"upsample" 成 15–80 词的详细描述**再喂给 DALL·E 3。这就是 **ChatGPT 集成的技术内核**:GPT-4 既是 prompt 改写器,也顺手承担安全改写(去公众人物名、把人「grounding」加属性、把品牌物泛化)。

## Infra(训练 / 推理工程)
- **算力 / 并行 / GPU·时 / 吞吐**:论文与 system card 均**未披露**(无 GPU 数、无训练时长、无并行策略、无混合精度细节)。仅消融实验给了 batch 2048 / 500k step / 1B 图的口径,正式版规模未公开。
- **训练基础设施伙伴**:system card 致谢明确——**微软 Azure 支持模型训练的基础设施设计与管理**;Microsoft Bing 与微软安全团队参与安全部署。
- **推理 / 部署形态**:作为 **ChatGPT 内的图像生成组件**(GPT-4 在前做 NL 交互 + prompt 合成)与 **API** 两种形态。latent 解码器蒸到 2 步以降推理成本。系统级还串了多道在线安全组件(prompt 输入分类器/Moderation API、blocklist、prompt 改写、输出图像分类器、分类器引导重采样),都在推理路径上。
- **classifier guidance 安全重采样**(infra-level trick):当输出分类器判定图偏 racy,**带 special flag 重新提交 prompt**,触发扩散采样用 racy 分类器做 [[classifier-guidance]](Dhariwal & Nichol)**反向「推离」**违规区域——把意外 racy 率压到 **0.7%**。

## 评测 benchmark(把效果讲清楚)
数字均来自已抓取的论文 PDF(Table 1/2)与 system card,**未报告项如实标注**。

**自动评测 — prompt following(论文 Table 1,DALL·E 3 vs [[dall-e-2]] 生产版 vs [[sdxl]] v1.0+refiner)**:

| 指标 | DALL·E 3 | DALL·E 2 | SDXL 1.0 |
| --- | --- | --- | --- |
| MSCOCO CLIP Score ↑ | **32.0** | 31.4 | 30.5 |
| Drawbench short (GPT-V) ↑ | **70.4%** | 49.0% | 46.9% |
| Drawbench long (GPT-V) ↑ | **81.0%** | 52.4% | 51.1% |
| T2I-CompBench 颜色绑定 ↑ | **81.1%** | 59.2% | 61.9% |
| T2I-CompBench 形状绑定 ↑ | **67.5%** | 54.7% | 61.9% |
| T2I-CompBench 纹理绑定 ↑ | **80.7%** | 63.7% | 55.2% |

- DALL·E 3 在以上**全部指标 SOTA**;Drawbench 用「GPT-V(论文对基于 GPT-4 的视觉感知 LLM 的称呼)判对错」的自动评测,且用 GPT-4 把 prompt upsample 后差距进一步拉大(论文 §4.1.2)。
- CLIP score 用公开 ViT-B/32,MSCOCO 2014 取 4,096 条 caption;论文坦白**未对 MSCOCO 去重,可能有数据泄漏**。

**人评 — ELO(论文 Table 2,DALL·E 3 Eval 170 条 prompt + MSCOCO 250 条,每对 3 评分,共 2040 评分/模型/问题)**:

| 维度 | DALL·E 3 | Midjourney 5.2 | SDXL | DALL·E 2 |
| --- | --- | --- | --- | --- |
| Prompt following (ELO) | **153.3** | -104.8 | -189.5 | — |
| Style (ELO) | **74.0** | 30.9 | -95.7 | — |
| Coherence/MSCOCO (ELO) | **71.0** | 48.9 | -84.2 | — |
| Drawbench (ELO) | **61.7** | — | -34.0 | -79.3 |

- DALL·E 3 在三个维度**全部最高**,**prompt following 优势最大**。

**关键消融结论**:① 合成 caption(SSC/DSC)无论用哪种评测都 ≥ 真值,**用合成 caption 训练没有 downside**;② 合成比例越高 CLIP score 越好;③ 推理时用 GPT-4 upsample prompt 能修正模型本会出错的复杂关系。

**安全侧量化结论**(system card):racy 输出分类器在 alpha 集 AUC 由 63.7→85.1(cut-paste+清洗),hard64 真阳率 1.6→78.1;意外 racy 率降到 **0.7%**;公众人物:DALL·E 3-early 合成-prompt 评测 **2.5%** 含公众人物 → DALL·E 3-launch **0%**;500 条对抗 prompt 中 launch 版 0.7% 出公众人物,33.8% 被 ChatGPT 拒、29.0% 被图像端拒。

**未报告**:FID、GenEval、DPG-Bench、MJHQ-30K、HPSv2、ImageReward、PickScore、GEdit/MagicBrush(DALL·E 3 非编辑模型)等均**未在一手源出现**;论文仅用 CLIP-S / Drawbench / T2I-CompBench / ELO 四类评测。

## 创新点与影响
**核心贡献**
1. **「重标注训练集」范式**:用自训 captioner 把数据全量重写成高描述性合成 caption,以 95%/5% 混合训练——把 prompt following 从「换更强 text encoder / 扩规模」之外开辟出一条「数据 caption 工程」的路,且给出可复现的消融与评测基线(开源了评测样本与 prompt:openai/dalle3-eval-samples)。
2. **「LLM 提示词上采样 / 改写」作为产品内核**:GPT-4 在前把口语化请求改写为详细 prompt,既补全细节、消歧复杂关系,又顺手做安全改写——奠定了 **ChatGPT 内置图像生成** 的交互范式。
3. **多层系统级安全栈**:模型层数据过滤 + ChatGPT 拒答 + Moderation/输入分类器 + blocklist + prompt 改写(去公众人物/grounding/泛化品牌)+ 输出图像分类器 + classifier-guidance 重采样,并给出 racy 分类器训练数据工程(Cognitive Service 清洗 + cut-paste 难例)的罕见细节。

**影响**:DALL·E 3 把「合成 caption 重标注」推成行业标配——此后 [[pixart-alpha]]、[[stable-diffusion-3]]、[[flux-1]] 等都重度依赖 recaptioning;「LLM 改 prompt」也成闭源 T2I 商用标杆做法,直至自家 [[gpt-4o-native-image]] 把生成内化进多模态模型。

**已知局限**(论文 §5):① **空间/方位**(左/下/后)仍不可靠——因 captioner 本身不擅描述方位;② **图中文字渲染** 不稳(缺字/多字),怀疑与 T5 文本编码器「看到的是整词 token、需自行映射到字母」有关,提出未来可探索字符级语言模型条件;③ **specificity 幻觉**——captioner 会对植物/鸟类等臆造属种,导致模型对特定术语生成不可靠;④ system card 记录的偏见(默认偏白人/年轻/女性、西方视角)、prompt 过度 grounding 等。

## 原始链接
- blog: https://openai.com/index/dall-e-3/
- paper (PDF, "Improving Image Generation with Better Captions"): https://cdn.openai.com/papers/dall-e-3.pdf
- system card (PDF): https://cdn.openai.com/papers/DALL_E_3_System_Card.pdf
- eval samples (GitHub): https://github.com/openai/dalle3-eval-samples

## 一手源存档（sources/）
- [dalle-3--blog.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/dalle-3--blog.md)
- [dalle-3-paper--text.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/dalle-3-paper--text.md)
- ../../../sources/omni/2024/dalle-3-paper-improving-image-generation.pdf (gitignored)
- [dalle-3-system-card--text.md](https://github.com/zhao9797/ai-research/blob/main/sources/omni/2024/dalle-3-system-card--text.md)
- ../../../sources/omni/2024/dalle-3-system-card.pdf (gitignored)
