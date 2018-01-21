# %%
# 定義
import math
import typing  # noqa: F401

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 戦略スーパークラス
class Storategy:
    def __init__(self, name, coin):  # type: (str, int) -> None
        self.name = name
        self.coin = coin
        self.next_bet = 0

    def bet(self):  # type: () -> int
        ret = self.next_bet
        self.coin -= ret
        return ret

    def refound(self, coin):  # type: (int) -> int
        self.coin += coin
        self.update(coin)
        return self.coin

    def update(self, coin):  # type: (int) -> None
        pass


# 定額
class FixedAmount(Storategy):
    def __init__(self, name, coin, first_bet):  # type: (str, int, int) -> None
        super().__init__(name, coin)
        self.first_bet = first_bet
        self.update(coin)

    def update(self, coin):  # type: (int) -> None
        self.next_bet = min(self.first_bet, self.coin)


# 定率
class FixedRate(Storategy):
    def __init__(self, name, coin, rate):  # type: (str, int, float) -> None
        super().__init__(name, coin)
        self.rate = rate
        self.update(coin)

    def update(self, coin):  # type: (int) -> None
        self.next_bet = math.floor(self.coin * self.rate)


# マーチンゲール法（負けたら倍賭け）
class Martingale(Storategy):
    def __init__(self, name, coin, first_bet):  # type: (str, int, int) -> None
        super().__init__(name, coin)
        self.first_bet = first_bet
        self.debt = 0
        self.update(coin)

    def update(self, coin):  # type: (int) -> None
        if coin == 0:
            self.next_bet *= 2
        else:
            self.next_bet = self.first_bet + self.debt
            self.debt = 0
        if self.next_bet > self.coin:
            self.debt = self.next_bet - self.coin
            self.next_bet = self.coin


# 勝敗（払い戻し率）リスト生成
def winning_list(winning_persentage, odds,
                 k):  # type: (float, float, int) -> np.ndarray[float]
    win = int(k * winning_persentage)
    ary = np.concatenate((np.full(win, odds),
                          np.zeros(k - win)))  # type: np.ndarray[float]
    np.random.shuffle(ary)
    return ary


# シミュレーション実施
def simulate(start_coin, num_rounds, winning_persentage, odds,
             k):  # type: (int, int, float, float, int) -> pd.DataFrame
    np.random.seed(1)  # 再現可能にする
    df = pd.DataFrame(columns=['name', 'round', 'count', 'coin'])
    for round in range(num_rounds):
        strategies = (
            FixedAmount('定額(300)', start_coin, 300),
            FixedAmount('定額(100)', start_coin, 100),
            FixedRate('定率(3%)', start_coin, 0.03),
            FixedRate('定率(1%)', start_coin, 0.01),
            Martingale('マーチンゲール(10開始)', start_coin, 10),
            Martingale('マーチンゲール(2開始)', start_coin, 2),
        )  # type: typing.Sequence[Storategy]
        wl = winning_list(winning_persentage, odds, k)

        for strategy in strategies:
            history = [strategy.coin]
            for result_odds in wl:
                bet_coin = strategy.bet()
                refound_coin = bet_coin * result_odds
                strategy.refound(refound_coin)
                history.append(strategy.coin)
            df_one = pd.DataFrame([
                np.full(len(history), strategy.name),
                np.full(len(history), round),
                np.arange(len(history)), history
            ]).T
            df_one.columns = df.columns
            df = df.append(df_one)
    return df.astype({'round': int, 'count': int, 'coin': int})


def save_plot(df, fname,
              save_rounds):  # type: (pd.DataFrame, str, int) -> None
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(16, 6 * math.ceil(save_rounds / 2)))
    for round in range(save_rounds):
        ax = fig.add_subplot(math.ceil(save_rounds / 2), 2, round + 1)
        for name in df['name'].unique():
            df_one = df[(df['name'] == name) & (df['round'] == round)]
            ax.plot(df_one['count'], df_one['coin'], label=name)
        ax.legend()
        ax.set_title(f'Round {round + 1}')
    fig.savefig(fname, bbox_inches='tight')
    fig.show()


def save_hist(df, fname):  # type: (pd.DataFrame, str) -> None
    plt.style.use('ggplot')
    storategy_names = df['name'].unique()
    num_charts = len(storategy_names)
    k = df['count'].max()
    fig = plt.figure(figsize=(16, 6 * math.ceil(num_charts / 2)))
    for i, storategy_name in enumerate(storategy_names, 1):
        ax = fig.add_subplot(math.ceil(num_charts / 2), 2, i)
        df_one = df[(df['name'] == storategy_name) & (df['count'] == k)]
        ax.hist(df_one['coin'], bins=20)
        ax.set_title(storategy_name)
    fig.savefig(fname, bbox_inches='tight')
    fig.show()


# %%
# 50%
# シミュレート
num_rounds = 100
k = 1000
per = 50
df = simulate(
    start_coin=10000,
    num_rounds=num_rounds,
    winning_persentage=per/100,
    odds=2,
    k=k)
# 保存
save_plot(df, f'{per}-plot.png', 4)
save_hist(df, f'{per}-hist.png')
df[(df['count'] == k)].groupby('name')[(
    'name', 'coin')].describe().round(1).T.to_csv(f'{per}.csv')


# %%
# 48%
# シミュレート
num_rounds = 100
k = 1000
per = 48
df = simulate(
    start_coin=10000,
    num_rounds=num_rounds,
    winning_persentage=per/100,
    odds=2,
    k=k)
# 保存
save_plot(df, f'{per}-plot.png', 4)
save_hist(df, f'{per}-hist.png')
df[(df['count'] == k)].groupby('name')[(
    'name', 'coin')].describe().round(1).T.to_csv(f'{per}.csv')


# %%
# 52%
# シミュレート
num_rounds = 100
k = 1000
per = 52
df = simulate(
    start_coin=10000,
    num_rounds=num_rounds,
    winning_persentage=per/100,
    odds=2,
    k=k)
# 保存
save_plot(df, f'{per}-plot.png', 4)
save_hist(df, f'{per}-hist.png')
df[(df['count'] == k)].groupby('name')[(
    'name', 'coin')].describe().round(1).T.to_csv(f'{per}.csv')
