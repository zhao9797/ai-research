---
title: "Omni / 多模态生成技术演进调研 (2020 → 2026-H1) · 主汇总"
type: source
tags: [omni, multimodal-generation, text-to-image, image-editing, unified-understanding-generation, any-to-any, video-generation, diffusion, autoregressive, survey]
created: 2026-06-25
updated: 2026-06-25
---

# Omni / 多模态生成技术演进调研 · 主汇总（2020 → 2026-H1）

> 覆盖**视觉/多模态「生成与编辑」模型及其使能方法**：文生图 · 图像编辑/可控生成 · 统一理解+生成 · any-to-any 全模态(omni) · 视频生成 · 全模态中的音频/语音 · 3D · 以及扩散/流/自回归等使能方法。
> 只收**一手官方来源**：arXiv 原文、官方技术报告/system card、官方博客/产品发布、官方 GitHub / HuggingFace / ModelScope model card。**不含第三方解读/二手聚合**。
> 每个工作页按**六维**梳理：`数据 · 训练方法 · 模型架构 · 评测 benchmark · Infra` + 创新影响；所有数字均经**对抗式 verify 逐条对照一手源**（删串列/张冠李戴/杜撰）。

---

## 一、语料统计

- **去重后一手来源**：**~322 条**（**324 个结构化工作页**，按原始 URL 去重）
- **下载原文**：arXiv PDF（gitignored，走本地落盘+HF bucket）+ 官方博客/model card 的 `.md/.html` 快照（随库），见各页 `downloaded:` 与 `sources/omni/<年>/`
- **横向综述**：6 篇 `sections/` + 5 篇模型族 `deep-dive/`
- **质量保证**：每页均经**对抗式 verify 逐条对照一手源**（删串列/张冠李戴/杜撰）；并经一轮 **查漏补缺 review**（补 33 个缺失基石工作如 DiT/MaskGIT/MAR/REPA/AudioLM/3D-GS + 修断链归一化内链）

**按年（页数）**：2020→7 · 2021→25 · 2022→45 · 2023→91 · 2024→69 · 2025→66 · 2026(H1)→21

**按国别（去重）**：美国/西方 ~150 · 中国 ~130 · 欧洲 ~36（FLUX/Stability/CompVis/StyleGAN-XL 等）· 其它（瑞/韩/新/以）少量 —— 中美欧 top 玩家全覆盖

**按类别（去重，单标主类）**：文生图 t2i ~72 · 视频 video ~60 · 使能方法 method ~53 · 编辑 edit ~48 · 统一 unified ~46 · 3D ~19 · 音频 audio ~11 · 全模态 omni ~11 · 基础 foundation 1

---

## 二、怎么读这份调研

从"结论"到"原文"四层：

1. **六大横向章节（核心，先读）** — `sections/`
   - [模型架构演进](sections/architecture.md) — U-Net→DiT→MMDiT→AR/next-scale/masked→统一 omni 骨干；tokenizer/VAE/text-encoder 演进
   - [数据：规模·配比·重标注·过滤](sections/data.md) — LAION 时代 → re-captioning 浪潮 → 分阶段配比 → 版权/安全过滤
   - [训练方法](sections/training.md) — diffusion/flow-matching/AR/masked 目标 · 多阶段 · 偏好对齐(DPO/DDPO/Flow-GRPO/reward) · 蒸馏少步
   - [评测 benchmark](sections/benchmark.md) — FID→CLIPScore→GenEval/DPG/T2I-CompBench→人评/Arena→编辑/视频 bench + 横向数字表
   - [Infra](sections/infra.md) — 训练规模/并行 · tokenizer 工程 · 推理加速 · 闭源黑盒边界
   - [统一理解生成 & any-to-any omni 专题](sections/unified-omni.md) — 三大范式对比
2. **模型族横向对比** — `deep-dive/`
   - [Stable Diffusion → SDXL → SD3 → FLUX 谱系](deep-dive/sd-flux-lineage.md)
   - [中国系文生图/编辑族（CogView·Qwen·Hunyuan·Seedream·Kolors·ERNIE）](deep-dive/chinese-t2i-families.md)
   - [统一/Omni 模型族（Chameleon·Emu·Janus·Bagel·OmniGen·Show-o·VAR）](deep-dive/unified-omni-families.md)
   - [视频生成族（Sora·Veo·Wan·Movie-Gen·Hunyuan·Kling·CogVideoX）](deep-dive/video-generation-families.md)
   - [图像编辑与可控生成族（ControlNet·InstructPix2Pix·Emu-Edit·Kontext·Step1X·Qwen-Edit）](deep-dive/image-editing-control.md)
3. **全量来源索引（按年月，可点开每条）** — [01-INDEX.md](01-INDEX.md)
4. **单工作结构化页** — `2020/`…`2026/`；**下载原文** — `sources/omni/<年>/`

---

## 三、六年主线速览

