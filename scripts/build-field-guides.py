#!/usr/bin/env python3
"""Build the 5 Markdown field guides as static GitHub Pages articles."""

from html import escape
from pathlib import Path
import json
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'docs' / 'guides'
SITE = 'https://marcodicesare-dev.github.io/jev-skill'
REPO = 'https://github.com/marcodicesare-dev/jev-skill'

GUIDES = [
    ('first-job', 'The first small decision I would give Jev in a new AI agent.', 'A beginner guide to routing, bounded choices and a labelled shadow test.'),
    ('lost-decisions', 'My AI missed 10 things I asked for in 14 team calls.', 'Find buried instructions in a meeting archive and keep every decision tied to its source.'),
    ('99-percent', 'Jev said 99%. About 15% of those answers were wrong.', 'Understand Jev probabilities and test an automation threshold on labelled cases.'),
    ('one-text-per-call', 'I made Jev cheaper. Then 34% of its answers changed.', 'Batch questions about one item without mixing different messages into one state.'),
    ('show-the-receipt', 'My AI cited a page that proved nothing.', 'Check extracted facts against the exact page they came from, with measured limits.'),
]


def pandoc(markdown: Path) -> str:
    return subprocess.run(
        ['pandoc', '--from=gfm', '--to=html5', '--wrap=none', str(markdown)],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout


def page_head(title: str, description: str, url: str, image: str, page_type: str) -> str:
    title_html = escape(title)
    description_html = escape(description)
    schema = {
        '@context': 'https://schema.org',
        '@type': page_type,
        'headline': title,
        'description': description,
        'url': url,
        'image': image,
        'author': {'@type': 'Person', 'name': 'Marco Di Cesare', 'url': 'https://x.com/marcodice_ai'},
        'datePublished': '2026-09-28',
        'publisher': {'@type': 'Person', 'name': 'Marco Di Cesare'},
    }
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index, follow">
  <title>{title_html} — Marco Di Cesare</title>
  <meta name="description" content="{description_html}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{title_html}">
  <meta property="og:description" content="{description_html}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="../../assets/jev-guide-cover.png">
  <link rel="preconnect" href="https://api.fontshare.com">
  <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=switzer@400,500,600,700&amp;display=swap">
  <link rel="stylesheet" href="../../style.css">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False).replace('</', '<\\/')}</script>
</head>
'''


def build_article(slug: str, deck: str) -> None:
    source = ROOT / 'guides' / f'{slug}.md'
    text = source.read_text()
    title = text.splitlines()[0].removeprefix('# ')
    assert text.startswith('# ') and text.count(f'](../docs/assets/guides/{slug}.jpg)') == 1
    assert REPO in text, f'{slug} is missing its skill link'
    rendered = pandoc(source)
    rendered = re.sub(r'<h1\b[^>]*>.*?</h1>', '', rendered, count=1, flags=re.S)
    rendered = rendered.replace(
        f'src="../docs/assets/guides/{slug}.jpg"',
        f'src="../../assets/guides/{slug}.jpg" width="1983" height="793" loading="eager"',
    )
    url = f'{SITE}/guides/{slug}/'
    image = f'{SITE}/assets/guides/{slug}.jpg'
    i = next(index for index, item in enumerate(GUIDES) if item[0] == slug)
    next_slug, next_label, _ = GUIDES[(i + 1) % len(GUIDES)]
    html = page_head(title, deck, url, image, 'Article') + f'''<body>
  <a class="skip" href="#article">Skip to the guide</a>
  <header class="site-head"><nav aria-label="Main navigation"><a href="{SITE}/">The ultimate guide</a><a href="{SITE}/guides/">5 field guides</a><a href="{REPO}">Get the skill on GitHub ↗</a></nav></header>
  <main id="article">
    <header class="article-head"><h1>{escape(title)}</h1><p class="dek">{escape(deck)}</p><p class="byline">By <a href="https://x.com/marcodice_ai">Marco Di Cesare</a> · 28 September 2026</p></header>
    <article>
{rendered}
      <nav class="guide-next" aria-label="Next field guide"><a href="../{next_slug}/">Next: {escape(next_label)} →</a></nav>
    </article>
  </main>
  <footer><p><a href="{REPO}">Get the Jev skill</a> · <a href="{SITE}/guides/">All 5 field guides</a> · <a href="https://www.luminafrontier.ai/?utm_source=github_pages&amp;utm_medium=field_guide&amp;utm_campaign=jev_skill">Lumina</a> · <a href="https://x.com/marcodice_ai">X</a></p><p>Independent field guide, not an official TypeSafe publication.</p></footer>
</body>
</html>
'''
    output = DEST / slug / 'index.html'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html)


def build_index() -> None:
    cards = '\n'.join(
        f'''<li><a href="{slug}/"><img src="../assets/guides/{slug}.jpg" width="1983" height="793" loading="lazy" alt=""><span class="guide-card-title">{escape(label)}</span><span class="guide-card-deck">{escape(deck)}</span></a></li>'''
        for slug, label, deck in GUIDES
    )
    title = '5 Jev field guides for building better AI agents'
    description = 'Real Jev tests turned into practical guides: routing, archive search, probability checks, batching and source verification.'
    html = page_head(title, description, f'{SITE}/guides/', f'{SITE}/assets/guides/first-job.jpg', 'CollectionPage')
    html = html.replace('href="../../style.css"', 'href="../style.css"')
    html = html.replace('href="../../assets/jev-guide-cover.png"', 'href="../assets/jev-guide-cover.png"')
    html += f'''<body>
  <a class="skip" href="#guides">Skip to the guides</a>
  <header class="site-head"><nav aria-label="Main navigation"><a href="{SITE}/">The ultimate guide</a><a href="{REPO}">Get the skill on GitHub ↗</a></nav></header>
  <main id="guides" class="guide-index">
    <header class="article-head"><h1>5 jobs I actually tested with Jev</h1><p class="dek">I made my AI writer cheaper and the writing got worse. These are the smaller decisions I tested next, with the setup and the failure in each case.</p><p class="byline">By <a href="https://x.com/marcodice_ai">Marco Di Cesare</a> · 28 September 2026</p></header>
    <ol class="guide-grid">{cards}</ol>
    <p class="guide-index-end">Want to try 1 in your own agent? <a href="{REPO}">Install the Jev skill</a> and run a labelled shadow test before replacing the current path.</p>
  </main>
  <footer><p><a href="{REPO}">Get the Jev skill</a> · <a href="{SITE}/">The ultimate guide</a> · <a href="https://www.luminafrontier.ai/?utm_source=github_pages&amp;utm_medium=field_guides&amp;utm_campaign=jev_skill">Lumina</a></p><p>Independent research, not an official TypeSafe publication.</p></footer>
</body>
</html>
'''
    (DEST / 'index.html').write_text(html)


def build_sitemap() -> None:
    urls = [f'{SITE}/', f'{SITE}/guides/'] + [f'{SITE}/guides/{slug}/' for slug, _, _ in GUIDES]
    body = '\n'.join(f'  <url><loc>{url}</loc><lastmod>2026-09-28</lastmod></url>' for url in urls)
    (ROOT / 'docs' / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f'{body}\n</urlset>\n'
    )


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for slug, _, deck in GUIDES:
        build_article(slug, deck)
    build_index()
    build_sitemap()


if __name__ == '__main__':
    main()
