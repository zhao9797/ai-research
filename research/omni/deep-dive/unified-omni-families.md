---
title: "统一/Omni 模型族横向对比：Chameleon · Emu · Janus · BAGEL · OmniGen · Show-o · VAR 谱系"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [unified-multimodal, omni, autoregressive, diffusion, flow-matching, next-scale-prediction, understanding-generation, image-editing, deep-dive]
---

# 统一/Omni 模型族横向对比（2022–2026）

> 本页横向梳理"理解+生成统一""any-to-image""any-to-any omni"这一大类工作的**架构范式分化**与**能力边界**。覆盖工作：
> [[chameleon-cm3leon]]/[[chameleon]]、[[emu-multimodal]]/[[emu3]]/[[emu3-5]]、[[janus]]/[[janusflow]]/[[janus-pro]]、[[bagel]]、[[omnigen]]/[[omnigen2]]/[[omnigen-ar]]、[[show-o]]/[[show-o2]]、[[var]]/[[infinity-bitwise-var]]、[[transfusion]]、[[blip3-o]]/[[metaqueries]]/[[uniworld-v1]]/[[ming-omni]]/[[skywork-unipic-3-0]]/[[internvl-u]]。
>
> 数字均引自上述单工作页（单页已对抗式核过一手 PDF/HF/blog）。GenEval 标注 `†` 表示带 prompt rewriter，FID/DPG 等同。

---

## 0. 一张总表（时间 / 参数 / 架构 / 关键指标）

