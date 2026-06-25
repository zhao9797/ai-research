# [2112.01455] Zero-Shot Text-Guided Object Generation with Dream Fields
Source: https://ar5iv.labs.arxiv.org/html/2112.01455
[2112.01455] Zero-Shot Text-Guided Object Generation with Dream Fields



# Zero-Shot Text-Guided Object Generation with Dream Fields

Ajay Jain1,2∗
  
Ben Mildenhall2
  
Jonathan T. Barron2
  
Pieter Abbeel1
  
Ben Poole2

###### Abstract

We combine neural rendering with multi-modal image and text representations to synthesize diverse 3D objects solely from natural language descriptions. Our method, Dream Fields, can generate the geometry and color of a wide range of objects without 3D supervision. Due to the scarcity of diverse, captioned 3D data, prior methods only generate objects from a handful of categories, such as ShapeNet. Instead, we guide generation with image-text models pre-trained on large datasets of captioned images from the web. Our method optimizes a Neural Radiance Field from many camera views so that rendered images score highly with a target caption according to a pre-trained CLIP model. To improve fidelity and visual quality, we introduce simple geometric priors, including sparsity-inducing transmittance regularization, scene bounds, and new MLP architectures. In experiments, Dream Fields produce realistic, multi-view consistent object geometry and color from a variety of natural language captions. ††1UC Berkeley, 2Google Research. ††∗Work done at Google. ††Correspondence to ajayj@berkeley.edu. ††Project website and code: <https://ajayj.com/dreamfields>

{strip}
![Refer to caption](/html/2112.01455/assets/x1.png)


Figure 1: Given a caption, we learn a Dream Field, a continuous volumetric representation of an object’s geometry and appearance learned with guidance from a pre-trained model. We optimize the Dream Field by rendering images of the object from random camera poses that are scored with frozen pre-trained  image and  text encoders trained on web images and alt-text. 2D views share the same underlying radiance field for consistent geometry.

![Refer to caption](/html/2112.01455/assets/x2.png)


Figure 2: Example Dream Fields rendered from four perspectives. On the right, we show transmittance from the final perspective. We create diverse outputs using the compositionality of language; these captions from MSCOCO describe three flower arrangements with different properties like context and color.

## 1 Introduction

