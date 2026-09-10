# -*- coding: utf-8 -*-
"""
타입캐스트 API로 나레이션 음성 생성
  python tts.py --test          → voice/test.mp3 한 줄 테스트
  python tts.py                 → work/narration.txt 각 줄 → work/voice/00.mp3, 01.mp3 ...
설정은 같은 폴더의 설정.txt 에서 읽는다 (TYPECAST_API_KEY, TYPECAST_VOICE_ID)
"""
import os, sys, json, time, subprocess, io
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)

def load_cfg():
    cfg = {}
    with io.open('설정.txt', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
    return cfg

CFG = load_cfg()
API_KEY = CFG.get('TYPECAST_API_KEY', '')
VOICE = CFG.get('TYPECAST_VOICE_ID', '')
if not API_KEY or not VOICE:
    sys.exit('설정.txt 에 TYPECAST_API_KEY 와 TYPECAST_VOICE_ID 를 채워주세요.')

EMOTION = CFG.get('TTS_EMOTION', 'smart')      # smart | normal | happy | sad | angry | whisper | toneup | tonemid | tonedown
INTENSITY = float(CFG.get('TTS_INTENSITY', '1.0'))
TEMPO = float(CFG.get('TTS_TEMPO', '1.0'))      # 타입캐스트 자체 배속. 줄별 속도 조절은 build.py 가 하므로 보통 1.0
URL = 'https://api.typecast.ai/v1/text-to-speech'
HEAD = {'X-API-KEY': API_KEY, 'Content-Type': 'application/json'}

import re
def check_audio(path, text):
    """길이가 글자 수 대비 비정상이거나 클리핑이 있으면 False"""
    try:
        d = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',path],capture_output=True,text=True).stdout.strip())
        r = subprocess.run(['ffmpeg','-i',path,'-af','volumedetect','-f','null','-'],capture_output=True,text=True)
        mx = float(re.search(r'max_volume: ([\-\d.]+)', r.stderr).group(1))
        syl = len(re.findall(r'[가-힣]', text)) or 1
        rate = syl / max(d, 0.1)
        if mx > -0.05: return False, f'클리핑 {mx}dB'   # 음량 정리는 build.py 가 하므로 진짜 클리핑만 재시도
        if rate > 9.5 or rate < 2.5: return False, f'길이 이상 {d:.1f}s/{syl}음절'
        return True, ''
    except Exception as e:
        return True, ''

def prompt_variants(prev, nxt):
    """설정.txt 의 TTS_EMOTION 에 따라 prompt 후보를 순서대로 (400 이면 다음 후보로)"""
    if EMOTION == 'smart':
        return [{'emotion_type': 'smart', 'previous_text': prev, 'next_text': nxt}]
    return [{'emotion_type': 'preset', 'emotion_preset': EMOTION, 'emotion_intensity': INTENSITY},
            {'emotion_preset': EMOTION, 'emotion_intensity': INTENSITY},
            {'emotion_type': 'smart', 'previous_text': prev, 'next_text': nxt}]

def synth(text, prev='', nxt='', out_path='work/voice/out.mp3'):
    """한 줄 합성. 앞뒤 문장을 같이 보내면 억양이 자연스럽게 이어진다."""
    prompts = prompt_variants(prev, nxt)
    payload = {
        'model': 'ssfm-v30',
        'text': text,
        'voice_id': VOICE,
        'prompt': prompts[0],
        'output': ({'audio_format': 'mp3', 'audio_tempo': TEMPO} if abs(TEMPO - 1.0) > 0.01 else {'audio_format': 'mp3'}),
    }
    pi = 0
    for attempt in range(6):
        r = requests.post(URL, headers=HEAD, json=payload, timeout=60)
        if r.status_code == 200:
            ctype = r.headers.get('Content-Type', '')
            print(f'  응답 {ctype} {len(r.content)} bytes')
            if 'wav' in ctype or r.content[:4] == b'RIFF':
                # wav 로 왔으면 mp3 로 변환 (헤더의 길이 정보가 틀린 경우가 있어 무시하고 끝까지 읽는다)
                tmp = out_path + '.wav'
                open(tmp, 'wb').write(r.content)
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ignore_length', '1', '-i', tmp,
                                '-b:a', '192k', out_path], check=True)
                if '--keep' not in sys.argv:
                    os.remove(tmp)
            else:
                open(out_path, 'wb').write(r.content)
            ok, why = check_audio(out_path, text)
            if not ok and attempt < 5:
                print(f'  품질 재시도({why})'); time.sleep(1); continue
            return True
        if r.status_code == 400:
            # 감정 형식이 안 맞으면 다음 후보, 그래도 안 되면 output 의 배속 옵션을 뺀다
            if pi + 1 < len(prompts):
                pi += 1; payload['prompt'] = prompts[pi]; print(f'  감정 형식 재시도({pi})'); continue
            if 'audio_tempo' in payload.get('output', {}):
                payload['output'] = {'audio_format': 'mp3'}; print('  배속 옵션 없이 재시도'); continue
            if 'output' in payload:
                payload.pop('output'); continue
        if r.status_code in (429, 500, 502, 503):
            time.sleep(2 + attempt * 2)
            continue
        print(f'  실패 {r.status_code}: {r.text[:300]}')
        return False
    return False

