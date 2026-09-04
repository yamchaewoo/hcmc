# -*- coding: utf-8 -*-
"""한글 기능명 + 단축키 + 액션ID 3열 라벨링 표를 만든다.

 - 한글명/단축키: 한/글 공식 도움말 단축키표(365행)에서 확인한 표기
 - 액션ID: CreateAction() 으로 실존 검증된 1,807개 중에서만 사용
 - 검증 실패(= 존재하지 않는 ID)는 표에 넣지 않고 경고로 출력한다
"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
BASE = r"C:\Users\SDIJ\PJ2"
VALID = set(json.load(open(os.path.join(BASE, "raw", "actions.json"), encoding="utf-8")))

# 형식:  분류 | 한글 기능명 | 단축키(없으면 비움) | 액션ID
TABLE = """
커서 이동|한 글자 오른쪽으로|→|MoveNextChar
커서 이동|한 글자 왼쪽으로|←|MovePrevChar
커서 이동|한 줄 아래로|↓|MoveDown
커서 이동|한 줄 위로|↑|MoveUp
커서 이동|한 단어 오른쪽으로|Ctrl+→|MoveNextWord
커서 이동|한 단어 왼쪽으로|Ctrl+←|MovePrevWord
커서 이동|낱말 처음으로||MoveWordBegin
커서 이동|낱말 끝으로||MoveWordEnd
커서 이동|줄 처음으로|Home|MoveLineBegin
커서 이동|줄 끝으로 (맨 뒤로)|End|MoveLineEnd
커서 이동|한 문단 아래로|Ctrl+↓|MoveNextParaBegin
커서 이동|한 문단 위로|Ctrl+↑|MovePrevParaBegin
커서 이동|문단 처음으로|Alt+Home|MoveParaBegin
커서 이동|문단 끝으로|Alt+End|MoveParaEnd
커서 이동|화면 첫 줄로|Ctrl+Home|MoveViewBegin
커서 이동|화면 끝 줄로|Ctrl+End|MoveViewEnd
커서 이동|한 화면 위로|Page Up|MovePageUp
커서 이동|한 화면 아래로|Page Down|MovePageDown
커서 이동|한 쪽 앞으로|Alt+Page Up|MovePageBegin
커서 이동|한 쪽 뒤로|Alt+Page Down|MovePageEnd
커서 이동|문서 처음으로|Ctrl+Page Up|MoveDocBegin
커서 이동|문서 끝으로 (문서 맨 뒤로)|Ctrl+Page Down|MoveDocEnd
커서 이동|왼쪽 단으로|Ctrl+Alt+←|MovePrevColumn
커서 이동|오른쪽 단으로|Ctrl+Alt+→|MoveNextColumn
커서 이동|단 처음으로||MoveColumnBegin
커서 이동|단 끝으로||MoveColumnEnd
커서 이동|앞 구역으로||MoveSectionUp
커서 이동|다음 구역으로||MoveSectionDown
커서 이동|이전 커서 위치로|Ctrl+=|MovePrevPos
커서 이동|다음 커서 위치로|Ctrl+Shift+=|MoveNextPos
커서 이동|화면 한 줄 위로 스크롤||MoveScrollUp
커서 이동|화면 한 줄 아래로 스크롤||MoveScrollDown
커서 이동|본문 처음으로||MoveTopLevelBegin
커서 이동|본문 끝으로||MoveTopLevelEnd
커서 이동|현재 리스트 처음으로||MoveListBegin
커서 이동|현재 리스트 끝으로||MoveListEnd

