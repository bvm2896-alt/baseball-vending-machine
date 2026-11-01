set -e
cd /home/claude/ks35; python3 build_text.py; python3 gen_1101_long35.py episodes/2026-11-01_롱폼.json; python3 assemble.py
cp episodes/2026-11-01_롱폼.json /home/claude/po45/sys2/episodes/; cp text_1101_long35.py gen_1101_long35.py /home/claude/po45/sys2/tools/
cd /home/claude/po45/sys2; for t in rule_check precheck read_check late_check; do echo "== $t"; python3 tools/$t.py episodes/2026-11-01_롱폼.json 2>&1 | grep -v "^\s*$" | grep -E "X|통과|늦게|사전|읽기 검사" | head -20; done
