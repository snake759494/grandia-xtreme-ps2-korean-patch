import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from gxtext import MAP,glyph_of
def inner_len(b,i):
    c=b[i]
    if c in (3,6,7,8,9,10,0xc,0xe,0xf,0x10,0x11,0x12,0x16,0x19,0x1a,0x1b,0x1f): return 1
    if c in (4,0x1c,0x1e): return 2
    if c in (5,0xb,0x18): return 3
    if c in (0x13,0x14): return 6
    if c==0x15: return 5
    if c==0xd:
        s=b[i+1]; return 10 if s==0 else 3 if s in(2,3) else 2
    if c==0x17:
        s=b[i+1]; return 4 if s in(0x20,0x40) else 2
    if c==0x1d: return 3 if b[i+1]==0xff else 4
    return None
def parse(b,i):
    """parse message body from i; returns (tokens,end) end= index after 17 00, or None"""
    toks=[];n=len(b)
    while i<n:
        c=b[i]
        if c>=0x20:
            if i+1<n and b[i+1]>=0xf0: code=c|b[i+1]<<8; L=2
            else: code=c;L=1
            g=glyph_of(code)
            if g>=len(MAP): return None
            toks.append(('c',MAP[g],b[i:i+L])); i+=L; continue
        if c in (0,1,2): return None
        L=inner_len(b,i)
        if L is None: return None
        if c==0x17 and b[i+1]==0: return toks,i+2
        toks.append(('x',None,b[i:i+L])); i+=L
    return None
