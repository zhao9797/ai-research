# GLM-4.6: Advanced Agentic, Reasoning and Coding Capabilities
Source: https://z.ai/blog/glm-4.6
GLM-4.6: Advanced Agentic, Reasoning and Coding Capabilities


![](https://z-cdn-media.chatglm.cn/prompts-rich-media-resources/5-blog/z-icon.png)

2025-09-30 · Research

# GLM-4.6: Advanced Agentic, Reasoning and Coding Capabilities

[- ![](https://z-cdn.chatglm.cn/z-blog/z-icon.svg)Try it at Z.ai](https://z.ai)[- ![](https://z-cdn.chatglm.cn/z-blog/z-icon.svg)Call it at Z.ai](https://docs.z.ai/guides/llm/glm-4.6)[- ![](https://z-cdn.chatglm.cn/z-blog/hf-logo.svg)HuggingFace](https://huggingface.co/zai-org/GLM-4.6)[- 📄Tech Report](https://arxiv.org/abs/2508.06471)

Today, we are releasing the latest version of our flagship model: **GLM-4.6**. Compared with GLM-4.5, this generation brings several key improvements:

* **Longer context window:** The context window has been expanded from 128K to 200K tokens, enabling the model to handle more complex agentic tasks.
* **Superior coding performance:** The model achieves higher scores on code benchmarks and demonstrates better real-world performance in applications such as Claude Code、Cline、Roo Code and Kilo Code, including improvements in generating visually polished front-end pages.
* **Advanced reasoning:** GLM-4.6 shows a clear improvement in reasoning performance and supports tool use during inference, leading to stronger overall capability.
* **More capable agents:** GLM-4.6 exhibits stronger performance in tool using and search-based agents, and integrates more effectively within agent frameworks.
* **Refined writing:** Better aligns with human preferences in style and readability, and performs more naturally in role-playing scenarios.
  We evaluated GLM-4.6 across eight public benchmarks covering agents, reasoning, and coding. Results show clear gains over GLM-4.5, with GLM-4.6 also holding competitive advantages over leading domestic and international models such as **DeepSeek-V3.2-Exp** and **Claude Sonnet 4**, but still lags behind Claude Sonnet 4.5 in coding ability.

![](https://z-cdn.chatglm.cn/z-blog/glm-4-6/coding_benchmark.png)

Real-world experience matters more than leaderboards. We extended **CC-Bench** from GLM-4.5 with more challenging tasks, where human evaluators worked with models inside isolated Docker containers and completed multi-turn real-world tasks across front-end development, tool building, data analysis, testing, and algorithm. **GLM-4.6** improves over GLM-4.5 and reaches **near parity with Claude Sonnet 4 (48.6% win rate)**, while clearly outperforming other open-source baselines. From a **token-efficiency** perspective, GLM-4.6 finishes tasks with about 15% fewer tokens than GLM-4.5, showing improvements in both capability and efficiency. All evaluation details and trajectory data have been made publicly available for further community research: <https://huggingface.co/datasets/zai-org/CC-Bench-trajectories>

![](https://z-cdn.chatglm.cn/z-blog/glm-4-6/perf.png)

# Getting started with GLM-4.6

## Call GLM-4.6 API on Z.ai API platform

The Z.ai API platform offers both GLM-4.6 models. For comprehensive API documentation and integration guidelines, please refer to <https://docs.z.ai/guides/llm/glm-4.6>. Alternatively, developers are welcome to access both models through OpenRouter.

## Use GLM-4.6 with Coding Agents

GLM-4.6 is now available to use within coding agents (Claude Code, Kilo Code, Roo Code, Cline and more).

For **GLM Coding Plan subscribers**: You'll be automatically upgraded to GLM-4.6. If you've previously customized the app configs (like `~/.claude/settings.json` in Claude Code), simply update the model name to `"glm-4.6"` to complete the upgrade.

For **New users**: The GLM Coding Plan offers Claude-level performance at a fraction of the cost — just 1/7th the price with 3x the usage quota. Start building today: <https://z.ai/subscribe>.

## Chat with GLM-4.6 on Z.ai

GLM-4.6 is accessible through [Z.ai](https://chat.z.ai) by selecting the GLM-4.6 model option.

## Serve GLM-4.6 Locally

Model weights of GLM-4.6 is publicly available at [HuggingFace](https://huggingface.co/zai-org/GLM-4.6) and [ModelScope](https://modelscope.cn/models/ZhipuAI/GLM-4.6). For local deployment, GLM-4.6 supports inference frameworks including vLLM and SGLang. Comprehensive deployment instructions are available in the official GitHub repository.

![](https://z-cdn.chatglm.cn/z-blog/z-icon.svg)

### Legal

[Privacy Policy](https://chat.z.ai/legal-agreement/privacy-policy)[Terms of Service](https://chat.z.ai/legal-agreement/terms-of-service)

© 2026 [Z.ai](https://chat.z.ai) Inc.

中
