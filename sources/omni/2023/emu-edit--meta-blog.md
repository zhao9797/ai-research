# Emu Video and Emu Edit: Our latest generative AI research milestones
Source: https://ai.meta.com/blog/emu-text-to-video-generation-image-editing-research/
Emu Video and Emu Edit: Our latest generative AI research milestones

[![Meta](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=CU4NmdgzVowQ7kNvwFOqFBr&_nc_oc=AdrlzoHU4S2VE0iNbEGHdgwUhLSLLJmHUS0YhCa5hzM3gxqArwdNGIPeJlyzBHNlpkHW5AFpln4bb1RTcTIBrX8Z&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9ZkzPevFzhrXmwDHGKUSFUOOLeFhrogPby5hg4hG1Niw&oe=6A4269B9)](/)

* [Products](#)
* [AI Research](#)
* [Resources](#)
* [About](#)
* [Get Llama](https://www.llama.com/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=09252025_moment)

* [Try Meta AI](https://applink.meta.ai/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=04082026_moment)

[BACK](# "Go up one level")

* [Meta AI](/meta-ai/)
* [Vibes](/vibes/)
* [AI Studio](/ai-studio/)

* [Overview](/research/)
* [Projects](/research/#projects)
* [Research Areas](/research/#research-areas)
* [People](/results/?content_types[0]=person)

* [Blog](/blog/)
* [Learning Hub](/learn/)
* [Demos](https://aidemos.meta.com/)

* [Overview](/about/)
* [Open Source](/opensourceai/)
* [Careers](https://www.metacareers.com/)

Clear

* Clear
* [Products

  >](#)
* [AI Research

  >](#)
* [Resources

  >](#)
* [About

  >](#)
* [Get Llama](https://www.llama.com/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=09252025_moment)

[Try Meta AI](https://applink.meta.ai/?utm_source=ai_meta_site&utm_medium=web&utm_content=AI_nav&utm_campaign=04082026_moment)

FEATURED

Generative AI

# Introducing Emu Video and Emu Edit, our latest generative AI research milestones

November 16, 2023

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t15.5256-10/377225088_884902269510689_3538521281340472487_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=861778&_nc_ohc=lB7KsWlplCAQ7kNvwFvfqhx&_nc_oc=AdpY1OAmCRV2Gs3BwUHBZ2Z17uqMeyGIgqDSgiaPQovT_1etOUw3MhTcdod5xRFLmxXZ8kJe4Ps6nso6QxIL7Eyi&_nc_zt=23&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8D9mwP7T3HSxkQAFtVvimJg-JMrbThukhxc0hs5M0r7g&oe=6A4237BC)](https://video-lax7-1.xx.fbcdn.net/o1/v/t2/f2/m412/AQMUxEtX0wzahNNUR3PtvsZ18DRbJVFXi2wmK6zXZZyZYbpKZJ3FzkWoiyBLc0LxlRmTbwBmleYo-THKjc2nI_E.mp4?_nc_cat=105&_nc_sid=8bf8fe&_nc_ht=video-lax7-1.xx.fbcdn.net&_nc_ohc=HVCiIHQhz-AQ7kNvwF5CZvY&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMzYwLnN2ZV9zZCIsInhwdl9hc3NldF9pZCI6ODkxOTMyMDA1NTk4Njg5LCJhc3NldF9hZ2VfZGF5cyI6OTUyLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6NCwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=17-1&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&_nc_zt=28&oh=00_Af-4EnWof__Kg9FtIV0MLwn2ZucsE1yZ0iZJbRjYRjGr4A&oe=6A425429&bitrate=268734&tag=sve_sd)

The field of generative AI is rapidly evolving, showing remarkable potential to augment human creativity and self-expression. In 2022, we made the leap from [image generation](https://ai.meta.com/blog/greater-creative-control-for-ai-image-generation/) to [video generation](https://ai.meta.com/blog/generative-ai-text-to-video/) in the span of a few months. And at this year’s Meta Connect, we announced several [new developments](https://about.fb.com/news/2023/09/introducing-ai-powered-assistants-characters-and-creative-tools/), including [Emu](https://ai.meta.com/research/publications/emu-enhancing-image-generation-models-using-photogenic-needles-in-a-haystack/), our first foundational model for image generation. Technology from Emu underpins many of our generative AI experiences, some AI image editing tools for Instagram that let you take a photo and change its visual style or background, and the Imagine feature within Meta AI that lets you generate photorealistic images directly in messages with that assistant or in group chats across our family of apps. Our work in this exciting field is ongoing, and today, we’re announcing new research into controlled image editing based solely on text instructions and a method for text-to-video generation based on diffusion models.

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t15.5256-10/368679422_3783093788609735_4967713998462029713_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=861778&_nc_ohc=ouWrPybG83QQ7kNvwFfdTG1&_nc_oc=Adq1cLrwCbhCI-Wpv4vjJ6mXTjX4aGoXpXfKM-qOn1NxAp4A1MvNO9-6N16v0L1TOJw28I3FLCjoDR_kP_5po41M&_nc_zt=23&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8Gl0KXMhPAOS6x0yqGRpf39l_SLuYloGdMbfWt3tseDg&oe=6A4258E8)](https://video-lax3-2.xx.fbcdn.net/o1/v/t2/f2/m266/AQOVXGvLG56yAqd2JrrQh5ChWe29LXBX1zXkVb8TVuF5TWSJWuvF5JjuMLzpym0_izexuf1G_w2GBCgSU3nyTqQEZ-shKCgrnow.mp4?strext=1&_nc_cat=100&_nc_sid=8bf8fe&_nc_ht=video-lax3-2.xx.fbcdn.net&_nc_ohc=31Hzaqh_e2oQ7kNvwH4IPt_&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMTA3NC5jb21wcmVzc2VkX3NvdXJjZSIsInhwdl9hc3NldF9pZCI6MzI3NjQ0MTgzMzA5NjQ1LCJhc3NldF9hZ2VfZGF5cyI6OTUyLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6MzMsInVybGdlbl9zb3VyY2UiOiJ3d3cifQ%3D%3D&ccb=17-1&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&_nc_zt=28&oh=00_Af9JEz0FYgbJh0kqtwC_YHpUxsnRVXJM-KDxRJZhEc1pPw&oe=6A3E432A&bitrate=1706015&tag=compressed_source)

## Emu Video: A simple factorized method for high-quality video generation

Whether or not you’ve personally used an AI image generation tool, you’ve likely seen the results: Visually distinct, often highly stylized and detailed, these images on their own can be quite striking—and the impact increases when you bring them to life by adding movement.

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t15.5256-10/400420062_844321670820404_3281034371545073355_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=861778&_nc_ohc=9_b7Va41dQ8Q7kNvwGqoskZ&_nc_oc=Adq0_qhhyJha6aAGyfTsZpE1Ix3BvAozxy39LoV1aO__Vcz04VqgZ_nB3mpt8DIwp9JasJlEaOD1TFh-uO62D07k&_nc_zt=23&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9O1kdWtwkuQ1aKAiU8i4iXsFOBu_gKKakP7DPhOwHgjw&oe=6A424F5D)](https://video-lax3-1.xx.fbcdn.net/o1/v/t2/f2/m412/AQNUjnxZeHLQg8eoOvdBpQ5M1QeaA2dL8C6BSrvNCmVxp3b4WM25dswWcYM-qcaWs7kdxoT-jWKCYQA9KWx1AEU.mp4?_nc_cat=104&_nc_sid=8bf8fe&_nc_ht=video-lax3-1.xx.fbcdn.net&_nc_ohc=1VmyiYg8viEQ7kNvwGeTkFP&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMzYwLnN2ZV9zZCIsInhwdl9hc3NldF9pZCI6MjQxMDM2NjAyMzI3MzI4LCJhc3NldF9hZ2VfZGF5cyI6OTUyLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6ODksInVybGdlbl9zb3VyY2UiOiJ3d3cifQ%3D%3D&ccb=17-1&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&_nc_zt=28&oh=00_Af8XUnKdHtB2sOS5cas7sunYnqbEXTRhOGnCTfftvZgWKg&oe=6A4249DE&bitrate=444833&tag=sve_sd)

With Emu Video, which leverages our Emu model, we present a simple method for text-to-video generation based on diffusion models. This is a unified architecture for video generation tasks that can respond to a variety of inputs: text only, image only, and both text and image. We’ve split the process into two steps: first, generating images conditioned on a text prompt, and then generating video conditioned on both the text and the generated image. This “factorized” or split approach to video generation lets us train video generation models efficiently. We show that factorized video generation can be implemented via a single diffusion model. We present critical design decisions, like adjusting noise schedules for video diffusion, and multi-stage training that allows us to directly generate higher-resolution videos.

[![](https://scontent-lax7-1.xx.fbcdn.net/v/t15.5256-10/400792118_1326755734877763_814421523400089495_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=861778&_nc_ohc=K6U903AnVmEQ7kNvwF4homb&_nc_oc=AdrxZ4RVQtroU3UAOWz-LVcYyr2eaGVvZoHkh5RF-ct4UqZ_IpxI0WLGgy3FbfNenJiKAfGSbO2-jXjtcCusGV-A&_nc_zt=23&_nc_ht=scontent-lax7-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af-BPD6xaJz6_VP3Nv2N071aj-kMe5KN1VDxMw5Y5EYCEQ&oe=6A4254C5)](https://video-lax3-2.xx.fbcdn.net/o1/v/t2/f2/m266/AQO3o9O9452EMoAL8meXDvgCHWgWVuzf5fFPqR1Oc0O-fkqLw5B4dN_P0Yd3L6pEg92dIJfmnn9PMYsVcjr7Gcn2OTzE68NS-8Y.mp4?strext=1&_nc_cat=106&_nc_sid=8bf8fe&_nc_ht=video-lax3-2.xx.fbcdn.net&_nc_ohc=_HG86t-1dmkQ7kNvwHXoGNb&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuNTEyLmNvbXByZXNzZWRfc291cmNlIiwieHB2X2Fzc2V0X2lkIjoxNDEyMDQ1NDYzMDYwNzcwLCJhc3NldF9hZ2VfZGF5cyI6OTUyLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6NCwidXJsZ2VuX3NvdXJjZSI6Ind3dyJ9&ccb=17-1&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&_nc_zt=28&oh=00_Af-Eu0X49v3vwIn4DgoecAW0dLuL-aRky1sQduwplL2JeA&oe=6A3E5568&bitrate=743073&tag=compressed_source)

Unlike prior work that requires a deep cascade of models (e.g., five models for [Make-A-Video](https://ai.meta.com/blog/generative-ai-text-to-video/)), our state-of-the-art approach is simple to implement and uses just two diffusion models to generate 512x512 four-second long videos at 16 frames per second. In human evaluations, our video generations are strongly preferred compared to prior work—in fact, this model was preferred over Make-A-Video by 96% of respondents based on quality and by 85% of respondents based on faithfulness to the text prompt. Finally, the same model can “animate” user-provided images based on a text prompt where it once again sets a new state-of-the-art outperforming prior work by a significant margin.

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/400716824_1091119852252102_4469709282943793457_n.png?_nc_cat=106&ccb=1-7&_nc_sid=e280be&_nc_ohc=WuoJXO-zsMcQ7kNvwFopvIL&_nc_oc=AdoiRgrXwuR6lQfp677hbdOjVJrUQmuNxX0LvNSlOaN9ZEnBM4pS6yE3wyehTVfvQogVDANDYHqgLZRzh8I7dLiM&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_YBFmaLXLdkcvuk6dSYgFvzJFBBJsTJynYVwEhMyKC6Q&oe=6A56BAC0)

## Emu Edit: Precise image editing via recognition and generation tasks

Of course, the use of generative AI is often a process. You try a prompt, the generated image isn’t *quite* what you had in mind, so you continue tweaking the prompt until you get to a more desired outcome. That’s why prompt engineering has become a thing. And while instructable image generative models have made significant strides in recent years, they still face limitations when it comes to offering precise control. That’s why we’re introducing Emu Edit, a novel approach that aims to streamline various image manipulation tasks and bring enhanced capabilities and precision to image editing.

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t15.5256-10/365341526_1582489445623131_1595448740127151562_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=861778&_nc_ohc=ya2deArBnekQ7kNvwHqsTl_&_nc_oc=Adoy6cz3sz2Sl16xYie2EOlpC1rzWHwRBHSdbfTBETzPQsXh7sAXJor46p-hT7lrlyv6lGV0faWaECqw26A9qrDo&_nc_zt=23&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af-Eov1yRfvjuAq-Q0YoH2xB5OO3sLFJpqx84Tr3SlZcFQ&oe=6A426B22)](https://video-lax3-2.xx.fbcdn.net/o1/v/t2/f2/m412/AQPxhX-a1qjoGYxx6-EJGwUKC1u5FaRfxaLaYNtb0vPd9V9EvIYEpJZV2PMF67C18JUuiXitL_SxchYy-1g4Gp8.mp4?_nc_cat=111&_nc_sid=8bf8fe&_nc_ht=video-lax3-2.xx.fbcdn.net&_nc_ohc=Dix2GAb34rYQ7kNvwHebvf1&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMzYwLnN2ZV9zZCIsInhwdl9hc3NldF9pZCI6ODY1MTUwNzg1MjY2MDc1LCJhc3NldF9hZ2VfZGF5cyI6OTUyLCJ2aV91c2VjYXNlX2lkIjoxMDEyOCwiZHVyYXRpb25fcyI6MzksInVybGdlbl9zb3VyY2UiOiJ3d3cifQ%3D%3D&ccb=17-1&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&_nc_zt=28&oh=00_Af_7fl2rzbuIXVNsj6t1sNGY7zaC_U39XrQB0Q9j1ATUuw&oe=6A42429B&bitrate=96179&tag=sve_sd)

Emu Edit is capable of free-form editing through instructions, encompassing tasks such as local and global editing, removing and adding a background, color and geometry transformations, detection and segmentation, and more. Current methods often lean towards either over-modifying or under-performing on various editing tasks. We argue that the primary objective shouldn’t just be about producing a “believable” image. Instead, the model should focus on precisely altering only the pixels relevant to the edit request. Unlike many generative AI models today, Emu Edit precisely follows instructions, ensuring that pixels in the input image unrelated to the instructions remain untouched. For instance, when adding the text “Aloha!” to a baseball cap, the cap itself should remain unchanged.

[![](https://scontent-lax7-1.xx.fbcdn.net/v/t15.5256-10/400570519_183943941379590_2194861706686804933_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=861778&_nc_ohc=7jw1A83y4ZAQ7kNvwGEQcL5&_nc_oc=AdoL-p1G8sNUxuTbDnMSQ0HujXV4cMGnaBBdcZ74HtAi7Ih16OqzUF-IIoJC9QAgcbLfhEQ7ZxXXSAzOt5vpu8t_&_nc_zt=23&_nc_ht=scontent-lax7-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af-zH98S245TRyI9bB-b1YkoZcS5UWOGVQMMCM3RnyrVXA&oe=6A42638D)](https://video-lax3-2.xx.fbcdn.net/o1/v/t2/f2/m412/AQP7fuKLFFcuNBRMtqcBm_TF4yKNNFZocqtxivqGlktjnTkgFZGreonqehB-c2RroAiN4vl2BWmj7sVpT3qODodS.mp4?_nc_cat=100&_nc_sid=8bf8fe&_nc_ht=video-lax3-2.xx.fbcdn.net&_nc_ohc=d-bEmO8YEvIQ7kNvwGVCD7n&efg=eyJ2ZW5jb2RlX3RhZyI6Inhwdl9wcm9ncmVzc2l2ZS5GQUNFQk9PSy4uQzMuMzYwLnN2ZV9zZCIsInhwdl9hc3NldF9pZCI6MjY3OTM1NDI3NTU2MDY3NSwiYXNzZXRfYWdlX2RheXMiOjk1MiwidmlfdXNlY2FzZV9pZCI6MTAxMjgsImR1cmF0aW9uX3MiOjM5LCJ1cmxnZW5fc291cmNlIjoid3d3In0%3D&ccb=17-1&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&_nc_zt=28&oh=00_Af_QVOSak_6x4oB0QDySsPqWrRHiWKVDnLAbooF5ZYMMHw&oe=6A426755&bitrate=100641&tag=sve_sd)

Our key insight is that incorporating computer vision tasks as instructions to image generation models offers unprecedented control in image generation and editing. Through a detailed examination of both local and global editing tasks, we highlight the vast potential of Emu Edit in executing detailed edit instructions.

In order to train the model, we’ve developed a dataset that contains 10 million synthesized samples, each including an input image, a description of the task to be performed, and the targeted output image. We believe it’s the largest dataset of its kind to date. As a result, our model displays unprecedented edit results in terms of both instruction faithfulness and image quality. In our evaluations, Emu Edit demonstrates superior performance over current methods, producing new state-of-the-art results in both qualitative and quantitative evaluations for a range of image editing tasks.

## The road ahead

Although this work is purely fundamental research right now, the potential use cases are clearly evident. Imagine generating your own animated stickers or clever GIFs on the fly to send in the group chat rather than having to search for the perfect media for your reply. Or editing your own photos and images, no technical skills required. Or adding some extra oomph to your Instagram posts by animating static photos. Or generating something entirely new.

While certainly no replacement for professional artists and animators, Emu Video, Emu Edit, and new technologies like them could help people express themselves in new ways—from an art director ideating on a new concept or a creator livening up their latest reel to a best friend sharing a unique birthday greeting. And we think that’s something worth celebrating.

[Get the Emu Video paper](https://emu-video.metademolab.com/assets/emu_video.pdf)  
  
[Visit the Emu Video project web page](https://emu-video.metademolab.com/)  
  
[Get the Emu Edit paper](https://emu-edit.metademolab.com/assets/emu_edit.pdf)  
  
[Visit the Emu Edit project web page](https://emu-edit.metademolab.com/)

---

Share:

---

Our latest updates delivered to your inbox

[Subscribe](https://ai.facebook.com/subscribe/) to our newsletter to keep up with Meta AI news, events, research breakthroughs, and more.

Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.2365-6/338318848_238475658638014_6444534044370711549_n.gif?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=KRuNE6RViuYQ7kNvwG-Y1l5&_nc_oc=AdoVTlLGkYsRRlF2sF5qMh44OnGR9jWDw4BFpl8SE4t1sKA0ybvKa0hnQmnZM26fX1fZM1dbOJsDBQ5wKKfOY3Tw&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_Auwv3oszJty1Cn0zMpuJ_VpC0ua4T2tY2E4iu1ZBCRw&oe=6A56A8E9)

Computer Vision

Introducing Segment Anything: Working toward the first foundation model for image segmentation

April 5, 2023

[Read post](https://ai.meta.com/blog/segment-anything-foundation-model-image-segmentation/)

FEATURED

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/284099254_760295688673506_1047420741523524710_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=JriodrSCKZ4Q7kNvwGagGvN&_nc_oc=Adpc12x7Kx1a3IMLp0wtVCeMsy6eslPiMtssklowL-wRuZEwInZ-xmQwolekLtFPLEiXc0MgRh-1rnmy8b9Crs9z&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9OFsdWAyWJOzEZTVP9VGrrfjjk5QbOdZl5NplOXANIiQ&oe=6A56B576)

Research

MultiRay: Optimizing efficiency for large-scale AI models

November 18, 2022

[Read post](https://ai.meta.com/blog/multiray-large-scale-AI-models/)

FEATURED

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/334793505_583125787173687_542838236294006040_n.png?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=oWyjW334zesQ7kNvwFnnqj2&_nc_oc=AdoSvcnWu95Hr1zaMgk_eBNVAjkYChYYttaEZ7NVS6Tucy4LeWCkAR8OprbxAp9Y4sYurAi6tNh9qzuFl_Y4KnyS&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_oKv5mDB3tVnxGfKgXlg6RyOs-92w1-c38SzRSScLn2g&oe=6A56C904)

ML Applications

MuAViC: The first audio-video speech translation benchmark

March 8, 2023

[Read post](https://ai.meta.com/blog/muavic-audio-visual-speech-translation-benchmark/)

[Our approach](/about)

[About AI at Meta](/about)

[People](/results/?content_types%5B0%5D=person&sort_by=random)

[Careers](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams[0]=Artificial%20Intelligence&is_in_page=0)

[Research](/research)

[Infrastructure](/infrastructure)

[Resources](/resources)

[Demos](https://aidemos.meta.com/)

[Meta AI](/meta-ai/)

[Explore Meta AI](/meta-ai/)

[Get Meta AI](/get-meta-ai/)

[AI Studio](/ai-studio/)

[Latest news](/blog)

[Blog](/blog)

[Newsletter](/subscribe)

Foundational models

[Llama](https://www.llama.com/)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=mOIsi79ov-MQ7kNvwGbYk5i&_nc_oc=Adrea_xK043rSFRMGNJOLshWyMTm-eSZiAONswolCTIQQYyPzNKYEhdeTLjyP730sk44vAGa2wQcH3dSXG1k8frn&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af-PeFarMnWUmfiYbV6a8amrzQdzPYxASQGN1lkVbunZ7A&oe=6A56D378)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=ghJpI4Q0-7UQ7kNvwERLh2m&_nc_oc=AdraEHj9S1X9jmSN7luBzLiDlA4GA9o_0oLBcacyt96UAhyj0W2L3PZ3Sdk9yI9XGq-JDgj7UblPu19ZzpMBf0z7&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9h0DpG8YA_BDbk9N3xH1JtTmaCurq_uZxGdNZ_i5HFiA&oe=6A56D84F)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_PQ56bplGbEoncVPkb1YJvZNWwzwYNsVx6nr0wmBJWYQ&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_PQ56bplGbEoncVPkb1YJvZNWwzwYNsVx6nr0wmBJWYQ&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_zf7Ljn1owEqcV8pZyWMDRzugNp8La8M1pgA78_3-09w&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_zf7Ljn1owEqcV8pZyWMDRzugNp8La8M1pgA78_3-09w&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8zfPXTEWsoxAYLNyh4FfBFy343Z_NXo9JR0c8HHAdRmw&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8zfPXTEWsoxAYLNyh4FfBFy343Z_NXo9JR0c8HHAdRmw&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9hHbTNoxQcp_PTpWokknUzGpJvNUmgVQSFdtOnM7L8wA&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9hHbTNoxQcp_PTpWokknUzGpJvNUmgVQSFdtOnM7L8wA&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

Our approach

[Our approach](/about)[About AI at Meta](/about)[People](/results/?content_types%5B0%5D=person&sort_by=random)[Careers](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams[0]=Artificial%20Intelligence&is_in_page=0)

Research

[Research](/research)[Infrastructure](/infrastructure)[Resources](/resources)[Demos](https://aidemos.meta.com/)

Meta AI

[Meta AI](/meta-ai/)[Explore Meta AI](/meta-ai/)[Get Meta AI](/get-meta-ai/)[AI Studio](/ai-studio/)

Latest news

[Latest news](/blog)[Blog](/blog)[Newsletter](/subscribe)

Foundational models

[Llama](https://www.llama.com/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_PQ56bplGbEoncVPkb1YJvZNWwzwYNsVx6nr0wmBJWYQ&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_PQ56bplGbEoncVPkb1YJvZNWwzwYNsVx6nr0wmBJWYQ&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_zf7Ljn1owEqcV8pZyWMDRzugNp8La8M1pgA78_3-09w&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_zf7Ljn1owEqcV8pZyWMDRzugNp8La8M1pgA78_3-09w&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8zfPXTEWsoxAYLNyh4FfBFy343Z_NXo9JR0c8HHAdRmw&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8zfPXTEWsoxAYLNyh4FfBFy343Z_NXo9JR0c8HHAdRmw&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9hHbTNoxQcp_PTpWokknUzGpJvNUmgVQSFdtOnM7L8wA&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9hHbTNoxQcp_PTpWokknUzGpJvNUmgVQSFdtOnM7L8wA&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)

[Privacy Policy](https://www.facebook.com/about/privacy/)

[Terms](https://www.facebook.com/policies/)

[Cookies](https://www.facebook.com/policies/cookies/)

Meta © 2026

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_PQ56bplGbEoncVPkb1YJvZNWwzwYNsVx6nr0wmBJWYQ&oe=6A4259E7)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=YSpvsdFqrfAQ7kNvwETuOOT&_nc_oc=Adp2DB1EB6yHQ1CuMPemHxv-27dtJo23K_l_n8dGXDJjZbBCQEsDZe3DddBp1h7z9lfCTljJ_P2tr5MO77z9Oh1U&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_PQ56bplGbEoncVPkb1YJvZNWwzwYNsVx6nr0wmBJWYQ&oe=6A4259E7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_zf7Ljn1owEqcV8pZyWMDRzugNp8La8M1pgA78_3-09w&oe=6A425222)

![](https://scontent-lax3-2.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Clxn6BB6KB0Q7kNvwE5lTm1&_nc_oc=AdoFbpLp3tfZ3lhv-E1I5E1JAHU2HwtDumSaNGWAQlBBRL2hWwYRXtiugDQQr8mZCRyAyluKWyXp_9epiyOxteNb&_nc_zt=14&_nc_ht=scontent-lax3-2.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af_zf7Ljn1owEqcV8pZyWMDRzugNp8La8M1pgA78_3-09w&oe=6A425222)](https://twitter.com/aiatmeta/)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8zfPXTEWsoxAYLNyh4FfBFy343Z_NXo9JR0c8HHAdRmw&oe=6A4245BB)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/336289415_1541032296405649_2165099305308791297_n.svg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=XamjHPNRa3IQ7kNvwEssEFu&_nc_oc=AdqvSK2WiyIP3cv3QIOV4dY89CF0WbSeSTB3VFC4F1FMqjapUBYIK2O8thT69l1hBfFAd-A4Z4RbrDSTE68OS8fN&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af8zfPXTEWsoxAYLNyh4FfBFy343Z_NXo9JR0c8HHAdRmw&oe=6A4245BB)](https://www.linkedin.com/showcase/aiatmeta)

[![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9hHbTNoxQcp_PTpWokknUzGpJvNUmgVQSFdtOnM7L8wA&oe=6A425F2E)

![](https://scontent-lax3-1.xx.fbcdn.net/v/t39.8562-6/335648731_142576991793348_7786819189843639239_n.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=8y-D2lssn4oQ7kNvwFTd6HW&_nc_oc=AdrrTwo4suYO8PkdPo9laVBl6zQ_nl_bkX8rTo_vc2gol0c7kv5V7fVIMNlQBmKlLZdIbpz5u8j9_tT6kGbN5qid&_nc_zt=14&_nc_ht=scontent-lax3-1.xx&_nc_gid=qapESLXGDYE6DL91nQan_A&_nc_ss=7b289&oh=00_Af9hHbTNoxQcp_PTpWokknUzGpJvNUmgVQSFdtOnM7L8wA&oe=6A425F2E)](https://www.youtube.com/@aiatmeta)
