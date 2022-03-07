from util.UTbkt import BackTest
from datetime import datetime


# Test: Backtesting: Small
s, e = datetime(2019, 8, 26), datetime(2022, 2, 28)
bt = BackTest(s, e)
a = bt.backtest(on_what='m')
b = bt.get_idx('m', s, e)

for k in a.keys():
    print(a[k]['best'][0])

for k in a.keys():
    print(a[k]['wrst'][0])
