# Creating with Gen-3 Alpha and Gen-3 Alpha Turbo – Runway
Source: https://help.runwayml.com/hc/en-us/articles/30266515017875-Creating-with-Gen-3-Alpha-and-Gen-3-Alpha-Turbo
Creating with Gen-3 Alpha and Gen-3 Alpha Turbo – Runway

[Skip to main content](#main-content)



[Go to Runway](https://app.runwayml.com/login)
[Get Help](https://help.runwayml.com/hc/en-us/articles/20821762056723-How-to-submit-a-support-request)



[

](https://d3phaj0sisr2ct.cloudfront.net/academy/videos/academy-bg.mp4)


1. [Runway](/hc/en-us)
2. [Creating with Runway](/hc/en-us/categories/1500001930562-Creating-with-Runway)
3. [Model Guides](/hc/en-us/sections/50990795422739-Model-Guides)
4. [More Tools](/hc/en-us/sections/42916827540243-More-Tools)
5. [Gen-3 Alpha](/hc/en-us/sections/30265301423635-Gen-3-Alpha)

# Creating with Gen-3 Alpha and Gen-3 Alpha Turbo

### Table of Contents

* [Step 1 – Drafting the Prompt](#toc-heading-0)
* [Step 2 – Configuring the Settings](#toc-heading-1)
* [Step 3 – Generating the Video](#toc-heading-2)
* [Step 4 – Extending the Video](#toc-heading-3)

This feature is currently available to users on a [**Standard**](https://runwayml.com/pricing/) plan or higher.

**Notice:** Gen-3 Alpha, Gen-3 Alpha Turbo will no longer be available after **July 30, 2026**. Updated replacements are available now:

* Text to Video – [Gen-4.5](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5)
* Image to Video – [Gen-4.5](https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5)
* Keyframes – [Animate Frames](https://app.runwayml.com/video-tools/teams/placeholder/ai-tools/generate?tool=apps&app=keyframes) app
* Video to Video – [Edit Studio Aleph 2.0](/hc/en-us/articles/51683104370451)

To explore further, see [Creating with Apps](https://help.runwayml.com/hc/en-us/articles/45570040112531-Creating-with-Apps) for a full list of task-specific functionality.

### Introduction

**Gen-3 Alpha** is a text to video and image to video model that was originally released in 2024.

**Gen-3 Alpha Turbo** is a faster model in the Gen-3 Alpha family that generates at a lower cost. The Turbo model is available on [all plan levels](https://runwayml.com/pricing) and requires an input image.

This article outlines the steps to create videos with Gen-3 Alpha, the available settings, and more.

### Article highlights

* The Turbo model requires an input image, so switch to Gen-3 Alpha for text-only prompting
* Text to Video is only supported on the Gen-3 Alpha model
* Focus on describing the desired motion when using an input image
* A single generation can be extended up to three times

### Related Links

* [Gen-3 Alpha Prompting Guide](https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide)
* [Getting Started: Gen-3 Alpha](https://academy.runwayml.com/gen3-alpha/getting-started-with-gen3-alpha)

### Spec Information

| Spec | Gen-3 Alpha | Gen-3 Alpha Turbo |
| --- | --- | --- |
| Cost | 10 credits per second | 5 credits per second |
| Supported durations | 5 seconds 10 seconds | |
| Platform availability | Web, iOS | |
| Base prompt inputs | Text Image | Text Image (Required) |
| Text character limit | 1000 characters | |
| Output resolutions | 1280x768 | 1280x768 768x1280 |
| [Keyframes](https://help.runwayml.com/hc/en-us/articles/34170748696595-Creating-with-Keyframes-on-Gen-3-Alpha-Turbo) support | First **or** last frame | First, middle, and last |
| Video Extension increments | 5 or 10 seconds | 8 seconds |
| Maximum extended length | 40 seconds | 34 seconds |
| Frame Rate (FPS) | 24fps | |

# Step 1 – Drafting the Prompt

Begin by navigating to **Generative Session** in your [Dashboard](https://app.runwayml.com/dashboard).

From here, open the model selector from the bottom left corner. Choose the **Legacy** tab to reveal the **Gen-3 Alpha** and **Gen-3 Alpha Turbo** models:

![legacy.png](/hc/article_attachments/49970103027603)

To use Text to Video, please ensure that you select the **Gen-3 Alpha** model. The Turbo model **requires an input image**.

## Text-only Prompts

**Gen-3 Alpha** can create highly detailed videos with complex scene changes, a wide range of cinematic choices, and detailed art directions. A descriptive yet clear prompt is key to generating a great video with Text to Video.

Add a descriptive text prompt that conveys the camera angle, subject, scene, style and movement to generate your video. Check out our [Gen-3 Alpha Prompting Guide](https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide) for ideas and more prompt examples.

Below are text-only prompt examples along with their respective outputs:

|  |  |
| --- | --- |
| **Prompt** | **Output** |
| A dramatic zoom in on the face of movie villain as he raises an eye brow and the lights shift, casting an eerie red glow across him. Evil villain lair, 1980s spy movie, cinematic, 35mm film, dynamic movement. | villian.gif |
| A sci-fi-like action chase scene, FPV hyper-speed fly through multiple locations. Racing through asteroid fields, through a dense clouds, through a complex system of desolate landscapes. Dynamic motion, dynamic blur, timelapse, 30x speed, cinematic, muted color palette. | Biome Switch 2.gif |
| Dynamic motion, 30x speed. Camera follows a translucent white plastic grocery bag with bold red letters printed on it that read "THANK YOU" as it flies organically in the wind of a desert. the slightly opaque bag undulates in the wind, maintaining the bold red "THANK YOU" text printed on it. | plasticbag.gif |

## Image and Text Prompts

Input images are optional in Gen-3 Alpha, but **required in Gen-3 Alpha Turbo**. Input images will act as the first frame of your video by default.

You’ll be prompted to crop your input image if it is not in a supported resolution.

Include a simplistic text prompt to guide the output of your video. Instead of describing what is in the image, **focus on describing the movement** of the camera, character, and scene you'd like in the output.

Describing the full contents of input images may lead to unexpected results.

Below are examples of input images, text prompts that focus on motion, and their respective outputs:

|  |  |  |
| --- | --- | --- |
| **Input image** | **Prompt** | **Output** |
| bubblegumstretchface.png | the gloved hands pull to stretch the face made of a bubblegum material | Gen-3 Alpha 970068599, the gloves hands pul, image-prompt, M 5.mp4.gif |
| seaanenomes.png | the sea anemones sway and flow naturally in the water. the camera remains still. | Gen-3 Alpha 1081709814, the sea anemones swa, Frames 30514788, pho, M 5.mp4.gif |
| knightincathedral.png | subject stiffly walks, his movement hindered by the heavy armor. dynamic motion. camera zooms out to retain framing as he moves closer. | Gen-3 Alpha Turbo 2300194801, subject stiffly walk, image-prompt, M 5.mp4.gif |

# Step 2 – Configuring the Settings

Gen-3 Alpha has a few additional settings that you should review before starting your generation.

## Keyframes

You can choose if you'd like your input image to act as the first **or** last frame in Gen-3 Alpha, or configure both the first, middle, **and** last frame on Turbo. Please see [Creating with Keyframes](https://help.runwayml.com/hc/en-us/articles/34170748696595-Creating-with-Keyframes) for more information on using this feature.

## Camera Control

Use Camera Control to choose both the direction and intensity of how you move through your scenes for even more intention in every shot. Please see [Creating with Camera Control](https://help.runwayml.com/hc/en-us/articles/34926468947347-Creating-with-Camera-Control-on-Gen-3-Alpha-Turbo) for more information on using these settings.

## Aspect ratio

On the Turbo model, you can choose between 1280x768 and 768x1280 aspect ratios before starting your generation. Changing this setting may prompt you to crop any currently selected input images.

# Step 3 – Generating the Video

After drafting your text prompt and configuring your settings, you're now ready to generate your video.

You can choose between a **5 or 10 second duration** for your output with the duration dropdown near the **Generate** button. Generative Video defaults to 10 second generations.

Your generations will be scrollable through your [session](https://help.runwayml.com/hc/en-us/articles/33545310653203-Generating-with-Sessions) as you continue to generate. You can also access completed videos in your **Assets**, where they will save to the relevant subfolder within **Sessions** by default.

You can continue working with the output by selecting **Use** towards the bottom left corner of the output:

![Screenshot 2026-01-14 at 13.07.33.png](/hc/article_attachments/48645104704915)

# Step 4 – Extending the Video

Completed Gen-3 Alpha and Turbo generations can be extended **up to three times** to create a longer video. Gen-3 Alpha videos can be extended to a maximum of 40 seconds, where Turbo generations can be extended to a maximum of 34 seconds given that the original video was 10 seconds.

To extend a video, click the **Use** button and select **Extend** beneath an output in your session. Alternatively, you can extend an existing generation by opening it through your **Assets** and clicking **Extend video**.

The last frame of the video you’re extending will automatically populate as the input.

Add a new text prompt to indicate what should happen in the extension. Extensions are similar to Image to Video generations, so try keeping your prompt focused on camera, character and scene movement.

You can choose between a 5 or 10 second extension before generating in Gen-3 Alpha. The Turbo model offers 8 second extensions. Please note that extension costs will be the same as the pricing of the model used to generate the original video. The model cannot be changed before an extension.

Click **Extend** to begin the extension. If you’re happy with the extended output, you’ll be able to follow these steps up to two more times to create a long video.

[

](https://d3phaj0sisr2ct.cloudfront.net/site/content/videos/gen4/Footer.mp4)

## Product

* [GWM-1](https://runwayml.com/research/introducing-runway-gwm-1)
* [General World Models](https://runwayml.com/research/introducing-general-world-models)
* [Robotics SDK](https://runwayml.com/research/introducing-runway-gwm-1#robotics-section)
* [Gen-4.5](https://runwayml.com/research/introducing-runway-gen-4.5)
* [Aleph](https://runwayml.com/research/introducing-runway-aleph)
* [Act-Two](https://runwayml.com/research/introducing-act-one)
* [API](https://runwayml.com/research/introducing-general-world-models)

## Initiatives

* [Studios](https://studios.runwayml.com/)
* [AI Film Festival](https://aiff.runwayml.com/)
* [Gen:48](https://gen48.runwayml.com/winners)
* [FOOM!](https://watchfoom.com/)
* [Academy](https://academy.runwayml.com/)
* [Telescope Magazine](https://www.telescopemagazine.com/)
* [Creative Partners Program](https://runwayml.com/creative-partners-program)
* [The Hundred Film Fund](https://runwayml.com/hundred-film-fund)

## Blog

* [Our Research](https://runwayml.com/research)
* [Publications](https://runwayml.com/research/publications)
* [Careers](https://runwayml.com/careers)
* [About Us](hhttps://runwayml.com/about)
* [Customer Stories](https://runwayml.com/customers/)
* [News](https://runwayml.com/news)
* [Talent Network](https://talent.runwayml.com/)

## Get Started

* [For Enterprises](https://runwayml.com/enterprise/)
* [For Education](https://runwayml.com/educators/)
* [Login](https://app.runwayml.com/login)
* [Pricing](https://runwayml.com/pricing/)
* [Help Center](https://help.runwayml.com/hc/en-us)
* [Data Security](https://runwayml.com/data-security)
* [Changelog](https://runwayml.com/changelog)

## Connect

* [Press](mailto:press@runwayml.com)
* [Partnerships](mailto:partnerships@runwayml.com)
* [Brand Guidelines](https://runwayml.com/brand-guidelines)
* [Meetups](https://runwayml.com/meetups)
* [Twitter](https://x.com/runwayml)
* [Instagram](https://instagram.com/runwayapp)
* [Youtube](https://www.youtube.com/runwayml)
* [Discord](http://discord.gg/invite/runwayml)

© 2025 RUNWAY AI, INC / [TERMS OF USE](https://runwayml.com/terms-of-use/) / [PRIVACY POLICY](https://runwayml.com/privacy-policy/) / [CODE OF CONDUCT](https://runwayml.com/coc/) / [SYSTEM STATUS](https://status.runwayml.com/)
