<!--
id: 6700b8459c81bdf24e1f
url: https://qiita.com/tenmyo/items/6700b8459c81bdf24e1f
created_at: 2023-02-23T00:13:17+09:00
updated_at: 2023-02-23T00:13:17+09:00
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

[^1]: これ→[マネースクエアCFDでリピートイフダン｜マネースクエア](https://www.m2j.co.jp/cfd/repeat-ifdone)

[[Python] ダウンロードしたくりっく株３６５のヒストリカルデータCSVをマージする - Qiita](https://qiita.com/tenmyo/items/4bfc4e9fee4b9c86ee01)

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
