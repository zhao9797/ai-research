# Llama 3.2: Revolutionizing edge AI and vision with open, customizable models
Source: https://ai.meta.com/blog/llama-3-2-connect-2024-vision-edge-mobile-devices/
Llama 3.2: Revolutionizing edge AI and vision with open, customizable models

[![Meta](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=XK6ck52-T0YQ7kNvwFlWEeZ&_nc_oc=AdpIuMfXawOjagnUKqLLbboYrVlxpoVixtjYG1dDTd9K3QJQTZxFrvVdAWe5LSltiCD1mVTY03wZ6GzqBvqoH3dR&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-_uK-btIvzsPEK-2uS0kBf38vtnBxhhF2RfhECBX9M3g&oe=6A38BEB9)](/)

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

FEATURED

Large Language Model

# Llama 3.2: Revolutionizing edge AI and vision with open, customizable models

September 25, 2024•

15 minute read

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/461179924_892945479558448_4846394290454647920_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=WyGpmkW3hSUQ7kNvwGKTfe2&_nc_oc=AdpizjcSO1BUadUVvR6QWP7aOjEnhdGVYb-e9hPNYvmKTRNUwo7w1yK_O5FEcwcGFhQse1Xi7qOhE3mxhaPgbQNa&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_-Z0vhTaXewRqJeRf8Va8iS8vZbwjcL2W4txBqcJbwLw&oe=6A4D0090)

## Takeaways:

