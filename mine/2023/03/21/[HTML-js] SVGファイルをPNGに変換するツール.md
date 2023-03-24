<!--
id: 00fb6548231b2da7ab1a
url: https://qiita.com/tenmyo/items/00fb6548231b2da7ab1a
created_at: 2023-03-21T18:44:28+09:00
updated_at: 2023-03-21T18:44:28+09:00
private: false
coediting: false
tags:
- JavaScript
- HTML5
team: null
-->

# [HTML/js] SVGファイルをPNGに変換するツール

## 背景など

javascriptのキャッチアップ練習です。
指定したSVGファイルをPNGファイルに変換してダウンロードします。

変換用のソフト（ペイント3Dとか）が使えないところでは便利かもしれません。

動かした環境は次の通り。

- Windows 11 Home 22H2
- Microsoft Edge バージョン 111.0.1661.44 (公式ビルド) (64 ビット)

## コード

```html:svg2png.html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>svg2png</title>
    <script>
      document.addEventListener('DOMContentLoaded', (ev) => {
        document
          .querySelector('#file_select_button')
          .addEventListener('change', (ev) => {
            // キャンセルの場合は何もしない
            if (!ev.target.files.length) {
              return;
            }
            // 選んだファイル
            const f = ev.target.files[0];
            // 保存名
            const pngName = f.name + '.png';
            // 画像読み込み用 Image要素
            const imgElement = new Image();
            // 読み込み後処理
            imgElement.onload = (ev) => {
              const img = ev.target;
              // 用済みのオブジェクトURLを解放
              URL.revokeObjectURL(img.src);
              // canvas生成
              const canvas = document.createElement('canvas');
              canvas.width = img.width;
              canvas.height = img.height;
              // canvasにimgを描画
              canvas.getContext('2d').drawImage(img, 0, 0);
              // PNGフォーマットでObjectURLを取得
              canvas.toBlob((blob) => {
                const pngurl = URL.createObjectURL(blob);
                // ダウンロード用にa要素を作成して、押す
                // （直接のダウンロードは行えないので、ダウンロード用リンクを作成しそれを踏む）
                const aElement = document.createElement('a');
                aElement.href = pngurl;
                aElement.download = pngName;
                aElement.dispatchEvent(new MouseEvent('click'));
                URL.revokeObjectURL(pngurl);
              }, 'image/png');
            };
            // ファイルをオブジェクトURLにして読み込み開始
            imgElement.src = URL.createObjectURL(f);
          });
      });
    </script>
  </head>
  <body>
    <input type="file" id="file_select_button" accept="image/svg+xml" />
  </body>
</html>
```

ObjectURLの必要生存期間がよく分からないです。dispatchEvent直後に解放しちゃダメな気もする。
ドラッグ＆ドロップに対応できると、より使い勝手がよさそう。

## 参考

[ウェブアプリケーションからのファイルの使用 - Web API | MDN](https://developer.mozilla.org/ja/docs/Web/API/File_API/Using_files_from_web_applications)
[HTMLCanvasElement.toBlob() - Web API | MDN](https://developer.mozilla.org/ja/docs/Web/API/HTMLCanvasElement/toBlob)
[javascript - Convert SVG to image (JPEG, PNG, etc.) in the browser - Stack Overflow](https://stackoverflow.com/questions/3975499/convert-svg-to-image-jpeg-png-etc-in-the-browser)
[SVG画像をjavascriptでpngに変換してダウンロードする方法](https://zenn.dev/skryo/articles/7d7f1ce601510b)
