import math,collections,os,re
HERE=os.path.dirname(os.path.abspath(__file__))
txt=open(os.path.join(HERE,'..','translation','mdt_jp.tsv'),encoding='utf8').read()
txt=re.sub(r'\{[0-9A-F]+\}','',txt)
uni=collections.Counter(txt); bi=collections.Counter(zip(txt,txt[1:]))
N=sum(uni.values()); V=len(uni)+1
def score(s):
    s=re.sub(r'\{[0-9A-F]+\}','',s)
    if len(s)<2: return -99
    lp=0
    for a,b in zip(s,s[1:]):
        lp+=math.log((bi[(a,b)]+0.1)/(uni[a]+0.1*V))
    return lp/(len(s)-1)
