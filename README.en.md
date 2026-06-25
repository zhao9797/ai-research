> 🌐 English entry page. Deep pages are in Chinese. 中文版 / Chinese: [README.md](README.md)

# ai-research

A personal AI technology research repository — **primary official sources only** (original arXiv papers / official technical reports / system cards / official blogs / official GitHub · HF · ModelScope model cards), with no third-party interpretations, translations, or secondary aggregations.

Every work is read closely along a unified set of dimensions (**data · training methods · model architecture · benchmark evaluation · infra** + innovation/impact), and **all numbers are checked line-by-line against primary sources via adversarial verification** (no dropped/misattributed/fabricated figures).

---

## Two Research Tracks

### 📚 [`research/llm/`](research/llm/) — Large Language Model Technology Evolution (GPT-3 2020-05 → 2026-06)
- **525+** primary sources after deduplication; five categories: **pretraining data · architecture · AI infra · post-training · agentic training**
- Entry → [`research/llm/00-SUMMARY.md`](research/llm/00-SUMMARY.md)　·　Full index → [`research/llm/01-INDEX.md`](research/llm/01-INDEX.md)
- Categorical summaries `sections/`　·　Open-source model deep dives `deep-dive/`

### 🎨 [`research/omni/`](research/omni/) — Multimodal / Omni-Modal "Generation" Evolution (2020 → 2026-H1)
- **324 work pages / ~322** primary sources; covering **text-to-image · image editing · unified understanding-and-generation · any-to-any omni · video · audio · 3D · enabling methods**
- Entry → [`research/omni/00-SUMMARY.md`](research/omni/00-SUMMARY.md)　·　Full index → [`research/omni/01-INDEX.md`](research/omni/01-INDEX.md)
- 6 cross-cutting chapters `sections/` (architecture / data / training / benchmark / infra / unified-omni topic)　·　5 model families `deep-dive/` (SD-FLUX lineage / Chinese T2I / unified omni / video / editing)

> For how each scope is organized and "how to read" it, see [`research/README.md`](research/README.md).

---

## Directory Structure

```
ai-research/
├── research/<scope>/      # Analysis (the part you read)
│   ├── 00-SUMMARY.md      #   Main summary (read this first)
│   ├── 01-INDEX.md        #   Full source index (by year/month, with each original URL)
│   ├── 2020/ … 2026/      #   Per-work structured pages (six-dimension close reading)
│   ├── sections/          #   Cross-cutting categorical summaries
│   └── deep-dive/         #   Cross-cutting deep dives by model / family
└── sources/<scope>/       # Raw materials (archived to disk)
    └── 2020/ … 2026/      #   *.md/*.html blog snapshots (in git) + *.pdf (on HF bucket)
```

## Storage-Compute Separation

- **In git**: `*.md` / `*.html` / `*.json` (official blog · model card snapshots — small, prone to going stale, worth versioning)
- **Not in git**: `*.pdf` (several GB, original papers/technical reports) + large images `*.png/*.jpg` — backed up in the **HuggingFace private Storage Bucket** `hf://buckets/jaczhao/ai-research-sources/<scope>`, and can also be re-downloaded from each entry's arXiv/official URL in `01-INDEX.md`. See [`sources/README.md`](sources/README.md).

## How to Read (four layers from "conclusion" to "primary source")

1. **Main summary** `00-SUMMARY.md` — quick overview of the storyline + statistics + reading guide
2. **Cross-cutting chapters / deep dives** `sections/` · `deep-dive/` — cross-cutting comparison by topic or family
3. **Full index** `01-INDEX.md` — every entry clickable, by year/month
4. **Per-work page** `<year>/<slug>.md` — six-dimension close reading; the **primary source** is in `sources/<scope>/<year>/`
