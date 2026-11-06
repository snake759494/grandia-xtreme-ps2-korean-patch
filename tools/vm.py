# outer event VM instruction lengths for MDT script sections
import struct
MSGOPS=set([0x16,0x19,0x1a,0x1b,0x1c])
def ilen(s,i):
    """returns (length, kind, extra). kind: 'op','msg','jmp','end'"""
    c=s[i]
    if c<=2: return 1,'end',None
    if c>=0x1e or c in MSGOPS:
        e=s.find(b'\x17\x00',i); return e+2-i,'msg',i
    a=s[i+1] if i+1<len(s) else 0
    if c==3:
        h=a>>4
        if h==0: return 2,'ret',None
        if h in(1,2,3): return 4,'jmp',((a&15)<<16)|struct.unpack_from('<H',s,i+2)[0]
        if h in(4,5): return 4,'op',None
        raise ValueError('03 hi %x'%h)
    if c==4: return 2,'op',None
    if c==5: return 3,'op',None
    if c==6: return 4,'op',None
    if c==7: return (8 if a==11 else 6),'op',None
    if c in(8,9,0xa):
        if a: return 6,'op',None
        return 4+{8:1,9:2,0xa:4}[c],'op',None
    if c==0xb: return 3,'op',None
    if c==0xc: return 2,'op',None
    if c==0xd: return (10 if a==0 else 3 if a in(2,3) else 2),'op',None
    if c==0xe: return (4 if a<=5 else 5 if a==6 else 2),'op',None
    if c==0xf: return 4,'op',None
    if c==0x10: return 8,'op',None
    if c==0x11: return 4,'op',None
    if c==0x12: return 2,'op',None
    if c==0x13: return 6,'op',None
    if c==0x14: return 6,'op',None
    if c==0x15: return 5,'op',None
    if c==0x17:
        if a==0: return 2,'op',None
        e=s.find(b'\x17\x00',i+2); return e+2-i,'msg',i
    if c==0x18: return 3,'op',None
    if c==0x1d: return (3 if a==0xff else 4),'op',None
    raise ValueError('op %x'%c)
def events(s):
    hs=struct.unpack_from('<I',s,0)[0]
    ev=[];i=4
    while i<hs:
        v=struct.unpack_from('<I',s,i)[0]
        if v==0xffffffff: break
        ev.append((v&0xffff,(v>>16)*8+hs,i)); i+=4
    return hs,ev
