Update available: cloakbrowser 0.3.31 → 0.4.3. Run: pip install --upgrade cloakbrowser
# Advancing Physical AI with NVIDIA Cosmos World Foundation Model Platform | NVIDIA Technical Blog
Source: https://developer.nvidia.com/blog/advancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform/
Advancing Physical AI with NVIDIA Cosmos World Foundation Model Platform | NVIDIA Technical Blog




[![Home](https://developer-blogs.nvidia.com/wp-content/themes/nvidia/dist/images/nvidia-logo_28b633c7.svg)](/ "Home")
[DEVELOPER](/ "Home")

* [Home](/ "Home")
* [Blog](/blog "Blog")
* [Forums](https://forums.developer.nvidia.com/ "Forums")
* [Docs](https://docs.nvidia.com/ "Docs")
* [Downloads](https://developer.nvidia.com/downloads "Downloads")
* [Training](https://www.nvidia.com/en-us/training/ "Training")




* [Join](https://developer.nvidia.com/login)

[Technical Blog](https://developer.nvidia.com/blog)

[Subscribe](https://developer.nvidia.com/email-signup)

[Related Resources](#main-content-end)

[Top Stories](https://developer.nvidia.com/blog/category/features/)



English한국어中文

# Advancing Physical AI with NVIDIA Cosmos World Foundation Model Platform

![](https://developer-blogs.nvidia.com/wp-content/uploads/2025/01/hardhat-composite-nvidia-cosmos-workflow-1024x576.jpg)

Jan 09, 2025

By [Pranjali Joshi](https://developer.nvidia.com/blog/author/pranjalij/ "Posts by Pranjali Joshi")

+28

Like

[Discuss (1)](#entry-content-comments)

* [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)
* [T](https://twitter.com/intent/tweet?text=Advancing+Physical+AI+with+NVIDIA+Cosmos+World+Foundation+Model+Platform+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)
* [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)
* [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F&title=Advancing+Physical+AI+with+NVIDIA+Cosmos+World+Foundation+Model+Platform+%7C+NVIDIA+Technical+Blog)
* [E](mailto:?subject=I'd like to share a link with you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)

AI-Generated Summary

Like

Dislike

* NVIDIA Cosmos is a platform that helps developers build custom world models for physical AI systems, offering open world foundation models and tools for data curation, training, and customization.
* Cosmos world foundation models are pretrained large generative AI models trained on 9,000 trillion tokens, creating realistic synthetic videos of environments and interactions for training complex systems.
* The platform includes tools like NVIDIA NeMo Curator for efficient video data curation, Cosmos Tokenizer for high-fidelity video tokenization, and NVIDIA NeMo Framework for model training and optimization.
* Cosmos world foundation models have shown strong adherence to physical laws in evaluations, with metrics such as 3D consistency and physics alignment, and can be fine-tuned for specific applications like autonomous driving or humanoid robotics.
* Developers can access Cosmos world foundation models on NGC and Hugging Face, and utilize additional tools like Cosmos tokenizers on GitHub and Hugging Face, with some features available on the NVIDIA API catalog.

AI-generated content may summarize information incompletely. Verify important information. [Learn more](https://www.nvidia.com/en-us/agreements/trustworthy-ai/terms/)

As robotics and autonomous vehicles advance, accelerating development of [physical AI](https://www.nvidia.com/en-us/glossary/generative-physical-ai/)—which enables [autonomous machines](https://www.nvidia.com/en-us/autonomous-machines/) to perceive, understand, and perform complex actions in the physical world—has become essential. At the center of these systems are [world foundation models (WFMs)](https://www.nvidia.com/en-us/glossary/world-models/)—AI models that simulate physical states through physics-aware videos, enabling machines to make accurate decisions and interact seamlessly with their surroundings.

[NVIDIA Cosmos](https://nvidianews.nvidia.com/news/nvidia-launches-cosmos-world-foundation-model-platform-to-accelerate-physical-ai-development) is a platform that helps developers build custom world models for physical AI systems at scale. It offers [open world foundation models](https://blogs.nvidia.com/blog/cosmos-world-foundation-models/) and tools for every stage of development, from data curation to training to customization.

*Video 1. NVIDIA Cosmos: A World Foundation Model Platform for Physical AI*

This post explains Cosmos and its key features that accelerate physical AI development.

## Accelerating world model development with NVIDIA Cosmos

Building physical AI is challenging, demanding precise simulations and real-world behavior understanding and prediction. A key tool for overcoming these challenges is a world model, which predicts future environmental states based on past observations and current inputs. These models are invaluable for physical AI builders, enabling them to simulate, train, and refine systems in controlled environments.

However, developing effective world models requires vast amounts of data, computational power, and real-world testing, which can introduce significant safety risks, logistical hurdles, and prohibitive costs. To address these challenges, developers often turn to [synthetic data](https://www.nvidia.com/en-us/use-cases/synthetic-data/) generated from [3D simulations](https://developer.nvidia.com/isaac/sim) to train models. While synthetic data is a powerful tool, creating it is resource-intensive and may fall short of accurately reflecting real-world physics, particularly in complex or edge-case scenarios.

The [end-to-end NVIDIA Cosmos platform](https://developer.nvidia.com/cosmos) accelerates world model development for physical AI systems. Built on CUDA, Cosmos combines state-of-the-art world foundation models, video tokenizers, and AI-accelerated data processing pipelines.

Developers can accelerate world model development by fine-tuning Cosmos world foundation models or building new ones from the ground up. In addition to Cosmos world foundation models, the platform also includes:

* [NVIDIA NeMo Curator](https://developer.nvidia.com/nemo-curator/) for efficient video data curation
* [Cosmos Tokenizer](https://developer.nvidia.com/blog/state-of-the-art-multimodal-generative-ai-model-development-with-nvidia-nemo/) for efficient, compact, and high-fidelity video tokenization
* Cosmos world foundation models pretrained for robotics and autonomous driving applications
* [NVIDIA NeMo Framework](https://docs.nvidia.com/nemo-framework/user-guide/latest/overview.html) for model training and optimization

![Diagram showing NVIDIA Cosmos platform that includes Cosmos world foundation models, NeMo Curator, Cosmos tokenizers and NeMo Framework.
](https://developer-blogs.nvidia.com/wp-content/uploads/2025/01/nvidia-cosmos.jpg)


**Figure 1. NVIDIA Cosmos is a world foundation model development platform with generative models, data curator, tokenizer, and framework to accelerate physical AI development**

### **Pretrained world foundation models for physical AI**

Cosmos world foundation models are pretrained large generative AI models trained on 9,000 trillion tokens—including 20 million hours of data from [autonomous driving](https://www.nvidia.com/en-us/use-cases/autonomous-vehicle-simulation/), [robotics](https://www.nvidia.com/en-us/solutions/robotics-and-edge-computing/), synthetic environments, and other related domains. These models create realistic synthetic videos of environments and interactions, providing a scalable foundation for training complex systems, from simulating [humanoid robots](https://www.nvidia.com/en-us/use-cases/humanoid-robots/) performing advanced actions to developing end-to-end autonomous driving models.

These models use two architectures: autoregressive and diffusion. Both approaches use the transformer architecture for its scalability and effectiveness in handling complex temporal dependencies.

#### Autoregressive model

Cosmos autoregressive model is designed for video generation, predicting the next token based on input text and past video frames. It uses a transformer decoder architecture, with key modifications for world model development.

* 3D RoPE (Rotary Position Embeddings) encodes spatial and temporal dimensions separately, ensuring precise video sequence representation.
* Cross-attention layers enable text inputs, providing better control over world generation.
* QK-normalization enhances training stability.

Pretraining of this model is progressive, starting with predicting up to 17 future frames from a single input frame, then extending to 34 frames, and eventually up to 121 frames (or 50,000 tokens). Text inputs are introduced to combine descriptions with video frames, and the model is fine-tuned with high-quality data for robust performance. This structured approach enables the model to generate videos of varying lengths and complexities, with or without text inputs.

![Autoregressive model architecture including text embedding, discrete tokenizer, and cross-attention layers.
](https://developer-blogs.nvidia.com/wp-content/uploads/2025/01/nvidia-cosmos-autoregressive-model-architecture.png)


*Figure 2. The Cosmos autoregressive model uses a transformer decoder architecture, with key modifications for world model development*

#### Diffusion models

[Diffusion models](https://developer.nvidia.com/blog/understanding-diffusion-models-an-essential-guide-for-aec-professionals/) are popular for generating images, videos, and audio due to their ability to deconstruct training data and reconstruct it based on user input, producing high-quality, realistic outputs.

Diffusion models operate in two phases:

1. **Forward diffusion process:** Training data is progressively corrupted by adding Gaussian noise over multiple steps, effectively transforming it into pure noise.
2. **Reverse diffusion process:** The model learns to reverse this noise step by step, recovering the original data by denoising the corrupted input.

Once trained, diffusion models generate new data by sampling random Gaussian noise and passing it through the learned denoising process. In addition, Cosmos diffusion models also get several key updates tailored for physical AI development.

* 3D patchification processes video into smaller patches, simplifying spatio-temporal sequence representation.
* Hybrid positional embeddings handle spatial and temporal dimensions, supporting videos with varying resolutions and frame rates.
* Cross-attention layers incorporate text inputs, enabling better control over video generation based on descriptions.
* Adaptive layer normalization with LoRA reduces model size by 36%, maintaining high performance with fewer resources.

![Diffusion model architecture including text input, visual input, and time embeddings into transformer based architecture, resulting in video output.
](https://developer-blogs.nvidia.com/wp-content/uploads/2025/01/nvidia-cosmos-diffusion-model-architecture.png)


*Figure 3. Cosmos diffusion model architecture combines advanced video compression, flexible positional encoding, and text integration to deliver high-quality, physics-aware video generation*

#### Model sizes for varied needs

Developers can choose from the following three model sizes to meet performance, quality, and deployment needs.

* **Nano:** Optimized for real-time, low-latency inference and edge deployment.
* **Super:** Designed as performant baseline models.
* **Ultra:** Focused on maximum quality and fidelity, ideal for distilling custom models.

#### Strengths and limitations

Cosmos world foundation models generate low-resolution, real-world-accurate synthetic video data, essential for training [robotics](https://www.nvidia.com/en-us/solutions/robotics-and-edge-computing/) and autonomous vehicle systems. While they lack artistic flair, their outputs closely replicate the physical world, making them ideal for precise object permanence and realistic scenarios in physical AI model training.

### Guardrails for safe use of Cosmos world foundation models

AI models need guardrails to ensure reliability by mitigating hallucinations, preventing harmful outputs, safeguarding privacy, and aligning with AI standards for safe and controlled deployment. Cosmos ensures the safe use of its world foundation models through a customizable, two-stage guardrail system aligned with NVIDIA’s commitment to trustworthy AI.

Cosmos Guardrails operates in two stages: Pre-guard and Post-guard.

#### **Pre-guard**

This stage involves text prompt-based safety measures using two layers:

* **Keyword Blocking:** A blocklist checker scans prompts for unsafe keywords, using lemmatization to detect variations and blocking non-English terms or spelling errors.
* **Aegis Guardrail:** The NVIDIA fine-tuned Aegis AI Content Safety model detects and blocks semantically unsafe prompts, including categories like violence, harassment, and profanity. Unsafe prompts halt video generation and return an error message.

#### **Post-guard**

The Post-guard stage ensures the safety of generated videos through:

* **Video Content Safety Classifier:** A multiclass classifier evaluates every video frame for safety. If any frame is flagged as unsafe, the entire video is rejected.
* **Face Blur Filter:** All human faces in generated videos are blurred using the RetinaFace model to protect privacy and reduce biases based on age, gender, or race.

NVIDIA experts rigorously test with adversarial examples, annotating over 10,000 prompt-video pairs to refine the system and address edge cases.

### Evaluating Cosmos world foundation models for 3D consistency and physics alignment

Cosmos benchmarks play a crucial role in assessing the ability of world foundation models to simulate real-world physics accurately and efficiently for physical AI applications. While publicly available benchmarks for video generation focus on fidelity, temporal consistency, and speed of generated videos, Cosmos benchmarks add new dimensions to evaluate generalist models: 3D consistency and physics alignment, ensuring the videos are evaluated based on accuracy required for physical AI systems.

#### 3D consistency

Cosmos models were tested for 3D consistency on static scenes from a curated subset of 500 videos from an [open dataset](https://google.github.io/realestate10k/). Text prompts describing the videos were generated to avoid motion-related complexities. Comparisons were made against [VideoLDM](https://arxiv.org/abs/2304.08818), a baseline generative model.

#### Metrics used

* **Geometric Consistency:** Assessed through epipolar geometry constraints using metrics like Sampson error and camera pose estimation success rate.
* **View Synthesis Consistency:** Evaluated through metrics such as Peak Signal-to-Noise Ratio (PSNR), Structural Similarity Index (SSIM), and Learned Perceptual Image Patch Similarity (LPIPS). These metrics measure the quality of synthesized views from interpolated camera positions.

Lower Sampson error and higher success rates indicate better 3D alignment. Similarly, higher PSNR and SSIM and lower LPIPS are indicators of a better quality.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Model** | **Sampson Error ↓** | **Pose Estimation Success Rate (%) ↑** | **PSNR ↑** | **SSIM ↑** | **LPIPS ↓** |
| VideoLDM | 0.841 | 4.40% | 26.23 | 0.783 | 0.135 |
| Cosmos 1.0 Diffusion Text2World 7B | 0.355 | 62.60% | **33.02** | **0.939** | **0.070** |
| Cosmos 1.0 Diffusion Video2World 7B | 0.473 | **68.40%** | 30.66 | 0.929 | 0.085 |
| Cosmos 1.0 Autoregressive 4B | 0.433 | 35.60% | 32.56 | 0.933 | 0.090 |
| Cosmos 1.0 Autoregressive Video2World 5B | 0.392 | 27.00% | 32.18 | 0.931 | 0.090 |
| Real videos (reference) | 0.431 | 56.40% | 35.38 | 0.962 | 0.054 |

*Table 1. Evaluation of 3D consistency for Cosmos world foundation models versus base VideoLDM model*

#### Results

Cosmos world foundation models outperform the baseline in 3D consistency (table 1), with higher geometric alignment and camera pose success rates. Their synthesized views match real-world quality, confirming their effectiveness as world simulators.

#### Physical alignment

Physics alignment tests how well Cosmos models simulate real-world physics, including motion, gravity, and energy dynamics. Using [NVIDIA PhysX](https://github.com/NVIDIA-Omniverse/PhysX) and [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac/sim), eight controlled scenarios were designed to evaluate properties like gravity, collision, torque, and inertia in virtual environments.

#### Metrics used

* **Pixel-Level Metrics:** Peak Signal-to-Noise Ratio (PSNR) measures how closely the pixel values of the model’s output match the reference video. Higher values indicate less noise and better accuracy. Structural Similarity Index Measure (SSIM) assesses the similarity in structure, luminance, and contrast between the generated and ground-truth frames. Higher SSIM values reflect greater visual fidelity.
* **Feature-Level Metric:** DreamSim measures the similarity between high-level features extracted from both videos. This approach evaluates the semantic consistency of the generated content, focusing on objects and motion rather than individual pixels.
* **Object-Level Metric:** Intersection-over-Union (IoU) calculates the overlap between the predicted and actual object regions in the video. This is especially useful for tracking specific objects through the simulation to ensure their behavior aligns with physical expectations.

Higher PSNR, SSIM, DreamSim and IoU are indicators of better physical alignment.

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| **Model** | **Conditioning** | **PSNR ↑** | **SSIM ↑** | **DreamSim ↑** | **Avg. IoU ↑** |
| Cosmos 1.0 Diffusion Video2World 7B | prompt + 1 frame | 17.34 | 0.54 | 0.84 | 0.332 |
| Cosmos 1.0 Diffusion Video2World 7B | prompt + 9 frames | **21.06** | **0.69** | 0.86 | 0.592 |
| Cosmos 1.0 Diffusion Video2World 14B | prompt + 1 frame | 16.81 | 0.52 | 0.84 | 0.338 |
| Cosmos 1.0 Diffusion Video2World 14B | prompt + 9 frames | 20.21 | 0.64 | 0.86 | **0.598** |
| Cosmos 1.0 Autoregressive 4B | 1 frame | 17.91 | 0.49 | 0.83 | 0.394 |
| Cosmos 1.0 Autoregressive 4B | 9 frames | 18.13 | 0.48 | 0.86 | 0.481 |
| Cosmos 1.0 Autoregressive Video2World 5B | prompt + 1 frame | 17.67 | 0.48 | 0.82 | 0.376 |
| Cosmos 1.0 Autoregressive Video2World 5B | prompt + 9 frames | 18.29 | 0.48 | 0.86 | 0.481 |
| Cosmos 1.0 Autoregressive Video2World 12B | 1 frame | 17.94 | 0.49 | 0.83 | 0.395 |
| Cosmos 1.0 Autoregressive Video2World 12B | 9 frames | 18.22 | 0.49 | **0.87** | 0.487 |
| Cosmos 1.0 Autoregressive Video2World 13B | prompt + 1 frame | 18 | 0.49 | 0.83 | 0.397 |
| Cosmos 1.0 Autoregressive Video2World 13B | prompt + 9 frames | 18.26 | 0.48 | 0.87 | 0.482 |

*Table 2. Physics alignment results with metrics calculated over 33 frames, the maximum length supported by the autoregressive variants of the Cosmos world foundation models*

#### Results

Cosmos world foundation models show strong adherence to physical laws (Table 2), particularly with increased conditioning data. Post-training on camera conditioning dataset achieves a twofold increase in pose estimation success rate compared to baseline models. However, challenges like object impermanence (where objects vanish or appear unexpectedly) and implausible behaviors (such as violating gravity) highlight areas for improvement.

### Customizing for physical AI applications with Cosmos and NVIDIA Omniverse

1. **Video search and understanding:** Simplifies video tagging and search by understanding spatial and temporal patterns, making training data preparation easier.
2. **Controllable 3D-to-real synthetic data generation:** With [NVIDIA Omniverse](https://www.nvidia.com/en-us/omniverse/), developers can create 3D scenarios and use Cosmos to generate photorealistic videos that are precisely controlled by 3D scenes for highly tailored synthetic datasets.
3. **Policy model development and evaluation:** World foundation models fine-tuned for action-conditioned video prediction enable scalable, reproducible evaluation of policy models—strategies mapping states to actions—reducing reliance on risky real-world tests or complex simulations for tasks like obstacle navigation or object manipulation.
4. **Foresight for action selection:** Cosmos equips physical AI models with predictive capabilities to assess the outcomes of potential actions.
5. **Multiverse simulation:** Using Cosmos and NVIDIA Omniverse, developers can simulate multiple future outcomes to help AI models evaluate and select the best strategy for achieving its goals, benefiting applications like predictive maintenance and autonomous decision-making.

### From generalist to customized specialist models

Cosmos introduces a two-stage approach to world model training.

**Generalist models:** Cosmos world foundation models are built as generalists, trained on extensive datasets that encompass diverse real-world physics and environments. These open models are capable of handling a broad range of scenarios, from natural dynamics to robotic interactions, providing a solid foundation for any physical AI task.

**Specialist models:** Developers can fine-tune generalist models using smaller, targeted datasets to create specialists tailored for specific applications, such as autonomous driving or humanoid robotics or they can generate customized synthetic scenarios, such as night scenes with emergency vehicles or high-fidelity industrial robotics environments. This fine-tuning process significantly reduces the required data and training time compared to training models from scratch.

Cosmos accelerates training and fine-tuning with efficient video processing pipelines, highly performant tokenizer, and advanced training frameworks, enabling developers to address operational needs and edge cases for advancing physical AI.

#### Accelerated data processing with NVIDIA NeMo Curator

Training models require curated, high-quality data, which is time and resource-intensive. NVIDIA Cosmos includes a data processing and curation pipeline powered by NVIDIA NeMo Curator and optimized for NVIDIA data center GPUs.

NVIDIA NeMo Curator enables robotics and AV developers to process vast datasets efficiently. For example, 20 million hours of video can be processed in 40 days on NVIDIA Hopper GPUs, or just 14 days on NVIDIA Blackwell GPUs—compared to 3.4 years on unoptimized CPU pipelines.

Key benefits include:

* **89x faster curation:** Dramatically reduces processing time
* **Scalability:** Handles 100+ PB of data seamlessly
* **High throughput:** Advanced filtering, captioning, and embedding ensure quality without sacrificing speed

![Graph showing performance compared with ISO power consumption on 2,000 Sapphire Rapids CPUs and 128 DGX nodes​.
](https://developer-blogs.nvidia.com/wp-content/uploads/2025/01/video-data-processing-performance-nvidia-cosmos-with-nemo-curator-625x576.png)


*Figure 4. Cosmos includes NeMo Curator that delivers 89x faster video data processing*

#### High-fidelity compression and reconstruction with Cosmos Tokenizer

After data is curated, it must be tokenized for training. Tokenization breaks down complex data into manageable units, enabling models to process and learn from it more efficiently.

Cosmos tokenizers simplify this process with faster compression and visual reconstruction while preserving quality, reducing costs and complexity. For autoregressive models, the discrete tokenizer compresses data 8x in time and 16×16 in space, processing up to 49 frames at once. For diffusion models, the continuous tokenizer achieves 8x time and 8×8 space compression, handling up to 121 frames.

#### Fine-tuning with NVIDIA NeMo

Developers can fine-tune Cosmos world foundation models using the [NVIDIA NeMo](https://www.nvidia.com/en-us/ai-data-science/products/nemo/) Framework. NeMo Framework accelerates model training on GPU-powered systems, whether enhancing an existing model or building a new one, from on-premises data centers to the cloud.

NeMo Framework efficiently loads multimodal data by:

* Sharding terabyte size dataset into compressed files to reduce IO overhead.
* Deterministically saving and loading datasets to avoid repetition and minimize compute waste.
* Reducing network bandwidth when exchanging data using optimized communications.

## Get started with NVIDIA Cosmos

Cosmos world foundation models are open and available on [NGC](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/cosmos/collections/cosmos) and [Hugging Face](https://huggingface.co/collections/nvidia/cosmos-6751e884dc10e013a0a0d8e6). Developers can also run Cosmos world foundation models on the [NVIDIA API catalog](https://build.nvidia.com/explore/simulation). Also available on the [API catalog](https://build.nvidia.com/nim?filters=usecase%3Ausecase_sdg) are Cosmos tools to enhance text prompts for accuracy, an inbuilt watermarking system that enables easy future identification of AI-generated sequences, and a specialized model to decode video sequences for augmented reality applications. To learn more, [watch the demo](https://www.youtube.com/watch?v=9Uch931cDx8).

[NeMo Curator](https://developer.nvidia.com/nemo-curator#section-demo) for accelerated data processing pipelines is available as a managed service and SDK. Developers can now [apply for early access](https://developer.nvidia.com/nemo-curator-video-processing-early-access). Cosmos tokenizers are open neural networks available on [GitHub](https://github.com/NVIDIA/Cosmos-Tokenizer) and [Hugging Face](https://huggingface.co/collections/nvidia/cosmos-tokenizer-672b93023add81b66a8ff8e6).

[Get started with NVIDIA Cosmos](https://developer.nvidia.com/cosmos).

[Discuss (1)](#entry-content-comments)

+28

Like

## Tags

[Agentic AI / Generative AI](https://developer.nvidia.com/blog/category/generative-ai/) | [Robotics](https://developer.nvidia.com/blog/category/robotics/) | [Simulation / Modeling / Design](https://developer.nvidia.com/blog/category/simulation-modeling-design/) | [General](https://developer.nvidia.com/blog/recent-posts/?industry=General) | [DRIVE](https://developer.nvidia.com/blog/recent-posts/?products=DRIVE) | [Jetson](https://developer.nvidia.com/blog/recent-posts/?products=Jetson) | [NeMo](https://developer.nvidia.com/blog/recent-posts/?products=NeMo) | [NeMo Curator](https://developer.nvidia.com/blog/recent-posts/?products=NeMo+Curator) | [Omniverse](https://developer.nvidia.com/blog/recent-posts/?products=Omniverse) | [Intermediate Technical](https://developer.nvidia.com/blog/recent-posts/?learning_levels=Intermediate+Technical) | [Deep dive](https://developer.nvidia.com/blog/recent-posts/?content_types=Deep+dive) | [Automotive / Transportation](https://developer.nvidia.com/blog/tag/automotive/) | [autonomous vehicles](https://developer.nvidia.com/blog/tag/autonomous-vehicles/) | [featured](https://developer.nvidia.com/blog/tag/featured/) | [Humanoid Robots](https://developer.nvidia.com/blog/tag/humanoid-robots/) | [NVIDIA Research](https://developer.nvidia.com/blog/tag/nvidia-research/) | [Synthetic Data Generation](https://developer.nvidia.com/blog/tag/synthetic-data/) | [Trustworthy AI](https://developer.nvidia.com/blog/tag/trustworthy-ai/)

## About the Authors

![Pranjali Joshi](https://developer-blogs.nvidia.com/wp-content/uploads/2022/10/image3-4-131x131.jpg)

**About Pranjali Joshi**
  
Pranjali Joshi is the product marketing manager for NVIDIA Omniverse, focusing on core technologies and visual generative AI. She holds an M.Sc. degree in data science and marketing strategy from the University of Maryland and a B.Sc. in electronics engineering. Previously, she worked at Accenture and Hitachi Vantara in software development and technology marketing roles.

[View all posts by Pranjali Joshi](https://developer.nvidia.com/blog/author/pranjalij/)

## Comments

## Notable Replies

1. ![Avatar for hameed.ibrahim](https://developer.download.nvidia.com/images/forums/profile-default-devtalk-84.png)
   **[hameed.ibrahim](https://forums.developer.nvidia.com/t/advancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform/318958)**
   says:

   February 5, 2025

   ![Avatar for Discourse user](https://sea2.discourse-cdn.com/nvidia/user_avatar/forums.developer.nvidia.com/jwitsoe/48/16591_2.png) jwitsoe:

   > **Video search and understanding:** Simplifies video tagging and search by understanding spatial and temporal patterns, making training data preparation easier.

   I want to understand more about this. Is there any documentation related to this?

   1. **Video search and understanding:** Simplifies video tagging and search by understanding spatial and temporal patterns, making training data preparation easier.

### Continue the discussion at [forums.developer.nvidia.com](https://forums.developer.nvidia.com/t/advancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform/318958)

#### Participants

![Avatar for jwitsoe](https://sea2.discourse-cdn.com/nvidia/user_avatar/forums.developer.nvidia.com/jwitsoe/64/16591_2.png)
![Avatar for hameed.ibrahim](https://developer.download.nvidia.com/images/forums/profile-default-devtalk-84.png)



## Related posts

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/05/Hammer-Robot.gif)

### Develop Physical AI Reasoning, World, and Action Models with NVIDIA Cosmos 3

[Develop Physical AI Reasoning, World, and Action Models with NVIDIA Cosmos 3](https://developer.nvidia.com/blog/develop-physical-ai-reasoning-world-and-action-models-with-nvidia-cosmos-3/)

![A GIF showing robotics.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/03/Cosmos-Data-Reasoning.gif)

### Scale Synthetic Data and Physical AI Reasoning with NVIDIA Cosmos World Foundation Models

[Scale Synthetic Data and Physical AI Reasoning with NVIDIA Cosmos World Foundation Models](https://developer.nvidia.com/blog/scale-synthetic-data-and-physical-ai-reasoning-with-nvidia-cosmos-world-foundation-models/)

![A decorative image.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/08/R2D2-Workflows.gif)

### R²D²: Boost Robot Training with World Foundation Models and Workflows from NVIDIA Research

[R²D²: Boost Robot Training with World Foundation Models and Workflows from NVIDIA Research](https://developer.nvidia.com/blog/r2d2-boost-robot-training-with-world-foundation-models-and-workflows-from-nvidia-research/)

![](https://developer-blogs.nvidia.com/wp-content/uploads/2025/06/cosmos-robot-arm-composite-gif.gif)

### Develop Custom Physical AI Foundation Models with NVIDIA Cosmos Predict-2

[Develop Custom Physical AI Foundation Models with NVIDIA Cosmos Predict-2](https://developer.nvidia.com/blog/develop-custom-physical-ai-foundation-models-with-nvidia-cosmos-predict-2/)

![Comos Reason GIF.](https://developer-blogs.nvidia.com/wp-content/uploads/2025/05/Cosmos-Reason-robotics.gif)

### Curating Synthetic Datasets to Train Physical AI Models with NVIDIA Cosmos Reason

[Curating Synthetic Datasets to Train Physical AI Models with NVIDIA Cosmos Reason](https://developer.nvidia.com/blog/curating-synthetic-datasets-to-train-physical-ai-models-with-nvidia-cosmos-reason/)

## Related posts

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/06/hc-bonemo-agent-toolkit-1920x1080-1-660x370.jpg)

### Build an AI Scientist for Life Science Discovery with NVIDIA BioNeMo Agent Toolkit

[Build an AI Scientist for Life Science Discovery with NVIDIA BioNeMo Agent Toolkit](https://developer.nvidia.com/blog/build-an-ai-scientist-for-life-science-discovery-with-nvidia-bionemo-agent-toolkit/)

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/06/ai-game-character.gif)

### Build On-Device AI Companions with the NVIDIA ACE Game Agent SDK and Unreal Engine 5 Plugins

[Build On-Device AI Companions with the NVIDIA ACE Game Agent SDK and Unreal Engine 5 Plugins](https://developer.nvidia.com/blog/build-on-device-ai-companions-with-the-nvidia-ace-game-agent-sdk-and-unreal-engine-5-plugins/)

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/05/auto-nvidia-alpamayo-1-1.gif)

### How to Post-Train Autonomous Vehicle Models in Closed-Loop with NVIDIA Alpamayo

[How to Post-Train Autonomous Vehicle Models in Closed-Loop with NVIDIA Alpamayo](https://developer.nvidia.com/blog/how-to-post-train-autonomous-vehicle-models-in-closed-loop-with-nvidia-alpamayo/)

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/05/Hammer-Robot.gif)

### Develop Physical AI Reasoning, World, and Action Models with NVIDIA Cosmos 3

[Develop Physical AI Reasoning, World, and Action Models with NVIDIA Cosmos 3](https://developer.nvidia.com/blog/develop-physical-ai-reasoning-world-and-action-models-with-nvidia-cosmos-3/)

![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/03/inference-press-dynamo-gtc26-4960950-1920x1080-1-660x370.png)

### DynoSim: Simulating the Pareto Frontier

[DynoSim: Simulating the Pareto Frontier](https://developer.nvidia.com/blog/dynosim-simulating-the-pareto-frontier/)

* [![](https://developer-blogs.nvidia.com/wp-content/uploads/2026/06/Copy-of-siggraph26-email-footer-1360x180-1.webp "NVIDIA at SIGGRAPH 2026")](https://www.nvidia.com/en-us/events/siggraph)

Sign up for NVIDIA News

[Subscribe](https://developer.nvidia.com/email-signup)

Follow NVIDIA Developer

Find more news and tutorials on [NVIDIA Technical Blog](https://developer.nvidia.com/blog)

* [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/)
* [Your Privacy Choices](https://www.nvidia.com/en-us/about-nvidia/privacy-center/)
* [Terms of Use](https://developer.nvidia.com/legal/terms)
* [Accessibility](https://www.nvidia.com/en-us/about-nvidia/accessibility/)
* [Corporate Policies](https://www.nvidia.com/en-us/about-nvidia/company-policies/)
* [Contact](https://developer.nvidia.com/contact)

Copyright © 2026 NVIDIA Corporation





Close


Previous
Next

* [L](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)
* [T](https://twitter.com/intent/tweet?text=Advancing+Physical+AI+with+NVIDIA+Cosmos+World+Foundation+Model+Platform+%7C+NVIDIA+Technical+Blog+https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)
* [F](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)
* [R](https://www.reddit.com/submit?url=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F&title=Advancing+Physical+AI+with+NVIDIA+Cosmos+World+Foundation+Model+Platform+%7C+NVIDIA+Technical+Blog)
* [E](mailto:?subject=I'd like to share a link with you&body=https%3A%2F%2Fdeveloper.nvidia.com%2Fblog%2Fadvancing-physical-ai-with-nvidia-cosmos-world-foundation-model-platform%2F)

* [Join](https://developer.nvidia.com/login)

* [Home](/ "Home")
* [Blog](/blog "Blog")
* [Forums](https://forums.developer.nvidia.com/ "Forums")
* [Docs](https://docs.nvidia.com/ "Docs")
* [Downloads](https://developer.nvidia.com/downloads "Downloads")
* [Training](https://www.nvidia.com/en-us/training/ "Training")

NVIDIA uses cookies to improve your experience on our web site. We and our third-party partners also use cookies and other tools to collect and record information you provide as well as information about your interactions with our websites for performance improvement, analytics, and to assist in marketing efforts. By clicking "Accept All", you consent to our use of cookies and other tools as described in our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/). You can manage your cookie settings by clicking on "Manage Settings." By continuing to use this site or by clicking one of the buttons below, you agree to our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information on our privacy practices.

We have detected the Global Privacy Control (GPC) signal and recorded your rejection of all optional cookies on this site for this browser. You can manage your cookie settings by clicking on "Manage Settings". Please see our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information. To opt out of non-cookie personal information "sales" / "sharing" for targeted advertising purposes, please visit the [NVIDIA Preference Center](https://www.nvidia.com/en-us/about-nvidia/privacy-center/). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information on our privacy practices.

We have detected the Global Privacy Control Signal (GPC) and have opted you out of all optional cookies on this browser. You can manage your cookie settings by clicking on "Manage Settings". Please see our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information. We have also opted you out of "sharing"/"sales" of personal information outside of cookies. You can manage these settings in the NVIDIA [NVIDIA Preference Center](https://www.nvidia.com/en-us/privacy-center/). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

We have detected the Global Privacy Control Signal (GPC) and have opted you out of all optional cookies on this browser. You can manage your cookie settings by clicking on "Manage Settings". Please see our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) for more information. We have also opted you out of "sharing"/"sales" of personal information outside of cookies which overrides at least one of your previous settings. You can manage them in the [NVIDIA Preference Center](https://www.nvidia.com/en-us/privacy-center/). Please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/) for more information.

Manage Settings

Reject Optional Accept All

![NVIDIA Logo](https://cdn.cookielaw.org/logos/10ddf4ca-c072-45d0-b3ac-eead0ed93db0/6e17f6e4-c77b-4a11-9f34-c107c42e4bfc/7981.png)

Cookie Settings

We and our third-party partners (including social media, advertising, and analytics partners) use cookies and other tracking technologies to collect, store, monitor, and process certain information about you when you visit our website. The information collected might relate to you, your preferences, or your device. We use that information to make the site work, analyze performance and traffic on our website, provide a more personalized web experience, and assist in our marketing efforts.  
  
Under certain privacy laws, you have the right to direct us not to "sell" or "share" your personal information for targeted advertising. To opt-out of the "sale" and "sharing" of personal information through cookies, you must opt-out of optional cookies using the toggles below. To opt out of the "sale" and "sharing" of data collected by other means (e.g., online forms) you must also update your data sharing preferences through the [NVIDIA Preference Center](https://www.nvidia.com/en-us/about-nvidia/privacy-center/).  
  
Click on the different category headings below to find out more and change the settings according to your preference. You cannot opt out of Required Cookies as they are deployed to ensure the proper functioning of our website (such as prompting the cookie banner and remembering your settings, etc.). By clicking "Save and Accept" or "Decline All" at the bottom, you consent to the use of cookies and other tools as described in our [Cookie Policy](https://www.nvidia.com/en-us/about-nvidia/cookie-policy/) in accordance with your settings and accept our [Terms of Service](https://www.nvidia.com/en-us/about-nvidia/terms-of-service/) (which contains important waivers). For more information about our privacy practices, please see our [Privacy Policy](https://www.nvidia.com/en-us/about-nvidia/privacy-policy/).

Required Cookies

Always Active

These cookies enable core functionality such as security, network management, and accessibility. These cookies are required for the site to function and cannot be turned off.

Cookies Details

Performance Cookies

Performance Cookies

These cookies are used to provide quantitative measures of our website visitors, such as the number of times you visit, time on page, your mouse movements, scrolling, clicks and keystroke activity on the websites; other browsing, search, or product research behavior; and what brought you to our site. These cookies may store a unique ID so that our system will remember you when you return. Information collected with these cookies is used to measure and find ways to improve website performance.

Cookies Details

Personalization Cookies

Personalization Cookies

These cookies collect data about how you have interacted with our website to help us improve your web experience, such as which pages you have visited. These cookies may store a unique ID so that our system will remember you when you return. They may be set by us or by third party providers whose services we have added to our pages. These cookies enable us to provide enhanced website functionality and personalization as well as make the marketing messages we send to you more relevant to your interests. If you do not allow these cookies, then some or all of these services may not function properly.

Cookies Details

Advertising Cookies

Advertising Cookies

These cookies record your visit to our websites, the pages you have visited and the links you have followed to influence the advertisements that you see on other websites. These cookies and the information they collect may be managed by other companies, including our advertising partners, and may be used to build a profile of your interests and show you relevant advertising on other sites. We and our advertising partners will use this information to make our websites and the advertising displayed on it, more relevant to your interests.

Cookies Details

Cookie List

Clear

* checkbox label label

Apply Cancel

Consent Leg.Interest

checkbox label label

checkbox label label

checkbox label label

Decline All Save and Accept

[![Powered by Onetrust](https://cdn.cookielaw.org/logos/static/powered_by_logo.svg "Powered by OneTrust Opens in a new Tab")](https://www.onetrust.com/solutions/consent-and-preferences/?utm_source=cmp&utm_medium=cmpbanner)
