# Introducing SDXL Turbo: A Real-Time Text-to-Image Generation Model — Stability AI
Source: https://stability.ai/news-updates/stability-ai-sdxl-turbo
Introducing SDXL Turbo: A Real-Time Text-to-Image Generation Model — Stability AI



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



# Introducing SDXL Turbo: A Real-Time Text-to-Image Generation Model

[Product](/news-updates/category/Product)

2023年11月29日

Written By [Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

**Key Takeaways:**

* SDXL Turbo achieves state-of-the-art performance with a new distillation technology, enabling single-step image generation with unprecedented quality, reducing the required step count from 50 to just one.
* See our [research paper](https://stability.ai/research/adversarial-diffusion-distillation) for specific technical details regarding the model’s new distillation technique that leverages a combination of adversarial training and score distillation.
* Download the model weights and code on [Hugging Face](https://huggingface.co/stabilityai/sdxl-turbo), currently being released under a non-commercial research license that permits personal, non-commercial use.
* Test SDXL Turbo on Stability AI’s image editing platform [Clipdrop](http://clipdrop.co/stable-diffusion-turbo), with a beta demonstration of the real-time text-to-image generation capabilities.

Today, we are releasing SDXL Turbo, a new text-to-image mode. SDXL Turbo is based on a novel distillation technique called Adversarial Diffusion Distillation (ADD), which enables the model to synthesize image outputs in a single step and generate real-time text-to-image outputs while maintaining high sampling fidelity. For researchers and enthusiasts interested in technical details, our research paper is available [here](https://stability.ai/research/adversarial-diffusion-distillation). It's important to note that SDXL Turbo is not yet intended for commercial use.

**Advantages of Adversarial Diffusion Distillation**

Featuring new advancements in diffusion model technologies, SDXL Turbo iterates on the foundation of SDXL 1.0 and implements a new distillation technique for text-to-image models: Adversarial Diffusion Distillation. By incorporating ADD, SDXL Turbo gains many advantages shared with GANs (Generative Adversarial Networks), such as single-step image outputs, while avoiding artifacts or blurriness often observed in other distillation methods. The SDXL Turbo research paper detailing this model’s new distillation technique is available [here](https://stability.ai/research/adversarial-diffusion-distillation).

**Performance Benefits Compared to Other Diffusion Models**

To make the selection for SDXL Turbo, we compared multiple different model variants (StyleGAN-T++, OpenMUSE, IF-XL, SDXL, and LCM-XL) by generating outputs with the same prompt. Human evaluators were then shown two outputs at random and tasked to pick the output that most closely followed the direction of the prompt. Next, an additional test was completed with the same method for image quality. In these blind tests, SDXL Turbo was able to beat a 4-step configuration of LCM-XL with a single step, as well as beating a 50-step configuration of SDXL with only 4 steps. With these results, we can see SDXL Turbo outperforming a state-of-the-art multi-step model with substantially lower computational requirements without sacrificing image quality.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/03adefa4-b2d6-41c3-975c-3a05c03b8a6c/turbo_comparing.jpg)

Additionally, SDXL Turbo provides major improvements to inference speed. On an A100, SDXL Turbo generates a 512x512 image in 207ms (prompt encoding + a single denoising step + decoding, fp16), where 67ms are accounted for by a single UNet forward evaluation.

**Explore SDXL Turbo with Clipdrop**

To test the capabilities of this new model, visit Stability AI's image editing platform, [Clipdrop,](http://clipdrop.co/stable-diffusion-turbo) for a beta demonstration of SDXL Turbo's real-time image generation. It's compatible with most browsers and is currently available to try for free.

**Commercial Applications**

If you want to use this model for your commercial products or purposes, please contact us [here](https://stability.ai/contact) to learn more.

You can also stay updated on our progress by signing up for our [newsletter](https://stability.ai/home#newsletter), following us on [Twitter](https://twitter.com/stabilityai), [Instagram](https://www.instagram.com/stability.ai/), [LinkedIn](https://www.linkedin.com/company/stability-ai), and joining our [Discord Community](https://discord.gg/stablediffusion).

[Image](/news-updates/tag/Image)

[![](https://images.squarespace-cdn.com/content/v2/namespaces/memberAccountAvatars/libraries/65ce473bcf080c7b53f8635b/df7b967d-6590-4357-a3b9-f35aeecf00f2/thirdPartyMemberAvatar-65ce473bcf080c7b53f8635b-70a9c56b-d2c3-4bf1-8075-c60686f043c0?format=300w)
Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

[Previous

Previous

## Statement to the U.S. Senate AI Insight Forum on Transparency, Explainability, and Copyright](/news-updates/copyright-us-senate-open-ai-transparency)
[Next

Next

## Introducing Stable Video Diffusion](/news-updates/stable-video-diffusion-open-ai-video-model)



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
