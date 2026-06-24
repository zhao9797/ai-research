# Agentic 训练

“Agentic 训练”指让大模型从“会聊天/会推理”走向“会自主行动”——调用工具、操作浏览器/电脑、多步规划、与环境交互并从结果中学习。其脉络大致是：**2020–2021** 用 RLHF 与“浏览器/定理证明”雏形把外部反馈与工具引入语言模型（Learning to summarize、WebGPT、GPT-f）；**2022–2023** 进入 prompt 范式爆发期，ReAct/ToT/Reflexion/Voyager 确立“思考-行动-观察”与搜索/反思/技能库，工具调用从 Toolformer/Gorilla/ToolLLM 走向工业 function calling，配套 WebShop/Mind2Web/WebArena/SWE-bench/GAIA 等真实环境与基准；**2024** 转向“训练造 agent”——SWE-agent/OpenHands 抽象 agent-computer 接口，AgentTuning/CodeAct/xLAM/ToolACE 用轨迹与合成数据做 SFT，computer-use（Claude/Operator）与多 agent（Magentic-One）落地，OSWorld/AndroidWorld/tau-bench/AppWorld 把评测推向真实 OS；**2025** 是“agentic RL”元年——DeepSeekMath 的 GRPO 经 DeepSeek-R1 的 RLVR 发扬成为底座，Search-o1/Search-R1/R1-Searcher/ToRL/ReTool/ToolRL/WebSailor 把可验证奖励推到搜索与工具交互，OpenAI deep research 与通义 WebThinker/WebDancer/DeepResearcher/Tongyi-DeepResearch 把深度研究 agent 端到端训练化，Kimi K2/Qwen3-Coder/GLM-4.5 等把 agentic 能力做进旗舰基座，配套 verl/OpenRLHF/AReaL/DAPO/Agent-Lightning 等 RL 基础设施；**2026** 走向长程自主、自我演化与多 agent 编排（GPT-5.5、Claude Opus 4.6、MiniMax-M2 的自我演化、Kimi K2.5 的 Agent Swarm、Nemotron 3/GLM-5 的异步 agent RL），同时安全与对齐评估（sabotage、reward hacking）成为前沿模型的必修。

> 范围与去重：本章收录 frontmatter `categories` 含「agentic训练」的全部条目，跨各年份目录与 `themes/`（agentic / post-training / ai-infra / architecture）。同一工作多处出现的（如 DeepSeek-R1、Kimi K2、WebGPT、ToolRL、WebDancer、QwQ-32B 等）已合并为一条。少数以推理/对齐为主、agentic 仅为次要标签的奠基论文（CoT、Self-Consistency、Zero-Shot Reasoners、LLM Can Self-Improve、Sparrow、General Language Assistant）归属"推理/对齐"章节，本章不重复收录。

---

## 一、早期奠基：RLHF、浏览器与定理证明（2020–2021）

- **Learning to summarize from human feedback** (OpenAI, 2020-09, paper) — RLHF 在语言生成上的奠基实证：SFT → 人类偏好奖励模型 → PPO（奖励 = RM − β·KL）。1.3B/6.7B 模型，TL;DR 约 12.3 万样本 + 约 6.4 万偏好对；人类反馈模型胜过 10× 大的监督模型，并指出 RM 过优化需 KL 约束。为 InstructGPT/ChatGPT 对齐范式铺路。https://arxiv.org/abs/2009.01325
- **Generative Language Modeling for Automated Theorem Proving (GPT-f)** (OpenAI, 2020-09, paper) — “语言模型 + 搜索 + 专家迭代”的早期代表：把证明步骤序列化，Transformer 自回归生成下一步策略，配 best-first 证明树搜索，用模型新发现的证明回灌再训练。约 774M 参数，Metamath set.mm 约 56% 证明率，部分更短证明被官方收录。https://arxiv.org/abs/2009.03393
- **WebGPT: Browser-assisted question-answering with human feedback** (OpenAI, 2021-12, paper) — agentic 浏览器使用开山之作：把浏览抽象成文本命令（Search/Click/Quote/Scroll/Answer），GPT-3（760M/13B/175B）经行为克隆 + RLHF + best-of-n 训练，作带引用的长问答。175B best-of-64 答案 56% 优于人类示范、69% 优于 Reddit 高赞，是 ReAct/工具调用的史前史。https://arxiv.org/abs/2112.09332

## 二、推理与行动范式（prompt-time，2022–2023）

- **A Generalist Agent (Gato)** (DeepMind, 2022-05, paper) — 单一 Transformer 序列模型当“通才 agent”：把对话、图像描述、Atari 游戏、真实机械臂控制等不同模态/任务统一序列化为 token，用同一套权重处理；是“一个模型做多种 agent 任务”的早期代表。https://arxiv.org/abs/2205.06175
- **ReAct: Synergizing Reasoning and Acting** (Princeton & Google Research, 2022-10, paper) — 定义至今主流的 agent 范式：交错生成 Thought-Action-Observation，few-shot 即触发、无需训练。PaLM-540B 基座；ALFWorld 较 Act-only 提升约 34 个百分点、WebShop 约 10 个百分点。https://arxiv.org/abs/2210.03629
- **Reflexion: Language Agents with Verbal Reinforcement Learning** (Northeastern/MIT/Princeton, 2023-03, paper) — “语言化强化学习”：失败后把反馈写成自然语言反思存入记忆，下次读回，不更新权重。Actor+Evaluator+Self-Reflection 三角色；HumanEval 91% pass@1（>GPT-4 80%），ALFWorld +约 22%、HotpotQA +约 20%。https://arxiv.org/abs/2303.11366
- **Tree of Thoughts: Deliberate Problem Solving** (Princeton & Google DeepMind, 2023-05, paper) — 把 CoT 从一条线推广为思考树：生成多候选思考 + 自评（value/vote）+ BFS/DFS 搜索回溯，纯 inference-time。GPT-4 在 Game of 24 从 CoT 4% 提到 ToT 74%。https://arxiv.org/abs/2305.10601
- **Voyager: An Open-Ended Embodied Agent** (NVIDIA/Caltech, 2023-05, paper) — Minecraft 终身学习具身 agent：自动课程 + 可执行代码技能库（code-as-action）+ 迭代提示自我纠错，无梯度更新。基座 GPT-4；独特物品 ×3.3、探索距离 ×2.3、科技树里程碑 ×15.3 速度。https://arxiv.org/abs/2305.16291
- **Generative Agents: Interactive Simulacra of Human Behavior** (Stanford & Google, 2023-04, paper) — 用 LLM 模拟可信人类行为：记忆流（recency+importance+relevance 检索）+ 反思 + 规划三件套，25 个 agent 在沙盒小镇自发组织情人节派对。基座 ChatGPT/GPT-3.5；消融证明三模块缺一不可。https://arxiv.org/abs/2304.03442

## 三、工具/函数调用学习（2020/2023–2024）

