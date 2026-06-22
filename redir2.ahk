;-----------------------------------易错语句说明---------------------------
;				普通							表达式
;赋值			a=%b%							a:=b
;字符串			a=s				a=				a:="s"	a:=""	尤其是空串
;比较			ifequal %a%,%b% if(a = b)		if(a = "s")		;括号在开头为运算符或函数时可以省略
;---------------------------------------------------------------------------
;;;提权
full_command_line := DllCall("GetCommandLine", "str")
if !(%A_IsUnicode%) goto l_reload
if !(A_IsAdmin or RegExMatch(full_command_line, " /restart(?!\S)")) {
l_reload:
	if A_IsCompiled
		Run *RunAs "%A_ScriptFullPath%" /restart /CP65001
	else
		Run *RunAs "%A_AhkPath%" /restart /CP65001 "%A_ScriptFullPath%"
	ExitApp
}
;;;;;;;;;;;;;;;;;;;;自动运行段，基础设置和窗口组
#NoEnv
#SingleInstance force
SetWorkingDir %A_ScriptDir%
Menu Tray, Icon, C:\WINDOWS\system32\SHELL32.dll, 44, 0
DetectHiddenWindows on
SetTitleMatchMode 2
SendMode Input
SetCapsLockState, AlwaysOff
SetNumLockState, AlwaysOn
SetScrollLockState, AlwaysOff
#WinActivateForce

GroupAdd, g_fastStone, ahk_class FastStoneImageViewerMainForm
GroupAdd, g_fastStone, ahk_class FastStoneImageViewerMainForm.UnicodeClass
GroupAdd, g_fastStone, ahk_class TFullScreenWindow
GroupAdd, g_ocr, Total Commander ahk_class TTOTAL_CMD
GroupAdd, g_ocr, ahk_class Chrome_WidgetWin_0 ahk_exe WeChatApp.exe
GroupAdd, g_ocr, ahk_class classFoxitReader
return
;;;;;;;;;;;;;;;;;;;;全局快捷键;;;;;;;;;;;;;;;;;;;;;;;;;;;
#IfWinActive
Capslock up::
	If (A_PriorKey = "CapsLock") {		;确认没形成组合键
		Send {esc}
	}
Return
>^CapsLock::SetCapsLockState % GetKeyState("CapsLock","T") ? "AlwaysOff" : "AlwaysOn"

Capslock & h::send {left}
Capslock & l::send {right}
Capslock & k::send {up}
Capslock & j::send {down}
Capslock & i::send {home}
Capslock & o::send {end}
Capslock & enter::
	send {end}
	sleep 100
	send {enter}
return

Capslock & u::send ^z
Capslock & n::send {Backspace}
Capslock & m::send {Del}
Capslock & .::send {NumpadDot}
Capslock & ,::send {U+002c}
;Capslock & ,::
;	SavedClipboard := ClipboardAll
;	Clipboard := ","
;	Send ^v
;	Sleep 50
;	Clipboard := SavedClipboard
;return
#F1::
	send,#5
return
$#F2::	;必须#UseHook on
	send,#6
return
#F3::
	send,#7
return
#F4::
	send,#8
return
#5::
	send,#9
return
#`::
	IfWinNotActive, ahk_class Chrome_WidgetWin_1 ahk_exe Obsidian.exe
		WinActivate, ahk_class Chrome_WidgetWin_1 ahk_exe Obsidian.exe
	Else
		WinMinimize
return
#t::	;焦点Windows终端
	IfWinNotExist,ahk_class CASCADIA_HOSTING_WINDOW_CLASS
	{
		envget,mycode,mycode
		runas,%A_UserName%,%mycode%
		run, C:\Users\%A_UserName%\AppData\Local\Microsoft\WindowsApps\wt.exe
		runas
	} else IfWinNotActive,ahk_class CASCADIA_HOSTING_WINDOW_CLASS
	{
		WinActivate,ahk_class CASCADIA_HOSTING_WINDOW_CLASS ahk_exe WindowsTerminal.exe
		CoordMode, Mouse, Screen
		MouseGetPos, xpos, ypos
		WinWaitActive, ahk_class CASCADIA_HOSTING_WINDOW_CLASS,,1
		if ErrorLevel
			return
		WinGetPos, X, Y, Width, Height, ahk_class CASCADIA_HOSTING_WINDOW_CLASS
		MouseClick, left, X+100, Y+100, , 0
		MouseMove, xpos, ypos ,0
	} Else
		WinMinimize
return
#w::	;必须#UseHook on
	IfWinNotExist ahk_class TTOTAL_CMD
	{
		envget,mycode,mycode
		runas,%A_UserName%,%mycode%
		;run %A_ComSpec% "/c start tc2.lnk"
		run tc.bat
		runas
	}
	IfWinNotActive ahk_class TTOTAL_CMD
		WinActivate
	Else
		WinMinimize
