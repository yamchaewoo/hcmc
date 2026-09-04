# -*- coding: utf-8 -*-
import sys, win32com.client as w
sys.stdout.reconfigure(encoding="utf-8")
hwp = w.gencache.EnsureDispatch("HWPFrame.HwpObject")
print("default MessageBoxMode:", hwp.GetMessageBoxMode())
for mode in (0x00000020, 0x00020000, 0xFFFFFFFF):
    try: print(f"  SetMessageBoxMode({mode:#x}) ->", hwp.SetMessageBoxMode(mode))
    except Exception as e: print(f"  SetMessageBoxMode({mode:#x}) EXC", str(e)[:70])
hwp.SetMessageBoxMode(0x00020000)
hwp.XHwpDocuments.Add(0)

tests = ["BreakPara","MoveDocEnd","CharShapeBold","TableCreate","ParagraphShape",
         "ComposeCharsEdit","TotallyBogusActionXYZ","ZZZnope","Cut","Paste","Hyperlink"]
print("\n%-24s %-8s %-8s %-9s %s" % ("ID","Create","ActID","Enable","SetID"))
for t in tests:
    ca = actid = setid = en = "-"
    try:
        a = hwp.CreateAction(t)
        ca = "obj" if a is not None else "None"
        if a is not None:
            try: actid = a.ActID
            except Exception as e: actid = "EXC"
            try: setid = a.SetID or "(none)"
            except Exception as e: setid = "EXC"
            hwp.ReleaseAction(a)
    except Exception as e:
        ca = "EXC:" + str(e)[:24]
    try: en = str(hwp.IsActionEnable(t))
    except Exception as e: en = "EXC"
    print("%-24s %-8s %-8s %-9s %s" % (t, ca, actid, en, setid))
hwp.Quit()
