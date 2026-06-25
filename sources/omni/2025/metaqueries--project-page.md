# Transfer between Modalities with MetaQueries
Source: https://xichenpan.com/metaquery/
Transfer between Modalities with MetaQueries



# *Transfer between Modalities with MetaQueries*

Introducing MetaQuery, a minimal recipe for building state-of-the-art unified multimodal understanding (text output) and generation (pixel output) models:

![metaquery Icon](./static/img/icons/query.svg)

**MetaQuery**: We introduce MetaQuery, a set of learnable queries that efficiently connect autoregressive multimodal LLMs (MLLMs) with diffusion-based image generators.

![transfer Icon](./static/img/icons/transfer.svg)

**Transfer**: This simple approach enables the world knowledge, strong reasoning and in-context learning capabilities inherent in MLLMs to be transferred to image generation.

![frozen Icon](./static/img/icons/freeze.svg)

**Frozen MLLM**: This transfer is effective even when the MLLM backbone remains frozen, thereby preserving its state-of-the-art multimodal understanding capabilities while achieving strong generative performance.

[arXiv](https://arxiv.org/abs/2504.06256)

[pdf](https://arxiv.org/pdf/2504.06256)

[Code](https://github.com/facebookresearch/metaquery)
[![Hugging Face logo](https://huggingface.co/front/assets/huggingface_logo-noborder.svg)
Data](https://huggingface.co/collections/xcpan/metaquery-instruction-tuning-data-685b0f16d81ce54bcb7ea3a8)

![Teaser Image](static/img/teaser.png)

[Xichen Pan1,2](https://xichenpan.com/)  
[Satya Narayan Shukla1,†](https://satyanshukla.github.io/)  
[Aashu Singh1](https://www.linkedin.com/in/aashu-singh-030ab646/)  
[Zhuokai Zhao1](https://zhuokai-zhao.com/)  
[Shlok Kumar Mishra1](https://shlokk.github.io/shlokmishra.github.io/)  
[Jialiang Wang1](https://sites.google.com/view/jialiangwang/home)  
[Zhiyang Xu1](https://scholar.google.com/citations?user=Qcshi8UAAAAJ&hl=en)  
[Jiuhai Chen1](https://scholar.google.com/citations?user=eJP77eoAAAAJ&hl=en)  
[Kunpeng Li1](https://kunpengli1994.github.io/)  
[Felix Juefei-Xu1](https://xujuefei.com/)  
[Ji Hou1,†](https://sekunde.github.io)  
[Saining Xie2,†](https://www.sainingxie.com/)

[1Meta](https://ai.meta.com/)  
[2New York University](https://cs.nyu.edu/home/index.html)

†Equal advising

We introduce MetaQueries, a set of learnable queries that efficiently connect autoregressive multimodal LLMs (MLLMs) with diffusion-based image generators. This simple approach enables the generative decoder to directly leverage the rich semantic understanding, reasoning capabilities, and world knowledge inherent in MLLMs for knowledge-augmented image generation.
  
  
This blogpost is structured around three key components:

1. **[§MetaQuery](#MetaQuery)**: We introduce MetaQuery and carefully analyze the impact of applying MetaQuery on image generation performance in a controlled setting.
2. **[§Instruction Tuning Data](#Instruction Tuning Data)**: We proposed a scalable data curation pipeline that directly leverages naturally occurring image pairs from web corpora, surprisingly unlocks several new capabilities like visual association and logo design.
3. **[§Performance](#Performance)**: We demonstrate our method can preserve SOTA multimodal understanding capabilities while achieving SOTA-level generative performance. We also show great performance on image reconstruction and editing, subject-driven generation, reasoning- and knowledge-based image generation.

[![MetaQuery Logo](static/img/icons/query.svg)
MetaQuery](#MetaQuery)
[![Instruction Tuning Data Logo](static/img/icons/database.svg)
Instruction Tuning Data](#Instruction Tuning Data)
[![Performance Logo](static/img/icons/image.svg)
Performance](#Performance)

![](static/img/icons/click.gif)
**Click to jump to each section.**

← Previous

Text-to-Image Generation

Next →

![Text-to-Image Example 1](static/demo/t2i/1.png)

A british shorthair wearing sunglasses

![Text-to-Image Example 2](static/demo/t2i/2.png)

An old rusted robot wearing pants and a jacket riding skis in a supermarket.

![Text-to-Image Example 3](static/demo/t2i/3.png)

A giant humanoid, made of fluffy blue cotton candy, stomping on the ground, and roaring to the sky, clear blue sky behind them.

![Text-to-Image Example 4](static/demo/t2i/4.png)

The word 'START' written on a street surface.

![Text-to-Image Example 5](static/demo/t2i/5.png)

Close-up of a bright blue parrot's feathers glittering in the light, showing its unique plumage and vibrant colors.

![Text-to-Image Example 6](static/demo/t2i/6.png)

A sunken ship at the bottom of the ocean.

![Instruction Example 1](static/demo/inst/12.png)
![Instruction Example 1](static/demo/inst/11.jpg)

Top view of the same berry bowl

![Instruction Example 2](static/demo/inst/22.png)
![Instruction Example 2](static/demo/inst/21.jpg)

The same robot in Minecraft

![Instruction Example 3](static/demo/inst/32.png)
![Instruction Example 3](static/demo/inst/31.png)

The same model but a real one in New York city

![Instruction Example 4](static/demo/inst/42.png)
![Instruction Example 4](static/demo/inst/41.jpg)

The skyline view of the city from this building

![Instruction Example 5](static/demo/inst/52.png)
![Instruction Example 5](static/demo/inst/51.jpg)

The statue in the same city

![Instruction Example 6](static/demo/inst/62.png)
![Instruction Example 6](static/demo/inst/61.jpg)

A logo for the same teapot

![Reasoning Example 1](static/demo/augment/1.png)

The national flag of the country where Yellowstone National Park is located.

![Reasoning Example 2](static/demo/augment/2.png)

The animal associated with having (2+7) lives.

![Reasoning Example 3](static/demo/augment/3.png)

The flower celebrated in spring festivals in the country where sushi originated.

![Reasoning Example 4](static/demo/augment/4.png)

The tallest building dominates the skyline of the city known as the City of Light.

![Reasoning Example 5](static/demo/augment/5.png)

A phone with a drained battery.

![Reasoning Example 6](static/demo/augment/6.png)

A night sky on a new moon night.

![Edited Image](static/demo/edit/12.png)
![Original Image](static/demo/edit/11.jpeg)

Add a chef hat to the dog

![Edited Image](static/demo/edit/42.png)
![Original Image](static/demo/edit/41.jpeg)

Replace the dog with a golden retriever

![Edited Image](static/demo/edit/52.png)
![Original Image](static/demo/edit/51.jpeg)

Change to cartoon style

![Edited Image](static/demo/edit/62.png)
![Original Image](static/demo/edit/61.jpeg)

Change it into lineart style

![Edited Image](static/demo/edit/72.png)
![Original Image](static/demo/edit/71.jpeg)

Chenage the bird to a blue one

![Edited Image](static/demo/edit/82.png)
![Original Image](static/demo/edit/81.jpeg)

Replace the fries with salad

---

# MetaQuery

MetaQuery bridges frozen MLLMs with diffusion models. We use randomly initialized learnable queries to query out the conditions for generation. For simplicity and compatibility, we continue to use causal masking for the entire sequence. The conditions are then fed into a trainable connector to align with the input space of text-to-image diffusion models. The whole model is trained with the original generation objective on paired data.

![MetaQuery](static/img/metaquery.png)


**Figure 1:** Overview of our model. Blue tokens maintain SOTA multimodal understanding; MetaQuery are learnable queries that directly applied to frozen MLLMs to query out conditions for generation. The model is tuned using only denoising objective with paired data. The generative diffusion models can be either frozen or further instruction-tuned for advanced generation tasks.

The proposed architecture involves two design choices: using **learnable queries** and keeping the **MLLM backbone frozen**. We explain the reasons why we adopted these choices and how they impact performance. We report FID score on MJHQ-30K for visual aesthetic quality, and GenEval and DPG-Bench (both without prompt rewriting) for prompt alignment, respectively.

**Learnable Queries:** While many models use the (M)LLM's last layer embedding of input tokens for image generation, this approach limits unified modeling capabilities such as in-context learning and multimodal outputs. Our experiments show that learnable queries with just 64 tokens achieve comparable image generation quality to using last layer embeddings while unlocking the MLLM's in-context learning capability. Increasing to 512 tokens further improves performance, even surpassing the last layer embedding approach.

| **Methods** | **Number of Tokens** | **MJHQ-30K FID ↓** | **GenEval ↑** | **DPG-Bench ↑** |
| --- | --- | --- | --- | --- |
| LLM last layer embedding\* | - | 7.49 | 0.55 | 78.41 |
| Learnable queries | 64 | 7.43 | 0.56 | 75.35 |
| Learnable queries | 512 | 7.34 | 0.56 | 78.43 |

**Table 1:** Study on different conditions for image generation. \* denotes the embeddings of input tokens.

**Frozen MLLMs:** We keep the MLLM backbone frozen to preserve its understanding capabilities while avoiding complex training. Our experiments show that frozen MLLMs perform comparably to fully-tuned models, with slightly better visual quality but lower prompt alignment. This suggests that MetaQuery is another possible training strategy, one that is simpler but also effective, as an alternative to fine-tuning the entire MLLM.

| **Methods** | **Train LLM** | **Train DiT** | **MJHQ-30K FID ↓** | **GenEval ↑** | **DPG-Bench ↑** |
| --- | --- | --- | --- | --- | --- |
| MLLM tuning | ✓ | ✗ | 7.75 | 0.58 | 78.97 |
| E2E tuning | ✓ | ✓ | 6.28 | 0.61 | 79.39 |
| Frozen MLLM | ✗ | ✗ | 7.43 | 0.56 | 75.35 |
| Frozen MLLM | ✗ | ✓ | 6.06 | 0.61 | 76.66 |

**Table 2:** Study on strategies for adapting MLLMs. The methods without training LLM do not suffer from multimodal understanding degradation.

# Training Recipe

We further study key training options for the two main components of MetaQuery: the **number of tokens** and **connector design**.

**Number of Tokens:** We observe promising scaling results on both text-to-image generation and image reconstruction.

![Number of Tokens](static/img/num_of_tokens.png)


**Figure 2:** Study on the scaling of token numbers on text-to-image generation. As the number of tokens increases, prompt alignment results consistently improve.



![Number of Tokens Rec Samples](static/img/num_of_tokens_rec_samples.png)


**Figure 3:** Visaul samples for image reconstruction with different numbers of tokens.

**Connector Design:** We study two connector designs: Projection Before Encoder (Proj-Enc) and Projection After Encoder (Enc-Proj). Enc-Proj first aligns conditions in the MLLM hidden dimension before projecting to the diffusion decoder input dimension, achieving better performance with fewer parameters than Proj-Enc.

| Architecture | # of Layers | Dims | # of Params | Rel. Wall Time | MJHQ-30K FID ↓ | GenEval ↑ | DPG-Bench ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Proj-Enc | 6 | 2304 | 517M | 1.06x | 7.80 | 0.53 | 73.37 |
| Proj-Enc | 24 | 2304 | 2046M | 1.23x | 7.41 | 0.51 | 73.75 |
| Enc-Proj | 6 | 896 | 84M | 1x | 7.73 | 0.49 | 71.39 |
| Enc-Proj | 24 | 896 | 316M | 1.06x | 7.43 | 0.56 | 75.35 |

**Table 3:** Study on connector design.

# Instruction Tuning Data

We choose to use a scalable data curation pipeline that directly leverages naturally occurring image pairs from web corpora, instead of depending on human-created pairs or synthetically generated data. These image pairs often exhibit meaningful associations and specific relationships spanning a broad spectrum.

We first cluster images with similar captions and designate one image as the target. This process yields 2.4M image pairs. Finally, we employ Qwen2.5-VL 3B to generate instructions for each pair, describing how to transform the source images into the target image.

![Instruction Tuning Data Construction](static/img/data.png)


**Figure 4:** Overview of instruction tuning data curation pipeline. We group images from web corpora based on caption similarity, then construct instruction-tuning data from these image pairs using an MLLM.

# Image Understanding and Generation

Finally, We train our models on three different MLLM backbones for different sizes: Base (LLaVA-OneVision 0.5B), Large (Qwen2.5-VL 3B), and X-Large (Qwen2.5-VL 7B). We set the number of tokens to 256 for all models, and utilize a 24-layer connector with Enc-Proj architecture. For image generation heads, we tested two different diffusion models: Stable Diffusion v1.5 and Sana-1.6B. Our model family demonstrates strong capabilities across both understanding and generation tasks. All of our models in different sizes exhibit competitive performance on all understanding benchmarks. In terms of image generation, MetaQuery achieves SOTA visual quality on MJHQ-30K, and closely match the SOTA prompt alignment results on GenEval and DPG-Bench.

| Methods | Base (M)LLM | MME-P | MMB | SEED | MMMU | MM-Vet | COCO FID ↓ | MJHQ FID ↓ | GenEval ↑ | DPG-Bench ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Emu | LLaMA 13B | - | - | - | - | - | 11.66 | - | - | - |
| DreamLLM | Vicuna 7B | - | - | - | - | 36.6 | 8.46 | - | - | - |
| Chameleon | From Scratch 7B | - | - | - | 22.4 | 8.3 | 26.74 | - | 0.39 | - |
| Show-o-512 | Phi-1.5 1.3B | 1097.2 | - | - | 26.7 | - | 9.24 | 15.18 | 0.68 | - |
| VILA-U | LLaMA-2 7B | 1401.8 | - | 59.0 | - | 33.5 | - | 7.69 | - | - |
| Emu3 | From Scratch 7B | - | 58.5 | 68.2 | 31.6 | 37.2 | 12.80 | - | 0.66† | 80.60 |
| MetaMorph | LLaMA-3 8B | - | 75.2 | 71.8 | - | - | 11.8 | - | - | - |
| TokenFlow-XL | Qwen-2.5 14B | 1551.1 | 76.8 | 72.6 | 43.2 | 48.2 | - | - | 0.63† | 73.38 |
| Transfusion | From Scratch 7B | - | - | - | - | - | 8.70 | - | 0.63 | - |
| LMFusion | LLaVA-Next 8B | 1603.7 | 72.1 | 72.5 | 41.7 | - | 8.20 | - | - | - |
| Janus | DeepSeek-LLM 1.5B | 1338.0 | 69.4 | 63.7 | 30.5 | 34.3 | 8.53 | 10.10 | 0.61 | - |
| JanusFlow | DeepSeek-LLM 1.5B | 1333.1 | 74.9 | 70.5 | 29.3 | 30.9 | - | 9.51 | 0.63 | 80.09 |
| Janus-Pro-1B | DeepSeek-LLM 1.5B | 1444.0 | 75.5 | 68.3 | 36.3 | 39.8 | - | 14.33‡ | 0.73 | 82.63 |
| Janus-Pro-7B | DeepSeek-LLM 7B | 1567.1 | 79.2 | 72.1 | 41.0 | 50.0 | - | 13.48‡ | 0.80 | 84.19 |
|  | | | | | | | | | | |
| MetaQuery-B | LLaVA-ov 0.5B | 1238.0 | 58.5 | 66.6 | 31.4 | 29.1 | 8.91 | 6.28 | 0.74† | 80.04 |
| MetaQuery-L | Qwen2.5-VL 3B | 1574.3 | 78.6 | 73.8 | 53.1 | 63.2 | 8.87 | 6.35 | 0.78† | 81.10 |
| MetaQuery-XL | Qwen2.5-VL 7B | 1685.2 | 83.5 | 76.9 | 58.6 | 66.6 | 8.69 | 6.02 | 0.80† | 82.05 |

**Table 4:** Quantitative results on multimodal understanding and generation benchmarks. We report the COCO FID with Stable Diffusion v1.5, and other metrics with Sana. † denotes rewritten prompts. ‡ denotes results tested by us under the same settings.



![Qualitative Results](static/img/t2i.png)


**Figure 5:** Qualitative results on text-to-image generation.

# Image Reconstruction

We demonstrate that MetaQuery can be easily fine-tuned for image reconstruction tasks with a frozen MLLM. Our model achieves comparable quality to SOTA models.

![Image Reconstruction](static/img/image_reconstruction.png)


**Figure 6:** Image reconstruction results.

# Image Editing

We demonstrate that MetaQuery can transfer its image reconstruction capability to perform image editing. We keep the MLLM backbone frozen and fine-tune our pre-trained Base model for only 1,000 steps on publicly available image editing data. Qualitative results demonstrate that our model performs effectively in these image-editing scenarios.

![Image Editing](static/img/edit.png)


**Figure 7:** Image editing results.

# Instruction Tuning

We show that after being instruction-tuned on the proposed 2.4M dataset, MetaQuery can achieve impressive zero-shot subject-driven generation performance, producing coherent results even with multiple highly customized subjects (the first row of Figure 8). Using various supervision signals, the instruction-tuned MetaQuery model surprisingly unlocks novel capabilities like visual association and logo design that go beyond copy-pasting (the second row of Figure 8).

![Instruction Tuning](static/img/subjectdriven.png)


**Figure 8:** Qualitative results for instruction tuning. Instruction-tuned MetaQuery achieves strong subject-driven capability (first row) and can even reason through the multimodal input to generate images (second row).

# Reasoning- and Knowledge-Augmented Generation

Our learnable queries effectively leverage the frozen LLM's capabilities, enabling better understanding of complex prompts requiring real-world knowledge and reasoning.

![Reasoning and Knowledge-Augmented Generation](static/img/commonsense.png)


**Figure 9:** MetaQuery leverages frozen MLLMs for reasoning- and knowledge-augmented generation. \* denotes that the LLM last layer embeddings of input tokens are used for image generation. This approach can be better than the base Sana model in some cases but fails to activate in-context learning to perform knowledge-augmented generation.

We evaluate MetaQuery's world knowledge reasoning capability on the WISE benchmark, which contains similar test cases to the knowledge-augmented generation examples shown in Figure 9. MetaQuery achieves SOTA performance, significantly outperforming all other unified models. Our work stands as the first unified model to successfully transfer the advanced capabilities of frozen MLLMs to image generation and exceed the performance of SOTA text-to-image models.

| **Methods** | **Cultural** | **Time** | **Space** | **Biology** | **Physics** | **Chemistry** | **Overall** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o | 0.94 | 0.64 | 0.98 | 0.93 | 0.98 | 0.95 | 0.89 |
| Text-to-Image Models | | | | | | | |
| SD-v1-5 | 0.34 | 0.35 | 0.32 | 0.28 | 0.29 | 0.21 | 0.32 |
| SD-XL | 0.43 | 0.48 | 0.47 | 0.44 | 0.45 | 0.27 | 0.43 |
| PixArt-Alpha | 0.45 | 0.50 | 0.48 | 0.49 | 0.56 | 0.34 | 0.47 |
| playground-v2.5 | 0.49 | 0.58 | 0.55 | 0.43 | 0.48 | 0.33 | 0.49 |
| SD-3.5-large | 0.44 | 0.50 | 0.58 | 0.44 | 0.52 | 0.31 | 0.46 |
| FLUX.1-dev | 0.48 | 0.58 | 0.62 | 0.42 | 0.51 | 0.35 | 0.50 |
| Unified Models | | | | | | | |
| show-o-512 | 0.28 | 0.40 | 0.48 | 0.30 | 0.46 | 0.30 | 0.35 |
| vila-u-7b-256 | 0.26 | 0.33 | 0.37 | 0.35 | 0.39 | 0.23 | 0.31 |
| Emu3 | 0.34 | 0.45 | 0.48 | 0.41 | 0.45 | 0.27 | 0.39 |
| Janus-1.3B | 0.16 | 0.26 | 0.35 | 0.28 | 0.30 | 0.14 | 0.23 |
| JanusFlow-1.3B | 0.13 | 0.26 | 0.28 | 0.20 | 0.19 | 0.11 | 0.18 |
| Janus-Pro-1B | 0.20 | 0.28 | 0.45 | 0.24 | 0.32 | 0.16 | 0.26 |
| Janus-Pro-7B | 0.30 | 0.37 | 0.49 | 0.36 | 0.42 | 0.26 | 0.35 |
| MetaQuery-B | 0.44 | 0.49 | 0.58 | 0.41 | 0.49 | 0.34 | 0.46 |
| MetaQuery-L | 0.56 | 0.57 | 0.62 | 0.48 | 0.63 | 0.42 | 0.55 |
| MetaQuery-XL | 0.56 | 0.55 | 0.62 | 0.49 | 0.63 | 0.41 | 0.55 |

**Table 5:** Comparison of world knowledge reasoning on WISE.

We also quantitatively evaluate MetaQuery's commonsense reasoning capability on the CommonsenseT2I benchmark. Results show that MetaQuery significantly improves the performance of the base Sana model, achieving SOTA performance.

| **Methods** | **w/o Neg. Prompt** | **w/ Neg. Prompt** |
| --- | --- | --- |
| DALL-E 3 w/ rewrite | 40.17 | N/A |
| SD-XL | 26.00 | 44.83 |
| SD-3-medium | 26.17 | 47.17 |
| FLUX.1-dev | 24.50 | 22.50 |
| Sana-1.6B | 25.17 | 43.33 |
| MetaQuery-B | 27.33 | 51.50 |
| MetaQuery-L | 28.83 | 57.67 |

**Table 6:** Comparison of visual commonsense reasoning capability on CommonsenseT2I.

# Discussion

While our learnable queries approach matches the image quality of using LLM's last layer embeddings, the latter treats the LLM merely as a text encoder, limiting in-context learning. As shown in Figure 9 and confirmed by WiScore and CommonsenseT2I benchmarks, MetaQuery significantly outperforms the last layer embedding approach by natively integrating with the LLM to leverage its reasoning capabilities for generating appropriate images.

| **Methods** | **MJHQ-30K FID ↓** | **GenEval ↑** | **DPG-Bench ↑** | **WiScore ↑** | **CommonsenseT2I ↑** |
| --- | --- | --- | --- | --- | --- |
| Ours-L w/ Last Layer Embed\* | 6.41 | 0.78 | 81.23 | 0.48 | 52.83 |
| Ours-L w/ MetaQuery | 6.35 | 0.78 | 81.10 | 0.55 | 57.67 |

**Table 7:** Comparison between MetaQuery and LLM last layer embedding. \* denotes that the LLM last layer embeddings of input tokens are used for image generation.

## Conclusion

We presented MetaQueries, a simple interface connecting MLLMs (for understanding) and diffusion decoders (for generation), effective even when the MLLM is frozen. This approach yields state-of-the-art understanding and generation performance with straightforward implementation. By enabling transfer between modalities, MetaQueries successfully channels MLLM knowledge and reasoning into multimodal generation. While effective, we hypothesize that bridging the remaining gap to leading proprietary systems may primarily involve further data scaling. We hope MetaQueries provides a powerful, accessible baseline for future unified multimodal model development.



### BibTeX

@article{pan2025transfer,  
  title={Transfer between Modalities with MetaQueries},  
  author={Pan, Xichen and Shukla, Satya Narayan and Singh, Aashu and Zhao, Zhuokai and Mishra, Shlok Kumar and Wang, Jialiang and Xu, Zhiyang and Chen, Jiuhai and Li, Kunpeng and Juefei-Xu, Felix and Hou, Ji and Xie, Saining},  
  journal={arXiv preprint arXiv:2504.06256},  
  year={2025}  
}

### Footnotes






[Privacy](https://opensource.fb.com/legal/privacy)
 | 
[Terms](https://opensource.fb.com/legal/terms)

Copyright © 2025 Meta Platforms, Inc
