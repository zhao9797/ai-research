# 后训练（Post-Training）

后训练指在预训练之后，把"会续写文本"的基座模型对齐为"会按指令做事、可对话、可推理、安全可控"的助手所用的全部技术。其演进可分为四个阶段：2020→2022 奠定 **RLHF 三段式**（SFT → 奖励模型 → PPO），从摘要、对话扩展到通用指令对齐（InstructGPT/ChatGPT），并衍生出红队、过程监督、Constitutional AI/RLAIF 等安全与 AI 反馈方向；2023 进入 **指令数据合成 + 离线偏好优化** 大爆发——Self-Instruct/Evol-Instruct 降低数据门槛，DPO 把"RM+PPO"压成一个分类损失，催生 IPO/KTO/ORPO/SimPO 等一整族无 RL 偏好方法，并配套 UltraFeedback、Zephyr、Tulu 等开源配方；2024 收敛为 **"SFT → 拒绝采样 → DPO/RLVR 多轮迭代"的工业级开放配方**（Llama 3、Tulu 3、Nemotron-4），同时过程奖励（PRM）与自动化过程标注（Math-Shepherd）成熟；2025→2026 则全面转向 **可验证奖励强化学习（RLVR）与长思维链推理 RL**——以 GRPO 为核心算法、DeepSeek-R1/o1 为标志，长上下文 RL、熵坍缩治理、on-policy 蒸馏、agentic/工具 RL 成为前沿。下面按子主题分组，组内按时间（YYYY-MM）排序。

## RLHF 奠基与三段式范式

- Learning to summarize from human feedback (OpenAI, 2020-09, paper) — RLHF 在生成式摘要上的奠基作，确立"偏好数据 → 奖励模型 → PPO"三段式。TL;DR 上 1.3B/6.7B RLHF 摘要被人类偏好程度超过 10× 监督模型乃至人类参考摘要；reward = RM − β·KL(π‖π_SFT)；首次给出 reward over-optimization 的早期证据。https://arxiv.org/abs/2009.01325
- WebGPT: Browser-assisted question-answering with human feedback (OpenAI, 2021-12, paper) — 早期"工具使用 + RLHF"代表，让 GPT-3 在文本浏览器中检索网页答长问题。BC（行为克隆）+ RM + rejection sampling/PPO 组合最佳，答案带引用（可验证奖励的雏形）；最佳模型 56% 胜过人类示范者、69% 胜过 Reddit ELI5 高赞。https://arxiv.org/abs/2112.09332
- Training language models to follow instructions with human feedback (InstructGPT) (OpenAI, 2022-03, paper) — 现代指令对齐奠基论文，SFT→RM→PPO 三段式。1.3B InstructGPT 人类偏好胜过 175B GPT-3；约 1.3 万 SFT + 3.3 万 RM 排序 + 3.1 万 PPO 提示；提出 PPO-ptx（RL 目标混入预训练梯度缓解性能退化）。https://arxiv.org/abs/2203.02155
- Training a Helpful and Harmless Assistant with RLHF (HH-RLHF) (Anthropic, 2022-04, paper) — 确立"有用-无害"双目标对齐范式并发布 HH 偏好数据集。13M–52B 规模研究 RM/RLHF scaling，发现 RLHF 几无对齐税；提出 online iterated RLHF（用部署策略持续重采偏好、重训 RM）；helpfulness 约 11.8 万对、harmlessness 约 4.2 万对。https://arxiv.org/abs/2204.05862
- Improving alignment of dialogue agents via targeted human judgements (Sparrow) (Google DeepMind, 2022-09, paper) — 基于"规则"拆分的 RLHF 对话代理。Chinchilla-70B 微调；双奖励（Preference RM + 约 23 条规则的 Rule RM）+ 定向人类判断 + 检索引用证据；可信回答率 78%。https://arxiv.org/abs/2209.14375

## 安全对齐、红队与 AI 反馈

