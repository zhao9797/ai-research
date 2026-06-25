# Stability AI releases DeepFloyd IF, a powerful text-to-image model that can smartly integrate text into images — Stability AI
Source: https://stability.ai/news-updates/deepfloyd-if-text-to-image-model
Stability AI releases DeepFloyd IF, a powerful text-to-image model that can smartly integrate text into images — Stability AI



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



# Stability AI releases DeepFloyd IF, a powerful text-to-image model that can smartly integrate text into images

[Product](/news-updates/category/Product)

2023年4月29日

Written By [Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

Today Stability AI and its multimodal AI research lab DeepFloyd announced the research release of DeepFloyd IF, a powerful text-to-image cascaded pixel diffusion model.

DeepFloyd IF is a state-of-the-art text-to-image model released on a non-commercial, research-permissible license that allows research labs to examine and experiment with advanced text-to-image generation approaches. In line with other Stability AI models, Stability AI intends to release a DeepFloyd IF model fully open source at a future date.

**Description and Features**

* **Deep text prompt understanding:**   
  The generation pipeline utilizes the large language model [T5-XXL-1.1](https://github.com/google-research/t5x/blob/main/docs/models.md) as a text encoder. Many text-image cross-attention layers also provide better prompt and image alliance.
* **Application of text description into images:**Incorporating the intelligence of the T5 model, DeepFloyd IF generates coherent and clear text alongside objects of different properties appearing in various spatial relations. Until now, these use cases have been challenging for most text-to-image models.
* **A high degree of photorealism:**  
  This property is reflected by the impressive zero-shot FID score of 6.66 on the [COCO dataset](https://cocodataset.org/#home)  (FID is a main metric used to evaluate the performance of text-to-image models; the lower the score, the better).
* **Aspect ratio shift:**  
  The ability to generate images with a non-standard aspect ratio, vertical or horizontal, and the standard square aspect.
* **Zero-shot image-to-image translations:**  
  Image modification is conducted by (1) resizing the original image to 64 pixels, (2) adding noise through forward diffusion, and (3) using backward diffusion with a new prompt to denoise the image (in inpainting mode, the process happens in the local zone of the image). The style can be changed further through super-resolution modules via a prompt text description. This approach allows modifying style, patterns and details in output while maintaining the basic form of the source image – all without the need for fine-tuning.

[View fullsize
![unnamed (1).png](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673255015-U70NOV235G4LH5WOL2KJ/unnamed+%281%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673255015-U70NOV235G4LH5WOL2KJ/unnamed+%281%29.png)

[View fullsize
![unnamed (2).png](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673254932-OXXF4TELFOR1WWWT2U22/unnamed+%282%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673254932-OXXF4TELFOR1WWWT2U22/unnamed+%282%29.png)

[View fullsize
![unnamed (3).png](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673256459-GA3C2DH5CB461TEZX3AB/unnamed+%283%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673256459-GA3C2DH5CB461TEZX3AB/unnamed+%283%29.png)

[View fullsize
![unnamed (4).png](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673257031-38CL47SPP4UOZHER3I3F/unnamed+%284%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673257031-38CL47SPP4UOZHER3I3F/unnamed+%284%29.png)

[View fullsize
![unnamed (5).png](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673257449-32G8F6TMDGYXKKSW40U1/unnamed+%285%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673257449-32G8F6TMDGYXKKSW40U1/unnamed+%285%29.png)

View fullsize

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/4cb61f93-763c-4524-b415-59e1ca7af06b/deep_floyd_if_image_2_image.gif)

#### **Prompt examples**

DeepFloyd IF can create different fusion concepts using prompts to arrange texts, styles and spatial relations to suit users’ needs.

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673377477-244ZCYBEM7UEIFK9UQDL/unnamed6.jpeg)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673377477-244ZCYBEM7UEIFK9UQDL/unnamed6.jpeg)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673377502-60ZCAXP2T49XXRNBPDAK/unnamed7.jpeg)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673377502-60ZCAXP2T49XXRNBPDAK/unnamed7.jpeg)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673366722-H6CV1H2LXMWS8TK7HOPM/unnamed+%286%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682673366722-H6CV1H2LXMWS8TK7HOPM/unnamed+%286%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699224779-I1X2T3922T4ZENX69E3I/unnamed+%287%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699224779-I1X2T3922T4ZENX69E3I/unnamed+%287%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699228452-C2EUOL5HH0018DJQLEH9/unnamed8.jpeg)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699228452-C2EUOL5HH0018DJQLEH9/unnamed8.jpeg)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699224469-74532F944JXLMVTHC34E/unnamed+%288%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699224469-74532F944JXLMVTHC34E/unnamed+%288%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699225821-AYWG7B2OZY2QJDG93NVD/unnamed+%289%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699225821-AYWG7B2OZY2QJDG93NVD/unnamed+%289%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699228597-CIE6ZFG9J5PJD7RIYLL1/unnamed9.jpeg)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699228597-CIE6ZFG9J5PJD7RIYLL1/unnamed9.jpeg)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699226397-MLS1H4P987HGM6MAFRFR/unnamed+%2810%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699226397-MLS1H4P987HGM6MAFRFR/unnamed+%2810%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699227511-B6422UAET05INB68XGVB/unnamed+%2814%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699227511-B6422UAET05INB68XGVB/unnamed+%2814%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699226916-N8DYXOEH6WZXKH1G75X4/unnamed+%2811%29.png)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699226916-N8DYXOEH6WZXKH1G75X4/unnamed+%2811%29.png)

