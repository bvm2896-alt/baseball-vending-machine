# 모션 디자인 효과 사전 — 야구 데이터 영상(HTML/JS 프레임 렌더)용

조사일: 2026-11-01. 출발점: 참고 영상의 9가지 움직임(Ease-in, Ease-out, Spring, Bounce, Stagger, Fade, Slide, Zoom transition, Shared element).

## 0. 읽는 법·공통 단위

- 진행도 `x` (0→1) = (현재 프레임 − 시작 프레임) / 지속 프레임. 곡선 함수 `e(x)`를 거쳐서 값 = 시작 + (끝 − 시작) × e(x).
- 프레임 환산: 30fps에서 1프레임 = 33.3ms(300ms = 9f, 500ms = 15f, 1s = 30f). 60fps에서 1프레임 = 16.7ms.
- **[검증]** 표시는 조사 중에 원문(또는 원문 소스코드)에서 직접 확인한 값이다. **[실무값]** 표시는 출처에 숫자가 없어서 업계에서 흔히 쓰는 값을 넣은 것이다. 영상에 맞춰 조정해서 써야 한다.
- 출처 주의: m3.material.io와 developer.apple.com HIG 본문은 JS 렌더링 페이지라서 직접 읽지 못했다. Material 수치는 같은 토큰을 담은 공식 GitHub 문서(material-components-android Motion.md)에서 확인했다.

### 공통 원칙 (출처 확인함)

| 원칙 | 내용 | 출처 |
|---|---|---|
| 지속 시간 범위 | 대부분 100~500ms다. 단순 피드백은 약 100ms, 큰 화면 변화는 200~300ms, 400ms는 큰 이동에만 쓴다. 500ms부터 "질질 끄는" 느낌이 난다. 너무 짧은 경우보다 너무 긴 경우가 훨씬 흔하다 | https://www.nngroup.com/articles/animation-duration/ |
| 등장 > 퇴장 | 등장 300ms, 퇴장 200~250ms처럼 퇴장을 더 짧게 잡는다. 자주 나오는 동작일수록 짧고 은은하게 한다 | 같은 곳 |
| 등장 = ease-out, 퇴장 = ease-in | 들어올 때는 빠르게 출발해 부드럽게 멈추고, 나갈 때는 가속하며 빠진다 | 같은 곳 / Material Motion.md |
| 이동 거리·면적에 비례 | 움직이는 면적·거리가 클수록 지속 시간을 늘린다 | https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md |
| 데이터 전환은 약 1초 | 데이터 그래픽 전환은 "필요한 만큼, 그 이상은 아니게" 한다. 실험에서는 1.25초(단일), 2초(다단계)를 썼고, 단계별로 약 1초를 권장한다. slow-in/slow-out을 쓴다 | https://homes.cs.washington.edu/~jheer/files/2007-AnimatedTrans-InfoVis.pdf |
| 한 번에 한 가지 (staging) | 복잡한 변화는 단계로 나눈다(예: 축 재조정 → 값 변화). 단계를 지나치게 잘게 나누면 오히려 오류가 늘어서 "적당한 단계화"가 좋다 | 같은 곳 |
| 객체 항상성 (object constancy) | 같은 데이터(같은 팀·선수)는 전환 중에도 같은 도형으로 추적되게 한다(key 함수). 관련 없는 데이터끼리는 크로스페이드나 컷으로 넘긴다 | https://bost.ocks.org/mike/constancy/ |
| 회전보다 이동·확대 | 이동, 확대·축소가 회전보다 따라가기 쉽다. 겹침(occlusion)을 줄이려면 stagger를 쓴다 | Heer & Robertson 2007 |
| 접근성 | 초당 3회 넘게 깜빡이지 않는다(특히 빨강). 패럴랙스·과한 줌은 전정기관 장애가 있는 사람에게 어지럼증을 일으킨다 | https://usability.yale.edu/digital-accessibility/accessibility-resources/accessibility-articles/animated-content-and-timing |
| 동작의 목적 | 상태 전달, 피드백·안내, 경험 강화를 위해서 쓴다(장식만을 위한 동작은 피한다) | https://developer.apple.com/design/human-interface-guidelines/motion (메타 설명만 확인) |

### 토큰 표 (Material 3) [검증]

| 이징 토큰 | cubic-bezier | 용도 |
|---|---|---|
| Emphasized | 경로 `M0,0 C0.05,0 0.133,0.06 0.167,0.4 C0.208,0.82 0.25,1 1,1` | 화면 안에서 시작해 끝나는 주요 동작 |
| Emphasized Decelerate | (0.05, 0.7, 0.1, 1) | 주요 등장 |
| Emphasized Accelerate | (0.3, 0, 0.8, 0.15) | 주요 퇴장 |
| Standard | (0.2, 0, 0, 1) | 보조 동작(화면 안) |
| Standard Decelerate | (0, 0, 0, 1) | 보조 등장 |
| Standard Accelerate | (0.3, 0, 1, 1) | 보조 퇴장 |
| Legacy FastOutSlowIn | (0.4, 0, 0.2, 1) | 구버전 기본 |
| Linear | (0, 0, 1, 1) | 단순·기계적 |

지속 시간 토큰: Short1~4 = 50/100/150/200ms, Medium1~4 = 250/300/350/400ms, Long1~4 = 450/500/550/600ms, ExtraLong1~4 = 700/800/900/1000ms.

스프링 토큰(감쇠비 damping ratio / stiffness): FastSpatial 0.9/1400, FastEffects 1/3800, DefaultSpatial 0.9/700, DefaultEffects 1/1600, SlowSpatial 0.9/300, SlowEffects 1/800. 위치·크기를 움직이는 spatial 스프링은 감쇠비 0.9로 살짝 튀게 하고, 색·투명도를 바꾸는 effects 스프링은 1.0으로 튀지 않게 한다.

