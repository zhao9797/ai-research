#!/usr/bin/env python3
"""Regenerate research/omni/01-INDEX.md from each page's YAML frontmatter.

Groups entries by the `date` year, dedupes by source URL. omni pages use a
single `category:` field (vs llm's `categories: [..]`) plus extra url fields
(hf/modelscope/project). Re-run after adding or removing source pages.

Usage:  python3 scripts/build_index_omni.py [BASE]
  BASE defaults to <repo>/research/omni
"""
import os, re, collections, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "research", "omni")
SCOPE = os.path.basename(os.path.normpath(BASE))  # "llm" or "omni"; links are content-root-relative
SRC_DIRS = ["2020", "2021", "2022", "2023", "2024", "2025", "2026", "2027",
            "sections", "deep-dive", "themes"]


def parse_fm(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except Exception:
        return None
    m = re.match(r"^---\s*\n(.*?)\n---", txt, re.S)
    if not m:
        return None
    body = m.group(1)

    def grab(pat, default=""):
        mm = re.search(pat, body, re.M)
        return mm.group(1).strip().strip('"').strip("'") if mm else default

    d = {}
    d["title"] = grab(r"^title:\s*(.+)$", "(no title)")
    d["org"] = grab(r"^org:\s*(.+)$")
    d["country"] = grab(r"^country:\s*(.+)$")
    d["date"] = grab(r"^date:\s*\"?([0-9]{4}(?:-[0-9]{2})?)")
    d["type"] = grab(r"^type:\s*(.+)$")
    d["category"] = grab(r"^category:\s*(.+)$")
    d["url"] = grab(r"^url:\s*(\S+)")
    d["_year"] = d["date"][:4] if re.match(r"\d{4}", d["date"]) else "未知"
    return d


entries = []
for sd in SRC_DIRS:
    full = os.path.join(BASE, sd)
    if not os.path.isdir(full):
        continue
    for root, _, files in os.walk(full):
        for fn in sorted(files):
            if not fn.endswith(".md") or fn.startswith("00-") or fn.startswith("01-"):
                continue
            fm = parse_fm(os.path.join(root, fn))
            if not fm:
                continue
            entries.append({
                "rel": os.path.relpath(os.path.join(root, fn), BASE),
                "title": fm["title"], "org": fm["org"], "country": fm["country"],
                "date": fm["date"], "year": fm["_year"], "type": fm["type"],
                "category": fm["category"], "url": fm["url"],
            })

# dedup by url (fallback title), prefer year-dir copy
by_url = {}
for e in sorted(entries, key=lambda e: (0 if e["rel"][:4].isdigit() else 1)):
    key = e["url"].rstrip("/") if e["url"] else e["title"].lower()
    by_url.setdefault(key, e)
uniq = list(by_url.values())


def norm_country(c):
    c = c.lower()
    if "china" in c or "cn" in c or "中国" in c:
        return "China"
    if "germany" in c or "eu" in c or "france" in c or "uk" in c or "europe" in c:
        return "Europe"
    if "us" in c or "usa" in c or "美" in c:
        return "US/West"
    return c if c else "other/unlabeled"


cnt_year = collections.Counter(e["year"] for e in uniq)
cnt_country = collections.Counter(norm_country(e["country"]) for e in uniq)
cnt_cat = collections.Counter(e["category"] for e in uniq if e["category"])

print("entries %d / unique %d" % (len(entries), len(uniq)))
for y in sorted(cnt_year):
    print("  %s: %d" % (y, cnt_year[y]))
print("country:", dict(cnt_country.most_common()))
print("category:", dict(cnt_cat.most_common()))

# dynamic year list: every year present, in order, with 未知 last
years = sorted(y for y in cnt_year if y != "未知")
if "未知" in cnt_year:
    years.append("未知")

out = ["---", "title: Omni / 多模态生成调研 — 全量来源索引", "type: source",
       "created: 2026-06-25", "updated: 2026-06-25", "---", "",
       "# 全量来源索引（按发布年月）", "",
       "> 去重后 **%d** 条一手来源（按 `date` 年份归组；去重键为原始 URL）。\n" % len(uniq)]
for y in years:
    ye = sorted([e for e in uniq if e["year"] == y], key=lambda e: (e["date"], e["title"]))
    if not ye:
        continue
    out.append("\n## %s（%d 条）\n" % (y, len(ye)))
    for e in ye:
        title = e["title"].replace("[", "(").replace("]", ")").replace("|", "/")
        out.append("- [[%s|%s]] — %s · %s · %s · [%s] — %s" % (
            SCOPE + "/" + e["rel"][:-3], title,
            e["org"] or "-", e["date"] or "?", e["type"] or "?",
            e["category"] or "-", e["url"] or ""))

open(os.path.join(BASE, "01-INDEX.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("wrote 01-INDEX.md (%d entries)" % len(uniq))
