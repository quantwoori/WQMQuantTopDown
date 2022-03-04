# Custom Package
from dbm.DBquant import PyQuantiwise
from eigen.Esize import Eigen

# Other
import pandas as pd

from typing import Tuple
from datetime import datetime


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
            pf = e.get_eigp(
                data=e.match_hist_price(univ)
            )
            result[(y, m)] = e.choose_eigp(histprc=prc, weights=pf)
        return result

    def get_idx(self, on_what:str):
        idx_strt = {
            's': 'IKS004',
            'm': 'IKS003',
            'b': 'IKS002'
        }
        m = self.qt.ind_data(
            index_code=idx_strt[on_what],
            start_date='20210101',
            end_date='20210201',
            item='종가지수'
        )
        m.VAL = m.VAL.astype('float32')
        return m
