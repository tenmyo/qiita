<!--
id: 4bfc4e9fee4b9c86ee01
url: https://qiita.com/tenmyo/items/4bfc4e9fee4b9c86ee01
created_at: 2023-02-21T22:52:28+09:00
updated_at: 2023-02-22T21:49:00+09:00
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

# [Python] ダウンロードしたくりっく株３６５のヒストリカルデータCSVをマージする

今回は新しめのPythonの練習です。
以下の記事でダウンロードしたCSVデータを、マージするPythonスクリプトを作りました。

[[PADフロー] くりっく株３６５のヒストリカルデータをダウンロードする - Qiita](https://qiita.com/tenmyo/items/b092500b0d84b71b63f4)

元データは複数指数を含んだ１年ごとのファイルになっていますが、指数ごとのファイルにまとめます。
約15か月のリセットが導入されたため、毎年３か月ほど重複期間があります。ここでは後年（Reset Date2022よりReset Date2023）のデータを採用します。
型のアノテーションでSelf（[PEP 673](https://peps.python.org/pep-0673/)）を使っているためPython3.11が必要です。

```python:cfd_merge.py
#!/usr/bin/env python3
# Python 3.11

"""
くりっく株３６５ヒストリカルデータCSVをマージし、指数ごとのCSVを出力します。
コマンド引数: CSVファイルパス...

入力CSV:
期間指定,2023/01/01～2023/12/31
株価指数,"N23/JPY,D23/JPY,Q23/JPY,X23/JPY,F23/JPY,G23/JPY,C23/JPY"
商品名,Product,取引日,前日清算価格,始値,高値,安値,終値,当日清算価格,前日比,金利相当額,配当相当額,取引数量,建玉数量
"日経 225 リセット付証拠金取引（Nikkei 225）2023","Nikkei 225 Daily Futures contract with Reset Date2023",2023/01/03,"25,829","25,974","26,032","25,645","25,881","25,872",43,,,"23,482","59,873"
"日経 225 リセット付証拠金取引（Nikkei 225）2023","Nikkei 225 Daily Futures contract with Reset Date2023",2023/01/04,"25,872","25,893","25,987","25,690","25,920","25,917",45,,,"27,937","61,165"
...

出力位置: 入力CSVの隣の"merged_cfd_csv"ディレクトリ
出力ファイル名: 指数短縮名.csv
出力CSV:
date,prevPrice,open,high,low,close,price,diff,interest,dividends,volume,position
2020-10-26,12670,12429,12430,12097,12186,12186,-484,0,0,159,72
...

特記事項:
取引数量が無いデータは飛ばします。
同じ指数で重複がある場合、新しい指数を優先します。（Reset Date2022よりReset Date2023を優先する）
"""

import csv
import os
import os.path
from collections import defaultdict
from datetime import date
from typing import DefaultDict, NamedTuple, Self

# 指数名寄せ用{Product列の"contract"より前: 名寄せ後の指数短縮名}
PRODUCT = {
    "Nikkei 225 Daily Futures": "Nikkei225",
    "FTSE 100 Daily Futures": "FTSE100",
    "DAX(R) Daily Futures": "DAX",
    "FTSE China 25 Margin": "FTSEChina25",
    "DJIA Daily Futures": "DJIA",
    "Gold ETF Daily Futures": "Gold",
    "WTI ETF Futures": "WTI",
    "NASDAQ-100 Daily Futures": "NASDAQ-100",
}


class Hist(NamedTuple):
    """くりっく株３６５ヒストリカルデータCSVの１行データ"""

    productj: str
    product: str
    date: date
    prevPrice: int
    open: int
    high: int
    low: int
    close: int
    price: int
    diff: int
    interest: int
    dividends: int
    volume: int
    position: int

    @classmethod
    def make(cls, row: list[str]) -> Self:
        """型変換するファクトリメソッド"""
        return cls(
            *row[0:2],
            date.fromisoformat(row[2].replace("/", "-")),
            *[int(e.replace(",", "")) if e else 0 for e in row[3:14]],
        )


def main(argv: list[str]):
    # 全CSVデータ
    data: dict[str, dict[date, Hist]] = {v: dict() for v in PRODUCT.values()}
    # 読み込んだ指数。重複判定用
    processed: dict[str, DefaultDict[date, str]] = {
        v: defaultdict(str) for v in PRODUCT.values()
    }
    # 全ファイル読み込み
    for fpath in argv:
        with open(fpath, mode="r", encoding="cp932") as f:
            reader = csv.reader(f)
            # skip header
            for _ in range(3):
                for _ in reader:
                    break
            # body
            for row in map(Hist.make, reader):
                # skip holiday
                if row.volume == 0:
                    continue
                # 指数の名寄せ。keyが指数名、key2はリセット年など。
                prod = row.product.split(" contrac")
                key, key2 = PRODUCT[prod[0]], prod[1]
                # 重複時は後年の指数（2022->2023）を優先して保持
                if processed[key][row.date] < key2:
                    processed[key][row.date] = key2
                    data[key][row.date] = row
    # 最初のファイルと隣のディレクトリに出力する
    dirpath = (
        os.path.dirname(os.path.dirname(os.path.abspath(argv[0]))) + "/merged_cfd_csv"
    )
    os.makedirs(dirpath, exist_ok=True)
    # 指数ごとに出力（指数短縮名.csv）
    for prod in PRODUCT.values():
        with open(f"{dirpath}\\{prod}.csv", mode="w", encoding="utf8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(Hist._fields[2:])
            for _, hist in sorted(data[prod].items()):
                writer.writerow(hist[2:])


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
```
