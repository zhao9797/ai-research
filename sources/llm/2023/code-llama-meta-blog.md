# Introducing Code Llama, a state-of-the-art large language model for coding
Source: https://ai.meta.com/blog/code-llama-large-language-model-coding/
Introducing Code Llama, a state-of-the-art large language model for coding

[![Meta](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/252294889_575082167077436_6034106545912333281_n.svg/meta-logo-primary_standardsize.svg?_nc_cat=108&ccb=1-7&_nc_sid=e280be&_nc_ohc=XK6ck52-T0YQ7kNvwFlWEeZ&_nc_oc=AdpIuMfXawOjagnUKqLLbboYrVlxpoVixtjYG1dDTd9K3QJQTZxFrvVdAWe5LSltiCD1mVTY03wZ6GzqBvqoH3dR&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8iMVUqDj3OOOywcEKP4vLGVOdRDQ9sqFN4nVH7hjBfsg&oe=6A38BEB9)](/)

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

Large Language Model

# Introducing Code Llama, a state-of-the-art large language model for coding

August 24, 2023

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/369899645_822741339422669_4458807373211021546_n.gif?_nc_cat=110&ccb=1-7&_nc_sid=f537c7&_nc_ohc=1lHEpEoWaY4Q7kNvwHo5Rp4&_nc_oc=AdrqA3UJ9XgSwDN58FIiqYFxgL43KWiaiC28ODOFHze8uf4WlJKJXKf9bDESXQzUCKqTmexUAs9fc27Twta4eITA&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8FVoEW-0C8SbH6U-t-bcm2VFqK0pnDX5xQODRBE57T-w&oe=6A38C110)

## Takeaways

**Update: Jan 29, 2024: Releasing Code Llama 70B**

* We are releasing Code Llama 70B, the largest and best-performing model in the Code Llama family
* Code Llama 70B is available in the same three versions as previously released Code Llama models, all free for research and commercial use:
  + CodeLlama - 70B, the foundational code model;
  + CodeLlama - 70B - Python, 70B specialized for Python;
  + and Code Llama - 70B - Instruct 70B, which is fine-tuned for understanding natural language instructions.

  

* Code Llama is a state-of-the-art LLM capable of generating code, and natural language about code, from both code and natural language prompts.
* Code Llama is free for research and commercial use.
* Code Llama is built on top of Llama 2 and is available in three models:
  + Code Llama, the foundational code model;
  + Codel Llama - Python specialized for Python;
  + and Code Llama - Instruct, which is fine-tuned for understanding natural language instructions.
* In our own benchmark testing, Code Llama outperformed state-of-the-art publicly available LLMs on code tasks

---

RECOMMENDED READS

