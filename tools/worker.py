# -*- coding: utf-8 -*-
"""안전 검증 워커: CreateAction 으로만 판별한다 (부작용/대화상자 없음).
   유효 시 ActID(정규 표기) 와 SetID(파라미터셋 이름)까지 함께 기록."""
import sys, os
import win32com.client as w

BASE = r"C:\Users\SDIJ\PJ2\raw"
CAND = os.path.join(BASE, "candidates_filtered.txt")
RES  = os.path.join(BASE, "validate_progress.tsv")
CUR  = os.path.join(BASE, "validate_current.txt")

start = int(sys.argv[1])
cands = [c for c in open(CAND, encoding="utf-8").read().split("\n") if c]

hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
hwp.SetMessageBoxMode(0x00020000)          # 안전장치: 대화상자 자동 처리
try: hwp.XHwpDocuments.Add(0)
except Exception: pass

res = open(RES, "a", encoding="utf-8")
for i in range(start, len(cands)):
    c = cands[i]
    with open(CUR, "w", encoding="utf-8") as f:
        f.write(f"{i}\t{c}")
    actid = setid = ""
    ok = 0
    try:
        a = hwp.CreateAction(c)
        if a is not None:
            ok = 1
            try: actid = a.ActID or ""
            except Exception: pass
            try: setid = a.SetID or ""
            except Exception: pass
            try: hwp.ReleaseAction(a)
            except Exception: pass
    except Exception:
        ok = 0
    res.write(f"{i}\t{c}\t{ok}\t{actid}\t{setid}\n")
    res.flush()
res.close()
print("WORKER_DONE")
