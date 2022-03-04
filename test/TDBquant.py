from dbm.DBquant import PyQuantiwise

quantiwise = PyQuantiwise()

# Test.1 # stk_data
t1 = quantiwise.stk_data(
    stock_code='005930',
    start_date='20210101',
    end_date='20210201',
    item='수정주가'
)

# Test.2 # stk_data_multi
t2 = quantiwise.stk_data_multi(
    stock_code_ls=['005930', '000660'],
    start_date='20210101',
    end_date='20210201',
    item='수정주가'
)

# Test.3 # ind_data
t3 = quantiwise.ind_data(
    index_code='IKS002',
    start_date='20210101',
    end_date='20210201',
    item='종가지수'
)

# Test.4 # ind_data_multi
t4 = quantiwise.ind_data_multi(
    index_code_ls=['IKS001', 'IKS200'],
    start_date='20210101',
    end_date='20210201',
    item='종가지수'
)
