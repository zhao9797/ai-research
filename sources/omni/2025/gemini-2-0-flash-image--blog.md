# Experiment with Gemini 2.0 Flash native image generation - Google Developers Blog
Source: https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/
Experiment with Gemini 2.0 Flash native image generation
- Google Developers Blog







[![Google for Developers](https://storage.googleapis.com/gweb-developer-goog-blog-cms-assets/site/20260519-162827/images/g-dev.svg)](https://developers.google.com/)

[Community/Events](//developers.google.com/community)

[Learn](//developers.google.com/solutions/catalog)

[Blog](//developers.googleblog.com)

[YouTube](https://www.youtube.com/user/GoogleDevelopers)

Search

[![Google for Developers](https://storage.googleapis.com/gweb-developer-goog-blog-cms-assets/site/20260519-162827/images/g-dev.svg)](https://developers.google.com/)

* [Community/Events](//developers.google.com/community)
* [Learn](//developers.google.com/solutions/catalog)
* [Blog](//developers.googleblog.com)
* [YouTube](https://www.youtube.com/user/GoogleDevelopers)

[Gemini](/en/search/?product_categories=Gemini) / [Google AI Studio](/en/search/?product_categories=Google+AI+Studio)

# Experiment with Gemini 2.0 Flash native image generation

MARCH 12, 2025

[Kat Kampf](/en/search/?author=Kat+Kampf)
Product Manager

[Nicole Brichtova](/en/search/?author=Nicole+Brichtova)
Product Manager
Google DeepMind

Share

* [Facebook](https://www.facebook.com/sharer/sharer.php?u=https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/ "Share on Facebook")
* [Twitter](https://twitter.com/intent/tweet?text=https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/ "Share on Twitter")
* [LinkedIn](https://www.linkedin.com/shareArticle?url=https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/&mini=true "Share on LinkedIn")
* [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/ "Send via Email")

![Gemini 2.0 Flash native image generation](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/gemini-image-generation.original.png)

In [December](https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/) we first introduced native image output in Gemini 2.0 Flash to trusted testers. Today, we're making it available for developer experimentation across [all regions](https://ai.google.dev/gemini-api/docs/available-regions) currently supported by Google AI Studio. You can test this new capability using an experimental version of Gemini 2.0 Flash ([gemini-2.0-flash-exp](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-exp)) in Google AI Studio and via the Gemini API.

Gemini 2.0 Flash combines multimodal input, enhanced reasoning, and natural language understanding to create images.

Here are some examples of where 2.0 Flash’s multimodal outputs shine:

### **1. Text and images together**

Use Gemini 2.0 Flash to tell a story and it will illustrate it with pictures, keeping the characters and settings consistent throughout. Give it feedback and the model will retell the story or change the style of its drawings.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-26bi7zxz_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/image-text-gemini-2-image-generation.mp4)

Story and illustration generation in Google AI Studio

### **2. Conversational image editing**

Gemini 2.0 Flash helps you edit images through many turns of a natural language dialogue, great for iterating towards a perfect image, or to explore different ideas together.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-n80ygwe3_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/conversational-image-editing-gemini-2-image-generation_2.mp4)

Multi-turn conversation image editing maintaining context throughout the conversation in Google AI Studio

### **3. World understanding**

Unlike many other image generation models, Gemini 2.0 Flash leverages world knowledge and enhanced reasoning to create the *right* image. This makes it perfect for creating detailed imagery that’s realistic–like illustrating a recipe. While it strives for accuracy, like all language models, its knowledge is broad and general, not absolute or complete.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-9jiz61bs_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/world-understanding-gemini-2-image-generation_3.mp4)

Interleaved text and image output for a recipe in Google AI Studio

### **4. Text rendering**

Most image generation models struggle to accurately render long sequences of text, often resulting in poorly formatted or illegible characters, or misspellings. Internal benchmarks show that 2.0 Flash has stronger rendering compared to leading competitive models, and great for creating advertisements, social posts, or even invitations.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-m6z8l7l9_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/text-rendering-gemini-2-image-generation_2.mp4)

Image outputs with long text rendering in Google AI Studio

## Start making images with Gemini today

Get started with Gemini 2.0 Flash via the Gemini API. Read more about image generation in our [docs](https://ai.google.dev/gemini-api/docs/image-generation).

```
from google import genai
from google.genai import types

client = genai.Client(api_key="GEMINI_API_KEY")

response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=(
        "Generate a story about a cute baby turtle in a 3d digital art style. "
        "For each scene, generate an image."
    ),
    config=types.GenerateContentConfig(
        response_modalities=["Text", "Image"]
    ),
)
```

Python

Copied

Whether you are building AI agents, developing apps with beautiful visuals like illustrated interactive stories, or brainstorming visual ideas in conversation, Gemini 2.0 Flash allows you to add text and image generation with just a single model. We're eager to see what developers create with native image output and your [feedback](https://discuss.ai.google.dev/c/gemini-api/4) will help us finalize a production-ready version soon.

posted in:

* [Gemini](/en/search/?product_categories=Gemini)
* [Google AI Studio](/en/search/?product_categories=Google+AI+Studio)
* [AI](/en/search/?technology_categories=AI)
* [Announcements](/en/search/?content_type_categories=Announcements)
* [image generation](/en/search/?tag=image generation)
* [Gemini 2.0](/en/search/?tag=Gemini 2.0)
* [Generative AI](/en/search/?tag=Generative AI)

Previous

Next

Related Posts

[![Build Cross-Language Multi-Agent Team with Google’s Agent Development Kit and A2A](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/banner.2e16d0ba.fill-800x400.jpg)

AI
Cloud
Announcements
Best Practices

Build Cross-Language Multi-Agent Team with Google’s Agent Development Kit and A2A

JUNE 22, 2026](/en/build-cross-language-multi-agent-team-with-google-agent-development-kit-and-a2a/)
[![How A2A is Building a World of Collaborative Agents](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/image2.original_6xqVyTd.2e16d0ba.fill-800x400.jpg)

AI
Cloud
Case Studies
Announcements

How A2A is Building a World of Collaborative Agents

JUNE 18, 2026](/en/how-a2a-is-building-a-world-of-collaborative-agents/)
[![Turn creative prompts into interactive XR experiences with Gemini](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemini_Generated_Image_gasezsgasez.2e16d0ba.fill-800x400.png)

Gemini
Web
AI
Tutorials
How-To Guides

Turn creative prompts into interactive XR experiences with Gemini

FEB. 19, 2026](/en/turn-creative-prompts-into-interactive-xr-experiences-with-gemini/)
[![Measuring What Matters with Jules](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Measuring_What_Matters_with_Jules_.2e16d0ba.fill-800x400.png)

Web
AI
Case Studies
Learn

Measuring What Matters with Jules

JUNE 22, 2026](/en/measuring-what-matters-with-jules/)
[![How we built the Google I/O 2026 Save the Date experience](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/mbu-svd-hero.2e16d0ba.fill-800x400.png)

Gemini
Google AI Studio
AI
Events

How we built the Google I/O 2026 Save the Date experience

MARCH 3, 2026](/en/how-we-built-the-google-io-2026-save-the-date-experience/)

* Connect
  + [Blog](//googledevelopers.blogspot.com)
  + [Bluesky](https://goo.gle/3FReQXN)
  + [Instagram](https://goo.gle/googlefordevs)
  + [LinkedIn](https://goo.gle/gdevs-li)
  + [X (Twitter)](https://goo.gle/gdevs-tw)
  + [YouTube](https://goo.gle/developers)
* Programs
  + [Google Developer Program](//developers.google.com/program)
  + [Google Developer Groups](//developers.google.com/community/gdg)
  + [Google Developer Experts](//developers.google.com/community/experts)
  + [Accelerators](//developers.google.com/community/accelerators)
  + [Women Techmakers](//www.womentechmakers.com)
  + [Google Cloud & NVIDIA](//developers.google.com/community/nvidia)
* Developer consoles
  + [Google API Console](//console.developers.google.com)
  + [Google Cloud Platform Console](//console.cloud.google.com)
  + [Google Play Console](//play.google.com/apps/publish)
  + [Firebase Console](//console.firebase.google.com)
  + [Actions on Google Console](//console.actions.google.com)
  + [Cast SDK Developer Console](//cast.google.com/publish)
  + [Chrome Web Store Dashboard](//chrome.google.com/webstore/developer/dashboard)
  + [Google Home Developer Console](//console.home.google.com/)

[![Google for Developers](https://storage.googleapis.com/gweb-developer-goog-blog-cms-assets/site/20260519-162827/images/g-dev.svg)](https://developers.google.com/)

* [Android](//developer.android.com)
* [Chrome](//developer.chrome.com/home)
* [Firebase](//firebase.google.com)
* [Google Cloud Platform](//cloud.google.com)
* [All products](//developers.google.com/products)
* Manage cookies


* [Terms](//developers.google.com/terms/site-terms)
* [Privacy](//policies.google.com/privacy)
