---
title: "FLUX.2"
org: "Black Forest Labs"
country: EU
date: "2025-11"
type: blog
category: t2i
tags: [flux, rectified-flow, mmdit, flow-matching, image-editing, multi-reference, vae, text-rendering, open-weights]
url: "https://bfl.ai/blog/flux-2"
arxiv: ""
pdf_url: ""
github_url: "https://github.com/black-forest-labs/flux2"
hf_url: "https://huggingface.co/black-forest-labs/FLUX.2-dev"
modelscope_url: ""
project_url: "https://bfl.ai/blog/flux-2"
downloaded: [flux-2--blog.md, flux-2--vae-techblog.md, flux-2--github-readme.md, flux-2--hf-modelcard.md, flux-2--hf-diffusers-blog.md, flux-2--diffusers-quant-doc.md, flux-2--prompt-upsampling-doc.md]
created: 2026-06-25
updated: 2026-06-25
---

## 一句话定位
FLUX.2 是 Black Forest Labs（BFL）2025 年 11 月发布的第二代旗舰图像生成/编辑模型族，把**文生图 + 单参考编辑 + 最多 10 张参考图的多图编辑**统一进一个 latent rectified-flow（整流流）transformer；最大开源档 **FLUX.2 [dev] 为 32B 参数**，用 **Mistral-3 24B 视觉-语言模型当文本编码器**，配一颗**从零重训、128 通道/token 的新 VAE**（rFID 0.1124）。人评中相对一众开源 SOTA 取得文生图 66.6% / 多参考 63.6% / 单参考 59.8% 的胜率，并显著强化了**文字渲染、4MP 高分辨率编辑与世界知识**。

## 背景与定位
FLUX.1（2024，[[flux-1]] 系）证明了流匹配 transformer 作为开源图像基座的潜力，其 FLUX.1 [dev] 是全球下载/喜欢数最高的开源图像模型；FLUX.1 Kontext（[[flux-1-kontext]]）则把"in-context 编辑"做进同一架构。FLUX.2 的定位不是 FLUX.1 的 drop-in 替换，而是**全新架构 + 从零预训练**的新一代，目标从"创意 demo"转向"真实生产工作流"：品牌一致性、结构化提示遵循、复杂排版（infographics/UI/meme）、稳定光照与 logo。

技术脉络上 FLUX.2 仍属 **Latent Diffusion / 流匹配**一支（[[latent-diffusion-ldm]] → [[rectified-flow]] → MMDiT，对应 [[sd3]] 的 Scaling Rectified Flow Transformers 路线），但有两条关键升级：(1) 用一个**大 VLM（Mistral-3 24B）单编码器**替换 FLUX.1 的双文本编码器（CLIP+T5），引入真实世界知识与上下文理解；(2) **从零重训 latent space**，瞄准作者提出的"可学习性-质量-压缩"三难（Learnability–Quality–Compression trilemma），同时改善重建保真度与生成可学习性。BFL 称这是迈向"统一感知、生成、记忆、推理的多模态模型"的一步。"open core"策略：开源 [dev]/[klein] + 闭源 [pro]/[flex] API 并行。

## 模型架构
**整体**：latent flow matching（rectified flow）单一架构，文生图与编辑共用一套权重。文本/视觉条件来自 **Mistral-3 24B 参数 VLM**（仓库与 prompt-upsampling 文档明确为 `Mistral-Small-3.2-24B-Instruct-2506`；HF diffusers 博客在描述实现时写作 "Mistral Small 3.1"——以 BFL 官方仓库口径为准，统一记为 Mistral-3 24B 级 VLM）。VLM 同时承担文本编码与（编辑场景下的）参考图理解，带来世界知识与空间逻辑；rectified flow transformer 负责空间关系、材质属性与构图。

