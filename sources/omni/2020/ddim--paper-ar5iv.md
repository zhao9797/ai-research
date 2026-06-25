# [2010.02502] Denoising Diffusion Implicit Models
Source: https://ar5iv.labs.arxiv.org/html/2010.02502
[2010.02502] Denoising Diffusion Implicit Models



# Denoising Diffusion Implicit Models

Jiaming Song, Chenlin Meng & Stefano Ermon
  
Stanford University
  
{tsong,chenlin,ermon}@cs.stanford.edu

###### Abstract

Denoising diffusion probabilistic models (DDPMs) have achieved high quality image generation without adversarial training, yet they require simulating a Markov chain for many steps in order to produce a sample. To accelerate sampling, we present denoising diffusion implicit models (DDIMs), a more efficient class of iterative implicit probabilistic models with the same training procedure as DDPMs. In DDPMs, the generative process is defined as the reverse of a particular Markovian diffusion process. We generalize DDPMs via a class of non-Markovian diffusion processes that lead to the same training objective. These non-Markovian processes can correspond to generative processes that are deterministic, giving rise to implicit models that produce high quality samples much faster. We empirically demonstrate that DDIMs can produce high quality samples 10×10\times to 50×50\times faster in terms of wall-clock time compared to DDPMs, allow us to trade off computation for sample quality, perform semantically meaningful image interpolation directly in the latent space, and reconstruct observations with very low error.

## 1 Introduction

