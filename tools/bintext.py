from jppool import J
# fixed-slot strings inside BATTLE.BIN (raw overlay): (jp, [ko candidates longest-first])
BATTLE=[
(J('50eb6b32e201689b'),['분노가 발동했다！','분노 발동！']),
(J('c21bd718afed5f0d'),['수동 조작','수동']),
(J('dfdde6d41fa17146'),['정정당당']),(J('a6112652a261accb'),['일점집중']),(J('6a8b5f9b544054e5'),['광희난무']),(J('df8dcc02ee45683d'),['비겁천만']),
(J('93c277ac2248cf66'),['안전제일']),(J('56c877c62a633888'),['타력본원']),(J('59655b3e85a7de7c'),['두뇌명석']),
(J('eb1a2d429c584dc9'),['실행']),(J('72796cd16c9d108b'),['작전']),(J('cd40f69d90b80167'),['단일']),(J('271181579b62801a'),['원형']),(J('3e947c4339e36ddf'),['부채꼴','부채']),(J('85c0ff38694740df'),['전체']),(J('971b6e5a0a75ac77'),['특수']),
(J('6f0f16e0c09884cc'),['무기']),(J('720c230fe99cdf33'),['신체']),(J('49e434723c9f9fb7'),['장식']),(J('708306c83e068dd8'),['장비품']),
(J('dbb0d097daefb3a6'),['도구１']),(J('bf114cd49bf32d04'),['도구２']),(J('68a0e245f25a392c'),['도구３']),(J('5efd6b3bbdadf276'),['도구４']),(J('c58796c2a7b7f422'),['도구５']),
(J('d982c1d2ef7bb2b2'),['필살기']),(J('bd22f46e64e8bc06'),['합체기１']),(J('471e7e82d6106f10'),['합체기２']),(J('ccdfe0bbe2223bd6'),['합체기３']),(J('83ae80201ae9fe30'),['합체기４']),(J('8f1235447ac96d98'),['합체기５']),
(J('55e95614c8375c4f'),['대기 중','대기']),(J('44900dcc3cd00cc8'),['전투불능']),(J('6360f7c7fe827cb9'),['커맨드 입력','명령 입력']),(J('2029e612c90df48d'),['방어']),
(J('e0e8b5311789cf8d'),['을(를) 습득','습득！']),(J('bac8ea504b9f8b3c'),['이(가) 파손','파손！']),
(J('2d210d68f8ae1d89'),['콤보']),(J('e2c97c717b6603be'),['\ubc29\uc5b4\u30fb\ud68c\ud53c']),(J('ea57571dfaa3901f'),['철수']),(J('51fd93fb67555aba'),['도구']),(J('e7d0d2013b10aab3'),['크리티컬']),(J('53ce4fd2b0ed8831'),['마법']),
(J('9713721612b2a197'),['기술','기']),(J('cdd671c52f030b75'),['직선']),(J('9b820d682d20d199'),['주위']),(J('bbef2b0a0528161b'),['팔']),(J('e349ae1338509622'),['머리','두']),(J('16fdcc7e77464f45'),['발']),
(J('84e21730fa45b976'),['선제공격']),(J('49bd4a92c6230daf'),['기습당했다！','기습！']),(J('926119ad0494a1d0'),['도주 성공']),(J('b82d1020626cf7b8'),['도주 실패']),
]
def texts():
    return [k for _,ks in BATTLE for k in ks]
def patch(b,enc,jpenc=None):
    import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
    from strscan import scan
    b=bytearray(b); log=[]; want={jp:kos for jp,kos in BATTLE}; done=set()
    for pos,L,t,_,_ in scan(bytes(b),1):
        if t not in want: continue
        j=pos+L
        while j<len(b) and b[j]==0: j+=1
        for ko in want[t]:
            e=enc(ko)
            if len(e)+1<=j-pos: b[pos:j]=e+bytes(j-pos-len(e)); done.add(t); break
        else: log.append('NOFIT '+t)
    log+=['MISS '+jp for jp in want if jp not in done]
    return bytes(b),log
