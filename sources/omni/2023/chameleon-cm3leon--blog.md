# Introducing CM3leon, a more efficient, state-of-the-art generative model for text and images
Source: https://ai.meta.com/blog/generative-ai-text-images-cm3leon/
Introducing CM3leon, a more efficient, state-of-the-art generative model for text and images

[![Meta](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=CU4NmdgzVowQ7kNvwFOqFBr&_nc_oc=AdrlzoHU4S2VE0iNbEGHdgwUhLSLLJmHUS0YhCa5hzM3gxqArwdNGIPeJlyzBHNlpkHW5AFpln4bb1RTcTIBrX8Z&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af-yoBke80LBArM-OaSPesQLB4CLFhLZqb2C2qOhSNEQ0Q&oe=6A4269B9)](/)

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

Research

# Introducing CM3leon, a more efficient, state-of-the-art generative model for text and images

July 14, 2023•

7 minute read

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/355350269_735396441693973_7081320402844920765_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=Hp-3T3MoClIQ7kNvwEi_P6H&_nc_oc=Adrj5HNzIF8F6Na6pdsdRcbPQFK-OB2raOdDqR-JmFVZd5RPIjzw5ChQ9hFspgS5nQZnSBf6ornNLR0_mQDPeL4T&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_Yt3uE0il0Hf_a8xQT24nMpB39vCRpi9NX8srp27tJUQ&oe=6A56D4EF)

Interest and research in generative AI models has accelerated in recent months with advancements in natural language processing that lets machines understand and express language, as well as systems that can generate images based on text input. Today, we’re showcasing CM3leon (pronounced like “chameleon”), a single foundation model that does both text-to-image and image-to-text generation.

RECOMMENDED READS

