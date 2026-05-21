import rqdatac
rqdatac.init()

df = rqdatac.get_price(
    order_book_ids=['000001.XSHE'],
    start_date='20250101',
    end_date='20250501',
    frequency='1d'
)

print("类型:", type(df))
print("形状:", df.shape)
print("索引:", df.index[:5])
print("列名:", df.columns)
print("dtypes:", df.dtypes)