# The next chapter of the Gemini era for developers - Google Developers Blog
Source: https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/
The next chapter of the Gemini era for developers
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

[Gemini](/en/search/?product_categories=Gemini)

# The next chapter of the Gemini era for developers

DEC. 11, 2024

[Shrestha Basu Mallick](/en/search/?author=Shrestha+Basu+Mallick)
Product
Google DeepMind

[Kathy Korevec](/en/search/?author=Kathy+Korevec)
Director of Product
Google Labs

Share

* [Facebook](https://www.facebook.com/sharer/sharer.php?u=https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/ "Share on Facebook")
* [Twitter](https://twitter.com/intent/tweet?text=https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/ "Share on Twitter")
* [LinkedIn](https://www.linkedin.com/shareArticle?url=https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/&mini=true "Share on LinkedIn")
* [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/ "Send via Email")

![Gemini 2.0](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Gemini2.0_1.original.png)

We're giving developers the power to build the future of AI with cutting-edge models, intelligent tools to write code faster, and seamless integration across platforms and devices. Since last December when we launched Gemini 1.0, millions of developers have used [Google AI Studio](https://aistudio.google.com/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-L0) and [Vertex AI](https://cloud.google.com/vertex-ai/?utm_source=google_dev&utm_medium=blog&utm_campaign=gemini2_blog_launch&utm_content=) to [build with Gemini](https://ai.google.dev/showcase/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-L0-showcase) across 109 languages.

Today, we are announcing [Gemini 2.0](http://deepmind.google/technologies/gemini) Flash Experimental to enable even more immersive and interactive applications, as well as new coding agents that will enhance workflows by taking action on behalf of the developer.

## Build with Gemini 2.0 Flash

Building on the success of Gemini 1.5 Flash, Flash 2.0 is twice as fast as 1.5 Pro while achieving stronger [performance](https://deepmind.google/technologies/gemini/flash/), includes new multimodal outputs, and comes with native tool use. We’re also introducing a Multimodal Live API for building dynamic applications with real-time audio and video streaming.

Starting today, developers can test and explore Gemini 2.0 Flash via the [Gemini API](https://ai.google.dev/gemini-api/docs?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-L0-docs) in [Google AI Studio](https://aistudio.google.com/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-L0) and [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/freeform?model=gemini-2.0-flash-exp) during its experimental phase, with general availability coming early next year.

With Gemini 2.0 Flash, developers have access to:

### **1. Better performance**

Gemini 2.0 Flash is more powerful than 1.5 Pro while still delivering on the speed and efficiency that developers expect from Flash. It also features improved multimodal, text, code, video, spatial understanding and reasoning performance on key [benchmarks](http://deepmind.google/technologies/gemini). Improved spatial understanding enables more accurate bounding boxes generation on small objects in cluttered images, and better object identification and captioning. Learn more in the [spatial understanding video](https://youtu.be/-XmoDzDMqj4) or read the [Gemini API docs](https://ai.google.dev/gemini-api/docs/models/gemini-v2#bounding-box).

[Link to Youtube Video](https://www.youtube.com/watch?v=-XmoDzDMqj4)
(visible only when JS is disabled)

### **2. New output modalities**

Developers will be able to use Gemini 2.0 Flash to generate integrated responses that can include text, audio, and images — all through a single API call. These new output modalities are available to early testers, with wider rollout expected next year. [SynthID](https://ai.google.dev/responsible/docs/safeguards/synthid/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-L0-synthid) invisible watermarks will be enabled in all image and audio outputs, helping decrease misinformation and misattribution concerns.

* **Multilingual native audio output:** Gemini 2.0 Flash features native text-to-speech audio output that provides developers fine-grained control over not just *what* the model says, but *how* it says it, with a choice of 8 high-quality voices and a range of languages and accents. [Hear native audio output](https://www.youtube.com/watch?v=qE673AY-WEI) in action or read more in the [developer docs](https://ai.google.dev/gemini-api/docs/models/gemini-v2).

* **Native image output:** Gemini 2.0 Flash now natively generates images and supports conversational, multi-turn editing, so you can build on previous outputs and refine them. It can output interleaved text and images, making it useful in multimodal content such as recipes. See more in the [native image output video](https://youtu.be/7RqFLp0TqV0).

[Link to Youtube Video](https://www.youtube.com/watch?v=7RqFLp0TqV0)
(visible only when JS is disabled)

### **3. Native tool use**

Gemini 2.0 has been trained to use tools–a foundational capability for building agentic experiences. It can natively call tools like Google Search and code execution in addition to custom third-party functions via function calling. Using Google Search natively as a tool leads to more factual and comprehensive answers and increases traffic to publishers. Multiple searches can be run in parallel leading to improved information retrieval by finding more relevant facts from multiple sources simultaneously and combining them for accuracy. Learn more in the [native tool use video](https://youtu.be/EVzeutiojWs) or start building from a [notebook](https://github.com/google-gemini/cookbook/blob/main/gemini-2/search_tool.ipynb).

[Link to Youtube Video](https://www.youtube.com/watch?v=EVzeutiojWs)
(visible only when JS is disabled)

### **4. Multimodal Live API**

Developers can now build real-time, multimodal applications with audio and video-streaming inputs from cameras or screens. Natural conversational patterns like interruptions and voice activity detection are supported. The API supports the integration of multiple tools together to accomplish complex use cases with a single API call. WebRTC SDK partner integration allows developers to build across platforms, at scale. See more in the [multimodal live streaming video](https://youtu.be/9hE5-98ZeCg), try the [web console](https://github.com/google-gemini/multimodal-live-api-web-console), or [starter code](https://github.com/google-gemini/cookbook/tree/main/gemini-2) (Python).

[Link to Youtube Video](https://www.youtube.com/watch?v=9hE5-98ZeCg)
(visible only when JS is disabled)

We’re thrilled to see startups making impressive progress with Gemini 2.0 Flash, prototyping new experiences like [tldraw's](http://ai.google.dev/showcase/tldraw) visual playground, [Viggle's](http://ai.google.dev/showcase/viggle) virtual character creation and audio narration, [Toonsutra's](http://ai.google.dev/showcase/toonsutra) contextual multilingual translation, and [Rooms'](http://ai.google.dev/showcase/rooms) adding real-time audio.

To jumpstart building, we’ve released [three starter app](https://aistudio.google.com/app/starter-apps/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-starterapps) experiences in [Google AI Studio](https://aistudio.google.com/app/starter-apps/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-starterapps) along with open source code for spatial understanding, video analysis and Google Maps exploration so you can begin building with Gemini 2.0 Flash.

## Enabling the evolution of AI code assistance

As AI code assistance rapidly evolves from simple code searches to AI-powered assistants embedded in developer workflows, we want to share the latest advancement that will use Gemini 2.0: coding agents that can execute tasks on your behalf.

In our latest research, we've been able to use 2.0 Flash equipped with code execution tools to achieve 51.8% on SWE-bench Verified, which tests agent performance on real-world software engineering tasks. The cutting edge inference speed of 2.0 Flash allowed the agent to sample hundreds of potential solutions, selecting the best based on existing unit tests and Gemini's own judgment. We're in the process of turning this research into new developer products.

### **Meet Jules, your AI-powered code agent**

Imagine your team has just finished a bug bash, and now you’re staring down a long list of bugs. Starting today, you can offload Python and Javascript coding tasks to Jules, an experimental AI-powered code agent that will use Gemini 2.0. Working asynchronously and integrated with your GitHub workflow, Jules handles bug fixes and other time-consuming tasks while you focus on what you actually want to build. Jules creates comprehensive, multi-step plans to address issues, efficiently modifies multiple files, and even prepares pull requests to land fixes directly back into GitHub.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-t7_gawuz_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/Jules_GIF_3D_10_1.mp4)
[Jules tackling an issue, developing a plan, and executing it (Sequences shortened. Results for illustrative purposes. Jules may make mistakes.)](https://www.youtube.com/watch?v=DjJL9XGXVGY)

It’s early, but from our internal experience using Jules, it’s giving developers:

* **More productivity.** Assign issues and coding tasks to Jules for asynchronous coding efficiency.

* **Progress tracking.** Stay informed and prioritize tasks that require your attention with real-time updates.

* **Full developer control.** Review the plans Jules creates along the way, and provide feedback or request adjustments as you see fit. Easily review and, if appropriate, merge the code Jules writes into your project.

We’re making Jules available for a select group of trusted testers today, and we’ll make it available for other interested developers in early 2025. Sign up to get updates about Jules on [labs.google.com/jules](http://labs.google.com/jules).

### **Colab's data science agent will create notebooks for you**

At I/O this year, we launched an experimental Data Science Agent on [labs.google/code](http://labs.google/code) that allows anyone to upload a dataset and get insights within minutes, all grounded in a working Colab notebook. We were thrilled to receive such positive feedback from the developer community and see the impact. For example, with the help of Data Science Agent, a scientist at Lawrence Berkeley National Laboratory working on a global tropical wetland methane emissions project has estimated their analysis and processing time was reduced from one week to five minutes.

Colab has started to integrate these same agentic capabilities, using Gemini 2.0. Simply describe your analysis goals in plain language, and watch your notebook take shape automatically, helping accelerate your ability to conduct research and data analysis. Developers can get early access to this new feature by joining the [trusted tester program](https://forms.gle/UQWKGrhFqVRLmJGy5) before it rolls out more widely to Colab users in the first half of 2025.

[![


Sorry, your browser doesn't support playback for this video

](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/wagtailvideo-226_snh3_thumb.jpg)](https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/DSA_Colab_All_Reduced.mp4)
[Colab’s data science agent uses Gemini 2.0 to create a notebook from natural language instructions](https://youtu.be/p1pYoT9wsyM)

## Developers are building the future

Our Gemini 2.0 models can empower you to build more capable AI apps faster and easier, so you can focus on great experiences for your users. We'll be bringing Gemini 2.0 to our platforms like [Android Studio](https://developer.android.com/gemini-in-android), [Chrome DevTools](https://developer.chrome.com/docs/devtools/ai-assistance/quickstart) and [Firebase](https://firebase.google.com/products/generative-ai) in the coming months. Developers can [sign up](https://docs.google.com/forms/d/e/1FAIpQLSc1yAQ8aJeUUHjlLjuEVmanVvoS_YFUmHtwsetl6GXVg-U0Jw/viewform) to use Gemini 2.0 Flash in [Gemini Code Assist](https://cloud.google.com/products/gemini/code-assist/?utm_source=google_dev&utm_medium=blog&utm_campaign=gemini2_blog_launch&utm_content=), for enhanced coding assistance capabilities in popular IDEs such as Visual Studio Code, IntelliJ, PyCharm and more. Visit [ai.google.dev](https://ai.google.dev/?utm_source=gfd&utm_medium=referral&utm_campaign=blog-dec&utm_content=gemini2-L1) to get started and follow [Google AI for Developers](https://x.com/googleaidevs) for future updates.

posted in:

* [Gemini](/en/search/?product_categories=Gemini)
* [AI](/en/search/?technology_categories=AI)
* [Announcements](/en/search/?content_type_categories=Announcements)
* [Industry Trends](/en/search/?content_type_categories=Industry+Trends)
* [Explore](/en/search/?tag=Explore)
* [Google Cloud Vertex AI](/en/search/?tag=Google Cloud Vertex AI)
* [Google AI Studio](/en/search/?tag=Google AI Studio)

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