---

## 1. 효과 사전 (51개)

형식: 이름(한글/영문) | 어떤 움직임 | 수식·파라미터 | 데이터 영상에서 언제 | 쓰면 안 될 때·주의 | 출처

### A. 곡선(이징)·시간

| # | 이름 | 움직임 | 수식·파라미터 | 언제 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 1 | 이즈 아웃 / Ease-out (Decelerate) | 빠르게 출발해서 부드럽게 멈춤 | easeOutCubic `1-(1-x)^3`, Quart `1-(1-x)^4`, Quint `1-(1-x)^5`. M3 Emphasized Decelerate `cubic-bezier(0.05,0.7,0.1,1)`. 등장 250~400ms(30fps 기준 8~12f) | 모든 등장(카드·숫자·막대)의 기본값 | 퇴장에 쓰면 끝이 굼뜬 느낌이 난다 | https://raw.githubusercontent.com/ai/easings.net/master/src/easings/easingsFunctions.ts , Material Motion.md |
| 2 | 이즈 인 / Ease-in (Accelerate) | 천천히 출발해서 가속하며 빠짐 | easeInCubic `x^3`. M3 Emphasized Accelerate `cubic-bezier(0.3,0,0.8,0.15)`. 퇴장 150~250ms | 화면 밖으로 내보낼 때, 장면을 닫을 때 | 등장에 쓰면 출발이 늦어서 반응이 둔해 보인다(NN/g) | 같은 곳, https://www.nngroup.com/articles/animation-duration/ |
| 3 | 이즈 인-아웃 / Ease-in-out (Standard) | 천천히 출발, 가운데서 빠르게, 천천히 도착 | easeInOutCubic `x<.5 ? 4x³ : 1-(-2x+2)³/2`, easeInOutSine `-(cos(πx)-1)/2`. M3 Standard `(0.2,0,0,1)`. 300~500ms | 화면 안에서 A→B로 옮길 때, 카메라 이동, 순위 재배치 | 너무 길면(>600ms) 늘어진다 | easings.net 소스, Material Motion.md |
| 4 | 선형 / Linear | 같은 속도 | `e(x)=x` | 시간축과 1:1로 맞춰야 하는 것(시즌 진행 선 그리기, 타임라인 진행바, 티커 스크롤, 회전 로딩) | UI 요소 등장에 쓰면 기계적·로봇 같다 | Material Motion.md, https://css-tricks.com/svg-line-animation-works/ |
| 5 | 지수 감속 / Expo-out | 아주 빠르게 거의 다 가고 끝을 오래 끈다 | `x===1 ? 1 : 1-2^(-10x)` | 숫자 카운트업 기본(CountUp.js 기본값), 극적인 줌인 | 끝 30%는 거의 움직이지 않아서 지속 시간을 짧게 잡는다 | easings.net 소스, https://github.com/inorganik/countUp.js |
| 6 | 오버슈트 / Back (easeOutBack) | 목표를 살짝 넘었다가 돌아옴(약 10%) | `c1=1.70158, c3=c1+1; 1 + c3(x-1)^3 + c1(x-1)^2`. InOut은 `c2=c1×1.525`. GSAP `back.out(1.7)` [실무값: 1.7은 GSAP 기본 표기]. 300~500ms | 배지·순위 숫자·VS 아이콘 팝, 강조 카드 | 막대·선처럼 값 자체를 나타내는 도형에 쓰면 실제 값을 넘는 거짓 수치를 잠깐 보여 준다(Heer: 유효한 그래픽 유지) | easings.net 소스 |
| 7 | 스프링 / Spring | 물리 용수철처럼 감쇠하며 정착 | 감쇠 조화 진동: `ω0=√(k/m)`, `ζ=c/(2√(km))`, `ωd=ω0√(1-ζ²)`, `x(t)=1-e^(-ζω0 t)[cos(ωd t)+(ζω0/ωd)sin(ωd t)]`. 값: Motion `stiffness/damping/mass/bounce(-1~1, 0=임계감쇠)/visualDuration`. SwiftUI 기본 `response 0.5s, dampingFraction 0.825`. M3 감쇠비 0.9(spatial)/1.0(effects). [실무값] stiffness 300, damping 30, mass 1 → ζ≈0.87 | 카드 등장, 스코어 버그 확장, 선수 사진 팝 | 지속 시간이 물리값에 따라 정해져서 대사 싱크를 맞추기 어렵다. visualDuration처럼 시간 기준 파라미터를 쓰거나 정착 시점(≈4/(ζω0)초)을 미리 계산한다. 색·투명도에는 ζ=1 | https://motion.dev/docs/react-transitions , https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:).md , Material Motion.md |
| 8 | 엘라스틱 / Elastic | 고무줄처럼 여러 번 출렁이며 정착 | `x=0→0, x=1→1, else 2^(-10x)·sin((10x-0.75)·c4)+1`, `c4=2π/3`. GSAP `elastic.out(amplitude=1, period=0.3)` [실무값]. 600~1000ms | 결론 숫자·"1위" 도장처럼 한 번만 쓰는 강한 강조 | 영상 하나에 1~2번만. 자주 쓰면 가볍고 장난스러워진다. 데이터 도형에는 쓰지 않는다 | easings.net 소스 |
| 9 | 바운스 / Bounce | 바닥에 떨어져 통통 튐 | `n1=7.5625, d1=2.75` 4구간 포물선(easings.net bounceOut). 500~900ms. GSAP CustomBounce `strength, squash` | 공이 떨어지는 연출, 낙하하는 아이콘, 꼴찌 팀이 "툭" 떨어지는 장면 | 물리적 은유가 맞을 때만. 텍스트 블록에 쓰면 읽기 어렵다 | easings.net 소스, https://gsap.com/docs/v3/Eases/ |
| 10 | 계단 / Steps | 중간값 없이 뚝뚝 끊어 바뀜 | CSS `steps(n)`, GSAP `steps(n)`. `e(x)=floor(x·n)/n` | 타이프라이터, 전광판 LED 숫자, 레트로 스코어보드 플립 | 부드러움이 필요한 이동에는 쓰지 않는다 | https://gsap.com/docs/v3/Eases/ |

