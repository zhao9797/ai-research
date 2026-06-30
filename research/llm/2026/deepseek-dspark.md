---
title: "DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation"
org: DeepSeek (深度求索) · 北京大学
country: China
date: 2026-06
type: paper
categories: [AI infra, 架构]
url: https://github.com/deepseek-ai/DeepSpec
pdf_url: https://github.com/deepseek-ai/DeepSpec/raw/main/DSpark_paper.pdf
github_url: https://github.com/deepseek-ai/DeepSpec
downloaded: [dspark-paper.pdf, deepspec-readme.md]
---

## 一句话定位
DeepSeek 的投机解码（speculative decoding）新框架：用"半自回归 draft + 置信度调度验证"在 [[llm/2026/deepseek-v4-technical-report|DeepSeek-V4]] 生产服务里取代 MTP-1，匹配吞吐下把单用户生成速度提 57%–85%；同时开源 DSpark 权重与 DeepSpec 训练代码库（含 Eagle3 / DFlash / DSpark 三算法）。

## 摘要
DSpark 是 DeepSeek-AI 与北京大学合作的投机解码工作（论文 *DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation*，Xin Cheng / Xingkai Yu / Chenze Shao / Jiashi Li / Yunfan Xiong 等共一，2026-06）。投机解码靠"轻量 draft 模型提议一段 token、target 模型一次前向并行验证、按 rejection sampling 接受最长合规前缀"无损加速推理，瓶颈在 draft 设计：自回归 drafter（如 Eagle3）质量高但 draft 延迟随块长线性增长，只能用浅网络 + 短块；并行 drafter（如 DFlash）单次前向出整块、延迟几乎与块长无关，却因各位置独立预测缺乏 token 间依赖而出现 **suffix decay（后缀接受率快速衰减）**，且对长块"无差别全验证"在高并发下浪费 batch 容量、压垮吞吐。DSpark 用两个互补机制破局：**半自回归生成**（重型并行 backbone + 轻量序列 head 注入块内依赖，缓解后缀衰减且几乎不加延迟）与**置信度调度验证**（confidence head 估计逐位存活概率 + 硬件感知调度器按实时引擎吞吐曲线动态裁剪验证长度，把 target 算力只投给正期望收益的 token）。离线在 Qwen3-4B/8B/14B、Gemma4-12B 上 accepted length 显著超 Eagle3 / DFlash；在线接入 V4-Flash/Pro preview 生产引擎后，相对 MTP-1 在匹配吞吐下提速 57%–85%，并把"严苛交互性 SLA"这一原先不可达的区间纳入可服务范围，外推服务 Pareto 前沿。团队开源 DSpark 权重 + **DeepSpec**（算法驱动的投机解码训练库，MIT）。

## 关键技术细节

### 架构（drafter）
- **半自回归（semi-autoregressive）= 并行 backbone + 序列 head**。并行阶段沿用 DFlash backbone（单次前向出全块 hidden ℎ₁..ℎ_γ 与 base logits U₁..U_γ；O(1) draft 延迟）；仅做一处改动——把 anchor 本身当第一个预测位（γ 个输入 = anchor + γ−1 个 mask → γ 个 draft logit），省算力。
- **序列阶段**给 base logit 叠加"前缀相关的转移偏置" B_k(x₀,x_<k,x_k)，按因果分解 p_k(v|x₀,x_<k)=softmax(U_k(v)+B_k(...)) 形成块内 causal 分布；推理时序列 head 从左到右采样。两种实例：
  - **Markov head（默认）**：B 只依赖前一 token，低秩分解 B=W₁W₂（W₁∈R^{V×r} 当查表、W₂∈R^{r×V} 当投影，默认秩 r=256），大词表下逐步开销也小。
  - **RNN head**：维护跨整块的门控递归状态 s_k，可看全前缀历史；仅在长块上比 Markov 边际略好，但实现复杂、部署属性差 → 默认用 Markov。
- **关键洞察"a little autoregression goes a long way"**：2 层 DSpark 即超 5 层 DFlash；位置级分析显示并行 drafter 在位置 1 capacity 高（DFlash 0.88 vs Eagle3 0.81 on Math；0.72 vs 0.53 on Chat），但 DFlash 后缀衰减、Eagle3 后缀稳/升，DSpark 兼得（Math 起点 0.93 且全块稳定）。
- **关键特性**：序列 head 保持局部修正、per-token 概率仍是精确 softmax，因此满足投机解码 rejection sampling 对"精确 per-token 概率"的硬要求（CRF-NAT 的全局归一化、CTC-drafter 的对齐边缘化都做不到，只能贪婪验证）。

