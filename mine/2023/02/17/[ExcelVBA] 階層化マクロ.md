<!--
id: 155cfad51cf87cc41ebe
url: https://qiita.com/tenmyo/items/155cfad51cf87cc41ebe
created_at: 2023-02-17T15:15:07+09:00
updated_at: 2023-02-17T15:15:36+09:00
private: false
coediting: false
tags:
- Excel
- VBA
- ExcelVBA
team: null
-->

# [ExcelVBA] 階層化マクロ

## 背景

ふだん家でExcel触ることはないのですが、私用のMicrosoftアカウントを見直してたらExcel2013を持っていることに気づきました。2023年4月11日には延長サポートも終了するみたいです。
[Microsoft アカウント | 注文履歴](https://account.microsoft.com/billing/orders?period=AllTime&type=All)
[Excel 2013 - Microsoft Lifecycle | Microsoft Learn](https://learn.microsoft.com/ja-jp/lifecycle/products/excel-2013)

せっかくなので色々触って遊んでみました。グループ化（アウトライン）で折り畳めるのが便利でしたが、いちいち手で設定しないと面倒でした。
ファイルツリーとか作る場合の手間を減らせないかと思ってVBAマクロを作ってみました。その記録記事です。

## 階層化の例

見やすいように一部手で折り畳んでます。

Linux系ファイルパス
![Linux系ファイルパス](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/142637/08884faa-26f7-c2f1-a4fa-af49d0e29138.png)
８つまでしか階層にできません。

Windows系ファイルパス
![Windows系ファイルパス](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/142637/fa6ef6f0-f9be-0bbf-d872-20f994d63b86.png)

章立て
![章立て](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/142637/ea510950-475b-bbc0-d4fe-4590a00fcbaa.png)

## コード

```vb
' 対象文字列strに含まれる特定文字findの数を数えます
Function StrCount(str As String, find As String) As Long
    StrCount = 0
    Dim cur As Long: cur = 0
    Do
        cur = InStr(cur + 1, str, find)
        If cur = 0 Then Exit Do
        StrCount = StrCount + 1
    Loop
End Function

Sub 階層化()
    Dim i As Long, tmpcnt As Long
    ' validate
    If (Selection.Columns.Count <> 1) Or (Selection.rows.Count = 1) Then
        Call MsgBox("１列＆複数行で選択してください")
        Exit Sub
    End If
    If Selection.Areas.Count <> 1 Then
        Call MsgBox("複数範囲には対応しません")
        Exit Sub
    End If
    ' 範囲の取得
    Dim srows As Range: Set srows = Selection.rows
    Dim endrow As Long: endrow = srows.Count
    If srows(endrow) = "" Then endrow = srows(srows.Count).End(XlDirection.xlUp).Row - srows.Row + 1
    ' valudate2
    If endrow = 0 Then
        Call MsgBox("選択範囲にデータが含まれません")
        Exit Sub
    End If
    ' 区切り文字設定
    Dim sep As String: sep = InputBox("区切り文字を指定してください", Default:="/")
    If sep = "" Then Exit Sub
    ' 最大値チェック。８階層までしか作れない。
    Dim msg As String: msg = ""
    If True Then ' 速度性能を追求したい場合はスキップさせるとよいかも
        Dim maxcnt As Long: maxcnt = 0
        For i = 1 To endrow
            tmpcnt = StrCount(srows(i), sep)
            If tmpcnt > maxcnt Then
                maxcnt = tmpcnt
                msg = vbCrLf & "（参考）最大レベルセル：" & maxcnt & vbCrLf & srows(i)
            End If
        Next i
    End If
    ' プレフィクス（階層化しないレベル）設定
    Dim rootlevel As Long: rootlevel = StrCount(srows(1), sep)
    Dim x_: x_ = InputBox("階層化し始めるレベルを指定してください。Excelの制限で最大８階層にキャップされます。" & vbCrLf & "（参考）先頭セル：" & rootlevel & vbCrLf & srows(1) & msg, Default:=rootlevel)
    If Not IsNumeric(x_) Then Exit Sub
    rootlevel = CLng(x_)
    ' 領域初期化
    Call srows.ClearOutline
    ActiveSheet.Outline.SummaryRow = XlSummaryRow.xlSummaryAbove
    ' for 各行:
    For i = 1 To endrow
        tmpcnt = StrCount(srows(i), sep) - rootlevel
        If tmpcnt >= 8 Then tmpcnt = 8 - 1 ' ８階層にキャップする。無理やり作るとエラーになる
        For j = 1 To tmpcnt
            Call srows(i).Group
        Next j
    Next i
End Sub
```

## 解説など

列をがっと選ぶか、セル範囲を選んで実行します。

区切り文字の数だけ階層を下げています。
厳密にやるなら上位との一致具合をきちんと見たほうがよいかもしれません。

今のやり方だと、上位階層が違っても同じグループになる場合があります。たとえば`/etc/a`, `/usr/b`と行が並んでいると同じグループになります。

![おかしな階層の例](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/142637/7ac2ca30-0697-965f-43a1-096f41087f05.png)

要望などは、ユースケース付きでコメントいただけるとお役に立てるかもしれません。
