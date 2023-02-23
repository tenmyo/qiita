<!--
id: 6700b8459c81bdf24e1f
url: https://qiita.com/tenmyo/items/6700b8459c81bdf24e1f
created_at: 2023-02-23T00:13:17+09:00
updated_at: 2023-02-23T20:52:11+09:00
private: false
coediting: false
tags:
- Python
- Finance
- 投資
- ヒストリカルデータ
- くりっく株３６５
team: null
-->

# [Python] くりっく株３６５ヒストリカルデータを解析する（リピート注文）

以下の記事でマージしたヒストリカルデータCSVを解析します。
リピート注文[^1]検討用のデータ作りです。
指値でリピート注文した場合の、リワード/リスクや注文間隔を調べます。
元データが日足だったり解析が荒かったりするので厳密さはないですが、ざっと見る分には十分じゃないでしょうか。

[^1]: これ→[マネースクエアCFDでリピートイフダン｜マネースクエア](https://www.m2j.co.jp/cfd/repeat-ifdone)

[[Python] ダウンロードしたくりっく株３６５のヒストリカルデータCSVをマージする - Qiita](https://qiita.com/tenmyo/items/4bfc4e9fee4b9c86ee01)

## 利用例

今回作ったデータで、本当はPowerBIの練習したかったのですが、アカウント云々の仕組みがよく分からなくて断念しました。残念。

以下はGoogleスプレッドシートで分析した例です。
target_priceが買い指値、Int, Rew, Riskは次に買えるまでの日数, そこまでの上昇幅, 下落幅です。
COUNT(指値を下から上抜けた回数), MED(中央値), Ave(平均), Q1(25パーセンタイル)。

![sheet.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/142637/e8465ff0-21f7-c7b7-e79f-27bbe5bfd1e6.png)

たとえば、2002年にリピートイフダンを新規買い27000円、決済売り27227円(27000 + Rew_MED:227)で注文していた場合。
(47(COUNT) * (2/4)) * 227(Rew_MID) でおよそ5300値幅分の益（注文数量100なので53万円の決済益）。
最大含み損がRisk_MAX: 2375（約24万円）。

また決済売りを27096円（27000 + Rew_Q1:96）の場合。
(47(COUNT) * (3/4)) * 96(Rew_Q1) でおよそ3384値幅分の益（約33万円の決済益）。

というあたりが読み取れます。

いろいろ検討のし甲斐があります。jupyterやpandasでもできると楽しそうですね。

## コード

始値→高値→安値→終値　と推移させています。（ただし高値/安値の順番は終値に応じてを変えています）
日経255を想定し、8000～31000買いを100刻みで調べています。今回はハードコードです。
わりと愚直な実装ですが、意外にも10年超の日足４本値でも瞬時に終わりました。

```python
#!/usr/bin/env python3
"""
ヒストリカルデータCSVを分析します。
指値でリピート注文した場合の、リワード/リスクや注文間隔を調べます。

コマンド引数: CSVファイルパス...

入力CSV:
date,prevPrice,open,high,low,close,price,diff,interest,dividends,volume,position
2020-10-26,12670,12429,12430,12097,12186,12186,-484,0,0,159,72
...

出力位置: 元ファイルと同じ
出力ファイル: 元ファイル名_.csv
出力CSV:
date,target_price,reward,risk,interval
2021-03-05,28700,923,-17,3
2021-03-08,28700,1841,-294,17
2021-03-25,28700,1615,-214,27
...
"""
import csv
import datetime
import itertools
import os.path
import typing


class Hist(typing.NamedTuple):
    date: datetime.date
    price: int


def main(argv: list[str]):
    # 全ファイル読み込み
    for fpath in argv:
        # 読み込み
        hists: list[Hist] = []  # ４本値を１本にして持つ
        with open(fpath, mode="r", encoding="utf8") as f:
            reader = csv.reader(f)
            # skip header
            for _ in reader:
                break
            # body
            for row in reader:
                date = datetime.date.fromisoformat(row[0])
                o, h, l, c = [int(e) for e in row[2:6]]
                hists.append(Hist(date, o))
                # 差の少ない並びにする
                if o < c:
                    hists.append(Hist(date, l))
                    hists.append(Hist(date, h))
                else:
                    hists.append(Hist(date, h))
                    hists.append(Hist(date, l))
                hists.append(Hist(date, c))
        # 書き出し
        with open(
            f"{os.path.splitext(fpath)[0]}_.csv",
            mode="w",
            encoding="utf8",
            newline="",
        ) as f:
            writer = csv.writer(f)
            writer.writerow("date target_price reward risk interval".split())
            # 解析
            # TODO: 調査の対象範囲は引数で与える
            for target_price in range(8000, 31000, 100):
                longs = [
                    b_i
                    for (_a_i, a_hist), (b_i, b_hist) in itertools.pairwise(
                        enumerate(hists)
                    )
                    if a_hist.price <= target_price < b_hist.price
                ]
                for i, j in itertools.pairwise(longs):
                    histi, histj = hists[i], hists[j]
                    prices = [h.price for h in hists[i:j]]
                    writer.writerow(
                        [
                            histi.date.isoformat(),
                            target_price,
                            max(prices) - target_price,
                            min(prices) - target_price,
                            (histj.date - histi.date).days,
                        ]
                    )


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
```
