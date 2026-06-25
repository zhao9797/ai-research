---
title: "DALL·E 3"
org: OpenAI
country: US
date: "2023-10"
type: blog
category: t2i
tags: [t2i, diffusion, latent-diffusion, recaptioning, synthetic-caption, prompt-following, chatgpt, t5]
url: "https://openai.com/index/dall-e-3/"
arxiv: ""
pdf_url: "https://cdn.openai.com/papers/dall-e-3.pdf"
github_url: "https://github.com/openai/dalle3-eval-samples"
hf_url: ""
modelscope_url: ""
project_url: "https://openai.com/index/dall-e-3/"
downloaded: [dall-e-3.pdf, dall-e-3--blog.md, dall-e-3--system-card.pdf]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
DALL·E 3 是 OpenAI 第三代文生图系统，核心创新不在模型结构而在**数据**：用一个定制图像 captioner 把训练集**全量重写成高描述性合成 caption**（95% 合成 + 5% 原始 alt-text 混训），再深度集成 ChatGPT/GPT-4 在推理时把用户短 prompt"上采样"成长描述，从而把长 prompt 遵循度、组合性与文字渲染拉到当时 SOTA——人评 prompt-following ELO 153.3，远超 Midjourney 5.2（-104.8）与 SDXL（-189.5）。

## 背景与定位
彼时文生图模型（[[dall-e-2]]、[[stable-diffusion]]、[[sdxl]]、Imagen、Parti）的通病是 **prompt following 差**：忽略词序、漏掉物体、混淆关系、数不清个数、画不对文字。前人给的药方各不相同——Imagen 靠更强的预训练语言模型（T5）做条件、并提出 DrawBench；Parti 靠把自回归生成器 scaling 上去；Rassin 等指出 DALL·E 2 存在"一词多义不约束"的缺陷。

DALL·E 3 论文（标题 *Improving Image Generation with Better Captions*，James Betker、Gabriel Goh、Li Jing、Aditya Ramesh 等）提出一条正交路线：**问题出在训练数据的图文对质量**。互联网 alt-text 往往只描述主体、漏掉背景/数量/位置/颜色/图中文字，甚至直接错误（广告、meme 混进 alt-text）。既然 caption 噪声大，那就**用模型重新生成准确而详尽的 caption** 来训练，把"averaging operation"般的噪声抹平。这是把"合成数据训练"（Parti 也提过）做成系统化方法并量化其收益的工作。

需要强调：论文**只覆盖 recaptioning 这一条贡献**，明确声明"不涵盖 DALL·E 3 模型本身的训练或实现细节"（脚注 5：DALL·E 3 相对 DALL·E 2 还有许多未披露、未消融的改进）。模型结构细节只在附录给了 ablation 用的 decoder。相关脉络见 [[latent-diffusion-ldm]] [[ddpm]] [[clip]]。

## 模型架构
论文正文聚焦数据，结构信息主要来自附录 A/B 与系统卡，**且部分是消融实验所用模型而非生产版 DALL·E 3**，需谨慎区分：

- **整体范式**：latent diffusion（潜空间扩散），不是自回归。这与初代 DALL·E（自回归 token）和 DALL·E 2（unCLIP，CLIP latent + diffusion prior + decoder）都不同。
- **VAE / 潜空间**：沿用 Rombach 等（LDM/Stable Diffusion）的 **VAE，8× 下采样**。消融实验在 256px 图上训练，潜空间为 32×32 latent。
- **image decoder（附录 A，消融用）**：文本条件的 **U-Net latent diffusion，三阶段**；时间步条件用 **modulated GroupNorm**（学习到的、依赖 timestep 的 scale/bias 作用于 GroupNorm 输出）；文本条件先过 **T5-XXL** text encoder，再由 "xfnet" 做 cross-attention 注入。
- **DALL·E 3 latent decoder（附录 B，生产相关）**：在上述 VAE 潜空间之上**额外训练了一个自家的 diffusion decoder**（卷积 U-Net，结构同 Ho 2020 DDPM），用来显著改善细节（文字、人脸）；并用 **consistency distillation（Song 2023）蒸馏到 2 步去噪**。这个改进版 latent decoder **不用于** 论文里的合成 caption 消融。
- **text encoder = T5（不是 CLIP text encoder）**：论文在 limitations 里把文字渲染不稳定归因于 T5——"模型看到的是整词 token，要映射成图中字母，故缺字漏字"，并设想未来引入字符级语言模型。
- **生产版完整结构（参数量、分辨率金字塔、具体 U-Net/DiT 选择）OpenAI 未披露**。

