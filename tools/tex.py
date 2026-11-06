# GRX texture: 0x80 header (w,h,lw,lh,psm,?,?,datasize,dataoff,...), pixels, then RGBA palette
import struct,numpy as np
from PIL import Image
def is_tex(b,o=0):
    if len(b)<o+0x80: return False
    w,h,lw,lh,psm=struct.unpack_from('<5I',b,o)
    if psm not in (0,0x13,0x14) or w==0 or h==0 or w>1024 or h>1024: return False
    if (1<<lw)!=w or (1<<lh)!=h: return False
    ds,do=struct.unpack_from('<II',b,o+0x18)
    return do==0x80 and ds>={0:w*h*4,0x13:w*h,0x14:w*h//2}[psm]
def info(b,o=0):
    w,h,lw,lh,psm=struct.unpack_from('<5I',b,o); ds=struct.unpack_from('<I',b,o+0x18)[0]
    n={0:0,0x13:256,0x14:16}[psm]
    return w,h,psm,o+0x80,o+struct.unpack_from('<I',b,o+0x40)[0],n
def unswz(i): return (i&0xe7)|((i&8)<<1)|((i&16)>>1)
def decode(b,o=0):
    w,h,psm,po,pal,n=info(b,o)
    if psm==0:
        a=np.frombuffer(b,np.uint8,w*h*4,po).reshape(h,w,4).copy(); a[...,3]=np.minimum(255,a[...,3].astype(int)*2); return a
    P=np.frombuffer(b,np.uint8,n*4,pal).reshape(n,4).copy()
    if n==256: P=P[[unswz(i) for i in range(256)]]
    P[:,3]=np.minimum(255,P[:,3].astype(int)*2)
    if psm==0x13: idx=np.frombuffer(b,np.uint8,w*h,po)
    else:
        r=np.frombuffer(b,np.uint8,w*h//2,po); idx=np.empty(w*h,np.uint8); idx[0::2]=r&15; idx[1::2]=r>>4
    return P[idx].reshape(h,w,4)
def png(b,o,path): Image.fromarray(decode(b,o),'RGBA').save(path)
