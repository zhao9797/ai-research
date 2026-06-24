---
title: "Kimi K2.6（月之暗面：原生多模态 agentic，1T MoE，agent swarm）"
org: 月之暗面 Moonshot AI
country: China
date: 2026-06
type: model-card
categories: [架构, AI infra, 后训练, agentic训练]
url: https://huggingface.co/moonshotai/Kimi-K2.6
github_url: https://github.com/MoonshotAI/Kimi-K2
downloaded: [kimi-k2.6-readme.md, kimi-k2.6-config.json, kimi-k2.6-blog.md, arxiv-2602.02276-kimi-k2.5.pdf]
---

## 一句话定位
开源**原生多模态 agentic** 模型，主打 long-horizon coding、coding-driven design、主动自主执行与 **agent swarm 群体编排**；1T MoE，K2.5 之后迭代。

## 架构（model summary + config.json）
- MoE，**总参 1T / 激活 32B**；**61 层**（含 1 dense 层）；attention hidden 7168；MoE 每专家中间维 2048。
- 64 注意力头，**MLA**；**384 专家，每 token 选 8，1 共享专家**；激活函数 SwiGLU；vocab 160K；上下文 **256K**。
- **视觉编码器 MoonViT（400M）** → 原生多模态（图、视频输入）。
- **Native INT4 量化**（同 Kimi-K2-Thinking 方案）。架构与 K2.5 一致，部署可直接复用。

## 数据 / 训练（K2.6 card 略，以下承 K2.5 技术报告 2602.02276 + K2 base）
- **基座 Kimi K2**：1.04T 总 / 32B 激活 MoE，384 专家/8 激活（稀疏度 48），**MuonClip 优化器 + QK-Clip** 稳训，预训练 **15T 高质量文本 token**。
- **K2.5 原生多模态联合预训练**：在 K2 上加约 **15T 文本+视觉混合 token**；关键发现——**全程等比例混合(早融合、低视觉占比)优于后期高占比**（Table 1：Early 10:90 最佳）。视觉编码器 **MoonViT-3D**（native 分辨率 + NaViT packing；4 连续帧→4× 时序压缩，视频在同上下文长 4×；SigLIP-SO-400M 初始化，参数与图像共享）。
- **三阶段**（Table 3）：ViT 训练（1T，seq 4096，alt-text/合成caption/grounding/OCR/video）→ 联合预训练（15T，seq 4096，+文本/知识/interleaving/video/OS 截图）→ 联合长上下文中训练（500B→200B，seq **32768→262144** YaRN，高质量文本+多模态/长文/长视频/long-CoT）。
- **训练 infra**：承 K2；**Decoupled Encoder Process (DEP)**（Balanced Vision Forward + Backbone Training + Vision Recomputation）解决视觉编码器在 PP Stage-0 的负载/显存波动，**多模态训练效率达纯文本的 90%**。

## RL / 后训练（承 K2.5 报告 2602.02276）
- **SFT**：承 K2 流程，用 K2 / K2-Thinking + 专有专家模型合成高质量候选 + 人工标注 + 多级验证。
- **Zero-Vision SFT**：只用文本 SFT 即激活视觉 agentic 能力（图像操作经 IPython 程序化代理）；得益于联合预训练的强视觉-文本对齐，泛化优于 text-vision SFT。
- **联合多模态 RL**：按**能力维度**（知识/推理/编码/agentic）而非模态组织；outcome-based 视觉 RL（视觉 grounding·计数 / 图表文档 / 视觉关键 STEM）**反哺文本**（MMLU-Pro 84.7→86.4、GPQA-D 84.3→86.4、LongBench v2 56.7→58.9）。
- **策略优化**：token 级裁剪（log-ratio 落 [α,β] 外则梯度置零，按 log-ratio 控 off-policy 漂移而非 PPO 式按优势裁剪），**MuonClip 优化器**；区别于 K1.5 算法。
- **混合奖励**：可验证任务规则 outcome reward + **budget-control 省 token reward** + 通用 **GRM（生成式奖励模型）** + 视觉任务专用奖励（grounding 用 IoU/F1、分割用 mask IoU、OCR 用编辑距离）；多 GRM rubric 防 reward hacking。
- **Toggle（token 高效 RL）**：在 budget-limited 相与 standard-scaling 相间每 m 轮交替（budget=正确响应长度 ρ 分位），**输出 token 降 25~30% 而性能几乎不掉**。
- **Agent Swarm / PARL（并行 agent RL）**：可训练 orchestrator + **冻结 subagents（不进优化目标，规避 credit assignment 与训练不稳）**；PARL reward = λ₁·r_parallel(抗串行塌缩) + λ₂·r_finish(抗虚假并行) + r_perf，λ 退火到 0；CriticalSteps 度量；宽搜索延迟降至 1/4.5、item-F1 72.8→79.0。
- **推理模式**：preserve_thinking（多轮保留完整 reasoning）+ interleaved thinking + 多步 tool call；Thinking(temp 1.0) / Instant(temp 0.6, `thinking:disabled`)，top_p 0.95。

