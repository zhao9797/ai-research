---
title: "UniWorld-V1: High-Resolution Semantic Encoders for Unified Visual Understanding and Generation"
org: "Peking University (PKU-YuanGroup) / Peng Cheng Lab / Rabbitpre AI"
country: China
date: "2025-06"
type: paper
category: unified
tags: [unified, edit, perception, siglip, flux, qwen2.5-vl, flow-matching, open-source]
url: "https://arxiv.org/abs/2506.03147"
arxiv: "https://arxiv.org/abs/2506.03147"
pdf_url: "https://arxiv.org/pdf/2506.03147"
github_url: "https://github.com/PKU-YuanGroup/UniWorld-V1"
hf_url: "https://huggingface.co/LanguageBind/UniWorld-V1"
modelscope_url: ""
project_url: ""
downloaded: [arxiv-2506.03147.pdf, uniworld-v1--readme.md, uniworld-v1--hf-modelcard.md, uniworld-v1--hf-dataset.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
UniWorld-V1 是北大 PKU-YuanGroup 推出的开源统一视觉模型：用**高分辨率对比语义编码器（SigLIP2）替代 VAE** 作为参考图控制信号，把"理解 + 文生图 + 图像编辑 + 图像感知"统进一个框架；仅用 **2.7M 训练样本**就在 ImgEdit-Bench 编辑总分 **3.26** 超过 BAGEL（2665M 数据，3.20）与 Step1X-Edit（3.06），GenEval 加 rewriter 达 **0.84**（逼近 BAGEL 0.88），是首个把感知（检测/分割/深度/canny 等）也纳入统一生成范式的开源模型。

## 背景与定位
现有统一模型（[[janus-pro]]、[[bagel]]、Emu3、MetaQuery 等）在"图→文理解"和"文→图生成"上很强，但普遍**做不了图→图的感知（detection/segmentation/depth）与操作（编辑/风格/换装）**。GPT-4o-Image 把这两类能力一并打通，引爆社区复刻。复刻的关键卡点在于"参考图的视觉特征怎么注入 DiT"：Step1X-Edit、[[flux-1-kontext]] 用 **VAE** 抽参考图特征，对单一编辑任务有效，但 VAE 编码携带大量低频信息，扩展到多感知/多操作任务时**无法收敛**。

作者做了一组"逆向 GPT-4o-Image"的对照实验（论文 Section 2）反推其特征注入方式：
- **编辑实验**："把公交车背面广告涂蓝"后，图中文字位置发生位移——若用强保低频的 VAE 特征，文字位置应几乎不变，故推断它不是 VAE。
- **去噪实验**：把狗图加 0.6× 噪声后让 GPT-4o-Image 去噪，结果被错误重建成"鹿"；同时 GPT-4o / Qwen2.5-VL 也把 0.6× 噪声狗图描述成鹿。说明其生成依赖**强多模态理解先验**，而非保结构的 VAE 低频特征。

结论：GPT-4o-Image **更可能用语义编码器而非 VAE** 抽参考图特征。UniWorld-V1 即据此设计——用语义编码器（SigLIP2）+ MLLM（Qwen2.5-VL）语义 token 双路注入。相关脉络见 [[latent-diffusion-ldm]] [[flux-1]] [[siglip]]。

## 模型架构
四大件：**VLM（理解）+ SigLIP（低层参考控制）+ DiT（生成）+ MLP connector**（论文 Figure 3）。

- **Backbone（生成）**：DiT，直接复用 **FLUX.1-dev** 的 MMDiT。生成走 **flow matching**。
- **理解/语义 token**：冻结的 **Qwen2.5-VL-7B** 自回归出理解 token，提供高层语义与历史状态。参考图同时过 Qwen2.5-VL-7B 和 SigLIP，两路输出拼接后送入 FLUX 的 **text branch**。
- **低层参考控制（核心创新）**：用 **SigLIP2-so400m/14、固定分辨率 512** 的对比语义编码器替代 VAE。作者的观察是：分辨率升高时，对比编码器的全局特征趋于饱和，模型容量转而保留细节，恰好有利于维持非编辑区的保真度——这正是 VAE 之外另一条可行的"参考一致性"控制路径。
- **条件注入**：FLUX 原本用的 **T5** 文本条件在 UniWorld 中是**可选**的；训练早期引入 T5 反而易陷入劣质局部最优，故早期不建议用 T5。
- **VLM 编码无 learnable token**：HF model card 强调利用 VLM 的因果注意力，参考图特征以 `<instruction><image>` 顺序排布尤为关键——指令在前、图像在后，使 VLM 在解读指令的同时保留图像先验，无需额外可学习 query token。
- **失败尝试（消融）**：尝试用 **DINOv2、RADIOv2.5** 替换 SigLIP 均失败；尝试直接拿 Qwen2.5-VL 视觉输出（取 image feature 弃 text feature）当参考控制信号，参考一致性很差——因对比学习的全局特征随分辨率饱和、VLM 又要兼顾全局+局部，导致保留的低层控制信号不足。

参数量层面：理解侧 Qwen2.5-VL-7B（冻结），生成侧基于 FLUX.1-dev（约 12B DiT）。**论文未给出统一框架的总可训练参数精确数字**；ZeRO 一节以"20B 模型"举例说明 EMA 分片显存，提示整体规模在 ~20B 量级（未明确确认）。分辨率策略：参考图与 SigLIP 固定 **512×512**，目标生成 1024×1024——这也是其参考一致性与文字编辑的主要瓶颈（512 SigLIP 看不清细节）。

## 数据
总量约 **2.7M**（vs BAGEL 2665M），分三大类（论文 Section 3.4 + HF dataset/model card）：

- **图像感知 ~1.4M**：canny / mlsd / hed / depth / sketch / normal / segmentation(mask) / detection(bbox)。主要来自 **Graph200k、COCO2017**。感知图多为 1024×1024，但 >90% 参考图仅 512×512；因感知图与参考图差异大，**无需 mask 加权策略**。HF dataset card 列出具体子集：coco2017_caption_{canny/depth/hed/mlsd/normal/sketch}-各236k、coco2017_seg_box-448k、openpose-62k、unsplash_canny-20k、open_pose-40k 等。
- **图像操作 ~1M**：add/remove/replace 等常见编辑。主源 **ImgEdit**（>1M，用 GPT-4o 过滤取高分子集 **724k**，短边 ≥1024px）与 **SEED-X**（选 part3，分辨率 ≥1024×1024）。另含 Graph200k 风格迁移、虚拟试穿、商品抠图（viton_hd-23k、deepfashion-27k、shop_product-23k、OmniEdit-368k、Ghibli-36k 风格数据等）。多数开源数据无编辑 mask，故按 §3.5 自动生成。
- **文生图 ~300k**：来自 **BLIP3-o（BLIP3o-60k）** 与 **Open-Sora Plan 内部图**（OSP1024-286k）。Open-Sora Plan 图用 **Qwen2-VL-72B** 重新打 dense caption，分辨率 ≥1024×1024、**美学分 ≥6.0**。

**自动 mask 生成 + 自适应编辑区域加权（§3.5，重要 trick）**：编辑区往往只占全图一小块，若全图均匀加权，编辑区的 loss 会被未编辑大背景淹没导致欠拟合。流水线：(1) 参考图与目标图**逐像素差分**（设容差阈值）→ (2) **膨胀**去噪 → (3) **连通域过滤**去碎片 → (4) **max-pooling 下采样**去内部气泡，得到编辑面积 A_edit。再以 x = A_total / A_edit 设计加权函数 w(x)，约束 w(1)=1（整图编辑/文生图/风格迁移退化为均匀加权）。对比四种函数（线性、指数根、对数、二次根），最终采用**对数函数 w(x)=log₂(x)+1**——增长温和、对极小区域不失稳、敏感性与鲁棒性平衡最佳。

## 训练方法
**两阶段训练**（论文 §3.2），两阶段用几乎相同的数据：

- **Stage 1 — 语义对齐预训练**：因 VLM 表征与 FLUX text branch 存在特征 gap，本阶段专注把 VLM 特征对齐到 T5 特征空间。**仅 VLM→FLUX 的 MLP 可训练，其余全冻结**；此阶段**不引入 SigLIP 特征**。完成后模型已能文生图、并能按编辑指令生成与参考图不同的图。
- **Stage 2 — 一致性生成微调**：载入 stage 1 的 VLM→FLUX MLP，以及 **FLUX-Redux** 的 MLP 权重（把 SigLIP 特征对齐到 text branch；该权重源自 ostris/Flex.1-alpha-Redux 重整理）。**解冻 FLUX image branch 全部可学习参数，冻结 text branch**。早期模型会"抄近路"直接重建参考图；约 **5,000–10,000 步**后才开始真正学会**用 SigLIP 特征作参考线索**、按指令生成。

- **生成目标**：flow matching（沿用 FLUX 的 rectified-flow 范式）。理解侧自回归、冻结不训练（继承 Qwen2.5-VL-7B 能力，省算力且避免生成任务损伤理解性能）。
- **EMA**：FP32 存储以保数值精度，每步更新。
- **蒸馏/步数加速**：**论文未报告**（无 consistency/LCM/ADD 等）。
- **偏好对齐（RLHF/DPO）**：V1 **无**。（注：后续 UniWorld-V2 才引入基于 DiffusionNFT + MLLM training-free reward 的 RL，属另一工作。）
- **关键超参（LR/batch size/总步数/epoch）**：**论文与 model card 均未披露**。

## Infra（训练 / 推理工程）
- **唯一明确披露的工程设计是 ZeRO-3 EMA**（论文 §3.3，Figure 4）：训练模型（DiT）跑 **ZeRO-2**，而 **EMA 模型用 ZeRO-3 跨 GPU 分片**。EMA 需额外存一份 FP32 副本，对超大模型会挤占显存、限制 batch；ZeRO-3 分片后每 GPU 仅持 20×4/N GiB（以 20B 模型、N 卡为例），每步只更新自己那片，计算量降到 1/N，随卡数增加成本几乎不增。该方案也支持训练模型本身跑 ZeRO-3 以进一步降显存、增大有效 batch。
- **算力规模（GPU 型号/卡数/GPU·时）**：**论文未披露**。
- **并行/混合精度/吞吐**：除 ZeRO-2/ZeRO-3 与 EMA FP32 外**未披露**。
- **推理部署**：开源 Gradio Web UI 与 CLI（`univa.serve.gradio_web_server` / `univa.serve.cli`），需分别指定 model / FLUX / SigLIP 路径；ComfyUI"coming soon"。推理步数、量化、缓存等加速**未报告**。

## 评测 benchmark（把效果讲清楚）
数字均来自论文表 1–6（已落盘 PDF）。

**GenEval（文生图，表 2）** Overall：UniWorld-V1 **0.80**（注：论文 §4.2 正文写 0.79、表 2 写 0.80，存在内部不一致，此处取表值），加 LLM rewriter（用 BLIP3-o 的 rewrite prompt）**0.84**。对照：BAGEL 0.82 / BAGEL† 0.88、GPT-4o-Image‡ 0.84、BLIP3-o 0.84、MetaQuery-XL† 0.80、Janus-Pro-7B 0.80、FLUX.1-dev† 0.82。分项（UniWorld-V1†，即带 rewriter 行）：Single 0.98 / Two 0.93 / Counting 0.81 / Colors 0.89 / Position 0.74 / Color-Attr 0.71（无 rewriter 行分项为 0.99/0.93/0.79/0.89/0.49/0.70）。卖点是**数据效率**：2.7M 对 BAGEL 的 2665M，0.84 vs 0.88 几乎追平。

**WISE（世界知识文生图，表 3）** Overall **0.55**（与 BAGEL 0.52、MetaQuery-XL 0.55 同档，远高于 Janus 0.23 / Show-o 0.35 / Emu3 0.39；GPT-4o-Image† 0.80 仍领先）。分项：Cultural 0.53 / Time 0.55 / **Space 0.73**（除 GPT-4o-Image 0.89 外全场最高）/ Biology 0.45 / Physics 0.59 / Chemistry 0.41。

**ImgEdit-Bench（图像编辑，表 4，GPT-4.1 评分）** Overall **3.26**，**开源第一**，超 BAGEL 3.20、Step1X-Edit 3.06、UltraEdit 2.70、AnyEdit 2.45（GPT-4o-Image 4.20 领先）。开源第一的分项：Adjust **3.64**、Extract **2.27**、Replace **3.47**、Remove **3.24**、Background **2.99**、Hybrid **2.96**；其余 Add 3.82、Style 4.21、Action 2.74。

**GEdit-Bench（域外泛化，English，表 5，GPT-4.1 评分）** G_SC（指令遵循）**4.93** 偏低、G_PQ（感知质量）**7.43** 较高、G_O **4.85**。对照 Step1X-Edit (7.09/6.76/6.70)、BAGEL (7.36/6.83/6.52)、GPT-4o (7.85/7.62/7.53)。G_SC 低的原因作者明确解释：编辑数据多来自 ImgEdit、指令多样性不足；且**数据里没有文字编辑样本**，而 GEdit 重视文字编辑、512 分辨率 SigLIP 也难做文字编辑。

**视觉理解（表 6）** 因冻结 Qwen2.5-VL-7B，理解力**无损继承**：MMBI 83.5 / MMMU 58.6 / MM-Vet 67.1，显著超 Janus/Show-o/Emu3，与 BAGEL(85.0/55.3/67.2)、MetaQuery、BLIP3-o 同档。

**图像感知（§4.5）** 因尚无统一感知 benchmark，仅与 GPT-4o-Image **定性对比**（Figure 6）：作者称在 canny、normal map、HED、segmentation、sketch 上指令理解与执行**优于 GPT-4o-Image**——**无定量分数，属定性结论**。

**消融结论**：(a) 加权函数对比选定对数 w(x)=log₂(x)+1；(b) SigLIP 不可替换（DINOv2/RADIOv2.5 失败）；(c) 直接用 Qwen2.5-VL 视觉特征作参考控制失败，验证"需要专门的高分辨率对比编码器保留低层控制信号"。

## 创新点与影响
**核心贡献**：
1. **反 VAE 的洞察**：通过对 GPT-4o-Image 的对照实验，论证统一编辑/感知模型应**用高分辨率对比语义编码器（SigLIP2）而非 VAE** 提供参考图控制信号——VAE 低频信息过强、扩展到多任务不收敛。
2. **首个把感知 + 操作 + 理解 + 生成四合一的开源统一模型**，且**极致数据效率**（2.7M 即追平/超越百倍数据量的 BAGEL）。
3. **自适应编辑区域加权 + 自动 mask 生成**这一可复用的编辑训练 trick。
4. **ZeRO-3 EMA** 这一大模型 EMA 显存优化工程方案。
5. **全栈开源**：模型权重、数据、训练与评测脚本全开（MIT，FLUX 权重受其非商用许可约束）。

**影响**：把"语义编码器 vs VAE 做参考控制"的路线之争摆上台面，为后续统一编辑模型提供了 VAE 之外的一条参照路径；催生 UniWorld 家族（V2 用 DiffusionNFT + MLLM training-free reward 做编辑 RL，OSP2.0 扩到 I2V 14B）。

**已知局限（作者自陈）**：
- **指令泛化不足**：训练数据有限 + 未微调 VLM，需特定指令模板才能稳超 BAGEL（GEdit G_SC 仅 4.93）。
- **参考一致性不足**：参考图固定 512×512，无法在 1024 生成下复现全部细节；**无文字编辑能力**。
- **benchmark 局限**：DPG-Bench/GenAI-Bench 高分常与人评不符；GenEval 强行绑定罕见共现物体；ImgEdit/GEdit 对参考区域不够敏感。
- 未来方向：与 VLM 联合训练、上更高分辨率/多尺度网格化语义编码器。

## 原始链接
- arxiv_abs: https://arxiv.org/abs/2506.03147
- arxiv_pdf: https://arxiv.org/pdf/2506.03147
- github: https://github.com/PKU-YuanGroup/UniWorld-V1
- hf_model: https://huggingface.co/LanguageBind/UniWorld-V1
- hf_dataset: https://huggingface.co/datasets/LanguageBind/UniWorld-V1

## 本地落盘文件
- ../../../sources/omni/2025/arxiv-2506.03147.pdf
- ../../../sources/omni/2025/uniworld-v1--readme.md
- ../../../sources/omni/2025/uniworld-v1--hf-modelcard.md
- ../../../sources/omni/2025/uniworld-v1--hf-dataset.md
