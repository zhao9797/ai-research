# Kosmos-G Project Page (xichenpan.github.io/kosmosg)

Kosmos-G: Generating Images in Context with Multimodal Large Language Models 

 More Research

 MetaLM

 Kosmos-1

 Kosmos-2

 Kosmos-2.5

 Kosmos-G : Generating Images in
 Context with Multimodal Large Language Models 

 Xichen Pan 1,2 , 

 Li Dong 1 , 

 Shaohan Huang 1 ,

 Zhiliang Peng 1 ,

 Wenhu Chen 3 ,

 Furu Wei 1 

 1 Microsoft Research, 
 2 New York University, 
 3 University of Waterloo 

 Paper 

 Code 

 ICLR 2024

 Zero-shot image generation examples with multimodal prompts. Kosmos-G 
 regards all image inputs as a “foreign language”. It can perceive generalized vision-language inputs
 that span multiple images and faithfully generate images.

 Abstract 

 Recent advancements in text-to-image (T2I) and vision-language-to-image (VL2I) generation have made
 significant strides. However, the generation from generalized vision-language inputs, especially
 involving multiple images, remains under-explored. This paper presents Kosmos-G , a model that leverages the advanced perception capabilities of
 Multimodal Large Language Models (MLLMs) to tackle the aforementioned challenge. Our approach aligns
 the output space of MLLM with CLIP using the textual modality as an anchor and performs
 compositional instruction tuning on curated data. Kosmos-G demonstrates
 a unique capability of zero-shot multi-entity subject-driven generation. Notably, the score
 distillation instruction tuning requires no modifications to the image decoder. This allows for a
 seamless substitution of CLIP and effortless integration with a myriad of U-Net techniques ranging
 from fine-grained controls to personalized image decoder variants. We posit Kosmos-G 
 as an initial attempt towards the goal of "image as a foreign language in image generation."

 Approch 

 Kosmos-G is a model that can perceive general modalities, follow
 instructions, and generate image conditions.
 It comprises an MLLM for multimodal perception, coupled with an AlignerNet that bridges the MLLM to the
 diffusion U-Net image decoder. Kosmos-G can pass the fine concept-level
 guidance from interleaved input to image decoder, and offer a seamless alternative to CLIP.
 Specifically, the backbone of Kosmos-G MLLM is a Transformer-based causal
 language model, serving as a general-purpose interface to multimodal input. We train Kosmos-G following an "align before instruct" manner, the entire training
 pipeline can be divided into 3 stages:

 Multimodal Language Modeling : We pre-train the MLLM on multimodal corpora,
 including monomodal data, cross-modal paired data, and interleaved multimodal data with language
 modeling loss following Kosmos-1 .
 Image Decoder Aligning : We use the U-Net of Stable Diffusion v1.5 as our image
 decoder. We trained an AlignerNet on only textual data to align the output space of Kosmos-G to U-Net's input space through CLIP supervision. Here,
 the language acts as the anchoring modality, ensuring image input is also compatible with the
 image decoder.
 Instruction Tuning : We further fine-tune Kosmos-G 
 through a compositional generation task on curated data, with the differentiable gradient passed
 from the frozen U-Net.

 We construct a large-scale dataset based on OpenImage V7 for instruction tuning, which contains around 9
 million images.

 Results 

 Kosmos-G demonstrates a unique capability of zero-shot multi-entity
 subject-driven generation.

 Kosmos-G can seamlessly substitute CLIP and effortlessly integrate with
 a myriad of U-Net techniques such as fine-grained controls by ControlNet.

 Kosmos-G can also work perfectly with customized image decoder variants.
 Left: with standard U-Net. Right: with LoRA fine-tuned U-Net.

 Disclaimer 
 Kosmos-G is purely a research project. Currently, we have no plans to incorporate Kosmos-G into a product or expand access to the public. We will also put Microsoft AI principles into practice when further developing the models.

 In our research paper, we account for the ethical concerns associated with text-to-image research. To mitigate issues associated with training data, we have implemented a rigorous filtering process to purge our training data of inappropriate content, such as explicit imagery and offensive language, to minimize the likelihood of generating inappropriate content.

 BibTeX 
 @article{kosmos-g,
 author = {Pan, Xichen and Dong, Li and Huang, Shaohan and Peng, Zhiliang and Chen, Wenhu and Wei, Furu},
 journal = {ArXiv preprint},
 title = {Kosmos-G: Generating Images in Context with Multimodal Large Language Models},
 url = {https://arxiv.org/abs/2310.02992},
 volume = {abs/2310.02992},
 year = {2023}
} 

 -->

 We thank the authors of Nerfies that kindly open sourced the template of this website.