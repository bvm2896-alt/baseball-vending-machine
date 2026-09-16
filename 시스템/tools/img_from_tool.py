#!/usr/bin/env python3
"""브라우저 JS 결과 파일(data:image/...;base64 문자열)을 이미지 파일로 저장.
사용: python3 img_from_tool.py <tool-results 파일> <저장 경로.jpg>
(Claude_Browser javascript_tool 로 window.__d 를 돌려받으면 결과가 tool-results/*.txt 에 저장된다)"""
import sys, json, re, base64
src, out = sys.argv[1], sys.argv[2]
arr = json.load(open(src)); t = arr[0]['text'] if isinstance(arr, list) else str(arr)
m = re.search(r'data:image/(?:jpeg|png|webp);base64,([A-Za-z0-9+/=]+)', t)
if not m: sys.exit('base64 이미지가 없음')
data = base64.b64decode(m.group(1)); open(out, 'wb').write(data); print(out, len(data), 'bytes')
