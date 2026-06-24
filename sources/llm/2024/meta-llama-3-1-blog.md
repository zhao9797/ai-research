# Introducing Llama 3.1: Our most capable models to date
Source: https://ai.meta.com/blog/meta-llama-3-1/
Introducing Llama 3.1: Our most capable models to date

[![Meta](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=XK6ck52-T0YQ7kNvwEz0_By&_nc_oc=Ado5uMoab6HCGBI0-hzBTDXrse6OwnkLcsv3rAfBOJ6i4nObQMZ03IDDkHf3NCKNvkoNaQaa_r4gVwHJPfnDIv2-&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9j9C3-ewc7pYJK5JzBLTPoJyy1WIVz4sVgOaIGfaNuRA&oe=6A38BEB9)](/)

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

# Introducing Llama 3.1: Our most capable models to date

July 23, 2024•

15 minute read

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/452380335_1646136526224716_2406884886416151566_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=SFhMyunpQ2UQ7kNvwHFWz4i&_nc_oc=Adr8Cfx3bzn0dPItkqUGEvLb7I-ShoiV91q_9KwpaAMYhjNVyW6u6pBPMPJdiGa5OzIGDi8D63vId1fuIN7po_kA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af91gfLZfeqzAC3H9geDGRPZb-YKI3As_eRwpicwejqdJQ&oe=6A4D2686)

## Takeaways:

