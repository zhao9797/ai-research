# [2305.18295] RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths
Source: https://ar5iv.labs.arxiv.org/html/2305.18295
[2305.18295] RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths



# RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths

Zeyue Xue111Equal contribution. Work done during Zeyue’s internship at SenseTime Research.
  
The University of Hong Kong
  
xuezeyue@connect.hku.hk
  
&Guanglu Song111Equal contribution. Work done during Zeyue’s internship at SenseTime Research.
  
SenseTime Research
  
songguanglu@sensetime.com
  
&Qiushan Guo
  
The University of Hong Kong
  
qsguo@cs.hku.hk
  
&Boxiao Liu
  
SenseTime Research
  
liuboxiao@sensetime.com
  
&Zhuofan Zong
  
SenseTime Research
  
zongzhuofan@gmail.com
  
&Yu Liu222Project lead.  333Corresponding authors.
  
SenseTime Research
  
liuyuisanai@gmail.com
  
&Ping Luo333Corresponding authors.
  
The University of Hong Kong
  
pluo@cs.hku.hk

###### Abstract

Text-to-image generation has recently witnessed remarkable achievements. We
introduce a text-conditional image diffusion model, termed RAPHAEL, to generate highly artistic images, which accurately portray the text prompts, encompassing multiple nouns, adjectives, and verbs. This is achieved by stacking tens of mixture-of-experts (MoEs) layers, *i.e.,* space-MoE and time-MoE layers, enabling billions of diffusion paths (routes) from the network input to the output. Each path intuitively functions as a “painter” for depicting a particular textual concept onto a specified image region at a diffusion timestep. Comprehensive experiments reveal that RAPHAEL outperforms recent cutting-edge models, such as Stable Diffusion, ERNIE-ViLG 2.0, DeepFloyd, and DALL-E 2, in terms of both image quality and aesthetic appeal. Firstly, RAPHAEL exhibits superior performance in switching images across diverse styles, such as Japanese comics, realism, cyberpunk, and ink illustration. Secondly, a single model with three billion parameters, trained on 1,000

10001,000 A100 GPUs for two months, achieves a state-of-the-art zero-shot FID score of 6.616.616.61 on the COCO dataset. Furthermore, RAPHAEL significantly surpasses its counterparts in human evaluation on the ViLG-300 benchmark. We believe that RAPHAEL holds the potential to propel the frontiers of image generation research in both academia and industry, paving the way for future breakthroughs in this rapidly evolving field. More details can be found on a webpage:
<https://raphael-painter.github.io/>444More creations can be found in <https://miaohua.sensetime.com/zh-CN/picture-selection>. Please select the Artist v0.3.0 Beta model to generate. This is our latest version based on RAPHAEL. This information was last updated on Sept. 19th, 2023..

*“When one is painting one does not think.”*

*— Raffaello Sanzio da Urbino*

## 1 Introduction

