# AudioLM project / examples page
source: https://google-research.github.io/seanet/audiolm/examples/

AudioLM
AudioLM
A Language Modeling Approach to Audio Generation
|
paper
|
blog post
|
Zalán Borsos, Raphaël Marinier, Damien Vincent, Eugene Kharitonov,
Olivier Pietquin, Matt Sharifi, Dominik Roblek, Olivier Teboul, David Grangier, Marco
Tagliasacchi, Neil Zeghidour
Google Research
Abstract.
We introduce AudioLM, a framework for high-quality
audio generation with long-term consistency. AudioLM maps the input
audio to a sequence of discrete tokens and casts audio generation as a
language modeling task in this representation space. We show how
existing audio tokenizers provide different trade-offs between
reconstruction quality and long-term structure, and we propose a hybrid
tokenization scheme to achieve both objectives. Namely, we leverage the
discretized activations of a masked language model pre-trained on audio
to capture long-term structure and the discrete codes produced by a
neural audio codec to achieve high-quality synthesis. By training on
large corpora of raw audio waveforms, AudioLM learns to generate natural
and coherent continuations given short prompts. When trained on speech,
and without any transcript or annotation, AudioLM generates
syntactically and semantically plausible speech continuations while also
maintaining speaker identity and prosody for unseen speakers.
Furthermore, we demonstrate how our approach extends beyond speech by
generating coherent piano music continuations, despite being trained
without any symbolic representation of music.
Speech continuation
Continuations using 3 second prompts from LibriSpeech test-{clean,
other}, for speakers and content not seen during training. AudioLM
excels at generating continuations that:
preserve speaker identity, prosody, accent and recording conditions of
the prompt,
have syntactically correct and semantically coherent content.
Librispeech test-clean
Original
Prompt
Continuations
1
2
3
4
5
Librispeech test-other
Original
Prompt
Continuations
1
2
Acoustic generation
For acoustic generation, we sample the acoustic tokens given the
semantic tokens extracted from the original samples from LibriSpeech
test-clean. The model generates samples with different speakers and
recording conditions, while the semantic content is identical.
Original
Acoustic generation (stage 2 and 3)
1
2
3
4
5
Unconditional generation
The unconditional generation performs sampling without using prompts. In
that case, every sequence varies in speaker identity, linguistic
content, and recording conditions.
Samples from unconditional generation
Generation without semantic tokens
To illustrate that the semantic tokens are crucial for generating
coherent linguistic content, we train the language model on the acoustic
tokens only. While the generated continuations of the 4-second prompts
maintain speaker identity, the linguistic content is inconsistent, and
often akin to babbling.
Continuations with a language model trained on the acoustic
tokens only (without semantic tokens)
Comparing SoundStream reconstructions
We compare SoundStream reconstructions of two models, one using 3-layer
residual vector quantization (3-RVQ) and another with 12 layers
(12-RVQ), the latter being the default. The equivalent bitrates are 1.5
kbps and 6 kbps.
Original
SoundStream 3-RVQ
SoundStream 12-RVQ
1
2
Piano continuation
AudioLM is not limited to modeling speech. It can also learn to generate
coherent piano music continuations, despite being trained on piano music
without any symbolic representation. We also show the continuations
produced by a version of the model trained exclusively on the acoustic
tokens. These continuations are much less coherent, stressing the
importance of the semantic tokens in our framework. The 4-second prompts
come from the test split of
MAESTRO
dataset.
Original
Prompt
Continuation by acoustic-only model
Continuation by AudioLM