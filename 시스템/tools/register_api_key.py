# -*- coding: utf-8 -*-
"""10/7: 회사 PC 는 보안 프로그램(DOCURAY)이 설정.txt 를 암호화해서 tts.py 가 타입캐스트 키를 못 읽는다.
→ 키를 윈도우 '사용자 환경 변수'로 한 번 등록해 두면 tts.py 가 설정.txt 대신 그걸 읽는다(파일이 아니라 암호화되지 않음).
실행: 야구롱폼\\API키등록.cmd (더블클릭) → 집 PC 설정.txt 의 값을 붙여 넣기. 키는 채팅에 붙이지 않는다."""
import subprocess, sys

ITEMS = [('TYPECAST_API_KEY', '타입캐스트 API 키 (1번 계정)', True),
         ('TYPECAST_VOICE_ID', '목소리 ID (1번 계정)', True),
         ('TYPECAST_API_KEY2', '2번 계정 API 키 (없으면 그냥 Enter)', False),
         ('TYPECAST_VOICE_ID2', '2번 계정 목소리 ID (없으면 그냥 Enter)', False)]

print('=' * 60)
print(' 타입캐스트 키를 이 PC 의 윈도우 환경 변수로 등록해요')
print(' 집 PC 시스템\\설정.txt 의 같은 이름 줄에서 = 뒤 값을 복사해 붙여 넣으세요')
print(' (붙여넣기: 마우스 오른쪽 클릭 또는 Ctrl+V)')
print('=' * 60)
done = []
for name, label, need in ITEMS:
    while True:
        v = input(f'{label}\n  {name} = ').strip().strip('"').strip("'")
        if v or not need: break
        print('  비어 있어요. 다시 붙여 넣어 주세요.')
    if not v: continue
    r = subprocess.run(['setx', name, v], capture_output=True, text=True)
    if r.returncode != 0:
        print(f'  등록 실패: {name} — {(r.stderr or r.stdout).strip()}'); sys.exit(1)
    done.append(f'{name} ({len(v)}자, 끝 4자리 …{v[-4:]})')
print('-' * 60)
print('등록했어요:'); [print('  ' + d) for d in done]
print('이 창을 닫고, 롱폼검수.cmd 를 새로 더블클릭해서 다시 실행하세요.')
print('(이미 열려 있던 창에는 반영되지 않아요)')
