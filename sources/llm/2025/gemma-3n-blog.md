# Announcing Gemma 3n preview: powerful, efficient, mobile-first AI - Google Developers Blog
Source: https://developers.googleblog.com/en/introducing-gemma-3n/
Announcing Gemma 3n preview: powerful, efficient, mobile-first AI
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

[Gemma](/en/search/?product_categories=Gemma)

# Announcing Gemma 3n preview: powerful, efficient, mobile-first AI

MAY 20, 2025

[Lucas Gonzalez](/en/search/?author=Lucas+Gonzalez)
Product Manager
Google DeepMind

[Rakesh Shivanna](/en/search/?author=Rakesh+Shivanna)
Principal Software Engineer

Share

* [Facebook](https://www.facebook.com/sharer/sharer.php?u=https://developers.googleblog.com/en/introducing-gemma-3n/ "Share on Facebook")
* [Twitter](https://twitter.com/intent/tweet?text=https://developers.googleblog.com/en/introducing-gemma-3n/ "Share on Twitter")
* [LinkedIn](https://www.linkedin.com/shareArticle?url=https://developers.googleblog.com/en/introducing-gemma-3n/&mini=true "Share on LinkedIn")
* [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20https://developers.googleblog.com/en/introducing-gemma-3n/ "Send via Email")

![Gemma 3n](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemma3n_Wagtial_RD2-V01.original.jpg)

Following the exciting launches of [Gemma 3](https://blog.google/technology/developers/gemma-3/) and [Gemma 3 QAT](https://developers.googleblog.com/en/gemma-3-quantized-aware-trained-state-of-the-art-ai-to-consumer-gpus/), our family of state-of-the-art open models capable of running on a single cloud or desktop accelerator, we're pushing our vision for accessible AI even further. Gemma 3 delivered powerful capabilities for developers, and we're now extending that vision to highly capable, real-time AI operating directly on the devices you use every day – your phones, tablets, and laptops.

To power the next generation of on-device AI and support a diverse range of applications, including advancing the capabilities of Gemini Nano, we engineered a new, cutting-edge architecture. This next-generation foundation was created in close collaboration with mobile hardware leaders like Qualcomm Technologies, MediaTek, and Samsung's System LSI business, and is optimized for lightning-fast, multimodal AI, enabling truly personal and private experiences directly on your device.

[Gemma 3n](https://deepmind.google/models/gemma/gemma-3n/) is our first open model built on this groundbreaking, shared architecture, allowing developers to begin experimenting with this technology today in an early preview. The same advanced architecture also powers the next generation of [Gemini Nano](https://deepmind.google/technologies/gemini/nano/), which brings these capabilities to a broad range of features in Google apps and our on-device ecosystem, and will become available later this year. Gemma 3n enables you to start building on this foundation that will come to major platforms such as Android and Chrome.

![Chatbot Arena Elo scores](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/image3_OjwrVp1.original.png)

This chart ranks AI models by Chatbot Arena Elo scores; higher scores (top numbers) indicate greater user preference. Gemma 3n ranks highly amongst both popular proprietary and open models.

Gemma 3n leverages a Google DeepMind innovation called Per-Layer Embeddings (PLE) that delivers a significant reduction in RAM usage. While the raw parameter count is 5B and 8B, this innovation allows you to run larger models on mobile devices or live-stream from the cloud, with a memory overhead comparable to a 2B and 4B model, meaning the models can operate with a dynamic memory footprint of just 2GB and 3GB. Learn more in our [documentation](https://ai.google.dev/gemma/docs/gemma-3n#parameters).

By exploring Gemma 3n, developers can get an early preview of the open model’s core capabilities and mobile-first architectural innovations that will be available on Android and Chrome with Gemini Nano.

In this post, we'll explore Gemma 3n's new capabilities, our approach to responsible development, and how you can access the preview today.

### **Key Capabilities of Gemma 3n**

Engineered for fast, low-footprint AI experiences running locally, Gemma 3n delivers:

* **Optimized On-Device Performance & Efficiency:** Gemma 3n starts responding approximately 1.5x faster on mobile with significantly better quality (compared to Gemma 3 4B) and a reduced memory footprint achieved through innovations like Per Layer Embeddings, KVC sharing, and advanced activation quantization.

* **Many-in-1 Flexibility:** A model with a 4B active memory footprint that natively includes a nested state-of-the-art 2B active memory footprint submodel (thanks to [MatFormer](https://arxiv.org/abs/2310.07707) training). This provides flexibility to dynamically trade off performance and quality on the fly without hosting separate models. We further introduce mix’n’match capability in Gemma 3n to dynamically create submodels from the 4B model that can optimally fit your specific use case -- and associated quality/latency tradeoff. Stay tuned for more on this research in our upcoming technical report.

* **Privacy-First & Offline Ready:** Local execution enables features that respect user privacy and function reliably, even without an internet connection.

* **Expanded Multimodal Understanding with Audio:** Gemma 3n can understand and process audio, text, and images, and offers significantly enhanced video understanding. Its audio capabilities enable the model to perform high-quality Automatic Speech Recognition (transcription) and Translation (speech to translated text). Additionally, the model accepts interleaved inputs across modalities, enabling understanding of complex multimodal interactions. (Public implementation coming soon)

* **Improved Multilingual Capabilities:** Improved multilingual performance, particularly in Japanese, German, Korean, Spanish, and French. Strong performance reflected on multilingual benchmarks such as 50.1% on WMT24++ (ChrF).

![MMLU performance](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Artboard_1.original.png)

This chart show’s MMLU performance vs model size of Gemma 3n’s mix-n-match (pretrained) capability.

### **Unlocking New On-the-go Experiences**

Gemma 3n will empower a new wave of intelligent, on-the-go applications by enabling developers to:

1. **Build live, interactive experiences** that understand and respond to real-time visual and auditory cues from the user's environment.

2. **Power deeper understanding** and contextual text generation using combined audio, image, video, and text inputs—all processed privately on-device.

3. **Develop advanced audio-centric applications**, including real-time speech transcription, translation, and rich voice-driven interactions.

Here’s an overview and the types of experiences you can build:

[Link to Youtube Video](https://www.youtube.com/watch?v=eJFJRyXEHZ0)
(visible only when JS is disabled)

### **Building Responsibly, Together**

Our commitment to responsible AI development is paramount. Gemma 3n, like all Gemma models, underwent rigorous safety evaluations, data governance, and fine-tuning alignment with our safety policies. We approach open models with careful risk assessment, continually refining our practices as the AI landscape evolves.

### **Get Started: Preview Gemma 3n Today**

We're excited to get Gemma 3n into your hands through a preview starting today:

**Initial Access (Available Now):**

* **Cloud-based Exploration with Google AI Studio:** Try Gemma 3n directly in your browser on [Google AI Studio](https://aistudio.google.com/app/prompts/new_chat?model=gemma-3n-e4b-it) – no setup needed. Explore its text input capabilities instantly.

* **On-Device Development with Google AI Edge:** For developers looking to integrate Gemma 3n locally, [Google AI Edge](https://developers.googleblog.com/en/google-ai-edge-small-language-models-multimodality-rag-function-calling) provides tools and libraries. You can get started with text and image understanding/generation capabilities today.

Gemma 3n marks the next step in democratizing access to cutting-edge, efficient AI. We’re incredibly excited to see what you’ll build as we make this technology progressively available, starting with today's preview.

Explore this announcement and all Google I/O 2025 updates on [io.google](https://io.google/2025/?utm_source=blogpost&utm_medium=pr&utm_campaign=event&utm_content=) starting May 22.

posted in:

* [Gemma](/en/search/?product_categories=Gemma)
* [AI](/en/search/?technology_categories=AI)
* [Announcements](/en/search/?content_type_categories=Announcements)
* [Industry Trends](/en/search/?content_type_categories=Industry+Trends)
* [Solutions](/en/search/?content_type_categories=Solutions)
* [Generative AI](/en/search/?tag=Generative AI)
* [Mobile App Development](/en/search/?tag=Mobile App Development)
* [multimodal AI](/en/search/?tag=multimodal AI)
* [Learn](/en/search/?tag=Learn)
* [Developer Tools](/en/search/?tag=Developer Tools)
* [open models](/en/search/?tag=open models)
* [Gemini Nano](/en/search/?tag=Gemini Nano)
* [on-device AI](/en/search/?tag=on-device AI)
* [Gemma 3 Nano](/en/search/?tag=Gemma 3 Nano)

Previous

Next

Related Posts

[![Unlocking the Power of the TPU Stack: Introducing our new Developer Hub](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/TPU_v5e_-_Board_4_-_Web.2e16d0ba.fill-800x400.jpg)

AI
Cloud
Announcements
Learn

Unlocking the Power of the TPU Stack: Introducing our new Developer Hub

JUNE 16, 2026](/en/unlocking-the-power-of-the-tpu-stack-introducing-our-new-developer-hub/)
[![Introducing EmbeddingGemma: The Best-in-Class Open Model for On-Device Embeddings](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/EmbeddingGemma_Metadatal_RD2-V01.2e16d0ba.fill-800x400.jpg)

Gemma
Mobile
AI
Announcements

Introducing EmbeddingGemma: The Best-in-Class Open Model for On-Device Embeddings

SEPT. 4, 2025](/en/introducing-embeddinggemma/)
[![Introducing Gemma 3 270M: The compact model for hyper-efficient AI](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemma3-270M_Metadata_RD2-V02.2e16d0ba.fill-800x400.jpg)

Gemma
AI
Announcements

Introducing Gemma 3 270M: The compact model for hyper-efficient AI

AUG. 14, 2025](/en/introducing-gemma-3-270m/)
[![Announcing the Agentic Resource Discovery specification](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemini_Generated_Image_gzxwoagzxwo.2e16d0ba.fill-800x400.jpg)

AI
Announcements
Learn

Announcing the Agentic Resource Discovery specification

JUNE 17, 2026](/en/announcing-the-agentic-resource-discovery-specification/)

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
