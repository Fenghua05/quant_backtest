from quant_backtest.strategy import MovingAverageCrossStrategy
from quant_backtest.data import DataFetcher,DataCache
import rqdatac
fetcher=DataFetcher()
cache=DataCache()
rqdatac.init()
df=fetcher.fetch_one("600000","20240101","20260501")
"""if df is not None:
    print("fetch_one成功")
    print(df.head())

    cache.save("600000",df)
    print(f"\ncache.exists('600000'):{cache.exists('600000')}")
    
    df_loaded = cache.load("600000")
    if df_loaded is not None:
        print(f"\n加载后date列类型:{df_loaded['date'].dtype}")"""
moving_strategy=MovingAverageCrossStrategy()
signal_df=moving_strategy.generate_signals(df)
df_change=signal_df[(signal_df["signal"]==1) | (signal_df["signal"]==-1)]
print(df_change)