### B. 등장·퇴장 기본

| # | 이름 | 움직임 | 수식·파라미터 | 언제 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 11 | 페이드 / Fade | 투명도 0↔1 | M3 Fade: 등장 150ms, 퇴장 75ms, Linear [검증: 표의 duration 토큰명과 ms 표기가 일부 어긋나지만 값은 150/75ms]. 영상에서는 [실무값] 200~300ms | 자막·주석·출처 표시, 보조 정보 | 페이드만 쓰면 밋밋하다. 위치 변화(슬라이드 8~20px)와 섞어 쓴다 | Material Motion.md |
| 12 | 슬라이드 / Slide | 한쪽에서 미끄러져 들어옴 | translateX/Y 거리 [실무값] 화면폭의 2~5%(1920 기준 40~100px) + 페이드. ease-out 300~400ms | 리스트 행, 로어서드 텍스트, 다음 항목 | 거리가 크면 지속 시간도 늘린다. 방향은 의미(다음=오른쪽→왼쪽)와 맞춘다 | NN/g, Material Motion.md |
| 13 | 스케일 팝 / Scale pop-in | 작게 있다가 커지며 나타남 | scale 0.6~0.85→1 + opacity 0→1, easeOutBack 또는 스프링(ζ≈0.6~0.8). 250~400ms | 배지, 아이콘, 순위 번호, "NEW" 태그 | 큰 면적(전체 카드)은 0.92→1처럼 작게만 키운다 | IxDF(Exaggeration), easings.net |
| 14 | 순차 등장 / Stagger | 여러 요소가 시차를 두고 차례로 | GSAP `stagger:{each:0.05~0.1 | amount:총시간, from:"start/center/end/edges/random/인덱스", grid:[행,열], ease}`. Motion `stagger(0.1,{from:"last"})`. [실무값] 항목 간격 40~80ms, 전체 stagger 합계 ≤ 600ms | 순위표 10행, 막대 묶음, 스탯 카드 그리드 | 항목이 많으면(>10) `amount`로 총시간을 고정한다. 간격이 길면 느려 보인다 | https://gsap.com/docs/v3/Staggers/ , motion.dev |
| 15 | 블러 인 / Blur-in (Focus pull) | 흐릿하다가 초점이 맞음 | filter blur 8~16px→0 + opacity, ease-out 300~500ms [실무값] | 오프닝 타이틀, 선수 사진 등장 | 렌더 비용이 크다(프레임 렌더에서는 느려진다). 텍스트 본문에는 쓰지 않는다 | 실무 관행(검증 출처 없음) |

### C. 장면 전환

| # | 이름 | 움직임 | 수식·파라미터 | 언제 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 16 | 확대 전환 / Zoom transition (Shared axis Z) | 앞 화면이 커지며 사라지고 다음 화면이 작은 데서 커지며 나타남(깊이 이동) | M3 Shared axis Z 300ms, Standard 이징. [실무값] 나가는 화면 scale 1→1.1 + fade out, 들어오는 화면 0.8→1 + fade in | 상위→하위(리그 전체→팀 상세), 챕터 진입 | 무관한 장면끼리는 페이드 스루를 쓴다. 과한 줌은 어지럼증 유발 | Material Motion.md, Yale 접근성 |
| 17 | 공유 축 X/Y / Shared axis | 같은 방향으로 함께 밀리며 넘어감 | M3 300ms. [실무값] 나가는 화면 x 0→−30px + fade, 들어오는 화면 +30→0 + fade | 1→2→3단계 설명, 1위→2위 넘기기, 시즌→다음 시즌 | 방향이 시간·순서 의미와 어긋나면 혼란스럽다 | Material Motion.md |
| 18 | 페이드 스루 / Fade through | 앞 화면이 먼저 사라지고, 다음 화면이 약간 커지며 나타남 | M3 300ms. [실무값, 구 M2 사양 기억] 처음 약 30% 구간에 퇴장, 나머지 구간에 등장, 들어오는 화면 scale 0.92→1 | 서로 관계없는 주제 전환(타자 얘기→투수 얘기) | 공간 관계가 있는 장면에는 shared axis가 낫다 | Material Motion.md |
| 19 | 컨테이너 트랜스폼 / Container transform | 카드 한 장이 커져서 전체 화면 상세가 됨 | M3 등장 300ms, 퇴장 250ms, FastOutSlowIn `(0.4,0,0.2,1)` | 순위표의 한 행 → 그 팀 상세 카드, 선수 카드 → 기록 전체 | 확장 중 내용이 늘어나 보이지 않게 내부는 크로스페이드한다 | Material Motion.md |
| 20 | 공유 요소 전환 / Shared element (FLIP, Magic Move) | 두 장면에 같은 요소(선수 얼굴·팀 로고)가 위치·크기만 바꿔 이어짐 | FLIP: First(시작 rect) → Last(끝 rect) → Invert(transform으로 시작 상태 흉내) → Play(transform을 0으로). 아핀 보간: `x=lerp(x0,x1,e)`, `s=lerp(w0/w1,1,e)`. 400~600ms ease-in-out | 선수 소개 사진이 다음 비교 화면 왼쪽 칸으로 이동, 로고가 스코어 버그로 들어감 | 비율이 다른 요소를 scale하면 찌그러진다. 텍스트는 분리해서 페이드한다 | https://aerotwist.com/blog/flip-your-animations/ |
| 21 | 마스크 리빌·와이프 / Mask reveal, Wipe | 가려진 경계선이 움직이며 드러남 | `clip-path: inset(0 100% 0 0) → inset(0 0 0 0)`(왼→오), `circle(0% at x y)→circle(150%)`(원형 아이리스). 같은 도형 함수끼리만 보간된다. 300~600ms ease-in-out | 표·그래프 드러내기, 사진 공개, 챕터 전환 | polygon끼리는 꼭짓점 수가 같아야 한다. 다른 도형 함수끼리는 보간되지 않는다 | https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path |
| 22 | 스팅어 / Stinger transition | 브랜드 그래픽이 화면을 덮었다가 걷히며 다음 장면 | [실무값] 총 0.8~1.2초, 덮개가 화면을 완전히 가린 프레임(대략 중간)에서 장면을 컷. 덮기는 ease-in, 걷기는 ease-out | 롱폼 챕터 구분, 쇼츠 루프 연결 | 자주 쓰면 지루하다. 챕터당 1회 | https://www.newscaststudio.com/2022/04/11/apple-tv-friday-night-baseball/2/ |
| 23 | 리플레이 와이프 / Replay(logo) wipe | 로고가 화면에 떴다가 작아지고 박스형 와이프로 영상을 드러냄 | Apple TV MLB 예: 파란 그래픽+로고 → 로고 축소 → 박스형 와이프로 리빌 → 로고가 좌하단으로 이동. [실무값] 0.6~1초 | "다시 보기", 명장면 회상, 과거 시즌으로 이동 | 리플레이가 아닌 장면에 쓰면 의미가 섞인다 | 같은 곳 |
| 24 | 크로스페이드·컷 / Cross-fade, Cut | 두 장면을 겹쳐 바꾸거나 바로 자름 | 크로스페이드 200~400ms linear/standard. 컷은 0프레임 | 관련 없는 데이터셋·차원으로 바꿀 때 | 같은 대상을 계속 따라가는 장면에서는 객체 항상성이 깨지므로 모프·재배치를 쓴다 | https://bost.ocks.org/mike/constancy/ |

