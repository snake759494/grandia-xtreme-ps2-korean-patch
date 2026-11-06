import struct,sys,os,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from msg import parse
from gxtext import MAP,glyph_of
ENT={33:0x1b78c,35:0xf0e0,36:0x480,41:0x19f4}
def entries(b):
    offs=[struct.unpack_from('<I',b,4*i)[0] for i in range(96)]
    return offs
def tok(s):
    out=[];i=0
    while i<len(s):
        c=s[i]
        if i+1<len(s) and s[i+1]>=0xf0: out.append(MAP[glyph_of(c|s[i+1]<<8)]); i+=2
        elif c>=0x20: out.append(MAP[c-0x20]); i+=1
        elif c==0x1f: out.append('|'); i+=1
        else:
            # control: take 1 byte + guess length via msg inner grammar
            from msg import inner_len
            L=inner_len(s,i) or 1
            out.append('{'+s[i:i+L].hex().upper()+'}'); i+=L
    return ''.join(out)
def strings(b):
    offs=entries(b); res=[]
    for k,ps in ENT.items():
        base=offs[k]; e=b[base:offs[k+1]]
        starts=set([ps]+[i+1 for i in range(ps,len(e)-1) if e[i]==0 and e[i+1]!=0])
        ptrs=[]
        for i in range(0,ps,4):
            v=struct.unpack_from('<I',e,i)[0]
            if v in starts: ptrs.append((i,v))
        tg=sorted(set(v for i,v in ptrs))
        for v in tg:
            end=e.index(b'\0',v); res.append((k,v,e[v:end],[i for i,x in ptrs if x==v]))
    return res
if __name__=='__main__':
    b=open('dec/SYS/GRXSYS.PAC','rb').read()
    r=strings(b); seen={};order=[]
    for k,v,s,p in r:
        t=tok(s)
        if t not in seen: seen[t]=len(order); order.append(t)
    with open('translation/sys_jp.tsv','w',encoding='utf8') as o:
        for i,t in enumerate(order): o.write('%d\t%s\n'%(i,t))
    print(len(r),len(order),sum(len(t) for t in order))
