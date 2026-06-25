 Ideogram 4.0 Technical Details: Open model at the forefront of design Models Ideogram 4.0 
 Ideogram 3.0 
 Custom Image Models 
 Features Background Remover 
 Print on Demand 
 Editable text layers 
 Character consistency 
 Styles 
 Open source Licensing 
 GitHub 
 Hugging Face 
 API Learn 
 Documentation 
 Dashboard 
 API pricing 
 MCP App Pricing 
 Enterprise Login Sign up 
Models
 Ideogram 4.0 Ideogram 3.0 Custom Image Models 
Features
 Background Remover Print on Demand Editable text layers Character consistency Styles 
Open source
 Licensing GitHub Hugging Face 
API
 Learn Documentation Dashboard API pricing 
 MCP 
App
 Pricing 
 Enterprise Login Sign up 
 Home / Blog / Ideogram 4.0 Technical Details: Open model at the forefront of design 
 Technical Model release June 3, 2026 
 Ideogram 4.0 Technical Details: Open model at the forefront of design
 Our first open-weight foundation model. A 9.3B single-stream Diffusion Transformer, trained from scratch, with a vision-language text encoder and structured JSON prompts.
 Authors. Ideogram Team Reading time. 5 min Weights. Hugging Face Code. GitHub 
 Overview
Ideogram 4.0 is a 9.3B parameter open-weight text-to-image model. Recent open-weight
 releases have converged on a single self-attention sequence over text and image tokens [1] [2] [3] , and Ideogram
 4.0 follows the same pattern: text and image tokens share the same projections at every
 layer of a 34-layer DiT. Two design choices distinguish it from peer releases. First, the
 text encoder is Qwen3-VL-8B-Instruct, a vision-language model, and the DiT consumes hidden
 states from 13 of its intermediate layers concatenated along the feature dimension,
 instead of a single hidden state [4] [5] or no external encoder at all [1] [3] . Second, the model is trained exclusively on structured JSON captions with per-element
 styling and optional bounding boxes and color palettes, and the reference inference
 pipeline parses every prompt as JSON and validates it against the schema before
 generation.
 Architecture at a glance
The pipeline has four components: a frozen vision-language text encoder, the trainable
 single-stream Diffusion Transformer [6] , a flow-matching
 Euler sampler with asymmetric classifier-free guidance, and a frozen KL autoencoder [7] that decodes latents to pixels.
 PROMPT IN IMAGE OUT 01 · ENCODER Qwen3-VL-8B Instruct, text-only mode Vision-language model used as text encoder. Hidden states from 13 layers, concatenated. FROZEN 02 · BACKBONE Ideogram 4 single-stream DiT 34 transformer layers. Text + image tokens share one sequence. QK-RMSNorm, MRoPE. 9.3B · TRAINED 03 · SAMPLER Euler flow-matching + CFG Asymmetric CFG and logit-normal noise schedule. 12, 20, or 48 denoising steps. RUNTIME 04 · DECODER Flux VAE latent → pixels Unpatch 2×2 latent tokens and decode to RGB. 8× spatial compression. FROZEN Pipeline. 
Two frozen models (Qwen3-VL, VAE) bookend a trained DiT and a runtime sampler.
Figure 1. End-to-end inference pipeline. The 9.3B parameter DiT is the only trained
 component; the text encoder and VAE are reused frozen.
 Model spec
 Field Value 
 parameters 9.3B 
 emb_dim 4608 
 num_layers 34 
 num_heads 18 
 intermediate 12 288 (SwiGLU) 
 adaln_dim 512 
 rope_theta 5 000 000 
 mrope_section (24, 20, 20) 
 latent channels 32 × 2² = 128 
 max text tokens 2048 
 resolution range 256–2048 px per side 
 aspect ratios flexible 
 quantization nf4 and fp8 
 sampler Euler flow-matching, asymmetric CFG 
 Model
The text encoder is
 Qwen3-VL-8B-Instruct [8] in text-only mode. The DiT consumes hidden states from
 13 of its intermediate layers, concatenated along the feature dimension, instead of a single
 hidden slice.
The DiT is 34 transformer blocks operating on one sequence of text and image latent
 tokens. Each block uses self-attention with QK-RMSNorm [9] , 3D Multimodal RoPE [10] [11] that places text and image tokens in one positional frame, and a SwiGLU [12] MLP. AdaLN [6] from the flow-matching timestep modulates
 the attention and MLP residual paths in every block.
The training objective is flow matching [13] [14] : the DiT predicts a velocity field v(z_t, t) that defines an ODE from pure noise
 to a clean latent. At inference, an Euler sampler integrates the ODE over a logit-normal noise
 schedule [15] whose mean auto-adjusts with resolution.
 Asymmetric classifier-free guidance
Classifier-free guidance [16] combines a conditional pass
 (text + image latents) with an unconditional pass. Ideogram 4.0 makes the unconditional pass
 asymmetric : it drops the text tokens entirely instead of replacing them with
 padding, so the unconditional pass runs only over image tokens. The two branches can also
 be tuned independently, which lets us schedule prompt adherence and image quality
 separately across the sampling trajectory.
The V4_QUALITY_48 preset, for example, runs 45 steps at gw=7 
followed by 3 polish steps at gw=3 near t=0 . The shorter
 V4_DEFAULT_20 and V4_TURBO_12 presets follow the same shape with two
 and one polish steps respectively. The polish tail tightens fine detail without over-saturating
 the global composition.
 Structured JSON prompting
The model is trained exclusively on structured JSON captions [21] . Each training caption exhaustively describes every element in the image, with a style
 block and optional bounding boxes and color palettes. Training and inference share one
 prompt format, and the more relationships each caption pins down, the more grounded
 supervision the model extracts per training pair.
The reference pipeline validates every prompt against the JSON schema before generation
 and rejects inputs that do not parse, so the input format at inference time is the same
 one the model saw during training.
 prompt example json 
 {
 "high_level_description": "A cinematic 35mm film photograph of a lone wooden sailboat on a glassy lake at sunset, the boat on a right-third vertical with the horizon at the lower third, in a cool muted blue palette.",
 "style_description": {
 "aesthetics": "Cinematic, minimal, serene, quiet stillness.",
 "lighting": "Cool overcast dusk light with a small warm sun low at the horizon; muted and low-contrast.",
 "photo": "35mm motion-picture film still, 16:9 framing, subtle grain, slightly desaturated.",
 "medium": "Photograph.",
 "color_palette": ["#1B3A5C", "#5B8FB9"]
 },
 "compositional_deconstruction": {
 "background": "Windless evening on a wide lake; horizon at the lower third. Dusty blue-violet sky with a small amber sun at the horizon and a thin gold streak across the glassy teal water. Subtle 35mm grain.",
 "elements": [
 { "type": "obj", "bbox": [380, 590, 660, 720],
 "desc": "Lone wooden sailboat on the right-third vertical in the midground, dark varnished hull and a single tall mast with a slack white sail hanging limp in the still air. No visible crew." },
 { "type": "obj",
 "desc": "Mirror-perfect reflection of the sailboat and its mast doubling straight down into the glassy teal water directly beneath the hull." },
 { "type": "obj",
 "desc": "Out-of-focus reed tips slicing into the lower-left foreground, soft dark blades against the teal water, blurred from proximity to the camera." }
 ]
 }
} Three things this surface gives you that a plain prompt does not:
 Color palette conditioning. Up to 16 hex colors per image (and 5 per element)
 steer the dominant colors directly, not through descriptive language.
 Bounding-box layout. Any element can be placed by bounding box, given as
 [y_min, x_min, y_max, x_max] in 0–1000 normalized
 coordinates (image origin at the top-left). The model honors the boxes through the shared
 MRoPE positional space.
 Typed text elements. A text element carries the literal string
 to render and a separate visual description for its styling. This is the mechanism behind
 multi-line, multi-font in-image text.
 Benchmarks