## 数据
DALL·E 3 的命脉就是数据，这部分披露最充分（合数据方法来自论文，规模/来源/过滤来自系统卡）：

- **来源**：系统卡明确——图文对来自"**公开可得 + 已授权（licensed）来源的组合**"。具体数据集名称、总量未公开。
- **核心方法：dataset recaptioning（重写 caption）**
  1. 先训一个 **bespoke 图像 captioner**：本质是条件语言模型，按 Yu 2022a（CoCa）做法，用 **CLIP 图像 embedding F(i)** 作为条件，联合 CLIP + 语言建模目标在自有 (t,i) 图文对上预训练。原始 captioner 仍有"不爱写细节"的毛病。
  2. **两轮 fine-tune 出两种合成 caption**：
     - **SSC（short synthetic caption）**：在"只描述主体"的小数据集上 continue-train，偏向描述主体。
     - **DSC（descriptive synthetic caption）**：再在"长、极详尽"的数据集上 fine-tune，描述主体 + 背景 + 图中文字 + 风格 + 配色等。
  3. 用 captioner 给**训练集每一张图重新打 caption**，得到全量合成 caption。
- **混合比例（关键 trick）**：直接 100% 合成会让模型过拟合 captioner 的模态偏好（大小写、标点、是否总以"a/an"开头、句长等），导致推理分布偏移。解决办法是**采样时按固定概率混入原始 ground-truth caption**做正则化。消融显示合成比例越高 CLIP score 越好（测了 65/80/90/95%，65% 明显落后被砍），最终 **DALL·E 3 用 95% 合成 + 5% ground-truth**。
- **安全/偏见过滤（系统卡）**：在 DALL·E 2 过滤算法基础上扩展，过滤露骨色情、暴力、仇恨符号。一个反直觉改动：**调低了笼统过滤器的阈值**，改用针对细分子类（露骨性化、仇恨图像）的更精确过滤器——因为笼统过滤器把大量女性图像误删，反而加重了模型对女性生成的偏置；放宽后既扩大了可用数据集又减轻了偏置。
- captioner 已知缺陷会传导到生成模型：合成 caption 会**幻觉细节**（如给植物画乱编属种、给鸟乱编物种），且 captioner 报不准空间位置 → 下游 DALL·E 3 在"具体物种""左右上下"这类指令上不可靠。

## 训练方法
- **生成目标**：扩散（denoising diffusion，latent space）。论文消融用的 T5-conditioned image diffusion，全部训到 **500,000 步、batch size 2048**，即累计 **10 亿张训练图像**。生产版 DALL·E 3 称为"上述消融模型的放大版 + 若干其它改进"，但放大倍数/总步数/总图量**未披露**。
- **多阶段 / 对齐**：论文**未提** SFT、RLHF、DPO、reward model 等后训练对齐——DALL·E 3 这一代的"对齐"主要发生在**数据层（recaptioning）+ 系统层（ChatGPT prompt 改写、分类器引导、blocklist）**，而非用偏好优化训练图像模型本身。
- **推理期 prompt"上采样"**：训练用 95% 长合成 caption → 模型只在"长详尽 caption 分布"内表现最好，故推理也必须喂长 caption。OpenAI 用 **GPT-4 把用户短 prompt 改写成 15–80 词的详尽描述**（附录 C 给了完整 system prompt 与 few-shot 示例），并指出 LLM 不仅补细节，还能**消歧复杂关系**，让小图像模型本来会画错的也能画对。这是 DALL·E 3 "原生构建于 ChatGPT 之上"的技术内核。
- **加速 / 蒸馏**：生产版 latent decoder 用 **consistency distillation 蒸到 2 步**去噪（附录 B），大幅降低解码成本。
- **安全侧训练 trick（系统卡）**：racy 输出分类器用"frozen CLIP image encoder + 小辅助头"，数据清洗用 Microsoft Cognitive Service API 打分排序 + 1024 张人工校准阈值，并引入 "cut-paste 数据"显著提升对小面积冒犯区域（hard64 基准）的召回；还部署 **classifier-guidance** ——检测到 racy 输出时给 prompt 打特殊 flag 重采样，让扩散过程"采样远离"触发分类器的图，使对抗 prompt 的非预期 racy 率从早期降到 **0.7%**。

