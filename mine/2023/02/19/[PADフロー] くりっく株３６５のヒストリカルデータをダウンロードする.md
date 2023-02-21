<!--
id: b092500b0d84b71b63f4
url: https://qiita.com/tenmyo/items/b092500b0d84b71b63f4
created_at: 2023-02-19T22:52:02+09:00
updated_at: 2023-02-19T22:52:02+09:00
private: false
coediting: false
tags:
- ダウンロード
- PowerAutomateDesktop
team: null
-->

# [PADフロー] くりっく株３６５のヒストリカルデータをダウンロードする

[Power Automate for Desktop](https://www.microsoft.com/store/productId/9NFTCH6J7FHV)（PAD）を練習しようと思い、「くりっく株３６５：ヒストリカルデータベース」[^1]からダウンロードするフローを作ってみました。

[^1]: 東証サイトへのリンク設定は電話番号等をメール連絡しないといけないそうなので、リンクは割愛します。

## フロー

バージョン：2.29.00258.23041
Microsoft Store のバージョン: 10.0.5878.0

![PAD くりっく株３６５のヒストリカルデータをダウンロードする](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/142637/293cbd15-3812-0c46-9c6e-4bf1f70f58d5.png)

<details><summary>コピペ用コード</summary>

そのままだとごちゃついていたので、UI要素のスクリーンショットデータを削ったり整形しています。

```:PAD くりっく株３６５のヒストリカルデータをダウンロードする
WebAutomation.LaunchEdge.LaunchEdge Url: $'''https://www.tfx.co.jp/historical/cfd/''' WindowState: WebAutomation.BrowserWindowState.Normal ClearCache: False ClearCookies: False WaitForPageToLoadTimeout: 60 Timeout: 60 BrowserInstance=> Browser
WebAutomation.ExecuteJavascript BrowserInstance: Browser Javascript: $'''function ExecuteScript() {
document.querySelectorAll(\"input[type=checkbox][id^=historicalcfddata-product-]\").forEach((e)=>e.checked=true) 
}'''
WebAutomation.SetCheckboxState.SetCheckboxStateNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['取得項目 \'ALL\''] State: WebAutomation.CheckboxState.Checked
WebAutomation.SelectRadioButton.SelectRadioButtonNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定from']
WebAutomation.SetDropDownListValue.SetDropDownListValueByIndexNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定from月'] OptionsIndeces: 2
WebAutomation.SetDropDownListValue.SetDropDownListValueByIndexNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定from日'] OptionsIndeces: 2
WebAutomation.SelectRadioButton.SelectRadioButtonNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定to']
WebAutomation.SetDropDownListValue.SetDropDownListValueByIndexNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定to月'] OptionsIndeces: 13
WebAutomation.SetDropDownListValue.SetDropDownListValueByIndexNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定to日'] OptionsIndeces: 32
WebAutomation.ExecuteJavascript BrowserInstance: Browser Javascript: $'''function ExecuteScript() {
return document.querySelectorAll(\"#historicalcfddata-period-start-year>option\").length
}''' Result=> YearLen
LOOP LoopIndex FROM YearLen + 0 TO 2 STEP -1
    WebAutomation.SetDropDownListValue.SetDropDownListValueByIndexNoWait BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定from年'] OptionsIndeces: LoopIndex
    WebAutomation.SetDropDownListValue.SetDropDownListValueByIndex BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['期間指定to年'] OptionsIndeces: LoopIndex WaitForPageToLoadTimeout: 60
    WebAutomation.Click.Click BrowserInstance: Browser Control: appmask['Web Page \'https://www.tfx.co.jp/historical/cfd/\'']['Anchor \'csvダウンロード\''] ClickType: WebAutomation.ClickType.LeftClick MouseClick: True WaitForPageToLoadTimeout: 60 MousePositionRelativeToElement: WebAutomation.RectangleEdgePoint.MiddleCenter OffsetX: 0 OffsetY: 0
    WAIT 3
END

# [ControlRepository][PowerAutomateDesktop]

{
  "ControlRepositorySymbols": [
    {
      "IgnoreImagesOnSerialization": false,
      "Repository": "{\r\n
        \"Screens\": [\r\n
          {\r\n
            \"Controls\": [\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Label\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"取得項目 'ALL'\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"div[Id=\\\"wrapper\\\"] > section > div > form > div > div > div > label[Text=\\\"ALL\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"label\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Label\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定from\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"#historicalcfddata-period-start-type-date\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"label\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Select\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定from月\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"select[Id=\\\"historicalcfddata-period-start-month\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"select\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Select\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定from日\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"select[Id=\\\"historicalcfddata-period-start-day\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"select\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Label\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定to\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"#historicalcfddata-period-end-type-date\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"label\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Select\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定to月\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"select[Id=\\\"historicalcfddata-period-end-month\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"select\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Select\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定to日\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"select[Id=\\\"historicalcfddata-period-end-day\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"select\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Select\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定from年\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"select[Id=\\\"historicalcfddata-period-start-year\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"select\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Select\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"期間指定to年\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"select[Id=\\\"historicalcfddata-period-end-year\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"select\",\r\n
                \"ScreenshotPath\": null\r\n
              },\r\n
              {\r\n
                \"AutomationProtocol\": \"uia3\",\r\n
                \"ScreenShot\": null,\r\n
                \"ElementTypeName\": \"Anchor\",\r\n
                \"InstanceId\": null,\r\n
                \"Name\": \"Anchor 'csvダウンロード'\",\r\n
                \"SelectorCount\": 1,\r\n
                \"Selectors\": [\r\n
                  {\r\n
                    \"CustomSelector\": \"a[Class=\\\"cfd_csv_download_submit\\\"][Text=\\\"csvダウンロード\\\"]\",\r\n
                    \"Elements\": [],\r\n
                    \"Ignore\": false,\r\n
                    \"IsCustom\": true,\r\n
                    \"IsWindowsInstance\": false,\r\n
                    \"Order\": 0,\r\n
                    \"Name\": \"Default Selector\"\r\n
                  }\r\n
                ],\r\n
                \"Tag\": \"a\",\r\n
                \"ScreenshotPath\": null\r\n
              }\r\n
            ],\r\n
            \"ScreenShot\": null,\r\n
            \"ElementTypeName\": \"Web Page\",\r\n
            \"InstanceId\": null,\r\n
            \"Name\": \"Web Page 'https://www.tfx.co.jp/historical/cfd/'\",\r\n
            \"SelectorCount\": 1,\r\n
            \"Selectors\": [\r\n
              {\r\n
                \"CustomSelector\": \":desktop > domcontainer\",\r\n
                \"Elements\": [\r\n
                  {\r\n
                    \"Attributes\": [],\r\n
                    \"CustomValue\": \"domcontainer\",\r\n
                    \"Ignore\": false,\r\n
                    \"Name\": \"Web Page 'https://www.tfx.co.jp/historical/cfd/'\",\r\n
                    \"Tag\": \"domcontainer\"\r\n
                  }\r\n
                ],\r\n
                \"Ignore\": false,\r\n
                \"IsCustom\": true,\r\n
                \"IsWindowsInstance\": false,\r\n
                \"Order\": 0,\r\n
                \"Name\": \"Default Selector\"\r\n
              }\r\n
            ],\r\n
            \"Tag\": \"domcontainer\",\r\n
            \"ScreenshotPath\": null\r\n
          }\r\n
        ],\r\n
        \"Version\": 1\r\n
      }",
      "ImportMetadata": {
        "DisplayName": "ローカル コンピューター",
        "ConnectionString": "",
        "Type": "Local",
        "DesktopType": "local"
      },
      "Name": "appmask"
    }
  ],
  "ImageRepositorySymbol": {
    "Repository": "{\r\n  \"Folders\": [],\r\n  \"Images\": [],\r\n  \"Version\": 1\r\n}",
    "ImportMetadata": {},
    "Name": "imgrepo"
  },
  "ConnectionReferences": []
}
```
</details>

### 解説や感想など

今回の対象は以下の特徴があります。

- 指数が毎年増える（毎年追加＆１年少しで停止）
- 最大１年分しかダウンロードできない

２：ダウンロードデータの取得指数として、すべてにチェックします
３：ダウンロードデータの取得項目として、「ALL」をチェックします
４～９：対象期間として、1/1～12/31を指定しておきます
10～16：年をずらしながら、「csvダウンロード」します

指数（２）と年（10）のところ、「Webデータ抽出」なりでPADだけでやりたかったのですがうまくできず、やむなくJavaScriptです。

専用のアクションが無くてもJavaScriptなりでカバーできるのは便利です。セレクターがウィザードで選べるのもカスタムできるのも良いですね。
ファイルのダウンロード先を指定できないのが不便です。
画面がぱらぱら変わっていくのを眺めるのは仕事してる感が出てよい気分になれそうですが、CLIに慣れている身からするとまだるっこしいです。

PADは、面倒な月末の集計作業なんかがパッと手間を省けそうで興味深いです。
こんな良いものが広まっていくと、業務系で言われるまま組むだけのプログラマーは食べていけなくなりそうです。
ドメイン知識を押さえて改善コンサル的なところに手を出さないと厳しそうな感じがします。