- Red Teaming Language Models with Language Models (DeepMind, 2022-02, paper) — 自动化红队奠基作，用一个 LM 生成测试用例攻击目标 LM。在 280B 对话 LM 上挖出数以万计冒犯回复；测试用例生成从 zero-shot → few-shot → SFT → RL 递进，覆盖歧视、隐私泄露、多轮累积危害等类型。https://arxiv.org/abs/2202.03286
- Constitutional AI: Harmlessness from AI Feedback (Anthropic, 2022-12, paper) — RLAIF 源头，用"宪法"自然语言原则让模型自我批评-修订并以 AI 反馈替代人类无害性标注。两阶段 SL-CAI（自批评+修订→SFT）+ RL-CAI（AI 偏好→偏好模型→RL）；偏好评判时先 CoT 再判断；无害-有用 Pareto 前沿优于纯 RLHF。https://arxiv.org/abs/2212.08073
- Claude's Constitution (Anthropic, 2023-05, blog) — Claude 所用"宪法"条款来源与设计理念的官方一手说明（CAI 的产品化落地）。原则取材自《世界人权宣言》、Sparrow 规则、Anthropic 自研原则等；以成文原则替代大量人类无害性标注以提升透明、可审计、可迭代。https://www.anthropic.com/news/claudes-constitution
- RLAIF vs. RLHF: Scaling RLHF with AI Feedback (Google Research / DeepMind, 2023-09, paper) — 系统证明 AI 反馈可达到与人类反馈相当的对齐效果。摘要/对话任务上 RLAIF 与 RLHF 人类胜率相当；提出 direct-RLAIF（d-RLAIF）直接用 LLM 打分当奖励、跳过独立 RM；缓解 position bias 是关键。https://arxiv.org/abs/2309.00267
- Collective Constitutional AI: Aligning a Language Model with Public Input (Anthropic, 2023-10, blog) — 把 CAI 推向"民主参与式对齐"，用约 1000 名美国民众经 Polis 投票产生的"公众宪法"训练模型。能力/安全与 Anthropic 宪法版相当，但 BBQ 偏见更低、对群体更公平。https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input
- Llama Guard: LLM-based Input-Output Safeguard (Meta, 2023-12, paper) — 基于 Llama-2-7B 的可指令化安全分类器，把内容审核做成 prompt/response 分类任务。安全 taxonomy 写入 prompt 支持 zero/few-shot 迁移；在 OpenAI Mod、ToxicChat 上优于 Perspective API / OpenAI Moderation；开源权重。https://arxiv.org/abs/2312.06674
- Deliberative Alignment: Reasoning Enables Safer Language Models (OpenAI, 2024-12, paper) — o 系列的安全对齐方法，教推理模型在回答前显式"推理安全规范"再作答。两步：SFT 用含规范引用的合成 CoT（judge 模型按 spec 过滤）+ RL 用按 spec 打分的 RM；对越狱更鲁棒、对良性请求过度拒绝更少、对未见安全场景泛化更好。https://arxiv.org/abs/2412.16339

## 指令数据合成与 SFT 配方

- Large Language Models Can Self-Improve (Google / UIUC, 2022-10, paper) — 证明 LLM 可仅用无标注数据自我改进，是自训练/拒绝采样微调（RFT）路线的奠基作。用 CoT + self-consistency 选高置信答案再自训练 PaLM-540B；GSM8K 74.4%→82.1%、DROP 78.2%→83.0%、OpenBookQA 90.0%→94.4%。https://arxiv.org/abs/2210.11610
- Self-Instruct: Aligning Language Models with Self-Generated Instructions (UW / AI2, 2022-12, paper) — 让模型自举生成指令数据再自微调，Alpaca/Vicuna/WizardLM 等的方法鼻祖。从 175 条种子任务自举出约 52K 指令/82K 实例；GPT-3 + Self-Instruct 在 SuperNI 绝对 +33%，≈ InstructGPT-001。https://arxiv.org/abs/2212.10560
- WizardLM: Empowering LLMs to Follow Complex Instructions (Evol-Instruct) (Microsoft / Peking University, 2023-04, paper) — 用 LLM 自动"进化"指令复杂度批量合成高难度 SFT 数据。深度进化（加约束/深化/具体化/增推理步）+ 广度进化；从约 5.2 万 Alpaca 种子进化出约 25 万条；衍生 WizardCoder/WizardMath。https://arxiv.org/abs/2304.12244
- LIMA: Less Is More for Alignment (Meta AI, 2023-05, paper) — 仅 1000 条精选样本 SFT（无 RLHF）即媲美 GPT-4，提出"表层对齐假说"。LLaMA-65B 上对 GPT-4 43% 持平或更优；论点：知识来自预训练，对齐只学交互风格/格式，数据质量 >> 数量。https://arxiv.org/abs/2305.11206
- Orca: Progressive Learning from Complex Explanation Traces of GPT-4 (Microsoft Research, 2023-06, paper) — 开创 explanation tuning，用 GPT-4"解释轨迹"教 13B 小模型学推理过程而非风格。约 5M ChatGPT + 1M GPT-4 解释样本，渐进学习（teacher assistant）；BBH 超 Vicuna-13B 113%、与 ChatGPT 持平。https://arxiv.org/abs/2306.02707
- UltraFeedback: Boosting Language Models with Scaled AI Feedback (Tsinghua / OpenBMB, 2023-10, paper) — 大规模细粒度 GPT-4 AI 反馈偏好数据集，成为社区 DPO/RM 训练事实标准。约 6.4 万指令 × 4 模型回答 ≈ 25.6 万样本，GPT-4 四维度（指令遵循/真实/诚实/有用）打分；衍生 UltraRM/UltraLM，被 Zephyr/Tulu 采用。https://arxiv.org/abs/2310.01377
- Orca 2: Teaching Small Language Models How to Reason (Microsoft Research, 2023-11, paper) — 教小模型"按任务选推理策略"而非单纯模仿（Cautious Reasoning）。7B/13B（Llama 2）训练时抹去 system prompt 迫使内化策略选择；15 基准约 100 任务上接近/超 5-10× 大模型。https://arxiv.org/abs/2311.11045

