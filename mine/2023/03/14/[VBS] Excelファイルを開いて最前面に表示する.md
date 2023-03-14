<!--
id: e7252c48f14b9641a7b1
url: https://qiita.com/tenmyo/items/e7252c48f14b9641a7b1
created_at: 2023-03-14T22:37:53+09:00
updated_at: 2023-03-14T22:37:53+09:00
private: false
coediting: false
tags:
- Excel
- VBScript
team: null
-->

# [VBS] Excelファイルを開いて最前面に表示する

## 背景

特定のExcelファイルを手軽に開きたくなりました。
実際は開いた後にいろいろやるんですが、うまく開くまでにえらい苦労したので、そのエッセンスを記録しておきます。
これのショートカットファイルをデスクトップに置いて、ショートカットキーを設定するとワンタッチで動かせます。

環境は次の通り。

- Windows 11 Home 22H2
- Excel 365 Desktop 2302(ビルド16130.20218)

## コード

```vb
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
```

Applicationは、変数で受けると別インスタンス（ウィンドウ）ができてしまいました。

## 参考

[【VBScript】使える時に使いたいVBScript(WSH)のコード - Qiita](https://qiita.com/Tabito/items/3772ec852908c7a1988f)
[GetObject(, "Excel~")だけで無く、GetObject(ファイル名)も活用しよう - Qiita](https://qiita.com/nukie_53/items/12cc0a3fc295a446a045)
[Bingチャット](https://www.bing.com/)
