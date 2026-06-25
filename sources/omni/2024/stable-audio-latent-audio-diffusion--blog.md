# Stable Audio: Fast Timing-Conditioned Latent Audio Diffusion — Stability AI
Source: https://stability.ai/research/stable-audio-efficient-timing-latent-diffusion
Stable Audio: Fast Timing-Conditioned Latent Audio Diffusion — Stability AI



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



# Stable Audio: Fast Timing-Conditioned Latent Audio Diffusion

[Research](/research/category/Research)

2023年9月13日

Written By [Joshua Lopez](/research?author=65ce473bcf080c7b53f8635b)

Visit [stableaudio.com](https://stableaudio.com)

#### Introduction

The introduction of diffusion-based generative models has revolutionized the field of generative AI over the last few years, leading to rapid improvements in the quality and controllability of generated images, video, and audio. Diffusion models working in the latent encoding space of a pre-trained autoencoder, termed “latent diffusion models”, provide significant speed improvements to the training and inference of diffusion models.

One of the main issues with generating audio using diffusion models is that diffusion models are usually trained to generate a fixed-size output. For example, an audio diffusion model might be trained on 30-second audio clips, and will only be able to generate audio in 30-second chunks. This is an issue when training on and trying to generate audio of greatly varying lengths, as is the case when generating full songs.

Audio diffusion models tend to be trained on randomly cropped chunks of audio from longer audio files, cropped or padded to fit the diffusion model’s training length. In the case of music, this causes the model to tend to generate arbitrary sections of a song, which may start or end in the middle of a musical phrase.

We introduce Stable Audio, a latent diffusion model architecture for audio conditioned on text metadata as well as audio file duration and start time, allowing for control over the content and length of the generated audio. This additional timing conditioning allows us to generate audio of a specified length up to the training window size.

Working with a heavily downsampled latent representation of audio allows for much faster inference times compared to raw audio. Using the latest advancements in diffusion sampling techniques, our flagship Stable Audio model is able to render 95 seconds of stereo audio at a 44.1 kHz sample rate in less than one second on an NVIDIA A100 GPU.

#### Audio Samples

**Music**

Prompt: epic trailer music intense tribal percussion and brass

Stable Audio

0:00

Prompt: lofi hip hop beat melodic chillhop 85 BPM

Stable Audio

0:00

Prompt: genre bluegrass

Stable Audio

0:00

Prompt: death metal power chord guitar riffs fast metal drums

Stable Audio

0:00

**Instruments**

Prompt: 116 BPM rock drums loop clean production

Stable Audio

0:00

Prompt: piano solo chord progression major key uplifting 90 BPM

Stable Audio

0:00

**Sound Effects**

Prompt: an airplane pilot speaking over the intercom

Stable Audio

0:00

Prompt: people talking in a busy restaurant

Stable Audio

0:00

#### Technical details

![](https://images.squarespace-cdn.com/content/v1/6213c340453c3f502425776e/55328fe4-f1fe-476b-bb55-58ac0a0b2346/Stable+Audio+chart.png)

The Stable Audio models are latent diffusion models consisting of a few different parts, similar to Stable Diffusion: A variational autoencoder (VAE), a text encoder, and a U-Net-based conditioned diffusion model.

The VAE compresses stereo audio into a data-compressed, noise-resistant, and invertible lossy latent encoding that allows for faster generation and training than working with the raw audio samples themselves. We use a fully-convolutional architecture based on the [Descript Audio Codec](https://github.com/descriptinc/descript-audio-codec) encoder and decoder architectures to allow for arbitrary-length audio encoding and decoding, and high-fidelity outputs.

To condition the model on text prompts, we use the frozen text encoder of a [CLAP](https://github.com/LAION-AI/CLAP/) model trained from scratch on our dataset. The use of a CLAP model allows the text features to contain some information about the relationships between words and sounds. We use the text features from the penultimate layer of the CLAP text encoder to obtain an informative representation of the tokenized input text. These text features are provided to the diffusion U-Net through cross-attention layers.

For the timing embeddings, we calculate two properties during training time when gathering a chunk of audio from our training data: the second from which the chunk starts (termed “seconds\_start”) and the overall number of seconds in the original audio file (termed “seconds\_total”). For example, if we take a 30-second chunk from an 80-second audio file, with the chunk starting at 0:14, then “seconds\_start” is 14, and “seconds\_total” is 80. These second values are translated into per-second discrete learned embeddings and concatenated with the prompt tokens before being passed into the U-Net’s cross-attention layers. During inference, these same values are provided to the model as conditioning, allowing the user to specify the overall length of the output audio.

The diffusion model for Stable Audio is a 907M parameter U-Net based on the model used in [Moûsai](https://arxiv.org/abs/2301.11757). It uses a combination of residual layers, self-attention layers, and cross-attention layers to denoise the input conditioned on text and timing embeddings. Memory-efficient implementations of attention were added to the U-Net to allow the model to scale more efficiently to longer sequence lengths.

#### Dataset

To train our flagship Stable Audio model, we used a dataset consisting of over 800,000 audio files containing music, sound effects, and single-instrument stems, as well as corresponding text metadata, provided through a deal with stock music provider AudioSparx. This dataset adds up to over 19,500 hours of audio.

#### Future work and open models

Stable Audio represents the cutting-edge audio generation research by Stability AI’s generative audio research lab, Harmonai. We continue to improve our model architectures, datasets, and training procedures to improve output quality, controllability, inference speed, and output length.

Keep an eye out for upcoming releases from Harmonai, including open-source models based on Stable Audio and training code to allow you to train your audio generation models.

[![](https://images.squarespace-cdn.com/content/v2/namespaces/memberAccountAvatars/libraries/65ce473bcf080c7b53f8635b/df7b967d-6590-4357-a3b9-f35aeecf00f2/thirdPartyMemberAvatar-65ce473bcf080c7b53f8635b-70a9c56b-d2c3-4bf1-8075-c60686f043c0?format=300w)
Joshua Lopez](/research?author=65ce473bcf080c7b53f8635b)

[Previous

Previous

## Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets](/research/stable-video-diffusion-scaling-latent-video-diffusion-models-to-large-datasets)
[Next

Next

## Humans in 4D: Reconstructing and Tracking Humans with Transformers](/research/humans-in-4d-reconstructing-and-tracking-humans-with-transformers)



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