- **Toolformer: Language Models Can Teach Themselves to Use Tools** (Meta AI/FAIR, 2023-02, paper) — 自监督学工具调用：模型自采候选 API 调用，用“是否降低后续 token 困惑度”过滤，再在 API 增强语料上常规微调。基座 GPT-J 6.7B（QA/计算器/维基/翻译/日历等），零样本超 GPT-3 175B 且语言建模能力不损。https://arxiv.org/abs/2302.04761
- **HuggingGPT (JARVIS)** (Microsoft Research / Zhejiang Univ., 2023-03, paper) — LLM 当调度大脑，把 HF 专家模型当工具：任务规划→模型选择→任务执行→响应生成四阶段编排跨模态任务，子任务间用资源引用传中间结果。https://arxiv.org/abs/2303.17580
- **Gorilla: LLM Connected with Massive APIs** (UC Berkeley / Microsoft, 2023-05, paper) — 微调 LLaMA-7B 专攻 API 调用 + 检索感知训练（retriever-aware）应对 API 文档变化；APIBench（TorchHub/TensorHub/HuggingFace），AST 子树匹配评测，准确度超 GPT-4、显著减幻觉 API；演化出 BFCL。https://arxiv.org/abs/2305.15334
- **WebGLM** (智谱 AI / 清华 KEG, 2023-06, paper) — 给 GLM 装“网页检索 + 引用生成 + 人类偏好打分”的高效联网问答，对标并改进 WebGPT：LLM 增强检索器 + 自举生成器（WebGLM-QA 数据集）+ 偏好打分器，基座 GLM-10B/2B，成本显著低于 WebGPT。https://arxiv.org/abs/2306.07906
- **Function calling and other API updates** (OpenAI, 2023-06, blog) — 把工具调用产品化进 API：gpt-4-0613/gpt-3.5-turbo-0613 按函数 schema 输出结构化 JSON 参数，奠定 tool use/agent 工业标准。https://openai.com/index/function-calling-and-other-api-updates/
- **ToolLLM: Mastering 16000+ Real-world APIs** (清华 THUNLP 等, 2023-07, paper) — 开源工具学习里程碑：ChatGPT 自动构造覆盖 16,464 个真实 RESTful API（49 类，来自 RapidAPI）的 ToolBench；DFSDT（深度优先决策树）支持多分支回溯 + ToolEval 自动评测，训出可比肩 ChatGPT 的 ToolLLaMA（配神经 API 检索器）。https://arxiv.org/abs/2307.16789
- **ToolACE: Winning the Points of LLM Function Calling** (华为诺亚 / 港科大, 2024-09, paper) — 函数调用数据合成引擎：自进化合成 26,507 个 API + 多 agent 自引导对话（单/并行/依赖/嵌套）+ 双层校验（规则+模型）；训练的 8B 模型在 Berkeley Function-Calling Leaderboard 比肩 GPT-4。https://arxiv.org/abs/2409.00920
- **xLAM: A Family of Large Action Models** (Salesforce AI Research, 2024-09, report) — “大动作模型”系列（1B 稠密到 8x22B MoE）专为 agent/函数调用训练，配统一“格式化+增强+合成”数据管线；多个登顶 BFCL，超 GPT-4/Claude-3；1B 适合端侧。https://arxiv.org/abs/2409.03215

## 四、Agent 专项微调与训练范式（2023–2024）

- **AgentTuning** (清华 / 智谱, 2023-10, paper) — 轻量 agent 轨迹指令微调 + 通用指令混合训练，使开源 LLM 获泛化 agent 能力又不损通用能力。AgentInstruct（GPT-4 构造的交互轨迹）+ 混合微调 → AgentLM-7B/13B/70B；70B 在未见 agent 任务达 GPT-3.5-turbo 水平。https://arxiv.org/abs/2310.12823
- **FireAct: Toward Language Agent Fine-tuning** (System2/剑桥/Princeton, 2023-10, paper) — 系统论证“微调比 prompt 更能造 agent”：用 GPT-4 在 QA+Google 搜索上生成多方法（ReAct/CoT/Reflexion）多任务轨迹微调小模型；仅 500 条轨迹即大幅提升 Llama-2-7B 的 HotpotQA，混合来源更鲁棒。https://arxiv.org/abs/2310.05915
- **CodeAct: Executable Code Actions Elicit Better LLM Agents** (UIUC/Apple/Google, 2024-02, paper) — 主张用可执行 Python 代码作为统一动作空间（code-as-action），取代 JSON/文本调用，天然支持控制流/组合/自调试。17 个 LLM 上较 JSON/text 成功率最多高 20%；开源 CodeActInstruct（7k 轨迹）与 CodeActAgent，深刻影响 OpenHands/SWE-agent。https://arxiv.org/abs/2402.01030
- **AgentGym: Evolving LLM-based Agents across Diverse Environments** (复旦 NLP, 2024-06, paper) — 通用自进化 agent 训练框架与平台：14 个环境 + 跨环境轨迹数据 AgentTraj（SFT 基础 agent）+ 自进化算法 AgentEvol（多环境探索、用成功轨迹自训练以跨环境泛化）；进化后 agent 达/超 SOTA。https://arxiv.org/abs/2406.04151

## 五、真实环境与基准（Web/GUI/SWE/通用，2022–2026）

