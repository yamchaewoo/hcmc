# -*- coding: utf-8 -*-
"""HwpObject.tlb 를 통째로 덤프해서 객체모델 + 모든 ParameterSet 스키마를 뽑는다."""
import json, os, pythoncom
from win32com.client import build

TLB = r"C:\Program Files (x86)\Hnc\Office 2024\HOffice130\Bin\HwpObject.tlb"
tl = pythoncom.LoadTypeLib(TLB)
n = tl.GetTypeInfoCount()

VT = {2:'int16',3:'int32',4:'float',5:'double',7:'date',8:'BSTR(문자열)',
      11:'bool',12:'VARIANT',13:'IUnknown',9:'IDispatch',16:'int8',17:'uint8',
      18:'uint16',19:'uint32',20:'int64',21:'uint64',22:'int',23:'uint',24:'void',
      26:'PTR',27:'SAFEARRAY',28:'CARRAY',29:'USERDEFINED',1:'NULL',0:'EMPTY'}
def vt(t):
    if isinstance(t, tuple):
        return vt(t[0]) if t[0] in (26,27,28) else VT.get(t[0], str(t))
    return VT.get(t, str(t))

INVKIND = {1:'method', 2:'get', 4:'put', 8:'putref'}
out = {}
for i in range(n):
    ti = tl.GetTypeInfo(i)
    name, doc = tl.GetDocumentation(i)[0], tl.GetDocumentation(i)[1]
    attr = ti.GetTypeAttr()
    members = []
    for f in range(attr.cFuncs):
        fd = ti.GetFuncDesc(f)
        fname = ti.GetNames(fd.memid)[0]
        argnames = ti.GetNames(fd.memid)[1:]
        args = [{"name": (argnames[j] if j < len(argnames) else f"arg{j}"),
                 "type": vt(fd.args[j][0])} for j in range(len(fd.args))]
        members.append({"name": fname, "kind": INVKIND.get(fd.invkind, fd.invkind),
                        "ret": vt(fd.rettype), "args": args})
    out[name] = {"doc": doc, "members": members}

os.makedirs(r"C:\Users\SDIJ\PJ2\raw", exist_ok=True)
p = r"C:\Users\SDIJ\PJ2\raw\typelib.json"
json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"types: {len(out)}   members: {sum(len(v['members']) for v in out.values()):,}")
print("saved:", p)
# 샘플
for k in ("HAction","HCharShape","HParameterSet"):
    if k in out:
        print(f"\n-- {k} ({len(out[k]['members'])} members) --")
        for m in out[k]['members'][:12]:
            print("   ", m['kind'], m['name'], "->", m['ret'])
