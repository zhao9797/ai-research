# RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths
Source: https://raphael-painter.github.io/
RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths



# RAPHAEL: Text-to-Image Generation via Large Mixture of Diffusion Paths

[Zeyue Xue](https://xuezeyue.github.io/)2\*,

[Guanglu Song](https://songguanglu.github.io/)1\*,
[Qiushan Guo](https://scholar.google.com/citations?user=nDLaim4AAAAJ&hl=zh-CN)2,

[Boxiao Liu](https://scholar.google.com/citations?user=-zEM0ycAAAAJ&hl=en)1,

[Zhuofan Zong](https://scholar.google.com/citations?user=vls0YhoAAAAJ&hl=zh-CN)1,

[Yu Liu](https://liuyu.us/)1†‡,

[Ping Luo](http://luoping.me/)2‡

SenseTime1, The University of Hong Kong2
  
\*Indicates equal contribution.   
†Indicates project lead. ‡Indicates corresponding authors.   
Work done during Zeyue's internship at SenseTime Research.

## Abstract

Text-to-image generation has recently witnessed remarkable achievements. We introduce a text-conditional image diffusion model, termed RAPHAEL, to generate highly artistic images, which accurately portray the text prompts, encompassing multiple nouns, adjectives, and verbs. This is achieved by stacking tens of mixture-of-experts (MoEs) layers, i.e., space-MoE and time-MoE layers, enabling billions of diffusion paths (routes) from the network input to the output. Each path intuitively functions as a "painter" for depicting a particular textual concept onto a specified image region at a diffusion timestep. Comprehensive experiments reveal that RAPHAEL outperforms recent cutting-edge models, such as Stable Diffusion, ERNIE-ViLG 2.0, DeepFloyd, and DALL-E 2, in terms of both image quality and aesthetic appeal. Firstly, RAPHAEL exhibits superior performance in switching images across diverse styles, such as Japanese comics, realism, cyberpunk, and ink illustration. Secondly, a single model with three billion parameters, trained on 1,000 A100 GPUs for two months, achieves a state-of-the-art zero-shot FID score of 6.61 on the COCO dataset. Furthermore, RAPHAEL significantly surpasses its counterparts in human evaluation on the ViLG-300 benchmark. We believe that RAPHAEL holds the potential to propel the frontiers of image generation research in both academia and industry, paving the way for future breakthroughs in this rapidly evolving field.



![MY ALT TEXT](static/images/carousel4.jpg)

## Photography closeup portrait of an adorable rusty broken-down steampunk robot covered in moss moist and budding vegetation, surrounded by tall grass, gorgeous dramatic spring landscape landscape scenic photograph, misty futuristic sci-fi forest environment, bokeh, depth of field.

![MY ALT TEXT](static/images/carousel5.jpg)

## The Caped Crusader, Gotham skyline, rooftop, mysterious, powerful, nighttime, mixed media, expressionism, dark tones, high contrast, in the style of comic book artist Frank Miller, modern, gritty and textured, collage technique.

![MY ALT TEXT](static/images/carousel1.jpg)

## A sureal parallel world where mankind avoid extinction by preserving nature, epic trees, water streams, various flowers, intricate details, rich colors, rich vegetation, cinematic, symmetrical, beautiful lighting, V-Ray render, sun rays, magical lights, photography.

![MY ALT TEXT](static/images/carousel2.jpg)

## Chinese illustration, oriental landscape painting, above super wide angle, magical, romantic, detailed, colorful, multi-dimensional paper kirigami craft.

![MY ALT TEXT](static/images/carousel3.jpg)

## Pirate ship trapped in a cosmic maelstrom nebula, rendered in cosmic beach whirlpool engine, volumetric lighting, spectacular, ambient lights, light pollution, cinematic atmosphere, art nouveau style, illustration art artwork by SenseiJaye, intricate detail.

![MY ALT TEXT](static/images/carousel4.jpg)

## Photography closeup portrait of an adorable rusty broken-down steampunk robot covered in moss moist and budding vegetation, surrounded by tall grass, gorgeous dramatic spring landscape landscape scenic photograph, misty futuristic sci-fi forest environment, bokeh, depth of field.

![MY ALT TEXT](static/images/carousel5.jpg)

## The Caped Crusader, Gotham skyline, rooftop, mysterious, powerful, nighttime, mixed media, expressionism, dark tones, high contrast, in the style of comic book artist Frank Miller, modern, gritty and textured, collage technique.

![MY ALT TEXT](static/images/carousel1.jpg)

## A sureal parallel world where mankind avoid extinction by preserving nature, epic trees, water streams, various flowers, intricate details, rich colors, rich vegetation, cinematic, symmetrical, beautiful lighting, V-Ray render, sun rays, magical lights, photography.

![MY ALT TEXT](static/images/carousel2.jpg)

## Chinese illustration, oriental landscape painting, above super wide angle, magical, romantic, detailed, colorful, multi-dimensional paper kirigami craft.

![MY ALT TEXT](static/images/carousel3.jpg)

## Pirate ship trapped in a cosmic maelstrom nebula, rendered in cosmic beach whirlpool engine, volumetric lighting, spectacular, ambient lights, light pollution, cinematic atmosphere, art nouveau style, illustration art artwork by SenseiJaye, intricate detail.

![MY ALT TEXT](static/images/carousel4.jpg)

## Photography closeup portrait of an adorable rusty broken-down steampunk robot covered in moss moist and budding vegetation, surrounded by tall grass, gorgeous dramatic spring landscape landscape scenic photograph, misty futuristic sci-fi forest environment, bokeh, depth of field.

![MY ALT TEXT](static/images/carousel5.jpg)

## The Caped Crusader, Gotham skyline, rooftop, mysterious, powerful, nighttime, mixed media, expressionism, dark tones, high contrast, in the style of comic book artist Frank Miller, modern, gritty and textured, collage technique.

![MY ALT TEXT](static/images/carousel1.jpg)

## A sureal parallel world where mankind avoid extinction by preserving nature, epic trees, water streams, various flowers, intricate details, rich colors, rich vegetation, cinematic, symmetrical, beautiful lighting, V-Ray render, sun rays, magical lights, photography.



## COCO Zero-Shot Results

**Comparisons** of RAPHAEL with the recent representative text-to-image generation models on the MS-COCO using zero-shot
FID-30k. We see that RAPHAEL outperforms all previous works in image quality, even a commercial product released recently.

![FID](./static/images/FID.png)



## Comparison with SOTA T2I models

### Comparison of presenting concepts

![SOTA](./static/images/comparison_sota.png)

**Comparisons** of RAPHAEL with recent representative generators, Stable Diffusion XL, DeepFloyd, DALL-E 2,
and ERNIE-ViLG 2.0. They are given the same prompts, where the words that the human artists yearn to preserve within the
generated images are highlighted in red. We see that previous models often fail to preserve the desired concepts.
For example, only the RAPHAEL-generated images precisely reflect the prompts such as "pearl earring, Vermeer", "playing soccer", "five cars", "black
high-waisted trouser", "white hair, manga, moon", and "sign, RAPHAEL", while other models generate compromised results.

### Comparison of aesthetics

![SOTA](./static/images/human_eval.png)

**Comparisons** of RAPHAEL with DALL-E 2, Stable Diffusion XL (SD XL), ERNIE-ViLG 2.0, and DeepFloyd in a user study using the ViLG-300 benchmark. We report the user's
preference rates with 95% confidence intervals. We see that RAPHAEL can generate images with higher quality and better
conform to the prompts.

### Efficient finetuning

![SOTA](./static/images/lora.png)

**Results with LoRA** We use 32 images to finetune RAPHAEL and Stable Diffusion. The prompts are "A boy, flower/night/sword/none",
only RAPHAEL preserves the concepts in prompts while Stable Diffusion yields compromised results.

### Prompts

**Prompts generated by GPT-3.5 for Section 3.1 can be found [here](./static/text/prompts.txt).
We use these templates to generate images and diffusion paths for each adjective, noun, and verb. The diffusion paths can be classified by XGBoost algorithm, and the accuracies reach more than 90%.**



This page was built using the [Academic Project Page Template](https://github.com/eliahuhorwitz/Academic-project-page-template).
  
 This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).
