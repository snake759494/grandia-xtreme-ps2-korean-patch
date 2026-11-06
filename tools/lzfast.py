import numpy as np, struct
from numba import njit
MAGIC=0x15246468
@njit(cache=True)
def _comp(d):
    n=d.shape[0]
    out=np.zeros(n+n//8+16,np.uint8); o=0
    HS=1<<15
    head=np.full(HS,-1,np.int64); prev=np.full(n,-1,np.int64)
    i=0
    def h3(i): return 0
    while i<n:
        fpos=o; o+=1; fl=0
        for bit in range(8):
            if i>=n: break
            bl=0; bj=0
            if i+3<=n:
                hv=((d[i]<<10)^(d[i+1]<<5)^d[i+2])&(HS-1)
                j=head[hv]; cnt=0
                mx=min(34,n-i)
                while j>=0 and cnt<128:
                    if i-j>0x7ff-0x12: break
                    l=0
                    while l<mx and d[j+l]==d[i+l]: l+=1
                    if l>bl:
                        bl=l; bj=j
                        if l==mx: break
                    j=prev[j]; cnt+=1
            if bl>=3:
                off=(0x7de+bj)&0x7ff
                out[o]=off&0xff; out[o+1]=((off>>3)&0xe0)|(bl-3); o+=2
                for k in range(bl):
                    p=i+k
                    if p+3<=n:
                        hv=((d[p]<<10)^(d[p+1]<<5)^d[p+2])&(HS-1)
                        prev[p]=head[hv]; head[hv]=p
                i+=bl
            else:
                fl|=1<<bit; out[o]=d[i]; o+=1
                if i+3<=n:
                    hv=((d[i]<<10)^(d[i+1]<<5)^d[i+2])&(HS-1)
                    prev[i]=head[hv]; head[hv]=i
                i+=1
        out[fpos]=fl
    return out[:o]
def compress(data,key=0x178c3615):
    c=_comp(np.frombuffer(data,np.uint8)).tobytes()
    return struct.pack('<4I',key,MAGIC^key,len(data)^key,len(c)^key)+c
