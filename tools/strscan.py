import sys,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from gxtext import MAP,glyph_of,decode
HIRA=set(range(52,131))
pat=re.compile(rb'(?:[\x20-\xef][\xf0-\xf9]|[\x20-\xef]|[\x1f\x0b\x1c\x1d\x18\x05\x04])+\x00')
def scan(b,minlen=2):
    out=[]
    for m in pat.finditer(b):
        s=m.group()[:-1]
        if m.start()>0 and b[m.start()-1]>=0xf0: continue
        t,_=decode(s)
        gl=[];i=0
        while i<len(s):
            if i+1<len(s) and s[i+1]>=0xf0: gl.append(glyph_of(s[i]|s[i+1]<<8)); i+=2
            else: gl.append(s[i]-0x20 if s[i]>=0x20 else -1); i+=1
        jp=sum(1 for g in gl if g>=52)
        if jp<minlen: continue
        if any(g>=len(MAP) for g in gl): continue
        hira=sum(1 for g in gl if g in HIRA); kanji=sum(1 for g in gl if g>=230)
        sym=sum(1 for g in gl if 0<g<16)
        if sym*2>len(gl): continue
        out.append((m.start(),len(s),t,hira,kanji))
    return out
if __name__=='__main__':
    for f in sys.argv[1:]:
        r=scan(open(f,'rb').read())
        print(f,len(r))
        for x in r[:int(os.environ.get('N','30'))]: print(' %x %d %s'%(x[0],x[1],x[2]))
