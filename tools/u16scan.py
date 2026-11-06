import sys,os,struct
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from gxtext import MAP
from lm import score
def scan(b,align=2):
    out=[];i=0;n=len(b)-1
    while i<n:
        st=i;g=[]
        while i<n:
            v=b[i]|b[i+1]<<8
            if v==0 or v>=2112: break
            g.append(v); i+=2
        if len(g)>=2 and i<n and (b[i]|b[i+1]<<8)==0:
            t=''.join(MAP[x] for x in g)
            if score(t)>-7 or len(g)>=3 and all(x>=52 for x in g) and score(t)>-8: out.append((st,t))
        i=st+2 if i==st else i+2
    return out
if __name__=='__main__':
    for f in sys.argv[1:]:
        b=open(f,'rb').read(); r=scan(b)
        print(f,len(r))
        for o,t in r: print(' %x %s'%(o,t))