Deep generative models have demonstrated the ability to produce high quality samples in many domains (Karras et al., [2020](#bib.bib20); van den Oord et al., [2016a](#bib.bib37)). In terms of image generation, generative adversarial networks (GANs, Goodfellow et al. ([2014](#bib.bib10))) currently exhibits higher sample quality than likelihood-based methods such as variational autoencoders (Kingma & Welling, [2013](#bib.bib21)), autoregressive models (van den Oord et al., [2016b](#bib.bib38)) and normalizing flows (Rezende & Mohamed, [2015](#bib.bib27); Dinh et al., [2016](#bib.bib9)). However, GANs require very specific choices in optimization and architectures in order to stabilize training (Arjovsky et al., [2017](#bib.bib1); Gulrajani et al., [2017](#bib.bib13); Karras et al., [2018](#bib.bib19); Brock et al., [2018](#bib.bib5)), and could fail to cover modes of the data distribution (Zhao et al., [2018](#bib.bib41)).

Recent works on iterative generative models (Bengio et al., [2014](#bib.bib3)), such as denoising diffusion probabilistic models (DDPM, Ho et al. ([2020](#bib.bib15))) and noise conditional score networks (NCSN, Song & Ermon ([2019](#bib.bib34))) have demonstrated the ability to produce samples comparable to that of GANs, without having to perform adversarial training. To achieve this, many denoising autoencoding models are trained to denoise samples corrupted by various levels of Gaussian noise. Samples are then produced by a Markov chain which, starting from white noise, progressively denoises it into an image. This generative Markov Chain process is either based on Langevin dynamics (Song & Ermon, [2019](#bib.bib34)) or obtained by reversing a forward diffusion process that progressively turns an image into noise (Sohl-Dickstein et al., [2015](#bib.bib32)).

A critical drawback of these models is that they require many iterations to produce a high quality sample. For DDPMs, this is because that the generative process (from noise to data) approximates the reverse of the forward diffusion process (from data to noise), which could have thousands of steps; iterating over all the steps is required to produce a single sample, which is much slower compared to GANs, which only needs one pass through a network.
For example, it takes around 20 hours to sample 50k images of size 32×32323232\times 32 from a DDPM, but less than a minute to do so from [a GAN](https://github.com/ajbrock/BigGAN-PyTorch) on a Nvidia 2080 Ti GPU. This becomes more problematic for larger images as sampling 50k images of size 256×256256256256\times 256 could take nearly 100010001000 hours on the same GPU.

To close this efficiency gap between DDPMs and GANs, we present denoising diffusion implicit models (DDIMs). DDIMs are implicit probabilistic models (Mohamed & Lakshminarayanan, [2016](#bib.bib23)) and are closely related to DDPMs, in the sense that they are trained with the same objective function. In Section [3](#S3 "3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models"),
we generalize the forward diffusion process used by DDPMs, which is Markovian, to non-Markovian ones, for which we are still able to design suitable reverse generative Markov chains.
We show that the resulting variational training objectives have a shared surrogate objective, which is exactly the objective used to train DDPM. Therefore, we can freely choose from a large family of generative models using the same neural network simply by choosing a different, non-Markovian diffusion process (Section [4.1](#S4.SS1 "4.1 Denoising Diffusion Implicit Models ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")) and the corresponding reverse generative Markov Chain.
In particular, we are able to use non-Markovian diffusion processes which lead to "short" generative Markov chains (Section [4.2](#S4.SS2 "4.2 Accelerated generation processes ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")) that can be simulated in a small number of steps.
This can massively increase sample efficiency only at a minor cost in sample quality.

In Section [5](#S5 "5 Experiments ‣ Denoising Diffusion Implicit Models"), we demonstrate several empirical benefits of DDIMs over DDPMs. First, DDIMs have superior sample generation quality compared to DDPMs, when we accelerate sampling by 10×10\times to 100×100\times using our proposed method.
Second, DDIM samples have the following ``consistency'' property, which does not hold for DDPMs: if we start with the same initial latent variable and generate several samples with Markov chains of various lengths, these samples would have similar high-level features. Third, because of ``consistency'' in DDIMs, we can perform semantically meaningful image interpolation by manipulating the initial latent variable in DDIMs, unlike DDPMs which interpolates near the image space due to the stochastic generative process.

## 2 Background

![Refer to caption](/html/2010.02502/assets/x1.png)

![Refer to caption](/html/2010.02502/assets/x2.png)

Figure 1: Graphical models for diffusion (left) and non-Markovian (right) inference models.

Given samples from a data distribution q​(𝒙0)𝑞subscript𝒙0q({\bm{x}}\_{0}), we are interested in learning a model distribution pθ​(𝒙0)subscript𝑝𝜃subscript𝒙0p\_{\theta}({\bm{x}}\_{0}) that approximates q​(𝒙0)𝑞subscript𝒙0q({\bm{x}}\_{0}) and is easy to sample from.
Denoising diffusion probabilistic models (DDPMs, Sohl-Dickstein et al. ([2015](#bib.bib32)); Ho et al. ([2020](#bib.bib15))) are latent variable models of the form

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ​(𝒙0)=∫pθ​(𝒙0:T)​d𝒙1:T,wherepθ​(𝒙0:T):=pθ​(𝒙T)​∏t=1Tpθ(t)​(𝒙t−1|𝒙t)formulae-sequencesubscript𝑝𝜃subscript𝒙0  subscript𝑝𝜃subscript𝒙:0𝑇differential-dsubscript𝒙:1𝑇whereassignsubscript𝑝𝜃subscript𝒙:0𝑇subscript𝑝𝜃subscript𝒙𝑇superscriptsubscriptproduct𝑡1𝑇subscriptsuperscript𝑝𝑡𝜃conditionalsubscript𝒙𝑡1subscript𝒙𝑡\displaystyle p\_{\theta}({\bm{x}}\_{0})=\int p\_{\theta}({\bm{x}}\_{0:T})\mathrm{d}{\bm{x}}\_{1:T},\quad\text{where}\quad p\_{\theta}({\bm{x}}\_{0:T}):=p\_{\theta}({\bm{x}}\_{T})\prod\_{t=1}^{T}p^{(t)}\_{\theta}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}) |  | (1) |

where 𝒙1,…,𝒙T

subscript𝒙1…subscript𝒙𝑇{\bm{x}}\_{1},\ldots,{\bm{x}}\_{T} are latent variables in the same sample space as 𝒙0subscript𝒙0{\bm{x}}\_{0} (denoted as 𝒳𝒳{\mathcal{X}}). The parameters θ𝜃\theta are learned to fit the data distribution q​(𝒙0)𝑞subscript𝒙0q({\bm{x}}\_{0}) by maximizing a variational lower bound:

|  |  |  |  |
| --- | --- | --- | --- |
|  | maxθ⁡𝔼q​(𝒙0)​[log⁡pθ​(𝒙0)]≤maxθ⁡𝔼q​(𝒙0,𝒙1,…,𝒙T)​[log⁡pθ​(𝒙0:T)−log⁡q​(𝒙1:T|𝒙0)]subscript𝜃subscript𝔼𝑞subscript𝒙0delimited-[]subscript𝑝𝜃subscript𝒙0subscript𝜃subscript𝔼𝑞subscript𝒙0subscript𝒙1…subscript𝒙𝑇delimited-[]subscript𝑝𝜃subscript𝒙:0𝑇𝑞conditionalsubscript𝒙:1𝑇subscript𝒙0\displaystyle\max\_{\theta}{\mathbb{E}}\_{q({\bm{x}}\_{0})}[\log p\_{\theta}({\bm{x}}\_{0})]\leq\max\_{\theta}{\mathbb{E}}\_{q({\bm{x}}\_{0},{\bm{x}}\_{1},\ldots,{\bm{x}}\_{T})}\left[\log p\_{\theta}({\bm{x}}\_{0:T})-\log q({\bm{x}}\_{1:T}|{\bm{x}}\_{0})\right] |  | (2) |

where q​(𝒙1:T|𝒙0)𝑞conditionalsubscript𝒙:1𝑇subscript𝒙0q({\bm{x}}\_{1:T}|{\bm{x}}\_{0}) is some inference distribution over the latent variables.
Unlike typical latent variable models (such as the variational autoencoder (Rezende et al., [2014](#bib.bib28))), DDPMs are learned with a fixed (rather than trainable) inference procedure q​(𝒙1:T|𝒙0)𝑞conditionalsubscript𝒙:1𝑇subscript𝒙0q({\bm{x}}\_{1:T}|{\bm{x}}\_{0}),
and latent variables are relatively high dimensional.
For example, Ho et al. ([2020](#bib.bib15)) considered the following Markov chain with Gaussian transitions
parameterized by a decreasing sequence
α1:T∈(0,1]Tsubscript𝛼:1𝑇superscript01𝑇\alpha\_{1:T}\in(0,1]^{T}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | q​(𝒙1:T|𝒙0):=∏t=1Tq​(𝒙t|𝒙t−1),where​q​(𝒙t|𝒙t−1):=𝒩​(αtαt−1​𝒙t−1,(1−αtαt−1)​𝑰)formulae-sequenceassign𝑞conditionalsubscript𝒙:1𝑇subscript𝒙0superscriptsubscriptproduct𝑡1𝑇𝑞conditionalsubscript𝒙𝑡subscript𝒙𝑡1assignwhere𝑞conditionalsubscript𝒙𝑡subscript𝒙𝑡1𝒩subscript𝛼𝑡subscript𝛼𝑡1subscript𝒙𝑡11subscript𝛼𝑡subscript𝛼𝑡1𝑰\displaystyle q({\bm{x}}\_{1:T}|{\bm{x}}\_{0}):=\prod\_{t=1}^{T}q({\bm{x}}\_{t}|{\bm{x}}\_{t-1}),\text{where}\ q({\bm{x}}\_{t}|{\bm{x}}\_{t-1}):={\mathcal{N}}\left(\sqrt{\frac{\alpha\_{t}}{\alpha\_{t-1}}}{\bm{x}}\_{t-1},\left(1-\frac{\alpha\_{t}}{\alpha\_{t-1}}\right){\bm{I}}\right) |  | (3) |

where the covariance matrix is ensured to have positive terms on its diagonal.
This is called the forward process due to the autoregressive nature of the sampling procedure (from 𝒙0subscript𝒙0{\bm{x}}\_{0} to 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T}). We call the latent variable model pθ​(𝒙0:T)subscript𝑝𝜃subscript𝒙:0𝑇p\_{\theta}({\bm{x}}\_{0:T}), which is a Markov chain that samples from 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} to 𝒙0subscript𝒙0{\bm{x}}\_{0}, the generative process, since it approximates the intractable reverse process q​(𝒙t−1|𝒙t)𝑞conditionalsubscript𝒙𝑡1subscript𝒙𝑡q({\bm{x}}\_{t-1}|{\bm{x}}\_{t}). Intuitively, the forward process progressively adds noise to the observation 𝒙0subscript𝒙0{\bm{x}}\_{0}, whereas the generative process progressively denoises a noisy observation (Figure [1](#S2.F1 "Figure 1 ‣ 2 Background ‣ Denoising Diffusion Implicit Models"), left).

A special property of the forward process is that

|  |  |  |
| --- | --- | --- |
|  | q​(𝒙t|𝒙0):=∫q​(𝒙1:t|𝒙0)​d𝒙1:(t−1)=𝒩​(𝒙t;αt​𝒙0,(1−αt)​𝑰);assign𝑞conditionalsubscript𝒙𝑡subscript𝒙0𝑞conditionalsubscript𝒙:1𝑡subscript𝒙0differential-dsubscript𝒙:1𝑡1𝒩  subscript𝒙𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡𝑰q({\bm{x}}\_{t}|{\bm{x}}\_{0}):=\int q({\bm{x}}\_{1:t}|{\bm{x}}\_{0})\mathrm{d}{\bm{x}}\_{1:(t-1)}={\mathcal{N}}({\bm{x}}\_{t};\sqrt{\alpha\_{t}}{\bm{x}}\_{0},(1-\alpha\_{t}){\bm{I}}); |  |

so we can express 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} as a linear combination of 𝒙0subscript𝒙0{\bm{x}}\_{0} and a noise variable ϵitalic-ϵ\epsilon:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙t=αt​𝒙0+1−αt​ϵ,whereϵ∼𝒩​(𝟎,𝑰).formulae-sequencesubscript𝒙𝑡  subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡italic-ϵwheresimilar-toitalic-ϵ𝒩0𝑰\displaystyle{\bm{x}}\_{t}=\sqrt{\alpha\_{t}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t}}\epsilon,\quad\text{where}\quad\epsilon\sim{\mathcal{N}}({\bm{0}},{\bm{I}}). |  | (4) |

When we set αTsubscript𝛼𝑇\alpha\_{T} sufficiently close to 00, q​(𝒙T|𝒙0)𝑞conditionalsubscript𝒙𝑇subscript𝒙0q({\bm{x}}\_{T}|{\bm{x}}\_{0}) converges to a standard Gaussian for all 𝒙0subscript𝒙0{\bm{x}}\_{0}, so it is natural to set pθ​(𝒙T):=𝒩​(𝟎,𝑰)assignsubscript𝑝𝜃subscript𝒙𝑇𝒩0𝑰p\_{\theta}({\bm{x}}\_{T}):={\mathcal{N}}({\bm{0}},{\bm{I}}).
If all the conditionals are modeled as Gaussians with trainable mean functions and fixed variances, the objective in Eq. ([2](#S2.E2 "In 2 Background ‣ Denoising Diffusion Implicit Models")) can be simplified to111Please refer to Appendix [C.2](#A3.SS2 "C.2 Derivation of denoising objectives for DDPMs ‣ Appendix C Additional Derivations ‣ Denoising Diffusion Implicit Models") for details.:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Lγ​(ϵθ)subscript𝐿𝛾subscriptitalic-ϵ𝜃\displaystyle L\_{\gamma}(\epsilon\_{\theta}) | :=∑t=1Tγt​𝔼𝒙0∼q​(𝒙0),ϵt∼𝒩​(𝟎,𝑰)​[∥ϵθ(t)​(αt​𝒙0+1−αt​ϵt)−ϵt∥22]assignabsentsuperscriptsubscript𝑡1𝑇subscript𝛾𝑡subscript𝔼formulae-sequencesimilar-tosubscript𝒙0𝑞subscript𝒙0similar-tosubscriptitalic-ϵ𝑡𝒩0𝑰delimited-[]superscriptsubscriptdelimited-∥∥superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡subscriptitalic-ϵ𝑡subscriptitalic-ϵ𝑡22\displaystyle:=\sum\_{t=1}^{T}\gamma\_{t}{\mathbb{E}}\_{{\bm{x}}\_{0}\sim q({\bm{x}}\_{0}),\epsilon\_{t}\sim{\mathcal{N}}({\bm{0}},{\bm{I}})}\left[{\lVert{\epsilon\_{\theta}^{(t)}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t}}\epsilon\_{t})-\epsilon\_{t}}\rVert}\_{2}^{2}\right] |  | (5) |

where ϵθ:={ϵθ(t)}t=1Tassignsubscriptitalic-ϵ𝜃superscriptsubscriptsuperscriptsubscriptitalic-ϵ𝜃𝑡𝑡1𝑇\epsilon\_{\theta}:=\{\epsilon\_{\theta}^{(t)}\}\_{t=1}^{T} is a set of T𝑇T functions, each ϵθ(t):𝒳→𝒳:superscriptsubscriptitalic-ϵ𝜃𝑡→𝒳𝒳\epsilon\_{\theta}^{(t)}:{\mathcal{X}}\to{\mathcal{X}} (indexed by t𝑡t) is a function with trainable parameters θ(t)superscript𝜃𝑡\theta^{(t)}, and γ:=[γ1,…,γT]assign𝛾

subscript𝛾1…subscript𝛾𝑇\gamma:=[\gamma\_{1},\ldots,\gamma\_{T}] is a vector of positive coefficients in the objective that depends on α1:Tsubscript𝛼:1𝑇\alpha\_{1:T}.
In Ho et al. ([2020](#bib.bib15)), the objective with γ=𝟏𝛾1\gamma={\bm{1}} is optimized instead to maximize generation performance of the trained model; this is also the same objective used in noise conditional score networks (Song & Ermon, [2019](#bib.bib34)) based on score matching (Hyvärinen, [2005](#bib.bib16); Vincent, [2011](#bib.bib39)). From a trained model, 𝒙0subscript𝒙0{\bm{x}}\_{0} is sampled by first sampling 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} from the prior pθ​(𝒙T)subscript𝑝𝜃subscript𝒙𝑇p\_{\theta}({\bm{x}}\_{T}), and then sampling 𝒙t−1subscript𝒙𝑡1{\bm{x}}\_{t-1} from the generative processes iteratively.

The length T𝑇T of the forward process is an important hyperparameter in DDPMs.
From a variational perspective, a large T𝑇T allows the reverse process to be close to a Gaussian (Sohl-Dickstein et al., [2015](#bib.bib32)), so that the generative process modeled with Gaussian conditional distributions becomes a good approximation; this motivates the choice of large T𝑇T values, such as T=1000𝑇1000T=1000 in Ho et al. ([2020](#bib.bib15)). However, as all T𝑇T iterations have to be performed sequentially, instead of in parallel, to obtain a sample 𝒙0subscript𝒙0{\bm{x}}\_{0}, sampling from DDPMs is much slower than sampling from other deep generative models, which makes them impractical for tasks where compute is limited and latency is critical.

## 3 Variational Inference for non-Markovian Forward Processes

Because the generative model approximates the reverse of the inference process, we need to rethink the inference process in order to reduce the number of iterations required by the generative model.
Our key observation is that the DDPM objective in the form of Lγsubscript𝐿𝛾L\_{\gamma} only depends on the marginals222We slightly abuse this term (as well as joints) when only conditioned on 𝒙0subscript𝒙0{\bm{x}}\_{0}. q​(𝒙t|𝒙0)𝑞conditionalsubscript𝒙𝑡subscript𝒙0q({\bm{x}}\_{t}|{\bm{x}}\_{0}), but not directly on the joint q​(𝒙1:T|𝒙0)𝑞conditionalsubscript𝒙:1𝑇subscript𝒙0q({\bm{x}}\_{1:T}|{\bm{x}}\_{0}). Since there are many inference distributions (joints) with the same marginals, we
explore
alternative
inference processes that are non-Markovian, which leads
to new generative processes (Figure [1](#S2.F1 "Figure 1 ‣ 2 Background ‣ Denoising Diffusion Implicit Models"), right).
These non-Markovian inference process lead to the same surrogate objective function as DDPM, as we will show below.
In Appendix [A](#A1 "Appendix A Non-Markovian Forward Processes for a Discrete Case ‣ Denoising Diffusion Implicit Models"), we show that the non-Markovian perspective also applies beyond the Gaussian case.

### 3.1 Non-Markovian forward processes

Let us consider a family 𝒬𝒬{\mathcal{Q}} of inference distributions, indexed by a real vector σ∈ℝ≥0T𝜎superscriptsubscriptℝabsent0𝑇\sigma\in\mathbb{R}\_{\geq 0}^{T}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙1:T|𝒙0):=qσ​(𝒙T|𝒙0)​∏t=2Tqσ​(𝒙t−1|𝒙t,𝒙0)assignsubscript𝑞𝜎conditionalsubscript𝒙:1𝑇subscript𝒙0subscript𝑞𝜎conditionalsubscript𝒙𝑇subscript𝒙0superscriptsubscriptproduct𝑡2𝑇subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0\displaystyle q\_{\sigma}({\bm{x}}\_{1:T}|{\bm{x}}\_{0}):=q\_{\sigma}({\bm{x}}\_{T}|{\bm{x}}\_{0})\prod\_{t=2}^{T}q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}) |  | (6) |

where qσ​(𝒙T|𝒙0)=𝒩​(αT​𝒙0,(1−αT)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑇subscript𝒙0𝒩subscript𝛼𝑇subscript𝒙01subscript𝛼𝑇𝑰q\_{\sigma}({\bm{x}}\_{T}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{T}}{\bm{x}}\_{0},(1-\alpha\_{T}){\bm{I}}) and for all t>1𝑡1t>1,

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙t−1|𝒙t,𝒙0)=𝒩​(αt−1​𝒙0+1−αt−1−σt2⋅𝒙t−αt​𝒙01−αt,σt2​𝑰).subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡1subscript𝒙0⋅1subscript𝛼𝑡1subscriptsuperscript𝜎2𝑡subscript𝒙𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡superscriptsubscript𝜎𝑡2𝑰\displaystyle q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})={\mathcal{N}}\left(\sqrt{\alpha\_{t-1}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t-1}-\sigma^{2}\_{t}}\cdot{\frac{{\bm{x}}\_{t}-\sqrt{\alpha\_{t}}{\bm{x}}\_{0}}{\sqrt{1-\alpha\_{t}}}},\sigma\_{t}^{2}{\bm{I}}\right). |  | (7) |

The mean function is chosen to order to ensure that qσ​(𝒙t|𝒙0)=𝒩​(αt​𝒙0,(1−αt)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡𝑰q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0},(1-\alpha\_{t}){\bm{I}}) for all t𝑡t
(see Lemma [1](#Thmlemma1 "Lemma 1. ‣ Appendix B Proofs ‣ Denoising Diffusion Implicit Models") of Appendix [B](#A2 "Appendix B Proofs ‣ Denoising Diffusion Implicit Models")), so that it defines a joint inference distribution that matches the ``marginals'' as desired. The forward process333We overload the term “forward process” for cases where the inference model is not a diffusion. can be derived from Bayes' rule:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙t|𝒙t−1,𝒙0)=qσ​(𝒙t−1|𝒙t,𝒙0)​qσ​(𝒙t|𝒙0)qσ​(𝒙t−1|𝒙0),subscript𝑞𝜎conditionalsubscript𝒙𝑡  subscript𝒙𝑡1subscript𝒙0subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0subscript𝑞𝜎conditionalsubscript𝒙𝑡1subscript𝒙0\displaystyle q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{t-1},{\bm{x}}\_{0})=\frac{q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0})}{q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{0})}, |  | (8) |

which is also Gaussian (although we do not use this fact for the remainder of this paper).
Unlike the diffusion process in Eq. ([3](#S2.E3 "In 2 Background ‣ Denoising Diffusion Implicit Models")), the forward process here is no longer Markovian, since each 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} could depend on both 𝒙t−1subscript𝒙𝑡1{\bm{x}}\_{t-1} and 𝒙0subscript𝒙0{\bm{x}}\_{0}. The magnitude of σ𝜎\sigma controls the how stochastic the forward process is; when σ→𝟎→𝜎0\sigma\to{\bm{0}}, we reach an extreme case where as long as we observe 𝒙0subscript𝒙0{\bm{x}}\_{0} and 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} for some t𝑡t, then 𝒙t−1subscript𝒙𝑡1{\bm{x}}\_{t-1} become known and fixed.

### 3.2 Generative process and unified variational inference objective

Next, we define a trainable generative process pθ​(𝒙0:T)subscript𝑝𝜃subscript𝒙:0𝑇p\_{\theta}({\bm{x}}\_{0:T}) where each pθ(t)​(𝒙t−1|𝒙t)superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}) leverages knowledge of qσ​(𝒙t−1|𝒙t,𝒙0)subscript𝑞𝜎conditionalsubscript𝒙𝑡1

subscript𝒙𝑡subscript𝒙0q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}). Intuitively, given a noisy observation 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t}, we first make a prediction444Learning a distribution over the predictions is also possible, but empirically we found little benefits of it. of the corresponding 𝒙0subscript𝒙0{\bm{x}}\_{0},
and then use it to obtain a sample 𝒙t−1subscript𝒙𝑡1{\bm{x}}\_{t-1} through the reverse conditional distribution qσ​(𝒙t−1|𝒙t,𝒙0)subscript𝑞𝜎conditionalsubscript𝒙𝑡1

subscript𝒙𝑡subscript𝒙0q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}), which we have defined.

For some 𝒙0∼q​(𝒙0)similar-tosubscript𝒙0𝑞subscript𝒙0{\bm{x}}\_{0}\sim q({\bm{x}}\_{0}) and ϵt∼𝒩​(𝟎,𝑰)similar-tosubscriptitalic-ϵ𝑡𝒩0𝑰\epsilon\_{t}\sim{\mathcal{N}}({\bm{0}},{\bm{I}}),
𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} can be obtained using Eq. ([4](#S2.E4 "In 2 Background ‣ Denoising Diffusion Implicit Models")). The model ϵθ(t)​(𝒙t)superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}) then attempts to predict ϵtsubscriptitalic-ϵ𝑡\epsilon\_{t} from 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t}, without knowledge of 𝒙0subscript𝒙0{\bm{x}}\_{0}.
By rewriting Eq. ([4](#S2.E4 "In 2 Background ‣ Denoising Diffusion Implicit Models")), one can then predict the denoised observation, which is a prediction of 𝒙0subscript𝒙0{\bm{x}}\_{0} given 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t}:

|  |  |  |  |
| --- | --- | --- | --- |
|  | fθ(t)​(𝒙t):=(𝒙t−1−αt⋅ϵθ(t)​(𝒙t))/αt.assignsuperscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡subscript𝒙𝑡⋅1subscript𝛼𝑡superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡subscript𝛼𝑡\displaystyle f\_{\theta}^{(t)}({\bm{x}}\_{t}):=({\bm{x}}\_{t}-\sqrt{1-\alpha\_{t}}\cdot\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}))/\sqrt{\alpha\_{t}}. |  | (9) |

We can then define the generative process with a fixed prior pθ​(𝒙T)=𝒩​(𝟎,𝑰)subscript𝑝𝜃subscript𝒙𝑇𝒩0𝑰p\_{\theta}({\bm{x}}\_{T})={\mathcal{N}}({\bm{0}},{\bm{I}}) and

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ(t)​(𝒙t−1|𝒙t)={𝒩​(fθ(1)​(𝒙1),σ12​𝑰)if​t=1qσ​(𝒙t−1|𝒙t,fθ(t)​(𝒙t))otherwise,superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡cases𝒩superscriptsubscript𝑓𝜃1subscript𝒙1superscriptsubscript𝜎12𝑰if𝑡1subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡otherwise,\displaystyle p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})=\begin{cases}{\mathcal{N}}(f\_{\theta}^{(1)}({\bm{x}}\_{1}),\sigma\_{1}^{2}{\bm{I}})&\text{if}\ t=1\\ q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},f\_{\theta}^{(t)}({\bm{x}}\_{t}))&\text{otherwise,}\end{cases} |  | (10) |

where qσ​(𝒙t−1|𝒙t,fθ(t)​(𝒙t))subscript𝑞𝜎conditionalsubscript𝒙𝑡1

subscript𝒙𝑡superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},f\_{\theta}^{(t)}({\bm{x}}\_{t})) is defined as in Eq. ([7](#S3.E7 "In 3.1 Non-Markovian forward processes ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")) with 𝒙0subscript𝒙0{\bm{x}}\_{0} replaced by fθ(t)​(𝒙t)superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡f\_{\theta}^{(t)}({\bm{x}}\_{t}). We add some Gaussian noise (with covariance σ12​𝑰superscriptsubscript𝜎12𝑰\sigma\_{1}^{2}{\bm{I}}) for the case of t=1𝑡1t=1 to ensure that the generative process is supported everywhere.

We optimize θ𝜃\theta via the following variational inference objective (which is a functional over ϵθsubscriptitalic-ϵ𝜃\epsilon\_{\theta}):

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | Jσ​(ϵθ):=𝔼𝒙0:T∼qσ​(𝒙0:T)​[log⁡qσ​(𝒙1:T|𝒙0)−log⁡pθ​(𝒙0:T)]assignsubscript𝐽𝜎subscriptitalic-ϵ𝜃subscript𝔼similar-tosubscript𝒙:0𝑇subscript𝑞𝜎subscript𝒙:0𝑇delimited-[]subscript𝑞𝜎conditionalsubscript𝒙:1𝑇subscript𝒙0subscript𝑝𝜃subscript𝒙:0𝑇\displaystyle J\_{\sigma}(\epsilon\_{\theta}):={\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q\_{\sigma}({\bm{x}}\_{0:T})}[\log q\_{\sigma}({\bm{x}}\_{1:T}|{\bm{x}}\_{0})-\log p\_{\theta}({\bm{x}}\_{0:T})] |  | (11) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | =\displaystyle= | 𝔼𝒙0:T∼qσ​(𝒙0:T)​[log⁡qσ​(𝒙T|𝒙0)+∑t=2Tlog⁡qσ​(𝒙t−1|𝒙t,𝒙0)−∑t=1Tlog⁡pθ(t)​(𝒙t−1|𝒙t)−log⁡pθ​(𝒙T)]subscript𝔼similar-tosubscript𝒙:0𝑇subscript𝑞𝜎subscript𝒙:0𝑇delimited-[]subscript𝑞𝜎conditionalsubscript𝒙𝑇subscript𝒙0superscriptsubscript𝑡2𝑇subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0superscriptsubscript𝑡1𝑇superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡subscript𝑝𝜃subscript𝒙𝑇\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q\_{\sigma}({\bm{x}}\_{0:T})}\left[\log q\_{\sigma}({\bm{x}}\_{T}|{\bm{x}}\_{0})+\sum\_{t=2}^{T}\log q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})-\sum\_{t=1}^{T}\log p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})-\log p\_{\theta}({\bm{x}}\_{T})\right] |  |

where we factorize qσ​(𝒙1:T|𝒙0)subscript𝑞𝜎conditionalsubscript𝒙:1𝑇subscript𝒙0q\_{\sigma}({\bm{x}}\_{1:T}|{\bm{x}}\_{0}) according to Eq. ([6](#S3.E6 "In 3.1 Non-Markovian forward processes ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")) and pθ​(𝒙0:T)subscript𝑝𝜃subscript𝒙:0𝑇p\_{\theta}({\bm{x}}\_{0:T}) according to Eq. ([1](#S2.E1 "In 2 Background ‣ Denoising Diffusion Implicit Models")).

From the definition of Jσsubscript𝐽𝜎J\_{\sigma}, it would appear that a different model has to be trained for every choice of σ𝜎\sigma, since it corresponds to a different variational objective (and a different generative process). However, Jσsubscript𝐽𝜎J\_{\sigma} is equivalent to Lγsubscript𝐿𝛾L\_{\gamma} for certain weights γ𝛾\gamma, as we show below.

###### Theorem 1.

For all σ>𝟎𝜎0\sigma>{\bm{0}}, there exists γ∈ℝ>0T𝛾superscriptsubscriptℝabsent0𝑇\gamma\in\mathbb{R}\_{>0}^{T} and C∈ℝ𝐶ℝC\in\mathbb{R}, such that Jσ=Lγ+Csubscript𝐽𝜎subscript𝐿𝛾𝐶J\_{\sigma}=L\_{\gamma}+C.

The variational objective Lγsubscript𝐿𝛾L\_{\gamma} is special in the sense that if parameters θ𝜃\theta of the models ϵθ(t)superscriptsubscriptitalic-ϵ𝜃𝑡\epsilon\_{\theta}^{(t)} are not shared across different t𝑡t, then the optimal solution for ϵθsubscriptitalic-ϵ𝜃\epsilon\_{\theta} will not depend on the weights γ𝛾\gamma (as global optimum is achieved by separately maximizing each term in the sum).
This property of Lγsubscript𝐿𝛾L\_{\gamma} has two implications. On the one hand, this justified the use of L𝟏subscript𝐿1L\_{\bm{1}} as a surrogate objective function for the variational lower bound in DDPMs; on the other hand, since Jσsubscript𝐽𝜎J\_{\sigma} is equivalent to some Lγsubscript𝐿𝛾L\_{\gamma} from Theorem [1](#Thmtheorem1 "Theorem 1. ‣ 3.2 Generative process and unified variational inference objective ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models"), the optimal solution of Jσsubscript𝐽𝜎J\_{\sigma} is also the same as that of L𝟏subscript𝐿1L\_{\bm{1}}. Therefore, if parameters are not shared across t𝑡t in the model ϵθsubscriptitalic-ϵ𝜃\epsilon\_{\theta}, then the L𝟏subscript𝐿1L\_{\bm{1}} objective used by Ho et al. ([2020](#bib.bib15)) can be used as a surrogate objective for the variational objective Jσsubscript𝐽𝜎J\_{\sigma} as well.

## 4 Sampling from Generalized Generative Processes

With L𝟏subscript𝐿1L\_{\bm{1}} as the objective, we are not only learning a generative process for the Markovian inference process considered in Sohl-Dickstein et al. ([2015](#bib.bib32)) and Ho et al. ([2020](#bib.bib15)), but also generative processes for many non-Markovian forward processes parametrized by σ𝜎\sigma that we have described. Therefore, we can essentially use pretrained DDPM models as the solutions to the new objectives, and focus on finding a generative process that is better at producing samples subject to our needs by changing σ𝜎\sigma.

### 4.1 Denoising Diffusion Implicit Models

From pθ​(𝒙1:T)subscript𝑝𝜃subscript𝒙:1𝑇p\_{\theta}({\bm{x}}\_{1:T}) in Eq. ([10](#S3.E10 "In 3.2 Generative process and unified variational inference objective ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")), one can generate a sample 𝒙t−1subscript𝒙𝑡1{\bm{x}}\_{t-1} from a sample 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} via:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | 𝒙t−1subscript𝒙𝑡1\displaystyle{\bm{x}}\_{t-1} | =αt−1​(𝒙t−1−αt​ϵθ(t)​(𝒙t)αt)⏟`` predicted ​𝒙0​''+1−αt−1−σt2⋅ϵθ(t)​(𝒙t)⏟``direction pointing to ​𝒙t​''+σt​ϵt⏟random noiseabsentsubscript𝛼𝑡1subscript⏟subscript𝒙𝑡1subscript𝛼𝑡superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡subscript𝛼𝑡`` predicted subscript𝒙0''subscript⏟⋅1subscript𝛼𝑡1superscriptsubscript𝜎𝑡2superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡``direction pointing to subscript𝒙𝑡''subscript⏟subscript𝜎𝑡subscriptitalic-ϵ𝑡random noise\displaystyle=\sqrt{\alpha\_{t-1}}\underbrace{\left(\frac{{\bm{x}}\_{t}-\sqrt{1-\alpha\_{t}}\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t})}{\sqrt{\alpha\_{t}}}\right)}\_{\text{`` predicted }{\bm{x}}\_{0}\text{''}}+\underbrace{\sqrt{1-\alpha\_{t-1}-\sigma\_{t}^{2}}\cdot\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t})}\_{\text{``direction pointing to }{\bm{x}}\_{t}\text{''}}+\underbrace{\sigma\_{t}\epsilon\_{t}}\_{\text{random noise}} |  | (12) |

where ϵt∼𝒩​(𝟎,𝑰)similar-tosubscriptitalic-ϵ𝑡𝒩0𝑰\epsilon\_{t}\sim{\mathcal{N}}({\bm{0}},{\bm{I}}) is standard Gaussian noise independent of 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t}, and we define α0:=1assignsubscript𝛼01\alpha\_{0}:=1. Different choices of σ𝜎\sigma values results in different generative processes, all while using the same model ϵθsubscriptitalic-ϵ𝜃\epsilon\_{\theta}, so re-training the model is unnecessary. When σt=(1−αt−1)/(1−αt)​1−αt/αt−1subscript𝜎𝑡1subscript𝛼𝑡11subscript𝛼𝑡1subscript𝛼𝑡subscript𝛼𝑡1\sigma\_{t}=\sqrt{(1-\alpha\_{t-1})/(1-\alpha\_{t})}\sqrt{1-\alpha\_{t}/\alpha\_{t-1}} for all t𝑡t, the forward process becomes Markovian, and the generative process becomes a DDPM.

We note another special case when σt=0subscript𝜎𝑡0\sigma\_{t}=0 for all t𝑡t555Although this case is not covered in Theorem [1](#Thmtheorem1 "Theorem 1. ‣ 3.2 Generative process and unified variational inference objective ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models"), we can always approximate it by making σtsubscript𝜎𝑡\sigma\_{t} very small.; the forward process becomes deterministic given 𝒙t−1subscript𝒙𝑡1{\bm{x}}\_{t-1} and 𝒙0subscript𝒙0{\bm{x}}\_{0}, except for t=1𝑡1t=1; in the generative process, the coefficient before the random noise ϵtsubscriptitalic-ϵ𝑡\epsilon\_{t} becomes zero. The resulting model becomes an implicit probabilistic model (Mohamed & Lakshminarayanan, [2016](#bib.bib23)), where samples are generated from latent variables with a fixed procedure (from 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} to 𝒙0subscript𝒙0{\bm{x}}\_{0}). We name this the denoising diffusion implicit model (DDIM, pronounced /d:Im/), because it is an implicit probabilistic model trained with the DDPM objective (despite the forward process no longer being a diffusion).

### 4.2 Accelerated generation processes

In the previous sections, the generative process is considered as the approximation to the reverse process; since of the forward process has T𝑇T steps, the generative process is also forced to sample T𝑇T steps. However, as the denoising objective L𝟏subscript𝐿1L\_{\bm{1}} does not depend on the specific forward procedure as long as qσ​(𝒙t|𝒙0)subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0}) is fixed, we may also consider forward processes with lengths smaller than T𝑇T, which accelerates the corresponding generative processes without having to train a different model.

![Refer to caption](/html/2010.02502/assets/x3.png)


Figure 2: Graphical model for accelerated generation, where τ=[1,3]𝜏13\tau=[1,3].

Let us consider the forward process as defined not on all the latent variables 𝒙1:Tsubscript𝒙:1𝑇{\bm{x}}\_{1:T}, but on a subset {𝒙τ1,…,𝒙τS}subscript𝒙subscript𝜏1…subscript𝒙subscript𝜏𝑆\{{\bm{x}}\_{\tau\_{1}},\ldots,{\bm{x}}\_{\tau\_{S}}\}, where τ𝜏\tau is an increasing sub-sequence of [1,…,T]

1…𝑇[1,\ldots,T] of length S𝑆S.
In particular, we define the sequential forward process over 𝒙τ1,…,𝒙τS

subscript𝒙subscript𝜏1…subscript𝒙subscript𝜏𝑆{\bm{x}}\_{\tau\_{1}},\ldots,{\bm{x}}\_{\tau\_{S}} such that q​(𝒙τi|𝒙0)=𝒩​(ατi​𝒙0,(1−ατi)​𝑰)𝑞conditionalsubscript𝒙subscript𝜏𝑖subscript𝒙0𝒩subscript𝛼subscript𝜏𝑖subscript𝒙01subscript𝛼subscript𝜏𝑖𝑰q({\bm{x}}\_{\tau\_{i}}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{\tau\_{i}}}{\bm{x}}\_{0},(1-\alpha\_{\tau\_{i}}){\bm{I}}) matches the ``marginals'' (see Figure [2](#S4.F2 "Figure 2 ‣ 4.2 Accelerated generation processes ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models") for an illustration).
The generative process now samples latent variables according to reversed​(τ)reversed𝜏\text{reversed}(\tau), which we term (sampling) trajectory. When the length of the sampling trajectory is much smaller than T𝑇T, we may achieve
significant increases in computational efficiency due to the iterative nature of the sampling process.

Using a similar argument as in Section [3](#S3 "3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models"), we can justify using the model trained with the L𝟏subscript𝐿1L\_{\bm{1}} objective, so no changes are needed in training. We show that only slight changes to the updates in Eq. ([12](#S4.E12 "In 4.1 Denoising Diffusion Implicit Models ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")) are needed to obtain the new, faster generative processes, which applies to DDPM, DDIM, as well as all generative processes considered in Eq. ([10](#S3.E10 "In 3.2 Generative process and unified variational inference objective ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")).
We include these details in Appendix [C.1](#A3.SS1 "C.1 Accelerated sampling processes ‣ Appendix C Additional Derivations ‣ Denoising Diffusion Implicit Models").

In principle, this means that we can train a model with an arbitrary number of forward steps but only sample from some of them in the generative process. Therefore, the trained model could consider many more steps than what is considered in (Ho et al., [2020](#bib.bib15)) or even a continuous time variable t𝑡t (Chen et al., [2020](#bib.bib7)). We leave empirical investigations of this aspect as future work.

### 4.3 Relevance to Neural ODEs

Moreover, we can rewrite the DDIM iterate according to Eq. ([12](#S4.E12 "In 4.1 Denoising Diffusion Implicit Models ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")), and its similarity to Euler integration for solving ordinary differential equations (ODEs) becomes more apparent:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙t−Δ​tαt−Δ​t=𝒙tαt+(1−αt−Δ​tαt−Δ​t−1−αtαt)​ϵθ(t)​(𝒙t)subscript𝒙𝑡Δ𝑡subscript𝛼𝑡Δ𝑡subscript𝒙𝑡subscript𝛼𝑡1subscript𝛼𝑡Δ𝑡subscript𝛼𝑡Δ𝑡1subscript𝛼𝑡subscript𝛼𝑡superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡\displaystyle\frac{{\bm{x}}\_{t-\Delta t}}{\sqrt{\alpha\_{t-\Delta t}}}=\frac{{\bm{x}}\_{t}}{\sqrt{\alpha\_{t}}}+\left(\sqrt{\frac{1-\alpha\_{t-\Delta t}}{\alpha\_{t-\Delta t}}}-\sqrt{\frac{1-\alpha\_{t}}{\alpha\_{t}}}\right)\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}) |  | (13) |

To derive the corresponding ODE, we can reparameterize (1−α/α)1𝛼𝛼(\sqrt{1-\alpha}/\sqrt{\alpha}) with σ𝜎\sigma and (𝒙/α)𝒙𝛼({\bm{x}}/\sqrt{\alpha}) with 𝒙¯¯𝒙\bar{{\bm{x}}}. In the continuous case, σ𝜎\sigma and 𝒙𝒙{\bm{x}} are functions of t𝑡t, where σ:ℝ≥0→ℝ≥0:𝜎→subscriptℝabsent0subscriptℝabsent0\sigma:{\mathbb{R}}\_{\geq 0}\to{\mathbb{R}}\_{\geq 0} is continous, increasing with σ​(0)=0𝜎00\sigma(0)=0.
Equation ([13](#S4.E13 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")) with can be treated as a Euler method over the following ODE:

|  |  |  |  |
| --- | --- | --- | --- |
|  | d​𝒙¯​(t)=ϵθ(t)​(𝒙¯​(t)σ2+1)​d​σ​(t),d¯𝒙𝑡superscriptsubscriptitalic-ϵ𝜃𝑡¯𝒙𝑡superscript𝜎21d𝜎𝑡\displaystyle\mathrm{d}\bar{{\bm{x}}}(t)=\epsilon\_{\theta}^{(t)}\left(\frac{\bar{{\bm{x}}}(t)}{\sqrt{\sigma^{2}+1}}\right)\mathrm{d}\sigma(t), |  | (14) |

where the initial conditions is 𝒙​(T)∼𝒩​(0,σ​(T))similar-to𝒙𝑇𝒩0𝜎𝑇{\bm{x}}(T)\sim{\mathcal{N}}(0,\sigma(T)) for a very large σ​(T)𝜎𝑇\sigma(T) (which corresponds to the case of α≈0𝛼0\alpha\approx 0). This suggests that with enough discretization steps, the we can also reverse the generation process (going from t=0𝑡0t=0 to T𝑇T), which encodes 𝒙0subscript𝒙0{\bm{x}}\_{0} to 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} and simulates the reverse of the ODE in Eq. ([14](#S4.E14 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")). This suggests that unlike DDPM, we can use DDIM to obtain encodings of the observations (as the form of 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T}), which might be useful for other downstream applications that requires latent representations of a model.

In a concurrent work, (Song et al., [2020](#bib.bib36)) proposed a ``probability flow ODE'' that aims to recover the marginal densities of a stochastic differential equation (SDE) based on scores, from which a similar sampling schedule can be obtained. Here, we state that the our ODE is equivalent to a special case of theirs (which corresponds to a continuous-time analog of DDPM).

###### Proposition 1.

The ODE in Eq. ([14](#S4.E14 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")) with the optimal model ϵθ(t)superscriptsubscriptitalic-ϵ𝜃𝑡\epsilon\_{\theta}^{(t)} has an equivalent probability flow ODE corresponding to the ``Variance-Exploding'' SDE in Song et al. ([2020](#bib.bib36)).

We include the proof in Appendix [B](#A2 "Appendix B Proofs ‣ Denoising Diffusion Implicit Models"). While the ODEs are equivalent, the sampling procedures are not, since the Euler method for the probability flow ODE will make the following update:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙t−Δ​tαt−Δ​t=𝒙tαt+12​(1−αt−Δ​tαt−Δ​t−1−αtαt)⋅αt1−αt⋅ϵθ(t)​(𝒙t)subscript𝒙𝑡Δ𝑡subscript𝛼𝑡Δ𝑡subscript𝒙𝑡subscript𝛼𝑡⋅121subscript𝛼𝑡Δ𝑡subscript𝛼𝑡Δ𝑡1subscript𝛼𝑡subscript𝛼𝑡subscript𝛼𝑡1subscript𝛼𝑡superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡\displaystyle\frac{{\bm{x}}\_{t-\Delta t}}{\sqrt{\alpha\_{t-\Delta t}}}=\frac{{\bm{x}}\_{t}}{\sqrt{\alpha\_{t}}}+\frac{1}{2}\left(\frac{1-\alpha\_{t-\Delta t}}{\alpha\_{t-\Delta t}}-\frac{1-\alpha\_{t}}{\alpha\_{t}}\right)\cdot\sqrt{\frac{\alpha\_{t}}{1-\alpha\_{t}}}\cdot\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}) |  | (15) |

which is equivalent to ours if αtsubscript𝛼𝑡\alpha\_{t} and αt−Δ​tsubscript𝛼𝑡Δ𝑡\alpha\_{t-\Delta t} are close enough. In fewer sampling steps, however, these choices will make a difference; we take Euler steps with respect to d​σ​(t)d𝜎𝑡\mathrm{d}\sigma(t) (which depends less directly on the scaling of ``time'' t𝑡t) whereas Song et al. ([2020](#bib.bib36)) take Euler steps with respect to d​td𝑡\mathrm{d}t.

## 5 Experiments

In this section, we show that DDIMs outperform DDPMs in terms of image generation when fewer iterations are considered, giving speed ups of 10×10\times to 100×100\times over the original DDPM generation process. Moreover, unlike DDPMs, once the initial latent variables 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} are fixed, DDIMs retain high-level image features regardless of the generation trajectory, so they are able to perform interpolation directly from the latent space. DDIMs can also be used to encode samples that reconstruct them from the latent code, which DDPMs cannot do due to the stochastic sampling process.

For each dataset, we use the same trained model with T=1000𝑇1000T=1000 and the objective being Lγsubscript𝐿𝛾L\_{\gamma} from Eq. ([5](#S2.E5 "In 2 Background ‣ Denoising Diffusion Implicit Models")) with γ=𝟏𝛾1\gamma={\bm{1}}; as we argued in Section [3](#S3 "3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models"), no changes are needed with regards to the training procedure.
The only changes that we make is how we produce samples from the model; we achieve this by controlling τ𝜏\tau (which controls how fast the samples are obtained) and σ𝜎\sigma (which interpolates between the deterministic DDIM and the stochastic DDPM).

We consider different sub-sequences τ𝜏\tau of [1,…,T]

1…𝑇[1,\ldots,T] and different variance hyperparameters σ𝜎\sigma indexed by elements of τ𝜏\tau. To simplify comparisons, we consider σ𝜎\sigma with the form:

|  |  |  |  |
| --- | --- | --- | --- |
|  | στi​(η)=η​(1−ατi−1)/(1−ατi)​1−ατi/ατi−1,subscript𝜎subscript𝜏𝑖𝜂𝜂1subscript𝛼subscript𝜏𝑖11subscript𝛼subscript𝜏𝑖1subscript𝛼subscript𝜏𝑖subscript𝛼subscript𝜏𝑖1\displaystyle\sigma\_{\tau\_{i}}(\eta)=\eta\sqrt{(1-\alpha\_{\tau\_{i-1}})/(1-\alpha\_{\tau\_{i}})}\sqrt{1-{\alpha\_{\tau\_{i}}}/{\alpha\_{\tau\_{i-1}}}}, |  | (16) |

where η∈ℝ≥0𝜂subscriptℝabsent0\eta\in\mathbb{R}\_{\geq 0} is a hyperparameter that we can directly control. This includes an original DDPM generative process when η=1𝜂1\eta=1 and DDIM when η=0𝜂0\eta=0. We also consider DDPM where the random noise has a larger standard deviation than σ​(1)𝜎1\sigma(1), which we denote as σ^^𝜎\hat{\sigma}:
σ^τi=1−ατi/ατi−1subscript^𝜎subscript𝜏𝑖1subscript𝛼subscript𝜏𝑖subscript𝛼subscript𝜏𝑖1\hat{\sigma}\_{\tau\_{i}}=\sqrt{1-{\alpha\_{\tau\_{i}}}/{\alpha\_{\tau\_{i-1}}}}
. This is used by [the implementation](https://github.com/hojonathanho/diffusion/blob/master/scripts/run_cifar.py#L136) in Ho et al. ([2020](#bib.bib15)) only to obtain the CIFAR10 samples, but not samples of the other datasets. We include more details in Appendix [D](#A4 "Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models").

### 5.1 Sample quality and efficiency

In Table [1](#S5.T1 "Table 1 ‣ 5.1 Sample quality and efficiency ‣ 5 Experiments ‣ Denoising Diffusion Implicit Models"), we report the quality of the generated samples with models trained on CIFAR10 and CelebA, as measured by Frechet Inception Distance (FID (Heusel et al., [2017](#bib.bib14))), where we vary the number of timesteps used to generate a sample (dim(τ)dimension𝜏\dim(\tau)) and the stochasticity of the process (η𝜂\eta).
As expected, the sample quality becomes higher as we increase dim(τ)dimension𝜏\dim(\tau), presenting a trade-off between sample quality and computational costs.
We observe that DDIM (η=0𝜂0\eta=0) achieves the best sample quality when dim(τ)dimension𝜏\dim(\tau) is small, and DDPM (η=1𝜂1\eta=1 and σ^^𝜎\hat{\sigma}) typically has worse sample quality compared to its less stochastic counterparts with the same dim(τ)dimension𝜏\dim(\tau), except for the case for dim(τ)=1000dimension𝜏1000\dim(\tau)=1000 and σ^^𝜎\hat{\sigma} reported by Ho et al. ([2020](#bib.bib15)) where DDIM is marginally worse. However, the sample quality of σ^^𝜎\hat{\sigma} becomes much worse for smaller dim(τ)dimension𝜏\dim(\tau), which suggests that it is ill-suited for shorter trajectories. DDIM, on the other hand, achieves high sample quality much more consistently.

In Figure [3](#S5.F3 "Figure 3 ‣ 5.1 Sample quality and efficiency ‣ 5 Experiments ‣ Denoising Diffusion Implicit Models"), we show CIFAR10 and CelebA samples with the same number of sampling steps and varying σ𝜎\sigma. For the DDPM, the sample quality deteriorates rapidly when the sampling trajectory has 10 steps. For the case of σ^^𝜎\hat{\sigma}, the generated images seem to have more noisy perturbations under short trajectories; this explains why the FID scores are much worse than other methods, as FID is very sensitive to such perturbations (as discussed in Jolicoeur-Martineau et al. ([2020](#bib.bib17))).

In Figure [4](#S5.F4 "Figure 4 ‣ 5.1 Sample quality and efficiency ‣ 5 Experiments ‣ Denoising Diffusion Implicit Models"), we show that the amount of time needed to produce a sample scales linearly with the length of the sample trajectory. This suggests that DDIM is useful for producing samples more efficiently, as samples can be generated in much fewer steps. Notably, DDIM is able to produce samples with quality comparable to 1000 step models within 202020 to 100100100 steps, which is a 10×10\times to 50×50\times speed up compared to the original DDPM. Even though DDPM could also achieve reasonable sample quality with 100×100\times steps, DDIM requires much fewer steps to achieve this; on CelebA, the FID score of the 100 step DDPM is similar to that of the 20 step DDIM.

Table 1: CIFAR10 and CelebA image generation measured in FID. η=1.0𝜂1.0\eta=1.0 and σ^^𝜎\hat{\sigma} are cases of DDPM (although Ho et al. ([2020](#bib.bib15)) only considered T=1000𝑇1000T=1000 steps, and S<T𝑆𝑇S<T can be seen as simulating DDPMs trained with S𝑆S steps), and η=0.0𝜂0.0\eta=0.0 indicates DDIM.

|  |  | CIFAR10 (32×32323232\times 32) | | | | | CelebA (64×64646464\times 64) | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S𝑆S | | 10 | 20 | 50 | 100 | 1000 | 10 | 20 | 50 | 100 | 1000 |
| η𝜂\eta | 0.00.00.0 | 13.36 | 6.84 | 4.67 | 4.16 | 4.04 | 17.33 | 13.73 | 9.17 | 6.53 | 3.51 |
| 0.2 | 14.04 | 7.11 | 4.77 | 4.25 | 4.09 | 17.66 | 14.11 | 9.51 | 6.79 | 3.64 |
| 0.5 | 16.66 | 8.35 | 5.25 | 4.46 | 4.29 | 19.86 | 16.06 | 11.01 | 8.09 | 4.28 |
| 1.0 | 41.07 | 18.36 | 8.01 | 5.78 | 4.73 | 33.12 | 26.03 | 18.48 | 13.93 | 5.98 |
| σ^^𝜎\hat{\sigma} | | 367.43 | 133.37 | 32.72 | 9.99 | 3.17 | 299.71 | 183.83 | 71.71 | 45.20 | 3.26 |



![Refer to caption](/html/2010.02502/assets/x4.png)

![Refer to caption](/html/2010.02502/assets/x5.png)

![Refer to caption](/html/2010.02502/assets/x6.png)

![Refer to caption](/html/2010.02502/assets/x7.png)

Figure 3: CIFAR10 and CelebA samples with dim(τ)=10dimension𝜏10\dim(\tau)=10 and dim(τ)=100dimension𝜏100\dim(\tau)=100.



![Refer to caption](/html/2010.02502/assets/x8.png)

![Refer to caption](/html/2010.02502/assets/x9.png)

Figure 4: Hours to sample 50k images with one Nvidia 2080 Ti GPU and samples at different steps.

### 5.2 Sample consistency in DDIMs

For DDIM, the generative process is deterministic, and 𝒙0subscript𝒙0{\bm{x}}\_{0} would depend only on the initial state 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T}. In Figure [5](#S5.F5 "Figure 5 ‣ 5.2 Sample consistency in DDIMs ‣ 5 Experiments ‣ Denoising Diffusion Implicit Models"), we observe the generated images under different generative trajectories (i.e. different τ𝜏\tau) while starting with the same initial 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T}. Interestingly, for the generated images with the same initial 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T}, most high-level features are similar, regardless of the generative trajectory. In many cases, samples generated with only 20 steps are already very similar to ones generated with 1000 steps in terms of high-level features, with only minor differences in details.
Therefore, it would appear that 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} alone would be an informative latent encoding of the image; and minor details that affects sample quality are encoded in the parameters, as longer sample trajectories gives better quality samples but do not significantly affect the high-level features.
We show more samples in Appendix [D.4](#A4.SS4 "D.4 Samples and Consistency ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models").

![Refer to caption](/html/2010.02502/assets/x10.png)

![Refer to caption](/html/2010.02502/assets/x11.png)

![Refer to caption](/html/2010.02502/assets/x12.png)

Figure 5: Samples from DDIM with the same random 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} and different number of steps.

### 5.3 Interpolation in deterministic generative processes

![Refer to caption](/html/2010.02502/assets/figures/celeba-interp-line.png)

![Refer to caption](/html/2010.02502/assets/figures/bedroom-interp-line.png)

![Refer to caption](/html/2010.02502/assets/figures/church-interp-line.png)

Figure 6: Interpolation of samples from DDIM with dim(τ)=50dimension𝜏50\dim(\tau)=50.

Since the high level features of the DDIM sample is encoded by 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T}, we are interested to see whether it would exhibit the semantic interpolation effect similar to that observed in other implicit probabilistic models, such as GANs (Goodfellow et al., [2014](#bib.bib10)). This is different from the interpolation procedure in Ho et al. ([2020](#bib.bib15)), since in DDPM the same 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} would lead to highly diverse 𝒙0subscript𝒙0{\bm{x}}\_{0} due to the stochastic generative process666Although it might be possible if one interpolates all T𝑇T noises, like what is done in Song & Ermon ([2020](#bib.bib35)).. In Figure [6](#S5.F6 "Figure 6 ‣ 5.3 Interpolation in deterministic generative processes ‣ 5 Experiments ‣ Denoising Diffusion Implicit Models"), we show that simple interpolations in 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} can lead to semantically meaningful interpolations between two samples. We include more details and samples in Appendix [D.5](#A4.SS5 "D.5 Interpolation ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models"). This allows DDIM to control the generated images on a high level directly through the latent variables, which DDPMs cannot.

### 5.4 Reconstruction from Latent Space

As DDIM is the Euler integration for a particular ODE, it would be interesting to see whether it can encode from 𝒙0subscript𝒙0{\bm{x}}\_{0} to 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} (reverse of Eq. ([14](#S4.E14 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models"))) and reconstruct 𝒙0subscript𝒙0{\bm{x}}\_{0} from the resulting 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} (forward of Eq. ([14](#S4.E14 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")))777Since 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} and 𝒙0subscript𝒙0{\bm{x}}\_{0} have the same dimensions, their compression qualities are not our immediate concern.. We consider encoding and decoding on the CIFAR-10 test set with the CIFAR-10 model with S𝑆S steps for both encoding and decoding; we report the per-dimension mean squared error (scaled to [0,1]01[0,1]) in Table [2](#S5.T2 "Table 2 ‣ 5.4 Reconstruction from Latent Space ‣ 5 Experiments ‣ Denoising Diffusion Implicit Models"). Our results show that DDIMs have lower reconstruction error for larger S𝑆S values and have properties similar to Neural ODEs and normalizing flows.
The same cannot be said for DDPMs due to their stochastic nature.

Table 2: Reconstruction error with DDIM on CIFAR-10 test set, rounded to 10−4superscript10410^{-4}.

| S𝑆S | 10 | 20 | 50 | 100 | 200 | 500 | 1000 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Error | 0.014 | 0.0065 | 0.0023 | 0.0009 | 0.0004 | 0.0001 | 0.00010.00010.0001 |

## 6 Related Work

Our work is based on a large family of existing methods on learning generative models as transition operators of Markov chains (Sohl-Dickstein et al., [2015](#bib.bib32); Bengio et al., [2014](#bib.bib3); Salimans et al., [2014](#bib.bib30); Song et al., [2017](#bib.bib33); Goyal et al., [2017](#bib.bib11); Levy et al., [2017](#bib.bib22)). Among them, denoising diffusion probabilistic models (DDPMs, Ho et al. ([2020](#bib.bib15))) and noise conditional score networks (NCSN, Song & Ermon ([2019](#bib.bib34); [2020](#bib.bib35))) have recently achieved high sample quality comparable to GANs (Brock et al., [2018](#bib.bib5); Karras et al., [2018](#bib.bib19)). DDPMs optimize a variational lower bound to the log-likelihood, whereas NCSNs optimize the score matching objective (Hyvärinen, [2005](#bib.bib16)) over a nonparametric Parzen density estimator of the data (Vincent, [2011](#bib.bib39); Raphan & Simoncelli, [2011](#bib.bib26)).

Despite their different motivations, DDPMs and NCSNs are closely related. Both use a denoising autoencoder objective for many noise levels, and both use a procedure similar to Langevin dynamics to produce samples (Neal et al., [2011](#bib.bib24)). Since Langevin dynamics is a discretization of a gradient flow (Jordan et al., [1998](#bib.bib18)), both DDPM and NCSN require many steps to achieve good sample quality. This aligns with the observation that DDPM and existing NCSN methods have trouble generating high-quality samples in a few iterations.

DDIM, on the other hand, is an implicit generative model (Mohamed & Lakshminarayanan, [2016](#bib.bib23)) where samples are uniquely determined from the latent variables. Hence, DDIM has certain properties that resemble GANs (Goodfellow et al., [2014](#bib.bib10)) and invertible flows (Dinh et al., [2016](#bib.bib9)), such as the ability to produce semantically meaningful interpolations. We derive DDIM from a purely variational perspective, where the restrictions of Langevin dynamics are not relevant; this could partially explain why we are able to observe superior sample quality compared to DDPM under fewer iterations. The sampling procedure of DDIM is also reminiscent of neural networks with continuous depth (Chen et al., [2018](#bib.bib8); Grathwohl et al., [2018](#bib.bib12)), since the samples it produces from the same latent variable have similar high-level visual features, regardless of the specific sample trajectory.

## 7 Discussion

We have presented DDIMs – an implicit generative model trained with denoising auto-encoding / score matching objectives – from a purely variational perspective. DDIM is able to generate high-quality samples much more efficiently than existing DDPMs and NCSNs, with the ability to perform meaningful interpolations from the latent space. The non-Markovian forward process presented here seems to suggest continuous forward processes other than Gaussian (which cannot be done in the original diffusion framework, since Gaussian is the only stable distribution with finite variance). We also demonstrated a discrete case with a multinomial forward process in Appendix [A](#A1 "Appendix A Non-Markovian Forward Processes for a Discrete Case ‣ Denoising Diffusion Implicit Models"), and it would be interesting to investigate similar alternatives for other combinatorial structures.

Moreover, since the sampling procedure of DDIMs is similar to that of an neural ODE, it would be interesting to see if methods that decrease the discretization error in ODEs, including multi-step methods such as Adams-Bashforth (Butcher & Goodwin, [2008](#bib.bib6)), could be helpful for further improving sample quality in fewer steps (Queiruga et al., [2020](#bib.bib25)). It is also relevant to investigate whether DDIMs exhibit other properties of existing implicit models (Bau et al., [2019](#bib.bib2)).

## Acknowledgements

The authors would like to thank Yang Song and Shengjia Zhao for helpful discussions over the ideas, Kuno Kim for reviewing an earlier draft of the paper, and Sharvil Nanavati and Sophie Liu for identifying typos. This research was supported by NSF (#1651565, #1522054, #1733686), ONR (N00014-19-1-2145), AFOSR (FA9550-19-1-0024), and Amazon AWS.

## References

* Arjovsky et al. (2017)

  Martin Arjovsky, Soumith Chintala, and Léon Bottou.
  Wasserstein GAN.
  *arXiv preprint arXiv:1701.07875*, January 2017.
* Bau et al. (2019)

  David Bau, Jun-Yan Zhu, Jonas Wulff, William Peebles, Hendrik Strobelt, Bolei
  Zhou, and Antonio Torralba.
  Seeing what a gan cannot generate.
  In *Proceedings of the IEEE International Conference on Computer
  Vision*, pp.  4502–4511, 2019.
* Bengio et al. (2014)

  Yoshua Bengio, Eric Laufer, Guillaume Alain, and Jason Yosinski.
  Deep generative stochastic networks trainable by backprop.
  In *International Conference on Machine Learning*, pp. 226–234, January 2014.
* Bishop (2006)

  Christopher M Bishop.
  *Pattern recognition and machine learning*.
  springer, 2006.
* Brock et al. (2018)

  Andrew Brock, Jeff Donahue, and Karen Simonyan.
  Large scale GAN training for high fidelity natural image synthesis.
  *arXiv preprint arXiv:1809.11096*, September 2018.
* Butcher & Goodwin (2008)

  John Charles Butcher and Nicolette Goodwin.
  *Numerical methods for ordinary differential equations*,
  volume 2.
  Wiley Online Library, 2008.
* Chen et al. (2020)

  Nanxin Chen, Yu Zhang, Heiga Zen, Ron J Weiss, Mohammad Norouzi, and William
  Chan.
  WaveGrad: Estimating gradients for waveform generation.
  *arXiv preprint arXiv:2009.00713*, September 2020.
* Chen et al. (2018)

  Ricky T Q Chen, Yulia Rubanova, Jesse Bettencourt, and David Duvenaud.
  Neural ordinary differential equations.
  *arXiv preprint arXiv:1806.07366*, June 2018.
* Dinh et al. (2016)

  Laurent Dinh, Jascha Sohl-Dickstein, and Samy Bengio.
  Density estimation using real NVP.
  *arXiv preprint arXiv:1605.08803*, May 2016.
* Goodfellow et al. (2014)

  Ian Goodfellow, Jean Pouget-Abadie, Mehdi Mirza, Bing Xu, David Warde-Farley,
  Sherjil Ozair, Aaron Courville, and Yoshua Bengio.
  Generative adversarial nets.
  In *Advances in neural information processing systems*, pp. 2672–2680, 2014.
* Goyal et al. (2017)

  Anirudh Goyal, Nan Rosemary Ke, Surya Ganguli, and Yoshua Bengio.
  Variational walkback: Learning a transition operator as a stochastic
  recurrent net.
  In *Advances in Neural Information Processing Systems*, pp. 4392–4402, 2017.
* Grathwohl et al. (2018)

  Will Grathwohl, Ricky T Q Chen, Jesse Bettencourt, Ilya Sutskever, and David
  Duvenaud.
  FFJORD: Free-form continuous dynamics for scalable reversible
  generative models.
  *arXiv preprint arXiv:1810.01367*, October 2018.
* Gulrajani et al. (2017)

  Ishaan Gulrajani, Faruk Ahmed, Martin Arjovsky, Vincent Dumoulin, and Aaron C
  Courville.
  Improved training of wasserstein gans.
  In *Advances in Neural Information Processing Systems*, pp. 5769–5779, 2017.
* Heusel et al. (2017)

  Martin Heusel, Hubert Ramsauer, Thomas Unterthiner, Bernhard Nessler, and Sepp
  Hochreiter.
  GANs trained by a two Time-Scale update rule converge to a local
  nash equilibrium.
  *arXiv preprint arXiv:1706.08500*, June 2017.
* Ho et al. (2020)

  Jonathan Ho, Ajay Jain, and Pieter Abbeel.
  Denoising diffusion probabilistic models.
  *arXiv preprint arXiv:2006.11239*, June 2020.
* Hyvärinen (2005)

  Aapo Hyvärinen.
  Estimation of Non-Normalized statistical models by score matching.
  *Journal of Machine Learning Researc h*, 6:695–709,
  2005.
* Jolicoeur-Martineau et al. (2020)

  Alexia Jolicoeur-Martineau, Rémi Piché-Taillefer, Rémi Tachet des
  Combes, and Ioannis Mitliagkas.
  Adversarial score matching and improved sampling for image
  generation.
  September 2020.
* Jordan et al. (1998)

  Richard Jordan, David Kinderlehrer, and Felix Otto.
  The variational formulation of the fokker–planck equation.
  *SIAM journal on mathematical analysis*, 29(1):1–17, 1998.
* Karras et al. (2018)

  Tero Karras, Samuli Laine, and Timo Aila.
  A Style-Based generator architecture for generative adversarial
  networks.
  *arXiv preprint arXiv:1812.04948*, December 2018.
* Karras et al. (2020)

  Tero Karras, Samuli Laine, Miika Aittala, Janne Hellsten, Jaakko Lehtinen, and
  Timo Aila.
  Analyzing and improving the image quality of stylegan.
  In *Proceedings of the IEEE/CVF Conference on Computer Vision
  and Pattern Recognition*, pp.  8110–8119, 2020.
* Kingma & Welling (2013)

  Diederik P Kingma and Max Welling.
  Auto-Encoding variational bayes.
  *arXiv preprint arXiv:1312.6114v10*, December 2013.
* Levy et al. (2017)

  Daniel Levy, Matthew D Hoffman, and Jascha Sohl-Dickstein.
  Generalizing hamiltonian monte carlo with neural networks.
  *arXiv preprint arXiv:1711.09268*, 2017.
* Mohamed & Lakshminarayanan (2016)

  Shakir Mohamed and Balaji Lakshminarayanan.
  Learning in implicit generative models.
  *arXiv preprint arXiv:1610.03483*, October 2016.
* Neal et al. (2011)

  Radford M Neal et al.
  Mcmc using hamiltonian dynamics.
  *Handbook of markov chain monte carlo*, 2(11):2, 2011.
* Queiruga et al. (2020)

  Alejandro F Queiruga, N Benjamin Erichson, Dane Taylor, and Michael W Mahoney.
  Continuous-in-depth neural networks.
  *arXiv preprint arXiv:2008.02389*, 2020.
* Raphan & Simoncelli (2011)

  Martin Raphan and Eero P Simoncelli.
  Least squares estimation without priors or supervision.
  *Neural computation*, 23(2):374–420,
  February 2011.
  ISSN 0899-7667, 1530-888X.
* Rezende & Mohamed (2015)

  Danilo Jimenez Rezende and Shakir Mohamed.
  Variational inference with normalizing flows.
  *arXiv preprint arXiv:1505.05770*, May 2015.
* Rezende et al. (2014)

  Danilo Jimenez Rezende, Shakir Mohamed, and Daan Wierstra.
  Stochastic backpropagation and approximate inference in deep
  generative models.
  *arXiv preprint arXiv:1401.4082*, 2014.
* Ronneberger et al. (2015)

  Olaf Ronneberger, Philipp Fischer, and Thomas Brox.
  U-net: Convolutional networks for biomedical image segmentation.
  In *International Conference on Medical image computing and
  computer-assisted intervention*, pp.  234–241. Springer, 2015.
* Salimans et al. (2014)

  Tim Salimans, Diederik P Kingma, and Max Welling.
  Markov chain monte carlo and variational inference: Bridging the gap.
  *arXiv preprint arXiv:1410.6460*, October 2014.
* Shoemake (1985)

  Ken Shoemake.
  Animating rotation with quaternion curves.
  In *Proceedings of the 12th annual conference on Computer
  graphics and interactive techniques*, pp.  245–254, 1985.
* Sohl-Dickstein et al. (2015)

  Jascha Sohl-Dickstein, Eric A Weiss, Niru Maheswaranathan, and Surya Ganguli.
  Deep unsupervised learning using nonequilibrium thermodynamics.
  *arXiv preprint arXiv:1503.03585*, March 2015.
* Song et al. (2017)

  Jiaming Song, Shengjia Zhao, and Stefano Ermon.
  A-nice-mc: Adversarial training for mcmc.
  *arXiv preprint arXiv:1706.07561*, June 2017.
* Song & Ermon (2019)

  Yang Song and Stefano Ermon.
  Generative modeling by estimating gradients of the data distribution.
  *arXiv preprint arXiv:1907.05600*, July 2019.
* Song & Ermon (2020)

  Yang Song and Stefano Ermon.
  Improved techniques for training Score-Based generative models.
  *arXiv preprint arXiv:2006.09011*, June 2020.
* Song et al. (2020)

  Yang Song, Jascha Sohl-Dickstein, Diederik P Kingma, Abhishek Kumar, Stefano
  Ermon, and Ben Poole.
  Score-based generative modeling through stochastic differential
  equations.
  *arXiv preprint arXiv:2011.13456*, 2020.
* van den Oord et al. (2016a)

  Aaron van den Oord, Sander Dieleman, Heiga Zen, Karen Simonyan, Oriol Vinyals,
  Alex Graves, Nal Kalchbrenner, Andrew Senior, and Koray Kavukcuoglu.
  WaveNet: A generative model for raw audio.
  *arXiv preprint arXiv:1609.03499*, September 2016a.
* van den Oord et al. (2016b)

  Aaron van den Oord, Nal Kalchbrenner, and Koray Kavukcuoglu.
  Pixel recurrent neural networks.
  *arXiv preprint arXiv:1601.06759*, January 2016b.
* Vincent (2011)

  Pascal Vincent.
  A connection between score matching and denoising autoencoders.
  *Neural computation*, 23(7):1661–1674,
  2011.
* Zagoruyko & Komodakis (2016)

  Sergey Zagoruyko and Nikos Komodakis.
  Wide residual networks.
  *arXiv preprint arXiv:1605.07146*, May 2016.
* Zhao et al. (2018)

  Shengjia Zhao, Hongyu Ren, Arianna Yuan, Jiaming Song, Noah Goodman, and
  Stefano Ermon.
  Bias and generalization in deep generative models: An empirical
  study.
  In *Advances in Neural Information Processing Systems*, pp. 10792–10801, 2018.

## Appendix A Non-Markovian Forward Processes for a Discrete Case

In this section, we describe a non-Markovian forward processes for discrete data and corresponding variational objectives. Since the focus of this paper is to accelerate reverse models corresponding to the Gaussian diffusion, we leave empirical evaluations as future work.

For a categorical observation 𝒙0subscript𝒙0{\bm{x}}\_{0} that is a one-hot vector with K𝐾K possible values, we define the forward process as follows. First, we have q​(𝒙t|𝒙0)𝑞conditionalsubscript𝒙𝑡subscript𝒙0q({\bm{x}}\_{t}|{\bm{x}}\_{0}) as the following categorical distribution:

|  |  |  |  |
| --- | --- | --- | --- |
|  | q​(𝒙t|𝒙0)=Cat​(αt​𝒙0+(1−αt)​𝟏K)𝑞conditionalsubscript𝒙𝑡subscript𝒙0Catsubscript𝛼𝑡subscript𝒙01subscript𝛼𝑡subscript1𝐾\displaystyle q({\bm{x}}\_{t}|{\bm{x}}\_{0})=\mathrm{Cat}(\alpha\_{t}{\bm{x}}\_{0}+(1-\alpha\_{t}){\bm{1}}\_{K}) |  | (17) |

where 𝟏K∈ℝKsubscript1𝐾superscriptℝ𝐾{\bm{1}}\_{K}\in\mathbb{R}^{K} is a vector with all entries being 1/K1𝐾1/K, and αtsubscript𝛼𝑡\alpha\_{t} decreasing from α0=1subscript𝛼01\alpha\_{0}=1 for t=0𝑡0t=0 to αT=0subscript𝛼𝑇0\alpha\_{T}=0 for t=T𝑡𝑇t=T.
Then we define q​(𝒙t−1|𝒙t,𝒙0)𝑞conditionalsubscript𝒙𝑡1

subscript𝒙𝑡subscript𝒙0q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}) as the following mixture distribution:

|  |  |  |  |
| --- | --- | --- | --- |
|  | q​(𝒙t−1|𝒙t,𝒙0)={Cat​(𝒙t)with probability ​σtCat​(𝒙0)with probability ​(αt−1−σt​αt)Cat​(𝟏K)with probability ​(1−αt−1)−(1−αt)​σt,𝑞conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0casesCatsubscript𝒙𝑡with probability subscript𝜎𝑡Catsubscript𝒙0with probability subscript𝛼𝑡1subscript𝜎𝑡subscript𝛼𝑡Catsubscript1𝐾with probability 1subscript𝛼𝑡11subscript𝛼𝑡subscript𝜎𝑡\displaystyle q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})=\begin{cases}\mathrm{Cat}({\bm{x}}\_{t})&\text{with probability }\sigma\_{t}\\ \mathrm{Cat}({\bm{x}}\_{0})&\text{with probability }(\alpha\_{t-1}-\sigma\_{t}\alpha\_{t})\\ \mathrm{Cat}({\bm{1}}\_{K})&\text{with probability }(1-\alpha\_{t-1})-(1-\alpha\_{t})\sigma\_{t}\end{cases}, |  | (18) |

or equivalently:

|  |  |  |  |
| --- | --- | --- | --- |
|  | q​(𝒙t−1|𝒙t,𝒙0)=Cat​(σt​𝒙t+(αt−1−σt​αt)​𝒙0+((1−αt−1)−(1−αt)​σt)​𝟏K),𝑞conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0Catsubscript𝜎𝑡subscript𝒙𝑡subscript𝛼𝑡1subscript𝜎𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡11subscript𝛼𝑡subscript𝜎𝑡subscript1𝐾\displaystyle q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})=\mathrm{Cat}\left(\sigma\_{t}{\bm{x}}\_{t}+(\alpha\_{t-1}-\sigma\_{t}\alpha\_{t}){\bm{x}}\_{0}+((1-\alpha\_{t-1})-(1-\alpha\_{t})\sigma\_{t}){\bm{1}}\_{K}\right), |  | (19) |

which is consistent with how we have defined q​(𝒙t|𝒙0)𝑞conditionalsubscript𝒙𝑡subscript𝒙0q({\bm{x}}\_{t}|{\bm{x}}\_{0}).

Similarly, we can define our reverse process pθ​(𝒙t−1|𝒙t)subscript𝑝𝜃conditionalsubscript𝒙𝑡1subscript𝒙𝑡p\_{\theta}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}) as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ​(𝒙t−1|𝒙t)=Cat​(σt​𝒙t+(αt−1−σt​αt)​fθ(t)​(𝒙t)+((1−αt−1)−(1−αt)​σt)​𝟏K),subscript𝑝𝜃conditionalsubscript𝒙𝑡1subscript𝒙𝑡Catsubscript𝜎𝑡subscript𝒙𝑡subscript𝛼𝑡1subscript𝜎𝑡subscript𝛼𝑡superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡1subscript𝛼𝑡11subscript𝛼𝑡subscript𝜎𝑡subscript1𝐾\displaystyle p\_{\theta}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})=\mathrm{Cat}\left(\sigma\_{t}{\bm{x}}\_{t}+(\alpha\_{t-1}-\sigma\_{t}\alpha\_{t})f\_{\theta}^{(t)}({\bm{x}}\_{t})+((1-\alpha\_{t-1})-(1-\alpha\_{t})\sigma\_{t}){\bm{1}}\_{K}\right), |  | (20) |

where fθ(t)​(𝒙t)superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡f\_{\theta}^{(t)}({\bm{x}}\_{t}) maps 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} to a K𝐾K-dimensional vector. As (1−αt−1)−(1−αt)​σt→0→1subscript𝛼𝑡11subscript𝛼𝑡subscript𝜎𝑡0(1-\alpha\_{t-1})-(1-\alpha\_{t})\sigma\_{t}\to 0, the sampling process will become less stochastic, in the sense that it will either choose 𝒙tsubscript𝒙𝑡{\bm{x}}\_{t} or the predicted 𝒙0subscript𝒙0{\bm{x}}\_{0} with high probability.
The KL divergence

|  |  |  |  |
| --- | --- | --- | --- |
|  | DKL(q(𝒙t−1|𝒙t,𝒙0)∥pθ(𝒙t−1|𝒙t))\displaystyle D\_{\mathrm{KL}}(q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})\|p\_{\theta}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})) |  | (21) |

is well-defined, and is simply the KL divergence between two categoricals. Therefore, the resulting variational objective function should be easy to optimize as well. Moreover, as KL divergence is convex, we have this upper bound (which is tight when the right hand side goes to zero):

|  |  |  |
| --- | --- | --- |
|  | DKL(q(𝒙t−1|𝒙t,𝒙0)∥pθ(𝒙t−1|𝒙t))≤(αt−1−σtαt)DKL(Cat(𝒙0)∥Cat(fθ(t)(𝒙t))).\displaystyle D\_{\mathrm{KL}}(q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})\|p\_{\theta}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}))\leq(\alpha\_{t-1}-\sigma\_{t}\alpha\_{t})D\_{\mathrm{KL}}(\mathrm{Cat}({\bm{x}}\_{0})\|\mathrm{Cat}(f\_{\theta}^{(t)}({\bm{x}}\_{t}))). |  |

The right hand side is simply a multi-class classification loss (up to constants), so we can arrive at similar arguments regarding how changes in σtsubscript𝜎𝑡\sigma\_{t} do not affect the objective (up to re-weighting).

## Appendix B Proofs

###### Lemma 1.

For qσ​(𝐱1:T|𝐱0)subscript𝑞𝜎conditionalsubscript𝐱:1𝑇subscript𝐱0q\_{\sigma}({\bm{x}}\_{1:T}|{\bm{x}}\_{0}) defined in Eq. ([6](#S3.E6 "In 3.1 Non-Markovian forward processes ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")) and qσ​(𝐱t−1|𝐱t,𝐱0)subscript𝑞𝜎conditionalsubscript𝐱𝑡1

subscript𝐱𝑡subscript𝐱0q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}) defined in Eq. ([7](#S3.E7 "In 3.1 Non-Markovian forward processes ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")), we have:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙t|𝒙0)=𝒩​(αt​𝒙0,(1−αt)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡𝑰\displaystyle q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0},(1-\alpha\_{t}){\bm{I}}) |  | (22) |

###### Proof.

Assume for any t≤T𝑡𝑇t\leq T, qσ​(𝒙t|𝒙0)=𝒩​(αt​𝒙0,(1−αt)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡𝑰q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0},(1-\alpha\_{t}){\bm{I}}) holds, if:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙t−1|𝒙0)=𝒩​(αt−1​𝒙0,(1−αt−1)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑡1subscript𝒙0𝒩subscript𝛼𝑡1subscript𝒙01subscript𝛼𝑡1𝑰\displaystyle q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t-1}}{\bm{x}}\_{0},(1-\alpha\_{t-1}){\bm{I}}) |  | (23) |

then we can prove the statement with an induction argument for t𝑡t from T𝑇T to 111, since the base case (t=T𝑡𝑇t=T) already holds.

First, we have that

|  |  |  |
| --- | --- | --- |
|  | qσ​(𝒙t−1|𝒙0):=∫𝒙tqσ​(𝒙t|𝒙0)​qσ​(𝒙t−1|𝒙t,𝒙0)​d𝒙tassignsubscript𝑞𝜎conditionalsubscript𝒙𝑡1subscript𝒙0subscriptsubscript𝒙𝑡subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0differential-dsubscript𝒙𝑡q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{0}):=\int\_{{\bm{x}}\_{t}}q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0})q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})\mathrm{d}{\bm{x}}\_{t} |  |

and

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙t|𝒙0)=𝒩​(αt​𝒙0,(1−αt)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡𝑰\displaystyle q\_{\sigma}({\bm{x}}\_{t}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0},(1-\alpha\_{t}){\bm{I}}) |  | (24) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ​(𝒙t−1|𝒙t,𝒙0)=𝒩​(αt−1​𝒙0+1−αt−1−σt2⋅𝒙t−αt​𝒙01−αt,σt2​𝑰).subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡1subscript𝒙0⋅1subscript𝛼𝑡1subscriptsuperscript𝜎2𝑡subscript𝒙𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡superscriptsubscript𝜎𝑡2𝑰\displaystyle q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})={\mathcal{N}}\left(\sqrt{\alpha\_{t-1}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t-1}-\sigma^{2}\_{t}}\cdot{\frac{{\bm{x}}\_{t}-\sqrt{\alpha\_{t}}{\bm{x}}\_{0}}{\sqrt{1-\alpha\_{t}}}},\sigma\_{t}^{2}{\bm{I}}\right). |  | (25) |

From Bishop ([2006](#bib.bib4)) (2.115), we have that qσ​(𝒙t−1|𝒙0)subscript𝑞𝜎conditionalsubscript𝒙𝑡1subscript𝒙0q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{0}) is Gaussian, denoted as 𝒩​(μt−1,Σt−1)𝒩subscript𝜇𝑡1subscriptΣ𝑡1{\mathcal{N}}(\mu\_{t-1},\Sigma\_{t-1}) where

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | μt−1subscript𝜇𝑡1\displaystyle\mu\_{t-1} | =αt−1​𝒙0+1−αt−1−σt2⋅αt​𝒙0−αt​𝒙01−αtabsentsubscript𝛼𝑡1subscript𝒙0⋅1subscript𝛼𝑡1subscriptsuperscript𝜎2𝑡subscript𝛼𝑡subscript𝒙0subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡\displaystyle=\sqrt{\alpha\_{t-1}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t-1}-\sigma^{2}\_{t}}\cdot{\frac{\sqrt{\alpha\_{t}}{\bm{x}}\_{0}-\sqrt{\alpha\_{t}}{\bm{x}}\_{0}}{\sqrt{1-\alpha\_{t}}}} |  | (26) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =αt−1​𝒙0absentsubscript𝛼𝑡1subscript𝒙0\displaystyle=\sqrt{\alpha\_{t-1}}{\bm{x}}\_{0} |  | (27) |

and

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Σt−1subscriptΣ𝑡1\displaystyle\Sigma\_{t-1} | =σt2​𝑰+1−αt−1−σt21−αt​(1−αt)​𝑰=(1−αt−1)​𝑰absentsuperscriptsubscript𝜎𝑡2𝑰1subscript𝛼𝑡1subscriptsuperscript𝜎2𝑡1subscript𝛼𝑡1subscript𝛼𝑡𝑰1subscript𝛼𝑡1𝑰\displaystyle=\sigma\_{t}^{2}{\bm{I}}+\frac{1-\alpha\_{t-1}-\sigma^{2}\_{t}}{1-\alpha\_{t}}(1-\alpha\_{t}){\bm{I}}=(1-\alpha\_{t-1}){\bm{I}} |  | (28) |

Therefore, qσ​(𝒙t−1|𝒙0)=𝒩​(αt−1​𝒙0,(1−αt−1)​𝑰)subscript𝑞𝜎conditionalsubscript𝒙𝑡1subscript𝒙0𝒩subscript𝛼𝑡1subscript𝒙01subscript𝛼𝑡1𝑰q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t-1}}{\bm{x}}\_{0},(1-\alpha\_{t-1}){\bm{I}}), which allows us to apply the induction argument.
∎

See [1](#Thmtheorem1 "Theorem 1. ‣ 3.2 Generative process and unified variational inference objective ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")

###### Proof.

From the definition of Jσsubscript𝐽𝜎J\_{\sigma}:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Jσ​(ϵθ)subscript𝐽𝜎subscriptitalic-ϵ𝜃\displaystyle J\_{\sigma}(\epsilon\_{\theta}) | :=𝔼𝒙0:T∼q​(𝒙0:T)​[log⁡qσ​(𝒙T|𝒙0)+∑t=2Tlog⁡qσ​(𝒙t−1|𝒙t,𝒙0)−∑t=1Tlog⁡pθ(t)​(𝒙t−1|𝒙t)]assignabsentsubscript𝔼similar-tosubscript𝒙:0𝑇𝑞subscript𝒙:0𝑇delimited-[]subscript𝑞𝜎conditionalsubscript𝒙𝑇subscript𝒙0superscriptsubscript𝑡2𝑇subscript𝑞𝜎conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0superscriptsubscript𝑡1𝑇superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡\displaystyle:={\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q({\bm{x}}\_{0:T})}\left[\log q\_{\sigma}({\bm{x}}\_{T}|{\bm{x}}\_{0})+\sum\_{t=2}^{T}\log q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})-\sum\_{t=1}^{T}\log p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})\right] |  | (29) |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | ≡𝔼𝒙0:T∼q​(𝒙0:T)[∑t=2TDKL(qσ(𝒙t−1|𝒙t,𝒙0))∥pθ(t)(𝒙t−1|𝒙t))−logpθ(1)(𝒙0|𝒙1)]\displaystyle\equiv{\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q({\bm{x}}\_{0:T})}\left[\sum\_{t=2}^{T}D\_{\mathrm{KL}}(q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}))\|p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}))-\log p\_{\theta}^{(1)}({\bm{x}}\_{0}|{\bm{x}}\_{1})\right] |  |

where we use ≡\equiv to denote ``equal up to a value that does not depend on ϵθsubscriptitalic-ϵ𝜃\epsilon\_{\theta} (but may depend on qσsubscript𝑞𝜎q\_{\sigma})''. For t>1𝑡1t>1:

|  |  |  |  |
| --- | --- | --- | --- |
|  |  | 𝔼𝒙0,𝒙t∼q​(𝒙0,𝒙t)[DKL(qσ(𝒙t−1|𝒙t,𝒙0))∥pθ(t)(𝒙t−1|𝒙t))]\displaystyle{\mathbb{E}}\_{{\bm{x}}\_{0},{\bm{x}}\_{t}\sim q({\bm{x}}\_{0},{\bm{x}}\_{t})}[D\_{\mathrm{KL}}(q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}))\|p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}))] |  |
|  |  |  |  |
| --- | --- | --- | --- |
|  | =\displaystyle= | 𝔼𝒙0,𝒙t∼q​(𝒙0,𝒙t)[DKL(qσ(𝒙t−1|𝒙t,𝒙0))∥qσ(𝒙t−1|𝒙t,fθ(t)(𝒙t)))]\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0},{\bm{x}}\_{t}\sim q({\bm{x}}\_{0},{\bm{x}}\_{t})}[D\_{\mathrm{KL}}(q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}))\|q\_{\sigma}({\bm{x}}\_{t-1}|{\bm{x}}\_{t},f\_{\theta}^{(t)}({\bm{x}}\_{t})))] |  |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | ≡\displaystyle\equiv | 𝔼𝒙0,𝒙t∼q​(𝒙0,𝒙t)​[∥𝒙0−fθ(t)​(𝒙t)∥222​σt2]subscript𝔼similar-to  subscript𝒙0subscript𝒙𝑡 𝑞subscript𝒙0subscript𝒙𝑡delimited-[]superscriptsubscriptdelimited-∥∥subscript𝒙0superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡222superscriptsubscript𝜎𝑡2\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0},{\bm{x}}\_{t}\sim q({\bm{x}}\_{0},{\bm{x}}\_{t})}\left[\frac{{\lVert{{\bm{x}}\_{0}-f\_{\theta}^{(t)}({\bm{x}}\_{t})}\rVert}\_{2}^{2}}{2\sigma\_{t}^{2}}\right] |  | (30) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | =\displaystyle= | 𝔼𝒙0∼q​(𝒙0),ϵ∼𝒩​(𝟎,𝑰),𝒙t=αt​𝒙0+1−αt​ϵ​[∥(𝒙t−1−αt​ϵ)αt−(𝒙t−1−αt​ϵθ(t)​(𝒙t))αt∥222​σt2]subscript𝔼formulae-sequencesimilar-tosubscript𝒙0𝑞subscript𝒙0formulae-sequencesimilar-toitalic-ϵ𝒩0𝑰subscript𝒙𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡italic-ϵdelimited-[]superscriptsubscriptdelimited-∥∥subscript𝒙𝑡1subscript𝛼𝑡italic-ϵsubscript𝛼𝑡subscript𝒙𝑡1subscript𝛼𝑡superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡subscript𝛼𝑡222superscriptsubscript𝜎𝑡2\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0}\sim q({\bm{x}}\_{0}),\epsilon\sim{\mathcal{N}}({\bm{0}},{\bm{I}}),{\bm{x}}\_{t}=\sqrt{\alpha\_{t}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t}}\epsilon}\left[\frac{{\lVert{\frac{{({\bm{x}}\_{t}-\sqrt{1-\alpha\_{t}}\epsilon)}}{\sqrt{\alpha\_{t}}}-\frac{({\bm{x}}\_{t}-\sqrt{1-\alpha\_{t}}\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}))}{\sqrt{\alpha\_{t}}}}\rVert}\_{2}^{2}}{2\sigma\_{t}^{2}}\right] |  | (31) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | =\displaystyle= | 𝔼𝒙0∼q​(𝒙0),ϵ∼𝒩​(𝟎,𝑰),𝒙t=αt​𝒙0+1−αt​ϵ​[∥ϵ−ϵθ(t)​(𝒙t)∥222​d​σt2​αt]subscript𝔼formulae-sequencesimilar-tosubscript𝒙0𝑞subscript𝒙0formulae-sequencesimilar-toitalic-ϵ𝒩0𝑰subscript𝒙𝑡subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡italic-ϵdelimited-[]superscriptsubscriptdelimited-∥∥italic-ϵsuperscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡222𝑑superscriptsubscript𝜎𝑡2subscript𝛼𝑡\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0}\sim q({\bm{x}}\_{0}),\epsilon\sim{\mathcal{N}}({\bm{0}},{\bm{I}}),{\bm{x}}\_{t}=\sqrt{\alpha\_{t}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t}}\epsilon}\left[\frac{{\lVert{\epsilon-\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t})}\rVert}\_{2}^{2}}{2d\sigma\_{t}^{2}\alpha\_{t}}\right] |  | (32) |

