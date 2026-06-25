# Stable Diffusion 3: Research Paper — Stability AI
Source: https://stability.ai/news-updates/stable-diffusion-3-research-paper
Stable Diffusion 3: Research Paper — Stability AI



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



# Stable Diffusion 3: Research Paper

[Research](/news-updates/category/Research)

2024年3月5日

Written By [Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

### **Key Takeaways**

* Today, we’re publishing our [research paper](https://arxiv.org/pdf/2403.03206.pdf) that dives into the underlying technology powering Stable Diffusion 3.
* Stable Diffusion 3 outperforms state-of-the-art text-to-image generation systems such as DALL·E 3, Midjourney v6, and Ideogram v1 in typography and prompt adherence, based on human preference evaluations.
* Our new Multimodal Diffusion Transformer (MMDiT) architecture uses separate sets of weights for image and language representations, which improves text understanding and spelling capabilities compared to previous versions of Stable Diffusion.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/50a6aa56-9b9c-4dec-9efc-8a159c7c8422/Blog+SD3+Research+Paper.png)

Following our announcement of the [early preview of Stable Diffusion 3](https://stability.ai/news/stable-diffusion-3), today we are publishing the [research paper](https://arxiv.org/pdf/2403.03206.pdf) which outlines the technical details of our upcoming model release. The paper will be accessible on arXiv soon, and we invite you to sign up for [the waitlist](https://stability.ai/stablediffusion3) to participate in the early preview.

### Performance

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/19acc961-3e42-413f-b495-450803aba582/baseline_comp.jpg)

*With SD3 as a baseline, this chart outlines the areas it wins against competing models based on human evaluations of Visual Aesthetics, Prompt Following, and Typography.*

We have compared output images from Stable Diffusion 3 with various other open models including [SDXL](https://stability.ai/news/stable-diffusion-sdxl-1-announcement), [SDXL Turbo](https://stability.ai/news/stability-ai-sdxl-turbo), [Stable Cascade](https://stability.ai/news/introducing-stable-cascade), Playground v2.5 and Pixart-α as well as closed-source systems such as DALL·E 3, Midjourney v6 and Ideogram v1 to evaluate performance based on human feedback. During these tests, human evaluators were provided with example outputs from each model and asked to select the best results based on how closely the model outputs follow the context of the prompt it was given (“prompt following”), how well text was rendered based on the prompt (“typography”) and, which image is of higher aesthetic quality (“visual aesthetics”).

From the results of our testing, we have found that Stable Diffusion 3 is equal to or outperforms current state-of-the-art text-to-image generation systems in all of the above areas.

In early, unoptimized inference tests on consumer hardware our largest SD3 model with 8B parameters fits into the 24GB VRAM of a RTX 4090 and takes 34 seconds to generate an image of resolution 1024x1024 when using 50 sampling steps. Additionally, there will be multiple variations of Stable Diffusion 3 during the initial release, ranging from 800m to 8B parameter models to further eliminate hardware barriers.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/12973f20-3043-4184-b4f7-a0f182022fb6/Blog+SD3+GPUs+go+brrrrrrr.png)

### Architecture Details

For text-to-image generation, our model has to take both modalities, text and images, into account. This is why we call this new architecture MMDiT, a reference to its ability to process multiple modalities. As in previous versions of Stable Diffusion, we use pretrained models to derive suitable text and image representations. Specifically, we use three different text embedders - two CLIP models and T5 - to encode text representations, and an improved autoencoding model to encode image tokens.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/2b5df5af-5b84-40d5-8fc0-c8618c22488c/simplemmdit2.png)

*Conceptual visualization of a block of our modified multimodal diffusion transformer: MMDiT.*

