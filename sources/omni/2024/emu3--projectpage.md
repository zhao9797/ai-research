# Emu3
Source: https://emu.baai.ac.cn/about
Emu3



![](/assets/logo-CdQBRR2F.svg)

* Emu3

中文/En

[](/assets/bg1-CcNX2l8V.mp4)

Next-Token Prediction is All You Need

[Code](https://github.com/baaivision/Emu3)

[Technical report](https://arxiv.org/pdf/2409.18869)

[Model](https://huggingface.co/collections/BAAI/emu3-66f4e64f70850ff358a2e60f)

Overview

While next-token prediction is considered a promising path towards AGI, it has struggled to excel in multimodal tasks, which are still dominated by diffusion models (e.g., Stable Diffusion) and compositional approaches (e.g., CLIP combined with LLMs). In this work, we introduce Emu3, a new suite of state-of-the-art multimodal models trained solely with next-token prediction. By tokenizing images, text, and videos into a discrete space, we train a single transformer from scratch on a mixture of multimodal sequences.

![](/assets/modelArchitecture-DD094UnK.png)

Emu3 outperforms several well-established task-specific models in both generation and perception tasks, surpassing flagship models such as SDXL, LLaVA-1.6 and OpenSora-1.2, while eliminating the need for diffusion or compositional architectures.

![](/assets/specificModel-CDLInZFV.png)

We simplify complex multimodal model designs by converging on a singular focus: tokens, unlocking great potential for scaling both during training and inference. Our results demonstrate that next-token prediction is a promising path towards building general multimodal intelligence beyond language.

Image Generation

Emu3 generates high-quality images by predicting next vision token. The model naturally supports flexible resolutions and styles.

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/1.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/2.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/3.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/4.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/5.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/6.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/7.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/8.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/9.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/10.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/11.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/12.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/13.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/14.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/15.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/16.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/17.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/18.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/19.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/20.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/21.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/22.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/23.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/24.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/25.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/26.webp)![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/image_generation_webp/27.webp)![](/assets/logo1-BOd5J4vL.svg)

Video Generation

Emu3 is capable of generating videos. Unlike Sora which employs a video diffusion model to generate the video from noise, Emu3 simply generates a video causally by predicting the next token in a video sequence.

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/113_113_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/131_131_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/141_141_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/186_186_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/196_196_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/208_208_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/A%20young%20girl%20with%20curly%20blonde%20hair%20smiles%20softly%2C%20her%20bright%20eyes%20twinkling.%20She%20wears%20a%20light%20pink%20lace%20dress%20against%20a%20blurred%20backdrop%20of%20blooming%20flowers..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/232_232_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/233_233_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/49_49_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/A%20drone%20view%20of%20celebration%20with%20Christmas%20tree%20and%20fireworks%2C%20starry%20sky%20-%20background..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/A%20man%20in%20his%20late%20twenties%20stands%20in%20calm%20water%20at%20sunrise%20or%20sunset.%20He%20wears%20a%20light%20shirt%20and%20looks%20away.%20Warm%20colors%20reflect%20on%20the%20water.%20The%20camera%20shows%20a%20steady%20side%20view..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/267_268_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/A%20squirrel%20eating%20a%20burger..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/A%20teenage%20boy%20with%20a%20casual%20hairstyle%20smiles%20friendly%20at%20the%20camera.%20He%20wears%20a%20hoodie%20and%20has%20a%20relaxed%20posture%20with%20a%20soft-focused%20background..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/A%20woman%20with%20long%20red%20hair%20and%20fair%20skin%20appears%20in%20a%20daytime%20urban%20background.%20She%20wears%20a%20dark%20top%20and%20a%20nose%20ring%2C%20with%20closed%20eyes%20and%20a%20calm%20expression.%20The%20scene%20is%20still%20and%20tranquil%2C%20captured%20in%20a%20portrait-style%20video..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/133_134_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/Aerial%20view%20of%20a%20city%20at%20dusk%20with%20the%20sky%20turning%20orange%20and%20pink.%20A%20canal%20with%20gabled%20buildings%20and%20warm%20streetlights%20runs%20through%20the%20city.%20Boats%20are%20docked%20nearby%2C%20and%20busy%20streets%20show%20people%20and%20vehicle%20light%20streaks..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/An%20astronaut%20flying%20in%20space%2C%20in%20cyberpunk%20style.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/An%20older%20woman%20with%20curly%20gray%20hair%20smiles%20warmly%2C%20wearing%20a%20denim%20jacket%20over%20a%20floral%20blouse..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/109_110_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/Fireworks..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/Lava%20bursts%20from%20the%20volcano%2C%20flowing%20down%20the%20mountain%20and%20filling%20the%20sky%20with%20ash..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/Snow%20and%20rocks%20cascade%20down%20a%20snowy%20mountain%2C%20creating%20a%20roaring%20cloud%20as%20the%20avalanche%20moves..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/Snow%20rocky%20mountains%20peaks%20canyon.%20snow%20blanketed%20rocky%20mountains%20surround%20and%20shadow%20deep%20canyons.%20the%20canyons%20twist%20and%20bend%20through%20the%20high%20elevated%20mountain%20peaks%2C%20pixel%20art.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/The%20sun%20rises%20over%20the%20ocean%2C%20warming%20the%20sky.%20Golden%20waves%20shimmer%20towards%20the%20shore..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/Two%20butterflies%20flutter%20among%20colorful%20flowers%20under%20a%20blue%20sky%2C%20their%20wings%20shimmering%20in%20the%20sunlight..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/White%20flowers%20with%20prominent%20stamens%20and%20green%20leaves.%20Delicate%20petals%20and%20brown-tipped%20stamens.%20Shiny%2C%20serrated%20leaves%20indicate%20health.%20Background%20shows%20blue%20sky%2C%20white%20clouds%2C%20and%20greenery..mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/demo_human_prompts_8_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

[](https://baai-solution.ks3-cn-beijing.ksyuncs.com/emu3/static/video_generation/demo_human_prompts_9_1_0.mp4)![](/assets/logo1-BOd5J4vL.svg)

Video Prediction

With a video in context, Emu3 can naturally extend the video and predict what will happen next. The model can simulate some aspects of the environment, people and animals in the physical world.

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Is loading

![](/assets/logo1-BOd5J4vL.svg)

Vision-Language Understanding

Emu3 demonstrates strong perception capabilities to understand the physical world and provides coherent text responses. Notably, this capability is achieved without depending on a CLIP and a pretrained LLM.

Case 1:

1

Input:

User:

Please describe the image in detail

![](/assets/understand1-D3aNxggw.png)

2

Output:

Emu3:

The image is the cover of a magazine titled "Parktakes," which is the Fall 2017 issue. The cover features two individuals in a white kayak, paddling on a body of water. The kayak is positioned diagonally, with the two individuals seated towards the front. Both individuals are wearing life jackets, which are red with black straps, and they are holding paddles with orange blades. The person on the left is a woman with long dark hair, wearing sunglasses and a black top. The person on the right is a man with short hair, wearing a green shirt and a light-colored cap. They both appear to be smiling and enjoying their time on the water.

The background shows a natural setting with trees and greenery, indicating that they are likely in a park or natural reserve. The water is calm, and the sky is not visible, suggesting a serene and peaceful environment.

The magazine cover includes several text elements:

1. \*\*Title\*\*: "Parktakes" is prominently displayed at the top in large, bold, blue letters.

2. \*\*Fall 2017 Issue\*\*: The issue is marked in the top right corner in a smaller, white font.

3. \*\*Main Feature\*\*: "Enjoy Fall Adventures in Parks" is written in a large, bold, orange font, emphasizing the theme of outdoor activities.

4. \*\*Additional Features\*\*: The cover lists several topics covered in the magazine:

- "Birding, Boating, and Hiking"

- "Seasonal Festivals"

- "New Attractions"

5. \*\*Registration Information\*\*: At the bottom, there is a call to action to "Registration begins Aug. 1 for full classes" and a website link:"www.fairfaxcounty.gov/parks."

Analysis and Description

The cover of "Parktakes" effectively conveys the theme of outdoor recreational activities, particularly in parks. The image of the two individuals in a kayak suggests that the magazine features content related to kayaking, canoeing, and other water sports. The inclusion of life jackets indicates a focus on safety and preparedness for water activities. The mention of seasonal festivals and new attractions implies that the magazine includes information on various events and attractions within the parks.

The cover also highlights the magazine's commitment to providing a comprehensive guide to outdoor activities, with a clear emphasis on safety and accessibility. The registration information suggests that the magazine is a resource for planning and participating in various outdoor activities, likely targeting a wide audience interested in parks and recreational activities.

In summary, the magazine cover is designed to attract readers interested in outdoor adventures, safety, and seasonal events within parks. The use of a kayak and life jackets emphasizes the magazine's focus on water sports and safety, while the inclusion of various features and registration information suggests a well-rounded resource for park visitors.

See full sample

Case 2:

1

Input:

User:

Describe the landmark.

![](/assets/understand2-CPbVKptU.png)

2

Output:

Emu3:

The image showcases the Brooklyn Bridge, a prominent suspension bridge in New York City, recognized by its distinctive towers and the web of cables that support it. This iconic structure connects the boroughs of Brooklyn and Manhattan.

Contact us:

Emu@baai.ac.cn

©2022 Beijing Zhiyuan Artificial Intelligence Research Institute Beijing IC

[Overview](#Overview)

[Image Generation](#Image-Generation)

[Video Generation](#Video-Generation)

[Video Prediction](#Video-Prediction)

[Understanding](#Vision-Language)
