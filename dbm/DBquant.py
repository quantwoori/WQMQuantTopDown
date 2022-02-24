from cfgr.Cquant import Stock, Consensus, Indice
from dbm.DBmssql import MSSQL
from typing import Iterable
import pandas as pd


class PyQuantiwise:
    """
    PyQuantiwise Module 2.0
    ==============================
    Do without .csv files stored in raw data.

    Dependencies reduced to only
        cfgr.Cquant > Stock, Consensus, Indice
        dbm.DBmssql > MSSQL

    Unit Tests at
        test > TDBquant.py

    Current Support upto
        Single, Multiple Stock information requests
        Single, Multiple Indices information requests

    Currently Under Development
        Single, Multiple Consensus items.
    """
    def __init__(self):
        self.server = MSSQL().instance()
        self.server.login(
            id='wsol1',
            pw='wsol1'
        )

        # IMMUTABLE
        self.STK = self.__get_cols('WFNS2DB', 'TS_STK_DATA')
        self.IND = self.__get_cols('WFNS2DB', 'TS_IDX_DATA')
        self.CSS = self.__get_cols('WFNR2DB', 'TT_CMP_CNS_DATA')

        self.STKESS = ['TRD_DT', 'STK_CD', 'VAL']
        self.INDESS = ['TRD_DT', 'SEC_CD', 'VAL']
        self.CSSESS = ['CNS_DT', 'CMP_CD', 'VAL']

    def __version__(self):
        return "PyQuantiwise 2.0.0"

    def __get_cols(self, database:str, table:str):
        col = self.server.get_columns(
            database=database,
            table_name=table,
            schema='dbo'
        )
        return col

    def stk_data(self, stock_code:str, start_date:str, end_date:str,
                 item:str, tablename='TS_STK_DATA') -> pd.DataFrame:
        assert len(start_date) == 8, "start_date out of range"
        assert len(end_date) == 8, "end_date out of range"
        assert item in Stock.QRY_CODE.keys(), "item out of range"

        item_code = Stock.QRY_CODE[item][0]
        restrict = [
            f"STK_CD = '{stock_code}'",
            f"ITEM_CD = '{item_code}'",
            f"ITEM_TYP = 'S'",
            f"TRD_DT >= '{start_date}'",
            f"TRD_DT <= '{end_date}'",
        ]
        restrict = ' and '.join(restrict)

        res = self.server.select_db(
            database='WFNS2DB',
            schema='dbo',
            table=tablename,
            column=self.STK,
            condition=restrict
        )
        res = pd.DataFrame(res, columns=self.STK)
        return res[self.STKESS]

    @staticmethod
    def __multi_qry(ls:Iterable, typ:str) -> str:
        result = list()
        if typ == 'S':
            for i in ls:
                result.append(
                    f"STK_CD = '{i}'"
                )
        else:
            for i in ls:
                result.append(
                    f"SEC_CD = '{i}'"
                )
        return f"({' or '.join(result)})"

    def stk_data_multi(self, stock_code_ls:Iterable, start_date:str, end_date:str,
                       item:str, tablename='TS_STK_DATA') -> pd.DataFrame:
        assert len(start_date) == 8, "start_date out of range"
        assert len(end_date) == 8, "end_date out of range"
        assert item in Stock.QRY_CODE.keys(), "item out of range"

        item_code = Stock.QRY_CODE[item][0]
        restrict = [
            self.__multi_qry(ls=stock_code_ls, typ='S'),
            f"ITEM_CD = '{item_code}'",
            f"ITEM_TYP = 'S'",
            f"TRD_DT >= '{start_date}'",
            f"TRD_DT <= '{end_date}'",
        ]
        restrict = ' and '.join(restrict)

        res = self.server.select_db(
            database='WFNS2DB',
            schema='dbo',
            table=tablename,
            column=self.STK,
            condition=restrict
        )
        res = pd.DataFrame(res, columns=self.STK)
        return res[self.STKESS]

    def ind_data(self, index_code:str, start_date:str, end_date:str,
                 item:str, tablename='TS_IDX_DATA') -> pd.DataFrame:
        assert len(start_date) == 8, "start_date out of range"
        assert len(end_date) == 8, "end_date out of range"
        assert item in Indice.QRY_CODE.keys(), "item out of range"

        item_code = Indice.QRY_CODE[item][0]
        restrict = [
            f"SEC_CD = '{index_code}'",
            f"ITEM_CD = '{item_code}'",
            f"FRQ_TYP = 1",  # Daily,
            f"ITEM_TYP = 'I'",
            f"TRD_DT >= '{start_date}'",
            f"TRD_DT <= '{end_date}'",
        ]
        restrict = ' and '.join(restrict)
        res = self.server.select_db(
            database='WFNS2DB',
            schema='dbo',
            table=tablename,
            column=self.IND,
            condition=restrict
        )
        res = pd.DataFrame(res, columns=self.IND)
        return res[self.INDESS]

    def ind_data_multi(self, index_code_ls:Iterable, start_date:str, end_date:str,
                       item:str, tablename='TS_IDX_DATA') -> pd.DataFrame:
        assert len(start_date) == 8, "start_date out of range"
        assert len(end_date) == 8, "end_date out of range"
        assert item in Indice.QRY_CODE.keys(), "item out of range"

        item_code = Indice.QRY_CODE[item][0]
        restrict = [
            self.__multi_qry(ls=index_code_ls, typ='I'),
            f"ITEM_CD = '{item_code}'",
            f"FRQ_TYP = 1",
            f"ITEM_TYP = 'I'",
            f"TRD_DT >= '{start_date}'",
            f"TRD_DT <= '{end_date}'",
        ]
        restrict = ' and '.join(restrict)

        res = self.server.select_db(
            database='WFNS2DB',
            schema='dbo',
            table=tablename,
            column=self.IND,
            condition=restrict
        )
        res = pd.DataFrame(res, columns=self.IND)
        return res[self.INDESS]

    def css_data(self, index_code:str, start_date:str, end_date:str,
                 item:str, tablename='TT_CMP_CNS_DATA') -> pd.DataFrame:
        assert len(start_date) == 8, "start_date out of range"
        assert len(end_date) == 8, "end_date out of range"
        assert item in Consensus.QRY_CODE.keys(), 'item out of range'

        raise NotImplementedError
