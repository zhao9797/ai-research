# An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion
Source: https://textual-inversion.github.io/
An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion



# An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion

[Rinon Gal](https://rinongal.github.io/)1,2,

[Yuval Alaluf](https://yuval-alaluf.github.io/)1,

[Yuval Atzmon](https://research.nvidia.com/person/yuval-atzmon)2,

[Or Patashnik](https://orpatashnik.github.io/)1,

[Amit H. Bermano](https://www.cs.tau.ac.il/~amberman/)1,

[Gal Chechik](https://research.nvidia.com/person/gal-chechik)2,

[Daniel Cohen-Or](https://www.cs.tau.ac.il/~dcor/)1,

1Tel Aviv University,
2NVIDIA

[Paper](https://arxiv.org/abs/2208.01618)





















[Code](https://github.com/rinongal/textual_inversion)

![Teaser.](static/images/editing/teaser.JPG)

## We learn to generate specific concepts, like personal objects or artistic styles, by describing them using new "words" in the embedding space of pre-trained text-to-image models. These can be used in new sentences, just like any other word. Our work builds on the publicly available [Latent Diffusion Models](https://github.com/CompVis/latent-diffusion)

## Here are some more generated examples. We hope they are cool enough to convince you it's worth reading on :)

![Elephant.](static/images/editing/elephant.JPG)

![Teapot.](static/images/editing/colorful_teapot.JPG)

![Puppet.](static/images/editing/puppet.JPG)

![Round-bird.](static/images/editing/round_bird.JPG)

![Furby.](static/images/editing/furby.JPG)

![bowl.](static/images/editing/bowl.JPG)

![Child Drawing.](static/images/editing/child_drawing.JPG)

![Red Teapot.](static/images/editing/red_teapot.JPG)

![Fluffy.](static/images/editing/fluffy.JPG)

![Thin Bird.](static/images/editing/thin_bird.JPG)

![Elephant.](static/images/editing/elephant.JPG)

![Teapot.](static/images/editing/colorful_teapot.JPG)

![Puppet.](static/images/editing/puppet.JPG)

![Round-bird.](static/images/editing/round_bird.JPG)

![Furby.](static/images/editing/furby.JPG)

![bowl.](static/images/editing/bowl.JPG)

![Child Drawing.](static/images/editing/child_drawing.JPG)

![Red Teapot.](static/images/editing/red_teapot.JPG)

![Fluffy.](static/images/editing/fluffy.JPG)

![Thin Bird.](static/images/editing/thin_bird.JPG)

![Elephant.](static/images/editing/elephant.JPG)

![Teapot.](static/images/editing/colorful_teapot.JPG)

![Puppet.](static/images/editing/puppet.JPG)

## Abstract

Text-to-image models offer unprecedented freedom to guide creation through natural language.
Yet, it is unclear how such freedom can be exercised to generate images of specific unique concepts, modify their appearance, or compose them in new roles and novel scenes.
In other words, we ask: how can we use language-guided models to turn *our* cat into a painting, or imagine a new product based on *our* favorite toy?
Here we present a simple approach that allows such creative freedom.

Using only 3-5 images of a user-provided concept, like an object or a style, we learn to represent it through new "words" in the embedding space of a frozen text-to-image model.
These "words" can be composed into natural language sentences, guiding *personalized* creation in an intuitive way.
Notably, we find evidence that a *single* word embedding is sufficient for capturing unique and varied concepts.

We compare our approach to a wide range of baselines, and demonstrate that it can more faithfully portray the concepts across a range of applications and tasks.

## How does it work?

![](static/images/training/training.JPG)

In the text-encoding stage of most text-to-image models, the first stage involves converting the prompt into a numerical representation. This is typically done by converting the words into tokens, each equivalent to an entry in the model's dictionary.
These entries are then converted into an "embedding" - a continuous vector representation for the specific token. These embeddings are usually learned as part of the training process. In our work, we find new embeddings that represent specific, user-provided visual concepts. These embeddings are then linked to new pseudo-words, which can be incorporated into new sentences like any other word.
In a sense, we are performing inversion into the text-embedding space of the frozen model. We're calling the process 'Textual Inversion'.

## Learning to represent styles

Our method can be used to represent a wide array of concepts - including visual artistic styles. In a sense, we can learn a pseudo-word that represents a specific artist or a new artistic movement, and mimic it in future creations.

![](static/images/style/style.JPG)

Image credits:[@David Revoy](https://commons.wikimedia.org/wiki/User:Deevad). [@QinniArt](https://www.deviantart.com/qinni) result removed at family's request. Image reproduction authorized for non-commercial use only.

## Reducing Biases

Text-to-image models suffer from biases inherited from the training data.
Rather than learning a new concept, we can find new embeddings for 'biased' concepts. These are found using small datasets, so we can easily curate the data and ensure a fairer representation.
For example, here we replace the model's notion of 'Doctor', with a new, more inclusive word.

![](static/images/bias/bias.JPG)

## Compositions

We can combine the new words in order to create scenes that draw on both concepts. Unfortunately, this doesn't yet work for relational prompts, so we can't show you our cat on a fishing trip with our clock.

![](static/images/compositions/compositions.JPG)

Image credits: [@Leslie Manlapig](https://www.pinkstripeysocks.com/p/about.htm). Reproductions authorized for non-commercial & non-print use.

## Downstream Models

Our pseudo-words work with downstream models. For example, if you're tired of your old photographs, you can spice them up by inserting some new friends using [Blended Latent Diffusion](https://omriavrahami.com/blended-latent-diffusion-page/):

![](static/images/blended/blended_diffusion.JPG)

## BibTeX

If you find our work useful, please cite our paper:

```
@misc{gal2022textual,
      doi = {10.48550/ARXIV.2208.01618},
      url = {https://arxiv.org/abs/2208.01618},
      author = {Gal, Rinon and Alaluf, Yuval and Atzmon, Yuval and Patashnik, Or and Bermano, Amit H. and Chechik, Gal and Cohen-Or, Daniel},
      title = {An Image is Worth One Word: Personalizing Text-to-Image Generation using Textual Inversion},
      publisher = {arXiv},
      year = {2022},
      primaryClass={cs.CV}
}
```

This website is licensed under a [Creative
Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/).

Website source code based on the  [Nerfies](https://nerfies.github.io/) project page. If you want to reuse their [source code](https://github.com/nerfies/nerfies.github.io), please credit them appropriately.
