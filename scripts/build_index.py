#!/usr/bin/env python3
"""Regenerate research/llm/01-INDEX.md from each page's YAML frontmatter.

Groups entries by the `date` year, dedupes by source URL (preferring the
year-directory copy over a themes/ copy). Re-run after adding or removing
source pages.

Usage:  python3 scripts/build_index.py [BASE]
  BASE defaults to <repo>/research/llm
"""
import os, re, collections, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "research", "llm")
SCOPE = os.path.basename(os.path.normpath(BASE))  # "llm" or "omni"; links are content-root-relative
SRC_DIRS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027",
            "themes/ai-infra", "themes/post-training", "themes/agentic", "themes/architecture"]


def parse_fm(path):
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    body = m.group(1)

    def grab(pat):
        mm = re.search(pat, body)
        return mm.group(1).strip() if mm else ""

    d = {}
    mt = re.search(r"^title:\s*(.+)$", body, re.M)
    d["title"] = (mt.group(1).strip().strip('"') if mt else "(no title)")
    mo = re.search(r"org:\s*(.+?)(?:\s{2,}(?:country|date|type|url):|\s*$)", body, re.M)
    d["org"] = (mo.group(1).strip().strip('"') if mo else "")
    d["country"] = grab(r"country:\s*([^\s]+)").strip('"')
    d["date"] = grab(r"date:\s*([0-9]{4}(?:-[0-9]{2})?)")
    d["type"] = grab(r"type:\s*([A-Za-z][A-Za-z-]*)")
    d["url"] = grab(r"\burl:\s*(\S+)")
    mc = re.search(r"categories:\s*\[([^\]]*)\]", body)
    d["_categories"] = [x.strip().strip("'\"") for x in mc.group(1).split(",") if x.strip()] if mc else []
    d["_date"] = d["date"]
    d["_year"] = d["_date"][:4] if re.match(r"\d{4}", d["_date"]) else "未知"
    return d


entries = []
for sd in SRC_DIRS:
    full = os.path.join(BASE, sd)
    if not os.path.isdir(full):
        continue
    for fn in sorted(os.listdir(full)):
        if not fn.endswith(".md"):
            continue
        fm = parse_fm(os.path.join(full, fn))
        if not fm:
            continue
        entries.append({
            "rel": os.path.relpath(os.path.join(full, fn), BASE), "dir": sd,
            "title": fm["title"], "org": fm["org"], "country": fm["country"],
            "date": fm["_date"], "year": fm["_year"], "type": fm["type"],
            "categories": fm["_categories"], "url": fm["url"],
        })

# dedup by url, prefer year-dir copy
by_url = {}
for e in sorted(entries, key=lambda e: (0 if e["dir"][:1].isdigit() else 1)):
    key = e["url"].rstrip("/") if e["url"] else e["title"].lower()
    by_url.setdefault(key, e)
uniq = list(by_url.values())


def norm_country(c):
    c = c.lower()
    if "china" in c or "cn" in c or "中国" in c:
        return "China"
    if "us" in c or "usa" in c or "美" in c:
        return "US/West"
    if c in ("eu", "france", "uk", "europe"):
        return "Europe"
    return c if c else "other/unlabeled"


cnt_year = collections.Counter(e["year"] for e in uniq)
cnt_country = collections.Counter(norm_country(e["country"]) for e in uniq)

print("entries %d / unique %d" % (len(entries), len(uniq)))
for y in sorted(cnt_year):
    print("  %s: %d" % (y, cnt_year[y]))
print("country:", dict(cnt_country.most_common()))

# dynamic year list: every year present, in order, with 未知 last
years = sorted(y for y in cnt_year if y != "未知")
if "未知" in cnt_year:
    years.append("未知")

out = ["---", "title: LLM 技术演进调研 — 全量来源索引", "type: source",
       "created: 2026-06-18", "updated: 2026-06-18", "---", "",
       "# 全量来源索引（按发布年月）", "",
       "> 去重后 **%d** 条一手来源（按 `date` 年份归组；去重键为原始 URL）。\n" % len(uniq)]
for y in years:
    ye = sorted([e for e in uniq if e["year"] == y], key=lambda e: (e["date"], e["title"]))
    if not ye:
        continue
    out.append("\n## %s（%d 条）\n" % (y, len(ye)))
    for e in ye:
        cats = "/".join(e["categories"]) if e["categories"] else "-"
        title = e["title"].replace("[", "(").replace("]", ")").replace("|", "/")
        out.append("- [[%s|%s]] — %s · %s · %s · [%s] — %s" % (
            SCOPE + "/" + e["rel"][:-3], title,
            e["org"] or "-", e["date"] or "?", e["type"] or "?", cats, e["url"] or ""))

with open(os.path.join(BASE, "01-INDEX.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")
print("wrote 01-INDEX.md (%d entries)" % len(uniq))
