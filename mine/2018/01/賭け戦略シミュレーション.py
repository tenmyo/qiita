#%%
import numpy as np
import seaborn as sns
import math
from pprint import pprint as pp

%matplotlib inline
sns.set(style='ticks', font=['Myrica M'])


# 定額
class FixedAmount:
    def __init__(self, name, coin, first_bet):
        self.name = name
        self.coin = coin
        self.first_bet = first_bet
        self.next_bet = first_bet
        self.history = [coin]

    def refound(self, coin):
        self.coin += coin
        self.next_bet = min(self.first_bet, self.coin)
        self.history.append(self.coin)

    def bet(self):
        self.coin -= self.next_bet
        return self.next_bet


# 定率
class FixedRate:
    def __init__(self, name, coin, rate):
        self.name = name
        self.coin = coin
        self.rate = rate
        self.next_bet = math.floor(self.coin * self.rate)
        self.history = [coin]

    def refound(self, coin):
        self.coin += coin
        self.next_bet = math.floor(self.coin * self.rate)
        self.history.append(self.coin)

    def bet(self):
        self.coin -= self.next_bet
        return self.next_bet


# マーチンゲール法（負けたら倍賭け）
class Martingale:
    def __init__(self, name, coin, first_bet):
        self.name = name
        self.coin = coin
        self.first_bet = first_bet
        self.next_bet = first_bet
        self.history = [coin]

    def refound(self, coin):
        self.coin += coin
        if coin == 0:
            self.next_bet *= 2
        else:
            self.next_bet = self.first_bet
        self.next_bet = min(self.next_bet, self.coin)
        self.history.append(self.coin)

    def bet(self):
        self.coin -= self.next_bet
        return self.next_bet


def winning_list(winning_persentage, k):
    return np.random.choice(2, k, p=(1-winning_persentage, winning_persentage))

START_COIN = 10000
K = 1000
strategies = (
    FixedAmount('定額(300)', START_COIN, 300),
    FixedAmount('定額(100)', START_COIN, 100),
    FixedRate('定率(3%)', START_COIN, 0.03),
    FixedRate('定率(1%)', START_COIN, 0.01),
    Martingale('マーチンゲール(10開始)', START_COIN, 10),
    Martingale('マーチンゲール(2開始)', START_COIN, 2),
)

wl = winning_list(0.5, K)
losses = 0
max_losses = 0
for result in wl:
    if result:
        losses = 0
    else:
        losses += 1
    max_losses = max(losses, max_losses)
    for strategy in strategies:
        bet_coin = strategy.bet()
        refound_coin = (0, bet_coin * 2)[result]
        strategy.refound(refound_coin)

x = np.arange(0, K+1)
fig = sns.mpl.pyplot.figure()
fig.clear()
ax = fig.add_subplot(111)
ax.clear()
for strategy in strategies:
    ax.plot(x, np.asarray(strategy.history, dtype=np.int32), label=strategy.name)
ax.legend()
print('勝ち{}/{} 連続負け{}'.format(sum(wl), K, max_losses))