## 离线偏好优化（DPO 及其变体）

- Direct Preference Optimization (DPO) (Stanford, 2023-05, paper) — 把"RM + PPO"两阶段重参数化为单一分类损失，直接用偏好对优化策略，无需显式 RM 与在线 RL。隐式奖励 r = β·log(π_θ/π_ref)；β 典型 0.1~0.5；开启 IPO/KTO/ORPO/SimPO 离线偏好优化大家族。https://arxiv.org/abs/2305.18290
- A General Theoretical Paradigm to Understand Learning from Human Preferences (IPO / ΨPO) (Google DeepMind, 2023-10, paper) — 提出统一偏好学习理论框架 ΨPO，指出 DPO 在确定性偏好下忽视 KL 正则而过拟合的根源。IPO 取恒等映射 + 平方误差目标使 KL 正则始终有效，对重复/确定性偏好更鲁棒。https://arxiv.org/abs/2310.12036
- Camels in a Changing Climate: Tulu 2 (AI2, 2023-11, paper) — 首批在 70B 规模验证 DPO 有效的工作之一，奠定 open-instruct 框架与 Tulu 系列。Llama-2 7B/13B/70B 上精选 SFT + UltraFeedback DPO，70B+DPO 在 MT-Bench/AlpacaEval 显著提升。https://arxiv.org/abs/2311.10702
- Contrastive Preference Optimization (CPO) (Johns Hopkins / Microsoft, 2024-01, paper) — 机器翻译场景的偏好优化，针对 SFT 模仿"含缺陷参考译文"的局限。DPO 偏好项 + BC 正则、丢弃参考模型（reference-free 近似）；ALMA-R 仅 22K 平行句、约 12M 可训参数即匹配/超越 WMT 冠军与 GPT-4。https://arxiv.org/abs/2401.08417
- KTO: Model Alignment as Prospect Theoretic Optimization (Stanford / Contextual AI, 2024-02, paper) — 把前景理论的损失厌恶引入对齐，只需"单条样本好/坏"二元信号即可训练。提出 HALOs 框架（DPO/PPO 为其特例）；对类别不平衡鲁棒，适合工业界海量单边反馈，1B–30B 上匹配或超 DPO。https://arxiv.org/abs/2402.01306
- ORPO: Monolithic Preference Optimization without Reference Model (KAIST, 2024-03, paper) — 把 SFT 与偏好对齐合并为单阶段、无参考模型训练。在交叉熵损失上加 odds ratio 惩罚项，一次训练既学正确回答又拉开 chosen/rejected 胜率差；省显存，超过 SFT+DPO 两段流程。https://arxiv.org/abs/2403.07691
- Is DPO Superior to PPO for LLM Alignment? (Tsinghua / OpenPsi, 2024-04, paper) — 系统对比 DPO 与 PPO，指出 DPO 可被分布外回答利用、能力上限受限。PPO 三关键技巧（优势归一化、大 batch、EMA 更新参考模型）；CodeContests 上 34B PPO（10@1k=22.4%）超 AlphaCode-41B。https://arxiv.org/abs/2404.10719
- RLHF Workflow: From Reward Modeling to Online RLHF (Salesforce / UIUC, 2024-05, paper) — 开源完整"在线迭代 RLHF"工作流，证明在线 > 离线。用代理偏好模型在线打标做迭代 DPO；Llama-3-8B-SFR-Iterative-DPO 在 AlpacaEval-2 LC 31.3%、Arena-Hard 29.1%、MT-Bench 8.46。https://arxiv.org/abs/2405.07863
- SimPO: Simple Preference Optimization with a Reference-Free Reward (Princeton / UVA, 2024-05, paper) — 用长度归一化平均对数似然作隐式奖励、去掉参考模型并加目标 margin γ。抑制长度偏置、更省显存；Llama-3-8B-Instruct + SimPO 在 AlpacaEval 2 LC 44%+、Arena-Hard 33%+，超 DPO/IPO/KTO/ORPO。https://arxiv.org/abs/2405.14734

