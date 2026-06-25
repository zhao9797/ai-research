# Null-text Inversion for Editing Real Images using Guided Diffusion Models
Source: https://null-text-inversion.github.io/
Null-text Inversion for Editing Real Images using Guided Diffusion Models



# Null-text Inversion for Editing Real Images using Guided Diffusion Models

[Ron Mokady\* 1,2](https://rmokady.github.io/) [Amir Hertz\* 1,2](https://amirhertz.github.io/) [Kfir Aberman1](https://kfiraberman.github.io/) [Yael Pritch1](https://research.google/people/106214/) [Daniel Cohen-Or1,2](https://www.cs.tau.ac.il/~dcor/)  
  
1 Google Research 2 Tel Aviv University   
\*Denotes Equal Contribution

  
![](./files/teaser-01.png)  


[Paper](https://arxiv.org/abs/2211.09794)     
[Code](https://github.com/google/prompt-to-prompt/#null-text-inversion-for-editing-real-images)

## TL;DR

Null-text inversion enables intuitive text-based editing of real images with the Stable Diffusion model. We use an initial DDIM inversion as an anchor for our optimization which only tunes the null-text embedding used in classifier-free guidance.

## Abstract

Recent large-scale text-guided diffusion models provide powerful image generation capabilities. Currently, a massive effort is given to enable the modification of these images using text only as means to offer intuitive and versatile editing tools. To edit a real image using these state-of-the-art tools, one must first invert the image with a meaningful text prompt into the pretrained model's domain. In this paper, we introduce an accurate inversion technique and thus facilitate an intuitive text-based modification of the image. Our proposed inversion consists of two key novel components: (i) **Pivotal inversion for diffusion models.** While current methods aim at mapping random noise samples to a single input image, we use a single pivotal noise vector for each timestamp and optimize around it. We demonstrate that a direct DDIM inversion is inadequate on its own, but does provide a rather good anchor for our optimization. (ii) **Null-text optimization**, where we only modify the unconditional textual embedding that is used for classifier-free guidance, rather than the input text embedding. This allows for keeping both the model weights and the conditional embedding intact and hence enables applying prompt-based editing while avoiding the cumbersome tuning of the model's weights. Our null-text inversion, based on the publicly available Stable Diffusion model, is extensively evaluated on a variety of images and various prompt editing, showing high-fidelity editing of real images.

## Null-text Inversion

On top: We first apply an initial DDIM inversion on the input image which estimates a diffusion trajectory (top trajectory). Starting the diffusion process from the last latent code results in unsatisfying reconstruction (bottom trajectory) as the intermediate codes become farther away from the original trajectory. We use the initial trajectory as a pivot for our optimization which brings the diffusion backward trajectory closer to the original image.
![](./files/diagram-01.png)  
Bottom: null-text optimization for
timestamp t. Recall that classifier-free guidance consists of performing the noise prediction twice – using text condition embedding
and unconditionally using null-text embedding ∅ (bottom-left).
Then, these are extrapolated with guidance scale w (middle). We
optimize only the unconditional embeddings ∅t by employing a reconstruction MSE loss (in red) between the predicated latent code to the pivot.

## Results

![](./files/editing_results-01.png)

## Inversion with Different Captions

As demonstrated below, our method accurately inverts an input image (top row) using different input captions (left image in each row).
Yet, the edited parts should be included in the caption. For example, to edit the print on the shirt,
the caption should include a descriptive term like ”shirt with a drawing” (last row).  
  
![](./files/multi_cap-01.png)  
The cross-attention maps, which were obtained after the inversion, provide intuition on the editing capabilities with respect to the different captions. For example, only in the top row, we do get an attention map that captures the hair of the woman and therefore enables the local editing of the hair color or style using [Prompt-to-Prompt](https://prompt-to-prompt.github.io/).   
  
![](./files/multi_cap-02.png)

## Inversion Ablation

![](./files/ablation-01.png)  
We compare the performance of our full algorithm (green line) to different variations, evaluating the reconstruction quality by measuring the PSNR score as a function of number optimization iterations and running time in minutes. Below, we visually show the inversion results after 200 iterations of our full algorithm (on right) compared to other baselines.  
  
![](./files/comparison_ablation-01.png)