where d𝑑d is the dimension of 𝒙0subscript𝒙0{\bm{x}}\_{0}. For t=1𝑡1t=1:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | 𝔼𝒙0,𝒙1∼q​(𝒙0,𝒙1)​[−log⁡pθ(1)​(𝒙0|𝒙1)]≡𝔼𝒙0,𝒙1∼q​(𝒙0,𝒙1)​[∥𝒙0−fθ(t)​(𝒙1)∥222​σ12]subscript𝔼similar-to  subscript𝒙0subscript𝒙1 𝑞subscript𝒙0subscript𝒙1delimited-[]superscriptsubscript𝑝𝜃1conditionalsubscript𝒙0subscript𝒙1subscript𝔼similar-to  subscript𝒙0subscript𝒙1 𝑞subscript𝒙0subscript𝒙1delimited-[]superscriptsubscriptdelimited-∥∥subscript𝒙0superscriptsubscript𝑓𝜃𝑡subscript𝒙1222superscriptsubscript𝜎12\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0},{\bm{x}}\_{1}\sim q({\bm{x}}\_{0},{\bm{x}}\_{1})}\left[-\log p\_{\theta}^{(1)}({\bm{x}}\_{0}|{\bm{x}}\_{1})\right]\equiv{\mathbb{E}}\_{{\bm{x}}\_{0},{\bm{x}}\_{1}\sim q({\bm{x}}\_{0},{\bm{x}}\_{1})}\left[\frac{{\lVert{{\bm{x}}\_{0}-f\_{\theta}^{(t)}({\bm{x}}\_{1})}\rVert}\_{2}^{2}}{2\sigma\_{1}^{2}}\right] |  | (33) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | =\displaystyle= | 𝔼𝒙0∼q​(𝒙0),ϵ∼𝒩​(𝟎,𝑰),𝒙1=α1​𝒙0+1−αt​ϵ​[∥ϵ−ϵθ(1)​(𝒙1)∥222​d​σ12​α1]subscript𝔼formulae-sequencesimilar-tosubscript𝒙0𝑞subscript𝒙0formulae-sequencesimilar-toitalic-ϵ𝒩0𝑰subscript𝒙1subscript𝛼1subscript𝒙01subscript𝛼𝑡italic-ϵdelimited-[]superscriptsubscriptdelimited-∥∥italic-ϵsuperscriptsubscriptitalic-ϵ𝜃1subscript𝒙1222𝑑superscriptsubscript𝜎12subscript𝛼1\displaystyle\ {\mathbb{E}}\_{{\bm{x}}\_{0}\sim q({\bm{x}}\_{0}),\epsilon\sim{\mathcal{N}}({\bm{0}},{\bm{I}}),{\bm{x}}\_{1}=\sqrt{\alpha\_{1}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t}}\epsilon}\left[\frac{{\lVert{\epsilon-\epsilon\_{\theta}^{(1)}({\bm{x}}\_{1})}\rVert}\_{2}^{2}}{2d\sigma\_{1}^{2}\alpha\_{1}}\right] |  | (34) |