We evaluate Ideogram 4.0 across five capabilities against the strongest closed-source
 models (GPT Image 2, Nano Banana 2) and every leading open-weight release. The two figures
 below give the headline picture; the model card has the full breakdown.
 Layout control
 0.69
7Bench [17] mIoU: how tightly generated objects sit inside
 their requested bounding boxes.
 Text rendering
 0.97
X-Omni [19] English OCR accuracy on in-image text.
 Spatial reasoning
 0.76
SpatialGenEval [18] accuracy *, combining the spatial-relationship
 and basic-object question splits.
 Prompt alignment
 0.89
Prism-bench [20] alignment track. Following the prompt
 across long, compositional inputs.
* We judge SpatialGenEval with gemini-2.5-flash instead of the leaderboard's
 Qwen2.5-VL-72B . Applied uniformly across all models, so cross-model
 comparisons remain valid.
 Catching up to closed-source on every axis Absolute scores, each axis 0–1. Larger and more balanced area is better. 0.2 0.4 0.6 0.8 1.0 Layout control Spatial reasoning Object fidelity Prompt alignment Text rendering 0.69 *
 Ideogram 3.0 Nano Banana 2 GPT Image 2 Ideogram 4.0 
Figure 2. Five-axis capability radar — Ideogram 4.0 vs leading closed-source models on
 layout control, spatial reasoning, object fidelity, prompt alignment, and text
 rendering.
 Layout control = 7Bench mIoU · Spatial reasoning = SpatialGenEval
 spatial_acc (8 spatial Qs) · Object fidelity = SpatialGenEval
 basic_acc · Prompt alignment = Prism alignment track · Text
 rendering = X-Omni OCR. *With Magic Prompt ON. Small open model, best text rendering Open weights only. Up and to the left is better. 0.5 0.6 0.7 0.8 0.9 1.0 0 20 40 60 80 Parameters (B) Text rendering (X-Omni OCR, 0–1) Ideogram 4.0 
(9.3B)
 Z-Image Base 
(6.15B)
 HiDream-O1 
(17B)
 Qwen-Image 
(20B)
 FLUX.2 [dev] 
(32B)
 Hunyuan Image v3 
(80B MoE)
Figure 3. Parameter efficiency on text rendering (X-Omni EN OCR). Ideogram 4.0 (9.3B)
 sits alone in the small-but-strong corner, ahead of every other open-weight release
 model. Hunyuan Image v3 reports 80B total parameters with ~13B active per token.
Hide closed models
 Designer preference, head to head Pairwise ELO from 4,366 graphic-designer votes across nine
 pipelines. Voters were not told which model produced each image. Higher is better. #1 GPT Image 2 CLOSED 1141 #2 Ideogram 4.0 OPEN 1062 #3 Nano Banana 2 CLOSED 1004 #4 Grok Imagine (2K) CLOSED 990 #5 Luma 1.1 (2K) CLOSED 983 #6 FLUX.2 Pro CLOSED 982 #7 Hunyuan Image v3 OPEN 978 #8 Krea v2 Large CLOSED 959 #9 FLUX.2 [dev] OPEN 900 800 900 1000 1100 1200 ELO score 
Figure 4. Designer-preference ELO from an internal arena where graphic designers pick
 the better of two generations without being told which model produced either image. Bar
 length is the ELO score; the cap-line on each bar marks the 95% confidence interval.
 Ideogram 4.0 sits in second place overall and first among open-weight models.
 Examples
A handful of qualitative samples grouped by capability. Every image below was generated
 with seed = 0 from the fp8 quantized checkpoint; click an image to
 view it larger (click again inside the viewer to toggle 1:1 zoom), and
 View prompt for the JSON.
Hide bounding boxes
 Detail and realism
View prompt
View prompt
View prompt
 Typography and text control
 Six text bounding boxes anchor the title, subtitle, date, tagline, credit, and RSVP. 
View prompt
View prompt
 Six text bounding boxes set each word at its own scale, position, and rotation. 
View prompt
 Layout with bounding boxes
 Four object bounding boxes place the woman, window, monstera, and cat in the scene. 
View prompt
 Twenty-eight bounding boxes mark the items; one text bounding box places the inventory line. 
View prompt
 Eight bounding boxes place the room contents; two boxes set the train label and book spine. 
View prompt
 Color palette control
 #1B3A5C #5B8FB9 
View prompt
 #5C1B1B #C0392B 
View prompt
 #7A5C12 #E6B422 
View prompt
 × JSON prompt 
