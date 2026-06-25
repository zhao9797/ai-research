<!-- source: https://blog.reve.com/posts/the-layout-bet/ -->
<!-- fetched: 2026-06-25 via curl direct -->

The Layout Bet - Reve Blog 

## 

## 

 Pricing 
 API 
 Blog 
 Start Creating 

## The Layout Bet

 June 3, 2026

 Modern image models use text as their internal representation: a Large Language Model (LLM) expands the user prompt into a long-form description, which a diffusion model then renders as pixels. Text is expressive, but it is fundamentally ambiguous — and ambiguity is the enemy of control. Tweak a prompt, and the whole image changes. Ask for a specific color or object position in plain text, and you are out of luck.

 We made a different bet. We replaced English prose and built a better intermediate representation: a layout. 

 Layout is a structured, hierarchical description of an image where every element has a location, a size, a local description, and other optional attributes like image references or color. A layout is an image’s backbone — separating semantic intent from pixel rendering, much like HTML is to a webpage or SVG to a vector image. Because layout is a structured, readable format, it becomes a shared interface between humans and AI agents — opening up a new world of precise, nonverbal visual control. Users can refine the results by writing natural language instructions or by directly editing the layout structure.

 Regions 

 Working with layouts requires a new genre of model, so we built our own unified Large Layout Model for agentic visual understanding and generation. Our model takes any combination of layouts, instructions, and images as input, derives a layout from its internal thinking trace, and then renders the final pixels.

 Your browser does not support the video tag.

 We built a novel data pipeline on billions of images, bootstrapped from dense human annotations. Then we did continued pretraining and post-training of open-source large language models (thank you, Qwen team!) to learn spatial reasoning capabilities around our layout representation.

## Our bet paid off!

 Reve 2.0 is the best image generation model made by a sub-$1T company, trained on 10x fewer GPUs.

 Model benchmark scores by category. 

 Arena text-to-image leaderboard as of June 3, 2026. 

 To validate our approach, we ran a large-scale ablation and found that layout models consistently outperform equal-size prompt-based generators, producing significantly better images across the board.

## Reconstruction quality

 Plain text prompts alone cannot faithfully reconstruct an image — no matter how detailed the description, the result will always diverge from the original. Layouts tell a different story: as the number of regions increases, the model continually improves, reconstructing finer and finer details — and all of this without a single pixel as input. This high reconstruction quality carries over to editing as well: when pixels are provided, layouts become even more powerful, enabling precise, targeted edits by defining exactly what goes where.

 CLIP similarity by region count: 0=0.865, 10=0.905, 20=0.913, 30=0.923, 40=0.927, 50=0.929 

 Original

 19 Regions + Style

 0 
 4 
 12 
 19 

 Original

 42 Regions + Style

 0 
 12 
 20 
 42 

## Generation quality

 We also found that scaling laws apply to layout models. Not only does quality improve significantly as model size increases, but layout models produce higher quality images when we increase the number of regions they output, essentially increasing their visual thinking context.

 Text Only

 All Regions

 Hover a region

 Text Only 

 Regions Applied 

## Looking ahead

 Layout is only the first step in our journey to treat image generation as program synthesis, so that humans and agents can read, write, and reason over a shared, code-like semantic intermediary.

 The foundation is solid. Now, it is time to scale L L Ms!

 Reve Research Team

## BibTeX

 @misc{reve2026layoutbet,
 title = {The Layout Bet},
 author = {{Reve Team}},
 organization = {Reve},
 year = {2026},
 month = {June},
 url = {https://reve.com},
 note = {Accessed: 2026-06-03}
} 

 Pricing 

 API 

 Blog 

 - About 

 - Creative Partners 

 - FAQ 

 - Support 

 - Privacy 

 - Terms 

 © 2025-2026 Reve AI, Inc

 - 

 - 

 - 

 - 

 - 

 -
