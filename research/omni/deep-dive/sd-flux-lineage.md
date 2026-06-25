---
title: "模型族横向对比：Stable Diffusion → SDXL → SD3 → FLUX 谱系"
type: source
created: 2026-06-25
updated: 2026-06-25
tags: [deep-dive, lineage, stable-diffusion, sdxl, sd3, flux, latent-diffusion, mmdit, rectified-flow, t2i, open-weights]
---

# Stable Diffusion → SDXL → SD3 → FLUX 谱系横向对比

> 一条线索贯穿 2021–2026：**潜空间扩散（latent diffusion）** 这套两阶段骨架（VAE 压缩 + 在潜空间里跑生成 backbone + 交叉/联合注意力注入文本条件）从未被推翻，被推翻的是它的每一个零件——backbone 从 **U-Net → MMDiT（多模态扩散 Transformer）**，训练目标从 **DDPM ε-预测 → rectified flow（整流流速度场）**，文本编码器从 **单 CLIP → 双 CLIP → 三编码器(CLIP×2+T5) → 单个大 VLM（Mistral-3 24B / Qwen3）**，VAE 潜通道从 **4 → 16 → 128**。这条谱系的人事也是一条线：LDM/SD/SDXL/SD3 的核心作者（Rombach、Esser 等）2024 年从 Stability 出走创立 Black Forest Labs，把同一套方法工业化成 FLUX。本页把这 13 个工作放在一张时间轴上，抠出"谁在什么时间用什么方法把什么指标推到多少"。

涉及工作（按谱系，slug 即单页文件名）：
[[latent-diffusion-ldm]] → [[stable-diffusion-1]] / [[stable-diffusion-2]] → [[sdxl]] → [[stable-cascade]] → [[stable-diffusion-3]] / [[stable-diffusion-3-5]] → [[flux-1]] / [[flux-1-1-pro]] / [[flux-1-tools]] / [[flux-1-kontext]] / [[flux-1-krea-dev]] / [[flux-2]] / [[flux-2-klein]]。

---

## 0. 一张总表（数字均引自对应单页，单页已对抗式核过）