## 拒绝采样、REINFORCE 与简化的 RL

- RAFT: Reward rAnked FineTuning (HKUST / LMFlow, 2023-04, paper) — 用 RM 对采样输出排序、只取高分样本做 SFT 的拒绝采样微调，作为 PPO 的简单稳定替代。采样 k → RM 打分 → 取 top → SFT 迭代；无 critic/优势估计，是 Llama-2 rejection sampling 路线的代表。https://arxiv.org/abs/2304.06767
- RRHF: Rank Responses to Align Language Models without tears (Alibaba DAMO / Tsinghua, 2023-04, paper) — 用"条件概率打分 + 排序损失"对齐人类偏好的极简范式，训练只需 1~2 个模型。长度归一化 log-prob 打分 + pairwise ranking loss + SFT 项；HH 数据集上对齐效果与 PPO 可比，本质是 best-of-n 学习器。https://arxiv.org/abs/2304.05302
- SPIN: Self-Play Fine-Tuning Converts Weak LMs to Strong LMs (UCLA, 2024-01, paper) — 自博弈微调，把"自己上一轮生成"当负样本、人类 SFT 数据当正样本做类 DPO 训练，无需新偏好数据。迭代直到生成与人类数据不可区分；zephyr-7b-sft 经 SPIN 后优于在额外数据上 DPO。https://arxiv.org/abs/2401.01335
- Self-Rewarding Language Models (Meta FAIR / NYU, 2024-01, paper) — 让同一模型既当策略又当裁判（LLM-as-a-Judge）自造偏好对做迭代 DPO，突破固定 RM 瓶颈。按 5 点 rubric 自评取最高/最低构对；Llama-2-70B 经 3 轮在 AlpacaEval 2.0 超 Claude 2/Gemini Pro/GPT-4 0613。https://arxiv.org/abs/2401.10020
- Back to Basics: REINFORCE Style Optimization for RLHF (RLOO) (Cohere / Cohere For AI, 2024-02, paper) — 论证 PPO 的 critic/clipping/GAE 在单步 RLHF 中多余，回归 REINFORCE + leave-one-out 基线。第 i 样本基线 = 其余 k−1 个奖励均值（无偏、无 critic）；更省显存、更鲁棒，TL;DR/HH 上胜过 PPO/RAFT/DPO。https://arxiv.org/abs/2402.14740

## 奖励模型与过程监督（PRM）

