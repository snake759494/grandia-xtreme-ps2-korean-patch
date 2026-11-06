import sys, os
HERE=os.path.dirname(os.path.abspath(__file__))
ISO=os.path.join(HERE,'..','Grandia Xtreme (Japan, Asia).iso')
def files():
    d={}
    for ln in open(os.path.join(HERE,'filelist.txt'),encoding='utf-8'):
        l,s,p=ln.split(None,2); d[p.strip().rstrip(';1').rstrip(';')]= (int(l),int(s))
    return d
def read(path, F=None):
    F=F or files(); l,s=F[path]
    with open(ISO,'rb') as f: f.seek(l*2048); return f.read(s)
if __name__=='__main__':
    F=files()
    args=sys.argv[1:]
    if args and args[0].startswith('@'): args=[x.strip() for x in open(args[0][1:],encoding='utf-8') if x.strip()]
    for p in ['/'+a.lstrip('/') for a in args]:
        out=os.path.join(HERE,'..','extract',p.lstrip('/'))
        os.makedirs(os.path.dirname(out),exist_ok=True)
        open(out,'wb').write(read(p,F))
