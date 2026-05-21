import pandas as pd

class DataCleaner:
    def __init__(self):
        pass
    def check_missing(self,df):
        if df.isnull().sum().sum()==0:
            print("没有缺失值")
        else:
            miss_col=df.isnull().sum()[df.isnull().sum()>0]
            print(f"缺失列为{miss_col}")
            print(f"缺失行有{df.isnull().any(axis=1).sum()}行")
    def check_price_anomaly(self, df):
        price_cols = ["open", "high", "low", "close", "limit_up", "limit_down"]
        existing_cols = [c for c in price_cols if c in df.columns]
        mask = (df[existing_cols] <= 0)
        if mask.any().any():
            bad_cols = mask.any()[mask.any()].index.tolist()
            raise ValueError(f"行情数据出现≤0的异常值，涉及列: {bad_cols}")