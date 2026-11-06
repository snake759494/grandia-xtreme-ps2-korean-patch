from jppool import J
# u16 glyph strings embedded in field code (not in the message table). file -> [(jp, ko)]
# ko must be <= jp length; the rest is zero-filled (terminates early).
C16={'2008.MDT':[  # concert minigame
 (J('0f8e5b4de960b3b2'),'결정'),(J('269b0f92e460f3dd'),'취소'),(J('f8d836f551467a79'),'갈매기 정'),(J('8b7dfdca28cb4b5c'),'그라나 세이버'),
 (J('1a03590319619715'),'그란디아의 테마'),(J('15214cab0f1a0a0a'),'『크래시 헤즈'),(J('0f48c555b5d7d524'),'콘서트』'),
 (J('ff9f14ca0a0b2a6c'),'자'),(J('98100e5f052d55e0'),'무엇을'),(J('5745ae28651abe60'),'모두에게 들려줄까？'),(J('95c765cab83a1166'),'흠'),
 (J('7202bebc7647213c'),'포근한 곡으로 가지？'),(J('a9c4912c0b981b8d'),'용맹한 곡으로 가지？'),
 (J('d418e9f0f86890dc'),'춤추고 싶은 곡으로 가지？'),(J('90fe4a0593a58097'),'웅대한 곡으로 가지？'),
 (J('99a835fed8889bc6'),'힘나는 곡으로 가지？'),(J('c61e14d34a3b1d65'),'연주곡은'),(J('5c875d2be226a54e'),'이걸로 됐나？'),
 (J('4d6d330e48a6a758'),'사양 변경으로 표시 안 함'),(J('9ce951aa8e511f13'),'그러면'),
 (J('d0074e27cf26e446'),'모두에게 들려줄 건가？'),(J('ce4a37e9b3664ce0'),'그럼'),(J('457800e9b28ee386'),'캐로의 무대는'),
 (J('63d5062196df49a4'),'자네가 연출해 주게'),(J('2e2140ef2cf9fdec'),'５마리까진'),(J('29e6ef859447c118'),'자유롭게 배치할 수 있네'),
 (J('aeaca5480c720aa7'),'먼저'),(J('35fd6059fb767a9c'),'캐로를 배치할 곳을 정해 주게'),(J('21e4faf6c20ce749'),'캐로 교체'),
 (J('6cceb9ce8fddaa19'),'포메이션 변경'),(J('7315e684b4817f24'),'캐로 빼기'),(J('5ef45be753b7b742'),'콘서트 시작'),
 (J('9a25572699f67934'),'캐로를 교체하는 거지？'),(J('27958821cf99fa5c'),'캐로의 포메이션을 바꾸는 건가？'),
 (J('7ad285963d9276a6'),'캐로를 빼는 거지？'),(J('ac73b89def055e38'),'콘서트를 시작하는 건가？'),
 (J('650d8f4a26952e5b'),'이 캐로를 교체하는 건가？'),(J('02efa74504b6aa63'),'이 자리에 캐로를 넣는 건가？'),
 (J('add97ba54f6b7e67'),'좋아'),(J('5a66a1849994f3ee'),'캐로를 넣었네！'),(J('bc18111d6d9d9c5f'),'이 자리의 캐로와 교체하는 건가？'),
 (J('2af585fc16d24fd8'),'캐로를 교체했네！'),(J('646bd2e4a62b28e6'),'캐로는 ５마리까지네'),
 (J('1df49e922f75d1e4'),'더는 무대에 올릴 수 없네！'),(J('34cce34e3f3c32c6'),'이 자리를 바꾸는 건가？'),
 (J('e3ca80d602da25cc'),'어디로 바꾸는 건가？'),(J('220b23bc24e35671'),'포메이션을 바꿨네'),
 (J('0290a4301ffba7e9'),'이 캐로를 빼는 거지？'),(J('ef0769380c12b8ef'),'캐로를 뺐네！'),(J('74d5a70fb995feb0'),'준비 완료'),
 (J('c1f26551087a17a7'),'콘서트를 시작하지！'),(J('a8121ae3d0580071'),'콘서트는 캐로 없이는 못 하네！'),
]}
LOTTO=[(J('0f8e5b4de960b3b2'),'결정'),(J('269b0f92e460f3dd'),'취소'),(J('ff9f14ca0a0b2a6c'),'자'),(J('2559f219b66d98ce'),'뭘로 할까？'),
 (J('8e24d35a1d45fea9'),'좋아하는 마크를 고르게！'),(J('61a0b52825115fc9'),'이걸로 되겠는가？'),
 (J('b49edb4e38c9022a'),'공 추가도 할 수 있네！'),(J('f36ecf91a2f6c8bc'),'１개당'),(J('1a63426dbb1b7a12'),'Ｇ일세！'),
 (J('bb0592e39fa5ae2f'),'더 추가는 못하네！'),(J('cfe79269616bca54'),'추가 접수는 끝났네！'),
 (J('4407655d54eac9cd'),'돈이 모자라네！'),(J('106bf256259a7d52'),'좋아！'),(J('68788784755b5f57'),'당첨일세！！'),(J('ed7f5bcf0ef4d7e0'),'꽝일세！'),
 (J('51b4b8ecb59c5856'),'아쉽구먼……'),(J('8712f7f81ebb7ce4'),'획득 아이템은 이걸세！！！'),
 (J('4aa25463635e9d74'),'현재 미사용'),(J('25946024bda8033e'),'소지금'),(J('fdc2efdeda54efcd'),'상품'),(J('e6e78049a07fc287'),'기호')]
C16['2090.MDT']=LOTTO; C16['E490.MDT']=LOTTO; C16['3034.MDT']=C16['2008.MDT']
def texts(): return [k for L in C16.values() for _,k in L]
def apply(name,d,gidx,blank=2107):
    import struct
    from gxtext import MAP
    if name not in C16: return d,0
    rv={}
    for i,c in enumerate(MAP): rv.setdefault(c,i)
    d=bytearray(d); n=0
    for jp,ko in C16[name]:
        assert len(ko)<=len(jp),(jp,ko)
        pat=b''.join(struct.pack('<H',rv[c]) for c in jp)+b'\0\0'
        new=b''.join(struct.pack('<H',blank if c in ' 　' else gidx[c]) for c in ko)
        new=new+b'\0'*(len(pat)-len(new))
        i=d.find(pat); k=0
        while i>=0:
            if i%2==0 and d[i-2:i]==b'\0\0': d[i:i+len(pat)]=new; k+=1
            i=d.find(pat,i+1)
        if not k: print('code16 miss',name,jp)
        n+=k
    return bytes(d),n