Therefore, when γt=1/(2​d​σt2​αt)subscript𝛾𝑡12𝑑superscriptsubscript𝜎𝑡2subscript𝛼𝑡\gamma\_{t}=1/(2d\sigma\_{t}^{2}\alpha\_{t}) for all t∈{1,…,T}𝑡1…𝑇t\in\{1,\ldots,T\}, we have

|  |  |  |  |
| --- | --- | --- | --- |
|  | Jσ​(ϵθ)≡∑t=1T12​d​σt2​αt​𝔼​[∥ϵθ(t)​(𝒙t)−ϵt∥22]=Lγ​(ϵθ)subscript𝐽𝜎subscriptitalic-ϵ𝜃superscriptsubscript𝑡1𝑇12𝑑superscriptsubscript𝜎𝑡2subscript𝛼𝑡𝔼delimited-[]superscriptsubscriptdelimited-∥∥superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡subscriptitalic-ϵ𝑡22subscript𝐿𝛾subscriptitalic-ϵ𝜃\displaystyle J\_{\sigma}(\epsilon\_{\theta})\equiv\sum\_{t=1}^{T}\frac{1}{2d\sigma\_{t}^{2}\alpha\_{t}}{\mathbb{E}}\left[{\lVert{\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t})-\epsilon\_{t}}\rVert}\_{2}^{2}\right]=L\_{\gamma}(\epsilon\_{\theta}) |  | (35) |

