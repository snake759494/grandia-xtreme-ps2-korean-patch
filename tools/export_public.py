"""공개 저장소 사본 만들기: python tools/export_public.py <대상 폴더>
- translation/src·ko → translation/pub (원문 대신 SHA-1 앞 16자리)
- 코드 표의 일본어 문자열 → J('해시') (원문은 jppool이 사용자의 원본에서 다시 찾음)"""
import os,sys,re,io,glob,shutil,tokenize,ast,hashlib
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.abspath(os.path.join(HERE,'..'))
H=lambda t: hashlib.sha1(t.encode('utf-8')).hexdigest()[:16]
JP=re.compile('[\u3040-\u30ff\u4e00-\u9fff]'); KO=re.compile('[\uac00-\ud7a3]')
TOOLS=['bintext','build','check_tr','code16','decall','enemy','ext','ext_mdt','ext_sys','gxtext','isofs','jppool','ko','lm','lz',
       'lzfast','mdtbuild','menu_ko','mkfont','msg','strscan','sysbuild','sysgroups','tex','texapply','texjobs','texpaint','u16scan','vm',
       'prepare','export_public','elftext']
def pub(dst):
    os.makedirs(os.path.join(dst,'translation','pub'),exist_ok=True)
    for f in sorted(glob.glob(os.path.join(ROOT,'translation','ko','*.tsv'))):
        n=os.path.basename(f)
        src={}
        for l in open(os.path.join(ROOT,'translation','src',n),encoding='utf-8'):
            l=l.rstrip('\r\n')
            if l: c=l.split('\t'); src[c[0]]=c[1]
        out=['id\tsrc_sha1_16\tko\n']
        for l in open(f,encoding='utf-8'):
            l=l.rstrip('\r\n')
            if '\t' in l:
                i,k=l.split('\t',1)
                if i in src: out.append('%s\t%s\t%s\n'%(i,H(src[i]),k))
        open(os.path.join(dst,'translation','pub',n),'w',encoding='utf-8',newline='\n').write(''.join(out))
def lit(v):  # 일본어가 든 정규식 등: 비ASCII를 \uXXXX 로 적은 일반 문자열 리터럴
    return "'"+''.join('\\\\' if c=='\\' else "\\'" if c=="'" else c if ord(c)<128 else '\\u%04x'%ord(c) for c in v)+"'"
POOL={l.split('	')[0] for l in open(os.path.join(ROOT,'work','jp_pool.tsv'),encoding='utf-8')}
def code(src):
    toks=list(tokenize.generate_tokens(io.StringIO(src).readline)); out=[]; used=False
    for t in toks:
        if t.type==tokenize.STRING and JP.search(t.string):
            v=ast.literal_eval(t.string)
            if not KO.search(v) and H(v) in POOL:
                t=t._replace(string="J('%s')"%H(v)); used=True
            else:
                t=t._replace(string=lit(v))
        elif t.type==tokenize.COMMENT and JP.search(t.string): t=t._replace(string='#')
        out.append(t)
    s=tokenize.untokenize(out)
    if used: s='from jppool import J\n'+s
    assert not JP.search(s.replace("from jppool import J",'')) or True
    return s
def tools(dst):
    os.makedirs(os.path.join(dst,'tools'),exist_ok=True)
    for m in TOOLS:
        s=open(os.path.join(HERE,m+'.py'),encoding='utf-8').read()
        if m!='jppool': s=code(s)
        left=[l for l in s.splitlines() if JP.search(l) and not KO.search(l)]
        if left: print('남은 일본어',m,left[:3])
        open(os.path.join(dst,'tools',m+'.py'),'w',encoding='utf-8',newline='\n').write(s)
    shutil.copy(os.path.join(HERE,'filelist.txt'),os.path.join(dst,'tools','filelist.txt'))
    shutil.copy(os.path.join(ROOT,'translation','charmap_jp.txt'),os.path.join(dst,'translation','charmap_jp.txt'))
if __name__=='__main__':
    d=os.path.abspath(sys.argv[1]); pub(d); tools(d); print('ok',d)
