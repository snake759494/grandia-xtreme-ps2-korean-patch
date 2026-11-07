import sys,os,glob,struct,time
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import ko,mkfont,lz,lzfast,isofs,bintext
from sysbuild import NAMES
from gxtext import encode_jp
from mdtbuild import rebuild_mdt
from sysbuild import rebuild,speakers,SPEAKERS,menu49,GTR
import menu_ko,texapply,code16,enemy,elftext
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
SRC=os.path.join(ROOT,'Grandia Xtreme (Japan, Asia).iso')
DST=os.path.join(ROOT,'Grandia Xtreme (Japan, Asia) (Korean).iso')
def main():
    t0=time.time()
    tr=ko.load_tr()
    gmap=ko.build_map(list(tr.values())+bintext.texts()+list(NAMES.values())+SPEAKERS+list(menu_ko.M.values())+[k for _,k in menu_ko.EXTRA.values()]+code16.texts()+[x for v in GTR.values() for x in v.split('|')]+enemy.texts()*40+elftext.texts()*10); enc=ko.encoder(gmap)
    with open(os.path.join(ROOT,'translation','charmap_ko.tsv'),'w',encoding='utf8') as o:
        for g in sorted(gmap): o.write('%d\t%s\n'%(g,gmap[g]))
    print('chars',sum(1 for c in gmap.values() if '가'<=c<='힣'))
    font,width=mkfont.build(gmap,open(os.path.join(ROOT,'work/font_orig.bin'),'rb').read(),open(os.path.join(ROOT,'work/width_orig.bin'),'rb').read())
    mtr={k[1]:v for k,v in tr.items() if k[0]=='mdt'}
    strr={k[1]:v for k,v in tr.items() if k[0]=='sys'}
    files={}; OVER=set(); NEN=[0]
    gidx={}
    for g,c in sorted(gmap.items()): gidx.setdefault(ko.norm(c),g)
    TN,TP,TS=texapply.prepare(); print('tex jobs',len(TN))
    for f in sorted(glob.glob(os.path.join(ROOT,'dec/FIELD/*.MDT'))):
        name=os.path.basename(f); raw=open(os.path.join(ROOT,'extract/FIELD',name),'rb').read()
        d0=open(f,'rb').read()
        d,ntex=texapply.apply(name,d0,TN,TP)
        sz,off=struct.unpack_from('<II',d,0x78)
        if off+sz>len(d) or sz==0:
            if ntex: files['/FIELD/'+name]=lzfast.compress(d,struct.unpack_from('<I',raw)[0])
            continue
        nd=rebuild_mdt(d,lambda t,body: enc(mtr[t]) if t in mtr else None)
        nd,k16=code16.apply(name,nd,gidx)
        nd,ken=enemy.apply(nd,enc,OVER); NEN[0]+=ken
        if k16: print('code16',name,k16)
        if nd!=d0: files['/FIELD/'+name]=lzfast.compress(nd,struct.unpack_from('<I',raw)[0])
    print('mdt',len(files),time.time()-t0,'enemy',NEN[0],'overflow',len(OVER))
    with open(os.path.join(ROOT,'work/enemy_over.txt'),'w',encoding='utf8') as o:
        for x in sorted(OVER): o.write(chr(9).join(map(str,x))+chr(10))
    raw=open(os.path.join(ROOT,'extract/SYS/GRXSYS.PAC'),'rb').read()
    d=open(os.path.join(ROOT,'dec/SYS/GRXSYS.PAC'),'rb').read()
    nd=rebuild(d,strr,enc,font,width)
    nd=speakers(nd,gidx); nd=menu49(nd,gidx); nd=texapply.apply_sys(nd,TS)
    print('grxsys',hex(len(d)),hex(len(nd))); open(os.path.join(ROOT,'work/grxsys_new.bin'),'wb').write(nd)
    files['/SYS/GRXSYS.PAC']=lzfast.compress(nd,struct.unpack_from('<I',raw)[0])
    bb,log=bintext.patch(open(os.path.join(ROOT,'extract/BATTLE.BIN'),'rb').read(),enc,encode_jp)
    print('battle',log); files['/BATTLE.BIN']=bb
    eb,log=elftext.patch(open(os.path.join(ROOT,'extract',elftext.ELF),'rb').read(),enc)
    print('elf',log); files['/'+elftext.ELF]=eb
    for f in sorted(glob.glob(os.path.join(ROOT,'extract/BTL_DATA/*'))):
        n=os.path.basename(f); b0=open(f,'rb').read(); b1,k=texapply.apply(n,b0,TN,TP)
        if k: files['/BTL_DATA/'+n]=b1
    print('files',len(files))
    isofs.patch(SRC,DST,files)
    print('done',time.time()-t0)
if __name__=='__main__': main()
