# AudioCraft: A simple one-stop shop for audio modeling
Source: https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-ai-audio/
AudioCraft: A simple one-stop shop for audio modeling

[![Meta](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=CU4NmdgzVowQ7kNvwFOqFBr&_nc_oc=AdrlzoHU4S2VE0iNbEGHdgwUhLSLLJmHUS0YhCa5hzM3gxqArwdNGIPeJlyzBHNlpkHW5AFpln4bb1RTcTIBrX8Z&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af-djXdNWeCKz961KglG1QBgLgLHPTkUK7zDXZP_K9GdGQ&oe=6A4269B9)](#)

- [Products](#)
- [AI Research](#)
- [Resources](#)
- [About](#)
- [Get Llama](https://www.llama.com/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=09252025_moment)
- [Try Meta AI](https://applink.meta.ai/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=04082026_moment)

FEATURED

Generative AI

# Open sourcing AudioCraft: Generative AI for audio made simple and available to all

August 2, 2023•

4 minute read

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/364044687_188110547422666_6558067645303623389_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=uyAEJ_oRQL8Q7kNvwFmpXA6&_nc_oc=Adq9i94grF5QC_WihVcr1tuCI6oQDZhkl2oYQW0g7aGT81D5BoYbEERKDla1ia_j5_r8UkVQs70KbXDEyI6qrhOz&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af86aSKNFU_rM3Vq4WIET8Z95AQGMXygbUweTmi_5a99Iw&oe=6A56B25F)

Imagine a professional musician being able to explore new compositions without having to play a single note on an instrument. Or an indie game developer populating virtual worlds with realistic sound effects and ambient noise on a shoestring budget. Or a small business owner adding a soundtrack to their latest Instagram post with ease. That’s the promise of AudioCraft — our simple framework that generates high-quality, realistic audio and music from text-based user inputs after training on raw audio signals as opposed to MIDI or piano rolls.

RECOMMENDED READS

* [Introducing CM3leon, a more efficient, state-of-the-art generative model for text and images](https://ai.meta.com/blog/generative-ai-text-images-cm3leon/)
* [Introducing Voicebox: The first generative AI model for speech to generalize across tasks with state-of-the-art performance](https://ai.meta.com/blog/voicebox-generative-ai-model-speech/)
* [Introducing speech-to-text, text-to-speech, and more for 1,100+ languages](https://ai.meta.com/blog/multilingual-model-speech-recognition/)

AudioCraft consists of three models: [MusicGen](https://huggingface.co/spaces/facebook/MusicGen), [AudioGen](https://felixkreuk.github.io/audiogen/), and [EnCodec](https://ai.meta.com/blog/ai-powered-audio-compression-technique/). MusicGen, which was trained with Meta-owned and specifically licensed music, generates music from text-based user inputs, while AudioGen, which was trained on public sound effects, generates audio from text-based user inputs. Today, we’re excited to release an improved version of our EnCodec decoder, which allows for higher quality music generation with fewer artifacts; our pre-trained AudioGen model, which lets you generate environmental sounds and sound effects like a dog barking, cars honking, or footsteps on a wooden floor; and all of the AudioCraft model weights and code. The models are available for research purposes and to further people’s understanding of the technology. We’re excited to give researchers and practitioners access so they can train their own models with their own datasets for the first time and help advance the state of the art.

## From text to audio with ease

In recent years, generative AI models including language models have made huge strides and shown exceptional abilities: from the [generation of a wide-variety of images and video from text descriptions](https://ai.facebook.com/blog/generative-ai-text-to-video/) exhibiting spatial understanding to text and speech models that perform [machine translation](https://ai.facebook.com/blog/nllb-200-high-quality-machine-translation/) or even text or [speech dialogue agents](https://ai.facebook.com/blog/generating-chit-chat-including-laughs-yawns-ums-and-other-nonverbal-cues-from-raw-audio/). Yet while we’ve seen a lot of excitement around generative AI for images, video, and text, audio has always seemed to lag a bit behind. There’s some work out there, but it’s highly complicated and not very open, so people aren’t able to readily play with it.

  

Generating high-fidelity audio of any kind requires modeling complex signals and patterns at varying scales. Music is arguably the most challenging type of audio to generate because it’s composed of local and long-range patterns, from a suite of notes to a global musical structure with multiple instruments. Generating coherent music with AI has often been addressed through the use of symbolic representations like MIDI or piano rolls. However, these approaches are unable to fully grasp the expressive nuances and stylistic elements found in music. More recent advances leverage [self-supervised audio representation learning](https://ai.facebook.com/blog/hubert-self-supervised-representation-learning-for-speech-recognition-generation-and-compression/) and a number of hierarchical or cascaded models to generate music, feeding the raw audio into a complex system in order to capture long-range structures in the signal while generating quality audio. But we knew that more could be done in this field.

  

The AudioCraft family of models is capable of producing high-quality audio with long-term consistency, and it can be easily interacted with through a natural interface. With AudioCraft, we simplify the overall design of generative models for audio compared to prior work in the field — giving people the full recipe to play with the existing models that Meta has been developing over the past several years while also empowering them to push the limits and develop their own models.

  

AudioCraft works for music and sound generation and compression — all in the same place. Because it’s easy to build on and reuse, people who want to build better sound generators, compression algorithms, or music generators can do it all in the same code base and build on top of what others have done.

  

And while a lot of work went into making the models simple, the team was equally committed to ensuring that AudioCraft could support the state of the art. People can easily extend our models and adapt them to their use cases for research. There are nearly limitless possibilities once you give people access to the models to tune them to their needs. And that’s what we want to do with this family of models: give people the power to extend their work.

## A simple approach to audio generation

Generating audio from raw audio signals is challenging as it requires modeling extremely long sequences. A typical music track of a few minutes sampled at 44.1 kHz (which is the standard quality of music recordings) consists of millions of timesteps. In comparison, text-based generative models like Llama and Llama 2 are fed with text processed as sub-words that represent just a few thousands of timesteps per sample.

  

To address this challenge, we learn discrete audio tokens from the raw signal using the [EnCodec neural audio codec](https://ai.facebook.com/blog/ai-powered-audio-compression-technique/), which gives us a new fixed “vocabulary” for music samples. We can then train autoregressive language models over these discrete audio tokens to generate new tokens and new sounds and music when converting the tokens back to the audio space with EnCodec’s decoder.

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/362278500_245853288291883_2304974600919081225_n.png?_nc_cat=109&ccb=1-7&_nc_sid=f537c7&_nc_ohc=tJwtwTkKXFYQ7kNvwH9Ife8&_nc_oc=AdqGKLNFB-hO98Q0GQxRSe_HkUQvUeFlOLpkF_IAp7CmR3xuJqiPs6bCpy5KeZ9MDMA_3tFgBlakpK97QlClrzYc&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8Tr7-Zq6nvu5gDPm7O1GWxr_7n8Xya7zd_WvKlS3jQuA&oe=6A4265CC)

## Learning audio tokens from the waveform

EnCodec is a lossy neural codec that was trained specifically to compress any kind of audio and reconstruct the original signal with high fidelity. It consists of an autoencoder with a residual vector quantization bottleneck that produces several parallel streams of audio tokens with a fixed vocabulary. The different streams capture different levels of information of the audio waveform, allowing us to reconstruct the audio with high fidelity from all the streams.

## Training audio language models

We then use a single autoregressive language model to recursively model the audio tokens from EnCodec. We introduce a simple approach to leverage the internal structure of the parallel streams of tokens and show that with a single model and elegant token interleaving pattern, our approach efficiently models audio sequences, simultaneously capturing the long-term dependencies in the audio and allowing us to generate high-quality sound.

## Generating audio from text descriptions

Text Prompt: Whistling with wind blowing

Text Prompt: Sirens and a humming engine approach and pass

With AudioGen, we demonstrated that we can train AI models to perform the task of text-to-audio generation. Given a textual description of an acoustic scene, the model can generate the environmental sound corresponding to the description with realistic recording conditions and complex scene context.

Text Prompt: Pop dance track with catchy melodies, tropical percussions, and upbeat rhythms, perfect for the beach

Text Prompt: Earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves

MusicGen is an audio generation model specifically tailored for music generation. Music tracks are more complex than environmental sounds, and generating coherent samples on the long-term structure is especially important when creating novel musical pieces. MusicGen was trained on roughly 400,000 recordings along with text description and metadata, amounting to 20,000 hours of music owned by Meta or licensed specifically for this purpose.

## Building on this research

Our team continues working on the research behind advanced generative AI audio models. As part of this AudioCraft release, we further provide new approaches to push the quality of synthesized audio through a diffusion-based approach for discrete representation decoding. We plan to keep investigating better controllability of generative models for audio, exploring additional conditioning methods, and pushing the ability of models to capture even longer range dependencies. Finally, we will continue investigating the limitations and biases of such models trained on audio.

  

The team is working to improve the current models by boosting their speed and efficiency from a modeling perspective and improving the way we control these models, which will open up new use cases and possibilities.

## Responsibility and transparency as the cornerstones of our research

It’s important to be open about our work so the research community can build on it and continue the important conversations we’re having about how to build AI responsibly. We recognize that the datasets used to train our models lack diversity. In particular, the music dataset used contains a larger portion of western-style music and only contains audio-text pairs with text and metadata written in English. By sharing the code for AudioCraft, we hope other researchers can more easily test new approaches to limit or eliminate potential bias in and misuse of generative models.

## The importance of open source

Responsible innovation can’t happen in isolation. Open sourcing our research and resulting models helps ensure that everyone has equal access.

  

We’re making the models available to the research community at several sizes and sharing AudioGen and MusicGen model cards that detail how we built the models in keeping with our approach to [Responsible AI practices](https://ai.facebook.com/blog/responsible-ai-progress-meta-2022/). Our audio research framework and training code is released under the MIT license to enable the broader community to reproduce and build on top of our work. And through the development of more advanced controls, we hope that such models can become useful to both music amateurs and professionals.

  

Having a solid open source foundation will foster innovation and complement the way we produce and listen to audio and music in the future: think rich bedtime story readings with sound effects and epic music. With even more controls, we think MusicGen can turn into a new type of instrument — just like synthesizers when they first appeared.

  

We see the AudioCraft family of models as tools for musicians’ and sound designers’ professional toolboxes in that they can provide inspiration, help people quickly brainstorm, and iterate on their compositions in new ways.

  

Rather than keeping the work as an impenetrable black box, being open about how we develop these models and ensuring that they’re easy for people to use — whether it’s researchers or the music community as a whole — helps people understand what these models can do, understand what they can’t do, and be empowered to actually use them.

In the future, generative AI could help people vastly improve iteration time by allowing them to get feedback faster during the early prototyping and grayboxing stages — whether they’re a large AAA developer building worlds for the metaverse, a musician (amateur, professional, or otherwise) working on their next composition, or a small or medium-sized business owner looking to up-level their creative assets. AudioCraft is an important step forward in generative AI research. We believe the simple approach we developed to successfully generate robust, coherent, and high-quality audio samples will have a meaningful impact on the development of advanced human-computer interaction models considering auditory and multi-modal interfaces. And we can’t wait to see what people create with it.

[Listen to more samples](https://audiocraft.metademolab.com/)

[Browse AudioCraft code](https://github.com/facebookresearch/audiocraft)

[Read MusicGen paper](https://arxiv.org/abs/2306.05284)

[Read AudioGen paper](https://arxiv.org/abs/2209.15352)

[Read Diffusion decoders paper](https://dl.fbaipublicfiles.com/encodec/Diffusion/paper.pdf)

*This blog post was made possible by the work of: Yossi Adi, Jade Copet, Alexandre Défossez, Itai Gat, David Kant, Felix Kreuk, Rashel Moritz, Tal Remez, Robin San Roman, Gabriel Synnaeve, and Mary Williamson.*

---

Share:

---

Our latest updates delivered to your inbox

[Subscribe](https://ai.facebook.com/subscribe/) to our newsletter to keep up with Meta AI news, events, research breakthroughs, and more.

Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/338318848_238475658638014_6444534044370711549_n.gif?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=KRuNE6RViuYQ7kNvwG-Y1l5&_nc_oc=AdoVTlLGkYsRRlF2sF5qMh44OnGR9jWDw4BFpl8SE4t1sKA0ybvKa0hnQmnZM26fX1fZM1dbOJsDBQ5wKKfOY3Tw&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8UJcmYjpqZp5cAgJvT7OVBmfdDViOKSO7QpMLCw4-6jg&oe=6A56A8E9)

Computer Vision

Introducing Segment Anything: Working toward the first foundation model for image segmentation

April 5, 2023

[Read post](https://ai.meta.com/blog/segment-anything-foundation-model-image-segmentation/)

FEATURED

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/284099254_760295688673506_1047420741523524710_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=JriodrSCKZ4Q7kNvwGagGvN&_nc_oc=Adpc12x7Kx1a3IMLp0wtVCeMsy6eslPiMtssklowL-wRuZEwInZ-xmQwolekLtFPLEiXc0MgRh-1rnmy8b9Crs9z&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af9RaQPL34bTSjkXR7z4NjMrCkHLysGGlouBvr2Ch1WHSA&oe=6A56B576)

Research

MultiRay: Optimizing efficiency for large-scale AI models

November 18, 2022

[Read post](https://ai.meta.com/blog/multiray-large-scale-AI-models/)

FEATURED

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/334793505_583125787173687_542838236294006040_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=oWyjW334zesQ7kNvwFnnqj2&_nc_oc=AdoSvcnWu95Hr1zaMgk_eBNVAjkYChYYttaEZ7NVS6Tucy4LeWCkAR8OprbxAp9Y4sYurAi6tNh9qzuFl_Y4KnyS&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_sDjj2GrgfhT2Ofd0qkEmwxr0utJsQoPf5WQ4_P9DEoA&oe=6A56C904)

ML Applications

MuAViC: The first audio-video speech translation benchmark

March 8, 2023

[Read post](https://ai.meta.com/blog/muavic-audio-visual-speech-translation-benchmark/)

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

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=mOIsi79ov-MQ7kNvwGbYk5i&_nc_oc=Adrea_xK043rSFRMGNJOLshWyMTm-eSZiAONswolCTIQQYyPzNKYEhdeTLjyP730sk44vAGa2wQcH3dSXG1k8frn&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af89IUKze6GePC-eJWjH5r5TIqQLyjrkzzrY0O1xYx2hcg&oe=6A56D378)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_tGS6ESi12FmU5pdGdXrS5oRe9iK8-SFUpR6eKmuO6Og&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_tGS6ESi12FmU5pdGdXrS5oRe9iK8-SFUpR6eKmuO6Og&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_NjR4wClr_BTNL4CIMWqU_Xog_NC3CQMxyBUR5KsN9_A&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_NjR4wClr_BTNL4CIMWqU_Xog_NC3CQMxyBUR5KsN9_A&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_qS-D4s_Vw7uLD0QAG8nS_r3XV1y8AU0LdUR4K1IaRlQ&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_qS-D4s_Vw7uLD0QAG8nS_r3XV1y8AU0LdUR4K1IaRlQ&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8svVoFNisqh1IBlKHb24MAGEIjSIW35bqkyhZxpD4Tyw&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8svVoFNisqh1IBlKHb24MAGEIjSIW35bqkyhZxpD4Tyw&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

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

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_tGS6ESi12FmU5pdGdXrS5oRe9iK8-SFUpR6eKmuO6Og&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_tGS6ESi12FmU5pdGdXrS5oRe9iK8-SFUpR6eKmuO6Og&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_NjR4wClr_BTNL4CIMWqU_Xog_NC3CQMxyBUR5KsN9_A&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_NjR4wClr_BTNL4CIMWqU_Xog_NC3CQMxyBUR5KsN9_A&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_qS-D4s_Vw7uLD0QAG8nS_r3XV1y8AU0LdUR4K1IaRlQ&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_qS-D4s_Vw7uLD0QAG8nS_r3XV1y8AU0LdUR4K1IaRlQ&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8svVoFNisqh1IBlKHb24MAGEIjSIW35bqkyhZxpD4Tyw&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8svVoFNisqh1IBlKHb24MAGEIjSIW35bqkyhZxpD4Tyw&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.facebook.com/policies/)

[Cookies](https://www.facebook.com/policies/cookies/)

Meta © 2026

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_tGS6ESi12FmU5pdGdXrS5oRe9iK8-SFUpR6eKmuO6Og&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_tGS6ESi12FmU5pdGdXrS5oRe9iK8-SFUpR6eKmuO6Og&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_NjR4wClr_BTNL4CIMWqU_Xog_NC3CQMxyBUR5KsN9_A&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_NjR4wClr_BTNL4CIMWqU_Xog_NC3CQMxyBUR5KsN9_A&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_qS-D4s_Vw7uLD0QAG8nS_r3XV1y8AU0LdUR4K1IaRlQ&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af_qS-D4s_Vw7uLD0QAG8nS_r3XV1y8AU0LdUR4K1IaRlQ&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8svVoFNisqh1IBlKHb24MAGEIjSIW35bqkyhZxpD4Tyw&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=Vjcmv2eRXAuMFCnlOFwfLA&_nc_ss=7b289&oh=00_Af8svVoFNisqh1IBlKHb24MAGEIjSIW35bqkyhZxpD4Tyw&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)
