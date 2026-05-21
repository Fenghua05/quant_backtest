from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    def __init__(self, params=None):
        self.params = params or {}
    
    @abstractmethod
    def generate_signals(self, df):
        """输入 OHLCV DataFrame，输出带 signal 列的 DataFrame"""
        pass