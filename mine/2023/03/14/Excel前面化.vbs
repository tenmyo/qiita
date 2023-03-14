' SJIS
' 変数の宣言を強制
Option Explicit

Dim oWsh : Set oWsh = WScript.CreateObject("WScript.Shell")
Dim oFSO:Set oFSO = CreateObject("Scripting.FileSystemObject")
Dim fpath:fpath = oFSO.GetParentFolderName(WScript.ScriptFullName) & "\ワークシート.xlsx"

' GetObjectでファイルパスを渡すと、（なければ新たに開いてから）オブジェクトが得られる
Dim oWb:set oWb = GetObject(fpath)
Call oWb.Activate ' なくても動いた
oWb.Windows(1).Visible = True
Call oWsh.AppActivate(oWb.Application.Caption)
' ここでマクロとかいろいろ実行する
