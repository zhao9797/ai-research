# BAGEL: The Open-Source Unified Multimodal Model
Source: https://bagel-ai.org/
BAGEL: The Open-Source Unified Multimodal Model


# BAGEL: The Open-Source Unified Multimodal Model

Released on May 20, 2025

Chaorui Deng∗, Deyao Zhu∗, Kunchang Li∗, Chenhui Gou∗, Feng Li∗,   
Zeyu Wang, Shu Zhong, Weihao Yu, Xiaonan Nie, Ziang Song, Guang Shi§, Haoqi Fan∗†

∗Equal contribution, §Corresponding Author, †Project lead

GitHubHuggingFacePaperShowcaseShareDemo

[](https://lf3-static.bytednsdoc.com/obj/eden-cn/nuhojubrps/bagel-hero-video.mp4)

  

Today we introduce **BAGEL**, the open-source Unified Multimodal Model you can fine-tune, distill and deploy anywhere, offering comparable functionality to proprietary systems like GPT-4o and Gemini 2.0 in an open form, unlocks useful and valuable image generation through a natively multimodal architecture capable of precise, accurate, and photorealistic outputs.

  
  

ChatGenerationEditingStyle TransferNavigationCompositionThinking

## Chat

BAGEL is a unified generation and understanding model, pre-training initialized from large language models, providing it with foundational capabilities for reasoning and conversation. BAGEL can handle both image and text inputs and outputs in a mixed format.

1 of 6

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/chat/case1/input_1.webp)

Tell me about this picture

This picture shows a close-up of the David statue, a famous sculpture by Michelangelo. The statue is a marble sculpture of a young man, likely representing the biblical hero David, who is known for his strength and courage. The statue is located in the Accademia Gallery in Florence, Italy. The sculpture is renowned for its lifelike depiction of the human form, with a focus on the muscular anatomy and the expression of the figure. The statue is a masterpiece of Renaissance art and is considered one of the most iconic sculptures in the world.

Show more

Can you tell me more about the artist of this sculpture?

Michelangelo Buonarroti was an Italian Renaissance artist, sculptor, painter, architect, and poet. He is widely regarded as one of the greatest artists of all time and is known for his works in sculpture, painting, and architecture. Michelangelo was born in 1475 in Florence, Italy, and died in 1564. He was a member of the Medici family and was commissioned to create several works for the Medici palace. Some of his most famous works include the David statue, the Sistine ceiling, and the Pieta. Michelangelo was a highly skilled artist who was known for his attention to detail, his use of light and shadow, and his ability to capture the human form in a way that was both realistic and idealized. He was also a highly skilled architect and designed several buildings, including the Medici villa in Arezzo. Michelangelo's works continue to inspire and awe audiences around the world, and he is considered one of the greatest artists of all time.

Show more

## Generation

BAGEL is pre-trained on large-scale, interleaved video and web data, enabling it to generate high-fidelity, photorealistic images, video frames, or interleaved image-text content. The interleaved data, with a proper alignment, fosters a natural multimodal Chain-of-Thought that allows the model to `<think>` before generating visual outputs.

1 of 16

a photo of three antique glass magic potions in an old abandoned apothecary shop: the first one is blue with the label "SDXL", the second one is red with the label "BAGEL", the third one is green with the label "FLUX"

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/generation/case4/output_1.webp)

## Editing

By pre-training on interleaved video clips, BAGEL naturally learns to preserve visual identities and fine details, while also capturing complex visual motion from videos—making it highly effective for image editing. With strong reasoning abilities inherited from visual-language models, BAGEL's intellectual editing ability effortlessly surpasses basic editing tasks.

1 of 21

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/editing/case1/input_1.webp)

He squatted down and touched a dog's head

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/editing/case1/output_1.webp)

## Style Transfer

With its deep understanding of visual content and styles, BAGEL can easily transform an image from one style to another—or even shift it across entirely different worlds—using only minimal alignment data.

1 of 12

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/editing/case6/input_1.webp)

Change to 3D animated style

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/style-transfer/case1/output_1.webp)

## Navigation

By learning from video, BAGEL effectively distills navigation knowledge from the largest simulator - the real world - allowing it to navigate a wide range of environments, including those found in sci-fi worlds, artistic paintings, and with diverse rotations or perspectives.

1 of 9

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/navigation/case1/input_1.webp)

After 0.40s, move forward

![Preview frame](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/navigation/case1/output_1_1.webp)

Generate

## Composition

BAGEL learns a wide range of knowledge and capabilities from video, web, and language data, enabling it to perform reasoning, model physical dynamics, predict future frames, and more—all through a unified multimodal interface. With the compositional abilities, BAGEL can engage in multi-turn conversations seamlessly.

1 of 3

A female cosplayer portraying an ethereal fairy or elf, wearing a flowing dress made of delicate fabrics in soft, mystical colors like emerald green and silver. She has pointed ears, a gentle, enchanting expression, and her outfit is adorned with sparkling jewels and intricate patterns. The background is a magical forest with glowing plants, mystical creatures, and a serene atmosphere.

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/composition/case1/output_1.webp)