블록 선택|모두 선택|Ctrl+A|SelectAll
블록 선택|블록 설정 (선택 시작)|F3|Select
블록 선택|선택 해제||Cancel
블록 선택|낱말 처음까지 선택||MoveSelWordBegin
블록 선택|낱말 끝까지 선택 (낱말 블록)||MoveSelWordEnd
블록 선택|앞쪽 개체 선택|F11|SelectCtrlFront
블록 선택|뒤쪽 개체 선택||SelectCtrlReverse
블록 선택|단 선택||SelectColumn
블록 선택|오른쪽으로 선택 확장|Shift+→|MoveSelRight
블록 선택|왼쪽으로 선택 확장|Shift+←|MoveSelLeft
블록 선택|위로 선택 확장|Shift+↑|MoveSelUp
블록 선택|아래로 선택 확장|Shift+↓|MoveSelDown
블록 선택|줄 처음까지 선택|Shift+Home|MoveSelLineBegin
블록 선택|줄 끝까지 선택|Shift+End|MoveSelLineEnd
블록 선택|문단 처음까지 선택||MoveSelParaBegin
블록 선택|문단 끝까지 선택||MoveSelParaEnd
블록 선택|문서 처음까지 선택||MoveSelDocBegin
블록 선택|문서 끝까지 선택||MoveSelDocEnd
블록 선택|한 단어 오른쪽 선택||MoveSelNextWord
블록 선택|한 단어 왼쪽 선택||MoveSelPrevWord
블록 선택|한 화면 위까지 선택|Shift+Page Up|MoveSelPageUp
블록 선택|한 화면 아래까지 선택|Shift+Page Down|MoveSelPageDown

나누기|문단 나누기 (엔터/줄바꿈)|Enter|BreakPara
나누기|강제 줄 나누기|Shift+Enter|BreakLine
나누기|쪽 나누기 (페이지 바꿈)|Ctrl+Enter|BreakPage
나누기|단 나누기 (단 바꿈)|Ctrl+Shift+Enter|BreakColumn
나누기|단 설정 나누기|Ctrl+Alt+Enter|BreakColDef
나누기|구역 나누기|Alt+Shift+Enter|BreakSection

편집|되돌리기|Ctrl+Z|Undo
편집|다시 실행|Ctrl+Shift+Z|Redo
편집|오려 두기|Ctrl+X|Cut
편집|복사하기|Ctrl+C|Copy
편집|붙이기|Ctrl+V|Paste
편집|골라 붙이기|Ctrl+Alt+V|PasteSpecial
편집|지우기|Ctrl+E|Delete
편집|앞글자 지우기|BackSpace|DeleteBack
편집|한 단어 지우기|Ctrl+T / Ctrl+Delete|DeleteWord
편집|앞 단어 지우기|Ctrl+BackSpace|DeleteWordBack
편집|한 줄 지우기|Ctrl+Y|DeleteLine
편집|줄 뒤 지우기|Alt+Y|DeleteLineEnd
편집|글자 입력 (문자열 삽입)||InsertText
편집|탭 삽입|Tab|InsertTab
편집|빈칸 삽입|SpaceBar|InsertSpace
편집|고정폭 빈칸|Alt+SpaceBar|InsertFixedWidthSpace
편집|묶음 빈칸|Ctrl+Alt+SpaceBar|InsertNonBreakingSpace
편집|무른 하이픈|Ctrl+Shift+-|InsertSoftHyphen
편집|문단 위로 이동|Alt+Shift+↑|EditParaUp
편집|문단 아래로 이동|Alt+Shift+↓|EditParaDown
편집|조판 부호 지우기||DeleteCtrls

찾기/바꾸기|찾기|Ctrl+Q,F|FindDlg
찾기/바꾸기|찾아 바꾸기|Ctrl+F2 / Ctrl+H|ReplaceDlg
찾기/바꾸기|모두 바꾸기||AllReplace
찾기/바꾸기|바꾸기 실행||ExecReplace
찾기/바꾸기|다시 찾기|Ctrl+L|RepeatFind
찾기/바꾸기|앞으로 찾기||ForwardFind
찾기/바꾸기|뒤로 찾기||BackwardFind
찾기/바꾸기|거꾸로 찾기|Ctrl+Q,L|ReverseFind
찾기/바꾸기|찾아가기|Alt+G|Goto

