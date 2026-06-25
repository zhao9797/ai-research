# Zero-Shot Text-Guided Object Generation with Dream Fields
Source: https://ajayj.com/dreamfields
Zero-Shot Text-Guided Object Generation with Dream Fields



# Zero-Shot Text-Guided Object Generation with Dream Fields

### CVPR 2022 and AI4CC 2022 (Best Poster)

##### [Ajay Jain](/)

###### UC Berkeley, Google Research

##### [Ben Mildenhall](https://bmild.github.io/)

###### Google Research

##### [Jonathan T. Barron](https://jonbarron.info/)

###### Google Research

##### [Pieter Abbeel](https://people.eecs.berkeley.edu/~pabbeel/)

###### UC Berkeley

##### [Ben Poole](https://cs.stanford.edu/~poole/)

###### Google Research

[Paper (arXiv)](https://arxiv.org/abs/2112.01455)
[Code](https://github.com/google-research/google-research/tree/master/dreamfields)
[Colab notebook demo](https://colab.research.google.com/drive/1TjCWS2_Q0HJKdi9wA2OSY7avmFUQYGje?usp=sharing)
[CVPR poster](/dreamfields/assets/dreamfields_cvpr_poster.pdf)

---

## Abstract

**We combine neural rendering with multi-modal image and text representations to synthesize diverse 3D objects solely from natural language descriptions.** Our method, Dream Fields, can generate
the geometry and color of a wide range of objects without 3D supervision. Due to the scarcity of diverse, captioned 3D data, prior methods only generate objects from a handful of categories, such as ShapeNet. Instead, we guide generation
with image-text models pre-trained on large datasets of captioned images from the web. Our method optimizes a Neural Radiance Field from many camera views so that rendered images score highly with a target caption according to a pre-trained
CLIP model. To improve fidelity and visual quality, we introduce simple geometric priors, including sparsity-inducing transmittance regularization, scene bounds, and new MLP architectures. In experiments, Dream Fields produce realistic,
multi-view consistent object geometry and color from a variety of natural language captions.

---

## Example generated objects

Dream Fields can be trained with diverse captions written by artists or from COCO. Descriptions control the style of generated objects, such as color and context.

###### bouquet of flowers sitting in a clear glass vase.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/glass_vase_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/818572727f7ce9066a6bc0a4dcd55e66d5786941/37a86/dreamfields/assets/videos/glass_vase_frames_hq_rgb_20000.mp4)

###### a sculpture of a rooster.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/rooster_frames_hq_rgb_100000.jpg)](https://d33wubrfki0l68.cloudfront.net/56af8e621e3d6c56fe7341aa2363c68ec15d8cc0/71b8b/dreamfields/assets/videos/rooster_frames_hq_rgb_100000.mp4)

###### a robotic dog. a robot in the shape of a dog.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/035_frames_hq_rgb_10000.jpg)](https://d33wubrfki0l68.cloudfront.net/03e12c9090c1ebc48dd15ffad052b754e63b013d/173cb/dreamfields/assets/videos/035_frames_hq_rgb_10000.mp4)

###### matte painting of a castle made of cheesecake surrounded by a moat made of ice cream; trending on artstation; unreal engine. [[ref]](https://twitter.com/ak92501/status/1414266205788065794?s=20)

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/044_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/ff07c25be840a68851c329d366845edfcb2a4b0c/19e27/dreamfields/assets/videos/044_frames_hq_rgb_20000.mp4)

###### a beautiful epic wonderous fantasy painting of the ocean. [[ref]](https://twitter.com/RiversHaveWings/status/1409600293172432899?s=20)

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/056_frames_hq_rgb_90000.jpg)](https://d33wubrfki0l68.cloudfront.net/984610072929551141f2cdf368b87033bac8a3bc/c30f6/dreamfields/assets/videos/056_frames_hq_rgb_90000.mp4)

###### matte painting of a bonsai tree; trending on artstation.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/062_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/b54aae495e4600ed0826c15d1cd8380d76314aa5/30e60/dreamfields/assets/videos/062_frames_hq_rgb_20000.mp4)

###### a cluster of pine trees are in a barren area.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/barren_tree_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/f3638f2f03dd5d45641ccac0f8ee60e68c8e8a07/4e536/dreamfields/assets/videos/barren_tree_frames_hq_rgb_20000.mp4)

###### a boat on the water tied down to a stake.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/boat_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/516826532ad8e4cda9479c86fe3be50391785a74/21af1/dreamfields/assets/videos/boat_frames_hq_rgb_20000.mp4)

###### a small green vase displays some small yellow blooms.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/blooms_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/4a155940302d99849592b49764f20bd3eba1cb8e/61616/dreamfields/assets/videos/blooms_frames_hq_rgb_20000.mp4)

###### a bus covered with assorted colorful graffiti on the side of it.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/graffiti_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/3420e12d8a11c59f397fbaf69c2743ab9a77845b/ca59b/dreamfields/assets/videos/graffiti_frames_hq_rgb_20000.mp4)

###### a pile of crab is seasoned and well cooked.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/crab_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/eafe3f5d5ff0ec7c0347221962d0663c4fbefd2b/87d65/dreamfields/assets/videos/crab_frames_hq_rgb_20000.mp4)

###### a tray that has meat and carrots on a table.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/meat_carrots_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/9d4d801e729fba759381ae1d4115b2278a760415/a74a6/dreamfields/assets/videos/meat_carrots_frames_hq_rgb_20000.mp4)

###### a snowboard standing upright in a snow bank.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/snowboard_frames_hq_rgb_20000.jpg)](https://d33wubrfki0l68.cloudfront.net/76a463b275be745ba8918f90a2e29d8080f87df5/4aeb5/dreamfields/assets/videos/snowboard_frames_hq_rgb_20000.mp4)

Slide 1 of 11.

---

## Compositional generation

The compositional nature of language allows users to combine concepts in novel ways and control generation. A template prompt describing a primary object (an armchair or a teapot) is stylized with 16 materials: *avocado, glacier, orchid, pikachu, brain coral, gourd, peach, rubik's cube, doughnut, hibiscus, peacock, sardines, fossil, lotus root, pig,* or *strawberry*. These prompt templates are sourced from [DALL-E](https://openai.com/blog/dall-e/).

###### an archair in the shape of a \_\_\_\_. an archair imitating a \_\_\_\_.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/armchairs.jpg)](https://d33wubrfki0l68.cloudfront.net/4e35b8317133976a8664486b16968fdf2e0b93fb/7d27e/dreamfields/assets/videos/armchairs.mp4)

###### a teapot in the shape of a \_\_\_\_. a teapot imitating a \_\_\_\_.

[![

Your browser does not support the video tag.
](/dreamfields/assets/videos/teapots.jpg)](https://d33wubrfki0l68.cloudfront.net/17a2ef5ac1a4a98c8386dccf7e59dc61da6c3dee/5a619/dreamfields/assets/videos/teapots.mp4)

---

## Related publications

[![Overview of DietNeRF's semantic consistency loss.](https://d33wubrfki0l68.cloudfront.net/8f2a5fbbb0ccbae01a0f5402cef18a682db8905a/1c039/dietnerf/assets/img/dietnerf_method_anim_25p.gif)](/dietnerf/)

#### Putting NeRF on a Diet: Semantically Consistent Few-Shot View Synthesis

##### Ajay Jain, Matthew Tancik, Pieter Abbeel ICCV 2021 International Conference on Computer Vision

DietNeRF regularizes Neural Radiance Fields with a CLIP-based loss to improve 3D reconstruction. Given only a few images of an object or scene, we reconstruct its 3D structure & render novel views using prior knowledge contained
in large image encoders.

* [[Website]](/dietnerf/)
* [[arXiv]](https://arxiv.org/abs/2104.00677)
* [[Code]](https://github.com/ajayjain/DietNeRF)

[![mip-NeRF integrated positional encoding](https://jonbarron.info/images/mipnerf_ipe.png)](http://jonbarron.info/mipnerf)

#### Mip-NeRF: A Multiscale Representation for Anti-Aliasing Neural Radiance Fields

##### Jonathan T. Barron, Ben Mildenhall, Matthew Tancik, Peter Hedman, Ricardo Martin-Brualla, Pratul Srinivasan ICCV 2021 International Conference on Computer Vision

NeRF is aliased, but we can anti-alias it by casting cones and prefiltering the positional encoding function. Dream Fields combine mip-NeRF's integrated positional encoding with [Fourier features](https://bmild.github.io/fourfeat/).

* [[Website]](https://jonbarron.info/mipnerf/)
* [[arXiv]](https://arxiv.org/abs/2103.13415)
* [[Code]](https://github.com/google/mipnerf)

---

## Citation

Ajay Jain, Ben Mildenhall, Jonathan T. Barron, Pieter Abbeel, Ben Poole. Zero-Shot Text-Guided Object Generation with Dream Fields. arXiv, 2021.

`@article{jain2021dreamfields,  
  author = {Jain, Ajay and Mildenhall, Ben and Barron, Jonathan T. and Abbeel, Pieter and Poole, Ben},  
  title = {Zero-Shot Text-Guided Object Generation with Dream Fields},  
  joural = {CVPR},  
  year = {2022},  
}`
