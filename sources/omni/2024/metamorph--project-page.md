# MetaMorph: Multimodal Understanding and Generation via Instruction Tuning
Source: https://tsb0601.github.io/metamorph/
MetaMorph: Multimodal Understanding and Generation via Instruction Tuning



# MetaMorph

## Multimodal Understanding and Generation via Instruction Tuning

We demonstrate that Large Language Models (LLMs) can be effectively finetuned into unified multimodal models capable of both understanding and generation using instruction tuning.

LLMs are already **VERY CLOSE** to being Unified Multimodal Models!

[arXiv Paper](https://arxiv.org/abs/2412.14164v1)
[GitHub Code](https://github.com/facebookresearch/metamorph/)

![MetaMorph Overview Teaser](static/img/metamorph_teaser.webp)

[Shengbang Tong1,2,\*,†](https://tsb0601.github.io/petertongsb/)  
[David Fan1](https://davidfan.io/)  
[Jiachen Zhu1,2,\*](https://jiachenzhu.github.io/)  
[Yunyang Xiong3](https://pages.cs.wisc.edu/~yunyang/)  
[Xinlei Chen1](https://xinleic.xyz/)  
  
[Koustuv Sinha1](https://koustuvsinha.com/)  
[Michael Rabbat1](https://ai.meta.com/people/1148536089838617/michael-rabbat/)  
[Yann LeCun1,2](https://yann.lecun.com/)  
[Saining Xie2](https://www.sainingxie.com/)  
[Zhuang Liu1,†](https://liuzhuang13.github.io/)

[1FAIR, Meta](https://fair.meta.com/)  
[2New York University](https://cs.nyu.edu/home/index.html)  
[3Meta Reality Labs](#)

\*Work done at Meta  
†Corresponding authors

## News & Updates

April 14, 2025

Training Code Released!

We release of the MetaMorph training code. You can find it on our [GitHub repository](https://github.com/facebookresearch/metamorph/). Explore the code and experiment with Visual-Predictive Instruction Tuning!

## Abstract

We extend Visual Instruction Tuning to **Visual-Predictive Instruction Tuning (VPiT)** to study unified multimodal models. This simple yet effective approach enables LLMs to predict both visual and text tokens through instruction tuning, without requiring extensive architectural changes or pretraining.

1

We discover that **generation and understanding are mutually beneficial**. Through extensive experiments, we reveal that visual generation emerges naturally as models improve at understanding—requiring as little as 200K samples when co-trained, compared to millions needed traditionally.

2

Our **Visual-Predictive Instruction Tuning (VPiT)** extends existing instruction tuning to predict continuous visual tokens alongside discrete text tokens. This simple modification unlocks powerful multimodal capabilities while maintaining the efficiency of instruction tuning.

3

We train the **MetaMorph** model using VPiT, achieving competitive performance across benchmarks. More importantly, we find intriguing evidence of modality unification: the model can leverage LLM knowledge for generation and perform implicit reasoning before generating visual tokens.

## MetaMorph Examples

See our unified multimodal model performing various tasks, including understanding, generation, and implicit reasoning.

![MetaMorph Demo GIF](static/img/examples.gif)

### Multimodal Understanding & Generation

Watch as MetaMorph handles both visual understanding and generation tasks after instruction tuning.

## Key Findings

Visual Understanding and Visual Generation are Coupled!

Finding 1

Visual Generation Emerges Naturally From Understanding

Only a small number of samples are needed to unlock visual generation when co-training with understanding tasks.

↓

![Data Efficiency Comparison Graph](static/img/fid_special_points_plot_new.jpg)

Visual generation capability can be unlocked with significantly less data when co-trained with visual understanding tasks. Our experiments show that 5,000 examples are enough to trigger visual generation, and 200K samples are sufficient to generate high-quality visual tokens when combined with understanding tasks, compared to millions needed for pure generation training.

Finding 2

Visual Understanding and Generation are Synergistic

Better understanding leads to better generation, and vice versa.

↓

![Understanding-Generation Correlation Graph](static/img/understanding_generation.PNG)

There exists a strong correlation between visual understanding and generation capabilities. As models improve their understanding abilities (e.g., VQA scores), their generation capabilities (e.g., lower FID scores) naturally enhance, and vice versa, creating a powerful synergistic effect.

Finding 3

Understanding Data Boosts Both Capabilities More Effectively

Understanding data significantly improves both understanding and generation performance compared to generation data alone.

↓

![Data Impact Comparison Heatmap](static/img/heatmap.PNG)

The darker the heatmap cell, the better the performance. Understanding data proves to be significantly more valuable than generation data for improving both understanding (e.g., MMBench) and generation (e.g., FID) tasks. For example, with the same total data amount (5M samples), using 4M VQA + 1M Generation data yields better results on both task types than using 1M VQA + 4M Generation data.

Finding 4

Visual Generation Aligns With Visually Demanding Tasks

Generation ability strongly correlates with general, text & chart, and vision-centric tasks, but less so with knowledge-based tasks.

↓

![Task Correlation Analysis Graph](static/img/benchmark_analysis.PNG)

Visual generation capabilities (measured by FID) show strong correlation with visually demanding understanding tasks (like MMBench-General, MMBench-V&C, MMBench-VisionCentric) but weaker correlation with knowledge-based tasks (MMBench-Knowledge). This suggests that visual understanding and generation are fundamental visual capabilities intertwined within autoregressive models.

## Visual Predictive Instruction Tuning (VPiT)

A simple yet effective extension enabling LLMs to predict both visual and text tokens.

Multimodal Input

Process visual (image/video frames) and text tokens in any sequence order.

Unified Processing

LLM backbone with separate, lightweight text and vision prediction heads.

Token Generation

Generate text tokens (via softmax) and continuous visual tokens (via projection). Visualize visual tokens using a diffusion model.

Training Process

Multimodal next-token prediction with instruction tuning.

↓

VPiT extends visual instruction tuning with:

* **Multimodal Input Processing:**
  + Visual inputs (images/frames) processed through a pretrained vision encoder (e.g., SigLIP).
  + Features are interpolated to a fixed number of visual tokens (e.g., 64).
  + A trainable projection layer matches visual token dimensions to the LLM's embedding space.
* **Model Architecture:**
  + Uses a standard LLM backbone (e.g., LLaMA).
  + Adds two lightweight prediction heads on top of the LLM's output embeddings:
  + *Language Head:* Standard linear layer for text token prediction (trained with cross-entropy loss).
  + *Vision Head:* MLP projecting LLM embeddings back to the vision encoder's feature dimension (trained with cosine similarity loss against ground truth visual tokens).
  + Only the LLM, adapter layers, and prediction heads are trained.
* **Token Prediction:**
  + Predicts the next token autoregressively, whether text or visual.
  + Uses cross-entropy loss for text tokens via the language head.
  + Uses cosine similarity loss for visual tokens via the vision head.
  + Special tokens `<image_start>` and `<image_end>` delineate visual token sequences.
  + Loss is only calculated for response tokens (masked inputs).
* **Unified Framework:**
  + Maintains the efficiency of instruction tuning.
  + Handles interleaved text and visual inputs/outputs naturally.
  + Requires minimal architectural changes to existing LLMs.

![VPiT Training Process Diagram](static/img/VPT.png)

Training Data Types

Utilizes a broad range of multimodal data formatted as instructions.

↓

![Data Categories Diagram](static/img/data.png)

Three major data categories are formatted into instruction-tuning pairs:

* **Visual Understanding Data:**
  + ImageQA: Utilizes the Cambrian-7M collection (LLaVA, ShareGPT4V, etc.).
  + VideoQA: Includes VideoStar and ShareVideo datasets (processed at 1 FPS).
  + Format: `Prompt: {<visual_tokens>, <text prompt>}`, `Response: {<text response>}`
* **Visual Generation Data:**
  + Image-Text Pairs: Up to 5M pairs from the MetaCLIP pipeline, curated into instruction format.
  + Format: `Prompt: {<text prompt>}`, `Response: {"Here is an image...", <image_start>, <visual_tokens>, <image_end>}`
* **Other Visual Data:**
  + Video Data (HowTo100M, SomethingSomethingV2): Formatted for tasks like frame prediction, sequence completion, and temporal reasoning.
  + Visual Thinking Data (Visual CoT, VStar): Includes visual generation within reasoning steps (e.g., generating zoomed views).
  + Image-to-Image Data (InstructPix2Pix, Aurora): For conditioned image transformation tasks.

Visual Token Visualization

A diffusion-based approach translates predicted visual tokens into images.

↓

![Token Visualization Pipeline Diagram](static/img/diffusion.png)

To visualize the continuous visual tokens predicted by MetaMorph:

* **Training Stage (Diffusion Autoencoder):**
  + We finetune an existing diffusion model (Stable Diffusion 1.5) to act as a visual decoder.
  + It's trained to reconstruct images conditioned on the visual tokens produced by the *frozen* pretrained vision encoder (SigLIP).
  + A simple MLP projector matches SigLIP embedding dimensions to the diffusion model's cross-attention dimension.
  + Trained on held-out image-text data using standard latent diffusion objectives.
* **Inference Pipeline:**
  + **Step 1 (MetaMorph Prediction):** The MetaMorph model processes the input prompt and generates a sequence of continuous visual tokens via its vision head.
  + **Step 2 (Token Visualization):** These predicted visual tokens are fed into the finetuned diffusion model (trained in the previous stage), conditioning the diffusion process to generate the final pixel-space image.

**Note:** This visualization step is primarily for analysis and demonstrating the model's capabilities, not for competing with state-of-the-art high-fidelity image generation models.

## MetaMorph Model

A unified model demonstrating true multimodal capabilities through VPiT.

Competitive Performance

Strong results across understanding and generation benchmarks using LLaMA-3.1 8B.

↓

| Model | | Image QA | | | | | | | | | Video QA | Generation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Method | Base LLM | MMBenchEN | SEED | RealWorldQA | MMVP | SQA | MMMU | VStar | ChartQA | TextVQA | MV-Bench | FID ↓ |
| GPT-4V\* | - | 75.8 | 69.1 | 61.4 | 50.0 | 75.7 | 56.8 | 55.0 | 78.5 | 78.0 | 43.5 | - |
| *T2I Models* | | | | | | | | | | | | |
| Stable Diffusion 1.5\* | - | - | - | - | - | - | - | - | - | - | - | 9.6 |
| Dalle 2\* | - | - | - | - | - | - | - | - | - | - | - | 10.4 |
| Imagen\* | - | - | - | - | - | - | - | - | - | - | - | 7.3 |
| *Unified Models* | | | | | | | | | | | | |
| EMU-3\* | - | 58.5 | 68.2 | 57.4 | 36.6† | 89.2 | 31.6 | 51.8† | 68.6 | 64.7 | - | 12.8 |
| Janus\* | DeepSeek 1.3B | 69.4 | 63.7 | - | - | - | 30.5 | - | - | - | - | 8.5 |
| VILA-U256† | LLaMA-2 7B | 66.6 | 57.1 | 46.6 | 22.0 | 67.1 | 32.2 | 38.7 | 11.4 | 48.3\* | 40.8 | 19.6 |
| Transfusion\* | - | - | - | - | - | - | - | - | - | - | - | 6.7 |
| Chameleon-7B† | - | 35.7 | 27.2 | 19.6 | 0.0 | 50.3 | 28.4 | 37.1 | 0.0 | 0.0 | - | 26.7\* |
| **MetaMorph (Ours)** | **LLaMA-3.1 8B** | **75.2** | **71.8** | **58.3** | **48.3** | **83.2** | **41.8** | **44.0** | **37.1** | **60.5** | **48.8** | **11.8** |

**Table 1:** Comparison with state-of-the-art models on various benchmarks. MetaMorph achieves competitive performance across both understanding and generation tasks. (\*): Numbers reported in original papers. (†): Results reproduced using released weights. FID is measured on MS-COCO 2014 validation set (lower is better).

MetaMorph demonstrates strong performance across a wide range of tasks, achieving results competitive with or superior to other open-source unified models of similar size. Notably, it performs well on both complex visual understanding benchmarks (like MMBench, SEED, MMMU) and shows reasonable visual generation quality (FID score), despite using only 64 tokens per image/frame and relying solely on instruction tuning without extensive pretraining stages common in other models.

LLM Knowledge Leverage

Successfully utilizes pretrained LLM knowledge for visual generation.

↓

MetaMorph demonstrates the ability to leverage the knowledge and capabilities embedded within the pretrained language model for visual generation tasks:

* It can generate accurate visual representations for specialized concepts like "Chhogori" (K2 mountain), "Oncilla" (wild cat), and "Chizarira" (national park), tapping into the LLM's broad world knowledge.
* The model exhibits nuanced semantic understanding, correctly visualizing prompts involving negation ("a glass without water") or complex relationships.
* This transfer of knowledge allows MetaMorph to generate meaningful visuals for a wider range of concepts than models relying solely on paired image-text data.

These examples suggest that unifying language and vision allows visual generation to be guided by the linguistic reasoning and background knowledge inherent in LLMs.

←
Example 1/5
→

![Generated image of Chhogori (K2)](static/img/chhogori.png)

#### Prompt:

Generate an image of Chhogori

#### Explanation:

Chhogori, also known as K2, is the second-highest mountain. The model uses its knowledge to generate the correct mountain.

![Generated image of an Oncilla](static/img/oncilla.png)

#### Prompt:

Generate an image of an Oncilla

#### Explanation:

The oncilla is a small spotted cat. The model accesses its knowledge base to visualize this specific animal.

![Generated image of Chizarira National Park view](static/img/chizarira.png)

#### Prompt:

Generate an image of the view of Chizarira

#### Explanation:

Chizarira is a national park in Zimbabwe. The model generates a plausible landscape view based on this geographic knowledge.

![Generated image of an empty glass](static/img/emptyglass.png)

#### Prompt:

Generate an image of a glass without water

#### Explanation:

MetaMorph correctly interprets the negation and generates an empty glass, demonstrating semantic understanding.

![Generated image of a glass full of water](static/img/fullglass.png)

#### Prompt:

Generate an image of a glass filled with water

#### Explanation:

Contrasting the previous example, the model accurately generates a glass containing water when negation is removed.

Multimodal Reasoning Capabilities

Demonstrates implicit reasoning within multimodal generation tasks.

↓

MetaMorph exhibits reasoning capabilities during generation, going beyond simple text-to-image mapping. Similar to how LLMs might precompute reasoning steps internally before generating text, MetaMorph appears to perform implicit reasoning before generating visual tokens:

* The model can decompose complex, multi-step prompts and implicitly solve them. For instance, given "Generate an image of the animal resulting from a monarch caterpillar's metamorphosis", MetaMorph internally reasons (caterpillar → metamorphosis → butterfly) and generates a butterfly image without explicit step-by-step instructions.
* It handles prompts requiring world knowledge and logical deduction, like identifying the US flag from "Generate an image of the national flag of the country where Yellowstone National Park is located".
* This implicit reasoning occurs without explicit chain-of-thought prompting, suggesting the model integrates reasoning directly into the generation process.

These capabilities highlight the potential of unified models like MetaMorph to perform more complex, compositional tasks by leveraging the underlying LLM's reasoning abilities.

←
Example 1/4
→

"Generate an image of the animal resulting from a monarch caterpillar's metamorphosis"

![Generated Monarch Butterfly](static/img/butterfly.png)

Model's Implicit Reasoning Process

1

2

3

Input

Identifies starting subject: monarch caterpillar.

Process

Applies knowledge of the 'metamorphosis' process.

Output

Determines the result: monarch butterfly. Generates image.

"Generate an image of the national flag of the country where Yellowstone National Park is located"

![Generated American Flag](static/img/usa.png)

Model's Implicit Reasoning Process

1

2

3

Location ID

Identifies Yellowstone National Park.

Country Link

Connects Yellowstone to the United States using geographic knowledge.

Symbol Retrieval

Retrieves the national symbol (flag) for the USA. Generates image.

"Generate an image of the flower celebrated in spring festivals in the country where sushi originated"

![Generated Cherry Blossoms](static/img/cherryblossom.png)

Model's Implicit Reasoning Process

1

2

3

Origin ID

Identifies sushi origin: Japan.

Cultural Link

Connects Japan, spring festivals, and celebrated flower: Cherry Blossom (Sakura).

Image Generation

Generates image of cherry blossoms.

"Generate an image of the pet animal whose name is a rearrangement of the letters in the word 'tca'"

![Generated Cat](static/img/tca.png)

Model's Implicit Reasoning Process

1

2

3

Anagram

Rearranges 'tca' to 'cat'.

Category ID

Identifies 'cat' as a common 'pet animal'.

Image Generation

Generates image of a cat.
