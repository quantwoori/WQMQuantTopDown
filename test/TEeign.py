from eigen.Esize import Eigen
from datetime import datetime


test_date = datetime(2022, 2, 28)

# Test: Eigen Portfolio Building: Small
e = Eigen(test_date, 2, 's')

r = e.get_univ()
m = e.match_price(r)
n0 = e.get_eigp(m)


# Test2: Eigen Portfolio Building: Middle
e = Eigen(test_date, 2, 'm')

r = e.get_univ()
m = e.match_price(r)
n1 = e.get_eigp(m)


# Test3: Eigen Portfolio BUilding: Big
e = Eigen(test_date, 2, 'b')

r = e.get_univ()
m = e.match_price(r)
n2 = e.get_eigp(m)