| 工作 | 时间 | 机构 | 规模 | 视觉表征 | 生成范式 | 理解/生成耦合 | GenEval | 其它关键数 |
|---|---|---|---|---|---|---|---|---|
| [[chameleon-cm3leon]] CM3Leon | 2023-07 | Meta FAIR | 7B | VQ 离散(Make-A-Scene) | 自回归 next-token | 单 decoder 单编码 | — | COCO FID **4.88**(检索增强,5× 省算力) |
| [[emu-multimodal]] Emu | 2023-07 | BAAI+THU+PKU | 14B | 连续 embedding(EVA-CLIP) | AR 回归 emb + 外挂 SD1.5 解码 | 单 LLM,视觉走 ℓ2 回归 | — | COCO-FID 11.66;Emu-I 14B 超 Flamingo-80B |
| [[chameleon]] Chameleon | 2024-05 | Meta FAIR | 7B/34B | VQ 离散(8192,512²→1024tok) | 早融合 AR next-token | 单 decoder 单编码 | 0.39 | 公开权重关图像生成;COCO-CIDEr 140.8(SFT) |
| [[var]] VAR | 2024-04 | ByteDance/PKU | 310M–2B | 多尺度残差 VQ(4096) | **next-scale prediction** | 纯生成(类别条件) | — | ImageNet256 **FID 1.73**/IS 350.2,~20× 快,NeurIPS24 best |
| [[show-o]] Show-o | 2024-08 | Show Lab/字节 | 1.3B(Phi-1.5) | VQ 离散(MAGVIT-v2,256tok) | **AR(文)+离散扩散/MaskGIT(图)** | 单 transformer,Omni-Attention | 0.68 | COCO-FID 9.24,采样步数~1/20 AR |
| [[transfusion]] Transfusion | 2024-08 | Meta/Waymo/USC | 0.16–7B | 连续 VAE latent | **AR(文)+DDPM 扩散(图)** | 单 transformer 单权重 | 0.63 | 对 Chameleon 图像 FID 达 parity 仅需 **1/34 算力** |
| [[emu3]] Emu3 | 2024-09 | BAAI | 8B | 离散(MoVQGAN,32768,4×8×8) | 纯 AR next-token(图/文/视频) | 单 decoder 单编码 | 0.66† | DPG 80.6,VBench 80.96(唯一 AR),首用 DPO 于 AR 生成 |
| [[omnigen]] OmniGen | 2024-09 | BAAI | 3.8B(Phi-3 init) | VAE latent(SDXL-VAE) | 扩散 rectified flow | 单 transformer(无 CLIP/T5) | 0.70 | 单模型统 T2I/编辑/主体/ControlNet/CV |
| [[janus]] Janus | 2024-10 | DeepSeek | 1.3B | **解耦**:理解 SigLIP / 生成 VQ | AR next-token | 单 transformer 双入口编码 | 0.61 | COCO-FID 8.53,理解超 LLaVA-1.5-7B |
| [[janusflow]] JanusFlow | 2024-11 | DeepSeek | 1.3B | 解耦:SigLIP / ConvNeXt-latent | **AR(文)+rectified flow(图)** | 单 LLM,普通 causal attn | 0.63 | MJHQ-FID **9.51**(1.3B 最佳) |
| [[infinity-bitwise-var]] Infinity | 2024-12 | ByteDance | 2B/8B | **比特级**多尺度残差(2^64) | bitwise next-scale | 纯 T2I | 0.73†(2B)/0.79†(8B) | 1024² **0.8s**(比 SD3-M 快 2.6×),ImageReward 0.96,CVPR25 Oral |
| [[janus-pro]] Janus-Pro | 2025-01 | DeepSeek | 1.5B/7B | 解耦:SigLIP / VQ(16384) | AR next-token | 单 transformer 双入口编码 | **0.80** | DPG 84.19,超 DALL-E3/SD3-M;无 RLHF |
| [[metaqueries]] MetaQuery | 2025-04 | Meta/NYU | 0.5/3/7B(冻结) | learnable queries→扩散 | 冻结 MLLM + 扩散解码器 | **集成**(MLLM 冻结) | 0.80† | 首个 **WISE 0.55 超 FLUX/SD3.5**;MJHQ-FID 6.02 |
| [[blip3-o]] BLIP3-o | 2025-05 | Salesforce | 4B/8B | **CLIP 特征扩散**(固定 64tok) | 冻结 Qwen2.5-VL + DiT flow | 集成(顺序训练,底座冻结) | 0.84(8B) | WISE 0.62,全开源(数据+权重) |
| [[bagel]] BAGEL | 2025-05 | ByteDance Seed | 7B激活/14B(MoT) | 双编码:SigLIP2 / FLUX-VAE | **AR(文)+rectified flow(图)** | MoT 双专家,共享自注意力 | 0.88†/0.82 | WISE 0.70(CoT),能力**涌现相位转变**(3.61T tok) |
| [[uniworld-v1]] UniWorld-V1 | 2025-06 | PKU-YuanGroup | ~20B(冻结 Qwen-VL+FLUX) | **SigLIP2 替 VAE** 做参考控制 | 冻结 VLM + FLUX flow | 集成 | 0.84† | 2.7M 数据 ImgEdit 3.26 超 BAGEL,首纳感知 |
| [[show-o2]] Show-o2 | 2025-06 | Show Lab/字节 | 1.5B/7B(Qwen2.5) | **3D 因果 VAE 连续**(Wan2.1) | **AR(文)+flow matching(图/视频)** | 单 transformer 双头 | 0.73/0.76 | DPG 86.14,66M 数据,扩展到视频 |
| [[omnigen2]] OmniGen2 | 2025-06 | BAAI | 3B+4B(VLM 冻结) | 双 tokenizer:ViT / Flux-VAE | 冻结 VLM + 扩散 flow + Omni-RoPE | 解耦双路,VLM 冻结 | **0.95** | OmniContext 7.95,Flow-GRPO 多任务 RL |
| [[ming-omni]] Ming-Omni | 2025-06 | 蚂蚁 Inclusion | 2.8B激活(MoE) | 模态专属 router + DiT 桥接 | 冻结 MLLM + multi-scale DiT | 集成(冻结+桥接) | 0.64 | **FID 4.85**,首开源对齐 GPT-4o 模态(图文音视) |
| [[emu3-5]] Emu3.5 | 2025-10 | BAAI | 34B | 离散(IBQ,131072,f16) | 纯 AR + **DiDA 并行去噪** | 单 decoder(类 Qwen3) | **0.86** | DPG 88.26,DiDA **~20× 加速**;世界模型/具身 |
| [[skywork-unipic-3-0]] UniPic 3.0 | 2026-01 | 昆仑 Skywork | 未披露(基 Qwen-Image) | VAE latent + 序列拼接 | flow MMDiT + **CM+DMD 蒸馏** | 专精编辑/多图合成 | — | ImgEdit 4.35,MultiCom 0.7255 超 Nano-Banana,**8 步 12.5×** |
| [[internvl-u]] InternVL-U | 2026-03 | 上海AILab/OpenGVLab | 4B(2B+1.7B) | 解耦:ViT / Qwen-Image-VAE | 冻结后解冻 + MMDiT flow | 集成→统一 SFT | **0.85** | DPG 85.18,RISEBench 3.6→9.4(CoT),门控 MMDiT |
| [[omnigen-ar]] OmniGen-AR | 2026-06 | 复旦/字节/HKU | 0.5B/1.5B | **共享图视频离散**(Cosmos-DV) | 纯 AR next-token | 单 decoder(Qwen2.5),DCA | 0.63 | VBench **80.02**(首个离散 AR 破 80);Any-to-Image |

> 注：参数列中"激活"指 MoE 激活参数。Chameleon/Emu/CM3Leon 等早期工作未用 FID/GenEval 标准报告生成质量，或聚焦人评（见正文）。

---

## 1. 脉络主线：从"碎片化拼接"到"单一序列"再到"分化为四条范式"

2023 年的起点是**碎片化**：理解（[[chameleon-cm3leon|CM3Leon]] 图→文、Flamingo/LLaVA）与生成（扩散系 SD/DALL-E/Imagen）由两类独立模型承担，"统一"往往只是把 LLM 当 condition 外挂一个预训练扩散模型（Emu、DreamLLM、SEED-X、NExT-GPT），本质仍是多模型系统。

