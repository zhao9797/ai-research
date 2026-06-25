# InstructPix2Pix
Source: https://www.timothybrooks.com/instruct-pix2pix/
InstructPix2Pix



# InstructPix2Pix

## Learning to Follow Image Editing Instructions

[Tim Brooks](https://timothybrooks.com/about)\*, 

[Aleksander Holynski](http://www.holynski.org)\*, 

[Alexei A. Efros](https://people.eecs.berkeley.edu/~efros/)

University of California, Berkeley

\*Denotes equal contribution

CVPR 2023 (Highlight)

[arXiv](https://arxiv.org/abs/2211.09800)

[Code](https://github.com/timothybrooks/instruct-pix2pix)

[Demo](https://huggingface.co/spaces/timbrooks/instruct-pix2pix)

![Teaser](https://instruct-pix2pix.timothybrooks.com/teaser.jpg)

## Given an image and a written instruction, our method follows the instruction to edit the image.

## Abstract

We propose a method for editing images from human instructions: given an input image and a written
instruction that tells the model what to do, our model follows these instructions to edit the image. To
obtain training data for this problem, we combine the knowledge of two large pretrained models---a
language model (GPT-3) and a text-to-image model (Stable Diffusion)---to generate a large dataset of image
editing examples. Our conditional diffusion model, InstructPix2Pix, is trained on our generated data, and
generalizes to real images and user-written instructions at inference time. Since it performs edits in the
forward pass and does not require per-example fine-tuning or inversion, our model edits images quickly, in
a matter of seconds. We show compelling editing results for a diverse collection of input images and
written instructions.

[

](https://instruct-pix2pix.timothybrooks.com/instruct-pix2pix.mp4)
Here is a fun mock text conversation showing the potential for instruction-based image editing assistants. The
texting part is just for show, but the instructions and images are real inputs and generated results.

## Results

![](https://instruct-pix2pix.timothybrooks.com/landscape.jpg)
Note that isolated changes also bring along
accompanying contextual effects: the addition of boats also adds wind ripples in the water, and the added
city skyline is reflected on the lake. ([source](https://www.pexels.com/photo/trees-near-body-of-water-371589/))
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/adam.jpg)
Despite being trained at 256x256 resolution, our model can perform realistic edits images up to 768-width resolution.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/abbey.jpg)
A single image (in this case, the iconic Beatles *Abbey Road* album cover) can be transformed in a large variety of ways.  
  
  
![](https://instruct-pix2pix.timothybrooks.com/mona.jpg)
Leonardo da Vinci's *Mona Lisa* transformed into various artistic mediums.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/cityscape.jpg)
A photograph of a cityscape edited to show different times of day ([source](https://www.pexels.com/photo/cityscape-photography-near-water-290595/)).
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/girl.jpg)
Vermeer's *Girl with a Pearl Earring* with a variety of edits.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/man.jpg)
Van Gogh's *Self-Portrait with a Straw Hat* in different mediums.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/garden.jpg)
Leighton's *Lady in a Garden* moved to a new setting.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/seeds.jpg)
By varying the latent noise, our model can produce many possible image edits for the same input image and
instruction.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/chained.jpg)
Applying our model recurrently with different instructions results in compounded edits.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/bias.jpg)
Our method reflects biases from the data and models it is based upon, such as correlations between
profession and gender.
  
  
  
![](https://instruct-pix2pix.timothybrooks.com/failures.jpg)
Failure cases. Left to right: our model is not capable of performing viewpoint changes, can make undesired
excessive changes to the image, can sometimes fail to isolate the specified object, and has difficulty
reorganizing or swapping objects with each other.

## BibTeX

```
@InProceedings{brooks2022instructpix2pix,
    author     = {Brooks, Tim and Holynski, Aleksander and Efros, Alexei A.},
    title      = {InstructPix2Pix: Learning to Follow Image Editing Instructions},
    booktitle  = {CVPR},
    year       = {2023},
}
```

## Slides

Feel free to use these slides to help explain our research:

* [PowerPoint](https://instruct-pix2pix.timothybrooks.com/instruct-pix2pix.pptx)
* [PDF](https://instruct-pix2pix.timothybrooks.com/instruct-pix2pix.pdf)

## Acknowledgements

We thank Ilija Radosavovic, William Peebles, Allan Jabri, Dave Epstein, Kfir Aberman, Amanda Buster, and David Salesin.
Tim Brooks is funded by an NSF Graduate Research Fellowship. Additional funding by a research grant from SAP
and a gift from Google.

Website adapted from the following [template](http://nerfies.github.io).
