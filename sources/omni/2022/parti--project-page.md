# Parti: Pathways Autoregressive Text-to-Image Model
Source: https://sites.research.google/parti/
Parti: Pathways Autoregressive Text-to-Image Model




# Parti

# Pathways Autoregressive Text-to-Image Model

![](paper_images_green_watermark_outputs/figures/cherries/art/art_black_red_white.jpg)![](paper_images_green_watermark_outputs/figures/cherries/spaceships/spaceship4.jpg)![](paper_images_green_watermark_outputs/figures/cherries/cherry2/sushi_robot_2.jpg)![](paper_images_green_watermark_outputs/figures/cherries/cities/ink_2_shanghai.jpg)![](paper_images_green_watermark_outputs/figures/cherries/cities/ink_1_manhattan.jpg)![](paper_images_green_watermark_outputs/figures/cherries/charcoal_landmarks/charcoal_pyramid.jpg)![](paper_images_green_watermark_outputs/figures/cherries/teddy_bears/teddy_0.jpg)![](paper_images_green_watermark_outputs/figures/cherries/cherry2/wombat_warrior.jpg)![](paper_images_green_watermark_outputs/figures/cherries/excellent/excellent_wood.jpg)![](paper_images_green_watermark_outputs/figures/cherries/tornado/tiger_cubism.jpg)![](paper_images_green_watermark_outputs/figures/cherries/ai/ai_2.jpg)![](paper_images_green_watermark_outputs/figures/cherries/birds/bird_sing2.jpg)![](paper_images_green_watermark_outputs/figures/cherries/cherry2/mantis_1.jpg)![](paper_images_green_watermark_outputs/figures/cherries/gothic/gothic_0.jpg)![](paper_images_green_watermark_outputs/figures/cherries/cherry2/sloth_kart_1.jpg)

