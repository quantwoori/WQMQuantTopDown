from util.UTbkt import BackTest
from datetime import datetime
import pandas as pd


if __name__ == "__main__":
    s, e = datetime(2020, 1, 1), datetime(2022, 2, 28)
    sstr, estr = s.strftime('%Y%m%d'), e.strftime('%Y%m%d')
    bt = BackTest(s, e)

    # No or Little Consensus
    resultb = bt.backtest_weekly(on_typ='style', on_what='consensus')
    bb, bw = list(), list()
    bbdf, bwdf = pd.DataFrame(None), pd.DataFrame(None)
    for k in resultb.keys():
        bb.append(resultb[k]['best'][0])
        bw.append(resultb[k]['wrst'][0])

        bbdf = pd.concat([bbdf, resultb[k]['best'][1]], axis=1)
        bwdf = pd.concat([bwdf, resultb[k]['wrst'][1]], axis=1)

    bbdf.columns = list(resultb.keys())
    bwdf.columns = list(resultb.keys())

    bbdf.to_csv('bbdf.csv')
    bwdf.to_csv('bwdf.csv')

    # Index