## agentic
- **Agent Swarm**：横向扩到 **300 个 sub-agents、4000 步**协同（**K2.5 为 100/1500，K2.6 翻 3×**），动态分解为并行领域专精子任务，一次自主运行产出文档/网站/幻灯/表格。官方实证：12 小时 14 轮把 Zig 推理吞吐从 ~15→~193 tok/s(超 LM Studio 20%)；按 CV 派 100 子 agent 匹配 100 个岗位并各出定制简历；K2.6-backed agent 自主运维 5 天(监控/事件响应/全周期处理)。
- 7×24 常驻后台 agent（自主管日程、跑代码、跨平台编排）；coding-driven design（prompt/视觉 → 生产级界面 + 动画）；long-horizon coding 跨 Rust/Go/Python。
- 最佳 agent 框架：Kimi Code CLI。

## Benchmark（thinking 模式；vs GPT-5.4 / Claude Opus 4.6 / Gemini 3.1 Pro / K2.5）
- **Agentic**：HLE-Full(w/tools) **54.0**；BrowseComp 83.2（**swarm 86.3**）；DeepSearchQA f1 **92.5** / acc **83.0**；WideSearch 80.8；Toolathlon 50.0；MCPMark 55.9；OSWorld-Verified 73.1；APEX-Agents 27.9。
- **Coding**（10 次平均）：SWE-Bench Verified **80.2** / Multilingual 76.7 / Pro 58.6；Terminal-Bench 2.0 66.7；LiveCodeBench v6 **89.6**；SciCode 52.2；OJBench 60.6。
- **推理&知识**：AIME 2026 96.4；HMMT Feb 2026 92.7；GPQA-Diamond 90.5；HLE-Full 34.7（text-only w/tools 55.5）。
- **视觉**：MMMU-Pro 79.4；MathVision 87.4（w/python 93.2）；V*(w/python) 96.9。
- 多数项较 K2.5 大幅提升（如 BrowseComp 74.9→83.2、MCPMark 29.5→55.9、Toolathlon 27.8→50.0）。

## AI infra / 部署
- vLLM / SGLang / KTransformers；`transformers>=4.57.1,<5`；native INT4；OpenAI/Anthropic 兼容 API（platform.moonshot.ai）。

## 原始链接
- url: https://huggingface.co/moonshotai/Kimi-K2.6 · blog: https://www.kimi.com/blog/kimi-k2-6.html
- 同代另有 **Kimi-K2.7-Code**、**Kimi-Linear-48B-A3B**；K2.5 报告 arXiv 2602.02276
- 许可 Modified-MIT

## 本地落盘文件
- ../../../sources/llm/2026/kimi-k2.6-readme.md
- ../../../sources/llm/2026/kimi-k2.6-config.json
- ../../../sources/llm/2026/arxiv-2602.02276-kimi-k2.5.pdf （K2.5 技术报告，K2.6 继承其训练方法）
