# Legacy Features – Midjourney
Source: https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features
Legacy Features – Midjourney














Midjourney Docs


[Skip to main content](#page-container)

[![Midjourney Help Center home page](/hc/theming_assets/01K1K3SHJHG4BTD9YK9VH9G86N)

Midjourney](/hc/en-us)


Toggle navigation menu





1. [Midjourney](/hc/en-us)
2. [Documentation](/hc/en-us/categories/32013335627533-Documentation)
3. [Midjourney Controls](/hc/en-us/sections/33329522730509-Midjourney-Controls)

# Legacy Features

### Discover legacy tools and features that shaped the Midjourney evolution.

If you’re curious about the older versions of Midjourney and the features they offer, you’ve come to the right place. As we keep moving forward with the latest updates, we also want to acknowledge and explore the tools and options from previous models that helped shape Midjourney to what it is today.

## Legacy Versions

#### Niji 6

The Niji 6 model, released on June 7, 2024, features improved rendering of Japanese text, handling short Japanese kana text effectively and even rendering simple Chinese characters. It offers better image detail, particularly in elements like the structure of anime eyes, and addresses certain minor image artifacts that affected a small number of previous generations.

#### Version 5.2

Version 5.2 was released in June 2023. It was the default model from June 22, 2023 to February 14, 2024. Version 5.2 produces more detailed, sharper results with better colors, contrast, and compositions. It also has a slightly better understanding of prompts than earlier models and is more responsive to the full range of the `--stylize` parameter.

#### Version 5.1

Version 5.1 was released on May 4th, 2023. It was the default model from May 3, 2023 to June 22, 2023. Version 5.1 has a stronger default aesthetic than earlier versions, making it easier to use with simple text prompts. It also has high coherency, excels at accurately interpreting natural language prompts, produces fewer unwanted artifacts and borders, has increased image sharpness, and supports advanced features like repeating patterns with `--tile`.

#### Version 5

Version 5 was released in March 2023. It was the default model from March 30, 2023 to May 3, 2023. Version 5 produces more photographic generations than the V5.1 model, and produces images that closely match the prompt but may require longer prompts to achieve your desired aesthetic.

#### Niji 5

The Niji 5 model was released in April 2023. It can be fine-tuned with specific `--style` parameters including:  
• `--style cute` creates charming and adorable characters, props, and settings.  
• `--style expressive` has a more sophisticated illustrated feeling.  
• `--style original` uses the original Niji Model version 5, which was the default before May 26th, 2023.  
• `--style scenic` makes beautiful backgrounds and cinematic character moments in the context of their fantastical surroundings.

**Default Parameter Values**

|  | Aspect Ratio | Chaos | Quality | Seed | Stop | Stylize |
| --- | --- | --- | --- | --- | --- | --- |
| Default Value | 1:1 | 0 | 1 | random | 100 | 100 |
| Range | any | 0-100 | 0.25, 0.5, 1 | 0-4294967295 | 10-100 | 0-1000 |

**Upscalers:** Version 5 features the Upscale (2x) and Upscale (4x) tools, which are not compatible with [Pan](/hc/en-us/articles/32570788043405) or [tile](/hc/en-us/articles/32197978340109).

* [## Version 4 Models](#zp-1-0)

  #### Version 4

  Version 4 was released in November 2022. It was the default model from December 20, 2022 to March 30, 2023. Version 4 is an entirely new codebase and brand-new AI architecture (compared to previous versions) designed by Midjourney and trained on the new Midjourney AI supercluster. Version 4 has more knowledge of creatures, places, objects, and more than previous versions. It's much better at getting small details right and can handle complex prompts with multiple characters or objects. Version 4 supports advanced functionality like image prompting and multi-prompts, and has very high coherency and excels with Image Prompts.  
    
  Version 4 has three slightly different "flavors" with slight tweaks to the stylistic tuning of the model. Experiment with these versions by adding `--style 4a`, `--style 4b`, or `--style 4c` to the end of a V4 prompt. 4c is the default and support aspect ratios up to 1:2 or 2:1. 4a and 4b only support 1:1, 2:3, and 3:2 aspect ratios.

  #### Niji 4

  The first Niji model, Niji 4, was released on December 20, 2022.   
    
  **Default Parameter Values**

  |  | Aspect Ratio | Chaos | Quality | Seed | Stop | Style | Stylize |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | Default Value | 1:1 | 0 | 1 | random | 100 | 4c | 100 |
  | Range | 1:2–2:1 | 0-100 | 0.25, 0.5, 1 | 0-4294967295 | 10-100 | 4a, 4b, 4c | 0-1000 |

  **Upscalers:** Earlier Midjourney model versions start by generating a grid of low-resolution image options for each Job. You can use a Midjourney upscaler on any of these images to increase the size and add additional details. The table below shows image sizes for 1:1 ratio images. For more information view our [Upscalers](/hc/en-us/articles/32804058614669) article.

  | Model Version | Starting Grid | Default Upscale | Detail Upscale | Light Upscale | Beta Upscale |
  | --- | --- | --- | --- | --- | --- |
  | Version 4 | 512 x 512px | 1024 x 1024px | 1536 x 1536px | 1536 x 1536px | 2048 x 2048px |
  | Niji 4 | 512 x 512px | 1024 x 1024px | 1024 x 1024px | 1024 x 1024px | 2048 x 2048px |

* [## Test Models](#zp-2-0)

  The `--test` and `--testp` models were introduced in August 2022 as part of an effort to gather community feedback and improve upon new features. These test models allow members to explore upcoming capabilities, and they can be used alongside the `--creative` parameter for more varied compositions. When using these models, keep in mind that they support `--stylize` values ranging from 1250 to 5000, offering strong artistic influence.

  There are some limitations with the test models. They do not support multi-prompts or image-prompts and have a maximum aspect ratio of 3:2 or 2:3. When the aspect ratio is 1:1, they generate two initial grid images, but with other aspect ratios, they produce only one initial grid image. Additionally, in crafting prompts, note that words at the beginning of your prompt may hold more weight than those at the end. These unique characteristics make the test models an exciting option for experimental image creation.

  **Upscalers:** Initial grid images are 512 x 512px and the only option to upscale is Beta Upscale, which creates a 2048 x 2048px image when using 1:1 aspect ratio. For more information view our [Upscalers](/hc/en-us/articles/32804058614669) article.

* [## Version 1-3 Models](#zp-3-0)

  #### Version 1

  Version 1 was the default model from February 2022 to April 2022. Version 1 is very abstract and painterly with low coherency.

  #### Version 2

  Version 2 was the default model from April 2022 to July 2022. Version 2 is creative, colorful, and painterly with low coherency.

  #### Version 3

  Version 3 was the default model from July 2022 to November 2022. Version 3 generates highly creative compositions with moderate coherency.  
    
  V3 Legacy Parameter: `--sameseed` Seed values create a single large random noise field applied across all images in the initial grid. When `--sameseed` is specified, all images in the initial grid use the same starting noise and will produce very similar generated images.

  #### High Definition

  `--hd` is an early alternative model that generates busy, detailed, and abstract images with low coherency.  
    
  **Upscalers:** Earlier Midjourney model versions start by generating a grid of low-resolution image options for each Job. You can use a Midjourney upscaler on any of these images to increase the size and add additional details. The table below shows image sizes for 1:1 ratio images. For more information view our [Upscalers](/hc/en-us/articles/32804058614669) article.

  | Model Version | Starting Grid | Default (Detail) Upscale | Light Upscale | Beta Upscale | Max Upscale |
  | --- | --- | --- | --- | --- | --- |
  | Version 1-3 | 256 x 256px | 1024 x 1024px | 1024 x 1024px | 1024 x 1024px | 1664 x 1664px |
  | hd | 512 x 512px | 1536 x 1536px | 1536 x 1536px | 2048 x 2048px | -- |

## Legacy Parameters

|  |  |  |
| --- | --- | --- |
| [**Style Tuner Codes**](#h_01JHKCCT80N011NG85Y2RB1Z0Q) --style code | [**Test Models**](#heading-3) --test --testp | [**Creative**](#heading-3) --creative |
| [**Sameseed**](#heading-4) --sameseed | [**Uplight**](#h_01JHKBTCPCKTEWV56CFSWK79R2) --uplight | [**Stop**](#h_01JY4H0VWNJ0642ANWQFCAGEZ3) --stop |
|  |  |  |

#### Deprecated Parameters

--width and --w (replaced with [Aspect Ratio](/hc/en-us/articles/31894244298125))  
--height and --h (replaced with [Aspect Ratio](/hc/en-us/articles/31894244298125))  
--fast (replaced with [Quality](/hc/en-us/articles/32176522101773))  
--vibe (now known as model version 1)  
--upanime  
--hq  
--newclip  
--nostretch  
--old  
--upbeta

#### Parameter Version Compatibility

For information on the current default version (V7), please visit our [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version#h_01JQSR0Q6H0AX8NCC8QGE6C2NZ) article.

|  | Affects Initial Images | Affects Variations & Remix | V6 | V5 | V4 | V3 | Test & Testp | Niji 4 | Niji 5 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Max. Aspect Ratio | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | any | any | 1:2 / 2:1 | 5:2 / 2:5 | 3:2 / 2:3 | 1:2 / 2:1 | any |
| Chaos | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |
| Image Weight | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | 0-3 default 1 | 0.5-2 default 1 | 0.5-2 default 1 | any default 0.25 |  |  | 0.2-2 default 1 |
| No | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |
| Quality | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | 0.5-2 | 0.25-1 | 0.25-1 | 0.25-2, 5 |  | 0.25-1 | 0.25-1 |
| Repeat | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |
| Seed | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |
| Sameseed | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  |  |  |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  |  |  |
| Stop | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |
| Style |  |  | raw | raw | 4a, 4b |  |  |  | expressive, cute, scenic, original |
| Stylize | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | 0-1000 default 100 | 0-1000 default 100 | 0-1000 default 100 | 625-60000 default 2500 | 1250-5000 default 2500 |  | 0-1000 default 100 |
| Tile | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |
| Weird | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/33481944268045) |  |  |  |  |  |
| # of Initial Images | -- | -- | 4 | 4 | 4 | 4 | 2 or 1 if custom aspect ratio | 4 | 4 |

## Legacy Upscalers

In previous Midjourney model versions, images generated at smaller sizes. You can still enlarge these images using a legacy upscaler. These tools not only increase the size but also add more details. There are various legacy upscalers you can choose from for images made with earlier models. Keep in mind, using a legacy upscaler will use [GPU minutes](/hc/en-us/articles/32016412137741).

#### Version 5

Midjourney model versions 5.x produce 1024 x 1024 pixel images. You can then use the `Upscale (2x)` or `Upscale (4x)` tools to increase the size of your image to 2048 x 2048 pixels or 4096 x 4096 pixels respectively. V5 upscale tools are not compatible with the [Pan tool](/hc/en-us/articles/32570788043405) or the [tile parameter](/hc/en-us/articles/32197978340109).

#### Versions 4 & Earlier

Each of these upscalers changes your image in different ways. All sizes are in pixels and for square aspect ratios.

| Version | Initial Image | V4 Default Upscale | Light Upscale | Beta Upscale | Detail Upscale | Max Upscale\*\* |
| --- | --- | --- | --- | --- | --- | --- |
| V4 | 512 x 512 | 1024 x 1024 | 1536 x 1536 | 2048 x 2048 | 1536 x 1536 | -- |
| V1-V3 | 256 x 256 | -- | 1024 x 1024 | 1024 x 1024 | 1024 x 1024\* | 1664 x 1664 |
| Niji | 512 x 512 | 1024 x 1024 | 1024 x 1024 | 2048 x 2048 | 1024 x 1024 | -- |
| test / testp | 512 x 512 | -- | -- | 2048 x 2048 | -- | -- |
| hd | 512 x 512 | -- | 1536 x 1536 | 2048 x 2048 | 1536 x 1536\* | -- |

\* = the default upscaler for each Midjourney version model.  
\*\* Max Upscale is an older resource-intensive upscaler and is only available when in Fast Mode.

When using legacy versions, the `--uplight` or `--upbeta` parameters in your prompt will turn the `U#` buttons in Discord into Light Upscale or Beta Upscale shortcut buttons.

## Style Tuner

The Style Tuner was a Discord feature in Midjourney version 5.2 and was one of the first steps toward developing [Personalization](/hc/en-us/articles/32433330574221), [Moodboards](/hc/en-us/articles/39193335040013), and the [Style Explorer](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference#h_01K4AQTTGG689MHVSHW9N7Q6KC). The `/tune` command no longer works, and new Style Tuners cannot be created.

You can still access previously created Style Tuners using the `/list_tuners` command, and existing `--style code` parameters can still be used.

## Remaster

Remaster is a Discord button for upscaled images generated using legacy versions of Midjourney. It automatically [remixes your prompt](/hc/en-us/articles/32799074515213) into version 5.2. Remaster any previously upscaled job by clicking the `🆕 Remaster` button beneath the upscaled image.

## Stop

Stop is a parameter compatible with versions 6 and earlier. Using `--stop` allows you to end the image creation process before it's fully completed, resulting in softer, less detailed images.

The default stop value is 100, meaning the image completes fully unless you specify otherwise. You can choose a value between 10 to 100. This value represents the percentage of the process you'd like to stop at.

## Rooms

Rooms were shared spaces on the Midjourney website where members could chat and generate creations together. They were discontinued on February 26, 2026. For events, collaboration, and socializing check out the [Midjourney Discord server](https://discord.gg/midjourney).

### In this article

1. [Legacy Versions](#h_01JHKAKQVS78XFCNP90A5K330T)
2. [Version 4 Models](#heading-2)
3. [Test Models](#heading-3)
4. [Version 1-3 Models](#heading-4)
5. [Legacy Parameters](#h_01JHKB45F6DJ2ZEDVC4V6WVDA2)
6. [Legacy Upscalers](#h_01JHKBTCPCKTEWV56CFSWK79R2)
7. [Style Tuner](#h_01JHKCCT80N011NG85Y2RB1Z0Q)
8. [Remaster](#h_01JHKDZ9DB40Y9MRFYVK5ZW5HM)
9. [Stop](#h_01JY4H0VWNJ0642ANWQFCAGEZ3)
10. [Rooms](#h_01KJE2A87RZ7Y2GHH70BWA22VC)

### Categories

* [Documentation](https://docs.midjourney.com/hc/en-us/categories/32013335627533-Documentation)

  + Getting Started

    - [Getting Started Guide](https://docs.midjourney.com/hc/en-us/articles/33329261836941-Getting-Started-Guide)
  + Prompting Basics

    - [Prompt Basics](https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics)
    - [Modifying Your Creations](https://docs.midjourney.com/hc/en-us/articles/33329329805581-Modifying-Your-Creations)
    - [Aspect Ratio](https://docs.midjourney.com/hc/en-us/articles/31894244298125-Aspect-Ratio)
    - [Image Size & Resolution](https://docs.midjourney.com/hc/en-us/articles/33329374594957-Image-Size-Resolution)
    - [Art of Prompting](https://docs.midjourney.com/hc/en-us/articles/32835253061645-Art-of-Prompting)
  + Using Your Own Images

    - [Video](https://docs.midjourney.com/hc/en-us/articles/37460773864589-Video)
    - [Image Prompts](https://docs.midjourney.com/hc/en-us/articles/32040250122381-Image-Prompts)
    - [Style Reference](https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference)
    - [Omni Reference](https://docs.midjourney.com/hc/en-us/articles/36285124473997-Omni-Reference)
    - [Character Reference](https://docs.midjourney.com/hc/en-us/articles/32162917505293-Character-Reference)
    - [Describe](https://docs.midjourney.com/hc/en-us/articles/32497889043981-Describe)
    - [Editor](https://docs.midjourney.com/hc/en-us/articles/32764383466893-Editor)
  + Using the Website

    - [Website Overview](https://docs.midjourney.com/hc/en-us/articles/33329460426765-Website-Overview)
    - [Creating on Web](https://docs.midjourney.com/hc/en-us/articles/33390732264589-Creating-on-Web)
    - [Organizing Your Creations](https://docs.midjourney.com/hc/en-us/articles/33329462451469-Organizing-Your-Creations)
    - [Using Folders](https://docs.midjourney.com/hc/en-us/articles/34580542725645-Using-Folders)
    - [Draft & Conversational Modes](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes)
    - [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization)
    - [Moodboards](https://docs.midjourney.com/hc/en-us/articles/39193335040013-Moodboards)
    - [Style Creator](https://docs.midjourney.com/hc/en-us/articles/41308374558221-Style-Creator)
    - [Profiles](https://docs.midjourney.com/hc/en-us/articles/41117938447629-Profiles)
    - [Complete Tasks](https://docs.midjourney.com/hc/en-us/articles/33390759197197-Complete-Tasks)
    - [Transitioning to Web](https://docs.midjourney.com/hc/en-us/articles/41268334793613-Transitioning-to-Web)
  + Midjourney Controls

    - [Parameter List](https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List)
    - [Chaos / Variety](https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety)
    - [Legacy Features](https://docs.midjourney.com/hc/en-us/articles/33329788681101-Legacy-Features)
    - [Multi-Prompts & Weights](https://docs.midjourney.com/hc/en-us/articles/32658968492557-Multi-Prompts-Weights)
    - [No](https://docs.midjourney.com/hc/en-us/articles/32173351982093-No)
    - [Pan](https://docs.midjourney.com/hc/en-us/articles/32570788043405-Pan)
    - [Permutations](https://docs.midjourney.com/hc/en-us/articles/32761322355597-Permutations)
    - [Quality](https://docs.midjourney.com/hc/en-us/articles/32176522101773-Quality)
    - [Raw](https://docs.midjourney.com/hc/en-us/articles/32634113811853-Raw)
    - [Remix](https://docs.midjourney.com/hc/en-us/articles/32799074515213-Remix)
    - [Repeat](https://docs.midjourney.com/hc/en-us/articles/32757107922061-Repeat)
    - [Seeds](https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds)
    - [Stylize](https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize)
    - [Text Generation](https://docs.midjourney.com/hc/en-us/articles/32502277092109-Text-Generation)
    - [Tile](https://docs.midjourney.com/hc/en-us/articles/32197978340109-Tile)
    - [Upscalers](https://docs.midjourney.com/hc/en-us/articles/32804058614669-Upscalers)
    - [Variations](https://docs.midjourney.com/hc/en-us/articles/32692978437005-Variations)
    - [Version](https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version)
    - [Weird](https://docs.midjourney.com/hc/en-us/articles/32390120435085-Weird)
    - [Zoom Out](https://docs.midjourney.com/hc/en-us/articles/32595476770957-Zoom-Out)
  + Using Discord

    - [Web vs Discord](https://docs.midjourney.com/hc/en-us/articles/33329300781837-Web-vs-Discord)
    - [Discord Quick Start](https://docs.midjourney.com/hc/en-us/articles/32631709682573-Discord-Quick-Start)
    - [Discord Overview](https://docs.midjourney.com/hc/en-us/articles/33330535666445-Discord-Overview)
    - [Discord Direct Messages](https://docs.midjourney.com/hc/en-us/articles/32637339216013-Discord-Direct-Messages)
    - [Add Midjourney to Your Discord Server](https://docs.midjourney.com/hc/en-us/articles/32637946450445-Add-Midjourney-to-Your-Discord-Server)
    - [Discord Command List](https://docs.midjourney.com/hc/en-us/articles/32894521590669-Discord-Command-List)
    - [Creation Settings in Discord](https://docs.midjourney.com/hc/en-us/articles/32868982949517-Creation-Settings-in-Discord)
    - [Info Command](https://docs.midjourney.com/hc/en-us/articles/32084927086861-Info-Command)
    - [Show Command](https://docs.midjourney.com/hc/en-us/articles/32635695384461-Show-Command)
    - [Vary Region](https://docs.midjourney.com/hc/en-us/articles/32794723105549-Vary-Region)
    - [Blend Images in Discord](https://docs.midjourney.com/hc/en-us/articles/32635189884557-Blend-Images-in-Discord)
    - [Hosting Images in Discord](https://docs.midjourney.com/hc/en-us/articles/32558957919117-Hosting-Images-in-Discord)
  + Midjourney Policies

    - [Terms of Service](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service)
    - [Community Guidelines](https://docs.midjourney.com/hc/en-us/articles/32013696484109-Community-Guidelines)
    - [Privacy Policy](https://docs.midjourney.com/hc/en-us/articles/32083472637453-Privacy-Policy)
    - [Cookie Policy](https://docs.midjourney.com/hc/en-us/articles/37012090959245-Cookie-Policy)
    - [Midjourney Trademark Policy](https://docs.midjourney.com/hc/en-us/articles/32084281102349-Midjourney-Trademark-Policy)
    - [Data Deletion and Privacy FAQ](https://docs.midjourney.com/hc/en-us/articles/32084462534541-Data-Deletion-and-Privacy-FAQ)
    - [Purchase Order Terms and Conditions](https://docs.midjourney.com/hc/en-us/articles/32084601469581-Purchase-Order-Terms-and-Conditions)
    - [AB2013 Documentation](https://docs.midjourney.com/hc/en-us/articles/42829949256205-AB2013-Documentation)
* [Billing Support](https://docs.midjourney.com/hc/en-us/categories/16016577793421-Billing-Support)

  + Plan Information

    - [How to Subscribe](https://docs.midjourney.com/hc/en-us/articles/31974654274573-How-to-Subscribe)
    - [Comparing Midjourney Plans](https://docs.midjourney.com/hc/en-us/articles/27870484040333-Comparing-Midjourney-Plans)
    - [GPU Speed (Fast, Relax, Turbo)](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo)
    - [Subscription Fast Time Expiration](https://docs.midjourney.com/hc/en-us/articles/27870521824653-Subscription-Fast-Time-Expiration)
    - [Purchasing Extra Fast Time](https://docs.midjourney.com/hc/en-us/articles/33570952624141-Purchasing-Extra-Fast-Time)
    - [Earning Free Fast Time](https://docs.midjourney.com/hc/en-us/articles/28014817524109-Earning-Free-Fast-Time)
    - [Using Images & Videos Commercially](https://docs.midjourney.com/hc/en-us/articles/27870375276557-Using-Images-Videos-Commercially)
    - [Stealth Mode](https://docs.midjourney.com/hc/en-us/articles/32019750070669-Stealth-Mode)
    - [Keeping Your Creations Private](https://docs.midjourney.com/hc/en-us/articles/28014645615373-Keeping-Your-Creations-Private)
    - [Free Trials](https://docs.midjourney.com/hc/en-us/articles/27870399340173-Free-Trials)
    - [Discord Nitro Subscription](https://docs.midjourney.com/hc/en-us/articles/27870371412749-Discord-Nitro-Subscription)
  + Account Management

    - [Logging In & Connecting Accounts](https://docs.midjourney.com/hc/en-us/articles/33390994570509-Logging-In-Connecting-Accounts)
    - [Managing Your Subscription](https://docs.midjourney.com/hc/en-us/articles/28014179406861-Managing-Your-Subscription)
    - [Finding Your Renewal Time](https://docs.midjourney.com/hc/en-us/articles/27870433501837-Finding-Your-Renewal-Time)
    - [Upgrading or Downgrading Your Plan](https://docs.midjourney.com/hc/en-us/articles/27870428114317-Upgrading-or-Downgrading-Your-Plan)
    - [Using Midjourney in Discord](https://docs.midjourney.com/hc/en-us/articles/31541509949069-Using-Midjourney-in-Discord)
    - [Turning Off Automatic Renewals](https://docs.midjourney.com/hc/en-us/articles/27868888211213-Turning-Off-Automatic-Renewals)
    - [Changing Your Billing Email](https://docs.midjourney.com/hc/en-us/articles/27868854770573-Changing-Your-Billing-Email)
    - [Transferring Your Subscription](https://docs.midjourney.com/hc/en-us/articles/31541557571981-Transferring-Your-Subscription)
    - [Deleting Your Data](https://docs.midjourney.com/hc/en-us/articles/27870397554701-Deleting-Your-Data)
    - [Contacting Support](https://docs.midjourney.com/hc/en-us/articles/32638309968141-Contacting-Support)
  + Payments

    - [Accepted Payment Methods](https://docs.midjourney.com/hc/en-us/articles/27868831972365-Accepted-Payment-Methods)
    - [Editing Your Payment Information](https://docs.midjourney.com/hc/en-us/articles/25385791792781-Editing-Your-Payment-Information)
    - [Viewing Your Payment History](https://docs.midjourney.com/hc/en-us/articles/27868885185293-Viewing-Your-Payment-History)
    - [Unsuccessful Payments](https://docs.midjourney.com/hc/en-us/articles/27868801964045-Unsuccessful-Payments)
    - [Fixing a Paused Plan](https://docs.midjourney.com/hc/en-us/articles/27868802467853-Fixing-a-Paused-Plan)
    - [Payment Currency](https://docs.midjourney.com/hc/en-us/articles/27868831424525-Payment-Currency)
    - [Reporting a Duplicate Charge](https://docs.midjourney.com/hc/en-us/articles/27868806085517-Reporting-a-Duplicate-Charge)
    - [Reporting an Unauthorized Charge](https://docs.midjourney.com/hc/en-us/articles/27868804543885-Reporting-an-Unauthorized-Charge)
    - [Changing Your Invoice Information](https://docs.midjourney.com/hc/en-us/articles/27868825749517-Changing-Your-Invoice-Information)
    - [Group Plans & Corporate Billing](https://docs.midjourney.com/hc/en-us/articles/27870607078285-Group-Plans-Corporate-Billing)
    - [Educational Use & Student Billing](https://docs.midjourney.com/hc/en-us/articles/42428820154765-Educational-Use-Student-Billing)
  + Cancellations & Refunds

    - [Canceling Your Subscription](https://docs.midjourney.com/hc/en-us/articles/25384024738573-Canceling-Your-Subscription)
    - [Requesting a Refund](https://docs.midjourney.com/hc/en-us/articles/25386088618253-Requesting-a-Refund)
  + Taxes & VAT

    - [Tax / VAT Charges](https://docs.midjourney.com/hc/en-us/articles/27868801261325-Tax-VAT-Charges)
    - [Setting Your Organization's Tax Status (VAT & Tax Exemptions)](https://docs.midjourney.com/hc/en-us/articles/27868838932621-Setting-Your-Organization-s-Tax-Status-VAT-Tax-Exemptions)
  + Magazines & Books

    - [Midjourney Magazine Subscription FAQ](https://docs.midjourney.com/hc/en-us/articles/28012940139021-Midjourney-Magazine-Subscription-FAQ)
    - [Managing Your Midjourney Magazine Subscription](https://docs.midjourney.com/hc/en-us/articles/27870410169997-Managing-Your-Midjourney-Magazine-Subscription)
    - [Midjourney Store Orders FAQ](https://docs.midjourney.com/hc/en-us/articles/28012925933837-Midjourney-Store-Orders-FAQ)



[Midjourney Website](https://www.midjourney.com)
[Midjourney Discord Server](https://discord.gg/midjourney)

Return to top
