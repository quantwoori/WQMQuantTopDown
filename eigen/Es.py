# Custom Package
from univ.Ufac import UniverseSizeFactory
from univ.Ufac import UniverseStyleFactory
from eigen.E import EigenBackEnd

# Other
import pandas as pd
from datetime import datetime, timedelta
from typing import Iterable, List, Dict


class Eigen(EigenBackEnd):
    def __init__(self, date:datetime, portnumber:int, divide_std:str):
        super().__init__(date, portnumber, divide_std)

        # LOCAL CLASS CONSTANT
        self.DTSET = self.set_dates(weekly=True, howmany=15)

    def set_dates(self, weekly:bool=False, howmany:int=None) -> (int, int, str, str):
        univ_dt_y, univ_dt_m = self.DT.year, self.DT.month
        if univ_dt_m == 1:
            if weekly is False:
                hist_dt_y = univ_dt_y - 1
                hist_dt_m = 12

                hist_dt_start = f"{hist_dt_y}{hist_dt_m}01"
                hist_dt_end = f"{hist_dt_y + 1}0101"
            else:
                hist_dt_start = (self.DT - timedelta(days=(howmany + 1))).strftime('%Y%m%d')
                hist_dt_end = (self.DT - timedelta(days=1)).strftime('%Y%m%d')

        else:
            if weekly is False:
                hist_dt_y = univ_dt_y - 1
                hist_dt_m = univ_dt_m - 1

                addzero = lambda x: '0' * (len(str(x)) == 1)

                hist_dt_start = f"{hist_dt_y}{addzero(hist_dt_m)}{str(hist_dt_m)}01"
                hist_dt_end = f"{hist_dt_y}{addzero(hist_dt_m + 1)}{hist_dt_m + 1}01"
            else:
                hist_dt_start = (self.DT - timedelta(days=(howmany + 1))).strftime('%Y%m%d')
                hist_dt_end = (self.DT - timedelta(days=1)).strftime('%Y%m%d')

        return univ_dt_y, univ_dt_m, hist_dt_start, hist_dt_end

    def get_univ(self, standard:str, with_restriction:bool=True) -> List:
        if standard == 'size':
            univ = UniverseSizeFactory(
            ).create_universe(
                self.STDARD
            ).get_universe(
                self.DT.year, self.DT.month, True
            )
            return [stk for _, _, _, stk, _ in univ]

        if standard == 'style':
            univ = UniverseStyleFactory(
            ).create_universe(
                self.STDARD
            ).get_universe(
                self.DT.year, self.DT.month, False
            )
            return univ

    def match_hist_price(self, univ:Iterable) -> pd.DataFrame:
        r = self.qt.stk_data_multi(
            stock_code_ls=univ,
            start_date=self.DTSET[2],
            end_date=self.DTSET[3],
            item='수정시가'
        )
        r.VAL = r.VAL.astype('float64')
        r = r.pivot_table(index='TRD_DT', columns='STK_CD')
        r = r.sort_index()
        r.columns = [s for _, s in r.columns]
        return r

    def match_hist_price_oc(self, univ:Iterable) -> pd.DataFrame:
        ro = self.qt.stk_data_multi(
            stock_code_ls=univ,
            start_date=self.DTSET[2],
            end_date=self.DTSET[3],
            item='수정시가'
        )
        rc = self.qt.stk_data_multi(
            stock_code_ls=univ,
            start_date=self.DTSET[2],
            end_date=self.DTSET[3],
            item='수정주가'
        )
        ro.VAL = ro.VAL.astype('float64')
        rc.VAL = rc.VAL.astype('float64')
        ro = ro.pivot_table(index='TRD_DT', columns='STK_CD')
        rc = rc.pivot_table(index='TRD_DT', columns='STK_CD')

        ro, rc = ro.sort_index(), rc.sort_index()
        r = pd.concat([ro, rc[len(ro)-1:]])  # ~ last day:open
        r.columns = [s for _, s in r.columns]
        return r

    def match_futr_price(self, univ:Iterable) -> pd.DataFrame:
        r = self.qt.stk_data_multi(
            stock_code_ls=univ,
            start_date=self.DTSET[0],
            end_date=self.DTSET[1],
            item='수정시가'
        )
        r.VAL = r.VAL.astype('float64')
        r = r.pivot_table(index='TRD_DT', columns='STK_CD')
        r = r.sort_index()
        r.columns = [s for _, s in r.columns]
        return r

    def choose_eigp(self, histprc:pd.DataFrame, weights:pd.DataFrame) -> Dict:
        histprc = histprc.bfill()
        mrtn0 = histprc[:1]
        mrtn1 = histprc[len(histprc)-1:]
        mrtn = pd.concat([mrtn0, mrtn1]).pct_change().dropna().transpose()
        mrtn = mrtn[mrtn.columns[0]]

        s = list()
        for cols in weights.columns:
            r = pd.concat([weights[cols], mrtn], axis=1)
            r.columns = ['weight', 'mrtn']
            hist_rtn = (r['weight'] * r['mrtn']).sum()

            s.append(hist_rtn)

        result = {
            'best': (max(s), weights[weights.columns[s.index(max(s))]]),
            'wrst': (min(s), weights[weights.columns[s.index(min(s))]]),
        }
        return result