| 模型 | 时间 | backbone | 主参数量 | 文本编码器 | VAE 潜通道 | 训练目标 | 关键指标（一手） |
|---|---|---|---|---|---|---|---|
| [[latent-diffusion-ldm]] | 2021-12 | U-Net | 文生图 1.45B；ImageNet 400M | 自训 BERT-tokenizer Transformer（32 层/dim1280/len77） | 4（f=8） | DDPM ε-pred（1000 步 linear） | ImageNet LDM-4-G FID **3.60**（CFG）；COCO LDM-KL-8-G FID **12.63**；训练 271 V100-days vs ADM 916 |
| [[stable-diffusion-1]] | 2022-08 | U-Net | UNet **860M** | 冻结 CLIP ViT-L/14（123M） | 4（f=8） | DDPM ε-pred | 6.9GB VRAM 出 512²；256 张 A100 / ~150k A100·h；官方只给相对 pareto 图，无绝对 FID |
| [[stable-diffusion-2]] | 2022-11 | U-Net | UNet **865M**（同 1.5） | OpenCLIP ViT-H/14（penultimate） | 4（f=8） | 512=ε-pred，768=**v-pred** | 原生 768²；附 x4 超分/depth2img/inpaint；无绝对 FID |
| [[sdxl]] | 2023-07 | U-Net（异构 `[0,2,10]`） | UNet **2.6B**；pipeline 6.6B | **双编码器** CLIP ViT-L ⊕ OpenCLIP ViT-bigG（ctx 2048） | 4（f=8，重训 VAE rFID 4.4） | DDPM DSM + offset-noise 0.05 | 四模型人评 base+refiner **48.4%** vs SD1.5 7.9%；PartiPrompts vs MJ v5.1 **54.9%**；刻意不报 FID |
| [[stable-cascade]] | 2024-02 | Stage C=16×ConvNeXt（无 U-Net）；Stage B=U-Net | Stage C 3.6B/1B + Stage B 1.5B/700M | OpenCLIP ViT-H/14（unpooled） | 语义潜空间 **42×** 压缩（24×24） | DDPM cosine + p2 加权 | Würstchen 1B：COCO-30k FID **23.6**/IS **40.9**；Stage C 仅 24,602 A100·h（vs SD2.1 200k） |
| [[stable-diffusion-3]] | 2024-03 | **MMDiT** | 800M–**8B**（depth 15→38） | **三编码器** CLIP-L+CLIP-G+T5-XXL(4.7B) | **16** | **rectified flow** + logit-norm(0,1) | GenEval overall **0.74**（8B,1024²,w/DPO）> DALL·E3 0.67；总算力 5×10²² FLOPs |
| [[stable-diffusion-3-5]] | 2024-10 | MMDiT / **MMDiT-X** | Large **8.1B** / Medium 2.5B / Turbo | CLIP-L+CLIP-bigG+T5-XXL | 16 | rectified flow + **QK-Norm** | Medium 9.9GB VRAM；Turbo **4 步**(ADD)；官方仅定性，无 GenEval 数字 |
| [[flux-1]] | 2024-08 | **混合双流(19)+单流(38) MMDiT**，3D RoPE | **12B**（pro/dev/schnell） | T5-XXL + CLIP | **16**（Flux-VAE） | rectified flow；dev=guidance 蒸馏，schnell=**LADD 1–4 步** | Flux-VAE PDist **0.332**/SSIM 0.896/PSNR 31.1（全胜 SD3/SDXL VAE）；1024² 3–5s |
| [[flux-1-1-pro]] | 2024-10 | 同 FLUX.1 骨干（闭源） | 未披露（家族 12B） | T5+CLIP（家族） | 16 | rectified flow + ADD/LADD | Artificial Analysis Arena **Elo 第一**（"blueberry"）；比初代 [pro] **快 6×**；Ultra 4MP/~10s |
| [[flux-1-tools]] | 2024-11 | FLUX.1 主干上微调/adapter | 12B | T5+CLIP | 16 | rectified flow + guidance 蒸馏 | 通道拼接把 ControlNet 内化（in_ch 64→128/384）；Fill[pro] inpaint ELO 第一；Depth[pro] > MJ ReTexture |
| [[flux-1-kontext]] | 2025-05 | FLUX.1 主干 + in-context token 拼接 | dev **12B**；pro/max 未披露 | T5+CLIP（家族） | 16 | rectified flow；[pro]=LADD，[dev]=guidance 蒸馏 | 多轮编辑角色一致性(AuraFace)漂移最慢；1024² 3–5s，比 GPT-Image 快 ~8×；KontextBench 1026 对 |
| [[flux-1-krea-dev]] | 2025-07 | 同 FLUX.1 [dev] 骨干（drop-in） | 12B | T5+CLIP（家族） | 16 | rectified flow + 自研偏好优化 **TPO** | 人评**与闭源 FLUX1.1 [pro] 持平**；<1M 后训练数据；专治"AI 塑料感" |
| [[flux-2]] | 2025-11 | MMDiT(8 双流+48 单流)+共享调制+无 bias | [dev] **32B** | **Mistral-3 24B VLM 单编码器**（中间层 [10,20,30]，len 512） | **128**（rFID **0.1124**） | rectified flow；[dev]=guidance 蒸馏 | 人评胜率 T2I **66.6%**/多参考 63.6%/单参考 59.8%；VAE gFID 3.70；4MP，≤10 参考图 |
| [[flux-2-klein]] | 2026-01 | MMDiT 缩小版（4B:5+20 / 9B:8+24） | **4B / 9B** | **Qwen3 嵌入器**（4B 用 Qwen3-4B、9B 用 Qwen3-8B，层 [9,18,27]） | 32（FLUX.2 VAE） | rectified flow + **尺寸+步数(4)+引导** 三重蒸馏 | 4B 消费级 ~13GB / 4 步 / **<0.5s**；9B distilled "匹配/超过 5× 尺寸模型"；KV-cache 多参考 2–2.7× |