- Scaling Laws for Reward Model Overoptimization (OpenAI, 2022-10, paper) — RLHF 中"奖励黑客/过度优化"的定量研究，用 gold RM 作真值给出失真 scaling law。best-of-n：gold(d)≈d·(α−β·d)；RL：gold(d)≈d·(α−β·log d)；RM 越大、数据越多，过优化点越靠后。https://arxiv.org/abs/2210.10760
- Solving math word problems with process- and outcome-based feedback (DeepMind, 2022-11, paper) — 首次在自然语言推理（GSM8K）上系统对比过程监督 vs 结果监督，是 PRM 的概念源头。结果监督即可达相近最终答案准确率，但要降低"答案对、过程错"必须用过程监督；最终答案错误率 16.8%→12.7%、推理错误率 14.0%→3.4%。https://arxiv.org/abs/2211.14275
- Let's Verify Step by Step (OpenAI, 2023-05, paper) — 过程奖励模型（PRM）奠基论文，逐步骤验证优于只看最终答案的结果监督（ORM），并发布 PRM800K。GPT-4 微调验证器，PRM best-of-1860 在 MATH 达 78.2%；约 80 万条人工步骤级标注，是 o1/Math-Shepherd 的直接源头。https://arxiv.org/abs/2305.20050
- Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations (PKU / DeepSeek-AI, 2023-12, paper) — 用蒙特卡洛 rollout 自动给推理步骤打过程标签，无需人工即可训练 PRM。对每步采样 N 条续解、以正确率为软标签；PRM 既做 best-of-n 验证又做 step-by-step PPO，GSM8K/MATH 上达甚至超人工 PRM。https://arxiv.org/abs/2312.08935
- RewardBench: Evaluating Reward Models for Language Modeling (AI2, 2024-03, paper) — 首个系统评测 RLHF 奖励模型的基准与排行榜。覆盖 Chat/Chat-Hard/Reasoning/Safety 的 prompt-chosen-rejected 三元组（部分含可验证理由）；支持分类 RM 与 DPO 隐式 RM，成为后续 RM/对齐标准评测。https://arxiv.org/abs/2403.13787
- The Lessons of Developing Process Reward Models in Mathematical Reasoning (Qwen Team, Alibaba, 2025-01, paper) — 对 PRM 训练与评测陷阱的系统复盘，发布 Qwen2.5-Math-PRM。揭示纯 MC 估计自动标注混淆"结果对/过程对"、best-of-n 评测有偏；提出 MC + LLM-as-judge 共识过滤，ProcessBench 上 SOTA。https://arxiv.org/abs/2501.07301

## 推理 RL 与可验证奖励（RLVR / GRPO 路线）