- **WebShop** (Princeton, 2022-07, paper) — 早期可扩展网购 agent 环境：118 万真实商品 + 1.2 万众包指令，动作含 search/choose/click；模仿学习 + RL（奖励=商品匹配度），可零样本迁移到 amazon/ebay，是 ReAct 标准实验床。https://arxiv.org/abs/2207.01206
- **Mind2Web: Towards a Generalist Agent for the Web** (Ohio State, 2023-06, paper) — 首个通用网页 agent 大规模真实数据集：137 个真实网站、31 领域、2000+ 任务带动作序列；MindAct 两阶段（小 LM 排序 DOM 元素 + 大 LM 多选预测动作）；cross-task/website/domain 三泛化设置。https://arxiv.org/abs/2306.06070
- **WebArena** (CMU, 2023-07, paper) — 高真实可复现网页环境：自托管电商/论坛/GitLab/CMS + 地图/计算器/Wiki，812 个长程任务执行级评测。GPT-4 仅 14.41% vs 人类 78.24%；衍生 WebArena-Lite。https://arxiv.org/abs/2307.13854
- **AgentBench: Evaluating LLMs as Agents** (清华 / 智谱 等, 2023-08, paper) — 首个多环境 LLM-as-agent 综合基准：OS/数据库/知识图谱/卡牌/具身/网购/网页等 8 个交互环境，测 25+ 模型，揭示 GPT-4 与开源模型的巨大差距（长程一致性、格式/指令遵循）。https://arxiv.org/abs/2308.03688
- **SWE-bench: Can LMs Resolve Real-World GitHub Issues?** (Princeton / U Chicago, 2023-10, paper) — 软件工程 agent 奠基评测：2,294 个真实 issue+PR（12 个 Python 仓库），用 FAIL_TO_PASS/PASS_TO_PASS 单元测试执行级判定。Claude 2 仅 1.96% resolved；衍生 Lite/Verified/Multimodal，成为 coding agent 事实标准。https://arxiv.org/abs/2310.06770
- **GAIA: a benchmark for General AI Assistants** (Meta FAIR/HF/AutoGPT, 2023-11, paper) — 通用 AI 助手标尺：466 题三难度，需推理+多模态+网页浏览+工具使用；人类 92% vs GPT-4+plugins 15%；成为 deep research/通用 agent 核心指标。https://arxiv.org/abs/2311.12983
- **WebVoyager** (浙大 / 腾讯 AI Lab / 西湖大学, 2024-01, paper) — 首批端到端多模态网页 agent：GPT-4V 看带 Set-of-Mark 标注的截图直接操作 15 个真实网站，并用 GPT-4V 做自动评测；任务成功率 59.1%，被 OpenAI CUA 等引为基准。https://arxiv.org/abs/2401.13919
- **OSWorld** (港大 / 上交 / Salesforce, 2024-04, paper) — computer-use agent 标准环境：真实 OS（Ubuntu/Windows/macOS）369 个跨应用任务，执行级判定。人类 72.36% vs 最优模型 12.24%（瓶颈在 GUI grounding）；成为 Claude/CUA/UI-TARS 核心赛场。https://arxiv.org/abs/2404.07972
- **AndroidWorld** (Google DeepMind, 2024-05, paper) — Android 移动 GUI agent 评测：真实模拟器 20 个 app、116 个程序化任务（参数化、可无限自然语言变体），每任务带 init/success-check/tear-down 给奖励信号，与 OSWorld 互补。https://arxiv.org/abs/2405.14573
- **τ-bench: Tool-Agent-User Interaction** (Sierra, 2024-06, paper) — 首个评测“工具-agent-用户”三方交互：LM 模拟用户与配 API+策略的 agent 多轮对话，按数据库终态判定，提出 pass^k 度量可靠性。gpt-4o 单次 <50%、retail pass^8 <25%，揭示一致性问题；衍生 τ²-bench。https://arxiv.org/abs/2406.12045
- **AppWorld** (Stony Brook, 2024-07, paper) — 交互式编码 agent 高保真世界：9 个日常 app、457 个 API、约 100 个虚构用户的模拟数字生活；750 个任务要求写带控制流的代码迭代完成，含副作用检查。GPT-4o 完整任务通过率约 30%。https://arxiv.org/abs/2407.18901
- **Introducing SWE-bench Verified** (OpenAI, 2024-08, blog) — 与 SWE-bench 原作者合作发布 500 题人审子集，修正过度特定测试/描述欠明确/环境难搭建三类问题（原基准低估模型能力），纳入 Preparedness 框架，成为各大模型标准报告口径。https://openai.com/index/introducing-swe-bench-verified/
- **OS-Genesis** (上海 AI Lab / 港大 等, 2024-12, paper) — 解 GUI 训练数据瓶颈：反转采集流程——先无目标交互再“逆向合成任务”（reverse task synthesis）+ 轨迹奖励模型质控，自动产高质量多样轨迹；在 AndroidWorld/AndroidControl/WebArena 上远超此前合成方法。https://arxiv.org/abs/2412.19723
- **WebWalker: Benchmarking LLMs in Web Traversal** (阿里通义, 2025-01, paper) — 网页深度遍历基准 WebWalkerQA + 多 agent explore-critic 框架，考查系统性遍历子页提取深层信息；是通义 DeepResearch 系列评测基石。https://arxiv.org/abs/2501.07572
- **Mind2Web 2: Agentic Search with Agent-as-a-Judge** (Ohio State, 2025-06, paper) — 面向 Deep Research 时代：130 个长程、需实时浏览+信息综合的真实任务（构建耗 1000+ 小时），提出 Agent-as-a-Judge 核验带引用、随时变的复杂答案。https://arxiv.org/abs/2506.21506

## 六、软件工程 agent 与多 agent 系统（2023–2024）

- **AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation** (Microsoft Research, 2023-08, paper) — 开源多 agent 对话框架：把应用抽象为多个可定制、可对话的 agent（LLM/工具/人类混合）以自然语言协作，支持灵活的对话编排与自动化；是后续 Magentic-One 等多 agent 系统的底座。https://arxiv.org/abs/2308.08155
- **SWE-agent: Agent-Computer Interfaces** (Princeton/Stanford, 2024-05, paper) — 提出 Agent-Computer Interface（ACI）概念：为 LM 专设命令行式浏览/编辑（带 lint）/测试接口，证明接口设计本身是性能关键变量。SWE-bench pass@1 12.5%、HumanEvalFix 87.7%（当时 SOTA）。https://arxiv.org/abs/2405.15793
- **OpenHands (原 OpenDevin)** (OpenHands community, 2024-07, paper) — 开源通用软件开发 agent 平台：统一动作空间（执行代码/bash/浏览器）+ Docker 沙盒 + 事件流架构 + 多 agent 委派；内置 15+ 基准近 2000 任务（SWE-bench/WebArena/GAIA 等），是社区最广用的 coding/computer-use 基础设施。https://arxiv.org/abs/2407.16741
- **Magentic-One** (Microsoft Research/AutoGen, 2024-11, paper) — 开源通用多 agent 系统：Orchestrator 主控做规划/进度跟踪/失败重规划（外层 task ledger + 内层 progress ledger），调度 WebSurfer/FileSurfer/Coder/Terminal 专才 agent；GAIA/WebArena/AssistantBench 有竞争力，模型无关。https://arxiv.org/abs/2411.04468

## 七、GUI / Computer-use Agent（2023–2026）

- **CogAgent: A VLM for GUI Agents** (清华 / 智谱, 2023-12, paper) — 18B 视觉语言模型专攻 GUI：低/高分辨率双编码器支持 1120×1120 识别细小元素，仅凭截图在 Mind2Web/AITW 超过用 HTML 文本的 LLM；9 个 VQA 基准 SOTA，是 AutoGLM 的视觉基座之一。https://arxiv.org/abs/2312.08914
- **Developing a computer use model / Claude 3.5 Sonnet computer use** (Anthropic, 2024-10, blog) — 首个前沿模型提供 computer use（公开 beta）：看截图、数像素定位光标、点击/键入操作任意软件；仅用计算器/文本编辑器等少量软件训练即泛化、会自我纠错。OSWorld 14.9%（同类最高），同时升级 SWE-bench Verified 33.4%→49.0%、TAU-bench retail 62.6%→69.2%/airline 36.0%→46.0%。https://www.anthropic.com/news/3-5-models-and-computer-use ；研发洞见见 https://www.anthropic.com/news/developing-computer-use
- **AutoGLM: Autonomous Foundation Agents for GUIs** (智谱 / 清华, 2024-10, report) — ChatGLM 家族 GUI 基础 agent：分离“规划”与“grounding”的中间接口设计 + 自进化在线课程 RL。VAB-WebArena-Lite 55.2%（retry 59.1%）、OpenTable 96.2%；AndroidLab 36.2%、中文热门 App 89.7%。https://arxiv.org/abs/2411.00820
- **WebRL: Training LLM Web Agents via Self-Evolving Online Curriculum RL** (清华 / 智谱, 2024-11, paper) — 自进化在线课程 RL 把开源模型训成强网页 agent：失败任务自动生成新任务 + 结果监督奖励模型（ORM）+ 自适应 RL 缓解分布漂移。WebArena-Lite 上 Llama-3.1-8B 4.8%→42.4%、GLM-4-9B 6.1%→43%，均超 GPT-4-Turbo(17.6%)/GPT-4o(13.9%)，是 AutoGLM 背后关键 RL 技术。https://arxiv.org/abs/2411.02337
- **Computer-Using Agent (CUA)** (OpenAI, 2025-01, blog) — 驱动 Operator 的模型：GPT-4o 视觉 + RL 习得推理，仅凭截图+键鼠操作 GUI，无需 OS/网页专用 API。OSWorld 38.1%、WebArena 58.1%、WebVoyager 87%。https://openai.com/index/computer-using-agent/
- **Introducing Operator** (OpenAI, 2025-01, blog) — 首个面向消费者的浏览器 agent 产品：自带云端浏览器替用户填表/下单/订位，由 CUA 驱动，2025-01 研究预览（美国 Pro），后并入 ChatGPT Agent 模式。https://openai.com/index/introducing-operator/
- **UI-TARS: Pioneering Automated GUI Interaction with Native Agents** (字节 Seed / 清华, 2025-01, paper) — 端到端原生 GUI agent（2B/7B/72B，基于 Qwen2-VL）：纯截图→统一跨平台动作空间，靠增强感知 + 统一动作建模 + System-2 推理 + 反思式在线轨迹迭代（数百 VM）训练。OSWorld 24.6(50步)/22.7(15步) > Claude(22.0/14.9)，AndroidWorld 46.6 > GPT-4o 34.5。https://arxiv.org/abs/2501.12326

