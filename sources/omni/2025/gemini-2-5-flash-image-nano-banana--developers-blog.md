# Introducing Gemini 2.5 Flash Image, our state-of-the-art image model - Google Developers Blog
Source: https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/
Introducing Gemini 2.5 Flash Image, our state-of-the-art image model
- Google Developers Blog



developers.googleblog.com uses cookies to deliver and enhance the quality of its services and to analyze traffic. If you agree, cookies are also used to serve advertising and to personalize the content and advertisements that you see. [Learn more](https://policies.google.com/technologies/cookies?hl=en)

AgreeNo thanks





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

# Introducing Gemini 2.5 Flash Image, our state-of-the-art image model

AUG. 26, 2025

[Alisa Fortin](/en/search/?author=Alisa+Fortin)
Product Manager

[Guillaume Vernade](/en/search/?author=Guillaume+Vernade)
Gemini Developer Advocate

[Kat Kampf](/en/search/?author=Kat+Kampf)
Product Manager

[Ammaar Reshi](/en/search/?author=Ammaar+Reshi)
Product and Design Lead
AI Studio

Share

* [Facebook](https://www.facebook.com/sharer/sharer.php?u=https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/ "Share on Facebook")
* [Twitter](https://twitter.com/intent/tweet?text=https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/ "Share on Twitter")
* [LinkedIn](https://www.linkedin.com/shareArticle?url=https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/&mini=true "Share on LinkedIn")
* [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20https://developers.googleblog.com/en/introducing-gemini-2-5-flash-image/ "Send via Email")

![Introducing Gemini 2.5 Flash Image, our state-of-the-art image model](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemini2.5Flash-Wagtial-Alt_RD4-V01.original.jpg)

Today, we’re excited to introduce [Gemini 2.5 Flash Image](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-preview-image) (aka nano-banana), our state-of-the-art image generation and editing model. This update enables you to blend multiple images into a single image, maintain character consistency for rich storytelling, make targeted transformations using natural language, and use Gemini's world knowledge to generate and edit images.

When we first launched native image generation in Gemini 2.0 Flash earlier this year, you told us you loved its low latency, cost-effectiveness, and ease of use. But you also gave us feedback that you needed higher-quality images and more powerful creative control.

This model is available right now via the [Gemini API](https://ai.google.dev/gemini-api/docs/image-generation) and [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-preview-image) for developers and [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/multimodal?model=gemini-2.5-flash-image-preview) for enterprise. Gemini 2.5 Flash Image is priced at $30.00 per 1 million output tokens with each image being 1290 output tokens ($0.039 per image). All other modalities on input and output follow Gemini 2.5 Flash [pricing](https://ai.google.dev/gemini-api/docs/pricing).

![Gemini-2-5-image-editing-performance](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/gemini-image__image-editing__no_product-reconte.original.png)
[(lmarena results come from https://lmarena.ai/leaderboard)](https://lmarena.ai/leaderboard)

## Gemini 2.5 Flash Image in action

To make building with Gemini 2.5 Flash Image even easier, we have made significant updates to [Google AI Studio’s “build mode”](https://aistudio.google.com/apps) (with more updates to come). In the examples below, not only can you quickly test the model’s capabilities with custom AI powered apps, but you can remix them or bring ideas to life with just a single prompt. When you are ready to share an app you built, you can deploy right from Google AI Studio or save the code to GitHub.

Try a prompt like “Build me an image editing app that lets a user upload an image and apply different filters" or choose one of the preset templates and remix it, all for free!

### **Maintain character consistency**

A fundamental challenge in image generation is maintaining the appearance of a character or object across multiple prompts and edits. You can now place the same character into different environments, showcase a single product from multiple angles in new settings, or generate consistent brand assets, all while preserving the subject.

We built a [template app in Google AI Studio](https://aistudio.google.com/apps/bundled/past_forward?showPreview=true&showAssistant=true) (that you can easily customize and vibe code on top of) to demonstrate the model’s character consistency capabilities.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-70_ydi_5_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/PastForward-HighRes.mp4)

(sequence shortened)

Beyond character consistency, the model is also excellent at adhering to visual templates. We have already seen developers explore areas like real estate listing cards, uniform employee badges, or dynamic product mockups for an entire catalog—all from a single design template.

![gemini-2-5-image-editing-character-consistency](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/gemini-2-5-image-editing-character-consistency.original.png)

### **Prompt based image editing**

Gemini 2.5 Flash Image enables targeted transformation and precise local edits with natural language. For example, the model can blur the background of an image, remove a stain in a t-shirt, remove an entire person from a photo, alter a subject's pose, add color to a black and white photo, or whatever else you can conjure up with a simple prompt.

To show these capabilities in action, we built a [photo editing template app in AI Studio](https://aistudio.google.com/apps/bundled/pixshop), with both UI and prompt-based controls.

![gemini-2-5-flash-prompt-based-image-editing](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/gemini-2-5-flash-prompt-based-image-editing.original.png)

### **Native world knowledge**

Historically, image generation models have excelled at aesthetic images, but lacked a deep, semantic understanding of the real world. With Gemini 2.5 Flash Image, the model benefits from Gemini’s world knowledge, which unlocks new use cases.

To demonstrate this, we built [a template app in Google AI Studio](https://aistudio.google.com/apps/bundled/codrawing) that turns a simple canvas into an interactive education tutor. It showcases the model's ability to read and understand hand-drawn diagrams, help with real world questions, and follow complex editing instructions in a single step.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-_7j2nlj6_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/gemini-2-5-flash-image-native-world-knowledge.mp4)

(Example prompts and model results)

### **Multi-image fusion**

Gemini 2.5 Flash Image can understand and merge multiple input images. You can put an object into a scene, restyle a room with a color scheme or texture, and fuse images with a single prompt.

To showcase multi-image fusion, we built a [template app in Google AI Studio](https://aistudio.google.com/apps/bundled/home_canvas) which lets you drag products into a new scene to quickly create a new photorealistic fused image.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-_390ekpo_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/gemini-2-5-flash-image-multi-image-fusion_1.mp4)

(Sequences shortened)

## Get started building

Check out our [developer docs](https://ai.google.dev/gemini-api/docs/image-generation) to start building with Gemini 2.5 Flash Image. The model is in preview today via the [Gemini API](https://ai.google.dev/gemini-api/docs/image-generation) and [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-preview-image) but will be stable in the coming weeks. All of the demo apps we highlighted here were vibe coded in Google AI Studio so they can be remixed and customized with just a prompt.

[OpenRouter.ai](https://openrouter.ai/google/gemini-2.5-flash-preview-image) has partnered with us to help bring Gemini 2.5 Flash Image to their 3M+ developers everywhere, today. This is the first model on OpenRouter – of the 480+ live today –that can generate images.

We're also excited to partner with [fal.ai](https://fal.ai/models/fal-ai/gemini-25-flash-image), a leading developer platform for generative media, to make Gemini 2.5 Flash Image available to the broader developer community.

All images created or edited with Gemini 2.5 Flash Image will include an invisible [SynthID digital watermark](https://deepmind.google/science/synthid/), so they can be identified as AI-generated or edited.

```
from google import genai
from PIL import Image
from io import BytesIO

client = genai.Client()

prompt = "Create a picture of my cat eating a nano-banana in a fancy restaurant under the gemini constellation"

image = Image.open('/path/to/image.png')

response = client.models.generate_content(
    model="gemini-2.5-flash-image-preview",
    contents=[prompt, image],
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO(part.inline_data.data))   
    image.save("generated_image.png")
```

Python

Copied

We are actively working to improve long-form text rendering, even more reliable character consistency, and factual representation like fine details in images. Please continue to send us feedback in our [developer forum](https://discuss.ai.google.dev/c/gemini-api/4) or on [X](https://x.com/googleaistudio).

We can’t wait to see what you build with Gemini 2.5 Flash Image!

posted in:

* [Gemini](/en/search/?product_categories=Gemini)
* [Google AI Studio](/en/search/?product_categories=Google+AI+Studio)
* [AI](/en/search/?technology_categories=AI)
* [Announcements](/en/search/?content_type_categories=Announcements)
* [Vertex AI](/en/search/?tag=Vertex AI)

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
