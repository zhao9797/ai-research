Language Model Beats Diffusion: Tokenizer is Key to Visual Generation 
 Language Model Beats Diffusion : Tokenizer is key to visual generation 
 Lijun Yu ‡† , José Lezama † , Nitesh B. Gundavarapu † , Luca Versari † , Kihyuk Sohn † , David Minnen † , Yong Cheng † , Agrim Gupta † , Xiuye Gu † , Alexander G. Hauptmann ‡ , Boqing Gong † , Ming-Hsuan Yang † , Irfan Essa † , David A. Ross † , Lu Jiang † 
 † Google, ‡ Carnegie Mellon University 
 While Large Language Models (LLMs) are the dominant models for generative tasks in language, they do not perform as well as diffusion models on image and video generation. To effectively use LLMs for visual generation, one crucial component is the visual tokenizer that maps pixel-space inputs to discrete tokens appropriate for LLM learning. In this paper, we introduce MAGVIT-v2, a video tokenizer designed to generate concise and expressive tokens for both videos and images using a common token vocabulary. Equipped with this new tokenizer, we show that LLMs outperform diffusion models on standard image and video generation benchmarks including ImageNet and Kinetics. In addition, we demonstrate that our tokenizer surpasses the previously top-performing video tokenizer on two more tasks: (1) video compression comparable to the next-generation video codec (VCC) according to human evaluations, and (2) learning effective representations for action recognition tasks.
 Research Paper 
 Video Generation 
 MAGVIT-v2 tokenizer is the core technique that enables VideoPoet: A large language model for zero-shot video generation . More . 
 ❮ 
 ❯ 
 Video Compression 
 Comparison with prior best model and standard video codec. 
 Human rater study results. 
 Comparison with prior best model and standard video codec (GIF format for easier sharing, which takes longer to load). 
 ❮ 
 ❯ 
 Image Generation 
 -->
 Comparison with prior works on ImageNet 512x512. 
 Reconstruction and generation quality curves regarding the vocabulary size on ImageNet 128x128. 
 -->
 "lorikeet" 
 -->
 "volcano" 
 ❮ 
 ❯ 
 Image Tokenization 
 Comparison with prior works. 
 ❮ 
 ❯ 
 -->
 While we're still updating this new version, also check out: MAGVIT(v1) 
 -->
 Acknowledgment 
 -->
