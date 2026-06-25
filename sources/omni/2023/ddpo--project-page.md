# Training Diffusion Models with Reinforcement Learning
Source: https://rl-diffusion.github.io/
Training Diffusion Models with Reinforcement Learning




## Training Diffusion Models with Reinforcement Learning

[Paper](https://arxiv.org/pdf/2305.13301) |
[Code & Weights](https://github.com/jannerm/ddpo) |
[Blog](https://bair.berkeley.edu/blog/2023/07/14/ddpo/)

[Kevin Black](https://kevin.black)\*,
[Michael Janner](https://jannerm.github.io)\*,
[Yilun Du](https://yilundu.github.io),
[Ilya Kostrikov](https://www.kostrikov.xyz),
and [Sergey Levine](https://people.eecs.berkeley.edu/~svlevine/)

\*equal contribution

[![

](images/teaser/teaser.jpg)](images/teaser/teaser.mp4)

![](images/replay.png)

replay

**UPDATE:** We now have a PyTorch implementation that supports LoRA for low-memory training [here](https://github.com/kvablack/ddpo-pytorch)!

### Summary

We train diffusion models directly on downstream objectives using reinforcement learning (RL).
We do this by posing denoising diffusion as a multi-step decision-making problem, enabling a class of
policy gradient algorithms that we call **denoising diffusion policy optimization** (DDPO).
We use DDPO to finetune Stable Diffusion on objectives that are difficult to express via prompting, such
as image compressibility, and those derived from human feedback, such as aesthetic quality.
We also show that DDPO can be used to improve prompt-image alignment without any human annotations using
feedback from a vision-language model.

![](images/vlm-bertscore.jpg)

We use feedback from a large vision-language model, [LLaVA](https://llava-vl.github.io), to
automatically improve prompt-image alignment.

### Results

We first evaluate our method on a few basic reward functions: compressibility, incompressibility, and
aesthetic quality as determined by the [LAION aesthetic
predictor](https://laion.ai/blog/laion-aesthetics/).

Base Model
![](images/algorithm-comparison/lora/pretrained/fox.jpg)
![](images/algorithm-comparison/lora/pretrained/dolphin.jpg)
![](images/algorithm-comparison/lora/pretrained/cow.jpg)
![](images/algorithm-comparison/lora/pretrained/hedgehog.jpg)
![](images/algorithm-comparison/lora/pretrained/wolf.jpg)
![](images/algorithm-comparison/lora/pretrained/horse.jpg)
![](images/algorithm-comparison/lora/pretrained/pig.jpg)
![](images/algorithm-comparison/lora/pretrained/squirrel.jpg)
![](images/algorithm-comparison/lora/pretrained/cat.jpg)

Aesthetic
![](images/algorithm-comparison/lora/aesthetic/fox.jpg)
![](images/algorithm-comparison/lora/aesthetic/dolphin.jpg)
![](images/algorithm-comparison/lora/aesthetic/cow.jpg)
![](images/algorithm-comparison/lora/aesthetic/hedgehog.jpg)
![](images/algorithm-comparison/lora/aesthetic/wolf.jpg)
![](images/algorithm-comparison/lora/aesthetic/horse.jpg)
![](images/algorithm-comparison/lora/aesthetic/pig.jpg)
![](images/algorithm-comparison/lora/aesthetic/squirrel.jpg)
![](images/algorithm-comparison/lora/aesthetic/cat.jpg)

Compressibility
![](images/algorithm-comparison/lora/compress/fox.jpg)
![](images/algorithm-comparison/lora/compress/dolphin.jpg)
![](images/algorithm-comparison/lora/compress/cow.jpg)
![](images/algorithm-comparison/lora/compress/hedgehog.jpg)
![](images/algorithm-comparison/lora/compress/wolf.jpg)
![](images/algorithm-comparison/lora/compress/horse.jpg)
![](images/algorithm-comparison/lora/compress/pig.jpg)
![](images/algorithm-comparison/lora/compress/squirrel.jpg)
![](images/algorithm-comparison/lora/compress/cat.jpg)

Incompressibility
![](images/algorithm-comparison/lora/incompress/fox.jpg)
![](images/algorithm-comparison/lora/incompress/dolphin.jpg)
![](images/algorithm-comparison/lora/incompress/cow.jpg)
![](images/algorithm-comparison/lora/incompress/hedgehog.jpg)
![](images/algorithm-comparison/lora/incompress/wolf.jpg)
![](images/algorithm-comparison/lora/incompress/horse.jpg)
![](images/algorithm-comparison/lora/incompress/pig.jpg)
![](images/algorithm-comparison/lora/incompress/squirrel.jpg)
![](images/algorithm-comparison/lora/incompress/cat.jpg)

### Prompt-Image Alignment

We also optimize a more ambitious reward function: prompt-image alignment as determined by the [LLaVA](https://llava-vl.github.io) vision-language model.
We use animals doing human-like activites, since the base Stable Diffusion model tends to struggle with
these kinds of prompts.
Each series of 3 images shows samples for the same prompt and random seed throughout training, with the
first sample coming from the base model.
Interestingly, the model shifts towards a more cartoon-like style, which was not intentional.
We hypothesize that this is because animals doing human-like activities are more likely to appear in a
cartoon-like style in the pretraining data, so the model shifts towards this style to more
easily align with the prompt.

a dolphin riding a bike
![](images/vlm/dolphin_bike/0.jpg)
![](images/vlm/dolphin_bike/1.jpg)
![](images/vlm/dolphin_bike/5.jpg)

RL training

a hedgehog riding a bike
![](images/vlm/hedgehog_bike/0.jpg)
![](images/vlm/hedgehog_bike/1.jpg)
![](images/vlm/hedgehog_bike/2.jpg)

RL training

a dog riding a bike
![](images/vlm/dog_bike/0.jpg)
![](images/vlm/dog_bike/2.jpg)
![](images/vlm/dog_bike/5.jpg)

RL training

a lizard riding a bike
![](images/vlm/lizard_bike/0.jpg)
![](images/vlm/lizard_bike/1.jpg)
![](images/vlm/lizard_bike/2.jpg)

RL training

a bear washing dishes
![](images/vlm/bear_dishes/0.jpg)
![](images/vlm/bear_dishes/3.jpg)
![](images/vlm/bear_dishes/5.jpg)

RL training

a shark washing dishes
![](images/vlm/shark_dishes/0.jpg)
![](images/vlm/shark_dishes/1.jpg)
![](images/vlm/shark_dishes/2.jpg)

RL training

a frog washing dishes
![](images/vlm/frog_dishes/0.jpg)
![](images/vlm/frog_dishes/1.jpg)
![](images/vlm/frog_dishes/2.jpg)

RL training

a monkey washing dishes
![](images/vlm/monkey_dishes/0.jpg)
![](images/vlm/monkey_dishes/1.jpg)
![](images/vlm/monkey_dishes/2.jpg)

RL training

a chicken playing chess
![](images/vlm/chicken_chess/0.jpg)
![](images/vlm/chicken_chess/1.jpg)
![](images/vlm/chicken_chess/2.jpg)

RL training

an ant playing chess
![](images/vlm/ant_chess/0.jpg)
![](images/vlm/ant_chess/1.jpg)
![](images/vlm/ant_chess/5.jpg)

RL training

### Generalization: Aesthetic Quality

Unexpected generalization has been found to arise when finetuning large language models with RL: for
example, models finetuned on instruction-following only in English often become better in other
languages.
We find that the same phenomenon occurs with text-to-image diffusion models.
Our aesthetic quality model was finetuned using prompts from a list of 45 common animals.
We find that it generalizes to unseen animals, as well as everyday objects (to a slightly lesser
extent).

New Animals: Base Model
![](images/generalization/aesthetic-animal/before/0.jpg)
![](images/generalization/aesthetic-animal/before/1.jpg)
![](images/generalization/aesthetic-animal/before/2.jpg)
![](images/generalization/aesthetic-animal/before/3.jpg)
![](images/generalization/aesthetic-animal/before/4.jpg)
![](images/generalization/aesthetic-animal/before/5.jpg)
![](images/generalization/aesthetic-animal/before/6.jpg)
![](images/generalization/aesthetic-animal/before/7.jpg)
![](images/generalization/aesthetic-animal/before/8.jpg)

New Animals: Aesthetic
![](images/generalization/aesthetic-animal/after/0.jpg)
![](images/generalization/aesthetic-animal/after/1.jpg)
![](images/generalization/aesthetic-animal/after/2.jpg)
![](images/generalization/aesthetic-animal/after/3.jpg)
![](images/generalization/aesthetic-animal/after/4.jpg)
![](images/generalization/aesthetic-animal/after/5.jpg)
![](images/generalization/aesthetic-animal/after/6.jpg)
![](images/generalization/aesthetic-animal/after/7.jpg)
![](images/generalization/aesthetic-animal/after/8.jpg)

Non-Animals: Base Model
![](images/generalization/aesthetic-objects/before/0.jpg)
![](images/generalization/aesthetic-objects/before/1.jpg)
![](images/generalization/aesthetic-objects/before/2.jpg)
![](images/generalization/aesthetic-objects/before/3.jpg)
![](images/generalization/aesthetic-objects/before/4.jpg)
![](images/generalization/aesthetic-objects/before/5.jpg)
![](images/generalization/aesthetic-objects/before/6.jpg)
![](images/generalization/aesthetic-objects/before/7.jpg)
![](images/generalization/aesthetic-objects/before/8.jpg)

Non-Animals: Aesthetic
![](images/generalization/aesthetic-objects/after/0.jpg)
![](images/generalization/aesthetic-objects/after/1.jpg)
![](images/generalization/aesthetic-objects/after/2.jpg)
![](images/generalization/aesthetic-objects/after/3.jpg)
![](images/generalization/aesthetic-objects/after/4.jpg)
![](images/generalization/aesthetic-objects/after/5.jpg)
![](images/generalization/aesthetic-objects/after/6.jpg)
![](images/generalization/aesthetic-objects/after/7.jpg)
![](images/generalization/aesthetic-objects/after/8.jpg)

### Generalization: Prompt-Image Alignment

Our prompt-image alignment model was finetuned using the same list of 45 common animals and **only 3
activities**:
*riding a bike*, *washing dishes*, and *playing chess*.
However, we find that it generalizes not only to unseen animals, but also to unseen activities and even
novel combinations of the two.
It also generalizes to inanimate objects, though to a much more limited extent.
Each series of 3 images again shows samples for the same prompt and random seed throughout training,
with the first sample coming from the base model.

a capybara washing dishes
![](images/vlm/capybara_dishes/0.jpg)
![](images/vlm/capybara_dishes/1.jpg)
![](images/vlm/capybara_dishes/2.jpg)

RL training

snail playing chess
![](images/vlm/snail_chess/0.jpg)
![](images/vlm/snail_chess/1.jpg)
![](images/vlm/snail_chess/5.jpg)

RL training

a dog doing laundry
![](images/vlm/dog_laundry/0.jpg)
![](images/vlm/dog_laundry/1.jpg)
![](images/vlm/dog_laundry/2.jpg)

RL training

a giraffe playing basketball
![](images/vlm/giraffe_basketball/0.jpg)
![](images/vlm/giraffe_basketball/1.jpg)
![](images/vlm/giraffe_basketball/2.jpg)

RL training

a parrot driving a car
![](images/vlm/parrot_car/0.jpg)
![](images/vlm/parrot_car/1.jpg)
![](images/vlm/parrot_car/2.jpg)

RL training

a duck taking an exam
![](images/vlm/duck_exam/0.jpg)
![](images/vlm/duck_exam/1.jpg)
![](images/vlm/duck_exam/2.jpg)

RL training

a robot fishing in a lake
![](images/vlm/robot_fishing/0.jpg)
![](images/vlm/robot_fishing/1.jpg)
![](images/vlm/robot_fishing/2.jpg)

RL training

a horse typing on a keyboard
![](images/vlm/horse_keyboard/0.jpg)
![](images/vlm/horse_keyboard/1.jpg)
![](images/vlm/horse_keyboard/2.jpg)

RL training

a rabbit sewing clothes
![](images/vlm/rabbit_sewing/0.jpg)
![](images/vlm/rabbit_sewing/1.jpg)
![](images/vlm/rabbit_sewing/2.jpg)

RL training

a tree riding a bike
![](images/vlm/tree_bike/0.jpg)
![](images/vlm/tree_bike/1.jpg)
![](images/vlm/tree_bike/2.jpg)

RL training

a car eating a sandwich
![](images/vlm/car_sandwich/0.jpg)
![](images/vlm/car_sandwich/1.jpg)
![](images/vlm/car_sandwich/2.jpg)

RL training

an apple playing soccer
![](images/vlm/apple_soccer/0.jpg)
![](images/vlm/apple_soccer/1.jpg)
![](images/vlm/apple_soccer/2.jpg)

RL training

### Overoptimization

Finetuning on a reward function, especially a learned one, has been observed to lead to reward
overoptimization in which the model exploits the reward function to achieve a high reward in a
non-useful way.
Our setting is no exception: on all the objectives, the model eventually destroys any meaningful image
content to maximize reward.

Compressibility
![](images/overoptimization/jpeg-ppo-llama/0.jpg)
![](images/overoptimization/jpeg-ppo-llama/79.jpg)
![](images/overoptimization/jpeg-ppo-llama/109.jpg)

RL training

Incompressibility
![](images/overoptimization/neg-jpeg-ppo-hartebeest/0.jpg)
![](images/overoptimization/neg-jpeg-ppo-hartebeest/59.jpg)
![](images/overoptimization/neg-jpeg-ppo-hartebeest/109.jpg)

RL training

  

We also observed that LLaVA is susceptible to typographic attacks:
when optimizing for alignment with respect to prompts of the form "*n* animals", DDPO was able to
successfully fool LLaVA by instead generating text loosely resembling the correct number.

![](images/overoptimization/vlm-counting/six-monkeys-2.jpg)
![](images/overoptimization/vlm-counting/six-tigers.jpg)
![](images/overoptimization/vlm-counting/five-turtles.jpg)
![](images/overoptimization/vlm-counting/seven-pigs.jpg)
![](images/overoptimization/vlm-counting/six-turtles.jpg)
![](images/overoptimization/vlm-counting/eight-lions.jpg)
![](images/overoptimization/vlm-counting/four-chickens.jpg)
![](images/overoptimization/vlm-counting/three-foxes.jpg)
![](images/overoptimization/vlm-counting/seven-lions.jpg)
![](images/overoptimization/vlm-counting/eight-foxes.jpg)
![](images/overoptimization/vlm-counting/five-frogs.jpg)
![](images/overoptimization/vlm-counting/seven-wolves.jpg)
![](images/overoptimization/vlm-counting/six-birds.jpg)
![](images/overoptimization/vlm-counting/seven-horses.jpg)
![](images/overoptimization/vlm-counting/five-wolves.jpg)
![](images/overoptimization/vlm-counting/six-dogs.jpg)
![](images/overoptimization/vlm-counting/six-frogs.jpg)
![](images/overoptimization/vlm-counting/eoght-cats.jpg)
![](images/overoptimization/vlm-counting/six-turtles-2.jpg)
![](images/overoptimization/vlm-counting/five-raccoons.jpg)
![](images/overoptimization/vlm-counting/six-lions.jpg)
![](images/overoptimization/vlm-counting/seven-birds.jpg)
![](images/overoptimization/vlm-counting/six-monkeys.jpg)
![](images/overoptimization/vlm-counting/six-cows.jpg)