> 口径提醒：本族官方普遍**以人评为主、刻意回避 FID**（SDXL 论文专门论证 COCO zero-shot FID 与人类审美负相关；BFL 全系只发 ELO/胜率）。GenEval 绝对值只有 SD3 公布过；FLUX 系几乎全部标准 t2i benchmark（GenEval/DPG/HPSv2/PickScore）官方**未报告**，只有 VAE 重建是硬数字。

---

## 1. 起点：潜空间扩散范式（2021，LDM）

[[latent-diffusion-ldm]]（CompVis，2021-12）确立了此后五年统治至今的两阶段骨架：先用一个对抗+感知损失训练的 **VAE/VQGAN 把图像压进低维潜空间**（下采样因子 f=8，512²→64×64×4），再在这个空间里跑 DDPM 式扩散 U-Net，**交叉注意力（cross-attention）** 把文本/语义图/布局等任意 token 化条件注入。核心收益是算力：ImageNet 类条件 LDM-4-G 取得 **FID 3.60**（仅 400M 参数、271 V100-days）就超过了像素扩散 ADM 的 FID 4.59（608M、916 V100-days）；文生图 LDM-KL-8-G 在 COCO 上 **FID 12.63**（1.45B），与同期 GLIDE（6B）/Make-A-Scene（4B）持平却小数倍。论文系统扫了 f∈{1,2,4,8,16,32}，论证 **f=4/8 是"压缩-保真"甜区**——这是后续全族都选 f=8 的依据。

注意一个常被忽略的细节：LDM 原论文文生图用的是**自训的 BERT-tokenizer Transformer 文本编码器**，不是 CLIP。把它换成冻结 CLIP，是 Stable Diffusion 的事，不是 LDM 的事。

## 2. 产品化与重训迭代（2022，SD1 / SD2）—— 同一 U-Net，换零件

[[stable-diffusion-1]]（2022-08）不是方法突破，而是把 LDM 工业化的工程里程碑：860M U-Net + **冻结 CLIP ViT-L/14**（"as suggested in Imagen"）+ LAION-2B 美学子集，**6.9GB VRAM 出 512²**，256 张 A100 训 ~150k A100·小时。它的意义全在"民主化"——WebUI/ComfyUI/DreamBooth/LoRA/ControlNet 几乎全部以 SD1.x 为底座。其 checkpoint 树（v1-1→v1-2，再并行分叉 v1-3/4/5）和"10% drop 文本条件以支持 CFG、guidance scale 7.5"是社区微调的事实标准。

[[stable-diffusion-2]]（2022-11）是"重训迭代"而非架构升级——U-Net 仍 865M、与 SD1.5 同规模。变的是三处零件：(1) 文本编码器换成**全开源的 OpenCLIP ViT-H/14**（解决 OpenAI CLIP 不可商用再训的卡脖子）；(2) **原生 768²** 并引入 **v-prediction** 训练目标（Salimans & Ho 的 progressive distillation，高分辨率数值更稳）；(3) 一次性附带 x4 latent 超分 / depth2img（MiDaS 深度引导）/ inpainting 三个配套模型，把 v1 时代靠社区拼装的能力官方化。其 depth2img "给 U-Net 加一条零初始化输入通道承载深度"是后来 ControlNet 结构控制思路的前身之一。代价：2.0 因 NSFW 过滤过严导致人像退化，两周后被迫发 2.1（唯一明文差异是"更宽松的 NSFW 过滤"）。

> SD1/SD2 都**只发相对 pareto 改进曲线、明确声明"未针对 FID 优化"**，无可引用的绝对 FID——这是本族"轻 benchmark"传统的开端。

