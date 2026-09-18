#!/usr/bin/env python3
"""Generates the Barn Dressage support site in the app's 13 languages: index / privacy / terms.
English is the default (index.html); other languages are index.<lang>.html and so on. Run: python3 build.py"""
import html
from i18n import T, ORDER

EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'
APPLE_PRIVACY = 'https://www.apple.com/legal/privacy/'
MAIL = 'gmemik@gmail.com'
MARK = '''<div class="mark" aria-hidden="true"><svg viewBox="0 0 64 64" width="56" height="56" role="img">
<rect x="14" y="8" width="36" height="48" rx="3" fill="none" stroke="#f0b64a" stroke-width="4"/>
<path d="M32 50V30c0-8 10-8 10-14" fill="none" stroke="#7ed98d" stroke-width="4" stroke-linecap="round"/>
<circle cx="32" cy="50" r="3.5" fill="#7ed98d"/></svg></div>'''

def fname(page, lang): return f'{page}.html' if lang == 'en' else f'{page}.{lang}.html'
def e(s): return html.escape(s, quote=False)

def switcher(page, cur):
    return '<p class="langs">' + ' · '.join(
        (f'<strong>{T[l]["name"]}</strong>' if l == cur else f'<a href="{fname(page, l)}" lang="{l}">{T[l]["name"]}</a>') for l in ORDER) + '</p>'

def shell(page, lang, title, desc, body):
    t = T[lang]
    nav = f'<a href="{fname("index", lang)}">{e(t["nav_support"])}</a> · <a href="{fname("privacy", lang)}">{e(t["nav_privacy"])}</a> · <a href="{fname("terms", lang)}">{e(t["nav_terms"])}</a> · <a href="mailto:{MAIL}">{e(t["nav_contact"])}</a>'
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Barn Dressage — {e(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
{switcher(page, lang)}
{body}
<footer>© 2026 thebarnapp · {nav}</footer>
</main>
</body>
</html>
'''

def ul(items): return '<ul>' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'

for lang in ORDER:
    t = T[lang]
    # support
    faq = ''.join(f'<h3>{e(q)}</h3><p>{e(a)}</p>' for q, a in t['faq'])
    body = f'''<header class="hero">{MARK}<h1>Barn Dressage</h1><p class="tagline">{e(t["tagline"])}</p></header>
<section><h2>{e(t["h_how"])}</h2>{ul(t["modes"])}</section>
<section><h2>{e(t["h_faq"])}</h2>{faq}</section>
<section><h2>{e(t["nav_contact"])}</h2><p>{e(t["contact"])} <a href="mailto:{MAIL}">{MAIL}</a></p></section>'''
    open(fname('index', lang), 'w').write(shell('index', lang, t['nav_support'], t['tagline'], body))
    # privacy
    p = t['privacy']
    secs = ''.join(f'<h2>{e(h)}</h2><p>{e(x)}</p>' for h, x in p['sections'])
    gc = e(p['gc'][1]).replace('{apple}', f'<a href="{APPLE_PRIVACY}">Apple Privacy Policy</a>')
    body = f'''<h1>{e(t["nav_privacy"])}</h1><p class="meta">Barn Dressage · thebarnapp · {e(t["effective"])}</p>
<p class="summary">{e(p["short"])}</p>
<h2>{e(p["h_not"])}</h2>{ul(p["not"])}
{secs}
<h2>{e(p["gc"][0])}</h2><p>{gc}</p>
<h2>{e(t["nav_contact"])}</h2><p><a href="mailto:{MAIL}">{MAIL}</a></p>'''
    open(fname('privacy', lang), 'w').write(shell('privacy', lang, t['nav_privacy'], p['short'], body))
    # terms
    m = t['terms']
    summary = e(m['summary']).replace('{eula}', f'<a href="{EULA}">Apple Licensed Application End User License Agreement (EULA)</a>')
    body = f'''<h1>{e(t["nav_terms"])}</h1><p class="meta">Barn Dressage · thebarnapp · {e(t["effective"])}</p>
<p class="summary">{summary}</p>
<h2>Barn Dressage Plus</h2>{ul(m["sub"])}
<h2>{e(m["h_scores"])}</h2><p>{e(m["scores"])}</p>
<h2>{e(t["nav_contact"])}</h2><p><a href="mailto:{MAIL}">{MAIL}</a></p>'''
    open(fname('terms', lang), 'w').write(shell('terms', lang, t['nav_terms'], m['sub'][0], body))
print('generated', len(ORDER) * 3, 'pages')
