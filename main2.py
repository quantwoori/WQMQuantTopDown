from util.UTbkt import BackTest
from datetime import datetime


if __name__ == "__main__":
    s, e = datetime(2020, 1, 1), datetime(2022, 2, 28)
    sstr, estr = s.strftime('%Y%m%d'), e.strftime('%Y%m%d')
    bt = BackTest(s, e)

    # Big
    resultb = bt.backtest_weekly(on_what='b')
    bb, bw = list(), list()
    for k in resultb.keys():
        bb.append(resultb[k]['best'][0])
        bw.append(resultb[k]['wrst'][0])

    # Middle
    resultm = bt.backtest_weekly(on_what='m')
    mb, mw = list(), list()
    for k in resultm.keys():
        mb.append(resultm[k]['best'][0])
        mw.append(resultm[k]['wrst'][0])

    # Small
    results = bt.backtest_weekly(on_what='s')
    sb, sw = list(), list()
    for k in results.keys():
        sb.append(results[k]['best'][0])
        sw.append(results[k]['wrst'][0])

    # Index
    idxb = bt.get_idx('b', sstr, estr)
    idxm = bt.get_idx('m', sstr, estr)
    idxs = bt.get_idx('s', sstr, estr)
