# OpenAI o3-mini | OpenAI
Source: https://openai.com/zh-Hans-CN/index/openai-o3-mini/
OpenAI o3-mini | OpenAI

[跳至主要内容](#main)

* [研究](/zh-Hans-CN/research/index/)
* 产品
* [企业](/zh-Hans-CN/business/)
* [开发人员](/zh-Hans-CN/api/)
* [公司](/zh-Hans-CN/about/)
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

登录[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=2ef666d5-d68e-41a5-8af7-70903e4e76cc&openaicom_referred=true)

* 研究
* 产品
* 企业
* 开发人员
* 公司
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

OpenAI o3-mini | OpenAI

2025年1月31日

[发布](/research/index/release/)

# OpenAI o3‑mini

推动高性价比推理的前沿发展。

聆听文章

5:56

快速、强大且针对 STEM 推理进行了优化

* [快速、强大且针对 STEM 推理进行了优化](#kuai-suqiang-da-qie-zhen-dui-stem-tui-li-jin-xing-liao-you-hua)
* [模型速度与性能](#mo-xing-su-du-yu-xing-neng)
* [安全](#an-quan)
* [下一步计划](#xia-yi-bu-ji-hua)

目录

* [快速、强大且针对 STEM 推理进行了优化](#kuai-suqiang-da-qie-zhen-dui-stem-tui-li-jin-xing-liao-you-hua)
* [模型速度与性能](#mo-xing-su-du-yu-xing-neng)
* [安全](#an-quan)
* [下一步计划](#xia-yi-bu-ji-hua)

我们正在发布 OpenAI o3‑mini，这是我们推理系列中最新、最具成本效益的模型，现在可在 ChatGPT 和 API 中使用。这款功能强大的快速模型于 [2024 年 12 月进行了预览发布⁠](/12-days/#day-12)，突破了小型模型的能力极限，提供卓越的 STEM 能力，尤其在科学、数学和编码方面具有优势，同时保持了 OpenAI o1‑mini 的低成本和低延迟性能。

OpenAI o3‑mini 是我们首款小型推理模型，支持开发人员高度期待的功能，包括[函数调用⁠（在新窗口中打开）](https://platform.openai.com/docs/guides/function-calling)、[结构化输出⁠（在新窗口中打开）](https://platform.openai.com/docs/guides/structured-outputs)及[开发人员消息⁠（在新窗口中打开）](https://platform.openai.com/docs/guides/text-generation#building-prompts)，使其从一开始就具备生产就绪状态。与 OpenAI o1‑mini 和 OpenAI o1‑preview 一样，o3‑mini 将支持[流式传输⁠（在新窗口中打开）](https://platform.openai.com/docs/api-reference/streaming)。此外，开发人员可以在三种[推理强度⁠（在新窗口中打开）](https://platform.openai.com/docs/api-reference/chat/create)选项（低、中、高）中进行选择，以针对其特定用例进行优化。这种灵活性使 o3‑mini 在应对复杂挑战时能够“深度思考”，或在担心延迟问题时优先考虑速度。o3‑mini 暂不支持视觉功能，开发人员处理视觉推理任务时仍需使用 OpenAI o1。即日起，o3‑mini 将在聊天完成 API、助手 API 和批处理 API 中逐步推出，面向 [API 使用第 3 至第 5 级⁠（在新窗口中打开）](https://platform.openai.com/docs/guides/rate-limits/usage-tiers#tier-3-rate-limits)的部分开发人员开放。

ChatGPT Plus、Team 和 Pro 版用户即日起可访问 OpenAI o3‑mini， Enterprise 版访问权限将于二月推出。o3‑mini 将取代模型选择器中的 OpenAI o1‑mini，提供更高的消息限额和更低的延迟，使其成为编码、STEM 和逻辑问题解决任务的理想选择。作为此次升级的一部分，我们将 Plus 和 Team 用户的消息限额提高了三倍，从 o1‑mini 的每天 50 条消息增加到 o3‑mini 的每天 150 条消息。 此外，o3‑mini 现在可以通过搜索功能查找带有相关网络资源链接的最新答案。这是我们致力于将搜索整合到推理模型中的早期原型。

即日起，Free 套餐用户还可以通过在消息编写器中选择“推理”或重新生成回复来试用 OpenAI o3‑mini。这标志着 ChatGPT 首次向免费用户提供推理模型。

虽然 OpenAI o1 仍然是我们更广泛的通用知识推理模型，但 OpenAI o3‑mini 为需要精确度和速度的技术领域提供了专门的替代方案。在 ChatGPT 中，o3‑mini 使用中等推理强度，在速度和准确性之间实现了平衡。所有付费用户还可以在模型选择器中选择 `o3‑mini‑high`，以获得生成回复时间稍长的高智能版本。Pro 用户可无限制访问 `o3‑mini` 和 `o3‑mini‑high`。

## 快速、强大且针对 STEM 推理进行了优化

与其前身 OpenAI o1 类似，OpenAI o3‑mini 针对 STEM 推理进行了优化。中等推理强度的 o3‑mini 在数学、编码和科学方面的表现与 o1 相当，同时回复速度更快。经专家测试人员的评估，o3‑mini 的答案比 OpenAI o1‑mini 更准确、更清晰，推理能力更强。56% 的测试人员更喜欢 o3‑mini 而不是 o1‑mini 的答案，并且还观察到在解决现实世界难题时主要错误减少了 39%。在中等推理强度下，o3‑mini 在一些最具挑战性的推理和智能评估（包括 AIME 和 GPQA）中的表现与 o1 相当。

### Competition Math (AIME 2024)

![The bar chart compares accuracy on AIME 2024 competition math questions across AI models. Older models (gray) score lower, while newer ones (yellow) improve. "o3-mini (high)" reaches the highest accuracy at 83.6%, showing significant progress.](https://images.ctfassets.net/kftzwdyauwt9/8P5ddf0mQCNmstUbSceyU/53aacead98e5224b73fd422487c87030/Competition_Math.png?w=3840&q=90&fm=webp)

***Mathematics****: With low reasoning effort, OpenAI o3‑mini achieves comparable performance with OpenAI o1‑mini, while with medium effort, o3‑mini achieves comparable performance with o1. Meanwhile, with high reasoning effort, o3‑mini outperforms both OpenAI o1‑mini and OpenAI o1, where the gray shaded regions show the performance of majority vote (consensus) with 64 samples.*

### PhD-level Science Questions (GPQA Diamond)

![The bar chart compares accuracy on PhD-level science questions (GPQA Diamond) across AI models. Older models (gray) perform lower, while newer ones (yellow) improve. "o3-mini (high)" reaches 77.0% accuracy, showing notable progress over earlier versions.](https://images.ctfassets.net/kftzwdyauwt9/6RtMqSi8nzD2TawNrhiCXr/1d7eed551d8d118e6c6d219e38f5b5a7/GPQA.png?w=3840&q=90&fm=webp)

***PhD-level science****: On PhD-level biology, chemistry, and physics questions, with low reasoning effort, OpenAI o3‑mini achieves performance above OpenAI o1‑mini. With high effort, o3‑mini achieves comparable performance with o1.*

### FrontierMath

![A black grid with multiple rows and columns, separated by thin white lines, creating a structured and organized layout.](https://images.ctfassets.net/kftzwdyauwt9/2Kqb3fMRY7h7BWguQ98nXh/4bf95bd4a3612e17db603a9bfe101338/Frontier_Math.png?w=3840&q=90&fm=webp)

***Research-level mathematics****: OpenAI o3‑mini with high reasoning performs better than its predecessor on FrontierMath. On FrontierMath, when prompted to use a Python tool, o3‑mini with high reasoning effort solves over 32% of problems on the first attempt, including more than 28% of the challenging (T3) problems. These numbers are provisional, and the chart above shows performance without tools or a calculator.*

### Competition Code (Codeforces)

![The bar chart compares Elo ratings on Codeforces competition coding tasks across AI models. Older models (gray) score lower, while newer ones (yellow) improve. "o3-mini (high)" reaches 2073 Elo, showing significant progress over previous versions.](https://images.ctfassets.net/kftzwdyauwt9/3saK5JZ8D4U2hSNiLebOyc/40928834335f5061fa60b7f200850983/Competition_Code.png?w=3840&q=90&fm=webp)

***Competition coding****: On Codeforces competitive programming, OpenAI o3‑mini achieves progressively higher Elo scores with increased reasoning effort, all outperforming o1‑mini. With medium reasoning effort, it matches o1’s performance.*

### Software Engineering (SWE-bench Verified (n=477))

![The bar chart compares accuracy on SWE-bench Verified software engineering tasks across AI models. Older models (gray) perform lower, while "o3-mini (high)" (yellow) achieves the highest accuracy at 48.9%, showing improvement over previous versions.](https://images.ctfassets.net/kftzwdyauwt9/3ww3UedB0YdteOeII6yGKI/ae9c0e372f7a294ecc93b638fc958b07/SWE.png?w=3840&q=90&fm=webp)

***Software engineering****: o3‑mini is our highest performing released model on SWEbench-verified. For additional datapoints on SWE-bench Verified results with high reasoning effort, including with the open-source Agentless scaffold (39%) and an internal tools scaffold representing maximum capability elicitation (61%), see our* [*system card⁠*⁠](/index/o3-mini-system-card/) *as the source of truth. All SWE-bench evaluation runs use a fixed subset of n=477 verified tasks which have been validated on our internal infrastructure.*

### LiveBench Coding

![The table compares AI models on coding tasks, showing performance metrics and evaluation scores. It highlights differences in accuracy and efficiency, with some models outperforming others in specific benchmarks.](https://images.ctfassets.net/kftzwdyauwt9/6DeAgFrWPGWvxr900jboFN/d87490f06d2f8f717bd3b97f3a1e8cc9/Model_Graphic_1.png?w=3840&q=90&fm=webp)

***LiveBench coding****: OpenAI o3‑mini surpasses o1‑high even at medium reasoning effort, highlighting its efficiency in coding tasks. At high reasoning effort, o3‑mini further extends its lead, achieving significantly stronger performance across key metrics.*

### 通用知识

![The table titled "Category Evals" compares AI models across different evaluation categories, showing performance metrics. It highlights differences in accuracy, efficiency, and effectiveness, with some models outperforming others in specific tasks.](https://images.ctfassets.net/kftzwdyauwt9/7M9bgnPM6aVPdVGjzyvPyS/cc82dfb95e7d190352ae178d5841ef68/Category_Evals.png?w=3840&q=90&fm=webp)

***General knowledge****: o3‑mini outperforms o1‑mini in knowledge evaluations across general knowledge domains.*

### 人类偏好评估

![The chart compares win rates for STEM and non-STEM tasks across AI models. "o3_mini_v43_s960_j128" (yellow) outperforms "o1_mini_chatgpt" (red baseline) in both categories, with a higher win rate for STEM tasks.](https://images.ctfassets.net/kftzwdyauwt9/2stEmupk7JqXZN02Md1E7v/9b9712ce375b0c6f75f9bb2c97a1ef9d/Human_Evals_1.png?w=3840&q=90&fm=webp)

![The chart compares win rates under time constraints and major error rates across AI models. "o3_mini_v43_s960_j128" (yellow) outperforms "o1_mini_chatgpt" (red baseline) in win rate and significantly reduces major errors.](https://images.ctfassets.net/kftzwdyauwt9/6bU2O7RkqWNcBMj12Kfrx0/be286fa9f39393be0838656ab8c1da60/Human_Evals_2.png?w=3840&q=90&fm=webp)

***Human preference evaluation****: Evaluations by external expert testers also show that OpenAI o3‑mini produces more accurate and clearer answers, with stronger reasoning abilities than OpenAI o1‑mini, especially for STEM. Testers preferred o3‑mini's responses to o1‑mini 56% of the time and observed a 39% reduction in major errors on difficult real-world questions.*

## 模型速度与性能

OpenAI o3‑mini 拥有与 OpenAI o1 相当的智能，性能更快，效率更高。除了上述重点呈现的 STEM 领域评估外，o3‑mini 在中等推理强度下，在其他数学能力与事实性评估中也展现出更优的性能表现。在 A/B 测试中，o3‑mini 的回复速度比 o1‑mini 快 24%，平均回复时间为 7.7 秒，而 o1‑mini 为 10.16 秒。

### Latency comparison between o1-mini and o3-mini (medium)

![The bar chart compares latency between "o1-mini" and "o3-mini (medium)" models. "o3-mini" (lighter yellow) has lower latency, indicating faster response times, while "o1-mini" (darker yellow) takes longer on average.](https://images.ctfassets.net/kftzwdyauwt9/6sHe00x1MDPeWhYtQFHXVp/fb9c1f60d445da4a80e2d35d0010eae1/Latency_comparison.png?w=3840&q=90&fm=webp)

***Latency****: o3‑mini has an avg 2500ms faster time to first token than o1‑mini.*

## 安全

我们用于教导 OpenAI o3‑mini 安全回复的核心技术之一是[审慎对齐](/index/deliberative-alignment/)，即通过训练模型在回答用户指令前，先对人类编写的安全规范进行推理。与 OpenAI o1 类似，我们发现 o3‑mini 在具有挑战性的安全和越狱评估方面明显优于 GPT‑4o。在部署之前，我们采用与 o1 相同的防范准备、外部红队测试和安全评估，仔细评估了 o3‑mini 的安全风险。我们衷心感谢申请参与 o3‑mini 早期测试的安全测评人员。有关以下评估的详细信息，以及对潜在风险和我们缓解措施有效性的全面解释，请参阅 [o3‑mini 系统卡](/index/o3-mini-system-card/)。

### Disallowed content evaluations

![The table compares AI models on safety metrics, evaluating performance across different risk categories. It highlights variations in safety compliance, with some models performing better at reducing potential risks.](https://images.ctfassets.net/kftzwdyauwt9/7fNxs8WBlcqaVgF5aBof5X/14d4b8d89ec9cb63f4c38dd42ab60b55/Safety_Comparison_1.png?w=3840&q=90&fm=webp)

### Jailbreak Evaluations

![The table compares AI models on safety metrics across multiple risk categories, showing performance variations. It highlights differences in risk mitigation, with some models demonstrating stronger compliance and safer responses.](https://images.ctfassets.net/kftzwdyauwt9/5Wuh830TR8fkkzKvhVlldI/48151e4686526bef95c3145944481f1f/Safety_Comparison_2.png?w=3840&q=90&fm=webp)

## 下一步计划

OpenAI o3‑mini 的发布标志着 OpenAI 在突破高性价比智能技术发展方面又迈出了坚实的一步。通过优化 STEM 领域的推理，同时保持较低的成本，我们让更多人可以获得高质量的人工智能。这款模型延续了我们降低智能成本的一贯做法，自推出 GPT‑4 以来，每个令牌的定价降低了 95%，同时保持了顶级的推理能力。随着人工智能应用的不断扩大，我们将继续致力于引领前沿研究，打造兼顾智能、效率和安全的大规模模型。

## 作者

OpenAI

## 训练

Brian Zhang、Eric Mitchell、Hongyu Ren、Kevin Lu、Max Schwarzer、Michelle Pokrass、Shengjia Zhao、Ted Sanders

## 评估

Adam Kalai、Alex Tachard Passos、Ben Sokolowsky、Elaine Ya Le、Erik Ritter、Hao Sheng、Hanson Wang、Ilya Kostrikov、James Lee、Johannes Ferstad、Michael Lampe、Prashanth Radhakrishnan、Sean Fitzgerald、Sebastien Bubeck、Yann Dubois、Yu Bai

## 前沿评估与准备

Andy Applebaum、Elizabeth Proehl、Evan Mays、Joel Parish、Kevin Liu、Leon Maksin、Leyton Ho、Miles Wang、Michele Wang、Olivia Watkins、Patrick Chao、Samuel Miserendino、Tejal Patwardhan

## 工程

Adam Walker、Akshay Nathan、Alyssa Huang、Andy Wang、Ankit Gohel、Ben Eggers、Brian Yu、Bryan Ashley、Callie Riggins Zetino、Chengdu Huang、Christian Hoareau、Davin Bogan、Emily Sokolova、Eric Horacek、Eric Jiang、Felipe Petroski Such、Jonah Cohen、Josh Gross、Justin Becker、Kan Wu、Kevin Whinnery、Larry Lv、Lee Byron、Lien Mamitsuka、Manoli Liodakis、Max Johnson、Mike Trpcic、Murat Yesildal、Rasmus Rygaard、RJ Marsan、Rohit Ramchandani、Rohan Kshirsagar、Roman Huet、Sara Conlon、Shuaiqi (Tony) Xia、Siyuan Fu、Srinivas Narayanan、Sulman Choudhry、Surya Mamidyala、Tomer Kaftan、Trevor Creech

## 搜索

Adam Fry、Adam Perelman、Brandon Wang、Cristina Scheau、Philip Pronin、Sundeep Tirumalareddy、Will Ellsworth、Zewei Chu

## 产品

Antonia Woodford、Beth Hoover、Jake Brill、Kelly Stirman、Minnia Feng、Neel Ajjarapu、Nick Turley、Nikunj Handa、Olivier Godement

## 安全性

Alex Beutel、Andrea Vallone、Andrew Duberstein、Enis Sert、Eric Wallace、Grace Zhao、Irina Kofman、Jieqi Yu、Joaquin Quinonero Candela、Madelaine Boyd、Matt Jones、Mehmet Yatbaz、Mike McClay、Mingxuan Wang、Saachi Jain、Sandhini Agarwal、Sam Toizer、Santiago Hernández、Steve Mostovoy、Young Cha、Tao Li、Yunyun Wang

## 外部红队测试

Lama Ahmad、Michael Lampe、Troy Peterson

## 研究项目经理

Carpus Chang、Kristen Ying

## 领导团队

Aidan Clark、Dane Stuckey、Jerry Tworek、Jakub Pachocki、Johannes Heidecke、Kevin Weil、Liam Fedus、Mark Chen、Sam Altman、Wojciech Zaremba

+ [o1 背后的所有贡献者⁠](/zh-Hans-CN/openai-o1-contributions/)。

研究

* [研究索引](/zh-Hans-CN/research/index/)
* [研究概览](/zh-Hans-CN/research/)
* [经济研究](/zh-Hans-CN/signals/)

最新进展

* [GPT-5.5](/zh-Hans-CN/index/introducing-gpt-5-5/)
* [GPT-5.4](/zh-Hans-CN/index/introducing-gpt-5-4/)
* [GPT-5.3 Instant](/zh-Hans-CN/index/gpt-5-3-instant/)

安全

* [安全措施](/zh-Hans-CN/safety/)
* [部署安全（在新窗口中打开）](https://deploymentsafety.openai.com/)
* [安全与隐私](/zh-Hans-CN/security-and-privacy/)
* [信任与透明度](/zh-Hans-CN/trust-and-transparency/)

ChatGPT

* [ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=2ef666d5-d68e-41a5-8af7-70903e4e76cc&openaicom_referred=true)
* [ChatGPT Business（在新窗口中打开）](https://chatgpt.com/business/?openaicom-did=2ef666d5-d68e-41a5-8af7-70903e4e76cc&openaicom_referred=true)
* [ChatGPT Enterprise（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/enterprise/?openaicom-did=2ef666d5-d68e-41a5-8af7-70903e4e76cc&openaicom_referred=true)
* [ChatGPT for Education（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/education/?openaicom-did=2ef666d5-d68e-41a5-8af7-70903e4e76cc&openaicom_referred=true)
* [Codex](/zh-Hans-CN/codex/)
* [发布说明](/products/release-notes/)

API 平台

* [平台概览](/zh-Hans-CN/api/)
* [API 登录（在新窗口中打开）](https://platform.openai.com/login)
* [文档（在新窗口中打开）](https://developers.openai.com/api/docs)

Business

* [概览](/zh-Hans-CN/business/)
* [解决方案](/zh-Hans-CN/solutions/)
* [资源](/zh-Hans-CN/business/learn/)
* [联系销售团队](/zh-Hans-CN/contact-sales/)

开发者

* [Apps SDK（在新窗口中打开）](https://developers.openai.com/apps-sdk)
* [开放模型](/zh-Hans-CN/open-models/)
* [文档（在新窗口中打开）](https://developers.openai.com/)
* [资源（在新窗口中打开）](https://developers.openai.com/learn)
* [开发者论坛（在新窗口中打开）](https://community.openai.com/)

公司

* [关于我们](/zh-Hans-CN/about/)
* [我们的宪章](/charter/)
* [工作机会](/careers/)
* [新闻](/zh-Hans-CN/news/)

支持

* [帮助中心（在新窗口中打开）](https://help.openai.com/)

更多

* [客户案例](/zh-Hans-CN/stories/)
* [Academy](/academy/)
* [直播](/zh-Hans-CN/live/)
* [播客](/zh-Hans-CN/podcast/)
* [RSS](/news/rss.xml)

条款与政策

* [使用条款](/zh-Hans-CN/policies/terms-of-use/)
* [隐私政策](/zh-Hans-CN/policies/privacy-policy/)
* [其他政策](/zh-Hans-CN/policies/)

[（在新窗口中打开）](https://x.com/OpenAI)[（在新窗口中打开）](https://www.youtube.com/OpenAI)[（在新窗口中打开）](https://www.linkedin.com/company/openai)[（在新窗口中打开）](https://github.com/openai)[（在新窗口中打开）](https://www.instagram.com/openai/)[（在新窗口中打开）](https://www.tiktok.com/@openai)[（在新窗口中打开）](https://discord.gg/openai)

OpenAI © 2015–2026你的隐私选择

中文中国

![](https://bat.bing.com/action/0?ti=187204252&Ver=2&mid=da2936a4-4bce-4d9a-bd20-342d2676bf43&bo=1&sid=2cffb1306a7a11f1b47b6354b14962ab&vid=2cffa8306a7a11f1a1832db85fa4426e&vids=1&msclkid=N&pi=918639831&lg=zh-CN&sw=1440&sh=900&sc=24&tl=OpenAI%20o3-mini%20%7C%20OpenAI&p=https%3A%2F%2Fopenai.com%2Fzh-Hans-CN%2Findex%2Fopenai-o3-mini%2F&r=&lt=3353&evt=pageLoad&sv=2&cdb=AQAQ&rn=471863)
