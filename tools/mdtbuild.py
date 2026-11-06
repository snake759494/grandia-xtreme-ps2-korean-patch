import struct,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from vm import ilen,events
from msg import parse
from ext_mdt import tok2s
def sweep(s):
    hs,ev=events(s)
    starts=sorted(set(e[1] for e in ev))
    ins=[]
    for k,st in enumerate(starts):
        i=st; lim=starts[k+1] if k+1<len(starts) else len(s)
        while i<lim:
            L,kind,x=ilen(s,i); ins.append((i,L,kind,x,i==st)); i+=L
        assert i==lim,(hex(i),hex(lim))
    return hs,ev,starts,ins
def msg_body(s,i):
    """for msg instruction at i: returns (prefix_end, body_end) body = s[prefix_end:body_end] (without 17 00)"""
    c=s[i]
    if c==0x17:
        k=s[i+1]; st=i+(4 if k in(0x40,0x80) else 2)
    else: st=i
    return st
def rebuild_script(s,repl):
    """repl(text_str, body_bytes)-> new body bytes or None"""
    hs,ev,starts,ins=sweep(s)
    out=bytearray(s[:hs]); newpos={}
    for (i,L,kind,x,isstart) in ins:
        if isstart:
            while (len(out)-hs)%8: out.append(0)
        newpos[i]=len(out)
        if kind=='msg':
            st=msg_body(s,i); en=i+L-2
            body=s[st:en]
            r=parse(s,st)
            nb=None
            if r and r[1]==i+L and any(t[0]=='c' for t in r[0]):
                txt=''.join(tok2s(t) for t in r[0])
                nb=repl(txt,body)
            if nb is None: nb=body
            assert nb.find(b'\x17\x00')<0
            out+=s[i:st]+nb+b'\x17\x00'
        else:
            out+=s[i:i+L]
    newpos[len(s)]=len(out)
    # fix jumps
    for (i,L,kind,x,isstart) in ins:
        if kind=='jmp':
            t=newpos[x+hs]-hs; p=newpos[i]
            assert t<(1<<20)
            out[p+1]=(out[p+1]&0xf0)|(t>>16); struct.pack_into('<H',out,p+2,t&0xffff)
    # fix event table
    for (eid,st,pos) in ev:
        no=newpos[st]-hs; assert no%8==0 and no//8<0x10000
        struct.pack_into('<I',out,pos,eid|(no//8)<<16)
    return bytes(out)
def rebuild_mdt(b,repl):
    sz,off=struct.unpack_from('<II',b,0x78)
    s=b[off:off+sz]
    ns=rebuild_script(s,repl)
    if ns==s: return b
    pad=(-(len(ns)-sz))%0x100
    ns2=ns+b'\0'*pad
    delta=len(ns2)-sz
    end=off+sz
    out=bytearray(b[:off]+ns2+b[end:])
    struct.pack_into('<I',out,0x78,len(ns))
    for i in range(0,0x200,4):
        if i==0x78: continue
        v=struct.unpack_from('<I',out,i)[0]
        if v!=0xffffffff and end<=v<=len(b)+0x100: struct.pack_into('<I',out,i,v+delta)
    return bytes(out)
