# Snowflake Arctic - LLM for Enterprise AI
Source: https://www.snowflake.com/en/blog/arctic-open-efficient-foundation-language-models-snowflake/
Snowflake Arctic - LLM for Enterprise AI




[Skip to content](#responsive-grid-main-content)

Product

Solutions

Why Snowflake

Resources

Developers

[Pricing](/en/pricing-options/)

Language

Languages

[English](/en/blog/arctic-open-efficient-foundation-language-models-snowflake/)[한국어](/ko/)[日本語](/ja/blog/arctic-open-efficient-foundation-language-models-snowflake/)[Português](/pt_br/blog/arctic-open-efficient-foundation-language-models-snowflake/)[Deutsch](/de/blog/arctic-open-efficient-foundation-language-models-snowflake/)[Français](/fr/blog/arctic-open-efficient-foundation-language-models-snowflake/)[Español](/es/blog/arctic-open-efficient-foundation-language-models-snowflake/)[Italiano](/it/blog/arctic-open-efficient-foundation-language-models-snowflake/)[中文（简体）](/zh_cn/)

[Sign in](https://app.snowflake.com/)

[CONTACT SALES](/en/contact-sales/)

[start for free](https://signup.snowflake.com/)

##### INSIDE THE DATA CLOUD

[##### ENGINEERING BLOG](/en/blog/engineering/)

[###### AI/ML](/en/blog/ai-ml/)[###### At Snowflake](/en/blog/company/)[###### Partner & Customer Value](/en/blog/customer-value/)[###### Industry Solutions](/en/blog/industry-solutions/)[###### Product & Technology](/en/blog/product-and-technology/)[###### Strategy & Insights](/en/blog/thought-leadership/)

##### INSIDE THE DATA CLOUD

[##### ENGINEERING BLOG](/en/blog/engineering/)

##### INSIDE THE DATA CLOUD

[##### ENGINEERING BLOG](/en/blog/engineering/)

[###### AI/ML](/en/blog/ai-ml/)[###### At Snowflake](/en/blog/company/)[###### Partner & Customer Value](/en/blog/customer-value/)[###### Industry Solutions](/en/blog/industry-solutions/)[###### Product & Technology](/en/blog/product-and-technology/)[###### Strategy & Insights](/en/blog/thought-leadership/)

[Blog](/en/blog/)/[Product and Technology](/en/blog/product-and-technology/)/Snowflake Arctic: The Best LLM for Enterprise AI — Efficiently Intelligent, Truly Open

Apr 24, 2024/13 min readProduct and Technology

# Snowflake Arctic: The Best LLM for Enterprise AI — Efficiently Intelligent, Truly Open

[![Snowflake AI Research](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--249da901-4810-48b7-ab40-99208c5e3b73/default-author-image.png?preferwebp=true&quality=85)

Snowflake AI Research](/en/blog/authors/snowflake-ai-research/)

![Snowflake Arctic: The Best LLM for Enterprise AI — Efficiently Intelligent, Truly Open](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--8cf68b94-88c5-481c-9145-719f03e2c9fb/snowflake-arctic-4-24-blog-hero.png?preferwebp=true&quality=85)

Building top-tier enterprise-grade intelligence using LLMs has traditionally been prohibitively expensive and resource-hungry, and often costs tens to hundreds of millions of dollars. As researchers, we have grappled with the constraints of efficiently training and inferencing LLMs for years. Members of the Snowflake AI Research team pioneered systems such as [ZeRO](https://arxiv.org/abs/1910.02054) and [DeepSpeed](https://github.com/microsoft/DeepSpeed), [PagedAttention](https://arxiv.org/abs/2309.06180) / [vLLM](https://github.com/vllm-project/vllm), and [LLM360](https://www.llm360.ai/) which significantly reduced the cost of [LLM training and inference](//www.snowflake.com/en/fundamentals/llm-inference/), and open sourced them to make LLMs more accessible and cost-effective for the community.   
  
Today, the Snowflake AI Research Team is thrilled to introduce Snowflake Arctic, a top-tier enterprise-focused [LLM](//www.snowflake.com/en/fundamentals/large-language-model/) that pushes the frontiers of cost-effective training and openness. Arctic is ***efficiently intelligent and truly open.***

* **Efficiently Intelligent:** Arctic excels at enterprise tasks such as SQL generation, coding and instruction following benchmarks even when compared to open source models trained with significantly higher compute budgets. In fact, it sets a new baseline for cost-effective training to enable Snowflake customers to create high-quality custom models for their enterprise needs at a low cost.

* **Truly Open:** Apache 2.0 license provides ungated access to weights and code. In addition, we are also open sourcing all of our data recipes and research insights.

Snowflake Arctic is available from Hugging Face, NVIDIA API catalog and Replicate today or via your model garden or catalog of choice, including Snowflake Cortex, Amazon Web Services (AWS), Microsoft Azure, Lamini, Perplexity and Together over the coming days.

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--6ac59123-d7c6-4527-a81a-4582a9660910/arctic-graph-breakthrough-efficiency-training-final%25403x-1.png?preferwebp=true&quality=85)

### Top-tier enterprise intelligence at incredibly low training cost

At Snowflake, we see a consistent pattern in AI needs and use cases from our enterprise customers. Enterprises want to use LLMs to build conversational SQL data copilots, code copilots and [RAG](//www.snowflake.com/en/fundamentals/rag/) chatbots. From a metrics perspective, this translates to LLMs that excel at SQL, code, complex instruction following and the ability to produce grounded answers. We capture these abilities into a single metric we call **enterprise intelligence** by taking an average of Coding (HumanEval+ and MBPP+), SQL Generation (Spider) and Instruction following (IFEval).

Arctic offers top-tier enterprise intelligence among open source LLMs, and it does so using a training compute budget of roughly under $2 million (less than 3K GPU weeks). This means Arctic is more capable than other open source models trained with a similar compute budget. More importantly, it excels at enterprise intelligence, even when compared to those trained with a significantly higher compute budget. The high training efficiency of Arctic also means that Snowflake customers and the AI community at large can train custom models in a much more affordable way.

As seen in Figure 1, Arctic is on par or better than both LLAMA 3 8B and LLAMA 2 70B on enterprise metrics, while using less than ½ of the training compute budget. Similarly, despite using 17x less compute budget, Arctic is on par with Llama3 70B in enterprise metrics like Coding (HumanEval+ & MBPP+), SQL (Spider) and Instruction Following (IFEval). It does so while remaining competitive on overall performance. For example, despite using 7x less compute than DBRX it remains competitive on Language Understanding and Reasoning (a collection of 11 metrics) while being better in Math (GSM8K). For a detailed breakdown of results by individual benchmark, see the Metrics section.

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--a3d21a5f-df62-4519-ae9b-c0afd4424066/table-3-1-1.png?preferwebp=true&quality=85)

### Training efficiency

To achieve this level of training efficiency, Arctic uses a unique Dense-MoE Hybrid transformer architecture. It combines a 10B dense transformer model with a residual 128x3.66B MoE MLP resulting in 480B total and 17B active parameters chosen using a top-2 gating. It was designed and trained using the following three key insights and innovations:

1) *Many-but-condensed experts with more expert choices:* In late 2021, the [DeepSpeed team demonstrated](https://arxiv.org/abs/2201.05596) that MoE can be applied to auto-regressive LLMs to significantly improve model quality without increasing compute cost.

In designing Arctic, we noticed, based on the above, that the improvement of the model quality depended primarily on the number of experts and the total number of parameters in the MoE model, and the number of ways in which these experts can be combined together.

Based on this insight, Arctic is designed to have 480B parameters spread across 128 fine-grained experts and uses top-2 gating to choose 17B active parameters. In contrast, recent MoE models are built with significantly fewer experts as shown in Table 2.  Intuitively, Arctic leverages a large number of total parameters and many experts to enlarge the model capacity for top-tier intelligence, while it judiciously chooses among many-but-condensed experts and engages a moderate number of active parameters for resource-efficient training and inference.

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--a07ea5e6-1d7f-4766-ac41-d955b3911795/figure-2-standard-moe-architecture-vs-arctic-4.png?preferwebp=true&quality=85)

2) *Architecture and System Co-design:*Training vanilla MoE architecture with a large number of experts is very inefficient even on the most powerful AI training hardware due to high all-to-all communication overhead among experts. However, it is possible to hide this overhead if the communication can be overlapped with computation.

Our second insight is that combining a dense transformer with a residual MoE component (Fig 2) in the Arctic architecture enables our training system to achieve good training efficiency via communication computation overlap, hiding a big portion of the communication overhead.  
  
3) *Enterprise-Focused Data Curriculum:* Excelling at enterprise metrics like Code Generation and SQL requires a vastly different data curriculum than training models for generic metrics. Over hundreds of small-scale ablations, we learned that generic skills like common sense reasoning can be learned in the beginning, while more complex metrics like coding, math and SQL can be learned effectively towards the latter part of the training. One can draw analogies to human life and education, where we acquire capabilities from simpler to harder. As such, Arctic was trained with a three-stage curriculum each with a different data composition focusing on generic skills in the first phase (1T Tokens), and enterprise-focused skills in the latter two phases (1.5T and 1T tokens). A high-level summary of our dynamic curriculum is shown here.

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--94db4708-b859-43fc-b138-1e8ff12e94c0/table-2-4.png?preferwebp=true&quality=85)

### Inference efficiency

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--11ebf03e-9986-4802-8411-6583e30ce13e/arctic-graph-breakthrough-efficiency-inference-final%25403x-1.png?preferwebp=true&quality=85)

Training efficiency represents only one side of the efficient intelligence of Arctic. Inference efficiency is equally critical to allow for the practical deployment of the model at a low cost. Arctic represents a leap in MoE model scale, using more experts and total parameters than any other open sourced auto-regressive MoE model. As such, several system insights and innovations are necessary to run inference on Arctic efficiently:

a) At interactive inference of a small batch size, e.g., batch size of 1, an MoE model’s inference latency is bottlenecked by the time it takes to read all the active parameters, where the inference is memory bandwidth bounded. At this batch size, Arctic (17B active parameters) can have up to 4x less memory reads than Code-Llama 70B, and up to 2.5x less than Mixtral 8x22B (44B active parameters), leading to faster inference performance.

We have collaborated with NVIDIA and worked with [NVIDIA TensorRT-LLM](https://developer.nvidia.com/blog/nvidia-tensorrt-llm-supercharges-large-language-model-inference-on-nvidia-h100-gpus/) and the [vLLM](https://github.com/vllm-project/vllm) teams to provide a preliminary implementation of Arctic for interactive inference. With FP8 quantization, we can fit Arctic within a single GPU node. While far from fully optimized, at a batch size of 1, Arctic has a throughput of over 70+ tokens/second for effective interactive serving.

b) As the batch size increases significantly e.g., thousands of tokens per forward pass, Arctic switches from being memory bandwidth bound to compute bound, where the inference is bottlenecked by the active parameters per token. At this point, Arctic incurs 4x less compute than CodeLlama 70B and Llama 3 70B.

To enable compute bound inference and high relative throughput that corresponds to the small number of active parameters in Arctic (as shown in Fig 3), a large batch size is needed. Achieving this requires having enough KV cache memory to support the large batch size while also having enough memory to store nearly 500B parameters for the model. While challenging, this can be achieved with two-node inference using a combination of system optimizations such as FP8 weights, split-fuse and continuous batching, tensor parallelism within a node and pipeline parallelism across nodes.

We have worked closely with NVIDIA to optimize inference for  NVIDIA NIM microservices powered by TensorRT-LLM. In parallel, we are working with the vLLM community, and our in-house development team is also enabling efficient inference of Arctic for enterprise use cases in the coming weeks.

### Truly open

Arctic was built upon the collective experiences of our diverse team, as well as major insights and learnings from the community. Open collaboration is key to innovation, and Arctic would not have been possible without open source code and open research insights from the community. We are thankful to the community and eager to give back our own learnings to enrich the collective knowledge and empower others to succeed.

Our commitment to a truly open ecosystem goes beyond open weights and code but also having open research insights and open source recipes.

#### Open research insights

The construction of Arctic has unfolded along two distinct trajectories: the open path, which we navigated swiftly thanks to the wealth of community insights, and the hard path, which is characterized by the segments of research that lacked prior community insights, necessitating intensive debugging and numerous ablations.

With this release, we’re not just unveiling the model; we’re also sharing our research insights through a comprehensive ‘cookbook’ that opens up our findings from the hard path. The cookbook is designed to expedite the learning process for anyone looking to build world-class MoE models. It offers a blend of high-level insights and granular technical details in crafting an LLM akin to Arctic so you can build your desired intelligence efficiently and economically — guided by the open path instead of the hard one.

The cookbook spans a breadth of topics, including pre-training, fine-tuning, inference and evaluation, and also delves into modeling, data, systems and infrastructure. You can preview [the table of contents](https://medium.com/@snowflake_ai_research/snowflake-arctic-cookbook-series-exploring-mixture-of-experts-moe-c7d6b8f14d16), which outlines over 20 subjects. We will be releasing corresponding Medium.com blog posts daily over the next month. For instance, we’ll disclose our strategies for sourcing and refining web data in “What data to use?”  We’ll discuss our data composition and curriculum in “How to compose data.” Our exploration of MoE architecture variations will be detailed in “Advanced MoE architecture,” discussing the co-design of model architecture and system performance. And for those curious about LLM evaluation, our “How to evaluate and compare model quality — less straightforward than you think” will shed light on the unexpected complexities we encountered.

Through this initiative, we aspire to contribute to an open community where collective learning and advancement are the norms to push the boundaries of this field further.

#### Open source serving code

* We are releasing model checkpoints for both the base and instruct-tuned versions of Arctic under an Apache 2.0 license. This means you can use them freely in your own research, prototypes and products.

* Our LoRA-based fine-tuning pipeline, complete with a recipe, allows for efficient model tuning on a single node.

* In collaboration with NVIDIA TensorRT-LLM and vLLM, we are developing initial inference implementations for Arctic, optimized for interactive use with a batch size of one. We are excited to work with the community to tackle the complexities of high-batch size inference of really large MoE models.

* Arctic is trained using a 4K attention context window. We are developing an attention-sinks-based sliding window implementation to support unlimited sequence generation capability in the coming weeks. We look forward to working with the community to extend to a 32K attention window in the near future.

##### Metrics

Our focus from a metrics perspective is primarily on what we call **enterprise intelligence** metrics, a collection of skills that are critical for enterprise customers that includes, Coding (HumanEval+ and MBPP+), SQL Generation (Spider) and Instruction following (IFEval).

At the same time, it is equally important to evaluate LLMs on the metrics the research community evaluates them on. This includes world knowledge, common sense reasoning and math capabilities. We refer to these metrics as **academic benchmarks**.

Here is a comparison of Arctic with multiple open source models across enterprise and academic metrics:

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--6bbf6ec4-3319-4b1e-a8a0-8ca54f49c102/snowflake-arctic-graph-enterprise-intelligence-horizontal-v02-scaled.jpg?preferwebp=true&quality=85)

For enterprise metrics, Arctic demonstrates top-tier performance compared to all other open source models regardless of the compute class. For other metrics, it achieves top-tier performance at its compute class and even remains competitive with models trained with higher compute budgets. Snowflake Arctic is the best open source model for off-the-shelf enterprise use cases. And if you are looking to train your own model from scratch at the lowest total cost of ownership (TCO), the training infrastructure and systems optimization descriptions in our cookbook should be of great interest.

For academic benchmarks, there has been a focus on world knowledge metrics such as MMLU to represent model performance. With high-quality web and STEM data, MMLU monotonically moves up as a function of training FLOPS. Since one objective for Arctic was to optimize for training efficiency while keeping the training budget small, a natural consequence is lower MMLU performance compared to recent top-tier models. In line with this insight, we expect our ongoing training run at a higher training compute budget than Arctic to exceed Arctic’s MMLU performance. We note that performance on MMLU world knowledge doesn’t necessarily correlate with our focus on enterprise intelligence.

![](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--981d2216-6343-41b4-a855-9f33977a7d3e/table-3-corrected.png?preferwebp=true&quality=85)

Table 3. Full Metrics Table. Comparing Snowflake Arctic with DBRX, LLAMA-3 8B, LLAMA-3 70B, Mixtral 8x7B, Mixtral 8x22B (instruction-tuned or chat variants if available).1 2 3

### Getting started with Arctic

Snowflake AI Research also recently announced and open sourced the Arctic Embed family of models that achieves SoTA in MTEB retrieval. We are eager to work with the community as we develop the next generation in the Arctic family of models. Join us at our Data Cloud Summit on June 3-6 to learn more.

Here's how we can collaborate on Arctic starting today:

* Go to [Hugging Face](https://huggingface.co/Snowflake/snowflake-arctic-instruct) to directly download Arctic and use our [Github repo](https://github.com/Snowflake-Labs/snowflake-arctic) for inference and fine-tuning recipes.
* For a serverless experience in Snowflake Cortex, Snowflake customers with a payment method on file will be able to access Snowflake Arctic for free until June 3. [Daily limits apply](//docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions).
* Access Arctic via your model garden or catalog of choice including Amazon Web Services (AWS), Lamini, Microsoft Azure, [NVIDIA API catalog](https://build.nvidia.com/snowflake/arctic), Perplexity, [Replicate](https://replicate.com/snowflake/snowflake-arctic-instruct) and Together AI over the coming days.
* Chat with Arctic! Try a live demo now on [Streamlit Community Cloud](https://arctic.streamlit.app/) or on [Hugging Face Streamlit Spaces](https://huggingface.co/spaces/Snowflake/snowflake-arctic-st-demo), with an API powered by our friends at Replicate.
* Get mentorship and credits to help you build your own Arctic-powered applications during our [Arctic-themed Community Hackathon](https://arctic-streamlit-hackathon.devpost.com/).

And finally, don’t forget to read the first edition of our [cookbook](https://medium.com/@snowflake_ai_research/snowflake-arctic-cookbook-series-exploring-mixture-of-experts-moe-c7d6b8f14d16) recipes to learn more about how to build your own custom MoE models in the most cost-effective way possible.

### Acknowledgments

We would like to thank AWS for their collaboration and partnership in building Arctic’s training cluster and infrastructure, and NVIDIA for their collaboration in enabling Arctic support on NVIDIA NIM with TensorRT-LLM.  We also thank the open source community for producing the models, datasets and dataset recipe insights we could build on top of to make this release possible. We would also like to thank our partners in AWS, Microsoft Azure, NVIDIA API catalog, Lamini, Perplexity, Replicate and Together AI for their collaboration in making Arctic available

1. The 11 metrics for Language Understanding and Reasoning include ARC-Easy, ARC-Challenge, BoolQ, CommonsenseQA, COPA, HellaSwag, LAMBADA, OpenBookQA, PIQA, RACE and WinoGrande.

2. Evaluation scores for HumanEval+/MBPP+ v0.1.0 were obtained assuming (1) bigcode-evaluation-harness using model-specific chat templates and aligned post-processing, (2) greedy decoding. We evaluated all models with our pipeline to ensure consistency. We validated that our evaluations results are consistent with [EvalPlus leaderboard](https://evalplus.github.io/leaderboard.html). In fact, our pipeline produces numbers that are a few points higher than the numbers in EvalPlus for all models giving us confidence that we are evaluating each model in the best way possible.

3. IFEval scores reported are the average of prompt\_level\_strict\_acc and inst\_level\_strict\_acc

#### Essential Guide to Gen AI

[Download Now](https://www.snowflake.com/resource/the-essential-guide-to-generative-ai/?utm_cta=website-blog-arctic-llm-enterprise-ai-guide-genai-ebk)

### Learn more about the author

[![Snowflake AI Research](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--249da901-4810-48b7-ab40-99208c5e3b73/default-author-image.png?preferwebp=true&quality=85)

#### Snowflake AI Research](/en/blog/authors/snowflake-ai-research/)

### More blog posts

[Jun 17, 2026Product and Technology

### Powering the Agentic Enterprise: Turning Enterprise Context into Governed Agentic Action

![Sridhar Ramaswamy](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--b36e118e-4dda-46c0-b103-474724a16051/sridhar-ramaswamy-1-1-1.jpg?preferwebp=true&quality=85)

Sridhar Ramaswamy +1](/en/blog/agentic-enterprise-snowflake-accenture/)[Jun 17, 2026Product and Technology

### Exploring Agent Discovery: Snowflake and the Agentic Resource Discovery Specification

![Arun Agarwal](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--8049a19c-6f69-400d-9f50-c2ee72ba1d88/arun-agarwal.jpg?preferwebp=true&quality=85)

Arun Agarwal +1](/en/blog/agentic-resource-discovery-specification/)[Jun 15, 2026Product and Technology

### What's New with Dynamic Tables: Faster and More Flexible

![PD Dutta](https://www.snowflake.com/adobe/dynamicmedia/deliver/dm-aid--32bbb89d-4d69-4e3d-a366-3229f76be8c8/pd-pic.jpg?preferwebp=true&quality=85)

PD Dutta +1](/en/blog/whats-new-dynamic-tables-faster-flexible/)

#### Subscribe to our blog newsletter Get the best, coolest and latest delivered to your inbox each week

\*

Subscribe Now

By submitting this form, I understand Snowflake will process my personal information in accordance with their Privacy Notice.

## Where Data Does More

[Start for free](https://signup.snowflake.com/)

[Watch a demo](/en/webinars/demo/)

**Subscribe to our monthly newsletter**

Stay up to date on Snowflake’s latest products, expert insights and resources—right in your inbox!

\*

\*

\*

CountryUnited StatesCanadaUnited KingdomGermanyFranceAustraliaJapanAland IslandsAlbaniaAlgeriaAmerican SamoaAndorraAngolaAnguillaAntarcticaAntigua and BarbudaArgentinaArmeniaArubaAustraliaAustriaAzerbaijanBahamasBahrainBangladeshBarbadosBelarusBelgiumBelizeBeninBermudaBhutanBoliviaBosnia and HerzegovinaBotswanaBouvet IslandBrazilBritish Indian Ocean TerritoryBrunei DarussalamBulgariaBurkina FasoBurundiCambodiaCameroonCanadaCape VerdeCayman IslandsCentral African RepublicChadChileChinaChristmas IslandCocos (Keeling) IslandsColombiaComorosCongoCongo The Democratic Republic of TheCook IslandsCosta RicaCote D'Ivoire (Ivory Coast)Croatia (Hrvatska)CyprusCzech RepublicDenmarkDjiboutiDominicaDominican RepublicEcuadorEgyptEl SalvadorEquatorial GuineaEritreaEstoniaEthiopiaFalkland Islands (Malvinas)Faroe IslandsFijiFinlandFranceFrench GuianaFrench PolynesiaFrench Southern TerritoriesGabonGambiaGeorgiaGermanyGhanaGibraltarGreeceGreenlandGrenadaGuadeloupeGuamGuatemalaGuineaGuinea-BissauGuyanaHaitiHeard and McDonald IslandsHoly See (Vatican City State)HondurasHong KongHungaryIcelandIndiaIndonesiaIraqIrelandIsle of ManIsraelItalyJamaicaJapanJordanKazakhstanKenyaKiribatiKorea Republic of (South)KuwaitKyrgyzstanLao People's Democratic RepublicLatviaLebanonLesothoLiberiaLiechtensteinLithuaniaLuxembourgMacauMacedoniaMadagascarMalawiMalaysiaMaldivesMaliMaltaMarshall IslandsMartiniqueMauritaniaMauritiusMayotteMexicoMicronesia Federated States ofMoldova Republic ofMonacoMongoliaMontenegroMontserratMoroccoMozambiqueNamibiaNauruNepalNetherlandsNetherlands AntillesNew CaledoniaNew ZealandNicaraguaNigerNigeriaNiueNorfolk IslandNorthern Mariana IslandsNorwayOmanPakistanPalauPalestinian Territory OccupiedPanamaPapua New GuineaParaguayPeruPhilippinesPitcairnPolandPortugalPuerto RicoQatarReunionRomaniaRussian FederationSaint HelenaSaint Kitts and NevisSaint LuciaSaint Pierre and MiquelonSaint Vincent and the GrenadinesSamoaSan MarinoSao Tome and PrincipeSaudi ArabiaSenegalSerbiaSeychellesSierra LeoneSingaporeSlovakiaSloveniaSolomon IslandsSomaliaSouth AfricaSouth Georgia and The South Sandwich IslandSpainSri LankaSurinameSvalbard and Jan Mayen IslandsSwazilandSwedenSwitzerlandTaiwanTajikistanTanzania United Republic ofThailandTimor-LesteTogoTokelauTongaTrinidad and TobagoTunisiaTurkeyTurkmenistanTurks and Caicos IslandsTuvaluUgandaUkraineUnited Arab EmiratesUnited KingdomUnited States Minor Outlying IslandsUruguayUzbekistanVanuatuVenezuelaViet NamVirgin Islands (British)Virgin Islands (U.S.)Wallis and Futuna IslandsWestern SaharaYemenZambiaZimbabwe

\*

Add me to the list to receive dedicated product updates and general availability emails.

By submitting this form, I understand Snowflake will process my personal information in accordance with their [**Privacy Notice**](https://www.snowflake.com/privacy-policy/).

Subscribe Now

Product

* [Platform](//www.snowflake.com/en/product/platform/)
* [Snowflake CoWork](/en/product/snowflake-cowork/)
* [Data Engineering](//www.snowflake.com/en/product/data-engineering/)
* [Analytics](//www.snowflake.com/en/product/analytics/)
* [AI](//www.snowflake.com/en/product/ai/)
* [Applications & Collaboration](//www.snowflake.com/en/product/applications-and-collaboration/)
* [Pricing](//www.snowflake.com/en/pricing-options/)

Support

* [Support](//www.snowflake.com/en/support/)
* [Priority Support](//www.snowflake.com/en/legal/addenda/priority-support-services-description/)
* [Status](//status.snowflake.com/)

[Industries](/en/solutions/industries/)

* [Advertising, Media & Entertainment](/en/solutions/industries/advertising-media-entertainment/)
* [Financial Services](/en/solutions/industries/financial-services/)
* [Healthcare & Life Sciences](/en/solutions/industries/healthcare-and-life-sciences/)
* [Manufacturing](/en/solutions/industries/manufacturing/)
* [Public Sector](/en/solutions/industries/public-sector/)
* [Retail & Consumer Goods](/en/solutions/industries/retail-consumer-goods/)
* [Telecom](/en/solutions/industries/telecom/)
* [Technology](//www.snowflake.com/en/solutions/industries/technology/)

Company

* [About Snowflake](//www.snowflake.com/en/company/overview/about-snowflake/)
* [Leadership & Board](//www.snowflake.com/en/company/overview/leadership-and-board/)
* [Careers](//careers.snowflake.com/us/en)
* [Investor Relations](//investors.snowflake.com/overview/default.aspx)
* [Trust Center](//trust.snowflake.com/)
* [Brand Guidelines](//www.snowflake.com/brand-guidelines/)
* [Contact](//www.snowflake.com/en/contact/)
* [Newsroom](//www.snowflake.com/en/news/)
* [Environmental, Social & Governance](//www.snowflake.com/en/company/overview/esg/)
* [Snowflake Ventures](//www.snowflake.com/en/company/overview/snowflake-ventures/)
* [End Data Disparity](//www.snowflake.com/en/company/overview/end-data-disparity/)
* [Snowflake Summit 26](/en/summit/)

Learn

* [Resource Library](//snowflake.com/en/resources/)
* [Live Demos](/en/webinars/demo/)
* [Fundamentals](//www.snowflake.com/en/fundamentals/)
* [Training](//www.snowflake.com/en/resources/learn/training/)
* [Certifications](//www.snowflake.com/en/resources/learn/certifications/)
* [Snowflake University](//learn.snowflake.com/en/)
* [Developer Guides](//www.snowflake.com/en/developers/guides)
* [Documentation](//docs.snowflake.com/)
* [Data Governance](/en/data-governance/)

[![Snowflake logo](https://www.snowflake.com/content/experience-fragments/snowflake-site/language-masters/en/site/footer/master/_jcr_content/root/container_573483281_/container_112062425/flexible_column_cont/flexible_column_content_container_1/container/container/image.coreimg.svg/1747882370694/nav-icon-snowflake-bug.svg)](/en/)

* © 2026 Snowflake Inc. All Rights Reserved
* [Privacy Policy](//www.snowflake.com/en/legal/privacy/privacy-policy/)
* [Site Terms](//snowflake.com/en/legal/snowflake-site-terms/)
* [Communication Preferences](//info.snowflake.com/Preference-center.html)
* Cookies Settings
* [Do Not Share My Personal Information](//www.snowflake.com/en/legal/privacy/privacy-policy/#12)
* [Legal](//www.snowflake.com/en/legal/)

## Snowflake's Use of Cookies

We use cookies to enhance your experience and to analyze site traffic as described in our Cookie Statement. By accepting, you consent to our use of cookies.[Cookie Statement.](https://www.snowflake.com/privacy-policy/cookie-statement/)

Cookies Settings Reject All Accept All Cookies

![Company Logo](https://cdn.cookielaw.org/logos/cb85e692-4053-4d0a-8dda-d24b5daa8b06/ff6c124b-1473-4861-9ca3-9eaf6debb37d/SNO-SnowflakeLogo_blue.png)

## Privacy Preference Center

Opt-Out Request Honored

## Privacy Preference Center

* ### Your Privacy
* ### Strictly Necessary Cookies
* ### Performance Cookies
* ### Functional Cookies
* ### Targeting Cookies

#### Your Privacy

When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. This information might be about you, your preferences, or your device, and is mostly used to make the site work as you expect. The information does not usually identify you directly, but it can give you a more personalized web experience. Because we respect your right to privacy, you can choose not to allow some types of cookies. Click on the different category headings to learn more and change our default settings. Blocking some types of cookies may impact your experience of the site and the services we are able to offer.
  
[More information](https://cookiepedia.co.uk/giving-consent-to-cookies)

#### Strictly Necessary Cookies

Always Active

These cookies are necessary for the website to function and cannot be switched off. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.

Cookies Details

#### Performance Cookies

Performance Cookies

These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site.    All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance.

Cookies Details

#### Functional Cookies

Functional Cookies

These cookies enable the website to provide enhanced functionality and personalisation. They may be set by us or by third party providers whose services we have added to our pages.    If you do not allow these cookies then some or all of these services may not function properly.

Cookies Details

#### Targeting Cookies

Targeting Cookies

These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly identifiable personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising.

Cookies Details

### Cookie List

Consent Leg.Interest

checkbox label label

checkbox label label

checkbox label label

Clear

* checkbox label label

Apply Cancel

Confirm My Choices

Allow All

[![Powered by Onetrust](https://cdn.cookielaw.org/logos/static/powered_by_logo.svg "Powered by OneTrust Opens in a new Tab")](https://www.onetrust.com/products/cookie-consent/)
