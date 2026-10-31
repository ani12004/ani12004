#!/usr/bin/env python3
"""Generate self-hosted, GitHub-compatible BIOME.OS profile artwork.
Run: python tools/generate_assets.py
Requires: cairosvg, Pillow
All artwork is created from vector geometry. No hosted fonts or image API required.
"""
from __future__ import annotations
from pathlib import Path
import math, random, io, html, itertools
from PIL import Image
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets'; A.mkdir(parents=True, exist_ok=True)
C={'bg':'#081A18','bg2':'#102A25','bg3':'#173B32','panel':'#17332D','panel2':'#1C4036','cream':'#F2EFE3','muted':'#B4C4B5','pale':'#DDE8D5','sage':'#8DBF9C','mint':'#87E1BA','teal':'#45B89B','gold':'#E8C18A','line':'#3D6556','faint':'#6C8F80','orange':'#F7A975'}

def E(t): return html.escape(str(t),quote=True)
class S:
 def __init__(self,w,h):
  self.w,self.h=w,h;self.a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">', '''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#071816"/><stop offset="0.55" stop-color="#133A30"/><stop offset="1" stop-color="#0C211F"/></linearGradient>
  <linearGradient id="sea" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#547E6E"/><stop offset="0.54" stop-color="#2E5C54"/><stop offset="1" stop-color="#132E2B"/></linearGradient>
  <linearGradient id="light" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#EACD9D"/><stop offset="0.6" stop-color="#B3BCA5"/><stop offset="1" stop-color="#2C6152"/></linearGradient>
  <linearGradient id="mint" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#66D0A4"/><stop offset="1" stop-color="#CEE1AD"/></linearGradient>
  <radialGradient id="glow"><stop stop-color="#F3D8AB" stop-opacity=".44"/><stop offset=".5" stop-color="#D2DDAD" stop-opacity=".18"/><stop offset="1" stop-color="#D2DDAD" stop-opacity="0"/></radialGradient>
  <linearGradient id="shade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#0B211D"/><stop offset=".65" stop-color="#0D241F" stop-opacity=".75"/><stop offset="1" stop-color="#0D241F" stop-opacity=".05"/></linearGradient>
 </defs>''']
 def add(self,raw): self.a.append(raw)
 def rect(self,x,y,w,h,fill,rx=0,stroke='none',sw=1,opacity=1): self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>')
 def cir(self,x,y,r,fill,stroke='none',sw=1,opacity=1): self.add(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>')
 def line(self,x,y,x2,y2,color,width=1,opacity=1,dash=None): self.add(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}" opacity="{opacity}" {f"stroke-dasharray={E(dash)!r}" if dash else ""}/>')
 def path(self,d,fill='none',stroke='none',sw=1,op=1): self.add(f'<path d="{E(d)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}" stroke-linejoin="round" stroke-linecap="round"/>')
 def tx(self,x,y,text,size=20,color=None,weight=400,family='Inter',spacing=0,anchor='start',opacity=1,style='normal'):
  color=color or C['cream']; self.add(f'<text x="{x}" y="{y}" font-family="{E(family)},DejaVu Sans,sans-serif" font-size="{size}" font-weight="{weight}" font-style="{style}" letter-spacing="{spacing}" text-anchor="{anchor}" fill="{color}" opacity="{opacity}">{E(text)}</text>')
 def pill(self,x,y,w,text,fill='#254E41',fg=None,border='#4E816B',h=30,size=12):
  self.rect(x,y,w,h,fill,15,border,1); self.tx(x+15,y+h/2+size*.37,text,size,fg or C['pale'],600)
 def finish(self): return '\n'.join(self.a+['</svg>'])

def grid(s,spacing=38,alpha=.06):
 for x in range(0,s.w,spacing):s.line(x,0,x,s.h,'#C1D8BB',1,alpha)
 for y in range(0,s.h,spacing):s.line(0,y,s.w,y,'#C1D8BB',1,alpha)

def label(s,x,y,n,title):
 s.cir(x,y-5,4,C['mint']);s.tx(x+14,y,n+' / '+title,13,C['mint'],700,spacing=2)

def mountain(s,w,h,phase=0,scene_start=0):
 # Right-side vista: horizon, sunlight, layered alpine ridges, trees and river
 cx=w*.82;cy=h*.38
 s.cir(cx,cy,105,'url(#glow)');s.cir(cx,cy,40,'#DFD2A8',opacity=.65)
 s.path(f'M{scene_start} {h*.69} L{w*.55} {h*.50} L{w*.66} {h*.63} L{w*.78} {h*.30} L{w*.93} {h*.59} L{w} {h*.45} L{w} {h} L{scene_start} {h} Z','#507D6B',op=.7)
 s.path(f'M{scene_start} {h*.79} L{w*.52} {h*.65} L{w*.67} {h*.70} L{w*.77} {h*.50} L{w*.88} {h*.69} L{w} {h*.60} L{w} {h} L{scene_start} {h} Z','#31594E')
 s.path(f'M{scene_start} {h*.89} Q{w*.66} {h*.71} {w*.75} {h*.82} T{w} {h*.78} L{w} {h} L{scene_start} {h} Z','#1B4137')
 # softly flowing water
 s.path(f'M{w*.73} {h} Q{w*.83} {h*.88} {w*.79} {h*.82} Q{w*.88} {h*.85} {w*.91} {h*.98} L{w*.88} {h}', '#749E89',op=.45)
 for i in range(12):
  xx=w*(.58+i*.038); height=22+(i*19)%50; y=h*.83+(i%4)*7
  s.path(f'M{xx-11} {y+15} L{xx} {y-height} L{xx+11} {y+15} Z','#0C2A24',op=.78)
  s.line(xx,y-9,xx,y+19,'#0B281F',2)
 # drifting stars / spores
 for i in range(22):
  xx=w*(.59+(i*37%39)/100); yy=h*(.12+(i*29%43)/100)
  xo=2*math.sin(phase*2*math.pi+i)
  s.cir(xx+xo,yy,1.3+(i%3)*.4,C['gold'] if i%3==0 else C['pale'],opacity=.23+(i%5)*.08)
 for j in range(3):
  yy=h*(.21+j*.065); x=w*(.68+phase*.04+j*.01)
  s.path(f'M{x-30} {yy} Q{x+3} {yy-10} {x+57} {yy}',stroke='#E4DDC3',sw=1.5,op=.16)

def save_png(s,name):
 data=cairosvg.svg2png(bytestring=s.finish().encode(),output_width=s.w,output_height=s.h)
 (A/name).write_bytes(data)
 return Image.open(io.BytesIO(data)).convert('RGB')

def save_gif(frames,name,duration=140):
 # Global palette from first frame to minimize flashing, fast to view in GitHub
 first=frames[0].quantize(colors=100,method=Image.Quantize.FASTOCTREE)
 result=[first]
 for f in frames[1:]: result.append(f.quantize(palette=first))
 result[0].save(A/name,save_all=True,append_images=result[1:],duration=duration,loop=0,optimize=True,disposal=2)
 print(name,(A/name).stat().st_size//1024,'KiB')

def hero(phase=0):
 w,h=1100,430;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');grid(s,46,.043);mountain(s,w,h,phase,550)
 s.rect(0,0,690,h,'url(#shade)')
 s.rect(19,18,w-38,h-36,'none',22,'#638B76',1,opacity=.56)
 s.line(39,75,w-40,75,'#7BA18C',1,.33)
 s.cir(54,46,5,C['mint']);s.tx(71,52,'BIOME / OS',16,C['pale'],800,2)
 s.tx(299,51,'PERSONAL DEVELOPER ENVIRONMENT',11,C['sage'],600,1.8)
 s.pill(909,31,142,'● SYSTEM ONLINE','#173C31',C['mint'],'#4E7C68',h=29,size=10)
 s.tx(55,116,'VOL. 2026     //     FIELD NOTES 001',12,C['mint'],700,2)
 s.tx(52,210,'ANIL',94,C['cream'],800,spacing=-2)
 s.tx(51,297,'SUTHAR',92,C['cream'],800,spacing=-2)
 s.rect(55,317,105,4,'url(#mint)',2)
 s.tx(177,326,'CLOUD  /  DEVOPS  /  AI  /  PRODUCT',16,C['pale'],600,1.2)
 s.tx(55,356,'Engineering useful things at the edge of imagination.',17,'#C3D5C5',400)
 # terminal status window overlays vista
 s.rect(692,253,352,122,'#112D27',13,'#70977D',1,opacity=.94)
 s.rect(692,253,352,32,'#244B3D',13,opacity=.93)
 for i,color in enumerate(['#E2A178','#DFD28F','#70CDA9']):s.cir(710+i*18,268,4,color)
 s.tx(778,273,'~/anil / mission.log',12,'#D3E2D1',600)
 s.tx(710,308,'$ cat current_mission.txt',12,C['mint'],600)
 s.tx(710,332,'> build • iterate • automate • ship',13,C['cream'],500)
 s.tx(710,355,'> stay curious'+ ('_' if phase<.5 else ' '),13,C['gold'],600)
 s.tx(1000,401,'EST. 2023   •   BENGALURU',10,C['sage'],600,1,anchor='end')
 s.line(39,392,670,392,'#7BA18C',1,.33)
 s.tx(53,408,'SCROLL TO EXPLORE  v',10,C['sage'],700,2)
 # tiny cursor spark on systems status
 s.cir(1011+5*math.sin(2*math.pi*phase),46,3.5,C['mint'],opacity=.1)
 return s

def section_bar():
 s=S(1100,94);s.rect(0,0,1100,94,C['bg']);grid(s,32,.035)
 s.rect(1,1,1098,92,'none',13,C['line'],1)
 for idx,(a,b) in enumerate([('01','THE PERSON'),('02','THE BUILDS'),('03','THE STACK'),('04','THE PROCESS')]):
  x=33+idx*271;s.cir(x,43,13,'#284B3B','#6A9A7E',1);s.tx(x,47,a,9,C['mint'],800,anchor='middle');s.tx(x+25,46,b,16,C['pale'],700,1)
  if idx<3:s.line(x+229,19,x+229,76,C['line'],1,.85)
 return s

def telemetry():
 s=S(1100,235);s.rect(0,0,1100,235,'url(#bg)');grid(s,40,.025)
 s.rect(1,1,1098,233,'none',16,C['line'],1)
 label(s,35,37,'01','AT A GLANCE');s.tx(817,37,'TRACK RECORD / HUMAN EDITION',11,C['faint'],600,1)
 items=[('01','CLOUD NATIVE','Cloud foundations','Containers & orchestration'),('02','APPLIED AI','Models into workflows','LLMs, vision & automation'),('03','ENGINEERING','Build. Test. Repeat.','Scripts, APIs & CI/CD'),('04','CREATIVE TECH','Beyond the terminal','3D, games & product UX')]
 for i,(n,title,desc,sub) in enumerate(items):
  x=28+i*268;s.rect(x,64,248,139,'#15382E',12,'#4A7762',1)
  s.tx(x+18,93,n+' /',11,C['mint'],700,2)
  s.tx(x+19,120,title,17,C['cream'],800,1)
  s.tx(x+19,152,desc,14,C['pale'],500)
  s.tx(x+19,179,sub,11,'#9EBEAC',500)
  for k in range(3):s.rect(x+195+k*9,87,5,14+(k%2)*8,C['teal'],2,opacity=.45+k*.19)
 return s

def identity():
 s=S(520,342);s.rect(0,0,520,342,'url(#bg)');s.rect(3,3,514,335,'none',15,C['line'],1)
 grid(s,35,.045)
 label(s,28,35,'ACTIVE','PROFILE CARD')
 s.rect(24,55,472,112,'#193C32',14,'#4C7763',1)
 s.cir(70,109,29,'#37624D','#8EB79F',1.5)
 # geometric mountain emblem
 s.path('M51 120 L67 91 L82 119 Z','#ABD4B4');s.path('M62 121 L77 100 L92 121 Z','#61AC91')
 s.tx(115,96,'Anil Suthar',25,C['cream'],800)
 s.tx(115,119,'B.Tech  ·  Cloud Computing',14,C['pale'],500)
 s.tx(115,140,'Alliance University, Bengaluru',12,C['sage'],500)
 s.pill(28,183,175,'NOW   ·   AI INTERN',h=33,size=12)
 s.pill(214,183,277,'2023–2027   ·   ENGINEERING',h=33,size=12)
 for idx,(key,val) in enumerate([('FOCUS','Applied AI & cloud systems'),('MODE','Curious. Pragmatic. Iterative.'),('BASE','Bengaluru, India')]):
  y=249+idx*28;s.tx(30,y,key,11,C['mint'],700,1);s.tx(116,y,val,12,C['pale'],500)
 return s

def project(which):
 specs={
 'prompt':('01','PROMPT FORGE','STUDIO','PROMPT ENGINEERING','NEXT.JS  /  GEMINI','#62DDB0'),
 'gini':('02','GINI 2.0','', 'AI COMPANION','TELEGRAM  /  GEMINI','#D4C18A'),
 'imperium':('03','IMPERIUM','', 'COMMUNITY AUTOMATION','DISCORD  /  BOT','#B1B4ED'),
 'quantum':('04','QUANTUMFLOW','BLR', 'TRAFFIC SYSTEMS RESEARCH','VISION  /  SUMO  /  QUBO','#84C5C0')}
 n,name,second,kicker,tags,accent=specs[which]
 w,h=536,293;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');grid(s,35,.034);s.rect(2,2,w-4,h-4,'none',14,'#567D66',1)
 s.tx(27,40,'PROJECT   /   '+n,12,accent,800,2)
 s.tx(510,40,'●   FIELD EXPERIMENT',10,C['sage'],600,1,anchor='end')
 s.line(25,56,511,56,'#547565',1,.7)
 # pseudo-interface vignette right
 s.rect(302,80,207,155,'#22473D',15,'#658C77',1)
 s.rect(302,80,207,32,'#345C4D',12)
 for i,col in enumerate([C['orange'],C['gold'],C['mint']]):s.cir(321+i*14,96,3,col)
 if which=='prompt':
  for i,(a,b,c) in enumerate([('SYSTEM','You are a useful...',''),('CONTEXT','Knowledge + goals',''),('OUTPUT','Structured + reliable','')]):
   y=128+i*31;s.rect(317,y,176,25,'#183A31',5);s.tx(326,y+10,a,7,accent,700,1);s.tx(326,y+20,b,9,C['pale'],500)
 elif which=='gini':
  s.cir(352,145,18,accent,opacity=.7);s.tx(352,150,'✦',21,C['bg'],700,anchor='middle')
  for i,l in enumerate(['Query understood','Signal cross-checked','Response composed']):
   y=127+i*31;s.rect(377,y,115,25,'#173A31',7);s.tx(385,y+16,l,9,C['pale'])
 elif which=='imperium':
  for i,l in enumerate(['MODERATION','COMMUNITY','AUTOMATION']):
   y=126+i*31;s.cir(329,y+9,5,accent,opacity=.65);s.tx(344,y+13,l,10,C['pale'],600,1);s.line(319,y+25,486,y+25,'#668779',1,.35)
 elif which=='quantum':
  for i in range(5):
   s.line(322+i*35,127,322+i*35,201,C['faint'],1,.22)
  for j in range(3):s.line(319,131+j*32,487,131+j*32,C['faint'],1,.22)
  s.path('M320 190 L362 167 L393 173 L420 142 L455 150 L490 126',stroke=accent,sw=3)
  for x,y in [(320,190),(362,167),(393,173),(420,142),(455,150),(490,126)]:s.cir(x,y,3.5,accent)
 # leaf line-art ornament bottom right
 s.path('M472 263 Q488 256 501 242 M486 249 Q488 237 502 236 M493 244 Q479 241 474 228',stroke='#89BB9B',sw=1,op=.55)
 s.tx(27,96,kicker,11,accent,700,1.2)
 s.tx(26,147,name,33,C['cream'],800,spacing=-.9)
 if second:s.tx(27,180,second,30,C['cream'],800)
 s.tx(27,216,'EXPLORE THE BUILD  >',11,C['mint'],700,1.1)
 s.rect(26,246,267,27,'#294D3F',10)
 s.tx(37,264,tags,10,C['pale'],600,1)
 return s

def ecosystem():
 w,h=1100,390;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');grid(s,37,.045);s.rect(1,1,w-2,h-2,'none',16,'#456D5C',1)
 label(s,31,39,'03','THE ECOSYSTEM');s.tx(32,74,'One toolbox. Many kinds of problems.',25,C['cream'],700)
 s.tx(32,98,'Systems, intelligence, and interfaces connected into one build practice.',13,C['muted'])
 # node graph
 nodes=[(175,175,'FOUNDATIONS','C / C++ / JAVA','#D6BD80'),(430,151,'CLOUD + DEVOPS','AWS / DOCKER / K8S','#7BDBAC'),(684,160,'APPLIED AI','PYTHON / LLMS / CV','#81CADA'),(934,177,'PRODUCT','NEXT.JS / API / UX','#DDAA98'),(374,286,'AUTOMATION','CI/CD / BASH / LINUX','#A0C58E'),(762,288,'CREATIVE TECH','UNREAL / UNITY / 3D','#D1B5DE')]
 edges=[(0,1),(1,2),(2,3),(0,4),(1,4),(2,5),(3,5),(4,5)]
 for a,b in edges:
  x,y,*_=nodes[a];x2,y2,*_=nodes[b]
  s.path(f'M{x} {y} Q{(x+x2)/2} {min(y,y2)-12} {x2} {y2}',stroke='#5B9780',sw=2,op=.38)
  for k in range(1,4):
   t=k/4; xx=(1-t)*x+t*x2; yy=(1-t)*y+t*y2-12*math.sin(math.pi*t)
   s.cir(xx,yy,2,C['mint'],opacity=.30)
 for i,(x,y,title,desc,accent) in enumerate(nodes):
  s.cir(x,y,46,'#102920','#547B68',1.2)
  s.cir(x,y,39,'#1D4739')
  s.cir(x,y-19,5,accent);s.tx(x,y+3,f'{i+1:02d}',18,C['cream'],800,anchor='middle')
  s.tx(x,y+65,title,12,C['cream'],800,1,anchor='middle')
  s.tx(x,y+81,desc,9,'#A3C2B2',600,anchor='middle')
 return s

def stack_ribbon():
 w,h=1100,328;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');grid(s,36,.032);s.rect(1,1,w-2,h-2,'none',15,C['line'],1)
 label(s,30,36,'03.1','SYSTEM MODULES')
 rows=[('LANGUAGES & FRAMEWORKS',['Python','C','C++','Java','JavaScript','TypeScript','Next.js'],C['mint']),
       ('PLATFORM & DEVOPS',['AWS','Azure','Docker','Kubernetes','Linux','Bash','Git / CI-CD'],C['sage']),
       ('AI & CREATIVE',['LLM APIs','Prompt Eng.','Vision','Automation','Unreal','Unity','Blender'],C['gold'])]
 for ri,(title,items,accent) in enumerate(rows):
  top=65+ri*88;s.tx(30,top,title,12,accent,700,1.6)
  for j,t in enumerate(items):
   xx=30+j*151;yy=top+15
   s.rect(xx,yy,138,47,'#1D4336',10,'#4A7661',1)
   s.cir(xx+17,yy+23,5,accent,opacity=.8)
   s.tx(xx+29,yy+29,t,14,C['pale'],600)
 return s

def pipeline(phase=0):
 w,h=1100,240;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');grid(s,33,.03);s.rect(1,1,w-2,h-2,'none',16,C['line'],1)
 label(s,30,39,'04','BUILD LOOP');s.tx(30,79,'From a small idea to something that ships.',23,C['cream'],700)
 steps=[('DISCOVER','Find the real problem'),('PROTOTYPE','Make it tangible'),('VALIDATE','Test what matters'),('AUTOMATE','Remove friction'),('SHIP','Learn from reality')]
 y=138
 for i,(n,sub) in enumerate(steps):
  x=47+i*213
  s.cir(x+36,y,23,'#17392F','#63977B',2)
  if i<=phase*5:s.cir(x+36,y,16,C['mint'],opacity=.25)
  s.tx(x+36,y+5,str(i+1),17,C['cream'],800,anchor='middle')
  s.tx(x+36,185,n,12,C['cream'],800,1,anchor='middle')
  s.tx(x+36,201,sub,10,C['muted'],500,anchor='middle')
  if i<4:
   s.line(x+64,y,x+175,y,'#61967D',2,.5)
   end=min(1,max(0,phase*5-i));s.line(x+64,y,x+64+111*end,y,C['mint'],3,.8)
   s.path(f'M{x+169} {y-4} L{x+176} {y} L{x+169} {y+4}',stroke=C['sage'],sw=2)
 s.tx(1050,45,'PROGRESS   •   ALWAYS ITERATING',10,C['sage'],600,1,anchor='end')
 s.cir(1054,223,4,C['mint'] if phase>.45 else '#537865')
 return s

def terminal(phase=0):
 w,h=1100,269;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');s.rect(1,1,w-2,h-2,'none',15,C['line'],1)
 s.rect(17,16,1066,237,'#102C24',13,'#567E69',1)
 s.rect(17,16,1066,37,'#234738',12)
 for i,col in enumerate(['#E3A77C','#D8C58A','#8FD7B5']):s.cir(39+i*18,34,5,col)
 s.tx(123,40,'anil@biome-os : ~/workspace/philosophy.md',13,C['pale'],600)
 s.tx(1055,39,'LIVE / NOT REALLY  ·  A PERSONAL MANIFESTO',10,C['sage'],600,1,anchor='end')
 s.tx(43,91,'$ cat philosophy.md',17,C['mint'],700)
 lines=['> Think independently. Design intentionally.','> Use AI as leverage, not a substitute for understanding.','> Keep the interface human, the system dependable.','> Document the edges. Test the weird cases.','> Ship useful work. Stay curious.']
 for i,l in enumerate(lines):
  s.tx(43,127+i*22,l,15,C['pale'] if i%2==0 else C['sage'],500)
 s.tx(44,246,'$'+(' _' if phase<.5 else '  '),14,C['mint'],700)
 # right 
 s.cir(952,163,65,'#1A4336',opacity=.75)
 for i in range(4):s.cir(952,163,18+i*13,'none','#B0D8AF',1,opacity=.14+i*.06)
 s.path('M952 208 L952 126 M952 157 C926 138 926 125 929 123 C960 121 966 146 952 157 M952 183 C975 155 993 160 996 162 C991 191 965 196 952 183',stroke=C['mint'],sw=2,op=.8)
 return s

def footer():
 w,h=1100,178;s=S(w,h);s.rect(0,0,w,h,'url(#bg)');grid(s,41,.033)
 s.cir(902,76,92,'url(#glow)');s.cir(901,72,30,C['gold'],opacity=.57)
 s.path('M0 132 L230 93 L360 129 L555 90 L676 128 L842 87 L1000 120 L1100 84 L1100 178 L0 178 Z','#2B594A',op=.9)
 s.path('M0 159 L120 142 L320 163 L470 127 L630 155 L830 134 L1100 155 L1100 178 L0 178 Z','#173E33')
 s.tx(34,61,'GOOD IDEAS GROW HERE.',32,C['cream'],800)
 s.tx(35,94,'Let’s make something worth using.',18,C['pale'])
 s.tx(35,132,'PORTFOLIO  /  GITHUB  /  LINKEDIN',12,C['mint'],700,2)
 s.tx(1064,167,'ANIL SUTHAR  •  2026',10,C['pale'],700,anchor='end',opacity=.8)
 return s

if __name__=='__main__':
 save_png(hero(.16),'hero-still.png')
 save_gif([save_png(hero(i/20),f'_temp_{i:02}.png') for i in range(20)],'hero-loop.gif',duration=125)
 for p in A.glob('_temp_*.png'):p.unlink()
 save_png(section_bar(),'section-bar.png')
 save_png(telemetry(),'telemetry.png')
 save_png(identity(),'identity.png')
 for n in ['prompt','gini','imperium','quantum']:save_png(project(n),f'project-{n}.png')
 save_png(ecosystem(),'ecosystem.png')
 save_png(stack_ribbon(),'stack-ribbon.png')
 save_png(pipeline(.65),'pipeline-still.png')
 save_gif([save_png(pipeline(i/25),f'_step_{i:02}.png') for i in range(25)],'pipeline-loop.gif',duration=110)
 for p in A.glob('_step_*.png'):p.unlink()
 save_png(terminal(.1),'terminal.png')
 save_png(footer(),'footer.png')
 print('done')