* [Introducing Make-A-Video: An AI system that generates videos from text](https://ai.meta.com/blog/generative-ai-text-to-video/)
* [Introducing Voicebox: The first generative AI model for speech to generalize across tasks with state-of-the-art performance](https://ai.meta.com/blog/voicebox-generative-ai-model-speech/)
* [I-JEPA: The first AI model based on Yann LeCun’s vision for more human-like AI](https://ai.meta.com/blog/yann-lecun-ai-model-i-jepa/)

CM3leon is the first multimodal model trained with a recipe adapted from text-only language models, including a large-scale retrieval-augmented pre-training stage and a second multitask supervised fine-tuning (SFT) stage. This recipe is simple, produces a strong model, and also shows that tokenizer-based transformers can be trained as efficiently as existing generative diffusion-based models. CM3leon achieves state-of-the-art performance for text-to-image generation, despite being trained with five times less compute than previous transformer-based methods. CM3leon has the versatility and effectiveness of autoregressive models, while maintaining low training costs and inference efficiency. It is a causal masked mixed-modal (CM3) model because it can generate sequences of text and images conditioned on arbitrary sequences of other image and text content. This greatly expands the functionality of previous models that were either only text-to-image or only image-to-text.

Although text-only generative models are commonly multitask instruction-tuned on a wide range of different tasks to improve their ability to follow instruction prompts, image generation models are instead typically specialized for particular tasks. We apply large-scale multitask instruction tuning to CM3leon for both image and text generation, and show that it significantly improves performance on tasks such as image caption generation, visual question answering, text-based editing, and conditional image generation. This provides another strong example of how the scaling recipes developed for text-only models generalize directly to our tokenization-based image generation models.

When comparing performance on the most widely used image generation benchmark (zero-shot MS-COCO), CM3Leon achieves an FID (Fréchet Inception Distance) score of 4.88, establishing a new state of the art in text-to-image generation and outperforming Google’s text-to-image model, Parti. This achievement underscores the potential of retrieval augmentation and highlights the impact of scaling strategies on the performance of autoregressive models. CM3Leon also shows an impressive ability to generate complex compositional objects, such as the potted cactus with sunglasses and a hat in the examples below. CM3leon performs well across a variety of vision-language tasks, including visual question answering and long-form captioning. Even with training on a dataset comprised of only three billion text tokens, CM3Leon's zero-shot performance compares favorably against larger models trained on more extensive datasets.

## How CM3leon performs across tasks

With CM3leon’s capabilities, image generation tools can produce more coherent imagery that better follows the input prompts. For example, many image generation models struggle with the capacity to recover global shapes and local details. CM3leon performs strongly in this area. Here’s a look at CM3leon’s capabilities across a variety of tasks — all performed with a single model:

**Text-guided image generation and editing**

Image generation can be challenging when it comes to complex objects or when the prompt includes many constraints that must all be included in the output. Text-guided image editing (e.g. “change the color of the sky to bright blue”) is challenging because it requires the model to simultaneously understand both textual instructions and visual content. CM3leon excels in all of the cases, as seen in the examples below.

**Text-to-image**

Given prompt text with potentially highly compositional structure, generate a coherent image that follows the prompt. For example, the following four images were created for the prompts: (1) A small cactus wearing a straw hat and neon sunglasses in the Sahara desert. (2) A close-up photo of a human hand, hand model. High quality. (3) A raccoon main character in an Anime preparing for an epic battle with a samurai sword. Battle stance. Fantasy, Illustration. (4) A stop sign in a Fantasy style with the text “1991.”

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/358675736_262727669790925_3190473684047147716_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=ycWeY834r6oQ7kNvwGu7qw0&_nc_oc=AdoO6jjv56gw_geVml4nnRuGuswwIxck8tdhZvbBCSCTSlS9FJPUH1LnnZPgZWG1xQA4arIku7pZNfWLQZl370x0&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_mAf7_1PIWsHmAEXnDkGOOIXA0IOwR2Fwb3E6JGLjvAQ&oe=6A56ACF6)

**Text-guided image editing**

Given an image and a text prompt, edit the image according to the instructions in the text. Because of the generality of the CM3leon models, this was achieved with the same model as all of the other tasks above and below, unlike previous models such as InstructPix2Pix which are tuned only for text-guided image editing.

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/358713848_660084255621228_746245581913776369_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=tyfeWGiTGnsQ7kNvwE9lejT&_nc_oc=AdrkL5E8FgwrSxdozJ_9OHEPSIrlYULA9gj9cdHFP3Jzbh2mQXvO-VFdwBUO6nNTfAtexsr9pwxxyED1A0YzZlrk&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_hZN6dWYqAbd63k8x0LcdYMyrKiub-7DArI5jPqdt1Jw&oe=6A56A46E)

**Text tasks**

The CM3leon model can also follow a range of different prompts to generate short or long captions and answer questions about an image.

For example, imagine a dog carrying a stick.

**Prompt Question:** What is the dog carrying?

**Model Generation:** Stick

**Prompt:** Describe the given image in very fine detail.

**Model Generation:** In this image, there is a dog holding a stick in its mouth. There is grass on the surface. In the background of the image, there are trees.

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/357473213_1417353592162138_1086817289622082602_n.png?_nc_cat=102&ccb=1-7&_nc_sid=e280be&_nc_ohc=oqngY-oFIM4Q7kNvwHEb8jf&_nc_oc=Ado7KcSpmVi4oewMCVlbjYxY0wz_U3Kn8iuTs39nKSOHw44GX6PRyYaDRd_g6htJQscDLGFNUjkn1upIp5ZvvTkN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af-xIqBXBMJtPqbzwhZM2kOAY4d1dtB6TzYeu9Y8gk2EJw&oe=6A56A7A6)

We empirically evaluated our instruction-tuned models on various image captioning generation and visual question answering tasks and compared them with previous state-of-the-art benchmarks. Even though CM3leon models saw significantly less text data (~3B tokens) compared to Flamingo (100B) and OpenFlamingo (40B), they match the zero-shot performance levels of OpenFlamingo on MS-COCO captioning and VQA2 question answering and even beat Flamingo by nearly 10 points on the VizWiz task.