### 验证调度（系统侧创新）
- **Confidence head**：逐位输出标量 c_k∈(0,1)，建模"在前缀全被接受的条件下，位置 k 的 draft token 能通过 target 验证的概率"；结构=线性投影([ℎ_k; Markov 嵌入 W₁[x_{k-1}]])+sigmoid。监督信号用解析逐步接受率 c*_k = 1 − ½‖p_k^d − p_k^t‖₁（draft 与 target 分布的 TV 距离）。
- **Sequential Temperature Scaling (STS)**：神经置信常过自信，而调度需要绝对量级（算期望接受长度 τ）。STS 按链式法则对累乘前缀存活概率 ∏c_i 从左到右逐位 1D 网格搜索温度、最小化 ECE，且保序不破坏排名。效果：原始 ROC-AUC 0.81–0.90 但 ECE 3%–8% → 校准后平均 ECE ~1%。
- **Hardware-Aware Prefix Scheduler（Algorithm 1）**：把"验证长度选择"建模为全局吞吐最大化 Θ = τ·SPS(B)。SPS(B)=引擎在前向 batch B 下的 steps/sec 容量曲线，**初始化时 profile 一次存成轻量 cost table**；因前缀存活 a_{r,j}=∏_{i≤j}c_{r,i} 关于 j 单调不增，可贪婪：全局按 a_{r,j} 降序逐个 admit、O(1) 查表更新 Θ，吞吐一旦下降即 early-stop（break）。该 early-stop 同时保证**非预期性（non-anticipating）→ 无损**：截断只依赖到该步为止的前缀，不泄露未来 token（附录 A 给反例）。
- **数据/系统双轴动机**：结构化文本（代码）接受率天然高于开放聊天；轻载下多验一个 token 几乎免费，重载下却挤占别的请求的 batch 容量——故需"按负载路由验证预算"。离线置信阈值扫描印证：Chat 接受率 45.7%→95.7%、Math 76.9%→92.5%、Code 67.6%→92.0%。

### 训练
- target 模型全程冻结；draft 共享并冻结 target 的 embedding + LM head，只训 backbone drafter + 序列 block + confidence head。从每条 target 序列随机采多个 anchor 位构成 γ-token 块作训练数据。
- **三项损失**：L_ce（交叉熵，预测正确 token）+ L_tv（draft/target 分布 TV 距离，直接代理接受率）+ L_conf（对软接受标签 c*_k 的 BCE）；逐位权重 w_k = exp(−(k−1)/γ)（强调对接受长度贡献更大的前面位置）。默认 α_ce=0.1, α_tv=0.9, α_conf=1.0。
- **离线训练数据**：Open-PerfectBlend（PerfectBlend 开源版，1.3M 样本；chat 17.6% / math 39.4% / code 38.9% / instruction-following 4.1%）；**只用 prompt**，response 由各 target 模型用推荐采样重新生成，non-thinking 模式；每个 drafter 训 10 epoch。

### Benchmark（离线，accepted length τ /轮，越高越好）
- 设置：target = Qwen3-4B/8B/14B、Gemma4-12B；基线 Eagle3（自回归/TTT，1 层）、DFlash（并行，5 层）；DSpark 5 层 + Markov head + block_size=7；同框架同数据公平重训，温度 1.0，chain-based drafting。
- **DSpark vs Eagle3**：Qwen3-4B/8B/14B 宏平均 +30.9% / +26.7% / +30.0%；**vs DFlash**：+16.3% / +18.4% / +18.3%；并泛化到 Gemma4-12B。
- 例（Qwen3-4B）：GSM8K 6.11（DFlash 5.40 / Eagle3 5.14）、MATH 5.70、AIME25 4.89、HumanEval 5.38、LiveCodeBench 4.86、MT-Bench 3.64、Alpaca 3.54、Arena-Hard 3.29。结构化任务（math/code）τ 天然高于开放 chat。
- **消融**：深度——2 层 DSpark > 5 层 DFlash（序列 head 的参数效率优于堆并行层）；提案长度——gap 随 γ 拉大（γ=7 时 math/code/chat +16/15/18%，γ=15 时 +30/26/22%）；RNN 仅边际优于 Markov。
- **延迟开销**：batch=128 下 draft 长 4→16 仅给整轮延迟加 0.2%–1.3%（target 验证主导算力），却带来最高 +30% accepted length。

