Source: https://make-a-video.github.io/
# Make-A-Video: Text-to-Video Generation without Text-Video Data



|  |  |  |  |
| --- | --- | --- | --- |
| Uriel Singer+ | Adam Polyak+ | Thomas Hayes+ | Xi Yin+ |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| Jie An | Songyang Zhang | Qiyuan Hu | Harry Yang | Oron Ashual | Oran Gafni |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | Devi Parikh+ | Sonal Gupta+ | Yaniv Taigman+ |  |

|  |
| --- |
| +Core Contributors |

|  |
| --- |
| Abstract |

|  |
| --- |
| We propose Make-A-Video -- an approach for directly translating the tremendous recent progress in Text-to-Image (T2I) generation to Text-to-Video (T2V). Our intuition is simple: learn what the world looks like and how it is described from paired text-image data, and learn how the world moves from unsupervised video footage. Make-A-Video has three advantages: (1) it accelerates training of the T2V model (it does not need to learn visual and multimodal representations from scratch), (2) it does not require paired text-video data, and (3) the generated videos inherit the vastness (diversity in aesthetic, fantastical depictions, etc.) of today's image generation models. We design a simple yet effective way to build on T2I models with novel and effective spatial-temporal modules. First, we decompose the full temporal U-Net and attention tensors and approximate them in space and time. Second, we design a spatial temporal pipeline to generate high resolution and frame rate videos with a video decoder, interpolation model and two super resolution models that can enable various applications besides T2V. In all aspects, spatial and temporal resolution, faithfulness to text, and quality, Make-A-Video sets the new state-of-the-art in text-to-video generation, as determined by both qualitative and quantitative measures. |

---

# Text-to-Video

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| There is a table by a window with sunlight streaming through illuminating a pile of books. | A blue unicorn flying over a mystical land. | A dog wearing a Superhero outfit with red cape flying through the sky. | Clown fish swimming through the coral reef. | Robot dancing in times square. | A litter of puppies running through the yard. |
|  |  |  |  |  |  |
| A knight riding on a horse through the countryside. | A panda playing on a swing set. | A fluffy baby sloth with a knitted hat trying to figure out a laptop, close up, highly detailed, studio lighting, screen reflecting in its eyes. | A teddy bear painting a portrait. | A young couple walking in a heavy rain. | A bear driving a car. |
|  |  |  |  |  |  |
| A beautiful scenery which leads to a jumpscare. | Sailboat sailing on a sunny day in a mountain lake. | A musk ox grazing on beautiful wildflowers. | Two kangaroos are busy cooking dinner in a kitchen. | A small domesticated carnivorous mammal with soft fur, a short snout, and retractable claws. | A spaceship being pulled into a blackhole. |
|  |  |  |  |  |  |
| An artists brush painting on a canvas close up. | An emoji of a baby panda wearing a red hat, blue gloves, green shirt, and blue pants. | Cat watching tv with a remote in hand. | Horse drinking water. | Humans building a highway on mars. | Hyper-realistic photo of an abandoned industrial site during a storm. |
|  |  |  |  |  |  |
| A ufo hovering over aliens in a field. | A golden retriever eating ice cream on a beautiful tropical beach at sunset. | Monkey learning to play the piano. | Photo of a cat singing in a barbershop quartet. | A ballerina performs a beautiful and difficult dance on the roof of a very tall skyscraper, the city is lit up and glowing behind her. | Unicorns running along a beach. |
|  |  |  |  |  |  |




---

# Video Variations

  
  

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Original Video | Generated Video Variations | | | |
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |




---

# Long Video Generation

  
  

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| a teddy bear on a skateboard in Times Square. | A ballerina performs a beautiful and difficult dance on the roof of a very tall skyscraper, the city is lit up and glowing behind her. | A panda playing on a swing set. | A fluffy baby sloth with a knitted hat trying to figure out a laptop, close up, highly detailed, studio lighting, screen reflecting in its eyes. | A teddy bear painting a portrait. |
|  |  |  |  |  |




---

# Image Animation

  
  

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Original Image |  |  |  |  |
| Animated Video |  |  |  |  |




---

# Image Interpolation

  
  

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| First Image |  |  |  |  |
| Second Image |  |  |  |  |
| Interpolated Video |  |  |  |  |




---

# T2V Generation Comparison

  

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | 4K Illuminated Christmas Tree at Night During Snowstorm | Construction Site Activity | Digital Information | Dramatic ocean sunset | fire |
| Video Diffusion Models |  |  |  |  |  |
| CogVideo |  |  |  |  |  |
| Make-A-Video (Ours) |  |  |  |  |  |
|  | Irrigation Canal in Western USA Water Sourced from the Colorado River 4K Aerial Video | Mountain river | Shinjuku Time Lapse | snowfall in city | Star Time Lapse in Japan |
| Video Diffusion Models |  |  |  |  |  |
| CogVideo |  |  |  |  |  |
| Make-A-Video (Ours) |  |  |  |  |  |




---

# Image Interpolation Comparison

  
  

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| FILM |  |  |  |  |
| Make-A-Video (Ours) |  |  |  |  |
