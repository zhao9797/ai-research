---
title: "Qwen-AgentWorld（首个语言世界模型 LWM：agent 环境仿真）"
org: 阿里巴巴 Qwen
country: China
date: 2026-06
type: paper
categories: [agentic训练, 架构, 后训练, 预训练数据]
url: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B
pdf_url: https://arxiv.org/abs/2606.24597
github_url: https://github.com/QwenLM/Qwen-AgentWorld
downloaded: [qwen-agentworld-readme.md, qwen-agentworld-config.json, qwen-agentworld-blog.md, arxiv-2606.24597-qwen-agentworld.pdf]
---

## 一句话定位
**首个语言世界模型（Language World Model, LWM）**：用 long CoT 预测「给定 agent 动作 + 交互历史 → 下一环境状态」，覆盖 **7 个 agent 交互域**。两个旗号：**Decouple**（当环境模拟器做 Sim RL）+ **Unify**（当 agent 基础模型，世界建模作为 warm-up）。发 35B-A3B 与 397B-A17B 两档（本页按报告 2606.24597 全文整理）。

## 立论
世界模型 = 预测环境动态的核心认知机制；Richens et al. 证明「能跨足够广任务泛化的 agent 必然学到了世界模型」。LLM agent 的环境交互含两半：policy（state→action）与 world model（(state,action)→next state），但研究几乎只做 policy。AgentWorld 补上语言世界建模这块，并探索它如何提升通用 agent。

## 架构（config.json + model card）
- 基座 **Qwen3.5-35B-A3B-Base**；35B 总 / 3B 激活 MoE；hidden 2048；**40 层**；vocab 248320；上下文 **262,144**。
- **混合层布局** `10 ×(3×(Gated DeltaNet→MoE) → 1×(Gated Attention→MoE))`：线性注意力(Gated DeltaNet，V 32/QK 16 头, head_dim 128) 与门控全注意力(16 Q/2 KV, head_dim 256, RoPE 64, θ=1e7) 3:1 交替；MoE 256 专家/8 路由+1 共享(中间维 512)；MTP 1 层。

## 七大域（Table 1：动作 → 观察 / 核心能力）
- MCP：JSON 工具调用 → 工具响应 / 事实世界知识；Search：web 搜索·抽取 → 会话历史 / 事实知识
- SWE：read/edit/bash → 工具输出·diff / 代码执行推理；Terminal：bash·keystrokes → 终端输出 / **长上下文因果推理**
- Android/Web/OS：触控·点击·鼠标键盘 → **UI view hierarchy / accessibility tree**（文本化，非像素）/ 视觉状态推理

## 统一环境轨迹 Schema（§2.2）
- `system_prompt = task_description ⊕ action_space ⊕ initial_state ⊕ demonstrations ⊕ simulation_instruction`（蓝=静态共享 / 红=每轨迹动态注入）
- `turn = (action, observation)`；`trajectory = system_prompt ⊕ [turn₁…turn_T]`
- LWM 目标：ô_{t+1} = f_θ(c, o_≤t, a_≤t)，训练目标为真值 o_{t+1}。

## 预训练数据 + 处理（§3.1）
- **三源（严格不相交）**：① 专用 agent 基础设施（容器化代码/工具沙箱、MCP server、持久 terminal、Android/浏览器/桌面 OS 环境跑在 Ubuntu/macOS/Android VM，自动合成任务并端到端执行 → 主力可复现数据）；② 开放环境交互轨迹（terminal 录制、开源 tool-call 日志、代码库执行 trace，多 agent 清洗管线，捕长尾）；③ 自家 foundation SFT agentic 轨迹（7 域，格式统一）。
- **数据处理**：Trajectory-to-Turn 展开（任一轮都可作预测目标，训练随机取 1 轮/轨迹增多样）；过滤（丢 <2 轮、MCP/SWE 调了未声明工具、GUI 环境失败如缺文件/CAPTCHA/HTTP 错）；**Retry-Cycle Skipping**（跳过"垃圾→错→重试"循环保状态链）、**No-Change Turn Filtering**（GUI 删动作前后无变化轮，防学会无脑复制）。
- **System prompt 模板 = AutoResearch 自动优化**（提示优化当研究问题，optimizer agent 迭代 propose→evaluate→refine，12 并行 run 出 v0–v11 模板：~30 行极简 → ~1100 行规范式；RL 用 v0、CPT 用 v1、SFT 随机 v2–v11 提多样性）。
- 数据量（Table 2）：**SFT 7,094 条 / RL 92,308 条**，平均 19,443 token、13.4 轮（Terminal RL 34,125 最多、SWE 36,734 token/avg 最长）。

## 训练三阶段（§3，"CPT injects, SFT activates, RL sharpens"）
- **CPT**：next-token（非思考）；除环境轨迹外加**专业领域世界知识语料**（工业控制/网安/法律/医疗/金融/时事/百科）→ 支撑零样本构造 7 域之外的新环境；**Turn-Level Information-Theoretic 损失掩码**（掩掉只回显输入的 boilerplate 轮）。
- **SFT**：把 next-state 预测变成显式 thinking pattern；带推理链轨迹 + **拒绝采样 + 质量阈值过滤**。
- **RL（§3.4）**：**GSPO**（group-wise sequence policy optimization）on-policy rollout；**混合奖励 = rubric-based LLM judge + rule-based verifiers**；只用模型生成 token 优化、忽略环境反馈 loss。

## AgentWorldBench（§4）
- 用 5 个前沿模型（含 Claude Opus 4.6）在 Terminal-Bench 1.0/2.0、OSWorld-Verified 等真实交互构建；ground-truth rubric 评 5 维：**Format / Factuality / Consistency / Realism / Quality**；另设 rule-based verifier 做确定性检查。
- 结果：**397B-A17B Overall 58.71（榜首，超 GPT-5.4 58.25、Claude Opus 4.8 56.59）；35B-A3B 56.39**（35B 即与 Opus 4.8 同档，远超同基座 Qwen3.5-35B 47.73）。

## agentic 训练的两种用法（§6，核心贡献）
- **① 解耦——当环境模拟器做 Sim RL**：用 LWM 仿真 4k 个真实 OpenClaw 环境训 policy → Claw-Eval **+4.3**、QwenClawBench **+7.1**；可控仿真（如"对 web_search 隐藏答案"）带来 Tool Decathlon **+12.3**、WideSearch **+3.9**（超真实环境训练）。
- **② 统一——当 agent 基础模型**：仅在**单轮、无工具调用**轨迹上做 LWM RL warm-up，迁移到多轮 tool-calling：Terminal-Bench 2.0 **+6.3**、Claw-Eval **+11.8**、SWE-Bench Pro **+5.2**、BFCL v4 **+9.0**（含完全 OOD 域）。次态预测被内化成"面向未来的 reflection"。

## AI infra / 部署
- SGLang/vLLM `tp=4`、`max-model-len 262144`、`reasoning-parser qwen3`；建议 ≥128K 上下文；输出建议 32K；thinking 模式默认。

## 原始链接
- url: https://huggingface.co/Qwen/Qwen-AgentWorld-35B-A3B · blog: https://qwen.ai/blog?id=qwen-agentworld
- paper: https://arxiv.org/abs/2606.24597 · github: https://github.com/QwenLM/Qwen-AgentWorld · dataset: Qwen/AgentWorldBench

## 本地落盘文件
- ../../../sources/llm/2026/qwen-agentworld-readme.md
- ../../../sources/llm/2026/qwen-agentworld-config.json
- ../../../sources/llm/2026/arxiv-2606.24597-qwen-agentworld.pdf
