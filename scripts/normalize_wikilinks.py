#!/usr/bin/env python3
"""Normalize [[alias]] wikilinks under research/omni to their real page slug.

Only maps unambiguous aliases (an alias -> the single page it must mean) and
trims stray whitespace inside otherwise-valid links. Re-run after adding pages
or renaming slugs.

Usage:  python3 scripts/normalize_wikilinks.py   (rewrites research/omni/**/*.md in place)
"""
import re, os, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(REPO, "research", "omni")

# alias -> real omni slug (unambiguous only)
ALIAS = {
    "stable-diffusion": "stable-diffusion-1",
    "stable-diffusion-xl": "sdxl",
    "sd3": "stable-diffusion-3",
    "sd3-mmdit": "stable-diffusion-3",
    "stable-diffusion-3-mmdit": "stable-diffusion-3",
    "sd3-5": "stable-diffusion-3-5",
    "dalle-2": "dall-e-2",
    "dalle-2-unclip": "dall-e-2",
    "dall-e": "dall-e-1",
    "dalle-1": "dall-e-1",
    "dalle-3": "dall-e-3",
    "flux": "flux-1",
    "flux-1-dev": "flux-1",
    "vqgan": "taming-transformers-vqgan",
    "taming-transformers": "taming-transformers-vqgan",
    "edm": "elucidating-edm",
    "var-next-scale": "var",
    "adm-guided-diffusion": "diffusion-models-beat-gans",
    "adm": "diffusion-models-beat-gans",
    "open-sora": "open-sora-plan",
    "grok-aurora": "aurora-grok-image",
    "qwen3-omni": "qwen3-5-omni",
    "ldm": "latent-diffusion-ldm",
    "ldm-stable-diffusion": "latent-diffusion-ldm",
    "latent-diffusion": "latent-diffusion-ldm",
    "dit": "dit-scalable-diffusion-transformers",
    "mmdit-sd3": "stable-diffusion-3",
    "var-next-scale-prediction": "var",
    "lcm-latent-consistency-models": "latent-consistency-models",
    "hunyuanvideo": "hunyuan-video",
    "hunyuanimage-3": "hunyuanimage-3-0",
    "flux-kontext": "flux-1-kontext",
    "hunyuandit": "hunyuan-dit",
    "qwen-image-edit-2509": "qwen-image-edit",
}

# valid slugs = every existing per-work page basename (year directories)
SLUGS = {os.path.basename(p)[:-3] for p in glob.glob(os.path.join(BASE, "20*", "*.md"))}

link = re.compile(r"\[\[([^\]\|]+)(\|[^\]]*)?\]\]")
files = glob.glob(os.path.join(BASE, "**", "*.md"), recursive=True)
changed = 0
for p in files:
    txt = open(p, encoding="utf-8").read()

    def repl(m):
        raw = m.group(1)
        target = raw.strip()
        alias = m.group(2) or ""
        if target in ALIAS:
            return f"[[{ALIAS[target]}{alias}]]"
        if target != raw and target in SLUGS:   # fix trailing/leading whitespace in valid slug
            return f"[[{target}{alias}]]"
        return m.group(0)

    new = link.sub(repl, txt)
    if new != txt:
        open(p, "w", encoding="utf-8").write(new)
        changed += 1
print(f"normalized wikilinks in {changed}/{len(files)} files")
