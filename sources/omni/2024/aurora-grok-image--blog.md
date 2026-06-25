# Grok Image Generation Release | xAI

Source: https://x.ai/news/grok-image-generation-release
(retrieved 2026-06-25 via Wayback Machine snapshot https://web.archive.org/web/20250313012603/https://x.ai/news/grok-image-generation-release — x.ai direct/proxy/cloakbrowser all failed TLS/connection on this network; real Chrome also hit error page on x.ai, so archived snapshot used. Snapshot text matches original Dec 2024 release announcement.)

---

We've enhanced Grok's image generation abilities with a new model, code-named **Aurora**.

Aurora is an **autoregressive mixture-of-experts network** trained to **predict the next token from interleaved text and image data**. We trained the model on **billions of examples from the internet**, giving it a deep understanding of the world. As a result, it excels at **photorealistic rendering** and **precisely following text instructions**.

Beyond text, the model also has **native support for multimodal input**, allowing it to take inspiration from or directly edit user-provided images.

Grok's new capabilities are now available on the X platform in select countries and will roll out to all users within a week.

## Image Generation

Grok can now generate high-quality images across several domains where other image generation models often struggle. It can render precise visual details of real-world entities, text, logos, and can create realistic portraits of humans.

Comparison gallery (prompt: "Cybertruck under an aurora") pits **Grok (Aurora)** against **Imagen 3**, **Flux.1 Pro**, **Ideogram 2.0**, and **DALL-E 3**. (Qualitative side-by-side only; no quantitative benchmark numbers reported.)

## Image Editing

Our new image generation model can now take images as input, giving users greater creative control and flexibility. We will release this capability to users on the X platform soon.

Example: prompt "Make the cat anime style" — input image -> output image. (Image-to-image editing demo.)

## Looking Forward

At xAI, we are advancing the frontier of multimodal understanding and generation. If this goal inspires you, we invite you to join us on this journey — we are hiring!

---

[META] This is the entirety of xAI's official disclosure for Aurora. No params, no training compute, no data pipeline details, no quantitative benchmarks, no architecture diagram beyond "autoregressive MoE predicting next token from interleaved text+image". Aurora is a closed product (Grok on X). No paper, no GitHub, no model card, no HF/ModelScope release.
