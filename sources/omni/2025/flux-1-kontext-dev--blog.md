# FLUX.1 Kontext [dev] - Open Weights for Image Editing | Black Forest Labs
Source: https://bfl.ai/blog/flux-1-kontext-dev
FLUX.1 Kontext [dev] - Open Weights for Image Editing | Black Forest Labs

* Models
* [Research](/research)
* API
* Open Weights
* [Enterprise](/enterprise)
* Resources

[Contact Sales](/contact)[Get started](https://dashboard.bfl.ai/?landing_page=%2Fblog%2Fflux-1-kontext-dev)

[Back to index](/blog)

June 26, 2025

# FLUX.1 Kontext [dev] - Open Weights for Image Editing

News
![FLUX.1 Kontext [dev] - Open Weights for Image Editing](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2Fa614f1e0c390a90030dec53542b14b7d775d7ee3-1559x641.jpg&w=3840&q=75)

Up until today, all capable generative image editing models were only available as proprietary tools. Today, that changes. We release FLUX.1 Kontext [dev], our developer version of [FLUX.1 Kontext [pro]](https://bfl.ai/models/flux-kontext), which delivers proprietary-level image editing performance in a 12B parameter model that can run on consumer hardware.

Making model weights openly accessible is fundamental to technological innovation. [FLUX.1 Kontext [dev]](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev) is now available as an open-weight model under the FLUX.1 Non-Commercial License, providing free access for research and non-commercial use. FLUX.1 Kontext [dev] is compatible with the existing FLUX.1 [dev] inference code and comes with day-0 support for popular inference frameworks like ComfyUI, HuggingFace Diffusers and TensorRT.

The model weights are available on [HuggingFace](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev). Our partners [FAL](https://fal.ai/models/fal-ai/flux-kontext/dev), [Replicate](https://replicate.com/black-forest-labs/flux-kontext-dev), [Runware](https://runware.ai/models#flux), [DataCrunch](https://datacrunch.io/managed-endpoints/flux-kontext) and [TogetherAI](https://www.together.ai/models/flux-1-kontext-dev) and [ComfyUI](https://www.comfy.org/) provide ready-to-use API endpoints and code for cloud-based and/or local inference.

The technical report is available [on arxiv](https://arxiv.org/abs/2506.15742).

### Setting New Standards in Open Image Editing

FLUX.1 Kontext [dev] focuses exclusively on editing tasks. The model enables iterative editing, excels at character preservation across a diverse set of scenes and environments, and allows both precise local and global edits.

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F5c1d3cd134efe3be87a6b505571cd4d497db2705-2548x490.png&w=3840&q=75)

At Black Forest Labs, we remain committed to providing researchers and developers with best-in-class open tools that are competitive with existing proprietary solutions. To validate the performance of FLUX.1 Kontext [dev], we conducted extensive evaluation across multiple image editing benchmarks.

Human preference evaluations on [KontextBench](https://huggingface.co/datasets/black-forest-labs/kontext-bench), our newly released image editing benchmark, demonstrate that FLUX.1 Kontext [dev] outperforms existing open image editing models, (Bytedance Bagel, HiDream-E1-Full) and closed models (Google's Gemini-Flash Image) across many categories. Independent evaluations run by [Artificial Analysis](http://artificialanalysis.ai/text-to-image/arena?tab=leaderboard&input=image) confirm these findings.

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2F525f3920273479af0842e215e1de47d9db6f3a05-1518x1273.png&w=3840&q=75)

### Optimized for NVIDIA Blackwell Architecture

We have collaborated with NVIDIA to build optimized TensorRT weights specifically designed for the new [NVIDIA Blackwell](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/?ncid=pa-srch-goog-139553) architecture which brings greatly improved inference speed and reduces memory usage while maintaining high-quality image editing performance.

![](/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2F2gpum2i6%2Fproduction%2Fc3a527f3d6491f75d9741c0bf12c04c9770c129f-2293x1274.png&w=3840&q=75)

Additionally to the original FLUX.1 Kontext [dev] weights, we’re making available these BF16, FP8 and FP4 TensorRT variants in our [Hugging Face repository](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev-onnx), giving developers the flexibility to balance speed, efficiency, and quality tailored to their use case. These optimized weights ensure that FLUX.1 Kontext [dev] can take full advantage of the latest hardware capabilities.

### Streamlined Commercial Access: The BFL Self-Serve Portal

We are releasing a [self-serve licensing portal](http://bfl.ai/pricing/licensing) with transparent terms and standardized commercials for simplifying commercial access to all of our open weights models. This includes the novel FLUX.1 Kontext [dev] as well as the FLUX.1 Tools [dev] and the popular text-to-image model FLUX.1 [dev].

Our self-serve portal provides transparent licensing terms that enable businesses to confidently integrate FLUX.1 models into their commercial products and services. Commercial Licenses to our open weights models can now be purchased with only a few clicks, accelerating the path from development to deployment. More information on self-serve licensing can be found at the [BFL Helpdesk](https://help.bfl.ai/collections/6939000511-licensing).

### License Update

Black Forest Labs also updated the [FLUX.1 [dev] Non-Commercial License](https://bfl.ai/legal/self-hosted-commercial-license-terms) with the following changes:

1. **Non-Commercial Purpose.** We edited the definition of “Non-Commercial Purpose” to better clarify what constitutes Non-Commercial Purposes under the FLUX.1 [dev] Non-Commercial License.
2. **Content Filters.** To prevent the creation and dissemination of unlawful or infringing content, the FLUX.1 [dev] Non-Commercial License requires content filters or manual review to be used with the FLUX.1 [dev] models. We’ve also made corresponding adjustments to the indemnification of the license.
3. **Content Provenance.** Users of FLUX.1 [dev] Models under a FLUX.1 [dev] Non-Commercial License must follow applicable law for content provenance under the license.
4. **Restrictions.** We made some clarifications on what are not permitted uses of FLUX.1 [dev] Models under a FLUX.1 [dev] Non-Commercial License.

### Resources

* Model weights: <https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev>
* Code: <https://github.com/black-forest-labs/flux>
* API Documentation: <https://docs.bfl.ai/quick_start/introduction>
* Self-Serve Portal: <http://bfl.ai/pricing/licensing>
* Helpdesk: [https://help.bfl.ai](https://help.bfl.ai/)

*We're just getting started. If you want to join us on our mission, we are actively hiring talented individuals across multiple roles. Apply* [*here.*](https://job-boards.greenhouse.io/blackforestlabs)

Previous article[Introducing FLUX.1 Kontext and the BFL Playground](/blog/flux-1-kontext)

Next article[FLUX.1 Krea [dev]: An ‘Opinionated’ Text-to-Image Model](/blog/flux-1-krea-dev)

![](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fbg-footer.c5582a35.png&w=3840&q=75&dpl=dpl_BhmvaEa9MS3ThkDo1YH7YVDvxZBK)

Models

[FLUX.2 Max](/models/flux-2-max)[FLUX.2](/models/flux-2)[FLUX.2 Klein](/models/flux-2-klein)[Flux Tools](/models/flux-tools)

API

[Documentation](https://docs.bfl.ai)[Pricing](/pricing)[Dashboard](https://dashboard.bfl.ai)[Status](https://status.bfl.ai)

Open Weights

[Licensing](/licensing)[Hugging Face](https://huggingface.co/black-forest-labs)[GitHub](https://github.com/black-forest-labs/flux)

Resources

[Documentation](https://docs.bfl.ai)[Help Desk](https://help.bfl.ai)[Blog](/blog)[Creator Program](/creator-program)[Brand](/brand)[GitHub](https://github.com/black-forest-labs)

Company

[About Us](/about)[Careers](/careers)[Trust and Security](https://app.vanta.com/blackforestlabs.ai/trust/0cb6ffww8qmy60nxzo3p5)[Contact Us](/contact)

 [ISO 27001:2022](https://app.vanta.com/blackforestlabs.ai/trust/0cb6ffww8qmy60nxzo3p5)

[SOC 2 Type II](https://app.vanta.com/blackforestlabs.ai/trust/0cb6ffww8qmy60nxzo3p5)

Enterprise

[Learn More](/enterprise)[Contact Sales](/contact)

Legal

[Imprint](/legal/imprint)[Terms of Service](/legal/terms-of-service)[Usage Policy](/legal/usage-policy)[Privacy Policy](/legal/privacy-policy)[Intellectual Property Policy](/legal/intellectual-property-policy)

[Developer Terms of Service](/legal/developer-terms-of-service)[FLUX API Service Terms](/legal/flux-api-service-terms)[Self-Hosted Terms of Service](/legal/self-hosted-commercial-license-terms)[Non-Commercial License Terms](/legal/non-commercial-license-terms)[Responsible AI Development Policy](/legal/responsible-ai-development-policy)[Training Data Disclosure](/transparency)

All rights reserved.

©2026 BLACK FOREST LABS.
