<!--
id: 5d799758afa3c487e7b9
url: https://qiita.com/tenmyo/items/5d799758afa3c487e7b9
created_at: 2017-08-20T01:21:16+09:00
updated_at: 2017-08-20T10:56:45+09:00
private: false
coediting: false
tags:
- doxygen
- 静的解析
team: null
-->

# DoxygenでXMLファイル出力（依存関係等の解析結果含む）

# 導入
自動ドキュメントツール[Doxygen](http://www.stack.nl/~dimitri/doxygen/index.html)。多くのプログラミング言語と出力形式に対応しているため、使ったことのある方も多いかと思います。

この記事では、ドキュメントではなく、コードの依存関係等をXML出力するためのDoxygen設定を紹介します。


# Doxygenの設定
Doxywizard(DoxygenのGUIフロントエンド)だと、Expertタブから以下のような感じです。

* Buildで、出力に含めたい要素をチェック
* Source Browserで、`REFERENCED_BY_RELATION`/`REFERENCES_RELATION`にチェック
* XMLで、`GENERATE_XML`をチェック。（`XML_PROGRAMLISTING`チェックは外してもよい）

![Doxywizard-Build.png](https://qiita-image-store.s3.amazonaws.com/0/142637/9cb04a74-5f9a-f912-5fcd-bf3e9de93758.png)

![Doxywizard-SourceBrowser.png](https://qiita-image-store.s3.amazonaws.com/0/142637/cf7fd5ca-a0d4-564f-ae17-a9851579d57c.png)

![Doxywizard-XML.png](https://qiita-image-store.s3.amazonaws.com/0/142637/c7e3cde9-331c-f11f-d374-55677423dabe.png)


# 結果
前記の設定でDoxygenを実行すると、xmlディレクトリ以下にXMLファイルが出力されます。
![Doxygen-xml.png](https://qiita-image-store.s3.amazonaws.com/0/142637/66fa99e4-5331-6315-a9ff-63e6f8a12ecf.png)


# おまけ
XMLファイルはソースファイルごとに生成されるため、そのままだと扱いづらいです。
１ファイルにまとめる用のXSLT/XML(`combine.xslt`/`index.xml`)も出力されるため、これを使ってまとめると扱いやすくなります。

WindowsだとXSLT処理させるのが面倒なため、以下のようなPowerShellバッチを用意しておくとお手軽便利です。(.NETのXSLT処理系を使うため、別途XSLT処理系の準備が不要となります)

```doxygenxml_combine.ps1
 # DoxygenのXMLを結合する
 # 引数: Doxygen結果のxml格納フォルダ
 [CmdletBinding()]
 param(
     [Parameter(Mandatory=$True)]
     [string]$xml_dir
 )
 
 # お約束
 Set-StrictMode -Version Latest
 $ErrorActionPreference = "Stop"
 $WarningPreference = "Continue"
 $VerbosePreference = "Continue"
 $DebugPreference = "Continue"
 trap {
     $Error | foreach {
         Write-Debug $_.Exception.Message
         Write-Debug $_.InvocationInfo.PositionMessage
     }
     Exit -1
 }
 
 
 #### 処理
 
 # パス準備
 $xml_dir = (Convert-Path $xml_dir)
 [string]$xslt_path = (Join-Path $xml_dir combine.xslt)
 [string]$index_path = (Join-Path $xml_dir index.xml)
 [string]$combined_path = ($xml_dir + ".xml")
 
 # 存在チェック
 if (-not (Test-Path $xslt_path)) {
     Write-Host ("Error File Not Found: " + $xslt_path) -ForegroundColor red
     Exit -1
 }
 if (-not (Test-Path $index_path)) {
     Write-Host ("Error File Not Found: " + $index_path) -ForegroundColor red
     Exit -1
 }
 
 # 結合
 # XSLT読み込み
 $xslt = New-Object System.Xml.Xsl.XslCompiledTransform
 $xslt_setting = New-Object System.Xml.Xsl.XsltSettings
 $xslt_setting.EnableDocumentFunction = $true
 $xslt_setting.EnableScript = $true
 $xslt.Load($xslt_path, $xslt_setting, $null)
 # 出力準備
 $writer_setting = New-Object System.Xml.XmlWriterSettings
 $writer_setting.Indent = $true
 $writer = [System.Xml.XmlWriter]::Create($combined_path, $writer_setting)
 # 変換
 $xslt.Transform($index_path, $writer)
 # 終了
 $writer.Close()
 Write-Host ("Complete Combine: " + $combined_path) -ForegroundColor green
```
