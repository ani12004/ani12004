from pathlib import Path
import base64, mimetypes
from markdown_it import MarkdownIt
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
md=(ROOT/'README.md').read_text(encoding='utf-8')
render=MarkdownIt('commonmark',{'html':True,'linkify':True}).enable('table')
content=render.render(md)
# Shields hosted remotely may not load during offline screenshot rendering. Replace their
# <img> tags with real anchor labels for preview only. This does not change README.md.
import re
content=re.sub(r'<img\s+[^>]*?src="https://img\.shields\.io/[^>]+>',lambda m:'<span class="preview-pill">'+re.search(r'alt="([^"]+)"',m.group(0)).group(1)+'</span>' if re.search(r'alt="([^"]+)"',m.group(0)) else '',content)
css='''
* {box-sizing:border-box} html{background:#0d1117} body{margin:0;background:#0d1117;color:#dae4dd;font:16px/1.55 -apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif} 
.markdown-body {box-sizing:border-box;max-width:1080px;margin:0 auto;padding:34px 34px 54px;background:#0d1117}
.markdown-body img {max-width:100%; height:auto; display:inline-block; vertical-align:middle}
.markdown-body a {color:#73cda2;text-decoration:none}
.markdown-body a:hover{text-decoration:underline}
.markdown-body h2{font-size:28px;margin:34px 0 22px;padding-bottom:10px;border-bottom:1px solid #33443c;color:#eff8f1;letter-spacing:-.2px}
.markdown-body h3{font-size:21px;margin:11px 0;color:#f3f1e7}
.markdown-body table{width:100%;border-spacing:0;border-collapse:collapse;margin:18px 0;color:#d4e0d7;display:table}
.markdown-body table td,.markdown-body table th{border:1px solid #354b40;padding:13px;vertical-align:top}
.markdown-body p{margin:12px 0 17px}.markdown-body blockquote{border-left:4px solid #70b996;padding-left:13px;margin:18px 0;color:#a8c3b2}
.markdown-body details{border:1px solid #365847;border-radius:11px;padding:14px 19px;margin:20px 0;background:#13231e}
.markdown-body code{font:12px/1.5 ui-monospace,SFMono-Regular,Consolas,monospace;background:#1b342a;border:1px solid #305846;padding:4px 6px;border-radius:5px;color:#a6dfbc}
.markdown-body pre{padding:16px;background:#111f1b;border-radius:8px}
.markdown-body pre code{border:0;background:transparent;padding:0}
.markdown-body sub{color:#97b3a4;font-size:12px}
.preview-pill {background:#1b4734;border:1px solid #3d8961;border-radius:7px;padding:9px 14px;display:inline-block;font-size:11px;color:#c4e8ce;font-weight:700;text-transform:uppercase;margin:4px}
'''
def embed_asset(match):
    name=match.group(1)
    blob=(ROOT/'assets'/name).read_bytes()
    mime=mimetypes.guess_type(name)[0] or 'image/png'
    return 'src="data:'+mime+';base64,'+base64.b64encode(blob).decode('ascii')+'"'
content=re.sub(r'src="\./assets/([^"]+)"',embed_asset,content)
page='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>BIOME / OS README layout preview</title><style>'+css+'</style></head><body><main class="markdown-body">'+content+'</main></body></html>'
html_path=ROOT/'layout-preview.html'; html_path.write_text(page,encoding='utf-8')
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--allow-file-access-from-files'])
 tab=browser.new_page(viewport={'width':1240,'height':1100},device_scale_factor=1)
 tab.set_content(page,wait_until='load',timeout=60000)
 tab.screenshot(path=str(ROOT.parent/'Anil_Biome_OS_Full_Preview.png'),full_page=True,animations='disabled')
 browser.close()
img=Image.open(ROOT.parent/'Anil_Biome_OS_Full_Preview.png').convert('RGB')
print('preview size',img.size)
img.crop((0,0,img.width,min(img.height,1430))).save(ROOT.parent/'Anil_Biome_OS_AboveFold_Preview.png',optimize=True)
html_path.unlink(missing_ok=True)