### D. 데이터 특화

| # | 이름 | 움직임 | 수식·파라미터 | 언제 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 25 | 숫자 카운트업 / Count-up | 0(또는 이전 값)에서 목표 숫자까지 올라감 | CountUp.js 기본: duration 2s, easeOutExpo, smartEasingThreshold 999, smartEasingAmount 333(큰 수는 마지막 333 구간만 감속), decimalPlaces 0, separator ",". 표시값 `round(v0+(v1-v0)·e(x), 소수자리)`. 자리수 흔들림을 막으려면 tabular-nums(고정폭 숫자) 사용 | 타율·홈런 수·관중 수·연봉 공개 | 소수 3자리 타율은 마지막 자리까지 정확히 멈춰야 한다(끝 프레임에 목표값을 강제). 비례 폭 폰트는 글자가 좌우로 떨린다 | https://github.com/inorganik/countUp.js |
| 26 | 오도미터·롤링 숫자 / Odometer roll | 자리마다 숫자 띠가 위아래로 굴러 바뀜 | 각 자리 열을 `translateY(-digit × 글자높이)`로 이동. 오른쪽(1의 자리)부터 stagger 30~60ms, ease-out 400~800ms [실무값]. 0~9 띠를 2바퀴 이어 붙이면 9→0도 자연스럽다 | 순위 숫자 바뀜, 스코어 변경, 누적 기록 갱신 | 자리수가 늘어나는 경우(99→100)는 새 자리를 페이드인으로 처리 | https://github.com/HubSpot/odometer (라이브러리 존재 확인. 원리는 실무 기법) |
| 27 | 막대 성장 / Bar grow | 막대가 기준선에서 값 길이까지 자람 | `scaleY(0→1)` + transform-origin을 기준선(아래/왼쪽)에. ease-out 400~700ms, 막대 간 stagger 50~80ms [실무값]. 값 라벨은 막대 끝을 따라가거나 성장 후에 카운트업 | 팀별 홈런, 기록 비교 | 오버슈트(back·elastic)는 쓰지 않는다(값 왜곡). 축 눈금은 성장 전에 먼저 보여 준다 | Heer & Robertson 2007(유효 그래픽 유지) |
| 28 | 선 그리기 / Line draw (stroke-dashoffset) | 선이 펜으로 그리듯 처음부터 끝까지 그려짐 | `L=path.getTotalLength()`, `stroke-dasharray:L; stroke-dashoffset:L→0`. 시간축 그래프는 linear, 장식 선은 ease-in-out. `pathLength="1"`이면 L=1로 고정 | 시즌 승률 추이, 누적 홈런 곡선, 타구 궤적 | 끝점 마커·라벨은 선 끝 위치(`getPointAtLength`)에 붙여 같이 이동 | https://css-tricks.com/svg-line-animation-works/ |
| 29 | 원형 게이지 / Radial gauge, Ring fill | 원호가 0%에서 값%까지 채워짐 | 원둘레 `C=2πr`, `dasharray=C`, `dashoffset=C×(1−p)`. 시작점은 12시(−90° 회전). ease-out 600~1000ms + 가운데 퍼센트 카운트업 동기화 | 승리 확률, 출루율, 진행률 | 사람은 각도 비교를 길이 비교보다 못한다. 정밀 비교는 막대로 하고 게이지는 한 값 강조에만 | css-tricks(같은 원리), Heer 2007 |
| 30 | 순위 재정렬 / Rank reorder (Bar race swap) | 순위가 바뀐 행·막대가 위아래로 자리를 바꿈 | 키(팀명)로 짝지어 y만 보간(객체 항상성). Flourish 예시: 막대 교차 0.5s. 들어오는 항목은 페이드인, 나가는 항목은 페이드아웃(enter/exit). ease-in-out | 주간 순위 변동, 시즌 중 순위 레이스 | 키 없이 인덱스로 짝지으면 엉뚱한 막대가 늘고 줄어 오해를 부른다 | https://bost.ocks.org/mike/constancy/ , https://helpcenter.flourish.studio/hc/en-us/articles/8761522984207 |
| 31 | 단계적 전환 / Staged transition | 복잡한 변화를 "축→값→라벨" 같은 단계로 나눠 차례로 | 단계별 약 1s, slow-in/slow-out. 예: 산점도→막대는 ① x로 정렬 ② 막대로 모프. 스태거로 겹침 감소 | 그래프 종류 변경, 축 스케일 변경(정규시즌→포스트시즌) | 3단계 넘게 쪼개면 오히려 오류가 늘고 선호도도 낮다 | Heer & Robertson 2007 |
| 32 | 하이라이트 & 디밍 / Highlight & dim (Focus+context) | 주인공 요소만 밝게, 나머지는 흐리게 | 비주목 요소 opacity 1→0.25~0.35, 채도↓. 주목 요소는 테두리·색 강조 또는 scale 1.03. 250~400ms [실무값] | 10팀 중 한 팀 짚기, 그래프에서 한 시점 강조 | 흐리게 한 요소도 읽을 수는 있어야 한다(맥락 유지) | https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design (Staging) |
| 33 | 줌-투-디테일 / Zoom to detail (Camera push) | 가상 카메라가 그래프의 특정 구간으로 확대해 들어감 | 카메라 transform `scale 1→2~3`, translate로 목표 중심 맞춤. ease-in-out 600~1000ms. 확대 후 그 구간 라벨을 등장 | 그래프 특정 경기·이닝 짚기, 표의 한 칸 | 확대 중에는 다른 변화를 동시에 주지 않는다(한 번에 한 가지). 과한 줌·반복 줌은 어지럼증 | Heer 2007, Yale 접근성 |
| 34 | 모프 / Morph (Shape tween) | 한 도형이 다른 도형으로 변형 | flubber `interpolate(pathA,pathB,{maxSegmentLength:10})` → `t(0~1)`마다 path. 400~800ms ease-in-out | 원형 게이지→막대, 공 아이콘→점, 숫자 박스→차트 | 구멍·여러 조각이 있는 도형은 첫 외곽선만 보간된다. 의미가 다른 데이터끼리 모프하면 오해를 부른다 | https://github.com/veltman/flubber |
| 35 | 진입·갱신·퇴장 / Enter–Update–Exit | 새 데이터는 나타나고, 유지되는 데이터는 이동하고, 빠지는 데이터는 사라짐 | 갱신: 위치·크기 보간. 진입: fade/scale-in. 퇴장: fade-out(진입보다 짧게). D3 key 조인 | 필터 변경(전체→좌타자만), 시즌 교체 | 세 가지를 동시에 하면 복잡하다. 퇴장 → 갱신 → 진입 순서로 단계화할 수 있다 | https://bost.ocks.org/mike/constancy/ |