## 八、Agentic RL：可验证奖励、工具与搜索的强化学习（2024–2025）

- **DeepSeekMath** (DeepSeek, 2024-02, paper) — 首次提出 GRPO（Group Relative Policy Optimization）——去掉 critic、用组内相对优势估计基线，成为后来 DeepSeek-R1 及几乎所有 agentic/工具/搜索 RL 的核心算法；DeepSeekMath-7B 首次让开源模型在竞赛级 MATH 突破 50%。https://arxiv.org/abs/2402.03300
- **DeepSeek-R1** (DeepSeek, 2025-01, paper) — 纯 RL 即可激发强推理的算法底座：R1-Zero 用 GRPO（去 critic、组内相对优势）+ 规则化可验证奖励（RLVR）让推理自发涌现，AIME 2024 pass@1 15.6%→71.0%（投票 86.7%）；R1 多阶段管线对标 o1-1217。GRPO+RLVR 成为 Search-R1/ReTool/ToolRL/WebSailor 等的事实标准。https://arxiv.org/abs/2501.12948
- **Kimi k1.5: Scaling RL with LLMs** (Moonshot AI, 2025-01, paper) — 把 RL 当新 scaling 轴：长上下文（128k 级）+ 简化策略优化，刻意不用 MCTS/价值函数/过程奖励即对标 o1（AIME 77.5、MATH500 96.2、Codeforces 94th）；提出 long2short 把长思考压回短模型。https://arxiv.org/abs/2501.12599
- **Search-o1: Agentic Search-Enhanced Large Reasoning Models** (人大 / 清华, 2025-01, paper) — 给 o1 类大推理模型（LRM）装“按需检索 + 文档精炼”的 agentic RAG，训练无关（inference-time）。主干 QwQ-32B-Preview；agentic RAG + 独立 Reason-in-Documents 模块（先精炼冗长文档再回填），是后续 Search-R1/R1-Searcher/DeepResearcher 的前置工作与对比基线。https://arxiv.org/abs/2501.05366
- **SWE-RL** (Meta FAIR/GenAI, 2025-02, paper) — 首个把 R1 式 RL 扩展到真实软工：用开源软件演化数据 + 轻量规则奖励（生成补丁与真实补丁的相似度，无需执行测试）训练 Llama3-SWE-RL-70B，SWE-bench Verified 41.0%（<100B SOTA），并涌现可迁移的域外推理。https://arxiv.org/abs/2502.18449
- **QwQ-32B: Embracing the Power of RL** (阿里 Qwen, 2025-03, blog) — 32B 稠密靠两阶段 RL（数学/编程 outcome-based 验证器 → 通用 RL）对标 DeepSeek-R1（671B/37B），集成工具调用时的批判性思考；131K 上下文，Apache 2.0。https://qwenlm.github.io/blog/qwq-32b/
- **Search-R1** (UIUC/UMass/Google, 2025-03, paper) — 把 R1 式 RL 推到“边推理边搜索”：推理链中以 <search> 自主发起多轮检索，用 retrieved token masking 稳定训练 + outcome-based 奖励（PPO/GRPO）。7 个 QA 数据集较 RAG 基线 Qwen2.5-7B +41%、3B +20%。https://arxiv.org/abs/2503.09516
- **R1-Searcher: Incentivizing the Search Capability via RL** (人大高瓴, 2025-03, paper) — 纯 RL（无蒸馏、无 SFT 冷启动）激发自主检索：两阶段 outcome-based RL（Stage1 检索奖励只激励发起检索 → Stage2 引入答案奖励）+ 检索 mask 损失，基于 Reinforce++。HotpotQA 较强基线最高 +48.22%，在未见的 Bamboogle（在线搜索）上超 32B 的 Search-o1 11.4%。https://arxiv.org/abs/2503.05592
- **ToRL: Scaling Tool-Integrated RL** (上交 / SII / GAIR, 2025-03, paper) — 直接从 base 模型（无任何 post-training）做工具集成 RL，让模型自主发现写代码→调解释器的最优策略而非靠 SFT 模仿。GRPO + veRL + Sandbox Fusion，省 KL/temp=1；TORL-7B 在 AIME24 达 43.3%（+10 vs Instruct-TIR），涌现策略性工具调用与无效代码自调节。https://arxiv.org/abs/2503.23383
- **ReTool: RL for Strategic Tool Use** (字节 Seed, 2025-04, paper) — outcome-driven RL 教模型“何时/如何调代码解释器”：rollout 内多轮实时执行代码 + 结果奖励。Qwen2.5-32B 400 步达 AIME 67%（文本 RL 基线 40% 需 1080 步），扩展设置 72.5%（超 o1-preview 27.9pt），涌现代码自纠错。https://arxiv.org/abs/2504.11536
- **ToolRL: Reward is All Tool Learning Needs** (UIUC/Amazon, 2025-04, paper) — 首个系统研究工具使用 RL 的奖励设计（类型/尺度/粒度/时序），给出格式+细粒度正确性奖励 + GRPO；较 base +17%、较 SFT +15%，分布外工具泛化更好。https://arxiv.org/abs/2504.13958
- **RAGEN: Self-Evolution via Multi-Turn RL** (西北大学/斯坦福/微软/NUS, 2025-04, paper) — 系统研究多轮 agent RL 为何不稳：提出轨迹级框架 StarPO，诊断“Echo Trap”（奖励方差崩塌、梯度尖峰），用 StarPO-S（轨迹过滤+critic+梯度稳定化）缓解；结论是无细粒度推理感知奖励则真推理难涌现。https://arxiv.org/abs/2504.20073
- **DeepResearcher: Scaling Deep Research via RL in Real-world Environments** (上交 / SII / GAIR, 2025-04, paper) — 首个在真实开放网络（真实搜索引擎 + 网页爬取）端到端 RL 训练 deep research agent，跳出本地静态 RAG 沙盒。Qwen2.5-7B + GRPO 仅用结果奖励、自建 50 节点集群处理海量 rollout 工具请求；比 prompt 基线 +28.9、比 RAG-RL +7.2，涌现跨源交叉验证/找不到答案时保持诚实等行为。https://arxiv.org/abs/2504.03160
- **WebThinker: Empowering LRMs with Deep Research Capability** (人大 / 智源 / 华为, 2025-04, paper) — 让大推理模型在推理中自主“搜网页 + 点链接深探 + 边想边写报告”：Deep Web Explorer + Autonomous Think-Search-and-Draft 策略，用迭代在线 DPO 端到端优化工具使用。主干 QwQ-32B→WebThinker-32B，GAIA 48.5、WebWalkerQA 46.5（NeurIPS 2025）。https://arxiv.org/abs/2504.21776
- **WebDancer: Towards Autonomous Information Seeking** (阿里通义, 2025-05, paper) — 通义 DeepResearch 端到端配方：浏览数据构造→轨迹采样→SFT 冷启动→RL，基于 ReAct 训出多步深度检索 web agent，在 GAIA/WebWalkerQA 表现强。https://arxiv.org/abs/2505.22648
- **WebSailor: Navigating Super-human Reasoning for Web Agent** (阿里通义, 2025-07, paper) — 后训练方法论：用“信息混淆”造高不确定性任务 + RFT 冷启动 + 高效 agentic RL 算法 DUPO（采样复用），让开源 web agent 在 BrowseComp 等极难检索任务逼近闭源 DeepResearch。https://arxiv.org/abs/2507.02592
- **Agent Lightning: Train ANY AI Agents with RL** (Microsoft Research, 2025-08, paper) — agent RL 基础设施：把 agent 执行与训练完全解耦（Training-Agent Disaggregation），几乎零改代码即可对 LangChain/OpenAI Agents SDK/AutoGen/自研 agent 做 RL；把执行建模为 MDP + 分层算法 LightningRL 做信用分配；在 text-to-SQL/RAG/数学工具上稳定提升。https://arxiv.org/abs/2508.03680