Recent advancements in text-to-image generators, such as Imagen [saharia2022photorealistic](#bib.bib1) , Stable Diffusion [rombach2022high](#bib.bib2) , DALL-E 2 [ramesh2022hierarchical](#bib.bib3) , eDiff-I [balaji2022ediffi](#bib.bib4) , and ERNIE-ViLG 2.0 [feng2022ernie](#bib.bib5) , have yielded remarkable success and found wide applications in computer graphics, culture and art, and the generation of medical and biological data.

![Refer to caption](/html/2305.18295/assets/x1.png)


Figure 1: Comparisons of RAPHAEL with recent representative generators, Stable Diffusion XL [rombach2022high](#bib.bib2) , DeepFloyd, DALL-E 2 [ramesh2022hierarchical](#bib.bib3) , and ERNIE-ViLG 2.0 [feng2022ernie](#bib.bib5) . They are given the same prompts, where the words that the human artists yearn to preserve within the generated images are highlighted in red. These images are not cherry-picked. We see that previous models often fail to preserve the desired concepts. For example, only the RAPHAEL-generated images precisely reflect the prompts such as “pearl earring, Vermeer”, “playing soccer”, “five cars”, “black
high-waisted
trouser”, “white hair, manga, moon”, and “sign, RAPHAEL”, while other models generate compromised results. Better zoom in 200%.

Despite the substantial progress made in text-to-image diffusion models [saharia2022photorealistic](#bib.bib1) ; [rombach2022high](#bib.bib2) ; [ramesh2022hierarchical](#bib.bib3) ; [balaji2022ediffi](#bib.bib4) ; [feng2022ernie](#bib.bib5) , there remains a pressing need for research to further
achieve more precise alignment between text and image. As illustrated in Fig.[1](#S1.F1 "Figure 1 ‣ 1 Introduction ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), existing models often fail to adequately preserve textual concepts within the generated images.
This is primarily due to the reliance on a classic cross-attention mechanism for integrating text descriptions into visual representations, resulting in relatively coarse control of the diffusion process, and leading to compromised results.

To address this issue, we introduce RAPHAEL, a text-to-image generator, which yields images with superior artistry and fidelity compared to prior work, as demonstrated in Fig.[2](#S1.F2 "Figure 2 ‣ 1 Introduction ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").
RAPHAEL, an acronym that stands for “distinct image regions align with different text phases in attention learning”,
offers an appealing benefit not found in existing approaches.

Specifically, we observe that different text concepts influence distinct image regions during the generation process [hertz2022prompt](#bib.bib6) ,
and the conventional cross-attention layer
often struggles to preserve these varying concepts adequately in an image.
To mitigate this issue,
we employ a diffusion model stacking tens of mixture-of-experts (MoE) layers [shazeer2017outrageously](#bib.bib7) ; [fedus2022switch](#bib.bib8) , including both space-MoE and time-MoE layers. Concretely, the space-MoE layers are responsible for depicting different concepts in specific image regions, while the time-MoE layers focus on painting these concepts at different diffusion timesteps.

![Refer to caption](/html/2305.18295/assets/x2.png)


Figure 2: These examples show that RAPHAEL can generate artistic images with varying text prompts across various styles. The synthesized images have rich details and semantics. The prompts were written by human artists without
cherry-picking.

This configuration leads to billions of diffusion paths from the network input to the output. Naturally, each path can act as a “painter” responsible for rendering a particular concept to an image region at a specific timestep.
The result is a more precise alignment between text tokens and image regions, enabling the generated images that accurately represent the associated text prompt.
This approach sets RAPHAEL apart from existing models and even sheds light on future studies of the explainability of the generation process.
Additionally, we propose an edge-supervised learning module to further enhance the image quality and aesthetic appeal of the generated images.

Extensive experiments demonstrate that RAPHAEL outperforms preceding approaches, such as Stable Diffusion, ERNIE-ViLG 2.0, DeepFloyd, and DALL-E 2.
(1) RAPHAEL exhibits superior performance in switching images across diverse styles, such as Japanese comics, realism, cyberpunk, and ink illustration.
(2) RAPHAEL establishes a new state-of-the-art with a zero-shot FID-30k score of 6.616.616.61 on the COCO dataset.
(3) RAPHAEL, a single model with three billion parameters trained on 1,000

10001,000 A100 GPUs, significantly surpasses its counterparts in human evaluation on the ViLG-300 benchmark.
(4) RAPHAEL is capable of generating images with resolutions up to 4096×6144409661444096\times 6144 with rich image contents and details, when combined with a tailor-made SR-GAN model [wang2021real](#bib.bib9) .

The contributions of this work are three-fold: (i) We propose a novel text-to-image generator, RAPHAEL, which, through the implementation of several carefully-designed techniques, generates images that more accurately reflect textual prompts than previous works.
(ii) We thoroughly explore RAPHAEL’s potential for switching images in diverse styles, such as Japanese comics, realism, cyberpunk, and ink illustration, and for extension using LoRA [hu2021lora](#bib.bib10) , ControlNet [zhang2023adding](#bib.bib11) , and SR-GAN [wang2021real](#bib.bib9) .
(iii) We have released the demo of the latest version of RAPHAEL to the public, which has been fine-tuned on more high aesthetics datasets. We believe that RAPHAEL holds the potential to advance the frontiers of image generation in both academia and industry, paving the way for
future breakthroughs in this rapidly evolving field.

## 2 Notation and Preliminary

We present the necessary notations and the Denoising Diffusion Probabilistic Model (DDPM) [ho2020denoising](#bib.bib12)  for text-to-image generation. Given a collection of N𝑁N images, denoted as {𝐱i}i=1Nsuperscriptsubscriptsubscript𝐱𝑖𝑖1𝑁\{\mathbf{x}\_{i}\}\_{i=1}^{N}, the aim is to learn a generative model, p​(𝐱)𝑝𝐱p(\mathbf{x}), that is capable of accurately representing the underlying distribution.

In forward diffusion, Gaussian noise is progressively introduced into the source images.
At an arbitrary timestep t𝑡t, it is possible to directly sample from the Gaussian distribution following the T𝑇T-step noise schedule {αt}t=1Tsuperscriptsubscriptsubscript𝛼𝑡𝑡1𝑇\{\alpha\_{t}\}\_{t=1}^{T}, without iterative forward sampling. Consequently, the noisy image at timestep t𝑡t, denoted as 𝐱tsubscript𝐱𝑡\mathbf{x}\_{t}, can be expressed as 𝐱t=1−α¯t​𝐱0+α¯t​ϵtsubscript𝐱𝑡1subscript¯𝛼𝑡subscript𝐱0subscript¯𝛼𝑡subscriptitalic-ϵ𝑡\mathbf{x}\_{t}=\sqrt{1-\bar{\alpha}\_{t}}\mathbf{x}\_{0}+\sqrt{\bar{\alpha}\_{t}}\mathbf{\epsilon}\_{t}, where α¯t=∏i=1tαisubscript¯𝛼𝑡superscriptsubscriptproduct𝑖1𝑡subscript𝛼𝑖\bar{\alpha}\_{t}=\prod\_{i=1}^{t}\alpha\_{i}. In this expression, 𝐱0subscript𝐱0\mathbf{x}\_{0} represents the source image, while ϵt∼𝒩​(0,I)similar-tosubscriptitalic-ϵ𝑡𝒩0𝐼\epsilon\_{t}\sim\mathcal{N}(0,I) indicates the Gaussian noise at step t𝑡t. In the reverse process, a denoising neural network, denoted as Dθ​(⋅)subscript𝐷𝜃⋅D\_{\theta}(\cdot), is employed to estimate the additive Gaussian noise. The optimization of this network is achieved by minimizing the loss function, ℒdenoise=𝔼t,𝐱0,ϵ∼𝒩​(0,I)​[‖ϵ−Dθ​(𝐱t,t)‖22]subscriptℒdenoisesubscript𝔼similar-to

𝑡subscript𝐱0italic-ϵ
𝒩0𝐼delimited-[]superscriptsubscriptnormitalic-ϵsubscript𝐷𝜃subscript𝐱𝑡𝑡22\mathcal{L}\_{\operatorname{denoise}}=\mathbb{E}\_{t,\mathbf{x}\_{0},\epsilon\sim\mathcal{N}(0,I)}\left[\left\|\epsilon-D\_{\theta}\left(\mathbf{x}\_{t},t\right)\right\|\_{2}^{2}\right].

By employing the Bayes’ theorem, it is feasible to iteratively estimate the image at timestep t−1𝑡1t-1 through sampling from the posterior distribution, pθ​(𝐱t−1|𝐱t)subscript𝑝𝜃conditionalsubscript𝐱𝑡1subscript𝐱𝑡p\_{\theta}(\mathbf{x}\_{t-1}|\mathbf{x}\_{t}).
We have 𝐱t−1=1αt​(𝐱t−1−αt1−α¯t​Dθ​(𝐱t,t))+σt​zsubscript𝐱𝑡11subscript𝛼𝑡subscript𝐱𝑡1subscript𝛼𝑡1subscript¯𝛼𝑡subscript𝐷𝜃subscript𝐱𝑡𝑡subscript𝜎𝑡𝑧\mathbf{x}\_{t-1}=\frac{1}{\sqrt{\alpha\_{t}}}\left(\mathbf{x}\_{t}-\frac{1-\alpha\_{t}}{\sqrt{1-\bar{\alpha}\_{t}}}D\_{\theta}\left(\mathbf{x}\_{t},t\right)\right)+\sigma\_{t}z, where σtsubscript𝜎𝑡\sigma\_{t} signifies the standard deviation of the newly injected noise into the image at each step, and z𝑧z represents the Gaussian noise.

In essence, the denoising neural network estimates the score function at varying time steps, thereby progressively recovering the structure of the image distribution. The fundamental insight provided by the DDPM lies in the fact that the perturbation of data points with noise serves to populate regions of low data density, ultimately enhancing the accuracy of estimated scores. This results in stable training and sampling.

U-Net with Text Prompts.
The denoising network is commonly implemented using a U-Net [ronneberger2015u](#bib.bib13)  architecture, as depicted in Fig.[8](#S7.F8 "Figure 8 ‣ 7.3 Details on Time-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") in Appendix [7.3](#S7.SS3 "7.3 Details on Time-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"). To incorporate textual prompts (denoted by 𝐲𝐲\mathbf{y}) into the U-Net, a text encoder neural network, Eθ​(𝐲)subscript𝐸𝜃𝐲E\_{\theta}(\mathbf{y}), is employed to extract the textual representation. The extracted text tokens are input into the U-Net through a cross-attention layer. The text tokens possess a size of ny×dysubscript𝑛𝑦subscript𝑑𝑦n\_{y}\times d\_{y}, where nysubscript𝑛𝑦n\_{y} represents the number of text tokens, and dysubscript𝑑𝑦d\_{y} signifies the dimension of a text token (*e.g.,* dy=768subscript𝑑𝑦768d\_{y}=768 in [radford2021learning](#bib.bib14) ).

The cross-attention layer can be formulated as attention⁡(𝐐,𝐊,𝐕)=softmax⁡(𝐐𝐊⊤d)​𝐕attention𝐐𝐊𝐕softmaxsuperscript𝐐𝐊top𝑑𝐕\operatorname{attention}(\mathbf{Q},\mathbf{K},\mathbf{V})=\operatorname{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}\right)\mathbf{V}, where 𝐐,𝐊

𝐐𝐊\mathbf{Q},~{}\mathbf{K}, and 𝐕𝐕\mathbf{V} correspond to the query, key, and value matrices, respectively. These matrices are computed as 𝐐=h​(𝐱t)​𝐖xqry,𝐊=Eθ​(𝐲)​𝐖ykeyformulae-sequence𝐐ℎsubscript𝐱𝑡subscriptsuperscript𝐖qry𝑥𝐊subscript𝐸𝜃𝐲subscriptsuperscript𝐖key𝑦\mathbf{Q}=h\left(\mathbf{x}\_{t}\right)\mathbf{W}^{\text{qry}}\_{x},~{}\mathbf{K}=E\_{\theta}(\mathbf{y})\mathbf{W}^{\text{key}}\_{y}, and 𝐕=Eθ​(𝐲)​𝐖yval𝐕subscript𝐸𝜃𝐲subscriptsuperscript𝐖val𝑦\mathbf{V}=E\_{\theta}(\mathbf{y})\mathbf{W}^{\text{val}}\_{y}, where 𝐖xqry∈ℝd×dsubscriptsuperscript𝐖qry𝑥superscriptℝ𝑑𝑑\mathbf{W}^{\text{qry}}\_{x}\in\mathbb{R}^{d\times d} and 𝐖ykey,𝐖yval∈

subscriptsuperscript𝐖key𝑦subscriptsuperscript𝐖val𝑦
absent\mathbf{W}^{\text{key}}\_{y},\mathbf{W}^{\text{val}}\_{y}\in ℝdy×dsuperscriptℝsubscript𝑑𝑦𝑑\mathbb{R}^{d\_{y}\times d} represent the parametric projection matrices for the image and text, respectively. Additionally, d𝑑d denotes the dimension of an image token, h​(𝐱t)∈ℝnx×dℎsubscript𝐱𝑡superscriptℝsubscript𝑛𝑥𝑑h(\mathbf{x}\_{t})\in\mathbb{R}^{n\_{x}\times d} indicates the flattened intermediate representation within the U-Net, with nxsubscript𝑛𝑥n\_{x} being the number of tokens in an image.
A cross-attention map between the text and image, 𝐌=softmax⁡(𝐐𝐊⊤d)∈ℝnx×ny𝐌softmaxsuperscript𝐐𝐊top𝑑superscriptℝsubscript𝑛𝑥subscript𝑛𝑦\mathbf{M}=\operatorname{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d}}\right)\in\mathbb{R}^{n\_{x}\times n\_{y}}, is defined, which plays a crucial role in the proposed approach, as described in the following sections.

![Refer to caption](/html/2305.18295/assets/x3.png)


Figure 3: Framework of RAPHAEL.
(a) Each block contains four primary components including a self-attention layer, a cross-attention layer, a space-MoE layer, and a time-MoE layer. The space-MoE is responsible for depicting different text concepts in specific image regions, while the time-MoE handles different diffusion timesteps. Each block uses edge-supervised cross-attention learning to further improve image quality.
(b) shows details of space-MoE.
For example, given a prompt “a furry bear under sky”, each text token and its corresponding image region (given by a binary mask) are directed through distinct space experts, *i.e.,* each expert learns particular visual features at a region. By stacking several space-MoEs, we can easily learn to depict thousands of text concepts.

## 3 Our Approach

The overall framework of RAPHAEL is illustrated in Fig.[3](#S2.F3 "Figure 3 ‣ 2 Notation and Preliminary ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), with the network configuration details provided in the Appendix [7.1](#S7.SS1 "7.1 Hyper-parameters and Values ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").
Employing a U-Net architecture, the framework consists of 16 transformer blocks, each containing four components: a self-attention layer, a cross-attention layer, a space-MoE layer, and a time-MoE layer. The space-MoE
is responsible for depicting different text concepts in specific image regions at a given scale, while the time-MoE handles different diffusion timesteps.

### 3.1 Space-MoE and Time-MoE

Space-MoE. Regarding the space-MoE layer, distinct text tokens correspond to various regions within an image, as previously mentioned.
For instance, when provided with the prompt “a furry bear under the sky”, each text token and its corresponding image region (represented by a binary mask) are fed into separate experts, as illustrated in Fig.[3](#S2.F3 "Figure 3 ‣ 2 Notation and Preliminary ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")b.
The space-MoE layer’s output is the mean of all experts, calculated using the following formula: 1ny​∑i=1nyeroute⁡(𝐲i)​(h′​(𝐱t)∘𝐌^i)1subscript𝑛𝑦superscriptsubscript𝑖1subscript𝑛𝑦subscript𝑒routesubscript𝐲𝑖superscriptℎ′subscript𝐱𝑡subscript^𝐌𝑖\frac{1}{n\_{y}}\sum\_{i=1}^{n\_{y}}e\_{\operatorname{route}(\mathbf{y}\_{i})}\left(h^{\prime}(\mathbf{x}\_{t})\circ\widehat{\mathbf{M}}\_{i}\right).
In this equation, 𝐌^isubscript^𝐌𝑖\widehat{\mathbf{M}}\_{i} is a binary two-dimensional matrix, indicating the image region the i𝑖i-th text token should correspond to, as shown in Fig.[3](#S2.F3 "Figure 3 ‣ 2 Notation and Preliminary ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")b.
Here, ∘\circ represents hadamard product, and h′​(𝐱t)superscriptℎ′subscript𝐱𝑡h^{\prime}(\mathbf{x}\_{t}) is the features from time-MoE. The gating (routing) function route⁡(𝐲i)routesubscript𝐲𝑖\operatorname{route}(\mathbf{y}\_{i}) returns the index of an expert in the space-MoE,
with {e1,e2,…,ek}subscript𝑒1subscript𝑒2…subscript𝑒𝑘\{e\_{1},e\_{2},\dots,e\_{k}\} being a set of k𝑘k experts.

Text Gate Network. The Text Gate Network is employed to distribute an image region to a specific expert,
as shown in Fig.[3](#S2.F3 "Figure 3 ‣ 2 Notation and Preliminary ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")b.
The function route⁡(𝐲i)=argmax​(softmax⁡(𝒢​(Eθ​(𝐲i))+ϵ))routesubscript𝐲𝑖argmaxsoftmax𝒢subscript𝐸𝜃subscript𝐲𝑖italic-ϵ\operatorname{route}(\mathbf{y}\_{i})=\mathrm{argmax}\left(\operatorname{softmax}\left(\mathcal{G}\left(E\_{\theta}(\mathbf{y}\_{i})\right)+\epsilon\right)\right) is used, where 𝒢:ℝdy↦ℝk:𝒢maps-tosuperscriptℝsubscript𝑑𝑦superscriptℝ𝑘\mathcal{G}:\mathbb{R}^{d\_{y}}\mapsto\mathbb{R}^{k} is a feed forward network, which
uses a text token representation Eθ​(𝐲i)subscript𝐸𝜃subscript𝐲𝑖E\_{\theta}(\mathbf{y}\_{i}) as input and assigns a space expert.
To prevent mode collapse, random noise ϵitalic-ϵ\epsilon is incorporated. The argmaxargmax\mathrm{argmax} function ensures that one expert exclusively handles the corresponding image region for each text token, without increasing computational complexity.

From Text to Image Region.
Recall that 𝐌𝐌\mathbf{M} is the cross-attention map between text and image, where each element, 𝐌j,isubscript𝐌

𝑗𝑖\mathbf{M}\_{j,i}, represents a correspondence value between the j𝑗j-th image token and the i𝑖i-th text token. In the space-MoE,
each entry in the binary mask 𝐌^isubscript^𝐌𝑖\widehat{\mathbf{M}}\_{i} equals “1” if 𝐌j,i≥ηisubscript𝐌

𝑗𝑖subscript𝜂𝑖\mathbf{M}\_{j,i}\geq\eta\_{i}, otherwise “0” if 𝐌j,i<ηisubscript𝐌

𝑗𝑖subscript𝜂𝑖\mathbf{M}\_{j,i}<\eta\_{i}, as illustrated in Fig.[3](#S2.F3 "Figure 3 ‣ 2 Notation and Preliminary ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")b.
A thresholding mechanism is introduced to determine the values in the mask.
The threshold value ηi=α​max⁡(𝐌∗,i)subscript𝜂𝑖𝛼subscript𝐌

∗𝑖\eta\_{i}=\alpha\max(\mathbf{M}\_{\ast,i}) is defined, where max⁡(𝐌∗,i)subscript𝐌

∗𝑖\max(\mathbf{M}\_{\ast,i}) represents the maximum correspondence between text token i𝑖i and all image regions. The hyper-parameter α𝛼\alpha will be evaluated through an ablation study.

Discussions. The insight behind the space-MoE is to effectively model the intricate relationships between text tokens and their corresponding regions in the image, accurately reflecting concepts in the generated images.
As illustrated in Fig.[4](#S3.F4 "Figure 4 ‣ 3.1 Space-MoE and Time-MoE ‣ 3 Our Approach ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), the employment of 16 space-MoE layers, each containing 6 experts, results in billions of spatial diffusion paths (*i.e.,* 616superscript6166^{16} possible routes). It is evident that each diffusion path is closely associated with a specific textual concept.

To investigate this further, we generate 100 prevalent adjectives that are the most frequently occurring adjectives for
describing artworks as suggested by GPT-3.5 [brown2020language](#bib.bib15) ; [ouyang2022training](#bib.bib16) . Given that GPT-3.5 has been trained on trillions of tokens, we posit that these adjectives reflect a diverse, real-world distribution.
We input each adjective into the RAPHAEL model with prompt templates given by GPT-3.5 to generate 100100100 distinct images and collect their corresponding diffusion paths. Consequently, we obtain ten thousand paths for the 100100100 words. By treating these pathways as features (*i.e.,* each path is a vector of 16 entries), we train a straightforward classifier (*e.g.,* XGBoost [chen2015xgboost](#bib.bib17) ) to categorize the words. The classifier after 5-fold cross-validation achieves over 93% accuracy for open-world adjectives, demonstrating that different diffusion paths distinctively represent various textual concepts. We observe analogous phenomena within the 808080 object categories of the COCO dataset. Further details on verbs and visualization are provided in the Appendix [7.5](#S7.SS5 "7.5 More Details on Routers of Space-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

![Refer to caption](/html/2305.18295/assets/x4.png)


Figure 4: 
Left: We visualize the diffusion paths (routes) from the network input to the output, utilizing 16 space-MoE layers, each containing 6 space experts. These paths are closely associated with 100 adjectives, such as “scenic”, “peaceful”, and “majestic”, which represent the most frequently occurring adjectives for describing artworks as suggested by GPT-3.5 [brown2020language](#bib.bib15) ; [ouyang2022training](#bib.bib16) . Given that GPT-3.5 has been trained on trillions of tokens, we believe that these adjectives reflect a diverse, real-world distribution. Our findings indicate that different paths distinctively represent various adjectives. Right: We depict the diffusion paths for ten categories (*i.e.,* nouns) within the COCO dataset. Our observations reveal that different categories activate distinct paths in a heterogeneous manner. The display colors blend together where the routes overlap.

Time-MoE.
We can further enhance the image quality by employing a time-mixture-of-experts (time-MoE) approach, which is inspired by previous works such as [balaji2022ediffi](#bib.bib4) ; [feng2022ernie](#bib.bib5) .
Given that the diffusion process iteratively corrupts an image with Gaussian noise over a series of timesteps t=1,…,T𝑡

1…𝑇t=1,\ldots,T, the image generator is trained to denoise the images in reverse order from t=T𝑡𝑇t=T to t=1𝑡1t=1. All timesteps aim to denoise a noisy image, progressively transforming random noise into an artistic image.
Intuitively, the difficulty of these denoising steps varies depending on the noise ratio presented in the image. For example, when t=T𝑡𝑇t=T, the denoising network’s input image 𝐱tsubscript𝐱𝑡\mathbf{x}\_{t} is highly noisy. When
t=1𝑡1t=1, the image 𝐱tsubscript𝐱𝑡\mathbf{x}\_{t} is closer to the original image.

To address this issue, we employ a time-MoE before each space-MoE in each transformer block. In contrast to [balaji2022ediffi](#bib.bib4) ; [feng2022ernie](#bib.bib5)  , which necessitate hand-crafted time expert assignments,
we implement an additional gate network to automatically learn to assign different timesteps to various time experts. Further details can be found in the Appendix [7.3](#S7.SS3 "7.3 Details on Time-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

### 3.2 Edge-supervised Learning

In order to further enhance the image quality, we propose incorporating an edge-supervised learning strategy to train the transformer block. By implementing an edge detection module, we aim to extract rich boundary information from an image. These intricate boundaries can serve as supervision to guide the model in preserving detailed image features across various styles.

Consider a neural network module, Pθ​(𝐌)subscript𝑃𝜃𝐌P\_{\theta}(\mathbf{M}), with parameters of N𝑁N convolutional layers (*e.g.,* N=5𝑁5N=5). This module is designed to predict an edge map given an attention map 𝐌𝐌\mathbf{M} (refer to Fig.[7](#S7.F7 "Figure 7 ‣ 7.2 Details of Edge-supervised Learning ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")a in the Appendix [7.2](#S7.SS2 "7.2 Details of Edge-supervised Learning ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")).
We utilize the edge map of the input image, denoted as 𝐈edgesubscript𝐈edge\mathbf{I}\_{\operatorname{edge}}, to supervise the network Pθsubscript𝑃𝜃P\_{\theta}.
𝐈edgesubscript𝐈edge\mathbf{I}\_{\operatorname{edge}} can be obtained by the holistically-nested edge detection algorithm [xie2015holistically](#bib.bib18)  (Fig.[7](#S7.F7 "Figure 7 ‣ 7.2 Details of Edge-supervised Learning ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")b).
Intuitively, the network Pθsubscript𝑃𝜃P\_{\theta} can be trained by minimizing the loss function, ℒedge=Focal⁡(Pθ​(𝐌),𝐈edge)subscriptℒedgeFocalsubscript𝑃𝜃𝐌subscript𝐈edge\mathcal{L}\_{\operatorname{edge}}=\operatorname{Focal}(P\_{\theta}(\mathbf{M}),\mathbf{I}\_{\operatorname{edge}}), where Focal⁡(⋅,⋅)Focal⋅⋅\operatorname{Focal}(\cdot,\cdot) denotes the focal loss [lin2017focal](#bib.bib19)  employed to measure the discrepancy between
the predicted and the “ground-truth” edge maps.
Moreover, as discussed in [feng2022ernie](#bib.bib5) ; [hertz2022prompt](#bib.bib6) , the attention map 𝐌𝐌\mathbf{M} is prone to becoming vague when the timestep t𝑡t is large. Consequently, it is essential to adopt a timestep threshold value to inactivate (pause) edge-supervised learning when t𝑡t is large.
This timestep threshold value (Tcsubscript𝑇𝑐T\_{c}) is a hyper-parameter that will be evaluated through an ablation study.

Overall, the RAPHAEL model is trained by combining two loss functions,
ℒ=ℒdenoise+ℒedgeℒsubscriptℒdenoisesubscriptℒedge\mathcal{L}=\mathcal{L}\_{\operatorname{denoise}}+\mathcal{L}\_{\operatorname{edge}}.
As demonstrated in Fig.[7](#S7.F7 "Figure 7 ‣ 7.2 Details of Edge-supervised Learning ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")d in the Appendix [7.2](#S7.SS2 "7.2 Details of Edge-supervised Learning ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), edge-supervised learning substantially improves the image quality and aesthetic appeal of the generated images.

## 4 Experiments

This section presents the experimental setups, the quantitative results compared to recent state-of-the-art models, and the ablation study to demonstrate the effectiveness of RAPHAEL. More artistic images generated by RAPHAEL and comparisons between RAPHAEL and other diffusion models can be found in Appendix [7.6](#S7.SS6 "7.6 More Comparisons between RAPHAEL and Prestigious Diffusion Models ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") and [7.7](#S7.SS7 "7.7 More Images Generated by RAPHAEL ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

Dataset. The training dataset consists of LAION-5B [schuhmann2022laion](#bib.bib20)  and some internal datasets. To collect training data from LAION-5B, we filter the images using the aesthetic scorer same as Stable Diffusion [rombach2022high](#bib.bib2)  and remove the image-text pairs that have scores smaller than 4.74.74.7. We remove the images with watermarks either. Since the text descriptions in LAION-5B are noisy, we clean them by removing useless information such as URLs, HTML tags, and email addresses, inspired by [rombach2022high](#bib.bib2) ; [balaji2022ediffi](#bib.bib4) ; [bao2023one](#bib.bib21) .

Multi-scale Training. To improve text-image alignment,
instead of cropping images to a fixed scale [rombach2022high](#bib.bib2) , we resize an image to its nearest size in a bucket, which has 999 different image scales\*\*\*The [height, width] for each bucket is [448, 832], [512, 768], [512, 704], [640, 640], [576, 640], [640, 576], [704, 512], [768, 512], and [832, 448].. Additionally, the GPU resources will be automatically allocated to each bucket depending on the number of images it contains, enabling effective use of computational resources.

Implementations. To reduce training and sampling complexity, we use a Variational Autoencoder (VAE) [van2017neural](#bib.bib22) ; [kingma2019introduction](#bib.bib23)  to compress images using Latent Diffusion Model [rombach2022high](#bib.bib2) . We first pre-train an image encoder to transform an image from pixel space to a latent space, and an image decoder to convert it back.
Unlike previous works, the cross-attention layers in RAPHAEL are augmented with space-MoE and time-MoE layers. The entire model is implemented in PyTorch [paszke2019pytorch](#bib.bib24) , and is trained by AdamW [loshchilov2017decoupled](#bib.bib25)  optimizer with a learning rate of 1​e−41𝑒41e-4, a weight decay of 00, a batch size of 2,000

20002,000, on 1,000

10001,000 NVIDIA A100s for two months. More details on the hyper-parameter settings can be found in the Appendix [7.1](#S7.SS1 "7.1 Hyper-parameters and Values ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

Table 1: Comparisons of RAPHAEL with the recent representative text-to-image generation models on the MS-COCO 256×256256256256\times 256 using zero-shot
FID-30k. We see that RAPHAEL outperforms all previous works in image quality, even a commercial product released recently.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Approach | Venue/Date | Model Type | FID-30K | Zero-shot FID-30K |
| DF-GAN [tao2022df](#bib.bib26) | CVPR’22 | GAN | 21.42 | - |
| DM-GAN + CL [zhu2019dm](#bib.bib27) | CVPR’19 | GAN | 20.79 | - |
| LAFITE [zhou2021lafite](#bib.bib28) | CVPR’22 | GAN | 8.12 | - |
| Make-A-Scene [gafni2022make](#bib.bib29) | ECCV’22 | Autoregressive | 7.55 | - |
| LDM [rombach2022high](#bib.bib2) | CVPR’22 | Diffusion | - | 12.63 |
| GLIDE [nichol2021glide](#bib.bib30) | ICML’22 | Diffusion | - | 12.24 |
| DALL-E 2 [ramesh2022hierarchical](#bib.bib3) | arXiv, April 2022 | Diffusion | - | 10.39 |
| Stable Diffusion [rombach2022high](#bib.bib2) | CVPR’22 | Diffusion | - | 8.32 |
| Muse-3B [chang2023muse](#bib.bib31) | arXiv, Jan. 2023 | Non-Autoregressive | - | 7.88 |
| Imagen [saharia2022photorealistic](#bib.bib1) | NeurIPS’22 | Diffusion | - | 7.27 |
| eDiff-I [balaji2022ediffi](#bib.bib4) | arXiv, Nov. 2022 | Diffusion Experts | - | 6.95 |
| ERNIE-ViLG 2.0 [feng2022ernie](#bib.bib5) | CVPR’23 | Diffusion Experts | - | 6.75 |
| DeepFloyd | Product, May 2023 | Diffusion | - | 6.66 |
| RAPHAEL | - | Diffusion Experts | - | 6.61 |

![Refer to caption](/html/2305.18295/assets/x5.png)


Figure 5: Comparisons of RAPHAEL with DALL-E 2, Stable Diffusion XL (SD XL), ERNIE-ViLG 2.0, and DeepFloyd in a user study using the ViLG-300 benchmark. We report the user’s
preference rates with 95% confidence intervals. We see that RAPHAEL can generate images with higher quality and better
conform to the prompts.

### 4.1 Comparisons

Results on COCO. Following previous works [saharia2022photorealistic](#bib.bib1) ; [rombach2022high](#bib.bib2) ; [balaji2022ediffi](#bib.bib4) , we evaluate RAPHAEL on the COCO 256×256256256256\times 256 dataset using zero-shot Frechet Inception Distance (FID), which measures the quality and diversity of images.
Similar to [saharia2022photorealistic](#bib.bib1) ; [rombach2022high](#bib.bib2) ; [balaji2022ediffi](#bib.bib4) ; [feng2022ernie](#bib.bib5) ; [chang2023muse](#bib.bib31) , 30,000

3000030,000 images are randomly selected from the validation set for evaluation.
Table [1](#S4.T1 "Table 1 ‣ 4 Experiments ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") shows that RAPHAEL achieves a new state-of-the-art performance of text-to-image generation, with 6.616.616.61 zero-shot FID-30k on MS-COCO, surpassing prominent image generators such as Stable Diffusion, Imagen, ERNIE-ViLG 2.0, and DALL-E 2.

Human Evaluations. We employ the ViLG-300 benchmark [feng2022ernie](#bib.bib5) , a bilingual prompt set, which enables to
systematically evaluate text-to-image models given various text prompts in Chinese and English. ViLG-300 allows us to convincingly compare RAPHAEL with recent-advanced models including DALL-E 2, Stable Diffusion, ERNIE-ViLG 2.0, and DeepFloyd, in terms of both image quality and text-image alignment.
For example,
human artists are presented with two sets of images generated by RAPHAEL and a competitor, respectively.
They are asked to compare these images from two aspects respectively, including image-text alignment, and image quality and aesthetics.
Throughout the entire process, human artists are unaware of which model the image is generated from. Fig.[5](#S4.F5 "Figure 5 ‣ 4 Experiments ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") shows that RAPHAEL surpasses all other models in both image-text alignment and image quality in the user study, indicating
that RAPHAEL can generate high-artistry images that conform to the text.

Extensions to LoRA, ControlNet, and SR-GAN.
RAPHAEL can be further extended by incorporating LoRA, ControlNet, and SR-GAN. In Appendix [7.8](#S7.SS8 "7.8 Extension to LoRA, ControlNet, and SR-GAN ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), we present a comparison between RAPHAEL and Stable Diffusion utilizing LoRA. RAPHAEL demonstrates superior robustness against overfitting compared to Stable Diffusion. We also demonstrate RAPHAEL with a canny-based ControlNet. Furthermore, by employing a tailormade SR-GAN model, we enhance the image resolution to 4096×6144409661444096\times 6144.

### 4.2 Ablation Study

Evaluate every module in RAPHAEL.
We conduct a comprehensive assessment of each module within the RAPHAEL model, utilizing the CLIP [radford2021learning](#bib.bib14)  score to measure image-text alignment. Given the significance of classifier-free guidance weight in controlling image quality and text alignment, we present ablation results as trade-off curves between CLIP and FID scores across a range of guidance weights [ho2022classifier](#bib.bib32) , specifically 1.51.51.5, 3.03.03.0, 4.54.54.5, 6.06.06.0, 7.57.57.5, and 9.09.09.0. Fig.[6](#S4.F6 "Figure 6 ‣ 4.2 Ablation Study ‣ 4 Experiments ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")b compares these curves for the complete RAPHAEL model and its variants without space-MoE, edge-supervised learning, and time-MoE, respectively. Our findings indicate that all modules contribute effectively. For example, space-MoE substantially enhances the CLIP score and the optimal guidance weight for the sampler shifts from 3.0 to 4.5. Moreover, at the same guidance weight, space-MoE considerably reduces the FID, resulting in a significant improvement in image quality.

![Refer to caption](/html/2305.18295/assets/x6.png)


Figure 6: Ablation Study. (a) examines the selection of α𝛼\alpha and Tcsubscript𝑇𝑐T\_{c}. (b) presents the trade-off between FID and CLIP scores for the complete RAPHAEL model and its variants without space-MoE, time-MoE, and edge-supervised learning. (c) visualizes the correlation between FID-5k and runtime complexity (measured in terms of the number of DDIM [song2020denoising](#bib.bib33)  steps for an image per second) as a function of the number of experts employed. Notably, the computational complexity is predominantly influenced by the number of space experts.

Choice of α𝛼\alpha and Tcsubscript𝑇𝑐T\_{c}.
As depicted in Fig.[6](#S4.F6 "Figure 6 ‣ 4.2 Ablation Study ‣ 4 Experiments ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")a, we observe that α=0.2𝛼0.2\alpha=0.2 delivers the best performance, implying a balance between preserving adequate features and avoiding the use of the entire latent features. An appropriate threshold value for Tcsubscript𝑇𝑐T\_{c} terminates edge-supervised learning when the diffusion timestep is large. Our experiments reveal that a suitable choice for Tcsubscript𝑇𝑐T\_{c} is 500, ensuring the effective learning of texture information.

Performance and Runtime Analysis on Number of Experts.
We offer an examination of the number of experts, ranging from 00 to 888, in Fig.[6](#S4.F6 "Figure 6 ‣ 4.2 Ablation Study ‣ 4 Experiments ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")c. For each setting, we employ 100 million training samples. Our results demonstrate that increasing the number of experts improves FID (lower values are preferable). However, adding space experts introduces additional computations, with the computational complexity bounded by the total number of experts.
Once all available experts have been deployed, the computational complexity ceases to grow. In the right-hand side of Fig.[6](#S4.F6 "Figure 6 ‣ 4.2 Ablation Study ‣ 4 Experiments ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths")c, we provide a runtime analysis for 40 input tokens, ensuring the utilization of all space experts. For instance, when the number of experts is 6, the inference speed decreases by 24% but yields superior fidelity. This remains faster than previous diffusion models such as Imagen [saharia2022photorealistic](#bib.bib1)  and eDiff-I [balaji2022ediffi](#bib.bib4) .

## 5 Related Work

We review related works from two perspectives, mixture-of-experts and text-to-image generation. More related works can be found in
Appendix [7.4](#S7.SS4 "7.4 Related Work ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").
Firstly,
the Mixture-of-Experts (MoE) method [shazeer2017outrageously](#bib.bib7) ; [fedus2022switch](#bib.bib8)  partitions model parameters into distinct subsets, each termed an “expert”. The MoE paradigm finds applicability beyond language processing tasks, extending to visual models [riquelme2021scaling](#bib.bib34)  and Mixture-of-Modality-Experts within multi-modal transformers [shen2023scaling](#bib.bib35) . Additionally, efforts are being made to accelerate the training or inference processes for MoE [he2021fastmoe](#bib.bib36) ; [lepikhin2020gshard](#bib.bib37) .
Secondly,
text-to-image generation is to synthesize images from natural language descriptions. Early approaches relied on generative adversarial networks (GANs) [creswell2018generative](#bib.bib38) ; [wang2018high](#bib.bib39) ; [karras2020analyzing](#bib.bib40) ; [goodfellow2020generative](#bib.bib41)  to generate images. More recently, with the transformative success of transformers in generative tasks, models such as DALL-E [ramesh2021zero](#bib.bib42) , Cogview [ding2021cogview](#bib.bib43) , and Make-A-Scene [gafni2022make](#bib.bib29)  have treated text-to-image generation as a sequence-to-sequence problem, utilizing auto-regressive transformers as generators and employing text/image tokens as input/output sequences. Recently, another research direction has focused on diffusion models
by integrating textual conditioning within denoising steps, like Stable Diffusion [rombach2022high](#bib.bib2) , DALL-E 2 [ramesh2022hierarchical](#bib.bib3) , eDiff-I [balaji2022ediffi](#bib.bib4) , ERNIE-ViLG 2.0 [feng2022ernie](#bib.bib5) , and Imagen [saharia2022photorealistic](#bib.bib1) .

## 6 Conclusion

This paper introduces RAPHAEL, a novel text-conditional image diffusion model capable of generating highly-artistic images using a large-scale mixture of diffusion paths. We carefully design space-MoE and time-MoE within an edge-supervised learning framework, enabling RAPHAEL to accurately portray text prompts, enhance the alignment between textual concepts and image regions, and produce images with superior aesthetic appeal. Comprehensive experiments demonstrate that RAPHAEL surpasses previous approaches, such as Stable Diffusion, ERNIE-ViLG 2.0, DeepFloyd, and DALL-E 2, in both FID-30k and the human evaluation benchmark ViLG-300. Additionally, RAPHAEL can be extended using LoRA, ControlNet, and SR-GAN. We believe that RAPHAEL has the potential to advance image generation research in both academia and industry.

Limitation and Potential Negative Societal Impact.
The potential negative social impact is to use the RAPHAEL API to create images containing misleading or false information. This issue potentially presents in all powerful text-to-image generators. We will solve this issue (*e.g.,* by prompt filtering) before releasing the API to the public.

## References

* [1]

  Chitwan Saharia, William Chan, Saurabh Saxena, Lala Li, Jay Whang, Emily L Denton, Kamyar Ghasemipour, Raphael Gontijo Lopes, Burcu Karagol Ayan, Tim Salimans, et al.
  Photorealistic text-to-image diffusion models with deep language understanding.
  Advances in Neural Information Processing Systems, 35:36479–36494, 2022.
* [2]

  Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, and Björn Ommer.
  High-resolution image synthesis with latent diffusion models.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 10684–10695, 2022.
* [3]

  Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen.
  Hierarchical text-conditional image generation with clip latents.
  arXiv preprint arXiv:2204.06125, 2022.
* [4]

  Yogesh Balaji, Seungjun Nah, Xun Huang, Arash Vahdat, Jiaming Song, Karsten Kreis, Miika Aittala, Timo Aila, Samuli Laine, Bryan Catanzaro, et al.
  ediffi: Text-to-image diffusion models with an ensemble of expert denoisers.
  arXiv preprint arXiv:2211.01324, 2022.
* [5]

  Zhida Feng, Zhenyu Zhang, Xintong Yu, Yewei Fang, Lanxin Li, Xuyi Chen, Yuxiang Lu, Jiaxiang Liu, Weichong Yin, Shikun Feng, et al.
  Ernie-vilg 2.0: Improving text-to-image diffusion model with knowledge-enhanced mixture-of-denoising-experts.
  arXiv preprint arXiv:2210.15257, 2022.
* [6]

  Amir Hertz, Ron Mokady, Jay Tenenbaum, Kfir Aberman, Yael Pritch, and Daniel Cohen-Or.
  Prompt-to-prompt image editing with cross attention control.
  arXiv preprint arXiv:2208.01626, 2022.
* [7]

  Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc Le, Geoffrey Hinton, and Jeff Dean.
  Outrageously large neural networks: The sparsely-gated mixture-of-experts layer.
  arXiv preprint arXiv:1701.06538, 2017.
* [8]

  William Fedus, Barret Zoph, and Noam Shazeer.
  Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity.
  The Journal of Machine Learning Research, 23(1):5232–5270, 2022.
* [9]

  Xintao Wang, Liangbin Xie, Chao Dong, and Ying Shan.
  Real-esrgan: Training real-world blind super-resolution with pure synthetic data.
  In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 1905–1914, 2021.
* [10]

  Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen.
  Lora: Low-rank adaptation of large language models.
  arXiv preprint arXiv:2106.09685, 2021.
* [11]

  Lvmin Zhang and Maneesh Agrawala.
  Adding conditional control to text-to-image diffusion models.
  arXiv preprint arXiv:2302.05543, 2023.
* [12]

  Jonathan Ho, Ajay Jain, and Pieter Abbeel.
  Denoising diffusion probabilistic models.
  Advances in Neural Information Processing Systems, 33:6840–6851, 2020.
* [13]

  Olaf Ronneberger, Philipp Fischer, and Thomas Brox.
  U-net: Convolutional networks for biomedical image segmentation.
  In Medical Image Computing and Computer-Assisted Intervention–MICCAI 2015: 18th International Conference, Munich, Germany, October 5-9, 2015, Proceedings, Part III 18, pages 234–241. Springer, 2015.
* [14]

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al.
  Learning transferable visual models from natural language supervision.
  In International Conference on Machine Learning, pages 8748–8763. PMLR, 2021.
* [15]

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.
  Language models are few-shot learners.
  Advances in Neural Information Processing Systems, 33:1877–1901, 2020.
* [16]

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
  Training language models to follow instructions with human feedback.
  Advances in Neural Information Processing Systems, 35:27730–27744, 2022.
* [17]

  Tianqi Chen, Tong He, Michael Benesty, Vadim Khotilovich, Yuan Tang, Hyunsu Cho, Kailong Chen, Rory Mitchell, Ignacio Cano, Tianyi Zhou, et al.
  Xgboost: extreme gradient boosting.
  R package version 0.4-2, 1(4):1–4, 2015.
* [18]

  Saining Xie and Zhuowen Tu.
  Holistically-nested edge detection.
  In Proceedings of the IEEE International Conference on Computer Vision, pages 1395–1403, 2015.
* [19]

  Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollár.
  Focal loss for dense object detection.
  In Proceedings of the IEEE International Conference on Computer Vision, pages 2980–2988, 2017.
* [20]

  Christoph Schuhmann, Romain Beaumont, Richard Vencu, Cade Gordon, Ross Wightman, Mehdi Cherti, Theo Coombes, Aarush Katta, Clayton Mullis, Mitchell Wortsman, et al.
  Laion-5b: An open large-scale dataset for training next generation image-text models.
  arXiv preprint arXiv:2210.08402, 2022.
* [21]

  Fan Bao, Shen Nie, Kaiwen Xue, Chongxuan Li, Shi Pu, Yaole Wang, Gang Yue, Yue Cao, Hang Su, and Jun Zhu.
  One transformer fits all distributions in multi-modal diffusion at scale.
  arXiv preprint arXiv:2303.06555, 2023.
* [22]

  Aaron Van Den Oord, Oriol Vinyals, et al.
  Neural discrete representation learning.
  Advances in Neural Information Processing Systems, 30, 2017.
* [23]

  Diederik P Kingma, Max Welling, et al.
  An introduction to variational autoencoders.
  Foundations and Trends in Machine Learning, 12(4):307–392, 2019.
* [24]

  Adam Paszke, Sam Gross, Francisco Massa, Adam Lerer, James Bradbury, Gregory Chanan, Trevor Killeen, Zeming Lin, Natalia Gimelshein, Luca Antiga, et al.
  Pytorch: An imperative style, high-performance deep learning library.
  Advances in Neural Information Processing Systems, 32, 2019.
* [25]

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  arXiv preprint arXiv:1711.05101, 2017.
* [26]

  Ming Tao, Hao Tang, Fei Wu, Xiao-Yuan Jing, Bing-Kun Bao, and Changsheng Xu.
  Df-gan: A simple and effective baseline for text-to-image synthesis.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 16515–16525, 2022.
* [27]

  Minfeng Zhu, Pingbo Pan, Wei Chen, and Yi Yang.
  Dm-gan: Dynamic memory generative adversarial networks for text-to-image synthesis.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 5802–5810, 2019.
* [28]

  Yufan Zhou, Ruiyi Zhang, Changyou Chen, Chunyuan Li, Chris Tensmeyer, Tong Yu, Jiuxiang Gu, Jinhui Xu, and Tong Sun.
  Lafite: Towards language-free training for text-to-image generation.
  arXiv preprint arXiv:2111.13792, 2021.
* [29]

  Oran Gafni, Adam Polyak, Oron Ashual, Shelly Sheynin, Devi Parikh, and Yaniv Taigman.
  Make-a-scene: Scene-based text-to-image generation with human priors.
  In Computer Vision–ECCV 2022: 17th European Conference, Tel Aviv, Israel, October 23–27, 2022, Proceedings, Part XV, pages 89–106. Springer, 2022.
* [30]

  Alex Nichol, Prafulla Dhariwal, Aditya Ramesh, Pranav Shyam, Pamela Mishkin, Bob McGrew, Ilya Sutskever, and Mark Chen.
  Glide: Towards photorealistic image generation and editing with text-guided diffusion models.
  arXiv preprint arXiv:2112.10741, 2021.
* [31]

  Huiwen Chang, Han Zhang, Jarred Barber, AJ Maschinot, Jose Lezama, Lu Jiang, Ming-Hsuan Yang, Kevin Murphy, William T Freeman, Michael Rubinstein, et al.
  Muse: Text-to-image generation via masked generative transformers.
  arXiv preprint arXiv:2301.00704, 2023.
* [32]

  Jonathan Ho and Tim Salimans.
  Classifier-free diffusion guidance.
  arXiv preprint arXiv:2207.12598, 2022.
* [33]

  Jiaming Song, Chenlin Meng, and Stefano Ermon.
  Denoising diffusion implicit models.
  arXiv preprint arXiv:2010.02502, 2020.
* [34]

  Carlos Riquelme, Joan Puigcerver, Basil Mustafa, Maxim Neumann, Rodolphe Jenatton, André Susano Pinto, Daniel Keysers, and Neil Houlsby.
  Scaling vision with sparse mixture of experts.
  Advances in Neural Information Processing Systems, 34:8583–8595, 2021.
* [35]

  Sheng Shen, Zhewei Yao, Chunyuan Li, Trevor Darrell, Kurt Keutzer, and Yuxiong He.
  Scaling vision-language models with sparse mixture of experts.
  arXiv preprint arXiv:2303.07226, 2023.
* [36]

  Jiaao He, Jiezhong Qiu, Aohan Zeng, Zhilin Yang, Jidong Zhai, and Jie Tang.
  Fastmoe: A fast mixture-of-expert training system.
  arXiv preprint arXiv:2103.13262, 2021.
* [37]

  Dmitry Lepikhin, HyoukJoong Lee, Yuanzhong Xu, Dehao Chen, Orhan Firat, Yanping Huang, Maxim Krikun, Noam Shazeer, and Zhifeng Chen.
  Gshard: Scaling giant models with conditional computation and automatic sharding.
  arXiv preprint arXiv:2006.16668, 2020.
* [38]

  Antonia Creswell, Tom White, Vincent Dumoulin, Kai Arulkumaran, Biswa Sengupta, and Anil A Bharath.
  Generative adversarial networks: An overview.
  IEEE Signal Processing Magazine, 35(1):53–65, 2018.
* [39]

  Ting-Chun Wang, Ming-Yu Liu, Jun-Yan Zhu, Andrew Tao, Jan Kautz, and Bryan Catanzaro.
  High-resolution image synthesis and semantic manipulation with conditional gans.
  In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 8798–8807, 2018.
* [40]

  Tero Karras, Samuli Laine, Miika Aittala, Janne Hellsten, Jaakko Lehtinen, and Timo Aila.
  Analyzing and improving the image quality of stylegan.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 8110–8119, 2020.
* [41]

  Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley, Sherjil Ozair, Aaron Courville, and Yoshua Bengio.
  Generative adversarial networks.
  Communications of the ACM, 63(11):139–144, 2020.
* [42]

  Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever.
  Zero-shot text-to-image generation.
  In International Conference on Machine Learning, pages 8821–8831. PMLR, 2021.
* [43]

  Ming Ding, Zhuoyi Yang, Wenyi Hong, Wendi Zheng, Chang Zhou, Da Yin, Junyang Lin, Xu Zou, Zhou Shao, Hongxia Yang, et al.
  Cogview: Mastering text-to-image generation via transformers.
  Advances in Neural Information Processing Systems, 34:19822–19835, 2021.
* [44]

  Zeyue Xue, Jianming Liang, Guanglu Song, Zhuofan Zong, Liang Chen, Yu Liu, and Ping Luo.
  Large-batch optimization for dense visual predictions.
  arXiv preprint arXiv:2210.11078, 2022.
* [45]

  David Eigen, Marc’Aurelio Ranzato, and Ilya Sutskever.
  Learning factored representations in a deep mixture of experts.
  arXiv preprint arXiv:1312.4314, 2013.
* [46]

  Nan Du, Yanping Huang, Andrew M Dai, Simon Tong, Dmitry Lepikhin, Yuanzhong Xu, Maxim Krikun, Yanqi Zhou, Adams Wei Yu, Orhan Firat, et al.
  Glam: Efficient scaling of language models with mixture-of-experts.
  In International Conference on Machine Learning, pages 5547–5569. PMLR, 2022.
* [47]

  Margaret Li, Suchin Gururangan, Tim Dettmers, Mike Lewis, Tim Althoff, Noah A Smith, and Luke Zettlemoyer.
  Branch-train-merge: Embarrassingly parallel training of expert language models.
  arXiv preprint arXiv:2208.03306, 2022.
* [48]

  Minguk Kang, Jun-Yan Zhu, Richard Zhang, Jaesik Park, Eli Shechtman, Sylvain Paris, and Taesung Park.
  Scaling up gans for text-to-image synthesis.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 10124–10134, 2023.
* [49]

  Nataniel Ruiz, Yuanzhen Li, Varun Jampani, Yael Pritch, Michael Rubinstein, and Kfir Aberman.
  Dreambooth: Fine tuning text-to-image diffusion models for subject-driven generation.
  arXiv preprint arXiv:2208.12242, 2022.
* [50]

  Chenlin Meng, Yutong He, Yang Song, Jiaming Song, Jiajun Wu, Jun-Yan Zhu, and Stefano Ermon.
  Sdedit: Guided image synthesis and editing with stochastic differential equations.
  In International Conference on Learning Representations, 2021.
* [51]

  Bahjat Kawar, Shiran Zada, Oran Lang, Omer Tov, Huiwen Chang, Tali Dekel, Inbar Mosseri, and Michal Irani.
  Imagic: Text-based real image editing with diffusion models.
  arXiv preprint arXiv:2210.09276, 2022.
* [52]

  Shaozhe Hao, Kai Han, Shihao Zhao, and Kwan-Yee K Wong.
  Vico: Detail-preserving visual condition for personalized text-to-image generation.
  arXiv preprint arXiv:2306.00971, 2023.
* [53]

  Zhiheng Liu, Ruili Feng, Kai Zhu, Yifei Zhang, Kecheng Zheng, Yu Liu, Deli Zhao, Jingren Zhou, and Yang Cao.
  Cones: Concept neurons in diffusion models for customized generation.
  arXiv preprint arXiv:2303.05125, 2023.
* [54]

  Zhiheng Liu, Yifei Zhang, Yujun Shen, Kecheng Zheng, Kai Zhu, Ruili Feng, Yu Liu, Deli Zhao, Jingren Zhou, and Yang Cao.
  Cones 2: Customizable image synthesis with multiple subjects.
  arXiv preprint arXiv:2305.19327, 2023.
* [55]

  Xi Chen, Lianghua Huang, Yu Liu, Yujun Shen, Deli Zhao, and Hengshuang Zhao.
  Anydoor: Zero-shot object-level image customization.
  arXiv preprint arXiv:2307.09481, 2023.
* [56]

  Lingting Zhu, Zeyue Xue, Zhenchao Jin, Xian Liu, Jingzhen He, Ziwei Liu, and Lequan Yu.
  Make-a-volume: Leveraging latent diffusion models for cross-modality 3d brain mri synthesis.
  In International Conference on Medical Image Computing and Computer-Assisted Intervention, pages 592–601. Springer, 2023.
* [57]

  Chen-Hsuan Lin, Jun Gao, Luming Tang, Towaki Takikawa, Xiaohui Zeng, Xun Huang, Karsten Kreis, Sanja Fidler, Ming-Yu Liu, and Tsung-Yi Lin.
  Magic3d: High-resolution text-to-3d content creation.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 300–309, 2023.
* [58]

  Ben Poole, Ajay Jain, Jonathan T Barron, and Ben Mildenhall.
  Dreamfusion: Text-to-3d using 2d diffusion.
  arXiv preprint arXiv:2209.14988, 2022.
* [59]

  Xiang Wang, Hangjie Yuan, Shiwei Zhang, Dayou Chen, Jiuniu Wang, Yingya Zhang, Yujun Shen, Deli Zhao, and Jingren Zhou.
  Videocomposer: Compositional video synthesis with motion controllability.
  arXiv preprint arXiv:2306.02018, 2023.
* [60]

  Andreas Blattmann, Robin Rombach, Huan Ling, Tim Dockhorn, Seung Wook Kim, Sanja Fidler, and Karsten Kreis.
  Align your latents: High-resolution video synthesis with latent diffusion models.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 22563–22575, 2023.
* [61]

  Lingting Zhu, Xian Liu, Xuanyu Liu, Rui Qian, Ziwei Liu, and Lequan Yu.
  Taming diffusion models for audio-driven co-speech gesture generation.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 10544–10553, 2023.
* [62]

  Shihao Zhao, Dongdong Chen, Yen-Chun Chen, Jianmin Bao, Shaozhe Hao, Lu Yuan, and Kwan-Yee K Wong.
  Uni-controlnet: All-in-one control to text-to-image diffusion models.
  Advances in Neural Information Processing Systems, 2023.

## 7 Appendix

### 7.1 Hyper-parameters and Values

We give the hyper-parameters and values in Table [2](#S7.T2 "Table 2 ‣ 7.1 Hyper-parameters and Values ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

Table 2: Hyper-parameters and values in RAPHAEL.

| Configs/Hyper-parameters | Values |
| --- | --- |
| T𝑇T | 1000 |
| nysubscript𝑛𝑦n\_{y} | 77 |
| dysubscript𝑑𝑦d\_{y} | 1024 |
| Tcsubscript𝑇𝑐T\_{c} | 500 |
| α𝛼\alpha | 0.2 |
| Betas of AdamW [[25](#bib.bib25)] | (0.9, 0.999) |
| Weight decay | 0.0 |
| Learning rate | 1e𝑒e-4 |
| Number of space experts | 6 |
| Number of time experts | 4 |
| Warmup steps | 20000 |
| Batch size | 2000 |
| Number of GPUs | 1000 |
| Number of transformer blocks | 16 |
| Use checkpoint | True |
| α𝛼\alpha in Focal Loss [[19](#bib.bib19)] | 0.5 |
| γ𝛾\gamma in Focal Loss [[19](#bib.bib19)] | 2 |
| Text encoder | OpenCLIP-g/14 [[14](#bib.bib14)] |
| Enable multi-scale training | True |
| Activations in experts and gate network | GELU |
| Architectures of experts and gate network | FFN |

### 7.2 Details of Edge-supervised Learning

We provide some demonstrations of edge-supervised learning in Fig.[7](#S7.F7 "Figure 7 ‣ 7.2 Details of Edge-supervised Learning ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

![Refer to caption](/html/2305.18295/assets/x7.png)


Figure 7: From left to right, we display the attention map corresponding to the pooled token in CLIP, the ground truth edges identified by the edge detection algorithm, and the associated image. In the fourth figure, we present the human evaluation results for models with and without edge-supervised learning on the ViLG-300 benchmark. Evaluators are instructed to compare these images considering image aesthetics and we report the preference rates, and our findings indicate that edge-supervised learning significantly enhances the aesthetic quality of the images.

### 7.3 Details on Time-MoE

![Refer to caption](/html/2305.18295/assets/x8.png)


Figure 8: 
(a) The architecture of U-Net, which consists of many transformer blocks.
(b) Each block contains four primary components including a self-attention layer, a cross-attention layer, a space-MoE layer, and a time-MoE layer. The space-MoE is responsible for depicting different text concepts in specific image regions, while the time-MoE handles different diffusion timesteps. Each block uses edge-supervised cross-attention learning to further improve image quality.
(c) shows details of space-MoE.
For example, given a prompt “a furry bear under sky”, each text token and its corresponding image region (given by a binary mask) are directed through distinct space experts, *i.e.,* each expert learns particular visual features at a region.
(d) For time-MoE, an initial timestep is provided, followed by the selection of an expert responsible for handling the visual features.

![Refer to caption](/html/2305.18295/assets/x9.png)


Figure 9: The routes of time-MoE in the first transformer block, where the first expert focuses on noisy images, while other experts handle images with low noise levels.

The overall architecture of RAPHAEL can be found in Fig.[8](#S7.F8 "Figure 8 ‣ 7.3 Details on Time-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").
The Time-MoE is composed of a Time Gate Network to distribute the features to a specific expert according to the timestep, which can be formulated as h′​(𝐱t)=t​et​\_​router⁡(ti)​(hc​(𝐱t))superscriptℎ′subscript𝐱𝑡𝑡subscript𝑒t\_routersubscript𝑡𝑖subscriptℎ𝑐subscript𝐱𝑡h^{\prime}(\mathbf{x}\_{t})=te\_{\operatorname{t\\_router}(t\_{i})}\left(h\_{c}(\mathbf{x}\_{t})\right). In this equation, hc​(𝐱t)subscriptℎ𝑐subscript𝐱𝑡h\_{c}(\mathbf{x}\_{t}) is the features from cross-attention module. The gating function t​\_​routert\_router\operatorname{t\\_router} returns the index of an expert in the Time-MoE, with {t​e1,t​e2,…,t​ent}𝑡subscript𝑒1𝑡subscript𝑒2…𝑡subscript𝑒subscript𝑛𝑡\{te\_{1},te\_{2},...,te\_{n\_{t}}\} being a set of ntsubscript𝑛𝑡n\_{t} experts.
Concretely, the Time Gate Network is implemented by a function, t​\_​router⁡(ti)=argmax​(softmax⁡(𝒢′​(Eθ′​(ti))+ϵ))t\_routersubscript𝑡𝑖argmaxsoftmaxsuperscript𝒢′subscriptsuperscript𝐸′𝜃subscript𝑡𝑖italic-ϵ\operatorname{t\\_router}(t\_{i})=\mathrm{argmax}\left(\operatorname{softmax}\left(\mathcal{G}^{\prime}\left(E^{\prime}\_{\theta}(t\_{i})\right)+\epsilon\right)\right) at timestep tisubscript𝑡𝑖t\_{i}. To prevent mode collapse, random noise ϵitalic-ϵ\epsilon is incorporated. Similar to the Text Gate, 𝒢′:ℝdt↦ℝnt:superscript𝒢′maps-tosuperscriptℝsubscript𝑑𝑡superscriptℝsubscript𝑛𝑡\mathcal{G}^{\prime}:\mathbb{R}^{d\_{t}}\mapsto\mathbb{R}^{n\_{t}}, is a feed forward network, where dtsubscript𝑑𝑡d\_{t} is the dimension of the time embedding Eθ′​(ti)subscriptsuperscript𝐸′𝜃subscript𝑡𝑖E^{\prime}\_{\theta}(t\_{i}).

Analysis. In our exploration, we uncover some statistical regularities within the routes of time experts across all transformer blocks, establishing a clear correlation with the timestep dimension. Notably, we observe a distinct division of labor among these experts, specializing in timesteps characterized by varying levels of noise. For instance, as illustrated in Fig.[9](#S7.F9 "Figure 9 ‣ 7.3 Details on Time-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), in the first transformer block, the first expert predominately focuses on processing noisy images (representing the initial 59% of DDIM sampler steps), while the remaining experts handle images with relatively lower noise levels (representing the final 41% of DDIM sampler steps). This systematic allocation of expertise based on noise characteristics underscores the model’s ability to adapt its computational resources efficiently and effectively.

### 7.4 Related Work

Foundation models have achieved remarkable success in several fields [[2](#bib.bib2), [44](#bib.bib44), [34](#bib.bib34), [15](#bib.bib15)], especially for text-to-image generation. We review related works from two perspectives, mixture-of-experts, and text-to-image generation.

Mixture-of-Experts. The Mixture-of-Experts (MoE) method [[7](#bib.bib7), [8](#bib.bib8)] in neural networks partitions specific model parameters into distinct subsets, each termed an "expert." During forward propagation, a dynamic routing mechanism assigns these experts to diverse inputs, with each input exclusively interacting with its selected experts. MoE models implement a learned gating function that selectively activates a subset of experts, enabling the input to engage either all experts [[45](#bib.bib45)] or a sparse mixture thereof [[8](#bib.bib8), [46](#bib.bib46)], as evidenced in recent expansive language models. While a multitude of models employs experts strictly within the linear layers, other research regards an entire language model as an expert [[47](#bib.bib47)]. The MoE paradigm finds applicability beyond language processing tasks, extending to visual models [[34](#bib.bib34)] and Mixture-of-Modality-Experts within multi-modal transformers [[35](#bib.bib35)]. Additionally, efforts are being made to accelerate the training or inference processes within the MoE paradigm [[36](#bib.bib36), [37](#bib.bib37)].

Text-to-Image Generation. Text-to-image generation, the task of synthesizing images from natural language descriptions, has experienced significant progress in recent years. Early approaches relied on generative adversarial networks (GANs) [[38](#bib.bib38), [39](#bib.bib39), [40](#bib.bib40), [41](#bib.bib41), [48](#bib.bib48)] to generate images. More recently, with the transformative success of transformers in generative tasks, models such as DALL-E [[42](#bib.bib42)], Cogview [[43](#bib.bib43)], and Make-A-Scene [[29](#bib.bib29)] have treated text-to-image generation as a sequence-to-sequence problem, utilizing auto-regressive transformers as generators and employing text/image tokens as input/output sequences. Recently, another research direction has focused on diffusion models, framing the task as an iterative denoising process. By integrating textual conditioning within denoising steps, models like Stable Diffusion [[2](#bib.bib2)], DALL-E 2 [[3](#bib.bib3)], eDiff-I [[4](#bib.bib4)], ERNIE-ViLG 2.0 [[5](#bib.bib5)], and Imagen [[1](#bib.bib1)] have consistently set new benchmarks in text-to-image generation. Specifically, Stable Diffusion and ERNIE-ViLG 2.0 map images into a latent space, following the Latent Diffusion Model paradigm to enhance training and sampling efficiency, while DALL-E 2, eDiff-I, and Imagen operate in pixel space. Furthermore, diffusion models also show great potential in image editing [[49](#bib.bib49), [6](#bib.bib6), [50](#bib.bib50), [51](#bib.bib51)], personalized generation [[52](#bib.bib52), [53](#bib.bib53), [54](#bib.bib54), [55](#bib.bib55)], and 3D/video/gesture generation [[56](#bib.bib56), [57](#bib.bib57), [58](#bib.bib58), [59](#bib.bib59), [60](#bib.bib60), [61](#bib.bib61)]. ControlNet [[11](#bib.bib11), [62](#bib.bib62)] is a noteworthy model in the text-to-image generation landscape. It builds upon the concept of controllable image synthesis, wherein generated images can be manipulated based on user-defined constraints or attributes.

### 7.5 More Details on Routers of Space-MoE

We continue to delve into the diffusion paths of both COCO categories and verbs, uncovering intriguing insights. Utilizing the powerful GPT-3.5 [[15](#bib.bib15), [16](#bib.bib16)], we randomly generate 50 verbs to enrich our investigation. Moreover, employing the prompt template randomly generated by GPT-3.5, we generate 100 samples for each COCO category and verb [[15](#bib.bib15), [16](#bib.bib16)]. Similar to Section 3.1, by adopting XGBoost as our classifier, we find that the accuracy rate reaches 94.3%percent\% and 97.5%percent\%, respectively. We give the routes of COCO and 50 verbs in Fig.[10](#S7.F10 "Figure 10 ‣ 7.5 More Details on Routers of Space-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"). We also show more visualization results of the attention maps in Fig.[11](#S7.F11 "Figure 11 ‣ 7.5 More Details on Routers of Space-MoE ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"). We provide the adjectives and verbs in the following section.

![Refer to caption](/html/2305.18295/assets/x10.png)


Figure 10: We visualize the diffusion paths (routes) from the network input to the output, utilizing 16 space-MoE layers, each containing 6 space experts. These paths are closely associated with COCO categories and 50 verbs.

![Refer to caption](/html/2305.18295/assets/x11.png)


Figure 11: We give the prompts, their associated generated images, and attention maps.

#### 7.5.1 Adjectives and Verbs

Adjectives.
Aesthetic, alluring, artistic, astonishing, attractive, baroque, beautiful, blissful, captivating, chic, classic, coastal, colorful, common, dark, decorative, delicate, dramatic, dreamlike, dreamy, dynamic, eclectic, elegant, emotive, enchanting, energetic, enthralling, essential, ethereal, evocative, extraordinary, fascinating, flexible, fragile, futuristic, glamorous, glossy, gorgeous, gothic, grand, harmonious, idyllic, impressive, industrial, innovative, inspiring, intricate, intriguing, joyful, lively, luxurious, magnificent, meditative, mesmerizing, minimal, minimalist, modern, moroccan, mysterious, nostalgic, ordinary, patterned, peaceful, picturesque, plain, playful, practical, quirky, rare, renaissance, retro, rigid, romantic, rough, rustic, satisfying, Scandinavian, scenic, serene, serious, shiny, simple, sleek, smooth, sophisticated, static, striking, stunning, sturdy, stylish, textured, traditional, tranquil, unique, unusual, useful, vibrant, victorian, vivid, whimsical.

Verbs.
Balance, blend, blossom, bond, carve, celebrate, cheer, climb, collaborate, conduct, conquer, cook, craft, create, dance, dream, embrace, experiment, explore, gaze, harmonize, hike, hug, ignite, illuminate, jump, laugh, leap, listen, meander, observe, paint, play, ponder, read, rejoice, relax, ride, run, savor, sculpt, sing, smile, soar, surf, swim, swing, taste, wander, whisper.

### 7.6 More Comparisons between RAPHAEL and Prestigious Diffusion Models

In this section, we provide more comparisons between RAPHAEL and Midjourney, Stable Diffusion XL, DALL-E 2, DeepFloyd, ERNIE-ViLG 2.0 in Fig.[12](#S7.F12 "Figure 12 ‣ 7.6 More Comparisons between RAPHAEL and Prestigious Diffusion Models ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") and [13](#S7.F13 "Figure 13 ‣ 7.6 More Comparisons between RAPHAEL and Prestigious Diffusion Models ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

![Refer to caption](/html/2305.18295/assets/x12.png)


Figure 12: The prompts for each column are given in the figure. We give the comparisons between DALL-E 2 Midjourney v5.1, Stable Diffusion XL, ERNIE ViLG 2.0, DeepFloyd, and RAPHAEL. They are given the same prompts, where the words that the human artists yearn to preserve within the generated images are highlighted in red. Only the RAPHAEL-generated images precisely reflect the prompts, while other models generate compromised results. For images with cartoon styles, we switch Midjourney v5.1 to Nijijourney v5.

![Refer to caption](/html/2305.18295/assets/x13.png)


Figure 13: The prompts for each column are given in the figure. We give the comparisons between DALL-E 2 Midjourney v5.1, Stable Diffusion XL, ERNIE ViLG 2.0, DeepFloyd, and RAPHAEL. They are given the same prompts, where the words that the human artists yearn to preserve within the generated images are highlighted in red. Only the RAPHAEL-generated images precisely reflect the prompts, while other models generate compromised results.

### 7.7 More Images Generated by RAPHAEL

We give more cases in Fig.[14](#S7.F14 "Figure 14 ‣ 7.7 More Images Generated by RAPHAEL ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), [15](#S7.F15 "Figure 15 ‣ 7.7 More Images Generated by RAPHAEL ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), [16](#S7.F16 "Figure 16 ‣ 7.7 More Images Generated by RAPHAEL ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), [17](#S7.F17 "Figure 17 ‣ 7.7 More Images Generated by RAPHAEL ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), and [18](#S7.F18 "Figure 18 ‣ 7.7 More Images Generated by RAPHAEL ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths").

![Refer to caption](/html/2305.18295/assets/x14.png)


Figure 14: These examples show that RAPHAEL can generate artistic images with varying text prompts across various styles.

![Refer to caption](/html/2305.18295/assets/x15.png)


Figure 15: These examples show that RAPHAEL can generate artistic images with varying text prompts across various styles.

![Refer to caption](/html/2305.18295/assets/x16.png)


Figure 16: These examples show that RAPHAEL can generate artistic images with varying text prompts across various styles.

![Refer to caption](/html/2305.18295/assets/x17.png)


Figure 17: These examples show that RAPHAEL can generate artistic images with varying text prompts across various styles.

![Refer to caption](/html/2305.18295/assets/x18.png)


Figure 18: These examples show that RAPHAEL can generate artistic images with varying text prompts across various styles.

### 7.8 Extension to LoRA, ControlNet, and SR-GAN

We give the results of LoRA in Fig.[19](#S7.F19 "Figure 19 ‣ 7.8 Extension to LoRA, ControlNet, and SR-GAN ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") and [20](#S7.F20 "Figure 20 ‣ 7.8 Extension to LoRA, ControlNet, and SR-GAN ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), ControlNet in Fig.[21](#S7.F21 "Figure 21 ‣ 7.8 Extension to LoRA, ControlNet, and SR-GAN ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"), and SR-GAN in Fig.[22](#S7.F22 "Figure 22 ‣ 7.8 Extension to LoRA, ControlNet, and SR-GAN ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths") and [23](#S7.F23 "Figure 23 ‣ 7.8 Extension to LoRA, ControlNet, and SR-GAN ‣ 7 Appendix ‣ RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths"). The detailed settings are given in captions.

![Refer to caption](/html/2305.18295/assets/x19.png)


Figure 19: 
Results with LoRA. We use 28 images to finetune RAPHAEL and Stable Diffusion. The prompts are "A spider-man figurine, in the night/on the moon/on the beach/none", only RAPHAEL preserves the concepts in prompts while Stable Diffusion yields compromised results.

![Refer to caption](/html/2305.18295/assets/x20.png)


Figure 20: Results with LoRA. We use 32 images to finetune RAPHAEL and Stable Diffusion. The prompts are "A boy, flower/night/sword/none", only RAPHAEL preserves the concepts in prompts while Stable Diffusion yields compromised results.

![Refer to caption](/html/2305.18295/assets/x21.png)


Figure 21: Results with ControlNet. We use the reference image to generate canny edges and adopt it as the extra constraint for RAPHAEL. The prompts for each group are "An ox, blue/none/snow/watercolor" and "Icon for game, fighting skill, monochrome/none/wooden/watercolor".

![Refer to caption](/html/2305.18295/assets/x22.png)


Figure 22: Result of 4096×\times6144 image. SR-GAN enhances the resolution of the image generated by RAPHAEL.

![Refer to caption](/html/2305.18295/assets/x23.png)


Figure 23: Result of 4096×\times6144 image. SR-GAN enhances the resolution of the image generated by RAPHAEL.

[◄](/html/2305.18294)
[![ar5iv homepage](/assets/ar5iv.png)](/)
[Feeling  
lucky?](/feeling_lucky)

[Conversion  
report](/log/2305.18295)
[Report  
an issue](https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+2305.18295)
[View original  
on arXiv](https://arxiv.org/abs/2305.18295)[►](/html/2305.18296)

[Copyright](https://arxiv.org/help/license)
[Privacy Policy](https://arxiv.org/help/policies/privacy_policy)

Generated on Thu Feb 29 05:06:34 2024 by [LaTeXML](http://dlmf.nist.gov/LaTeXML/)