**条件注入与序列**：单文本编码器，`max_sequence_length = 512`；不取末层单层输出，而是**堆叠中间层输出**作为 prompt embedding（已知中间层更有利，arXiv:2505.10046）。编辑时多张参考图（≤10）一并作为条件输入，可用序号（image 1/2）或自然语言（the kangaroo）引用。

**DiT backbone（相对 FLUX.1 的具体改动，来自 HF diffusers 工程博客）**：沿用 **MMDiT + 并行 DiT** 双结构——前段 "double-stream"（图像/文本分流，仅在 attention 处汇合）+ 后段 "single-stream"（拼接后单流）。关键变更：
- **共享调制**：时间与 guidance 信息（AdaLayerNorm-Zero 调制参数）在所有 double-stream / single-stream 块间**各自共享一套**，不再每块独立（更省参/算力，DiT-Air 思路，arXiv:2503.10618 的 global modulation）。
- **全程无 bias**：attention 与 FFN 子层一律不带 bias 参数。
- **更彻底的并行块**：single-stream 块把 attention QKV 投影与 FF 输入投影也融合，形成"fully parallel transformer block"（ViT-22B 式），MLP 用 **SwiGLU** 激活。
- **块配比偏向单流**：**8 个 double-stream + 48 个 single-stream**（FLUX.1 为 19/38）。参数分布上 FLUX.1[dev]-12B 约 54% 参数在双流块，而 **FLUX.2[dev]-32B 仅约 24% 在双流块、约 73% 在单流块**。
- 更好的**分辨率相关 timestep 调度**（resolution-dependent timestep schedules）。

**VAE（FLUX.2 - VAE，单独 Apache-2.0 开源，附 representation-comparison 研究博客）**：从零重训的新 autoencoder `AutoencoderKLFlux2`，是所有 FLUX.2 流匹配 backbone 的基础。核心思路是在 SD/FLUX.1 的"信息瓶颈 + 感知/对抗损失"之上，引入**语义正则（REPA / DINOv2 对齐式）**以提升潜空间可学习性，同时**放大潜维度换重建保真**：相比 SD-VAE，FLUX.2 VAE 潜维度放大 8×、相比 FLUX.1 放大 2×。在 2×2 patch、256-token 固定序列设定下，每 token 通道数：**SD 16 / FLUX.1 64 / FLUX.2 128 / RAE 768**。支持最高 **4MP（兆像素）**分辨率的生成与编辑，并支持灵活输入/输出宽高比。

**参数档位**（仓库 model overview）：
- **FLUX.2 [pro]**（闭源 API）：旗舰画质，对标顶级闭源模型。
- **FLUX.2 [flex]**（闭源 API）：开放 steps / guidance 等参数控制，擅长文字与细节。
- **FLUX.2 [dev]**：32B 开源权重，guidance-distilled（蒸馏过 guidance），由 base 模型派生；当前最强开源图像生成+编辑单 checkpoint。
- **FLUX.2 [klein]**（size-distilled；2026-01-15 正式放出 4B/9B/9B-KV/4B-Base/9B-Base 系列）：从 base 模型尺寸蒸馏，亚秒级、消费级 GPU 可跑（4B 约 8GB VRAM）。**仅 4B/4B-Base 为 Apache-2.0**，9B 各档为 FLUX 非商业许可（仓库 README 模型表）。distilled 档 4-step，base 档 50-step——属 FLUX.2 后续衍生，非本次 11 月主发布范畴（11 月博客原话仅预告 klein "coming soon"、Apache-2.0）。