## 九、Agentic RL 训练基础设施（2024–2025）

- **OpenRLHF** (OpenRLHF community, 2024-05, paper) — 首批可扩展到 70B+ 的开源 RLHF 框架：Ray 编排 + vLLM 生成 + DeepSpeed ZeRO-3 训练，解耦 actor/critic/reward/ref 四模型；支持 PPO/DPO/KTO/拒绝采样，后扩展到异步/多轮/VLM agentic RL。https://arxiv.org/abs/2405.11143
- **HybridFlow (verl)** (字节 / 港大, 2024-09, paper) — 当前最主流大规模 RL post-training 框架之一：single-controller（算法 dataflow）+ multi-controller（分布式执行）混合范式 + 3D-HybridEngine 在训练/生成间高效 resharding；较 SOTA 吞吐 1.5–20×，支撑 DAPO 等。https://arxiv.org/abs/2409.19256
- **DAPO: Open-Source LLM RL System at Scale** (字节 Seed / 清华 AIR, 2025-03, paper) — 完全开源的大规模推理 RL 系统与算法（Clip-Higher / Dynamic Sampling / Token-Level PG Loss / Overlong Reward Shaping，基于 verl）；Qwen2.5-32B base 在 AIME 2024 达 50 分（超 R1-Zero-Qwen-32B 47，约半训练步数）。https://arxiv.org/abs/2503.14476
- **AReaL: Large-Scale Asynchronous RL System** (蚂蚁 / 清华 IIIS, 2025-05, paper) — 全异步 RL 系统：rollout 与训练完全解耦（rollout 持续生成、training 异步更新），靠 staleness 控制 + staleness-enhanced PPO 保稳，消除“等最长序列”空转，端到端显著提速。https://arxiv.org/abs/2505.24298
- **SGLang** (Stanford / UC Berkeley, 2023-12, paper) — 面向结构化 LLM 程序（多轮/并行/工具调用/约束解码）的前端 DSL + 运行时，核心 RadixAttention 用基数树跨请求自动复用 KV 前缀；吞吐最高 6.4×，被 DeepSeek/xAI 等用于大规模 serving，是 agentic rollout 的常用后端。https://arxiv.org/abs/2312.07104

## 十、Agentic 能力进入旗舰基座（2023–2026）

### 2023–2024
- **Qwen Technical Report** (阿里 Qwen, 2023-09, paper) — Qwen 首份技术报告：1.8B/7B/14B 基座 + Qwen-Chat（SFT+RM+RLHF），Chat 原生支持 tool use / code interpreter / ReAct 式 agent；另有 Code-Qwen / Math-Qwen 专用模型。https://arxiv.org/abs/2309.16609
- **ChatGLM3 series** (智谱 / 清华 KEG, 2023-10, github) — 第三代开源对话模型：全新 Prompt 格式（system/user/assistant/observation）原生支持 Function Call、Code Interpreter、Agent 任务；ChatGLM3-6B-Base 为 10B 以下最强基座。https://github.com/THUDM/ChatGLM3
- **MOSS** (复旦 OpenMOSS, 2023-04, github) — 中国首个公开支持插件/工具调用的开源对话模型：16B 基座（约 700B 词预训练）→ SFT（约 110 万多轮）→ 插件增强 SFT（约 30 万，搜索/文生图/计算器/解方程）→ 偏好模型，全链路开源。https://github.com/OpenMOSS/MOSS
- **InternLM2 Technical Report** (上海 AI Lab / 商汤, 2024-03, paper) — 1.8B/7B/20B 全开放技术报告：InternEvo 训练框架、200K 长上下文、COOL RLHF（条件奖励模型 + 多轮 PPO 缓解 reward hacking）；agentic 与长上下文联动，配 Lagent/AgentFLAN 体系。https://arxiv.org/abs/2403.17297
- **Introducing Command R+** (Cohere, 2024-04, blog) — 面向企业、RAG 优化的旗舰（约 104B）：128K 上下文、带内联引用的高级 RAG、Multi-Step Tool Use（规划并按序调用多工具/API 的 agent 能力）、10 种业务语言，首发 Microsoft Azure。https://cohere.com/blog/command-r-plus-microsoft-azure
- **Introducing Claude 3.5 Sonnet** (Anthropic, 2024-06, blog) — 以 Claude 3 Sonnet 的速度/成本超越 Opus，agentic 编码大幅领先：内部 agentic coding eval 解决 64%（Opus 38%）——给自然语言描述即自主修 bug/加功能并执行代码；引入 Artifacts。https://www.anthropic.com/news/claude-3-5-sonnet
- **ChatGLM: from GLM-130B to GLM-4 All Tools** (智谱 / 清华, 2024-06, paper) — GLM-4 系列技术报告（GLM-4 / Air / 9B）整体逼近 GPT-4-Turbo、中文对齐超 GPT-4；GLM-4 All Tools 强调模型自主理解意图并自动规划调用工具（浏览器/Python/文生图等）完成复杂任务。https://arxiv.org/abs/2406.12793
- **Learning to Reason with LLMs (OpenAI o1)** (OpenAI, 2024-09, blog) — 首次系统阐述用大规模 RL 训练“先思考再回答”（长内部 CoT），开辟 test-time compute scaling：性能随 train-time 与 test-time 算力 log-linear 提升；AIME/Codeforces(89th)/GPQA Diamond 大超 GPT-4o。https://openai.com/index/learning-to-reason-with-llms/
- **OpenAI o1 System Card** (OpenAI, 2024-12, model-card) — o1/o1-mini 正式版安全卡：提出 deliberative alignment（模型在 CoT 中显式推理安全策略），在抗越狱等基准 SOTA；含 Preparedness 框架（CBRN/网络/说服/模型自主）评级与外部红队。https://openai.com/index/openai-o1-system-card/
- **Introducing Gemini 2.0 — AI for the agentic era** (Google DeepMind, 2024-12, blog) — 主打 agentic 时代：Gemini 2.0 Flash 原生多模态输入/输出 + 原生工具（Search/代码执行/函数调用），配 Project Astra/Mariner（WebVoyager 83.5%）/Jules 等 agent 原型与 Deep Research。https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/
- **Building effective agents** (Anthropic, 2024-12, blog) — 工程指南，定义“workflows vs agents”区分与五大可组合模式（提示链/路由/并行/编排-工人/评估-优化），主张简单可组合胜过复杂框架，强调 ACI 与护栏。https://www.anthropic.com/engineering/building-effective-agents