for all ϵθsubscriptitalic-ϵ𝜃\epsilon\_{\theta}. From the definition of ``≡\equiv'', we have that Jσ=Lγ+Csubscript𝐽𝜎subscript𝐿𝛾𝐶J\_{\sigma}=L\_{\gamma}+C.
∎

See [1](#Thmproposition1 "Proposition 1. ‣ 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")

###### Proof.

In the context of the proof, we consider t𝑡t as a continous, independent ``time'' variable and 𝒙𝒙{\bm{x}} and α𝛼\alpha as functions of t𝑡t. First, let us consider a reparametrization between DDIM and the VE-SDE888Refer to (Song et al., [2020](#bib.bib36)) for more details of VE-SDE. by introducing the variables 𝒙¯¯𝒙\bar{{\bm{x}}} and σ𝜎\sigma:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙¯​(t)=𝒙¯​(0)+σ​(t)​ϵ,ϵ∼𝒩​(0,𝑰),formulae-sequence¯𝒙𝑡¯𝒙0𝜎𝑡italic-ϵsimilar-toitalic-ϵ𝒩0𝑰\displaystyle\bar{{\bm{x}}}(t)=\bar{{\bm{x}}}(0)+\sigma(t)\epsilon,\quad\epsilon\sim{\mathcal{N}}(0,{\bm{I}}), |  | (36) |

for t∈[0,∞)𝑡0t\in[0,\infty) and an increasing continuous function σ:ℝ≥0→ℝ≥0:𝜎→subscriptℝabsent0subscriptℝabsent0\sigma:{\mathbb{R}}\_{\geq 0}\to{\mathbb{R}}\_{\geq 0} where σ​(0)=0𝜎00\sigma(0)=0.

We can then define α​(t)𝛼𝑡\alpha(t) and 𝒙​(t)𝒙𝑡{\bm{x}}(t) corresponding to DDIM case as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙¯​(t)=𝒙​(t)α​(t)¯𝒙𝑡𝒙𝑡𝛼𝑡\displaystyle\bar{{\bm{x}}}(t)=\frac{{\bm{x}}(t)}{\sqrt{\alpha(t)}} |  | (37) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | σ​(t)=1−α​(t)α​(t).𝜎𝑡1𝛼𝑡𝛼𝑡\displaystyle\sigma(t)=\sqrt{\frac{1-\alpha(t)}{\alpha(t)}}. |  | (38) |

This also means that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙​(t)=𝒙¯​(t)σ2​(t)+1𝒙𝑡¯𝒙𝑡superscript𝜎2𝑡1\displaystyle{\bm{x}}(t)=\frac{\bar{{\bm{x}}}(t)}{\sqrt{\sigma^{2}(t)+1}} |  | (39) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | α​(t)=11+σ2​(t),𝛼𝑡11superscript𝜎2𝑡\displaystyle\alpha(t)=\frac{1}{1+\sigma^{2}(t)}, |  | (40) |

which establishes an bijection between (𝒙,α)𝒙𝛼({\bm{x}},\alpha) and (𝒙¯,σ)¯𝒙𝜎(\bar{{\bm{x}}},\sigma). From Equation ([4](#S2.E4 "In 2 Background ‣ Denoising Diffusion Implicit Models")) we have (note that α​(0)=1𝛼01\alpha(0)=1):

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙​(t)α​(t)=𝒙​(0)α​(0)+1−α​(t)α​(t)​ϵ,ϵ∼𝒩​(0,𝑰)formulae-sequence𝒙𝑡𝛼𝑡𝒙0𝛼01𝛼𝑡𝛼𝑡italic-ϵsimilar-toitalic-ϵ𝒩0𝑰\displaystyle\frac{{\bm{x}}(t)}{\sqrt{\alpha(t)}}=\frac{{\bm{x}}(0)}{\sqrt{\alpha(0)}}+\sqrt{\frac{1-\alpha(t)}{\alpha(t)}}\epsilon,\quad\epsilon\sim{\mathcal{N}}(0,{\bm{I}}) |  | (41) |

which can be reparametrized into a form that is consistent with VE-SDE:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙¯​(t)=𝒙¯​(0)+σ​(t)​ϵ.¯𝒙𝑡¯𝒙0𝜎𝑡italic-ϵ\displaystyle\bar{{\bm{x}}}(t)=\bar{{\bm{x}}}(0)+\sigma(t)\epsilon. |  | (42) |

Now, we derive the ODE forms for both DDIM and VE-SDE and show that they are equivalent.

#### ODE form for DDIM

We repeat Equation ([13](#S4.E13 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")) here:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙t−Δ​tαt−Δ​t=𝒙tαt+(1−αt−Δ​tαt−Δ​t−1−αtαt)​ϵθ(t)​(𝒙t),subscript𝒙𝑡Δ𝑡subscript𝛼𝑡Δ𝑡subscript𝒙𝑡subscript𝛼𝑡1subscript𝛼𝑡Δ𝑡subscript𝛼𝑡Δ𝑡1subscript𝛼𝑡subscript𝛼𝑡superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡\displaystyle\frac{{\bm{x}}\_{t-\Delta t}}{\sqrt{\alpha\_{t-\Delta t}}}=\frac{{\bm{x}}\_{t}}{\sqrt{\alpha\_{t}}}+\left(\sqrt{\frac{1-\alpha\_{t-\Delta t}}{\alpha\_{t-\Delta t}}}-\sqrt{\frac{1-\alpha\_{t}}{\alpha\_{t}}}\right)\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}), |  | (43) |

which is equivalent to:

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙¯​(t−Δ​t)=𝒙¯​(t)+(σ​(t−Δ​t)−σ​(t))⋅ϵθ(t)​(𝒙​(t))¯𝒙𝑡Δ𝑡¯𝒙𝑡⋅𝜎𝑡Δ𝑡𝜎𝑡superscriptsubscriptitalic-ϵ𝜃𝑡𝒙𝑡\displaystyle\bar{{\bm{x}}}(t-\Delta t)=\bar{{\bm{x}}}(t)+(\sigma(t-\Delta t)-\sigma(t))\cdot\epsilon\_{\theta}^{(t)}({\bm{x}}(t)) |  | (44) |

Divide both sides by (−Δ​t)Δ𝑡(-\Delta t) and as Δ​t→0→Δ𝑡0\Delta t\to 0, we have:

|  |  |  |  |
| --- | --- | --- | --- |
|  | d​𝒙¯​(t)d​t=d​σ​(t)d​t​ϵθ(t)​(𝒙¯​(t)σ2​(t)+1),d¯𝒙𝑡d𝑡d𝜎𝑡d𝑡superscriptsubscriptitalic-ϵ𝜃𝑡¯𝒙𝑡superscript𝜎2𝑡1\displaystyle\frac{\mathrm{d}\bar{{\bm{x}}}(t)}{\mathrm{d}t}=\frac{\mathrm{d}\sigma(t)}{\mathrm{d}t}\epsilon\_{\theta}^{(t)}\left(\frac{\bar{{\bm{x}}}(t)}{\sqrt{\sigma^{2}(t)+1}}\right), |  | (45) |

which is exactly what we have in Equation ([14](#S4.E14 "In 4.3 Relevance to Neural ODEs ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")).

We note that for the optimal model, ϵθ(t)superscriptsubscriptitalic-ϵ𝜃𝑡\epsilon\_{\theta}^{(t)} is a minimizer:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ϵθ(t)=arg​minft⁡𝔼𝒙​(0)∼q​(𝒙),ϵ∼𝒩​(0,𝑰)​[∥ft​(𝒙​(t))−ϵ∥22]superscriptsubscriptitalic-ϵ𝜃𝑡subscriptargminsubscript𝑓𝑡subscript𝔼formulae-sequencesimilar-to𝒙0𝑞𝒙similar-toitalic-ϵ𝒩0𝑰delimited-[]superscriptsubscriptdelimited-∥∥subscript𝑓𝑡𝒙𝑡italic-ϵ22\displaystyle\epsilon\_{\theta}^{(t)}=\operatorname\*{arg\,min}\_{f\_{t}}{\mathbb{E}}\_{{\bm{x}}(0)\sim q({\bm{x}}),\epsilon\sim{\mathcal{N}}(0,{\bm{I}})}[{\lVert{f\_{t}({\bm{x}}(t))-\epsilon}\rVert}\_{2}^{2}] |  | (46) |

where 𝒙​(t)=α​(t)​𝒙​(t)+1−α​(t)​ϵ𝒙𝑡𝛼𝑡𝒙𝑡1𝛼𝑡italic-ϵ{\bm{x}}(t)=\sqrt{\alpha(t)}{\bm{x}}(t)+\sqrt{1-\alpha(t)}\epsilon.

#### ODE form for VE-SDE

Define pt​(𝒙¯)subscript𝑝𝑡¯𝒙p\_{t}(\bar{{\bm{x}}}) as the data distribution perturbed with σ2​(t)superscript𝜎2𝑡\sigma^{2}(t) variance Gaussian noise. The probability flow for VE-SDE is defined as Song et al. ([2020](#bib.bib36)):

|  |  |  |  |
| --- | --- | --- | --- |
|  | d​𝒙¯=−12​g​(t)2​∇𝒙¯log⁡pt​(𝒙¯)​d​td¯𝒙12𝑔superscript𝑡2subscript∇¯𝒙subscript𝑝𝑡¯𝒙d𝑡\displaystyle\mathrm{d}\bar{{\bm{x}}}=-\frac{1}{2}g(t)^{2}\nabla\_{\bar{{\bm{x}}}}\log p\_{t}(\bar{{\bm{x}}})\mathrm{d}t |  | (47) |

where g​(t)=d​σ2​(t)d​t𝑔𝑡dsuperscript𝜎2𝑡d𝑡g(t)=\sqrt{\frac{\mathrm{d}\sigma^{2}(t)}{\mathrm{d}t}} is the diffusion coefficient, and ∇𝒙¯log⁡pt​(𝒙¯)subscript∇¯𝒙subscript𝑝𝑡¯𝒙\nabla\_{\bar{{\bm{x}}}}\log p\_{t}(\bar{{\bm{x}}}) is the score of ptsubscript𝑝𝑡p\_{t}.

The σ​(t)𝜎𝑡\sigma(t)-perturbed score function ∇𝒙¯log⁡pt​(𝒙¯)subscript∇¯𝒙subscript𝑝𝑡¯𝒙\nabla\_{\bar{{\bm{x}}}}\log p\_{t}(\bar{{\bm{x}}}) is also a minimizer (from denoising score matching (Vincent, [2011](#bib.bib39))):

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝒙¯log⁡pt=arg​mingt⁡𝔼𝒙​(0)∼q​(𝒙),ϵ∼𝒩​(0,𝑰)​[∥gt​(𝒙¯)+ϵ/σ​(t)∥22]subscript∇¯𝒙subscript𝑝𝑡subscriptargminsubscript𝑔𝑡subscript𝔼formulae-sequencesimilar-to𝒙0𝑞𝒙similar-toitalic-ϵ𝒩0𝑰delimited-[]superscriptsubscriptdelimited-∥∥subscript𝑔𝑡¯𝒙italic-ϵ𝜎𝑡22\displaystyle\nabla\_{\bar{{\bm{x}}}}\log p\_{t}=\operatorname\*{arg\,min}\_{g\_{t}}{\mathbb{E}}\_{{\bm{x}}(0)\sim q({\bm{x}}),\epsilon\sim{\mathcal{N}}(0,{\bm{I}})}[{\lVert{g\_{t}(\bar{{\bm{x}}})+\epsilon/\sigma(t)}\rVert}\_{2}^{2}] |  | (48) |

where 𝒙¯​(t)=𝒙¯​(t)+σ​(t)​ϵ¯𝒙𝑡¯𝒙𝑡𝜎𝑡italic-ϵ\bar{{\bm{x}}}(t)=\bar{{\bm{x}}}(t)+\sigma(t)\epsilon.

Since there is an equivalence between 𝒙​(t)𝒙𝑡{\bm{x}}(t) and 𝒙¯​(t)¯𝒙𝑡\bar{{\bm{x}}}(t), we have the following relationship:

|  |  |  |  |
| --- | --- | --- | --- |
|  | ∇𝒙¯log⁡pt​(𝒙¯)=−ϵθ(t)​(𝒙¯​(t)σ2​(t)+1)σ​(t)subscript∇¯𝒙subscript𝑝𝑡¯𝒙superscriptsubscriptitalic-ϵ𝜃𝑡¯𝒙𝑡superscript𝜎2𝑡1𝜎𝑡\displaystyle\nabla\_{\bar{{\bm{x}}}}\log p\_{t}(\bar{{\bm{x}}})=-\frac{\epsilon\_{\theta}^{(t)}\left(\frac{\bar{{\bm{x}}}(t)}{\sqrt{\sigma^{2}(t)+1}}\right)}{\sigma(t)} |  | (49) |

from Equation ([46](#A2.E46 "In ODE form for DDIM ‣ Appendix B Proofs ‣ Denoising Diffusion Implicit Models")) and Equation ([48](#A2.E48 "In ODE form for VE-SDE ‣ Appendix B Proofs ‣ Denoising Diffusion Implicit Models")). Plug Equation ([49](#A2.E49 "In ODE form for VE-SDE ‣ Appendix B Proofs ‣ Denoising Diffusion Implicit Models")) and definition of g​(t)𝑔𝑡g(t) in Equation ([47](#A2.E47 "In ODE form for VE-SDE ‣ Appendix B Proofs ‣ Denoising Diffusion Implicit Models")), we have:

|  |  |  |  |
| --- | --- | --- | --- |
|  | d​𝒙¯​(t)=12​d​σ2​(t)d​t​ϵθ(t)​(𝒙¯​(t)σ2​(t)+1)σ​(t)​d​t,d¯𝒙𝑡12dsuperscript𝜎2𝑡d𝑡superscriptsubscriptitalic-ϵ𝜃𝑡¯𝒙𝑡superscript𝜎2𝑡1𝜎𝑡d𝑡\displaystyle\mathrm{d}\bar{{\bm{x}}}(t)=\frac{1}{2}\frac{\mathrm{d}\sigma^{2}(t)}{\mathrm{d}t}\frac{\epsilon\_{\theta}^{(t)}\left(\frac{\bar{{\bm{x}}}(t)}{\sqrt{\sigma^{2}(t)+1}}\right)}{\sigma(t)}\mathrm{d}t, |  | (50) |

and we have the following by rearranging terms:

|  |  |  |  |
| --- | --- | --- | --- |
|  | d​𝒙¯​(t)d​t=d​σ​(t)d​t​ϵθ(t)​(𝒙¯​(t)σ2​(t)+1)d¯𝒙𝑡d𝑡d𝜎𝑡d𝑡superscriptsubscriptitalic-ϵ𝜃𝑡¯𝒙𝑡superscript𝜎2𝑡1\displaystyle\frac{\mathrm{d}\bar{{\bm{x}}}(t)}{\mathrm{d}t}=\frac{\mathrm{d}\sigma(t)}{\mathrm{d}t}\epsilon\_{\theta}^{(t)}\left(\frac{\bar{{\bm{x}}}(t)}{\sqrt{\sigma^{2}(t)+1}}\right) |  | (51) |

which is equivalent to Equation ([45](#A2.E45 "In ODE form for DDIM ‣ Appendix B Proofs ‣ Denoising Diffusion Implicit Models")). In both cases the initial conditions are 𝒙¯​(T)∼𝒩​(𝟎,σ2​(T)​𝑰)similar-to¯𝒙𝑇𝒩0superscript𝜎2𝑇𝑰\bar{{\bm{x}}}(T)\sim{\mathcal{N}}({\bm{0}},\sigma^{2}(T){\bm{I}}), so the resulting ODEs are identical.
∎

## Appendix C Additional Derivations

### C.1 Accelerated sampling processes

In the accelerated case, we can consider the inference process to be factored as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ,τ​(𝒙1:T|𝒙0)=qσ,τ​(𝒙τS|𝒙0)​∏i=1Sqσ,τ​(𝒙τi−1|𝒙τi,𝒙0)​∏t∈τ¯qσ,τ​(𝒙t|𝒙0)subscript𝑞  𝜎𝜏conditionalsubscript𝒙:1𝑇subscript𝒙0subscript𝑞  𝜎𝜏conditionalsubscript𝒙subscript𝜏𝑆subscript𝒙0superscriptsubscriptproduct𝑖1𝑆subscript𝑞  𝜎𝜏conditionalsubscript𝒙subscript𝜏𝑖1  subscript𝒙subscript𝜏𝑖subscript𝒙0subscriptproduct𝑡¯𝜏subscript𝑞  𝜎𝜏conditionalsubscript𝒙𝑡subscript𝒙0\displaystyle q\_{\sigma,\tau}({\bm{x}}\_{1:T}|{\bm{x}}\_{0})=q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{S}}|{\bm{x}}\_{0})\prod\_{i=1}^{S}q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}},{\bm{x}}\_{0})\prod\_{t\in\bar{\tau}}q\_{\sigma,\tau}({\bm{x}}\_{t}|{\bm{x}}\_{0}) |  | (52) |

where τ𝜏\tau is a sub-sequence of [1,…,T]

1…𝑇[1,\ldots,T] of length S𝑆S with τS=Tsubscript𝜏𝑆𝑇\tau\_{S}=T, and let τ¯:={1,…,T}∖τassign¯𝜏1…𝑇𝜏\bar{\tau}:=\{1,\ldots,T\}\setminus\tau be its complement. Intuitively, the graphical model of {𝒙τi}i=1Ssuperscriptsubscriptsubscript𝒙subscript𝜏𝑖𝑖1𝑆\{{\bm{x}}\_{\tau\_{i}}\}\_{i=1}^{S} and 𝒙0subscript𝒙0{\bm{x}}\_{0} form a chain, whereas the graphical model of {𝒙t}t∈τ¯subscriptsubscript𝒙𝑡𝑡¯𝜏\{{\bm{x}}\_{t}\}\_{t\in\bar{\tau}} and 𝒙0subscript𝒙0{\bm{x}}\_{0} forms a star graph. We define:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ,τ​(𝒙t|𝒙0)=𝒩​(αt​𝒙0,(1−αt)​𝑰)∀t∈τ¯∪{T}formulae-sequencesubscript𝑞  𝜎𝜏conditionalsubscript𝒙𝑡subscript𝒙0𝒩subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡𝑰for-all𝑡¯𝜏𝑇\displaystyle q\_{\sigma,\tau}({\bm{x}}\_{t}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0},(1-\alpha\_{t}){\bm{I}})\quad\forall t\in\bar{\tau}\cup\{T\} |  | (53) |
|  |  |  |
| --- | --- | --- |
|  | qσ,τ​(𝒙τi−1|𝒙τi,𝒙0)=𝒩​(ατi−1​𝒙0+1−ατi−1−στi2⋅𝒙τi−ατi​𝒙01−ατi,στi2​𝑰)​∀i∈[S]subscript𝑞  𝜎𝜏conditionalsubscript𝒙subscript𝜏𝑖1  subscript𝒙subscript𝜏𝑖subscript𝒙0𝒩subscript𝛼subscript𝜏𝑖1subscript𝒙0⋅1subscript𝛼subscript𝜏𝑖1subscriptsuperscript𝜎2subscript𝜏𝑖subscript𝒙subscript𝜏𝑖subscript𝛼subscript𝜏𝑖subscript𝒙01subscript𝛼subscript𝜏𝑖superscriptsubscript𝜎subscript𝜏𝑖2𝑰for-all𝑖delimited-[]𝑆\displaystyle q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}},{\bm{x}}\_{0})={\mathcal{N}}\left(\sqrt{\alpha\_{\tau\_{i-1}}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{\tau\_{i-1}}-\sigma^{2}\_{\tau\_{i}}}\cdot{\frac{{\bm{x}}\_{\tau\_{i}}-\sqrt{\alpha\_{\tau\_{i}}}{\bm{x}}\_{0}}{\sqrt{1-\alpha\_{\tau\_{i}}}}},\sigma\_{{\tau\_{i}}}^{2}{\bm{I}}\right)\ \forall i\in[S] |  |

where the coefficients are chosen such that:

|  |  |  |  |
| --- | --- | --- | --- |
|  | qσ,τ​(𝒙τi|𝒙0)=𝒩​(ατi​𝒙0,(1−ατi)​𝑰)∀i∈[S]formulae-sequencesubscript𝑞  𝜎𝜏conditionalsubscript𝒙subscript𝜏𝑖subscript𝒙0𝒩subscript𝛼subscript𝜏𝑖subscript𝒙01subscript𝛼subscript𝜏𝑖𝑰for-all𝑖delimited-[]𝑆\displaystyle q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{i}}|{\bm{x}}\_{0})={\mathcal{N}}(\sqrt{\alpha\_{\tau\_{i}}}{\bm{x}}\_{0},(1-\alpha\_{\tau\_{i}}){\bm{I}})\quad\forall i\in[S] |  | (54) |

i.e., the ``marginals'' match.

The corresponding ``generative process'' is defined as:

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ​(𝒙0:T):=pθ​(𝒙T)​∏i=1Spθ(τi)​(𝒙τi−1|𝒙τi)⏟use to produce samples×∏t∈τ¯pθ(t)​(𝒙0|𝒙t)⏟in variational objectiveassignsubscript𝑝𝜃subscript𝒙:0𝑇subscript⏟subscript𝑝𝜃subscript𝒙𝑇superscriptsubscriptproduct𝑖1𝑆subscriptsuperscript𝑝subscript𝜏𝑖𝜃conditionalsubscript𝒙subscript𝜏𝑖1subscript𝒙subscript𝜏𝑖use to produce samplessubscript⏟subscriptproduct𝑡¯𝜏superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙0subscript𝒙𝑡in variational objective\displaystyle p\_{\theta}({\bm{x}}\_{0:T}):=\underbrace{p\_{\theta}({\bm{x}}\_{T})\prod\_{i=1}^{S}p^{(\tau\_{i})}\_{\theta}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}})}\_{\text{use to produce samples}}\times\underbrace{\prod\_{t\in\bar{\tau}}p\_{\theta}^{(t)}({\bm{x}}\_{0}|{\bm{x}}\_{t})}\_{\text{in variational objective}} |  | (55) |

where only part of the models are actually being used to produce samples. The conditionals are:

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ(τi)​(𝒙τi−1|𝒙τi)=qσ,τ​(𝒙τi−1|𝒙τi,fθ(τi)​(𝒙τi−1))if​i∈[S],i>1formulae-sequencesuperscriptsubscript𝑝𝜃subscript𝜏𝑖conditionalsubscript𝒙subscript𝜏𝑖1subscript𝒙subscript𝜏𝑖subscript𝑞  𝜎𝜏conditionalsubscript𝒙subscript𝜏𝑖1  subscript𝒙subscript𝜏𝑖superscriptsubscript𝑓𝜃subscript𝜏𝑖subscript𝒙subscript𝜏𝑖1formulae-sequenceif𝑖delimited-[]𝑆𝑖1\displaystyle p\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}})=q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}},f\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i-1}}))\quad\text{if}\ i\in[S],i>1 |  | (56) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ(t)​(𝒙0|𝒙t)=𝒩​(fθ(t)​(𝒙t),σt2​𝑰)otherwise,superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙0subscript𝒙𝑡  𝒩superscriptsubscript𝑓𝜃𝑡subscript𝒙𝑡superscriptsubscript𝜎𝑡2𝑰otherwise,\displaystyle p\_{\theta}^{(t)}({\bm{x}}\_{0}|{\bm{x}}\_{t})={\mathcal{N}}(f\_{\theta}^{(t)}({\bm{x}}\_{t}),\sigma\_{t}^{2}{\bm{I}})\quad\text{otherwise,} |  | (57) |