## 数据
BFL 未公开 FLUX.2 的训练数据规模、来源配比与图文对数量（"new pre-training done from scratch"，但无量化披露）。可确证的数据/安全侧信息（来自 HF model card 的 Risks 章节）：
- **预训练数据过滤**：对多类 NSFW 与已知 CSAM 进行过滤；与 Internet Watch Foundation 合作剔除已知 CSAM。
- **后训练安全微调**：多轮针对 T2I 与 I2I 攻击的定向微调，抑制特定行为/概念以防生成 CSAM/NCII。
- **第三方对抗评测**：发布前做最终第三方评测（合计 prompts n≈2,800），分 (i) 纯文本、(ii) 单参考图+文本、(iii) 多参考图+文本三类，结论是 FLUX.2 [dev] 对违规输入的抵御力高于主流开源模型。
- VAE 研究博客中的可学习性对照实验用的是 **ImageNet 256×256**（DiT-XL backbone、batch 256、lr 1e-4、EMA 0.9999），但这是分析性实验，非 FLUX.2 主模型训练数据。

主模型的美学过滤、re-captioning、合成数据占比等：**未披露**。

## 训练方法
- **训练目标**：conditional flow matching / rectified flow（整流流），VAE 研究博客给出 CFM 损失形式 `L = E ‖v_θ((1-t)E(u)+tε; t) - (ε - E(u))‖²`。
- **timestep 采样**：作者系统比较了 shifted-uniform、shifted logit-normal、plateau logit-normal 三种训练时刻分布与多组 shift 系数 α∈{1.00,1.78,2.95,4.63,6.93}；结论是 **logit-normal / plateau-logit-normal 一致优于 shifted-uniform**，且 shift 参数随潜空间维度变化（FLUX.2 VAE 训练最优 shift≈4.63，采样最优≈6.93）。FLUX.2 主模型采用"更好的分辨率相关 timestep 调度"。
- **VAE 训练**：像素回归 + 感知损失 + 对抗损失（GAN）+ KL 正则的经典组合，叠加 **REPA 式语义对齐正则**提升可学习性（研究博客明确把 DINOv2/REPA 思路整合进 VAE 训练）。
- **多阶段 / 蒸馏**：
  - **FLUX.2 [dev] 经 guidance distillation**（guidance-distilled，HF card "Key Features" 第 3 条），因此推理无需 CFG 双前向、用单一 `guidance_scale`（默认 4）即可。
  - **FLUX.2 [klein] 经尺寸蒸馏（size-distilled）**自 base 模型；其中 distilled 档为 4-step（step-distilled + guidance-distilled），base 档为 50-step。
  - 安全后训练（targeted safety fine-tuning）多轮。
- **RL / 偏好对齐（DPO/RLHF/reward model）**：BFL 一手源**未披露**采用了哪种偏好对齐方法，仅说做了多轮安全/能力微调；不臆造。
- 关键超参（学习率、总步数、batch、预训练算力）：主模型**未披露**（仅 VAE 分析实验给出了上述 ImageNet 设定）。

## Infra（训练 / 推理工程）
**训练算力/并行/吞吐**：**未披露**。仓库仅说推理代码在 **GB200（CUDA 12.9 / Python 3.12）**上测试。

**推理工程（来自 HF diffusers 博客与 BFL 仓库 docs，第一手）**：
- FLUX.2 [dev]（32B DiT + Mistral-3 24B 文本编码器 + VAE）bf16 全量同载 **>80GB VRAM**；即便 H100-80G 也装不下三件套同时，需 `enable_model_cpu_offload()` 顺序换入；H200/B200 可全装。
- **量化（与 NVIDIA / ComfyUI / HF diffusers 合作）**：bitsandbytes **NF4 4-bit**（DiT+文本编码器）可在 **24–32GB（RTX 4090/5090）**运行；DiT 4-bit + **remote text-encoder**（文本嵌入在云端 bf16 算好，本地只载 DiT）最低 **~18GB VRAM**；DiT 4-bit + 文本编码器 4-bit + cpu-offload **~20GB**。
- **group_offloading**（leaf_level）可压到 **8GB VRAM**（需 ~32GB RAM，或 `low_cpu_mem_usage=True` 降到 ~10GB RAM）。8-bit 量化适合 40–48GB GPU。
- **采样步数 / guidance**：默认 50 步、`guidance_scale=4`；**28 步是质量/速度的好折中**；编辑多参考时示例用 `guidance_scale=2.5`。
- **可变步数（[flex] 档）**："steps" 参数显式 trade-off：6 / 20 / 50 步分别在排版准确度、细节与延迟间取舍。
- **prompt upsampling**：用 Mistral-Small-3.2-24B（本地，与文本编码同模型）或 OpenRouter API 扩写复杂/推理型 prompt（meme、含图内指令、代码/数学可视化）。
- **部署形态**：BFL Playground / BFL API；开源权重经 HF、ComfyUI、Diffusers 本地运行；多家云（FAL/Replicate/Together/Cloudflare/DeepInfra 等）提供 [dev] 端点。**内容溯源**：[pro] API 对输出加**密码学签名的 C2PA 元数据**；[dev] 参考推理代码内置**像素层水印示例**（可选 invisible-watermark 库），并附 C2PA 标准链接（model card Risks 第 6 条 / 仓库 README）。HF 上 FLUX.2-dev "月下载量 307,427"（model card 截图当时）。

