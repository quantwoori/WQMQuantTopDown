# Custom Package
from dbm.DBquant import PyQuantiwise
from eigen.Es import Eigen

# Other
import pandas as pd
from typing import Tuple, Dict, Iterable
from datetime import datetime, timedelta


class BackTest:
    def __init__(self, start_date:datetime, end_date:datetime, portnum:int=1):
        # CLASS MODULES
        self.qt = PyQuantiwise()

        # IMMUTABLE CLASS CONSTANT
        self.START, self.END = start_date, end_date
        self.PORTCOUNT = portnum

    def set_dates(self) -> [Tuple]:
        """
        Retrieve every (year,month) combination from start date to end date
        """
        sy, sm = self.START.year, self.START.month
        ey, em = self.END.year, self.END.month

        result = list()
        for y in range(sy, ey + 1):
            if y == sy:
                for m in range(sm, 12 + 1):
                    result.append(
                        (y, m)
                    )
            elif y < ey:
                for m in range(1, 12 + 1):
                    result.append(
                        (y, m)
                    )
            else:
                for m in range(1, em + 1):
                    result.append(
                        (y, m)
                    )
        return result

    def backtest(self, on_typ:str, on_what:str):
        date_ls = self.set_dates()
        result = dict()
        for y, m in date_ls:
            print(y, m)
            d = datetime(year=y, month=m, day=1)
            e = Eigen(date=d,
                      portnumber=self.PORTCOUNT,
                      divide_std=on_what)

            univ = e.get_univ(standard=on_typ)
            prc = e.match_hist_price(univ)
            pf = e.get_eigp(data=prc)
            result[(y, m)] = e.choose_eigp(histprc=prc, weights=pf)
        return result

    def backtest_weekly(self, on_typ:str, on_what:str) -> Dict:
        date_ls = self.set_dates()
        result, result_rtn = dict(), dict()
        (y, m), (ey, em) = date_ls[0], date_ls[-1]
        ds = datetime(year=y, month=m, day=1)
        while True:
            print(ds)
            e = Eigen(date=ds,
                      portnumber=self.PORTCOUNT,
                      divide_std=on_what)
            univ = e.get_univ(standard=on_typ)
            prc = e.match_hist_price_oc(univ)
            pf = e.get_eigp(data=prc)
            result[(ds.year, ds.month, ds.day)] = e.choose_eigp(histprc=prc, weights=pf)

            # Return?
            p = result[(ds.year, ds.month, ds.day)]['best'][1].index.tolist()
            p_rtn = self.get_rtn(p, ds, (ds + timedelta(days=7)))

            result[(ds.year, ds.month, ds.day)]['best'].append(
                (result[(ds.year, ds.month, ds.day)]['best'][1] * p_rtn).sum()
            )
            result[(ds.year, ds.month, ds.day)]['wrst'].append(
                (result[(ds.year, ds.month, ds.day)]['wrst'][1] * p_rtn).sum()
            )

            ds += timedelta(days=7)

            if ds > datetime(year=ey, month=em, day=1):
                break
        return result

    def get_rtn(self, portfolios:Iterable, start_date:datetime, end_date:datetime):
        ro = self.qt.stk_data_multi(
            stock_code_ls=portfolios,
            start_date=start_date.strftime("%Y%m%d"),
            end_date=end_date.strftime('%Y%m%d'),
            item='수정시가'
        )
        rc = self.qt.stk_data_multi(
            stock_code_ls=portfolios,
            start_date=start_date.strftime("%Y%m%d"),
            end_date=end_date.strftime('%Y%m%d'),
            item='수정주가'
        )
        ro.VAL = ro.VAL.astype('float32')
        rc.VAL = rc.VAL.astype('float32')
        ro, rc = ro.sort_index(), rc.sort_index()
        ro = ro.pivot_table(values='VAL', index='TRD_DT', columns='STK_CD')
        rc = rc.pivot_table(values='VAL', index='TRD_DT', columns='STK_CD')

        r = pd.concat([ro[:1], rc[(len(rc) - 1):]])
        r = r.pct_change().dropna().transpose()
        return r[r.columns[0]]

    def get_idx(self, on_what:str, start:str, finish:str):
        assert len(start) == 8, "Check the starting date"
        assert len(finish) == 8, "Check the finishing date"
        idx_strt = {
            's': 'IKS004',
            'm': 'IKS003',
            'b': 'IKS002'
        }
        m = self.qt.ind_data(
            index_code=idx_strt[on_what],
            start_date=start,
            end_date=finish,
            item='시가지수'
        )
        m.VAL = m.VAL.astype('float32')
        return m
