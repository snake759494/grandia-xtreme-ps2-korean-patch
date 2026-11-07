from jppool import J
# UI strings in the executable's .rodata (status abbreviations, elements, monster types, ailments,
# equipment info labels, strategy names and strategy help). Each string has its own pointer, so it is
# replaced in place: Korean bytes <= original bytes + trailing NUL padding, the rest zero-filled.
ELF='SLPM_650.89'
RODATA=(0xa0f80,0xa8af0)
T=[
(J('8d4f769e03806cc2'),['공']),(J('fbee8d20cb2e75d5'),['방']),(J('5b415cad5757c2ba'),['마']),(J('2cffdb150535d322'),['저']),(J('2a2b777ae485ecb8'),['행']),(J('c59a75dc9cf38591'),['이']),
(J('efb2620838c4f431'),['불']),(J('0b703039737fbd87'),['풍']),(J('8ffbf192934ab70c'),['물']),(J('90fbc9b1ac2e78e1'),['땅']),(J('29e0d877fc579e5f'),['폭']),(J('deaefde2be7e8304'),['뇌']),(J('e2fc60d070bd81ec'),['빙']),(J('d92836b0d9bfe741'),['숲']),
(J('9279d24cae639578'),['폭렬']),(J('945f67938ffcacf0'),['번개']),(J('af68b296265db0ca'),['눈보라','설']),(J('70f4c18c327660f1'),['삼림']),(J('7d3c35c29be1de8b'),['속성']),(J('7bf5955ac6a60173'),['강점']),(J('2fc1f2b871000fa2'),['약점']),
(J('d55be023c2b27c56'),['있음',J('fbd5b75066a6dc39')]),(J('6eff79fb2b1a161c'),['특수효과']),(J('1d8ef3e629251dfb'),['사용효과']),(J('894ab6bc9edbda4c'),['속성방어']),(J('202d55dd6ab57965'),['상태내성']),(J('19c79fec0e8bbb23'),['특수방어']),
(J('16e9a68bafa78cb0'),['에 유효','에유효']),(J('d4a400514aa6f121'),['조류']),(J('4a05fa9d67bfb537'),['곤충계']),(J('7d5ed47981582987'),['파충류']),(J('657adb570f460525'),['인간형']),(J('6e498744f4a0aa5a'),['악마계']),
(J('b4641d6d19c5da49'),['불사계']),(J('957009e07b4a8214'),['마수계']),(J('431b6685f09839f9'),['식물계']),(J('4917ccdc2020dc2c'),['부유계']),(J('42f147c39c64bcd3'),['수서류']),(J('b4e54fa511597d2e'),['용계','용']),(J('af8082f48b6fd654'),['물질계']),
(J('8aa0efae2de16a9c'),['독']),(J('0a74c8c396e85eaa'),['수면']),(J('ec47f89a66ace18b'),['마비']),(J('a17f70a8d3d66e14'),['정지']),(J('3216abca99d9ad3a'),['혼란']),(J('fa3a81b735b119c8'),['기봉인']),(J('d908b2a3e8da4f58'),['마봉인']),(J('9fd003a72958e7a8'),['병']),
(J('c91391b06649da2d'),['저주']),(J('d6a85caed086815b'),['결계']),(J('1492c464f7faf94d'),['소멸']),(J('2e80fbbe32e3eec1'),['즉사']),(J('f11e32f4cf409755'),['효과']),(J('116611cf8c5c86e8'),['내성']),(J('c4bbe28879da346b'),['파손율']),
(J('4c9b62f529fd43f7'),['의 공격을 경감한다','의 공격을 경감']),(J('c89cacba47a1d82c'),['대상']),(J('9820b7636a8b8fab'),['아군']),(J('b0af5773fc2c15f2'),['적']),(J('55e9a3f996fc1776'),['자신']),(J('4220cd2fb7ede69a'),['전원']),
(J('c8d55b4cf985f2bd'),['범위']),(J('cd40f69d90b80167'),['단일']),(J('271181579b62801a'),['원형']),(J('cdd671c52f030b75'),['직선']),(J('3e947c4339e36ddf'),['부채꼴','부채']),(J('85c0ff38694740df'),['전체']),(J('9b820d682d20d199'),['주위']),(J('971b6e5a0a75ac77'),['특수']),
(J('c21bd718afed5f0d'),['수동 조작','수동']),(J('dfdde6d41fa17146'),['정정당당']),(J('a6112652a261accb'),['일점집중']),(J('6a8b5f9b544054e5'),['광희난무']),(J('df8dcc02ee45683d'),['비겁천만']),
(J('93c277ac2248cf66'),['안전제일']),(J('56c877c62a633888'),['타력본원']),(J('59655b3e85a7de7c'),['두뇌명석']),
(J('4e9b0ef725a449b9'),['－－／작전 없음','－－／작전없음']),
(J('bd0caf40edbf3de7'),['절약／일반 공격 중시 작전','절약／일반공격 중시']),
(J('eb89e6f516f614c0'),['격파／단일 공격 중시 작전','격파／단일공격 중시']),
(J('63854b743fc22b4b'),['전력／범위 공격 중시 작전','전력／범위공격 중시']),
(J('73ee1cd01ade274c'),['지원／서포트 중시 작전','지원／서포트 중시']),
(J('a5b2f8c0fac4bedf'),['신중／회복 중시 작전','신중／회복 중시']),
(J('3fbb514cb7f7330a'),['소극／방어 중시 작전','소극／방어 중시']),
(J('c32ba39324bb91a5'),['만능／균형 중시 작전','만능／균형 중시']),
(J('857b3e2072133c1b'),['플레이어가 직접 커맨드를 입력한다','플레이어가 커맨드를 입력']),
(J('c303085906ab09a0'),['일반 공격만으로 싸운다','일반 공격만 쓴다']),
(J('00af7bf01d523e8e'),['집중 공격으로 적의 수를 확실히 줄인다','집중 공격으로 적의 수를 줄인다']),
(J('6ab06553f73de88d'),['필살기나 마법으로 큰 대미지를 준다']),
(J('9823f65fb83bb1c2'),['보조 공격으로 전투를 유리하게 이끈다','보조 공격으로 전투를 유리하게']),
(J('51413bcd1acdf947'),['쓰러지지 않도록 자주 회복한다','쓰러지지 않게 자주 회복한다']),
(J('fd048457b3954015'),['아군을 지원하고 직접 공격하지 않는다','아군을 돕고 공격하지 않는다']),
(J('70fe05a2a4a6f1da'),['전투 상황과 적의 강함에 맞춰 싸운다','상황에 맞춰 싸운다']),
]
def texts(): return [k for _,ks in T for k in ks]
def patch(b,enc):
    import re
    from gxtext import decode
    b=bytearray(b); want=dict(T); done=set(); log=[]
    a0,a1=RODATA
    for m in re.finditer(rb'(?<=\x00)[^\x00]+(?=\x00)',bytes(b[a0:a1])):
        p=a0+m.start(); L=len(m.group())
        try: t=decode(m.group())[0]
        except Exception: continue
        if t not in want: continue
        j=p+L
        while j<a1 and b[j]==0: j+=1
        for ko in want[t]:
            e=enc(ko)
            if len(e)+1<=j-p: b[p:j]=e+bytes(j-p-len(e)); done.add(t); break
        else: log.append('NOFIT '+t)
    log+=['MISS '+jp for jp in want if jp not in done]
    return bytes(b),log
