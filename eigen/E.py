# Custom Package
from dbm.DBquant import PyQuantiwise
from dbm.DBmssql import MSSQL
from univ.Ufac import UniverseSizeFactory

# PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Other
import pandas as pd
from datetime import datetime


class EigenBackEnd:
    def __init__(self, date:datetime, portnumber:int, divide_std:str):
        # CLASS MODULES
        self.qt = PyQuantiwise()
        self.db = MSSQL.instance()
        self.db.login(id='wsol2', pw='wsol2')

        # CLASS CONSTANT
        assert divide_std in {'s', 'm', 'b'}
        self.DT = date
        self.PORTNO = portnumber
        self.STDARD = divide_std

    def match_hist_price(self, *args, **kwargs):
        pass

    def match_futr_price(self, *args, **kwargs):
        pass

    def get_univ(self, *args, **kwargs):
        pass

    def choose_eigp(self, *args, **kwargs):
        pass

    @staticmethod
    def _get_2eig(long_portfolio:pd.Series, short_portfolio:pd.Series,
                  direction:bool) -> pd.DataFrame:
        if direction is True:
            l = long_portfolio * 0
            return pd.concat([l, short_portfolio * -1])
        else:
            s = short_portfolio * 0
            return pd.concat([long_portfolio, s])

    def _calc_eig(self, d:pd.DataFrame):
        """
        Perform Principal Component Analysis.
        Find [self.PORTNO] weights.
        """
        # Normalize
        scalar = StandardScaler()
        df_norm = pd.DataFrame(
            scalar.fit_transform(d),
            index=d.index,
            columns=d.columns
        )

        # Calc Eigen Portfolio
        pca = PCA()
        pca.fit(df_norm)
        return pca.components_[:self.PORTNO]

    def get_eigp(self, data:pd.DataFrame) -> pd.DataFrame:
        """
        :param data: Price dataframe.
        :return:
        """
        df = data.bfill().pct_change().dropna()
        potential_w = self._calc_eig(df)
        result = pd.DataFrame(None)

        for i, weights in enumerate(potential_w):
            w = pd.Series(weights, index=df.columns)

            # Long Portfolio and Short Portfolio is generated
            w_long, w_short = w.loc[w >= 0], w.loc[w < 0]
            w_long, w_short = (w_long / abs(w_long.sum()),
                               w_short / abs(w_short.sum()))

            # Direction-wise portfolio
            wpos = self._get_2eig(w_long, w_short, True)
            wneg = self._get_2eig(w_long, w_short, False)

            result_seg = pd.concat([wpos, wneg], axis=1)
            result_seg.columns = [f"p{i}pos", f"p{i}neg"]
            result = pd.concat([result, result_seg], axis=1)
        return result