**2020 — 地基**：扩散三件套 [[ddpm]]（ε-MSE，FID 3.17）/[[ddim]]（确定性少步采样）/[[score-sde]]（连续 SDE+概率流 ODE，FID 2.20）奠定生成式公式；[[taming-transformers-vqgan]] 开辟离散 token 自回归赛道。

**2021 — 引导与潜空间**：[[diffusion-models-beat-gans]] 用 classifier guidance 在 ImageNet 上扩散首超 GAN；[[classifier-free-guidance]] 成为此后所有 T2I 标配旋钮；[[latent-diffusion-ldm]] 把扩散搬进 VAE 潜空间 + cross-attention 文本条件（Stable Diffusion 直系前身）；[[dall-e-1]]/[[glide]]/[[cogview]] 把"文生图"推向大众视野。

**2022 — 文生图大爆发**：[[dall-e-2]]（unCLIP）/[[imagen]]（T5+像素级联）/[[parti]]（自回归）/[[stable-diffusion-1]]（开源引爆）四箭齐发；[[dreambooth]]/[[textual-inversion]]/[[prompt-to-prompt]] 开个性化与编辑先河；[[rectified-flow]]/[[flow-matching]]/[[dpm-solver]]/[[elucidating-edm]] 夯实方法地基；视频 [[make-a-video]]/[[imagen-video]]/[[phenaki]] 起步。

**2023 — 可控、统一、提速三线并进**：编辑可控 [[controlnet]]/[[instructpix2pix]]/[[ip-adapter]]/[[emu-edit]]；质量 [[sdxl]]/[[dall-e-3]](合成 caption)/[[pixart-alpha]]；统一多模态 [[chameleon-cm3leon]]/[[emu-multimodal]]/[[next-gpt]]/[[kosmos-g]]；蒸馏少步 [[consistency-models]]/[[latent-consistency-models]]/[[sdxl-turbo-add]]；偏好对齐 [[diffusion-dpo]]/[[ddpo]]/[[hps-v2]]；视频 [[stable-video-diffusion]]/[[animatediff]]/[[emu-video]]；3D [[zero-1-to-3]]/[[mvdream]]。

**2024 — DiT/MMDiT 化与"统一生成"范式确立**：[[stable-diffusion-3]](MMDiT+rectified flow)/[[flux-1]]/[[hunyuan-dit]]/[[sana]]；自回归/统一 [[chameleon]]/[[transfusion]]/[[show-o]]/[[emu3]]/[[janus]]/[[var]]；视频跃迁 [[sora]]/[[movie-gen]]/[[cogvideox]]/[[kling]]/[[veo-2]]；GPT-4o/[[gemini-2-0-flash-native-image]] 预告"原生多模态生成"。

**2025 — 原生 omni 与中国军团爆发**：产品级原生图像 [[gpt-image-1]]/[[gemini-2-5-flash-image-nano-banana]]；统一旗舰 [[bagel]]/[[janus-pro]]/[[blip3-o]]/[[omnigen2]]/[[ming-omni]]/[[qwen2-5-omni]]；中国文生图/编辑 [[qwen-image]]/[[qwen-image-edit]]/[[seedream-3-0]]/[[seedream-4-0]]/[[hunyuanimage-2-1]]/[[step1x-edit]]/[[flux-1-kontext]]；视频 [[wan-2-1]]/[[wan-2-2]]/[[veo-3]]/[[sora-2]]/[[hunyuanvideo-1-5]]。

**2026-H1 — 全模态推理与极致工程**：[[qwen-image-2-0]]/[[qwen3-5-omni]]/[[ernie-image]]/[[omnigen-ar]]/[[skywork-unipic-3-0]]/[[internvl-u]]/[[flux-2-klein]]/[[gpt-image-2]]/[[seedream-5-0-lite]]/[[reve-2-0]]/[[ideogram-4-0]]/[[nano-banana 系]]，统一"理解—推理—生成—编辑"与端侧亚秒推理成为前沿。

---

## 四、四条贯穿性技术主线（详见各 section）

1. **生成式公式**：DDPM 离散链 → score-SDE 连续 → rectified flow/flow matching"直线"（2024 起 T2I 默认）；与离散 token AR / next-scale / masked 并行、并在统一模型融合。
2. **Backbone**：U-Net → DiT（纯 Transformer）→ MMDiT（文图双流）｜｜ LLM 式 decoder-only AR；2025+ 单骨干承载任意模态。
3. **条件与 tokenizer**：text encoder `CLIP→T5→冻结 MLLM→无外部编码器`；visual `离散 VQ ｜ 连续 KL-VAE ｜ 语义 RAE ｜ next-scale 残差量化`。
4. **后训练**：SFT → 偏好对齐（Diffusion-DPO/DDPO/Flow-GRPO + ImageReward/HPS/PickScore 奖励）→ 蒸馏少步（Consistency/LCM/ADD/MeanFlow），编辑与 in-context 能力从"专用模块"走向"统一指令"。

---

*维护：调研脚本与索引生成器在 `self-wiki/scripts/tmp/`（`build_index_omni.py` 刷新索引、`normalize_wikilinks.py` 归一化内链）。*
