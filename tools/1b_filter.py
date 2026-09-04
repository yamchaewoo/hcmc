# -*- coding: utf-8 -*-
"""후보를 액션ID 형태로 좁힌다: 대문자 시작 + 영숫자만 + 소문자 포함 + 3~40자."""
import re, os
BASE = r"C:\Users\SDIJ\PJ2\raw"
cands = [c for c in open(os.path.join(BASE,"candidates.txt"), encoding="utf-8").read().split("\n") if c]
pat = re.compile(r"^[A-Z][A-Za-z0-9]{2,39}$")
keep = [c for c in cands if pat.match(c) and any(ch.islower() for ch in c)]
keep = sorted(set(keep))
open(os.path.join(BASE,"candidates_filtered.txt"),"w",encoding="utf-8").write("\n".join(keep))
print(f"{len(cands):,} -> {len(keep):,} 후보 (액션ID 형태만)")
