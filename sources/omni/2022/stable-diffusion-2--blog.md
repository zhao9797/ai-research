# Stable Diffusion 2.0 Release — Stability AI
Source: https://stability.ai/news-updates/stable-diffusion-v2-release
Stable Diffusion 2.0 Release — Stability AI



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



# Stable Diffusion 2.0 Release

[Product](/news-updates/category/Product)

2022年11月24日

Written By [Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

![a generated photo overlooking a lush green valley](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1669252301642-3VO8GC81VMRDDVMATA5I/overllooking-a-green-valley.jpg)

We are pleased to announce the open-source release of [Stable Diffusion Version 2](https://github.com/Stability-AI/stablediffusion).

The original [Stable Diffusion V1](https://github.com/CompVis/stable-diffusion) led by [CompVis](https://ommer-lab.com) changed the nature of open source AI models and spawned hundreds of other models and innovations worldwide. It had one of the fastest climbs to 10K GitHub stars of any software, rocketing through 33K stars in less than two months.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/5e7ed637-5a94-4c22-aaf3-eb774a33145a/Stability+AI+Stable+Diffusion+Develop+Adoption+Github+Graph.jpg)

*Source:* [*A16z and Github*](https://a16z.com/2022/11/16/creativity-as-an-app/)

The dynamic team of Robin Rombach ([Stability AI](https://stability-ai.squarespace.com)) and Patrick Esser ([Runway ML](https://runwayml.com/)) from the [CompVis Group at LMU Munich](https://ommer-lab.com), headed by [Prof. Dr. Björn Ommer](https://ommer-lab.com/people/ommer/), led the original Stable Diffusion V1 release. They built on their prior work in the lab with [Latent Diffusion Models](https://arxiv.org/abs/2112.10752) and got critical support from [LAION](https://laion.ai/) and [Eleuther AI](https://eleuther.ai). In our earlier blog post, you can read more about the original Stable Diffusion V1 release. Robin is now leading the effort with Katherine Crowson at Stability AI to create the next generation of media models with our broader team.

Stable Diffusion 2.0 delivers several big improvements and features versus the original V1 release, so let’s dive in and take a look at them.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/80bc20a8-cdd4-457b-a7b7-c83d7d7586bf/Stability+AI+Stable+Diffusion+Astronaut+Feeding+Chickens.jpg)

#### **New Text-to-Image Diffusion Models**

The Stable Diffusion 2.0 release includes robust text-to-image models trained using a brand new text encoder (OpenCLIP), developed by LAION with support from Stability AI, which greatly improves the quality of the generated images compared to earlier V1 releases. The text-to-image models in this release can generate images with default resolutions of 512x512 pixels and 768x768 pixels.

These models are trained on an aesthetic subset of the [LAION-5B](https://laion.ai/blog/laion-5b/) dataset created by the DeepFloyd team at Stability AI, which is then further filtered to remove adult content using LAION’s [NSFW filter](https://openreview.net/forum?id=M3Y74vmsMcY).

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/0fbc90e8-e1ce-4812-9c70-2fcbb48ba9f9/Stability+AI+Stable+Diffusion+Example+Images.jpg)

*Examples of images produced using Stable Diffusion 2.0, at 768x768 image resolution.*

#### **Super-resolution Upscaler Diffusion Models**

Stable Diffusion 2.0 also includes an Upscaler Diffusion model that enhances the resolution of images by a factor of 4. Below is an example of our model upscaling a low-resolution generated image (128x128) into a higher-resolution image (512x512). Combined with our text-to-image models, Stable Diffusion 2.0 can generate images with resolutions of 2048x2048–or even higher.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/b1b98b60-f0a1-4b2d-9cd6-da915057d5ad/Stability+AI+Stable+Diffusion+LowRes-SuperRes.jpg)

*Left: 128x128 low-resolution image. Right: 512x512 resolution image produced by Upscaler.*

#### **Depth-to-Image Diffusion Model**

Our new *depth-guided* stable diffusion model, called *depth2img*, extends the previous image-to-image feature from V1 with brand-new possibilities for creative applications. *Depth2img* infers the depth of an input image (using an existing [model](https://github.com/isl-org/MiDaS)) and then generates new images using both the text and depth information.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/3d0d3b3f-94ca-43eb-bb4d-79af0f4d10ac/Stability+AI+Stable+Diffusion+V2+Depth2Img.jpg)

*The input image (left) can produce several new images (right). This new model can be used for structure-preserving image-to-image and shape-conditional image synthesis.*

Depth-to-Image can offer all sorts of new creative applications, delivering transformations that look radically different from the original but which still preserve the coherence and depth of that image:

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/01b5f8a8-7568-4c43-91bf-2f1764d264b9/d2i.gif)

*Depth-to-Image preserves coherence.*

#### **Updated Inpainting Diffusion Model**

We also include a new text-guided inpainting model, fine-tuned on the new Stable Diffusion 2.0 base text-to-image, which makes it super easy to switch out parts of an image intelligently and quickly.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/86d2d10c-c67e-416b-9b24-d923586f06b2/inpainting.gif)

*The updated inpainting model fine-tuned on Stable Diffusion 2.0 text-to-image model.*

Just like the first iteration of Stable Diffusion, we’ve worked hard to optimize the model to run on a single GPU–we wanted to make it accessible to as many people as possible from the very start. We’ve already seen that when millions of people get their hands on these models, they collectively create truly amazing things. This is the power of open source: tapping the vast potential of millions of talented people who might not have the resources to train a state-of-the-art model but who have the ability to do something incredible with one.

This new release, along with its powerful new features like *depth2img* and higher resolution upscaling capabilities, will serve as the foundation of countless applications and enable an explosion of new creative potential.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/87a90323-28d8-4b24-9c5e-a577462d044f/Stability+AI+Stable+Diffusion+Furby.jpg)

For more details about accessing the model, please check out the release notes on our GitHub: [https://github.com/Stability-AI/StableDiffusion](https://github.com/Stability-AI/stablediffusion)

We will offer active support to this repository as our direct contribution to open source AI and look forward to all the amazing things you all build on it.

*We are releasing these models into the Stability AI API Platform (*[*platform.stability.ai*](https://platform.stability.ai)*) and* [*DreamStudio*](https://beta.dreamstudio.ai)*in the next few days. We will send an update with information for developers and partners, including pricing updates. We hope you all enjoy these updates!*

---

*We are hiring researchers and engineers who are excited to work on the next generation of open source Generative AI models! If you’re interested in joining Stability AI, please contact* [*careers@stability.ai*](mailto:careers@stability.ai)*, with your CV and a short statement about yourself.*

[![](https://images.squarespace-cdn.com/content/v2/namespaces/memberAccountAvatars/libraries/65ce473bcf080c7b53f8635b/df7b967d-6590-4357-a3b9-f35aeecf00f2/thirdPartyMemberAvatar-65ce473bcf080c7b53f8635b-70a9c56b-d2c3-4bf1-8075-c60686f043c0?format=300w)
Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

[Previous

Previous

## DreamStudio beta Updates 1-Dec 22](/news-updates/dreamstudio-update-1-dec-2022)
[Next

Next

## Stability’s API Platform](/news-updates/api-platform-for-stability-ai)



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
