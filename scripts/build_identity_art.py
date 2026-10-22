#!/usr/bin/env python3
"""Create GitHub-compatible personal identity SVG artwork (no JS, fonts or external dependencies)."""
from pathlib import Path
from html import escape
import math
O=Path(__file__).resolve().parents[1]/'assets'
O.mkdir(exist_ok=True)
C={'bg':'#071315','text':'#E6FFF4','muted':'#97BFB6','mint':'#68F1AE','teal':'#71E0DC','gold':'#F6CA87','line':'#2F6559'}
def txt(x,y,s,fs=20,color=None,weight=500,mono=False,anchor=None,ls=None):
 a=f' x="{x}" y="{y}" fill="{color or C["text"]}" font-size="{fs}" font-weight="{weight}" font-family="'+ ('DejaVu Sans Mono, Courier New, monospace' if mono else 'Arial, Helvetica, sans-serif')+'"'
 if anchor:a+=f' text-anchor="{anchor}"'
 if ls:a+=f' letter-spacing="{ls}"'
 return f'<text{a}>{escape(str(s))}</text>'
def rect(x,y,w,h,r=0,stroke=None,fill='none',sw=1,opacity=1):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}" opacity="{opacity}"/>'
def line(x1,y1,x2,y2,c=None,op=.6,w=1):
 return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{c or C["line"]}" stroke-width="{w}" fill="none" opacity="{op}"/>'
def circle(x,y,r,stroke=None,fill='none',sw=1,op=1):
 return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke or "none"}" stroke-width="{sw}" opacity="{op}"/>'
def base(w,h,label):
 return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<title>{escape(label)}</title><defs>
