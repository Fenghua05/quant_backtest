import pandas as pd
from .base_strategy import BaseStrategy

class MovingAverageCrossStrategy(BaseStrategy):
    def __init__(self,short_window:int=5,long_window:int=20):
        if not (isinstance(short_window, int) and isinstance(long_window, int)):
            raise TypeError("窗口天数必须为整数")
        if short_window <= 0 or long_window <= 0:
            raise ValueError("窗口天数必须大于0")
        if short_window >= long_window:
            raise ValueError("短期均线窗口必须小于长期均线窗口")

        self.short_window = short_window
        self.long_window = long_window

        strategy_params = {
            "short_window": short_window,
            "long_window": long_window
        }
        super().__init__(strategy_params)

    def generate_signals(self,df:pd.DataFrame):
        df=df.copy()
        if "close" not in df.columns:
            raise ValueError("输入的Dataframe应包含close列")
        df["short_ma"]=df["close"].rolling(window=self.short_window).mean()
        df["long_ma"]=df["close"].rolling(window=self.long_window).mean()
        df["signal"]=0

        golden_cross=(df["short_ma"]>df["long_ma"])&(
            df["short_ma"].shift(1)<=df["long_ma"].shift(1)
        )
        death_cross=(df["short_ma"]<df["long_ma"])&(
            df["short_ma"].shift(1)>=df["long_ma"].shift(1)
        )

        df.loc[golden_cross,"signal"]=1
        df.loc[death_cross,"signal"]=-1

        return df
            