#!/usr/bin/env python3
"""콘티 미리보기 html 만들기(클라우드/PC 공용, 렌더 없이 장면만 확인).
사용: python3 tools/preview.py episodes/2026-09-16_순위.json [template.html] [out.html]
템플릿을 안 주면 시리즈에 맞춰 고른다(순위 template.html / 이슈 template_issue.html / 분석 template_analysis.html).
그 다음 node tools/shot.js out.html 0,1,3 prefix 로 장면별 png 를 찍는다."""
import os, json, io, sys, os
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(HERE); sys.path.insert(0, HERE); sys.argv = ['build.py'] + sys.argv[1:]
import build
epp = sys.argv[1]
ep = json.load(io.open(epp, encoding='utf-8-sig'))
tpl = sys.argv[2] if len(sys.argv) > 2 else build.template_for(ep) if hasattr(build, 'template_for') else 'template.html'
out = sys.argv[3] if len(sys.argv) > 3 else 'work/preview.html'
N = len(ep['lines'])
EP = build.load_episode(epp); EP['_path'] = epp
EP['bounds'] = [float(i + 1) for i in range(N)]
def _sub(x):
    t = x['sub'] if isinstance(x, dict) else str(x)
    return t.split('|')[-1] if os.environ.get('PV_LAST') else t.split('|')[0]
EP['subs'] = [[i, i + 1, _sub(ep['lines'][i])] for i in range(N)]
EP['logos'] = build.logos_data_uri(); EP['photos'] = build.photos_data_uri(ep, epp); EP['photoSizes'] = build.PHOTO_SIZES; EP['total'] = float(N)
html = io.open(tpl, encoding='utf-8').read().replace('__FONT_DIR__', build.font_dir_url())
html = html.replace('<script>', '<script>window.EP=' + json.dumps(EP, ensure_ascii=False) + ';</script><script>', 1)
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
io.open(out, 'w', encoding='utf-8').write(html)
print('ok', out, 'lines', N, 'photos', len(EP['photos']), 'template', tpl)