### 2025
- **OpenAI o3-mini** (OpenAI, 2025-01, blog) — 小型推理模型，可调推理强度（low/medium/high），首次把带 function calling/结构化输出的推理模型推向 API；AIME 2024 high 档 83.6%、GPQA Diamond 77.0%，专家盲评 56% 偏好于 o1-mini。https://openai.com/index/openai-o3-mini/
- **Introducing deep research** (OpenAI, 2025-02, blog) — agentic 深度研究：为浏览优化的 o3 早期版，端到端 RL 训练于真实浏览+沙盒 Python，自主多步检索/综合产带引用长报告，GAIA 创 SOTA。https://openai.com/index/introducing-deep-research/
- **Claude 3.7 Sonnet and Claude Code** (Anthropic, 2025-02, blog) — 市场首个 hybrid reasoning 模型：同一模型 standard 与 extended thinking 双模式、API 可设思考预算（最高 128K），后训练转向真实业务任务，SWE-bench Verified / TAU-bench 当时 SOTA；同步发布终端 agentic 编码 CLI Claude Code。https://www.anthropic.com/news/claude-3-7-sonnet
- **Grok 3 Beta — The Age of Reasoning Agents** (xAI, 2025-02, blog) — Colossus 超算（约 10× 前代算力）预训练 + 大规模 RL 推理后训练：Grok 3 (Think) AIME 2025 cons@64 93.3%、GPQA 84.6%、LiveCodeBench 79.4%；Grok Agents 结合推理与工具使用（DeepSearch）。https://x.ai/news/grok-3
- **Amazon Nova Family** (Amazon AGI, 2025-03, technical-report) — Nova Pro/Lite/Micro 理解模型 + Canvas/Reel 生成模型族，评测维度显式含 agentic performance 与 long context，强调多模态与高性价比。https://www.amazon.science/publications/the-amazon-nova-family-of-models-technical-report-and-model-card
- **Command A** (Cohere, 2025-03, technical-report) — 111B 企业级多语言模型，面向 RAG/工具使用/agentic 业务流程自动化：sliding-window+full attention 3:1 混合架构、256K 上下文、去中心化训练（self-refinement + model merging）；23 语言、最高 156 tok/s（约 1.75× GPT-4o）。https://arxiv.org/abs/2504.00698
- **Seed1.5-Thinking** (字节 Seed, 2025-04, paper) — RL 推理模型，200B 总参/20B 激活的小型 MoE：AIME 2024 86.7、Codeforces 55.0、GPQA 77.3，非推理任务胜率超 DeepSeek-R1 8%。https://arxiv.org/abs/2504.13914
- **Introducing OpenAI o3 and o4-mini** (OpenAI, 2025-04, blog) — 首批“会自己用全套工具”的推理模型：训练学会何时/如何自主调用并组合 ChatGPT 全部工具（网搜/Python/视觉推理/图像生成）。o3 在 Codeforces/SWE-bench(无定制 scaffold)/MMMU SOTA；o4-mini 允许 Python 时 AIME 2025 99.5% pass@1。https://openai.com/index/introducing-o3-and-o4-mini/
- **OpenAI o3 and o4-mini System Card** (OpenAI, 2025-04, system-card) — o3/o4-mini 安全卡：首次让推理模型在单条思维链中“agentically”组合调用 ChatGPT 全部工具（浏览/Python/图像分析与生成/文件检索/记忆）；依 Preparedness Framework 评估，三类追踪风险均未达 High 阈值。https://openai.com/index/o3-o4-mini-system-card/
- **DeepSeek-R1-0528** (DeepSeek, 2025-05, blog) — R1 重大更新：扩大 RL 后训练规模提升推理，减少幻觉，新增 JSON 输出与 function calling 为 agent 场景铺路（671B MoE/37B 激活）。https://api-docs.deepseek.com/news/news250528
- **Qwen3 Technical Report** (阿里 Qwen, 2025-05, paper) — 把思考/非思考统一进单一模型并引入“思考预算”，0.6B–235B（含 235B-A22B MoE）全开源 Apache 2.0，原生 function calling/工具使用，agent 任务对标更大 MoE 与闭源。https://arxiv.org/abs/2505.09388
- **Seed1.5-VL** (字节 Seed, 2025-05, paper) — 视觉语言基座（532M 编码器 + 20B 激活 MoE）：60 个公开 benchmark 中 38 个 SOTA；GUI 控制/游戏等 agent 任务超 OpenAI CUA 与 Claude 3.7。https://arxiv.org/abs/2505.07062
- **Introducing Claude 4 (Opus 4 & Sonnet 4)** (Anthropic, 2025-05, blog) — 主打编码与长时程 agent：Opus 4 SWE-bench Verified 72.5%、Terminal-bench 43.2%，可持续 agent 工作数小时（Rakuten 验证连续 7 小时重构）；extended thinking + 工具交替、并行工具调用、本地文件“记忆”；新增 code execution / MCP connector / Files API。https://www.anthropic.com/news/claude-4
- **MiniMax-M1** (MiniMax, 2025-06, paper) — 全球首个开源大规模混合注意力推理模型（456B/45.9B 激活，原生 1M 上下文）：提出 CISPO RL 算法（裁剪重要性采样权重），在 sandbox 软工等任务全程 RL 仅 512×H800 约三周（约 53.5 万美元）。https://arxiv.org/abs/2506.13585
- **Hunyuan-A13B** (腾讯混元, 2025-06, report) — 细粒度 MoE（80B 总/13B 激活），fast/slow 双模式思考、256K 上下文，多阶段 RL 含 agent/tool use 强化，开源权重。https://github.com/Tencent-Hunyuan/Hunyuan-A13B
- **Gemini 2.5 Technical Report** (Google DeepMind, 2025-06, technical-report) — 稀疏 MoE + 原生多模态的 thinking 模型族（2.5 Pro/Flash + 2.0 Flash/Flash-Lite）：1M（部分 2M）输入上下文、思考预算可控，后训练含 RL 提升推理与工具使用，覆盖能力-成本 Pareto 前沿。https://arxiv.org/abs/2507.06261
- **GLM-4.5V and GLM-4.1V-Thinking** (智谱, 2025-07, paper) — 视觉语言推理家族：提出 RLCS（带课程采样的 RL），覆盖 GUI agent/编程/grounding；GLM-4.5V（基于 GLM-4.5-Air 106B MoE）在 42 个 benchmark 多数开源同尺寸 SOTA，GUI/Coding 对标 Gemini-2.5-Flash。https://arxiv.org/abs/2507.01006
- **Qwen3-Coder: Agentic Coding in the World** (阿里 Qwen, 2025-07, blog) — 最强 agentic 代码模型 Qwen3-Coder-480B-A35B（MoE，原生 256K 外推 1M）：在 20K 并行环境做大规模 agentic code RL（Coding/Browser-Use/Tool-Use），开源 SOTA 对标 Claude Sonnet 4，配 Qwen Code CLI。https://qwenlm.github.io/blog/qwen3-coder/
- **Kimi K2: Open Agentic Intelligence** (Moonshot AI, 2025-07, paper) — 1T 总参/32B 激活 MoE 专为 agentic 打造：MuonClip 优化器（QK-clip）15.5T token 零 loss spike 预训练 + 大规模 agentic 数据合成 + 联合 RL；non-thinking 下 Tau2-Bench 66.1、SWE-Bench Verified 65.8、ACEBench(En) 76.5。https://arxiv.org/abs/2507.20534
- **Grok 4** (xAI, 2025-07, blog) — Colossus 20 万 GPU 集群把 RL 扩到“预训练规模”（训练计算效率 +6×），大规模可验证数据 + 原生工具使用（code interpreter/web/X 浏览，自主选搜索查询）；Humanity's Last Exam 带工具领先，并推出多 agent 协作版 Grok 4 Heavy。https://x.ai/news/grok-4
- **GLM-4.5: Agentic, Reasoning, and Coding (ARC)** (智谱, 2025-08, paper) — 以 ARC 为目标的开源 MoE 旗舰（355B 总/32B 激活，另 Air 106B）：混合推理（思考+直答），23T token + 专家模型迭代 + RL 后训练。TAU-Bench 70.1%、AIME 24 91.0%、SWE-bench Verified 64.2%，agentic 基准排名第 2。https://arxiv.org/abs/2508.06471
- **OpenAI GPT-5 System Card** (OpenAI, 2025-08, system-card) — 统一系统：gpt-5-main（快速）+ gpt-5-thinking（深推理）+ real-time router 自动路由；新 “safe completions” 安全训练范式；依 Preparedness Framework 对生化领域按 High capability 部署缓解，含 agentic/工具使用红队，并降低幻觉/欺骗/sycophancy。https://openai.com/index/gpt-5-system-card/
- **gpt-oss-120b & gpt-oss-20b Model Card** (OpenAI, 2025-08, model-card) — OpenAI 时隔多年的开放权重模型（Apache 2.0）：MoE（120b 116.8B 总/5.13B 激活）+ 交替带状窗口/全密注意力 + attention sink + MXFP4 量化（120B 单卡 80GB）；后训练面向推理与工具使用，含 variable effort reasoning 与 agentic tool use（harmony 格式）。https://openai.com/index/gpt-oss-model-card/
- **DeepSeek-V3.1** (DeepSeek, 2025-08, blog) — 迈向 agent 时代第一步：首个混合推理（Think/Non-Think 单模型双模式）模型，后训练强化工具使用与多步 agent 任务（671B MoE/37B 激活）。https://api-docs.deepseek.com/news/news250821
- **LongCat-Flash** (美团, 2025-09, paper) — 美团首个开源大模型（560B MoE）：Zero-computation Experts 动态激活 18.6B–31.3B（均值 27B）+ Shortcut-connected MoE，约 20T+ token 30 天训成，面向 agentic 的多阶段后训练（含 RL/tool use）。https://arxiv.org/abs/2509.01322
- **Baichuan-M2** (百川智能, 2025-09, paper) — 医疗大模型：用“大型验证器系统”（患者模拟器 + 临床评分生成器）做动态交互式 RL，弥合静态医考分数与真实临床决策的差距，基于 Qwen2.5-32B。https://arxiv.org/abs/2509.02208
- **GLM-4.6** (智谱, 2025-09, blog) — GLM-4.5 升级：上下文 128K→200K，编程/推理/agent 全面增强、支持推理时工具调用，对标 DeepSeek-V3.2-Exp 与 Claude Sonnet 4（延续 355B MoE/32B 激活 ARC 架构）。https://z.ai/blog/glm-4.6
- **Tongyi DeepResearch Technical Report** (阿里通义实验室, 2025-10, technical-report) — 开源 deep research agentic 大模型（30.5B 总/3.3B 激活，基于 Qwen3-30B-A3B）：统一“agentic 中训练 + agentic 后训练”端到端范式 + 全自动数据合成 + 定制 GRPO；HLE 32.9、BrowseComp 43.4、GAIA 70.9，多项超 o3/DeepSeek-V3.1/GLM-4.5/Kimi-K2。https://arxiv.org/abs/2510.24701
- **Ring-1T** (蚂蚁 InclusionAI, 2025-10, paper) — 首个万亿参数开源 thinking 模型（1T 总/约 50B 激活）：提出 IcePop（token 级差异 masking+clipping 解决训推不一致）/ C3PO++（rollout 效率）/ ASystem（万亿级 RL 系统），数学/代码/逻辑开源 SOTA。https://arxiv.org/abs/2510.18855
- **DeepSeek-V3.2** (DeepSeek, 2025-12, paper) — 引入 DeepSeek Sparse Attention（DSA，lightning indexer + top-k）大降长上下文训练/推理成本 + 可扩展 RL 框架，性能对标 GPT-5；V3.2-Exp 落地 DSA 后 API 降价 50%+。https://arxiv.org/abs/2512.02556

