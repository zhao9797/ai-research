# Releasing Open Weights for FLUX.1 Krea - Krea
Source: https://www.krea.ai/blog/flux-krea-open-source-release
Releasing Open Weights for FLUX.1 Krea - Krea 

[App](https://www.krea.ai/app) [Image Generator](https://www.krea.ai/features/ai-image-generator) [Video Generator](https://www.krea.ai/features/ai-video-generator) [Upscaler](https://www.krea.ai/features/ai-upscaler) [API](https://www.krea.ai/features/api) [Pricing](https://www.krea.ai/pricing) [Enterprise](https://www.krea.ai/enterprise)

[Sign up for free](https://www.krea.ai/login) [Log in](https://www.krea.ai/login)

 

[Sign up for free](https://www.krea.ai/login) [Log in](https://www.krea.ai/login)

[App](https://www.krea.ai/app) [Image Generation](https://www.krea.ai/features/ai-image-generator) [Video Generation](https://www.krea.ai/features/ai-video-generator) [Upscale & Enhance](https://www.krea.ai/features/ai-enhancer) [API](https://www.krea.ai/features/api) [Pricing](https://www.krea.ai/pricing) [Enterprise](https://www.krea.ai/enterprise)

   [Breaking down the "AI Look"](#section-0)[The art of mode collapse](#section-1)[Pre-training](#section-2)[Post-training](#section-3)[Starting with a raw base](#section-4)[Our post-training pipeline](#section-5)[Future research directions](#section-6)[Acknowledgements](#section-7)[Citation](#section-8) 

[Krea](/) / [News](/blog) / Releasing Open Weights for FLUX.1 Krea  

# Releasing Open Weights for FLUX.1 Krea

Sangwu Lee, Erwann Millon
 31 July, 2025

[Try FLUX.1 Krea now](https://www.krea.ai/apps/image/flux-krea)

[Download the weights [22GB] on Hugging Face](https://huggingface.co/black-forest-labs/FLUX.1-Krea-dev) [View our repository on Github](https://github.com/krea-ai/flux-krea)

Today, we're releasing an open version of Krea 1, our first image model trained in
collaboration with [Black Forest Labs](https://bfl.ai) to offer superior
aesthetic control and image quality. This checkpoint is a guidance distilled model fully
compatible with
[FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) allowing
seamless integration with the existing ecosystem. FLUX.1-Krea [dev] has been distilled to
match the quality of Krea 1 with a focus on preserving aesthetics and photorealism.

Unlike most image models, FLUX.1 Krea has been created with opinionated aesthetics in
mind. We focused on creating a model that truly fits our specific aesthetic preferences.
In this technical report, we'll share the process and learnings from developing this
model, including insights on pre-training and post-training, as well as future research
directions.

![White owl, close up portrait, mysterious ghost like owl, low contrast, cinematic dark moody photo, slight blue color grading](https://s.krea.ai/k1-os-examples/owl.png)![A warm, elegant living room drenched in late afternoon sunlight features a carefully curated mix of mid-century modern and contemporary furniture.](https://s.krea.ai/k1-os-examples/midcentury-interior.png)![Extreme close up of a vintage BMW racing through Tokyo at night, tilted camera, green color grading, bokeh](https://s.krea.ai/k1-os-examples/car-tokyo.png)![A bear on a chair in a car museum, moody, cinematic, dark shot, muted colors, film grain, soothing tones, technicolor](https://s.krea.ai/k1-os-examples/bear.png)![Moody night photography, a small store with an orange glowing sign that says "Black Forest Labs"](https://s.krea.ai/k1-os-examples/bfl-neon.png)![Photo of two people having a tea party in a lush garden](https://s.krea.ai/k1-os-examples/tea.png)![Tiny paper origami kingdom, a river flowing through a lush valley, bright saturated image, a fox to the left, deer to the right, birds in the sky, bushes and tress all around](https://s.krea.ai/k1-os-examples/paper-fox.png)![8 bit pixel art of the world's coziest house, cinematic lighting, red sunset, dark winter](https://s.krea.ai/k1-os-examples/pixel-house.png)![Super close up wide shot bird eye on black background](https://s.krea.ai/k1-os-examples/bird.png)![Vibrant garden with victorian house](https://s.krea.ai/k1-os-examples/garden.png)![Vibrant photo close up](https://s.krea.ai/k1-os-examples/flower.png)![Dslr photo, bird with horns](https://s.krea.ai/k1-os-examples/bird-horns.png)![Dreamy scene of a woman dancing with a super long red dress made of flowers](https://s.krea.ai/k1-os-examples/woman.png)![Dreamy scene dad and son look at the sunset, ghibli style anime scene, the kid is pointing towards the sunset](https://s.krea.ai/k1-os-examples/anime-dad.png)![Cinematic dramatic wide shot super close up](https://s.krea.ai/k1-os-examples/man.png)

“White owl, close up portrait, mysterious ghost like owl, low contrast, cinematic dark moody photo, slight blue color grading”

## Breaking down the "AI Look"

> "When a measure becomes a target, it ceases to be a good measure"

—Charles Goodhart

 

Image generation has come a long way since the early days of generating cats and flowers
with GANs. Today's models can generate coherent human faces, limbs, and hands. They
understand exact quantities, render complex typography, and make an astronaut ride a
horse.

However, a clear trend when working with AI generated images is their unique look:
overly-blurry backgrounds, waxy skin textures, boring composition, and more. Together,
these problems constitute what is now known as the ["AI look"](https://arxiv.org/abs/2506.15742).

 

![AI look example](/blog/flux-krea/ailook2.webp) ![AI look example](/blog/flux-krea/ailook1.webp) ![AI look example](/blog/flux-krea/ailook3.webp)

Some examples of the "AI look" in human faces

 

People often focus on how "smart" a model is. We often see users testing complex
prompts. Can it make a horse ride an astronaut? Does it fill up the wine glass to the
brim? Can it render text properly? Over the years, we have devised various benchmarks to
formalize these questions into concrete metrics. The research community has done a
remarkable job advancing generative models. However, in this pursuit of technical
capabilities and benchmark optimization, the messy genuine look, stylistic diversity,
and creative blend of early image models took a backseat.

 ![DALLE-2 generations](/blog/flux-krea/dalle2.webp) 

Generations from DALLE-2, an imperfect model which produced flawed but interesting
outputs. [Source](https://thesephist.com/posts/epistemic-calibration/)

 

Our goal from the beginning was simple: "Make AI images that don't look AI." As users of
generative AI ourselves, we wanted to create a model that addressed these issues.
Unfortunately, many of the academic benchmarks and metrics are misaligned with what
users actually want.

For the pre-training stage, metrics such as [Fréchet inception distance (FID)](https://arxiv.org/abs/1706.08500)
and [CLIP Score](https://arxiv.org/abs/2104.08718) are useful for measuring
general performance of the model since most images at this stage are incoherent. Beyond the
pre-training stage, evaluation benchmarks such as [DPG](https://arxiv.org/abs/2403.05135),
[GenEval](https://arxiv.org/abs/2310.11513), [T2I-Compbench](https://arxiv.org/abs/2307.06350), and [GenAI-Bench](https://arxiv.org/abs/2406.13743) are widely used to
benchmark academic and industry models. But, these benchmarks are limited to measuring prompt
adherence with focus on spatial relationships, attribute binding, object counts, etc.

For evaluating aesthetics, models such as [LAION-Aesthetics](https://github.com/christophschuhmann/improved-aesthetic-predictor), [Pickscore](https://arxiv.org/abs/2305.01569), [ImageReward](https://arxiv.org/abs/2304.05977), [HPSv2](https://arxiv.org/abs/2306.09341) are commonly used, but many
of these models are finetuned variants of [CLIP](https://openai.com/index/clip/),
which processes low-resolution images (224×224 pixels) with limited parameter
count. As the capability of image generation models has increased, these older aesthetic
score models are no longer good enough to evaluate them.

For instance, we find that LAION Aesthetics — a model commonly used to obtain high
quality training images — to be highly biased towards depicting women, blurry
backgrounds, overly soft textures, and bright images. While these aesthetic scorers and
image quality filters are **useful for filtering out bad images**, relying on these
models to obtain high quality training images adds implicit biases to the model's
priors.

 ![LAION aesthetics examples](/blog/flux-krea/laion.webp) 

Examples of images that are in the top 5% of LAION aesthetics

 

While better aesthetic scorers based on vision language models ([[1]](https://arxiv.org/abs/2505.03318),
[[2]](https://arxiv.org/abs/2412.21059)) are emerging, the issue remains that human preference and aesthetics are highly
personal. They cannot be easily reduced to a single number. Advancing model capabilities
without regressing towards the "AI look" requires careful data curation and thorough
calibration of model outputs.

## The art of mode collapse

> "The sculpture is already complete within the marble block, before I start my work.
> It is already there, I just have to chisel away the superfluous material."

—Michelangelo

 

Training an image generation model can be roughly divided into two stages: pre-training
and post-training. Most of the aesthetics of a model are learned during the post
training stage, but before explaining our post-training methodology, let's go over some
intuition on how we think about these training stages.

 

Good mode coverage

    

Bad mode coverage

Pre-training is all about mode coverage, post-training is all about mode collapsing.

 

### Pre-training

The focus of the pre-training stage should be all about "mode coverage" and "world
understanding." During this stage, we give the model rich knowledge about the visual
world: styles, objects, places, people. The goal here is to maximize diversity.

We would even argue that the pre-trained model should be trained on "bad" data, as long
as the undesirable aspects of the data are accurately captured in its conditioning.
Indeed, in addition to telling the model what we want, we often want to tell it what we
*don't* want.

Many image generation workflows use negative prompts like "too many fingers, deformed
faces, blurry, oversaturated" to improve image quality. For the negative prompt to steer
the model away from undesirable parts of the data distribution, it must first have
learned what these undesirable parts look like. Negative prompting would not be
effective if the model never saw examples of "bad images."

While post-training has the highest impact on the final quality of the model, it's
important to remember that the quality ceiling of the model and the stylistic diversity
comes from the pre-trained model.

### Post-training

During post-training, the focus should be on shifting and chipping away the undesirable
part of the distribution. A pre-trained model can output diverse images and understands
a wide range of concepts, but struggles to reliably output high quality images as it's
not biased enough towards producing aesthetic outputs. This is where mode collapsing
comes into play: we want to start biasing the model towards the part of the distribution
we find desirable.

## Starting with a raw base

To start post-training, we need a "raw" model. We want a malleable base model with a
diverse output distribution that we can easily reshape towards a more opinionated
aesthetic. Unfortunately, many existing open weights models have been already heavily
finetuned and post-trained. In other words, they are too "baked" to use as a base model.

To be able to fully focus on aesthetics, we partnered with a world-class foundation
model lab, [Black Forest Labs](http://bfl.ai), who provided us with
**flux-dev-raw**, a pre-trained and [guidance-distilled](https://arxiv.org/abs/2210.03142)
12B parameter diffusion transformer model.

![flux-dev-raw](/blog/flux-krea/fluxdevraw1.webp) ![flux-dev-raw](/blog/flux-krea/fluxdevraw2.webp) ![flux-dev-raw](/blog/flux-krea/fluxdevraw3.webp) ![flux-dev-raw](/blog/flux-krea/fluxdevraw4.webp)

Samples from flux-dev-raw generations

 

As a pre-trained base model, **flux-dev-raw** does not achieve image quality anywhere
near that of state-of-the-art foundation models. However, it is a strong base for post-training
for three reasons:

1. **flux-dev-raw** contains a lot of world knowledge — it already knows common objects,
   animals, people, camera angles, medium, etc.
2. **flux-dev-raw**, although being a raw model, already offers compelling quality: it
   can generate coherent structure, basic composition, and render text.
3. **flux-dev-raw** is not "baked" — it is an untainted model that does not have the "AI
   aesthetic." It is able to generate very diverse images, ranging from raw to beautiful.

## Our post-training pipeline

Our post-training pipeline is split into two stages. A Supervised Finetuning (SFT)
stage and Reinforcement Learning from Human Feedback (RLHF) stage.
During the supervised finetuning stage, we hand curate a dataset of the highest quality
of images that match our aesthetic standards. For training FLUX.1 Krea [dev], we also
incorporate high quality synthetic samples from Krea-1 during SFT stage. We find that
synthetic images to be beneficial for stabilizing the performance of the checkpoint.

Since flux-dev-raw is a guidance distilled model, we devise a custom loss to finetune
the model directly on a classifier-free guided ([CFG](https://arxiv.org/abs/2207.12598)) distribution. After the SFT stage, the model's image quality output is significantly
improved. However, further work is needed to make the model more robust and nail the
aesthetics we are looking for. This is where RLHF comes in.

 

Pre-training

![A row of images from the pre-training stage](/blog/flux-krea/pretraining.webp)

SFT

![A row of images from the SFT stage](/blog/flux-krea/sft.webp)

RLHF

![A row of images from the RLHF stage](/blog/flux-krea/rlhf.webp)

During RLHF, we apply a variant of preference optimization technique which we call TPO
to further boost the aesthetics and stylization of our model. We use high quality
internal preference data which has been rigorously filtered to ensure data quality. In
many cases, we applied multiple rounds of preference optimization to further calibrate
the model's outputs.

While exploring various post-training techniques, we discovered a few key findings we
would like to share.

1. 1.

   #### Quality over Quantity

   You need a surprisingly small amount of data (< 1M) to do good post-training.
   Quantity helps with stability and mitigating biases, but the quality of the data
   matters the most. This observation is in line with previous literature that report the
   effectiveness of training on small set of carefully curated data ([[3]](https://arxiv.org/abs/2305.11206),
   [[4]](https://arxiv.org/abs/2309.15807),
   [[5]](https://arxiv.org/abs/2505.19297))

   Our preference labels were carefully collected from labelers who were acutely aware of
   the current model's limitation, areas of improvement, strengths, and weaknesses. In
   particular, we ensured that the images in our preference annotation interface
   contained a diverse set to obtain a focused annotation.
2. 2.

   #### Take an opinionated approach

   There are many open source preference datasets ([[6]](https://arxiv.org/abs/2305.01569),
   [[7]](https://arxiv.org/abs/2304.05977),
   [[8]](https://huggingface.co/blog/image-preferences)) that have been used to benchmark preference finetuning techniques. During
   exploration stages, these datasets were useful for testing various techniques.
   However, we found that training on existing datasets led to unintended behaviors such
   as:

   * Bias towards symmetric, simple composition
   * Blurry and overly soft textures
   * Color palette collapse
   * Regression towards the "AI look"

   It's our belief that a model that has been finetuned on "global" user preference is
   suboptimal. For goals like text rendering, anatomy, structure, and prompt adherence
   where there's an objective ground truth, data diversity and scale are helpful.
   However, for subjective goals such as aesthetics, it's almost adversarial to mix
   different aesthetic tastes together.

   Pre-training is all about mode coverage, post-training is all about mode
   collapsing.

   For example, consider a case where one user loves high fashion photography and another
   user is into minimalist style drawings. Given a focused annotation from the respective
   users, it would be easy to align the model to excel at respective styles. But, when
   you merge the two distributions together, we get a marginal preference distribution
   which is not biased enough to make either party happy. This limitation can be
   partially addressed by prompting, but it's not a satisfactory solution. Most people
   often end up relying on LoRAs to get the level of stylization they want out of the
   model because prompting is insufficient for their use case. Furthermore, users often
   want reasonable defaults without extensive prompting and adding modifiers to get
   aesthetic outputs from the model.

   Global preference will make both parties unsatisfied.

   Motivated by this intuition, we decided to collect our preference data in a very
   opinionated manner which aligns with our aesthetic taste with a clear art direction.
   It's often better and easier to overfit a model towards a certain style.

## Future research directions

As a product-focused company, we focus on building intuitive and delightful user
experiences for interacting with generative models. We see Krea 1 as our first step
to offering a model that meets the aesthetic standard and quality that creatives have
been craving for. With the open release of FLUX.1 Krea [dev], we are excited to see what
the open source community will build on top of it.

We plan to improve core capabilities of the model as well as expanding to more visual
domains to allow our users to explore, blend, and mix diverse set of visuals.

This work was our first step into aesthetics research. We have built a model that to
provide an opinionated aesthetic, but we want to build something that is more personal
and tailored to your sense of aesthetics. In future works, through personalization,
aesthetics, and controllability research, we hope to provide you a model that clicks
with your taste and the ability to refine your work.

## Acknowledgements

We would like to thank the Black Forest Labs team for providing us with their base model
weights. None of this would be possible without their contribution. Additionally, we
thank our data, infrastructure, and product teams, whose hard work was key to building a
foundation for our post-training pipeline.

## Citation

```
@misc{flux1kreadev2025,
  author={Sangwu Lee, Titus Ebbecke, Erwann Millon, Will Beddow, Le Zhuo, Iker García-Ferrero, Liam Esparraguera, Mihai Petrescu, Gian Saß, Gabriel Menezes, Victor Perez},
  title={FLUX.1 Krea [dev]},
  year={2025},
  howpublished={\url{https://github.com/krea-ai/flux-krea}}
}
```

Want to contribute to work like this?   
 Join us — [we're hiring](https://krea.ai/careers)

[Discuss on Hacker News](https://news.ycombinator.com/item?id=44745555)

research

## Read more

[Browse all](/blog)

[![Krea Realtime 14B: Real-Time, Long-Form AI Video Generation](https://s.krea.ai/krea_realtime_14b_cover.webp)

### Krea Realtime 14B: Real-Time, Long-Form AI Video Generation

Oct 15, 2025](/blog/krea-realtime-14b)[![Krea 2 Technical Report](https://s.krea.ai/blog-posts/krea-2-technical-report/agent/1782227962641-krea2-hero-new.jpg)

### Krea 2 Technical Report

Jun 23, 2026](/blog/krea-2-technical-report)[![Krea 2 vs Midjourney: which AI image generator is right for you?](https://optim-images.krea.ai/https---s-krea-ai-yellowrunners-png-1024.webp)

### Krea 2 vs Midjourney: which AI image generator is right for you?

May 15, 2026](/blog/krea-2-vs-midjourney)[![Meet Nano Banana 2, Google's Latest Image Model](https://s.krea.ai/news_nano_banana_2.webp)

### Meet Nano Banana 2, Google's Latest Image Model

Feb 26, 2026](/blog/nano-banana-2)

### Krea

* [Log In](/login)
* [Pricing](/pricing)
* [Enterprise](/enterprise)
* [Models](/models)
* [Download iOS](/download/ios)

### Resources

* [Pricing](/pricing)
* [Careers](/careers)
* [Terms of Service](/terms)
* [Privacy Policy](/privacy)
* [Press](/press)
* [Release Notes](/news/release-notes)
* [API](/features/api)
* [Image Galleries](/feed/search)
* [Documentation](https://docs.krea.ai)

### Solutions

* [Architecture](/architecture)
* [Interior Design](/interior-design)
* [Ecommerce](/ecommerce)
* [Gaming](/gaming)

### About

* [News](/news)
* [Customer Stories](/news/customer-stories)
* [Discord](/discord)
* [Articles](/news/articles)

### All Tools

* [Krea 2](/krea-2)
* [Image](/image)
* [Video](/video)
* [Enhancer](/enhancer)
* [Nano Banana](/nano-banana)
* [Realtime](/realtime)
* [Edit](/edit)
* [Lip Sync](/lipsync)
* [Motion Transfer](/motion-transfer)
* [3D](/3d)

### Models

* [Krea 2](/krea-2)
* [Seedance 2](/models/seedance2)
* [Nano Banana 2](/models/nano-banana-2)
* [Veo 3.1](/models/veo3.1)
* [Krea 1](/models/krea-1)
* [Kling](/models/kling)
* [GPT-IMG-2](/image/gpt-image-2)

### News

* [Company](/news/company)
* [Product](/news/product)
* [Open Source](/news/open-source)
* [Research](/news/research)

© 2026 Krea. All rights reserved.

* [X](https://x.com/krea_ai)
* [LinkedIn](https://linkedin.com/company/krea-ai)
* [Instagram](https://instagram.com/krea_ai)
* [Reddit](https://www.reddit.com/r/krea/)
* [YouTube](https://www.youtube.com/@krea_ai)

 
