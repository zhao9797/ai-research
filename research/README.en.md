> 🌐 English entry page. Deep pages are in Chinese. 中文版 / Chinese: [README.md](README.md)

# research/ — Research Analysis

Two independent scopes, **isomorphically organized** (both follow the "four-layer reading model" below). This is the navigation page; for actual content, go into each scope's `00-SUMMARY.md`.

| scope | Theme | Span | Scale | Entry |
|---|---|---|---|---|
| [`llm/`](llm/) | LLM technology evolution (pretraining data / architecture / AI infra / post-training / agentic) | GPT-3 2020-05 → 2026-06 | **525+** primary sources | [00-SUMMARY](llm/00-SUMMARY.md) · [01-INDEX](llm/01-INDEX.md) |
| [`omni/`](omni/) | Multimodal/omni-modal generation (text-to-image / editing / unified understanding-and-generation / any-to-any omni / video / audio / 3D / enabling methods) | 2020 → 2026-H1 | **324 work pages / ~322 sources** | [00-SUMMARY](omni/00-SUMMARY.md) · [01-INDEX](omni/01-INDEX.md) |

## Structure of Each Scope

```
<scope>/
├── 00-SUMMARY.md     # Main summary: storyline overview + statistics + reading guide (read this first)
├── 01-INDEX.md       # Full source index: grouped by year/month, each with original URL, clickable
├── 2020/ … 2026/     # Per-work structured pages (one work per file, kebab-case slug)
├── sections/         # Cross-cutting categorical/topical summaries
└── deep-dive/        # Cross-cutting deep-dive comparisons of models or families
```

## Four-Layer Reading Model (from "conclusion" to "primary source")

1. **`00-SUMMARY.md`** — for the storyline and reading guide, read just this page.
2. **`sections/` · `deep-dive/`** — for a cross-cutting comparison of a topic (architecture evolution, training methods, benchmarks…) or a family (SD-FLUX, Qwen, unified omni…).
3. **`01-INDEX.md`** — to browse all entries along the timeline and find the original link for a given entry.
4. **`<year>/<slug>.md`** — for the six-dimension close reading of a single work (data / training / architecture / benchmark / infra + innovation/impact); its **downloaded primary source** is in `../sources/<scope>/<year>/`.

## Page Conventions

- Each page begins with a YAML frontmatter (`title / org / country / date / type / category / url / …`).
- The body uses Obsidian-style `[[slug]]` internal links to cross-reference pages (slug = filename without `.md`).
- Per-work pages share a uniform six-dimension structure; all numbers come from primary sources and are checked via adversarial verification.

## Maintenance

After source pages are added or removed, refresh using scripts under `self-wiki/scripts/tmp/`:
- `build_index.py` / `build_index_omni.py` — regenerate the corresponding scope's `01-INDEX.md` from each page's frontmatter
- `normalize_wikilinks.py` — normalize omni internal-link aliases (e.g. `[[dit]]`→`[[dit-scalable-diffusion-transformers]]`)
- `fix_frontmatter.py` — fix YAML (multiple fields crammed on one line / scalars containing colons not quoted)
