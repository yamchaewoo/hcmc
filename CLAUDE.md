# 한/글(HWP) 매크로 작성 가이드

이 저장소를 읽은 Claude는 **추측 없이** 한/글 COM 매크로를 작성할 수 있습니다.
한/글의 액션 이름과 파라미터는 일반적인 상식으로 맞힐 수 없으므로, **반드시 이 저장소의 사전을 조회한 뒤** 코드를 쓰세요.

## 0. 가장 중요한 규칙

1. **액션 ID를 기억이나 추측으로 쓰지 마세요.** 반드시 `hwp_macro_dict.json`에 있는지 확인하고 쓰세요.
   일반적인 추측(`SelectWord`, `InsertPicture`, `ParaShape` 등)은 실제로 존재하지 않는 ID입니다.
2. **파라미터 이름도 추측하지 마세요.** 액션마다 쓰는 파라미터셋이 정해져 있고, 그 목록이 사전에 있습니다.
3. 사전에 없는 기능이 필요하면, 없는 ID를 지어내지 말고 **사전에서 비슷한 것을 검색해 후보를 제시**하고 사용자에게 확인받으세요.

## 1. 이 저장소의 파일

| 파일 | 내용 |
|---|---|
| `한글매크로_액션사전.md` | 사람이 읽는 3열 표 — **한글 기능명 / 단축키 / 액션ID**. 293개 주요 기능. |
| `hwp_macro_dict.json` | 기계 조회용 전체 사전 — 검증된 액션 **1,807개** + 파라미터셋 **136개**의 인자 목록·자료형. |
| `raw/typelib.json` | 한/글 타입라이브러리 원본 덤프 (266개 타입, 7,956개 멤버). 사전에 없는 속성까지 찾을 때. |
| `tools/` | 이 사전을 만든 추출 파이프라인. 한/글 버전이 바뀌면 다시 돌려 갱신. |

기준 버전: **한글 13.0.0.3379 (한글 2024)**. 액션 ID는 버전 간 대체로 안정적입니다.

## 2. 사전 조회 방법

```bash
# 액션이 존재하는지 + 어떤 파라미터셋을 쓰는지
python -c "import json;d=json.load(open('hwp_macro_dict.json',encoding='utf-8'));print(d['actions'].get('TableCreate'))"
# -> {'actionID': 'TableCreate', 'setID': 'TableCreation', 'paramCount': 15}

# 그 파라미터셋이 받는 인자 전체
python -c "import json;d=json.load(open('hwp_macro_dict.json',encoding='utf-8'));print([p['name'] for p in d['parameterSets']['TableCreation']['params']])"

# 이름으로 액션 검색 (미주 관련 전부)
python -c "import json;d=json.load(open('hwp_macro_dict.json',encoding='utf-8'));print([k for k in d['actions'] if 'Note' in k])"
```

한글 기능명으로 찾을 때는 `한글매크로_액션사전.md`를 grep 하세요.

## 3. 기본 코드 골격

```python
import win32com.client as win32

hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.SetMessageBoxMode(0x00020000)   # 대화상자 자동 처리 (자동화 시 반드시)
hwp.XHwpDocuments.Add(0)            # 새 빈 문서
```

작업이 끝나면 `hwp.Quit()`. 안 하면 `Hwp.exe` 프로세스가 계속 남습니다.

### 패턴 A — 인자가 없는 액션 (`setID` 가 `null`)

```python
hwp.HAction.Run("BreakPara")     # 엔터 (문단 나누기)
hwp.HAction.Run("MoveDocEnd")    # 문서 맨 뒤로
hwp.HAction.Run("CharShapeBold") # 진하게 토글
```

1,807개 중 1,185개가 이 유형입니다.

### 패턴 B — 인자가 있는 액션 (`setID` 가 있음)

**반드시 `GetDefault`로 기본값을 먼저 채운 뒤** 필요한 값만 덮어씁니다.
이 단계를 건너뛰면 나머지 인자가 비어 있어 실패하거나 엉뚱하게 동작합니다.

```python
pset = hwp.HParameterSet.HTableCreation            # H + setID
hwp.HAction.GetDefault("TableCreate", pset.HSet)   # 1) 기본값 채우기
pset.Rows, pset.Cols = 3, 4                        # 2) 원하는 값만 수정
hwp.HAction.Execute("TableCreate", pset.HSet)      # 3) 실행
```

파라미터셋 객체 이름은 **`H` + `setID`** 입니다 (`setID`가 `TableCreation` → `hwp.HParameterSet.HTableCreation`).

### 배열형 인자

