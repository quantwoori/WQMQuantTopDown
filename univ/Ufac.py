from rstrct.RSTuniv import UniverseRestrict
from abc import ABC, abstractmethod


class SmallUniverse(ABC):
    """
    Class Factory Hub of Creating Small Universe
    ----------------------------------------
    >> Universe Size : divided by (IKS002, IKS003, IKS004)
    >> Universe Style : divided by (..., ..., ...)
    """
    @abstractmethod
    def get_universe(self):
        pass


class UniverseSize(SmallUniverse):
    def get_universe(self):
        return None


class UniverseStyle(SmallUniverse):
    def get_universe(self):
        return None