**Structure-guided image editing**

Structure-guided image editing involves understanding and interpreting not only textual instructions but also structural or layout information that’s provided as input. This enables CM3leon models to create visually coherent and contextually appropriate edits to an image while adhering to the given structure or layout guidelines.

**Object-to-image**

Given a text description of the bounding box segmentation of the image, generate an image.

![](https://scontent-lax7-1.xx.fbcdn.net/v/t39.2365-6/359198671_298094419267090_6070744248933373628_n.png?_nc_cat=105&ccb=1-7&_nc_sid=e280be&_nc_ohc=KZ-dikloxuwQ7kNvwHHBagN&_nc_oc=AdqGQX1oQW3P9dQj393NnfgRaVi3vCu-rvW2R5b17MA3ERAdiD0C_1aDdQrgspzqfmFYA37M-XGmvFWpCsYSGq1h&_nc_zt=14&_nc_ht=scontent-lax7-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af9GsleSzJUSGrjENGGOZVFW8CMJncrxSk-69BwB4QfxEA&oe=6A56D351)

**Segmentation-to-image**

Given an image containing only the segmentation (with no text classes), generate an image. The input here denotes the image from which we extract the segmentation.

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/358696519_301734465641511_2309463697092042055_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=AHyaVq5-0pgQ7kNvwFFImhx&_nc_oc=AdoLbZQi381xl9PPSjZq4AeSE_-A9f_uzMysYqFKR1RkCZkimvkdr-t1hMrBb9TwxcYmuNu9XxQdkyorrnZjDv_5&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_DcHV-mzrj3jhtTY-MYeyKn-lh2g5OPcljSELWo-DwQA&oe=6A56D49C)

## Super-resolution results

All of the generated images above show raw outputs from the CM3leon model. However, a common trick for image generation is to add a separately trained super-resolution stage to produce higher-resolution images from the original model outputs. This works very well with CM3leon too, as we show in the examples below for the text-to-image generation task.

Four example images for each of the prompts: (1) A steaming cup of coffee with mountains in the background. Resting during road trip. (2) Beautiful, majestic road during sunset. Aesthetic. (3) Small circular island in the middle of a lake. Forests surrounding the lake. High Contrast.

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/358148386_6665485166824360_298298629349987547_n.png?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=uFxA-leHn3kQ7kNvwGVK1ex&_nc_oc=AdoBjDc_0WwP8JGaCSCcueMz_wDDeEMSFSo5SVSjM168tQU-DjFBRQoSxEOIKnkbTvDkzjm4DiNl-NtFDwDjStIk&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_tqEUllVnce6KRHE8G3SknsbonlC_B4CI7_9Z0G2skIQ&oe=6A56B9B5)

More examples for the prompts: (1) Turtle swimming underwater. Aesthetic. Fantasy. (2) Elephant swimming underwater. Aesthetic. Fantasy. (3) Flock of sheep. Aesthetic. Fantasy.

