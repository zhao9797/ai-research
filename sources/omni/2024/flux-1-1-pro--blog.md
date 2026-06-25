# Announcing FLUX1.1 [pro] and the BFL API

Source: https://bfl.ai/blog/24-10-02-flux
Published: 2024-10-02
Fetched via Chrome MCP (bfl.ai is a JS SPA; curl/cloakbrowser blocked by network in this env)

---

Today, we release FLUX1.1 [pro], our most advanced and efficient model yet, alongside the general availability of the beta BFL API. This release marks a significant step forward in our mission to empower creators, developers, and enterprises with scalable, state-of-the-art generative technology.

## FLUX1.1 [pro]: Faster & Better

FLUX1.1 [pro] provides six times faster generation than its predecessor FLUX.1 [pro] while also improving image quality, prompt adherence, and diversity. At the same time, we updated FLUX.1 [pro] to generate the same output as before, but two times faster.

- Superior Speed and Efficiency: Faster generation times and reduced latency, enabling more efficient workflows. FLUX1.1 [pro] provides an ideal tradeoff between image quality and inference speed. FLUX1.1 [pro] is three times faster than the currently available FLUX.1 [pro].
- Improved Performance: FLUX1.1 [pro] has been introduced and tested under the codename "blueberry" into the Artificial Analysis image arena (https://artificialanalysis.ai/text-to-image), a popular benchmark for text-to-image models. It surpasses all other models on the leaderboard, achieving the highest overall Elo score.
- All metrics from artificialanalysis.ai as of Oct 1, 2024, except FLUX.1 inference speeds (benchmarked internally).
- Fast High-res coming soon: FLUX1.1 [pro], natively set up for fast ultra high-resolution generation coming soon to the API. Generate up to 2k images without sacrificing any of the prompt following.

We are excited to announce that FLUX1.1 [pro] will also be available through Together.ai, Replicate, fal.ai, and Freepik.

## Building with the BFL API

Our new beta BFL API brings FLUX's capabilities directly to developers and businesses looking to integrate state-of-the-art image generation into their own applications. Our API stands out with key advantages over competitors:

- Advanced Customization: Tailor the API outputs to your specific needs with customization options on model choice, image resolution, and content moderation.
- Scalability: Seamlessly scale your applications, whether you are building small projects or enterprise-level applications.
- Competitive pricing: The API offers superior image quality at a lower cost. The pricing for our FLUX.1 model suite is as follows:
  - FLUX.1 [dev]: 2.5 cts/img
  - FLUX.1 [pro]: 5 cts/img
  - FLUX1.1 [pro]: 4 cts/img

Get started with the BFL API today at: docs.bfl.ml.
