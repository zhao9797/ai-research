# scripts/ — maintenance tooling

Standalone, dependency-free (Python 3 standard library only) tools for keeping
`research/` consistent. Run them from the repo root.

| script | what it does |
|---|---|
| `build_index.py` | Regenerate `research/llm/01-INDEX.md` from each page's frontmatter (group by `date` year, dedup by URL). |
| `build_index_omni.py` | Same for `research/omni/01-INDEX.md`. |
| `normalize_wikilinks.py` | Rewrite unambiguous `[[alias]]` links under `research/omni` to the real page slug. |
| `fix_frontmatter.py` | Repair YAML frontmatter under `research/` (split crammed lines, quote colon-bearing scalars); validates with PyYAML if installed. |
| `lint.py` | Read-only checks: missing/invalid frontmatter, accidental duplicate pages (same URL + same title within a scope), broken wikilinks, folder/date mismatches. Used by CI. |
| `templates/work-page.md` | Skeleton for a new per-work page (frontmatter + section structure). |

## Adding a new work page

1. Copy `templates/work-page.md` to `research/<scope>/<year>/<slug>.md`, fill it in.
   - `<slug>` is kebab-case; the folder `<year>` should match the page's `date` year.
   - `url:` is the dedup key — it must be unique within a scope.
2. Put the archived primary source under `sources/<scope>/<year>/` (PDFs/images are
   git-ignored; keep HTML/JSON/README sources in git).
3. Regenerate the index and lint:
   ```sh
   python3 scripts/build_index.py        # or build_index_omni.py for omni
   python3 scripts/lint.py
   ```
4. Commit the page and the regenerated `01-INDEX.md` together. CI re-runs the lint
   and verifies the index is up to date.
