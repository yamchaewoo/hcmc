# -*- coding: utf-8 -*-
"""검증된 액션 + 타입라이브러리 스키마를 합쳐 최종 사전을 만든다."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\Users\SDIJ\PJ2"
RAW  = os.path.join(BASE, "raw")

actions = json.load(open(os.path.join(RAW,"actions.json"), encoding="utf-8"))
tl      = json.load(open(os.path.join(RAW,"typelib.json"), encoding="utf-8"))

SKIP = {"QueryInterface","AddRef","Release","GetTypeInfoCount","GetTypeInfo",
        "GetIDsOfNames","Invoke","HSet","CreateItemArray","Application"}

def schema(setid):
    """SetID -> 파라미터 목록 [{name, type, readonly}]"""
    t = tl.get("H" + setid)
    if not t: return None
    props = {}
    for m in t["members"]:
        n = m["name"]
        if n in SKIP: continue
        if m["kind"] in ("get","put","putref"):
            e = props.setdefault(n, {"name": n, "type": None, "writable": False})
            if m["kind"] == "get": e["type"] = m["ret"]
            else:
                e["writable"] = True
                if e["type"] is None and m["args"]: e["type"] = m["args"][0]["type"]
        elif m["kind"] == "method":
            props.setdefault(n, {"name": n, "type": "method", "writable": False})
    return sorted(props.values(), key=lambda x: x["name"])

# 파라미터셋 사전
paramsets = {}
for setid in sorted({v["setID"] for v in actions.values() if v["setID"]}):
    s = schema(setid)
    if s is not None:
        paramsets[setid] = {"setID": setid, "comType": "H"+setid, "params": s}

# 액션 사전
out_actions = {}
for aid, v in sorted(actions.items()):
    e = {"actionID": aid, "setID": v["setID"] or None}
    e["paramCount"] = len(paramsets[v["setID"]]["params"]) if v["setID"] in paramsets else 0
    out_actions[aid] = e

doc = {
  "_meta": {
    "설명": "한/글 매크로(COM 오토메이션) 사전 - 설치된 한/글에서 기계적으로 추출·검증함",
    "한글버전": "13.0.0.3379 (한글 2024)",
    "추출방법": {
      "액션ID": "HwpApp.dll/Hwp.exe/HwpAppModule.dll 문자열 추출 -> HwpObject.CreateAction() 으로 전수 검증 (없는 ID는 None 반환)",
      "SetID":  "CreateAction(id).SetID - 해당 액션이 사용하는 파라미터셋 이름",
      "파라미터": "HwpObject.tlb 타입라이브러리 덤프에서 'H'+SetID 타입의 속성 목록"
    },
    "액션수": len(out_actions),
    "파라미터셋수": len(paramsets),
    "주의": "한글 설명(라벨)은 아직 미포함 - 별도 작업 필요"
  },
  "actions": out_actions,
  "parameterSets": paramsets,
}
p = os.path.join(BASE, "hwp_macro_dict.json")
json.dump(doc, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"액션 {len(out_actions):,}개 / 파라미터셋 {len(paramsets)}개 -> {p}")
print(f"파일 크기: {os.path.getsize(p):,} bytes")

# 사용 예시 확인
for a in ["BreakPara","TableCreate","AllReplace"]:
    e = out_actions[a]
    print(f"\n  {a}: setID={e['setID']} params={e['paramCount']}")
    if e["setID"]:
        for pr in paramsets[e["setID"]]["params"][:5]:
            print(f"      - {pr['name']} : {pr['type']}")