- DeepSeekMath (GRPO) (DeepSeek-AI, 2024-02, paper) — GRPO（组相对策略优化）提出论文，用组内相对奖励替代 critic、省去价值网络，是 R1/QwQ 等的核心算法。优势 Â_i=(r_i−mean)/std；DeepSeekMath-7B 在 MATH 51.7%（self-consistency@64 60.9%）；给出 SFT/RFT/DPO/PPO/GRPO 统一梯度视角。https://arxiv.org/abs/2402.03300
- Learning to Reason with LLMs (OpenAI o1) (OpenAI, 2024-09, blog) — 首个大规模"用 RL 训练长思维链"的前沿模型，确立 test-time compute 新 scaling 轴。train-time RL 与 test-time 思考 token 均近似 log-linear 提升准确率；AIME 2024 13%→74%（共识 83%、重排 93%）、Codeforces Elo ~1807、GPQA 78%；刻意不展示原始 CoT。https://openai.com/index/learning-to-reason-with-llms/
- VinePPO: Unlocking RL Potential Through Refined Credit Assignment (Mila / McGill / ServiceNow, 2024-10, paper) — 用蒙特卡洛 rollout 估计每步真实价值替代不准的价值网络，做细粒度信用分配。对中间状态采样 K 条续解取回报均值（无偏、无 critic）；MATH/GSM8K 上更少梯度步/更短 wall-clock 超过 PPO。https://arxiv.org/abs/2410.01679
- DeepSeek-R1: Incentivizing Reasoning Capability via Reinforcement Learning (DeepSeek-AI, 2025-01, paper) — RLVR/reasoning RL 路线的标志性开源工作，证明纯 RL（R1-Zero）即可自发涌现长 CoT 与"顿悟时刻"。GRPO + 规则可验证奖励，R1-Zero AIME 2024 15.6%→71.0%；R1 用冷启动 + 多阶段 RL 对标 o1；蒸馏 80 万样本到 Qwen/Llama（1.5B–70B）。https://arxiv.org/abs/2501.12948
- Kimi k1.5: Scaling Reinforcement Learning with LLMs (Moonshot AI, 2025-01, report) — 与 R1 同期的多模态推理 RL 报告，主张长上下文 RL（最高 128K）+ 简单策略优化即可、无需 MCTS/value/PRM。提出 long2short 把长 CoT 蒸成短 CoT；long-CoT 版 AIME 77.5/MATH-500 96.2 达 o1 级，short-CoT 超 GPT-4o/Claude 3.5。https://arxiv.org/abs/2501.12599
- rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking (Microsoft Research Asia, 2025-01, paper) — 用 MCTS + 代码增强 CoT + 过程偏好模型（PPM）做四轮自进化，让小模型逼近 o1。每步附 Python 代码执行过滤、用 Q 值偏好对训 PPM；Qwen2.5-Math-7B MATH 58.8%→90.0%、AIME 2024 ~53.3%，1.5B 也超 o1-preview。https://arxiv.org/abs/2501.04519
- SWE-RL: Advancing LLM Reasoning via RL on Open Software Evolution (Meta FAIR / GenAI, 2025-02, paper) — 首个把 R1 式 RL 扩展到真实软件工程，用开源软件演化数据 + 轻量规则奖励（与真实补丁的相似度）。Llama3-SWE-RL-70B 在 SWE-bench Verified 41.0%（<100B SOTA）；仅在 SE 数据上 RL 却泛化到 5 个域外任务。https://arxiv.org/abs/2502.18449
- TAO: Test-time Adaptive Optimization (Databricks Mosaic AI, 2025-03, blog) — 用 test-time compute + RL 在"无标注输出"下微调 LLM，仅靠企业已有输入样本。探索多候选 → DBRM 奖励模型筛选 → RL 训练；仅需数千输入样本，无标签把 Llama 3.3 70B 整体提升 2.4%，FinanceBench/BIRD-SQL 超有标注微调。https://www.databricks.com/blog/tao-using-test-time-compute-train-efficient-llms-without-labeled-data
- DAPO: An Open-Source LLM RL System at Scale (ByteDance Seed / Tsinghua AIR, 2025-03, paper) — 完全开源的大规模 RL 系统，用四项技术修复 GRPO。Clip-Higher（防熵坍缩）、Dynamic Sampling（滤全对/全错组）、Token-Level PG Loss、Overlong Reward Shaping；Qwen2.5-32B 仅半步数达 AIME 2024 50 分（超 R1-Zero-Qwen-32B）。https://arxiv.org/abs/2503.14476
- Open-Reasoner-Zero (StepFun / Tsinghua, 2025-03, paper) — 首个完全开源的"base 模型上大规模 reasoning RL"实现，证明极简 vanilla PPO + 规则奖励、无 KL 正则即可复现 R1-Zero scaling。同 base（Qwen2.5-32B）下仅 ~1/10 训练步即超 R1-Zero-Qwen-32B，全开源 0.5B–32B 权重。https://arxiv.org/abs/2503.24290
- QwQ-32B: Embracing the Power of Reinforcement Learning (Qwen Team, Alibaba, 2025-03, blog) — 用多阶段大规模 RL 让 32B 稠密模型达到与 671B DeepSeek-R1 相当的推理水平。阶段一数学/代码用答案验证器与代码执行给奖励、阶段二通用 RL + agent 工具能力；AIME24/LiveCodeBench/BFCL 等可比 R1，Apache 2.0 开源。https://qwenlm.github.io/blog/qwq-32b/
- Seed1.5-Thinking: Advancing Superb Reasoning Models with RL (ByteDance Seed, 2025-04, report) — MoE 推理模型（约 200B 总参 / 20B 激活），用可验证 + 不可验证两类奖励 RL。结合 VAPO/DAPO 系列稳定化（token-level loss、dynamic sampling、value pretraining、length-adaptive GAE）+ 自研异步 RL infra；AIME 2024/Codeforces/GPQA 领先，提出 BeyondAIME。https://arxiv.org/abs/2504.13914
- ToolRL: Reward is All Tool Learning Needs (UIUC, 2025-04, paper) — 首个系统研究"工具使用 RL 奖励设计"的工作，提出格式 + 细粒度正确性奖励 + GRPO。系统消融奖励 scale/granularity/temporal dynamics；相对 base +17%、相对 SFT +15%，工具场景泛化更好。https://arxiv.org/abs/2504.13958
- DeepSeek-Prover-V2 (DeepSeek, 2025-04, paper) — 面向 Lean 4 形式化定理证明的 671B 模型，用 DeepSeek-V3 子目标分解递归证明 + RL 冷启动。统一非形式化与形式化推理；MiniF2F-test 88.9% pass ratio、PutnamBench 49/658。https://arxiv.org/abs/2504.21801
- ProRL: Prolonged RL Expands Reasoning Boundaries (NVIDIA, 2025-05, paper) — 用长时程 RL 正面反驳"RL 只放大 base 已有能力"，证明足够长 + 稳定 RL 能解出 base 怎么采样都解不出的新问题。KL 控制 + reference policy resetting + 多样任务套件；产出 Nemotron-Research-Reasoning-Qwen-1.5B（同规模开源 SOTA）。https://arxiv.org/abs/2505.24864
- Skywork Open Reasoner 1 (Skywork-OR1) (Skywork AI / Kunlun, 2025-05, report) — 开源可复现的推理 RL 配方，系统研究 RL 中策略熵坍缩问题及缓解。从 R1-Distill 出发的 GRPO 类 RL + 难度分层/去污染/滤无信号样本；Skywork-OR1-32B 在 AIME24/25、LiveCodeBench 达开源领先，全开源。https://arxiv.org/abs/2505.22312
- Magistral (Mistral AI, 2025-06, report) — Mistral 首个推理模型，完全自研、不蒸馏外部推理模型的纯 RLVR 配方 + 可扩展异步 RL infra。改进 GRPO（去 KL 惩罚、归一化、clip-higher、滤零优势组）；纯 RL 还保留并提升多语言推理；发布 Magistral Small 24B（Apache 2.0）+ Medium。https://arxiv.org/abs/2506.10910

