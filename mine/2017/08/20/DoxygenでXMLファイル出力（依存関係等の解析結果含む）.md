<!--
id: 5d799758afa3c487e7b9
url: https://qiita.com/tenmyo/items/5d799758afa3c487e7b9
created_at: 2017-08-20T01:21:16+09:00
updated_at: 2022-06-12T18:43:13+09:00
private: false
coediting: false
tags:
- doxygen
- XSLT
- 静的解析
team: null
-->

# DoxygenでXMLファイル出力（依存関係等の解析結果含む）

# 導入

ソースコードからのドキュメント生成ツール[Doxygen](https://doxygen.nl/)。多くのプログラミング言語と出力形式に対応しているため、使ったことのある方も多いんじゃないでしょうか。

この記事では、ドキュメントではなくコードの依存関係等をXML出力するためのDoxygen設定を紹介します。
出力のXSLT変換例も少し紹介します。

XML出力は、例えば以下のような独自のコード分析/解析やラッパーの自動生成等に活用できるかもしれません。

* 改修時の変更影響箇所の検討
* 関数呼び出し関係の見える化、コールグラフの作成
* グローバル変数への参照箇所の洗い出し
* 未使用関数や不要なincludeの洗い出し
* メトリクス測定
* 他言語バインディングの自動生成
* テストコードひな形の自動生成
* モックの自動生成

# Doxygenの設定

Doxywizard(DoxygenのGUIフロントエンド)だと、Expertタブから以下のような感じです。

* Buildで、出力に含めたい要素をチェック
* Source Browserで、`REFERENCED_BY_RELATION`/`REFERENCES_RELATION`にチェック
* XMLで、`GENERATE_XML`をチェック。（`XML_PROGRAMLISTING`チェックは外してもよい）

![Doxywizard-Build.png](https://qiita-image-store.s3.amazonaws.com/0/142637/9cb04a74-5f9a-f912-5fcd-bf3e9de93758.png)

![Doxywizard-SourceBrowser.png](https://qiita-image-store.s3.amazonaws.com/0/142637/cf7fd5ca-a0d4-564f-ae17-a9851579d57c.png)

![Doxywizard-XML.png](https://qiita-image-store.s3.amazonaws.com/0/142637/c7e3cde9-331c-f11f-d374-55677423dabe.png)

# 結果

前記の設定でdoxygenを実行すると、xmlディレクトリ以下にXMLファイルが出力されます。
![Doxygen-xml.png](https://qiita-image-store.s3.amazonaws.com/0/142637/66fa99e4-5331-6315-a9ff-63e6f8a12ecf.png)

## XML内容について

自然言語での公式ドキュメントは無さそうです。
スキーマ定義はxml出力先に含まれます（index.xsd, xml.xsd）。

定義や参照関係は出ますが、関数内のブロック構造は出ないようです。

<details><summary>xml抜粋</summary>

```xml:xml.xml
      <memberdef kind="define" id="aitc_8c_1a2512e9f94d9ab9e4c48b78400f9f2d44" prot="public" static="no">
        <name>FIPNDH</name>
        <param><defname>base</defname></param>
        <initializer>((base)+0x60)</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="aitc.c" line="79" column="9" bodyfile="aitc.c" bodystart="79" bodyend="-1" />
      </memberdef>
...
      <memberdef kind="function" id="aitc_8c_1a8353f48d9b6c62f1eaf43a0c0ac6ac9d" prot="public" static="yes" const="no" explicit="no" inline="no" virt="non-virtual">
        <type>void</type>
        <definition>static void int_source_change</definition>
        <argsstring>(SigNode *node, int value, void *clientData)</argsstring>
        <name>int_source_change</name>
        <param>
          <type><ref refid="struct_sig_node" kindref="compound">SigNode</ref> *</type>
          <declname>node</declname>
        </param>
        <param>
          <type>int</type>
          <declname>value</declname>
        </param>
        <param>
          <type>void *</type>
          <declname>clientData</declname>
        </param>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="aitc.c" line="172" column="1" bodyfile="aitc.c" bodystart="172" bodyend="183" />
        <references refid="struct_irq_trace_info_1ae85401bf0069a66b078436a712c5e550" compoundref="aitc_8c" startline="111">IrqTraceInfo::aitc</references>
        <references refid="struct_aitc_1a920cf4d7d13a06eb8944a7af53eeaa5f" compoundref="aitc_8c" startline="100">Aitc::intsrc</references>
        <references refid="struct_irq_trace_info_1af3d6abfd2d5ee95a490b9bb84230ed2a" compoundref="aitc_8c" startline="110">IrqTraceInfo::nr</references>
        <references refid="signode_8h_1a4893a579f5b29db39ff56a83d3d0622a" compoundref="signode_8h" startline="24">SIG_LOW</references>
        <references refid="aitc_8c_1a102505e8050a3b3e5066d02855ca1238" compoundref="aitc_8c" startline="115" endline="163">update_interrupts</references>
        <referencedby refid="aitc_8c_1a1190b3c9b1a45bbd79159dae993001f1" compoundref="aitc_8c" startline="587" endline="623">Aitc_New</referencedby>
      </memberdef>
```

</details>

<details><summary>xsd</summary>

```xml:index.xsd
<?xml version='1.0' encoding='utf-8' ?>
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
  <xsd:import namespace="http://www.w3.org/XML/1998/namespace" schemaLocation="xml.xsd"/>

  <xsd:element name="doxygenindex" type="DoxygenType"/>

  <xsd:complexType name="DoxygenType">
    <xsd:sequence>
      <xsd:element name="compound" type="CompoundType" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="version" type="xsd:string" use="required"/>
    <xsd:attribute ref="xml:lang" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="CompoundType">
    <xsd:sequence>
      <xsd:element name="name" type="xsd:string"/>
      <xsd:element name="member" type="MemberType" minOccurs="0" maxOccurs="unbounded"/>
    </xsd:sequence>
    <xsd:attribute name="refid" type="xsd:string" use="required"/>
    <xsd:attribute name="kind" type="CompoundKind" use="required"/>
  </xsd:complexType>

  <xsd:complexType name="MemberType">
    <xsd:sequence>
      <xsd:element name="name" type="xsd:string"/>
    </xsd:sequence>
    <xsd:attribute name="refid" type="xsd:string" use="required"/>
    <xsd:attribute name="kind" type="MemberKind" use="required"/>
  </xsd:complexType>
  
  <xsd:simpleType name="CompoundKind">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="class"/>
      <xsd:enumeration value="struct"/>
      <xsd:enumeration value="union"/>
      <xsd:enumeration value="interface"/>
      <xsd:enumeration value="protocol"/>
      <xsd:enumeration value="category"/>
      <xsd:enumeration value="exception"/>
      <xsd:enumeration value="file"/>
      <xsd:enumeration value="namespace"/>
      <xsd:enumeration value="group"/>
      <xsd:enumeration value="page"/>
      <xsd:enumeration value="example"/>
      <xsd:enumeration value="dir"/>
      <xsd:enumeration value="type"/>
      <xsd:enumeration value="concept"/>
    </xsd:restriction>
  </xsd:simpleType>

  <xsd:simpleType name="MemberKind">
    <xsd:restriction base="xsd:string">
      <xsd:enumeration value="define"/>
      <xsd:enumeration value="property"/>
      <xsd:enumeration value="event"/>
      <xsd:enumeration value="variable"/>
      <xsd:enumeration value="typedef"/>
      <xsd:enumeration value="enum"/>
      <xsd:enumeration value="enumvalue"/>
      <xsd:enumeration value="function"/>
      <xsd:enumeration value="signal"/>
      <xsd:enumeration value="prototype"/>
      <xsd:enumeration value="friend"/>
      <xsd:enumeration value="dcop"/>
      <xsd:enumeration value="slot"/>
    </xsd:restriction>
  </xsd:simpleType>

</xsd:schema>
```

```xml:xml.xsd
<?xml version='1.0'?>
<xsd:schema targetNamespace="http://www.w3.org/XML/1998/namespace"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema"
            xml:lang="en">

  <xsd:attribute name="lang" type="xsd:language">
  </xsd:attribute>

  <xsd:attribute name="space" default="preserve">
    <xsd:simpleType>
      <xsd:restriction base="xsd:NCName">
        <xsd:enumeration value="default"/>
        <xsd:enumeration value="preserve"/>
      </xsd:restriction>
    </xsd:simpleType>
  </xsd:attribute>

  <xsd:attributeGroup name="specialAttrs">
    <xsd:attribute ref="xml:lang"/>
    <xsd:attribute ref="xml:space"/>
  </xsd:attributeGroup>

</xsd:schema>
```

</details>

# おまけ

## XMLファイル結合用PowerShellバッチ

XMLファイルはソースファイルごとに生成されるため、そのままだと扱いづらいです。
１ファイルにまとめる用のXSLT/XML(`combine.xslt`/`index.xml`)も出力されるため、これを使ってまとめると扱いやすくなります。
Linuxだとxlstprocを使うのが手軽です。`xsltproc -o combined.xml xml/combine.xslt xml/index.xml`

WindowsだとXSLT処理させるのが面倒なため、以下のようなPowerShellバッチを用意しておくとお手軽便利です。(.NETのXSLT処理系を使うため、別途XSLT処理系の準備が不要となります)

<details><summary>XMLファイル結合用PowerShellバッチ</summary>

Doxygen結果のxml格納フォルダを引数で渡すと、xml格納フォルダの隣にxml.xmlファイルを出力します。

```ps1:doxygenxml_combine.ps1
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

</details>

## XSLT

XMLファイルはXSLTで変換/整形できます。
いくつかXSLT例を紹介します。

<details><summary>要素一覧CSV</summary>

```xml:member_dump.xslt
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="Shift_JIS" />

  <xsl:param name="delim" select="'&#x09;'" />
  <xsl:param name="break" select="'&#x0D;&#x0A;'" />
  
  <xsl:template match="/doxygen">
    <xsl:text>#id</xsl:text><xsl:value-of select="$delim" />
    <xsl:text>kind</xsl:text><xsl:value-of select="$delim" />
    <xsl:text>static</xsl:text><xsl:value-of select="$delim" />
    <xsl:text>name</xsl:text><xsl:value-of select="$delim" />
    <xsl:text>file</xsl:text><xsl:value-of select="$delim" />
    <xsl:text>line</xsl:text><xsl:value-of select="$break" />
    <xsl:for-each select="//memberdef">
      <xsl:value-of select="./@id" /><xsl:value-of select="$delim" />
      <xsl:value-of select="./@kind" /><xsl:value-of select="$delim" />
      <xsl:value-of select="./@static" /><xsl:value-of select="$delim" />
      <xsl:value-of select="./name" /><xsl:value-of select="$delim" />
      <xsl:value-of select="./location/@file" /><xsl:value-of select="$delim" />
      <xsl:value-of select="./location/@line" /><xsl:value-of select="$break" />
    </xsl:for-each>
  </xsl:template>
  
</xsl:stylesheet>
```

</details>

<details><summary>関数呼び出し一覧CSV</summary>

```xml:ref_dump.xslt
<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="text" encoding="Shift_JIS" />

  <xsl:param name="delim" select="'&#x09;'" />
  <xsl:param name="break" select="'&#x0D;&#x0A;'" />
  
  <xsl:template match="/doxygen">
    <xsl:text>#src_id</xsl:text><xsl:value-of select="$delim" />
    <xsl:text>dst_id</xsl:text><xsl:value-of select="$break" />
    <xsl:for-each select="//memberdef[@kind=&quot;function&quot;]/references">
      <xsl:value-of select="../@id" /><xsl:value-of select="$delim" />
      <xsl:value-of select="./@refid" /><xsl:value-of select="$break" />
    </xsl:for-each>
    <xsl:for-each select="//memberdef[@kind=&quot;function&quot;]/referencedby">
      <xsl:value-of select="./@refid" /><xsl:value-of select="$delim" />
      <xsl:value-of select="../@id" /><xsl:value-of select="$break" />
    </xsl:for-each>
  </xsl:template>
  
</xsl:stylesheet>
```

</details>

### XSLT処理用Windowsバッチ

<details><summary>XSLT処理用PowerShellバッチ</summary>

結合済みのXMLファイルを引数で渡すと、バッチと同名のXSLT（XSLT処理.ps1ならXSLT処理.xslt）を適用して、結果をout.csvに出力します。

```ps1:XSLT処理.ps1
# 引数: Doxygenの結合XML
# 出力: out.csv
[CmdletBinding()]
param(
    [Parameter(Mandatory=$True)]
    [string]$xml_path
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
$xml_path = (Convert-Path $xml_path)
[string]$xslt_path = [System.IO.Path]::ChangeExtension($MyInvocation.MyCommand.Path, ".xslt")
[string]$out_path = [System.IO.Path]::ChangeExtension($xml_path, "out.tsv")

# 存在チェック
if (-not (Test-Path $xslt_path)) {
    Write-Host ("Error File Not Found: " + $xslt_path) -ForegroundColor red
    Exit -1
}

# 結合
# XSLT読み込み
$xslt = New-Object System.Xml.Xsl.XslCompiledTransform
$xslt_setting = New-Object System.Xml.Xsl.XsltSettings
$xslt_setting.EnableDocumentFunction = $true
$xslt_setting.EnableScript = $true
$xslt.Load($xslt_path, $xslt_setting, $null)
# 変換
$xslt.Transform($xml_path, $out_path)
# 終了
Write-Host ("Complete: " + $out_path) -ForegroundColor green
```

</details>

# もっと知りたい方向け資料

以下のような資料を見つけました。
私の興味と異なるためあまり読み込んでいませんが、皆さんの参考にはなるかもしれません。

[doxygen/addon/doxmlparser at master · doxygen/doxygen](https://github.com/doxygen/doxygen/tree/master/addon/doxmlparser)
doxygenのXML出力の解析サンプル（python）

[XML/XSLT examples : Doxygen: Helper tools and scripts](https://doxygen.nl/helpers.html#dox_xmlexamples)
XML/XSLTのサンプル紹介

[C言語の構造体を構造分析したい〜静的解析としての doxygen](https://cat-in-136.github.io/2014/04/c-struct-with-doxygen-xml.html)
XMLから、C言語構造体の構造を JSON で吐き出すスクリプト（ruby）

[DoxygenのXML出力 - unyaunyaの日記](https://unyaunya.hatenadiary.org/entry/20130830/p1)
XMLから、CSVで関数・変数の参照を出力（python）

なお、もっとしっかり解析したい方には、フリーだとclang/LLVM系ツールが おすすめです。
https://clang.llvm.org/docs/Tooling.html
