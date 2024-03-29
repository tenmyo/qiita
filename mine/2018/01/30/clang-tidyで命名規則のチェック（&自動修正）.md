<!--
id: 9753609385c7e4ff5222
url: https://qiita.com/tenmyo/items/9753609385c7e4ff5222
created_at: 2018-01-30T15:23:48+09:00
updated_at: 2018-02-02T12:25:59+09:00
private: false
coediting: false
tags:
- C++
- 命名規則
- naming
- lint
- clang-tidy
team: null
-->

# clang-tidyで命名規則のチェック（&自動修正）

`clang-tidy`、C/C++のプログラミングでは、とても便利な静的解析ツールです。
`-fix`や`-fix-errors`オプションをつけて実行すれば、ある程度自動修正してくれる賢さも嬉しいです。

命名規則のチェックや、自動修正に対応していることに気づいたので紹介します。
種類ごとにキャピタライズ(CamelCase,lower_case)や、プレフィクス/サフィックスルールを決められます。

いちおう[ドキュメント](https://clang.llvm.org/extra/clang-tidy/checks/readability-identifier-naming.html)もありますが、指定できるオプションは記載されていませんでした。[テスト](http://llvm.org/svn/llvm-project/clang-tools-extra/trunk/test/clang-tidy/readability-identifier-naming.cpp)を直接見るのが確実です。

`clang-tidy`は、`.clang-tidy`ファイルに設定を書いておくと、デフォルトでそれを使ってくれます。
個別の設定をいちいち引数で指定するのは面倒なので、設定ファイルにまとめて書いておくのがおすすめです。

```yaml:.clang-tidy
Checks: 'readability-identifier-naming'
HeaderFilterRegex: '.*'
CheckOptions:
  - key:             readability-identifier-naming.ClassCase
    value:           CamelCase
  - key:             readability-identifier-naming.EnumCase
    value:           CamelCase
  - key:             readability-identifier-naming.FunctionCase
    value:           camelBack
  - key:             readability-identifier-naming.MemberCase
    value:           lower_case
  - key:             readability-identifier-naming.MemberSuffix
    value:           _
  - key:             readability-identifier-naming.ParameterCase
    value:           lower_case
  - key:             readability-identifier-naming.UnionCase
    value:           CamelCase
  - key:             readability-identifier-naming.VariableCase
    value:           lower_case
```

## 参考メモ
[ソースコード](http://llvm.org/svn/llvm-project/clang-tools-extra/trunk/clang-tidy/readability/IdentifierNamingCheck.cpp)より。

### 対象の種類
複数に当てはまる場合、上のが優先されます。*は複数ヶ所に反映されるもの。なかなか混沌としています。

1. `Typedef`
1. `TypeAlias`
1. 名前空間
  1. `InlineNamespace`
  1. `Namespace`
1. `Enum`*
1. Enum定数
  1. `EnumConstant`
  1. `Constant`*
1. クラス系
  1. `AbstractClass`
  1. `Struct`
  1. `Class`
  1. `Union`
  1. `Enum`*
1. メンバ
  1. `ConstantMember`
  1. `Constant`*
  1. `PrivateMember`
  1. `ProtectedMember`
  1. `PublicMember`
  1. `Member`
1. 引数
  1. `ConstexprVariable`*
  1. `ConstantParameter`
  1. `Constant`*
  1. `ParameterPack`
  1. `Parameter`
1. 変数
  1. const系
     1. `ConstexprVariable`*
     1. `ClassConstant`
     1. `GlobalConstant`
     1. `StaticConstant`
     1. `LocalConstant`
     1. `Constant`*
  1. `ClassMember`
  1. `GlobalVariable`
  1. `StaticVariable`
  1. `LocalVariable`
  1. `Variable`
1. メソッド
  1. `ConstexprMethod`
  1. `ConstexprFunction`*
  1. `ClassMethod`
  1. `VirtualMethod`
  1. `PrivateMethod`
  1. `ProtectedMethod`
  1. `PublicMethod`
  1. `Method`
  1. `Function`*
1. 関数
  1. `ConstexprFunction`*
  1. `GlobalFunction`
  1. `Function`*
1. テンプレート引数(型)
  1. `TypeTemplateParameter`
  1. `TemplateParameter`*
1. テンプレート引数(型以外)
  1. `ValueTemplateParameter`
  1. `TemplateParameter`*
1. テンプレート引数(テンプレート)
  1. `TemplateTemplateParameter`
  1. `TemplateParameter`*
1. 非対応ぽい
  1. `MacroDefinition`
  1. `PureFunction`
  1. `PureMethod`
  1. `TemplateUsing`
  1. `Using`

### キャピタライズの種類

- aNy_CasE
- lower_case
- UPPER_CASE
- camelBack
- CamelCase
- Camel_Snake_Case（アップデートで追加？[^1]）
- camel_Snake_Back（アップデートで追加？[^1]）

[^1]: https://reviews.llvm.org/D21472