## 蒸馏与知识迁移

- On-Policy Distillation (Thinking Machines Lab, 2025-10, blog) — 系统阐述 on-policy distillation：在学生自采轨迹上用教师逐 token 打分（reverse KL），兼具 RL 的 on-policy 相关性与蒸馏的密集奖励。比 RL 稀疏 0/1 奖励样本效率高得多、消除离线蒸馏的分布漂移；数学推理用约 1/10 RL 算力达相近性能、缓解灾难性遗忘。https://thinkingmachines.ai/blog/on-policy-distillation/

## 开源端到端后训练配方与工业级技术报告

- Llama 2: Open Foundation and Fine-Tuned Chat Models (Meta, 2023-07, paper) — 开源代表性完整 RLHF 后训练配方，提出双奖励模型（有用/安全）+ 拒绝采样 + PPO 与 Ghost Attention 多轮一致性技巧。约 140 万条人类偏好；5 轮 RLHF 迭代（v1–v5）；safety SFT/RLHF/context distillation。https://arxiv.org/abs/2307.09288
- Zephyr: Direct Distillation of LM Alignment (Hugging Face H4, 2023-10, paper) — 用蒸馏式 SFT + 蒸馏式 DPO（dDPO）在无人类标注下对齐 Mistral-7B，确立开源 SFT→DPO 标准两段式。dSFT 用 UltraChat、dDPO 用 UltraFeedback（β≈0.1）；MT-Bench 7.34，配套 alignment-handbook。https://arxiv.org/abs/2310.16944
- Gemini 1.5 (Google DeepMind, 2024-03, report) — 稀疏 MoE 多模态模型，后训练用人类偏好做指令微调与 RLHF（官方一手报告）。上下文 1M token（研究达 10M）；Flash 通过在线蒸馏从 Pro 蒸出。https://arxiv.org/abs/2403.05530
- Nemotron-4 340B Technical Report (NVIDIA, 2024-06, report) — 开放权重 340B 模型族，后训练高度依赖合成数据（>98% 对齐数据为模型生成）并开源 RM 与合成数据管线。偏好优化用 DPO + RPO（reward-aware preference optimization）；Reward 模型当时 RewardBench 领先。https://arxiv.org/abs/2406.11704
- The Llama 3 Herd of Models (Meta, 2024-07, report) — 把后训练简化为"SFT + 拒绝采样 + DPO 多轮迭代"，明确弃用 PPO。405B 预训练 15.6T tokens、上下文 128K；6 轮迭代（RM → rejection sampling → SFT → DPO，DPO 中 mask 格式 token + NLL 正则）；详尽公开各能力专项与安全栈。https://arxiv.org/abs/2407.21783
- Tulu 3: Pushing Frontiers in Open Language Model Post-Training (AI2, 2024-11, report) — 完全开源的前沿后训练配方，首次系统提出并开源 RLVR，确立"SFT → DPO → RLVR"三段式开放标准。对可验证任务（数学、精确指令）用 verifier 给 0/1 奖励做 RL（PPO/GRPO）；8B/70B 逼近/超 Llama 3.1 与 Qwen2.5 Instruct，全开放数据/代码/评测。https://arxiv.org/abs/2411.15124
- DeepSeek-V3 Technical Report (DeepSeek-AI, 2024-12, report) — 671B MoE 基座（37B 激活），后训练首次把 R1 长 CoT 推理蒸馏进通用模型（"从推理模型蒸馏 → 通用模型"范例），也是 R1 的基座。SFT + GRPO RL + reasoning distillation；14.8T tokens、约 278.8 万 H800 GPU·小时。https://arxiv.org/abs/2412.19437
- 2 OLMo 2 Furious (AI2, 2025-01, report) — 全开放（数据/代码/权重/日志）模型族，后训练直接套用 Tulu 3 配方（SFT + DPO + RLVR），是可复现"开放后训练"的端到端样本。改进训练稳定性（reordered norm、QK-Norm、Z-loss）；OLMo 2-Instruct 同规模开放权重领先。https://arxiv.org/abs/2501.00656
- Hunyuan-TurboS (Tencent, 2025-05, report) — Mamba-Transformer 混合 MoE + 自适应长短 CoT，后训练含多阶段 SFT 与可验证奖励 RL，实现"按难度决定是否深思考"。约 560B 总参 / 56B 激活；adaptive CoT 在 no-think 快路径与 deep-think 间自适应切换。https://arxiv.org/abs/2505.15431
- Llama-Nemotron: Efficient Reasoning Models (NVIDIA, 2025-05, report) — 开放高效推理模型族（Nano/Super/Ultra），用 NAS 压缩 + 推理 SFT 蒸馏 + 大规模 RL，支持运行时推理开关。LN-Ultra 253B 用 GRPO 在科学推理上做大规模 RL；"detailed thinking on/off"切换长 CoT 与直答，全开源权重/数据/代码。https://arxiv.org/abs/2505.00949
- Qwen3 Technical Report (Qwen Team, Alibaba, 2025-05, report) — 把"思考/非思考"两模式统一进一个模型（thinking budget 可控），后训练用四阶段 + strong-to-weak 蒸馏。四阶段：长 CoT 冷启动 SFT → 推理 RL → thinking/non-thinking 融合 SFT → 通用 RL；约 36T tokens、119 语言；旗舰 235B-A22B。https://arxiv.org/abs/2505.09388
- MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention (MiniMax, 2025-06, report) — 首个开源大规模混合注意力 + MoE 推理模型，提出 CISPO RL 算法。456B 总参 / ~45.9B 激活、原生 1M 上下文，生成 10 万 token 算力约 R1 的 25%；CISPO 裁剪重要性采样权重而非 token、比 DAPO 快约 2×；RL 仅约 53.5 万美元。https://arxiv.org/abs/2506.13585
- GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models (Zhipu AI, 2025-08, report) — 把 Agentic/Reasoning/Coding 三类能力统一进 MoE 模型，后训练用专家分训 + self-distillation 融合 + 大规模 RL。355B 总参 / 32B 激活（Air 106B/12B）；支持 hybrid thinking；约 23T tokens，权重 MIT 开源。https://arxiv.org/abs/2508.06471

