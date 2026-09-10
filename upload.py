# -*- coding: utf-8 -*-
"""
유튜브 업로드 / 공개 전환 / 삭제
  python upload.py auth                          → 최초 1회 브라우저 로그인 (token.json 생성)
  python upload.py upload out/2026-09-06.mp4 episodes/2026-09-06.json   → 비공개 업로드, videoId 출력
  python upload.py update VIDEO_ID episodes/2026-09-06.json → 제목/설명/태그만 교체
  (VIDEO_ID 자리에 latest 라고 쓰면 가장 최근 올린 영상)
  python upload.py thumb  VIDEO_ID out/2026-09-06_thumb.jpg → 썸네일 등록 (채널 전화번호 인증 필요)
  python upload.py publish VIDEO_ID              → 공개로 전환
  python upload.py delete VIDEO_ID               → 삭제
필요: 설정.txt 의 YOUTUBE_CLIENT_SECRET_FILE (구글 클라우드에서 받은 client_secret.json)
"""
import os, sys, json, io
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube']

def cfg():
    c = {}
    for line in io.open('설정.txt', encoding='utf-8-sig'):
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1); c[k.strip()] = v.strip()
    return c

def service():
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            secret = cfg().get('YOUTUBE_CLIENT_SECRET_FILE', 'client_secret.json')
            if not os.path.exists(secret):
                raise SystemExit(f'{secret} 파일이 없습니다. 구글 클라우드 콘솔에서 받아서 이 폴더에 넣어주세요.')
            flow = InstalledAppFlow.from_client_secrets_file(secret, SCOPES)
            creds = flow.run_local_server(port=0, prompt='consent')
        io.open('token.json', 'w', encoding='utf-8').write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

def upload(video, ep_path, privacy='private'):
    from googleapiclient.http import MediaFileUpload
    ep = json.load(io.open(ep_path, encoding='utf-8-sig'))
    yt = ep.get('youtube', {})
    title = yt.get('title') or ep.get('title') or '오늘의 KBO'
    if '#shorts' not in title.lower() and '#shorts' not in yt.get('description', '').lower(): title = title + ' #Shorts'
    body = {
        'snippet': {'title': title[:100], 'description': yt.get('description', ''),
                    'tags': yt.get('tags', []), 'categoryId': '17', 'defaultLanguage': 'ko'},
        'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False},
    }
    media = MediaFileUpload(video, chunksize=8 * 1024 * 1024, resumable=True, mimetype='video/mp4')
    req = service().videos().insert(part='snippet,status', body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
    vid = resp['id']
    print('VIDEO_ID', vid)
    return vid

def latest_video_id():
    """내 채널에 가장 최근 올린 영상 ID"""
    s = service()
    ch = s.channels().list(part='contentDetails', mine=True).execute()
    pl = ch['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    it = s.playlistItems().list(part='contentDetails', playlistId=pl, maxResults=1).execute()
    return it['items'][0]['contentDetails']['videoId']

def resolve(vid):
    if vid in ('latest', '최근', 'VIDEO_ID'):
        vid = latest_video_id(); print('최근 영상:', vid)
    return vid

def update_meta(vid, ep_path):
    vid = resolve(vid)
    """이미 올린 영상의 제목/설명/태그를 콘티 파일의 youtube 항목으로 교체"""
    ep = json.load(io.open(ep_path, encoding='utf-8-sig'))
    yt = ep.get('youtube', {})
    title = yt.get('title') or ep.get('title') or '오늘의 KBO'
    if '#shorts' not in title.lower() and '#shorts' not in yt.get('description', '').lower(): title = title + ' #Shorts'
    s = service()
    s.videos().update(part='snippet', body={'id': vid, 'snippet': {
        'title': title[:100], 'description': yt.get('description', ''), 'tags': yt.get('tags', []),
        'categoryId': '17', 'defaultLanguage': 'ko'}}).execute()
    print('UPDATED', vid)

def set_thumb(vid, image):
    from googleapiclient.http import MediaFileUpload
    vid = resolve(vid)
    service().thumbnails().set(videoId=vid, media_body=MediaFileUpload(image, mimetype='image/jpeg')).execute()
    print('THUMB', vid, image)

def set_privacy(vid, privacy):
    vid = resolve(vid)
    s = service()
    s.videos().update(part='status', body={'id': vid, 'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False}}).execute()
    print('OK', vid, privacy)

def delete(vid):
    vid = resolve(vid)
    service().videos().delete(id=vid).execute()
    print('DELETED', vid)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: raise SystemExit(__doc__)
    if a[0] == 'auth': service(); print('로그인 완료 (token.json)')
    elif a[0] == 'upload': upload(a[1], a[2], a[3] if len(a) > 3 else 'private')
    elif a[0] == 'update': update_meta(a[1], a[2])
    elif a[0] == 'thumb': set_thumb(a[1], a[2])
    elif a[0] == 'publish': set_privacy(a[1], 'public')
    elif a[0] == 'private': set_privacy(a[1], 'private')
    elif a[0] == 'delete': delete(a[1])
    else: raise SystemExit(__doc__)