Make her a Jellycat plush toy.

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/composition/case1/output_2.webp)

I want to promote this doll to kids. Can you help me come up with a catchy slogan?

Fly into Imagination with Our Magical Fairy Doll!

## Thinking

BAGEL incorporates a thinking mode, leveraging its multimodal understanding to enhance generation and editing. By reasoning through prompts, BAGEL transforms brief descriptions into detailed and coherent outputs. This ensures generated content has nuanced context, accurate details, and logical consistency, resulting in richer and more precise outcomes.

1 of 6

A car made of small cars.

<think>
The model should generate an image where numerous small cars are combined to form the shape and structure of a larger car.
The refined prompt is: A highly detailed and creative image showcasing a large car composed entirely of numerous small cars, meticulously arranged to replicate the shape and structure of a full-sized vehicle. The small cars are tightly interlocked, creating a seamless and realistic exterior with accurate proportions and details. The setting is neutral and clean, with soft, diffused lighting to emphasize the intricacy of the composition without any distractions. The image captures the concept in a photorealistic style, with a focus on precision and craftsmanship, highlighting the innovative use of scale and form.
</think>

Read more

![Content 0](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/thinking/case1/output_1.webp)

  
  

## Method

  

BAGEL adopts a Mixture-of-Transformer-Experts (MoT) architecture to maximize the model’s capacity to learn from richly diverse multimodal information. Following the same principle of capacity maximization, it utilizes two separate encoders to capture pixel-level and semantic-level features of an image. The overall framework follows a Next Group of Token Prediction paradigm, where the model is trained to predict the next group of language or visual tokens as a compression target.

BAGEL scales MoT’s capacity through Pre-training, Continued Training, and Supervised Finetuning on trillions of interleaved multimodal tokens spanning language, image, video, and web data. It surpasses open models on standard understanding and generation benchmarks and demonstrates advanced in-context multimodal abilities like free-form image editing, future frame prediction, 3D manipulation, world navigation, and sequential reasoning.

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang/tmp/method/input_1.webp)

  
  

## Emerging Properties

![](https://lf3-static.bytednsdoc.com/obj/eden-cn/slnhi/ljhwZthlaukjlkulzlp/likunchang2/emerging/case1/input_1.webp)

As we scale up BAGEL’s pretraining with more multimodal tokens, we observe consistent performance gains across understanding, generation, and editing tasks. Different capabilities emerge at distinct training stages—multimodal understanding and generation appear early, followed by basic editing, while complex, intelligent editing emerges later. This staged progression suggests an emergent pattern, where advanced multimodal reasoning builds on well-formed foundational skills. Ablation studies further show that combining VAE and ViT features significantly improves intelligent editing, underscoring the importance of visual-semantic context in enabling complex multimodal reasoning and further supporting its role in the emergence of advanced capabilities.

## Benchmark

### Understanding

| Model | MME-P | MMBench | MMMU | MMVet |
| --- | --- | --- | --- | --- |
| Chameleon-7B | - | 35.7 | 28.4 | 8.3 |
| Show-o-1.3B | 1097 | - | 26.7 | - |
| Emu3-8B | 1244 | 58.5 | 31.6 | 37.2 |
| TokenFlow-XL-13B | 1546 | 68.9 | 38.7 | 40.7 |
| Janus-Pro-7B | 1567 | 79.2 | 41 | 50 |
| MetaQuery-XL-7B | 1685 | 83.5 | 58.6 | 66.6 |
| BLIP3-o-8B | 1683 | 83.5 | 50.6 | 66.6 |
| BAGEL | 1687 | 85 | 55.3 | 67.2 |

Note: MetaQuery and BLIP3-o adopts pre-trained model from Qwen2.5-VL and freezes it during training.

### Generation

| Model | Single Object | Two Object | Counting | Colors | Position | Color Attribute | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Chameleon-7B | - | - | - | - | - | - | 0.39 |
| Show-o-1.3B | 0.98 | 0.80 | 0.66 | 0.84 | 0.31 | 0.50 | 0.68 |
| Emu3-8B | 0.99 | 0.81 | 0.42 | 0.80 | 0.49 | 0.45 | 0.66 |
| TokenFlow-XL-13B | 0.95 | 0.60 | 0.41 | 0.81 | 0.16 | 0.24 | 0.55 |
| Janus-Pro-7B | 0.99 | 0.89 | 0.59 | 0.90 | 0.79 | 0.66 | 0.80 |
| MetaQuery-XL-7B | - | - | - | - | - | - | 0.80 |
| BLIP3-o-8B | - | - | - | - | - | - | 0.84 |
| BAGEL | 0.98 | 0.95 | 0.84 | 0.95 | 0.78 | 0.77 | 0.88 |

BAGEL

A Scalable Unified Multimodal Model for next-generation AI systems.

Share Site

© 2025 BAGEL Unified Multimodal Model. All rights reserved.