The SD3 architecture builds upon the [Diffusion Transformer (“DiT”, Peebles & Xie, 2023)](https://arxiv.org/abs/2212.09748). Since text and image embeddings are conceptually quite different, we use two separate sets of weights for the two modalities. As shown in the above figure, this is equivalent to having two independent transformers for each modality, but joining the sequences of the two modalities for the attention operation, such that both representations can work in their own space yet take the other one into account.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/c1835fc8-892c-4c5b-94bf-eedda9fa967a/blog_plot_combo.png)

*Our novel MMDiT architecture outperforms established text-to-image backbones such as* [*UViT (Hoogeboom et al, 2023)*](https://arxiv.org/abs/2301.11093) *and* [*DiT (Peebles & Xie, 2023)*](https://arxiv.org/abs/2212.09748)*, when measuring visual fidelity and text alignment over the course of training.*

By using this approach, information is allowed to flow between image and text tokens to improve overall comprehension and typography within the outputs generated. This architecture is also easily extendable to multiple modalities such as video, as we discuss in our [paper](https://arxiv.org/pdf/2403.03206.pdf)[.](https://stabilityai-public-packages.s3.us-west-2.amazonaws.com/Stable+Diffusion+3+Paper.pdf)

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/96d35c17-a76d-4f0d-a4ba-454955dbd87f/Blog+SD3+-+Wizard+and+Frog.png)

Thanks to Stable Diffusion 3’s improved prompt following, our model has the ability to create images that focus on various different subjects and qualities while also remaining highly flexible with the style of the image itself.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/10401b22-e408-4ce6-9883-893569ebaa65/Blog+SD3.png)

### Improving Rectified Flows by Reweighting

Stable Diffusion 3 employs a Rectified Flow (RF) formulation ([Liu et al., 2022](https://arxiv.org/abs/2209.03003); [Albergo & Vanden-Eijnden,2022](https://arxiv.org/abs/2209.15571); [Lipman et al., 2023](https://arxiv.org/abs/2210.02747)), where data and noise are connected on a linear trajectory during training. This results in straighter inference paths, which then allow sampling with fewer steps. Furthermore, we introduce a novel trajectory sampling schedule into the training process. This schedule gives more weight to the middle parts of the trajectory, as we hypothesize that these parts result in more challenging prediction tasks. We test our approach against 60 other diffusion trajectories such as [LDM](https://arxiv.org/abs/2112.10752), [EDM](https://arxiv.org/abs/2206.00364) and [ADM](https://arxiv.org/abs/2105.05233), using multiple datasets, metrics, and sampler settings for comparison. The results indicate that while previous RF formulations show improved performance in few step sampling regimes, their relative performance declines with more steps. In contrast, our re-weighted RF variant consistently improves performance.

### Scaling Rectified Flow Transformer Models

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/b62062fe-e5b0-4d89-8316-ca938e31d55c/Scalming_Rectified_Flow_Transformer_Models.png)

We conduct a scaling study for text-to-image synthesis with our reweighted Rectified Flow formulation and MMDiT backbone. We train models ranging from 15 blocks with 450M parameters to 38 blocks with 8B parameters and observe a smooth decrease in the validation loss as a function of both model size and training steps (top row). To test whether this translates into meaningful improvements of the model outputs, we also evaluate automatic image-alignment metrics ([GenEval](https://arxiv.org/abs/2310.11513)) as well as human preference scores (ELO) (bottom row). Our results demonstrate a strong correlation between these metrics and the validation loss, indicating that the latter is a strong predictor of overall model performance. Furthermore, the scaling trend shows no signs of saturation, which makes us optimistic that we can continue to improve the performance of our models in the future.

### Flexible Text Encoders

By removing the memory-intensive 4.7B parameter T5 text encoder for inference, SD3’s memory requirements can be significantly decreased with only small performance loss. Removing this text encoder does not affect visual aesthetics (win rate w/o T5: 50%) and results only in slightly reduced text adherence (win rate 46%) as seen in the above image under the “Performance” section. However, we recommend including T5 for using SD3’s full power in generating written text, since we observe larger performance drops in typography generation without it (win rate 38%) as seen in the examples below:

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/05ce9c95-78ff-47f7-8fdc-c7772c0996af/text-encoders.png)

*Removing T5 for inference only results in significant performance drops when rendering very complex prompts involving many details or large amounts of written text. The above figure shows three random samples per example.*

To learn more about MMDiT, Rectified Flows, and the research behind Stable Diffusion 3, read our full research paper [here](https://arxiv.org/pdf/2403.03206.pdf).

To stay updated on our progress follow us on [Twitter](https://twitter.com/stabilityai), [Instagram](https://www.instagram.com/stability.ai/), [LinkedIn](https://www.linkedin.com/company/stability-ai), and join our [Discord Community](https://discord.gg/stablediffusion).

[![](https://images.squarespace-cdn.com/content/v2/namespaces/memberAccountAvatars/libraries/65ce473bcf080c7b53f8635b/df7b967d-6590-4357-a3b9-f35aeecf00f2/thirdPartyMemberAvatar-65ce473bcf080c7b53f8635b-70a9c56b-d2c3-4bf1-8075-c60686f043c0?format=300w)
Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

[Previous

Previous

## Behind the Compute: Benchmarking Compute Solutions](/news-updates/putting-the-ai-supercomputer-to-work)
[Next

Next

## Introducing TripoSR: Fast 3D Object Generation from Single Images](/news-updates/triposr-3d-generation)



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