`ColWidth` 처럼 배열인 인자는 `CreateItemArray`로 크기를 먼저 잡습니다.

```python
pset.CreateItemArray("ColWidth", 4)
for i in range(4):
    pset.ColWidth.SetItem(i, 5000)
```

## 4. 실수하기 쉬운 지점

| 흔한 오해 | 실제 |
|---|---|
| Enter = 줄바꿈 | Enter는 **문단 나누기** `BreakPara`. 문단을 유지한 줄바꿈은 Shift+Enter `BreakLine` (실측 확인: BreakPara는 문단번호 0→1, BreakLine은 1→1) |
| 액션ID가 `ParaShape` | 액션은 `ParagraphShape`, **파라미터셋 이름**이 `ParaShape` |
| 표 만들기 파라미터셋이 `TableCreate` | 액션은 `TableCreate`, 파라미터셋은 `TableCreation` |
| 낱말 선택은 `SelectWord` | 그런 액션 없음. `MoveWordBegin` → `MoveSelWordEnd` 2단계 |
| 그림 넣기는 `InsertPicture` | 그런 액션 없음. `PictureInsertDialog` |
| 각주/미주 이동이 따로 있음 | 각주·미주 공통으로 `NoteToNext` / `NoteToPrev` |

### 자주 쓰는 값

`HParaShape.AlignType` (문단 정렬) — 실측 확인:

| 값 | 정렬 | 값 | 정렬 |
|---|---|---|---|
| 0 | 양쪽 | 3 | 가운데 |
| 1 | 왼쪽 | 4 | 배분 |
| 2 | 오른쪽 | 5 | 나눔 |

## 5. 자동화할 때 지켜야 할 안전 수칙

이 사전을 만들면서 실제로 겪은 사고들입니다. 그대로 따르세요.

1. **`GetDefault`를 모르는 ID에 마구 호출하지 마세요.**
   일부 액션은 `GetDefault` 단계에서 현재 문맥을 계산하며 **실제 대화상자를 띄웁니다**
   (예: `ComposeCharsEdit`는 응답 없이 멈춤, 개인정보 보호 암호 설정 창이 뜨는 경우도 있었음).

2. **액션 존재 여부는 `CreateAction`으로 확인하세요.** 부작용이 없습니다.

   ```python
   a = hwp.CreateAction("BreakPara")
   if a is not None:          # 없는 ID면 None
       print(a.ActID, a.SetID)  # 정규 표기 + 파라미터셋 이름
       hwp.ReleaseAction(a)
   ```

3. **자동화 전에 `hwp.SetMessageBoxMode(0x00020000)`** 를 호출해 대화상자를 자동 처리하세요.

4. **긴 루프에는 반드시 상한을 두세요.** 특히 `GetText()` 스캔 루프와 `HeadCtrl`/`Next` 개체 순회는
   종료 조건을 잘못 쓰면 무한 루프가 됩니다.

5. 스크립트가 멈추면 `Hwp.exe`가 남습니다. 정리: `taskkill /F /IM Hwp.exe`

## 6. 문서 내용 다루기

```python
hwp.GetPos()          # 커서 위치 (list, para, pos) — 이동 액션 검증에 유용
hwp.PageCount         # 쪽 수
hwp.HeadCtrl          # 개체 연결리스트의 머리. .Next 로 순회, .CtrlID 로 종류 확인
                      #   'tbl'=표, 'en'=미주, 'fn'=각주, 'secd'=구역정의, 'cold'=단정의
```

문자열 입력은 액션으로 합니다.

```python
p = hwp.HParameterSet.HInsertText
hwp.HAction.GetDefault("InsertText", p.HSet)
p.Text = "넣을 내용"
hwp.HAction.Execute("InsertText", p.HSet)
```

## 7. 사전을 갱신해야 할 때

한/글 버전이 바뀌어 액션이 안 맞으면 `tools/`를 순서대로 실행하세요.

```
1_extract_candidates.py  # 한/글 바이너리에서 후보 문자열 추출
1b_filter.py             # 액션ID 형태로 후보 축소
2_validate.py            # CreateAction 으로 전수 검증 (워치독 포함)
3_dump_typelib.py        # 타입라이브러리 덤프
4_build_dict.py          # hwp_macro_dict.json 생성
5_label.py               # 한글 라벨 붙이기 (ID 실존 자동 검증)
6_make_md.py             # 사전 마크다운 생성
7_behavior_test.py       # 라벨이 실제 동작과 맞는지 실측
```

경로가 `C:\Users\SDIJ\PJ2` 로 하드코딩되어 있으니 환경에 맞게 고치세요.