## 3. 第一次规模与条件升级（2023，SDXL）—— U-Net 的巅峰

[[sdxl]]（2023-07）是 Stability 走向 DiT 之前的**最后一代旗舰 U-Net**，把工程杠杆叠满：

- **3× 放大的异构 U-Net（2.6B）**：把 transformer block 重心下移到低分辨率层（`[0,2,10]`，删掉 8× 下采样级）。
- **双文本编码器**：CLIP ViT-L ⊕ OpenCLIP ViT-bigG 拼成 **context dim 2048**（SD1 为 768、SD2 为 1024），并额外注入 OpenCLIP pooled embedding 做全局条件。
- 两个"无需额外监督"的招牌**微条件（micro-conditioning）**：**size-conditioning**（把原始高宽喂进去，免丢小图——论文测得按 256² 阈值丢图会丢 **39%** 数据；ImageNet 消融 FID-5k 36.53 优于无条件 39.76）和 **crop-conditioning**（喂裁剪坐标，推理设 (0,0) 消除裁切伪影）。
- **multi-aspect** 多宽高比训练 + **base+refiner 两阶段"ensemble of experts"**（refiner 用 SDEdit 在潜空间精修后 20% 去噪步）。

评测口径上 SDXL 做了一件影响深远的事：**用人评取代 FID 并公开论证 FID 不适用**（COCO zero-shot FID 反而是 SD1.5/2.1/SDXL 三者最差）。四模型人评中 base+refiner 胜率 **48.4%**（SD1.5 仅 7.9%、SD2.1 6.7%），PartiPrompts 对 Midjourney v5.1 以 **54.9%** 略胜。SDXL 此后两年是开源 t2i 的事实底座。

## 4. 效率支线（2024-02，Stable Cascade）—— 一次没有延续的实验

[[stable-cascade]]（Würstchen v3）是 SDXL→SD3 之间一次**效率方向的开源押注**，也是本谱系唯一"非主线、未被延续"的分支。它把潜空间压缩从 SD 的 8× 拉到 **42×**（1024²→24×24），靠的不是单一 VAE 而是**三级级联**：Stage A（f4 VQGAN，20M）+ Stage B（U-Net 潜扩散重建器，由 EfficientNetV2-S 语义压缩器引导）+ **Stage C（16 个无下采样 ConvNeXt block，彻底抛弃 U-Net）**。核心收益是训练成本：底层 Würstchen 1B Stage C 仅 **24,602 A100·小时**（vs SD2.1 200k，约 8×），v3 口径相比同规模 SD 降约 16×。

但它质量绝对值仍逊于更大的 SDXL——Würstchen 论文 PickScore 二选一对 SDXL **仅 39.4%**（对 SD1.4/2.1 则 78%+）；COCO-30k FID 23.6（偏高，因生成图偏平滑），不过 **IS 40.9 是该表最高**。Stability 没有把级联路线延续下去，下一代直接跳到了 DiT。

## 5. 范式跃迁（2024-03，SD3 / MMDiT + rectified flow）—— 全族的分水岭

[[stable-diffusion-3]] 是整条谱系**真正的范式断点**，一次性换掉了两个最核心的零件，且都用大规模控制实验证明：

1. **训练目标：DDPM/v-pred → rectified flow**。把数据-噪声连成**直线** `z_t=(1−t)x0+tε`、网络回归速度场，配关键的 **logit-normal 时间步加权**（中间步信息量最大）。SD3 对比了 **61 种公式**，结论 `rf/lognorm(m=0,s=1)` 在 5/10/20/25+ 步全区间一致最优。整流流方法本身来自 [[rectified-flow]]（UT Austin, 2022）与 flow matching。
2. **backbone：U-Net → MMDiT（Multimodal Diffusion Transformer）**。文本流与图像流**各持一套独立权重**，仅在 attention 处拼接序列实现**双向信息流**（优于 Pixart-α 那种单向 cross-attention 喂文本）。架构对比中 MMDiT 在 validation loss/CLIP/FID 三项全面优于 vanilla DiT / CrossDiT / UViT。

