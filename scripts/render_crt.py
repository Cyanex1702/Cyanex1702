#!/usr/bin/env python3
"""Render raster GIF artwork for CYANEX1702's GitHub profile.
No network calls, no external image assets, no hidden font requirements in the README.
Pillow and NumPy required to regenerate: python -m pip install Pillow numpy.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import math, random
import numpy as np

OUT=Path(__file__).resolve().parent.parent/'assets'
OUT.mkdir(exist_ok=True)
FONT_B='/usr/share/fonts/opentype/inter/Inter-Black.otf'
FONT_S='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
FONT_M='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
FONTS={}
def font(px, style='mono'):
    key=(px,style)
    if key not in FONTS:
        FONTS[key]=ImageFont.truetype({'big':FONT_B,'semi':FONT_S,'mono':FONT_M}[style],px)
    return FONTS[key]

INK='#020905'; DEEP='#06150B'; GRID=(17,53,28); GREEN='#63FF81'; BRIGHT='#D8FFE0'; MUTED='#69A67A'; GLOW='#20C94D'; TEAL='#6ACFB1'; AMBER='#DCE782'; DIM='#26543A'

def draw_text(d,xy,s,sz=15,fill=BRIGHT,style='mono',spacing=None):
    d.text(xy,s,font=font(sz,style),fill=fill,spacing=spacing or 3)

def panel(im,title,tag):
    w,h=im.size; d=ImageDraw.Draw(im,'RGBA')
    d.rectangle((11,11,w-12,h-12),outline=(41,144,70,170),width=2)
    d.line((29,11,100,11),fill=(134,255,159,250),width=3)
    d.line((w-100,h-12,w-29,h-12),fill=(134,255,159,250),width=3)
    for x,dir in ((11,1),(w-12,-1)):
        for y,dy in ((11,1),(h-12,-1)):
            d.line((x,y,x+17*dir,y),fill=(153,255,169,240),width=2)
            d.line((x,y,x,y+17*dy),fill=(153,255,169,240),width=2)
    d.rectangle((30,23,w-30,52),fill=(5,19,11,200))
    draw_text(d,(39,29),title,13,GREEN)
    bb=d.textbbox((0,0),tag,font=font(12)); draw_text(d,(w-bb[2]-40,29),tag,12,MUTED)
    d.line((30,59,w-30,59),fill=(43,104,56,180),width=1)

def scanlines(im,t):
    layer=Image.new('RGBA', im.size,(0,0,0,0));d=ImageDraw.Draw(layer); w,h=im.size
    for y in range(1,h,4):
        d.line((0,y,w,y),fill=(0,0,0,45),width=1)
    # rolling sweep of the electron beam - a slim green-white trace
    sy=int(((t*19)%(h+100))-50)
    d.rectangle((10,sy,w-10,sy+2),fill=(116,255,139,16))
    d.rectangle((10,sy-11,w-10,sy+11),fill=(65,205,100,5))
    im.alpha_composite(layer)
    return im

def base(w,h,seed=17):
    rng=random.Random(seed)
    im=Image.new('RGBA',(w,h),INK)
    d=ImageDraw.Draw(im,'RGBA')
    # fine PCB / CRT reticle grid
    for x in range(0,w,34):d.line((x,0,x,h),fill=(21,67,38,50))
    for y in range(0,h,34):d.line((0,y,w,y),fill=(21,67,38,44))
    for _ in range(95):
        x=rng.randrange(w); y=rng.randrange(h)
        d.point((x,y),fill=(98,250,123,rng.choice([24,35,50,70])))
    return im

def matrix_rain(im,t, region=(0,0,1000,500),density=32,seed=1702):
    layer=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(layer);x0,y0,x1,y1=region
    rng=random.Random(seed)
    glyphs='01ABCDEF<>/::{}|'
    f=font(15)
    for i in range(density):
        x=x0+int((i+.28)*(x1-x0)/density)
        offset=(i*31+rng.randrange(50)+t*(1+(i%3)))%max(10,(y1-y0+180))
        for j in range(9):
            y=int(y0+offset-j*22-90)
            if y0+4<y<y1-2:
                char=glyphs[(t//3+i*7+j*3)%len(glyphs)]
                a=max(4,70-j*8)
                d.text((x,y),char,font=f,fill=(59,244,103,a))
    im.alpha_composite(layer)

def glow_dot(d,x,y,r=3,a=190):
    d.ellipse((x-r-5,y-r-5,x+r+5,y+r+5),fill=(24,215,74,a//6))
    d.ellipse((x-r,y-r,x+r,y+r),fill=(149,255,171,a))

def glow_text(im,xy,s,sz=22,fill=BRIGHT,style='mono',radius=7,glow_color=(24,224,76,145)):
    lay=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.text(xy,s,font=font(sz,style),fill=glow_color)
    gl=lay.filter(ImageFilter.GaussianBlur(radius))
    im.alpha_composite(gl)
    ImageDraw.Draw(im).text(xy,s,font=font(sz,style),fill=fill)

def load_winged_emblem(size=218):
    """Treat supplied winged CYANEX emblem as a phosphor-lit transparency.

    The input image is kept alongside the renderer; black pixels fade away while
    the green illustration glows inside the rotating radar. No generative art.
    """
    source=Image.open(OUT/'cyanex-winged-emblem.png').convert('RGB')
    # Contain the full illustrated silhouette and both wings.
    source=source.resize((size,size),Image.Resampling.LANCZOS)
    a=np.asarray(source,dtype=np.float32)
    # Luminous green linework becomes opacity, dark background recedes.
    intensity=np.maximum(0,a[:,:,1]-10)
    opacity=np.clip((intensity / 180.0)**0.85*255,0,230)
    yy,xx=np.ogrid[:size,:size]
    rr=np.sqrt((xx-(size-1)/2)**2+(yy-(size-1)/2)**2)
    # Feather the edge so the rectangular photo disappears into the CRT glass.
    vignette=np.clip(((size*0.5)-rr)/18.0,0,1)
    opacity*=vignette
    # Tint keeps the design coherent with existing CRT green, avoids gray halos.
    green=np.clip(a[:,:,1]*1.2+25,0,255)
    rgba=np.empty((size,size,4),dtype=np.uint8)
    rgba[:,:,0]=np.uint8(np.clip(green*0.5,0,255))
    rgba[:,:,1]=np.uint8(green)
    rgba[:,:,2]=np.uint8(np.clip(green*0.58,0,255))
    rgba[:,:,3]=opacity.astype(np.uint8)
    return Image.fromarray(rgba,'RGBA')

def write_gif(frames,path,duration=80,colors=96):
    # Optimized RGB -> P mode with global palette helps remove noisy dithering.
    arr=[]
    for x in frames:
        arr.append(x.convert('RGB').quantize(colors=colors,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.NONE))
    arr[0].save(OUT/path,save_all=True,append_images=arr[1:],duration=duration,loop=0,optimize=True,disposal=2)
    print(path,round((OUT/path).stat().st_size/1024/1024,2),'MiB')

# ── 01: cinematic cathode ray / Matrix splash ──
def hero():
    W,H=1100,435; N=42
    bg=base(W,H,seed=1702)
    panel(bg,'BIOS // CYANEX-OS  17.02','CRT SIGNAL: LOCKED    ● LIVE')
    d=ImageDraw.Draw(bg,'RGBA')
    # static data plane and section labels
    d.rounded_rectangle((38,74,668,371),radius=3,fill=(1,9,5,185),outline=(25,72,34,145))
    d.line((64,135,645,135),fill=(29,95,51,155))
    draw_text(d,(66,91),'// PERSONAL TERMINAL  /  AUTHORIZED SESSION',16,TEAL)
    draw_text(d,(67,154),'AI / SOFTWARE BUILDER',22,BRIGHT,'semi')
    draw_text(d,(67,318),'THE MODEL IS ONE COMPONENT.',15,MUTED)
    draw_text(d,(67,341),'THE SYSTEM IS THE THING THAT MATTERS.',15,GREEN)
    d.rectangle((39,391,1060,417),fill=(4,24,11,225))
    draw_text(d,(57,396),'> GENERATIVE_AI    > COMPUTER_VISION    > RAG    > LOCAL_AI    > NATIVE_SYSTEMS',15,GREEN)
    # radar housing
    cx,cy=870,228
    d.rounded_rectangle((700,77,1061,372),radius=7,fill=(2,13,6,180),outline=(35,83,40,170),width=1)
    draw_text(d,(726,90),'NEURAL / CATHODE INTERFACE',12,TEAL)
    d.ellipse((cx-137,cy-137,cx+137,cy+137),outline=(36,97,48,170),width=1)
    d.ellipse((cx-113,cy-113,cx+113,cy+113),outline=(57,164,85,160),width=2)
    d.ellipse((cx-77,cy-77,cx+77,cy+77),outline=(50,143,80,160),width=1)
    for degree in range(0,360,15):
        a=math.radians(degree)
        r0=130 if degree%45 else 124
        d.line((cx+r0*math.cos(a),cy+r0*math.sin(a),cx+139*math.cos(a),cy+139*math.sin(a)),fill=(120,246,144,138),width=2)
    draw_text(d,(760,349),'ID: 0x1702  /  LINK: STABLE',13,GREEN)
    emblem=load_winged_emblem(210)
    emblem_glow=emblem.filter(ImageFilter.GaussianBlur(9))
    frames=[]
    for t in range(N):
        im=base(W,H,seed=1702)
        matrix_rain(im,t,(0,0,W,H),density=52)
        im.alpha_composite(bg)
        dr=ImageDraw.Draw(im,'RGBA')
        # analog scope arcs and sweep over radar
        for j in range(8):
            delta=j*42
            dr.arc((cx-124,cy-124,cx+124,cy+124),start=(t*7+delta)%360,end=(t*7+delta+14)%360,fill=(60,255,99,100+j*16),width=3 if j%2 else 2)
        angle=math.radians((t*8)-90)
        ex=cx+115*math.cos(angle);ey=cy+115*math.sin(angle)
        for q in range(7,0,-1):
            a=math.radians(t*8-90-q*6)
            dr.line((cx,cy,cx+108*math.cos(a),cy+108*math.sin(a)),fill=(44,235,91,max(5,70-q*9)),width=max(1,4-q//2))
        dr.line((cx,cy,ex,ey),fill=(160,255,179,145),width=2)
        # The personal emblem takes the place of the old letter-C glyph.
        # Its original background disappears into the radar as the scan rotates.
        ax=cx-emblem.width//2; ay=cy-emblem.height//2
        pulse=0.68+0.13*math.sin(t/42*math.pi*4)
        flare=emblem_glow.copy()
        flare.putalpha(flare.getchannel('A').point(lambda p:int(p*pulse*.62)))
        im.alpha_composite(flare,(ax,ay))
        crest=emblem.copy()
        crest.putalpha(crest.getchannel('A').point(lambda p:min(255,int(p*(.78+.10*math.sin(t/42*math.pi*4))))))
        im.alpha_composite(crest,(ax,ay))
        dr=ImageDraw.Draw(im,'RGBA')
        dr.arc((cx-101,cy-101,cx+101,cy+101),start=-t*12,end=-t*12+120,fill=(126,255,158,170),width=2)
        dr.arc((cx-113,cy-113,cx+113,cy+113),start=t*9,end=t*9+40,fill=(111,255,141,180),width=4)
        for j in range(7):
            a=math.radians(j*360/7+t*1.1)
            rr=117
            glow_dot(dr,cx+rr*math.cos(a),cy+rr*math.sin(a),2,185)
        dr.text((726,326),f'PHOSPHOR / SCAN {t:03d}',font=font(12),fill=GREEN)
        # title remains large and legible, tiny rare glitch signal in the shadows
        jitter=(-3 if t in (8,9,29) else (2 if t==30 else 0))
        glow_text(im,(60+jitter,184),'CYANEX',79,BRIGHT,'big',9,(40,245,99,135))
        glow_text(im,(65-jitter,245),'1702',77,GREEN,'big',10,(34,215,71,150))
        if t in (8,29):
            dr=ImageDraw.Draw(im,'RGBA')
            dr.rectangle((40,258,653,262),fill=(190,255,199,105))
            dr.rectangle((46,300,660,302),fill=(14,215,61,130))
        # live-looking status is only animation, no fake API values
        dr=ImageDraw.Draw(im,'RGBA')
        dr.ellipse((1040,91,1049,100),fill=(115,255,150,255 if t%12<9 else 50))
        scanlines(im,t)
        frames.append(im)
    write_gif(frames,'crt-boot.gif',duration=90,colors=96)

# ── 02: interactive-feeling terminal, typewriter and diagnostics ──
def operator():
    W,H=1100,327;N=36
    bg=base(W,H,seed=781)
    panel(bg,'SHELL / IDENTITY  /  ~ / WHOAMI','PID 1702  ●  OPERATOR')
    dr=ImageDraw.Draw(bg,'RGBA')
    dr.rounded_rectangle((33,72,689,278),radius=3,fill=(2,16,8,210),outline=(34,90,49,150))
    dr.rounded_rectangle((712,72,1063,278),radius=3,fill=(2,14,6,205),outline=(37,110,54,145))
    draw_text(dr,(52,86),'cyanex@node-17.02:~$ whoami --verbose',18,BRIGHT)
    fields=[('HANDLE','CYANEX1702'),('CLASS','AI / SOFTWARE BUILDER'),('FOCUS','GEN AI / VISION / RETRIEVAL'),('RUNTIME','DESKTOP / ANDROID / LOCAL')]
    for i,(k,v) in enumerate(fields):
        y=132+i*31
        draw_text(dr,(55,y),k.ljust(9),16,MUTED)
        draw_text(dr,(215,y),':: '+v,17,GREEN)
    draw_text(dr,(731,88),'COGNITIVE ACTIVITY',14,TEAL)
    draw_text(dr,(731,265),'DESIGN  >  BUILD  >  BREAK',12,GREEN)
    frames=[]
    for t in range(N):
        im=bg.copy(); d=ImageDraw.Draw(im,'RGBA')
        # little heart/oscilloscope trace, actually moves and breathes
        pts=[]
        for x in range(736,1041,4):
            phase=(x-736+t*13)/36
            spike=(math.sin(phase*2.45)**15)*33 if math.sin(phase*2.45)>0 else 0
            y=189+14*math.sin(phase)+spike
            pts.append((x,y))
        d.line(pts,fill=(31,134,59,50),width=7)
        d.line(pts,fill=(116,255,151,250),width=2)
        d.line((734,209,1043,209),fill=(46,96,59,90),width=1)
        for j in range(19):
            x=740+j*15
            hh=7+int((math.sin((j+t*0.6)*0.85)+1)*11)
            d.rectangle((x,228-hh,x+7,228),fill=(62,245,100,150+int(85*math.sin(j+t/9)**2)))
        if (t//6)%2==0:
            d.rectangle((562,260,572,279),fill=(150,255,176,255))
        draw_text(d,(48,299),'// NO CORPORATE PERSONA INSTALLED',13,MUTED)
        draw_text(d,(711,299),'SYSTEMS > BUZZWORDS',13,GREEN)
        scanlines(im,t)
        frames.append(im)
    write_gif(frames,'whoami-console.gif',duration=100,colors=72)

# ── 03: animated skills as an actual systems constellation ──
def mind():
    W,H=1100,426;N=48;cx,cy=557,242
    bg=base(W,H,seed=991)
    panel(bg,'TOPOLOGY / HOW MY MIND IS WIRED','PACKET ROUTING  ●  LIVE')
    d=ImageDraw.Draw(bg,'RGBA')
    draw_text(d,(49,76),'I CONNECT THE PARTS.',28,BRIGHT,'big')
    draw_text(d,(50,111),'NOT JUST THE MODELS.',15,TEAL)
    positions=[(205,205),(205,313),(905,205),(905,313),(817,103),(570,374)]
    labels=[('GENERATIVE AI','DIFFUSION / INFERENCE'),('COMPUTER VISION','SEGMENTATION / CV'),('RETRIEVAL + RAG','EMBEDDINGS / CONTEXT'),('NATIVE SOFTWARE','RUST / KOTLIN / TAURI'),('LOCAL-FIRST AI','PRIVACY / ON-DEVICE'),('DATA + MEDIA','PYTHON / FFMPEG')]
    for (x,y),(title,desc) in zip(positions,labels):
        left=x-148; top=y-29
        d.rounded_rectangle((left,top,left+296,top+67),radius=5,fill=(2,16,8,236),outline=(50,139,66,196),width=2)
        draw_text(d,(left+15,top+11),title,17,BRIGHT,'semi')
        draw_text(d,(left+15,top+38),desc,12,TEAL)
    # central core chip
    d.ellipse((cx-101,cy-101,cx+101,cy+101),fill=(0,23,10,250),outline=(111,255,149,183),width=2)
    d.ellipse((cx-82,cy-82,cx+82,cy+82),outline=(34,117,57,230),width=1)
    d.ellipse((cx-55,cy-55,cx+55,cy+55),fill=(6,29,11,250),outline=(77,246,119,230),width=2)
    draw_text(d,(cx-34,cy-19),'SYS',26,BRIGHT,'big')
    draw_text(d,(cx-36,cy+18),'CORE',16,GREEN)
    frames=[]
    for t in range(N):
        im=bg.copy(); d=ImageDraw.Draw(im,'RGBA')
        # dynamic routes; route path avoids central text somewhat
        for i, (x,y) in enumerate(positions):
            ang=math.atan2(y-cy,x-cx)
            rx=cx+105*math.cos(ang);ry=cy+105*math.sin(ang)
            endx=x-148 if x>cx else x+148 if x<cx else x
            endy=y+3 if i in (4,5) else y
            if i in (4,5): endx=x; endy=y+34 if i==4 else y-29
            d.line((rx,ry,endx,endy),fill=(30,95,50,170),width=3)
            d.line((rx,ry,endx,endy),fill=(79,188,98,145),width=1)
            a=((t+i*7)%N)/N
            px=rx+(endx-rx)*a;py=ry+(endy-ry)*a
            glow_dot(d,px,py,3,245)
        d.arc((cx-99,cy-99,cx+99,cy+99),start=t*8,end=t*8+36,fill=(142,255,170,238),width=5)
        d.arc((cx-69,cy-69,cx+69,cy+69),start=-t*9,end=-t*9+55,fill=(107,255,159,216),width=3)
        for j in range(12):
            a=math.radians(j*30+t*1.5);r=116
            if j%3==0:glow_dot(d,cx+r*math.cos(a),cy+r*math.sin(a),2,170)
        # redrawing node rectangles over the route endpoints helps readable labels
        for (x,y),(title,desc) in zip(positions,labels):
            left=x-148;top=y-29
            d.rounded_rectangle((left,top,left+296,top+67),radius=5,fill=(2,16,8,245),outline=(50,139,66,204),width=2)
            draw_text(d,(left+15,top+11),title,17,BRIGHT,'semi')
            draw_text(d,(left+15,top+38),desc,12,TEAL)
        d.ellipse((cx-55,cy-55,cx+55,cy+55),fill=(4,24,11,255),outline=(92,252,126,233),width=2)
        draw_text(d,(cx-34,cy-19),'SYS',26,BRIGHT,'big');draw_text(d,(cx-36,cy+18),'CORE',16,GREEN)
        scanlines(im,t)
        frames.append(im)
    write_gif(frames,'neural-topology.gif',duration=95,colors=96)

# ── 04: skill spectrum and technical specs, active VU meters ──
def specs():
    W,H=1100,388;N=36
    bg=base(W,H,seed=159)
    panel(bg,'LSHW / OPERATOR CAPABILITIES','SPEC BUS  ●  ONLINE')
    d=ImageDraw.Draw(bg,'RGBA')
    sections=[('01 / INTELLIGENCE', ['Generative AI', 'Computer Vision / U2NET','RAG / Embeddings','Whisper / Local Models']),
              ('02 / PLATFORMS', ['React / TypeScript','Rust / Tauri', 'Kotlin / Jetpack Compose','Android / Media3']),
              ('03 / SYSTEMS I/O', ['Python / Data Pipelines','FFmpeg / Media','ChromaDB / Vector Search','SQLite / Local Storage'])]
    for i,(title,skills) in enumerate(sections):
        x=35+i*350
        d.rounded_rectangle((x,76,x+335,333),radius=4,fill=(2,15,8,236),outline=(47,115,62,180),width=2)
        draw_text(d,(x+17,92),title,17,GREEN)
        d.line((x+17,123,x+310,123),fill=(30,99,51,200),width=1)
        for j,s in enumerate(skills):
            y=146+j*45
            draw_text(d,(x+17,y),s,15,BRIGHT,'semi')
    d.line((34,349,1068,349),fill=(44,103,60,200))
    draw_text(d,(45,359),'PHILOSOPHY  ::  LOCAL-FIRST  /  PRIVATE BY DESIGN  /  BUILD BEYOND THE DEMO',13,TEAL)
    frames=[]
    for t in range(N):
        im=bg.copy();d=ImageDraw.Draw(im,'RGBA')
        for i in range(3):
            x=35+i*350
            for j in range(4):
                y=170+j*45
                for b in range(12):
                    xx=x+18+b*13
                    # instruments animate, no invented percentages or 'skill levels'
                    active=b<int(2+(t//3+j*3+i*4)%12)
                    d.rectangle((xx,y,xx+8,y+5),fill=(87,247,112,195) if active else (20,61,29,175))
            d.rectangle((x+298,92,x+315,109),fill=(115,255,146,250 if (t+i*4)%18<14 else 55))
        scanlines(im,t)
        frames.append(im)
    write_gif(frames,'specs-rack.gif',duration=100,colors=72)

if __name__=='__main__':
    hero();operator();mind();specs()
