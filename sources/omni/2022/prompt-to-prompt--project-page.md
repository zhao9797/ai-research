# Prompt-to-Prompt
Source: https://prompt-to-prompt.github.io/
Prompt-to-Prompt



# Prompt-to-Prompt Image Editing with Cross-Attention Control

[Amir Hertz1,2](https://amirhertz.github.io/) [Ron Mokady1,2](https://rmokady.github.io/) [Jay Tenenbaum1](jayten@google.com)  [Kfir Aberman1](https://kfiraberman.github.io/) [Yael Pritch1](https://research.google/people/106214/) [Daniel Cohen-Or1,2](https://www.cs.tau.ac.il/~dcor/)  
1 Google Research   2 Tel Aviv University

  
![](./ptp_files/teaser.png)  


[Paper](./ptp_files/Prompt-to-Prompt_preprint.pdf)     
[Code](https://github.com/google/prompt-to-prompt/)

## Abstract

Recent large-scale text-driven synthesis diffusion models have attracted much attention thanks to their remarkable capabilities of generating highly diverse images that follow given text prompts. Therefore, it is only natural to build upon these synthesis models to provide text-driven image editing capabilities. However, Editing is challenging for these generative models, since an innate property of an editing technique is to preserve some content from the original image, while in the text-based models, even a small modification of the text prompt often leads to a completely different outcome. State-of-the-art methods mitigate this by requiring the users to provide a spatial mask to localize the edit, hence, ignoring the original structure and content within the masked region. In this paper, we pursue an intuitive **prompt-to-prompt** editing framework, where the edits are controlled by text only. We analyze a text-conditioned model in depth and observe that the cross-attention layers are the key to controlling the relation between the spatial layout of the image to each word in the prompt. With this observation, we propose to control the attention maps of the edited image by injecting the attention maps of the original image along the diffusion process. Our approach enables us to monitor the synthesis process by editing the textual prompt only, paving the way to a myriad of caption-based editing applications such as localized editing by replacing a word, global editing by adding a specification, and even controlling the extent to which a word is reflected in the image. We present our results over diverse images and prompts with different text-to-image models, demonstrating high-quality synthesis and fidelity to the edited prompts.

## Prompt-to-Prompt Image Editing

Our method enables editing generated images by only modifying the textual prompt.
For example, here we first generate an image from the input prompt "A cat with a hat is lying on a beach chair." using the [Imagen](https://imagen.research.google/) text-to-image diffusion model. Then, with our approach, we can easily replace the hat or the main character.

![](./ptp_files/cat_default.png)

"A   
  
 cat       leopard       lion       horse       turtle       elephant       giraffe       koala
  
  
 with a   
  
 ...       floral       cylinder       police       straw       swimming       pirates       musketeer       clown       unicorn
  
  
 hat is lying on a beach chair."

  

Another prompt editing example is modifying the semantic influence of specific words in the prompt over the generated image.
Using our method, we can amplify or attenuate the "fluffiness" of the bunny doll in the image below.

![](./ptp_files/bunny_seq/fluffy_bunny_42.png)  

"My fluffy bunny doll."

## Cross-Attention Control

The key observation behind our method is that the spatial layout and geometry of an image depend on the cross-attention maps. Below, we show that pixels are attend more to the words that
describe them.

![](./ptp_files/03_bird_and_bear.png)

Therefore, our main idea is to inject the cross-attention maps during the diffusion
process, controlling which pixels attend to which tokens of the prompt text during which diffusion steps.
To apply our approach to various creative editing applications, we show several methods to control the cross-attention maps through a simple and semantic interface. In the *word swap* control, we
modify a token in the prompt (e.g., “dog” to “cat”), while fixing the cross-attention maps, to preserve the scene composition. In the second, *prompt refinement* control, we add new words to the prompt and freeze
the attention to previous tokens while allowing new attention to flow to the new tokens. This enables us to perform global editing or modify a specific object.
In the third, *attention Re-weighting* control, we increase or decrease the attention weights of specified tokens.
This results with amplification or attenuation of the semantic effect of the tokens on the generated image.

![](./ptp_files/03_ca_diagram.png)

### Word Swap Examples

In this case, we swap tokens of the original prompt with others, e.g., “a
basket with apples." to “a basket with oranges.”.

![](./ptp_files/99_imagen_results_web-02.png)

### Prompt Refinement Examples

By extending the initial prompt, we perform local or global editing.

![](./ptp_files/99_imagen_results_web-03.png)

### Attention Re-weighting Examples

By reducing or increasing the cross-attention of
specific words (marked with an arrow), we control the extent to which it influences the generation.

![](./ptp_files/99_imagen_results_web-04.png)
  

## Text-to-Image Style Transfer

By adding a style description to the prompt while injecting the source attention maps, we can create various images in the new desired styles that preserve the structure of the original image.

  
![](./ptp_files/04_style_transfer_web.png)

## Followup Works

[Null-text inversion for Editing Real Images using Guided Diffusion Models](https://null-text-inversion.github.io/) applying Prompt-to-Prompt editing on real images by, first, inverting an input image using pivotal null-text optimization.  
  
[InstructPix2Pix: Learning to Follow Image Editing Instructions](https://www.timothybrooks.com/instruct-pix2pix) training an instruction to image network on synthetic data obtained by combining GPT3 and Prompt-to-Prompt on Stable Diffusion.

#### BibTex

@article{hertz2022prompt,  
  title={Prompt-to-prompt image editing with cross attention control},  
  author={Hertz, Amir and Mokady, Ron and Tenenbaum, Jay and Aberman, Kfir and Pritch, Yael and Cohen-Or, Daniel},  
  booktitle={arXiv preprint arXiv:2208.01626},  
  year={2022}  
}

  

#### Acknowledgements

We thank Noa Glaser, Adi Zicher, Yaron Brodsky, Shlomi Fruchter and David Salesin for their valuable inputs that helped
improve this work, and to Mohammad Norouzi, Chitwan Saharia and William Chan for providing us with
their support and the pretrained models of Imagen. The website template is borrowed from [DreamBooth](https://dreambooth.github.io/).