* Today, we’re releasing Llama 3.2, which includes small and medium-sized vision LLMs (11B and 90B), and lightweight, text-only models (1B and 3B) that fit onto edge and mobile devices, including pre-trained and instruction-tuned versions.
* The Llama 3.2 1B and 3B models support context length of 128K tokens and are state-of-the-art in their class for on-device use cases like summarization, instruction following, and rewriting tasks running locally at the edge. These models are enabled on day one for Qualcomm and MediaTek hardware and optimized for Arm processors.
* Supported by a broad ecosystem, the Llama 3.2 11B and 90B vision models are drop-in replacements for their corresponding text model equivalents, while exceeding on image understanding tasks compared to closed models, such as Claude 3 Haiku. Unlike other open multimodal models, both pre-trained and aligned models are available to be fine-tuned for custom applications using torchtune and deployed locally using torchchat. They’re also available to try using our smart assistant, Meta AI.
* We’re sharing the first official [Llama Stack](https://github.com/meta-llama/llama-stack) distributions, which will greatly simplify the way developers work with Llama models in different environments, including single-node, on-prem, cloud, and on-device, enabling turnkey deployment of retrieval-augmented generation (RAG) and tooling-enabled applications with integrated safety.
* We’ve been working closely with partners like AWS, Databricks, Dell Technologies, Fireworks, Infosys, and Together AI to build Llama Stack distributions for their downstream enterprise clients. On-device distribution is via PyTorch [ExecuTorch](https://github.com/pytorch/executorch), and single-node distribution is via Ollama.
* We continue to share our work because we believe [openness drives innovation and is good for developers, Meta, and the world](https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/). Llama is already leading the way on openness, modifiability, and cost efficiency—enabling more people to have creative, useful, and life-changing breakthroughs using generative AI.
* We’re making Llama 3.2 models available for download on [llama.com](https://llama.meta.com/) and [Hugging Face](https://huggingface.co/meta-llama), as well as available for immediate development on our broad ecosystem of partner platforms, including AMD, AWS, Databricks, Dell, Google Cloud, Groq, IBM, Intel, Microsoft Azure, NVIDIA, Oracle Cloud, Snowflake, and more.

We’ve been excited by the [impact the Llama 3.1 herd of models have made](https://ai.meta.com/blog/llama-usage-doubled-may-through-july-2024/) in the two months since we announced them, including the [405B](https://www.meta.ai/?utm_source=llama_meta_site&utm_medium=web&utm_content=Llama_nav&utm_campaign=July_moment)—the first open frontier-level AI model. While these models are incredibly powerful, we recognize that building with them requires significant compute resources and expertise. We’ve also heard from developers who don’t have access to these resources and still want the opportunity to build with Llama. As Meta Founder and CEO Mark Zuckerberg shared today at Connect, they won’t have to wait any longer. Today, we’re releasing Llama 3.2, which includes small and medium-sized vision LLMs (11B and 90B) and lightweight, text-only models (1B and 3B) that fit onto select edge and mobile devices.

It’s only been a year and a half since we first announced Llama, and we’ve made incredible progress in such a short amount of time. This year, [Llama has achieved 10x growth](https://ai.meta.com/blog/llama-usage-doubled-may-through-july-2024/) and become the standard for responsible innovation. Llama also continues to lead on openness, modifiability, and cost efficiency, and it’s competitive with closed models—even leading in some areas. We believe that openness drives innovation and is the right path forward, which is why we continue to share our research and collaborate with our partners and the developer community.

We’re making Llama 3.2 models available for download on [llama.com](https://llama.meta.com/) and [Hugging Face](https://huggingface.co/meta-llama), as well as available for immediate development on our broad ecosystem of partner platforms. Partners are an important part of this work, and we’ve worked with over 25 companies, including AMD, AWS, Databricks, Dell, Google Cloud, Groq, IBM, Intel, Microsoft Azure, NVIDIA, Oracle Cloud, and Snowflake, to enable services on day one. For the Llama 3.2 release, we’re also working with on-device partners Arm, MediaTek, and Qualcomm to offer a broad range of services at launch. Starting today, we’re also making [Llama Stack](https://github.com/meta-llama/llama-stack) available to the community. More details on the latest release, including information on the [multimodal availability](https://euneedsai.com/) in Europe, can be found in [our acceptable use policy](https://github.com/meta-llama/llama-models/blob/main/models/llama3_2/USE_POLICY.md).

## Meet Llama 3.2

The two largest models of the Llama 3.2 collection, 11B and 90B, support image reasoning use cases, such as document-level understanding including charts and graphs, captioning of images, and visual grounding tasks such as directionally pinpointing objects in images based on natural language descriptions. For example, a person could ask a question about which month in the previous year their small business had the best sales, and Llama 3.2 can then reason based on an available graph and quickly provide the answer. In another example, the model could reason with a map and help answer questions such as when a hike might become steeper or the distance of a particular trail marked on the map. The 11B and 90B models can also bridge the gap between vision and language by extracting details from an image, understanding the scene, and then crafting a sentence or two that could be used as an image caption to help tell the story.

The lightweight 1B and 3B models are highly capable with multilingual text generation and tool calling abilities. These models empower developers to build personalized, on-device agentic applications with strong privacy where data never leaves the device. For example, such an application could help summarize the last 10 messages received, extract action items, and leverage tool calling to directly send calendar invites for follow-up meetings.

Running these models locally comes with two major advantages. First, prompts and responses can feel instantaneous, since processing is done locally. Second, running models locally maintains privacy by not sending data such as messages and calendar information to the cloud, making the overall application more private. Since processing is handled locally, the application can clearly control which queries stay on the device and which may need to be processed by a larger model in the cloud.

## Model evaluations

Our evaluation suggests that the Llama 3.2 vision models are competitive with leading foundation models, Claude 3 Haiku and GPT4o-mini on image recognition and a range of visual understanding tasks. The 3B model outperforms the Gemma 2 2.6B and Phi 3.5-mini models on tasks such as following instructions, summarization, prompt rewriting, and tool-use, while the 1B is competitive with Gemma.

We evaluated performance on over 150 benchmark datasets that span a wide range of languages. For the vision LLMs, we evaluated performance on benchmarks for image understanding and visual reasoning.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/461288018_1255239495501495_271827633811450582_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=RjiwtnF5IvsQ7kNvwGjPbim&_nc_oc=Adpoy8tUnUO4abBUcTqQe37ujRQhlWzOmr37KOJ9ik6Xvlx-bQHxq1Sn4F4Wpm9V6MRP40x6NWgQLYyYVl0FE6gz&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_rI-nILZd3pVQrxWBnwXbeQTyzQHcz8qz3ErDWzwp0TA&oe=6A4D04ED)![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/461157789_931406385491961_1692349435372036848_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=SHF20eTqnWMQ7kNvwEMUNTA&_nc_oc=AdqeHkFcGGicqXU37HoXuUald91_YS5rMkZa1yE_1Un3ZnCRknmHJZR60N5VAa3rtowIvVTg-OJirdOulVUfO-yc&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_obPp9vl7B3HfzXT0Wln6CoWxN-qAR1igxt2RtBfdRIA&oe=6A4D1C58)

## Vision models

As the first Llama models to support vision tasks, the 11B and 90B models required an entirely new model architecture that supports image reasoning.

To add image input support, we trained a set of adapter weights that integrate the pre-trained image encoder into the pre-trained language model. The adapter consists of a series of cross-attention layers that feed image encoder representations into the language model. We trained the adapter on text-image pairs to align the image representations with the language representations. During adapter training, we also updated the parameters of the image encoder, but intentionally did not update the language-model parameters. By doing that, we keep all the text-only capabilities intact, providing developers a drop-in replacement for Llama 3.1 models.

Our training pipeline consists of multiple stages, starting from pretrained Llama 3.1 text models. First, we add image adapters and encoders, then pretrain on large-scale noisy (image, text) pair data. Next, we train on medium-scale high quality in-domain and knowledge-enhanced (image, text) pair data.

In post-training, we use a similar recipe as the text models by doing several rounds of alignment on supervised fine-tuning, rejection sampling, and direct preference optimization. We leverage synthetic data generation by using the Llama 3.1 model to filter and augment question and answers on top of in-domain images, and use a reward model to rank all the candidate answers to provide high quality fine-tuning data. We also add safety mitigation data to produce a model with a high level of safety while retaining helpfulness of the mode

The end result is a set of models that can take in both image and text prompts, and deeply understand and reason on the combination. This is another step toward Llama models having even richer agentic capabilities.

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t15.5256-10/461056114_513962811237812_8614398012684914528_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=b07905&_nc_ohc=cyHIjtQox1sQ7kNvwFKnwr3&_nc_oc=AdpBc0WS8fPVZAcyG_21B-O43-MkQItuo870jW8hRusROITLO3_vsH5KERbsrUXdS3udGdlKrhhW8LAbHVi_g1ok&_nc_zt=23&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_NNuMEr2qublKZo3o-KUe7RRTBmLLzl8pf8wejF9r4Mw&oe=6A38BCBF)](https://video-sea5-1.xx.fbcdn.net/o1/v/t2/f2/m266/AQOohfHCdNCPm_12hmuOO9h1XA9DJ_Oyv_TyzZobLdK9GdWv3KoOrrClHV35xUPOAlMTt1WjrHsHcEj5_p1E2DYjG_bAqn68yzI.mp4?strext=1&_nc_cat=107&_nc_sid=8bf8fe&_nc_ht=video-sea5-1.xx.fbcdn.net&_nc_ohc=99cbzufpEvwQ7kNvwGo0kq6&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTUwMC5jb21wcmVzc2VkX3NvdXJjZSIsInhwdl9hc3NldF9pZCI6MjIwNTA4MDAyOTg5MDk3NCwiYXNzZXRfYWdlX2RheXMiOjYzMSwidmlfdXNlY2FzZV9pZCI6MTAxMjgsImR1cmF0aW9uX3MiOjM0LCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=17-1&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&_nc_zt=28&oh=00_Af-2gzYk0FJLIjcvb5HVQp5tkDggv4f65GN16iy3fyXiNA&oe=6A34A69F&bitrate=1034270&tag=compressed_source)

## Lightweight models

As we talked about with Llama 3.1, powerful teacher models can be leveraged to create smaller models that have improved performance. We used two methods—pruning and distillation—on the 1B and 3B models, making them the first highly capable lightweight Llama models that can fit on devices efficiently.

Pruning enabled us to reduce the size of extant models in the Llama herd while recovering as much knowledge and performance as possible. For the 1B and 3B models, we took the approach of using structured pruning in a single shot manner from the Llama 3.1 8B. This involved systematically removing parts of the network and adjusting the magnitude of the weights and gradients to create a smaller, more efficient model that retains the performance of the original network.

Knowledge distillation uses a larger network to impart knowledge on a smaller network, with the idea that a smaller model can achieve better performance using a teacher than it could from scratch. For the 1B and 3B in Llama 3.2, we incorporated logits from the Llama 3.1 8B and 70B models into the pre-training stage of the model development, where outputs (logits) from these larger models were used as token-level targets. Knowledge distillation was used after pruning to recover performance.

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/461209081_511117684875670_45564063096782202_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=RISeMp_D0DQQ7kNvwGiMAz9&_nc_oc=AdpMhEzxgIAxGePUF9NwNCrG0FdrvYHdGmomnY-qelCm5NrCVi61wFj1PK1tzRnrBc4AZtsqHAJHoTtJb2csyHaY&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af9oiask9M5_-CMOzqvFTBh_9LpuFJzrbm1sKwh80oS9fQ&oe=6A4D045E)

In post-training, we use a similar recipe as Llama 3.1 and produce final chat models by doing several rounds of alignment on top of the pre-trained model. Each round involves supervised fine-tuning (SFT), rejection sampling (RS), and direct preference optimization (DPO).

In post-training, we scale context length support to 128K tokens, while maintaining the same quality as the pre-trained model. We also engage in synthetic data generation that goes through careful data processing and filtering to ensure high quality. We carefully blend the data to optimize for high quality across multiple capabilities like summarization, rewriting, instruction following, language reasoning, and tool use.

To enable the community to innovate on these models, we worked closely with Qualcomm and Mediatek, the top two mobile system on a chip (SoC) companies in the world, and Arm, who provides the foundational compute platform for [99](https://www.arm.com/company)[%](https://www.arm.com/company) of mobile devices. The weights being released today are based on BFloat16 numerics. Our teams are actively exploring quantized variants that will run even faster, and we hope to share more on that soon.

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t15.5256-10/461175777_1232835904725128_2221758518972028631_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=b07905&_nc_ohc=H0-paD4S5LwQ7kNvwF_ffgi&_nc_oc=AdqMSnhTx64CO_VeSTi0V5iVF8TGGC4qAncvV_WxwEZ8UuDApwEPcfB7ORC6vnI91xWy739nxUqowqRuq48G7twi&_nc_zt=23&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_dv9cQZKN6pWbsEdp4aMJjy4eRM3HCKzU6HEwf6yJbmw&oe=6A389CB2)](https://video-sea1-1.xx.fbcdn.net/o1/v/t2/f2/m266/AQOyR4sN2EUPZhMNC_k0g_4KgDI0aLLqmM0icGEaC9WMp5_MJ8ZgF54xrw3h8d2OvKpPssnB5aWtpB3rXquMqJ1UX-1fKEnnV2Y.mp4?strext=1&_nc_cat=101&_nc_sid=8bf8fe&_nc_ht=video-sea1-1.xx.fbcdn.net&_nc_ohc=ndUMOceMkAkQ7kNvwH2lF1e&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTgyMC5jb21wcmVzc2VkX3NvdXJjZSIsInhwdl9hc3NldF9pZCI6ODUwODg3MDAwNDY3NDcyLCJhc3NldF9hZ2VfZGF5cyI6NjMwLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6MTgsInVybGdlbl9zb3VyY2UiOiJ3d3cifQ%3D%3D&ccb=17-1&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&_nc_zt=28&oh=00_Af-5m8tHF0a7IKNtct7_-9B337gfJi6O9qXKNOMje6zlLw&oe=6A349C55&bitrate=1118334&tag=compressed_source)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t15.5256-10/461266248_500239006240707_7896476132563198179_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=b07905&_nc_ohc=S7WOfzy1XdIQ7kNvwHgTS_S&_nc_oc=AdqMgSc5_Sk_yl5KXw22atT82tiUAGF7t5zq0CvodaZwUf-OtJcjs1iIqCW18Xy0nkqwmHvT02jIVKrCtuNH_T4K&_nc_zt=23&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af8Pp1JhPcD_cB8BPISwiyryhdy_SVz_EeKpcHa7YPaePw&oe=6A38BAAF)](https://video-sea5-1.xx.fbcdn.net/o1/v/t2/f2/m266/AQOHP9omwRw3UT2mXktAtzt4Vd5V4qTSJMAq6wYH9ICw-lBrVyhjff7wd1hS0UmDBvrm5D9KI8aX4bZDAN-UhIaPfD4PHoSrzeY.mp4?strext=1&_nc_cat=102&_nc_sid=8bf8fe&_nc_ht=video-sea5-1.xx.fbcdn.net&_nc_ohc=_9YmrrVWc_UQ7kNvwEyneYT&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTgyMC5jb21wcmVzc2VkX3NvdXJjZSIsInhwdl9hc3NldF9pZCI6MjgxNDY5NDA4ODgyOTg3MywiYXNzZXRfYWdlX2RheXMiOjYzMCwidmlfdXNlY2FzZV9pZCI6MTAxMjgsImR1cmF0aW9uX3MiOjIxLCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=17-1&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&_nc_zt=28&oh=00_Af9rh_gE4owY5KEQR-y531LYof5ucaZDsy0qpkfjEwEn_g&oe=6A34D228&bitrate=924042&tag=compressed_source)

This demo is based on an unreleased quantized model.

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t15.5256-10/460968799_1051568729954907_4307399417507307983_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=b07905&_nc_ohc=yfbv5JMzMagQ7kNvwF0si2M&_nc_oc=AdrJAajEaIpb0dxNT5BKUl9t0eGKqq72qPazTccYQNiM4b5inulKzQ9mocKoMiyfZW8ibcL30CAc8v19XQRjWi7O&_nc_zt=23&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-db2g4J6k9KsnwinG0kMCv-deLBOPXP2Emuzu6Ai8n1A&oe=6A389A72)](https://video-sea1-1.xx.fbcdn.net/o1/v/t2/f2/m266/AQM_l8wHXotefQe3AMM2yh5yB1n_b7MEkCTZWvF4v7JFcLICbbd6okADyIMmZRn_aUvyKIqcWdJlfcVKFa8sETNPF2MIN6SL9bU.mp4?strext=1&_nc_cat=101&_nc_sid=8bf8fe&_nc_ht=video-sea1-1.xx.fbcdn.net&_nc_ohc=loeGFTJtt8gQ7kNvwFtRYFN&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTI4MC5jb21wcmVzc2VkX3NvdXJjZSIsInhwdl9hc3NldF9pZCI6Mzk2MzE1MTE2NjM5MDI2LCJhc3NldF9hZ2VfZGF5cyI6NjMxLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6MTYsInVybGdlbl9zb3VyY2UiOiJ3d3cifQ%3D%3D&ccb=17-1&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&_nc_zt=28&oh=00_Af84u6zKw9Ugir8o4r4OWmMPwGummHG1ryiy_fLY9jDh8g&oe=6A34C33D&bitrate=897016&tag=compressed_source)

This demo is based on an unreleased quantized model.

## Llama Stack distributions

In July, we released a request for comment on the Llama Stack API, a standardized interface for canonical toolchain components (fine-tuning, synthetic data generation) to customize Llama models and build agentic applications. The engagement has been great.

Since then, we have been working hard to make the API real. We built a reference implementation of the APIs for inference, tool use, and RAG. In addition, we have been working with partners to adapt them to become providers for the APIs. Finally, we have introduced Llama Stack Distribution as a way to package multiple API Providers that work well together to provide a single endpoint for developers. We are now sharing with the community a simplified and consistent experience that will enable them to work with Llama models in multiple environments, including on-prem, cloud, single-node, and on-device.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/460924239_3402957093334534_4357083070437107157_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=YlWjCCzo2HAQ7kNvwGMod7m&_nc_oc=Adobyukck4MAnXNPUfd4Y3bdV_FOpctsOc23LBSTiW8NUO_8cMBQG4PAQKatzez_CZ_ImKeg7MYTekEY6dPWgzAW&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af8i6rHc_7IbNXSuXw7S-5zg1qFeupKsm1jbrR2pYsCjHQ&oe=6A4D1EE0)

The full set of releases includes:

1. Llama CLI (command line interface) to build, configure, and run Llama Stack distributions
2. Client code in multiple languages, including python, node, kotlin, and swift
3. Docker containers for Llama Stack Distribution Server and Agents API Provider
4. Multiple distributions
   1. Single-node Llama Stack Distribution via Meta internal implementation and Ollama
   2. Cloud Llama Stack distributions via AWS, Databricks, Fireworks, and Together
   3. On-device Llama Stack Distribution on iOS implemented via PyTorch ExecuTorch
   4. On-prem Llama Stack Distribution supported by Dell

We look forward to working with developers and partners to simplify all aspects of building with Llama models and welcome feedback.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/460942153_931942502081982_4461283719059292584_n.png?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=QfitoAhkSycQ7kNvwEibaq1&_nc_oc=Ado9rQAvoR9kN6aL0ycoUjvi-m_o5TqMJeVy3kATLocApJGVhqlv5M2hnAsCQh2-XIrsNVgxH-Lz5vAfopYgJmJj&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af8X8NO-NPIh6_MRTsSninyMpUEyQIl7spydy4O-hSWzfA&oe=6A4D2D15)

