# Diffusion Transformers with Representation Autoencoders
Source: https://rae-dit.github.io/
Diffusion Transformers with Representation Autoencoders



# Diffusion Transformers with Representation Autoencoders

Representation Autoencoders (RAEs) reuse pretrained, frozen representation encoders together with lightweight trained decoders to provide high-fidelity, semantically rich latents for diffusion transformers.

[Paper](https://arxiv.org/abs/2510.11690)
[Code](https://github.com/bytetriper/RAE)
[🤗 Models](https://huggingface.co/collections/nyu-visionx/rae-68ecb57b8bfbf816c83cce15)

### Authors

[Boyang Zheng](http://bytetriper.github.io/)

[Nanye Ma](https://willisma.github.io/)

[Shengbang Tong](https://tsb0601.github.io/)

[Saining Xie](https://www.sainingxie.com/)

### Affiliations

[New York University](https://cs.nyu.edu/home/index.html)

### Resources

[Paper](https://arxiv.org/abs/2510.11690)

[Code Repository](https://github.com/bytetriper/RAE)

[Hugging Face Models](https://huggingface.co/collections/nyu-visionx/rae-68ecb57b8bfbf816c83cce15)

#### Contents

[Overview](#overview)

[High Fidelity Reconstruction from RAE](#autoencoders)

[Taming Diffusion Transformers for RAE](#diffusion)

[Improve the Model Scalability with Wide Diffusion Head](#sec-ddt)

[Discussions](#sec-discussions)

[Conclusion](#sec-conclusion)

## Overview

Latent generative modeling, where a pretrained autoencoder maps pixels into a latent space for the diffusion process, has become the standard strategy for Diffusion Transformers (DiT);
however, the autoencoder component has barely evolved. Most DiTs continue to rely on the original VAE encoder, which introduces several limitations: outdated backbones that compromise architectural simplicity, low-dimensional latent spaces that restrict information capacity, and weak representations that result from purely reconstruction-based training and ultimately limit generative quality.
In this work, we explore replacing the VAE with pretrained representation encoders (e.g., DINO, SigLIP, MAE) paired with trained decoders, forming what we term **R**epresentation **A**uto**e**ncoders (RAEs).

These models provide both high-quality reconstructions and semantically rich latent spaces, while allowing for a scalable transformer-based architecture.
Since these latent spaces are typically high-dimensional, a key challenge is enabling diffusion transformers to operate effectively within them. We analyze the sources of this difficulty, propose theoretically motivated solutions, and validate them empirically.

Our approach achieves faster convergence without auxiliary representation alignment losses. Using a DiT variant equipped with a lightweight, wide DDT head, we achieve strong image generation results on ImageNet: **1.51** FID at 256x256 (no guidance) and **1.13 / 1.13** at 256x256 and 512x512 (with guidance).
RAE offers clear advantages and should be the new default for diffusion transformer training.

![Pipeline overview for representation autoencoders](images/rae/intro.png)


Pipeline overview: a frozen vision encoder writes semantic tokens, a lightweight decoder reconstructs pixels, and diffusion transformers operate in the latent space.

As with training VAEs, there are two questions to answer:

* **How well can RAE reconstruct the input image?**
* **How well can diffusion transformers operate within the RAE latent space?**

![RAE architecture overview](images/rae/arch_teaser_v1.png)


**Comparison of SD-VAE and RAE (DINOv2-B).** The VAE relies on convolutional backbones with aggressive down- and up-sampling, while the RAE uses a ViT architecture *without* compression. SD-VAE is also more computationally expensive, requiring about 6× and 3× more GFLOPs than RAE for the encoder and decoder, respectively. GFlops are evaluated on one 256×256 image.

## High Fidelity Reconstruction from RAE

We challenge the common assumption that pretrained representation encoders, such as DINOv2 and SigLIP2, are unsuitable for the reconstruction task because they *“emphasize high-level semantics while downplaying low-level details”* . We show that, with a properly trained decoder, frozen SEM can in fact serve as strong encoders for the diffusion latent space. Our **Representation Autoencoders (RAE)** pair frozen, pretrained SEM with a ViT decoder, yielding reconstructions on par with—or even better than—SD-VAE. More importantly, RAEs alleviate the fundamental limitations of VAEs , whose heavily compressed latent space (e.g., SD-VAE maps 2562 images to 322×4  latents) restricts reconstruction fidelity and, more importantly, representation quality.

![Reconstruction examples produced by RAEs](images/rae/reprdit_recon.png)


Reconstruction examples with a frozen DINOv2-B encoder. Even small RAEs rival SD-VAE quality while keeping rich semantic tokens.

### Reconstruction, scaling, and representation.

As shown below, RAEs achieve consistently better reconstruction quality (rFID) than SD-VAE.
For instance, RAE with MAE-B/16 reaches an rFID of 0.16, clearly outperforming SD-VAE and challenging the assumption that representation encoders cannot recover pixel-level detail.

We next study the scaling behavior of both encoders and decoders. As shown in Table 1c, reconstruction quality remains stable across DINOv2-S, B, and L, indicating that even small representation encoder models preserve sufficient low-level detail for decoding.
On the decoder side (Table 1b), increasing capacity consistently improves rFID: from 0.58 with ViT-B to 0.49 with ViT-XL.
Importantly, ViT-B already outperforms SD-VAE while being 14× more efficient in GFLOPs, and ViT-XL further improves quality at only one-third of SD-VAE’s cost.
We also evaluate representation quality via linear probing on ImageNet-1K in Table 1d.
Because RAEs use frozen pretrained encoders, they directly inherit the representations of the underlying encoders.
In contrast, SD-VAE achieves only approximately 8% accuracy.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | Decoder | rFID↓ | GFLOPs | | --- | --- | --- | | ViT-B | 0.58 | 22.2 | | ViT-L | 0.50 | 78.1 | | ViT-XL | **0.49** | 106.7 | | SD-VAE | 0.62 | 310.4 |  Larger decoders improve rFID while remaining much more efficient than VAEs. | | Encoder | rFID↓ | | --- | --- | | DINOv2-S | 0.52 | | DINOv2-B | **0.49** | | DINOv2-L | 0.52 |  Encoder scaling — rFID remains stable across RAE sizes. | | Model | Top-1 Acc.↑ | | --- | --- | | DINOv2-B | **84.5** | | SigLIP-B | 79.1 | | MAE-B | 68.0 | | SD-VAE | ~8 |  RAEs have much higher linear probing accuracy than VAEs. |

## Taming Diffusion Transformers for RAE

With RAE demonstrating good reconstruction quality, we now proceed to investigate the *diffusability* of its latent space;
that is, how easily its latent distribution can be modeled by a diffusion model, and how good the generation performance can be.
Empirically, despite the superior reconstruction quality of MAE encoders,
we found that DINOv2 produces the strongest generation results, so we adopt it as the default, unless otherwise specified.

Following standard practice, we adopt the flow matching objective to train the diffusion model, for which we use LightningDiT, a variant of DiT, as our model backbone.

We adopt a patch size of 1, which results in a token length of 256 for all RAEs on 256x256 images, matching the sequence length used by VAE-based DiTs. We note that, Since the
computational cost of DiT depends primarily on the sequence length, **using RAE latents on DiTs will not incur additional computational cost compared to using VAE latents.**

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **DiT Does Not Work Out of the Box.** Surprisingly, the standard diffusion recipe fails with RAE: training directly on RAE latents causes a small backbone such as DiT-S to completely fail, while a larger backbone like DiT-XL significantly underperforms it's counterpart with the SD-VAE latents. To investigate this observation, we raise several hypotheses detailed below, which we will discuss in the following sections: | |  | RAE | SD-VAE | | --- | --- | --- | | DiT-S | 215.76 | **51.74** | | DiT-XL | 23.08 | **7.13** |  Standard DiT struggles to model RAE's latent distribution. |

* **Suboptimal design for diffusion transformers.** When modeling high-dimensional RAE tokens, the optimal design choices for diffusion transformers can diverge from the standard DiT, which was originally tailored for low-dimensional VAE tokens.
* **Suboptimal noise scheduling.** Prior noise scheduling and loss re-weighting tricks are derived for image-based or VAE-based input, and it remains unclear if they transfer well to high-dimension semantic tokens.
* **Diffusion generates noisy latents.** VAE decoders are trained to reconstruct images from noisy latents, making them more tolerant to small noises in diffusion outputs. In contrast, RAE decoders are trained on clean latents and may struggle to generalize.

### Scaling DiT Width to Match Token Dimensionality

To better understand the training dynamics of Diffusion Transformers in RAE latent space, we construct a simplified experiment:
we randomly select **a single image**, encode it by RAE, and test whether the diffusion model can *reconstruct* it. Starting from a DiT-S, we first vary the model width while fixing depth.
We fix the RAE encoder to DINOv2-B with token dimension of 768.

As shown in the following figure, sample quality is poor when the model width d< token dimension n=768,
but improves sharply and reproduces the input almost perfectly once d>=n. Training losses exhibit the same trend, converging only when d>=n.
One might suspect that this improvement still arises from the larger model capacity, but again as shown in the following figure,
even when doubling the depth from 12 to 24, the generated images remain artifact-heavy, and the training losses fail to converge to similar level of d=768.

![Overfitting analysis for different decoder widths](images/rae/overfit_width.png)


**Overfitting to a single sample.** Left: increasing model width lead to lower loss and better sample quality; Right: changing model depth has marginal effect on overfitting results.

Together, the results indicate that for generation in RAE's latent space to succeed, **the diffusion model's width must match or exceed the RAE's token dimension**.
This appears to contradict the common belief that data usually has low intrinsic dimension  and thus allowing generative models like GAN to operate effectively without scaling width to the full data dimension .
We note that this is due to the nature of diffusion models, where the injected Gaussian noise during training extends the data distribution’s support to the entire space, thereby "diffusing" the data manifold into a full-rank one, requiring model capacity that scales with the full data dimensionality.

|  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| We further extend our investigation to a more practical setting by examining three models of varying width, \{DiT-S, DiT-B, DiT-L\}. Each model is overfit on a single image encoded by {DINOv2-S, DINOv2-B, DINOv2-L}, respectively, corresponding to different token dimensions of {384, 768, 1024}. | |  | DiT-S | DiT-B | DiT-L | | --- | --- | --- | --- | | DINOv2-S | 3.6e-2 ✓ | 1.0e-3 ✓ | 9.7e-4 ✓ | | DINOv2-B | 5.2e-1 ✗ | 2.4e-2 ✓ | 1.3e-3 ✓ | | DINOv2-L | 6.5e-1 ✗ | 2.7e-1 ✗ | 2.2e-2 ✓ |  **Overfitting losses.** |

As shown above, convergence occurs only when the model width is at least as large as the token dimension (e.g., DiT-B with DINOv2-B), while the loss fails to converge otherwise (e.g., DiT-S with DINOv2-B).

* **Suboptimal design for diffusion transformers.**We now fix the width of DiT to be at least as large as the RAE token dimension. For RAE with the DINOv2-B encoder, we pair it with DiT-XL in our following experiments.

### Dimension-Dependent Noise Schedule Shift

Many prior works , , ,  have observed that,
for inputs z∈RC×H×W, increasing the spatial resolution (H×W) reduces information corruption at the same noise level, impairing diffusion training.
These findings, however, are based mainly on pixel- or VAE-encoded inputs with few channels (e.g., C≤16).
In practice, the Gaussian noise is applied to both spatial and channel dimensions; as the number of channels increases, the effective “resolution” per token also grows, reducing information corruption further. We therefore argue that proposed resolution-dependent strategies in these prior works should be generalized to the \textit{effective data dimension}, defined as the number of tokens times their dimensionality.

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| |  | gFID↓ | | --- | --- | | w/o shift | 23.08 | | w/ shift | **4.81** |  **Impact of schedule shift.** | Specifically, We adopt the shifting strategy of: for a schedule tn∈[0,1] and input dimensions n,m, the shifted timestep is defined as tm=αtn1+(α−1)tn where α=m/n is a dimension-dependent scaling factor. We follow in using n=4096 as the base dimension and set m to the effective data dimension of RAE. |

This this yields significant performance gains, showing its importance for training diffusion models in the high-dimensional RAE latent space.

* **Suboptimal noise scheduling.** We now default the noise schedule to be dependent on the effective data dimension for all our following experiments.

### Noise-Augmented Decoding

Unlike VAEs, whose latents follow a continuous distribution N(μ,σ2I),
the RAE decoder D is trained to reconstruct images from a discrete latent distribution p(z)=∑iδ(z−zi), where zi are encoder outputs from the training set.
At inference, diffusion-generated latents may deviate slightly from this distribution due to imperfect training or sampling, leading to out-of-distribution artifacts and degraded sample quality.
To address this, following prior work in Normalizing Flows, , , we add Gaussian noise n∼N(0,σ2I) during decoder training.
Instead of decoding from the clean distribution p(z), we train on its smoothed variant pn(z)=∫p(z−n)N(0,σ2I)(n)dn, improving generalization to the denser latent space of diffusion models.
We further sample σ from |N(0,τ2)| to regularize training and enhance robustness.

|  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| |  | gFID↓ | rFID↓ | | --- | --- | --- | | z∼p(z) | 4.81 | 0.49 | | z∼pn(z) | **4.28** | 0.57 |  **Impact of pn(z).** | We analyze how pn(z) affects reconstruction and generation. As shown on the right, it improves gFID but slightly worsens rFID. This trade-off is expected: adding noise smooths the latent distribution and, therefore, helps reduce OOD issues for the decoder, but also removes fine details, lowering reconstruction quality. |

* **Diffusion generates noisy latents.** We now adopt the noise-augmented decoding for all our following experiments.

|  |  |
| --- | --- |
| Combining all the above techniques, we train a DiT-XL model on RAE latents, which achieves a gFID of 4.28 ([Right](#fig-compare_convergence)) after only 80 epochs and 2.39 after 720 epochs. With the same model size, this not only surpasses prior diffusion baselines (e.g., SiT-XL) trained on VAE latents—achieving a 47× training speedup—but also outpaces recent representation-alignment methods (e.g., REPA-XL) with a 16× faster convergence. | Convergence comparison between RAEs and SD-VAE   Training convergence on ImageNet 256×256: RAEs reach strong sample quality in one tenth the number of updates. |

In the following sections, we investigate ways to make RAE generation more efficient and effective, pushing it toward state-of-the-art performance.

## Improving the Model Scalability with Wide Diffusion Head

As discussed in [Section 2](#sec-theory), within the standard DiT framework, handling higher-dimensional RAE latents
requires scaling up the width of the entire backbone, which quickly becomes computationally expensive.
To overcome this limitation, we draw inspiration from DDT  and introduce the
DDT head—a *shallow yet wide* transformer module dedicated to denoising.
By attaching this head to a standard DiT, we effectively increase model width without incurring quadratic growth in FLOPs.
We refer to this augmented architecture as **DiTDH**.

![The Wide DDT Head architecture](images/DDT_arch.png)


**The Wide DDT Head.**

**Wide DDT Head.** Formally, a DiTDH model consists of a base DiT M
and an additional wide, shallow transformer head H.
Given a noisy input xt, timestep t,
and an optional class label y, the combined model predicts the velocity
vt as

zt=M(xt∣t,y),vt=H(xt∣zt,t).

![DiT<sup>DH</sup> scales better than large DiT with RAE latents](images/ditdh_vs_ditxl.png)


**DiTDH** scales much better than DiT.


![DiT<sup>DH</sup> with RAE converges faster than VAE-based methods](images/convergence_teaser_standalone.png)


**DiTDH** on RAE converges faster than VAE-based methods.

**DiTDH converges faster than DiT.** We train a series of DiTDH models with varying backbone sizes
(DiTDH-S, B, L, and XL) on RAE latents.
We use a 2-layer, 2048-dim DiTDH head for all models. Performance is compared against the standard DiT-XL baseline.
DiTDH is substantially more FLOP-efficient than DiT.
For example, DiTDH-B requires only ∼40% of the training FLOPs yet outperforms DiT-XL by a large margin;
when scaled to DiTDH-XL under a comparable training budget, it achieves an FID of 2.16—nearly half that of DiT-XL.

**Convergence Comparison.** We compare the convergence behavior of DiTDH-XL with previous state-of-the-art diffusion
models , , ,
, and  in terms of FID without guidance.
We show the convergence curve of DiTDH-XL with
training epochs and GFLOPs, while baseline models are plotted at their reported final performance.
DiTDH-XL already surpasses REPA-XL, MDTv2-XL, and SiT-XL around 5×1010 GFLOPs,
and by 5×1011 GFLOPs it achieves the best FID overall, requiring over 40× less compute.

**Scaling Behavior.** We compare DiTDH with recent methods across different model scales.
Increasing the size of DiTDH consistently
improves FID performance. The smallest model, DiTDH-S, achieves a competitive FID of 6.07—already outperforming the
much larger REPA-XL. Scaling up to DiTDH-B yields a substantial improvement from 6.07 to 3.38, surpassing all prior
works of similar or even larger scale. The performance continues to improve with DiTDH-XL, reaching a new
state-of-the-art FID of 2.16 at 80 training epochs.


![DiT<sup>DH</sup> with RAE reaches better FID than VAE methods at all scales](images/encoder_scaling_epoch80.png)


**DiTDH scalability.** With RAE latents, DiTDH scales more efficiently in both training compute and model size
than RAE-based DiT and VAE-based methods. Bubble area indicates FLOPs.

**Performance.** we provide a quantitative comparison between DiTDH-XL, our most performant model, with recent state-of-the-art diffusion models on ImageNet 256×256 and 512×512 in [Table 1](#tab:comparison_perf) and [Table 2](#tab:imagenet512_sota).
Our method outperforms all prior diffusion models by a large margin, setting new state-of-the-art FID scores of 1.51 without guidance and 1.13 with guidance at 256×256. On 512×512, with 400-epoch training, DiTDH-XL achieves an FID of 1.13 with guidance, surpassing the previous best performance achieved by EDM-2 (1.25).

| Method | Epochs | #Params | Generation@256 w/o guidance | | | | Generation@256 w/ guidance | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | gFID↓ | IS↑ | Prec.↑ | Rec.↑ | gFID↓ | IS↑ | Prec.↑ | Rec.↑ |
| Autoregressive | | | | | | | | | | |
| VAR | 350 | 2.0B | 1.92 | 323.1 | 0.82 | 0.59 | 1.73 | **350.2** | 0.82 | 0.60 |
| MAR | 800 | 943M | 2.35 | 227.8 | 0.79 | 0.62 | 1.55 | 303.7 | 0.81 | 0.62 |
| xAR | 800 | 1.1B | - | - | - | - | 1.24 | 301.6 | **0.83** | 0.64 |
| Pixel Diffusion | | | | | | | | | | |
| ADM | 400 | 554M | 10.94 | 101.0 | 0.69 | 0.63 | 3.94 | 215.8 | **0.83** | 0.53 |
| RIN | 480 | 410M | 3.42 | 182.0 | - | - | - | - | - | - |
| PixelFlow | 320 | 677M | - | - | - | - | 1.98 | 282.1 | 0.81 | 0.60 |
| PixNerd | 160 | 700M | - | - | - | - | 2.15 | 297.0 | 0.79 | 0.59 |
| SiD2 | 1280 | - | - | - | - | - | 1.38 | - | - | - |
| Latent Diffusion with VAE | | | | | | | | | | |
| DiT | 1400 | 675M | 9.62 | 121.5 | 0.67 | 0.67 | 2.27 | 278.2 | **0.83** | 0.57 |
| MaskDiT | 1600 | 675M | 5.69 | 177.9 | 0.74 | 0.60 | 2.28 | 276.6 | 0.80 | 0.61 |
| SiT | 1400 | 675M | 8.61 | 131.7 | 0.68 | 0.67 | 2.06 | 270.3 | 0.82 | 0.59 |
| MDTv2 | 1080 | 675M | - | - | - | - | 1.58 | 314.7 | 0.79 | 0.65 |
| VA-VAE | 80 | 675M | 4.29 | - | - | - | - | - | - | - |
| 800 | 2.17 | 205.6 | 0.77 | 0.65 | 1.35 | 295.3 | 0.79 | 0.65 |
| REPA | 80 | 675M | 7.90 | 122.6 | 0.70 | 0.65 | - | - | - | - |
| 800 | 5.78 | 158.3 | 0.70 | 0.68 | 1.29 | 306.3 | 0.79 | 0.64 |
| DDT | 80 | 675M | 6.62 | 135.2 | 0.69 | 0.67 | 1.52 | 263.7 | 0.78 | 0.63 |
| 400 | 6.27 | 154.7 | 0.68 | **0.69** | 1.26 | 310.6 | 0.79 | 0.65 |
| REPA-E | 80 | 675M | 3.46 | 159.8 | 0.77 | 0.63 | 1.67 | 266.3 | 0.80 | 0.63 |
| 800 | 1.70 | 217.3 | 0.77 | 0.66 | 1.15 | 304.0 | 0.79 | 0.66 |
| Latent Diffusion with RAE (Ours) | | | | | | | | | | |
| DiT-XL (DINOv2-S) | 800 | 676M | 1.87 | 209.7 | 0.80 | 0.63 | 1.41 | 309.4 | 0.80 | 0.63 |
| DiTDH-XL (DINOv2-B) | 20 | 839M | 3.71 | 198.7 | **0.86** | 0.50 | -- | -- | -- | -- |
| 80 | 2.16 | 214.8 | 0.82 | 0.59 | -- | -- | -- | -- |
| 800 | **1.51** | **242.9** | 0.79 | 0.63 | **1.13** | 262.6 | 0.78 | **0.67** |

**Table 1: Class-conditional performance on ImageNet 256×256.**
RAE reaches an FID of 1.51 without guidance, outperforming all prior methods by a large margin. It also achieves an FID of 1.13 with AutoGuidance. We identified an inconsistency in the FID evaluation protocol in prior literature and re-ran the sampling process for several baselines. This resulted in higher baseline numbers than those originally reported.




| Method | Generation@512 | | | |
| --- | --- | --- | --- | --- |
|  | gFID↓ | IS↑ | Prec.↑ | Rec.↑ |
| BigGAN-deep | 8.43 | 177.9 | **0.88** | 0.29 |
| StyleGAN-XL | 2.41 | 267.8 | 0.77 | 0.52 |
| VAR | 2.63 | 303.2 | - | - |
| MAGVIT-v2 | 1.91 | **324.3** | - | - |
| XAR | 1.70 | 281.5 | - | - |
| ADM | 3.85 | 221.7 | 0.84 | 0.53 |
| SiD2 | 1.50 | - | - | - |
| DiT | 3.04 | 240.8 | 0.84 | 0.54 |
| SiT | 2.62 | 252.2 | 0.84 | 0.57 |
| DiffiT | 2.67 | 252.1 | 0.83 | 0.55 |
| REPA | 2.08 | 274.6 | 0.83 | 0.58 |
| DDT | 1.28 | 305.1 | 0.80 | **0.63** |
| EDM2 | 1.25 | - | - | - |
| DiTDH-XL (DINOv2-B) | **1.13** | 259.6 | 0.80 | **0.63** |

**Table 2: Class-conditional performance on ImageNet 512×512 with guidance.**
DiTDH-XL with 400-epoch training achieves a strong FID score of 1.13.

## Discussions

### How can RAE extend to high-resolution synthesis efficiently?

A central challenge in generating high-resolution images is that resolution scales with the number of tokens:
doubling image size in each dimension requires roughly four times as many tokens. To address this, we let the
decoder handle resolution scaling by allowing its patch size pd to differ from the
encoder patch size pe. When pd=pe, the output matches the input resolution;
setting pd=2pe produces a 2× upsampled image, reconstructing a 512×512 image from the same tokens used at 256×256.

| Method | #Tokens | gFID ↓ | rFID ↓ |
| --- | --- | --- | --- |
| Direct | 1024 | 1.13 | 0.53 |
| Upsample | 256 | 1.61 | 0.97 |

**Comparison on ImageNet 512×512.** Decoder upsampling achieves competitive FID compared to
direct 512-resolution training. Both models are trained for 400 epochs.

Since the decoder is decoupled from both the encoder and the diffusion process, we can reuse diffusion models trained at
256×256 resolution, simply swapping in an upsampling decoder to produce 512×512 outputs without retraining.
This approach slightly increases both rFID and gFID, but being 4× more efficient than quadrupling the number of tokens.

### Does DiTDH work without RAE?

In this work, we propose and study RAE and DiTDH. In [Section 2](#sec-theory), we showed that
RAE combined with DiT already brings substantial benefits, even without the additional head.
Here, we turn the question around: can DiTDH still provide improvements without the latent space of RAE?

|  | VAE | DINOv2-B |
| --- | --- | --- |
| DiT-XL | 7.13 | 4.28 |
| DiTDH-XL | 11.70 | **2.16** |

**gFID-50k on VAE.** DiTDH yields worse FID than DiT, despite using extra compute for
the wide head.

To investigate, we train both DiT-XL and DiTDH-XL on SD-VAE latents with a patch size of 2, alongside DINOv2-B
for comparison, for 80 epochs, and report unguided FID. As shown on the left, DiTDH performs even worse than DiT on SD-VAE, despite the
additional computation introduced by the diffusion head. This indicates that the head provides little benefit in
low-dimensional latent spaces, and its primary strength arises in high-dimensional diffusion tasks introduced by RAE.

### The role of structured representation in high-dimensional diffusion

DiTDH achieves strong performance when paired with the high-dimensional latent space of RAE.
This raises a key question: is the structured representation of RAE essential, or would DiTDH work equally well
on unstructured high-dimensional inputs such as *raw pixels*?

|  | Pixel | DINOv2-B |
| --- | --- | --- |
| DiT-XL | 51.09 | 4.28 |
| DiTDH-XL | 30.56 | **2.16** |

**Comparison on pixel diffusion (gFID-50k).** Pixel diffusion performs far worse than diffusion on DINOv2-B
latents.

To evaluate this, we train DiT-XL and DiTDH-XL directly on raw pixels.
For 256×256 images with a patch size of 16, the resulting DiT input token dimensionality is 16×16×3 = 768,
matching that of the DINOv2-B latents. We report unguided FID after 80 epochs. As shown on the right, DiTDH outperforms DiT on pixels, but both models perform far
worse than their counterparts trained on RAE latents. These results demonstrate that high dimensionality alone is not
sufficient—the structured representation provided by RAE is crucial for achieving strong performance gains.

## Conclusion

In this work, we challenge the belief that pretrained representation encoders are too high-dimensional and too semantic
for reconstruction or generation. We show that a frozen representation encoder, paired with a lightweight trained decoder,
forms an effective **Representation Autoencoder (RAE)**. On this latent space, we train Diffusion Transformers
in a stable and efficient way with three added components: (1) match DiT width to the encoder token dimensionality,
(2) apply a dimension-dependent shift to the noise schedule, and (3) add decoder noise augmentation so the decoder
handles diffusion outputs. We also introduce **DiTDH**, a shallow-but-wide diffusion transformer
head that increases width without quadratic compute. Empirically, RAEs enable strong visual generation: on ImageNet, our
RAE-based DiTDH-XL achieves an FID of **1.51** at 256×256 (no guidance) and
**1.13 / 1.13** at 256×256 and 512×512 (with guidance). We believe RAE latents serve as a strong candidate
for training diffusion transformers efficiently and robustly in future generative modeling research.



### BibTeX

@misc{zheng2025diffusiontransformersrepresentationautoencoders,  
  title={Diffusion Transformers with Representation Autoencoders},  
  author={Boyang Zheng and Nanye Ma and Shengbang Tong and Saining Xie},  
  year={2025},  
  eprint={2510.11690},  
  archivePrefix={arXiv},  
  primaryClass={cs.CV}  
}

### Footnotes



### References

1. Scalable diffusion models with transformers   
   Peebles, W. and Xie, S., 2023. ICCV.
2. Auto-encoding variational bayes   
   Kingma, D.P. and Welling, M., 2014. ICLR.
3. Emerging Properties in Self-Supervised Vision Transformers   
   Caron, M., Touvron, H., Misra, I., Jégou, H., Mairal, J., Bojanowski, P. and Joulin, A., 2021. ICCV.
4. SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features   
   Tschannen, M., Gritsenko, A., Wang, X., Naeem, M.F., Alabdulmohsin, I., Parthasarathy, N., Evans, T., Beyer, L., Xia, Y., Mustafa, B., Hénaff, O., Harmsen, J., Steiner, A. and Zhai, X., 2025.
5. Masked Autoencoders Are Scalable Vision Learners   
   He, K., Chen, X., Xie, S., Li, Y., Dollár, P. and Girshick, R., 2021. CVPR.
6. UniLiP: Adapting CLIP for Unified Multimodal Understanding, Generation and Editing   
   Tang, H., Xie, C., Bao, X., Weng, T., Li, P., Zheng, Y. and Wang, L., 2025.
7. High-Resolution Image Synthesis with Latent Diffusion Models   
   Rombach, R., Blattmann, A., Lorenz, D., Esser, P. and Ommer, B., 2022. CVPR.
8. The intrinsic dimension of images and its impact on learning   
   Pope, P., Zhu, C., Abdelkader, A., Goldblum, M. and Goldstein, T., 2021. ICLR.
9. StyleGAN-XL: Scaling StyleGAN to Large Diverse Datasets   
   Sauer, A., Schwarz, K. and Geiger, A., 2022. SIGGRAPH.
10. Relay diffusion: Unifying diffusion process across resolutions for image synthesis   
    Teng, J., Zheng, W., Ding, M., Hong, W., Wangni, J., Yang, Z. and Tang, J., 2023. ICLR.
11. On the importance of noise scheduling for diffusion models   
    Chen, T., 2023. arXiv preprint arXiv:2301.10972.
12. Simple Diffusion: End-to-End Diffusion for High Resolution Images   
    Hoogeboom, E., Heek, J. and Salimans, T., 2023. ICML.
13. Scaling Rectified Flow Transformers for High-Resolution Image Synthesis   
    Esser, P., Kulal, S., Blattmann, A., Entez

[truncated]
