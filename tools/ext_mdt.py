# extract all messages in FIELD/*.MDT script sections -> translation/mdt_jp.tsv (unique), work/mdt_index.tsv
import sys,glob,re,struct,os,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from msg import parse
def tok2s(t):
    if t[0]=='c': return t[1]
    b=t[2]
    if b==b'\x1f': return '|'
    return '{'+b.hex().upper()+'}'
def messages(s):
    got={}
    for m in re.finditer(b'(?=\x17[\x01\x02\x20\x40\x80])',s):
        k=s[m.start()+1]; st=m.start()+(4 if k&0xe0 else 2)
        r=parse(s,st)
        if not r: continue
        t,e=r; fe=s.find(b'\x17\x00',m.start()+2)+2
        if fe==e and any(x[0]=='c' for x in t) and e not in got:
            got[e]=(st,e-2,''.join(tok2s(x) for x in t))
    return sorted(got.values())
def script(b):
    sz,off=struct.unpack_from('<II',b,0x78)
    if off+sz>len(b) or sz==0: return None,None
    return off,b[off:off+sz]
if __name__=='__main__':
    order=[];seen={};idx=[]
    for f in sorted(glob.glob('dec/FIELD/*.MDT')):
        b=open(f,'rb').read(); off,s=script(b)
        if s is None: continue
        for st,en,txt in messages(s):
            if txt not in seen: seen[txt]=len(order); order.append(txt)
            idx.append((os.path.basename(f),off+st,en-st,seen[txt]))
    os.makedirs('translation',exist_ok=True)
    with open('translation/mdt_jp.tsv','w',encoding='utf8') as o:
        for i,t in enumerate(order): o.write('%d\t%s\n'%(i,t))
    with open('work/mdt_index.tsv','w') as o:
        for r in idx: o.write('%s\t%d\t%d\t%d\n'%r)
    print(len(idx),len(order),sum(len(t) for t in order))