* Meta is committed to openly accessible AI. Read [Mark Zuckerberg’s letter](https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/) detailing why open source is good for developers, good for Meta, and good for the world.
* Bringing open intelligence to all, [our latest models](https://ai.meta.com/research/publications/the-llama-3-herd-of-models/) expand context length to 128K, add support across eight languages, and include Llama 3.1 405B—the first frontier-level open source AI model.
* Llama 3.1 405B is in a class of its own, with unmatched flexibility, control, and state-of-the-art capabilities that rival the best closed source models. Our new model will enable the community to unlock new workflows, such as synthetic data generation and model distillation.
* We’re continuing to build out Llama to be a system by providing more components that work with the model, including a reference system. We want to empower developers with the tools to create their own custom agents and new types of agentic behaviors. We’re bolstering this with [new security and safety tools](http://ai.meta.com/blog/meta-llama-3-1-ai-responsibility), including Llama Guard 3 and Prompt Guard, to help build responsibly. We’re also releasing a [request for comment](https://github.com/meta-llama/llama-toolchain/issues/6) on the Llama Stack API, a standard interface we hope will make it easier for third-party projects to leverage Llama models.
* The ecosystem is primed and ready to go with over 25 partners, including AWS, NVIDIA, Databricks, Groq, Dell, Azure, Google Cloud, and Snowflake offering services on day one.
* Try Llama 3.1 405B in the US on WhatsApp and at [meta.ai](http://www.meta.ai/) by asking a challenging math or coding question.

RECOMMENDED READS

* [Expanding the Llama ecosystem responsibly](https://ai.meta.com/blog/meta-llama-3-1-ai-responsibility/)
* [The Llama ecosystem: Past, present, and future](https://ai.meta.com/blog/llama-2-updates-connect-2023/)

Until today, open source large language models have mostly trailed behind their closed counterparts when it comes to capabilities and performance. Now, we’re ushering in a new era with open source leading the way. We’re publicly releasing Meta Llama 3.1 405B, which we believe is the world’s largest and most capable openly available foundation model. With more than 300 million total downloads of all Llama versions to date, we’re just getting started.

## Introducing Llama 3.1

Llama 3.1 405B is the first openly available model that rivals the top AI models when it comes to state-of-the-art capabilities in general knowledge, steerability, math, tool use, and multilingual translation. With the release of the 405B model, we’re poised to supercharge innovation—with unprecedented opportunities for growth and exploration. We believe the latest generation of Llama will ignite new applications and modeling paradigms, including synthetic data generation to enable the improvement and training of smaller models, as well as model distillation—a capability that has never been achieved at this scale in open source.

As part of this latest release, we’re introducing upgraded versions of the 8B and 70B models. These are multilingual and have a significantly longer context length of 128K, state-of-the-art tool use, and overall stronger reasoning capabilities. This enables our latest models to support advanced use cases, such as long-form text summarization, multilingual conversational agents, and coding assistants. We’ve also made changes to our license, allowing developers to use the outputs from Llama models—including the 405B—to improve other models. True to our commitment to open source, starting today, we’re making these models available to the community for download on [llama.meta.com](https://llama.meta.com/) and [Hugging Face](https://huggingface.co/collections/meta-llama/llama-31-669fc079a0c406a149a5738f) and available for immediate development on our broad ecosystem of partner platforms.

## Model evaluations

For this release, we evaluated performance on over 150 benchmark datasets that span a wide range of languages. In addition, we performed extensive human evaluations that compare Llama 3.1 with competing models in real-world scenarios. Our experimental evaluation suggests that our flagship model is competitive with leading foundation models across a range of tasks, including GPT-4, GPT-4o, and Claude 3.5 Sonnet. Additionally, our smaller models are competitive with closed and open models that have a similar number of parameters.

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/451735590_1030734788570365_1093008500142144333_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=gN244ZZOJ2QQ7kNvwHOmUlT&_nc_oc=AdqovNrsphQxzTEzHndhjUuXTnyXRdxcec3twX4QqqZPUfRdzNNuZRQjYeHyHf7sFwnoYuNHeI1UvWVUO0WDR4F3&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_p6_14IlKL2u5xZVOlXmq3mBq4in-S8d1DU7PG1jJ4AQ&oe=6A4D0FFE)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/452673884_1646111879501055_1352920258421649752_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=GyBgDEstm1AQ7kNvwEN8b_8&_nc_oc=AdoMyEqWIxV62yih8w9hSNwDG_zSgFmt2fKO_CkBTPutiFgDOXlj9WqtkczuiQrjv3vOk_22yW-oAUFqntGVpvbq&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9frmJJ-PAL9ZCE9aKU7E4ooZ6VL785tQxebV9_cM36mw&oe=6A4D2DA8)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/452444647_1680516006017732_6134289479575303637_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=TYnCZ-QKd0kQ7kNvwFhrHVa&_nc_oc=AdqwoWwqhxiDkO6FMS4i08gn2t9mQxc-hRMW-8U7OlCjOPwf2df6j_pjTFcdL9neO36LY9VhKatjMzXWJrqI3guN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9cSVjT7uzz2A8XrJaI84qNo4_spH5HL0MunT2sf6Y98A&oe=6A4D2029)

## Model Architecture

As our largest model yet, training Llama 3.1 405B on over 15 trillion tokens was a major challenge. To enable training runs at this scale and achieve the results we have in a reasonable amount of time, we significantly optimized our full training stack and pushed our model training to over 16 thousand H100 GPUs, making the 405B the first Llama model trained at this scale.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/452342830_524225500031704_780745667054798266_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=Y2efSxUsAcwQ7kNvwGG4hHN&_nc_oc=AdoZSjGQWJSVILZBoUX88wnZslZQtw8rjeLfn1IWNh445wlrEXwtEtWLdRjxOpx2xP-lrFBjVBYuLITBsmcA86nL&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af8uiky4vYHwtifa5VSa1cTzIObWY_A0y22EfODgT66DfQ&oe=6A4D328D)

To address this, we made design choices that focus on keeping the model development process scalable and straightforward.

* We opted for a standard decoder-only transformer model architecture with minor adaptations rather than a mixture-of-experts model to maximize training stability.
* We adopted an iterative post-training procedure, where each round uses supervised fine-tuning and direct preference optimization. This enabled us to create the highest quality synthetic data for each round and improve each capability’s performance.

Compared to previous versions of Llama, we improved both the quantity and quality of the data we use for pre- and post-training. These improvements include the development of more careful pre-processing and curation pipelines for pre-training data, the development of more rigorous quality assurance, and filtering approaches for post-training data.

As expected per scaling laws for language models, our new flagship model outperforms smaller models trained using the same procedure. We also used the 405B parameter model to improve the post-training quality of our smaller models.

To support large-scale production inference for a model at the scale of the 405B, we quantized our models from 16-bit (BF16) to 8-bit (FP8) numerics, effectively lowering the compute requirements needed and allowing the model to run within a single server node.

## Instruction and chat fine-tuning

With Llama 3.1 405B, we strove to improve the helpfulness, quality, and detailed instruction-following capability of the model in response to user instructions while ensuring high levels of safety. Our biggest challenges were supporting more capabilities, the 128K context window, and increased model sizes.

In post-training, we produce final chat models by doing several rounds of alignment on top of the pre-trained model. Each round involves Supervised Fine-Tuning (SFT), Rejection Sampling (RS), and Direct Preference Optimization (DPO). We use synthetic data generation to produce the vast majority of our SFT examples, iterating multiple times to produce higher and higher quality synthetic data across all capabilities. Additionally, we invest in multiple data processing techniques to filter this synthetic data to the highest quality. This enables us to scale the amount of fine-tuning data across capabilities.

We carefully balance the data to produce a model with high quality across all capabilities. For example, we maintain the quality of our model on short-context benchmarks, even when extending to 128K context. Similarly, our model continues to provide maximally helpful answers, even as we add safety mitigations.

## The Llama system

Llama models were always intended to work as part of an overall system that can orchestrate several components, including calling external tools. Our vision is to go beyond the foundation models to give developers access to a broader system that gives them the flexibility to design and create custom offerings that align with their vision. This thinking started last year when we first [introduced](https://ai.meta.com/blog/purple-llama-open-trust-safety-generative-ai/) the incorporation of components outside of the core LLM.

As part of our ongoing efforts to develop AI responsibly beyond the model layer and helping others to do the same, we’re releasing a full [reference system](https://github.com/meta-llama/llama-agentic-system) that includes several sample applications and includes new components such as [Llama Guard 3](https://llama.meta.com/trust-and-safety/#safeguard-model%20?), a multilingual safety model and Prompt Guard, a prompt injection filter. These sample applications are open source and can be built on by the community.

The implementation of components in this Llama System vision is still fragmented. That’s why we’ve started working with industry, startups, and the broader community to help better define the interfaces of these components. To support this, we’re releasing a [request for comment](https://github.com/meta-llama/llama-toolchain/issues/6) on GitHub for what we’re calling “Llama Stack.” Llama Stack is a set of standardized and opinionated interfaces for how to build canonical toolchain components (fine-tuning, synthetic data generation) and agentic applications. Our hope is for these to become adopted across the ecosystem, which should help with easier interoperability.

We welcome feedback and ways to improve the [proposal](https://github.com/meta-llama/llama-toolchain/issues/6)[.](https://github.com/meta-llama/llama-toolchain/issues) We’re excited to grow the ecosystem around Llama and lower barriers for developers and platform providers.

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t15.5256-10/438057453_339519052544366_6093286565889760785_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=eedc80&_nc_ohc=BBex4wzXLUsQ7kNvwGgYDgU&_nc_oc=Ado3WiDUaQnDnNzXeBt4q2coZlDBTshIZOo7YH9rkzH5EUTAHBuwxw5wDBuF6PU_4VjSY7Z27JtE4MlSWayvVyq3&_nc_zt=23&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9Oz4ULM3RLwhVNugIzpDqWIzV9lagNZiKXmxbHAbM2hg&oe=6A38AD39)](https://video-sea5-1.xx.fbcdn.net/o1/v/t2/f2/m266/AQOOYeH8O2Zv5Ae1ur6XhKBqekW2JdWzc1rXcgizCvvgbn_ivkxGRmvW96_YiEpnUacc7hBMvJM04H4vSjkkky0AbpdxYxAM6_s.mp4?strext=1&_nc_cat=107&_nc_sid=8bf8fe&_nc_ht=video-sea5-1.xx.fbcdn.net&_nc_ohc=8twvwrv5gokQ7kNvwGrNPSz&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuOTYwLmNvbXByZXNzZWRfc291cmNlIiwieHB2X2Fzc2V0X2lkIjo4MjM2NTQzNjY1NTkwNDcsImFzc2V0X2FnZV9kYXlzIjo2OTQsInZpX3VzZWNhc2VfaWQiOjEwMTI4LCJkdXJhdGlvbl9zIjo3MCwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=17-1&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&_nc_zt=28&oh=00_Af_nXTa-Y6PAsAgj0HtxZlzTU5X44Jxiv2URiYdWM1AUTw&oe=6A34A86B&bitrate=548889&tag=compressed_source)

## Openness drives innovation

Unlike closed models, Llama model weights are [available to download](https://llama.meta.com/). Developers can fully customize the models for their needs and applications, train on new datasets, and conduct additional fine-tuning. This enables the broader developer community and the world to more fully realize the power of generative AI. Developers can fully customize for their applications and run in any environment, including on prem, in the cloud, or even locally on a laptop—all without sharing data with Meta.

While many may argue that closed models are more cost effective, Llama models offer some of the lowest cost per token in the industry, according to testing by [Artificial Analysis](https://artificialanalysis.ai/). And as Mark Zuckerberg [noted](https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/), open source will ensure that more people around the world have access to the benefits and opportunities of AI, that power isn’t concentrated in the hands of a small few, and that the technology can be deployed more evenly and safely across society. That’s why we continue to take steps on the path for open access AI to become the industry standard.

We’ve seen the [community](https://llama.meta.com/community-stories/) build amazing things with past Llama models including [an AI study buddy](https://ai.meta.com/blog/foondamate-study-aid-education-llama/) built with Llama and deployed in WhatsApp and Messenger, an [LLM tailored to the medical field](https://ai.meta.com/blog/llama-2-3-meditron-yale-medicine-epfl-open-source-llm/) designed to help guide clinical decision-making, and a [healthcare non-profit startup](https://github.com/noharm-ai/summary) in Brazil that makes it easier for the healthcare system to organize and communicate patients’ information about their hospitalization, all in a data secure way. We can’t wait to see what they build with our latest models thanks to the power of open source.

## Building with Llama 3.1 405B

For the average developer, using a model at the scale of the 405B is challenging. While it’s an incredibly powerful model, we recognize that it requires significant compute resources and expertise to work with. We’ve spoken with the community, and we realize there’s so much more to generative AI development than just prompting models. We want to enable everyone to get the most out of the 405B, including:

* Real-time and batch inference
* Supervised fine-tuning
* Evaluation of your model for your specific application
* Continual pre-training
* Retrieval-Augmented Generation (RAG)
* Function calling
* Synthetic data generation

This is where the Llama ecosystem can help. On day one, developers can take advantage of all the advanced capabilities of the 405B model and start building immediately. Developers can also explore advanced workflows like easy-to-use synthetic data generation, follow turnkey directions for model distillation, and enable seamless RAG with solutions from partners, including AWS, NVIDIA, and Databricks. Additionally, Groq has optimized low-latency inference for cloud deployments, with Dell achieving similar optimizations for on-prem systems.

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/465245227_525650590344456_1770582698392042096_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=9J8muuIsdjkQ7kNvwHD_8uZ&_nc_oc=AdoFDH5TQJE3mysKCDSdUCfjpjIJ-HF3_shuHd7dsgXLu-_RiugDR6nmZhu9p25p0qdhESrSUY36qA5C8EoobyTM&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af92O8iXEAlW3-eypJdpg3am5Kj6GvOQYkj1O1Iqv1FSkQ&oe=6A4D155D)

We’ve worked with key community projects like vLLM, TensorRT, and PyTorch to build in support from day one to ensure the community is ready for production deployment.

We hope that our release of the 405B will also spur innovation across the broader community to make inference and fine-tuning of models of this scale easier and enable the next wave of research in model distillation.

## Try the Llama 3.1 collection of models today

We can’t wait to see what the community does with this work. There’s so much potential for building helpful new experiences using the multilinguality and increased context length. With the Llama Stack and new safety tools, we look forward to continuing to build together with the open source community responsibly. Before releasing a model, we work to identify, evaluate, and mitigate potential risks through several measures, including pre-deployment risk discovery exercises through red teaming, and safety fine-tuning. For example, we conduct extensive red teaming with both external and internal experts to stress test the models and find unexpected ways they may be used. (Read more about how we’re scaling our Llama 3.1 collection of models responsibly in this [blog post](http://ai.meta.com/blog/meta-llama-3-1-ai-responsibility).)

While this is our biggest model yet, we believe there’s still plenty of new ground to explore in the future, including more device-friendly sizes, additional modalities, and more investment at the agent platform layer.As always, we look forward to seeing all the amazing products and experiences the community will build with these models.

*This work was supported by our partners across the AI community. We’d like to thank and acknowledge (in alphabetical order): Accenture, Amazon Web Services, AMD, Anyscale, CloudFlare, Databricks, Dell, Deloitte, Fireworks.ai, Google Cloud, Groq, Hugging Face, IBM WatsonX, Infosys, Intel, Kaggle, Microsoft Azure, NVIDIA, OctoAI, Oracle Cloud, PwC, Replicate, Sarvam AI, Scale.AI, SNCF, Snowflake, Together AI, and vLLM project developed in Sky Computing Lab at UC Berkeley.*

[Get started with Llama 3.1](https://llama.meta.com/)[Read the Llama 3.1 paper](https://ai.meta.com/research/publications/the-llama-3-herd-of-models/)[Visit the Llama GitHub repo](https://github.com/meta-llama/llama-models)[Download Llama 3.1 on Hugging Face](https://huggingface.co/collections/meta-llama/llama-31-669fc079a0c406a149a5738f)

---

Share:

---

Our latest updates delivered to your inbox

[Subscribe](https://ai.facebook.com/subscribe/) to our newsletter to keep up with Meta AI news, events, research breakthroughs, and more.

Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/452200370_449648051376886_8640872118555060010_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=45pBsK6TF4QQ7kNvwFJD8SP&_nc_oc=AdrmhleWLOvQSaYr_7j8krrJa7Bf-3aA--O0_rrZSdGBRfizDwSwhlRjBl3nc6KZQ2eyJ_idmp_KyA_F0PRe0jjK&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-lTj_mXWQ2rg9EYU2ZGj67zwA36n2OqCcnBdjJ-uKq8A&oe=6A4D06A9)

Open Source

Expanding our open source large language models responsibly

July 23, 2024

[Read post](https://ai.meta.com/blog/meta-llama-3-1-ai-responsibility/)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/441887542_458900317075837_3768303019386397812_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=Wgs8Kp14ggMQ7kNvwFWOl_K&_nc_oc=Ado0yuAjLZIpyRDPlFS-Yqfbgr3Ab-2h1stCEkE7JDoVlKL82GrPzf8r3jhu-tpLb7S3cVyOw87h4deDJ7y0a_vf&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af92o9zW78C08zNzyF-pQLQnHzFAKnERgQSpyiOLuZLxTg&oe=6A4D3587)

Large Language Model

A social ‘study buddy’ gets a conversational lift from Meta Llama

June 6, 2024

[Read post](https://ai.meta.com/blog/foondamate-study-aid-education-llama/)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/439645618_745665614390489_272535049175550402_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=vTMlVSJYZxsQ7kNvwHSlZkn&_nc_oc=AdqC6-8tDQ7yvpYUFzxhjHTQEK2YN5MXgLVRIlbDNwLIxyh1OFuXOelEzHe3lI_ufxWCn9Ca6EhN71ruSRgcCnYe&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af8q1FEV1vWAWYN37tjroSAlkNXDa43_6IzxGqx4-GoPJA&oe=6A4D2942)

Large Language Model

How SAIF CHECK is using Meta Llama 3 to validate and build trust in AI models

June 20, 2024

[Read post](https://ai.meta.com/blog/saif-check-llama-3-validation-trust/)

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

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=C2HG24npvwYQ7kNvwG0RyrH&_nc_oc=AdptCqVJQJPLbRtXnSREzEZnlux7g_82gv50avE_ri2mE328tNh5MOIPxrPKQQS3-EawsNIB37KqH4mD_w698D-2&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af97MHRAg6Ij-lUnxGs39xV1UaMS0VLGCqugp5Yo-kFxKA&oe=6A4D2878)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=bJOdWS-UzpEQ7kNvwHEWSJk&_nc_oc=AdqY7cuE1VsRQzWKKPHkHeK7M_IuidVlFR2W3Ff3aS0-h6UQr-yqNzH16ykxxOeM1cJG0cCC710ssQ1y0uhcI19D&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-F_Krhp0IhxM4o8kvFdeHHoMRrpVSpYlEk0SXVsRTd1A&oe=6A4D2D4F)

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9AFcrkilwCmBEXqGG2HsZCghjHR_BNsIdd4RT6AqwFmw&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9AFcrkilwCmBEXqGG2HsZCghjHR_BNsIdd4RT6AqwFmw&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_kXYi-Gz6u4rfsyq5ogiQnwoC24xAQD8FDObzzPdU5-g&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_kXYi-Gz6u4rfsyq5ogiQnwoC24xAQD8FDObzzPdU5-g&oe=6A38A722)](https://twitter.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-icoOO2Lpoo0_hOKgpGlWGt5K5t-8UuP9o00lc-Ix9hw&oe=6A389ABB)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-icoOO2Lpoo0_hOKgpGlWGt5K5t-8UuP9o00lc-Ix9hw&oe=6A389ABB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_ycUAYXPUzq_H80x-Po-iPc2ne7dNw62-HcY0XBLoWug&oe=6A38B42E)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_ycUAYXPUzq_H80x-Po-iPc2ne7dNw62-HcY0XBLoWug&oe=6A38B42E)](https://www.youtube.com/@aiatmeta)

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

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9AFcrkilwCmBEXqGG2HsZCghjHR_BNsIdd4RT6AqwFmw&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9AFcrkilwCmBEXqGG2HsZCghjHR_BNsIdd4RT6AqwFmw&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_kXYi-Gz6u4rfsyq5ogiQnwoC24xAQD8FDObzzPdU5-g&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_kXYi-Gz6u4rfsyq5ogiQnwoC24xAQD8FDObzzPdU5-g&oe=6A38A722)](https://twitter.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-icoOO2Lpoo0_hOKgpGlWGt5K5t-8UuP9o00lc-Ix9hw&oe=6A389ABB)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-icoOO2Lpoo0_hOKgpGlWGt5K5t-8UuP9o00lc-Ix9hw&oe=6A389ABB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_ycUAYXPUzq_H80x-Po-iPc2ne7dNw62-HcY0XBLoWug&oe=6A38B42E)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm1&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_ycUAYXPUzq_H80x-Po-iPc2ne7dNw62-HcY0XBLoWug&oe=6A38B42E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.facebook.com/policies/)

[Cookies](https://www.facebook.com/policies/cookies/)

Meta © 2026

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9AFcrkilwCmBEXqGG2HsZCghjHR_BNsIdd4RT6AqwFmw&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwE0dbHm&_nc_oc=Adr-WnTHL0BSNp0h9kBNPC3QknT0tnjoWOSgDkjhNipEVJcRCbED1Qpytd_FdoNADoDsGwbeSQpiOhd7hZVCF54R&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af9AFcrkilwCmBEXqGG2HsZCghjHR_BNsIdd4RT6AqwFmw&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_kXYi-Gz6u4rfsyq5ogiQnwoC24xAQD8FDObzzPdU5-g&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwFsK58z&_nc_oc=AdpycVula8EMnn3wYvFzGzPiGm90eIc22RUWwnSJ4QkhQXK5UjVst3G260qALJMba-zy3twpr9IdxN8nwl8QoFxN&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af_kXYi-Gz6u4rfsyq5ogiQnwoC24xAQD8FDObzzPdU5-g&oe=6A38A722)](https://twitter.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-icoOO2Lpoo0_hOKgpGlWGt5K5t-8UuP9o00lc-Ix9hw&oe=6A389ABB)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwE8L8Yd&_nc_oc=Adr2K1cexitmtKrr-o7qNNaqZQtv4iFrgmmvKnwnfF9Lz2CpBNgY5iNh0ZN1tnou57uXZpmOAwVRBnkbFiQzrIab&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=DPyTcTwS4Dep5qd4kZL6jw&_nc_ss=7b289&oh=00_Af-icoOO2Lpoo0_hOKgpGlWGt5K5t-8UuP9o00lc-Ix9hw&oe=6A389ABB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwFrWaSz&_nc_oc=AdqK37LccYmpqyCnBVKejEa6h357fxmQD_fKaJpbxoYMXUbnVuyYHn5fM1iInsdXVDFx0ezZ8GCrcEcdCoFfdmm

[truncated]
