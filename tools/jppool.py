# 코드 표(menu_ko·bintext·code16)의 일본어 원문은 저장소에 넣지 않고 SHA-1 앞 16자리로만 적는다.
# J('해시')는 사용자의 원본에서 뽑은 문자열 풀(work/jp_pool.tsv)에서 원문을 찾아 돌려준다.
import os,sys,re,glob,hashlib,struct
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..')
sys.path.insert(0,HERE)
POOL=os.path.join(ROOT,'work','jp_pool.tsv')
H=lambda t: hashlib.sha1(t.encode('utf-8')).hexdigest()[:16]
SPLIT=re.compile(r'\{[0-9A-F]+\}|\|')
def build():
    from gxtext import MAP,decode
    S=set()
    def add(t):
        if not t: return
        S.add(t)
        for p in SPLIT.split(t): S.add(p)
    byte_files=[os.path.join(ROOT,'dec','SYS','GRXSYS.PAC'),os.path.join(ROOT,'extract','BATTLE.BIN')]
    for f in byte_files:
        b=open(f,'rb').read(); i=0
        for chunk in b.split(b'\0'):
            if chunk:
                try: add(decode(chunk)[0])
                except Exception: pass
    u16=[os.path.join(ROOT,'dec','FIELD',n+'.MDT') for n in ('2008','3034','2090','E490')]+byte_files[:1]
    for f in u16:
        b=open(f,'rb').read()
        for par in (0,):
            cur=[]
            for i in range(par,len(b)-1,2):
                v=struct.unpack_from('<H',b,i)[0]
                if 0<v<len(MAP): cur.append(MAP[v])
                else:
                    if v==0 and cur: S.add(''.join(cur))
                    cur=[]
    os.makedirs(os.path.dirname(POOL),exist_ok=True)
    with open(POOL,'w',encoding='utf-8',newline='\n') as o:
        for t in sorted(S):
            if '\t' not in t and '\n' not in t: o.write(H(t)+'\t'+t+'\n')
    return len(S)
_P=None
def J(h):
    global _P
    if _P is None:
        if not os.path.exists(POOL): build()
        _P={}
        for l in open(POOL,encoding='utf-8'):
            a,b=l.rstrip('\n').split('\t',1); _P[a]=b
    if h not in _P: raise KeyError('원문 풀에 없는 해시 '+h+' (원본 ISO·추출 확인)')
    return _P[h]
if __name__=='__main__': print('pool',build())
