# Emu: Enhancing Image Generation Models Using Photogenic Needles in a Haystack | Research - AI at Meta
Source: https://ai.meta.com/research/publications/emu-enhancing-image-generation-models-using-photogenic-needles-in-a-haystack/
Emu: Enhancing Image Generation Models Using Photogenic Needles in a Haystack | Research - AI at Meta

[![Meta](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=CU4NmdgzVowQ7kNvwHRwkzs&_nc_oc=AdqC8xIBgDpNZ_vypxZPIjejOPnqRP8_1ybSVpz4X2BUqFY-3cq583HoIcEa1bQODR0&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af8veaAJ0YMqRfzPQ_16eSDyUISw5BtHi3_QPiaMZgw9oA&oe=6A4269B9)](/)

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

#### COMPUTER VISION

# Emu: Enhancing Image Generation Models Using Photogenic Needles in a Haystack

September 27, 2023

## Abstract

Training text-to-image models with web scale image-text pairs enables the generation of a wide range of visual concepts from text. However, these pre-trained models often face challenges when it comes to generating highly aesthetic images. This creates the need for aesthetic alignment post pre-training. In this paper, we propose quality-tuning to effectively guide a pre-trained model to exclusively generate highly visually appealing images, while maintaining generality across visual concepts. Our key insight is that supervised fine-tuning with a set of surprisingly small but extremely visually appealing images can significantly improve the generation quality. We pre-train a latent diffusion model on 1.1 billion image-text pairs and fine-tune it with only a few thousand carefully selected high-quality images. The resulting model, Emu, achieves a win rate of 82.9% compared with its pre-trained only counterpart. Compared to the state-of-the-art SDXLv1.0, Emu is preferred 68.4% and 71.3% of the time on visual appeal on the standard PartiPrompts and our Open User Input benchmark based on the real-world usage of text-to-image models. In addition, we show that quality-tuning is a generic approach that is also effective for other architectures, including pixel diffusion and masked generative transformer models.

[Download the Paper](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/10000000_737030324488003_486930325709036258_n.pdf?_nc_cat=102&ccb=1-7&_nc_sid=3c67a6&_nc_ohc=LpEvYar3rFkQ7kNvwGk8Chb&_nc_oc=AdoD68we8rPaHp-j412_B69l2m_LZttnDEggXkZgJLwtAVJS6J-_C6dAIbz0rjvpWpQ&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9b-YTV4Xg8U-_0RdiaShrdYAWtL4-TCb1_YDz09dduHg&oe=6A426BEA)

#### 作者

Written by

Xiaoliang Dai

[Ji Hou](/people/955744385546411/ji-hou/)

Kevin Chih-Yao Ma

Sam Tsai

[Jialiang Wang](/people/673461174828840/jialiang-wang/)

[Rui Wang](/people/7558226144216020/rui-wang/)

Peizhao Zhang

Simon Vandenhende

Xiaofang Wang

[Abhimanyu Dubey](/people/1401136157273652/abhimanyu-dubey/)

Matthew Yu

Abhishek Kadian

[Filip Radenovic](/people/1088833472330914/filip-radenovic/)

[Dhruv Mahajan](/people/921856686298087/dhruv-mahajan/)

Kunpeng Li

Yue (R) Zhao

Vladan Petrovic

[Mitesh Kumar Singh](/people/1151432666279848/mitesh-kumar-singh/)

Simran Motwani

Yiwen Song

Yi Wen

[Roshan Sumbaly](/people/1149407329757624/roshan-sumbaly/)

[Vignesh Ramanathan](/people/773456394368212/vignesh-ramanathan/)

Zijian He

Peter Vajda

[Devi Parikh](/people/716474937299789/devi-parikh/)

Publisher

Meta

Research Topics

[Computer Vision](/research/computer-vision/)

### Related Publications

May 26, 2026

#### HUMAN & MACHINE INTELLIGENCE

#### THEORY

#### Misalignment Between Backpropagation and the Hierarchy of Brain Responses to Images

