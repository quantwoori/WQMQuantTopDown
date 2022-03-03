import pymssql
import pandas as pd

from typing import Iterable, List, Dict
import datetime
import json


class MSSQL:
    @classmethod
    def __get_instance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kwargs):
        """
        Singleton. Sync Memory
        """
        cls.__instance = cls(*args, **kwargs)
        cls.instance = cls.__get_instance
        return cls.__instance

    def __init__(self, ip="172.29.1.6"):
        self.address = ip

    def login(self, **kwargs):
        """
        :param kwargs: include set of 'id' 'pw' or include only 'config'
        :return: conn object
        """
        if ('id' in kwargs.keys()) and ('pw' in kwargs.keys()):  # Login with ID and PW
            id = kwargs['id']
            pw = kwargs['pw']

        elif 'config' in kwargs.keys():  # Login with config json
            # The db.json file will already be inside the security dir
            loc = f"../security/{kwargs['config']}.json"
            with open(loc, 'r') as file:
                idpw = json.load(file)['mssql']
                id, pw = list(idpw.items())[0]

        self.conn = pymssql.connect(
            server=self.address,
            user=id,
            password=pw
        )

    @staticmethod
    def _variable_creater(realtime:bool, varname_ls=None, vartype_ls=None) -> Dict:
        """
        If realtime is True = You type as you go along
        Else = Predesignated varname_ls, and vartype_ls required
        :return: Returns dictionary of {Variable : Variable Type}
        """
        if realtime is True:
            print("Type the length of target column")
            l = int(input())
            var = dict()
            for i in range(l):
                print("Type Varname")
                k = input()
                print("Type Vartype")
                t = input()
                var[k] = t
            return var
        else:
            assert (varname_ls is not None) and (vartype_ls is not None)
            assert len(varname_ls) == len(vartype_ls), \
                f"Varname({len(varname_ls)}) or Vartype({len(vartype_ls)}) missing"
            return {k: v for k, v in zip(varname_ls, vartype_ls)}

    def get_tablename(self, database):
        announce = f"use {database};"
        qry = f"""
        select TABLE_NAME, TABLE_SCHEMA 
        from INFORMATION_SCHEMA.TABLES 
        where TABLE_TYPE='BASE TABLE'"""

        c = self.conn.cursor()
        c.execute(announce)
        c.execute(qry)
        r = c.fetchall()
        c.close()
        return pd.DataFrame(r, columns=['name', 'schema'])

    def get_columns(self, table_name, database, schema) -> List:
        announce = f"use {database};"
        qry = \
            f"""
            select COLUMN_NAME, * from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{table_name}'
            """
        if schema != '':
            qry = f"{qry} and TABLE_SCHEMA = '{schema}'"

        c = self.conn.cursor()
        c.execute(announce)
        c.execute(qry)
        r = c.fetchall()
        c.close()
        return [_[0] for _ in r]

    def drop_table(self, table_name, database, schema) -> None:
        qry = f"Drop table {database}.{schema}.{table_name}"

        c = self.conn.cursor()
        c.execute(qry)
        self.conn.commit()
        c.close()

    def create_table(self, table_name:str, variables:dict, database:str) -> None:
        announce = f"use {database}"
        new_cols = ', '.join(f"{k} {v}" for k, v in variables.items())
        qry = f"create table {table_name} ({new_cols})"
        print(qry)
        # SQL Execution
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(
            f"Created at {now}. NAME: {table_name}, COLUMNS: {variables.keys()}"
        )

        c = self.conn.cursor()
        c.execute(announce)
        c.execute(qry)
        self.conn.commit()
        c.close()

    def create_pkey(self, table_name:str, schema:str, database:str,
                    primary_key:Iterable):
        """
        """
        pk = ', '.join(primary_key)
        announce = f"use {database}"
        qry = f"alter table {table_name} "
        const = f"add constraint {table_name}_PK primary key ({pk})"

        c = self.conn.cursor()
        c.execute(announce)
        c.execute(f"{qry}{const}")
        self.conn.commit()
        c.close()

    def insert_row(self, table_name:str, schema:str, database:str, col_:Iterable,
                   rows_:[Iterable]):
        announce = f"use {database}"

        columns = ', '.join(str(_) for _ in col_)
        rows = ', '.join('%s' for _ in col_)

        qry = f"insert into {table_name} ({columns}) values ({rows})"
        print(qry)
        c = self.conn.cursor()
        c.execute(announce)
        c.executemany(qry, rows_)
        self.conn.commit()
        c.close()

    def select_db(self, database:str, schema:str, table:str, column:Iterable,
                  distinct=None, condition:str=None, orderby:str=None, groupby:str=None):
        """
        :param database: Name of the directory. ex) WOORIFS
        :param schema: Name of the schema. ex) dbo
        :param table: Name of the table. ex) BMKA1000
        :param column: target columns
        :param condition: WHERE condition for sql
        :param orderby: ORDER BY condition for sql
        :param groupby: GROUP BY condition for sql
        """
        cols = ', '.join(column)

        if distinct is None:
            qry = f"select {cols} from {database}.{schema}.{table}"
        else:
            qry = f"select distinct {distinct} from {database}.{schema}.{table}"

        if condition is not None:
            qry = f"{qry} where {condition}"

        if orderby is not None:
            qry = f"{qry} order by {orderby}"

        if groupby is not None:
            qry = f"{qry} group by {groupby}"
        # print(qry)

        # SQL Execution
        c = self.conn.cursor()
        c.execute(qry)
        row = c.fetchall()
        c.close()
        return [_ for _ in row]


if __name__ == '__main__':
    c = MSSQL().instance()
    # Login Test
    c.login(id='wsol1', pw='wsol1')

    tcol1 = ['FUND_ID', 'QTY_BEF', 'QTY_TR', 'QTY_CA', 'SEC_ID']
    tcol2 = ['STK_CD', 'ISIN_CD']
    var1 = c.select_db("WOORIFS", "dbo", "BMKA1000", column=tcol1, condition="PR_DATE=20210929 and SEC_ID='KR7089860001'")
    var2 = c.select_db("WFNS2DB", "", "TS_STOCK", column=tcol2)
