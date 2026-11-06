import numpy as np,os,sys
from PIL import Image,ImageDraw,ImageFont
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..')
FONT=os.path.join(ROOT,'NanumSquareNeo-bRg.ttf'); SIZE=16
def render(ch,font):
    im=Image.new('L',(16,16)); d=ImageDraw.Draw(im)
    d.text((8,8),ch,font=font,fill=255,anchor='mm')
    a=np.asarray(im).astype(np.int32)
    return np.clip((a*15+127)//255,0,15).astype(np.uint8)
def pack(a):
    f=a.reshape(-1)
    return bytes((f[0::2]|(f[1::2]<<4)).astype(np.uint8))
def build(gmap,font_orig,width_orig):
    font=bytearray(font_orig); width=bytearray(width_orig)
    fnt=ImageFont.truetype(FONT,SIZE)
    for g,ch in gmap.items():
        if not ('가'<=ch<='힣'): continue
        a=render(ch,fnt)
        font[g*128:(g+1)*128]=pack(a)
        xs=np.nonzero(a.max(0)>2)[0]
        l,r=(int(xs.min()),int(xs.max())+1) if len(xs) else (0,8)
        width[2*g]=l; width[2*g+1]=r
    width[0]=0; width[1]=7  # narrow space
    font[2107*128:2108*128]=bytes(128); width[2*2107]=0; width[2*2107+1]=3  # BLANK pad / narrow space
    return bytes(font),bytes(width)