[Research paper](https://arxiv.org/abs/2206.10789)
 
[GitHub repository](https://github.com/google-research/parti)

# Introduction

We introduce the *Pathways Autoregressive Text-to-Image* model (Parti), an autoregressive text-to-image generation model that achieves high-fidelity photorealistic image generation and supports content-rich synthesis involving complex compositions and world knowledge. Recent advances with diffusion models for text-to-image generation, such as Google’s [Imagen](https://imagen.research.google/), have also shown impressive capabilities and state-of-the-art performance on research benchmarks. Parti and Imagen are complementary in exploring two different families of generative models – autoregressive and diffusion, respectively – opening exciting opportunities for combinations of these two powerful models.
  
  
Parti treats text-to-image generation as a sequence-to-sequence modeling problem, analogous to machine translation – this allows it to benefit from advances in large language models, especially capabilities that are unlocked by scaling data and model sizes. In this case, the target outputs are sequences of image tokens instead of text tokens in another language. Parti uses the powerful image tokenizer, [ViT-VQGAN](https://ai.googleblog.com/2022/05/vector-quantized-image-modeling-with.html), to encode images as sequences of discrete tokens, and takes advantage of its ability to reconstruct such image token sequences as high quality, visually diverse images.
  
  
We observed the following results:

* Consistent quality improvements by scaling Parti’s encoder-decoder up to 20 billion parameters.
* State-of-the-art zero-shot FID score of 7.23 and finetuned FID score of 3.22 on MS-COCO.
* Effectiveness across a wide variety of categories and difficulty aspects in our analysis on Localized Narratives and PartiPrompts, our new holistic benchmark of 1600+ English prompts that we release as part of this work.

  
We also explore and highlight limitations of our models, giving key example areas of focus for further improvements.
  
  
![](assets/parti_overview.jpg)

# Scaling from 350M to 20B parameters

Parti is implemented in [Lingvo](https://github.com/tensorflow/lingvo) and scaled with [GSPMD](https://ai.googleblog.com/2021/12/general-and-scalable-parallelization.html) on [TPU v4](https://cloud.google.com/blog/topics/tpus/google-showcases-cloud-tpu-v4-pods-for-large-model-training) hardware for both training and inference, which allowed us to train a 20B parameter model that achieves record performance on multiple benchmarks.
  
  
We perform detailed comparisons of four scales of Parti models – 350M, 750M, 3B and 20B – and observe:

* Consistent and substantial improvements in model capabilities and output image quality.
* When comparing the 3B and 20B models, human evaluators preferred the latter most of the time, specifically:

+ 63.2% for image realism/quality
+ 75.9% for image-text match

* The 20B model especially excels at prompts that are abstract, require world knowledge, specific perspectives, or writing and symbol rendering.

  
Click on one of the following prompts to compare Parti models across scales:
  
  

A portrait photo of a kangaroo wearing an orange hoodie and blue sunglasses standing on the grass in front of the Sydney Opera House holding a sign on the chest that says Welcome Friends!
  

A green sign that says "Very Deep Learning" and is at the edge of the Grand Canyon. Puffy white clouds are in the sky.
  

A photo of an astronaut riding a horse in the forest. There is a river in front of them with water lilies.
  

A map of the United States made out of sushi. It is on a table next to a glass of red wine.
  

A squirrel gives an apple to a bird
  

The back of a violin
  

Infinity

# 350M

![](paper_images_green_watermark_outputs/figures/scaling_comparison/kangaroo_0.jpg)

# 750M

![](paper_images_green_watermark_outputs/figures/scaling_comparison/kangaroo_1.jpg)

# 3B

![](paper_images_green_watermark_outputs/figures/scaling_comparison/kangaroo_2.jpg)

# 20B

![](paper_images_green_watermark_outputs/figures/scaling_comparison/kangaroo_3.jpg)

# Composing real-world knowledge

Text-to-image generation is most interesting when it allows us to create scenes that have never been seen.
  
  
We find that Parti can manage long, complex prompts that require it to:

* Accurately reflect world knowledge
* Compose many participants and objects, with fine-grained details and interactions
* Adhere to a specific image format and style

  
In the following examples of prompts and output images, we show how Parti responds to changes in participants, activities, descriptions, locations, and format.

![](paper_images_green_watermark_outputs/figures/cherries/raccoons/hokusai.jpg)

A raccoon wearing formal clothes, wearing a tophap and holding a cane.
The raccoon is holding a garbage bag. Oil painting in the style of
Rembrandt
Vincent Van Gogh
Hokusai
pixel art
abstract cubism
Egyptian tomb heiroglyphics

![](paper_images_green_watermark_outputs/figures/cherries/tigers/tiger3.jpg)

Portrait of a tiger wearing a train conductor’s hat and holding a skateboard that has a yin-yang symbol on it.
photograph
comic book illustration
oil painting
marble statue
charcoal sketch
woodcut
child’s crayon drawing
color ink-and-wash drawing
Chinese ink and wash painting

![](paper_images_green_watermark_outputs/figures/cherries/teddy_bears/teddy_1.jpg)

A teddy bear wearing a motorcycle helmet and cape is
standing in front of Loch Awe with Kilchurn Castle behind him
driving a speed boat near the Golden Gate Bridge
car surfing on a taxi cab in New York City
riding a motorcycle in Rio de Janeiro with Dois Irmãos in the background. dslr photo.

![](paper_images_green_watermark_outputs/figures/cherries/water/water_crocodile.jpg)

A photo of a
maple leaf
palm tree
four-leaf clover
lotus flower
panda
teddy bear
crocodile
dragonfly
made of water.

![](paper_images_green_watermark_outputs/figures/cherries/cherry2/pangolin_basketball.jpg)

A photo of an Athenian vase with a painting of
pandas
toucans
pangolins
playing
tennis
soccer
basketball
in the style of Egyptian hieroglyphics.

![](paper_images_green_watermark_outputs/figures/cherries/tornado/tiger_cubism.jpg)

A tornado made of
sharks
tigers
bees
crashing into a skyscraper. Painting in thestyle of
Hokusai
abstract cubism
watercolor

# PartiPrompts benchmark

PartiPrompts (P2) is a rich set of over 1600 prompts in English that [we release as part of this work](https://github.com/google-research/parti). P2 can be used to measure model capabilities across various categories and challenge aspects.
  
  
![](assets/bcp.png)
  
  
P2 prompts can be simple, allowing us to gauge the progress from scaling.
They can also be complex, such as the following 67-word description we created for Vincent van Gogh’s *The Starry Night* (1889):

Oil-on-canvas painting of a blue night sky with roiling energy. A fuzzy and bright yellow crescent moon shining at the top. Below the exploding yellow stars and radiating swirls of blue, a distant village sits quietly on the right. Connecting earth and sky is a flame-like cypress tree with curling and swaying branches on the left. A church spire rises as a beacon over rolling blue hills.

![](paper_images_green_watermark_outputs/teaser_images/starry_night/11.jpg)

![](paper_images_green_watermark_outputs/teaser_images/starry_night/20.jpg)

![](paper_images_green_watermark_outputs/teaser_images/starry_night/28.jpg)

![](paper_images_green_watermark_outputs/teaser_images/starry_night/34.jpg)

# Discussion and limitations

Many of the images shown here have been selected, or cherry-picked, from a large set of examples generated during prompt exploration and modification interactions. We call this process “Growing The Cherry Tree'' and provide a detailed example of it in [the paper](https://arxiv.org/abs/2206.10789), where we build a very complex prompt and strategies to produce an image that fully reflects the description.
  
  
While Parti produces high quality outputs for a broad range of prompts, the model nevertheless has many limitations. In the paper, we discuss these challenges with examples, current failure modes, and opportunities for future work. We provide a sample of some of these failure cases in the interactive visualization below.

![](paper_images_green_watermark_outputs/figures/limitations/banana_juice/banana_juice_1.jpg)

Failure: improper handling of negation or indication of absence.

Two baseballs to the left of three tennis balls.
  

A rhino beetle this size of a tank grapples a real life passenger airplane on the tarmac.
  

A portrait of a statue of Anubis with a crown and wearing a yellow t-shirt that has a space shuttle drawn on it. A white brick wall is in the background.
  

A cream colored labradoodle next to a white cat with black-tipped ears.
  

A plate that has no bananas on it. there is a glass without orange juice next to it.
  

A robot painted as graffiti on a brick wall. The words "Fly an airplane" are written on the wall. A sidewalk is in front of the wall, and grass is growing out of cracks in the concrete.
  

A shiny robot wearing a race car suit and black visor stands proudly in front of an F1 race car. The sun is setting on a cityscape in the background. comic book illustration.

# Responsibility and broader impact

As we discuss at greater length in the paper, text-to-image models introduce many opportunities and risks, with potential impact on bias and safety, visual communication, disinformation, and creativity and art. Similar to
[Imagen](https://imagen.research.google/),
we recognize there is a risk that Parti may encode harmful stereotypes and representations. Some potential risks relate to the way in which the models are themselves developed, and this is especially true for the training data. Current models like Parti are trained on large, often noisy, image-text datasets that are known to contain biases regarding people of different backgrounds. This leads such models, including Parti, to produce stereotypical representations of, for example, people described as lawyers, flight attendants, homemakers, and so on, and to reflect Western biases for events such as weddings. This presents particular problems for people whose backgrounds and interests are not well represented in the data and the model, especially if such models are applied to uses such as visual communication, e.g. to help low-literacy social groups. Models which produce photorealistic outputs, especially of people, pose additional risks and concerns around the creation of deepfakes. This creates risks with respect to the possible propagation of visually-oriented misinformation, and for individuals and entities whose likenesses are included or referenced.
  
  
Text-to-image models open up many new possibilities for people to create unique and aesthetically pleasing images – essentially, acting as a paint brush to enhance human creativity and productivity. However, in assessing design or artistic merit, it is important to have
[a nuanced understanding of algorithmically based art](https://direct.mit.edu/leon/article-abstract/55/2/130/102695/Who-or-What-Is-an-AI-Artist?redirectedFrom=fulltext)
over the years, the model itself, the people involved and the broader artistic milieu. Bias also matters here, as the range of outputs from a model is dependent on the training data, and this may have biases toward Western imagery and further prevent models from exhibiting radically new artistic styles – the way human artists can.
  
  
For these reasons, we have decided not to release our Parti models, code, or data for public use without further safeguards in place. In the meantime, we provide a Parti watermark on all images that we release. We will focus on following this work with further careful model bias measurement and mitigation strategies, such as prompt filtering, output filtering, and model recalibration. We believe it may be possible to use text-to-image generation models to understand biases in large image-text datasets at scale, by explicitly probing them for a suite of known bias types, and potentially uncovering other forms of hidden bias. We also plan to coordinate with artists to adapt high-performing text-to-image generation models’ capabilities to their work. This is especially important given the intense interest among many research groups, and the rapid development of models and data to train them. Ideally, we hope these models will augment human creativity and productivity, not replace it, so that we can all enjoy a world filled with new, varied, and responsible aesthetic visual experiences.
  

  
  
[Data card](https://github.com/google-research/parti/tree/main/data_cards)
 

# Acknowledgements

Parti is a collaboration that spans authors across multiple [Google Research](https://research.google/) teams:
  
  
Jiahui Yu\*,
Yuanzhong Xu†,
Jing Yu Koh†,
Thang Luong†,
Gunjan Baid†,
Zirui Wang†,
Vijay Vasudevan†,
Alexander Ku†
  
Yinfei Yang,
Burcu Karagol Ayan,
Ben Hutchinson,
Wei Han,
Zarana Parekh,
Xin Li,
Han Zhang
  
Jason Baldridge†,
Yonghui Wu\*
  
  
\*Equal contribution
 
†Core contribution
  
  
We would like to thank Elizabeth Adkison, Fred Alcober, Tania Bedrax-Weiss, Krishna Bharat, Nicole Brichtova, Yuan Cao, William Chan, Zhifeng Chen, Eli Collins, Claire Cui, Andrew Dai, Jeff Dean, Emily Denton, Toju Duke, Dumitru Erhan, Brian Gabriel, Zoubin Ghahramani, Jonathan Ho, Michael Jones, Sarah Laszlo, Quoc Le, Lala Li, Zhen Li, Sara Mahdavi, Kathy Meier-Hellstern, Kevin Murphy, Paul Natsev, Paul Nicholas, Mohammad Norouzi, Niki Parmar, Ruoming Pang, Fernando Pereira, Slav Petrov, Vinodkumar Prabhakaran, Utsav Prabhu, Evan Rapoport, Keran Rong, Negar Rostamzadeh, Chitwan Saharia, Gia Soles, Austin Tarango, Ashish Vaswani, Tao Wang, Tris Warkentin, Austin Waters, Ben Zevenbergen for helpful discussions and guidance, Peter Anderson, Corinna Cortes, Tom Duerig, Douglas Eck, David Ha, Radu Soricut and Rahul Sukthankar for paper review and feedback, Erica Moreira and Victor Gomes for help with resource coordination, Tom Small for designing the Parti watermark, Google ML Data Operations team for collecting human evaluations on our generated images and others in the Google Brain team and Google Research team for support throughout this project.
  
  
We would also like to give particular acknowledgments to the Imagen team, especially Mohammad Norouzi, Chitwan Saharia, Jonathan Ho and William Chan, for sharing their near complete results prior to releasing Imagen; their findings on the importance of CF guidance were particularly helpful for the final Parti model. We also thank the Make-a-Scene team, especially Oran Gafni, for helpful discussion on CF-guidance implementation in autoregressive models. We thank the DALL-E 2 authors, especially Aditya Ramesh, for helpful discussion on MS-COCO evaluation. We also thank the DALL-Eval authors, especially Jaemin Cho, for help with reproducing their numbers.

# Gallery