where we leverage qσ,τ​(𝒙τi−1|𝒙τi,𝒙0)subscript𝑞

𝜎𝜏conditionalsubscript𝒙subscript𝜏𝑖1

subscript𝒙subscript𝜏𝑖subscript𝒙0q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}},{\bm{x}}\_{0}) as part of the inference process (similar to what we have done in Section [3](#S3 "3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models")). The resulting variational objective becomes (define 𝒙τL+1=∅subscript𝒙subscript𝜏𝐿1{\bm{x}}\_{\tau\_{L+1}}=\varnothing for conciseness):

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | J​(ϵθ)𝐽subscriptitalic-ϵ𝜃\displaystyle J(\epsilon\_{\theta}) | =𝔼𝒙0:T∼qσ,τ​(𝒙0:T)​[log⁡qσ,τ​(𝒙1:T|𝒙0)−log⁡pθ​(𝒙0:T)]absentsubscript𝔼similar-tosubscript𝒙:0𝑇subscript𝑞  𝜎𝜏subscript𝒙:0𝑇delimited-[]subscript𝑞  𝜎𝜏conditionalsubscript𝒙:1𝑇subscript𝒙0subscript𝑝𝜃subscript𝒙:0𝑇\displaystyle={\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q\_{\sigma,\tau}({\bm{x}}\_{0:T})}[\log q\_{\sigma,\tau}({\bm{x}}\_{1:T}|{\bm{x}}\_{0})-\log p\_{\theta}({\bm{x}}\_{0:T})] |  | (58) |
|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  |  | =𝔼𝒙0:T∼qσ,τ​(𝒙0:T)[∑t∈τ¯DKL(qσ,τ(𝒙t|𝒙0)∥pθ(t)(𝒙0|𝒙t)\displaystyle={\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q\_{\sigma,\tau}({\bm{x}}\_{0:T})}\Bigg{[}\sum\_{t\in\bar{\tau}}D\_{\mathrm{KL}}(q\_{\sigma,\tau}({\bm{x}}\_{t}|{\bm{x}}\_{0})\|p\_{\theta}^{(t)}({\bm{x}}\_{0}|{\bm{x}}\_{t}) |  | (59) |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | +∑i=1LDKL(qσ,τ(𝒙τi−1|𝒙τi,𝒙0)∥pθ(τi)(𝒙τi−1|𝒙τi)))]\displaystyle\qquad\qquad\qquad\qquad+\sum\_{i=1}^{L}D\_{\mathrm{KL}}(q\_{\sigma,\tau}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}},{\bm{x}}\_{0})\|p\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i-1}}|{\bm{x}}\_{\tau\_{i}})))\Bigg{]} |  |

