# Paint by Word
Source: http://paintbyword.csail.mit.edu/
Paint by Word



Paint by Word

[Alex Andonian](https://www.alexandonian.com/)1,
[Sabrina Osmany](https://www.gsd.harvard.edu/person/sabrina-osmany/)2,
[Audrey Cui](https://audreycui.github.io/)1,
[YeonHwan Park](https://yeonhwanp.com/)1,
[Ali Jahanian](http://people.csail.mit.edu/jahanian/index.html)1,
[Antonio Torralba](http://web.mit.edu/torralba/www/)1,
[David Bau](https://people.csail.mit.edu/davidbau/home/)1,
  
1[Massachusetts Institute of Technology CSAIL](https://www.csail.mit.edu/),
2[Harvard GSD](https://www.gsd.harvard.edu/)

[![](images/paper-thumb.png)  
ArXiv  
Preprint](https://arxiv.org/abs/2103.10951)
[![](images/code-thumb.png)  
Source Code  
Github](https://github.com/alexandonian/paint-by-word)

### What is Paint by Word?

Paint by Word allows you to use words to create an AI paintbrush.
For example, if you want to make a piece of furniture look rustic,
you can use the words "rustic bed" to define a paintbrush that can
modify a bed to take on that style. Or use other words and paint other objects,
as shown in the example below.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | In this area... | ... Paint this word: | | | |
|  | (user-painted) | Metallic | Rustic | Purple | Floral |
| Window |  |  |  |  |  |
| Bed |  |  |  |  |  |

Demonstrating our method. A user scribbles on a region of an image and specifies words to paint in that area. Painting the window to make it "rustic" adds wooden dividers; painting a bed "rustic" changes the style of the bedframe and sheets. Each word has an effect that is specific to the context.

## How does Paint by Word Work?

Paint by Word pairs an image generator such as StyleGANv2
([Karras, et al 2019](https://arxiv.org/abs/1912.04958))
or BigGAN ([Brock, et al 2018](https://arxiv.org/abs/1809.11096))
with the recent CLIP network from OpenAI
([Radford, et al 2021](https://arxiv.org/abs/2103.00020)).
We split the image generator to allow the region painted by the user
to be separately controlled, and then we modify the generator's
representation of the region to match the words given by the user,
by maximizing the score given by CLIP.

The approach is remarkably simple: both networks are taken
off-the-shelf without fine-tuninig to the task. Both networks were
originally trained on simpler problems: CLIP does not know how to
edit or generate an image on its own, and the GAN does not know about
anything about language on its own.

![](images/pbw-arch.png)

Overview of the architecture. C denotes networks in the CLIP model. f and h denote layers of a GAN generator. We search for masked perturbations of internal latents (w) of the generator to optimize semantic similarity between the image and the text provided by the user.

## What do we learn?

It is interesting to find that a pair of models that were not trained together can
acheive good results on a difficult task by just guiding one another. To create
accurate, realistic, targeted results, we make two key observations:

1. Results are more realistic and accurate when **optimizing a distribution**
   of images to the objective, rather than overfitting a single image. We find
   that Covariance Matrix Adaptation ([CMA-ES](https://en.wikipedia.org/wiki/CMA-ES))
   yields better results than
   gradient descent, and good enough to achieve state-of-the-art on
   a standard benchmark of bird descriptions.
   ![](images/cma-vs-adam.png)
   Despite minimizing losses well (a), gradient-descent
   methods such as Adam tend to synthesize unrealistic images like (b).
   Distribution-optimizing methods such as CMA make more realistic results (c)
   even though numerical losses are higher.
2. Targeting changes to a specific user-provided region can be
   done by **splitting the generative model** spatially, so
   that the area inside the user region is represented using a different
   latent from the area outside the region.
   ![](images/split-vs-not.png)
   When steering a generator to match a text description
   by allowing CLIP to only see and give gradients in a selected region (b),
   the generator will modify other regions of the image too (c); modifying
   the generator to decouple latents inside the region will allow it to focus
   changes in the selected area.

## Benchmarking realism and accuracy

One of the standard ways to evaluate accuracy and realism on the difficult
text-to-image task is to generate images of birds based on a set of
English captions of birds based on
the [CUB birds](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html)
dataset. We evaluated our method on this test by training a StyleGANv2 on CUB birds
and painting the full image using the caption words.

![](images/bird-comparison.png)

Our method yields strong results on this benchmark, outperforming
the bird images synthesized previous state-of-the-art
[DALL-E method (Ramesh, et al. 2021)](https://arxiv.org/abs/2102.12092) when rated by humans.
In the evaluation below, five hundred synthesized images are each evaluated by three people
for realism (which method looks more like a real photograph?) and accuracy (which image
is a better match for the text?)

![](images/bird-benchmark.png)
Note that, in this setting, our method is much narrower than DALL-E and can only draw
birds, whereas DALL-E can draw a much broader variety of general images. However,
this test shows that competitive results can be obtained using a very simple approach
where the image generator is not trained with any awareness of text.

## More examples of editing

## How to Cite

### bibtex

```
@misc{bau2021paintbyword,
 title={Paint by Word},
 author={Alex Andonian and Sabrina Osmany and Audrey Cui and YeonHwan Park
   and Ali Jahanian and Antonio Torralba and David Bau},
 year={2021},
 eprint={arXiv:2103.10951},
}
```



[About David Bau](https://people.csail.mit.edu/davidbau/)

[About Alex Andonian](https://www.alexandonian.com/)

[Accessibility](https://accessibili

[truncated]
