from univ.Ufac import UniverseSizeBig, UniverseSizeMiddle, UniverseSizeSmall
from univ.Ufac import UniverseSizeFactory

# Factory Test
sb = UniverseSizeBig()
sm = UniverseSizeMiddle()
ss = UniverseSizeSmall()

# Test: Small
small0 = ss.get_universe(2021, 1, True)  # KH03 Filter On
small1 = ss.get_universe(2021, 1, False)

# Test: Middle
middl0 = sm.get_universe(2021, 1, True)
middl1 = sm.get_universe(2021, 1, False)

# Test: Big
big0 = sb.get_universe(2021, 1, True)
big1 = sb.get_universe(2021, 1, False)

# Test: Factory
u = UniverseSizeFactory().create_universe('s').get_universe(2021, 1, True)
print(u)