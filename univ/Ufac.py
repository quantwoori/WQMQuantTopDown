from dbm.DBmssql import MSSQL
from rstrct.RSTuniv import UniverseRestrict
from abc import ABC, abstractmethod
from typing import Tuple


class SmallUniverse(ABC):
    """
    Class Factory Hub of Creating Small Universe
    ----------------------------------------
    >> Universe Size : divided by (IKS002, IKS003, IKS004)
    >> Universe Style : divided by (..., ..., ...)
    """
    server = MSSQL.instance()
    server.login(id='wsol2', pw='wsol2')
    index_name = {
        'big': 'ksbig',
        'middle': 'ksmid',
        'small': 'kssml'
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
    def get_universe(self):
        """
        TBD
        """
        return None