where each KL divergence is between two Gaussians with variance independent of θ𝜃\theta. A similar argument to the proof used in Theorem [1](#Thmtheorem1 "Theorem 1. ‣ 3.2 Generative process and unified variational inference objective ‣ 3 Variational Inference for non-Markovian Forward Processes ‣ Denoising Diffusion Implicit Models") can show that the variational objective J𝐽J can also be converted to an objective of the form Lγsubscript𝐿𝛾L\_{\gamma}.

### C.2 Derivation of denoising objectives for DDPMs

We note that in Ho et al. ([2020](#bib.bib15)), a diffusion hyperparameter  βtsubscript𝛽𝑡\beta\_{t}999In this section we use teal to color notations used in Ho et al. ([2020](#bib.bib15)). is first introduced, and then relevant variables αt:=1−βtassignsubscript𝛼𝑡1subscript𝛽𝑡\alpha\_{t}:=1-\beta\_{t} and α¯t=∏t=1Tαtsubscript¯𝛼𝑡superscriptsubscriptproduct𝑡1𝑇subscript𝛼𝑡\bar{\alpha}\_{t}=\prod\_{t=1}^{T}\alpha\_{t} are defined. In this paper, we have used the notation αtsubscript𝛼𝑡\alpha\_{t} to represent the variable  α¯tsubscript¯𝛼𝑡\bar{\alpha}\_{t} in Ho et al. ([2020](#bib.bib15)) for three reasons. First, it makes it more clear that we only need to choose one set of hyperparameters, reducing possible cross-references of the derived variables. Second, it allows us to introduce the generalization as well as the acceleration case easier, because the inference process is no longer motivated by a diffusion. Third, there exists an isomorphism between α1:Tsubscript𝛼:1𝑇\alpha\_{1:T} and 1,…,T

1…𝑇1,\ldots,T, which is not the case for  βtsubscript𝛽𝑡\beta\_{t}.

In this section, we use  βtsubscript𝛽𝑡\beta\_{t} and  αtsubscript𝛼𝑡\alpha\_{t} to be more consistent with the derivation in Ho et al. ([2020](#bib.bib15)), where

|  |  |  |  |
| --- | --- | --- | --- |
|  | αt=αtαt−1subscript𝛼𝑡subscript𝛼𝑡subscript𝛼𝑡1\displaystyle{\color[rgb]{0,.5,.5}\alpha\_{t}}=\frac{\alpha\_{t}}{\alpha\_{t-1}} |  | (60) |
|  |  |  |  |
| --- | --- | --- | --- |
|  | βt=1−αtαt−1subscript𝛽𝑡1subscript𝛼𝑡subscript𝛼𝑡1\displaystyle{\color[rgb]{0,.5,.5}\beta\_{t}}=1-\frac{\alpha\_{t}}{\alpha\_{t-1}} |  | (61) |

can be uniquely determined from αtsubscript𝛼𝑡\alpha\_{t} (i.e. α¯tsubscript¯𝛼𝑡\bar{\alpha}\_{t}).

First, from the diffusion forward process:

|  |  |  |
| --- | --- | --- |
|  | q​(𝒙t−1|𝒙t,𝒙0)=𝒩​(αt−1​βt1−αt​𝒙0+αt​(1−αt−1)1−αt​𝒙t⏟μ~​(𝒙t,𝒙0),1−αt−11−αt​βt​𝑰)𝑞conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0𝒩subscript⏟subscript𝛼𝑡1subscript𝛽𝑡1subscript𝛼𝑡subscript𝒙0subscript𝛼𝑡1subscript𝛼𝑡11subscript𝛼𝑡subscript𝒙𝑡~𝜇subscript𝒙𝑡subscript𝒙01subscript𝛼𝑡11subscript𝛼𝑡subscript𝛽𝑡𝑰\displaystyle q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})={\mathcal{N}}\Bigg{(}\underbrace{\frac{\sqrt{\alpha\_{t-1}}{\color[rgb]{0,.5,.5}\beta\_{t}}}{1-\alpha\_{t}}{\bm{x}}\_{0}+\frac{\sqrt{{\color[rgb]{0,.5,.5}\alpha\_{t}}}(1-\alpha\_{t-1})}{1-\alpha\_{t}}{\bm{x}}\_{t}}\_{\color[rgb]{0,.5,.5}\tilde{\mu}({\bm{x}}\_{t},{\bm{x}}\_{0})},\frac{1-\alpha\_{t-1}}{1-\alpha\_{t}}{\color[rgb]{0,.5,.5}\beta\_{t}}{\bm{I}}\Bigg{)} |  |

Ho et al. ([2020](#bib.bib15)) considered a specific type of pθ(t)​(𝒙t−1|𝒙t)superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}):

|  |  |  |  |
| --- | --- | --- | --- |
|  | pθ(t)​(𝒙t−1|𝒙t)=𝒩​(μθ​(𝒙t,t),σt​𝑰)superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡𝒩subscript𝜇𝜃subscript𝒙𝑡𝑡subscript𝜎𝑡𝑰\displaystyle p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})={\mathcal{N}}\left({\color[rgb]{0,.5,.5}\mu\_{\theta}({\bm{x}}\_{t},t)},\sigma\_{t}{\bm{I}}\right) |  | (62) |

which leads to the following variational objective:

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | L𝐿\displaystyle{\color[rgb]{0,.5,.5}L} | :=𝔼𝒙0:T∼q​(𝒙0:T)​[q​(𝒙T|𝒙0)+∑t=2Tlog⁡q​(𝒙t−1|𝒙t,𝒙0)−∑t=1Tlog⁡pθ(t)​(𝒙t−1|𝒙t)]assignabsentsubscript𝔼similar-tosubscript𝒙:0𝑇𝑞subscript𝒙:0𝑇delimited-[]𝑞conditionalsubscript𝒙𝑇subscript𝒙0superscriptsubscript𝑡2𝑇𝑞conditionalsubscript𝒙𝑡1  subscript𝒙𝑡subscript𝒙0superscriptsubscript𝑡1𝑇superscriptsubscript𝑝𝜃𝑡conditionalsubscript𝒙𝑡1subscript𝒙𝑡\displaystyle:={\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q({\bm{x}}\_{0:T})}\left[q({\bm{x}}\_{T}|{\bm{x}}\_{0})+\sum\_{t=2}^{T}\log q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0})-\sum\_{t=1}^{T}\log p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t})\right] |  | (63) |
|  |  |  |  |
| --- | --- | --- | --- |
|  |  | ≡𝔼𝒙0:T∼q​(𝒙0:T)​[∑t=2TDKL(q(𝒙t−1|𝒙t,𝒙0))∥pθ(t)(𝒙t−1|𝒙t))⏟Lt−1−log⁡pθ(1)​(𝒙0|𝒙1)]\displaystyle\equiv{\mathbb{E}}\_{{\bm{x}}\_{0:T}\sim q({\bm{x}}\_{0:T})}\left[\sum\_{t=2}^{T}\underbrace{D\_{\mathrm{KL}}(q({\bm{x}}\_{t-1}|{\bm{x}}\_{t},{\bm{x}}\_{0}))\|p\_{\theta}^{(t)}({\bm{x}}\_{t-1}|{\bm{x}}\_{t}))}\_{\color[rgb]{0,.5,.5}L\_{t-1}}-\log p\_{\theta}^{(1)}({\bm{x}}\_{0}|{\bm{x}}\_{1})\right] |  |

