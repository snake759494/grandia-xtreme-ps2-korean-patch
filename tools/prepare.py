"""재빌드 준비: 원본 ISO → extract/·dec/ 추출, 글꼴·텍스처 목록·원문 목록 생성,
공개 번역(translation/pub, 원문 SHA-1 앞 16자리)을 빌드용 번역(translation/src, translation/ko)으로 복원.
사용: python tools/prepare.py   (저장소 최상위에 원본 ISO가 있어야 함)"""
import os,sys,re,glob,struct,hashlib,subprocess,collections
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..'))
sys.path.insert(0,HERE)
H=lambda t: hashlib.sha1(t.encode('utf-8')).hexdigest()[:16]
TR=os.path.join(ROOT,'translation')
def run(m): subprocess.run([sys.executable,os.path.join(HERE,m+'.py')],cwd=ROOT,check=True)
def extract():
    import ext
    F=ext.files()
    want=[p for p in F if p.split('/')[1] in ('FIELD','BTL_DATA','SYS') or p.count('/')==1]
    os.makedirs(os.path.join(ROOT,'work'),exist_ok=True)
    with open(os.path.join(ROOT,'work','all.txt'),'w') as o:
        for p in want:
            if p.split('/')[1] in ('FIELD','BTL_DATA','SYS'): o.write(p+'\n')
    for p in want:
        out=os.path.join(ROOT,'extract',p.lstrip('/'))
        if os.path.exists(out): continue
        os.makedirs(os.path.dirname(out),exist_ok=True); open(out,'wb').write(ext.read(p,F))
    run('decall')
def font():
    b=open(os.path.join(ROOT,'dec','SYS','GRXSYS.PAC'),'rb').read()
    open(os.path.join(ROOT,'work','font_orig.bin'),'wb').write(b[0x180:0x180+2112*128])
    open(os.path.join(ROOT,'work','width_orig.bin'),'wb').write(b[0xfda00:0xfda00+2112*2])
def texlist():
    import numpy as np
    from tex import is_tex
    os.chdir(ROOT)
    fs=[f for f in glob.glob('dec/**/*',recursive=True)+glob.glob('extract/*')+glob.glob('extract/BTL_DATA/*') if os.path.isfile(f) and 'GRXSYS' not in f]
    with open('work/texlist.txt','w') as out:
        for f in fs:
            b=open(f,'rb').read()
            a=np.frombuffer(b[:len(b)//16*16],np.uint32).reshape(-1,4)
            cand=np.nonzero(((a[:,0]&(a[:,0]-1))==0)&(a[:,0]>0)&(a[:,0]<=1024))[0]
            for k in cand:
                o=int(k)*16
                if is_tex(b,o): out.write('%s\t%x\n'%(f.replace('/',chr(92)),o))
def candidates():
    """원본에서 뽑을 수 있는 모든 번역 대상 원문"""
    from gxtext import decode
    from ext_sys import ENT
    from sysgroups import groups,GE
    S=set()
    for n in ('mdt_jp','sys_jp'):
        for l in open(os.path.join(TR,n+'.tsv'),encoding='utf-8'):
            S.add(l.rstrip('\n').split('\t',1)[1])
    b=open(os.path.join(ROOT,'dec','SYS','GRXSYS.PAC'),'rb').read()
    offs=[struct.unpack_from('<I',b,4*i)[0] for i in range(96)]
    for k in GE:
        for v,(L,end,emp) in groups(b[offs[k]:offs[k+1]],ENT[k]).items(): S.add('|'.join(L))
    pat=re.compile(rb'\0([\x20-\xff]{2,40})(?=\0)')
    for f in glob.glob(os.path.join(ROOT,'dec','FIELD','*.MDT')):
        d=open(f,'rb').read()
        for m in pat.finditer(d):
            try: S.add(decode(m.group(1))[0])
            except Exception: pass
    return {H(t):t for t in S}
def restore():
    C=candidates(); miss=collections.Counter()
    os.makedirs(os.path.join(TR,'src'),exist_ok=True); os.makedirs(os.path.join(TR,'ko'),exist_ok=True)
    for fn in sorted(glob.glob(os.path.join(TR,'pub','*.tsv'))):
        name=os.path.basename(fn); src=[]; ko=[]
        for l in open(fn,encoding='utf-8').read().splitlines()[1:]:
            i,h,k=l.split('\t')
            if h not in C: miss[name]+=1; continue
            src.append(i+'\t'+C[h]+'\n'); ko.append(i+'\t'+k+'\n')
        open(os.path.join(TR,'src',name),'w',encoding='utf-8',newline='\n').write(''.join(src))
        open(os.path.join(TR,'ko',name),'w',encoding='utf-8',newline='\n').write(''.join(ko))
    print('missing =',sum(miss.values()),dict(miss))
if __name__=='__main__':
    os.chdir(ROOT)
    extract(); font(); texlist()
    run('ext_mdt'); run('ext_sys')
    import jppool; print('pool',jppool.build())
    restore()
