# Korean charset assignment + encoder
import os,re,glob,collections,sys
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,'..')
sys.path.insert(0,HERE)
from gxtext import MAP,glyph_of
def code_of(g):
    if g<0xd0: return g+0x20
    p=(g+0x20)//0xd0-1; lo=g+0x20-(p+1)*0xd0
    if lo<0x20: p-=1; lo+=0xd0
    c=0xf000|p<<8|lo; assert glyph_of(c)==g and 0x20<=lo<0xf0
    return c
TOK=re.compile(r'(\{[0-9A-F]+\}|\|)')
HALF2FULL={' ':'　','!':'！','?':'？','~':'～',':':'：','(':'（',')':'）','-':'－','+':'＋','/':'／'}
for i in range(10): HALF2FULL[str(i)]=chr(0xff10+i)
for i in range(26): HALF2FULL[chr(65+i)]=chr(0xff21+i)
def norm(ch): return HALF2FULL.get(ch,ch)
KEEP_CHARS=set('\u3000\u203c\u2049\uff01\uff1f\uff5e\u2026\u30fc\u30fb\u2665\u00a2\uff1a\uff08\uff09\u300e\u300f\uff10\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19\uff21\uff22\uff23\uff24\uff25\uff26\uff27\uff28\uff29\uff2a\uff2b\uff2c\uff2d\uff2e\uff2f\uff30\uff31\uff32\uff33\uff34\uff35\uff36\uff37\uff38\uff39\uff3a\u25ef\u266a\uff0b\uff0d\u25a1\uff3f\uff0f\uff3b\uff3d\u2192\u203b\uff05\u00d7\uff06\uff03\uff0a\uff1d\uff1c\uff1e\uff20')
def load_tr():
    tr={}
    for f in sorted(glob.glob(os.path.join(ROOT,'translation','ko','*.tsv'))):
        kind=os.path.basename(f)[:3]
        src=os.path.join(ROOT,'translation','src',os.path.basename(f))
        sm={}
        for l in open(src,encoding='utf8'):
            l=l.rstrip('\n')
            if l: i,s=l.split('\t',1); sm[int(i)]=s
        for l in open(f,encoding='utf8'):
            l=l.rstrip('\n')
            if not l: continue
            i,s=l.split('\t',1); i=int(i)
            if i in sm: tr[(kind,sm[i])]=s
    return tr
BLANK=2107
def build_map(texts):
    cnt=collections.Counter()
    for t in texts:
        for part in TOK.split(t):
            if part and not part.startswith('{') and part!='|':
                for ch in part:
                    ch=norm(ch)
                    if '가'<=ch<='힣': cnt[ch]+=1
    keep={}
    for g,ch in enumerate(MAP):
        if g<52 or (ch in KEEP_CHARS and ch not in keep.values()): keep[g]=ch
    free=[g for g in range(52,BLANK) if g not in keep]
    hang=[c for c,_ in cnt.most_common()]
    if len(hang)>len(free): raise SystemExit('too many syllables %d>%d'%(len(hang),len(free)))
    gmap=dict(keep)
    for ch,g in zip(hang,free): gmap[g]=ch
    return gmap
def encoder(gmap):
    rev={}
    for g,ch in sorted(gmap.items()): rev.setdefault(ch,g)
    def enc(t):
        out=bytearray()
        for part in TOK.split(t):
            if not part: continue
            if part=='|': out.append(0x1f)
            elif part.startswith('{'): out+=bytes.fromhex(part[1:-1])
            else:
                for ch in part:
                    g=rev[norm(ch)]; c=code_of(g)
                    out+= bytes([c]) if c<0x100 else bytes([c&0xff,c>>8])
        return bytes(out)
    return enc
