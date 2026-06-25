# ACE++: Instruction-Based Image Creation and Editing via Context-Aware Content Filling
Source: https://ali-vilab.github.io/ACE_plus_page/
ACE++: Instruction-Based Image Creation and Editing via Context-Aware Content Filling



# ++: Instruction-Based Image Creation and Editing via Context-Aware Content Filling

Chaojie Mao,

Jingfeng Zhang,

Yulin Pan,

Zeyinzi Jiang,

Zhen Han,

Yu Liu,

Jingren Zhou



















[arXiv](https://arxiv.org/abs/2501.02487)


[Code](https://github.com/ali-vilab/ACE_plus)


[Model(HF)](https://huggingface.co/ali-vilab/ACE_Plus/tree/main)


[Model(MS)](https://www.modelscope.cn/models/iic/ACE_Plus/summary)


[Demo(HF)](https://huggingface.co/spaces/scepter-studio/ACE-Plus)

[Demo(MS)](https://www.modelscope.cn/studios/iic/ACE-Plus/summary)

Subject-Driven
Portrait-Consistency
Flexible ins./des.
Local Editing
Local Reference Editing

[

](static/videos/ace++.webm)



## Abstract

We report ACE++, an instruction-based diffusion framework that tackles various image generation and editing tasks.
Inspired by the input format for the inpainting task proposed by FLUX.1-Fill-dev, we improve the Long-context Condition Unit (LCU)
introduced in ACE and extend this input paradigm to any editing and
generation tasks. To take full advantage of image generative priors, we develop
a two-stage training scheme to minimize the efforts of finetuning powerful text-to-image diffusion models like FLUX.1-dev.
In the first stage, we pre-train the
model using task data with the 0-ref tasks from the text-to-image model. There
are many models in the community based on the post-training of text-to-image
foundational models that meet this training paradigm of the first stage. For example, FLUX.1-Fill-dev deals primarily with painting tasks and can be used as
an initialization to accelerate the training process. In the second stage, we finetune the above model to support the general instructions using all tasks defined
in ACE. To promote the widespread application of ACE++ in different scenarios, we provide a comprehensive set of models that cover both full finetuning and
lightweight finetuning, while considering general applicability and applicability in
vertical scenarios. The qualitative analysis showcases the superiority of ACE++
in terms of generating image quality and prompt following ability



![method](static/images/method++.png)



## Subject-Driven Generation

![Character 1](static/images/subject/input/test_cartoon_1.jpg)

![Character 2](static/images/subject/output/cartoon_1.jpg)

#### The duck is walking on the road with many shops on both sides, anime style.

![Character 3](static/images/subject/output/cartoon_2.jpg)

#### The duck sit on beach chairs drinking drinks, with coconut trees and the sea behind, anime style.

![Character 4](static/images/subject/output/cartoon_3.jpg)

#### The duck sits on the sofa in the living room with many indoor decorations.

![Character 5](static/images/subject/output/cartoon_4.jpg)

#### The duck is riding a skateboard in a skate park filled with colorful graffiti, anime style.

![Character 1](static/images/subject/input/17160902d2nl.jpg)

![Character 2](static/images/subject/output/logo_1.jpg)

#### Show the logo printed elegantly on the front of a premium product box, nestled among natural elements like leaves and wood to reflect an eco-friendly brand.

![Character 3](static/images/subject/output/logo_2.jpg)

#### Incorporate the logo into a stylish name badge hanging from a lanyard, worn by participants at a professional conference with a bright and enaging background.

![Character 4](static/images/subject/output/logo_3.jpg)

#### Render the logo in dynamic animation on a digital billboard, showcasing it in a colorful urban landscape as commuters pass by during evening rush hour.

![Character 5](static/images/subject/output/logo_4.jpg)

#### Display the logo in a minimalist style printed in white on a matte black ceramic coffee mug, alongside a steaming cup of coffee on a cozy cafe table.

![Character 1](static/images/subject/input/test_ip_2.jpg)

![Character 2](static/images/subject/output/ip_1.jpg)

#### The girl's pattern is printed on the computer screen and the packing box on the table, with rich anime elements.

![Character 3](static/images/subject/output/ip_2.jpg)

#### The girl’s style acrylic standing plaque is placed in front of the computer on the desk.

![Character 4](static/images/subject/output/ip_3.jpg)

#### Print the girl's design on a handsome off-road vehicle, with the streets of the city behind it.

![Character 5](static/images/subject/output/ip_4.jpg)

#### The casing of a desktop computer from ASUS features a design of this cartoon girl. The main unit is placed on the desk, with a close-up showcasing the design details of the case. The girl's pattern blends seamlessly with the exterior of the unit. The transparent case design allows the internal hardware to be clearly visible, with blinking LED lights highlighting the details of the graphics card, motherboard, and other components.

![Character 1](static/images/subject/input/test_icon_1.jpg)

![Character 2](static/images/subject/output/icon_4.jpg)

#### Attach this icon to the top right corner of a pair of jeans, product image.

![Character 3](static/images/subject/output/icon_1.jpg)

#### Place this icon in the center of a sleek black leather wallet on a wooden table.

![Character 4](static/images/subject/output/icon_2.jpg)

#### Stick this icon to the right sleeve of a stylish red sports jacket hanging in a vibrant urban alley.

![Character 5](static/images/subject/output/icon_3.jpg)

#### Stick this icon on the tag hanging on the fashionable red jacket.

![Character 1](static/images/subject/input/test_toy_1.jpg)

![Character 2](static/images/subject/output/toy_4.jpg)

#### the furry duck toy wears a blue sweater, is placed on a bookshelf nearby a television.

![Character 3](static/images/subject/output/toy_1.jpg)

#### Plush ducks are placed on Spider Man's head and shuttle through the city with him.

![Character 4](static/images/subject/output/toy_3.jpg)

#### Plush ducks are drifting on the sea surface in a small boat.

![Character 5](static/images/subject/output/toy_2.jpg)

#### Plush duck toy wearing sunglasses, placed next to vinyl record, rock style.

![Character 1](static/images/subject/input/test_creative_1.jpg)

![Character 2](static/images/subject/output/creative_1.jpg)

#### The fox is standing with Snow White in front of a cartoon castle gate.

![Character 3](static/images/subject/output/creative_2.jpg)

#### Make this fox become a twin fox. They are in the office, with one fox looking at his watch.

![Character 4](static/images/subject/output/creative_3.jpg)

#### There is a fox on the pedestrian street of the city, surrounded by people coming and going.

![Character 5](static/images/subject/output/creative_4.jpg)

#### The fox pendant is hanging next to the backpack, with a close-up of the fox pendant and a blurred background.

![Character 1](static/images/subject/input/test_cartoon_1.jpg)

![Character 2](static/images/subject/output/cartoon_1.jpg)

#### The duck is walking on the road with many shops on both sides, anime style.

![Character 3](static/images/subject/output/cartoon_2.jpg)

#### The duck sit on beach chairs drinking drinks, with coconut trees and the sea behind, anime style.

![Character 4](static/images/subject/output/cartoon_3.jpg)

#### The duck sits on the sofa in the living room with many indoor decorations.

![Character 5](static/images/subject/output/cartoon_4.jpg)

#### The duck is riding a skateboard in a skate park filled with colorful graffiti, anime style.

![Character 1](static/images/subject/input/17160902d2nl.jpg)

![Character 2](static/images/subject/output/logo_1.jpg)

#### Show the logo printed elegantly on the front of a premium product box, nestled among natural elements like leaves and wood to reflect an eco-friendly brand.

![Character 3](static/images/subject/output/logo_2.jpg)

#### Incorporate the logo into a stylish name badge hanging from a lanyard, worn by participants at a professional conference with a bright and enaging background.

![Character 4](static/images/subject/output/logo_3.jpg)

#### Render the logo in dynamic animation on a digital billboard, showcasing it in a colorful urban landscape as commuters pass by during evening rush hour.

![Character 5](static/images/subject/output/logo_4.jpg)

#### Display the logo in a minimalist style printed in white on a matte black ceramic coffee mug, alongside a steaming cup of coffee on a cozy cafe table.

![Character 1](static/images/subject/input/test_ip_2.jpg)

![Character 2](static/images/subject/output/ip_1.jpg)

#### The girl's pattern is printed on the computer screen and the packing box on the table, with rich anime elements.

![Character 3](static/images/subject/output/ip_2.jpg)

#### The girl’s style acrylic standing plaque is placed in front of the computer on the desk.

![Character 4](static/images/subject/output/ip_3.jpg)

#### Print the girl's design on a handsome off-road vehicle, with the streets of the city behind it.

![Character 5](static/images/subject/output/ip_4.jpg)

#### The casing of a desktop computer from ASUS features a design of this cartoon girl. The main unit is placed on the desk, with a close-up showcasing the design details of the case. The girl's pattern blends seamlessly with the exterior of the unit. The transparent case design allows the internal hardware to be clearly visible, with blinking LED lights highlighting the details of the graphics card, motherboard, and other components.

![Character 1](static/images/subject/input/test_icon_1.jpg)

![Character 2](static/images/subject/output/icon_4.jpg)

#### Attach this icon to the top right corner of a pair of jeans, product image.

![Character 3](static/images/subject/output/icon_1.jpg)

#### Place this icon in the center of a sleek black leather wallet on a wooden table.

![Character 4](static/images/subject/output/icon_2.jpg)

#### Stick this icon to the right sleeve of a stylish red sports jacket hanging in a vibrant urban alley.

![Character 5](static/images/subject/output/icon_3.jpg)

#### Stick this icon on the tag hanging on the fashionable red jacket.

![Character 1](static/images/subject/input/test_toy_1.jpg)

![Character 2](static/images/subject/output/toy_4.jpg)

#### the furry duck toy wears a blue sweater, is placed on a bookshelf nearby a television.

![Character 3](static/images/subject/output/toy_1.jpg)

#### Plush ducks are placed on Spider Man's head and shuttle through the city with him.

![Character 4](static/images/subject/output/toy_3.jpg)

#### Plush ducks are drifting on the sea surface in a small boat.

![Character 5](static/images/subject/output/toy_2.jpg)

#### Plush duck toy wearing sunglasses, placed next to vinyl record, rock style.

![Character 1](static/images/subject/input/test_creative_1.jpg)

![Character 2](static/images/subject/output/creative_1.jpg)

#### The fox is standing with Snow White in front of a cartoon castle gate.

![Character 3](static/images/subject/output/creative_2.jpg)

#### Make this fox become a twin fox. They are in the office, with one fox looking at his watch.

![Character 4](static/images/subject/output/creative_3.jpg)

#### There is a fox on the pedestrian street of the city, surrounded by people coming and going.

![Character 5](static/images/subject/output/creative_4.jpg)

#### The fox pendant is hanging next to the backpack, with a close-up of the fox pendant and a blurred background.

![Character 1](static/images/subject/input/test_cartoon_1.jpg)

![Character 2](static/images/subject/output/cartoon_1.jpg)

#### The duck is walking on the road with many shops on both sides, anime style.

![Character 3](static/images/subject/output/cartoon_2.jpg)

#### The duck sit on beach chairs drinking drinks, with coconut trees and the sea behind, anime style.

![Character 4](static/images/subject/output/cartoon_3.jpg)

#### The duck sits on the sofa in the living room with many indoor decorations.

![Character 5](static/images/subject/output/cartoon_4.jpg)

#### The duck is riding a skateboard in a skate park filled with colorful graffiti, anime style.

![Character 1](static/images/subject/input/17160902d2nl.jpg)

![Character 2](static/images/subject/output/logo_1.jpg)

#### Show the logo printed elegantly on the front of a premium product box, nestled among natural elements like leaves and wood to reflect an eco-friendly brand.

![Character 3](static/images/subject/output/logo_2.jpg)

#### Incorporate the logo into a stylish name badge hanging from a lanyard, worn by participants at a professional conference with a bright and enaging background.

![Character 4](static/images/subject/output/logo_3.jpg)

#### Render the logo in dynamic animation on a digital billboard, showcasing it in a colorful urban landscape as commuters pass by during evening rush hour.

![Character 5](static/images/subject/output/logo_4.jpg)

#### Display the logo in a minimalist style printed in white on a matte black ceramic coffee mug, alongside a steaming cup of coffee on a cozy cafe table.

![Character 1](static/images/subject/input/test_ip_2.jpg)

![Character 2](static/images/subject/output/ip_1.jpg)

#### The girl's pattern is printed on the computer screen and the packing box on the table, with rich anime elements.

![Character 3](static/images/subject/output/ip_2.jpg)

#### The girl’s style acrylic standing plaque is placed in front of the computer on the desk.

![Character 4](static/images/subject/output/ip_3.jpg)

#### Print the girl's design on a handsome off-road vehicle, with the streets of the city behind it.

![Character 5](static/images/subject/output/ip_4.jpg)

#### The casing of a desktop computer from ASUS features a design of this cartoon girl. The main unit is placed on the desk, with a close-up showcasing the design details of the case. The girl's pattern blends seamlessly with the exterior of the unit. The transparent case design allows the internal hardware to be clearly visible, with blinking LED lights highlighting the details of the graphics card, motherboard, and other components.

![Character 1](static/images/subject/input/test_icon_1.jpg)

![Character 2](static/images/subject/output/icon_4.jpg)

#### Attach this icon to the top right corner of a pair of jeans, product image.

![Character 3](static/images/subject/output/icon_1.jpg)

#### Place this icon in the center of a sleek black leather wallet on a wooden table.

![Character 4](static/images/subject/output/icon_2.jpg)

#### Stick this icon to the right sleeve of a stylish red sports jacket hanging in a vibrant urban alley.

![Character 5](static/images/subject/output/icon_3.jpg)

#### Stick this icon on the tag hanging on the fashionable red jacket.

![Character 1](static/images/subject/input/test_toy_1.jpg)

![Character 2](static/images/subject/output/toy_4.jpg)

#### the furry duck toy wears a blue sweater, is placed on a bookshelf nearby a television.

![Character 3](static/images/subject/output/toy_1.jpg)

#### Plush ducks are placed on Spider Man's head and shuttle through the city with him.

![Character 4](static/images/subject/output/toy_3.jpg)

#### Plush ducks are drifting on the sea surface in a small boat.

![Character 5](static/images/subject/output/toy_2.jpg)

#### Plush duck toy wearing sunglasses, placed next to vinyl record, rock style.

![Character 1](static/images/subject/input/test_creative_1.jpg)

![Character 2](static/images/subject/output/creative_1.jpg)

#### The fox is standing with Snow White in front of a cartoon castle gate.

![Character 3](static/images/subject/output/creative_2.jpg)

#### Make this fox become a twin fox. They are in the office, with one fox looking at his watch.

![Character 4](static/images/subject/output/creative_3.jpg)

#### There is a fox on the pedestrian street of the city, surrounded by people coming and going.

![Character 5](static/images/subject/output/creative_4.jpg)

#### The fox pendant is hanging next to the backpack, with a close-up of the fox pendant and a blurred background.

![Character 1](static/images/subject/input/test_cartoon_1.jpg)

![Character 2](static/images/subject/output/cartoon_1.jpg)

#### The duck is walking on the road with many shops on both sides, anime style.

![Character 3](static/images/subject/output/cartoon_2.jpg)

#### The duck sit on beach chairs drinking drinks, with coconut trees and the sea behind, anime style.

![Character 4](static/images/subject/output/cartoon_3.jpg)

#### The duck sits on the sofa in the living room with many indoor decorations.

![Character 5](static/images/subject/output/cartoon_4.jpg)

#### The duck is riding a skateboard in a skate park filled with colorful graffiti, anime style.

![Character 1](static/images/subject/input/17160902d2nl.jpg)

![Character 2](static/images/subject/output/logo_1.jpg)

#### Show the logo printed elegantly on the front of a premium product box, nestled among natural elements like leaves and wood to reflect an eco-friendly brand.

![Character 3](static/images/subject/output/logo_2.jpg)

#### Incorporate the logo into a stylish name badge hanging from a lanyard, worn by participants at a professional conference with a bright and enaging background.

![Character 4](static/images/subject/output/logo_3.jpg)

#### Render the logo in dynamic animation on a digital billboard, showcasing it in a colorful urban landscape as commuters pass by during evening rush hour.

![Character 5](static/images/subject/output/logo_4.jpg)

#### Display the logo in a minimalist style printed in white on a matte black ceramic coffee mug, alongside a steaming cup of coffee on a cozy cafe table.

![Character 1](static/images/subject/input/test_ip_2.jpg)

![Character 2](static/images/subject/output/ip_1.jpg)

#### The girl's pattern is printed on the computer screen and the packing box on the table, with rich anime elements.

![Character 3](static/images/subject/output/ip_2.jpg)

#### The girl’s style acrylic standing plaque is placed in front of the computer on the desk.

![Character 4](static/images/subject/output/ip_3.jpg)

#### Print the girl's design on a handsome off-road vehicle, with the streets of the city behind it.

![Character 5](static/images/subject/output/ip_4.jpg)

#### The casing of a desktop computer from ASUS features a design of this cartoon girl. The main unit is placed on the desk, with a close-up showcasing the design details of the case. The girl's pattern blends seamlessly with the exterior of the unit. The transparent case design allows the internal hardware to be clearly visible, with blinking LED lights highlighting the details of the graphics card, motherboard, and other components.



## Portrait-Consistency Generation

![Character 1](static/images/face/input/human_1.jpg)

![Character 2](static/images/face/output/human_1_1.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 3](static/images/face/output/human_1_2.jpg)

#### Make the character in the image embody the goddess Artemis, adorned in ancient Greek-style clothing, showcasing elegance and strength.

![Character 4](static/images/face/output/human_1_3.jpg)

#### (Seed: xxx) Maintain the facial features, A girl is wearing a neat police uniform with "HOPPS" labeled on it and sporting a badge with a cute Disney cartoon style like Officer Judy Hopps from "Zootopia". She has large, bright purple eyes, smiling with a friendly and confident demeanor. She stands in front of a microphone, seemingly giving a speech or presentation, with lively gestures that convey positive emotions. The background is blurred, featuring a cartoon logo of "Police Department".

![Character 5](static/images/face/output/human_1_4.jpg)

#### (Seed: yyy) Maintain the facial features, A girl is wearing a neat police uniform with "HOPPS" labeled on it and sporting a badge with a cute Disney cartoon style like Officer Judy Hopps from "Zootopia". She has large, bright purple eyes, smiling with a friendly and confident demeanor. She stands in front of a microphone, seemingly giving a speech or presentation, with lively gestures that convey positive emotions. The background is blurred, featuring a cartoon logo of "Police Department".

![Character 1](static/images/face/input/human_2.jpg)

![Character 2](static/images/face/output/human_2_1.jpg)

#### Keep the characters in the picture unchanged and switch the background to Chinese architecture.

![Character 3](static/images/face/output/human_2_2.jpg)

#### Transform the character into a modern athlete, wearing shiny sportswear.

![Character 4](static/images/face/output/human_2_3.jpg)

#### Replace the character's clothing with a Chinese traditional clothing, with an ancient teahouse in the background.

![Character 5](static/images/face/output/human_2_4.jpg)

#### Insert the character into Grant Wood’s "American Gothic" scene, filled with a rural atmosphere.

![Character 1](static/images/face/input/human_3.jpg)

![Character 2](static/images/face/output/human_3_1.jpg)

#### Replace the character's outfit with an Indian sari and place her in a colorful market.

![Character 3](static/images/face/output/human_3_2.jpg)

#### the man like muscular superhero character standing confidently in an underwater setting. He is dressed in a striking metallic costume featuring green and gold hues, designed with intricate patterns that evoke a sense of aquatic origins. The character holds a powerful trident in one hand and a shield in the other, emphasizing his role as a protector of the seas. Water splashes around him, enhancing the dynamic and heroic atmosphere of the scene. His flowing hair adds to the dramatic effect, highlighting his fierce demeanor as he prepares for action in the depths of the ocean.

![Character 4](static/images/face/output/human_3_3.jpg)

#### the person seated at a chessboard, holding a knight piece in their hand. The chess setup includes a mix of wooden and lightcolored pieces, creating a contrast against a polished wooden table. Surrounding the chessboard are various small bottles, likely containing different liquids, suggesting an assortment of beverages or condiments. The person is dressed in a simple black shirt with a white collar, exuding a vintage or classic aesthetic, and has short, styled hair. The backdrop is a muted gray.

![Character 5](static/images/face/output/human_3_4.jpg)

#### Replace the character's clothing with classic Western cowboy attire, holding a guitar by the campfire.

![Character 1](static/images/face/input/human_4.jpg)

![Character 2](static/images/face/output/human_4_1.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 3](static/images/face/output/human_4_2.jpg)

#### The man, with his white hair billowing in the gentle breeze, glides down the sunlit street on his sleek white electric scooter, a picture of carefree joy. He’s dressed in a light blue shirt and comfortable jeans, exuding a relaxed charm as he makes his way to the local market to pick up groceries. The pleasant weather adds to his contentment, with birds chirping and the sun casting a warm glow. Behind him, a colorful roadside vendor displays vibrant fruits and fresh flowers, creating a lively scene. The man smiles at the vendor, appreciating the community spirit around him, as he feels the excitement of a simple errand that brightens his day.

![Character 4](static/images/face/output/human_4_3.jpg)

#### Dress the character in old-fashioned pirate attire, standing inside a ship's cabin.

![Character 5](static/images/face/output/human_4_4.jpg)

#### Dress the character in the image in Harry Potter's wizarding robes, holding a wand as if casting a spell.

![Character 1](static/images/face/input/human_5.jpg)

![Character 2](static/images/face/output/human_5_1.jpg)

#### Transform the character in the image into Superman, wearing a blue jumpsuit, a red cape, and featuring the Superman logo on the chest.

![Character 3](static/images/face/output/human_5_2.jpg)

#### the man dressed in traditional attire inspired by historical Asian clothing. He has a decorative hair accessory. Her outfit consists of layered garments featuring vibrant colors, notably orange and blue, complemented by a patterned sash around his waist. He carries a long, ornate sword with a decorative hilt, resting against her arm. Additionally, he has a straw backpack slung over one shoulder and various pouches attached to her belt, suggesting readiness for travel or adventure. The backdrop is a lush, green landscape, enhancing the adventurous theme of the image.

![Character 4](static/images/face/output/human_5_3.jpg)

#### Dress the character in medieval knight armor, standing in front of a castle.

![Character 5](static/images/face/output/human_5_4.jpg)

#### Make the character in the image resemble Peter Pan, dressed in a green outfit and evoking a sense of flying.

![Character 1](static/images/face/input/human_6.jpg)

![Character 2](static/images/face/output/human_6_1.jpg)

#### Dress the character in the image in the combat gear of Desert Fox, displaying a brave and adventurous demeanor.

![Character 3](static/images/face/output/human_6_2.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 4](static/images/face/output/human_6_3.jpg)

#### the man standing confidently in traditional Middle Eastern attire. He is wearing a light, flowing thobe with intricate golden detailing along the neckline. A white dishdasha is worn underneath, complementing the overall elegant look. The attire is completed with a black agal and a white ghutrah draped gracefully. The background is plain, emphasizing the cultural significance of the garment. The background is a magnificent palace.

![Character 5](static/images/face/output/human_6_4.jpg)

#### Change the character's attire to traditional Russian lace headscarf and long skirt, with a winter snow landscape around her.

![Character 1](static/images/face/input/human_1.jpg)

![Character 2](static/images/face/output/human_1_1.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 3](static/images/face/output/human_1_2.jpg)

#### Make the character in the image embody the goddess Artemis, adorned in ancient Greek-style clothing, showcasing elegance and strength.

![Character 4](static/images/face/output/human_1_3.jpg)

#### (Seed: xxx) Maintain the facial features, A girl is wearing a neat police uniform with "HOPPS" labeled on it and sporting a badge with a cute Disney cartoon style like Officer Judy Hopps from "Zootopia". She has large, bright purple eyes, smiling with a friendly and confident demeanor. She stands in front of a microphone, seemingly giving a speech or presentation, with lively gestures that convey positive emotions. The background is blurred, featuring a cartoon logo of "Police Department".

![Character 5](static/images/face/output/human_1_4.jpg)

#### (Seed: yyy) Maintain the facial features, A girl is wearing a neat police uniform with "HOPPS" labeled on it and sporting a badge with a cute Disney cartoon style like Officer Judy Hopps from "Zootopia". She has large, bright purple eyes, smiling with a friendly and confident demeanor. She stands in front of a microphone, seemingly giving a speech or presentation, with lively gestures that convey positive emotions. The background is blurred, featuring a cartoon logo of "Police Department".

![Character 1](static/images/face/input/human_2.jpg)

![Character 2](static/images/face/output/human_2_1.jpg)

#### Keep the characters in the picture unchanged and switch the background to Chinese architecture.

![Character 3](static/images/face/output/human_2_2.jpg)

#### Transform the character into a modern athlete, wearing shiny sportswear.

![Character 4](static/images/face/output/human_2_3.jpg)

#### Replace the character's clothing with a Chinese traditional clothing, with an ancient teahouse in the background.

![Character 5](static/images/face/output/human_2_4.jpg)

#### Insert the character into Grant Wood’s "American Gothic" scene, filled with a rural atmosphere.

![Character 1](static/images/face/input/human_3.jpg)

![Character 2](static/images/face/output/human_3_1.jpg)

#### Replace the character's outfit with an Indian sari and place her in a colorful market.

![Character 3](static/images/face/output/human_3_2.jpg)

#### the man like muscular superhero character standing confidently in an underwater setting. He is dressed in a striking metallic costume featuring green and gold hues, designed with intricate patterns that evoke a sense of aquatic origins. The character holds a powerful trident in one hand and a shield in the other, emphasizing his role as a protector of the seas. Water splashes around him, enhancing the dynamic and heroic atmosphere of the scene. His flowing hair adds to the dramatic effect, highlighting his fierce demeanor as he prepares for action in the depths of the ocean.

![Character 4](static/images/face/output/human_3_3.jpg)

#### the person seated at a chessboard, holding a knight piece in their hand. The chess setup includes a mix of wooden and lightcolored pieces, creating a contrast against a polished wooden table. Surrounding the chessboard are various small bottles, likely containing different liquids, suggesting an assortment of beverages or condiments. The person is dressed in a simple black shirt with a white collar, exuding a vintage or classic aesthetic, and has short, styled hair. The backdrop is a muted gray.

![Character 5](static/images/face/output/human_3_4.jpg)

#### Replace the character's clothing with classic Western cowboy attire, holding a guitar by the campfire.

![Character 1](static/images/face/input/human_4.jpg)

![Character 2](static/images/face/output/human_4_1.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 3](static/images/face/output/human_4_2.jpg)

#### The man, with his white hair billowing in the gentle breeze, glides down the sunlit street on his sleek white electric scooter, a picture of carefree joy. He’s dressed in a light blue shirt and comfortable jeans, exuding a relaxed charm as he makes his way to the local market to pick up groceries. The pleasant weather adds to his contentment, with birds chirping and the sun casting a warm glow. Behind him, a colorful roadside vendor displays vibrant fruits and fresh flowers, creating a lively scene. The man smiles at the vendor, appreciating the community spirit around him, as he feels the excitement of a simple errand that brightens his day.

![Character 4](static/images/face/output/human_4_3.jpg)

#### Dress the character in old-fashioned pirate attire, standing inside a ship's cabin.

![Character 5](static/images/face/output/human_4_4.jpg)

#### Dress the character in the image in Harry Potter's wizarding robes, holding a wand as if casting a spell.

![Character 1](static/images/face/input/human_5.jpg)

![Character 2](static/images/face/output/human_5_1.jpg)

#### Transform the character in the image into Superman, wearing a blue jumpsuit, a red cape, and featuring the Superman logo on the chest.

![Character 3](static/images/face/output/human_5_2.jpg)

#### the man dressed in traditional attire inspired by historical Asian clothing. He has a decorative hair accessory. Her outfit consists of layered garments featuring vibrant colors, notably orange and blue, complemented by a patterned sash around his waist. He carries a long, ornate sword with a decorative hilt, resting against her arm. Additionally, he has a straw backpack slung over one shoulder and various pouches attached to her belt, suggesting readiness for travel or adventure. The backdrop is a lush, green landscape, enhancing the adventurous theme of the image.

![Character 4](static/images/face/output/human_5_3.jpg)

#### Dress the character in medieval knight armor, standing in front of a castle.

![Character 5](static/images/face/output/human_5_4.jpg)

#### Make the character in the image resemble Peter Pan, dressed in a green outfit and evoking a sense of flying.

![Character 1](static/images/face/input/human_6.jpg)

![Character 2](static/images/face/output/human_6_1.jpg)

#### Dress the character in the image in the combat gear of Desert Fox, displaying a brave and adventurous demeanor.

![Character 3](static/images/face/output/human_6_2.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 4](static/images/face/output/human_6_3.jpg)

#### the man standing confidently in traditional Middle Eastern attire. He is wearing a light, flowing thobe with intricate golden detailing along the neckline. A white dishdasha is worn underneath, complementing the overall elegant look. The attire is completed with a black agal and a white ghutrah draped gracefully. The background is plain, emphasizing the cultural significance of the garment. The background is a magnificent palace.

![Character 5](static/images/face/output/human_6_4.jpg)

#### Change the character's attire to traditional Russian lace headscarf and long skirt, with a winter snow landscape around her.

![Character 1](static/images/face/input/human_1.jpg)

![Character 2](static/images/face/output/human_1_1.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 3](static/images/face/output/human_1_2.jpg)

#### Make the character in the image embody the goddess Artemis, adorned in ancient Greek-style clothing, showcasing elegance and strength.

![Character 4](static/images/face/output/human_1_3.jpg)

#### (Seed: xxx) Maintain the facial features, A girl is wearing a neat police uniform with "HOPPS" labeled on it and sporting a badge with a cute Disney cartoon style like Officer Judy Hopps from "Zootopia". She has large, bright purple eyes, smiling with a friendly and confident demeanor. She stands in front of a microphone, seemingly giving a speech or presentation, with lively gestures that convey positive emotions. The background is blurred, featuring a cartoon logo of "Police Department".

![Character 5](static/images/face/output/human_1_4.jpg)

#### (Seed: yyy) Maintain the facial features, A girl is wearing a neat police uniform with "HOPPS" labeled on it and sporting a badge with a cute Disney cartoon style like Officer Judy Hopps from "Zootopia". She has large, bright purple eyes, smiling with a friendly and confident demeanor. She stands in front of a microphone, seemingly giving a speech or presentation, with lively gestures that convey positive emotions. The background is blurred, featuring a cartoon logo of "Police Department".

![Character 1](static/images/face/input/human_2.jpg)

![Character 2](static/images/face/output/human_2_1.jpg)

#### Keep the characters in the picture unchanged and switch the background to Chinese architecture.

![Character 3](static/images/face/output/human_2_2.jpg)

#### Transform the character into a modern athlete, wearing shiny sportswear.

![Character 4](static/images/face/output/human_2_3.jpg)

#### Replace the character's clothing with a Chinese traditional clothing, with an ancient teahouse in the background.

![Character 5](static/images/face/output/human_2_4.jpg)

#### Insert the character into Grant Wood’s "American Gothic" scene, filled with a rural atmosphere.

![Character 1](static/images/face/input/human_3.jpg)

![Character 2](static/images/face/output/human_3_1.jpg)

#### Replace the character's outfit with an Indian sari and place her in a colorful market.

![Character 3](static/images/face/output/human_3_2.jpg)

#### the man like muscular superhero character standing confidently in an underwater setting. He is dressed in a striking metallic costume featuring green and gold hues, designed with intricate patterns that evoke a sense of aquatic origins. The character holds a powerful trident in one hand and a shield in the other, emphasizing his role as a protector of the seas. Water splashes around him, enhancing the dynamic and heroic atmosphere of the scene. His flowing hair adds to the dramatic effect, highlighting his fierce demeanor as he prepares for action in the depths of the ocean.

![Character 4](static/images/face/output/human_3_3.jpg)

#### the person seated at a chessboard, holding a knight piece in their hand. The chess setup includes a mix of wooden and lightcolored pieces, creating a contrast against a polished wooden table. Surrounding the chessboard are various small bottles, likely containing different liquids, suggesting an assortment of beverages or condiments. The person is dressed in a simple black shirt with a white collar, exuding a vintage or classic aesthetic, and has short, styled hair. The backdrop is a muted gray.

![Character 5](static/images/face/output/human_3_4.jpg)

#### Replace the character's clothing with classic Western cowboy attire, holding a guitar by the campfire.

![Character 1](static/images/face/input/human_4.jpg)

![Character 2](static/images/face/output/human_4_1.jpg)

#### Dress the character in the image with elf ears and a wizard's robe, transforming them into a mage character from a fantasy world.

![Character 3](static/images/face/output/human_4_2.jpg)

#### The man, with his white hair billowing in the gentle breeze, glides down the sunlit street on his sleek white electric scooter, a picture of carefree joy. He’s dressed in a light blue shirt and comfortable jeans, exuding a relaxed charm as he makes his way to the local market to pick up groceries. The pleasant weather adds to his contentment, with birds chirping and the sun casting a warm glow. Behind him, a colorful roadside vendor displays vibrant fruits and fresh flowers, creating a lively scene. The man smiles at the vendor, appreciating the community spirit around him, as he feels the excitement of a simple errand that brightens his day.

![Character 4](static/images/face/output/human_4_3.jpg)

#### Dress the character in old-fashioned pirate attire, standing inside a ship's cabin.

![Character 5](static/images/face/output/human_4_4.jpg)

#### Dress the character in the image in Harry Potter's wizarding robes, holding a wand as if casting a spell.

![Character 1](static/images/face/input/human_5.jpg)

![Character 2](static/images/face/output/human_5_1.jpg)

#### Transform the character in the image into Superman, wearing a blue jumpsuit, a red cape, and featuring the Superman logo on the chest.

![Character 3](static/images/face/output/human_5_2.jpg)

#### the man dressed in traditional attire inspired by historical Asian clothing. He has a decorative hair accessory. Her outfit consists of layered garments featuring vibrant colors, notably orange and blue, complemented by a patterned sash around his waist. He carries a long, ornate sword with a decorative hilt, resting against her arm. Additionally, he has a straw backpack slung over one shoulder and various pouches attached to her belt, suggesting readiness for travel or adventure. The backdrop is a lush, green landscape, enhancing the adventurous theme of the image.

![Character 4](static/images/face/output/human_5_3.jpg)

#### Dress the character in medieval knight armor, standing in front of a castle.

![Character 5](static/images/face/output/human_5_4.jpg)

#### Make the character in the image resemble Peter Pan, dressed in a green outfit and evoking a sense of flying.

![Character 1](static/images

[truncated]
