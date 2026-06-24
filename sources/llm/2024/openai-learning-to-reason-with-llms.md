# 学习利用 LLM 进行推理 | OpenAI
Source: https://openai.com/zh-Hans-CN/index/learning-to-reason-with-llms/
学习利用 LLM 进行推理 | OpenAI

[跳至主要内容](#main)

* [研究](/zh-Hans-CN/research/index/)
* 产品
* [企业](/zh-Hans-CN/business/)
* [开发人员](/zh-Hans-CN/api/)
* [公司](/zh-Hans-CN/about/)
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

登录[试用 ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=0e165523-a07c-4552-86a6-ee7210a54fc8&openaicom_referred=true)

* 研究
* 产品
* 企业
* 开发人员
* 公司
* [基金会（在新窗口中打开）](https://openaifoundation.org/zh-Hans-CN/)

学习利用 LLM 进行推理 | OpenAI

2024年9月12日

[发布](/research/index/release/)

# 学习利用 LLM 进行推理

我们正在引入 OpenAI o1，这是一种通过强化学习训练出来的新型大型语言模型，可以执行复杂的推理。o1 在回答问题之前会先思考——它可以在回应用户之前产生很长的内部思考链。

[贡献](/zh-Hans-CN/openai-o1-contributions/)[使用 o1（在新窗口中打开）](https://chatgpt.com/?openaicom-did=0e165523-a07c-4552-86a6-ee7210a54fc8&openaicom_referred=true)

评估

* [评估](#ping-gu)
* [思维链](#si-wei-lian)
* [编码](#bian-ma)
* [人类偏好评估](#ren-lei-pian-hao-ping-gu)
* [安全](#an-quan)
* [隐藏思维链](#yin-cang-si-wei-lian)
* [结论](#jie-lun)
* [附录 A](#fu-lu-a)

目录

* [评估](#ping-gu)
* [思维链](#si-wei-lian)
* [编码](#bian-ma)
* [人类偏好评估](#ren-lei-pian-hao-ping-gu)
* [安全](#an-quan)
* [隐藏思维链](#yin-cang-si-wei-lian)
* [结论](#jie-lun)
* [附录 A](#fu-lu-a)

OpenAI o1 在编程竞赛题 (Codeforces) 中排名第 89 位，在美国数学奥林匹克竞赛 (AIME) 预选赛中跻身全美前 500 名学生行列，在物理、生物和化学问题 (GPQA) 基准测试中的准确率超过了人类博士水平。虽然使这一新模型与当前模型一样易于使用的工作仍在进行中，但我们已发布了该模型的早期版本 OpenAI o1‑preview，供 ChatGPT 和[可信 API 用户⁠（在新窗口中打开）](https://platform.openai.com/docs/guides/rate-limits/usage-tiers)立即使用。

我们的大规模强化学习算法在一个数据效率极高的训练过程中，教会模型如何利用其思维链进行富有成效的思考。我们发现，随着强化学习（训练时间计算）和思考时间（测试时间计算）的增加，o1 的性能也在不断提高。这种方法的扩展限制与 LLM 预训练的限制有很大不同，我们正在继续研究。

![图中显示了两张散点图，分别比较了训练时和测试时的“o1 AIME 精度”。两个图表的 y 轴均为“pass@1 准确度”，x 轴为计算量（对数标度）。点表示计算时间越长，准确率越高。](https://images.ctfassets.net/kftzwdyauwt9/3OO9wpK8pjcdemjd7g50xk/5ec2cc9d11f008cd754e8cefbc1c99f5/compute.png?w=3840&q=90&fm=webp)

o1 性能随着训练时间和测试时间计算量的增加而平稳提高

## 评估

为了突出与 GPT‑4o 相比的推理改进，我们在一组不同的人类考试和 ML 基准上测试了我们的模型。结果表明，在绝大多数推理繁重的任务中，o1 的表现明显优于 GPT‑4o。除非另有说明，我们在最大测试时间计算设置上对 o1 进行了评估。

![竞赛数学评估 (AIME 2024)](https://cdn.openai.com/reasoning-evals/v3/headline-mobile-0.png?w=3840&q=90&fm=webp)![竞赛数学评估 (AIME 2024)](https://cdn.openai.com/reasoning-evals/v3/headline-mobile-0-dark.png?w=3840&q=90&fm=webp)

![竞赛代码（CodeForces）](https://cdn.openai.com/reasoning-evals/v3/headline-mobile-1.png?w=3840&q=90&fm=webp)![竞赛代码（CodeForces）](https://cdn.openai.com/reasoning-evals/v3/headline-mobile-1-dark.png?w=3840&q=90&fm=webp)

![博士级科学问题 (GPQA Diamond)](https://cdn.openai.com/reasoning-evals/v3/headline-mobile-2.png?w=3840&q=90&fm=webp)![博士级科学问题 (GPQA Diamond)](https://cdn.openai.com/reasoning-evals/v3/headline-mobile-2-dark.png?w=3840&q=90&fm=webp)

o1 在挑战性推理基准测试中比 GPT-4o 有了很大改进。实线表示 pass@1 准确率，阴影区域表示 64 个样本的多数投票（共识）表现。

![数学竞赛评估 (AIME 2024)、代码竞赛评估 (CodeForces) 以及博士级科学问题竞赛评估 (GPQA Diamond)](https://cdn.openai.com/reasoning-evals/v3/headline-desktop.png?w=3840&q=90&fm=webp)![数学竞赛评估 (AIME 2024)、代码竞赛评估 (CodeForces) 以及博士级科学问题竞赛评估 (GPQA Diamond)](https://cdn.openai.com/reasoning-evals/v3/headline-desktop-dark.png?w=3840&q=90&fm=webp)

o1 在挑战性推理基准测试中比 GPT-4o 有了很大改进。实线表示 pass@1 准确率，阴影区域表示 64 个样本的多数投票（共识）表现。

![GPT-4o 与 o1 在各种竞赛评估中的准确率和原始分数详细分析](https://cdn.openai.com/reasoning-evals/v3/breakdown.png?w=3840&q=90&fm=webp)![GPT-4o 与 o1 在各种竞赛评估中的准确率和原始分数详细分析](https://cdn.openai.com/reasoning-evals/v3/breakdown-dark.png?w=3840&q=90&fm=webp)

o1 在广泛基准测试中比 GPT-4o 有所改进，包括 54/57 MMLU 子类别。图中显示了七个。

![GPT-4o 对比 o1 的机器学习基准测试与考试成绩提升数据（顶部显示），移动设备替代文本](https://cdn.openai.com/reasoning-evals/v3/breakdown-mobile-left.png?w=3840&q=90&fm=webp)![GPT-4o 对比 o1 的机器学习基准测试与考试成绩提升数据（顶部显示），移动设备替代文本](https://cdn.openai.com/reasoning-evals/v3/breakdown-mobile-left-dark.png?w=3840&q=90&fm=webp)

![博士级科学问题（GPQA Diamond）和 MMLU 类别分数，移动设备替代文本](https://cdn.openai.com/reasoning-evals/v3/breakdown-mobile-right.png?w=3840&q=90&fm=webp)![博士级科学问题（GPQA Diamond）和 MMLU 类别分数，移动设备替代文本](https://cdn.openai.com/reasoning-evals/v3/breakdown-mobile-right-dark.png?w=3840&q=90&fm=webp)

o1 在广泛基准测试中比 GPT-4o 有所改进，包括 54/57 MMLU 子类别。图中显示了七个。

在许多推理繁重的基准测试中，o1 的表现可以与人类专家相媲美。最近的前沿模型[1](#citation-bottom-1)在 MATH[2](#citation-bottom-2)和 GSM8K 中表现出色，以至于这些基准不再能有效区分模型。我们评估了 AIME 考试的数学成绩，该考试旨在挑战美国最聪明的高中数学学生。在 2024 年的 AIME 考试中，GPT‑4o 平均只解决了 12% 的问题 (1.8/15)。o1 在每个问题只有一个样本的情况下平均得分 74% (11.1/15)，在 64 个样本达成共识的情况下平均得分 83% (12.5/15)，在使用学习的评分函数对 1000 个样本重新排序的情况下平均得分 93% (13.9/15)。13.9 的得分使它跻身全国前 500 名学生之列，并高于美国数学奥林匹克竞赛的分数线。

我们还在 GPQA 钻石级上对 o1 进行了评估，这是一项高难度的智力基准测试，测试化学、物理和生物方面的专业知识。为了将模型与人类进行比较，我们招募了拥有博士学位的专家来回答 GPQA 钻石级的问题。我们发现，o1 的表现超过了这些人类专家，成为第一个在这一基准测试中超过人类专家的模型。这些结果并不意味着 o1 在所有方面都比博士更有能力——只是说明该模型在解决博士有望解决的某些问题时更加熟练。在其他几项 ML 基准测试中，o1 的表现都超过了最先进的水平。在启用了视觉感知能力后，o1 在 MMMU 上的得分率达到了 78.2%，成为第一个能与人类专家竞争的模型。在 57 个 MMLU 子类别中，它还在 54 个类别上超过了 GPT‑4o。

## 思维链

与人类在回答难题之前可能会思考很长时间类似，o1 在尝试解决问题时也会使用思维链。通过强化学习，o1 可以学会磨练自己的思维链，并完善自己使用的策略。它学会识别和纠正错误。它学会把棘手的步骤分解成更简单的步骤。它学会在当前方法无效时尝试不同的方法。这一过程极大地提高了模型的推理能力。为了说明这一飞跃，我们在下面展示了 o1‑preview 在几个难题上的思维链。

密码编码数学填字游戏英语科学安全健康科学

## GPT-4o

用户

oyfjdnisdr rtqwainr acxz mynzbhhx -> Think step by step

Use the example above to decode:

oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz

Let’s break this down step by step based on the example:

**1. Example given:**• Input: oyfjdnisdr rtqwainr acxz mynzbhhx  
• Output: **Think step by step**

By examining the words:  
• The pattern involves selecting specific letters or transforming them.

**2. Now, let’s decode the new phrase:**• Input: oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz

**Step-by-step decoding process:**

**Identify possible word divisions.**

The first phrase might follow the same structure as the example. It seems like the input text could be broken into groups based on natural separations or patterns.

A possible division could be:

* oyekaijzdf
* aaptcg
* suaokybhai
* ouow
* aqht
* mynznvaatzacdfoulxxz

However, to make a meaningful decoding, I would need more context about the transformations or letter shifting that might be involved.

Could you provide any additional decoding rules or transformations used in this cipher?

## OpenAI o1-preview

用户

oyfjdnisdr rtqwainr acxz mynzbhhx -> Think step by step

Use the example above to decode:

oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz

已思考 5 秒

First, what is going on here?  
  
We are given:  
  
First, an example:  
  
"oyfjdnisdr rtqwainr acxz mynzbhhx -> Think step by step"  
  
We can see that when "oyfjdnisdr rtqwainr acxz mynzbhhx" is transformed to "Think step by step"  
  
Our task is: Use the example above to decode: "oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz"  
  
So the first part is to figure out how "oyfjdnisdr rtqwainr acxz mynzbhhx" is decoded into "Think step by step"  
  
Observation 1: The phrase "Think step by step" is 18 letters (excluding spaces) . Let's count the letters.  
  
Similarly, let's count the letters in "oyfjdnisdr rtqwainr acxz mynzbhhx"  
  
Original Ciphertext:  
  
oyfjdnisdr rtqwainr acxz mynzbhhx  
  
Plaintext:  
  
Think step by step  
  
First, break down the letters:  
  
Ciphertext letters: o y f j d n i s d r r t q w a i n r a c x z m y n z b h h x  
  
Total letters: Let's count the letters in the ciphertext.  
  
First word: oyfjdnisdr (10 letters)  
  
Second word: rtqwainr (8 letters)  
  
Third word: acxz (4 letters)  
  
Fourth word: mynzbhhx (8 letters)  
  
Total letters in ciphertext: 10 + 8 + 4 + 8 = 30 letters  
  
Plaintext: Think step by step  
  
First word: Think (5 letters)  
  
Second word: step (4 letters)  
  
Third word: by (2 letters)  
  
Fourth word: step (4 letters)  
  
Total letters in plaintext: 5 + 4 + 2 + 4 = 15 letters  
  
Hmm.  
  
But actually in the problem it says the example:  
  
[Ciphertext] -> Think step by step  
  
So is the decoding process that the ciphertext maps to "Think step by step"?  
  
Our goal is to use the example above to decode:  
  
"oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz"  
  
First, the cipher seems connected to the plaintext.  
  
Given the time constraints, perhaps the easiest way is to try to see patterns.  
  
Option 1: Try to find mapping from letters to letters.  
  
Do any letters match?  
  
First, let's write down the ciphertext and plaintext letters on top of each other.  
  
Ciphertext: o y f j d n i s d r r t q w a i n r a c x z m y n z b h h x  
  
Plaintext: T h i n k s t e p b y s t e p  
  
Wait a minute.  
  
I think maybe there is an anagram or substitution cipher here.  
  
Alternatively, I think that we can notice that each group of ciphertext corresponds to a plaintext word.  
  
Check the number of letters.  
  
First ciphertext word: oyfjdnisdr (10 letters)  
  
First plaintext word: Think (5 letters)  
  
Hmm.  
  
Second ciphertext word: rtqwainr (8 letters)  
  
Second plaintext word: step (4 letters)  
  
Third ciphertext word: acxz (4 letters)  
  
Third plaintext word: by (2 letters)  
  
Fourth ciphertext word: mynzbhhx (8 letters)  
  
Fourth plaintext word: step (4 letters)  
  
Interesting.  
  
It seems that the ciphertext words are exactly twice as long as the plaintext words.  
  
(10 vs 5, 8 vs 4, 4 vs 2, 8 vs 4)  
  
Idea: Maybe we need to take every other letter or rebuild the plaintext from the ciphertext accordingly.  
  
Let's test this theory.  
  
If we take every other letter from the ciphertext words, maybe we'll get the plaintext.  
  
Let's try this for the first word:  
  
Ciphertext word: o y f j d n i s d r (10 letters)  
  
Alternate letters:  
  
First letters (positions 1,3,5,7,9): o f d i d  
  
Second letters (positions 2,4,6,8,10): y j n s r  
  
Wait: Let's try taking every second letter or first letter.  
  
Option 1: Take the odd positions:  
  
Positions: 1 3 5 7 9  
  
Letters: o f d i d  
  
Plaintext word is "Think", letters are T h i n k  
  
Hmm.  
  
Perhaps we can map letters:  
  
o f d i d --> Think  
  
Not directly  
  
Option 2: Try mapping as per an assigned code: perhaps columns of letters?  
  
Alternatively, perhaps the cipher is more complex.  
  
Alternatively, notice that "oyfjdnisdr" has 10 letters and "Think" has 5 letters.  
  
What if each plaintext letter is being represented by two ciphertext letters?  
  
Similarly for other words.  
  
Suppose that each plaintext letter corresponds to pair of letters in the ciphertext.  
  
Meaning that the first two letters of ciphertext map to the first plaintext letter, and so on.  
  
So for the first word, partition the ciphertext letters into pairs:  
  
oy fj dn is dr  
  
Corresponding to plaintext letters T h i n k  
  
So we can attempt to map:  
  
oy -> T  
  
fj -> h  
  
dn -> i  
  
is -> n  
  
dr -> k  
  
If this is the mapping, perhaps each pair of letters maps to one plaintext letter.  
  
Similarly for other words.  
  
Let's test this mapping.  
  
Is there a consistent mapping from pairs to letters?  
  
Let's make a table of pairs and corresponding letters.  
  
First, make the pairs from the first word and their corresponding plaintext letters:  
  
Ciphertext Pairs -> Plaintext Letter  
  
oy -> T  
  
fj -> h  
  
dn -> i  
  
is -> n  
  
dr -> k  
  
Now, what's the mapping from "oy" to 'T'?  
  
Is there a way to map 'oy' to 'T'?  
  
Similarly for others.  
  
One possible way is that 'oy' represents 'T'.  
  
But how?  
  
Option 1: Sum of the letters.  
  
Convert letters to numbers (A=1, B=2, ..., Z=26)  
  
So let's try to get to 'T' from 'o' and 'y'  
  
o = 15  
  
y = 25  
  
Sum: 15 +25 = 40  
  
But 'T' is 20.  
  
Alternatively, perhaps subtract: 25 -15 = 10.  
  
No.  
  
Alternatively, perhaps combine the numbers in some way.  
  
Alternatively, think about their positions in the alphabet.  
  
Alternatively, perhaps the letters are encrypted via a code.  
  
Alternatively, perhaps if we overlay the word 'Think' over the cipher pairs 'oy', 'fj', etc., the cipher is formed by substituting each plaintext letter with two letters.  
  
Alternatively, perhaps consider the 'original' letters.  
  
Let's look at the letters between the word "Think" and "oyfjdnisdr"  
  
Perhaps we can spot that "oyfjdnisdr" is an anagram for "Thinkfiles"?  
  
But that seems unlikely.  
  
Alternatively, think of the pairs.  
  
Suppose we assign numbers to letters: a=1, b=2, ..., z=26  
  
Consider the numbers in 'oy':  
  
o = 15  
  
y = 25  
  
Add them: 15 + 25 = 40  
  
Now, for 'T' we have:  
  
'T' is number 20  
  
What if we take the sum of the cipher pair mod 26.  
  
15 +25 = 40  
  
Then 40 mod 26 = 14  
  
14 corresponds to 'N'  
  
Doesn't match.  
  
Alternatively, see if the cipher pairs correspond to something else.  
  
Alternatively, perhaps the pair 'oy' corresponds to 'T' via key.  
  
Alternatively, perhaps it's as simple as 'oy' is 'T'.  
  
But 'o' corresponds to 'T', subtracting 'o' ASCII code from 'T'.  
  
Now, let's think in terms of symmetric letters.  
  
Alternatively, perhaps we can spot that the letters correspond to the first letters of words.  
  
But perhaps an easier way is to look at the word positions.  
  
Alternatively, perhaps we can see that the ciphertext letters are offsets from the plaintext letters.  
  
So let's try to map the pairs to the plaintext letters.  
  
First pair 'oy' and plaintext letter 'T'  
  
Letter 'o' is 15, 'T' is 20  
  
Letter 'o' + 5 = 'T' (15 +5=20)  
  
But 'y' is 25, which is 5 letters after 'T' (20 +5=25)  
  
Interesting, seems that 'o' +5 = 'T'  
  
Similarly, 'y' +1 = 'Z', which is not 'T'.  
  
Alternatively, maybe the average of the two letters corresponds to 'T'  
  
(15 +25)/2 =20, which is 'T'  
  
Wait a minute, that seems promising.  
  
First pair: 'o' (15) + 'y' (25) = 40  
  
40 /2 =20  
  
20 corresponds to 'T'  
  
So perhaps the average of the letters in the pair corresponds to the plaintext letter.  
  
Let's check this with the second pair.  
  
Second pair: 'fj' corresponding to 'h'  
  
Letters 'f'=6, 'j'=10  
  
Sum: 6+10=16  
  
Average:16/2=8  
  
8 corresponds to 'h' (since 'h' is 8)  
  
Success!  
  
Third pair: 'dn' to 'i'  
  
'd'=4, 'n'=14  
  
Sum:4+14=18  
  
Average:18/2=9  
  
9 corresponds to 'i'(9='i')  
  
But 'i' is 9, so that seems off by 1.  
  
So perhaps we need to think carefully about letters.  
  
Wait, 18/2=9, 9 corresponds to 'I'  
  
So this works.  
  
Fourth pair: 'is' corresponding to 'n'  
  
'i'=9, 's'=19  
  
Sum:9+19=28  
  
Average:28/2=14  
  
14 corresponds to 'n'(14='N')  
  
Yes!  
  
Fifth pair: 'dr' corresponds to 'k'  
  
'd'=4, 'r'=18  
  
Sum:4+18=22  
  
Average:22/2=11  
  
11 corresponds to 'k'(11='K')  
  
Perfect!  
  
So our code is: For each pair, sum their numeric values, divide by 2, get the corresponding letter.  
  
Alternatively, the average of the numeric values of the letters corresponds to the plaintext letter.  
  
This seems to be a valid method.  
  
Now let's test this with the other words.  
  
Second word ciphertext: rtqwainr  
  
Ciphertext pairs:  
  
rt -> s  
  
qw -> ?  
  
ai -> ?  
  
nr -> ?  
  
Corresponding to plaintext letters 's', 't', 'e', 'p'  
  
So let's take the pairs:  
  
1. 'rt' corresponds to 's'  
  
r=18, t=20  
  
Sum:38  
  
Average:19  
  
19 corresponds to 's' (19='S')  
  
Good  
  
2. 'qw' corresponds to 't'  
  
q=17, w=23  
  
Sum:17+23=40  
  
Average:20  
  
20 corresponds to 't' (20='T')  
  
Good  
  
3. 'ai' corresponds to 'e'  
  
a=1, i=9  
  
Sum:10  
  
Average:5  
  
5 corresponds to 'e' (5='E')  
  
Good  
  
4. 'nr' corresponds to 'p'  
  
n=14, r=18  
  
Sum:32  
  
Average:16  
  
16 corresponds to 'p' (16='P')  
  
Perfect!  
  
Third word: acxz (4 letters)  
  
Plaintext word: 'by' (2 letters)  
  
Ciphertext pairs:  
  
a c  
  
x z  
  
Plaintext letters: 'b', 'y'  
  
First pair: 'a', 'c'  
  
a=1, c=3  
  
Sum:4  
  
Average:2  
  
2 corresponds to 'b'(2='B')  
  
Second pair: 'x' and 'z'  
  
x=24, z=26  
  
Sum:50  
  
Average:25  
  
25 corresponds to 'y'(25='Y')  
  
Yes!  
  
Fourth word: mynzbhhx (8 letters)  
  
Plaintext word: 'step' (4 letters)  
  
Ciphertext pairs:  
  
my  
  
nz  
  
bh  
  
hx  
  
Plaintext letters 's','t','e','p'  
  
First pair 'm','y'  
  
m=13, y=25  
  
Sum:38  
  
Average:19  
  
19 corresponds to 's'(19='S')  
  
Second pair: 'n','z'  
  
n=14, z=26  
  
Sum: 40  
  
Average:20  
  
20='t'  
  
Third pair: 'b','h'  
  
b=2, h=8  
  
Sum:10  
  
Average:5  
  
5='e'  
  
Fourth pair: 'h','x'  
  
h=8, x=24  
  
Sum:32  
  
Average:16  
  
16='p'  
  
Got it!  
  
Now, given this, we can decode the given message.  
  
Ciphertext to decode:  
  
"oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz"  
  
First, we need to divide into words.  
  
Given that the ciphertext in the example had words of length:  
  
-10 letters (5 pairs)  
-8 letters (4 pairs)  
-4 letters (2 pairs)  
-8 letters (4 pairs)  
  
Transported to plaintext words of:  
  
-5 letters  
-4 letters  
-2 letters  
-4 letters  
  
So perhaps in our supplied ciphertext, we need to divide the letters into words accordingly.  
  
Ciphertext: o y e k a i j z d f a a p t c g s u a o k y b h a i o u o w a q h t m y n z n v a a t z a c d f o u l x x z  
  
First, let's write the letters in order:  
  
1) oyekaijzdf (10 letters) -> word of 5 letters  
  
2) aaptcg (6 letters) -> word of 3 letters  
  
3) suaokybhai (10 letters) -> word of 5 letters  
  
4) ouow (4 letters) -> word of 2 letters  
  
5) aqht (4 letters) -> word of 2 letters  
  
6) mynznvaatzacdfoulxxz (22 letters) -> word of 11 letters  
  
Totals:  
  
So the letters are:  
  
First word: oyekaijzdf (10 letters = 5 pairs)  
  
Second word: aaptcg (6 letters=3 pairs)  
  
Third word: suaokybhai (10 letters=5 pairs)  
  
Fourth word: ouow (4 letters=2 pairs)  
  
Fifth word: aqht (4 letters=2 pairs)  
  
Sixth word: mynznvaatzacdfoulxxz (22 letters=11 pairs)  
  
So we can suppose that the plaintext words have lengths:  
  
1) 5 letters  
  
2) 3 letters  
  
3) 5 letters  
  
4) 2 letters  
  
5) 2 letters  
  
6)11 letters  
  
Now we can proceed to decode.  
  
First word: oyekaijzdf  
  
Divide into pairs:  
  
oy  
  
ek  
  
ai  
  
jz  
  
df  
  
So we can find the plaintext letters by averaging the numeric values of the letters in each pair.  
  
First pair: 'o','y'  
  
o=15, y=25  
  
Sum=40  
  
Average=20  
  
20='T'  
  
Second pair: 'e','k'  
  
e=5, k=11  
  
Sum=16  
  
Average=8  
  
8='H'  
  
Third pair: 'a','i'  
  
a=1, i=9  
  
Sum=10  
  
Average=5  
  
5='E'  
  
Fourth pair: 'j','z'  
  
j=10, z=26  
  
Sum=36  
  
Average=18  
  
18='R'  
  
Fifth pair: 'd','f'  
  
d=4, f=6  
  
Sum=10  
  
Average=5  
  
5='E'  
  
So the first word is 'T','H','E','R','E'  
  
So 'THERE'  
  
Second word: aaptcg  
  
Pairs:  
  
aa  
  
pt  
  
cg  
  
First pair: 'a','a'  
  
a=1, a=1  
  
Sum=2  
  
Average=1  
  
1='A'  
  
Second pair: 'p','t'  
  
p=16, t=20  
  
Sum=36  
  
Average=18  
  
18='R'  
  
Third pair: 'c','g'  
  
c=3, g=7  
  
Sum=10  
  
Average=5  
  
5='E'  
  
So second word: 'A','R','E'  
  
Third word: suaokybhai  
  
Pairs:  
  
su  
  
ao  
  
ky  
  
bh  
  
ai  
  
First pair: s=19, u=21  
  
Sum=40, Average=20  
  
20='T'  
  
Second pair: a=1, o=15  
  
Sum=16, Average=8  
  
8='H'  
  
Third pair: k=11, y=25  
  
Sum=36, Average=18  
  
18='R'  
  
Fourth pair: b=2, h=8  
  
Sum=10, Average=5  
  
5='E'  
  
Fifth pair: a=1, i=9  
  
Sum=10, Average=5  
  
5='E'  
  
Third word: 'T','H','R','E','E'  
  
Fourth word: ouow  
  
Pairs: ou, ow  
  
First pair: o=15, u=21  
  
Sum=36, Average=18  
  
18='R'  
  
Second pair: o=15, w=23  
  
Sum=38, Average=19  
  
19='S'  
  
Fourth word: 'R','S'  
  
Fifth word: aqht  
  
Pairs: a q, h t  
  
First pair: a=1, q=17  
  
Sum=18, Average=9  
  
9='I'  
  
Second pair: h=8, t=20  
  
Sum=28, Average=14  
  
14='N'  
  
Fifth word: 'I','N'  
  
Sixth word: mynznvaatzacdfoulxxz (22 letters: 11 pairs)  
  
Pairs:  
  
m y  
  
n z  
  
n v  
  
a a  
  
t z  
  
a c  
  
d f  
  
o u  
  
l x  
  
x z  
  
Let's list them properly.  
  
Wait, earlier I missed some letters there.  
  
Let's re-express the sixth word letters:  
  
m y n z n v a a t z a c d f o u l x x z  
  
Total letters: 22 letters  
  
Pairs:  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x x  
  
11. z  
  
Wait, that's 21 letters.  
  
But in total, we have 22 letters; I think I have a mismatch.  
  
Wait, in the problem the sixth word is:  
  
mynznvaatzacdfoulxxz  
  
Let's separate the letters:  
  
m y n z n v a a t z a c d f o u l x x z  
  
Total letters: 22 letters  
  
So pairs would be:  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x x  
  
11. z  
  
Wait, 'z' is only one letter at the end.  
  
So maybe the letters are:  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x x  
  
11. z (left alone?)  
  
But then we're missing a letter.  
  
Alternatively, perhaps the 'z' at the end is an extra letter or it's paired with the previous 'x'.  
  
Alternatively, perhaps there is a mistake.  
  
Alternatively, perhaps when we reach the last 'x x z', we should write:  
  
9. l x  
  
10. x z  
  
Total pairs: 11  
  
So updated pairs:  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x z  
  
Now total pairs: 10 pairs. But we are supposed to have 11 letters in the plaintext word.  
  
So perhaps I have miscounted and not considered including 'f' or 'z'.  
  
Wait, is there any chance that the sequence is:  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x x  
  
11. z  
  
We have 22 letters.  
  
Perhaps the 'x x' and 'z' are overlapping.  
  
But we need 11 pairs.  
  
I think for this to work, we need to create 11 pairs from the 22 letters.  
  
So let's try pairing letters in order, taking two letters at a time.  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x x  
  
11. z ?  
  
But again, last pair only has one letter 'z'  
  
Alternatively, we might need to adjust the pairs.  
  
Perhaps it's 'ou', 'lx', 'xz', and there is no extra 'x'.  
  
Maybe I miswrote.  
  
Wait, let's write the letters as they come:  
  
m y n z n v a a t z a c d f o u l x x z  
  
Positions:  
  
1 m  
  
2 y  
  
3 n  
  
4 z  
  
5 n  
  
6 v  
  
7 a  
  
8 a  
  
9 t  
  
10 z  
  
11 a  
  
12 c  
  
13 d  
  
14 f  
  
15 o  
  
16 u  
  
17 l  
  
18 x  
  
19 x  
  
20 z  
  
So 20 letters.  
  
Now that makes sense.  
  
Now we can divide into pairs:  
  
Pairs:  
  
1. m y  
  
2. n z  
  
3. n v  
  
4. a a  
  
5. t z  
  
6. a c  
  
7. d f  
  
8. o u  
  
9. l x  
  
10. x z  
  
Total of 10 pairs, which will correspond to 10 letters.  
  
But earlier we thought the word was 11 letters.  
  
But 10 letters may be acceptable.  
  
Maybe we should proceed with the 10 pairs.  
  
First pair: m y  
  
m=13, y=25  
  
Sum=38  
  
Average=19  
  
19='S'  
  
Second pair: n z  
  
n=14, z=26  
  
Sum=40  
  
Average=20  
  
20='T'  
  
Third pair: n v  
  
n=14, v=22  
  
Sum=36  
  
Average=18  
  
18='R'  
  
Fourth pair: a a  
  
a=1, a=1  
  
Sum=2  
  
Average=1  
  
1='A'  
  
Fifth pair: t z  
  
t=20, z=26  
  
Sum=46  
  
Average=23  
  
23='W'  
  
Sixth pair: a c  
  
a=1, c=3  
  
Sum=4  
  
Average=2  
  
2='B'  
  
Seventh pair: d f  
  
d=4, f=6  
  
Sum=10  
  
Average=5  
  
5='E'  
  
Eighth pair: o u  
  
o=15, u=21  
  
Sum=36  
  
Average=18  
  
18='R'  
  
Ninth pair: l x  
  
l=12, x=24  
  
Sum=36  
  
Average=18  
  
18='R'  
  
Tenth pair: x z  
  
x=24, z=26  
  
Sum=50  
  
Average=25  
  
25='Y'  
  
So the tenth word is 'S', 'T', 'R', 'A', 'W', 'B', 'E', 'R', 'R', 'Y'  
  
Wait that's 10 letters  
  
So the sixth word is 'STRAWBERRY', which makes sense.  
  
So putting all these translated letters together:  
  
First word: 'THERE'  
  
Second word: 'ARE'  
  
Third word: 'THREE'  
  
Fourth word: 'RS' (? Doesn't make sense)  
  
Wait, the fourth word, the pairs were:  
  
ou ow  
  
Pairs:  
  
First pair: o u  
  
o=15, u=21  
  
Sum=36, Average=18  
  
18='R'  
  
Second pair: o w  
  
o=15, w=23  
  
Sum=38, Average=19  
  
19='S'  
  
So we get 'R','S'  
  
Similarly, fifth word 'IN'  
  
'R', 'S' 'I','N'  
  
So the message so far is  
  
'THERE ARE THREE RS IN'  
  
And then 'STRAWBERRY'  
  
Wait, let's put the words together:  
  
'THERE ARE THREE Rs IN STRAWBERRY'  
  
I think 'RS' is 'R's', meaning 'Rs'  
  
So the message is:  
  
'THERE ARE THREE R'S IN STRAWBERRY'  
  
Which is true.  
  
So the decoded message is:  
  
"THERE ARE THREE R'S IN STRAWBERRY"

To decode the given ciphertext using the example provided, we’ll use the pattern identified in the example.

**Ciphertext Example:**

#### 纯文本

```` ```
1

oyfjdnisdr rtqwainr acxz mynzbhhx
``` ````

**Decoded as:**

#### 纯文本

```` ```
1

Think step by step
``` ````

**Decoding Method:**

1. **Pair the letters** in the ciphertext.
2. **Convert each letter to its numerical position** in the alphabet (A=1, B=2, …, Z=26).
3. **Sum the numerical values** of each pair.
4. **Compute the average** of the sum (divide by 2).
5. **Convert the average back to a letter** (1=A, 2=B, …, 26=Z).

**Apply this method to the given ciphertext:**

#### 纯文本

```` ```
1

oyekaijzdf aaptcg suaokybhai ouow aqht mynznvaatzacdfoulxxz
``` ````

**Break down the ciphertext into pairs:**

1. 1. **First word: “oyekaijzdf”**
   1. Pairs: oy, ek, ai, jz, df
   2. Decoded letters:
      1. oy → (15+25)/2 = 20 → T
      2. ek → (5+11)/2 = 8 → H
      3. ai → (1+9)/2 = 5 → E
      4. jz → (10+26)/2 = 18 → R
   3. df → (4+6)/2 = 5 → E
   4. Decoded word: **THERE**
2. **Second word: “aaptcg”**
   1. Pairs: aa, pt, cg
   2. Decoded letters:
      1. aa → (1+1)/2 = 1 → A
      2. pt → (16+20)/2 = 18 → R
      3. cg → (3+7)/2 = 5 → E
      4. Decoded word: **ARE**
3. **Third word: “suaokybhai”**
   1. Pairs: su, ao, ky, bh, ai
   2. Decoded letters:
      1. su → (19+21)/2 = 20 → T
      2. ao → (1+15)/2 = 8 → H
      3. ky → (11+25)/2 = 18 → R
      4. bh → (2+8)/2 = 5 → E
      5. ai → (1+9)/2 = 5 → E
   3. Decoded word: **THREE**
4. **Fourth word: “ouow”**
   1. Pairs: ou, ow
   2. Decoded letters:
      1. ou → (15+21)/2 = 18 → R
      2. ow → (15+23)/2 = 19 → S
   3. Decoded letters: **R’S**
5. **Fifth word: “aqht”**
   1. Pairs: aq, ht
   2. Decoded letters:
      1. aq → (1+17)/2 = 9 → I
      2. ht → (8+20)/2 = 14 → N
   3. Decoded word: **IN**
6. **Sixth word: “mynznvaatzacdfoulxxz”**
   1. Pairs: my, nz, nv, aa, tz, ac, df, ou, lx, xz
   2. Decoded letters:
      1. my → (13+25)/2 = 19 → S
      2. nz → (14+26)/2 = 20 → T
      3. nv → (14+22)/2 = 18 → R
      4. aa → (1+1)/2 = 1 → A
      5. tz → (20+26)/2 = 23 → W
      6. ac → (1+3)/2 = 2 → B
      7. df → (4+6)/2 = 5 → E
      8. ou → (15+21)/2 = 18 → R
      9. lx → (12+24)/2 = 18 → R
      10. xz → (24+26)/2 = 25 → Y
   3. Decoded word: **STRAWBERRY**

**Final Decoded Message:**

#### 纯文本

```` ```
1

THERE ARE THREE R'S IN STRAWBERRY
``` ````

**Answer:**THERE ARE THREE R’S IN STRAWBERRY

## 编码

我们训练了一个模型，该模型在 2024 年国际信息学奥林匹克竞赛 (IOI) 中获得了 213 分，排名第 49 位，训练方法是从 o1 开始初始化，通过训练进一步提高编程技能。该模型在与人类选手相同的条件下参加了 2024 年国际信息学奥林匹克竞赛。它有 10 个小时的时间来解决 6 个具有挑战性的算法问题，每个问题允许提交 50 次。

对于每个问题，我们的系统都会抽取许多候选方案，并根据测试时间选择策略提交其中的 50 个方案。我们根据 IOI 公开测试用例、模型生成的测试用例和学习的评分函数的表现来选择提交的问题。如果我们采用随机提交的方式，平均只能得到 156 分，这表明在竞争限制条件下，这种策略的价值接近 60 分。

放宽提交限制后，我们发现模型性能有了显著提高。当每个问题允许提交 10,000 个方案时，即使没有任何测试时间选择策略，模型也能获得 362.14 分，超过了金牌门槛。  

最后，我们模拟了由 Codeforces 主办的编程竞赛，以展示该模型的编码技能。我们的评估与竞赛规则密切相关，并允许提交 10 份作品。GPT‑4o 的 Elo 评分[3](#citation-bottom-3)达到 808，在人类选手中排名第 11 位。该模型远远超过了 GPT‑4o 和 o1——它的 Elo 评分达到 1807，优于 93% 的竞争对手。

![图片显示的是一个条形图，比较了不同模型的 Codeforces Elo 百分位数排名。GPT-4o 的 Elo 评分为 808（第 11 位），o1 预览版的 Elo 评分为 1258（第 62 位），o1 的 Elo 评分为 1673（第 89 位），o1-ioi 的 Elo 评分为 1807（第 93 位）。](https://images.ctfassets.net/kftzwdyauwt9/2A6QVjt4bIQo4XR7VEnhgq/892e593ed472562b300c71fe40116bc3/ioi-code.png?w=3840&q=90&fm=webp)

在编程竞赛中的进一步微调改进了 o1。根据竞赛规则，改进后的模型在 2024 年国际信息学奥林匹克竞赛中排名第 49 位。

## 人类偏好评估

除了考试和学术基准外，我们还评估了 o1‑preview 与 GPT‑4o 在广泛领域中具有挑战性的开放式提示上的人类偏好。在这项评估中，我们向人类训练师展示了 o1‑preview 和 GPT‑4o 的匿名提示回答，并让他们投票决定他们更喜欢哪种回答。在数据分析、编码和数学等偏重推理的类别中，o1‑preview 比 GPT‑4o 更受青睐。但是，o1‑preview 在一些自然语言任务中并不受欢迎，这表明它并不适合所有的使用情况。

![图中的横条形图比较了五个模型的得分，误差条代表置信区间。x 轴的范围从 0 到 100，虚线为性能参考点。](https://images.ctfassets.net/kftzwdyauwt9/7fCp1d7GJ0xkeVjL8mpCIv/71cd158887e4c0715112b26744e612fd/win_rate_matplotlib.png?w=3840&q=90&fm=webp)

## 安全

思维链推理为一致性和安全提供了新的机遇。我们发现，将我们的模型行为政策整合到推理模型的思维链中，是有力传授人类价值观和原则的有效方法。通过向模型传授我们的安全规则以及如何在上下文中对其进行推理，我们发现了推理能力直接有益于模型稳健性的证据：o1‑preview 在关键的越狱评估和用于评估模型安全拒绝边界的最难内部基准方面的性能得到了大幅提升。我们认为，使用思维链能显著提高安全性和一致性，因为：(1) 它能让我们以清晰的方式观察模型的思维；(2) 模型对安全规则的推理对分布外场景更加稳健。

为了对改进措施进行压力测试，我们在部署前根据我们的[准备框架⁠（在新窗口中打开）](https://cdn.openai.com/openai-preparedness-framework-beta.pdf)进行了一系列安全测试和红队测试。我们发现，在整个评估过程中，思维链推理有助于提高能力。特别值得注意的是，我们观察到了一些[有趣的奖励黑客行为⁠（在新窗口中打开）](https://cdn.openai.com/o1-system-card.pdf#page=16)。这些评估的详细结果见随附的[系统卡](/index/openai-o1-system-card/)。

| 评估指标 | GPT-4o | o1-preview |
| --- | --- | --- |
| 有害提示下安全生成内容的占比 % 标准 | 0.990 | 0.995 |
| 有害提示下安全生成内容的占比 % 挑战：越狱及边缘案例 | 0.714 | 0.934 |
| ↳ 骚扰（严重） | 0.845 | 0.900 |
| ↳ 剥削性内容 | 0.483 | 0.949 |
| ↳ 涉及未成年人的性内容 | 0.707 | 0.931 |
| ↳ 关于非暴力不当行为的建议 | 0.688 | 0.961 |
| ↳ 关于暴力不当行为的建议 | 0.778 | 0.963 |
| WildChat 中每类审核 API 得分最高的前 200 名安全生成率 % [赵等人2024 年](https://arxiv.org/abs/2405.01470) | 0.945 | 0.971 |
| Goodness@0.1 StrongREJECT 越狱评估 [苏利 (Souly) 等人2024 年](https://arxiv.org/abs/2402.10260) | 0.220 | 0.840 |
| 人工越狱评估 | 0.770 | 0.960 |
| 内部良性边缘案例的合规率 % “非过度拒绝” | 0.910 | 0.930 |
| XSTest 良性边缘案例合规率 % “非过度拒绝” [罗特格 (Röttger) 等人2023 年](https://arxiv.org/abs/2308.01263) | 0.924 | 0.976 |

## 隐藏思维链

我们认为，隐藏的思维链为监测模型提供了一个独特的机会。假设它是忠实可读的，那么隐藏的思维链就能让我们“读懂”模型的思想，了解它的思维过程。例如，将来我们可能希望监控思维链，以发现操纵用户的迹象。但是，要做到这一点，模型必须能够以不改变的形式自由表达自己的想法，因此我们不能在思维链上训练任何政策遵从或用户偏好。我们也不想让用户直接看到不一致的思维链。

因此，在权衡了用户体验、竞争优势以及对思维链进行监控的选项等多种因素后，我们决定不向用户显示原始思维链。我们承认这一决定存在弊端。我们努力通过教授模型在答案中重现思维链中任何有用的想法来部分弥补这一缺陷。在 o1 模型系列中，我们展示了模型生成的思维链摘要。

## 结论

o1 极大地推动了人工智能推理的发展。我们计划在继续迭代的过程中发布该模型的改进版本。我们希望这些新的推理能力能够提高我们使模型符合人类价值观和原则的能力。我们相信，o1 及其后续版本将为人工智能在科学、编码、数学和相关领域的应用带来许多新的应用案例。我们非常期待用户和 API 开发人员能够发现它如何改善他们的日常工作。

## 附录 A

| 数据集 | 评估指标 | gpt-4o | o1-preview | o1 |
| --- | --- | --- | --- | --- |
| 数学竞赛 AIME (2024) | cons@64 | 13.4 | 56.7 | 83.3 |
| 通过率@1 | 9.3 | 44.6 | 74.4 |
| 竞赛守则 CodeForces | Elo 评分 | 808 | 1,258 | 1,673 |
| 百分位数 | 11.0 | 62.0 | 89.0 |
| GPQA 钻石级 | cons@64 | 56.1 | 78.3 | 78.0 |
| 通过率@1 | 50.6 | 73.3 | 77.3 |
| 生物学 | cons@64 | 63.2 | 73.7 | 68.4 |
| 通过率@1 | 61.6 | 65.9 | 69.2 |
| 化学 | cons@64 | 43.0 | 60.2 | 65.6 |
| 通过率@1 | 40.2 | 59.9 | 64.7 |
| 物理 | cons@64 | 68.6 | 89.5 | 94.2 |
| 通过率@1 | 59.5 | 89.4 | 92.8 |
| 数学 | 通过率@1 | 60.3 | 85.5 | 94.8 |
| MMLU | 通过率@1 | 88.0 | 92.3 | 90.8 |
| MMMU (val) | 通过率@1 | 69.1 | n/a | 78.2 |
| MathVista（测试精简版） | 通过率@1 | 63.8 | n/a | 73.9 |

* [o1](/zh-Hans-CN/research/index/?tags=o1)
* [推理与政策](/zh-Hans-CN/research/index/?tags=reasoning-policy)
* [生成式模型](/zh-Hans-CN/research/index/?tags=generative-models)
* [语言](/zh-Hans-CN/research/index/?tags=language)

## 作者

OpenAI

[查看撰稿人](/zh-Hans-CN/openai-o1-contributions/)

## 引用

1. 1

   [https://www.anthropic.com/news/claude-3-5-sonnet⁠（在新窗口中打开）](https://www.anthropic.com/news/claude-3-5-sonnet)，[https://deepmind.google/technologies/gemini/pro⁠（在新窗口中打开）](https://deepmind.google/technologies/gemini/pro)
2. 2

   我们的评估使用了 [https://arxiv.org/abs/2305.20050⁠（在新窗口中打开）](https://arxiv.org/abs/2305.20050) 中相同的 500 个问题测试拆分。
3. 3

   [https://codeforces.com/blog/entry/68288⁠（在新窗口中打开）](https://codeforces.com/blog/entry/68288)

研究

* [研究索引](/zh-Hans-CN/research/index/)
* [研究概览](/zh-Hans-CN/research/)
* [经济研究](/zh-Hans-CN/signals/)

最新进展

* [GPT-5.5](/zh-Hans-CN/index/introducing-gpt-5-5/)
* [GPT-5.4](/zh-Hans-CN/index/introducing-gpt-5-4/)
* [GPT-5.3 Instant](/zh-Hans-CN/index/gpt-5-3-instant/)

安全

* [安全措施](/zh-Hans-CN/safety/)
* [部署安全（在新窗口中打开）](https://deploymentsafety.openai.com/)
* [安全与隐私](/zh-Hans-CN/security-and-privacy/)
* [信任与透明度](/zh-Hans-CN/trust-and-transparency/)

ChatGPT

* [ChatGPT（在新窗口中打开）](https://chatgpt.com/?openaicom-did=0e165523-a07c-4552-86a6-ee7210a54fc8&openaicom_referred=true)
* [ChatGPT Business（在新窗口中打开）](https://chatgpt.com/business/?openaicom-did=0e165523-a07c-4552-86a6-ee7210a54fc8&openaicom_referred=true)
* [ChatGPT Enterprise（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/enterprise/?openaicom-did=0e165523-a07c-4552-86a6-ee7210a54fc8&openaicom_referred=true)
* [ChatGPT for Education（在新窗口中打开）](https://chatgpt.com/zh-Hans-CN/business/education/?openaicom-did=0e165523-a07c-4552-86a6-ee7210a54fc8&openaicom_referred=true)
* [Codex](/zh-Hans-CN/codex/)
* [发布说明](/products/release-notes/)

API 平台

* [平台概览](/zh-Hans-CN/api/)
* [API 登录（在新窗口中打开）](https://platform.openai.com/login)
* [文档（在新窗口中打开）](https://developers.openai.com/api/docs)

Business

* [概览](/zh-Hans-CN/business/)
* [解决方案](/zh-Hans-CN/solutions/)
* [资源](/zh-Hans-CN/business/learn/)
* [联系销售团队](/zh-Hans-CN/contact-sales/)

开发者

* [Apps SDK（在新窗口中打开）](https://developers.openai.com/apps-sdk)
* [开放模型](/zh-Hans-CN/open-models/)
* [文档（在新窗口中打开）](https://developers.openai.com/)
* [资源（在新窗口中打开）](https://developers.openai.com/learn)
* [开发者论坛（在新窗口中打开）](https://community.openai.com/)

公司

* [关于我们](/zh-Hans-CN/about/)
* [我们的宪章](/charter/)
* [工作机会](/careers/)
* [新闻](/zh-Hans-CN/news/)

支持

* [帮助中心（在新窗口中打开）](https://help.openai.com/)

更多

* [客户案例](/zh-Hans-CN/stories/)
* [Academy](/academy/)
* [直播](/zh-Hans-CN/live/)
* [播客](/zh-Hans-CN/podcast/)
* [RSS](/news/rss.xml)

条款与政策

* [使用条款](/zh-Hans-CN/policies/terms-of-use/)
* [隐私政策](/zh-Hans-CN/policies/privacy-policy/)
* [其他政策](/zh-Hans-CN/policies/)

[（在新窗口中打开）](https://x.com/OpenAI)[（在新窗口中打开）](https://www.youtube.com/OpenAI)[（在新窗口中打开）](https://www.linkedin.com/company/openai)[（在新窗口中打开）](https://github.com/openai)[（在新窗口中打开）](https://www.instagram.com/openai/)[（在新窗口中打开）](https://www.tiktok.com/@openai)[（在新窗口中打开）](https://discord.gg/openai)

OpenAI © 2015–2026你的隐私选择

中文中国

![](https://bat.bing.com/action/0?ti=187204252&Ver=2&mid=058b1eb6-7101-4d73-9a5c-597ca62c702b&bo=1&sid=38aea5906a7011f1b2bf4fcc548d0b95&vid=38aecee06a7011f1a5a9e59f0b77fc11&vids=1&msclkid=N&pi=918639831&lg=zh-CN&sw=1440&sh=900&sc=24&tl=%E5%AD%A6%E4%B9%A0%E5%88%A9%E7%94%A8%20LLM%20%E8%BF%9B%E8%A1%8C%E6%8E%A8%E7%90%86%20%7C%20OpenAI&p=https%3A%2F%2Fopenai.com%2Fzh-Hans-CN%2Findex%2Flearning-to-reason-with-llms%2F&r=&lt=2392&evt=pageLoad&sv=2&cdb=AQAQ&rn=191314)