return
#f::
return
!F4:: send !{F12}
$!F12::
	send !{F4}
	sleep,100
	send,{alt up}
return
;;;;;;;;;;;;;;;;;;;;chrome;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#IfWinActive,Google Chrome
^b::^+b
F1::^t
;;;;;;;;;;;;;;;;;;;;anki;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;TODO
#IfWinActive
#a::			;在多个anki窗口间切换，如果是添加卡片窗口则点击输入框
	;send,{lwin up}
	DetectHiddenWindows, off
	global anki_iter
	global anki_arr
	if(anki_iter=""){
		anki_iter:=1
		anki_arr:=[]
	}
	if(anki_iter=1){
		anki_index=1
		IfWinExist Edit ahk_exe anki.exe
			anki_arr[anki_index++]:= "Edit ahk_exe anki.exe"
		IfWinExist Add ahk_exe anki.exe
			anki_arr[anki_index++]:= "Add ahk_exe anki.exe"
		IfWinExist selected) ahk_exe anki.exe
			anki_arr[anki_index++]:= "selected) ahk_exe anki.exe"
		IfWinExist Anki ahk_exe anki.exe
			anki_arr[anki_index++]:= "Anki ahk_exe anki.exe"
	}
	if(anki_arr[anki_iter]="")
		anki_iter=1
	WinActivate % anki_arr[anki_iter]
	SetTimer, l_anki_iter, 500
	SetTimer, l_anki_LWin, -1
	anki_iter++
Return
l_anki_iter:
	anki_iter=1
	SetTimer, l_anki_iter, off
return
l_anki_LWin:
	CoordMode, Mouse, Screen
	KeyWait, LWin
	WinWaitActive Add ahk_exe anki.exe,,1
	if ErrorLevel
		return
	MouseGetPos, xpos, ypos
	WinGetPos, X, Y, Width, Height, Add ahk_exe anki.exe
	MouseClick, left, X+100, Y+140, , 0
	MouseMove, xpos, ypos ,0
return
#IfWinActive Browse ahk_exe anki.exe
^f::
	send ^f{end}
return
#IfWinActive ahk_exe anki.exe
#a::				;全选当前文本，剪切，记录，切换到1.txt窗口
	;send,{lwin up}
	clipboard=
	;keywait,LWin
	send,^a^x
	clipwait,2
	FileAppend,%clipboard%, d:\Program Files\1.txt ,UTF-8
	WinActivate 1.txt ahk_class Vim
return
;;;;;;;;;;;;;;;;;;;;gvim;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#IfWinActive
#q::
	;send,{lwin up}
	envget,mycode,mycode
	IfWinNotExist ahk_class Vim
	{
		runas,%A_UserName%,%mycode%
		Run gvim.bat
		runas
	}Else IfWinNotActive ahk_class Vim
		WinActivate
	Else
		WinMinimize
