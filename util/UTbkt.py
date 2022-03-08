# Custom Package
from dbm.DBquant import PyQuantiwise
from eigen.Esize import Eigen

# Other
from typing import Tuple
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

    def backtest(self, on_what:str):
        date_ls = self.set_dates()
        result = dict()
        for y, m in date_ls:
            print(y, m)
            d = datetime(year=y, month=m, day=1)
            e = Eigen(date=d,
                      portnumber=self.PORTCOUNT,
                      divide_std=on_what)

            univ = e.get_univ()
            prc = e.match_hist_price(univ)
            pf = e.get_eigp(data=prc)
            result[(y, m)] = e.choose_eigp(histprc=prc, weights=pf)
        return result

    def backtest_weekly(self, on_what:str):
        date_ls = self.set_dates()
        result = dict()
        (y, m), (ey, em) = date_ls[0], date_ls[-1]
        ds = datetime(year=y, month=m, day=1)
        while True:
            print(ds)
            e = Eigen(date=ds,
                      portnumber=self.PORTCOUNT,
                      divide_std=on_what)
            univ = e.get_univ()
            prc = e.match_hist_price(univ)
            pf = e.get_eigp(data=prc)
            result[(ds.year, ds.month, ds.day)] = e.choose_eigp(histprc=prc, weights=pf)
            ds += timedelta(days=7)

            if ds > datetime(year=ey, month=em, day=1):
                break
        return result

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