Copy
×
 {
 "high_level_description": "A tender close-up photograph of a grandfather cradling an infant against his chest in a quiet domestic interior, their foreheads nearly touching as they share a quiet gaze in soft late-afternoon light, shot on Kodak Portra 400 with shallow depth of field.",
 "compositional_deconstruction": {
 "background": "A quiet domestic interior late in the afternoon, dissolved into soft creamy bokeh by shallow depth of field. A cream linen curtain hangs blurred behind the pair, lit by neutral daylight from a north-facing window that rakes gently across the left side of the scene. In the deep background, a brass table lamp casts a small localized amber pool of light. Cool-neutral white balance overall, fine Kodak Portra 400 grain across the frame, no warm global grade.",
 "elements": [
 {
 "type": "obj",
 "desc": "Sixty-year-old man, head and upper chest filling the upper two-thirds of the frame, face at the upper-third, in three-quarter front view with head tilted gently down toward the baby cradled against his chest. Deep forehead creases, crow's-feet around the eyes, a short gray three-day-old stubble beard, thinning combed-back gray hair. Soft charcoal cable-knit sweater. Small closed-mouth smile, slightly glassy eyes catching the window light, gaze directed down at the infant's face. Natural detailed skin with visible pores and fine wrinkles around the eyes."
 },
 {
 "type": "obj",
 "desc": "Infant cradled against the man's chest, head anchored at the lower-third of the frame, foreheads nearly touching the grandfather above. Round cheeks with a faint pink flush, wispy light brown hair, soft translucent skin. Striking pale blue eyes catching the window light, fixed up on the man's face. Tiny fingers gripping the edge of the charcoal sweater. Swaddled in a cream waffle-knit blanket visible at the lower edge."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A macro photograph of a dragonfly perched on the curled tip of a fiddlehead fern at first light, dew droplets beaded along the fern spine and wing membranes, set against a clear blue sky.",
 "compositional_deconstruction": {
 "background": "A clear, cloudless blue sky fills the entire background, bright and evenly lit, graduating from a deeper blue at the top to a paler blue toward the bottom. Smooth and uniform with no clouds, the fern and dragonfly standing out crisply against the open sky. Neutral-cool white balance, clean clarity with no grain.",
 "elements": [
 {
 "type": "obj",
 "desc": "Fiddlehead fern rising diagonally from lower-right to upper-left, tightly curled into its characteristic shepherd's crook shape at the top. Fuzzy brown scales cling along the stem, deep green frond unfurling below. The primary perch for the dragonfly."
 },
 {
 "type": "obj",
 "desc": "Dragonfly perched in profile on the coiled tip of the fiddlehead, positioned slightly right of center on the rule-of-thirds line, body oriented leftward. Iridescent teal-and-cobalt wings held flat and slightly translucent with fine venation visible. Segmented emerald abdomen with thin black banding. Large compound eyes catching pinpoint highlights. Six slender legs gripping the fern spine. Head and thorax in critical focus; abdomen and far wing tips fall into gentle defocus."
 },
 {
 "type": "obj",
 "desc": "Cluster of spherical dew droplets beaded along the fern spine and across the dragonfly's wing membranes. Each droplet holds a tiny inverted reflection of the surrounding foliage, surface tension clearly defined."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A photograph of a quiet West Village side street on an early autumn morning, with 19th-century brownstones along the left, fallen ginkgo and maple leaves scattered across the sidewalk, a half-bare street tree mid-frame, parked cars along the curb, and a lone figure walking away toward a distant intersection.",
 "compositional_deconstruction": {
 "background": "A quiet New York City side street in the West Village on an early autumn morning, shot on a 50mm lens at eye level. The street recedes diagonally from the lower-right foreground toward a vanishing point in the upper-left third. Cool open shade fills the street itself, with soft north-facing morning daylight just clipping the top-floor cornices on the left. Cool grey asphalt and concrete sidewalk surfaces drift with mustard, burnt-orange, and oxblood leaves, especially against the curb and gutters. Sky overhead is a flat pale cool blue-grey, glimpsed between bare branches. Fine Kodak Portra grain throughout.",
 "elements": [
 {
 "type": "obj",
 "desc": "Far intersection in the deep background at the upper-left third vanishing point. Cross-street recedes perpendicular to the camera, with a lamppost on the far corner and low storefronts beyond. Cool open shade, slightly hazy with distance."
 },
 {
 "type": "obj",
 "desc": "A cyclist crossing the far intersection in the deep background, small in the frame, viewed in profile from the side, moving left to right. Dark jacket and pants, head down, gaze directed forward across the intersection. Softly rendered at distance."
 },
 {
 "type": "obj",
 "desc": "Row of 19th-century brownstone facades lining the entire left side of the street, four to five stories tall, receding into the distance. Weathered terracotta-red and chocolate-brown stone, carved cornices catching low morning sun at the top floors, tall double-hung windows, stoops with wrought-iron railings descending to garden-level entrances, planter boxes at garden-level windows. Lower floors in cool shade."
 },
 {
 "type": "obj",
 "desc": "Garden-level café entrance set into one of the brownstones on the left, midground. Recessed doorway down a few steps, a dark-painted wood door with a small glass pane, a window beside it with a planter box. Warm interior light barely visible through the glass."
 },
 {
 "type": "obj",
 "desc": "A mature street tree at mid-frame, trunk ringed by a low black iron tree guard at the sidewalk edge. Bare branches reaching up and outward, still holding scattered clusters of yellow leaves in the upper canopy. In sharp focus as the midground anchor."
 },
 {
 "type": "obj",
 "desc": "A dark forest-green Subaru wagon parked along the curb on the right side of the street, nearest the camera, in three-quarter rear view facing away from camera down the street. Fallen yellow and orange leaves collected on the windshield and hood. Slightly soft in focus."
 },
 {
 "type": "obj",
 "desc": "A silver four-door sedan parked along the curb farther down the street beyond the green Subaru, in three-quarter rear view facing away from camera. Smaller in the frame, slightly softer focus."
 },
 {
 "type": "obj",
 "desc": "A lone figure in the mid-distance walking away from camera down the center of the sidewalk on the left, seen from behind. Long charcoal-grey wool coat reaching below the knee, dark trousers, a brown canvas tote bag slung over the right shoulder. Face not visible to the camera."
 },
 {
 "type": "obj",
 "desc": "Sidewalk along the left side of the street, cool grey concrete slabs, thickly scattered with fallen ginkgo and maple leaves in mustard yellow, burnt orange, and oxblood. Leaves drift against the curb and pile in the gutters."
 },
 {
 "type": "obj",
 "desc": "A few out-of-focus fallen leaves caught mid-fall at the lower-left frame edge in the immediate foreground, in mustard yellow and burnt orange, softly blurred."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A retro-style square 1:1 poster for a \"Mango Sago Social\" team tasting event, featuring bold red typography on a salmon pink background with illustrations of a tall glass of mango sago dessert, fresh mangoes, and scattered sago pearls, composed for a square format.",
 "compositional_deconstruction": {
 "background": "Solid salmon-pink background with scattered decorative elements including small yellow and white confetti-like shapes and thin wavy lines. A stylized sunburst effect radiates from behind the central glass dessert.",
 "elements": [
 {
 "type": "text",
 "bbox": [70, 270, 470, 730],
 "text": "MANGO\nSAGO\nSOCIAL",
 "desc": "Large, bold, blocky sans-serif text in a deep reddish-orange color. The words are stacked vertically in the upper half of the poster. The letters have a slightly distressed or textured appearance."
 },
 {
 "type": "text",
 "bbox": [490, 210, 565, 790],
 "text": "TEAM TASTING EVENT",
 "desc": "Medium-sized sans-serif text in white, centered within a horizontal reddish-orange banner ribbon located below the main title."
 },
 {
 "type": "text",
 "bbox": [580, 170, 700, 830],
 "text": "FRIDAY · JULY 18 · 4–6 PM\nTHE PANTRY · 5TH FLOOR LOUNGE",
 "desc": "Small sans-serif text in white. The first line is on a horizontal reddish-orange banner ribbon. The second line is directly below it on the same color background."
 },
 {
 "type": "obj",
 "desc": "A tall glass filled with an orange-colored beverage containing numerous small translucent spheres (sago pearls). The drink is topped with whipped cream and diced mango pieces. A whole mango sits to the right of the glass."
 },
 {
 "type": "obj",
 "desc": "A halved peach or nectarine lying on its side at the bottom left foreground, showing its pit and juicy interior."
 },
 {
 "type": "obj",
 "desc": ">~25 small translucent sago pearls scattered around the base of the glass dessert and near the halved fruit."
 },
 {
 "type": "text",
 "bbox": [905, 680, 965, 965],
 "text": ">RSVP BY JULY 15<",
 "desc": ">Small sans-serif text in white within a rounded rectangular button shape with a dark reddish-brown border located at the bottom right corner."
 },
 {
 "type": "text",
 "bbox": [855, 200, 905, 800],
 "text": ">Bring your appetite – pearls included<",
 "desc": ">Small cursive script text in dark reddish-brown at the bottom center of the poster."
 },
 {
 "type": "text",
 "bbox": [915, 230, 960, 660],
 "text": ">HOSTED BY THE PEOPLE TEAM<",
 "desc": ">Small all-caps sans-serif text in white at the very bottom center of the poster."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A maximalist square gig poster for Sound & Color Festival 2026, packed edge-to-edge with a stacked cream-yellow headline, tiered lineup of fifteen band names, date strip, sponsor row, and small print, over a magenta-to-cobalt halftone gradient with psychedelic sun-rays radiating from behind the title.",
 "compositional_deconstruction": {
 "background": "Full-bleed gradient field sweeping from electric magenta in the upper-left through deep purple at the center to electric cobalt blue at the lower-right, overlaid with a fine halftone-dot texture and a faint paper-grain across the entire frame. Subtle riso-print registration offset between coral and cyan plates gives the whole field a layered classic gig-poster character. No empty regions — color and texture saturate every corner edge-to-edge.",
 "elements": [
 {
 "type": "obj",
 "desc": "Wavy psychedelic sun-ray graphics radiating outward from behind the headline area in the upper third, the primary background graphic element. Long curving cream and coral ray lines fan in all directions from a central point near the top of the poster, undulating like heat shimmer, with thin and thick alternating widths."
 },
 {
 "type": "obj",
 "desc": "Thin solid black horizontal bar cutting across the upper-middle of the poster, full frame width, serving as the substrate for the date and venue strip."
 },
 {
 "type": "obj",
 "desc": "Bright coral horizontal band stretching across the lower-middle of the poster, full frame width, serving as the substrate for the ticket info strip."
 },
 {
 "type": "text",
 "text": "Three Days One Sound",
 "desc": "Medium-sized arched italic hand-lettered script in coral, curving in a gentle upward arc above the headline, horizontally centered, with a slight riso offset shadow."
 },
 {
 "type": "text",
 "text": "SOUND & COLOR\nFESTIVAL 2026",
 "desc": "Headline-sized display type dominating the upper third of the poster, stacked on two lines and spanning nearly the full frame width edge-to-edge. Heavy condensed sans-serif in cream-yellow with a thin coral drop-shadow offset to the lower-right, horizontal, centered."
 },
 {
 "type": "text",
 "text": "JULY 17 • RIVERSIDE PARK",
 "desc": "Medium-sized bold condensed sans-serif caps in cream-yellow, set on the thin black bar across the upper-middle, horizontal, centered, tight tracking with bullet-dot separator between date and venue."
 },
 {
 "type": "text",
 "text": "THE VELVET ORBIT\nMIDNIGHT PARADE",
 "desc": "Large tier-one headliner names, the biggest type in the lineup block, stacked on two lines just beneath the date strip. Cream condensed display sans-serif, horizontal, centered, slightly smaller than the main headline above."
 },
 {
 "type": "text",
 "text": "CORAL STATIC • NEON FERNS • PAPER TIGERS",
 "desc": "Medium-large tier-two sub-headliner row, smaller than the tier-one names above but clearly larger than tier-three below. Coral condensed sans-serif caps, single horizontal row, centered, bullet-dot separators between band names."
 },
 {
 "type": "text",
 "text": "HOLLOW CHORUS • RIVER QUEEN • AMBER SIGNAL • GLASS HOUNDS",
 "desc": "Medium tier-three act row, smaller than tier-two above and larger than tier-four below. Cream tracked condensed sans-serif caps, single horizontal row, centered, bullet-dot separators."
 },
 {
 "type": "text",
 "text": "KID SAINT • THE LOW TIDE • SOFT MACHINERY •\nECHO BUREAU • WILD CITRUS • MOONLIT TRANSIT",
 "desc": "Smaller tier-four opening acts, the smallest tier in the lineup block, set in two tight horizontal rows. Cream tracked sans-serif caps, centered, bullet-dot separators between names."
 },
 {
 "type": "text",
 "text": "TICKETS FROM $129 • 3-DAY PASSES $299 • SOUNDANDCOLORFEST.COM",
 "desc": "Small bold sans-serif caps in cream-yellow set on the coral horizontal band, horizontal, centered, tight tracking with bullet-dot separators."
 },
 {
 "type": "text",
 "text": "PRESENTED BY HORIZON SOUNDS • PRISMFM • CITRUS CO. • NORTHWIND BREWING • ATLAS RECORDS",
 "desc": "Small muted-cream sans-serif wordmarks set in a single horizontal row near the bottom, evenly spaced, monochrome lockups, centered, bullet-dot separators between sponsor names."
 },
 {
 "type": "text",
 "text": "ALL AGES • RAIN OR SHINE • NO RE-ENTRY • LINEUP SUBJECT TO CHANGE • ©2026 SOUND & COLOR FESTIVAL LLC",
 "desc": "Tiny tracked sans-serif caps in cream along the very bottom edge, horizontal, centered, the smallest type on the poster, with bullet-dot separators between clauses."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A square typographic poster assembling six expressive words in wildly different lettering styles on a warm off-white paper ground, with oxblood blackletter, hairline vertical sans-serif, sage copperplate script, cyan pixel block, mustard marker brush, and navy serif caps filling the canvas.",
 "compositional_deconstruction": {
 "background": "Warm off-white cream paper ground filling the full square frame, edge-to-edge full-bleed composition with subtle deckled texture across the surface. Slight riso-print registration offset visible between some elements suggests analog print energy. No decorative borders, no drop shadows, no gradients — just the textured paper field carrying the typography.",
 "elements": [
 {
 "type": "text",
 "bbox": [20, 20, 540, 700],
 "text": "WILD",
 "desc": "Massive headline-sized chunky condensed blackletter display type dominating the upper-left quadrant, deep oxblood red ink with rough bleed edges at the stroke terminals. Stacked vertically with each letter on its own line, left-aligned, occupying roughly half the frame height."
 },
 {
 "type": "text",
 "bbox": [60, 870, 700, 980],
 "text": "SLOW",
 "desc": "Tall narrow word running vertically down the right edge of the frame, reading top-to-bottom. Hairline modern sans-serif, all caps, thin charcoal strokes, letters stacked one above the other, right-aligned to the frame edge."
 },
 {
 "type": "text",
 "bbox": [350, 250, 680, 780],
 "text": "softly",
 "desc": "Medium-large flowing copperplate calligraphy script swooping diagonally across the center of the frame from lower-left up to upper-right. Soft sage green ink, looping connected lowercase letterforms with an exaggerated tail flourish extending from the final 'y'."
 },
 {
 "type": "text",
 "bbox": [760, 40, 900, 420],
 "text": "PIXEL",
 "desc": "Pixelated blocky word built from square bitmap glyphs anchored in the lower-left corner. Electric cyan color, horizontal orientation, faint scanline shimmer across the glyph blocks, left-aligned."
 },
 {
 "type": "text",
 "bbox": [690, 560, 850, 900],
 "text": "LOUD",
 "desc": "Medium-sized hand-drawn marker word in uneven brushy strokes, mustard yellow with rough ink texture and visible dry-brush gaps. Tilted slightly off-axis clockwise in the mid-right area, all caps, centered within its zone."
 },
 {
 "type": "text",
 "bbox": [910, 600, 960, 970],
 "text": "STUDIO NINE",
 "desc": "Small ornate serif word tucked into the lower-right corner like a publisher's mark. Deep navy, tiny tracked caps with wide letter-spacing, horizontal, right-aligned to the frame edge."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A soft contemporary illustration of a cozy late-afternoon living room with a young woman curled sideways on a mustard-yellow sofa reading a paperback, a tall window to her right showing rooftops and a tree branch, a tabby cat asleep nearby, and warm daylight pouring across the rug.",
 "compositional_deconstruction": {
 "background": "Warm off-white interior walls in a cozy living room rendered in soft contemporary illustration style with clean confident linework, flat-but-warm color fills, and light cel-shading. A woven jute area rug anchors the seating arrangement, its edge slicing into the lower-left foreground. Daylight pours in from the right window casting a soft elongated rectangle of light across the rug and the woman's lap; the rest of the room sits in quiet ambient warmth. Palette of mustard yellow, cream, walnut brown, sage green, and pale sky blue. Slight paper-grain texture across the whole image.",
 "elements": [
 {
 "type": "obj",
 "bbox": [40, 660, 835, 990],
 "desc": "Tall floor-to-ceiling window filling the right third of the frame, thin black mullions dividing six panes in a 2x3 grid. Sheer white curtains pulled aside at each side. Through the glass: a leafy sage-green tree branch crossing the foreground pane, a row of red-tiled rooftops in the midground, and a pale sky-blue expanse above with two small dark birds drifting across."
 },
 {
 "type": "obj",
 "desc": "Framed botanical print mounted on the wall above the sofa, simple thin black rectangular frame around a cream background with a single sage-green leafy stem illustration centered inside."
 },
 {
 "type": "obj",
 "desc": "Mustard-yellow linen sofa anchored slightly left of center, low back and rounded arms, viewed in three-quarter front view facing the camera. Soft cel-shaded folds in the cushions, warm ambient tone across the body with a brighter patch where daylight falls."
 },
 {
 "type": "obj",
 "bbox": [295, 150, 660, 480],
 "desc": "Young woman seated sideways on the sofa, body angled toward the window at right, legs tucked under her. Soft brown hair loose over one shoulder, fair skin, wearing a cream cable-knit sweater and dark olive joggers, bare feet peeking out. Both hands hold an open paperback at chest height, head tilted down toward the page, gaze directed at the book. A soft rectangle of window light falls across her lap."
 },
 {
 "type": "obj",
 "bbox": [560, 535, 890, 655],
 "desc": "Small potted monstera beside the window on the floor, terracotta pot with a flared rim, broad split sage-green leaves rising upward and catching bright daylight along their upper edges."
 },
 {
 "type": "obj",
 "desc": "Round walnut coffee table in front of the sofa, rich brown wood grain visible on the top surface, slim tapered legs. On its surface: a half-full cream ceramic mug at the left, a small stack of three books in muted spines (sage, cream, walnut) at the back, and a brass candlestick holding a lit taper with a small warm flame at the right."
 },
 {
 "type": "obj",
 "bbox": [775, 90, 905, 340],
 "desc": "Tabby cat curled asleep on the jute rug near the woman's feet, orange-brown striped fur with darker bands, eyes closed, tail wrapped neatly around its front paws, body forming a compact oval."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A square top-down editorial spread of a household junk drawer on a soft peach (#ffd6b8) with faint terrazzo speckles background titled 'JUNK DRAWER, CATALOGUED'. A warm-tan wooden drawer interior fills the middle of the frame; 28 distinct hand-drawn small objects (rubber-band ball, batteries, buttons, safety pin, sewing needle, postage stamp, expired coupon, hex key, screwdriver bit, tape measure, birthday candle, matchbook, string ball, twist tie, flash drive, earplugs, playing card, die, paperclips, rubber stopper, loose key, rubber washer, deflated balloon, scribbled note) are scattered across the drawer interior, each its own bbox.",
 "style_description": {
 "aesthetics": "top-down household-drawer editorial inventory, hand-drawn doodles, peach terrazzo",
 "lighting": "n/a, flat illustrated with soft drop shadows",
 "medium": "digital vector graphic, square editorial poster",
 "art_style": "hand-drawn editorial illustration, flat color fills with subtle ink linework, no real photography of people"
 },
 "compositional_deconstruction": {
 "background": "soft peach (#ffd6b8) with faint terrazzo speckles fills the entire square frame; no people, no extra props or decorative elements outside the listed elements.",
 "elements": [
 {
 "type": "text",
 "text": "JUNK DRAWER, CATALOGUED",
 "desc": "Enormous extra-bold uppercase deep-burgundy (#7f1d1d) sans-serif title 'JUNK DRAWER, CATALOGUED' filling the top band, single line, tight letter-spacing, magazine-style headline."
 },
 {
 "type": "text",
 "text": "— ONE SATURDAY'S WORK",
 "desc": "Italic medium dark-charcoal (#1f1f1f) serif deck '— ONE SATURDAY'S WORK' centered horizontally below the title, single line, magazine-spread feel."
 },
 {
 "type": "obj",
 "bbox": [275, 60, 895, 940],
 "desc": "Big hand-drawn warm-tan wooden drawer interior filling the middle of the frame, top-down view with a thin charcoal border, subtle wood-grain texture, soft drop shadow at the edges."
 },
 {
 "type": "obj",
 "bbox": [745, 203, 866, 303],
 "desc": "Small ball of tangled multicolored rubber bands, doodle 1 of 28 — 'rubber band ball'."
 },
 {
 "type": "obj",
 "bbox": [589, 694, 710, 794],
 "desc": "Single aa battery, sky-blue and white wrapper, doodle 2 of 28 — 'aa battery a'."
 },
 {
 "type": "obj",
 "bbox": [740, 574, 861, 674],
 "desc": "Single aa battery, copper-top wrapper, doodle 3 of 28 — 'aa battery b'."
 },
 {
 "type": "obj",
 "bbox": [748, 92, 869, 192],
 "desc": "Smaller aaa battery, charcoal wrapper, doodle 4 of 28 — 'aaa battery'."
 },
 {
 "type": "obj",
 "bbox": [305, 93, 426, 193],
 "desc": "Small brown four-hole shirt button, doodle 5 of 28 — 'button a'."
 },
 {
 "type": "obj",
 "bbox": [599, 572, 720, 672],
 "desc": "Small warm-yellow two-hole button, doodle 6 of 28 — 'button b'."
 },
 {
 "type": "obj",
 "bbox": [459, 447, 580, 547],
 "desc": "Single chrome safety pin, closed, doodle 7 of 28 — 'safety pin'."
 },
 {
 "type": "obj",
 "bbox": [740, 447, 861, 547],
 "desc": "Single steel sewing needle with a tiny thread looped through the eye, doodle 8 of 28 — 'sewing needle'."
 },
 {
 "type": "obj",
 "bbox": [301, 806, 422, 906],
 "desc": "Small square us postage stamp with a faded flower design, doodle 9 of 28 — 'postage stamp'."
 },
 {
 "type": "obj",
 "bbox": [744, 813, 865, 913],
 "desc": "Rectangular warm-cream coupon with 'expired' stamped diagonally, doodle 10 of 28 — 'expired coupon'."
 },
 {
 "type": "obj",
 "bbox": [600, 815, 721, 915],
 "desc": "Single chrome allen-wrench hex key, l-shaped, doodle 11 of 28 — 'hex key'."
 },
 {
 "type": "obj",
 "bbox": [311, 204, 432, 304],
 "desc": "Single chrome screwdriver bit, hex-shank, doodle 12 of 28 — 'screwdriver bit'."
 },
 {
 "type": "obj",
 "bbox": [453, 564, 574, 664],
 "desc": "Small round retractable tape-measure case, deep-yellow, doodle 13 of 28 — 'tape measure'."
 },
 {
 "type": "obj",
 "bbox": [456, 687, 577, 787],
 "desc": "Tiny pink birthday candle, partly burned, doodle 14 of 28 — 'birthday candle'."
 },
 {
 "type": "obj",
 "bbox": [589, 332, 710, 432],
 "desc": "Small warm-cream matchbook with a red stripe and a few matches inside, doodle 15 of 28 — 'matchbook'."
 },
 {
 "type": "obj",
 "bbox": [302, 568, 423, 668],
 "desc": "Tiny ball of twine string, loose end peeking out, doodle 16 of 28 — 'string ball'."
 },
 {
 "type": "obj",
 "bbox": [749, 332, 870, 432],
 "desc": "Single green twist tie, looped, doodle 17 of 28 — 'twist tie'."
 },
 {
 "type": "obj",
 "bbox": [312, 683, 433, 783],
 "desc": "Small silver usb flash drive with a blue cap, doodle 18 of 28 — 'flash drive'."
 },
 {
 "type": "obj",
 "bbox": [601, 211, 722, 311],
 "desc": "Two foam earplugs, neon-orange, doodle 19 of 28 — 'earplug pair'."
 },
 {
 "type": "obj",
 "bbox": [302, 454, 423, 554],
 "desc": "Single playing card (joker), face-up, doodle 20 of 28 — 'playing card'."
 },
 {
 "type": "obj",
 "bbox": [602, 448, 723, 548],
 "desc": "Small white six-sided die showing the face '5', doodle 21 of 28 — 'dice'."
 },
 {
 "type": "obj",
 "bbox": [459, 216, 580, 316],
 "desc": "Single chrome paperclip, slightly bent, doodle 22 of 28 — 'paper clip a'."
 },
 {
 "type": "obj",
 "bbox": [745, 695, 866, 795],
 "desc": "Single rose-gold paperclip, classic shape, doodle 23 of 28 — 'paper clip b'."
 },
 {
 "type": "obj",
 "bbox": [600, 97, 721, 197],
 "desc": "Small black rubber stopper, conical, doodle 24 of 28 — 'rubber stopper'."
 },
 {
 "type": "obj",
 "bbox": [450, 85, 571, 185],
 "desc": "Lone brass key, no ring, slight tarnish, doodle 25 of 28 — 'loose key'."
 },
 {
 "type": "obj",
 "bbox": [444, 817, 565, 917],
 "desc": "Small grey rubber washer, ring-shaped, doodle 26 of 28 — 'rubber washer'."
 },
 {
 "type": "obj",
 "bbox": [454, 335, 575, 435],
 "desc": "Deflated lime-green balloon, limp, knot tied at neck, doodle 27 of 28 — 'balloon (deflated)'."
 },
 {
 "type": "obj",
 "bbox": [308, 336, 429, 436],
 "desc": "Folded scrap of warm-cream paper with 'happy birthday' scribbled on it, doodle 28 of 28 — 'birthday note'."
 },
 {
 "type": "text",
 "bbox": [905, 60, 965, 940],
 "text": "INVENTORY: 28 THINGS. ONE COMPLETELY UNIDENTIFIED.",
 "desc": "Italic medium dark-charcoal (#1f1f1f) serif footer line centered at the bottom."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A casual iPhone snapshot of a toddler's bedroom mid-afternoon after play, with an unmade twin bed anchoring the upper third and scattered toys filling the lower two-thirds in chaotic disarray.",
 "compositional_deconstruction": {
 "background": "A toddler's bedroom interior in mid-afternoon. Pale neutral walls with cool-toned ambient daylight spilling in from an unseen window on the left side, casting soft even light across the room. Light beige low-pile carpet covers the floor, slightly rumpled from activity. The wall carries faint scuff marks at child height. Neutral cool white balance throughout, no warm grading. Fine phone-snapshot grain consistent across the frame.",
 "elements": [
 {
 "type": "obj",
 "bbox": [120, 150, 430, 720],
 "desc": "Unmade twin bed anchoring the upper third of the frame, headboard against the back wall. Rumpled pastel-blue duvet half-kicked off the mattress, bunched toward the foot. Two stuffed animals slumped against the wooden headboard — a worn brown teddy bear on the left, a pink bunny on the right with floppy ears."
 },
 {
 "type": "obj",
 "bbox": [300, 700, 600, 990],
 "desc": "Plastic toy kitchen pushed against the right wall, primary colors — red oven door hanging open, yellow cabinets, blue sink area. A small plastic frying pan dangles from the oven handle by its loop."
 },
 {
 "type": "obj",
 "bbox": [610, 760, 800, 990],
 "desc": "Wooden dresser drawer pulled halfway out on the right side, light oak finish. Socks and underwear tumbling onto the carpet below — a pair of striped socks, a green tee, and folded underwear spilling over the front edge."
 },
 {
 "type": "obj",
 "bbox": [360, 20, 545, 210],
 "desc": "Nightstand beside the bed on the left, light wood. A white ceramic plate holds three half-eaten apple slices with crumbs scattered around them. A blue sippy cup tipped on its side next to the plate, lid still attached."
 },
 {
 "type": "obj",
 "bbox": [710, 360, 920, 710],
 "desc": "Wooden train set tracks tangled across the carpet in the center-left foreground, interlocking brown rails forming loops and crossings. Three wooden locomotives derailed at different angles — one upright, one on its side showing painted wheels, one tipped backward."
 },
 {
 "type": "obj",
 "bbox": [560, 380, 705, 610],
 "desc": "Collapsed tower of mismatched building blocks near the rug edge, individual cubes in red, yellow, blue, and green scattered outward in a radial pattern across the carpet. Larger blocks clustered at the center, smaller ones fanning out."
 },
 {
 "type": "obj",
 "bbox": [625, 640, 790, 880],
 "desc": "Open cardboard box of crayons tipped on its side, wax crayons in assorted bright colors spilling out across an unrolled coloring book. Pages show crayon marks in waxy streaks, partially filled drawings visible."
 },
 {
 "type": "obj",
 "bbox": [725, 30, 985, 350],
 "desc": "Small wooden rocking horse in the foreground left, painted cream with a soft yarn mane and curved red rockers, facing right."
 },
 {
 "type": "text",
 "bbox": [800, 430, 865, 670],
 "text": "LEARNING EXPRESS",
 "desc": "Small printed label on the side of the largest wooden train car in the center-left. Black sans-serif font on a cream-colored rectangular sticker, horizontal, oriented along the length of the train car."
 },
 {
 "type": "text",
 "bbox": [600, 250, 745, 350],
 "text": "ABC",
 "desc": "Bold lettering on the spine of a picture book lying face-down near the block tower. Large red serif capitals on a white spine, vertical orientation along the book's length."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A detailed ink-and-watercolor illustration of a sprawling fantasy floating city of interconnected airborne islands drifting through a dreamy sky in the low light of late afternoon, with a baroque cathedral spire at the center, suspension bridges, airships, hanging gardens, and a cloud sea below.",
 "style_description": {
 "aesthetics": "Romantic, ornate, and dreamy; grand sweeping scale with a centered focal composition and deep atmospheric depth.",
 "lighting": "Soft, low-angle light of late afternoon with a gentle glow blooming around every light source and pale atmospheric haze softening the far distance.",
 "medium": "Ink and watercolor.",
 "art_style": "Painterly and romantic illustration with fine, crisp linework.",
 "color_palette": ["#1B3A5C", "#5B8FB9"]
 },
 "compositional_deconstruction": {
 "background": "Dreamy sky in the low light of late afternoon spanning the full frame, luminous in the cloud highlights, softer across the mid-cloud shadows, deep in the lowest recesses. A layered cloud sea rolls beneath all the islands, broken by shafts of soft light filtering down from above. The far distance recedes into pale atmospheric haze where linework softens to suggestion. Ink-and-watercolor illustration, painterly and romantic, with soft glow blooming around every light source.",
 "elements": [
 {
 "type": "obj",
 "desc": "Distant flock of small silhouetted birds threading between the farthest islands in the upper-right background, rendered as tiny dark dashes fading into the pale haze toward the horizon."
 },
 {
 "type": "obj",
 "desc": "Largest central floating island in the midground, crowned with a tall baroque cathedral spire wrapped in copper clockwork gears, flying buttresses extending outward into open air. Stained-glass rose windows on the spire catch the light. Filling roughly 50% of the frame height as the focal subject."
 },
 {
 "type": "obj",
 "desc": "Exposed clockwork mechanisms built into the central island's underside — oversized copper gears, swinging pendulums, escapement wheels half-visible through wrought scaffolding, rendered in crisp linework."
 },
 {
 "type": "obj",
 "desc": "Cascading waterfall pouring from the underside of the central island, breaking into mist before dissolving into the cloud sea below. Pale wash with soft edge bloom."
 },
 {
 "type": "obj",
 "desc": "Cluster of smaller satellite islands in the upper-left midground, each topped with ornate towers, onion domes, and pitched slate roofs in steampunk-baroque fusion. Cascading waterfalls trail from their undersides."
 },
 {
 "type": "obj",
 "desc": "Cluster of smaller satellite islands on the upper-right side, ornate towers and onion domes with pitched slate roofs, hanging gardens spilling over the edges in tangled cascades of vines, wisteria, and trailing roses. Waterfalls trail beneath."
 },
 {
 "type": "obj",
 "desc": "Winding suspension bridges of wrought-iron filigree and rope cabling stitching the central island to its satellite neighbors, small lanterns strung along their lengths glowing."
 },
 {
 "type": "obj",
 "desc": "Large airship drifting in the left midground between districts, brass hull riveted in panels, balloon envelope ribbed with copper bands, small propeller turning at the stern. Side profile, moving rightward."
 },
 {
 "type": "obj",
 "desc": "Mid-sized airship in the upper-right midground, brass-hulled with a ribbed copper-banded envelope, propeller at the stern, oriented in three-quarter view drifting leftward toward the central spire."
 },
 {
 "type": "obj",
 "desc": "Smallest airship drifting in the lower-center midground beneath the central island, brass hull and ribbed envelope, seen in profile, smaller in scale due to depth."
 },
 {
 "type": "obj",
 "desc": "Tiny silhouetted figures bustling through tiered open-air markets on the central island, crossing bridges, leaning on balcony railings, queuing at airship docks. Rendered as small dark figures at distance, ~40 visible."
 },
 {
 "type": "obj",
 "desc": "Hanging gardens spilling over the central island's edges in tangled cascades of vines, wisteria, and trailing roses, softening the architectural lines."
 },
 {
 "type": "obj",
 "desc": "Foreground island corner slicing into the lower-left edge of the frame, partial stone balustrade with carved baroque detailing and a single wrought-iron lantern hanging from a bracket, glowing. Rendered in soft focus, larger in scale due to proximity to the lens."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A detailed ink-and-watercolor illustration of a sprawling fantasy floating city of interconnected airborne islands drifting through a dreamy sky in the low light of late afternoon, with a baroque cathedral spire at the center, suspension bridges, airships, hanging gardens, and a cloud sea below.",
 "style_description": {
 "aesthetics": "Romantic, ornate, and dreamy; grand sweeping scale with a centered focal composition and deep atmospheric depth.",
 "lighting": "Soft, low-angle light of late afternoon with a gentle glow blooming around every light source and pale atmospheric haze softening the far distance.",
 "medium": "Ink and watercolor.",
 "art_style": "Painterly and romantic illustration with fine, crisp linework.",
 "color_palette": ["#5C1B1B", "#C0392B"]
 },
 "compositional_deconstruction": {
 "background": "Dreamy sky in the low light of late afternoon spanning the full frame, luminous in the cloud highlights, softer across the mid-cloud shadows, deep in the lowest recesses. A layered cloud sea rolls beneath all the islands, broken by shafts of soft light filtering down from above. The far distance recedes into pale atmospheric haze where linework softens to suggestion. Ink-and-watercolor illustration, painterly and romantic, with soft glow blooming around every light source.",
 "elements": [
 {
 "type": "obj",
 "desc": "Distant flock of small silhouetted birds threading between the farthest islands in the upper-right background, rendered as tiny dark dashes fading into the pale haze toward the horizon."
 },
 {
 "type": "obj",
 "desc": "Largest central floating island in the midground, crowned with a tall baroque cathedral spire wrapped in copper clockwork gears, flying buttresses extending outward into open air. Stained-glass rose windows on the spire catch the light. Filling roughly 50% of the frame height as the focal subject."
 },
 {
 "type": "obj",
 "desc": "Exposed clockwork mechanisms built into the central island's underside — oversized copper gears, swinging pendulums, escapement wheels half-visible through wrought scaffolding, rendered in crisp linework."
 },
 {
 "type": "obj",
 "desc": "Cascading waterfall pouring from the underside of the central island, breaking into mist before dissolving into the cloud sea below. Pale wash with soft edge bloom."
 },
 {
 "type": "obj",
 "desc": "Cluster of smaller satellite islands in the upper-left midground, each topped with ornate towers, onion domes, and pitched slate roofs in steampunk-baroque fusion. Cascading waterfalls trail from their undersides."
 },
 {
 "type": "obj",
 "desc": "Cluster of smaller satellite islands on the upper-right side, ornate towers and onion domes with pitched slate roofs, hanging gardens spilling over the edges in tangled cascades of vines, wisteria, and trailing roses. Waterfalls trail beneath."
 },
 {
 "type": "obj",
 "desc": "Winding suspension bridges of wrought-iron filigree and rope cabling stitching the central island to its satellite neighbors, small lanterns strung along their lengths glowing."
 },
 {
 "type": "obj",
 "desc": "Large airship drifting in the left midground between districts, brass hull riveted in panels, balloon envelope ribbed with copper bands, small propeller turning at the stern. Side profile, moving rightward."
 },
 {
 "type": "obj",
 "desc": "Mid-sized airship in the upper-right midground, brass-hulled with a ribbed copper-banded envelope, propeller at the stern, oriented in three-quarter view drifting leftward toward the central spire."
 },
 {
 "type": "obj",
 "desc": "Smallest airship drifting in the lower-center midground beneath the central island, brass hull and ribbed envelope, seen in profile, smaller in scale due to depth."
 },
 {
 "type": "obj",
 "desc": "Tiny silhouetted figures bustling through tiered open-air markets on the central island, crossing bridges, leaning on balcony railings, queuing at airship docks. Rendered as small dark figures at distance, ~40 visible."
 },
 {
 "type": "obj",
 "desc": "Hanging gardens spilling over the central island's edges in tangled cascades of vines, wisteria, and trailing roses, softening the architectural lines."
 },
 {
 "type": "obj",
 "desc": "Foreground island corner slicing into the lower-left edge of the frame, partial stone balustrade with carved baroque detailing and a single wrought-iron lantern hanging from a bracket, glowing. Rendered in soft focus, larger in scale due to proximity to the lens."
 }
 ]
 }
}
 JSON prompt 
Copy
×
 {
 "high_level_description": "A detailed ink-and-watercolor illustration of a sprawling fantasy floating city of interconnected airborne islands drifting through a dreamy sky in the low light of late afternoon, with a baroque cathedral spire at the center, suspension bridges, airships, hanging gardens, and a cloud sea below.",
 "style_description": {
 "aesthetics": "Romantic, ornate, and dreamy; grand sweeping scale with a centered focal composition and deep atmospheric depth.",
 "lighting": "Soft, low-angle light of late afternoon with a gentle glow blooming around every light source and pale atmospheric haze softening the far distance.",
 "medium": "Ink and watercolor.",
 "art_style": "Painterly and romantic illustration with fine, crisp linework.",
 "color_palette": ["#7A5C12", "#E6B422"]
 },
 "compositional_deconstruction": {
 "background": "Dreamy sky in the low light of late afternoon spanning the full frame, luminous in the cloud highlights, softer across the mid-cloud shadows, deep in the lowest recesses. A layered cloud sea rolls beneath all the islands, broken by shafts of soft light filtering down from above. The far distance recedes into pale atmospheric haze where linework softens to suggestion. Ink-and-watercolor illustration, painterly and romantic, with soft glow blooming around every light source.",
 "elements": [
 {
 "type": "obj",
 "desc": "Distant flock of small silhouetted birds threading between the farthest islands in the upper-right background, rendered as tiny dark dashes fading into the pale haze toward the horizon."
 },
 {
 "type": "obj",
 "desc": "Largest central floating island in the midground, crowned with a tall baroque cathedral spire wrapped in copper clockwork gears, flying buttresses extending outward into open air. Stained-glass rose windows on the spire catch the light. Filling roughly 50% of the frame height as the focal subject."
 },
 {
 "type": "obj",
 "desc": "Exposed clockwork mechanisms built into the central island's underside — oversized copper gears, swinging pendulums, escapement wheels half-visible through wrought scaffolding, rendered in crisp linework."
 },
 {
 "type": "obj",
 "desc": "Cascading waterfall pouring from the underside of the central island, breaking into mist before dissolving into the cloud sea below. Pale wash with soft edge bloom."
 },
 {
 "type": "obj",
 "desc": "Cluster of smaller satellite islands in the upper-left midground, each topped with ornate towers, onion domes, and pitched slate roofs in steampunk-baroque fusion. Cascading waterfalls trail from their undersides."
 },
 {
 "type": "obj",
 "desc": "Cluster of smaller satellite islands on the upper-right side, ornate towers and onion domes with pitched slate roofs, hanging gardens spilling over the edges in tangled cascades of vines, wisteria, and trailing roses. Waterfalls trail beneath."
 },
 {
 "type": "obj",
 "desc": "Winding suspension bridges of wrought-iron filigree and rope cabling stitching the central island to its satellite neighbors, small lanterns strung along their lengths glowing."
 },
 {
 "type": "obj",
 "desc": "Large airship drifting in the left midground between districts, brass hull riveted in panels, balloon envelope ribbed with copper bands, small propeller turning at the stern. Side profile, moving rightward."
 },
 {
 "type": "obj",
 "desc": "Mid-sized airship in the upper-right midground, brass-hulled with a ribbed copper-banded envelope, propeller at the stern, oriented in three-quarter view drifting leftward toward the central spire."
 },
 {
 "type": "obj",
 "desc": "Smallest airship drifting in the lower-center midground beneath the central island, brass hull and ribbed envelope, seen in profile, smaller in scale due to depth."
 },
 {
 "type": "obj",
 "desc": "Tiny silhouetted figures bustling through tiered open-air markets on the central island, crossing bridges, leaning on balcony railings, queuing at airship docks. Rendered as small dark figures at distance, ~40 visible."
 },
 {
 "type": "obj",
 "desc": "Hanging gardens spilling over the central island's edges in tangled cascades of vines, wisteria, and trailing roses, softening the architectural lines."
 },
 {
 "type": "obj",
 "desc": "Foreground island corner slicing into the lower-left edge of the frame, partial stone balustrade with carved baroque detailing and a single wrought-iron lantern hanging from a bracket, glowing. Rendered in soft focus, larger in scale due to proximity to the lens."
 }
 ]
 }
}
 Resolution flexibility
A single set of weights covers everything from square thumbnails to ultrawide banners. The
 noise schedule auto-adjusts per resolution, so you do not need a dedicated model for phone
 wallpapers, social headers, or 2K finals.
 Use case Resolution 
 Square 1024 × 1024 
 Landscape 1536 × 1024 
 Portrait 1024 × 1536 
 Widescreen 1920 × 1088 
 Ultrawide 2048 × 768 
 Phone wallpaper 1024 × 1792 
 Social banner 1584 × 396 
 Safety
Open weights ship with three layers of mitigation. Pre-training data is filtered through
 NSFW classifiers across multiple categories before the model ever sees it, so the base
 distribution does not contain the content we explicitly do not want it to reproduce.
 Post-training procedures further reduce the probability of unsafe generations, even for
 prompts that explicitly request them. At inference time, the reference pipeline screens
 every prompt and every output through Hive moderation, and we require equivalent or
 stronger filtering for any redistributed deployment.
 Open weight
Weights, inference code, full prompting guide, and sampler presets are public. The
 repository ships both fp8 and nf4 checkpoints; the nf4 variant fits on a single 24 GB GPU.
 Get the model
 Weights on Hugging Face. Inference code, prompting guide, and license on GitHub.
 Hugging Face GitHub API 
 References
Tencent Hunyuan.
 HunyuanImage 3.0 Technical Report . 2025. 
Z-Image Team.
 Z-Image: An Efficient Image Generation Foundation Model with Single-Stream Diffusion
 Transformer . 2025. 
Cai et al.
 HiDream-O1-Image: A Natively Unified Image Generative Foundation Model with
 Pixel-level Unified Transformer . 2026. 
Black Forest Labs.
 FLUX.2: Frontier Visual Intelligence . 2025. 
Wu et al.
 Qwen-Image Technical Report . 2025. 
Peebles, Xie.
 Scalable Diffusion Models with Transformers . ICCV 2023. 
Rombach, Blattmann, Lorenz, Esser, Ommer.
 High-Resolution Image Synthesis with Latent Diffusion Models . CVPR 2022. 
Qwen Team.
 Qwen3-VL Technical Report . 2025. 
Dehghani et al.
 Scaling Vision Transformers to 22 Billion Parameters . ICML 2023. 
Su, Lu, Pan, Murtadha, Wen, Liu.
 RoFormer: Enhanced Transformer with Rotary Position Embedding . 2021. 
Wang et al.
 Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution . 2024. 
Shazeer.
 GLU Variants Improve Transformer . 2020. 
Lipman, Chen, Ben-Hamu, Nickel, Le.
 Flow Matching for Generative Modeling . ICLR 2023. 
Liu, Gong, Liu.
 Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow . ICLR 2023. 
Esser et al.
 Scaling Rectified Flow Transformers for High-Resolution Image Synthesis . ICML 2024. 
Ho, Salimans.
 Classifier-Free Diffusion Guidance . 2022. 
Izzo et al.
 7Bench: a Comprehensive Benchmark for Layout-guided Text-to-Image Models . ICIAP 2025. 
Wang et al.
 Everything in Its Place: Benchmarking Spatial Intelligence of Text-to-Image Models . ICLR 2026. 
Geng et al.
 X-Omni: Reinforcement Learning Makes Discrete Autoregressive Image Generative Models
 Great Again . 2025. 
Fang et al.
 FLUX-Reason-6M & PRISM-Bench: A Million-Scale Text-to-Image Reasoning Dataset and
 Comprehensive Benchmark . ICLR 2026. 
Gutflaish et al.
 Generating an Image From 1,000 Words: Enhancing Text-to-Image With Structured
 Captions . 2025. 
 Cite this work
 bibtex 
 @misc{ideogram-4-2026,
 author = {Ideogram AI},
 title = {{Ideogram 4.0}},
 year = {2026},
 howpublished = {\url{https://ideogram.ai/blog/ideogram-4.0/}}
} We're hiring
We're looking for Research Scientists and Research Engineers to work on next-generation
 generative models and the products built on top of them. Interested candidates please
 apply at
 ideogram.ai/careers .
 Start building with Ideogram today
 Build with API Try in App 
 Think it. Make it. Own it.
Ideogram 4.0 gives visual ideas somewhere to go: into products, agents, campaigns, and
 finished design systems.
 Ideogram 4.0 Ideogram 3.0 Custom Image Models Background Remover Print on Demand Editable text layers Character consistency Styles 
 Enterprise Pricing Careers API MCP Terms of service Privacy Policy 
 X YouTube LinkedIn Instagram TikTok Discord 
© 2026 Ideogram, Inc. All rights reserved.
×
 Contact sales
 Tell us what you are building.
Share a few details and our team will follow up about enterprise customization, API,
 licensing, or partnerships.
 * Required fields
 About you
 Name * Work email * Title * 
What are you interested in?
 * Enterprise Customization API Licensing Partnerships 
What are you trying to solve for?
 * 
Monthly generation volume
 * Select a range 0-10K images / month 10K-100K images / month 100K-1M images / month 1M+ images / month 
Cancel
 Submit request 
 Request received
 ✓
 Thanks, we received your request.
We will review the details and follow up at your work email.
 Done 
 