# -*- coding: utf-8 -*-
"""네이버 스포츠 KBO 팀순위 HTML → JSON
해시가 붙는 CSS 클래스명(Table_table_area__icfvj 등)은 프론트 빌드마다 바뀌므로
절대 셀렉터로 쓰지 않는다. 대신 빌드와 무관한 3개 앵커만 사용한다.
  1) 순위     : >N<span class="blind">위</span>
  2) 팀 코드  : href=".../team/SS"   (SS, KT, LG ... 고정 코드)
  3) 지표     : <span class="blind">wra</span>0.614   (의미 이름이 그대로 노출됨)
"""
import re, json, sys, datetime

TEAM = {'SS':'삼성','KT':'KT','LG':'LG','HT':'KIA','OB':'두산',
        'NC':'NC','LT':'롯데','SK':'SSG','HH':'한화','WO':'키움'}
FIELDS = ['wra','gameBehind','gameCount','winGameCount',
          'loseGameCount','drawnGameCount','continuousGameResult',
          'offenseHra','defenseEra']

ROW = re.compile(r'>(\d{1,2})<span class="blind">위</span>')
CODE = re.compile(r'/team/([A-Z]{2})"')
STAT = re.compile(r'<span class="blind">([A-Za-z]+)</span>\s*([^<]+)')
RESULT = re.compile(r'<span class="blind">(승|패|무)</span>')

def parse(html):
    # 순위 표기를 기준으로 팀 블록을 자른다
    marks = [m.start() for m in ROW.finditer(html)]
    rows = []
    for i, start in enumerate(marks):
        end = marks[i+1] if i+1 < len(marks) else len(html)
        block = html[start:end]
        rank = int(ROW.search(block).group(1))
        code = CODE.search(block)
        if not code:
            continue
        code = code.group(1)
        stats = {k: v.strip() for k, v in STAT.findall(block) if k in FIELDS}
        if len(stats) < len(FIELDS):
            continue
        recent = RESULT.findall(block)[:5]
        rows.append({
            'rank': rank, 'code': code, 'team': TEAM.get(code, code),
            'winRate': float(stats['wra']),
            'gameBehind': float(stats['gameBehind']),
            'games': int(stats['gameCount']),
            'win': int(stats['winGameCount']),
            'lose': int(stats['loseGameCount']),
            'draw': int(stats['drawnGameCount']),
            'streak': stats['continuousGameResult'],
            'avg': float(stats['offenseHra']),
            'era': float(stats['defenseEra']),
            'recent5': recent,
        })
    return {'date': datetime.date.today().isoformat(),
            'source': 'naver-sports-kbo-teamrank',
            'standings': sorted(rows, key=lambda r: r['rank'])}

if __name__ == '__main__':
    html = open(sys.argv[1], encoding='utf-8').read()
    out = parse(html)
    print(json.dumps(out, ensure_ascii=False, indent=2))