Backpropagation is the core learning mechanism underlying deep learning.
However, whether and how this algorithm is implemented in the brain remains highly debated.
In particular, while forward activations of pretrained models reliably map onto the cortical hierarchy of visual processing, it is unknown whether backpropagated gradients exhibit a similar correspondence.
Here, we address this question using functional magnetic resonance imaging (fMRI) and magnetoencephalography (MEG) recordings of human brain responses to natural images. For this, we extend standard encoding analyses of forward activations to map backpropagated gradients onto neural data. Focusing on a recent self-supervised vision model (DINOv3) and reproducing results on eight vision models, we find that backpropagated gradients can reliably predict both fMRI and MEG signals, specifically in higher-level visual cortex and for later latencies. However, the spatial and temporal organization of these backpropagated gradients in the brain diverges from the patterns expected under a biologically plausible backpropagation mechanism: specifically, both the order in which gradients
are computed and their spatial organization diverge from the temporal and spatial hierarchies of the human brain. Together, these results suggest that, although deep networks and the brain may share similar representational content, they likely rely on fundamentally different mechanisms to learn those representations.

Josephine Raugel, Max Seitzer, Marc Szafraniec, Huy V. Vo, Jérémy Rapin, Patrick Labatut, Piotr Bojanowski, Valentin Wyart, Jean Remi King

May 26, 2026

[Read the Paper](/research/publications/misalignment-between-backpropagation-and-the-hierarchy-of-brain-responses-to-images/)

May 20, 2026

#### HUMAN & MACHINE INTELLIGENCE

#### RESEARCH

#### EgoBabyVLM: Benchmarking Cross-Modal Learning from Naturalistic Egocentric Video Data

Children acquire language grounding with remarkable robustness from limited visuo-linguistic input in ways that surpass today's best large multimodal models. Recent research suggests current vision-language models (VLMs) trained on curated web data fail to generalize to the sparse, weakly-aligned egocentric streams produced by wearable devices, embodied agents, and infant head-cams -- and no fixed evaluation pipeline exists for measuring progress on this regime. We train VLMs on datasets with varying degrees of semantic alignment between visual and linguistic inputs, including naturalistic infant and adult egocentric videos, and evaluate them with a comprehensive suite spanning multimodal language grounding and unimodal vision and language tasks. At the core of this suite is Machine-DevBench, a corpus-grounded benchmark of lexical and grammatical competence, automatically generated from the model's training vocabulary across logarithmic frequency bins to eliminate the train/eval mismatch and low statistical power of prior developmental benchmarks. Our results show that current VLM paradigms hinge on the tight semantic alignment of curated data and fail to exploit the weakly-aligned signal that dominates naturalistic egocentric input -- the very regime in which humans thrive. To motivate progress, we introduce the EgoBabyVLM Challenge to drive the development of models capable of grounded language learning from the kind of naturalistic data that human infants experience.

[Dongyan Lin](/people/2023351861723323/dongyan-lin/), Phillip Rust, Angel Villar Corrales, Alvin W. M. Tan, Mahi Luthra, Charles-Eric Saint-James, Rashel Moritz, Sheila Krogh-Jespersen, Vanessa Stark, Surya Parimi, Jiayi Shen, Youssef Benchekroun, Yosuke Higuchi, Martin Gleize, Tom Fizycki, Nicolas Hamilakis, Manel Khentout, Sho Tsuji, Balázs Kégl, [Juan Pino](/people/776668760684735/juan-pino/), Michael C. Frank, Emmanuel Dupoux

May 20, 2026

[Read the Paper](/research/publications/egobabyvlm-benchmarking-cross-modal-learning-from-naturalistic-egocentric-video-data/)

May 12, 2026

#### HUMAN & MACHINE INTELLIGENCE

#### RESEARCH

#### NeuralSet: A High-Performing Python Package for Neuro-AI