Return
#IfWinActive ahk_class Vim
^!l::		;重启autohotkey脚本
	;reload 默认重启后不再是utf8代码页,不能识别中文, 使用run可指定代码页
	MsgBox redir`nA_IsAdmin: %A_IsAdmin%`nCommand line: `n"%A_AhkPath%" /restart /CP65001 "%A_ScriptFullPath%"
	Run *RunAs "%A_AhkPath%" /restart /CP65001 "%A_ScriptFullPath%"
	;PostMessage, 0x0111, 65305,,,ScriptFileName.ahk - AutoHotkey ; 挂起
	;PostMessage, 0x0111, 65306,,,ScriptFileName.ahk - AutoHotkey ; 暂停
	PostMessage, 0x0111, 65303,,,snip-md.ahk ahk_class AutoHotkey ; 重启
	ExitApp
return
;;;;;;;;;;;;;;;;;;;;屏幕识图ocr;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#IfWinActive ahk_group g_ocr
;^!a::		;复制文本到暂存
;	clipboard=	;剪贴板置空, 这样可用ClipWait检测文本什么时候被复制到剪贴板中
;	send ^!a
;	SetTimer, l_clipwait, 250
;return
l_clipwait:
	WinWait 屏幕识图 ahk_class TXGuiFoundation,,5
	if ErrorLevel
		return
	CoordMode, Mouse, Screen
	MouseGetPos, xpos, ypos
	WinGetPos, X, Y, Width, Height
	WinActivate
	MouseClick, left, X+Width-80, Y+Height-30, , 0
	MouseMove, xpos, ypos ,0
	ClipWait,5,1
	if ErrorLevel
		return
	SetTimer, l_clipwait, off
	WinClose
	;StringReplace,clipboard,clipboard,`r`n,,All
	FileAppend,%clipboard%, d:\Program Files\1.txt ,UTF-8
	if(substr(clipboard,0,1)!="`n")
		FileAppend,`n, d:\Program Files\1.txt ,UTF-8	;*表示二进制模式
return
;;;;;;;;;;;;;;;;;;;;foxit;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
	;TODO
#IfWinActive,ahk_class classFoxitReader
^q::		;复制文本到暂存
	ClipSaved := ClipboardAll
	clipboard=	;剪贴板置空, 这样可用ClipWait检测文本什么时候被复制到剪贴板中
	send ^c
	ClipWait,0.5,1
	if(ErrorLevel) {
		Clipboard := ClipSaved
		return
	}
	WinGetTitle, title_all
	StringSplit, title, title_all, -, %A_Space%%A_Tab%
	StringReplace,text,clipboard,`r`n,,All
	;获取控件文本
	ControlGetText, page_all1, Edit1, ahk_class classFoxitReader, , ,
	ControlGetText, page_all2, Edit2, ahk_class classFoxitReader, , ,
	ControlGetText, page_all3, Edit3, ahk_class classFoxitReader, , ,
	ControlGetText, page_all4, Edit4, ahk_class classFoxitReader, , ,
	ControlGetText, page_all5, Edit5, ahk_class classFoxitReader, , ,
	page_all=%page_all1% %page_all2% %page_all3% %page_all4% %page_all5%
	msgbox % page_all
	StringSplit, page, page_all, /, %A_Space%%A_Tab%
	updf=[p%page1%](updf://%title1%#page=%page1%)
	text=%updf%`n%text%
	run pyw.exe append1txt.pyw %text%
	;FileAppend,%text%, d:\Program Files\1.txt ,UTF-8
	;if(substr(text,0,1)!="`n")
	;	FileAppend,`n, d:\Program Files\1.txt ,UTF-8	;*表示二进制模式
	Clipboard := ClipSaved
return
$^c::		;trim头尾空格
	clipboard=
	send ^c
	ClipWait,5,1
	Clipboard:=trim(clipboard)
	ControlGetText, page_all, Edit3, ahk_class classFoxitReader, , ,
	StringSplit, page, page_all, /, %A_Space%%A_Tab%
	updf=[p%page1%](updf://p%page1%)
;	Clipboard=%updf%`n%Clipboard%
return
^!q::		;调用qq的截图功能,上传到图床并发送链接到暂存
	clipboard=	;剪贴板置空, 这样可用ClipWait检测文本什么时候被复制到剪贴板中
	send ^!a
	SetTimer, l_clipwait_oss, 250
return
l_clipwait_oss:
	ClipWait,5,1
	if ErrorLevel
		return
	SetTimer, l_clipwait_oss, off
	send ^!p
	Loop{
		StringGetPos, pos, clipboard, oss-cn-hangzhou
		if !ErrorLevel	;没有找到SearchText时ErrorLevel被置为1，否则为0
			break
	}
	FileAppend,%clipboard%, d:\Program Files\1.txt ,UTF-8
	if(substr(clipboard,0,1)!="`n")
		FileAppend,`n,* d:\Program Files\1.txt ,UTF-8	;*表示二进制模式
return
;;;;;;;;;;;;;;;;;;;;;;;对FastStone屏蔽home end;;;;;;;;;;;;;
#IfWinActive, ahk_group g_fastStone
End:: send {PgDn}
Home:: send {PgUp}
NumpadEnd::return
NumpadHome::return
NumpadEnter::return
^End:: send {End}
^Home:: send {Home}
\:: send f
;;;;;;;;;;;;;;;;;;;;;;;;;boss键;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#IfWinActive
#ESC::		;隐藏,boss键
	;send,{lwin up}
	winhide,魔兽世界
	winhide,ahk_class LWJGL
	winhide,Google Chrome
	sleep,100
	winactivate,ahk_class XLMAIN
	IfWinNotExist,ahk_class XLMAIN
	{
		winactivate,ahk_class SUMATRA_PDF_FRAME
	}
return
^esc::		;恢复,反boss键
	winshow,ahk_class LWJGL
	winshow,Google Chrome
	winshow,Google Chrome
	winshow,魔兽世界
	sleep,200
	winactivate,Google Chrome
return
;;;;;;;;;;;;;;;;;;;;魔兽世界;;;;;;;;;;;;;;;;;
#IfWinActive,魔兽世界
	lwin & `::send ^\
	lwin & 1::send ^+o
	lwin & 2::send ^+p
	lwin & 3::send ^+[
	lwin & 4::send ^+]
	lwin & q::send ^o
	lwin & w::send ^p
	lwin & e::send ^[
	lwin & r::send ^]
	lwin & a::send ^k
	lwin & s::send ^l
	lwin & d::send ^;
	lwin & f::send ^'
	lwin & z::send ^m
	lwin & x::send ^<
	lwin & c::send ^>
	lwin & v::send ^/
	lwin::return
