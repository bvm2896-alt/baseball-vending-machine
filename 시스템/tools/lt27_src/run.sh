set -e
cd /home/claude/lt27; python3 build_text.py
{ printf '# -*- coding: utf-8 -*-\n"""11/4 롱폼「롯데 2027 스토브리그」 콘티 (회사 PC · 음성 API).\n대사 = tools/text_1104_lt.py. 근거 = 기사 원문 2곳 이상(lt27 facts_A·B).\n실행: python -X utf8 tools/gen_1104_lt.py → episodes/2026-11-04_롱폼.json"""\n'; cat gen_head.py gen_body_lt.py gen_tail_lt.py; } > gen_1104_lt.py
python3 gen_1104_lt.py episodes/2026-11-04_롱폼.json
for t in rule_check precheck read_check late_check; do echo "== $t"; python3 /home/claude/po45/sys2/tools/$t.py episodes/2026-11-04_롱폼.json 2>&1 | grep -v "^\s*$" | head -40; done