![](https://scontent-lax7-1.xx.fbcdn.net/v/t39.2365-6/357444665_289991886771406_461385829756514603_n.png?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=f9N7BG7k9AgQ7kNvwGrc2i9&_nc_oc=AdpvRs9411UDmwx_faFvnegQ2CktkTNTsf57fJaeA4GcugTYu2mgzsQgAhrRmC60jc-XRTgTr8icgQqsmj0iMOl4&_nc_zt=14&_nc_ht=scontent-lax7-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af9t8Xpw0oI6_KJnJYpgSEngXa0gUAv4HEwy_c_Qqotk1Q&oe=6A56D821)

## How we built CM3leon

**Architecture**

CM3Leon's architecture uses a decoder-only transformer akin to well-established text-based models. However, what sets CM3Leon apart is its ability to input and generate both text and images. This empowers CM3Leon to successfully handle the variety of tasks we shared above.

**Training**

CM3leon’s training retrieval augmented, following our [recent work](https://arxiv.org/abs/2211.12561), greatly improving efficiency and controllability of the resulting model. Finally, as described above, we performed instruction fine-tuning on a wide range of different image and text generation tasks.

As the AI industry continues to evolve, generative models like CM3leon are becoming increasingly sophisticated. These models learn the relationship between visuals and text by training on millions of example images, but they can also reflect any biases present in the training data. While the industry is still in its early stages of understanding and addressing these challenges, we believe that transparency will be key to accelerating progress.

As such, and as described in our paper, we’ve trained CM3leon using a licensed dataset. This demonstrates that strong performance is possible with a very different data distribution from what all previous models used. By making our work transparent, we hope to encourage collaboration and innovation in the field of generative AI. We believe that by working together, we can create models that are not only more accurate, but also more fair and equitable for everyone.

## Paving the way for multimodal language models

With the goal of creating high-quality generative models, we believe CM3leon’s strong performance across a variety of tasks is a step toward higher-fidelity image generation and understanding. Models like CM3leon could ultimately help boost creativity and better applications in the metaverse. We look forward to exploring the boundaries of multimodal language models and releasing more models in the future.

[Read the research paper](https://ai.facebook.com/research/publications/scaling-autoregressive-multi-modal-models-pretraining-and-instruction-tuning/)

---

Written by:

Armen Aghajanyan

Research Scientist

Sony Theakanath

Director, Product Management

Lili Yu

AI Research Scientist

Luke Zettlemoyer

Research Director, FAIR

Share:

---

Our latest updates delivered to your inbox

[Subscribe](https://ai.facebook.com/subscribe/) to our newsletter to keep up with Meta AI news, events, research breakthroughs, and more.

Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/357441725_598359505742319_1895335334851154209_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=Tp4o7ieV4soQ7kNvwE4A9SH&_nc_oc=AdraWQZ1Lubkg8GO64cl_bVs0t90fpDA8FnK8wi5L3axIXYFmsZEpW2n9-FPfAdo8E9m8-3GzNoBTiAy1EzdF8oA&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8wc5KAd8yurgtzjDBHSpfUKXRiAZ4tbPwwZOHkIsWncg&oe=6A56CC3E)

Research

Improving fairness and robustness in speech recognition

July 13, 2023

[Read post](https://ai.meta.com/blog/improving-fairness-and-robustness-in-speech-recognition/)

FEATURED

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/356891361_305782345127740_288559619232908129_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=SfZVYXjOWKUQ7kNvwFnXaNg&_nc_oc=Adpy6mFlL6o40OdPHbLhFCkldCiqkaXxbcEygXNKzxtQjVKrMU82tApkoKdgh55azqZ8UK7kzioVL36_woOQjOPb&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_7w51UAei6ZyvJ1n-Tb28ggsrqJ_EfX0_v_SfryoCQLg&oe=6A56C0DD)

ML Applications

Introducing 22 system cards that explain how AI powers experiences on Facebook and Instagram

June 29, 2023

[Read post](https://ai.meta.com/blog/how-ai-powers-experiences-facebook-instagram-system-cards/)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/346873766_274638798275632_8494050904807553947_n.png?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=GJ8dK84kxt8Q7kNvwERvGuD&_nc_oc=Adrd0Y_00HrgxuK8wLWQRFeuYp9ze8H29-AcrPpPFzIYTPzE3PYd9-0Y51LTDgXltkFW9Lf3YiHRNPoJbYzA-cDm&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8hNuqFZZ20PIL_zyJRt-kI-tcbvTWs7ZiPTx9ddHSAcA&oe=6A56D4F6)

Research

Introducing Voicebox: The first generative AI model for speech to generalize across tasks with state-of-the-art performance

June 16, 2023

[Read post](https://ai.meta.com/blog/voicebox-generative-ai-model-speech/)

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

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=mOIsi79ov-MQ7kNvwGbYk5i&_nc_oc=Adrea_xK043rSFRMGNJOLshWyMTm-eSZiAONswolCTIQQYyPzNKYEhdeTLjyP730sk44vAGa2wQcH3dSXG1k8frn&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af9EJL4MwVzqa8uKarOTpFO7qV4YneoePj8awatwAeui_w&oe=6A56D378)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=ghJpI4Q0-7UQ7kNvwERLh2m&_nc_oc=AdraEHj9S1X9jmSN7luBzLiDlA4GA9o_0oLBcacyt96UAhyj0W2L3PZ3Sdk9yI9XGq-JDgj7UblPu19ZzpMBf0z7&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af97ADcbYhwHJgF6U95HeukzbrKxEGXn9h1Y1KDN4CeFsg&oe=6A56D84F)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_HDH7--Y9fuMh7jFmIS3trK7QguTYuySs1fmXI0-u5UA&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_HDH7--Y9fuMh7jFmIS3trK7QguTYuySs1fmXI0-u5UA&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_64-bJmDNzx7i4DB9hT6THWWboh-B2O7aTOT2SBvfJ_g&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_64-bJmDNzx7i4DB9hT6THWWboh-B2O7aTOT2SBvfJ_g&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8rsRy_YfR3cVMiFTuIvny-cVMW-uy29tBvtVdp_R_qLg&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8rsRy_YfR3cVMiFTuIvny-cVMW-uy29tBvtVdp_R_qLg&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af95TyVJGSqrVoZnJhLoONoUl1PDzX1mZOmZsGPztCqs5g&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af95TyVJGSqrVoZnJhLoONoUl1PDzX1mZOmZsGPztCqs5g&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

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

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_HDH7--Y9fuMh7jFmIS3trK7QguTYuySs1fmXI0-u5UA&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_HDH7--Y9fuMh7jFmIS3trK7QguTYuySs1fmXI0-u5UA&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_64-bJmDNzx7i4DB9hT6THWWboh-B2O7aTOT2SBvfJ_g&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_64-bJmDNzx7i4DB9hT6THWWboh-B2O7aTOT2SBvfJ_g&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8rsRy_YfR3cVMiFTuIvny-cVMW-uy29tBvtVdp_R_qLg&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8rsRy_YfR3cVMiFTuIvny-cVMW-uy29tBvtVdp_R_qLg&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af95TyVJGSqrVoZnJhLoONoUl1PDzX1mZOmZsGPztCqs5g&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af95TyVJGSqrVoZnJhLoONoUl1PDzX1mZOmZsGPztCqs5g&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.facebook.com/policies/)

[Cookies](https://www.facebook.com/policies/cookies/)

Meta © 2026

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_HDH7--Y9fuMh7jFmIS3trK7QguTYuySs1fmXI0-u5UA&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_HDH7--Y9fuMh7jFmIS3trK7QguTYuySs1fmXI0-u5UA&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_64-bJmDNzx7i4DB9hT6THWWboh-B2O7aTOT2SBvfJ_g&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af_64-bJmDNzx7i4DB9hT6THWWboh-B2O7aTOT2SBvfJ_g&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8rsRy_YfR3cVMiFTuIvny-cVMW-uy29tBvtVdp_R_qLg&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af8rsRy_YfR3cVMiFTuIvny-cVMW-uy29tBvtVdp_R_qLg&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af95TyVJGSqrVoZnJhLoONoUl1PDzX1mZOmZsGPztCqs5g&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=lsl83Jz6e6nb6leugxeTIA&_nc_ss=7b289&oh=00_Af95TyVJGSqrVoZnJhLoONoUl1PDzX1mZOmZsGPztCqs5g&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)
