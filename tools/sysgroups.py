# multi-line descriptions in GRXSYS entries 33/35/41: only line 1 is pointed to; the game reads
# following null-terminated lines until an empty line (max 4).  group = (start, [lines], end, trailing_empty)
import struct,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ext_sys import ENT,tok
GE=(33,35,41)
def groups(e,ps):
    P=set(); 
    for i in range(0,ps,4):
        v=struct.unpack_from('<I',e,i)[0]
        if ps<=v<len(e): P.add(v)
    out={}
    for v in sorted(P):
        if v and e[v-1]!=0: continue
        lines=[];i=v
        ok=True
        for n in range(4):
            if n and i in P: ok=False; break
            j=e.index(b'\0',i); lines.append(tok(e[i:j])); i=j+1
        if ok: out[v]=(lines,i,False)
    return out
def load(p=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','translation','ko','desc_groups.tsv')):
    d={}
    if os.path.exists(p):
        for l in open(p,encoding='utf8'):
            l=l.rstrip('\n')
            if '\t' in l: a,b=l.split('\t',1); d[a]=b
    return d
if __name__=='__main__':
    b=open('dec/SYS/GRXSYS.PAC','rb').read()
    offs=[struct.unpack_from('<I',b,4*i)[0] for i in range(96)]
    seen={}; 
    for k in GE:
        e=b[offs[k]:offs[k+1]]
        for v,(L,end,emp) in groups(e,ENT[k]).items():
            if any(L[1:]): seen.setdefault('|'.join(L),k)
    with open('translation/src/desc_groups.tsv','w',encoding='utf8') as o:
        for t in seen: o.write(t+'\n')
    print(len(seen))
