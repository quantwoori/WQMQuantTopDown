from util.UTbkt import BackTest
from datetime import datetime
import pandas as pd


if __name__ == "__main__":
    s, e = datetime(2020, 1, 1), datetime(2022, 2, 28)
    sstr, estr = s.strftime('%Y%m%d'), e.strftime('%Y%m%d')
    bt = BackTest(s, e)

    # Big
    resultb = bt.backtest_weekly(on_what='b')
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

    # Middle
    resultm = bt.backtest_weekly(on_what='m')
    mb, mw = list(), list()
    mbdf, mwdf = pd.DataFrame(None), pd.DataFrame(None)
    for k in resultm.keys():
        mb.append(resultm[k]['best'][0])
        mw.append(resultm[k]['wrst'][0])

        mbdf = pd.concat([mbdf, resultm[k]['best'][1]], axis=1)
        mwdf = pd.concat([mwdf, resultm[k]['wrst'][1]], axis=1)

    mbdf.columns = list(resultm.keys())
    mwdf.columns = list(resultm.keys())

    mbdf.to_csv('mbdf.csv')
    mwdf.to_csv('mwdf.csv')

    # Small
    results = bt.backtest_weekly(on_what='s')
    sb, sw = list(), list()
    sbdf, swdf = pd.DataFrame(None), pd.DataFrame(None)
    for k in results.keys():
        sb.append(results[k]['best'][0])
        sw.append(results[k]['wrst'][0])

        sbdf = pd.concat([sbdf, results[k]['best'][1]], axis=1)
        swdf = pd.concat([swdf, results[k]['wrst'][1]], axis=1)

    sbdf.columns = list(resultm.keys())
    swdf.columns = list(resultm.keys())

    sbdf.to_csv('sbdf.csv')
    swdf.to_csv('swdf.csv')

    # Index
    idxb = bt.get_idx('b', sstr, estr)
    idxm = bt.get_idx('m', sstr, estr)
    idxs = bt.get_idx('s', sstr, estr)