Artificial intelligence (AI) is increasingly central to understanding how the brain processes information. However, the integration of neuroscience and modern AI is bottlenecked by a fragmented software ecosystem. Current tools are siloed by recording modality and optimized for small-scale, in-memory workflows, limiting the use of massive, naturalistic datasets. Here, we introduce NeuralSet, a Python framework that efficiently unifies the processing of diverse neural recordings (including fMRI, M/EEG, and spikes) and complex experimental stimuli (such as text, audio, and video). By decoupling experimental metadata from lazy, memory-efficient data extraction, NeuralSet harmonizes standard neuroscientific preprocessing pipelines with pretrained deep learning embeddings. This approach provides a single PyTorch-ready interface that scales seamlessly from local prototyping to high-performance cluster execution. By eliminating manual data wrangling and ensuring full computational provenance, NeuralSet establishes a scalable, unified infrastructure for the next generation of neuro-AI research.

Jean Remi King, Corentin Bel, Linnea Evanson, Julien Gadonneix, Sophia Houhamdi, Jarod Levy, Josephine Raugel, Andrea Santos Revilla, Mingfang (Lucy) Zhang, Julie Bonnaire, Charlotte Caucheteux, Alexandre Défossez, Théo Desbordes, Pablo Diego-Simón, Shubh Khanna, Juliette Millet, Pierre Orhan, Saarang Panchavati, Antoine Ratouchniak, Alexis Thual, Teon Brooks, Katelyn Begany, Yohann Benchetrit, Marlene Careil, Hubert Jacob Banville, [Stéphane d'Ascoli](/people/7732427943457653/stephane-d-ascoli/), Simon Dahan, Jérémy Rapin

May 12, 2026

[Read the Paper](/research/publications/neuralset-a-high-performing-python-package-for-neuro-ai/)

April 14, 2026

#### COMPUTER VISION

#### ML APPLICATIONS

#### TransText: Transparency Aware Image-to-Video Typography Animation

We introduce the first method, to the best of our knowledge, for adapting image-to-video models to layer-aware text (glyph) animation, a capability critical for practical dynamic visual design. Existing approaches predominantly handle the transparency-encoding (alpha channel) as an extra latent dimension appended to the RGB space, necessitating the reconstruction of the underlying RGB-centric variational autoencoder (VAE). However, given the scarcity of high-quality transparent glyph data, retraining the VAE is computationally expensive and may erode the robust semantic priors learned from massive RGB corpora, potentially leading to latent pattern mixing. To mitigate these limitations, we propose TransText, a framework based on a novel Alpha-as-RGB paradigm to jointly model appearance and transparency without modifying the pre-trained generative manifold. TransText embeds the alpha channel as an RGB-compatible visual signal through latent spatial concatenation, explicitly ensuring strict cross-modal (RGB-and-Alpha) consistency while preventing feature entanglement. Our experiments demonstrate that TransText significantly outperforms baselines, generating coherent, high-fidelity transparent animations with diverse, fine-grained effects.

Fei Zhang, Zijian Zhou, Bohao Tang, Sen He, Hang Li (BizAI), Zhe Wang, Soubhik Sanyal, Pengfei Liu, Viktar Atliha, Tao Xiang, [Frost Xu](/people/1217216222966775/mengmeng-xu-frost/), Semih Gunel

April 14, 2026

[Read the Paper](/research/publications/transtext-transparency-aware-image-to-video-typography-animation/)

[See All Papers](/global_search/?content_types%5B0%5D=publication&page=1)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/90971213_248000486247635_8189447952712859648_n.jpg?_nc_cat=104&ccb=1-7&_nc_sid=e280be&_nc_ohc=DRBPDi8EuxgQ7kNvwFDJbof&_nc_oc=AdrKjoH_X0BE1xrww1J2xL7AVGG0i8morUv6wfUdYe4pC8aZeUAH9_2IGSfULMUOJS4&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af8jFinDNJVpFyCJ1QFdXNsK5J2p_vkmKEAz9sGF3v7B6g&oe=6A56CD97)

## Help Us Pioneer The Future of AI

##### We share our open source frameworks, tools, libraries, and models for everything from research exploration to large-scale production deployment.

