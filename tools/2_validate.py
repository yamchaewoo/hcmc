# -*- coding: utf-8 -*-
"""워치독 러너 (CreateAction 기반 안전 검증). 워커가 멈추면 죽이고 다음부터 재개."""
import subprocess, os, time, sys, json

BASE = r"C:\Users\SDIJ\PJ2\raw"
CAND = os.path.join(BASE, "candidates_filtered.txt")
RES  = os.path.join(BASE, "validate_progress.tsv")
CUR  = os.path.join(BASE, "validate_current.txt")
BLK  = os.path.join(BASE, "hanging_ids.txt")
WORKER = r"C:\Users\SDIJ\PJ2\tools\worker.py"
STALL = 25

total = len([c for c in open(CAND, encoding="utf-8").read().split("\n") if c])

def scan():
    rows, last = [], -1
    if os.path.exists(RES):
        with open(RES, encoding="utf-8") as f:
            for line in f:
                p = line.rstrip("\n").split("\t")
                if len(p) >= 3:
                    rows.append(p)
                    try: last = int(p[0])
                    except ValueError: pass
    return rows, last

t0 = time.time()
while True:
    rows, last = scan()
    start = last + 1
    if start >= total: break
    print(f"[runner] start={start:,}/{total:,}  ({time.time()-t0:.0f}s)", flush=True)
    p = subprocess.Popen([sys.executable, WORKER, str(start)],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    size = os.path.getsize(RES) if os.path.exists(RES) else 0
    moved = time.time()
    while p.poll() is None:
        time.sleep(2)
        sz = os.path.getsize(RES) if os.path.exists(RES) else 0
        if sz != size:
            size, moved = sz, time.time()
        elif time.time() - moved > STALL:
            culprit = open(CUR, encoding="utf-8").read() if os.path.exists(CUR) else "?"
            print(f"[runner] STALL -> kill. culprit: {culprit}", flush=True)
            p.kill()
            subprocess.run(["taskkill","/F","/IM","Hwp.exe"], capture_output=True)
            open(BLK,"a",encoding="utf-8").write(culprit+"\n")
            idx = culprit.split("\t")[0]
            if idx.isdigit():
                open(RES,"a",encoding="utf-8").write(f"{idx}\t{culprit.split(chr(9))[1]}\t0\t\t\n")
            time.sleep(2)
            break
    else:
        time.sleep(1)

rows, _ = scan()
actions = {}
for p in rows:
    if p[2] == "1":
        cand = p[1]
        actid = p[3] if len(p) > 3 and p[3] else cand
        setid = p[4] if len(p) > 4 else ""
        actions[actid] = {"actID": actid, "setID": setid}
out = os.path.join(BASE, "actions.json")
json.dump(actions, open(out,"w",encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
print(f"\n[runner] DONE {time.time()-t0:.0f}s  checked={len(rows):,}  VALID ACTIONS={len(actions):,}")
print("saved:", out)
