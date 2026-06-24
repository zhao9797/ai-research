# The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation
Source: https://ai.meta.com/blog/llama-4-multimodal-intelligence/
The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation

[![Meta](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=XK6ck52-T0YQ7kNvwEz0_By&_nc_oc=Ado5uMoab6HCGBI0-hzBTDXrse6OwnkLcsv3rAfBOJ6i4nObQMZ03IDDkHf3NCKNvkoNaQaa_r4gVwHJPfnDIv2-&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9akPvbL8i0Nut43zjnRhsU7T9Vw3TY9r-TaUZbtcTk7w&oe=6A38BEB9)](/)

* [Products](#)
* [AI Research](#)
* [Resources](#)
* [About](#)
* [Get Llama](https://www.llama.com/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=09252025_moment)

* [Try Meta AI](https://applink.meta.ai/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=04082026_moment)

[BACK](# "Go up one level")

* [Meta AI](/meta-ai/)
* [Vibes](/vibes/)
* [AI Studio](/ai-studio/)

* [Overview](/research/)
* [Projects](/research/#projects)
* [Research Areas](/research/#research-areas)
* [People](/results/?content_types[0]=person)

* [Blog](/blog/)
* [Learning Hub](/learn/)
* [Demos](https://aidemos.meta.com/)

* [Overview](/about/)
* [Open Source](/opensourceai/)
* [Careers](https://www.metacareers.com/)

Clear

* Clear
* [Products

  >](#)
* [AI Research

  >](#)
* [Resources

  >](#)
* [About

  >](#)
* [Get Llama](https://www.llama.com/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=09252025_moment)

[Try Meta AI](https://applink.meta.ai/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=04082026_moment)

Large Language Model

# The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation

April 5, 2025•

12 minute read

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/489528324_1866126614188079_2353760794201377773_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=B_3rUFr5QBQQ7kNvwFePpfK&_nc_oc=AdpzzqVQN-0PZ5-STeuhz8XGvl0EI8L2Ka1XHYb3dVv09WAx2kuF8qjCpgRcr5Xzvm4iN9U92PsZpkLFVgNJYXm8&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9xVBaUcRjEXtNGdkiSiDH_ubskQDO5hu26ZYh0a0cnaw&oe=6A4D1CB3)

## Takeaways

* We’re sharing the first models in the Llama 4 herd, which will enable people to build more personalized multimodal experiences.
* Llama 4 Scout, a 17 billion active parameter model with 16 experts, is the best multimodal model in the world in its class and is more powerful than all previous generation Llama models, while fitting in a single NVIDIA H100 GPU. Additionally, Llama 4 Scout offers an industry-leading context window of 10M and delivers better results than Gemma 3, Gemini 2.0 Flash-Lite, and Mistral 3.1 across a broad range of widely reported benchmarks.
* Llama 4 Maverick, a 17 billion active parameter model with 128 experts, is the best multimodal model in its class, beating GPT-4o and Gemini 2.0 Flash across a broad range of widely reported benchmarks, while achieving comparable results to the new DeepSeek v3 on reasoning and coding—at less than half the active parameters. Llama 4 Maverick offers a best-in-class performance to cost ratio with an experimental chat version scoring ELO of 1417 on [LMArena](https://lmarena.ai/leaderboard).
* These models are our best yet thanks to distillation from Llama 4 Behemoth, a 288 billion active parameter model with 16 experts that is our most powerful yet and among the world’s smartest LLMs. Llama 4 Behemoth outperforms GPT-4.5, Claude Sonnet 3.7, and Gemini 2.0 Pro on several STEM benchmarks. Llama 4 Behemoth is still training, and we’re excited to share more details about it even while it’s still in flight.
* Download the Llama 4 Scout and Llama 4 Maverick models today on [llama.com](https://www.llama.com/llama-downloads/) and [Hugging Face](https://huggingface.co/meta-llama). Try Meta AI built with Llama 4 in WhatsApp, Messenger, Instagram Direct, and on the [web](http://meta.ai/).

As more people continue to use artificial intelligence to enhance their daily lives, it’s important that the leading models and systems are openly available so everyone can build the future of personalized experiences. Today, we’re excited to announce the most advanced suite of models that support the entire [Llama](https://www.llama.com/) ecosystem. We’re introducing Llama 4 Scout and Llama 4 Maverick, the first open-weight natively multimodal models with unprecedented context length support and our first built using a mixture-of-experts (MoE) architecture. We’re also previewing Llama 4 Behemoth, one of the smartest LLMs in the world and our most powerful yet to serve as a teacher for our new models.

These Llama 4 models mark the beginning of a new era for the Llama ecosystem. We designed two efficient models in the Llama 4 series, Llama 4 Scout, a 17 billion active parameter model with 16 experts, and Llama 4 Maverick, a 17 billion active parameter model with 128 experts. The former fits on a single H100 GPU (with Int4 quantization) while the latter fits on a single H100 host. We also trained a teacher model, Llama 4 Behemoth, that outperforms GPT-4.5, Claude Sonnet 3.7, and Gemini 2.0 Pro on STEM-focused benchmarks such as MATH-500 and GPQA Diamond. While we’re not yet releasing Llama 4 Behemoth as it is still training, we’re excited to share more technical details about our approach.

We continue to believe that openness drives innovation and is good for developers, good for Meta, and good for the world. We’re making Llama 4 Scout and Llama 4 Maverick available for download today on [llama.com](https://www.llama.com/llama-downloads/) and [Hugging Face](https://huggingface.co/meta-llama) so everyone can continue to build new experiences using our latest technology. We’ll also make them available via our partners in the coming days. You can also try Meta AI with Llama 4 starting today in WhatsApp, Messenger, Instagram Direct, and on the [Meta.AI](http://meta.ai/) website.

This is just the beginning for the Llama 4 collection. We believe that the most intelligent systems need to be capable of taking generalized actions, conversing naturally with humans, and working through challenging problems they haven’t seen before. Giving Llama superpowers in these areas will lead to better products for people on our platforms and more opportunities for developers to innovate on the next big consumer and business use cases. We’re continuing to research and prototype both models and products, and we’ll share more about our vision at LlamaCon on April 29—[sign up to hear more](https://www.llama.com/events/llamacon/signup/).

Whether you’re a developer building on top of our models, an enterprise integrating them into your workflows, or simply curious about the potential uses and benefits of AI, Llama 4 Scout and Llama 4 Maverick are the best choices for adding next-generation intelligence to your products. Today, we’re excited to share more about the four major parts of their development and insights into our research and design process. We also can’t wait to see the incredible new experiences the community builds with our new Llama 4 models.

## Pre-training

These models represent the best of Llama, offering multimodal intelligence at a compelling price while outperforming models of significantly larger sizes. Building the next generation of Llama models required us to take several new approaches during pre-training.

Our new Llama 4 models are our first models that use a mixture of experts (MoE) architecture. In MoE models, a single token activates only a fraction of the total parameters. MoE architectures are more compute efficient for training and inference and, given a fixed training FLOPs budget, delivers higher quality compared to a dense model.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/488655517_650996354186993_1043942188415715102_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=MLLT0x0HCvAQ7kNvwEFedl6&_nc_oc=AdrGXGXF2GVOESVOytJxcGqXL-OA12vMwLglImLXwSyQnwtEEwLT4DmDZFx45Bv5OjQPjTte2jK8f2Rzv2877gF3&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-IByCAFZKz5ZlSCeS2jyvSDP5X8ffPNSSrIwEJ6vDz4g&oe=6A4D0F80)

As an example, Llama 4 Maverick models have 17B active parameters and 400B total parameters. We use alternating dense and mixture-of-experts (MoE) layers for inference efficiency. MoE layers use 128 routed experts and a shared expert. Each token is sent to the shared expert and also to one of the 128 routed experts. As a result, while all parameters are stored in memory, only a subset of the total parameters are activated while serving these models. This improves inference efficiency by lowering model serving costs and latency—Llama 4 Maverick can be run on a single NVIDIA H100 DGX host for easy deployment, or with distributed inference for maximum efficiency.

Llama 4 models are designed with native multimodality, incorporating early fusion to seamlessly integrate text and vision tokens into a unified model backbone. Early fusion is a major step forward, since it enables us to jointly pre-train the model with large amounts of unlabeled text, image, and video data. We also improved the vision encoder in Llama 4. This is based on MetaCLIP but trained separately in conjunction with a frozen Llama model to better adapt the encoder to the LLM.

We developed a new training technique which we refer to as MetaP that allows us to reliably set critical model hyper-parameters such as per-layer learning rates and initialization scales. We found that chosen hyper-parameters transfer well across different values of batch size, model width, depth, and training tokens. Llama 4 enables open source fine-tuning efforts by pre-training on 200 languages, including over 100 with over 1 billion tokens each, and overall 10x more multilingual tokens than Llama 3.

Additionally, we focus on efficient model training by using FP8 precision, without sacrificing quality and ensuring high model FLOPs utilization—while pre-training our Llama 4 Behemoth model using FP8 and 32K GPUs, we achieved 390 TFLOPs/GPU. The overall data mixture for training consisted of more than 30 trillion tokens, which is more than double the Llama 3 pre-training mixture and includes diverse text, image, and video datasets.

We continued training the model in what we call “mid-training” to improve core capabilities with new training recipes including long context extension using specialized datasets. This enabled us to enhance model quality while also unlocking best-in-class 10M input context length for Llama 4 Scout.

## Post-training our new models

Our newest models include smaller and larger options to accommodate a range of use cases and developer needs. Llama 4 Maverick offers unparalleled, industry-leading performance in image and text understanding, enabling the creation of sophisticated AI applications that bridge language barriers. As our product workhorse model for general assistant and chat use cases, Llama 4 Maverick is great for precise image understanding and creative writing.

The biggest challenge while post-training the Llama 4 Maverick model was maintaining a balance between multiple input modalities, reasoning, and conversational abilities. For mixing modalities, we came up with a carefully curated curriculum strategy that does not trade-off performance compared to the individual modality expert models. With Llama 4, we revamped our post-training pipeline by adopting a different approach: lightweight supervised fine-tuning (SFT) > online reinforcement learning (RL) > lightweight direct preference optimization (DPO). A key learning was that SFT and DPO can over-constrain the model, restricting exploration during the online RL stage and leading to suboptimal accuracy, particularly in reasoning, coding, and math domains. To address this, we removed more than 50% of our data tagged as easy by using Llama models as a judge and did lightweight SFT on the remaining harder set. In the subsequent multimodal online RL stage, by carefully selecting harder prompts, we were able to achieve a step change in performance. Furthermore, we implemented a continuous online RL strategy, where we alternated between training the model and then using it to continually filter and retain only medium-to-hard difficulty prompts. This strategy proved highly beneficial in terms of compute and accuracy tradeoffs. We then did a lightweight DPO to handle corner cases related to model response quality, effectively achieving a good balance between the model’s intelligence and conversational abilities. Both the pipeline architecture and the continuous online RL strategy with adaptive data filtering culminated in an industry-leading, general-purpose chat model with state-of-the-art intelligence and image understanding capabilities.

As a general purpose LLM, Llama 4 Maverick contains 17 billion active parameters, 128 experts, and 400 billion total parameters, offering high quality at a lower price compared to Llama 3.3 70B. Llama 4 Maverick is the best-in-class multimodal model, exceeding comparable models like GPT-4o and Gemini 2.0 on coding, reasoning, multilingual, long-context, and image benchmarks, and it’s competitive with the much larger DeepSeek v3.1 on coding and reasoning.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/488688605_1406312723692874_1536535503366996614_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=J-nFaovjrRAQ7kNvwFo413A&_nc_oc=AdrZfF7wBUv6W3XCuTJptXbRcDwbmqfnRgqhsCNEbHKyMnKe2zbvy6Rh6twnFXTBCV7U5UfeieT_m6YMDqk4B_yW&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af8xWrBFza5QhwbKRKuxIWKOS9G8oFq7gyFhyTui9V8q-Q&oe=6A4D0B8F)

Our smaller model, Llama 4 Scout, is a general purpose model with 17 billion active parameters, 16 experts, and 109 billion total parameters that delivers state-of-the-art performance for its class. Llama 4 Scout dramatically increases the supported context length from 128K in Llama 3 to an industry leading 10 million tokens. This opens up a world of possibilities, including multi-document summarization, parsing extensive user activity for personalized tasks, and reasoning over vast codebases.

Llama 4 Scout is both pre-trained and post-trained with a 256K context length, which empowers the base model with advanced length generalization capability. We present compelling results in tasks such as retrieval with “retrieval needle in haystack” for text as well as cumulative negative log-likelihoods (NLLs) over 10 million tokens of code. A key innovation in the Llama 4 architecture is the use of interleaved attention layers [without positional embeddings](https://arxiv.org/abs/2305.19466). Additionally, we employ [inference time temperature scaling](https://arxiv.org/pdf/2501.19399) of attention to enhance length generalization. We call this the iRoPE architecture, where “i” stands for “interleaved” attention layers, highlighting the long-term goal of supporting “infinite” context length, and “RoPE” refers to the [rotary position embeddings](https://arxiv.org/abs/2104.09864) employed in most layers.

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/488601380_691716116851230_4462222921335148419_n.png?_nc_cat=107&ccb=1-7&_nc_sid=f537c7&_nc_ohc=pLEcIpwwA-cQ7kNvwHWbqrv&_nc_oc=AdrK1seVnEMtZd7EXGVJmiXJYENVEU19Xx1-mrkrPqCCZevce_148eKLp2A8lNOBT1RQL0ZvrshwDXmsQibN2HCV&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-hQcfNDkVumiw7fWyhgFby32ZND8vhr03CxNzyBIEG8A&oe=6A38A7ED)](https://video-sea5-1.xx.fbcdn.net/o1/v/t2/f2/m412/AQMIYZGABW8ZE8KwxR3vnXjcz_s3uGT97tmejckO--8L-WmO0XxQrb0RkEmC6kOeqn3SLBdlWXY_4fnRAtCxSc4.mp4?_nc_cat=103&_nc_sid=5e9851&_nc_ht=video-sea5-1.xx.fbcdn.net&_nc_ohc=9XEGihA1Ds8Q7kNvwF_ZgnO&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTkyMC5kYXNoX2gyNjQtYmFzaWMtZ2VuMl8xMDgwcCIsInhwdl9hc3NldF9pZCI6MTE3NzY3MjI1MDUxOTU5NiwiYXNzZXRfYWdlX2RheXMiOjQzOSwidmlfdXNlY2FzZV9pZCI6MTA4MjUsImR1cmF0aW9uX3MiOjE4LCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=17-1&vs=e07070599552b70&_nc_vs=HBksFQIYNGZiX3Blcm1hbmVudC80NzAzMjc4NDk0MDY0NDhfNTI1MTk3NzgzMzgyMzA5OTc1NS5tcDQVAALIARIAFQIYNWZiX3Blcm1hbmVudC8yMTc3NTE5MDAyNjcxMTE4Xzg5OTE2NTI1ODQ0OTc3MDM1NjYubXA0FQICyAESACgAGAAbAogHdXNlX29pbAExEnByb2dyZXNzaXZlX3JlY2lwZQExFQAAJtjAu4LGxZcEFQIoAkMzLBdAMgAAAAAAABgaZGFzaF9oMjY0LWJhc2ljLWdlbjJfMTA4MHARAHUCZZKpAQA&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&_nc_zt=28&oh=00_Af-hcdC9uhDkUfECNOUKeZyLV7Nh10urvbC_LpkLpPMFnw&oe=6A38B7AB&bitrate=636947&tag=dash_h264-basic-gen2_1080p)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/488955260_630849766606664_4970227915274398227_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=0z8rrcwlNukQ7kNvwF8HDpd&_nc_oc=AdrRbq57ixIUxHsgYqX6Utw0ymsL36PyCNO9Suv5Aa5gm7N0-QEPCt7n83fO0F7DYR1AzDscrBHw56Wwygeunkfg&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-UFwjcuQ_Knv4jI6Szcymo3jZIUu9TJ3132IJeN8DPHg&oe=6A4D2960)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/488641575_1306808653730812_1227810128658266115_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=Pa3kTXi3nrsQ7kNvwH9RO-Q&_nc_oc=Adox91p3EYbo8viIYObBs5me_T0Y8fJMVqdirGrDxqeokE26ufo67gNwEnWDkEebSoNhWbhRY835QajoB74noIK8&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af8aUJCqdlRZGJJFEzDVw7sPsi3tPV7t6TUUOdqeON5u0g&oe=6A4D4171)

We trained both of our models on a wide variety of image and video frame stills in order to give them broad visual understanding, including of temporal activities and related images. This enables effortless interaction on multi-image inputs alongside text prompts for visual reasoning and understanding tasks. The models were pre-trained on up to 48 images, and we’ve tested in post-training with good results up to eight images.

Llama 4 Scout is also best-in-class on image grounding, able to align user prompts with relevant visual concepts and anchor model responses to regions in the image. This enables more precise visual question answering for the LLM to better understand user intent and localize objects of interest. Llama 4 Scout also exceeds comparable models on coding, reasoning, long context, and image benchmarks and offers stronger performance than all previous Llama models.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/488658055_1347378876402143_3412007366291908454_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=-ByISxzdjVMQ7kNvwGixoSE&_nc_oc=AdolW_DDHCwOIQOXXny5vDSEa45utBXfsLH7_jHC8fkZiSClhk4xea9_U_2eQAxdNezYw2bsOqPKmvbwIC-1r70x&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af8D85lPqhNVd9yMapUo2oIV5AzIHGAi_JKTmT9Tw46AYw&oe=6A4D1D9F)

These new models are important building blocks that will help enable the future of human connection. In keeping with our commitment to open source, we’re making Llama 4 Maverick and Llama 4 Scout available to download on [llama.com](https://www.llama.com/llama-downloads/) and Hugging Face, with availability across the most widely used cloud and data platforms, edge silicon, and global service integrators to follow shortly.

## Pushing Llama to new sizes: The 2T Behemoth

We’re excited to share a preview of Llama 4 Behemoth, a teacher model that demonstrates advanced intelligence among models in its class. Llama 4 Behemoth is also a multimodal mixture-of-experts model, with 288B active parameters, 16 experts, and nearly two trillion total parameters. Offering state-of-the-art performance for non-reasoning models on math, multilinguality, and image benchmarks, it was the perfect choice to teach the smaller Llama 4 models. We codistilled the Llama 4 Maverick model from Llama 4 Behemoth as a teacher model, resulting in substantial quality improvements across end task evaluation metrics. We developed a novel distillation loss function that dynamically weights the soft and hard targets through training. Codistillation from Llama 4 Behemoth during pre-training amortizes the computational cost of resource-intensive forward passes needed to compute the targets for distillation for the majority of the training data used in student training. For additional new data incorporated in student training, we ran forward passes on the Behemoth model to create distillation targets.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/489511937_1627813884508038_4209289296588372348_n.png?_nc_cat=107&ccb=1-7&_nc_sid=e280be&_nc_ohc=9vBfWTGH79wQ7kNvwFdTcHp&_nc_oc=AdrbwulYQsIIHTUyWkWp8u3XqRlvzTfTq3fMHxa635BYAH53E_6NvOBmXKRdy5K-fybnq8b57STHXJX9iJxANZl4&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af978taVgqAJKRcshgxN0zfv01jp5M-0FpjzPLY0aOb-MA&oe=6A4D4309)

Post-training a model with two trillion parameters was a significant challenge too that required us to completely overhaul and revamp the recipe, starting from the scale of data. In order to maximize performance, we had to prune 95% of the SFT data, as opposed to 50% for smaller models, to achieve the necessary focus on quality and efficiency. We also found that doing lightweight SFT followed by large-scale reinforcement learning (RL) produced even more significant improvements in reasoning and coding abilities of the model. Our RL recipe focused on sampling hard prompts by doing pass@k analysis with the policy model and crafting a training curriculum of increasing prompt hardness. We also found that dynamically filtering out prompts with zero advantage during training and constructing training batches with mixed prompts from multiple capabilities were instrumental in providing a performance boost on math, reasoning, and coding. Finally, sampling from a variety of system instructions was crucial in ensuring that the model retained its instruction following ability for reasoning and coding and was able to perform well across a variety of tasks.

Scaling RL for a two trillion parameter model also required revamping our underlying RL infrastructure due to its unprecedented scale. We optimized the design of our MoE parallelization for speed, which enabled faster iteration. We developed a fully asynchronous online RL training framework that enhanced flexibility. Compared to the existing distributed training framework, which sacrifices the compute memory in order to stack all models in memory, our new infrastructure enabled flexible allocation of different models to separate GPUs, balancing resources across multiple models based on computational speed. This innovation resulted in a ~10x improvement in training efficiency over previous generations.

## Safeguards and protections

We aim to develop the most helpful and useful models while protecting against and mitigating the most severe risks. We built Llama 4 with the best practices outlined in our Developer Use Guide: AI Protections. This includes integrating mitigations at each layer of model development from pre-training to post-training to tunable system-level mitigations that shield developers from adversarial users. In doing so, we empower developers to create helpful, safe, and adaptable experiences for their Llama-supported applications.

**Pre- and post-training mitigations**

For pre-training, we use data filtering in combination with other data mitigations to safeguard models. For post-training, we apply a range of techniques to ensure our models conform to policies that are helpful to users and developers, including the right level of safety data at each stage.

**System-level approaches**

At the system-level, we have open-sourced several safeguards which can help identify and guard against potentially harmful inputs and outputs. These tools can be integrated into our Llama models and with other third-party tools:

* Llama Guard: Our input/output safety large language model based on the [hazards taxonomy](https://arxiv.org/abs/2404.12241) we developed with MLCommons. Developers can use it to detect whether inputs or outputs violate the policies they’ve created for their specific application.
* Prompt Guard: A classifier model trained on a large corpus of attacks, which is capable of detecting both explicitly malicious prompts (Jailbreaks) as well as prompts that contain inject inputs (Prompt Injections).
* CyberSecEval: Evaluations that help AI model and product developers understand and reduce generative AI cybersecurity risk.

We’ve heard from developers that these tools are most effective and helpful when they can be tailored to their applications. We provide developers with an open solution so they can create the safest and most effective experiences based on their needs. We’ll also continue working with a global set of partners to create industry-wide system standards that benefit the open source community.

**Evaluations and red-teaming**

We run systematic testing of models across a wide range of scenarios and use cases in a controlled and repeatable manner. This produces data that we incorporate back into post-training.

We stress test our models using adversarial dynamic probing across a range of topics using automated and manual testing. We’ve made advancements in understanding and evaluating potential model risk. One example of this is our new development of Generative Offensive Agent Testing (GOAT). Using GOAT, we address the limitations of traditional red-teaming by simulating multi-turn interactions of medium-skilled adversarial actors, helping us increase our testing coverage and raise vulnerabilities faster. By adding automation to our testing toolkit, GOAT has allowed our expert human red teamers to focus on more novel adversarial areas, while the automation focuses on known risk areas. This makes the process more efficient and effective, and it enables us to build a better quantitative and qualitative picture of risk.

**Addressing bias in LLMs**

It’s well-known that all leading LLMs have had issues with bias—specifically, they historically have leaned left when it comes to debated political and social topics. This is due to the types of training data available on the internet.

Our goal is to remove bias from our AI models and to make sure that Llama can understand and articulate both sides of a contentious issue. As part of this work, we’re continuing to make Llama more responsive so that it answers questions, can respond to a variety of different viewpoints without passing judgment, and doesn't favor some views over others.

We have made improvements on these efforts with this release—Llama 4 performs significantly better than Llama 3 and is comparable to Grok:

* Llama 4 refuses less on debated political and social topics overall (from 7% in Llama 3.3 to below 2%).
* Llama 4 is dramatically more balanced with which prompts it refuses to respond to (the proportion of unequal response refusals is now less than 1% on a set of debated topical questions).
* Our testing shows that Llama 4 responds with strong political lean at a rate comparable to Grok (and at half of the rate of Llama 3.3) on a contentious set of political or social topics. While we are making progress, we know we have more work to do and will continue to drive this rate further down.

We’re proud of this progress to date and remain committed to our goal of eliminating overall bias in our models.

## Explore the Llama ecosystem

While it’s important that models are intelligent, people also want models that can reply in a personalized way with human-like speed. As our most advanced models yet, Llama 4 is optimized to meet these needs.

Of course, models are one piece of the larger ecosystem that brings these experiences to life. We’re focused on the full stack, which includes new product integrations. We’re excited to continue the conversations we’re having with our partners and the open source community, and as always, we can’t wait to see the rich experiences people build in the new Llama ecosystem.

Download the Llama 4 Scout and Llama 4 Maverick models today on [llama.com](https://www.llama.com/llama-downloads/) and [Hugging Face](https://huggingface.co/meta-llama). Try Meta AI built with Llama 4 in WhatsApp, Messenger, Instagram Direct, and on the [Meta.AI](http://meta.ai/) website.

*This work was supported by our partners across the AI community. We’d like to thank and acknowledge (in alphabetical order): Accenture, Amazon Web Services, AMD, Arm, CentML, Cerebras, Cloudflare, Databricks, Deepinfra, DeepLearning.AI, Dell, Deloitte, Fireworks AI, Google Cloud, Groq, Hugging Face, IBM Watsonx, Infosys, Intel, Kaggle, Mediatek, Microsoft Azure, Nebius, NVIDIA, ollama, Oracle Cloud, PwC, Qualcomm, Red Hat, SambaNova, Sarvam AI, Scale AI, Scaleway, Snowflake, TensorWave, Together AI, vLLM, Wipro.*

## Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/480457472_530944076174486_7354825982659691759_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=dVcOF9Js0a0Q7kNvwEKZBQy&_nc_oc=Adqp_ntZboT99rOR-903-kxw99Wbw8G_jt5ylIOwoJa1GG6Sao0xozgLXBlTQzYU4dkwp6pC07hruOhSZxFoGDZP&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af_BiPQxRJGRAPmaLMaFzMVAV4nQ3Ozvwbsio82WsBr7dA&oe=6A4D2754)

Open Source

How Sevilla FC is discovering future soccer stars with Llama

February 28, 2025

[Read post](https://ai.meta.com/blog/sevilla-fc-scout-advisor-llama-ibm-watsonx/)

FEATURED

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/470665849_1620699585191822_2616824612634584243_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=zvNMFwRkANQQ7kNvwGLMtAu&_nc_oc=AdoEHaVPn8LOdOsgVMgXPBpV-MbPuzbCDp2XaFFt54Fj6n7EQ8hcsDi53NJMxSuV9e6uTGutxuPR4yfDoADYoe_C&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af8itwZMQ9lMZBta0OsbkJUD6L3sNnm1OfOnk1om7WGI4g&oe=6A4D1EAF)

Large Language Model

The future of AI: Built with Llama

December 19, 2024

[Read post](https://ai.meta.com/blog/future-of-ai-built-with-llama/)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/470644933_3774351322782456_2883934816651785513_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=cE_pEnJ65skQ7kNvwF896SQ&_nc_oc=AdqPsTSl5eYHxJq8ZpVe7zqcj9-Qe1CwwKwQlAmOOj1DAYBeOqpoyQr-oo7JdKi7gcQxF98qn-R0A_j1PVLku170&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af_ULaYCiverDeIEWJFlRSYLWjqO2BZ7N08D4Ft_Ny_cdA&oe=6A4D1494)

How Spotify is using Llama to create personalized recommendations and enhance content discovery

December 18, 2024

[Read post](https://ai.meta.com/blog/spotify-personalized-recommendations-built-with-llama/)

[Our approach](/about)

[About AI at Meta](/about)

[People](/results/?content_types%5B0%5D=person&sort_by=random)

[Careers](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams[0]=Artificial%20Intelligence&is_in_page=0)

[Research](/research)

[Infrastructure](/infrastructure)

[Resources](/resources)

[Demos](https://aidemos.meta.com/)

[Meta AI](/meta-ai/)

[Explore Meta AI](/meta-ai/)

[Get Meta AI](/get-meta-ai/)

[AI Studio](/ai-studio/)

[Latest news](/blog)

[Blog](/blog)

[Newsletter](/subscribe)

Foundational models

[Llama](https://www.llama.com/)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=C2HG24npvwYQ7kNvwG0RyrH&_nc_oc=AdptCqVJQJPLbRtXnSREzEZnlux7g_82gv50avE_ri2mE328tNh5MOIPxrPKQQS3-EawsNIB37KqH4mD_w698D-2&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af8pHDPLOEqHfoXKV3fWkj41sdKBORVDTtVB-s1KUSxVUg&oe=6A4D2878)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=bJOdWS-UzpEQ7kNvwHEWSJk&_nc_oc=AdqY7cuE1VsRQzWKKPHkHeK7M_IuidVlFR2W3Ff3aS0-h6UQr-yqNzH16ykxxOeM1cJG0cCC710ssQ1y0uhcI19D&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9x2ypyUmxNTVj4XVam_0OF4xk5vvWZCW56Nr1ESShX1w&oe=6A4D2D4F)

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-ZXNOPpopQrSNfm65tI0MyMQiL37Hni55kvNL76At3OQ&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-ZXNOPpopQrSNfm65tI0MyMQiL37Hni55kvNL76At3OQ&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9NSQxENb35DzCRaQzuNhiHmhlk9zaeSc1asPSgM5Qviw&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9NSQxENb35DzCRaQzuNhiHmhlk9zaeSc1asPSgM5Qviw&oe=6A38A722)](https://twitter.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-8Us-CE4pD7HOylh4Nm1qy7BPLhDqULUhT_qoz0n6VVg&oe=6A38D2FB)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-8Us-CE4pD7HOylh4Nm1qy7BPLhDqULUhT_qoz0n6VVg&oe=6A38D2FB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-Tw6e2zqZavF3ezWgT4Jv-UoS0DIjU-j2YCHTIW6IC6A&oe=6A38B42E)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-Tw6e2zqZavF3ezWgT4Jv-UoS0DIjU-j2YCHTIW6IC6A&oe=6A38B42E)](https://www.youtube.com/@aiatmeta)

Our approach

[Our approach](/about)[About AI at Meta](/about)[People](/results/?content_types%5B0%5D=person&sort_by=random)[Careers](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams[0]=Artificial%20Intelligence&is_in_page=0)

Research

[Research](/research)[Infrastructure](/infrastructure)[Resources](/resources)[Demos](https://aidemos.meta.com/)

Meta AI

[Meta AI](/meta-ai/)[Explore Meta AI](/meta-ai/)[Get Meta AI](/get-meta-ai/)[AI Studio](/ai-studio/)

Latest news

[Latest news](/blog)[Blog](/blog)[Newsletter](/subscribe)

Foundational models

[Llama](https://www.llama.com/)

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-ZXNOPpopQrSNfm65tI0MyMQiL37Hni55kvNL76At3OQ&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-ZXNOPpopQrSNfm65tI0MyMQiL37Hni55kvNL76At3OQ&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9NSQxENb35DzCRaQzuNhiHmhlk9zaeSc1asPSgM5Qviw&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af9NSQxENb35DzCRaQzuNhiHmhlk9zaeSc1asPSgM5Qviw&oe=6A38A722)](https://twitter.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-8Us-CE4pD7HOylh4Nm1qy7BPLhDqULUhT_qoz0n6VVg&oe=6A38D2FB)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-8Us-CE4pD7HOylh4Nm1qy7BPLhDqULUhT_qoz0n6VVg&oe=6A38D2FB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-Tw6e2zqZavF3ezWgT4Jv-UoS0DIjU-j2YCHTIW6IC6A&oe=6A38B42E)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=0V49Qu6aYNnbf8_s2Ynd0Q&_nc_ss=7b289&oh=00_Af-Tw6e2zqZavF3ezWgT4Jv-UoS0DIjU-j2YCHTIW6IC6A&oe=6A38B42E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.fa

[truncated]