## 增量补录（2026 调研后查漏，后训练维度）
- **GLM-5.2**（承 GLM-5）— SFT(3类/202K上下文/三种thinking) → **Reasoning RL(GRPO+IcePop,去KL,混合4域) → Agentic RL(全异步/TITO/双边IS) → General RL(规则+ORM+GRM混合奖励)** → On-Policy 跨阶段蒸馏。[详](llm/2026/glm-5.2.md)
- **Kimi-K2.6**（承 K2.5）— zero-vision SFT、按能力联合多模态 RL(视觉RL反哺文本)、token级裁剪+MuonClip、混合奖励(规则+budget+GRM+视觉)、**Toggle 省 token 25~30%**、Agent Swarm/PARL。[详](llm/2026/kimi-k2.6.md)
- **Qwen-AgentWorld** — CPT→SFT→RL(**GSPO** + rubric&rule 混合奖励)。[详](llm/2026/qwen-agentworld.md)
- **Intern-S2-Preview** — 全链 pretrain→RL、shared-weight MTP+KL、CoT 压缩。[详](llm/2026/intern-s2-preview.md)
- **MiniCPM5-1B** — **RL+OPD 两阶段推理 RL**(math/code/IF 均分↑16、超长↓29pp)。[详](llm/2026/minicpm5-1b.md)
- **Mistral-Small-4** — 统一 Instruct+Reasoning(Magistral)+Devstral，reasoning_effort 可调。[详](llm/2026/mistral-small-4.md)