os.makedirs('work/voice', exist_ok=True)

if '--test' in sys.argv:
    ok = synth('야구자판기 음성 테스트예요. 삼성이 일위, 케이티가 영점오 게임 차예요.', out_path='work/voice/test.mp3')
    print('OK → work/voice/test.mp3 재생해 보세요.' if ok else '실패')
    sys.exit(0 if ok else 1)

lines = [l.strip() for l in io.open('work/narration.txt', encoding='utf-8-sig') if l.strip()]
PAUSE = float(CFG.get('TTS_PAUSE', '0.12'))   # 대사 안의 " / " 표시 자리에서 쉬는 시간(초). 구간 자체의 앞뒤 무음은 잘라내므로 아주 짧게

def synth_line(line, prev, nxt, out):
    """한 줄 합성. 줄 안에 ' / ' 가 있으면 호흡 단위로 나눠 따로 합성한 뒤 사이에 짧은 쉼을 넣어 붙인다."""
    segs = [x.strip() for x in line.split('/') if x.strip()]
    if len(segs) <= 1:
        try: os.remove(out.replace('.mp3', '.segs.json'))
        except Exception: pass
        return synth(segs[0] if segs else line, prev, nxt, out)
    parts = []
    for j, seg in enumerate(segs):
        p = segs[j - 1] if j > 0 else prev
        n = segs[j + 1] if j + 1 < len(segs) else nxt
        tmp = out.replace('.mp3', f'_s{j}.mp3')
        if not synth(seg, p, n, tmp): return False
        wav = tmp.replace('.mp3', '.wav')   # 이어 붙이기는 wav 로 (형식을 맞춰야 함)
        # 구간 앞뒤의 무음을 잘라낸다(각 끝에 0.05초만 남김) → 구간 사이가 늘어지지 않게
        trim = ('silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.05,areverse,'
                'silenceremove=start_periods=1:start_threshold=-42dB:start_silence=0.06,areverse')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', tmp, '-af', trim, '-ar', '44100', '-ac', '1', wav], check=True)
        os.remove(tmp); parts.append(wav)
    sil = out.replace('.mp3', '_sil.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', f'{PAUSE:.2f}', sil], check=True)
    lst = out.replace('.mp3', '_list.txt')
    with open(lst, 'w', encoding='utf-8') as f:
        for j, ptn in enumerate(parts):
            if j: f.write(f"file '{os.path.basename(sil)}'\n")
            f.write(f"file '{os.path.basename(ptn)}'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-ar', '44100', '-ac', '1', '-b:a', '192k', out], check=True)
    # 자막을 호흡 단위로 맞추기 위해 각 구간 길이를 기록
    durs = []
    for ptn in parts:
        d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', ptn], capture_output=True, text=True).stdout.strip()
        durs.append(float(d or 0))
    json.dump({'durs': durs, 'pause': PAUSE}, open(out.replace('.mp3', '.segs.json'), 'w'))
    for f_ in parts + [sil, lst]:
        try: os.remove(f_)
        except Exception: pass
    return True

only = None
for a in sys.argv:
    if a.startswith('--only='): only = {int(x) for x in a.split('=',1)[1].replace(',', ' ').split()}
print(f'{len(lines)}줄 합성 시작' + (f' (줄 {sorted(only)} 만)' if only else ''))
fail = 0
for i, line in enumerate(lines):
    if only is not None and i not in only: continue
    prev = lines[i-1] if i > 0 else ''
    nxt = lines[i+1] if i+1 < len(lines) else ''
    out = f'work/voice/{i:02d}.mp3'
    ok = synth_line(line, prev, nxt, out)
    print(f'{i:02d} {"OK " if ok else "XX "} {line}')
    fail += (not ok)
    time.sleep(0.3)
if fail:
    sys.exit(f'{fail}줄 실패')
print('완료')
