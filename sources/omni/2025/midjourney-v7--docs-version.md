# Version – Midjourney
Source: https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version
Version – Midjourney














Midjourney Docs

[Skip to main content](#page-container)

[![Midjourney Help Center home page](/hc/theming_assets/01K1K3SHJHG4BTD9YK9VH9G86N)

Midjourney](/hc/en-us)


Toggle navigation menu





1. [Midjourney](/hc/en-us)
2. [Documentation](/hc/en-us/categories/32013335627533-Documentation)
3. [Midjourney Controls](/hc/en-us/sections/33329522730509-Midjourney-Controls)

# Version

### Explore and switch between Midjourney versions using the version parameter: `--version` or `--v`

[![version-header.png](/hc/article_attachments/32206880228621)](https://docs.midjourney.com/hc/article_attachments/32206880228621)

## What are Versions?

Think of versions like software updates. When software is updated, it might have better graphics or new features. Similarly, Midjourney versions refer to the different models released over time—each with unique features.

Each version might handle prompts differently, have unique artistic styles, or offer improved image quality.

The current default Midjourney version is V8.1.

## Setting a Version

* [On Web](#zp-1-0)
* [In Discord](#zp-1-1)

Add `--v #` to the end of your prompt in the Imagine bar.  
[![web-imagine-prompt-version.png](/hc/article_attachments/32206960222605)](https://docs.midjourney.com/hc/article_attachments/32206960222605)  
You can choose a default version for all your images in the settings panel. To do this, click the settings [![settings-icon.svg](/hc/article_attachments/32199847452173)](https://docs.midjourney.com/hc/article_attachments/32199847452173) button in the Imagine bar. Once you set it, this will apply to all your future prompts.

Add `--v #` to the end of your prompt in Discord.  
  
[![discord-imagine-prompt-version.png](/hc/article_attachments/32206981994509)](https://docs.midjourney.com/hc/article_attachments/32206981994509)  
  
You can also set the default Version for all images using the [settings command](/hc/en-us/articles/32868982949517) and selecting one from the version dropdown menu.

## V8.1

V8.1 released on [midjourney.com](https://www.midjourney.com) on April 30, 2026, and became the default version on June 10, 2026. V8.1 is our fastest model so far, with standard jobs rendering about 4–5 times faster than earlier versions. It also does a better job reading your prompt and holding on to small details. For even more prompt adherence, you can turn on [Raw](/hc/en-us/articles/32634113811853) to remove default styling.

You may need to unlock your Global V7/V8 [Personalization](https://docs.midjourney.com/hc/en-us/articles/32433330574221-Personalization) Profile to use V8.1.

#### HD Images

V8.1 features HD images, allowing you to generate higher resolution 2K images, without upscaling. You can turn on HD images in the Version section of the settings panel on web, or by using the `--sd` and `--hd` parameters. Using the web "Run batch as HD" button on SD V8.1 images will rerun the seedlocked prompt in HD. HD costs 1.3 minutes of [GPU time](https://docs.midjourney.com/hc/en-us/articles/32016412137741-GPU-Speed-Fast-Relax-Turbo), compared to SD which costs 0.8 minutes of GPU time.

Note: Using any of our inpainting or outpainting tools (Pan, Zoom Out, Edit/Vary Region) on HD images will downscale the resulting images to SD. You can use the Upscale options to return these images to HD resolution.

For more information and tips, see our [V8.1 Alpha post](https://updates.midjourney.com/v8-1-alpha/).

The V8.0 Alpha, launched on March 17, 2026 on [alpha.midjourney.com](https://alpha.midjourney.com), is still available for a limited time. When using it, please be aware of the following:  
• V8.0 Alpha is only compatible with Fast mode.  
• Using `--sv 6` with Style References and Moodboards costs 4x more GPU time, and does not work with `--hd` or `--q 4`.  
• `--hd` and `--q 4` each cost 4x more GPU time.   
• Using `--hd` with `--q 4` together costs 16x more GPU time.

#### Feature Compatibility & Comparison Chart

|  | V6 | V7 | V8.1 |
| --- | --- | --- | --- |
| Max. [Aspect Ratio](/hc/en-us/articles/31894244298125) | 14:1 | 14:1 | 14:1 (4:1 for HD) |
| [Variations](/hc/en-us/articles/32692978437005) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Upscalers](/hc/en-us/articles/32804058614669) | Subtle & Creative | Using V6.1 Upscalers | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) SD Images |
| HD Images (2048px) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) (1.3 min GPU cost) |
| [Pan](/hc/en-us/articles/32570788043405) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) Using V6.1 | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) Using V6.1 |
| [Zoom Out](/hc/en-us/articles/32595476770957) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) Using V6.1 | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) Using V6.1 |
| [Remix](/hc/en-us/articles/32799074515213) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Personalization](/hc/en-us/articles/32433330574221) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Moodboards](/hc/en-us/articles/39193335040013) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Editor](/hc/en-us/articles/32764383466893) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) Using V6.1 | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) Using V6.1 |
| [Character Reference](/hc/en-us/articles/32162917505293) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |
| [Character Weight](/hc/en-us/articles/32162917505293-Character-Reference#h_01JD5G8C3RY38GSHNSFH6H7H31) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |
| [Omni Reference](/hc/en-us/articles/36285124473997) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) (Uses V7) |
| [Omni Reference Weight](/hc/en-us/articles/36285124473997-Omni-Reference#h_01JD5G8C3RY38GSHNSFH6H7H31) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) (Uses V7) |
| [Style Reference](/hc/en-us/articles/32180011136653) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Style Reference Codes](/hc/en-us/articles/32180011136653-Style-Reference#h_01JDK11MKAANM6VRPRBKNW6WYX) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Style Weight](/hc/en-us/articles/32180011136653-Style-Reference#h_01JD5G8C3RY38GSHNSFH6H7H31) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Image Prompts](/hc/en-us/articles/32040250122381) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Image Weight](/hc/en-us/articles/32040250122381-Image-Prompts#h_01JD5G8C3RY38GSHNSFH6H7H31) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Multi-Prompting](/hc/en-us/articles/32658968492557) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |
| [No Parameter](/hc/en-us/articles/32173351982093) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Quality Parameter](/hc/en-us/articles/32176522101773) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) (0.5, 1, 2) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) (1, 2, 4) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |
| [Seed Parameter](/hc/en-us/articles/32604356340877) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733)  (99% identical) |
| [Chaos Parameter](/hc/en-us/articles/32099348346765) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Raw](/hc/en-us/articles/32634113811853) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Stylize Parameter](/hc/en-us/articles/32196176868109) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Tile Parameter](/hc/en-us/articles/32197978340109) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Weird Parameter](/hc/en-us/articles/32390120435085) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [--exp Parameter](https://www.midjourney.com/updates/v7-update-editor-and-exp) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Niji Version](#01JDMR4T1CFVJHAF627ZVXR17A) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) --niji 6 | [check-icon.svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) --niji 7 | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |
| [Draft Mode](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [check-icon.svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |
| [Conversational Mode](https://docs.midjourney.com/hc/en-us/articles/35577175650957-Draft-Conversational-Modes) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) | [check-icon.svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [check-icon.svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Relax Mode](/hc/en-us/articles/32016412137741) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Fast Mode](/hc/en-us/articles/32016412137741) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) |
| [Turbo Mode](/hc/en-us/articles/32016412137741) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--check-16-solid (1).svg](https://docs.midjourney.com/hc/article_attachments/35577079214733) | [heroicons--no-symbol-16-solid.svg](https://docs.midjourney.com/hc/article_attachments/35577055885197) |

## V7

V7 was released on April 3, 2025, and became the default version on June 17, 2025.

In V7, text and image prompts are handled with stunning precision, while image quality shines with richer textures and more coherent details—especially in bodies, hands, and objects.

V7 also introduced [Draft Mode](/hc/en-us/articles/35577175650957) and [Omni Reference](/hc/en-us/articles/36285124473997).

## V6.1

V6.1 was released on July 30, 2024, and was the default until June 16, 2025. It produces more coherent images with more precise details and textures, and generates images approximately 25% faster than V6.

## V6

V6 was released on December 20, 2023, and was the default from February 14 to July 30, 2024. V6 has enhanced prompt accuracy for longer inputs, improved coherence and knowledge, and advanced image prompting and remixing capabilities.

## Niji 7

*Niji models are a special series within Midjourney, developed in collaboration with Spellbrush, to focus on Eastern and anime aesthetics and illustrative styles. Niji models have their own dedicated* [*website*](https://nijijourney.com/home) *and* [*Discord server*](https://discord.com/invite/nijijourney)*, providing a tailored experience for anime enthusiasts.*

Niji 7, launched on January 9, 2026, brings a major boost in coherency. Fine details like eyes, reflections, and small background elements are now much clearer. It also follows prompts more closely, which helps with specific designs or repeatable characters. This version is more literal, so broad or “vibey” prompts may not behave the same as before. Niji 7 also introduces a cleaner, flatter look designed to highlight its improved line work. For more details check out the [Niji blog](https://nijijourney.com/blog/niji-7).

For information about older versions, please see our [Legacy Features](/hc/en-us/articles/33329788681101) article.

### In this article

1. [What are Versions?](#h_01JDMQ7QGAXNS6B0R2015M9H3R)
2. [Setting a Version](#h_01JDMQ7QGA9EZCPT320Q3BH7XK)
3. [V8.1](#h_01JQSR0Q6H0AX8NCC8QGE6C2NZ)
4. [V7](#h_01KKEKYXC5MBVM2G6SEN4TQ82G)
5. [V6.1](#h_01JDMQ7QGAVB4SJ17XBBZAPQZB)
6. [V6](#h_01JDMQ7QGARVMQNTJYK6GP6DFQ)
7. [Niji 7](#01JDMR4T1CFVJHAF627ZVXR17A)

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