外加四个工程要点：VAE **潜通道 4→16**（重建 FID 2.41→1.06，从此 16 通道成全族标配）、**CogVLM 做 50/50 原始/合成 re-caption**（GenEval overall 43.27→49.78）、**QK-RMSNorm** 稳定 bf16 高分辨率训练、分辨率相关 timestep shift（α=3.0）。规模做到 depth=38 / **8B / 5×10²² FLOPs** 无饱和。

硬数字：8B 模型 **GenEval overall 0.74**（1024², w/DPO），超过此前 prompt-comprehension SOTA DALL·E 3（0.67），Two Objects 0.94、Color Attribution 0.60 尤为突出；人评 typography/prompt-following 等于或胜过 DALL·E 3 / MJ v6 / Ideogram v1。**这套 DiT+flow 配方此后被本族全部后继者（SD3.5、整个 FLUX 系）继承。**

> 注：SD3 论文成绩对应 8B 基座；实际首发的 SD3 Medium（2B）在人体解剖上口碑翻车，直接催生了 SD3.5。

## 6. 产品化重训（2024-10，SD3.5）—— 把 SD3 做成"可生态化底座"

[[stable-diffusion-3-5]] 是 SD3 Medium 翻车后基于社区反馈的重训，**架构核心（rectified flow + MMDiT + 三编码器 + 16ch VAE）与 SD3 论文一致，未发独立技术报告**。三个增量：(1) 把 **QK-Normalization** 系统性引入，既稳训又**大幅提升下游可微调性**（官方坦诚代价是同 prompt 不同 seed 方差更大——刻意保留更广风格多样性）；(2) Medium 专属 **MMDiT-X**（前若干层加双注意力）+ 多分辨率渐进训练（**256→512→768→1024→1440** + mixed-scale）；(3) 对 Large 用 **ADD（Adversarial Diffusion Distillation）** 蒸出 **4 步**的 Large Turbo。

档位：Large 8.1B / Medium 2.5B（仅 **9.9GB VRAM**，不含文本编码器）/ Large Turbo（4 步、guidance 0）。它和同期 FLUX.1 形成"开源 MMDiT/flow 路线双雄"。SD3.5 自身**未公布任何 GenEval/FID 绝对值**，只有定性自评。

## 7. 工业化集大成（2024-08起，FLUX 家族）—— 原班人马的"再创业"

SD3 的核心作者出走创立 Black Forest Labs，[[flux-1]]（2024-08）是这条"潜空间+整流流+多模态 DiT"主线的工业化巅峰。它在 SD3 基础上把规模拉到 **12B**，并升级架构：

- **混合双流/单流块**：先过 **19 个双流块**（MMDiT 式各持权重），拼接后过 **38 个单流块**，最后丢文本 token。
- **3D RoPE**（每个潜 token 用 (t,h,w) 索引，单图 t≡0）——这给后续 Kontext 的"多图序列拼接"和视频扩展留好了接口。
- **融合 FFN + 并行注意力**（ViT-22B 式，减半调制参数 + 融合 attn/MLP 线性层成大矩阵乘）提升吞吐。
- **16 通道 Flux-VAE**（对抗目标从零训）：Kontext 论文 Table 1 给出它对全族 VAE 的碾压——**PDist 0.332 / SSIM 0.896 / PSNR 31.1**，全面优于 SD3-VAE(0.452/0.858/29.6)、SDXL-VAE(0.890/0.748/25.9)。

**三档发布范式**是其商业模式创新：`[pro]`（闭源 API 旗舰，超 MJ v6/DALL·E3 HD/SD3-Ultra）+ `[dev]`（开源、**guidance 蒸馏**、质量近 pro）+ `[schnell]`（Apache-2.0、**LADD 蒸馏 1–4 步**）。1024² 出图 3–5 秒。**最大透明度缺口：FLUX.1 基座始终无技术报告，训练数据与算力完全未披露**，架构细节要靠后续 Kontext 论文反推。

