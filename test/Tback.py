from util.UTbkt import BackTest
from datetime import datetime


# Test: Backtesting: Small
s, e = datetime(2019, 12, 26), datetime(2022, 2, 28)
bt = BackTest(s, e)
a = bt.backtest(on_what='b')
b = bt.get_idx(on_what='b')

for k in a.keys():
    print(a[k]['best'][0])

for k in a.keys():
    print(a[k]['wrst'][0])