[View fullsize
![Prompt:](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699227773-4N7LHWRWG2BMUYVWM071/unnamed.jpg)](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/1682699227773-4N7LHWRWG2BMUYVWM071/unnamed.jpg)

#### **Definitions and processes**

DeepFloyd IF is a modular, cascaded, pixel diffusion model. We break down the definitions of each of these descriptors here:

* **Modular:**  
  DeepFloyd IF consists of several neural modules (neural networks that can solve independent tasks, like generating images from text prompts and upscaling) whose interactions in one architecture create synergy.
* **Cascaded:**  
  DeepFloyd IF models high-resolution data in a cascading manner,  using a series of individually trained models at different resolutions. The process starts with a base model that generates unique low-resolution samples (a ‘player’), then upsampled by successive super-resolution models (‘amplifiers’) to produce high-resolution images.
* **Diffusion:**  
  DeepFloyd IF’s base and super-resolution models are diffusion models, where a Markov chain of steps is used to inject random noise into data before the process is reversed to generate new data samples from the noise.
* **Pixel:**  
  DeepFloyd IF works in pixel space. Unlike latent diffusion models (like Stable Diffusion), diffusion is implemented on a pixel level, where latent representations are used.

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/5bd9d71f-bd97-41e4-9fb1-97813c4669fe/Screenshot+2023-04-28+at+17.05.23.png)

This generation flowchart represents a three-stage performance:

A text prompt is passed through the frozen T5-XXL language model to convert it into a qualitative text representation.

* **Stage 1:** A base diffusion model transforms the qualitative text into a 64x64 image. This process is as magical as witnessing a vinyl record’s grooves turn into music. The DeepFloyd team has trained three versions of the base model, each with different parameters: IF-I 400M, IF-I 900M and IF-I 4.3B.
* **Stage 2:** To ‘amplify’ the image, two text-conditional super-resolution models (Efficient U-Net) are applied to the output of the base model. The first of these upscale the 64x64 image to a 256x256 image. Again, several versions of this model are available: IF-II 400M and IF-II 1.2B.
* **Stage 3:** The second super-resolution diffusion model is applied to produce a vivid 1024x1024 image. The final third stage model IF-III has 700M parameters. Note: We have not released this third-stage model yet; however, the modular character of the IF model allows us to use other upscale models – like the [Stable Diffusion x4 Upscaler](https://huggingface.co/stabilityai/stable-diffusion-x4-upscaler) – in the third stage.

#### **Dataset training**

DeepFloyd IF was trained on a custom high-quality LAION-A dataset that contains 1B (image, text) pairs. LAION-A is an aesthetic subset of the English part of the [LAION-5B](https://laion.ai/blog/laion-5b/) dataset and was obtained after deduplication based on similarity hashing, extra cleaning, and other modifications to the original dataset. DeepFloyd’s custom filters removed watermarked, NSFW and other inappropriate content.

**License**

We are releasing DeepFloyd IF under a research license as a new model. Incorporating feedback, we intend to move to a permissive license release; please send feedback to deepfloyd@stability.ai. We believe that the research on DeepFloyd IF can lead to the development of novel applications across various domains, including art, design, storytelling, virtual reality, accessibility, and more. By unlocking the full potential of this state-of-the-art text-to-image model, researchers can create innovative solutions that benefit a wide range of users and industries.

As a source of inspiration for potential research, we pose several questions divided into three groups: **technical, academic** and **ethical**.

**1. Technical research questions:**

a) How can users optimize the IF model by identifying potential improvements that can enhance its performance, scalability, and efficiency?

b) How can output quality be improved by better sampling, guiding, or fine-tuning the DeepFloyd IF mode?