Detailed 3D object models bring multimedia experiences to life. Games, virtual reality applications and films are each populated with thousands of object models, each designed and textured by hand with digital software.
While expert artists can author high-fidelity assets, the process is painstakingly slow and expensive.
Prior work leverages 3D datasets to synthesize shapes in the form of point clouds, voxel grids, triangle meshes, and implicit functions using generative models like GANs [[57](#bib.bib57), [4](#bib.bib4), [21](#bib.bib21), [65](#bib.bib65)]. These approaches only support a few object categories due to small labeled 3D shape datasets. But multimedia applications require a wide variety of content, and need both 3D geometry and texture.

In this work, we propose Dream Fields, a method to automatically generate open-set 3D models from natural language prompts. Unlike prior work, our method does not require any 3D training data, and uses natural language prompts that are easy to author with an expressive interface for specifying desired object properties. We demonstrate that the compositionality of language allows for flexible creative control over shapes, colors and styles.

A Dream Field is a Neural Radiance Field (NeRF) trained to maximize a deep perceptual metric with respect to both the geometry and color of a scene. NeRF and other neural 3D representations have recently been successfully applied to novel view synthesis tasks where ground-truth RGB photos are available. NeRF is trained to reconstruct images from multiple viewpoints. As the learned radiance field is shared across viewpoints, NeRF can interpolate between viewpoints smoothly and consistently. Due to its neural representation, NeRF can be sampled at high spatial resolutions unlike voxel representations and point clouds, and are easy to optimize unlike explicit geometric representations like meshes as it is topology-free.

However, existing photographs are not available when creating novel objects from descriptions alone. Instead of learning to reconstruct known input photos, we learn a radiance field such that its renderings have high semantic similarity with a given text prompt. We extract these semantics with pre-trained neural image-text retrieval models like CLIP [[46](#bib.bib46)], learned from hundreds of millions of captioned images. As NeRF’s volumetric rendering and CLIP’s image-text representations are differentiable, we can optimize Dream Fields end-to-end for each prompt. Figure Zero-Shot Text-Guided Object Generation with Dream Fields illustrates our method.

In experiments, Dream Fields learn significant artifacts if we naively optimize the NeRF scene representation with textual supervision without adding additional geometric constraints (Figure [3](#S1.F3 "Figure 3 ‣ 1 Introduction ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")). We propose general-purpose priors and demonstrate that they greatly improve the realism of results. Finally, we quantitatively evaluate open-set generation performance using a dataset of diverse object-centric prompts.

Our contributions include:

* •

  Using aligned image and text models to optimize NeRF without 3D shape or multi-view data,
* •

  Dream Fields, a simple, constrained 3D representation with neural guidance that supports diverse 3D object generation from captions in zero-shot, and
* •

  Simple geometric priors including transmittance regularization, scene bounds, and an MLP architecture that together improve fidelity.

![Refer to caption](/html/2112.01455/assets/x3.png)


Figure 3: Challenges of text-to-3D synthesis: (a) Poor generalization from limited 3D datasets: Most 3D generative models are learned on datasets of specific object categories like ShapeNet [[7](#bib.bib7)], and won’t generalize to novel concepts zero-shot. (b) Neural Radiance Fields are too flexible without multi-view supervision: NeRF learns to represent geometry and texture from scene-specific multi-view data, so it does not require a diverse dataset of objects. Yet, when only a source caption is available instead of multi-view images, NeRF produces significant artifacts (*e.g*., near field occlusions). (c) Dream Fields: We introduce general geometric priors that retain much of NeRF’s flexibility while improving realism.

## 2 Related Work

Our work is primarily inspired by DeepDream [[34](#bib.bib34)] and other methods for visualizing the preferred inputs and features of neural networks by optimizing in image space [[39](#bib.bib39), [37](#bib.bib37), [36](#bib.bib36)]. These methods enable the generation of interesting images from a pre-trained neural network without the additional training of a generative model. Closest to our work is [[35](#bib.bib35)], which studies differentiable image parameterizations in the context of style transfer. Our work replaces the style and content-based losses from that era with an image-text loss enabled by progress in contrastive representation learning on image-text datasets [[12](#bib.bib12), [46](#bib.bib46), [26](#bib.bib26), [60](#bib.bib60)].
The use of image-text models enables easy and flexible control over the style and content of generated imagery through textual prompt design. We optimize both geometry and color using the differentiable volumetric rendering and scene representation provided by NeRF, whereas [[35](#bib.bib35)] was restricted to fixed geometry and only optimized texture. Together these advances enable a fundamentally new capability: open-ended text-guided generation of object geometry and texture.

Concurrently to Dream Fields, a few early works have used CLIP [[46](#bib.bib46)] to synthesize or manipulate 3D object representations. CLIP-Forge [[49](#bib.bib49)] generates multiple object geometries from text prompts using a CLIP embedding-conditioned normalizing flow model and geometry-only decoder trained on ShapeNet categories. Still, CLIP-Forge generalizes poorly outside of ShapeNet categories and requires ground-truth multi-view images and voxel data.
Text2Shape [[9](#bib.bib9)] learns a text-conditional Wasserstein GAN [[1](#bib.bib1), [19](#bib.bib19)] to synthesize novel voxelized objects, but only supports finite resolution generation of individual ShapeNet categories.
In [[10](#bib.bib10)], object geometry is optimized evolutionarily for high CLIP score from a single view then manually colored. ClipMatrix [[25](#bib.bib25)] edits the vertices and textures of human SMPL models [[31](#bib.bib31)] to create stylized, deformable humanoid meshes.
[[44](#bib.bib44)] creates an interactive interface to edit signed-distance fields in localized regions, though they do not optimize texture or synthesize new shapes. Text-based manipulation of existing objects is complementary to us.

For images, there has been an explosion of work that leverages CLIP to guide image generation. Digital artist Ryan Murdock ([@advadnoun](https://twitter.com/advadnoun)) used CLIP to guide learning of the weights of a SIREN network [[52](#bib.bib52)], similar to NeRF but without volume rendering and focused on image generation. Katherine Crowson ([@rivershavewings](https://twitter.com/rivershavewings)) combined CLIP with optimization of VQ-GAN codes [[16](#bib.bib16)] and used diffusion models as an image prior [[14](#bib.bib14)]. Recent work from Mario Klingemann ([@quasimondo](https://twitter.com/quasimondo)) and [[43](#bib.bib43)] have shown how CLIP can be used to guide GAN models like StyleGAN [[27](#bib.bib27)]. Some works have optimized parameters of vector graphics, suggesting CLIP guidance is highly general [[23](#bib.bib23), [17](#bib.bib17), [50](#bib.bib50)]. These methods highlighted the surprising capacity of what image-text models have learned and their utility for guiding 2D generative processes. Direct text to image synthesis with generative models has also improved tremendously in recent years [[48](#bib.bib48), [61](#bib.bib61)], but requires training large generative models on large-scale datasets, making such methods challenging to directly apply to text to 3D where no such datasets exist.

There is also growing progress on generative models with NeRF-based generators trained solely from 2D imagery. However, these models are category-specific and trained on large datasets of mostly forward-facing scenes [[5](#bib.bib5), [38](#bib.bib38), [51](#bib.bib51), [20](#bib.bib20), [66](#bib.bib66)], lacking the flexibility of open-set text-conditional models. Shape-agnostic priors have been used for 3D reconstruction [[2](#bib.bib2), [58](#bib.bib58), [64](#bib.bib64)].

## 3 Background

Our method combines Neural Radiance Fields (NeRF) [[33](#bib.bib33)] with an image-text loss from [[46](#bib.bib46)]. We begin by discussing these existing methods, and then detail our improved approach and methodology that enables high quality text to object generation.

### 3.1 Neural Radiance Fields

NeRF [[33](#bib.bib33)] parameterizes a scene’s density and color using a multi-layer perceptron (MLP) with parameters θ𝜃\theta trained with a photometric loss relying on multi-view photographs of a scene.
In our simplified model, the NeRF network takes in a 3D position 𝐱𝐱\mathbf{x} and outputs parameters for an emission-absorption volume rendering model: density σθ​(𝐱)subscript𝜎𝜃𝐱\sigma\_{\theta}({\mathbf{x}}) and color 𝐜θ​(𝐱)subscript𝐜𝜃𝐱\mathbf{c}\_{\theta}({\mathbf{x}}).
Images can be rendered from desired viewpoints by integrating color along an appropriate ray, 𝐫​(t)𝐫𝑡\mathbf{r}(t), for each pixel according to the volume rendering equation:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐂​(r,θ)=∫tntfT​(𝐫,t)​σθ​(𝐫​(t))​𝐜θ​(𝐫​(t))​𝑑t,𝐂𝑟𝜃superscriptsubscriptsubscript𝑡𝑛subscript𝑡𝑓𝑇𝐫𝑡subscript𝜎𝜃𝐫𝑡subscript𝐜𝜃𝐫𝑡differential-d𝑡\displaystyle\mathbf{C}(r,\theta)=\int\_{t\_{n}}^{t\_{f}}T(\mathbf{r},t)\sigma\_{\theta}(\mathbf{r}(t))\mathbf{c}\_{\theta}(\mathbf{r}(t))dt, |  | (1) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | where ​T​(𝐫,θ,t)=exp⁡(−∫tntσθ​(𝐫​(s))​𝑑s).where 𝑇𝐫𝜃𝑡superscriptsubscriptsubscript𝑡𝑛𝑡subscript𝜎𝜃𝐫𝑠differential-d𝑠\displaystyle\text{where }T(\mathbf{r},\theta,t)=\exp\left(-\int\_{t\_{n}}^{t}\sigma\_{\theta}(\mathbf{r}(s))ds\right)\,. |  | (2) |

The integral T​(𝐫,θ,t)𝑇𝐫𝜃𝑡T(\mathbf{r},\theta,t) is known as “transmittance” and describes the probability that light along the ray will not be absorbed when traveling from tnsubscript𝑡𝑛t\_{n} (the near scene bound) to t𝑡t. In practice [[33](#bib.bib33)], these two integrals are approximated by breaking up the ray into smaller segments [ti−1,ti)subscript𝑡𝑖1subscript𝑡𝑖[t\_{i-1},t\_{i}) within which σ𝜎\sigma and 𝐜𝐜\mathbf{c} are assumed to be roughly constant:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝐂​(𝐫,θ)≈∑iTi​(1−exp⁡(−σθ​(𝐫​(ti))​δi))​𝐜θ​(𝐫​(ti))𝐂𝐫𝜃subscript𝑖subscript𝑇𝑖1subscript𝜎𝜃𝐫subscript𝑡𝑖subscript𝛿𝑖subscript𝐜𝜃𝐫subscript𝑡𝑖\displaystyle\mathbf{C}(\mathbf{r},\theta)\approx\sum\_{i}T\_{i}(1-\exp(-\sigma\_{\theta}(\mathbf{r}(t\_{i}))\delta\_{i}))\mathbf{c}\_{\theta}(\mathbf{r}(t\_{i})) |  | (3) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | Ti=exp⁡(−∑j<iσθ​(𝐫​(tj))​δj),δi=ti−ti−1.formulae-sequencesubscript𝑇𝑖subscript𝑗𝑖subscript𝜎𝜃𝐫subscript𝑡𝑗subscript𝛿𝑗subscript𝛿𝑖subscript𝑡𝑖subscript𝑡𝑖1\displaystyle T\_{i}=\exp\left(-\textstyle\sum\_{j<i}\sigma\_{\theta}(\mathbf{r}(t\_{j}))\delta\_{j}\right),\quad\delta\_{i}=t\_{i}-t\_{i-1}\,. |  | (4) |

For a given setting of MLP parameters θ𝜃\theta and pose 𝐩𝐩\mathbf{p}{}, we determine the appropriate ray for each pixel, compute rendered colors C​(𝐫,θ)𝐶𝐫𝜃C(\mathbf{r},\theta) and transmittances, and gather the results to form the rendered image, I​(θ,𝐩)𝐼𝜃𝐩I(\theta,\mathbf{p}{}) and transmittance T​(θ,𝐩)𝑇𝜃𝐩T(\theta,\mathbf{p}{}).

In order for the MLP to learn high frequency details more quickly [[55](#bib.bib55)], the input 𝐱𝐱\mathbf{x} is preprocessed by a sinusoidal positional encoding γ𝛾\gamma before being passed into the network:

|  |  |  |  |
| --- | --- | --- | --- |
|  | γ​(𝐱)=[cos⁡(2l​𝐱),sin⁡(2l​𝐱)]l=0L−1,𝛾𝐱superscriptsubscriptsuperscript2𝑙𝐱superscript2𝑙𝐱𝑙0𝐿1\displaystyle\gamma(\mathbf{x})=\left[\cos(2^{l}\mathbf{x}),\sin(2^{l}\mathbf{x})\right]\_{l=0}^{L-1}\,, |  | (5) |

where L𝐿L is referred to as the number of “levels” of positional encoding. In our implementation, we specifically apply the integrated positional encoding (IPE) proposed in mip-NeRF to combat aliasing artifacts [[3](#bib.bib3)] combined with a random Fourier positional encoding basis [[55](#bib.bib55)] with frequency components sampled according to

|  |  |  |  |
| --- | --- | --- | --- |
|  | ω=2u​𝐝,where ​u∼𝒰​[0,L],𝐝∼𝒰​(𝕊2).formulae-sequence𝜔superscript2𝑢𝐝formulae-sequencesimilar-towhere 𝑢𝒰0𝐿similar-to𝐝𝒰superscript𝕊2\displaystyle\mathbf{\omega}=2^{u}\mathbf{d},\quad\text{where }u\sim\mathcal{U}[0,L],\,\,\mathbf{d}\sim\mathcal{U}(\mathbb{S}^{2})\,. |  | (6) |

### 3.2 Image-text models

Large-scale datasets of images paired with associated text have enabled training large-scale models that can accurately score whether an image and an associated caption are likely to correspond [[46](#bib.bib46), [26](#bib.bib26), [12](#bib.bib12)].
These models consist of an image encoder 𝐠𝐠\mathbf{g}, and text encoder 𝐡𝐡\mathbf{h}, that map images and text into a shared embedding space. Given a sentence y𝑦y and an image 𝐈𝐈\mathbf{I}{}, these image-text models produce a scalar score: 𝐠​(𝐈)T​𝐡​(𝐲)𝐠superscript𝐈T𝐡𝐲\mathbf{g}(\mathbf{I}{})^{\mathrm{T}}\mathbf{h}(\mathbf{y}) that is high when the text is a good description of the image, and low when the the image and text are mismatched. Note that the embeddings 𝐠​(𝐈)𝐠𝐈\mathbf{g}(\mathbf{I}{}) and 𝐡​(𝐲)𝐡𝐲\mathbf{h}(\mathbf{y}) are often normalized, i.e. ‖𝐠​(𝐈)‖=‖𝐡​(𝐲)‖=1norm𝐠𝐈norm𝐡𝐲1\|\mathbf{g}(\mathbf{I}{})\|=\|\mathbf{h}(\mathbf{y})\|=1. Training is typically performed with a symmetric version of the InfoNCE loss [[40](#bib.bib40), [45](#bib.bib45)] that aims to maximize a variational lower bound on the mutual information between images and text. Prior work has shown that once trained, the image and text encoders are useful for a number of downstream tasks [[46](#bib.bib46), [60](#bib.bib60)]. In [[48](#bib.bib48)], the image and text encoders are used to score the correspondence of outputs of a generative image model to a target caption [[48](#bib.bib48)]. We build on this work by optimizing a volume to produce a high-scoring image, not just reranking.

## 4 Method

In this section, we develop Dream Fields: a zero-shot object synthesis method given only a natural language caption.

### 4.1 Object representation

Building on the NeRF scene representation (Section [3.1](#S3.SS1 "3.1 Neural Radiance Fields ‣ 3 Background ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")), a Dream Field optimizes an MLP with parameters θ𝜃\theta that produces outputs σθ​(𝐱)subscript𝜎𝜃𝐱\sigma\_{\theta}(\mathbf{x}) and 𝐜θ​(𝐱)subscript𝐜𝜃𝐱\mathbf{c}\_{\theta}(\mathbf{x}) representing the differential volume density and color of a scene at every 3D point 𝐱𝐱\mathbf{x}. This field expresses object geometry via the density network. Our object representation is only dependent on 3D coordinates and not the camera’s viewing direction, as we did not find it beneficial. Given a camera pose 𝐩𝐩\mathbf{p}{}, we can render an image 𝐈​(θ,𝐩)𝐈𝜃𝐩\mathbf{I}{}(\theta,\mathbf{p}{}) and compute the transmittance T​(θ,𝐩)𝑇𝜃𝐩T(\theta,\mathbf{p}{}) using N𝑁N segments via ([4](#S3.E4 "Equation 4 ‣ 3.1 Neural Radiance Fields ‣ 3 Background ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")). Segments are spaced at roughly equal intervals with random jittering along the ray. The number of segments, N𝑁N, determines the fidelity of the rendering. In practice, we fix it to 192 during optimization.

### 4.2 Objective

How can we train a Dream Field to represent a given caption? If we assume that an object can be described similarly when observed from any perspective, we can randomly sample poses and try to enforce that the rendered image matches the caption at all poses. We can implement this idea by using a CLIP network to measure the match between a caption and image given parameters θ𝜃\theta and pose 𝐩𝐩\mathbf{p}{}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒCLIP​(θ,pose​𝐩,caption​y)=−𝐠​(𝐈​(θ,𝐩))T​𝐡​(𝐲)subscriptℒCLIP𝜃pose𝐩caption𝑦𝐠superscript𝐈𝜃𝐩T𝐡𝐲\mathcal{L}\_{\mathrm{CLIP}}{}(\theta,\text{pose}~{}\mathbf{p}{},\text{caption}~{}y)=-\mathbf{g}(\mathbf{I}{}(\theta,\mathbf{p}{}))^{\mathrm{T}}\mathbf{h}(\mathbf{y}) |  | (7) |

where 𝐠​(⋅)𝐠⋅\mathbf{g}(\cdot) and 𝐡​(⋅)𝐡⋅\mathbf{h}(\cdot) are aligned representations of image and text semantics, and 𝐈​(θ,𝐩)𝐈𝜃𝐩\mathbf{I}{}(\theta,\mathbf{p}{}) is a rendered image of the scene from camera pose 𝐩𝐩\mathbf{p}{}. Each iteration of training, we sample a pose 𝐩𝐩\mathbf{p}{} from a prior distribution, render 𝐈𝐈\mathbf{I}{}, and minimize ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}}{} with respect to the parameters of the Dream Field MLP, θ𝜃\theta. Equation ([7](#S4.E7 "Equation 7 ‣ 4.2 Objective ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) measures the similarity of an image and the provided caption in feature space.

We primarily use image and text encoders from CLIP [[46](#bib.bib46)], which has a Vision Transformer image encoder 𝐠​(⋅)𝐠⋅\mathbf{g}(\cdot) [[15](#bib.bib15)] and masked transformer text encoder 𝐡​(⋅)𝐡⋅\mathbf{h}(\cdot) [[56](#bib.bib56)] trained contrastively on a large dataset of 400M captioned 2242 images. We also use a baseline Locked Image-Text Tuning (LiT) ViT B/32 model from [[60](#bib.bib60)] trained via the same procedure as CLIP on a larger dataset of billions of higher-resolution (2882) captioned images. The LiT training set was collected following a simplified version of the ALIGN web alt-text dataset collection process [[26](#bib.bib26)] and includes noisy captions.

Figure Zero-Shot Text-Guided Object Generation with Dream Fields shows a high-level overview of our method.
DietNeRF [[24](#bib.bib24)] proposed a related semantic consistency regularizer for NeRF based on the idea that “a bulldozer is a bulldozer from any perspective”. The method computed the similarity of a rendered and a real image. In contrast, ([7](#S4.E7 "Equation 7 ‣ 4.2 Objective ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) compares rendered images and a *caption*, allowing it to be used in zero-shot settings when there are no object photos.

### 4.3 Challenges with CLIP guidance

Due to their flexibility, Neural Radiance Fields are capable of high-fidelity novel view synthesis on a tremendous diversity of real-world scenes when supervised with multi-view consistent images. Their reconstruction loss will typically learn to remove artifacts like spurious density when sufficiently many input images are available. However, we find that the NeRF scene representation is too unconstrained when trained solely with ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} ([7](#S4.E7 "Equation 7 ‣ 4.2 Objective ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) alone from a discrete set of viewpoints, resulting in severe artifacts that satisfy ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} but are not visually compatible according to humans (see Figure [3](#S1.F3 "Figure 3 ‣ 1 Introduction ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")b).
NeRF learns high-frequency and near-field [[62](#bib.bib62)] artifacts like partially-transparent “floating“ regions of density. It also fills the entire camera viewport rather than generating individual objects. Geometry is unrealistic, though textures reflect the caption, reminiscent of the artifacts in Deep Dream feature visualizations [[34](#bib.bib34), [39](#bib.bib39)].

### 4.4 Pose sampling

Image data augmentations such as random crops are commonly used to improve and regularize image generation in DeepDream[[34](#bib.bib34)] and related work. Image augmentations can only use in-plane 2D transformations. Dream Fields support 3D data augmentations by sampling different camera pose extrinsics at each training iteration. We uniformly sample camera azimuth in 360∘ around the scene, so each training iteration sees a different orientation of the object. As the underlying scene representation is shared, this improves the realism of object geometry. For example, sampling azimuth in a narrow interval tended to create flat, billboard geometry.

The camera elevation, focal length and distance from the subject can also be augmented, but we did not find this necessary. Instead, we use a fixed camera focal length during optimization that is scaled by mfocal=1.2subscript𝑚focal1.2m\_{\mathrm{focal}}=1.2 to enlarge the object 20%. Rendering cost is constant in the focal length.

![Refer to caption](/html/2112.01455/assets/x4.png)


Figure 4: To encourage coherent foreground objects, Dream Fields train with 3 types of background augmentations: blurred Gaussian noise, textures and checkerboards. At test time, we render with a white background. Prompt: “A sculpture of a rooster.”

### 4.5 Encouraging coherent objects through sparsity

To remove near-field artifacts and spurious density, we regularize the opacity of Dream Field renderings. Our best results maximize the average transmittance of rays passing through the volume up to a target constant. Transmittance is the probability that light along ray r𝑟r is not absorbed by participating media when passing between point t𝑡t along the ray and the near plane at tnsubscript𝑡𝑛t\_{n} ([2](#S3.E2 "Equation 2 ‣ 3.1 Neural Radiance Fields ‣ 3 Background ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")).
We approximate the total transmittance along the ray as the joint probability of light passing through N𝑁N discrete segments of the ray according to Eq. ([4](#S3.E4 "Equation 4 ‣ 3.1 Neural Radiance Fields ‣ 3 Background ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")).
Then, we define the following transmittance loss:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ℒTsubscriptℒ𝑇\displaystyle\mathcal{L}\_{T} | =−min⁡(τ,mean⁡(T​(θ,𝐩)))absent𝜏mean𝑇𝜃𝐩\displaystyle=-\min\!\left(\tau,\operatorname{mean}\!\left(T(\theta,\mathbf{p}{})\right)\right) |  | (8) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ℒtotalsubscriptℒtotal\displaystyle\mathcal{L}\_{\text{total}} | =ℒCLIP+λ​ℒTabsentsubscriptℒCLIP𝜆subscriptℒ𝑇\displaystyle=\mathcal{L}\_{\mathrm{CLIP}}+\lambda\mathcal{L}\_{T} |  | (9) |

This encourages a Dream Field to increase average transmittance up to a target transparency τ𝜏\tau. We use τ=88%𝜏percent88\tau=88\% in experiments.
τ𝜏\tau is annealed in from τ=40%𝜏percent40\tau=40\% over 500 iterations to smoothly introduce transparency, which improves scene geometry and is essential to prevent completely transparent scenes. Scaling 1−τ∝f2/d2proportional-to1𝜏superscript𝑓2superscript𝑑21-\tau\propto f^{2}/d^{2} preserves object cross sectional area for different focal and object distances.

When the rendering is alpha-composited with a simple white or black background during training, we find that the average transmittance approaches τ𝜏\tau, but the scene is diffuse as the optimization populates the background. Augmenting the scene with random background images leads to coherent objects. Dream Fields use Gaussian noise, checkerboard patterns and the random Fourier textures from [[35](#bib.bib35)] as backgrounds. These are smoothed with a Gaussian blur with randomly sampled standard deviation. Background augmentations and a rendering during training are shown in Figure [4](#S4.F4 "Figure 4 ‣ 4.4 Pose sampling ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields").

We qualitatively compare ([9](#S4.E9 "Equation 9 ‣ 4.5 Encouraging coherent objects through sparsity ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) to baseline sparsity regularizers in Figure [5](#S4.F5 "Figure 5 ‣ 4.6 Localizing objects and bounding scene ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields"). Our loss is inspired by the multiplicative opacity gating used by [[35](#bib.bib35)]. However, the gated loss has optimization challenges in practice due in part to its non-convexity. The simplified additive loss is more stable, and both are significantly sharper than prior approaches for sparsifying Neural Radiance Fields.

### 4.6 Localizing objects and bounding scene

When Neural Radiance Fields are trained to reconstruct images, scene contents will align with observations in a consistent fashion, such as the center of the scene in NeRF’s Realistic Synthetic dataset [[33](#bib.bib33)]. Dream Fields can place density away from the center of the scene while still satisfying the CLIP loss as natural images in CLIP’s training data will not always be centered. During training, we maintain an estimate of the 3D object’s origin and shift rays accordingly. The origin is tracked via an exponential moving average of the center of mass of rendered density.
To prevent objects from drifting too far, we bound the scene inside a cube by masking the density σθsubscript𝜎𝜃\sigma\_{\theta}.

![Refer to caption](/html/2112.01455/assets/x5.png)


Figure 5: Our transmittance losses and background augmentations are complementary. Top: Without background augmentations, priors on transmittance (right three columns) do not remove low-density structures. NeRF’s density perturbations improve coherence, but cloudy artifacts remain. Bottom: When the object is alpha composited with random backgrounds during training, CLIP fills the scene with opaque material to conceal the background. However, gated and our simplified additive transmittance regularizers both limit the opacity of the volume successfully and lead to a sharper object. Inset panels depict transmittance. Prompt: “an illustration of a pumpkin on the vine.”

### 4.7 Neural scene representation architecture

The NeRF network architecture proposed in [[33](#bib.bib33)] parameterizes scene density with a simple 8-layer MLP of constant width, and radiance with an additional two layers. We use a residual MLP architecture instead that introduces residual connections around every two dense layers. Within a residual block, we find it beneficial to introduce Layer Normalization at the beginning and increase the feature dimension in a bottleneck fashion. Layer Normalization improves optimization on challenging prompts. To mitigate vanishing gradient issues in highly transparent scenes, we replace ReLU activations with Swish [[47](#bib.bib47)] and rectify the predicted density σθsubscript𝜎𝜃\sigma\_{\theta} with a softplus function. Our MLP architecture uses 280K parameters per scene, while NeRF uses 494K parameters.

## 5 Evaluation

We evaluate the consistency of generated objects with their captions and the importance of scene representation, then show qualitative results and test whether Dream Fields can generalize compositionally.
Ablations analyze regularizers, CLIP and camera poses. Finally, supplementary materials have further examples and videos.

### 5.1 Experimental setup

3D reconstruction methods are evaluated by comparing the learned geometry with a ground-truth reference model, e.g. with Chamfer Distance. Novel view synthesis techniques like LLFF [[32](#bib.bib32)] and NeRF do not have ground truth models, but compare renderings to pixel-aligned ground truth images from held-out poses with PSNR or LPIPS, a deep perceptual metric [[63](#bib.bib63)].

As we do not have access to diverse captioned 3D models or captioned multi-view data, Dream Fields are challenging to evaluate with geometric and image reference-based metrics. Instead, we use the CLIP R-Precision metric [[41](#bib.bib41)] from the text-to-image generation literature to measure how well rendered images align with the true caption. In the context of text-to-image synthesis, R-Precision measures the fraction of generated images that a retrieval model associates with the caption used to generate it. We use a different CLIP model for learning the Dream Field and computing the evaluation metric. As with NeRF evaluation, the image is rendered from a held-out pose. Dream Fields are optimized with cameras at a 30∘superscript3030^{\circ} angle of elevation and evaluated at 45∘superscript4545^{\circ} elevation. For quantitative metrics, we render at resolution 1682 during training as in [[24](#bib.bib24)]. For figures, we train with a 50%percent\% higher resolution of 2522.

We collect an object-centric caption dataset with 153 captions as a subset of the Common Objects in Context (COCO) dataset [[28](#bib.bib28)] (see supplement for details). Object centric examples are those that have a single bounding box annotation and are filtered to exclude those captioned with certain phrases like “extreme close up”. COCO includes 5 captions per image, but only one is used for generation. Hyperparameters were manually tuned for perceptual quality on a set of 20-74 distinct captions from the evaluation set, and are shared across all other scenes. Additional dataset details and hyperparameters are included in the supplement.

### 5.2 Analyzing retrieval metrics

In the absence of 3D training data, Dream Fields use geometric priors
to constrain generation. To evaluate each proposed technique, we start from a simplified baseline Neural Radiance Field largely following [[33](#bib.bib33)] and introduce the priors one-by-one. We generate two objects per COCO caption using different seeds, for a total of 306 objects. Objects are synthesized with 10K iterations of CLIP ViT B/16 guided optimization of 168×\times168 rendered images, bilinearly upsampled to the contrastive model’s input resolution for computational efficiency. R-Precision is computed with CLIP ViT B/32 [[46](#bib.bib46)] and LiTuuuu{}\_{\text{uu}} B/32 [[60](#bib.bib60)] to measure the alignment of generations with the source caption.

Table [5.2](#S5.SS2 "5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") reports results. The most significant improvements come from sparsity, scene bounds and architecture. As an oracle, the ground truth images associated with object-centric COCO captions have high R-Precision. The NeRF representation converges poorly and introduces aliasing and banding artifacts, in part from its use of axis-aligned positional encodings.

We instead combine mip-NeRF’s integrated positional encodings with random Fourier features, which improves qualitative results and removes a bias toward axis-aligned structures. However, the effect on precision is neutral or negative. The transmittance loss ℒTsubscriptℒ𝑇\mathcal{L}\_{T} in combination with background augmentations significantly improves retrieval precision ++18% and ++15.6%, while the transmittance loss is not sufficient on its own. This is qualitatively shown in Figure [5](#S4.F5 "Figure 5 ‣ 4.6 Localizing objects and bounding scene ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields"). Our MLP architecture with residual connections, normalization, bottleneck-style feature dimensions and smooth nonlinearities further improves the R-Precision ++8% and ++2%. Bounding the scene to a cube improves retrieval ++13% and ++11%. The additional bounds explicitly mask density σ𝜎\sigma and concentrate samples along each ray.

We also scale up Dream Fields by optimizing with an image-text model trained on a larger captioned dataset of 3.6B images from [[60](#bib.bib60)]. We use a ViT B/32 model with image and text encoders trained from scratch. This corresponds to the uu configuration from [[60](#bib.bib60)], following the CLIP training procedure to learn both encoders contrastively. The LiTuuuu{}\_{\text{uu}} ViT encoder used in our experiments takes higher resolution 2882 images while CLIP is trained with 2242 inputs. Still, LiTuuuu{}\_{\text{uu}} B/32 is more compute-efficient than CLIP B/16 due to the larger patch size in the first layer.

LiTuuuu{}\_{\text{uu}} does not significantly help R-Precision when optimizing Dream Fields with low resolution renderings, perhaps because the CLIP B/32 model used for evaluation is trained on the same dataset as the CLIP B/16 model in earlier rows. Optimizing for longer with higher resolution 2522 renderings closes the gap. LiTuuuu{}\_{\text{uu}} improves visual quality and sharpness (Appendix [A](#A1 "Appendix A Qualitative results and ablations ‣ Acknowledgements ‣ 7 Conclusion ‣ 6 Discussion and limitations ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")), suggesting that improvements in multimodal image-text models transfer to 3D generation.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Method | R-Precision ↑↑\uparrow | | |
|  | CLIP B/32 |  | LiTuuuu{}\_{\text{uu}} B/32 |
| Baseline | COCO GT images | 77.1±plus-or-minus\pm3.4 |  | 75.2±plus-or-minus\pm3.5 |
| Simplified NeRF | 31.4±plus-or-minus\pm2.7 |  | 10.8±plus-or-minus\pm1.8 |
| Positional encoding | + mip-NeRF IPE | 29.7±plus-or-minus\pm2.6 |  | 12.4±plus-or-minus\pm1.9 |
| + Higher freq. Fourier features | 24.2±plus-or-minus\pm2.5 |  | 10.5±plus-or-minus\pm1.8 |
| Sparsity, augment | + random crops | 25.8±plus-or-minus\pm2.5 |  | 10.5±plus-or-minus\pm1.8 |
| + transmittance loss | 23.7±plus-or-minus\pm2.4 |  | 7.6±plus-or-minus\pm1.5 |
| + background aug. | 44.1±plus-or-minus\pm2.8 |  | 26.1±plus-or-minus\pm2.5 |
| Scene param. | + MLP architecture | 52.0±plus-or-minus\pm2.9 |  | 27.8±plus-or-minus\pm2.6 |
| + scene bounds | 65.4±plus-or-minus\pm2.7 |  | 38.9±plus-or-minus\pm2.8 |
| + track origin | 59.8±plus-or-minus\pm2.8 |  | 34.6±plus-or-minus\pm2.7 |
| Scaling | + LiTuuuu{}\_{\text{uu}} ViT B/32 | 59.5±plus-or-minus\pm2.8 |  | – |
| + 20K iterations, 2522 renders | 68.3±plus-or-minus\pm2.7 |  | – |

Table 1: When used together, geometric priors improve caption retrieval precision. We start with a simplified version of the NeRF scene representation and add in one prior at a time until all are used in conjunction. Captions are retrieved from rendered images of the generated objects at held-out camera poses using CLIP’s ViT B/32. Objects are generated with ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} guidance from the pre-trained CLIP ViT B/16 except in scaling experiments where we experiment with the higher-resolution LiTuuuu{}\_{\text{uu}} B/32 model.

![Refer to caption](/html/2112.01455/assets/x6.png)

![Refer to caption](/html/2112.01455/assets/x7.png)

Figure 6: Compositional object generation. Dream Fields allow users to express specific artistic styles via detailed captions.
Top two rows: Similar to text-to-image experiments in [[48](#bib.bib48)], we generate objects with the caption “armchair in the shape of an avocado. armchair imitating avocado.” Bottom: Generations vary the texture of a single snail. Captions follow the template “a snail made of baguette. a snail with the texture of baguette” Results are not cherry-picked.

### 5.3 Compositional generation

In Figure [6](#S5.F6 "Figure 6 ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields"), we show non-cherrypicked generations that test the compositional generalization of Dream Fields to fine-grained variations in captions taken from the website of [[48](#bib.bib48)]. We independently vary the object generated and stylistic descriptors like shape and materials.
DALL-E [[48](#bib.bib48)] also had a remarkable ability to combine concepts in prompts out of distribution, but was limited to 2D image synthesis. Dream Fields produces compositions of concepts in 3D, and supports fine-grained variations in prompts across several categories of objects. Some geometric details are not realistic, however.
For example, generated snails have eye stalks attached to their shell rather than body, and the generated green vase is blurry.

### 5.4 Model ablations

| Method | Loss or parameterization | R-Prec. |
| --- | --- | --- |
| No regularizer | ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} ([7](#S4.E7 "Equation 7 ‣ 4.2 Objective ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) | 35.3 |
| Perturb σ𝜎\sigma [[33](#bib.bib33)] | σ=softplus⁡(fθ​(𝐱)+ϵ)𝜎softplussubscript𝑓𝜃𝐱italic-ϵ\sigma=\operatorname{softplus}(f\_{\theta}(\mathbf{x})+\epsilon) | 47.7 |
| Beta prior [[30](#bib.bib30)] | ([10](#S5.E10 "Equation 10 ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) | 50.3 |
| Gated T𝑇T [[35](#bib.bib35)] | −mean⁡(T​(θ,𝐩))⋅ℒCLIP⋅mean𝑇𝜃𝐩subscriptℒCLIP-\operatorname{mean}(T(\theta,\mathbf{p}{}))\cdot\mathcal{L}\_{\mathrm{CLIP}} | 34.6 |
| Clipped gated T𝑇T | −ℒT⋅ℒCLIP⋅subscriptℒ𝑇subscriptℒCLIP-\mathcal{L}\_{T}\cdot\mathcal{L}\_{\mathrm{CLIP}} ([11](#S5.E11 "Equation 11 ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) | 62.1 |
| Clipped additive T𝑇T | ℒCLIP+λ​ℒTsubscriptℒCLIP𝜆subscriptℒ𝑇\mathcal{L}\_{\mathrm{CLIP}}+\lambda\mathcal{L}\_{T} ([9](#S4.E9 "Equation 9 ‣ 4.5 Encouraging coherent objects through sparsity ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) | 62.1 |

Table 2: Ablating sparsity regularizers. Optimization is done for 10K iterations at 1682 resolution with LiTuuuu{}\_{\text{uu}} ViT B/32 and background augmentation, and retrieval uses CLIP ViT B/32. For the purposes of ablation, we run one seed per caption (153 runs).

Ablating sparsity regularizers    
While we regularize the mean transmittance, other sparsity losses are possible.
We compare unregularized Dream Fields, perturbations to the density σ𝜎\sigma [[33](#bib.bib33)], regularization with a beta prior on transmittance [[30](#bib.bib30)], multiplicative gating versions of ℒTsubscriptℒ𝑇\mathcal{L}\_{T} and our additive ℒTsubscriptℒ𝑇\mathcal{L}\_{T} regularizer in Figure [5](#S4.F5 "Figure 5 ‣ 4.6 Localizing objects and bounding scene ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields").
On real-world scenes, NeRF added Gaussian noise to network predictions of the density prior to rectification as a regularizer. This can encourage sharper boundary definitions as small densities will often be zeroed by the perturbation. The beta prior from Neural Volumes [[30](#bib.bib30)] encourages rays to either pass through the volume or be completely occluded:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒtotalbeta=ℒCLIP+λ⋅mean⁡(log⁡T​(θ,𝐩)+log⁡(1−T​(θ,𝐩)))superscriptsubscriptℒtotalbetasubscriptℒCLIP⋅𝜆mean𝑇𝜃𝐩1𝑇𝜃𝐩\mathcal{L}\_{\mathrm{total}}^{\text{beta}}=\mathcal{L}\_{\mathrm{CLIP}}+\lambda\cdot\operatorname{mean}\!\left(\log T(\theta,\mathbf{p}{})+\log(1-T(\theta,\mathbf{p}{}))\right) |  | (10) |

The multiplicative loss is inspired by the opacity scaling of [[35](#bib.bib35)] for feature visualization. We scale the CLIP loss by a clipped mean transmittance:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ℒtotal=min⁡(τ,mean⁡(T​(θ,𝐩)))⋅ℒCLIPsubscriptℒtotal⋅𝜏mean𝑇𝜃𝐩subscriptℒCLIP\mathcal{L}\_{\text{total}}=\min(\tau,\;\operatorname{mean}(T(\theta,\mathbf{p}{})))\cdot\mathcal{L}\_{\mathrm{CLIP}} |  | (11) |

Table [2](#S5.T2 "Table 2 ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") compares the regularizers, showing that density perturbations and the beta prior improve R-Precision ++12.4% and ++15%, respectively. Scenes with clipped mean transmittance regularization best align with their captions, ++26.8% over the baseline.
The beta prior can fill scenes with opaque material even without background augmentations as it encourages both high and low transmittance. Multiplicative gating works well when clipped to a target and with background augmentations, but is also non-convex and sensitive to hyperparameters.
Figure [7](#S5.F7 "Figure 7 ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") shows the effect of varying the target transmittance τ𝜏\tau with an additive loss.

![Refer to caption](/html/2112.01455/assets/x8.png)


Figure 7: The target transmittance τ𝜏\tau affects the size of generated objects. Inset panels depict transmittance. Prompt from Object Centric COCO: “A cake toped [sic] with white frosting flowers with chocolate centers.”

#### Varying the image-text model

We compare different image and text representations h​(⋅),g​(⋅)

ℎ⋅𝑔⋅h(\cdot),g(\cdot) used in ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} ([7](#S4.E7 "Equation 7 ‣ 4.2 Objective ‣ 4 Method ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) and for retrieval metrics. Table [3](#S5.T3 "Table 3 ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") shows the results. CLIP B/32, B/16 and LiTuuuu{}\_{\text{uu}} B/32 all have high retrieval precision, indicating they can synthesize objects generally aligned with the provided captions. CLIP B/32 performs the best, outperforming the more compute intensive CLIP B/16 model. The architectures differ in the number of pixels encoded in each token supplied to the Transformer backbone, i.e. the ViT patch size. A larger patch size may be sufficient due to the low resolution of renders: 1682 cropped to 1542, then upsampled to CLIP’s input size of 2242. Qualitatively, training with LiTuuuu{}\_{\text{uu}} B/32 produced the most detailed geometry and textures, suggesting that open-set evaluation is challenging.

|  | Retrieval model R-Precision | | |
| --- | --- | --- | --- |
| Optimized model | CLIP B/32 | CLIP B/16 | LiTuuuu{}\_{\text{uu}} B/32 |
| COCO GT | 77.1±plus-or-minus\pm3.4 | 79.1±plus-or-minus\pm3.3 | 75.2±plus-or-minus\pm3.5 |
| CLIP B/32 [[46](#bib.bib46)] | (86.6±plus-or-minus\pm2.0) | 74.2±plus-or-minus\pm2.5 | 42.8±plus-or-minus\pm2.8 |
| CLIP B/16 [[46](#bib.bib46)] | 59.8±plus-or-minus\pm2.8 | (93.5±plus-or-minus\pm1.4) | 35.6±plus-or-minus\pm2.7 |
| LiTuuuu{}\_{\text{uu}} B/32 | 59.5±plus-or-minus\pm2.8 | 66.7±plus-or-minus\pm2.7 | (88.9±plus-or-minus\pm1.8) |

Table 3: The aligned image-text representation used to optimize Dream Fields influences their quantitative validation R-Precision according to a held-out retrieval model. All contrastive models produce high retrieval precision, though qualitatively CLIP B/32 produced overly smooth and simplified objects. We optimize for 10K iterations at 1682 resolution. (Italicized) metrics use the optimized model at a held-out pose and indicate Dream Fields overfit.

Varying optimized camera poses    
Each training iteration, Dream Fields samples a camera pose 𝐩𝐩\mathbf{p} to render the scene. In experiments, we used a full 360∘ sampling range for the camera’s azimuth, and fixed the elevation. Figure [8](#S5.F8 "Figure 8 ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") shows multiple views of a bird when optimizing with smaller azimuth ranges. In the left-most column, a view from the central azimuth (frontal) is shown, and is realistic for all training configurations. Views from more extreme angles (right, left, rear view columns) have artifacts when the Dream Field is optimized with narrow azimuth ranges. Training with diverse cameras is important for viewpoint generalization.

![Refer to caption](/html/2112.01455/assets/x9.png)


Figure 8: Training with diversely sampled camera poses improves generalization across views. In the top row, we sample camera azimuth from a single viewpoint. The rendered view from the same perspective (left column) is realistic, but the object structure is poor as seen from other angles. Qualitative results improve with larger sampling intervals, with the best results from 360∘ sampling.

## 6 Discussion and limitations

There are a number of limitations in Dream Fields.
Generation requires iterative optimization, which can be expensive. 2K-20K iterations are sufficient for most objects, but more detail emerges when optimizing longer. Meta-learning [[54](#bib.bib54)] or amortization [[42](#bib.bib42)] could speed up synthesis.

We use the same prompt at all perspectives. This can lead to repeated patterns on multiple sides of an object. The target caption could be varied across different camera poses.
Many of the prompts we tested involve multiple subjects, but we do not target complex scene generation [[11](#bib.bib11), [8](#bib.bib8), [6](#bib.bib6), [13](#bib.bib13)] partly because CLIP poorly encodes spatial relations [[29](#bib.bib29), [53](#bib.bib53)]. Scene layout could be handled in a post-processing step.

The image-text models we use to score renderings are not perfect even on ground truth training images, so improvements in image-text models may transfer to 3D generation. Our reliance on pre-trained models inherits their harmful biases. Identifying methods that can detect and remove these biases is an important direction if these methods are to be useful for larger-scale asset generation.

## 7 Conclusion

Our work has begun to tackle the difficult problem of object generation from text. By combining scalable multi-modal image-text models and multi-view consistent differentiable neural rendering with simple object priors, we are able to synthesize both geometry and color of 3D objects across a large variety of real-world text prompts. The language interface allows users to control the style and shape of the results, including materials and categories of objects, with easy-to-author prompts. We hope these methods will enable rapid asset creation for artists and multimedia applications.

## Acknowledgements

We thank Xiaohua Zhai, Lucas Beyer and Andreas Steiner for providing pre-trained models on the LiT 3.6B dataset, Paras Jain, Kevin Murphy, Matthew Tancik and Alireza Fathi for useful discussions and feedback on our work, and many colleagues at Google for building and supporting key infrastructure. Ajay Jain is supported in part by the NSF GRFP under Grant Number DGE 1752814.

## References

* [1]

  Martin Arjovsky, Soumith Chintala, and Léon Bottou.
  Wasserstein generative adversarial networks.
  ICML, 2017.
* [2]

  Jonathan T. Barron and Jitendra Malik.
  Shape, illumination, and reflectance from shading.
  TPAMI, 2015.
* [3]

  Jonathan T. Barron, Ben Mildenhall, Matthew Tancik, Peter Hedman, Ricardo
  Martin-Brualla, and Pratul P. Srinivasan.
  Mip-NeRF: A multiscale representation for anti-aliasing neural
  radiance fields.
  ICCV, 2021.
* [4]

  Ruojin Cai, Guandao Yang, Hadar Averbuch-Elor, Zekun Hao, Serge Belongie, Noah
  Snavely, and Bharath Hariharan.
  Learning gradient fields for shape generation.
  ECCV, 2020.
* [5]

  Eric Chan, Marco Monteiro, Petr Kellnhofer, Jiajun Wu, and Gordon Wetzstein.
  pi-gan: Periodic implicit generative adversarial networks for
  3d-aware image synthesis.
  CVPR, 2021.
* [6]

  Angel Chang, Will Monroe, Manolis Savva, Christopher Potts, and Christopher D.
  Manning.
  Text to 3d scene generation with rich lexical grounding.
  ACL-IJCNLP, 2015.
* [7]

  Angel X Chang, Thomas Funkhouser, Leonidas Guibas, Pat Hanrahan, Qixing Huang,
  Zimo Li, Silvio Savarese, Manolis Savva, Shuran Song, Hao Su, et al.
  Shapenet: An information-rich 3d model repository.
  arXiv preprint arXiv:1512.03012, 2015.
* [8]

  Angel X Chang, Manolis Savva, and Christopher D Manning.
  Learning spatial knowledge for text to 3D scene generation.
  EMNLP, 2014.
* [9]

  Kevin Chen, Christopher B. Choy, Manolis Savva, Angel X. Chang, Thomas A.
  Funkhouser, and Silvio Savarese.
  Text2shape: Generating shapes from natural language by learning joint
  embeddings.
  CoRR, abs/1803.08495, 2018.
* [10]

  Eric Chu.
  Evolving evocative 2d views of generated 3d objects.
  NeurIPS Creativity and Design Workshop, 2021.
* [11]

  Bob Coyne and Richard Sproat.
  Wordseye: an automatic text-to-scene conversion system.
  Computer graphics and interactive techniques, 2001.
* [12]

  Karan Desai and Justin Johnson.
  VirTex: Learning Visual Representations from Textual Annotations.
  CVPR, 2021.
* [13]

  Terrance DeVries, Miguel Angel Bautista, Nitish Srivastava, Graham W. Taylor,
  and Joshua M. Susskind.
  Unconstrained scene generation with locally conditioned radiance
  fields.
  arXiv, 2021.
* [14]

  Prafulla Dhariwal and Alex Nichol.
  Diffusion models beat gans on image synthesis.
  arXiv:2105.05233, 2021.
* [15]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  ICLR, 2021.
* [16]

  Patrick Esser, Robin Rombach, and Bjorn Ommer.
  Taming transformers for high-resolution image synthesis.
  CVPR, 2021.
* [17]

  Kevin Frans, Lisa B. Soros, and Olaf Witkowski.
  Clipdraw: Exploring text-to-drawing synthesis through language-image
  encoders.
  CoRR, 2021.
* [18]

  Gabriel Goh, Nick Cammarata †, Chelsea Voss †, Shan Carter, Michael Petrov,
  Ludwig Schubert, Alec Radford, and Chris Olah.
  Multimodal neurons in artificial neural networks.
  Distill, 2021.
  https://distill.pub/2021/multimodal-neurons.
* [19]

  Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley,
  Sherjil Ozair, Aaron Courville, and Yoshua Bengio.
  Generative adversarial nets.
  NeurIPS, 2014.
* [20]

  Jiatao Gu, Lingjie Liu, Peng Wang, and Christian Theobalt.
  Stylenerf: A style-based 3d-aware generator for high-resolution image
  synthesis, 2021.
* [21]

  Kunal Gupta and Manmohan Chandraker.
  Neural mesh flow: 3d manifold mesh generationvia diffeomorphic flows,
  2020.
* [22]

  Jonathan Heek, Anselm Levskaya, Avital Oliver, Marvin Ritter, Bertrand
  Rondepierre, Andreas Steiner, and Marc van Zee.
  Flax: A neural network library and ecosystem for JAX, 2020.
* [23]

  Ajay Jain.
  VectorAscent: Generate vector graphics from a textual description,
  2021.
* [24]

  Ajay Jain, Matthew Tancik, and Pieter Abbeel.
  Putting nerf on a diet: Semantically consistent few-shot view
  synthesis.
  ICCV, 2021.
* [25]

  Nikolay Jetchev.
  Clipmatrix: Text-controlled creation of 3d textured meshes, 2021.
* [26]

  Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le,
  Yun-Hsuan Sung, Zhen Li, and Tom Duerig.
  Scaling up visual and vision-language representation learning with
  noisy text supervision.
  ICML, 2021.
* [27]

  Tero Karras, Samuli Laine, Miika Aittala, Janne Hellsten, Jaakko Lehtinen, and
  Timo Aila.
  Analyzing and improving the image quality of stylegan.
  CVPR, 2020.
* [28]

  Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva
  Ramanan, Piotr Dollár, and C. Lawrence Zitnick.
  Microsoft COCO: Common objects in context.
  ECCV, 2014.
* [29]

  Nan Liu, Shuang Li, Yilun Du, Joshua B. Tenenbaum, and Antonio Torralba.
  Learning to compose visual relations.
  In Thirty-Fifth Conference on Neural Information Processing
  Systems, 2021.
* [30]

  Stephen Lombardi, Tomas Simon, Jason Saragih, Gabriel Schwartz, Andreas
  Lehrmann, and Yaser Sheikh.
  Neural volumes: Learning dynamic renderable volumes from images.
  ACM Trans. Graph., 2019.
* [31]

  Matthew Loper, Naureen Mahmood, Javier Romero, Gerard Pons-Moll, and Michael J.
  Black.
  SMPL: A skinned multi-person linear model.
  SIGGRAPH Asia, 2015.
* [32]

  Ben Mildenhall, Pratul P. Srinivasan, Rodrigo Ortiz-Cayon, Nima Khademi
  Kalantari, Ravi Ramamoorthi, Ren Ng, and Abhishek Kar.
  Local light field fusion: Practical view synthesis with prescriptive
  sampling guidelines.
  ACM Transactions on Graphics (TOG), 2019.
* [33]

  Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi
  Ramamoorthi, and Ren Ng.
  Nerf: Representing scenes as neural radiance fields for view
  synthesis.
  ECCV, 2020.
* [34]

  Alexander Mordvintsev, Christopher Olah, and Mike Tyka.
  Inceptionism: Going deeper into neural networks.
  2015.
* [35]

  Alexander Mordvintsev, Nicola Pezzotti, Ludwig Schubert, and Chris Olah.
  Differentiable image parameterizations.
  Distill, 2018.
  https://distill.pub/2018/differentiable-parameterizations.
* [36]

  Anh Nguyen, Jeff Clune, Yoshua Bengio, Alexey Dosovitskiy, and Jason Yosinski.
  Plug & play generative networks: Conditional iterative generation of
  images in latent space.
  CVPR, 2017.
* [37]

  Anh Nguyen, Alexey Dosovitskiy, Jason Yosinski, Thomas Brox, and Jeff Clune.
  Synthesizing the preferred inputs for neurons in neural networks via
  deep generator networks.
  NeurIPS, 2016.
* [38]

  Michael Niemeyer and Andreas Geiger.
  Giraffe: Representing scenes as compositional generative neural
  feature fields.
  CVPR, 2021.
* [39]

  Chris Olah, Alexander Mordvintsev, and Ludwig Schubert.
  Feature visualization.
  Distill, 2017.
  https://distill.pub/2017/feature-visualization.
* [40]

  Aaron van den Oord, Yazhe Li, and Oriol Vinyals.
  Representation learning with contrastive predictive coding.
  arXiv:1807.03748, 2018.
* [41]

  Dong Huk Park, Samaneh Azadi, Xihui Liu, Trevor Darrell, and Anna Rohrbach.
  Benchmark for compositional text-to-image synthesis.
  NeurIPS, 2021.
* [42]

  Jeong Joon Park, Peter Florence, Julian Straub, Richard Newcombe, and Steven
  Lovegrove.
  Deepsdf: Learning continuous signed distance functions for shape
  representation.
  CVPR, 2019.
* [43]

  Or Patashnik, Zongze Wu, Eli Shechtman, Daniel Cohen-Or, and Dani Lischinski.
  Styleclip: Text-driven manipulation of stylegan imagery.
  ICCV, 2021.
* [44]

  Victor Perez, Joel Simon, and Tal Shiri.
  Sculpting with words.
  2021.
* [45]

  Ben Poole, Sherjil Ozair, Aaron Van Den Oord, Alex Alemi, and George Tucker.
  On variational bounds of mutual information.
  ICML, 2019.
* [46]

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh,
  Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark,
  Gretchen Krueger, and Ilya Sutskever.
  Learning transferable visual models from natural language
  supervision.
  CoRR, abs/2103.00020, 2021.
* [47]

  Prajit Ramachandran, Barret Zoph, and Quoc V. Le.
  Searching for activation functions.
  CoRR, abs/1710.05941, 2017.
* [48]

  Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec
  Radford, Mark Chen, and Ilya Sutskever.
  Zero-shot text-to-image generation.
  CoRR, abs/2102.12092, 2021.
* [49]

  Aditya Sanghi, Hang Chu, Joseph G. Lambourne, Ye Wang, Chin-Yi Cheng, and Marco
  Fumero.
  Clip-forge: Towards zero-shot text-to-shape generation, 2021.
* [50]

  Peter Schaldenbrand, Zhixuan Liu, and Jean Oh.
  Styleclipdraw: Coupling content and style in text-to-drawing
  synthesis, 2021.
* [51]

  Katja Schwarz, Yiyi Liao, Michael Niemeyer, and Andreas Geiger.
  Graf: Generative radiance fields for 3d-aware image synthesis.
  NeurIPS, 2020.
* [52]

  Vincent Sitzmann, Julien Martel, Alexander Bergman, David Lindell, and Gordon
  Wetzstein.
  Implicit neural representations with periodic activation functions.
  NeurIPS, 2020.
* [53]

  Sanjay Subramanian, Will Merrill, Trevor Darrell, Matt Gardner, Sameer Singh,
  and Anna Rohrbach.
  Reclip: A strong zero-shot baseline for referring expression
  comprehension.
  In Proceedings of the 60th Annual Meeting of the Association for
  Computational Linguistics, Dublin, Ireland, May 2022. Association for
  Computational Linguistics.
* [54]

  Matthew Tancik, Ben Mildenhall, Terrance Wang, Divi Schmidt, Pratul P.
  Srinivasan, Jonathan T. Barron, and Ren Ng.
  Learned initializations for optimizing coordinate-based neural
  representations.
  CVPR, 2021.
* [55]

  Matthew Tancik, Pratul P. Srinivasan, Ben Mildenhall, Sara Fridovich-Keil,
  Nithin Raghavan, Utkarsh Singhal, Ravi Ramamoorthi, Jonathan T. Barron, and
  Ren Ng.
  Fourier features let networks learn high frequency functions in low
  dimensional domains.
  NeurIPS, 2020.
* [56]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
  Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  NeurIPS, pages 5998–6008, 2017.
* [57]

  Jiajun Wu, Chengkai Zhang, Tianfan Xue, William T Freeman, and Joshua B
  Tenenbaum.
  Learning a probabilistic latent space of object shapes via 3d
  generative-adversarial modeling.
  In Advances in Neural Information Processing Systems, pages
  82–90, 2016.
* [58]

  Jiajun Wu, Chengkai Zhang, Xiuming Zhang, Zhoutong Zhang, William T Freeman,
  and Joshua B Tenenbaum.
  Learning 3D Shape Priors for Shape Completion and Reconstruction.
  In European Conference on Computer Vision (ECCV), 2018.
* [59]

  Lior Yariv, Jiatao Gu, Yoni Kasten, and Yaron Lipman.
  Volume rendering of neural implicit surfaces.
  arXiv:2106.12052, 2021.
* [60]

  Xiaohua Zhai, Xiao Wang, Basil Mustafa, Andreas Steiner, Daniel Keysers,
  Alexander Kolesnikov, and Lucas Beyer.
  Lit: Zero-shot transfer with locked-image text tuning, 2021.
* [61]

  Han Zhang, Jing Yu Koh, Jason Baldridge, Honglak Lee, and Yinfei Yang.
  Cross-modal contrastive learning for text-to-image generation.
  CVPR, 2021.
* [62]

  Kai Zhang, Gernot Riegler, Noah Snavely, and Vladlen Koltun.
  Nerf++: Analyzing and improving neural radiance fields.
  arXiv:2010.07492, 2020.
* [63]

  Richard Zhang, Phillip Isola, Alexei A Efros, Eli Shechtman, and Oliver Wang.
  The unreasonable effectiveness of deep features as a perceptual
  metric.
  CVPR, 2018.
* [64]

  Xiuming Zhang, Zhoutong Zhang, Chengkai Zhang, Joshua B Tenenbaum, William T
  Freeman, and Jiajun Wu.
  Learning to Reconstruct Shapes From Unseen Classes.
  In Advances in Neural Information Processing Systems (NeurIPS),
  2018.
* [65]

  Linqi Zhou, Yilun Du, and Jiajun Wu.
  3d shape generation and completion through point-voxel diffusion.
  ICCV, 2021.
* [66]

  Peng Zhou, Lingxi Xie, Bingbing Ni, and Qi Tian.
  CIPS-3D: A 3D-Aware Generator of GANs Based on
  Conditionally-Independent Pixel Synthesis.
  2021.

Supplementary Material

![Refer to caption](/html/2112.01455/assets/x10.png)


Figure 9: Varying the image-text model used for Dream Field optimization.

## Appendix A Qualitative results and ablations

An explanatory video with more qualitative results, code, an interactive Colab notebook, and object-centric prompts are available at <https://ajayj.com/dreamfields>. The video includes 360∘ renderings where the camera orbits the object, as well as associated depth maps.

![Refer to caption](/html/2112.01455/assets/x11.png)


Figure 10: Object diversity: Objects vary with different seeds, effecting NeRF’s weight initialization, camera sampling and augmentations.

#### Changing the image-text model

Figure [9](#A0.F9 "Figure 9 ‣ Acknowledgements ‣ 7 Conclusion ‣ 6 Discussion and limitations ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") qualitatively compares generations using guidance from three different contrastive image-text models. Dream Fields generated with LiTuuuu{}\_{\text{uu}} B/32 are generally sharper than those with CLIP models, but all three can produce objects reflecting some aspects of the prompts.

#### Diversity of synthesized objects

In creative applications, users often want to select between multiple synthesized results. Dream Fields can synthesize multiple objects from the same prompt by changing the random seed before optimization. The seed changes the initialization of the NeRF weights, the camera pose sampled each iteration and the random background and crop augmentations. Figure [10](#A1.F10 "Figure 10 ‣ Appendix A Qualitative results and ablations ‣ Acknowledgements ‣ 7 Conclusion ‣ 6 Discussion and limitations ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") shows the effect of changing the seed for four object-centric COCO prompts. Changing the seed changes scene shape and layout. For example, the bus on the left is compressed into a cubical shape, while the bus on the right is elongated. Colors and textures are often similar across the seeds, though can also vary. Changing the seed is another dimension of control in addition to prompt engineering.

## Appendix B Object Centric COCO captions dataset

Our Object Centric COCO dataset includes 153 test set prompts and 74 development set prompts. Several additional prompts are used for qualitative results, and are included in the main paper alongside figures. Captions are included along with code on the [project website](https://ajayj.com/dreamfields).

## Appendix C Hyperparameters and training setup

#### Positional encoding

Our Fourier feature positional encodings use L=8𝐿8L=8 frequency levels, while novel view synthesis applications with image supervision commonly use L=10𝐿10L=10 to fit high-frequency details in photographs. Low-frequency ablations in Table 1 use L=6𝐿6L=6, which can improve convergence in the absence of our other geometric priors.

#### Rendering

Scenes are bounded to a cube with side length 2.
The camera is sampled at a fixed radius of 4 units from the center of the cubical scene bounds and an elevation of 30∘ above the equator. Near and far planes are set at 4±3plus-or-minus434\pm\sqrt{3} units from the camera based on the minimum and maximum possible distance to the corners of the cube. During training, we sample 192 points along each ray, spaced uniformly and jittered with uniform noise.
Rendered 1682 views are cropped to 1542 and upsampled to CLIP’s input resolution for scenes where we compute qualitative metrics or 2522 views are cropped to 2242 for certain higher-quality visualizations. Crop sizes are selected to cover about 80% of the image area. At test time, we sample 512 points along the rays and render at a higher resolution equal to CLIP’s input size of 2242 or LiT’s input size of 2882 for computing R-Precision and 4002 for visualizations.

![Refer to caption](/html/2112.01455/assets/x12.png)


Figure 11: Total loss with different sparsity regularizers and constant ℒCLIP∈[0.1,−0.3]subscriptℒCLIP0.10.3\mathcal{L}\_{\mathrm{CLIP}}\in[0.1,-0.3]. Upper and lower bounds of ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} are shown with dashed lines. The additive loss is convex, and is always minimized by increasing transmittance.

#### Optimization

MLP parameters are initialized with the Flax [[22](#bib.bib22)] defaults: LeCun normal weights and zero bias for linear layers, and unit scaling and zero bias for layer normalization. The MLP is optimized with Adam with ϵ=10−5italic-ϵsuperscript105\epsilon=10^{-5}. Learning rate warms up exponentially from 10−5superscript10510^{-5} to 10−4superscript10410^{-4} over 1500 iterations, then is held constant. The camera origin is separately tracked with an exponential moving average with decay rate 0.9990.9990.999 of the center of mass of rendered density. Figure [11](#A3.F11 "Figure 11 ‣ Rendering ‣ Appendix C Hyperparameters and training setup ‣ Acknowledgements ‣ 7 Conclusion ‣ 6 Discussion and limitations ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") visualizes different forms of the transmittance loss.

![Refer to caption](/html/2112.01455/assets/x13.png)


Figure 12: Optimizing a Neural Radiance Field scene representation (bottom) leads to fewer artifacts than optimizing an explicit single-view 2D image (top) or 3D voxel grid (middle), even when the explicit representations are regularized. Our MLP has 16×\times fewer parameters than the voxel grid, which may contribute to smoother, less noisy objects. We use CLIP B/16 for this experiment.

#### Hyperparameter selection

Hyperparameters are manually tuned for visual quality on a development set of 74 object-centric COCO captions distinct from the test set reported in the paper. Most tuning is done on a smaller subset of 20 of the 74 captions, and hyperparameters are shared across all scenes.

#### Hardware

Optimization is done on 8 preemptible TPU cores, and 10K iterations takes approximately 1 hour 12 minutes. This means each Dream Field costs approximately $3-4 to generate on Google Cloud, which is economical for applications. Training is bottlenecked by MLP inference and backpropagation during volumetric rendering, not CLIP.

## Appendix D Pixel and voxel baselines

We implemented 2D image optimization with a total variation loss and generative prior (CLIP Guided Diffusion), as well as a 3D voxel baselines to replace NeRF in Fig. [12](#A3.F12 "Figure 12 ‣ Optimization ‣ Appendix C Hyperparameters and training setup ‣ Acknowledgements ‣ 7 Conclusion ‣ 6 Discussion and limitations ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields"). All results for this ablation optimize CLIP ViT B/16.

The 2D image is an RGBα𝛼\alpha pixel grid, composited with random backgrounds during optimization similar to Dream Fields.
Optimizing a single 2D RGBα𝛼\alpha image does not produce a multi-view consistent 3D object, so other viewpoints cannot be rendered. Even with transmittance and TV regularization, the resulting image is noisy.

The voxel grid stores 1283 RGB and alpha values, interpolated trilinearly at ray sample points and composited without a neural network using the PyTorch3D library. Despite the transmittance loss, data augmentations and scene bounds, the voxel grid also has significant low-density artifacts. The voxel baseline has CLIP B/32 R-Precision 37.0%±plus-or-minus\pm3.9, while NeRF has 59.8%±plus-or-minus\pm2.8 (Tables [5.2](#S5.SS2 "5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields"), [3](#S5.T3 "Table 3 ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields")) with 16×\times fewer parameters, showing that the neural representation improves consistency with the input caption in a generalizable way. Using a hybrid representation with an explicit voxel grid followed by a smaller MLP head might improve computational efficiency of Dream Fields without degrading quality.

## Appendix E Signed distance field parameterization

In early experiments, we learned scene density σ𝜎\sigma with the VolSDF parameterization [[59](#bib.bib59)] σ​(𝐱)=α​Φβ​(−dΩ​(𝐱))𝜎𝐱𝛼subscriptΦ𝛽subscript𝑑Ω𝐱\sigma(\mathbf{x})=\alpha\Phi\_{\beta}(-d\_{\Omega}(\mathbf{x})) where dΩ​(𝐱)subscript𝑑Ω𝐱d\_{\Omega}(\mathbf{x}) is a signed distance function implicitly defining the object surface and ΦΦ\Phi is the CDF of the Laplace distribution. This allows normal vector prediction with autodifferentiation and could improve the quality of the surface extracted from the radiance field. Dream Fields successfully train with this alternate parameterization and produce visually compelling objects. The SDF Eikonal loss introduces an additional loss weight hyperparameter, which benefits from some tuning. Alternate 3D representations are an interesting avenue for future work.

## Appendix F Impact of optimization time

![Refer to caption](/html/2112.01455/assets/x14.png)


Figure 13: Long-run training and validation curves averaged over 79 hand-written prompts. Transmittance remains close to the target τ𝜏\tau throughout training. Dream Fields overfit to the image-text representations used for optimization, so in quantitative experiments, we stop training at 10K iterations. The standard error of the mean is shaded.

Dream Fields can overfit to the aligned image-text representation used for optimization. Figure [13](#A6.F13 "Figure 13 ‣ Appendix F Impact of optimization time ‣ Acknowledgements ‣ 7 Conclusion ‣ 6 Discussion and limitations ‣ Varying the image-text model ‣ 5.4 Model ablations ‣ 5.3 Compositional generation ‣ 5.2 Analyzing retrieval metrics ‣ 5 Evaluation ‣ Zero-Shot Text-Guided Object Generation with Dream Fields") shows the training losses, ℒCLIPsubscriptℒCLIP\mathcal{L}\_{\mathrm{CLIP}} and mean transmittance mean​(T​(θ,𝐩))mean𝑇𝜃𝐩\mathrm{mean}(T(\theta,\mathbf{p})), as well as the validation R-Precision. Objects are generated with LiTuuuu{}\_{\text{uu}} ViT B/32 guidance, and R-Precision is computed with a different contrastive image-text model, CLIP ViT B/32. Validation renderings are also done at a held-out elevation angle. Training loss continues to improve over long optimization trajectories, up to 10×\times longer than reported in the main paper. However, validation retrieval accuracy declines after 5-10K iterations. The metrics are averaged over 79 different hand-written captions that test fine-grained variations in wording and prompt engineering.

Qualitatively, additional details and hyper-realistic effects are added over the course of long runs, shown in our supplementary video. Some details are not realistic, like floating text related to the typographic attacks identified in [[18](#bib.bib18)].

More augmentations may help further regularize the optimization. These include more aggressive 2D image augmentations such as smaller random crops, and more 3D data augmentations including varying focal length, varying distance from the subject and varying elevation. 3D data augmentations are supported by our approach.

[◄](/html/2112.01454)
[![ar5iv homepage](/assets/ar5iv.png)](/)
[Feeling  
lucky?](/feeling_lucky)

[Conversion  
report](/log/2112.01455)
[Report  
an issue](https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+2112.01455)
[View original  
on arXiv](https://arxiv.org/abs/2112.01455)[►](/html/2112.01456)

[Copyright](https://arxiv.org/help/license)
[Privacy Policy](https://arxiv.org/help/policies/privacy_policy)

Generated on Sat Mar 2 02:34:05 2024 by [LaTeXML](http://dlmf.nist.gov/LaTeXML/)