글자 모양|글자 모양 대화상자|Alt+L|CharShape
글자 모양|진하게|Ctrl+B / Alt+Shift+B|CharShapeBold
글자 모양|기울임|Ctrl+I / Alt+Shift+I|CharShapeItalic
글자 모양|밑줄|Ctrl+U / Alt+Shift+U|CharShapeUnderline
글자 모양|취소선||CharShapeStrikeout
글자 모양|외곽선||CharShapeOutline
글자 모양|그림자||CharShapeShadow
글자 모양|양각||CharShapeEmboss
글자 모양|음각||CharShapeEngrave
글자 모양|위 첨자|Alt+Shift+P|CharShapeSuperscript
글자 모양|아래 첨자|Alt+Shift+S|CharShapeSubscript
글자 모양|위/아래 첨자 순환|Ctrl+Alt+A|CharShapeSuperSubscript
글자 모양|보통 모양|Alt+Shift+C|CharShapeNormal
글자 모양|글씨 크게|Alt+Shift+E / Ctrl+]|CharShapeHeightIncrease
글자 모양|글씨 작게|Alt+Shift+R / Ctrl+[|CharShapeHeightDecrease
글자 모양|글자 크기 지정||CharShapeHeight
글자 모양|자간 넓게|Alt+Shift+W|CharShapeSpacingIncrease
글자 모양|자간 좁게|Alt+Shift+N|CharShapeSpacingDecrease
글자 모양|장평 넓게|Alt+Shift+K|CharShapeWidthIncrease
글자 모양|장평 좁게|Alt+Shift+J|CharShapeWidthDecrease
글자 모양|다음 글꼴|Alt+Shift+F|CharShapeNextFaceName
글자 모양|이전 글꼴|Alt+Shift+G|CharShapePrevFaceName
글자 모양|글꼴 지정||CharShapeTypeFace
글자 모양|검정 글자색|Ctrl+M,K|CharShapeTextColorBlack
글자 모양|빨강 글자색|Ctrl+M,R|CharShapeTextColorRed
글자 모양|파랑 글자색|Ctrl+M,B|CharShapeTextColorBlue
글자 모양|자주 글자색|Ctrl+M,D|CharShapeTextColorViolet
글자 모양|초록 글자색|Ctrl+M,G|CharShapeTextColorGreen
글자 모양|노랑 글자색|Ctrl+M,Y|CharShapeTextColorYellow
글자 모양|청록 글자색|Ctrl+M,C|CharShapeTextColorBluish
글자 모양|흰색 글자색|Ctrl+M,W|CharShapeTextColorWhite

문단 모양|문단 모양 대화상자|Alt+T|ParagraphShape
문단 모양|양쪽 정렬|Ctrl+Shift+M|ParagraphShapeAlignJustify
문단 모양|왼쪽 정렬|Ctrl+Shift+L|ParagraphShapeAlignLeft
문단 모양|오른쪽 정렬|Ctrl+Shift+R|ParagraphShapeAlignRight
문단 모양|가운데 정렬|Ctrl+Shift+C|ParagraphShapeAlignCenter
문단 모양|배분 정렬|Ctrl+Shift+T|ParagraphShapeAlignDistribute
문단 모양|나눔 정렬||ParagraphShapeAlignDivision
문단 모양|줄 간격 넓게|Alt+Shift+Z / Ctrl+Shift+W|ParagraphShapeIncreaseLineSpacing
문단 모양|줄 간격 좁게|Alt+Shift+A / Ctrl+Shift+Q|ParagraphShapeDecreaseLineSpacing
문단 모양|왼쪽 여백 늘이기|Ctrl+Alt+F6 / Ctrl+Shift+G|ParagraphShapeIncreaseLeftMargin
문단 모양|왼쪽 여백 줄이기|Ctrl+Alt+F5 / Ctrl+Shift+E|ParagraphShapeDecreaseLeftMargin
문단 모양|오른쪽 여백 늘이기|Ctrl+Alt+F7 / Ctrl+Shift+D|ParagraphShapeIncreaseRightMargin
문단 모양|오른쪽 여백 줄이기|Ctrl+Alt+F8 / Ctrl+Shift+F|ParagraphShapeDecreaseRightMargin
문단 모양|양쪽 여백 늘이기|Ctrl+F8|ParagraphShapeIncreaseMargin
문단 모양|양쪽 여백 줄이기|Ctrl+F7|ParagraphShapeDecreaseMargin
문단 모양|첫 줄 들여쓰기|Ctrl+F6 / Ctrl+Shift+I|ParagraphShapeIndentPositive
문단 모양|첫 줄 내어쓰기|Ctrl+F5 / Ctrl+Shift+O|ParagraphShapeIndentNegative
문단 모양|빠른 내어쓰기|Shift+Tab|ParagraphShapeIndentAtCaret
문단 모양|문단 보호||ParagraphShapeProtect
문단 모양|다음 문단과 함께||ParagraphShapeWithNext
문단 모양|외톨이 줄 보호||ParagraphShapeSingleRow
문단 모양|줄 간격 지정||ParaShapeLineSpace
문단 모양|문단 번호 모양|Ctrl+K,N|ParaNumberDlg
문단 모양|문단 번호/글머리표 적용||ParaNumberBullet
문단 모양|한 수준 증가|Ctrl+(Num)-|ParaNumberBulletLevelUp
문단 모양|한 수준 감소|Ctrl+(Num)+|ParaNumberBulletLevelDown
문단 모양|스타일|F6|Style
문단 모양|스타일로 이동||GotoStyle

쪽/구역|편집 용지|F7|PageSetup
쪽/구역|가로 용지||PageLandscape
쪽/구역|세로 용지||PagePortrait
쪽/구역|구역 설정|Ctrl+N,G|ModifySection
쪽/구역|단 설정||MultiColumn
쪽/구역|쪽 번호 매기기|Ctrl+N,P|PageNumPos
쪽/구역|쪽 번호 넣기||InsertPageNum
쪽/구역|현재 쪽만 감추기|Ctrl+N,S|PageHiding
쪽/구역|머리말/꼬리말|Ctrl+N,H|HeaderFooter
쪽/구역|머리말/꼬리말 고치기||HeaderFooterModify
쪽/구역|머리말/꼬리말 지우기||HeaderFooterDelete
쪽/구역|다음 머리말로 이동||HeaderFooterToNext
쪽/구역|이전 머리말로 이동||HeaderFooterToPrev
쪽/구역|쪽 테두리/배경||PageBorder
쪽/구역|첫 쪽으로||GotoFirstPage
쪽/구역|마지막 쪽으로||GotoLastPage
쪽/구역|다음 쪽으로||GotoNextPage
쪽/구역|이전 쪽으로||GotoPrevPage
쪽/구역|쪽 지우기||DeletePage
쪽/구역|쪽 복사||CopyPage
쪽/구역|바탕쪽||MasterPage

주석(각주/미주)|각주 넣기|Ctrl+N,N|InsertFootnote
주석(각주/미주)|미주 넣기 (미주 삽입)|Ctrl+N,E|InsertEndnote
주석(각주/미주)|주석 지우기||NoteDelete
주석(각주/미주)|주석 고치기||NoteModify
주석(각주/미주)|다음 주석으로 이동||NoteToNext
주석(각주/미주)|이전 주석으로 이동||NoteToPrev
주석(각주/미주)|주석 번호 모양||NoteNumShape
주석(각주/미주)|주석 번호 속성||NoteNumProperty
주석(각주/미주)|주석 위치||NotePosition
주석(각주/미주)|각주를 미주로||FootnoteToEndnote
주석(각주/미주)|미주를 각주로||EndnoteToFootnote
주석(각주/미주)|각주/미주 서로 바꾸기||ExchangeFootnoteEndnote
주석(각주/미주)|미주를 문서 끝에||EndnoteEndOfDocument
주석(각주/미주)|미주를 구역 끝에||EndnoteEndOfSection
주석(각주/미주)|주석 구분선 모양||NoteLineShape
주석(각주/미주)|주석 구분선 길이||NoteLineLength
주석(각주/미주)|주석 번호 위 첨자로||NoteSuperscript
주석(각주/미주)|주석 번호 보통으로||NoteNoSuperscript

수식|수식 만들기|Ctrl+N,M|EquationCreate
수식|수식 고치기 (수식 편집)||EquationModify
수식|수식 속성||EquationPropertyDialog
수식|수식을 글자처럼 취급||EqTreatAsChar

표|표 만들기|Ctrl+N,T|TableCreate
표|표 나누기|Ctrl+N,A|TableSplitTable
표|표 붙이기|Ctrl+N,Z|TableMergeTable
표|셀 합치기|M|TableMergeCell
표|셀 나누기|S|TableSplitCell
표|셀 블록 설정|F5|TableCellBlock
표|줄 전체 블록||TableCellBlockRow
표|칸 전체 블록||TableCellBlockCol
표|셀 블록 확장|Shift+F5|TableCellBlockExtend
표|위에 줄 추가||TableInsertUpperRow
표|아래에 줄 추가||TableInsertLowerRow
표|왼쪽에 칸 추가||TableInsertLeftColumn
표|오른쪽에 칸 추가||TableInsertRightColumn
표|줄/칸 추가하기|Alt+Insert|TableInsertRowColumn
표|줄/칸 지우기|Alt+Delete|TableDeleteRowColumn
표|줄 지우기||TableDeleteRow
표|칸 지우기||TableDeleteColumn
표|마지막 줄에 줄 추가|Ctrl+Enter|TableAppendRow
표|줄 높이를 같게|H|TableDistributeCellHeight
표|칸 너비를 같게|W|TableDistributeCellWidth
표|오른쪽 셀로|Tab|TableRightCell
표|왼쪽 셀로|Shift+Tab|TableLeftCell
표|위쪽 셀로||TableUpperCell
표|아래쪽 셀로||TableLowerCell
표|줄 처음 셀로||TableColBegin
표|줄 마지막 셀로||TableColEnd
표|표/셀 속성|P|TablePropertyDialog
표|셀 테두리/배경||CellBorderFill
표|캡션 넣기|Ctrl+N,C|TableCaption
표|표를 문자열로||TableTableToString
표|문자열을 표로||TableStringToTable
표|표 자동 채우기|A|TableAutoFill
표|계산식|Ctrl+N,F|TableFormula
표|가로 합계|Ctrl+Shift+H|TableFormulaSumHor
표|세로 합계|Ctrl+Shift+V|TableFormulaSumVer
표|가로 평균|Ctrl+Shift+J|TableFormulaAvgHor
표|세로 평균|Ctrl+Shift+B|TableFormulaAvgVer
표|가로 곱|Ctrl+Shift+K|TableFormulaProHor
표|세로 곱|Ctrl+Shift+N|TableFormulaProVer

입력/개체|그림 넣기|Ctrl+N,I|PictureInsertDialog
입력/개체|글상자 넣기|Ctrl+N,B|DrawObjCreatorTextBox
입력/개체|차트 넣기||InsertChart
입력/개체|문서 끼워 넣기|Ctrl+O|InsertFile
입력/개체|문단 띠|Ctrl+N,L|InsertLine
입력/개체|하이퍼링크|Ctrl+K,H|Hyperlink
입력/개체|하이퍼링크 넣기||InsertHyperlink
입력/개체|하이퍼링크 지우기||DeleteHyperlink
입력/개체|하이퍼링크 뒤로|Ctrl+Q,B|HyperlinkBackward
입력/개체|하이퍼링크 앞으로|Ctrl+Q,R|HyperlinkForward
입력/개체|책갈피|Ctrl+K,B|Bookmark
입력/개체|상호 참조|Ctrl+K,R|InsertCrossReference
입력/개체|날짜/시간 문자열|Ctrl+K,D|InsertStringDateTime
입력/개체|날짜/시간 코드|Ctrl+K,C|InsertDateCode
입력/개체|파일 이름 넣기||InsertFileName
입력/개체|파일 경로 넣기||InsertFilePath
입력/개체|문자표|Ctrl+F10|InputCodeTable
입력/개체|메모 넣기||InsertFieldMemo
입력/개체|메모 지우기||DeleteFieldMemo
입력/개체|다음 메모로||MemoToNext
입력/개체|이전 메모로||MemoToPrev
입력/개체|덧말 지우기||DeleteDutmal
입력/개체|글자 겹치기||ComposeChars

파일|새 문서|Alt+N|FileNew
파일|새 탭|Ctrl+Alt+T|FileNewTab
파일|불러오기|Alt+O|FileOpen
파일|저장하기|Alt+S / Ctrl+S|FileSave
파일|다른 이름으로 저장|Alt+V|FileSaveAs
파일|PDF로 저장||FileSaveAsPdf
파일|문서 닫기|Ctrl+F4|FileClose
파일|끝 (한글 종료)|Alt+X|FileQuit
파일|미리 보기||FilePreview
파일|문서 정보|Ctrl+Q,I|DocumentInfo
파일|문서마당|Ctrl+Alt+N|FileTemplate
파일|호환 문서|Ctrl+N,D|CompatibleDocument

보기|전체 화면|Ctrl+G,Z|FrameFullScreen
보기|전체 화면 끝내기||FrameFullScreenEnd
보기|가로 눈금자||FrameHRuler
보기|세로 눈금자||FrameVRuler
보기|상태 표시줄||FrameStatusBar
보기|가로 스크롤바||HorzScrollbar

도구|한컴 사전|Shift+F6 / F12|HwpDic
도구|한글을 한자로|F9|InputHanja
도구|한자를 한글로|Alt+F9|ConvertToHangul
도구|한자 단어 등록|Ctrl+Alt+F9|AddHanjaWord
도구|한자 부수/총획수|Ctrl+F9|InputHanjaBusu
도구|상용구 넣기|Alt+I|InsertIdiom
도구|상용구 등록||Idiom
도구|차례 만들기||MakeContents
도구|색인 만들기||MakeIndex
도구|제목 차례 표시|Ctrl+K,T|MarkTitle
도구|색인 표시 달기|Ctrl+K,I|IndexMark
도구|메일 머지 필드 넣기|Ctrl+K,M|MailMergeField
도구|메일 머지 만들기|Alt+M|MailMergeGenerate
도구|스크립트 매크로 정의|Alt+Shift+H|MacroDefine
도구|스크립트 매크로 중지|Alt+Shift+X|MacroStop
도구|매크로 실행 1|Alt+Shift+1|MacroPlay1
도구|매크로 반복||MacroRepeat
"""

rows, missing = [], []
for line in TABLE.strip().split("\n"):
    line = line.strip()
    if not line:
        continue
    cat, ko, key, aid = [x.strip() for x in line.split("|")]
    (rows if aid in VALID else missing).append((cat, ko, key, aid))

print(f"검증 통과: {len(rows)}개  /  실패(존재하지 않는 ID): {len(missing)}개")
if missing:
    print("\n--- 표에서 제외됨 (액션ID 미존재) ---")
    for c, k, s, a in missing:
        print(f"  [{c}] {k:30} -> {a}")

json.dump([{"분류": c, "기능": k, "단축키": s, "액션ID": a} for c, k, s, a in rows],
          open(os.path.join(BASE, "raw", "labels.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