## Infra（训练 / 推理工程）
- **算力/集群**：系统卡致谢 **Microsoft Azure** 支持模型训练的基础设施设计与管理（系统卡原文：感谢 Microsoft 合作、Azure 支持模型训练的基础设施设计与管理，Bing 团队与安全团队参与安全部署）；blog 把"推断优化（inference optimization）"单列一组贡献者（Connor Holmes、Arash Bakhtiari、Umesh Chand、Zhewei Yao、Samyam Rajbhandari、Yuxiong He——其中数人为 DeepSpeed 团队成员），但 blog/系统卡均未点名所用推理框架。GPU 数量、GPU·时、并行/分布式策略、混合精度、吞吐**均未披露**。
- **推理加速**：latent decoder 经 consistency distillation **降到 2 步去噪**是已披露的关键加速点；具体采样步数、缓存、量化等未公开。
- **部署形态**：作为 ChatGPT 的图像生成组件上线，并通过 **OpenAI API** 开放；GPT-4 在前端用自然语言与用户交互、再合成发给 DALL·E 3 的 prompt。生成图像配套有**输入 prompt 分类器（Moderation API）+ 输出图像分类器 + blocklist + ChatGPT 拒绝**多层缓解。

## 评测 benchmark（把效果讲清楚）
评测全部围绕 **prompt following**（论文核心命题），数字来自论文 Table 1/2 与图 4/5：

**caption 类型消融（图 4，CLIP score ViT-B/32）**：在 ground-truth caption 上评测时，合成 caption 训练略好于 baseline；在 DSC 上评测时**显著更好**。合成 caption 评测曲线**方差明显更低**（支持"recaptioning ≈ averaging"假说），净 CLIP score 也更高（图文绑定更强）。结论：用合成 caption 训练**没有任何下行风险**。

**混合比例消融（图 5）**：DSC 合成比例越高，CLIP score 单调越好 → 取 95%。

**DALL·E 3 vs DALL·E 2 vs SDXL（Table 1，自动评测）**：

| 指标 | DALL·E 3 | DALL·E 2 | SDXL 1.0(+refiner) |
|---|---|---|---|
| MSCOCO CLIP Score ↑ | **32.0** | 31.4 | 30.5 |
| Drawbench short(GPT-V) ↑ | **70.4%** | 49.0% | 46.9% |
| Drawbench long(GPT-V) ↑ | **81.0%** | 52.4% | 51.1% |
| T2I-CompBench Colors ↑ | **81.1%** | 59.2% | 61.9% |
| T2I-CompBench Shape ↑ | **67.5%** | 54.7% | 61.9% |
| T2I-CompBench Texture ↑ | **80.7%** | 63.7% | 55.2% |

DALL·E 3 在**全部**自动指标上 SOTA。Drawbench 评测用 **GPT-V（vision-aware GPT-4）做裁判**（附录 D 给了完整裁判 prompt），并对所有模型都用 GPT-4"上采样"caption 后再生成——**用上采样 caption 后 DALL·E 3 领先幅度进一步拉大**。MSCOCO 用 4096 条 caption、短 ground-truth caption 推理；论文坦承未对 MSCOCO 去重，可能有数据泄漏。