到 2024–2026，竞争收敛到"**一个 Transformer 把理解和生成都装进来**"，但在三个关键设计轴上分化出截然不同的范式：

- **轴 A — 图像怎么表征？** 离散 token（VQ/MoVQGAN/IBQ/bitwise）vs 连续 latent（VAE）vs CLIP 语义特征。
- **轴 B — 图像怎么生成？** 自回归 next-token vs next-scale vs 离散扩散(MaskGIT) vs 连续扩散/flow matching。
- **轴 C — 理解和生成怎么耦合？** 单编码器共享 vs 解耦双编码器（理解 SigLIP/生成 VQ）vs 集成（冻结 MLLM + 外接扩散解码器）。

下面五节按"范式"而非"团队"组织，把谁在何时用什么方法把什么指标推到多少讲清楚。

---

## 2. 范式一：纯离散 token 自回归（"Next-Token is All You Need"）

**主张**：把图像也离散成 token，丢进一个标准 LLM 式 decoder，用单一 next-token 交叉熵统吃图/文（/视频）。优点是与 LLM 生态（scaling、infra、KV-cache）无缝；代价是 VQ 量化有损 + 逐 token 解码慢。

**谱系与硬线索**：
- [[chameleon-cm3leon]]（Meta FAIR, 2023-07, 7B）：先驱。复用 Make-A-Scene 的 VQ tokenizer（8192 码本、256² 图→1024 token），**检索增强**预训练 + SFT，zero-shot COCO **FID 4.88** 拿下当时 token-based SOTA，并号称比同类方法**省 5× 算力**；但**强依赖检索**（同 7B，0→1→2 检索文档 FID 由 10.82→5.78→4.88），分辨率仅 256²。
- [[chameleon]]（Meta FAIR, 2024-05, 7B/34B）：把上述思路 scale 到 ~10T token 的早融合 dense 模型，核心工程贡献是用 **QK-Norm + Swin 式 norm 重排 + z-loss** 解决多模态共享 softmax 的 logit-drift 发散。COCO-CIDEr 微调到 **140.8**（开源 SOTA），长文本混合模态人评对 Gemini-Pro+ 胜率 60.4%；但公开权重**关闭了图像生成**，图像 tokenizer 对**含文字图重建差**，GenEval 仅 0.39。
- [[emu3]]（BAAI, 2024-09, 8B）：第一个证明纯 next-token 在**生成和理解两端同时对标 SOTA**的工作。MoVQGAN tokenizer（32768 码本、4×8×8 压缩，图/视频共用），GenEval **0.66†**、DPG 80.6（超 SDXL、对标 DALL-E3）、视频 VBench **80.96**（唯一 AR，超 OpenSora-1.2），**首次把 DPO 用于 AR 视觉生成**。短板：裸短 prompt 要靠 GPT-4V rewriter、逐 token 解码慢。
- [[emu3-5]]（BAAI, 2025-10, 34B）：把离散 AR 路线推到"**世界模型**"，在 ~13T 视觉-语言交错 token（6300 万条视频关键帧+ASR）上预训练 + GRPO 多任务 RL。GenEval 跃到 **0.86**、DPG 88.26（vs Emu3 0.66/80.6），编辑 GEdit G_O **7.59**（超 Qwen-Image-Edit-2509、Nano-Banana）。最关键是 **DiDA**（离散扩散适配）把逐 token 解码改成双向并行去噪，单图 1024² 从 120s→**10s（~12×，整体口径 ~20×）**，让 AR **首次在速度与质量上同时逼近闭源 diffusion**。
- [[omnigen-ar]]（复旦/字节/HKU, 2026-06, 0.5/1.5B）：把离散 AR 推向 **any-to-image**——用**共享图像-视频离散 tokenizer（Cosmos-DV）**把文本/分割/深度/参考图/历史帧全部编进同一码本，单 decoder 统 T2I/T2V/帧预测/编辑/seg-to-image。创新点是**训练期注意力正则 DCA（Disentangled Causal Attention）**防"条件→内容"信息泄漏（10% 概率替换因果掩码），零推理开销。1.5B GenEval 0.63、VBench **80.02**（首个离散 AR 破 80）。

**共性边界**：离散 AR 对 tokenizer 质量高度依赖（Infinity 后面专治这点）；逐 token 解码慢（Emu3.5 的 DiDA 才破局）；裸 prompt 偏弱、依赖 rewriter。

---

## 3. 范式二：next-scale prediction（VAR 系，"由粗到细"重定义图像顺序）

**主张**：传统视觉 AR 把 2D token grid 展平成 1D 再 next-token，违反 VQ encoder 自带的双向相关、破坏空间局部性、且 O(n⁶) 低效。VAR 把自回归单元从"单 token"升级为"**整张尺度 token map**"，从 1×1 起逐级提分辨率，尺度内并行。

