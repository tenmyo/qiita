# Qiita

[Qiita投稿](https://qiita.com/tenmyo)の原稿。

## License

別途記載無い場合、投稿記事内の長いコードはzlibライセンスやBoostライセンスでご利用できます。短いコードは著作権を主張できないと考えてますのでご自由にどうぞ。

## 運用メモ

Visual Studio CodeとDev Containerを前提とします。

Qiitaとの連携は、[qiitactl](https://github.com/minodisk/qiitactl)を使います。
API経由だと更新ログ（更新内容のコメント）が書けないため、pullでのみ（fetchのみ）使います。
`.env`には`QIITA_ACCESS_TOKEN`に加えて`TZ=Asia/Tokyo`も書いておくと、ファイル先頭のメタデータの時刻が分かりやすいです。

1. `qiitactl fetch posts`でpullする
1. ファイルを作ったり書き換えたりする
1. コミットする
1. ファイルの内容をコピーしてブラウザから投稿/更新する
1. `qiitactl fetch post --id=...`でpullする
1. コミットする（--amendでもよいかも？）
