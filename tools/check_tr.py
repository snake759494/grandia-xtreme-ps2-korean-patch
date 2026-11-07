# usage: python tools/check_tr.py translation/src/mdt_00.tsv translation/ko/mdt_00.tsv
import sys,re
TOK=re.compile(r'\{[0-9A-F]+\}')
BRK=re.compile(r'\||\{1A\}|\{1B\}|\{1701\}|\{1702\}|\{17[248]0[0-9A-F]{4}\}')
ALLOWED=set(' \u3000\u203c\u2049\uff01\uff1f\uff5e\u2026\u30fc\u30fb\u2665\uff1a\uff08\uff09\u300e\u300f0123456789\uff10\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19ABCDEFGHIJKLMNOPQRSTUVWXYZ\uff21\uff22\uff23\uff24\uff25\uff26\uff27\uff28\uff29\uff2a\uff2b\uff2c\uff2d\uff2e\uff2f\uff30\uff31\uff32\uff33\uff34\uff35\uff36\uff37\uff38\uff39\uff3a\u25ef\u266a\uff0b\uff0d\u25a1\uff3f\uff0f\uff3b\uff3d\u2192\u203b!?~:()-+/')
def width(s):
    w=0
    for ch in s:
        w+=1  # dialogue window is fixed-pitch: a space takes a full cell
    return w
def load(p):
    d={}
    for l in open(p,encoding='utf8'):
        l=l.rstrip('\n')
        if not l: continue
        i,s=l.split('\t',1); d[int(i)]=s
    return d
SYS='--sys' in sys.argv
src=load(sys.argv[1]); ko=load(sys.argv[2]); err=0
for i,s in src.items():
    if i not in ko: print(i,'누락'); err+=1; continue
    k=ko[i]
    if TOK.findall(s)!=TOK.findall(k) or s.count('|')!=k.count('|') and False:
        print(i,'토큰 불일치',TOK.findall(s),TOK.findall(k)); err+=1
    if SYS:
        lim=max(width(TOK.sub('',l)) for l in BRK.split(s))
        lim=max(lim,len(TOK.sub('',s).split('|')[0])) if False else lim
    else: lim=22
    for line in BRK.split(k):
        p=TOK.sub('',line)
        if width(p)>lim and (not SYS or width(p)>max(lim,2)): print(i,'줄 너무 김(%.1f>%.1f)'%(width(p),lim),p); err+=1
    bad=[ch for ch in TOK.sub('',k).replace('|','') if not ('가'<=ch<='힣' or ch in ALLOWED)]
    if bad: print(i,'허용되지 않은 문자',''.join(sorted(set(bad)))); err+=1
for i in ko:
    if i not in src: print(i,'원문에 없는 id'); err+=1
print('오류',err,'/',len(src))
