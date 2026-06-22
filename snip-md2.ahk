;不要在此文件加入任何capslock相关热键，防止冲突
#Requires AutoHotkey v2.0
;;;自动运行段，基础设置和窗口组
#SingleInstance force
SetWorkingDir(A_ScriptDir)
TraySetIcon("C:\WINDOWS\system32\SHELL32.dll", 75, 0)
DetectHiddenWindows True
SetTitleMatchMode(2)
SendMode("Input")
#WinActivateForce
full_command_line := DllCall("GetCommandLine", "str")
if InStr(full_command_line, "restart")
	MsgBox "snip-md`nA_IsAdmin: " A_IsAdmin "`nCommand line: `n" full_command_line

GroupAdd "g_md", "ahk_class NeteaseYoudaoYNoteMainWnd"
GroupAdd "g_md", "Typora"
return
;;;;;;;;;;;;;;;;;;;;全局热键/热字串;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;;;;;;;;;;;;;;;;;;;;有道云笔记热键/热字串;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#HotIf WinActive("ahk_class NeteaseYoudaoYNoteMainWnd")
tab:: Send("{U+0009}")
:o:``````::```````n`n``````{up}
:o:````::```````n`n``````{up}
:o:````m::``````math`n`n`n``````{up}
:o:``m::``````math`n`n`n``````{up}
:o:``::``$	$``{left 3}
;;;;;;;;;;;;;;;;;;;;有道云笔记/Typora热键/热字串;;;;;;;;;;;;;;;;;;;;;;;;;;;;
#HotIf WinActive("ahk_group g_md")
#Hotstring EndChars :;, `t
:co:rl::Reload()
;;;;;;;;;;;;;;;;;;;希腊字母;;;;;;;;;;;;;;;;;;
:co:alpha::α
:co:beta::β
:co:gamma::γ
:co:delta::δ
:co:epsilon::ε
:co:zeta::ζ
:co:eta::η
:co:theta::θ
:co:iota::ι
:co:kappa::κ
:co:lambda::λ
:co:mu::μ
:co:nu::ν
:co:xi::ξ
:co:omicron::ο
:co:pi::π
:co:rho::ρ
:co:sigma::σ
:co:tau::τ
:co:upsilon::υ
:co:phi::φ
:co:chi::χ
:co:psi::ψ
:co:omega::ω

:co:Alpha::Α
:co:Beta::Β
:co:Gamma::Γ
:co:Delta::Δ
:co:Epsilon::Ε
:co:Zeta::Ζ
:co:Eta::Η
:co:Theta::Θ
:co:Iota::Ι
:co:Kappa::Κ
:co:Lambda::Λ
:co:Mu::Μ
:co:Nu::Ν
:co:Xi::Ξ
:co:Omicron::Ο
:co:Pi::Π
:co:Rho::Ρ
:co:Sigma::Σ
:co:Tau::Τ
:co:Upsilon::Υ
:co:Phi::Φ
:co:Chi::Χ
:co:Psi::Ψ
:co:Omega::Ω
;;;;;;;;;;;;;;;;;;;;;;;;;粗体字符;;;;;;;;;;;;;;;;;;;;;;;;;
:co:.ba::\bm α
:co:.bb::\bm β
:co:.bg::\bm γ
:co:.bi::\bm i
:co:.bj::\bm j
:co:.bk::\bm k
:co:.be::\bm e
:co:.bn::\bm n
:co:.bs::\bm s
:co:.bv::\bm v
;;;;;;;;;;;;;;;;;;;;;;;;;正体字符;;;;;;;;;;;;;;;;;;;;;;;;;
:co:.rd::\mathrm d
;;;;;;;;;;;;;;;;;;;;;;;;;花体字符;;;;;;;;;;;;;;;;;;;;;;;;;
:co:.sP::\mathscr P

;;;;;;;;;;;;;;;;;;;;;;;;;算符替换;;;;;;;;;;;;;;;;;;;;;;;;;
:o?:./::\dfrac{{}{}}{{}{}}{left 3}		;;/
:co:.ol::\overline{{}{}}{left 1}		;;上划线
:co:.sq::\sqrt{{}{}}{left 1}			

:co:.pt::∂				;;偏微分∂ \partial `
:co:.int::\int_{{}{}}{^}{{}{}}{left 4}		;;∫
:co:.inti::\int_{{}-∞{}}{^}{{}{+}∞{}} `	;;∫-∞,+∞
:co:.ii::\iint\limits_{{}{}}{left 1}		;;∬
:co:.iii::\iiint\limits_{{}{}}{left 1}		;;∭
:co:.oi::\oint\limits_{{}{}}{^}{{}{}}{left 4}	;;∮ 
:co:.oii::\oiint\limits_{{}{}}{left 1}		;;O∬
:co:.lim::\lim\limits_{{}{}} {left 2}		;;lim_
:co:.limi::\lim\limits_{{}n\to ∞{}}		;;lim_n→∞
:co:.sum::\sum\limits_{{}{}}{^}{{}{}}{left 4}	;;sum_^
:co:.s1i::\sum\limits_{{}n=1{}}{^}{{}∞{}}	;;sum_n=1^∞
:co:.s0i::\sum\limits_{{}n=0{}}{^}{{}∞{}}	;;sum_n=0^∞

