from util.UTbkt import BackTest
from datetime import datetime
import pandas as pd


if __name__ == "__main__":
    s, e = datetime(2020, 1, 1), datetime(2022, 2, 28)
    sstr, estr = s.strftime('%Y%m%d'), e.strftime('%Y%m%d')
    bt = BackTest(s, e)

    # No or Little Consensus
    resultb, resulti = bt.backtest_weekly(on_typ='style', on_what='consensus')
    bb, bw, irtn = list(), list(), list()
    bbdf, bwdf = pd.DataFrame(None), pd.DataFrame(None)
    for k in resultb.keys():
        bb.append(resultb[k]['best'][2])
        bw.append(resultb[k]['wrst'][2])
        irtn.append(resulti[k])

        bbdf = pd.concat([bbdf, resultb[k]['best'][1]], axis=1)
        bwdf = pd.concat([bwdf, resultb[k]['wrst'][1]], axis=1)

    bbdf.columns = list(resultb.keys())
    bwdf.columns = list(resultb.keys())

    bbdf.to_csv('bbdf.csv')
    bwdf.to_csv('bwdf.csv')

    # Return
    bbw = pd.DataFrame([bb, bw, irtn]).transpose()
    bbw.index = list(resultb.keys())
    bbw.index = [f"{datetime(y, m, d).strftime('%Y%m%d')}" for y, m, d in bbw.index]


