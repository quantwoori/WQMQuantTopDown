import pandas as pd


class BackTest:
    @staticmethod
    def monthly_return(price_info:pd.DataFrame):
        """
        Close to Close Return
        """
        p = price_info.bfill()
        start, end = p[:1], p[-1:]
        print(start.append(end))

        m_rtn = start.append(end).pct_change().dropna().transpose()
