# apply Korean texture repaints to every identical texture copy
import os,sys,struct,hashlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from tex import info
from texpaint import load,encode
from texjobs import JOBS
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
def block(b,o):
    w,h,psm,po,pal,n=info(b,o); return po,pal+n*4
def prepare():
    new={}; sysj={}
    for (f,k),fn in JOBS.items():
        b=bytearray(open(os.path.join(ROOT,f),'rb').read())
        if f.endswith('GRXSYS.PAC'): sysj[k]=fn; continue
        s,e=block(b,k); h=hashlib.md5(b[s:e]).hexdigest()
        a=load(b,k); fn(a); encode(b,k,a); new[h]=bytes(b[s:e])
    per={}
    for l in open(os.path.join(ROOT,'work/texlist.txt')):
        f,o=l.split(); o=int(o,16)
        per.setdefault(os.path.basename(f.replace(chr(92),'/')),[]).append(o)
    return new,per,sysj
def apply(name,b,new,per):
    b=bytearray(b); n=0
    for o in per.get(name,[]):
        s,e=block(b,o); h=hashlib.md5(b[s:e]).hexdigest()
        if h in new: b[s:e]=new[h]; n+=1
    return bytes(b),n
def apply_sys(pac,sysj):
    b=bytearray(pac)
    for k,fn in sysj.items():
        o=struct.unpack_from('<I',b,4*k)[0]; a=load(b,o); fn(a); encode(b,o,a)
    return bytes(b)
