import struct
MAGIC=0x15246468
def info(b):
    k,a,u,c=struct.unpack_from('<4I',b,0)
    return (a^k)==MAGIC, u^k, c^k
def decompress(b):
    ok,usize,csize=info(b)
    if not ok: raise ValueError('not lz')
    src=b[16:16+csize]; out=bytearray(); win=bytearray(0x800); wp=0x7de
    i=0; flags=0; n=len(src)
    while i<n:
        flags>>=1
        if not flags&0x100:
            flags=src[i]|0xff00; i+=1
            if i>=n: break
        if flags&1:
            c=src[i]; i+=1; out.append(c); win[wp]=c; wp=(wp+1)&0x7ff
        else:
            if i+1>=n: break
            lo=src[i]; hi=src[i+1]; i+=2
            off=lo|(hi&0xe0)<<3; ln=(hi&0x1f)+3
            for k in range(ln):
                c=win[(off+k)&0x7ff]; out.append(c); win[wp]=c; wp=(wp+1)&0x7ff
    return bytes(out[:usize])
def compress(data,key=0x178c3615):
    # greedy LZSS matching the game's window semantics (pos starts at 0x7de, zero-filled)
    n=len(data); out=bytearray(); i=0
    win_pos=lambda p:(0x7de+p)&0x7ff
    heads={}
    def find(i):
        best_l=0;best_o=0
        if i+3>n: return 0,0
        key3=data[i:i+3]
        for j in reversed(heads.get(key3,[])[-64:]):
            if i-j>0x7ff-0x12: break
            l=0; mx=min(34,n-i)
            while l<mx and data[j+l]==data[i+l]: l+=1
            if l>best_l: best_l=l;best_o=j
            if l==34: break
        # zero run from pre-filled window (only at start)
        if best_l<3: return 0,0
        return best_l,best_o
    while i<n:
        fpos=len(out); out.append(0); fl=0
        for bit in range(8):
            if i>=n: break
            l,j=find(i)
            if l>=3:
                off=win_pos(j); ln=l-3
                out.append(off&0xff); out.append(((off>>3)&0xe0)|ln)
                for k in range(l):
                    if i+k+3<=n: heads.setdefault(data[i+k:i+k+3],[]).append(i+k)
                i+=l
            else:
                fl|=1<<bit; out.append(data[i])
                if i+3<=n: heads.setdefault(data[i:i+3],[]).append(i)
                i+=1
        out[fpos]=fl
    hdr=struct.pack('<4I',key,MAGIC^key,n^key,len(out)^key)
    return hdr+bytes(out)
if __name__=='__main__':
    import sys
    b=open(sys.argv[1],'rb').read(); print(info(b))
    d=decompress(b); open(sys.argv[2],'wb').write(d); print(len(d))