## System level safety

Taking an open approach has many benefits. It helps ensure that more people around the world can access the opportunities that AI provides, guards against concentrating power in the hands of a small few, and deploys technology more equitably and safely across society. As we continue to innovate, we also want to make sure we’re empowering developers to build safe and responsible systems.

Building on our previous release and continuous effort to support responsible innovation, today we’re adding new updates to our family of safeguards:

* First, we’re releasing Llama Guard 3 11B Vision, which is designed to support Llama 3.2’s new image understanding capability and filter text+image input prompts or text output responses to these prompts.
* Second, as we released 1B and 3B Llama models to be used in more constrained environments like on-device, we also optimized Llama Guard to drastically reduce its deployment cost. Llama Guard 3 1B is based on the Llama 3.2 1B model and has been pruned and quantized bringing its size from 2,858 MB down to 438 MB, making it more efficient than ever to deploy.

These new solutions are integrated into our reference implementations, demos, and applications and are ready for the open source community to use on day one.

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t15.5256-10/461286504_3795120387436397_5947879418794172056_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=b07905&_nc_ohc=dgZo788NvgoQ7kNvwGHowhY&_nc_oc=AdqL5a_v29tdMWiC_wQ0GMg05aUA81Ajh62C85ddA8NN4IgWPblAAPFEQzSb-zSpDDra73r99z8FRudXpfjkEqnd&_nc_zt=23&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-XlA9C8JWaIlnU_G3mh8goIZZlJ9ix3VnckTzI0D0MCg&oe=6A38AE1A)](https://video-sea5-1.xx.fbcdn.net/o1/v/t2/f2/m266/AQOzfu4QhP7qa8pDhiBx-ybH4vnYFSN5_hdAIkvBLjDpUaAsD1oib14_BOdT90aI_aUynZ9TR8HZEMHj4MTYuNn1facfeN6tviY.mp4?strext=1&_nc_cat=109&_nc_sid=8bf8fe&_nc_ht=video-sea5-1.xx.fbcdn.net&_nc_ohc=tHNCE4dVAZgQ7kNvwHIng6X&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTgyMC5jb21wcmVzc2VkX3NvdXJjZSIsInhwdl9hc3NldF9pZCI6MTEwNjY0ODQzNzY5OTcxNywiYXNzZXRfYWdlX2RheXMiOjYzMCwidmlfdXNlY2FzZV9pZCI6MTAxMjgsImR1cmF0aW9uX3MiOjI5LCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=17-1&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&_nc_zt=28&oh=00_Af_QHP_uk_YZktgIFYIea9DRM_bjKZ8envyreQJ-U5XKeQ&oe=6A34ACF5&bitrate=542094&tag=compressed_source)

## Try Llama 3.2 today

Llama 3.2 is poised to reach more people than ever before and enable exciting new use cases. We believe sharing these models with the open source community isn’t enough. We want to make sure developers also have the tools they need to build with Llama responsibly. As part of our continued responsible release efforts, we’re offering developers new [tools and resources](https://ai.meta.com/blog/responsible-ai-connect-2024/), and as always, we’ll update best practices in our [Responsible Use Guide](https://ai.meta.com/static-resource/responsible-use-guide/).

We continue to share the latest advancements in the Llama ecosystem because we believe openness drives innovation and is good for developers, Meta, and the world. We’re excited to continue the conversations we’re having with our partners and the open source community, and as always, we can’t wait to see what the community builds using Llama 3.2 and Llama Stack.

*This work was supported by our partners across the AI community. We’d like to thank and acknowledge (in alphabetical order): Accenture, AMD, Arm, AWS, Cloudflare, Databricks, Dell, Deloitte, Fireworks.ai, Google Cloud, Groq, Hugging Face, IBM watsonx, Infosys, Intel, Kaggle, Lenovo, LMSYS, MediaTek, Microsoft Azure, NVIDIA, OctoAI, Ollama, Oracle Cloud, PwC, Qualcomm, Sarvam AI, Scale AI, Snowflake, Together AI, and UC Berkeley - vLLM Project.*

[Learn more on the Llama website](https://www.llama.com/)

[Visit Hugging Face](https://huggingface.co/meta-llama)

---

Share:

---

Our latest updates delivered to your inbox

[Subscribe](https://ai.facebook.com/subscribe/) to our newsletter to keep up with Meta AI news, events, research breakthroughs, and more.

Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/460981187_554072500307898_6342706179093701619_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=2A86eL-tV88Q7kNvwFIt1KJ&_nc_oc=AdoDS8oUqdUvKFMQh3G3weTxn5vKJBFhjvIaVvb6hA_9wYAuRK50GvqRjwqQKcQjfsLWvFQdzp-dlTNFK2qXilQ8&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-QO2dxaA4_M4nDElJpDlwh1vC8vH3faYnj-utsKIXbxg&oe=6A4D2ECB)

Responsible AI

Connect 2024: The responsible approach we’re taking to generative AI

September 25, 2024

[Read post](https://ai.meta.com/blog/responsible-ai-connect-2024/)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/457150402_870575128016623_8609219656406574252_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=0vTHgdlBTUEQ7kNvwG3qBh0&_nc_oc=AdrP0beLAPE_r5YBHLZ8QEWnYbrZTzSPjHbvbhaCqZhVM7RLYm-NvdhBPagCn09n0SII5faacvfRRreH-vrZR72E&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af8zvFjU17P9nerFcSQ4VV4ajj1FaQnt4PYFZJAmDFrU1g&oe=6A4D2BD5)

With 10x growth since 2023, Llama is the leading engine of AI innovation

August 29, 2024

[Read post](https://ai.meta.com/blog/llama-usage-doubled-may-through-july-2024/)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/460055422_2744099152427826_2112966215088891339_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=OfTGbjwvThMQ7kNvwGx_D-Z&_nc_oc=Adosx-cXblyeT3NDqILINOkUw7JcpRuZWTWGgr9o8N6B3nk4nOhUmQ5vdf4k_NMLItFRqrt26TfIz49nkWVf5OI9&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af8-NWPivNbhuL7_F2lVZ86Rz8ccEllti5pDEdbW_TmDpw&oe=6A4D1F11)

Open Source

Generate an entire app from a prompt using Together AI’s LlamaCoder

September 18, 2024

[Read post](https://ai.meta.com/blog/together-ai-llamacoder/)

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

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=C2HG24npvwYQ7kNvwHAH2e6&_nc_oc=AdpCJux6uVmKYiat2kni8-jXETldtNNT6zRuQYhCPWFAQZXQzDv1XnEXXoGgyKDUyxwqvMuGiqHz5zPbQthevbcb&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-GmbPHfDIsNWF7qq528r0Qz_-4IWOXV6KmelP9Ktsemg&oe=6A4D2878)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=bJOdWS-UzpEQ7kNvwG2QCqT&_nc_oc=Adot26PGLpuEp86kgNfqvX9udx3OARf23IRm1_Tso_lTXeQQs-p-vWN-EysvsbJ3QOE2oCOJHp-HEkEYsrPUFhdn&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af9vNYLn31THh9j9wThOrc4LWJ-ACxGzPC5ip0wwsC6c1w&oe=6A4D2D4F)

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwFi_027&_nc_oc=AdoD_VI539zTt7tAZA22gJewiGThmzL_FhCn9un2BvXM_jMy8bKiHrsNfhvDh5BulzuTDN-NwypjfhIfBoUqHDlO&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af95m44sOyLj7j3CUd3Pwa9nNOprhoI24llMnsimng24vg&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwFi_027&_nc_oc=AdoD_VI539zTt7tAZA22gJewiGThmzL_FhCn9un2BvXM_jMy8bKiHrsNfhvDh5BulzuTDN-NwypjfhIfBoUqHDlO&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af95m44sOyLj7j3CUd3Pwa9nNOprhoI24llMnsimng24vg&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwHnCq6X&_nc_oc=AdpYj833LUmFcjRZRQZKBXuHSbUAXanosUko6WXylxh2OHVMrJJXbs2xBgxKY-4t07uS2qypJLxP5n8FwXMs81YM&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af82xPULRQOFWmDJ447_o5h--_1_UF6_ypNNf2bEtwowOA&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwHnCq6X&_nc_oc=AdpYj833LUmFcjRZRQZKBXuHSbUAXanosUko6WXylxh2OHVMrJJXbs2xBgxKY-4t07uS2qypJLxP5n8FwXMs81YM&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af82xPULRQOFWmDJ447_o5h--_1_UF6_ypNNf2bEtwowOA&oe=6A38A722)](https://twitter.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwEP-5un&_nc_oc=AdpxkwJli-NiXi1fV-ixSFlqi5pmHNM_a5Afwk1TI8YT1z5vGA4FeYkqthFx6FB6kElnVTmGIfTKtZ9XYPiZ6tca&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_m98JMUarqHOqteEJ3eWbpR7fq3v6BAVE-viBwV05GGQ&oe=6A389ABB)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=gsVSA7IbqGcQ7kNvwEP-5un&_nc_oc=AdpxkwJli-NiXi1fV-ixSFlqi5pmHNM_a5Afwk1TI8YT1z5vGA4FeYkqthFx6FB6kElnVTmGIfTKtZ9XYPiZ6tca&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af_m98JMUarqHOqteEJ3eWbpR7fq3v6BAVE-viBwV05GGQ&oe=6A389ABB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwEfNTku&_nc_oc=AdpyTejC43uhr40iKWiqPHvFPBelSzv3T86I9J419LOz8dSMjSzwUr_5o3PueTPdeffZwLJgDl2IVyouxu8YJalP&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-qUzciT2GRvSQBo4EZnT16_FvDmBv9Uf7Bj0qY3xcb_g&oe=6A38B42E)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=K0V3gW02xCkQ7kNvwEfNTku&_nc_oc=AdpyTejC43uhr40iKWiqPHvFPBelSzv3T86I9J419LOz8dSMjSzwUr_5o3PueTPdeffZwLJgDl2IVyouxu8YJalP&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af-qUzciT2GRvSQBo4EZnT16_FvDmBv9Uf7Bj0qY3xcb_g&oe=6A38B42E)](https://www.youtube.com/@aiatmeta)

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

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwFi_027&_nc_oc=AdoD_VI539zTt7tAZA22gJewiGThmzL_FhCn9un2BvXM_jMy8bKiHrsNfhvDh5BulzuTDN-NwypjfhIfBoUqHDlO&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af95m44sOyLj7j3CUd3Pwa9nNOprhoI24llMnsimng24vg&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwFi_027&_nc_oc=AdoD_VI539zTt7tAZA22gJewiGThmzL_FhCn9un2BvXM_jMy8bKiHrsNfhvDh5BulzuTDN-NwypjfhIfBoUqHDlO&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=VWEn8LT-djDITOSqepIx8w&_nc_ss=7b289&oh=00_Af95m44sOyLj7j3CUd3Pwa9nNOprhoI24llMnsimng24vg&oe=6A38A

[truncated]