One can write:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Lt−1=𝔼q​[12​σt2​∥μθ​(𝒙t,t)−μ~​(𝒙t,𝒙0)∥22]subscript𝐿𝑡1subscript𝔼𝑞delimited-[]12superscriptsubscript𝜎𝑡2superscriptsubscriptdelimited-∥∥subscript𝜇𝜃subscript𝒙𝑡𝑡~𝜇subscript𝒙𝑡subscript𝒙022\displaystyle{\color[rgb]{0,.5,.5}L\_{t-1}}={\mathbb{E}}\_{q}\left[\frac{1}{2\sigma\_{t}^{2}}{\lVert{{\color[rgb]{0,.5,.5}\mu\_{\theta}({\bm{x}}\_{t},t)}-{\color[rgb]{0,.5,.5}\tilde{\mu}({\bm{x}}\_{t},{\bm{x}}\_{0})}}\rVert}\_{2}^{2}\right] |  | (64) |

Ho et al. ([2020](#bib.bib15)) chose the parametrization

|  |  |  |  |
| --- | --- | --- | --- |
|  | μθ​(𝒙t,t)=1αt​(𝒙t−βt1−αt​ϵθ​(𝒙t,t))subscript𝜇𝜃subscript𝒙𝑡𝑡1subscript𝛼𝑡subscript𝒙𝑡subscript𝛽𝑡1subscript𝛼𝑡subscriptitalic-ϵ𝜃subscript𝒙𝑡𝑡\displaystyle{\color[rgb]{0,.5,.5}\mu\_{\theta}({\bm{x}}\_{t},t)}=\frac{1}{\sqrt{{\color[rgb]{0,.5,.5}\alpha\_{t}}}}\left({\bm{x}}\_{t}-\frac{{\color[rgb]{0,.5,.5}\beta\_{t}}}{\sqrt{1-\alpha\_{t}}}{\color[rgb]{0,.5,.5}\epsilon\_{\theta}({\bm{x}}\_{t},t)}\right) |  | (65) |

which can be simplified to:

|  |  |  |  |
| --- | --- | --- | --- |
|  | Lt−1=𝔼𝒙0,ϵ​[βt22​σt2​(1−αt)​αt​∥ϵ−ϵθ​(αt​𝒙0+1−αt​ϵ,t)∥22]subscript𝐿𝑡1subscript𝔼  subscript𝒙0italic-ϵdelimited-[]superscriptsubscript𝛽𝑡22superscriptsubscript𝜎𝑡21subscript𝛼𝑡subscript𝛼𝑡superscriptsubscriptdelimited-∥∥italic-ϵsubscriptitalic-ϵ𝜃subscript𝛼𝑡subscript𝒙01subscript𝛼𝑡italic-ϵ𝑡22\displaystyle{\color[rgb]{0,.5,.5}L\_{t-1}}={\mathbb{E}}\_{{\bm{x}}\_{0},\epsilon}\left[\frac{{\color[rgb]{0,.5,.5}\beta\_{t}}^{2}}{2\sigma\_{t}^{2}(1-\alpha\_{t}){\color[rgb]{0,.5,.5}\alpha\_{t}}}{\lVert{\epsilon-{\color[rgb]{0,.5,.5}\epsilon\_{\theta}(\sqrt{\alpha\_{t}}{\bm{x}}\_{0}+\sqrt{1-\alpha\_{t}}\epsilon,t)}}\rVert}\_{2}^{2}\right] |  | (66) |

## Appendix D Experimental Details

### D.1 Datasets and architectures

We consider 4 image datasets with various resolutions: CIFAR10 (32×32323232\times 32, unconditional), CelebA (64×64646464\times 64), LSUN Bedroom (256×256256256256\times 256) and LSUN Church (256×256256256256\times 256). For all datasets, we set the hyperparameters α𝛼\alpha according to the heuristic in (Ho et al., [2020](#bib.bib15)) to make the results directly comparable. We use the same model for each dataset, and only compare the performance of different generative processes. For CIFAR10, Bedroom and Church, we obtain the pretrained checkpoints from the original DDPM implementation; for CelebA, we trained our own model using the denoising objective L𝟏subscript𝐿1L\_{\bm{1}}.

Our architecture for ϵθ(t)​(𝒙t)superscriptsubscriptitalic-ϵ𝜃𝑡subscript𝒙𝑡\epsilon\_{\theta}^{(t)}({\bm{x}}\_{t}) follows that in Ho et al. ([2020](#bib.bib15)), which is a U-Net (Ronneberger et al., [2015](#bib.bib29)) based on a Wide ResNet (Zagoruyko & Komodakis, [2016](#bib.bib40)). We use the pretrained models from Ho et al. ([2020](#bib.bib15)) for CIFAR10, Bedroom and Church, and train our own model for the CelebA 64×64646464\times 64 model (since a pretrained model is not provided). Our CelebA model has five feature map resolutions from 64×64646464\times 64 to 4×4444\times 4, and we use the original CelebA dataset (not CelebA-HQ) using the [pre-processing technique](https://github.com/NVlabs/stylegan/blob/master/dataset_tool.py#L484-L499) from the StyleGAN (Karras et al., [2018](#bib.bib19)) repository.

Table 3: LSUN Bedroom and Church image generation results, measured in FID. For 1000 steps DDPM, the FIDs are 6.36 for Bedroom and 7.89 for Church.

|  | Bedroom (256×256256256256\times 256) | | | | Church (256×256256256256\times 256) | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dim(τ)dimension𝜏\dim(\tau) | 10 | 20 | 50 | 100 | 10 | 20 | 50 | 100 |
| DDIM (η=0.0𝜂0.0\eta=0.0) | 16.95 | 8.89 | 6.75 | 6.62 | 19.45 | 12.47 | 10.84 | 10.58 |
| DDPM (η=1.0𝜂1.0\eta=1.0) | 42.78 | 22.77 | 10.81 | 6.81 | 51.56 | 23.37 | 11.16 | 8.27 |

### D.2 Reverse process sub-sequence selection

We consider two types of selection procedure for τ𝜏\tau given the desired dim(τ)<Tdimension𝜏𝑇\dim(\tau)<T:

* •

  Linear: we select the timesteps such that τi=⌊c​i⌋subscript𝜏𝑖𝑐𝑖\tau\_{i}=\lfloor ci\rfloor for some c𝑐c;
* •

  Quadratic: we select the timesteps such that τi=⌊c​i2⌋subscript𝜏𝑖𝑐superscript𝑖2\tau\_{i}=\lfloor ci^{2}\rfloor for some c𝑐c.

The constant value c𝑐c is selected such that τ−1subscript𝜏1\tau\_{-1} is close to T𝑇T. We used quadratic for CIFAR10 and linear for the remaining datasets. These choices achieve slightly better FID than their alternatives in the respective datasets.

### D.3 Closed form equations for each sampling step

From the general sampling equation in Eq. ([12](#S4.E12 "In 4.1 Denoising Diffusion Implicit Models ‣ 4 Sampling from Generalized Generative Processes ‣ Denoising Diffusion Implicit Models")), we have the following update equation:

|  |  |  |
| --- | --- | --- |
|  | 𝒙τi−1​(η)=ατi−1​(𝒙τi−1−ατi​ϵθ(τi)​(𝒙τi)ατi)+1−ατi−1−στi​(η)2⋅ϵθ(τi)​(𝒙τi)+στi​(η)​ϵsubscript𝒙subscript𝜏𝑖1𝜂subscript𝛼subscript𝜏𝑖1subscript𝒙subscript𝜏𝑖1subscript𝛼subscript𝜏𝑖superscriptsubscriptitalic-ϵ𝜃subscript𝜏𝑖subscript𝒙subscript𝜏𝑖subscript𝛼subscript𝜏𝑖⋅1subscript𝛼subscript𝜏𝑖1subscript𝜎subscript𝜏𝑖superscript𝜂2superscriptsubscriptitalic-ϵ𝜃subscript𝜏𝑖subscript𝒙subscript𝜏𝑖subscript𝜎subscript𝜏𝑖𝜂italic-ϵ\displaystyle{\bm{x}}\_{\tau\_{i-1}}(\eta)=\sqrt{\alpha\_{\tau\_{i-1}}}\left(\frac{{\bm{x}}\_{\tau\_{i}}-\sqrt{1-\alpha\_{\tau\_{i}}}\epsilon\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i}})}{\sqrt{\alpha\_{\tau\_{i}}}}\right)+\sqrt{1-\alpha\_{\tau\_{i-1}}-\sigma\_{\tau\_{i}}(\eta)^{2}}\cdot\epsilon\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i}})+\sigma\_{\tau\_{i}}(\eta)\epsilon |  |

where

|  |  |  |
| --- | --- | --- |
|  | στi​(η)=η​1−ατi−11−ατi​1−ατiατi−1subscript𝜎subscript𝜏𝑖𝜂𝜂1subscript𝛼subscript𝜏𝑖11subscript𝛼subscript𝜏𝑖1subscript𝛼subscript𝜏𝑖subscript𝛼subscript𝜏𝑖1\sigma\_{\tau\_{i}}(\eta)=\eta\sqrt{\frac{1-\alpha\_{\tau\_{i-1}}}{1-\alpha\_{\tau\_{i}}}}\sqrt{1-\frac{\alpha\_{\tau\_{i}}}{\alpha\_{\tau\_{i-1}}}} |  |

For the case of σ^^𝜎\hat{\sigma} (DDPM with a larger variance), the update equation becomes:

|  |  |  |
| --- | --- | --- |
|  | 𝒙τi−1=ατi−1​(𝒙τi−1−ατi​ϵθ(τi)​(𝒙τi)ατi)+1−ατi−1−στi​(1)2⋅ϵθ(τi)​(𝒙τi)+σ^τi​ϵsubscript𝒙subscript𝜏𝑖1subscript𝛼subscript𝜏𝑖1subscript𝒙subscript𝜏𝑖1subscript𝛼subscript𝜏𝑖superscriptsubscriptitalic-ϵ𝜃subscript𝜏𝑖subscript𝒙subscript𝜏𝑖subscript𝛼subscript𝜏𝑖⋅1subscript𝛼subscript𝜏𝑖1subscript𝜎subscript𝜏𝑖superscript12superscriptsubscriptitalic-ϵ𝜃subscript𝜏𝑖subscript𝒙subscript𝜏𝑖subscript^𝜎subscript𝜏𝑖italic-ϵ\displaystyle{\bm{x}}\_{\tau\_{i-1}}=\sqrt{\alpha\_{\tau\_{i-1}}}\left(\frac{{\bm{x}}\_{\tau\_{i}}-\sqrt{1-\alpha\_{\tau\_{i}}}\epsilon\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i}})}{\sqrt{\alpha\_{\tau\_{i}}}}\right)+\sqrt{1-\alpha\_{\tau\_{i-1}}-\sigma\_{\tau\_{i}}(1)^{2}}\cdot\epsilon\_{\theta}^{(\tau\_{i})}({\bm{x}}\_{\tau\_{i}})+\hat{\sigma}\_{\tau\_{i}}\epsilon |  |

which uses a different coefficient for ϵitalic-ϵ\epsilon compared with the update for η=1𝜂1\eta=1, but uses the same coefficient for the non-stochastic parts. This update is more stochastic than the update for η=1𝜂1\eta=1, which explains why it achieves worse performance when dim(τ)dimension𝜏\dim(\tau) is small.

### D.4 Samples and Consistency

We show more samples in Figure [7](#A4.F7 "Figure 7 ‣ D.4 Samples and Consistency ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (CIFAR10), Figure [8](#A4.F8 "Figure 8 ‣ D.4 Samples and Consistency ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (CelebA), Figure [10](#A4.F10 "Figure 10 ‣ D.4 Samples and Consistency ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (Church) and consistency results of DDIM in Figure [9](#A4.F9 "Figure 9 ‣ D.4 Samples and Consistency ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (CelebA).

![Refer to caption](/html/2010.02502/assets/x13.png)

![Refer to caption](/html/2010.02502/assets/x14.png)

![Refer to caption](/html/2010.02502/assets/x15.png)

Figure 7: CIFAR10 samples from 1000 step DDPM, 1000 step DDIM and 100 step DDIM.



![Refer to caption](/html/2010.02502/assets/x16.png)

![Refer to caption](/html/2010.02502/assets/x17.png)

![Refer to caption](/html/2010.02502/assets/x18.png)

Figure 8: CelebA samples from 1000 step DDPM, 1000 step DDIM and 100 step DDIM.

![Refer to caption](/html/2010.02502/assets/x19.png)


Figure 9: CelebA samples from DDIM with the same random 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} and different number of steps.



![Refer to caption](/html/2010.02502/assets/x20.png)

![Refer to caption](/html/2010.02502/assets/x21.png)

Figure 10: Church samples from 100 step DDPM and 100 step DDIM.

### D.5 Interpolation

To generate interpolations on a line, we randomly sample two initial 𝒙Tsubscript𝒙𝑇{\bm{x}}\_{T} values from the standard Gaussian, interpolate them with spherical linear interpolation (Shoemake, [1985](#bib.bib31)), and then use the DDIM to obtain 𝒙0subscript𝒙0{\bm{x}}\_{0} samples.

|  |  |  |  |
| --- | --- | --- | --- |
|  | 𝒙T(α)=sin⁡((1−α)​θ)sin⁡(θ)​𝒙T(0)+sin⁡(α​θ)sin⁡(θ)​𝒙T(1)superscriptsubscript𝒙𝑇𝛼1𝛼𝜃𝜃superscriptsubscript𝒙𝑇0𝛼𝜃𝜃superscriptsubscript𝒙𝑇1\displaystyle{\bm{x}}\_{T}^{(\alpha)}=\frac{\sin((1-\alpha)\theta)}{\sin(\theta)}{\bm{x}}\_{T}^{(0)}+\frac{\sin(\alpha\theta)}{\sin(\theta)}{\bm{x}}\_{T}^{(1)} |  | (67) |

where θ=arccos⁡((𝒙T(0))⊤​𝒙T(1)∥𝒙T(0)∥​∥𝒙T(1)∥)𝜃superscriptsuperscriptsubscript𝒙𝑇0topsuperscriptsubscript𝒙𝑇1delimited-∥∥superscriptsubscript𝒙𝑇0delimited-∥∥superscriptsubscript𝒙𝑇1\theta=\arccos\left(\frac{({\bm{x}}\_{T}^{(0)})^{\top}{\bm{x}}\_{T}^{(1)}}{{\lVert{{\bm{x}}\_{T}^{(0)}}\rVert}{\lVert{{\bm{x}}\_{T}^{(1)}}\rVert}}\right). These values are used to produce DDIM samples.

To generate interpolations on a grid, we sample four latent variables and separate them in to two pairs; then we use slerp with the pairs under the same α𝛼\alpha, and use slerp over the interpolated samples across the pairs (under an independently chosen interpolation coefficient). We show more grid interpolation results in Figure [11](#A4.F11 "Figure 11 ‣ D.5 Interpolation ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (CelebA), Figure [12](#A4.F12 "Figure 12 ‣ D.5 Interpolation ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (Bedroom), and Figure [13](#A4.F13 "Figure 13 ‣ D.5 Interpolation ‣ Appendix D Experimental Details ‣ Denoising Diffusion Implicit Models") (Church).

![Refer to caption](/html/2010.02502/assets/figures/celeba-interp-grid.png)


Figure 11: More interpolations from the CelebA DDIM with dim(τ)=50dimension𝜏50\dim(\tau)=50.

![Refer to caption](/html/2010.02502/assets/figures/bedroom-interp-grid.png)


Figure 12: More interpolations from the Bedroom DDIM with dim(τ)=50dimension𝜏50\dim(\tau)=50.

![Refer to caption](/html/2010.02502/assets/figures/church-interp-grid.png)


Figure 13: More interpolations from the Church DDIM with dim(τ)=50dimension𝜏50\dim(\tau)=50.

[◄](/html/2010.02501)
[![ar5iv homepage](/assets/ar5iv.png)](/)
[Feeling  
lucky?](/feeling_lucky)

[Conversion  
report](/log/2010.02502)
[Report  
an issue](https://github.com/dginev/ar5iv/issues/new?template=improve-article--arxiv-id-.md&title=Improve+article+2010.02502)
[View original  
on arXiv](https://arxiv.org/abs/2010.02502)[►](/html/2010.02504)

[Copyright](https://arxiv.org/help/license)
[Privacy Policy](https://arxiv.org/help/policies/privacy_policy)

Generated on Sat Mar 2 09:32:15 2024 by [LaTeXML](http://dlmf.nist.gov/LaTeXML/)
