# repaint Japanese text in GRX textures with Korean, re-encode into the same slot
import os,struct,numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from tex import info,decode,unswz
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
FONTS={k:os.path.join(ROOT,'NanumSquareNeo-%s.ttf'%v) for k,v in
       dict(L='aLt',R='bRg',B='cBd',E='dEb',H='eHv').items()}
def erase(a,box,mode='clear'):
    x0,y0,x1,y1=box
    if mode=='clear': a[y0:y1,x0:x1]=0; return
    # interpolate each row between the columns just outside the box
    L=a[y0:y1,max(x0-1,0)].astype(np.float32); R=a[y0:y1,min(x1,a.shape[1]-1)].astype(np.float32)
    if mode=='v':
        T=a[max(y0-1,0),x0:x1].astype(np.float32); B=a[min(y1,a.shape[0]-1),x0:x1].astype(np.float32)
        t=np.linspace(0,1,y1-y0)[:,None,None]
        a[y0:y1,x0:x1]=np.clip(T[None]*(1-t)+B[None]*t,0,255).astype(np.uint8); return
    t=np.linspace(0,1,x1-x0)[None,:,None]
    a[y0:y1,x0:x1]=np.clip(L[:,None]*(1-t)+R[:,None]*t,0,255).astype(np.uint8)
def text(a,box,s,fill=(255,255,255),stroke=None,sw=1,font='B',size=None,align='l',grad=None,shadow=None):
    x0,y0,x1,y1=box; W,H=x1-x0,y1-y0
    size=size or H
    f=ImageFont.truetype(FONTS[font],size)
    bb=f.getbbox(s,stroke_width=sw if stroke else 0)
    tw,th=bb[2]-bb[0],bb[3]-bb[1]
    pad=4
    lay=Image.new('RGBA',(tw+2*pad,th+2*pad),(0,0,0,0)); d=ImageDraw.Draw(lay)
    org=(pad-bb[0],pad-bb[1])
    if shadow: d.text((org[0]+1,org[1]+1),s,font=f,fill=shadow,stroke_width=sw if stroke else 0,stroke_fill=shadow)
    if stroke: d.text(org,s,font=f,fill=fill if not grad else (255,255,255,255),stroke_width=sw,stroke_fill=stroke)
    else: d.text(org,s,font=f,fill=fill if not grad else (255,255,255,255))
    if grad:
        # vertical gradient applied to glyph body only
        m=Image.new('L',lay.size,0); ImageDraw.Draw(m).text(org,s,font=f,fill=255)
        g=np.zeros((lay.size[1],lay.size[0],4),np.uint8)
        c0,c1=np.array(grad[0]),np.array(grad[1]); ys=np.linspace(0,1,lay.size[1])[:,None]
        g[...,:3]=(c0*(1-ys)+c1*ys)[:,None,:].repeat(lay.size[0],1); g[...,3]=np.asarray(m)
        lay.alpha_composite(Image.fromarray(g,'RGBA'))
    tw2=lay.size[0]-2*pad
    if tw2>W:  # squeeze horizontally to fit
        lay=lay.resize((W+2*pad,lay.size[1]),Image.LANCZOS)
    lw,lh=lay.size
    if align=='c': x=x0+(W-(lw-2*pad))//2-pad
    elif align=='r': x=x1-(lw-pad)
    else: x=x0-pad
    y=y0+(H-(lh-2*pad))//2-pad
    base=Image.fromarray(a,'RGBA'); cv=Image.new('RGBA',base.size,(0,0,0,0)); cv.paste(lay,(x,y)); base=Image.alpha_composite(base,cv)
    a[:]=np.asarray(base)
def encode(b,o,a):
    w,h,psm,po,pal,n=info(b,o)
    im=Image.fromarray(a,'RGBA')
    q=im.quantize(colors=n,method=Image.FASTOCTREE,dither=Image.NONE)
    mode=q.palette.mode
    P=np.frombuffer(bytes(q.palette.palette),np.uint8)
    P=P.reshape(-1,len(mode))[:n]
    if len(mode)==3: P=np.concatenate([P,np.full((len(P),1),255,np.uint8)],1)
    P=np.vstack([P,np.zeros((n-len(P),4),np.uint8)])
    idx=np.asarray(q,np.uint8).ravel()
    st=P.copy(); st[:,3]=(P[:,3].astype(int)*128+127)//255
    if n==256: st=st[[unswz(i) for i in range(256)]]
    b[pal:pal+n*4]=st.tobytes()
    if psm==0x13: b[po:po+w*h]=idx.tobytes()
    else: b[po:po+w*h//2]=(idx[0::2]|(idx[1::2]<<4)).astype(np.uint8).tobytes()
def load(b,o): return decode(bytes(b),o).copy()