<linearGradient id="surface" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#091C1F"/><stop offset="1" stop-color="#061013"/></linearGradient>
<linearGradient id="beam"><stop stop-color="#68F1AE" stop-opacity="0"/><stop offset=".5" stop-color="#68F1AE" stop-opacity=".9"/><stop offset="1" stop-color="#68F1AE" stop-opacity="0"/></linearGradient>
<radialGradient id="halo"><stop stop-color="#58DEA6" stop-opacity=".22"/><stop offset=".45" stop-color="#58DEA6" stop-opacity=".09"/><stop offset="1" stop-color="#58DEA6" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="29" height="29" patternUnits="userSpaceOnUse"><path d="M29 0H0V29" fill="none" stroke="#54867C" stroke-width=".7" opacity=".15"/></pattern>
<pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r=".75" fill="#6AADA0" opacity=".25"/></pattern>
</defs>{rect(0,0,w,h,0,fill='url(#surface)')}{rect(0,0,w,h,0,fill='url(#grid)')}{rect(1,1,w-2,h-2,0,stroke='#2F685B',sw=2)}
{line(28,21,w-28,21,C['mint'],.6,2)}'''
def end(s,filename):
 (O/filename).write_text(s+'</svg>',encoding='utf-8')
# Personal operator identity — all source-derived, no fabricated person/life details.
s=base(1080,460,'Operator file: CYANEX1702, builder across AI systems and native software')
s+=rect(28,43,1024,392,14,stroke='#356A5F',fill='#071316',sw=1.2)
s+=txt(56,82,'OPERATOR FILE    //    ID 17.02',16,C['mint'],700,True,ls=2)
s+=txt(55,151,'THE PERSON',57,C['text'],800)
s+=txt(55,210,'BEHIND THE',57,C['text'],800)
s+=txt(55,269,'SYSTEM.',57,C['mint'],800)
s+=txt(57,314,'AI  /  SOFTWARE  /  SYSTEMS THINKING',17,C['teal'],650,True)
s+=line(56,333,562,333,C['line'],1,1.5)
s+=txt(56,365,'FROM FIRST PRINCIPLE TO FINISHED SOFTWARE',15,C['muted'],500,True)
s+=txt(56,391,'MODE: LEARN  ·  EXPERIMENT  ·  BUILD  ·  SHIP',14,C['muted'],500,True)
# custom creative silhouette: abstract operator presence, not an actual portrait
s+='<ellipse cx="841" cy="235" rx="202" ry="205" fill="url(#halo)"/>'
for r,o in [(165,.21),(140,.36),(116,.38)]: s+=circle(836,235,r,C['teal'],'none',1.4,o)
for k in range(20):
 a=2*math.pi*k/20; x=836+167*math.cos(a);y=235+167*math.sin(a)
 s+=circle(round(x,1),round(y,1),2.6,C['mint'],C['mint'],.4,.66 if k%3==0 else .32)
# helmet-ish abstract, clearly not a real face
s+=f'<path d="M780 314Q783 269 815 260Q760 235 763 186C764 145 792 120 834 121C878 122 904 154 901 194Q900 238 863 260Q907 273 912 314" fill="#0A2727" stroke="{C["mint"]}" stroke-width="2.4"/>'
s+=f'<path d="M772 188Q839 207 906 180" fill="none" stroke="{C["teal"]}" stroke-width="2" opacity=".7"/>'
s+=f'<path d="M803 217H870M821 232H854" fill="none" stroke="{C["mint"]}" opacity=".65" stroke-width="2"/>'
s+=rect(768,335,150,40,7,stroke='#388576',fill='#092321')+txt(843,361,'CYANEX1702',17,C['text'],700,True,'middle')
s+=txt(839,416,'NOT A FACE · AN IDENTITY',12,C['muted'],500,True,'middle')
end(s,'operator-identity.svg')
# six discipline nodes with a center. Not projects or repository listings.
s=base(1080,538,'My engineering map: generative AI, vision, RAG, local AI, native apps and media/data')
s+=txt(42,65,'01   /   THE MENTAL MODEL',16,C['mint'],750,True,ls=2)
s+=txt(41,117,'ONE MIND. MANY SYSTEMS.',40,C['text'],800)
s+=txt(44,145,'The interesting work happens where disciplines meet.',17,C['muted'])
cy=326; cx=540
s+='<ellipse cx="540" cy="324" rx="232" ry="193" fill="url(#halo)"/>'
for r in [144,118,83]: s+=circle(cx,cy,r,C['mint'] if r==118 else C['teal'],'none',1.4,.4)
for k in range(60):
 a=k*math.tau/60;inner=147 if k%5 else 139; outer=157 if k%5 else 168
 s+=line(round(cx+inner*math.cos(a),1),round(cy+inner*math.sin(a),1),round(cx+outer*math.cos(a),1),round(cy+outer*math.sin(a),1),C['teal'],.40,1.2)
s+=circle(cx,cy,73,fill='#092423',stroke=C['mint'],sw=1.8,op=1)
s+=txt(cx,311,'SYSTEMS',24,C['text'],800,True,'middle')
s+=txt(cx,341,'THINKING',24,C['mint'],800,True,'middle')
s+=txt(cx,368,'CORE / 17.02',12,C['muted'],500,True,'middle')
# cards left/right
nodes=[('GEN AI','Diffusion + multimodal',48,189,C['mint']),('COMPUTER VISION','Segmentation + images',48,302,C['teal']),('RETRIEVAL / RAG','Context + vector search',48,415,C['gold']),('LOCAL AI','On-device inference',763,189,C['mint']),('NATIVE APPS','Desktop + Android',763,302,C['teal']),('MEDIA + DATA','Pipelines + processing',763,415,C['gold'])]
for i,(name,sub,x,y,color) in enumerate(nodes):
 w=269
 s+=rect(x,y,w,88,9,stroke='#34695E',fill='#0C2223')
 s+=rect(x,y,5,88,2,fill=color)
 s+=txt(x+22,y+33,name,18,color,750,True)
 s+=txt(x+22,y+61,sub,14,C['muted'])
 yy=y+42
 ix=x+w if i<3 else x
 xx= cx-142 if i<3 else cx+142
 s+=line(ix,yy,xx,cy+(y-302)*.35,color,.42,1.6)
 s+=circle(ix,yy,3,color,color,1,.8)
s+=txt(541,514,'NOT SIX JOB TITLES. ONE WAY OF CONNECTING THE DOTS.',13,C['muted'],500,True,'middle')
end(s,'mental-model.svg')
# manifesto visual panel
s=base(1080,350,'My engineering principles: think in systems, design for real use, build beyond the demo')
s+=txt(40,65,'03   /   HOW I WORK',16,C['mint'],750,True,ls=2)
s+=txt(40,115,'ENGINEERING IS A PRACTICE.',37,C['text'],800)
s+=txt(41,143,'What matters to me when technology leaves the screen.',17,C['muted'])
ideas=[('01','THINK IN SYSTEMS','The model is a component.','Architecture is the craft.',C['mint']),('02','DESIGN FOR REAL USE','Make complexity usable.','Respect the machine and user.',C['teal']),('03','BUILD BEYOND THE DEMO','Test the edges.','Keep improving. Then ship.',C['gold'])]
for i,(n,title,l1,l2,color) in enumerate(ideas):
 x=37+i*347
 s+=rect(x,169,324,153,10,stroke='#315D55',fill='#0A2021')
 s+=rect(x,169,324,3,0,fill=color,opacity=.8)
 s+=txt(x+20,206,n,25,color,750,True)
 s+=txt(x+20,241,title,18,C['text'],750,True)
 s+=txt(x+20,272,l1,15,C['muted'])+txt(x+20,295,l2,15,C['muted'])
end(s,'engineering-principles.svg')
print('Created operator-identity.svg, mental-model.svg, engineering-principles.svg')
# Tiny self-hosted navigation keys; no dependence on an external badge host.
for ix,(slug,name,wide) in enumerate([('whoami','WHOAMI',158),('mindset','MINDSET',163),('specs','SPECS',140),('principles','PRINCIPLES',191),('signal','SIGNAL',145)]):
 s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{wide}" height="33" viewBox="0 0 {wide} 33" role="img" aria-label="{ix:02d} {name}">'\
 +f'<rect x=".5" y=".5" rx="5" width="{wide-1}" height="32" fill="#0D2625" stroke="#37816B"/>'\
 +f'<rect x="1" y="1" rx="4" width="38" height="31" fill="#5DE7A6"/>'\
 +txt(20,22,f'{ix:02d}',15,'#061816',850,True,'middle')\
 +txt(48,22,name,14,'#D5FAE9',750,True)+'</svg>'
 (O/f'nav-{slug}.svg').write_text(s)
