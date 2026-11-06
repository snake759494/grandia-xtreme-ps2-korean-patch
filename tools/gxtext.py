import os
HERE=os.path.dirname(os.path.abspath(__file__))
MAP=open(os.path.join(HERE,'..','translation','charmap_jp.txt'),encoding='utf8').read()
def glyph_of(code):
    if code<0x100: return code-0x20
    return ((code>>8&0xf)+1)*0xd0-0x20+(code&0xff)
def code_of(g):
    if g<0xd0: return g+0x20
    p=(g+0x20)//0xd0-1; lo=g+0x20-(p+1)*0xd0
    return 0xf000|p<<8|lo
def decode(b,i=0,stop0=True):
    s=[];n=len(b)
    while i<n:
        c=b[i]
        if c==0 and stop0: break
        if i+1<n and b[i+1]>=0xf0:
            code=c|b[i+1]<<8; i+=2
        else:
            code=c; i+=1
        if code<0x20: s.append('{%02X}'%code); continue
        g=glyph_of(code)
        s.append(MAP[g] if 0<=g<len(MAP) else '{%X}'%code)
    return ''.join(s),i
REV={}
for _i,_c in enumerate(MAP):
    REV.setdefault(_c,_i)
def encode_jp(s):
    out=bytearray()
    for ch in s:
        c=code_of(REV[ch])
        if c<0x100: out.append(c)
        else: out+=bytes([c&0xff,c>>8])
    return bytes(out)
