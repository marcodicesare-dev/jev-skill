#!/usr/bin/env python3
"""Render the public Jev guide as a static, readable GitHub Pages article.

Requires pandoc. The generated HTML is committed so Pages needs no build tooling.
"""

from pathlib import Path
import re
import subprocess


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
    rendered = rendered.replace('src="assets/jev-guide-cover.png"', 'src="assets/jev-guide-cover.png" width="2000" height="825" loading="eager"')
    rendered = re.sub(
        r'href="(?!https?://|#|mailto:)([^"]+)"',
        lambda match: f'href="{REPO}/blob/main/{match.group(1)}"',
        rendered,
    )
    rendered = rendered.replace(
        "utm_source=github&amp;utm_medium=guide",
        "utm_source=github_pages&amp;utm_medium=guide",
    )
    rendered = rendered.replace("<h1\n", "<h1\n", 1)
    rendered = re.sub(r"<h1\b[^>]*>.*?</h1>", "", rendered, count=1, flags=re.S)
    head = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index, follow">
  <title>{TITLE} — Marco Di Cesare</title>
  <meta name="description" content="A practical guide to Jev and TypeSafe System One after 19,367 successful calls: API quickstart, 5 copyable recipes, measured failures, agent patterns, cost and calibration.">
  <link rel="canonical" href="{URL}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="We ran Jev 19,367 times. The result that changed how we use it was a failure. Read the tested guide and copy a first workflow.">
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
  <header class="site-head"><a class="wordmark" href="{URL}">Jev, explained.</a><nav aria-label="Main navigation"><a href="{REPO}">The skill on GitHub ↗</a><a href="{REPO}/blob/main/AUDIT-YOUR-AGENT.md">Audit your agent ↗</a></nav></header>
  <main id="article">
    <header class="article-head"><h1>{TITLE}</h1><p class="dek">The failures, a runnable call, and 5 questions worth stealing.</p><p class="byline">By <a href="https://x.com/marcodice_ai">Marco Di Cesare</a> · 28 September 2026 · Independent research</p></header>
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


if __name__ == "__main__":
    main()
