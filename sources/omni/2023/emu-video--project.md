# Emu Video | Meta
Source: https://emu-video.metademolab.com/
Emu Video | Meta



We use cookies and similar technologies to help provide the content on the Emu-Video site and Google Analytics for analytics purposes. You can learn more about cookies and how we use them in our [**Cookie Policy**](#/cookies)

DeclineAccept

* [Emu Video](/)
* [Demo](#/demo)
* [Blog](https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/)
* [Paper](https://arxiv.org/pdf/2311.10709.pdf)
* [Emu Edit](https://emu-edit.metademolab.com/)

[Emu Video](/)

Research by AI at Meta

* [Emu Video](/)
* [Demo](#/demo)
* [Blog](https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/)
* [Paper](https://arxiv.org/pdf/2311.10709.pdf)
* [Emu Edit](https://emu-edit.metademolab.com/)

# Emu Video: Factorizing Text-to-Video Generation by Explicit Image Conditioning

### State-of-the-art text-to-video generation

[Try it out](#/demo)

[Sorry, your browser doesn't support embedded videos.](/assets/videos/hero/emu_hero_figure_v2.mp4)

An Emu on a ski trip, 4k, high resolution

PrevShuffleNext

[](/assets/videos/shuffle/videos_16fps_watermarked_v2/000015.mp4)

A grizzly bear hunting for fish in a river at the edge of a waterfall, photorealistic

[](/assets/videos/shuffle/videos_16fps_watermarked_v2/000048.mp4)

Backside view of a man rowing a boat and moving away from the camera

[](/assets/videos/shuffle/videos_16fps_watermarked_v2/000046.mp4)

A ghost made with ice in the Grand Canyon, with a breathtaking view, photorealistic

[](/assets/videos/shuffle/videos_16fps_watermarked_v2/000021.mp4)

A corgi ice skating in winter wonderland, photorealistic

[Try it out](#/demo)

## Factorizing Text-to-Video Generation by Explicit Image Conditioning

![](assets/images/approach_overview_v15_bis.png)

**Emu Video** is a simple method for text to video generation based on diffusion models, factorizing the generation into two steps:

* First generating an image conditioned on a text prompt
* Then generating a video conditioned on the prompt and the generated image

Factorized generation allows us to train high quality video generation models efficiently. Unlike prior work that requires a deep cascade of models, our approach only requires two diffusion models to generate 512px, 4 second long videos at 16fps.

## State of the Art results

We compared **Emu Video** against state of the art text-to-video generation models on a varity of prompts, by asking human raters to select the most convincing videos, based on **quality** and **faithfulness** to the prompt.

Our 512 pixels, 16 frames per second, 4 second long videos win on both metrics against prior works: Make-a-Video (**MAV**), Imagen-Video (**Imagen**), Align Your Latents (**AYL**), Reuse & Diffuse (**R&D**), Cog Video (**Cog**), Gen2 (**Gen2**) and Pika Labs (**Pika**).

[Read the paper](https://arxiv.org/pdf/2311.10709.pdf)

[Read our blog](https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/)

## Authors

Rohit Girdhar^\*

Mannat Singh^\*

Andrew Brown\*

Quentin Duval\*

Samaneh Azadi\*

Sai Saketh Rambhatla

Akbar Shah

Xi Yin

Devi Parikh

Ishan Misra\*

(^): equal first authors(\*): equal technical contribution

## Acknowledgments

###### We are grateful for the support of multiple collaborators who helped us in this work.

Baixue Zheng, Baishan Guo, Jeremy Teboul, Milan Zhou, Shenghao Lin, Kunal Pradhan, Jort Gemmeke, Jacob Xu, Dingkang Wang, Samyak Datta, Guan Pang, Symon Perriman, Vivek Pai, Shubho Sengupta for their help with the data and infra. We would like to thank Uriel Singer, Adam Polyak, Shelly Sheynin, Yaniv Taigman, Licheng Yu, Luxin Zhang, Yinan Zhao, David Yan, Yaqiao Luo, Xiaoliang Dai, Zijian He, Peizhao Zhang, Peter Vajda, Roshan Sumbaly, Armen Aghajanyan, Michael Rabbat, and Michal Drozdzal for helpful discussions. We are also grateful to the help from Lauren Cohen, Mo Metanat, Lydia Baillergeau, Amanda Felix, Ana Paula Kirschner Mofarrej, Kelly Freed, Somya Jain. We thank Ahmad Al-Dahle and Manohar Paluri for their support.

[Privacy Policy](https://www.facebook.com/privacy/)[Cookie Policy](#/cookies)

©2023 Meta

[Privacy Policy](https://www.facebook.com/privacy/)[Cookie Policy](#/cookies)