c) How can users apply certain techniques to modify Stable Diffusion output, such as DreamBooth, ControlNet and LoRA on DeepFloyd IF?

**2. Academic research questions:**

a) Exploring the role of pre-training for transfer learning: Can DeepFloyd IF solve tasks other than generative ones (e.g. semantic segmentation) by using fine-tuning (or ControlNet)?

b) Enhancing the model's control over image generation: Can researchers explore methods to provide greater control over generated images? These variables include specific visual attributes like customized image style, tailored image synthesis, or other user preferences.

c) Exploring multi-modal integration to expand the model's capabilities beyond text-to-image synthesis: What are the best ways to integrate multiple modalities, such as audio or video, with DeepFloyd IF to generate greater dynamic and context-aware visual representations?

d) Assessing the model's interpretability: To gain a clearer insight into DeepFloyd IF's inner processes, researchers can develop techniques to improve the model's interpretability, e.g. by allowing for a deeper understanding of the generated images' visual features.

**3. Ethical research questions:**

a) What are the biases in DeepFloyd IF, and how can we mitigate their impact? As with any AI model, DeepFloyd IF may contain biases stemming from its training data. Researchers can explore potential biases in generated images and develop methods to mitigate their impact, ensuring fairness and equity in the AI-generated content.

b) How does the model impact social media and content generation? As DeepFloyd IF can generate high-quality images from text, it is crucial to understand its implications on social media content creation. Researchers can study how the generated images impact user engagement, misinformation, and the overall quality of content on social media platforms.

c) How can researchers develop an effective fake image detector that utilizes our model? Can researchers design a DeepFloyd iF-backed detection system to identify AI-generated content intended to spread misinformation and fake news?

Access to weights can be obtained by accepting the license on the model's cards at Deep Floyd's Hugging Face space: <https://huggingface.co/DeepFloyd>.

If you want to know more, check the model's website: <https://deepfloyd.ai/deepfloyd-if>.

The model card and code are available here: <https://github.com/deep-floyd/IF>.

Everyone is welcome to try the Gradio demo: <https://huggingface.co/spaces/DeepFloyd/IF>.

Join us in public discussions: <https://linktr.ee/deepfloyd>.  
  
We welcome your feedback! Please send your comments and suggestions about DeepFloyd IF to [deepfloyd@stability.ai](mailto:deepfloyd@stability.ai)

[![](https://images.squarespace-cdn.com/content/v2/namespaces/memberAccountAvatars/libraries/65ce473bcf080c7b53f8635b/df7b967d-6590-4357-a3b9-f35aeecf00f2/thirdPartyMemberAvatar-65ce473bcf080c7b53f8635b-70a9c56b-d2c3-4bf1-8075-c60686f043c0?format=300w)
Joshua Lopez](/news-updates?author=65ce473bcf080c7b53f8635b)

[Previous

Previous

## Stability AI releases StableVicuna, the AI World’s First Open Source RLHF LLM Chatbot](/news-updates/stablevicuna-open-source-rlhf-chatbot)
[Next

Next

## Stability AI releases its Image Upscaling API](/news-updates/stability-ai-releases-image-upscaling-api)



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