**人评 ELO（Table 2，每模型每问题 2040 个评分）**：

| 维度 | DALL·E 3 | Midjourney 5.2 | SDXL+refiner | DALL·E 2 |
|---|---|---|---|---|
| Prompt following | **153.3** | -104.8 | -189.5 | — |
| Style | **74.0** | 30.9 | -95.7 | — |
| Coherence(MSCOCO) | **71.0** | 48.9 | -84.2 | — |
| Drawbench | **61.7** | — | -34.0 | -79.3 |

三个维度（prompt following / style / coherence）DALL·E 3 均**大幅胜出**，prompt following 优势尤其悬殊。评测设计细节：prompt-following 用 170 条"DALL·E 3 Eval"贴近真实用法的 caption（含人物、产品、地点、概念混合、文字渲染、艺术）；coherence 怕评审歧视想象场景，特意从 MSCOCO 采 250 条"可信存在"的 caption；style/coherence 评测**不给评审看 caption**以免混入 prompt-following 判断。

**关键消融结论**：合成 caption 比例越高越好、且无副作用；推理期 LLM 上采样 caption 能进一步消歧复杂关系、纠正本会画错的图。GPT-V 在"数物体个数"类任务上裁判能力不超过随机，故计数任务改用人评补充。

## 创新点与影响
**核心贡献**：
1. **dataset recaptioning 范式**——证明"重写训练 caption 为高描述性合成文本"能可靠、无副作用地提升 prompt following，把数据质量而非模型结构作为 prompt-following 的主要抓手。这是后续一大批工作（PixArt-α、SD3、各类开源模型、视频生成）做合成 caption / re-caption 的直接先声。
2. **训练分布 ↔ 推理分布对齐**——用 LLM 在推理期上采样 prompt，弥合"训练用长 caption / 用户输入短 prompt"的鸿沟，开创"LLM as prompt rewriter"的产品形态（ChatGPT 原生集成）。
3. **可复现评测基线**——公开评测样本、prompt 与 GPT-V 裁判 prompt（GitHub `openai/dalle3-eval-samples`），把 prompt-following 评测标准化。

**影响**：让"图文对齐/长指令遵循/图中文字"成为文生图竞赛的主战场；"合成 caption + 比例混合"几乎成为之后开源/闭源 T2I 的标配配方；ChatGPT × 图像生成的产品范式被广泛模仿。

**已知局限（论文 §5 + 系统卡）**：
- **空间关系**不可靠（"左边/下面/后面"），根因是合成 captioner 自身报不准位置。
- **文字渲染**不稳定（缺字多字），归因于 T5 整词 token，设想用字符级 LM 改进。
- **specificity 幻觉**：captioner 乱编植物属种/鸟类物种 → 模型对特定术语生成不可靠。
- **偏见**：默认倾向生成白人/年轻/女性、西方视角；靠 ChatGPT 改写 prompt 加"groundedness"缓解，但有 over-grounding（给场景硬加人、给非人物体加人特征）副作用。
- 拒绝在世艺术家风格请求、拒绝点名公众人物；提供创作者退出训练集（opt-out）机制；探索 provenance 分类器检测图像是否由 DALL·E 3 生成。

## 原始链接
- blog（产品页/官方公告）: https://openai.com/index/dall-e-3/
- paper（技术报告 PDF，*Improving Image Generation with Better Captions*）: https://cdn.openai.com/papers/dall-e-3.pdf
- system card（DALL·E 3 System Card，2023-10-03）: https://cdn.openai.com/papers/DALL_E_3_System_Card.pdf
- eval samples / 代码: https://github.com/openai/dalle3-eval-samples

## 本地落盘文件
- ../../../sources/omni/2023/dall-e-3.pdf
- ../../../sources/omni/2023/dall-e-3--blog.md
- ../../../sources/omni/2023/dall-e-3--system-card.pdf