### Infra（在线生产部署 @ DeepSeek-V4）
- 与 V4-Flash(preview) / V4-Pro(preview) **co-deploy**；生产配置 **DSpark-5**：backbone = 3 个 MoE 层 + [[llm/2026/deepseek-v4-technical-report|mHC]] + sliding-window attention 128；max block γ=5；Markov head；confidence head 端到端联训后经 STS 校准。
- **训练系统优化（内部框架 HAI-LLM）**：① **Hidden-state 通信**——不跨 worker 传全词表 logits（V≈10⁵），只缓存并传 LM head 前的 hidden state，LM head 投影在 draft worker 本地只对采样位置算，把每 token 通信复杂度降到 O(d)；② **Anchor-bounded sequence packing**——只采固定数量 anchor、用 token 级 attention index（而非 2D mask）把独立预测块密集打包，使 draft 算力与 target 上下文长度解耦、避免 padding 开销。
- **调度器落地**——为兼容 CUDA graph replay 与 Zero-Overhead Scheduling (ZOS)，改成**异步**：用前两步的 confidence 预测当前步的动态 top-K 截断长度（当前步候选仍按最新累计 confidence 严格排序）；这道"两步前"信息形成 causal barrier，从而可去掉 early-stop break、对锯齿状 SPS 曲线做无约束全局搜索仍保持无损。
- **变长路由**：把所有请求 token 展平当独立元素处理，块内依赖靠 sparse attention 里的 marker tensor 传递；在 V4 架构上只需改 index-attention 与 compress 两个 kernel。
- **在线收益 vs MTP-1**（MTP-1 是 V4-preview 发布两周后被 DSpark 取代的旧生产基线；静态多 token drafter 在高并发下会因过度验证反而降吞吐，故此前只能用单 token）：
  - **V4-Flash**：80 tok/s/user SLA 下吞吐 +51%；匹配吞吐下单用户提速 **60%–85%**。
  - **V4-Pro**：35 tok/s/user SLA 下吞吐 +52%；匹配吞吐下单用户提速 **57%–78%**。
  - **负载自适应**：轻载（V4-Flash <200 / V4-Pro <150 并发）时验证预算从 MTP-1 的静态 2 token 扩到 ~4–6 token；重载时平滑收缩，先剪低置信后缀以保 batch 容量。把 120 TPS(Flash)/50 TPS(Pro) 这类原先 MTP-1 会崩的严苛交互档变为可服务，外推服务 Pareto 前沿。
- **局限**：仍有固定的 draft 侧开销（并行 backbone 生成初始 γ 块）；对接受率天然低的复杂 query 这部分算力不可回收，未来可在 drafter 内引入难度感知 early-exit。

### 开源物 DeepSpec（codebase）
- **DeepSpec** = 投机解码"全栈"训练/评测库（数据准备 + draft 模型实现 + 训练 + 评测脚本），MIT；内置三算法：**DSpark**、**DFlash**（arXiv 2602.06036）、**Eagle3**（arXiv 2503.01840）。建立在 SpecForge（sgl-project，Apache-2.0，提供整体训练框架与 Eagle3 实现）与 DFlash（z-lab，MIT）之上；支持 Qwen3 / Gemma target 族。
- **已放出 checkpoint（对应论文 Table 1）**：dspark / dflash / eagle3 × {Qwen3-4B, Qwen3-8B, Qwen3-14B, google/gemma-4-12B-it}（block7；Eagle3 为 ttt7），均在各自 target 用 non-thinking 模式生成的 open-perfectblend 上训练。
- **工程提示**：数据准备的 target cache 可能极大（默认 Qwen3-4B 设定 ~38 TB）；默认单机 8 GPU；评测集含 gsm8k/math500/aime25/humaneval/mbpp/livecodebench/mt-bench/alpaca/arena-hard-v2。
- HF 上 **DeepSeek-V4-Pro-DSpark / DeepSeek-V4-Flash-DSpark** = V4 同一 checkpoint **外挂投机解码模块**（官方明示"不是新模型"），最小推理示例在仓库 `inference/` 目录。

## 原始链接
- url（DeepSpec 仓库）: https://github.com/deepseek-ai/DeepSpec
- pdf_url（DSpark 论文）: https://github.com/deepseek-ai/DeepSpec/raw/main/DSpark_paper.pdf
- HF 权重: https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-DSpark · https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-DSpark
- DeepSpec 训练 checkpoint 索引（dspark/dflash/eagle3 × Qwen3/Gemma）见仓库 README "Released Checkpoints"

## 一手源存档（sources/）
- dspark-paper.pdf  （PDF 不入 git，走 HF bucket）
- [deepspec-readme.md](https://github.com/zhao9797/ai-research/blob/main/sources/llm/2026/deepspec-readme.md)
