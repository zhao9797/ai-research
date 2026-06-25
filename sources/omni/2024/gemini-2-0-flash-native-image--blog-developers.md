# The next chapter of the Gemini era for developers

Source: https://developers.googleblog.com/en/the-next-chapter-of-the-gemini-era-for-developers/
Authors: Shrestha Basu Mallick, Kathy Korevec
Date: DEC. 11, 2024
Fetched via: chrome MCP (chrome_get_web_content), 2026-06-25 (curl/cloakbrowser blocked by network/proxy)

---

DEC. 11, 2024 — We're giving developers the power to build the future of AI with cutting-edge models, intelligent tools to write code faster, and seamless integration across platforms and devices. Since last December when we launched Gemini 1.0, millions of developers have used Google AI Studio and Vertex AI to build with Gemini across 109 languages.

Today, we are announcing Gemini 2.0 Flash Experimental to enable even more immersive and interactive applications, as well as new coding agents that will enhance workflows by taking action on behalf of the developer.

## Build with Gemini 2.0 Flash

Building on the success of Gemini 1.5 Flash, Flash 2.0 is twice as fast as 1.5 Pro while achieving stronger performance, includes new multimodal outputs, and comes with native tool use. We're also introducing a Multimodal Live API for building dynamic applications with real-time audio and video streaming.

Starting today, developers can test and explore Gemini 2.0 Flash via the Gemini API in Google AI Studio and Vertex AI during its experimental phase, with general availability coming early next year.

With Gemini 2.0 Flash, developers have access to:

### 1. Better performance
Gemini 2.0 Flash is more powerful than 1.5 Pro while still delivering on the speed and efficiency that developers expect from Flash. It also features improved multimodal, text, code, video, spatial understanding and reasoning performance on key benchmarks. Improved spatial understanding enables more accurate bounding boxes generation on small objects in cluttered images, and better object identification and captioning.

### 2. New output modalities
Developers will be able to use Gemini 2.0 Flash to generate integrated responses that can include text, audio, and images — all through a single API call. These new output modalities are available to early testers, with wider rollout expected next year. **SynthID invisible watermarks will be enabled in all image and audio outputs**, helping decrease misinformation and misattribution concerns.

- **Multilingual native audio output:** Gemini 2.0 Flash features native text-to-speech audio output that provides developers fine-grained control over not just what the model says, but how it says it, with a choice of **8 high-quality voices** and a range of languages and accents.
- **Native image output:** Gemini 2.0 Flash **now natively generates images and supports conversational, multi-turn editing**, so you can build on previous outputs and refine them. It can output **interleaved text and images**, making it useful in multimodal content such as recipes.

### 3. Native tool use
Gemini 2.0 has been trained to use tools — a foundational capability for building agentic experiences. It can natively call tools like Google Search and code execution in addition to custom third-party functions via function calling. Using Google Search natively as a tool leads to more factual and comprehensive answers and increases traffic to publishers. Multiple searches can be run in parallel leading to improved information retrieval.

### 4. Multimodal Live API
Developers can now build real-time, multimodal applications with audio and video-streaming inputs from cameras or screens. Natural conversational patterns like interruptions and voice activity detection are supported. The API supports the integration of multiple tools together to accomplish complex use cases with a single API call. WebRTC SDK partner integration allows developers to build across platforms, at scale.

Startups: tldraw's visual playground, Viggle's virtual character creation and audio narration, Toonsutra's contextual multilingual translation, and Rooms' adding real-time audio.

Three starter app experiences released in Google AI Studio along with open source code for spatial understanding, video analysis and Google Maps exploration.

## Enabling the evolution of AI code assistance

In our latest research, we've been able to use 2.0 Flash equipped with code execution tools to achieve **51.8% on SWE-bench Verified**, which tests agent performance on real-world software engineering tasks. The cutting edge inference speed of 2.0 Flash allowed the agent to sample hundreds of potential solutions, selecting the best based on existing unit tests and Gemini's own judgment.

## Meet Jules, your AI-powered code agent
(experimental AI-powered code agent using Gemini 2.0, GitHub workflow integration, Python/Javascript)

## Colab's data science agent
(agentic notebook generation using Gemini 2.0)

We'll be bringing Gemini 2.0 to Android Studio, Chrome DevTools and Firebase. Gemini Code Assist for VS Code, IntelliJ, PyCharm.
