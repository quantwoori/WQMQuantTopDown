from dbm.DBmssql import MSSQL
from dbm.DBquant import PyQuantiwise
from rstrct.RSTuniv import UniverseRestrict
from abc import ABC, abstractmethod
from typing import Tuple, List
from datetime import datetime, timedelta


class SmallUniverse(ABC):
    """
    Class Factory Hub of Creating Small Universe
    ----------------------------------------
    >> Universe Size : divided by (IKS002, IKS003, IKS004)
    >> Universe Style : divided by (..., ..., ...)
    """
    server = MSSQL.instance()
    server.login(id='wsol2', pw='wsol2')
    data = PyQuantiwise()
    index_name = {
        'big': 'ksbig',
        'middle': 'ksmid',
        'small': 'kssml',
        '200': 'ks200'
    }
    restriction = UniverseRestrict.kh03

    def __init__(self):
        self.typ = None

    def retrieve_universe(self, year:int, month:int, restriction:bool=True) -> [Tuple]:
        cond = [
            f"year = {year}",
            f"chg_no = {month}",
            f"ind_ = '{self.index_name[self.typ]}'"
        ]
        cond = ' and '.join(cond)
        result = self.server.select_db(
            database='WSOL',
            schema='dbo',
            table='indcomp',
            column=['year', 'chg_no', 'code', 'stk_no', 'ind_'],
            condition=cond
        )

        if restriction is True:
            r = list()
            for y, m, n, stk, idx in result:
                if stk in self.restriction:
                    r.append(
                        (y, m, n, stk, idx)
                    )
            return r
        else:
            return result

    @abstractmethod
    def get_universe(self, *args, **kwargs):
        pass


class UniverseSizeBig(SmallUniverse):
    """
    Factory product
    KOSPI SIZE BIG
    """
    def __init__(self):
        self.typ = 'big'

    def get_universe(self, y:int, m:int, rstrct:bool) -> [Tuple]:
        d = self.retrieve_universe(year=y, month=m, restriction=rstrct)
        return d


class UniverseSizeMiddle(SmallUniverse):
    """
    Factory product
    KOSPI SIZE MIDDLE
    """
    def __init__(self):
        self.typ = 'middle'

    def get_universe(self, y, m, rstrct:bool) -> [Tuple]:
        d = self.retrieve_universe(year=y, month=m, restriction=rstrct)
        return d


class UniverseSizeSmall(SmallUniverse):
    """
    Factory product
    KOSPI SIZE SMALL
    """
    def __init__(self):
        self.typ = 'small'

    def get_universe(self, y, m, rstrct:bool) -> [Tuple]:
        d = self.retrieve_universe(year=y, month=m, restriction=rstrct)
        return d


class UniverseSizeFactory:
    def create_universe(self, size:str):
        cond_s = size == "s"
        cond_m = size == "m"
        cond_b = size == "b"

        if cond_s:
            return UniverseSizeSmall()
        elif cond_m:
            return UniverseSizeMiddle()
        elif cond_b:
            return UniverseSizeBig()


class UniverseStyle(SmallUniverse):

    def __init__(self):
        self.typ = '200'

    def get_universe(self, y:int, m:int, rstrct:bool) -> List:
        """
        TBD
        """
        d = self.retrieve_universe(year=y, month=m, restriction=rstrct)
        d = [r[3] for r in d]

        def get_no_consen(stks, no_consensus:int=0) -> List:
            dt = datetime(year=y, month=m, day=1)
            while True:
                df_cons = self.data.css_data_multi(
                    stock_code_ls=stks,
                    qry_date=dt.strftime('%Y%m%d'),
                    item='투자의견참여증권사'
                )
                df = self.retrieve_universe(year=y, month=m, restriction=False)

                if df_cons.empty:
                    dt += timedelta(days=1)
                else:

                    df_stk = set(df_cons.CMP_CD.tolist())
                    df_miss = [r[3] for r in df if r[3] not in df_stk]  # VAL = 0

                    return df_cons.loc[df_cons.VAL <= no_consensus].CMP_CD.to_list() + df_miss

        return get_no_consen(d)


class UniverseStyleFactory:
    def create_universe(self, style:str):
        cond_consen = style == 'consensus'

        if cond_consen:
            return UniverseStyle()
