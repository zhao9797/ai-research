---
title: Seed2.0（字节跳动 Seed 通用智能体模型系列）
org: 字节跳动 ByteDance Seed
country: 中国
date: 2026-02
type: model-release
categories: [agentic, multimodal, post-training, eval, llm]
url: https://seed.bytedance.com/en/seed2
pdf_url: https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2/0214/Seed2.0%20Model%20Card.pdf
github_url: ""
downloaded: [files/seed-2.0-model-card.pdf]
---

# Seed2.0

## 一句话定位
字节跳动 Seed 团队 2026-02-14 正式发布的通用智能体模型系列（Pro / Lite / Mini 三档），主打大规模线上生产部署下的用户体验、原生多模态理解与长时程 Agent 能力；以 Doubao-Seed-2.0-pro 形式上线火山引擎/BytePlus。这是本资料库 ByteDance Seed 方向的首条收录（此前目录完全缺失字节）。

## 摘要
Seed2.0 是 Seed 模型家族（Seed1.6/1.8、Seed1.5-VL、Seed-OSS、Seed-Coder、Seed Diffusion、Seed-Prover）的新一代通用模型，定位为「面向真实世界复杂度」的智能体基座。官方 Model Card 强调四点设计优先级：稳健的视觉/多模态理解、快速灵活推理（三档尺寸）、可靠的复杂指令执行、流畅编码协助；并把能力上限从竞赛级推理推向研究级任务（Erdős 问题、科学编码）。官方建立四维评测框架：科学发现（Science Discovery）、Vibe Coding、上下文学习（Context Learning）、真实世界任务（Real-World Tasks）。截至 2026-02-16，Seed 在 LMSYS Chatbot Arena 文本榜（Overall）第 6、视觉榜第 3。官方坦承与国际前沿仍有差距：编码（SWE-Evo、NL2Repo）逊于 Claude，长尾知识（SuperGPQA、SimpleQA-Verified）逊于 Gemini。

Seed2.0 Lite 于 4 月底升级为 Seed 家族首个全模态理解模型，原生统一理解 video/image/audio/text。

## 关键技术细节（带数字）
> 重要诚实说明：Seed2.0 官方 Model Card（11 页）属于**部署/评测/智能体能力**导向，**未披露任何预训练架构数字**（无总参/激活参、层数、隐藏维、专家数、训练 token、算力、并行、精度、tokenizer、RL 算法名）。以下为官方明确给出的可验证数字。

**系列与可用性**
- 三档：**Seed2.0 Pro / Lite / Mini**。Pro 主打长链推理与复杂工作流鲁棒性；Lite 平衡质量与速度（生产级通用）；Mini 主打推理吞吐与部署密度（高并发、批量生成）。
- 模型 ID：**Doubao-Seed-2.0-pro**；火山引擎方舟（Ark）接入，亦提供 BytePlus API（model id seed-2-0-pro）。

**API 定价（官方 Table 1，USD / 1M token，prefill / decode）**
- Seed2.0 Pro：**$0.47（¥3.41）/ $2.37（¥17.04）**
- Seed2.0 Lite：**$0.09（¥0.64）/ $0.53（¥3.83）**
- Seed2.0 Mini：**$0.03（¥0.22）/ $0.31（¥2.24）**
- 对照：GPT-5.2 High $1.75/$14.00；Claude-Opus-4.5-thinking $5.00/$25.00；Gemini-3-Pro $2.00–4.00/$12.00–18.00；Claude-Sonnet-4.5-thinking $3.00/$15.00；GPT-5.0-mini High $0.25/$2.00；Gemini-3-Flash High $0.50–1.00/$3.00。官方称 Seed2.0 价格约为前沿模型的 1/10 量级。

**Arena 排名（as of 2026-02-16）**：LMSYS Text Arena Overall 第 6，Vision Arena 第 3。

**评测对标对象**：GPT-5.2 High、Claude-Sonnet-4.5、Claude-Opus-4.5、Gemini-3-Pro High、Gemini-3-Flash High。

**评测基准覆盖（节选）**
- 基础语言/推理：AIME 2025、HMMT 2025、BeyondAIME、IMOAnswerBench、AetherCode、LiveCodeBench(v6)、Codeforces Elo（2025.6–12 题集）、GPQA Diamond、PhyBench、ARC-AGI-1/2、MMLU-Pro、SuperGPQA 等。
- 长尾专业知识：自建 **LPFQA**（专业论坛长尾问答）、**Encyclo-K**（书本级知识，支持 zero-shot 与 few-shot ICL，用于探测预训练/后训练阶段知识获取）、**HLE-Verified**（人工复核版 HLE）。
- 智能体五维：Coding Agents、Search Agents、Tool Use、GUI Agents、Deep Research（含 Terminal-Bench、SWE-Bench/Multi-SWE-Bench/SWE-Bench Pro/SWE-Evo、BrowseComp、τ²-Bench、BFCL-v4、MCP-Mark、VitaBench、Minedojo-Verified、MM-BrowseComp 等；Trae In-House Bench 覆盖前后端生产场景）。
- 高价值真实任务四维：Scientific Discovery（含自建 Ainstain Bench、BABE）、Vibe Coding、Context Learning、Real-World Tasks。

**生产使用画像（中国大陆 MaaS，官方 Figure 1–2）**
- 行业流量：互联网占绝对主导，消费电子/金融/新零售/商业服务次之；制造/汽车/通信各 <1%。
- 场景：非结构化信息处理分析占最大单一份额；教育、内容创作、搜索推荐次之。
- Agentic coding 画像：前端开发请求占主导；前端语言（JS/TS/CSS/HTML）占多数；框架 **Vue.js 领先（>3× React）**（反映中国大陆生态）；任务类型以 bug fixing 为首，refactoring、文档其次。

## 同期 ByteDance Seed 2026 H1 其它发布（官方博客，供索引）
- Seed1.8（A Generalized Agentic Model，官方发布）
- Seed Prover 1.5（数学推理，新型 agentic 架构）
- Dola-Seed-2.0-Preview（Arena 发布，2026-02-16）
- Seedream 5.0 Lite（图像，2026-02-13）/ Seedance 2.0（视频，2026-02-12）/ Seed3D 2.0（2026-04-23）
- Seed Full-Duplex Speech LLM（全双工语音，2026-04-09）
- 「Dynamic Linear Attention」（arXiv 2606.10650，ICML 2026，ByteDance Seed × UMich，多状态线性注意力动态记忆框架 DLA）

## 原始链接
- 官方 Seed2.0 页：https://seed.bytedance.com/en/seed2
- 官方 Model Card PDF：https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2/0214/Seed2.0%20Model%20Card.pdf
- 官方技术博客：https://seed.bytedance.com/en/blog/seed2-0-%E6%AD%A3%E5%BC%8F%E5%8F%91%E5%B8%83
- Seed 博客总览：https://seed.bytedance.com/en/blog

## 本地落盘文件
- files/seed-2.0-model-card.pdf（官方 Model Card，11 页）
