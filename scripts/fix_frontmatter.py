#!/usr/bin/env python3
"""Repair YAML frontmatter under research/ so it is valid for GitHub/Obsidian.

Two classes of problem:
  1) multiple fields crammed on one line:
     `org: X    country: Y    date: Z    type: W`  ->  split into separate lines
  2) a scalar value containing a colon left unquoted:
     `title: PaLM: Scaling...`  ->  wrap in double quotes
Runs a PyYAML validation pass at the end if PyYAML is installed.

Usage:  python3 scripts/fix_frontmatter.py [ROOT]
  ROOT defaults to <repo>/research
"""
import os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "research")
KEYS = ("title|org|country|date|type|category|categories|url|arxiv|pdf_url|github_url|"
        "hf_url|modelscope_url|project_url|downloaded|sources|tags|updated|created")
SPLIT_RX = re.compile(r'[ \t]{2,}(?=(?:' + KEYS + r'):)')
SPECIAL = set('!&*?|>%@`{[]},#"\'')


def needs_quote(v):
    if v == "" or v[0] in SPECIAL:
        return False
    if re.search(r':(\s|$)', v):
        return True
    if v[0] in '-?:' and (len(v) == 1 or v[1] == ' '):
        return True
    return v != v.strip()


def quote(v):
    return '"' + v.replace('\\', '\\\\').replace('"', '\\"') + '"'


def process(fm):
    fm = SPLIT_RX.sub('\n', fm)                       # pass 1: split one-line multi-field
    out = []
    for line in fm.split('\n'):
        line = line.rstrip()
        lm = re.match(r'^([A-Za-z_][\w]*):\s?(.*)$', line)
        if lm and needs_quote(lm.group(2)):           # pass 2: quote colon-bearing scalars
            out.append(f'{lm.group(1)}: {quote(lm.group(2))}')
        else:
            out.append(line)
    return "\n".join(out)


fixed = 0
for dp, _, fns in os.walk(ROOT):
    for fn in fns:
        if not fn.endswith('.md'):
            continue
        p = os.path.join(dp, fn)
        with open(p, encoding='utf-8') as f:
            txt = f.read()
        m = re.match(r'^(---\s*\n)(.*?)(\n---)', txt, re.S)
        if not m:
            continue
        new = m.group(2)
        new2 = process(new)
        if new2 != new:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(m.group(1) + new2 + m.group(3) + txt[m.end():])
            fixed += 1
print("fixed files:", fixed)

try:
    import yaml
    bad = []
    for dp, _, fns in os.walk(ROOT):
        for fn in fns:
            if not fn.endswith('.md'):
                continue
            with open(os.path.join(dp, fn), encoding='utf-8') as f:
                txt = f.read()
            m = re.match(r'^---\s*\n(.*?)\n---', txt, re.S)
            if not m:
                continue
            try:
                yaml.safe_load(m.group(1))
            except Exception as e:
                bad.append((fn, str(e).splitlines()[0]))
    print("YAML validation: failures =", len(bad))
    for b in bad[:15]:
        print("  BAD:", b[0], "|", b[1])
except ImportError:
    print("(PyYAML not installed, skipping validation)")
