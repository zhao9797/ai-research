# Introducing FLUX.1 Tools - Black Forest Labs
Source: https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-1-tools/
Introducing FLUX.1 Tools - Black Forest Labs



The Wayback Machine - https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-1-tools/

[Skip to content](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-1-tools/#wp--skip-link--target)

[![Black Forest Labs](https://web.archive.org/web/20250109131320im_/https://blackforestlabs.ai/wp-content/uploads/2024/07/bfl_logo_retraced_blk.png)](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/)

* our models.
  + [FLUX Tools](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/)
  + [FLUX 1.1 PRO Ultra / Raw](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/ultra-home)
* [announcements.](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/announcements/)
* [what’s next.](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/up-next/)
* [careers.](https://web.archive.org/web/20250109131320/https://job-boards.greenhouse.io/blackforestlabs)
* [api.](https://web.archive.org/web/20250109131320/https://docs.bfl.ml/)
* [contact.](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/contact/)



![](https://web.archive.org/web/20250109131320im_/https://blackforestlabs.ai/wp-content/uploads/2024/11/sample-1-scaled.jpeg)

# Introducing FLUX.1 Tools

[Nov 21, 2024](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-1-tools/)

—

by

[BlackForestLabs](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/author/blackforestlabs/)

in [News.](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/category/news/)

Today, we are excited to release *FLUX.1 Tools*, a suite of models designed to add control and steerability to our base text-to-image model FLUX.1, enabling the modification and re-creation of real and generated images. At release, *FLUX.1 Tools* consists of four distinct features that will be available as open-access models within the FLUX.1 [dev] model series, and in the BFL API supplementing FLUX.1 [pro]:

* **FLUX.1 Fill:** State-of-the-art inpainting and outpainting models, enabling editing and expansion of real and generated images given a text description and a binary mask.
* **FLUX.1 Depth:** Models trained to enable structural guidance based on a depth map extracted from an input image and a text prompt.
* **FLUX.1 Canny:** Models trained to enable structural guidance based on canny edges extracted from an input image and a text prompt.
* **FLUX.1 Redux:** An adapter that allows mixing and recreating input images and text prompts.

This release reinforces our dual commitment: delivering cutting-edge open-weight models for the research community while offering best-in-class capabilities through our API. We release each tool in the BFL API as **FLUX.1 [pro]** variants and with inference code and weights available as guidance-distilled, open-access **FLUX.1 [dev]**variants. Additionally, we are excited that our released models will be available via our partners [fal.ai](https://web.archive.org/web/20250109131320/https://fal.ai/models?keywords=flux), [Replicate](https://web.archive.org/web/20250109131320/https://replicate.com/collections/flux),[Together.ai,](https://web.archive.org/web/20250109131320/https://www.together.ai/blog/flux-tools-models-together-apis-canny-depth-image-generation?utm_source=bfl&utm_medium=blog-post&utm_campaign=flux-tools) [Freepik](https://web.archive.org/web/20250109131320/https://www.freepik.com/ai/image-generator) and [krea.ai](https://web.archive.org/web/20250109131320/https://www.krea.ai/apps/image/flux).

The following sections contain details on the new models, analyses on their performance and how they can be accessed. We are excited to see how the vibrant Flux ecosystem will be supplemented by our new tools.

## **Inpainting and Outpainting with FLUX.1 Fill**

FLUX.1 Fill introduces advanced **inpainting** capabilities that surpass existing tools like Ideogram 2.0 and popular open-source variants such as AlimamaCreative’s [FLUX-Controlnet-Inpainting](https://web.archive.org/web/20250109131320/https://github.com/alimama-creative/FLUX-Controlnet-Inpainting). It allows for seamless edits that integrate naturally with existing images.

![](https://web.archive.org/web/20250109131320im_/https://lh7-rt.googleusercontent.com/docsz/AD_4nXfM84Nir6HIU1xcJeNOolz7ZH7SIYTBudA0jeM2EQJb0LHoJMOZR17PAwf43peoFydja_z_j83LAYVMRL5gry5QF-q-Cm-SQG_iwhJcH7m8Sg1yXrQTi2JYjJQEQfLm5F30_fCnYQ?key=Ult89JQdBB7CX3l5ClfyS9B_)

Additionally, FLUX.1 Fill supports **outpainting**, enabling the user to extend images beyond their original borders.

![](https://web.archive.org/web/20250109131320im_/https://lh7-rt.googleusercontent.com/docsz/AD_4nXdN_mwhw6xp3EmgDgHqo5zchmEY0TaRznhrwyaHn8Qxz5kvdA5q7OnKsoeeyPWMWUTXD1DfhJ-6X1hDGMDqxR1nspxBNB8pCjb4IKLEMkdUKBgn-kaTOXx6rgWfZk-HgkjaFvjBsw?key=Ult89JQdBB7CX3l5ClfyS9B_)

We conduct a benchmark, publicly available [here](https://web.archive.org/web/20250109131320/https://drive.google.com/file/d/1y4CyrvBgy_QXRc7BllYTCyv0PnHb7xeX/view?usp=sharing). The results show that Flux.1 Fill [pro] outperforms all other competing methods, making it the state-of-the-art inpainting model to date. Second is Flux.1 Fill [dev], outperforming proprietary solutions while being more efficient at inference.

![](https://web.archive.org/web/20250109131320im_/https://blackforestlabs.ai/wp-content/uploads/2024/11/elo_bar_plot_fill-1024x768.png)

*Flux.1 Fill [dev] is available under the Flux Dev License, with*

* *Full model weights available on Hugging Face: [[**Fill**](https://web.archive.org/web/20250109131320/https://huggingface.co/black-forest-labs/FLUX.1-Fill-dev)]*
* *Inference code available on [**GitHub**](https://web.archive.org/web/20250109131320/https://github.com/black-forest-labs/flux)*

*Flux.1 Fill [pro]* is available in the [**[BFL API**](https://web.archive.org/web/20250109131320/https://docs.bfl.ml/)]

## **Structural Conditioning with FLUX.1 Canny / Depth**

Structural conditioning uses canny edge or depth detection to maintain precise control during image transformations. By preserving the original image’s structure through edge or depth maps, users can make text-guided edits while keeping the core composition intact. This is particularly effective for retexturing images.

![](https://web.archive.org/web/20250109131320im_/https://lh7-rt.googleusercontent.com/docsz/AD_4nXe065BZ3q1xRcnpFUxUQ7YTkjOrery_E2Mgo94buBKFKlV8w8p0CCYyB89Ya1A_ePiH1i9KxjzE6bLnoFf1nasWzFH-dIhChPv5jdig5alqBdeUPeS1RBRMyPFEx2qCwA7AVqHepg?key=Ult89JQdBB7CX3l5ClfyS9B_)
![](https://web.archive.org/web/20250109131320im_/https://lh7-rt.googleusercontent.com/docsz/AD_4nXd9F-aIYKft6az72jM9X1DZl7WNkxNxLepuUe9rGhNAZCPVGIWN8RR10oq-CgsYGkN3tcuIUnGAGubHj6aPsSgb8547iOXHB_9s4J_o-xITJ0P90f2Z4Hlu0L6hkAJ4jK2TUZk9fg?key=Ult89JQdBB7CX3l5ClfyS9B_)

In our evaluations, benchmark available [here](https://web.archive.org/web/20250109131320/https://drive.google.com/file/d/1DFfhOSrTlKfvBFLcD2vAALwwH4jSGdGk/view?usp=sharing), *FLUX.1 Depth* outperforms proprietary models like *Midjourney ReTexture*. In particular, *FLUX.1 Depth [pro]* offers higher output diversity, while the Dev version of *FLUX.1 Depth* delivers more consistent results in depth-aware tasks. For canny edge models, benchmark [here](https://web.archive.org/web/20250109131320/https://drive.google.com/file/d/1dRoxOL-vy3tSAesyqBSJoUWsbkMwv3en/view?usp=sharing),  *FLUX.1 Canny [pro]* is the best in class, followed by *FLUX.1 Canny [dev].*

![](https://web.archive.org/web/20250109131320im_/https://blackforestlabs.ai/wp-content/uploads/2024/11/elo_bar_plot_depth-canny-1024x384.png)

FLUX.1 Canny / Depth are available in two versions: full models for maximum performance, and LoRA versions based on FLUX.1 [dev] for easier development.

Flux Depth / Canny [dev] are available under the Flux Dev License with

* Full model weights available on Hugging Face: [[**Depth**]](https://web.archive.org/web/20250109131320/https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev) [[**Canny**]](https://web.archive.org/web/20250109131320/https://huggingface.co/black-forest-labs/FLUX.1-Canny-dev)
* LoRA weights available on Hugging Face: [[**Depth**]](https://web.archive.org/web/20250109131320/https://huggingface.co/black-forest-labs/FLUX.1-Depth-dev-lora) [[**Canny**]](https://web.archive.org/web/20250109131320/https://huggingface.co/black-forest-labs/FLUX.1-Canny-dev-lora)
* Inference code available on [**GitHub**](https://web.archive.org/web/20250109131320/https://github.com/black-forest-labs/flux)

Flux.1 Depth / Canny [pro] are available in the [**BFL API.**](https://web.archive.org/web/20250109131320/https://docs.bfl.ml/)

## **Image Variation and Restyling** with **FLUX.1 Redux**

FLUX.1 Redux is an adapter for all FLUX.1 base models for image variation generation. Given an input image, FLUX.1 Redux can reproduce the image with slight variation, allowing to refine a given image.

![](https://web.archive.org/web/20250109131320im_/https://lh7-rt.googleusercontent.com/docsz/AD_4nXcO4QZZqolpRS2lTXSqJ8uJcTY9yXwiXhYAypw3d1yIqYnpLUFz4KWw5hUJisrH_nTqMalYQal0iUZPuFv0h6mGmIlq9CGNA-4a6A5tm9TUh5gNs1dmE7js2ayudgF_IN2BPXkrOQ?key=Ult89JQdBB7CX3l5ClfyS9B_)

It naturally integrates into more complex workflows unlocking image restyling via prompt. Restyling is available through our API by providing an image plus a prompt. The feature is supported in our latest model *FLUX1.1 [pro] Ultra*, allowing for combining input images and text prompts to create high-quality 4-megapixel outputs with flexible aspect ratios.

![](https://web.archive.org/web/20250109131320im_/https://blackforestlabs.ai/wp-content/uploads/2024/11/image298-3-7-5-1024x393.png)

Our [benchmark](https://web.archive.org/web/20250109131320/https://drive.google.com/file/d/1rqbyUjXqYatn2oMqkdjHCLfbsKMsjBla/view?usp=sharing) demonstrates that FLUX.1 Redux achieves state-of-the-art performance in image variation.

![](https://web.archive.org/web/20250109131320im_/https://blackforestlabs.ai/wp-content/uploads/2024/11/elo_bar_plot_redux-1024x768.png)

Flux.1 Redux [dev] is available under the Flux Dev License with

* Model weights available on Hugging Face: [[**Redux**](https://web.archive.org/web/20250109131320/https://huggingface.co/black-forest-labs/FLUX.1-Redux-dev)]
* Inference code available on [**GitHub**](https://web.archive.org/web/20250109131320/https://github.com/black-forest-labs/flux)

Flux.1 Redux supporting FLUX1.1 [pro] Ultra is available in the [**BFL API.**](https://web.archive.org/web/20250109131320/https://docs.bfl.ml/)

We’re excited to see what the community is going to build with our new set of tools. Try our API at [[api.bfl.m](https://web.archive.org/web/20250109131320/http://api.bfl.ml/)l].

---



←[Previous:  Introducing FLUX1.1 [pro] Ultra and Raw Modes](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-1-1-ultra/)

[Next:  Bringing Lightning-Fast FLUX Performance to More Creators in Collaboration with NVIDIA](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/flux-nvidia-blackwell/)→



* [Impressum](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/impressum/)
* [Terms of Service](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/terms-of-service/)
* [Privacy Policy](https://web.archive.org/web/20250109131320/https://blackforestlabs.ai/privacy-policy/)

![](https://web.archive.org/web/20250109131217/https://pixel.wp.com/g.gif?v=ext&blog=235585371&post=1700&tz=0&srv=blackforestlabs.ai&j=1%3A13.7.1&host=blackforestlabs.ai&ref=&fcp=18000&rand=0.382445987654321)
