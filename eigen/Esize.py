# Custom Package
from univ.Ufac import UniverseSizeFactory
from eigen.E import EigenBackEnd

# Other
import pandas as pd
from datetime import datetime
from typing import Iterable, List


class Eigen(EigenBackEnd):
    def __init__(self, date:datetime, portnumber:int, divide_std:str):
        super().__init__(date, portnumber, divide_std)

        # LOCAL CLASS CONSTANT
        self.DTSET = self.set_dates()

    def set_dates(self) -> (int, int, str, str):
        univ_dt_y, univ_dt_m = self.DT.year, self.DT.month
        if univ_dt_m == 1:
            hist_dt_y = univ_dt_y - 1
            hist_dt_m = 12

            hist_dt_start = f"{hist_dt_y}{hist_dt_m}01"
            hist_dt_end = f"{hist_dt_y + 1}0101"

        else:
            hist_dt_y = univ_dt_y - 1
            hist_dt_m = univ_dt_m - 1

            addzero = lambda x: '0' * (len(str(x)) == 1)

            hist_dt_start = f"{hist_dt_y}{addzero(hist_dt_m)}{str(hist_dt_m)}01"
            hist_dt_end = f"{hist_dt_y}{addzero(hist_dt_m + 1)}{hist_dt_m + 1}01"

        return univ_dt_y, univ_dt_m, hist_dt_start, hist_dt_end

    def get_univ(self, with_restriction:bool=True) -> List:
        univ = UniverseSizeFactory(
        ).create_universe(
            self.STDARD
        ).get_universe(
            self.DT.year, self.DT.month, with_restriction
        )
        return [stk for _, _, _, stk, _ in univ]

    def match_price(self, univ:Iterable) -> pd.DataFrame:
        r = self.qt.stk_data_multi(
            stock_code_ls=univ,
            start_date=self.DTSET[2],
            end_date=self.DTSET[3],
            item='수정시가'
        )
        r.VAL = r.VAL.astype('float64')
        r = r.pivot_table(index='TRD_DT', columns='STK_CD')
        r.columns = [s for _, s in r.columns]
        return r