### 7.1 [[flux-1-1-pro]]（2024-10）—— 闭源旗舰 + API 商业化
"更快更好"的闭源迭代：比初代 [pro] **快 6×**，以代号 "blueberry" 匿名进 Artificial Analysis Arena **登顶 Elo**（截至 2024-10-01）。一个月后补 **Ultra 模式**（4× 分辨率、≤4MP、~10s/图）与 **Raw 模式**（真实摄影质感），上线 BFL API（4¢/图）。确立"开放权重(dev/schnell)+API 旗舰(pro)"双轨范本。

### 7.2 [[flux-1-tools]]（2024-11）—— 把 ControlNet/IP-Adapter "内化"进主干
四件套（Fill/Canny/Depth/Redux），创新不在新网络而在**统一范式**：Canny/Depth/Fill 走"**VAE 编码条件图 + 沿通道维拼接 + 微调主干**"（in_channels 64→128/384，Fill 含 256 通道显式 mask），**没有旁路网络、没有 residual 注入**——diffusers 文档明确"this is *not* a ControlNetModel"；Redux 走"**SigLIP 图像 token 投影后拼进文本序列**"的轻 adapter。每件 [dev](含 LoRA)+[pro] 双轨。Fill[pro] 号称彼时 inpainting SOTA、Depth[pro] 超 MJ ReTexture（均 ELO，无自动指标）。它的"参考图 token 当文本 token"思路直接通向 Kontext。

### 7.3 [[flux-1-kontext]]（2025-05）—— in-context 统一生成+编辑（FLUX 系唯一正式技术报告）
把参考图经**冻结 Flux-VAE 编码成 latent token，直接追加到目标 token 后**（论文试过通道拼接，效果更差故弃用），用 **3D RoPE 常数偏移** 区分 context/target（参考图当"虚拟时间步" u=(i,h,w)）。单一 rectified-flow DiT 同时做 T2I 与五类编辑（局部/全局/角色/风格/文字）。最大亮点是**多轮编辑角色一致性**（用 **AuraFace 人脸相似度** 量化，漂移显著慢于 GPT-Image-1/Runway Gen-4），1024² 3–5s（比 GPT-Image 快 ~8×）。自建 **KontextBench**（1026 image-prompt 对）。[dev] 12B 开源、只在 i2i 上训；[pro]=LADD、[max]=更多 compute。它也是全族唯一披露完整训练 infra 的（FSDP2 混合精度 bf16 all-gather + fp32 reduce-scatter、Flash Attention 3、regional compilation）。

### 7.4 [[flux-1-krea-dev]]（2025-07）—— "opinionated 后训练"专治 AI 味
**架构完全不变**（12B、drop-in 替换 FLUX.1 [dev]），创新全在后训练方法论：用 BFL 提供的"未烘焙(raw)"base `flux-dev-raw` → SFT（手工策展 + 混入 Krea 1 合成样本稳定 checkpoint）→ 自研偏好优化 **TPO**（DPO 系）。核心论点反主流：**主观美学不应用全局/平均偏好对齐**（在公开偏好集 PickScore/ImageReward 上训练会引发"色板坍缩 color palette collapse"、构图对称化、纹理过软、回归 AI look），而应**故意过拟合到一种明确艺术方向**。实证"**<1M 数据即可做好后训练，质量 > 数量**"。人评中**与闭源 FLUX1.1 [pro] 持平**（无具体数字）。

### 7.5 [[flux-2]]（2025-11）—— 全新架构、从零预训练
不是 FLUX.1 的 drop-in，而是新一代，目标转向"真实生产工作流"。两条关键升级：

