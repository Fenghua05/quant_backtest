import rqdatac
import pandas as pd
class DataFetcher:
    def __init__(self):
        pass
    def _normalize_symbol(self,symbol):
        if symbol[0]==str(6):
            symbol=symbol+".XSHG"
            return symbol
        elif symbol[0]==str(0) or symbol[0]==str(3):
            symbol=symbol+".XSHE"
            return symbol
        else:
            raise ValueError("股票代码格式不对，请检查")
    def fetch_one(self,symbol,start_date,end_date,adjust_type='pre'):
        try:
            symbol=self._normalize_symbol(symbol)
            df = rqdatac.get_price(order_book_ids=symbol,start_date=start_date,end_date=end_date,adjust_type=adjust_type,frequency='1d')
            if df.empty:
                return None
            return df
        except Exception as e:
            print(f"股票{symbol}获取失败，原因：{str(e)}")
            return None
    def fetch_pool(self,symbols,start_date,end_date,adjust_type='pre'):
        result={}
        for symbol in symbols:
            df = self.fetch_one(symbol,start_date,end_date,adjust_type)
            if df is not None:
                result[symbol]=df
        return result
        