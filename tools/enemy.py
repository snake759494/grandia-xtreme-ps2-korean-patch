# enemy name / enemy move strings inside field MDT battle data.
# Each block starts with the normal-attack string; every string is referenced by its own relative pointer,
# so strings are replaced in place (Korean bytes <= Japanese bytes, rest zero-filled).
import os,sys,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from gxtext import decode
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
PAT=re.compile(bytes([92,48,40,91,92,120,50,48,45,92,120,102,102,93,123,56,44,50,52,125,41,40,63,61,92,48,41]))
KEY=bytes.fromhex('def278f136f037f000')  # normal attack string + NUL
def load():
    if not os.path.exists(os.path.join(ROOT,'translation/src/enemy.tsv')): return {}
    S={l.split('\t')[0]:l.rstrip('\r\n').split('\t')[1] for l in open(os.path.join(ROOT,'translation/src/enemy.tsv'),encoding='utf8')}
    K={}
    p=os.path.join(ROOT,'translation/ko/enemy.tsv')
    if os.path.exists(p):
        for l in open(p,encoding='utf8'):
            l=l.rstrip('\r\n')
            if '\t' in l:
                i,k=l.split('\t',1)
                if k and i in S: K[S[i]]=k
    return K
TR=load()
def texts(): return [x for v in TR.values() for x in v.split('/')]
def strings(d):
    i=d.find(KEY)
    while i>=0:
        j=i
        for _ in range(12):
            e=d.index(b'\0',j)
            if e==j: break
            t=decode(d[j:e])[0]
            if '{' in t: break
            yield j,e,t
            j=e+1
        i=d.find(KEY,i+1)
    # loose strings elsewhere (exact null-delimited match of a known long name)
    for m in re.finditer(PAT,d):
        a=m.start(1); e=m.end(1)
        try: t=decode(d[a:e])[0]
        except Exception: continue
        if len(t)>=4 and t in TR: yield a,e,t
def apply(d,enc,over=None):
    d=bytearray(d); n=0
    for a,e,t in list(strings(bytes(d))):
        k=TR.get(t)
        if not k: continue
        C=[]
        for x in k.split('/'): C+=[x,x.replace(' ','')]
        for cand in C:
            b=enc(cand)
            if len(b)<=e-a:
                d[a:e]=b+b'\0'*(e-a-len(b)); n+=1; break
        else:
            if over is not None: over.add((t,k,e-a,min(len(enc(x)) for x in C)))
    return bytes(d),n