### E. 텍스트·강조·캐릭터성(디즈니 원칙)

| # | 이름 | 움직임 | 수식·파라미터 | 언제 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 36 | 타이프라이터 / Typewriter | 글자가 한 자씩 찍힘 | `보이는 글자수 = floor(x × N)`(steps). [실무값] 한글 12~20자/초, 커서 깜빡임 약 1Hz | 질문 던지기("과연 1위는?"), 데이터 출처·조건문 | 긴 문장은 너무 느리다(20자 넘으면 다른 방법). 대사 속도와 맞춘다 | GSAP steps |
| 37 | 텍스트 분할 등장 / Split text reveal | 글자·단어·줄 단위로 나눠 순차 등장 | GSAP SplitText 예: `y:100, autoAlpha:0, stagger:0.05, duration:1`. 줄 단위는 `yPercent:20`. `mask:"lines"`로 줄마다 클리핑해서 아래에서 솟아오르게 | 챕터 제목, 결론 한 줄, 쇼츠 훅 문장 | 글자 단위로 쪼개면 줄바꿈이 깨질 수 있어 단어·줄 단위를 같이 쓴다. 한글은 단어(어절) 단위가 더 읽힌다 | https://gsap.com/docs/v3/Plugins/SplitText/ |
| 38 | 하이라이트 스윕·광택 / Shine sweep | 비스듬한 빛 띠가 표면을 훑고 지나감 | 의사요소에 `linear-gradient(105deg, transparent 40%, rgba(255,255,255,.6) 50%, transparent 60%)`, `skewX(-20deg)`, `translateX(-120%→220%)`. 600~900ms ease-in-out, 한 번만 [실무값] | 1위 카드, 기록 경신 배지, 썸네일풍 타이틀 | 반복 루프는 산만하다. 정보가 아닌 장식이라 1~2회만 | https://smashingmagazine.com/2023/07/shines-perspective-rotations-css-3d-effects-images |
| 39 | 형광펜 밑줄 / Marker underline | 강조 단어 아래로 색 띠가 왼→오로 그어짐 | `scaleX(0→1)`, transform-origin left, ease-out 300~450ms, 단어 등장 후 100~200ms 지연 [실무값] | 대사의 핵심 숫자·키워드 강조 | 한 화면에 1~2개만 | 실무 관행(마스크 리빌 #21 변형) |
| 40 | 펄스 / Pulse | 살짝 커졌다 돌아오기 반복(심장 박동) | `scale = 1 + A·sin²(πt/T)`, A 0.04~0.08, T 0.6~1.0s, 2~3회 [실무값]. 글로우 펄스는 box-shadow 반경 | 지금 진행 중인 값, 클릭 유도(구독), "주목" | 초당 3회 넘는 깜빡임은 금지(광과민). 끝없는 펄스는 시선을 뺏는다 | Yale 접근성 |
| 41 | 흔들림 / Shake (Trauma shake) | 화면이나 요소가 덜덜 떨림 | Trauma 모델: `trauma -= decay(0.8/s)·dt`, `amount = trauma^2`(또는 ^3), `offset = maxOffset(예: 100,75px) × amount × noise(t)`, `roll = maxRoll(0.1rad) × amount × noise`. 랜덤 대신 노이즈(period 4, octaves 2)를 써서 부드럽게. UI 요소의 "부정" 흔들림은 [실무값] x ±6~10px, 3~4회, 300~400ms | 오류·부정 수치(블론세이브, 실책), 충격 반전 | 화면 전체 흔들림은 짧고 드물게. 회전(roll)은 아껴 쓴다. 텍스트를 읽어야 할 때는 금지 | https://kidscancode.org/godot_recipes/3.x/2d/screen_shake/ |
| 42 | 예비동작 / Anticipation | 본 동작 전에 반대 방향으로 살짝 움츠림 | [실무값] 본 동작 직전 80~150ms 동안 scale 0.95 또는 반대 방향 4~8px, 그 뒤 본 동작. easeInBack `c3x³ − c1x²`가 곡선 하나로 같은 효과 | 큰 숫자 공개 직전, 카드 날아가기 직전 | 반복 동작에 넣으면 답답하다 | IxDF(Anticipation), easings.net(easeInBack) |
| 43 | 후속·겹침 동작 / Follow-through & Overlapping | 주 요소가 먼저 멈추고 딸린 요소가 조금 늦게 따라와 멈춤 | 이미지 → 제목 → 설명 순으로 지연 [실무값] 60~120ms, 후행 요소는 약한 스프링(ζ 0.7~0.8) | 선수 카드(사진 → 이름 → 기록), 로어서드 | 지연이 길면 따로 노는 것처럼 보인다 | IxDF(Follow-through) |
| 44 | 스쿼시 & 스트레치 / Squash & stretch | 충돌·가속 때 찌그러지고 늘어남(부피 보존) | `scaleY = s`, `scaleX = 1/s`(부피 보존). 착지 프레임 s≈0.85, 비행 중 s≈1.1 [실무값] | 공 튀기기, 버튼·배지 착지 | 텍스트·로고·사진에는 쓰지 않는다(브랜드 왜곡) | IxDF(Squash & stretch) |
| 45 | 패럴랙스 / Parallax | 앞뒤 레이어가 다른 속도로 움직여 깊이감 | 레이어별 이동 = 카메라 이동 × 계수(배경 0.2, 중경 0.5, 전경 1.0) [실무값] | 오프닝·선수 소개 배경(구장 사진 + 선수 누끼) | 전정기관 장애 유발 요인 1순위. 짧게, 작은 이동량으로 | Yale 접근성 |
| 46 | 아크 이동 / Arcs | 직선이 아닌 곡선 경로로 이동 | 2차 베지어 `P(t)=(1-t)²P0 + 2(1-t)tP1 + t²P2`, 속도는 ease-in-out. 포물선(타구)은 `y = v0y·t − ½g t²` | 타구·송구 궤적, 아이콘이 다른 자리로 날아감 | 정보 UI의 단순 이동은 직선이 더 예측 가능하다 | IxDF(Arc) |
| 47 | 2차 동작 / Secondary action | 주 동작을 보조하는 작은 효과 | 예: 결론 등장 후 컨페티·스파크 파티클 0.6~1.2s, 중력 감속 [실무값] | 우승·신기록 결론, 쇼츠 마지막 펀치 | 남발하면 싸 보인다. 주 동작이 끝난 뒤에 | IxDF(Secondary action) |

### F. 스포츠 중계 그래픽

| # | 이름 | 움직임 | 수식·파라미터 | 언제 | 주의 | 출처 |
|---|---|---|---|---|---|---|
| 48 | 스코어 버그 갱신 / Score bug update | 상시 점수판이 잠깐 늘어나거나 슬라이드해서 정보를 보여 준 뒤 기본 상태로 복귀 | 확장: 폭 스프링(ζ≈0.9) 300~400ms → 정보 2~4s 유지 → 축소 250ms [실무값]. 점수 숫자는 오도미터(#26) | 롱폼 상단의 "현재 다루는 팀·시즌·장면 번호" 상시 표시 | 1순위 정보(점수·시간)는 절대 가리지 않는다. 장식 최소화, 작은 화면(폰)에서 읽히는지 확인 | https://www.sportsvideo.org/2026/06/09/designing-the-modern-scorebug-how-broadcast-graphics-teams-are-rethinking-the-most-important-element-on-screen/ |
| 49 | 로어서드 / Lower third | 화면 아래 1/3에 이름·소속 띠 | [실무값] 색 띠 scaleX 0→1(왼쪽 기준) 300ms ease-out → 텍스트 슬라이드·마스크 리빌 +100ms → 유지 4~6s → 퇴장은 역순으로 200ms ease-in | 선수·감독 소개, 인용 출처 | 쇼츠(9:16)에서는 자막 위치와 충돌하지 않게 | sportsvideo.org(위계), NN/g(등장>퇴장) |
| 50 | 스탯 바 와이프 / Head-to-head stat bars | 가운데 축에서 좌우로 두 선수 막대가 동시에 뻗음 | 가운데 기준 좌측 scaleX(origin right), 우측 scaleX(origin left). 500~700ms ease-out, 항목 간 stagger 80~120ms, 더 높은 쪽 값은 끝나고 하이라이트(#32) | A vs B 선수·팀 기록 비교 | 항목마다 단위·스케일이 다르면 막대 길이를 항목 안에서만 정규화하고 그 사실을 표시 | Heer 2007(유효 그래픽), 실무 관행 |
| 51 | 매치업 카드 / Matchup card (VS) | 두 패널이 양쪽에서 미끄러져 들어와 가운데서 만나고 VS가 팝 | 좌·우 패널 translateX ±화면폭 50%→0, ease-out 400~500ms(동시 또는 50ms 차이) → 충돌 프레임에 미세 흔들림(#41, 2~4px) → VS 스케일 팝(#13, easeOutBack) | 맞대결 예고, 투수 vs 타자 | 정보 카드보다 연출용이다. 한 편에 1회 | 실무 관행(중계 패키지 일반) |

---

## 2. 야구 데이터 영상 장면별 추천

| 장면 | 1순위 조합 | 파라미터 요약 | 피할 것 |
|---|---|---|---|
| 쇼츠 첫 1초(훅) | 텍스트 분할 등장(#37, 어절·mask) + 스케일 팝 숫자(#13) | 어절 stagger 50ms, 전체 ≤ 500ms(15f@30fps), easeOutBack | 페이드만 쓰는 느린 시작, 0.5초 넘는 빈 화면 |
| 순위 공개(10위→1위 카운트다운) | 행 슬라이드+페이드(#12) → 순위 숫자 오도미터(#26) → 1위만 하이라이트 & 디밍(#32)+광택 스윕(#38) | 행 ease-out 350ms, 행 간 stagger 60ms(또는 대사 박자에 맞춰 1행씩), 1위 공개 직전 예비동작(#42) 120ms | 모든 행에 엘라스틱·광택(강조가 사라짐) |
| 순위 변동(지난주→이번주) | 순위 재정렬(#30)+진입·퇴장(#35) | 키=팀명, y 보간 500~700ms ease-in-out, 상승 팀 초록 ▲·하락 팀 빨강 ▼ 페이드 | 인덱스 기준 보간, 한 번에 색·위치·크기 동시 변경 |
| 기록 비교(A vs B) | 매치업 카드(#51) → 스탯 바 와이프(#50) → 승자 값 하이라이트(#32) | 패널 450ms, 막대 600ms, 항목 stagger 100ms, 숫자 카운트업 막대와 동기화 | 막대에 back/elastic 오버슈트(값 왜곡) |
| 시즌 추이·기록 흐름 | 선 그리기(#28, linear) + 끝점 마커 추적 + 줌-투-디테일(#33) | 선 1.5~3s(대사 길이에 맞춤), 줌 800ms ease-in-out, 줌 후 라벨 페이드 | 줌과 선 그리기를 동시에 |
| 확률 계산(승리 확률·기대값) | 원형 게이지(#29) 또는 막대 성장(#27) + 숫자 카운트업(#25) + 수식 단계 등장(#31 staged) | 게이지 800ms ease-out, 카운트업 같은 시간·같은 곡선, 수식 항목마다 1초 단계 | 정밀 비교를 게이지로, 소수점 마지막 자리가 목표와 다르게 멈춤 |
| 선수 소개 | 블러/마스크 리빌 사진(#15/#21) + 후속동작(#43: 사진→이름→기록) + 로어서드(#49) + 약한 패럴랙스(#45) | 사진 400ms, 이름 +100ms, 기록 +200ms, 패럴랙스 계수 0.2/1.0, 이동량 작게 | 사진에 스쿼시, 긴 패럴랙스 |
| 장면 전환(관련 있음: 리그→팀) | 컨테이너 트랜스폼(#19) / 공유 요소(#20) / 확대 전환(#16) | 300~500ms, 등장 > 퇴장, ease-in-out | 매번 다른 전환(일관성 붕괴) |
| 장면 전환(관련 없음: 주제 바뀜) | 페이드 스루(#18) 또는 크로스페이드·컷(#24) | 300ms, 들어오는 화면 0.92→1 | 공간 이동 연출(관계가 있다고 오해) |
| 챕터 구분(롱폼) | 스팅어(#22) 또는 마스크 와이프(#21) + 챕터 제목 split text(#37) | 0.8~1.2s, 완전히 덮인 프레임에서 컷 | 챕터마다 1회 넘게 쓰기 |
| 과거 장면 회상·"다시 보기" | 리플레이 와이프(#23) | 로고 등장 → 축소 → 박스 와이프 0.6~1s | 리플레이가 아닌 곳에 같은 와이프 |
| 결론 강조 | 텍스트 분할 등장(#37) + 핵심 숫자 엘라스틱 또는 스프링 팝(#8/#7) + 형광펜 밑줄(#39) + 2차 동작(#47) | 엘라스틱 800ms 한 번, 밑줄 +150ms, 파티클 1s | 결론 전 장면에서 같은 효과를 이미 많이 쓰기(대비가 사라짐) |
| 경고·부정 수치(실책·블론·최하위) | 흔들림(#41, UI 요소 단위) + 빨강 펄스 1~2회(#40) + 바운스로 "툭" 떨어짐(#9) | x ±8px 3회 350ms, 펄스 T 0.8s 2회, 초당 3회 미만 | 화면 전체를 길게 흔들기, 빨강 빠른 점멸(광과민) |
| 출처·조건·각주 | 페이드(#11) + 작은 슬라이드(#12), 또는 타이프라이터(#36) | 200~300ms, 이동 8~12px | 큰 모션(본문보다 눈에 띔) |
| 상시 정보(지금 어느 팀·시즌) | 스코어 버그(#48) | 확장 350ms 스프링 ζ0.9, 2~4s 유지, 축소 250ms | 핵심 데이터 위를 가리기 |
| 타구·투구 궤적 | 아크 이동(#46) + 선 그리기(#28) + 착지 스쿼시(#44, 공 아이콘만) | 포물선 실제 비율, 0.8~1.5s | UI 텍스트에 아크·스쿼시 |
| 구독·CTA 마무리 | 스케일 팝(#13) + 펄스 2회(#40) | back 350ms, 펄스 A 0.05 | 끝없는 루프 펄스 |

---

## 3. 프레임 렌더용 최소 코드 조각 (참고)

```js
// x: 0~1 진행도. 출처: easings.net 소스(위 URL)
const c1 = 1.70158, c2 = c1 * 1.525, c3 = c1 + 1, c4 = (2 * Math.PI) / 3;
const E = {
  linear: x => x,
  outCubic: x => 1 - Math.pow(1 - x, 3),
  inCubic: x => x * x * x,
  inOutCubic: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
  outExpo: x => x === 1 ? 1 : 1 - Math.pow(2, -10 * x),
  outBack: x => 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2),
  inBack: x => c3 * x * x * x - c1 * x * x,
  outElastic: x => x === 0 ? 0 : x === 1 ? 1 : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * c4) + 1,
  outBounce: x => { const n1 = 7.5625, d1 = 2.75;
    if (x < 1 / d1) return n1 * x * x;
    if (x < 2 / d1) return n1 * (x -= 1.5 / d1) * x + .75;
    if (x < 2.5 / d1) return n1 * (x -= 2.25 / d1) * x + .9375;
    return n1 * (x -= 2.625 / d1) * x + .984375; },
};
// 감쇠 스프링(0→1), t초. k=stiffness, c=damping, m=mass
function spring(t, k = 300, c = 30, m = 1) {
  const w0 = Math.sqrt(k / m), z = c / (2 * Math.sqrt(k * m));
  if (z >= 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);           // 임계감쇠 근사
  const wd = w0 * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w0 * t) * (Math.cos(wd * t) + (z * w0 / wd) * Math.sin(wd * t));
}
// 정착 시간 근사 ≈ 4 / (z*w0) 초 → 대사 싱크용 프레임 계산에 사용
const prog = (f, start, dur) => Math.min(1, Math.max(0, (f - start) / dur)); // 프레임→진행도
```

## 4. 출처 목록

- Material Components Android, Motion 문서(M3 이징·지속 시간·스프링 토큰, 전환 패턴): https://github.com/material-components/material-components-android/blob/master/docs/theming/Motion.md
- easings.net 이징 함수 소스: https://raw.githubusercontent.com/ai/easings.net/master/src/easings/easingsFunctions.ts (사이트 https://easings.net/)
- GSAP Staggers: https://gsap.com/docs/v3/Staggers/ · GSAP Eases: https://gsap.com/docs/v3/Eases/ · GSAP SplitText: https://gsap.com/docs/v3/Plugins/SplitText/
- Motion(구 Framer Motion) transitions(spring·stagger): https://motion.dev/docs/react-transitions
- SwiftUI spring 기본값: https://developer.apple.com/documentation/swiftui/animation/spring(response:dampingfraction:blendduration:).md
- Apple HIG Motion(메타 설명만 확인): https://developer.apple.com/design/human-interface-guidelines/motion
- NN/g 애니메이션 지속 시간: https://www.nngroup.com/articles/animation-duration/
- Heer & Robertson 2007, Animated Transitions in Statistical Data Graphics: https://homes.cs.washington.edu/~jheer/files/2007-AnimatedTrans-InfoVis.pdf · https://idl.uw.edu/papers/animated-transitions
- Mike Bostock, Object Constancy: https://bost.ocks.org/mike/constancy/
- CSS-Tricks, SVG 선 그리기: https://css-tricks.com/svg-line-animation-works/
- MDN clip-path: https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path
- Paul Lewis, FLIP: https://aerotwist.com/blog/flip-your-animations/
- IxDF, 디즈니 12원칙의 UI 적용: https://ixdf.org/literature/article/ui-animation-how-to-apply-disney-s-12-principles-of-animation-to-ui-design
- CountUp.js: https://github.com/inorganik/countUp.js · flubber: https://github.com/veltman/flubber · HubSpot Odometer: https://github.com/HubSpot/odometer
- KidsCanCode 트라우마 셰이크: https://kidscancode.org/godot_recipes/3.x/2d/screen_shake/
- Flourish 바 차트 레이스 속도: https://helpcenter.flourish.studio/hc/en-us/articles/8761522984207-How-to-change-the-animation-speed-of-your-bar-chart-race
- Yale 접근성(깜빡임·전정기관): https://usability.yale.edu/digital-accessibility/accessibility-resources/accessibility-articles/animated-content-and-timing
- SVG(Sports Video Group), 현대 스코어 버그 디자인(2026-06): https://www.sportsvideo.org/2026/06/09/designing-the-modern-scorebug-how-broadcast-graphics-teams-are-rethinking-the-most-important-element-on-screen/
- NewscastStudio, Apple TV+ Friday Night Baseball 그래픽: https://www.newscaststudio.com/2022/04/11/apple-tv-friday-night-baseball/2/
- Smashing Magazine, 광택(shine) 효과: https://smashingmagazine.com/2023/07/shines-perspective-rotations-css-3d-effects-images
