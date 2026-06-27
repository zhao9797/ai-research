#!/usr/bin/env python3
"""Lint the research/ knowledge base. Read-only; never edits files.

Checks (ERROR = fails CI, WARN/INFO = reported only):
  [ERROR] year-dir page missing frontmatter or a required field (title/date/url)
  [ERROR] accidental duplicate: same source URL + same title across two year-dir
          pages WITHIN ONE SCOPE. Intentional version/event splits keep DIFFERENT
          titles; cross-scope (llm<->omni) and year<->themes cross-listings of the
          same work are expected and are NOT flagged.
  [WARN]  broken [[wikilink]] pointing at a slug with no matching page (many are
          pre-existing dangling concept-links; promote to ERROR after a cleanup)
  [WARN]  a year-dir page whose `date` year differs from its folder year
  [INFO]  how many works are duplicated across files (year<->themes magnitude)

Usage:  python3 scripts/lint.py
Exit code is non-zero if any ERROR is found.
"""
import os, re, sys, collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(REPO, "research")
SCOPES = ["llm", "omni"]
YEAR_RX = re.compile(r"^(19|20)\d{2}$")
# URLs that legitimately host more than one distinct work (shared landing pages).
SHARED_LANDING = {
    "https://www.anthropic.com/system-cards",
}

errors, warns = [], []


def parse_fm(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return None, ""
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return None, txt
    body = m.group(1)

    def grab(pat):
        mm = re.search(pat, body, re.M)
        return mm.group(1).strip().strip('"').strip("'") if mm else ""

    fm = {
        "title": grab(r"^title:\s*(.+)$"),
        "date": grab(r"^date:\s*\"?([0-9]{4}(?:-[0-9]{2})?)"),
        "url": grab(r"^\s*url:\s*(\S+)"),
    }
    return fm, txt


def norm_title(t):
    return re.sub(r"\s+", " ", t.strip().lower())


def is_workpage(fn):
    return fn.endswith(".md") and not fn.startswith(("00-", "01-", "README"))


# ---- collect pages ----
all_slugs = set()          # every page basename (for wikilink resolution)
year_pages = []            # (scope, folder_year, relpath, fm)
url_to_files = collections.defaultdict(list)   # url -> [relpath] across ALL pages
wikilink_sites = []        # (relpath, [slugs])
LINK_RX = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]")

for scope in SCOPES:
    base = os.path.join(RESEARCH, scope)
    for root, _, files in os.walk(base):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, REPO)
            all_slugs.add(fn[:-3])   # every page is a valid wikilink target
            fm, txt = parse_fm(path)
            # wikilink targets (skip auto-generated index; ignore inline-code examples)
            if not fn.startswith("01-"):
                slugs = []
                scan = re.sub(r"`[^`\n]*`", "", txt)   # drop inline-code spans
                for m in LINK_RX.finditer(scan):
                    tgt = m.group(1).strip()
                    if not tgt or tgt.startswith("#"):
                        continue
                    slugs.append(os.path.basename(tgt).removesuffix(".md"))
                if slugs:
                    wikilink_sites.append((rel, slugs))
                # Internal markdown links must be content-root-relative (start with a
                # scope folder, e.g. llm/ or omni/). Bare/relative .md links resolve
                # to the wrong path on the site: Quartz computes folder-style relative
                # hrefs but GitHub Pages serves file-style URLs, so a link like
                # ](2020/x.md) from /llm/ drops to /2020/x (404). Use ](llm/2020/x.md).
                for m in re.finditer(r"\]\(([^)\s]+\.md)\)", scan):
                    tgt = m.group(1)
                    if "://" in tgt or tgt.startswith("#"):
                        continue
                    t = tgt[2:] if tgt.startswith("./") else tgt
                    if t.split("/", 1)[0] not in SCOPES:
                        errors.append(
                            f"{rel}: internal link ]({tgt}) is not content-root-relative — "
                            f"prefix the scope, e.g. ]({scope}/{t})"
                        )
            if not is_workpage(fn):
                continue
            folder = os.path.basename(root)
            url = (fm or {}).get("url", "").rstrip("/")
            if url:
                url_to_files[url].append(rel)
            if YEAR_RX.match(folder):
                if not fm:
                    errors.append(f"{rel}: missing YAML frontmatter")
                    continue
                for field in ("title", "date", "url"):
                    if not fm.get(field):
                        errors.append(f"{rel}: frontmatter missing `{field}`")
                year_pages.append((scope, folder, rel, fm))

# ---- ERROR: accidental duplicate (same url + same title, within ONE scope) ----
# Cross-scope (llm<->omni) and year<->themes copies of the same work are expected.
by_scope_url = collections.defaultdict(list)
for scope, folder, rel, fm in year_pages:
    if fm.get("url"):
        by_scope_url[(scope, fm["url"].rstrip("/"))].append((rel, norm_title(fm.get("title", ""))))
for (scope, url), items in by_scope_url.items():
    if url in SHARED_LANDING or len(items) < 2:
        continue
    title_groups = collections.defaultdict(list)
    for rel, t in items:
        title_groups[t].append(rel)
    for t, rels in title_groups.items():
        if len(rels) > 1:
            errors.append("duplicate page (same url + same title): %s\n        %s" % (url, " | ".join(rels)))

# ---- WARN: broken wikilinks (deduped per file+slug) ----
broken = set()
for rel, slugs in wikilink_sites:
    for s in slugs:
        if s and s not in all_slugs:
            broken.add((rel, s))

# ---- WARN: folder year != date year ----
for scope, folder, rel, fm in year_pages:
    dy = (fm.get("date") or "")[:4]
    if dy and dy != folder:
        warns.append(f"{rel}: folder {folder} != date year {dy}")

# ---- INFO: duplication magnitude (across all pages, by url) ----
dist = collections.Counter(len(v) for v in url_to_files.values())

# ---- report ----
print("=== research/ lint ===")
print(f"year-dir work pages: {len(year_pages)} | unique source URLs: {len(url_to_files)}")
print("duplication by URL (across year+themes+deep-dive):")
for n in sorted(dist):
    works = dist[n]
    extra = (n - 1) * works
    print(f"  in {n} file(s): {works} work(s)" + (f"  (+{extra} redundant copies)" if n > 1 else ""))

if broken:
    missing = collections.Counter(s for _, s in broken)
    print(f"\n--- WARN: broken wikilinks ({len(broken)} occurrences, {len(missing)} distinct slugs) ---")
    for slug, n in missing.most_common(40):
        print(f"  WARN missing page [[{slug}]] (referenced {n}x)")
    if len(missing) > 40:
        print(f"  ... and {len(missing) - 40} more distinct slugs")

if warns:
    print(f"\n--- WARN: other ({len(warns)}) ---")
    for w in warns:
        print("  WARN", w)

if errors:
    print(f"\n--- ERROR ({len(errors)}) ---")
    for e in errors:
        print("  ERROR", e)
    print(f"\nFAILED: {len(errors)} error(s)")
    sys.exit(1)

print(f"\nOK: no errors ({len(warns)} warning(s))")
