# Introducing Stable Cascade — Stability AI
Source: https://stability.ai/news-updates/introducing-stable-cascade
Introducing Stable Cascade — Stability AI



[0](/cart)

Need to prove the ROI on your AI? Try our [calculator.](/roi-calculator)

[Skip to Content](#page)

[![Stability AI](//images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/a3485d53-7e65-42b5-bc62-e2e55f8409b9/stability-ai-white-dot-desktop.png?format=1500w)](/)

[![Stability AI](//images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/8346fca1-a188-450e-8c75-e487e0ff3fae/stability-ai-white-dot-logo-mobile.png?format=1500w)](/)

Models

[Image](/stable-image)

[Video](/stable-video)

[Audio](/stable-audio)

[3D](/stable-3d)

Solutions

[ROI Calculator](/roi-calculator)

[Enterprise Solutions](/solutions)

[Brand Style](/brand-style)

[Product Photography](/productphotography)

[Customer Stories](/customer-stories)

[Brand Studio](/brandstudio)

Deployment

[Brand Studio Plans](/brand-studio-plans)

[Self-Hosted License](/license)

[Platform API](https://platform.stability.ai)

[Cloud Platforms](https://stability.ai/partners)

Insights

[Foundations](/foundations)

[Implementations](/implementations)

[Guides](/guides)

[News](/news-updates)

Company

[Careers](/careers)

[Partners](/partners)

[Research](/research)

[Safety](/safety)

[Board of Directors](/board-of-directors)

[Get in touch](/enterprise)

Open Menu
Close Menu

[![Stability AI](//images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/a3485d53-7e65-42b5-bc62-e2e55f8409b9/stability-ai-white-dot-desktop.png?format=1500w)](/)

[![Stability AI](//images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/8346fca1-a188-450e-8c75-e487e0ff3fae/stability-ai-white-dot-logo-mobile.png?format=1500w)](/)

Models

[Image](/stable-image)

[Video](/stable-video)

[Audio](/stable-audio)

[3D](/stable-3d)

Solutions

[ROI Calculator](/roi-calculator)

[Enterprise Solutions](/solutions)

[Brand Style](/brand-style)

[Product Photography](/productphotography)

[Customer Stories](/customer-stories)

[Brand Studio](/brandstudio)

Deployment

[Brand Studio Plans](/brand-studio-plans)

[Self-Hosted License](/license)

[Platform API](https://platform.stability.ai)

[Cloud Platforms](https://stability.ai/partners)

Insights

[Foundations](/foundations)

[Implementations](/implementations)

[Guides](/guides)

[News](/news-updates)

Company

[Careers](/careers)

[Partners](/partners)

[Research](/research)

[Safety](/safety)

[Board of Directors](/board-of-directors)

[Get in touch](/enterprise)

Open Menu
Close Menu

[Folder:
Models](/Models)

[Folder:
Solutions](/solutions-1)

[Brand Studio](/brandstudio)

[Folder:
Deployment](/deployment)

[Folder:
Insights](/insights)

[News](/news-updates)

[Folder:
Company](/company)

[Get in touch](/enterprise)

[Back](/)

[Image](/stable-image)

[Video](/stable-video)

[Audio](/stable-audio)

[3D](/stable-3d)

[Back](/)

[ROI Calculator](/roi-calculator)

[Enterprise Solutions](/solutions)

[Brand Style](/brand-style)

[Product Photography](/productphotography)

[Customer Stories](/customer-stories)

[Back](/)

[Brand Studio Plans](/brand-studio-plans)

[Self-Hosted License](/license)

[Platform API](https://platform.stability.ai)

[Cloud Platforms](https://stability.ai/partners)

[Back](/)

[Foundations](/foundations)

[Implementations](/implementations)

[Guides](/guides)

[Back](/)

[Careers](/careers)

[Partners](/partners)

[Research](/research)

[Safety](/safety)

[Board of Directors](/board-of-directors)



# Introducing Stable Cascade

[Product](/news-updates/category/Product)

2024年2月12日

Written By [Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

**Key Takeaways:**

* Today we are releasing Stable Cascade in research preview, a new text to image model building upon the [Würstchen](https://openreview.net/forum?id=gU58d5QeGv) architecture. This model is being released under a non-commercial license that permits non-commercial use only.
* Stable Cascade is exceptionally easy to train and finetune on consumer hardware thanks to its three-stage approach.
* In addition to providing checkpoints and inference scripts, we are releasing scripts for finetuning, ControlNet, and LoRA training to enable users further to experiment with this new architecture that can be found on [the Stability GitHub page.](https://github.com/Stability-AI/StableCascade)

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/6b6242aa-4bdc-4cef-9139-8bb69b5baee8/collage_1.jpg)

Today we are launching Stable Cascade in research preview. This innovative text to image model introduces an interesting three-stage approach, setting new benchmarks for quality, flexibility, fine-tuning, and efficiency with a focus on further eliminating hardware barriers. Additionally, we are releasing training and inference code that can be found on the [Stability GitHub page](https://github.com/Stability-AI/StableCascade) to allow further customization of the model & its outputs. The model is available for inference in the [diffusers library](https://huggingface.co/stabilityai/stable-cascade).

**Technical Details**

Stable Cascade differs from our Stable Diffusion lineup of models as it is built on a pipeline comprising three distinct models: Stages A, B, and C. This architecture allows for a hierarchical compression of images, achieving remarkable outputs while utilizing a highly compressed latent space. Let’s look at each stage to understand how they come together:

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/a0a347b4-7a48-4e5a-a8ee-72b3d6798dfa/model-overview.jpg)

The Latent Generator phase, Stage C, transforms the user inputs into compact 24x24 latents that are passed along to the Latent Decoder phase (Stages A & B), which is used to compress images, similar to what the job of the VAE is in Stable Diffusion, but achieving much higher compression.

By decoupling the text-conditional generation (Stage C) from the decoding to the high-resolution pixel space (Stage A & B), we can allow additional training or finetunes, including ControlNets and LoRAs to be completed singularly on Stage C. This comes with a 16x cost reduction compared to training a similar-sized Stable Diffusion model (as shown in the original [paper](https://openreview.net/forum?id=gU58d5QeGv)). Stages A and B can optionally be finetuned for additional control, but this would be comparable to finetuning the VAE in a Stable Diffusion model. For most uses, it will provide minimal additional benefit & we suggest simply training Stage C and using Stages A and B in their original state.

Stages C & B will be released with two different models: 1B & 3.6B parameters for Stage C and 700M & 1.5B parameters for Stage B. It is recommended to use the 3.6B model for Stage C as this model has the highest quality outputs. However, the 1B parameter version can be used for those who want to focus on the lowest hardware requirements. For Stage B, both achieve great results, however, the 1.5 billion excels at reconstructing fine details. Thanks to Stable Cascade’s modular approach, the expected VRAM requirements for inference can be kept to approximately 20gb but can be further lowered by using the smaller variants (as mentioned before, this may also decrease the final output quality).

**Comparison**

During our evaluations, we found Stable Cascade performs best in both prompt alignment and aesthetic quality in almost all model comparisons. The figures show the results from a human evaluation using a mix of [parti-prompts](https://huggingface.co/datasets/nateraw/parti-prompts) and aesthetic prompts:

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/f14ebda4-fb1f-4098-8dd2-284e2877e499/comparison.png)

*The above image compares Stable Cascade (30 inference steps) against Playground v2 (50 inference steps), SDXL (50 inference steps), SDXL Turbo (1 inference step) and Würstchen v2 (30 inference steps).*

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/b3f21470-721c-4d89-86b0-2f26cce3cb65/comparison-inference--speed.png)

*The above image demonstrates the differences in inference speed between   
Stable Cascade, SDXL, Playground v2, and SDXL Turbo*

Stable Cascade´s focus on efficiency is evidenced through its architecture and higher compressed latent space. Despite the largest model containing 1.4 billion parameters more than Stable Diffusion XL, it still features faster inference times, as seen in the figure below.

**Additional Features**

Next to standard text-to-image generation, Stable Cascade can generate image variations and image-to-image generations.

Image variations work by extracting image embeddings from a given image using CLIP and then returning this back to the model. Below you can see some example outputs. The left image shows the original, while the four to its right are the variations generated.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/f91afc43-d8f7-4e60-8d8e-2c535ff0c32c/variations-headset.jpg)

Image-to-image works by simply adding noise to a given image and then using this as a starting point for the generation. Here is an example for noising the left image and then running the generation from there.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/545729e9-833e-440f-8846-0d98ef9d347f/image-to-image-rodent.jpg)

**Code for Training, Finetuning, ControlNet and LoRA**

With the release of Stable Cascade, we are releasing all the code for training, finetuning, ControlNet, and LoRA to lower the requirements to experiment with this architecture further. Here are some of the ControlNets we will be releasing with the model:

**Inpainting / Outpainting:** Input an image paired with a mask to accompany a text prompt. The model will then fill the masked part of the image by following the text prompt provided.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/b970f01f-2e44-420b-8686-b87db1b8977c/Cascade_Masking.png)

**Canny Edge:** Generate a new image by following the edges of an existing image input to the model. From our testing, it can also expand upon sketches.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/2a82cc7c-f030-40d8-9777-9c1d1d128582/Examples.png)

*In the above image, the top sketches are input into the model to produce the outputs on the bottom.*

**2x Super Resolution:** Upscale an image to 2x its side (for example, turning a 1024 x 1024 image into a 2048x2048 output) and can also be used on latents generated by Stage C.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/f71c9e4f-59bf-49fb-99b1-f12776dbc63c/controlnet-sr.jpg)

The details for these can be found on the [Stability GitHub page](https://github.com/Stability-AI/StableCascade), including the training and inference code.

While this model is not currently available for commercial purposes, if you’d like to explore using one of our other image models for commercial use, please visit our [Stability AI Membership page](https://stability.ai/membership) for self-hosted commercial use or our [Developer Platform](https://platform.stability.ai/) to access our API.

To stay updated on our progress follow us on [Twitter](https://twitter.com/stabilityai), [Instagram](https://www.instagram.com/stability.ai/), [LinkedIn](https://www.linkedin.com/company/66318622/), and join our [Discord Community](https://discord.gg/stablediffusion).

[Image](/news-updates/tag/Image)

[![](https://images.squarespace-cdn.com/content/v2/namespaces/memberAccountAvatars/libraries/65ce473bcf080c7b53f8635b/df7b967d-6590-4357-a3b9-f35aeecf00f2/thirdPartyMemberAvatar-65ce473bcf080c7b53f8635b-70a9c56b-d2c3-4bf1-8075-c60686f043c0?format=300w)
Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

[Previous

Previous

## Stability AI Partners with Jasper in Divestment of Init ML](/news-updates/init-ml-divestment)
[Next

Next

## Stability AI Joins U.S. Artificial Intelligence Safety Institute Consortium](/news-updates/stability-ai-joins-us-artificial-intelligence-safety-institute-consortium)



![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/4e38b1d7-350c-4fd8-ac08-114a3448f110/Stability-ai-logo-white-dot.png)

Stability AI is unlocking the power of open-source generative AI to expand human creativity. We build world-class models that are accessible, adaptable, and designed to empower creators, developers, and enterprises everywhere.

#### Company

[Board of Directors](/board-of-directors)

[Partners](/partners)

[Safety](/safety)

[Research](/research)

[Careers](/careers)

[News](/news)

[Brand Resources](https://drive.google.com/file/d/1Kuq2SZhSnEwGjqsGy8fYaI0LA6KNfQhu/view?usp=sharing)

#### Models

[Image](/stable-image)

[Video](/stable-video)

[Audio](/stable-audio)

[3D](/stable-3d)

#### Deployment

[Stability AI License](/license)

[Community License Agreement](/community-license-agreement)

[Platform API](https://platform.stability.ai/?_gl=1*1c3kyrj*_gcl_au*NjI1NTE2NzgyLjE3NTEwNjA1MjY.*_ga*ODk2ODYxMzU1LjE3NTA4NzcyMzQ.*_ga_W4CMY55YQZ*czE3NTIyMDAwMTgkbzIzJGcxJHQxNzUyMjAwNjYxJGo2MCRsMCRoMA..)

[Cloud Platforms](/partners)

#### ResourceS

[Learning Hub](/learning-hub)

[Customer Stories](/customer-stories)

#### Contact Us

[press@stability.ai](mailto:mailto:press@stability.ai?)

[partners@stability.ai](mailto:mailto:partners@stability.ai?)

[Submit a Support Request](https://kb.stability.ai/knowledge-base/kb-tickets/new)

#### Legal

[Acceptable Use Policy](/use-policy)

[Privacy Policy](/privacypolicy)

[Terms of Service](/terms-of-service)

[Trust Center](https://trust.stability.ai/)

[Your Privacy Choices](#)

#### Applications

[Brand Studio](/brandstudio)

[Stable Audio](https://stableaudio.com/)

#### Join the Mailing List

Email\*

Which of our products or services are you interested in?\*

Please SelectEnterprise solutionsGamingImage generation & editingAudio generation & editing3D/4D modelsVideo modelsDream StudioPartnership opportunities

© Stability AI Ltd, 2026









By clicking “Accept All Cookies”, you agree to our use of cookies. We use cookies to provide you with a great experience and to help our website run effectively.

Cookies Settings

Reject All Accept All Cookies

![Company Logo](https://cdn-ukwest.onetrust.com/logos/a1c661f2-0124-4ece-a7a6-c61ba980d61d/0196b02b-6810-7729-9655-031e350cc595/93ab96cb-52dc-4418-bf5c-5f55229429f4/StabilityAi_Logo_White-19.png)

## Privacy Preference Center

When you visit any website, it may store or retrieve information on your browser, mostly in the form of cookies. This information might be about you, your preferences or your device and is mostly used to make the site work as you expect it to. The information does not usually directly identify you, but it can give you a more personalized web experience. Because we respect your right to privacy, you can choose not to allow some types of cookies. Click on the different category headings to find out more and change our default settings. However, blocking some types of cookies may impact your experience of the site and the services we are able to offer.
  
[More information](https://cookiepedia.co.uk/giving-consent-to-cookies)

Allow All

### Manage Consent Preferences

#### Strictly Necessary Cookies

Always Active

These cookies are necessary for the website to function and cannot be switched off in our systems. They are usually only set in response to actions made by you which amount to a request for services, such as setting your privacy preferences, logging in or filling in forms. You can set your browser to block or alert you about these cookies, but some parts of the site will not then work. These cookies do not store any personally identifiable information.

#### Advertising Cookies

Advertising Cookies

These cookies may be set through our site by our advertising partners. They may be used by those companies to build a profile of your interests and show you relevant adverts on other sites. They do not store directly personal information, but are based on uniquely identifying your browser and internet device. If you do not allow these cookies, you will experience less targeted advertising.

#### Analytics Cookies

Analytics Cookies

These cookies allow us to count visits and traffic sources so we can measure and improve the performance of our site. They help us to know which pages are the most and least popular and see how visitors move around the site. All information these cookies collect is aggregated and therefore anonymous. If you do not allow these cookies we will not know when you have visited our site, and will not be able to monitor its performance.

### Cookie List

Clear

checkbox label label

Apply Cancel

Consent Leg.Interest

checkbox label label

checkbox label label

checkbox label label

Reject All Confirm My Choices

[![Powered by Onetrust](https://cdn-ukwest.onetrust.com/logos/static/powered_by_logo.svg "Powered by OneTrust Opens in a new Tab")](https://www.onetrust.com/products/cookie-consent/)