;;;;;;;;;;;;;;;;;;;;;;;;;环境设定;;;;;;;;;;;;;;;;;;;;;;;;;
:co:.align::\begin{{}aligned{}}`n`n\end{{}aligned{}} {up 1}{end}
:co:.case::\begin{{}cases{}}`n`n\end{{}cases{}} {up 1}{end}
:co:.arr::\begin{{}array{}}{{}{}}`n`n\end{{}array{}} {up 2}{end}
:co:.sarr::\begin{{}subarray{}}{{}{}}`n`n\end{{}subarray{}} {up 2}{end}	;;用于求和或求积的多行上下限

:co:.pmtr::\begin{{}pmatrix{}}`n`n\end{{}pmatrix{}} {up 1}{end}		;;( )矩阵
:co:.bmtr::\begin{{}bmatrix{}}`n`n\end{{}bmatrix{}} {up 1}{end}		;;[ ]矩阵
:co:.Bmtr::\begin{{}Bmatrix{}}`n`n\end{{}Bmatrix{}} {up 1}{end}		;;{ }矩阵
:co:.vmtr::\begin{{}vmatrix{}}`n`n\end{{}vmatrix{}} {up 1}{end}		;;| |矩阵
:co:.Vmtr::\begin{{}Vmatrix{}}`n`n\end{{}Vmatrix{}} {up 1}{end}		;;‖‖矩阵
:co:.pht::\phantom{{}{}}{left 1}					;;幻影占位

;;;;;;;;;;;;;;;;;;;;;;;;;自适应括号;;;;;;;;;;;;;;;;;;;;;;;;;
:co:.larr::\left\{{}`t\begin{{}array{}}{{}{}}`n`n\end{{}array{}} `t\right.{up 2}{end}{left 1}
:co:.mbrc::\left\{{}\right\{}} {end}{left 8}`n`n{up 1}
:co:.bbrc::\bigl\{{}\bigr\{}} {end}{left 7}`n`n{up 1}
:co:.mbrk::\left[`n`n\right{up 1}{end}
:co:.bbrk::\bigl[`n`n\bigr{up 1}{end}
:co:.mvert::\left|`n`n\right|{up 1}{end}
:co:.mpr::{Space}{left}\left(`n`n\right){del}`n{up 2}{end}

;;;;;;;;;;;;;;;;;;;;;;;;;单个字符;;;;;;;;;;;;;;;;;;;;;;;;;
:o?:^::{^}{{}{}}{left 1}
:o?:_::_{{}{}}{left 1}
:co:.brc::\{{}\{}}{left 2}			;;真实{}
:*o?:=::= `				;;等于号=加空格

; :*o?:()::{right 1}
; :*o?:(::(){left 1}
; :*o?:[::[]{left 1}
; :*o?:{::{{}{}}{left 1}

;;;;;;;;;;;;;;;;;;;;;;;;;特殊字符;;;;;;;;;;;;;;;;;;;;;;;;;
;;;集合
:co:.bs::⊂
:co:.nbs::⊄
:co:.bse::⊆
:co:.nbse::⊈
:co:.ps::⊃
:co:.nps::⊅
:co:.pse::⊇
:co:.npse::⊉
:co:.in::∈
:co:.nin::∉
:co:.cap::∩
:co:.cup::∪
:co:.es::∅
:co:.pce::≼
:co:.pc::≺
:co:.join::⋈
;;;逻辑
:co:.fa::∀
:co:.ex::∃
:co:.la::∧
:co:.lo::∨
:co:.ln::¬
:co:.op::⊕
:co:.r::→
:co:.l::←
:co:.R::⟹	;→→
:co:.lr::↔
:co:.nlr::↮
:co:.Lr::⇔
:co:.nLr::⇎
:co:.vd::⊢	;\vdash
:co:.Vd::⊨
:co:.if::∵
:co:.then::∴
;;;比较
:co:.ne::≠
:co:.ae::≡
:co:.le::≤
:co:.leq::≦
:co:.ge::≥
:co:.geq::≧
:co:.appr::≈
:co:.sim::∼
:co:.sime::≃
:co:.cong::≅
;;;其它
:co:.opr::\operatorname{{}{}}{left 1}
:co:.inf::∞
:co:.pp::∝
:co:.tm::×
:co:.pm::±
:co:.mp::∓
:co:.cd::·
:co:...::⋯
:co:.cc::∘
:co:.blt::∙
:co:.star::⋆
:co:.*::∗		;\ast