- [[var]]（ByteDance/PKU, 2024-04, 2B, NeurIPS24 best paper）：多尺度残差共享码本 VQVAE（4096 码本、16× 下采样）+ GPT-2 式 transformer。ImageNet 256² **FID 1.73 / IS 350.2**——**首次让 GPT 式 AR 超越扩散 Transformer**（2B VAR 击败 3B/7B 的 L-DiT），推理仅需 **10 个 model step**（vs DiT 250 步），快约 **20×**。最硬的实证：**仅替换"展平 next-token→next-scale"这一范式**（无任何 trick），FID 就从 18.65 暴降到 5.22、推理成本降到 0.013×。并首次在视觉生成中验证 LLM 式幂律 scaling law（相关系数 ≈ **−0.998**）。局限：仅类别条件 ImageNet，文生图/视频留作后续。
- [[infinity-bitwise-var]]（ByteDance, 2024-12, 2B/8B, CVPR25 Oral）：把 VAR 从 index-wise 升级为 **bitwise**，词表理论扩到 **2^64**。三大件：(1) **比特级 tokenizer（BSQ）**——词表 2^32 时 rFID 0.61 已**超过 SD 连续 VAE 的 0.87**，打破"离散细节差"瓶颈；(2) **Infinite-Vocabulary Classifier**——用 d 个并行二分类器替代 2^d 类大分类器，省 99.95% 参数（8.8 万亿→可算）；(3) **Bitwise Self-Correction**——随机翻转 30% 比特再重量化纠错，把 FID 从 9.76→**3.48**。结果 GenEval **0.73†**（2B）/**0.79†**（8B）、ImageReward 0.96、1024² **0.8s**（比 SD3-Medium 快 2.6×、对 SD3.5 快 7×），人评对 SD3-Medium 胜率 66%。

**意义**：VAR 系证明"离散自回归=又快又好"在 T2I 上可行，并催生 FlowAR/HART/Switti/STAR/VARGPT、视频 InfinityStar 等一大族 scale-wise 工作。

---

## 4. 范式三：单模型混合目标（AR 文 + 扩散/流 图，在同一 transformer 内）

**主张**：图像不必量化成离散 token——文本走 next-token（AR 强项），图像留在连续空间走扩散/flow（扩散在视觉质量上普遍优于 AR），两套损失塞进**一个 transformer**。

- [[transfusion]]（Meta/Waymo/USC, 2024-08, 7B）：单 transformer 单套权重，文本 next-token + 图像 **DDPM 扩散**，from-scratch 联合预训练（损失 `L_LM + 5·L_DDPM`）。关键 recipe：**整图内双向注意力 + 全局 causal**（消融把 FID 从 61.3→20.3）、image-level 扩散损失、U-Net patch 编码可把每图压到 16 token（64×）。与同门早融合离散的 [[chameleon]] 严格对照（同算力同数据）：图像 FID **达 parity 仅需 1/34 算力**，文本能力也更省——这是"连续扩散 vs 离散 AR"之争的一记重锤。GenEval 0.63、文本 Llama-Acc 66.1（与 Llama-1 持平）。未开源。
- [[show-o]]（Show Lab/字节, 2024-08, 1.3B, ICLR25）：另一条混合路——文本 next-token + 图像 **离散扩散（MaskGIT 式 masked-token，等价简化离散扩散）**，单一 Phi-1.5 backbone，**Omni-Attention**（文本 causal / 图像 full attention 自适应切换）。1.3B+35M 数据即 COCO-FID **9.24**、GenEval **0.68**（同尺寸 LDM 仅 0.37），且文生图采样步数约为 AR 的 **1/20**。还消除了独立 text encoder。
- [[show-o2]]（Show Lab/字节, 2025-06, 1.5B/7B）：升级到 **Wan2.1 的 3D 因果 VAE 连续潜空间** + **AR 头 + flow matching 头双头**，首次把统一建模扩展到**视频**。dual-path 空间-时间融合（SigLIP 蒸馏语义层 + projector 低层特征）兼顾理解/生成。仅 **66M 图文对**（vs Janus-Pro 144M、BAGEL 1600M）即 GenEval 0.76、DPG **86.14**（超 SD3-M/Janus-Pro），VBench 81.34（2B 总参超 Emu3-8B）。核心卖点是**两阶段配方保住语言能力**（7B 的 MMLU 70.73 几乎无损于原 Qwen2.5-7B；而一阶段共训会灾难退化到 28.43）。
- [[janusflow]]（DeepSeek, 2024-11, 1.3B）：把 rectified flow **原生嵌入 LLM**——证明无需 Transfusion 那样的特殊注意力掩码，**普通 causal attention 即可**，只配一对 ~70M ConvNeXt encoder/decoder + REPA 表征对齐正则。MJHQ-FID **9.51**（1.3B 最佳）、GenEval 0.63。
- [[bagel]]（ByteDance Seed, 2025-05, 7B激活/14B, MoT）：范式三里的集大成者。**Mixture-of-Transformer-Experts**——理解专家（next-token）+ 生成专家（rectified flow）每层**共享同一条 token 序列、共享多模态自注意力**（bottleneck-free，区别于 external-diffuser 的 latent 压缩瓶颈），双视觉编码器（SigLIP2 理解 / FLUX-VAE 生成）。在万亿级图文/视频/网页**交错**数据上从 Qwen2.5-7B 续训。GenEval **0.88†**、WISE 0.52→**0.70（CoT）**、编辑 IntelligentBench 44.9→55.3（远超开源 Step1X-Edit 14.9）。最有理论价值的发现是**能力涌现的相位转变**：以"达 85% 峰值所需 token"衡量，理解 ~0.18T、生成 ~0.68T 早饱和，经典编辑 ~2.64T，而**自由形变编辑/智能编辑要 ~3.61T token 才涌现**（3T 后从 15 飙到 45），且 loss 曲线看不出这种跃变，必须靠历史 checkpoint 评测追踪。

---

## 5. 范式四：解耦视觉编码（Janus 系，"理解归 SigLIP / 生成归 VQ"）

**主张**：理解需高层语义、生成需低层细节，**单一视觉编码器**同时服务两者会冲突，拖累理解。Janus 在"入口处"分叉视觉编码路径，但仍共享单一自回归 Transformer。

- [[janus]]（DeepSeek, 2024-10, 1.3B）：理解走 SigLIP 连续语义、生成走 LlamaGen 的 VQ（16384 码本、16× 下采样、384²→576 token），消融把"折衷"量化坐实：单编码器共享（Exp-B/C）理解明显逊于解耦（Exp-D POPE 87.0/MMB 69.4/SEED 63.7）。1.3B 即理解超 LLaVA-1.5-7B、生成 GenEval 0.61/COCO-FID 8.53 超 SDXL/DALL-E2。
- [[janus-pro]]（DeepSeek, 2025-01, 1.5B/7B）：架构不变，只**加数据加规模改策略**：延长 Stage I、Stage II 丢掉低效的 ImageNet 子集、SFT 配比 7:3:10→5:1:4、引入 **72M 合成美学数据**（真实:合成=1:1）。7B GenEval **0.80**、DPG **84.19**，**正面超过 DALL-E3(0.67)/SD3-Medium(0.74)**，同时理解 MMB 79.2。无 RLHF，靠合成数据兜底美感。

> 注：[[janusflow]] 虽出自 Janus 家族、也用解耦编码器，但生成范式是 flow matching，已归入范式三讨论；它是"解耦编码 × 混合目标"的交叉点。

**解耦思想的扩散**：后续 [[omnigen2]]、[[internvl-u]] 等都采纳"理解 ViT/生成 VAE 双 tokenizer"，可见这是被广泛复用的设计准则。

---

## 6. 范式五：集成（冻结 MLLM + 外接条件扩散解码器）

**主张**：不重建单体大模型，而是**桥接两个各自最强的预训练专家**——冻结 SOTA 理解 MLLM（保住理解、零损失），用可学习 query / VLM hidden states 把它"查询"出生成条件，喂给条件扩散解码器。哲学是"生成归扩散，理解归 LLM"，与推测中的 GPT-4o 图像管线（token→transformer→diffusion→pixels）同源。

- [[metaqueries]]（Meta/NYU, 2025-04, 0.5/3/7B 冻结）：用 256 个 **learnable queries** 把冻结 MLLM 接到 Sana/SD 扩散解码器，仅图文对 + 标准去噪目标即训成。最亮：**首个 WISE 超过纯 T2I SOTA 的统一模型**（WiScore **0.55** vs FLUX 0.50/SD3.5 0.46，碾压 Janus-Pro 0.35），MJHQ-FID 6.02。证明**冻结 MLLM 的世界知识与 in-context learning 可被有效转移到生成**；但 prompt alignment（GenEval/DPG）略逊自回归生成的 Janus-Pro。
- [[blip3-o]]（Salesforce, 2025-05, 4B/8B）：核心创新是**扩散对准 CLIP 语义特征**（固定 64 token）而非 VAE 像素 + flow matching + 顺序训练（冻结 Qwen2.5-VL 只训 1.4B DiT）。系统消融三轴得出"CLIP+Flow Matching+顺序训练"为最优配方。8B GenEval **0.84**、WISE 0.62，且**完全开源**（代码+权重+预训练数据+60k 指令数据），是该方向少有的可复现基线。
- [[uniworld-v1]]（PKU-YuanGroup, 2025-06, ~20B）：通过"逆向 GPT-4o-Image"对照实验论证应**用高分辨率对比语义编码器 SigLIP2 替代 VAE** 做参考图控制信号（VAE 低频信息过强、多任务不收敛）。冻结 Qwen2.5-VL-7B + FLUX.1-dev，**首个把感知（检测/分割/深度/canny）纳入统一生成**。极致数据效率：**2.7M 数据**即 ImgEdit **3.26** 超 BAGEL（2665M 数据）、GenEval 0.84†。短板：参考图固定 512² 致无文字编辑能力、GEdit G_SC 仅 4.93。
- [[ming-omni]]（蚂蚁 Inclusion, 2025-06, 2.8B 激活 MoE）：**首个对齐 GPT-4o 模态支持的开源 omni**（输入图/文/音/视，输出文/实时语音/图）。以 MoE LLM Ling 为中枢 + **模态专属 router**（T/V/A）缓解多模态冲突，冻结 MLLM 主体只训生成模块。图像生成 GenEval 0.64、**FID 4.85**（号称当时新 SOTA），语音理解超 Qwen2.5-Omni/Kimi-Audio。是本族里唯一真正"any-to-any"（含音频）的工作。
- [[internvl-u]]（上海 AILab/OpenGVLab, 2026-03, 4B=2B+1.7B）：把生成"无损"嫁接到 InternVL3.5-2B 理解基座 + 自研 **门控 MMDiT 生成头（首次把门控机制集成进 MMDiT 缓解 attention-sink）** + Unified 3D MSRoPE。三阶段渐进训练（冻结主干训生成头→任意分辨率→全解冻统一 SFT）。4B 即 GenEval **0.85**、DPG 85.18，**追平 14B 的 BAGEL**（MMMU 54.7 ≈ BAGEL 55.3）。最大特色是 **CoT 推理中心化数据**：RISEBench 3.6→**9.4**（CoT，超 BAGEL 6.1 与 Qwen-Image-Edit 8.9）、WISE 0.46→0.58、文字渲染 CVTG-2k 0.623（统一模型 SOTA），实质改善了"统一模型不会写字/缺知识推理"两大短板。

---

## 7. 范式六：通用图像生成基座（OmniGen 系，"图像生成界的 GPT 范式"）+ 多图合成

这条线介于范式三与五之间，强调"**单模型端到端跟随任意多模态指令，无插件无预处理**"，覆盖 T2I/编辑/主体/ControlNet/CV 等更广任务谱。

- [[omnigen]]（BAAI, 2024-09, 3.8B）：极简双组件 = VAE + 一个 Transformer（Phi-3 init），**消灭 CLIP/T5 文本编码器与所有条件 Adapter**，rectified flow 目标。3.8B 即 GenEval **0.70**（超 SD3 的 0.68/12.7B、DALL-E3 0.67），且单模型一步完成 ControlNet 式视觉条件生成（Canny F1 38.96 全表最高）。开源首个统一图像生成数据集 **X2I（~1 亿图）**。关键 trick：图像内双向注意力 + 编辑加权损失（防"直接复制输入"捷径）。
- [[omnigen2]]（BAAI, 2025-06, 3B+4B）：改为**解耦双路**——冻结 Qwen2.5-VL-3B + 随机初始化 diffusion decoder（Lumina-Image 2.0 backbone）+ 独立双 tokenizer（ViT 理解 / Flux-VAE 生成），diffusion 只条件化在 VLM **变长** hidden states 上（比 MetaQuery 定长 query 无瓶颈）。**Omni-RoPE**（实例身份 ΔI + 图内 2D 坐标）保证编辑空间对齐。仅 4B 可训练参数即 GenEval **0.95**（超 BAGEL 0.88、Qwen-Image），OmniContext **7.95**。**Flow-GRPO 多任务渐进 RL** 是主要功臣（无 RL 仅 0.78），并系统验证任务顺序敏感（Edit→T2I→IC 最优）、HPSv3 会 reward hacking。
- [[skywork-unipic-3-0]]（昆仑 Skywork, 2026-01）：把单图编辑与**多图合成（1~6 张）**统一为**序列建模**——目标噪声 latent + 全部参考 latent 沿序列维拼成长序列，同一 MMDiT（基 Qwen-Image）+ flow matching。仅 700K 量级 HOI 数据，**首次把"轨迹映射(consistency FM)+分布匹配(DMD)"联合蒸馏用于大规模多图合成**，**8 步推理、相对 50 步 12.5× 加速**。ImgEdit **4.35**（SOTA），自建 MultiCom-Bench **0.7255** 超闭源 Nano-Banana(0.7224)/Seedream 4.0(0.7088)。

---

## 8. 横向对比与能力边界

### 8.1 GenEval 时间线（谁把指令遵循推到多少）

```
Chameleon 0.39 (24-05)  →  Transfusion 0.63 / Show-o 0.68 (24-08)  →  Emu3 0.66† / OmniGen 0.70 (24-09)
   →  Janus 0.61 (24-10)  →  Infinity 0.73† 2B (24-12)  →  Janus-Pro-7B 0.80 (25-01)
   →  MetaQuery 0.80† (25-04)  →  BLIP3-o-8B 0.84 (25-05)  →  BAGEL 0.88† / OmniGen2 0.95 (25-05/06)
   →  Emu3.5 0.86 (25-10)  →  InternVL-U 0.85 (26-03)
```
两年内统一模型的 GenEval 从 0.39 推到 0.95（OmniGen2），关键拐点是 **Janus-Pro 用合成美学数据 + 策略修正首次正面超过 DALL-E3/SD3-Medium**，以及 **OmniGen2/BAGEL 用多任务 RL / 交错数据 + rewriter** 把上限拉到 0.88–0.95。注意 0.9+ 普遍依赖 prompt rewriter 与 RL，裸 prompt 差距更小。

### 8.2 三大轴上的选择如何决定能力边界

| 能力 | 谁最强 | 机制根因 |
|---|---|---|
| **理解保真** | 集成系（冻结 MLLM）：MetaQuery-XL MMMU 58.6、BLIP3-o-8B MMMU 50.6、UniWorld/OmniGen2 无损继承 Qwen2.5-VL | 冻结 SOTA 理解模型 = 理解零损失；而单编码器共享（Chameleon）会牺牲理解 |
| **世界知识生成 WISE** | MetaQuery 0.55（首超 FLUX/SD3.5）、BLIP3-o 0.62、BAGEL 0.70(CoT) | 把冻结 MLLM 的知识/ICL 转移到生成；CoT 进一步催化 |
| **推理式编辑** | BAGEL IntelligentBench 55.3、InternVL-U RISEBench 9.4(CoT)、Emu3.5 | 交错数据涌现 + 显式 CoT 规划 |
| **图像质量(FID)** | 集成/扩散系：MetaQuery MJHQ 6.02、Ming-Omni FID 4.85；VAR 系 ImageNet 1.73 | 扩散解码器控视觉伪影优于 AR；next-scale 由粗到细 |
| **推理速度** | Infinity 0.8s/1024²、Emu3.5-DiDA ~20×、UniPic3 8 步 12.5×、VAR ~20× | next-scale 少步 / 并行去噪 / 步数蒸馏破解 AR 慢的固有短板 |
| **文字渲染** | Emu3.5（LeX/LongText SOTA）、InternVL-U(CVTG-2k 0.623)；Show-o2/Janus 系弱 | 离散 VQ + 低分辨率致文字差；专门文本中心数据 + 高分辨率才补齐 |
| **any-to-any（含音频）** | Ming-Omni（唯一图文音视全模态） | MoE 模态 router + 端到端语音 decoder |
| **多图合成/感知** | UniPic3（多图 0.7255 超闭源）、UniWorld-V1（首纳感知）、OmniGen-AR（any-to-image） | 序列拼接 / 语义编码器参考控制 / 共享离散 tokenizer |

### 8.3 "离散 AR vs 连续扩散"之争的硬证据

- [[transfusion]] 与 [[chameleon]] 同算力同数据严格对照：连续扩散达到离散 AR 图像 FID parity **仅需 1/34 算力**，且文本也更省——一度被读作"连续扩散完胜"。
- 但 [[var]]（FID 1.73 超 DiT）、[[infinity-bitwise-var]]（rFID 0.61 反超 SD-VAE、GenEval 0.79†、0.8s）、[[emu3-5]]（DiDA 让 AR ~20× 提速逼近 diffusion）反过来证明：**离散 AR 的劣势主要来自 tokenizer 质量与解码顺序，而非范式本身**——把 tokenizer 做到 bitwise、把顺序改成 next-scale、把解码改成并行去噪后，离散路线在速度与质量上都能与扩散正面竞争。

### 8.4 数据效率谱（生成训练图文对数）

```
Show-o2  66M   <  Janus-Pro 144M  <  UniWorld-V1 2.7M(但含感知/编辑)  ≈  OmniGen2 ~150M
   <  Show-o 2.0B  <  Transfusion 3.5B  <  BAGEL 1600M  <  Emu3.5 ~13T token
```
鲜明对照：[[uniworld-v1]] 用 **2.7M 数据**追平 [[bagel]] 的 **2665M**（ImgEdit 3.26 vs 3.20），[[show-o2]] 用 **66M** 拿到与百M~十亿级模型可比的 DPG 86.14——集成/冻结底座路线的数据效率优势显著；而 [[bagel]]/[[emu3-5]] 走"大数据 scale 出涌现"的相反路径。

---

## 9. 时间轴上的范式迁移（同一团队的路线选择）

- **Meta FAIR**：[[chameleon-cm3leon|CM3Leon]]（离散 AR + 检索）→ [[chameleon]]（早融合离散 AR scale）→ [[transfusion]]（连续扩散，证明比离散 AR 省 34× 算力）→ [[metaqueries]]（冻结 MLLM 集成）——**从"全离散自训"一路退到"冻结+集成"**。
- **BAAI**：[[emu-multimodal|Emu]]（连续 emb + 外挂 SD）→ [[emu3]]（纯离散 AR）→ [[omnigen]]（扩散基座）→ [[omnigen2]]（解耦 + RL）→ [[emu3-5]]（离散 AR + DiDA 世界模型）——**离散与扩散两条线并行押注**。
- **DeepSeek**：[[janus]]（解耦 VQ-AR）→ [[janusflow]]（解耦 + rectified flow）→ [[janus-pro]]（VQ-AR scale）——**解耦编码是不变内核，生成范式在 AR/flow 间摇摆**。
- **Show Lab/字节**：[[show-o]]（离散扩散 MaskGIT）→ [[show-o2]]（连续 VAE + AR+flow 双头 + 视频）——**从离散 token 转连续潜空间**。
- **ByteDance（VAR 线）**：[[var]]（next-scale 类别条件）→ [[infinity-bitwise-var|Infinity]]（bitwise T2I）→ InfinityStar（视频）——**next-scale 一以贯之**。

---

## 10. 一句话总结各工作的不可替代贡献

- [[chameleon-cm3leon]]：首次把 LLM 全套配方（检索增强+SFT）搬到 token 多模态，FID 4.88 + 5× 省算力。
- [[chameleon]]：QK-Norm+z-loss+norm 重排解决早融合发散，把离散 AR scale 到 34B。
- [[emu-multimodal]]：连续视觉 embedding 统一生成的早期代表，video 作可扩展交错数据源（YT-Storyboard-1B）。
- [[emu3]]：第一个证明纯 next-token 生成与理解双端对标 SOTA，首用 DPO 于 AR 生成。
- [[emu3-5]]：DiDA 让 AR ~20× 提速逼近 diffusion，把 next-token 推到世界模型/具身。
- [[var]]：next-scale prediction 范式，首次 AR 超 DiT（FID 1.73），验证视觉 scaling law。
- [[infinity-bitwise-var]]：bitwise 建模 + IVC + 自纠正，离散 rFID 反超 SD-VAE，0.8s 出图。
- [[transfusion]]：单 transformer 双损失，证明连续扩散比离散 AR 省 34× 算力。
- [[show-o]]：单 transformer 内 AR + 离散扩散，采样步数 1/20 AR。
- [[show-o2]]：3D 因果 VAE 连续潜空间 + 双头扩展到视频，两阶段配方保语言能力。
- [[janus]]：首次提出"解耦视觉编码"，把单编码器折衷量化坐实。
- [[janusflow]]：rectified flow 原生嵌入 LLM（普通 causal attention 即可）。
- [[janus-pro]]：合成美学数据 + 策略修正，纯 AR 统一模型首超 DALL-E3/SD3-M。
- [[bagel]]：MoT 无瓶颈统一 + 发现能力涌现相位转变（智能编辑 3.61T token 才出现）。
- [[metaqueries]]：冻结 MLLM + learnable query，首个 WISE 超纯 T2I SOTA。
- [[blip3-o]]：扩散对准 CLIP 语义特征 + 全开源，系统性三轴消融。
- [[uniworld-v1]]：论证 SigLIP2 替 VAE 做参考控制，首纳感知，2.7M 数据追平 BAGEL。
- [[ming-omni]]：MoE 模态 router，首个开源对齐 GPT-4o 模态（图文音视）。
- [[omnigen]]：VAE+单 Transformer 极简基座，消灭 CLIP/T5 与所有 Adapter。
- [[omnigen2]]：冻结 VLM + 解耦双路 + Omni-RoPE + Flow-GRPO，GenEval 0.95。
- [[omnigen-ar]]：共享图视频离散 tokenizer + DCA 防泄漏，离散 AR 首破 VBench 80。
- [[skywork-unipic-3-0]]：多图合成序列建模 + CM/DMD 蒸馏，8 步超闭源 Nano-Banana。
- [[internvl-u]]：门控 MMDiT + CoT 数据，4B 追平 14B BAGEL，补齐文字/推理短板。

---

## 11. 仍未解决的共性边界（2026 视角）

1. **真正的"共享特征空间"统一未达成**：集成路线（冻结 MLLM + 桥接）是工程折中，Ming-Omni 等坦言理解-生成深层统一仍是 future work。
2. **裸 prompt 与 rewriter/CoT 的依赖**：GenEval 0.9+ 普遍靠 rewriter，WISE/RISEBench 高分靠 CoT，去掉后差距明显。
3. **文字渲染与精确空间推理**仍是离散 VQ + 低分辨率路线的硬伤，需专门数据 + 高分辨率（Emu3.5/InternVL-U 才补齐）。
4. **与闭源 SOTA 的差距**：GenExam（InternVL-U 22.9 vs Nano-Banana Pro 93.7）、RISEBench（vs GPT-Image-1.5 50.0）等高难推理基准上开源统一模型仍远落后。
5. **infra 不透明**：几乎所有工作未披露 GPU·时/并行/吞吐，复现成本难评估；高度依赖外部强模型蒸馏合成数据，存在配方可复现性与数据合规隐忧。