## 评测 benchmark（把效果讲清楚）
**注意**：BFL 一手源**未公布** FID / GenEval / DPG-Bench / T2I-CompBench 等自动指标，主模型对外只给**人评胜率**；自动指标仅出现在 VAE 分析实验里（ImageNet，针对潜空间而非整模型）。以下数字均来自已落盘的一手源，未报告维度明确标注。

**人评（FLUX.2 vs 主流开源权重模型，研究博客 Figure 3，胜率 win rate）**：
- 文生图 text-to-image：**66.6%**（胜率最高）
- 多参考 multi-reference 编辑：**63.6%**
- 单参考 single-reference 编辑：**59.8%**

BFL 自评：开源权重档 FLUX.2 [dev] 在文生图、单参考编辑、多参考编辑三项上"大幅领先所有开源替代品"，并称 [pro] 在画质上对标顶级闭源模型，但速度更快、成本更低。

**VAE 重建指标（ImageNet 验证集，研究博客 Table 1；反映潜空间质量，非整模型）**：

| AE | LPIPS↓ | SSIM↑ | PSNR↑ | rFID↓ | 通道/token |
|---|---|---|---|---|---|
| RAE | 1.6737 | 0.4962 | 18.83 | 0.6107 | 768 |
| SD | 0.9519 | 0.6976 | 25.05 | 0.6451 | 16 |
| FLUX.1 | 0.3380 | 0.8893 | 31.13 | 0.1761 | 64 |
| **FLUX.2** | **0.2668** | **0.9038** | **31.46** | **0.1124** | **128** |

**可学习性（gFID，DiT-XL 在各 VAE 潜空间训练）**：FLUX.2 gFID 3.70（最优 shift），优于 FLUX.1 (10.13) 与 SD (7.73)，接近纯语义型 RAE (3.10) —— 即 FLUX.2 VAE 在**同时改善重建保真度的前提下**把可学习性拉到接近 RAE 的水平（FLUX.1→FLUX.2：gFID -63.4%）。

**关键消融结论（研究博客）**：(1) REPA 语义对齐对所有 VAE 一致提升生成质量；(2) 训练/采样 timestep shift 选择影响极大（FLUX.2 最差→最优 shift 间 FID 相对变化达 73.3%）；(3) logit-normal / plateau-logit-normal 优于 shifted-uniform。

人评 ELO/Arena、GenEval、DPG-Bench、T2I-CompBench、HPSv2、ImageReward、PickScore、编辑专项（GEdit/MagicBrush）等：**一手源未报告**。