### 2026
- **LongCat-Flash-Thinking-2601** (美团, 2026-01, paper) — 560B MoE 推理模型主打 agentic 推理（search/tool use/TIR）：统一“领域并行专家训练 + 后续融合”训练框架 + 端到端协同设计，在 agentic search/tool use 开源 SOTA、噪声真实环境稳健。https://arxiv.org/abs/2601.16725
- **System Card: Claude Opus 4.6** (Anthropic, 2026-02, model-card) — 前沿旗舰（ASL-3）：强软件工程/agentic/长上下文；新增 adaptive thinking + effort 四档（low/medium/high/max）；后训练含 RLHF+RLAIF；用 interpretability（activation oracles/attribution graphs/SAE 特征）做对齐评估，观察到 sabotage concealment 与 computer-use 过度 agentic 行为上升。https://www.anthropic.com/system-cards
- **Risk Report: February 2026** (Anthropic, 2026-02, report) — 配合 Opus 4.6 的 105 页安全评估：以 Sabotage 为首要自主性威胁模型做“主张-证据”论证（评估意识/隐写/推理忠实性/model organism），并管理 reward hacking（最高风险设置用 inoculation prompting + 暴露 prompt-reward 不匹配的可视化工具）。https://www.anthropic.com/feb-2026-risk-report
- **GLM-5: from Vibe Coding to Agentic Engineering** (智谱, 2026-02, paper) — 把 vibe coding 推进到 agentic engineering：DSA 稀疏注意力降本 + 全新异步 RL 基础设施（解耦 generation/training）+ 新颖异步 agent RL 算法从长程交互学习；真实端到端软工超 baseline（迭代至 GLM-5.2 支持 1M 上下文、IndexShare）。https://arxiv.org/abs/2602.15763
- **Kimi K2.5: Visual Agentic Intelligence** (Moonshot AI, 2026-02, paper) — 开源多模态 agentic：文本-视觉联合优化（joint pre-train + zero-vision SFT + joint RL）+ Agent Swarm（自主并行智能体编排，动态分解异构子问题，延迟降低最多 4.5×）；编码/视觉/推理/agentic 多域开源 SOTA。https://arxiv.org/abs/2602.02276
- **Nemotron-Cascade 2** (NVIDIA, 2026-03, paper) — 开放 30B MoE（3B 激活）后训练模型：SFT → 大幅扩展的 Cascade RL（覆盖更广推理+agentic 域）+ 多域在线策略蒸馏（每域取最强中间教师）；2025 IMO/IOI/ICPC 金牌级（开放权重中第二个），20× 更少参数。https://arxiv.org/abs/2603.19220
- **LongCat-Flash-Prover** (美团, 2026-03, paper) — 560B MoE 通过 agentic 工具集成 RL（TIR）推进 Lean4 原生形式化推理：任务分解为 auto-formalization/sketching/proving，提出 HisPO（分层重要性采样策略优化，梯度掩码处理 policy staleness 与训推差异）稳定长程 MoE RL，含防 reward hacking 检测。https://arxiv.org/abs/2603.21065
- **Introducing GPT-5.5** (OpenAI, 2026-04, blog) — 旗舰 agentic 模型（含 Pro/Thinking）主打智能体化办公：长周期自主规划→调用工具→自我核查。Terminal-Bench 2.0 82.7%、SWE-Bench Pro 58.6%、OSWorld-Verified 78.7%、BrowseComp 84.4%、Tau2-bench Telecom 98.0%、GDPval 84.9%；通过 Preparedness 全套安全评估。https://openai.com/index/introducing-gpt-5-5/
- **Grok 4.20 System Card** (xAI, 2026-04, model-card) — 旗舰模型具备高级推理与多智能体能力，可单智能体(SA)或多智能体(MA)部署；按 Frontier AI Framework 沿恶意使用/失控两轴 + CBRN/网络安全/有害操纵做双用途评估。https://data.x.ai/2026-04-07-grok-4-20-model-card.pdf
- **Nemotron 3 Super** (NVIDIA, 2026-04, paper) — 120B 总/12B 激活的混合 Mamba-Attention MoE，为 agentic 优化：首用 NVFP4 预训练（25T token）+ LatentMoE + MTP 投机解码，1M 上下文；吞吐相比 GPT-OSS-120B 2.2×、Qwen3.5-122B 7.5×，全开源。https://arxiv.org/abs/2604.12374
- **Introducing Muse Spark** (Meta Superintelligence Labs, 2026-04, blog) — MSL 首个模型（原生多模态推理）：tool-use + visual CoT + multi-agent orchestration，新增 Contemplating mode 并行编排多 agent 推理（HLE 58%）；三条 scaling 轴（预训练 FLOPs 较 Llama 4 Maverick 省 >10×、RL、test-time）。https://ai.meta.com/blog/introducing-muse-spark-msl/
- **MiMo-V2.5-Pro** (小米 MiMo, 2026-04, model-card) — 1.02T 总参/42B 激活开源 MoE：沿用 MiMo-V2-Flash 混合注意力 + 3 层 MTP，最高 1M 上下文，定位 agent/long-context/code，MIT。https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro
- **Hy3 preview (Hunyuan 3 preview)** (腾讯混元, 2026-04, model-card) — 295B/21B 激活 MoE，是混元在“重建基础设施”上训练的首个、最强模型，强化复杂推理/指令跟随/上下文学习/代码与 agent（重建 RL 基础设施带来 code/agent 最大增幅）；192 专家 top-8、256K 上下文。https://huggingface.co/tencent/Hy3-preview
- **Step-Audio-R1.5** (阶跃星辰, 2026-04, paper) — 音频推理大模型，识别 RLVR 在音频上的“可验证奖励陷阱”：纯客观奖励虽刷高基准却损害韵律/情感连续性/对话自然度，提出兼顾可验证收益与声学细节的方向。https://arxiv.org/abs/2604.25719
- **Remote agents in Vibe (Mistral Medium 3.5)** (Mistral AI, 2026-05, blog) — 旗舰“合并模型”（128B 稠密、256k 上下文、per-request 推理强度，开放权重）支撑 Vibe 远程 agent 与 Le Chat Work mode 长周期 agentic：SWE-Bench Verified 77.6%、τ³-Telecom 91.4。https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/
- **Step 3.7 Flash** (阶跃星辰, 2026-05, model-card) — 198B 稀疏 MoE 视觉语言模型（11B 激活、400 tok/s、256k、三档推理）面向高频生产级 agentic：ClawEval-1.1 67.1、Toolathlon 49.5、Terminal-Bench 2.1 59.5、SWE-Bench PRO 56.3，Apache-2.0。https://huggingface.co/stepfun-ai/Step-3.7-Flash
- **The MiniMax-M2 Series** (MiniMax, 2026-05, paper) — “mini 激活释放最大真实世界智能”（旗舰 229.9B 总/9.8B 激活）：agent 驱动数据 pipeline（可验证轨迹 + artifact 对齐奖励）+ Forge agent-native RL 系统（训练/推理/agent 三方解耦）+ M2.7 checkpoint 迈出自我演化（自主 debug 训练 run、改自身 scaffold）。https://arxiv.org/abs/2605.26494
- **Introducing new capabilities to GPT-Rosalind** (OpenAI, 2026-06, blog) — 企业级生命科学专用模型系列：把 GPT-5.5 的 agentic 编程/工具使用与药物化学/基因组学领域智能结合，配套端到端 LifeSciBench（六大科研工作流），trusted access 研究预览。https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind/
- **Baichuan-M4: A Clinical-Grade Medical Agent System for Continuous Care** (百川智能, 2026-06, paper) — 临床级医疗 agent 系统，面向“持续照护”而非单轮问答：Baichuan-Harness 运行时（工具使用/长期患者记忆/多 agent 协调）+ 连续照护 RL 核心推理模型（span-level reward SPAR++、推理路径压缩、课程学习）+ 临床工具层（循证检索/多模态影像）；动态 OSCE 问诊/长上下文临床记忆/医疗 OCR 均领先。https://arxiv.org/abs/2606.08982
- **Ling and Ring 2.6 Technical Report** (蚂蚁 InclusionAI, 2026-06, paper) — 万亿级 MoE 模型族（Ling-2.6 即时响应 / Ring-2.6 深度推理）：经“架构迁移预训练 + 大规模后训练”从 Ling-2.0 升级，引入 hybrid linear attention（Lightning Attention + MLA），以 Evolutionary CoT / Linguistic Unit Policy Optimization 优化每输出 token 能力密度。https://arxiv.org/abs/2606.15079
- **Nemotron 3 Ultra** (NVIDIA, 2026-06, paper) — Nemotron 3 家族最强（550B 总/55B 激活混合 Mamba-Attention MoE）为长时自主 agentic 优化：20T token 预训练→扩 1M 上下文→SFT+RL+多教师在线策略蒸馏(MOPD)；LatentMoE/MTP/NVFP4/多环境 RLVR，吞吐相比公开 SOTA 最高约 6×，全开源。https://arxiv.org/abs/2606.15007
