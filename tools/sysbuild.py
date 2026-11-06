from jppool import J
import struct,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from ext_sys import ENT,tok
from sysgroups import groups,GE
import sysgroups
def _gtr():
    root=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','translation')
    S=[l.rstrip('\r\n').split('\t') for l in open(os.path.join(root,'src','desc_groups.tsv'),encoding='utf8')]
    K=sysgroups.load(os.path.join(root,'ko','desc_groups.tsv'))
    return {s[1]:K[s[0]] for s in S if s[0] in K}
GTR=_gtr()
NAMES={J('354cf9b7642622e9'):'에반',J('bb42a0654b9562b0'):'브랜돌',J('216f770dfa69e07f'):'카마인',J('61caaa4e8806c517'):'제이드',J('28196171da4a9997'):'티토',J('58a3f58f9d5b2f02'):'울크',J('0b7faa6a5935cf30'):'미얌',J('84f7b1e0536da0cc'):'루티나'}
def rebuild(b,trans,enc,font=None,width=None):
    offs=[struct.unpack_from('<I',b,4*i)[0] for i in range(96)]
    ents=[b[offs[i]:offs[i+1]] for i in range(95)]+[b[offs[95]:]]
    for k,ps in ENT.items():
        if k==36: continue
        e=bytearray(ents[k])
        starts=set([ps]+[i+1 for i in range(ps,len(e)-1) if e[i]==0 and e[i+1]!=0])
        ptrs={}
        for i in range(0,ps,4):
            v=struct.unpack_from('<I',e,i)[0]
            if v in starts: ptrs.setdefault(v,[]).append(i)
        new={};spans=[]
        G=groups(bytes(e),ps) if k in GE else {}
        for v in sorted(ptrs):
            if v in G:
                # 4-line description: the game reads 4 consecutive strings, keep them together
                L,gend,_=G[v]; key='|'.join(L)
                if any(L[1:]):
                    if key not in GTR: raise SystemExit('missing group translation: '+key)
                    KL=GTR[key].split('|')
                elif L[0] in trans: KL=[trans[L[0]],'','','']
                else: continue
                new[v]=b''.join(enc(x)+b'\0' for x in KL); spans.append([v,gend]); continue
            end=e.index(b'\0',v); t=tok(e[v:end])
            if t in trans:
                new[v]=enc(trans[t])+b'\0'; spans.append([v,end+1])
        # merge spans
        spans.sort(); runs=[]
        for a,c in spans:
            if runs and a<=runs[-1][1]: runs[-1][1]=max(runs[-1][1],c)
            else: runs.append([a,c])
        for a,c in runs: e[a:c]=b'\0'*(c-a)
        tail=bytearray(); base=len(e)
        newpos={}
        for v,nb in sorted(new.items(),key=lambda x:-len(x[1])):
            for r in runs:
                if r[1]-r[0]>=len(nb):
                    newpos[v]=r[0]; e[r[0]:r[0]+len(nb)]=nb; r[0]+=len(nb); break
            else:
                newpos[v]=base+len(tail); tail+=nb
        e+=tail
        while len(e)%0x80: e.append(0)
        for v,p in newpos.items():
            for i in ptrs[v]: struct.pack_into('<I',e,i,p)
        ents[k]=bytes(e)
    # party name list (entry 36): rewrite sequentially, fix any pointers
    e=bytearray(ents[36]); i=0x4e0; old=[]
    while e[i]:
        j=e.index(b'\0',i); old.append((i,tok(e[i:j]))); i=j+1
    endr=i; out=bytearray(); newst={}
    for st,t in old:
        newst[st]=0x4e0+len(out); out+=enc(NAMES.get(t,trans.get(t,t)))+b'\0'
    assert 0x4e0+len(out)<=0x580,len(out)
    e[0x4e0:0x580]=out+bytes(0xa0-len(out))
    for k in range(0,0x4e0,4):
        v=struct.unpack_from('<I',e,k)[0]
        if v in newst and v!=0x4e0: struct.pack_into('<I',e,k,newst[v])
    ents[36]=bytes(e)
    if font is not None:
        e=bytearray(ents[0]); e[:len(font)]=font[:len(e)]; ents[0]=bytes(e)
    if width is not None:
        e=bytearray(ents[43]); e[:len(width)]=width; ents[43]=bytes(e)
    out=bytearray(b[:offs[0]]); newoffs=[]
    for i in range(96):
        while len(out)%0x80: out.append(0)
        newoffs.append(len(out)); out+=ents[i]
    for i,o in enumerate(newoffs): struct.pack_into('<I',out,4*i,o)
    return bytes(out)
SPEAKERS=['얼굴없음','에반','？？？','브랜돌','카마인','제이드','티토','울크','미얌','루티나','크로이츠 중령','스펙트','디네','에볼','콴 리',
'도구점 주인','도구점 아주머니','도구점 아이','웨이트리스','마법점 주인','지도사','지아스테','기술자','관리인','행상인','할란','스코','챕스','튜터',
'짐 관리인','파이크','병사','병사１','병사２','병사３','중사','중사１','중사２','중사３','여관 주인','의뢰인','의뢰인의 딸','이스메네','유리데스','벨다','이주',
'신부의 아내','과학 사관','친위대원','남자아이','아주머니','아저씨','개','\ub9c8\ubc95\uc810\u30fb\uc5b8\ub2c8','\ub9c8\ubc95\uc810\u30fb\ub3d9\uc0dd','？점','스킬점']
def speakers(pac,gidx):
    offs=[struct.unpack_from('<I',pac,4*i)[0] for i in range(96)]
    base=offs[48]; e=bytearray(pac[base:offs[49]])
    assert len(SPEAKERS)==57
    p=0x6ec
    for k,name in enumerate(SPEAKERS):
        struct.pack_into('<I',e,0x608+4*k,p)
        for ch in name:
            struct.pack_into('<H',e,p,gidx[{' ':'　'}.get(ch,ch)]); p+=2
        struct.pack_into('<H',e,p,0); p+=2
    assert p<=len(e),hex(p)
    e[p:len(e)]=bytes(len(e)-p) if p<0x980 else b''
    return pac[:base]+bytes(e)+pac[offs[49]:]

def menu49(pac,gidx,blank=2107):
    from u16scan import scan
    from menu_ko import get
    offs=[struct.unpack_from('<I',pac,4*i)[0] for i in range(96)]
    base=offs[49]; e=bytearray(pac[base:offs[50]]); n=0
    for o,t in scan(bytes(e)):
        k=get(t)
        if not k: continue
        g=[blank if ch in ' 　' else gidx[ch] for ch in k]
        assert len(g)<=len(t),(t,k)
        g+= [blank]*(len(t)-len(g))
        for j,v in enumerate(g): struct.pack_into('<H',e,o+2*j,v)
        n+=1
    from menu_ko import EXTRA
    from gxtext import MAP
    for o,(jp,k) in EXTRA.items():
        cur=''.join(MAP[struct.unpack_from('<H',e,o+2*j)[0]] for j in range(len(jp)))
        assert cur==jp and struct.unpack_from('<H',e,o+2*len(jp))[0]==0,(hex(o),cur,jp)
        g=[blank if ch in ' 　' else gidx[ch] for ch in k]+[blank]*(len(jp)-len(k))
        for j,v in enumerate(g): struct.pack_into('<H',e,o+2*j,v)
        n+=1
    print('menu49',n)
    return pac[:base]+bytes(e)+pac[offs[50]:]