[Join our Team](/join-us/)

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

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=mOIsi79ov-MQ7kNvwG1Qt7b&_nc_oc=AdoKDZQSKRlQjqd428sEqiMORxgcvlJ8j_47XHI6kI4uuF94z7B3lxtCHB1avtlJbNQ&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af8uQyGXM_D8l6Yjpwkah3JgPhhAR0U8JpDajrXgY9E61g&oe=6A56D378)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=ghJpI4Q0-7UQ7kNvwEwdkD1&_nc_oc=AdpCsRLGaXPmdGYJg6L8Ljz9R3OFGU8sPG9WbtPQZmIuCoG6lKhz37v5QC2rwyqAuYs&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-jl3RRtzxc_42L-lhBUIrI8PckIUvhgQoXV80Q-yJb3Q&oe=6A56D84F)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwHnUYbW&_nc_oc=AdqaUEremMnM5u-YsAwWoHDDefAzzyIRsEOWZkD8LzQQQy5oGitxNpchfTT3skg7KlY&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-6z9cbTfimNZylkAOKuNxyhk6NA7e-YpzOIwMFflgQkw&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwHnUYbW&_nc_oc=AdqaUEremMnM5u-YsAwWoHDDefAzzyIRsEOWZkD8LzQQQy5oGitxNpchfTT3skg7KlY&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-6z9cbTfimNZylkAOKuNxyhk6NA7e-YpzOIwMFflgQkw&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwEolxP1&_nc_oc=AdoIMWMUrRMGqy9Wl_H16Mgasibb6DIF4bkdKCQJ2VgjUrmBycg8V92bXj3IBwg50kM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9AJU70XDNLJYEtnn9KlbkE0tOGb3TxRsvo7k6Jpqq0Mg&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwEolxP1&_nc_oc=AdoIMWMUrRMGqy9Wl_H16Mgasibb6DIF4bkdKCQJ2VgjUrmBycg8V92bXj3IBwg50kM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9AJU70XDNLJYEtnn9KlbkE0tOGb3TxRsvo7k6Jpqq0Mg&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwHI8gkA&_nc_oc=AdrGqxHTfmW76ACWg6i-o_p_umawgejIF292swan4wmhWbQpgh_RFxGDTtRmAgupVzg&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af_svXzdSHHSiu9hj_1M1SXA-iZhGkdS3KyRYO-mh9YCYQ&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwHI8gkA&_nc_oc=AdrGqxHTfmW76ACWg6i-o_p_umawgejIF292swan4wmhWbQpgh_RFxGDTtRmAgupVzg&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af_svXzdSHHSiu9hj_1M1SXA-iZhGkdS3KyRYO-mh9YCYQ&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwGWadob&_nc_oc=AdpDGMb4EnxTIr2iNL4Fx-m7OKCf5qLPfUWUGaOtMpOP9KV_xawKh9mlOGvolHYbsuI&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-KZM2OStHHM8w1bLfOBVxrhR9IqIRUKpzbmwms35MXdA&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwGWadob&_nc_oc=AdpDGMb4EnxTIr2iNL4Fx-m7OKCf5qLPfUWUGaOtMpOP9KV_xawKh9mlOGvolHYbsuI&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-KZM2OStHHM8w1bLfOBVxrhR9IqIRUKpzbmwms35MXdA&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

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

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwHnUYbW&_nc_oc=AdqaUEremMnM5u-YsAwWoHDDefAzzyIRsEOWZkD8LzQQQy5oGitxNpchfTT3skg7KlY&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-6z9cbTfimNZylkAOKuNxyhk6NA7e-YpzOIwMFflgQkw&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwHnUYbW&_nc_oc=AdqaUEremMnM5u-YsAwWoHDDefAzzyIRsEOWZkD8LzQQQy5oGitxNpchfTT3skg7KlY&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-6z9cbTfimNZylkAOKuNxyhk6NA7e-YpzOIwMFflgQkw&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwEolxP1&_nc_oc=AdoIMWMUrRMGqy9Wl_H16Mgasibb6DIF4bkdKCQJ2VgjUrmBycg8V92bXj3IBwg50kM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9AJU70XDNLJYEtnn9KlbkE0tOGb3TxRsvo7k6Jpqq0Mg&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwEolxP1&_nc_oc=AdoIMWMUrRMGqy9Wl_H16Mgasibb6DIF4bkdKCQJ2VgjUrmBycg8V92bXj3IBwg50kM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9AJU70XDNLJYEtnn9KlbkE0tOGb3TxRsvo7k6Jpqq0Mg&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwHI8gkA&_nc_oc=AdrGqxHTfmW76ACWg6i-o_p_umawgejIF292swan4wmhWbQpgh_RFxGDTtRmAgupVzg&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af_svXzdSHHSiu9hj_1M1SXA-iZhGkdS3KyRYO-mh9YCYQ&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwHI8gkA&_nc_oc=AdrGqxHTfmW76ACWg6i-o_p_umawgejIF292swan4wmhWbQpgh_RFxGDTtRmAgupVzg&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af_svXzdSHHSiu9hj_1M1SXA-iZhGkdS3KyRYO-mh9YCYQ&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwGWadob&_nc_oc=AdpDGMb4EnxTIr2iNL4Fx-m7OKCf5qLPfUWUGaOtMpOP9KV_xawKh9mlOGvolHYbsuI&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-KZM2OStHHM8w1bLfOBVxrhR9IqIRUKpzbmwms35MXdA&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwGWadob&_nc_oc=AdpDGMb4EnxTIr2iNL4Fx-m7OKCf5qLPfUWUGaOtMpOP9KV_xawKh9mlOGvolHYbsuI&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-KZM2OStHHM8w1bLfOBVxrhR9IqIRUKpzbmwms35MXdA&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.facebook.com/policies/)

