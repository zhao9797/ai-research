# Experiment with Gemini 2.0 Flash native image generation

Source: https://developers.googleblog.com/en/experiment-with-gemini-20-flash-native-image-generation/
Authors: Kat Kampf, Nicole Brichtova
Date: MARCH 12, 2025
Fetched via: chrome MCP, 2026-06-25
(Follow-up to the Dec 11 2024 launch — public developer rollout of the native image generation capability first announced Dec 2024. Included because the Dec 2024 work was the "起点/starting point" and this blog details the capability concretely.)

---

MARCH 12, 2025 — In December we first introduced native image output in Gemini 2.0 Flash to trusted testers. Today, we're making it available for developer experimentation across all regions currently supported by Google AI Studio. You can test this new capability using an experimental version of Gemini 2.0 Flash (`gemini-2.0-flash-exp`) in Google AI Studio and via the Gemini API.

Gemini 2.0 Flash combines multimodal input, enhanced reasoning, and natural language understanding to create images.

Examples where 2.0 Flash's multimodal outputs shine:

1. **Text and images together** — Tell a story and it will illustrate it with pictures, keeping characters and settings consistent throughout. Give feedback and the model will retell the story or change the style of its drawings. (Story + illustration generation in Google AI Studio)

2. **Conversational image editing** — Edit images through many turns of a natural language dialogue, great for iterating towards a perfect image. (Multi-turn conversation image editing maintaining context throughout)

3. **World understanding** — Unlike many other image generation models, Gemini 2.0 Flash leverages world knowledge and enhanced reasoning to create the right image. Perfect for creating detailed imagery that's realistic — like illustrating a recipe. While it strives for accuracy, like all language models, its knowledge is broad and general, not absolute or complete. (Interleaved text and image output for a recipe)

4. **Text rendering** — Most image generation models struggle to accurately render long sequences of text, often resulting in poorly formatted or illegible characters, or misspellings. **Internal benchmarks show that 2.0 Flash has stronger rendering compared to leading competitive models** — great for creating advertisements, social posts, or even invitations.

Code:
```python
from google import genai
from google.genai import types
client = genai.Client(api_key="GEMINI_API_KEY")
response = client.models.generate_content(
    model="gemini-2.0-flash-exp",
    contents=("Generate a story about a cute baby turtle in a 3d digital art style. "
              "For each scene, generate an image."),
    config=types.GenerateContentConfig(
        response_modalities=["Text", "Image"]
    ),
)
```

"Gemini 2.0 Flash allows you to add text and image generation with just a single model." Feedback will help finalize a production-ready version soon.
