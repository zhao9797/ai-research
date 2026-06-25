# Blended Latent Diffusion
Source: https://omriavrahami.com/blended-latent-diffusion-page/
Blended Latent Diffusion



# Blended Latent Diffusion

[Omri Avrahami](https://omriavrahami.com)1,

[Ohad Fried](https://www.ohadf.com/)2,

[Dani Lischinski](https://www.cs.huji.ac.il/~danix/)1

1The Hebrew University of Jerusalem,
2Reichman University

SIGGRAPH 2023

[PDF](static/paper/Blended_Latent_Diffusion_Paper.pdf)


[arXiv](https://arxiv.org/abs/2206.02779)


[Video](https://www.youtube.com/watch?v=7ZZXmwJCsKI)


[Code](https://github.com/omriav/blended-latent-diffusion)

![Blended Latent Diffusion teaser.](./static/images/teaser.png)

## Given an input image and a mask, Blended Latent Diffusion modifies the masked area according to a guiding text prompt, without affecting the unmasked regions

## Abstract

The tremendous progress in neural image generation, coupled with the emergence of seemingly omnipotent
vision-language models has finally enabled text-based interfaces for creating and editing images. Handling
*generic* images requires a diverse underlying generative model, hence the latest works utilize
diffusion models, which were shown to surpass GANs in terms of diversity. One major drawback of diffusion
models, however, is their relatively slow inference time. In this paper, we present an accelerated
solution to the task of *local* text-driven editing of generic images, where the desired edits are
confined to a user-provided mask. Our solution leverages a recent text-to-image Latent Diffusion Model
(LDM), which speeds up diffusion by operating in a lower-dimensional latent space. We first convert the
LDM into a local image editor by incorporating Blended Diffusion into it. Next we propose an
optimization-based solution for the inherent inability of this LDM to accurately reconstruct images.
Finally, we address the scenario of performing local edits using thin masks. We evaluate our method
against the available baselines both qualitatively and quantitatively and demonstrate that in addition to
being faster, our method achieves better precision than the baselines while mitigating some of their
artifacts.

## Video

## Method

Blended Latent Diffusion aims to offer a solution for the task of
**local** text-driven editing of **generic** images that was introduced in
[Blended Diffusion](https://omriavrahami.com/blended-diffusion-page/) paper. Blended Diffusion
suffered from a slow inference time (getting a good result requires about 25 minutes on a single GPU) and
pixel-level artifacts.

In order to address these issues, we offer to incorporate Blended Diffusion into the text-to-image
[Latent Diffusion Model](https://github.com/CompVis/latent-diffusion). In order to do so, we
operate on the latent space and repeatedly blend the foreground and the background parts in this latent
space, as the diffusion progresses in the following way:

![](./static/images/method_illustration.png)

Operating on the latent space indeed enjoys a fast inference speed, however, it suffers from an imperfect
reconstruction of the unmasked area and it is unable to handle thin masks. For more details on how we
addressed these problems please read the paper.

## Applications

### Background Replacement

Given a source image and a mask of the background, Blended Latent
Diffusion is able to replace the background according to the text description. Note that the
famous landmarks are not meant to accurately appear in the new background but serve as an inspiration for
the image completion.

![](./static/images/background_replacement/img.jpg)

Input image

![](./static/images/background_replacement/mask_overlay.jpg)

Input mask

![](./static/images/background_replacement/beach.jpg)

"beach"

![](./static/images/background_replacement/mountain.jpg)

"big mountain"

![](./static/images/background_replacement/Giza.jpg)

"The Great Pyramid of Giza"

![](./static/images/background_replacement/acropolios.jpg)

"Acropolis"

![](./static/images/background_replacement/Arc_de_Triomphe.jpg)

"Arc de Triomphe"

![](./static/images/background_replacement/big_waterfall.jpg)

"big waterfall"

![](./static/images/background_replacement/China.jpg)

"China"

![](./static/images/background_replacement/Colosseum.jpg)

"Colosseum"

![](./static/images/background_replacement/fire.jpg)

"fire"

![](./static/images/background_replacement/Golden_Gate_Bridge.jpg)

"Golden Gate Bridge"

![](./static/images/background_replacement/Machu_Picchu.jpg)

"Machu Picchu"

![](./static/images/background_replacement/mount fuji.jpg)

"Mount Fuji"

![](./static/images/background_replacement/New_York_City.jpg)

"New York City"

![](./static/images/background_replacement/nuclear-power-plant.jpg)

"nuclear power plant"

![](./static/images/background_replacement/petra.jpg)

"Petra"

![](./static/images/background_replacement/rainy.jpg)

"rainy"

![](./static/images/background_replacement/river.jpg)

"river"

![](./static/images/background_replacement/Stanford_university.jpg)

"Stanford University"

![](./static/images/background_replacement/Stonehenge.jpg)

"Stonehenge"

![](./static/images/background_replacement/sunny.jpg)

"sunny"

![](./static/images/background_replacement/sunrise.jpg)

"sunrise"

![](./static/images/background_replacement/swimming pool.jpg)

"swimming pool"

![](./static/images/background_replacement/volcanic_eruption.jpg)

"volcanic eruption"

![](./static/images/background_replacement/winter.jpg)

"winter"

![](./static/images/background_replacement/green_hills.jpg)

"green hills"

![](./static/images/background_replacement/desert.jpg)

"desert"

![](./static/images/background_replacement/big_lake.jpg)

"big lake"

![](./static/images/background_replacement/forset.jpg)

"forest"

![](./static/images/background_replacement/dusty_road.jpg)

"dusty road"

![](./static/images/background_replacement/horses_stable.jpg)

"horses stable"

![](./static/images/background_replacement/houses.jpg)

"houses"

### Adding a New Object

Given a source image and a mask of an area to edit, Blended Latent
Diffusion is able to add a new object in the masked area seamlessly.

![](./static/images/add_a_new_object/img.jpg)

Input image

![](./static/images/add_a_new_object/mask_overlay.jpg)

Input mask

![](./static/images/add_a_new_object/gravestone2.jpg)

"gravestone"

![](./static/images/add_a_new_object/toy_truck.jpg)

"toy truck"

![](./static/images/add_a_new_object/pred_snake.jpg)

"snake"

![](./static/images/add_a_new_object/big_stone2.jpg)

"big stone"

![](./static/images/add_a_new_object/bread1.jpg)

"bread"

![](./static/images/add_a_new_object/Buddha.jpg)

"Buddha"

![](./static/images/add_a_new_object/car_tire1.jpg)

"car tire"

![](./static/images/add_a_new_object/clay_pot1.jpg)

"clay pot"

![](./static/images/add_a_new_object/cola0.jpg)

"cola"

![](./static/images/add_a_new_object/egg1.jpg)

"egg"

![](./static/images/add_a_new_object/glow_stick1.jpg)

"glow stick"

![](./static/images/add_a_new_object/ice_cube.jpg)

"ice cube"

![](./static/images/add_a_new_object/lamp2.jpg)

"lamp"

![](./static/images/add_a_new_object/milk1.jpg)

"milk"

![](./static/images/add_a_new_object/pile_of_dirt1.jpg)

"pile of dirt"

![](./static/images/add_a_new_object/pile_of_gold1.jpg)

"pile of gold"

![](./static/images/add_a_new_object/tooth1.jpg)

"tooth"

![](./static/images/add_a_new_object/black_chair.jpg)

"black chair"

![](./static/images/add_a_new_object/white_chair.jpg)

"white chair"

![](./static/images/add_a_new_object/bonfire.jpg)

"bonfire"

![](./static/images/add_a_new_object/stones.jpg)

"stones"

![](./static/images/add_a_new_object/black_stones.jpg)

"black stones"

![](./static/images/add_a_new_object/green_stones.jpg)

"green stones"

![](./static/images/add_a_new_object/purple_stones.jpg)

"purple stones"

![](./static/images/add_a_new_object/red_ball.jpg)

"red ball"

![](./static/images/add_a_new_object/yellow_ball.jpg)

"yellow ball"

![](./static/images/add_a_new_object/huge_ant.jpg)

"huge ant"

![](./static/images/add_a_new_object/smoke.jpg)

"smoke"

![](./static/images/add_a_new_object/toy_car.jpg)

"toy car"

![](./static/images/add_a_new_object/water_puddle.jpg)

"water puddle"

![](./static/images/add_a_new_object/huge_apple.jpg)

"huge apple"

![](./static/images/add_a_new_object/yellow_toy_truck.jpg)

"yellow toy truck"

### Object Editing

Given a source image and a mask of an area to edit an existing object, Blended
Latent Diffusion is able alter the object seamlessly.

![](./static/images/object_editing/img.jpg)

Input image

![](./static/images/object_editing/mask_overlay.jpg)

Input mask

![](./static/images/object_editing/pred_yellow.jpg)

"a man with a yellow sweater"

![](./static/images/object_editing/pred_blue.jpg)

"a muscular man with a blue shirt"

![](./static/images/object_editing/pred_red_suit.jpg)

"a man with a red suit"

### Text Generation

Blended Latent Diffusion is able to generate plausible texts.

![](./static/images/text_generation/books/img.jpg)

Input image

![](./static/images/text_generation/books/mask_overlay.jpg)

Input mask

![](./static/images/text_generation/books/pred1.jpg)

a horror book named "CVPR"

![](./static/images/text_generation/books/pred2.jpg)

a children's book titled "ECCV"

![](./static/images/text_generation/books/pred3.jpg)

a romantic novel titled "SIGGRAPH"

### Multiple Results

Because of the one-to-many nature of our problem, there is a need for multiple predictions for each input.
Blended Latent Diffusion is able to to do so.

![](./static/images/multiple_results/graffiti/img.jpg)

Input image

![](./static/images/multiple_results/graffiti/mask_overlay.jpg)

Input mask

![](./static/images/multiple_results/graffiti/recon_pred1.jpg)

Prediction 1

![](./static/images/multiple_results/graffiti/recon_pred2.jpg)

Prediction 2

![](./static/images/multiple_results/graffiti/recon_pred3.jpg)

Prediction 3

![](./static/images/multiple_results/graffiti/recon_pred4.jpg)

Prediction 4

![](./static/images/multiple_results/graffiti/recon_pred5.jpg)

Prediction 5

![](./static/images/multiple_results/graffiti/recon_pred6.jpg)

Prediction 6

  

Input prompt: graffiti with the text "no free lunch"

![](./static/images/multiple_results/stones/img.jpg)

Input image

![](./static/images/multiple_results/stones/mask_overlay.jpg)

Input mask

![](./static/images/multiple_results/stones/pred1.jpg)

Prediction 1

![](./static/images/multiple_results/stones/pred2.jpg)

Prediction 2

![](./static/images/multiple_results/stones/pred3.jpg)

Prediction 3

![](./static/images/multiple_results/stones/pred4.jpg)

Prediction 4

  

Input prompt: "stones"

### Scribble Editing

A user-provided scribble can be used as a guide. Specifically, the user can scribble a rough shape on
a background image, provide a mask (covering the scribble) to indicate the area that is allowed to change,
and provide a text prompt.Blended Latent Diffusion transforms the
scribble into a natural object while attempting to match the prompt.

![](./static/images/scribble_editing/org_img.jpg)

Input image

![](./static/images/scribble_editing/img.jpg)

Input image with scribble

![](./static/images/scribble_editing/mask_overlay.jpg)

Input mask

![](./static/images/scribble_editing/pred1.jpg)

Prediction 1

![](./static/images/scribble_editing/pred2.jpg)

Prediction 2

![](./static/images/scribble_editing/pred3.jpg)

Prediction 3

  

Input prompt: "paint splashes"

## BibTeX

If you find this research useful, please cite the following:

```
@article{avrahami2023blendedlatent,
        author = {Avrahami, Omri and Fried, Ohad and Lischinski, Dani},
        title = {Blended Latent Diffusion},
        year = {2023},
        issue_date = {August 2023},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        volume = {42},
        number = {4},
        issn = {0730-0301},
        url = {https://doi.org/10.1145/3592450},
        doi = {10.1145/3592450},
        journal = {ACM Trans. Graph.},
        month = {jul},
        articleno = {149},
        numpages = {11},
        keywords = {zero-shot text-driven local image editing}
}

@InProceedings{Avrahami_2022_CVPR,
  author    = {Avrahami, Omri and Lischinski, Dani and Fried, Ohad},
  title     = {Blended Diffusion for Text-Driven Editing of Natural Images},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
  month     = {June},
  year      = {2022},
  pages     = {18208-18218}
}
```

You are free to borrow the of this website, we just ask that you link back to this page in the footer. This
page was adapted from [this](https://github.com/nerfies/nerfies.github.io) source code.