[Cookies](https://www.facebook.com/policies/cookies/)

Meta © 2026

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwHnUYbW&_nc_oc=AdqaUEremMnM5u-YsAwWoHDDefAzzyIRsEOWZkD8LzQQQy5oGitxNpchfTT3skg7KlY&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-6z9cbTfimNZylkAOKuNxyhk6NA7e-YpzOIwMFflgQkw&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwHnUYbW&_nc_oc=AdqaUEremMnM5u-YsAwWoHDDefAzzyIRsEOWZkD8LzQQQy5oGitxNpchfTT3skg7KlY&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-6z9cbTfimNZylkAOKuNxyhk6NA7e-YpzOIwMFflgQkw&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwEolxP1&_nc_oc=AdoIMWMUrRMGqy9Wl_H16Mgasibb6DIF4bkdKCQJ2VgjUrmBycg8V92bXj3IBwg50kM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9AJU70XDNLJYEtnn9KlbkE0tOGb3TxRsvo7k6Jpqq0Mg&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwEolxP1&_nc_oc=AdoIMWMUrRMGqy9Wl_H16Mgasibb6DIF4bkdKCQJ2VgjUrmBycg8V92bXj3IBwg50kM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af9AJU70XDNLJYEtnn9KlbkE0tOGb3TxRsvo7k6Jpqq0Mg&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwHI8gkA&_nc_oc=AdrGqxHTfmW76ACWg6i-o_p_umawgejIF292swan4wmhWbQpgh_RFxGDTtRmAgupVzg&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af_svXzdSHHSiu9hj_1M1SXA-iZhGkdS3KyRYO-mh9YCYQ&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwHI8gkA&_nc_oc=AdrGqxHTfmW76ACWg6i-o_p_umawgejIF292swan4wmhWbQpgh_RFxGDTtRmAgupVzg&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af_svXzdSHHSiu9hj_1M1SXA-iZhGkdS3KyRYO-mh9YCYQ&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwGWadob&_nc_oc=AdpDGMb4EnxTIr2iNL4Fx-m7OKCf5qLPfUWUGaOtMpOP9KV_xawKh9mlOGvolHYbsuI&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-KZM2OStHHM8w1bLfOBVxrhR9IqIRUKpzbmwms35MXdA&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwGWadob&_nc_oc=AdpDGMb4EnxTIr2iNL4Fx-m7OKCf5qLPfUWUGaOtMpOP9KV_xawKh9mlOGvolHYbsuI&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=GMf1h-bSw5nut1tUt0j6Sg&_nc_ss=7b289&oh=00_Af-KZM2OStHHM8w1bLfOBVxrhR9IqIRUKpzbmwms35MXdA&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)
