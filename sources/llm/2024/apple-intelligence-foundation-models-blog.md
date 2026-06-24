# Introducing Apple’s On-Device and Server Foundation Models - Apple Machine Learning Research
Source: https://machinelearning.apple.com/research/introducing-apple-foundation-models
Introducing Apple’s On-Device and Server Foundation Models - Apple Machine Learning Research

[Machine Learning Research](/)

[Open Menu](#localnav-menustate)[Close Menu](#)

* [Overview](/)
* [Research Highlights](/highlights)
* [Publications](/research/)
* [Events](/updates/)
* [Work with us](/work-with-us)

content type Featured highlight

# Introducing Apple’s On-Device and Server Foundation Models

[](https://mlr.cdn-apple.com/video/hero_fm_1680_e4e238ab3d.mp4)

June 10, 2024

At the 2024 [Worldwide Developers Conference](https://developer.apple.com/wwdc24/), we introduced Apple Intelligence, a personal intelligence system integrated deeply into iOS 18, iPadOS 18, and macOS Sequoia.

Apple Intelligence is comprised of multiple highly-capable generative models that are specialized for our users’ everyday tasks, and can adapt on the fly for their current activity. The foundation models built into Apple Intelligence have been fine-tuned for user experiences such as writing and refining text, prioritizing and summarizing notifications, creating playful images for conversations with family and friends, and taking in-app actions to simplify interactions across apps.

In the following overview, we will detail how two of these models — a ~3 billion parameter on-device language model, and a larger server-based language model available with [Private Cloud Compute](https://security.apple.com/blog/private-cloud-compute/) and running on Apple silicon servers — have been built and adapted to perform specialized tasks efficiently, accurately, and responsibly. These two foundation models are part of a larger family of generative models created by Apple to support users and developers; this includes a coding model to build intelligence into Xcode, as well as a diffusion model to help users express themselves visually, for example, in the Messages app. We look forward to sharing more information soon on this broader set of models.

**Update** *- July 29, 2024: The figures in this article have been updated to reflect the model versions and evaluations used in the technical report released today. For more detail, please see the paper: [Apple Intelligence Foundation Language Models](/research/apple-intelligence-foundation-language-models).*

## [Our Focus on Responsible AI Development](#our-focus-on-responsible-ai-development)

Apple Intelligence is designed with our core values at every step and built on a foundation of groundbreaking privacy innovations.

Additionally, we have created a set of Responsible AI principles to guide how we develop AI tools, as well as the models that underpin them:

1. Empower users with intelligent tools: We identify areas where AI can be used responsibly to create tools for addressing specific user needs. We respect how our users choose to use these tools to accomplish their goals.
2. Represent our users: We build deeply personal products with the goal of representing users around the globe authentically. We work continuously to avoid perpetuating stereotypes and systemic biases across our AI tools and models.
3. Design with care: We take precautions at every stage of our process, including design, model training, feature development, and quality evaluation to identify how our AI tools may be misused or lead to potential harm. We will continuously and proactively improve our AI tools with the help of user feedback.
4. Protect privacy: We protect our users’ privacy with powerful on-device processing and groundbreaking infrastructure like Private Cloud Compute. We do not use our users’ private personal data or user interactions when training our foundation models.

These principles are reflected throughout the architecture that enables Apple Intelligence, connects features and tools with specialized models, and scans inputs and outputs to provide each feature with the information needed to function responsibly.

In the remainder of this overview, we provide details on decisions such as: how we develop models that are highly capable, fast, and power-efficient; how we approach training these models; how our adapters are fine-tuned for specific user needs; and how we evaluate model performance for both helpfulness and unintended harm.

[![Modeling overview](https://mlr.cdn-apple.com/media/Fig1_Responsible_AI_8bf7727ab5.png)](https://mlr.cdn-apple.com/media/Fig1_Responsible_AI_8bf7727ab5.png)

Figure 1: Modeling overview for the Apple foundation models.

## [Pre-Training](#pre-training)

Our foundation models are trained on [Apple’s AXLearn framework](https://github.com/apple/axlearn), an open-source project we released in 2023. It builds on top of JAX and XLA, and allows us to train the models with high efficiency and scalability on various training hardware and cloud platforms, including TPUs and both cloud and on-premise GPUs. We used a combination of data parallelism, tensor parallelism, sequence parallelism, and Fully Sharded Data Parallel (FSDP) to scale training along multiple dimensions such as data, model, and sequence length.

We train our foundation models on licensed data, including data selected to enhance specific features, as well as publicly available data collected by our web-crawler, AppleBot. Web publishers have [the option to opt out](https://support.apple.com/en-us/119829) of the use of their web content for Apple Intelligence training with a data usage control.

We never use our users’ private personal data or user interactions when training our foundation models, and we apply filters to remove personally identifiable information like social security and credit card numbers that are publicly available on the Internet. We also filter profanity and other low-quality content to prevent its inclusion in the training corpus. In addition to filtering, we perform data extraction, deduplication, and the application of a model-based classifier to identify high quality documents.

## [Post-Training](#post-training)

We find that data quality is essential to model success, so we utilize a hybrid data strategy in our training pipeline, incorporating both human-annotated and synthetic data, and conduct thorough data curation and filtering procedures. We have developed two novel algorithms in post-training: (1) a rejection sampling fine-tuning algorithm with teacher committee, and (2) a reinforcement learning from human feedback (RLHF) algorithm with mirror descent policy optimization and a leave-one-out advantage estimator. We find that these two algorithms lead to significant improvement in the model’s instruction-following quality.

## [Optimization](#optimization)

In addition to ensuring our generative models are highly capable, we have used a range of innovative techniques to optimize them on-device and on our private cloud for speed and efficiency. We have applied an extensive set of optimizations for both first token and extended token inference performance.

Both the on-device and server models use grouped-query-attention. We use shared input and output vocab embedding tables to reduce memory requirements and inference cost. These shared embedding tensors are mapped without duplications. The on-device model uses a vocab size of 49K, while the server model uses a vocab size of 100K, which includes additional language and technical tokens.

For on-device inference, we use low-bit palletization, a critical optimization technique that achieves the necessary memory, power, and performance requirements. To maintain model quality, we developed a new framework using LoRA adapters that incorporates a mixed 2-bit and 4-bit configuration strategy — averaging 3.7 bits-per-weight — to achieve the same accuracy as the uncompressed models. More aggressively, the model can be compressed to 3.5 bits-per-weight without significant quality loss.

Additionally, we use an interactive model latency and power analysis tool, [Talaria](/research/talaria), to better guide the bit rate selection for each operation. We also utilize activation quantization and embedding quantization, and have developed an approach to enable efficient Key-Value (KV) cache update on our neural engines.

With this set of optimizations, on iPhone 15 Pro we are able to reach time-to-first-token latency of about 0.6 millisecond per prompt token, and a generation rate of 30 tokens per second. Notably, this performance is attained before employing token speculation techniques, from which we see further enhancement on the token generation rate.

## [Model Adaptation](#model-adaptation)

Our foundation models are fine-tuned for users’ everyday activities, and can dynamically specialize themselves on-the-fly for the task at hand. We utilize adapters, small neural network modules that can be plugged into various layers of the pre-trained model, to fine-tune our models for specific tasks. For our models we adapt the attention matrices, the attention projection matrix, and the fully connected layers in the point-wise feedforward networks for a suitable set of the decoding layers of the transformer architecture.

By fine-tuning only the adapter layers, the original parameters of the base pre-trained model remain unchanged, preserving the general knowledge of the model while tailoring the adapter layers to support specific tasks.

[](https://mlr.cdn-apple.com/video/Fig2_Adapters_9f087bc5c5.mp4)

Figure 2: Adapters are small collections of model weights that are overlaid onto the common base foundation model. They can be dynamically loaded and swapped — giving the foundation model the ability to specialize itself on-the-fly for the task at hand. Apple Intelligence includes a broad set of adapters, each fine-tuned for a specific feature. It’s an efficient way to scale the capabilities of our foundation model.

We represent the values of the adapter parameters using 16 bits, and for the ~3 billion parameter on-device model, the parameters for a rank 16 adapter typically require 10s of megabytes. The adapter models can be dynamically loaded, temporarily cached in memory, and swapped — giving our foundation model the ability to specialize itself on the fly for the task at hand while efficiently managing memory and guaranteeing the operating system’s responsiveness.

To facilitate the training of the adapters, we created an efficient infrastructure that allows us to rapidly retrain, test, and deploy adapters when either the base model or the training data gets updated. The adapter parameters are initialized using the accuracy-recovery adapter introduced in the Optimization section.

## [Performance and Evaluation](#performance-and-evaluation)

Our focus is on delivering generative models that can enable users to communicate, work, express themselves, and get things done across their Apple products. When benchmarking our models, we focus on human evaluation as we find that these results are highly correlated to user experience in our products. We conducted performance evaluations on both feature-specific adapters and the foundation models.

To illustrate our approach, we look at how we evaluated our adapter for summarization. As product requirements for summaries of emails, messages, and notifications differ in subtle but important ways, we fine-tune accuracy-recovery low-rank (LoRA) adapters on top of the palletized model to meet these specific requirements. Our training data is based on synthetic summaries generated from bigger server models, filtered by a rejection sampling strategy that keeps only the high quality summaries.

To evaluate the product-specific summarization, we use a set of 750 responses carefully sampled for each use case. These evaluation datasets emphasize a diverse set of inputs that our product features are likely to face in production, and include a stratified mixture of single and stacked documents of varying content types and lengths. As product features, it was important to evaluate performance against datasets that are representative of real use cases. We find that overall, our models with adapters generate better summaries than a comparable model.

As part of responsible development, we identified and evaluated specific risks inherent to summarization. For example, summaries occasionally remove important nuance or other details in ways that are undesirable. However, we found that the summarization adapter did not amplify sensitive content in over 99% of targeted adversarial examples. We continue to adversarially probe to identify unknown harms and expand our evaluations to help guide further improvements.

### Human Satisfaction with Summarization Feature

#### Good Result Ratio

##### Email

1. Llama-3-8B: 36.1%
2. Phi-3-mini: 44.7%
3. Gemma-7B: 70.9%
4. Apple On-Device + Adapter: 71.3%

##### Message

1. Llama-3-8B: 21.3%
2. Phi-3-mini: 32.8%
3. Gemma-7B: 51.1%
4. Apple On-Device + Adapter: 63.0%

##### Notification

1. Llama-3-8B: 27.7%
2. Phi-3-mini: 56.6%
3. Gemma-7B: 60.9%
4. Apple On-Device + Adapter: 74.9%

#### Poor Result Ratio

##### Email

1. Llama-3-8B: 12.8%
2. Phi-3-mini: 12.0%
3. Gemma-7B: 4.5%
4. Apple On-Device + Adapter: 7.2%

##### Message

1. Llama-3-8B: 35.3%
2. Phi-3-mini: 31.4%
3. Gemma-7B: 18.3%
4. Apple On-Device + Adapter: 15.9%

##### Notification

1. Llama-3-8B: 48.3%
2. Phi-3-mini: 18.3%
3. Gemma-7B: 12.9%
4. Apple On-Device + Adapter: 10.0%

Figure 3: Ratio of "good" and "poor" responses for three summarization use cases relative to all responses. Summaries are classified as "good", "neutral", "poor" given the grader's scores across five dimensions. A result is classified as "good" if all of the dimensions are good (higher is better). A result is classified as "poor" if any of the dimensions are poor (lower is better). Our models with adapters overall generate better summaries than comparable models.

In addition to evaluating feature specific performance powered by foundation models and adapters, we evaluate both the on-device and server-based models’ general capabilities. We utilize a comprehensive evaluation set of real-world prompts to test the general model capabilities. These prompts are diverse across different difficulty levels and cover major categories such as brainstorming, classification, closed question answering, coding, extraction, mathematical reasoning, open question answering, rewriting, safety, summarization, and writing.

We compare our models with both open-source models (Phi-3, Gemma, Mistral, DBRX, Llama) and commercial models of comparable size (GPT-3.5, GPT-4)[1](#footnotes). We find that our models are preferred by human graders over most comparable competitor models. On this benchmark, our on-device model, with ~3B parameters, outperforms larger models including Phi-3-mini, Mistral-7B, Gemma-7B, and Llama-3-8B. Our server model compares favorably to DBRX-Instruct, Mixtral-8x22B, GPT-3.5, and Llama-3-70B while being highly efficient.

### Human Evaluation

Win

Tie

Lose

#### Apple On-Device versus

1. Apple On-Device versus Llama-3-8B: win 29.7%, tie 32.0%, lose 38.3%.
2. Apple On-Device versus Gemma-7B: win 43.7%, tie 26.8%, lose 29.5%.
3. Apple On-Device versus Phi-3-mini: win 47.7%, tie 24.2%, lose 28.1%.
4. Apple On-Device versus Mistral-7B: win 50.7%, tie 24.7%, lose 24.6%.
5. Apple On-Device versus Gemma-2B: win 63.8%, tie 21.0%, lose 15.2%.

#### Apple Server versus

1. Apple Server versus GPT-4: win 29.3%, tie 31.9%, lose 38.8%.
2. Apple Server versus Llama-3-70B: win 31.7%, tie 33.0%, lose 35.3%.
3. Apple Server versus Mixtral-8x22B: win 44.9%, tie 29.3%, lose 25.8%.
4. Apple Server versus GPT-3.5: win 51.5%, tie 27.4%, lose 21.1%.
5. Apple Server versus DBRX-Instruct: win 56.4%, tie 24.6%, lose 19.0%.

Figure 4: Fraction of preferred responses in side-by-side evaluation of Apple's foundation model against comparable models. We find that our models are preferred by human graders.

We use a set of diverse adversarial prompts to test the model performance on harmful content, sensitive topics, and factuality. We measure the violation rates of each model as evaluated by human graders on this evaluation set, with a lower number being desirable. Both the on-device and server models are robust when faced with adversarial prompts, achieving violation rates lower than open-source and commercial models.

### Human Evaluation of Output Harmfulness

#### On-Device

1. Mistral-7B: 51.3%
2. Phi-3-mini: 24.4%
3. Llama-3-8B: 21.8%
4. Gemma-2B: 13.9%
5. Gemma-7B: 13.6%
6. Apple On-Device: 7.5%

#### Server

1. Mixtral-8x22B: 47.5%
2. DBRX-Instruct: 43.7%
3. GPT-4: 28.8%
4. Llama-3-70B: 27.9%
5. GPT-3.5: 22.6%
6. Apple Server: 6.3%

Figure 5: Fraction of violating responses for harmful content, sensitive topics, and factuality (lower is better). Our models are robust when faced with adversarial prompts.

Our models are preferred by human graders as safe and helpful over competitor models for these prompts. However, considering the broad capabilities of large language models, we understand the limitation of our safety benchmark. We are actively conducting both manual and automatic red-teaming with internal and external teams to continue evaluating our models’ safety.

### Human Preference Evaluation on Safety Prompts

Win

Tie

Lose

#### Apple On-Device versus

1. Apple On-Device versus Gemma-7B: win 42.9%, tie 41.5%, lose 15.6%.
2. Apple On-Device versus Gemma-2B: win 54.0%, tie 33.3%, lose 12.7%.
3. Apple On-Device versus Llama-3-8B: win 60.4%, tie 30.0%, lose 9.6%.
4. Apple On-Device versus Phi-3-mini: win 61.2%, tie 29.0%, lose 9.8%.
5. Apple On-Device versus Mistral-7B: win 70.6%, tie 23.2%, lose 6.2%.

#### Apple Server versus

1. Apple Server versus GPT-3.5: win 59.4%, tie 29.2%, lose 11.4%.
2. Apple Server versus GPT-4: win 62.2%, tie 28.7%, lose 9.1%.
3. Apple Server versus Llama-3-70B: win 64.4%, tie 28.6%, lose 7.0%.
4. Apple Server versus DBRX-Instruct: win 66.8%, tie 24.5%, lose 8.7%.
5. Apple Server versus Mixtral-8x22B: win 67.0%, tie 25.1%, lose 7.9%.

Figure 6: Fraction of preferred responses in side-by-side evaluation of Apple's foundation model against comparable models on safety prompts. Human graders found our responses safer and more helpful.

To further evaluate our models, we use the Instruction-Following Eval (IFEval) benchmark to compare their instruction-following capabilities with models of comparable size. The results suggest that both our on-device and server model follow detailed instructions better than the open-source and commercial models of comparable size.

### IFEval Benchmarks

#### On-Device

##### Instruction-level Accuracy

1. Gemma-2B: 40.5%
2. Gemma-7B: 61.6%
3. Mistral-7B: 65.2%
4. Phi-3-mini: 67.9%
5. Llama-3-8B: 82.5%
6. Apple On-Device: 85.7%

##### Prompt-level Accuracy

1. Gemma-2B: 28.7%
2. Gemma-7B: 51.4%
3. Mistral-7B: 54.2%
4. Phi-3-mini: 57.8%
5. Llama-3-8B: 74.7%
6. Apple On-Device: 79.3%

#### Server

##### Instruction-level Accuracy

1. DBRX-Instruct: 65.8%
2. GPT-3.5: 74.8%
3. Mixtral-8x22B: 79.4%
4. GPT-4: 85.4%
5. Llama-3-70B: 88.1%
6. Apple Server: 88.5%

##### Prompt-level Accuracy

1. DBRX-Instruct: 53.6%
2. GPT-3.5: 65.3%
3. Mixtral-8x22B: 71.4%
4. GPT-4: 79.3%
5. Llama-3-70B: 82.3%
6. Apple Server: 83.0%

Figure 7: Instruction-following capability (measured with IFEval) for Apple's foundation models and models of comparable size (higher is better).

We evaluate our models’ writing ability on our internal summarization and composition benchmarks, consisting of a variety of writing instructions. These results do not refer to our feature-specific adapter for summarization (seen in [Figure 3](#figure3)), nor do we have an adapter focused on composition.

### Writing Benchmarks

#### On-Device

##### Summarization

1. Gemma-2B: 7.6
2. Phi-3-mini: 8.8
3. Gemma-7B: 8.9
4. Mistral-7B: 8.9
5. Apple On-Device: 9.1

##### Composition

1. Gemma-2B: 8.0
2. Phi-3-mini: 9.0
3. Apple On-Device: 9.0
4. Gemma-7B: 9.1
5. Mistral-7B: 9.1

#### Server

##### Summarization

1. GPT-3.5: 8.6
2. DBRX-Instruct: 9.2
3. Mixtral-8x22B: 9.5
4. GPT-4: 9.5
5. Apple Server: 9.5

##### Composition

1. GPT-3.5: 8.9
2. DBRX-Instruct: 9.2
3. Mixtral-8x22B: 9.5
4. Apple Server: 9.6
5. GPT-4: 9.7

Figure 8: Writing ability on internal summarization and composition benchmarks (higher is better).

## [Conclusion](#conclusion)

The Apple foundation models and adapters introduced at WWDC24 underlie Apple Intelligence, the new personal intelligence system that is integrated deeply into iPhone, iPad, and Mac, and enables powerful capabilities across language, images, actions, and personal context. Our models have been created with the purpose of helping users do everyday activities across their Apple products, and developed responsibly at every stage and guided by Apple’s core values. We look forward to sharing more information soon on our broader family of generative models, including language, diffusion, and coding models.

## Footnotes

[1] We compared against the following model versions: gpt-3.5-turbo-0125, gpt-4-0125-preview, Phi-3-mini-4k-instruct, Mistral-7B-Instruct-v0.2, Mixtral-8x22B-Instruct-v0.1, Gemma-1.1-2B, Gemma-1.1-7B, Llama-3-8B-Instruct, and Llama-3-70B-Instruct. The open-source and Apple models are evaluated in bfloat16 precision.

## Related readings and updates.

[### Apple Intelligence Foundation Language Models Tech Report 2025](/research/apple-foundation-models-tech-report-2025)

July 17, 2025[research area Speech and Natural Language Processing](/research/?domain=Speech%20and%20Natural%20Language%20Processing)

We introduce two multilingual, multimodal foundation language models that power Apple Intelligence features across Apple devices and services: (i) a ∼3B-parameter on-device model optimized for Apple silicon through architectural innovations such as KV-cache sharing and 2-bit quantization-aware training; and (ii) a scalable server model built on a novel Parallel-Track Mixture-of-Experts (PT-MoE) transformer that combines track parallelism,…

[Read more](/research/apple-foundation-models-tech-report-2025)

[### Updates to Apple’s On-Device and Server Foundation Language Models](/research/apple-foundation-models-2025-updates)

June 9, 2025

With Apple Intelligence, we’re integrating powerful generative AI right into the apps and experiences people use every day, all while protecting their privacy. At the 2025 Worldwide Developers Conference we introduced a new generation of language foundation models specifically developed to enhance the Apple Intelligence features in our latest software releases. We also introduced the new Foundation Models framework, which gives app developers…

[Read more](/research/apple-foundation-models-2025-updates)

![Bottom banner](https://mlr.cdn-apple.com/media/Discover_1440x420_2x_9c465d585e.jpg)

## Discover opportunities in Machine Learning.

Our research in machine learning breaks new ground every day.

[Work with us](/work-with-us)

1. [Machine Learning Research](/)
2. [Publications](/research)
3. Introducing Apple’s On-Device and Server Foundation Models

* [Privacy Policy](https://www.apple.com/legal/privacy/)
* [Terms of Use](https://www.apple.com/legal/internet-services/terms/site.html)
* [Legal](https://www.apple.com/legal/)

Copyright © 2026 [Apple Inc.](https://www.apple.com) All rights reserved.

  
