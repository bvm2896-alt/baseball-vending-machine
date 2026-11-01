import re,sys,json,importlib
src=open('/home/claude/kt_ks/gen_1028_long33.py',encoding='utf-8').read()
ns={'re':re}; exec(src[src.index('DIG = '):src.index('def sub_of')],ns); narr_of=ns['narr_of']
sys.path.insert(0,'.'); import lines_ks as lines_v8
def pre(t):
    def frac(m):
        s=ns['sino'](m.group(1)); j='과' if s[-1] in '일육칠팔십' else '와'
        return f'{s}{j} 3분의 {"1" if m.group(2)=="⅓" else "2"}'
    t=re.sub(r'(\d+)([⅓⅔])',frac,t); t=t.replace('1~3차전','1차전부터 3차전')
    t=re.sub(r'(\d+)구\b',lambda m: ns['sino'](m.group(1))+' 구',t); return t
out=[];tot=0;bad=0
for k,sub,nar in lines_v8.L:
    n=(nar or narr_of(pre(sub))).replace('삼 분의','삼분의').replace('삼 루수','삼루수').replace('%',' 퍼센트')
    out.append((k,n,sub)); tot+=len(n)
    for b in n.split(' / '):
        if len(b)>22: print('LONG',k,len(b),b); bad+=1
    assert len(n.split(' / '))==len(sub.split(' / ')),k
o=['# -*- coding: utf-8 -*-','"""롱폼㉟ 한국시리즈 KT 대사 (11/1). (열쇠, 나레이션, 자막)."""','LINES = [']
for k,n,sb in out: o.append('('+repr(k)+', '+repr(n)+', '+repr(sb)+'),')
o.append(']'); open('/home/claude/ks35/text_1101_long35.py','w',encoding='utf-8').write('\n'.join(o)+'\n')
R=['롱폼㉟ 한국시리즈 KT — 22일 쉰 1위팀, 통합우승 확률은? 대사','']
for i,(k,n,s) in enumerate(out,1): R.append(f'{i}. '+n.replace(' / ',' /\n    '))
open('/mnt/user-data/outputs/ks35/롱폼35_대사.txt','w',encoding='utf-8').write('\n'.join(R)+'\n')
print(len(out),tot,'long',bad)
