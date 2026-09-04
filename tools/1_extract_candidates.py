# -*- coding: utf-8 -*-
"""HWP 바이너리에서 액션ID 후보 문자열을 추출한다."""
import re, os, json, glob

BIN = r"C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin"
TARGETS = ["HwpApp.dll", "Hwp.exe", "HwpAppModule.dll", "HwpCore.dll",
           "HwpEngine.dll", "HncOfficeFramework.dll", "HwpModel.dll"]

# 액션ID 형태: 영문자 시작, 영숫자, 2~48자. 대개 PascalCase.
PAT = re.compile(rb"[A-Za-z][A-Za-z0-9_]{2,47}")

cands = set()
stats = {}
for name in TARGETS:
    p = os.path.join(BIN, name)
    if not os.path.exists(p):
        stats[name] = "MISSING"; continue
    data = open(p, "rb").read()
    before = len(cands)
    # ASCII 문자열
    for m in PAT.finditer(data):
        cands.add(m.group().decode("ascii"))
    # UTF-16LE 문자열: 널바이트 제거 후 재스캔
    u16 = data[::2]          # 짝수 바이트만 (UTF-16LE의 ASCII 하위바이트)
    for m in PAT.finditer(u16):
        cands.add(m.group().decode("ascii"))
    u16b = data[1::2]
    for m in PAT.finditer(u16b):
        cands.add(m.group().decode("ascii"))
    stats[name] = f"{len(data):,} bytes -> +{len(cands)-before:,} new"

print("== 소스 ==")
for k, v in stats.items():
    print(f"  {k}: {v}")
print(f"\n총 후보: {len(cands):,}")

os.makedirs(r"C:\Users\SDIJ\PJ2\raw", exist_ok=True)
out = r"C:\Users\SDIJ\PJ2\raw\candidates.txt"
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(cands)))
print("저장:", out)
