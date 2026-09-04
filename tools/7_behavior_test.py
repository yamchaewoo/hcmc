# -*- coding: utf-8 -*-
"""라벨이 실제 동작과 맞는지 실측 검증.
   대화상자를 띄우지 않는 액션만 골라, 새 빈 문서에서 실행하고
   쪽수 / 커서위치 / 파라미터셋 값 / 개체목록 같은 안전한 관측값으로만 확인한다.
   (텍스트 스캔 API는 종료조건이 까다로워 쓰지 않는다)"""
import sys
import win32com.client as w
sys.stdout.reconfigure(encoding="utf-8")

hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.SetMessageBoxMode(0x00020000)
hwp.XHwpDocuments.Add(0)

def put(s):
    p = hwp.HParameterSet.HInsertText
    hwp.HAction.GetDefault("InsertText", p.HSet)
    p.Text = s
    hwp.HAction.Execute("InsertText", p.HSet)

def ctrls(cap=200):
    """문서의 개체 목록 (무한루프 방지 상한 있음)"""
    out, c, n = [], hwp.HeadCtrl, 0
    while c is not None and n < cap:
        out.append(c.CtrlID)
        c = c.Next
        n += 1
    return out

results = []
def check(label, ok, detail):
    results.append((label, bool(ok), detail))

put("첫째 줄")

# 1) 문단 나누기 -> 커서의 문단 번호가 증가해야 함
para_before = hwp.GetPos()[1]
hwp.HAction.Run("BreakPara")
para_after = hwp.GetPos()[1]
check("BreakPara = 문단 나누기(Enter)", para_after > para_before,
      f"문단번호 {para_before} -> {para_after}")

# 2) 강제 줄 나누기 -> 문단은 그대로여야 함 (BreakPara 와의 차이 확인)
put("둘째 줄")
p0 = hwp.GetPos()[1]
hwp.HAction.Run("BreakLine")
p1 = hwp.GetPos()[1]
check("BreakLine = 줄 나누기(Shift+Enter, 문단 유지)", p1 == p0,
      f"문단번호 {p0} -> {p1} (안 바뀌어야 정상)")

# 3) 쪽 나누기 -> 쪽수 증가
pg0 = hwp.PageCount
hwp.HAction.Run("BreakPage")
put("둘째 쪽")
pg1 = hwp.PageCount
check("BreakPage = 쪽 나누기(Ctrl+Enter)", pg1 > pg0, f"쪽수 {pg0} -> {pg1}")

# 4) 문서 처음/끝 이동
hwp.HAction.Run("MoveDocBegin")
b = hwp.GetPos()
hwp.HAction.Run("MoveDocEnd")
e = hwp.GetPos()
check("MoveDocBegin / MoveDocEnd = 문서 처음 / 맨 뒤로", b != e, f"처음={b}  끝={e}")

# 5) 줄 처음/끝 이동 (Home / End)
hwp.HAction.Run("MoveLineEnd")
le = hwp.GetPos()
hwp.HAction.Run("MoveLineBegin")
lb = hwp.GetPos()
check("MoveLineBegin / MoveLineEnd = 줄 처음(Home) / 줄 끝(End)", lb != le,
      f"줄처음={lb}  줄끝={le}")

# 6) 진하게 토글 -> CharShape 파라미터셋의 Bold 값 변화
hwp.HAction.Run("MoveDocEnd")
hwp.HAction.Run("MoveSelLineBegin")
cs = hwp.HParameterSet.HCharShape
hwp.HAction.GetDefault("CharShape", cs.HSet)
bold0 = cs.Bold
hwp.HAction.Run("CharShapeBold")
hwp.HAction.GetDefault("CharShape", cs.HSet)
bold1 = cs.Bold
check("CharShapeBold = 진하게 토글", bold0 != bold1, f"Bold {bold0} -> {bold1}")

# 7) 가운데 정렬 -> ParaShape 의 정렬값 변화
hwp.HAction.GetDefault("ParagraphShape", hwp.HParameterSet.HParaShape.HSet)
al0 = hwp.HParameterSet.HParaShape.AlignType
hwp.HAction.Run("ParagraphShapeAlignCenter")
hwp.HAction.GetDefault("ParagraphShape", hwp.HParameterSet.HParaShape.HSet)
al1 = hwp.HParameterSet.HParaShape.AlignType
check("ParagraphShapeAlignCenter = 가운데 정렬", al0 != al1, f"AlignType {al0} -> {al1}")

# 8) 미주 넣기 -> 개체 목록에 미주가 생겨야 함
hwp.HAction.Run("Cancel")
hwp.HAction.Run("MoveDocEnd")
c0 = ctrls()
hwp.HAction.Run("InsertEndnote")
hwp.HAction.Run("Close")          # 미주 편집창 빠져나오기
c1 = ctrls()
check("InsertEndnote = 미주 넣기(Ctrl+N,E)", len(c1) > len(c0),
      f"개체 {len(c0)}개 -> {len(c1)}개, 목록={c1}")

# 9) 표 만들기 (파라미터셋 사용) -> 표 개체 생성
hwp.HAction.Run("MoveDocEnd")
hwp.HAction.Run("BreakPara")
tc = hwp.HParameterSet.HTableCreation
hwp.HAction.GetDefault("TableCreate", tc.HSet)
tc.Rows, tc.Cols = 3, 4
tc.WidthType, tc.HeightType = 0, 0
tc.CreateItemArray("ColWidth", 4)
for i in range(4):
    tc.ColWidth.SetItem(i, 5000)
ok_exec = hwp.HAction.Execute("TableCreate", tc.HSet)
c2 = ctrls()
check("TableCreate(Rows=3,Cols=4) = 표 만들기", ok_exec and "tbl" in c2,
      f"Execute={ok_exec}, 개체목록={c2}")

print()
print(f"{'결과':<5}{'검증 항목':<48}근거")
print("-" * 104)
for label, ok, detail in results:
    print(f"{'통과' if ok else '실패':<5}{label:<48}{detail}")
print("-" * 104)
print(f"{sum(1 for _, o, _ in results if o)} / {len(results)} 통과")

hwp.XHwpDocuments.Item(0).Clear(1)
hwp.Quit()