1. **大 VLM 单编码器**：用 **Mistral-3 24B VLM** 替换 FLUX.1 的 CLIP+T5 双编码器（取中间层 [10,20,30] 堆叠、len 512），把世界知识/上下文理解灌进生成，同时承担多参考图理解。
2. **从零重训的 128 通道 VAE**：以"可学习性-质量-压缩三难"为框架，引入 **REPA/DINOv2 式语义正则** + 放大潜维度。每 token 通道数演进 **SD 16 / FLUX.1 64 / FLUX.2 128**；rFID **0.1124**（族内最佳），可学习性 gFID 3.70（FLUX.1 的 10.13 → -63.4%）。

DiT 也改：**8 双流 + 48 单流**（偏向单流，FLUX.1 为 19/38）、共享调制（DiT-Air）、全程无 bias、SwiGLU。[dev] **32B 开源**，统一文生图 + ≤10 张参考图编辑、4MP。人评胜率 **T2I 66.6% / 多参考 63.6% / 单参考 59.8%**（vs 主流开源）。代价：32B 全量 bf16 >80GB VRAM，消费级需 NF4/FP8 量化（最低 group-offload 8GB）。

### 7.6 [[flux-2-klein]]（2026-01）—— "蒸馏出的小模型" + 交互式视觉智能
把 32B FLUX.2 base 通过**尺寸蒸馏 + 步数蒸馏(4步) + 引导蒸馏**三重压成 4B/9B（"比同尺寸从头训练更强、保留教师大部分能力"）。**关键差异：klein 换文本编码器为 Qwen3 嵌入器**（4B 用 Qwen3-4B、9B 用 Qwen3-8B，取层 [9,18,27]），而非 base 的 Mistral-24B——验证"换更小但够强的 LLM 当 text embedder"可行。4B 消费级 ~13GB / 4 步 / **<0.5s**，**Apache-2.0**。工程创新 **KV-cache 编辑加速**：把 LLM 的 KV-cache 搬到 diffusion 多参考编辑（参考 token 跨去噪步不变，一次编码复用），多参考 **2–2.7× 提速**且不掉质量。9B distilled "匹配/超过 5× 尺寸模型，且在半秒内"。

---

## 8. 五条演进主线（把零件的变化串成趋势）

### 8.1 Backbone：U-Net → MMDiT → 偏单流的高效 DiT
`LDM/SD1/SD2 U-Net(860–865M)` → `SDXL 异构 U-Net(2.6B)` → `Stable Cascade 抛 U-Net 用 ConvNeXt（旁支）` → `SD3 MMDiT(8B)，文图双流各持权重、attention 处共享` → `FLUX.1 双流19+单流38(12B)` → `FLUX.2 双流8+单流48(32B)，共享调制/无bias/SwiGLU` → `klein 缩小版(4B 双流5+单流20 / 9B 8+24)`。趋势是**参数重心从双流移向单流**（FLUX.1[dev] 54% 参数在双流块，FLUX.2[dev] 仅 ~24%），单流块更省算力。

### 8.2 训练目标：DDPM ε-pred → v-pred → rectified flow
`LDM/SD1 ε-pred(1000步 linear)` → `SD2-768 v-prediction` → `SDXL DSM + offset-noise` → `SD3 起全族 rectified flow + logit-normal 时间步加权(0,1)`。SD3 用 61 公式对比把整流流钉成 SOTA 实践后，**FLUX 全系无一例外是 rectified flow**。加速侧：从无蒸馏(SD1/SDXL)，到 **ADD**（SDXL-Turbo/SD3.5 Turbo 4 步）、**guidance 蒸馏**（FLUX [dev]）、**LADD**（schnell/Kontext[pro] 1–4 步）、到 klein 的**三重蒸馏**（尺寸+步数+引导）。

