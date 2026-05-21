import pandas as pd
import os
class DataCache:
    def __init__(self,cache_dir="./cache/data"):
        self.cache_dir=cache_dir
        os.makedirs(self.cache_dir,exist_ok=True)
    def save(self,symbol,df):
        file_path=os.path.join(self.cache_dir,f"{symbol}.csv")
        df=df.reset_index()
        df.to_csv(file_path,index=False)
    def load(self,symbol,parse_dates=["date"]):
        file_path=os.path.join(self.cache_dir,f"{symbol}.csv")
        if not os.path.exists(file_path):
            return None
        df=pd.read_csv(file_path,parse_dates=parse_dates)
        return df
    def exists(self,symbol):
        file_path=os.path.join(self.cache_dir,f"{symbol}.csv")
        return os.path.exists(file_path)