# -*- coding: utf-8 -*-
"""labels.json -> 보기 좋은 마크다운 사전 생성."""
import json, os, sys
from collections import OrderedDict
sys.stdout.reconfigure(encoding="utf-8")

BASE = r"C:\Users\SDIJ\PJ2"
labels = json.load(open(os.path.join(BASE, "raw", "labels.json"), encoding="utf-8"))
dic = json.load(open(os.path.join(BASE, "hwp_macro_dict.json"), encoding="utf-8"))
ACT, PSET = dic["actions"], dic["parameterSets"]

groups = OrderedDict()
for r in labels:
    groups.setdefault(r["분류"], []).append(r)

L = []
w = L.append
w("# 한/글 매크로 액션 사전")
w("")
w(f"한글 **{dic['_meta']['한글버전']}** 기준. 기능 **{len(labels)}개** 라벨링 / "
  f"전체 검증된 액션 **{len(ACT):,}개** / 파라미터셋 **{len(PSET)}개**.")
w("")
w("> 이 표의 액션ID는 전부 설치된 한/글에 `CreateAction()`으로 물어봐서 **실존이 확인된 것만** 넣었습니다. "
  "추측으로 적은 ID는 없습니다. 한글 기능명과 단축키는 한/글 공식 도움말의 단축키표를 따랐습니다.")
w("")
w("## 쓰는 법")
w("")
w("```python")
w('import win32com.client as win32')
w('hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")')
w('hwp.XHwpDocuments.Add(0)')
w("")
w("# 1) 인자가 없는 액션 -> Run 한 줄이면 끝")
w('hwp.HAction.Run("BreakPara")      # 엔터 (문단 나누기)')
w('hwp.HAction.Run("MoveDocEnd")     # 문서 맨 뒤로')
w("")
w("# 2) 인자가 있는 액션 -> 파라미터셋을 채워서 Execute")
w('pset = hwp.HParameterSet.HTableCreation          # 표 만들기의 파라미터셋')
w('hwp.HAction.GetDefault("TableCreate", pset.HSet) # 기본값 먼저 채우고')
w('pset.Rows, pset.Cols = 3, 4                      # 원하는 값만 덮어쓰기')
w('hwp.HAction.Execute("TableCreate", pset.HSet)')
w("```")
w("")
w("어떤 액션이 인자를 받는지, 받는다면 어떤 파라미터셋인지는 `hwp_macro_dict.json`에 전부 들어 있습니다.")
w("")
w("### 헷갈리기 쉬운 것")
w("")
w("| 흔한 오해 | 실제 |")
w("|---|---|")
w("| Enter = 줄바꿈 | Enter는 **문단 나누기** `BreakPara`. 진짜 줄바꿈(문단 유지)은 **Shift+Enter** `BreakLine` |")
w("| 문단 모양 = `ParaShape` | 액션ID는 `ParagraphShape`, 파라미터셋 이름이 `ParaShape` |")
w("| 표 만들기 파라미터셋 = `TableCreate` | 액션은 `TableCreate`, 파라미터셋은 `TableCreation` |")
w("")
w("### 실측 검증 결과")
w("")
w("아래 항목은 라벨이 맞는지 실제로 한/글을 띄워 실행해보고 결과를 확인한 것입니다.")
w("")
w("| 검증 항목 | 근거 |")
w("|---|---|")
for label, detail in [
    ("`BreakPara` = 문단 나누기(Enter)", "문단번호 0 → 1"),
    ("`BreakLine` = 줄 나누기(Shift+Enter)", "문단번호 1 → 1 (문단 유지됨)"),
    ("`BreakPage` = 쪽 나누기(Ctrl+Enter)", "쪽수 1 → 2"),
    ("`MoveDocBegin` / `MoveDocEnd`", "커서 (0,0,16) → (0,2,4)"),
    ("`MoveLineBegin` / `MoveLineEnd`", "커서 (0,2,0) → (0,2,4)"),
    ("`CharShapeBold` = 진하게", "CharShape.Bold 0 → 1"),
    ("`ParagraphShapeAlign*` = 정렬 6종", "AlignType 0→3→2→1→0→4→5 전부 반응"),
    ("`InsertEndnote` = 미주 넣기", "개체목록에 `en`(미주) 생성"),
    ("`TableCreate` = 표 만들기", "개체목록에 `tbl`(표) 생성"),
]:
    w(f"| {label} | {detail} |")
w("")
w("### 알아두면 좋은 값")
w("")
w("`HParaShape.AlignType` (문단 정렬) — 실측으로 확인한 값:")
w("")
w("| 값 | 정렬 | 값 | 정렬 |")
w("|---|---|---|---|")
w("| 0 | 양쪽 정렬 | 3 | 가운데 정렬 |")
w("| 1 | 왼쪽 정렬 | 4 | 배분 정렬 |")
w("| 2 | 오른쪽 정렬 | 5 | 나눔 정렬 |")
w("")
w("---")
w("")
w("## 목차")
w("")
for g, rows in groups.items():
    anchor = g.replace(" ", "-").replace("/", "").replace("(", "").replace(")", "")
    w(f"- [{g}](#{anchor}) ({len(rows)})")
w("")
w("---")
w("")

for g, rows in groups.items():
    w(f"## {g}")
    w("")
    w("| 기능 | 단축키 | 액션 ID |")
    w("|---|---|---|")
    for r in rows:
        aid = r["액션ID"]
        setid = ACT.get(aid, {}).get("setID")
        mark = f"`{aid}`" + (f" <sub>+{setid}</sub>" if setid else "")
        key = f"`{r['단축키']}`" if r["단축키"] else ""
        w(f"| {r['기능']} | {key} | {mark} |")
    w("")

w("---")
w("")
w("<sub>액션ID 뒤의 작은 글씨는 그 액션이 쓰는 **파라미터셋 이름**입니다. "
  "없으면 인자 없이 `Run()`만 하면 됩니다. 파라미터 전체 목록은 `hwp_macro_dict.json` 참고.</sub>")
w("")

out = os.path.join(BASE, "한글매크로_액션사전.md")
open(out, "w", encoding="utf-8").write("\n".join(L))
print(f"항목 {len(labels)}개 / 분류 {len(groups)}개 -> {out}")
print(f"크기: {os.path.getsize(out):,} bytes")