## 创新点与影响
**核心贡献**：
1. **大 VLM 单编码器**：用 Mistral-3 24B VLM 替换 FLUX.1 的 CLIP+T5 双编码器，把世界知识/上下文理解直接灌进图像生成，提升复杂结构化提示遵循、文字渲染与场景合理性，并天然支撑多参考图理解。
2. **从零重训的 128 通道 VAE**：以"可学习性-质量-压缩三难"为框架，用语义正则（REPA/DINOv2 式）+ 放大潜维度，**同时**改善重建保真（rFID 0.1124，SOTA 中最佳）与生成可学习性——把"高保真编辑需求"与"可学习潜空间"两个常冲突的目标统一。
3. **统一文生图 + 单/多参考编辑（≤10 图）单 checkpoint**，4MP 高分辨率，免微调即可做角色/产品/风格一致性。
4. **更高效的 DiT 设计**：共享调制 + 无 bias + 全并行单流块 + SwiGLU + 偏向单流的块配比，在 32B 规模上提升 compute 效率。
5. **完整产品矩阵 + 开放性**：[pro]/[flex]（API）/[dev]（32B 开源，FLUX 非商业许可）/[klein]（蒸馏小模型，仅 4B 档 Apache-2.0）+ 单独开源的 Apache-2.0 VAE，配 NVIDIA/ComfyUI/HF 的消费级量化方案（最低 8GB VRAM）。

**影响**：作为 2025 年末最强开源图像生成+编辑权重，FLUX.2 [dev] 迅速成为社区基座（HF 上 70+ adapters、27 finetunes、13 quantizations、100+ Spaces）；其 VAE 研究把"潜空间可学习性"这一问题（REPA-E、RAE 等学术线）正式带入工业级旗舰模型，并预告 FLUX.3 将探索"不依赖外部特征网络（如 DINOv2）"的可学习性增强路径。

**已知局限**：(1) 重建-可学习性 gap 仍在——更牺牲重建的 VAE 仍更可学习，BFL 自承需继续缩小；(2) 32B 全量推理对显存要求高（>80GB），消费级需重度量化/offload，速度受影响；(3) 训练数据、算力、偏好对齐方法等工程细节几乎全部未公开；(4) 自动 benchmark 缺失，对外只有自评人评胜率，第三方可复现性弱。

## 原始链接
- blog（主发布，最权威）: https://bfl.ai/blog/flux-2
- research blog（VAE / 潜空间分析，含架构与人评数字）: https://bfl.ai/research/representation-comparison
- github（参考推理代码）: https://github.com/black-forest-labs/flux2
- hf model card（FLUX.2 [dev]，含安全披露/用法）: https://huggingface.co/black-forest-labs/FLUX.2-dev
- hf diffusers 工程博客（架构改动/量化/LoRA 细节）: https://huggingface.co/blog/flux-2
- github docs - 量化/低显存推理: https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_dev_hf.md
- github docs - prompt upsampling: https://github.com/black-forest-labs/flux2/blob/main/docs/flux2_with_prompt_upsampling.md
- klein 后续发布（2026-01，补充）: https://bfl.ai/blog/flux2-klein-towards-interactive-visual-intelligence
- 文档/Prompting 指南: https://docs.bfl.ai/flux_2/ ・ https://docs.bfl.ai/guides/prompting_guide_flux2

## 本地落盘文件
- ../../../sources/omni/2025/flux-2--blog.md  （BFL 主发布博客快照）
- ../../../sources/omni/2025/flux-2--vae-techblog.md  （representation-comparison 全文，含 Table 1 / Figure 3 数字与架构）
- ../../../sources/omni/2025/flux-2--github-readme.md  （flux2 仓库 README，含档位表/参数/News）
- ../../../sources/omni/2025/flux-2--hf-modelcard.md  （FLUX.2-dev model card，含安全披露）
- ../../../sources/omni/2025/flux-2--hf-diffusers-blog.md  （HF diffusers 工程博客，DiT/VAE/文本编码器改动）
- ../../../sources/omni/2025/flux-2--diffusers-quant-doc.md  （低显存/量化推理 doc）
- ../../../sources/omni/2025/flux-2--prompt-upsampling-doc.md  （prompt upsampling doc，确认 Mistral-Small-3.2-24B）