### 8.3 文本编码器：从单 CLIP 到大 VLM
`LDM 自训 BERT-Transformer` → `SD1 冻结 CLIP ViT-L(768)` → `SD2 OpenCLIP ViT-H(1024)` → `SDXL 双编码器 CLIP-L⊕bigG(2048)` → `SD3/SD3.5 三编码器 CLIP-L+bigG+T5-XXL(4.7B)` → `FLUX.1 T5+CLIP` → `FLUX.2 Mistral-3 24B VLM 单编码器` → `klein Qwen3 嵌入器`。质的飞跃在 FLUX.2：从"专用文本/对齐编码器拼接"变成"**直接拿一个大语言/视觉模型的隐状态当条件**"，把世界知识引入图像生成（取中间层而非末层，arXiv:2505.10046）。

### 8.4 VAE 潜空间：通道数一路狂飙，重建天花板抬高
`SD/SDXL f=8、4 通道`（SDXL 重训 VAE rFID 4.4）→ `SD3/FLUX.1 16 通道`（SD3 重建 FID 1.06；Flux-VAE PDist 0.332/PSNR 31.1）→ `FLUX.2 128 通道`（rFID 0.1124）。Stable Cascade 是异类——不是加通道而是把**空间压缩从 8× 推到 42×**（语义级压缩 + 两级解码器）。FLUX.2 还引入 **REPA 语义正则**解决"重建质量 vs 潜空间可学习性"的张力，这是把学术界 REPA-E/RAE 路线带进工业旗舰。

### 8.5 评测哲学：本族集体"轻 FID、重人评"
SDXL 论文白纸黑字论证 COCO zero-shot FID 与人类审美**负相关**，自此 SD1/SD2/SDXL/SD3.5 都只发相对 pareto 图或定性自评，**唯一公布 GenEval 绝对值的是 SD3（0.74）**。FLUX 全系更彻底——只发 ELO/人评胜率（FLUX.2 T2I 66.6%）和 **VAE 重建硬数字**，GenEval/DPG/HPSv2/PickScore 等标准 t2i 自动指标官方**一律未报告**。Kontext 甚至提出 **"bakeyness（AI 味）"** 概念批判单一偏好评测会偏向过饱和。这是一个一致的、需要读者警惕的口径——本族横评只能靠人评和 VAE 指标，难以用统一自动 benchmark 排座次。

---

## 9. 一句话收束

这条谱系的内核 5 年没变（VAE 潜空间 + 生成 backbone + 注意力注入文本），但每个零件都被换了一遍，且换零件的节奏越来越快：**2021–2023 是 U-Net + DDPM 的渐进放大（LDM→SD→SDXL）**，**2024-03 的 SD3 是分水岭（一次性换上 MMDiT + rectified flow + 16ch VAE + 三编码器）**，此后原班人马把它工业化成 FLUX 并持续加速——**2024 三档蒸馏发布、2025 in-context 统一编辑(Kontext)与 opinionated 后训练(Krea)、2025-11 换大 VLM 编码器与 128ch VAE(FLUX.2)、2026 三重蒸馏的交互级小模型(klein)**。如果说 SD3 论文回答了"用什么生成式公式 + 怎么注入文本"，那么 FLUX 系正在回答下一个问题：**怎么把图像生成模型变成一个能感知、生成、记忆、推理的多模态智能体的一部分**——FLUX.2 用大 VLM 当编码器、klein 主打"交互式视觉智能"，已经是这个方向的脚注。

---

## 相关单页（slug 内链）
- 范式根基：[[latent-diffusion-ldm]] · [[rectified-flow]]（整流流方法源头）
- Stable Diffusion 线：[[stable-diffusion-1]] · [[stable-diffusion-2]] · [[sdxl]] · [[stable-cascade]] · [[wurstchen]]（Cascade 底层）
- SD3 线：[[stable-diffusion-3]] · [[stable-diffusion-3-5]]
- FLUX 线：[[flux-1]] · [[flux-1-1-pro]] · [[flux-1-tools]] · [[flux-1-kontext]] · [[flux-1-krea-dev]] · [[flux-2]] · [[flux-2-klein]]
