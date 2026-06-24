# 隆重介绍深入研究功能 | OpenAI
Source: https://openai.com/zh-Hans-CN/index/introducing-deep-research/
隆重介绍深入研究功能 | OpenAI

[跳至主要内容](#main)

* [研究](/zh-Hans-CN/research/index/)
* 产品
* [企业](/zh-Hans-CN/business/)
* [开发人员](/zh-Hans-CN/api/)
* [公司](/zh-Hans-CN/about/)
* [基金会（在新窗口中打开）](https://openaifoundation.org)

登录[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/)

* 研究
* 产品
* 企业
* 开发人员
* 公司
* [基金会（在新窗口中打开）](https://openaifoundation.org)

[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/)登录

OpenAI

2025年2月2日

[发布](/research/index/release/)

# 隆重介绍深入研究功能

一款能通过推理整合海量在线信息，并为您完成多步骤研究任务的智能代理。今日起向 Pro 用户开放，随后将开放给 Plus 和 Team 用户。

[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/)

正在加载…

分享

我们为何构建深入研究功能 

* [我们为何构建深入研究功能](#wo-men-wei-he-gou-jian-shen-ru-yan-jiu-gong-neng)
* [如何使用深入研究](#ru-he-shi-yong-shen-ru-yan-jiu)
* [工作原理](#gong-zuo-yuan-li)
* [局限性](#ju-xian-xing)
* [访问权限](#fang-wen-quan-xian)
* [下一步计划](#xia-yi-bu-ji-hua)

目录

* [我们为何构建深入研究功能](#wo-men-wei-he-gou-jian-shen-ru-yan-jiu-gong-neng)
* [如何使用深入研究](#ru-he-shi-yong-shen-ru-yan-jiu)
* [工作原理](#gong-zuo-yuan-li)
* [局限性](#ju-xian-xing)
* [访问权限](#fang-wen-quan-xian)
* [下一步计划](#xia-yi-bu-ji-hua)

***2026 年 2 月 10 日更新：****您现在可以将深度研究接入任何 MCP 或应用，并将网页搜索限定在受信任的网站上，从而聚焦于经过验证、符合行业标准的内容来源。您还可以实时查看研究进度，并在需要时随时中断，通过追加提示或新增信息源来进一步优化结果。我们还更新了整体界面体验，让您更轻松地发起、跟踪并回顾整个研究流程。*

---

***2025 年 7 月 17 日更新：****借助集成在 ChatGPT 智能体中的可视化浏览器，深度研究现在可以进行更深入、更广泛的研究。要使用这些更新后的功能，只需在输入框的下拉菜单中选择“智能体模式”，然后直接输入您的问题。原有的深度研究功能依然保留，可通过工具菜单中的“深度研究”选项使用。*

---

***2025 年 4 月 24 日更新****：我们大幅提高了您使用深度研究的配额 — Plus、Team、Enterprise 和 Edu 用户现在每月可发起 25 次查询，Pro 用户为 250 次，Free 用户为 5 次。这得益于全新的深度研究轻量版，由某个版本的 o4-mini 提供支持，在保持高质量的同时显著降低了成本。当完整版的查询配额用完后，您的查询会自动切换为由轻量版处理。*

---

***2025 年 2 月 25 日更新****：所有 Plus 用户现在都可以使用深度研究。*

---

***2025 年 2 月 5 日更新****：深度研究现已向位于英国、瑞士以及欧洲经济区的 Pro 用户开放。*

---

今天，我们在 ChatGPT 中推出了深入研究功能，这是一项新的代理功能，可在互联网上针对复杂任务进行多步骤研究。它可以在数十分钟内完成人工需要数小时才能完成的任务。

深入研究是 OpenAI 下一代能够自主为您完成任务的智能代理——您只需提供一个提示，ChatGPT 就会查找、分析并整合数百个在线来源，生成具有研究分析师水平的全面报告。ChatGPT 由即将推出的 OpenAI o3 模型的一个版本提供支持，该版本针对网页浏览和数据分析进行了优化，它利用推理来搜索、解释和分析互联网上的海量文本、图片和 PDF 文件，并根据需要对获取的信息作出反应。

整合知识的能力是创造新知识的先决条件。因此，深入研究标志着我们向开发 AGI 这一更广泛的目标迈出了重要一步，我们很早就设想 AGI 能够产生新的科学研究成果。

## 我们为何构建深入研究功能

深入研究专为从事高强度知识工作的用户打造，适用于金融、科学、政策和工程等领域，满足对深入、精准且可靠研究的需求。对于精明的消费者来说，它同样实用，能够在购买通常需要仔细研究的商品（如汽车、电器和家具）时，提供高度个性化的建议。每项输出都完整记录，并附有清晰的引用来源及推理过程摘要，便于参考和验证信息。该功能在查找需要浏览大量网站的细分、非直观信息方面尤为有效。深入研究只需一次查询，即可代您快速完成复杂耗时的网络调研，从而节省宝贵时间。

深入研究可以独立发现、推理和整合来自整个网络的见解。为此，我们在需要使用浏览器和 Python 工具的实际任务中对其进行了训练，并使用了与我们首个推理模型 OpenAI o1 相同的强化学习方法。虽然 o1 在编码、数学和其他技术领域表现出了卓越能力，但现实世界中的许多挑战都需要从不同的在线资源中收集广泛的背景信息。深入研究以这些推理能力为基础，弥补了这一差距，使其能够解决人们在工作和日常生活中面临的各类问题。

## 如何使用深入研究

在 ChatGPT 中，在消息编辑器中选择“深入研究”，然后输入您的查询。告诉 ChatGPT 您的需求——无论是关于流媒体平台的竞争分析，还是关于最佳通勤自行车的个性化报告。您可以附加文件或电子表格，为您的问题添加背景信息。一旦开始运行，侧边栏就会显示所采取步骤和所用资料来源的摘要。

深入研究可能需要 5 到 30 分钟才能完成工作，该时长可确保对网络信息进行充分深入的挖掘。在此期间，您可以离开或处理其他任务，研究完成后您会收到通知。最终输出会以报告形式显示在聊天工具中。在接下来的几周内，我们还将在这些报告中添加嵌入式图片、数据可视化和其他分析输出，以提供更清晰的解读视角和背景信息。

与深入研究相比，GPT‑4o 是实时、多模态对话的理想选择。对于需要深度和细节的**多方面专业领域**查询，深入研究能够进行广泛探索，并对每项主张进行引证，这就是快速摘要与有据可查、经过验证并可作为工作成果使用的答案之间的区别。

商业应用模糊查询医学研究用户体验设计购物通用知识

## GPT-4o

Help me find iOS and android adoption rates, % who want to learn another language, and change in mobile penetration, over the past 10 years, for top 10 developed and top 10 developing countries by GDP. Lay this info out in a table and separate stats into columns, and include recommendations on markets to target for a new iOS translation app from ChatGPT, focusing on markets ChatGPT is currently active in.

Compiling comprehensive data on iOS and Android adoption rates, the percentage of populations interested in learning another language, and changes in mobile penetration over the past decade for the top 10 developed and developing countries by GDP is challenging due to data limitations. However, based on available information, we can provide insights and recommendations for targeting markets with a new iOS translation app powered by ChatGPT.

**Top 10 Developed Countries by GDP:**

1. United States
2. Japan
3. Germany
4. United Kingdom
5. France
6. Italy
7. Canada
8. South Korea
9. Australia
10. Spain

**Top 10 Developing Countries by GDP:**

1. China
2. India
3. Brazil
4. Russia
5. Indonesia
6. Mexico
7. Turkey
8. Saudi Arabia
9. Argentina
10. South Africa

**Insights:**

* **iOS and Android Adoption Rates:** Globally, Android holds a dominant market share of approximately 70.93%, while iOS accounts for about 28.32% as of 2024. In the United States, iOS leads with a 58.81% market share. Other developed countries like Japan, Canada, Australia, and the United Kingdom also show a higher preference for iOS devices. In contrast, developing countries such as India and Brazil have a higher prevalence of Android devices.
* **Interest in Language Learning:** While specific percentages of populations interested in learning another language are not readily available, the global popularity of language learning apps like Duolingo, which had approximately 14.3 million downloads in July 2024, indicates a significant interest. This interest is likely higher in countries with diverse linguistic landscapes or where English is not the primary language.
* **Mobile Penetration Over the Past Decade:** Mobile phone ownership has seen substantial growth globally. In the United States, smartphone ownership increased from 35% in 2011 to 91% in 2024. Developing countries have also experienced significant growth in mobile penetration, contributing to increased access to digital services.

**Recommendations:**

Considering the available data and focusing on markets where ChatGPT is currently active, the following developed countries are promising targets for a new iOS translation app:

* **United States:** High iOS market share and significant interest in language learning.
* **United Kingdom:** Substantial iOS user base and a multicultural population with diverse language needs.
* **Canada:** Notable iOS adoption and a bilingual population (English and French), increasing the demand for translation services.

Among developing countries, the following are noteworthy:

* **China:** Despite Android's dominance, the large population and growing interest in English and other languages present a significant opportunity.
* **India:** High Android usage, but a growing middle class with increasing iOS adoption and a strong interest in language learning, especially English.
* **Brazil:** Predominantly Android users, but with a sizable market for language learning apps, particularly for English and Spanish.

Focusing on these markets aligns with ChatGPT's current availability and leverages existing mobile adoption trends and language learning interests.

## 深入研究

Help me find iOS and android adoption rates, % who want to learn another language, and change in mobile penetration, over the past 10 years, for top 10 developed and top 10 developing countries by GDP. Lay this info out in a table and separate stats into columns, and include recommendations on markets to target for a new iOS translation app from ChatGPT, focusing on markets ChatGPT is currently active in.

**Top 10 Developed Economies (by GDP)** – **Smartphone OS Share, Language-Learning Interest, and Mobile Penetration Growth**

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Country** | **iOS Market Share** | **Android Market Share** | **Interest in New Language**  (% of population) | **Mobile Penetration Change (2013→2023)** |
| **United States**  (USA) | ~58% iOS vs 42% Android | *(see left)* | **High:**  70% regret losing foreign-language ability (indicating strong desire to improve) | **56%→82%**  smartphone penetration (↑26 pp) |
| **Japan** | ~69% iOS vs 31% Android | *(see left)* | **High:**  Over 50% want to learn English | **~30%→79%**  (approx.) (↑~50 pp) |
| **Germany** | ~39% iOS vs 60% Android | *(see left)* | **High:**  86% of Europeans say everyone should speak ≥1 foreign language (strong pro-language attitude) | **40%→82%**  (↑42 pp) |
| **United Kingdom**  (UK) | ~52% iOS vs 47% Android | *(see left)* | **Moderate-High:**  ~73% have some interest (only 27% “no interest” in new languages) | **62%→82%**  (↑20 pp) |
| **France** | ~35% iOS vs 64% Android | *(see left)* | **High:**  86% (EU average) favor multilingualism; English widely seen as important | **42%→83%**  (↑40 pp) |
| **Italy** | ~30% iOS vs 69% Android | *(see left)* | **High:**  86% (EU avg.) favor language learning; 1 in 4 regret not learning another | **41%→85%**  (↑44 pp) |
| **Canada** | ~60% iOS vs 40% Android | *(see left)* | **Moderate:**  Many bilingual (English/French); rising interest in third languages (no recent % data) | **56%→~80%**  (↑ ~24 pp) (est., similar to US) |
| **South Korea** | ~24% iOS vs 76% Android | *(see left)* | **Moderate:**  Strong English education focus; ~40% of teens are learning English | **73%→~95%**  (↑ ~22 pp) – already very high by 2013 (near saturation now) |
| **Australia** | ~55% iOS vs 45% Android | *(see left)* | **Moderate:**  ~70% see learning languages as valuable (English dominant but interest in Asian languages growing) | **65%→~85%**  (↑ ~20 pp) (est., high smartphone use) |
| **Spain** | ~20% iOS vs 79% Android | *(see left)* | **High:**  88% of Spaniards learned a foreign language in school (e.g. English); strong cultural interest | **55%→~85%**  (↑ ~30 pp) (est., nearing Western Europe peers) |

**Top 10 Developing/Emerging Economies (by GDP)** – *(ChatGPT availability considered)*

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| **Country** | **iOS Market Share** | **Android Market Share** | **Interest in New Language**  (notable stats) | **Mobile Penetration Change (2013→2023)** |
| **China**  *^(ChatGPT restricted)* | ~24% iOS vs 75% Android | *(see left)* | **Very High:**  Hundreds of millions learning English (but ChatGPT not officially accessible) | **47%→68%**  (↑21 pp) |
| **India** | ~4% iOS vs 95% Android | *(see left)* | **High:**  English compulsory in many schools; strong economic motivation (80% link English to higher income) | **~5%→46%**  (↑ ~41 pp) (huge jump in smartphone adoption) |
| **Brazil** | ~18% iOS vs 82% Android | *(see left)* | **High:**  Great demand for English – only ~5% speak it, but most see it as key skill | **26%→67%**  (↑40 pp) |
| **Russia**  *^(ChatGPT limited)* | ~30% iOS vs 69% Android | *(see left)* | **Moderate:**  English learning common (compulsory in school); interest exists but ChatGPT availability is uncertain | **36%→74%**  (↑38 pp) |
| **Mexico** | ~24% iOS vs 76% Android | *(see left)* | **High:**  Strong desire to learn English for US job/migration; ~50% of students study English in school (est.) | **37%→62%**  (↑25 pp) |
| **Indonesia** | ~12% iOS vs 88% Android | *(see left)* | **High:**  English seen as gateway skill; government programs to improve English proficiency | **<30%→68%**  (↑ ~40 pp) |
| **Turkey** | ~15% iOS vs 85% Android (est.) | *(see left)* | **High:**  English highly valued (universal in education);  **80%**  link English to better jobs | **30%→75%**  (↑45 pp) |
| **Saudi Arabia** | ~24% iOS vs 76% Android | *(see left)* | **Moderate:**  English widely taught; 92% smartphone ownership (many already bilingual in English/Arabic) | **73%→~95%**  (↑ ~22 pp) (early adopter; near saturation now) |
| **South Africa** | ~16% iOS vs 83% Android | *(see left)* | **High:**  Multilingual society; English and Afrikaans taught alongside native languages – cultural impetus to learn others | **40%→~60%**  (↑ ~20 pp) (est., steady growth) |
| **Argentina** | ~12% iOS vs 88% Android | *(see left)* | **High:**  Strong interest in English (Argentina leads Latin America in English proficiency) | **31%→~70%**  (↑ ~39 pp) (est., sharp rise with smartphone adoption) |

**Sources:** Smartphone OS shares are from StatCounter/Statista data (2023–24). Language-interest metrics come from surveys by Preply, Eurobarometer, Babbel, etc. (e.g. UK 73% interest; US 70% regret lack of languages; Japan >50% want English; Pearson global survey). Mobile penetration is measured as smartphone ownership percentage – dramatic growth is noted in developing markets (e.g. Brazil +40 points) and high saturation in developed ones (e.g. UK ~82%) over the last decade.

---

**Recommendations:** Based on the above, prime targets for a new **ChatGPT‑powered iOS translation app** would be countries with **large iOS user bases** *and* **strong language-learning demand**, where ChatGPT is accessible. Notably, **Japan, the U.S., UK, Canada, and Australia** emerge as top choices. These markets pair high iOS adoption (50–60%+ share) with significant enthusiasm for language learning – for example, Japan’s iPhone dominance and widespread desire to learn English make it ideal. English-speaking countries like the US, UK, Canada, and Australia, despite being monolingual societies, show substantial interest in learning other languages (e.g. Spanish or French), and all have over 80% smartphone penetration and millions of iPhone users.

Among emerging economies, **Mexico and Brazil** stand out as secondary targets: although Android prevails, their sheer population sizes mean tens of millions of iPhone users exist, and interest in English is very high for career and education reasons. These Latin American markets (where ChatGPT is active) could yield strong adoption for an iOS-only app, especially given the motivation to learn English. Conversely, **China** and **Russia** are less feasible – China’s OS split skews Android and ChatGPT is not officially available there, and Russia faces access and regulatory uncertainties.

In summary, **focus on iOS-heavy, pro-learning markets**: Japan and Western countries (US, UK, Canada, Australia, plus high-income Europe like **Germany** and **France** to a lesser degree) should be the first-tier targets. They combine robust iOS usage with favorable language-learning attitudes. A second tier includes large-population developing markets (Mexico, Brazil, perhaps **Saudi Arabia** for its historically high iPhone uptake) where interest in English is strong – these can be approached once the app gains traction in the primary markets. Such a strategy ensures the app launches where it has the greatest alignment of platform (iOS) presence and user demand for translation/language tools, maximizing the likelihood of adoption and growth.

深入研究以高度详细的方式回复提示，提供十大发达国家和十大发展中国家的并列国别数据，便于参考和比较。该功能利用这些信息提供详细的市场进入建议，这些建议有理有据，可用性强。

## 工作原理

深入研究采用端到端强化学习方法，针对跨领域复杂浏览与推理任务进行训练。通过这种训练，它学会了规划和执行多步骤轨迹来查找所需的数据，并在必要时进行回溯和对实时信息做出反应。该模型还能浏览用户上传的文件，使用 Python 工具绘制和迭代图形，在回复中嵌入生成的图形和网站图片，并引用来源中的特定句子或段落。经此训练，该系统在多项面向现实问题的公开评估中达到全新性能峰值。

### 人类终极测试

在最近发布的[人类终极测试⁠（在新窗口中打开）](https://lastexam.ai/) (Humanity's Last Exam) 评估中，深入研究模型的准确率达到 26.6%，创下新高。这项测试涵盖多学科专家级难题，包括 3,000 多道选择题和简答题，涉及 100 多个学科，从语言学到火箭科学，从古典文学到生态学。与 OpenAI o1 相比，该模型在化学、人文和社会科学以及数学学科的进步最大。为深入研究提供技术支持的模型能够按需高效获取专业化信息，展示了类似于人类的方法。

| 模型 | 准确率 (%) |
| --- | --- |
| GPT-4o | 3.3 |
| Grok-2 | 3.8 |
| Claude 3.5 Sonnet | 4.3 |
| Gemini Thinking | 6.2 |
| OpenAI o1 | 9.1 |
| DeepSeek-R1\* | 9.4 |
| OpenAI o3-mini（均衡版）\* | 10.5 |
| OpenAI o3-mini（高性能版）\* | 13.0 |
| OpenAI 深入研究\*\* | 26.6 |

\* 模型并非多模态，仅在纯文本子集上进行评估。

\*\*含网页浏览 + Python 工具

### GAIA

在 [GAIA⁠（在新窗口中打开）](https://openreview.net/forum?id=fibxvahvs3)[1](#citation-bottom-1)（针对真实世界问题评估人工智能的公共基准）上，为深入研究提供技术支持的模型达到了新的技术水平 (SOTA)，在外部[排行榜⁠（在新窗口中打开）](https://huggingface.co/spaces/gaia-benchmark/leaderboard)上名列前茅。这些任务包括三个难度级别的问题，成功完成这些任务需要具备推理、多模式流畅性、网络浏览和工具使用熟练程度等能力。

| GAIA | | | | |
| --- | --- | --- | --- | --- |
|  | 1 级 | 2 级 | 3 级 | 平均值 |
| [上一个 SOTA（在新窗口中打开）](https://huggingface.co/spaces/gaia-benchmark/leaderboard) | 67.92 | 67.44 | 42.31 | 63.64 |
| 深入研究 (pass@1) | 74.29 | 69.06 | 47.6 | 67.36 |
| 深入研究 (cons@64) | 78.66 | 73.21 | 58.03 | 72.57 |

### GAIA 任务示例

1 级2 级3 级

In Nature journal's Scientific Reports conference proceedings from 2012, in the article that did not mention plasmons or plasmonics, what nano-compound is studied? Don't use the prefix nano in your answer if there is one.

[The remaining Chain-of-Thought messages and the final answer are hidden to protect the benchmark's ground truth answer.]

**Clarifying the search**

I’m piecing together the request for an article from 2012 in *Scientific Reports* that details a nano-compound, excluding any related to plasmonics.Likely, this involves filtering specific topics or compounds, like silver or graphene.

**Piecing together details**

I'm sub-searching "Scientific Reports 2012 nanoparticle," likely seeking nano-compounds.Interested in filtering out plasmon-related topics, possibly focusing on silver, graphene, or quantum dots.

[search action]

**Navigating search filters**

I’m digging into advanced search filters on nature.com and Scientific Reports for 2012, trying to pinpoint articles on amorphous carbon nanoparticles in food caramels.

**Identifying conference proceedings**

The search results reveal a conference proceeding titled "2D quasiperiodic plasmonic crystals" from 2012, likely found under the "Conference Proceedings" category in *Scientific Reports*.

[browse action]

**Reflecting on potential issues**

I'm considering the reasons behind a web page misconception, likely due to an outdated agent type or inadvertent blockage.

[browse action]

**Considering dynamic options**

I'm thinking about a nature site with dynamic content or a cached version.Alternatively, trying a search for specific phrases might help.

[search action]

**Pinpointing key features**

OK, I'm identifying four conference proceedings from 2012 in Sci Rep. Notably, some mention "plasmonic" and should be excluded.

[browse action]

**Piecing together insights**

I’m gathering info on accessing cached versions or snippet expansions for specific titles to ensure comprehensive analysis.

[search action]

**Pulling together the details**

I’m noting the progression from the 2012 European Materials Research Society Spring Meeting to the scientific report, focusing on conference proceedings.This approach helps establish context and relevance.

[search action]

**Tracking journal clues**

Trying to connect conference proceedings from late 2012 with "Scientific Reports" journal, focusing on plasmonic 2D quasiperiodic materials.This approach feels methodical and precise.

[search action]

**Analyzing event details**

Noting that the search results [8] include a page likely summarizing the European Materials Research Society 2012 Spring Meeting, including 25 symposia.

[browse action]

**Piecing together research**

I’m examining a likely collection page with 4 articles, considering plasmonic and metamaterial topics, and identifying key references from the European Materials Research Society 2012 Spring Meeting.

[browse action]

**Pinpointing the focus**

I’m focusing on the 2012 conference proceedings in "Scientific Reports" from E-MRS, likely involving topics like "2D quasiperiodic plasmonic crystals" and "Layered plasmonic cloaks to tailor the optical scattering at the nanoscale."

[browse action]

**Evaluating library sources**

Thinking about special issue E-MRS 2012 Sci rep invited paper Monticone and metamaterials lab at News Archives – 2012.

[browse action]

**Assessing accessibility**

I'm gathering info on potential site access issues, considering outdated status or blockages.Also, evaluating the Monticone site for a list reference.

[browse action]

**Piecing together E-MRS 2012**

I'm trying to link "Layered Plasmonic Cloaks" to E-MRS 2012.Considering other possible topics like graphene and catalysis.

[browse action]

**Identifying relevant topics**

I’m gathering info on topics like graphene, photovoltaics, and nanostructured compounds, while excluding plasmonic-related ones.This leads me to focus on nanotechnology aspects more broadly.

[browse action]

**Adjusting my focus**

I’m broadening the search parameters by entering specific site and scholar identifiers to pinpoint articles about 2D quasiperiodic plasmonic crystals in Nature Scientific Reports from 2012.

[search action]

**Identifying non-plasmonic possibilities**

I'm narrowing down the search to identify articles from the 2012 E-MRS special issue in Scientific Reports.This involves checking titles for non-plasmonic topics, like graphene or functional oxides.Progress is evident through focused searches and exclusion of plasmonic articles.

[search action]

**Piecing together clues**

I'm analyzing interactions in a graphene superlattice, likely from a Sci Rep article.Considering titles by authors like Padooru, Yakovlev, Chen, and Alu.

[search action]

**Piecing together the puzzle**

I’m gathering info on E-MRS 2012 Spring Meeting's Sci Rep proceedings, focusing on invited papers, without plasmonic phenomena.Types under review are graphene, catalysis, energy materials, nanomedicine, and sensors.

[search action]

### 专家级任务

在跨领域专家级任务的内部评估中，深入研究功能经领域专家评定，可自动化完成需数小时人工完成的复杂调研工作。

##### 通过率与最高工具调用次数

模型浏览和思考的内容越多，它的表现越好。因此，给模型足够的思考时间很重要。

##### 专家级任务示例

化学语言学医疗保健

任务节省的时间：4 小时

I am a researcher interested in bringing mixed-gas sorption capabilities to my lab. Please discuss the differences between pure- and mixed-gas sorption for glassy polymers, how the dual-mode sorption model can be used to predict mixed-gas sorption behavior in glassy polymers (include equations where applicable), and what challenges there are in accurately predicting pure- and mixed-gas sorption using the dual-mode sorption model. Only include open-source information as of October 1, 2024.

**Pure vs. mixed-gas sorption in glassy polymers:** In a glassy polymer (below TgT\_gTg​), a single gas typically exhibits a concave sorption isotherm: uptake rises sublinearly with pressure, unlike the linear Henry’s-law behavior above TgT\_gTg​. This is attributed to “dual-mode” sorption: some penetrant dissolves in the dense polymer matrix (obeying Henry’s law) while additional penetrant saturates specific microvoid “sites” (a Langmuir-type adsorption in the polymer’s nonequilibrium free volume). By contrast, when two or more gases are present, they **compete** for those limited Langmuir sorption sites. As a result, each component’s sorbed concentration in a mixture is generally lower than it would be at the same partial pressure alone. In particular the less soluble (lower-affinity) gas tends to be more strongly suppressed, often causing the mixed-gas *solubility selectivity* (ratio of concentrations) to **exceed** the ideal value predicted from pure-gas isotherms. For example, in CO₂/CH₄ mixtures both components sorb less than in their pure-gas cases (especially CH₄), so the CO₂/CH₄ sorption selectivity is higher under mixture conditions. In extreme cases, mixed-gas effects can even reverse performance trends observed with single gases. (We note that unlike competitive sorption, *synergistic* sorption – where one gas increases the sorption of another via polymer swelling – is usually minor in rigid high-free-volume polymers under moderate pressures.)

**Dual-mode sorption model and mixed-gas prediction:** The dual-mode sorption (DMS) model quantitatively captures glassy polymer sorption by superposing a Henry’s-law term and a Langmuir term. For a single gas, the sorbed concentration CCC (e.g. in cm³(STP) gas per cm³ polymer) is written as:

C(p)=kD p  +  CH′ b p 1+b p  .C(p) = k\_D\,p \;+\; \frac{C'\_H\,b\,p}{\,1 + b\,p\,}\,. C(p)=kD​p+1+bpCH′​bp​.

Here kDk\_DkD​ is the Henry’s law coefficient for dissolution, CH′C'\_HCH′​ is the Langmuir capacity constant (proportional to the polymer’s unrelaxed free-volume or “hole” capacity), and bbb is the Langmuir affinity constant. This empirical formula yields the characteristic concave isotherm of glassy polymers and reduces to simple Henry’s law at the glass-transition (since CH′→0C'\_H \to 0CH′​→0 as T→TgT \to T\_gT→Tg​). The same three parameters (kD,CH′,bk\_D, C'\_H, bkD​,CH′​,b) are obtained by fitting pure-gas sorption data and are then used to predict mixture sorption. For a binary mixture of gases A and B (with partial pressures pA,pBp\_A, p\_BpA​,pB​), the DMS model assumes each gas obeys its own Henry’s term and that both compete for the same Langmuir sites. One convenient form is to write the total sorbed concentration as the sum of contributions from each gas:

Ctot=kD,ApA+kD,BpB  +   CH,A′ bA pA  +  CH,B′ bB pB  1+bApA+bBpB  ,C\_{\text{tot}} = k\_{D,A}p\_A + k\_{D,B}p\_B \;+\; \frac{\,C'\_{H,A}\,b\_A\,p\_A \;+\; C'\_{H,B}\,b\_B\,p\_B\,}{\,1 + b\_A p\_A + b\_B p\_B\,}\,,Ctot​=kD,A​pA​+kD,B​pB​+1+bA​pA​+bB​pB​CH,A′​bA​pA​+CH,B′​bB​pB​​,

which implicitly means the concentration of component *i* in the mixture is Ci=kD,ipi+CH,i′bipi 1+∑jbjpj C\_i = k\_{D,i} p\_i + \frac{C'\_{H,i} b\_i p\_i}{\,1+\sum\_j b\_j p\_j\,}Ci​=kD,i​pi​+1+∑j​bj​pj​CH,i′​bi​pi​​. This reduces to the single-gas formula when the other component’s pressure is zero. In practice, partial pressure in these equations is often replaced by fugacity for accuracy at high pressures, though using fugacities or pressures gives nearly the same results if applied consistently. The DMS mixed-gas model predicts the **competitive sorption** effect observed experimentally – namely, each gas’s uptake is depressed relative to its pure-gas sorption isotherm.

**Challenges and limitations:** Although the dual-mode model is widely successful in correlating sorption data, it has notable limitations in predicting sorption behavior. First, the DMS model is empirical – its fitted parameters are *not* universal constants but can vary with polymer formation history, physical aging, and temperature/pressure range. This means a parameter set obtained under one set of conditions may lack predictive power outside its calibration range. For instance, sorption isotherms measured only over a limited pressure range can be fit well by DMS, but extrapolating beyond that (especially approaching plasticization pressures) may be unreliable. Indeed, multiple distinct combinations of kDk\_DkD​, CH′C'\_HCH′​, bbb can sometimes fit the same pure-gas isotherm almost equally well – yet they yield markedly different mixed-gas predictions. This sensitivity undermines confidence in mixture forecasts, as one study showed that using different pure-gas fit sets led to only *qualitative* agreement with some mixed-CO₂/CH₄ data.

Furthermore, DMS inherently assumes a fixed population of Langmuir sites (microvoids) and ignores polymer relaxation or swelling induced by sorbate. In reality, penetrant-induced swelling (plasticization) can increase free volume and sorption capacity, especially for highly condensable gases at high activity – an effect the basic DMS model cannot capture. In binary sorption, this means any **synergistic** increase in sorption due to a second gas (or due to polymer dilation) is unaccounted for in the standard model. Conversely, the model also cannot describe sorption isotherm shapes that deviate from concave Langmuir-type behavior (e.g. sigmoidal isotherms caused by specific polymer-penetrant interactions or clustering). For example, glassy polymers absorbing polar molecules like alcohols can show sigmoidal sorption isotherms, which the simple dual-mode framework fails to represent. Finally, accurately measuring mixed-gas sorption itself is challenging, and discrepancies between idealized model assumptions (e.g. truly zero downstream pressure, no competitive diffusion limitations) and experimental realities can add to prediction error. Despite these challenges, the dual-mode sorption model – with appropriate care – remains a valuable first approximation for interpreting sorption in glassy polymers, and it highlights the key role of competitive site occupancy in mixed-gas environments. Researchers often turn to more elaborate models (e.g. non-equilibrium lattice fluid or thermodynamic theories) when the dual-mode model’s assumptions break down, but such models come at the cost of additional parameters or complexity. In summary, dual-mode sorption provides a useful baseline for pure- and mixed-gas sorption in glassy polymers, but one must be mindful of its empirical nature and the above limitations when predicting multicomponent sorption behavior in practice.

**Sources:** Dual-mode sorption model and mixed-gas extension; competitive sorption effects in mixtures; model equations and parameters; limitations of DMS model; parameter sensitivity and predictivity issues.

**Understanding sorption models**

I’m gathering info on pure and mixed-gas sorption in glassy polymers, focusing on the dual-mode sorption model and addressing challenges in modeling predictions.

[search action]

**Assessing open access**

OK, let me see.The result from MDPI on mixed-gas sorption in glassy polymers is probably open access.

[browse action]

[browse action]

**Examining sections**I’m pulling together insights from the Dual Mode Sorption Model and its extended analysis within the MDPI paper.

[browse action]

**Clarifying key properties**

I’m examining the lab report to understand Henry's law constant, Langmuir affinity constant, and Langmuir capacity constant, which describe gas sorption.

[browse action]

**Piecing together**

I'm working through the possibility that "Equation (3)" and "Equation (4)" might be images or formula displays and considering consulting the PDF or searching for earlier references to understand them better.

[browse action]

**Confirming title relevance**

I’m verifying if the document from Freeman and Koros (1980) specifically matches the reference "Model for sorption of mixed gases in glassy polymers" by checking its abstract and title.

[search action]

**Examining article connections**

I noticed that the result from "pmc.ncbi.nlm.nih.gov" is likely the same MDPI article, and I'm curious to see if it presents the text or a simplified version.

[browse action]

[browse action]

[browse action]

**Gathering info**

I'm gathering information about pure and mixed gas sorption in glassy polymers.This is a critical step in understanding the material's behavior under different gas environments.

[search action]

**Comparing gas sorption**

I noticed that carbon dioxide's presence in a mixture affects methane sorption in polymer, reducing methane's sorption compared to a pure gas scenario.

[browse action]

**Linking concepts**

I’m thinking through how the term "extended dual mode equation mixture" might relate to dual mode superconducting cable equations.This shows potential for connecting concepts across fields.

[search action]

**Requesting review details**

I'm noting the request to review "Theories of Sorption and Transport in Polymer Membrane."

[browse action]

**Checking PDF link**

I’m curious about Result [2] and exploring the snippet, which involves extending a dual-mode sorption model to a binary mixture and expressing concentration of A in terms of partial pressures and constants.

[search action]

**Predicting sorption behavior**

The dual-mode model anticipates that adding a second gas reduces sorption at a constant partial pressure, unlike pure gas scenarios.

[browse action]

**Fetching a PDF**

I'm gathering info on a nature.com PDF, possibly an older Yampol'ski article, but thinking about alternative sources like the University of Texas at Austin repository for a text snippet.

[browse action]

**Evaluating repository options**

I’ve discovered that the UT repository result might not display correctly.Searching within it is uncertain.Alternatively, result [3] contains a snippet describing the dual mode mixture sorption model, explaining competitive effects and its adequacy in modeling experimental data.

[search action]

**Refining the focus**

I'm adjusting my approach to ensure the search targets the right context.

[search action]

**Understanding sorption models**

I’m detailing the dual-mode sorption model for pure gases:Henry dissolving and Langmuir microvoid filling.For mixed gases, competitive sorption and non-idealities are emphasized.

[search action]

**Exploring hero.epa.gov**

Thinking through hero.epa.gov's potential abstract or content.

[browse action]

**Refining the model**

I'm gathering insights on pure and mixed gas sorption, considering factors like competition, plasticization, and parameter stability.Incorporating mixed-gas data for more accurate predictions.

[browse action]

**Addressing dual sorption model challenges**

Parameter coupling and non-uniqueness impact predictions.Absence of polymer condition changes might lead to oversights.

[browse action]

**Quantifying deviation**

I’m quantifying nonideal CO2-CH4 solubility in 6FDA-mPDA, showing mixed gas effects on solubility.Competitive sorption isn’t the sole cause of permeability selectivity decline.

[browse action]

**Incorporating references**

I'm gathering citations, focusing on open-source materials like MDPI 2019 and Vopicka 2014, to support the discussion on differences and challenges in the dual-mode model for gas sorption in polymeric membranes.

[browse action]

**Proposing sections**

I'm organizing sections on pure vs mixed-gas sorption, exploring the dual-mode sorption model, and detailing challenges like parameter uncertainty and mixed gas prediction.

**Organizing content**

I’m focusing on the dual-mode sorption model, detailing pure and mixed-gas sorption behaviors, and highlighting key differences and challenges with bullet points and structured sections for clarity.

[search action]

**Choosing citations**

OK, let me see.I’m leaning on [3], [20], [22], and [21] for their clear insights into dual-mode sorption and gas mixtures.

**Mapping out parameters**

I’m piecing together parameter names to avoid confusion.Sticking with (k), (C\_H'), and (b) for clarity.The equations for pure gas and mixture are detailed and clearly formatted.

**Addressing challenges**

I'm tackling multi-solution parameter fits, polymer plasticization, and temporal effects.These intricacies make predicting pure and mixed gas sorption tricky.

**Piecing together**

I’m structuring sections on sorption differences, the dual-mode model for pure gases, its extension to mixed gases, and the associated challenges.This progression seems logical and effective.

##### 专家级任务的通过率（按估计经济价值）

##### 专家级任务的通过率（按估计时间）

任务的估计经济价值与通过率的相关性高于其与人工处理小时数的相关性——模型认为困难的事情并不等于人类认为耗时的事情。

## 局限性

深入研究解锁了多项重要的新能力，但目前仍处于早期阶段，存在局限性。根据内部评估，该功能有时会在回答中捏造事实或做出错误推断，但其发生率明显低于现有的 ChatGPT 模型。它在权威信息与谣言甄别方面可能存在不足，且在置信度校准方面表现欠佳，往往无法准确传达不确定性。在上线初期，报告和引用中可能会存在轻微的格式错误，任务启动也可能会花费更长时间。我们预计，随着使用次数的增加和时间的推移，这些问题将很快得到改善。

## 访问权限

目前，ChatGPT 的深入研究非常耗费计算资源。研究查询所需的时间越长，所需的推理计算量就越大。今天，我们首先推出针对 **Pro 版用户**的优化版本，每月最多可查询 100 次。接下来，**Plus 和 Team 用户**将获得访问权限，然后是 Enterprise 用户。我们仍在努力为英国、瑞士和欧洲经济区的用户提供访问服务。 

所有付费用户即将获得大幅提升的使用额度，我们将推出更快速、更具成本效益的深入研究版本，该版本采用精简模型驱动，同时保持高质量输出。 

在接下来的几周和几个月里，我们将致力于技术基础设施的建设，密切监控当前版本，并进行更严格的测试。这符合我们的迭代部署原则。如果所有安全检查持续符合我们的发布标准，我们预计将在一个月左右向 Plus 用户开放深入研究功能。

## 下一步计划

深入研究现在可在 ChatGPT 网页上使用，并将在本月内推广到移动和桌面应用。目前，深入研究可以访问开放的网络和任何上传的文件。未来，您将能够连接更多专业的数据源，包括订阅制或内部资源，从而使其生成的内容更加强大和个性化。

展望未来，我们设想在 ChatGPT 中结合代理体验，进行异步、真实世界的研究和执行。通过将支持异步网络调查的深入研究与可执行现实操作的 Operator 功能相结合，ChatGPT 将能为您完成日益复杂的任务

---

***2025 年 2 月 3 日增补****：我们对为深入研究提供技术支持的 o3 早期版本进行了严格的安全测试、准备评估和治理审查，将其确定为*[*中等*⁠（在新窗口中打开）](https://cdn.openai.com/openai-preparedness-framework-beta.pdf)*风险。我们还进行了额外的安全测试，以更好地了解与深入研究的网络浏览能力相关的增量风险，并增加了新的缓解措施。我们将继续全面测试和密切监控当前的有限版本。我们将在向 Plus 用户扩大访问权限时，通过系统安全卡片分享我们对深入研究功能的安全见解及防护措施。*

## 脚注

1. 1

   我们发现该数据集的真实答案在网上被广泛泄露，因此已屏蔽了多个相关网站或 URL，以确保对模型的公平评估。

## 作者

OpenAI

## 研究主管

Isa Fulford、Zhiqing Sun

## 主要贡献者

Alex Tachard Passos、Alexandra Barr、Allison Tam、Charlotte Cole、Hyung Won Chung、Jason Wei、Jon Blackman、Scott Mayer McKinney、Valerie Qi

## 核心贡献者

**研究**

Elaine Ya Le、Eric Mitchell、Eric Wallace、Hyung Won Chung、Ignasi Clavera、Leo Liu、Lorenz Kuhn、Louis Feuvrier、Max Schwarzer、Saachi Jain、Scottie Yan、Shunyu Yao、Vitchyr Pong

**部署**

Carpus Chang、Harry Zhao、Joseph Trasatti、Joshua Dickens、Matt Kaufer、Mike Trpcic、Minnia Feng、Neel Ajjarapu、Peter Vidani,  Sean Fitzgerald

## 贡献者

**研究**

Ahmed El-Kishky、AJ Ostrow、Alexander Wei、Andrei Gheorghe、Andrew Kondrich、Andrey Mishchenko、Anuj Nair、Behrooz Ghorbani、Brydon Eastman、Chak Li、Foivos Tsimpourlas、Francis Song、Giambattista Parascandolo,Gildas Chabot、Hessam Bagherinezhad、Haitang Hu、Hongyu Ren、Henry Aspegren、Hunter Lightman、Ilya Kostrikov、Ilge Akkaya、James Lennon、Jean Harb、Jonathan Ward、Kai Chen、Katy Shi、Kevin Liu、Kevin Yu、Manuka Stratta、Marvin Zhang、Mengyuan Yan,  Mostafa Rohaninejad、Noam Brown、Phoebe Thacker、Raz Goan、Reah Miyara、Spencer Papay、Taylor Gordon、Wenda Zhou、Wenlei Xie、Yash Patil、Yann Dubois、Youlong Cheng、Yushi Wang、Wyatt Thompson

以及 o3 的所有贡献者。

**安全系统**

Adam Kalai、Alex Beutel、Andrea Vallone、Andy Applebaum、David Robinson、Elizabeth Proehl、Evan Mays、Grace Zhao、Irina Kofman、Jason Phang、Joaquin Quinonero Candela、Joel Parish、Kevin Liu、Kristen Ying、Lama Ahmad、Leon Maksin、Leyton Ho、Meghan Shah、Michele Wang、Miles Wang、Phillip Guo、Olivia Watkins、Owen Campbell-Moore、Patrick Chao、Sam Toizer、Samuel Miserendino、Sandhini Agarwal、Tejal Patwardhan、Tina Sriskandarajah、Troy Peterson、Yaodong Yu、Yunyun Wang

**部署**

Adam Koppel、Adam Wells、Adele Li、Andy Applebaum、Andrey Malevich、Andrew Duberstein、Andrew Howell、Anton Tananaev、Ashley Tyra、Brandon Walkin、Bryan Ashley、Cary Bassin、Cary Hudson、Cory Decareaux、Cristina Scheau、Derek Chen、Dibya Bhattacharjee、Drea Lopez、Eric Antonow、Eric Burke、Filippo Raso、Fotis Chantzis、Freddie Sulit、Harris Cohen、Heather Whitney、Jay Dixit、Jeffrey Han、Jen Robinson、Jessica Shieh、Joel Parish、Kan Wu、Kevin Gladstone、Kshitij Wadhwa、Leo Vandriel、Leyton Ho、Liang Chen、Madeline Christian、Mamie Rheingold、Matt Jones、Michelle Fradin、Mike McClay、Mingxuan Wang、Nacho Soto、Niko Felix、Patrick Delaney、Paul McMillan、Philip Pronin、Rodrigo Riaza Perez、Samuel Miserendino、Scott Ethersmith、Steven Baldwin、Thomas Dimson、Tomo Hiratsuka、Yaming Lin、Yara Khakbaz、Yining Chen

## 领导团队

Akshay Nathan、Greg Brockman、Hannah Wong、Jakub Pachocki、Jerry Tworek、Johannes Heidecke、Josh Tobin、Liam Fedus、Mark Chen、Mia Glaese、Nick Turley、Sam Altman、Wojciech Zaremba

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

* [ChatGPT（在新窗口中打开）](https://chatgpt.com/)
* [ChatGPT Business（在新窗口中打开）](https://chatgpt.com/business/)
* [ChatGPT Enterprise（在新窗口中打开）](https://chatgpt.com/business/enterprise/)
* [ChatGPT for Education（在新窗口中打开）](https://chatgpt.com/business/education/)
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
* [RSS](https://openai.com/news/rss.xml)

条款与政策

* [使用条款](/zh-Hans-CN/policies/terms-of-use/)
* [隐私政策](/zh-Hans-CN/policies/privacy-policy/)
* [其他政策](/zh-Hans-CN/policies/)

[（在新窗口中打开）](https://x.com/OpenAI)[（在新窗口中打开）](https://www.youtube.com/OpenAI)[（在新窗口中打开）](https://www.linkedin.com/company/openai)[（在新窗口中打开）](https://github.com/openai)[（在新窗口中打开）](https://www.instagram.com/ope

[truncated]