* [Code Llama research paper](https://ai.meta.com/research/publications/code-llama-open-foundation-models-for-code/)
* [Code Llama GitHub](https://github.com/facebookresearch/codellama)
* [Download the Code Llama model](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)

Today, we are releasing Code Llama, a large language model (LLM) that can use text prompts to generate code. Code Llama is state-of-the-art for publicly available LLMs on code tasks, and has the potential to make workflows faster and more efficient for current developers and lower the barrier to entry for people who are learning to code. Code Llama has the potential to be used as a productivity and educational tool to help programmers write more robust, well-documented software.

The generative AI space is evolving rapidly, and we believe an open approach to today’s AI is the best one for developing new AI tools that are innovative, safe, and responsible. We are releasing Code Llama [under the same community license as Llama 2](https://github.com/facebookresearch/llama/blob/main/LICENSE).

## How Code Llama works

Code Llama is a code-specialized version of [Llama 2](https://ai.meta.com/llama/) that was created by further training Llama 2 on its code-specific datasets, sampling more data from that same dataset for longer. Essentially, Code Llama features enhanced coding capabilities, built on top of Llama 2. It can generate code, and natural language about code, from both code and natural language prompts (e.g., “Write me a function that outputs the fibonacci sequence.”) It can also be used for code completion and debugging. It supports many of the most popular languages being used today, including Python, C++, Java, PHP, Typescript (Javascript), C#, and Bash.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/369652058_690162392972818_1173984281354057457_n.gif?_nc_cat=103&ccb=1-7&_nc_sid=f537c7&_nc_ohc=HgbcRK0WrVIQ7kNvwFMZ6iO&_nc_oc=AdqI-wLoEU__jHmvxUf43LmQMM9CCZSFzzFDOtYCakSPD6IJWeP18E82TJLzVH-TDDSZlL_mWYfzMddrFPqsPY5a&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af9RsbwxL_WbTG_wOq9dmZrojglPusor32FUvf12XpH6dA&oe=6A38AA93)

We are releasing four sizes of Code Llama with 7B, 13B, 34B, and 70B parameters respectively. Each of these models is trained with 500B tokens of code and code-related data, apart from 70B, which is trained on 1T tokens. The 7B and 13B base and instruct models have also been trained with fill-in-the-middle (FIM) capability, allowing them to insert code into existing code, meaning they can support tasks like code completion right out of the box.

The three models address different serving and latency requirements. The 7B model, for example, can be served on a single GPU. The 34B and 70B models return the best results and allow for better coding assistance, but the smaller 7B and 13B models are faster and more suitable for tasks that require low latency, like real-time code completion.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/369628374_974402950309179_3355223640107296330_n.gif?_nc_cat=108&ccb=1-7&_nc_sid=f537c7&_nc_ohc=FCUcev5fdssQ7kNvwHhiri1&_nc_oc=Ado96q9uatd704yhR7q3_1wB5DK4h02SOga1h6lUXaJG2muSTOb0DRnieDd3J3dEK0t03fayfW1ZxEYrGAUPzf0_&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af_LaZ4LDPFdYngrywxcDHt0pgC8DgOpWQtSX3F5kKeT7g&oe=6A38928D)

The Code Llama models provide stable generations with up to 100,000 tokens of context. All models are trained on sequences of 16,000 tokens and show improvements on inputs with up to 100,000 tokens.

Aside from being a prerequisite for generating longer programs, having longer input sequences unlocks exciting new use cases for a code LLM. For example, users can provide the model with more context from their codebase to make the generations more relevant. It also helps in debugging scenarios in larger codebases, where staying on top of all code related to a concrete issue can be challenging for developers. When developers are faced with debugging a large chunk of code they can pass the entire length of the code into the model.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/369634634_298372716122486_560769700771259146_n.gif?_nc_cat=110&ccb=1-7&_nc_sid=f537c7&_nc_ohc=FWGcivTS9y0Q7kNvwFS-h6c&_nc_oc=Adox1qaMeaXUZ61jiVw5PyMOFt_8AkgIAnDYa3A0W-7o3jfNGIgKEVK1CWMDS17hA0bbEGMGSYlrgSQ_K_SRODjC&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8FQx8lyEHvDO9_dY9yK-X4dlLD9RaJ896Fy9P6pCik1Q&oe=6A3890CB)

Additionally, we have further fine-tuned two additional variations of Code Llama: Code Llama - Python and Code Llama - Instruct.

Code Llama - Python is a language-specialized variation of Code Llama, further fine-tuned on 100B tokens of Python code. Because Python is the most benchmarked language for code generation – and because Python and [PyTorch](https://ai.meta.com/blog/pytorch-builds-the-future-of-ai-and-machine-learning-at-facebook/) play an important role in the AI community – we believe a specialized model provides additional utility.

Code Llama - Instruct is an instruction fine-tuned and aligned variation of Code Llama. Instruction tuning continues the training process, but with a different objective. The model is fed a “natural language instruction” input and the expected output. This makes it better at understanding what humans expect out of their prompts. We recommend using Code Llama - Instruct variants whenever using Code Llama for code generation since Code Llama - Instruct has been fine-tuned to generate helpful and safe answers in natural language.

We do not recommend using Code Llama or Code Llama - Python to perform general natural language tasks since neither of these models are designed to follow natural language instructions. Code Llama is specialized for code-specific tasks and isn’t appropriate as a foundation model for other tasks.

When using the Code Llama models, users must abide by our license and acceptable use policy.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/422371016_407978498286607_4696551346233862918_n.png?_nc_cat=107&ccb=1-7&_nc_sid=f537c7&_nc_ohc=CCG-hHkwKhQQ7kNvwE3qmD1&_nc_oc=AdoebmkiovuGhY1fcgxNggaa4Y0rcAcxa9WkJtFX5ZpxM-QCg0H8ZxhDQB0wrmSj5D8s6u5CJe-p-R2UlPst88Cu&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af9DqgTAEEXgPOKp6Pt1eu2qmNJA9p0hZWx-ltMEcFYniQ&oe=6A3891B2)

## Evaluating Code Llama’s performance

To test Code Llama’s performance against existing solutions, we used two popular coding benchmarks: [HumanEval](https://github.com/openai/human-eval) and Mostly Basic Python Programming ([MBPP](https://github.com/google-research/google-research/tree/master/mbpp)). HumanEval tests the model’s ability to complete code based on docstrings and MBPP tests the model’s ability to write code based on a description.

Our benchmark testing showed that Code Llama performed better than open-source, code-specific LLMs and outperformed Llama 2. Code Llama 34B, for example, scored 53.7% on HumanEval and 56.2% on MBPP, the highest compared with other state-of-the-art open solutions, and on par with ChatGPT.

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/422554813_2009913702712867_3187269214893717726_n.png?_nc_cat=111&ccb=1-7&_nc_sid=f537c7&_nc_ohc=uCZOs2E3c90Q7kNvwF7SzMb&_nc_oc=AdoR23qJ3Fi-nDjJdHAHx6lvkkCqEhkP1wtXcvoCXW_7RBwb1L7jle215v7fhiJPJU7af72-wZJa93fWOdvmdLDz&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8gSMCtOcGzm7kBVSnLk187w9DVC9O84AqPqNVK9h38sg&oe=6A38AE92)

As with all cutting edge technology, Code Llama comes with risks. Building AI models responsibly is crucial, and we undertook numerous safety measures before releasing Code Llama. As part of our red teaming efforts, we ran a quantitative evaluation of Code Llama’s risk of generating malicious code. We created prompts that attempted to solicit malicious code with clear intent and scored Code Llama’s responses to those prompts against ChatGPT’s (GPT3.5 Turbo). Our results found that Code Llama answered with safer responses.

Details about our red teaming efforts from domain experts in responsible AI, offensive security engineering, malware development, and software engineering are available in our [research paper](https://ai.meta.com/research/publications/code-llama-open-foundation-models-for-code/).

## Releasing Code Llama

Programmers are already using LLMs to assist in a variety of tasks, ranging from writing new software to debugging existing code. The goal is to make developer workflows more efficient, so they can focus on the most human centric aspects of their job, rather than repetitive tasks.

At Meta, we believe that AI models, but LLMs for coding in particular, benefit most from an open approach, both in terms of innovation and safety. Publicly available, code-specific models can facilitate the development of new technologies that improve peoples' lives. By releasing code models like Code Llama, the entire community can evaluate their capabilities, identify issues, and fix vulnerabilities.

Code Llama’s training recipes are available on our [Github repository](https://github.com/facebookresearch/codellama).

[Model weights](https://ai.meta.com/llama/) are also available.

## Responsible use

Our [research paper](https://ai.meta.com/research/publications/code-llama-open-foundation-models-for-code/) discloses details of Code Llama’s development as well as how we conducted our benchmarking tests. It also provides more information into the model’s limitations, known challenges we encountered, mitigations we’ve taken, and future challenges we intend to investigate.

We’ve also updated our [Responsible Use Guide](https://ai.meta.com/llama/responsible-use-guide/) and it includes guidance on developing downstream models responsibly, including:

* Defining content policies and mitigations.
* Preparing data.
* Fine-tuning the model.
* Evaluating and improving performance.
* Addressing input- and output-level risks.
* Building transparency and reporting mechanisms in user interactions.

Developers should evaluate their models using code-specific evaluation benchmarks and perform safety studies on code-specific use cases such as generating malware, computer viruses, or malicious code. We also recommend leveraging safety datasets for automatic and human evaluations, and red teaming on [adversarial prompts](https://ai.meta.com/blog/facebooks-five-pillars-of-responsible-ai/).

## The future of generative AI for coding

Code Llama is designed to support software engineers in all sectors – including research, industry, open source projects, NGOs, and businesses. But there are still many more use cases to support than what our base and instruct models can serve.

We hope that Code Llama will inspire others to leverage Llama 2 to create new innovative tools for research and commercial products.

Try Code Llama today

[Code Llama GitHub repository](https://github.com/facebookresearch/codellama)

[Download the Code Llama Model](https://ai.meta.com/resources/models-and-libraries/llama-downloads/)

Read the research paper

[Code Llama: Open foundation models for code](https://ai.meta.com/research/publications/code-llama-open-foundation-models-for-code/)

---

Share:

---

Our latest updates delivered to your inbox

[Subscribe](https://ai.facebook.com/subscribe/) to our newsletter to keep up with Meta AI news, events, research breakthroughs, and more.

Join us in the pursuit of what’s possible with AI.

[See all open positions](https://www.metacareers.com/jobs/?is_leadership=0&sub_teams%5B0%5D=Artificial+Intelligence&is_in_page=0&fbclid=IwAR0O8BF7opOj5gASJmwYVGalPPXTLu-6xrl9w00eC7Rarp2HQ9uEH8tERFw)

Related Posts

FEATURED

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/361917710_291784043360251_714121493924052728_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=KjXvIeEcs1UQ7kNvwG4CxFO&_nc_oc=AdrrEoLEIVzFBDVvycQTUqS3oISfyTnEdoBv1U6hdWU8ucqM9LpkdPGEFfSuUfAF9tbq8xseONSmkc65Av4B05_L&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af-LBAFQfefWNfqEdoOczzjRB1xEoZFb_bE44mLH8LDsig&oe=6A4D07CA)

Research

Meta and Microsoft Introduce the Next Generation of Llama

July 18, 2023

[Read post](https://ai.meta.com/blog/llama-2/)

FEATURED

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/355350269_735396441693973_7081320402844920765_n.png?_nc_cat=111&ccb=1-7&_nc_sid=e280be&_nc_ohc=mYOz6bL-yVUQ7kNvwGaP8dV&_nc_oc=Adrq2uaoHs8wYdaUeiycIXNseYkjCJ5JDesswIXKcxFTCNVMsIbp6lN5GktnuFV-CS9VJwt8avq-bUOyCP-udNO-&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8UxoEgdAXG5Gc043Ivu7kpVvTQJG1WQyMR2z6aI-T7MQ&oe=6A4D29EF)

Research

Introducing CM3leon, a more efficient, state-of-the-art generative model for text and images

July 14, 2023

[Read post](https://ai.meta.com/blog/generative-ai-text-images-cm3leon/)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.2365-6/361944785_562462122573647_2190435326701700877_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=e280be&_nc_ohc=GPy9J9MWPvcQ7kNvwHE5AET&_nc_oc=Adr_9IqiSlqu0h5R3g2i2HOYIiCY1heejzoRQcsnXVM9BHj5xsl_LRK2E1N_rNwIrzvuwr9zwKRsgM36NK4jrh6B&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8QutnSJSzMHauCD93GEtKFnn6kcFZAKyTOFZsgNvHNTg&oe=6A4D34FE)

Large Language Model

Community-driven AI innovation comes alive with Llama 2

July 28, 2023

[Read post](https://ai.meta.com/blog/llama-2-update/)

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

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/87524316_2677189655726266_6338721200264445952_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=C2HG24npvwYQ7kNvwHAH2e6&_nc_oc=AdpCJux6uVmKYiat2kni8-jXETldtNNT6zRuQYhCPWFAQZXQzDv1XnEXXoGgyKDUyxwqvMuGiqHz5zPbQthevbcb&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af9HenwTr7Ax9u7c2-Bm4eU4MzTC6F6iW-sZXqWDD4GaCA&oe=6A4D2878)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.2365-6/85559716_2814260008668824_1992323131183726592_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=bJOdWS-UzpEQ7kNvwG2QCqT&_nc_oc=Adot26PGLpuEp86kgNfqvX9udx3OARf23IRm1_Tso_lTXeQQs-p-vWN-EysvsbJ3QOE2oCOJHp-HEkEYsrPUFhdn&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af8alBnJjVXQ0im9I9owuTjwcYDIPyIZ5OAO4OIJgFDf4A&oe=6A4D2D4F)

[![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwFi_027&_nc_oc=AdoD_VI539zTt7tAZA22gJewiGThmzL_FhCn9un2BvXM_jMy8bKiHrsNfhvDh5BulzuTDN-NwypjfhIfBoUqHDlO&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af9GNAaksN4PolY5_zJWGj7pta4580Uuz4LlQ05ZCFQ6qQ&oe=6A38AEE7)

![](https://scontent-sea1-1.xx.fbcdn.net/v/t39.8562-6/335682312_964107378293184_3093631164486164913_n.svg?_nc_cat=100&ccb=1-7&_nc_sid=e280be&_nc_ohc=334gruP3Po8Q7kNvwFi_027&_nc_oc=AdoD_VI539zTt7tAZA22gJewiGThmzL_FhCn9un2BvXM_jMy8bKiHrsNfhvDh5BulzuTDN-NwypjfhIfBoUqHDlO&_nc_zt=14&_nc_ht=scontent-sea1-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af9GNAaksN4PolY5_zJWGj7pta4580Uuz4LlQ05ZCFQ6qQ&oe=6A38AEE7)](https://www.facebook.com/aiatmeta/)

[![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwHnCq6X&_nc_oc=AdpYj833LUmFcjRZRQZKBXuHSbUAXanosUko6WXylxh2OHVMrJJXbs2xBgxKY-4t07uS2qypJLxP5n8FwXMs81YM&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=x6y-F3y-xTl4Kr3ll0kHGA&_nc_ss=7b289&oh=00_Af_Wdwgv13QkMXb44f-Hg4A5_LuVmq8rPseAJW7sWHjs1A&oe=6A38A722)

![](https://scontent-sea5-1.xx.fbcdn.net/v/t39.8562-6/336009607_1870102080040414_6753977241281150924_n.svg?_nc_cat=103&ccb=1-7&_nc_sid=e280be&_nc_ohc=Uz5aTvCq4qkQ7kNvwHnCq6X&_nc_oc=AdpYj833LUmFcjRZRQZKBXuHSbUAXanosUko6WXylxh2OHVMrJJXbs2xBgxKY-4t07uS2qypJLxP5n8FwXMs81YM&_nc_zt=14&_nc_ht=scontent-sea5-1.xx&_nc_gid=

[truncated]
