#!/usr/bin/env python3
"""Update assets/activity.svg from public GitHub repos (stdlib-only).
No API key is required for public-only access; a GitHub Actions token increases rate limits.
No data is fabricated: errors fail the workflow without altering the existing SVG.
"""
from pathlib import Path
from datetime import datetime, timezone
import os, json, urllib.request, html

ROOT=Path(__file__).resolve().parents[1]
USER=os.environ.get('GH_USERNAME','ani12004')
TOKEN=os.environ.get('GITHUB_TOKEN','')
req=urllib.request.Request('https://api.github.com/users/'+USER+'/repos?per_page=100&sort=pushed',headers={'User-Agent':'BIOME-OS-GitHub-README','Accept':'application/vnd.github+json',**({'Authorization':'Bearer '+TOKEN} if TOKEN else {})})
with urllib.request.urlopen(req,timeout=20) as f: repos=json.loads(f.read().decode())
if not isinstance(repos,list):raise RuntimeError('GitHub repository listing was not a list')
repos=[r for r in repos if not r.get('fork') and r.get('name')!='ani12004' and not r.get('archived')]
repos.sort(key=lambda r:r.get('pushed_at') or '',reverse=True)
repos=repos[:4]
if not repos:raise RuntimeError('No public repositories available')
def esc(v):return html.escape(str(v),quote=True)
def short(v,n):return v if len(v)<=n else v[:n-1]+'…'
now=datetime.now(timezone.utc).strftime('%d %b %Y, %H:%M UTC')
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="254" viewBox="0 0 1100 254" role="img">',
'<defs><linearGradient id="b" x2="1" y2="1"><stop stop-color="#091c18"/><stop offset="1" stop-color="#173d31"/></linearGradient></defs>',
'<rect x="1" y="1" width="1098" height="252" rx="16" fill="url(#b)" stroke="#47745d"/>',
'<g font-family="Arial,DejaVu Sans,sans-serif">',
'<circle cx="34" cy="35" r="5" fill="#8be0b7"/><text x="50" y="41" font-size="14" font-weight="700" fill="#9fe1b9" letter-spacing="2">REPO SIGNAL / LIVE PUBLIC SNAPSHOT</text>',
f'<text x="1060" y="41" text-anchor="end" font-size="11" fill="#a5c5b4">Updated {esc(now)}</text>']
for i,r in enumerate(repos):
 x=30+i*267; name=short(r.get('name','unnamed'),25)
 desc=short(r.get('description') or 'Public repository',38)
 lang=short(r.get('language') or 'Code',20)
 pushed=r.get('pushed_at','')[:10] or 'Unknown'
 s.extend([f'<rect x="{x}" y="65" width="247" height="152" rx="12" fill="#1b4033" stroke="#4a7861"/>',
 f'<text x="{x+18}" y="95" fill="#90dfae" font-size="12" font-weight="700">0{i+1} / REPOSITORY</text>',
 f'<text x="{x+18}" y="128" fill="#f2efe3" font-size="17" font-weight="700">{esc(name)}</text>',
 f'<text x="{x+18}" y="154" fill="#bdcfc0" font-size="11">{esc(desc)}</text>',
 f'<text x="{x+18}" y="189" fill="#99d2b0" font-size="11">{esc(lang)}  ·  {esc(pushed)}</text>'])
s.append('</g></svg>')
(ROOT/'assets'/'activity.svg').write_text('\n'.join(s),encoding='utf-8')
print(f'Updated public activity for {len(repos)} repositories')
