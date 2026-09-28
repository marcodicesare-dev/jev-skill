#!/usr/bin/env python3
"""Render the public Jev guide as a static, readable GitHub Pages article.

Requires pandoc. The generated HTML is committed so Pages needs no build tooling.
"""

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "GUIDE.md"
OUTPUT = ROOT / "docs" / "index.html"
REPO = "https://github.com/marcodicesare-dev/jev-skill"
TITLE = "The Ultimate Guide to Jev (After 19,367 Calls and 90M Tokens)"
URL = "https://marcodicesare-dev.github.io/jev-skill/"


def main() -> None:
    rendered = subprocess.run(
        ["pandoc", "--from=gfm", "--to=html5", "--wrap=none", str(GUIDE)],
        check=True,
        capture_output=True,
        text=True,
        cwd=ROOT,
    ).stdout
    rendered = rendered.replace('src="assets/jev-guide-cover.png"', 'src="assets/jev-guide-cover.png" width="1983" height="793" loading="eager"')
    for asset in ("jev-archive.png", "jev-source-check.png"):
        rendered = rendered.replace(f'src="assets/{asset}"', f'src="assets/{asset}" width="1983" height="793" loading="lazy"')
    rendered = re.sub(
        r'href="(?!https?://|#|mailto:)([^"]+)"',
        lambda match: f'href="{REPO}/blob/main/{match.group(1)}"',
        rendered,
    )
    rendered = rendered.replace(
        "utm_source=github&amp;utm_medium=guide",
        "utm_source=github_pages&amp;utm_medium=guide",
    )
    rendered = re.sub(r"<h1\b[^>]*>.*?</h1>", "", rendered, count=1, flags=re.S)
    head = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index, follow">
  <title>{TITLE} — Marco Di Cesare</title>
  <meta name="description" content="I tried to make my AI writer cheaper with Jev. The writing got worse. After 19,367 calls, here is where the decision model helped, failed, and earned a place in an agent.">
  <link rel="canonical" href="{URL}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="I tried to make my AI writer cheaper with Jev. The writing got worse. Then I gave the model a different job.">
  <meta property="og:url" content="{URL}">
  <meta property="og:image" content="{URL}assets/jev-guide-cover.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="assets/jev-guide-cover.png">
  <link rel="preconnect" href="https://api.fontshare.com">
  <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=switzer@400,500,600,700&amp;display=swap">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <a class="skip" href="#article">Skip to the guide</a>
  <header class="site-head"><nav aria-label="Main navigation"><a href="guides/">5 field guides</a><a href="{REPO}">The skill on GitHub ↗</a><a href="{REPO}/blob/main/AUDIT-YOUR-AGENT.md">Audit your agent ↗</a></nav></header>
  <main id="article">
    <header class="article-head"><h1>{TITLE}</h1><p class="dek">I made my AI writer 37% cheaper. The ads got worse, 13–3. Then Jev found 51 of 54 buried instructions for $0.32.</p><p class="byline">By <a href="https://x.com/marcodice_ai">Marco Di Cesare</a> · 28 September 2026</p></header>
    <article>
{rendered}
    </article>
  </main>
  <footer><p>Built while working on <a href="https://www.luminafrontier.ai/?utm_source=github_pages&amp;utm_medium=jev_guide&amp;utm_campaign=jev_skill">Lumina</a>. <a href="{REPO}">Get the Jev skill</a> · <a href="https://www.instagram.com/marcodice.ai/">Instagram</a> · <a href="https://x.com/marcodice_ai">X</a></p><p>This is an independent guide, not an official TypeSafe publication.</p></footer>
</body>
</html>
'''
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(head)
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build-field-guides.py')], check=True)


if __name__ == "__main__":
    main()
