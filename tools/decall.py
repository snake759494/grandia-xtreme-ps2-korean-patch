import os,sys
sys.path.insert(0,os.path.dirname(__file__)); import lz
from concurrent.futures import ProcessPoolExecutor
def job(p):
    src='extract/'+p; dst='dec/'+p
    if os.path.exists(dst): return p,'skip'
    b=open(src,'rb').read()
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    try: ok=lz.info(b)[0]
    except Exception: ok=False
    if not ok: return p,'raw'
    open(dst,'wb').write(lz.decompress(b)); return p,'lz'
if __name__=='__main__':
    L=[l.strip().lstrip('/') for l in open('work/all.txt')]
    from collections import Counter
    with ProcessPoolExecutor(6) as ex: r=list(ex.map(job,L))
    print(Counter(x[1] for x in r)); print([x[0] for x in r if x[1]=='raw'][:20])
